# Automation retro, 2026-08-01 (Carousel No. 22, shipped 7.92)

Phase 12. Written by the upgrade-engineer after the merge, before the Gmail
draft. One upgrade this run: a determinism gate. Everything else is analysis,
a park, or a recommendation.

---

## 1. THE STANDING WEAKNESS (mandatory, `scripts/trend_check.py --window 10`)

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  8/10  mean 6.38   last 6.0    Artwork craft and genuine detail        worked 2026-07-31 (1 run(s) ago)
  weakest  1/10  mean 6.0    last 6.0    Legibility & platform fitness           worked never (never)  <-- STALE
  weakest  1/10  mean 6.62   last 6.0    Legibility and platform fitness         worked never (never)  <-- STALE

HARD FAILS (3 of 10 run(s) carried one)
   3x  text against geometry       2026-07-25, 2026-07-29, 2026-07-31  <-- RECURRING
   1x  contrast                    2026-07-31

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   3 run(s)  warns:top-loaded composition                          latest 2026-08-01
   2 run(s)  warns:busy art under text                             latest 2026-08-01

SCORE, most recent runs
  07-23 8.90  07-24 8.66  07-25 6.90  07-26 6.90  07-29 6.90  07-30 8.09  07-31 6.90  08-01 7.92
```

Top repeat offender: **artwork craft and genuine detail**, weakest in 8 of the
last 10 runs, mean 6.38, weakest again today at 6.0.

**VERDICT: DEFERRED as a direct target, with one partial contribution shipped.
This is a stated deferral, not a silent one.**

Why deferred, plainly:

- The 2026-07-29 corpus study (171 slides, 19 decks, written up in FIELD_NOTES
  and in `encoding_reads()`'s own docstring in qa.py) tested whether artwork
  craft is measurable from the pixels and found that **both candidate metrics
  failed to separate high-craft from low-craft slides, in the wrong direction**.
  The finding that survived is: automate the GEOMETRIC defects, route the
  SEMANTIC ones to a judge with measurements in hand. Building a craft-score
  gate today would be re-running an experiment the corpus already answered, and
  the brief for this run explicitly says to respect that.
- Today's craft-6.0 causes were diagnosed by the scorer and are not
  machine-shaped. The stipple field on slide 09 does not read at any size
  (drawn too small, too faint, then correctly clipped); the relief was flat
  until the heightfield got a detail octave. Neither is a threshold. Both are
  in `ledger/instincts.json` and the FIELD_NOTES retro, which is where a
  judgement-shaped lesson belongs.
- The three most recent craft-adjacent upgrades (2026-07-26 frame_balance,
  2026-07-30/31 the relief and engraving benches) all went the same way: they
  moved the FLOOR, not the ceiling. Frame balance now fires on three of this
  run's slides as a WARN and the deck still scored 6.0 on craft. The remaining
  gap is composition and figure quality, and no measurement in the corpus
  study tracked it.

What is contributed toward it today, honestly labelled: the determinism gate
below is not a craft-quality lever, but it is a craft-REVIEW integrity lever.
An unseeded field means every repair round silently repaints art a pixel
critic already reviewed, so a critic's note stops describing the file it was
written against. Today that was live: slide 09's stipple was the deck's
weakest element AND the unseeded one, and it went through five render rounds.
Reviewers of generative art need the art to hold still.

**What would have to be true to tackle artwork craft directly.** Named so the
next run can check them off rather than re-deriving them:

1. A labelled corpus with craft scored PER SLIDE, not per deck. Today the
   scorer emits one artwork number for ten slides, so no metric can be
   correlated against a slide. That is ~200 slide-level labels, and the
   cheapest source is asking the pixel critics for a 1-10 craft number per
   slide from now on (a prompt change, zero engine risk, and it accrues).
2. A candidate metric that separates on THAT corpus with a gap wide enough to
   threshold (the 07-29 study's bar: rank-AUC clearly off 0.5 in the right
   direction on held-out slides).
3. Only then a gate, and it should still be a WARN that routes to a judge.

Item 1 is the unblocker and is a prompt-level change to the pixel-critic
agent. It was not taken this run because the budget is 0-1 upgrades and the
reactive fix takes precedence by the phase's own rule; it is the standing
recommendation for the next run that has a free slot.

Note also the two STALE rows for legibility are one criterion appearing under
two spellings ("&" vs "and"), so trend_check counts them separately and reads
them both as never-worked. That is a reporting artefact, not a blind spot: the
last three engine upgrades were all legibility gates. Left alone deliberately
(normalising the label would rewrite history in the trend report, and the
maintainer should decide that).

---

## 2. REACTIVE RETRO, run_state.json phase by phase

Every phase reads `done` with an artifact path; the completion gate passed and
the run merged. The deviations are inside phases, not between them.

**wake / craft_refresh / research / claims / docket / selection, clean.**
claims_check PASS 29/29 with 3 primary. dedupe_check exit 0 on the chosen
story and exit 1 with seven likely duplicates on the runner-up, which is the
gate doing exactly its job. docket_dates_check clean across 123 assertions.
No environment breakage this run: bootstrap installed clean, no 403s, no API
limits, no retries at the tooling layer.

**directors_room, clean and better than clean.** Three directors converged
independently and all three refused the showrunner's "seventeen times"
multiplier on claims grounds. No machine change wanted.

**art_build, four defects, none of which any gate caught, plus one the gates
caught repeatedly without being understood.** These are the run's real scars.

| # | Defect | Who caught it | Machine-shaped? |
|---|---|---|---|
| 1 | Clipping vector strokes out of reserved text fields ERASED boroughs and coastline across ~40% of the state | pixel critic | no (see below) |
| 2 | Leaf filter `children.length===0` silently excluded every label containing `<br>`, so multi-line labels got no reservation | qa.py's art-crossing-glyphs gate, three rounds running, symptom only | partly (helper, not gate) |
| 3 | The generative reservation was ITSELF a dead cell: a flat blend cleared the contrast gate and failed frame_balance | frame_balance (gate worked) | no change wanted |
| 4 | The stipple field used `Math.random()`, breaking the determinism contract | a human running grep | **YES, fixed this run** |
| 5 | An Imhof elevation-keyed contrast rule CREATED the dead lower third, because in this projection the ranges sit mid-frame | scorer + frame_balance | no (doctrine) |

Defect 1, why no gate. Detecting "geometry that should be there is missing"
requires knowing what should be there. For a map that means re-projecting the
source geodata and comparing coverage against the render, per slide, per
projection, per clip stack. That is a bespoke cartographic regression harness,
not a bounded check, and it would fire falsely on every deliberate crop. The
transferable lesson is authoring doctrine and it is already written into the
FIELD_NOTES retro: never clip geometry out of a text reserve, draw everything
everywhere and re-damp the glyph boxes so geometry ghosts through. Recommended
to the maintainer, not built.

Defect 2, why a helper and not a gate. The gate DID see it, five times; the
loop failed at diagnosis, not detection. The durable fix is that per-run build
scripts should stop hand-writing "which nodes are text" filters. A shared
`AK.textLeaves(root)` in `assets/js/aktype.js` that returns every text-bearing
element including ones with `<br>` and `<tspan>` children would have made the
defect impossible to write. That is a real, bounded, ~25-line upgrade and it is
the first candidate for the next free slot. Not taken today: the budget is
0-1, and between the two, the determinism gate covers a defect that NO gate can
see, while this one covers a defect an existing gate already reports.

Defect 3 is the system working. The reservation cleared contrast and failed
frame_balance, which is exactly why frame_balance exists. No change.

Defect 5 is the most interesting and the least machine-shaped: a craft rule
imported from Imhof and the composition gate pointed in opposite directions,
because the rule assumes high ground sits high in frame. The gate is right and
must not be weakened; the rule needs a projection-aware caveat. Recorded in
FIELD_NOTES as doctrine.

**pixel_review / flow_review / assemble / scoring / ship, clean.** Five pixel
critics, four-plus revision rounds, which is what earned the relaxed 7.7
threshold; the deck shipped at 7.92 and the email says so. Final machine_qa:
0 fails, 4 warns (three top-loaded composition, one busy-art-under-text), all
of which are the known WARN classes trend_check already tracks.

**Gates that passed a defect a human caught: one, and only one, is
automatable, determinism.** That is this run's upgrade.

---

## 3. FRONTIER SCAN, procedural art portable to offline Canvas/SVG

Rotation slot chosen by the 2026-07-31 scan_log entry's own nomination: this is
the stalest slot (last scanned 2026-07-21) and it differs from the last three
foci (2026-07-31 deferred, 2026-07-29 typography, 2026-07-26 headless
Chromium). It also serves the standing weakness.

**PARTIALLY BLOCKED, stated honestly.** WebSearch returned
`web search budget (200 of 200 WebSearch calls)` on the first query, so no
discovery was possible. The scan proceeded by WebFetch against known
substantive sources: 5 attempts, 3 read (2 refused: inconvergent.net 403,
one Hobbs essay URL 404). Treat the coverage as thin by construction; the
rotation slot is NOT marked satisfied and should be rescanned when the search
budget resets.

Read, and relevant to this studio:

1. **Blue-noise point sets** (Bostock, "Visualizing Algorithms"). Uniform
   random sampling produces "both severe under- and oversampling", clumps and
   holes. Best-candidate sampling (generate ~10 candidates per point, keep the
   one farthest from all existing samples) and Bridson's Poisson-disc (sample
   an annulus r..2r around an active point, reject anything within r, grid of
   cell r/sqrt(2) for the distance test) both fix it, and the article shows
   the result carries "substantially more detail and less noise".
   This is directly the deck we just shipped: slide 09 placed 3,048 dots on a
   jittered regular grid, and the pre-fix version's unconstrained placement is
   what leaked marks onto the landmass. https://bost.ocks.org/mike/algorithms/
2. **Flow-field parameters** (Hobbs). Grid resolution ~0.5% of image width,
   step 0.1-0.5% of width, and the seeding advice is the same finding: a
   regular grid "can feel overly stiff", uniform random "creates clumps and
   sparse areas", circle packing gives balanced spacing with relaxed variation.
   Also: enforce a minimum distance between curves at each step; distort the
   grid between rounds. https://tylerxhobbs.com/essays/2020/flow-fields
3. **Particle systems with collision response** in vanilla canvas (normal,
   relative velocity, impulse over combined mass, plus a repulsion term to stop
   interpenetration sticking). Confirmed library-free; noted as available, not
   currently wanted. https://www.gorillasun.de/blog/an-algorithm-for-particle-systems-with-collisions/

**Outcome: parked, nothing applied.** A `AK.bluenoise(w, h, r, rng)` helper in
`assets/js/noise.js` (Bridson, ~60 lines, seeded, zero dependencies) is the
right shape for this studio and would have improved the exact element that
scored worst today. It is parked and not applied because the budget is 0-1 and
the slot went to the reactive fix, and because a new art helper wants a worked
TECHNIQUE_LIBRARY entry with parameters and at least one trial slide before a
director is told to reach for it. Written to `knowledge/FIELD_NOTES.md` under
2026-08-01 with the source URLs.

---

## 4. UPGRADE APPLIED, 1 of 1 (reactive fix)

**A determinism gate: render.py scans slide source, qa.py FAILs unseeded
randomness.**

`SKILL.md` has said since the engine was written that slides must seed all
noise and that "same inputs must reproduce the same pixels". Nothing enforced
it. On this run a stipple field ran on `Math.random()` through five render
rounds on a deck about a public record, and was caught by a human running grep.

Every other check in qa.py reads ONE screenshot, so an irreproducible slide is
structurally invisible to all of them: the PNG looks fine, because a random
field is a plausible-looking field. The defect only exists between renders.

Design:

- `render.py :: scan_nondeterminism()` reads each slide's INLINE `<script>`
  blocks (external `src=` is not read, so vendored d3/three/zdog never trip
  it; `type="text/template"` and friends are skipped; JS comments are blanked
  before matching, preserving offsets so line numbers stay true). Findings are
  recorded per slide in `render_report.json` under `nondeterminism`.
- `qa.py` judges: `Math.random()`, `crypto.getRandomValues()`,
  `crypto.randomUUID()` are a **FAIL** naming the file, the line number and the
  source line, and pointing at the one-argument replacement `AK.rng(seed)`.
  `Date.now()`, `new Date()` (no argument) and `performance.now()` are a
  **WARN**: usually a timing log, occasionally an animation phase that does
  feed pixels, so the author decides but the machine will not let it pass
  unseen. A dated literal like `new Date("2026-08-01")` is deterministic and is
  not flagged.
- No escape hatch on the hard tier, deliberately, matching the precedent of
  the offline/external-URL rule in `resolve_html()`. There is no legitimate
  use of unseeded randomness in a slide, and the replacement is one argument.
- A deck that PRINTS the string "Math.random" as body copy is DOM text, not
  script, and is not flagged.
- Zero new dependencies; ~90 lines of stdlib `re`.

### Verification (all four required pieces)

1. **Scanner unit cases, 9 of 9 correct**: seeded `AK.rng` clean; bare
   `Math.random()` hard; the same call in `//` and `/* */` comments clean;
   `<script src=...>` not read; the string in body copy clean;
   `type="text/template"` skipped; the three clock APIs soft; `new Date("...")`
   clean; `crypto.getRandomValues()` hard.
