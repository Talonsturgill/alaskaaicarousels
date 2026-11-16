# STORYBOARD — No.116, 2026-11-15 — "The Route Runs Backwards"

## DECK HEADER

- **Thesis.** The regents did not just delay AI Engaged; they reversed the order of decisions, so campus AI policies are now drafted before the system statement that would require them is adopted, and the one-year clock for a system policy report starts only at adoption.
- **Document title (<=60).** `UA regents moved the AI vote. Campus policies start first.` (57 chars)
- **Framing.** UPDATE of No.109 (November 8th), which shipped with the vote outcome unconfirmed. The cover kicker prints UPDATE.
- **Arc (9).** 01 hook (the order flipped) -> 02 payoff (vote moved, work didn't) -> 03 definition (a benchmark, not a law; masterful depth) -> 04 the number (about 20 percent survived, Shier says; keepable measured rails) -> 05 breather (nearly 200 asked for a human statement) -> 06 counter-move (UAA's Faculty Senate paused too) -> 07 keepable route map (the order now) -> 08 synthesis (rules drawn campus by campus) -> 09 close (one ask). Temperature: cold survey light 01 to 02, lit peak 03, measured calm 04, hush 05, contested violet 06, clear diagram 07, expansive 08, still open ring 09.
- **Slide count rationale.** Nine: the update needs a payoff, a definition, the number, the dissent, the order, the synthesis and an ask; each carries a new verified specific. A breather at 05.
- **Continuity system.** (1) MOTIF EVOLUTION, the gold route head: the decision path's live end is the only gold mark on 01 to 08 (gold on 04 is the surviving share, which is the route's own measured piece), and it changes state every frame. (2) EDGE-TEASE, the route line leaves the right edge of 01 at y 880 and enters 02 from the left at y 880. (3) THE UNSET BENCHMARK STATE, February drawn as an open ring, never filled, on 02, 07, 08 and 09.

| slide | gold route head | February ring |
|---|---|---|
| 01 | leaves the UAF ring, exits right at y 880 | absent |
| 02 | enters left at y 880, reaches Fairbanks, forks: dashed FEB line plus three solid spurs south | open ring at the dashed line's end |
| 03 | a short gold sightline tick on the cap's datum notch | absent |
| 04 | the surviving share rail, gold | absent |
| 05 | thin gold thread past the Anchorage glow | absent |
| 06 | gold path head stops at the UAA ring; violet dashed branch to DEC | absent |
| 07 | gold on the NOVEMBER station (where the path is now) | open ring at FEBRUARY |
| 08 | gold on the open ring the three spurs converge to | the open ring, hovering |
| 09 | Polaris above the open ring | open ring, still unset |

- **Variety ledger check.** Last four heroes: light pillars on a snow plain (11-11), bodegon instrument niche (11-12), lidar occlusion lot (11-13), field kit objects (11-14); sibling No.109 was a two-light paper evidence table. This deck: NEW, RAKING-LIGHT RELIEF SURVEY, real DEM relief of Alaska as a surveyor's sheet with the decision path as a route and the statement as an unset benchmark. Atmosphere NEW: polar-twilight raking light, a low southern sun on real terrain, no fog, no window, no overcast. Hook archetype NEW: THE ORDER REVERSED. Palette NEW: INTERIOR TWILIGHT SURVEY. Type: Unbounded + Manrope + JetBrains Mono (neither of the last two pairings; Unbounded last used weeks ago). Continuity: route-head motif, route edge-tease, unset ring state (none forbidden).
- **Variance dials.** design_variance 5 (a cartographic deck built on real elevation with GPU terrain and survey furniture, far from the object-still-life run of the last week), visual_density 3 (map detail high, copy moderate), type_temperature 1 (Unbounded geometric caps as a USGS cartouche, cool Manrope body). Triple (5,3,1) differs from (6,3,3) (3,4,5) (4,5,2) (2,2,4).
- **Palette.** base #040A18; elevation steps #0B1830, #13253F; relief shadow #1A2C4A; relief lit #7FA3C8; frost highlight #DCE7F4; machine draft and benchmark cyan #5AC8F0; human route snow #F4F8FF; dissent violet #9664E6 (slide 06 only); alpenglow rim #E9B7A6 (under 1 percent of any frame); watermark #46545F; gold #FFC72C (route head, surviving share, Polaris; nowhere else).
- **Type system.** Display Unbounded wght 600 (500 for 60 px lines), tracking -0.02em, AK.fitText maxLines 3. Body Manrope 450 at 34 px, leading 1.38. Instrument JetBrains Mono 500 caps +0.08em for kickers, stations, labels. Fixtures: wordmark ALASKA.AI in Unbounded 600 20 px, counter NN / NN in Mono, coordinates footer and alaskaaihq.com in Mono 18 px #46545F, data-decorative.
- **Gold drawn after the grade** on every canvas; DOM gold is DOM.

## Claims index

| claim | slides |
|---|---|
| C01 | 01, 02, 07 |
| C03 | 01, 02, 07 |
| C22 | 02, 07 |
| C13 | 03, 04 |
| C24 | 03 |
| C14 | 03 |
| C06 | 04 |
| C07 | 04 |
| C09 | 04 |
| C10 | 04 |
| C17 | 05 |
| C05 | 06, 07 |
| C20 | 06 |
| C16 | 07 |
| C15 | 07 |
| C08 | 07 |
| C32 | 07 |
| C25 | 07, 08 |
| C18 | 08 |
| NOT USED on slides | C02, C04, C11, C12, C19, C21, C23, C26, C27, C28, C29, C30, C31, C33 to C56 |

## CRAFT PLAN

