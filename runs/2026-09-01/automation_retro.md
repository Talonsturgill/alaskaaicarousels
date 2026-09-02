# AUTOMATION RETRO - Run No.47, 2026-09-01

Phase 12, written after the merge and before the Gmail draft. Section 1 walks
`out/2026-09-01/run_state.json` and the run's artifacts against
`prompts/routine_instructions.md`. Section 2 logs the frontier scan. Section 3
records what was changed, what was refused, and what was parked.

Run headline: 9 slides, scored 8.89 against the standing 8.3, zero hard fails,
`gate_status` 17 rows and 0 FAIL, merged to `main`.

The shape of this run's defects matters more than the count. Three of the four
were one mistake wearing different clothes: THE CODE COMPUTED THE HONEST ANSWER
AND THEN DID NOT USE IT. Every one of them was invisible to the machine,
because every instrument here was pointed at whether the code RAN and none at
whether its answer REACHED THE FRAME.

---

## 0. TREND CHECK (run first, as the phase requires)

`python scripts/trend_check.py --window 10`, over 2026-08-20 to 2026-09-01:

```
weakest 9/10  mean 6.6  last 7.0  Artwork craft and genuine detail   worked 2026-08-31 (1 run ago)
0 of 10 runs carried a hard fail
defect classes still shipping: busy art under text (6), top-loaded
composition (6), outside safe zone (4), contact shadow (4)
```

**Top repeat offender: artwork craft. This phase DEFERRED it, and here is the
plain statement the rule asks for.**

Two of this run's three upgrades do work on artwork, but on its CORRECTNESS and
not on its RICHNESS: upgrade 1 catches a routine that drew nothing where nine
shadows were solved, upgrade 2 catches a slide arguing in type that two objects
are identical when they are not. Both were live artwork defects in this deck
and both are now impossible to ship silently. Neither of them makes a thin
frame less thin, which is what the 6.6 mean is measuring.

