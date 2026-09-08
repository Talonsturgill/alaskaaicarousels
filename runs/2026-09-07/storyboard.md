# STORYBOARD — Alaska.Ai Carousel No. 53 — 2026-09-07
## THE CURVED TRANSECT

---

# DECK HEADER

## The directors room, and how this was synthesised

Three treatments came back. All three were strong and all three named their own
weakest thing, which made the choice easy rather than hard.

- **THE GAUGE BENCH** (data-journalist). A metrology bench, contracts as machined
  steel bars, the comma as a *burr* on a leading edge. Best single wordless idea
  in the room, "the count is a property of the light, not of the objects." It
  disqualified itself in its own self-critique: **no Alaska in it**, a mono ZIP
  code and some proper nouns, on a rubric that weights Alaska authenticity at 12
  percent. It also flagged its own monotony risk, three slides that are all steel
  bars on lit granite.
- **THE RESET STATION** (historian-of-the-future). Survey monument discs cast in
  bronze and set into Kodiak rock. A genuinely beautiful central metaphor, a
  designation that never changes while the agency name does, and a destroyed
  point that gets RESET. Same Alaska problem, and its scale descent sat close to
  the forbidden RETENTION SHEET, which it admitted.
- **THE CURVED TRANSECT** (cartographer). **WINNER.**

**Why the cartographer wins.** It is the only treatment that carries Alaska
authenticity, and it carries it structurally rather than decoratively. It has
the strongest wordless claim in the room, *length means distance and zero length
means work*. Its geometry is computed rather than eyeballed. And it deletes both
recurring machine defects by construction rather than passing them, because
nothing rests on a surface anywhere except one declared instance, and every
frame's lower band is a lit sphere.

**Organs grafted from the losers, named so the reconciliation can check them.**

1. **From the historian, the renaming beat, and it is the best fact in the
   room.** In 2019 the buyer was the Joint Artificial Intelligence Center. In
   2026 the buyer is the Deputy to the Chief Digital and Artificial Intelligence
   Office. **The offices renamed themselves around a requirement sentence that
   did not change.** That is a historian's observation, it is verified twice
   (C19, C13), and it becomes the spine of slide 05.
2. **From the data-journalist, the printed-query discipline.** Every count on
   every slide is printed beside the exact query that produced it, and labelled
   as what a named query returns rather than as a fact about the world.
3. **From the data-journalist, the phantom-dash epistemic convention** (technique
   67), used on slide 06 to draw the difference between a record whose worksite
   is in the file and one whose worksite is not.

## THESIS

The federal AI money with an Alaska name on it is a 3,362 mile line rather than
a place, and the public's own search for those lines is broken by a comma, so
the only way to see where Alaska AI work actually happens is to stop reading the
vendor address and start drawing the geodesic.

**PDF document title (47 chars):** `Alaska AI Contracts and the Comma That Hides One`

## THE CORRECTIONS THE FACT-CHECKER FORCED, applied before a pixel is drawn

The cartographer's treatment carried five facts the claims package killed or
changed. All five are corrected here, and the reconciliation section repeats
them so no dossier drifts back.

| the treatment said | the record says | where |
|---|---|---|
| origin Woody Island, Leisnoi a subsidiary of the village corporation | **KILLED.** No source states the ownership. Leisnoi, Inc. LISTS Leisnoi Professional among its companies (C53), and the contract holder's own address is Anchorage (C12). | transect origin is **ANCHORAGE**, Kodiak appears only on 07 as where shareholders are |
| Tuknik 140D0419C0047 at $9,479,118.55, a floor | **$21,596,322.25 across 14 actions** (C20) | S05 |
| Settlement Trust $46,013,900 | **KILLED, unverified.** Removed entirely. | S07 |
| dividend January 27th, **2026** | year unverified (C33). Print the day, no year. | S07 |
| ICE, $63M, one year, Adams TN pop 600, Koniag Government Services | **Koniag Services Inc**, **$17,456,917.40 obligated**, **August 6th 2026 to August 5th 2030**, place of performance now **NASHVILLE** (C38, C39, C40, C41) | S08 |

## SLIDE COUNT RATIONALE

**Nine.** The house default, and the right number here. Ten was pitched twice and
both pitchers admitted the tenth slide strained a VISUAL_DENSITY 2 dial. Nine
gives the deck a clean three-act shape, five slides flying southeast, a hard cut
home at 06, and two slides returning. The measured-silence beat (the Fairbanks
moratorium on both 2027 priority lists against zero opinion-page items) is cut
to the caption rather than crowding slide 08, which is a disclosed loss.

## ARC

| # | beat | opens | pays |
|---|---|---|---|
| 01 | COVER. A comma hides an exact figure. | what search, what comma | — |
| 02 | The two queries. 24 and 25, and **nothing in common**. | how can a superset return more | 01 |
| 03 | The comma is the mechanism. Four cases fit. | which contract fell in the gap | 02 |
| 04 | Leisnoi, to the cent, lawful on the face. | how long has this run | 03 |
| 05 | Seven years. One day. **The buyers renamed, the sentence didn't.** | where is any of it performed | 04 |
| 06 | **HARD CUT HOME.** Place of performance. One record, nine records. | if the work is Outside, where does the money land | 05 |
| 07 | **BREATHER, declared.** Kodiak. What comes home and by what route. | what else does the mechanism buy | 06 |
| 08 | The counterweight. Nashville, 102 signatures, a threshold. | what does Alaska AI mean then | 07 |
| 09 | CLOSE. September 10th, 2026. One ask. | — | 08 |

Emotional temperature turns at 06. Five slides of monotonic southeast crawl,
then the camera snaps home and the arc is gone because its length is zero.

## THE GEOMETRY, computed and not eyeballed

Endpoints are the two the record actually gives. Anchorage 99503 is the place of
performance of the one Alaska-performed AI contract (C14) and also the Leisnoi
vendor address (C12). Washington DC 20301 is where the Leisnoi work is performed
(C12).

```
ANCHORAGE   [-149.9003,  61.2181]
PENTAGON    [ -77.0563,  38.8719]

central angle        48.6527 deg
great circle         3,362 statute miles   (5,410 km)
initial bearing      82.28 deg out of Anchorage
back-bearing         322.21 deg arriving Arlington
midpoint             55.6184 N, 103.6097 W   (northern Saskatchewan)
vertex, northernmost 61.5032 N, 141.0823 W   (eastern Alaska border)
half-separation      24.3264 deg ; 2*sin(half) = 0.8239
scale for a 900px span   S = 900 / 0.8239 = 1092 px
```

Globe radius 1092 exceeds the frame's half-diagonal of 864, so **the limb is off
frame on the close slides and the picture is solid Earth**. No fake horizon.

**Roll is solved numerically, never guessed.** d3's `fitExtent` preserves aspect,
so the extent is set on the axis meant:

```js
const P0 = d3.geoOrthographic().rotate([103.61,-55.62,0]).translate([540,675]).scale(S);
const a = P0(ANC), b = P0(PEN);
const gamma = Math.atan2(b[0]-a[0], b[1]-a[1]) * 180/Math.PI;
// rebuild with rotate([103.61,-55.62,gamma]); ASSERT Math.abs(a[0]-b[0]) < 6
```

**Data-honesty rule, deck-wide and absolute.** No quantity is ever encoded as a
length, area or radius drawn on the sphere. Arc length on the sphere is geodesic
distance, a geometric truth, and that is the only measurement the projection
carries. Every dollar figure and every count lives in mono tabular figures or in
one flat cabinet-oblique register drawn OFF the sphere (S05).

## CONTINUITY SYSTEM — four devices

**D1. THE TRANSECT** (camera move plus panorama on a sphere). One geodesic
sampled ONCE at plan time as a 512-point lon/lat list in a shared module. Every
slide projects the same list, so junction misalignment is structurally
impossible. No slide authors its own curve.

**D2. THE GAP** (motif evolution). The arc carries a hard break that changes
state every slide. Full table below.

**D3. THE ALTITUDE RAIL.** Right-edge mono rail, 24px JetBrains Mono tracked
+10%, printing the projection centre's real lat/lon, along-track angular
distance, running great-circle miles, and the progress counter. Every value on
it is measured, so it is a **measured axis** and is declared. It doubles as the
constellation coordinates footer.

**D4. ARC AND TYPE NEVER SHARE A COLUMN.** The projection is translated so the
arc holds one third and primary type holds the opposite third. This is the type
reserve, designed into the composition from the first build rather than defended
with a plate after a gate fails.

### FULL MOTIF STATE TABLE

| # | camera t | S | centre | limb | D2 gap state | arc column | gold, exact |
|---|---|---|---|---|---|---|---|
| 01 | 0.00 | 1092 | 61.2 N 149.9 W | off | one arc leaves Anchorage, **broken**, gap unexplained | left | comma glyph seated in the gap, 28px |
| 02 | 0.10 | 1092 | 61.5 N 143.2 W | off | 25 arcs drawn, **all 25 greyed and broken**, 24 solid beside them | left | the disjointness bracket, 30px |
| 03 | 0.20 | 1040 | 61.4 N 136.4 W | off | one gap enlarged to 120px, **gold comma seated inside it** | left | 4 comma glyphs in the 4 case strings |
| 04 | 0.36 | 940 | 60.2 N 125.1 W | off | the gap **closed**, that arc now solid and labelled at both ends | left | the healed segment, 6px x 210px |
| 05 | 0.52 | 880 | 57.6 N 112.4 W | off | **four arcs stacked**, same origin, same destination | left | the ONE DAY dimension call |
| 06 | **cut to 0.01** | 4200 | 62.0 N 149.5 W | off | **arc length zero.** two marks, no line | none | Polaris on the rail only |
| 07 | 0.00 (Kodiak) | 2200 | 57.5 N 152.2 W | corner | no arc. one ring of return channels | none | Polaris on the rail only |
| 08 | 0.90 | 1000 | 41.0 N 82.1 W | off | the arc returns and **branches** southwest to Nashville | right | Polaris on the rail only |
| 09 | whole arc | 400 | 55.6 N 103.6 W | visible | arc **entire**, end to end, sealed into Polaris at Anchorage | centre | Polaris + wordmark |

