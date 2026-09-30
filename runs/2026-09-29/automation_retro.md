# Automation retro, 2026-09-29 (No.72, E-Rate)

Phase 12, upgrade engineer. Inputs: out/2026-09-29/run_state.json, WORKLOG.md, storyboard.md
(BUILD RECONCILIATION), score_report.json, flow_review.json, render/machine_qa.json,
render/render_report.json, the 2026-09-29 retro block in knowledge/FIELD_NOTES.md, the
showrunner's five incident notes, and `python scripts/trend_check.py --window 10`.

## 1. Trend check and the top repeat offender

`trend_check --window 10` (2026-09-19 to 2026-09-29):

- Artwork craft and genuine detail: weakest in 7 of 10, mean 7.15, last 8.0, last worked
  2026-09-28 (AKSNOW nearEdge, one run ago).
- Legibility and platform fitness: weakest 1 of 10 (TODAY), mean 7.3, STALE (never worked).
- Variety vs ledger, Deliverable completeness: weakest 1 of 10 each, STALE.
- No hard fails in the window. Defect classes still shipping (2 runs each, latest today):
  art touching glyphs, busy art under text, outside safe zone.

**Decision: DEFER the top offender, artwork craft, and say why.** It was worked yesterday and today
it read 8.0 after one craft cycle (7.5 before), the best art reading since the craft floor
arrived on 2026-09-26 (7, 7, 7). The scorer's four named frames (05 subtle fold and a soft pool,
02 a repetitive ream field with uneven falloff, 08 a uniform paper ground, 04 open ink right of the
short bars) are composition choices on this deck, not a helper or gate that misbehaved, so there is
no bounded machine change that would have moved them. The one craft-adjacent machine cost this run
(incident 3, two rounds on contacts over a dim pool) is also deferred, below. What would have to be
true to work it next: a craft defect the scorer names on two decks that traces to one shared
helper's default, or the pairwise judge parked on 2026-09-28 unblocked by measuring the scorer's
AB/BA flip rate on the pre_craft folders (now four runs of them).

Today's weakest criterion, Legibility (7), is a disagreement between two instruments rather than a
missing fix, and it is written up as a recommendation in section 4, not built.

## 2. Deviations, phase by phase, with evidence

1. **Phase 7 art build: a new chassis read as 40 percent drawn.** bespoke_check FAILED the deck at
   18 drawn vs 27 blocky because akstack.js draws inside the module. The showrunner fixed it
   mid-run as f591b784 (CHASSIS_RE counts chassis constructors at the call site); logged here as
   this run's first upgrade. Measured now: 62 drawn vs 27 blocky, 70 percent. Transparency for the
   maintainer: this change can only RAISE the drawn share, and 12 of the 44 counted calls are
   grounds (paperGround, inkGround) and drop shadows, which are arguably not drawn marks. Without
   those 12 the share is 65 percent, still over the 45 percent line, so the verdict on this deck
   does not rest on them. It follows the AKSDF and AKT. precedent in DRAWN. The bare `A.` alias in
   the regex could in principle count an unrelated object named A with a method of the same name.
   Whether grounds and shadows should count is the maintainer's call, not a Phase 12 edit.
2. **Phase 8: a subset re-render after a shared-helper edit (incident 2).** render.py `--only`
   after editing assets/js/akstack.js printed STALE for the other frames, and qa.py would have
   FAILED them; the gate worked, but the run came within one command of reviewing or gating on
   seven stale PNGs, and the only correct next step was always the full re-render the two checks
   demand. FIXED (upgrade 2).
3. **Phase 8: contact shadows on ink measured 1 to 4 L* until the lamp pool was brightened
   (incident 3), two rounds.** Final declarations read dL 10 to 24 (contact_probe --verify, this
   run's render). qa.py already appends "the ground is already near black ... light the ground
   first" when the ground reads under L* 12, and contact_probe's notes do not say it. NOT upgraded:
   the round-1 readings are not on disk, so I can't tell whether the grounds sat under 12 (and the
   existing hint fired) or between 12 and about 20 (where it would not). A probe note keyed on the
   frame's ink floor is a sensible next step, but building it without the failing numbers would be
   a guess. What would make it buildable: the next ink-ground deck keeps its round-1
   contact_probe output in out/<date>/.
