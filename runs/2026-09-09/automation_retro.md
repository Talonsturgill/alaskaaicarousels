# AUTOMATION RETRO — run of 2026-09-09 (No. 54)

Phase 12, written after the merge and before the Gmail draft. Read against
`prompts/routine_instructions.md`, `out/2026-09-09/run_state.json`, the three
BUILD RECONCILIATION rounds in `out/2026-09-09/storyboard.md`, and the three
instinct entries born this run.

The deck shipped: ten slides, 8.47 against a threshold of 8.3, every gate row
green. Nothing below is about the deck. It is about what the machine let
through and what it charged to find out.

## 1. WHERE THE RUN AND THE ROUTINE DISAGREE

Phase by phase. Every row carries its evidence.

| Phase | Spec says | Run did | Reading |
|---|---|---|---|
| 0 WAKE | take the day if `runs/<date>` is free | took 2026-09-09, noted 2026-09-08 had no run at all | conforms; the gap is a MISSED RUN on the 8th and is not this run's defect. Worth the maintainer's eye: the last ship before this was 2026-09-07. |
| 3.5 DOCKET | refresh against primary sources | 8 items at `--budget 8`; the BASIS sweep in `watch.json` failed with a 503 on the 8th | conforms. `docket_watch.py` runs on its own workflow and its failure did not touch the run. Environment breakage, absorbed correctly. |
| 3.6 SITE SIGN-OFF | `site_signoff.py` repairs what it finds | PASS, 100 pages, 18 checks; ONE defect found BY EYE and fixed (docket map pin tap targets) | DEVIATION, small. The signoff script passed a page whose tap targets were under the touch floor. Nothing in it measures hit-target size. Not upgraded this run (see section 4). |
| 7 ART BUILD | `dossier_check` before the render | PASS first pass, 10 dossiers, 0 fails | conforms — but see the four spurious failures under §2.3, which happened during the build and were repaired by MOVING THE MARKUP, so the green row is downstream of a workaround. |
| 7 ART BUILD | qa.py must exit 0 | 0 fails deck-wide, verdict WARN, 11 warns | conforms. One of those warns ("busy art under text", slide 02) was the WRONG CAUSE for a real defect. §2.2. |
| 8 PIXEL REVIEW | five-round cap | 2 build rounds + 2 scoring rounds; nine critic findings in round 2, six in round 3 | conforms, and the round budget was the binding constraint. Four of the fifteen findings are defects a machine could have had for free. |
| 10 SCORING | below threshold is a work order | round 1 6.9 (capped), round 2 8.47, shipped | conforms, exactly as the law requires. |
| 11 SHIP | `shrink_pdfs.py` at step 1b | DECLINED: every candidate image 35.9-40.1 dB against a 42 dB PSNR floor; ships at 37.09 MB | conforms. A declined shrink is the correct outcome and there is no flag to force past it. But the PDF is 12 MB over the rubric's own 2-25 MB band and the scorer measured it. NOT a Phase 12 matter: the fix is either a lower DPI target or a wider band, both of which are the maintainer's call. Recommended in the email, not changed here. |
| 11 SHIP | merge the run's own PR | merged. Two unrelated PRs left open (#317, eighteen days old, ready; #299, a deliberate draft) | conforms with the reported exception. #317's artifacts never reached main and merging it now would insert a retroactive topics entry. Correctly escalated rather than done. |

No manual intervention outside the failure protocol. No API limits hit. No
retries other than the four re-renders that repaired real defects. The
environment was clean except for the BASIS 503, which cost nothing.

## 2. THE DEFECTS THE GATES DID NOT CATCH

Five, in the order they cost the most.

### 2.1 A geometry helper that opened its own path (slides 02, 03, 04, 08)

`sheetPath()` began with `cx.beginPath()` and was called inside
`beginPath(); rect(0,0,W,H); <outline>; clip('evenodd')`. Canvas discards the
current path on `beginPath`, so the full-frame rect vanished, the clip became
the sheet, and four cast shadows were drawn INSIDE their own sheets where the
sheet's fill hid them. **Four slides lost their contacts in one commit and
every render looked fine**, because a missing shadow is an absence and not an
artefact. Only `qa.py`'s contact gate caught it, and only on the two slides
whose declared rects happened to sample the right band; the other two rendered
clean and wrong.

