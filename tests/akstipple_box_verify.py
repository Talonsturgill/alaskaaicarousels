#!/usr/bin/env python3
"""akstipple_box_verify.py -- the reconstruction behind AKSTIPPLE.field's
corner-box contract (2026-10-25 weekly pass, queue item of 2026-10-23).

THE DEFECT. No.94 slide 08 passed `box` as a size, [x, y, w, h]. field() reads
corners, [x0, y0, x1, y1], so y1 fell above y0, the throws landed on a strip
outside the borough, the borough came out empty, and no gate said anything.

THE FIXTURES, through the REAL render.py and qa.py:
  01 box as a size, [120, 420, 840, 300] (y1 < y0)   -> library contract FAIL
  02 the same region as corners, [120, 420, 960, 720] -> clean
  03 no box (the default full frame)                  -> clean

  python3 tests/akstipple_box_verify.py     # exit 0 = all three hold
No network. Writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
NEEDLE = "AKSTIPPLE.field: `box`"

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#081018}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
h1{position:absolute;left:80px;top:1120px;font:600 60px sans-serif;color:#F4F8FF}</style>
<script src="@@ASSETS@@/js/noise.js"></script>
<script src="@@ASSETS@@/js/akstipple.js"></script>
</head><body><canvas id="c" width="2160" height="2700"></canvas><h1>Stipple box fixture</h1>
<script>
window.renderReady = (async () => {
  await document.fonts.ready;
  const cx = document.getElementById('c').getContext('2d'); cx.scale(2, 2);
  try {
    AKSTIPPLE.field(cx, { seed: 7, count: 20000, w: 1080, h: 1350BOX,
      height: (x, y) => (x > 120 && x < 960 && y > 420 && y < 720) ? 0.8 : 0 });
  } catch (e) { /* a slide that swallows the throw: the console.error still reaches qa */ }
  return true;
})();
</script></body></html>"""

CASES = [
    ("box as a size (No.94 08)", True, ", box: [120, 420, 840, 300]"),
    ("box as corners (the repair)", False, ", box: [120, 420, 960, 720]"),
    ("no box", False, ""),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="stipplebox_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, _f, box) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(PAGE.replace("BOX", box))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, should_fail, _b) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None:
            ok = False
            print("[BROKE] %-34s -> slide never rendered" % name)
            continue
        hits = [f for f in s["fails"] if NEEDLE in f]
        good = bool(hits) if should_fail else not any(NEEDLE in w for w in s["fails"] + s["warns"])
        ok &= good
        print("[%s] %-34s -> %s" % ("HOLD" if good else "BROKE", name,
                                    hits[0][:140] if hits else "clean"))
    print("akstipple_box_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
