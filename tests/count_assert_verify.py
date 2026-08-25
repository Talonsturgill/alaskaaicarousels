#!/usr/bin/env python3
"""count_assert_verify.py -- the defect reconstruction behind the `points`
form of the __akAssert contract (2026-08-25).

WHAT IT RECONSTRUCTS. Run No.40's cover printed the hook 750 and drew 24 rows
of 30 marks, because row 0's centre sat 20px past the canvas edge and never
painted. Every machine gate passed the slide, including the 2026-08-12
assertion gate, because a slide that derives `actual` from its own loop bound
gets 750 from arithmetic that never asks where the marks landed. A pixel critic
counted the rows by hand.

A hook that is a count must survive being counted, so the assertion now
declares the mark centres and the FRAME does the counting.

  python tests/count_assert_verify.py            # exit 0 = the gate holds

FIXTURES, both drawing from one array so only the geometry differs:
  slide-01  25 rows of 30 inside the frame, expect 750      -> holds
  slide-02  row 0 at y = -20, the No.40 cover               -> FAIL, 30 off-frame
  slide-03  the same 750 marks, `actual` hand-written as 750 -> FAIL anyway,
            which is the point: the hand-written number is what lied
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
  /* ONE array: the same 750 centres are drawn and declared */
  var pts = [];
  for (var r = 0; r < 25; r++) for (var c2 = 0; c2 < 30; c2++) {{
    pts.push([54 + c2 * 33, {y0} + r * 44]);
  }}
  cx.fillStyle = "#9FB0A6";
  pts.forEach(function (p) {{ cx.fillRect(p[0] - 5, p[1] - 5, 10, 10); }});
  window.__akAssert = [{{ what: "750 funded devices, one mark each",
                          expect: 750, points: pts, {extra}unit: "marks" }}];
}})();
</script></body></html>
"""

FIXTURES = [
    ("slide-01.html", dict(y0=24, extra=""), False),
    ("slide-02.html", dict(y0=-20, extra=""), True),
    ("slide-03.html", dict(y0=-20, extra="actual: 750, "), True),
]

FAIL_MARK = "self-assertion failed"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="count-verify-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, kw, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(**kw))

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
    for name, _kw, want_fail in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if FAIL_MARK in f]
        infos = s.get("asserts", [])
        warns = [w for w in s.get("warns", []) if "assertion" in w]
        got = bool(fails)
        line = (fails or warns or infos or ["(the assertion was never judged)"])[0]
        bad = got != want_fail or (not want_fail and not infos)
        if got and want_fail and "outside the frame" not in line:
            bad = True          # it must fail for the RIGHT reason
        if bad:
            ok = False
            print("  BAD  %s  expected %s\n       %s"
                  % (name, "a FAIL naming the off-frame marks" if want_fail
                     else "the assertion to hold", line[:260]))
        else:
            print("  ok   %s\n       %s" % (name, line[:260]))

    print("\ncounted-hook assertion: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