The richness half is deferred because it is not safely boundable this run and
because the two reactive defects above nearly shipped. WHAT WOULD HAVE TO BE
TRUE to take it: a per-region craft-density census that names the largest inert
rectangle in a frame as a fraction of the frame, calibrated against the frames
scorers have actually named as dead (2026-09-01 S05's top 40 percent, S04's
left third, S03's right-centre quadrant) and against frames they praised, so
"fill the dead zone with the deck's own vocabulary" becomes a number handed to
the treatment director at PLANNING time rather than a note a pixel critic has
to notice after the render. `scripts/value_structure.py` (2026-08-31) already
reads the notan off the pixels and is the right file to extend; what it lacks
is a region census. That is recommendation 4 in section 3, and it is a
one-upgrade job on a run whose reactive budget is not already full.

---

## 1. REACTIVE RETRO: deviations, with evidence

### D1. Nine solved shadow tips, none of them drawn (SEVERE, the worst of the run)

Slide 07's clip loop tested whether each cast point was left of a surveyed
boundary and broke at `s = 0` for every marker, so nine analytic shadows were
built base to base, filled at zero length, and the slide's declared focal point
was never in the picture. The root cause is compositional and is worth keeping:
the boundary descended in the SAME BEARING the sun throws shadows, so it
overtook its own shadows within ten pixels of the marker bases.

Evidence: `render.py`, `qa.py`, `dossier_check` and `bespoke_check` all passed
the slide. It shipped into the first render and a pixel critic caught it a full
review round later.

**Owned by this phase. Fixed, upgrade 1. See section 3.**

### D2. A solved cast tip, and a different one drawn (SEVERE)

Slide 09 assigned `tx` and `ty` from the deck's own sun solve, never read them
again, and painted a wedge to the frame edge that was thirty two times the
solved length. On a deck whose entire honesty mechanic is that the shadows are
computed, that is the one lie a reader would be entitled to be angry about.

Evidence: every machine gate passed. A pixel critic found it by reading the
source beside the render.

**NOT fixed this run, and the reason is a boundary rather than a shrug.** The
upgrade that covers D1 asks whether a routine painted ANYTHING; D2's routine
painted plenty, just not the thing the arithmetic said. Catching it needs the
slide to DECLARE the segment (`from`, `to`) so the drawn extent can be measured
against the solved one, which is a new authoring contract in the family of
`__akLeaders` and `__akMotifs`. That is a design worth having and it is not
safely boundable in one Phase 12 slot beside two other changes. Parked in
`knowledge/FIELD_NOTES.md` with its shape and its unblocking condition.

### D3. An assertion that could not fail (SEVERE)

Slide 08 argued in type that two stamped tags carry the same seven struck rows,
built the two tags separately in 3D, and shipped nine rows on one against eight
on the other at different insets, so the picture argued the opposite of the
caption.

Evidence, verbatim from the slide source:

```js
window.__akAssert=[{what:"both tags carry the same seven struck rows",
                    expect:7, actual:7, tol:0, unit:"rows"}];
```

`x == x`. It holds for any picture whatsoever, and the deck's own artifacts then
cited it as proof. The same run's slide 05 wrote `+sidePx.toFixed(2)` on both
sides of its scale assertion. The 2026-08-12 contract's whole value is in the
authoring, "you can't write `actual` without deriving it from the thing that
actually drew", and nothing had ever enforced that half.

**Owned by this phase. Fixed, upgrade 2. See section 3.**

### D4. Two suns across nine slides

Slide 03's GL rig keyed from IN FRONT of the subject at `pos [1.2, 2.2, 2.6]`
while every other frame keyed from behind at the deck header's declared azimuth
062, elevation 14. No gate compares light directions between slides.

**NOT fixed. Recommended instead, section 3.** The honest version needs each
slide to declare its key as a vector or an azimuth/elevation pair and a
cross-slide check that they agree with the storyboard's solve. That is cheap
arithmetic once the declaration exists, and the declaration is the work: a
grep-based version would have to understand a GL light position, a 2D
`SUNX/SUNY/SUNZ` triple and a hand-rolled offset as the same thing, and would
be silently wrong in exactly the case that matters.

### D5. A repair reached one of two twin slides

Slides 01 and 02 share a declared stance. Round 1 moved the sun bloom after the
ground fill on 01 and left it sliced flat at the horizon on 02, and applied a
24 px spacing change to 01's row and not 02's, so twelve markers slid sideways
on the deck's FIRST swipe under a camera the header calls unchanged.

**NOT fixed.** A machine version needs slides to declare their shared stance,
which is the same missing declaration D4 wants. Recorded in
`ledger/instincts.json` and in the field notes as process, and folded into the
D4 recommendation, since one declaration would serve both.

### D6. A declared encoding rect that did not contain the ink it proves

Slide 07's `data-encodes` region a was written at y 700 to 840 from camera
arithmetic while every pin head it existed to prove sat at y 571 to 604. The
pair reported a large dE that came entirely from the ground gradient. The gate
PASSED, on the wrong evidence, which is worse than failing.

**NOT fixed. Recommended, section 3.** The check is the same family as D2's:
the machine cannot know what a region is supposed to contain without being
told, and the honest fix is to derive the rect from the same coordinates that
drew the marks rather than from a second arithmetic.

### D7. config/brand.yaml contradicted the enforcer it names

`brand.yaml`'s voice line and its `date_form` style key both said "with a year
use the plain form, 'August 27, 2026'", while its own `date_format` block
listed "August 10" among the bad forms and said never a bare month-day, and
`scripts/caption_check.py` DATE_FORMS hard-fails the plain form on the caption
and on every reader-facing string in `copy.json`. The file gave two answers and
one of them was the one the machine rejects.

Evidence: the scorer read two correctly-set slides as house-rule misses on the
strength of the wrong half. The larger cost is forward-looking: a copywriter
that follows `brand.yaml` literally writes a dated caption the caption gate
then hard-fails, which is a repair round every time a caption carries a year.

**Owned by this phase. Fixed, upgrade 3. See section 3.**

### D8. Artwork craft scored 7 for the eleventh consecutive run

The scorer's named weakest criterion, eleven runs running, this time for the
dead zones: slide 05's inert top 40 percent, slide 04's left-third circle of
confusion reading as a smear rather than a row, slide 03's empty right-centre
quadrant.

**NOT fixed, and it is not a taste problem.** `scripts/value_structure.py`
(2026-08-31) already measures the frame's value structure off the rendered
pixels and deliberately reports rather than gates, at about a 15 percent flag
rate on known-good frames. Nothing measures a DEAD ZONE as such. Recommended,
section 3.

### D9. The COMPLETION GATE has never had a machine behind it (NEW, found here)

`prompts/routine_instructions.md` line 202: "Update each phase to 'done' WITH
its artifact paths as you complete it. The COMPLETION GATE (before merge)
requires every phase done and every artifact existing." Phase 11 step 5 repeats
it: "verify run_state.json shows every prior phase done".

Evidence: `runs/2026-09-01/run_state.json`, the MERGED artifact, records
`directors_room`, `copy`, `art_build`, `pixel_review`, `flow_review`,
`assemble`, `scoring` and `ship` as **"pending"** on a run that did all eight
and shipped. `scripts/gate_status.py` `artifacts_row` opens `run_state.json`
and checks only that it PARSES; nothing anywhere reads `phases`. So the run's
own record of itself is false in a file that is now on `main`, and the named
gate that was supposed to catch that has never existed.

This is the shape render.py's own 2026-08-27 comment already names: "a gate
that is silently off is worse than one never written."

**NOT fixed. Budget was full with D1, D3 and D7, which are the three that
produced or nearly produced a shipped defect. Recommended, section 3, and it is
the first thing I would take next run.**

---

## 2. FRONTIER SCAN

**Focus: (a) LinkedIn platform and algorithm changes that move the craft
numbers.** The stalest legal slot, last scanned 2026-08-21 (12 days), and
distinct from the last three logged foci (2026-08-31 typography and layout,
2026-08-30 agent and automation workflows, 2026-08-29 editorial dataviz and
cartography).

Five searches, two fetches, timeboxed. Aimed deliberately at the HOLE the
2026-08-21 scan recorded (nothing on slide-count effects, aspect ratio, or how
LinkedIn actually renders a document) rather than at the benchmark tables,
which this repo already carries.

**The one finding, and it is a subtraction rather than an addition.** The claim
now circulating through 2026 LinkedIn-algorithm writeups, that feed ranking
carries a "Long Dwell" classifier thresholded at a CONTEXT-DEPENDENT PERCENTILE,
is sourced to LinkedIn's LiGR paper, arXiv 2502.03417. That paper has been
**withdrawn by its own authors**: "We found discrepancies in the claims of the
paper upon further investigation and therefore request to withdraw this
submission from arXiv" (v3, February 2026), and no PDF is served. The other
paper the same writeups cite, LiRank (arXiv 2402.06859), carries no dwell-label
description in its abstract at all. Recorded so no future scan in this slot
spends its budget re-deriving a retracted claim, and so nothing in
`CAROUSEL_CRAFT.md` is ever written up from it.

Everything else was corroboration of what the knowledge base already holds:
documents remain the top format at 7.00 percent engagement on Socialinsider's
2026 benchmark refresh (already carried as tier [B] evidence), 1080 x 1350 at
4:5 is still the rendered shape, and the 8 to 12 slide band is unchanged. The
2026-08-21 hole is still a hole: no source read today reports per-slide alt
text for documents or any change to how a document is rendered in the feed,
which is where an engine parameter would have to move.

**Outcome: nothing applied, one negative result parked.** All three upgrade
slots went to reactive fixes, which is the reactive-first rule working as
written, and the scan's own best result was a claim not to build on.

---

## 3. WHAT CHANGED, WHAT WAS REFUSED, WHAT IS PARKED

### Upgrade 1 (fix, engine): a drawing routine that painted nothing

`render.py` now wraps the 2D canvas path API and measures every `fill()`'s own
path box; `qa.py` **FAILS** when a CALL SITE made at least 3 fills and at least
80 percent of them enclosed no area. The verdict is on the site and not on the
fill because an isolated degenerate fill is ordinary drawing; a site whose fills
all painted nothing is a routine that ran for nothing.

Calibrated before it was wired in, over 22 known-good slides from three decks
(`out/2026-09-01`, `runs/2026-08-31`, `examples/demo-deck`): 10,999 `fill()`
calls at 155 call sites carrying exactly ONE degenerate fill, `ak3d.js`'s
triangle rasteriser at 1 of 9,216 at that site, a ratio of 0.0001 against the
0.8 the gate needs and a count of 1 against the 3. The reconstruction of slide
07's real defect measures 9 of 9.

Cost measured on the 9,386-fill stress slide (`examples/demo-deck/slide-04`):
60 ms of a 280 ms render, all of it the per-fill stack.
`Error.stackTraceLimit` is deliberately left alone, because lowering it to 4
saved nothing measurable and would have truncated the page-error stacks the
same run collects.

### Upgrade 2 (fix, engine): an assertion that cannot fail

`render.py` scans the slide SOURCE for `__akAssert` entries whose `actual` is
textually identical to `expect` or is a bare numeric literal; `qa.py` **FAILS**
them. Assertions carrying `points` are never read here, because the frame
computes their `actual`.

Measured over the 16 assertions in the four slide sets on disk: 7 carry a
hand-written `actual`, 5 of them genuinely derived (`750-96`,
`dx(139)-dx(49)`, `Math.round(window.__G[2])`) and silent, and exactly the two
this run shipped fire. An `actual` folded out of typed literals is weak and is
deliberately NOT flagged, because it does at least name the drawing's own
numbers and it fires on 2 of 7 known-good assertions; it is written up in
SKILL.md as guidance instead.

### Upgrade 3 (fix, scripts + config): the config may not contradict the enforcer

`config/brand.yaml` now says one thing about a dated sentence, and says what
`caption_check.py` actually enforces: month first, ordinal always, a year does
not suspend it. More usefully, the file's own `date_format.good` and
`date_format.bad` example lists are now EXECUTABLE against `DATE_FORMS` on
every `caption_check.py` invocation, and no other line in the file may
prescribe a form the table rejects.

### ONE THING THE SHOWRUNNER SHOULD KNOW

Upgrade 2 FAILS this run's own slides 05 and 08, which is the gate working
rather than a regression: both assertions really are `x == x`, and they are two
of the four defects this retro documents. The deck has already shipped and
`gate_status` is not re-run after Phase 12, so nothing is blocked. It does mean
that re-running `qa.py` over `out/2026-09-01/render` now reports 2 fails where
the shipped `machine_qa.json` reports 0. Every one of the 18 warns is identical
before and after, and `examples/demo-deck` is unchanged at 0 fails / 11 warns.

### REFUSED

- Nothing was loosened. No threshold moved down, no FAIL became a WARN.
- No new runtime dependency. All three upgrades are stdlib and vanilla JS.
- A cross-slide light-direction grep (D4) was refused as written: it would have
  to treat a GL light position, a `SUNX/SUNY/SUNZ` triple and a hand-rolled
  offset as the same thing, and would be silently wrong in exactly the case
  that matters. It needs a declaration first, which is a design and not a
  Phase 12 slot.

### RECOMMENDED TO THE MAINTAINER (in priority order)

1. **A `run_state` row in `scripts/gate_status.py` (D9).** Read `phases` and
   FAIL under `--require` when any phase up to `scoring` is not `"done"`. The
   completion gate is written in the spec twice and has never been machine
   checked, and this run merged a run record that calls eight completed phases
   pending. Small, and it is the first thing I would take next run.
2. **A declared key light per slide (D4 + D5).** `window.__akLight = {az, el}`
   or a unit vector, checked against the storyboard's own solve and against
   every other slide. One declaration answers both the two-suns defect and the
   twin-slide repair miss, and both are pure arithmetic once it exists.
3. **A declared cast segment (D2 + D6).** `from`/`to` in design px for any
   drawn thing whose length is solved, so the drawn extent can be measured
   against the solved one. This is the half of the declared-but-undrawn class
   that upgrade 1 does not reach.
4. **Make the dead zone measurable (D8).** Eleven runs at 7 on artwork craft is
   a machine problem. `value_structure.py` already reads the notan; what is
   missing is a per-region craft-density census that names the largest inert
   rectangle as a fraction of frame, so "fill the dead zone with the deck's own
   vocabulary" becomes a number a critic can be handed instead of a note a
   critic has to notice.

### PARKED (knowledge/FIELD_NOTES.md, 2026-09-01 Phase 12 block)

- The declared-cast-segment contract (D2), with its shape and the reason it is
  a design rather than a slot.
- The LiGR withdrawal, so no future (a) scan builds on a retracted paper.
