# Automation retro, run 2026-11-03 (carousel No.104)

## Trend check, top repeat offender

`trend_check.py --window 10`: Artwork craft and genuine detail was the weakest criterion on 6 of the last 10 runs (mean 7.26), last worked 2026-10-04, marked STALE. `machine_due.py` exit 1 (last weekly pass 2026-11-01, two days ago), so the weekly pass does not run today. The offender is QUEUED for that pass, and this run's evidence goes with it: the desk frames took four critic rounds because one shared 2D ground module was wrong in three ways at once (periodic walnut, saturated leather with no pool falloff, a pasted-rectangle blotter edge). Each was fixed once in `assets/js/akdesk.js`, not per frame, which is the doctrine's "fix the cause once" and is what the weekly pass should look for in the digest.

## Deviations, phase by phase

- Wake: `run_guard` defaults to the UTC date; the run woke at 21:04 AKST November 3rd, already November 4th in UTC, and was run against the Anchorage date by hand. No change (the routine says to use the Anchorage date).
- Phase 3.6: the Gas Watch audit found `late_post`; dispatching `gaswatch.yml` repaired it, but the first re-audit ran before Pages had deployed and read FAIL. A second audit after the Pages run passed. Showrunner timing, not a machine defect.
- Phase 3: one curl to eScribe with a browser user agent was refused by the auto-mode classifier as bot-check circumvention and was not retried. Correct outcome.
- Phase 6: the caption room reached its cap with both candidates rejected; the showrunner wrote the caption under the room's terms (caption_check PASS).
- Phase 7: `render.py --only-exact 3` is not valid syntax (`--only 3 --only-exact` is); a slide generator crashed on Python `%` formatting of CSS and moved to token replace. Both self-inflicted.
- Phase 8: four rounds. Round 1 all revise (4.5 to 6.5), round 2 all revise (6.0 to 7.0). The cross-frame causes were all in the new shared desk module (see trend check). Three contact declarations had to be moved because `contact_probe.py`'s horizontal axis proposed a "lit ground" rect on the object itself (06 the pencil's lit face, 07 the jacket's cover, 09 the brass lamp base). That class was fixed on 2026-10-11 for an object whose colour matches the sample just above the base; it still misses when the object's lit face differs from that sample.
- Phase 8: a `THREE.PCFShadowMap` trial with `shadow.radius` 10 to 12 to soften casts printed stepped bands along the cast edge; reverted to PCFSoft. akthree has no soft-shadow path that honours a radius without banding.
- Phase 8: `AKPOST.grade`'s grain at its documented `size: 2` was named as a regular lattice in near-black fields on 03, 04 and 09 by three critics; size 1 cured it.

## Queued for the weekly pass (knowledge/MACHINE_QUEUE.md)

1. contact_probe: the h-axis ground rect still lands on a lit object face whose colour differs from the base sample (No.104 06, 07, 09).
2. akthree: no soft shadow option; PCF with a radius bands, PCFSoft ignores the radius (No.104 01).
3. akpost: grade grain `size: 2` prints a lattice in near-black at 100 percent; make 1 the default or document it (No.104 03, 04, 09).
4. akdesk (new module): the 2D ground's blotter edges, pool falloff and walnut periodicity are now built in; a weekly pass may promote `pool` from an option to the default.

Weekly pass not due (49 items queued before this run). No machine upgrade commit this run.
