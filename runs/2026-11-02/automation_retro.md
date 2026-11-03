# Automation retro, run 2026-11-02 (No.103)

## Standing repeat offender

trend_check --window 10 names Artwork craft the weakest criterion on 6 of the last 10 runs (mean 7.26), last worked 2026-10-04. The weekly machine pass is not due today: machine_due.py says the last pass ran 2026-11-01, so the next is due at 7 days, and 46 items are queued with 0 repeat offenders. The offender is therefore queued for that pass, and this answer is the deferral. In-run, the deck met it with the CRAFT PLAN, two full pixel-review rounds on all nine frames and the craft floor cycle.

## Deviations, phase by phase

- Wake: bootstrap installed python playwright 1.64.1 (unpinned) against the pre-installed chromium-1243, and render failed to launch. It was pinned to 1.63.0 in-run. Queued in MACHINE_QUEUE (bootstrap should pin playwright to the image's chromium build).
- Phase 3.5 and 3.6: the ask pack crossed its 32,000-token hard ceiling once the docket grew, and the build went red. Fixed in-run: ask_pack.py keeps a one-entry history window for settled items (decided or closed), with measurements in its comment. The ask engine self-test also failed on a new agency (AEA) with no rule; an AGENCY_RULES entry was added. All browser suites pass. Both changes are logged in ledger/upgrades.json as fixes. A two-hop design for the pack is queued.
- Phase 7: machine QA first FAILED on fitText maxLines counting block spans. Every headline was converted to authored `<br>` lines (authored: true). It also failed on the contact declarations: an apostrophe inside a single-quoted data-contacts attribute, then the same defect in data-scale. qa.py's own message named the cause both times. The authoring habit is worth a lint at write time; queued.
- Phase 7: slide 05's planned column march came out blocky and from the wrong side, and was rebuilt as akthree terrain. Its key first sat behind the camera, which front-lit the range flat. A key behind the camera is a recurring way for a GPU terrain frame to lose its modelling. Queued as a helper warning in akthree.frame (warn when the key direction is within 60 degrees of the view direction).
- Phase 7: the sawn block's table plane z-fought the pool at distance, because near was 1 and far was 2400, so the pool rendered black on slide 09 only. Fixed by separating the planes and raising near to 3.
- Phase 8: all nine frames came back revise in round 1. The causes that recurred across frames were stair-stepped coasts on every map (fixed once, in SAWN.coastRings), largest objects painted flat (01, 09, 03, 05), and dead lower thirds (01, 03, 05, 09). These match the week's themes in the digest, so they go to the weekly pass as evidence.
- Copy: the copywriter flagged the caption's paraphrase "his complaint about DeepGreen" as broader than the mayor's quoted words. The showrunner tightened it and re-ran the caption gate.

## Upgrades this run

No weekly pass today. The machine changes were the in-run fixes above (ask_pack settled-history window, the AEA agency rule) and deck furniture (akblock veSea, the aksawn coast helpers, the grain tile at 640). All are logged in ledger/upgrades.json.