Slides 06, 07 and 08 hold gold out as story ink on purpose, so ice blue
`#5AC8F0` owns "work performed here" with no competition on the two slides where
that is the whole argument. Gold still appears on every slide as the fixed
Polaris on the rail, satisfying the constellation requirement without leaking
story meaning.

## ATMOSPHERE

### NEW: TERMINATOR GRAZE, KEY AT AZ 142 / EL 4

- **One light pair, deck-wide, exported as a single constant and passed byte
  identical to every consumer.** The transect's back-bearing at Arlington
  computes to 322.21 degrees, so light arriving down the transect arrives from
  **azimuth 142.21, rounded to 142**. Elevation 4. **The deck is lit from
  Washington.** Alaska is the dark end of every frame and the lit end is the end
  the money is at. That is the thesis before a word is read.
- **Key to fill 6:1.** Key `#C8DCF0`, fill is upper-atmosphere skyglow `#1B3550`
  from the opposite limb plus `AKT.environment` procedural IBL so the ocean gets
  a real reflection instead of a painted sheen.
- **Arc.** 6:1 on 01 to 05. **2.5:1 on 07**, the layer thickens for the breather
  and it is the flattest frame in the deck. 7:1 on 09 as it clears.
- **All cast shadows share one bearing**, screen-left and down-screen, per slide
  in the dossiers.
- **Elevation caveat, checked against the function that consumes it.** Elevation
  4 is the SCENE key. Any `akengrave` region declares its own bench light at **az
  142 / el 24**, same azimuth, because elevation under 15 collapses the swell.
  Load `akcolor.js` before `akengrave.js`, always.

**Divergence.** Not raking light on frozen muskeg (fill dominates and the surface
is water and rock, not organic ground). Not a coaxial read on damp rag. Not a
downwelling key at elevation 76 through particulate, which is the inverse
relationship, since this is a *low* key with the particulate as the fill source.

## PALETTE — TERMINATOR BLUE AND LIMESTONE

Derived from the story's own material world, North Pacific water at night and
Indiana limestone, which is the Pentagon's actual facade stone.

| role | hex | where |
|---|---|---|
| base, deep ocean night | `#050A14` | space and unlit sphere. never pure black |
| elevation 1, sphere in shadow | `#0B1626` | the Alaska end of every frame |
| elevation 2, continent at grazing key | `#16293F` | the lit half, land mass |
| terminator glow, sea specular | `#3E6E96` | the streak, one direction, southeast |
| **limestone** | `#D6D0C2` | ONLY the Arlington point mark and one 34px glyph. never a mass. the single warm neutral, foreign on purpose |
| primary type | `#EAF1FA` | headlines, body |
| secondary type, mono instrument | `#8FA6BE` | rail, labels, legends |
| **ALASKA PERFORMED**, aurora ice | `#5AC8F0` | one meaning only, the zero-length marks at Anchorage and Fairbanks. zero cross-leak |
| accent, Alaska flag gold | `#FFC72C` | the comma and what it hides, plus the fixed Polaris |

Divergence from the last three families: not cold boreal night with one warm
token (the warm here is a *material* holding real area), not peat and mineral (no
organic browns), not diatom green and wet steel (no green at any stop).

**Gold budget.** Under 0.4 percent of frame area on every slide, measured and not
asserted. Placement is in the state table above.

## TYPE SYSTEM

- **Unbounded 700**, display only, 84 to 132px, tracking -2%, max 2 lines,
  `AK.fitText(el,{min,max,maxLines})` always, called after
  `await document.fonts.ready`.
- **Manrope 500** body 34px, leading 1.38, measure 30 to 38 characters.
  **Manrope 700** for the one lead line per slide.
- **JetBrains Mono 400/500**, 24 to 30px, `tabular-nums lining-nums` always,
  tracked +10% for all-caps labels.
- Three sizes per slide, never more. **No serif anywhere in this deck.**

## VARIETY LEDGER CHECK

| axis | last decks | this deck | diverges |
|---|---|---|---|
| hero structure | NIGHT APRON / RULED WORLD / RETENTION SHEET / WATERLINE | **NEW: THE CURVED TRANSECT** | yes, see section 3 of the treatment. no sheet, no document surface, no rising level, no human-scale weather |
| atmosphere | muskeg raking / coaxial damp rag / downwelling el 76 | **NEW: TERMINATOR GRAZE az 142 el 4** | yes, a planetary grazing key with particulate as FILL |
| continuity | PLATE CHAIN + GAUGE / FIVE STRAND SHOT LINE | THE TRANSECT + THE GAP + THE ALTITUDE RAIL + column separation | yes |
| hook archetype | HALF NOBODY IS ARGUING ABOUT / MATCH THAT TAKES 105 / BILL NOBODY HAS PRICED | **NEW: THE MARK THAT HIDES A NUMBER** | yes |
| palette | boreal+token / peat+mineral / diatom+steel | TERMINATOR BLUE AND LIMESTONE | yes |
| type pairing | Fraunces+Space Grotesk+Mono / Instrument Serif+Archivo+Mono | **Unbounded + Manrope + JetBrains Mono** | yes |

**PAPER IS SPENT AND THIS DECK CONTAINS NO SHEET OF ANY KIND.** No page, no form,
no stamp, no printed document object, no card, no plate, no rounded rectangle.

## VARIANCE DIALS

- **DESIGN_VARIANCE 4.** A deck shot entirely from orbit is far from house centre.
  Justified because the story's single hardest fact is a distance.
- **VISUAL_DENSITY 2.** Deliberately sparse against a run of dense decks. The
  argument is that the large thing is QUIET, so very large figures in a nearly
  empty frame is the composition doing the argument rather than decorating it.
- **TYPE_TEMPERATURE 2, cool.** No serif in the deck at all.

## HOW THIS DECK ATTACKS THE STANDING WEAKNESS

`trend_check` names **artwork craft and genuine detail** weakest in 7 of 10 runs,
mean 6.7, last 6.0. Three commitments, made here and not at Phase 9.

1. **The rendered ladder carries the hero.** `akthree` GPU PBR on 01 to 05, 08
   and 09, `aksdf` raymarch on 06. Both were smoke-tested in this container
   before this storyboard was written and both render clean. `setPixelRatio`
   BEFORE `setSize`; `await AKT.snapshot(R)` and check `.ok` on every slide; the
   Canvas fallback is designed per slide, not improvised.
2. **Two recurring defect classes are deleted structurally.** Top-loaded
   composition warned in 6 of 10 runs; here every slide's lower band is a lit
   sphere, a lit limb with atmospheric shell, a cabinet register with cast
   shadows, or a sculpted mass, each named in field 4a. Contact shadows warned in
   5 of 10; **nothing rests on a surface anywhere in this deck except one
   declared instance on slide 06**, so the class does not exist here rather than
   being passed.
3. **The type reserve is a composition rule, not a plate.** D4 puts the arc and
   primary type in opposite columns by construction. There is no scrim, no
   backdrop blur and no plate anywhere in the deck.

## CLAIMS INDEX

| slide | claim ids used |
|---|---|
| 01 | C07 |
| 02 | C01, C02, C03 |
| 03 | C05, C06 |
| 04 | C07, C08, C09, C10, C11, C12 |
| 05 | C19, C20, C21, C22, C23, C13 |
| 06 | C13, C14, C16, C17, C18 |
| 07 | C31, C32, C33, C35, C36, C37 |
| 08 | C38, C39, C40, C41, C42, C43, C54, C55 |
| 09 | C11 |

NOT USED on any slide, carried in the verification record and the first comment
only: C04, C15, C20 (value used, id also on 05), C24, C25, C26, C27, C28, C29,
C30, C44, C45, C46, C47, C49, C50, C51, C52, C53.

ADDED IN PHASE 8, after the pixel round found the defect. C54 and C55 verify the
Bering Straits petition figure that slide 08 was already printing on the strength
of a scout note the first claims pass never turned into a claim. The number stood
up (The Nome Nugget, January 8th, 2026), and verifying it also corrected the
slide: the 102 are shareholders AND descendants, it is an early-December count,
and it excludes 20 non-shareholder signatures. All three now print.

---

# PER-SLIDE DOSSIERS

---

## SLIDE 01 — COVER

**1. BEAT.** Stop the scroll with a number and a punctuation mark in the same
breath. Plants the loop, what search, and what comma. Inherits nothing.

**2. COPY, FINAL.**
- Display line 1, Unbounded 700, 108px, tracking -2%: `A COMMA HIDES` (13 ch)
- Display line 2, JetBrains Mono 500, 112px, tabular: `$20,632,119.41` (14 ch)
- Body, Manrope 500, 34px: `from the public's own search for AI contracts` (44 ch) [C07]
- Rail, mono 24px: `61.2181N 149.9003W . t 0.00 . 0 MI . 01 / 09`
- Provenance strip, mono 24px, `data-decorative`: `FPDS-NG READ 2026-09-07`

Cover word count for the headline proper is 4 plus a figure, well under 12.

**3. READER TAKEAWAY.** A comma is hiding an exact, large number.

**4. LAYOUT MAP.** 12 cols. Arc occupies cols 1 to 5, entering from the Anchorage
coast at the upper left and exiting the top-right edge with a hard 34px break at
roughly y=380. Type block cols 7 to 12, optically left-aligned at x=600, rows 3
to 5. Focal point is the gap at (742, 388), a rule-of-thirds intersection. Eye
path is gap, then figure, then body. Quiet zone is cols 7 to 12, rows 6 to 7,
about 18 percent of the frame, well under the quarter ceiling.

