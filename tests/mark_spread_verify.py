#!/usr/bin/env python3
"""mark_spread_verify.py -- the defect reconstruction behind `dispersed: true`
on the `points` form of the __akAssert contract (2026-09-04).

WHAT IT RECONSTRUCTS. Run No.50's slide 08 lit 31 of 72 grid cells to stand for
the 31 sections of two townships that a 19,950 acre conveyance covers. Where
those acres sit inside the townships has not been published, so the label
seventy pixels under the grid reads EXTENT ONLY. NO BOUNDARY IS DRAWN. The
build shuffled the 72 cells with a seeded Fisher Yates and took the first 31,
which put them edge to edge in one township, and the frame drew a solid parcel
with holes in it. The count contract reported 31 of 31 and the pixel probe
reported all 31 painted, and both were right: they ask HOW MANY and WHETHER
THEY PAINTED, and this defect is about WHERE. Every machine gate was green and
five pixel critics scored the slide 2.5.

So a count whose meaning is extent declares `dispersed: true`, and qa.py
measures the largest touching mass of the declared centres.

  python tests/mark_spread_verify.py            # exit 0 = the gate holds

FIXTURES, all four on the same 6 x 12 grid of 62px cells, all four lighting
exactly 31 of the 72, so only WHERE the 31 sit differs:
  slide-01  the shipped repair: cells accepted in seeded
            random order only while every touching run
            stays under a cap                             -> holds
  slide-02  THE DEFECT: the first 31 cells of the grid,
            one solid township, which is what a shuffle
            that clusters produces                        -> FAIL, one mass
  slide-03  NEGATIVE CONTROL: a plain seeded shuffle,
            take the first 31. This is the build the run
            rejected by eye, and at 43 percent density it
            still leaves runs of a dozen. A gate that
            fired here would fire on chance, so it must
            NOT fail                                      -> holds
  slide-04  NEGATIVE CONTROL: the same 31 cells as the
            defect, with the flag left off. A slide that
            never claimed dispersion is never judged      -> silent
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
  body {{ background:#0B1119; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  cx.fillStyle = "#0B1119"; cx.fillRect(0, 0, 1080, 1350);

  var GX = 300, GY = 300, CELL = 62, COLS = 6, ROWS = 12, N = COLS * ROWS;

  /* one seeded stream, so every fixture is deterministic */
  var s = 20260904 >>> 0;
  function rnd() {{ s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }}
  function shuffled() {{
    var a = [], i, j, t;
    for (i = 0; i < N; i++) a.push(i);
    for (i = N - 1; i > 0; i--) {{ j = (rnd() * (i + 1)) | 0; t = a[i]; a[i] = a[j]; a[j] = t; }}
    return a;
  }}
  function nbrs(c) {{
    var col = c % COLS, row = (c / COLS) | 0, o = [];
    if (col > 0) o.push(c - 1);
    if (col < COLS - 1) o.push(c + 1);
    if (row > 0) o.push(c - COLS);
    if (row < ROWS - 1) o.push(c + COLS);
    return o;
  }}
  function runOf(set, c) {{           /* the touching run c would join */
    var seen = {{}}, st = [c], n = 0, k, i, v;
    seen[c] = 1;
    while (st.length) {{
      k = st.pop(); n++;
      v = nbrs(k);
      for (i = 0; i < v.length; i++) if (set[v[i]] && !seen[v[i]]) {{ seen[v[i]] = 1; st.push(v[i]); }}
    }}
    return n;
  }}
  function capped(cap) {{            /* offer in random order, accept under a cap */
    var order = shuffled(), set = {{}}, lit = [], i, c;
    for (i = 0; i < order.length && lit.length < 31; i++) {{
      c = order[i]; set[c] = 1;
      if (runOf(set, c) > cap) {{ set[c] = 0; continue; }}
      lit.push(c);
    }}
    return lit;
  }}

  var LIT = {lit};
  var pts = LIT.map(function (c) {{
    return [GX + (c % COLS) * CELL + CELL / 2, GY + ((c / COLS) | 0) * CELL + CELL / 2];
  }});

  cx.strokeStyle = "#26313F"; cx.lineWidth = 1;
  for (var a = 0; a <= COLS; a++) {{
    cx.beginPath(); cx.moveTo(GX + a * CELL, GY); cx.lineTo(GX + a * CELL, GY + ROWS * CELL); cx.stroke();
  }}
  for (var b = 0; b <= ROWS; b++) {{
    cx.beginPath(); cx.moveTo(GX, GY + b * CELL); cx.lineTo(GX + COLS * CELL, GY + b * CELL); cx.stroke();
  }}
  cx.fillStyle = "#E4DCC8";
  pts.forEach(function (p) {{
    cx.beginPath(); cx.arc(p[0], p[1], 16, 0, 6.2832); cx.fill();
  }});

  window.__akAssert = [{{ what: "31 of 72 sections, extent only",
                          expect: 31, points: pts, {flag}unit: "marks" }}];
}})();
</script></body></html>
"""

FIXTURES = [
    # name, the expression that produces the 31 lit cells, flag, wants a FAIL
    ("slide-01.html", "capped(3)", "dispersed: true, ", False),
    ("slide-02.html", "(function () { var a = [], i; for (i = 0; i < 31; i++) a.push(i); return a; })()",
     "dispersed: true, ", True),
    ("slide-03.html", "shuffled().slice(0, 31)", "dispersed: true, ", False),
    ("slide-04.html", "(function () { var a = [], i; for (i = 0; i < 31; i++) a.push(i); return a; })()",
     "", None),
]

FAIL_MARK = "declared scatter drew a shape"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mark-spread-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, lit, flag, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(lit=lit, flag=flag))

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
    for name, _lit, _flag, want_fail in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if FAIL_MARK in f]
        warns = [w for w in s.get("warns", []) if w.startswith("declared scatter")]
        infos = [i for i in s.get("asserts", []) if "largest touching mass" in i]
        line = (fails or warns or infos or ["(dispersion was never measured)"])[0]
        if want_fail is None:                      # the flag was never declared
            bad = bool(fails or warns or infos)
        else:
            bad = bool(fails) != want_fail or bool(warns) or not (fails or infos)
        # every fixture lights exactly 31, so the count assertion must hold too
        if [f for f in s.get("fails", []) if "self-assertion failed" in f]:
            bad = True
        if bad:
            ok = False
            print("  BAD  %s  expected %s\n       %s"
                  % (name, {True: "a FAIL naming one mass", False: "no fail",
                            None: "silence"}[want_fail], line[:300]))
        else:
            print("  ok   %s\n       %s" % (name, line[:300]))

    print("\ndeclared-scatter dispersion: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
