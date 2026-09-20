#!/usr/bin/env python3
"""subset_assert_verify.py -- the defect reconstruction behind aggregate_check's
`subset` kind (2026-09-20, run No.64), plus the eight holes Codex found in the
first cut of that gate on PR #391.

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

This runs the REAL aggregate_check against render reports carrying the exact
shipped string and the real C27 verbatim, so every fixture below is the defect,
a near miss of it, or one of the ways a gate with holes would have waved it
through.

  python tests/subset_assert_verify.py           # exit 0 = the gate holds

THE ORIGINAL SEVEN
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

THE EIGHT CODEX HOLES (PR #391), numbered as he filed them
  1 over_total    "Twelve of the ten items", declared as an
                  ordinary ten-member COUNT. The count
                  detector reads only "ten items" and
                  ignores the numerator, so the whole
                  report was PASS                          -> FAIL, IMPOSSIBLE
  2 all_but_nine  "All but nine of the ten items" means ONE
                  item. The all-but branch skipped without
                  claiming its match, so RX_SUBSET read the
                  nested "nine of the ten" with the
                  OPPOSITE meaning                         -> no 9-of-10 detection
  3 decl_replaces the shipped string, covered by a
                  declaration carrying n 5 / of 10 and five
                  correctly selected items. Declared
                  figures used to REPLACE the printed ones  -> FAIL, corroboration
  4 item_edges    an enumeration whose items end in the
                  characters of " ;.,and": strip() is a
                  CHARACTER SET, so "Borough land" parsed
                  as "Borough l"                           -> PASS, and the
                                                             receipts read whole
  5 tail_xref     C27 followed by "see subsection (9)". Any
                  later parenthetical cleared the whole run
                  and the claim reported as unenumerated,
                  which let Route B skip the item check     -> FAIL, DOES enumerate
  6 compound_ten  "Two of 30 precincts" against a claim that
                  says "thirty two". The word loops recorded
                  2 and 30 as well as 32                   -> FAIL, neither figure
  7 decimal_lend  "None of the ten stations" against a claim
                  whose only zero is inside "0.01 inches"   -> FAIL, 0 not a figure
  8a term_inside  terms matched as bare substrings, so "air"
                  was found inside "Repairs" and a lying
                  selection passed                         -> FAIL, matches NONE
  8b term_words   THE OTHER HALF, a negative control: the
                  honest selection of "Air quality" and
                  "Land surveys" used to FAIL, because
                  "air" is in "Repairs" and "land" is in
                  "Island"                                  -> PASS

CODEX ROUND TWO (PR #391, head 80792e7)
  2 ratio_digits  "9 of 10 items ask about the payload"
                  declared as a `ratio` over C27's real
                  enumeration with the WRONG first nine.
                  RX_RATIO is digits-only and runs first,
                  so it claimed the span and verify_subset
                  never saw the string; ratio proves the
                  arithmetic and never reads a predicate
                  or a term                                 -> FAIL, ENUMERATES
  2 ratio_subset  the same digit form declared HONESTLY as
                  a subset, which the detector records as a
                  ratio: covers() has to let the stronger
                  declaration answer for it                 -> PASS
  2 ratio_found   NEGATIVE CONTROL: the "0 OF 5 FOUND"
                  shape ratio was built for, over a notice
                  that enumerates nothing                   -> PASS
  4 tie_later     two completed enumerations of EQUAL
                  length, the superseded list first and the
                  adopted one second. max() returns the
                  FIRST maximal element, against the
                  documented policy that a tie takes the
                  later run                                 -> PASS, on New A/B
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
    # The SAME ordinance, with the cross reference a statute normally carries
    # after its own list. Codex finding 5.
    {"id": "C28",
     "claim": "Ordinance 2026-35 would require ten items in an application.",
     "value": "ten items",
     "verbatim": C27_VERBATIM + " See subsection (9) for the fee schedule.",
     "source_url": "https://kpb.legistar1.com/kpb/attachments/73cfabad.docx",
     "source_is_primary": True,
     "notes": ""},
    {"id": "C40",
     "claim": "The hand count audit sampled two of 32 precincts.",
     "value": "two of 32 precincts",
     "verbatim": "The board selected two of the 32 precincts at random for the "
                 "hand count audit.",
     "source_url": "https://www.elections.alaska.gov/audit.pdf",
     "source_is_primary": True,
     "notes": ""},
    # Codex finding 6: the only figure here is thirty two, as one number.
    {"id": "C41",
     "claim": "The board sampled thirty two precincts by hand.",
     "value": "thirty two precincts",
     "verbatim": "The board sampled thirty two precincts by hand.",
     "source_url": "https://www.elections.alaska.gov/audit.pdf",
     "source_is_primary": True,
     "notes": ""},
    # Codex finding 7: the only zero here is inside a decimal.
    {"id": "C42",
     "claim": "Every one of the ten gauges reported 0.01 inches of rain.",
     "value": "0.01 inches",
     "verbatim": "Each gauge reported 0.01 inches of precipitation across the "
                 "ten stations that morning.",
     "source_url": "https://www.weather.gov/afc/obs",
     "source_is_primary": True,
     "notes": ""},
    # Codex findings 4 and 8: items whose last word is built from the
    # characters of " ;.,and", and items that CONTAIN a term inside a longer
    # word ("Repairs" holds air, "Island" holds land).
    {"id": "C43",
     "claim": "The borough's capital list carries four items.",
     "value": "four items",
     "verbatim": "The capital list is as follows: (1) Repairs to the dock; "
                 "(2) Island access roads; (3) Air quality monitoring; and "
                 "(4) Land surveys.",
     "source_url": "https://kpb.legistar1.com/kpb/attachments/capital.pdf",
     "source_is_primary": True,
     "notes": ""},
    # Codex round two, finding 2's negative control: the shape `ratio` was
    # built for. A notice, not a list, so nothing enumerates.
    {"id": "C05",
     "claim": "The solicitation never uses any of the five machine-learning terms.",
     "value": "0 of 5",
     "verbatim": "A full text search of the solicitation for artificial "
                 "intelligence, machine learning, automated speech recognition, "
                 "ASR and AI returned no occurrence of any of the five.",
     "source_url": "https://sam.gov/opp/abc",
     "source_is_primary": True,
     "notes": ""},
    # Codex round two, finding 4: two completed runs of the same length, the
    # superseded list first and the adopted one second.
    {"id": "C45",
     "claim": "The adopted permit names two entries.",
     "value": "two entries",
     "verbatim": "The list was amended. Superseded: (1) Old A; (2) Old B. "
                 "As adopted: (1) New A; and (2) New B.",
     "source_url": "https://kpb.legistar1.com/kpb/attachments/amended.pdf",
     "source_is_primary": True,
     "notes": ""},
    {"id": "C44",
     "claim": "The permit names two borough parcels.",
     "value": "two parcels",
     "verbatim": "The permit covers the following: (1) Borough land; and "
                 "(2) Flight duration.",
     "source_url": "https://kpb.legistar1.com/kpb/attachments/permit.pdf",
     "source_is_primary": True,
     "notes": ""},
]}

DEFECT = ("Nine of the ten items ask about the payload. The tenth asks for "
          "coordinates.")
TRUTH = ("Five of the ten items ask about the payload. Four ask about the "
         "flight.")
PRECINCTS = "Two of 32 precincts were sampled."
OVER = "Twelve of the ten items ask about the payload."
ALLBUT9 = "All but nine of the ten items ask about the payload."
PRECINCTS30 = "Two of 30 precincts were sampled."
GAUGES = "None of the ten stations reported measurable rain."
CAPITAL = "Two of the four items name the air and the land."
PARCELS = "Two of the two entries name a place and a span."
NINE_DIGITS = "9 of 10 items ask about the payload."
FIVE_DIGITS = "5 of 10 items ask about the payload."
FOUND = "0 OF 5 FOUND"
ADOPTED = "Two of the two entries name the adopted pair."
SEARCH_TERMS = ["artificial intelligence", "machine learning",
                "automated speech recognition", "ASR", "AI"]

PAYLOAD_TERMS = ["chemical", "flare", "pyrotechnic", "material", "msds"]
FLIGHT_TERMS = ["flights or activities", "weather modification activities"]

# A count declaration for "ten items" that is individually perfect. Before
# Codex finding 1 was fixed, this made the whole OVER report read PASS.
TEN_ITEMS = ["Type of chemicals", "Quantity of chemicals",
             "total weight of flares", "Total pyrotechnic material", "MSDS",
             "Frequency of weather modification", "altitude of individual flights",
             "Total duration of all flights", "Maximum total flights",
             "Release coordinates"]


def has_fail(needle):
    return lambda rep: (any(needle in f for f in rep["fails"]),
                        "a FAIL naming %r" % needle)


def clean(rep):
    return (not rep["fails"], "a clean pass")


def no_subset_n(n):
    """No subset detection anywhere claiming a subset of n members."""
    def check(rep):
        bad = [h for h in rep["detections"]
               if h["kind"] == "subset" and h.get("n") == n]
        return (not bad and not rep["fails"],
                "no subset detection of %d and no fail (got %r)" % (n, bad[:1]))
    return check


def receipts_read(*wanted):
    """The selected items in the report read as whole strings."""
    def check(rep):
        got = [it["text"] for s in rep.get("subsets", []) for it in (s.get("selected") or [])]
        return (not rep["fails"] and got == list(wanted),
                "a clean pass whose receipts read %r (got %r)" % (list(wanted), got))
    return check


FIXTURES = [
    # name, rendered text, declarations, assertion, must a subset be detected
    ("undeclared", DEFECT, [], has_fail("UNDECLARED subset"), True),
    ("from_claim", DEFECT,
     [{"kind": "from_claim", "slide": 7, "text": DEFECT, "member": "C27"}],
     has_fail("UNDECLARED subset"), True),
    ("route_b", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "basis": "the ordinance does not number its requirements in a way this "
                "gate can read, so the items are not addressable"}],
     has_fail("is not in claim C27's own claim/value/verbatim"), True),
    ("route_a_lie", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "selected": [1, 2, 3, 4, 5, 6, 7, 8, 9], "terms": PAYLOAD_TERMS,
       "predicate": "ask about the payload"}],
     has_fail("matches NONE of the declared terms"), True),
    ("route_a_gamed", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "selected": [1, 2, 3, 4, 5, 6, 7, 8, 9],
       "terms": PAYLOAD_TERMS + ["flight"],
       "predicate": "ask about the payload"}],
     has_fail("matches NONE of the declared terms"), True),
    ("route_a_true", TRUTH,
     [{"kind": "subset", "slide": 7, "text": TRUTH, "fragment": "Five of the ten",
       "member": "C27", "selected": [1, 2, 3, 4, 5], "terms": PAYLOAD_TERMS,
       "predicate": "ask about the payload, the chemicals or the pyrotechnics"},
      {"kind": "subset", "slide": 7, "text": TRUTH, "fragment": "Four ask about",
       "member": "C27", "selected": [6, 7, 8, 9], "terms": FLIGHT_TERMS,
       "predicate": "ask about the flight rather than the payload",
       "n": 4, "of": 10}],
     clean, True),
    ("route_b_true", PRECINCTS,
     [{"kind": "subset", "slide": 7, "text": PRECINCTS, "member": "C40",
       "basis": "the audit board's own record names the sample size and the "
                "precinct total and enumerates neither set"}],
     clean, True),

    # ---- the eight Codex holes ----------------------------------------
    ("1 over_total", OVER,
     [{"kind": "count", "slide": 7, "text": OVER, "fragment": "ten items",
       "subject": "items", "members": ["C27"], "items": TEN_ITEMS}],
     has_fail("IMPOSSIBLE subset"), True),
    ("2 all_but_nine", ALLBUT9, [], no_subset_n(9), False),
    ("3 decl_replaces", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C27",
       "selected": [1, 2, 3, 4, 5], "terms": PAYLOAD_TERMS,
       "predicate": "ask about the payload", "n": 5, "of": 10}],
     has_fail("it never replaces it"), True),
    ("4 item_edges", PARCELS,
     [{"kind": "subset", "slide": 7, "text": PARCELS, "member": "C44",
       "selected": [1, 2], "terms": ["borough land", "flight duration"],
       "predicate": "name a place and a span"}],
     receipts_read("Borough land", "Flight duration"), True),
    ("5 tail_xref", DEFECT,
     [{"kind": "subset", "slide": 7, "text": DEFECT, "member": "C28",
       "basis": "the ordinance does not number its requirements in a way this "
                "gate can read, so the items are not addressable"}],
     has_fail("DOES enumerate 10 item(s)"), True),
    ("6 compound_ten", PRECINCTS30,
     [{"kind": "subset", "slide": 7, "text": PRECINCTS30, "member": "C41",
       "basis": "the board's own record names the sample size and the precinct "
                "total and enumerates neither set"}],
     has_fail("the subset figure 2 is not in claim C41"), True),
    ("7 decimal_lend", GAUGES,
     [{"kind": "subset", "slide": 7, "text": GAUGES, "member": "C42",
       "basis": "the observation record names the station count and the reading "
                "and enumerates neither set"}],
     has_fail("the subset figure 0 is not in claim C42"), True),
    ("8a term_inside", CAPITAL,
     [{"kind": "subset", "slide": 7, "text": CAPITAL, "member": "C43",
       "selected": [1, 3], "terms": ["air"],
       "predicate": "name the air and the land"}],
     has_fail("matches NONE of the declared terms"), True),
    # ---- Codex round two --------------------------------------------
    ("2 ratio_digits", NINE_DIGITS,
     [{"kind": "ratio", "slide": 7, "text": NINE_DIGITS, "members": ["C27"],
       "items": TEN_ITEMS, "found": TEN_ITEMS[:9]}],
     has_fail("ENUMERATES its 10 item(s)"), False),
    ("2 ratio_subset", FIVE_DIGITS,
     [{"kind": "subset", "slide": 7, "text": FIVE_DIGITS, "member": "C27",
       "selected": [1, 2, 3, 4, 5], "terms": PAYLOAD_TERMS,
       "predicate": "ask about the payload, the chemicals or the pyrotechnics"}],
     clean, False),
    ("2 ratio_found", FOUND,
     [{"kind": "ratio", "slide": 7, "text": FOUND, "members": ["C05"],
       "items": SEARCH_TERMS, "found": []}],
     clean, False),
    ("4 tie_later", ADOPTED,
     [{"kind": "subset", "slide": 7, "text": ADOPTED, "member": "C45",
       "selected": [1, 2], "terms": ["new a", "new b"],
       "predicate": "name the adopted pair"}],
     receipts_read("New A", "New B"), True),
    ("8b term_words", CAPITAL,
     [{"kind": "subset", "slide": 7, "text": CAPITAL, "member": "C43",
       "selected": [3, 4], "terms": ["air", "land"],
       "predicate": "name the air and the land"}],
     receipts_read("Air quality monitoring", "Land surveys"), True),
]


def render_report(text):
    return {"slides": [{"file": "slide-07.html",
                        "text_nodes": [{"text": text}]}]}


def main():
    tmp = Path(tempfile.mkdtemp(prefix="subset-gate-"))
    ok = True
    for name, text, decls, assertion, want_detect in FIXTURES:
        d = tmp / name.replace(" ", "-")
        d.mkdir()
        (d / "render_report.json").write_text(json.dumps(render_report(text)))
        (d / "claims.json").write_text(json.dumps(CLAIMS))
        (d / "aggregates.json").write_text(
            json.dumps({"run_date": "2026-09-20", "aggregates": decls}))
        code, rep = ac.run(d)
        if code == 2:
            print("  BAD  %-15s unreadable: %s" % (name, rep.get("error")))
            ok = False
            continue
        detected = [h for h in rep["detections"] if h["kind"] == "subset"]
        good, expected = assertion(rep)
        if want_detect and not detected:
            good = False
            expected += " (and the subset shape was never detected)"
        line = (rep["fails"] or ["(clean)"])[0]
        if good:
            print("  ok   %-15s %s\n       %s"
                  % (name, "FAIL" if rep["fails"] else "PASS", line[:230]))
        else:
            ok = False
            print("  BAD  %-15s expected %s\n       %s"
                  % (name, expected, line[:230]))

    print("\nsubset-of-an-enumeration gate: %s   (fixtures in %s)"
          % ("HOLDS" if ok else "BROKEN", tmp))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
