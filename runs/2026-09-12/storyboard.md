# STORYBOARD — Carousel No.57 — 2026-09-12
## THE OCCUPIED STATION, DESCENDED

# DECK HEADER

## THESIS

The permit knows the machine's position and does not know the animal's number.

Nine frames are one dive through a single column of Arctic water. NMFS issued the
Office of Naval Research a Year 9 authorization on September 10th for an acoustic
navigation grid, and the same document's stock table gives the Beaufort beluga a
1992 figure and the Arctic ringed seal, the one species here listed as threatened,
no figure at all. The deck does not argue the grid should not exist.

PDF document title, 58 characters: `The Permit Knows Where the Machine Is`

## ARC

| # | beat | window, metres below the ice | temperature |
|---|---|---|---|
| 01 | HOOK. The paired readout, one resolved and one blank | -6 to 30 | cool |
| 02 | PAYS OFF IMMEDIATELY. What the sound is for | 0 to 120 | |
| 03 | What goes in the water, and on what cycle | 20 to 400 | |
| 04 | BREATHER, declared. The place itself | 380 to 1,000 | |
| 05 | CONCEDE PRECISELY. Every number about an animal is a distance | 500 to 2,000 | |
| 06 | The unattended year | 800 to 2,600 | cold |
| 07 | THE TURN, and the keeper. The stock gauge | 1,000 to 3,000 | coldest |
| 08 | What the record actually is | 1,200 to 3,400 | |
| 09 | CLOSE. One ask | 1,200 to 3,400 | |

Breather 04. Keepable data slides 06 and 07. The temperature turns at 07.

Slide 05 CONCEDES precisely, and that is deliberate. The permit does publish exact
figures about animals and all of them are distances. Drawing them carefully is
what makes 07's blank an argument rather than a complaint.

## SLIDE COUNT RATIONALE

Nine, inside the 8 to 10 default. Eight descending frames give the shared depth
mapping enough travel to read as a descent rather than as arbitrary crops, and the
ninth holding the eighth's window is the camera's full stop.

## CONTINUITY SYSTEM, four devices

**D1, THE DESCENDING WINDOW.** `AKICE.setWindow(d0, d1, y0, y1)` on one shared
mapping. `d0` never decreases and `d1` always increases, so the camera cannot
double back and nothing needs aligning by hand. This is 94c's fix by construction.

**D2, THE GOLD FIX, full state table.**

| slide | state |
|---|---|
| 01 | one gold fix point where two range arcs close, and NO gold on the dial |
| 02 | rebuilt out of three intersecting range arcs into one cross at 62 m |
| 03 | eight source ticks, one per source in use, no intersection drawn |
| 04 | one faint arc crossing the upper third. The sound still arriving |
| 05 | the common centre of four mitigation circles, which are cool ink |
| 06 | full strength over the pulse field, and the 132 attended ticks |
| 07 | two gold needle caps, and the third dial's socket is empty. WITHHELD |
| 08 | the only bright mark above a bed that is drawn and not measured |
| 09 | resolves into the Polaris at the close |

**D3, THE RISER CHAIN**, declared once, every exit IS the next entry. 01 exits
y 980. 02 enters 980, exits 742. 03 enters 742, exits 1,106. 04 enters 1,106,
exits 610. 05 enters 610, exits 928. 06 enters 928, exits 1,192. 07 enters 1,192,
exits 520. 08 enters 520, exits 860. 09 enters 860 and dead-ends on the anchor
shackle. Exactly one frame terminates and it is the ninth.

**D4, THE PALETTE ARC.** Each frame's water top hex is the previous frame's bed
hex, so the value ladder is one continuous ramp across nine frames, checkable with
one pixel sample per frame. `#1A4C57` `#123E49` `#0C2E38` `#08202A` `#061821`
`#04111A` `#03090C` `#02080D` `#02060F`.

## VARIETY LEDGER CHECK

Last four hero structures were No.53's curved transect as a nine frame camera
move, No.54's stamped field and printed page, No.55's struck register on laid
paper, No.56's sheet and its margin. This deck's required divergence, stated
explicitly: **three of those four are printed surfaces and this deck contains no
printed surface at all.** It traverses no geography and never pans, so it is not
the transect. It has no neatline, no margin and no annotation gutter, which is the
deliberate inversion of No.56: that deck made type safe by fencing it out of the
art and then spent its detail budget on the fence. Here type is IN the water and
measurement pays for it.

Atmospheres of the last three were sodium lamp and galvanized steel, a printer's
bench under a north window, and overcast Southcentral daylight. This is first dark
under new ice, and its key is DOWNWELLING, which is new for this house after a run
of low raking keys.

Continuity devices of the last two were two struck squares in a footer gutter and
an edge-on volume plus a header index diagram. None of the four here is either.

Hook archetypes of the last three were the sentence that isn't there, timeline
collapse, and the object you can see and can't read. This is **NEW: THE PAIRED
READOUT**, two measurements taken in one grammar by one document, where one
resolves to a single point and the other is a fully legible dial with a printed
scale and no needle. It is not the sentence that isn't there, because every word
on the cover is present and the missing thing is a NEEDLE. It is not timeline
collapse, because the cover carries no time axis. It is not the object you can
see and can't read, because the blank dial is completely readable and being
readable is exactly what makes it land.

Palette families of the last three were sodium-zinc, laid-paper-and-burin, and
inlet-silt-under-overcast. This is new ice over black water.

Type pairings of the last two were Instrument Serif with Bricolage Grotesque, and
Archivo with Manrope. This is Fraunces over Space Grotesk over JetBrains Mono.

LINEAGE NAMED HONESTLY. `akcolumn.js` did a shared altitude mapping for AIR over
the Kenai on No.42, fifteen decks back and outside every window. This is the same
structural idea pointed at water, with a different medium, a different light and a
different measured quantity.

## VARIANCE DIALS

design_variance 5, visual_density 5, type_temperature 3. Density 5 is the budget
for the ray field and the mote populations, and it is paid inside the picture
rather than in annotation furniture.

## PALETTE AND TYPE SYSTEM

Light, declared once and never varied: **az 12 clockwise from up, el 62,
downwelling, key to fill 5.0 to 1.** The lee of every form falls just to its lower
left and every cast is short.

| hex | role |
|---|---|
| `#D8ECEE` | ice crust, the one genuinely lit surface, frames 01 to 03 |
| `#9FC2C8` | ice body |
| `#5E838C` | the keel, the ice underside |
| `#E8F6F7` | the arris, the deck's hardest edge |
| ladder above | water, one hex per window boundary |
| `#F4F8FF` | display type |
| `#D8ECEE` | body type |
| `#BAD6DA` | rail ink, mono labels, units, mitigation circles |
| `#7D8F94` | THE UNDETERMINED INK |
| `#6EA5FF` | the two beluga stocks, the species that have numbers |
| `#3CE6B4` | one use only, the glider's lit upper surface on 04 |
| `#16333B` | header fixtures on frames 01 to 03, dark ink on lit ice |
| `#46545F` | the alaskaaihq.com watermark, every frame |
| `#FFC72C` | THE ONE GOLD |

**THE COLOUR LAW. GOLD IS WHAT THE RECORD KNOWS. THE UNDETERMINED INK IS WHAT IT
DOES NOT.** `#FFC72C` appears only on the fix cross, the range arcs that make it,
the 132 attended ticks and the Polaris. `#7D8F94` appears only on the unattended
ticks, the phantom rail below 2,000 m, the ghost marks of a coefficient of
variation, and the word UND. Nothing else in the deck is warm and nothing else is
that grey. Auditable in one pass.

Display **Fraunces**, cover 118 px wght 640 opsz 96 SOFT 24 WONK 1, headlines 72
px wght 600 SOFT 12 WONK 0. Support **Space Grotesk** 500 at 34 px, leading 1.38,
max width 560 px. Instrument **JetBrains Mono** 500, labels 25 px caps tracked
plus 8 percent, rail numerals 25 px tabular lining, counter 22 px, watermark 18
px. Body type never below 32 px. The watermark is the deck's only sub-floor
element and the brand spec licenses it as a fixture.

**THE TOP BAND IS LIT ICE, SO HEADER TYPE IS DARK** on frames 01 to 03, measured
on the prototype where a light wordmark read 1.7 and brightening it read 1.0.

## THE RESERVE, settled by render and not by argument

Every field generator takes an `atten` function from `AKICE.basins`, built from
`AKFIT.reserveBoxes` measured PER LINE BOX. The field puts fewer marks where the
words go and the water's value ladder runs unbroken behind them.
`AKENGRAVE.punchReserves` is NOT used in this deck. Both treatments specified it
and the prototype shipped three hard-edged black rectangles.

## CLAIMS INDEX

RECONCILED TO THE BUILD after Phase 7, which is the direction the drift gate
names: the deck on disk is the artifact and this table is the plan, so where the
two disagreed the table moved. Six rows changed and three claims left the deck
entirely, every one of them because the caption room's final copy is shorter and
more careful than the dossiers' drafts.

| claim | slides |
|---|---|
| C02 | 06, 08 |
| C05 | 01 |
| C06 | 08 |
| C11 | 04 |
| C12 | 04 |
| C13 | 04 |
| C14 | 03 |
| C15 | 03 |
| C16 | 03, 05, 06 |
| C17 | 03, 06 |
| C18 | 03 |
| C19 | 03 |
| C23 | 08 |
| C25 | 01, 02 |
| C26 | 04 |
| C27 | 02, 04 |
| C30 | 03 |
| C31 | 06 |
| C32 | 06 |
| C34 | 06 |
| C37 | 05 |
| C39 | 07 |
| C40 | 08 |
| C41 | 07 |
| C42 | 07 |
| C43 | 01, 07 |
| C44 | 08 |
| C45 | 05, 06 |
| C46 | 05 |
| C47 | 08 |
| C50 | 05 |
| C53 | 09 |

