# STORYBOARD, No.94, 2026-10-23, THE REGISTERED LAYER

## THESIS
Fairbanks North Star Borough's proposed Ordinance No. 2026-42 pauses land use permits for large-scale data centers through December 31st, 2027, but the decision inside it is the definition. The ordinance itself says that under today's code a large data center would be permitted only in the GU-1 and GU-5 General Use districts, and the borough's own zoning layer puts those two districts at 97 percent of the zoned map, while Heavy and Light Industrial together are under a fifth of a percent. A code from 2005 that names no data center fences almost nothing; the draft's first real fence is a size, 5 MW. Position taken: argue that number now, in the 90 days the Planning Commission has, because the permanent rule will inherit it. PDF title: "Only Two Zones, 97 Percent of the Map" (copy.json carries the final one).

UPDATE of No.76 (2026-10-03, "Fairbanks Votes Tuesday. Six Voices on AI Data Centers"). Material new since No.76: the borough's own enforceable permit pause (Ordinance 2026-42, on the October 22nd agenda), its three-test definition and end date, and the zoning map it would freeze. The cover says UPDATE.

## ARC, nine slides
- 01 COVER, hook [dusk, wide]. UPDATE. "Only" two zones. 97 percent of the map.
- 02 PAYOFF [plan, cool]. The ordinance's word against the borough's map, GU-1 and GU-5 by acre.
- 03 THE 3 PERCENT [plan, close]. Everything else, and the industrial land the code skips.
- 04 WHY THERE [at grade, the land itself]. A 2005 plan and a code with no word for a data center.
- 05 THE DEFINITION [sunlit snow, the brightest]. The turn: three tests, and the floor test drawn to scale.
- 06 BREATHER, THE PAUSE [last light, the depth frame]. Through December 31st, 2027; the "large" footprint as a fleck in the land.
- 07 THE GRID [blue hour, keepable]. 5 MW against GVEA's 38 MW and 15 MW alert lines.
- 08 NEXT [civil twilight]. 90 days, October 27th, six months, temporary.
- 09 CLOSE [night, the darkest]. Is 5 MW the right line for "large" in Fairbanks?
Temperature turns on 05 (the definition, in daylight) and falls with the day to 09.

## SLIDE COUNT RATIONALE
Nine. Each beat is a different object or document: the map claim, the payoff by acre, the 3 percent and the industrial irony, the 2005 plan, the three tests, the pause, the grid comparison, the process, the ask. 02 and 03 cannot merge without losing the industrial acreage, which is the frame a Fairbanks planner forwards.

## HOOK ARCHETYPE
NEW: THE ONE-WORD AUDIT. The cover takes one word from the record, the ordinance's "only", and measures it against the borough's own map.

## CONTINUITY SYSTEM
- D1, THE REGISTERED LAYER (camera move through one scene). One real GIS layer, the borough's 1,129 zoning polygons (assets/geo/fnsb-zoning.geo.json), held in geographic registration through the deck and reprinted in a different medium on each frame: a dusk oblique (01), the equal-area plan (02), the Fairbanks to North Pole cluster at about 6x (03), the land at grade looking north (04), a 150 m plan of one GU-1 muskeg plot (05), a low oblique into last light (06), an insert of the gauge (07), the plan again at civil twilight (08) and at night (09). 02, 08 and 09 share one projection to the pixel: d3.geoConicEqualArea().parallels([55,65]).rotate([147,0]) fitted to the borough in the box [[90,520],[990,1250]].
- D2, THE GOLD LINE (motif evolution). Flag gold #FFC72C means "where large is fenced" and nothing else (plus the Polaris, which is DOM). It migrates from place to size to power to time, which is the thesis drawn: 01 a hairline ring around the 3 percent cluster (today's only fence is around what is NOT General Use); 02 the GU edge at map weight; 03 the same edge close, with rust industrial parcels inside it; 04 a phantom dashed tick on a blank survey staff, no height (the code draws no line); 05 a solid square at true size in the snow (the first line drawn by size); 06 the same square as a gold fleck on a lit bench above the fog; 07 a solid bar at 5 MW on the gauge (the line as power); 08 a dashed line around the whole borough (temporary, not codified); 09 the line closes into the Polaris.
- Light, declared once and never varied: plan frames take a key from the upper left, az 315, el 24, casts to the lower right; oblique frames take the late October sun low in the south, placed in screen space at the upper left by the camera heading. Shadows are darkened ground hue, never black.

Motif state table:
| slide | D1 camera | D2 gold line |
|---|---|---|
| 01 | dusk oblique from the west, about 40 km out | hairline ring around the 3 percent cluster |
| 02 | equal-area plan, registered | the GU edge, map weight |
| 03 | the cluster at about 6x | the GU edge close, around the industrial parcels |
| 04 | at grade on the Tanana Flats, looking north | phantom dashed tick on a blank staff |
| 05 | 150 m plan, one muskeg plot | the solid square, true size |
| 06 | low oblique into last light | gold fleck on a lit bench |
| 07 | insert, orthographic | solid bar at 5 MW |
| 08 | plan, registered, civil twilight | dashed line around the borough |
| 09 | plan, registered, night | closes into the Polaris |

## VARIETY LEDGER CHECK, and this deck's required divergence
Last four hero structures: THE SPLIT SPECIMEN (10-19), THE PINNED RELIEF SHEET (10-20), THE FLOWN LINE (10-21), THE COMPOSING STONE (10-22). Last three atmospheres: THE MAP-TABLE LAMP, THE OCTOBER NOON OVER MAGNETITE, THE NORTH SKYLIGHT AT FOUR. Last two continuity devices: panorama rail with an aircraft tick, gold meaning the flown line, tonal arc; the ink law, a brass line, a stamp ticker, one skylight, an edge tease. Last three hooks: THE WRONG ADDRESS, THE ODOMETER, THE NAMED PARTY ANSWERS. Last three palettes: chart night, plaster and salmonberry; caesius and magnetite; type metal, oak and proof bond. Last two type pairings: Space Grotesk + Mono; Instrument Serif + Archivo + Mono. No.76 (THE DISTANCE, the same borough) and No.87 (the gigawatt ruler) are avoided too.
This deck: hero NEW: THE REGISTERED LAYER (one real zoning layer, reprinted per frame in a new medium, camera moving through one registered scene); atmosphere NEW: THE FIRST ICE FOG (a low October sun over real terrain, fog lying in the real lowlands); palette NEW: INVERSION SEASON (spruce jade, hoarfrost, industrial rust, alpenglow, gold for the line); type Fraunces + JetBrains Mono; hook NEW: THE ONE-WORD AUDIT; continuity a registered camera move and a gold line that migrates. No rail, no ticker, no ink law, no edge tease, no lamp.