2. **`examples/demo-deck` regression**: render 4/4 OK, and the resulting
   `machine_qa.json` is **byte-identical to the pre-change baseline** (0 fails,
   11 warns, same messages). The demo deck's flow-field and software-3D slides
   raise zero determinism findings, so seeded practice is the norm and the gate
   adds no noise.
3. **This run's slides** (`out/2026-08-01/slides/`, 10 slides): render 10/10
   OK, qa 0 fails / 4 warns, **identical to the shipped
   `runs/2026-08-01/machine_qa.json`**, and zero determinism findings, the
   showrunner's in-run fix holds. Stronger: the 10 fresh PNGs are
   **sha256-identical to all 10 shipped renders**, so this deck is now provably
   reproducible from its committed HTML.
4. **Defect reconstruction**: slide 09's stipple restored to the pre-fix form
   (`AK.rng` line removed, `rnd()` -> `Math.random()` at both call sites).
   render.py printed `[determinism] slide-09.html: Math.random() line 163,
   Math.random() line 164`; qa.py returned **verdict FAIL, exit 1**, with both
   line numbers and source lines quoted. Rendering that same reconstructed
   slide twice produced **different pixel hashes** (`c398e3a3d3840612` vs
   `da7f912524b1c04e`), which is the defect itself, demonstrated. Its
   frame_balance number also drifted between the two renders (top 87% vs 88%),
   a small live illustration of why unseeded art corrupts an iterative review.