Where the machine was: the render succeeded, nothing overflowed, `bespoke_check`
was unaffected, `dossier_check` had already passed. There was no instrument
pointed at the drawing operation, only at the pixels it produced.

### 2.2 Even-odd used to reserve overlapping boxes (slide 02)

One rect per reserved element, added to an even-odd clip. `.sec` and `.sub`
overlapped by 25px, and a region covered by the outer shape plus two rects has
three crossings, which is odd, which is INSIDE, so the set lines painted back
into the reserve exactly where the two elements touched. `qa.py` reported
**"busy art under text"** — the right flag with the wrong cause. Nobody reaches
`destination-out` from that sentence.

Same root as 2.1: an idiom whose failure is invisible in the frame and obvious
in the operation.

### 2.3 Two gates reading two surfaces (slides 02, 04, 07, 10)

`dossier_check.py` reads `data-contacts` off the `<body>` TAG in the source,
because it is designed to run before any render exists. `qa.py` reads what
render.py measured off the LIVE dom. Four slides set the attribute with
`setAttribute` at the end of `renderReady`. The render report carried the
contacts, qa measured them, and `dossier_check` failed all four for declaring
nothing. Both tools were right about their own surface and the message named
neither. The repair was to move four attributes into the markup, which is the
correct repair, arrived at by guessing.

### 2.4 `json.dumps(..., separators=(',', ' '))` (four attributes at once)

The second element of that tuple is the KEY separator, so it emits
`{"what" "x"}` and `json.loads` answers `Expecting ':' delimiter`. It went into
four `data-contacts` attributes in one generation pass and was findable only
because one gate printed the tail of the attribute it could not parse. The
error message reads like a typing slip and the cause is a one-character
argument.

### 2.5 Thirteen contact ellipses thrown into the light (slide 01)

Four plate bolts and nine belt fasteners offset DOWN AND RIGHT on a deck whose
key is az 118 and whose every other lee falls up and left. **No gate anywhere
looks at the DIRECTION of a hand-drawn contact shadow.** A pixel critic found
it by eye. `qa.py`'s existing light check compares a declared relief azimuth
against the slide's own prose; it has no way to know that a given ellipse is a
shadow rather than a mark.

## 3. WHAT WAS CHANGED

Two upgrades, both reactive, both verified. Full detail in
`ledger/upgrades.json` under 2026-09-09.

1. **render.py grows a canvas path/clip auditor; qa.py grades it.** A
   full-frame path built and then discarded by `beginPath()` with nothing
   painted from it FAILS (2.1). Two axis-aligned rect reserves of one even-odd
   clip that overlap WARN, with both rects and the `destination-out` repair
   printed (2.2). Fitted over 32 shipped slides across four decks. The hook is
   observe-and-forward: all 32 renders are byte-identical to their baselines.
2. **dossier_check.py names the surface and the separator.** A body-JSON
   contract written at runtime is reported as exactly that, once per deck, with
   both surfaces named (2.3); and a parse failure whose error is
   `Expecting ':' delimiter` now names `json.dumps(..., separators=(',', ':'))`
   (2.4). Neither changes any verdict's strength: fail counts are identical
   across eight decks.

## 4. WHAT WAS NOT CHANGED, AND WHY

- **2.5, contact-shadow direction.** The highest-value gate still missing and
  the one with no cheap surface. Nothing in the slide contract tells a machine
  which of a slide's ellipses are shadows, and inferring it from geometry alone
  is a research problem, not a bounded upgrade. Parked in
  `knowledge/FIELD_NOTES.md` with the shape a real version would take: a
  `lee:[dx,dy]` on `data-contacts`, checked against the deck's declared key.
  That is a slide-contract change and belongs in its own session.
- **The overlap check as a hard FAIL.** Run No.53 SHIPPED five slides doing it,
  and on its slide 03 two of the four pairs are real unreserved regions
  (164x26 and 164x14 design px) while two are 6px padding slivers. There is no
  gap between those populations to put a threshold in. Reported as a WARN with
  the geometry; promoting it is the maintainer's call and is recommended in the
  email.
- **Tap-target size in `site_signoff.py`.** Real, found by eye, and a
  measurement of rendered CSS box sizes in a built page is a different
  instrument from anything that file currently owns. Out of budget.
- **The 37 MB PDF.** `shrink_pdfs.py` declined correctly. Widening the band or
  lowering the DPI target is a threshold decision and Phase 12 does not make
  those.
