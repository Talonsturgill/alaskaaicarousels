# AUTOMATION RETRO, run No.62, 2026-09-18

Phase 12. Written after the merge, before the Gmail draft. Scope: where the
MACHINE cost this run, not where the showrunner did.

## 1. REACTIVE RETRO, phase by phase against prompts/routine_instructions.md

### Deviations that cost a cycle

**D1. The paint census evicted the ink the ink law exists to look for.**
`INK_HOOK_JS` keeps 160 distinct colours and drops by ARRIVAL. Round zero's
aerial perspective was a per-row colour lerp in the hachure, which minted a
fresh literal on every row, filled the census before the gold was painted, and
qa.py FAILED two frames with

    promised ink #FFC72C: no brush on this frame ever carried it
    (160 colours in the paint census, none within dE 2 of it ...)

on frames that plainly had gold on them. The verdict was FALSE and the message
named no possible instrument cause, so the repair went at the art. Cost: one
full render cycle. Evidence: commit 4e1aaf4's message ("a fresh colour literal
per row flooded qa.py's 160 entry paint census and evicted #FFC72C, so two
frames failed the ink law reporting no gold on frames that plainly had gold").
Reproduced exactly on a fresh fixture this phase, see
`tests/ink_census_evict_verify.py`.
A gate that can return a false FAIL is worse than a missing gate: a run is
required by CLAUDE.md to treat a low score as a work order, so it will spend its
budget on the named defect whether or not the defect is real.

**D2. Every machine gate was green through the deck's two worst findings, and
both were geometrically checkable.** Round one re-originated slide 02's leader
at the disclosure to fix a real honesty defect and produced a 1,020 design px
hairline at 37 degrees across the lower right quadrant, on the frame that prints
THE LENGTH IS PUBLISHED. THE ROUTE IS NOT. Two pixel critics and the flow critic
read it as a plotted route; it scored 4.0 and was deleted in round two. The
existing leader gates (`leader_lands`, `leader_labelled`) both returned ok,
because both ask where the line STOPS and neither asks what the line LOOKS LIKE.
Evidence: `out/2026-09-18/storyboard.md` BUILD RECONCILIATION rows 1366 and
1386, `ledger/instincts.json` 2026-09-18 entry at confidence 0.98.

VERIFIED BEFORE BUILDING, as the brief required. The leader WAS declared in
`window.__akLeaders` with `from`, `at`, `to` and `label` (storyboard section 11
of the slide 02 dossier requires it, and `qa.py` failed slide 05's stem on the
label half in the same round, so the declarations were live). `from` to `to` is
therefore available to a gate with no new authoring contract, and 1,020 px is
1.9x any ceiling this house could defend. A gate WOULD have fired. Built.

THE ANGLE HALF WAS DECLINED, with its measurement. The same reconciliation row
notes the leader's 37 degrees "put a second angle family into a deck whose whole
discipline is one angle", and that is true, but the deck's 28 degree vector
exists only as PROSE (17 occurrences across `design_notes.md` and
`storyboard.md`, zero machine-readable). Checking it would need a new declared
surface (`data-angles` or `window.__akAngles`) that no deck has ever written and
that only helps decks which choose to declare one. The length ceiling catches
this defect without inventing a contract, so it is the whole of the upgrade.
Recommended to the maintainer as a separate decision, not taken here.

**D3. The artwork ledger published a number nobody measured.**
`ledger/artwork.json` shipped with `bespoke` at median 0.251 and 50 percent
drawn share, which were the ROUND ZERO measurements; the shipped render measures
0.149 and 46 percent. Nothing in the pipeline compares that file to the
artifact. Only the scorer caught it, at the end, and it was corrected in commit
a0057cb. That file is the variety engine future runs read for divergence.

