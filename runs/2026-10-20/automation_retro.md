# Automation retro, run No.91 (2026-10-20)

The weekly machine pass is not due (machine_due.py: last pass 2026-10-17, due at 7 days, 0 repeat offenders). This run fixed what broke in it and queued the rest.

## Top repeat offender
Artwork craft and genuine detail again: 7.0 here, the weakest weighted shortfall, with the craft cycle stood down at the five-round cap. The evidence this run adds for the weekly pass (due 2026-10-24): the largest object read as least modelled on 04 and 05 through four critic rounds. Texture artifacts were named in every round: stair-stepped coasts at the DEM's cell size, specks, a tile-join seam, and a bump texture reading as cloth. A GPU breather was lit right but rendered in the wrong material and value.

## Deviations, phase by phase
- Phase 0: the run_guard default date was UTC 2026-10-21. Woke 22:05 AKDT, so the run used --run-date 2026-10-20, as prior runs have.
- Phase 3.6: the first live Gas Watch audit at 06:10Z found CINGSA's 16:35 Alaska reading of October 20th missing. A gaswatch.yml dispatch on main returned 204 (the last runs got 403), the collection ran, and the re-audit passed at 06:14Z. cron_health PASS, site sign-off PASS.
- Phase 3: claims were numbered Y01 and up. plan_drift's claim regex reads only C ids, so it could not look. FIXED IN RUN by renumbering the run's claims to C (house convention). Worth one line in the fact-checker's spec.
- Phase 6: the caption room returned "neither". One reassigned director wrote the winner, which passed caption_check at 887 characters.
- Phase 7: qa FAILed present-ink promises on frames whose inks were written per pixel (07, 08, 09 washes) or by WebGL (04). Fixed with legend chips, masked source-in fills, and label text in the inks. QUEUED for the GPU case.
- Phase 7: putImageData over a transparent desk punched a hole through the background on 05, which the critic saw as a seam. FIXED IN RUN (offscreen layer plus drawImage).
- Phase 8: four pixel rounds plus a flow round. A seam on 05 that survived two render-side fixes was a terrain-tile join at 60.0 N in ak-ykdelta-dem. Repaired at load in the slide. QUEUED for the asset.
- Phase 8: critics again could not find the thumbs (slide-NN-thumb.png). QUEUED: the critic_brief item's repeat was raised to 1.
- Phase 10: scored 8.44 (threshold 7.7), art 7.0. The craft cycle stood down at the five-round cap.
- Phase 11: site built at 2026-10-20 (main had no newer docs build). No subscriber alert was due. prune_runs freed 2.32M from 2026-09-20.

## Queued in knowledge/MACHINE_QUEUE.md
1. qa ink law: a GPU frame can't keep a present-ink promise.
2. assets: repair ak-ykdelta-dem's 60 N tile join at the source and scan the other DEMs.
3. critic_brief thumb path, repeat raised to 1.
4. gaswatch evening slots, repeat raised to 14 (this run's dispatch worked).

No upgrade commit this run; the pass is weekly.
