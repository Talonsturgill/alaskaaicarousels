# RUN PLAN — Alaska.Ai Carousel No. 43 — 2026-08-28

## Date

Woke at 23:17 Anchorage on 2026-08-27 with `runs/2026-08-27/` already holding
No.42's shipped deck. The run date is therefore 2026-08-28, the first date with
no run directory, which is also the date Anchorage rolls into within the hour.
Recorded in `run_state.json` under `date_note`.

carousel_no = 43 (42 entries in ledger/topics.json).

No `prompts/NEXT_RUN.md` exists, so story selection is this run's own.

## Seasonal Alaska context (late August)

Alaska Legislature is out of session (interim, committee hearings only). Alaska
State Fair is running in Palmer through Labor Day. Bristol Bay salmon season has
wrapped and the fall silver run is on. School year has started statewide. Fall
hunting seasons are open, moose and caribou. Termination dust and freeze-up are
six to ten weeks out, which is when the gas and power beats sharpen. PFD amount
announcement and the October payment sit just ahead. AFN convention prep is
under way for October. Wildfire season is winding down. Federal fiscal year ends
September 30th, which pushes grant, solicitation and procurement deadlines into
the next four weeks.

## TOP 5 INSTINCTS (confidence >= 0.7, injected into every subagent brief)

1. (0.99) Never treat a machine_qa PASS as composition approval. The pixel
   critics judge composition, hierarchy and collision at full size and at thumb.
2. (0.99) Before rendering, sanity-check long serif or body copy line counts
   against any fixed-position labels, bars or plates. DOM text overlaps pass
   machine QA and fail the eye.
3. (0.98) qa.py's text-collision check is DOM-only. Any label positioned against
   Canvas or SVG geometry can collide freely and the gate still returns PASS.
4. (0.99) A generated block pasted into a run record goes stale the moment
   another round runs. Re-sync `gate_status.py --sync` after every round.
5. (0.97) A constraint you cannot point at is a constraint you invented. There
   is no context budget in this routine. NO EMPTY RUNS.

## VARIETY CONSTRAINTS (derived from ledger/artwork.json)

FORBIDDEN hero structures (last 4 decks, 39 to 42):
- 39 the vacant machined cradle on a dry inspection bench
- 40 the 750-pad municipal apron, one table re-projected
- 41 the horizon ladder, real landscapes indexed by award end year
- 42 the sounding column, a to-scale vertical section of one night's atmosphere

FORBIDDEN atmospheres (last 3):
- 40 high mast and illuminator, single distant parallel key plus IR fill
- 41 the travelling day, one late-August day swept across nine frames
- 42 supercooled cloud interior at night, no lit surface anywhere

FORBIDDEN continuity devices (last 2):
- 41 GOLD IS MEASURED, BLUE IS MODELLED (colour-level)
- 42 INK IS RECORDED, VOID IS MODELED (texture-level) plus the altimeter tape

FORBIDDEN hook archetypes (last 3):
- 40 the order of operations running backwards
- 41 two figures, one scale (a ratio read as pure size)
- 42 the count against the singular

FORBIDDEN palette families (last 3):
- 40 NIGHT APRON, IR AND SODIUM
- 41 LOW SUN, YELLOW BIRCH
- 42 cold droplet blues on near black

FORBIDDEN type pairings (last 2):
- 41 Fraunces + Space Grotesk + JetBrains Mono
- 42 Instrument Serif + JetBrains Mono

AVAILABLE and clean this run: Archivo (last used 40, out of window),
Bricolage Grotesque (39, out of window), Manrope, Unbounded (not used in the
last four decks at all).

### VARIANCE DIALS (deliberately different from recent runs)

- design_variance 4 (No.42 ran high concept at low chroma; this run keeps
  concept ambition and adds colour range)
- visual_density 3 (No.42 ran dense mark-field texture across nine frames and
  the scorer still read the hero as texture without internal form. A lower
  density with more per-mark craft is the corrective)
- type_temperature 4 (warmer, more editorial voice than 42's two-family
  instrument register)

## STANDING WEAKNESS THIS RUN ATTACKS

`trend_check --window 10` says:

```
REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)
  weakest  9/10  mean 6.75   last 7.0    Artwork craft and genuine detail        worked 2026-08-25 (2 run(s) ago)
  weakest  1/10  mean 7.83   last 8.0    Copy                                    worked 2026-08-27 (0 run(s) ago)

HARD FAILS (0 of 10 run(s) carried one)
  none in this window

DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)
   3 run(s)  warns:top-loaded composition                          latest 2026-08-27
   3 run(s)  warns:busy art under text                             latest 2026-08-27
   2 run(s)  warns:art touching glyphs                             latest 2026-08-27
   2 run(s)  warns:outside safe zone                               latest 2026-08-27

SCORE, most recent runs
  08-16 8.91  08-18 8.33  08-19 8.07  08-20 8.39  08-21 8.54  08-25 8.66  08-26 8.51  08-27 8.67
```

**THE ONE WEAKNESS THIS RUN ATTACKS: artwork craft and genuine detail, weakest
in nine of the last ten runs, mean 6.75.**

Read the shape of it rather than the label. The four warn classes that keep
recurring are all the SAME defect wearing four names: art and type are fighting
for the same pixels. "Busy art under text", "art touching glyphs", "top-loaded
composition" and "outside safe zone" are what a deck produces when the artwork
is authored first and the type is placed onto it afterwards, so every slide ends
up needing a reserve carved out of finished art. No.41 then made it worse by
carving those reserves as gradient ellipses after the fact and left an arc
across six slides.

So the attack is structural and it happens in Phase 5, not in a Phase 9 repair:

1. **THE TYPE ZONE IS A DESIGNED ELEMENT OF THE ART, NOT A HOLE IN IT.** Every
   dossier names the object, plane or material that the type sits ON, by name,
   with its own hex and its own lighting. A masthead band that is a real thing
   in the scene (a paper strip, a machined face, a shadowed plane) can carry
   type at any density around it. A gradient scrim cannot.
2. **DENSITY IS SPENT WHERE THE EYE IS, NOT EVERYWHERE.** visual_density 3 is
   chosen for this reason. Each slide declares ONE region that gets the
   expensive marks and at least one region that is deliberately quiet. That is
   the line-weight hierarchy the rubric's 10 descriptor asks for and the thing
   nine runs of uniform field texture have not delivered.
3. **THE HERO CLIMBS THE RENDERED LADDER** (akthree GPU PBR or an aksdf
   raymarch, akpost graded), with its designed Canvas fallback and the snapshot
   sentinel checked. No.42's hero was a raymarch extinguished down to a density
   field, which is how a rendered hero scores as texture without internal form.
   This run's hero keeps its lit faces.
4. **LOWER THIRD CARRIES MODELLED TONE.** dossier_check field 4a is a gate, and
   the dead lower zone has been named by the scorer repeatedly. Every dossier
   names what the bottom band CARRIES as a thing with form, never a plate.

## Craft refresh notes (Phase 1)

Two searches, appended to FIELD_NOTES as a dated entry. Headline for this run:
document posts still lead the format table on dwell time, 8 to 12 slides is the
performing band (this deck ships 9), and reporting on the March 2026
"Authenticity Update" says the first-comment LINK workaround is now read as
bridge behavior and penalised. That is about promotional links, not about a
sources block, and this routine's first comment carries citations rather than a
call to click. No change to the contract; noted so a future run does not
introduce a link-in-comment CTA.
