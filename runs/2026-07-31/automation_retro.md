# AUTOMATION RETRO, 2026-07-31 (run 21)

Phase 12. This document improves the MACHINE. The editorial retro in Phase 14
improves the content brain.

## 1. THE STANDING REPEAT OFFENDER, AND WHAT THIS PHASE DID WITH IT

`scripts/trend_check.py --window 10` over 2026-07-20 to 2026-07-31 reports this.

```
weakest  8/10  mean 6.5   last 6.0   Artwork craft and genuine detail   worked 2026-07-31
HARD FAILS (3 of 10 runs carried one)
   3x  text against geometry   2026-07-25, 2026-07-29, 2026-07-31   <-- RECURRING
   1x  contrast                2026-07-31
```

**Artwork craft was worked on THIS run**, with `assets/js/akengrave.js`, a
white-line intaglio bench whose central idea is a per-region detail budget
expressed as a drawing system rather than as a subject count. That is the
mechanism-level change No. 20's retro asked for, and it is logged. It is not
worked on again here, because two upgrades to the same criterion in one day is
churn, not improvement, and the honest read of this run is that the craft
mechanism was fine and the LEGIBILITY around it is what capped the score.

**So this phase takes the RECURRING hard fail instead**, text against geometry
and its contrast twin, which is now three runs in ten and was the thing that
capped 6.9 on all three. That is a reactive fix and it takes precedence over any
frontier improvement, per the phase's own rule.

## 2. WHAT ACTUALLY WENT WRONG, WITH EVIDENCE

Walking `run_state.json` phase by phase, the deviation that matters is not a
process gap. Every gate ran, in order, and the ordering fix added on 2026-07-25
(reconciliation before critics) held. The deviation is that **a gate reported
PASS on material a human reader failed.**

The mechanism, exactly. `qa.py`'s `contrast_estimate()` takes ONE background
value per text node, the median of the non-ink pixels across the whole bounding
box. Against a flat ground that is correct and cheap. Against a GRADED ground it
is the thing that hides the defect. This deck's whole visual premise is a lit
paper sheet under one raking key, so every ground in it is graded by
construction. A line of type running across that sheet from its dark end to its
lit end averages to a comfortable ratio while one end of it is unreadable.

The scorer's second report named the site precisely. Slide 07's four ballot-row
labels and two annotation lines "sit BARE on the lit sheet", at 3.3 to 4.4 to 1.
`qa.py` had reported zero contrast warnings on those nodes, because its
thresholds are 2.0 to FAIL and 3.5 to WARN and the box means were above both.
The rubric's hard-fail rule reads "primary text contrast below 4.5 to 1 **at
worst point**". The machine was measuring a mean and the rule is about a
minimum. The only reader who could see the difference was the scorer, at the
ship gate, where the fix costs a whole revision cycle and the score is already
capped.

Same root cause on 2026-07-29 (type metrics) and 2026-07-25 (art-band labels,
where the response was `glyph_ink_contamination`, which measures foreign INK
against the glyphs but says nothing about a ground that is simply too close in
value).

## 3. THE UPGRADE

`contrast_worst_cell()` in `.claude/skills/carousel-engine/qa.py`.

Walks each of a node's measured line boxes in 64 device-px cells, estimates the
background from **that cell's own** non-ink pixels (glyph mask dilated 2 px to
drop anti-aliasing, reusing the existing `_dilate` and `BUSY_INK_DIST`), and
returns the minimum ratio over every cell that carries real glyph ink. Reported
only when it is meaningfully below the box mean, so flat-ground slides produce
no new noise at all.

Tiers. FAIL at worst-cell below 3.0 on primary text. WARN below 4.5, which is
the rubric's own hard-fail line, quoted back at the build. This TIGHTENS the
gate. It can never raise a ratio the old check reported, and the old check is
untouched and still runs.

Calibration, measured rather than guessed. Run against this deck's ten renders
it produced 5 hits and 0 fails, which is the shape a good tripwire has. Three of
the five were real and are fixed below. Two are slide counters at 4.2 and 4.4,
marginal navigation furniture, left alone deliberately (see 5).

Verified by fixing what it found. It flagged slide 05's body copy at 3.9 worst
point against a 6.1 box mean, on the hero, the deck's second most-read slide,
and slide 07's two sponsor attributions at 3.7 against 4.3. Both got a burin
reserve, which is the answer the deck's own reconciliation item 5 already
required and which nobody had applied to those six nodes. Re-rendered, and the
walk now returns 2 hits, both counters, 0 fails, with no new plate clips or
collisions introduced on either slide.

**This is the point of the upgrade and it earned itself inside the same run.**
Three nodes on shipped material were below the rubric's own line after two full
scoring cycles, five revision rounds, five pixel critics and two scorers had all
signed off. No human reader found them. A 60-line function did.

## 4. FRONTIER SCAN

Not run this cycle, and this is a deliberate deferral rather than an omission.
The phase allows 0 to 3 upgrades and directs that reactive fixes come first at a
daily cadence of 0 to 1. Two upgrades were already logged during the run
(`akengrave`, the type-pairing audit) and this is the third. The rotation slot
that is stalest is procedural art portable to offline Canvas/SVG, last scanned
2026-07-21, and it should be the focus on 2026-08-01. A `scan_log` entry
recording the deferral and the reason is appended so the rotation does not
silently lose a turn.

## 5. WHAT IS DEFERRED, NAMED

**The slide counters at 4.2 and 4.4 worst point.** Slides 03 and 07. This was
attempted during the run and made things worse. A background plate behind the
counters cleared two furniture contrast warnings and created two new plate clips
on slides 08 and 09. The plate was reverted and the ink brightened to `#EAF4EC`
instead. The counters are 24 px navigation furniture carrying no fact, they are
0.1 to 0.3 below the line at their single worst cell, and the cheap fix is known
to break something else. The durable answer is a deck-level rule that the
counter never sits on the lit half of a graded sheet, which belongs in
DESIGN_DOCTRINE rather than in a per-run patch. Deferred to 2026-08-01.

**"Outside safe zone" and "top-loaded composition" warns**, 2 runs each. Both
are composition warnings that the pixel critics currently adjudicate by eye and
neither has ever become a hard fail. Left alone.