WHAT MOVED, and why each one moved:

- **C01 and C31 leave slide 01.** The planned cover was "The ship leaves after 22
  days. The sound stays 12 months." The built cover is "The permit can find the
  robot. It can't count the seal.", which is the thesis rather than the duration
  asymmetry, so the issuance date and the 22 days are no longer printed there.
  C31 is on slide 06, which is where the 22 days now do their work. C01 is not
  printed on any frame and is carried by the caption's own first sentence and by
  the first comment, where a dated citation is a citation.
- **C16 gains slides 03 and 05.** The copy room moved the year onto slide 03's
  headline, "all year", and slide 05's lower band names the year the source then
  transmits. It leaves slide 01 with the cover.
- **C23 moves from slide 05 to slide 08.** The 2,000 m figure is printed in the
  honesty line at the bottom of the dive, not beside the mitigation radii.
- **C45 gains slide 06.** Slide 06's body carries the observer clause, which is
  the mitigation half of that claim.
- **C02 leaves slide 09.** The close prints no date.
- **C04 leaves the deck.** It was carried only by a provenance mark on slide 09
  and the owner's 2026-09-11 change forbids a source note on that frame, so the
  frame does not print it and neither does this table.
- **C22 leaves slide 04.** The Argo floats are not named in the built copy, which
  keeps that frame to the area, the distance and the three jurisdictions.

NOT USED, and deliberately: C01, C03, C04, C07, C08, C09, C10, C20, C21, C22,
C28, C29, C33, C35, C36, C38, C48, C49, C51, C52. C20, C21, C28 and C29 are the
REMUS and the very low frequency sources, both of which are permissions rather
than plans, and the safest handling of a permission that is not a plan is to draw
neither.

## D5, THE PROVENANCE MARK, a fixture that carries the deck's subject

SLIDE 09 CARRIES NONE, and that is the fixture\'s one exception. The owner\'s
change of 2026-09-11 forbids a source note on the close, and a device table may
not quietly overrule an owner change. The table below is read with that
exception; the flow room was right that a nine frame fixture missing its last
frame needs saying out loud rather than leaving two documents to disagree.

One mono line, 20 px, `#7D8F94`, at x 80 baseline y 1244, the same position on
every frame, above the watermark. It says what the notice publishes, or that it
does not. This replaces the coordinates footer, because a real citation address
beats an invented latitude and because this deck's subject is what the record
contains.

| slide | the mark |
|---|---|
| 01 | `TWO READINGS, ONE DOCUMENT` |
| 02 | `SATELLITE FIXES DO NOT REACH UNDER ICE. THIS PAGE'S GLOSS, NOT THE NOTICE'S` |
| 03 | `PROPORTIONS ARE THE DRAWING'S. PULSE AND CEILING ARE THE NOTICE'S` |
| 04 | `AREA AND STANDOFF ARE THE NOTICE'S` |
| 05 | `ALL FOUR RADII ARE IN THE NOTICE` |
| 06 | `THE CYCLE AND THE TERM ARE THE NOTICE'S. THE TALLY IS THE DRAWING'S` |
| 07 | `RING RADIUS IS A COEFFICIENT OF VARIATION, NOT A DISTANCE` |
| 08 | `SEABED DEPTH DOES NOT APPEAR IN THE NOTICE` |
| 09 | `91 FR 57547, ISSUED SEPTEMBER 10TH` |

## D6, THE PHANTOM DASH MEANS THE NOTICE DOES NOT SAY

Dash kit, library 67, `30 5 6 5 6 5` at 1.25 px with `pathLength="100"` so both
ends land on full dashes. ONE meaning across the whole deck, taught on slide 03
where the sixth mooring is phantom because the notice says up to six. It appears
on the sixth mooring (03), the rail below 2,000 m (06, 07, 08), the 15 m circle
(05), the third dial's rim and socket (07), and the Year 10 stub (09). Nowhere
else, and never decoratively.

## GLOBALS ON EVERY FRAME

`AKICE.water` to the ladder. `AKICE.marine` with a required `near` band,
`nearShare` 0.68, tint [196,226,224], `atten` from the basins. `AKICE.rail` at
x 1000, its returned scale written straight into `data-scale`.
`AKICE.railLabels` for every depth label, placed from the mapping and clamped.
Grain tile at 0.07 overlay, last layer. `AKPOST.grade` with `exposure` in the
house band and `grain` as an object. Counter top right. Watermark bottom left in
its own lane. Seed is `20260912 + slide index`.

---

## SLIDE 01 — THE PAIRED READOUT

### A. NARRATIVE

1. **Beat.** Two readings from one document hang in one water. One resolves to a
   point. The other is a fully legible dial with a printed scale and no needle.
   Inherits no loop. Plants the loop of what the blank one is.

2. **COPY, final.**
   - Kicker, mono 25 px: `BEAUFORT AND CHUKCHI SEAS, YEAR 9` (C05)
   - Headline, Fraunces 118 px, 2 lines broken by sense, 11 words:
     `The permit can find the robot.` / `It can't count the seal.` (C25, C43)
   - Label on the fix, mono 25 px: `POSITION, FIXED` (C25)
   - Label on the dial, mono 25 px, 2 lines: `STOCK ABUNDANCE` / `UNDETERMINED` (C43)
   - Dial face, Fraunces 96 px: `UND` (C43)
   - Counter, mono 22 px: `01 / 09` [furniture]
   - Provenance mark, mono 20 px: `TWO READINGS, ONE DOCUMENT` [furniture]
   - Watermark, mono 18 px: `alaskaaihq.com` [furniture]

3. **Reader takeaway.** The same document resolves the machine and leaves the
   animal blank.

### B. COMPOSITION

4. **Layout map.** 12 x 8 grid, 80 px margins. The lit crust occupies rows 1 to 1
   and the ice underside sits at y 112. Headline mass rows 3 to 5, cols 1 to 8,
   optically pulled 6 px left so the stems align. THE FIX upper right at [822,
   352], cols 9 to 12 rows 2 to 3. THE DIAL lower left at [330, 980], cols 1 to 5
   rows 6 to 8. Focal point is the dial's empty socket, and the eye path is
   headline, then the fix, then down the diagonal to the socket. Quiet zone upper
   right between the fix and the headline, about 16 percent of frame. No grid
   violation used.

4a. **Lower-third treatment.** The blank dial is the largest mass in the frame and
   it sits in the band, a modelled solid whose bezel is drawn as a real thickness
   with a lit upper edge and a heavy dark lower lee from `AKICE.profile`, standing
   in front of the deepest and densest band of the marine snow population over the
   graded water of the value ladder, with the ray field's lower arcs passing behind
   it. Modelled tone, a solid and a population, never a plate or a hairline.

5. **Depth plan.** Water ladder `#1A4C57` to `#123E49`, then `AKICE.daylight`
   screened from the lid at peak 0.16 reach 620, then the ray field at low alpha,
   then the mote population, then the ice lid with its keels and brine channels,
   then the fix arcs, then the dial body, then type, then grain. Five depth cues:
   occlusion, the dial over the motes and the ray field; atmospheric contrast via
   `AKICE.contrast(y)`; scale gradient, mote radius falling with depth; detail
   density stripped in the middle band so the two readouts carry the frame; one key
   light at az 12 el 62 with the lighting-ranked profile. Focal plane is the dial.

6. **Continuity device state.** D1 window -3 to 33 m. D2, one gold point where two
   range arcs close, and NO gold anywhere on the dial. D3, the riser exits the
   right edge at y 980. D4, water top `#1A4C57`. D5, the provenance mark reads
   `TWO READINGS, ONE DOCUMENT`. D6, the dial's rim and socket are phantom dashed.

### C. ART DIRECTION

7. **Technique stack.** `AKICE.setWindow(-3, 33, 0, 1350)`.
   `AKICE.ice({seed: 20260913, thickness: 2.0, keels: [[210,9.0,150],[640,13.0,190],[930,7.0,120]], channels: 230})`,
   all keel numbers `[design]`. `AKICE.daylight({peak: 0.16, reach: 620})`.
   `AKICE.rays({seed: 570131, x: 822, y: 352, count: 18, curve: 0.0026, alpha: 0.18, blend: "screen", atten})`, `[design]`.
   `AKICE.marine({seed: 570111, count: 3600, near: [880, 1350], nearShare: 0.70, atten})`.
   THE FIX, two `AKICE.ring` arcs at r 300 and r 214 centred off frame, clipped so
   neither closes, width 9, alpha 0.5, plus a 10 px gold dot at [822, 352] with a
   3 px dark casing so it survives the thumb. THE DIAL, centre [330, 980], bezel
   outer radius 168 px, face flat on to camera so no perspective touches a
   quantity, bezel thickness in cabinet extrusion at half scale 45 degrees with
   three-face tone from the one key, rim phantom dashed at 1.25 px with
   `pathLength` set so both ends land on full dashes, and an unlit 11 px needle
   socket with its own occlusion seam. `AKICE.profile` on the dial silhouette at
   weight 2.0, heavyMul 1.6, threshold -0.12.
   `AKPOST.grade({exposure: -0.04, saturation: 1.04, contrast: 1.05, grain: {amount: 0.055, size: 2.0, seed: 20260912}, dither: true})`.

8. **Data-in-art mapping.** The dial prints a scale and carries NO mark, from C43.
   The fix is one point where two arcs close, from C25. Ray count, ring radii, the
   keel list and the dial's bezel radius are all `[design]`. Nothing on this frame
   encodes a verified quantity as a drawn length.

