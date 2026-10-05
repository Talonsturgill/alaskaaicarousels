# Machine queue: what the weekly machine pass works on

Since 2026-10-03 a run fixes only what broke in its own run and queues every other machine change
here, in Phase 12. Once a week the machine pass (Phase 12, brief in
`prompts/machine_weekly.md`) reads the week's own artifacts through
`scripts/week_digest.py`, works the themes that recurred and this list, and marks what it
shipped. `scripts/machine_due.py` reads this file to decide whether a pass is due early.

The owner's words, 2026-10-02: the daily automation should "only fix like the things that were
broken during the run", and once a week spend time "addressing the things that really need to be
fixed based on the recurring themes that it saw during the week ... based on actual output".

One line per item, in this exact shape, so the due check can read it:

    - [ ] <date found> | repeat: <runs it has bitten beyond the first> | <signature> | evidence: <what showed it, with frames and rounds> | fix: <the proposed change>

**A defect already open is never added twice.** The run that meets it again raises its `repeat`
count in place and appends its date to the evidence. An item at `repeat: 2` makes the pass due the
next day rather than waiting out the week.

A pass that ships an item changes `[ ]` to `[x]` and appends ` | shipped <date> <commit>`. An item
it can't fix safely stays open with ` | escalated <date>: <why>` and goes in the email.

## Open


- [ ] 2026-09-30 | repeat: 5 | gaswatch: evening collection slots land after the daily audit | evidence: runs 2026-09-30, 2026-10-01, 2026-10-02, 2026-10-03, 2026-10-04 and 2026-10-05 UTC (No.78: FAIL at wake, WARN by 08:21Z, the 22:57 Alaska reading uncollected; No.79: WARN at 06:2xZ, CINGSA's 22:12 Alaska reading of October 4th posted after the 22:22Z collection, workflow_dispatch 403 again) each found CINGSA's evening reading unpublished because GitHub dispatched the 19:20Z slot 3 to 4 hours late and the 04:40Z and 07:20Z slots after the run; workflow_dispatch from the routine is 403 | fix: owner decision only (schedules and credentials are off limits to a run): either grant the routine Actions write so it can dispatch the collector, or move the routine's audit later than the 07:20Z slot
- [ ] 2026-10-04 | repeat: 1 | render: synchronous art before the first await blocks page load | evidence: No.77 slides 06 (aksdf, 90 to 140 s) and 07 (per-pixel paint); No.78 slide 06 (per-pixel heightfield) timed out page.goto('load') at 45 s until the slide awaited load and yielded once | fix: render.py detects a load timeout with no renderReady settled and prints the remedy (await the load event, then never yield after the long block); SKILL.md states it beside the 30 s race note
- [ ] 2026-10-04 | repeat: 0 | qa: axis census threshold set by a declared-but-undrawn mark | evidence: No.77 slide 03 reported phantom undeclared marks at 144.5 and 904 after a tick was removed but its declaration kept | fix: when the weakest declared mark carries no ink, name THAT mark as undrawn instead of reporting texture as undeclared marks
- [ ] 2026-10-05 | repeat: 1 | akengrave: surface() lay collapses on non-rectilinear forms | evidence: No.77 slide 08 (river channel, collapsed onto a few iso-lines even with seedDeg); No.78 slide 08 (radial flange face, rectangular patches and gaps); both rebuilt by hand | fix: seed lines along the form's own iso-lines (marching squares on form) when the field is radial or sinuous, and add a self-test that fails when coverage of a radial form drops under a set share
- [ ] 2026-10-05 | repeat: 0 | render: --timeout is milliseconds and a seconds-sized value fails silently | evidence: No.78 slide 06, `--timeout 300` failed page.goto in 0.4 s | fix: render.py warns and treats values under 1000 as seconds, or rejects them with the unit in the message

## Done

- [x] 2026-10-05 | repeat: 0 | cron_health: GitHub's branch-filtered run listing can serve stale runs | evidence: No.79 at 06:22Z, `runs?branch=main` returned Pages newest 2026-09-11 and broadband 2026-09-14 while the unfiltered list had 2026-10-04 and 2026-09-28, so two healthy jobs read FAIL | fix: dropped the server-side filter, since production() already keeps main; the weekly pass may add a regression test that feeds a stale filtered list | shipped 2026-10-06 fb3d935f
