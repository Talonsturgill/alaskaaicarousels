# Automation retro, 2026-10-04 (No.77)

## Trend check, the standing repeat offender
`trend_check.py --window 10`: Artwork craft and genuine detail was the weakest criterion on 8 of 10 runs (mean 7.2). It is STALE by text match, last worked 2026-09-28. Today it was WORKED: this is a weekly pass day (machine_due exit 0), and the upgrade engineer's pass went straight at the flow critic's three per-frame art causes (b largest object least modelled, d texture artifact, c dead region). The per-slide pixel critic now answers those three questions against the CRAFT PLAN (scripts/critic_brief.py). The declared tonal arc is now measured (scripts/tonal_arc_check.py, a WARN-only gate_status row). Variety vs ledger and Legibility (1 of 10 each) are deferred, because neither recurred. The legibility warns that keep shipping (ragged display line on 5 runs) sit in a line-break area where text-wrap has measured null four times.

## Deviations, phase by phase, with evidence
- Phase 3.6 Gas Watch live audit FAILED all run on 'source reading published' only. CINGSA posted an 18:52 Alaska reading after the last collection (run 386 at 23:03Z, itself the 19:20Z slot dispatched 3h43m late), and GitHub had not dispatched the 04:40Z or 07:20Z slots by 08:36Z. workflow_dispatch from this session returns 403 Resource not accessible by integration. This is the fourth consecutive daily run with this exact shape, and it is now a queued machine item (below). Incident recorded in gaswatch_incident.json, and the gate reads WARN.
- Phase 7: two slides blocked page load. aksdf's raymarch on 06 (90 to 140 s, synchronous) and 07's per-pixel paint ran before the first await inside renderReady, so page.goto('load') timed out at 45 s. Fixed in the slides by waiting for the load event, yielding once, then never yielding after the long block. SKILL.md documents the 30 s race but not the load block.
- Phase 7: akengrave `surface()` collapsed onto a few iso-lines for a sinuous river channel form, even with seedDeg set. 08 was rebuilt as a hand-made streamline lay (technique 119).
- Phase 8: qa.py's axis census reported two phantom undeclared marks on 03 after a drawn tick was removed but its declaration kept. The census threshold is the weakest declared mark, so a declared-but-undrawn mark drops the threshold into the ground texture. The message named the phantoms, not the cause.
- Phase 8: the copywriter's claim assignment diverged from the storyboard CLAIMS INDEX on 12 ids. plan_drift caught it, and the index was regenerated from copy.json.
- Phase 8: five frames carried a dome-cobble bed (cross-frame repeat over the CRAFT PLAN limit of three). The CRAFT PLAN census counts primary mark-making only, so the planning check could not see it. The flow critic did. Two frames were rebuilt (06 moss, 02 trimmed lane).
- Subagents: none failed. The upgrade engineer ran in an isolated worktree and its diff was carried over as one patch.

## Weekly pass (machine_due exit 0)
Run by the upgrade engineer in a worktree and carried over as one patch; changes in commit 1d20e423 (`upgrade(2026-10-04)`), SHA recorded in 349789f7. Every verify command it returned was re-run from the repo root: the critic_brief, tonal_arc_check, gate_status, week_digest and machine_due self-tests passed; tonal_arc_check reproduces 2026-10-02's WARN and passes today's deck; the demo deck renders, and its pre-existing qa WARN is unchanged (no engine file touched). Themes, counts and the verification are in ledger/upgrades.json and config/machine_pass.json.

## Queued for the next pass
See knowledge/MACHINE_QUEUE.md (three items added today).
