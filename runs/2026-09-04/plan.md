# RUN PLAN — Alaska.Ai Carousel No. 50 — 2026-09-04

## Date

Anchorage local at wake was 2026-09-04, 23:09 AKDT. `runs/2026-09-04/` did not
exist, so this run takes its own Anchorage date. Prior shipped runs end at
2026-09-03 (No.49). Carousel number is 49 topic entries plus one, so No. 50.

## Ledgers read

topics 49 entries, artwork 49, captions 49, instincts 192 (166 at or above
0.7 confidence), upgrades 131 with 42 scan_log entries, docket 24 items,
watch.json present with 0 bills and 0 hearings.

## TOP INSTINCTS injected into every subagent this run

1. A machine_qa PASS is never composition approval. qa.py's text collision
   check is DOM only, so any label set against Canvas or SVG geometry can
   collide freely under a green gate. (0.99, 0.98)
2. A constraint you can't point at is a constraint you invented. There is no
   context or token budget in this routine. (0.99)
3. Grain is a small repeating tile, never a full frame feTurbulence rect. (0.99)
4. Size every plate from the MEASURED string, never a guessed constant.
   JetBrains Mono at 24px with 0.10em tracking advances 16.8px per character
   and the eye guesses 14. (0.95)
5. Re-run the dedupe gate whenever the candidate story changes; dedupe_check is
   stateless and answers whatever fingerprint it is handed. (0.97)

## VARIETY CONSTRAINTS (hard, from ledger/artwork.json)

Forbidden hero structures, last 4: THE SPINE WALL AND THE UNSEWN BLOCK
(08-31), THE COUNT LINE AND ITS OWN SHADOW (09-01), THE MEASURED SECTION of
ballot edges (09-02), THE NIGHT APRON / runoff mirror (09-03).

Forbidden atmospheres, last 3: first hour under a high cloud lid (09-01),
raking fluorescent on cut paper (09-02), rain at a 17 degree bearing gated by
a lamp cone (09-03).

Forbidden continuity devices, last 2: THE RIFFLE LANE panorama plus the
threshold rule the light never touches (09-02), the chained conductor THE WIRE
IS ONE WIRE plus the unlit band (09-03).

Forbidden hook archetypes, last 3: THE COUNTING ERROR (09-01), THE EXHIBIT
THAT CHANGED NO VOTES (09-02), THE MACHINE THAT ISN'T MOVING (09-03).

Forbidden palette families, last 3: muskeg and galvanized steel (09-01),
ballot edge under a fluorescent tube (09-02), sodium free island night (09-03).

Forbidden type pairings, last 2: Space Grotesk with JetBrains Mono (09-02),
Instrument Serif with Archivo and JetBrains Mono (09-03).

Light deck budget: allowed once per 8 runs. 2026-08-30 was the high key paper
white register, 5 runs ago, so a light deck is NOT available this run. The
deck is a dark arctic register.

## VARIANCE DIALS, chosen deliberately

design_variance 4, visual_density 3, type_temperature 2.

The last four runs all sat high on density (a mass of cut sheet edges, a wall
of spines, a rain field, a marker population). Dropping density to 3 while
holding design_variance at 4 pushes this run toward FEWER, LARGER, MORE FULLY
DRAWN objects, which is the same direction the standing weakness points.
type_temperature 2 keeps the type cool and structural so the art carries the
frame.

## SEASONAL ALASKA CONTEXT (first week of September 2026)

Legislature is out of session (interim), so BASIS is quiet and watch.json
reporting zero hearings is normal, not a broken sweep. Alaska State Fair runs
to Labor Day, September 7th. School year has started statewide. Fairbanks
North Star Borough municipal election is October 6th, and Anchorage's
Assembly is back in regular session. Salmon seasons are closing out and
processors are reporting. Fire season is winding down and freeze-up planning
starts. Cook Inlet gas contracting decisions cluster ahead of heating season.
PFD distribution lands in early October. Federal fiscal year ends September
30th, which pulls solicitations, awards and obligations into this window, and
that is the single strongest seasonal signal for Beat D.

## STANDING WEAKNESS (scripts/trend_check.py --window 10, 2026-08-25 to 2026-09-03)

```
REPEAT OFFENDERS (criterion, times weakest, mean, last worked on)
  weakest  8/10  mean 6.7    last 7.0    Artwork craft and genuine detail   worked 2026-08-31  <-- STALE
  weakest  1/10  mean 7.7    last 8.0    Story arc and swipe momentum       worked 2026-07-30  <-- STALE
  weakest  1/10  mean 8.1    last 9.0    Deliverable completeness           worked never       <-- STALE

HARD FAILS (0 of 10 runs carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   7 runs  warns:top-loaded composition       latest 2026-09-02
   5 runs  warns:busy art under text          latest 2026-09-01
   5 runs  warns:outside safe zone            latest 2026-09-02
   5 runs  warns:contact shadow               latest 2026-09-03
   4 runs  warns:tiny-text                    latest 2026-09-02
   2 runs  warns:art touching glyphs          latest 2026-08-27

SCORE, most recent runs
  08-27 8.67  08-28 7.93  08-29 8.51  08-30 8.79  08-31 7.79  09-01 8.89  09-02 8.52  09-03 8.81
```

## THE ONE STANDING WEAKNESS THIS RUN ATTACKS, and how

**Artwork craft and genuine detail.** Weakest in 8 of the last 10 runs at a
mean of 6.7, which is a full point and a half below every other criterion.
No.49 proved the method works by taking top-loaded composition, naming it in
the plan, designing against it in the dossiers, and measuring the result with
value_structure rather than asserting it. Same method, new target.

The diagnosis this run works from, read off the recent scorer notes and the
defect table: the decks that lose this criterion lose it in the MIDDLE
DISTANCE. The hero object is drawn well and the far field is atmosphere, and
between them sits a zone that is one flat value with nothing in it, so a
reader who looks past the anchor finds nothing to look at and the frame reads
thin at exactly the moment the swipe would have paid off.

The attack, decided here and binding on every Phase 5 dossier:

1. **THREE SCALES OF DRAWN MATERIAL IN EVERY REGION.** Each dossier declares,
   per region, what carries the silhouette (metres), what carries the surface
   (centimetres) and what carries the tooth (millimetres). A region that can
   only name two of the three is unfinished and is redrawn before it renders,
   not after a critic says it reads flat.
2. **THE MIDDLE DISTANCE IS THE SUBJECT OF ITS OWN PASS.** Every slide names
   one middle ground population that is drawn, not washed, and that is
   materially different from both the anchor and the far field.
3. **DENSITY DOWN, DETAIL UP.** Dial 3 rather than the 4 and 5 of the last
   four runs. Fewer objects, each one actually finished. A frame with six
   fully drawn things beats a frame with sixty implied ones, and the second
   is what the bespoke gate's drawn share measures.
4. **THE BENCH, NOT THE BOX.** bespoke_check fails a drawn share under 45
   percent and the recurring cause is axis aligned rectangles standing in for
   drawing. The techniques chosen in Phase 5 come off the library's bench
   (engraving, stipple, contour, relief, flow) and every fillRect in the deck
   has to justify itself as a real edge in the depicted world.

Not attacked this run, and named so the deferral is not silent: top-loaded
composition, which No.49 worked three runs ago and which value_structure now
measures, so it is under instrumentation and gets held rather than pushed.

## PHASE 1 note

Craft refresh runs before the scouts, per the search budget rule. Six scouts
are capped at 25 WebSearch calls each in their briefs.
