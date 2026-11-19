# AUTOMATION RETRO, run No.118, 2026-11-18

## The standing weakness (trend_check --window 10)
Artwork craft has been the weakest criterion in 7 of the last 10 runs (mean 7.15). This run attacked it in the plan (CRAFT PLAN with a masterful depth frame built first, lit grounds under every object from the first build, contact rects measured with contact_probe), and spent all three editing rounds on art. Work on the root (machine changes to raise the craft floor) is the weekly pass's: machine_due says the next pass is due 2026-11-24 (last pass 2026-11-17). Queued for it: the akperf face/side material and segment defaults, and a shape census for inline drawings repeated across frames.

## Deviations, phase by phase
- Wake: `$CLAUDE_EFFORT` read medium; settings carry high. Same as No.117. Not fixable from inside a run (the scheduled trigger passes no level).
- Phase 3.6: gaswatch_health FAILed with `collected_after_post`, but the collector log proves CINGSA's dashboard still showed the 09:00 posting at 01:19Z, after its 16:00 reading's stamp (01:00Z). A dispatched gaswatch.yml rerun (44470235563) collected 8.06 Bcf at 06:12Z, Pages deployed, live audit PASS at 06:16:12Z. The diagnosis wording is wrong for a late dashboard; queued.
- Phase 3: the fact-checker's WebFetch got 403 on the FAA fact sheet PDF; the showrunner fetched it with scripts/fetch_pdf_text.py and admitted 9 claims with that fetch on record (the routine's own PDF route). The Anchorage-center inclusion in SMART stayed unverified and was kept off every surface.
- Phase 7: aggregate_check had no honest kind for a duration between two clock times (261 minutes, 11:54 a.m. AKST to 8:15 p.m. ET) or a sum of two claims (827 = 670 + 157). Added `clock_duration` and `sum` (strict, each FAILs on bad arithmetic) with tests/aggregate_clock_sum_verify.py, committed in ebe82d85 and its follow-up. That is a mid-run fix of a gate that could not express the deck, and it tightens rather than loosens.
- Phase 7: assets/js/akperf.js added (one plate builder for three GPU frames, because a slide can't share code with a sibling).
- Phase 8: round 1 critics returned all nine revise (5.2 to 7.8). Causes repeated across frames: dark PBR plate faces (01, 09), weak lower thirds (03, 05), labels detached from their rows (04). Round 2: 06 ship 8.0, rest 5.8 to 7.0. Round 3 (flow): headline honesty on 05, a breather that was the densest frame (07), a box behind the 09 plate.
- Caption room: the critic chose B with one fix and caught "officials say no link" overstating C12; the same overstatement sat on slide 06's guard line and was fixed there too.

## Fetch counts (SOURCE FETCH SCOPE)
Fact-checker: 12 WebFetch calls, 9 distinct URLs, one justified repeat (Petroleum News, to confirm a missing figure was absent). Showrunner: 1 PDF fetch (FAA ZAN fact sheet) plus docket refresh fetches (Federal Register API, AIDEA schedule and agenda PDF, DOE, AEA, state notice, UA, KPBSD twice with 503).

## Machine changes this run
- scripts/aggregate_check.py: `clock_duration` and `sum` kinds; tests/aggregate_clock_sum_verify.py.
- assets/js/akperf.js: perforated plate builder.
No weekly pass today (machine_due exit 1). Queued 4 items in knowledge/MACHINE_QUEUE.md.
