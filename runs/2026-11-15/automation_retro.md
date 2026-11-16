# Automation retro, 2026-11-15 (No.116)

## Top repeat offender (trend_check --window 10)
Artwork craft has been the weakest criterion on 8 of the last 10 runs (mean 7.1). It is QUEUED for the weekly pass.
`machine_due.py` says the pass isn't due yet: the last one ran on 2026-11-11, and the next is due 2026-11-18.
This run spent its fourth revision round on the CRAFT FLOOR cycle (frames 3, 8, 1 and 5). Art rose from 6.5 to 7.0, and the
result is recorded in score_report.craft_cycle for the weekly digest.

## Deviations, phase by phase
- Wake: CLAUDE_EFFORT read `medium` although `.claude/settings.json` carries `effortLevel: high`.
  This is recorded in run_state and the email. It is a routine-trigger setting and is out of this repo's reach.
- Phase 3.6 Gas Watch: the live audit was WARN with late_post. I dispatched gaswatch.yml again (run 43815033214), Pages deployed
  and the re-audit read PASS. Cron health was PASS on 7 workflows and site sign-off was PASS on 181 pages.
- Phase 8 render: real-DEM akthree scenes rendered black terrain until `R.camera.far` was raised from the
  default 200 to 8000. This is the same family as the 2026-10-25 shipped far-plane item, but here the
  symptom is clipping, not a wedge. Queued as a new item.
- Phase 8 render: DEM edge-clamp streaks showed on 04, 05 and 09, and a lit 141st-meridian wall showed on 01 and 08. Fixed per slide
  with footprint masks and the state outline. Slide-authoring slips.
- Craft cycle: softening 03's shadow left its declared contact stale (dL -0.4). qa.py caught it, and a
  contact_probe re-read at the flange foot fixed it. The machine worked as designed.
- Scoring: the scorer's report card carries no `passes` key, so gate_status's score row read
  `passes=None` and FAILED on a passing score. The showrunner added `passes` derived from
  weighted_total >= threshold with no hard fails. Queued as a new item: the scorer agent definition or gate_status
  should derive this rather than trust a key the agent doesn't emit.
- Craft cycle regression: the cover's added Gulf glint was named a spotlight beam by the cycle-2
  scorer and was reverted after scoring.

## Upgrades
No upgrades. The weekly pass isn't due.

## Queue
Two new items queued.