4. **Phase 8 and 10: curly quotes that were not there (incident 4).** Three pixel critics and the
   scorer reported curly quotes on slides 05 and 08. The showrunner's defence, "copy_sync and
   caption_check PASS", was not evidence: caption_check reads copy.json only, and copy_sync
   compared letters and digits only, so NOTHING in the gate battery read the punctuation that
   actually rendered. A curly mark or an em dash typed into slide HTML, or into a label, coordinate
   or fixture copy.json never holds, would have shipped with every row green. Measured cause of the
   false reports: Space Grotesk draws the neutral U+0022 and U+0027 slanted and tapered, and
   Manrope draws U+0027 comma-shaped. FIXED (upgrade 3), with the census the critics can be handed.
5. **Phase 8: a cut mask one row short of its descender (06, "connectivity" read as a v).** Caught
   by a critic, no gate. Deferred: a mask-vs-glyph-box coverage check is a new measurement inside
   the akstack terrace path and needs its own design.
6. **Phase 8: the record-stack caption ran 31 px past the right margin on all nine frames.** Written
   once at 18 px, then set to 17 px. Caught in review. The node is data-decorative; qa.py exempts
   decorative type from the floor and reports "outside safe zone" as a warn class that has shipped
   two runs running. Deferred with section 4.
7. **Phase 8 flow review: slide 07 ended at $313,070 while slide 08 quoted "$9,229,248 to
   $373,345".** Caught by the flow critic only. A cross-slide figure-consistency check would need
   semantic pairing of figures; not bounded.
8. **Phase 3.6: Gas Watch live audit (incident 5).** One read FAILED on a CINGSA 307, the next two
   read WARN (a source reading newer than the last collection, scheduler late, workflow_dispatch
   403 as on 2026-09-27 and 09-28). run_state.json carries both states in two places
   (`phases.gas_watch` WARN, top-level `gas_watch` FAIL), so the gate battery's fresh read at ship
   is the one to trust. No machine change: collectors are out of this phase's scope and the
   transient cleared on re-read. Third night of dispatch 403s; the maintainer should look at the
   integration's workflow permissions (already in the 09-28 notes).
9. **Phase 10: scored 8.79 raw, 7.99 normalised.** The rubric's weights sum to 1.10 (known since
   FIELD_NOTES line ~5252), so every threshold comparison runs about 10 percent generous. Correcting
   it would tighten the ship bar and change the meaning of every historic score; that is the
   maintainer's call. Recommend in the email, no edit.

## 3. Frontier scan, focus (d) typography

Last three scan_log foci: (f) 09-28, (b) 09-27, (e) 09-26. (d) was last read 2026-09-17 and had
recorded itself as well mined for line-breaking (text-wrap balance and pretty reconfirmed null four
times, text-box-trim already parked), so it was narrowed to glyph-level quote-mark behaviour, the
subject of incident 4. 4 searches, 2 fetches, 3 measurements in the engine's own Chromium.