DECLINED AS A GATE THIS RUN, with the measurement. `bespoke` appears in 1 of the
last 20 artwork entries and `machine_qa` in 1 of 20, and NEITHER is in
`artwork.json`'s own `_spec.entry_schema`. A gate built on a field one run
invented would fail every run that does not happen to write it, or warn
uselessly on all of them. The right order is: add both fields to the schema
(maintainer's call, it is a ledger contract), then the comparison against
`bespoke_check.py --json` is about twenty lines and a `gate_status.py` row.
Recommended in the email.

### Deviations that cost less

**D4. `run_state.json` stopped being updated at Phase 8.** The shipped file
records `pixel_review: in_progress` and `flow_review`, `scoring`, `ship`,
`upgrade`, `gmail`, `retro` as `pending`, on a run that scored 8.76 and shipped.
Its `bespoke` field still carries the round zero numbers (the same defect as D3,
one file earlier). Nothing reads those fields as a gate, so the cost is to
whoever reads the run state afterwards, which this phase does.

**D5. Flag mismatches cost two invocations.** `scripts/bespoke_check.py` takes
`--slides-dir` only and was called with `--render-dir`; `caption_check.py`'s
`--burns` and `--deck-summary` both take values and the run's own record of the
working invocation was lost. Not upgraded: argparse already errors clearly and
the fix is for the phase to record its own invocations, which is prose, not
machinery.

**D6. A circular gradient poured into an ellipse came back in slide 03's foot
contacts, eighty lines from the chassis comment recording the same mistake on
`litPool`.** No upgrade needed and this is the SUCCESS case: `qa.py` caught it
and printed the exact repair. It is the pattern the other upgrades copy.

### Environment

No installs failed, no API limit was hit, and `gaswatch_health.py` ran with the
live audit at MAINTENANCE (an announced, parsed maintenance window), which is
the documented WARN path and not a machine defect.

### A PRE-EXISTING DEAD GATE, found while regression-testing this phase's work

`tests/empty_paint_verify.py` reports BROKEN at HEAD, BEFORE any change made
today. Confirmed by stashing this phase's diff and re-running: the reconstruction
fixture that is supposed to produce "FAIL, 9 of 9" reports "255 fills, 1 sites,
1 with an empty one" on BOTH the good fixture and the defect fixture, i.e. the
call-site attribution in `PAINT_HOOK_JS` is collapsing every fill onto one site,
so the empty-paint gate can no longer distinguish a routine that painted nothing
from one that painted. That gate exists because run No.47 solved nine analytic
shadow tips and drew none of them.

NOT FIXED THIS RUN: the budget was full with three verified upgrades, and the
likely cause (`(new Error()).stack.split('\n')[2]` no longer resolving to the
caller frame under the current Chromium) needs its own diagnosis rather than a
guess. It is the first thing the next Phase 12 should take, and it outranks
anything on the frontier.

## 2. FRONTIER SCAN

Focus **(a) LinkedIn platform and algorithm**. Rotation check: the last three
logged foci are 2026-09-17 (d) typography, 2026-09-15 (f) self-improving
pipelines, 2026-09-14 (b) editorial dataviz, so (a), (c), (e) and (g) are legal;
(a) is the stalest at 9 days (last 2026-09-09) AND is the slot behind the
criterion `trend_check` records as weakest twice in ten runs with "worked
never". 5 searches, 3 fetches, one of them through this phase's own new helper.

The marketing-blog layer is worthless and was discarded after two searches: it
recycles the same unsourced engagement percentages. The substantive sources are
LinkedIn's own, and they are specific. Findings and the park are written up in
`knowledge/FIELD_NOTES.md` under the 2026-09-18 Phase 12 frontier scan heading.
Headline: LinkedIn's production Feed ranker optimises two named responses,
**Long Dwell** and **Contributions**, and the paper states the long-dwell
threshold outright at **15 seconds**.

Parked rather than applied, because dwell is reader behaviour and this machine
cannot measure it offline; a gate that estimated it from slide count would be
the prose vibes this phase refuses. It is a PLANNING number, and it is the first
published one this studio has for the legibility-and-platform-fitness criterion.

## 3. UPGRADES MADE

Three, all reactive, budget full, frontier findings parked as the rule requires.
Each has a reconstruction that fails before the change and passes after.

| # | kind | what | reconstruction |
|---|---|---|---|
| 1 | fix | qa.py measures a leader's DRAWN SPAN, warn 360 px, fail 540 px | `tests/leader_span_verify.py` |
| 2 | fix | the paint census pins every hex named in `data-ink`, and a saturated census names itself in the failure | `tests/ink_census_evict_verify.py` |
| 3 | fix | `scripts/fetch_pdf_text.py`, so a remote PDF is a primary source and not a dead end | `--self-test`, 6 checks |

## 4. VERIFICATION

- `tests/leader_span_verify.py`: HOLDS. The 1,020 px defect FAILS, the shipped
  123 px leader is silent, 400 px and 500 px negative controls WARN and do not
  fail.
- `tests/ink_census_evict_verify.py`: BROKEN before the fix (the exact run
  message reproduced verbatim, gold absent from a 160-entry capped census),
  HOLDS after, on four fixtures covering the canvas hook cap, the export op-count
  slice, and the forbidden-ink direction.
- `scripts/fetch_pdf_text.py --self-test`: PASS, 6 checks. Also used in anger to
  read the CIKM paper above, which WebFetch had returned as binary.
- `examples/demo-deck` through render.py + qa.py: 4 of 4 rendered, 0 fails,
  verdict WARN at exit 0, the house's standing defect classes and nothing new.
- This run's nine slides through render.py + qa.py: 9 of 9 rendered, **0 fails,
  0 warns, verdict PASS**, unchanged from the shipped result.
- **All nine PNGs are byte-identical (sha256) to `out/2026-09-18/render/`**, so
  the render.py change is purely observational and `runs/2026-09-18/` remains
  reproducible from the committed source.
- Neighbouring engine reconstructions re-run for regression:
  `mark_paints_verify.py` HOLDS, `clip_reserve_verify.py` ALL HOLD,
  `empty_paint_verify.py` BROKEN both before and after (see above).

## 5. RECOMMENDED TO THE MAINTAINER, not done here

1. `tests/empty_paint_verify.py` is dead at HEAD. Next Phase 12's first job.
2. Add `bespoke` and `machine_qa` to `ledger/artwork.json`'s `_spec.entry_schema`
   as structured fields. Then a gate comparing them to `bespoke_check.py --json`
   and `machine_qa.json` is twenty lines, and D3 cannot recur.
3. A declared ANGLE FAMILY surface (`data-angles`) would make D2's second half
   checkable. It is a new authoring contract and therefore a decision, not a fix.
4. `config/sources.yaml refuses_automated_fetch` wants BoardDocs (University of
   Alaska regents packets) and newsminer.com (429, not 403), plus a note that
   federalregister.gov article pages redirect while the API and raw-text
   endpoints work. This run's scouts measured all three; this phase did NOT
   re-measure them and does not write unverified data into a source ledger.
