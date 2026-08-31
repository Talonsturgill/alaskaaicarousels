# AUTOMATION RETRO - Run No.46, 2026-08-31

Phase 12, written after the merge and before the Gmail draft. Section 1 walks
`out/2026-08-31/run_state.json` and the run's artifacts against
`prompts/routine_instructions.md`. Section 2 logs the frontier scan. Section 3
records what was changed, what was refused, and what was parked.

Run headline: 9 slides, vector PDF 8.47 MB, scored 7.79 against the 7.7
iteration-ladder threshold, zero hard fails, `gate_status` 17 rows and 0 FAIL.
It does NOT clear the standing 8.3 and the email says so.

---

## 1. REACTIVE RETRO: deviations, with evidence

### D1. A gate passed a defect a human found by cropping the render (SEVERE)

Slide 03's printed claim is that the FCC asked EIGHT consecutive questions
about AI. The slide declared eight proud leaves, drew eight, and shipped SIX
until a human cropped the render and counted by eye. The body copy's type
reserve was clipping the two leftmost.

Evidence: `render_report.json` slide-03 asserts
`{"what": "eight consecutive AI questions, one proud leaf each", "expect": 8,
"actual": 8, "points_n": 8, "offframe": 0}`. It read 8 of 8 the whole time.

Cause, exactly: the 2026-08-25 count contract counts CENTRES INSIDE THE FRAME.
`RES()` applies the reserve as an evenodd canvas clip, and a clip erases ink
without moving a coordinate, so the arithmetic can never see it. This is the
same shape as the 2026-08-25 motif loss (drawn, then buried) and the 2026-08-30
one-axis projection (valid call, wrong picture): the code is right and the
picture is wrong, and every instrument was pointed at the code.

Nearly-shipped severity: the deck's Story-art fusion score cites "eight proud
leaves for eight consecutive AI questions" as evidence the art encodes the
story. Had it shipped at six, the deck's own strongest claim would have been
false in the frame on the slide that prints it.

**Owned by this phase. Fixed. See section 3.**

### D2. The five-round cap was exceeded by a factor of two

`run_state.rounds_note`: "Editing rounds far exceeded the five-round cap.
Rounds 1 to 7 were contact shadows and type reflow; round 8 was the two
critics' consolidated findings; rounds 9 and 10 were the scorer's work order."

Ten rounds against an AUTHORITATIVE cap of five
(`routine_instructions.md` Phase 8, 2026-08-26, owner). Disclosed in the email,
which is right, and the cap still says "ship what is on disk" at five.

This is a genuine, standing conflict between two authoritative rules and it is
NOT a Phase 12 change:

- Phase 8's cap: at five rounds, ship as-is and log the rest as known
  shortfalls.
- CLAUDE.md's LOW SCORE IS A WORK ORDER (2026-08-15, owner): a below-threshold
  score means go back to Phase 8 and fix the named defects, repeat until it
  clears.

A run that scores under threshold at round five is told to stop and told to
continue by two owner-level rules. This run resolved it by continuing, which is
the choice that ships a deck, and then the ladder relaxed the threshold to 7.7
so it "cleared" at round ten. Either rule could be adjusted; both are the
maintainer's call and adjusting either from here would be weakening a rule.
Recommended in the email, not changed.

### D3. The date gate reads copy.json and not the render

The scorer flagged slide 01's provenance stamp
`FEDERAL REGISTER VOL 91 NO 167 . AUGUST 31, 2026` as a house date-rule breach.
It is not one: `config/brand.yaml` blesses the plain form with a year and
separately blesses provenance stamps in a source list, and the string is both.

Two real defects underneath, evidenced:

1. CLAUDE.md's own date sentence states the ordinal rule and carries no stamp
   exemption, so a careful reader reaches the opposite conclusion, which is
   what the scorer did. The two blessings sit far apart in brand.yaml.
2. `caption_check.py` reads copy.json's fields. `copy.json["slides"]` carries
   `headline` and `claim_ids` and nothing else (verified: 9 entries, 2 keys
   each), so NO gate reads a rendered mono stamp. A real date breach printed in
   slide furniture would have shipped unseen. The false positive cost a scoring
   paragraph; a false negative would cost a house rule.

Recommended, not changed. Fixing (1) means editing CLAUDE.md, which this agent
does not do on an agent's instruction; fixing (2) is a second new gate in one
phase and loses to D1 on the reactive-first ordering.

### D4. copy_sync_check has only nine strings to check

`gate_status` row: "copy_sync_check: PASS -- 9 authored slide strings all
present in the render". Nine, for a nine-slide deck: one headline each.

