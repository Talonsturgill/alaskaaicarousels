# AUTOMATION RETRO -- run No. 50, 2026-09-04

Phase 12. Written after the merge, before the Gmail draft. Subject is the
machine, not the deck.

## 0. THE STANDING REPEAT OFFENDER (trend_check --window 10)

    weakest  8/10  mean 6.7  last 7.0  Artwork craft and genuine detail
                              worked 2026-08-31 (3 runs ago)  <-- STALE

**Worked on, not deferred.** Upgrade A below is an artwork-craft gate. Slide
08 scored 2.5 with five pixel critics agreeing, and the cause was not ink,
palette or detail: 31 marks that had to read as EXTENT drew a solid parcel.
That is the criterion's own failure mode at its most expensive, and it is now
measurable at render time instead of at round two of pixel review.

Two other criteria appear once each (story arc 7.7, deliverable completeness
8.1) and neither was this run's problem.

## 1. DEVIATIONS, phase by phase, with evidence

**wake.** Woke 23:09 AKDT. `date_note` correctly records that the run takes
its own Anchorage date. DEVIATION, downstream: the caption's first candidate
opened on a countdown ("Ten days are left") written at 23:09; the deadline
arithmetic changed date before the copy chamber finished. `caption_check` has
no clock and cannot have a useful one. Caught by the copywriter reading it.
See "not fixed" below.

**research.** Six scouts, 143 WebSearch calls against the 150 the briefs
allow. Inside the cap. No deviation. (Phase 12's own scan spent 5, which is
the budget working as written.)

**claims.** 19 claims, 12 primary, claims_check PASS. DEVIATION, cosmetic:
`run_state.json` carries `claims` TWICE, once inside `phases` and once at the
top level of the document, so the second write of that phase landed outside
the structure the completion gate reads. Nothing consumed the stray key.

**docket / gas_watch / selection / directors_room.** Clean against the spec.
dossier_check 9/9, dedupe_check exit 0, site_signoff PASS.

**copy.** DEVIATION, and it shipped: three slides carry body copy shortened
in the build to fit its box (34 words against a declared 46, 23 against 43, 36
against 47). One cut removed the sentence its own on-slide attribution
qualifies, leaving C15 with no referent in the picture. `copy_sync_check`
compares copy.json to the RENDER, and a build that cut a sentence plus a
copy.json written from that build agree perfectly, so the gate was green and
correct. Three pixel critics found it by reading. Upgrade C.

**art_build.** DEVIATIONS, three:
  * Slide 08's honesty architecture rests on 31 of 72 grid cells reading as
    extent. A seeded Fisher Yates put all 31 in one township edge to edge and
    the frame drew a parcel with holes in it, seventy pixels under a label
    reading EXTENT ONLY. NO BOUNDARY IS DRAWN. `__akAssert` counted 31 of 31,
    the pixel probe found all 31 painted, both were right, every gate green.
    Five pixel critics scored the slide 2.5. Upgrade A.
  * `AK.reliefShade` writes with putImageData, which ignores the context
    transform, so its `scale` option must be the canvas backing scale. Called
    with `scale: 1` on a `cx.scale(2,2)` canvas it painted the top left
    QUARTER of the frame and left two pin sharp straight edges across the art.
    The option contract passed it because the option is valid and merely
    wrong. NOT FIXED this run; see below.
  * `plan_drift_check` reads the whole storyboard, generated GATE STATUS block
    included, so a failure message quoting a sentence was rewritten into the
    record by `gate_status --sync` and re-detected on the next pass. Rewording
    the offending sentence did not clear the row; it had to be cleared by
    hand. Upgrade B.

**pixel_review / flow_review.** Two full rounds, deck mean 5.38 then a
deck-wide cause fix. DEVIATION, record-keeping: `run_state.json` still reads
`flow_review: pending`, `scoring: in progress` and `ship: in progress` while
assemble, scoring (8.48) and the merge have all happened. The completion gate
requires every phase done with its artifact path; the file is behind the run.

**assemble / scoring / ship.** gate_status re-run at Phase 12 with the
upgrades in place: 17 PASS, 1 WARN, 0 FAIL, score 8.48 against 8.30.
DEVIATION, minor: `run_state` records art_build as "qa.py PASS 0 fails 0
warns"; the render directory that shipped carries 1 warn (slide 05, art
touching glyphs at 4 percent). Measured with the PREVIOUS qa.py as well, so it
is the record that is stale, not the new code.

## 2. FRONTIER SCAN

Focus (g), accessibility and PDF/document format. Stalest legal slot, last
scanned 2026-08-27; the last three logged foci were (c) 2026-09-03,
(e) 2026-09-02 and (a) 2026-09-01. 5 searches, 2 fetches, 2 local experiments
in this engine. Findings and both parks are in knowledge/FIELD_NOTES.md under
2026-09-04, and in the scan_log. Nothing applied: the one change that looked
like a one-liner (`tagged=True` on page.pdf) is measurably undone by the merge
step, and fixing that is a redesign of the assemble path.

## 3. UPGRADES MADE (3, all reactive, budget full)

**A. engine.** A `points` assertion may declare `dispersed: true`; qa.py
measures the largest touching mass of the declared centres and FAILS at 75
percent of them. Fitted on 4,000 simulated scatters per count plus this run's
two real cohorts. Reconstruction: `python tests/mark_spread_verify.py`.

**B. scripts.** `plan_drift_check` strips every generated GATE STATUS block
before reading, and a dossier now ends at the next top-level heading that is
not a slide, the way dossier_check's has since 2026-08-26.

**C. scripts.** `plan_drift_check` compares the body copy a dossier quotes
against copy.json's body for that slide and FAILS a CUT (sentences removed and
nothing added). A rewrite is reported and not judged.

Three is above the daily norm of 0 to 1. Each of the three is a defect this
run actually shipped or lost time to, B and C are the same file and about 60
lines together, and all three revert as one commit.

## 4. NOT FIXED, deliberately

**The reliefShade backing-scale guard.** Ranked fourth by the showrunner and
fourth by me; the budget filled with three defects that shipped. It is small
and certain (compare the `scale` option against the context's own transform
and throw the way an unknown key does) and it is the first thing the next run
should take. Recommended, not done.

**A clock in caption_check.** No. A countdown is stale the moment it is
written and the linter cannot know when the post will be read. The durable fix
is editorial and is already in FIELD_NOTES: anchor to the closing DATE, never
to a count of days. Nothing to gate.

**contact_probe.py --verify's stacked-rect warning.** It prints the boilerplate
about putting rects side by side at the object's base line even when the
declared pair measures dL 36.9, which trains a reader to ignore it. Real, and
the fix is a condition on a message rather than a gate. Left for a quiet day.
