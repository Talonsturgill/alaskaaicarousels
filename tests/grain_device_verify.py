#!/usr/bin/env python3
"""grain_device_verify.py -- the reconstruction behind AK.grainOn (2026-10-11,
weekly machine pass).

WHAT IT RECONSTRUCTS. No.84's round 3 critics named "a faint regular dot
lattice" in the near-black skies of slides 07, 08 and 09. The grain tile was the
house pairing, AK.grainTile(280, ...) shown at 280 CSS px, and the engine renders
at deviceScaleFactor 2, so every grain cell landed on 2 x 2 device pixels. The
run fixed it by hand (a 560 px tile at background-size 280px). AK.grainOn makes
that the helper's job, and AKINLET.grain and AKPOUR.grainOn now go through it.

    python3 tests/grain_device_verify.py      # exit 0 = every check holds

It runs the REAL noise.js, akinlet.js and akpour.js in the engine's own browser
(render.launch_chromium) at deviceScaleFactor 2, and reads device pixels back.

  defect    the old pairing (a 280 px tile at 280 CSS px) correlates neighbouring
            device pixels at 0.5 or more (measured 0.75): the cells are 2 px wide.
  grainOn   AK.grainOn correlates them under 0.15 (measured 0.00): one cell
            per device pixel.
  canvas    AKINLET.grain on a 2x-scaled canvas is under 0.15 too, and the
            committed (git HEAD) akinlet.js is held to the defect bound, so
            the check is shown to fail on the code it replaced.
  akpour    AKPOUR.grainOn is under 0.15.
  parity    AK.grainTile(280, 46, 1) with no scale returns the same tile as the
            committed noise.js, so no existing slide changes.
  alias     AK.noise2 and AK.noise3 are simplex2 and simplex3.
"""

import io
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

JS = ROOT / "assets" / "js"
DEFECT_MIN = 0.5     # the 2x2 cell: lag-1 correlation at or above this
CLEAN_MAX = 0.15     # one cell per device pixel: under this


def head_copy(rel, dest):
    """The committed version of a file, written to dest (for the parity and
    the defect checks against the code this change replaced)."""
    out = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:" + rel],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    dest.write_text(out.stdout)
    return dest


def lag1(a):
    """Mean lag-1 autocorrelation of a grey image, across and down."""
    r = a.astype(np.float64) - a.mean()
    v = r.var()
    if v == 0:
        return 0.0
    return float(((r[:, :-1] * r[:, 1:]).mean() + (r[:-1, :] * r[1:, :]).mean()) / (2 * v))


PAGE = """<!doctype html><html><body style="margin:0;background:#808080">
<div id="g" style="position:absolute;left:0;top:0;width:540px;height:540px"></div>
<canvas id="c" width="1080" height="1080"
  style="position:absolute;left:0;top:0;width:540px;height:540px;display:none"></canvas>
<script src="NOISE"></script>
<script src="EXTRA"></script>
<script>
window.renderReady = (async () => {
  const mode = "MODE", g = document.getElementById("g"), c = document.getElementById("c");
  if (mode === "defect") {
    g.style.backgroundImage = "url(" + AK.grainTile(280, 46, 7) + ")";
  } else if (mode === "grainOn") {
    AK.grainOn(g, {size: 280, strength: 46, seed: 7});
  } else if (mode === "akpour") {
    AKPOUR.grainOn(g, 7, 1);
  } else if (mode === "canvas") {
    g.style.display = "none"; c.style.display = "block";
    const cx = c.getContext("2d"); cx.scale(2, 2);
    cx.fillStyle = "#808080"; cx.fillRect(0, 0, 540, 540);
    await AKINLET.grain(cx, 540, 540, 7);
  } else if (mode === "probe") {
    return JSON.stringify({
      tile: AK.grainTile(280, 46, 1),
      n2: AK.noise2 === AK.simplex2, n3: AK.noise3 === AK.simplex3,
      v: typeof AK.noise2 === "function" && AK.noise2(0.31, 0.77) === AK.simplex2(0.31, 0.77)});
  }
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  return "ok";
})();
</script></body></html>"""