`copy_sync_check.py` already accepts kicker, body, labels and chips; the gap is
upstream, in what Phase 6 authors. Every other on-slide string in this deck
(kickers, body prose, mono citation stamps, footers, tags) has no authored
source of truth, which is why the storyboard's BUILD RECONCILIATION drifted
against five shipped strings and had to be corrected by hand at the end, and
why the scorer could still find stale declarations in `aggregate_report`
("Deliverable completeness", 8/10).

The checker does not need changing. The COPY CHAMBER's output contract does,
and that change reaches Phase 6, SLIDE_DOSSIER_SPEC and every downstream
consumer. Too large for a bounded upgrade; recommended in the email.

### D5. bespoke_check reads the shared preamble (the question Phase 10 deferred)

Adding one helper to the build's shared JS preamble moved the median pairwise
art similarity from 0.517 to 0.591 against a 0.60 fail line, with no change to
any slide's own art; moving four comment blocks out took it back to 0.538. The
run correctly refused to touch the gate mid-run and left the decision here.

**Decided on the merits: NO. The preamble stays inside what the gate reads.**
Measured this phase: the block before `window.renderReady` is 39 to 56 percent
of each slide's art code, and stripping it takes the median from 0.538 to 0.110
and the worst pair from 0.641 to 0.226. That is the argument against it, not
for it. A strip list for "the shared preamble" would hide half of every slide
from the gate, and the defect this gate exists for (run No.26) was one build
script whose nine frames called the same six drawing functions with different
arguments. Such a deck would pass at 0.110 by moving its six functions above
`renderReady`. The strip list can only hold FIXED house furniture.

Written up with the numbers in knowledge/FIELD_NOTES.md. A non-weakening
alternative, printing both figures and gating on the existing one, is available
to any future run that wants it.

### D6. Environment, retries, fallbacks

Nothing to report, which is worth recording. No install failure, no fetch
failure, no API limit, no degraded fallback in the run record: PDF is vector
not raster, `site_signoff` PASS on 91 pages and 18 checks, gas watch PASS with
26 days on record and no gaps, `site_fresh` says docs/ is exactly a fresh
build, `dossier_check` 9/9 with 0 fails. The one engine breakage of the run
(assemble globbing the new `slide-NN.canvas.png` diagnostic layers and
assembling eighteen pages) was caught by `gate_status`'s assemble row and fixed
inside the run, and is already in the ledger.

### D7. Not deviations, recorded so they are not re-litigated

- The date roll (wake at 2026-08-30 23:19 AKDT, run dated 2026-08-31) follows
  the routine's stated date rule and touched no shipped artifact.
- 43 machine_qa warns and 0 fails, of which 38 are tiny-text at 20 to 21px
  against the 24px mobile floor. Declared in `known_unfixed` with the reason
  (24px overruns the safe zone on the longest strings). A standing craft debt,
  not a run deviation.
- Two mono stamps at exactly 4.5:1 worst-point contrast. Passing with nothing
  in reserve, and flagged to the maintainer in the email. Correct behaviour.

---

## 2. FRONTIER SCAN

**Focus: (d) typography and layout craft.** The stalest legal slot, last
scanned 2026-08-20 (11 days), and distinct from the last three logged foci
(2026-08-30 agent workflows, 2026-08-29 editorial dataviz, 2026-08-27
accessibility/PDF). Relevant as well as stale: rounds 1 to 7 of this run were
contact shadows and TYPE REFLOW, the worst defect of the run was a TYPE RESERVE
erasing artwork, and 38 of 43 machine warns are type below the mobile floor.

Six searches, two substantive reads, and one experiment run in the engine's own
browser rather than a claim taken on trust.

**THE FINDING, measured locally.** `text-box-trim` / `text-box-edge` (Chrome
133+, February 2025) is supported by the browser this engine actually renders
in. Probed through `render.launch_chromium`, Chromium 141.0.7390.37:
`CSS.supports('text-box-trim','trim-both')` true, and a 60px/2 serif line
measures `getBoundingClientRect().height` 120.0px untrimmed against 39.3px with
`text-box: trim-both cap alphabetic`. Eighty pixels of that box is half-leading
belonging to nobody. `measureReserve()` builds the type reserve out of exactly
that box plus a 12/8 pad and applies it as an evenodd CLIP, so every pixel of
half-leading is a pixel of artwork the slide is forbidden to draw.
https://developer.chrome.com/blog/css-text-box-trim

PARKED, not applied. Trimming the boxes moves every flowed element on every
slide at once, because `flow()` positions each block off the previous block's
bottom edge and those gaps are hand-tuned against the untrimmed box. That is a
redesign of the layout contract with a full re-render and re-review behind it,
which is not a Phase 12 change. Unblocking condition written into FIELD_NOTES.

Two smaller results, both worth not rediscovering:

- `hanging-punctuation` is NOT supported in Chromium 141 (`CSS.supports` false;
  Safari-only). Optical margin alignment on the deck's opening quotation marks
  needs a manual negative text-indent; there is no property to reach for.
  `text-wrap: pretty` and `text-spacing-trim` both ARE supported.
