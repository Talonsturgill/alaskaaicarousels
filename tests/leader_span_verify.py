#!/usr/bin/env python3
"""leader_span_verify.py -- the defect reconstruction behind qa.py's
LEADER_SPAN_FAIL ceiling (2026-09-18, run No.62).

WHAT IT RECONSTRUCTS. Round one of No.62 moved slide 02's leader off the gold
"1,000 KM" figure, which was right: a quantity roped to a mark on the ground is
a dimension call, and that frame's own sentence is THE LENGTH IS PUBLISHED. THE
ROUTE IS NOT. Re-originating the leader at the disclosure line made it a 1,020
design px hairline at 37 degrees across the lower right quadrant. Its declared
ends were both perfect, so leader_lands returned ok and leader_labelled returned
ok and machine QA returned PASS at zero fails and zero warns -- and at 432 px
feed width that line was the most prominent non-type mark on the slide and read
as A PLOTTED ROUTE, on the frame built to refuse to draw one. Two pixel critics
and the flow critic scored it 4.0 and it was deleted in round two.

The gate this reconstructs asks the third question about a leader: not where its
ends are, but how far the MARK reaches. Every fixture below declares a leader
that lands exactly on its target and meets its label, so the only variable is
length.

  python3 tests/leader_span_verify.py          # exit 0 = the gate holds

FIXTURES, all four 1080x1350, all four with a correct two-ended declaration:
  slide-01  THE SHIPPED GOOD SPAN. No.62 slide 07's own
            leader, [712,752] to [800,838], 123 px      -> silent, ok
  slide-02  THE DEFECT. No.62 slide 02 round one's
            geometry, 1,020 px at 37 degrees            -> FAIL
  slide-03  NEGATIVE CONTROL at 400 px. Long enough to
            be worth a look and nowhere near a depicted
            feature, so it must WARN and must NOT fail  -> WARN only
  slide-04  NEGATIVE CONTROL at 500 px, 40 px under the
            540 px ceiling. It must reach the WARN and
            stop there; a gate that failed here would be
            tuned to the fixture and not to the defect   -> WARN, never FAIL
"""

import json
import math
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
  body {{ background:#171410; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
  #lab {{ position:absolute; left:{lx}px; top:{ly}px; font-family:Georgia,serif;
         font-size:30px; color:#C9C2B4; letter-spacing:0.02em; }}
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
  <div id="lab">{label}</div>
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  /* a modelled ground, so the frame is not a flat plate and the leader is not
     the only thing on it */
  var g = cx.createLinearGradient(0, 0, 0, 1350);
  g.addColorStop(0, "#2A241B"); g.addColorStop(0.55, "#3B342A");
  g.addColorStop(1, "#1A1712");
  cx.fillStyle = g; cx.fillRect(0, 0, 1080, 1350);
  var s = 20260918 >>> 0;
  function rnd() {{ s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }}
  cx.strokeStyle = "#7A6A4F";
  for (var i = 0; i < 4200; i++) {{
    var px = rnd() * 1080, py = 300 + rnd() * 1050;
    cx.globalAlpha = 0.10 + rnd() * 0.18;
    cx.lineWidth = 0.7 + rnd() * 1.4;
    var a = rnd() * 6.2832, L = 4 + rnd() * 7;
    cx.beginPath();
    cx.moveTo(px - Math.cos(a) * L / 2, py - Math.sin(a) * L / 2);
    cx.lineTo(px + Math.cos(a) * L / 2, py + Math.sin(a) * L / 2);
    cx.stroke();
  }}
  cx.globalAlpha = 1;

  var FROM = {frm}, TO = {to};
  {draw}

  {decl}
}})();
</script></body></html>
"""

LEADER_DRAW = """
  /* the leader itself, and a landing tick on the target so the terminus has
     ink, which is exactly why a pixel test could never judge this */
  cx.strokeStyle = "#C9C2B4"; cx.lineWidth = 1.25; cx.globalAlpha = 0.9;
  cx.beginPath(); cx.moveTo(FROM[0], FROM[1]); cx.lineTo(TO[0], TO[1]); cx.stroke();
  cx.beginPath(); cx.arc(TO[0], TO[1], 4, 0, 6.2832); cx.stroke();
  cx.globalAlpha = 1;
"""

DECL = """window.__akLeaders = [{{ target: {target},
                          at: TO, to: TO, from: FROM,
                          label: {label} }}];"""

LABEL = "THE ROUTE IS NOT PUBLISHED"


def at_angle(frm, length, deg):
    r = math.radians(deg)
    return [round(frm[0] + math.cos(r) * length, 1),
            round(frm[1] + math.sin(r) * length, 1)]


FROM_PT = [150.0, 560.0]

FIXTURES = [
    # name, from, to, declared, want ("ok" | "warn" | "fail" | "silent")
    ("slide-01.html", [712.0, 752.0], [800.0, 838.0], True, "ok"),
    ("slide-02.html", FROM_PT, at_angle(FROM_PT, 1020.0, 37.0), True, "fail"),
    ("slide-03.html", FROM_PT, at_angle(FROM_PT, 400.0, 28.0), True, "warn"),
    ("slide-04.html", FROM_PT, at_angle(FROM_PT, 500.0, 28.0), True, "warn"),
]

FAIL_MARK = "leader is drawn as a feature"
WARN_MARK = "leader reaches across the frame"
OK_MARK = "inside the pointer band"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="leader-span-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, frm, to, declared, _want in FIXTURES:
        decl = (DECL.format(target=json.dumps(name.split(".")[0] + " target"),
                            label=json.dumps(LABEL)) if declared else "")
        # the label sits where the line meets it, inside LEADER_LABEL_PX
        (sdir / name).write_text(SLIDE.format(
            frm=json.dumps(frm), to=json.dumps(to), label=LABEL,
            lx=int(frm[0]) + 8, ly=int(frm[1]) - 34,
            draw=LEADER_DRAW, decl=decl))

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
    for name, frm, to, _declared, want in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if FAIL_MARK in f]
        warns = [w for w in s.get("warns", []) if WARN_MARK in w]
        oks = [i for i in s.get("leaders", []) if OK_MARK in i]
        # the two older leader contracts must stay green on every fixture, or
        # this test is measuring the wrong thing
        other = [f for f in s.get("fails", [])
                 if "leader lands on nothing" in f or "leader carries no label" in f]
        span = math.hypot(to[0] - frm[0], to[1] - frm[1])
        got = ("fail" if fails else "warn" if warns else "ok" if oks else "silent")
        bad = got != want or bool(other)
        line = (fails or warns or oks or ["(span was never measured)"])[0]
        if bad:
            ok = False
            print("  BAD  %s  %.0f px  expected %s, got %s\n       %s"
                  % (name, span, want, got, (other or [line])[0][:300]))
        else:
            print("  ok   %s  %.0f px  %s\n       %s"
                  % (name, span, got, line[:260]))

    print("\nleader span ceiling: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