9. **Palette assignment.** bg `#1A4C57` to `#123E49`; ice `#D8ECEE` / `#9FC2C8` /
   `#5E838C`; arris `#E8F6F7` at 0.82; dial body `#0E2138` with a lit upper edge
   `#B9D6DA` and a lee at `rgba(4,12,16,0.88)`; dial rim, socket and `UND` all
   `#7D8F94`; fix arcs and dot `#FFC72C`; display type `#F4F8FF`; header fixtures
   `#16333B` on ice. Worst-case text contrast is the headline's lower line at
   `#F4F8FF` over water near `#143F4B`, target above 12 to 1.

10. **Type spec.** Headline Fraunces 118 px wght 640 opsz 96 SOFT 24 WONK 1,
    leading 0.97, tracking -2 percent, colour `#F4F8FF`, max width 760 px, fitted
    with `AK.fitText(el, {min: 84, max: 118, maxLines: 2})`. `UND` Fraunces 96 px
    wght 600 in `#7D8F94`. Labels JetBrains Mono 500 at 25 px caps, tracking +8
    percent, each in a container built by `AKFIT.plate` from its own measured ink.

11. **Anchor spec.** Two instrument readouts are the anchor, the fix and the dial.
    Annotation furniture is two leaders, each a world-coordinate polyline
    terminating on its own feature's coordinates and declared in
    `window.__akLeaders` with `at`, `to`, `from` and `label`. Leader one runs from
    the `POSITION, FIXED` label box to the gold dot's own centre and ends in a 5 px
    filled dot because it lands on a face. Leader two runs from the two-line label
    box to the dial rim's own coordinates and ends in an arrow because it lands on
    an edge. They do not cross. The depth rail is SUPPRESSED on the cover so the
    two readouts carry the frame alone.

11a. **WORDLESS CLAIM.** One reading resolves to a point and the other has nothing
    in it. Region A, the fix, `[782, 312, 80, 80]`. Region B, the dial's socket,
    `[290, 940, 80, 80]`. `reads` is `differ`. **BOTH RECTS ARE MEASURED OFF THE
    RENDERED PNG BEFORE DECLARATION**, never computed from this layout plan.

### D. VERIFICATION

12. **Reference intent.** Two instruments photographed in the same water, one
    working and one never fitted.

13. **Risk flags.** The headline is the deck's longest display string and could
    wrap to three lines, mitigated by `AK.fitText` with `maxLines: 2` and a `min`
    low enough that the fitter cannot bottom out. The lit crust makes light header
    type illegible, mitigated by the dark-on-ice rule measured on the prototype.
    The gold dot is small and could vanish at thumb size, mitigated by the 3 px
    casing and by its position against the darkest water on the frame.

14. **Acceptance checklist.**
    - [ ] The headline sets in exactly two lines and breaks after `robot.`
    - [ ] The wordmark and counter are dark ink on the ice, not light
    - [ ] Exactly one gold mark appears and it is the fix. No gold on the dial
    - [ ] The dial's rim is phantom dashed all the way round and its socket is empty
    - [ ] The dial's lower arcs are visibly heavier and darker than its upper edge
    - [ ] Both leaders land on their own feature and neither crosses the other
    - [ ] The mote population is visibly denser below 880 px than above it

## SLIDE 02 — WHAT THE SOUND IS FOR

### A. NARRATIVE

1. **Beat.** Pay off immediately. The mechanism, in the document's own words, with
   the physics as the deck's own gloss. Inherits the loop that something is in the
   water. Plants the loop of what is making the sound.

2. **COPY, final.**
   - Kicker, mono, 41 chars: `HOW A MACHINE UNDER ICE KNOWS WHERE IT IS`
   - Headline, Fraunces 72 px, 2 lines: `Sound is how the machine` / `knows where it is.`
   - Body, Space Grotesk 34 px, 40 words: `Above the ice, a glider gets its position from a satellite modem. Under the ice, that signal can't reach it. The notice says gliders then navigate by trilateration from moored acoustic sound sources, the geometry of intersecting circles.` (C27, C25)
   - Labels, mono: `RANGE FROM SOURCE A` · `RANGE FROM SOURCE B` · `RANGE FROM SOURCE C` · `THE FIX`
   - Depth note, mono: `GLIDERS TRANSIT TO DEPTHS OF UP TO 1,000 m` (C27)

3. **Reader takeaway.** Under ice a position is three distances, and the distances
   are sound.

### B. COMPOSITION

4. **Layout map.** Type right, cols 7 to 12, rows 3 to 6. Range arcs left. Focal
   point at the fix cross [392, 698], the lower left rule-of-thirds. Eye path is
   headline, body, then the three arcs converging on the cross. Quiet zone upper
   right at about 18 percent.

4a. **Lower-third treatment.** The interference field of the three sources sits at
   its densest across the whole band, a modelled population of thresholded bands
   rather than a wash, with the glider's body and its riser standing in it as a lit
   solid whose down-light arcs carry the heavy rank, and the graded water of the
   ladder behind both. The 100 m rail tick and its dimension extension lines sit on
   top of modelled ground, never on bare fill.

5. **Depth plan.** Water ladder, then the interference field, then the mote
   population attenuated by the basins, then three discrete gold arcs, then the
   glider and riser, then type, then grain. Four cues: occlusion, the glider over
   two of three arcs; atmospheric contrast via `AKICE.contrast`; scale gradient in
   the motes; one key light with the ranked profile. Focal plane is the glider.

6. **Continuity device state.** D1 window 0 to 120 m. D2, the gold mark above the
   ice is GONE and is rebuilt below as three arcs intersecting at one cross at 62
   m. D3, enters left at y 980, exits right at y 742. D4, water top `#123E49`.

### C. ART DIRECTION

7. **Technique stack.** Interference rings, library 13, as the sound field:
   brightness is the sum of sin(dist(p, source_i) times f plus phase_i) from three
   off-frame sources at [-240, 210], [1290, 640] and [430, -180], f 0.021,
   thresholded into 14 bands at alpha 0.05 to 0.11, screen blend, all `[design]`.
   Three `AKICE.ring` arcs on top at width 7, alpha 0.52, rgb [255,199,44], clipped
   so no full circle closes. `AKICE.profile` on the glider. Leaders per library 72,
   oblique snapped to 15 degrees with an 18 px elbow at the text end, each
   terminating on its own arc's coordinates and declared in `window.__akLeaders`
   with `at`, `to`, `from` and `label`.

8. **Data-in-art mapping.** Source positions, f and the band count are `[design]`.
   The glider sits at 62 m `[design]`. The only verified figure on the frame is
   1,000 m (C27) and it is typed, not drawn as a length.

9. **Palette assignment.** Water `#123E49` to `#0C2E38`; interference bands
   `#BAD6DA` at 0.05 to 0.11; arcs and cross `#FFC72C`; glider `#0A2530` with lit
   cap `#B9D6DA`; type `#F4F8FF` and `#D8ECEE`; labels `#BAD6DA`. Gold budget is
   the three arcs and the cross and nothing else.

10. **Type spec.** Headline Fraunces 72 px wght 600 SOFT 12 WONK 0, leading 1.02,
    tracking -1.5 percent, max width 520 px, fitted `maxLines: 2`. Body Space
    Grotesk 500 at 34 px, leading 1.38, max width 520 px. Labels mono 25 px caps
    tracked +8 percent, every one in a container built by `AKFIT.plate` from its
    own measured ink.

11. **Anchor spec.** The glider is the literal anchor. Annotation furniture is
    four leaders, the depth rail with ticks at 0, 50 and 100 m, and one dimension
    call on the 100 m tick.

### D. VERIFICATION

12. **Reference intent.** A navigation plot that happens to be underwater.

13. **Risk flags.** Four mono labels in the same region could collide, mitigated
    because every container is measured and `AKFIT.guard` fails the render if one
    is narrower than its string. A leader could land in void, mitigated by the
    declaration and by qa.py's 24 px landing gate. The interference field could
    swamp the three discrete arcs, mitigated by capping band alpha at 0.11 against
    the arcs' 0.52.

14. **Acceptance checklist.**
    - [ ] Three arcs meet at ONE point and the cross sits exactly there
    - [ ] Every one of the four labels sits inside its own measured container
    - [ ] The word GPS appears nowhere on the slide
    - [ ] The trilateration sentence carries the words `The notice says`
    - [ ] The glider occludes two arcs and is occluded by none
    - [ ] No full gold circle closes anywhere on the frame

---

## SLIDE 03 — WHAT GOES IN

### A. NARRATIVE

1. **Beat.** The inventory, as real objects at real depths in one body of water.
   Inherits the loop of what makes the sound. Plants the loop that all of this
   runs for a year.

2. **COPY, final.**
   - Kicker, mono: `THE GRID, AS AUTHORIZED`
   - Headline, Fraunces 72 px, 2 lines: `Up to six moorings,` / `two drifting buoys.` (C14, C15)
   - Body, Space Grotesk, 48 words: `The moorings are fixed acoustic navigation sources at 900 to 950 Hz. Each transmits a 30 second pulse every four hours. Two ice gateway buoys drift with the ice on the same cycle. Source levels this year stay under 185 dB re 1 uPa at 1 m.` (C14, C18, C17, C15, C30, C19)
   - Labels, mono: `MOORING, FIXED` · `ICE GATEWAY BUOY, DRIFTING` · `900 TO 950 Hz` · `30 s EVERY 4 h` · `NTE 185 dB re 1 uPa at 1 m`

3. **Reader takeaway.** Eight sources go in, and they are quiet and constant
   rather than loud and occasional.

### B. COMPOSITION

4. **Layout map.** Type left, cols 1 to 6, rows 2 to 4. Objects staggered across
   cols 5 to 12 at four different depths so nothing lines up into a row. Focal
   point on the nearest buoy at [742, 512]. Eye path headline, body, nearest buoy,
   then down the stagger. Quiet zone upper right at 16 percent.

