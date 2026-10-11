# Automation retro, run 2026-10-12 (No.85)

## Weekly machine pass
Not due. `scripts/machine_due.py --date 2026-10-12` exited 1: last pass 2026-10-11, 1 day ago, due at 7; 11 items now queued. Steps 2 to 4 don't run today, and no `upgrade(2026-10-12)` commit exists.

## Standing repeat offender (trend_check --window 10)
Artwork craft and genuine detail was the weakest criterion 7 of 10 times, mean 6.93, last worked 2026-10-04. This run scored it 7.0, so the trend continues. It is queued for the weekly pass, not worked today. The pass should take it up with this run's two machine-level causes: the aksdf ready cap below, and the largest object on frames 02, 03 and 04 still reading least modelled after five rounds.

## Deviations, phase by phase
- Wake through directors room: no deviations.
- Phase 3.6, gas watch: WARN at 06:19Z, FAIL at 08:12Z on 'source reading published'. CINGSA posted October 10th's reading at 20:47 Alaska, after the 22:39Z collection. The 04:40Z and 07:20Z schedule slots had not started by 08:47Z, and workflow_dispatch via the GitHub MCP returned 403 twice. Incident filed (blocker github). Queue item raised to repeat 10. Only the owner can fix it (schedules or Actions credentials).
- Phase 7: slide 09 shipped one page error (`-x ** 2` precedence) and one undefined rng after a refactor. render.py caught both, and both were fixed.
- Phase 8: qa.py caught three real defects the eye had passed:
  - a painted screen pool over 02's declared contact;
  - two of 03's 112 discs too faint to count;
  - 03's undeclared '22 legislative candidates' aggregate after a copy cut.
  All three gates worked as designed.
- Phase 8: aksdf on 07 ran 29 to 30 s, against render.py's 30 s renderReady cap, at 1080 x 790 internal. A distance-only shadowScene cut the march to 19 s. Native resolution (about 60 s) can't fit, and critics named the stair-stepping in every round. QUEUED as a new item (render/aksdf ready budget).
- Phase 10: the scorer again noted that the rubric weights sum to 1.10, so 8.62 is 7.84 normalised. This is the existing queue item (2026-10-11), not re-raised.
- Phase 11: prune_runs freed 0.56 MB from runs/2026-09-10, as designed.

## Queued today
- render/aksdf: the 30 s ready cap holds an aksdf still life below native resolution (new).
- gaswatch: evening collection slots land after the daily audit (repeat 10, owner decision).

## Upgrades this run
None (weekly pass not due).
