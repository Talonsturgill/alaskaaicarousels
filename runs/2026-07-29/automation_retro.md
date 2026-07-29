# AUTOMATION RETRO, run 2026-07-29 (Carousel No. 19)

Phase 12, step 1. Walked `out/2026-07-29/run_state.json` phase by phase against
`prompts/routine_instructions.md`, with the showrunner's `incident_notes.md`,
`score_report.json`, `render/machine_qa.json`, `render/render_report.json` and
`scripts/gate_status.py` output as evidence. Every phase reads "done" and the
completion gate exits 0, so the deviations below are all inside phases that the
state file calls clean.

## Deviations

### D1 (dominant). The machine could not see six broken labels, through two full scoring cycles

Spec: Phase 7 says "Fix every FAIL ... do not proceed until qa.py exits 0", and
the machine gates are non-negotiable 5. The gates ran and returned 0 fails on a
visibly broken deck.

Evidence:
- `score_report.json` `hard_fails_as_scored`, six entries: slide 05
  "ABOUT 10% OF AK PERMITS" overran its chip by 20px with the chip border rule
  drawn through the "T" of PERMITS; slide 04 "DIFFERENT MEASURES, NOT ONE."
  overran by 34px onto the brass ledge; slide 05 "1,300 MARKS, ONE PER PERMIT"
  by 58px and "ONE LIT. NO COUNT." by 12px; slide 07 "SCORE. THE PERMIT HOLDER"
  by 9px and "ONE MACHINE PER 2 WKS" sat entirely off its knockout.
- `cap_reason_as_scored`: the rubric capped the deck at 6.9 of record against a
  threshold of 8.3, from an uncapped 8.33. Legibility scored 5.
- Root cause is arithmetic, per `post_score_remediation.root_cause`: JetBrains
  Mono at 24px with 0.10em tracking advances 16.8px per character, and every
  affected plate was hand-sized at roughly 14px per character. Slide 05's
  authoring shape shows it exactly: `el('rect', {x:580, width:420 ...})`
  followed by `mono(594, y+32, s, 24, ...)`, two independent hand-typed numbers
  that have to agree.
- Why no gate saw it: `render.py`'s collision detector walks DOM text LINE
  BOXES (a Range-based path), and every defect was SVG `<text>` against an SVG
  `<rect>`, against canvas artwork, or under a DOM block. The 2026-07-26
  occlusion probe hit-tests DOM text only.

Status: fixed in-run by the showrunner in Phase 9. `render.py` now emits
`out.svg_plates`, measuring every SVG `<text>` against (a) the `<rect>` painted
under it, (b) any opaque `<rect>` appended AFTER it in document order, and
(c) any opaque DOM element composited above the whole `<svg>`, sampled with
`elementsFromPoint` across the label's own box; `qa.py` grades all three as
FAIL, demoted to WARN for `data-decorative` / `data-overlap-ok`. Verified
against a purpose-built ground-truth slide. Logged as a Phase 12 entry this run
(it was not previously in `ledger/upgrades.json`, so the maintainer's daily
email would not have shown it).

Residual, and the reason this run spends a second slot: the gate is a DETECTOR.
The arithmetic that produced the defect is still reachable at authoring time,
and nothing stops the next deck from typing two numbers that disagree.

### D2. The remediation loop misdiagnosed the defect once and manufactured it once

Spec: Phase 10 allows two bounded scoring cycles. Both were spent.
- Cycle 1's `one_sentence_fix` called it a z-index problem. It was not; the
  labels were wider than their plates.
- Cycle 2 found that revision #3 had CREATED one of the instances, by
  lengthening a legend string without re-sizing its chip.

This is the same root as D1 seen from the other side: with no measurement, a
copy edit silently changes a geometric fact.

### D3. Every repair produced a knock-on, at six render cycles

Evidence: incident notes 2. Widening a chip pushed it into a legend; raising a
plate cut the label above it; moving slide 03's source line off the counter
landed it on the self-audit annotation, and the next move put it in the bottom
safe margin. The gate caught each knock-on, which is the system working, but
the cost was six render cycles on what looked like a one-line fix. Hand-typed
absolute coordinates are the shared cause with D1 and D2.

### D4. The deck's central visual encoding did not render, and artwork craft hit a ceiling for the second consecutive run