4a. **Lower-third treatment.** The two deepest mooring bodies stand in it with
   their risers running down, each modelled with a two-strip value ladder and
   `AKICE.profile`'s lighting rank so the down-light arcs go heavy and dark, with
   the mote population at its densest around them and the graded water carrying
   tone behind. The 400 m rail tick lands on modelled ground.

5. **Depth plan.** Water, motes, ray field at low alpha, eight object bodies in
   depth order, type, grain. Four cues: occlusion between staggered bodies;
   atmospheric contrast; scale gradient, bodies drawn smaller with depth; detail
   density stripped in the upper third.

6. **Continuity device state.** D1 window 20 to 400 m. D2, eight gold arc ticks,
   one at each source, no intersection drawn. D3, enters 742, exits 1,106. D4,
   water top `#0C2E38`.

### C. ART DIRECTION

7. **Technique stack.** Five mooring bodies drawn SOLID and a sixth drawn as a
   phantom dash, library 67, `30 5 6 5 6 5` at 1.25 px, because the notice says up
   to six and the drawing should say up to six too (C14). Two buoy bodies solid and
   no phantom, because C15 carries no hedge. Each body modelled with
   `AKICE.profile` at weight 2.0. Haloed balloon numbers, library 74, at 26 px with
   a 3 px halo ring on the eight sources. `AKICE.rays` at low alpha 0.16 to keep
   the column from going flat behind the objects, `[design]`.

8. **Data-in-art mapping.** Five solid plus one phantom mooring equals the `up to
   six` of C14, and the phantom IS the hedge drawn. Two solid buoys equals C15.
   Eight balloon numbers equal the eight sources in use. The gold arc length is
   0.75 degrees, which is 30 seconds in every four hours at 1 part in 480
   `[design]` from C17.

9. **Palette assignment.** Water `#0C2E38` to `#08202A`; bodies `#0A2530` with lit
   caps `#B9D6DA`; phantom body `#7D8F94`; balloons `#BAD6DA` on halo; gold ticks
   `#FFC72C`; type `#F4F8FF` and `#D8ECEE`.

10. **Type spec.** As slide 02. Five mono labels, every one in a measured
    container.

11. **Anchor spec.** Eight drawn instruments are the anchor. Furniture is eight
    balloon numbers and the rail with ticks at 50, 100, 200, 300 and 400 m.

### D. VERIFICATION

12. **Reference intent.** A mooring deployment diagram redrawn as a lit scene.

13. **Risk flags.** Eight labelled objects risks reading as a catalogue rather
    than a place, mitigated by the four-depth stagger and by the ray field behind
    them. The phantom sixth mooring could read as a rendering error rather than as
    a hedge, mitigated by its own balloon number and by the `UP TO` in the
    headline.

14. **Acceptance checklist.**
    - [ ] Exactly five mooring bodies are solid and exactly one is phantom dashed
    - [ ] Exactly two buoy bodies are drawn and both are solid
    - [ ] No two objects share a depth
    - [ ] Every source level string carries `dB re 1 uPa at 1 m`
    - [ ] The figure 190 appears nowhere on the slide
    - [ ] Every one of the five labels sits inside its own measured container

---

## SLIDE 04 — THE PLACE. BREATHER, DECLARED.

### A. NARRATIVE

1. **Beat.** Rest. Let the reader be somewhere with no lid, no ship and no grid in
   it. Inherits the year loop. Plants the loop of how big this water is.

2. **COPY, final.**
   - Kicker, mono: `THE STUDY AREA`
   - Headline, Fraunces 72 px, 2 lines: `This is the water` / `the permit is about.`
   - Body, Space Grotesk, 24 words: `The study area is about 639,237 square kilometres. Its closest point to the Alaska coast is 204 kilometres, or 110 nautical miles.` (C11, C12)
   - Mono, 2 lines: `THREE JURISDICTIONS, THE US EEZ,` / `THE HIGH SEAS DESCRIBED AS THE GLOBAL COMMONS, AND PART OF THE CANADIAN EEZ` (C13)
   - Dimension call, mono: `UP TO 1,000 m, GLIDER TRANSIT DEPTH` (C27)
   - Drift note, mono: `0.25 METRES PER SECOND, ABOUT 23 km A DAY` (C26)

3. **Reader takeaway.** The permit's water is enormous and the nearest coast is a
   long way off.

### B. COMPOSITION

4. **Layout map.** Type upper left, cols 1 to 7, rows 2 to 4. Quiet zone upper
   right, capped at 22 percent and deliberately NOT the bottom band. Focal point
   the glider at [676, 930]. `data-breather` IS NOT SET, because this frame still
   carries a modelled lower third and does not need the demotion.

4a. **Lower-third treatment.** The glider's modelled body sits in it at the 1,000
   m mark with its dimension call, drawn as a lit solid with the lighting-ranked
   profile and the deck's single use of aurora green on its upper surface, and the
   mote population reaches its greatest density across the whole band, with the
   graded water of the ladder behind. Modelled tone and a solid, not furniture.

5. **Depth plan.** Water, motes, one faint gold arc, the glider, type, grain. Four
   cues: occlusion, the glider over the arc; atmospheric contrast; scale gradient
   in the motes; detail density stripped in the far upper third.

6. **Continuity device state.** D1 window 380 to 1,000 m. D2, one faint arc across
   the upper third at alpha 0.18, the sound still arriving from above. D3, enters
   1,106, exits 610. D4, water top `#08202A`.

### C. ART DIRECTION

7. **Technique stack.** `AKICE.water`, `AKICE.marine({count: 3000, near: [880, 1350]})`,
   one `AKICE.ring` arc at alpha 0.18, `AKICE.profile` on the glider with a stipple
   tone field, library 66, on its lit face. `AKICE.daylight` at peak 0.09, the last
   frame that carries any.

8. **Data-in-art mapping.** Mote count 3,000 as the study area at one mote per
   about 213 square kilometres `[design]`, derived from C11. The glider's depth on
   the rail IS 1,000 m and that is verified (C27), so the rail tick at 1,000 m and
   the glider's y are the same number by construction.

9. **Palette assignment.** Water `#08202A` to `#061821`; glider `#0A2530` with its
   upper surface `#3CE6B4`, the deck's only use; gold arc `#FFC72C` at 0.18; type
   `#F4F8FF` and `#D8ECEE`; mono `#BAD6DA`.

10. **Type spec.** As slide 02. The two-line mono jurisdiction string is the
    deck's longest mono run and sets at 25 px with a 520 px measure.

11. **Anchor spec.** The glider. Furniture is the rail at 400, 600, 800 and 1,000
    m, one dimension call, and the drift note.

### D. VERIFICATION

12. **Reference intent.** Open water, the middle of a long transit.

13. **Risk flags.** A breather frame in a deck already worried about wallpaper is
    the likeliest place to be called empty, mitigated by putting the deck's
    HIGHEST mote count on it and by giving it the only aurora-green object.

14. **Acceptance checklist.**
    - [ ] The Alaska coast is not drawn anywhere, and 204 kilometres is typed
    - [ ] The jurisdiction string names three, including Canada
    - [ ] The glider sits exactly on the 1,000 m rail tick
    - [ ] Aurora green appears on this slide and on no other
    - [ ] Square kilometres, never square miles

---

## SLIDE 05 — EVERY ZONE, AT ONE SCALE

### A. NARRATIVE

1. **Beat.** The permit's protective geometry, drawn honestly at the section's own
   metre scale. Inherits the size loop. Plants the loop of who is watching for the
   other eleven months.

2. **COPY, final.**
   - Kicker, mono: `THE MITIGATION ZONES, DRAWN TO THE SAME SCALE`
   - Headline, Fraunces 72 px, 2 lines: `Every zone in the permit,` / `at one scale.`
   - Body, Space Grotesk, 40 words: `Vessels hold 457 metres from observed cetaceans and 183 metres from other observed marine mammals. Deployment and recovery of a source carries a 55 metre zone. The estimated range to temporary hearing threshold shift is under 15 metres.` (C45, C46, C50)
   - Labels, mono: `457 m, OBSERVED CETACEANS` · `183 m, OTHER OBSERVED MARINE MAMMALS` · `55 m, DURING DEPLOYMENT AND RECOVERY` · `UNDER 15 m, ESTIMATED RANGE TO TTS`
   - Lower band line, Space Grotesk 32 px: `The 55 metre zone applies during deployment and recovery, not for the year the source then transmits.` (C46, C16)
   - Finding, mono: `LEVEL A HARASSMENT NEITHER ANTICIPATED NOR AUTHORIZED` (C37)

3. **Reader takeaway.** The protections are real, they are small, and most of them
   need a person aboard.

### B. COMPOSITION

4. **Layout map.** Type upper right, cols 6 to 12, rows 1 to 4. Circles low left.
   Focal point the common centre at [396, 902]. The single permitted grid violation
   is the 457 m circle breaking the left margin, which is how a 457 m radius
   actually behaves at this scale.

4a. **Lower-third treatment.** The two largest mitigation circles' lower arcs
   sweep through it as cased lines over the deepest and densest band of the mote
   population, with the graded water of the ladder carrying modelled tone behind
   them, and the lower band sentence set inside a basin in that field rather than
   on a plate. The circles are drawn ink on worked ground, never furniture on bare
   fill.

5. **Depth plan.** Water, motes, four nested circles, the gold cross, type, grain.
   Four cues: occlusion of motes by the cased circle lines; atmospheric contrast;
   scale gradient; detail density stripped above 700 m.

6. **Continuity device state.** D1 window 500 to 2,000 m, which puts the scale at
   0.90 px per metre. D2, the gold cross sits at the exact common centre of all
   four circles, which is literally true of the permit. D3, enters 610, exits 928.
   D4, water top `#061821`.

### C. ART DIRECTION

