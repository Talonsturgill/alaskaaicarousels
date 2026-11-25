# AUTOMATION RETRO, run No.123, 2026-11-24

## Standing repeat offender
trend_check --window 10 names Artwork craft and genuine detail (weakest 8 of 10, mean 6.98, last worked 2026-11-11). The weekly pass is DUE today (machine_due exit 0), so it is handed to the upgrade engineer with this run's incident notes as the week's top theme; its report and any upgrades ride this PR as one upgrade(2026-11-24) commit.

## Deviations, phase by phase (with evidence)
- Wake: CLAUDE_EFFORT read `medium` although .claude/settings.json sets effortLevel high. Recorded in plan.md and the draft's editor notes; nothing in the repo can force it.
- Research: all six beats thin (searches 24, 26, 25, 24, 25, 18). The story came from the docket refresh (KFSK November 23rd), not a scout, which is the docket watch doing its job.
- Claims: the fact-checker spent 20 WebFetch calls on 12 distinct URLs; 8 justified repeats because WebFetch returned summaries without verbatim text on the first read (KFSK, Alaska's News Source, Petersburg Pilot). The primary PDFs (ordinance, agenda) came from the borough's CivicClerk API, found by the showrunner after the borough website returned a JS shell and a fetch worker hit 403.
- Docket: worklist budget raised from 6 to 11 to cover the deferred tail; four items could not be re-verified (DNR 403, notices 404, FNSB 404, Alaska health newsroom 404) and were left unstamped rather than stamped unchecked. Ask payload headroom 5,027 bytes (near the 5,000 floor).
- Gas Watch and cron: gaswatch.yml exit 5 because CINGSA prints "0]" in the injection Available Capacity cell. Upstream; incident JSONs written; rows WARN. Not fixable without inferring a value, which the Gas Watch rules forbid.
- Art build: the first full build passed qa.py after three FAILs (canvas over body text on 05, a dead bottom third on 08, a motif under a label on 09), each fixed in one pass. qa.py's "metal with nothing to reflect" warned 40 times until environment intensity rose to 0.55 to 0.85.
- Pixel review round 1: all nine frames revise. Causes the critics shared: GPU edges flat; lower thirds promised in 4a but rendered as plain pad or uniform texture; gold leaking into type; a hachure relief reading as fur. One repair (a near bank section on 05) buried the subject and was reverted inside the round.
- Flow review round 2: tonal plateau (eight frames within 9 L*), a misaligned 02 to 03 edge-tease, three dense frames 02 to 04. All fixed except the plateau, which improved (07 and 08 lifted from 11 to 16 and 15) but still WARNs.
- copy_sync caught two first-person/copy drifts before ship ("Tell us" on 09 failed the first-person rule; slide copy edits re-synced to copy.json).
- aggregate_check required 16 declarations for vote tallies and "three tests"; the Fairbanks line's 2027 was not in its claim, so the slide says "next year" instead.

## Queued (not fixed this run)
See knowledge/MACHINE_QUEUE.md entries added or bumped by this run and the weekly pass report.