## VARIANCE DIALS
design_variance 4 (a real GIS layer as the whole deck, rendered terrain, the definition argued by drawing; far from the still-life house centre of the last two runs); visual_density 2 (one large, best-modelled object per frame, deliberately, against the standing weakness); type_temperature 4 (Fraunces carries display and body, warm serif, with mono only as the instrument).

## PALETTE (roles fixed)
Night ground #050A12, slate step #16242F, deep step #0D1824. General Use film, spruce jade #2E6B5E (lit #4E8F7E, lee #1B4038). Every other district, hoarfrost #DCE6EA (shaded #A9BAC2). Industrial rust #A9502E (HI and LI only, the smallest areas). Ice fog #93A7B4, fog lit top alpenglow #EFB39B. Snow #F4F8FF, snow shade #B9C7D6, spruce black #18241F. Settled lamps (08, 09) amber #E0954A. Flag gold #FFC72C, the line only, drawn after the grade or held with AKPOST.holdInk. Display type #F4F8FF, body type #C9D3D9, label #A9B8C2, fixture #6E7F8C. On 05 (light frame) type is #0E1A22 and the fixture #5E6B76.

## TYPE SYSTEM
Fraunces (variable, opsz and wght) for display and body: display opsz 144 wght 560 tracking -2 percent leading 0.98, fitted with AK.fitText; body opsz 24 wght 400 at 32 to 34 px, leading 1.36, 600 to 660 px columns. JetBrains Mono 500 for kickers, labels, acreages and the counter, 24 px and up, tracked +8 percent, tabular. No italic accent words, no numbered section labels, no pills.

## SITE FIXTURE
Every frame: Polaris (gold four point star, SVG) and `ALASKA.AI` Fraunces 30 px wght 600 top left (x 80, y 60); counter `NN / 09` JetBrains Mono 24 px top right; `alaskaaihq.com` JetBrains Mono 19 px #6E7F8C bottom left (y 1290), data-decorative; coordinates `64°50'N · 147°43'W` [design] JetBrains Mono 19 px data-decorative bottom right. Fixtures at z-index 9 above every canvas, written by the deck helper `assets/js/akborough.js`.

## THE STANDING WEAKNESS, and what is different here
Artwork craft was the weakest criterion in 7 of the last 10 runs (mean 7.1). Here every frame's largest object is real land or one thing standing on it, built from committed data (the zoning layer, the borough terrain) and modelled under the declared light: the borough massif in PBR with real cast shadows (01, 06), slope and aspect hachure from the real DEM (02), raised paper terraces of the real districts (03), real ridgelines at grade (04), snow and spruce in a bench relief with long casts (05), a PBR enamel gauge frozen in ice (07), DEM stipple (08) and DEM engraving (09). Visual density 2 so each frame spends its craft on one object. Gold drawn after the grade. Every foot sits on a lit pool with a measured contact. 06 is built first.

## HONESTY GUARDS (bind every frame)
- The ordinance is PROPOSED and on the October 22nd agenda for referral. No frame says it was referred or adopted as a completed act (C03; the referral as an act was killed for want of minutes).
- 97 percent is acreage on the borough's zoning map, the showrunner's sum of the ACRES field the borough publishes (C63 to C67). Printed as "of the map" or "zoned acres", never "of the land", and the method note is on 02.
- No frame implies any data center has applied in the borough.
- 07 never implies data centers caused the October 12th alert; its own sentence carries the cause GVEA gave (C40).
- No frame states whether borough zoning reaches Eielson or Fort Wainwright (killed claim).
- The 50,000 square foot square on 05 and 06 is a footprint drawn to scale for size only, placed on a GU-1 polygon; no site is named or implied.
- Atmosphere (fog, sun, snow, spruce) is drawn and encodes nothing; no frame names a temperature or an inversion.

## CRAFT PLAN
| slide | primary mark-making | largest object, and how it is modelled |
|---|---|---|
| 01 | gpu render in three.js, PBR terrain from the borough DEM | the borough hill massif, lit faces warm under a low sun from the upper left with real shadow map casts into the valleys, snow albedo on high ground, the jade film draped from the zoning layer, exp2 fog in the ice fog hue |
| 02 | slope and aspect hachure from the real DEM | the General Use field in plan, stroke width from slope and rotation from aspect under the az 315 key, with the hoarfrost districts as flat paper with a lit lip and a cast |
| 03 | multi-material bench relief | the raised hoarfrost terrace of the Fairbanks to North Pole districts, chamfered paper walls with lit upper left and lee lower right faces, rust enamel industrial inlays with specular, casts onto the lit jade ground |
| 04 | real terrain ridgeline stack at grade | the near ridge of the Yukon-Tanana uplands, filled profiles stroked lit or lee by the real terrain normal, the fog floor luminous below it |
| 05 | bench relief of snow and spruce with long casts | the sunlit muskeg snow plot, micro relief Lambert lit, spruce crowns modelled with lit and lee sides, blue casts streaming to the lower right, the gold square lying on it |
| 06 | gpu render in three.js, PBR terrain with thin lens focus | the mid hill bench rising out of the fog, rim lit by the last sun, with a blurred near ridge as repoussoir and far ridges fading by atmospheric perspective, the gold fleck on the bench |
| 07 | gpu render in three.js, PBR enamel gauge in ice | the enamel staff gauge, clearcoat enamel with a grazing key from the upper left, chipped edges, frozen into a shelf ice slab with a lit pool, a contact cast and a collar |
| 08 | DEM driven weighted stipple | the borough at civil twilight, stipple density from the skyglow lit aspect of the real terrain, amber dots in the settled districts, with the dashed gold boundary |
| 09 | white line intaglio engraving from the DEM | the night borough in plan, modelled by swelled white lines whose lay wraps the hills, lit faces cut wide and lee faces cut thin under a raking virtual key, amber interdots in the settled districts |
Masterful depth frame: 06, the low oblique into last light, the mid hill bench rising out of the fog in tack sharp focus between a blurred near ridge (repoussoir, bleeding off the lower left) and far ridges fading by atmospheric perspective, one sun with real casts
Tonal arc: a dusk mid 01, plan darks 02 and 03, a lift at grade on 04, the brightest peak is 05 on sunlit snow, falling through last light on 06 and blue hour on 07, civil twilight on 08, the darkest close on 09 at night