| slide | primary mark-making | largest object, and how it is modelled |
|---|---|---|
| 01 | gpu render PBR terrain of the whole state | the Alaska relief mesh, three.js PBR from the real state DEM at 1.0 m per km exaggeration, a low southern key at elevation 6 degrees casting long north shadows, cool fill, sea as dark gloss with a sun streak |
| 02 | hillshade of the Tanana valley | the Tanana flats and the Yukon-Tanana uplands, per-pixel Lambert hillshade from the FNSB DEM at device resolution over an OKLCH hypsometric ramp, lit from azimuth 175 |
| 03 | gpu render PBR of a survey monument cap set in granite | the aluminium cap and its boulder, three.js PBR lathe cap with engraved tick rings, IBL reflections, a displaced granite boulder with contact AO on a sun pool, the Alaska Range blurred behind |
| 04 | contour engraving of the Denali massif | the contour field, lit index contours on the south faces and a lee-side fade, three line weights, the three measured rails cased so the contours knock out under them |
| 05 | stipple glow of Southcentral at night | the Anchorage glow, a stipple density field graded by distance from the bowl with a two-part glow, the coast drawn as a soft transmitted line |
| 06 | hillshade of the Anchorage bowl and Knik Arm | the Chugach front and the arm, per-pixel hillshade from the Cook Inlet DEM, water flattened to #0B1830 with a specular glint line |
| 07 | transit diagram with hatched station rings | the route diagram, cased lines (dark casing plus colour core), station rings with inner fill states and a hachured Alaska coast ghost behind |
| 08 | gpu render PBR terrain from a high aerial camera | the state relief again from directly above the Gulf, PBR mesh, three light threads rising from the campus pins to a hovering open ring with its own soft glow on the terrain |
| 09 | depth-faded contour sheet of the Interior | the contour sheet around Fairbanks, line alpha falling with distance from the open ring, Polaris glow above |

Masterful depth frame: 03, the monument cap tack-sharp with a blurred granite shard repoussoir in the lower left, the cap over the boulder over the lit pool over the defocused range under exp2 sky haze, one low key, two-part contact shadow on a lit ground.
Tonal arc: cold and dark on 01 and 02, the lit peak on 03 (sunlit cap and granite, the brightest frame), mid on 04, the darkest frame on 05 (night glow breather), violet mid on 06, the clear diagram on 07, wide mid on 08, a still dark close on 09.

## SLIDE 01 — COVER (hook)

### A. NARRATIVE
1. **Beat.** Hook. Plants: why would the rules come before the statement that requires them?
2. **COPY, final.**
   - Kicker: `UPDATE  /  UA REGENTS  /  AI ENGAGED`
   - Headline line 1 (60 px): `Regents pushed the AI vote to February.` (C01)
   - Headline line 2 (132 px): `Campus policies start first.` (C03)
   - Pin labels: `UAA` `UAF` `UAS`
   - Counter `01 / 09`; fixtures (wordmark, coordinates `64°51'N 147°50'W`, alaskaaihq.com).
3. **Reader takeaway.** UA's AI vote moved to February and campus policies go first.

### B. COMPOSITION
4. **Layout map.** Kicker and headline cols 1 to 11, rows 1 to 3 (y 110 to 520) in the dark sky above the terrain's far edge. Terrain rows 4 to 8, horizon about y 560. Focal point the UAF ring at about (640, 860). Eye path headline -> UAF ring -> gold route exiting right at y 1000. Quiet zone the upper-right sky. Grid violation the route bleeding off the right edge.
4a. **Lower-third treatment.** The Alaska Range and the Gulf coast relief fill the lower third, modelled by the low key with long cast shadows and the sea's gloss streak; the gold route runs across that lit relief at y 1000 to the right edge, cased dark so it sits on the land.
5. **Depth plan.** sky gradient -> far terrain (Brooks Range, fogged toward sky) -> mid terrain -> near Gulf coast and Alaska Range -> pins and route -> type -> grain. Cues: exp2 fog to sky teal, scale gradient of the mesh, cast shadows, occlusion of far ranges by near ranges. Camera from (40, 520, 980) world units looking at (60, 0, -40), fov 34; terrain plane spans x -540..540, z -470..470 in projection units.
6. **Continuity device state.** Route head leaves UAF and exits right at y 880.

### C. ART DIRECTION
7. **Technique stack.** akthree setup supersample 2, softShadows 9; terrain PlaneGeometry 360x320 segments, vertex height = DEM metres x 0.012 world units (sampled from ak-state-dem via AKS.loadDEM.sampleCubic at the lon/lat inverted from AKGeo.alaskaProjection fitted to [[-540,-470],[540,470]]); land MeshStandardMaterial vertex colours from an OKLCH ramp #1A2C4A (low) to #7FA3C8 to #DCE7F4 (above 1,800 m), roughness 0.86; sea plane y -0.4 #071122 roughness 0.22 metalness 0.1; key DirectionalLight from azimuth 175 elevation 6 degrees, colour #FFE2C8, intensity 2.6; fill hemisphere #2A4A72 0.35; fog exp2 #0B1830 density 0.0011; pins TorusGeometry r 7 tube 1.4 cyan emissive #5AC8F0 at UAA (-149.82, 61.19), UAF (-147.83, 64.857), UAS (-134.64, 58.385) [design coordinates]; route a 2D gold polyline drawn after the grade from the projected UAF point to x 1080 at y 1000. Grade AKPOST exposure -0.06, contrast 1.08, cool lift.
8. **Data-in-art mapping.** Three pins = the three universities (C25 names them); relief is real elevation (no data encoding).
9. **Palette assignment.** sky #040A18 to #0B1830; terrain ramp above; pins #5AC8F0; route #FFC72C (the only gold besides none); headline #F4F8FF on sky about #08142A, contrast above 12:1.
10. **Type spec.** Kicker Mono 500 24 px +0.08em #5AC8F0. Line 1 Unbounded 500 fitText min 48 max 60 maxLines 1, width 920, #DCE7F4. Line 2 Unbounded 600 fitText min 104 max 132 maxLines 2, leading 0.98, tracking -0.02em, #F4F8FF, width 920. Pin labels Mono 500 22 px #DCE7F4 with a dark halo.
11. **Iconography/anchor spec.** Anchor the state relief in the canonical projection (parallels 55/65, rotate 154). Pins at real campus coordinates. No leaders.

