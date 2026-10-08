#!/usr/bin/env python3
"""span_heading_verify.py -- can copy_sync_check see a headline built from one
<span> per line? (2026-10-09, weekly pass; queue item 2026-10-07, repeat 1)

THE DEFECT. `<h1><span>line one</span><span>line two</span></h1>` is the
authored-break idiom the dossier spec asks for, and the <h1> holds no direct
text, so render.py never recorded it as a text node: only its spans were
recorded, no element carried the headline whole, and copy_sync_check FAILED
every headline of No.80 and of No.81 until each was rebuilt with <br> by hand.

THE FIX. render.py records such a block's joined string in `text_composites`
(not a text node, so no qa.py check reads it) and copy_sync_check takes each
one as a candidate string.

    python3 tests/span_heading_verify.py      # exit 0 = every check holds

It renders a real slide through render.py and checks:
  red     with `text_composites` removed from the report (the pre-fix record),
          the span-per-line headline is reported MISSING
  green   with them, it is found, and so is the <br> headline beside it
  narrow  a block of two <div> children is not a composite, and a shredded
          headline (a word dropped) is still reported missing
  hidden  a display:none child's words never join the composite (Codex, PR #422)
  inert   qa.py's machine_qa.json is identical with and without the field
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
sys.path.insert(0, str(ROOT / "scripts"))
import copy_sync_check as cs  # noqa: E402

SLIDE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#0b1622}
h1{position:absolute;left:96px;top:120px;font-family:"Bricolage Grotesque",sans-serif;font-size:88px;color:#f2f6fd;line-height:1}
h1 span{display:block;white-space:nowrap}
h2{position:absolute;left:96px;top:520px;font-family:"Bricolage Grotesque",sans-serif;font-size:64px;color:#f2f6fd;white-space:nowrap}
.pair{position:absolute;left:96px;top:820px;font-family:"Manrope",sans-serif;font-size:32px;color:#cfd8e6}
.w{position:absolute;right:96px;bottom:96px;font-family:"JetBrains Mono",monospace;font-size:24px;color:#cfd8e6}
h3{position:absolute;left:96px;top:1000px;font-family:"Manrope",sans-serif;font-size:40px;color:#f2f6fd}
h3 span{display:block;white-space:nowrap}</style>
</head><body>
<h1><span>The vessel ranks</span><span>the feed it eats</span></h1>
<h2>A second headline<br>written with a break</h2>
<div class="pair"><div>first block line</div><div>second block line</div></div>
<h3><span>A shown line</span><span style="display:none">never rendered words</span><span>and <em style="display:none">buried </em>its pair</span></h3>
<div class="w">alaskaaihq.com 01 / 01</div>
</body></html>"""

HEADLINE = "The vessel ranks the feed it eats"
BR_HEADLINE = "A second headline written with a break"
HIDDEN_KID = "A shown line and its pair"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))


def main():
    checks = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        sd, rd = td / "slides", td / "render"
        sd.mkdir()
        (sd / "slide-01.html").write_text(SLIDE)
        r = run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd),
                 "--out-dir", str(rd)])
        checks.append((r.returncode == 0, "render.py rendered the slide"))
        rr = json.loads((rd / "render_report.json").read_text())
        comps = rr["slides"][0].get("text_composites") or []
        print("  text_composites: %s" % [c["full"] for c in comps])
        checks.append(([c["full"] for c in comps] == [HEADLINE, HIDDEN_KID],
                       "exactly the two span-per-line headings are recorded as composites"))
        # Codex, PR #422: a hidden child must not lend its words to the composite
        hid = {"slides": [{"n": 1, "headline": "A shown line never rendered words and its pair"}]}
        _, misses, _, _, _ = cs.check(hid, rr)
        checks.append((len(misses) == 1 and not any("never rendered" in c["full"] for c in comps),
                       "hidden: a display:none child's words are not in the composite"))
        checks.append((not any("buried" in c["full"] for c in comps),
                       "hidden deeper: a display:none <em> inside a visible line is not in it either"))

        copy = {"slides": [{"n": 1, "headline": HEADLINE, "kicker": BR_HEADLINE}]}
        pre = json.loads(json.dumps(rr))
        for s in pre["slides"]:
            s.pop("text_composites", None)
        _, misses, _, _, _ = cs.check(copy, pre)
        checks.append(([m[2] for m in misses] == [HEADLINE],
                       "red: without composites the span headline is MISSING (%s)"
                       % [m[2] for m in misses]))
        _, misses, _, _, _ = cs.check(copy, rr)
        checks.append((not misses, "green: with composites both headlines are found (%s)" % misses))
        shred = {"slides": [{"n": 1, "headline": "The vessel ranks the feed"
                                                  " it always eats"}]}
        _, misses, _, _, _ = cs.check(shred, rr)
        checks.append((len(misses) == 1, "narrow: a headline the page never carried is still missing"))

        q1 = run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(rd)])
        m1 = (rd / "machine_qa.json").read_text()
        (rd / "render_report.json").write_text(json.dumps(pre, indent=2))
        q2 = run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(rd)])
        m2 = (rd / "machine_qa.json").read_text()
        checks.append((m1 == m2 and q1.returncode == q2.returncode,
                       "inert: machine_qa.json is identical with and without the field"))
    bad = 0
    for ok, m in checks:
        print(("PASS " if ok else "FAIL ") + m)
        bad += 0 if ok else 1
    print("%d/%d checks hold" % (len(checks) - bad, len(checks)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
