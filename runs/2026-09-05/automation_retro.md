# AUTOMATION RETRO, run No. 51, 2026-09-05

Written in Phase 12, after the merge and before the Gmail draft. The run
shipped: nine plates, scored 8.77 against a threshold of 8.3, after THREE full
rebuild rounds in Phase 8. This document is the diff between what
`prompts/routine_instructions.md` describes and what the machine actually did,
and it is the input to the upgrades logged in `ledger/upgrades.json`.

## 1. Phase by phase, against the spec

| Phase | Status | Deviation, with evidence |
|---|---|---|
| 0 wake | clean | `run_state.date_note`: woke 23:09 AKDT, took the first date with no `runs/<date>/`. Correct. |
| 1 craft refresh | clean | Two entries added to FIELD_NOTES, one of them a NEW number (Socialinsider 7.00 percent, up 14 percent YoY). |
| 2 research | DEVIATION | Three scouts and the fact-checker all recorded `aws.state.ak.us` (APOC, the campaign disclosure database) as UNREACHABLE. It answers `python requests` with an ordinary user agent at HTTP 200 and returned 4,604 rows. The whole deck came out of a source the machine had already written off. Separately: Chromium in this container can't reach the open internet at all. |
| 3 claims | clean | 39 claims, 28 primary, `claims_check` PASS. C42 was added mid-build to carry the 4,588 of 4,604 reconciliation, which is the contract working. |
| 3.5 docket | clean | Worklist refreshed, one dead source link fixed. |
| 3.6 site | clean | `site_signoff` PASS, 97 pages, 18 of 18 checks, nothing repaired. |
| 4 gas watch | clean | PASS, 32 days on record, model misses by 6.82 percent. |
| 5 selection | clean | Story selected, topic dedupe clean. |
| 6 directors room | PARTIAL | The ATMOSPHERE block it approved asserted `az 205` AND a down-left lee. Those can't both be true. The plan of record shipped a contradiction into Phase 8 and nothing in the room or in `dossier_check` could see it. |
| 7 copy | clean | 106 authored strings, `copy_sync` PASS. |
| 8 art build | THREE ROUNDS | Round 1 averaged 4.8 across five pixel critics. Round 2 averaged 6.2 with flow 7.4. Round 3 ships. Every change is in the storyboard's three BUILD RECONCILIATION sections, 12 rows plus 30 plus 27. |
| 9 pixel/flow review | clean, and it worked | The critics found what the gates did not. That is the correct division of labour and also the expense this retro exists to reduce. |
| 10 assemble | clean | Vector PDF 11.55 MB, 9 thumbs, sources verified. |
| gates | 2 FAIL rows at the time of the block | `caption_check` was run WITHOUT `--copy`, so `copy.json`'s slide bodies and first comment were never scanned, and `gate_status` caught it by reading the invocation rather than the verdict. `ship_gate` FAILed on a missing score, which is the correct state mid-run. |
| qa.py | WARN, 0 fails, 12 warns | Includes one live finding worth a look next run: slide 05's axis census reports "the slide declares a mark at 727 and there is no measurable ink within 4px of it in the band". The 726.6 assertion was the run's own repair of a self-comparing assertion, and the census can't calibrate on it. |

## 2. The defect classes that cost the rounds

Six classes, in the order of what they cost, with the honest answer to "could a
machine have caught this".

1. **A defect and its OVERCORRECTION both shipped, twice.** The mineral ring
   went from a uniform stroke (a lamp, not a ridge) to a pale stop over a third
   of every ring, which broke the deck's founding rule that ink is darker than
   the rag. The 105 counting rings went from bubbles to invisible, on a deck
   whose cover headline names that cohort. Both were caught by a human read of
   the render. NOT AUTOMATED THIS RUN: the general form is a declared value
   invariant checked over declared marks, and it needs a design pass rather
   than a patch. Recommended below.
2. **Two light directions in nine frames for three rounds.**
   `akrelief.lightVec(205, 14)` is a light from the LOWER LEFT and every ring,
   debossment and written lee assumed the upper right. AUTOMATED: upgrade 3.
3. **A canvas mark under an opaque DOM knockout is silently erased.** The
   deck's one filled gold seal, the ninth state of a motif tracked across eight
   plates, never reached the page. Its own assertion checked its RADIUS, which
   was correct. AUTOMATED: upgrade 2.
4. **`bespoke_check` went the wrong way when shared helpers were factored into
   the page template**, 0.592 to 0.632, over the 0.60 fail line. The gate was
   RIGHT: nine identical copies of code half the plates never call is not nine
   bespoke frames. Emitting only the helpers a plate calls took it to 0.556. No
   change: the gate did its job and the build changed, which is the intended
   direction.
5. **`<br>` concatenates without a space in extracted text.** "FOUR
   CERTIFIED<br>TICKETS." reached the aggregate gate as "FOUR
   CERTIFIEDTICKETS" and hard-failed as an undeclared count on a word that does
   not exist. The gate was measuring a string the slide never drew. AUTOMATED:
   upgrade 1.
6. **A `%(seed)s` inside an art string is never expanded** and reaches the
   browser as a syntax error. Already caught on round one by render.py's page
   error count (a plate that throws is a FAIL row, not a silent pass), so the
   cost was diagnosis time and not a shipped defect. No new check: a static
   scan would only rename an error the engine already refuses to ship.

## 3. Process and environment deviations