7. **Technique stack.** Four nested circles at TRUE relative radius, 411 px, 165
   px, 50 px and 13.5 px at 0.90 px per metre, all cool ink `#BAD6DA`, none gold.
   Weights by meaning, 2 px for the two observed-animal zones, 1.25 px for the 55 m
   and for the 15 m. Phantom dash, library 67, on the 15 m circle only, since it is
   modelled rather than required. Cased lines, library 79, so every circle survives
   the mote field. Dimension calls, library 73, with 4 px gaps, 6 px overshoots and
   3 to 1 arrowheads, rows 24 px then 16 px apart. The 15 m circle's leader ends in
   a 5 px filled dot ON its rim, because at 13.5 px radius an arrowhead cannot land.

8. **Data-in-art mapping.** Radii are 457 m and 183 m (C45), 55 m (C46) and under
   15 m (C50), all at 0.90 px per metre from the window, so the drawn lengths are
   the verified metres and the scale is the slide's own mapping. This is the deck's
   only frame where a verified quantity is drawn as a length.

9. **Palette assignment.** Water `#061821` to `#04111A`; circles `#BAD6DA` with
   casings in the local water value; the 15 m circle `#7D8F94` phantom; cross
   `#FFC72C`; type `#F4F8FF` and `#D8ECEE`.

10. **Type spec.** As slide 02, plus the lower band line at Space Grotesk 500, 32
    px, which is exactly the body floor and not below it.

11. **Anchor spec.** The four circles are the anchor and the annotation. Furniture
    is four dimension calls and the rail at 500, 1,000, 1,500 and 2,000 m.

### D. VERIFICATION

12. **Reference intent.** A range card, drawn to scale for once.

13. **Risk flags.** The 13.5 px circle is near the limit of legibility at thumb
    size, mitigated by the filled-dot terminator and by its label carrying the
    number in type. The 457 m circle leaving the frame could read as a mistake,
    mitigated by its label sitting on the visible arc.

14. **Acceptance checklist.**
    - [ ] All four circles share one centre and the gold cross is exactly on it
    - [ ] The four radii are in the ratio 457 to 183 to 55 to 15, measurable
    - [ ] No circle is gold
    - [ ] The 15 m circle is the only phantom-dashed one
    - [ ] The lower band line sets at 32 px and not below
    - [ ] Level A is stated as neither anticipated nor authorized

---

## SLIDE 06 — THE UNATTENDED YEAR. THE TURN.

### A. NARRATIVE

1. **Beat.** The temperature goes cold. The deck's strongest single image.
   Inherits the watching loop. Plants the loop that the permit is written about
   two animals.

2. **COPY, final.**
   - Kicker, mono: `WHAT RUNS AFTER THE SHIP GOES HOME`
   - Headline, Fraunces 72 px, 2 lines: `A 22 day cruise.` / `A full year of transmission.` (C31, C16)
   - Body, Space Grotesk, 46 words: `The cruise is planned for 22 days starting September 22nd, on a ship the notice calls ice strengthened rather than icebreaking. The sources stay in and keep transmitting until September 13th, 2027. Mitigation that depends on an observer only works while an observer is aboard.` (C31, C32, C34, C02, C45)
   - Labels, mono: `ONE TICK, ONE 30 SECOND TRANSMISSION` (C17) · `EVERY FOUR HOURS` (C17) · `THE 22 DAYS WITH A SHIP ABOARD` (C31) · `THE REST OF THE YEAR` (C16)

3. **Reader takeaway.** A person is there for three weeks of a year of
   transmission.

### B. COMPOSITION

4. **Layout map.** Type left, cols 1 to 6, rows 2 to 5. Pulse field right, cols 7
   to 12, rows 1 to 7. Focal point where the gold band ends, [812, 318], the
   frame's one hard value break. Eye path headline, the gold band, the long dim
   field below it.

4a. **Lower-third treatment.** The pulse field's own lower nine hundred ticks
   occupy it as a dense modelled population rather than a wash, the phantom rail
   tail runs down through it carrying the undetermined ink, and the deepest and
   densest band of the mote population sits behind both over graded water. The
   lower third is the majority of the argument on this frame and carries the most
   ink in the deck.

5. **Depth plan.** Water, motes, the pulse field, type, grain. Four cues:
   occlusion of motes by ticks; atmospheric contrast; scale gradient; detail
   density stripped left of the field so the type side stays quiet.

6. **Continuity device state.** D1 window 800 to 2,600 m. D2, gold at full
   strength on the 132 attended ticks. THIS IS NOT THE DECK'S PEAK GOLD AND THE
   PLAN WAS WRONG TO SAY IT WAS, corrected in round 3 by counting pixels: this
   frame carries 11,330 gold pixels against slide 02's 19,735, and it SHOULD,
   because 132 of 2,190 is a small share by construction and that share is the
   whole argument. Peak INTENSITY, not peak area. D3, enters 928, exits
   1,192. D4, water top `#04111A`.

7. **Technique stack.** THE PULSE FIELD. Hairline ticks at 0.75 px, six per day
   for 365 days, laid in 30 columns within cols 7 to 12, each tick a `fillRect` and
   never a stroke. The top band, six per day for the 22 days with a ship aboard, is
   drawn gold-warm `#FFC72C` at alpha 0.62 in one contiguous run. The remainder is
   `#7D8F94` at alpha 0.30. Nothing about the ratio is annotated beyond the four
   labels, because the picture is the argument. The rail's last tick is 2,000 m and
   below it the rail continues as a phantom dash with NO ticks.

8. **Data-in-art mapping.** Six ticks per day for 365 days `[design]`, the product
   of C17's four-hour cycle and C16's one year. The lit run is six per day for the
   22 days of C31, also `[design]` as a product. Only `22 days`, `every four hours`
   and the year are PRINTED; neither product is.

9. **Palette assignment.** Water `#04111A` to `#03090C`; attended ticks `#FFC72C`
   at 0.62; unattended ticks `#7D8F94` at 0.30; phantom rail `#7D8F94`; type
   `#F4F8FF` and `#D8ECEE`.

10. **Type spec.** As slide 02. Four mono labels, each in a measured container,
    two of them set against the tick field and therefore basined.

11. **Anchor spec.** The pulse field is both anchor and annotation. Furniture is
    four labels and the rail, whose ticks stop at 2,000 m.

### D. VERIFICATION

12. **Reference intent.** A tally sheet that turned out to be mostly blank.

13. **Risk flags.** A field of thousands of hairlines could moire at thumb size,
    mitigated by a 0.75 px tick on a 2x backing store and by column spacing chosen
    against the 432 px downsample. The gold band could read as a highlight rather
    than as a count, mitigated by its label naming one tick as one transmission.

14. **Acceptance checklist.**
    - [ ] The gold run is ONE contiguous band at the top of the field, not scattered
    - [ ] The gold band is visibly a small fraction of the field at thumb size
    - [ ] The rail carries no tick below 2,000 m and continues as a phantom dash
    - [ ] Neither derived product is printed anywhere on the slide
    - [ ] The ship is described as ice strengthened rather than icebreaking

---

## SLIDE 07 — THE STOCK GAUGE. THE TURN, AND THE KEEPER.

### A. NARRATIVE

1. **Beat.** Same water, same window, same instrument grammar, different question.
   The temperature turns here. Inherits the unattended loop. Plants the loop of
   what the finding rests on.

2. **COPY, final.**
   - Kicker, mono: `STOCK ABUNDANCE ESTIMATES. NOT TAKE.`
   - Headline, Fraunces 72 px, 2 lines: `The same page gives` / `the seal's number as UND.` (C43)
   - Body, Space Grotesk 34 px, 36 words: `Beaufort beluga, 39,258, from a 1992 survey. Eastern Chukchi beluga, 13,305, from 2017, at a coefficient of variation of 0.51. Arctic ringed seal, the one species here listed as threatened, undetermined.` (C41, C42, C43, C39)
   - Dial one face, mono 44 px tabular: `39,258` (C41)
   - Dial two face, mono 44 px tabular: `13,305` (C42)
   - Dial three face, Fraunces 96 px: `UND` (C43)
   - Dial labels, mono 25 px: `BEAUFORT BELUGA, CV 0.229, 1992 SURVEY` (C41) · `EASTERN CHUKCHI BELUGA, CV 0.51, 2017 SURVEY` (C42) · `ARCTIC RINGED SEAL, LISTED THREATENED` (C39, C43) · `PBR, UNDETERMINED` (C43) · `NO VALUE TO PLOT` (C43)
   - Provenance mark, mono 20 px: `RING RADIUS IS A COEFFICIENT OF VARIATION, NOT A DISTANCE` [furniture]

3. **Reader takeaway.** Two dials have a needle and the threatened one has an
   empty socket.

### B. COMPOSITION

4. **Layout map.** Three dials on a descending diagonal, centres at [300, 420],
   [540, 730] and [780, 1040], asymmetric on the symmetric grid. Type rows 1 to 2
   across cols 1 to 8, clear of dial one. Focal point dial three's empty socket at
   [780, 1040], the lower right rule-of-thirds. Eye path headline, dial one's
   needle, down the diagonal, then the socket. No grid violation used.

4a. **Lower-third treatment.** Dial three is the largest mass on the frame and it
   sits in the band, a modelled solid with its bezel drawn in cabinet extrusion so
   the thickness is real, its upper rim carrying the lit edge and its lower arcs
   carrying the heavy dark lee rank from `AKICE.profile`, over the deepest and
   densest band of the mote population and the graded water of the ladder. The
   composition's mass is moved DOWN on purpose, which is also what makes the blank
   read at thumb size. Modelled tone and a solid, never a plate.

5. **Depth plan.** Water, motes, three dial bodies in depth order, needles, type,
   grain. Five cues: occlusion, dial three over the mote field; atmospheric
   contrast, via `AKICE.contrast` which is near its most compressed here; scale
   gradient, the three dials at one size but progressively lower contrast with
   depth; the cabinet extrusion's own three-face tone; one key light at az 12.