## CLAIMS INDEX
(filled at the end of this section by the build; see the per-slide copy)
| claim | slide(s) |
|---|---|
| C01 | 02 |
| C03 | 08 |
| C04 | 08 |
| C05 | 05, 07, 09 |
| C06 | 05, 06 |
| C07 | 05 |
| C08 | 06 |
| C09 | 06 |
| C11 | 08 |
| C12 | 08 |
| C14 | 08 |
| C15 | 04 |
| C16 | 04 |
| C18 | 01, 02, 03, 04 |
| C19 | 04 |
| C32 | 08 |
| C34 | 07 |
| C35 | 07 |
| C36 | 07 |
| C37 | 07 |
| C40 | 07 |
| C63 | 02 |
| C64 | 02 |
| C66 | 01, 02 |
| C67 | 03 |
| C68 | 03 |
| C69 | 03 |
Every other claim is NOT USED on a slide (some feed the caption and the first comment).

## SLIDE 01, COVER, the oblique

**1. Beat.** Hook. The ordinance's soothing word "only" against the borough's own map. Plants: which two zones, and 97 percent of what?

**2. COPY, final.**
- Kicker: `UPDATE · FAIRBANKS DATA CENTERS` (31 chars)
- Headline line 1: `"Only" two zones.` (C18)
- Headline line 2: `97 percent of the map.` (C66)
- Fixtures: `ALASKA.AI`, `01 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]
12 words on the cover including the kicker.

**3. Reader takeaway.** In Fairbanks, the zones "only" allowed for big data centers are nearly the whole borough.

**4. Layout map.** Kicker cols 1 to 8, y 150. Headline cols 1 to 11, y 190 to 520, two lines, line 2 the figure. Terrain fills y 520 to 1350 and bleeds off three edges. Focal point the lit hoarfrost cluster with its gold ring at about (640, 860), on the right third. Eye path headline, then the ring, then the long jade land. Quiet zone the dusk sky behind the headline, y 120 to 520.

**4a. Lower-third treatment.** The terrain massif in modelled PBR tone runs through the whole lower third: the near western hills with sun-lit south faces, lee faces in cool fill and real shadow map casts into the valleys, the jade film on the lit slopes, and fog lying in the valley floors. Nothing flat, no plate.

**5. Depth plan.** Sky gradient, far ridges in fog, the Tanana Flats under fog, the cluster, near hills, DOM type, grain. Cues: atmospheric perspective (exp2 fog in #93A7B4), overlap of ridges, scale gradient, real shadow map casts, one key. Camera: world units of 1 km, vertical exaggeration 3, camera from the west-southwest about 40 km outside the boundary, 9 km up, heading 70, pitch -11, fov 42; horizon at about y 520 by construction (the camera is solved so the far boundary sits at y 560).

**6. Continuity device state.** D1 the establishing oblique. D2 a hairline gold ring around the hoarfrost cluster (the 3 percent). 

**7. Technique stack.** `three.js` via `AKT.setup` with `AKT.snapshot`, a terrain PlaneGeometry of 600 x 320 segments displaced from assets/geo/fnsb-dem.bin, MeshStandardMaterial with a CanvasTexture map rasterised from the zoning layer on the DEM's own lon/lat grid (jade #2E6B5E on GU, hoarfrost #DCE6EA elsewhere, snow albedo blended above 700 m), DirectionalLight sun (el 7, from the camera's upper left), 4096 shadow map, hemisphere fill #7F97C8 at 5:1, scene fog exp2 in #93A7B4. Graded with `AKPOST.grade` (exposure -0.05, saturation 0.98, contrast 1.06). The gold ring drawn after the grade on a 2D canvas from the projected outline of the non-GU polygons near Fairbanks (`AKT.projectPoint`). Grain via AK.grainOn. Seed 2026102301.

**8. Data-in-art mapping.** The jade film is the real GU-1 and GU-5 geometry (C63, C64), the hoarfrost is every other polygon (C67); terrain is the real DEM at vertical exaggeration 3 [design]. The ring follows the real cluster outline.

**9. Palette assignment.** Sky #16242F to #050A12, fog #93A7B4, jade #2E6B5E, hoarfrost #DCE6EA, snow #F4F8FF, alpenglow #EFB39B on lit crests, gold #FFC72C on the ring only. Type #F4F8FF on sky at about L* 10, contrast above 12:1.

**10. Type spec.** Kicker JetBrains Mono 500 26 px +8 percent #A9B8C2. Headline Fraunces opsz 144 wght 560, line 1 about 132 px, line 2 about 120 px, AK.fitText min 96 max 150 maxLines 1 per line, #F4F8FF, left aligned, max width 920.

**11. Iconography and anchor spec.** Anchor: the borough itself, real terrain and real zoning. Annotation: the gold ring, 1.6 px, around the cluster.

**12. Reference intent.** A National Geographic relief oblique at dusk, data-honest.

**13. Risk flags.** The cluster could vanish at thumb size under fog: fog density capped where the cluster sits, hoarfrost slightly emissive (0.12). The ring could look like a label circle: it follows the true outline, not a circle.

**14. Acceptance checklist.**
- [ ] Headline two lines, second line the figure, readable at 432 px
- [ ] Jade film visibly covers most of the visible borough
- [ ] The hoarfrost cluster reads as small and bright, ringed in gold
- [ ] Terrain reads lit and modelled with real casts, not flat
- [ ] Fog in valleys, not a rectangle
- [ ] Gold appears only on the ring and the Polaris

## SLIDE 02, PAYOFF, the plan

**1. Beat.** Pays the cover at once: the ordinance's own words, and the two districts by acre. Plants: the pale holes in the map, what is in them?

**2. COPY, final.**
- Kicker: `ORDINANCE NO. 2026-42`
- Headline: `The draft says "only" GU-1 and GU-5. They are nearly all of it.` (C18)
- Body: `Under today's code, the ordinance says, a large data center would be permitted only in these two General Use districts.` (C18)
- Label: `GU-1 · 4,420,232 ACRES` (C63)
- Label: `GU-5 · 197,540 ACRES` (C64)
- Method: `ACRES AS THE BOROUGH PUBLISHES THEM, SUMMED` (C63, C64)
- Fixtures: `ALASKA.AI`, `02 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** GU-1 and GU-5 are almost the whole borough map.

**4. Layout map.** Kicker y 150; headline cols 1 to 11, y 190 to 360, up to 2 lines; body cols 1 to 8, y 380 to 500. Map in the registered box [[90,520],[990,1250]]. GU-1 label with a leader into the eastern uplands at about (760, 760); GU-5 label below its block at about (600, 1150); method note bottom left inside the map margin at y 1240. Focal point the hoarfrost cluster's edge in gold at about (380, 980).

**4a. Lower-third treatment.** The southern half of the borough in slope and aspect hachure from the real DEM (stroke weight from slope, so the Tanana Flats read pale and the uplands dense), the GU-5 block's hachure and the dimmed relief beyond the boundary carry the lower third, with the GU-5 label leader landing on its polygon.

**5. Depth plan.** Night ground, dimmed relief outside the boundary, the GU hachure field, the hoarfrost paper districts raised 2 px with a lit lip and a cast, the gold edge, labels, grain. Cues: shadow (casts of the paper districts), light (lit lip upper left), overlap (paper over field), texture gradient (hachure density by slope).

**6. Continuity device state.** D1 the registered plan (shared with 08 and 09). D2 the GU edge at map weight 2.2 px gold.

**7. Technique stack.** `d3` geoConicEqualArea projection, registered box. `akhachure` slope and aspect hachure with height sampled from the DEM (cubic), jade ink #4E8F7E on #0D1824, clipped to GU polygons. Hoarfrost districts filled #DCE6EA with a paper tooth, lit lip and a 3 px cast to the lower right. Gold edge stroked after the grade. Graded with `AKPOST.grade` before the gold. Leaders declared in window.__akLeaders.

**8. Data-in-art mapping.** Equal-area projection, so visible area share is the true acreage share (C63 to C67). Hachure width from real slope [design].

**9. Palette assignment.** Ground #0D1824, hachure #4E8F7E lit to #1B4038 lee, hoarfrost #DCE6EA, gold #FFC72C on the edge only, labels #F4F8FF on dark plates? No plates: labels sit on routed quiet ground. Body #C9D3D9 on #050A12, above 11:1.

**10. Type spec.** Kicker Mono 500 24 px #A9B8C2. Headline Fraunces opsz 144 wght 560, fit 64 to 84 px, maxLines 2, width 920. Body Fraunces opsz 24 wght 400 32 px leading 1.36, width 640. Labels Mono 500 24 px #F4F8FF. Method Mono 400 20 px #A9B8C2 data-decorative.

**11. Iconography and anchor spec.** Anchor the borough in plan, real polygons. Annotation two leaders ending on the GU-1 and GU-5 polygons' own coordinates, 1.2 px #A9B8C2 with 5 px dot terminals.

**12. Reference intent.** A USGS shaded relief sheet, re-inked as a zoning proof.

**13. Risk flags.** Hachure too dense reads as fur: stroke spacing 6 px, width 0.4 to 2.2 px by slope. Label over hachure: labels sit in reserved routing, AKPOST.reserve with the ground colour if needed.

**14. Acceptance checklist.**
- [ ] The jade hachure field reads as terrain and covers nearly all of the borough
- [ ] The hoarfrost districts read as small paper cut-outs with a lit lip and a cast
- [ ] Both leaders land on their own polygons
- [ ] Gold only on the GU edge and the Polaris
- [ ] Method note present and small

## SLIDE 03, THE 3 PERCENT, the cluster

**1. Beat.** Everything that is not General Use, and the industrial land the code skips. Plants: why would a code point big loads past its industrial land?

**2. COPY, final.**
- Kicker: `EVERY OTHER DISTRICT`
- Headline: `Everything else fits in 3 percent.` (C67)
- Body: `Every district besides GU-1 and GU-5 covers 145,827 acres. Heavy Industrial is 3,555 of them, Light Industrial 5,929. Under today's code, the draft says, a large data center could go to neither.` (C67, C68, C69, C18)
- Labels: `HEAVY INDUSTRIAL`, `LIGHT INDUSTRIAL`, `FAIRBANKS`, `NORTH POLE`
- Fixtures: `ALASKA.AI`, `03 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** The non-General-Use districts are a small cluster, and industry is a sliver of that.

**4. Layout map.** Text cols 1 to 8, y 150 to 520. Relief y 540 to 1350, bleeding off left, right and bottom: the cluster from Fairbanks (left) to North Pole (lower right) at about 6x, raised as terraces. Focal point the largest rust industrial parcel at about (520, 900). Labels with leaders to the largest HI and LI parcels and place names at their own coordinates.

**4a. Lower-third treatment.** The cluster's terraced paper run toward North Pole fills the lower third: hoarfrost terraces with lit upper left walls and lee lower right walls, casts falling onto the lit jade ground with its paper tooth, and rust enamel inlays catching a specular, all of it bleeding off the bottom edge.

**5. Depth plan.** Jade ground with tooth, hoarfrost terrace 1 (all non-GU) raised 7 px, rust enamel inlays raised a further 2 px, gold edge, labels, grain. Cues: cast shadow, lit and lee walls, cavity occlusion, specular on enamel.

**6. Continuity device state.** D1 the cluster at about 6x, same projection family re-fitted. D2 the GU edge in gold, close, around the rust parcels.

**7. Technique stack.** `AKBENCH.relief` with height from the rasterised district mask (signed distance chamfer 5 px), materials jade, hoarfrost paper, rust enamel; light az 315 el 24; spec on enamel; shadow and AO on. `d3` for the projection and rasterising. Gold edge after `AKPOST.grade`. Contacts declared on the largest rust parcel.

**8. Data-in-art mapping.** The terraces are the real non-GU polygons (C67); rust inlays are the real 12 HI and 43 LI polygons (C68, C69). Heights are [design].

**9. Palette assignment.** Jade ground #2E6B5E lit #4E8F7E, hoarfrost #DCE6EA shaded #A9BAC2, rust #A9502E, gold #FFC72C edge only. Text on the night band above the relief.

**10. Type spec.** Kicker Mono 500 24 px. Headline Fraunces fit 64 to 84 px maxLines 2. Body Fraunces 32 px, width 660. Labels Mono 500 24 px on routed ground.

**11. Iconography and anchor spec.** Anchor the real cluster. Leaders to the HI and LI parcels' own centroids.

**12. Reference intent.** A paper architectural site model under one lamp.

**13. Risk flags.** Terrace walls on tiny parcels become noise: chamfer 5 px, small polygons under 0.5 px area are merged by the raster. Body length versus the relief top edge checked before render.

**14. Acceptance checklist.**
- [ ] Hoarfrost terraces read raised with lit and lee walls and casts
- [ ] Rust parcels read as distinct enamel inlays
- [ ] HI and LI leaders land on rust parcels of the right type
- [ ] FAIRBANKS and NORTH POLE at their own places
- [ ] Gold only on the edge and the Polaris

## SLIDE 04, WHY THERE, at grade

**1. Beat.** Why the code points there: a 2005 plan and a code with no word for a data center. Plants: the code draws no line, so who draws one?

**2. COPY, final.**
- Kicker: `THE OLD MAP`
- Headline: `Written in 2005, before AI demand.` (C15)
- Body: `The draft says the Comprehensive Plan was last updated in 2005 and the zoning code doesn't address data centers as a use. General Use allows the widest range of uses in the borough, so that is where they fall.` (C15, C16, C19, C18)
- Fixtures: `ALASKA.AI`, `04 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** The rules predate AI demand, so the default is the widest zone.

**4. Layout map.** Text cols 1 to 8, y 150 to 560, in sky. Horizon at y 700. Ridges y 600 to 1000, the fog floor y 1000 to 1100, the near flats y 1100 to 1350 with a blank survey staff standing at (880, 1110) carrying a phantom gold tick. Focal point the staff.

**4a. Lower-third treatment.** The near flats as filled ridgeline bands with lit and lee strokes weighted by depth, the fog floor's luminous lit surface where it meets the hills, and the survey staff with its lit pool of snow and its contact shadow carry the lower third, toned edge to edge.

**5. Depth plan.** Sky, far ridges lerped to fog by (i/n)^1.4, mid ridges, fog floor, near flats, the staff, DOM type, grain. Cues: atmospheric perspective, overlap, scale gradient, fog, one key (sun low upper left).

**6. Continuity device state.** D1 at grade. D2 a phantom dashed gold tick on the staff at no height.

**7. Technique stack.** NEW: ridgeline stack from the borough DEM (port of akvalley's method onto fnsb-dem.bin in the deck helper): profiles perpendicular to heading 0 from a station on the Tanana Flats south of Fairbanks, filled with ground colour then stroked lit or lee by the real normal. Fog floor a height-gated luminous band. Staff drawn in 2D with a lit face and a lee face. `AKPOST.grade`; gold tick after it.

**8. Data-in-art mapping.** Real ridgelines [design], VE 2. No quantity encoded.

**9. Palette assignment.** Sky #16242F to #2A3A4A low, ridges #18241F to fog #93A7B4, lit strokes #EFB39B, fog top #EFB39B, staff enamel #DCE6EA, gold the tick only.

**10. Type spec.** As 03.

**11. Iconography and anchor spec.** Anchor the real hills north of town; the staff as the deck's survey instrument (planted blank here, graduated on 07).

**12. Reference intent.** A Bradford Washburn panorama, drawn as engraving.

**13. Risk flags.** Profiles reading as an audio waveform: tone first, strokes second, weight by depth. The staff reading as a post: give it graduations without numbers.

**14. Acceptance checklist.**
- [ ] Ridges read as real terrain with depth
- [ ] Fog floor luminous, not flat
- [ ] Staff present with a phantom gold tick and a contact
- [ ] Body readable on the sky

## SLIDE 05, THE DEFINITION, the square

**1. Beat.** The turn: the draft's line is a size, not a place. Plants: how big is that, against the land?

**2. COPY, final.**
- Kicker: `THE DEFINITION`
- Headline: `The pause makes news. The definition decides.`
- Body: `Under the draft, a data center is large at 5 MW of peak demand, more than 50,000 square feet of data center floor, or 5 MW of onsite generation. Any one test is enough.` (C05, C06, C07)
- Dimension label: `50,000 SQUARE FEET, DRAWN TO SCALE` (C06)
- Scale bar: `50 M` [design]
- Fixtures: `ALASKA.AI`, `05 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** Large means 5 MW or 50,000 square feet, any one test.

