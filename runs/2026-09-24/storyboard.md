# STORYBOARD — Carousel No. 67 — September 24th

## THESIS

XPRIZE Wildfire's autonomous track was examined over the Tanana Flats at Nenana and paid out in New
York on September 23rd, and the record of the result is thinner than the purse. The one 10 minute
gate on the record as met is a detection gate (S1-C31). Nothing in XPRIZE's release says any team
fully suppressed a fire inside 10 minutes (S1-C34). The next 12 to 15 months name no Alaska place
and no Alaska fire agency (S1-C39, S1-C41, S1-C42). **Hosting the exam didn't make Alaska the
customer, and the state that hosted it has a reason to ask for a seat in what comes next.**

PDF document title (at most 60 chars): `Tested at Nenana. Awarded in New York. Next stop unnamed.`

## ARC, nine slides

| # | Beat | Temperature | Open loop planted |
|---|---|---|---|
| 01 | HOOK, three datelines, two filled and one blank | cold, wide | who won, and did anyone reach the goal? |
| 02 | PAY, the verdict and the purse, camera turned toward New York | warm, specific | where was it earned? |
| 03 | PLACE, the airport and the airspace, close | intimate | what did the machines have to do? |
| 04 | TASK, the square revealed at true size, the clock stated | wide, monumental | did anyone beat the clock? |
| 05 | TURN, the scorecard, one gate met, one lane empty | tight, forensic | so where does the prize stand? |
| 06 | BREATHER, the quote laid on the literal horizon | still | how big is the problem the prize is for? |
| 07 | DATA, keepable, one season in test squares | cool, factual | what comes next, and where? |
| 08 | ESCALATE, what comes next names no Alaska address | cooling | should that change? |
| 09 | CLOSE, one ask | resolved | none |

## SLIDE COUNT RATIONALE

