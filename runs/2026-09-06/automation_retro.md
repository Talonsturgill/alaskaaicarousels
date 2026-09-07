# AUTOMATION RETRO, run No. 52, 2026-09-06

Written in Phase 12, after the merge and before the Gmail draft. The run
shipped: nine slides, scored 8.08 against a threshold of 7.7 with zero hard
fails, after FIVE editing rounds, which is the full round cap. This document is
the diff between what `prompts/routine_instructions.md` describes and what the
machine actually did, and it is the input to the upgrades logged in
`ledger/upgrades.json`.

## 1. Phase by phase, against the spec

| Phase | Status | Deviation, with evidence |
|---|---|---|
| 0 wake | clean | `run_state.json` phases advance in order; artifacts recorded per phase. |
| 1 craft refresh | clean | `run_state.artifacts.craft_refresh`: "nothing new; every finding traced to notes already in knowledge/FIELD_NOTES.md". An honest empty is not a deviation. |
| 2 research | clean | `out/2026-09-06/scout_merge.md` present. |
| 3 claims | clean | 25 claims indexed; `plan_drift_check` PASS, `claims` artifacts present. |
| 3.5 docket | clean | `ledger/docket.json`, 5 items refreshed, 1 correction. |
| 3.6 site | clean | site sign-off PASS, 98 pages, 18 checks. `site_fresh_check --date 2026-09-06` still returns "docs/ is exactly a fresh build". |
| 4 gas watch | clean | PASS, read 2026-09-04, 33 days on record, chart present. |
| 5 selection | clean | `selection.md` present, topic dedupe clean. |
| 6 directors room | DEVIATION, downstream | The dossier for slide 05 reserved a fallback (a crop to the palm) against the exact failure that then happened. The room did its job; the run did not use what the room gave it. See defect 4. |
| 7 copy | clean | `copy_sync_check` PASS, 54 authored strings all present in the render. |
| 8 art build | FIVE ROUNDS, the cap | Pixel critics returned a mean of 5.26 on the first review (01 5.5, 02 6.8, 03 5.5, 04 4.5, 05 4.5, 06 5.0, 07 5.5, 08 4.0, 09 6.0). Machine QA went from 2 FAIL slides and 29 warnings to 0 fails and 13 warnings. Four defect classes account for most of the rounds and all four are machine problems, not taste problems. |
| 9 pixel / flow review | worked, expensively | Flow critic scored the sequence 5.4 and predicted the bail point at slide 05, which is the same slide whose reserved fallback was not taken. Two findings were raised and deliberately NOT fixed and recorded as such in the reconciliation, which is the contract working. |
| 10 assemble | DEVIATION | The shipped PDF carried the wrong document title: `--title` was typed by hand at the console and got slide 07's headline instead of `copy.json`'s `document_title`. The scorer found it by opening the file. |
| 11 ship | DEVIATION, minor | The staging copy used the glob `slide-0*.png`, which matched the nine `slide-0N.canvas.png` debug frames render.py writes beside the real ones. Nine files nobody wants were staged into `runs/` and removed by hand. `runs/2026-09-06/` now holds none, so the run shipped clean; the glob is still wrong. |
| gates | 0 FAIL rows | `gate_status.py --run out/2026-09-06`: 18 rows, 0 FAIL, qa.py WARN at 0 fails and 13 warns, score 8.08 vs 7.70, ship_gate PASS. |
| scoring | clean, and low | 8.08. Weakest scored criterion: "Artwork craft and genuine detail" at 6. That is the eighth run out of the last eleven with artwork craft as the weakest row. |

## 2. The four defect classes that cost the rounds

**1. Two declared contact shadows were measuring something that was not a
shadow, and both passed `qa.py` silently.** Slide 08's declared rect sat on the
camera's own dark mount plate and read dL 55. Slide 04's pair straddled 115 px
of open sediment and read dL 25, which was the strobe's falloff across the
frame. `qa.py` has a floor at 4.0 L* and a comfort band at 8.0 and deliberately
no ceiling, so both returned INFO and printed nothing at all. Five pixel critics
found them by looking. The physical cause was identical twice: the occlusion
pool was drawn no wider than the object, so the object covered all of it and
there was no lit ground left beside the foot to pair against, and the author
then reached across the picture for something bright. FIXED, upgrade 1.

