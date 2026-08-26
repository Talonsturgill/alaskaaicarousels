# STORYBOARD — Carousel No. 41 — 2026-08-26
# FIVE SURFACES

## THE DIRECTORS ROOM, AND THE SYNTHESIS

Three lenses pitched in parallel and blind to each other. Cartographer,
editorial-essayist, field-documentarian. The trio differs from No. 40's
(data-journalist, systems-illustrator, historian-of-the-future).

All three independently found the same spine, which is worth recording because
it is the strongest signal the room produced: **the five surfaces stack in the
vertical.** Smoke and fire weather in the air, the refuse pile a few metres up,
the moving ground at grade, the water descending from the waterline, the
concealed rock hundreds of metres down. Nobody was told to see it that way.

Where they split is the horizontal axis, and that split decided the run.

- **CARTOGRAPHER, THE FIVE-HORIZON SECTION.** One continuous geological section
  9,720 px wide, panned along a named 870 km transect from the Chukchi coast to
  Cook Inlet. Superb drawing, and its own self-critique names the disqualifying
  flaw. A section drawing is a strong truth claim by genre, NSF publishes no
  field sites for any of these awards, and a reader absorbs geometry rather than
  marginalia. Printing "line of section drawn by this page" nine times does not
  undo an invented 870 km transect that implies where five awards sit. Rejected
  on the fabrication risk, which outranks a good picture.
- **EDITORIAL-ESSAYIST, THE DATUM STACK.** Camera descends through altitude
  rather than across geography, which dissolves the cartographer's problem
  entirely because there is no invented line. Contributed the deck's cover and
  its argument sentence, both grafted below. Its own slide 07, a two-column
  ranking by dollars and by dollars-per-year, is a category error a hostile
  reader can puncture (a one-year I-Corps translation grant is not a scaled-down
  ten-year Engine) and its self-critique says so. Dropped.
- **FIELD-DOCUMENTARIAN, THE STANDING TRAVERSE. WINNER.** Nine full-bleed
  Alaska grounds at the eye height of the person taking the measurement, across
  one continuous late-August day, with two beats where the camera stands
  vertical onto paper. It wins on three things no other treatment produced.

**Why it won, specifically.**

1. **THE HORIZON LADDER.** The far horizon's y position is set by the award's
   end year. The longer a project runs, the further you can see across its
   ground. It is legible at 432 px, it makes the contact sheet read as one
   camera walking backward for ten years, and it is the only device any director
   produced that argues the deck's actual thesis at swipe speed.
2. **THE NEAR GROUND.** The bottom 16 to 20 percent of every frame is the
   ground within arm's reach of the person measuring, at 1:1 hand scale, and it
   is the deck's single tack-sharp focal plane carrying five physically
   different materials. That is a STRUCTURAL kill for the inert-lower-band
   defect the scorer has named in six-plus runs, rather than another promise to
   be careful. The lowest band cannot be skipped because it is where the finest
   texture octave lives.
3. **GOLD IS MEASURED, BLUE IS MODELLED.** One `#FFC72C` mark per slide,
   always meaning a person or instrument recorded this. One `#6EA5FF` element
   per surface slide, always meaning a model computed this. A colour law that is
   auditable on every secondary label and that carries the whole argument.

**GRAFTED FROM THE ESSAYIST, and both are improvements on the winner's own.**

- **THE COVER.** The winner's cover was a label ("Five Alaska surfaces. Six
  clocks. 18.6 million."). The essayist's is a claim, and it is the best thing
  the room produced. Two verified obligated figures, 210 to 1 apart, stacked so
  the eye measures the gap before it reads a word, in four-letter Anglo-Saxon
  nouns that survive recompression. Adopted whole.
- **THE ARGUMENT SENTENCE**, now slide 02's headline. "Five surfaces Alaskans
  already argue about." The essayist's insight is that every one of the five
  reads a surface this audience has personally been in an argument about. What
  the water is doing, what is in the waste pile, when it is safe to burn,
  whether the ground will move, what is under the rock.

**ORDERED UP FRONT, at the winner's own request.** Its self-critique predicted
slide 03 would carry the flattest hachure field in the deck (`widthRatio` about
1.6 against 3.1 on slide 06) because one award, one number and one year is
genuinely uniform data, and warned that "the texture is uniform because the data
is uniform" is a true sentence a scorer may read as an excuse. The fix it asked
for is granted before the build rather than discovered at round two. Slide 03's
MESO octave takes a SECOND real variable, the Beer-Lambert extinction the
abstract itself names (C07), so stroke density and channel value both fall off
with modelled depth. Predicted `widthRatio` rises to 2.6 and is declared below.

**REJECTED FROM THE WINNER.** The runtime solar computation. The nine sun
positions are tabulated as authored design constants instead. They set light
direction and nothing else, no slide prints a time, an azimuth or an elevation,
and the dossiers mark them as design parameters rather than published facts,
because a solar position is not in claims.json and this deck does not assert
what it has not verified.

**A DELIBERATE REFUSAL, and it is the reason the cartographer lost.** The
horizon ladder is a COMPOSITION device and is NOT declared as a measured axis.
No slide invites a reader to read a year off horizon height, no `data-scale` is
declared for it, and every end date is printed as type instead. Declaring it
would create a measured band across full-bleed terrain, which qa.py would then
require every mark inside to mean something, and it would assert a precision the
picture can't carry.

---

## DECK HEADER

**THESIS.** Five NSF projects put $18,647,929 in obligated dollars into teaching
machines to read five physical Alaska surfaces, every clock started this summer,
and the ranking of which surface Alaska will know best runs to 2036.

**PDF DOCUMENT TITLE** (13 chars): `Five Surfaces`

**ARC.** hook / payoff / point / breather / point / point / data / turn / close.

| # | Beat | Emotional temperature |
|---|---|---|
| 01 | The two price tags | cold, withheld |
| 02 | The five named, and the argument | opening out |
| 03 | The water, the cheapest surface | quiet, close, tender |
| 04 | The burning weather (BREATHER) | wide, bright, released |
| 05 | The moving ground | brightest, most exposed |
| 06 | The rock, from both ends | warm, deep, the deck's hero |
| 07 | The ledger | flat, cool, factual |
| 08 | The turn, fifteen headlines | failing light, the argument lands |
| 09 | Close | dusk, resolved, one question |

**SLIDE COUNT RATIONALE.** Nine. Five surfaces need five frames and each one is
a different material; compressing two into one frame was the essayist's own
identified weak point and the winner's arc avoids it by giving the two mineral
projects a single frame that is ABOUT their pairing (near ridge and far range in
one composition) rather than a frame that merely contains both. Cover, the
named-set payoff, the ledger, the turn and the close are the other four. Eight
would cost the turn, which is where the deck's position actually lands. Ten
would split the rock frame and destroy its one-composition argument.

**CONTINUITY SYSTEM.** Four devices, none of them a forbidden one. No member of
a counted set changing state on nine slides, no dash legend binding after slide
04, no empty seat, no rail whose unit changes, no edge tease.

- **A. THE HORIZON LADDER.** `horizonY = 560 - 20 * (endYear - 2027)`.
  Revised during the art build, and the reason is worth keeping. The first
  ladder put 2027 at y972, which left seventy percent of the frame as inert
  sky on every surface slide and put the ground, where all the drawn texture
  and every data-driven field live, into the bottom quarter. The rungs are
  2027 y560, 2030 y500, 2032 y460, 2036 y380: the ladder still climbs with
  the end year and is still legible AS a ladder on slide 06, but the ground
  now dominates every frame that has one.
- **B. THE TRAVELLING KEY.** One late-August day. Authored sun positions sweep
  azimuth 32 to 306 degrees and elevation -4.5 to +34.5 and back to -6, so no
  two slides share a shadow direction.
- **C. THE NEAR GROUND.** Bottom 16 to 20 percent, 1:1 hand scale, the deck's
  one tack-sharp focal plane, a different material per surface.
- **D. GOLD IS MEASURED, BLUE IS MODELLED.**

### MOTIF STATE TABLE

| # | Sun (el / az) | Horizon y | Near-ground material | GOLD (measured) | BLUE (modelled) |
|---|---|---|---|---|---|
| 01 | -4.5 / 32 | 972 | duff and lichen | Sept 1st clock tick | none yet |
| 02 | 3 / 55 | plan view | glacial till from above | two campus pins | five register names |
| 03 | 12 / 85 | 972 | river cobble | sounding numeral | computed isobath |
| 04 | 26 / 128 | 765 | moss, duff, charcoal | anemometer tick | modelled burn window |
| 05 | 34 / 180 | 627 | schist scree | seismic station triangle | surrogate displacement field |
| 06 | 26 / 231 | 765 near, 351 far | coal refuse and ash | assay dot on the pile | phantom concealed body |
| 07 | 18 / 253 | plan view | till and lichen crust | the obligated total rule | none, the estimate is neutral grey |
| 08 | 8 / 280 | 351 | duff and lichen | September 1st tick | the August 11th headline tick |
| 09 | -6 / 306 | 351 | duff and lichen, slide 01's field | Polaris | none |

**VARIETY LEDGER CHECK.**

| axis | last decks | this deck | divergence |
|---|---|---|---|
| hero structure | 37 the re-inked press plate, 38 the locked lens over swapped floors, 39 the vacant cradle on a bench, 40 the 750 apron | **NEW: THE STANDING TRAVERSE** | All four hold ONE MANUFACTURED ARTIFACT still and change what surrounds it. This holds nothing still and contains no artifact. The subject is terrain at a scale no bench contains, the camera moves in three axes, and what recurs is a horizon rule and a moving key, not a prop. |
| atmosphere | 38 wet hemispheric overcast, 39 hard near-point lamp with sediment fog, 40 distant parallel key az 214 with IR fill | **NEW: THE LOW ALL-DAY SUN** | Direct sun on seven of nine slides, key at infinity, clear dry air, and the key TRAVELS 274 degrees of azimuth. None of the three forbidden atmospheres moves its light at all. |
| continuity | 39 the empty seat and the unit-changing rail, 40 cell 0016 and the phantom law | horizon ladder, travelling key, near ground, colour law | No counted set, no legend, no seat, no rail, no edge tease. |
| hook archetype | 38 purchase against its instrument, 39 the measured absence, 40 the order of operations | **NEW: THE TWO PRICE TAGS** | Two verified figures for two surfaces, 210 to 1 apart, and the gap is the question. |
| palette family | 38 cold maritime industrial, 39 rock flour and arc light, 40 night apron IR and sodium | **NEW: LOW SUN, YELLOW BIRCH** | A large desaturated warm birch mass, boreal greens, and a mid-value daylight register in the middle of the deck. None of the three carries a warm mass or leaves the dark register at all. |
| type pairing | 39 Bricolage with walking width plus Manrope plus Mono, 40 Archivo with Mono width-by-role | Fraunces cold cut plus Space Grotesk plus JetBrains Mono | Different families and a different mechanic. The axis in play is optical size and softness, not a walking width. |

**VARIANCE DIALS.** DESIGN_VARIANCE 4, VISUAL_DENSITY 4, TYPE_TEMPERATURE 2.

**PALETTE, `LOW SUN, YELLOW BIRCH`.**

| Hex | Role |
|---|---|
| `#050B14` | twilight base, deepest ground value (01, 09) |
| `#0F2033` | cold shadow, relief `low` on twilight slides |
| `#12222E` | wet shadow, river and slope shadow |
| `#1E3A46` | tea water, deepest channel (03) |
| `#3E6E63` | muskeg spruce mid |
| `#7E8C4E` | willow, second mid |
| `#C8A24A` | yellow birch, largest warm mass, desaturated |
| `#E4D7B8` | silt light, relief `high` on daylight slides |
| `#B4552F` | tundra rust, oxidised iron, small areas only (06) |
| `#2A2622` | coal refuse black-brown (06) |
| `#F4F8FF` | snow, all primary type |
| `#6EA5FF` | forget-me-not, MODELLED ONLY |
| `#FFC72C` | flag gold, MEASURED ONLY |

