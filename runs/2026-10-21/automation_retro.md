# Automation retro, run 2026-10-21 (No.92, THE FLOWN LINE)

## Trend check (window 10)
Top repeat offender: Artwork craft and genuine detail, weakest in 6 of 10, mean 7.05, last worked 2026-10-04.
Today's answer: worked. The weekly machine pass came due today (the critic_brief thumb item reached
repeat 2) and the upgrade engineer ran it before the merge with this week's digest; its changes are the
separate upgrade commit and are listed in ledger/upgrades.json under 2026-10-21. In the run itself the
art got four editing rounds of the five-round cap.

## Deviations, phase by phase
- Phase 3.6: cron_health first read WARN on a pending news.yml run; re-run before ship read PASS.
  Site screenshots needed Playwright's executable_path set to /opt/pw-browsers/chromium.
- Phase 3: one DGGS report PDF exceeded the 48 MB fetch ceiling (fetched with --max-mb), and DGGS
  reset connections twice (retried). A draft claim (C82) read a cited reference title as a place;
  replaced with the verbatim from GPR 2026-3.
- Phase 5: dossier_check failed on 4a fields under 200 characters and on figures 3 and 4 lacking
  claims; fixed by expanding 4a and adding C80 and C81.
- Phase 6: the caption critic returned "neither" in round 1; one reassigned director wrote the
  winner. The first caption's hook ran 155 characters against 140.
- Phase 7: qa FAILed on top-loaded compositions (02, 03, 06), a measured-axis census reading a filled
  bar's face as undeclared marks (06), a text collision and a wrap drift (07). Cured by a regional
  terrain-shade asset (02), an engraved ground plane (03), reordered rows and declared ticks under
  the bars (06). The census item is queued.
- Phase 8: all nine frames returned revise in rounds 1 and 2. Deck-wide causes: type reserves
  printing as slabs, a rail lip stroked per segment (beading), the gold drifting to lemon under the
  grade, the footer fixture at about 2.3:1. Round 3 shipped 03, 04, 06, 07; round 4 shipped 01, 02, 04,
  09; 05 and 08 took one more fix after round 4. Two fixes overshot and were dialled back inside the
  same round after the showrunner re-read the frame (a row cull on 01, an edge fade on 08 that thinned
  the whole field because the grid has isolated empty cells inside it).
- Phase 8: critic_brief.py does not name a 432 px thumb, so thumbs were written into render/thumbs
  by hand every round (queue item raised to repeat 2, which made the weekly pass due).
- The harness-designated branch is tsturg/clever-mayer-d3poy8, not claude/carousel-<date>; the run
  used the designated branch.

## Queued today (knowledge/MACHINE_QUEUE.md)
- qa/doctrine: no gate measures the site fixture's contrast.
- qa axis census: a filled bar's own face reads as undeclared marks.
- doctrine/qa: the one gold drifts to lemon or olive when drawn before the grade or inside WebGL.
- raised: critic_brief thumb path, repeat 1 to 2.
