# AUTOMATION RETRO, 2026-11-04 (No.105)

## Standing repeat offender (trend_check --window 10)
Artwork craft and genuine detail was the weakest criterion in 6 of 10 runs (mean 7.18). Today's pass is not a
weekly pass (machine_due exit 1, last pass 2026-11-01), so the offender is QUEUED for the November 8th pass and this
run attacked it in the plan instead: one object per frame, each the most modelled thing on it, no shared 2D ground
module, every per-pixel field at the device pixel, and the masterful depth frame (01) built first.

## Deviations, phase by phase
- Phase 0: run_guard defaults to the UTC date (2026-11-05) while the routine's run date is the Anchorage date
  (2026-11-04). The run passed `--run-date 2026-11-04` by hand. Queued.
- Phase 0: bootstrap reinstalled python playwright and broke a direct `chromium.launch()` (it now wants
  chromium_headless_shell-1248 while the image ships 1243). render.py survives because it globs /opt/pw-browsers;
  a showrunner script for site screenshots failed until given executable_path. Existing queue item raised to repeat 1.
- Phase 3.6: Gas Watch LIVE FAILED on a late post (CINGSA posted at 03:37Z after the 00:25Z collection). Dispatched
  gaswatch.yml on main (run 41978585382, success), re-audit PASS. The diagnosis line named the remedy exactly.
- Phase 3.5: the staleness worklist deferred 11 items past the default budget of 6 on consecutive days; the run
  raised --budget to 17 and refreshed every live item. aws.state.ak.us rejected two of seventeen fetches with a WAF
  page (HTTP 200 body "Request Rejected"), recorded as could-not-re-read.
- Phase 3.5: the ask payload headroom is 4,781 bytes, under the 5,000 the routine asks to flag. Flagged here.
- Phase 7: dossier_check failed every 4a under 200 characters on the first pass (one sentence each); cheap, fixed
  in one edit. qa.py's single FAIL was an ink-law promise on 05 made by putImageData pixels, which the brush census
  can't see; a DOM legend ramp carried the ink and is also better for readers.
- Phase 7: the "plate on a near-black desk" default recurred on 02, 04 and 07 (grounds under L* 10); the
  contact probe caught all three before the critics.

- Phase 8: four per-slide rounds (the cap). Three repairs took two rounds each because the first fix treated the
  symptom: the 05 slab (a cast gated to d > 0), the 03 arrows (positions re-derived from builder constants, not the
  motors' world positions), the 07 dome (too little slope to shade). Each is queued with its measurement.
- Phase 8: the tonal arc's declared peak (07) measured fourth; re-declared to 03 with the reason in the reconciliation
  and 03's exposure lifted 0.2 so the peak no longer tied with 01.
- Phase 8: render.py widened `--only` to stale slides when the shared akdrone.js changed, which re-rendered 01 and 09
  correctly; no action needed, noted because it doubled two render passes.

- Phase 10: the scorer found config/scoring_rubric.yaml's weights sum to 1.10. Verified (0.14+0.14+0.16+0.14+0.12+0.10+0.08+0.07+0.05+0.10). Every past total carries it. Not changed here: altering weights or thresholds changes what ships and is the owner's call. Queued as an OWNER DECISION item and named in the draft.

## Upgrades
None this run (weekly pass not due). New module `assets/js/akdrone.js` (FPV quad builder with an explode helper)
ships as deck work, documented in TECHNIQUE_LIBRARY.

## Queued for the weekly pass
Three new items dated 2026-11-04 in knowledge/MACHINE_QUEUE.md (continuous offset casts, overlays anchored to world positions, dome slope), and three repeats raised: run_guard UTC default (now 4), the unpinned python playwright (now 1), aws.state.ak.us refusals (now 1). machine_due exit 1: 55 items queued, the pass is weekly (next due November 8th).
