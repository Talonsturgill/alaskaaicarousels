# AUTOMATION RETRO — run No.58, 2026-09-13

Phase 12, step 1. Written by the upgrade engineer against
`out/2026-09-13/run_state.json`, the run's incident notes and
`prompts/routine_instructions.md`. Three upgrades were made, all reactive; the
frontier scan's two findings are parked. The run shipped at 8.39 against a
threshold of 8.3.

## 0. THE STANDING REPEAT OFFENDER: DEFERRED, AND HERE IS WHY

`python scripts/trend_check.py --window 10` names **Artwork craft and genuine
detail** as the weakest criterion in 6 of the last 10 runs, mean 6.8, last 7.0,
last worked on 2026-09-12 (one run ago). It is **DEFERRED AGAIN THIS RUN.** Not
silently, and not for lack of a candidate.

The candidate exists and is dated: the 2026-09-12 frontier scan parked weighted
sample elimination (Yuksel 2015) with its parameters read out of the reference
implementation, and Jobard and Lefer evenly spaced streamlines, precisely
because three of that run's six review rooms reported mote populations reading
as grain. That is the right instrument for this criterion and it is ready to be
built.

It is deferred because all three slots went to defects that each cost this run
build rounds or score, and two of the three are the SAME defect class the
scorer hard-failed:

- the canvas-through-DOM collision capped round one at 6.9 from an uncapped
  7.55, and no gate in this repo could see it;
- five body paragraphs shipped short of their dossier and were found by hand,
  one at a time, by three critics across two rounds;
- all nine display headlines broke against their own meaning in the first
  build, and the rule set that would have caught them has been parked since
  2026-09-07.

The phase rule is reactive-first, and a defect that capped a score outranks a
standing weakness that did not move this run (artwork craft scored 7, its
window mean).

**WHAT WOULD HAVE TO BE TRUE TO TAKE IT.** A run whose incident list costs one
slot or none. The work itself is bounded and already specified: an
`assets/js/` helper of about 100 lines of vanilla JS implementing weighted
sample elimination (2D r_max = sqrt(A / (2*sqrt(3)*N)), d_max = 2*r_max, weight
= sum of (1 - d/d_max)^8 over neighbours inside d_max, weight limit fraction
(1 - (N_out/N_in)^1.5)*0.65, uniform grid in place of the kd-tree at our
counts), plus a before-and-after fit on one real frame at 432px, plus a named
entry in TECHNIQUE_LIBRARY. It needs one slot and one frame, not a redesign.
Recommend it be the first slot of the next run whose incident list is short.

Two entries are marked STALE with `worked never`:

- **Legibility and platform fitness** (weakest 2 of 10, mean 6.7). NOT
  untouched in fact: the trend check matches on upgrade prose, and this run's
  three upgrades are all legibility machinery (type printed through type, copy
  that went missing, lines broken against sense). The row should move on its
  own next window; nothing extra is warranted for it this run.
- **Deliverable completeness** (weakest 1 of 10, mean 7.6, last 8.0). The
  frontier scan below landed directly on it and found two real defects in the
  shipped PDF. Both are parked with measurements, which is the honest state:
  they change the artifact and want their own gate.

## 1. DEVIATIONS, PHASE BY PHASE, WITH EVIDENCE

Read against `run_state.json` and the artifacts in `out/2026-09-13/`.

### 1.1 Pixel review and build reconciliation passed a defect the scorer caught (FIXED)

Evidence: `score_report.json.round_one` — "clipped, overlapping or cut-off text:
slide 02's rotated canvas axis label ran through the DOM unit guard, and slide
07's chisel crossed the motif label", capping 7.55 to 6.9.
`render/machine_qa.json` slide 02 — "leader label unverifiable: ... its POSITION
is not confirmed, because a canvas string has no line box." The gate said in its
own words that it could not look, the run recorded the repair as done in BUILD
RECONCILIATION, and the repair had put the DOM block back into the label's
column. Two review rounds and eight critic reports did not settle it, because
the question is geometric and was being answered by eye.

This is the single most expensive deviation in the run and it was mechanically
tractable: render.py already instrumented `fillText` and `render_report.json`
already carried every DOM line box. Nothing compared them. **Upgrade 1.**

### 1.2 A dormant gate (FIXED)

Evidence: five body paragraphs (slides 02, 03, 04, 05, 06) shipped their first
build short of the dossier's last sentence, found one at a time by three
different critics across two rounds; `scripts/plan_drift_check.py` exists for
exactly this class (the No.50 cut) and reported nothing. Measured cause: its
`BODY_RE` required the quote on the same line as the `- body` marker and its
counterpart required a `body` key in copy.json. This run's dossiers put the
quote on the continuation line and its copy.json carries `strings`. The check
compared **zero** bodies and said so in a note, which is indistinguishable from
a clean sheet at a glance. **Upgrade 2.**

### 1.3 An overdue park (FIXED)

