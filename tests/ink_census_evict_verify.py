#!/usr/bin/env python3
"""ink_census_evict_verify.py -- the reconstruction behind PINNING a declared
law ink in the paint census (2026-09-18, run No.62).

WHAT IT RECONSTRUCTS. No.62's first build graded aerial perspective with a
per-row colour lerp, which minted a fresh colour literal on every row of the
hachure field. The census keeps 160 entries. The lerp filled it, #FFC72C was
evicted, and qa.py FAILED two frames with

    promised ink #FFC72C: no brush on this frame ever carried it
    (160 colours in the paint census, none within dE 2 of it ...)

on frames that plainly had gold on them. The verdict was false and the message
named the wrong cause, so the diagnosis cost a full render cycle before anyone
suspected the instrument rather than the art.

A gate that can report a FALSE FAIL is worse than a missing gate, because the
run then spends its budget repairing something that was never broken. The fix
is not a looser ink law -- nothing here is loosened. It is that the census
reserves a slot for every ink the frame's own `data-ink` law names, at the
source of the paint and again at export, so the one colour the gate exists to
look for is the one colour it can never lose. And when the census IS saturated,
the failure message now says so first.

  python3 tests/ink_census_evict_verify.py      # exit 0 = the fix holds

FIXTURES, all 1080x1350, all declaring the same one-line ink law and all
painting the same gold mark at the same size and alpha:
  slide-01  BASELINE. A handful of colours, then the gold.
            Nothing is near the cap                     -> gold found, no fail
  slide-02  THE DEFECT. 300 distinct per-row colour
            literals ahead of the gold, which is exactly
            the aerial lerp that evicted it             -> gold found, no fail
  slide-03  THE DEFECT WITH THE LAW INVERTED. The same
            300 literals, and the law says the gold is
            ABSENT while a brush paints it. Pinning must
            not become a way to smuggle a forbidden ink
            past the census                             -> FAIL, forbidden ink
  slide-04  THE OTHER HALF OF THE CAP. 170 distinct SVG
            fills at three ops each, which never touch
            the canvas hook and are cut on the EXPORT
            side by OP COUNT, where a two-op gold mark
            loses however early it was painted. Its
            census comes back at 161 entries, which is
            the 160 slice plus the pinned gold put back  -> gold found, no fail
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
  body {{ background:#171410; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
  #cap {{ position:absolute; left:80px; top:1180px; font-family:Georgia,serif;
         font-size:32px; color:#C9C2B4; }}
</style></head>
<body data-ink='[{{"hex":"#FFC72C","means":"what the record carries","state":"{state}"}}]'>
  <canvas id="c" width="2160" height="2700"></canvas>
  <div id="cap">the record is small</div>
  <svg id="sv" width="1080" height="1350" style="position:absolute;inset:0"></svg>
<script>
/* {svgn} distinct SVG fills, three elements each. These never touch the canvas
   hook, so they arrive on the EXPORT side of the census, where the list is cut
   to 160 by OP COUNT -- and three ops each outranks a gold mark's two however
   early the gold was painted. This is the half of the fix the canvas flood
   cannot reach. */
(function () {{
  var sv = document.getElementById("sv");
  for (var i = 0; i < {svgn}; i++) {{
    var col = "rgb(" + (20 + i % 160) + "," + (24 + (i * 13) % 150) + "," + (18 + (i * 29) % 140) + ")";
    for (var j = 0; j < 3; j++) {{
      var el = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      el.setAttribute("x", (i % 40) * 27); el.setAttribute("y", 40 + ((i / 40) | 0) * 9 + j);
      el.setAttribute("width", 26); el.setAttribute("height", 1);
      el.setAttribute("fill", col);
      sv.appendChild(el);
    }}
  }}
}})();
</script>
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  var g = cx.createLinearGradient(0, 0, 0, 1350);
  g.addColorStop(0, "#2A241B"); g.addColorStop(1, "#1A1712");
  cx.fillStyle = g; cx.fillRect(0, 0, 1080, 1350);

  /* THE EVICTION. A per-row lerp between two greys, one fresh colour literal
     per row. This is the aerial-perspective band that flooded No.62's census;
     {rows} rows is {rows} distinct inks ahead of the gold. */
  for (var r = 0; r < {rows}; r++) {{
    var R = 60 + (r % 150), G = 50 + ((r * 11) % 130), B = 30 + ((r * 7) % 90);
    cx.fillStyle = "rgb(" + R + "," + G + "," + B + ")";
    /* three ops per row, so every flood colour outranks the gold's two on the
       export's op-count sort as well as beating it to the cap. Both pins have
       to hold or the gold is gone. */
    cx.fillRect(0, 300 + r * 2, 1080, 2);
    cx.fillRect(0, 300 + r * 2, 540, 1);
    cx.fillRect(540, 300 + r * 2, 540, 1);
  }}

  /* THE GOLD. One sealed mark, last, exactly as the deck's law describes it:
     small, opaque, and the only saturated thing on the frame. */
  cx.fillStyle = "#FFC72C";
  cx.beginPath(); cx.arc(880, 980, 14, 0, 6.2832); cx.fill();
  cx.fillRect(760, 1060, 120, 9);
}})();
</script></body></html>
"""

FIXTURES = [
    # name, rows of canvas lerp, distinct SVG fills, declared state, want
    ("slide-01.html", 6, 0, "present", "clean"),
    ("slide-02.html", 300, 0, "present", "clean"),
    ("slide-03.html", 300, 0, "absent", "forbidden"),
    ("slide-04.html", 6, 170, "present", "clean"),
]

MISSING_MARK = "no brush on this frame ever carried it"
FORBIDDEN_MARK = "forbidden ink #FFC72C"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="ink-evict-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, rows, svgn, state, _want in FIXTURES:
        (sdir / name).write_text(SLIDE.format(rows=rows, svgn=svgn, state=state))

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
    rep = json.loads((rdir / "render_report.json").read_text())
    census = {s["file"]: s for s in rep.get("slides", [])}

    by_file = {s["file"]: s for s in qa["slides"]}
    ok = True
    for name, rows, svgn, state, want in FIXTURES:
        s = by_file.get(name, {})
        missing = [f for f in s.get("fails", []) if MISSING_MARK in f]
        forbidden = [f for f in s.get("fails", []) if FORBIDDEN_MARK in f
                     and "is painted on this frame" in f]
        rec = census.get(name, {})
        inks = rec.get("inks") or []
        gold = [e for e in inks if isinstance(e, dict)
                and e.get("rgb") == [255, 199, 44]]
        capped = bool(rec.get("ink_cap"))
        if want == "clean":
            bad = bool(missing) or not gold
        else:
            bad = not forbidden or not gold
        note = (missing or forbidden or ["(the ink law said nothing)"])[0]
        state_line = ("%d lerp rows + %d svg inks, census %d entries%s, "
                      "gold in census: %s"
                      % (rows, svgn, len(inks), " (CAPPED)" if capped else "",
                         "yes" if gold else "NO"))
        if bad:
            ok = False
            print("  BAD  %s  %s\n       %s" % (name, state_line, note[:320]))
        else:
            print("  ok   %s  %s\n       %s"
                  % (name, state_line,
                     (forbidden or ["the promised ink survived the census"])[0][:200]))

    print("\ndeclared law ink pinned in the census: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