6. **Continuity device state.** D1 window 1,000 to 3,000 m. **CORRECTED
   2026-09-12, ROUND 3.** This section said the window was held IDENTICAL to
   slide 06 and it is not: 06 runs 800 to 2,600 m and this frame runs 1,000 to
   3,000, which the arc table has said all along. The scorer caught the
   contradiction and it matters, because the unchanged environment argument this
   frame leans on was resting on a sentence that was false. The argument still
   holds in the form the arc table supports, which is that the window ADVANCES
   by the smallest step in the deck, 200 m against the 300 to 600 m elsewhere,
   so the instrument changes and the water very nearly does not. The water does not change between the beat before the turn and the
   turn, which is the unchanged-environment discipline: the instrument moved and
   the world did not. D2, gold appears on two needle caps and is WITHHELD from the
   third dial entirely. D3, enters 1,192, exits 520. D4, water top `#03090C`.
   D5, the provenance mark. D6, dial three's rim and socket are phantom dashed.

### C. ART DIRECTION

7. **Technique stack.** Three dials as modelled objects hanging in water, never a
   chart on a sheet. Outer bezel radius 148 px. The dial FACE is flat on to camera
   so no perspective ever touches a quantity, and the bezel thickness is drawn in
   cabinet extrusion, library 39, front face undistorted with depth at half scale
   45 degrees, walls darker and lid lightest, three-face tone from the one key.
   `AKICE.profile` on each bezel silhouette at weight 2.0, heavyMul 1.6, threshold
   -0.12. Needles are 2 px machined ink with a 5 px gold cap. The uncertainty band
   is an arc on the rim whose angular half width is the coefficient of variation
   times the needle's own value in the dial's units, DRAWN and never printed as a
   product. Dial three carries a phantom dashed rim all the way round, library 67
   at 1.25 px with `pathLength="100"` so both ends land on full dashes, an unlit 11
   px needle socket with its own occlusion seam, and `UND`. Every instrument mark
   elsewhere on the frame drops to a context grey at 45 percent opacity, per the
   Tufte tiers, because on the turn the machine is context and the animal is data.

8. **Data-in-art mapping.** Dial one's needle angle is 39,258 on the shared
   abundance scale (C41) and its uncertainty arc half width is 0.229 of that
   (C41). Dial two's needle is 13,305 (C42) and its arc half width is 0.51 of that
   (C42), which is visibly more than twice dial one's and is the honest reading of
   an imprecise estimate. Dial three has NO needle and NO arc, from C43. The dial
   span of 40,000 is `[design]`.

9. **Palette assignment.** Water `#03090C` to `#02080D`; bezels `#0E2138` with lit
   upper edges `#B9D6DA` and lee arcs `rgba(4,12,16,0.88)`; dial faces and needles
   `#6EA5FF`, which is the animal voice; needle caps `#FFC72C` on dials one and
   two ONLY; dial three's rim, socket, `UND` and whole label group `#7D8F94`;
   type `#F4F8FF` and `#D8ECEE`. **NO GOLD TOUCHES DIAL THREE.** That absence is
   the deck's argument and it is auditable in one pass.

10. **Type spec.** Headline Fraunces 72 px wght 600 SOFT 12 WONK 0, fitted
    `maxLines: 2`. Body Space Grotesk 500 at 34 px, max width 520 px. Dial faces
    mono 44 px `tabular-nums lining-nums` on dials one and two, and Fraunces 96 px
    for `UND` on dial three, which is the deck's one place a display face carries a
    non-numeral where a numeral should be. Five mono labels at 25 px, every one in
    a container built by `AKFIT.plate` from its own measured ink so a longer
    species name grows its own box.

11. **Anchor spec.** The three dials are the anchor and the annotation together.
    Furniture is five leaders, each a world-coordinate polyline terminating on its
    own feature's coordinates and declared in `window.__akLeaders` with `at`, `to`,
    `from` and `label`. Targets are dial one's needle tip, dial one's uncertainty
    arc outer edge, dial two's uncertainty arc, dial three's empty socket centre,
    and dial three's rim at its 200 degree point for the PBR label. None cross.

11a. **WORDLESS CLAIM.** Two dials have a needle and the third has a socket, and
    that reads with no words at all. Region A, dial one's needle and cap,
    `[262, 296, 80, 80]`. Region B, dial three's empty socket,
    `[740, 1000, 80, 80]`. `reads` is `differ`. **BOTH RECTS ARE MEASURED OFF THE
    RENDERED PNG BEFORE DECLARATION**, never computed from this layout plan, which
    is the No.29 discipline.

### D. VERIFICATION

12. **Reference intent.** A panel of survey instruments, one of which was never
    fitted.

13. **Risk flags.** A reader arriving from slide 05's metre radii could carry
    metres into this frame and read the uncertainty arc as a distance, mitigated by
    the provenance mark saying exactly that and by the two frames never sharing a
    unit on screen. An empty dial could read as unfinished art, mitigated because
    the rim, the scale, the socket and the label are all fully drawn and only the
    needle is absent, which is the difference between a blank and a gap. A tick
    standing in for a missing value would be the No.35 defect, and it is refused
    outright: dial three carries NO mark and prints `NO VALUE TO PLOT` instead.

14. **Acceptance checklist.**
    - [ ] Dial three has no needle, no gold and no mark of any kind on its scale
    - [ ] Dial three's rim is phantom dashed all the way round and both ends land on full dashes
    - [ ] Dial two's uncertainty arc is visibly more than twice dial one's
    - [ ] All three dials print the SAME abundance scale, so the two figures are comparable
    - [ ] The kicker reads ABUNDANCE ESTIMATES. NOT TAKE. and is legible at thumb size
    - [ ] Every one of the five labels sits inside its own measured container
    - [ ] The bezel's lower arcs are visibly heavier and darker than its upper edge

## SLIDE 08 — WHAT THE RECORD IS

### A. NARRATIVE

1. **Beat.** Synthesis, the thesis sentence, and the fairness clause that keeps a
   permittee reading. Inherits the what-it-rests-on loop. Plants the close.

2. **COPY, final.**
   - Kicker, mono: `NINE YEARS, ONE YEAR AT A TIME`
   - Headline, Fraunces 72 px, 3 lines: `The permit knows` / `where the machine is.` / `The rest is undetermined.`
   - Body, Space Grotesk, 45 words: `The authorization runs from September 14th and by statute can't run longer than a year, which is why there are nine of them. It relies on a Biological Opinion issued on September 13th, 2022. Three private citizens wrote in.` (C02, C47, C06, C40, C44)
   - Tags, mono: `BIOLOGICAL OPINION, SEPTEMBER 13TH, 2022` (C40) · `THREE COMMENT LETTERS, PRIVATE CITIZENS` (C44)
   - Honesty line, mono, 2 lines: `THE RECORD'S DEEPEST STATED DEPTH IS 2,000 METRES.` / `BELOW THAT, THIS SECTION IS DRAWN AND NOT MEASURED.` (C23, `[design]`)

3. **Reader takeaway.** Nine years of this is carried by a four year old finding
   and three letters.

### B. COMPOSITION

4. **Layout map.** Type upper left, cols 1 to 7, rows 1 to 4. The anchor at [486,
   1178], the low left rule-of-thirds. Focal point the anchor's contact. Eye path
   headline, tags, then down to the anchor on the bed.

4a. **Lower-third treatment.** The sea bed finally arrives and fills it, an
   engraved surface with modelled tone across its whole width, and the mooring's
   anchor stands on it with a two-part contact shadow drawn in the only order that
   measures, a lit pool laid down first, then the cast, then the hard seam at the
   foot. The phantom rail tail descends through it. This is the most modelled lower
   third in the deck, deliberately, because the deck has been descending toward it
   for eight frames.

5. **Depth plan.** Water, motes, the engraved bed, the lit pool, the anchor, the
   cast, the seam, type, grain. Five cues: occlusion, the anchor over the bed;
   atmospheric contrast at its most compressed; scale gradient; the contact shadow
   itself; one key light.

6. **Continuity device state.** D1 window 1,200 to 3,400 m. D2, the gold cross is
   the only bright mark above the bed. D3, enters 520, exits 860. D4, water top
   `#02080D`.

### C. ART DIRECTION

7. **Technique stack.** The bed is one `AKENGRAVE` surface with `seedDeg` 37 to
   dodge the one-axis lay collapse that cost No.49 four diagnoses in one deck, tone
   0.62 to 0.18, wMax 2.2, inkLo `#02060F`, inkHi `#0C2328`, `form` a shallow
   two-term proxy solid precomputed into a 4 px lookup grid so `normalAt` is not
   calling a many-term function millions of times. `akcolor.js` loads BEFORE
   `akengrave.js`, always. Then the contact, `AKICE.litPool` at peak 0.26 centred
   at foot plus 14 with rx 96, then `AKICE.cast` at foot plus 2 with w 88 and k
   1.0, then `AKICE.seam`. The two declared rects go SIDE BY SIDE at the anchor's
   own base line and are MEASURED with
   `python3 scripts/contact_probe.py --render-dir out/2026-09-12/render --slide 8 --base 486,1178`,
   never typed.

8. **Data-in-art mapping.** Nothing on this frame encodes a verified quantity as a
   drawn length. The bed's depth is `[design]` and the honesty line says so on the
   slide, which is the deck's own disclosure rather than a caption.

9. **Palette assignment.** Water `#02080D` to `#02060F`; bed `#02060F` to
   `#0C2328`; anchor `#0A2530` with lit cap `#B9D6DA`; pool a screened lift, cast
   and seam in darkened water hues and never black; cross `#FFC72C`; tags `#BAD6DA`
   with the 2022 tag in `#6EA5FF`; honesty line `#7D8F94`.

