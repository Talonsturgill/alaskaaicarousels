#!/usr/bin/env python3
"""empty_paint_verify.py -- the defect reconstruction behind the
"a drawing routine that painted nothing" gate (2026-09-01).

WHAT IT RECONSTRUCTS. Run No.47's slide 07 solved nine analytic shadow tips and
drew none of them. The clip test asked whether each cast point was left of a
surveyed cut and broke at s = 0 for every marker, so every wedge was built base
to base, filled at zero length, and the slide's declared focal point was never
in the picture. render.py, qa.py, dossier_check and bespoke_check all passed it,
and a pixel critic caught it a full review round after it shipped into the first
render.

The verdict is on the CALL SITE and not on the individual fill, because an
isolated degenerate fill is ordinary drawing: an edge-on mesh triangle, a bar
whose value is zero. A site whose fills ALL painted nothing is a routine that
ran for nothing. Thresholds live in qa.py (EMPTY_PAINT_MIN, EMPTY_PAINT_RATIO).

  python tests/empty_paint_verify.py             # exit 0 = the gate holds

FIXTURES, all rendered and graded through the real render.py + qa.py:
  slide-01  nine cast wedges at the solved length       -> holds
  slide-02  the same loop with the tip collapsed onto
            the base, which is the s = 0 break          -> FAIL, 9 of 9
  slide-03  240 mesh facets, ONE of them edge on, the
            ak3d.js case that sets the floor            -> silent, 1 of 240
  slide-04  three degenerate fills at a site that also
            painted three real ones, ratio 0.5          -> silent, under the ratio
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

  /* THE CAST FAN. `reach` is the solved shadow length; the defect sets it to 0
     for every marker, which is what a clip that breaks on the first step does. */
  var base = 900, w = 14, reach = {reach};
  cx.fillStyle = "rgba(5,10,18,0.8)";
  for (var i = 0; i < 9; i++) {{
    var x = 120 + i * 96;
    var ex = x - reach * 0.28, ey = base + reach;
    cx.beginPath();
    cx.moveTo(x - w / 2, base); cx.lineTo(x + w / 2, base);
    cx.lineTo(ex + w, ey); cx.lineTo(ex - w, ey);
    cx.closePath(); cx.fill();
  }}

  /* A MESH. One facet is edge on, exactly like ak3d.js's rasteriser. */
  cx.fillStyle = "#5A6E7A";
  for (var t = 0; t < 240; t++) {{
    var fx = 100 + (t % 24) * 36, fy = 200 + Math.floor(t / 24) * 26;
    var flat = (t === 117) ? 0 : 9;
    cx.beginPath();
    cx.moveTo(fx, fy); cx.lineTo(fx + 22, fy + flat); cx.lineTo(fx + 11, fy + flat);
    cx.closePath(); cx.fill();
  }}

  /* A SITE THAT MISSES HALF THE TIME. Six fills, three of them degenerate. */
  cx.fillStyle = "#8A9AA4";
  var hs = [40, 0, 55, 0, 62, 0];
  for (var k = 0; k < hs.length; k++) {{
    cx.beginPath();
    cx.rect(60 + k * 30, 1180, 18, hs[k]);
    cx.fill();
  }}
}})();
</script></body></html>
"""

FIXTURES = [
    ("slide-01.html", dict(reach=180), False),
    ("slide-02.html", dict(reach=0), True),
]

FAIL_MARK = "a drawing routine that painted nothing"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="empty-paint-"))
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
    rep = {s["file"]: s for s in json.loads((rdir / "render_report.json").read_text())["slides"]}

    by_file = {s["file"]: s for s in qa["slides"]}
    ok = True
    for name, _kw, want_fail in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if FAIL_MARK in f]
        got = bool(fails)
        paint = (rep.get(name) or {}).get("paint") or {}
        census = "%s fills, %s sites, %s with an empty one" % (
            paint.get("fills"), paint.get("sites"), len(paint.get("empty") or []))
        if got != want_fail or len(fails) > 1:
            ok = False
            print("  BAD  %s  expected %s\n       %s\n       %s"
                  % (name, "exactly one FAIL" if want_fail else "silence",
                     (fails or ["(no empty-paint fail)"])[0][:240], census))
        else:
            print("  ok   %s  %s\n       %s"
                  % (name, census, (fails or ["(silent)"])[0][:200]))
        # the two negative controls live in every fixture: the edge-on facet and
        # the half-empty bar site must never be named.
        for f in fails:
            if "of 240" in f or "3 of 6" in f:
                ok = False
                print("  BAD  %s named a negative control: %s" % (name, f[:200]))

    print("\nempty-paint gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