**2. A declared axis had ink under only one of its three marks, and the gate
described the symptom.** Slide 07's `data-scale` was corrected from x 1000 to
x 960 and the canvas variable that DRAWS the axis was left at 1000. The axis
census caught it on the first render, correctly, and said "the weakest declared
mark is no stronger than the band's own texture ... draw the marks so a reader
can tell them from the ground", which is a sentence about stroke weight. The run
looked at stroke weights. The census already computed the ink of every mark and
threw all but the minimum away; one strong mark and two at the noise floor is a
different diagnosis from three uniformly weak ones. FIXED, upgrade 2. The same
branch was flagged as a live finding in run No.51's retro
(`runs/2026-09-05/automation_retro.md`, slide 05, "no measurable ink within
4px"), so this is the second consecutive run to lose time inside it.

**3. Filled quads crossing type.** Slide 01's beam cones and slide 09's
volumetric shafts each tripped the "label crossed by art" ring test for the same
reason: a filled polygon has a hard lateral edge. Both were repaired
identically, by drawing offscreen and blurring once at composite. NOT taken as
an upgrade slot this run. `knowledge/TECHNIQUE_LIBRARY.md` already carries the
offscreen-and-blur-once construction twice (entry 91's performance note, entry
94b's "the ramps multiply"), so the technique is present and what is missing is
a pointer from the ring-test failure to it. Recommended, section 4.

**4. A dossier reserved a fallback, the failure it named happened on the first
render, and three repair rounds went into rescuing the original shot.** Slide
05's risk flag named the mitten outcome exactly and reserved a crop. The crop
was taken in round five and worked immediately. PARKED, with the reason and an
unblocking condition, in `knowledge/FIELD_NOTES.md`.

## 3. What was changed (three upgrades, all reactive)

All three are in `ledger/upgrades.json` under 2026-09-06 with full verification
records. In one line each:

1. `qa.py` WARNs when a declared contact shadow and its ground are more than 96
   design px apart. Calibrated on all 45 declarations in the decks that ship
   their sources; an upper bound on dL was measured and rejected.
2. `qa.py`'s axis census names WHICH mark is dead, prints the per-mark ink
   table, and points at the nearest position that does carry mark-strength ink.
   Message only; it can re-route a warn that already fired and can invent none.
3. `assemble.py` takes the PDF's document title from `copy.json`, so the
   hand-typed `--title` defect is unreachable rather than merely detected.

The frontier scan ran in slot (f), agent and automation workflow patterns, and
its finding was applied INTO upgrades 1 and 2 rather than beside them: the
measured result that a validator message needs an admissible ALTERNATIVE and not
just a location is why both new messages name the position to move to.

## 4. Recommended, not done (maintainer's call or next run's slot)

- **The staging glob.** `assemble.py` learned to skip `.canvas.png` on
  2026-08-31 and `gmail_draft.py` and `value_structure.py` both know about it;
  `scripts/ship_images.py` does not (`SLIDE_GLOB = "slide-*.png"`), and neither
  does the hand-typed copy in Phase 11 step 1. One line in `ship_images.py` and
  one in the prompt would close it. Not taken because it cost this run minutes,
  not rounds.
- **`caption_check.py`'s two-failure trap.** It hard-fails when run without
  `--deck-summary`, and `gate_status`'s caption row separately FAILs when the
  report was written without `--copy`. A run that invokes it plainly gets two
  confusing failures in a row for a caption that is fine. Neither rule should be
  weakened; the fix is a single usage error that names BOTH required flags at
  once. Recommended.
- **A pointer from the ring test to the blur.** When `qa.py` reports "art
  touching glyphs" and the crossing ink is a filled polygon, the message could
  name the offscreen-and-blur-once repair. Needs a way to tell a filled quad
  from a stroke at that point in the gate, which is not free.
- **Artwork craft at 6.** The weakest scored criterion in eight of the last
  eleven runs. This is not a gate problem and no gate will fix it; it is the
  standing recommendation that it wants a session of its own.

## 5. Live at the time of writing, and NOT this phase's to fix

`out/2026-09-06/` was being rewritten while this phase ran: a post-score
correction pass edited the slides, `copy.json` and `ledger/artwork.json`
(four corrections, recorded in artwork.json's `corrections` field). As of the
last read, `qa.py` on that directory returns **FAIL**:

    FAIL slide-05: leader carries no label: the leader for 'the otolith in the
    palm' arrives at (286,930) but its label 'OTOLITH' is drawn 52 design px
    away (tolerance 32), so the line and the words it belongs to are not
    connected on the page

That is the shortened otolith label pulling away from its own leader, and it is
the showrunner's under the failure protocol, not an upgrade. Flagged here
because a run does not ship on a FAIL and `runs/2026-09-06/` currently holds the
pre-correction deck. Every upgrade in section 3 was verified against frozen
copies for exactly this reason.