### D. VERIFICATION
12. **Reference intent.** USGS shaded relief plate meets a polar-night satellite still.
13. **Risk flags.** Headline over terrain (horizon kept below y 560); route over pins (route starts at the UAF ring edge); mesh stair-steps (cubic sampling, 360 segments).
14. **Acceptance checklist.**
   - [ ] UPDATE readable in the kicker at 432 px
   - [ ] the state is recognisable in relief, Gulf coast and Alaska Range lit from the south
   - [ ] three cyan pins at the three campus locations
   - [ ] gold route exits the right edge at about y 1000
   - [ ] headline 2 sentences, no clipping

## SLIDE 02 — PAYOFF

### A. NARRATIVE
1. **Beat.** Pays the cover immediately. Plants: what exactly were they voting on?
2. **COPY, final.**
   - Kicker: `FAIRBANKS  /  NOVEMBER 4TH TO 6TH` (C22)
   - Headline: `The vote moved.` / `The work didn't.`
   - Body: `Meeting at UAF, regents postponed AI Engaged to their February meeting and told the AI Coordinating Council to start campus-specific AI policies in the interim, ADN reports.` (C22, C01, C03)
   - Map labels: `UAF`, `FEB, VOTE` (C01), `CAMPUS POLICY WORK, NOW` (C03)
3. **Reader takeaway.** The vote waits for February while campus policy work starts now.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 9, y 130 to 330; body cols 1 to 8, y 350 to 560 over the dark sheet margin above the neatline. Map panel y 600 to 1260 full width inside an 80 px neatline. Focal point the Fairbanks ring (about 560, 820). Eye path headline -> body -> ring -> fork. Quiet zone the sheet margin top right.
4a. **Lower-third treatment.** The Tanana flats and the Alaska Range foothills in hillshade fill the lower third, modelled tone lit from the south with long lee shadows, the three solid spurs running down through them toward the bottom edge.
5. **Depth plan.** sheet ground -> hillshade relief -> hydro tint -> route and rings -> labels -> type -> grain. Flat plan view (depth cues: hillshade light, cased lines over relief, a soft drop under the panel).
6. **Continuity device state.** Gold route enters from the left at y 1000, reaches the ring, forks: dashed snow FEB line ends at an open cyan ring; three solid snow spurs run south off frame.

### C. ART DIRECTION
7. **Technique stack.** Per-pixel hillshade at DEVICE resolution (ImageData 2160 x 1320 drawn 1:1 under setTransform(1,0,0,1,0,0)) from fnsb-dem via sampleCubic, projection equirect scaled by cos(64.85 deg), centre (-147.6, 64.75), 5.6 px per km; Lambert az 175 el 18 degrees, z factor 3.0; hypsometric OKLCH ramp #0B1830 (100 m) -> #1A2C4A -> #7FA3C8 (1,200 m); shade multiplies ramp; neatline 1 px #46545F; graticule hairlines 0.5 px snow at 0.12 every 0.5 degree. Route cased lines (casing #040A18 6 px, core 3 px). Grade light (AKPOST contrast 1.05).
8. **Data-in-art mapping.** Fork: one dashed line (the postponed vote, C01) and three solid spurs (campus policy work begun, C03). Ring at real UAF coordinates.
9. **Palette assignment.** sheet #040A18; relief ramp above; route gold #FFC72C head only; spurs and dashed line #F4F8FF; open ring #5AC8F0. Body #DCE7F4 on #040A18 above 14:1.
10. **Type spec.** Kicker Mono 500 24 px #5AC8F0. Headline Unbounded 600 fitText min 72 max 96 maxLines 2, width 880. Body Manrope 450 34 px leading 1.38 #DCE7F4 width 840. Labels Mono 500 22 px.
11. **Iconography/anchor spec.** Anchor the Fairbanks ring on real relief; labels attached to the dashed line end and the spur bundle with short leaders declared in __akLeaders.

### D. VERIFICATION
12. **Reference intent.** USGS 1:250,000 quadrangle in night mode.
13. **Risk flags.** DEM lattice (cubic sampling at device px); body length (four lines max at 840 px); labels crossing relief (halo).
14. **Acceptance checklist.**
   - [ ] route enters from the left edge at about y 1000
   - [ ] dashed FEB line ends at an open ring, never filled
   - [ ] three solid spurs leave the ring southward
   - [ ] relief has no lattice at 100 percent
   - [ ] body four lines or fewer, no clipping

## SLIDE 03 — DEFINITION (masterful depth)

### A. NARRATIVE
1. **Beat.** Definition: what the regents will vote on. Plants: who drew the first draft?
2. **COPY, final.**
   - Kicker: `WHAT REGENTS WILL VOTE ON`
   - Headline: `A benchmark,` / `not a law.`
   - Body: `AI Engaged is a four-page statement of intent, ADN reports. It doesn't establish policy.` (C13, C14)
   - Ring labels: `SIX PRINCIPLES` `FOUR PRIORITIES` `FIVE EXPECTATIONS` (C24)