**GOLD BUDGET.** One mark per slide, minimum long dimension 14 px so it survives
432 px. Approximate areas: 01 380 px², 02 220, 03 340, 04 180, 05 260, 06 300,
07 1,900 (the one deliberate spend, the total rule), 08 240, 09 900. Under 0.4
percent of frame everywhere except 07.

**TYPE SYSTEM.** Display **Fraunces** in its cold cut, `opsz 144, wght 300,
SOFT 0, WONK 0`, tracking -2%, leading 0.98, every display block fitted with
`AK.fitText(el, {min, max, maxLines})` inside renderReady after
`await document.fonts.ready`. Support **Space Grotesk** 400 at 34px leading
1.38, labels 500 at 26px, measure 34 to 40 characters. Instrument **JetBrains
Mono** 400 at 22 to 26px, +12% tracking, `tabular-nums lining-nums` on every
figure, carrying the `NN / 09` counter, coordinates footer (`data-decorative`),
the ledger table, all guards and the provenance stamp.

**THE THREE-OCTAVE DETAIL BUDGET (deck rule).** Every slide declares MACRO,
MESO and MICRO with generator, parameters, seed and what it encodes. An octave
that encodes nothing is cut before build.

- **MACRO, the form, 90 to 400 px features.** `AK.reliefShade` laid down FIRST
  as substrate (it writes ImageData and REPLACES its region). `low` and `high`
  always named from the slide's own palette pair. `strength = 0.9 + 1.5 *
  (log10(D) - 4.699) / 2.322` where D is that award's obligated dollars.
  `noiseScale = 0.0028 * (48 / months)`, clamped to 0.009. **Relief amplitude is
  the money and relief wavelength is the clock.**
- **MESO, the shading marks, 6 to 16 px.** `AK.hachureField` with `height`
  always from a story quantity, never noise. `maxWidth = 1.6 + 2.2 * frac`.
  Every slide declares named `probes` and a predicted `widthRatio` BEFORE the
  build, so a pixel critic can be asked to contradict a number from the render.
- **MICRO, the near ground, 0.8 to 3 px, bottom 16 to 20 percent only.**
  Per-site material at 1:1 hand scale with density falling from the near edge.

**COMPUTED OCTAVE CONSTANTS, verified arithmetic:**

| surface | D obligated | months | strength | noiseScale | maxWidth |
|---|---|---|---|---|---|
| water | 50,000 | 12 | 0.90 | 0.0090 (clamped) | 1.60 |
| burning weather | 1,588,147 | 48 | 1.87 | 0.00280 | 3.02 |
| moving ground | 1,772,170 | 72 | 1.90 | 0.00187 | 3.07 |
| waste | 4,737,612 | 48 | 2.18 | 0.00280 | 3.47 |
| concealed rock | 10,500,000 | 120 | 2.40 | 0.00112 | 3.80 |
| deck (01, 09) | 18,647,929 | n/a | 2.60 | 0.00260 | 3.95 |

**CLAIMS INDEX.**

| claim | slides |
|---|---|
| C01 | 03 |
| C02 | 01, 03, 07 |
| C04 | 03, 07 |
| C05 | 03 |
| C06 | 02, 03 |
| C07 | 03 |
| C09 | 02, 06, 07 |
| C10 | 02, 06, 07 |
| C11 | 01, 02, 06 |
| C12 | 06 |
| C13 | 06 |
| C16 | 06, 07 |
| C19 | 02, 06 |
| C20 | 05 |
| C21 | 05, 07 |
| C22 | 05, 07 |
| C23 | 05 |
| C24 | 05 |
| C25 | 05 |
| C26 | 02, 05 |
| C27 | 06 |
| C28 | 06, 07 |
| C29 | 01, 06, 07 |
| C30 | 06, 07, 09 |
| C31 | 06, 07 |
| C33 | 02, 06 |
| C36 | 06 |
| C37 | 01, 02, 07 |
| C38 | 01, 07, 08, 09 |
| C39 | 07, 09 |
| C43 | 02, 04 |
| C44 | 04 |
| C45 | 04, 07 |
| C46 | 08 |
| C47 | 08 |
| NOT USED | C03, C08, C14, C15, C17, C18, C32, C34, C35, C40, C41, C42, C48 |

**C48 IS USED NOWHERE.** The unverified fire-season-end date appears on no
slide, in no footnote and in no caption line. Slide 04 argues from C43, C44 and
C45 alone.

**THERE IS NO EXCLUDED-AWARD BEAT ANYWHERE IN THIS DECK.** No slide, caption or
comment states that an award was examined and cut. None was.

---

<!-- This section sits ABOVE the first dossier deliberately. dossier_check
     runs the last slide's section to end of file, so a deck-level section
     placed after SLIDE 09 is parsed as part of SLIDE 09's dossier, and this
     one's description of the contact-shadow fixes made slide 09 fail a
     promise it never made. Logged for Phase 12. -->

## BUILD RECONCILIATION

Every dossier number the build actually changed. The GATE STATUS block below is
written by `scripts/gate_status.py --sync` and is never hand-written; this
section is the human half, and it is what the pixel critics must measure the
renders against. Read it before the dossiers: where the two disagree, this
section is what shipped.

**A. THE HORIZON LADDER MOVED, AND EVERY DOSSIER'S HORIZON NUMBER WITH IT.**
Planned `horizonY = 972 - 69 * (endYear - 2027)`; shipped
`horizonY = 560 - 20 * (endYear - 2027)`. Rungs are now 2027 y560, 2030 y500,
2032 y460, 2036 y380. The first ladder left roughly seventy percent of every
surface frame as inert sky and pushed the ground, which carries all the drawn
texture and every data-driven field, into the bottom quarter. The ladder still
climbs with the end year and is still legible AS a ladder on slide 06. Do not
measure any horizon against the old numbers; the dossiers were re-synced.

**B. SLIDE 06'S NEAR RIDGE RAMP.** Planned `low #2A2622 high #C8A24A`; shipped
`low #141110 high #6E6153`, ambient 0.30 to 0.26, diffuse 0.66 to 0.62. Across
an 850px full-bleed region the planned high stop rendered the lower two thirds
as a gold field, which broke the 60/30/10 budget and swallowed the single gold
element the slide is allowed. Warmth is carried by the late key instead.

**C. A TYPE RESERVE WAS ADDED TO SIX SLIDES (01, 02, 03, 05, 06, 09).** Not in
any dossier. Machine QA measured white type at 1.7:1 to 2.8:1 against the pale
end of the gradients it sits on, and flagged three more labels as crossed by
art. Each of those slides now carries a soft elliptical scrim behind its
display column, drawn as the last art operation before the post grade. It has
no edge and leaves the art continuous behind the words.

**C2. THE RESERVE WAS REBUILT TWICE, AND THE FIRST REBUILD DID NOT HOLD.** The
first version filled an ELLIPSE (rx r, ry under r) with a CIRCULAR gradient of
radius r, so the falloff was cut off vertically and every one of the six slides
carried a visible conic arc across its ground; four pixel critics reported that
arc as the most conspicuous thing in the frame. It is now drawn as a scaled
circle inside a transform, the way the lit pools already were, and keyed to
each slide's own sky hue rather than a neutral grey. Even then slides 03, 05
and 06 still measured 4.3, 3.7 and 3.0 at worst point, so their reserves were
deepened again in the final round. Machine QA now reports ZERO contrast
failures across all nine slides. Do not read the first "all six now pass" as
the end of this story; it was written a round too early and the scorer caught
it.

**C3. LOAD-BEARING LABELS CAME UP TO THE 24px MOBILE FLOOR.** FAIRBANKS and
ANCHORAGE, slide 03's instrument block and its WATERLINE and BED ticks, slides
04 and 05's attribution plates, and slide 06's split, guard and note lines were
all set at 18 to 22px, which is 7 to 9px on a 432px feed thumb. Every one of
them names a fact. Tiny-text warnings fell from 37 to 27; the remainder are
counters, coordinates and axis labels, which are decorative or tabular.

**D. CONTACT DECLARATIONS WERE RE-MEASURED OFF THE RENDERS, NOT THE CAMERA
MATHS.** Slides 01, 02, 03, 04 and 06 all declared the ground rect directly
BELOW the shadow rect, which put it at the lit pool's dark edge while the
shadow sat near the pool's bright centre; three of the five measured NEGATIVE
separation. Every pair is now side by side at the same y, both inside the pool,
with positions read off the rendered PNG. Slide 03's pair was 118px from where
the marker actually drew. Pools were widened and casts deepened and offset on
01, 03, 04, 05 and 06.

**E. SLIDE 08'S RAIL IS BUILT FROM REFETCHED DATA AND ITS MARKS ARE SQUARES.**
The dossier called for fifteen 3x18px ticks. claims.json fixes only the window
and the August 11th date, so fifteen ticks at invented positions would have
asserted fifteen unverified dates on a measured axis. The UAF index was
refetched during the art build: three headlines on August 21st, one on the
20th, one on the 19th, two on the 13th, three on the 12th, two on the 11th,
two on the 10th, one on the 9th, which confirms C46's count and C47's verbatim
exactly. Same-day headlines therefore STACK VERTICALLY as 9px squares, one
square per headline, because the axis is x and a horizontal nudge would be a
date the source does not support. The declared band is `[994, 1005]`, the
one row every stack crosses, and the contact shadow the dossier promises is
declared on the gold September 1st tick.

**F. SLIDE 07'S TABLE.** Set at 24px rather than the planned 26px and the
SURFACE column dropped its "THE " article, because at 26px with the article the
column ran into OBLIGATED on three of six rows. 24px is at the mobile floor,
not under it. The height field is log scaled and the method note on the page
says so, because a linear surface renders every award except the Engine as flat
zero across a 50,000 to 10,500,000 range.

**G. SLIDE 02'S REGISTER CAME UP TO THE FLOOR.** Sub-lines were set at 19px and
the row numbers at 20px, which is about 8px on a 432px feed thumb. Every line
there names a surface and is load-bearing, so the block is now 22/26/24px and
the row height grew from 64px to 88px to hold it.

**H. BODY COPY WAS SHORTENED ON 05, 06, 08 AND 09** to clear the horizon or a
ridge line, and slides 06 and 08 moved their supporting copy onto plates. The
storyboard's slide 05 copy block was re-synced to what ships.

**I. PLANNED AND NOT SHIPPED.** Slide 05's dossier described en-echelon crown
cracks; a discrete row of arcs at a regular pitch read as border ornament, so
the second structural line is a single wandering bench that fades along its
length. Slide 06's `data-encodes` uses the engine's `a`/`b` rect grammar rather
than the `regions` shape the dossier sketched.

## SLIDE 01 — COVER, THE TWO PRICE TAGS

**1. BEAT.** The hook. Plants the deck's only open loop worth planting on a
cover, which is that five surfaces are announced and only two are priced.
Inherits nothing. Plants everything.

**2. COPY, FINAL.**
- Kicker, mono, 24px, +12% tracking: `OBLIGATED, SIX NSF AWARDS` (25 chars)
- Display line 1, Fraunces 138px: `$50,000 to read the water.` (26 chars) [C02]
- Display line 2, Fraunces 138px: `$10,500,000 to read the rock.` (29 chars) [C29]
- Footer, mono, 24px: `FIVE PROJECTS. SIX AWARDS. FIVE ALASKA SURFACES.` (47 chars)
- Gold field label, mono 22px, on the near ground: `SEPTEMBER 1ST` (13 chars) [C38]
- Counter, mono: `01 / 09`
- Coordinates footer, mono 20px, `data-decorative`: `64°51'N 147°43'W`
- Wordmark: `ALASKA.AI`

Eleven display words, inside the twelve-word ceiling. The hedge that C37 and
C28 require lives in the kicker, where it is load-bearing and typographically
small, so the display stays huge.

**3. READER TAKEAWAY.** Two numbers 210 to 1 apart buy two readings of Alaska,
and there are three more surfaces nobody has named yet.

