# RUN PLAN — 2026-08-16 — Carousel No. 35

Showrunner wake record. America/Anchorage date 2026-08-16 (UTC 2026-08-17 07:26,
which is 23:26 AKDT on the 16th, the same wake position as every run in the
ledger).

## 0. Queued assignment

`prompts/NEXT_RUN.md` does NOT exist. No maintainer directive is queued, so
Phase 4 selects freely from this run's own research.

## 1. Bootstrap

`bash .claude/skills/carousel-engine/bootstrap.sh` completed. playwright, pypdf,
img2pdf, pillow, numpy installed; pypdf import was broken by the cryptography
rust-binding panic and self-repaired; chromium ok.

## 2. Carousel number

`ledger/topics.json` holds 34 entries, so this is **carousel No. 35**.

## 3. TOP INSTINCTS injected into every subagent this run

1. **A constraint you can't point at is a constraint you invented** (0.99).
   There is no context or token budget in this routine. A blocked run reports an
   error; a rationalising run writes an essay. Draw the next slide.
2. **Never treat a machine_qa PASS as composition approval** (0.99). qa.py's
   text-collision check is DOM only, so any label set against canvas or SVG
   geometry can collide freely and still return zero warns.
3. **Prototype the hero through the real gates BEFORE writing the dossier**
   (0.90). No.33 rendered six scratch slides and qa.py failed all four map
   compositions for top-loaded composition at 0, 49, 38 and 0 percent bottom
   third density. The deck's best image and its worst gate failure were the
   same picture.
4. **No machine gate can count claims** (0.92). Any on-slide string that
   aggregates verified claims into a new number is a fresh factual assertion and
   is re-derived in aggregates.json at Phase 8.
5. **Brief a scorer, a critic and a fact-checker with CLAIMS and invite them to
   disprove them, never with conclusions** (0.85). Given eight repairs to
   verify, a scorer found the two that had not landed, and they were exactly the
   two that had been mis-diagnosed.

## 4. VARIETY CONSTRAINTS derived from ledger/artwork.json

Reading entries No. 31 through No. 34 (2026-08-12, 08-13, 08-14, 08-15) plus
No. 30 (2026-08-09) where the window reaches back that far.

FORBIDDEN this run:

- **Hero structures (last 4)**: THE FALLING FRAME (No.31, scale itself as the
  variable, nine rungs from 670 km to twenty feet); THE LOCKED CHASE (No.32,
  letterpress composing stone at a fixed 30 degrees); THE EQUAL-AWARD PROJECTION
  (No.33, one chart sheet square on, projection as the variable); THE CHILD'S EYE
  LINE (No.34, nursery floor under a steadily dollying camera).
- **Atmospheres (last 3)**: LOCKUP RAKE (No.32); NEAR-EDGE PLATE LAMP (No.33);
  HALLWAY BACKLIGHT, ROOM FOG (No.34).
- **Continuity devices (last 2)**: No.33's ONE-AWARD RING plus its updating
  projection note; No.34's empty DUE field, receding toy and sheet grammar.
- **Hook archetypes (last 3)**: THE HONEST WITNESS (No.32); THE CONTRADICTED
  ARTIFACT (No.33); THE SUBJECT'S EYE LINE (No.34).
- **Palette families (last 3)**: TYPE METAL AND NEWSPRINT (No.32); PLATE NIGHT
  AND REGULATED MAGENTA (No.33); CARPET WOOL AND HALLWAY BLUE (No.34).
- **Type pairings (last 2)**: Bricolage Grotesque + Fraunces + JetBrains Mono
  (No.33); Unbounded + Manrope + JetBrains Mono (No.34).

Note on type: the library is Fraunces, JetBrains Mono, Space Grotesk, Archivo,
Manrope, Instrument Serif, Bricolage Grotesque, Unbounded. Instrument Serif and
Space Grotesk have both been idle for several runs. Two similar sans faces
together is a type crime, so a fresh trio may not simply pair Space Grotesk with
Archivo. The full-ledger pairing audit (instinct 0.85) runs in the directors
room before type is locked, and the novelty claim is written as a sentence
naming which decks used each face.

## 5. VARIANCE DIALS, chosen deliberately

Recent dials, so they can be varied rather than repeated: No.30 was 5 / 2 / 3.5,
No.32 was 4 / 4 / 2, No.33 was 5 / 5 / 5, and No.34 abandoned the three-dial
vocabulary entirely for a four-field set.

This run returns to the three declared dials and picks a combination the ledger
has not held:

- **DESIGN_VARIANCE 4.** Far from house center, but one notch below No.33's 5,
  because this run spends its ambition on per-region craft rather than on
  conceptual distance (see section 7).
- **VISUAL_DENSITY 3.** Deliberately mid. No.33 ran 5 and No.30 ran 2. A mid
  density is the harder discipline, because it removes both the "fill it" and
  the "it is meant to be sparse" excuses, and the standing weakness this run is
  attacking lives exactly there.
- **TYPE_TEMPERATURE 4.** Warm, serif-forward. No.32 ran 2 and No.34 ran a cold
  wide grotesk display. A warm display register has not led a deck since No.30.

Final dials are re-confirmed in the storyboard header once the story is known;
if the story pushes them, the storyboard says so and says why.

## 6. SEASONAL ALASKA CONTEXT (so scouts do not miss the obvious)