def run(browser, tmp, mode, noise, extra):
    f = tmp / ("grain_%s_%s.html" % (mode, extra.stem))
    f.write_text(PAGE.replace("NOISE", noise.as_uri()).replace("EXTRA", extra.as_uri())
                 .replace("MODE", mode))
    page = browser.new_page(viewport={"width": 540, "height": 540}, device_scale_factor=2)
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(f.as_uri(), wait_until="load", timeout=60000)
    res = page.evaluate("() => window.renderReady")
    shot = None
    if mode != "probe":
        shot = np.asarray(Image.open(io.BytesIO(page.screenshot())).convert("L"))[60:1020, 60:1020]
    page.close()
    return res, shot, errs


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium
    import json

    bad, seen = [], []
    with tempfile.TemporaryDirectory() as d, sync_playwright() as p:
        tmp = Path(d)
        old_noise = head_copy("assets/js/noise.js", tmp / "noise_head.js")
        old_inlet = head_copy("assets/js/akinlet.js", tmp / "akinlet_head.js")
        b = launch_chromium(p)
        try:
            noise = JS / "noise.js"
            _, a, e = run(b, tmp, "defect", noise, JS / "akinlet.js")
            c_def = lag1(a)
            seen.append("defect %.2f" % c_def)
            if c_def < DEFECT_MIN:
                bad.append("defect did not reproduce: a 280 px tile at 280 CSS px "
                           "correlates %.2f, expected %.2f or more" % (c_def, DEFECT_MIN))
            _, a, e2 = run(b, tmp, "grainOn", noise, JS / "akinlet.js")
            c_on = lag1(a)
            seen.append("grainOn %.2f" % c_on)
            if c_on >= CLEAN_MAX or a.std() < 2:
                bad.append("AK.grainOn correlates %.2f (std %.1f): not one cell per "
                           "device pixel" % (c_on, a.std()))
            _, a, e3 = run(b, tmp, "akpour", noise, JS / "akpour.js")
            c_pour = lag1(a)
            seen.append("akpour %.2f" % c_pour)
            if c_pour >= CLEAN_MAX or a.std() < 2:
                bad.append("AKPOUR.grainOn correlates %.2f (std %.1f)" % (c_pour, a.std()))
            _, a, e4 = run(b, tmp, "canvas", noise, JS / "akinlet.js")
            c_can = lag1(a)
            seen.append("AKINLET.grain %.2f" % c_can)
            if c_can >= CLEAN_MAX or a.std() < 0.8:
                bad.append("AKINLET.grain on a 2x canvas correlates %.2f (std %.2f)"
                           % (c_can, a.std()))
            if old_inlet:
                _, a, _ = run(b, tmp, "canvas", noise, old_inlet)
                c_old = lag1(a)
                seen.append("AKINLET.grain at HEAD %.2f" % c_old)
                if c_old < DEFECT_MIN and "grainTile(280, 52, seed, sc)" not in old_inlet.read_text():
                    bad.append("the committed AKINLET.grain correlates %.2f: the "
                               "canvas check would not have caught it" % c_old)
            res, _, e5 = run(b, tmp, "probe", noise, JS / "akinlet.js")
            pr = json.loads(res)
            if not (pr["n2"] and pr["n3"] and pr["v"]):
                bad.append("AK.noise2 / AK.noise3 are not simplex2 / simplex3: %s" % pr)
            if old_noise:
                res_old, _, _ = run(b, tmp, "probe", old_noise, JS / "akinlet.js")
                if json.loads(res_old)["tile"] != pr["tile"]:
                    bad.append("parity: AK.grainTile(280, 46, 1) changed its tile")
            for errs in (e, e2, e3, e4, e5):
                if errs:
                    bad.append("page error: %s" % errs[0][:200])
        finally:
            b.close()

    print("measured lag-1 correlation: " + ", ".join(seen))
    if bad:
        print("BROKEN")
        for x in bad:
            print(" - " + x)
        return 1
    print("HOLDS: the old pairing reproduces the 2 px cell, AK.grainOn, AKPOUR.grainOn "
          "and AKINLET.grain put one grain cell on one device pixel, the bare tile is "
          "unchanged, and AK.noise2 / noise3 are the simplex functions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
