# AUTOMATION RETRO, run No.39, 2026-08-21

Deck shipped at 8.54 against a threshold of 8.3, in two scoring rounds. Round 1
scored 7.80 raw and was capped to 6.9. Nine slides, every machine gate green at
the ship gate, PR #315 merged to main at b5376f1.

This retro walks run_state.json phase by phase against
prompts/routine_instructions.md and lists every deviation with the evidence for
it, then names which ones became machine changes today.

## PHASE WALK

| phase | spec | what happened | deviation |
|---|---|---|---|
| wake | run date is the first date with no runs/<date>/ | 2026-08-21 chosen at 23:14 AKDT on the 20th, reasoned in run_state.date_note | none |
| craft_refresh | read the knowledge base, append what is new | FIELD_NOTES 2026-08-21 entry written before the build | none |
| research | scouts in parallel | six scouts A-F into scout_merge.md | none |
| claims | claims_check PASS | 47 verified, 11 primary, 15 killed | none |
| docket 3.5 | maintain ledger/docket.json | six items refreshed, one material AIDEA correction | none |
| gas watch 3.6 | read-only sign-off, presentation fixes only | site_signoff 18/18, pagecheck 15/15, one presentation fix in site_build.py (mobile nav hit area) | none; collectors and ledgers untouched, as required |
| selection | dedupe_check | one LIKELY DUPLICATE read in full and rejected | none |
| directors_room | dossier_check PASS | 3 directors synthesised, 9 dossiers, PASS 9/9 | none |
| copy | caption_check with --ledger --deck-summary --copy | PASS, 900 chars, 5.0 commas/100w | none |
| art_build | qa.py exit 0 before Phase 8 | 0 fails; asserts, contacts, encodings declared | **D1**, **D2**, **D3** |
| pixel_review | loop until every slide verdicts ship, max 4 rounds | 2 rounds, 5 critics each, mean 4.5 to 5.7 | **D5** |
| flow_review | max 2 rounds | one round, 7.2 as a sequence, all findings applied | none |
| assemble | vector PDF, 2-25 MB | vector, 3.56 MB, 9 slides | none |
| scoring | a low score is a work order | round 1 7.80 raw capped 6.9, defects fixed, round 2 8.54 | **D4** |
| ship | merge before the email | branch pushed, PR ready, merged, both raw URLs 200 | none |

## DEVIATIONS, WITH EVIDENCE

**D1. A display headline was typeset by the browser and every gate agreed.**
slide-07.html styled its `<h2>` with position, left, top, width, family, weight,
variation settings, line-height, tracking and colour, and no `font-size`, and
the file never loaded `assets/js/aktype.js`, so `AK.fitText` was never called on
it. Chromium's user-agent rule then set the deck's hook line at 1.5em of an
unstyled 16px root: 24px, the same size as the mono labels beside it, 9.6px at
the 432px feed width the doctrine reviews at. It passed render.py, qa.py,
dossier_check and copy_sync_check and reached a pixel critic before a human
named it. Nothing here was close to catching it: 24px clears the 24px mobile
floor exactly, it collides with nothing, its contrast is 16:1, and a slide that
never calls fitText declares no fit record for the maxLines gate to grade.
This is the highest-value catch the run offered and it is upgrade 1.

**D2. Two self-assertions shipped that can't fail.** Both are still in the
shipped slide-06.html:

    {what:"the clamp bar covering the whole depth of the seat",
     expect: Math.round(R),
     actual: Math.round(Math.min(CLY+CLH, TOP+R) - TOP), tol:2}
      // CLY = TOP-16, CLH = R+26, so CLY+CLH = TOP+R+10 and the min IS TOP+R

    {what:"the rail bar against its own 180 day span",
     expect:820, actual: Math.round(DAYS*DAY_PX), tol:2}
      // DAY_PX = RSPAN/DAYS = 820/180, so DAYS*DAY_PX is 820 by construction

Both reported PASS in machine_qa.json and both made the QA report claim
something had been checked when nothing had. Note the tension with the assert
gate's own advice, "derive one FROM the other so they can't disagree": deriving
the DRAWING from the printed number is right and is what slide 06 did, but then
recomputing `actual` from the same constant instead of from the value handed to
the drawing call is what empties the assertion. PARKED, see below.

**D3. Roughly two thousand invented per-point values were drawn as chart
soundings** on slides 01 and 04, generated from a noise field, on a deck whose
thesis is that nothing in this record was measured. The record holds one depth
fact, C14. Caught by a reader, not a gate, and fixed in-run by replacing them
with survey cross ticks (BUILD RECONCILIATION rows for slides 01 and 04).
aggregate_check sees aggregate ASSERTIONS in text runs; nothing looks at a
numeral field drawn to canvas. PARKED, see below.

