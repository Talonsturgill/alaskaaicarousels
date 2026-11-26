# AUTOMATION RETRO, run No.124, 2026-11-25

## Standing repeat offender
trend_check --window 10 still names Artwork craft and genuine detail as the weakest criterion. The weekly pass is NOT due (machine_due: last pass 2026-11-24, due at 7 days, 0 repeat offenders), so this run fixes only what broke in it and queues the rest.

## Deviations, phase by phase (with evidence)
- Wake: CLAUDE_EFFORT read `medium` although .claude/settings.json sets effortLevel high. Recorded in run_state.json; nothing in the repo can force it.
- Research: the story came from scouts plus the AIDEA schedule page (meeting recessed to Friday, November 27th). The fact-checker verified 60 claims, 17 primary, 12 fetches over 11 URLs.
- Geodata: overpass-api.de refused the container; the rail ways came from the OSM editing API in small bboxes and were stitched by hand. The z12 terrarium DEM carried needles and black holes over tidal water and muskeg; three cleaning passes (neighbourhood water vote, 30 m despike, lowland despike) plus an in-slide 15x15 median cap were needed before the cover rendered clean. Both queued in MACHINE_QUEUE.md.
- Art build: qa FAILs on leaders not landing (01), labels crossed by art (01, 05) and an OSM credit colliding with a label (03), each fixed in one pass. bespoke drawn share dipped to 45 percent once and was restored by stroking thin fillRects.
- Pixel review round 1: all nine frames revise (5.4 to 6.6). Flow review round 2: revise 7.0; bodies on 02 and 07 cut, 08 warmed, 09 given a real-place ground.
- Scoring: round 2 scored 8.275 against 8.3 with art 7.0, so the CRAFT FLOOR cycle (round 3) rebuilt 07's camera and ground, cleaned 01's terrain, straightened 02's hachures, re-seeded 04's engraving and re-routed 09 to the true bearing.
- Phase 3.6: cron health PASS (7 workflows), gas watch live PASS, site sign-off PASS (191 pages), page check PASS; nothing to repair.

## Queued (not fixed this run)
- scripts/dem_fetch.py for terrarium corridor DEMs with the water clean and despike as flags.
- an OSM API fetch-and-stitch helper for when overpass is refused.
