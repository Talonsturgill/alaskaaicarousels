# Automation retro, run 2026-10-10 (No.83)

Weekly machine pass: NOT DUE. machine_due.py: last pass 2026-10-09, due at seven days; 11 items queued, 0 repeat offenders at repeat 2. This run fixed what broke in it and queued the rest.

## Top repeat offender (trend_check --window 10)
Artwork craft and genuine detail, weakest in 7 of the last 10 runs (mean 6.98, this run 7.0), last worked 2026-10-04 and in the 2026-10-09 weekly pass. Queued for the next weekly pass, which is the answer the daily phase owes. This run's own evidence for that pass: the cover (the masterful depth frame) took four fix rounds and its last two landed without a per-slide review, and three of the four weak frames the scorer named (01, 06, 09) were frames where a critic named a different symptom each round of one root cause (an environment-reflecting floor, inverted hachure density on a dark ground, a card lit too flat). The deferral holds until the weekly pass reads the week's digest; what would make it a daily fix is the same root cause biting a second run before then.

## Deviations, phase by phase
- Phase 3.6: all audits PASS (site sign-off 141 pages 18 of 18, Gas Watch live PASS on the October 8th reading, page check PASS, cron health 6 workflows plus Pages). No incident files.
- Phase 7/8: aggregate_check misread "15,141 of 77,227" as "141 of 77" and failed a correct declaration. Fixed in-run (commit 2d153023, logged in ledger/upgrades.json, kind fix).
- Phase 8: five rounds used, four per-slide and one deck-level. Round 1 all nine frames revise (5.0 to 7.3); round 2 shipped 02; round 3 shipped 03, 04, 05, 07, 08, 09; round 4 shipped 06; 01 took its fourth and fifth fixes without a per-slide review. The flow critic caught an honesty-guard miss no per-slide critic saw (08 stated the lead without UNOFFICIAL).
- Phase 8: contact_probe's h axis proposed a ground rect straddling the card's lit corner on 09. Re-probed by hand. Queue repeat raised to 1.
- Phase 8: qa.py's ragged-display-line warn fired on 05's numeral headline in every round, a false positive the scorer confirmed. Queued (trend_check counts the warn on 4 of 10 runs).
- Phase 8: akhachure's density sits on the lee faces, which inverts for pale ink on a dark ground; akpost bloom tiles on one-pixel emitters. Both fixed in the slide and queued as helper options.
- Phase 10: scored 8.6 against the round-5 threshold of 7.7, no hard fails; art 7.0 under the craft floor, at the five-round cap, so no craft cycle.
- Phase 11: site_build noted the run date is a day ahead of Anchorage and built for 2026-10-09 (the 2026-10-09 fix working as shipped). Browser suites 4 of 4 PASS, site_fresh exact.

## Upgrades
No weekly pass today. One in-run fix (aggregate_check thousands grouping), logged.
