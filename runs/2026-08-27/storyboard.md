# STORYBOARD, Carousel No. 42, 2026-08-27

## THE ROOM, AND WHAT THE SHOWRUNNER TOOK

Three treatments came back. All three independently chose a scattering medium
over lit surfaces, and two independently invented the same continuity device, a
texture level distinction between what an instrument recorded and what a model
supplied. That convergence is the strongest signal the room produced, so it is
the deck's spine.

**The chassis is LENS B, the field documentarian.** Its SOUNDING COLUMN is the
best hero structure of the three, because a to-scale vertical section of one
night's atmosphere carries the physics and the epistemology in one object. The
radar looks from its beam upward. The claim is about water reaching the ground.
The gap between those two facts is a shape, and it can be drawn.

**Grafted from LENS A, the data journalist.** Its slide 07, three bands of the
same figure drawn at true scale and each narrower than the last, is the single
best data slide either room produced and it is the thesis in one keepable frame.
Lens B's arc was a beautiful field record that never stated the argument. This
graft fixes the one real hole in it.

**Grafted from LENS C, the editorial essayist.** Its refusal, "a gap in the
record is not a finding," is what makes this deck publishable rather than
insinuating. It becomes slide 08's stated turn rather than its own slide, because
nine is the budget and the physical arc needs its beats.

**Overruled from LENS A.** The proposal to write a new marked-volume renderer,
akmurk, this run. Lens A named this as its own biggest risk and it was right.
`assets/js/akstipple.js` is committed, tested, shipped once, and does exactly
this job, with `height` required and no default so the mark population is
structurally a function of the story's own quantity. The reason no director
proposed it is that it is not in TECHNIQUE_LIBRARY.md, which is logged as a
Phase 12 candidate in `out/2026-08-27/upgrade_candidates.md`.

**Overruled from LENS C.** Nine slides inside one cloud with Alaska present only
in words. Lens C flagged this itself as its weakest point and the fix it proposed
is the one taken. Slide 05 and slide 06's ground line carry the real Kenai
coastal profile from committed geodata, and slide 03 sets the wet area against
the borough at true area ratio.

---

## DECK HEADER

### Thesis

**An operation that was precise to the second produced a number that is a range,
and every retelling made the range narrower, starting with the company's own.**

### Document title (51 characters)

`Nineteen Flares Over the Kenai, and One Number`

### Arc

| # | Beat | Temperature |
|---|---|---|
| 01 | HOOK. Inside the cloud at the first release, and the tension named. | Cold, one hot point |
| 02 | PAYOFF. The operations log Alaska has not seen. | Precise, factual |
| 03 | ESCALATION. How little material, over how much ground. | Rising |
| 04 | THE PHYSICS. The one thing that had to be right, and the night's one direct measurement. | Steady |
| 05 | BREATHER. The dark, the Gulf low, the ranges, nobody watching. | Quiet, the trough |
| 06 | HERO AND TURN. The column to scale. Where the instrument stops. | The pivot |
| 07 | DATA. Three widths of one figure. | Sharp |
| 08 | HONESTY. What was checked, what came back, and the refusal. | Level |
| 09 | CLOSE. One ask. | Resolved |

Cadence is HOOK, context, point, point, breather, hero, data, synthesis, close,
which is the nine-slide rhythm CAROUSEL_CRAFT names. Slides 06 and 07 are the
two peaks and 05 is the trough between the escalation and the turn.

### Slide count rationale

Nine. The physical event has four beats (log, material, physics, section), the
argument has two (the three widths, the record), and the deck needs a cover, a
breather and a close. Eight would cost the breather, which is where attention
normally dies and which this deck needs because slides 06 and 07 are both dense.
Ten would add a beat the material does not have.

### Continuity system

**Device A, load bearing. THE ALTIMETER TAPE.** A vertical instrument tape at
x 940 to 1000, y 120 to 1230 on every slide. Minor ticks every 100 m at hair
weight, major ticks every 500 m at fine weight with mono labels. A gold index
chevron marks the camera's altitude. The `NN / 09` counter sits at the tape's
head, so the tape IS the progress indicator. State changes are shape changes,
never brightness alone.

**Device B, load bearing. INK IS RECORDED, VOID IS MODELED.** A texture level
distinction and the deliberate replacement for the burned GOLD IS MEASURED, BLUE
IS MODELLED of No.41. Three states, legend printed once on slide 02 and never
again:

- **INK.** Drawn marks. Poisson stipple, swelled engraved line, hachure, solid
  ticks. Anything an instrument recorded or a document prints verbatim.
- **VOID.** The marks stop. A hole in the texture bounded by a phantom dash
  (`30 5 6 5 6 5` at 1.25px) and always carrying a mono label naming what it is,
  because an absence does not identify itself.
- **THINNING.** A smooth density falloff with no boundary, used only for type
  reserves, so a reserve can never be misread as a void.

**Device C, support. EDGE TEASE.** Slides 01 through 05, the flare plume or a
falling streak population is cut by the right edge and completes on the next
slide. Slides 06 through 08, a dimension line's extension runs off the right.

**Device D, support. PALETTE ARC, THE DESCENT.** The flare is the only heat in
the deck and the deck leaves it behind. Scattered red appears on 01, 02 and 03 at
up to 12 percent of frame area, is gone by 05, and from 06 onward gold is the
only warm thing left.

### Motif state table

| # | Altimeter tape | Index altitude | Ink emphasis | Void here | Edge tease |
|---|---|---|---|---|---|
| 01 | Full tape, top third lit, lower two thirds at 25 percent | 3,500 to 4,200 m (C18) | Cloud body, drone silhouette, flare | None. The night is all record | Flare plume cut right |
| 02 | Tape gains a second column, the UTC clock | 3,500 to 4,200 m | 19 ticks, 7 mission blocks, 2 drone lanes | Interior spacing between releases, and the 10 flight ghost lane | Timeline runs off right |
| 03 | Silver iodide stipple bleeds across the tape's left rail, occluding four minor ticks | 3,500 to 4,200 m, adds 374.3 g | 3,743 plume dots, borough silhouette | The wet area boundary, modelled threshold | Plume drift cut right |
| 04 | Tape grows a temperature column to its left | 1,874 m, gold, the sounding | Isotherm ribbon, crystal population, freezing level rule | None. The deck's most measured moment | Isotherm runs off right |
| 05 | BREATHER. Tape reduced to a hairline ghost, no ticks, index at 20 percent | No printed value | Ridge silhouettes, flow streaks, coastal profile | None. The device rests | None. Rest |
| 06 | HERO. The tape becomes the slide, full column 0 to 4,300 m at true scale | 1,874 m, gold | Cloud mass, four named altitude rules, ground profile | The 1,800 m under the lowest beam. The deck's largest void | Dimension extension right |
| 07 | Tape rotated flat, becomes the acre foot axis | 0 m | Three band walls, tick labels, the stair | Rows 1 and 2 are voids, row 3 has no width at all | Implied fourth row cut bottom right |
| 08 | Tape drawn entirely as phantom dash, no ticks. The record that could not be read | Index migrates onto the SOURCED plate | The sourced rows, engraved | The three rows that came back empty | Ledger rule right |
| 09 | Tape collapses. The index chevron resolves into the gold Polaris | 0 m, ground | Column base, ground profile, wordmark | None. Sealed | None. Close |

### Variety ledger check, and this deck's required divergence

| Axis | Last four decks | This deck |
|---|---|---|
| Hero structure | locked lens with substituted ground (38), vacant fixture in two registers (39), the 750 apron (40), the horizon ladder (41) | **NEW: THE SOUNDING COLUMN.** One night's atmosphere as a to-scale vertical coordinate system with four named physical surfaces in it, and a camera descending through it slide by slide. Divergence from the horizon ladder stated explicitly. The ladder was many repeated horizon LINES used as a time axis, viewed from outside. This is one continuous MEDIUM with named surfaces, and the deck is inside it. |
| Atmosphere | wet ceiling, near point inspection lamp with sediment fog, high mast and illuminator, the travelling day | **NEW: SUPERCOOLED INTERIOR.** Inside a scattering medium at the minus 5 to minus 15 Celsius activation window. Not one specular highlight and not one lit surface in nine slides. Form carried by density and by stroke swell. |
| Continuity | CELL 0016 (40), GOLD IS MEASURED BLUE IS MODELLED (41) | INK IS RECORDED, VOID IS MODELED, plus the altimeter tape. Texture level, not colour level. |
| Hook archetype | the measured absence (39), the order of operations (40), two figures at one scale (41) | **NEW: THE PRECISE NIGHT AND THE ROUND NUMBER.** An event knowable to the second and the gram produced a figure knowable only to a factor of two. |
| Palette family | rock flour and arc light, night apron IR and sodium, low sun yellow birch | **NEW: RED FLARE IN A COLD CLOUD.** Derived from the source string "19 red flares" (C03) and from supercooled marine stratus at night. |
| Type pairing | Archivo with Mono (40), Fraunces with Space Grotesk and Mono (41) | Instrument Serif with JetBrains Mono. Two families. Manrope does not appear. |

### Variance dials

**design_variance 4.** High, not maximal. The last four decks each invented a
new hero structure and still scored 6 on artwork craft, so novelty of SYSTEM is
not the lever. Spend the variance on surface.

**visual_density 5.** The run's single biggest departure and the direct attack on
the standing weakness. Density means DRAWN density, texture and annotation
furniture, never more elements or more words. The restraint budget still binds
and the quiet zone still exists, bounded and placed.

**type_temperature 2.** Cool and instrumental, so the type stays out of the way
of a dense surface. A hot display voice on a dense drawn ground is exactly how
"busy art under text" ships, and that class has shipped twice in the window.

### Palette, with roles

| Role | Hex |
|---|---|
| Base, deepest, below the cloud | `#050A12` |
| Cloud far, high optical depth | `#0B1725` |
| Cloud mid, the type reserve fill so contrast is a computed constant | `#17293C` |
| Cloud near, DOF blurred | `#27405A` |
| Supercooled droplet, the stipple ink and secondary labels | `#A9C4DA` |
| Ice crystal, brightest, brand snow. Headline type and the top 4 percent of droplets | `#F4F8FF` |
| Silver iodide, slide 03 plume marks | `#C9CFD6` |
| Flare core, emissive, slides 01 and 03 only | `#FF6A3D` |
| Flare deep, the pyrotechnic body | `#C0301E` |
| Scattered halo where the red dies into the medium | `#7A3A46` |
| Coast and spruce, slides 05 and 06 ground only | `#16352C` |
| Radar beam sheet, slide 06 only | `#5AC8F0` |
| **Accent, gold** | **`#FFC72C`** |

**Gold budget, audited.** `#FFC72C` is emitted by exactly one function,
`drawIndexChevron()`, plus the Polaris path on slide 09. One grep for the hex
proves it. The chevron means one thing on every slide, which is where the camera
is in the column. No second accent anywhere.

Ramps built with `AKC.ramp` at 7 steps, keyHue toward the flare on 01 to 03,
ambientHue toward `#0B1725` in shadow. Gradients through `AKC.mixOklab`. Never
nest `lerpHex` inside itself; it returns an `rgb()` string and the nested parse
yields NaN with no console error.

