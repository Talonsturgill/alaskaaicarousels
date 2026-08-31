#!/usr/bin/env python3
"""mark_paints_verify.py -- the defect reconstruction behind the PIXEL half of
the `points` form of the __akAssert contract (2026-08-31).

WHAT IT RECONSTRUCTS. Run No.46's slide 03 printed the claim that the FCC asked
EIGHT consecutive questions about AI, declared eight proud leaves, drew eight,
and SHIPPED SIX. The type reserve is applied as an evenodd clip, so the two
leftmost leaves were erased at draw time. The 2026-08-25 count contract
reported 8 of 8 for the whole run, because it counts CENTRES INSIDE THE FRAME
and a clip removes ink without moving a coordinate. Every machine gate stayed
green and a human found it by cropping the render and counting by eye.

So the declared centres are now probed on the composited png, and a mark whose
local ink falls under 30 percent of its own cohort's median is a mark that
never painted.

  python tests/mark_paints_verify.py             # exit 0 = the gate holds

FIXTURES, all four drawing the same 60 centres from one array, so only what
happens to the ink afterwards differs:
  slide-01  nothing in the way                          -> holds
  slide-02  an evenodd reserve clip over 12 of them,
            which is run No.46's own mechanism          -> FAIL, 12 missing
  slide-03  an opaque DOM plate over the same 12,
            a different erasure, same verdict           -> FAIL, 12 missing
  slide-04  NEGATIVE CONTROL: a 65 percent scrim over
            half the field. The marks are dimmed and
            plainly visible, and a check that fires
            here is a check runs would learn to
            work around                                 -> holds
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

# 60 marks, 6 rows of 10 at a 96px pitch, centred in the frame.
SLIDE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1080px; height:1350px; overflow:hidden; }}
  body {{ background:#0A121C; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
  {plate}
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  var g = cx.createLinearGradient(0, 0, 900, 1350);
  g.addColorStop(0, "#0A121C"); g.addColorStop(1, "#132635");
  cx.fillStyle = g; cx.fillRect(0, 0, 1080, 1350);

  /* ONE array: the same 60 centres are drawn and declared */
  var pts = [];
  for (var r = 0; r < 6; r++) for (var c2 = 0; c2 < 10; c2++) {{
    pts.push([108 + c2 * 96, 420 + r * 96]);
  }}

  cx.save();
  {clip}
  cx.fillStyle = "#E4DCC8";
  pts.forEach(function (p) {{
    cx.beginPath(); cx.arc(p[0], p[1], 14, 0, 6.2832); cx.fill();
  }});
  cx.restore();

  window.__akAssert = [{{ what: "60 declared marks, one each",
                          expect: 60, points: pts, unit: "marks" }}];
}})();
</script></body></html>
"""

# The RES() idiom out of the studio's own build: the whole frame minus the
# reserve boxes, filled evenodd, is the clip. Art under a reserve is never
# drawn. This box stands on the last two columns of the top six rows.
CLIP = """
  cx.beginPath();
  cx.rect(0, 0, 1080, 1350);
  cx.moveTo(840, 380); cx.lineTo(840, 990);
  cx.lineTo(1080, 990); cx.lineTo(1080, 380); cx.closePath();
  cx.clip("evenodd");
"""

PLATE = ('<div style="position:absolute;left:840px;top:380px;width:240px;'
         'height:610px;background:#0A121C"></div>')

SCRIM = ('<div style="position:absolute;left:0;top:380px;width:560px;'
         'height:610px;background:rgba(10,18,28,0.65)"></div>')

FIXTURES = [
    ("slide-01.html", dict(clip="", plate=""), False),
    ("slide-02.html", dict(clip=CLIP, plate=""), True),
    ("slide-03.html", dict(clip="", plate=PLATE), True),
    ("slide-04.html", dict(clip="", plate=SCRIM), False),
]

FAIL_MARK = "declared marks missing from the frame"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mark-paints-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, kw, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(**kw))

    subprocess.run([sys.executable, str(ENGINE / "render.py"), "--slides-dir",
                    str(sdir), "--out-dir", str(rdir)],
                   capture_output=True, text=True)
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
        infos = [i for i in s.get("asserts", []) if "mark centres probed" in i]
        warns = [w for w in s.get("warns", []) if w.startswith("declared marks")]
        got = bool(fails)
        line = (fails or warns or infos or ["(the marks were never probed)"])[0]
        bad = got != want_fail
        if want_fail and got and "12 of them carry no mark" not in line:
            bad = True          # it must fail for the RIGHT reason, and for 12
        if not want_fail and (warns or not infos):
            bad = True          # silence here means the probe abstained
        if bad:
            ok = False
            print("  BAD  %s  expected %s\n       %s"
                  % (name, "a FAIL naming 12 missing marks" if want_fail
                     else "all 60 present", line[:300]))
        else:
            print("  ok   %s\n       %s" % (name, line[:300]))

    print("\ndeclared-mark visibility: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
