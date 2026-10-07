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

- Phase 11 to 12, branch CI: two checks went red on the first push, both caused by the day's new docket item. The ask box's inline payload passed its 190,000-byte ceiling (189.6 KB), and the landscape phone map fit fell to 53 percent (floor 55) because the item's pin sat 2.2 map units from the Anchorage pins, just outside the 2.0-unit shared-coordinate rule. Fixed in the run without loosening either gate: the payload now ships each row's hay without the opening it shares with the row's own fields and the page rebuilds it byte for byte (170.1 KB, asserted in the self test), and the item uses Port MacKenzie's own coordinate (57 percent). A third red (the embed regression's fixture row has no hay) was the first fix's own edge and is fixed. This is the second day running that one new docket item tripped both gates; queued for the weekly pass.

## Upgrades this run

No upgrades. The pass is weekly. The two CI repairs above are fixes to what broke in this run's PR (scripts/ask_answers.py, scripts/site_build.py, the docket item's coordinate), carried in the fix commits, not upgrade commits.
