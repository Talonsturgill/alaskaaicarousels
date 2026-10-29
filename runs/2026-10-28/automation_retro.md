# Automation retro, run 2026-10-28 (No.98)

## Trend check, and what this run does with the top offender

`trend_check.py --window 10`: Artwork craft and genuine detail was the weakest criterion in 7 of the last 10 runs (mean 7.21), last worked 2026-10-04 per the text match. The weekly machine pass is not due (`machine_due.py`: last pass 2026-10-25, due at 7 days; 34 items queued, 0 repeat offenders), so the offender is QUEUED for the next weekly pass rather than worked here. This run's own answer to it was in-run craft: one full critic round across all nine frames, each fix aimed at the plan's named craft causes (b largest object, c lower third, d texture), before scoring.

Defect classes that kept shipping, for the weekly pass to weigh: busy art under text (6 runs), outside safe zone (4), ragged display line (4), art touching glyphs (3), top-loaded composition (3), contact shadow (2). This run met four of them in its first qa pass (ragged lines on 03, 04, 05; top-loaded 06; contact on 01; glyph ring on 01, a false positive both critics confirmed).

## Deviations, phase by phase, with evidence

1. Wake. `run_guard` defaults to the UTC date; the run is dated by Anchorage (2026-10-28) and needed `--run-date`. Known, not new.
2. Gas Watch live audit FAILED at first read: the scheduled collection had run before CINGSA published the October 28th 16:00 reading. Repaired by dispatching `gaswatch.yml` on main; live audit PASS afterwards. A timing race between the cron and the source, not a defect in the collector.
3. Federal Register API stopped answering this container after a few calls (IP rate block). Worked around with other sources. Environment, not machine.
4. Docket pre-flight failed twice: the ask payload went 3,141 bytes over its ceiling once two AIDEA items were added, and the agency vocabulary had no AIDEA rule. Fixed in this run by shipping catalogue routes as row positions (headroom 13,845 bytes) and adding the agency rule, with self-test and browser-suite coverage. The ceiling held as a hard gate, which is what it is for.
5. Copy. The copywriter caught four factual problems in slide strings that every machine gate had passed: kickers and the document title implying the AIDEA board voted on the NuCube stake (the record shows no board resolution for it), "four cables" where the resolution counts subsea systems only, "$9.25 PAID" for a purchase that closes with the merger, and "FULL COST FUNDED" for committed money. All four came from the storyboard, so `plan_drift_check` could never see them. Queued: a claims-to-kicker check is not boundable; the defence that worked was the copywriter reading claims.json notes.
6. Aggregates. `aggregate_check` caught "ONE DAY" as an undeclarable duration; the kicker was rewritten to a date rather than declared as design.
7. Pixel review. Round 1 returned revise on all nine frames (scores 6.4 to 7.6). Recurring causes: largest object under-modelled (05 block, 06 steel, 07 paper, 08 plaque), lower third under-carried (01, 05, 06), texture artifacts (02 lip stub, 03 hard drop shadow, 06 horizon seam, 07 hard rectangle, 08 stair-stepped screen, 09 grid-quantized dropout). These are the same three causes the weekly digest has named since September 27th.

## Queued for the weekly pass (knowledge/MACHINE_QUEUE.md)

- A rotated halftone screen clipped by an axis-aligned rectangle stair-steps at its edge (08). A helper that feathers dot radius to zero at a mask, or a crisp bevel drawn over the edge, would remove a whole class.
- akthree floors: the fog colour and floor size seam (06), queued.
- Per-cell random dropout on ring engravings reads as a mosaic (09). Arc-length runs are the fix; worth a TECHNIQUE_LIBRARY note.

Queued today: three items (the fog and floor seam, metals reflecting a dark environment floor, the halftone edge and ring dropout cures). The weekly pass is not due (last 2026-10-25), so nothing else changes in the machine this run.
