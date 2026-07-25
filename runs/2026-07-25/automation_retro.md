# AUTOMATION RETRO -- run 2026-07-25, Carousel No. 17

"On File, Off Record. Alaska's AI Governor Race." 10 slides, light ground, new
MILLED REGISTER chassis (axonometric orthographic canvas plus one akthree GL
hero). Written by the upgrade-engineer in Phase 12, after the merge (4ea3e4b,
PR #100) and before the Gmail draft.

Method: walk `out/2026-07-25/run_state.json` phase by phase against
`prompts/routine_instructions.md`, with the artifacts open, then decide what
becomes permanent machinery. The showrunner's incident notes were input, not
the answer.

---

## 1. PHASE-BY-PHASE DIFF (actual vs the spec)

Every phase in run_state reads "done" through scoring, with artifact paths. The
deviations below are behavioural, not bookkeeping, unless stated.

### Phase 0 WAKE -- clean
carousel_no 17 = topics.json entries + 1 (17 entries, one dated 2026-07-25).
Variance dials, variety constraints and seasonal notes are in plan.md. Top-5
instincts were injected (they appear verbatim in the subagent prompts the run
recorded). No deviation.

### Phase 1 CRAFT REFRESH -- clean
4 searches (spec allows ~10), appended as a dated FIELD_NOTES entry. No
doctrine file touched during the run. No deviation.

### Phase 2 RESEARCH -- clean
6 scouts, one per beat, all returned (scout_findings.json). No deviation.

### Phase 3 CLAIMS -- clean, with environment breakage handled correctly
31 claims (1 derived), 13 rejected, 7 counter-framing points. Environment:
APOC and a state notice system returned 503, akleg 403, gvea.com 403, and a
partisan outlet's page 404'd, which killed the intended centerpiece. The
fact-checker REJECTED the affected claim rather than softening it, which is the
behaviour the spec asks for ("Never fabricate"). No machine fix available: these
are third-party outages behind WebFetch. **Verdict: correct degraded behaviour,
disclosed in run_state.**

### Phase 3.5 DOCKET -- clean
Refresh only (3 items), no new item, because HCR 3 / HB 259 status was
unverifiable (akleg 403) and AIDEA plus STAK notices were 503. Style-linted
pre-flight per the 2026-07-09/10 lesson. Honest "refresh only" note in
run_state. No deviation.

### Phase 4 SELECTION + DEDUPE -- clean, and the 07-23/07-24 fixes worked
`dedupe_check.py` exit 0, no LIKELY DUPLICATE, strongest match No.14 soft 0.022
with 0 shared entities, and run_state records that the output was **read in
full** (the 2026-07-24 tail-truncation scar). The two dedupe upgrades from the
last two runs are behaving as designed. No deviation.

### Phase 5 DIRECTORS ROOM -- one process deviation
3 treatment-directors, storyboard written to spec, and the storyboard gate ran.
DEVIATION D1: slide 02's dossier carried risk flag (b), which PREDICTED IN
WRITING that qa.py's DOM-only collision gate could not see canvas geometry
crossing art-band labels. The deck was then built with unplated art-band labels
anyway, and the predicted defect happened on four slides. A risk flag was
recorded without a mitigation, and nothing in the storyboard gate requires one.
Evidence: storyboard.md slide-02 dossier risk flags; score_report.json
`post_cycle2_fixes.root_cause` ("This run's own slide 02 dossier predicted it in
risk flag (b) and the prediction came true on four slides across two cycles").

### Phase 6 COPY CHAMBER -- clean
2 caption directors, 1 caption critic, 1 copywriter; caption_check PASS at 874
chars; copy_sync_check PASS; style_lint clean; caption_meta present. The caption
critic independently caught the same overstatement ("million dollar hauls") the
build caught on slide 07, which is the room working as designed. No deviation.

### Phase 7 ART BUILD -- the run's root defect, and one gate that worked
DEVIATION D2 (the big one). **qa.py's collision gate is DOM-only and its only
pixel-level tripwire was size-gated to primary text (font_px >= 30), so the
24px art-band mono labels of this deck were never sampled at all.** Four slides
shipped labels whose glyphs were crossed by canvas-drawn groove edges, scored
slot outlines and leader rules, and machine QA returned PASS with 0 warns
across TWO scoring cycles. Human and critic eyes caught it; the machine never
did. Evidence: score_report.json `cap_reason` (two hard fails, slides 02, 03,
07, 09) and `post_cycle2_fixes.root_cause`; instincts.json top entry at 0.97;
machine_qa.json PASS 0/0 at every cycle. The in-run fix was structural but
LOCAL to this run's generator (`L()` in build_slides.py now defaults
`plate=True`), so run No. 18 would have started blind again.
Per the top instinct of this run: a gate passing is not evidence the thing it
names is correct, and a defect a critic catches that a gate missed is a gate
bug. **This is the reactive fix of record (UPGRADE 1).**

Gate that worked: the 24px mobile floor caught the planned 22px mono labels and
20px chips; both were raised to 24px (storyboard BUILD RECONCILIATION item 9).
No action.

Gate that worked: the `.display` CSS rule shipped without `position:absolute`,
so six headlines collapsed to 0,0 and overprinted their kickers; `text_collisions`
FAILED six slides at once and the bug was fixed in minutes (BUILD RECONCILIATION
item 12). This is exactly the defect class the DOM gate is good at, and it is
the reason the DOM gate is not being replaced, only complemented.

DEVIATION D3: a whole class of canvas-geometry SEMANTIC defects was caught only
by eye, and no gate can see any of them: a recess drawn without clipping to its
opening polygon read as a RAISED BLOCK and inverted the deck's cut/proud state
machine (three pixel critics independently reported "reads proud"); the well lip
lit on the far edge made cuts read as rims; gold #FFC72C drawn before
`AKPOST.grade` came out acid yellow-green because ACES pushed it; `scene.background
= null` in akthree cleared to OPAQUE BLACK so the GL hero rendered as a black
frame on a bone deck; GL bay walls built with swapped width/height rendered as
tall standing slabs; and a mark placed at recess depth projects about 56 px lower
than the same coordinates at depth 0, so fireweed and gold marks near the near
edge were silently clipped away by the opening clip.
Assessment: these are not one gate's blindness, they are four different kinds of
thing. Two are API traps that a library default could close forever (the
akthree transparent-clear trap, the gold-before-grade trap) and are PARKED with
concrete parameters rather than rushed into the shared GPU path this run. Two
are projection footguns that belong in the knowledge base (depth-projection
offset, opening-clip interaction). Two were plain coding errors caught by the
critics doing their job.

### Phase 8 PIXEL REVIEW -- two process deviations
DEVIATION D4: the 4 pixel critics were spawned BEFORE the storyboard's BUILD
RECONCILIATION section existed, so roughly a third of their findings measured
the renders against superseded numbers (old azimuth, old slab thickness, old
label sizes). Logged as an instinct at 0.88. Evidence: instincts.json
2026-07-25 entry 4; storyboard.md BUILD RECONCILIATION exists only as an
appended section.
DEVIATION D5 (not in the incident notes): **the critic fan-out was UNDER the
planned set.** The spec fixes pixel-critics at "one per 1 to 2 slides"; a
10-slide deck therefore plans 5 to 10 critics and this run spawned 4 (2.5
slides each). Evidence: run_state.json `artifacts.pixel_review` ("4 pixel
critics over 10 slides"). NON-NEGOTIABLE 7 is a cap on over-spawning, not a
licence to under-spawn: with D4 in the same phase, the taste gate ran both thin
and early, which is a plausible contributor to four label collisions surviving
to the scorer.
Gate that worked: RECORD-SYNC pre-flight (`copy_sync_check.py`) PASSed and the
2026-07-17 stale-copy class did not recur.

### Phase 9 FINAL ASSEMBLY -- clean
Vector PDF, 10 pages, 4.87 MB (in the 2 to 25 band), thumbs and contact sheet
present; assemble_report.json consistent with the render. No deviation.

### Phase 10 SCORING -- one honest spec collision
Raw weighted 8.22 against the 8.0 ladder threshold, capped to 6.9 by two hard
fails from D2. DEVIATION D6, structural rather than anyone's error: the spec
says "Max 2 scoring cycles" AND "Any HARD FAIL: fix it no matter what". When a
hard fail appears AT cycle 2 those two rules collide, and the run resolved it
the honest way: it fixed every instance and recorded that the repair was
self-verified by reading the renders and 432px thumbs, NOT by a third scorer
pass. Evidence: score_report.json `post_cycle2_fixes.note`. This is a rubric
policy question (a verify-only re-score that does not consume a cycle would
close it) and therefore a MAINTAINER decision, not something Phase 12 may
change: it touches the scoring ladder. Recommended in the email, not coded.

### Phase 11 SHIP -- one artifact-vs-reality deviation, one false flag
DEVIATION D7: the first hand-written BUILD RECONCILIATION gate block claimed
"qa.py PASS, zero warns" while machine_qa.json on disk said WARN with 5. The
scorer caught the contradiction; the showrunner then generated the block from
the artifacts. A human sentence stood in for an artifact, in the one document
whose purpose is to prevent record drift. The same section also carries a
"Correction to item 6 above" for a second factual slip about where c5/c6
shipped. **UPGRADE 2 makes that block machine-generated.**
DEVIATION D8: the showrunner's completion gate false-flagged a VALID
`caption_report.json` because it tested the file against a 200-byte size
threshold and the valid file is 196 bytes. Fixed in-run by parsing the JSON
instead of measuring it. Any artifact check that measures bytes instead of
parsing is the same bug waiting to happen. Folded into UPGRADE 2, which parses
JSON and checks binaries by magic bytes, never by size.
DEVIATION D9 (minor, record hygiene): the shipped `runs/2026-07-25/run_state.json`
records `ship`, `upgrade`, `gmail`, `retro` as "pending", because the completion
gate necessarily runs before those phases finish and the file is committed at
that moment. The shipped record therefore contradicts the merge that happened
(4ea3e4b). Phase 14 says "Mark run_state complete", so the fix is to re-copy
run_state.json into runs/<date>/ in the Phase 13/14 amend commit. Recommended,
not coded (prose-level, and the shipped copy is not load-bearing for any gate).
DEVIATION D10 (minor, ledger discipline): Phase 11 step 4 asks for 1 to 3 new
instincts; this run appended 5 (confidences 0.97, 0.95, 0.92, 0.88, 0.82).
Evidence: ledger/instincts.json. All five are good, which is exactly why the
cap exists (an unbounded instinct list dilutes the top-5 injection). No code
change; noted for the next wake.

### Phase 12 UPGRADE -- this document
### Phases 13/14 -- pending at the time of writing

---

## 2. WHAT THE DEVIATIONS ADD UP TO

Ranked by how close each came to shipping a public defect:

1. **D2, the DOM-only / size-gated art-under-text blindness.** It DID ship
   defects into two scoring cycles and it capped the deck at 6.9. Only the
   generator's local `plate=True` default stood between run No. 18 and the same
   blindness. Highest-value reactive fix available. -> UPGRADE 1.
2. **D7 + D8, the record-vs-artifact class.** A gate artifact was contradicted
   by a hand-written sentence, and a valid artifact was rejected by a byte
   count. Both are one small script's worth of work, and the same script closes
   part of D4 by making the pre-critics reconciliation cheap to produce. ->
   UPGRADE 2.
3. **D4 + D5, the pixel-review process.** Ordering is now a hard step in the
   prompt alongside UPGRADE 2's command (a machine precondition would require
   the showrunner's own tooling to gate agent spawning, which this phase cannot
   build safely in one run). The under-spawn (D5) is a discipline item for the
   showrunner: 10 slides means 5 to 10 critics.
4. **D1 and D3**, the risk-flag-without-mitigation habit and the canvas-semantic
   defect class. D1 is the more interesting one: this run WROTE DOWN the exact
   failure it then shipped. UPGRADE 1 converts that specific prediction into a
   gate, which is the durable answer; a general "every risk flag names a
   verifiable mitigation" rule for the storyboard gate is recommended for the
   next prompt pass.
5. **D6, D9, D10**: maintainer call, record hygiene, ledger discipline. Written
   up, not coded.

---

## 3. FRONTIER SCAN (focus: accessibility and PDF/document-format)

Rotation: the last three foci were LinkedIn platform (2026-07-24),
self-improving-pipeline patterns (2026-07-23) and editorial dataviz/cartography
(2026-07-22). Accessibility/PDF was the stalest slot (last scanned 2026-07-12)
and it is directly adjacent to this run's scar, which is a legibility defect.
6 searches, 3 substantive sources read in full.

Findings:

- **Worst-case, not average, is the correct way to measure text over art.**
  NN/g's text-over-images guidance is explicit that the solution must hold for
  "the worst-case background image and text placement", and the remedy ladder is
  scrim -> semi-opaque box behind the text -> halo/outline, with 4.5:1 (3:1 for
  large text) still the operative ratio. This CORROBORATES the design of
  UPGRADE 1, which measures the ring immediately around the glyphs (worst case,
  locally) rather than a box-wide average, and whose failure message names the
  same three remedies. It also identifies a real remaining weakness in
  `contrast_estimate()`: it takes a bbox-wide median background, so a dark rule
  crossing part of a label is averaged away. PARKED (see below) because a
  worst-case-window contrast tightening needs multi-deck calibration before it
  can be trusted not to flood.
  https://www.nngroup.com/articles/text-over-images/ ,
  https://webaim.org/articles/contrast/
- **WCAG 3 / APCA is still not a threshold source.** As of April 2026 the WCAG 3
  draft says the contrast algorithm "is yet to be determined"; APCA was pulled
  from the draft in 2023 and remains exploratory, and WCAG 2.2 AA is the
  operative standard (finalisation estimates 2029 to 2030). The studio's
  WCAG2-style ratios in qa.py stay correct; no change, and no reason to revisit
  this for a year.
  https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html
- **LinkedIn destroys PDF semantics on document posts.** Screen-reader testing
  reports that a document post's text is effectively OCR'd: heading levels are
  picked up only partially, alt text is acknowledged but not read out, list tags
  and reading order are lost, and there is no per-slide alt-text field for a
  multi-page PDF upload. So tagging our PDF buys nothing ON PLATFORM; its value
  is for the artifact people download from the site and the email.
  https://intopia.digital/articles/navigating-the-accessibility-challenges-of-linkedin-carousels/
- **Tagged PDF is now one keyword away in our stack, but not one keyword away in
  our pipeline.** Playwright 1.61's `page.pdf()` accepts `tagged=True` (verified
  by inspecting the installed signature: `outline` and `tagged` are both
  present), and Chromium has emitted tagged PDFs since Chrome 85. But
  assemble.py prints ten single-page PDFs and merges them with pypdf, and a
  page-level merge does not carry a `/StructTreeRoot`, so the merged deck would
  claim nothing and prove nothing. PARKED with the specifics.
  https://pdfa.org/chrome-plated-pdfs-exploring-google-chromes-new-pdf-capabilities/
