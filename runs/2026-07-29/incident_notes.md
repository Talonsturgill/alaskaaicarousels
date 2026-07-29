# Showrunner incident notes for the Phase 12 upgrade engineer (run 2026-07-29)

## Incident 1 (THE BIG ONE) — six labels shipped off their own plates, through two scoring cycles

The scorer capped the deck at 6.90 from an uncapped 8.33 on a single hard fail:
clipped/overlapping text. Six mono labels overran their knockout plates across
slides 04, 05 and 07, including a chip border rule drawn straight through the
"T" of PERMITS, and one annotation ('ONE MACHINE PER 2 WKS') sat entirely off
its knockout.

Root cause was arithmetic: JetBrains Mono at 24px with 0.10em tracking advances
16.8px per character; every affected plate had been hand-sized at roughly 14.

Why nothing caught it: render.py's overlap detector inspects DOM text line
boxes. Every defect was SVG <text> against an SVG <rect>, against canvas
artwork, or under a DOM block. machine_qa reported 0 fails on a visibly broken
deck through TWO full scoring cycles. Note that cycle 1's one_sentence_fix
misdiagnosed it as a z-index problem, and cycle 2 found that revision #3 had
CREATED one instance (lengthening a legend without re-sizing its chip).

Fix already applied in-run (Phase 9, showrunner): render.py now emits
out.svg_plates measuring every SVG <text> against (a) the <rect> painted under
it, (b) any opaque <rect> appended AFTER it in document order, and (c) any
opaque DOM element composited above the whole <svg>, sampled with
elementsFromPoint across the label's own box. qa.py grades all three as FAIL,
demoted to WARN for data-decorative / data-overlap-ok. Verified against a
purpose-built ground-truth slide carrying one spill case, one painted-over case
and one correct control: both defects reported, control stayed silent.

YOUR JOB on this one: log it properly in ledger/upgrades.json as kind "fix"
(it is already implemented and verified, do NOT re-implement it), and consider
whether it should be hardened further. Specifically worth your judgement:
  - the 2px tolerance is empirical, not derived
  - the backing-plate heuristic picks the LAST overlapping preceding rect,
    which is a guess, not a declaration; a data-plate attribute would be exact
  - nothing yet prevents the arithmetic error at AUTHORING time. A helper that
    sizes a plate from getComputedTextLength (or from a published per-font
    advance constant) would make the class unreachable rather than merely
    detectable. This may be the higher-value upgrade.

## Incident 2 — every repair produced a knock-on

Widening a chip pushed it into a legend. Raising a plate cut the label above
it. Moving slide 03's source line off the counter landed it on the self-audit
annotation, and the next move landed it in the bottom safe margin. Six render
cycles were spent on what looked like a one-line fix. The gate caught each
knock-on, which is the system working, but the cost was real.

## Incident 3 — the deck's central visual encoding did not render

The artwork ledger states the hero column's material change at hour 7 (steel
below, brass above) carries the thesis with zero words. Under a single
0xffb067 sodium key, steel 0xb9bcbd and brass 0xd39c31 both read as one amber
extrusion. Lifting steel to 0xe8edf0 and adding a proud collar at the seam
helped; darkening the brass to force contrast made the frame muddier and was
reverted. Scorer put artwork craft at 6, its lowest criterion. This is the
second consecutive run to hit an artwork-craft ceiling (see the 2026-07-26
FIELD_NOTES entry and upgrade). Consider whether anything objective can be
gated here, e.g. a check that a declared two-material hero actually shows two
separable value populations in the rendered region.

## Incident 4 — dossier_check.py reads only field 4a's FIRST LINE

Its continuation loop breaks on the first (empty) element of splitlines(), so a
dossier can satisfy the modeled-tone requirement with one line and say anything
afterwards. All nine dossiers had to be rewritten to lead with modeled-tone
words. This is a real gate weakness (it under-reads, so it can pass a dossier
whose lower-third plan is furniture from line 2 onward).

## Incident 5 — a shell cd/&& short-circuit silently skipped a whole fix script

`cd out/2026-07-29/slides && python3 ...` failed the cd (persistent cwd had
already moved) and && swallowed the rest. The script reported nothing and I
believed it had run. Low-value to gate, recorded for completeness.

## Environment notes
- getImageData is pathologically slow in this headless build once a WebGL
  canvas has been composited: 34,118ms for one AKPOST.grade call on slide 03.
  Fixed in-run by grading the 2D atmosphere BEFORE the GL composite. This is
  already documented but is NOT yet enforced anywhere.
- slide 03 still takes ~38s to render against a 30s renderReady cap; it passes
  because the cap covers renderReady, not total page time. Fragile.
- shrink_pdfs.py declined this run's PDF (images at 40.6 and 41.4 dB, below the
  42 dB floor). Correct behaviour, reported honestly, no action needed.