**4. LAYOUT MAP.** 12 x 8 grid. Kicker at col 1 to 5, row 1. Display block cols
1 to 9, rows 2 to 4, optical-left overhang 6px on the `$`. Horizon rule at
y560, which is row 3.3. Gold tick and its label at cols 7 to 9, row 7. Footer
cols 1 to 8, row 8. Focal point is the second dollar figure at (0.33, 0.30).
Eye path: figure one, figure two, the gold spark on the ground. Quiet zone is
cols 10 to 12 rows 2 to 4, bounded at about 18 percent of frame, upper right,
deliberately NOT the bottom band. One permitted grid violation is the display
block's optical overhang past the 80px margin.

**4a. Lower-third treatment.** The bottom band is the deck's premise made
physical and it is the densest region in the frame. It carries the near ground
at 1:1 hand scale, duff and lichen over frozen-hard mineral soil, drawn as a fur
field of 5 to 9 step ticks from Poisson starts at one tick per 42 px² in
`#1B2A22` over a `#0E1A18` graded base, with the relief substrate's own modelled
tone underneath it and a two-part contact shadow beneath the gold clock tick
falling onto ground that has already been lit. Texture density falls with
distance from the bottom edge per the depth-of-field rule, so the band is a real
focal plane rather than a strip of noise, and the hachure field's stroke widths
carry the funding-by-year surface right down into the last 40 px of the frame.
Nothing here is a plate, a hairline or a caption sitting on bare ground.

**5. DEPTH PLAN.** Background sky ramp (five-stop OKLCH keyed to solar elevation
-4.5, IGN dithered) → relief substrate → hachure field → mid-ground silhouette
line → near ground micro → gold tick and its cast shadow → DOM type → grain
tile. Depth cues, five: atmospheric perspective in the sky's own hue, occlusion
of the mid-ground line by the near ground, scale gradient in the fur ticks,
depth of field with the near band tack sharp and the horizon soft, and a
two-part shadow under the one object. Focal plane is the near ground.

**6. CONTINUITY DEVICE STATE.** Horizon at y560, the ladder's lowest rung,
which is the 2027 end date. Sun el -4.5 az 32, civil twilight, no direct beam.
Near ground is duff and lichen. Gold present as the September 1st tick. Blue
absent, because nothing has been modelled yet. Nothing bleeds off the right edge
because this deck has no edge tease.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:0, w:1080, h:1350, scale:2, seed:20260826,
  noiseScale:0.0026, octaves:5, warp:0.55, strength:2.60, low:'#050B14',
  high:'#22384C', ambient:0.34, diffuse:0.30, lights:[{az:32, el:6, w:0.35}]})`.
  Computed at 1x into an offscreen canvas and drawImage-upscaled, per the
  feasibility note. **Encodes C37**, the whole obligated set at deck amplitude.
- MESO: `AK.hachureField(cx, {x:0, y:972, w:1080, h:378, scale:2,
  seed:20260826, cell:13, passes:4, lenScale:1.9, sunAz:32, sunEl:6,
  sunJitter:11, color:'#0A1622', alpha:0.13, minWidth:0.45, maxWidth:3.95,
  height: fundingByYear, probes:[{name:'early, FY2027 to FY2029', x:80,
  y:1010, w:300, h:200}, {name:'late, FY2033 to FY2036', x:700, y:1010,
  w:300, h:200}]})` where `fundingByYear` is a 6 x 11 grid, six awards by
  eleven fiscal years 2026 to 2036, each cell that award's obligated dollars if
  the year falls inside its performance period and 0 otherwise, precomputed to a
  4px lookup grid and handed in as a bilinear sampler. **Encodes C02, C09, C10,
  C21, C29, C45, C04, C16, C22, C30, C39.**
  **DECLARED PREDICTION, falsifiable from the render alone: `widthRatio >= 3.0`,
  and probe `early` meanWidth / probe `late` meanWidth in the range 1.6 to 2.2,
  because five awards overlap in the early years and one runs alone to 2036.**
- MICRO: fur field #10, ticks 5 to 9 steps, Poisson starts, one per 42 px²,
  `#1B2A22`, y1150 to y1350, density falling with distance from the bottom edge.
  Plus `AK.grainTile(280, 50, 20260826)` at alpha 0.07 over the whole art
  canvas, then `AKPOST.grade` with IGN dither on.

**8. DATA-IN-ART MAPPING.** Relief strength 2.60 is the log-scaled deck total
(C37). Hachure height is the six-award by eleven-year obligation surface, so
the ground's steepness at any horizontal position is how much federal money is
live in that fiscal year. Horizon at y560 is the earliest end year, 2027.

**9. PALETTE ASSIGNMENT.** bg base `#050B14`; relief ramp `#050B14` to
`#22384C`; sky ramp `#0F2033` to `#2A4058`; hachure ink `#0A1622`; near ground
`#1B2A22` on `#0E1A18`; type primary `#F4F8FF`; type secondary
`rgba(244,248,255,0.72)`; accent `#FFC72C` on the tick only. Worst-case contrast
pair is display `#F4F8FF` on `#22384C` at about 11.9 to 1, and the mono footer
`rgba(244,248,255,0.72)` on `#0E1A18` at about 9.4 to 1. Both clear 4.5 to 1
with margin.

**10. TYPE SPEC.**
- Kicker: JetBrains Mono, 24px, 400, leading 1.2, tracking +12%, uppercase,
  `rgba(244,248,255,0.66)`, left, max width 520px, fixed.
- Display: Fraunces, 138px, `opsz 144 wght 300 SOFT 0 WONK 0`, leading 0.98,
  tracking -2%, sentence case, `#F4F8FF`, left, max width 880px, fitted with
  `AK.fitText(el, {min:104, max:138, maxLines:2})` per line block.
- Footer: JetBrains Mono, 24px, 400, tracking +12%, uppercase,
  `rgba(244,248,255,0.72)`, left, max width 760px, fixed.
- Gold label: JetBrains Mono, 22px, 600, tracking +12%, uppercase, `#FFC72C`,
  on a measured knockout plate, `AK.svgPlate` sized from the laid-out text.
- Counter and coordinates: JetBrains Mono, 20px, 400, `data-decorative`.

**11. ICONOGRAPHY / ANCHOR SPEC.** The literal anchor is the horizon rule itself
plus the single gold clock tick standing on the near ground, a 4px x 26px
vertical mark with a 6px perpendicular terminal, at (742, 946), with its
two-part contact shadow declared. Annotation furniture is one leader from the
tick to its label, authored as a world-coordinate polyline ending ON (742, 946)
and declared in `window.__akLeaders` with `from`, `label` and `at`.

**12. REFERENCE INTENT.** A field notebook's first page at 05:12, before
anything has been measured. NASA mission-poster restraint, arctic edition, with
the numbers doing the shouting and the ground doing the work.

**13. RISK FLAGS.** (a) Two 138px dollar figures may not fit two lines at
`min:104`; mitigated by `AK.fitText` with `maxLines:2` per block and a measured
880px box, and the fit record is checked in `render_report.json`. (b) A twilight
frame risks 8-bit banding across a large soft sky; mitigated by IGN dither,
always on. (c) Gold at 22px on a dark ground could fall under the 14px minimum
long dimension at thumb scale; the tick is 26px tall, which clears it.

**14. ACCEPTANCE CHECKLIST.**
- [ ] Both dollar figures render on exactly two lines, no third line, no overlap
      with the footer.
- [ ] The bottom 200 px contains visible fur-tick texture at 100 percent zoom,
      not a flat fill.
- [ ] The gold tick is the ONLY `#FFC72C` in the frame.
- [ ] No forget-me-not `#6EA5FF` appears anywhere on this slide.
- [ ] The horizon sits at y560 plus or minus 4 px.
- [ ] `widthRatio` reported by the hachure call is at least 3.0.
- [ ] The contact shadow under the gold tick measures at least 4.0 L* against
      the lit ground beside it.
- [ ] At 432 px the two figures are both legible and the gold spark is visible.

---

## SLIDE 02 — THE FIVE SURFACES

**1. BEAT.** Pays the cover off in one frame by naming all five surfaces and the
total. Inherits the cover's withheld three. Plants the loop that the five are
not five topics but five arguments Alaskans are already having.

**2. COPY, FINAL.**
- Kicker, mono 24px: `NSF, SIX AWARDS, FIVE PROJECTS` (30 chars)
- Headline, Fraunces 76px, two lines broken at sense:
  `Five surfaces Alaskans` / `already argue about.` (42 chars)
- Body, Space Grotesk 34px (44 words):
  `NSF funded five projects across six awards to University of Alaska campuses.
  Each one teaches a model to read one physical surface. The water. The waste.
  The burning weather. The moving ground. The concealed rock. Obligated dollars
  total 18,647,929.` [C06, C19, C43, C26, C33, C37]
- Guard, mono 22px: `SURFACES DRAWN AS TYPES. NSF'S RECORDS NAME NO FIELD SITES.`
- Five register labels, mono 24px, set in place on the map.
- Two campus pins, mono 22px: `FAIRBANKS`, `ANCHORAGE`
- Counter `02 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** Five machines, five surfaces, one state, 18.6 million
obligated dollars.

**4. LAYOUT MAP.** Camera stands vertical. Alaska at the canonical conic
(`d3.geoConicEqualArea().parallels([55,65]).rotate([154,0])`) via
`AKGeo.alaskaProjection(ak, [[96,470],[984,1130]])`, fitted to the FULL state,
never `fitExtent` to a small bbox. Kicker row 1, headline cols 1 to 8 rows 2 to
3, body cols 1 to 6 row 4, map rows 4 to 7 bleeding left and right, guard row 8.
Focal point at the map's interior mass (0.5, 0.62). Eye path headline, body,
map, register names. Quiet zone cols 9 to 12 rows 2 to 3, about 16 percent.

**4a. Lower-third treatment.** The lower band is the map's own southern interior
and it is fully modelled, not a margin. It carries the multidirectional relief
substrate at full amplitude across Bristol Bay, the Alaska Peninsula and the
Gulf coast, with the five material registers interlocking down into it and the
hachure field's stroke widths continuing to the bottom bleed. A graded haze ramp
in the sky's own hue sits over the deepest 90 px so the landmass recedes rather
than stops, the two campus pins throw two-part contact shadows onto lit ground,
and the near-ground micro octave lays glacial till seen from above at 1:1 across
the bottom 200 px. No region of the lower third is a flat fill, a plate or a
bare caption band.

**5. DEPTH PLAN.** Sky ramp → ocean field → relief substrate (multidirectional)
→ five material registers → hachure → coastline stroke → pins and shadows → DOM
type → grain. Four cues: occlusion (registers over relief), atmosphere (haze
ramp at the south), scale gradient (till texture), and shadow (pin contacts).
Focal plane is the map's mid-latitude band.

**6. CONTINUITY DEVICE STATE.** Plan view, so the horizon ladder is suspended
and its absence is the signal that this is a paper beat. Sun el 3 az 55, low and
early. Near ground is glacial till from above. Gold is the two campus pins. Blue
is the five register names, because a register is a modelled classification.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:380, w:1080, h:820, scale:2,
  seed:20260827, multidirectional:true, noiseScale:0.0032, octaves:5,
  warp:0.60, strength:2.10, low:'#0F2033', high:'#7E8C4E', ambient:0.36,
  diffuse:0.60})`, clipped to the projected landmass. Multidirectional here
  because a plan view has no single sun direction that reads honestly.
  **Encodes** the physical shape of the state the five surfaces sit in.
- MESO: `AK.hachureField` over the landmass, `height` = the five-register
  membership field, `cell:14, passes:3, lenScale:1.9, sunAz:55, sunEl:12,
  color:'#12222E', alpha:0.10, minWidth:0.45, maxWidth:2.9`,
  `probes:[{name:'interior', ...},{name:'coastal margin', ...}]`.
  **Encodes C06, C19, C43, C26, C33** as five interlocking material zones.
  **DECLARED PREDICTION: `widthRatio >= 2.8`.**
- MICRO: glacial till from above, crosshatch material code #65 at 0.9 to 1.5 px,
  density falling toward frame edges, plus grain tile 280/48 at 0.06.