- PDF/UA-1 remains the practical conformance target in 2026 (validators support
  it; PDF/UA-2 tooling is still catching up), and the EAA's June 2025 in-force
  date matters for customer-facing documents. Context only: nothing in this
  studio's deliverables is in scope, and no change is warranted.

Outcome: nothing applied from the scan. Two items parked as dated
knowledge/FIELD_NOTES candidates with source URLs; one item (WCAG3/APCA)
reconfirmed existing practice.

---

## 4. UPGRADES MADE (2, both kind="fix", reactive)

### UPGRADE 1 -- qa.py sees a label crossed by art, and FAILS
`.claude/skills/carousel-engine/qa.py` gains `glyph_ink_contamination()` plus
its wiring, and `busy_art_under_text()` loses its `font_px >= 30` restriction.
The new check samples a thin ring around every non-decorative label's glyph ink
(skipping 2px of anti-aliasing, out to 5px) and counts ring pixels that are
closer to the GLYPH's own value than to the local paper value. It FAILS when
that contaminated fraction is >= 0.07 AND the contamination spans >= 30% of the
label's columns or rows; it WARNs from 0.02. `data-overlap-ok` demotes the FAIL
to a WARN, as with the DOM collision gate.

Why this metric and not "busy background": it measures the DEFENCE, not the
busyness. A knockout plate, a dark-ground scrim or a halo leaves the ring clean
(a halo is the OPPOSITE value by construction, so it cannot trip the gate),
while a rule, outline, groove edge or specular highlight running through the
letterforms puts ink of the glyphs' own value hard against them, all the way
across the label. That is what separates this run's defect from legitimate
art-band typography, which is why the busy-art tripwire could only ever WARN.