No gate, threshold or hard-fail rule was weakened. This adds one FAIL class and
one WARN class and touches nothing existing.

Rollback: revert the `upgrade(2026-08-01)` commit. `scan_nondeterminism()` and
its two tables are self-contained in render.py with one call site in the render
loop, and the qa.py consumer is one `for` block over `rec.get("nondeterminism",
[])` which reads an absent key as empty, so older render reports still parse.

---

## 5. NOT DONE, ON PURPOSE (recommendations for the maintainer / next slot)

Ranked. None of these were taken because the budget is 0-1 and the reactive fix
took the slot.

1. **`AK.textLeaves(root)` in `assets/js/aktype.js`**, the durable fix for
   defect 2. Per-run scripts keep hand-writing "which nodes are text" filters,
   and `children.length===0` is the wrong one whenever a label contains `<br>`
   or `<tspan>`. ~25 lines, bounded, verifiable against this run's slide set.
   First candidate for the next free slot.
2. **Per-slide craft labels from the pixel critics**, the unblocker for the
   standing weakness, per section 1. Prompt-level, zero engine risk, and it
   only pays off if it starts accruing.
3. **`AK.bluenoise()` (Bridson)**, parked frontier item, section 3.
4. **Projection-aware caveat on imported value rules**, doctrine, defect 5.
   Belongs to the editorial brain (Phase 14), already in FIELD_NOTES.
5. **Two spellings of the legibility criterion in trend_check**, a reporting
   artefact, maintainer's call, see section 1.
