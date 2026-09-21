# AUTOMATION RETRO — run 2026-09-21, Carousel No. 65

Phase 12. Written after the merge, before the Gmail draft. The run shipped at
7.98 normalised against a relaxed threshold of 7.70, four revision rounds, every
gate green at the end, `qa.py` carrying 9 warns of one idiom.

Sources read: `out/2026-09-21/run_state.json`, `out/2026-09-21/WORKLOG.md`
(PHASE 12 CANDIDATES, eight findings written as they were found),
`out/2026-09-21/render/machine_qa.json`, `out/2026-09-21/score_report.json`,
`prompts/routine_instructions.md`, and the shipped commits on
`claude/carousel-2026-09-21`.

---

## 1. REACTIVE RETRO: deviations, phase by phase, with evidence

### D1 — Phase 2. Every scout brief orders a script no scout can run. [NOT FIXED, RECOMMENDED]

`prompts/routine_instructions.md` Phase 2 says every scout brief names
`scripts/fetch_pdf_text.py`. `.claude/agents/scout.md` grants `WebSearch`,
`WebFetch`, `Read` — no `Bash`. `.claude/agents/fact-checker.md` grants
`WebFetch`, `Read`. Three scouts reported the impossibility independently today
(Beat B verbatim: "Bash is disabled in this subagent, so
scripts/fetch_pdf_text.py could not be run at all") and each then worked around
it SILENTLY, which is the damaging part: the run cannot tell which citations
were read in full and which were read from a search snippet. Beat B lost the
2026 Biennial Report on Alaska Native Languages to it; Beat C found its own
route and read four NPFMC PDFs.

Not taken this run, deliberately. Both honest repairs change the RESEARCH
CONTRACT rather than a script: granting `Bash` to a research agent hands an
interpreter to the least supervised stage of the run, and rewriting the
instruction requires naming the route that actually works and proving it on a
PDF that currently fails. Neither is verifiable by a regression check inside
this phase's budget, and the three fixes below each already had one. See
section 4 for the recommendation.

### D2 — Phase 2. Two sources now 403 and are not in the refusal list. [NOT FIXED, RECOMMENDED]

`aws.state.ak.us` (two scouts, independently) and `go.boarddocs.com` (the
primary route to Board of Regents material) both answer this container with
HTTP 403, and neither is listed in `config/sources.yaml` under
`refuses_automated_fetch`, which exists precisely so a run does not spend budget
rediscovering a workaround. A third joined them during this phase's own frontier
scan: `pdfa.org` 403s a plain WebFetch. All three are recorded in
`knowledge/FIELD_NOTES.md` under today's entry. Left to the maintainer as a data
edit because the only "regression check" available for a config list is a
network call, and a gate that needs the network to pass is a gate that fails on
a bad day.

### D3 — Phase 8. The axis census produced four confident, precisely worded, WRONG diagnoses. [FIXED — upgrade 1]

`.claude/skills/carousel-engine/qa.py`'s `axis_census` clamps its SAMPLE WINDOW
to the frame (`r0 = max(0, int(lo * ns))`) and then set `origin = lo`, the
UNCLAMPED minimum of the declared endpoints. A slide that declares an endpoint
above the top of the frame — the correct declaration for a camera that has
descended past it — got every `peak_at(p)` read at an index offset by exactly
the amount clamped. The gate's own output is the proof: slide 06 declared
`to: [-180.0, 59]` and the census reported "the nearest mark-strength ink to the
mark declared at 418 is at 238, 180 px away". 180 is the clamp. Slides 03, 04
and 05 showed the same signature at their own offsets. The round went to stroke
weights, and the four warns cleared only when the declarations were rewritten to
describe the axis AS DRAWN, which is a workaround: it makes the declaration
describe the visible fragment instead of the scale the slide measures against.
`_census_band_hunt` carried the identical bug two lines below an `origin_perp`
that does the clamped division correctly.

### D4 — Phase 5/8. A storyboard lost every dossier and the gate row said n/a. [FIXED — upgrade 2]

`out/2026-09-21/storyboard.md` reached round three with its deck header, its
continuity tables and its BUILD RECONCILIATION section intact and ZERO
`## SLIDE NN` sections. `gate_status.py` printed
`[n/a ] dossier_check could not run (JSONDecodeError)` for two rounds. Root
cause, measured: `dossier_check.py --json` had two exits that fire before it can
build a report and both printed PROSE on the `--json` path, so the wrapper's
`json.loads` raised and the `except` called `absent()` — the helper for an
artifact not yet written. The loudest finding the gate can produce arrived as
the quietest row it can print. Consequences: all six human-proxy critics in
round two reported judging the frames against the deck header because the
per-slide contracts were not on disk, so two rounds of acceptance checklists
were never checked, and the `reconciled` row passed throughout because it tests
for PRESENCE.

### D5 — Phase 6/8. A house-rule date shipped through a gate that claims to catch it. [FIXED — upgrade 3]

`SEPT 4 TO NOV 2` went onto slide 01's axis key and through round one; a
human-proxy critic caught it, not `scripts/caption_check.py`. CLAUDE.md
describes that table as enforced "on the caption AND on every slide string,
case-insensitively, because the surface that prompted the rule was mono caps on
a cover", and `DATE_FORMS` was compiled WITHOUT `re.I`. Measured during the
repair, the hole was wider than the worklog's reading: `SEPTEMBER 4` and
`2 SEPTEMBER` were equally invisible, and across the 66 shipped `copy.json`
files under `runs/`, 19 decks carry 96 strings this table could not see. The
caption surface never showed the hole because its own `DAY_FIRST` /
`BARE_CARDINAL` pair has been `re.I` since it was written.

### D6 — Phase 8. The reconciliation table passed on presence while carrying superseded numbers. [NOT FIXED, RECOMMENDED]

The BUILD RECONCILIATION camera table still held ROUND ONE offsets through the
whole of round two while the frames moved under it, and three critics measured
renders against superseded values and said so. The proposed check — read each
built slide's `CAM` constant and compare it to the table's row — is about
fifteen lines, and it is a good idea. It is not taken this run because it is a
gate on an AUTHORED table whose column names, units and row identifiers are not
specified anywhere: this run's table is one shape, No.61's was another, and a
gate built against one run's format would hard-fail correct storyboards. The
honest order is: specify the reconciliation table in
`knowledge/SLIDE_DOSSIER_SPEC.md` first, then check it. Recommendation in
section 4.

### D7 — Phase 10. The scoring rubric's weights sum to 1.10. [EXPLICITLY OUT OF SCOPE]

`config/scoring_rubric.yaml` weights ten criteria 0.14, 0.14, 0.16, 0.14, 0.12,
0.10, 0.08, 0.07, 0.05, 0.10 = 1.10. A literal weighted sum inflates every deck
by ten percent; round three's scorer used the literal sum (9.08) and round
four's the normalised (8.25) on the same class of deck. Recorded as a MAINTAINER
call in the worklog because the two honest repairs are not equivalent
(renormalising breaks comparability with every past score; lowering thresholds
keeps comparability and retires the number the doctrine quotes).
`config/scoring_rubric.yaml` was NOT touched. No scorer-side change was made
either: telling the scorer which convention it computes in is only separable
once the convention is DECIDED, and writing one into the agent file now would
be this phase quietly making the maintainer's call.

### D8 — Phase 11/12. run_state.json's phase flags disagree with the run's own artifacts. [NOT FIXED, RECOMMENDED]

`out/2026-09-21/run_state.json` records `pixel_review: pending`,
`flow_review: pending`, `scoring: pending` and `ship: pending`, while
`score_report.json` exists with a 7.98, four review rounds are in the worklog,
and the ship commit `260d9faa` has landed. Every downstream reader of that file
— `gmail_draft.py` among them — is reading a state the run left behind. Not
fixed here because the write is the showrunner's, in phases this agent does not
run; the durable form of the fix is a `gate_status` row asserting that a phase
marked pending has none of its artifacts on disk, which is a next-run job with a
real fixture behind it.

### D9 — Phase 12 itself. An in-flight upgrade was swept into an unrelated commit, mid-edit and broken. [FIXED FORWARD in this commit]

At 10:10Z the showrunner ran `git add -A` to commit a Gas Watch incident record
and picked up this phase's then-uncommitted work. Commit `2c4792d5`
(`gaswatch(2026-09-21): the incident record for an announced upstream shut-in`)
therefore contains `.claude/skills/carousel-engine/qa.py`,
`scripts/dossier_check.py` and `tests/axis_origin_verify.py`, and it is pushed.
History was NOT rewritten: PR #392 is open against that branch.

**The swept state was NOT complete, and the pushed branch was broken for four
hours.** Checked rather than assumed: `git show 2c4792d5:scripts/dossier_check.py`
contains three `_early_exit(...)` call sites and one `RECON_HEAD_RE.search(text)`
and defines NEITHER (`grep -c "^def _early_exit\|^RECON_HEAD_RE"` returns 0). It
compiles, so nothing static catches it, and it raises at runtime on exactly the
paths it was written to make loud:

```
$ python3 <2c4792d5 dossier_check.py> --run-dir <truncated storyboard> --json
NameError: name 'RECON_HEAD_RE' is not defined. Did you mean: 'TOP_HEAD_RE'?
```

A missing `storyboard.md` would have raised `NameError: _early_exit` the same
way. The `--require` gate did not catch it because this run's storyboard is
intact, so neither path is reached. The qa.py half of the sweep WAS complete:
both hunks are present in `2c4792d5` and are byte-identical to the working tree.
Fixed forward in the `upgrade(2026-09-21)` commit, which adds the two missing
definitions. Both shas are named in the ledger entries, and reverting upgrade 1
or 2 requires BOTH commits.

### Also observed, no action

- Four revision rounds, the most since No.34, with the deck shipping at 7.98
  against the relaxed 7.70 and flagged short of 8.3. Two of those rounds are
  accounted for by D3 and D4 above: a round spent on stroke weights that were
  never wrong, and two rounds of critique run against no contract.
- `qa.py` must be invoked at its committed path. Run from a copy elsewhere it
  silently reports a different, larger warn set (25 vs 14 on the same demo
  render) because it resolves repo assets from `__file__`. Noted here so the
  next A/B does not mistake that for a regression; not a defect in a run, since
  every caller uses the real path.

---

## 2. FRONTIER SCAN — focus (g), accessibility and PDF/document format

Stalest legal slot: last read 2026-09-13, eight days, and distinct from the last
three logged foci (2026-09-20 (c), 2026-09-19 (e), 2026-09-18 (a)). Slot (d) was
skipped on `knowledge/FIELD_NOTES.md`'s own instruction after four consecutive
nulls on CSS wrapping.

4 searches, 3 fetches (one 403), and five measurements taken in this repo rather
than read anywhere. Full detail in the dated `knowledge/FIELD_NOTES.md` entry.

- Chromium's `page.pdf(tagged=True)` (Playwright 1.63, already installed) emits
  `/StructTreeRoot`, `/MarkInfo {/Marked true}` and `/Lang en-US` per page, with
  no flag change and no new dependency.
- What it tags on an art deck is nearly nothing: slide 02's tree is `/Document`
  1, `/Div` 14, `/NonStruct` 12, `/H2` 1, `/Alt` ZERO, because the frames carry
  no `aria-label` or `alt`.
- The merge throws it away, by all three routes. `add_page`: no tree.
  `append()`: no tree. `PdfWriter(clone_from=first)` + `append`: tree survives
  with 20 elements — all of them pointing at page 1, with page 2 absent from it.
  `clone_from` is the route the 2026-09-13 park named as the way forward, and it
  is now measured as a dead end: on nine slides it would tag slide 01 and say
  nothing about the other eight. A real fix needs structure-tree merging, which
  pypdf does not provide.
- The destination caps the value anyway. Intopia's NVDA testing of LinkedIn's
  carousel Accessibility Mode: it picks up heading levels but not other tag
  types, acknowledges a graphic but does not read its alt text, nests everything
  in a list, and does not always follow the PDF's reading order. A document post
  has no alt-text field at all.

PARKED, not applied, and the park is now a recipe plus a closed dead end. The
one boundable piece (`/Lang` and `/ViewerPreferences /DisplayDocTitle` on the
merged writer, two lines, worth having without any tags) was not taken only
because the budget filled reactive-first, which is the rule.

---

## 3. UPGRADES MADE (3 of 3, all reactive fixes)

All three were proven RED before the change and GREEN after. Nothing in the
engine changed behaviour on a correct frame: this run's nine slides and the
committed demo deck were re-rendered and re-judged, old engine against new, on
the same pixels.

| # | kind | area | what | reconstruction |
|---|------|------|------|----------------|
| 1 | fix | engine | `axis_census` and `_census_band_hunt` take their origin from the CLAMPED sample start, so an axis endpoint declared off the frame is followed instead of misread | `tests/axis_origin_verify.py` |
| 2 | fix | scripts | `dossier_check --json` answers in JSON on both early exits and names a TRUNCATED storyboard by its signature; `gate_status` calls a check that died on a PRESENT artifact a FAIL, not an n/a | `tests/dossier_truncated_verify.py` |
| 3 | fix | scripts | `caption_check.DATE_FORMS` is case-insensitive, which is what CLAUDE.md always said, and the abbreviation branch catches a trailing ordinal | `caption_check.py --self-test`, 9 new cases |

Verification evidence, in full:

```
tests/axis_origin_verify.py   BEFORE: [BROKE] y axis declared to [-180,59]  (census warns, ink "180 px away")
                                      [HOLD ] the same drawing declared as drawn   <- the control
                                      [BROKE] x axis declared from [-200,0]
                              AFTER:  ALL HOLD (3/3)
tests/axis_band_verify.py     AFTER:  ALL HOLD (3/3, the neighbouring census reconstruction, unchanged)
tests/dossier_truncated_verify.py
                              BEFORE: [BROKE] JSONDecodeError: "FAIL: no '## SLIDE NN' dossiers found..."
                                      [BROKE] JSONDecodeError on a missing storyboard
                                      [BROKE] gate row reads "n/a: could not run (JSONDecodeError)"  <- the shipped symptom
                                      [HOLD ] an artifact not written yet is still n/a  <- the control
                              AFTER:  ALL HOLD (4/4)
caption_check.py --self-test  BEFORE: 4 BAD (SEPT 4 TO NOV 2, SEPTEMBER 4, 2 SEPTEMBER, SEPT 4TH all invisible)
                              AFTER:  brand date self-test PASS (5/5) + mono-caps date self-test PASS (9/9)

engine A/B, same PNGs, old qa.py vs new, run in place:
  examples/demo-deck  old: WARN 0 fails 14 warns   new: WARN 0 fails 14 warns   per-slide findings IDENTICAL
  out/2026-09-21 x9   old: WARN 0 fails  9 warns   new: WARN 0 fails  9 warns   per-slide findings IDENTICAL
                      and identical to the shipped out/2026-09-21/render/machine_qa.json
  the census still reads its marks on all nine frames (10, 10+1, 9, 6, 8, 8, 11, 10, 11 declared marks, no others found)

scripts/gate_status.py --run-dir out/2026-09-21 --require  ->  0 FAIL row(s)
```

No gate, threshold or hard-fail rule was weakened. All three changes tighten or
repair. No new runtime dependency; nothing about the offline slide contract
changed.

---

## 4. RECOMMENDATIONS FOR THE MAINTAINER (not taken as upgrades)

1. **The scout PDF contract (D1).** Decide between granting `scout` and
   `fact-checker` a narrow read-only route to PDF text, and rewriting the Phase 2
   instruction to name the route those agents can already take. Whichever is
   chosen, add the rule that a scout which cannot read a cited PDF must SAY SO in
   its brief: the silent workaround is worse than the failure, because the claims
   stage then cannot tell a full read from a snippet.
2. **The rubric weights (D7).** Renormalise, or lower the thresholds ten
   percent. Then tell the scorer which convention it computes in. This phase
   deliberately did neither.
3. **The reconciliation table (D6).** Specify its columns in
   `SLIDE_DOSSIER_SPEC` and then gate `CAM` against it; in that order.
4. **run_state phase flags (D8).** A row that fails when a phase marked
   `pending` has its artifacts on disk.
5. **Two 403 sources (D2).** `aws.state.ak.us` and `go.boarddocs.com` into
   `config/sources.yaml` under `refuses_automated_fetch`, dated today.
6. **This upgrade set reverts as TWO commits, not one (D9).** `2c4792d5` and the
   `upgrade(2026-09-21)` commit. Both are named in every affected ledger entry.
