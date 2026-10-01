#!/usr/bin/env python3
"""ink_census_css_verify.py -- the reconstruction behind the paint census reading
CSS BOX PAINT: border sides, outlines and background colours (2026-09-30,
run No.73).

WHAT IT RECONSTRUCTS. No.73's slides 06 and 08 drew their gold rule under a
label as `border-bottom: 3px solid #FFC72C`. render.py's export-side census
read canvas ops, SVG fill and stroke, and DOM text colour, and nothing else, so
qa.py FAILED both frames with

    promised ink #FFC72C: no brush on this frame ever carried it

while the rule was plainly on screen. The same blindness has a worse face that
nobody had hit yet: a FORBIDDEN ink painted as a CSS border or background was
never seen at all, so the absent half of the law passed it. The repair is in
what the census can see. Nothing in qa.py's ink law is loosened: a promised ink
that reaches zero pixels still FAILs on the pixel half, and a declaration that
draws nothing (border-style none, a 0-width outline, a hidden or fully
transparent box) is still not a brush.

  python3 tests/ink_census_css_verify.py                 # exit 0 = the fix holds
  python3 tests/ink_census_css_verify.py --engine DIR    # run against another
                                                         # copy of render.py

FIXTURES, all 1080x1350, each painting gold ONLY through the CSS named:
  slide-01  PRESENT, a 3 px border-bottom rule under a label (the incident) -> clean
  slide-02  PRESENT, a 3 px div with background-color gold                 -> clean
  slide-03  PRESENT, a 2 px outline round a plate                          -> clean
  slide-04  ABSENT, a 3 px div with background gold (the blind spot)       -> FAIL, forbidden
  slide-05  ABSENT, gold only in declarations that draw nothing: border-style
            none, a 0 px outline, display:none, visibility:hidden, a box inside
            an opacity:0 parent, a 0x0 box                                 -> clean, no gold
  slide-06  PRESENT, gold only in a border with style none                 -> FAIL, missing
"""

import argparse
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
  body {{ background:#0B1620; }}
  canvas {{ position:absolute; inset:0; width:1080px; height:1350px; }}
  .lab {{ position:absolute; left:80px; top:900px; width:700px; font-family:Georgia,serif;
          font-size:32px; color:#C9D3D6; }}
</style></head>
<body data-ink='[{{"hex":"#FFC72C","means":"the one zone that differs","state":"{state}"}}]'>
  <canvas id="c" width="2160" height="2700"></canvas>
  <div class="lab">{body}</div>
<script>
(function () {{
  var cx = document.getElementById("c").getContext("2d");
  cx.scale(2, 2);
  var g = cx.createLinearGradient(0, 0, 0, 1350);
  g.addColorStop(0, "#14232C"); g.addColorStop(1, "#0B1620");
  cx.fillStyle = g; cx.fillRect(0, 0, 1080, 1350);
}})();
</script></body></html>
"""

GOLD = "#FFC72C"
FIXTURES = [
    ("slide-01.html", "present", "clean",
     '<span style="display:block;padding-bottom:9px;border-bottom:3px solid %s">'
     'THE KODIAK INTERIOR</span>' % GOLD),
    ("slide-02.html", "present", "clean",
     'THE KODIAK INTERIOR<div style="height:3px;margin-top:9px;'
     'background-color:%s"></div>' % GOLD),
    ("slide-03.html", "present", "clean",
     '<span style="display:inline-block;padding:6px 10px;outline:2px solid %s">'
     'OCTOBER 8TH</span>' % GOLD),
    ("slide-04.html", "absent", "forbidden",
     'THE KODIAK INTERIOR<div style="height:3px;margin-top:9px;'
     'background:%s"></div>' % GOLD),
    ("slide-05.html", "absent", "nothing",
     'THE KODIAK INTERIOR'
     '<div style="height:3px;margin-top:9px;border-bottom:3px none %s"></div>'
     '<div style="height:20px;outline:0 solid %s"></div>'
     '<div style="display:none;height:20px;background:%s"></div>'
     '<div style="visibility:hidden;height:20px;background:%s"></div>'
     '<div style="opacity:0"><div style="height:20px;background:%s"></div></div>'
     '<div style="width:0;height:0;background:%s"></div>'
     % (GOLD, GOLD, GOLD, GOLD, GOLD, GOLD)),
    ("slide-06.html", "present", "missing",
     '<span style="display:block;padding-bottom:9px;border-bottom:3px none %s">'
     'THE KODIAK INTERIOR</span>' % GOLD),
]

MISSING_MARK = "no brush on this frame ever carried it"
FORBIDDEN_MARK = "forbidden ink #FFC72C"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default=str(ENGINE),
                    help="directory holding render.py (qa.py is always this repo's)")
    args = ap.parse_args()

    tmp = Path(tempfile.mkdtemp(prefix="ink-css-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, state, _want, body in FIXTURES:
        (sdir / name).write_text(SLIDE.format(state=state, body=body))

    subprocess.run([sys.executable, str(Path(args.engine) / "render.py"),
                    "--slides-dir", str(sdir), "--out-dir", str(rdir)],
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
    for name, state, want, _body in FIXTURES:
        s = by_file.get(name, {})
        fails = s.get("fails", [])
        missing = [f for f in fails if MISSING_MARK in f]
        forbidden = [f for f in fails if FORBIDDEN_MARK in f
                     and "is painted on this frame" in f]
        inks = census.get(name, {}).get("inks") or []
        gold = [e for e in inks if isinstance(e, dict)
                and e.get("rgb") == [255, 199, 44]]
        if want == "clean":
            bad = bool(missing) or bool(forbidden) or not gold
        elif want == "forbidden":
            bad = not forbidden or not gold
        elif want == "missing":
            bad = not missing or bool(gold)
        else:  # nothing: no brush may be counted, and the absent law stays quiet
            bad = bool(gold) or bool(forbidden)
        kinds = sorted({e.get("kind") for e in gold})
        line = "%s  gold %-8s want %-9s census gold kinds %s" % (
            name, state, want, kinds or "none")
        note = (missing or forbidden or ["(the ink law said nothing)"])[0]
        print("  %s %s\n       %s" % ("BAD " if bad else "ok  ", line, note[:240]))
        ok = ok and not bad

    print("\npaint census reads CSS box paint: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