Evidence: `score_report.json` criteria, Artwork craft and genuine detail = 6 of
10 at weight 0.16, the deck's lowest. `ledger/artwork.json` states the hero
column's material change at hour 7 (steel below, brass above) carries the
thesis with zero words; under a single 0xffb067 sodium key, steel 0xb9bcbd and
brass 0xd39c31 both read as one amber extrusion. Repaired by hand (steel lifted
to 0xe8edf0, a proud collar added at the seam). The 2026-07-26 run hit the same
ceiling and shipped the `frame_balance` gate for its lower-zone half.

Assessed for a bounded gate this run and NOT taken: a check that a declared
two-material hero shows two separable value populations in the rendered region
needs a declaration of which region and which two materials, i.e. a new slide
contract plus a clustering threshold calibrated across the whole 170-slide
corpus. That is a redesign, not a bounded upgrade. Recommendation recorded
below rather than coded.

### D5. A Phase 5 gate under-reads its own field

`scripts/dossier_check.py` (as shipped before this retro, line 77) walks
continuation lines with
`for line in body[m.end():].splitlines()`. `m.end()` sits at the end of the
matched 4a line, so the slice starts with a newline and `splitlines()[0]` is the
empty string, which trips the `if not s: break` guard immediately. The gate
therefore reads only field 4a's FIRST LINE.

Measured on this run's storyboard: the nine field-4a paragraphs run 400 to 900
characters each, of which the checker saw 120, 148, 46, 166, 45, 171, 183, 176
and 178. Two dossiers (03, 05) satisfied it on a 45-character fragment. The
authoring distortion is visible in the file: all nine fields were rewritten to
LEAD with modeled-tone words, leaving dangling markdown mid-sentence
("It is a modeled evidence" / "shelf**:" in slide 04). A dossier whose bottom
band becomes furniture from line 2 onward is invisible to it.

### D6. A shell short-circuit silently skipped a whole fix script

`cd out/2026-07-29/slides && python3 ...` failed the `cd` (the persistent cwd
had already moved) and `&&` swallowed the rest with no output, and the run
believed the script had run. Low value to gate, and CLAUDE.md already tells
agents to use absolute paths. Recorded, not actioned.

### D7. Environment, recorded and not yet enforced

- `getImageData` is pathologically slow in this headless build once a WebGL
  canvas has been composited: 34,118 ms for one `AKPOST.grade` call on slide 03.
  Worked around in-run by grading the 2D atmosphere BEFORE the GL composite.
  Documented in FIELD_NOTES, enforced nowhere.
- Slide 03 still takes about 38s to render against a 30s `renderReady` cap, and
  passes only because the cap covers `renderReady` and not total page time.
  Fragile, but tightening a timeout is a threshold change and is the
  maintainer's call, not this phase's.
- `shrink_pdfs.py` declined this run's PDF (images at 40.6 and 41.4 dB, under
  the 42 dB floor). Correct behaviour, honestly reported, no action.

### D8. The score of record cannot reflect a post-score repair

`post_score_remediation.score_after_fix` says it plainly: the 2-cycle cap was
already reached, so the six hard fails were repaired and verified by machine
gate and direct pixel review, but the number of record stays 6.9. This is the
policy working as written (Phase 10 caps cycles, and hard fails are never
shipped around), and the email discloses it. Noted so the maintainer knows the
6.9 in the daily email describes a deck that no longer exists on disk.

## Non-deviations worth recording

- `machine_qa.json` finishes at WARN with one warn: slide 02's `frame_balance`
  at 74 percent of the slide's own craft density. Below the FAIL line, disclosed.
- Every other gate is green from the artifacts, not from prose: render 9/9,
  `dossier_check` 9 dossiers 0 fails, `caption_check` PASS at 859 chars,
  `copy_sync` PASS at 119 strings, `scanner_sync` PASS, assemble 9 slides vector
  3.77 MB. `gate_status.py --require` exits 0.

## Frontier scan: typography craft (5 searches, 2 source reads)

Rotation slot chosen: typography and layout craft. It is the stalest craft slot
(last scanned 2026-07-20) and is distinct from the last four foci
(self-improving-pipeline 07-23, LinkedIn platform 07-24, accessibility and PDF
07-25, headless Chromium 07-26). It is also the slot this run's scar sits in:
the defect was type metrics.

What the sources say, and what it changed:

