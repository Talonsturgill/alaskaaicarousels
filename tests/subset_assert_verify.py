#!/usr/bin/env python3
"""subset_assert_verify.py -- the defect reconstruction behind aggregate_check's
`subset` kind (2026-09-20, run No.64).

WHAT IT RECONSTRUCTS. Slide 07 printed "Nine of the ten items ask about the
payload. The tenth asks for coordinates." C27's verbatim enumerates Ordinance
2026-35's ten required items, and (6) frequency, (7) duration and altitude of
individual flights, (8) total duration of all flights and (9) maximum total
flights are FLIGHT questions. FIVE of ten are payload. Slide 06 printed those
four rows verbatim one swipe earlier.

Every machine gate passed it, and the reason is structural rather than
accidental: plan_drift compares the BUILD to the PLAN and the plan carried the
same wrong sentence; copy_sync compares copy.json to the render; dossier_check
backs FIGURES and "nine" is a word; aggregate_check's own ratio detector is
digits-only with no "the" in it. Only the claim's verbatim could catch it, and
the only reader that opens claims.json is the scorer, at the ship gate, where
it capped the run at 6.9 and forced a full return to Phase 8.

This runs the REAL aggregate_check against a render report carrying the exact
shipped string and the real C27 verbatim, so every fixture below is the defect
or a near miss of it.

  python tests/subset_assert_verify.py           # exit 0 = the gate holds

FIXTURES
  undeclared      the string as it shipped, with the run's own aggregates.json
                  (which has no entry for it)              -> FAIL, undeclared
  from_claim      the cheapest way to make an undeclared
                  finding go away: file it as `from_claim`
                  against C27. C27's verbatim contains
                  "(9)", so the old substring number test
                  would have found a 9 and passed         -> FAIL, still undeclared
  route_b         declared as a subset with no item list,
                  taking the not-enumerated route          -> FAIL twice: C27 DOES
                                                             enumerate, and 9 is
                                                             not a figure in it
  route_a_lie     the honest-looking declaration: items
                  1..9 selected, payload terms            -> FAIL, items 6/7/8/9
                                                             match no term
  route_a_gamed   terms widened with "flight" to cover the
                  flight questions                        -> FAIL, item (6) says
                                                             "activities", not
                                                             "flights"
  route_a_true    THE NEGATIVE CONTROL. What the deck
                  should have printed: five of the ten,
                  items 1..5, payload terms               -> PASS, and the report
                                                             carries the items
  route_b_true    NEGATIVE CONTROL for the second route:
                  "Two of 32 precincts were sampled",
                  a real set nothing enumerates            -> PASS
"""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import aggregate_check as ac  # noqa: E402

C27_VERBATIM = (
    "An application for a commercial lease or commercial land use permit for "
    "the temporary use of borough land for the purposes of conducting weather "
    "modification or geoengineering activities must include in the application "
    "the following: (1) Type of chemicals that will be used to attempt weather "
    "modification; (2) Quantity of chemicals that will be used; (3) Quantity, "
    "type, manufacturer, serial number, and total weight of flares; (4) Total "
    "pyrotechnic material used; (5) MSDS for any chemicals or materials to be "
    "released; (6) Frequency of weather modification activities or attempts; "
    "(7) Duration and altitude of individual flights or activities; (8) Total "
    "duration of all flights or activities; (9) Maximum total flights or "
    "activities that will be attempted; and (10) Release coordinates, "
    "including predicted impacted areas.")

CLAIMS = {"claims": [
    {"id": "C27",
     "claim": "Ordinance 2026-35 would require ten items in an application for "
              "a borough commercial lease or land use permit to conduct weather "
              "modification.",
     "value": "ten items",
     "verbatim": C27_VERBATIM,
     "source_url": "https://kpb.legistar1.com/kpb/attachments/73cfabad.docx",
     "source_is_primary": True,
     "notes": "All ten items concern the payload, the pyrotechnics or the "
              "flight. NONE asks about the software that selects time and place."},
    {"id": "C40",
     "claim": "The hand count audit sampled two of 32 precincts.",
     "value": "two of 32 precincts",
     "verbatim": "The board selected two of the 32 precincts at random for the "
                 "hand count audit.",
     "source_url": "https://www.elections.alaska.gov/audit.pdf",
     "source_is_primary": True,
     "notes": ""},
]}