- Unicode means U+0022 and U+0027 to be neutral, vertical glyphs, never directional
  (https://www.cl.cam.ac.uk/~mgk25/ucs/quotes.html). Two house faces depart from that.
- MEASURED over all eight committed families at 72 px: Space Grotesk slants and tapers both marks
  (its straight opening quote looks like a closing curly one); Manrope slants U+0027. The other six
  draw both upright. No `salt`, `ss01` to `ss07`, `calt` off or `case` changes either face's marks
  (screenshot hashes identical across all eleven settings), so there is no CSS fix.
- MEASURED: Chromium's PDF text layer records Manrope's apostrophe as U+2019 for some occurrences.
  15 of 72 shipped carousel.pdf files carry U+2019 in extracted text; four spot-checked copy.json
  files for those decks hold only U+0027.
- Nothing new on line breaking; Space Grotesk's own documentation lists stylistic alternates but
  none that touch the quote marks (https://fontsource.org/fonts/space-grotesk/about).

Outcome: the first finding supplies the principle and the census flag for upgrade 3 (logged as a
fix). Two candidates PARKED in knowledge/FIELD_NOTES.md ("Parked, 2026-09-29 frontier scan, focus
(d)"): setting quote marks in the other face when quoting in Space Grotesk or Manrope, and the PDF
text layer's U+2019.

## 4. Recommendation, not built: the 24 px floor and data-decorative

Legibility was today's weakest criterion (7). The scorer charged the 17 px record-stack caption,
slide 04's 17 px key line and slide 09's 18 px FY ticks, all under the 24 px floor (slide 04's
20 px pin labels are in the same class and were not named). Every one is data-decorative, and render.py exempts decorative type from its 24 px warn, so
machine QA was silent. The rubric's descriptor ("All floors met (32px body / 24px min)") has no
decorative exemption. This is the same two-instrument disagreement qa.py already documents for
text collisions. A warn on decorative type under 24 px would be a tightening, but it would fire on
the house chrome of every deck (the 20 px coordinates and the alaskaaihq.com mark), which the
scorer has accepted. The maintainer should rule whether house chrome is exempt by name; with that
ruling the warn is a small render.py change.

## 5. Upgrades (3 total, all reactive fixes)

1. **bespoke_check counts akstack chassis constructors as drawn marks** (showrunner, f591b784,
   logged only). See deviation 1.
2. **render.py `--only` widens to every slide that is already STALE.** Before rendering, any slide
   whose existing record fails the same hash arithmetic the STALE notice and qa.py use is added to
   the list, with a printed reason. `--only-exact` keeps the literal list; qa.py still FAILs
   whatever that leaves stale. It can only render more than asked. Files:
   .claude/skills/carousel-engine/render.py, .claude/skills/carousel-engine/SKILL.md.
3. **copy_sync_check reads punctuation where it rendered.** It FAILS on U+201C, U+201D, U+2018,
   U+2019, U+2014 or U+2013 in any rendered DOM text or canvas string, and prints each slide's
   quote marks by codepoint and face, flagging the two faces that draw neutral marks slanted. The
   pixel-critic and scorer briefs judge quotes by codepoint and trust the census; Phase 8 step 2
   pastes each critic its line. Files: scripts/copy_sync_check.py,
   tests/copy_sync_punct_verify.py, .claude/agents/pixel-critic.md, .claude/agents/scorer.md,
   prompts/routine_instructions.md, knowledge/FIELD_NOTES.md.

Three is the cap and above the daily 0 to 1 norm. The reason: upgrade 1 was already made mid-run,
upgrade 2 fixes a near-miss that would have cost a round, and upgrade 3 closes a hole in a house
rule that "never bends", enforced until today on the wrong surface.

## 6. Verification

- This run's slides, scratch copy, full render + qa: 9/9 OK, qa WARN, 0 fails, 30 warns (identical
  to the shipped machine_qa), all nine PNGs byte-identical to out/2026-09-29/render.
- Reconstruction of incident 2: one comment appended to assets/js/akstack.js (restored after, sha1
  2fec565a before and after, git clean). `--only 2 --only-exact` (the old path): 1 slide rendered,
  STALE printed for 8, qa.py exit 1 with 8 stale-render FAILs. `--only 2` (new): "--only widened
  to 8 stale slide(s)", 9 rendered, qa.py exit 0, 0 stale fails. An HTML-only edit to slide 05
  with `--only 3`: widened to slide 05 alone, qa exit 0, all nine PNGs byte-identical to shipped.
- examples/demo-deck, full render + qa: 4/4 OK, qa WARN 0 fails 14 warns (same as 2026-09-28's
  log); `--only 2` with nothing stale: no widening, 1 slide rendered, qa exit 0.
- copy_sync_check on this run: PASS (86 strings), census names Space Grotesk "drawn slanted" on
  slides 02, 03, 05 and 09, and slide 05's two U+0022 are the marks the scorer read as curly.
  gate_status copy_sync row: PASS with the verdict line. gate_status --self-test 27/27.
- Reconstruction of the enforcement hole: scratch slide 05 with a curly apostrophe and an em dash
  in its decorative coordinate line and an en dash drawn by canvas fillText, rendered: the new
  script FAILS all three (U+2019, U+2014, U+2013); the pre-upgrade script PASSES the same render.
- tests/copy_sync_punct_verify.py: 6/6 HOLD; against the pre-upgrade script 4 BROKEN.
  tests/copy_sync_shred_verify.py still HOLDS.
