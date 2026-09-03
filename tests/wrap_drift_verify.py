#!/usr/bin/env python3
"""wrap_drift_verify.py -- the defect reconstruction behind the wrap-drift
warn (2026-09-02).

WHAT IT RECONSTRUCTS. Run No.48's slide 07 carried a spec plate of four
stamped fields, the fourth deliberately never struck, which is how the deck
DRAWS "the ordinance carries no fiscal analysis" [C06, C31] rather than
asserting it. The four canvas field markers were counted off the plate
RECTANGLE at a fixed pitch, `py + 42 + f * 39`. The stamp text then wrapped to
five lines inside its 330 px box, every marker slid up one row, and the proud
unstruck tab came to rest on `AMENDABLE . NO`. The slide shipped a picture
arguing the inverse of its own claims. render.py, qa.py and every gate in
gate_status passed it, because nothing anywhere compared a block's AUTHORED
line count against its RENDERED one. A pixel critic found it by reading.

The in-run fix was two parts, `white-space:nowrap` so the count cannot drift
plus marker y values read off getBoundingClientRect at render time. This is the
instrument that names the drift in round one instead.

  python tests/wrap_drift_verify.py            # exit 0 = the check holds

FIXTURES, all rendered and graded through the real render.py + qa.py:
  slide-01  4 fields, <br>-separated, in a 330 px box, one field long enough
            to wrap                                  -> WARN, 4 authored / 5 rendered
  slide-02  the same four fields with white-space:nowrap (the shipped fix)
                                                     -> silent
  slide-03  the same four fields as preserved newlines under white-space:pre
            (the shape slide 07 actually ships)      -> silent
  slide-04  the same four fields as newlines under white-space:pre-wrap, which
            DOES wrap                                -> WARN
  slide-05  ordinary prose with no authored breaks at all, wrapping to many
            lines                                    -> silent (nothing declared,
            nothing to drift from)
  slide-06  a <br> block containing a <span>, which the Range walk cannot
            count                                    -> silent (skipped, not
            measured wrong)
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

SLIDE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1080px; height:1350px; overflow:hidden; }}
  body {{ background:#0A121C; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
  .mn {{ position:absolute; font-family:monospace; font-size:24px;
         color:#C6D0DA; line-height:1.62; }}
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
  <div class="mn" id="plate" style="left:656px;top:196px;width:330px;{ws}">{body}</div>
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  cx.fillStyle = "#0A121C"; cx.fillRect(0, 0, 1080, 1350);
  cx.fillStyle = "#3A4658"; cx.fillRect(120, 300, 420, 700);
  cx.fillStyle = "#9FB0A6";
  for (var i = 0; i < 40; i++) cx.fillRect(140 + (i % 8) * 50, 340 + ((i / 8) | 0) * 90, 34, 34);
  // the defect's mechanism, kept here so the fixture reads like the slide:
  // four field markers counted off the PLATE RECTANGLE at a fixed pitch.
  var py = 196;
  for (var f = 0; f < 4; f++) {{ cx.fillRect(1000, py + 42 + f * 39, 14, 14); }}
}})();
</script></body></html>
"""

FIELDS_BR = ("EFFECTIVE . 2027 CYCLE<br>TERM . TWO YEARS AND A FULL "
             "BOROUGH CYCLE<br>AMENDABLE . NO<br>COST . ")
FIELDS_NL = ("EFFECTIVE . 2027 CYCLE\nTERM . TWO YEARS AND A FULL "
             "BOROUGH CYCLE\nAMENDABLE . NO\nCOST . ")

FIXTURES = [
    ("slide-01.html", FIELDS_BR, "", True),
    ("slide-02.html", FIELDS_BR, "white-space:nowrap;", False),
    ("slide-03.html", FIELDS_NL, "white-space:pre;", False),
    ("slide-04.html", FIELDS_NL, "white-space:pre-wrap;", True),
    ("slide-05.html",
     "The ordinance does not include a fiscal analysis or estimate of "
     "implementation costs, and the overall cost would depend on turnout, "
     "staffing and the number of races on the ballot.", "", False),
    ("slide-06.html",
     "EFFECTIVE . <span>2027 CYCLE</span><br>TERM . TWO YEARS AND A FULL "
     "BOROUGH CYCLE<br>AMENDABLE . NO", "", False),
]

WARN_MARK = "wrap drift"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="wrap-drift-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, body, ws, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(body=body, ws=ws))

    subprocess.run([sys.executable, str(ENGINE / "render.py"), "--slides-dir",
                    str(sdir), "--out-dir", str(rdir)], capture_output=True, text=True)
    if not (rdir / "render_report.json").exists():
        print("FAIL: render produced no report")
        return 1
    q = subprocess.run([sys.executable, str(ENGINE / "qa.py"), "--render-dir",
                        str(rdir)], capture_output=True, text=True)
    if not (rdir / "machine_qa.json").exists():
        print(q.stdout[-2000:] + q.stderr[-2000:])
        print("FAIL: qa produced no machine_qa.json")
        return 1
    qa = json.loads((rdir / "machine_qa.json").read_text())

    by_file = {s["file"]: s for s in qa["slides"]}
    ok = True
    for name, _body, _ws, want_warn in FIXTURES:
        s = by_file.get(name, {})
        warns = [w for w in s.get("warns", []) if WARN_MARK in w]
        got = bool(warns)
        line = (warns or ["(no wrap-drift warn)"])[0]
        if got != want_warn:
            ok = False
            print("  BAD  %s  expected %s\n       %s"
                  % (name, "a WARN" if want_warn else "silence", line[:240]))
        else:
            print("  ok   %s  %s" % (name, line[:170]))

    print("\nwrap-drift check: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
