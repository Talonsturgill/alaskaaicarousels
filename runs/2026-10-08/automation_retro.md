# Automation retro, run No.81, October 8th

## The weekly pass

`scripts/machine_due.py --date 2026-10-08`: not due. The last pass was October 6th, two days ago, and no queued item reached repeat 2 today. Steps 2 to 4 don't run. Every change this run found is queued in knowledge/MACHINE_QUEUE.md for the next weekly pass.

## Standing repeat offender

trend_check over the last 10 scored runs names Artwork craft as the weakest criterion on 7 of 10, last worked on October 4th. Queued for the weekly pass, not deferred silently: it is the theme the pass is built around. This run's per-slide loop spent all four rounds on art, and the round notes are evidence for it (critics/round1.json to round4.json).

## Deviations, phase by phase, with evidence

- Phase 3.6, Gas Watch live: FAIL at wake and again at 07:45Z on CINGSA's evening reading, the same cause as the last seven runs (GitHub dispatches the evening slots late, the routine's workflow_dispatch is 403). Already escalated to the owner; repeat raised.
- Phase 7, headline markup: AK.fitText exceeded maxLines on several frames while lines were authored as spans, until every headline moved to `<br>` breaks with white-space nowrap. Same class as two open queue items (aktype authored breaks, render span headings). Repeats raised.
- Phase 8, contacts: contact_probe proposed a ground rect that sat on the object itself twice. On slide 01 its h axis took the lit tag face (L* 67) as the pool, and on slide 06 its v axis took the twine crossing the shelf front as the lit ground. The proposed pairs measured dL 59 and 29 for a shadow the eye reads as dL 6 to 9. Both were declared by hand from a measured profile instead. Queued.
- Phase 8, aksdf deadline: slide 07's lump at 650 x 812 internal ran past deadlineMs 70000 and dropped shadows from row 590, which printed the hard horizontal seam round 1's critic reported. render.py's console capture and the AK DEGRADED message named it exactly, and raising deadlineMs to 200000 cleared it. The gate worked; nothing to queue.
- Phase 8, critics without a crop: every round's critics said again that they judged texture from the 1600 px view. Repeat raised on the open item.
- Phase 8, rounds: all four per-slide rounds used. 05 and 07 were holdouts at round 4 and carried a final fix into the flow critic unreviewed per slide.

## Upgrades this run

No upgrades. The pass is weekly; nothing broke mid-run that needed an engine change to finish the deck.