10. **Type spec.** As slide 02, with the honesty line in mono 22 px, tracked +8
    percent, in the undetermined ink.

11. **Anchor spec.** The anchor block on the bed is the literal anchor. Furniture
    is two measured tags, the honesty line, and the phantom rail.

### D. VERIFICATION

12. **Reference intent.** The bottom of a long dive, with one made thing on it.

13. **Risk flags.** The deck's darkest frame could measure as a dead canvas,
    mitigated by the engraved bed's own tone range and by the contact pair.
    A contact shadow on near-black ground measures nothing, mitigated by laying the
    lit pool FIRST and by earning separation from the cast's k rather than by
    raising the pool, whose ceiling is 0.28 in code.

14. **Acceptance checklist.**
    - [ ] `data-contacts` is declared in the MARKUP on the body tag, not written at runtime
    - [ ] The shadow and ground rects sit SIDE BY SIDE at the anchor's base line, not stacked
    - [ ] The measured separation is above 4.0 L star and the pair reads as attached, not as a hole in a spotlight
    - [ ] The bed carries visible engraved tone across its full width
    - [ ] The honesty line about drawn versus measured depth is present
    - [ ] The count nine refers to YEARS and never to a stack of documents

---

## SLIDE 09 — CLOSE. ONE ASK.

### A. NARRATIVE

1. **Beat.** Back at the bed, the camera stopped. One ask. Inherits everything.
   Plants nothing; the deck ends.

2. **COPY, final.**
   - Wordmark, Fraunces: `ALASKA.AI` [furniture]
   - Headline, Fraunces 82 px, 2 lines: `A robot's position` / `or a seal's number.`
   - The single ask, Space Grotesk 36 px: `Year 10 is already inside the comment scope of Year 9. Which of those two numbers should the next authorization improve?` (C53)
   - Counter, mono: `09 / 09` [furniture]
   - Watermark, mono: `alaskaaihq.com` [furniture]

3. **Reader takeaway.** There is a next one, and it is already open.

### B. COMPOSITION

4. **Layout map.** Centred type, which the doctrine reserves for a one to two line
   title card and this is one. Rows 3 to 6. The Polaris at [908, 262], the upper
   right rule-of-thirds. NO SOURCE NOTE anywhere on the frame, per the owner's
   2026-09-11 change.

4a. **Lower-third treatment.** The bed is held from slide 08 with its engraved
   tone intact and the anchor still standing on it, now with the near-third mote
   population stripped by 40 percent so the frame reads as the same place seen a
   moment later, and the riser descends into the band and dead-ends on the anchor
   shackle. A modelled surface, a solid and a population, not furniture.

5. **Depth plan.** As slide 08, with the mote population reduced and no new
   layer. Four cues: occlusion, atmospheric contrast, scale gradient, one key
   light.

6. **Continuity device state.** D1 window held identical to 08 at 1,200 to 3,400
   m, the camera's full stop. D2, the gold cross resolves into the four point
   Polaris. D3, enters 860 and DEAD-ENDS on the anchor shackle, the deck's one
   permitted termination. D4, water top `#02060F`, held.

### C. ART DIRECTION

7. **Technique stack.** Identical chassis calls to slide 08 with the same seeds
   for the bed, so the place is demonstrably the same place, and a different seed
   for the mote population so the water has moved. The Polaris is a four point star
   drawn in DOM/SVG so the film grade never shifts the brand mark.

8. **Data-in-art mapping.** None. This frame carries no quantity and is not
   permitted one.

9. **Palette assignment.** As slide 08. Gold appears only in the Polaris.

10. **Type spec.** Headline Fraunces 82 px wght 600, fitted `maxLines: 2`. Ask
    Space Grotesk 500 at 36 px, leading 1.34, max width 700 px, centred.

11. **Anchor spec.** The anchor and the bed, held. The Polaris is the brand mark
    and is the only furniture besides the counter and the watermark.

### D. VERIFICATION

12. **Reference intent.** The last frame of the dive, looking at the one made
    thing that stays.

13. **Risk flags.** A held frame risks reading as a duplicate of 08, mitigated by
    the stripped population, the resolved Polaris and the terminated riser. A
    centred title card in a deck of asymmetric frames could read as a different
    deck, mitigated by holding the identical window and bed.

14. **Acceptance checklist.**
    - [ ] The window and the bed are identical to slide 08
    - [ ] The mote population is visibly thinner than slide 08's
    - [ ] The riser terminates ON the anchor shackle and does not leave the frame
    - [ ] Exactly one ask appears and nothing else is asked
    - [ ] The string `sources in comments` appears nowhere
    - [ ] `alaskaaihq.com` is present, small, mono and low contrast

---

# BUILD RECONCILIATION

Nine frames built, rendered and gated. `qa.py` reports 0 fails and 0 warns on all
nine. Where the build left the plan it is named here, per slide, with the measured
reason, because the plan is a plan and the render is the artifact.

