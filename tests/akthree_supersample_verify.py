#!/usr/bin/env python3
"""akthree_supersample_verify.py -- the reconstruction behind AKT.setup's
opt-in `supersample` and AKT.drawDown (2026-10-06, weekly machine pass).

WHAT IT RECONSTRUCTS. No.79 drew a 10,500-seat hall in akthree. At the 2x
backing the seat rows sat near 2 device px apart and BEAT into moire (scanline
hatch, stair-stepped wedge edges) on slides 02 and 05; two pixel-critic rounds
named it, a 0.7 px blur did not cure it, and a hand-rolled 3x render drawn down
did. The option makes that the helper's job.

  python3 tests/akthree_supersample_verify.py      # exit 0 = every check holds

It runs the REAL akthree.js and three.module.min.js in the engine's own
browser (render.launch_chromium), on a scene of the same kind: 14,400 instanced
seat blocks in rows at a pitch near 2 device px, under an orthographic camera.

  moire     the beat is the LOW-FREQUENCY part of the error against a 6x
            area-resolved reference (a 9 px box blur of the difference, which a
            sharpness difference can't survive and a beat does). The 2x render
            must carry it, supersample 3 must remove at least 40 percent of it
            (measured: half).
  resolve   the area resolve is closer to the reference, on both measures,
            than the browser's own drawImage downscale with
            imageSmoothingQuality high, the hand-rolled way No.79 used.
  parity    without the option, the new akthree.js renders the same pixels as
            the committed one (git HEAD), so no existing slide changes.
  contract  supersample outside 2 to 4 throws an AK CONTRACT error.
"""

import base64
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

PAGE = r"""<!doctype html><html><body style="margin:0;background:#000">
<canvas id="c" width="1080" height="1350" style="width:540px;height:675px"></canvas>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('THREE_URL');
  const AKT = (await import('AKT_URL')).init(THREE);
  const mode = 'MODE';
  const canvas = document.getElementById('c');
  if (mode === 'contract') {
    try { AKT.setup(canvas, { w: 540, h: 675, supersample: 6 }); return 'no-throw'; }
    catch (e) { return String(e.message || e); }
  }
  let R, opts = { w: 540, h: 675, bg: 0x070B12, exposure: 1.15 };
  if (mode === 'ss3' || mode === 'ss3smooth') opts.supersample = 3;
  if (mode === 'ref') { canvas.width = 3240; canvas.height = 4050; }
  R = AKT.setup(canvas, opts);
  const PPM = 1.8, PITCH = 50 * Math.PI / 180;
  const cam = new THREE.OrthographicCamera(-270 / PPM, 270 / PPM, 337.5 / PPM, -337.5 / PPM, 1, 600);
  const dir = new THREE.Vector3(0, -Math.sin(PITCH), Math.cos(PITCH));
  const target = new THREE.Vector3(0, 10, 50);
  cam.position.copy(target).addScaledVector(dir, -200); cam.lookAt(target);
  cam.updateProjectionMatrix(); R.camera = cam;
  const key = new THREE.DirectionalLight(0xDCEEF6, 2.6); key.position.set(26, 46, -40);
  R.scene.add(key); R.scene.add(new THREE.HemisphereLight(0x5B7F93, 0x060A12, 0.8));
  // seat rows: a wedge of rows at a pitch near 2 device px, each row a run of
  // seat blocks with a lit back and a dark slot between, slightly fanned so the rows
  // and the pixel grid drift in and out of phase
  const g = new THREE.BoxGeometry(0.42, 0.34, 0.30);
  const m = new THREE.MeshStandardMaterial({ color: 0x9FB4C2, roughness: 0.6 });
  const N = 14400, inst = new THREE.InstancedMesh(g, m, N), M4 = new THREE.Matrix4();
  let k = 0;
  for (let r = 0; r < 120 && k < N; r++) {
    const rad = 30 + r * 0.62, y = r * 0.205;
    for (let s = 0; s < 120 && k < N; s++) {
      const a = -0.62 + 1.24 * s / 119;
      M4.makeRotationY(a); M4.setPosition(rad * Math.sin(a), y, rad * Math.cos(a) - 6);
      inst.setMatrixAt(k++, M4);
    }
  }
  inst.count = k; R.scene.add(inst);
  let out;
  if (mode === 'ss3smooth') {
    const shot = await AKT.snapshot(R, { resolve: false });
    const cx = canvas.getContext('2d');
    cx.imageSmoothingEnabled = true; cx.imageSmoothingQuality = 'high';
    cx.drawImage(R.glCanvas, 0, 0, 1080, 1350);
    out = canvas.toDataURL('image/png');
    return JSON.stringify({ ok: shot.ok, png: out });
  }
  const shot = await AKT.snapshot(R);
  if (mode === 'ref') {
    const dst = document.createElement('canvas'); dst.width = 1080; dst.height = 1350;
    AKT.drawDown(dst.getContext('2d'), canvas);
    out = dst.toDataURL('image/png');
  } else {
    out = canvas.toDataURL('image/png');
  }
  return JSON.stringify({ ok: shot.ok, png: out, kind: canvas.getContext ? 'x' : '' });
})();
</script></body></html>"""