1. APPLIED. `getComputedTextLength()` returns only the horizontal ADVANCE of
   the text, glyph widths plus letter-spacing and word-spacing, ignoring `x`
   adjustments, so it yields no height and no anchor-correct origin.
   `getBBox()` returns the laid-out box in the element's own user space, which
   is what a plate has to contain. The new `AK.svgPlate` measures with getBBox
   for that reason, rather than with the advance the incident notes suggested.
   https://developer.mozilla.org/en-US/docs/Web/API/SVGTextContentElement
2. APPLIED. getBBox EXCLUDES stroke, and leading or trailing whitespace in an
   SVG text node corrupts its box in every engine. The helper adds half the
   computed stroke width back and console.errors on untrimmed content (which
   surfaces as a qa.py warn).
   https://bugzilla.mozilla.org/show_bug.cgi?id=1078743 and
   https://github.com/GoogleChrome/puppeteer/issues/814 (headless Chrome
   measures SVG text differently from desktop Chrome, which is harmless here
   because the same browser measures the label and screenshots the slide).
3. CORROBORATION. Measure-then-size with an explicit padding object is the
   settled dataviz practice for label backgrounds, not an invention: Victory
   exposes `backgroundPadding` as top/bottom/left/right, the standard D3 recipe
   reads `getBBox()` and adds padding, and the Vega-Lite legible-label-layout
   paper formalises label boxes plus padding with an occupancy bitmap for
   collision resolution. https://arxiv.org/html/2405.10953v1 and
   https://nearform.com/open-source/victory/docs/api/victory-label
4. PARKED. The occupancy-bitmap plus eight-position placement model from that
   paper is the principled answer to D3's knock-on churn (rasterise the marks,
   test eight candidate positions per label, place in the first free one, skip
   with graceful degradation). It is real machinery, roughly 150 lines over the
   existing render, but it changes how slides are composed and needs a
   multi-deck trial, so it is parked rather than forced into a daily slot.
5. PARKED. SVG `textLength` with `lengthAdjust="spacingAndGlyphs"` is the
   complement of the helper shipped today: it fits the TEXT to a fixed box
   instead of the box to the text, for the case where the plate geometry is
   load-bearing (a cadastral parcel, a rail tick). Chrome supports it on
   `tspan`, Firefox does not, which is irrelevant to this engine.
   `spacing` alone can collide glyphs, so `spacingAndGlyphs` is the safe value.
   https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/text
6. PARKED, craft note. 2026 editorial typography is running monospace as a
   deliberate editorial voice (precision, lab-form, dosage-chart register)
   rather than as a code signal, which is exactly the register this deck's
   JetBrains Mono furniture already uses; and optical-size axes open tracking
   automatically at small sizes, where our all-caps mono labels are hand-tracked
   at a flat 0.08 to 0.12em. Worth a controlled comparison on a future deck.
7. NOT PURSUED. `text-box-trim` / `text-box-edge` (Chrome 133+, Safari 18.2+,
   still not Firefox) would make plate padding exact by trimming the leading
   half-band. It was already parked on 2026-07-26 for the same reason it is
   parked now: it re-tunes vertical rhythm deck-wide.

Scan outcome: applied inside upgrade 2, plus three parked candidates recorded
in the ledger `scan_log` entry.

## Upgrades chosen this run

Three, reactive-first, the maximum the phase allows:

1. FIX, logged only: the SVG plate containment gate the showrunner shipped
   in-run (D1). Already implemented and verified; this phase records it in
   `ledger/upgrades.json` so it appears in the dated email and can be reverted
   as a named change.
2. FIX: `AK.svgPlate` / `AK.svgPlateAll` in `assets/js/aktype.js`, which sizes a
   knockout plate from the measured text box and inserts it as the text's
   preceding sibling. D1's arithmetic becomes unreachable at authoring time
   instead of merely detectable after render.
3. FIX: `scripts/dossier_check.py` reads the WHOLE of field 4a (D5), with the
   thin-plan floor raised to match the larger text it can now see, and breather
   detection deliberately left on the first line so the escape hatch cannot
   widen.

## Recommendations for the maintainer (not coded)

- D4: gating "a declared two-material hero renders as two separable value
  populations" requires a new slide-contract declaration and corpus-wide
  calibration. Worth a dedicated dev session, not a Phase 12 slot.
- D7: slide 03 renders in about 38s against a 30s `renderReady` cap. Either the
  cap should cover total page time or the deck should stop grading after a GL
  composite. Changing a timeout is a threshold call and is yours.