Verification, all in scratch dirs (nothing shipped was modified):
- DEFECT RECONSTRUCTION: `out/2026-07-25/build_slides.py` copied with `L()`'s
  `plate` default flipped back to False, regenerating this deck's plate-less
  labels over the same tuned geometry, then rendered. Confirmed genuine by eye:
  TREG TAYLOR, ADAM CRUM and MEDA DEWITT are struck through by their scored slot
  outlines and THE RECORD STOPS HERE crosses the near-black incision.
  Old qa.py on that render: **PASS, 0 fails, 0 warns** (the blindness,
  reproduced). New qa.py: **FAIL, 4 fails, exit 1** on slides 03 and 07, the
  same slides the scorer hard-failed (contamination 12%/9%/9%/8% spanning
  62%/60%/60%/60%), plus a 2% WARN on slide 02's "Six Anthropic employees".
- THIS RUN'S SHIPPED SLIDES: render 10/10 OK, new qa.py **PASS, 0 fails,
  0 warns**, byte-identical verdict to the shipped machine_qa.json. Zero new
  noise on a deck that solved the problem structurally: the knockout plates put
  every measured ring at 0.000 contamination.
- examples/demo-deck: render 4/4 OK, **0 fails**, verdict WARN, exit 0
  (unchanged verdict). Warns went 1 -> 9, all genuine and all now visible:
  ANCHORAGE over the cartography at 3%, the demo-03 headline over the flow field
  at 6% (correctly below the FAIL line, and it is haloed-adjacent editorial
  work, not a strike-through), and the small page markers over art that the old
  size gate never sampled.
