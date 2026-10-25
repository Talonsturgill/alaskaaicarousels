# AUTOMATION RETRO, 2026-10-24 (No.95), notes taken during the run

## Deviations so far
- Wake: the Bash auto-mode classifier returned no verdict for about ten minutes (06:05Z to 06:15Z)
  and again briefly near 06:25Z and 06:33Z. Read and Write (allowlisted out/ paths) kept working, so
  the run read the knowledge base and wrote run_state.json and plan.md meanwhile. Not a repo defect;
  harness side. No permission prompt was raised.
- bootstrap.sh "no chromium found" again (MACHINE_QUEUE item raised to repeat 1).
- run_guard.py with no argument reads the UTC date (2026-10-25); the routine's run date is the
  Anchorage date (2026-10-24). Passing --run-date fixed it; the docstring says "(today, UTC)". Worth a
  queue line if it bites again: a late-evening Anchorage wake always sees tomorrow's UTC date.
- Gas Watch live audit FAILed at 06:15Z on CINGSA's 19:10 Alaska reading (the standing evening-slot
  item, repeat 14 and escalated). workflow_dispatch on main returned 204 this time, the collector ran
  and the re-audit PASSED at about 06:20Z. Logged on the escalated item's evidence at the retro.
- docket_staleness deferred 9 past the budget of 6; the run raised its own coverage to 10.

## Art and review (Phases 7 to 10)
- Helper: a deck helper (assets/js/akkachemak.js) carried the fixtures, the DEM loader, the camera, the per-pixel field, the cloud field and the column-marched terrain. Fixed in-run: the terrain march printed comb teeth on crests (now two columns per device px plus a horizontal three-tap filter); a full-frame grain canvas broke qa's canvas-over-text measurement on all nine frames (grain is back on a DOM layer, 540 px tile).
- Five rounds used: three per-slide rounds, one flow round (04's headline to its own takeaway, 08's dusk afterglow, 05's shaft into the left field), one craft cycle (04, 07, 02, 05, 01).
- 04, the planned depth frame, was weakest all run. Root cause written up as a queue item: the dossier promised a reflection the lens geometry can't give. Seven fallstreaks became countable only when painted in 2D, evenly spaced, densest in front of the lit snow. A neighbour-max despike flattened real summits; a median test caught the one bad DEM cell.
- 07's all-sky disc shipped first with ground-map handedness (E left of S-at-top); the scorer caught it and the craft cycle mirrored it. The skyline is drawn three times true and the readout says SKYLINE x3.
- Declined on measurement: the critics' 'dot lattice' on near-black frames (no autocorrelation period, grain std 1.5 levels).
- Selection missed prior coverage (No.64, 34 days earlier) because the dedupe looked back 30 days and not the ledger's 90. Reframed the hook as an update; queued a scripted dedupe.

## Queued this run (knowledge/MACHINE_QUEUE.md)
- selection dedupe over the _spec's 90 days (new); critic texture claims without a measurement (new); dossier lens arithmetic for the lower third (new); run_guard's UTC default (new); gaswatch evening slot raised to repeat 15; bootstrap chromium glob raised to repeat 1 at wake.
- Weekly pass not due (last 2026-10-21, 4 days ago).
