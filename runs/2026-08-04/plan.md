# RUN PLAN - 2026-08-04 - Carousel No. 25

## 0. Wake state

- Run date (America/Anchorage): 2026-08-04
- carousel_no: 25 (ledger/topics.json holds 24 entries)
- Queued assignment: NONE. `prompts/NEXT_RUN.md` does not exist.
- Bootstrap: OK (playwright, pypdf repaired, chromium ok)
- Branch policy: run branch `claude/carousel-2026-08-04`, PR ready (not draft),
  merged to main in this run per CLAUDE.md. The session-injected feature-branch
  directive is overridden by repo policy, which says so explicitly.

## 1. Seasonal Alaska context (so scouts do not miss the obvious)

- The Alaska primary election is 2026-08-18, fourteen days out. Wide open
  governor's race, Ballot Measure 1 on contribution limits on the same ballot.
  Two decks have already worked this ground (No.17, No.21), so the bar for a
  third election deck is a genuinely new document.
- Peak wildfire season in the Interior; smoke is a live public grievance.
- Bristol Bay sockeye winding down, Upper Cook Inlet runs active, peak
  processing and peak air-taxi season.
- Legislative interim. Federal fiscal year end approaching, so solicitations
  and awards cluster in August.
- Cook Inlet gas shortfall and Railbelt reliability are the standing energy
  story underneath every data-center item.
- Alaska State Fair opens late August. Freeze-up and PFD announcement are out
  of window.

## 2. Variety constraints derived from ledger/artwork.json

FORBIDDEN hero structures (last 4, decks 21 to 24):
- No.21 THE ENGRAVED INSTRUMENT (white-line intaglio sheet on a copy stand)
- No.22 THE UNFILLED SHEET (Imhof relief Alaska, eight camera stations)
- No.23 THE POSTING LANES (cabinet-oblique instrument bed, fixed camera)
- No.24 THE CUT BLOCK (axonometric solid, affine map transfer, hachure)

FORBIDDEN atmospheres (last 3):
- No.22 HIGH-ALTITUDE SHEET LIGHT
- No.23 LOW-ANGLE TERMINAL GLOW
- No.24 SEA FOG AT THE BASIN

FORBIDDEN continuity devices (last 2), AND a standing calcification flag:
- No.23 THE DEADLINE RAIL (lower-band horizontal quantity strip)
- No.24 THE SCALE BAR + SOLID/PHANTOM RULE + TENURE INKS
- CALCIFICATION, flagged by the scorer on No.24 in its own words: "a horizontal
  quantity strip in the lower band that changes shape per slide is now the
  third consecutive run's device A", after No.20's REGISTER and No.23's
  DEADLINE RAIL. This run may NOT use a lower-band horizontal strip, rail,
  comb or register as its device A. That is a hard constraint on this run, not
  a preference.

FORBIDDEN hook archetypes (last 3):
- No.22 THE WITHHELD MAP, No.23 THE OPEN WINDOW, No.24 THE MISMATCHED PAIR