**4. Layout map.** Text cols 1 to 8 on the snow, y 150 to 560, dark type. The square 518 px a side centred at (600, 930), from y 671 to 1189, slightly rotated 6 degrees; the dimension call along its lower edge. Spruce scattered by rejection sampling outside text boxes. Focal point the square's upper left corner.

**4a. Lower-third treatment.** Sunlit snow micro relief lit from the upper left, spruce crowns modelled with lit and lee sides, and their long blue casts streaming to the lower right across the full width, with the gold square's lower edge, its dimension call and the 50 m scale bar on the snow.

**5. Depth plan.** Snow surface, casts, spruce crowns, gold square, labels, grain. Cues: cast shadows, lit and lee crowns, scale (spruce crowns at true size), texture.

**6. Continuity device state.** D1 a 150 m plan. D2 the solid gold square at true size.

**7. Technique stack.** `AKBENCH.relief` height = snow micro relief (seeded fbm) plus spruce cones (radius 4 to 7 px, height 18 to 40 px), materials snow and spruce, light az 315 el 14, shadow on, softness 6. Spruce rejection-sampled away from type boxes. Gold square stroked after `AKPOST.grade` at 3 px with a dark 1 px casing. Scale 7.6 px per metre [design]: 68.15 m a side is 518 px, asserted in window.__akAssert.

