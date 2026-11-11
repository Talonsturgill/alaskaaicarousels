# Automation retro, run 2026-11-10 (No.111)

Weekly machine pass: NOT due (machine_due exit 1; last pass 2026-11-08). No upgrades this run. Every
machine change the run found is queued in knowledge/MACHINE_QUEUE.md (65 open items, 0 at repeat 2).

## Top repeat offender (trend_check --window 10)
Artwork craft was the weakest criterion on 6 of the last 10 runs (mean 7.1, last 7.0). This run it
was the weakest again, at 7. It is QUEUED for the next weekly pass, not worked today, because the pass
is weekly. Two concrete causes from this deck go to that pass with evidence: aksdf's internal-res
upscale (new item) and the plan-oblique column-lift smear (new item). Both were named by critics in
every round and by the scorer. What would let the pass tackle the offender at root: a renderer-level
supersample in aksdf, and a column-fill that interpolates instead of painting one sample down a gap.

## Deviations, phase by phase
- Phase 3.6: the Gas Watch late post was found and repaired in-run (dispatch, then verify live). Live
  audit PASS afterwards.
- Phase 7: three engine traps were met again and fixed in the slide code. AKPOST.grade and holdInk on
  an unscaled context graded only the top-left quarter. aksdf on an unscaled context did the same.
  A leader label must equal the rendered text. All are documented. The slide authoring missed them on
  first write, so none is a machine defect.
- Phase 8: five editing rounds, the cap. Round 1 found three SHARED causes that every critic could see:
  the bilinear DEM lookup printed the lattice in every per-pixel relief, a straight sine ripple printed
  as a comb, and the fixtures sat on lit sand. All three were fixed once, in aksand.js and the fixture
  template. Round 2 overcorrected the plan-frame ripple into corduroy and cost a round to put back.
  The flow critic's best single change (08 into the akthree table) came at round 5. Earlier, it would
  have left a round for the scorer's weakest frames.
- Phase 8: one helper-call edit caught the helper's own body in a global replace (RP calling RP). The
  smoke render would have hung; it was read and fixed before render. A second edit appended a line
  into a trailing comment, which moved a label to the top-left corner. It was caught on the next thumb read.
- Phase 10: the scorer found that the rubric's weights sum to 1.10. Every total in the trend window is
  inflated by that factor (8.735 by the formula is 7.94 normalized). This needs a human call because it
  moves every threshold's meaning. It is queued and escalated in the email, not changed by the run.
- Phase 11: main had moved on (gaswatch cron, docket watch, video feed). The merge was clean. The cron
  builds the site at the Alaska date, which was November 10th, so the run built at 2026-11-10 without
  rolling the site back.

## Queued this run
- rubric weights sum to 1.10 (new, escalate)
- aksdf internal-res upscale stair-steps silhouettes (new)
- plan-oblique column lift smears steep lee faces (new)
- aksdf has no bounce term (repeat 0 to 1)
- ask pack at 31,877 of 32,000 tokens, ask payload 106 bytes under ceiling (repeat 0 to 1)

no upgrades

## After the PR opened
- CI `checks` failed on the ask-box stress suite: "bitcoin mining in wyoming" matched the Houston docket item, because a new source outlet label named DNR's Division of Mining, Land and Water and the engine indexes outlets. The label was changed to "Alaska DNR public notice" (URL unchanged) and the suite passed locally. Its E5 row also fails locally on unmodified main (an environment difference), and CI passes it.
- The Gmail sign-off table first printed UNREPORTED: the run kept its Phase 3.6 verdicts in site_lines.txt, not under the run_state keys gmail_draft.py reads (site_signoff, gas_watch_verdict, gas_watch, cron_health, site_fixes). They were added to run_state and the table now prints verdicts. The record should be written at Phase 3.6, not reconstructed at Phase 13.