**8. DATA-IN-ART MAPPING.** Five material registers are the five surfaces
(C06, C19, C43, C26, C33). Two campus pins sit at the true projected coordinates
of Fairbanks and Anchorage, which are the two awardee cities on the six records.
The total 18,647,929 is set as type, never encoded in form shading.

**9. PALETTE ASSIGNMENT.** bg `#050B14`; ocean `#0F2033`; relief ramp `#0F2033`
to `#7E8C4E`; register inks `#3E6E63`, `#7E8C4E`, `#C8A24A`, `#12222E`,
`#B4552F` at 0.30 alpha each; coastline `#E4D7B8` hairline; type `#F4F8FF`;
register names `#6EA5FF`; pins `#FFC72C`. Worst case is body `#F4F8FF` on
`#0F2033` at about 13.6 to 1.

**10. TYPE SPEC.** Headline Fraunces 76px `opsz 144 wght 300 SOFT 0 WONK 0`,
leading 1.00, tracking -1%, `#F4F8FF`, max width 760px, `AK.fitText({min:60,
max:76, maxLines:2})`. Body Space Grotesk 34px 400, leading 1.38, max width
560px, measure about 38 characters. Register names JetBrains Mono 24px 500,
+10%, `#6EA5FF`, each on a measured `AK.svgPlate` knockout. Pin labels
JetBrains Mono 22px 600 `#FFC72C` on measured plates. Guard JetBrains Mono 22px
400 `rgba(244,248,255,0.62)`.

**11. ICONOGRAPHY / ANCHOR SPEC.** The literal anchor is Alaska itself, from
`assets/geo/alaska-state.geo.json` at the canonical projection, stroke `#E4D7B8`
at `--w-fine` 1.25px with a 12 percent interior fill. Annotation furniture is
five register names on knockout plates, two pins with contact shadows, one
scale bar in the lower right at `--w-hair`, and a graticule at 10 percent.

**12. REFERENCE INTENT.** A geologic quadrangle index sheet, where the state is
divided by what is being surveyed rather than by who owns it.

**13. RISK FLAGS.** (a) Five registers at 0.30 alpha over relief could read as
mud; mitigated by holding each register to a distinct hue family and letting the
relief carry value while the registers carry hue only. (b) `fitExtent` to a
small bbox renders a giant fill disc; mitigated by fitting the FULL state per
`AKGeo`. (c) Register names could collide with the coastline; every one sits on
a measured knockout plate.

**14. ACCEPTANCE CHECKLIST.**
- [ ] All five register names are legible at 432 px.
- [ ] The coastline reads as Alaska, with the Panhandle and the Aleutian chain
      both present and recognisable.
- [ ] Both campus pins sit on land, not water, at their true projected points.
- [ ] The guard line about field sites is present and legible.
- [ ] Body copy states 18,647,929 with the word obligated somewhere in the
      frame.
- [ ] Gold appears ONLY on the two pins.
- [ ] The bottom 200 px carries till texture and haze, not a flat fill.

---

## SLIDE 03 — THE WATER

**1. BEAT.** The first surface, and the cheapest. Inherits the cover's water
price tag and pays it with the mechanism. Plants the loop that if daylight depth
costs fifty thousand dollars, the expensive surfaces must be the ones you can't
photograph.

**2. COPY, FINAL.**
- Kicker, mono 24px: `AWARD 2630206, I-CORPS` (22 chars) [C01]
- Headline, Fraunces 72px, two lines: `The water,` / `read from orbit.` (27)
- Body, Space Grotesk 34px (41 words):
  `Award 2630206 develops explainable AI that turns satellite imagery into high
  resolution maps of underwater depth for coastlines, rivers and lakes. NSF
  obligated 50,000 dollars. The clock runs September 1st, 2026 to August 31st,
  2027.` [C06, C02, C04]
- Label, mono 22px, gold, on the bed: `SOUNDING` (8 chars)
- Label, mono 22px, blue: `MODELLED ISOBATH` (16 chars)
- Attribution, mono 22px: `ERIN TROCHIM, UNIVERSITY OF ALASKA FAIRBANKS` [C05]
- Method note, mono 22px: `PHYSICS INFORMED NEURAL NETWORKS` [C07]
- Counter `03 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** Fifty thousand dollars and one year buys a model that
reads river and coastal depth off satellite pictures.

**4. LAYOUT MAP.** Eye height on a braided river bar. Horizon at y560, the
ladder's lowest rung. Kicker row 1, headline cols 1 to 7 rows 2 to 3, body cols
1 to 6 row 4. The wetted channel runs from cols 3 to 12 across rows 5 to 7. Gold
sounding numeral at (628, 1042); blue isobath curve running from (300, 1088)
through (628, 1050) to (980, 1006), agreeing with the sounding at one point and
drifting away from it either side. Focal point at the sounding (0.58, 0.77).
Quiet zone cols 8 to 12 rows 2 to 3, about 17 percent. Attribution and method
note bottom left, rows 7 to 8.

**4a. Lower-third treatment.** The bottom band is the river bar itself at 1:1
hand scale and it is the sharpest, most worked region of the frame. River cobble
is drawn as a Poisson-disk stipple with minimum distance proportional to
1/sqrt(density), radii 1.1 to 1.6 px, each clast carrying a wet-side highlight
on its sun-facing quarter and a small cast shadow onto the graded bar surface
beneath, over the relief substrate's own modelled tone. The wetted channel's
hachure field continues into this band with stroke widths driven by the bed
slope, so the texture is data-driven right to the bottom bleed, and a two-part
contact shadow sits under the gold sounding marker on ground already lit by the
morning key. No plate, hairline or caption is doing the work here.

**5. DEPTH PLAN.** Sky ramp → far bank silhouette → relief substrate on bar and
channel → hachure on the wetted channel → water value layer → cobble micro →
gold sounding and shadow → blue isobath → DOM type → grain. Five cues:
atmospheric perspective on the far bank, occlusion of bank by bar, scale
gradient in cobble size, depth of field with the near cobble sharp and the far
bank soft, and the two-part contact shadow. Focal plane is the near bar.

**6. CONTINUITY DEVICE STATE.** Horizon y560 (2027, the earliest end date). Sun
el 12 az 85, morning, raking across the wetted channel. Near ground is river
cobble. Gold is the sounding numeral, a thing a person measured. Blue is the
computed isobath, a thing a model produced. The two agree at exactly one point,
which is the slide's wordless argument.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:900, w:1080, h:450, scale:2,
  seed:20260829, noiseScale:0.0090, octaves:5, warp:0.50, strength:0.90,
  low:'#12222E', high:'#E4D7B8', ambient:0.34, diffuse:0.66,
  lights:[{az:85, el:12, w:1.0}]})`. **Encodes C02** as amplitude (the smallest
  in the deck) and **C04** as wavelength (the shortest clock, so the tightest,
  busiest bar). The cheapest award produces the deck's finest-grained ground,
  and that is the honest visual consequence of the numbers.
- MESO: `AK.hachureField(cx, {x:120, y:960, w:900, h:300, scale:2,
  seed:20260829, cell:12, passes:4, lenScale:1.9, sunAz:85, sunEl:12,
  sunJitter:11, color:'#0B1A22', alpha:0.12, minWidth:0.45, maxWidth:1.60,
  height: bedTimesExtinction, probes:[{name:'thalweg', x:560, y:1000, w:200,
  h:160},{name:'point bar', x:180, y:1000, w:200, h:160}]})`.
  **THE SECOND VARIABLE, ORDERED UP FRONT.** `bedTimesExtinction(u,v)` is the
  product of the bed cross-section profile and the Beer-Lambert per-channel
  extinction term that C07 says the model embeds, normalised 0 to 1. Bed slope
  alone would give a nearly uniform field, which the winning director predicted
  and flagged; the extinction term makes stroke density fall with modelled depth
  as well as with slope. **Encodes C06 and C07.**
  **DECLARED PREDICTION: `widthRatio >= 2.6`, and probe `thalweg` meanWidth /
  probe `point bar` meanWidth in the range 1.7 to 2.4.** This number is the
  whole reason the second variable was ordered, and a pixel critic is invited to
  contradict it from the render alone.
- MICRO: river cobble, Poisson-disk stipple #66, r 1.1 to 1.6, wet-side
  highlights on the sun-facing quarter, y1180 to y1350, plus grain tile 280/46
  at 0.07.

**8. DATA-IN-ART MAPPING.** Relief strength 0.90 is the log-scaled 50,000
obligated dollars (C02). Relief noiseScale 0.0090, the clamped maximum, is the
twelve-month clock (C04). Hachure height is bed profile times modelled
extinction (C07). The blue isobath touches the gold sounding at exactly one
point, which encodes what a calibrated model with an uncertainty estimate
actually gives you.

**9. PALETTE ASSIGNMENT.** bg `#050B14`; sky `#12222E` to `#3E5A66`; relief ramp
`#12222E` to `#E4D7B8`; channel `#1E3A46`; hachure `#0B1A22`; cobble `#C4B79A`
on `#8A8069`; type `#F4F8FF`; sounding `#FFC72C`; isobath `#6EA5FF`. Worst case
is body `#F4F8FF` on `#12222E` at about 14.1 to 1; the gold sounding numeral
sits on a measured knockout plate at `#071018`.

**10. TYPE SPEC.** Headline Fraunces 72px, `opsz 144 wght 300 SOFT 0 WONK 0`,
leading 1.00, tracking -1%, `#F4F8FF`, max width 700px, `AK.fitText({min:56,
max:72, maxLines:2})`. Body Space Grotesk 34px 400, leading 1.38, max width
560px. Kicker, labels, attribution and method note JetBrains Mono 22 to 24px,
+12%, uppercase, each on a measured `AK.svgPlate`.

