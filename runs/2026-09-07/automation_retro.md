# AUTOMATION RETRO, Carousel No. 53, 2026-09-07

Written in Phase 12, after the merge and before the Gmail draft, from
`out/2026-09-07/run_state.json`, the five score reports, the 42-row BUILD
RECONCILIATION and the shipped artifacts. The run shipped at 8.78 against a 7.7
rung, clearing the flat 8.3, with zero hard fails open.

It cost FIVE scoring rounds to get there: merit 8.18, 8.77, 8.60, 8.73, 8.78,
with the first three capped at 6.9 by one hard fail each. Two of those three
caps were defects that earlier repair work introduced or missed rather than
original ones. That is the shape of this run and it is what the upgrades are
aimed at.

---

## 1. THE RUN AGAINST THE SPEC, PHASE BY PHASE

| phase | state | deviation from `prompts/routine_instructions.md`, with evidence |
|---|---|---|
| 0 wake | done | none. |
| 1 craft refresh | done | none. 2 searches, nothing new, FIELD_NOTES untouched per the phase rule. |
| 2 research | done | none. 6 scouts, all returned inside the turn. |
| 3 claims | done | **DEVIATION.** 55 claims, but C54 and C55 were added LATE, during the Phase 8 pixel rounds, "because slide 08 was found printing a scout figure that the first claims pass never turned into a claim" (run_state). claims_check PASSed the whole time, because it verifies the claims that exist. |
| 3.5 docket | done | none. 11 items refreshed, 13 reader-facing date forms repaired, committed at the phase boundary as `b50c6c2`. |
| 3.6 gas watch / site sign-off | done | none. 99 pages, 18 checks, PASS. |
| 4 selection | done | none. |
| 5 directors room | done | **DEVIATION, invisible at the time.** dossier_check PASSed 9 of 9, and the plan it passed contained the 102-signature figure with no claim behind it, "1971" backed only by a note, and a "$632,119.41" subtraction backed by nothing. The gate had no instrument for any of them. |
| 6 copy | done | none. caption_check PASS at 770 chars. |
| 7 art build | done | **DEVIATION, invisible at the time.** qa reported 0 fails on a build in which one line of drawing code was flattening seven of nine frames. |
| 8 pixel review | done | **THE EXPENSIVE PHASE.** 5 pixel critics scored the first build 3.0 to 6.8. Four repair rounds. The round-2 repair introduced the round-2 capping defect. |
| 9 flow review | done | The flow critic, alone, caught the missing gold Polaris on all nine rails. |
| 10 assemble | done | none. Vector PDF, 8.96 MB. |
| 11 scoring | done | Five rounds. See below. |
| 12 ship | done | Merged. |

---

## 2. DEFECTS NO GATE COULD SEE, RANKED BY WHAT THEY COST