**D4. Round 1 was capped 0.9 by the run record, not by the deck.** score_report
round_1: raw 7.80, weighted 6.9, "one hard fail, unfinished artifact". The
storyboard reaching the scorer carried a stale generated gate block and no BUILD
RECONCILIATION section at all, though Phase 8 step 1b has required one since
2026-07-25 and gives the measured reason (2026-07-25's critics graded a third of
their findings against superseded dossier numbers). gate_status.py already has
`--sync`, `--require` and `--verify-pasted` for the staleness half; nothing had
ever checked that the section exists. That is upgrade 2.

**D5. Two critic findings were wrong and each cost a rebuild cycle before
measurement disproved them.** From score_report.showrunner_findings_rejected: a
claimed texture leak inside slide 04's gold limit (measured mark density 0.27
outside, 0.00 inside at every band; the dark region was the label's own opaque
knockout) and a claimed non-square square (the gold bbox scan was catching the
gold label and the leader above the square; the drawn side is 783 render px
against AK_SIDE 780 plus a 4px stroke). Both were sampling artifacts. There is
no committed tool a showrunner can reach for to measure a declared region's mark
density or a drawn rectangle's aspect off a render, so each rebuttal was
improvised. PARKED, see below.

No environment breakage this run: no failed installs, no fetch failures, no API
limits inside the run itself, no degraded fallbacks on the ladder, and no
repeated retries. The only degraded resource was in THIS phase (see the scan).

## UPGRADES MADE (2)

1. **TYPE NOBODY SIZED, a new qa.py hard fail** (engine). render.py now records,
   per text element, whether any author `font-size` applies anywhere on its
   ancestor chain: an inline style (which is what AK.fitText writes), an SVG
   presentation attribute, or a matching rule in a readable stylesheet. qa.py
   FAILs when none does, because the size then came from the UA stylesheet and
   the 16px initial value alone. Unreadable stylesheets are counted and demote
   the finding to a WARN that says the check went partly blind.
2. **`reconciled`, a new gate_status.py row** (scripts). FAILs under `--require`
   and WARNs mid-run when storyboard.md carries no BUILD RECONCILIATION heading,
   or carries one with nothing under it. Deliberately the weakest possible test
   of content, because the failure that actually happens is total absence and a
   stricter test would only teach a run to pad.

## PARKED (3), with the unblocking condition for each

- **The tautological assert (D2).** Detectable in principle: expand `actual` and
  `expect` under constant propagation of the slide's own `const` declarations
  and flag the pair when they reduce to the same expression. Not shipped today
  because a partial version (require `expect` to be a numeric literal) catches
  one of this run's two cases and false-fails the legitimate pattern where the
  printed number lives in a named constant. Unblocking condition: a small
  expression reducer tested against every `__akAssert` in the shipped corpus,
  with the two No.39 asserts as the known-bad and the No.31 dimension lock as
  the known-good.
- **The numeral field nobody can trace (D3).** render.py's canvas-text hook
  already records every fillText string, so counting numerals drawn to canvas is
  cheap; deciding which are legitimate is not (axis ticks and unit labels are
  numerals too). Unblocking condition: a rule stated in terms of DISTINCT
  unexplained values, cross-checked against copy.json and the declared scales,
  calibrated on decks that legitimately print dense numerals.
- **The measurement helper for critic rebuttals (D5).** A committed
  `region_measure` that reports mark density inside and outside a declared rect
  and the ink bbox and aspect of a drawn figure, off a render. Real value, low
  risk, but it is a tool rather than a gate, and a tool nobody is told to reach
  for is shelfware. Unblocking condition: name it in the pixel-critic and
  showrunner prompts in the same change, so a disputed finding has a named
  command instead of an improvisation.

## FRONTIER SCAN

Focus (a), LinkedIn platform and algorithm changes that move the craft numbers.
Last scanned 2026-08-08, the stalest slot, and different from the last three
logged foci (d, f, b). Recorded honestly: this session's WebSearch budget was
already exhausted by the run itself (200 of 200), so the scan was eight direct
WebFetch reads of known sources rather than a search sweep, and four of them
404'd. Nothing was applied.

What the readable sources say: Socialinsider's 2026 benchmarks put native
documents first at 7.00% engagement, up 14% year over year, with multi-image
second at 6.45%, video at 6.00% and video VIEWS down 36% year over year, on a
platform average of 5.20%. knowledge/CAROUSEL_CRAFT.md already carries the 7.00%
figure and the format ranking, so this is a confirmation, not news. Buffer's
algorithm page restates relevance/expertise/engagement, dwell as the ranking
signal and hook-first, all of which are already hard rules here. No source found
today reports slide-count effects, aspect-ratio effects, or any change to
document rendering that would move an engine parameter.

Parked as a dated FIELD_NOTES candidate: the year-over-year deltas and the
multi-image format rising above video, which is the only ranking change in the
data, with the source URL.
