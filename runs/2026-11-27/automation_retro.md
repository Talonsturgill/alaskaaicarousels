# Automation retro, 2026-11-27 (No.126)

Weekly machine pass: NOT due (machine_due.py exit 1; last pass 2026-11-24). Zero upgrades shipped today; items queued below.

## trend_check top repeat offender
Artwork craft and genuine detail, weakest on 7 of the last 10 runs (mean 7.08). Deferred to the weekly pass (due 2026-12-01, or 2026-11-28 now that a queued item reached repeat 2). This run attacked it in the plan (fewer, larger objects; lit ground; art routed around type) and in round 1 with a deck-level snow micro-normal, which overshot into stripes at first and had to be cut to a 0.12 normal scale.

## Deviations, phase by phase
- Wake: CLAUDE_EFFORT read medium, not the settings' high. Recorded in plan.md and the editor notes; the settings file was not changed (permissions and effort are not this run's to edit without evidence of why it did not take).
- Research: all six beats thin (Thanksgiving week). Beat B and E returned no in-window story.
- Gas Watch: live audit WARN late_post at wake; dispatched gaswatch.yml on main (run 46115370606, success). The first re-audit reported collected_after_post while Pages had not redeployed; one minute later PASS. Queue item raised to repeat 2.
- Directors room: the container restarted while three directors were running; their hand-backs were recovered from the subagent transcripts on disk. No work lost, no respawn.
- Art build: AKPOST.field refused a 64 x 1 lattice (queued). A grade on an identity transform was caught by the AK CONTRACT console error and fixed with setTransform(2,...). A data-contacts apostrophe broke the JSON once (qa caught it).
- Aggregate gate: the detector read "0.15 PROPOSAL COVERS" across a line break as a count; the note was reordered, then removed in round 2.
- Fetch counts (SOURCE FETCH SCOPE): fact-checker 12 WebFetch calls over 9 distinct URLs; repeats were the 116,145-character notice tail (offset), one narrow Table 5 re-read, and one offset read of the 512,825-character October rule. Counts, not a token bill.

## Queued (knowledge/MACHINE_QUEUE.md)
- akpost: AKPOST.field on a one-row lattice (new, repeat 0).
- gaswatch_health: collected_after_post during a Pages deploy lag (raised to repeat 2).

## Weekly machine pass (run later the same day, 2026-11-27; machine_due exit 0 on queue item 2026-11-18 at repeat 2)
The note above said "not due" before the queue item reached repeat 2. The pass ran on the week digest (6 runs; flow causes b 4 runs/6 frames, d 4/9, c 3/5). Three changes, staged for the `upgrade(2026-11-27):` commit:
1. TOP REPEAT OFFENDER, FIXED: gaswatch_health's timing diagnosis. Root cause: it compared a run's START against CINGSA's stamp, so a collection that had already committed the reading (today: dispatch 46115370606 recorded the 21:02 posting at 06:11:35Z, with Pages a few minutes behind) read as "collector, parser or Pages at fault", and so did a clean run that fetched before CINGSA served a reading it had stamped earlier (No.118). The audit now reads main's ledger/gaswatch.jsonl (contents API with the raw media type, read only, and only when a run started after the stamp) and names deploy_pending (wait for Pages, don't dispatch; past 30 minutes read pages.yml), collection_running, late_post (clean runs all inside 60 minutes of the stamp, none recorded it: dispatch) and collected_after_post (a failed run, or a clean run long after the stamp that recorded nothing: a real fault). No status or verdict moves. tests/gaswatch_health.py 12/12; the new tests FAIL against the old script; a replay of 06:13Z with the real ledger reads deploy_pending; the live audit PASSes; ledger_guard PASS.
   DEFERRED about it: the audit still can't see the Pages run itself (it infers from the ledger timestamp and a 30 minute grace), and the 60 minute stamp lead rests on one measured lag (19+ minutes, No.118). If a late post ever lands past 60 minutes, the label reads collected_after_post and the remedy still says to read the run log, which is the safe direction.
2. Cause d (texture artifact), the z-fight share: AKT.audit 'coplanar' plus a qa WARN. It flags the shipped slide 08's stripe (rear face flush with the bevelled body) and nothing on the other eight slides or the demo deck.
3. Queue item: AKPOST.field accepts rows == 1 as a 1D curve.
Deferred in plain words: the ground contact shadow (unblocked 2026-11-24, contact shadow WARN still shipping) needs a pixel-critic-judged fixture and didn't fit after the trigger; cause b and c have no shared missing helper this week; Variety vs ledger (STALE) is a directors'-room choice against ledger/artwork.json with no machine defect named; the rubric 1.10 weights stay an owner decision, queued and untouched. Parked: reversed-Z depth (FIELD_NOTES 2026-11-27).
