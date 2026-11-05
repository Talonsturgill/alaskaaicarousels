# STORYBOARD, run 2026-11-04, carousel No.105

## THESIS

The Army's own record of the 11th Airborne's drone work this fall publishes a scoped first and a list of
medals, and no measurements; the Alaska problems on that record (added weight, cold that drains a battery,
mountains in the way, snow) are being answered by named soldiers, by hand. Arctic drone readiness here reads
as a maintenance problem solved from the bottom up, not as a purchase.

Robotics beat only. Every drone in the record is a first-person view drone or a relay flown by people; none
of the three Army articles mentions AI or autonomy (C01 notes), and no frame implies either.

Document title (PDF): `Weight, cold, mountains. The Army's Alaska drone, taken apart.` (61 characters; the
copywriter may tighten under 60).

## ARC, nine frames

01 COVER, hook: the quad exploded into its parts with three gold balloons on the payload point, the battery and
   the antenna. Weight. Cold. Mountains. Plants: what goes wrong at each numbered part?
02 PAYS: the record itself. The first kinetic drone strike in the Richardson Training Area, the unit, the dates
   on a true-scale rail, who flew alongside, and the scope (not the Army's first, per Army Recognition).
   Plants: before any live strike they flew the weight. Why?
03 WEIGHT (balloon 1): unarmed test flights to learn how added weight changes maneuverability; the master
   trainer named. Plants: how much weight? The Army never said.
04 BREATHER, THE BLANK PLATE: the five things the Army did not identify (model, payload mass, endurance,
   engagement range, measured accuracy). Plants: so what did the record publish? What soldiers built.
05 COLD (balloon 2): a private hand-sewed a passive battery vault that runs on body heat and radiant barriers.
   The warmest frame in the deck. Plants: you can carry cold against your body, you can't move a mountain.
06 MOUNTAINS (balloon 3): first place at Angel Ascent went to a Skydio drone relay for mountain terrain; a real
   Chugach profile drawn to show why a relay helps. Plants: not every fix flies.
07 SNOW (balloon 4): a metal gunner hatch cover, snow-proof, about $300 in materials, the record's only price.
   Plants: the full list is longer.
08 KEEPER: Angel Ascent as a parts list, every entry the Army named, the format and the medals.
09 CLOSE, single ask: put back together, at rest; "the best ideas come from the bottom up"; what problem
   should soldiers bring to the next one?

Temperature shifts at 04 (rest, the cold machine frames end) and peaks at 05 (heat), returns to cool steel and
paper, and ends dark at 09.

## SLIDE COUNT RATIONALE

Nine. Each content frame carries a different line of the record and a different object (the exploded quad, a
dated rail, the assembled quad under load, a data plate, a sewn pouch, a mountain section, a steel hatch, a
parts sheet, the quad at rest). Merging the hatch into the keeper would lose the record's only price as a
picture; merging the blank plate into 03 would bury the deck's sharpest analytical beat.

## HOOK ARCHETYPE

NEW: THE THREE-PART TEARDOWN. The cover names three physical problems in three words and shows the machine taken
apart with three numbered parts, so the frame promises three payoffs rather than asking a question, quoting a
ballot or setting a sentence against a drawing. Not the reversed question, the partner as drawn or the
four-word ballot.

## NARRATIVE STRUCTURE

NEW: TEARDOWN AND REASSEMBLY. The machine apart (01), the record (02), each problem with its fix in the cover's
order (03 weight, 05 cold, 06 mountains) with the blank plate between the first and second (04), a fix that
does not fly (07), the parts list (08), the machine together again (09).

## CONTINUITY SYSTEM

D1 CAMERA MOVE ON ONE MODEL. One quad built by `assets/js/akdrone.js` (seeded, deterministic, carbon twill,
anodised steel, copper windings) is the GPU subject of 01, 03 and 09: exploded and seen from above at three
quarters (01), assembled and hovering in an orthographic dimetric elevation under drafting vectors (03),
assembled and at rest on a frosted floor from low at three quarters (09). Same materials, same key.

D2 THE BALLOON STRIP. Under the counter at top right, four 26 px drafting balloons numbered 1 to 4 in mono. On
01 balloons 1 to 3 are hollow gold rings; 02 the same; 03 fills 1 gold; 04 shows all as frost-ink rings with a
dashed outline (the blank frame, nothing answered); 05 fills 1 and 2; 06 fills 1 to 3; 07 adds balloon 4 filled;
08 and 09 all four filled. Gold fill means "answered on the record by a soldier". The strip is the progress
device as well as the counter.

D3 ONE COLD KEY. A single large cool softbox key, colour `#E8F0FF`, upper left and behind (screen azimuth 300,
elevation 34), fixed for every frame in every renderer. Casts fall to the lower right on every frame. Fill is
the cool floor bounce at about 1 to 5.

D4 PALETTE ARC TO KEPT HEAT, measured as the tonal arc (CRAFT PLAN). Steel and carbon cold on 01 to 04, the
ironbow heat peak on 05, steel and snow on 06 and 07, paper on 08, night on 09.

No edge tease on a line, no ink law of statuses, no desk module, no lamp key, no dateline, no reveal: none of
the last two decks' devices.

## VARIETY LEDGER CHECK, and this deck's required divergence

Last four hero structures: the order's sentence over the freeze-up coast (No.101), the idle transformer on the
Narrows (No.102), the sawn inlet and its sheets (No.103), the lamp left on, a walnut desk still life (No.104).
Last three atmospheres: Southeast November stratus rain, clear moon over glacial flour, one tungsten lamp after
the polls close. Last three hooks: the reversed question, the partner as drawn, the four-word ballot. Last three
palettes: stratus slate and pad green, glacial flour and chart magenta, lamplit walnut and oxblood. Last two
type pairings: Fraunces with Bricolage, Archivo with Instrument Serif.

This deck: hero NEW: THE ALASKA DRONE TAKEN APART, a technical-manual teardown of one machine with each figure
drawn by a different instrument (GPU exploded view, engraved rail, orthographic force diagram, bas-relief data
plate, thermal image, drafted terrain section, plan relief, wireframe parts sheet). Atmosphere NEW: COLD BAY
SOFTBOX, one cool overhead softbox in a dark maintenance bay at sub-zero, frost on the floor, no warm light
anywhere except the battery's own heat on 05. Palette NEW: CARBON, FOIL AND IRONBOW. Type Unbounded with Manrope
and JetBrains Mono, no serif (Unbounded absent from the last twelve decks). Only one DEM frame (06); the last
ten decks used terrain on six.

## VARIANCE DIALS

DESIGN_VARIANCE 4, VISUAL_DENSITY 3, TYPE_TEMPERATURE 1. Yesterday was 4/2/3 with a serif for people's words; the
day before 3/4/5. Today is the coolest voice possible in the library, a wide geometric display and a grotesk with
mono, because the subject is a machine and its manual; density 3 because each frame carries one object plus its
drafting furniture.

## PALETTE (roles fixed)

| role | hex |
|---|---|
| bay night | `#060A10` |
| graphite floor, panel | `#101820`, `#18222D` |
| floor pool (lit ground) | `#26323F` |
| carbon twill, edge | `#1A1D22`, `#3A414B` |
| anodised steel | `#B8C2CC` |
| radiant foil | `#DCE3EA` |
| frost ink (drafting lines, labels) | `#8CC9E3` |
| phantom ink (what was not published) | `#5B6977` |
| snow | `#F4F8FF` |
| type primary, body, label | `#EEF3F8`, `#CBD5DF`, `#B9C7D4` |
| site fixture | `#5B6B7A` |
| ironbow heat ramp, 05 ONLY | `#2A0B4A`, `#6E1468`, `#B42652`, `#DE4A2A`, `#F48C28`, `#FFCE60`, `#FFF6D6` |
| flag gold | `#FFC72C` |

Flag gold means "answered on the record by a soldier": the filled balloons, the gold leader rings on the parts
that a soldier's fix answers, the relay on 06, the $300 on 07, the first-place row on 08, plus the Polaris and
the counter slash. Gold in a graded canvas is restored with `AKPOST.holdInk` as the last art op; DOM and SVG
gold is drawn after the grade by construction.

## TYPE SYSTEM

Display Unbounded, wght 560, tracking -0.02em, leading 1.04, `#EEF3F8`, fitted with `AK.fitText` (cover max 104,
headlines max 84, min 58, maxLines 3). Body Manrope 500, 33 px, leading 1.38, `#CBD5DF`, max width 880 px.
Kickers and labels JetBrains Mono 500, 24 px, tracking 0.12em caps, `#A9BCCD` or frost ink. Quotes are Manrope
500 roman inside straight quotes (no italic accent words).

## SITE FIXTURE

Every frame: `alaskaaihq.com` in JetBrains Mono 19 px `#5B6B7A`, bottom left at x 80, bottom 62, data-decorative,
with a dark halo. Wordmark `ALASKA.AI` in Unbounded 600 22 px `#C9D4DE` top left at (80, 62), the gold Polaris
glyph beside it. Counter `NN / 09` mono 22 px top right, the slash in gold. Coordinates footer bottom right only
on the Angel Ascent frames 05 to 08 (Fairbanks from the gazetteer, `64°50'N 147°43'W`); no frame carries a
coordinate that could locate the Richardson Training Area.

## THE STANDING WEAKNESS, and what is different here

Artwork craft was the weakest criterion in 6 of the last 10 runs (mean 7.18). Three changes. (1) Every frame is a
drawing of ONE object, and that object is the most modelled thing in it: PBR with twill and IBL, a raymarched or
per-pixel relief, a thermal field with fabric form, a hatched section with a lit skin. (2) No mark-making on more
than three frames, and the shared GPU model never paints a ground for 2D frames (No.104's shared desk failed on
six frames at once). (3) Every DEM sample that is shaded is Catmull-Rom C1, every per-pixel field is computed at
the device pixel, grain is `AKPOST.grade` grain at size 1.

## HONESTY GUARDS (bind every frame)

- "First" is always scoped: the first kinetic drone strike within the Richardson Training Area (C04, C10). Army
  Recognition's caution is attributed to Army Recognition (C13).
- No frame says or implies the training area is on JBER or near Anchorage (killed claim). The 06 profile is
  labelled as a drawing of line of sight, not the site.
- No performance figure exists (C12). Every payload is drawn in phantom line, every dimension call that would
  carry a measurement says "NOT PUBLISHED", the heat legend on 05 has no scale.
- The quad is generic: `[design]` and never sized, never a model name. The vault layers, the hatch shape and the
  ridge positions are studio drawings and say so where they appear.
- No explosion, no target, no strike art. The penetrators (C23) are named on 08 and never drawn.
- Quotes verbatim only (C10, C25, C31). Pereira's unit is not named anywhere (it is not in the record).
- No AI or autonomy wording on any frame.

## CRAFT PLAN
| slide | primary mark-making | largest object, and how it is modelled |
|---|---|---|
| 01 | GPU PBR render (akthree) of the exploded quad | the carbon frame plate with its four arms, twill albedo and roughness under the cool softbox, anodised standoffs and copper windings catching IBL, the floating parts above it each with a two-part cast widening with height onto a lit floor pool |
| 02 | engraved white-line intaglio (akengrave) on a machined bar | the anodised range-log bar across the lower half, its bevelled faces cut in swelled white lines lit from the upper left, three date grooves with lit floors and dark lips, a contact shadow on the lit graphite floor |
| 03 | GPU PBR render (akthree), orthographic | the assembled quad hovering under load, twill top plate in the key, motor bells and prop motion discs reflecting the softbox, its soft cast on the lit floor below with the phantom payload between |
| 04 | digital bas-relief height field (per pixel) | the riveted aluminium data plate, rolled edge and four domed rivets lit upper left, five recessed empty fields with brushed dark floors and cavity shade, a two-part cast onto the lit bench |
| 05 | thermal field with fabric relief (per pixel) | the quilted battery vault, quilt cells as a height field lit from the upper left and mapped through the ironbow heat ramp, stitch channels cooler, the battery core warmest, the body side heat rising from the bottom edge |
| 06 | density-ramp hatching on a real DEM section | the Chugach ridge section, hatched body darkening with depth, a lit skin stroke on the key-facing flank, cased surface profile, the radio-shadow wedge in counter-hatch beyond the crest |
| 07 | plan relief height field (per pixel) of steel and snow | the steel hatch cover in plan, a domed brushed plate with weld bead, hinge and latch lit upper left, a snow mound on it with its own albedo and sparkle, a cast onto the lit roof plate |
| 08 | depth-weighted wireframe figures on a vellum sheet | the parts sheet itself, vellum with tooth lying on the lit floor pool with a soft cast at its lower right, row thumbnails drawn as object-normalised wireframes lit from the left |
| 09 | GPU PBR render (akthree) at rest | the assembled quad resting on its arms on a frosted floor, frost crystals in the lit pool catching the key, contact seam under each motor, two-part cast to the lower right into the lit pool |

Masterful depth frame: 01, the exploded quad, parts overlapping in depth along one axis, casts widening with each part's height, floor haze in the bay colour, the near arm and prop larger and the antenna smaller (scale gradient), one key at about 5 to 1.
Tonal arc: a lit softbox cover on 01, the brightest frame the weight study on 03 under the same softbox, a darker timeline on 02 and bench on 04 between them, the warm heat on 05, the darkest frame the night section on 06, the snow-loaded hatch as a lit object on a dark roof on 07, film on 08, a dark quiet close on 09.

## CLAIMS INDEX

| claim | slides |
|---|---|
| C01 | 02 |
| C02 | 02 |
| C03 | NOT USED |
| C04 | 01, 02 |
| C05 | 02 |
| C06 | 02 |
| C07 | 03 |
| C08 | 03 |
| C09 | NOT USED |
| C10 | NOT USED |
| C11 | 01 |
| C12 | 01, 03, 04, 06 |
| C13 | 02 |
| C14 | 05, 08 |
| C15 | 06, 08 |
| C16 | 06, 08 |
| C17 | 06 |
| C18 | 06 |
| C19 | 08 |
| C20 | 08 |
| C21 | 08 |
| C22 | 05, 08 |
| C23 | 08 |
| C24 | 08 |
| C25 | 09 |
| C26 | 08 |
| C27 | 08, 09 |
| C28 | 08 |
| C29 | 07 |
| C30 | 07 |
| C31 | 07 |
| C32 | NOT USED |

---

## SLIDE 01

1. **Beat**: hook. The machine taken apart, three numbered parts, three Alaska problems. Plants: what goes wrong at
   each part?
2. **Copy, final**
   - Kicker (mono 24): `11TH AIRBORNE DIVISION, FROM THE ARMY'S OWN RECORD` (C11)
   - Headline (Unbounded, 2 to 3 lines): `Weight. Cold. Mountains.` / `The Army's Alaska drone, taken apart.` (C11; 9 words)
   - Balloon labels on the art (mono 24): `1 WEIGHT` at the phantom payload point, `2 COLD` at the battery, `3 MOUNTAINS` at the antenna (C11) [design]
   - Phantom tag (mono 20, data-decorative): `PAYLOAD NOT DESCRIBED` [design]
   - Fixtures: wordmark, Polaris, counter `01 / 09`, balloon strip (1 to 3 hollow), `alaskaaihq.com`.
3. **Reader takeaway**: Alaska attacks a drone three ways, and this deck takes each apart.
4. **Layout map**: art occupies columns 1 to 12, rows 1 to 5 (y 120 to 820), the exploded stack centred at x 560
   with its axis tilted 12 degrees, the focal point the battery at about (600, 300). Kicker at y 868, headline from
   y 908 to about 1180 in columns 1 to 11. Eye path battery, then balloons 1 to 3, then headline. Quiet zone the
   floor haze at the upper right corner. Grid violation: the near prop bleeds off the left edge.
4a. **Lower-third treatment**: the lit floor pool under the exploded stack runs down behind the headline, a graded
   cool floor with the widening two-part casts of the floating parts, falling off to the bay night at the bottom edge. The near prop's blurred disc bleeds off the lower left into it.
5. **Depth plan**: bay night background, floor plane with exp2 haze in `#0E1620`, the frame plate (nearest large),
   motors and props, boards, top plate, battery, antenna (farthest up the axis), casts on the floor, then DOM type.
   Cues: occlusion of parts along the axis, scale gradient near prop to antenna, floor haze, two-part casts widening
   with height, one key at about 5 to 1. Camera: perspective fov 30, from (0.42, 0.52, 0.62) metres looking at
   (0, 0.08, 0); the stack spans about 0.25 m of world height. Focal plane the battery.
6. **Continuity**: D1 exploded state; D2 balloons 1 to 3 hollow; D3 key upper left behind.
7. **Technique stack**: akthree (GPU PBR, #87) with `AKT.environment` intensity 1.0 and a custom rig, the quad from
   akdrone `build({spin:false})` then `explode(group, 1.0, {gap: 0.045})`, rotation y 0.6; floor plane colour
   `#18222D` roughness 0.85; floor pool as a CanvasTexture radial gradient under the stack; akpost grade (exposure 0,
   contrast 1.08, grain amount 0.03 size 1, dither) then `AKPOST.holdInk` for gold; phantom payload drawn in 2D
   from `AKT.projectPoint` corners, dashed `#5B6977` 2 px, dash 8 6; balloons and leaders in SVG, gold rings 3 px,
   leaders frost ink 1.5 px declared in `__akLeaders`. noise.js, aktype.js for the fit.
8. **Data-in-art mapping**: three balloons equal the three problems the headline names [design]; no measurement
   is encoded.
9. **Palette**: bay night `#060A10`, floor `#18222D`, pool `#26323F`, carbon `#1A1D22`, steel `#B8C2CC`, frost ink
   `#8CC9E3`, phantom `#5B6977`, type `#EEF3F8`, gold `#FFC72C` only on balloon rings, Polaris and counter slash.
   Worst text pair: headline `#EEF3F8` on floor pool about `#26323F`, about 11 to 1.
10. **Type spec**: kicker mono 500 24 px 0.12em `#A9BCCD`; headline Unbounded 560 fitted 72 to 104 px, leading 1.04,
    width 920; labels mono 500 24 px frost ink.
11. **Anchor**: the quad itself is the literal anchor; annotation is the three numbered balloons with leaders that
    land on the parts' projected centres (`AKT.projectPoint`).
12. **Reference intent**: a service manual's exploded parts plate, photographed.
13. **Risk flags**: parts reading as stickers (casts must widen with height, declared contacts); twill moire (repeat
    tested at 40 and 20); leader endpoints must be projected, never typed; headline over the floor must keep contrast.
14. **Acceptance checklist**
    - [ ] every leader lands on its part (qa leaders PASS)
    - [ ] the payload is a dashed phantom, never a solid box
    - [ ] each floating part has a visible cast on the lit floor
    - [ ] gold appears only on the balloon rings, Polaris and counter slash
    - [ ] the headline reads at 432 px and sits on lit floor, not on a part
    - [ ] the twill reads as weave at 100 percent with no moire

## SLIDE 02

1. **Beat**: payoff. The record: what happened, who, when, with what, and the scope. Plants: they flew the weight first.
2. **Copy, final**
   - Kicker (mono): `THE ARMY'S RECORD, PUBLISHED OCTOBER 27TH` (C01)
   - Headline: `The first kinetic drone strike in the Richardson Training Area.` (C04; 10 words)
   - Body: `Paratroopers of the 2nd Mobile Brigade Combat Team (Airborne), 11th Airborne Division, flew armed first-person view drones in live fire, alongside sniper teams, reconnaissance elements and a gun truck.` (C01, C05, C06; 30 words)
   - Scope line (mono 22): `ARMY RECOGNITION SAYS IT WAS NOT THE ARMY'S FIRST EXPLOSIVE FPV USE` (C13)
   - Rail labels (mono 22): `SEPTEMBER 29TH`, `OCTOBER 19TH`, `OCTOBER 20TH` (C02); rail scale note `ONE GROOVE PER LIVE-FIRE DAY, TRUE CALENDAR SPACING` [design]
3. **Reader takeaway**: an armed drone strike happened in Alaska live fire this fall, and it is scoped.
4. **Layout map**: headline columns 1 to 11 at y 150 to 420, body y 450 to 640, scope line y 676. The bar spans
   x 80 to 1000 at y 860 to 1060, its three grooves at true calendar spacing (September 29th at x 230, October 19th at
   x 830, October 20th at x 860: 30 px per day [design]), labels above and below. Focal point the double groove.
4a. **Lower-third treatment**: the engraved bar itself, a modelled anodised solid with lit bevels and a cast onto the
   lit floor, fills the band from y 860 to 1110, its floor pool continuing to the bottom edge. The bar's soft ambient shadow widens below its tight cast.
5. **Depth plan**: graphite floor, a lit pool under the bar, the bar's cast, the bar (bevels, top face, grooves), type.
   Cues: cast shadow, lit bevel versus lee, the groove floors deeper than the face, pool falloff.
6. **Continuity**: D2 balloons hollow; D3 key upper left, cast lower right.
7. **Technique stack**: akengrave white-line intaglio (`AKENGRAVE.create().surface()` with a bar height field:
   rounded bevel profile, grooves as narrow Gaussian troughs, light from the upper left), drawn offscreen at
   device resolution then composited; floor pool radial in a scaled transform; akpost grade, grain size 1.
8. **Data-in-art mapping**: groove positions are calendar days at 30 px per day (C02) [design]; three grooves equal
   three live-fire days.
9. **Palette**: floor `#101820`, pool `#26323F`, bar ink white lines `#DCE3EA` on `#3A414B`, groove floors `#8CC9E3`
   tint, type `#EEF3F8`, body `#CBD5DF`. No gold on the art.
10. **Type spec**: headline Unbounded 560 fitted 60 to 84 px maxLines 3 width 920; body Manrope 500 33 px width 880;
    scope and rail labels mono 500 22 px `#A9BCCD`.
11. **Anchor**: the dated bar; annotation the three date labels with short ticks landing on the grooves.
12. **Reference intent**: an engraved range log, a machinist's rule for days.
13. **Risk flags**: body copy line count against the scope line (check before render); groove labels at x 830 and 860
    collide (stack October 19th above and October 20th below).
14. **Acceptance checklist**
    - [ ] groove spacing measures 600 px between September 29th and October 19th, 30 px to October 20th
    - [ ] labels do not collide and each tick lands on its groove
    - [ ] the bar reads as a machined solid with a cast
    - [ ] "first" is scoped in the headline and the scope line is legible at thumb size
    - [ ] no gold on the art

## SLIDE 03

1. **Beat**: the first problem, weight. Plants: how much weight? Not published.
2. **Copy, final**
   - Kicker: `PROBLEM 1, WEIGHT` (C07)
   - Headline: `Before the strike, they flew the weight.` (C07)
   - Body: `Operators first flew unarmed explosive payloads to see how the added weight changed the drone's maneuverability. Sgt. 1st Class Devin McNamara, the brigade's sUAS master trainer, helped enable the test flights.` (C07, C08; 31 words)
   - Drafting labels (mono 22): `THRUST` (four arrows) [design], `ADDED WEIGHT` (one arrow) [design], `PAYLOAD MASS NOT PUBLISHED` (C12)
3. **Reader takeaway**: they learned the weight before the strike, and the weight is not on the record.
4. **Layout map**: headline y 150 to 360, body y 390 to 580; the hovering quad centred at (560, 820) spanning x 160 to
   960, phantom payload under it at y 900 to 960, thrust arrows rising from the four motors, the weight arrow falling
   from the payload to y 1080; the cast ellipse at y 1170. Quiet zone upper right.
4a. **Lower-third treatment**: the lit floor pool with the hovering quad's soft cast and the weight arrow's head, a
   graded floor falling off at the bottom edge. The phantom payload's dashed box hangs just above the cast, so the force diagram reaches the band.
5. **Depth plan**: floor with pool, the cast, the quad (orthographic), drafting overlay, type. Cues: cast below a
   hovering object, lit top face versus lee undersides, motion discs reflecting the softbox, floor falloff.
   Camera: OrthographicCamera, dimetric elevation 18 degrees, azimuth 35 degrees.
6. **Continuity**: D1 assembled hovering; D2 balloon 1 filled gold; D3 key upper left.
7. **Technique stack**: akthree orthographic render, akdrone `build({spin:true})`, the floor pool texture, akpost
   grade then `holdInk`; SVG drafting overlay (filled 3 to 1 arrowheads, frost ink 2 px, dimension call with blank
   value); leaders declared.
8. **Data-in-art mapping**: four thrust arrows equal four motors [design]; the weight arrow is unscaled and its
   label says the mass is not published (C12).
9. **Palette**: floor `#18222D`, pool `#26323F`, carbon, steel, frost ink arrows `#8CC9E3`, phantom `#5B6977`, gold only
   on the strip, Polaris and counter.
10. **Type spec**: as 02.
11. **Anchor**: the assembled quad; annotation the force arrows and the blank dimension call.
12. **Reference intent**: a free-body diagram drawn over a product render.
13. **Risk flags**: arrow labels over the props; orthographic shadow camera framing.
14. **Acceptance checklist**
    - [ ] the quad reads as hovering with a cast directly below
    - [ ] the payload is phantom and the mass label says not published
    - [ ] four thrust arrows start at the four motors
    - [ ] balloon 1 is filled gold in the strip

## SLIDE 04

1. **Beat**: breather and analytical turn. What the Army left blank. Plants: what did it publish? What soldiers built.
2. **Copy, final**
   - Kicker: `WHAT THE RECORD LEAVES OUT` (C12)
   - Headline: `What the Army left blank.` (C12)
   - Plate field names (mono 24, DOM): `MODEL`, `PAYLOAD MASS`, `ENDURANCE`, `ENGAGEMENT RANGE`, `MEASURED ACCURACY` (C12)
   - Line (mono 22): `NOT IDENTIFIED BY THE ARMY, ARMY RECOGNITION REPORTED ON OCTOBER 28TH` (C12)
3. **Reader takeaway**: the Army published a first, not a specification.
4. **Layout map**: headline y 150 to 300; the plate at x 110 to 970, y 400 to 1120, five field rows at y 470, 600,
   730, 860, 990; line y 1180. Focal point the empty fields.
4a. **Lower-third treatment**: BREATHER, the deck rests here between the record and the soldiers' fixes; the plate's
   lower two field rows, its rolled edge and its two-part cast on the lit bench still carry modelled tone.
5. **Depth plan**: bench, pool, cast, plate (rolled edge, rivets, recess floors), DOM field names. Cues: recess
   depth with cavity shade, rivet domes, cast, edge highlight.
6. **Continuity**: D2 all balloons dashed frost rings (nothing answered on this frame).
7. **Technique stack**: digital bas-relief (#100) per device pixel: rounded-rect plate height with a rolled edge, four
   domed rivets, five recessed fields, brushed anisotropic albedo noise along x, Lambert plus Blinn from the key
   (screen az 300, el 34), cavity AO from a blurred height difference; noise.js; floor pool; akpost grade.
8. **Data-in-art mapping**: five empty fields equal the five items Army Recognition lists (C12).
9. **Palette**: bench `#101820`, pool `#26323F`, plate aluminium `#9AA6B2` to `#C9D2DB`, recess floors `#1A2028`,
   field names sit in the recesses at `#B9C7D4` on `#1A2028` (about 9 to 1).
10. **Type spec**: headline Unbounded 560 fitted 60 to 84 px; field names mono 500 24 px; line mono 22 px.
11. **Anchor**: the data plate; annotation none beyond its own fields.
12. **Reference intent**: an equipment nameplate with nothing stamped.
13. **Risk flags**: recess floors reading as domes (keep them darker than the face); names must sit inside recesses.
14. **Acceptance checklist**
    - [ ] five recessed fields, all empty, names legible
    - [ ] rivets read as domes lit upper left
    - [ ] the plate casts onto the bench
    - [ ] `data-breather` present

## SLIDE 05

1. **Beat**: the second problem, cold. The warmest frame. Plants: you can't carry a mountain.
2. **Copy, final**
   - Kicker: `PROBLEM 2, COLD` (C22)
   - Headline: `A private hand-sewed a battery vault.` (C22)
   - Body: `Pfc. Michael Pereira's passive prototype keeps drone batteries viable in sub-zero temperatures using only body heat and radiant barriers. It was an entry at Angel Ascent, the 11th Airborne's innovation competition, on October 28th.` (C22, C14; 35 words)
   - Legend (mono 20): `RELATIVE HEAT, NO TEMPERATURE PUBLISHED` (C22) and `PROTOTYPE AS DESCRIBED, NOT PHOTOGRAPHED` [design]
   - Labels: `BODY SIDE` [design], `BATTERY` [design]
3. **Reader takeaway**: one soldier answered Alaska's cold with a needle and body heat.
4. **Layout map**: headline y 150 to 360, body y 390 to 590; the pouch in thermal from x 220 to 860, y 640 to 1230,
   heat rising from the bottom edge; legend at y 1240 left. Focal point the warm core at (540, 960).
4a. **Lower-third treatment**: the pouch's warmest half and the body-side heat field rising from the bottom edge
   carry modelled fabric relief mapped through the heat ramp. The hem's lit fold and the isolines bending around the core run down to the bottom edge.
5. **Depth plan**: cold field, body heat glow from below, pouch height field (quilt cells, hem, seams), isolines,
   type. Cues: relief shading on the quilt, heat diffusion halo, stitch grooves, hem shadow.
6. **Continuity**: D2 balloons 1 and 2 filled; D4 the heat peak.
7. **Technique stack**: per-device-pixel thermal field: emission from a pouch SDF, a battery core SDF, a body-side
   exponential from the bottom, quilt-cell dome height field (diamond quilting at 9.5 px cells per design 48 px)
   shaded Lambert from the key and multiplied into the emission, stitch channels cooler; mapped through the
   seven-stop ironbow ramp; d3 contours in frost ink at hairline with no values; noise.js; d3.
8. **Data-in-art mapping**: none numeric; the legend says relative and unscaled.
9. **Palette**: ironbow ramp only here; frost ink isolines; type `#EEF3F8` over the cold violet field
   (`#2A0B4A`, about 14 to 1).
10. **Type spec**: as 02; legend mono 20 px.
11. **Anchor**: the pouch; annotation two labels with leaders to the battery core and the body side.
12. **Reference intent**: a field infrared photograph of kit.
13. **Risk flags**: the pouch reading as a flat rectangle (quilt relief and a puffed silhouette); heat ramp banding
    (dither before the 8-bit write).
14. **Acceptance checklist**
    - [ ] the pouch reads as a puffed, quilted object, not a rectangle
    - [ ] the core is warmest and the stitches cooler
    - [ ] the legend states no temperature was published
    - [ ] ironbow appears on this frame only

## SLIDE 06

1. **Beat**: the third problem, mountains; the winner. Plants: not every fix flies.
2. **Copy, final**
   - Kicker: `PROBLEM 3, MOUNTAINS` (C17)
   - Headline: `First place went to a relay over the ridge.` (C15, C16)
   - Body: `Spc. Leighton Keilen won Angel Ascent, and a Meritorious Service Medal, with a Skydio drone relay and modular payload delivery system. The Army says it significantly extends tactical drone range in Alaska's mountains.` (C15, C16, C17, C18; 36 words)
   - Art labels (mono 22): `OPERATOR` [design], `RELAY` [design], `NO LINE OF SIGHT` [design], `DISTANCE NOT PUBLISHED` (C12)
   - Note (mono 20): `A CHUGACH PROFILE, DRAWN TO SHOW LINE OF SIGHT. NOT THE SITE.` [design]; `VERTICAL EXAGGERATION 2X` [design]
3. **Reader takeaway**: a ridge blocks the link; a relay over it was the winning idea.
4. **Layout map**: headline y 150 to 360, body y 390 to 600; the section spans x 0 to 1080, profile from y 1240 (base)
   up to the crest at about y 820, operator mark at x 120 on the flats, crest near x 430, valley beyond near x 640, far
   ridge rising to the right edge; relay above the crest at about (430, 700).
4a. **Lower-third treatment**: the hatched section body of the ridge fills the band, darkening with depth, its lit
   skin on the key-facing flank. The far ridge rises off the right edge and the counter-hatched radio-shadow wedge sits in the valley.
5. **Depth plan**: night, section body (density-ramp hatch), skin stroke, radio-shadow wedge (counter-hatch), sight
   lines, relay, labels, type. Cues: hatch density with depth, skin lighting, overlap of near ridge over far ridge.
6. **Continuity**: D2 balloons 1 to 3 filled.
7. **Technique stack**: real profile from `ak-cookinlet-dem` sampled Catmull-Rom along (61.25 N, 149.72 W) to
   (61.30 N, 149.10 W), smoothed twice, vertical exaggeration 2 [design]; density-ramp hatching (#64) at -41 degrees,
   spacing 4 to 12 px by depth below the skin, crosshatch below 60 percent depth (#65); cased profile line 5 px;
   sightlines frost ink with a blocked cap; relay as a small gold glyph with two link segments; noise.js.
8. **Data-in-art mapping**: the profile is real terrain at vertical exaggeration 2 [design]; positions are illustrative.
9. **Palette**: night `#060A10`, hatch ink `#5B6977` to `#8CC9E3`, skin `#DCE3EA`, relay gold `#FFC72C`.
10. **Type spec**: as 02.
11. **Anchor**: the ridge section; annotation operator, relay and blocked-link labels.
12. **Reference intent**: a geologist's section with a radio engineer's link drawn on it.
13. **Risk flags**: hatch moire at the 2x backing (line weight 1.2 device px minimum); label collisions on the slope.
14. **Acceptance checklist**
    - [ ] the direct link stops at the crest with a blocked cap
    - [ ] the relay sits above the crest and both segments clear terrain
    - [ ] the not-the-site note is legible
    - [ ] gold only on the relay, strip, Polaris and counter

## SLIDE 07

1. **Beat**: a fix that does not fly; the record's only price. Plants: the list is longer.
2. **Copy, final**
   - Kicker: `PROBLEM 4, SNOW` (C29)
   - Headline: `Not every fix flies. This one costs about $300.` (C30)
   - Quote: `"We put together a metal version that can sustain the weight of snow, and can also be popped open easily."` (C31)
   - Attribution (mono 22): `CAPT. DANIEL WOODARD, 725TH LIGHT SUPPORT BATTALION` (C29, C31)
   - Line: `It replaces cloth gunner hatch covers that let snow leak into truck cabs.` (C29)
   - Art label: `HATCH SHAPE ILLUSTRATIVE` [design]
3. **Reader takeaway**: about $300 of steel keeps snow out of an Army truck cab.
4. **Layout map**: headline y 150 to 340, quote y 370 to 560, attribution y 580, line y 630; the hatch in plan centred at
   (600, 980), plate diameter 560, snow mound off-centre on its upper half; roof plate running off the bottom and right.
4a. **Lower-third treatment**: the brushed steel hatch's lower half, its weld bead and latch, and the cast onto the
   lit roof plate, with the roof running off the frame. The roof's own brushed texture and the pool's falloff carry tone to the bottom edge.
5. **Depth plan**: roof plate with a lit pool, cast, hatch plate (dome, bead, hinge, latch), snow mound (height,
   albedo, sparkle), type. Cues: cast, dome shading, snow over steel occlusion, sparkle.
6. **Continuity**: D2 balloon 4 added, filled; D4 brightest frame.
7. **Technique stack**: plan relief height field per device pixel (akbench-style multi-material in a slide-local
   shader): steel dome height with domain-warped radial brushing, weld bead ring, hinge cylinder, latch; snow mound
   from fbm with a soft edge, high albedo, sparkle from thresholded noise; Lambert plus Blinn from the key; cast by
   offset blurred mask; noise.js; akpost grade, `holdInk` for the gold `$300` stencil drawn in DOM.
8. **Data-in-art mapping**: the $300 is printed once (C30).
9. **Palette**: roof `#2A333D`, steel `#9AA6B2` to `#DCE3EA`, snow `#F4F8FF`, quote type `#EEF3F8` on the dark top band.
10. **Type spec**: headline as 02; quote Manrope 500 33 px; attribution mono 22 px.
11. **Anchor**: the hatch; annotation the illustrative tag.
12. **Reference intent**: a product shot of a shop-made part, straight down.
13. **Risk flags**: snow reading as paint (needs height and sparkle); the dome reading as a flat disc.
14. **Acceptance checklist**
    - [ ] the hatch reads as domed steel with a weld bead and hinge
    - [ ] the snow mound has height and sparkle
    - [ ] the quote is verbatim with straight quotes
    - [ ] $300 appears once

## SLIDE 08

1. **Beat**: the keeper. Angel Ascent as a parts list. Plants: which problem next?
2. **Copy, final**
   - Kicker: `ANGEL ASCENT, OCTOBER 28TH` (C14)
   - Headline: `The entries the Army named.` (C15, C22)
   - Rows (Manrope 28 and mono 22):
     - `Skydio drone relay and payload delivery system, Spc. Leighton Keilen, first place` (C15, C16)
     - `Hand-sewn passive thermal battery vault, Pfc. Michael Pereira` (C22)
     - `Unit-fabricated ring mount hatch for FMTVs, for convoy gunners` (C24)
     - `TroopToTask.org, Staff Sgt. Robert Baddeley` (C26)
     - `3D-printed explosively formed penetrators for FPV drones, named here, not drawn` (C23)
   - Title block (mono 22): `10 MINUTES TO BRIEF, FIVE OF QUESTIONS` (C20); `FIVE CRITERIA` (C21); `SECOND ITERATION, TWICE A YEAR` (C27, C28); `EVERY OTHER COMPETITOR, AN ARMY COMMENDATION MEDAL. EVERYONE, A FOUR-DAY PASS.` (C19)
3. **Reader takeaway**: the list of what soldiers built, and how it was judged.
4. **Layout map**: headline y 150 to 300; the sheet x 70 to 1010, y 340 to 1230 with five rows at 120 px pitch from
   y 380, each with a 110 px thumbnail cell at left; title block y 1000 to 1210 with the 15-tick strip.
4a. **Lower-third treatment**: the sheet's title block and its last row lie on the lit floor pool with the sheet's
   soft cast at the lower right, vellum tooth modelled. The 15-tick briefing strip and the medal line sit in the title block's cells.
5. **Depth plan**: floor, pool, sheet cast, vellum sheet, thumbnails, type. Cues: cast, sheet edge lift, tooth.
6. **Continuity**: D2 all four filled.
7. **Technique stack**: object-normalised depth-weighted wireframes (#123) of four simple solids (a relay quad, a
   pouch, a ring hatch, a page) drawn in Canvas 2D with line width and alpha by depth; the penetrator cell left empty
   with a dashed border and the words in the row; vellum tooth from noise.js; 15-tick strip in SVG (10 solid, 5 hollow).
8. **Data-in-art mapping**: 15 ticks equal 15 minutes, 10 solid, 5 hollow (C20); five rows are the five entries named
   here, not the full field (C19 notes) [design].
9. **Palette**: sheet a dark drafting film `#1E2A36` with frost ink
   `#8CC9E3` lines and type `#EEF3F8`; gold only on the first-place row's rule.
10. **Type spec**: rows Manrope 500 28 px; title block mono 22 px.
11. **Anchor**: the sheet; annotation the title block.
12. **Reference intent**: a parts list sheet from a maintenance manual.
13. **Risk flags**: word count (about 90 words of labels, keep rows one line each); tiny text floor 24 px except
    title block at 22 marked as a label with good contrast.
14. **Acceptance checklist**
    - [ ] five rows, one line each, no collisions
    - [ ] the penetrator cell is empty
    - [ ] 15 ticks, 10 solid and 5 hollow
    - [ ] gold only on the first-place rule, strip, Polaris and counter

## SLIDE 09

1. **Beat**: close, single ask. Put back together.
2. **Copy, final**
   - Quote (Manrope 33): `"Soldiers across the 11th Airborne Division continue to demonstrate that many of the best ideas come from the bottom up."` (C25)
   - Attribution (mono 22): `COL. MATTHEW ADAMCZYK, 11TH AIRBORNE DIVISION` (C25)
   - Ask (Unbounded): `What Alaska problem should soldiers bring to the next Angel Ascent?` (C27)
3. **Reader takeaway**: the next fix could be one you name.
4. **Layout map**: ask y 150 to 420, quote y 460 to 640, attribution y 660; the resting quad centred at (560, 1000),
   spanning x 170 to 950, on the frosted floor.
4a. **Lower-third treatment**: the resting quad, its contact seams and two-part cast into the lit floor pool, floor
   frost catching the key, falling off to night at the bottom edge. The floor's frost texture shows in the pool and fades out of it.
5. **Depth plan**: bay night, floor with frost, pool, cast, quad, type. Camera perspective fov 32 from (0.30, 0.16,
   0.42) looking at (0, 0.02, 0). Cues: contact seam, cast, floor falloff, rim on the arms.
6. **Continuity**: D1 assembled at rest; D2 all filled.
7. **Technique stack**: akthree with akdrone `build({spin:false})` resting on the floor, rime via a white noise
   roughness and colour blend on the twill material, floor pool texture, akpost grade then `holdInk`.
8. **Data-in-art mapping**: none.
9. **Palette**: as 01, darker overall.
10. **Type spec**: ask Unbounded 560 fitted 60 to 84 px maxLines 3; quote Manrope 500 33 px.
11. **Anchor**: the quad.
12. **Reference intent**: the last plate of a manual, the assembled unit.
13. **Risk flags**: the dark frame must keep the quad readable (rim and pool).
14. **Acceptance checklist**
    - [ ] one ask only
    - [ ] the quad sits with contact seams under its motors and a cast
    - [ ] the quote is verbatim

## BUILD RECONCILIATION

| slide | the dossier said | the build did |
|---|---|---|
| 01 | camera (0.42, 0.52, 0.62), explode gap 0.045, headline 2 to 3 lines | camera (0.56, 0.66, 0.80) looking at (0.02, 0.035, 0), gap 0.036 m, FogExp2 0.32; headline four authored lines at 60 to 84 px; tag `PAYLOAD MASS NOT PUBLISHED`; added `GENERIC QUAD, STUDIO DRAWING` at y 812 |
| 02 | bar y 860 to 1060, October 20th tick below | bar y 950 to 1100; a short tick above the bar for every date so all three marks sit in the axis band y 920 to 946; scope line `ARMY RECOGNITION SAYS NOT TO READ IT AS THE ARMY'S FIRST EXPLOSIVE FPV USE`; pool brightened (cast dL 15.2) |
| 03 | orthographic dimetric, arrows unscaled | frustum half-height 0.3125 m, view raised 0.062 m; thrust arrows start at each motor's own world position and run 70 to 120 px up, floor at y -0.105 m; weight labels set right of the weight arrow; motion discs lightened, top plate twill at repeat 4.5 by 6 with clearcoat, phantom hung at y -0.05 m below the plate, a larger weight arrowhead |
| 04 | closing line "none of the five" | `NOT IDENTIFIED BY THE ARMY, ARMY RECOGNITION REPORTED ON OCTOBER 28TH` (a subset count with no enumerated claim can't be declared); bench pool under the foot (cast dL 16.3) |
| 05 | body "keeps", note "prototype as described" | `is designed to keep` (C22's wording), `STUDIO DRAWING FROM THE ARMY'S DESCRIPTION`; seven-swatch DOM heat legend added; pouch centre (540, 905), 300 by 250 |
| 06 | vertical exaggeration 2, Fairbanks coordinate | exaggeration 6 (at 2 the relief was under 90 px), base y 1150, two hatch lays over a graded body, `DRONE` label added, no coordinate on this frame; body trimmed of 'It published no distance.' (the dimension call says it); the wedge's fill and hatch fade in below the body copy (y 640 to 760) and its lay runs against the rock's; the direct link stops at the true grazing point (steepest rise seen from the operator) and the shadow wedge starts on that ray, labelled `NO LINE OF SIGHT` / `RADIO SHADOW, DRAWN` inside the hatch |
| 07 | headline "This one costs about $300" | `Not every fix flies. About $300 in materials.` (C30); snow mound smoothed and its albedo blended into the steel; plate edge continuous (no cliff ring); roof pool brightened (cast dL 12.1); dome raised to 92 px with a weld bead 18 px inside the rim and turned (concentric) brushing; plate centre x 620; illustrative tag in the dark band above the plate at y 722; attribution moved to sit 12 px under the quote so it groups with the quote and not the body line |
| 08 | rows Manrope 28 and mono 22 | Manrope 26 title line and mono 24 name line; tick strip at x 754, pitch 15; film tooth drawn as lit fibres, a key-side bevel and lee edge, a two-part cast and a dithered pool; thumbnail column at x 172 (row 1 at 0.8 scale, 6 px left); a key gradient and the pool's light on the film face; fibres at random angles lit on the key half |
| 09 | camera (0.30, 0.16, 0.42), rime on the twill and steel | camera (0.40, 0.22, 0.60) looking at (0, 0.098, 0); ask in four authored lines; no rime on the model (at this camera distance a frost film read as dust on the carbon), the cold lives in the frosted floor crystals inside the pool instead; pack lifted to slate `#3A4656`, blades untwisted and matte, the floor falls to night over the bottom 220 px |
| strip | balloon 4 appears on 07 | balloon 4 waits from 01 as a dashed phantom ring (#6E7E8E) and fills gold on 07, so the strip never reads finished at 06 and no mark moves (flow critic, round 5) |
| all | labels 20 to 22 px, fixtures at y 62 | labels 24 px, fixtures at y 80 inside the safe zone, balloon strip at y 122 |

Tonal arc as measured: the darkest frame is 06 (the section at night, L* 10.6), not 09; the close stays dark but quieter. The lit peak moved from 07 to the two softbox frames: 03 measures L* 37.1 (exposure lifted 0.2 so it leads) and 01 L* 33.7, against 07 at L* 18.6, because the hatch reads as a lit object on a dark roof rather than a lit field. The softbox pair bracketing the darker 02 is the deck's camera-move continuity (01, 03, 09 on one quad), so the arc was re-declared to match rather than dimming the cover. The CRAFT PLAN line is updated to say so.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-11-04. Do not hand-write these lines.
[WARN] render         9/9 slides OK, 0 page errors, 4 overflow warnings
[WARN] qa.py          WARN, 0 fails, 28 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 11 table row(s), 4203 chars
[PASS] caption_check  PASS, 883 chars, hook 121, 3 hashtags
[PASS] word_ban       word_ban: 0 banned word(s) in out/2026-11-04 and the docket
[PASS] copy_sync      copy_sync_check: PASS -- 74 authored slide strings all present in the render; alaskaaihq.com on every slide; no banned slide string; no curl
[PASS] aggregate      aggregate_check: PASS -- 4 aggregate assertion(s) detected, 4 declared -> out/2026-11-04/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 32 claims indexed, 0 declared counts checked, 0 body quote(s) checked, 0 11a region set(s) checked, 0 drift(s)
[PASS] tonal_arc      brightest 03, darkest 06, span 29.1 L*, as declared
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.123 (fail at 0.60), max pair 0.498, drawn share 68% (77 drawn vs 36 blocky
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] ledger_guard   LEDGER GUARD: PASS, 7 cron-written file(s) untouched
[PASS] docket_dates   docket dates clean at 2026-11-04: 434 assertions over 6 fixtures and 41 ledger items
[PASS] gas_watch      92 day(s) on record, 78 verified, no gaps, latest 2026-11-04, EIA through 202608 over 132 months, model misses by 6.82%
[PASS] gas_watch_live PASS, checked 2026-11-05T06:14:30Z
[PASS] cron_health    7 scheduled workflows audited at 2026-11-05T06:07:56.799239Z
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-11-04 (298 generated files)
[PASS] assemble       9 slides, pdf vector 6.58 MB, 9 thumbs, sources verified
[PASS] score          8.225 / 10 vs threshold 7.7, scorer says passes=True
[PASS] ship_gate      scored 8.22 against a threshold of 7.70; craft floor capped, artwork craft 7.0, but the run is at the 5-round cap
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```