Worst case contrast pairs, declared. `#F4F8FF` on `#17293C` about 12.3 to 1.
`#A9C4DA` on `#0B1725` about 9.1 to 1. `#C9CFD6` on `#050A12` about 12.8 to 1.
Earned by composition, because every text block sits in a reserved region whose
base fill is known before any mark is generated.

### Type system

**Instrument Serif** display and every verbatim quotation, roman 400 and italic
400. Italic is reserved for the two verbatim strings on slide 07 and appears
nowhere else. **JetBrains Mono** the instrument voice, 300 body, 500 labels, 700
figures, tracking plus 10 percent on small caps labels.

Nothing in this deck is set below **26 px**. The tiny-text warn has shipped twice
in the last ten runs and it is bought out at the spec level rather than at
repair. `AK.fitText(el, {min, max, maxLines})` inside `renderReady` after
`await document.fonts.ready` on every display block.

### THE COLUMN CONSTANT, the deck's single point of failure

One exported object, imported by all nine slide files. If two slides disagree by
four pixels the continuity dies silently, so this is the first item on every
acceptance checklist.

```
COL = { yGround: 1240, yTop: 90, mTop: 4300 }
y(alt) = 1240 - alt * (1150 / 4300)      // 0.2674419 px per metre
```

| Altitude | Source | y |
|---|---|---|
| 0 m, ground | ground line | 1240 |
| 1,874 m, freezing level | C08 | 739 |
| 1,800 m, lowest beam floor | C15 | 759 |
| 2,200 m, beam floor top | C15 | 652 |
| 3,500 m, release band bottom | C18 | 304 |
| 4,200 m, release band top | C18 | 117 |

### THE ACRE FOOT AXIS, slide 07 only

```
AX = { x0: 120, af0: 35, pxPerAF: 12.00 }
x(af) = 120 + (af - 35) * 12
```

| Value | Source | x |
|---|---|---|
| 41.70 acre feet | C14 | 200.4 |
| 45 acre feet | C17 | 240.0 |
| 57.62 acre feet, the mean | C14 | 391.4 |
| 58.31 acre feet, 19 million gallons converted | C16, studio arithmetic | 399.7 |
| 65 acre feet | C17 | 480.0 |
| 89.35 acre feet | C14 | 772.2 |

Band widths, 571.8 px (47.65 acre feet), 240.0 px (20.00 acre feet), 0 px.

### Claims index

| Claim | Slides |
|---|---|
| C01 | 01, 02 |
| C02 | 02, 05 |
| C03 | 01, 02 |
| C04 | 02 |
| C05 | 03 |
| C06 | 01, 02 |
| C07 | 04 |
| C08 | 04, 06 |
| C09 | 03 |
| C10 | 06 |
| C11 | 07 |
| C12 | 07 |
| C13 | 07 |
| C14 | 07 |
| C15 | 06 |
| C16 | 01, 07 |
| C17 | 07 |
| C18 | 01, 02, 06 |
| C19 | 02 |
| C22 | 02 |
| C20 | 05 |
| C29 | 02 |
| C30 | 08 |
| C32 | 08 |
| C33 | 08 |
| C34 | 08 |
| C35 | 08 |
| C36 | 03 |
| C37 | 08 |
| C38 | 07 |
| C39 | 01 |

NOT USED, and each must appear nowhere in the deck. C21, C23, C24, C25,
C26, C27, C28, C31, C40. The Atmo material and most of the Stratus material
(C23 to C28) is cut
because the honest version of it is narrow, the fact-checker killed "the AI
decides where and when it rains", and a deck that leans on vendor marketing
figures to establish the AI angle would be doing the thing this deck criticises.
The AI is established once, on slide 02, from C22's own careful wording, and is
not stretched further. C40, the ALPA line, is omitted per the default in
selection.md.

---

## SLIDE 01, COVER

### 1. Beat
The hook. Put the reader inside the cloud at the moment of the first release and
name the tension in one breath. Inherits no loop. Plants the deck's only
question, which is how an event this precise produced a number this round.

### 2. Copy, final

- Kicker, JetBrains Mono 500, 27px, tracked +10 percent, uppercase:
  `KENAI PENINSULA, AUGUST 23RD, 2026` (34 chars) (C01)
- Headline, Instrument Serif 400, fitted 118 to 146px, 3 lines broken by sense:
  `Nineteen flares burned` / `over the Kenai.` / `Alaska got one number.` (60
  chars, 10 words) (C03, C16)
- Corner readout, JetBrains Mono 500, 26px:
  `06:38:18 UTC, FIRST RELEASE (C06)` (33 chars)
- Local time note, JetBrains Mono 300, 26px:
  `THE EVENING OF AUGUST 22ND IN ALASKA (C39)` (42 chars)
- Counter, JetBrains Mono 700, 27px: `01 / 09`

### 3. Reader takeaway
Something happened over the Kenai four nights ago that produced a single famous
number, and this deck is going to take that number apart.

### 4. Layout map
Twelve column grid, 80px margins. Headline occupies columns 1 to 8, rows 3 to 5,
left aligned, optical left edge pulled 6px past the margin so the N stem aligns.
Focal point is the flare at the rule of thirds intersection, (720, 450), which is
columns 9 to 10, row 3. Eye path is flare, then headline, then the drone
silhouette low right at (860, 1010). Quiet zone is the thinned region behind the
headline, columns 1 to 8, rows 3 to 5, about 22 percent of frame. Single
permitted grid violation is the flare's bloom crossing the right margin.

4a. **Lower-third treatment.**
The bottom band carries the densest part of the scattering medium plus the
falling ice streak population entering from the release layer above. Below y 900
the stipple density function rises from 0.42 to its frame maximum of 0.89, so
the lower third is the most heavily marked region of the frame, and the flare's
scattered halo grades through it in `#7A3A46` at low chroma. A graded ground
haze in `#0B1725` closes the bottom 120px, and the drone silhouette sits in it at
hero stroke weight with its rotor seams at hair weight, so a real object with
modeled tone occupies the band rather than furniture floating on bare ground.
The altimeter tape's lower two thirds run through the band at 25 percent, giving
annotation furniture with tick marks inside modeled atmosphere.

### 5. Depth plan
Background `#050A12`, then five aerosol shells at scale 0.72^i with atmospheric
lerp `(i/n)^1.4` toward `#0B1725`, then the aksdf cloud mass, then the emissive
flare inside the mass, then the falling streak population, then the drone
silhouette, then DOM type, then grain. Four depth cues named. Atmospheric
perspective on the shells, occlusion where the mass eats the drone's outline,
scale gradient across the streak population, and depth of field with one tack
sharp plane at the flare and a blurred repoussoir wisp bleeding off the upper
left. Fog is exp2 in `#0B1725`, never gray. Focal plane is the flare at z 0.
Camera is the aksdf hero's camera A, inside the mass.

### 6. Continuity device state
Altimeter tape full, top third lit, index chevron gold inside the release band at
y 117 to 304, printing `3,500 to 4,200 m (C18)`. Ink everywhere, no void, because
the night itself is all record. Edge tease is the flare plume cut mid curl by the
right edge, completing on slide 02.

### 7. Technique stack
**#88 aksdf** camera A. Six primitives blended with quadratic smin into an
overhanging cloud mass, thin shell fbm displacement where `|d| < 0.12`,
tetrahedral normals, 5 tap AO on sky and indirect only, one soft shadow ray at
k 14, fresnel rim, raised indirect floor, one emissive primitive as the flare in
`#FF6A3D`. Rendered 384 x 576 internal, upscaled, `deadlineMs 12000`, cached by
seed `20260827` and shared with slide 06 at camera B.
**#66 stipple via AKSTIPPLE.field**, seed `20260827`, count 16000, height is the
aerosol density function, ramp is the 7 step droplet ladder, radius
`0.8 + 0.7 * q`, alpha `0.30 + 0.55 * q`.
**#14 particle drift** for the falling streaks, 900 particles, trails via
translucent bg rect per step, final frame only.
**#89 akpost** grade, bloom 0.10, exposure -0.05 STOPS, log contrast pivot 0.18,
ACES, gamma, split tone cool in shadow, IGN dither on, unsharp 0.35, chromatic
aberration permitted here.
**#2 grain**, `AK.grainTile(280, 52, 20260827)`, overlay 0.07.
**#84** instrument corner readouts.

### 8. Data in art mapping
The stipple population's baseline density is 58 marks per 10,000 design px
squared, from the mean of 57.62 acre feet (C14), and the field is never drawn
below 42 or above 89 marks per 10,000 px squared, from the band 41.70 to 89.35
(C14). The air the reader is looking at is drawn between the fifth and
ninety fifth percentile of the deck's own subject. The flare's emissive radius is
set from the 3.5 minute nominal burn (C05) as a fraction of the 2 hour 55 minute
window (C06).

### 9. Palette assignment
bg `#050A12`, shells `#0B1725` to `#27405A`, droplet ink `#A9C4DA`, brightest
crystals `#F4F8FF`, flare core `#FF6A3D`, flare body `#C0301E`, scattered halo
`#7A3A46`, headline `#F4F8FF` on reserve fill `#17293C` at about 12.3 to 1,
kicker and readouts `#A9C4DA`, index chevron `#FFC72C`.

### 10. Type spec
Headline Instrument Serif 400, fitted 118 to 146px, maxLines 3, leading 1.00,
tracking -1.5 percent, `#F4F8FF`, max width 760px, left aligned. Kicker JetBrains
Mono 500, 27px, +10 percent tracking, uppercase, `#A9C4DA`. Corner readouts
JetBrains Mono 500 and 300, 26px, `#A9C4DA` at 75 percent. Counter JetBrains Mono
700, 27px.

