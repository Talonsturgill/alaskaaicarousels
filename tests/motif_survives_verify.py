#!/usr/bin/env python3
"""motif_survives_verify.py -- the defect reconstruction behind qa.py's
`declared motif does not reach the slide` gate (2026-08-25).

WHAT IT RECONSTRUCTS. Run No.40 lost three declared motifs on three slides and
every machine gate stayed green on all three:

  slide 07  the continuity cell was drawn on the canvas and then covered by the
            `.lane` plate (`background:#0A121C`), which paints above canvas
  slide 03  the same cell, drawn and then covered by the `.guard` plate
  slide 06  the cell was drawn and then painted out by the channel's own void
            fill on the very next drawing operation

The code was right and the picture was empty each time; twice a repair note
recorded the element as visible when nothing was on the slide at all.

This builds all three as fixtures, plus the two cases the gate must NOT fire
on, and asserts the verdicts. It is hermetic: it writes its own slides into a
temp dir, renders them and reads qa.py's JSON. No repo state is touched.

  python tests/motif_survives_verify.py            # exit 0 = the gate holds

FIXTURES
  slide-01  motif drawn, nothing over it                    -> no motif fail
  slide-02  motif under an opaque DOM plate  [No.40 S07/S03] -> FAIL, buried
  slide-03  motif painted out by the next canvas op [No.40 S06] -> FAIL, no ink
  slide-04  motif under a 45% scrim (legitimate atmosphere)  -> no motif fail

Slides 01 and 04 are the false-positive guard: a gate that fails them would
make declaring a motif more dangerous than staying silent, which is how a
contract stops being used.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

MOTIF = (812, 214, 96, 96)          # the declared rect, design px
GROUND = "#0A121C"

# A ground with real texture (so the frame is not uniform), then the motif: a
# stencil of ticks in the studio's own grey-green. Written as plain canvas 2d
# with no AK helpers and no @@ASSETS@@ so the fixture depends on nothing.
SLIDE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1080px; height:1350px; overflow:hidden; }}
  body {{ background:{ground}; position:relative; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
  .plate {{ position:absolute; left:780px; top:196px; width:160px; height:132px;
            background:#0A121C; }}
  .scrim {{ position:absolute; left:780px; top:196px; width:160px; height:132px;
            background:rgba(10,18,28,0.45); }}
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
  {plate}
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  cx.fillStyle = "{ground}"; cx.fillRect(0, 0, 1080, 1350);
  /* ground texture: a seeded hatch, so the frame is never uniform */
  var s = 1234567;
  function rnd() {{ s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; }}
  cx.strokeStyle = "#16202C"; cx.lineWidth = 1;
  for (var i = 0; i < 400; i++) {{
    var x = rnd() * 1080, y = rnd() * 1350;
    cx.beginPath(); cx.moveTo(x, y); cx.lineTo(x + 18 * rnd(), y + 6 * rnd()); cx.stroke();
  }}
  /* THE MOTIF: a cell stencil at the declared rect */
  var MX = {mx}, MY = {my};
  {draw}
  {after}
  window.__akMotifs = [{{ what: "cell 0016, the continuity stencil",
                          rect: [{mx}, {my}, {mw}, {mh}] }}];
}})();
</script></body></html>
"""

DRAW = """
  cx.fillStyle = "#9FB0A6";
  for (var r = 0; r < 4; r++) for (var c2 = 0; c2 < 4; c2++) {
    cx.fillRect(MX + 6 + c2 * 22, MY + 6 + r * 22, 14, 9);
  }
  cx.strokeStyle = "#D7E2DA"; cx.lineWidth = 2;
  cx.strokeRect(MX + 2, MY + 2, 92, 92);
"""

PAINT_OUT = """
  /* the void fill on the very next drawing operation -- No.40 slide 06 */
  cx.fillStyle = "#0E1622"; cx.fillRect(MX - 8, MY - 8, 112, 112);
"""

FIXTURES = [
    ("slide-01.html", dict(plate="", draw=DRAW, after=""), False),
    ("slide-02.html", dict(plate='<div class="plate"></div>', draw=DRAW, after=""), True),
    ("slide-03.html", dict(plate="", draw=DRAW, after=PAINT_OUT), True),
    ("slide-04.html", dict(plate='<div class="scrim"></div>', draw=DRAW, after=""), False),
]

MOTIF_FAIL = "declared motif does not reach the slide"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="motif-verify-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, kw, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(
            ground=GROUND, mx=MOTIF[0], my=MOTIF[1], mw=MOTIF[2], mh=MOTIF[3], **kw))

    r = subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sdir), "--out-dir", str(rdir)],
                       capture_output=True, text=True)
    if not (rdir / "render_report.json").exists():
        print(r.stdout[-2000:] + r.stderr[-2000:])
        print("FAIL: render produced no report")
        return 1
    q = subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(rdir)], capture_output=True, text=True)
    if not (rdir / "machine_qa.json").exists():
        print(q.stdout[-2000:] + q.stderr[-2000:])
        print("FAIL: qa produced no machine_qa.json")
        return 1
    qa = json.loads((rdir / "machine_qa.json").read_text())

    by_file = {s["file"]: s for s in qa["slides"]}
    ok = True
    for name, _kw, want_fail in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if MOTIF_FAIL in f]
        warns = [w for w in s.get("warns", []) if w.startswith("motif:")]
        infos = s.get("motifs", [])
        got_fail = bool(fails)
        verdict = "FAIL" if got_fail else ("warn" if warns else "pass")
        line = (fails or warns or infos or ["(the motif was never judged)"])[0]
        if got_fail != want_fail or (not want_fail and not (warns or infos)):
            ok = False
            print("  BAD  %s  expected %s, got %s\n       %s"
                  % (name, "a motif FAIL" if want_fail else "no motif fail",
                     verdict, line[:220]))
        else:
            print("  ok   %s  %s\n       %s" % (name, verdict, line[:220]))

    print("\nmotif survival gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