| slide | what diverged | why |
|---|---|---|
| 01 | Nothing. Built as planned. | |
| 02 | Headline sets in THREE lines, not the planned two. Kicker is the dossier's 41 character string, set on two mono lines. | "Sound is how the machine" is 24 characters and needs about 46 px to fit a 480 px column, which is under the display floor this deck set. Three lines at 62 px is the legible reading. |
| 02 | The three range arcs end in a radial falloff centred on the fix rather than at a rect clip, and are composited source over rather than screen. | A rect clip leaves a vertical edge in open water that reads as a mistake, and `#FFC72C` screened onto teal water composites to olive and stops being the deck colour. |
| 02 | The interference field takes each source's own crest rather than the sum of three. | The summed field lights only where all three crests agree, which is a scatter of isolated spots and reads as bokeh rather than as geometry. |
| 02 | A depth rail was added with two numerals, 50 m and 100 m, and the ice arris is declared as a mark on that axis. | Section 11 names the rail as furniture and the first build omitted it. The axis census then found the ice arris crossing the rail band and was right to: on a depth axis the top of the lid is a quantity. |
| 03 | Headline is `30 seconds, / every four hours, / all year.` rather than the planned `Up to six moorings, / two drifting buoys.` Body is 42 words rather than 48. Two labels reset on two lines. | The copy room's measured call: both planned headline lines ran 19 characters against a 17 character budget, and the up to six hedge survives intact in the body. |
| 03 | Ticks are 100, 200, 300 and 400 m. The planned 50 m tick is gone. | Its numeral lands in the counter's lane at the top of the frame, and a mark clamped away from its own tick is worse than no mark. |
| 03 | The rail band carries a washed lane. | Proto finding 4's own remedy. The census measures declared marks against the band's texture and the ray field was that texture. |
| 04 | 1,000 m lands at y 1040 rather than at the frame's bottom edge, so the mapping's nominal window ends 310 px above the frame. (This row said 1180 until ROUND 3; 1180 was the first build's answer and a pixel critic measured the glider as parked on the trim at that value.) | The acceptance test is that the glider sits exactly on the 1,000 m tick, and a mapping that puts 1,000 m at y 1350 puts the deck's one aurora object half off the bottom. That is the prototype's third finding verbatim. |
| 04 | The mote population is drawn in the slide rather than through `AKICE.marine`, with a size floor, and the count is 6,392 rather than 3,000. | `marine`'s radius falls to 0.55 px by the bottom of a window, which is right where motes are atmosphere and wrong on the one frame where they ARE the subject. 6,392 is 639,237 square kilometres at one mote per 100, so the count stays a datum. Measured: at 3,000 the centre of the frame read as bare gradient. |
| 04 | The single gold arc is at alpha 0.30, not the planned 0.18. | At 0.18 over water this dark it composites to an olive smudge. |
| 04 | `data-breather` is not set, as the dossier intended. | `dossier_check` warns that qa.py will fail frame balance without it. qa.py then measured the frame and passed. The warn is a stale prediction and the attribute stays off. |
| 05 | The four zone labels stand in a left hand column at x 80, each with a leader that leaves by the side its own target is beyond, or vertically at the target's own x when the target is inside the label's span. | **THIS ROW WAS WRONG UNTIL ROUND 3 AND THAT IS HOW THE RUN'S ONE HARD FAIL SURVIVED SIX REVIEW ROOMS.** It claimed the labels stood at their own rim angles, which was an arrangement tried and abandoned, and nobody re-read the artifact against the row. What shipped at x 120 put the widest label's right edge 9 px from the prose column, which reads at 432 px as one run-on string, DEPLOYMENT AND RECOVERYThe 55 metre zone applies. A reconciliation table that misdescribes the render is worse than no table, because every reader downstream trusts it. |
| 05 | The four circles are knocked out of the reserve boxes on their own surface. | A circle takes no basin and at 411 px the largest runs through the right hand column. |
| 06 | Tick alphas are 0.92 and 0.52, not the planned 0.62 and 0.30. | Measured: at 0.30 a 0.75 px tick on `#03090C` water does not exist, and the deck's strongest single image came back as a faint gold patch on bare black. The argument is a ratio of counts and it is carried by how much of the field is lit. |
| 06 | Ticks are 1.5 px tall and the field is drawn on the slide canvas rather than the offscreen. | `AKENGRAVE.drawOffscreen` returns a 1x surface, where a 0.75 px mark resolves to a grey smear. |
| 07 | The uncertainty mark is a RING whose RADIUS is the coefficient of variation, not an arc whose angular half width is the CV times the value. | The frame prints `RING RADIUS IS A COEFFICIENT OF VARIATION, NOT A DISTANCE`, and a frame may not carry a disclosure describing a mark it did not draw. The planned instrument is also the one that makes the 1992 figure the wider of the two and contradicts this frame's own acceptance test. |
| 07 | The 2,000 m tick carries no DOM numeral. | Every clear lane on this frame is taken by three dials or by the type column, and slide 06 immediately before labels 2,000 m explicitly. The mark is declared in `data-scale`. |
| 08 | Kicker is `THE NINTH YEAR, ONE AT A TIME`, not `NINE YEARS, ONE YEAR AT A TIME`. | `aggregate_check` refused NINE YEARS and was right: C06 says the ninth year and does not print the number nine. |
| 08 | Pool rx 138 at peak 0.28 with the cast at w 76 and wide 1.10, not pool rx 96 with cast w 88 at the default wide 2.0. | The planned pair measured dL 0.0 at 432 wide, because a cast at wide 2.0 spans 176 px and darkens every pixel the pool lifted. The shipped pair measures dL 12.4 and the rects are `contact_probe`'s own. |
| 08 | The anchor is a low wide clump, 158 by 52, with a padeye, and its face carries a value ladder. | At 132 by 80 with a U shackle and a flat fill inside a bright outline it read as a handbag at feed size. |
| 09 | The riser is drawn AFTER the bed. | Drawn before it, the bed buried its last 160 px and the termination the acceptance test asks for was invisible. |
| 09 | The wordmark stays Space Grotesk rather than becoming Fraunces. | A fixture that changes face on the last frame of nine reads as an error rather than as a title card. |
| 09 | No provenance or source note, and none in `copy.json` either. | The owner's 2026-09-11 change forbids one on this frame. The copy room supplied one and the render was right to omit it. |

The claims index above was reconciled to the build in the same pass: six rows
moved and three claims left the deck, every one of them because the caption
room's final copy is shorter and more careful than the dossiers' drafts. What
moved and why is written out under that table.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-09-12. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[PASS] qa.py          PASS, 0 fails, 0 warns
[WARN] dossier_check  WARN, 9 dossiers, 0 fails, 1 warns
[PASS] reconciled     BUILD RECONCILIATION present, 24 table row(s), 7216 chars
[PASS] caption_check  PASS, 825 chars, hook 109, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 70 authored slide strings all present in the render
[PASS] aggregate      aggregate_check: PASS -- 17 aggregate assertion(s) detected, 17 declared -> out/2026-09-12/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 32 claims indexed, 0 declared counts checked, 0 body quote(s) checked, 0 drift(s)
[PASS] bespoke        bespoke_check: PASS -- 9 slides, median pairwise art similarity 0.125 (fail at 0.60), max pair 0.452, drawn share 65% (58 drawn vs 31 blocky
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] docket_dates   docket dates clean at 2026-09-12: 317 assertions over 6 fixtures and 25 ledger items
[WARN] gas_watch      37 day(s) on record, 1 missing from the series, first 2026-09-08
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-09-12 (184 generated files)
[PASS] assemble       9 slides, pdf vector 8.48 MB, 9 thumbs, sources verified
[PASS] score          8.72 / 10 vs threshold 8.3, scorer says passes=True
[PASS] ship_gate      scored 8.72 against a threshold of 8.30
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```


## ROUND 2, AFTER SIX REVIEW ROOMS

Five pixel critics and a flow critic returned per slide scores of 4.5, 4.5, 6.0,
4.5, 5.5, 5.0, 5.5, 5.5 and 6.5 against a threshold of 8.3, with the sequence at
6.6. Below is what was fixed, in the order of leverage. Everything in it is
measured, and the three findings that were WRONG are named as wrong rather than
quietly dropped.

### FOUR CHASSIS DEFECTS, each reported by more than one room

1. **`AKICE.rays` defaulted to GOLD.** Three frames called it without an rgb and
   shipped a warm fan across two of them, which is a colour law breach on a deck
   whose law reserves `#FFC72C` for what the record knows. The default is now the
   ice family. This one finding was worth more than any per frame fix.
2. **A rail tick read as an em dash.** At the numeral's own weight, at its cap
   middle, eight pixels after its last glyph, an 18 px tick IS an em dash, and
   four rooms read the rail as `50 m --`. Two attempted fixes failed first and
   both failures were instructive: dimming the tick made every declared mark
   weaker than the band's own texture, and dropping it 8 px MOVED THE MARK, which
   the axis census reported exactly. The tick now draws outward from a brighter
   spine at its true depth.
3. **`AKFIT.plate` painted hard edged rectangles.** Five rooms used almost the
   same sentence, and it is verbatim the defect this run had already banned in the
   art layer. A flat background colour IS that defect. Plain fills are now
   feathered into a radial falloff.
4. **A sub pixel mote is not a mote.** `AKICE.marine`'s radius falls to 0.55 px by
   the bottom of a window, and three rooms reported populations that read as grain
   or as JPEG noise. `rFloor` and `aFloor` exist now and the defaults are
   unchanged, so nothing that was right moved.

### WHAT EACH FRAME OWED

- **01.** The hook set in four lines with two word orphans against a two line
  acceptance test; it is two lines. The phantom rim was drawn BEFORE the bezel
  profile, which re-stroked the same circle and painted the dashes out. The riser
  drifted off the right edge at y 848 instead of joining slide 02 at 980.
- **02.** The kicker repeated five of the headline's eight words directly above
  it. The body was nine ragged left lines. The glider drew a pale X beside the
  gold dot, so the frame showed two candidate fixes on the frame whose subject is
  that a position resolves to one, and its antenna was a phantom dash on an
  object whose depth the notice states, which breaks D6's single meaning on the
  second frame of nine. The riser dead ended behind the body column.
- **03.** The gold source ticks DID NOT DRAW AT ALL: a 0.75 degree arc at r 46 is
  six tenths of a pixel and a degenerate subpath gets no cap, so the frame shipped
  with zero gold pixels and the state table had a hole in it. They are ticks now,
  marks at a position rather than lengths, and the duty cycle is printed here and
  drawn as a ratio of counts on 06 where that argument belongs. The buoy label sat
  above the kicker and read as the frame's opening line.
- **04.** A third of the frame carried a fill and a scatter, and both declared
  mitigations had failed: the aurora object was three percent of the frame parked
  on the bottom trim and the population had no gradient. 1,000 m now lands at
  y 1040, the population carries a size and alpha ramp, and the arc is a real
  gold across the upper third with both ends dissolving.
- **05.** The 55 m dimension ran through the gold cross at the common centre. The
  circle group sat 264 px high of its declared centre. The rail's numerals landed
  inside the prose and, clamped, made 05 show 1,500 m at its top where 06 shows
  1,000 m, so swiping between them read as five hundred metres of ASCENT: this
  frame keeps the spine and the four declared ticks and gives up its numerals,
  which also removes the metre confusion its own risk flag names.
- **06.** The label naming the gold band was BASINING THE BAND AWAY, so the
  attended run began 62 px right of the field's own edge and read as a detached
  swatch. The unattended ticks could not survive a five times downsample, which
  left the lit band with nothing to be a fraction of. Three leaders climbed across
  the body's last four lines.
- **07.** The wordless claim measured 0.1 dE, which is the pixel critic's
  sentence in a number. The needle is 5 px now with a 9.5 px cap and the socket is
  a 15 px hole with a lit lip; the claim measures 115.6 dE. The bezel's lee at
  rgba(4,12,16,0.88) on `#03090C` water was invisible BY CONSTRUCTION, so the
  lower arcs get a casing one step lighter than the water. The CV rings escaped
  their own cases. Both leaders crossed their own dial's face numeral.
- **08.** The bed arrived as a 21 percent sliver after eight frames of descending
  toward it, and the contact read as a glow because the pool was concentric with
  the cast. The pool now sits opposite the lee, the seam runs the whole base line,
  the anchor is 254 by 92, and the gold cross moved to the Polaris coordinates so
  the close's star blooms out of it in situ rather than 600 px away.
- **09.** The headline stranded the word `number.` on a centred line, on the close
  of a deck about a missing number.

### THREE FINDINGS REFUSED, and why

- **"Move slide 01's dial to the planned lower left."** The render is the artifact
  and the plan is the plan. The dial reads where it is, the frame's mass is
  balanced headline left against instrument right, and the fix that mattered was
  the phantom rim, not the position. The 11a rects were re measured off the render
  instead, which is what 11a actually requires.
- **"Reset slide 04's window to 380 to 860 so the glider is not on the trim."**
  That breaks the frame's own acceptance test, which is that the glider sits
  exactly on the 1,000 m tick, because C27 puts its transit floor there. The
  mapping's bottom moved instead.
- **"Slide 07's uncertainty should be CV times the value."** That is a different
  instrument and a defensible one, and it contradicts both the line this frame
  prints and its own acceptance test. A frame may not carry a disclosure that
  describes a mark it did not draw.


## THE COLOUR LAW, AUDITED BY COUNTING PIXELS (round 3)

The gate this run recommends building does not exist yet, so the audit was done
by hand, on the shipped renders, and it is recorded here because an audit nobody
can reproduce is not one.

| frame | gold px | undetermined px |
|---|---|---|
| 01 | 228 | 49,227 |
| 02 | 19,735 | 30,993 |
| 03 | 1,563 | 30,342 |
| 04 | 2,660 | 28,712 |
| 05 | 368 | 36,138 |
| 06 | 11,330 | 78,961 |
| 07 | 2,268 | 65,482 |
| 08 | 557 | 42,842 |
| 09 | 5,545 | 8,314 |

Both law bearing inks are present on all nine frames, which is what the state
table promises and what the first build did not deliver, since slide 03 shipped
with ZERO gold pixels on it. The budget varies the way the table says it should, with
the two structural golds on 02 and 06 and a single mark on 01, 05 and 08.

One claim in the table was wrong and the count is how it was caught. Frame 06 was
described as the deck's peak gold and it carries 11,330 pixels against 02's
19,735, and it should, because 132 attended ticks out of 2,190 is a small share BY
CONSTRUCTION and that share is the argument. What 06 peaks in is intensity, not
area, and the table now says so.