**11. ICONOGRAPHY / ANCHOR SPEC.** The literal anchor is the gold sounding
marker on the river bed, a 5px filled dot with a mono depth numeral beside it,
at (628, 1042), with a two-part contact shadow declared. The blue isobath is a
segment-interpolated stroke (#81) at `--w-fine`. Annotation furniture is one
leader from the sounding to its `SOUNDING` label, a world-coordinate polyline
ending ON (628, 1042), declared in `window.__akLeaders` with `from`, `label`
and `at`; plus a scale bar and a coordinate readout at `--w-hair`.

**12. REFERENCE INTENT.** A hydrographic field sheet, morning light, where the
measured point and the modelled line are drawn in different inks and the reader
can see exactly where they part company.

**13. RISK FLAGS.** (a) The predicted flat field, addressed with the Beer-Lambert
second variable and a declared `widthRatio` floor of 2.6. (b) The blue isobath
crossing the gold sounding could read as a collision; the isobath is drawn UNDER
the sounding dot and the dot carries a 3px canvas-colour halo ring. (c) A single
key at el 12 could leave the far bank black; the fill is a hemispheric sky term
at weight 0.34, not zero.

**14. ACCEPTANCE CHECKLIST.**
- [ ] `widthRatio` from the hachure call is at least 2.6.
- [ ] The blue isobath visibly touches the gold sounding at one point and
      visibly diverges from it on both sides.
- [ ] Cobble texture is individually resolvable at 100 percent zoom in the
      bottom 170 px.
- [ ] The contact shadow under the sounding marker measures at least 4.0 L*.
- [ ] The horizon sits at y560.
- [ ] Exactly one gold element and exactly one blue element in the frame.
- [ ] The leader from the sounding arrives at the word SOUNDING within 32 px.
- [ ] 50,000 and both dates are present and correct.

---

## SLIDE 04 — THE BURNING WEATHER (DECLARED BREATHER)

**1. BEAT.** The rest beat, and the deck's widest frame. Inherits the water's
loop about surfaces you can't photograph and answers it with one you can only
photograph. Plants the loop that a machine is being paid to find a safe day.

`data-breather` is set on the body.

**2. COPY, FINAL.**
- Kicker, mono 24px: `AWARD 2536745, FIRE-WUI` (23 chars)
- Headline, Fraunces 72px, two lines: `The weather that` / `decides a burn.` (31)
- Body, Space Grotesk 34px (34 words):
  `Award 2536745 reads historical weather reanalysis with statistical and
  machine learning methods to find windows safe enough for controlled burning
  across Alaska. 1,588,147 obligated dollars. Four years.` [C43, C45]
- Note, mono 22px: `NSF FILES IT UNDER ARTIFICIAL INTELLIGENCE` [C44]
- Gold label, mono 22px: `STATION` (7 chars)
- Blue label, mono 22px: `MODELLED WINDOW` (15 chars)
- Counter `04 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** A model is being built to say when it is safe to light a
fire on purpose in Alaska.

**4. LAYOUT MAP.** Sky takes 62 percent, which is what makes this the breather.
Horizon at y500. Kicker row 1, headline cols 1 to 7 rows 2 to 3, body cols 1 to
6 rows 3 to 4, all in the sky zone where the ground is quietest. Black spruce
silhouette line along y740 to y790. Gold anemometer tick at (840, 742). Blue
modelled window bar at cols 2 to 6, y820. Focal point at the cloud base
(0.44, 0.36). Quiet zone is the upper right, cols 9 to 12 rows 1 to 2, about 20
percent, which is the ceiling.

**4a. Lower-third treatment.** Even as the declared breather this slide's lower
band is modelled ground rather than a rest. It carries the burn unit's own
surface, moss and duff over a graded relief substrate at strength 1.87, with a
fur field of stand-density ticks and Bayer 4x4 dithered charcoal patches from
previous fire, all lit by the 26 degree midday key and throwing a soft ambient
occlusion into the moss hollows. Charcoal density falls with distance from the
bottom edge so the band holds a real focal plane, the black spruce silhouette
line occludes the horizon behind it to buy depth, and a two-part contact shadow
sits beneath the gold anemometer tick on lit ground. The band is quieter than
slides 03 and 06 by design, and it is still tone and texture rather than a flat
fill or a caption strip.

**5. DEPTH PLAN.** Five-stop OKLCH sky ramp with IGN dither → fbm-displaced
cumulus band at coverage 0.48 → far ridge with atmospheric fade → black spruce
silhouette → relief substrate → hachure on stand density → moss and charcoal
micro → gold tick and shadow → blue window bar → DOM type → grain. Four cues:
atmosphere on the far ridge, occlusion by the spruce line, scale gradient in the
spruce, and fog in the sky's own hue. Focal plane is the cloud base.

**6. CONTINUITY DEVICE STATE.** Horizon y500 (2030). Sun el 26 az 128, late
morning. Near ground is moss, duff and charcoal. Gold is the anemometer tick, a
real instrument in a real place. Blue is the modelled burn window, a computed
span. The gold instrument sits inside the blue window's horizontal extent, which
is the wordless point.

**7. TECHNIQUE STACK.**
- MACRO: the sky carries this octave. Five-stop OKLCH ramp keyed to solar
  elevation 26, `#4E7A96` to `#C8D6DE` to `#E4D7B8`, plus an fbm-displaced
  cumulus band at coverage fraction 0.48 seeded 20260831, base sitting just
  above the horizon, with a legible mixing-height line drawn and carrying NO
  number attached. Ground band gets `AK.reliefShade(cx, {x:0, y:790, w:1080,
  h:560, scale:2, seed:20260831, noiseScale:0.0028, octaves:5, warp:0.55,
  strength:1.87, low:'#243026', high:'#C8A24A', ambient:0.36, diffuse:0.62,
  lights:[{az:128, el:26, w:1.0}]})`. **Encodes C45** as amplitude and the
  48-month clock as wavelength.
- MESO: `AK.hachureField(cx, {x:0, y:840, w:1080, h:400, scale:2,
  seed:20260831, cell:15, passes:4, lenScale:1.9, sunAz:128, sunEl:26,
  sunJitter:11, color:'#243026', alpha:0.11, minWidth:0.45, maxWidth:3.02,
  height: standDensity, probes:[{name:'inside the unit', x:180, y:900, w:240,
  h:200},{name:'outside the unit', x:720, y:900, w:240, h:200}]})`.
  `standDensity` is black spruce stand density, higher outside the burn unit and
  thinned inside it. **Encodes C43**, the geographic and seasonal patterns the
  toolkit characterises, expressed as the thing a burn boss actually looks at.
  **DECLARED PREDICTION: probe `outside` meanWidth / probe `inside` meanWidth
  in the range 1.7 to 2.2, and `widthRatio >= 3.0`.**
- MICRO: moss and duff as a fur field #10 at 5 to 9 steps, plus Bayer 4x4
  dither #17 in the charcoal patches, y1180 to y1350, density falling from the
  bottom edge, plus grain tile 280/48 at 0.06.

**8. DATA-IN-ART MAPPING.** Relief strength 1.87 is the log-scaled 1,588,147
obligated dollars (C45). Wavelength 0.0028 is the 48-month clock (C16 pattern,
C45 dates). Hachure height is stand density, the physical variable the toolkit
exists to read against (C43). NO burn-window quantity is drawn or printed,
because C48 is unverified and this deck does not assert what it has not checked.

**9. PALETTE ASSIGNMENT.** sky `#4E7A96` to `#E4D7B8`; cumulus `#F4F8FF` at
0.86; far ridge `#5E7A72`; spruce silhouette `#243026`; relief ramp `#243026` to
`#C8A24A`; charcoal `#2A2622`; type `#F4F8FF` in the sky zone, `#131C24` on the
light band; tick `#FFC72C`; window bar `#6EA5FF`. The headline sits on the
brightest part of the sky, so it is set in `#131C24` ink there, giving about
12.8 to 1.

**10. TYPE SPEC.** Headline Fraunces 72px `opsz 144 wght 300 SOFT 0 WONK 0`,
leading 1.00, tracking -1%, `#131C24`, max width 660px, `AK.fitText({min:56,
max:72, maxLines:2})`. Body Space Grotesk 34px 400, leading 1.38, `#131C24`, max
width 540px. Mono labels 22px 600 on measured knockout plates.

**11. ICONOGRAPHY / ANCHOR SPEC.** Literal anchor is the gold anemometer tick, a
3-cup glyph under 30 px on a 26 px mast at (840, 742), with a two-part contact
shadow declared onto the lit ground. Annotation furniture is one leader from the
tick to `STATION`, ending ON (840, 742) and declared; the blue window bar with
round-cap terminals; a mixing-height hairline; and a scale bar at `--w-hair`.

**12. REFERENCE INTENT.** A prescribed-fire go/no-go morning, photographed from
the unit boundary, where most of the picture is the sky because the sky is the
decision.

**13. RISK FLAGS.** (a) A 62 percent sky will band; IGN dither is mandatory and
declared. (b) Dark type on a light sky inverts the deck's register; deliberate,
this is the brightest slide and the ink is `#131C24`, an in-palette value. (c)
`data-breather` demotes the frame-balance FAIL to a warning, which could license
a dead band; the lower-third plan above is written to clear the check on its own
merits and the acceptance checklist tests it.

**14. ACCEPTANCE CHECKLIST.**
- [ ] `data-breather` is present on the body AND this dossier declares the
      breather. Both, or neither.
- [ ] The sky shows no visible 8-bit banding at 100 percent zoom.
- [ ] The bottom 170 px carries moss texture AND charcoal dither, both
      resolvable.
- [ ] The gold anemometer tick falls inside the horizontal extent of the blue
      window bar.
- [ ] No number of any kind is attached to the mixing-height line or the window.
- [ ] Headline contrast on the brightest sky pixel under it is at least 4.5 to 1.
- [ ] The horizon sits at y500.
- [ ] Exactly one gold element and exactly one blue element.

---

## SLIDE 05 — THE MOVING GROUND

**1. BEAT.** The deck's brightest, most exposed frame. Inherits the burn window
loop and turns from air to earth. Plants the loop that the instrument is already
buried, so what is the machine adding.

**2. COPY, FINAL.**
- Kicker, mono 24px: `AWARD 2608510, GAIA` (19 chars) [C20]
- Headline, Fraunces 72px, two lines: `The ground that is` / `already moving.` (32)
- Body, Space Grotesk 30px:
  `Surrogate models fed live observations, producing real time digital twins
  that forecast geohazards.` [C25, C26]
- Meta block, mono 21px, on a solid plate:
  `CARL TAPE, WITH THREE CO-INVESTIGATORS` / `1,772,170 OBLIGATED DOLLARS,
  THROUGH JULY 31ST, 2032` / `TESTED ON LANDSLIDES IN ALASKA` [C23, C21, C22]
- Gold label, mono 22px: `STATION` (7 chars)
- Blue label, mono 22px: `SURROGATE FIELD` (15 chars)
- Counter `05 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** A model that runs fast enough to forecast a landslide
while it is still happening, tested on Alaska ground.

**4. LAYOUT MAP.** A slope at mid-afternoon under the deck's highest sun.
Horizon at y460. Kicker row 1, headline cols 1 to 7 rows 2 to 3, body cols 1 to
6 row 4. The slope runs from upper left down to lower right across rows 4 to 8.
Gold seismic station triangle already buried in the hillside at (306, 942), only
its top plate showing. Blue surrogate displacement field draped over the slope
above it, cols 5 to 12, rows 4 to 6. Focal point at the station (0.28, 0.70).
Quiet zone cols 8 to 12 rows 2 to 3, about 17 percent.

**4a. Lower-third treatment.** The lower band is the slope's own toe, carrying
the graded relief substrate at strength 1.90 whose modelled terrain form runs to
the bottom bleed, with the hachure field's stroke widths following the local
displacement gradient down into it and a two-part contact shadow falling from
the buried station's top plate onto ground already lit by the 34 degree key.
Weathered schist scree supplies the micro texture, drawn with `akengrave`'s
swelled-line intaglio at a low raking key, with crosshatch gated to appear only
where tone drops below the mid range and interdots only in the darkest fifth,
which is a per-region detail budget expressed as a drawing system rather than as
a promise. Scree clast size grades from three px at the bottom edge to under one
px at the band's top, so the depth-of-field rule is made literal and the band
holds a real focal plane. No plate, hairline or caption is doing this work.

**5. DEPTH PLAN.** Sky ramp → far range with atmospheric fade → relief substrate
on the slope → hachure on displacement → engraved scree micro → buried station
and shadow → blue surrogate field → DOM type → grain. Five cues: atmosphere on
the far range, occlusion of range by slope, scale gradient in the scree, depth of
field toe-sharp to horizon-soft, and the two-part contact shadow. Focal plane is
the station and the scree around it.

**6. CONTINUITY DEVICE STATE.** Horizon y460 (2032). Sun el 34 az 180, solar
noon, the deck's brightest. Near ground is schist scree. Gold is the seismic
station, an instrument that has been in the ground for years. Blue is the
surrogate displacement field, which is new. The blue lies OVER the slope the
gold is buried in, which is the wordless argument about what the money adds.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:600, w:1080, h:750, scale:2,
  seed:20260833, noiseScale:0.00187, octaves:6, warp:0.62, strength:1.90,
  low:'#12222E', high:'#E4D7B8', ambient:0.30, diffuse:0.70,
  lights:[{az:180, el:34, w:1.0}]})`. **Encodes C21** as amplitude and the
  72-month clock (C22) as wavelength, which is why this slope is the
  longest-wavelength, most open-formed ground on any surface slide.
- MESO: `AK.hachureField(cx, {x:0, y:660, w:1080, h:520, scale:2,
  seed:20260833, cell:13, passes:4, lenScale:1.9, sunAz:180, sunEl:34,
  sunJitter:11, color:'#12222E', alpha:0.12, minWidth:0.45, maxWidth:3.07,
  height: displacementField, probes:[{name:'above the failure plane', x:600,
  y:700, w:240, h:180},{name:'below the toe', x:180, y:1020, w:240, h:180}]})`.
  `displacementField` is a modelled slope-displacement magnitude, highest just
  above the failure plane. **Encodes C25 and C26.**
  **DECLARED PREDICTION: probe `above` meanWidth / probe `below` meanWidth in
  the range 1.8 to 2.5, and `widthRatio >= 3.2`.**
- MICRO: weathered schist via `akengrave` swelled line, `eng.reserve(
  AKENGRAVE.boxesFor(sel))` called after `document.fonts.ready` so no stroke is
  ever generated inside a text box, `crossDeg` gated at tone <= 0.45 and
  interdots at <= 0.22, y1150 to y1350, plus grain tile 280/48 at 0.07.

**8. DATA-IN-ART MAPPING.** Relief strength 1.90 is the log-scaled 1,772,170
obligated dollars (C21). Wavelength 0.00187 is the 72-month clock (C22).
Hachure height is modelled displacement (C25). The blue field's extent stops at
the failure plane, which is what a surrogate model actually bounds.

**9. PALETTE ASSIGNMENT.** sky `#5E86A0` to `#C8D6DE`; far range `#6E8290` with
atmospheric fade; relief ramp `#12222E` to `#E4D7B8`; schist `#8A8A82` on
`#3A3E3E`; hachure `#12222E`; type `#131C24` on the lit slope and `#F4F8FF` in
the sky zone; station `#FFC72C`; surrogate field `#6EA5FF` at 0.42 with a
`--w-fine` boundary. Worst case body `#131C24` on `#E4D7B8` at about 12.2 to 1.

**10. TYPE SPEC.** As slide 03, with the headline in `#F4F8FF` because it sits
in the sky zone and the body in `#131C24` because it sits on the lit slope.
Every mono label on a measured `AK.svgPlate`.

**11. ICONOGRAPHY / ANCHOR SPEC.** Literal anchor is the buried seismic station,
a gold triangle top plate 24 px on a side at (306, 942) with its buried body
implied by a phantom dash outline (#67) below grade, and a two-part contact
shadow declared where the plate meets the scree. Annotation furniture is one
leader from the plate to `STATION`, ending ON (306, 942), declared; the blue
field's boundary; a slope-angle dimension call; and a scale bar.

**12. REFERENCE INTENT.** A slope-stability site visit at solar noon, where the
old instrument is nearly invisible and the new model is the thing draped over
everything.

**13. RISK FLAGS.** (a) `akengrave` calls `form` four times per sample and can
put millions of calls on the main thread; the form is precomputed to a 4px
lookup grid and handed in as a bilinear sampler. (b) A 34 degree key flattens
swelled-line width variance; the engrave pass uses its own low raking key at
elevation 24 for the scree only, which is the documented craft decision, while
the relief substrate uses the true 34 degree key. (c) The blue field over a lit
slope could fail contrast for its label; the label sits on a measured knockout.

**14. ACCEPTANCE CHECKLIST.**
- [ ] The buried station reads as buried, with only the top plate above grade.
- [ ] Scree clast size visibly grades from bottom edge to band top.
- [ ] `widthRatio` at least 3.2.
- [ ] No engraved stroke crosses any text glyph anywhere in the frame.
- [ ] The blue surrogate field stops at the failure plane, not at the frame edge.
- [ ] The contact shadow at the station plate measures at least 4.0 L*.
- [ ] The horizon sits at y460.
- [ ] Exactly one gold element and exactly one blue element.

---

## SLIDE 06 — THE ROCK, FROM BOTH ENDS

**1. BEAT.** The deck's hero and its deepest sight. Inherits the surrogate loop
and answers it with the two projects that read rock from opposite ends, one
recovering metal from waste already dug and one hunting ore nobody has found.
Plants the loop that this is the biggest number on the page.

**2. COPY, FINAL.**
- Kicker, mono 24px: `AWARDS 2614749, 2614751, 2532372` (32 chars)
- Headline, Fraunces 72px, two lines: `The same rock,` / `from both ends.` (29)
- Body, Space Grotesk 34px (48 words):
  `One four year project recovers critical minerals from coal refuse and ash,
  obligating 4,737,612 dollars across Anchorage and Fairbanks. Anchorage holds
  about four times what Fairbanks holds. A ten year Engine hunts ore bodies
  nobody has found, with a co-PI listed at a nana.com address.`
  [C12, C13, C19, C27, C30, C33, C35]
- Guard, mono 22px: `10,500,000 OBLIGATED OF A 15,000,000 ESTIMATED TOTAL.
  COOPERATIVE AGREEMENT.` [C28, C29, C31]
- Note, mono 22px: `THE ABSTRACT NAMES ALASKA NATIVE CORPORATIONS AMONG
  PARTNERS` [C36]
- Gold label, mono 22px: `ASSAY` (5 chars)
- Blue label, mono 22px: `CONCEALED BODY, MODELLED` (24 chars)
- Counter `06 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** Two projects read rock from opposite ends, and the one
looking for what nobody has found gets ten years and the deck's biggest number.

**4. LAYOUT MAP.** The deck's only two-horizon frame. A near refuse ridge with
its crest at y500 (2030) and a far range at y380 (2036), with the overlap doing
the depth work. Kicker row 1, headline cols 1 to 7 rows 2 to 3 in the sky
between the two horizons, body cols 1 to 6 rows 3 to 4. Gold assay dot on the
refuse pile at (760, 860). Blue phantom concealed body drawn under the far range
at cols 3 to 8, y400 to y470, in dash kit #67. Guard and note bottom left rows 7
to 8. Focal point at the assay dot (0.70, 0.64). Quiet zone cols 9 to 12 rows 2
to 3, about 15 percent.

**4a. Lower-third treatment.** The bottom band is the refuse pile's own working
face and it is the most heavily worked ground in the deck. Coal refuse and ash
is drawn at 1:1 hand scale as a Bayer 4x4 ordered dither over a matte
black-brown, with oxidised iron staining picked out in tundra rust where water
has run through the pile, laid over a relief substrate at strength 2.18 whose
form carries the pile's angle of repose to the bottom bleed. The hachure field
continues into the band with stroke widths driven by the Anchorage-to-Fairbanks
mass split, so the band is data-driven rather than decorative, and a two-part
contact shadow falls from the gold assay marker onto ground already lit by the
late-afternoon key. Dither cell size grades from 3 px at the bottom edge to 1 px
at the band's top, giving the band a real focal plane.

**5. DEPTH PLAN.** Sky ramp → far range with heavy atmospheric fade → blue
phantom body under the range → mid-ground valley → near refuse ridge → relief
substrate → hachure → refuse micro → gold assay and shadow → DOM type → grain.
Six cues: atmosphere on the far range, occlusion of range by ridge, scale
gradient in the refuse, depth of field, fog in the sky's own hue between the two
horizons, and the two-part shadow. Focal plane is the near ridge's working face.

**6. CONTINUITY DEVICE STATE.** Two horizons, y500 and y380, the only frame
where the ladder is visible AS a ladder. Sun el 26 az 231, late afternoon,
warm. Near ground is coal refuse and ash. Gold is the assay dot, a sample
somebody took. Blue is the concealed body, which nobody has seen. The gold is
near and the blue is far, which is the wordless argument.

**7. TECHNIQUE STACK.**
- MACRO: two `AK.reliefShade` regions, laid separately because the function
  replaces its region and there is no blend. Near ridge `{x:0, y:790, w:1080,
  h:560, scale:2, seed:20260835, noiseScale:0.0028, octaves:5, warp:0.58,
  strength:2.18, low:'#141110', high:'#6E6153', ambient:0.26, diffuse:0.62,
  lights:[{az:231, el:26, w:1.0}]}`. The high stop was drafted at `#C8A24A` and
  came down after the first render: across an 850px full-bleed region that stop
  does not read as a lit coal face, it renders the whole lower two thirds as a
  gold field, which breaks the 60/30/10 budget and swallows the single gold
  element the slide is allowed. The warmth is carried by the late key instead.
  Far range `{x:0, y:300, w:1080, h:340,
  scale:2, seed:20260836, noiseScale:0.00112, octaves:6, warp:0.70,
  strength:2.40, low:'#3E4E5E', high:'#8FA0AE', ambient:0.44, diffuse:0.40}`,
  deliberately lower contrast because it is far. **Encodes C12 and C29** as two
  amplitudes and **C16 and C30** as two wavelengths, in one frame, which is the
  whole reason this composition exists.
- MESO: `AK.hachureField` on the near ridge, `x:0, y:840, w:1080, h:420,
  seed:20260835, cell:12, passes:4, sunAz:231, sunEl:26, sunJitter:11,
  color:'#2A2622', alpha:0.13, minWidth:0.45, maxWidth:3.47, height:
  massSplit, probes:[{name:'anchorage lobe', x:120, y:900, w:260, h:200},
  {name:'fairbanks lobe', x:740, y:900, w:260, h:200}]`. `massSplit` gives the
  left lobe 3,824,575 and the right lobe 913,037 normalised, so the larger lobe
  is measurably steeper. **Encodes C09, C10, C13.**
  **DECLARED PREDICTION: probe `anchorage` meanWidth / probe `fairbanks`
  meanWidth in the range 1.7 to 2.3, and `widthRatio >= 3.4`.** The dossier
  states about four times in the copy and does NOT claim the stroke ratio is
  four, because stroke width is a slope proxy and not a linear dollar readout.
  **MEASURED ON THE SHIPPED FIELD: anchorage meanWidth 1.925 against fairbanks
  0.976, a ratio of 1.972, inside the declared 1.7 to 2.3; widthRatio 7.449
  against a declared floor of 3.4; meanSlope 0.0474 against 0.0169, so the
  larger lobe is 2.8 times the steepness. The prediction was declared before
  the field was built and it held.**
- MICRO: coal refuse and ash, Bayer 4x4 dither #17 over matte `#2A2622`, with
  `#B4552F` oxidation picked out along runoff paths, y1150 to y1350, cell size
  grading 3 px to 1 px, plus grain tile 280/50 at 0.07.

**8. DATA-IN-ART MAPPING.** Two relief amplitudes are the two obligated figures
(C12, C29). Two wavelengths are the two clocks (C16 four years, C30 ten years).
The mass split between the pile's two lobes is Anchorage against Fairbanks
(C09, C10, C13). The far horizon at y380 is 2036 (C30). The blue phantom body is
drawn in dash kit #67 because it has never been observed (C33).

**9. PALETTE ASSIGNMENT.** sky `#7E92A0` to `#E4D7B8`; far range `#3E4E5E` to
`#8FA0AE`; near ridge `#141110` to `#6E6153`; oxidation `#B4552F`; hachure
`#0B0908`; type `#F4F8FF` in the sky and `#131C24` on the lit pile; assay
`#FFC72C`; concealed body `#6EA5FF` at 0.34 in phantom dash. This is the only
slide carrying tundra rust, and it is a small-area accent per the 60/30/10 rule.

**10. TYPE SPEC.** As slide 05. The guard and note are JetBrains Mono 22px 400
at `rgba(244,248,255,0.72)` on measured knockout plates, and the guard is the
one place the 15,000,000 estimate appears, always with the words estimated total
beside it.

**11. ICONOGRAPHY / ANCHOR SPEC.** Literal anchor is the gold assay dot, a 5 px
filled dot with a 3 px canvas-colour halo ring at (760, 860), with a two-part
contact shadow declared onto the lit pile. Second anchor is the blue phantom
concealed body, an outlined lens shape in dash `30 5 6 5 6 5` at 1.25 px.
Annotation furniture is two leaders, one from the assay dot to `ASSAY` ending ON
(760, 860) and one from the phantom body to its label ending ON its own
boundary, both declared in `window.__akLeaders` with `from`, `label` and `at`;
plus a scale bar and a depth readout at `--w-hair`.

**11a. WORDLESS CLAIM.** The deck's argument in this frame with no words is
that the near, cheap, four-year surface is a pile somebody already dug, and the
far, expensive, ten-year surface has never been seen. The two regions that carry
it are the near refuse ridge at `[0,900,1080,300]` and the far range with its
phantom body at `[0,330,1080,180]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A minerals reconnaissance afternoon, where the sample
in your hand and the target on the horizon are the same element at two
completely different distances.

**13. RISK FLAGS.** (a) Two relief regions could seam visibly at the mid-ground;
mitigated by a graded fog band in the sky's hue between them, drawn after both.
(b) The 15,000,000 figure could be read as money in hand; it appears once, in
the guard, always beside the words estimated total, and never in gold and never
as a drawn quantity. (c) Tundra rust could push the frame warm past the
palette's 60/30/10 budget; oxidation is held under 6 percent of frame area.

**14. ACCEPTANCE CHECKLIST.**
- [ ] Both horizons are visible and distinct, near at y500 and far at y380.
- [ ] The left pile lobe is visibly larger and visibly steeper than the right.
- [ ] The guard line carries 10,500,000 obligated AND 15,000,000 estimated total
      AND the words cooperative agreement.
- [ ] The phantom concealed body is drawn in dash, never solid.
- [ ] Refuse dither is resolvable at 100 percent zoom and grades in cell size.
- [ ] Both leaders arrive at their words within 32 px.
- [ ] The contact shadow at the assay dot measures at least 4.0 L*.
- [ ] Exactly one gold element and exactly one blue element.
- [ ] `data-encodes` declares the two regions and reports at least 4.0 dE.

---

## SLIDE 07 — THE LEDGER

**1. BEAT.** The keepable data slide. Inherits the biggest-number loop and
answers it by putting all six awards on one page. Plants the loop that every
clock starts inside one month.

**2. COPY, FINAL.**
- Kicker, mono 24px: `NSF AWARD API, FETCHED AUGUST 26TH, 2026`
- Headline, Fraunces 72px, one line: `Six awards, one page.` (21 chars)
- Table, JetBrains Mono 26px, tabular figures, six rows plus a total:

| AWARD | SURFACE | OBLIGATED | STARTS | ENDS |
|---|---|---|---|---|
| 2630206 | THE WATER | 50,000 | SEP 1 2026 | AUG 31 2027 |
| 2536745 | THE BURNING WEATHER | 1,588,147 | SEP 1 2026 | AUG 31 2030 |
| 2614749 | THE WASTE, ANCHORAGE | 3,824,575 | SEP 1 2026 | AUG 31 2030 |
| 2614751 | THE WASTE, FAIRBANKS | 913,037 | SEP 1 2026 | AUG 31 2030 |
| 2608510 | THE MOVING GROUND | 1,772,170 | AUG 1 2026 | JUL 31 2032 |
| 2532372 | THE CONCEALED ROCK | 10,500,000 | AUG 1 2026 | JUL 31 2036 |
| | **TOTAL OBLIGATED** | **18,647,929** | | |

  [C02, C45, C09, C10, C21, C29, C37, C38, C39]
- Guard, mono 24px: `OBLIGATED DOLLARS, NOT PROJECT VALUE. THE ENGINE'S
  15,000,000 IS AN ESTIMATED TOTAL ON A TEN YEAR COOPERATIVE AGREEMENT.`
  [C28, C31]
- Method note, mono 22px: `GROUND RELIEF ON EACH SURFACE SLIDE IS SCALED FROM
  THAT AWARD'S OBLIGATED DOLLARS AND ITS PERFORMANCE PERIOD.`
- Counter `07 / 09`, coordinates `data-decorative`.

Dates in the table are a CITATION STAMP in a tabular column, not a sentence, so
the ISO-adjacent compact form is correct there. Every date in prose elsewhere in
the deck takes the ordinal.

**3. READER TAKEAWAY.** Six awards, 18,647,929 obligated, every clock starting
in one month and ending across nine years.

**4. LAYOUT MAP.** Camera stands vertical for the second and last time. Kicker
row 1, headline cols 1 to 7 row 2, table cols 1 to 11 rows 3 to 6 with the
total rule at row 6.4, guard row 7, method note row 8. The table sits on a
plan-view relief whose height field IS the six-award obligation surface. Focal
point at the total rule (0.5, 0.55). Quiet zone cols 9 to 12 row 2, about 12
percent.

**4a. Lower-third treatment.** The lower band is the plan-view ground the ledger
is printed on and it is modelled rather than blank. It carries the
multidirectional relief substrate at strength 2.00 whose height field is the
six-award by eleven-fiscal-year obligation surface, so the paper the table sits
on is literally the shape of the money, with the hachure field running from the
same array over the top so relief and hachure agree by construction. Till and
lichen crust seen from above at 18:00 supplies the micro octave at 0.9 to 1.5 px
stipple, with density falling toward the frame edges per the depth-of-field
rule, and the guard and method note sit on measured knockout plates that let the
modelled ground read continuously around and beneath them. This band was named
by No. 40's scorer as the deck's inert quarter, and it is here the densest
information region in the frame.

**5. DEPTH PLAN.** Relief substrate (multidirectional) → hachure from the same
array → till micro → knockout plates → table type → total rule → grain. Four
cues: multidirectional relief modelling, occlusion of ground by plates, scale
gradient in the till, and depth of field toward the edges. Focal plane is the
table's centre band. This is deliberately the flattest depth plan in the deck,
because it is the paper beat.

**6. CONTINUITY DEVICE STATE.** Plan view, ladder suspended for the second and
last time. Sun el 18 az 253, evening, low. Near ground is till and lichen crust.
Gold is the obligated total rule, the one deliberate gold spend of the deck at
about 1,900 px². Blue is ABSENT, because nothing on this page is modelled, and
the Engine's estimate is drawn in neutral grey rather than in either signal
colour, which is itself the honesty move.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:0, w:1080, h:1350, scale:2, seed:20260837,
  multidirectional:true, noiseScale:0.0034, octaves:5, warp:0.50,
  strength:2.00, low:'#0B1622', high:'#3A5468', ambient:0.34, diffuse:0.55})`
  over a plan-view height field bilinear-sampled from the 6 x 11 obligation
  array. Computed at 1x offscreen and upscaled. **Encodes C02, C09, C10, C21,
  C29, C45, C37.**
- MESO: `AK.hachureField(cx, {x:0, y:0, w:1080, h:1350, scale:2, seed:20260837,
  cell:12, passes:4, lenScale:1.9, sunAz:253, sunEl:18, sunJitter:11,
  color:'#0B1622', alpha:0.10, minWidth:0.45, maxWidth:3.40, height:
  AK.hachureFromGrid(obligationValues, 6, 11), probes:[{name:'FY2027 band',
  x:80, y:300, w:920, h:120},{name:'FY2035 band', x:80, y:980, w:920, h:120}]})`.
  **Encodes the same array as the MACRO octave**, which is the craft claim: a
  critic can verify by eye that the relief and the hachure agree, because they
  are literally the same numbers.
  **DECLARED PREDICTION: probe `FY2027` meanWidth / probe `FY2035` meanWidth in
  the range 1.8 to 2.6, and `widthRatio >= 3.6`.**
- MICRO: till and lichen crust from above, Poisson stipple r 0.9 to 1.5, density
  falling toward all four frame edges, plus grain tile 280/44 at 0.06.

**8. DATA-IN-ART MAPPING.** The page's relief IS the obligation table. The
hachure over it is the same array. The total rule is gold and sits at
18,647,929 (C37). The Engine's estimate is drawn as an open dashed extension
past its solid row, in neutral `#5A6672`, labelled `ESTIMATED TOTAL`, never gold
and never blue (C28, C29, C31).

