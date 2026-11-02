# Automation retro, run 2026-11-01 (No.102)

## What broke in this run, and what happened to it

- cron_health: the first audit died on a TLS reset inside `git fetch --unshallow`. A manual re-run passed. Fixed this run in the weekly pass (88097ad4): two retries at 5 s and 15 s, each printed.
- Gas Watch: the November 1st reading posted at 20:53 AKST, after the evening slots, so the first live audit FAILED. Dispatched gaswatch.yml on main (run 41398362893), the record landed at 58.6 percent, Pages deployed, the re-audit PASSED. The 18th run to meet this. The weekly pass made gaswatch_health name the shape (`late_post` versus `collected_after_post`); the remaining slot or audit-time decision is the owner's.
- AKPOST.grade under an identity transform on the 2x backing graded a quarter of slide 01 and drew a seam that every gate passed. Fixed in the weekly pass: an AK CONTRACT error and a qa FAIL.
- contact_probe proposed a ground rect inside slide 06's "ABOUT 2%" readout. Fixed in the weekly pass: text boxes are skipped.
- docket.json was rewritten with indent 1 by a one-off script, which would have produced a whole-file diff. Caught before commit and rewritten at indent 2. Not queued: the docket tools already write indent 2, the fault was a hand script.
- The locator's GRID LOAD label overran its 460 px SVG box at 13 px and qa read the overflow as painted over. Fixed in the deck's own aklocator.js (500 px box). Deck furniture, not machine.

## Queued, not fixed

- Nothing new. The pixel critics' round 1 found the same three art causes the weekly digest counts (b largest object under-modelled on 05 and 07, c an eventless lower band on 03 and 06, d texture artifacts on 02, 06 and 07); the weekly pass judged them per-object with no shared measurable cause, and this run agrees.