- **Alaska primary election, August 18th, 2026**, two days out. Election
  administration, deepfake law, and the voter-roll story are all live, and the
  voter roll was No.28 on 2026-08-07 so it is inside the 30-day dedupe window.
- Legislature out of regular session. An LNG-focused special session has been
  discussed publicly.
- **Federal fiscal year ends September 30th**, so solicitations, award
  announcements and comment deadlines cluster through August and September.
- Cook Inlet winter gas supply is the running Southcentral anxiety. As of the
  2026-08-16 collector reading, storage is 6.96 Bcf, 53.5 percent of design,
  with injection restriction and withdrawal restriction both active.
- Alaska State Fair opens in Palmer late August. School year starting across
  most districts. University fall semester starting.
- Salmon season winding down (Bristol Bay finished, Southeast coho running).
  Fall subsistence hunts opening. Wildfire season tailing off. Arctic shipping
  season at its peak. Fall storm season approaching for western Alaska.
- PFD amount is announced around late September; distribution in October.

## 7. TREND — the standing weakness this run attacks

Verbatim from `python scripts/trend_check.py --window 10`:

```
TREND -- generated by scripts/trend_check.py over the last 10 scored run(s), 2026-08-04 to 2026-08-15.

REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  'worked' is a text match over ledger/upgrades.json prose, so it can UNDER-report:
  an upgrade that fixed a criterion without naming it reads as 'never'. Check before acting.
  weakest  8/10  mean 6.1    last 6.0    Artwork craft and genuine detail        worked 2026-08-07 (6 run(s) ago)  <-- STALE
  weakest  2/10  mean 6.15   last 7.0    Legibility and platform fitness         worked never (never)  <-- STALE

HARD FAILS (0 of 10 run(s) carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   5 run(s)  warns:top-loaded composition                          latest 2026-08-15
   4 run(s)  warns:outside safe zone                               latest 2026-08-09
   3 run(s)  warns:tiny-text                                       latest 2026-08-13
   3 run(s)  warns:art touching glyphs                             latest 2026-08-08
   2 run(s)  warns:text collision                                  latest 2026-08-06
   2 run(s)  warns:contact shadow                                  latest 2026-08-15

SCORE, most recent runs
  08-06 7.93  08-07 8.55  08-08 8.02  08-09 7.57  08-12 8.42  08-13 8.08  08-14 8.45  08-15 7.77
```

### The ONE standing weakness this run attacks, and how

**ARTWORK CRAFT AND GENUINE DETAIL.** Weakest criterion in 8 of the last 10
scored runs, mean 6.1, and 6.0 on the most recent run. That is not a fact about
the past. Read as a prediction it says today's deck scores about a 6 on artwork
unless this run changes something structural, and the place to change it is here
and in the Phase 5 dossiers, not in a repair pass at Phase 9.

Read the two data points together before choosing the attack. No.34 climbed to
rung 1 of the rendered ladder, real GPU PBR with volumetric fog and authored
contact occlusion, and STILL scored 6.0 on artwork craft. No.32 used no GPU at
all, ran akengrave across all nine frames, and scored 8.08 overall. So the
weakness is not the rung. Reaching for a more expensive renderer has now been
tried and did not move this number.

What the failing criterion actually measures is DESIGN_DOCTRINE section 5, the
zoom test, craft in every region. A smooth physically-rendered material is
beautiful and has no marks in it, so the deck's detail budget all lands in the
annotation furniture, and the furniture concentrates where the labels are, which
is the top two thirds. That is also, precisely, why `top-loaded composition` is
the number one recurring machine warn, present in 5 of the last 10 runs and
latest on 2026-08-15. The two findings are one finding.

So the attack, declared now and binding on Phase 5:

1. **The deck's primary bench is a DRAWN one that produces marks across the
   whole frame by construction**, not a smooth render decorated afterwards.
   Hatching, engraving, stipple, contour or relief driven by a real height
   field, so that detail is a property of the substrate rather than a budget
   spent near the labels. Rung choice follows the story; a GPU hero is allowed
   only if it sits ON such a substrate rather than replacing it.
2. **The bottom third is designed FIRST on every slide.** Field 4a is written
   before the layout map, not after, and it names something with modeled tone.
   Any slide that cannot name one is a breather and is declared as one.
3. **Prototypes go through the real gates before any dossier is written.** Per
   instinct 0.90 and the No.33 precedent, scratch slides are rendered and run
   through `qa.py` and `bespoke_check.py` first, and their findings are binding
   on all nine dossiers. This is what turned a predicted 6 into an 8.45 once
   already.
4. **The craft claim is made falsifiable before the build** (instinct 0.90 on
   palette divergence, generalized). The storyboard states a measurable target
   for per-region detail and hands the test to the pixel critics, rather than
   asserting richness in prose.

The second repeat offender, **legibility and platform fitness** (weakest 2 of
10, worked never), is NOT this run's declared target and is being deferred
deliberately rather than silently. Its mean of 6.15 sits inside the same band as
artwork craft, but it has been the weakest criterion a quarter as often, and the
two share a root cause in the 432px feed test, so a real fix to per-region craft
plus the standing thumb review should move both. Phase 12 is told the same, and
if artwork craft clears this run, legibility is the next declared target.

## 8. Phase order

Standard, per `prompts/routine_instructions.md`. Six scouts spawned in parallel
at wake for Phase 2, so Phase 1's craft refresh and the knowledge-base read run
against the same clock.