**9. PALETTE ASSIGNMENT.** bg `#0B1622`; relief ramp `#0B1622` to `#3A5468`;
hachure `#0B1622`; till `#7A8490` at 0.5; plates `#071018` at 0.92 with a 1 px
`#2A4256` top edge; table type `#F4F8FF`; secondary `rgba(244,248,255,0.72)`;
estimate extension `#5A6672`; total rule `#FFC72C`. Worst case table type on
plate is about 15.8 to 1.

**10. TYPE SPEC.** Headline Fraunces 72px, one line, `AK.fitText({min:56,
max:72, maxLines:1})`. Table JetBrains Mono 26px 400 with `tabular-nums
lining-nums`, column rules at `--w-hair`, row rhythm 44 px. Total row JetBrains
Mono 26px 600. Guard 24px 400. Method note 22px 400. Every plate sized from the
MEASURED string after `document.fonts.ready` via `AK.svgPlateAll`.

**11. ICONOGRAPHY / ANCHOR SPEC.** The literal anchor is the ledger table
itself, drafted as a title-block table per technique #83 with a 2.5 px outer
border, hairline internal rules and mono small caps. Annotation furniture is the
gold total rule with 45-degree cut terminals, the dashed estimate extension with
a round-cap terminal, a scale bar, and the provenance stamp in the kicker.

