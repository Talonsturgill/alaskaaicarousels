#!/usr/bin/env python3
"""canvas_over_text_verify.py -- the defect reconstruction behind the
"text under canvas ink" gate (2026-10-16, weekly machine pass).

WHAT IT RECONSTRUCTS. Run No.88's AKDOCKET.fixtures appended the ALASKA.AI
wordmark, the NN / 09 counter and the alaskaaihq.com line to <body> with
position:absolute and NO z-index, after a z-index:1 full-bleed art canvas. A
positioned box at z-index auto paints before a z-index 1 sibling, so all three
painted UNDER the art on all nine frames. They were in the DOM, so render.py,
qa.py and copy_sync_check passed, and five pixel critics found them missing.
render.py's plate probe skips <canvas> deliberately (canvas ink is sparse), so
nothing machine-side could see it.

  python3 tests/canvas_over_text_verify.py      # exit 0 = the gate holds

FIXTURES, all rendered and graded through the real render.py + qa.py:
  slide-01  the No.88 shape: fixtures with no z-index after a
            z-index 1 opaque art canvas                       -> 3 FAILs (wordmark,
                                                                 counter, site), the
                                                                 z-indexed headline silent
  slide-02  the same frame with the fixtures at z-index 9,
            which is the in-run fix in assets/js/akdocket.js   -> silent
  slide-03  a near-transparent grain canvas (alpha 24) stacked
            above every line of type                          -> silent
  slide-04  an opaque canvas above the type with
            mix-blend-mode screen                             -> silent
  slide-05  an opaque canvas chip over the left third of a
            reading line                                      -> one WARN, no FAIL
  slide-06  art over 60 percent of a decorative ghost numeral -> one WARN, no FAIL
  slide-07  an opaque band with pointer-events none over the
            headline (hit testing can't see it)              -> one FAIL
  slide-08  two sibling bands at opacity .7 over the headline
            (they composite to 91 percent)                    -> one FAIL
  slide-09  a line inked with an inline !important colour
            under an opaque band                              -> one FAIL
  slide-10  difference-blended text over a canvas UNDER it    -> silent
The probe is pixel truth (render.py canvas_cover_probe), so these hold without
modelling any CSS.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

HEAD = """<!doctype html>
<html><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1350px; overflow:hidden; }
  body { background:#0A121C; font-family:'JetBrains Mono', monospace; }
  h1 { position:absolute; left:80px; top:520px; width:900px; font-size:72px;
       line-height:1.1; color:#F4F8FF; font-weight:600; }
</style></head><body>
"""

ART = """<canvas id="art" width="2160" height="2700" style="position:absolute;inset:0;
  width:1080px;height:1350px;z-index:1;{style}"></canvas>
<script>
(function () {{
  var cx = document.getElementById("art").getContext("2d");
  cx.scale(2, 2);
  cx.fillStyle = "rgba(40,58,74,{alpha})"; cx.fillRect({rect});
}})();
</script>
"""

FIXTURES_JS = """<script>
(function () {{
  var css = "position:absolute;{z}font-family:'JetBrains Mono';font-weight:500;letter-spacing:0.08em;";
  var w = document.createElement("div"); w.textContent = "ALASKA.AI"; w.setAttribute("data-decorative", "");
  w.style.cssText = css + "left:80px;top:84px;font-size:24px;color:#B9BDC2;"; document.body.appendChild(w);
  var c = document.createElement("div"); c.textContent = "04 / 09"; c.className = "counter";
  c.style.cssText = css + "right:80px;top:82px;font-size:24px;color:#B9BDC2;"; document.body.appendChild(c);
  var f = document.createElement("div"); f.textContent = "alaskaaihq.com"; f.setAttribute("data-decorative", "");
  f.style.cssText = css + "left:200px;top:1240px;font-size:24px;color:#8A949E;"; document.body.appendChild(f);
}})();
</script>
"""

HEADLINE = '<h1 style="z-index:2">The hearing room keeps its own calendar</h1>\n'
TAIL = "</body></html>\n"


def slide(art, fixtures=None, extra=""):
    return HEAD + art + HEADLINE + extra + (FIXTURES_JS.format(z=fixtures) if fixtures is not None
                                            else "") + TAIL


GHOST = ('<div data-decorative style="position:absolute;z-index:2;left:600px;top:900px;font-size:260px;'
         'line-height:1;color:#1C2A38;font-weight:700">88</div>\n'
         '<canvas id="hill" width="2160" height="2700" style="position:absolute;inset:0;'
         'width:1080px;height:1350px;z-index:3"></canvas>\n<script>\n(function () {\n'
         '  var cx = document.getElementById("hill").getContext("2d"); cx.scale(2, 2);\n'
         '  cx.fillStyle = "#24384A"; cx.fillRect(560, 1010, 520, 340);\n})();\n</script>\n')

CHIP = ('<canvas id="chip" width="640" height="200" style="position:absolute;left:60px;top:500px;'
        'width:320px;height:100px;z-index:5"></canvas>\n<script>\n(function () {\n'
        '  var cx = document.getElementById("chip").getContext("2d");\n'
        '  cx.fillStyle = "#C9A227"; cx.fillRect(0, 0, 640, 200);\n})();\n</script>\n')

FULL = "0, 0, 1080, 1350"

# Codex on PR #438: a canvas with pointer-events none is invisible to hit testing but still paints;
# two sibling canvases at opacity .7 composite to 91 percent over the headline
def _band(cid, style):
    return ('<canvas id="%s" width="2160" height="400" style="position:absolute;left:0;top:480px;'
            'width:1080px;height:200px;%s"></canvas>\n<script>(function(){var c=document.getElementById('
            '"%s").getContext("2d");c.fillStyle="#0A121C";c.fillRect(0,0,2160,400);})();</script>\n' % (cid, style, cid))
NOHIT = _band("nohit", "z-index:6;pointer-events:none;")
STACK = _band("s1", "z-index:6;opacity:.7;") + _band("s2", "z-index:7;opacity:.7;")
# an inline !important colour must not hide the line from the probe; blended text over a canvas UNDER it is not covered
LINE = ('<div style="position:absolute;z-index:4;left:80px;top:820px;font-size:48px;font-weight:700;'
        'color:#E8E2D4 !important;%s">%s</div>\n')
INLINE = (LINE % ("", "Inline important ink line") +
          '<canvas id="lid" width="2160" height="240" style="position:absolute;left:0;top:800px;width:1080px;'
          'height:120px;z-index:5"></canvas>\n<script>(function(){var c=document.getElementById("lid")'
          '.getContext("2d");c.fillStyle="#0A121C";c.fillRect(0,0,2160,240);})();</script>\n')
BLEND = ('<canvas id="under" width="2160" height="240" style="position:absolute;left:0;top:800px;width:1080px;'
         'height:120px;z-index:3"></canvas>\n<script>(function(){var c=document.getElementById("under")'
         '.getContext("2d");c.fillStyle="#808080";c.fillRect(0,0,2160,240);})();</script>\n' +
         LINE % ("mix-blend-mode:difference;", "Blended line over a lower canvas"))
CASES = [
    # name, html, expected FAIL count, expected WARN count, labels that must be named
    ("slide-01.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures=""),
     3, 0, ["ALASKA.AI", "04 / 09", "alaskaaihq.com"]),
    ("slide-02.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;"),
     0, 0, []),
    ("slide-03.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;",
                            extra='<canvas id="grain" width="2160" height="2700" style="position:'
                                  'absolute;inset:0;width:1080px;height:1350px;z-index:20">'
                                  '</canvas>\n<script>(function(){var g=document.getElementById('
                                  '"grain").getContext("2d");g.fillStyle="rgba(255,255,255,0.094)";'
                                  'g.fillRect(0,0,2160,2700);})();</script>\n'),
     0, 0, []),
    ("slide-04.html", slide(ART.format(style="mix-blend-mode:screen;z-index:30;", alpha=1, rect=FULL),
                            fixtures="z-index:9;"),
     0, 0, []),
    ("slide-05.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;",
                            extra=CHIP),
     0, 1, ["The hearing room"]),
    ("slide-06.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;",
                            extra=GHOST),
     0, 1, ["88"]),
    ("slide-07.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;", extra=NOHIT),
     1, 0, ["The hearing room"]),
    ("slide-08.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;", extra=STACK),
     1, 0, ["The hearing room"]),
    ("slide-09.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;", extra=INLINE),
     1, 0, ["Inline important"]),
    ("slide-10.html", slide(ART.format(style="", alpha=1, rect=FULL), fixtures="z-index:9;", extra=BLEND),
     0, 0, []),
]
MARK = "text under canvas ink"


def main():
    tmp = Path(tempfile.mkdtemp(prefix="canvas-over-text-"))
    sdir, rdir = tmp / "slides", tmp / "render"
    sdir.mkdir(parents=True)
    for name, html, *_ in CASES:
        (sdir / name).write_text(html)
    r = subprocess.run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sdir),
                        "--out-dir", str(rdir)], capture_output=True, text=True)
    if not (rdir / "render_report.json").exists():
        print(r.stdout[-2000:] + r.stderr[-2000:])
        print("FAIL: render produced no report")
        return 1
    q = subprocess.run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(rdir)],
                       capture_output=True, text=True)
    if not (rdir / "machine_qa.json").exists():
        print(q.stdout[-2000:] + q.stderr[-2000:])
        print("FAIL: qa produced no machine_qa.json")
        return 1
    by = {s["file"]: s for s in json.loads((rdir / "machine_qa.json").read_text())["slides"]}
    ok = True
    for name, _html, nf, nw, labels in CASES:
        s = by.get(name, {})
        fails = [f for f in s.get("fails", []) if MARK in f]
        warns = [w for w in s.get("warns", []) if MARK in w]
        named = all(any(("'%s" % lb) in m for m in fails + warns) for lb in labels)
        good = len(fails) == nf and len(warns) == nw and named
        ok &= good
        print("  %s  %s  %d FAIL, %d WARN (want %d, %d)" % ("ok  " if good else "BAD ", name,
                                                         len(fails), len(warns), nf, nw))
        for m in (fails + warns)[:4]:
            print("         " + m[:230])
    print("\ncanvas-over-text gate: %s   (fixtures in %s)" % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
