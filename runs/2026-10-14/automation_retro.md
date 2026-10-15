# Automation retro, run 2026-10-14 (No.86)

## Weekly machine pass
Not due. `scripts/machine_due.py` reported: last pass 2026-10-11, 4 days ago, due at 7; 11 items queued, 0 repeat offenders. No `upgrade(2026-10-14)` commit exists.

## Standing repeat offender (trend_check --window 10)
Artwork craft and genuine detail was the weakest criterion 7 of 10 times, mean 6.98, last worked 2026-10-04. This run's art score is in score_report.json. It stays with the weekly pass.

## Fixed in this run because it broke in this run
- `scripts/ask_pack.py` (commit 318ede1d). The site build failed on the ask pack's 32,000 token ceiling after the day's ordinary docket refresh: 31,884 tokens on main, 32,108 with today's notes. Cause measured, not nudged: the refresh writes "Checked and unchanged." as a note's last sentence and the run collapse only matched notes that open with it, so 139 of 579 notes never collapsed. The matcher now also accepts the verdict as the closing sentence; the pack is 29,594 tokens with MAX_TOKENS untouched, and two self-test checks pin both directions.

## Deviations, phase by phase
- Phase 3.6, gas watch: FAIL at wake and at 07:55Z on 'recent calendar days' and 'source reading published'. CINGSA posted October 14th's reading at 16:00 Alaska, after the 22:21Z collection; the 04:40Z and 07:20Z slots had not started by 07:56Z and workflow_dispatch is 403. Incident filed (github). Repeat 11 of the standing owner item.
- Phase 7: three quarter-frame draws (akpost grade on 02, aksdf on 05, the akthree canvas on 09) until a 2x transform came first, and 09's object landed off frame until the camera matrices were updated before unproject. All caught by eye on the first render.
- Phase 7: 05's single-scene shark (depth bands inside the water SDF) took 38 s and posterised; a two-pass build (surface, then the shark alone, veiled and clipped) took 13 s. At full 1080 x 1350 internal the surface pass plus shark pass rendered in 30 s with no degrade, so the aksdf ready-cap item did not bite here.
- Phase 8: plan_drift_check read 'Agenda item C1' in a NOT USED row as claim C01 (queued). aggregate_check flagged a body that printed '3 years' twice as ambiguous; the slide was rewritten to 'since 2024', which C05 names.
- Phase 8: the reuse census put AKBENCH.relief on four frames; 04's teak was repainted per pixel so the bench sits on three.

## Queued today
- plan_drift: the claim regex reads an agenda code like 'item C1' as claim C01 (new).
- akbench: material edges are sampled once per device pixel with no antialiasing (new).
- gaswatch: evening collection slots land after the daily audit (repeat 11, owner decision).

## Upgrades this run
None (weekly pass not due). The ask pack fix above is a repair of what broke in this run, committed on its own.