def lum(png_b64):
    im = Image.open(io.BytesIO(base64.b64decode(png_b64.split(",", 1)[1]))).convert("RGB")
    a = np.asarray(im, dtype=np.float64)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def box(a, k=9):
    c = np.cumsum(np.cumsum(np.pad(a, ((1, 0), (1, 0))), 0), 1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def render(page, mode, akt_url):
    three = (ROOT / "assets/js/three.module.min.js").as_uri()
    html = PAGE.replace("THREE_URL", three).replace("AKT_URL", akt_url).replace("MODE", mode)
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "p.html"
        f.write_text(html)
        page.goto(f.as_uri(), wait_until="load", timeout=120000)
        res = page.evaluate("() => window.renderReady")
    return res


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium
    new_url = (ROOT / "assets/js/akthree.js").as_uri()
    head = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:assets/js/akthree.js"],
                          capture_output=True, text=True, check=True).stdout
    checks, out = [], {}
    with tempfile.TemporaryDirectory() as td, sync_playwright() as p:
        old = Path(td) / "akthree_head.js"
        old.write_text(head)
        b = launch_chromium(p)
        imgs = {}
        for mode, url in (("plain", new_url), ("ss3", new_url), ("ss3smooth", new_url),
                          ("ref", new_url), ("plain_head", old.as_uri())):
            page = b.new_page(viewport={"width": 540, "height": 675}, device_scale_factor=2)
            r = json.loads(render(page, "plain" if mode == "plain_head" else mode, url))
            page.close()
            if not r["ok"]:
                checks.append((False, f"{mode}: snapshot not ok"))
            imgs[mode] = lum(r["png"])
        page = b.new_page()
        msg = render(page, "contract", new_url)
        page.close()
        b.close()

    ref = imgs["ref"]
    for k in ("plain", "ss3", "ss3smooth"):
        d = imgs[k] - ref
        out[k] = {"rmse": float(np.sqrt((d ** 2).mean())),
                  "lowpass_rmse": float(np.sqrt((box(d) ** 2).mean()))}
    print(json.dumps(out, indent=1))
    lp_plain, lp_ss3 = out["plain"]["lowpass_rmse"], out["ss3"]["lowpass_rmse"]
    # measured 2026-10-06: 2x 0.492, supersample 3 0.247 (0.50 of it), the
    # hand-rolled drawImage resolve 0.353; the bars sit under those with margin
    checks.append((lp_ss3 <= 0.6 * lp_plain,
                   f"moire: low-pass error vs the 6x reference, 2x {lp_plain:.3f}, "
                   f"supersample 3 {lp_ss3:.3f} (must remove at least 40 percent)"))
    lp_sm = out["ss3smooth"]["lowpass_rmse"]
    checks.append((lp_ss3 < lp_sm and out["ss3"]["rmse"] <= out["ss3smooth"]["rmse"],
                   f"resolve: area resolve low-pass {lp_ss3:.3f} vs drawImage high {lp_sm:.3f}, "
                   f"rmse {out['ss3']['rmse']:.3f} vs {out['ss3smooth']['rmse']:.3f}"))
    same = np.array_equal(imgs["plain"], imgs["plain_head"])
    checks.append((same, "parity: no option renders the same pixels as git HEAD's akthree.js"
                   + ("" if same else f" (max diff {np.abs(imgs['plain'] - imgs['plain_head']).max():.1f})")))
    checks.append((str(msg).startswith("AK CONTRACT:"), f"contract: supersample 6 -> {str(msg)[:70]}"))
    bad = 0
    for ok, m in checks:
        print(("PASS " if ok else "FAIL ") + m)
        bad += 0 if ok else 1
    print(f"{len(checks) - bad}/{len(checks)} checks hold")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
