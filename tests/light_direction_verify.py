#!/usr/bin/env python3
"""light_direction_verify.py -- the defect reconstruction behind render.py's
`[light]` resolution line and qa.py's `two light directions` warn (2026-09-05).

WHAT IT RECONSTRUCTS. Run No.51 wanted a grazing fill from the UPPER RIGHT.
It wrote `lights:[{az:205, el:14, w:1.0}]` on all nine slides, which resolves
through akrelief.js's own lightVec() to [-0.41, +0.88, 0.24] -- a light from
the LOWER LEFT -- and hand-shaded every drying ring, every debossment and the
deck's written "lee-side shadow offset down-left" for the upper right. Two
light directions coexisted in nine frames through three build rounds, five
pixel critics and every machine gate, and were found only when somebody read
the library. Nothing anywhere turned the number into a direction a human could
disagree with.

So render.py resolves every declared azimuth and PRINTS it, and reads the
slide's own inline-script comments for a direction that contradicts it. The
comment side is prose, so qa.py warns and never fails, and it abstains on
interior surfaces, which reverse: a pit lit from the upper right has its LIT
wall on the lower left, and No.51's plate 06 says exactly that, correctly.

This is a source-level scan, so the reconstruction needs no browser.

  python tests/light_direction_verify.py          # exit 0 = the scan holds

CASES
  1  az 25  + "lit up-right, lee down-left"      -> agrees, no conflict
  2  az 205 + the same comments        [No.51]   -> 2 conflicts
  3  az 205 + "lit down-left"                    -> agrees, no conflict
  4  az 205 + "the lit inner wall, lower left"   -> abstains (interior)
  5  az 25  + "a trough running to the lower left" -> abstains (not light)
  6  no azimuth + "lee down-left"                -> nothing to compare
  7  two lights, az 25 and az 200, claim up-right -> agrees with one, no conflict

Cases 3 through 7 are the false-positive guard. A scan that fired on them
would make writing a directional comment dangerous, and the comments are how
this house records the intent the azimuth is supposed to serve.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

SLIDE = """<!doctype html>
<html><head><meta charset="utf-8"></head><body>
<canvas id="c" width="2160" height="2700"></canvas>
<script>
(function () {
  var cx = document.getElementById("c").getContext("2d");
  %(lights)s
  %(comment)s
  cx.fillRect(0, 0, 10, 10);
})();
</script>
</body></html>
"""

RAG_25 = 'AK.reliefShade(cx, {low:"#221E18", high:"#4C443A", lights:[{az:25,el:14,w:1.0}]});'
RAG_205 = 'AK.reliefShade(cx, {low:"#221E18", high:"#4C443A", lights:[{az:205,el:14,w:1.0}]});'
RAG_TWO = ('AK.reliefShade(cx, {low:"#221E18", high:"#4C443A", '
           'lights:[{az:25,el:14,w:0.6},{az:200,el:40,w:0.4}]});')

C_RING = ("// the ridge's shading, one gradient laid along the light. "
          "lit up-right, lee down-left.")
C_INVERTED = "// the lit inner wall, lower left, and the shadowed inner wall, upper right"
C_GEOM = "/* A near flat pan cut by one shallow trough running to the lower left. */"
C_DOWNLEFT = "// the key is low and to the down-left, so every crest is lit down-left"

CASES = [
    ("az 25 with the house's own ring comment", RAG_25, C_RING, 0),
    ("az 205 with the same comment (No.51)", RAG_205, C_RING, 2),
    ("az 205 with a comment that agrees", RAG_205, C_DOWNLEFT, 0),
    ("az 205 with an INTERIOR comment", RAG_205, C_INVERTED, 0),
    ("az 25 with a comment about geometry", RAG_25, C_GEOM, 0),
    ("no azimuth at all", "", C_RING, 0),
    ("two lights, a claim agreeing with one", RAG_TWO, C_RING, 0),
]


def main():
    spec = importlib.util.spec_from_file_location("akrender", ENGINE / "render.py")
    rp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rp)

    # the resolver itself, against akrelief.js's lightVec by hand
    ok = True
    for az, want in ((25, "the upper right"), (205, "the lower left"),
                     (315, "the upper left"), (135, "the lower right")):
        got = rp._dir_name(*rp.light_from(az))
        if got != want:
            ok = False
            print("  BAD  az %d resolves to %s, expected %s" % (az, got, want))
        else:
            print("  ok   az %-3d -> lit from %s" % (az, got))

    for name, lights, comment, want in CASES:
        html = SLIDE % {"lights": lights, "comment": comment}
        r = rp.scan_light_direction(html, name)
        got = len(r["conflicts"])
        if got != want:
            ok = False
            print("  BAD  %s: %d conflict(s), expected %d\n       %s"
                  % (name, got, want, r["conflicts"]))
        else:
            print("  ok   %-44s %d conflict(s), %d azimuth(s), %d claim(s)"
                  % (name, got, len(r["lights"]), len(r["claims"])))

    print("\nlight direction scan: %s" % ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
