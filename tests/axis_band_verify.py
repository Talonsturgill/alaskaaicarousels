#!/usr/bin/env python3
"""axis_band_verify.py -- the reconstruction behind qa.py's 2026-09-10 checks on
a `data-scale` band. One defect from run No.55, three fixtures, one drawing.

THE DEFECT. `data-scale`'s "band" is the strip the scale owns ACROSS its own
axis, [y0,y1] for an x axis, and it is what the pixel census samples. Written as
an [x,y,w,h] artwork rect it still parsed: render.py kept the first two numbers
and qa.py asked for two. BOTH slides in No.55 that declared a scale did it --
slide 04 declared [130,790,860,130] so the census read y130-790 while the ticks
drew at y859, slide 08 declared [170,640,740,72] and read y170-640 while the
rule drew at y676 -- and every mark came back at ink 0.0 to 0.6. The message the
run acted on ("no stronger than the band's own texture") describes a drawing
that is too faint, so two repair rounds went to stroke weights. Nothing was
wrong with either drawing.

THE TWO CHECKS. The first is a hard FAIL on the arity, for the same reason an
unparseable declaration is one: the census RAN and printed values about a strip
of the frame the scale does not own. The second is the diagnosis for the case
the arity check cannot see, a well-formed two-number band simply aimed off the
marks: when EVERY declared mark reads dead, the census hunts across the axis for
the strip where those same marks do carry ink, and names it.

THE FIXTURES, one day rule with five declared ticks, drawn identically in all
three:

  1. band as an [x,y,w,h] rect                -> FAILS, and names "band":[660,700]
  2. the same slide, band [660,700]           -> clean, the census reads the marks
  3. a two-number band aimed at blank ground  -> WARNS, and finds the marks' strip

Fixture 2 is what keeps the arity check honest: it is the same drawing with the
one-line repair applied, so neither check fires on the idiom itself.

Usage: python tests/axis_band_verify.py   (exit 0 = all three hold)
Renders with the engine's own render.py and judges with its own qa.py. No
network. Writes only into a temp directory.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENGINE = REPO / ".claude" / "skills" / "carousel-engine"

MARKS = [190, 365, 540, 715, 890]

HEAD = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#141821; font-family:"JetBrains Mono", monospace;
         position:relative; color:#E7EDF3; }
  canvas { position:absolute; inset:0; }
</style></head><body data-scale='%s'>
<canvas id="c" width="2160" height="2700" style="width:1080px;height:1350px"></canvas>
<script type="module">
  const cx = document.getElementById('c').getContext('2d');
  cx.scale(2, 2);
  const W = 1080, H = 1350;
  let s = 20260910;
  const rnd = () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  cx.fillStyle = '#141821';
  cx.fillRect(0, 0, W, H);
  for (let i = 0; i < 3000; i++) {           /* a little ground texture */
    cx.fillStyle = 'rgba(180,200,225,' + (0.02 + 0.05 * rnd()).toFixed(3) + ')';
    cx.fillRect(rnd() * W, rnd() * H, 2 + 3 * rnd(), 2 + 3 * rnd());
  }
  /* THE DAY RULE. Identical in all three fixtures: a thin rule at y676 and
     five ticks crossing the strip y652-708. */
  cx.fillStyle = '#C8D6E6';
  cx.fillRect(190, 673, 700, 5);
  for (const x of [190, 365, 540, 715, 890]) cx.fillRect(x - 3, 652, 6, 56);
</script>
</body></html>
"""


def scale_decl(band):
    return json.dumps([{
        "what": "the fourteen day rule", "axis": "x", "unit": "days",
        "from": [190, 0], "to": [890, 14], "band": band,
        "marks": [{"at": p, "means": "day %d" % ((p - 190) / 50.0)}
                  for p in MARKS],
    }], separators=(",", ":"))


# (name, band as declared, should_be_clean, needle, which list it lands in)
CASES = [
    ("band written as an [x,y,w,h] rect", [190, 660, 700, 40], False,
     '"band" declares 4 numbers and it takes exactly 2', "fails"),
    ("the same slide with band [660,700]", [660, 700], True,
     '"band" declares', "fails"),
    ("a two-number band aimed at blank ground", [560, 600], False,
     "CHECK THE BAND BEFORE THE DRAWING", "warns"),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="axisband_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, band, _ok, _n, _w) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(HEAD % scale_decl(band))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=600)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=600)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, _band, should_pass, needle, where) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html", {"fails": ["slide never rendered"],
                                        "warns": ["slide never rendered"]})
        hits = [f for f in s.get(where, []) if needle in f]
        good = (not hits) if should_pass else bool(hits)
        # each finding has to carry the repair, not just the class
        if good and hits and i == 1:
            good = '"band":[660,700]' in hits[0]
        if good and hits and i == 3:
            # the strip it names has to be the one the ticks are actually drawn
            # in (y652-708), not just any run of ink in the window
            m = re.search(r"across y (\d+)-(\d+)", hits[0])
            good = bool(m) and int(m.group(1)) < 708 and int(m.group(2)) > 652
            # and the self-contradicting "nearest ink (ink 0.0)" line is gone
            good = good and "did not draw at all" in hits[0]
        if good and should_pass:
            # and the repaired slide's census must actually read its marks
            good = not [w for w in s.get("warns", []) if "axis census" in w]
        ok &= good
        print("[%s] %-42s -> %s" % ("HOLD" if good else "BROKE", name,
                                    "clean" if not hits else hits[0][:200]))
    print("axis_band_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