DEFECT = ("Nine of the ten items ask about the payload. The tenth asks for "
          "coordinates.")
TRUTH = ("Five of the ten items ask about the payload. Four ask about the "
         "flight.")
PRECINCTS = "Two of 32 precincts were sampled."

PAYLOAD_TERMS = ["chemical", "flare", "pyrotechnic", "material", "msds"]

FIXTURES = [
    ("undeclared", DEFECT, [], True, "UNDECLARED subset"),
    ("from_claim", DEFECT,
     [{"kind": "from_claim", "slide": 7, "text": DEFECT, "member": "C27"}],
     True, "UNDECLARED subset"),
    ("route_b", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "basis": "the ordinance does not number its requirements in a way this "
                "gate can read, so the items are not addressable"}],
     True, "is not in claim C27's own claim/value/verbatim"),
    ("route_a_lie", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "selected": [1, 2, 3, 4, 5, 6, 7, 8, 9],
       "terms": PAYLOAD_TERMS,
       "predicate": "ask about the payload"}],
     True, "matches NONE of the declared terms"),
    ("route_a_gamed", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "selected": [1, 2, 3, 4, 5, 6, 7, 8, 9],
       "terms": PAYLOAD_TERMS + ["flight"],
       "predicate": "ask about the payload"}],
     True, "matches NONE of the declared terms"),
    ("route_a_true", TRUTH,
     [{"kind": "subset", "slide": 7, "text": TRUTH, "fragment": "Five of the ten",
       "member": "C27", "selected": [1, 2, 3, 4, 5], "terms": PAYLOAD_TERMS,
       "predicate": "ask about the payload, the chemicals or the pyrotechnics"},
      {"kind": "subset", "slide": 7, "text": TRUTH, "fragment": "Four ask about",
       "member": "C27", "selected": [6, 7, 8, 9],
       "terms": ["flights or activities", "weather modification activities"],
       "predicate": "ask about the flight rather than the payload",
       "n": 4, "of": 10}],
     False, ""),
    ("route_b_true", PRECINCTS,
     [{"kind": "subset", "slide": 7, "text": PRECINCTS, "member": "C40",
       "basis": "the audit board's own record names the sample size and the "
                "precinct total and enumerates neither set"}],
     False, ""),
]


def render_report(text):
    return {"slides": [{"file": "slide-07.html",
                        "text_nodes": [{"text": text}]}]}


def main():
    tmp = Path(tempfile.mkdtemp(prefix="subset-gate-"))
    (tmp / "claims.json").write_text(json.dumps(CLAIMS))
    ok = True
    for name, text, decls, want_fail, needle in FIXTURES:
        d = tmp / name
        d.mkdir()
        (d / "render_report.json").write_text(json.dumps(render_report(text)))
        (d / "claims.json").write_text(json.dumps(CLAIMS))
        (d / "aggregates.json").write_text(
            json.dumps({"run_date": "2026-09-20", "aggregates": decls}))
        code, rep = ac.run(d)
        if code == 2:
            print("  BAD  %-14s unreadable: %s" % (name, rep.get("error")))
            ok = False
            continue
        detected = [h for h in rep["detections"] if h["kind"] == "subset"]
        fails = rep["fails"]
        got = bool(fails)
        line = (fails or ["(clean)"])[0]
        bad = got != want_fail
        if not detected:
            bad = True                     # the shape has to be SEEN first
            line = "the subset shape was never detected in %r" % text[:50]
        if got and want_fail and not any(needle in f for f in fails):
            bad = True                     # it must fail for the RIGHT reason
        if not want_fail and not (rep.get("subsets") or [{}])[0].get("selected") \
                and decls and decls[0].get("selected"):
            bad = True                     # a pass has to carry its receipts
        if bad:
            ok = False
            print("  BAD  %-14s expected %s\n       %s"
                  % (name, ("a FAIL naming %r" % needle) if want_fail
                     else "a clean pass", line[:240]))
        else:
            print("  ok   %-14s %s\n       %s"
                  % (name, "FAIL" if got else "PASS", line[:240]))

    print("\nsubset-of-an-enumeration gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
