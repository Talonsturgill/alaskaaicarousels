#!/usr/bin/env python3
"""assert_vacuous_verify.py -- the defect reconstruction behind the
"an assertion that cannot fail" gate (2026-09-01).

WHAT IT RECONSTRUCTS. Run No.47's slide 08 printed in type that two stamped
tags carry the same seven struck rows, built the two tags SEPARATELY in 3D,
shipped nine rows on one and eight on the other at different insets, and
declared

    window.__akAssert = [{ what: "both tags carry the same seven struck rows",
                           expect: 7, actual: 7, tol: 0, unit: "rows" }];

which holds for any picture whatsoever. The same run's slide 05 put
`+sidePx.toFixed(2)` on both sides of its scale assertion. Both read green in
render_report and in machine_qa, and the deck's own artifacts then cited them
as proof; a pixel critic found the tags by reading the source beside the render.

The 2026-08-12 assertion contract's whole value is in the authoring, "you can't
write `actual` without deriving it from the thing that actually drew". This is
the half of it that is now enforced.

  python tests/assert_vacuous_verify.py           # exit 0 = the gate holds

FIXTURES, all five rendered and graded through the real render.py + qa.py:
  slide-01  expect 840 against 20 * FT_PX          -> holds, a real measurement
  slide-02  expect 7 against actual 7              -> FAIL, same expression
  slide-03  the same variable on both sides        -> FAIL, same expression
  slide-04  a derived expect against a typed 654   -> FAIL, literal `actual`
  slide-05  the `points` count form, plus a
            hand-written `actual`                  -> silent here; the count
            contract owns that case and reports it
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
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  cx.fillStyle = "#0A121C"; cx.fillRect(0, 0, 1080, 1350);
  var FT_PX = 42, sidePx = 318.5, SPAN = 750 - 96;
  var pts = [];
  for (var i = 0; i < 12; i++) pts.push([120 + i * 70, 900]);
  cx.fillStyle = "#9FB0A6";
  pts.forEach(function (p) {{ cx.fillRect(p[0] - 6, p[1] - 6, 12, 12); }});
  cx.fillRect(120, 400, 20 * FT_PX, 6);
  window.__akAssert = [{decl}];
}})();
</script></body></html>
"""

FIXTURES = [
    ("slide-01.html",
     '{ what: "the 20 ft lock, printed as an 840 px rule", '
     'expect: 840, actual: 20 * FT_PX, tol: 2, unit: "px" }', False),
    ("slide-02.html",
     '{ what: "both tags carry the same seven struck rows", '
     'expect: 7, actual: 7, tol: 0, unit: "rows" }', True),
    ("slide-03.html",
     '{ what: "the square drawn at the map\'s own scale", '
     'expect: +sidePx.toFixed(2), actual: +sidePx.toFixed(2), tol: 0.5, unit: "px" }', True),
    ("slide-04.html",
     '{ what: "the bracket reaches the first station to the last", '
     'expect: SPAN, actual: 654, tol: 1, unit: "px" }', True),
    ("slide-05.html",
     '{ what: "twelve parcel pins, one per parcel on offer", '
     'expect: 12, points: pts, actual: 12, unit: "marks" }', False),
]

FAIL_MARK = "an assertion that cannot fail"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="assert-vacuous-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, decl, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(decl=decl))

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
    for name, _decl, want_fail in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if FAIL_MARK in f]
        got = bool(fails)
        line = (fails or ["(no vacuous-assertion fail)"])[0]
        if got != want_fail:
            ok = False
            print("  BAD  %s  expected %s\n       %s"
                  % (name, "a FAIL" if want_fail else "silence", line[:240]))
        else:
            print("  ok   %s  %s" % (name, line[:200]))

    print("\nvacuous-assertion gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
