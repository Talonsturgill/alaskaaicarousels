# Automation retro, run No.88 (2026-10-16)

## Trend check (window 10)
Top repeat offender in machine QA: contact shadow warns (4 of 10 runs, latest 2026-10-15). Stale weakest criteria: Variety vs ledger (worked 53 runs ago) and Thumb-stop cover (39 runs ago). Today is a weekly pass day (machine_due.py exit 0), so the upgrade engineer works the week's themes, the digest's counts first; this retro hands it today's deviations.

## Deviations, phase by phase
- Phase 0 bootstrap: pip ReadTimeout on first try; rerun passed. Environment, no change.
- Phase 2 research: aws.state.ak.us, af.mil and AOGCC answer 403; the run used akleg BASIS documents, the Federal Register API and press. BASIS PDFs extract one word per line through fetch_pdf_text; whitespace normalised by hand.
- Phase 2/3 agents: one hand-back was saved as {"message": "<json>"} by the run's own extract script and unwrapped by hand. Showrunner tooling, no machine change.
- Phase 3.6 Gas Watch: live audit FAIL at wake and on every re-audit (06:19Z, 06:46Z, 07:41Z, 08:2xZ) on CINGSA's 17:11 Alaska reading of October 16th, posted after the 22:07Z collection; no scheduled slot has run since; workflow_dispatch from this session is 403. The audit PASSED at 08:59Z once GitHub ran a late slot (last run 0.2 hours before), so no incident was filed. Same signature as the escalated queue item (repeat raised to 13). Owner decision only.
- Phase 7 build: the akengrave form collapsed into ribbons on near-level muskeg until the form rode a tilted plane with even seeding; the DEM tile carried +-32767 spikes repaired by median. Local fixes.
- Phase 8 pixel round 1, THE MATERIAL ONE: the wordmark, counter and alaskaaihq.com fixture were absent from the pixels on all nine frames. They were in the DOM, appended after the z-index 1 art canvas with no z-index of their own, so they painted under it. render.py, qa.py and copy_sync_check all read the DOM and passed; five independent pixel critics each caught it. Fixed in assets/js/akdocket.js (z-index 9). The gate gap is queued for today's weekly pass: a text node whose box is covered by a canvas should FAIL.
- Phase 8 round 1, recurring art cause: five of nine frames (02, 03, 05, 06, 08) set a plate on a near-black desk (L* about 5 to 7), so the plate's cast and bevel had nothing to darken and the plate read as printed or floating. qa's contact gate only measures declared contacts, and only 06 declared one. Fixed per frame with a lit desk pool under each plate. Queued.
- Phase 8 round 1: a comment typed inside an argument list in akhearing.js broke two module renders ("missing ) after argument list"); the run's own node --check skipped type="module" scripts. Caught on render; no machine change beyond a note.
- Phase 8: render.py --only 1,4,6,9 also re-rendered slide 07. Harmless, unexplained; not queued until it bites again.

## Queue
Two new items queued in knowledge/MACHINE_QUEUE.md (fixture occlusion, dark-ground casts); the gas watch item raised to repeat 13.

## Weekly pass
Ran today (machine_due.py exit 0). The upgrade engineer worked the week's digest and today's deviations under prompts/machine_weekly.md and shipped five fixes as upgrade(2026-10-16), commit 868297b1, with the SHA recorded in 0cd7e2b2:
1. engine: render.py reads the pixel of every canvas stacked above each text line box, fixtures included, and qa.py FAILs a reading line half covered or a fixture 90 percent covered (tests/canvas_over_text_verify.py; today's nine frames with the pre-fix akdocket.js FAIL 27 times).
2. tonal_arc_check: two new WARNs, one tone under a spike and a tied peak (never a FAIL).
3. dossier_check WARNs a dossier that promises a cast with no data-contacts; DESIGN_DOCTRINE section 3 names a plate on a near-black desk as a default to avoid.
4. plan_drift_check takes claim ids only from a claims index row's leading token.
5. contact_probe: a neutral object sample matches on full-weight L*, so the false "object's own colour" note stops.
Frontier scan focus (b), dark-ground still life; the deck-level light chart is parked in FIELD_NOTES. Queue: four items shipped, the Gas Watch item stays escalated at repeat 13, the docket pre-ship landscape check (repeat 2) makes the pass due again tomorrow. Top repeat offender (contact shadow warns, 4 of 10 runs) was worked through item 3 and today's lit desk pools.
Every new check was re-run by the showrunner before the commit: all five verifies HOLD or PASS.