- Chromium's `text-wrap: pretty` prevents last-line orphans only; Safari's
  implementation improves the whole rag. DESIGN_DOCTRINE is already correct
  that it gives no line-count guarantee and can't replace `AK.fitText`, but it
  is free and additive on the free-flowing `.bd` blocks, which are not
  fitText'd today.
  https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/
- Tracking for all-caps small labels: +5 to +10 percent, and 3 to 5 percent for
  10 to 12px labels. Nothing here the doctrine does not already carry, and
  nothing that reaches the 24px-floor problem, which is a safe-zone width
  problem and not a tracking problem.

Outcome: nothing applied from the scan. The one upgrade slot went to the
reactive fix, which is this phase's reactive-first rule working as written.

---

## 3. UPGRADES

Budget: 0 to 3 per run. Two were already spent inside this run and are
committed (`scripts/value_structure.py`, report-only; and the `assemble.py`
canvas-layer glob fix). **One slot remained and one upgrade was made.**

### Applied: the declared-mark visibility check (fix, engine)

A count assertion's declared centres are now probed on the COMPOSITED png, and
qa.py FAILS when a mark carries no ink where the slide says it drew one. This
closes D1.

Design, in the house shape:

- render.py exports the mark centres (`points_xy`), capped at 240 with an even
  stride, so a 750-mark census costs a bounded amount of report and the sample
  spreads over the whole field.
- qa.py measures `_ink_spread` at each centre, on ONE implementation shared
  with the motif gate rather than a second one written in JS. The probe box is
  half the cohort's median nearest-neighbour distance, clamped to 4 to 14
  design px, so the probe is always about the size of the thing it looks for.
- The verdict is a RATIO inside the assertion's own cohort. Every mark in one
  assertion is by construction the same kind of mark, so the cohort is its own
  control group and the check needs no absolute ink threshold and no idea of
  what the mark depicts. A scrim over half the field cancels out.

Calibration, from measurement and not from a guess:

| corpus | result |
| --- | --- |
| run No.46's 3 real cohorts, 74 marks, all human-verified present | ratio median 1.00, p10 0.96 to 0.99, worst single mark 0.56 |
| the 750-mark fixture in tests/count_assert_verify.py | silent, no false positive on a strided census |
| slide 03's defect reconstruction (reserve widened over 2 leaves) | 0.078 and 0.074 |

FAIL line 0.30, between a worst known-good of 0.56 and a worst defect of 0.078.
A softer "being smothered" band at 0.55 was written first and then REMOVED: the
worst known-good mark lands on it and nothing in the corpus says a ratio
between 0.3 and 0.6 means anything. The check asks exactly one question.

Three ways it can miss, all false negatives, all written into SKILL.md: it asks
whether ANYTHING is at the centre and not whether the mark is; it resolves at
the mark pitch, so where marks are packed tighter than the box only a RUN of
losses shows; and a flat cohort is reported unmeasurable, never as 100 percent
lost, because marks drawn in the DOM look the same from here.

Verification, all of it run: the two known-good decks are byte-identical in
verdict before and after (this run's 9 slides 0 fails / 43 warns, demo-deck 0
fails / 11 warns, and every individual warn string unchanged); the real defect
reconstructs and FAILS naming both leaves at their coordinates; a second,
different erasure mechanism (an opaque DOM plate) also FAILS; a 65 percent
scrim over half a mark field stays silent; both 2026-08-25 gates still hold;
assemble still produces a 4-page vector PDF from demo-deck. A committed
reconstruction, `tests/mark_paints_verify.py`, carries all four cases so the
calibration survives this session.

### Refused

- **Do not add the per-deck preamble to bespoke_check's HARNESS strip list.**
  See D5. Refusing is the whole point: it would hide 39 to 56 percent of every
  slide from the gate.
- **Do not relax the five-round cap or the low-score work order.** See D2. Both
  are owner-level rules and the conflict between them is the maintainer's to
  resolve.

### Parked

- `text-box-trim` for the type reserve, with the local measurement, the reason
  it is a redesign, and its unblocking condition
  (knowledge/FIELD_NOTES.md, 2026-08-31 Phase 12 block).
- The `hanging-punctuation` and `text-wrap: pretty` support results, so the
  next run in this slot does not re-measure them.
- The bespoke_check decision with its numbers, including the non-weakening
  alternative.

### Recommended to the maintainer, not changed

1. Add the provenance-stamp exemption to CLAUDE.md's own date sentence, so it
   agrees with brand.yaml (D3).
2. Teach a date gate to read rendered slide furniture, not just copy.json (D3).
3. Have Phase 6 author every on-slide string, not only the headline;
   `copy_sync_check.py` is already built to check them (D4).
4. Resolve the five-round cap against the low-score work order (D2).