- examples/proof-3d (extra corpus): the new gate found a REAL defect the old one
  could not see. Slide 03's body copy sits over the GL hero's gold column and
  its specular ran through the letterforms (11% of the ring, spanning 100% of
  the label). Old qa.py on the same render: PASS 0/0. Fixed the slide with the
  remedy the gate names, a `.dekscrim` plate at rgba(3,6,13,.84) behind the
  copy (measured: beacon luminance under the copy drops from 116.6 to 47.4
  mean), and proof-3d is back to **PASS 0 fails 0 warns** under both the old
  and the new gate.
- Margin analysis: shipped deck max contamination 0.000; demo-deck max 0.056;
  reconstruction defects 0.083 to 0.118 with extents 0.60 to 0.62 against demo's
  0.50 to 0.65 extents but far lower fractions. The FAIL line at 0.07 x 0.30 sits
  between the corpora on the fraction axis. It is a tightening, never a
  loosening: no existing gate, threshold or hard-fail rule was touched.
- Runtime cost: qa.py over 10 slides 4.6s (was ~3.5s). No new dependency
  (numpy/PIL already required by qa.py).

Documented in SKILL.md as a slide-contract rule, because the fix an author
reaches for must be in the contract: text over art needs a declared defense.

### UPGRADE 2 -- scripts/gate_status.py, the gate block no human writes
New read-only stdlib script that prints the run's GATE STATUS block straight
from the artifacts: render_report.json, machine_qa.json, caption_report.json,
copy.json via copy_sync_check, assemble_report.json (plus a magic-byte check on
carousel.pdf), score_report.json (the scorer's own numbers, never re-derived),
and a presence-and-parse sweep of the artifact set. JSON is PARSED, never
measured; binaries are checked by magic bytes. Exit 1 on any FAIL row; with
`--require` (the ship gate) a missing or unparseable artifact is a FAIL. Works
on both the nested `out/<date>/` layout and the flat `runs/<date>/` copy.

Wired into the prompt in two places: Phase 8 gains step 1b, which makes
"reconcile the storyboard, generate the gate lines from the artifacts, THEN
spawn pixel critics" a hard ordering (D4), and Phase 11 step 5 adds
`--require` to the completion gate (D8).

Verification:
- On this run's real artifacts: every row matches the artifacts exactly, and
  the honest 6.9 cap renders as a WARN row quoting the scorer's own cap_reason
  rather than as a pass claim. Exit 0. Also correct on `runs/2026-07-25/`
  (flat layout), where the absent render_report is reported as n/a rather than
  guessed.
- D7 RECONSTRUCTION: a scratch copy of the run dir with machine_qa.json set to
  verdict WARN / warns 5 prints `[WARN] qa.py WARN, 0 fails, 5 warns`. The
  sentence "qa.py PASS, zero warns" is no longer possible to produce from the
  block.
- D8 RECONSTRUCTION: the real 196-byte valid caption_report.json passes (the
  in-run false flag cannot recur), while a 394-byte TRUNCATED caption_report
  (which any ">200 bytes" size threshold would accept) is caught as
  "unparseable (JSONDecodeError)" and FAILs the ship gate at exit 1. Same for
  binaries: a 5 MB file of zeros named carousel.pdf FAILs on bad magic, where a
  size threshold would have passed it.
- Missing artifacts: `--require` FAILs and exits 1 on a deleted carousel.pdf;
  without `--require` the same run reads n/a, so the tool is usable mid-run.
- ast.parse OK. Read-only (verified: the real run dir is unchanged after every
  invocation; all mutation tests ran on a scratch copy). Stdlib only.
- Engine untouched by this upgrade: this run's slides render OK + qa PASS 0/0
  and examples/demo-deck render OK + qa 0 fails, both re-run after the change.

Not weakened anywhere: gate_status.py reports, it does not judge. A below-
threshold-but-honest score is a WARN row, so it can never block a disclosed
shortfall ship, and every FAIL row it can emit corresponds to an artifact that
is genuinely broken, missing or self-contradictory.

---

## 5. PARKED (promising, not safely boundable this run)

Written as dated candidates in knowledge/FIELD_NOTES.md with source URLs:

1. **Worst-case-window contrast for text over art.** Replace or complement
   `contrast_estimate()`'s bbox-wide median background with a per-window (say
   24px column) worst-case ratio, per NN/g's worst-case rule. Parked because it
   touches an existing FAIL threshold on every text node in every deck and needs
   a multi-deck calibration pass to prove it does not flood; UPGRADE 1 already
   covers the acute version of this defect.
