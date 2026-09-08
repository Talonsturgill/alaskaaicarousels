#!/usr/bin/env python3
"""figure_backing_verify.py -- the reconstruction behind dossier_check's
2026-09-07 figure cross-check.

Run No.53 planned and printed "102 SIGNATURES" plus a 102-mark struck field off
a scout paragraph that the first claims pass never turned into a claim, and
printed "1971" twice in mono off a fact-checker NOTE reading "consistent with
1971". claims_check, aggregate_check and plan_drift all passed both, because
each checks the claims that exist rather than the figures a dossier quotes. The
first cost a late verification pass during the pixel rounds; the second capped a
scoring round and was probably factually wrong.

Six fixtures, each a two-file run directory (storyboard.md + claims.json):

  1. the 102 defect as it was planned            -> FAILS, "NO claim ... at all"
  2. the same dossier once C54 exists            -> passes
  3. the 1971 defect, verified only in a note    -> FAILS, names C35, "NOTES of"
  4. the same line printing what C35 verifies    -> passes
  5. a drawing constant marked [design]          -> passes
  6. rail furniture and a progress counter       -> passes
  7. the statute cite 43 U.S.C. 1606(i)          -> passes (an address, not a figure)
  8. a bare "1606 SHAREHOLDERS" beside it        -> FAILS (the cite backs nothing)

Usage: python tests/figure_backing_verify.py    (exit 0 = all six hold)
Stdlib only, no network, writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECK = REPO / "scripts" / "dossier_check.py"

LOWER = ("**4a. LOWER-THIRD TREATMENT.** The lit sphere carries the terminator "
         "ramp down through the band, the branch arc descends across it toward "
         "the lower left with a graded foreground plane under it, and the "
         "annotation furniture runs down into the corner so the bottom third "
         "holds modeled tone rather than a plate. Every mark has a lit windward "
         "lip and a dark lee edge at az 142.")


def dossier(copy_lines):
    return ("# STORYBOARD\n\n## SLIDE 08 - THE COUNTERWEIGHT\n\n"
            "**1. BEAT.** The same mechanism buys other things.\n\n"
            "**2. COPY, FINAL.**\n" + "\n".join(copy_lines) + "\n\n"
            "**3. READER TAKEAWAY.** The record is not comfortable.\n\n"
            + LOWER + "\n")


def claims(*entries):
    return {"run_date": "2026-09-07", "claims": list(entries)}


C54 = {"id": "C54", "claim": "A Bering Straits shareholder petition had "
       "garnered 102 signatures from shareholders and descendants.",
       "value": "102 signatures", "verbatim": "had garnered 102 signatures",
       "notes": "Verified from the Nome Nugget."}
C38 = {"id": "C38", "claim": "The Koniag Services task order obligates "
       "$17,456,917.40.", "value": "$17,456,917.40",
       "verbatim": "OBLIGATED $17,456,917.40", "notes": "PIID 70CDCR26FR0000034."}
C31 = {"id": "C31", "claim": "Federal law requires regional Alaska Native "
       "corporations to share 70 percent of their timber and subsurface "
       "revenue with the other eleven.", "value": "70 percent",
       "verbatim": "shall be divided annually by the recipient among all "
                   "twelve Regional Corporations",
       "notes": "43 U.S.C. 1606(i)(1)(A), statute text read today."}
C35_NOTE = {"id": "C35", "claim": "Koniag has grown from 3,400 shareholders at "
            "incorporation to more than 4,700 today.",
            "value": "4,700 shareholders",
            "verbatim": "growing its shareholders, dividends and finances",
            "notes": "Background. Incorporation dated nearly 55 years ago, "
                     "consistent with 1971 and the Settlement Act."}

CASES = [
    ("102 printed with no claim anywhere", False, "NO claim",
     dossier(["- Mono block, 26px: `OBLIGATED   $17,456,917.40` [C38]",
              "- Body, 34px: `Bering Straits shareholders petitioned. 102 signatures.`"]),
     claims(C38)),
    ("102 printed once C54 exists", True, None,
     dossier(["- Mono block, 26px: `OBLIGATED   $17,456,917.40` [C38]",
              "- Body, 34px: `Bering Straits shareholders petitioned. 102 signatures.` [C54]"]),
     claims(C38, C54)),
    ("1971 reasoned to in a note", False, "NOTES of C35",
     dossier(["- Mono block, 26px: `SHAREHOLDERS   3,400 AT INCORPORATION IN 1971` [C35]"]),
     claims(C35_NOTE)),
    ("the same line printing what C35 verifies", True, None,
     dossier(["- Mono block, 26px: `SHAREHOLDERS   3,400 AT INCORPORATION` [C35]"]),
     claims(C35_NOTE)),
    ("a drawing constant marked [design]", True, None,
     dossier(["- Key, mono 24px: `ONE DOT IS 100 SHAREHOLDERS` [design]",
              "- Mono block, 26px: `OBLIGATED   $17,456,917.40` [C38]"]),
     claims(C38)),
    ("rail furniture and a progress counter", True, None,
     dossier(["- Rail, mono 24px: `41.0N 82.1W . t 0.90 . 3,026 MI . 08 / 09`",
              "- Mono counter, bottom left: `08 / 09`",
              "- Mono block, 26px: `OBLIGATED   $17,456,917.40` [C38]"]),
     claims(C38)),
    # THE FALSE POSITIVE THE SHOWRUNNER HIT ON THE FIRST USE OF THIS GATE.
    # A title number and a section number are an address in a book. C31's own
    # subject IS the citation, read at uscode.house.gov, and the gate was
    # reading 43 and 1606 as unverified quantities.
    ("a statute cite beside a figure the claim verifies", True, None,
     dossier(["- Record block, mono 26px: `43 U.S.C. 1606(i)   70% OF TIMBER "
              "AND SUBSURFACE REVENUE` [C31]"]),
     claims(C31)),
    # And the other half of the same rule: the cite is skipped, the number that
    # merely LOOKS like part of one is not. Nothing verifies 1606 shareholders,
    # including C31, whose notes carry 1606 only inside the citation.
    ("a bare figure that echoes the section number", False, "NO claim",
     dossier(["- Record block, mono 26px: `43 U.S.C. 1606(i)   70% OF TIMBER "
              "AND SUBSURFACE REVENUE` [C31]",
              "- Mono block, 26px: `1606 SHAREHOLDERS AT INCORPORATION` [C31]"]),
     claims(C31)),
]


def run_case(tmp, sb, cj):
    d = Path(tmp)
    (d / "storyboard.md").write_text(sb)
    (d / "claims.json").write_text(json.dumps(cj, indent=1))
    p = subprocess.run([sys.executable, str(CHECK), "--run-dir", str(d), "--json"],
                       capture_output=True, text=True, timeout=60)
    rep = json.loads(p.stdout)
    fails = [x for s in rep["slides"] for x in s["fails"]
             if "planned copy prints" in x]
    return fails


def main():
    ok = True
    for name, should_pass, needle, sb, cj in CASES:
        tmp = tempfile.mkdtemp(prefix="figback_")
        try:
            fails = run_case(tmp, sb, cj)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        got_pass = not fails
        good = (got_pass == should_pass)
        if good and needle:
            good = any(needle in f for f in fails)
        ok &= good
        print("[%s] %-42s -> %s" % ("HOLD" if good else "BROKE", name,
                                    "clean" if got_pass else fails[0][:110]))
    print("figure_backing_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
