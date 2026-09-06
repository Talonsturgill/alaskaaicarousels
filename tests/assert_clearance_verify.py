#!/usr/bin/env python3
"""assert_clearance_verify.py -- the defect reconstruction behind the `at`
clearance contract on __akAssert (2026-09-05).

WHAT IT RECONSTRUCTS. Run No.51's slide 09 carried the deck's ONE filled gold
seal, the ninth state of a motif tracked through eight plates. Its assertion
derived the seal's radius from the deck constant and compared it against the
radius the drawing used, correctly, and passed. The seal was drawn at a
coordinate that fell inside an opaque mono knockout, so it never reached the
page, and a pixel critic found it on the third build round. An assertion about
how BIG a mark is says nothing about whether anyone can see it.

The repair is one optional key. `at:[x,y]` (with `r`, default 12 design px)
turns the assertion's subject into the same evidence record __akMotifs
produces, so the elementsFromPoint census and the canvas-versus-page ink ratio
judge it, on the motif gate's own thresholds.

Hermetic: writes its own slides into a temp dir, renders them, reads qa.py's
JSON. No repo state is touched.

  python tests/assert_clearance_verify.py         # exit 0 = the gate holds

FIXTURES
  slide-01  the seal on clean rag, `at` declared            -> no clearance fail
  slide-02  the same seal inside an opaque knockout [No.51] -> FAIL, buried
  slide-03  the same seal under a 45% scrim                 -> no clearance fail
  slide-04  the seal drawn, then painted out by the next canvas op -> FAIL
  slide-05  the same buried seal with NO `at`               -> no fail at all

Slides 01, 03 and 05 are the false-positive guard. 03 in particular: this
house sets marks under atmosphere on purpose, and a gate that failed a scrim
would make declaring `at` more dangerous than staying silent. 05 is the proof
that the contract stays opt-in.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

SEAL_R = 14
GROUND = "#221E18"

SLIDE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1080px; height:1350px; overflow:hidden; }}
  body {{ background:{ground}; position:relative; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
  .knock {{ position:absolute; left:480px; top:600px; width:300px; height:200px;
            background:#14120E; }}
  .scrim {{ position:absolute; left:480px; top:600px; width:300px; height:200px;
            background:rgba(20,18,14,0.45); }}
</style></head><body>
  <canvas id="c" width="2160" height="2700"></canvas>
  {plate}
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  cx.fillStyle = "{ground}"; cx.fillRect(0, 0, 1080, 1350);
  /* the rag: a seeded tooth, so no region of the frame is uniform */
  var s = 51513;
  function rnd() {{ s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; }}
  for (var i = 0; i < 30000; i++) {{
    var x = rnd() * 1080, y = rnd() * 1350;
    cx.fillStyle = rnd() > 0.5 ? "rgba(18,16,12,0.22)" : "rgba(92,86,74,0.20)";
    cx.fillRect(x, y, 2, 2);
  }}
  /* THE SEAL: the deck's one filled gold mark, at the deck constant's radius */
  var SEAL = [{sx}, {sy}], GR = {r};
  cx.beginPath(); cx.arc(SEAL[0], SEAL[1], GR, 0, 6.2832);
  cx.fillStyle = "#C79A2E"; cx.fill();
  cx.lineWidth = 2; cx.strokeStyle = "#E8C46A"; cx.stroke();
  {after}
  window.__akAssert = [{{ what: "the inked gauge, radius from the deck constant",
                          expect: {r}, actual: GR, tol: 0.01, unit: "px"{clear} }}];
}})();
</script></body></html>
"""

PAINT_OUT = """
  /* a later canvas operation floods the seal's own region */
  cx.fillStyle = "#221E18"; cx.fillRect(SEAL[0] - 40, SEAL[1] - 40, 80, 80);
"""

CLEAR = ", at: SEAL, r: GR"
ON_RAG = (600, 1080)          # clean paper, well clear of the plate
IN_PLATE = (600, 690)         # inside the .knock / .scrim box

FIXTURES = [
    ("slide-01.html", dict(plate="", sx=ON_RAG[0], sy=ON_RAG[1],
                           after="", clear=CLEAR), False),
    ("slide-02.html", dict(plate='<div class="knock"></div>', sx=IN_PLATE[0],
                           sy=IN_PLATE[1], after="", clear=CLEAR), True),
    ("slide-03.html", dict(plate='<div class="scrim"></div>', sx=IN_PLATE[0],
                           sy=IN_PLATE[1], after="", clear=CLEAR), False),
    ("slide-04.html", dict(plate="", sx=ON_RAG[0], sy=ON_RAG[1],
                           after=PAINT_OUT, clear=CLEAR), True),
    ("slide-05.html", dict(plate='<div class="knock"></div>', sx=IN_PLATE[0],
                           sy=IN_PLATE[1], after="", clear=""), False),
]

CLEAR_FAIL = "the mark an assertion declares does not reach the slide"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="clearance-verify-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, kw, _ in FIXTURES:
        (sdir / name).write_text(SLIDE.format(ground=GROUND, r=SEAL_R, **kw))

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
    for name, kw, want_fail in FIXTURES:
        s = by_file.get(name, {})
        fails = [f for f in s.get("fails", []) if CLEAR_FAIL in f]
        warns = [w for w in s.get("warns", []) if w.startswith("assert clearance:")]
        infos = [i for i in s.get("motifs", []) if "inked gauge" in i]
        got_fail = bool(fails)
        judged = bool(fails or warns or infos)
        # slide 05 declares no `at`, so the machine must say NOTHING about the
        # mark: the contract is opt-in and a silent default would change that.
        want_judged = bool(kw["clear"])
        line = (fails or warns or infos or ["(nothing was said about the mark)"])[0]
        if got_fail != want_fail or judged != want_judged:
            ok = False
            print("  BAD  %s  expected %s, got %s\n       %s"
                  % (name, "a clearance FAIL" if want_fail else
                     ("a clear verdict" if want_judged else "silence"),
                     "FAIL" if got_fail else ("a clear verdict" if judged else "silence"),
                     line[:220]))
        else:
            print("  ok   %s  %s\n       %s"
                  % (name, "FAIL" if got_fail else ("clear" if judged else "silent"),
                     line[:220]))

    print("\nassert clearance gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
