#!/usr/bin/env python3
"""akpost_grade_scale_verify.py -- the reconstruction behind AKPOST.grade's
quarter-frame contract (2026-11-01 weekly pass, No.102 incident).

THE DEFECT. No.102 slide 01 called AKPOST.grade(cx, {w: 1080, h: 1350}) on a
2160 x 2700 backing whose transform had been reset to identity. grade() sizes
its read from the context's current scale, so it graded the top-left 1080 x
1350 device px, a quarter of the frame, and left a visible seam. Every gate
passed; the critics found it.

THE FIXTURES, through the REAL render.py and qa.py:
  01 identity transform on the 2x backing, {w: 1080, h: 1350}  -> contract FAIL
  02 scale(2) set first, the same call (the cure)              -> clean
  03 identity transform, {w: 2160, h: 2700} (the other cure)   -> clean
  04 a 1x offscreen canvas graded at its own size              -> clean
And the pixels: on fixture 01 the bottom-right quarter is ungraded (its mean
equals the ungraded fill) while the top-left is graded, which is the seam.

  python3 tests/akpost_grade_scale_verify.py     # exit 0 = all hold
No network. Writes only into a temp directory.
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
NEEDLE = "AKPOST.grade({w:"

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#081018}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
h1{position:absolute;left:80px;top:1120px;font:600 60px sans-serif;color:#F4F8FF}</style>
<script src="@@ASSETS@@/js/akpost.js"></script>
</head><body><canvas id="c" width="2160" height="2700"></canvas><h1>Grade scale fixture</h1>
<script>
window.renderReady = (async () => {
  await document.fonts.ready;
  const cx = document.getElementById('c').getContext('2d');
  cx.fillStyle = '#3A5068'; cx.fillRect(0, 0, 2160, 2700);
  BODY
  return true;
})();
</script></body></html>"""

GRADE = "{exposure: 0.6, saturation: 1, contrast: 1.3, filmic: true, dither: false}"
CASES = [
    ("identity on 2x, design w/h (No.102 01)", True,
     "cx.setTransform(1,0,0,1,0,0); AKPOST.grade(cx, Object.assign({w: 1080, h: 1350}, %s));" % GRADE),
    ("scale(2) first (the cure)", False,
     "cx.setTransform(2,0,0,2,0,0); AKPOST.grade(cx, Object.assign({w: 1080, h: 1350}, %s));" % GRADE),
    ("identity, backing w/h (the other cure)", False,
     "cx.setTransform(1,0,0,1,0,0); AKPOST.grade(cx, Object.assign({w: 2160, h: 2700}, %s));" % GRADE),
    ("1x offscreen at its own size", False,
     "const o = document.createElement('canvas'); o.width = 1080; o.height = 1350; "
     "const oc = o.getContext('2d'); oc.fillStyle = '#3A5068'; oc.fillRect(0, 0, 1080, 1350); "
     "AKPOST.grade(oc, Object.assign({w: 1080, h: 1350}, %s)); "
     "cx.setTransform(1,0,0,1,0,0); cx.drawImage(o, 0, 0, 2160, 2700);" % GRADE),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="gradescale_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, _f, body) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(PAGE.replace("BODY", body))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
        png = tmp / "render" / "slide-01.png"
        px = np.asarray(Image.open(png).convert("RGB")).astype(float) if png.exists() else None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, should_fail, _b) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None:
            ok = False
            print("[BROKE] %-42s -> slide never rendered" % name)
            continue
        hits = [f for f in s["fails"] if NEEDLE in f]
        good = bool(hits) if should_fail else not any(NEEDLE in w for w in s["fails"] + s["warns"])
        ok &= good
        print("[%s] %-42s -> %s" % ("HOLDS" if good else "BROKE", name,
                                    (hits[0][:150] if hits else "no grade contract finding")))
    if px is not None:
        h, w = px.shape[:2]
        tl = px[: h // 4, : w // 4].mean()
        br = px[3 * h // 4:, 3 * w // 4:].mean()
        seam = abs(tl - br) > 8
        ok &= seam
        print("[%s] fixture 01 pixels: top-left mean %.1f, bottom-right mean %.1f (%s)"
              % ("HOLDS" if seam else "BROKE", tl, br,
                 "the quarter-frame seam is real" if seam else "no seam reproduced"))
    else:
        ok = False
        print("[BROKE] fixture 01 png missing")
    print("ALL HOLD" if ok else "BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
