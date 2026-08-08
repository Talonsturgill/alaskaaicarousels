# PHASE 3.6 — GAS WATCH ONCE OVER, 2026-08-08

## Step 1, the checker (baseline, before any edit)
`python scripts/gaswatch_pagecheck.py --out docs` -> exit 0, 15 of 15 PASS.
Reading current as of 2026-08-07, 3 days on record, chart present.

## Step 2, the look — ONE REAL DEFECT FOUND

Section "What is not measured by anyone" published this sentence:

  "On August 6th, 2026 that residual came to 136.8 MMcf per day against modeled
   demand of 102 MMcf per day, which is 134.1 percent of the region's gas
   arriving from sources no public feed reports daily."

A share OF THE REGION'S GAS caps at one hundred percent by definition, so the
page was asserting something impossible. The arithmetic was fine. The noun was
wrong. `unmeasured_share_pct` is the residual divided by MODELED DEMAND, not by
the region's gas, and on a summer injection day the measured storage withdrawal
is negative, so the residual necessarily comes out above demand.

This is the exact class Phase 3.6 names: a sentence that asserts a state the
data could flip. It would have read correctly all winter and wrongly all
summer, and nothing on the page compared the words to the sign of the number.

## Step 3, the fix — PRESENTATION ONLY

Edited `scripts/gaswatch_build.py` HTML and its `_comparison` helper. Nothing in
the collector, the model config, the HDD history or either gas ledger was
touched, per non-negotiable 19.

1. New `_comparison` key `residual_regime`, keyed to the sign of the measured
   `storage_withdrawal_mmcfd`: filling / drawing / flat. Comparisons belong in
   `_comparison` and not in prose, which is the rule that made this fixable.
2. The paragraph now says "or 134.1 percent of it, and all of it arrived from
   sources no public feed reports daily", then adds the computed clause:
   "It runs higher than demand because the field was filling that day, so some
   of that gas went into storage rather than to a burner."
   The withdrawal-season wording is the same sentence with the other branch.
3. Self-test case added alongside the three existing state-dependent-wording
   flips, asserting the clause follows its input both ways.

No numeral was typed, so the numeral lint is unaffected.

## Verification
- `python scripts/gaswatch_build.py --self-test` -> clean, including the new
  "residual_regime follows its inputs both ways" row.
- Rendered the paragraph directly from `page_body()` and read it back.
- Full `site_build` + `gaswatch_pagecheck` re-run happens at Phase 11 step 2.

## Draft line (Phase 13)
GAS WATCH: PASS, read 2026-08-08, 3 days on record, chart present. Checker clean
at 15 of 15. The daily read caught one prose defect and fixed it in presentation
only: the residual paragraph called a ratio-to-demand a share of the region's
gas, and was publishing 134.1 percent of it on an injection day. The clause is
now computed from the sign of the measured withdrawal rather than typed.
