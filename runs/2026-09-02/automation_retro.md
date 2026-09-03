# AUTOMATION RETRO — run No.48, 2026-09-02 (Phase 12)

Six build rounds to a shippable deck, final score 8.52 against a 7.70
threshold. Every hard fail in this run was caught by a HUMAN-SHAPED reviewer
(pixel critic, flow room, scorer) and none by a machine gate. That is the
finding: the gates are all pointed at whether the code was right, and the
defects were all in whether the picture was right.

## Deviations, with evidence

**D1 — a rendered row dropped the noun its claim turns on (near hard fail).**
Slide 08, round 3, printed two absentee rows without the word APPLICATIONS.
C18 is "Absentee by mail applications are due September 29th, 2026 at 5:00
p.m." and C19 is "Electronic absentee applications close October 5th, 2026 at
noon"; both are about the APPLICATION, not the ballot, and slide 08 is the one
frame a voter acts from. copy_sync_check passed because copy.json and the
render agreed with each other; both were wrong against the claim.
`copy_sync_check.py` is one-directional by design (authored -> rendered) and
nothing in the machine runs copy -> CLAIM. Spec gap, not an operator error.

**D2 — a slide argued the inverse of its own claims (near hard fail).** Slide
07's spec plate has four stamped fields with the fourth deliberately never
struck, which is how the deck draws C06/C31 ("the ordinance does not include a
fiscal analysis") instead of asserting it. The four canvas markers were placed
at `py + 42 + f*39`, counted off the plate RECTANGLE. The stamp wrapped to five
lines in its 330 px box, every marker slid up one row, and the unstruck tab
landed on `AMENDABLE . NO`. render.py, qa.py, bespoke_check, dossier_check and
every gate_status row were green. Nothing compared authored line count to
rendered line count. FIXED THIS RUN (upgrade U2).

**D3 — the thumb and the full-size PNG came from two different builds.** A
round edited slide 03, re-ran render.py, and never re-ran assemble.py, so
thumbs/, contact_sheet.png and the PDF described the previous render. A pixel
critic caught it by transcribing both. assemble_report.json recorded the PDF
size, the mode and a slide count and nothing about WHICH renders it was made
from, so the divergence was undetectable by arithmetic. FIXED THIS RUN (U1).

**D4 — frame_balance answered with addition when the cure was subtraction.**
`frame_balance` box-downsamples 6x and therefore responds to luminance STEPS at
cell scale, not to smooth grading. Slide 01's dead lower zone was answered with
34 soft radials and fell from 41 to 31 percent of cell craft. What worked was
removing the text bloom's flat pale lane: its padding was `half-width + 72`,
which on an 880 px block is a 542 px radius ellipse, 1084 px wide. Root cause
still live in the shared helper: `AKSEAM.bloom`'s default `grow: [72, 38]` is a
flat constant ADDED to the half-width, so every wide chip in every future deck
inherits a bloom wider than the frame's lower third. Recommended, not shipped
(see below).

**D5 — a filled face put a tonal step through a word.** The mass is drawn as
filled polygons and only its STROKES were broken around type, so slide 02
shipped a hard rule through a mono chip ending at x 675 (where that sheet's
reach ended), reading as a strike-through. qa.py graded it a WARN.
`AKSEAM.lineLift` now lifts each text line's box back to the lit value, which
is the in-run fix.

**D6 — the declared continuity device was not in the pixels.** The artwork
ledger let this deck declare `panorama` as its primary continuity device for
six rounds while the render carried nothing of the kind. The flow room and the
scorer found it independently. Nothing checks a declared device against a
render. NOT FIXED, and see the measurement below, which is the reason.

**Environment.** No install failures, no fetch failures, no API limits, no
retries attributable to the machine. render.py, qa.py and assemble.py all ran
clean; the six rounds were editorial, not infrastructural.

## Frontier scan — focus (e), headless Chromium and Playwright

Chosen as the stalest legal slot (last scanned 2026-08-25) and distinct from
the last three logged foci (2026-09-01 LinkedIn platform, 2026-08-31 typography
and layout, 2026-08-30 agent workflows). Also the most relevant slot available:
three of this run's six deviations are about MEASURING a laid-out page from the
browser, which is what this area is.

Six searches, two substantive reads, two local experiments.

1. THE FINDING, and it is a live risk here. Playwright 1.57 stopped shipping
   Chromium and now manages Chrome for Testing, headed as `chrome` and headless
   as `chrome-headless-shell` (playwright.dev/docs/release-notes). This repo
   runs playwright 1.62 against browsers at revision 1194 and
   `launch_chromium` finds them with a `chromium-*/chrome-linux/chrome` glob.
   When that glob stops matching, the ordering fix of 2026-08-27 has nothing
   left to order and the fallback returns the default channel, which since 1.57
   is the shell. Measured on this machine, same flags, same target: the full
   browser fetches a file:// asset, `headless_shell` returns "Failed to fetch".
   That breaks every geodata slide SILENTLY. APPLIED as U3.
2. Range.getClientRects is confirmed as the standard way to read rendered line
   boxes (bennadel.com/blog/4310, MDN). Corroborates U2's mechanism; the caveat
   both sources name, that it is meaningless on mixed content, is why U2 skips
   any block with element children other than <br>.
3. A SUBTRACTION. `--font-render-hinting=none` and `--disable-lcd-text`, which
   the search surfaced as the standard determinism flags, are already in
   CHROMIUM_ARGS. Nothing to do.
4. CSS scroll-state container queries (Chrome 133/144) can query an
   `overflowing` state from CSS with no JS. Not usable here: a slide is a fixed
   1080x1350 frame with no scroller, so there is nothing to query.

## Upgrades shipped (3)

U1 assemble.py records the sha256 of every render PNG and slide HTML it
   consumed; gate_status's `assemble` row re-hashes and FAILS on divergence.
U2 render.py measures authored vs rendered line count for every block that
   declares its lines; qa.py WARNs on drift.
U3 launch_chromium probes a candidate browser's file:// fetch capability
   instead of inferring it from the path, and knows the Chrome for Testing
   layouts.

## Not shipped, and why

**A gate comparing a rendered string against the verbatim of the claim it
cites (D1).** This is the highest-severity deviation of the run and it does not
have a safely boundable gate yet. The obvious form does not work: C18's
`verbatim` is "Tuesday, September 29, 2026, at 5:00 p.m." and contains no noun
at all, so a verbatim comparison passes the defective row. The defect is an
OMISSION from the claim's SUBJECT ("absentee by mail applications"), and every
formulation tried here either needs subject-phrase parsing or over-triggers:
requiring all of a claim's significant tokens to survive into a label makes C02
("The Fairbanks North Star Borough regular municipal election is October 6th,
2026, with polls open from 7:00 a.m. to 8:00 p.m.") demand eight tokens of a
five-word row. A declaration-based form modelled on `aggregate_check`'s
`from_claim` kind is the promising shape, adding a `date` kind that requires a
member claim and a declared event whose tokens must appear in BOTH the claim
and the printed string; the deck prints 11 date strings, so the authoring cost
is comparable to the existing aggregates burden. It needs calibration across
several decks' claim sets before it is safe to make a ship gate, which is a
redesign, so this is a RECOMMENDATION and not code. Until it exists, slide 08's
class of row is guarded only by the fact-checker and the critics.

**A seam-continuity check off the shipped PNGs (D6).** Built the measurement
and it says the gate cannot ship yet. Taking each slide's last and first W/60
columns as row luminance profiles and correlating them, run No.48's ADJACENT
pairs score a mean r of 0.082 against 0.100 for non-adjacent pairs in the same
deck; RMS step is 88 for adjacent against 88 for non-adjacent. In other words
the shipped deck, AFTER akseam.js, still carries no measurable pixel continuity
at its seams. AKSEAM.y makes the LANE a continuous function of global x, which
is a real improvement and is not the same thing as an image that continues. A
gate written to this metric would fail the deck that just shipped, with no fix
path short of rebuilding how the art is composed, so it is PARKED with the
numbers rather than shipped. That the metric disagrees with the ledger's
declaration is itself the answer to D6, and it is the strongest argument yet
that "panorama" should have to be earned.

**fanBloom / AKSEAM.bloom padding (D4).** `grow: [72, 38]` should scale with
the SHORTER side of the text box rather than being a flat constant added to the
half-width. Real bug, one line, and it changes the look of every slide that
blooms a wide chip, which makes it an art decision rather than a machine fix on
the last night of a run. Recommended to the maintainer.

## What the machine should learn from this run

Every one of D1, D2 and D6 is the same shape as the 2026-08-25 buried motif,
the 2026-08-31 clipped marks and the 2026-09-01 empty fills: the code was right
and the picture was wrong, and every instrument was pointed at the code. The
gates added since have been closing that gap one question at a time (did the
ink survive, did the canvas ever have anything to survive, can the assertion
fail). U2 adds the next one: does the TYPE still have the shape the art was
positioned against. D1 and D6 name the two questions still unasked: does the
row still say what its claim says, and does the deck do what its ledger says it
does.