**8. Data-in-art mapping.** Square side = the square root of 50,000 square feet, 68.15 m, at 7.6 px per metre [design] (C06).

**9. Palette assignment.** Snow #F4F8FF lit, #B9C7D6 shade, casts #7F93AE, spruce #18241F lit #2E4A3E, gold #FFC72C square only. Type #0E1A22 on snow about L* 92, above 14:1.

**10. Type spec.** Kicker Mono 500 24 px #3A4A56. Headline Fraunces fit 64 to 84 px maxLines 2 #0E1A22. Body Fraunces 32 px #1B2A33 width 640. Dimension label Mono 500 24 px #0E1A22.

**11. Iconography and anchor spec.** Anchor the square at true size; scale bar 50 m [design] bottom right.

**12. Reference intent.** An aerial survey photograph of a winter muskeg, re-drawn.

**13. Risk flags.** Light frame contrast against the fixture: fixture ink switched to #5E6B76. Bench relief time: region rendered at scale 2 over the full frame, kept under 12 s.

**14. Acceptance checklist.**
- [ ] Snow reads sunlit with modelled micro relief
- [ ] Spruce read as trees with long casts to the lower right
- [ ] Square is gold, true size per the assertion, with its dimension call
- [ ] Dark type fully legible on snow

## SLIDE 06, BREATHER, THE PAUSE