3. **Reader takeaway.** AI Engaged is a statement of intent with 6, 4 and 5 parts, not policy.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 8, y 120 to 330; body cols 1 to 7, y 350 to 600 over the blurred dark sky and range. Cap and boulder cols 4 to 11, rows 5 to 8, cap centre about (640, 930). Ring labels right of the cap at x 860, y 860 to 980 with short leaders. Quiet zone the upper right sky.
4a. **Lower-third treatment.** The granite boulder in the low sun with a lit pool on the frost-shattered ground, two-part contact shadow under the cap's rim and the boulder, and a blurred granite shard bleeding off the lower left as the near plane of the depth stack.
5. **Depth plan.** sky (#0B1830 to teal band) -> Alaska Range skyline from the Denali DEM, blurred 6 px -> haze -> ground plane with sun pool -> boulder -> cap -> repoussoir shard (blurred) -> type -> grain. Cues: DOF (range and shard blurred), occlusion, atmospheric fade, contact shadow on a lit ground, one low key. Camera (0, 0.55, 1.35) m looking at (0, 0.18, 0), fov 34.
6. **Continuity device state.** Gold appears as a short sightline tick at the cap's datum notch only.

### C. ART DIRECTION
7. **Technique stack.** akthree softShadows 9, supersample 2; cap LatheGeometry [r, y] profile radius 0.09 m, domed top, aluminium metalness 1 roughness 0.32 with a canvas bump map carrying three concentric tick rings (6, 4 and 5 ticks, radii 0.032, 0.052, 0.072 m) and a centre cross; environment AKT.environment intensity 0.8; boulder IcosahedronGeometry detail 5 displaced by AK.fbm3 seed 2026111503, granite vertex colours #5E6670 to #A6ADB3 with feldspar speckle; ground plane roughness 0.95 #1A2433 with a radial sun pool texture to #56606C under the boulder; key DirectionalLight az 170 el 9 degrees #FFE2C8; skyline painted on a 2D background canvas from ak-denali-dem horizon heights, blurred, alpenglow rim #E9B7A6 on the crest; shard a small displaced mesh near the camera, blurred via a separate layer. Grade AKPOST then holdInk gold.
8. **Data-in-art mapping.** Tick rings carry 6, 4 and 5 ticks = principles, priorities, expectations (C24).
9. **Palette assignment.** aluminium reflecting #7FA3C8 and #DCE7F4; granite #5E6670 to #A6ADB3; pool #56606C; sky #0B1830; gold tick #FFC72C. Body #DCE7F4 on blurred sky about #0E1C33, above 11:1.
10. **Type spec.** Headline Unbounded 600 fitText min 80 max 108 maxLines 2, width 760. Body Manrope 450 34 px #DCE7F4 width 700. Labels Mono 500 22 px #DCE7F4.
11. **Iconography/anchor spec.** Anchor the survey cap; three leaders from labels to their rings declared in __akLeaders.

### D. VERIFICATION
12. **Reference intent.** Large-format still of a USGS benchmark on a summit at last light.
13. **Risk flags.** Cap reads as a coin (lathe dome, stamped centre cross, rim bevel); metal black (environment intensity 0.8); boulder floating (contact declared, lit pool).
14. **Acceptance checklist.**
   - [ ] the cap reads as a survey benchmark set in rock
   - [ ] three tick rings with 6, 4 and 5 ticks visible at full size
   - [ ] contact shadow on a lit ground under the cap and boulder
   - [ ] range blurred, cap tack-sharp
   - [ ] gold only on the datum tick

## SLIDE 04 — THE NUMBER

### A. NARRATIVE
1. **Beat.** The number. Plants: not everyone accepts that account.
2. **COPY, final.**
   - Kicker: `THE FIRST DRAFT`
   - Headline: `About 20 percent survived, Shier says.` (C09)
   - Body: `Ben Shier, UA's chief information technology officer, wrote the first draft by prompting Claude with human ideas, "all fed to Claude." He says about 20 percent of that two-page draft survived human edits.` (C06, C07, C09, C10)
   - Rail labels: `FIRST DRAFT, 2 PAGES` (C10), `SURVIVED, ABOUT 20%` (C09), `AI ENGAGED, 4 PAGES, PER ADN` (C13), `1 UNIT = 1 PAGE` [design], `SHARE, NOT POSITION` [design]
3. **Reader takeaway.** By its author's estimate, about a fifth of the two-page machine draft survived into a four-page document.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 10, y 120 to 330; body cols 1 to 9, y 350 to 600. Rails cols 1 to 11, y 820 to 1140 on the contour field. Focal point the gold rail at (190 to 330, 980). Quiet zone a calm contour band at y 640 to 760.
4a. **Lower-third treatment.** The contour engraving of the Denali massif carries the lower third with index contours lit by the low key, and the three cased rails sit on it, the four-page road the longest mark; contours fade under the type band and rise to full weight below y 760.
5. **Depth plan.** sheet -> contour field (three weights, alpha by elevation) -> rail casings knocking out contours -> rails -> labels -> type -> grain. Flat by choice: quantities stay in parallel projection (doctrine 4).
6. **Continuity device state.** Gold is the surviving share rail.

### C. ART DIRECTION
7. **Technique stack.** d3.contours on a 400 x 300 grid sampled from ak-denali-dem (cubic), thresholds every 150 m, index every 750 m; contour stroke 0.8 px #7FA3C8 at 0.30, index 1.4 px at 0.55, a lit-side boost toward azimuth 175; rails as cased lines: draft dashed #5AC8F0 4 px, survived solid #FFC72C 6 px, document solid #F4F8FF 5 px, casing #040A18 12 px; scale declared on data-scale (x from 120 px = 0 pages to 960 px = 4 pages, 210 px per page) with every end mark declared.
8. **Data-in-art mapping.** 210 px per page: draft 420 px (2 pages, C10), survived 84 px (0.2 x 2 pages, C09), document 840 px (4 pages, C13). Share, not position.
9. **Palette assignment.** contours #7FA3C8; draft #5AC8F0; survived #FFC72C; document #F4F8FF; labels #DCE7F4. Body #DCE7F4 on #040A18 above 14:1.
10. **Type spec.** Headline Unbounded 600 fitText min 64 max 88 maxLines 2, width 900. Body Manrope 450 34 px width 900. Labels Mono 500 22 px.
11. **Iconography/anchor spec.** Anchor the Denali contour field (labelled `DENALI MASSIF, CONTOURS 150 M` [design], data-decorative). __akAssert on each rail length against its page value.

### D. VERIFICATION
12. **Reference intent.** Engineering survey plate, alignment comparison sheet.
13. **Risk flags.** Rail read as geography (legend `1 UNIT = 1 PAGE`, `SHARE, NOT POSITION`); undeclared marks in the scale band (contours knocked out under the band).
14. **Acceptance checklist.**
   - [ ] three rails on one scale, lengths 2, 0.4 and 4 units
   - [ ] gold only on the surviving share rail
   - [ ] the legend and caveat readable at full size
   - [ ] quote marks straight
   - [ ] contours readable as terrain, not noise

## SLIDE 05 — BREATHER

### A. NARRATIVE
1. **Beat.** Rest beat with one human fact. Plants: did Anchorage's faculty act too?
2. **COPY, final.**
   - Headline: `Nearly 200 students and staff asked for a brief statement written by humans.` (C17)
   - Small: `MOSTLY IN ANCHORAGE, PER ADN` (C17)
3. **Reader takeaway.** Nearly 200 people asked for a human-written statement.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 9, y 160 to 520 over open dark sea and sky. The Anchorage glow at about (640, 940); Cook Inlet coast runs from lower left to upper right. Quiet zone the upper right.
4a. **Lower-third treatment.** BREATHER — the deck rests after the number; the lower third carries the Kenai and Turnagain coast as a soft transmitted line and the Anchorage glow's outer stipple, modelled by density, but the frame is deliberately quiet. `data-breather` set.
5. **Depth plan.** night ground -> faint relief from the Cook Inlet DEM at 0.18 alpha -> coast glow -> stipple glow -> thin gold thread -> type -> grain. Cues: glow falloff, scale, low-alpha relief.
6. **Continuity device state.** A thin gold thread runs past the Anchorage glow.

### C. ART DIRECTION
7. **Technique stack.** Coast drawn from the Cook Inlet DEM's zero contour (d3.contours threshold 1 m) as a 1.2 px #5AC8F0 line plus a 6 px blurred copy at 0.25 (halation); stipple: points Poisson-disc spaced 3 px over a density field exp(-d/48 px) about the bowl (seeded AK.rng(2026111505)), radius 0.6 to 1.4 px, #DCE7F4 to #7FA3C8; two-part glow (tight core, wide 220 px halo at 0.12) in screen; relief hillshade at 0.18 alpha. The dots are a density, not a count [design].
8. **Data-in-art mapping.** None; the glow locates "mostly in Anchorage" (C17). Dot count carries no meaning.
9. **Palette assignment.** ground #040A18; coast #5AC8F0; glow #DCE7F4; thread #FFC72C. Headline #F4F8FF on #050C1C above 15:1.
10. **Type spec.** Headline Unbounded 600 fitText min 60 max 80 maxLines 4, width 880, leading 1.04. Small Mono 500 24 px #7FA3C8.
11. **Iconography/anchor spec.** Anchor the Cook Inlet coast; no leaders.

### D. VERIFICATION
12. **Reference intent.** NASA Black Marble crop, Southcentral.
13. **Risk flags.** Dots read as a count (no number printed beside them); glow banding (grain tile).
14. **Acceptance checklist.**
   - [ ] the headline reads at 432 px
   - [ ] Cook Inlet coast recognisable
   - [ ] the glow sits on Anchorage
   - [ ] frame feels quiet

## SLIDE 06 — COUNTER-MOVE

### A. NARRATIVE
1. **Beat.** Dissent from Anchorage. Plants: so what is the order now?
2. **COPY, final.**
   - Kicker: `ANCHORAGE`
   - Headline: `UAA's Faculty Senate` / `paused too.`
   - Body: `Senators postponed their vote on a resolution to reject and replace AI Engaged until next month, ADN reports. Senate chair Andrea Dewees said, "I think it's probably going to be messy."` (C05, C20)
   - Map labels: `UAA`, `REJECT AND REPLACE`, `DECEMBER, PER ADN` (C05)
3. **Reader takeaway.** Anchorage's faculty senate has its own pending vote to reject and replace AI Engaged.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 9, y 120 to 330; body cols 1 to 8, y 350 to 590 over the sheet margin. Map panel y 620 to 1260. UAA ring at about (620, 900); violet dashed branch runs east and south to an open DEC ring near (880, 1080).
4a. **Lower-third treatment.** The Chugach front and Turnagain Arm in hillshade fill the lower third, lit from the south, the water of Knik and Turnagain Arm flattened to deep blue with a specular glint line, and the violet dashed branch crosses the lit relief to its open ring.
5. **Depth plan.** sheet -> hillshade -> water with glint -> route and branch -> rings -> labels -> type -> grain. Flat plan view; cues hillshade light, casing over relief.
6. **Continuity device state.** Gold path head stops at the UAA ring; violet dashed branch to an open ring.

### C. ART DIRECTION
7. **Technique stack.** Per-pixel hillshade at device resolution from ak-cookinlet-dem (sampleCubic), equirect scaled by cos(61.2), centre (-149.6, 61.15), 7.2 px per km; Lambert az 175 el 20 degrees z 2.6; land ramp #13253F -> #7FA3C8 -> #DCE7F4 (above 1,400 m); water (elevation <= 0) #0B1830 with a 1 px glint line #5AC8F0 at 0.35 along a band; violet dashed branch 3 px #9664E6 dash 14 8, cased; rings r 14.
8. **Data-in-art mapping.** Branch = the senate's resolution to reject and replace (C05); open ring = vote not yet taken.
9. **Palette assignment.** violet #9664E6 here only; gold head #FFC72C; rings #5AC8F0. Body #DCE7F4 on #040A18 above 14:1.
10. **Type spec.** Headline Unbounded 600 fitText min 72 max 96 maxLines 2, width 880. Body Manrope 450 34 px width 860. Labels Mono 500 22 px with dark halo.
11. **Iconography/anchor spec.** Anchor the UAA ring at real coordinates; leaders from the two labels to their marks declared in __akLeaders.

### D. VERIFICATION
12. **Reference intent.** Night-mode nautical chart of Knik Arm with a survey overlay.
13. **Risk flags.** Violet reads as SaaS purple (desaturated relief around it, used once); quote marks straight.
14. **Acceptance checklist.**
   - [ ] UAA ring on the Anchorage bowl
   - [ ] violet branch dashed, ends at an open ring
   - [ ] water reads as water
   - [ ] body four lines max

## SLIDE 07 — THE ORDER NOW (keepable)

### A. NARRATIVE
1. **Beat.** Keepable reference: the sequence. Plants: if the campuses go first, what is February for?
2. **COPY, final.**
   - Kicker: `THE ORDER NOW`
   - Headline: `Campus policies start` / `before the statement.`
   - Body: `The statement would require each of the three universities to write its own AI policy. That work now starts first. A one-year clock for a system-wide policy report starts only at adoption.` (C16, C03, C15)
   - Stations: `MAY` `REGENTS DIRECT SHIER` (C08); `OCTOBER 9TH` `CLAUDE'S ROLE DISCLOSED, CRITICS SAY` (C32); `NOVEMBER 4TH TO 6TH` `VOTE POSTPONED` (C22, C01); `DECEMBER` `UAA SENATE VOTE, PER ADN` (C05); `FEBRUARY` `REGENTS VOTE` (C01); `ADOPTION` `ONE YEAR TO A SYSTEM POLICY REPORT` (C15); spur labels `UAA` `UAF` `UAS` `CAMPUS POLICY WORK` (C03, C25)
3. **Reader takeaway.** Campus policy work starts in November, before the February vote; the one-year clock starts at adoption.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 10, y 110 to 290; body cols 1 to 10, y 300 to 470. The route runs vertically down col 2 to 3 (x 170) from y 560 to 1220 with six stations; spurs branch right at the NOVEMBER station to three rings at x 620, 760, 900. Labels right of each station.
4a. **Lower-third treatment.** A graded ground: the Gulf of Alaska coast ghost drawn as lit hachure relief rising in value toward the bottom edge, under the ADOPTION station and its twelve-month dashed extension, so the band carries modelled tone and not bare sheet.
5. **Depth plan.** sheet -> hachured coast ghost at 0.14 -> cased route lines -> station rings -> labels -> type -> grain. Flat and schematic by design; no perspective.
6. **Continuity device state.** Gold on the NOVEMBER station; FEBRUARY an open ring.

### C. ART DIRECTION
7. **Technique stack.** SVG transit diagram: line casing #040A18 10 px, core #F4F8FF 4 px; future segments dashed 12 6; station rings r 12 stroke 3 with inner fill states (past filled #F4F8FF, now gold #FFC72C, future open); spurs octolinear snapped at 45 degrees; behind, a canvas ghost of the Alaska coast via AKGeo projection, drawn as short hachure ticks along the coast normal (seed 2026111507), #5AC8F0 at 0.14.
8. **Data-in-art mapping.** Station order = the reported sequence; the twelve dashed ticks after ADOPTION are equal months of the one-year clock (C15), declared on data-scale.
9. **Palette assignment.** line #F4F8FF; now #FFC72C; future open #5AC8F0; labels #DCE7F4; secondary #7FA3C8.
10. **Type spec.** Headline Unbounded 600 fitText min 64 max 84 maxLines 2, width 900. Body Manrope 450 32 px width 900. Station names Mono 500 24 px #F4F8FF; station notes Manrope 500 24 px #A9B9CC.
11. **Iconography/anchor spec.** Anchor the coast ghost; the stations are the annotation.

### D. VERIFICATION
12. **Reference intent.** Transit authority service-change map, survey edition.
13. **Risk flags.** Label collisions (stations 108 px apart, labels single line); month ticks implying dates (labelled only 1 YEAR).
14. **Acceptance checklist.**
   - [ ] six stations in order, NOVEMBER gold
   - [ ] three spurs branch at NOVEMBER, before FEBRUARY
   - [ ] FEBRUARY ring open
   - [ ] twelve equal ticks after ADOPTION
   - [ ] no label collisions

## SLIDE 08 — SYNTHESIS

### A. NARRATIVE
1. **Beat.** Synthesis. Plants: which order is right?
2. **COPY, final.**
   - Kicker: `THREE UNIVERSITIES, ONE STATEMENT`
   - Headline: `The rules get drawn` / `campus by campus.`
   - Body: `UA says the statement keeps curriculum, academic integrity and faculty instructional judgment with UAA, UAF and UAS. Cooper says UA is "never going to have everyone on the same page with AI."` (C25, C18)
   - Pin labels `UAA` `UAF` `UAS`, ring label `FEBRUARY, UNSET`
3. **Reader takeaway.** The rules that bind will be campus rules; the system statement is still unset.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 10, y 110 to 300; body cols 1 to 10, y 320 to 520 over dark sky. Terrain from y 600 down, seen from high above the Gulf, the state filling cols 1 to 12. Open ring hovering at about (560, 640) with its glow on the terrain below.
4a. **Lower-third treatment.** The Gulf coast, Kenai Peninsula and Southeast in PBR relief fill the lower third, with the UAA and UAS light threads rising out of it and the ring's glow pooled on the lit relief, the sea a dark gloss with a cool reflection of the threads.
5. **Depth plan.** sky -> terrain mesh (fogged far edge) -> threads -> hovering ring -> type -> grain. Camera (60, 900, 700) looking at (40, 0, -60), fov 38. Cues: fog, scale, occlusion of threads by the ring, cast glow.
6. **Continuity device state.** Gold on the open ring the three threads converge to.

### C. ART DIRECTION
7. **Technique stack.** akthree terrain as 01 but its own mesh (280x250 segments) with a colder ramp, key az 200 el 14, sea #050E1D; threads TubeGeometry r 1.2 emissive #DCE7F4 from each campus pin to the ring; ring TorusGeometry r 26 tube 2.2 emissive #FFC72C drawn after grade as a 2D overlay at its projected position; glow pool painted on terrain under the ring after the grade.
8. **Data-in-art mapping.** Three threads = three universities (C25).
9. **Palette assignment.** terrain ramp #13253F to #DCE7F4; threads #DCE7F4; ring #FFC72C. Body #DCE7F4 on sky #050C1C above 14:1.
10. **Type spec.** Headline Unbounded 600 fitText min 64 max 92 maxLines 2, width 900. Body Manrope 450 34 px width 900. Labels Mono 500 22 px.
11. **Iconography/anchor spec.** Anchor the state relief, pins at real campus coordinates.

### D. VERIFICATION
12. **Reference intent.** Orbital night photograph with survey overlay.
13. **Risk flags.** Ring reads as a place (labelled UNSET, floating clearly above terrain); threads thin at thumb (glow).
14. **Acceptance checklist.**
   - [ ] three threads rise from three campus pins
   - [ ] ring open and floating
   - [ ] the state relief reads from above
   - [ ] body four lines max

## SLIDE 09 — CLOSE (one ask)

### A. NARRATIVE
1. **Beat.** One ask.
2. **COPY, final.**
   - Headline: `Campus rules first,` / `or statement first?`
   - Ask: `Which order should UA have chosen? Say so in the comments.`
   - Wordmark `ALASKA.AI`
3. **Reader takeaway.** A question about the order of decisions.

### B. COMPOSITION
4. **Layout map.** Headline cols 1 to 10, y 160 to 400; ask cols 1 to 9, y 430 to 520. Contour sheet fills y 560 to 1350. Open ring at (620, 900) with Polaris above at (620, 760). Wordmark bottom left above the fixtures.
4a. **Lower-third treatment.** The contour sheet of the Fairbanks hills runs through the lower third, line alpha rising toward the open ring, index contours at heavier weight catching the low key, the Tanana flats a calm band with the river traced in faint cyan.
5. **Depth plan.** sheet -> contours (depth-faded) -> ring and its glow -> Polaris -> type -> grain.
6. **Continuity device state.** Polaris above the still-open ring.

### C. ART DIRECTION
7. **Technique stack.** d3.contours from fnsb-dem (cubic, 360 x 300 grid) thresholds every 60 m, line alpha = 0.10 + 0.5 x exp(-d/360 px) from the ring, stroke 0.7 px #7FA3C8, index every 300 m at 1.2 px; ring 2D r 30 stroke 3 #5AC8F0 open; Polaris 4-point star #FFC72C 18 px with a soft halo; grain tile.
8. **Data-in-art mapping.** None by design.
9. **Palette assignment.** contours #7FA3C8; ring #5AC8F0; Polaris #FFC72C. Headline #F4F8FF on #040A18 above 15:1.
10. **Type spec.** Headline Unbounded 600 fitText min 72 max 100 maxLines 2, width 900. Ask Manrope 500 36 px #DCE7F4. Wordmark Unbounded 600 40 px.
11. **Iconography/anchor spec.** Anchor the Fairbanks hills contours; Polaris.

### D. VERIFICATION
12. **Reference intent.** Survey sheet title block at night.
13. **Risk flags.** Close stacks asks (one question only); contours noisy under type (faded near the top).
14. **Acceptance checklist.**
   - [ ] a single ask
   - [ ] Polaris present, gold
   - [ ] ring open
   - [ ] no source note anywhere

## BUILD RECONCILIATION

Dossier numbers the build changed, recorded before the critics:
- Edge-tease: the gold route exits 01 and enters 02 at y 880, not y 1000 (the 1000 band crossed the UAS ring on 01).
- Slide 01: the headline is three lines ("Campus / policies / start first.") at about 120 px with the 56 px line above it in two lines (authored break before "to February."); terrain HS 0.0034 world units per metre, camera from (150, 1230, 1060) to (150, 0, -250), fov 40, key elevation 11 degrees; the coast is traced as a faint cyan line on the terrain.
- Slide 02: the UAF label sits left of the ring; no other change.
- Slide 03: camera from (0.05, 0.30, 1.18) to (0, 0.282, 0); the boulder and cap tilted 0.42 rad toward the camera so the ring face reads; key azimuth 222, elevation 17; ring labels on dark knockout plates at x 690; the contact shadow declared at the cap's front foot (shaded flange and grout ring against lit granite, dL 49.6 measured by contact_probe). The cast falls behind the cap and is too shallow to measure.
- Slide 04: Denali's summit placed at (740, 790), 4.2 px per km; contours every 150 m with cumulative tint fills, no lee offset pass; lanes behind each label row instead of under the rails; the contour field masked to the DEM footprint with a 70 px feather.
- Slide 05: the coast is the state outline (not the DEM zero contour, which clamped at the DEM edge); relief faded inside the DEM footprint; headline authored in four lines.
- Slide 06: no glint line (it found water only at the panel edge and printed a stray stub); centre moved to -149.72 so the DEM's east edge stays off the panel; violet labels on dark plates.
- Slide 07: stations at y 556, 640, 760, 870, 972, 1100; the campus bundle leaves NOVEMBER up-right above its label at y 716 and splits at 45 degrees to rings at x 760, 860, 960, y 900; twelve clock ticks span the declared band.
- Slide 08: ring at world (-20, 150, -20), camera from (40, 1180, 1120) to (40, 0, -330); UAS label left of its pin.
- Slide 09: headline copy changed to "Campus rules first, / or statement first?" so it holds two lines at fit; contour engraving masked to the DEM footprint.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-11-15. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[WARN] qa.py          WARN, 0 fails, 2 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 11 line(s), 2134 chars
[PASS] caption_check  PASS, 886 chars, hook 117, 3 hashtags
[PASS] word_ban       word_ban: 0 banned word(s) in out/2026-11-15 and the docket
[PASS] copy_sync      copy_sync_check: PASS -- 63 authored slide strings all present in the render; alaskaaihq.com on every slide; no banned slide string; no curl
[PASS] aggregate      aggregate_check: PASS -- 9 aggregate assertion(s) detected, 10 declared -> out/2026-11-15/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 19 claims indexed, 0 declared counts checked, 0 body quote(s) checked, 0 11a region set(s) checked, 0 drift(s)
[PASS] tonal_arc      brightest 03, darkest 05, span 14.4 L*, as declared
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.115 (fail at 0.60), max pair 0.286, drawn share 71% (105 drawn vs 42 block
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] ledger_guard   LEDGER GUARD: PASS, 7 cron-written file(s) untouched
[PASS] docket_dates   docket dates clean at 2026-11-15: 433 assertions over 6 fixtures and 43 ledger items
[PASS] gas_watch      103 day(s) on record, 89 verified, no gaps, latest 2026-11-15, EIA through 202608 over 132 months, model misses by 6.82%
[PASS] gas_watch_live PASS, checked 2026-11-16T06:16:05Z
[PASS] cron_health    7 scheduled workflows audited at 2026-11-16T06:16:07.344227Z
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-11-15 (322 generated files)
[PASS] assemble       9 slides, pdf vector 7.8 MB, 9 thumbs, sources verified
[PASS] score          8.59 / 10 vs threshold 7.7, scorer says passes=True
[PASS] ship_gate      scored 8.59 against a threshold of 7.70; craft floor closed, one craft cycle ran on frames [3, 8, 1, 5] (art 6.5 -> 7.0)
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```


### Round 1 repairs (after the first pixel review)
- Slide 01: relief exaggeration 0.0058 per metre, brighter ramp, key at elevation 7 degrees and intensity 5.2, camera from (170, 980, 1000) to (170, 0, -260); a room-tone floor under the fixtures. Unbounded display lines carry a 0.5 to 0.6 px same-colour stroke on every slide to close the variable font's overlap seams.
- Slide 02: map panel ends at y 1224 so the footer has clear air; labels on dark plates.
- Slide 03: granite albedo cut to the planned tone with a visible terminator; a soft contact decal under the cap flange and a granite grout ring replace the black gasket; skyline relief raised and smoothed and hazed into the ground colour with no seam; the rock raised 0.055 m so the cap sits higher; leaders sampled at three ring angles so none cross; the gold tick seated on the notch; contact declared at the cap's left foot (dL 31.1).
- Slide 04: label lanes removed (labels on dark plates); a south-lit device-resolution hillshade under the contours restores the lit faces; only the ruler band keeps a knockout.
- Slide 05: relief layer and the two satellite glows removed; a centred two-part halo; coast and thread faded out of the fixture band.
- Slide 06: map panel ends at y 1222; water flat below 2 m with one soft sheen band; a 3.2 px centred difference removes the stair steps; the REJECT AND REPLACE plate lifted off the branch.
- Slide 07: the coast ghost drops long straight runs and the 141st meridian, grades upward in value, keeps clear of the ADOPTION note; a dashed continuation runs through the one-year ruler; spurs at the trunk's 4 px.
- Slide 08: mesh at 2.5 projected units per cell, no shadow map (its seams), threads rise vertically from each pin before arcing, with a stroke-blurred glow; ring at world (-40, 150, -110); labels on plates; the glow pool removed.
- Slide 09: window moved wholly inside the FNSB DEM (5.2 px per km, centre -146.0, 64.98) so no data edge prints; steeper radial falloff; index contours every 400 m at 1.7 px; the river traced at 200 m; Polaris at 32 px with a 104 px halo; the ask broken after "chosen?".

### Round 2 repairs (after the second pixel review)
- Declined on measurement: the "seams" reported in Unbounded's d, a and n on slides 01 and 02 are the typeface's own ink traps (the notches it cuts where a stem meets a bowl), visible at 100 percent in a clean crop of slide 02's headline; they are design, not a render defect.
- Slide 01: the mesh's sea vertices take the open-sea colour #030812 so no grid footprint shows; an attempt to shade the shelf from the DEM's bathymetry printed streaks at the DEM edge and was reverted.
- Slide 03: a horizon haze band hides the line where the painted range meets the rendered ground; feldspar flecks quieter; the cap's flange is matte metal (metalness 0.35), not a black gasket; leaders are straight lines from each plate to its own ring, none crossing.
- Slide 06: normals from heights smoothed over a 1.2 px five-tap kernel and a 3.6 px centred difference; a shoreline glint (cyan) on the water's edge inside the water.
- Slide 07: the coast ghost keeps every coast segment under 30 px, so the Gulf coast reads continuous.
- Slide 08: the mesh is clipped to the Alaska outline (Canada's terrain no longer extrudes), threads are 3.6 world units with a 12 px stroke-blurred glow, the ring sits at world (10, 150, -120) over the Interior, camera from (60, 1120, 1120) to (60, 0, -420); the deep-sea plane at -2.0 under shelf-shaded sea vertices.

### Round 3 repairs (after the flow critic)
- Declined on measurement: the flow critic read Manrope's apostrophes on 03, 04, 06 and 07 as curly. copy_sync_check's census reads every one as U+0027; Manrope draws the straight mark slanted.
- Slide 03: body cut to two sentences (the ring plates carry six, four and five); the boulder takes a 2048 px speckle map on its own UVs, so it is crisp at the cap; the contact decal softened; the rock raised to 0.085 m; contact re-measured below the flange's front edge (dL 9.2).
- Slide 05: denser stipple core; the gold thread now leaves the left edge at y 1150, so 06's left-edge entry completes it.
- Slide 07: the hachure coast ghost replaced by a continuous cased coastline graded in alpha, plus a faint south-lit hillshade of the Gulf coast from the state DEM rising in value toward the bottom; the DECEMBER station ring is violet, carrying the senate's dissent from 06.
- Slide 08: sea vertices take the sea plane's colour #030812 (no shelf), so no mesh footprint shows. A low oblique camera was tried and reverted (the ring crossed the body copy).
- Slide 09: the crosshair inside the February ring removed, so it reads unset rather than targeted.

### Craft cycle (round 4, on the scorer's frames 03, 08, 01, 05)
- Slide 03: the cap is set flush (no flange above the rock) in a flattened mortar collar #7A8088; granite grain at three scales (soft mineral clusters, crystals, grit); the painted skyline lowered (0.020 px per metre) so its crest stays under the body copy; contact re-measured (dL 14.5, axis v).
- Slide 08: a dashed gold drop line from the ring to a soft glow on the terrain beneath it, so the ring reads as hovering and unset; Canada's terrain sinks to a low dim ghost so no lit wall stands at the border.
- Slide 01: Canada's terrain sinks to a low dim ghost (#08121F) so no lit wall stands at the 141st meridian.
- Slide 05: a luminous core, dot size and brightness falling off radially, a stronger halo.