Evidence: `FIELD_NOTES` 2026-09-13, "AUTHOR THE LINE BREAK OR THE FITTER WILL —
all nine headlines broke against meaning in the first build"; two full critic
rounds reported it on every frame. The rule set has been parked since the
2026-09-07 scan (https://24ways.org/2013/run-ragged/) with a stated blocker:
per-line TEXT is not recorded, and the known technique is one client-rect call
per character. The blocker no longer holds. A bisection finds the same
breakpoints in O(lines * log characters), and measured over this run's nine
slides the render time is unchanged inside noise. **Upgrade 3.**

### 1.4 Environment: the ask-box browser suite could not run (NOT FIXED, deliberate)

Evidence: `run_state.artifacts.known_gap` — "tests/ask_engine.mjs could not run:
the node playwright package is not installed in this container." The Python
package is present; the node one is not. This is a container provisioning
matter, not a repo defect, and the fix a run could make (adding an `npm i -D
playwright` step to a bootstrap) would add a runtime dependency and minutes to
every run for a suite that guards another surface. Recommend to the maintainer:
install the node package in the routine's image, or move `tests/ask_engine.mjs`
onto its own workflow the way the collectors are, so its absence is visible in
CI rather than in a run's known-gaps line. No change made here.

### 1.5 Not deviations, checked and cleared

- `docket_alerts.py` sent one subscriber email covering three live events. That
  is its designed behaviour (at most one email per run, no repeats from
  `ledger/alerts.json`). Not an incident.
- GAS WATCH read WARN, report only: "one gap in the series first missing
  2026-09-08 (cron-written)". Under the guardrail this routine looks and does
  not touch. The gap is in a cron-written ledger. **PROPOSAL FOR THE
  MAINTAINER, not a change:** `.github/workflows/gaswatch.yml` missed at least
  one scheduled collection and nothing outside a run's daily read reports that.
  A missed day is the one irreversible failure in this project. Worth a
  workflow-level alarm on a failed or skipped run. No collector, model config
  or ledger was touched by this phase.
- Site sign-off PASS, 105 pages, 18 of 18 checks; site build PASS at 109 pages.
  No deviation.
- Score round 2 at 8.39 with zero hard fails, ship gate green. The run followed
  the low-score work-order rule correctly: it went back and fixed, it did not
  stop and report.

## 2. FRONTIER SCAN — focus (g), accessibility and PDF/document format

Stalest legal slot (last scanned 2026-09-04), and distinct from the last three
logged foci (09-12 generative art, 09-10 headless Chromium, 09-09 LinkedIn).
Four searches, two substantive reads, and the two findings that matter were
measured in this repo's own shipped artifact.

1. **Every shadowed line ships three or four times in the PDF.** Extracted text
   from `runs/2026-09-13/carousel.pdf` reads "The bill would make rates to a
   large-" four times in a row. A controlled probe through the engine's own
   Chromium gives the law: copies = 1 + number of `text-shadow` layers (0→1,
   1→2, 2→3, 3→4); `-webkit-text-stroke` with `paint-order` still gives 2.
   PARKED with the candidate gate (extract per page at assemble time, fail on a
   repeated line) and the house-native single-run alternative (`P.reserve`).
2. **The merged PDF is untagged and has no language.** Its catalog holds only
   `/Pages` and `/Type`. Chromium emits tagged PDFs and Playwright's `page.pdf`
   takes `tagged=True`, but `assemble.py`'s pypdf `add_page` merge does not
   carry the structure tree across (`clone_from` does). PARKED.

Both are in `knowledge/FIELD_NOTES.md` under 2026-09-13 with source URLs,
measurements and unblocking conditions. Nothing applied: the budget filled
reactive-first, and both are changes to the shipped artifact that want a gate
and a visual comparison of their own.

## 3. UPGRADES MADE (3, all `kind: fix`)

Logged in `ledger/upgrades.json` with full verification evidence. Summary:

1. **Canvas type is checked against DOM type** (engine). render.py records each
   drawn string's ink box as a quad through the whole transform, so a rotated
   label is measurable for the first time, and stamps the canvas element id into
   the canvas telemetry; qa.py FAILS on 30 percent of the smaller ink box or 40
   square px of glyph through glyph, against the DOM line's em box rather than
   its line box. Reconstruction in `tests/overprint_verify.py` (6 cases, all
   hold). Fires on 0 of 136 shipped slides.
2. **`plan_drift_check.py`'s body comparison actually runs** (scripts). Reads
   the continuation-line dossier shape and falls back to the slide's authored
   `strings`. Comparisons over the shipped corpus rise from 17 to 38; the one
   new finding is a real historical cut. Reconstruction of this run's defect
   fails as it should.
3. **Ragged display lines are measured, not eyeballed** (engine). `line_text`
   per node via Range bisection, and a WARN for a hanging function word, a
   stranded two or three letter word, or two consecutive in-word breaks.
   Reconstruction in `tests/line_text_verify.py` (4 cases, all hold).

No gate, threshold or hard-fail rule was weakened. No runtime dependency was
added. No file under `docs/videos/`, no collector, no gas ledger and no model
config was touched.