**1. Beat.** Rest beat with one fact: the pause and its end date; the "large" footprint is a fleck in the land. Plants: if land isn't the limit, what is?

**2. COPY, final.**
- Body: `If adopted, no applications accepted and none approved through December 31st, 2027.` (C08, C09)
- Leader label: `50,000 SQUARE FEET, TRUE SIZE` (C06)
- Fixtures: `ALASKA.AI`, `06 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** Nothing big gets permitted through 2027, and "large" is tiny against the land.

**4. Layout map.** BREATHER — the deck rests here after the definition and before the grid, so the frame carries one sentence and one image. Sentence cols 1 to 9, y 170 to 330. Terrain fills the frame; the lit bench with the gold fleck at about (690, 860); leader from the label at (720, 760) down to the fleck.

**4a. Lower-third treatment.** BREATHER — the deck needs a rest between the definition and the grid; the lower third still carries the blurred near ridge repoussoir and the lit fog surface, modelled tone, and the slide sets `data-breather`.

**5. Depth plan.** Sky with last light, far ridges in fog, the fog sea, the mid hill bench (focal plane), the near ridge (blurred repoussoir), DOM type, grain. Cues: thin lens depth of field, atmospheric perspective, overlap, scale, real shadows, rim light. Camera 1.1 km up over the Chena valley, heading 200, pitch -8, fov 38, VE 2.

**6. Continuity device state.** D1 low oblique into last light. D2 the square, now a gold fleck on the bench, placed at a real lon and lat inside a GU-1 polygon and projected.

**7. Technique stack.** `three.js` via `AKT.setup`, a high resolution terrain patch of the DEM around the station (segment 120 m), MeshStandardMaterial with the jade film texture, low sun el 3 from the camera's upper left, 4096 shadow map, exp2 fog, a separate depth render for a 2D thin-lens blur (focus on the bench, near ridge strongly blurred). The square as a flat gold quad on the bench, re-held with `AKPOST.holdInk` after `AKPOST.grade`.

**8. Data-in-art mapping.** The square is 68.15 m a side in world units (C06) [design]; terrain is the real DEM [design].

**9. Palette assignment.** Sky #2A3A4A to #EFB39B at the horizon, fog #93A7B4 lit top #EFB39B, jade film dim, gold fleck #FFC72C only. Type #F4F8FF on sky.

**10. Type spec.** Body Fraunces opsz 36 wght 420 44 px leading 1.24, width 880, #F4F8FF. Leader label Mono 500 24 px.

**11. Iconography and anchor spec.** Anchor the real hills; leader 1.2 px ending on the fleck's projected coordinates.

**12. Reference intent.** A Galen Rowell long-lens alpenglow, data-honest.

**13. Risk flags.** The fleck too small to see: placed on a lit face, 14 px minimum projected width, gold held after grade. Depth blur cost: blur from a depth texture in 2D, 3 passes.

**14. Acceptance checklist.**
- [ ] One sharp focal plane on the bench, near ridge blurred
- [ ] Fog sea reads as volume with a lit top
- [ ] Gold fleck visible at full size and its leader lands on it
- [ ] Sentence legible on the sky

## SLIDE 07, THE GRID, the gauge

**1. Beat.** Is 5 MW large? Put it on the same linear scale as GVEA's alert lines. Plants: so where should the line be?

**2. COPY, final.**
- Kicker: `THE GRID`
- Headline: `Is 5 MW large? Ask the reserve.` (C05)
- Body: `GVEA's Level 1 alert starts below 38 MW of reserve, Level 2 below 15 MW. Its first alert, October 12th, was a Level 2, with two units in maintenance and a third offline.` (C36, C37, C34, C35, C40)
- Gauge labels: `38 MW LEVEL 1` (C36), `15 MW LEVEL 2` (C37), `5 MW DRAFT LINE` (C05)
- Fixtures: `ALASKA.AI`, `07 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** The draft's 5 MW is a third of GVEA's Level 2 reserve line.

**4. Layout map.** Text cols 1 to 7, y 150 to 600. The gauge at x 760 to 860, zero at y 1200, 22 px per MW, so 38 MW at y 364 and 15 MW at y 870 and 5 MW at y 1090. Labels to the right? No: to the left of the gauge at x 480 to 740, right aligned, below the body (y 870, 1090) and the 38 MW label at y 364 sits beside the headline column's end. Ice slab y 1180 to 1350.

**4a. Lower-third treatment.** The shelf ice slab in PBR with frazil pans and a lit top surface, the gauge's frozen foot with its lit pool, its contact cast and its ice collar, and the 5 MW and 15 MW labels with their short leaders to the marks on the gauge.

**5. Depth plan.** Blue hour sky, far shore line, ice slab, gauge, labels, grain. Cues: shadow, specular, overlap, fog.

**6. Continuity device state.** D1 the insert of the staff planted on 04, now graduated. D2 a solid gold bar at 5 MW.

**7. Technique stack.** `three.js` via `AKT.setup`, an OrthographicCamera for the gauge (no perspective on the quantity), a BoxGeometry staff with a CanvasTexture of graduations (1 MW ticks, an E bar every 5 MW, no numerals), clearcoat enamel MeshPhysicalMaterial, an ice slab with a normal noise texture, `AKT.environment` at 0.6, directional key from the upper left. Gold bar drawn after `AKPOST.grade`. Marks declared in data-scale with every tick's meaning.

**8. Data-in-art mapping.** Linear scale, 22 px per MW [design]: 38 MW (C36), 15 MW (C37), 5 MW (C05). The staff's ticks are one per MW.

**9. Palette assignment.** Sky #0D1824 to #2A3A4A, enamel #DCE6EA, graduations #16242F, ice #A9BAC2 to #5E7486, gold #FFC72C bar only.

**10. Type spec.** As 03; gauge labels Mono 500 24 px right aligned.

**11. Iconography and anchor spec.** Anchor the gauge; three labels with short leaders to their marks.

**12. Reference intent.** A USGS river gauge photographed at freeze-up.

**13. Risk flags.** A reader computing a causal link: the body carries GVEA's own cause. Scale honesty: orthographic camera, asserted marks.

**14. Acceptance checklist.**
- [ ] Gauge linear, marks at the declared positions
- [ ] Gold only on the 5 MW bar and the Polaris
- [ ] Enamel reads as enamel with clearcoat, ice reads as ice with a contact
- [ ] All three labels legible and on their marks

## SLIDE 08, NEXT, the clock

**1. Beat.** What happens next, and why now. Plants: the reader's own answer.

**2. COPY, final.**
- Kicker: `NEXT`
- Headline: `The line gets argued now.`
- Body: `The agenda sends the draft to the Planning Commission, recommendation due in 90 days. A commission work session on the final plan is set for October 27th. If adopted, a study of energy, air, water and noise follows within six months.` (C03, C04, C32, C11, C12)
- Boundary label: `TEMPORARY, NOT CODIFIED` (C14)
- Fixtures: `ALASKA.AI`, `08 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** The Planning Commission has 90 days; the moment to argue the number is now.