- **The ship commit swept an in-flight engine edit.** `ship(2026-09-05)`
  (16bff13) was created while Phase 12 was mid-edit and committed the first
  upgrade's hunk in `render.py` along with the run artifacts. Nothing is lost
  and nothing is wrong in the tree, but the upgrade set no longer reverts as
  one commit, which is the whole point of the `upgrade(<date>):` convention.
  The fix is ordering, not code: Phase 12 starts after the ship commit exists,
  so the ship commit should be made with `git commit -- <paths>` naming the
  run's own paths rather than committing the whole tree.
- **A gate run by this retro overwrote a run artifact.** `caption_check` was
  invoked here without `--deck-summary`, and it writes
  `out/<date>/caption_report.json` unconditionally, so the run's PASS record
  was replaced with a FAIL. Restored byte for byte from the shipped copy at
  `runs/2026-09-05/caption_report.json` (verdict PASS, 841 chars). Worth a
  maintainer note: a checker that writes its report even when its arguments are
  incomplete can destroy the evidence of an earlier, better-formed run.
- **A source that refuses a browser may answer an ordinary HTTP client.**
  Recorded in FIELD_NOTES this run. Not automated: the right form is a fetch
  helper that falls back from WebFetch to `requests` and records which one
  worked, which is a Phase 2 change and outside this budget.

## 4. Upgrades made

Three, all reactive, all verified. See `ledger/upgrades.json` for the full
entries.

1. **A `<br>` extracts as a space** (`render.py` in-page text record). The
   engine's text record is `textContent` with exactly one rule added.
2. **An assertion can say WHERE its subject is** (`at:[x,y]`, `r`), and the
   motif gate's own census and ink ratio judge it. New FAIL, opt-in,
   reconstruction committed at `tests/assert_clearance_verify.py`.
3. **Every declared relief azimuth is resolved and printed**, and a direction
   the slide's own comments claim that disagrees with it is a WARN.
   Reconstruction committed at `tests/light_direction_verify.py`.

## 5. Verification

Everything below was run, not reasoned about.

- `render.py` + `qa.py` on this run's nine slides, before and after: 9/9 OK, 0
  page errors both times; qa verdict WARN, 0 fails, 12 warns both times, and
  the same warn on the same line of the same slide. The only differences in the
  QA output are the message strings, which now show the real spaced text
  ("GENERAL ELECTION, NOVEMBER 3RD, 2026. FO" where the baseline read
  "...2026.FOU"), plus nine new `[light]` resolution lines. Run twice: once
  against the slides as they stood at 11:2x and once against the 11:36 edit,
  because the showrunner was still repairing slide 01 while this ran and the
  engine's own stale-render gate caught the mismatch. Both sides of the second
  comparison were run from inside the repo, the pre-upgrade side out of a
  temporary copy of `fa3edf9`'s engine which was deleted afterwards.
- `render.py` + `qa.py` on `examples/demo-deck`: QA output byte identical to
  the baseline.
- Defect reconstruction for upgrade 1: the same slide through the pre-upgrade
  engine and this one gives `'...2026.FOUR CERTIFIEDTICKETS. BRONSON AND
  CHURCH.'` and `'...2026. FOUR CERTIFIED TICKETS. BRONSON AND CHURCH.'`, and
  `aggregate_check` on the two reports reports the count over
  `'FOUR CERTIFIEDTICKETS'` and over `'FOUR CERTIFIED TICKETS'` respectively.
- Defect reconstruction for upgrade 2: `tests/assert_clearance_verify.py`, five
  fixtures, HOLDS. The buried seal FAILS, the seal painted out by a later
  canvas op FAILS, the seal on clean rag and the seal under a 45 percent scrim
  both pass, and the same buried seal with no `at` is judged not at all.
- Defect reconstruction for upgrade 3: `tests/light_direction_verify.py`, four
  resolver cases and seven scan cases, HOLDS. Over the 58 slides on disk the
  scan reads 15 azimuths and 37 direction claims with 0 conflicts; this run's
  SECOND build (the same nine slides with az 205 restored) fires 26 conflicts
  on 8 of the 9.
- The neighbouring reconstructions, all HOLD: `motif_survives_verify`,
  `count_assert_verify`, `assert_vacuous_verify`, `wrap_drift_verify`,
  `mark_paints_verify`, `mark_spread_verify`, `copy_sync_shred_verify`,
  `empty_paint_verify`, `gradient_clip_verify`.
- The gates that read the render report, re-run against the new one:
  `aggregate_check` PASS (12 detected, 12 declared), `copy_sync_check` PASS
  (106 strings), `plan_drift_check` PASS (40 claims, 0 drifts), and its own
  `--self-test` PASS.

## 6. Recommendations, for the maintainer and not for this commit

- **`aggregate_check` should read `full`, not `text`.** It scans the
  80-character `text` field, and the space upgrade 1 restores can push a count
  past that cut: on this run's own slides, detections moved from 13 to 12, and
  the one that dropped ("4,588 GIFTS") is declared and re-derived anyway.
  Reading the 400-character `full` field finds 17 counts on this deck against
  12 declared. That is a STRONGER gate and five aggregates would need declaring
  or rewording before it goes green, so it is a decision and not a repair, and
  it is not in this commit.
- **The overcorrection class wants a declared value invariant.** "The ink is
  never lighter than the rag" is checkable against declared marks and their
  local ground, and it would have caught both of this run's overcorrections on
  the round they were made. It needs a contract design (which marks, which
  ground, what tolerance) rather than a patch, so it is written down here
  rather than half built.
- **A checker should not write its report when its arguments are incomplete.**
  See section 3.
