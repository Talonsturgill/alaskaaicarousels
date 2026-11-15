# Automation retro, 2026-11-14 (No.115)

## Top repeat offender (trend_check --window 10)
Artwork craft, weakest on 6 of the last 10 runs (mean 7.15). QUEUED for the weekly pass, which
`machine_due.py` says is not due (last pass 2026-11-11, four days ago). This run spent its
fourth revision round on the CRAFT FLOOR cycle the scorer named (slides 05, 04, 06, 02, 07) and
records art_before / art_after in score_report.craft_cycle for the weekly digest to count.

## Deviations, phase by phase
- Phase 3.5 docket: a new NOAA 2027 observer/EM item was verified but not added; the inline ask
  payload would reach 191,709 of 190,000 bytes. History notes only. Queued (new item).
- Phase 3.6 cron health: WARN on a ghost workflow run (612) recorded as a `github` blocker in
  cron_incidents.json; site sign-off PASS (179 pages), Gas Watch live PASS.
- Phase 8 render: run in batches of three throughout to avoid the exit-137 OOM queued on
  2026-11-13. Repeat raised to 1.
- Phase 8 QA: the grain div rendered as opaque grey until given mix-blend-mode overlay; slide 06's
  orange fill read as an undeclared run inside its scale band; slide 05 shipped an unfilled canvas
  strip between horizon and float for one pass. All fixed in-run; each is a slide-authoring slip,
  not a machine defect.
- Phase 9/10: two pixel rounds, a flow round and a third repair round put the score at 8.08 with
  art 6.5, under the 8.5 craft floor; one craft cycle followed (round 4 of 5).
- Caption critic caught "a person reviews" as unsupported; slide 02, 04 and 08 copy reworded.

## Queue
68 items queued after this run (one new, one repeat raised). Weekly pass due 2026-11-18.