**(a) A canvas radial gradient with a non-zero inner radius is not a ring.**
`createRadialGradient(CX,CY,S-6, CX,CY,S+96)` fills every pixel inside `S-6`
with stop 0, so an "atmospheric limb" was added FLAT over the whole globe in
`lighter` on SEVEN of nine slides, erasing the az-142 terminator the deck's
whole thesis rests on. Evidence: reconciliation row `01, 02, 03, 04, 05, 08, 09`.
Five pixel critics each reported a symptom ("flat lighting", "no directional
terminator", "a centred radial gradient with a vignette") and it took reading
three reports together to find the one cause. **It is still in the shipped
deck, on slide 07** (`createRadialGradient(CX,CY,S-8, CX,CY,S+150)`, stop 0 at
`rgba(104,164,214,0.34)`, `lighter`), and the round-5 scorer named it by its
symptom: "slide 07's flat blue gradient". Fixed by upgrade 1.

**(b) A fact can reach a render without ever becoming a claim.** Slide 08
printed "102 SIGNATURES" and a 102-mark struck field off a scout paragraph.
claims_check, aggregate_check and plan_drift all passed. Verifying it late also
CORRECTED it three ways (shareholders and descendants, an early-December
snapshot, 20 non-shareholder signatures excluded), which is three corrections
that cost a re-render because the check happened after the art. Fixed by
upgrade 2.

**(c) Fixed brand furniture belongs to no slide's dossier.** The gold Polaris
was missing from all nine rails and three consecutive frames carried no gold.
Only the flow critic saw it. NOT FIXED, deliberately: see section 4.

**(d) A date the fact-checker reasoned to in a note is not a verified date.**
Slide 07 printed "1971" for four rounds where C35 verifies only "at
incorporation" and only the note said "consistent with 1971". It capped round 3
and was probably wrong (ANCSA was signed in 1971; the regional corporations
incorporated in 1972). Round 5 dropped a second inference of the same shape,
the "2019 JOINT ARTIFICIAL INTELLIGENCE CENTER" pairing. Fixed by upgrade 2,
which reads the `notes` field separately and refuses it as a source.

**(e) A repair round can regress.** Round 2 fixed four text collisions and
introduced a fifth: a value column right-aligned to the gutter landed on the
longest of four names and printed `SERVICESHQ003425CE092`. Merit had risen and
the run was still capped. Every one of these overprints is a few characters
worth a few per cent of either box, which is exactly what qa.py's 30-percent
area test cannot see. Fixed by upgrade 3.

---

## 3. WHAT WAS BUILT

Three upgrades, all reactive, logged in `ledger/upgrades.json` and staged for a
single `upgrade(2026-09-07)` commit.

1. **A ring with a filled middle** (render.py + qa.py). The gradient hook records
   every flat core with its numbers; qa FAILs an additive one over 2 percent of
   the frame. Fitted on 40 re-rendered slides carrying 158 flat cores.
2. **Every figure in the planned copy, against claims.json** (dossier_check.py).
   Verified-only-in-notes fails by name; unsourced fails; furniture and declared
   `[design]` numbers are exempt. Reconstruction:
   `tests/figure_backing_verify.py`.
3. **Two strings on one line may not share a column** (qa.py), on DOM line boxes
   AND on canvas ink boxes, which had no collision gate at all. Reconstruction:
   `tests/overprint_verify.py`.

Frontier scan, focus (d) typography and layout craft: two findings PARKED in
`knowledge/FIELD_NOTES.md`, nothing applied. See `scan_log`.

---

## 4. CONSIDERED AND NOT DONE, WITH THE MEASUREMENT

**A deck-wide gold / Polaris presence check. REJECTED ON THE EVIDENCE.**
brand.yaml says `gold_presence: "#FFC72C appears deliberately on every slide"`,
so a gate looked obvious. Measured first: brand-gold pixels in every shipped
slide of 54 archived runs. The rail Polaris alone reads 120 px at 2x, cleanly
separable from zero, so the instrument works, but gold-free slides are ordinary
in shipped work. Runs 2026-07-13, 2026-08-04, 2026-08-14, 2026-08-15,
2026-08-18, 2026-09-02, 2026-09-05 and 2026-09-06 each ship four or more slides
at exactly zero, and a dozen more ship one or two. A per-slide FAIL would have
failed a large share of the archive and a consecutive-run WARN would fire on it
too. The written brand rule is
aspirational and the practice is not it. **Recommendation for the maintainer:
decide which one is true.** Either the rule should read "at least once per deck,
and never three frames without" and be enforced, or it should stop claiming
every slide. A gate cannot settle that.

**The scoring rubric's weights sum to 1.10.** `config/scoring_rubric.yaml`'s ten
weights total 1.10 while its header implies 1.00, so an all-8 deck scores 8.80
on the literal formula and every threshold in the ledger is quoted on that
scale. NOT CHANGED, and not because it is unimportant. Normalising would lower
every future score by about 9 percent against thresholds fitted on the inflated
scale, which silently makes the 8.3 flat bar equivalent to 9.13 today and breaks
comparison with 50 runs of history. That is a maintainer's decision about the
scale, not a defect to patch in a retro. **Recommendation: either normalise the
weights AND restate the thresholds in the same commit, or amend the header to
say the scale is 1.10 and leave every number alone.**

**`tests/gmail_note_verify.py` is red, and it is not this run's doing.** Its
end-to-end case requires the Editor's note section to contain `<li>` whenever it
is not "None.", and this run's `editor_notes_for_email` is a single long STRING,
which renders correctly as a paragraph. It fails identically on 2026-09-06 and
on the pristine engine, so it is a pre-existing test bug, not a defect in the
draft. Left alone because the fix is a decision about what shape that field is
allowed to take, and the budget was spent. **Recommendation: relax the check to
demand bullets only when the source value is a list.**

---

## 5. WHAT THE GATES DID TO THIS RUN, WITHIN THE HOUR

All three fired on this run's own artifacts, which is the evidence they work,
and the showrunner closed every finding before the draft went out.

- **The gradient gate found an EIGHTH flat core.** The round-2 repair had
  matched on `S-6` and slide 07 was written `S-8`, so a regex-and-eyeball pass
  missed it for five rounds. That is the frame every critic called "a broad flat
  blue gradient" and the reason artwork craft held at 7. Slide 07's limb is now
  `createRadialGradient(CX,CY,0, CX,CY,S+150)` and qa is back to 0 fails across
  all nine slides.
- **The figure gate found three real things**, all now closed: two stale dossier
  lines five repair rounds had left behind (`2019 JOINT ARTIFICIAL INTELLIGENCE
  CENTER` on slide 05, `AT INCORPORATION IN 1971` on slide 07), and
  `$632,119.41` on slide 08, now recorded as C56 with
  `derived_from: ["C07","C42"]`, since it is exact arithmetic on two verified
  claims rather than a new source.
- **And one false positive, fixed the same hour.** `43 U.S.C. 1606(i)` was read
  as the figures 43 and 1606. Citations and identifiers are now recognised by
  shape and blanked out of BOTH sides of the comparison, so the gate does not
  ask who verified a section number, and a claim that merely mentions a statute
  cannot make a bare 1606 a verified figure elsewhere. Re-measured over the same
  fifteen storyboards: 36 findings before, 34 after, the only change being the
  two copies of that one hit, nothing added.

`gate_status.py` on the repaired run reads render PASS, qa WARN with 0 fails,
dossier_check PASS 9 of 9.