2. **Tagged PDF for the downloadable artifact.** `page.pdf(tagged=True)` in
   Playwright 1.61 plus a merge path that preserves `/StructTreeRoot` (pypdf's
   page-level merge does not). Parked because the merge is the hard half and the
   platform payoff is zero (LinkedIn OCRs document posts); the payoff is the
   site/email download only.
3. **akthree transparent-clear default.** `AKT.setup` should create the
   WebGLRenderer with `alpha: true` and call `setClearAlpha(0)` when `opts.bg`
   is null, so a hero composited over a light deck cannot clear to opaque black
   (this run's GL hero did, and it was caught by eye). Parked deliberately: it
   changes the shared GPU path for every future deck and deserves its own run's
   verification budget rather than a third slot in this one.
4. **Gold-after-grade rule for akpost.** #FFC72C drawn before `AKPOST.grade`
   comes out acid yellow-green because ACES pushes it; the fix is to defer brand
   gold to a post-grade pass, or for akpost to expose a protected-swatch pass.
   Parked as doctrine plus a helper candidate.
5. **Depth-projection footgun.** In an axonometric chassis, a mark at recess
   depth projects about 56 px lower than the same coordinates at depth 0, so
   marks near a recess's near edge get silently clipped away by the opening
   clip. Parked as a TECHNIQUE_LIBRARY note candidate for the next non-run
   development session (it is chassis doctrine, not engine code).

## 6. RECOMMENDED TO THE MAINTAINER (not coded, on purpose)

- **A verify-only re-score that does not consume a scoring cycle** (D6). When a
  hard fail lands at cycle 2, today's rules force either an unverified repair or
  an abandoned run. This is a rubric change, so it is the maintainer's call;
  Phase 12 may not touch the scoring ladder.
- **Pixel-critic fan-out floor** (D5): 10 slides means 5 to 10 critics, not 4.
  Worth stating as a number in Phase 8 next time the prompt is edited.
- **Every storyboard risk flag names a verifiable mitigation** (D1). This run
  predicted its own defect in writing and shipped it anyway.
- **Planned-vs-shipped element reconciliation** (the scale bar, the three money
  wells, claim c26). copy_sync_check verifies STRINGS; the gap is planned
  ELEMENTS. The machinable version is a spec change: each dossier carries a
  machine-readable element id list, slides tag rendered elements with
  `data-element="id"`, and a checker diffs planned against rendered. That is a
  SLIDE_DOSSIER_SPEC plus authoring-contract change, too large for one Phase 12
  slot, and it should be designed once rather than half-built.

## 7. LEDGER

Both upgrades logged in ledger/upgrades.json with verification evidence and
rollback hints, plus one scan_log entry (focus: accessibility/PDF, outcome:
parked). Staged for a single `upgrade(2026-07-25):` commit so the set reverts
cleanly.