### 11. Anchor spec
The literal anchor is the drone silhouette at (860, 1010), 90px across, drawn
from a real quadcopter profile, outline at `--w-hero` 5.5px and rotor seams at
`--w-hair` 0.75px per the profile heaviest rule (#58). The annotation is the
altimeter tape with its ticks and printed altitude. Two anchors, which is the
maximum, and zero would be wallpaper.

### 11a. Wordless claim
The flare is the only warm thing in a cold volume and it is small. Regions,
flare core `[690, 420, 60, 60]` versus medium body `[120, 700, 300, 300]`,
`reads: "differ"`. **MEASURE BOTH RECTS OFF THE RENDERED PNG, never off the
camera arithmetic.** Run No.29 computed two probe boxes from camera maths, they
landed on empty water 300px from where the art drew, and the deck's central
wordless claim reported 0.9 dE.

### 12. Reference intent
A NOTAM crossed with a night dive photograph. Precise, unhurried, and cold, with
one fire in it.

### 13. Risk flags
- aksdf carved interiors go near black. Mitigation, raised indirect floor plus
  the emissive flare, which is the story rather than a workaround.
- Banding across a large soft medium. Mitigation, IGN dither always on plus the
  grain tile.
- Headline overflow into the flare. Mitigation, `AK.fitText` with maxLines 3, and
  the reserve field zeroes mark generation inside the measured box.
- The 26px floor must hold. No string on this slide is under 26px.

### 14. Acceptance checklist
- [ ] The column constant matches `COL` exactly and the index chevron sits inside y 117 to 304.
- [ ] Headline renders in exactly 3 lines with no fourth line and no overflow.
- [ ] The flare is the only pixel in the frame warmer than `#7A3A46`, gold chevron excepted.
- [ ] The drone silhouette's outline reads at 432px thumb width.
- [ ] Stipple density visibly rises below y 900; the lower third is denser than the upper third.
- [ ] No mark is generated inside the headline's measured box.
- [ ] `data-encodes` rects were measured off the render, not computed.
- [ ] Every visible string is 26px or larger.
- [ ] The flare plume is cut by the right edge and its continuation exists on slide 02.

---

## SLIDE 02, THE LOG

### 1. Beat
Pay the cover off in one second with the specificity nobody in Alaska has been
given. Inherits the question of what happened. Plants the question of how much
material 19 flares actually is.

### 2. Copy, final

- Kicker: `THE OPERATION, AS PUBLISHED` (26 chars)
- Headline, Instrument Serif, fitted 76 to 92px, 2 lines:
  `Two drones. Seven missions.` / `Nineteen flares.` (43 chars)
- Body, JetBrains Mono 300, 33px, max width 700px:
  `Rainmaker says drones EL-151 and EL-153 released 19 silver iodide flares over the Kenai on August 23rd, between 06:38:18 and 09:33:41 UTC. Missions 4 through 7 were flown by EL-151 alone.` (185 chars, 30 words) (C01, C03, C04, C06)
- Ghost lane label, JetBrains Mono 300, 26px:
  `THE SAME COMPANY, THE SAME DAY, A SECOND POST SAYS 10 FLIGHTS (C18)` (66 chars)
- Void label, JetBrains Mono 500, 26px:
  `ENDPOINTS PUBLISHED. INDIVIDUAL RELEASE TIMES NOT PUBLISHED (C03, C06)` (69 chars)
- Provenance, JetBrains Mono 300, 26px:
  `EL SEGUNDO, CALIFORNIA. ON THE KENAI SINCE JUNE (C19, C29)` (57 chars)
- AI line, JetBrains Mono 300, 26px:
  `THE COMPANY SAYS ITS SOFTWARE PICKS THE SEEDING WINDOW (C22)` (59 chars)
- Legend, three 18px swatches with 26px mono labels: `INK, RECORDED` /
  `VOID, NOT IN THE RECORD` / `THINNING, TYPE RESERVE`
- Counter: `02 / 09`

### 3. Reader takeaway
Nineteen flares, two aircraft, three hours, and one of the drones went home
after mission three.

### 4. Layout map
Headline columns 1 to 7, rows 1 to 2. The timeline occupies columns 1 to 11,
rows 4 to 6, a horizontal axis 760px wide from x 120 to x 880 spanning
06:38:18 to 09:33:41 UTC. Two drone lanes stacked beneath it, EL-151 upper and
EL-153 lower. The ghost lane sits a further 60px below in phantom dash. Focal
point is the point at which the EL-153 lane terminates, at mission 3. Eye path
is headline, then the 19 ticks, then the terminating lane. Quiet zone is columns
1 to 7 rows 1 to 2 behind the headline, about 18 percent of frame. Legend sits
bottom left, columns 1 to 4, row 8.

4a. **Lower-third treatment.**
The bottom band carries the two drone lanes and the seven mission blocks run
down into it over a graded cloud floor, with the medium's stipple field
continuing beneath at density 0.55 so the lanes sit ON modeled atmosphere rather
than on bare ground. The legend's three swatches are themselves drawn texture
samples, a stipple patch, a void with its phantom edge, and a thinning gradient,
so even the legend carries marks. A foreground haze plane in `#0B1725` at 18
percent crosses the lowest 90px and the altimeter tape's ticks run through it,
giving depth and annotation furniture in the same band. The ghost lane's phantom
ticks and their leader lines occupy the band's right half.

### 5. Depth plan
Background, then the medium at reduced density 0.55, then the graded cloud floor,
then the timeline apparatus, then the lanes, then DOM type, then grain. Four
cues, atmospheric perspective on the medium behind, occlusion where the mission
blocks overlap the tape's left rail, scale gradient in the tick heights, and a
foreground haze plane. Focal plane is the lane row.

### 6. Continuity device state
Tape gains a second column, the UTC clock, aligned to the timeline. Index stays
in the release band. First appearance and only appearance of the legend. Ink is
the ticks, blocks and lanes. Void is the interior spacing between releases and
the whole ghost lane. Edge tease, the timeline's axis runs off the right margin.

### 7. Technique stack
**AKSTIPPLE.field** seed `20260827 + 2`, count 9000, height falls off above the
lane row so the composition routes clear space to the type.
**#93 akengrave** for the mission blocks, `light {azDeg 62, elDeg 24}`,
`crossDeg 41`, `step 3`, `wMax 3.2`, `inkLo 0.06`, `inkHi 0.62`, form a shallow
plateau with a 4 percent cylindrical roll. **LOW `tone` MEANS DARK.** Form
precomputed into a 4px lookup grid with a bilinear sampler, per the bench's
performance note. `eng.reserve(AKENGRAVE.boxesFor('[data-reserve]'))` called
after `await document.fonts.ready`.
**#67 alphabet of lines dash kit** phantom `30 5 6 5 6 5` at 1.25px for every
unrecorded element, with **#68 pathLength dash symmetry** at `pathLength="100"`.
**#69 round cap dot rhythm** for the ghost ticks.
**#72 leader discipline**, every leader a world coordinate polyline terminating
on its target's own coordinates, declared in `window.__akLeaders` with `from`,
`at`, `to` and `label`.
**#79 cased line** on every rule crossing texture.
**#83 drafting furniture kit** crop mark Ls.
**#89 akpost**, **#2 grain**.

### 8. Data in art mapping
The timeline axis endpoints are exactly 06:38:18 and 09:33:41 UTC (C06), a span
of 10,523 seconds across 760px. Each of the 19 flare ticks (C03) is a bar whose
length is the nominal 3.5 minute burn (C05), which is 210 of 10,523 seconds, so
**15.2px** each. They are visibly short against the window and that shortness is
the point. Seven solid mission blocks (C02). Two lanes (C04), and the EL-153 lane
terminates after mission 3. The ghost lane carries exactly 10 phantom ticks
(C18).

`window.__akScale` declares the time axis with `from: [120, 0]`,
`to: [880, 10523]`, unit seconds, `band: [560, 600]`, and every mark inside that
band enumerated with its meaning. There is no decorative tick on a measured axis.

### 9. Palette assignment
bg `#050A12`, medium `#0B1725` to `#17293C`, engraved lay `#A9C4DA`, mission
blocks engraved white line `#C9CFD6`, ticks `#F4F8FF`, phantom dash `#7A3A46` at
low chroma for the ghost lane so the red palette arc is still alive here, index
chevron `#FFC72C`, headline `#F4F8FF` on `#17293C`.

### 10. Type spec
Headline Instrument Serif 400, fitted 76 to 92px, maxLines 2, leading 1.02,
tracking -1 percent. Body JetBrains Mono 300, 33px, leading 1.42, max width
700px, about 34 characters per line. Labels JetBrains Mono 500, 26px, uppercase,
+10 percent tracking. All claim id chips 26px.

### 11. Anchor spec
The anchor is the two drone lanes as a real operations log, with the annotation
furniture being the time axis, its ticks, the mission blocks and the leaders to
the ghost lane. Weights, axis at `--w-std` 2px, ticks at `--w-std`, leaders and
all phantom at `--w-fine` 1.25px, engraved lay at `--w-hair` 0.75px.

### 12. Reference intent
An air operations log plate from a technical report, set by someone who cares
about type.

### 13. Risk flags
- Fifteen point two pixel bars are small. They are ink on a knockout window
  (#75) and the axis is cased (#79) so they read at thumb size as a rhythm even
  when individually unreadable, which is honest because their individual times
  were never published.
- The discrepancy must never read as an accusation. Both figures are printed and
  attributed and the label says the company does not reconcile them.
- Leaders into void. Every leader declares `at` on its target's own coordinates.

### 14. Acceptance checklist
- [ ] Exactly 19 flare ticks, countable at full size.
- [ ] Exactly 7 mission blocks and exactly 10 ghost ticks.
- [ ] The EL-153 lane visibly terminates after mission 3 and EL-151 continues.
- [ ] Every mark inside the declared `data-scale` band carries a meaning.
- [ ] The legend's three swatches are drawn texture, not flat colour chips.
- [ ] No engraved stroke is generated inside any measured type box.
- [ ] Both the 7 and the 10 appear on the slide, neither called an error.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 03, THE MATERIAL

### 1. Beat
Escalation. Make the quantity concrete and set it against the ground it covered.
Inherits the question of how much material. Plants the question of what a few
hundred grams can do to a sky.

### 2. Copy, final

- Kicker: `WHAT WAS RELEASED` (17 chars)
- Headline, Instrument Serif, fitted 76 to 96px, 2 lines:
  `374.3 grams of silver iodide,` / `across 249.53 square kilometres.` (61 chars)
- Body, JetBrains Mono 300, 33px:
  `Each flare dispersed about 19.7 grams over a nominal 3.5 minute burn. The company puts the wet area at 249.53 square kilometres, about 0.6 percent of the borough's land.` (167 chars, 28 words) (C05, C09, C36)
- Mark legend, JetBrains Mono 500, 26px: `1 DOT = 0.1 g OF SILVER IODIDE (C05)` (36 chars)
- Void label, JetBrains Mono 500, 26px:
  `WET AREA IS A MODELLED THRESHOLD, 0.01 mm (C09)` (46 chars)
- Ratio note, JetBrains Mono 300, 26px:
  `249.53 SQ KM AGAINST 41,485.21 SQ KM OF BOROUGH LAND (C09, C36)` (62 chars)
- Counter: `03 / 09`

### 3. Reader takeaway
The whole payload was about the mass of a can of soup, and the area it is
credited with is a modelled boundary rather than a wet boot.

### 4. Layout map
Headline columns 1 to 7, rows 1 to 2. The plume occupies columns 4 to 12, rows 3
to 7, drifting down and right. The borough silhouette sits bottom left, columns
1 to 5, rows 6 to 8, with the wet area drawn inside it at true area ratio. Focal
point is the wet area void at (300, 1050). Eye path is headline, plume, then the
void inside the borough. Quiet zone columns 1 to 7 rows 1 to 2, about 17 percent.

4a. **Lower-third treatment.**
The bottom band is the densest stipple in the deck. The silver iodide plume
settles into it and the borough silhouette sits inside that settled material with
its coastline drawn from committed Kenai geodata under the canonical projection,
so the band carries a real anchor with modeled tone rather than a plate. The
borough's interior is a hachure field whose stroke width comes from the gradient
of distance to the coastline, giving genuine per mark texture across the whole
lower left. The wet area is a void cut into that hachure with a phantom edge and
a leader running to its label, so the band holds ink, void and annotation
furniture together. A graded ground haze in `#0B1725` closes the last 80px
beneath the silhouette and the plume's scattered halo grades through it.

### 5. Depth plan
Background, medium at density 0.62, the drifting plume, the borough silhouette,
the hachure interior, the void, DOM type, grain. Four cues, atmospheric
perspective across the plume's depth, occlusion where the plume crosses the
silhouette's upper edge, scale gradient in the plume's mark radius as it recedes,
and a foreground haze plane. Focal plane is the borough silhouette.

### 6. Continuity device state
Tape's left rail is occluded by the plume's stipple across four minor ticks, the
first time the medium eats the instrument. Index adds `374.3 g` to the data
column. Ink is the plume and the hachure. Void is the wet area. Edge tease, the
plume's drift is cut by the right edge.

### 7. Technique stack
**AKSTIPPLE.field** twice. Once for the medium at count 8000, and once for the
plume with `box` restricted to the plume's bounding region so `count` means what
it says, exactly **3,743 marks**, one per 0.1 grams (C05). Passing `box` is
mandatory here; the sampler throws uniformly and rejects, so a small region wins
a fraction of the throws and a previous deck drew its smallest quantity as
literally nothing.
**#92 akhachure** for the borough interior. `height` is the signed distance to
the Kenai coastline built from `assets/geo/alaska-boroughs.geo.json` under
`d3.geoConicEqualArea().parallels([55,65]).rotate([154,0])`. No noise anywhere in
the height field. `passes 4`, `sunAz` varied per pass, `lightBias` on,
`slopeGamma 1.25`. Declared as FORM SHADING ONLY; nobody is asked to read a
magnitude off it.
**#67 phantom dash**, **#72 leader discipline**, **#73 dimension call** for the
area ratio, **#75 hatch knockout windows** so no numeral sits on hachure,
**#79 cased line**, **#89 akpost**, **#2 grain**.

### 8. Data in art mapping
Plume mark count is exactly 3,743, one mark per 0.1 grams of the 374.3 gram total
(C05), declared in `window.__akAssert` as `{what, expect: 3743, points: pts,
unit: "marks"}` with `points` being the array of centres the drawing loop
actually used, so the FRAME does the counting. A count derived from the loop
bound agrees with the type and disagrees with the picture, which is the one
disagreement that matters.

The wet area void's drawn area is 0.6 percent of the borough silhouette's drawn
area, from 249.53 square kilometres against 41,485.21 (C09, C36). Verifiable by
pixel count in the render.

`window.__akMotifs` declares the wet area void as
`{what: "the modelled wet area", rect: [...]}` so the engine reads it back out of
the canvas and fails if it is buried, flat or painted out. Three motifs on three
slides were lost that way in one recent deck with every gate green.

### 9. Palette assignment
bg `#050A12`, medium `#0B1725`, plume marks `#C9CFD6`, scattered halo `#7A3A46`,
borough silhouette edge `#F4F8FF` at `--w-hero`, hachure `#A9C4DA`, void interior
`#050A12` with phantom edge `#7A3A46`, headline `#F4F8FF` on `#17293C`.

### 10. Type spec
Headline Instrument Serif 400, fitted 76 to 96px, maxLines 2. Body JetBrains Mono
300, 33px. Labels 26px mono 500 uppercase. The two figures 374.3 and 249.53 set
in JetBrains Mono 700 at 44px inside the headline block as tabular lining
numerals.

### 11. Anchor spec
The literal anchor is the Kenai Peninsula Borough silhouette from committed
geodata, true projection, outline at `--w-hero` 5.5px. Annotation furniture is
the dimension call on the area ratio, the leader to the void label, and the mark
legend.

### 11a. Wordless claim
The material is almost nothing and the area is enormous. Regions, plume core
`[560, 380, 120, 120]` versus borough interior `[160, 980, 120, 120]`,
`reads: "differ"`. Measure both off the render.

### 12. Reference intent
A materials plate from a field report, with a real map in it.

### 13. Risk flags
- `AKGeo` warning. Never `fitExtent` to a small lon lat bbox, which renders a
  giant fill disc. Use `AKGeo.zoomTo(proj, geo, lonlat, targetXY, zoom)` and draw
  the coastline stroke only at zoom above about 2.
- akhachure with a distance transform may be slow. Fallback declared here rather
  than discovered at build, **#91 aksnow** `AKSNOW.surface` over the same
  coastline contour, which gives carved form and needs no field.
- 3,743 marks in a small box needs `box` passed or the count is a lie.

### 14. Acceptance checklist
- [ ] `__akAssert` reports actual 3743 inside the frame, tolerance 0.
- [ ] The borough silhouette is the real Kenai outline, recognisable to an Alaskan.
- [ ] The wet area void is visibly a hole in the hachure, not a fill.
- [ ] No numeral sits on hachure anywhere.
- [ ] `__akMotifs` reports the wet area rect as present and not flat.
- [ ] The plume's marks visibly vary in radius with depth.
- [ ] The four occluded tape ticks are visible as occluded, not missing.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 04, THE WINDOW

### 1. Beat
The physics, and the night's one direct measurement. Inherits the question of
what the material does. Plants the question of how anyone would know what reached
the ground.

### 2. Copy, final

- Kicker: `THE ONE THING THAT HAD TO BE RIGHT` (34 chars)
- Headline, Instrument Serif, fitted 76 to 92px, 2 lines:
  `Silver iodide only works` / `between minus 5 and minus 15.` (53 chars)
- Body, JetBrains Mono 300, 33px:
  `Every median release temperature landed inside that window. Soundings launched from the site put the average freezing level at 1,874 metres, and that sounding is the night's one direct measurement.` (194 chars, 31 words) (C07, C08)
- Rule label, JetBrains Mono 500, 26px: `FREEZING LEVEL, 1,874 m MSL (C08)` (33 chars)
- Band label, JetBrains Mono 500, 26px: `ACTIVATION WINDOW (C07)` (23 chars)
- Counter: `04 / 09`

### 3. Reader takeaway
The physics of the night was checked with a balloon. The rainfall figure was not.

### 4. Layout map
Headline columns 1 to 7, rows 1 to 2. The isotherm ribbon runs across columns 1
to 12, rows 4 to 5, a horizontal band with its own printed temperature scale. The
crystal population appears only inside the ribbon. The freezing level rule sits
at y 739 per `COL`, running full width at `--w-bold`. Focal point is the
intersection of the ribbon and the tape's temperature column at (940, 560). Eye
path is headline, ribbon, freezing rule. Quiet zone columns 1 to 7 rows 1 to 2,
about 18 percent.

4a. **Lower-third treatment.**
The bottom band carries the crystal population falling out of the activation
ribbon above, drawn as individual marks whose density rises toward the freezing
level rule at y 739 and stops dead below it, which is the physics made visible.
Beneath that rule the medium continues as a graded wash in `#0B1725` with the
stipple field at density 0.48 and a foreground haze plane crossing the lowest
110px, so the band carries modeled atmosphere with a real gradient in it. The
altimeter tape's temperature column and its ticks run down through the band and
the freezing level rule is dimension called into it with leaders, giving
annotation furniture inside modeled tone rather than a plate on bare ground.

### 5. Depth plan
Background, medium at 0.58, the isotherm ribbon, the crystal population, the
freezing rule, DOM type, grain. Four cues, atmospheric perspective on the
population's depth, occlusion where crystals cross the ribbon's lower edge, scale
gradient in crystal size with fall distance, and fog in `#0B1725`. Focal plane is
the ribbon.

### 6. Continuity device state
Tape grows a temperature column to its left and the index chevron moves for the
first time, from the release band down to **1,874 m at y 739 in gold**, because
that is the one in situ measurement of the night. Ink dominant, no void, the
deck's most measured moment. Edge tease, the isotherm runs off the right margin.

### 7. Technique stack
**AKSTIPPLE.field** for the medium at count 8500 and for the crystal population
with `box` on the ribbon and the band beneath it.
**#66 stipple tone field** law inside it, blue noise, never grid jitter.
**#59 tapered ribbon stroke** for the isotherm, polygon from centreline sampled
every 6px, offset by `w(t)/2` along normals with `w(t) = wMax * sin(pi*t)^0.7`.
**#73 dimension call** on the freezing level, extension lines with a 4px gap and
6px overshoot, 3 to 1 arrowheads, centred small caps value.
**#67 dash kit**, **#75 knockout windows**, **#79 cased line**, **#89 akpost**
with no chromatic aberration here, **#2 grain**.

### 8. Data in art mapping
The ribbon spans exactly minus 5 to minus 15 Celsius on its own printed
temperature scale (C07), declared in `window.__akScale` with `from`, `to`, `band`
and every mark inside the band enumerated with its meaning. Crystals are
generated ONLY inside the window and the population density is zero outside it,
so the activation window is drawn as a fact about where marks exist rather than
as a coloured stripe.

The freezing level rule sits at **y 739**, from 1,874 m through the deck's column
constant (C08). `window.__akAssert` declares
`{what: "1,874 m drawn on the deck column", expect: 739, actual: COL.y(1874),
tol: 1, unit: "px"}` so the derivation survives the next edit.

### 9. Palette assignment
bg `#050A12`, medium `#0B1725`, ribbon `#A9C4DA` with the swell reading against
`#17293C`, crystals `#F4F8FF` at the top 4 percent of the population and
`#A9C4DA` below, freezing rule `#F4F8FF` at `--w-bold`, index chevron `#FFC72C`,
headline `#F4F8FF`.

### 10. Type spec
Headline Instrument Serif 400, fitted 76 to 92px, maxLines 2. Body JetBrains Mono
300, 33px. The two temperatures set as tabular figures in JetBrains Mono 700 at
44px within the headline. Labels 26px.

### 11. Anchor spec
The anchor is the freezing level rule as a real, measured, drawn horizontal at
its true column position, with the altimeter tape as the annotation system.
Weights, ribbon at variable taper, freezing rule at `--w-bold` 3.5px, dimension
lines at `--w-fine`, tape minor ticks at `--w-hair`.

### 12. Reference intent
A thermodynamic diagram that has been rained on.

### 13. Risk flags
- The temperature scale and the altitude scale are two different scales on one
  frame. A guard line prints `TWO SCALES ON THIS FRAME, NOT ONE SUM` and each
  carries its own printed scale bar.
- Crystals must not read as decorative snow. They exist only inside the window,
  which is the claim.

### 14. Acceptance checklist
- [ ] Zero crystal marks exist outside the minus 5 to minus 15 band.
- [ ] The freezing rule sits at y 739 plus or minus 1px.
- [ ] `__akAssert` passes on the 1,874 m derivation.
- [ ] Both scales carry their own printed scale bar and the guard line is present.
- [ ] The index chevron is gold and at y 739, having moved from slide 03.
- [ ] Every mark in the declared temperature band has a meaning.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 05, BREATHER

### 1. Beat
BREATHER. The deck needs a rest here because slides 03 and 04 are both dense
data frames and slides 06 and 07 are the two hardest frames in the deck. A
reader who arrives at the section already tired will not read the void. This
slide is also where Alaska enters as a place rather than as a coordinate, which
the room identified as the treatment's weakest point. Inherits the question of
what was watching. Plants the question directly.

### 2. Copy, final

- Headline, Instrument Serif, fitted 84 to 104px, 3 lines:
  `A low in the Gulf.` / `Northeasterly flow.` / `Nobody watching.` (54 chars)
- Corner readout, JetBrains Mono 300, 26px:
  `CHUGACH AND KENAI COASTAL RANGES (C20)` (38 chars)
- Corner readout, JetBrains Mono 300, 26px: `60 33 N, 151 15 W`
- Counter: `05 / 09`

Body copy is deliberately absent. This is the rest beat and the frame carries
three short lines and two readouts, which is under the 25 to 50 word floor by
design and is why `data-breather` is declared.

### 3. Reader takeaway
This happened over real country, at night, with no one from Alaska present.

### 4. Layout map
Headline columns 1 to 6, rows 5 to 7, sitting LOW in the frame against the
deck's habit, because the composition's mass is the sky above it. The ridge
silhouettes run across columns 1 to 12, rows 6 to 8. Flow streaks fill rows 1 to
5. Focal point is the gap between two ridges at (410, 980). Eye path is the flow
field, then down to the ridges, then the headline. Quiet zone is rows 3 to 4
across the full width, about 20 percent, and it is NOT the bottom band.

4a. **Lower-third treatment.**
BREATHER, and the deck needs a rest here because 03 and 04 are both dense data
frames and 06 and 07 are the two hardest frames in the deck, so a reader arriving
at the section tired will not read the void that carries the whole turn. The band
still carries modeled tone and is not left empty. It holds the Kenai and Chugach
ridge silhouettes drawn from committed geodata as three overlapping planes at
atmospheric perspective, each lerped toward the sky hue by `(i/n)^1.4` and
desaturated by `1 - 0.6*i/n`, with a spruce toned foreground plane in `#16352C`
closest to camera and a graded valley haze pooling between the ranges. The
stipple field continues at density 0.66 through the whole band. `data-breather`
is set on the slide body, which demotes the frame balance gate to a warning, but
the band is composed rather than left over and would clear the gate anyway.

### 5. Depth plan
Background, flow field, three ridge planes at 0.72^i scale with atmospheric lerp,
valley haze, spruce foreground plane, DOM type, grain. Five cues, atmospheric
perspective across the ridge planes, occlusion between them, scale gradient,
depth of field with the middle ridge sharp and the foreground plane blurred, and
exp2 fog in `#0B1725`. Focal plane is the middle ridge.

### 6. Continuity device state
Tape reduced to a hairline ghost with no ticks and the index at 20 percent. No
printed altitude. The record pauses. No void, no edge tease. The device rests,
which is itself a state change and is legible as one because the tape's SHAPE
changes rather than its brightness alone.

### 7. Technique stack
**#9 streamline field** for the flow. Hobbs flow field, angle grid
`= fbm(x * 0.0016) * 2.2 * PI`, grid extended 50 percent beyond canvas, long
curves stepped at 0.3 percent of width, collision spaced via an occupancy grid at
7px cells, tapered width fat in the middle. Mean direction 225 degrees so the lay
runs with the northeasterly flow the report names (C02).
**AKSTIPPLE.field** for the medium at count 11000, density 0.66 through the band.
**#90 akcolor** `AKC.ramp` for the ridge planes, and `AKC.mixOklab` for the haze.
**#89 akpost** with chromatic aberration permitted here, **#2 grain**.
Committed geodata, `assets/geo/alaska-boroughs.geo.json` for the coastal profile
under the canonical projection.

### 8. Data in art mapping
The flow field's mean direction is 225 degrees, from the northeasterly flow the
validation report names (C02). The ridge profile is the real Kenai and Chugach
coastal geometry the company gave as its reason for choosing the region (C20).
No quantity is encoded in the relief, per doctrine, because relief is form
shading and a breather should not ask the reader to read a magnitude.

### 9. Palette assignment
bg `#050A12`, sky medium `#0B1725` to `#17293C`, ridge planes lerping `#27405A`
to `#0B1725` with distance, spruce foreground `#16352C`, valley haze `#17293C`,
flow streaks `#A9C4DA` at 40 percent, headline `#F4F8FF`, tape ghost `#A9C4DA` at
20 percent. No red anywhere. The flare is gone and the palette arc has completed
its cooling.

### 10. Type spec
Headline Instrument Serif 400, fitted 84 to 104px, maxLines 3, leading 1.04,
tracking -1 percent, `#F4F8FF`. Two corner readouts JetBrains Mono 300, 26px,
`#A9C4DA` at 70 percent. Counter 27px.

### 11. Anchor spec
The literal anchor is the real coastal ridge profile of the Kenai and Chugach
ranges from committed geodata. The annotation is the coordinate readout. Two
anchors, at the maximum.

### 12. Reference intent
A plate from a coastal pilot book, at night, with the wind drawn on it.

### 13. Risk flags
- A breather can become an empty slide. Mitigated by the ridge planes and the
  flow field carrying real texture across the whole frame.
- Three ridge planes risk reading as flat cutouts. Mitigated by the atmospheric
  lerp and desaturation per plane, and by the stipple continuing through them.

### 14. Acceptance checklist
- [ ] `data-breather` is set on the slide body and the dossier declares it.
- [ ] The ridge profile is real geodata under the canonical projection.
- [ ] Three ridge planes are distinguishable by value at 432px.
- [ ] No red pixel appears anywhere on the slide.
- [ ] The tape's shape has changed, not merely its brightness.
- [ ] The quiet zone is rows 3 to 4 and is not the bottom band.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 06, THE SECTION (HERO)

### 1. Beat
The hero and the deck's turn. Draw the night's atmosphere to scale and show where
the instrument stops. Inherits the question of what was watching. Plants the
question of what the number is actually made of.

### 2. Copy, final

- Kicker: `WHAT AN INSTRUMENT COULD SEE` (28 chars)
- Headline, Instrument Serif, fitted 84 to 108px, 2 lines:
  `The radar looks` / `from 1,800 metres up.` (36 chars)
- Body, JetBrains Mono 300, 33px:
  `Flares burned between 3,500 and 4,200 metres. The lowest radar beam sits near 1,800 to 2,200 metres. The company says its range does not cover what happens to precipitation below that beam.` (186 chars, 31 words) (C15, C18)
- Void label, JetBrains Mono 500, 26px:
  `THE BAND DOES NOT COVER THIS AIR (C15)` (38 chars)
- Altitude labels, JetBrains Mono 500, 26px: `4,200 m` `3,500 m` `2,200 m`
  `1,874 m` `1,800 m` `0 m`
- Surface line, JetBrains Mono 300, 26px:
  `SURFACE = VERTICAL SECTION, 0 TO 4,300 m (C08, C15, C18)` (55 chars)
- Radar label, JetBrains Mono 500, 26px: `PAHG NEXRAD (C10)` (17 chars)
- Counter: `06 / 09`

### 3. Reader takeaway
There are 1,800 metres of air between the ground and the lowest thing the radar
can see, and the rainfall figure is about water that crossed it.

### 4. Layout map
This slide takes the deck's single permitted grid violation, running the column
from y 90 to y 1240 straight through the bottom margin band, because the section
must reach the ground or the argument does not close. Headline columns 1 to 6,
rows 1 to 2. The column occupies columns 4 to 10 full height. Altitude labels and
dimension calls run in columns 1 to 3. Focal point is the void's upper boundary
at the beam floor, (540, 759). Eye path is headline, release band, down the
column, into the void. Quiet zone columns 1 to 3, rows 1 to 2, about 15 percent.

4a. **Lower-third treatment.**
The bottom band is the slide's subject. The dithered void occupies from the beam
floor at y 759 down to y 1240, which is 481px, and it is closed underneath by an
inked ground profile drawn from the real Kenai coastal geometry, which is what
makes it read as a void rather than as unfinished art. The void's interior
carries an ordered Bayer dither decaying toward the ground so the region has
genuine per mark texture and a value gradient rather than being a flat hole, and
its upper and lower boundaries are both phantom dashed and dimension called with
leaders and a printed 1,800 m value. Beneath the ground profile a graded spruce
toned foreground plane in `#16352C` closes the last 60px. The band therefore
carries modeled tone, a real anchor, a dither texture and the annotation
furniture that names the deck's central claim, all inside the frame's most
important region.

### 5. Depth plan
Background, medium, the aksdf cloud mass occupying y 90 to about y 560, the four
named altitude rules, the radar beam sheet, the dither void, the ground profile,
the spruce foreground plane, DOM type, grain. Five cues, atmospheric perspective
into the mass, occlusion where the beam sheet crosses the column edge, scale
gradient in the dither's cell size with depth, depth of field with the column
face sharp, and fog. Focal plane is the column face.

Camera B for aksdf, the same cached mass as slide 01 viewed from outside and
below, which gives the deck a real camera move for the cost of one extra raymarch
and halves the render budget.

### 6. Continuity device state
The tape BECOMES the slide. Full column 0 to 4,300 m at true scale with all four
altitudes dimension called. Index chevron gold at 1,874 m, y 739. Ink is the
cloud mass, the four rules and the ground profile. Void is the 1,800 m under the
lowest beam, the deck's largest. Edge tease, a dimension extension runs off the
right margin.

### 7. Technique stack
**#88 aksdf** camera B, same seed `20260827`, same cached mass as slide 01.
**#93 akengrave** for the column's modelled tone beneath the mass,
`light {azDeg 62, elDeg 24}`, low raking key because elevation 20 to 30 spreads
`ndotl` across its range and makes the swell legible, `crossDeg 41`, `step 3`,
`wMax 3.2`. **LOW `tone` MEANS DARK.** `form` precomputed into a 4px lookup grid
with a bilinear sampler. A LIT GROUND IS LAID FIRST and any cast shadow goes in
AFTER `eng.surface`, or the lay paints over it and it samples brighter than the
ground it is supposed to darken.
**#17 dither decay** in the void, ordered Bayer 4x4, quantisation decaying toward
the ground.
**#73 dimension call** on all four altitudes and on the void's 1,800 m height.
**#67 dash kit**, **#68 pathLength symmetry**, **#72 leader discipline**,
**#79 cased line**, **#83 title block**, **#84 corner readouts**,
**#89 akpost** with chromatic aberration permitted, **#2 grain**.

### 8. Data in art mapping
Every altitude on this slide is placed by the deck's column constant and the
arithmetic is shown so a critic can measure it in the PNG. 3.7391 metres per
pixel. Release band 3,500 to 4,200 m at y 304 to y 117 (C18). Beam floor 1,800 to
2,200 m at y 759 to y 652 (C15). Freezing level 1,874 m at y 739 (C08). Ground
0 m at y 1240.

The void's height is the blind zone. 1,800 m in column units is **481px**, and it
is the region between the ground and the lowest radar beam.
`window.__akAssert` declares
`{what: "the 1,800 m blind zone drawn as a 481 px void", expect: 481,
actual: COL.y(0) - COL.y(1800), tol: 2, unit: "px"}`.

`window.__akScale` declares the altitude axis with `from: [1240, 0]`,
`to: [90, 4300]`, unit metres, the band it owns, and every mark inside that band
enumerated with its meaning. There is no decorative tick on a measured axis.

`window.__akMotifs` declares the void rect so the engine reads it back out of the
canvas and fails if it is buried or flat.

### 9. Palette assignment
bg `#050A12`, cloud mass `#0B1725` to `#27405A` with the aksdf two tone ramp warm
key `#B9CBD6` and cool shadow `#1A3247`, engraved column `#A9C4DA`, the four
altitude rules `#F4F8FF` at `--w-bold`, radar beam sheet `#5AC8F0` at 2px, void
interior `#050A12` with Bayer dither in `#0B1725`, phantom edges `#A9C4DA` at 45
percent, ground profile `#F4F8FF` at `--w-hero`, spruce foreground `#16352C`,
index chevron `#FFC72C`, headline `#F4F8FF`.

### 10. Type spec
Headline Instrument Serif 400, fitted 84 to 108px, maxLines 2, leading 1.02.
Body JetBrains Mono 300, 33px, max width 660px. Altitude labels JetBrains Mono
500, 26px, tabular. Void label JetBrains Mono 500, 26px, uppercase, sitting on a
hatch knockout window.

### 11. Anchor spec
Two anchors. The column itself as a real sounding section, and the ground profile
as real Kenai coastal geometry. Annotation furniture is four dimension calls,
the altitude axis, the leaders and the title block.

### 11a. Wordless claim
The region the radar never saw is larger than the region it did. Regions, void
`[380, 800, 320, 380]` versus the beam-to-cloud region `[380, 380, 320, 240]`,
`reads: "differ"`. **Measure both off the render, never off the column
arithmetic.**

### 12. Reference intent
A sounding plate from an atmospheric science paper, engraved rather than
plotted.

### 13. Risk flags
- Void reading as unfinished art at 432px. Mitigated by the phantom dashed
  boundaries top and bottom, the interior dither so it has texture rather than
  being flat, the printed label, and an inked ground closing it underneath.
- akengrave polarity. LOW tone means dark. Inverting it inverts the whole detail
  budget and the mistake is invisible until the render.
- akengrave performance. `normalAt` calls `form` four times per sample. The 4px
  lookup grid is mandatory, not optional.
- No object on this slide stands on a surface. The cloud mass is suspended, the
  altitude rules are drawn instrument marks and the ground profile is terrain
  rather than a plinth, so the slide declares no `data-contacts` and there is
  nothing here for that gate to measure. Anything that later grows a base on
  this frame has to add the declaration before it is drawn.

### 14. Acceptance checklist
- [ ] All six altitude labels sit within 1px of their column constant positions.
- [ ] `__akAssert` passes on the 481px void height.
- [ ] The void carries visible dither texture and is not a flat fill.
- [ ] The void is closed underneath by an inked ground profile.
- [ ] The radar beam sheet is exactly 2px and appears once.
- [ ] `__akMotifs` reports the void rect present and not flat.
- [ ] Nothing on the frame stands on a surface, so no `data-contacts` is present.
- [ ] The grid violation is the column only; nothing else breaks the margin.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 07, THREE WIDTHS (KEEPABLE DATA SLIDE)

### 1. Beat
The data slide and the thesis in one keepable frame. Inherits the question of
what the number is made of. Plants the question of what the public record holds.

### 2. Copy, final

- Kicker: `ONE FIGURE, THREE WIDTHS` (24 chars)
- Headline, Instrument Serif, fitted 76 to 96px, 2 lines:
  `Every retelling was narrower` / `than the one before.` (48 chars)
- Row 1 label, JetBrains Mono 500, 27px:
  `THE TECHNICAL REPORT, 41.70 TO 89.35 ACRE FEET (C14)` (51 chars)
- Row 2 label: `THE SUMMARY POST, 45 TO 65 ACRE FEET (C17)` (41 chars)
- Row 3 label: `THE HEADLINE, ABOUT 19 MILLION GALLONS (C16, C38)` (48 chars)
- Note, JetBrains Mono 300, 26px:
  `THE FIRST TWO WERE PUBLISHED THE SAME DAY, BY THE SAME COMPANY (C14, C16)` (72 chars)
- Method line, JetBrains Mono 300, 26px:
  `THE BACKGROUND WAS NOT OBSERVED. 5 dBZ WAS SUBTRACTED FROM EVERY GATE (C11)` (74 chars)
- Ensemble line, JetBrains Mono 300, 26px:
  `THE SPREAD IS 27 REFLECTIVITY RELATIONSHIPS (C12)` (48 chars)
- Verb line, Instrument Serif italic 400, 40px, the deck's only italic:
  `The report says estimates.` (26 chars) (C13)
- Counter: `07 / 09`

### 3. Reader takeaway
The company published a range that spans a factor of 2.14, and the number that
travelled has no width at all.

### 4. Layout map
Headline columns 1 to 8, rows 1 to 2. Three band rows stacked at rows 4, 5 and 6,
all on the shared acre foot axis, left edges at their true x. Row labels sit
above each band, right aligned to the band's left wall. The method and ensemble
lines run in columns 1 to 6, row 8. Focal point is row 3's zero width mark at
(399.7, 780). Eye path is headline, row 1's full width, down the descending
stair to the point. Quiet zone columns 9 to 12, rows 1 to 3, about 16 percent,
placed RIGHT rather than in the bottom band.

4a. **Lower-third treatment.**
The bottom band carries the acre foot axis as a real measured scale with its
ticks, its labels and its printed constant, drawn over a graded ground of the
medium's stipple field at density 0.58 so the axis sits in modeled atmosphere
rather than on bare paper. Beneath the axis the method and ensemble lines sit on
hatch knockout windows cut into an engraved surface whose lay wraps a shallow
plateau form, giving swelled per stroke texture across the whole band. The
27 reflectivity relationships are drawn as 27 fine engraved curves fanning
through the lower band and converging on the mean tick, so the band literally
contains the mechanism that produced the spread above it, and a foreground haze
plane in `#0B1725` grades across the lowest 70px. This is the densest annotation
region in the deck and it is composed, not left over.

### 5. Depth plan
Background, medium at 0.58, the engraved lower surface, the 27 ensemble curves,
the three bands, the axis, DOM type, grain. Four cues, atmospheric perspective in
the curve fan, occlusion where bands overlap the curves, a scale gradient in the
curve weights, and a foreground haze plane. Focal plane is the band rows.

### 6. Continuity device state
The altimeter tape ROTATES FLAT and becomes the acre foot axis, which is the
deck's strongest single motif move and the moment the vertical story becomes a
horizontal one. Index at 0 m. Rows 1 and 2 are voids, phantom edged. Row 3 has no
width at all and is therefore a single ink mark rather than a void, which is the
argument. Edge tease, the stair's implied fourth row is cut off bottom right.

### 7. Technique stack
**#93 akengrave** for the lower surface, same light and polarity as slide 06.
**AKSTIPPLE.field** for the medium at count 7500.
**#67 phantom dash** on the two void bands, **#68 pathLength symmetry** so both
ends of every dashed wall land on full dashes.
**#29 big number tile** for the 2.14 figure, one huge tabular figure with a unit,
a one line context and a hairline rule, Swiss placed.
**#73 dimension call** on each band's width.
**#72 leader discipline** from the verb line to row 1's wall.
**#75 knockout windows**, **#79 cased line**, **#83 title block**,
**#89 akpost** with NO chromatic aberration on a data frame, **#2 grain**.

### 8. Data in art mapping
Everything on this slide is at true scale on one declared axis.
`window.__akScale` declares it with `from: [120, 35]`, `to: [1000, 108.33]`, unit
acre feet, the band each row owns, and every mark enumerated with its meaning.

Row 1, 41.70 to 89.35 acre feet (C14), x 200.4 to x 772.2, width **571.8px**.
Row 2, 45 to 65 acre feet (C17), x 240.0 to x 480.0, width **240.0px**.
Row 3, about 19 million gallons which is 58.31 acre feet (C16, studio arithmetic
from two cited figures), a single mark at x 399.7, width **0px**.
The mean of 57.62 (C14) is ticked at x 391.4, so the round figure sits 8.3px to
the right of the company's own mean and the deck prints that honest detail.

The 27 ensemble curves are exactly 27 (C12) and their landing points are drawn
from a seeded distribution whose 5th and 95th order statistics are pinned to
200.4 and 772.2 and whose mean is pinned to 391.4, so the band above is literally
the envelope of the marks below rather than a shape drawn beside them.

`window.__akAssert` declares `{what: "row 1 drawn at 571.8 px", expect: 571.8,
actual: AX.x(89.35) - AX.x(41.70), tol: 1, unit: "px"}`.

### 9. Palette assignment
bg `#050A12`, medium `#0B1725`, engraved lower surface `#A9C4DA`, band walls
`#F4F8FF` at `--w-hero` 5.5px, void interiors `#050A12` with phantom edges in
`#A9C4DA` at 45 percent, row 3's single mark in `#F4F8FF`, ensemble curves
`#A9C4DA` at 35 percent at `--w-hair`, axis `#F4F8FF` at `--w-std`, headline
`#F4F8FF`, italic verb line `#A9C4DA`.

**No gold on this slide except the index chevron on the axis.** The temptation to
gild the 19 million gallon mark is refused, because gold means camera position in
this deck and nothing else, and a second meaning would break the one device the
reader has learned.

### 10. Type spec
Headline Instrument Serif 400, fitted 76 to 96px, maxLines 2. Row labels
JetBrains Mono 500, 27px, uppercase, +10 percent tracking. Figures JetBrains Mono
700, 44px, tabular lining. The 2.14 big number tile JetBrains Mono 700 at 88px.
Verb line Instrument Serif italic 400, 40px, the deck's only italic.

### 11. Anchor spec
The anchor is the measured axis itself with its printed constant. Annotation
furniture is three dimension calls, the row labels, the leader to the verb line
and the title block. No geographic anchor here, because this frame is about
arithmetic and the deck has spent its geography on 03, 05 and 06.

### 11a. Wordless claim
The published range is wide and the number that travelled is a point. Regions,
row 1 band `[200, 560, 572, 44]` versus row 3 mark `[380, 760, 44, 44]`,
`reads: "differ"`. Measure both off the render.

### 12. Reference intent
An FT or Datawrapper comparison plate, engraved.

### 13. Risk flags
- Three horizontal bands risk reading as one chart. Mitigated because each row
  has a different STATE, void, void and point, and because the 27 curve fan
  changes the frame's texture entirely from any other slide.
- A zero width row could read as a missing row. Mitigated by drawing it as a
  deliberate ink mark with a dimension call reading 0 and a label.
- The gallon conversion is the studio's arithmetic and must be labelled as such
  on the slide, not presented as the company's figure.

### 14. Acceptance checklist
- [ ] Row 1 measures 571.8px plus or minus 1px and `__akAssert` passes.
- [ ] Row 2 measures 240.0px plus or minus 1px.
- [ ] Row 3 has zero width and carries a printed 0 dimension.
- [ ] Exactly 27 ensemble curves, countable at full size.
- [ ] The mean tick at x 391.4 and the 19 million gallon mark at x 399.7 are both present and distinct.
- [ ] Every mark inside the declared axis band carries a meaning.
- [ ] The gallon conversion is labelled as the studio's arithmetic.
- [ ] No gold appears except the index chevron.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 08, THE RECORD

### 1. Beat
The honesty beat and the deck's ethical spine. Say exactly what was checked and
exactly what came back, and refuse to fill the blank. Inherits the question of
what the public record holds. Plants the close.

### 2. Copy, final

- Kicker: `WHAT WAS CHECKED, AND WHAT CAME BACK` (36 chars)
- Headline, Instrument Serif, fitted 76 to 96px, 2 lines:
  `A gap in the record` / `is not a finding.` (36 chars)
- Body, JetBrains Mono 300, 33px:
  `FAA docket FAA-2025-1630 is open and no decision has been published in the Federal Register. NOAA requires a report ten days before any weather modification. Its project list would not load.` (187 chars, 31 words) (C30, C32, C33, C34)
- Row labels, JetBrains Mono 500, 26px, six rows:
  - `FAA PETITION, PUBLISHED JULY 29TH, 2025 (C30)` INK
  - `A DECISION ON IT, NOT IN THE FEDERAL REGISTER (C32)` VOID
  - `NOAA REPORTING RULE, TEN DAYS PRIOR (C33)` INK
  - `NOAA PROJECT LIST, WOULD NOT LOAD (C34)` VOID
  - `ALASKA STATUTES TITLE 46, NO WEATHER MODIFICATION CHAPTER (C35)` INK
  - `FOUR ALASKA OUTLETS SEARCHED, NOTHING FOUND (C37)` VOID
- Refusal line, JetBrains Mono 500, 27px:
  `UNREADABLE IS NOT EMPTY` (23 chars)
- Counter: `08 / 09`

### 3. Reader takeaway
Four things are on the record and three came back empty, and the empty ones
prove nothing except that they are empty.

### 4. Layout map
Headline columns 1 to 7, rows 1 to 2. Six ledger rows stacked in columns 1 to 11,
rows 3 to 7, alternating ink and void. The refusal line sits alone in columns 1
to 6, row 8, at the largest label size in the deck. Focal point is the refusal
line at (300, 1120). Eye path is headline, down the alternating rows, then the
refusal. Quiet zone columns 8 to 12, rows 1 to 2, about 15 percent.

4a. **Lower-third treatment.**
The bottom band carries the refusal line set on an engraved paper tooth surface
whose lay wraps a shallow plateau, so the most important sentence in the deck
sits on genuine swelled per stroke texture rather than on a plate. The last two
ledger rows run down into the band, one ink and one void, and the void's phantom
edge and its leader line cross the band's full width. The stipple field continues
beneath at density 0.52 with a graded ground haze in `#0B1725` closing the lowest
80px, and the altimeter tape, drawn entirely as phantom dash on this slide,
descends through the band with its index chevron migrating onto the sourced
plate. The band therefore carries a modelled engraved surface, a void with its
annotation furniture, a graded haze and the deck's gold mark in its final
position before the close.

### 5. Depth plan
Background, medium at 0.52, the engraved ledger surface, the six rows, the
phantom tape, DOM type, grain. Four cues, atmospheric perspective behind the
ledger, occlusion where the void rows cut the engraved lay, scale gradient in the
row weights, and a foreground haze plane. Focal plane is the ledger surface.

### 6. Continuity device state
Tape drawn entirely as phantom dash with no ticks, which is the record that could
not be read, and the index chevron migrates onto the sourced plate. Same glyph,
new home. Ink rows are engraved, void rows are holes with phantom edges and mono
labels. Edge tease, the ledger's rule runs off the right margin.

### 7. Technique stack
**#93 akengrave** for the ledger surface and the ink rows, same light and
polarity as 06 and 07. **#58e source provenance evidence tags**, solid plate for
SOURCED and phantom plate for NOT CHECKED, which is the committed pattern for
exactly this beat.
**#63 seeded hachure fill** for the ink rows' interior, minus 41 degrees, gap 4x
stroke width, weight 0.5x, jittered ends, seeded per row index.
**#17 dither decay** inside each void row so a void has texture and cannot read
as unfinished.
**AKSTIPPLE.field** for the medium at count 7000.
**#67 dash kit**, **#72 leader discipline**, **#75 knockout windows** so no
numeral sits on hachure, **#79 cased line**, **#83 title block**,
**#89 akpost** with no chromatic aberration, **#2 grain**.

### 8. Data in art mapping
Row texture IS what came back. Three hachured ink rows for C30, C33 and C35.
Three dithered void rows for C32, C34 and C37. The ratio of ink row area to void
row area is 1 to 1 by construction, because three of the six things checked
returned something and three did not, and that is a fact about the search rather
than about the operation.

C35's row is the honest edge case and it is drawn as one. Its left portion is
hachured for the Title 46 chapter list that WAS read, and its right portion is a
void for the four legal sources that returned 403, split by a phantom rule with
both portions labelled.

### 9. Palette assignment
bg `#050A12`, medium `#0B1725`, engraved ledger `#A9C4DA`, ink row hachure
`#C9CFD6`, void interiors `#050A12` with Bayer dither in `#0B1725` and phantom
edges in `#A9C4DA` at 45 percent, refusal line `#F4F8FF`, index chevron
`#FFC72C`, headline `#F4F8FF`.

### 10. Type spec
Headline Instrument Serif 400, fitted 76 to 96px, maxLines 2. Body JetBrains Mono
300, 33px. Row labels JetBrains Mono 500, 26px, uppercase. Refusal line JetBrains
Mono 500, 27px, uppercase, +12 percent tracking, the largest mono on the slide.

### 11. Anchor spec
The anchor is the ledger itself as a drafted evidence table with a title block.
Annotation furniture is six leaders, the split rule on C35's row, and the
provenance tags.

### 12. Reference intent
An evidence schedule from a filing, engraved, with three rows deliberately
empty.

### 13. Risk flags
- **The deck's single largest editorial risk lives on this slide.** A void row
  could read as an accusation. Mitigated three ways, by the headline stating the
  refusal before the rows are read, by every void row carrying a label naming
  exactly what was checked, and by the refusal line sitting at the largest mono
  size in the deck at the end of the eye path.
- The deck must never say Rainmaker failed to file. It says NOAA's list would not
  load and that its last update stamp predates the operation.
- The deck must never say Alaska has no weather modification law. It says Title
  46 carries no weather modification chapter and names the four sources that
  refused.

### 14. Acceptance checklist
- [ ] Exactly six rows, three ink and three void.
- [ ] Every void row carries a mono label naming what was checked.
- [ ] C35's row is visibly split, hachured left and void right, both labelled.
- [ ] The refusal line is the largest mono string in the deck.
- [ ] No string on this slide asserts a failure to file or an absence of law.
- [ ] Void rows carry dither texture and are not flat.
- [ ] The tape is entirely phantom dashed and the chevron sits on the sourced plate.
- [ ] Every visible string is 26px or larger.

---

## SLIDE 09, CLOSE

### 1. Beat
Resolve. One ask, the brand fixture, and the column sealed. Inherits everything.
Plants nothing.

### 2. Copy, final

- Headline, Instrument Serif, fitted 76 to 96px, 2 lines:
  `Two documents.` / `Read the one with the band in it.` (47 chars)
- Ask, JetBrains Mono 500, 36px:
  `Save this, and ask the next water number for its range.` (54 chars)
- Source note, JetBrains Mono 300, 27px: `Sources in comments` (19 chars)
- Wordmark, Instrument Serif 400, 54px: `ALASKA.AI`
- Site fixture, JetBrains Mono 300, 27px: `alaskaaihq.com`
- Counter, sitting on the 0 m tick: `09 / 09`

One ask only. Not stacked. The site fixture is a fixture and not the ask.

### 3. Reader takeaway
Next time a round number arrives, go and find the document with the range in it.

### 4. Layout map
Headline columns 1 to 8, rows 3 to 4. The ask sits in columns 1 to 8, row 6. The
wordmark, Polaris and site fixture group bottom left, columns 1 to 4, row 8.
Focal point is the Polaris at (300, 1120). Eye path is headline, ask, wordmark.
Quiet zone columns 9 to 12, rows 1 to 5, about 22 percent.

4a. **Lower-third treatment.**
The bottom band carries the column's base resolving into the real Kenai ground
profile from committed geodata, drawn at hero stroke weight, with a graded spruce
toned foreground plane in `#16352C` beneath it and the medium's stipple field
continuing at density 0.60 above it, so the band holds a real anchor inside
modeled atmosphere. The altimeter tape's collapse happens here, its index chevron
resolving into the gold Polaris beside the wordmark, so the deck's continuity
device completes inside the band rather than above it. A graded ground haze in
`#0B1725` pools between the ground profile and the foreground plane and the last
altitude tick, 0 m, is dimension called into it, giving annotation furniture with
modeled tone at the frame's close.

### 5. Depth plan
Background, medium at 0.60, the ground profile, the spruce foreground plane, the
brand group, DOM type, grain. Four cues, atmospheric perspective in the medium,
occlusion where the foreground plane crosses the ground profile, scale gradient
in the stipple, and a graded haze pool. Focal plane is the ground profile.

### 6. Continuity device state
The tape collapses and the index chevron resolves into the gold Polaris at the
column's base. This is the deck's last gold and it is the same glyph the reader
has followed for nine frames, arriving home at 0 m. No void. Sealed. No edge
tease, because the deck is closing.

### 7. Technique stack
**AKSTIPPLE.field** at count 9000. **#90 akcolor** for the haze pool.
Committed geodata for the ground profile. **#89 akpost**, **#2 grain**.
Deliberately the lightest technique stack in the deck, because a close should
rest and because the brand group must read cleanly at 432px.

### 8. Data in art mapping
The ground profile is real Kenai coastal geometry under the canonical projection.
The Polaris sits at the column's 0 m tick, which is y 1240 by the deck's column
constant, so the continuity device's resolution is at a true coordinate rather
than at a convenient one.

### 9. Palette assignment
bg `#050A12`, medium `#0B1725` to `#17293C`, ground profile `#F4F8FF` at
`--w-hero`, spruce foreground `#16352C`, haze pool `#17293C`, headline and ask
`#F4F8FF`, site fixture `#A9C4DA`, Polaris `#FFC72C`.

### 10. Type spec
Headline Instrument Serif 400, fitted 76 to 96px, maxLines 2. Ask JetBrains Mono
500, 36px. Wordmark Instrument Serif 400, 54px, tracking +2 percent. Site fixture
JetBrains Mono 300, 27px, `#A9C4DA`, set small beside the mark per
CAROUSEL_CRAFT. Source note 27px.

### 11. Anchor spec
The anchor is the Kenai ground profile. The brand fixture group is the wordmark,
the gold Polaris and the site, and it is a fixture rather than an ask.

### 12. Reference intent
The last plate in a report, where the section finally reaches the ground.

### 13. Risk flags
- A close can go flat. Mitigated by the ground profile and the haze pool carrying
  real modeled tone.
- The single ask must not be crowded by the site fixture. They are separated by a
  full row and set at different sizes and colours.

### 14. Acceptance checklist
- [ ] Exactly one ask on the slide.
- [ ] "Sources in comments" is present.
- [ ] `alaskaaihq.com` is small, in the mono face, near the brand mark.
- [ ] The Polaris sits at y 1240, the column's 0 m tick.
- [ ] The ground profile is real geodata.
- [ ] The counter reads 09 / 09.
- [ ] Every visible string is 26px or larger.

---

## BUILD RECONCILIATION

Appended after the first render and after every round that changes an artifact.
Three rounds ran on this deck: nine pixel critics, then the flow critic, then
the scorer. Where the build differs from the dossiers above, the BUILD is right
and the rounds below say why. The deck changed on all nine frames. The largest
single change is slide 06's hero mass, which shipped as a smooth gradient and
now carries shell displacement and a stipple surface read back off its own
raymarch. The largest single correction is slide 07's OUR ARITHMETIC, which was
first person on a slide and is banned outright in brand.yaml.

### Round 1 repairs, 2026-08-27, from the nine pixel critics

Where the build now differs from the dossiers above, the BUILD is right and
these lines say why.

- **Slide 01.** Headline break authored at the sense boundaries rather than
  left to the fitter. Chromatic aberration set to zero, because at 0.6 it split
  the tape's 0.75px hair ticks into per channel lines and put magenta and green
  on a frame whose palette allows one accent.
- **Slide 02.** The altimeter tape was missing and is now drawn. Four labels had
  been shortened past their hedges and are restored, so the software line is
  attributed to the company, El Segundo carries C29, and the ghost lane names the
  same company rather than an anonymous second post. The axis moved to x 200 to
  960 so the lane labels sit inside the margin, and its extension is cut by the
  right edge, which is Device C.
- **Slide 03.** The altimeter tape was missing and is now drawn. The wet area
  void is DERIVED from the borough's own projected area at the published ratio
  and asserted at 0.601 percent, where it had been drawn by eye at about four
  percent and placed in Cook Inlet rather than on land. The interior's ground
  gradient was spruce green, which this deck reserves for slides 05 and 06, and
  is now cold. The headline says the area is modelled. The ratio note reads
  AGAINST and names LAND, because C36 is a land area.
- **Slide 04.** The activation ribbon was drawn BELOW the freezing rule, which
  on a frame carrying an altitude tape reads as the minus 5 to minus 15 layer
  sitting under the 1,874 m freezing level. The ribbon is now above it, the
  crystal population falls from it and stops dead at the rule, the temperature
  scale prints its two endpoints, the closed outline is gone, the marks are
  points rather than snowflake glyphs, and the band below the floor carries the
  medium instead of bare page.
- **Slide 06.** The column moved right to x 760 and bleeds off the frame, which
  is what buys the hero its headline: it had silently fallen to three lines at
  69px and split 1,800 from metres. The rail no longer crosses the kicker. The
  void's dither is lifted and it is closed on all four sides. The blind zone is
  dimensioned in the band that was empty. The release band hatch is cool, because
  from slide 06 onward gold is the only warm thing left. The counter is back at
  the head of the tape it indexes.
- **Slide 07.** The axis prints its own numbers and its unit. The mean rule and
  the zero width row are named. The claim chips moved into their own right hand
  column so no row label wraps, and the labels cleared the dimension line that
  had been running through their descenders. The method line names the 5 dBZ
  subtraction rather than characterising it. Field 11a's data-encodes probe is
  NOT declared: this frame's wordless claim is carried by EXTENT, which a colour
  difference probe cannot see, and the two width assertions check it instead.
- **Slide 08.** Row 5's split is gone. A phantom rule that cut MODIFICATION in
  half and left its void half unlabelled said less than the footnote that
  replaces it. Every row label is one line with its chip in a right hand column,
  centred in its box so no rule runs through the glyphs. Title 46 names Alaska.
  The refusal is set at 44px, the largest mono string in the deck.
- **Slide 09.** Headline break authored. The tape collapses down the right edge
  and along the 0 m datum into the Polaris, so the star is the foot of the
  column rather than a mark beside a wordmark. The terrain runs below the datum,
  never through it. A distant plane sits behind the profile so the crossing is an
  occlusion. The ask is set at headline value.

`python scripts/gate_status.py --run-dir out/2026-08-27 --sync out/2026-08-27/storyboard.md`

### Round 2 repairs, 2026-08-27, from the flow critic

The flow critic scored the sequence 7.3 and found four faults that are
sequence faults rather than frame faults.

- **Slide 02's legend was teaching the wrong key.** It read VOID, NOT IN THE
  RECORD, but the device is INK IS RECORDED, VOID IS MODELED, and slide 03's
  void is a modelled threshold while slide 07's two voids are published ranges.
  All three are in the record. A reader who learned the key on 02 misread the
  thesis frame. It now reads VOID, NOT MEASURED, which is true of every void in
  the deck.
- **Device C was declared on seven junctions and drawn on one.** Slide 01's
  flare drift now runs past the right edge at y 884 and enters slide 02 at the
  same height, so one seam actually aligns.
- **Slide 08 was as heavy as slide 07** where the arc promised a level exhale.
  Its body paragraph restated rows 1 through 4 word for word, so it is one line
  now.
- **Slide 06 printed 1,800 four times.** The body carries only the sentence the
  column cannot draw.

### Round 3 repairs, 2026-08-27, from the scorer

Scored 6.9 against a threshold of 8.3, capped from an honest 8.32 by one hard
fail. A low score is a work order.

- **BLOCKING, now fixed.** Slide 07 rendered OUR ARITHMETIC. brand.yaml bans
  first person on a slide outright, and no gate catches it because
  caption_check enforces first person on the caption only. The line now reads
  58.31 ACRE FEET IS THAT HEADLINE, STUDIO CONVERSION (C16). Logged as a Phase
  12 candidate: the rule is enforced on captions and slides by different code
  paths and only one of them exists.
- **Two unit symbols were being eaten by a CSS uppercase transform**, so an
  instrument register deck printed 1,800 M beside five lowercase m labels and
  5 DBZ where the authored string was 5 dBZ. Both units are wrapped now.
- **Slide 04 drew MINUS 5 above MINUS 15** on a frame carrying an altitude
  tape. Air cools with height, so the scale read backwards against the physics
  whatever the guard line said. The cold edge is the top edge now.
- **The hero was the deck's weakest object.** Slide 06's aksdf mass rendered as
  a smooth gumdrop: the smin blend of six spheres with no displacement, at
  320 by 300, tone mapped to a single gradient. It now carries two octaves of
  shell displacement at 480 by 450, and its surface is a 30,000 mark stipple
  field whose density is read back off the raymarch's own luminance, so the
  hero is drawn in the same language as the other eight frames. Drawn share
  67 percent, up from 66.
- **Slide 07's 27 ensemble curves were a 40px smudge.** The fan launches from
  a common origin inside the engraved plate with about 90px of throw and its
  two extreme curves are drawn at fine weight, so the band above reads as the
  envelope of the marks below.
- **Dead zones on slides 04, 06 and 09** are filled with graded medium rather
  than with a bigger quiet zone.

### Round 4 repairs, 2026-08-27, from the second scoring pass

Scored 8.80 against a threshold of 8.3 with no hard fail, so this round is not
a gate repair. It is the scorer's one-sentence fix for the criterion that is
still the weakest, artwork craft at 6.5, taken because that criterion is the
standing weakness this run set out to attack.

- **The hero's silhouette is dissolved.** A raymarched surface has a hard
  analytic edge, and after round 3 the mass read as an opaque rock rather than
  as cloud. Its edge is now taken apart into the same medium that carries form
  on the other eight frames: 26,000 marks are scattered OUTSIDE the mass with a
  density following a cheap dilation of its own rendered luminance, so the
  boundary is a density gradient and not a line. Its key and material are
  darkened so it is no longer the brightest, most saturated object in a deck
  whose declared atmosphere has no lit surface in nine slides.
- **The blind air continues off the section.** The lower left quadrant was
  black. It now carries the void's own Bayer lay, fading left, so the empty
  region states the frame's argument instead of being answered with a bigger
  quiet zone.
- **copy.json's bodies were stored truncated at 80 characters** on four slides,
  because the rebuild read render_report's `text` field rather than joining its
  `texts` array. copy_sync_check could not catch it, because it asks whether an
  authored string is PRESENT in the render and a truncated string is.

### Round 5 repairs, 2026-08-27, from the third scoring pass

Scored 8.80 again, no hard fail, and named the same weakest criterion. This is
the fifth and last round under the editing cap.

- **The hero stops being shaded at all.** Two rounds of softening the raymarch's
  lighting did not change what the frame WAS, and the third pass found why: the
  surface stipple painted #F4F8FF at up to 0.38 alpha across the lit face while
  the dissolve whispered at the edge. The lit face is now extinguished before a
  single mark is drawn, with a #050A12 scrim at 0.93, and the raymarch survives
  only as a DENSITY FIELD sampled off its own render. No mark on the mass
  exceeds #C6DAE8, and the interior and the dissolve share one colour ladder so
  density falls continuously from the middle out with no step. The hero has no
  lit surface and no analytic silhouette, which is what the deck's declared
  atmosphere promised on every one of its nine frames.
- **copy.json's LABELS were shredded by the same joining bug** that round 4 fixed
  in the bodies: `texts` is per child and DROPS `<span>` children, so a unit
  wrapper cost the label its unit. The rule is now to take `text` unless it was
  truncated at 80 characters and only then fall back to `texts`. Both halves of
  this bug are one Phase 12 candidate: the extractor is in the run, not in the
  engine, and copy_sync_check structurally cannot see either half because a
  shard is still PRESENT in the render.

### Corrections to the dossiers above, from the final scoring pass

The dossiers are the PLAN. Where the shipped render disagrees with one, the
render is what shipped and this is the correction, so nothing archived under
`runs/` asserts something the pixels contradict.

- **Slide 07, field 8.** The dossier says the 27 ensemble curves have their 5th
  and 95th order statistics pinned to the band above them, at x 200.4 and
  x 772.2, with the mean landing on the 391.4 tick. Measured off the shipped
  PNG the fan spans roughly 42 to 77 acre feet and converges near 78. The
  BAND is drawn from the published figures and is correct to 1 px, and both
  width assertions hold; it is the FAN that is not the band's envelope. No
  printed string on the slide claims otherwise, so no reader is misled, but the
  dossier sentence is false and is retired here rather than archived.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-08-27. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[WARN] qa.py          WARN, 0 fails, 13 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 8 line(s), 604 chars
[PASS] caption_check  PASS, 896 chars, hook 122, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 86 authored slide strings all present in the render
[PASS] aggregate      aggregate_check: PASS -- 23 aggregate assertion(s) detected, 23 declared -> out/2026-08-27/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 31 claims indexed, 1 declared counts checked, 0 drift(s)
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.127 (fail at 0.60), max pair 0.290, drawn share 66% (85 drawn vs 44 blocky
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] docket_dates   docket dates clean at 2026-08-27: 285 assertions over 6 fixtures and 22 ledger items
[PASS] gas_watch      22 day(s) on record, 22 verified, no gaps, latest 2026-08-26, EIA through 202605 over 131 months, model misses by 6.82%
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-08-27 (149 generated files)
[PASS] assemble       9 slides, pdf vector 13.52 MB, 9 thumbs
[PASS] score          8.67 / 10 vs threshold 7.7, scorer says passes=True
[PASS] ship_gate      scored 8.67 against a threshold of 7.70
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```