**12. REFERENCE INTENT.** A compilation sheet's title block, where the table is
the product and the ground under it is the survey it came from.

**13. RISK FLAGS.** (a) A full-bleed relief at scale 2 is 5.8M px of Sobel plus
Lambert; computed at 1x offscreen and upscaled, with the crispness supplied by
the micro octave at full resolution. (b) A six-row table risks type under the
24 px floor; the table is set at 26 px, above the floor. (c) The dashed estimate
extension could be mistaken for a phantom-modelled element; it is neutral grey,
not forget-me-not, and it is labelled.

**14. ACCEPTANCE CHECKLIST.**
- [ ] All six award numbers are present and correct.
- [ ] Every obligated figure matches its claim exactly.
- [ ] The total reads 18,647,929 and carries the word OBLIGATED.
- [ ] The guard naming the 15,000,000 estimated total is present and legible.
- [ ] No forget-me-not appears anywhere on this slide.
- [ ] The relief under the table is visibly non-uniform and its high regions
      correspond to the larger awards.
- [ ] Table type is at least 26 px and uses tabular figures.
- [ ] The bottom 200 px carries till stipple and modelled relief, not flat fill.

---

## SLIDE 08 — THE TURN

**1. BEAT.** Where the deck's position lands. Inherits the one-month loop and
turns it into the argument. Plants the closing question.

**2. COPY, FINAL.**
- Kicker, mono 24px: `UAF NEWS INDEX, READ AUGUST 26TH, 2026`
- Headline, Fraunces 72px, two lines: `Fifteen headlines,` / `none of these six.` (36)
- Body, Space Grotesk 34px (46 words):
  `The UAF news index carried fifteen headlines dated August 9th to August 21st.
  None names the Engine, GAIA, the bathymetry work, the fire weather toolkit or
  critical minerals. The same index carried a separate AI headline on August
  11th about rural power grids.` [C46, C47]
- Hedge, mono 22px: `ONE INDEX PAGE, READ ON ONE DAY. THE INDEX PAGINATES.`
  [C46]
- Rail labels, mono 22px: `AUG 9`, `AUG 21`, `SEP 1`
- Counter `08 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** The university's own news page ran fifteen headlines in
that window and none of them was any of these six awards.

**4. LAYOUT MAP.** Failing light, wide ground, horizon at y380, the deck's
highest and most distant. Kicker row 1, headline cols 1 to 7 rows 2 to 3, body
cols 1 to 6 rows 3 to 4. The date rail runs horizontally at y1010, cols 1 to 12,
carrying fifteen grey headline ticks between `AUG 9` and `AUG 21`, one of them
forget-me-not for the August 11th rural power grid headline, then a visible gap,
then the gold tick at `SEP 1`. Hedge at row 8. Focal point at the gap (0.66,
0.75). Quiet zone cols 9 to 12 rows 2 to 3, about 16 percent.

**4a. Lower-third treatment.** The lower band carries the wide evening ground
the rail is laid across, modelled and lit rather than left as a bed for
furniture. Duff and lichen returns as the micro material at 1:1 hand scale in a
fur field of 5 to 9 step ticks, over a relief substrate at deck amplitude 2.60
whose long-wavelength form runs to the bottom bleed, with the hachure field's
stroke widths following the funding-by-year surface into the band and a graded
dusk wash in the sky's own hue pooling in the hollows. Every rail tick throws a
two-part contact shadow onto that lit ground, so the rail sits ON the terrain
rather than floating over it, and the gold September 1st tick is the brightest
point in the band. Texture density falls from the bottom edge, holding the focal
plane.

**5. DEPTH PLAN.** Dusk sky ramp → distant range with heavy atmospheric fade →
relief substrate → hachure → duff micro → rail and its ticks with shadows →
DOM type → grain. Five cues: strong atmospheric perspective at the deck's
longest sight line, occlusion of range by ground, scale gradient in the duff,
depth of field, and two-part shadows under every tick. Focal plane is the rail.

**6. CONTINUITY DEVICE STATE.** Horizon y380, matching slide 06's far range and
slide 09, which is 2036, the deck's longest clock. Sun el 8 az 280, failing.
Near ground is duff and lichen, returning from the cover. Gold is the September
1st tick. Blue is the single August 11th headline tick, which is a different
project and therefore the only modelled-adjacent mark that belongs here.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:340, w:1080, h:1010, scale:2,
  seed:20260838, noiseScale:0.0026, octaves:5, warp:0.55, strength:2.60,
  low:'#0F2033', high:'#8A7E62', ambient:0.30, diffuse:0.44,
  lights:[{az:280, el:8, w:1.0}]})`. **Encodes C37**, the deck total, returning
  to the cover's amplitude now that the whole set has been named.
