# Automation retro, run 2026-10-09 (No.82)

Weekly machine pass: RAN. machine_due.py read NOT due at first (exit 1, last pass 2026-10-06); raising the critic-crop item to repeat 2 in this run's queue update made it DUE (exit 0), so the upgrade engineer ran the week's pass here, before the merge, on week_digest.md.

## Top repeat offender (trend_check --window 10)
Artwork craft and genuine detail, weakest in 7 of the last 10 runs (mean 7.18), last worked 2026-10-04. Worked in this run's weekly pass (native 100 percent crops for the critics, the akthree material audit and glass helper, the 11a region check); deferred causes c, a and e are explained below. This run also adds three measured lessons in ledger/instincts.json and FIELD_NOTES (glass albedo and shadows in akthree, heap versus cone shading, depth normalised across the object), each a candidate for a helper default rather than prose.

## Deviations, phase by phase
- Phase 3.6, Gas Watch live audit FAIL all run on the October 7th evening reading: GitHub had not dispatched the 04:40Z or 07:20Z gaswatch.yml slots (last scheduled run 23:36Z), and workflow_dispatch from the routine returned 403 again. The incident is filed (gaswatch_incident.json, blocker github) and the gate reads WARN. Owner-only item, already escalated; repeat raised.
- Phase 3.5/site: browser_suites ask_engine E5 disagrees when the site is built for a run date two days ahead of Anchorage (the AIDEA Houston October 8th hearing). Queued.
- Phase 8: four per-slide rounds. Round 1 to 3 regressions came from fixes that traded one defect for another (02's glass went from milk to invisible; 01's interior from flat to blotchy). Both were measurement problems: the milk was the glass's diffuse term, found by measuring the broth region with and without each mesh.
- Phase 8: the storyboard's 11a rects drifted from the slides' data-encodes on five frames while dossier_check and plan_drift_check passed; a critic reads the storyboard's rects. Queued as a plan_drift extension.
- Phase 8: critics again could not crop to 100 percent (every report says so). Repeat raised.
- Phase 8: akthree metal read matte under the low global environment intensity (02's headplate) until its envMapIntensity was raised to 2.8; same class as the open 2026-10-07 akthree item. Repeat raised.

## Upgrades (weekly pass, five, logged in ledger/upgrades.json)
1. fix, engine: render.py cuts every frame into six native 1080 x 900 tiles for the pixel critic (cause d, 4 of 6 runs; queue repeat 2). critic_brief lists them; the critic must read them.
2. fix, assets: AKT.mat.glass() and AKT.audit(); qa.py WARNs on an under-lit metal and on glass that casts a shadow or reads as milk (cause b on 3D frames; No.80 and No.82).
3. fix, engine: span-per-line headings recorded as text_composites so copy_sync finds them (queue repeat 1).
4. fix, scripts: plan_drift_check FAILs when a dossier's 11a rects differ from the slide's data-encodes (No.82, five frames).
5. improvement, assets: AK.fitText authored mode, a re-implementation of CSS text-fit shrink consistent (the engine's Chromium 141 lacks it).
Verified in this run: critic_brief, plan_drift self-tests, akthree audit 10/10, supersample 4/4, span heading 6/6, fittext authored 6/6, copy_sync shred, line_text, wrap_drift all pass; today's nine slides and the demo deck render byte-identical before and after (sha1); gate_status --require 0 FAIL.

## Deferred, with the condition to take them
- c, dead regions: three pixel probes measured null on 2026-10-04; the critic's frame_causes c stays the live check.
- a, reuse across frames, and e, tonal arc: their censuses have under two weeks of record; take them when two weeks of output can be checked against the critic's labels.
- noise2 alias (first next pass), axis census, 24 px label floor, contact_probe ground rect, site_build Anchorage today, docket payload (touches site_build, live this run).
- Escalated, owner only: Gas Watch evening slots (repeat 8).
