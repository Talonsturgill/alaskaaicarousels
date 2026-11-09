#!/usr/bin/env python3
"""akthree_soft_shadow_verify.py -- the reconstruction behind AKT.setup's
softShadows option and AKT.audit's shadow_radius_ignored finding (2026-11-08,
weekly pass; queue items No.104 2026-11-03 and No.106 2026-11-05).

THE DEFECT. three r170's PCFSoftShadowMap, akthree's default, reads no
shadow.radius on a directional or spot light: its shader chunk is a fixed 3x3
bilinear kernel. So a slide that writes `key.shadow.radius = 9` gets a hard
cast and no message. No.106's round 2 critics named a "hard black offset slab"
under the notice case on 01 and 09 until the slide switched to VSMShadowMap
with radius 9 and blurSamples 20; No.104 tried PCFShadowMap at radius 10 to 12
and got stepped bands; No.109 (2026-11-08) set VSM by hand on its GPU frame.

THE FIXTURES, run through the REAL render.py and qa.py. Each draws a ground
lit by AKT.rig's key and a box that CASTS but is not drawn (colorWrite off),
so the only edge in the frame is the cast's:
  01 default setup, the slide sets key.shadow.radius = 9 (No.106) -> WARN
  02 AKT.setup({softShadows: 9}) (the repair)                       -> clean
  03 default setup and AKT.rig untouched (the house default)        -> clean
and the cast edge is MEASURED: the 99.5th percentile of the luminance
gradient over the ground. 02's must be under 0.6 of 01's, which is the
penumbra the radius promised and PCFSoft never drew.

  python3 tests/akthree_soft_shadow_verify.py     # exit 0 = all hold
No network. Writes only into a scratch directory under out/ (gitignored).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
NEEDLE = "soft shadow asked for and not drawn"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#05080f}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;left:96px;top:96px;font:600 40px sans-serif;color:#eef4fc}</style>
</head><body data-breather><canvas id="scene" width="2160" height="2700"></canvas>
<div class="t">Soft shadow reconstruction</div>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('@@ASSETS@@/js/three.module.min.js');
  const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
  const R = AKT.setup(document.getElementById('scene'), SETUP);
  const made = AKT.rig(R, AKT.rigs.arcticNight);
BODY
  AKT.ground(R, { color: 0x8a96a4, y: 0 });
  const box = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.4, 1.4),
    new THREE.MeshStandardMaterial({ color: 0xffffff, colorWrite: false, depthWrite: false }));
  box.name = 'invisible caster'; box.position.y = 1.6; AKT.add(R, box);
  AKT.frame(R, { from: [0, 9, 0.01], look: [0, 0, 0], fov: 40 });
  await AKT.snapshot(R);
  return true;
})();
</script></body></html>"""

BASE = "{ w:1080, h:1350, bg:0x05080f, exposure:1.0 }"
SOFT = "{ w:1080, h:1350, bg:0x05080f, exposure:1.0, softShadows: 9 }"
CASES = [
    ("default setup, slide sets radius 9 (No.106)", True, BASE,
     "  made[0].shadow.radius = 9;"),
    ("softShadows: 9 (the repair)", False, SOFT, ""),
    ("default setup, house rig untouched", False, BASE, ""),
]


def edge(png):
    """99.5th percentile luminance gradient over the frame's ground (the middle)."""
    a = np.asarray(Image.open(png).convert("L"), dtype=np.float64)
    h, w = a.shape
    a = a[int(h * 0.2):int(h * 0.9), int(w * 0.1):int(w * 0.9)]
    gx = np.abs(np.diff(a, axis=1))[:-1, :]
    gy = np.abs(np.diff(a, axis=0))[:, :-1]
    return float(np.percentile(np.hypot(gx, gy), 99.5)), float(a.max() - a.min())


def main():
    scratch = ROOT / "out"
    scratch.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="softshadow_", dir=str(scratch)))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_n, _w, setup, body) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(HEAD.replace("SETUP", setup).replace("BODY", body))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
        edges = {}
        for i in range(1, len(CASES) + 1):
            p = tmp / "render" / f"slide-0{i}.png"
            edges[i] = edge(p) if p.exists() else None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, should_warn, _s, _b) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None or edges.get(i) is None:
            ok = False
            print("[BROKE] %-46s -> slide never rendered" % name)
            continue
        hits = [w for w in s["warns"] + s["fails"] if NEEDLE in w]
        good = bool(hits) if should_warn else not hits
        ok &= good
        print("[%s] %-46s -> %s | cast edge %.1f levels/px, range %.0f" % (
            "HOLD" if good else "BROKE", name, hits[0][:110] if hits else "clean",
            edges[i][0], edges[i][1]))
    if edges.get(1) and edges.get(2):
        hard, soft = edges[1][0], edges[2][0]
        good = edges[1][1] > 20 and soft < 0.6 * hard
        ok &= good
        print("[%s] the repair softens the cast: %.1f against %.1f (%.2f, must be under 0.60; "
              "the fixture's cast spans %.0f levels)" % (
                  "HOLD" if good else "BROKE", soft, hard, soft / max(hard, 1e-6), edges[1][1]))
    print("akthree_soft_shadow_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