- MESO: `AK.hachureField(cx, {x:0, y:1040, w:1080, h:310, scale:2,
  seed:20260838, cell:13, passes:4, lenScale:1.9, sunAz:280, sunEl:8,
  sunJitter:11, color:'#0A1622', alpha:0.13, minWidth:0.45, maxWidth:3.95,
  height: fundingByYear, probes:[{name:'early', x:120, y:1080, w:280, h:180},
  {name:'late', x:680, y:1080, w:280, h:180}]})`, the same funding-by-year
  surface as the cover, closing the bracket. **Encodes C38 and C39.**
  **DECLARED PREDICTION: `widthRatio >= 3.0`.**
- MICRO: duff and lichen fur field, same generator and material as the cover at
  a different seed, y1180 to y1350, plus grain tile 280/50 at 0.07.

**8. DATA-IN-ART MAPPING.** Fifteen grey ticks are the fifteen headlines (C46).
One forget-me-not tick at the correct proportional position is August 11th
(C47). The gap between the last headline tick and the gold September 1st tick is
drawn at the rail's own linear date scale, so the gap's width IS August 21st to
September 1st (C38). **The rail IS a measured axis and is declared as
`data-scale` with every one of its seventeen marks enumerated and meaning
something.** There is no decorative tick anywhere in the rail's band.

**9. PALETTE ASSIGNMENT.** dusk sky `#1A2430` to `#8A5E3E`; distant range
`#3E4A56`; relief ramp `#0F2033` to `#8A7E62`; hachure `#0A1622`; duff
`#1B2A22`; rail `rgba(244,248,255,0.34)`; headline ticks
`rgba(244,248,255,0.52)`; August 11th tick `#6EA5FF`; September 1st tick
`#FFC72C`; type `#F4F8FF`. Worst case body on relief high is about 8.9 to 1.

**10. TYPE SPEC.** As slide 05. Rail labels JetBrains Mono 22px 600 on measured
knockout plates. The hedge is `rgba(244,248,255,0.62)`.

**11. ICONOGRAPHY / ANCHOR SPEC.** The literal anchor is the date rail, a
`--w-fine` horizontal rule at y1010 with 45-degree cut terminals, carrying
seventeen marks. Fifteen headline ticks at 3 px x 18 px, one blue tick at 3 px x
24 px, one gold tick at 4 px x 30 px with a 6 px perpendicular terminal.
Annotation furniture is three date labels on measured plates, one leader from
the blue tick to a mono label reading `AUGUST 11TH, RURAL POWER GRIDS`, declared
in `window.__akLeaders` ending ON the tick's own coordinates, and a scale bar.

**12. REFERENCE INTENT.** A dusk field note, where the argument is a gap on a
timeline and the light is going.

**13. RISK FLAGS.** (a) A declared `data-scale` band means qa.py FAILS any
undeclared ink at or above the weakest declared mark's strength inside the band;
the band is kept to y996 to y1024, a 28 px strip, the hachure field is held
BELOW y1040, and the relief in that strip is deliberately low contrast so no
terrain feature reads as strong as a tick. (b) Fifteen ticks could read as
decorative; every one is enumerated in the declaration with its date. (c) Dusk
plus a long sight line risks banding; IGN dither on.

**14. ACCEPTANCE CHECKLIST.**
- [ ] Exactly fifteen grey headline ticks, countable by hand.
- [ ] Exactly one blue tick, at the August 11th position.
- [ ] Exactly one gold tick, at September 1st.
- [ ] The gap between the last grey tick and the gold tick is visibly wider than
      the spacing between any two grey ticks.
- [ ] The hedge about one index page is present and legible.
- [ ] `data-scale` declares all seventeen marks and qa.py reports no undeclared
      ink in the band.
- [ ] The rail's ticks throw visible contact shadows onto lit ground.
- [ ] The horizon sits at y380.

---

## SLIDE 09 — CLOSE

**1. BEAT.** Resolution. Returns to the cover's ground seventeen hours later,
same seed, same terrain, different light. Pays every loop and asks one question.

**2. COPY, FINAL.**
- Headline, Fraunces 84px, two lines: `Which surface should` / `Alaska know best in 2036?` (45 chars)
- Support, Space Grotesk 34px (26 words):
  `Four clocks started September 1st. Two started August 1st. The last one runs
  to July 31st, 2036.` [C38, C39, C30]
- Ask, mono 24px: `SOURCES IN COMMENTS`
- Wordmark: `ALASKA.AI`
- Site fixture, JetBrains Mono 22px, small, beside the mark: `alaskaaihq.com`
- Counter `09 / 09`, coordinates `data-decorative`.

**3. READER TAKEAWAY.** The ranking runs to 2036, and the reader has an opinion
about which surface should have won.

**4. LAYOUT MAP.** The cover's ground at dusk. Horizon at y380, matching slide
08. Headline cols 1 to 8 rows 2 to 3. Support cols 1 to 6 row 4. Gold Polaris
due north in the upper field at (824, 300). Wordmark and site fixture bottom
left rows 7 to 8, ask bottom right row 8. Focal point at the Polaris (0.76,
0.22). Quiet zone cols 9 to 12 rows 4 to 5, about 15 percent.

**4a. Lower-third treatment.** The lower band closes the deck on the same ground
it opened on, seventeen hours later, and it is the frame's most modelled region.
Duff and lichen from slide 01 returns at the identical seed so the terrain is
literally the same ground, drawn as a fur field over a relief substrate at deck
amplitude 2.60, now lit from azimuth 306 at elevation -6 so every form that was
rim-lit on the cover is counter-lit here and the shadow direction has reversed
across the deck. A graded dusk wash in the sky's own hue pools in the hollows,
the hachure field's stroke widths carry the funding-by-year surface to the
bottom bleed, and the wordmark block sits on a measured knockout plate that
lets the modelled ground read continuously around it rather than sitting on a
cleared strip. Texture density falls from the bottom edge, holding the plane.

**5. DEPTH PLAN.** Dusk sky ramp → distant range with atmospheric fade → relief
substrate → hachure → duff micro → Polaris with a three-layer neon stack → DOM
type → grain. Four cues: atmosphere at the long sight line, occlusion, scale
gradient in the duff, and depth of field. Focal plane is the near ground.

**6. CONTINUITY DEVICE STATE.** Horizon y380 (2036), the ladder's highest rung,
held from slide 08. Sun el -6 az 306, past sunset. Near ground is slide 01's
duff and lichen at the same seed. Gold is the Polaris, and it is the only mark
left in either signal colour. Blue is absent, which is the resolution.

**7. TECHNIQUE STACK.**
- MACRO: `AK.reliefShade(cx, {x:0, y:340, w:1080, h:1010, scale:2,
  seed:20260826, noiseScale:0.0026, octaves:5, warp:0.55, strength:2.60,
  low:'#050B14', high:'#4A4436', ambient:0.32, diffuse:0.26,
  lights:[{az:306, el:6, w:0.30}]})`. **Seed 20260826 is the cover's seed**, so
  the terrain is provably identical and only the light has moved. **Encodes
  C37.**
- MESO: `AK.hachureField` over the near ground, same `fundingByYear` height as
  the cover, `sunAz:306, sunEl:6, maxWidth:3.95`, seed 20260826.
  **Encodes C38 and C39.** **DECLARED PREDICTION: `widthRatio >= 3.0`.**
- MICRO: duff and lichen fur field, seed 20260826, identical generator and
  parameters to slide 01, plus grain tile 280/50 at 0.07. The Polaris gets a
  three-layer neon stack (#80) as the deck's last and smallest hot point.

**8. DATA-IN-ART MAPPING.** Relief and hachure repeat the cover's encoding of
the deck total and the funding-by-year surface, at the same seed, so the deck's
first and last grounds are the same measured place under different light. The
Polaris is the brand fixture and encodes nothing, which is stated so no reviewer
reads it as a quantity.

**9. PALETTE ASSIGNMENT.** dusk sky `#050B14` to `#6E5340`; distant range
`#2A3440`; relief ramp `#050B14` to `#4A4436`; duff `#1B2A22`; type `#F4F8FF`;
Polaris `#FFC72C` with `#FFDA6E` halo. Worst case headline on relief high is
about 9.6 to 1.

**10. TYPE SPEC.** Headline Fraunces 84px `opsz 144 wght 300 SOFT 0 WONK 0`,
leading 0.98, tracking -1.5%, `#F4F8FF`, max width 820px, `AK.fitText({min:64,
max:84, maxLines:2})`. Support Space Grotesk 34px 400. Ask and site fixture
JetBrains Mono 22 to 24px on measured plates.

**11. ICONOGRAPHY / ANCHOR SPEC.** The literal anchor is the four-point gold
Polaris at (824, 300), the constellation fixture, at 42 px across with a
three-layer glow. Annotation furniture is the wordmark block, the site fixture
in mono beside the mark, the ask, and the counter. No leader, because nothing on
this slide points at anything.

**12. REFERENCE INTENT.** The cover's field, seventeen hours later, with the
work done and one question left.

**13. RISK FLAGS.** (a) An 84 px headline of 45 characters could run three
lines; `AK.fitText` with `maxLines:2` and an 820 px box, fit record checked.
(b) The Polaris could read as a quantity; it is stated as a fixture in field 8
and sits nowhere near a measured band. (c) Repeating the cover's seed could look
like a duplicate frame at thumb size; the light has moved 274 degrees of azimuth
and the horizon has climbed from y560 to y380, so the two frames share terrain
and share nothing else.

**14. ACCEPTANCE CHECKLIST.**
- [ ] The ask is present and there is exactly ONE ask.
- [ ] `sources in comments` is present.
- [ ] `alaskaaihq.com` is present, small, in the mono face, near the wordmark.
- [ ] The gold Polaris is present and is the only `#FFC72C` in the frame.
- [ ] No forget-me-not appears anywhere.
- [ ] The headline sets on exactly two lines.
- [ ] The terrain is recognisably the cover's ground under different light.
- [ ] The horizon sits at y380.

---

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-08-26. Do not hand-write these lines.
[WARN] render         9/9 slides OK, 0 page errors, 37 overflow warnings
[WARN] qa.py          WARN, 0 fails, 103 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 62 line(s), 4453 chars
[PASS] caption_check  PASS, 838 chars, hook 107, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 150 authored slide strings all present in the render
[PASS] aggregate      aggregate_check: PASS -- 17 aggregate assertion(s) detected, 17 declared -> out/2026-08-26/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 35 claims indexed, 0 declared counts checked, 0 drift(s)
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.167 (fail at 0.60), max pair 0.359, drawn share 76% (128 drawn vs 41 block
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] docket_dates   docket dates clean at 2026-08-26: 285 assertions over 6 fixtures and 22 ledger items
[PASS] gas_watch      21 day(s) on record, 21 verified, no gaps, latest 2026-08-25, EIA through 202605 over 131 months, model misses by 6.82%
[FAIL] site_fresh     FAIL: docs/ is not what site_build.py builds from the committed data at --date 2026-08-26.
[PASS] assemble       9 slides, pdf vector 13.37 MB, 9 thumbs
[n/a ] score          score_report.json missing
[FAIL] ship_gate      score_report.json missing. The run cannot ship or stop until it has been scored. ITERATE, do not stop. weakest: ?
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 2 FAIL row(s). Fix the artifact, not the sentence.
```