**4a. LOWER-THIRD TREATMENT.** The lit sphere itself. The grazing specular streak
on water runs lower-left to upper-right across the whole band at el 4, with the
terminator gradient rendered in OKLCH and IGN dithered, plus a blurred additive
limb-haze shell mesh below y=1180 as a repoussoir. Modeled tone throughout, no
plate and no hairline furniture.

**5. DEPTH PLAN.** background space `#050A14` -> sphere body via akthree PBR ->
atmospheric shell mesh -> Canvas 2D coastline and graticule -> SVG arc and gap ->
DOM type -> grain tile. Four cues, atmospheric perspective (the terminator ramp),
occlusion (the shell over the limb), scale gradient (graticule convergence), and
depth of field (the near arc sharp, the far coast softened). Focal plane is the
gap. Camera is a `THREE.OrthographicCamera` down -z, frustum `k = S/R` with
S=1092, so the three.js silhouette matches `d3.geoOrthographic().scale(1092)`.

**6. CONTINUITY DEVICE STATE.** D2 gap is present and unexplained, 34px. D3 rail
reads t 0.00. D4 arc left, type right. Edge-tease, the arc is cut by the top
right corner and resumes on 02.

**7. TECHNIQUE STACK.** akthree (#87) sphere, `MeshStandardMaterial` roughness
0.78 metalness 0.04, procedural normal from a seeded canvas bump, one
`DirectionalLight` az 142 el 4, 2048px PCFSoft, ACES, `AKT.environment` IBL.
akcolor (#90) `AKC.ramp('#16293F',{steps:7,keyHue:210,ambientHue:250,drift:0.3})`.
akpost (#89) house grade, IGN dither on, aberration 0.6px permitted here.
`AK.grainTile(280,52,seed 20260907)`. Cased coastline (#79) at 1.25px.
All seeded with `AK.rng(20260907 + 1)`.

**8. DATA-IN-ART MAPPING.** Arc path is the true 512-point geodesic, so its
on-screen length IS 3,362 statute miles at this projection. The gap's along-track
position is the arc's own midpoint. No quantity is encoded by any drawn length.

**9. PALETTE ASSIGNMENT.** bg `#050A14`; sphere shadow `#0B1626`; sphere lit
`#16293F`; specular `#3E6E96`; arc `#8FA6BE` at 2px cased; type `#EAF1FA` on
`#0B1626` measuring 13.9:1; gold `#FFC72C` on the comma glyph only, 28px, about
0.06 percent of frame.

**10. TYPE SPEC.** Line 1 Unbounded 700 108px, leading 0.98, tracking -2%, colour
`#EAF1FA`, max width 420px, fitText min 84 max 116 maxLines 1. Line 2 JetBrains
Mono 500 112px tabular, tracking 0. Body Manrope 500 34px leading 1.38 max width
430px. Rail mono 400 24px tracked +10% `#8FA6BE`.

**11. ANCHOR SPEC.** The literal anchor is the Alaska coastline entering the top
left, drawn from `alaska-state.geo.json` through the same projection, cased at
1.25px. Annotation furniture is the graticule at 50/60/70 N and 150/120 W, hair
weight 0.75px, plus the rail.

**11a. WORDLESS CLAIM.** A line leaves a dark coast and is broken. Regions,
region A the arc's lit segment `[120,300,300,120]`, region B the gap and the
unlit sphere beside it `[700,330,260,110]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A night reconnaissance plate from orbit, NASA mission
poster restraint, nothing decorative.

**13. RISK FLAGS.** (a) three.js and d3 must agree, mitigated by projecting the
Pentagon through both and asserting agreement within 1px, logged to
`window.__akChecks`. (b) black-frame race, mitigated by `await AKT.snapshot(R)`
and checking `.ok`. (c) the figure is 14 characters and could wrap, mitigated by
fitText maxLines 1 and a 420px box measured after `fonts.ready`.

**14. ACCEPTANCE CHECKLIST.**
- [ ] the gap in the arc is visible at 432px thumb width
- [ ] the gold comma glyph sits ON the arc's own path, not beside it
- [ ] `$20,632,119.41` renders on one line with tabular figures
- [ ] the limb is NOT visible anywhere in the frame
- [ ] the specular streak runs one direction only, lower-left to upper-right
- [ ] the Alaska coastline is recognisable to an Alaskan at full size
- [ ] gold appears ONLY on the comma glyph
- [ ] the lower third carries modeled tone, no flat band

---

## SLIDE 02 — THE TWO QUERIES

**1. BEAT.** Pay the cover instantly with the measurement. Plants, how can a
superset return more.

**2. COPY, FINAL.**
- Lead, Manrope 700, 44px: `The longer phrase is inside the shorter one. The narrower search returns more.` (77 ch)
- Mono block, 27px, tabular:
  `"ARTIFICIAL INTELLIGENCE"                          24` [C01]
  `"ARTIFICIAL INTELLIGENCE, AND MACHINE LEARNING"    25` [C02]
- Callout, Unbounded 700, 76px: `NOTHING IN COMMON` (17 ch) [C03]
- Guard, mono 24px: `COUNTS RETURNED BY TWO NAMED FPDS-NG QUERIES. VENDOR STATE AK. NOT A TOTAL.`
- Rail: `61.5032N 143.2W . t 0.10 . 336 MI . 02 / 09`

**3. READER TAKEAWAY.** Two searches, one inside the other, and they share no
records at all.

**4. LAYOUT MAP.** Arc field cols 1 to 4. Type cols 5 to 12. 25 arcs leave the
Alaska coast in a low fan, all 25 drawn broken and dropped to `#3E6E96` at 40
percent; 24 solid arcs in `#8FA6BE` run beside them and never touch. Focal point
is the callout at (620, 690). Eye path is mono block, callout, guard. Quiet zone
cols 5 to 8 row 2.

**4a. LOWER-THIRD TREATMENT.** The lit sphere plus a declared unlit trough at the
band's left, whose contents are named rather than left flat: the rock's rib pitch
carried through as shallow engraved arches at az 142 el 24, plus the dome's
ambient return at the trough lip. Target 5.0 dE separation from the flat fill it
would otherwise be. Modeled tone.

**5. DEPTH PLAN.** Same z-stack as 01. Four cues, atmospheric perspective, arc
overlap where the two fans cross, scale gradient in the graticule, and fog toward
the dark limb. Focal plane is the mono block.

**6. CONTINUITY DEVICE STATE.** D2, all 25 arcs broken, the 24 solid. D3 rail t
0.10. D4 arc left, type right.

**7. TECHNIQUE STACK.** akthree sphere as 01 with camera advanced along the
transect. Arc fan generated from one seeded spread, `AK.rng(20260907 + 2)`,
angular spread 14 degrees. Phantom dash (#67) `30 5 6 5 6 5` at 1.25px on the
broken set. akpost house grade, no aberration on a data slide.

**8. DATA-IN-ART MAPPING.** Arc counts are literal, 25 broken and 24 solid, drawn
from the two arrays so the picture cannot disagree with the type.
`window.__akAssert` declares `{what:"25 broken arcs", expect:25, points:brokenCentres, unit:"marks"}`
and the same for the 24, with `actual` derived from the drawing arrays and never
from a literal.

**9. PALETTE.** As 01. Gold on the disjointness bracket only, 30px.

**10. TYPE SPEC.** Lead Manrope 700 44px leading 1.24 max width 720px. Mono 27px
tabular tracked +6%, two lines, right-aligned counts on a common column. Callout
Unbounded 700 76px fitText min 60 max 84 maxLines 1. Guard mono 24px `#8FA6BE`.

**11. ANCHOR SPEC.** Alaska coastline as the fan's origin. Leader from the gold
bracket to the broken set's centroid, authored as a world-coordinate polyline
ending on the set's own projected coordinates, declared in `window.__akLeaders`
with `from`, `at`, `to` and `label: "NOTHING IN COMMON"`.

**11a. WORDLESS CLAIM.** Two fans of lines leave the same coast and never touch.
Region A the solid fan `[100,520,290,260]`, region B the broken fan
`[100,300,290,200]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A range-safety plot. Two families of trajectories that
should overlap and do not.

**13. RISK FLAGS.** (a) 49 arcs is a lot of ink under type, mitigated by D4
column separation and by capping the fan to cols 1 to 4. (b) the phantom dash can
read as noise at thumb size, mitigated by the 40 percent value drop doing the
work instead.

**14. ACCEPTANCE CHECKLIST.**
- [ ] exactly 25 broken arcs and 24 solid arcs are drawn, and the assert agrees with the frame
- [ ] the two counts align on one right-hand column with tabular figures
- [ ] the two query strings are readable verbatim at full size
- [ ] the guard line naming these as query returns is present and legible
- [ ] the leader terminates ON the broken fan, not in void
- [ ] no arc crosses the mono block's line boxes
- [ ] the lower third's unlit trough has named engraved content, not a flat fill

---

## SLIDE 03 — THE COMMA

**1. BEAT.** The mechanism, and the deck's one loud device. Plants, which contract
fell in the gap.

**2. COPY, FINAL.**
- Display, Unbounded 700, 96px, 2 lines: `THE MARK` / `THAT HIDES` (8 / 10 ch)
- Case block, mono 26px, the comma in each set in gold:
  `ARTIFICIAL INTELLIGENCE,        MISSED`
  `ARTIFICIAL INTELLIGENCE,        MISSED`
  `ARTIFICIAL INTELLIGENCE (AI)    FOUND`
  `ARTIFICIAL INTELLIGENCE (AI)    FOUND`
- Lead, Manrope 700, 40px: `Four cases fit. A comma right after the phrase appears to break the match.` (73 ch) [C06]
- Guard, mono 24px: `APPARENT MECHANISM, NOT A PROVEN ONE. THE INCONSISTENCY ON THE LAST FRAME DOES NOT DEPEND ON IT.`
- Rail: `61.4N 136.4W . t 0.20 . 672 MI . 03 / 09`

The word "appears" and the guard line are REQUIRED. C06 carries confidence 0.72
and the fact-checker asked for exactly this softening.

**3. READER TAKEAWAY.** A comma right after the phrase is what the search trips on.

**4. LAYOUT MAP.** One arc pulled forward to hero weight, 5.5px cased, running
cols 1 to 5 with its gap enlarged to 120px at (300, 600). A gold comma glyph
Unbounded 700 96px sits INSIDE the gap at the correct along-track position. Type
cols 6 to 12. Focal point the comma at (322, 618). Eye path comma, display,
cases.

**4a. LOWER-THIRD TREATMENT.** The lit sphere plus an `akhachure` toned band over
the Alaska panhandle relief, height field taken from the frame's own rendered
depth buffer rather than from noise, so the shading is driven by the actual
surface. Modeled tone.

**5. DEPTH PLAN.** Same stack. Cues, DOF with the hero arc tack sharp and the fan
behind it blurred, occlusion where the hero arc crosses the graticule, atmospheric
ramp, and fog at the dark edge. Focal plane the comma glyph.

**6. CONTINUITY DEVICE STATE.** D2, the gap at its largest, 120px, holding the
comma. D3 rail t 0.20, near the vertex at 61.5032N 141.0823W. D4 arc left.

**7. TECHNIQUE STACK.** akthree sphere. akhachure (#92) band, height from depth
buffer, probes declared before build. akpost with aberration 0.8px permitted here
and nowhere else on a data slide, because this is the hero panel.

**8. DATA-IN-ART MAPPING.** Four case strings, four drawn states, two missed and
two found, matching C06's four cases exactly. The comma glyph's cap height equals
the gap width divided by 1.25, solved from the gap rather than typed.

**9. PALETTE.** As 01. Gold on the four comma characters in the case block plus
the hero glyph. Measured under 0.4 percent.

**10. TYPE SPEC.** Display Unbounded 700 96px leading 0.98 tracking -2% fitText
min 76 max 104 maxLines 2. Case block JetBrains Mono 400 26px tracked +8%,
two-column tab stop at 34ch. Lead Manrope 700 40px. Guard mono 24px.

**11. ANCHOR SPEC.** The hero arc is the anchor. Annotation is a dimension call
(#73) across the gap with 4px extension gaps and 6px overshoot, labelled
`120 PX AT THIS SCALE`, and it is DECORATIVE-FREE, the label states a screen fact
and not a story quantity.

**11a. WORDLESS CLAIM.** A single punctuation mark is sitting in a break in a
line. Region A the gap with the comma `[240,560,180,130]`, region B an unbroken
stretch of the same arc `[430,470,180,130]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A fault diagram. One defect, magnified, on an otherwise
continuous run.

**13. RISK FLAGS.** (a) the comma glyph could read as an apostrophe or a tail at
thumb size, mitigated by seating it in a 120px gap so the break reads first and
the glyph second. (b) aberration on a slide with mono text, mitigated by keeping
aberration to the ART canvas only and holding all type in DOM above it.

**14. ACCEPTANCE CHECKLIST.**
- [ ] the word "appears" is present in the lead line
- [ ] the guard line about it not being a proven mechanism is present and legible
- [ ] the comma glyph is unmistakably a comma at full size
- [ ] exactly four case strings, two MISSED and two FOUND
- [ ] gold appears on the comma characters and nowhere else
- [ ] the dimension call's label states a screen fact, not a story quantity
- [ ] the hachure band's height comes from the depth buffer, not from noise

---

## SLIDE 04 — WHAT FELL IN THE GAP

**1. BEAT.** Name the contract, to the cent, and state the lawfulness ON THE FACE.
Plants, how long has this run.

**2. COPY, FINAL.**
- Lawfulness line FIRST, mono 26px tracked, `#EAF1FA`: `LAWFUL. 8(a) IS THE MECHANISM CONGRESS BUILT.` (44 ch)
- Name, Manrope 700, 44px: `Leisnoi Professional Services LLC` (33 ch)
- Mono block, 28px tabular:
  `PIID        HQ003425CE092` [C07]
  `OFFICE      WASHINGTON HEADQUARTERS SERVICES` [C07]
  `OBLIGATED   $20,632,119.41   ACROSS 8 ACTIONS` [C07][C09]
  `CEILING     $20,632,119.41   OBLIGATED TO THE CENT` [C08]
  `MECHANISM   8(a) SOLE SOURCE   NAICS 541512` [C10]
  `PERFORMED   WASHINGTON DC 20301` [C12]
  `RUNS        SEPTEMBER 11TH, 2025 TO SEPTEMBER 10TH, 2026` [C11]
- Body, Manrope 500, 34px: `The vendor address is in Anchorage. The work is at the Pentagon.` (63 ch) [C12]
- Rail: `60.2N 125.1W . t 0.36 . 1,210 MI . 04 / 09`

**3. READER TAKEAWAY.** The hidden contract is an Anchorage-registered firm doing
Pentagon work, obligated to the cent.

**4. LAYOUT MAP.** Arc cols 1 to 5, gap now CLOSED and that arc solid, labelled at
both ends with leaders terminating on the projected coordinates. Type cols 6 to
12. Focal point the `$20,632,119.41` row. Eye path lawfulness line, name, figures.

**4a. LOWER-THIRD TREATMENT.** The lit sphere with the terminator ramp, plus the
Arlington limestone point mark at `#D6D0C2` sitting in the lower band as the
frame's only warm pixel, with the arc's final approach running into it. Modeled
tone.

**5. DEPTH PLAN.** Same stack. Cues, atmospheric ramp, arc-over-graticule
occlusion, scale gradient, DOF on the near arc. Focal plane the mono block.

**6. CONTINUITY DEVICE STATE.** D2 the gap is healed, and the healed segment is
the slide's gold, 6px by 210px. D3 rail t 0.36. D4 arc left.

**7. TECHNIQUE STACK.** akthree sphere. Leaders (#72) at 45 degrees with 20px
elbows and 5px filled-dot terminators. akpost house grade, no aberration.

**8. DATA-IN-ART MAPPING.** The healed segment's along-track span is centred on
the arc's own midpoint, the same position the gap held on 01 to 03, so the reader
sees the same place mended. No quantity encoded as length.

**9. PALETTE.** As 01, plus limestone `#D6D0C2` on the Arlington point only, 12px.
Gold on the healed segment.

**10. TYPE SPEC.** Lawfulness line mono 500 26px tracked +12%. Name Manrope 700
44px. Mono block 28px tabular tracked +6%, label column 12ch, value column
left-aligned at 13ch. Body Manrope 500 34px max width 460px.

**11. ANCHOR SPEC.** Two labelled endpoints. `ANCHORAGE 61.2181N 149.9003W` and
`THE PENTAGON, ARLINGTON 38.8719N 77.0563W`. Both leaders declared in
`window.__akLeaders` with `at` equal to `projection([lon,lat])` of their own
target and a `label` matching rendered DOM text.

**11a. WORDLESS CLAIM.** The line that was broken is now whole, and it ends on a
pale point. Region A the healed segment `[150,420,220,120]`, region B the
Arlington approach and limestone mark `[560,980,200,120]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A repaired circuit trace. The fault is closed and now
you can read where the line goes.

**13. RISK FLAGS.** (a) seven mono rows plus a name plus a body is dense for
VISUAL_DENSITY 2, mitigated by holding the arc field to a bare sphere with no fan
on this slide. (b) the two identical figures on consecutive rows could read as a
typo, mitigated by the `OBLIGATED TO THE CENT` label making the repetition the
point.

**14. ACCEPTANCE CHECKLIST.**
- [ ] the lawfulness line is the FIRST line of the type block, not the last
- [ ] both leaders terminate on their own projected coordinates
- [ ] the limestone point is the only warm-hued pixel in the frame
- [ ] `$20,632,119.41` appears twice with tabular figures and aligns exactly
- [ ] the deck says PERFORMED WASHINGTON DC 20301 and does NOT say Alaska
- [ ] no sentence implies the contract has been reviewed
- [ ] the healed segment sits at the same along-track position the gap held

---

## SLIDE 05 — SEVEN YEARS, ONE DAY

**1. BEAT.** The keepable data slide. The succession, and the historian's organ,
the buyers renamed and the sentence did not. Plants, where is any of it performed.

**2. COPY, FINAL.**
- Display, Unbounded 700, 84px, 2 lines: `THE BUYERS RENAMED.` / `THE SENTENCE DIDN'T.` (19 / 20 ch)
- Register rows, mono 26px tabular, bar length is MONTHS on a printed axis:
  `TUKNIK GOVERNMENT SERVICES   140D0419C0047   $21,596,322.25   14 ACTIONS` [C20]
  `TUKNIK, FOR THE JOINT AI CENTER   140D0421C0002   $24,210,536.43` [C19]
  `KONIAG IT SYSTEMS   HQ003425CE012   $12,022,390.38   ENDS SEPTEMBER 10TH, 2025` [C21]
  `LEISNOI PROFESSIONAL SERVICES   HQ003425CE092   $20,632,119.41   BEGINS SEPTEMBER 11TH, 2025` [C22]
- Dimension call, Unbounded 700, 64px, gold: `ONE DAY` [C22]
- Mono, 26px: `THEN   JOINT ARTIFICIAL INTELLIGENCE CENTER` [C19]
- Mono, 26px: `NOW   DEPUTY TO THE CHIEF DIGITAL AND ARTIFICIAL INTELLIGENCE OFFICE` [C13]
- Guard, mono 24px: `OBLIGATED TO DATE, NOT CEILING. TUKNIK IS A WHOLLY OWNED SUBSIDIARY OF KONIAG GOVERNMENT SERVICES.` [C23]
- Rail: `57.6N 112.4W . t 0.52 . 1,748 MI . 05 / 09`

**3. READER TAKEAWAY.** The same described work passed between Kodiak-linked firms
for seven years with one day between two of them.

**4. LAYOUT MAP.** Upper half, four arcs stacked from the same origin to the same
destination with a 14px normal offset each and atmospheric fade by age. Lower
half, cols 1 to 12, the deck's ONE flat cabinet-oblique register (#39). Focal
point the ONE DAY call at (700, 1010). Eye path display, register, ONE DAY.

**4a. LOWER-THIRD TREATMENT.** The cabinet-oblique register itself, four
three-face-shaded bars standing on a lit ground plane with real cast shadows at
az 142, plus the printed months axis. This is the slide's mass, deliberately
moved to the bottom band. Modeled tone.

**5. DEPTH PLAN.** background -> sphere (upper) -> four arcs -> cabinet register
on its own lit plane (lower) -> DOM type -> grain. Cues, atmospheric fade by arc
age at `(i/n)^1.4`, occlusion where arcs cross, three-face shading on the bars,
cast shadows sharing one bearing. Focal plane the register.

**6. CONTINUITY DEVICE STATE.** D2, four arcs, one origin, one destination, and
the gap between bars 3 and 4 at true scale is sub-pixel. D3 rail t 0.52. D4 arc
upper, type upper-right, register full width lower.

**7. TECHNIQUE STACK.** akthree sphere upper. Cabinet oblique (#39) lower, depth
at half scale 45 degrees, three-face light top +15L, left base, right -15L.
Dimension call (#73). akpost house grade.

**8. DATA-IN-ART MAPPING.** **Bar length is MONTHS OF PERFORMANCE on a printed
axis, never dollars.** The gap between bars 3 and 4 is one day at true scale,
which is 0.27 percent of a twelve-month bar and renders sub-pixel. **The honest
drawing of seamlessness is a gap you can't see**, and that is the slide's
argument. The dimension call points at the invisible gap and reads ONE DAY.

**MEASURED AXIS, DECLARED.** `<body data-scale>` carries
`{what:"the months axis", axis:"x", unit:"months", from:[80,0], to:[1000,96],
band:[1290,1312], marks:[...]}` with EVERY tick enumerated and given a meaning.
There is no decorative tick in that band.

**9. PALETTE.** As 01. Bars in `#16293F` to `#3E6E96` three-face. Gold on the ONE
DAY call only.

**10. TYPE SPEC.** Display Unbounded 700 84px leading 0.98 fitText min 68 max 92
maxLines 2. Register rows mono 400 26px tabular tracked +6%. ONE DAY Unbounded
700 64px gold. Guard mono 24px `#8FA6BE`.

**11. ANCHOR SPEC.** The four bars are the anchor. Furniture is the months axis
with labelled ticks, extension lines at 4px gaps, 6px overshoot, 3:1 arrowheads.

**11a. WORDLESS CLAIM.** Four bars of the same kind of work run end to end with no
visible break between the last two. Region A the bars 3 and 4 junction
`[600,1180,180,90]`, region B the wide gap between bars 2 and 3
`[300,1180,180,90]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A Gantt strip in a shipbuilding review. Dry, dated,
consequential.

**13. RISK FLAGS.** (a) a sub-pixel gap is the point but a reviewer may read it as
a rendering error, mitigated by the dimension call naming it. (b) four long mono
rows risk overflow, mitigated by fitText on the register and a measured 920px
box. (c) months-not-dollars must be unmistakable, mitigated by the printed axis
and the guard line.

**14. ACCEPTANCE CHECKLIST.**
- [ ] the months axis is printed and every tick in the band has a declared meaning
- [ ] no bar length encodes dollars
- [ ] the gap between bars 3 and 4 is visually smaller than the stroke weight
- [ ] the ONE DAY dimension call points at that gap and lands on it
- [ ] the Tuknik 2019 figure reads $21,596,322.25 and NOT $9,479,118.55
- [ ] both agency names appear, JAIC 2019 and Deputy to the CDAO 2026
- [ ] the guard line names Tuknik's parent
- [ ] four bars cast shadows sharing one bearing

---

## SLIDE 06 — HARD CUT. WHERE THE WORK LANDS

**1. BEAT.** The deck's turn. Camera snaps home and the arc is gone because its
length is zero. Plants, if the work is Outside, where does the money land.

**2. COPY, FINAL.**
- Display, Unbounded 700, 92px, 2 lines: `ARC LENGTH` / `ZERO` (10 / 4 ch)
- Row A, mono 26px: `PLACE OF PERFORMANCE ALASKA + "ARTIFICIAL INTELLIGENCE"   1 RECORD` [C16]
- Row A detail, mono 26px: `W519TC26CA019   KONIAG EMERGING TECHNOLOGIES   $5,267,244.80   ANCHORAGE 99503` [C13][C14]
- Row B, mono 26px: `PLACE OF PERFORMANCE ALASKA + "MACHINE LEARNING"   9 RECORDS` [C17]
- Row B detail, mono 26px: `ALL UNIVERSITY OF ALASKA FAIRBANKS. ALL NASA. $1,187,674.80 ACROSS THESE NINE.` [C17][C18]
- Body, Manrope 500, 34px: `Two very different things are both called Alaska AI.` (51 ch)
- Guard, mono 24px: `WHAT THE QUERY RETURNS, NOT A CENSUS. A COMMA WOULD HIDE ANY OTHER.` [C16]
- Rail: `62.0N 149.5W . t 0.01 . 34 MI . 06 / 09`

**3. READER TAKEAWAY.** Only one AI contract is actually performed in Alaska, and
the state's machine learning work is nine NASA grants at a university.

**4. LAYOUT MAP.** Full-frame sculpted Alaska terrain, the Chugach and Alaska
Range as a raymarched organic mass. Two ice-blue marks, Anchorage centre at
(520, 880) and Fairbanks upper at (600, 420). Type cols 6 to 12 upper, mono rows
lower-left. Focal point the Anchorage mark. Eye path display, Anchorage mark,
rows.

**4a. LOWER-THIRD TREATMENT.** The sculpted mass itself, carrying the Anchorage
marker, its cast shadow and its contact seam, plus a raised ridge fold running off
the bottom edge. This is the only slide in the deck where anything stands on
ground, and the lower band is where it stands. Modeled tone.

**5. DEPTH PLAN.** background -> aksdf raymarched terrain -> ice-blue marks and
their contacts -> DOM type -> grain. Cues, soft shadow from a single ray, contact
AO, atmospheric fade to the far range, and DOF with Anchorage sharp. Focal plane
the Anchorage marker.

**6. CONTINUITY DEVICE STATE.** D2, arc length zero. Two marks, no line, which is
the state that pays the whole transect. D3 rail resets from t 0.52 to t 0.01,
which is the cut made legible. D4, no arc, so type may occupy any column.

**7. TECHNIQUE STACK.** aksdf (#88), 11 primitives, quadratic smin, 480x720
internal upscaled, tetrahedral normals, 5-tap AO on sky and indirect only, single
soft-shadow ray k=14, two-tone warm-key cool-shadow ramp, ACES, cached by seed
`20260907 + 6`, `deadlineMs` degrades shadows to AO and never aborts. akpost with
aberration 0.6px permitted, since this is a hero panel and carries no dense mono
over the art.

**8. DATA-IN-ART MAPPING.** One mark for the one record, nine marks for the nine,
drawn from the arrays. `window.__akAssert` declares
`{what:"9 UAF machine learning records", expect:9, points:uafCentres, unit:"marks"}`
with `actual` from the drawing array. The nine are drawn as a tight Fairbanks
cluster, so `dispersed` is NOT set, because these are one place and not an extent.

**9. PALETTE.** Terrain `#0B1626` to `#3E6E96` via `AKC.ramp`. Ice blue `#5AC8F0`
on the two marks and NOWHERE else in the deck. Gold on the rail Polaris only.

**10. TYPE SPEC.** Display Unbounded 700 92px leading 0.98 fitText min 74 max 100
maxLines 2. Mono rows 400 26px tracked +8%. Body Manrope 500 34px. Guard mono
24px.

**11. ANCHOR SPEC.** The Alaska Range silhouette is the anchor and it is real
terrain, not invented. Scale bar in statute miles, the deck's ONLY one, legitimate
here because the extent is about 17 degrees and orthographic distortion is under
0.2 percent, and that is stated in this dossier.

**11a. WORDLESS CLAIM.** Where the work is actually done there is no line at all,
only ground with something standing on it. Region A the Anchorage marker and its
contact `[440,820,180,140]`, region B an equivalent patch of bare sculpted ground
`[760,820,180,140]`. `reads: "differ"`.

**CONTACT SHADOW, THE DECK'S ONLY ONE, DECLARED.** `<body data-contacts>` with
the Anchorage marker's shadow and ground rects. Build order is lit pool FIRST,
then the cast, then the seam. The lit pool is wider than the cast's ambient term.
Rects are MEASURED off the render with
`python3 scripts/contact_probe.py --render-dir out/2026-09-07/render --slide 6 --base 520,880`
and pasted, NEVER computed off camera arithmetic. Target separation 12 to 30 L*,
pair within 96px. **The floor is not a target. If the contact reads, stop.**

**12. REFERENCE INTENT.** A relief model under museum lighting. The land is the
only solid thing in a deck made of lines.

**13. RISK FLAGS.** (a) the hard cut may not read as a return home at 432px,
mitigated by making the Alaska Range silhouette large and unmistakable rather than
relying on the 24px rail readout, which is the exact failure the cartographer
flagged. (b) aksdf carved regions go near-black, mitigated by raising the indirect
floor. (c) render cost 5 to 15s, mitigated by seed caching.

**14. ACCEPTANCE CHECKLIST.**
- [ ] no arc appears anywhere in the frame
- [ ] the Alaska Range reads as Alaska at 432px thumb width
- [ ] exactly one ice-blue mark at Anchorage and nine at Fairbanks, assert agrees
- [ ] ice blue appears on these marks and nowhere else in the deck
- [ ] the contact pair was measured with contact_probe, not computed
- [ ] the contact reads as attached, with no gap between marker and shadow
- [ ] the guard line saying this is not a census is present
- [ ] the scale bar is present and the extent justifies it

---

## SLIDE 07 — BREATHER. WHAT COMES HOME

**1. BEAT.** Declared rest beat, and the fairness in full. Plants, what else does
the mechanism buy.

`data-breather` IS SET on the body. The deck needs a rest here because 05 and 06
are the two densest frames and 08 is the counterweight, which has to land on a
reader who is not already saturated.

**2. COPY, FINAL.**
- Lead, Manrope 700, 42px: `The sharing rule covers resource revenue. It doesn't reach government contracting.` (80 ch) [C32]
- Mono block, 26px:
  `43 U.S.C. 1606(i)   70% OF TIMBER AND SUBSURFACE REVENUE, SHARED ACROSS TWELVE REGIONAL CORPORATIONS` [C31]
  `DIVIDEND            $33 PER SHARE, DISTRIBUTED JANUARY 27TH` [C33]
  `ELDER BENEFIT       $1,200` [C34]
  `SHAREHOLDERS        4,700+ TODAY, 3,400 AT INCORPORATION` [C35]
  `FOUNDATION          $10 MILLION+, 4,000+ SCHOLARSHIPS, 158 CURRENT` [C36]
- Body, Manrope 500, 34px: `So this money comes home through one corporation's own channels.` (63 ch) [C37]
- Guard, mono 24px: `8(a) IS ROUGHLY 4 PERCENT OF ALL FEDERAL CONTRACTING.` [C48]
- Rail: `57.5N 152.2W . t 0.00 . KODIAK . 07 / 09`

**NOTE, the dividend year is deliberately absent.** C33's source gives January 27
with no year. The slide prints the day and no year. Do not restore a year.

**3. READER TAKEAWAY.** Contracting revenue is not shared under the settlement
act, so it returns through the corporation that earned it.

**4. LAYOUT MAP.** Camera over Kodiak at S=2200, limb in one corner, fill raised
to 2.5:1 so this is the flattest frame in the deck. Mono block cols 7 to 12, rows
3 to 6, right-aligned to the rail. Very large air, cols 1 to 6. Focal point the
lead line. Quiet zone cols 1 to 5 rows 2 to 4, about 22 percent, under the ceiling.

**4a. LOWER-THIRD TREATMENT.** The lit limb crossing the lower band with the
atmospheric shell glow above it, plus a graded starfield below with a real value
ramp rather than a flat black. The Kodiak Archipelago coastline sits in the band,
cased, as the literal anchor. Modeled tone, and this is a declared rest beat that
still carries mass.

**5. DEPTH PLAN.** background -> sphere -> limb shell -> starfield -> coastline ->
DOM type -> grain. Cues, atmospheric shell, limb occlusion, scale gradient in the
graticule, fog. Focal plane the coastline.

**6. CONTINUITY DEVICE STATE.** D2, no arc at all, second consecutive slide of
absence, which makes 08's return land. D3 rail reads KODIAK rather than a
distance, the one row where the rail names a place. D4 no arc, type right.

**7. TECHNIQUE STACK.** akthree sphere with fill raised. Atmospheric shell mesh.
akpost house grade, IGN dither ON because this is the largest soft gradient in the
deck, no aberration.

**8. DATA-IN-ART MAPPING.** The shareholder growth is drawn as two ISOTYPE dot
rows, 34 dots and 47 dots, each dot equal to 100 shareholders, same-size
pictograms and never enlarged ones. The 13 additional dots are a brighter step of
the same ramp, NOT gold. `window.__akAssert` declares both counts from the drawing
arrays.

**9. PALETTE.** As 01, fill raised. Dots in `#3E6E96` and `#8FA6BE`. Gold on the
rail Polaris only.

**10. TYPE SPEC.** Lead Manrope 700 42px leading 1.26 max width 640px. Mono block
400 26px tracked +8%, label column 20ch. Body Manrope 500 34px. Guard mono 24px.

**11. ANCHOR SPEC.** Kodiak Archipelago coastline from `alaska-state.geo.json`,
cased at 1.25px. Furniture is the graticule and the rail.

**11a. WORDLESS CLAIM.** None declared. This is a rest beat and the frame makes no
wordless argument. Written as "none, because this slide is a declared breather and
its job is air".

**12. REFERENCE INTENT.** A quiet orbital plate. The place the money is for,
seen from far enough away to be calm.

**13. RISK FLAGS.** (a) a breather carrying five mono rows is a tension the
treatment admitted, mitigated by cutting the settlement trust row entirely, which
the fact-checker killed anyway, and by holding the left six columns completely
empty. (b) a large soft gradient will band, mitigated by IGN dither always on.

**14. ACCEPTANCE CHECKLIST.**
- [ ] `data-breather` is set on the body
- [ ] no settlement trust figure appears anywhere
- [ ] the dividend line prints January 27th with NO year
- [ ] the 1606(i) line says the rule covers timber and subsurface, and does NOT say the law exempts contracting
- [ ] two ISOTYPE rows of 34 and 47 same-size dots, assert agrees with the frame
- [ ] the left six columns are genuinely empty
- [ ] the lower band carries the lit limb and shell glow, not flat black

---

## SLIDE 08 — THE COUNTERWEIGHT

**1. BEAT.** The same mechanism buys other things, and Alaskans argue about it in
their own register. Plants, what does Alaska AI mean then.

**2. COPY, FINAL.**
- Lead, Manrope 700, 42px: `The same mechanism buys other things.` (36 ch)
- Mono block, 26px:
  `KONIAG SERVICES INC   ICE   TASK ORDER 70CDCR26FR0000034` [C38]
  `OBLIGATED   $17,456,917.40` [C38]
  `EFFECTIVE   AUGUST 6TH, 2026 TO AUGUST 5TH, 2030` [C39]
  `PERFORMED   NASHVILLE, TENNESSEE` [C40]
  `REPORTED    UP TO $63 MILLION, PER THE TENNESSEE LOOKOUT` [C41]
- Body, Manrope 500, 34px: `Bering Straits shareholders petitioned their own corporation to divest from ICE detention work. 102 signatures.` (110 ch)
- Threshold line, Manrope 500, 34px: `Sole source 8(a) awards above $20 million were ordered reviewed in January 2026. The Leisnoi contract is $632,119.41 above that line. No review of it is on the record.` [C42][C07][C56]
- Pull quote, Manrope 700, 36px: `"Nobody has quantified how much of that $13.5 billion runs through 8(a) contracts."` [C43]
- Attribution, mono 24px: `ROSS JOHNSTON, COMMONWEALTH NORTH, ADN, JUNE 6TH, 2026` [C43]
- Rail: `41.0N 82.1W . t 0.90 . 3,026 MI . 08 / 09`

**THE THRESHOLD SENTENCE IS EXACT AND MAY NOT BE REWORDED.** It states the order,
states the arithmetic, and states the absence of evidence. It does not imply a
review happened.

**3. READER TAKEAWAY.** The same 8(a) route carries work Alaskans themselves argue
about, and the record is not comfortable in either direction.

**4. LAYOUT MAP.** Arc returns, cols 8 to 12, and BRANCHES southwest to Nashville
at 36.16N 86.78W, a point that sits almost under the transect's own flight path.
Type cols 1 to 7. Focal point the branch junction. Eye path lead, mono block,
threshold line, quote.

**4a. LOWER-THIRD TREATMENT.** The lit sphere with the terminator ramp, the
branch arc descending through the band toward Nashville, and 102 small punch
marks struck into the lower-left as a modeled field, each with a lit windward lip
and a dark lee edge at az 142. Modeled tone.

**5. DEPTH PLAN.** Same stack. Cues, atmospheric ramp, arc overlap at the branch,
scale gradient, DOF. Focal plane the branch.

**6. CONTINUITY DEVICE STATE.** D2, the arc returns after two slides of absence
and branches for the first time in the deck. D3 rail t 0.90. D4 arc right, type
left, the mirror of 01 to 05.

**7. TECHNIQUE STACK.** akthree sphere. Punch-mark field with per-mark modeled
relief, seeded `AK.rng(20260907 + 8)`. Leader (#72) from the punch block to its
label, declared. akpost house grade, no aberration.

**8. DATA-IN-ART MAPPING.** 102 punch marks for 102 signatures, countable at full
size and a texture at 432px. `window.__akAssert` declares
`{what:"102 signatures, one mark each", expect:102, points:markCentres, unit:"marks"}`,
`actual` from the drawing array, and the composited ink probe rides on `points`.

**9. PALETTE.** As 01. Limestone on the Arlington point. Gold on the rail Polaris
only, so the counterweight carries no accent, which is deliberate.

**10. TYPE SPEC.** Lead Manrope 700 42px. Mono block 400 26px tracked +8%. Body
and threshold Manrope 500 34px leading 1.38 max width 520px. Quote Manrope 700
36px. Attribution mono 24px.

**11. ANCHOR SPEC.** The branch to Nashville is the anchor. Leader declared with
`at` on Nashville's own projected coordinates and `label: "102 SHAREHOLDER AND DESCENDANT SIGNATURES"`
matching rendered DOM text.

**11a. WORDLESS CLAIM.** The line forks, and the fork goes somewhere else
entirely. Region A the branch junction `[720,600,200,140]`, region B the main
arc's continuation `[820,860,200,140]`. `reads: "differ"`.

**12. REFERENCE INTENT.** A wire diagram with an unexpected tap. Dry, not
accusatory.

**13. RISK FLAGS.** (a) the threshold sentence is the most legally sensitive
string in the deck, mitigated by fixing the wording here and adding an acceptance
check. (b) 102 marks under type, mitigated by holding them to the lower-left
outside the type columns. (c) Nashville must not be written as Adams, mitigated
by an acceptance check.

**14. ACCEPTANCE CHECKLIST.**
- [ ] the place of performance reads NASHVILLE and never Adams
- [ ] the obligated figure $17,456,917.40 appears, and $63 million is labelled as reported
- [ ] the term reads August 6th, 2026 to August 5th, 2030 and is never called one year
- [ ] the entity is Koniag Services Inc, not Koniag Government Services
- [ ] the threshold sentence appears verbatim as specified, including "No review of it is on the record."
- [ ] exactly 102 punch marks, assert agrees with the frame
- [ ] no gold accent appears except the rail Polaris

---

## SLIDE 09 — CLOSE

**1. BEAT.** One ask, and a date a reader can go and check. Pays the whole deck.

**2. COPY, FINAL.**
- Display, Unbounded 700, 88px, 2 lines: `SEPTEMBER 10TH,` / `2026.` (15 / 5 ch)
- Body, Manrope 500, 34px: `Leisnoi's period of performance ends that day. The federal fiscal year ends September 30th. Whatever happens next shows up in the same public feed.` (146 ch) [C11]
- THE ONE ASK, Manrope 700, 40px: `Which Alaska AI do you mean?` (28 ch)
- Mono, 26px: `FPDS-NG. VENDOR STATE AK. SEARCH THE REQUIREMENT DESCRIPTION FOR BOTH STRINGS, WITH THE COMMA AND WITHOUT IT.`
- Mono, 24px: `SOURCES IN COMMENTS`
- Wordmark `ALASKA.AI` Unbounded 700 34px, `alaskaaihq.com` JetBrains Mono 400 22px beside it
- Rail: `55.6184N 103.6097W . WHOLE ARC . 3,362 MI . 09 / 09`

**ONE ASK ONLY.** The mono search instruction is CONTENT, not a second ask. It
tells the reader how to answer the question, which is the same act.

**3. READER TAKEAWAY.** Go look at the feed after September 10th, and decide which
Alaska AI you meant.

**4. LAYOUT MAP.** Camera pulls all the way out, S=400, limb visible, the ENTIRE
transect in one frame end to end for the first and only time. Arc runs centre
diagonally. Type cols 1 to 6 upper, ask cols 1 to 8 lower. Focal point the Polaris
seal at the Anchorage end. Eye path display, arc entire, ask.

**4a. LOWER-THIRD TREATMENT.** The lit limb across the band with the atmospheric
shell glow, the arc's Anchorage terminus sealing into the gold Polaris, and the
mono instruction block set over graded sphere rather than over black. Modeled tone.

**5. DEPTH PLAN.** background -> sphere -> limb shell -> arc entire -> Polaris ->
DOM type -> grain. Cues, atmospheric shell, limb occlusion, scale gradient, fog.
Focal plane the Polaris.

**6. CONTINUITY DEVICE STATE.** D2 resolves. The gap that opened on 01 is gone and
the arc is entire, end to end, sealed into the Polaris at the Anchorage end. That
is the motif's final state and the deck's visual resolution. D3 rail reads WHOLE
ARC and 3,362 MI. D4 arc centre, type left.

**7. TECHNIQUE STACK.** akthree sphere at S=400 with the limb visible. Polaris as
flat DOM SVG so akpost never shifts a brand-exact mark. akpost house grade,
aberration 0.4px permitted, IGN dither on.

**8. DATA-IN-ART MAPPING.** The arc is the same 512-point geodesic as every other
slide, now shown entire, so its drawn length IS the 3,362 miles the rail prints.
`window.__akAssert` declares
`{what:"the transect printed as 3,362 miles", expect:3362, actual:milesFromGeodesic, tol:6, unit:"mi"}`
where `actual` is computed from the sampled path and NOT typed as a literal.

**9. PALETTE.** As 01. Gold on the Polaris and the wordmark period. Limestone on
the Arlington terminus.

**10. TYPE SPEC.** Display Unbounded 700 88px leading 0.98 fitText min 70 max 96
maxLines 2. Body Manrope 500 34px max width 480px. Ask Manrope 700 40px. Mono
26px and 24px tracked +10%.

**11. ANCHOR SPEC.** The whole transect plus both coastlines. Furniture is the
graticule, the rail and the scale-free limb.

**11a. WORDLESS CLAIM.** The broken line from the cover is whole, and it reaches
from one dark end to one lit end. Region A the Anchorage terminus with the Polaris
`[300,880,200,140]`, region B the Arlington terminus with the limestone mark
`[720,520,200,140]`. `reads: "differ"`.

**12. REFERENCE INTENT.** The last plate in a survey report. Everything shown at
once, quietly.

**13. RISK FLAGS.** (a) exactly one ask, mitigated by an acceptance check that
counts imperatives. (b) the site fixture must be present and small, mitigated by
the spec. (c) at S=400 the coastlines are small, mitigated by drawing them cased
and accepting that this frame is about the whole line rather than about place.

**14. ACCEPTANCE CHECKLIST.**
- [ ] exactly ONE ask appears, and the mono search string is not phrased as a second ask
- [ ] `sources in comments` is present
- [ ] `alaskaaihq.com` is present, small, in the mono face, near the brand mark
- [ ] the arc is unbroken from end to end
- [ ] the assert's `actual` is computed from the geodesic, not typed
- [ ] the rail prints 3,362 MI and the drawn arc does not contradict it
- [ ] the Polaris is DOM or SVG and unshifted by the grade

---

# BUILD RECONCILIATION

The build left the plan in forty-five named places, one row each with the reason
it moved, accumulated across five revision rounds and a Phase 12 pass. They fall
into repairs to facts or sourcing, type that was crossing type, lighting or
probes that were measuring the wrong thing, and placement. The largest single
one is the limb glow: a radial gradient with a non-zero inner radius adds a rim
light FLAT over the whole globe, because canvas paints every pixel inside that
radius with stop 0. It was doing that on EIGHT of the nine slides and quietly
erasing the az-142 terminator the entire deck is built on. Seven were repaired
in round 2 by matching `S-6`; the eighth was written `S-8` and survived five
more rounds until a gate that measures gradients rather than matching names
found it in Phase 12.

**WHERE THE BUILD LEFT THE PLAN, per slide.**

Written after the Phase 8 rounds, from the shipped render and not from memory.

| slide | divergence from the dossier | why |
|---|---|---|
| 01 | composition MIRRORED: type left, arc right. The dossier's layout map, focal point and 11a rects describe the opposite. | The build settled early and the code's own `data-encodes` rects are the honest ones. The map was not reconciled until this table. |
| 02 | The bracket's terminators grew from 4px dots to 9px discs with a dark casing. | At 4px they were invisible at 432px and too small for the encoding probe to measure at all. They are the marks that say the two sets share nothing, so they earn the size. |
| 02 | The wordless claim was re-authored. It was "two families of lines leave the same coast and never touch", probed over two 180x140 boxes. | qa reads the MEDIAN of a region, so both boxes measured the ground the lines are drawn on rather than the lines: one population, measured twice. The claim now compares the two temperatures of ink actually in the frame, and the regions were MEASURED off the render. |
| 03 | Same class of repair. The probe now sits inside the comma's own body and inside the transect's 4.5px stroke, both measured off the PNG. | Same reason: a wide box around a thin feature measures background twice. |
| 04 | The record block gained a THROUGH row and the PENTAGON endpoint label moved 238px up, clear of the block. | The label was printing ON the ACTIONS row and truncating it, and ISO dates are not slide copy. |
| 05 | Entity names printed in full: TUKNIK GOVERNMENT SERVICES and LEISNOI PROFESSIONAL SERVICES, not TUKNIK and LEISNOI. | The fact-checker KILLED the Leisnoi Inc ownership link. A bare LEISNOI beside a Pentagon contract asserts wordlessly what the record does not carry. |
| 05 | The ONE DAY call moved out of the register band into the empty band above it, and its leader grew a real run. | It was printing over the Leisnoi row and shredding $20,632,119.41 on the slide whose job is exact figures. |
| 05 | Bar length is TIME, with Koniag IT Systems' start phantom-dashed because the record does not carry it. The guard now also says the dollar figures are obligated. | Four dollar figures printed beside four time bars needed both qualifiers, not one. |
| 06 | Terrain is akthree displaced relief, not aksdf. | Decided in Phase 7 after a de-risking smoke test. |
| 06 | The frame was RELIT in Phase 8: key 3.6 to 6.4, sky 0.14 to 0.34, material 0x16293F to 0x2C4A6E. | The first build sampled the terrain at roughly L* 3 to 9 against an L* 3 sky, so the deck's declared hard cut read as a failed render rather than a deliberate stop. |
| 06 | The deck DOES carry one contact shadow after all, and it is here. | The dossier promised one and the first build shipped none, which left qa's contact gate switched off on the only slide that could honestly carry it. A lit pool was laid on the site first, because dark ground gives a shadow nothing to be darker than; shadow and ground rects are MEASURED, dL 18.3. |
| 07 | The record block gained a line so that 1606(i) reads 70% OF TIMBER AND SUBSURFACE REVENUE. | Without REVENUE the slide misstated the statute: it shares 70 percent of the revenue from those estates, not 70 percent of the estates. |
| 07 | A KMXT attribution line was added to the guard. | C34's own note says to attribute on the slide; three non-primary background figures were being stated in the deck's voice. |
| 07 | The ISOTYPE labels were rebuilt as three explicitly placed elements. | The dot rows were drawn straight through their own labels. |
| 08 | The threshold sentence, which the dossier froze, now opens "A law firm briefing reports that". | C42 is marked NON PRIMARY, MUST BE LABELLED. The sentence's logic, the order, the arithmetic and the absence of a review, is untouched. |
| 08 | "This one is $632,119.41 above that line" became "The Leisnoi contract is". | "This one" had no antecedent on this frame. The only contract named here is the ICE task order at $17,456,917.40, which is BELOW the threshold, so the sentence as built said the opposite of the record. |
| 08 | REPORTED now reads "UP TO $63 MILLION, A CEILING" with a SOURCE row naming Alaska Public Media, not the Tennessee Lookout the dossier named. | The Lookout page returns 403; the fetched source is the Alaska Public Media republication, and C41 is a reported ceiling, not money spent. |
| 08 | The 102 signature line survived only because it was VERIFIED in Phase 8 as C54 and C55. | The dossier carried it from a scout note that the first claims pass never turned into a claim, so the frame was printing an unsourced fact. Verifying it also corrected it: shareholders AND descendants, an early-December count, and 20 non-shareholder signatures excluded. All three now print. |
| 08 | No contact shadow, and no gold Polaris on the rail. | The contact-shadow defect class was deleted deck-wide except for slide 06; gold is held to slides 01, 02, 03 and 05. |
| 09 | "The federal fiscal year ends September 30th." was CUT. | It carried no claim-id and claims.json has none for it. Every fact carries a claim-id. |
| 09 | The Arlington terminus grew a 26px open limestone ring. | At 5px it was one pixel at feed scale, so the payoff frame argued that Alaska was the loud end, the inverse of the thesis. |
| 01, 02, 03, 04, 05, 08, 09 | The atmospheric limb glow was rebuilt as a true annulus on SEVEN slides. | It was a radial gradient with an inner radius of S-6, and canvas paints every pixel inside that radius with stop 0, so a rim light was being added FLAT over the whole globe in `lighter` mode. That single line was erasing the az-142 terminator the entire deck is built on. |
| 03 | The dimension call '121 PX AT THIS SCALE' moved above the case block, set on two lines, with a stem drawn down to the dimension line it belongs to. | ROUND 2, the capping defect. It was set through case row 2 and neither string read at 432px. Its leader declaration moved with it. |
| 04 | Both endpoint labels moved 44px left. | ROUND 2. Their last glyphs were inside the rail's own mono column. |
| 04 | The ANCHORAGE label and its leader recoloured from ice blue to #8FA6BE. | ROUND 2. Ice blue means ALASKA PERFORMED in this deck with zero cross-leak declared, and this is a VENDOR ADDRESS on the frame arguing the work is at the Pentagon. The palette was arguing against the copy. |
| 05 | The register rows split into a name at the left margin and a value column right-aligned to the gutter. | ROUND 2. The two longest rows reached the rail. It also puts the four PIID and dollar pairs on one shared right edge, which is what the block should always have been. |
| 06 | Mono rows narrowed to 856px at 24px, the Fairbanks tag moved 66px left, the scale bar moved 92px left. | ROUND 2. The closing quote of ARTIFICIAL INTELLIGENCE and both the tag and the bar label were inside the rail column. |
| 08 | THE PENTAGON and NASHVILLE clamped on their MEASURED width rather than on a guessed W-276 constant. | ROUND 2. The constants were wrong for these two strings and both ran into the rail. |
| 08 | The guard now opens BERING STRAITS IS NOT KONIAG. | ROUND 2. C55's own note warns the two corporations must never blur, and the frame set a Bering Straits petition beside a Koniag task order without saying they are different companies. |
| 07 | The forward hook became a question, 'Does all of it come home?' | ROUND 2. As a statement it asserted a fact and carried no claim-id. A question asserts nothing and plants slide 08 harder. |
| 02 | The SETS DISJOINT label clamped to the gutter on its measured width. | ROUND 2. |
| 05 | The register's value column is now placed from MEASUREMENT, its left edge set to the widest name plus a 30px gap and clamped to the gutter, with an `__akChecks` assertion that the two columns cannot touch. | ROUND 3, and this one was a regression the round-2 fix caused. Right-aligning the values to the gutter pulled them left onto the longest name and printed SERVICESHQ003425CE092. A constant could not have been right for four names of different lengths. |
| 06 | The APPROX 200 MI scale bar and its label were REMOVED. | ROUND 3. It was wrong by 79 percent, since Anchorage to Fairbanks is 260 miles and the drawn 417px separation against a 180px bar implied 464. More importantly the frame is displaced terrain rather than a projection and both mark sets are placed by composition, so no scale bar can be honest on it; correcting the number would only have tidied a false precision claim. |
| 06 | A feathered full-width atmospheric band was laid under the two mono rows. | ROUND 3. The worst point of row A crossed a lit ridge at 3.99:1 against a 4.5 floor, which is a hard-fail criterion. The deck bans plates and scrims, so the value came out of the ART. Every text node on the frame now measures 6.48:1 or better. |
| 08 | The guard became three short lines inside the gutter and the bottom stack lifted to make room. | ROUND 3. Its ink ran to 9px from the frame edge, past the rail and past the 80px safe margin, because a nowrap string overflowed a box that itself measured inside the margin, so no box-based gate saw it. |
| 07 | Both printed instances of the year 1971 became AT INCORPORATION. | ROUND 4, the capping defect. C35 says "3,400 shareholders at incorporation" and the year lived only in the fact-checker's note as "consistent with 1971", which is inference rather than verification. It also carried live risk: ANCSA was signed in 1971 but the twelve regional corporations incorporated in 1972, so the deck that argues one character changes an answer was likely printing the wrong founding year, in mono, twice, on its Alaska-facing frame. |
| 05 | The year axis ends at x 950 rather than x 1000. | ROUND 4. The 2027 label ran to x 1023, past the 80px safe margin, on the slide whose own declaration says the axis ends at 1000. Every bar, tick and the ONE DAY leader derive from the axis, so they followed it in. |
| first comment | The closing line lost its first person. | ROUND 4. brand.yaml scopes the first-person ban to the caption and caption_check passed it, so this was not a rule breach, but it is the page narrating its own work in the most-read comment on the post, which is the posture the rule exists to prevent. |
| 02 | The lead became "The shorter phrase is inside the longer one." | ROUND 5. It read "The longer phrase is inside the shorter one", which is the INVERSE of its own cited C03, "the longer phrase is a strict superset of the shorter one". On the frame carrying the argument, to an audience who run federal phrase search for a living. |
| 05 | The buyer pair became THEN and NOW rather than 2019 and 2026. | ROUND 5. The JAIC-named contract in the record is 140D0421C0002, signed December 2020 to September 2021 (C19); the 2019 award C20 never names the JAIC. Pairing the year with the office asserted a mapping the record does not carry, the same class of inference as the 1971 line. The slide's argument is the RENAMING, and the year axis underneath already carries the chronology. |
| caption | "runs back to 2019 and the Joint Artificial Intelligence Center" became two sentences. | ROUND 5. Same soft pairing as slide 05, in the copy. Splitting rather than adding a comma, because the comma budget is a hard fail and the house rule says split the sentence instead. |
| 07 | The limb glow's EIGHTH flat-core instance was repaired, and the KODIAK label's halo strengthened. | PHASE 12. Round 2's annulus repair matched `createRadialGradient(CX,CY,S-6,...)` by regex; slide 07 used `S-8`, so it kept the flat additive wash for five more rounds. It is the frame every critic called a broad flat blue gradient and the reason artwork craft held at 7. The new engine gate found it by MEASUREMENT rather than by name, on its first run, and printed the stop-based annulus to write instead. Restoring the terminator then made the coastline read through the KODIAK label, so its halo went to the deck's full eight-direction stack. |
| 05, 07 | Two dossier lines reconciled to the build, `2019 JOINT ARTIFICIAL INTELLIGENCE CENTER` to THEN and `3,400 AT INCORPORATION IN 1971` to `3,400 AT INCORPORATION`. | PHASE 12. Five repair rounds had left the PLAN behind the deck. The upgraded dossier figure check reads the planned copy against claims.json and caught both. |
| 08 | $632,119.41 is now C56, recorded with `derived_from` C07 and C42. | PHASE 12. It was printed on a frame with no claim carrying it, and aggregate_check's shape detector never saw it because it is a difference rather than a count, a span or a ratio. It is exact arithmetic on two verified claims and inherits C42's softness, which slide 08 already labels. |
| caption | The measured-silence beat the storyboard planned for was cut. | It did not survive the caption room, and the caption is the whole deck for a screen reader, so it may not braid in a strand no slide carries. |




## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-09-07. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[WARN] qa.py          WARN, 0 fails, 5 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 45 table row(s), 13727 chars
[PASS] caption_check  PASS, 776 chars, hook 118, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 99 authored slide strings all present in the render
[PASS] aggregate      aggregate_check: PASS -- 13 aggregate assertion(s) detected, 13 declared -> out/2026-09-07/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 35 claims indexed, 0 declared counts checked, 0 body quote(s) checked, 0 drift(s)
[PASS] bespoke        bespoke_check: WARN -- 9 slides, median pairwise art similarity 0.431 (fail at 0.60), max pair 0.631, drawn share 76% (115 drawn vs 36 block
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] docket_dates   docket dates clean at 2026-09-07: 301 assertions over 6 fixtures and 24 ledger items
[PASS] gas_watch      34 day(s) on record, 32 verified, no gaps, latest 2026-09-07, EIA through 202605 over 131 months, model misses by 6.82%
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-09-07 (175 generated files)
[PASS] assemble       9 slides, pdf vector 8.95 MB, 9 thumbs, sources verified
[PASS] score          9.07 / 10 vs threshold 7.7, scorer says passes=True
[PASS] ship_gate      scored 9.07 against a threshold of 7.70
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```
