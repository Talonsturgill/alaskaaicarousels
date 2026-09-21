#!/usr/bin/env python3
"""axis_origin_verify.py -- the reconstruction behind qa.py's 2026-09-21 repair
to the axis census's ORIGIN. One defect from run No.65, three fixtures, one
drawing.

THE DEFECT. `data-scale` declares an axis with two endpoints in design px, and
a slide is entitled to declare an endpoint OFF THE FRAME: a camera that has
descended past the top of its own scale draws only the part of the axis that is
still on screen, and the honest declaration is the one the drawing code uses,
`"to":[-180,59]`. The census sampled that correctly -- it clamps the sample
window to the frame, `r0 = max(0, int(lo * ns))` -- and then set
`origin = lo`, the UNCLAMPED minimum. So the profile it had just built started
at design px 0 while every lookup into it was computed from -180, and every
`peak_at(p)` read the profile exactly 180 px away from the mark it was asking
about. Same arithmetic in `_census_band_hunt`, whose `origin_axis = lo` sits two
lines under an `origin_perp` that does the clamped division correctly.

WHAT IT COST. Run No.65's round one: four frames, four confident and precisely
worded census warns, every one of them wrong. Slide 06 declared `to:[-180,59]`
and the gate reported "the nearest mark-strength ink to the mark declared at 418
is at 238, 180 px away" -- 180 is the clamp, reported as a drawing defect. The
showrunner spent a round on stroke weights and then re-declared four axes AS
DRAWN to get past it, which is a workaround: it makes the declaration describe
the visible fragment rather than the scale the slide actually measures against.

THE FIXTURES, one day rule of four ticks, drawn identically in all three:

  1. y axis declared to [-180,59], above the frame  -> clean, the census reads it
  2. the same drawing declared only where it is drawn -> clean (nothing regressed)
  3. x axis declared from [-200,0], left of the frame -> clean, both branches

Fixture 2 is the control: it is the workaround No.65 shipped, and it passed
before this repair as well as after, so a green 2 beside a red 1 and 3 is the
signature of the bug and not of the drawing.

Before the repair, fixtures 1 and 3 each warn that every declared mark is dead
and name ink found "180 px away" / "200 px away". After it, all three are clean.

Usage: python tests/axis_origin_verify.py   (exit 0 = all three hold)
Renders with the engine's own render.py and judges with its own qa.py. No
network. Writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENGINE = REPO / ".claude" / "skills" / "carousel-engine"

Y_MARKS = [150, 450, 750, 1050]      # design px, all inside the frame
X_MARKS = [100, 400, 700, 1000]

HEAD = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#141821; position:relative; color:#E7EDF3; }
  canvas { position:absolute; inset:0; }
</style></head><body data-scale='%s'>
<canvas id="c" width="2160" height="2700" style="width:1080px;height:1350px"></canvas>
<script type="module">
  const cx = document.getElementById('c').getContext('2d');
  cx.scale(2, 2);
  const W = 1080, H = 1350;
  let s = 20260921;
  const rnd = () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  cx.fillStyle = '#141821';
  cx.fillRect(0, 0, W, H);
  for (let i = 0; i < 3000; i++) {           /* a little ground texture */
    cx.fillStyle = 'rgba(180,200,225,' + (0.02 + 0.05 * rnd()).toFixed(3) + ')';
    cx.fillRect(rnd() * W, rnd() * H, 2 + 3 * rnd(), 2 + 3 * rnd());
  }
  cx.fillStyle = '#C8D6E6';
  const AXIS = '@@AXIS@@';
  if (AXIS === 'y') {
    /* four ticks crossing the strip x830-890, at y150/450/750/1050 */
    for (const y of [150, 450, 750, 1050]) cx.fillRect(830, y - 3, 60, 6);
  } else {
    /* four ticks crossing the strip y600-660, at x100/400/700/1000 */
    for (const x of [100, 400, 700, 1000]) cx.fillRect(x - 3, 600, 6, 60);
  }
</script>
</body></html>
"""


def y_scale(frm, to):
    span = float(to[0] - frm[0])
    return json.dumps([{
        "what": "the descent rule", "axis": "y", "unit": "days",
        "from": [frm[0], frm[1]], "to": [to[0], to[1]], "band": [820, 900],
        "marks": [{"at": p,
                   "means": "day %d" % round(frm[1] + (p - frm[0]) *
                                             (to[1] - frm[1]) / span)}
                  for p in Y_MARKS],
    }], separators=(",", ":"))


def x_scale(frm, to):
    span = float(to[0] - frm[0])
    return json.dumps([{
        "what": "the comment window", "axis": "x", "unit": "days",
        "from": [frm[0], frm[1]], "to": [to[0], to[1]], "band": [600, 660],
        "marks": [{"at": p,
                   "means": "day %d" % round(frm[1] + (p - frm[0]) *
                                             (to[1] - frm[1]) / span)}
                  for p in X_MARKS],
    }], separators=(",", ":"))


# (name, axis, scale declaration)
CASES = [
    ("y axis declared to [-180,59], above the frame", "y",
     y_scale([1050, 0], [-180, 59])),
    ("the same drawing declared only where it is drawn", "y",
     y_scale([1050, 0], [150, 43])),
    ("x axis declared from [-200,0], left of the frame", "x",
     x_scale([-200, 0], [1000, 12])),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="axisorigin_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, axis, decl) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(
            (HEAD % decl).replace("@@AXIS@@", axis))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=900)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=900)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, _axis, _decl) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None:
            print("[BROKE] %-52s -> slide never rendered" % name)
            ok = False
            continue
        hits = [f for f in s.get("warns", []) if "axis census" in f]
        hits += [f for f in s.get("fails", []) if "a mark on a measured axis" in f]
        # and the census has to have RUN and read the marks, not merely stayed
        # quiet: its clean verdict is an info line naming the declared marks.
        ran = [d for d in s.get("scales", []) if "declared mark" in d]
        good = not hits and bool(ran)
        ok &= good
        print("[%s] %-52s -> %s" % ("HOLD" if good else "BROKE", name,
                                    (hits[0][:220] if hits else
                                     (ran[0][:120] if ran else
                                      "the census never ran on this slide"))))
    print("axis_origin_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
