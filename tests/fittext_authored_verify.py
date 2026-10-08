#!/usr/bin/env python3
"""fittext_authored_verify.py -- AK.fitText's opt-in `authored: true`
(2026-10-09, weekly pass; queue item 2026-10-06 at repeat 1).

THE DEFECT. No.79 (slides 05 and 08) and No.81 (every headline): a headline
authored on two lines with <br>, fitted with a maxLines above its authored
count, kept the MAX size and soft-wrapped inside an authored line, and qa.py
reported wrap drift and a ragged line until white-space:nowrap went in by hand.

    python3 tests/fittext_authored_verify.py      # exit 0 = every check holds

In the engine's own browser, with the real aktype.js:
  red      the No.79 shape without the option: 3 rendered lines from 2
           authored, at the max size
  green    with `authored: true`: 2 lines, under the max, the longest line
           inside the box, and the fit registry records authored:true
  content  a box that sizes to its content (absolute, no width) with `width`
           shrinks to that width
  spans    a span-per-line headline fits the same way
  parity   without the option the new aktype.js gives the same sizes and line
           counts as git HEAD's on all three shapes
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="FONTS">
<style>body{margin:0;width:1080px;height:1350px}
h1{position:absolute;left:96px;top:100px;width:620px;font-family:"Bricolage Grotesque",sans-serif;line-height:1;margin:0}
h2{position:absolute;left:96px;top:600px;font-family:"Bricolage Grotesque",sans-serif;line-height:1;margin:0}
h3{position:absolute;left:96px;top:1000px;width:620px;font-family:"Bricolage Grotesque",sans-serif;line-height:1;margin:0}
h3 span{display:block}
h4{position:absolute;left:96px;top:1180px;width:620px;font-family:"Bricolage Grotesque",sans-serif;line-height:1;margin:0}
h4 span{display:block;white-space:normal}</style>
<script src="AKTYPE"></script></head><body>
<h1 id="a">Ash holds it<br>locked in the waste for now</h1>
<h2 id="b">Ash holds it<br>locked in the waste for now</h2>
<h3 id="c"><span>Ash holds it</span><span>locked in the waste for now</span></h3>
<h4 id="d"><span>Ash holds it</span><span>locked in the waste for now</span></h4>
<script>
window.run = async (opt) => {
  await document.fonts.ready;
  const out = {};
  for (const id of ['a', 'b', 'c', 'd']) {
    const el = document.getElementById(id);
    const o = Object.assign({ min: 40, max: 96, maxLines: 3 }, opt ? opt : {});
    if (opt && id === 'b') o.width = 620;
    const r = AK.fitText(el, o);
    out[id] = { size: r.size, lines: r.lines, sw: el.scrollWidth, cw: el.clientWidth,
                right: Math.round(el.getBoundingClientRect().right) };
  }
  out.reg = (window.__akFit || []).map(f => f.authored);
  return out;
};
</script></body></html>"""


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium
    head = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:assets/js/aktype.js"],
                          capture_output=True, text=True, check=True).stdout
    res = {}
    with tempfile.TemporaryDirectory() as td, sync_playwright() as p:
        old = Path(td) / "aktype_head.js"
        old.write_text(head)
        b = launch_chromium(p)
        for key, url, opt in (("plain", (ROOT / "assets/js/aktype.js").as_uri(), None),
                              ("head", old.as_uri(), None),
                              ("authored", (ROOT / "assets/js/aktype.js").as_uri(), {"authored": True})):
            f = Path(td) / ("%s.html" % key)
            f.write_text(PAGE.replace("FONTS", (ROOT / "assets/fonts/fonts.css").as_uri())
                         .replace("AKTYPE", url))
            page = b.new_page(viewport={"width": 1080, "height": 1350})
            page.goto(f.as_uri(), wait_until="load")
            res[key] = page.evaluate("(o) => window.run(o)", opt)
            page.close()
        b.close()
    print(json.dumps(res, indent=1))
    pa, au, hd = res["plain"]["a"], res["authored"]["a"], res["head"]
    checks = [
        (pa["lines"] == 3 and pa["size"] == 95.5 or (pa["lines"] == 3 and pa["size"] >= 90),
         "red: without the option the 2-line authored headline wraps to %d lines at %s px"
         % (pa["lines"], pa["size"])),
        (au["lines"] == 2 and au["size"] < pa["size"] and au["sw"] <= au["cw"] + 1,
         "green: authored:true sets 2 lines at %s px, longest line %d inside %d"
         % (au["size"], au["sw"], au["cw"])),
        (res["authored"]["b"]["lines"] == 2 and res["authored"]["b"]["right"] <= 96 + 620 + 1,
         "content: a content-sized box with width 620 ends at x %d (limit 716)"
         % res["authored"]["b"]["right"]),
        (res["authored"]["c"]["lines"] == 2 and res["authored"]["c"]["size"] == au["size"],
         "spans: a span-per-line headline fits to the same %s px" % res["authored"]["c"]["size"]),
        # Codex, PR #422: a child rule (h4 span {white-space: normal}) must not let a line soft-wrap
        (res["authored"]["d"]["lines"] == 2 and res["authored"]["d"]["size"] == au["size"],
         "child rule: spans styled white-space:normal still hold 2 lines at %s px"
         % res["authored"]["d"]["size"]),
        (res["authored"]["reg"] == [True] * 4 and res["plain"]["reg"] == [False] * 4,
         "registry: __akFit records authored per call"),
        (all(res["plain"][k]["size"] == hd[k]["size"] and res["plain"][k]["lines"] == hd[k]["lines"]
             for k in "abc"),
         "parity: without the option, sizes and line counts equal git HEAD's aktype.js"),
    ]
    bad = 0
    for ok, m in checks:
        print(("PASS " if ok else "FAIL ") + m)
        bad += 0 if ok else 1
    print("%d/%d checks hold" % (len(checks) - bad, len(checks)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
