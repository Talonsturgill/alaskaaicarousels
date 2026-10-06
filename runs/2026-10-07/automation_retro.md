# Automation retro, run 2026-10-07 (No.80)

## Trend check (window 10)
Artwork craft and genuine detail was the weakest criterion on 8 of the last 10 scored runs (mean 7.15, last 7.5, last worked 2026-10-04). It stays the repeat offender. The weekly machine pass ran yesterday (machine_due exit 1, last pass 2026-10-06), so it is queued for the next pass rather than worked today; this run attacked it inside the deck instead, with four editing rounds aimed at the largest object on each frame (07 rebuilt as a per-pixel perspective terrain render, 06's conductor given an environment to reflect, 02 and 05's terrain marks retuned). Thumb-stop cover and Legibility each appear once, stale but not recurring.

## Deviations this run, with evidence
1. Run date: Anchorage date 2026-10-05 22:15 AKDT, and runs/2026-10-05 and 2026-10-06 had already shipped, so run_guard's default date read ALREADY_SHIPPED; the first free date, 2026-10-07, cleared.
2. Gas Watch live audit FAILED at 06:20Z on the evening reading of October 5th (CINGSA posted after the 00:51Z collection; the 04:40Z and 07:20Z slots had not run; workflow_dispatch from the routine is 403). It PASSED on the later re-audit once a slot collected the reading, so no incident file was needed. MACHINE_QUEUE gaswatch item raised to repeat 6 (owner decision, already escalated).
3. curl to aws.state.ak.us failed through the proxy (ws_closed_mid_exchange); WebFetch read the page instead.
4. The fact-checker's final message was a handback tool call, so its claims JSON was recovered from the transcript by walking its strings.
5. The planned type sizes (kickers 21 to 22 px, labels 19 to 21 px) produced 36 tiny-text warnings on the first full render; every mono label was raised to 24 px by hand. Queued (dossier_check should catch a sub-floor plan).
6. All nine headlines used per-line nowrap spans, which render.py does not record as one node, so copy_sync_check failed every headline until each last line was moved out of its span. Queued (render.py).
7. The locator strip's blue base dots broke the ink law on the six frames declaring military ink absent (qa.py FAIL). Fixed in run: akcorridor.js reads the frame's own data-ink and draws hollow grey rings where blue is absent.
8. The fixture counter at top 1270 sat outside the 80 px safe zone; moved to 1234. On light frame 06 its gold digits measured contrast 1.0, now on a dark chip.
9. Slide 06's aluminium conductor rendered near black because the hand-rolled renderer had no environment; round 1 scored it 5.5. Fixed with a PMREM of the haze sky. Queued (qa.py warn for metal without an environment).
10. Slide 07's first engraving (crest-parallel offset lines) read as stacked waves (5.3 in round 1); rebuilt as a per-pixel perspective terrain render with constant-distance engraving. Its first rebuild at eye 300 m let the near foothills dominate; an eye of 1,500 m and fov 48 fixed the layering.
11. The cover's other Railbelt lines ran from the Beluga ring toward Willow and read as the proposed line, an honesty-guard breach a pixel critic caught in round 1; those lines are no longer drawn on 01 or 09.
12. The flow critic found 06's conductor cast across the snow read as a second wire, and 06's headline restated 03; both changed in round 4.
13. Pixel critics repeatedly said they could not crop to 100 percent, so texture calls rested on the 1600 px display. Queued (native-pixel crops beside the thumbs).
14. Two critic tasks launched as background jobs although run in the foreground; no turn ended while they ran.

## Rounds
Four editing rounds after the first render (cap five): round 1 all nine frames, round 2 five frames, round 3 slide 06, round 4 the flow review.

## Queue
Four new items in knowledge/MACHINE_QUEUE.md (akthree metal without environment, dossier_check sub-floor type, render.py span headings, critic native crops) and the gaswatch item raised to repeat 6. Eight items now open. The pass is weekly; the next is due 2026-10-13 unless a queued item bites twice more first.
