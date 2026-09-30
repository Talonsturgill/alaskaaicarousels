#!/usr/bin/env python3
"""Does copy_sync_check read the punctuation that RENDERED? (2026-09-29)

Hermetic: synthetic render reports whose truth is known by construction, run
through the real script as a subprocess, the way gate_status.py runs it.

  1. CLEAN. Straight marks only, one of them in Space Grotesk: exit 0, and the
     census names the slanted face so a critic can be handed the fact.
  2. DOM. A curly apostrophe and an em dash typed into a decorative label that
     copy.json never holds: exit 1, both named. The pre-2026-09-29 script
     passed exactly this, because it compares letters and digits only.
  3. CANVAS. An en dash drawn with fillText: exit 1.
  4. NO DOUBLE COUNT. A mark in a span is counted once, in the span's face,
     although the parent element's `full` string carries it too.
  5. ROW LINE. On PASS the first stdout line is the verdict, which is the line
     gate_status.py prints in its copy_sync row.

    python3 tests/copy_sync_punct_verify.py

Exit 0 HOLDS, exit 1 BROKEN.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "copy_sync_check.py"


def node(text, family, texts=None, full=None, decorative=False):
    return {"text": text[:80], "texts": texts if texts is not None else [text],
            "full": full if full is not None else text, "family": family,
            "decorative": decorative, "line_text": [text]}


def run(nodes, canvas=None):
    rr = {"slides": [{"file": "slide-01.html", "text_nodes": nodes + [
        node("alaskaaihq.com", "JetBrains Mono", decorative=True)],
        "canvas_text": canvas or []}]}
    copy = {"slides": [{"n": 1, "headline": "Alaska's share"}]}
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "rr.json").write_text(json.dumps(rr))
        (Path(d) / "copy.json").write_text(json.dumps(copy))
        p = subprocess.run([sys.executable, str(SCRIPT), "--copy", str(Path(d) / "copy.json"),
                            "--render-report", str(Path(d) / "rr.json")],
                           capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout


def main():
    ok = True

    def hold(name, cond, out=""):
        nonlocal ok
        print("%s  %s" % ("HOLDS " if cond else "BROKEN", name))
        if not cond:
            ok = False
            print(out)

    base = [node("Alaska's share", "Space Grotesk"),
            node('"a quoted line"', "Fraunces")]
    rc, out = run(base)
    hold("1 clean deck passes", rc == 0, out)
    hold("1 census flags Space Grotesk as slanted",
         "U+0027 x1 in space grotesk (drawn slanted)" in out
         and "U+0022 x2 in fraunces" in out and "fraunces (drawn" not in out, out)
    hold("5 first line is the PASS verdict", out.splitlines()[0].startswith("copy_sync_check: PASS"), out)

    rc, out = run(base + [node("60°47’N — 161°45'W", "JetBrains Mono",
                                decorative=True)])
    hold("2 DOM curly apostrophe and em dash fail", rc == 1
         and "curly apostrophe U+2019" in out and "em dash U+2014" in out, out)

    rc, out = run(base, canvas=[{"text": "FY2017–2026", "font": "600 30px 'Space Grotesk'"}])
    hold("3 canvas en dash fails", rc == 1 and "en dash U+2013" in out, out)

    parent = node("The notice asks 'why' now", "Fraunces",
                  texts=["The notice asks ", " now"], full="The notice asks 'why' now")
    span = node("'why'", "Space Grotesk")
    rc, out = run([node("Alaska's share", "Fraunces"), parent, span])
    hold("4 a span's marks count once, in the span's face",
         rc == 0 and "U+0027 x2 in space grotesk (drawn slanted)" in out
         and "U+0027 x1 in fraunces" in out, out)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
