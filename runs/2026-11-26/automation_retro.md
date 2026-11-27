# AUTOMATION RETRO, run No.125, 2026-11-26

## Standing repeat offender
trend_check --window 10 still names Artwork craft and genuine detail as the weakest criterion, with "busy art under text" the defect class that keeps shipping (6 of 10 runs). The weekly pass is NOT due (machine_due: last pass 2026-11-24, 2 days ago, due at 7, 0 repeat offenders), so it is queued for that pass, and this run fixed only what broke in it. This deck kept type on dark wall or bare paper throughout and the final machine_qa carries no busy-art warn.

## Deviations, phase by phase (with evidence)
- Wake: CLAUDE_EFFORT read `medium` although .claude/settings.json sets effortLevel high. Recorded in run_state.json; nothing in the repo can force it.
- Research and claims: 52 claims (39 primary). FNSB's action memo is a scanned PDF with no text layer; pdftoppm to PNG plus a visual read verified it. af.mil answered 403, so the Air Force data center claim was dropped.
- Art build: a new deck module (assets/js/akdater.js, akdater3d.js) built the PBR band dater, felt, sheet impressions and a PMREM desk room. Round 2 added `blur` and `plate` options to buildDater.
- Pixel review: round 1 all nine revise (5.0 to 7.0), round 2 all nine revise (5.8 to 7.4). Flow review round 3: revise 7.3; 04 body cut, 07 trimmed and made to plant 08.
- Scoring: round 3 scored 8.395 with art 7.5; the CRAFT FLOOR cycle (round 4) on 04, 08, 03, 06 re-scored 8.395, art 7.5 (08 and 03 better, 04 and 06 not).
- Gates during the run: aggregate_check FAILed once on an undeclared "+6 MONTHS" tick label (declared); qa FAILed contact shadows twice after relighting (pool restored on 04, 06 re-probed with contact_probe); copy gates PASS throughout.
- Phase 3.6: cron health PASS (7 workflows), gas watch live PASS, site sign-off PASS (192 pages); nothing to repair.

## Fixed in this run
- akdater3d.buildDater gained `blur` (band glyph motion blur) and `plate` (material overrides) so slide 06 could show the declared blurred bands.

## Queued (not fixed this run), in knowledge/MACHINE_QUEUE.md
- rubric weights sum to 1.10, so weighted totals run about ten percent high (an owner decision; this run's 8.395 is 7.63 normalized).
- qa's metal-with-nothing-to-reflect check reads a slide's metalness literal and misses an environment built in a module.
- a second instance of a critic naming an "ordered dither lattice" on a frame with dither off (measured random grain).

Weekly pass: not due. 84 items queued.