**4. Layout map.** Text cols 1 to 8, y 150 to 520. Registered plan in the box [[90,520],[990,1250]]; dashed gold borough boundary; label at the boundary's south edge.

**4a. Lower-third treatment.** The stippled southern borough at civil twilight, its south facing slopes lit by skyglow in denser stipple and the Tanana Flats in sparse dots, amber basin dots in the settled districts, and the dashed gold line crossing it with its label.

**5. Depth plan.** Night ground, stipple terrain, amber dots, dashed boundary, labels, grain. Cues: light (skyglow-lit slopes), texture density gradient, overlap.

**6. Continuity device state.** D1 the registered plan at civil twilight. D2 the dashed gold line around the borough.

**7. Technique stack.** `d3` registered projection; `AKSTIPPLE` weighted stipple with density from the DEM's skyglow-lit aspect (light az 200, el 6); amber dots inside non-GU polygons; dashed boundary (phantom dash 10 on 7) after `AKPOST.grade`.

**8. Data-in-art mapping.** Stipple density from real aspect and slope [design]. Amber dots only in the real non-GU polygons (C67).

**9. Palette assignment.** Ground #050A12, stipple #9AA9C9 to #DCE6EA, amber #E0954A, gold #FFC72C dashed line only.

**10. Type spec.** As 03.

**11. Iconography and anchor spec.** The borough boundary as the anchor.

**12. Reference intent.** A night satellite composite, hand stippled.

**13. Risk flags.** Stipple density moire at thumb: min radius 0.7 px, blue noise.

**14. Acceptance checklist.**
- [ ] Stipple reads as terrain lit from the south
- [ ] Dashed gold boundary closed around the borough
- [ ] Amber only in the settled districts

## SLIDE 09, CLOSE, the night borough

**1. Beat.** The single ask.

**2. COPY, final.**
- Headline: `Is 5 MW the right line for "large" in Fairbanks?` (C05)
- Fixtures: `ALASKA.AI`, `09 / 09`, `alaskaaihq.com`, `64°50'N · 147°43'W` [design]

**3. Reader takeaway.** A question to answer in the comments.

**4. Layout map.** Question cols 1 to 11, y 170 to 480. Engraved borough in the registered box; the Polaris larger at the top right of the borough at about (900, 560) where the gold line closes into it.

**4a. Lower-third treatment.** The engraved southern borough in white line intaglio, swelled lines wrapping the hills so the lay itself models the relief under a raking light, with amber interdots in the settled districts and the borough edge in a lit hairline.

**5. Depth plan.** Ink ground, engraving, interdots, Polaris, type, grain. Cues: light (raking virtual key), line swell, texture.

