#!/usr/bin/env python3
"""line_text_verify.py -- the reconstruction behind render.py's per-line text
walk and qa.py's 2026-09-13 ragged-display-line warning.

THE DEFECT. Run No.58 opened with all nine display headlines breaking against
their own sense ("HAS VOTED ON THE / IMPLEMENTATION", "About / 639,237 square
kilometres") and spent two full critic rounds, on every frame, putting <br>s in
by eye. DESIGN_DOCTRINE has forbidden a hanging preposition since the beginning
and nothing measured it, because render.py recorded WHERE each line sat and
never which words ended it.

THE WALK. getClientRects() on a Range from a text node's start to offset i
returns one rect per line it touches, and that count is non-decreasing in i, so
the end of a line is found by BISECTION in O(lines * log characters) rather
than by extending the range one character at a time. The count first exceeds a
line once the range swallows the first inked character of the NEXT line, so the
break sits at lo - 1; without that correction the walk reports "...a large-l"
and "oad customer ...", a line break nobody wrote.

THE FIXTURES, three headlines in one slide:
  1. an authored <br> block          -> line_text is exactly the authored lines
  2. a soft wrap ending on "ON THE"  -> WARNS, naming the hanging article
  3. a soft wrap ending on a noun    -> no ragged warning

Usage: python tests/line_text_verify.py   (exit 0 = all hold)
Renders with the engine's own render.py and judges with its own qa.py. No
network. Writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENGINE = REPO / ".claude" / "skills" / "carousel-engine"

SLIDE = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#081426; color:#E7EFF8; position:relative;
         font-family:"Archivo", sans-serif; }
  .hd { position:absolute; left:80px; width:780px; font-size:46px;
        line-height:1.1; font-weight:600; }
</style></head><body>
  <div class="hd" id="authored" style="top:120px">THE SENATE STRUCK IT.<br>THE HOUSE NEVER<br>PICKED UP THE DIE.</div>
  <div class="hd" id="ragged" style="top:520px">THE STATE LEGISLATURE HAS VOTED ON THE IMPLEMENTATION</div>
  <div class="hd" id="clean" style="top:900px">REPORTED.<br>NOT SCHEDULED.</div>
</body></html>
"""

AUTHORED = ["THE SENATE STRUCK IT.", "THE HOUSE NEVER", "PICKED UP THE DIE."]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="linetext_"))
    sl = tmp / "slides"
    sl.mkdir()
    (sl / "slide-01.html").write_text(SLIDE)
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                        "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        rep = json.loads((tmp / "render" / "render_report.json").read_text())
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    nodes = {n.get("full", "")[:24]: n for n in rep["slides"][0]["text_nodes"]}
    warns = [w for w in qa["slides"][0]["warns"] if "ragged display line" in w]
    ok = True

    def check(label, good, detail=""):
        nonlocal ok
        ok &= bool(good)
        print("[%s] %-46s %s" % ("HOLD" if good else "BROKE", label, detail))

    node = nodes.get("THE SENATE STRUCK IT. TH")
    got = (node or {}).get("line_text")
    check("an authored <br> block reports its three lines", got == AUTHORED,
          str(got))

    soft = nodes.get("THE STATE LEGISLATURE HA")
    lt = (soft or {}).get("line_text") or []
    check("a soft-wrapped block reports whole words",
          bool(lt) and all(w.strip() == w and "  " not in w for w in lt)
          and " ".join(lt) == (soft or {}).get("full"), str(lt))

    check("the badly broken headline is named, once",
          len(warns) == 1 and "STATE LEGISLATURE" in warns[0],
          "; ".join(w[:90] for w in warns) or "no ragged warn")
    check("the clean two-line headline is not reported",
          not any("REPORTED." in w for w in warns))

    print("line_text_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
