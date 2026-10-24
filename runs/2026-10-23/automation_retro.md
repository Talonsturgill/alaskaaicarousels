# Automation retro, run No.94 (2026-10-23)

## Trend check (window 10)
Top repeat offender: Artwork craft and genuine detail, weakest in 7 of the last 10 scored runs (mean 7.1). The weekly pass is not due today (machine_due: last pass 2026-10-21, due at 7 days), so it is queued for that pass, which is the stated answer for a non-pass day. This run attacked it inside the deck instead: one best-modelled object per frame, nine different mark-making systems, and every frame through at least three critic rounds. What the round record says about the offender is below.

## Deviations, phase by phase
- Wake: bootstrap.sh warned "no chromium found" on a container whose browser is at chrome-linux64; render.py's own fallback found it. False warning (queued).
- Research: scout E ran 27 searches against a cap of 25; 149 searches in all.
- Claims: the FNSB agenda packet is a 339 MB PDF that WebFetch can't pass; the showrunner pulled it with curl, extracted the ordinance with pypdf, and the fact-checker verified against the extract. The borough GIS layer gave the acreage claims C63 to C69 as primary data (route added to config/sources.yaml).
- Docket: the worklist deferred six items past --budget 6 for the second day running; --budget 12 covered all twelve. State notice host answered 503 then 200; KPBSD egov 503 all day.
- Gas Watch (Phase 3.6): gaswatch.yml exited 5 by design on a CINGSA cell reading "0]" and the live audit found the 16:00 posting unpublished. Repaired by a production workflow_dispatch on main; both audits PASS after. No code change.
- Art build: a prototype's async renderReady IIFE was never invoked and rendered blank with OK and 0 errors (queued). AKSTIPPLE.field's box arity ([x0,y0,x1,y1], not [x,y,w,h]) drew slide 08's borough empty with no error (queued). akvalley is hard-wired to the Nenana DEM, so slide 04's ridgeline stack was re-implemented inline, and two critic rounds went to defects akvalley had already solved (queued).
- Copy: the copywriter queried three attributions (industrial zones by inference, "first alert was a Level 2", the October 27th session); all three were corrected in caption and slides before the critics' second round.
- Pixel review: round 1 was nine of nine revise (6.2 to 7.9). Recurring causes, counted: texture or seam artifacts on 8 frames (sky seams on 01, 03, 04; a tiled detail lattice on 01 and 06; stipple box on 08; march bands on 05); largest object not best modelled on 4 (03, 04, 05, 07). Round 2 shipped 06, 08, 09. Rounds 3 and 4 worked the rest; the per-slide cap ended review with 01 to 05 and 07 fixed again but not re-reviewed.
- Shared furniture: one periodic texture tile in akborough.terrain printed as a lattice across two frames; fixed once in the helper (two non-commensurate rotated layers), which is the "fix the idiom, not the instance" rule working.

## Queued for the weekly pass (knowledge/MACHINE_QUEUE.md)
Five new items dated 2026-10-23: akstipple box arity warn; akvalley DEM adapter; renderReady-is-a-function warn; bootstrap chromium glob; an explicit-cast mode for akbench at low keys. None repeats an open item.

## Fixed in this run
Only the deck's own furniture (assets/js/akborough.js, committed as wip). No machine file was changed.
