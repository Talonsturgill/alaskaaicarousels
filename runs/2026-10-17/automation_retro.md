# Automation retro, No.89, 2026-10-17

Today was a weekly pass day (`scripts/machine_due.py`: DUE, one repeat offender queued). The upgrade engineer ran the pass under `prompts/machine_weekly.md`, landing commits 50f11925 and SHA follow-up 5693ce02. Its full report is summarized under "Weekly pass" below.

## Trend check, the standing repeat offender

`trend_check.py --window 10` names Artwork craft as the weakest criterion on 5 of the last 7 runs (mean 6.93). It was worked today, on two fronts.

- **In the run.** Four pixel rounds took every frame from 6.0 to 7.6 in round 1 up to 7.0 to 8.4 in round 4. Seven of nine frames shipped a "ship" verdict.
- **In the weekly pass.** It fixed two machine causes:
  - the thin-lens focal region (cause b, the largest object least modelled);
  - technique 126 (cause d, beaded strokes).

## Deviations this run, with evidence

1. **Round 1: the same four causes on most frames.** The critics' round 1 verdicts named four causes across frames:
   - a soft largest object on both akthree relief frames (01, 09), from AKSTROBE.focus at k 5 to 7;
   - near-black clipped lee and cast (01, 09);
   - rectangular type veils with hard edges over lit land (03, 04, 05, 08);
   - round-capped translucent strokes beading at every joint (04 vortex, 07 swell).

   Fixed in the run, and the weekly pass made the first and last into machinery: AKSTROBE `o.sharp` and depthRange, and TECHNIQUE_LIBRARY 126.
2. **The 01 coast stayed soft at k 2.** The cause was mesh and mask resolution, not focus. NX 560 with a 9 px mask blur smeared the coast. 900 x 840 with a 5 px blur cured it. A shadow normalBias of 0.03 combed the steep bevel walls with acne, fixed at 0.09.
3. **A critic dropped a slide.** The critic assigned 07 and 08 returned 07 only, so 08 went unreviewed for a round. Fixed by the weekly pass: one object per assigned slide, plus a coverage check.
4. **A shared asset changed under the live renders.** The upgrade engineer edited the shared `assets/js/akstrobe.js` while the run was rendering. qa.py's stale-render gate caught it, and slides 01, 05 and 09 were re-rendered. The change is byte-identical without `o.sharp`, so nothing moved. Lesson: a concurrent weekly pass that edits shared assets forces a re-render; the stale gate is what makes that safe.
5. **lighten composite tripped about 20 WARNs.** qa.py's "a layer of light ends in mid-air" WARN fired about 20 times on 07's opaque ribbon layer under a `lighten` composite. Switched to source-over. Queued by the pass for measurement (WARN-only).
6. **Two land masks failed in their own ways.**
   - Slide 02: a geoEquirectangular mask with a hand-solved translate was wrong. A plain geoTransform is exact for a window this far from the antimeridian.
   - Slide 08: the mask and the swath construction needed per-pixel latitude fades. A great circle sampled from l = -180 starts mid-Arctic, so it has to start at its southern end.
7. **Gas Watch live FAIL: the 04:40Z collection never started.** The "source reading published" check fails because the 04:40Z scheduled collection had not started more than four hours after its slot. workflow_dispatch from the session returns 403 (Resource not accessible by integration). This is the escalated evening-slot item (repeat 13), which is the owner's decision on schedules and credentials.
8. **The published docket map fails iPhone 13 landscape at the run date.** The weekly pass found it. CI's `mobile` job builds at a fixed 2026-07-25, so it stays green. Repaired in this run's Phase 3.6 as presentation; see the docket section of the draft. The CI date change is queued to ride with the repair.

## Weekly pass (upgrade-engineer)

- **Five changes, all verified.** See ledger/upgrades.json for each entry.
  1. Docket map pre-flight at the run date (browser_suites, Phase 3.5 step 5).
  2. gate_status's gas_watch_live holds incident records to CI's `audit_checked_utc` rule.
  3. Per-slide critic returns.
  4. AKSTROBE.focus focal region and AKSTROBE.depthRange.
  5. TECHNIQUE_LIBRARY 126: stroke opacity, not dab flow.
- **Deferred.**
  - Dead or eventless region (cause c): seven different fixes on seven frames, with no shared cause.
  - Variety vs ledger: weakest on 2 of 7 runs, with no machine cause named.
- **Escalated.**
  - The Gas Watch evening slots, for the owner.
  - CI's docket map date: it rides with the map repair.
- **Frontier scan:** focus (c), translucent variable-width strokes. Applied as technique 126.

## Queued

The pass updated knowledge/MACHINE_QUEUE.md: four items closed, two added. Nothing else from this run is queued.
