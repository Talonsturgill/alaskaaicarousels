#!/usr/bin/env python3
"""technique_stack_verify.py -- the defect reconstruction behind dossier_check's
field-7 technique-stack gate (2026-09-20, run No.64).

WHAT IT RECONSTRUCTS. Eight of the nine dossiers in run No.64 named `akthree`
-- for the slab, the steps, the port and the ring -- and NO FRAME IN THE DECK
LOADED three.js. Every one of those objects was an `aksection` primitive or
canvas lathing. The claim survived planning, the build, two full pixel rounds
and a flow read; three pixel critics then found it INDEPENDENTLY in round three
by opening the slides and reading the `<script>` list themselves. That is a
machine's job, and both sides of the comparison were already on disk.

  python tests/technique_stack_verify.py         # exit 0 = the gate holds

FIXTURES, all four written against the SAME slide, which loads aksection.js,
akengrave.js and akpost.js and nothing else:
  01  names `aksection` `akengrave` `akpost`            -> holds
  02  names `akthree` for the slab, run No.64's own
      claim                                             -> FAIL, akthree.js
  03  names no file but writes `AKT.snapshot`, which is
      how the claim survived the round-three sweep: the
      token was renamed and the handle was left behind  -> FAIL, akthree.js
  04  NEGATIVE CONTROL: writes `AK.grainTile`. noise.js,
      aktype.js, aklabel.js, akrelief.js and
      akhachure.js all publish into AK, so it is not
      attributable and the gate must not guess          -> holds
  05  NEGATIVE CONTROL: field 7 is prose with no
      backticked library at all                         -> holds
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SLIDE = """<!doctype html>
<html><head><meta charset="utf-8"></head>
<body data-ink='{}'>
<canvas id="c" width="2160" height="2700"></canvas>
<script src="@@ASSETS@@/js/aksection.js"></script>
<script src="@@ASSETS@@/js/akengrave.js"></script>
<script src="@@ASSETS@@/js/akpost.js"></script>
<script>/* the slab is an aksection primitive */</script>
</body></html>
"""

F4A = ("**4a. Lower-third treatment.** The modelled earth slab fills the bottom "
       "31 percent of the frame, its engraved tone carrying the story quantity, "
       "with a lit lip whose thickness varies with how the surface faces the key "
       "and a shadowed trough beneath it. Cast shadows land on it, the contour "
       "hatching is a real relief field rather than a texture, and the graded fog "
       "beyond the cut gives the band depth. Nothing flat, nothing floating.\n")

DOSSIER = """## SLIDE {n:02d} -- THE SECTION

### B. COMPOSITION
{f4a}
### C. ART DIRECTION
**7. Technique stack.** {stack}
**8. Data in art.** The section span drives the scale bar `[design]`.
"""

FIXTURES = [
    (1, "`aksection` `S.slab` for the slab, `akengrave` tone, `akpost` grade.",
     False, ""),
    (2, "`akthree` GPU PBR for the slab, `akengrave` tone, `akpost` grade.",
     True, "akthree.js"),
    (3, "`aksection` for the slab, `AKT.snapshot` read back onto the 2D canvas, "
        "`akpost` grade.", True, "akthree.js"),
    (4, "`aksection` for the slab, `AK.grainTile` over the sky, `akpost` grade.",
     False, ""),
    (5, "The slab is lathed by hand on the 2D canvas, no library involved.",
     False, ""),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="technique-stack-"))
    (tmp / "slides").mkdir()
    parts = []
    for n, stack, _want, _needle in FIXTURES:
        (tmp / "slides" / ("slide-%02d.html" % n)).write_text(SLIDE)
        parts.append(DOSSIER.format(n=n, f4a=F4A, stack=stack))
    (tmp / "storyboard.md").write_text("# DECK\n\n" + "\n".join(parts))

    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "dossier_check.py"),
                        "--run-dir", str(tmp), "--json"],
                       capture_output=True, text=True)
    import json
    try:
        rep = json.loads(p.stdout)
    except ValueError:
        print("  BAD  dossier_check produced no report\n%s\n%s"
              % (p.stdout[-800:], p.stderr[-800:]))
        return 1

    by_slide = {s["slide"]: s for s in rep["slides"]}
    ok = True
    for n, _stack, want_fail, needle in FIXTURES:
        fails = [f for f in by_slide.get(n, {}).get("fails", []) if "field 7" in f]
        got = bool(fails)
        line = (fails or by_slide.get(n, {}).get("fails") or ["(clean)"])[0]
        bad = got != want_fail
        if got and want_fail and needle not in line:
            bad = True                     # it must fail for the RIGHT reason
        if not want_fail and by_slide.get(n, {}).get("fails"):
            bad = True                     # no unrelated finding either
        if bad:
            ok = False
            print("  BAD  slide %02d  expected %s\n       %s"
                  % (n, ("a FAIL naming %s" % needle) if want_fail
                     else "no finding", line[:240]))
        else:
            print("  ok   slide %02d  %s\n       %s"
                  % (n, "FAIL" if got else "clean", line[:240]))

    print("\ndeclared-technique-stack gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