**6. Continuity device state.** D1 the registered plan at night. D2 the line closes into the Polaris.

**7. Technique stack.** `AKENGRAVE.create` surface() with form from the DEM (pre-sampled to a 4 px lookup), seed "even", light az 315 el 24 virtual; amber interdots inside non-GU polygons; Polaris SVG.

**8. Data-in-art mapping.** Engraving from the real DEM [design]; amber dots in the real non-GU polygons (C67).

**9. Palette assignment.** Ground #050A12, engraving #9FB2BE to #DCE6EA, amber #E0954A, gold Polaris.

**10. Type spec.** Question Fraunces opsz 144 wght 560 fit 80 to 110 px maxLines 3 #F4F8FF.

**11. Iconography and anchor spec.** Polaris 64 px gold four point star.

**12. Reference intent.** A banknote engraving of the Interior at night.

**13. Risk flags.** Engraving moire at thumb: gap 4 px, swell 0.4 to 1.8 px.

**14. Acceptance checklist.**
- [ ] One question, no source note
- [ ] Engraving wraps the hills, not a uniform hatch
- [ ] Polaris and wordmark present

## BUILD RECONCILIATION
What the build changed against this plan, and why (written after round 2 of pixel review; the machine block below is generated by gate_status.py --sync).
- Copy, accuracy: the copywriter queried three attributions. Slide 03's last sentence is now "By the draft's own reading of today's code, neither one qualifies." (the ordinance names GU-1 and GU-5, never industrial land, C18). Slide 07 says the first alert "reached Level 2" (C35 could describe an escalation). Slide 08 names the October 27th session as one on the final Comprehensive Plan (C32). The caption hook and GVEA line changed to match.
- Slide 01: the gold hairline now rings every visible non General Use district, not only the Fairbanks to North Pole run, so the fence reads as around all of the 3 percent. Fog is denser and the sky below the horizon is the fog colour.
- Slide 03: the cluster window was zoomed about 1.3x so the run fills the lower third; Heavy and Light Industrial carry separate enamels (deep oxide, lighter rust) so each leader lands on its own type.
- Slide 04: horizon near y 650 rather than 700; the near flats carry real black spruce in perspective (true positions, true height x1.5 [design]) in place of filled ridgeline bands alone; the phantom tick is 4.5 px and about 280 px long.
- Slide 05: the scale bar moved to the lower left, clear of the square's corner; the dimension call runs along the top edge; casts are drawn as an explicit layer (az 315, el 14, shortened to 0.62 of true length [design]).
- Slide 07: the gauge sits at x 700 to 790 with labels to its right as two-line stacks; the 38 and 15 MW marks are full-width bars; the shelf edge sits at y 1166 with an open lead and frost smoke beyond it.
- Slide 08: the outside-borough stipple falls to zero within about 36 px of the edge; amber has no glow.
- Slide 09: the cross lay was dropped; only the borough's outer edge is drawn; the Polaris sits on the borough's north eastern vertex.
- Shared furniture: akborough.js's terrain detail is now two non-commensurate rotated layers (a single periodic tile printed as a lattice on 01 and 06).
- Craft cycle (round 5, after score 1 of 8.535 with art 7.0): 03 relief starts at y 560 and the night fades the ground only, never a terrace; 04's body cut to one sentence pair and a near row of black spruce bleeds off the foot; 05 casts are per-crown wedges anchored at each crown, fading along their length; 07 gets a sharper clearcoat stripe, a darker lee edge, rime on every long graduation, softer ice and thinner smoke under the label column; 09's swell is driven harder by the light and the borough edge is now solid gold closing into the Polaris (08's dashed line made permanent, the D2 close). Caption: 'The two zones it names', 'Its first test is 5 MW'.
- 08 keeps its skyglow light (az 200, el 6) on purpose: the deck's plan key is az 315, and the flow critic noted the same hills flip relief between 02 and 08. Civil twilight comes from the south in late October; the stipple reads as lit terrain to both its critics.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-10-23. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[WARN] qa.py          WARN, 0 fails, 2 warns
[WARN] dossier_check  WARN, 9 dossiers, 0 fails, 1 warns
[PASS] reconciled     BUILD RECONCILIATION present, 12 line(s), 3016 chars
[PASS] caption_check  PASS, 897 chars, hook 118, 3 hashtags
[PASS] word_ban       word_ban: 0 banned word(s) in out/2026-10-23 and the docket
[PASS] copy_sync      copy_sync_check: PASS -- 37 authored slide strings all present in the render; alaskaaihq.com on every slide; no banned slide string; no curl
[PASS] aggregate      aggregate_check: PASS -- 9 aggregate assertion(s) detected, 9 declared -> out/2026-10-23/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 27 claims indexed, 0 declared counts checked, 6 body quote(s) checked, 0 11a region set(s) checked, 0 drift(s)
[PASS] tonal_arc      brightest 05, darkest 08, span 78.1 L*, as declared
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.083 (fail at 0.60), max pair 0.269, drawn share 67% (110 drawn vs 54 block
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] ledger_guard   LEDGER GUARD: PASS, 7 cron-written file(s) untouched
[PASS] docket_dates   docket dates clean at 2026-10-23: 406 assertions over 6 fixtures and 37 ledger items
[PASS] gas_watch      80 day(s) on record, 66 verified, no gaps, latest 2026-10-23, EIA through 202607 over 131 months, model misses by 6.82%
[PASS] gas_watch_live PASS, checked 2026-10-24T06:17:13Z
[PASS] cron_health    7 scheduled workflows audited at 2026-10-24T06:17:26.446244Z
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-10-23 (272 generated files)
[PASS] assemble       9 slides, pdf vector 10.21 MB, 9 thumbs, sources verified
[PASS] score          8.633 / 10 vs threshold 7.7, scorer says passes=True
[PASS] ship_gate      scored 8.63 against a threshold of 7.70; craft floor closed, one craft cycle ran on frames [3, 7, 4, 5, 9] (art 7.0 -> 7.3)
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```