FORBIDDEN palette families (last 3):
- No.22 GRAPHITE SHEET AND BUFF CARD (and its recorded caveat, that it still
  read as the series' default cold arctic navy and cost the variety score)
- No.23 INK PLUM AND QUARTZ
- No.24 TUNDRA AUTUMN OVER COLD WATER

FORBIDDEN type pairings (last 2):
- No.23 Bricolage Grotesque + Manrope + JetBrains Mono
- No.24 Fraunces + Archivo (width axis) + JetBrains Mono

Light-deck allowance: a light base register is permitted at most once per 8
runs. Last light deck was No.21's copy-stand register on 2026-07-31, four runs
back, so a light deck is NOT available this run. Dark arctic base.

## 3. Variance dials, chosen deliberately

Recent dials: No.20 (3,3,3), No.22 (4,2,2), No.23 (5,4,4), No.24 (4,3,4.5).

THIS RUN: DESIGN_VARIANCE 3, VISUAL_DENSITY 5, TYPE_TEMPERATURE 2.

Justification, and it is the whole argument of this plan. Design variance has
run 4 or 5 for three consecutive decks and artwork craft was the weakest
criterion in all three anyway. Buying a novel chassis every run has not bought
craft. So this run spends its variance budget the other way, at 3, on a chassis
close to house center, and puts the saved effort into RENDERED QUALITY inside
that chassis. VISUAL_DENSITY 5 has never been used in 24 runs and is the direct
antidote to the two defect classes that keep shipping (dead lower zones,
top-loaded composition): a density-5 deck has no room for an empty band.
TYPE_TEMPERATURE 2 is cool grotesk, against 4, 4.5 and 4 in the last three.

## 4. Top instincts injected into every subagent this run

1. Never treat a machine_qa PASS as composition approval. qa.py's collision
   check is DOM-ONLY, so any label against Canvas or SVG geometry can collide
   freely and still return PASS with zero warns. Every art-band label ships on
   an opaque knockout plate by default. (0.98/0.99)
2. Size every plate from the MEASURED string, never a guessed constant.
   JetBrains Mono 24px at 0.10em advances exactly 16.8px per character; the eye
   estimates 14 and loses three characters per twenty. Compute or measure. (0.95)
3. Never nest a colour helper. lerpHex returns rgb(), feeding rgb() into a hex
   parser gives NaN on every channel, canvas silently keeps the previous
   fillStyle, and a whole region renders the wrong colour with a clean gate.
   Precompute endpoints as hex literals. (0.97)
4. Put the knockout ON the text element, never a hand-sized scrim. A scrim
   sized by hand cannot track a wrapped block; a plate on the element grows
   with the copy. (0.94)
5. A banded fill that paints each band down to the frame bottom must run
   light-to-dark. Dark-to-light means the lightest band covers everything
   behind it and the whole mass flattens to one value. (0.95)
6. Grade the 2D atmosphere BEFORE compositing any GL frame. AKPOST.grade costs
   about 34 seconds on a canvas that has already had WebGL pixels drawn into
   it, and about 0.9 seconds before. (0.95)
7. An absence has no magnitude. Never draw a count of zero as a bar, arc, area
   or radius; encode presence at full weight so the missing thing is a
   fixed-size hole in a dense field. (0.93)

## 5. TREND BLOCK (pasted verbatim from scripts/trend_check.py --window 10)

```
TREND -- generated by scripts/trend_check.py over the last 10 scored run(s), 2026-07-23 to 2026-08-03.

REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  'worked' is a text match over ledger/upgrades.json prose, so it can UNDER-report:
  an upgrade that fixed a criterion without naming it reads as 'never'. Check before acting.
  weakest  7/10  mean 6.22   last 6.0    Artwork craft and genuine detail        worked 2026-07-31 (3 run(s) ago)  <-- STALE
  weakest  2/10  mean 6.33   last 5.0    Legibility and platform fitness         worked never (never)  <-- STALE
  weakest  1/10  mean 6.0    last 6.0    Legibility &amp; platform fitness       worked never (never)  <-- STALE

HARD FAILS (3 of 10 run(s) carried one)
   3x  text against geometry       2026-07-25, 2026-07-29, 2026-07-31  <-- RECURRING
   1x  contrast                    2026-07-31

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   3 run(s)  warns:top-loaded composition                          latest 2026-08-01
   2 run(s)  warns:busy art under text                             latest 2026-08-01

SCORE, most recent runs
  07-25 6.90  07-26 6.90  07-29 6.90  07-30 8.09  07-31 6.90  08-01 7.92  08-02 8.37  08-03 6.90
```

## 6. THE ONE STANDING WEAKNESS THIS RUN ATTACKS, AND HOW

THE WEAKNESS: artwork craft and genuine detail, weakest in 7 of the last 10
runs, mean 6.22, last scored 6.0. It has been the target of two upgrades in
twenty-four runs and it has not moved. Read as a prediction rather than a
report, it says today's deck scores 6 on artwork unless this run does something
different at planning altitude.

THE DIAGNOSIS, and it is No.24's own retro rather than a guess. No.24 built a
real mechanism (akhachure, stroke width from local slope, rotation from
aspect), a pixel critic who was not told which region was which named the heavy
basin and the fine plateau correctly, and then qa.py measured the same
mechanism at AUC 0.51, chance, and 0 percent visible at 432px. The mechanism
was real and invisible. Phase 1's craft refresh found the name for that failure
and it is five centuries old. Notan is value structure at two tones, the squint
test made formal, and its operative sentence is that if the thumbnail turns to
muddy grey you need more value separation, not more drawing.

THE ATTACK, in three parts, each of which is checkable and each of which is
somebody's job in a later phase.

(a) NOTAN FIRST, IN THE DOSSIER. Every slide dossier states its two-value mass
    arrangement BEFORE its technique stack: which regions are the dark mass,
    which are the light mass, and where the boundary runs. A slide whose notan
    is one grey field is redesigned at Phase 5, where it costs a paragraph,
    rather than at Phase 10, where it costs a rebuild.

(b) EVERY MECHANISM DRIVES VALUE, NOT ONLY GEOMETRY. This is the one multiply
    No.24's retro asked for, generalised into a law for this deck. Any
    generative system whose parameter comes from a story number must move
    lightness with that number in the same pass, not only width, spacing,
    count or radius. Stated per slide in dossier field 8 so the pixel critics
    can verify it, and stated as a deck-level rule in the storyboard header.

(c) THE MECHANISM IS A PROPERTY OF THE DECK. No.24's other finding was that
    four critics independently reported its signature field was absent from
    every slide that was not the hero. The storyboard must name where the
    mechanism runs on EVERY slide, including the breather and the close, or
    say in writing why it is held out there.

SECONDARY, because they are cheap once (a) is done. VISUAL_DENSITY 5 and
DESIGN_DOCTRINE's composed bottom third together kill the top-loaded and
dead-lower-zone warns that shipped in three of the last ten runs. And every
art-band label on a computed opaque knockout plate kills the text-against-
geometry hard fail that has recurred three times, by construction rather than
by registration tuning.

## 7. Phase plan

Phases 2 and 3 are running or next: six scouts out, then the fact-checker,
then claims_check as a gate. Phase 3.5 refreshes the public docket. Phase 4
runs dedupe_check before the directors room, reading every LIKELY DUPLICATE in
full and never through head or tail. Phase 5 spends real effort, three
treatment directors on three lenses not used together last run. Phase 6 is the
caption room with two directors and a critic. Phases 7 to 10 build, review,
assemble and score. Phase 11 ships and merges. Phase 12 upgrades the machine.
Phase 13 drafts the email. Phase 14 closes the run.