Nine. The story has exactly nine distinct verified beats: a verdict, a place, a task, a scorecard,
a quote, a scale comparison, a next phase, and a hook and a close. Three extra candidates were cut
because each would repeat a beat: the entrant funnel (about 300 entrants, per Dryad, S1-C26, lives
only as a thought and is not printed), the three machines in detail (folded into 02's names), and
VIP Day (folded into 08's institutions line).

## CONTINUITY SYSTEM (three devices, >= 2 required)

**D1 CAMERA MOVE.** One real terrain (assets/geo/nenana-dem.bin, 197 m cells), one light, one
vertical exaggeration (x3, printed on every perspective frame), nine camera stations. The camera
always flies and never stands on the ground, which keeps it clear of No.62's kneeling camera on the
same Nenana apron six days ago. Profiles are cut perpendicular to each station's heading.

**D2 THE SQUARE (the motif).** The 1,000 km2 test area (S1-C13), always at true size, always
centred on the FAA point for Nenana Municipal Airport (ENN, -149.0821, 64.5486, from the USGS
National Map airports layer), always gold, and its SHAPE state changes every frame.

**D3 THE STATION CARD.** A mono readout, lower left, data-decorative, computed from the live camera
and never typed: altitude, heading, heights x3. It is proof the camera moved.

### D1 + D2 state table

| # | Station (lon, lat, agl m, heading, pitch, fov) | The square's state |
|---|---|---|
| 01 | AP+0.42, AP+0.17, 2600, 222, -15, 54 | FULL DRAPE, solid gold 2.6 px, near edges crossing the ridge |
| 02 | AP+0.10, AP-0.02, 900, 82 (the bearing to New York), -7, 56 | ONE EDGE, the east edge seen end on as a gold line toward the horizon |
| 03 | AP+0.07, AP+0.045, 700, 228, -24, 52 | ABSENT FROM FRAME, the airport mark only (gold ring and dot on the ground) |
| 04 | AP+0.02, AP+0.34, 6200, 182, -31, 54 | REVEALED WHOLE with a dimension call on its near edge |
| 05 | AP+0.00, AP-0.05, 420, 180, -6, 58 | FROM INSIDE, only the far (south) edge, a gold line across the flats |
| 06 | AP+0.00, AP-0.11, 180, 182, -1, 60 | THE HORIZON EDGE, the south edge faint and near the horizon |
| 07 | plan view, parallel projection | ONE UNIT TILE beside 6.8, the gold original on the map plus a tray of 6.8 fireweed tiles |
| 08 | AP-0.05, AP-0.42, 2200, 2, -12, 54 | PHANTOM, dashed #7E8F95, no gold at all |
| 09 | AP+0.60, AP+0.30, 5200, 230, -16, 52 | GONE, a small gold Polaris on the airport point replaces it |

AP = Nenana Municipal Airport, -149.0821 W 64.5486 N.

## VARIETY LEDGER CHECK, and this deck's required divergence

Last four heroes: the season disc (No.63, machined instrument, parallel oblique), the jurisdiction
section (No.64, orthographic vertical section, NO camera), the waterline hold (No.65, a survey camera
at a water surface with a docket staff), the reading frame plate (No.66, frontal engraved plate, NO
camera). This deck's hero is **NEW: THE AERIAL UNIT OVER REAL GROUND**, a perspective camera flown
over a real digital elevation model, drawn as lit and lee ridgeline profiles. It puts a camera back
into the house after three decks without one, and it is the first deck built on a real DEM.

Atmospheres, last three: Kachemak stratus at low sun, flood tide under high overcast, interior plate
light. This deck: **NEW: BLANK SKY BY RULE.** No page reports the weather on test days, so the sky
carries nothing: no sun disc, no cloud, no smoke. The ground is lit by the cartographer's standard
key, azimuth 315, elevation 30, for all nine frames. The empty sky is where the type goes.

Continuity, last two: docket staff, render state, edge tease; reading frame, engraved ground, struck
slot, scale ladder. This deck: camera move, a shape-changing square, a station card. No edge tease.

Hooks, last three: the vector, the state of matter, the enacted limit. This deck: **NEW: THE THREE
DATELINES**, an itinerary with two stops filled and the third blank.

Palettes, last three: cold navy over warm cut earth; extinction to specular through water, silt and
flour; ink and plate. This deck: **spruce-black, sphagnum and river ice**, green ground with gold for
the exam only.

Type, last two: Unbounded / Instrument Serif / Mono; Fraunces / Manrope / Mono. This deck: **Archivo
(condensed display, normal-width body) over JetBrains Mono.** Two families.

## VARIANCE DIALS

- design_variance **3**: after three extreme abstractions, a camera over real ground is the move.
- visual_density **4**: a field of lit ridgelines is dense by nature.
- type_temperature **2**: cool grotesk, condensed, no serif.

## PALETTE (roles fixed)

| Role | Hex |
|---|---|
| Sky, top to horizon | `#060D12` to `#0B161B` |
| Horizon haze and fog | `#1C2B2C` |
| Ground fill (occlusion) | `#0A1712` |
| Lee stroke | `#1D3325` |
| Lit stroke | `#9FBF8F` |
| Major rivers | `#5AC8F0` |
| Minor flowlines | `#2C6A7E` |
| Gold, the exam and nothing else (square, airport mark, 10 minute gate, Polaris) | `#FFC72C` |
| Phantom, "not stated" (only ever dashed or open) | `#7E8F95` |
| Fireweed, burned area, slide 07 only | `#E2568C` |
| Display type | `#F4F8FF` |
| Body type | `#B3C1C4` |
| Mono | `#8FA2A6` |
| Site fixture | `#46545F` |

Ink law, declared on every frame's `data-ink`: gold means the exam; `#7E8F95` means not stated;
fireweed is absent everywhere except 07.

## TYPE SYSTEM

- Display: Archivo 700, font-stretch 75%, tracking -0.02em, leading 0.96, `AK.fitText` with declared
  maxLines. Cover 128 to 150 px; content headlines 64 to 86 px.
- Body: Archivo 400, stretch 100%, 33 px, leading 1.36, `#B3C1C4`, max width 860 px.
- Mono: JetBrains Mono 500 for kickers (24 px, +0.10em, caps) and lane labels (22 to 24 px); 400 for
  the station card, counter and site fixture (18 to 20 px).

## LOWER THIRD, deck-wide policy

On every perspective frame the lower third IS the nearest terrain: the densest, heaviest lit and lee
profiles, drawn at the widest stroke weights, with draped rivers and minor flowlines. The station card
and site fixture sit on that modelled ground. On 07 the lower third is the plan-view hachure field.

## SITE FIXTURE

`alaskaaihq.com`, JetBrains Mono 400, 18 px, `#46545F`, bottom right at y 1296, data-decorative, on all
nine frames. No "sources in comments" anywhere.

## THE STANDING WEAKNESS, and what is different here

Artwork craft, weakest in 8 of the last 10. The picture is made ENTIRELY of drawn marks whose weight
and tone come from real data: each profile segment's weight and value come from the dot product of
the real terrain normal with the key light, and each river is a real USGS flowline. Take the DEM away
and there is no picture. Every frame has its own station, its own overlays and its own instrument.
The shared ground renderer lives in `assets/js/akvalley.js` as house furniture, and the slide's own
code draws everything that says anything.

## PROTOTYPE FINDINGS, before any slide was committed

1. Latitude-row profiles (the first prototype) read as radiating spokes to any camera not facing due
   south. Profiles are now cut perpendicular to heading.
2. A camera north of Nenana looking south puts featureless flats in the near field; the northeast
   station over the ridge puts real relief in the foreground and the square across the flats beyond.
   Adopted for 01.
3. Draped lines chipped into dashes near the camera, because each piece was depth-tagged at its
   midpoint and nearer profile fills covered it. Pieces are now tagged at their nearer end and
   subdivided finer near the camera.
4. The DEM crop ends about 50 km from Nenana, and the edge read as a mesa on the horizon. Every
   perspective frame runs fog dense enough to lose the crop edge, plus a haze band at the horizon.

## COPY SPINE, claim ids attached

Written in the dossiers below.

## CLAIMS INDEX

| Claim | Slide(s) |
|---|---|
| S1-C01 | 01, 02, 06, 08 |
| S1-C02 | 02 |
| S1-C03 | NOT USED |
| S1-C04 | 02 |
| S1-C05 | 02 |
| S1-C06 | NOT USED |
| S1-C07 | NOT USED |
| S1-C08 | 02 |
| S1-C09 | 02 |
| S1-C10 | 02 |
| S1-C11 | 02 |
| S1-C12 | 04, 05 |
| S1-C13 | 01, 04, 07 |
| S1-C15 | 01, 02 |
| S1-C16 | 01, 03, 08, 09 |
| S1-C17 | 03, 08 |
| S1-C18 | NOT USED |
| S1-C19 | 03 |
| S1-C20 | 04 |
| S1-C21 | NOT USED |
| S1-C22 | NOT USED |
| S1-C23 | NOT USED |
| S1-C24 | NOT USED |
| S1-C25 | NOT USED |
| S1-C26 | NOT USED |
| S1-C27 | NOT USED |
| S1-C28 | 05 |
| S1-C29 | NOT USED |
| S1-C30 | NOT USED |
| S1-C31 | 05 |
| S1-C32 | NOT USED |
| S1-C33 | NOT USED |
| S1-C34 | 05, 06 |
| S1-C35 | NOT USED |
| S1-C36 | NOT USED |
| S1-C37 | 07 |
| S1-C38 | NOT USED |
| S1-C39 | 08 |
| S1-C40 | NOT USED |
| S1-C41 | 01, 08, 09 |
| S1-C42 | 01, 08 |
| S1-C43 | NOT USED |

---

## SLIDE 01 — HOOK

**1. Beat.** Three datelines. Two are filled with a place and a verb and the third is blank, so the
only way to fill it is to swipe. Plants WHO WON, AND DID ANYONE REACH THE GOAL, which 02 pays at once.

**2. COPY, final.**
- Kicker, mono: `XPRIZE WILDFIRE, AUTONOMOUS FINALS` (S1-C15)
- Headline line 1, Archivo 700: `Tested at Nenana.` (S1-C16)
- Headline line 2: `Awarded in New York.` (S1-C01)
- Headline line 3, phantom: `Next stop unnamed.` (S1-C41, S1-C42)
- Tag, mono small: `GOLD SQUARE = THE 1,000 KM² TEST AREA AT TRUE SIZE, PLACED FOR SCALE` (S1-C13)
- Station card, mono: `ALT` and `HDG` values computed [design], `HEIGHTS X3` [design]
- Counter: `01 / 09` [design]; site fixture `alaskaaihq.com` [design]

**3. Reader takeaway.** Alaska was where the fire drones were tested, and the next stop isn't named.

**4. Layout map.** 12 x 8 grid, 80 px margins. Kicker row 1 at y 96. Headline rows 1 to 3, cols 1 to
11, y 140 to 520: line 1 at the fitted display size, lines 2 and 3 at 60 percent of it. Terrain from
the horizon at about y 470 down. Tag at y 1190 cols 1 to 9 on a measured veil. Focal point is the
square's far corner over the flats at about (700, 620). Eye path headline, the gold square, the ridge.
Quiet zone is the sky right of line 1, about a sixth of the frame. One grid violation, the square's
near edges run off the left and bottom of the frame.

**4a. Lower-third treatment.** The lower third carries the nearest and heaviest terrain, the ridge
northeast of Nenana in lit and lee profiles at the widest weights, with the square's two near edges
and the minor flowlines draped across it. Modelled ground from edge to edge.

**5. Depth plan.** Sky gradient (DOM), then the profile stack far to near with exp2 fog, draped rivers
and square flushed between profiles, then the station card and type. Depth cues: occlusion (ridge
over flats), atmospheric perspective (fog), scale gradient (profile spacing uniform in 1/d), depth-
weighted line width, and the single key light. Camera at 2,600 m agl, pitch -15, fov 54, cy 440; the
horizon lands near y 440 + tan(15 deg) x f, and is measured off the render.

**6. Continuity device state.** D1 station 01. D2 FULL DRAPE. D3 card reads the live station.

**7. Technique stack.** NEW: akvalley lit and lee ridgeline profiles (technique 12 on a real DEM,
light az 315 el 30, VE 3, 330 profiles, 480 samples, fog 1/44). Technique 79 cased line on the
square (a 5 px `#0A1712` casing under 2.6 px gold). Technique 84 instrument readout. Grain tile.

**8. Data-in-art mapping.** Square side is the square root of 1,000 km2 (S1-C13), drawn in world
kilometres on the real ground. Rivers are USGS NHD flowlines. Heights are the DEM times 3.

**9. Palette assignment.** As the deck table. Gold on the square and the airport mark only. Worst-case
text contrast is the headline over sky `#060D12`, far above 4.5:1.

**10. Type spec.** Kicker JetBrains Mono 500 24 px. Headline line 1 Archivo 700 stretch 75,
`AK.fitText(el,{min:120,max:156,maxLines:1})`; lines 2 and 3 at 64 to 88 px, maxLines 1 each; line 3
in `#7E8F95`. Tag JetBrains Mono 400 20 px.

**11. Iconography and anchor spec.** Literal anchor, the real ridge and confluence at Nenana. The one
annotation, the tag naming the square. No leaders.

**12. Reference intent.** A survey flight over the Tanana Flats, drawn by a pen plotter.

**13. Risk flags.** Crop edge showing on the horizon, mitigated by fog and haze band. Headline over
terrain, mitigated by pitching so the horizon sits below the headline block.

**14. Acceptance checklist.**
- [ ] The gold square reads as one closed shape at 432 px, with its near edges crossing the ridge
- [ ] Line 3 is visibly quieter (phantom grey) than lines 1 and 2
- [ ] No crop cliff or mesa shape on the horizon
- [ ] The ridge reads as relief at thumb size (lit faces bright, lee faces dark)
- [ ] Gold appears on the square and the airport mark only
- [ ] `alaskaaihq.com` present, small, bottom right

---

## SLIDE 02 — PAY, the verdict

**1. Beat.** Pay the cover at once, names and money. Plants WHERE WAS IT EARNED.

**2. COPY, final.**
- Kicker: `SEPTEMBER 23RD, NEW YORK CITY FIRE MUSEUM` (S1-C01)
- Headline: `Anduril first. Dryad second. AURA third.` (S1-C08, S1-C09, S1-C10)
- Body: `XPRIZE paid $4.55 million across both tracks. The autonomous track was decided in the Alaska finals, and Lockheed Martin's $1 million detection bonus also went to Anduril.` (S1-C02, S1-C15, S1-C11)
- Bar labels: `ANDURIL $1.2 MILLION` (S1-C08), `LOCKHEED MARTIN BONUS $1 MILLION` (S1-C11), `DRYAD $800,000` (S1-C09), `AURA FORESIGHT $500,000` (S1-C10)
- Footnote: `TRACK TOTAL $2.5 MILLION, OR $3.5 MILLION WITH THE BONUS` (S1-C04, S1-C05)
- Station card `HDG 082, TOWARD NEW YORK` [design]

**3. Reader takeaway.** Three companies split the autonomous purse; Anduril also took the bonus.

**4. Layout map.** Kicker y 96, headline y 136 to 330 (2 lines), body y 350 to 520. Bars y 580 to 860
in the sky zone, cols 1 to 10, left-aligned to x 80, labels right of each bar. Horizon near y 900.
Focal point the Anduril bar. Quiet zone upper right.

**4a. Lower-third treatment.** Terrain east of Nenana seen end-on toward New York: the Tanana
floodplain in lit profiles, the river draped and cased, and the square's east edge as a gold line
running toward the horizon. Modelled ground.

**5. Depth plan.** Sky, flat bars (parallel, no perspective, they carry quantities), profile stack,
draped Tanana, the square's east edge. Cues: occlusion, fog, width by depth, scale gradient.

**6. Continuity device state.** D1 station 02 facing 82 degrees. D2 ONE EDGE. D3 card.

**7. Technique stack.** akvalley profiles (fog 1/40); flat bars drawn as canvas paths with a hatched
bonus segment (technique 63 seeded hachure, 41 degrees) so the bonus never merges with the place
award; technique 69 dot rhythm on the footnote rule.

**8. Data-in-art mapping.** Bar length linear in dollars, 300 px per $1M: 360, 300 (hatched, bonus),
240, 150. Declared on `data-scale`.

**9. Palette assignment.** Bars in `#B3C1C4` outline with `#9FBF8F` fill at 55 percent; bonus hatched
`#B3C1C4`. No gold on bars (gold is the exam, not money).

**10. Type spec.** Headline Archivo 700 stretch 75, fitText min 64 max 92 maxLines 2. Body 33 px.
Labels JetBrains Mono 500 22 px.

**11. Iconography and anchor spec.** Anchor the Tanana running east. Annotation, the bar scale.

**12. Reference intent.** A results board hung over the valley the results came from.

**13. Risk flags.** Bars reading as a HUD pasted over a landscape; mitigated by a haze veil behind
them and a baseline rule tied to the horizon.

**14. Acceptance checklist.**
- [ ] Anduril's two awards are two separate segments, never one total
- [ ] Bar lengths are in ratio 1.2 : 1 : 0.8 : 0.5
- [ ] The footnote states both track totals
- [ ] No gold on money
- [ ] Terrain carries the lower third

---

## SLIDE 03 — PLACE, the airport

**1. Beat.** Where it happened, close. Plants WHAT DID THE MACHINES HAVE TO DO.

**2. COPY, final.**
- Kicker: `NENANA MUNICIPAL AIRPORT, JUNE` (S1-C17, S1-C16)
- Headline: `The exam was flown from Nenana's airport` (S1-C17)
- Body: `For two weeks in June the finalists flew from Nenana Municipal Airport. UAF's drone center, ACUASI, managed the airspace. The test site lay along the Nenana-Totchaket Road corridor.` (S1-C16, S1-C17, S1-C19)
- Labels: `NENANA MUNICIPAL AIRPORT` (S1-C17), `TANANA RIVER`, `NENANA RIVER` (place names from USGS NHD)

**3. Reader takeaway.** The finals ran out of a small airport on the Tanana, with UAF running the sky.

**4. Layout map.** Kicker y 96; headline y 136 to 330; body y 350 to 560. Terrain from about y 600.
The airport's two runways (FAA polygons) sit near (560, 900). Leader from the label at (120, 700) to
the runway centre. River labels on the water. Quiet zone upper right.

**4a. Lower-third treatment.** The ground at the confluence close up and at its heaviest: the ridge's west flank in the widest lit and lee profiles of the deck, the Tanana and Nenana rivers cased and draped across it, the airport's two runways and the town's streets drawn as real USGS geometry. Modelled ground edge to edge, nothing flat.

**5. Depth plan.** Low oblique at 700 m agl; occlusion by the ridge flank; fog; width by depth.

**6. Continuity device state.** D1 station 03. D2 ABSENT, the airport mark only. D3 card.

**7. Technique stack.** akvalley profiles (fog 1/30, 360 profiles for the close range); runway
polygons draped as filled and cased shapes; town streets from USGS local roads as 0.6 px hairlines;
technique 72 leader, declared on `__akLeaders`.

**8. Data-in-art mapping.** Runways, streets, rivers all real geometry.

**9. Palette assignment.** Runways `#B3C1C4` fill cased `#0A1712`; the airport mark gold ring. Rivers
per deck.

**10. Type spec.** Headline fitText min 60 max 84 maxLines 2. Labels JetBrains Mono 500 22 px on
veils.

**11. Iconography and anchor spec.** Anchor, the two runways of ENN. Annotation, the leader.

**12. Reference intent.** An approach plate for a place most readers have driven past.

**13. Risk flags.** Faceting of the 197 m DEM near the camera; mitigated by 700 m agl and dmin 1.2 km.

**14. Acceptance checklist.**
- [ ] Two runways visible, parallel as built (ENN 04L/22R and 04R/22L)
- [ ] The leader lands on the runway (qa leader gate)
- [ ] Both rivers labelled on their own water
- [ ] No text over busy art without a veil

---

## SLIDE 04 — TASK, the square revealed

**1. Beat.** The size of the exam and its clock. Plants DID ANYONE BEAT THE CLOCK.

**2. COPY, final.**
- Kicker: `THE TASK, AS XPRIZE SET IT` [design]
- Headline: `One fire. Ten minutes. 1,000 square kilometers.` (S1-C12, S1-C13)
- Body: `Each team's machines watched alone for 8 hours. The goal was to detect and fully suppress a high-risk fire within 10 minutes of ignition.` (S1-C20, S1-C12)
- Dimension call: `31.6 KM` [design] (the side of the drawn square, root of S1-C13, declared in aggregates.json)
- Tag: `TRUE SIZE, CENTERED ON THE AIRPORT FOR SCALE. NO SOURCE GIVES THE BOUNDARY.` (S1-C13)

**3. Reader takeaway.** The exam covered a square the size of most of the Tanana Flats in view.

**4. Layout map.** Kicker y 96, headline y 136 to 330, body y 350 to 560. Square from y about 640 to
1180. Dimension call on the near edge. Tag at y 1200.

**4a. Lower-third treatment.** The square's near edge and the flats inside it, drawn as lit and lee profiles at the frame's widest weights, with the Nenana River and the minor flowlines draped across the square and the dimension call and its extension lines set on that modelled ground rather than on a plate.

**5. Depth plan.** High oblique, 6,200 m agl, pitch -31. Fog lighter (1/60). Cues as deck.

**6. Continuity device state.** D1 station 04. D2 REVEALED WHOLE. D3 card.

**7. Technique stack.** akvalley profiles; technique 73 dimension call on the square's near edge,
extension lines drawn from the projected corners; technique 79 cased square.

**8. Data-in-art mapping.** Square side root 1,000 = 31.62 km; the dimension call reads the side in
kilometres, declared.

**9. Palette assignment.** Gold square and gold dimension call; the tag in mono.

**10. Type spec.** Headline fitText min 60 max 86 maxLines 2.

**11. Iconography and anchor spec.** Anchor the square on real ground. Annotation, the dimension call.

**12. Reference intent.** A range card for an exam.

**13. Risk flags.** The square reading as a claimed boundary; the tag says it is not.

**14. Acceptance checklist.**
- [ ] The whole square is in frame
- [ ] The dimension call's ends land on the square's corners
- [ ] The honesty tag is legible at full size
- [ ] Gold only on the square and the call

---

## SLIDE 05 — TURN, the scorecard

**1. Beat.** What the record says about the clock. Plants SO WHERE DOES THE PRIZE STAND.

**2. COPY, final.**
- Kicker: `THE RECORD, AGAINST THE CLOCK` [design]
- Headline: `One 10 minute gate is on the record, for detection` (S1-C31)
- Body: `XPRIZE says AURA met the 10 minute detection gate. Dryad says it detected and verified the fire in 12 minutes or less. XPRIZE's release doesn't say any team fully suppressed a fire inside 10 minutes.` (S1-C31, S1-C28, S1-C34)
- Lane labels: `THE GOAL, DETECT AND SUPPRESS, PER XPRIZE` (S1-C12), `AURA, DETECTION, PER XPRIZE` (S1-C31), `DRYAD, DETECT AND VERIFY, PER DRYAD` (S1-C28), `SUPPRESSION IN 10, NOT IN XPRIZE'S RELEASE` (S1-C34)
- Axis: `IGNITION` [design]
- Axis: `10 MIN` (S1-C12), `12 MIN` (S1-C28)

**3. Reader takeaway.** Detection inside 10 minutes happened on the record; suppression didn't.

**4. Layout map.** Headline and body y 96 to 520. Four lanes y 580 to 880, axis at 60 px per minute
from x 120 (0) to x 840 (12). Gold gate rule at 10. Horizon near y 930.

**4a. Lower-third treatment.** Inside the square and low: the flats south of the airport as a foreground plane of dense lit and lee profiles at the heaviest weights, graded by the key light, with the Nenana River and minor flowlines draped through them and the square's far edge as a thin gold line lying on that modelled ground near the horizon.

**5. Depth plan.** 420 m agl, pitch -6, fog 1/34. Lanes flat.

**6. Continuity device state.** D1 station 05. D2 FROM INSIDE. D3 card.

**7. Technique stack.** Lanes as canvas paths: AURA a solid bracket closing at 10 with an open left
end (no time published), Dryad a hatched bracket closing at 12 with an open left end ("or less"),
suppression a dashed phantom box with no end cap. akvalley profiles below.

**8. Data-in-art mapping.** 60 px per minute, declared on `data-scale` with every mark.

**9. Palette assignment.** Gold only on the 10 minute gate rule and the square edge. Phantom grey on
the empty lane.

**10. Type spec.** Headline fitText min 58 max 80 maxLines 2. Lane labels JetBrains Mono 500 22 px.

**11. Iconography and anchor spec.** Anchor the square's far edge on the ground. Annotation, the axis.

**12. Reference intent.** A race timing sheet with one line left blank.

**13. Risk flags.** Readers taking the Dryad bracket as a measured start; the open end and "per Dryad"
say otherwise.

**14. Acceptance checklist.**
- [ ] Gate rule at exactly 10 on the axis
- [ ] AURA's bracket touches the gate; Dryad's ends at 12
- [ ] The suppression lane is visibly empty and dashed
- [ ] Every lane says who says so

---

## SLIDE 06 — BREATHER

**1. Beat.** Rest, on the one quote that sets the tone. Plants HOW BIG IS THE PROBLEM.

**2. COPY, final.**
- Quote: `"The final prize remains on the horizon"` (S1-C34)
- Attribution: `ADAM BROECKER, LOCKHEED MARTIN, SEPTEMBER 23RD` (S1-C34, S1-C01)

**3. Reader takeaway.** Even the sponsors say the goal hasn't been reached.

**4. Layout map.** The quote set on two lines just above the real horizon at about y 760; attribution
below the horizon on a veil at y 1120. Everything else is terrain and sky.

**4a. Lower-third treatment.** BREATHER, the deck rests on the one quote after four dense frames, and
the frame is otherwise the flats running to the foothills. `data-breather` is set. The lower third is
still modelled ground, low profiles at heavy near weights.

**5. Depth plan.** 180 m agl, pitch -1, fov 60, fog 1/30 so the crop edge is lost in haze.

**6. Continuity device state.** D1 station 06. D2 THE HORIZON EDGE. D3 card.

**7. Technique stack.** akvalley profiles, 380 profiles for the low grazing view.

**8. Data-in-art mapping.** The literal horizon under the quote is the real southern skyline.

**9. Palette assignment.** Quote snow; gold only on the faint square edge.

**10. Type spec.** Quote Archivo 300 stretch 75, fitText min 64 max 96 maxLines 2.

**11. Iconography and anchor spec.** Anchor, the horizon itself.

**12. Reference intent.** A film still with a title card.

**13. Risk flags.** Quote reading as the deck's own claim; attribution directly under it.

**14. Acceptance checklist.**
- [ ] Quote sits above the terrain skyline without touching it
- [ ] Attribution legible
- [ ] data-breather declared

---

## SLIDE 07 — DATA, keepable

**1. Beat.** The scale comparison worth saving. Plants WHAT COMES NEXT, AND WHERE.

**2. COPY, final.**
- Kicker: `THE SCALE XPRIZE CITED` (S1-C37)
- Headline: `Alaska's 2025 fires covered nearly seven test areas` (S1-C37, S1-C13)
- Body: `XPRIZE estimates Alaska's 2025 season burned 1.68 million acres. That is about 6,800 square kilometers, the 1,000 km² test area nearly seven times over. The tiles show area only, not where anything burned.` (S1-C37, S1-C13) [design] the 6,800 is 1.68 million acres times 0.0040469 square kilometers per acre, declared as a ratio in aggregates.json
- Labels: `1 TEST AREA, 1,000 KM²` (S1-C13), `NENANA` [design], `20 KM` [design]
- Tag: `AREA ONLY, NOT WHERE IT BURNED` [design] restates the body's area-only caveat on the tray itself (risk flag 13)
- Label: `2025 BURN, ABOUT 6.8 TEST AREAS` [design] the ratio 6,799 over 1,000 from S1-C37 and S1-C13, declared in aggregates.json

**3. Reader takeaway.** One Alaska season is about seven of the areas the drones were tested on.

**4. Layout map.** Headline and body y 96 to 470. Plan-view hachure map y 500 to 1240. The gold
test square at the airport, plus a tray of 6.8 fireweed tiles (6 full, one 0.8) laid in rows beside it. Scale bar inside the map, lower left.

**4a. Lower-third treatment.** The plan-view slope-and-aspect hachure of the real DEM, whose stroke width is local slope and rotation local aspect, with the rivers cased over it. The lower tiles, the scale bar and the station card sit on that hachured relief, never on bare ground.

**5. Depth plan.** Parallel projection, deliberately: the frame carries a quantity. Depth by hachure
relief shading and cased river lines.

**6. Continuity device state.** D1 plan. D2 ONE UNIT TILE. D3 card reads `PLAN VIEW, NO CAMERA`.

**7. Technique stack.** Technique 92 akhachure on the real DEM, cell 8, 4 passes, sun az 315 el 30.
Tiles as cased outlines with a fireweed stipple fill (technique 66, dots per tile fixed).

**8. Data-in-art mapping.** Tile side = the test square's side at map scale. 6.80 tiles =
1.68 million acres x 0.0040469 / 1,000. Declared in aggregates.json.

**9. Palette assignment.** Gold original tile; fireweed tiles; rivers ice.

**10. Type spec.** Headline fitText min 58 max 80 maxLines 2.

**11. Iconography and anchor spec.** Anchor, Nenana and the confluence in plan. Annotation, scale bar.

**12. Reference intent.** A USGS quad with a fire officer's pencil tiles on it.

**13. Risk flags.** Tiles read as burn locations; the body and a mono tag say area only.

**14. Acceptance checklist.**
- [ ] Exactly one gold unit square on the map and 6.8 fireweed tiles in the tray (the last one 0.8 of a tile)
- [ ] Scale bar reads 20 km against the map
- [ ] "Area only" stated on frame

---

## SLIDE 08 — ESCALATE

**1. Beat.** What comes next names no Alaska place. Plants SHOULD THAT CHANGE.

**2. COPY, final.**
- Kicker: `AFTER NENANA` [design]
- Headline: `What comes next names no Alaska address` (S1-C41, S1-C42, S1-C39)
- Body: `XPRIZE now moves to a 12 to 15 month Impact Phase to turn these systems into deployable tools. Dryad plans pilots in 2027 and names no location. The only Alaska institutions in the record are UAF and ACUASI.` (S1-C41, S1-C42, S1-C39)
- Timeline labels: `SEPTEMBER 23RD` (S1-C01), `IMPACT PHASE, 12 TO 15 MONTHS` (S1-C41), `DRYAD PILOTS 2027, NO PLACE NAMED` (S1-C42)
- Tick labels: `12 MO`, `15 MO` [design] the Impact Phase ends on the month axis (S1-C41)

**3. Reader takeaway.** The next stage is set; Alaska isn't in it on paper.

**4. Layout map.** Text y 96 to 540; flat timeline y 600 to 700 across cols 1 to 11; horizon near y
760; the phantom square on the flats below.

**4a. Lower-third treatment.** Reverse shot from the southern foothills looking north: the foothills' lit and lee profiles are the heaviest marks in the frame and fill the lower third, with the Nenana River running north out of them toward the flats and the phantom square beyond.

**5. Depth plan.** 2,200 m agl over the foothills, heading 2, pitch -12.

**6. Continuity device state.** D1 station 08. D2 PHANTOM. D3 card.

**7. Technique stack.** akvalley profiles; phantom square as a dashed drape; timeline as a flat
measured axis with feathered ends for the 12 to 15 month range.

**8. Data-in-art mapping.** Timeline months linear, declared on `data-scale`.

**9. Palette assignment.** No gold anywhere; phantom grey square.

**10. Type spec.** Headline fitText min 60 max 86 maxLines 2.

**11. Iconography and anchor spec.** Anchor, the foothills and the flats.

**12. Reference intent.** Looking back at a place you are leaving.

**13. Risk flags.** Foothills are near the crop's south edge; the camera sits inside the crop.

**14. Acceptance checklist.**
- [ ] No gold on the frame
- [ ] The square is dashed grey
- [ ] Timeline marks all declared

---

## SLIDE 09 — CLOSE

**1. Beat.** One ask.

**2. COPY, final.**
- Kicker: `NEXT STOP, UNNAMED` [design] in phantom grey, the cover's blank third dateline echoed on the close
- Headline: `Alaska hosted the exam. Should it get a seat in the Impact Phase?` (S1-C16, S1-C41)
- Mono: `ANSWER IN THE COMMENTS` [design]
- Wordmark `ALASKA.AI` and Polaris [design]

**3. Reader takeaway.** Should Alaska ask for a seat?

**4. Layout map.** Headline y 180 to 520; the pulled-back valley below; the gold Polaris on the
airport point; wordmark lower left above the site fixture.

**4a. Lower-third treatment.** The ridge northeast of Nenana from the farthest station of the deck: its lit and lee profiles at heavy near weights fill the lower third, with the Tanana draped across the flats beyond and the gold Polaris sitting on the airport point in the middle distance.

**5. Depth plan.** 5,200 m agl, heading 230, pitch -16.

**6. Continuity device state.** D1 station 09. D2 GONE, the Polaris on the airport. D3 card.

**7. Technique stack.** akvalley profiles; Polaris drawn as a four-point star with arcs.

**8. Data-in-art mapping.** None new; the place is the data.

**9. Palette assignment.** Gold only on the Polaris.

**10. Type spec.** Headline fitText min 64 max 92 maxLines 3.

**11. Iconography and anchor spec.** Anchor, the airport point.

**12. Reference intent.** The last frame of a survey film.

**13. Risk flags.** None beyond the deck's.

**14. Acceptance checklist.**
- [ ] One ask only
- [ ] Polaris on the airport point
- [ ] No source note on the slide

## BUILD RECONCILIATION

Every dossier number the build changed, written before any critic was spawned.

- **Cameras are solved, not typed (slides 03 to 09).** `AKV.aim` in `assets/js/akvalley.js` places the
  camera `distKm` back from a target along the heading, `agl` above the ground there, and searches
  pitch and principal point so the target lands on a chosen screen row and the ground `farKm` ahead
  on another. The station table's lon/lat/pitch numbers for 03 to 09 are superseded by these solves:
  03 target the airport, heading 112 (not 228), 9 km, 1,300 m agl, fov 46; 04 heading 182, 56 km,
  9,000 m, fov 44; 05 target the square's south edge, heading 180, 11 km, 480 m; 06 target the
  foothills at 64.19 N, heading 182, 30 km, 240 m, solved against the quote's own bottom edge;
  08 heading 2, 44 km, 420 m, fov 56; 09 heading 226, 30 km, 3,600 m, fov 50. Slides 01 and 02 keep
  typed stations: 01 at AP+0.42/AP+0.17, 2,600 m, heading 222, pitch -21, cy 930; 02 moved to
  AP-0.22/AP+0.02, 1,500 m, heading 82, pitch -16, cy 1060, so the ridge and the Tanana sit under the
  purse instead of bare flats.
- **Slide 02's square state** is the square's east edge seen as a line across the frame, not end on.
- **Slide 03's station** was re-cut three times: a close station over the ridge posterized the near
  relief, a north station put a hill in the foreground. The shipped station looks east-southeast
  across the Tanana at town, airport and confluence with the ridge behind.
- **Slide 04's dimension call** moved from the square's near edge (its corners fall off-frame at this
  station) to the FAR (south) edge, the one edge wholly in frame, with the label on a veil because a
  terrain profile ran through it.
- **Slide 06** has no retraced skyline. The retrace sampled sparsely and drew spikes; the skyline is
  now measured only, and the slide asserts the quote sits above it (qa.py PASS).
- **Slide 07** runs at 5 px per km, not 4, with the tray in rows of two (3 rows plus a 0.8 tile)
  instead of three, so the map and tiles fill the lower third.
- **Slide 08's station** moved into the southern foothills at low altitude so the foothills fill the
  near field; the phantom square is dashed `#9AAAB0`, not `#7E8F95`, for legibility at feed scale.
- **Copy** changed on 02 (tightened body), 04 and 05 (copywriter corrections for the word budget), 05
  kicker `THE RECORD, AGAINST THE CLOCK`, and authored `<br>` breaks on 03, 05, 06, 08, 09 per
  qa.py's ragged-line warnings. All mirrored into the COPY blocks above.
- **Labels are 24 px** (the mobile floor), not 20 to 22; the counter is decorative furniture.
- **Station card** reads `HEIGHTS X3   ALT ... M   HDG ...` so the heading number is not read as a count.
- **akvalley.js** gained, during the build: nearer-end depth tags and finer steps for draped lines,
  `V.overlay` (line-of-sight clipped overlays, pieces joined so dashes run continuously), `V.aim`, fog
  quantised to eighths (the ink census cap), and 9 lit buckets instead of 5 (posterized near relief).

### Phase 8, round 1 (five pixel critics: 01 6.4, 02 7.2, 03 6.4, 04 7.2, 05 6.4, 06 7.0, 07 6.8, 08 5.9, 09 7.0)

- **Renderer, every perspective frame.** The critics' shared defects were strokes across the station
  card and site fixture, flats that read as ruled stripes, and the DEM crop edge reading as a mesa.
  akvalley.js gained: `spacing` (profiles uniform in d^-p, so gaps open toward the camera) with
  `minGap` pruning; `widthPow` (weight by nearness in 1/d); `relief` plus `contrast` (lighting only,
  from DEM minus a 5 cell box blur, so real sloughs and terraces print as lit and lee patches; the
  geometry stays x3); `haze` (dmax held inside the crop via `V.cropDepth`, the last quarter fading
  wholly to the fog ink over a feathered fog floor); `V.overlay` `minRun` and `hidden`; and
  `AKV.quietCanvas`, a feathered knockout the build shell runs behind `.card`, `.foot` and `.quiet`
  after every slide draws. The card is `white-space:pre` so its triple spacing renders.
- **01** hairline haze band removed (it was the hard-topped slab); `GOLD SQUARE` in the tag set white,
  so gold is on the square and airport mark only; the tag sits on a feathered knockout, not a plate.
- **02** place bars solid sphagnum fill with a `#B3C1C4` outline, the bonus alone hatched; the axis
  rule runs to $2.5M past the longest row, ticks still at $0, $1M, $2M; orphan gold fragment removed.
- **03** runways drawn after the ring, filled `#B3C1C4`, cased 4 px, held to 4 px across; the ring
  widened to 0.95 km radius so it holds both. The dossier's "crossed" was wrong: ENN's two runways
  are parallel (04L/22R and 04R/22L), and the checklist line is corrected. The railroad is solid,
  since a dash means "not stated" in this deck. `Nenana-Totchaket` no longer breaks at its hyphen.
- **04** re-solved to 70 km, fov 50, airport row 900, so the square is revealed WHOLE; a small cased
  white cross marks the airport (not gold), so "centered on the airport" can be checked on the frame.
- **05** lane labels now say who says so: `THE GOAL, DETECT AND SUPPRESS, PER XPRIZE` and
  `SUPPRESSION IN 10, NOT IN XPRIZE'S RELEASE` (COPY block updated). The dotted lead-ins and hard bar
  starts are gone: AURA and Dryad fade in from ignition, so no start time is implied. Minute ticks
  1 to 11 are drawn and declared in data-scale. The square's edge sits just under the horizon, thinner.
- **06** the attribution sits directly under the quote, and the slide asserts quote AND attribution
  clear the measured skyline. Camera at 44 km, so the square's south edge lies near the horizon.
- **07** NENANA sits on the town with a leader to the airport dot; minor flowlines removed (their pull
  covers the square's neighbourhood only, which showed as an edge in plan); hachure clipped to the
  neatline and weighted by slope (flats emptier than the ridge); scale bar inside the map; new tag
  `AREA ONLY, NOT WHERE IT BURNED` in the empty tray cell; body at the 860 cap. D2 text now says a
  tray of 6.8 tiles, not 5.8.
- **08** re-solved at 1,000 m agl, 40 km, target 0.12 degrees west, so the Nenana crosses the flats
  and the phantom square reads closed; timeline ticks reduced to 0, 12 and 15 (declared marks match),
  `SEPTEMBER 23RD` starts on its origin tick, 12 and 15 centred on theirs; the Dryad span is a faint
  fill between offset dashes. Body at 860.
- **09** CTA in `#B3C1C4`, so gold is on the Polaris alone; the wordmark on a feathered knockout;
  camera 24 km; the Polaris is 1.3x with two open arcs, and its stem ends in a cased ring on the ENN
  ground point (the floating dot is gone).

### Phase 8, round 2 (critics: 01 6.9, 02 7.3, 03 7.4, 04 5.6, 05 6.6, 06 7.0, 07 7.1, 08 6.6, 09 7.6)

- **Renderer.** `quietFlat` draws the shade buckets nearest flat ground's own value at 0.3 alpha,
  so the floodplain stops reading as ruled paper and only its real relief prints; every perspective
  frame now runs spacing 0.6, minGap 3, relief 20, contrast 3.2 to 4. `haze.fadeFrom` sets where
  the last fade begins. `V.overlay` counts only on-screen length toward `minRun`. The quiet pad
  widened to 22 by 10 px, feather 10.
- **01** camera pulled back and up (AP+0.6 / AP+0.25, 3,600 m, pitch -19, cy 880): the near NE
  corner is now in frame, so the square reads closed with two corners cropped. Tag moved to y 1204.
- **02** heading 78 (card updated), so the square's east edge recedes on a diagonal instead of
  reading as a chart baseline; the left stub is culled (minRun 240 on-screen px). The Anduril joint
  is a dark seam, not a gap, so both awards keep full length. `$0` sits on its tick; the footnote
  moved to y 822.
- **03** the airport label sits in the flats ABOVE the ring on a straight leader, clear of both
  rivers; ring radius 1.35 km so it encloses the long runway.
- **04** round 1's re-solve put the camera 70 km north, off the DEM (it ends about 50 km north of
  Nenana), and the haze took the whole ground. Re-solved at 48 km, 9,000 m, fov 58 (probed in node
  first): all four corners in frame, asserted in the slide. Fog 1/140, the major rivers less fogged.
  The dimension line is dead level.
- **05** the gold gate runs in two pieces around lane 4's label; AURA is a ramped filled bar, the
  brightest mark; the goal lane is a thin spec bracket; the horizon re-solved below the chart
  (yFar 952); axis labels on feathered knockouts cut BEFORE the axis is drawn (a knockout after it
  cut a gap that qa read as an undeclared mark). Body at 860.
- **06** a re-aim at the square's edge put the camera beside the hills north of town; reverted to
  round 1's station at 120 m agl instead, so the gold edge lies about 34 px under the flats' far
  edge, in front of the foothill silhouette. River pieces below row 1270 dropped. Quote mark hung.
- **07** the map is cropped to the reach the river data covers (-149.80 to -148.32, 64.26 to 64.90,
  about 71 km square), so every river exits at the neatline; the tray runs in rows of three beside
  it; the map ground is opaque and the slide's sky flat (no horizon glow in a plan view); hachure
  brighter (alpha 0.6, cell 5); NENANA sits right of the airport dot, haloed; the scale bar is
  cased on the hachure, no plate; card `PLAN VIEW, NO CAMERA, NORTH UP`; `1.68&nbsp;million`.
- **08** a level camera 50 km south at 3,200 m, fov 70, cy 884 (the aim solver kept choosing a
  steep pitch with a huge lens shift): the phantom square is closed and wholly in frame (asserted).
  Tick labels `12 MO` and `15 MO`; the Dryad fill at 0.18.
- **09** a feathered disc of air behind the Polaris so no river touches it; arcs 1.7 px at 0.88.

### Phase 8, round 3 (critics: 01 8.3 ship, 02 7.3, 03 8.0 ship, 04 7.3, 05 8.1 ship, 06 7.6, 07 7.5, 08 6.9, 09 8.2 ship; flow 7.5)

- **Renderer.** Each profile's lateral reach is now sized by CAMERA-SPACE depth, not horizontal
  distance, so a high pitched-down camera (04) no longer leaves bare wedges at the lower corners.
  quietFlat alpha is 0.12 to 0.2 per frame.
- **02** heading restored to 82, the true bearing the card names; the scene drops 100 px (cy 1160)
  so the square's east edge lies about 175 px under the footnote and can't read as a gold underline
  on money. The critic's "use the south edge" can't apply: the camera stands inside the square
  looking east, so the south edge is behind it (probed in node). minRun 300 culls the north edge's
  hill-crest fragment.
- **03** body trimmed to three short sentences (flow critic: 02 to 05 were four dense frames in a
  row); label plates are feathered knockouts.
- **04** body trimmed to two sentences, dropping the decoys line (S1-C14 leaves the claims index;
  the goal line, S1-C12, stays because 05 depends on it); the tag is a feathered knockout.
- **05** `12&nbsp;minutes or&nbsp;less` keeps the caveat whole; ground dropped 35 px; minute
  graduations heavier (qa's axis census read them as texture).
- **06** only the fogged far reaches of the major river remain (the near hook is gone).
- **07** kicker `THE SCALE XPRIZE CITED` (S1-C37), tying the season to the prize after the breather;
  rivers stroked as one path, casings first, so no reach reads dashed; NENANA inside the square
  under the dot; scale bar to the map's lower right, label above it; chart group up 50 px. The
  station card sits on bare ground below the map by design: the map is fixed to the river reach.
- **08** a closer camera was probed and puts the near corners out of frame, which would undo
  round 2's closed square, so the 50 km station stays; its flats are quieted harder instead.
- **09** kicker `NEXT STOP, UNNAMED` in phantom grey, echoing the cover's blank third dateline.
- Declined: re-ordering headings into one continuous turn (the flow critic itself judged the one
  scene holds; the stations are cuts, which the card states); a caption rewrite to match the slide
  question word for word (the caption's close and the slide's ask are one question about Alaska's
  place in what comes next, and the caption passed its room and linter).

### Phase 8, round 4 (critics: 01 8.4, 02 8.0, 03 8.1, 04 8.2, 05 8.2, 06 8.0, 07 8.2, 09 8.2 all ship; 08 7.0 revise)

- **Renderer.** `shadeSmooth` averages the shade along each profile before bucketing, so DEM
  micro-noise can't split a flat profile into short lit and lee pieces.
- **08** relief 6, contrast 1.8, shadeSmooth 6, quietFlat 0.35, widthPow 0.9: the ground reads as
  quiet continuous tone under fog and the phantom square is the only dashed shape on the frame. A
  steeper pitch was probed: with the square's far edge pinned it is equivalent to a lens shift and
  the bottom row stays about 14.5 km out, over flats; the southern foothills lie mostly beyond the
  DEM's south edge (64.05 N). Dossier 4a's "foothills fill the lower third" is amended to "the
  flats south of the square, quiet, with the Nenana running north through them".
- **02, 03** body blocks at the 860 px cap.
- Declined as polish, recorded so a later run doesn't treat them as open: 04's near-right corner at
  66 px from the edge (inside the frame, asserted); 07's bare band under the map (the map is fixed
  to the river reach); 09's river interrupted behind the wordmark knockout.

### Phase 8, round 5, the last edit round the cap allows (critics: 02 8.0 ship, 03 8.1 ship, 08 6.9 revise)

- **Renderer.** `tonal {nearKm, lee, lit}`: near profiles fill their band with shaded tone, a column
  per segment bucketed like the strokes, fading into the plain ground ink with distance and
  quantised to steps of 6 per channel (unquantised it hit qa's 160-ink paint census on 08).
- **08** the smoothed ground of round 4 read as an empty void. It now carries tonal lit and lee
  surface from the real DEM out to 34 km, fading into fog, with faint strokes; the draped Nenana
  tapers with depth (depthRef 22). The phantom square stays the only dashed shape.
- Per the five-round cap this is the ship round. Remaining polish recorded, not fixed: 02's body
  widow on "Anduril." and the square edge's blunt start; 03's far flats band; 08's far-edge dash
  cadence over a crest.

### Phase 10, scoring cycle 1 repair (scorer 8.29, weakest artwork craft, named slide 08)

- **08** the round 5 tonal fill stepped with the DEM's 200 m cells into blocks. The near band below
  the square is now a feathered 6 px blur of that real lit and lee tone, reading as an
  out-of-focus foreground, and the Nenana is redrawn on its own layer, fading out toward its
  southern end, where the NHD pull stops. Re-reviewed: 6.9 to 7.2 before the fade.
- The PDF document title now matches the cover's casing, `Next stop unnamed.`
- Noted for Phase 12, not changed in-run: the rubric's ten weights sum to 1.10 and have since the
  rubric was written (July 8th), so every shipped score and every threshold uses that basis.
  8.29 as written is 7.54 normalised.

### Phase 12, Codex review of b92f8e1 (five findings)

- **P1 claims.json carried the runner-up stories** (S2 SB 250 and the governor candidates, S3 the
  Air Force EUL), and the site publishes every claim in that array. Fixed: the shipped record holds
  the 43 S1 claims; the full research is kept at out/2026-09-24/claims_all_stories.json.
- **P2 the quote's attribution never reached the serialized story.** Fixed with no builder change:
  slide 06's body is the attribution exactly as rendered, so the article, feeds, llms-full.txt,
  JSON-LD and alt text carry it (copy_sync matches it against the render).
- **P2 the questions-page chip check compared counts.** Fixed: `check_questions_page` pairs each
  chip with the docket link beside it and compares (item, date) pairs; self-test C reconstructs a
  dropped window plus a repeated one with the same count and dates, and it goes red.
- **P2 cropDepth did not use the drawn span.** Fixed: `V.profileDepth` is shared by terrain() and
  cropDepth(). Declined in part, on measurement: cropDepth keeps the in-frame span (x1.08), not
  terrain()'s 1.25 overscan, because a run cut outside the frame is not seen. All nine renders are
  byte-identical after the change.
- **P1 "ship marked done with Gmail pending".** Reviewed commit b92f8e1, before Phase 12. The
  routine puts the Gmail draft AFTER the merge by design (its image URLs point at main, and
  gmail_draft_id.txt is the one post-merge commit); the upgrade and retro landed in 3d019a1b.

### Phase 12, CI red on b92f8e1: the ask box stress suite (2 of 254)

- Reproduced locally; main is clean on the same test, so this PR's docket changes caused both.
- "what is the capital of france" matched SB 250: its location read "Juneau, Alaska State
  Capitol", and the engine's fuzzy matching reads "capitol" as "capital". The location is now
  "Juneau".
- "which agency has the most decisions" answered THE ALASKA LEGISLATURE. That is TRUE: SB 250 gave
  the Legislature 4 tracked decisions against DNR's 3. The test's /DNR/ expectation was a fact
  about the record, now updated with a dated comment.
- Every ask.yml step re-run locally: engine and corpus self-tests, worker tests, site build,
  sign-off (WARN on the documented upstream Gas Watch block only), ask_engine 254 clean,
  home_ask 29 clean, docket_ask 55 clean.

### Phase 12, Codex review of 9fd1ea9 (five findings)

- **P1 the Eielson COMMENT NOW button linked the June 2025 procurement article** (sources[0]).
  Fixed: KUAC's September 20th report, which carries the comment channel, is the item's first source.
- **P2 the Eielson Event claimed a 2025 start.** Fixed: the September 20th milestone reads "Public
  comment opens ...", so window_open_date resolves 2026-09-20 (verified in the built JSON-LD).
- **P2 V.visible sampled 48 fixed steps.** Fixed: half a DEM cell per step along the ground track.
  Measured effect: slides 02 and 08 changed. 02 is visually identical (edge pixels). On 08 the
  denser test correctly found the ridge hiding part of the phantom square's far edge; a phantom is
  not a physical thing on the ground, so it now draws with the new `los: false` and stays closed.
  Webps, thumbs, PDF and contact sheet refreshed; qa PASS.
- **P2 akv_probe near-field width** now uses V.profileDepth, as terrain() does.
- **P2 akv_probe rounding**: geographic keys keep 1e-5 degrees and `--expr` prints full precision.

### Phase 12, Codex review of 109d180 (three findings, all fixed)

- akv_probe measures the camera's own W and H (they may be set inside `aim` or `camera`).
- akvalley caches the blurred DEM per relief radius (every slide uses the default 5; renders
  byte-identical).
- ledger/topics.json records 43 claims for No.67, matching the pruned record.
- CI note: none of this session's git pushes triggered the PR workflows (only the PR opening
  did, and workflow_dispatch answers 403 for this integration). A commit made through the GitHub
  API is how CI reaches the current head; recorded in automation_retro.md.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-09-24. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[PASS] qa.py          PASS, 0 fails, 0 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 212 line(s), 18404 chars
[PASS] caption_check  PASS, 878 chars, hook 134, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 58 authored slide strings all present in the render; alaskaaihq.com on every slide; no banned slide string
[PASS] aggregate      aggregate_check: PASS -- 15 aggregate assertion(s) detected, 17 declared -> out/2026-09-24/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 42 claims indexed, 0 declared counts checked, 6 body quote(s) checked, 0 drift(s)
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.284 (fail at 0.60), max pair 0.409, drawn share 85% (50 drawn vs 9 blocky,
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] ledger_guard   LEDGER GUARD: PASS, 7 cron-written file(s) untouched
[PASS] docket_dates   docket dates clean at 2026-09-24: 411 assertions over 6 fixtures and 32 ledger items
[WARN] gas_watch      51 day(s) on record, 37 verified, no gaps, latest 2026-09-13, EIA through 202606 over 131 months, model misses by 6.82%, which is 11 days old
[WARN] gas_watch_live UNRESOLVED upstream: CINGSA's public dashboard has still not published a new reading since 09/13/2026 21:00 Alaska. Its own operational note announced a semiannual shut-in field balance and maintenance from September 14th until September 21st, and on September 24th the dashboard is three days past that announced return date with the same stamp and no extension. The collector ran on schedule, fetched the page, archived the snapshot, carried no measurement forward, wrote an explicit unverified record and failed its job loudly, which is the designed behavior for a stale source past its announced window. Nothing in this repository can produce a measurement CINGSA has not published, so the failure is upstream and no repair exists here.
[WARN] cron_health    UNRESOLVED external blockers: gaswatch.yml:completion, gaswatch.yml:steps
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-09-24 (213 generated files)
[PASS] assemble       9 slides, pdf vector 9.91 MB, 9 thumbs, sources verified
[PASS] score          8.34 / 10 vs threshold 7.7, scorer says passes=True
[PASS] ship_gate      scored 8.34 against a threshold of 7.70
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```

