# STORYBOARD — Carousel No. 62 — 2026-09-18
# THE RETURNED APRON

## DECK HEADER

### Thesis

A global sports body came to Alaska for the one thing Alaska has too much of,
distance, and then flew a circle with it. The circle is honest, because a circle
is how you test cargo and a line is how you deliver care. What has been
published is the flight. The finding is not published and has no date.

**PDF document title.** `Out of Nenana and Back, With the Finding Pending` (46 characters)

### Arc

| # | Beat | Temperature |
|---|---|---|
| 01 | HOOK. A thousand kilometres, and the wheels stopped where they started. | still, arresting |
| 02 | PAYOFF. The track leaves the frame and comes back into its own impression. | matter of fact |
| 03 | THE PAIR. Every volunteer gave two samples. One flew. One stayed. | careful, human |
| 04 | THE AIRCRAFT. Thirty one feet of span for a box that fits in two hands. | technical, admiring |
| 05 | THE TURN. A circle tests the cargo. A line delivers the care. | cool, exact, the hinge |
| 06 | BREATHER. The distance was the point, and Alaska had the distance. | wide, quiet |
| 07 | THE HANGAR. The laboratory was in a building at the same airport. | procedural |
| 08 | THE RECORD, AS PUBLISHED. Filled rows, empty rows, and a tape that stops. | forensic, keepable |
| 09 | CLOSE. Alaska supplied the distance. One question. | level, handed over |

The emotional shift happens at 05, and it is a concession before it is a
position. Slides 01 to 04 build a reader's suspicion that a thousand kilometres
ending where it started is a shortfall. Slide 05 takes that suspicion away and
replaces it with a better one. You close a route precisely so the route stops
being a variable and the blood is the only thing that changed, which is good
science, and which means the distance Alaska supplied was the part deliberately
held still. The variable nobody varied is the one a village clinic needs varied.

### Slide count rationale

NINE. The band is 6 to 12 and the default is 8 to 10. The winning treatment
pitched TEN and named its own slide 05, a closed loop displayed on a screen, as
the frame it would cut first, because a screen showing a closed loop is one bad
render away from being the plan-view map of Alaska the variety ledger forbids,
on the deck's most-looked-at content frame. Cutting it removes the treatment's
top risk, lands on the doctrine default, holds the render budget to one GPU
frame, and saves a build round under the five round cap. The route honesty
fixture it carried moves to slide 02, which is the frame that makes a claim
about shape and therefore the frame that owes the disclosure.

### Continuity system

**DEVICE A. THE PANORAMA SPINE.** One master apron 9 x 1080 = 9,720 px wide,
sliced into nine windows, camera x += 1080 per slide. Height, lens and light
never change. The treeline horizon is a pure function of global x and so are the
haze band, the sky ramp and the gravel height field's seed, so adjacent frames
seam exactly:

```
gx        = slideIndex * 1080 + localX
yHorizon(gx) = 506 + 14 * sin(2*PI*(gx - 1400) / 5200) + 6 * sin(2*PI*gx / 1730)
yApron(gx)   = 940 + 9 * sin(2*PI*(gx - 300) / 6100)
```

Declared ONCE, in a shared header block every slide copies verbatim. No slide
authors its own horizon. Only art crosses the cuts and all primary text sits at
least 80 px inside its own column.

**DEVICE B. THE TYRE TRACK.** One track in the shoulder gravel, present on all
nine frames, whose every state change is a SHAPE change and never a brightness
change. It is the deck's thesis stated physically. On slide 02 it leaves the
right edge and comes back INTO ITS OWN IMPRESSION, the second pass offset 40 px
and crushing the first, which is a closed loop drawn without a diagram.

**DEVICE C. EDGE-TEASE.** Every frame's right edge is cut by the track or by the
day's one shadow vector. Slide 09 is the only frame that runs its track OUT of
the bottom-left corner toward the reader rather than off the right edge.

**DEVICE D. THE PHANTOM ARC.** The cool slate `#9FB3C4` is ENTIRELY ABSENT from
frames 01 to 07, appears on 08 as the card's empty half and the tape's
continuation, and is the last mark on 09. The deck gets cooler exactly where the
record runs out.

#### Full motif state table

| # | Tyre track state (SHAPE) | Phantom ink | Gold marks, and the claim each names | Archivo wdth |
|---|---|---|---|---|
| 01 | OUTBOUND. Enters bottom right, cut by the right edge, sharp | none | chock pair (C03) | 118 |
| 02 | CLOSED. Runs left, returns into its own impression, second pass offset 40 px | none | chock pair re-set (C03), `1,000 KM` figure (C01) | 113 |
| 03 | OCCLUDED. Passes behind the folding table's legs | none | seal on the flown box (C16) | 107 |
| 04 | SOURCED. Runs under the mainwheels, same width as the tyre | none | `31 FT` dimension call (C11) | 101 |
| 05 | THE TWO GEOMETRIES. The track's closed return at left, and a straight wheel rut leaving frame right | none | closure tick (C03) | 95 |
| 06 | ALONE. The only mark in the frame, full width, both ends cut | none | sun disc rim hairline (C02) | 89 |
| 07 | PASSED. Crosses the door's light spill on the apron | none | XN-Series indicator, one 6 px square (C19) | 84 |
| 08 | COVERED BY PAPER. The card lies across it, half hiding it | five empty channel rows, and the tape's continuation | `8 H 47 MIN` cell (C04), two date nodes (C02, C06) | 79 |
| 09 | OPEN TOWARD THE READER. Runs to the bottom left corner and out of frame | one dashed arc, unclosed | Polaris in the last chock (C03) | 74 |

### Variety ledger check, and the required divergence

Last four decks: No.58 a bronze monument disc on a green concrete pad; No.59 a
cargo hold with one repeated unit crate; No.60 nine nadir plan views on one
conic equal area mapping of Alaska; No.61 a Wyoming-pattern snow fence as a
continuous receding line.

**THE DIVERGENCE IS THE LIGHT AND THE CAMERA, AND BOTH ARE TOTAL.** Two of the
last three atmospheres were night and the third was twilight. This is DAYLIGHT,
outdoors, at 24 degrees of sun elevation, and the flight really did happen in
daylight on August 19th, so the divergence is handed over by the story rather
than chosen for novelty.

Three of the last four decks were AN OBJECT UNDER ONE HARD KEY WITH A POOL OF
LIGHT AT ITS FOOT. Four specific breaks. There is no key, there is a sun at 24
degrees with the whole sky dome as fill at 3.5 to 1, and nothing falls off to
black. There is no pool, the ground is lit edge to edge across all 9,720 px and
shadows are long directional casts that LEAVE the frame rather than ellipses
that close under a foot. The camera is INSIDE the scene, kneeling on the
shoulder at 620 mm with out-of-focus gravel in the near field, where the last
four decks put the reader outside looking at a specimen on a stage. And the
objects are annotations of the ground rather than subjects on it.

Against No.61 specifically, which is the closest and is conceded rather than
argued away. That fence receded INTO the frame along a vanishing line and was
one object repeated. This pans LATERALLY at constant depth and the repeated
element is a SURFACE, not an object. That deck's mass was vertical structure
against sky; this deck's mass is horizontal ground at 62.5 percent of every
frame.

There is NO MAP in this deck. No projection, no coastline, no borough, no
geodata file loaded. The literal geographic anchor is Nenana Municipal Airport,
named in copy and carried as a decorative coordinate fixture.

Hook archetype is NEW: THE COMPLETED CONTRADICTION, a fact that has to be
resolved rather than a tease. It is none of the three forbidden archetypes. It
is not two labelled sums, it is not a centre and its remainder, and it never
addresses the reader in the second person.

### Variance dials

DESIGN_VARIANCE 4, VISUAL_DENSITY 3, TYPE_TEMPERATURE 2.

Justification. Variance 4 because the standing weakness is artwork craft and a
cautious deck has never once fixed it, and because a daylight exterior with a
kneeling camera is a genuinely new register for this lineage. It is not a 5,
which would be a light deck, and the one-light-deck allowance is not being
spent here. Density 3 because the last two decks ran at 4 and this deck's
argument needs the ground to be LOOKED at rather than inventoried. Temperature
2 because Instrument Serif appears on only four frames and everything else is a
cool wide grotesk.

### THE STANDING WEAKNESS THIS DECK ATTACKS, and how it is measured

`scripts/trend_check.py --window 10` names artwork craft and genuine detail as
the weakest criterion in 6 of the last 10 runs at a mean of 6.8, and lists four
recurring machine defects that are one defect wearing four names. Art touching
glyphs, canvas mark near reserved text, busy art under text, and top-loaded
composition.

**THIS DECK ANSWERS IT BY CONSTRUCTION, AND THE METHOD WAS PROVEN ON A PROBE
BEFORE ANY SLIDE WAS WRITTEN.**

1. **Type and art occupy DIFFERENT REGIONS on six of nine frames.** All display
   type on slides 01, 02, 03, 06 and 09 sits on the sky band, which is a graded
   atmosphere the apron never reaches. The art is on the ground.
2. **On the three frames where copy drops onto the apron (04, 05, 07) the
   reserve is PUNCHED, not plated.** Field drawn to an `AKENGRAVE.drawOffscreen`
   buffer, `AKENGRAVE.punchReserves` against `boxesFor('[data-reserve]')` with
   BLURRED RECTANGLES at blur 9 to 11, then composited. A probe run this morning
   carried a 112 px headline over live art with zero art-touching-glyphs and
   zero busy-art warnings, where the house's own demo deck carries both.
3. **Slide 04's GPU frame is composited into 2D BEFORE the punch.** A probe
   proved that a GL canvas with type over it FAILS four ways, because
   `punchReserves` cannot reach a GL canvas in the DOM, and that rendering GL
   offscreen, drawing it into the buffer, punching THAT and compositing returns
   zero fails on the identical scene.
4. **The bottom band is 100 percent modeled lit ground on all nine frames.**
   `qa.py frame_balance` fails under 0.60 and warns under 0.80 of the frame's
   own craft density. Predicted 1.15 to 1.35 here. Target every frame at or
   above 0.95 with nothing below 0.90, CHECKED ON THE FIRST RENDER of every
   slide, before any critic is spawned.

**SECOND TARGET, riding the same decisions.** Legibility and platform fitness,
the weakest criterion twice in ten runs and worked on by NO upgrade ever. No
rendered string in this deck is below 26 px except three declared decorative
fixtures. Every display headline is fitted with `AK.fitText` inside
`renderReady` after `await document.fonts.ready`, so no headline can soft wrap
into the block below it. Set at planning time, not discovered at scoring.

### Light, declared once and carried on every frame

- Sun azimuth **208 degrees**, elevation **24 degrees**, key to fill **3.5 : 1**.
- Fill is the whole sky dome at `#5A6A78`, not a bounce card, so nothing falls
  off to black.
- Screen shadow vector is down and to the right at **28 degrees below
  horizontal** on every frame. Nine frames of casts leaning toward the swipe.
- Cast length is **2.25 times object height**, since tan(24) = 0.445.
- Shadow ink is a darkened background hue, cool slate `#5A6A78` at 22 percent of
  key value. Never black.
- The sun disc is visible on frames 01 and 06 only, a dim ochre disc, no flare
  and no rays. **The sun is never gold.** Gold means the record, and a gold sun
  would quietly destroy the law.

**Why elevation 24 is a craft decision and not a mood.** The engraving bench
needs a raking key between 20 and 30 for the swelled line to be legible, and
above that every stroke flattens to one width and the intaglio gives back a
uniform hatch. 24 also gives 2.25x shadows, which is what makes gravel read as
gravel and the apron read as flat.

**The light never moves, and the constancy is also an argument.** The light did
not move. The aircraft did.

### Palette + type system

**Palette family: INTERIOR AUGUST, LOW SUN AND HAZE.** Built as OKLCH ramps with
`AKC.ramp`, gamut mapped by chroma reduction, IGN dithered on the sky.

| Hex | Role |
|---|---|
| `#1A1712` | deepest ground shadow, warm near black. The deck's floor value |
| `#2A241B` | gravel shadow side, base register |
| `#4A3D2C` | mid gravel body |
| `#7A6A4F` | lit gravel crown |
| `#A8946F` | gravel specular glint, highest surface value |
| `#3A3B33` | spruce treeline, far plane, desaturated |
| `#6E6252` | haze band at the horizon |
| `#443C31` to `#9A8460` | sky ramp, zenith to horizon glow |
| `#5A6A78` | sky bounce fill on every shadow side. The only cool thing in the warm world |
| `#F4F8FF` | type primary, snow |
| `#C9C2B4` | type secondary, warm bone |
| `#6B6355` | mono fixture grey, watermark and counter, low contrast by design |
| `#9FB3C4` | **THE PHANTOM REGISTER.** Always dashed `30 5 6 5 6 5` at 1.25 px, always unfilled, never touched by the sun |
| `#FFC72C` | **GOLD. THE RECORD.** |

**THE GOLD LAW, one meaning deck-wide, and it is a gate rather than a taste.**

Gold marks WHAT THE RECORD CARRIES, and the record is small. One to three marks
a frame, never more than about 1.2 percent of frame area, and **every gold mark
traces to a claim id that is printed on that same frame and declared in
`data-ink`.** If a mark can't name its claim, it isn't gold.

**Gold is only ever applied to a SEALED form.** Filled, capped, bolted,
terminated at both ends. **The phantom is only ever an OPEN form.** Unfilled,
lidless, dashed, and where it is a bar it has no terminator on one end. The
distinction is carried by SHAPE and not by value, because a brightness-only
state change reads as a static logo at 432 px and a silhouette does not.

**Type.** Archivo (display) / Instrument Serif (the human voice) / JetBrains
Mono (telemetry). Neither forbidden pairing is touched.

THE BINARY SIZE RULE, and the empty band:

| Band | Family | Use |
|---|---|---|
| **88 px and above** | Archivo only | headlines and the wordmark. Nothing else lives here |
| **34 to 62 px** | Instrument Serif only | body, pull quotes. No Archivo may enter |
| **26 to 30 px** | JetBrains Mono only | labels, dimension calls, card rows, counter, attributions |
| **19 px** | JetBrains Mono, declared decorative | the site watermark and the coordinates fixture only |

**NOTHING RENDERS BETWEEN 63 PX AND 87 PX, DECK-WIDE.** That 25 px gap is the
rule that makes the registers unmistakable. Reinforced by two absolutes.
**Archivo is never set in caps anywhere in this deck, and JetBrains Mono is
never set in lowercase anywhere.** So the two faces can never be mistaken for
two similar sans sharing a register, which is the type crime this rule exists
to stop, and the reader learns without being told that caps means instrument
and sentence case means a person talking.

`wdth` runs **118 down to 74** across the nine frames, a decrescendo. The cover
is widest because the claim is a thousand kilometres. The close is narrowest
because the argument has come down to one unanswered question. `wght` holds at
600 throughout so the width change is unambiguous. Display leading 0.98,
tracking -2 percent. Instrument Serif at 1.38 leading, tracking 0. Mono tracked
+10 percent.

### Claims index

Regenerated from `copy.json` AFTER the build, because `plan_drift_check` found
nine drifts between the planned index and what the frames actually print. The
build is the artifact and the plan was the stale one, so the index was
corrected rather than the deck.

| Claim | Slides |
|---|---|
| C01 1,000 km | 01, 02, 08 |
| C02 August 19th | 01, 08 |
| C03 Nenana Municipal Airport | 01, 02, 05, 07, 08 |
| C04 8 hours and 47 minutes | 02, 08 |
| C05 several hours | 02 |
| C06 28 days | 08 |
| C09 ACUASI is part of the University of Alaska Fairbanks and provided flight plann | 02, 09 |
| C11 31-foot wingspan | 04 |
| C13 two groups | 03 |
| C14 two samples | 03 |
| C15 chilled | 03 |
| C16 Neil Robinson of the ITA said samples are in sealed boxes and loaded in the dr | 04 |
| C18 five channels | 08 |
| C19 XN-Series | 07, 08 |
| C20 After the flight both groups of samples were analysed in the same on site labo | 07 |
| C21 Dr. Sven Voss | 07 |
| C23 The results of the scientific analysis will be communicated once the evaluatio | 08, 09 |
| C24 The ITA intends to submit the findings for publication in a peer reviewed scie | 08 |
| C26 approximately 20 kilometres | 05 |
| C27 Post flight analysis of the earlier Doha study indicated that relevant blood b | 05 |
| C29 Cathy Cahill described nurses going into a community, taking samples, sending | 09 |
| C31 Neil Robinson said the interest is to use sport as a model to ship samples, an | 06 |
| C34 Sysmex enabled the long distance test flight through a financial contribution | 07 |
| C35 Staff from the Interior Region EMS Council collected samples from volunteers t | 03 |
| C36 one of nine | 04 |

NOT USED, and deliberately: C07, C08, C10, C12, C17, C22, C25, C28, C30, C32, C33, C37, C38, C39, C40, C41. C12 in particular is not
used ANYWHERE. The range comparison, about 600 miles published against about
621 flown, is either a real fact or a rounding artefact and no source explains
it, so this deck prints neither figure and draws neither. That decision is
written here so a later round does not rediscover the discrepancy and print it.

### What this deck refuses to draw

- **THE ROUTE.** No source published a track. The deck knows the LENGTH and that
  it closed on its own start. Slide 02 carries the disclosure in 26 px mono ON
  THE FRAME, not in the dossier only.
- **ANY SENSOR VALUE.** Five channels were logged and not one number is public.
  No trace, no wiggle, no needle, no bar, anywhere in the deck. Slide 08 gives
  the five channels as NAMED EMPTY ROWS and the emptiness is the drawing.
- **A RESULT.** No source has published one. Nothing in this deck states or
  implies survival or damage, and the words intact, degraded, safe and unharmed
  appear nowhere.
- **THE RANGE COMPARISON.** See the claims index.
- **A GOLD SUN.** See the light section.

---

## SLIDE 01 — THE COVER, OUTBOUND

**1. Beat.** HOOK. State the completed contradiction and let the reader feel it
resolve into a question. No loop inherited. Plants the loop that only slide 02
closes, which is why a thousand kilometres ended at its own start.

**2. Copy, final.**
- kicker, mono 26 px, `NENANA MUNICIPAL AIRPORT, AUGUST 19TH` (37 ch, C02, C03)
- headline, Archivo 140 px, two lines broken at the comma,
  `1,000 kilometres out of Nenana,` / `back to the same airport.` (56 ch, 9 words, C01, C03)
- counter, mono 22 px, `01 / 09` (fixed furniture)
- watermark, mono 19 px, `alaskaaihq.com` (fixed furniture)
- coordinates, mono 19 px, `64 33 N 149 04 W` (decorative fixture, Nenana, read from the committed gazetteer or dropped)

**3. Reader takeaway.** Blood flew a thousand kilometres out of an Interior
airstrip and came back to the same one.

**4. Layout map.** Twelfths. Kicker at col 1 to 6, row 1. Headline at col 1 to
10, rows 2 to 3, optical-left at x 80 with the stem of the numeral 1 pulled 6 px
left so the glyph edge aligns rather than the sidebearing. Focal point is the
chock pair at the rule-of-thirds intersection near 720, 900. Eye path is
headline, then the gold chocks, then the track leaving the right edge. Quiet
zone is the sky band between the headline and the treeline, about 18 percent of
the frame, well inside the quarter ceiling. One permitted grid violation, the
track breaks the right margin, which is the swipe cue.

**4a. Lower-third treatment.** The bottom band is the gravel shoulder in tack
sharp focus, an akhachure slope and aspect field whose stroke widths are the
local slope of a seeded height field and whose rotations are its aspect, so the
texture cannot be uniform unless the ground is. Over it lies the long cast of
the chock pair, running down and right at 28 degrees, 2.25 times the chock
height, in the darkened sky hue rather than black. A blurred repoussoir clod
sits in the bottom 90 px and bleeds off the frame, which puts a genuinely
out-of-focus foreground plane in front of the reader and makes the sharp middle
distance read as depth rather than as flatness. The mass, the modelled relief
and the deck's brightest specular crowns are all in this band.

**5. Depth plan.** Background sky ramp, then haze band, then treeline
silhouette, then apron asphalt, then gravel shoulder, then the repoussoir clod,
then type. Six depth cues, atmospheric perspective on the treeline lerped toward
haze, occlusion where the chocks overlap their own cast, a scale gradient in the
gravel population, depth of field with the shoulder tack sharp and both the
treeline and the clod blurred, the haze term itself, and one key light with all
casts sharing one direction. Focal plane is the gravel shoulder at y 1050.

**6. Continuity device state.** Track OUTBOUND, entering bottom right and cut by
the right edge, single pass, sharp. Phantom ink absent. Gold is the chock pair
only. Archivo wdth 118, the widest the deck ever goes.

**7. Technique stack.** akhachure slope and aspect field over the shoulder, seed
20260918, grid 9 px, stroke width from slope at 0.6 to 2.4 px, rotation from
aspect, four accumulation passes at 0.22 alpha with the sun angle varied 3
degrees each pass. Multiplane parallax for the three planes at scale 0.72^i and
atmosphere lerp (i/n)^1.4. Gradient solids for the chock forms. Grain tile 280
px at strength 50, seed 21, as a repeating CSS background at 0.08 overlay.
AKPOST.grade on the art canvas last.

**8. Data-in-art mapping.** The shoulder carries 527 lit specular crowns in this
1080 px column, one per minute aloft (C04), declared in `window.__akAssert` with
`points` and `dispersed: true` because the marks stand for how much and
deliberately not for where. The chock pair is two objects because the flight had
two ends at one place (C03).

**9. Palette assignment.** Sky ramp `#443C31` to `#9A8460`, haze `#6E6252`,
treeline `#3A3B33`, apron `#2A241B` to `#4A3D2C`, shoulder `#4A3D2C` to
`#7A6A4F` with crowns at `#A8946F`, cast shadow `#5A6A78` at 22 percent,
headline `#F4F8FF` on the sky's darkest zenith zone, measured target 8 to 1,
earned by composition with no scrim. Gold `#FFC72C` on the chock pair only,
about 0.4 percent of frame area.

**10. Type spec.** Headline Archivo 140 px, wdth 118, wght 600, leading 0.98,
tracking -2 percent, sentence case, colour `#F4F8FF`, max width 920 px, fitted
with `AK.fitText(el, {min: 104, max: 148, maxLines: 2})` and an authored `<br>`
after the comma. Kicker JetBrains Mono 26 px, 500, tracking +10 percent, caps,
`#C9C2B4`. Counter and watermark mono 22 and 19 px, `#6B6355`, both
`data-decorative`.

**11. Anchor spec.** The literal anchor is the wheel chock pair, a rubber wedge
form built from gradient solids with a chamfered top face, a moulded rib
pattern, and a rope eye. Positioned at 690 to 790 x, base at y 1044. The one
annotation is the mono coordinate readout. No leader lines on this frame.

**11a. Wordless claim.** None on this frame, because the cover's argument is
carried by the sentence and the art's job here is to be a place rather than a
proof. Written rather than omitted so a critic does not look for one.

**12. Reference intent.** A working airstrip photographed at eye level by
someone kneeling, in the register of a field report rather than an aviation
brochure. Nothing heroic about the machine, everything specific about the
ground.

**13. Risk flags.** The headline is the deck's largest type over the sky, and if
the sky ramp's zenith is not dark enough at the top left the contrast fails.
Mitigation, the ramp's darkest stop is pinned at `#443C31` and the headline sits
entirely above y 420 where the ramp has not yet lightened. Second risk, the
gravel crowns could read as noise rather than as modelled relief. Mitigation,
the hachure strokes carry real slope and aspect so the field has structure, and
the count assertion is verified against the composited png rather than the loop.

**14. Acceptance checklist.**
- [ ] The headline reads in exactly two lines with the break after the comma
- [ ] `1,000 kilometres` is legible at 432 px thumb width
- [ ] Gold appears ONLY on the chock pair, nowhere else in the frame
- [ ] The cast shadow runs down and right at 28 degrees, like every other frame
- [ ] The track is cut by the right edge and is the only element that breaks the margin
- [ ] The gravel shoulder shows visible stroke direction change across the band, not a uniform texture
- [ ] The repoussoir clod is genuinely out of focus and bleeds off the bottom edge
- [ ] `alaskaaihq.com` is present, bottom, mono, low contrast
- [ ] No sensor trace, no result, no route shape anywhere on the frame

---

## SLIDE 02 — THE RETURN

**1. Beat.** PAYOFF, and the steepest drop in the deck is 1 to 2 so it pays
immediately. The loop the cover planted closes here, physically, in gravel.
Plants the next loop, what was in the box.

**2. Copy, final.**
- kicker, mono 26 px, `THE TRACK` (9 ch)
- headline, Archivo 118 px, two lines,
  `8 hours 47 minutes aloft.` / `The wheels stopped where they started.` (62 ch, C04, C03)
- body, Instrument Serif 38 px,
  `ACUASI, part of the University of Alaska Fairbanks, flew human blood for the International Testing Agency. UAF puts the flight at 8 hours and 47 minutes. The ITA's own release says only several hours.` (196 ch, 32 words, C09, C15, C04, C05)
- mono tag, 26 px, `DURATION PER UAF AND ACUASI` (27 ch, C04, C05)
- mono disclosure, 26 px, `THE LENGTH IS PUBLISHED. THE ROUTE IS NOT.` (42 ch, `[design]`)
- gold figure, mono 30 px, `1,000 KM` (8 ch, C01)
- counter `02 / 09`, watermark `alaskaaihq.com`

**3. Reader takeaway.** It flew for most of a working day and landed back on the
same gravel it left.

**4. Layout map.** Kicker col 1 to 3 row 1. Headline col 1 to 10 rows 2 to 3.
Body col 1 to 7 row 4. Mono tag and disclosure col 1 to 6 row 5, both above the
apron line. Focal point is the track's return crossing at 430, 1180. Eye path is
headline, body, then down to the double impression. Quiet zone is the upper
right sky, about 16 percent.

**4a. Lower-third treatment.** The bottom band carries the whole argument of the
frame as modelled ground. The tyre track runs the full width in the gravel
shoulder, and its second pass is offset 40 px and crushes the first, so the
reader sees one continuous impression with a doubled, deepened lobe where the
two passes overlap. Each pass is a real depression in the akhachure height
field, not a drawn line, so its walls carry a lit side and a shadow side under
the deck's one key at 24 degrees, and the crushed overlap is the darkest
modelled tone in the frame. The long cast of the chock pair crosses it at 28
degrees. This band is where the deck's craft density and its thesis are the same
thing.

**5. Depth plan.** Same six-cue stack as slide 01 with the focal plane moved
forward to y 1180 where the track crossing sits, so the crossing is the sharpest
thing in the deck. Treeline and haze carry the atmospheric lerp, the clod
carries the near blur, the track's own walls carry occlusion.

**6. Continuity device state.** Track CLOSED, the state change that names the
deck. Phantom absent. Gold on the chock pair, re-set beside the track, and on
the `1,000 KM` figure. Archivo wdth 113.

**7. Technique stack.** akhachure as slide 01 with the height field carrying two
gaussian troughs along the track's centreline, sigma 11 px, depth 0.42 and 0.55,
the deeper one being the second pass. The track's edge crumble is a seeded
displacement of the trough walls at amplitude 2.4 px. Cased line discipline on
the disclosure rule. Grain and grade as the deck.

**8. Data-in-art mapping.** Track length in frame is 1080 px of a 9,720 px
panorama and carries NO story quantity, so it is declared decorative for scale.
The 527 crowns continue. The `1,000 KM` figure is type, not a drawn length, and
the frame prints its own disclosure that the route's shape is not published.

**9. Palette assignment.** As slide 01. The crushed overlap reaches `#1A1712`,
the deck's floor value, and it is the only place on this frame that does. Gold
on two marks totalling about 0.6 percent of frame area.

**10. Type spec.** Headline Archivo 118 px wdth 113 wght 600, fitted
`{min: 92, max: 124, maxLines: 2}`, authored `<br>` after `aloft.`. Body
Instrument Serif 38 px, leading 1.38, `#C9C2B4`, max width 720 px. Mono 26 px
caps `#C9C2B4`, the gold figure mono 30 px `#FFC72C`.

**11. Anchor spec.** Two anchors, which is the doctrine maximum. The chock pair
as on slide 01, and the track itself as a drawn ground feature. Annotation
furniture is one dimension-call rule under the `1,000 KM` figure with 45 degree
cut terminals, and a leader from the disclosure text to the track's return
crossing, authored as a world coordinate polyline ending on the crossing's own
coordinates and declared in `window.__akLeaders` with `from`, `at`, `to` and
`label`.

**11a. Wordless claim.** A reader who reads nothing learns that the vehicle came
back, because the track returns into its own impression. Region A, the single
pass at `[760, 1120, 300, 120]`. Region B, the doubled crushed overlap at
`[330, 1140, 300, 120]`. `reads: "differ"`, and the two must be at least 4.0 dE
apart at feed scale, which the deepened trough should clear comfortably.

**12. Reference intent.** A gravel road surface photographed for a soils report,
where the marks in the ground are the evidence and nobody has arranged
anything.

**13. Risk flags.** The doubled impression could read as one wide track rather
than two passes. Mitigation, the offset is 40 px against a track width of about
210 px, so the lobe is clearly a partial overlap, and the acceptance checklist
makes a pixel critic answer it. Second risk, the leader could land in void.
Mitigation, it is authored to the crossing's own coordinates and qa.py fails it
beyond 24 design px.

**14. Acceptance checklist.**
- [ ] The track visibly returns into its own impression, two passes readable as two
- [ ] The crushed overlap is the darkest modelled tone on the frame
- [ ] The leader terminates on the crossing and its label reads
- [ ] `THE LENGTH IS PUBLISHED. THE ROUTE IS NOT.` is present and legible
- [ ] The body attributes the duration to UAF and never to the ITA
- [ ] Gold appears on exactly two marks
- [ ] No route shape is drawn anywhere on the frame
- [ ] `alaskaaihq.com` present, counter reads `02 / 09`

---

## SLIDE 03 — THE PAIR

**1. Beat.** The protocol becomes human. Two samples from one person, one flown
and one held, is the experiment's whole design and it is a thing a reader can
picture. Inherits what was in the box, plants what carried it.

**2. Copy, final.**
- kicker, mono 26 px, `THE DAY BEFORE, AT UAF` (22 ch, C35)
- headline, Archivo 112 px, two lines,
  `Every volunteer gave two samples.` / `One flew. One stayed.` (54 ch, C14, C13)
- body, Instrument Serif 36 px,
  `Staff from the Interior Region EMS Council drew the blood the day before at UAF. The samples were anonymised, chilled, and split into two groups, one flown and one held on the ground as a control.` (192 ch, 34 words, C35, C13, C14, C15, C17)
- mono label A, 26 px, `FLOWN` (5 ch, C13)
- mono label B, 26 px, `GROUND CONTROL` (14 ch, C13)
- mono note, 26 px, `SEALED BOXES, AND A TRACK TO PROVE IT NEVER LANDED` (49 ch, C16)
- counter `03 / 09`, watermark

**3. Reader takeaway.** The experiment is a pair, and only one half of it went
anywhere.

**4. Layout map.** Kicker row 1, headline rows 2 to 3 at col 1 to 9, body col 1
to 6 row 4. The folding table occupies col 4 to 11, rows 5 to 7, with the two
boxes on it. Focal point is the seal on the flown box at 700, 880. Eye path is
headline, body, the two boxes, then the seal. Quiet zone upper right, 15
percent.

**4a. Lower-third treatment.** The bottom band carries the folding table's legs
and their casts falling across the gravel shoulder at the deck's 28 degree
shadow vector, at 2.25 times leg height, so four long modelled bars of darkened
sky hue lie over the hachured ground and tie the table to the place. The track
passes behind the legs and is occluded by them, which is the frame's strongest
depth cue and also the continuity device changing state. The shoulder's own
slope and aspect field continues under everything with its specular crowns
intact, and the repoussoir clod holds the bottom 90 px out of focus.

**5. Depth plan.** As the deck, with an added occlusion layer where the table
legs cross the track. Focal plane at the table top, y 880. The far treeline is
lerped toward haze at (i/n)^1.4 and the clod carries the near blur.

**6. Continuity device state.** Track OCCLUDED, passing behind the legs. Phantom
absent. Gold on the seal of the flown box only, one mark. Archivo wdth 107.

**7. Technique stack.** Gradient solids for the two boxes with a 4 percent hard
highlight on each lid chamfer. Cross-hatch material code on the box sides, dense
crosshatch for the insulated flown box and sparse parallels for the open rack
holding the control. Layered shadow elevation under each box, stacked at 1, 2,
4, 8, 16 px in the darkened background hue. akhachure continues on the shoulder.

**8. Data-in-art mapping.** Two boxes because there were two groups (C13). The
rack behind them holds tubes in strict PAIRS because every volunteer gave two
(C14), and the rack is CUT BY THE FRAME EDGE so no count is claimed, which
keeps the pairing sourced and the quantity a property of the drawing. The 527
crowns continue on the shoulder.

**9. Palette assignment.** As the deck. The two boxes are the same value so
neither reads as favoured, and the only difference between them is the gold
seal on one, which is the record marking the one that travelled. Body type
`#C9C2B4`, labels `#F4F8FF`.

**10. Type spec.** Headline Archivo 112 px wdth 107 wght 600, fitted
`{min: 88, max: 118, maxLines: 2}`, authored `<br>` after `samples.`. Body
Instrument Serif 36 px. Labels mono 26 px caps on their own knockout plates
sized from the laid-out text with `AK.svgPlate`, never a typed width.

**11. Anchor spec.** The literal anchor is the folding table with two boxes. The
annotation is the two mono labels with leaders to their boxes, both authored as
world coordinate polylines ending on each box's own coordinates and declared in
`window.__akLeaders` with `from`, `at`, `to` and `label`.

**11a. Wordless claim.** One of these two identical boxes has a seal on it and
the other does not, which is the record marking the half that moved. Region A,
the flown box `[620, 800, 180, 130]`. Region B, the control box `[840, 800, 180, 130]`.
`reads: "differ"`.

**12. Reference intent.** A field table set up beside a runway, photographed
without styling, in the register of a chain-of-custody log rather than a
product shot.

**13. Risk flags.** Two labels with two leaders on a busy ground is the classic
place this house collides type with art. Mitigation, both labels sit on measured
knockout plates built by `AK.svgPlate` from the text's own bounding box, and
both leaders are declared so qa.py checks both ends. Second risk, the two boxes
could read as one object at thumb size. Mitigation, a 40 px gap and different
surface codes, dense crosshatch against sparse parallels.

**14. Acceptance checklist.**
- [ ] The two boxes are separable at 432 px thumb width
- [ ] Exactly one box carries the gold seal
- [ ] Both labels sit fully inside their own plates
- [ ] Both leaders terminate on their boxes and their labels read
- [ ] The track is visibly occluded by the table legs
- [ ] Four leg casts run down and right at 28 degrees
- [ ] The tube rack is cut by the frame edge so no count is implied
- [ ] `alaskaaihq.com` present, counter reads `03 / 09`

---

## SLIDE 04 — THE AIRCRAFT

**1. Beat.** Make the machine concrete, and make the payload look small against
it. The deck's one rendered frame. Inherits what carried the boxes, plants the
question the turn answers, which is what a thousand kilometres was for.

**2. Copy, final.**
- kicker, mono 26 px, `ACUASI OWNS TWO OF THEM` (23 ch, C11)
- headline, Archivo 104 px, two lines,
  `A 31 foot span,` / `and a 200 pound bay.` (35 ch, C11)
- body, Instrument Serif 36 px,
  `They are twin engine aircraft with three cargo drop doors, and they work off dirt, grass, ice or tarmac. UAF is one of nine FAA designated test sites for uncrewed aircraft.` (168 ch, 30 words, C11, C36)
- dimension call, mono 26 px, `31 FT` (5 ch, C11)
- mono note, 26 px, `TRACKED THROUGHOUT, SO NOBODY HAD TO TAKE ITS WORD` (49 ch, C16)
- counter `04 / 09`, watermark

**3. Reader takeaway.** It is a real aeroplane with a real bay, and the thing it
carried would fit in a picnic cooler.

**4. Layout map.** This is one of three frames where copy drops onto the apron,
so the reserve is punched rather than avoided. Headline col 1 to 7 rows 5 to 6,
sitting ON the apron with a punched reserve beneath it. Kicker row 4. Body col 1
to 6 row 7. The aircraft occupies col 3 to 12 rows 3 to 5, its starboard wing
cut by the right edge. Focal point is the main gear at 700, 940. Eye path is the
aircraft silhouette, the dimension call, then down into the headline. Quiet zone
is the sky above the tail, 14 percent.

**4a. Lower-third treatment.** The bottom band carries the aircraft's own cast,
a long modelled bar running down and right at the deck's 28 degree vector, at a
length of twice the wing height and a quarter again, laid across the hachured
gravel shoulder and broken where it crosses the tyre track's trough. Under the
main gear sits a measured contact, a lit pool of apron first and then an
attached cast into it, probed off the render rather than computed from the
camera. The repoussoir clod holds the bottom 90 px out of focus, and the
shoulder's slope and aspect field with its specular crowns continues beneath
everything, so the band carries mass, modelled relief, direction and the deck's
continuity device at once.

**5. Depth plan.** Sky ramp, haze, treeline, apron, the rendered aircraft,
gravel shoulder, repoussoir clod, type. Seven depth cues. The GPU frame supplies
real occlusion, a shadow map and IBL reflection on the nacelles. Focal plane at
the main gear, y 940. Camera math is the deck's shared kneeling rig, eye height
620 mm, and the aircraft is placed so that 31 feet of span subtends 840 px,
which sets the frame's scale at **27.1 px per foot** and is the number every
other dimension on this frame is derived from.

**6. Continuity device state.** Track SOURCED, running under the mainwheels at
the same width as the tyre, which is how the reader learns what has been making
the track for four frames. Phantom absent. Gold on the `31 FT` dimension call
only. Archivo wdth 101.

**7. Technique stack.** akthree GPU PBR, the deck's only rendered frame.
`AKT.setup` with the deck's fog in the haze hue, `AKT.environment` at 0.5,
`AKT.rig` matched to azimuth 208 elevation 24, anodized aluminium and glass
presets, 2048 px PCFSoft shadow map, ACES. **The GL frame renders to an
offscreen canvas and is composited into an `AKENGRAVE.drawOffscreen` buffer,
the reserves are punched on THAT buffer with blurred rectangles at blur 11, and
the result is drawn onto the visible 2D canvas and graded once.** A designed
Canvas fallback using painter's solid at identical silhouette and the identical
contact triple runs when `AKT.webglOK()` is false, and `AKT.snapshot` is checked
for `.ok` so a black frame can never ship. Dimension call per technique 73 with
4 px extension gaps and 6 px overshoot.

**8. Data-in-art mapping.** The aircraft is drawn at **27.1 px per foot**
`[design]`, solved from the 31 foot span (C11) so the printed dimension and the
drawn width are the same number rather than two typed constants. The bay is
drawn at that same scale. The three cargo drop doors are three real belly lines
(C11). Two nacelles because it is twin engine (C11). The 527 crowns continue on
the shoulder.

**9. Palette assignment.** Aircraft in the deck's cool bounce `#5A6A78` on its
shadow side and `#C9C2B4` on lit upper surfaces, so the machine sits in the same
light as the ground and never reads as a sticker. Apron `#2A241B` to `#4A3D2C`,
shoulder as the deck. Gold on one mark, the dimension call, about 0.3 percent of
frame area. Headline `#F4F8FF` on punched apron, worst-case contrast computed
against the punched fill rather than measured afterwards.

**10. Type spec.** Headline Archivo 104 px wdth 101 wght 600, fitted
`{min: 82, max: 110, maxLines: 2}`, authored `<br>` after the comma. Body
Instrument Serif 36 px. Dimension call and note mono 26 px caps.

**11. Anchor spec.** The literal anchor is the aircraft in elevation. The
annotation is the dimension call across the span with 3 to 1 arrowheads about
10 by 3.3 px, extension lines with a 4 px gap from the airframe and 6 px
overshoot, and the value set in mono small caps centred on the rule.

**11a. Wordless claim.** A very large machine was moved to carry a very small
thing. Region A, the aircraft's wing box `[300, 690, 420, 120]`. Region B, the
payload box drawn at the same 27.1 px per foot inside the bay cutaway
`[648, 806, 46, 32]`. `reads: "differ"`. The claim is that the scale is true,
which is why both regions are measured off the same solved constant.

**12. Reference intent.** An aircraft on a gravel strip in a general aviation
inspection photograph, not an air show. Matt surfaces, working paint, no glamour
lighting.

**13. Risk flags.** This is the frame most likely to fail the type gate, because
it is the only one where display type sits on rendered art. The proven mitigation
is the offscreen composite plus punch, verified this run on a probe that went
from four fails to zero on exactly that change. Second risk, a GL frame that
renders dead. Mitigation, the snapshot sentinel and a designed Canvas fallback.
Third risk, the aircraft reads as pasted on. Mitigation, its rig azimuth and
elevation are the deck's declared light, and its contact is probed off the
render.

**14. Acceptance checklist.**
- [ ] `AKT.snapshot` reported ok and the frame is not near uniform
- [ ] The headline sits on punched apron with zero art touching its glyphs
- [ ] The dimension call spans exactly the drawn span and reads `31 FT`
- [ ] Three cargo drop doors are visible on the belly
- [ ] The aircraft's cast runs down and right at 28 degrees like every other frame
- [ ] The contact under the main gear is attached, with a lit pool, not a detached dark ellipse
- [ ] The tyre track runs under the mainwheels at the tyre's own width
- [ ] Gold appears on exactly one mark
- [ ] `alaskaaihq.com` present, counter reads `04 / 09`

---

## SLIDE 05 — THE TURN

**1. Beat.** THE HINGE, and it concedes before it argues. The reader has spent
four frames suspecting that a thousand kilometres ending where it started is a
shortfall. This frame takes that away and gives back something sharper.
Inherits what the flight was for, plants what the distance was for.

**2. Copy, final.**
- kicker, mono 26 px, `WHY A CIRCLE` (12 ch)
- headline, Archivo 98 px, two lines,
  `A circle tests the cargo.` / `A line delivers the care.` (50 ch)
- body, Instrument Serif 36 px,
  `The flight began and ended at Nenana Municipal Airport. Closing a route holds everything still except the blood, which is how you find out whether the blood minds. It also means this test measured a sample and not a delivery.` (221 ch, 39 words, C03)
- mono note A, 26 px, `BEFORE THIS, UP TO ABOUT 20 KM, IN DOHA` (39 ch, C26)
- mono note B, 26 px, `THAT TRIAL INDICATED NO ADVERSE EFFECT, FOR SHORT DISTANCE TRANSPORT` (68 ch, C27)
- counter `05 / 09`, watermark

**3. Reader takeaway.** The loop was the control, and that is exactly why the
thing a clinic needs was not what got tested.

**4. Layout map.** Copy drops onto the apron here, punched. Headline col 1 to 8
rows 3 to 4. Body col 1 to 7 row 5. Notes col 1 to 8 rows 6 to 7. The two
geometries live in the shoulder below, the closed return at col 1 to 5 and the
straight rut at col 7 to 12 leaving the frame. Focal point is the closure at
340, 1150. Eye path is headline, then the two ground marks, then the notes.
Quiet zone upper right, 17 percent.

**4a. Lower-third treatment.** The bottom band carries the frame's entire
argument as two modelled marks in the same ground. On the left the tyre track's
closed return, a trough whose walls carry a lit side and a shadow side under the
deck's key at 24 degrees. On the right a straight wheel rut leaving the frame
with no return, in the same height field and the same hachured slope and aspect
texture, so the reader compares two shapes made of the same material rather than
two symbols. Between them the shoulder's specular crowns and the long cast of
the day's one light vector cross at 28 degrees. The band is the densest modelled
relief in the deck because this is the frame the deck exists for.

**5. Depth plan.** As the deck. Focal plane at the closure, y 1150. The straight
rut carries a scale gradient as it recedes toward the right edge and is lerped
slightly toward haze, so the two marks are at different depths and the reader
reads them as one continuous ground rather than a diagram.

**6. Continuity device state.** Track THE TWO GEOMETRIES. This is the only frame
where the motif appears twice in two states at once, which is why it is the
hinge. Phantom absent, deliberately, because nothing on this frame is about the
missing finding. Gold on one closure tick. Archivo wdth 95.

**7. Technique stack.** akhachure over both marks from one shared height field,
with the closed return as a pair of gaussian troughs and the straight rut as a
single trough that runs off the right edge without curvature. Cased line on both
mono notes. `AKENGRAVE.punchReserves` with blurred rectangles for the headline
and body boxes. Grain and grade as the deck.

**8. Data-in-art mapping.** The closed return is the flight's geometry (C03) and
the straight rut is its counterfactual, which is a `[design]` figure and is
never labelled as a real journey. Neither mark carries a length, and no measured
axis is declared on this frame, deliberately, so no position can be read as a
distance. The 50 to 1 comparison between 1,000 km and the earlier ceiling of
about 20 km is carried in TYPE (C01, C26) and not drawn, because drawing it
would require an axis this frame should not have.

**9. Palette assignment.** As the deck. Both marks in the same gravel values so
neither is favoured. The closure tick is the frame's only gold, about 0.2
percent of frame area, and it is a SEALED form, a filled disc, because the
closure is a published fact.

**10. Type spec.** Headline Archivo 98 px wdth 95 wght 600, fitted
`{min: 78, max: 104, maxLines: 2}`, authored `<br>` after `cargo.`. Body
Instrument Serif 36 px, max width 760 px. Notes mono 26 px caps.

**11. Anchor spec.** The literal anchor is the pair of ground marks. The
annotation is the closure tick with a short leader to the crossing point,
authored to the crossing's own coordinates and declared in `window.__akLeaders`
with `from`, `at`, `to` and `label`.

**11a. Wordless claim.** One of these marks comes back and the other does not.
Region A, the closed return `[220, 1090, 260, 140]`. Region B, the straight rut
`[760, 1090, 260, 140]`. `reads: "differ"`.

**12. Reference intent.** Two tyre marks on the same shoulder, read the way a
tracker reads ground. No arrows, no diagram, no legend.

**13. Risk flags.** The straight rut could be read as a second real flight,
which would be a fabrication. Mitigation, it is never labelled, it carries no
length and no destination, and the copy says only that a circle tests and a line
delivers. Second risk, the headline's two clauses could be read as a slogan
rather than an argument. Mitigation, the body immediately explains the
mechanism, which is that closing a route holds everything still except the
blood.

**14. Acceptance checklist.**
- [ ] The two marks are clearly the same material and clearly different shapes
- [ ] The straight rut carries NO label, NO length and NO destination
- [ ] The headline reads in two lines with the break after `cargo.`
- [ ] The body's mechanism sentence is present and legible at full size
- [ ] Both mono notes carry the Doha hedging exactly, up to about 20 km and for short distance transport
- [ ] Gold appears on exactly one mark and it is a filled disc
- [ ] No measured axis is declared on this frame
- [ ] `alaskaaihq.com` present, counter reads `05 / 09`

---

## SLIDE 06 — BREATHER

**1. Beat.** BREATHER, declared, and it earns its place by carrying a position
rather than a fact. The deck has just turned and the reader needs one frame to
stand still in before the record arrives. Inherits the distance question, plants
the timetable question.

**2. Copy, final.**
- headline, Archivo 92 px, two lines,
  `The distance was the point.` / `Alaska had the distance.` (51 ch)
- pull quote, Instrument Serif 56 px, three lines,
  `"I'm not saying we're ready today, but I think we'll be ready tomorrow."` (71 ch, C31)
- attribution, mono 26 px, `NEIL ROBINSON, ITA SCIENCE AND MEDICAL, TO UAF` (45 ch, C31)
- counter `06 / 09`, watermark

**3. Reader takeaway.** The people who ran it say plainly that this is not
ready yet, and they expect it to be.

**4. Breather declaration.** `data-breather` is set on the slide body. The deck
needs a rest here because slide 05 is its densest argument and slide 08 is its
densest record, and a reader who goes from one to the other without a pause
arrives at the card already tired. This frame carries one position and one human
sentence and nothing else.

**4a. Lower-third treatment.** The bottom band is the widest, most open view of
the apron and shoulder in the deck, and it is the frame where the hero structure
is exposed with nothing standing on it. The tyre track runs the full width with
both ends cut, the only mark in the frame, its trough walls modelled by the
deck's key at 24 degrees. The hachured slope and aspect field runs edge to edge
with its full population of specular crowns, the long cast of the frame's one
chock crosses it at 28 degrees, and the repoussoir clod holds the bottom 90 px
in genuine near blur. Nothing here is furniture and nothing is flat. The band is
modelled ground being looked at, which is what a breather in this deck should
be.

**5. Depth plan.** The deck's six cues with the sun disc visible for the second
and last time, a dim ochre disc with no flare and no rays, sitting just above
the haze band. Focal plane at the track, y 1120. The treeline is at its furthest
lerp toward haze on this frame, which is what makes the frame read as wide.

**6. Continuity device state.** Track ALONE, full width, both ends cut, the only
mark in the frame. Phantom absent. Gold is a single hairline on the sun disc's
rim, which names the date the flight happened (C02) and is the smallest gold
mark in the deck. Archivo wdth 89.

**7. Technique stack.** akhachure at its fullest population, four accumulation
passes. Multiplane parallax with the treeline at maximum atmospheric lerp.
Gradient solids for the sun disc. No punch needed, all type is on the sky band.
Grain and grade as the deck.

**8. Data-in-art mapping.** The 527 specular crowns continue and are at their
most visible here because nothing occludes them. Declared in
`window.__akAssert` with `points` and `dispersed: true`, and verified against the
composited png rather than against the loop that drew them, because a grade or a
punch can remove marks this fine without moving a coordinate.

**9. Palette assignment.** As the deck, at its widest tonal spread. The sun disc
is `#9A8460`, the sky ramp's own warm end, and it is NEVER gold. Pull quote in
`#F4F8FF`, attribution `#C9C2B4`.

**10. Type spec.** Headline Archivo 92 px wdth 89 wght 600, fitted
`{min: 74, max: 96, maxLines: 2}`. Pull quote Instrument Serif 56 px, leading
1.24, roman not italic, straight quotes, three lines broken by sense with
authored breaks so no line ends on a conjunction. Attribution mono 26 px caps.

**11. Anchor spec.** The literal anchor is the track. The annotation is the
single chock at the left edge with its cast. No leaders on this frame.

**11a. Wordless claim.** None. This frame is a rest beat and its art makes no
argument beyond being the place. Written rather than omitted so a critic does
not look for one.

**12. Reference intent.** The wide establishing frame of a documentary, held a
beat longer than necessary.

**13. Risk flags.** This is the frame most likely to bore a scroller, and the
declared breather demotes a frame balance failure to a warning, which means the
gate will NOT catch a weak version of it and a human has to. Mitigation, the
pull quote is the best human sentence in the whole claims record and it is set
at 56 px, and the frame carries the deck's most complete hachure field. Second
risk, the sun disc could read as gold. Mitigation, it is `#9A8460` and the ink
law is declared per frame so qa.py judges the gold at the brush.

**14. Acceptance checklist.**
- [ ] `data-breather` is set on the body and the dossier explains why
- [ ] The pull quote reads in three lines with no line ending on a conjunction
- [ ] The sun disc is NOT gold and carries no flare or rays
- [ ] The track is the only mark in the frame and both its ends are cut
- [ ] The hachure field shows visible direction change across the whole band
- [ ] The specular crown count is verified against the composited png
- [ ] Gold appears on exactly one hairline
- [ ] `alaskaaihq.com` present, counter reads `06 / 09`

---

## SLIDE 07 — THE HANGAR

**1. Beat.** Kill the misconception before it forms. A reader who has heard that
a German laboratory was involved will assume the blood was flown to Germany, and
it was not. Both groups were analysed on site, in a building at the same
airport, which is also the second half of the geometry argument. Inherits the
timetable question, plants who the answer is for.

**2. Copy, final.**
- kicker, mono 26 px, `ON SITE` (7 ch, C20)
- headline, Archivo 88 px, two lines,
  `The laboratory was in a building` / `at the same airport.` (52 ch, C19, C03)
- body, Instrument Serif 36 px,
  `Sysmex equipped a satellite laboratory inside an airport hangar with XN-Series analysers. Dr. Sven Voss, who directs the WADA accredited laboratory in Dresden, ran it. Both groups were analysed on site, under identical conditions.` (226 ch, 34 words, C19, C21, C20)
- mono disclosure, 26 px, `SYSMEX, WHOSE ANALYSERS WERE USED, HELPED PAY FOR THE FLIGHT` (59 ch, C34)
- counter `07 / 09`, watermark

**3. Reader takeaway.** The blood never left the airport, and the company whose
machines read it helped pay for the flight.

**4. Layout map.** The third and last frame where copy drops onto the apron, so
punched. The hangar's open door fills col 8 to 12 rows 2 to 5 and throws a wedge
of light onto the apron. Headline col 1 to 7 rows 3 to 4, body col 1 to 6 row 5,
disclosure col 1 to 8 row 7 on the apron itself. Focal point is the door's
light spill edge at 820, 900. Eye path is the door, the spill, the headline,
then the disclosure. Quiet zone is the sky at col 1 to 5, 15 percent.

**4a. Lower-third treatment.** The bottom band carries the door's wedge of
interior light falling across the apron and onto the gravel shoulder, which is a
second modelled light event in a deck that otherwise has one, and it is
motivated because an open hangar door on a lit apron really does throw one. The
wedge's edge is hard where it crosses asphalt and breaks into the hachured
gravel's slope and aspect field where it reaches the shoulder, so the texture
under it changes character rather than just brightness. The tyre track crosses
the spill and its trough walls flip which side is lit inside the wedge, which is
a real optical fact and the frame's best small piece of craft. The day's one cast
vector still runs at 28 degrees over the top of all of it.

**5. Depth plan.** Sky, haze, treeline, the hangar mass, the door aperture, the
apron, the spill, the shoulder, the clod, type. Seven cues, with the hangar
providing the deck's only large occluding mass and the door aperture providing a
genuine second light source rather than a painted patch. Focal plane at the
spill edge, y 900.

**6. Continuity device state.** Track PASSED, crossing the door's light spill.
Phantom still absent, and this is the last frame where that is true. Gold on one
mark, a 6 px square indicator on an analyser visible through the door (C19).
Archivo wdth 84.

**7. Technique stack.** Gradient solids for the hangar mass with a cabinet
oblique door reveal. The spill is a clipped polygon with a soft inner falloff
built as a blurred rectangle punch on an offscreen canvas, never a radial
gradient. akhachure continues on the shoulder with its lighting term flipped
inside the spill polygon. `AKENGRAVE.punchReserves` for the headline, body and
disclosure boxes. Cased line on the disclosure rule. Grain and grade as the
deck.

**8. Data-in-art mapping.** One analyser indicator because one company equipped
the laboratory (C19). The hangar is a building at the same airport, which is the
frame's whole factual content (C03, C19, C20). The 527 crowns continue outside
the spill. No quantity is encoded in the spill's size, which is `[design]`.

**9. Palette assignment.** The hangar mass is the deck's darkest large area,
`#1A1712` to `#2A241B`. The spill is a warm interior value at `#7A6A4F`
desaturated, deliberately NOT gold, because the light is not a record. Gold on
the single indicator square only, about 0.1 percent of frame area, the smallest
gold area in the deck. Headline `#F4F8FF` on punched apron.

**10. Type spec.** Headline Archivo 88 px, the deck's display floor, wdth 84
wght 600, fitted `{min: 88, max: 92, maxLines: 2}` with an authored `<br>` after
`building`. Body Instrument Serif 36 px. Disclosure mono 26 px caps `#C9C2B4`.

**11. Anchor spec.** The literal anchor is the hangar door with the laboratory
bench visible through it. The annotation is a leader from the disclosure line to
the analyser indicator, authored to the indicator's own coordinates and declared
in `window.__akLeaders` with `from`, `at`, `to` and `label`.

**11a. Wordless claim.** None declared. The frame's argument is carried by the
words, because where a laboratory was is not a thing a picture can assert
without a caption. Written rather than omitted.

**12. Reference intent.** An open hangar on a working strip in late afternoon
light, photographed from outside because that is where the reader is standing.

**13. Risk flags.** The spill is a second light and could be read as
contradicting the deck's one declared key. Mitigation, it is a motivated
aperture, it is named in the dossier as a disclosed second source, and its hue
is the interior warm rather than the sun's. Second risk, the disclosure line
could read as an accusation. Mitigation, its wording is flat and it says helped
pay, which is what the ITA's own release discloses, and the body has already
established the protocol was run to WADA documentation.

**14. Acceptance checklist.**
- [ ] The headline sits on punched apron with zero art touching its glyphs
- [ ] The body says both groups were analysed ON SITE and never that samples went to Germany
- [ ] The disclosure says HELPED PAY and never PAID
- [ ] The track's lit side visibly flips where it crosses the spill
- [ ] The spill is not gold
- [ ] Gold appears on exactly one 6 px indicator
- [ ] The leader terminates on the indicator and its label reads
- [ ] `alaskaaihq.com` present, counter reads `07 / 09`

---

## SLIDE 08 — THE RECORD, AS PUBLISHED

**1. Beat.** SYNTHESIS, and the deck's keepable frame. Everything the record
carries, laid out as a thing a reader would screenshot, with the empty half in
the same hand on the same paper. This is where the phantom register arrives.
Inherits who the answer is for, plants the one question the close asks.

**2. Copy, final.**
- kicker, mono 26 px, `THE RECORD, AS PUBLISHED` (24 ch)
- card rows, mono 28 px, right aligned values on a measured column:
  `FROM        NENANA MUNICIPAL` (C03)
  `TO          NENANA MUNICIPAL` (C03)
  `FLOWN       AUGUST 19TH` (C02)
  `ALOFT       8 H 47 MIN` (C04)
  `LENGTH      1,000 KM` (C01)
  `LAB         AIRPORT HANGAR, ON SITE` (C19)
  `PUBLISHED   SEPTEMBER 16TH` (C06)
- channel rows, mono 28 px, each with a dashed phantom rule and NO value:
  `TEMPERATURE` / `ATMOSPHERIC PRESSURE` / `HUMIDITY` / `VIBRATION` / `ACCELERATION` (C18)
- mono note under the channels, 26 px, `FIVE CHANNELS LOGGED. NO VALUES PUBLISHED.` (42 ch, C18)
- body, Instrument Serif 34 px,
  `The ITA says the results will be communicated once the evaluation has been completed, and that it intends to submit them to a peer reviewed journal. The comparison of blood counts before and after has not been published.` (219 ch, 37 words, C23, C24, C25)
- tape nodes, mono 26 px, `AUGUST 19TH` (C02) and `SEPTEMBER 16TH` (C06)
- tape tail label, mono 26 px, `NO DATE` (7 ch, C23)
- counter `08 / 09`, watermark

**3. Reader takeaway.** Everything about this test is written down except the
thing it was for.

**4. Layout map.** The card lies on the shoulder at col 2 to 10, rows 2 to 6,
rotated 7 degrees in plane with a 4 percent keystone so glyphs stay effectively
upright at 28 px and the perspective is carried by the lifted corner, the clip
and the contact rather than by distorting type. The steel tape lies in the tyre
track at col 1 to 12, row 8, running left to right. Focal point is the boundary
between the filled rows and the empty rows at 540, 860. Eye path is the filled
rows, the empty rows, then the tape's tail. Quiet zone is the sky above the
card, 14 percent.

**4a. Lower-third treatment.** The bottom band carries the steel tape lying in
the tyre track's trough, a real object in a real depression, so its body catches
the deck's key at 24 degrees on its upper face and drops a hard attached cast
into the trough wall beside it. Around and under it the hachured slope and
aspect field continues with its specular crowns, and the card's own cast falls
across the band at the deck's 28 degree vector at 2.25 times the card's lifted
corner height. The tape's solid segment is gold and ends in a sealed node; its
continuation past that node is the phantom, dashed and unfilled, running off the
right edge with no terminator, which puts the deck's whole argument into the
band the frame balance gate measures.

**5. Depth plan.** Sky, haze, treeline, apron, the card lifted off the shoulder
on one corner, the tape in the trough, the shoulder field, the clod, type. Seven
cues. Two measured contacts on this frame, one under the card's lifted corner
and one under the tape, both probed off the render with
`scripts/contact_probe.py --slide 8 --base cx,cy` and declared in
`data-contacts` in the MARKUP, never at runtime. Focal plane at the card, y 720.

**6. Continuity device state.** Track COVERED BY PAPER, half hidden under the
card, with the tape lying in what remains visible. Phantom ARRIVES, in two
places, the five channel rules and the tape's continuation. Gold on the
`8 H 47 MIN` cell and the two date nodes, three marks, the deck's maximum.
Archivo wdth 79.

**7. Technique stack.** The card is a paper solid with a lifted corner, built
from gradient solids with a 4 percent hard highlight along the lift and layered
shadow elevation beneath. Rows are SVG text with plates sized by `AK.svgPlate`
from each label's own bounding box, never a typed width. The phantom rules use
`pathLength="100"` with a dasharray dividing evenly so both ends land on full
dashes. The tape is a cabinet extrusion with a lit upper face. akhachure
continues on the shoulder. Grain and grade as the deck.

**8. Data-in-art mapping.** The tape is a MEASURED AXIS and is declared in
`data-scale`, `from` [180, 0] `to` [740, 28], unit days, band [1150, 1182], with
**every mark inside the band enumerated with its meaning**, twenty eight day
ticks plus two nodes, because there is no such thing as a decorative tick on a
measured axis. That is **20 px per day** `[design]`, solved from the 28 days
between August 19th and September 16th (C02, C06). The five channel rows are
five because five channels were logged (C18) and every one of them is EMPTY,
which is the drawing. No sensor value appears anywhere.

**9. Palette assignment.** The card is warm bone `#C9C2B4` paper with `#2A241B`
ink, the only light-valued large area in the deck and it is a lit object rather
than a background. The five channel rules are phantom `#9FB3C4`. The tape's
solid segment is gold `#FFC72C`, its continuation phantom. Three gold marks
totalling about 1.1 percent of frame area, just inside the 1.2 percent ceiling.

**10. Type spec.** Card rows JetBrains Mono 28 px, 500, tracking +10 percent,
caps, tabular figures, on a measured column so the values align on a common left
edge. Body Instrument Serif 34 px, the deck's body floor. Kicker, note and tape
labels mono 26 px caps. No Archivo on this frame at all, which is deliberate,
because this frame is the instrument speaking.

**11. Anchor spec.** Two anchors, the doctrine maximum. The card and the tape.
Annotation furniture is the tape's tick rhythm with 45 degree cut terminals on
its solid segment and NO terminator on its phantom continuation, plus a leader
from the `NO DATE` label to the point where the gold stops and the phantom
begins, authored to that point's own coordinates and declared in
`window.__akLeaders`.

**11a. Wordless claim.** The same paper, the same hand, the same rules, and one
half has numbers in it. Region A, the filled rows `[300, 560, 520, 240]`.
Region B, the five empty channel rows `[300, 820, 520, 200]`. `reads: "differ"`.
This is the deck's central declaration and its regions are measured off the
rendered png, never off the layout arithmetic.

**12. Reference intent.** A flight record card on a clipboard, photographed
where it was filled in. The register of evidence, not of design.

**13. Risk flags.** An empty half can read as BROKEN rather than as PENDING,
which would hand the deck an implication of failure the record does not support
and the brief forbids. Mitigation, the five rows are fully NAMED and ruled in
the same hand as the filled rows, so they read as specified and not yet
answered, and the body says in words that the evaluation is not complete.
Second risk, twenty eight day ticks plus two nodes is thirty declarations on a
measured axis and a single undeclared mark fails the deck. Mitigation, the marks
are generated from the same loop that draws them and the declaration is written
from that loop rather than by hand. Third risk, density. This is the deck's
densest frame at VISUAL_DENSITY 3 and it is allowed to be, because a keepable
reference frame is the one place density is a feature.

**14. Acceptance checklist.**
- [ ] The card's filled rows and empty rows are on the same paper in the same hand
- [ ] All five channel names are present and NONE carries a value
- [ ] `FIVE CHANNELS LOGGED. NO VALUES PUBLISHED.` is present and legible
- [ ] The tape's gold segment ends in a sealed node and the phantom has NO terminator
- [ ] Every tick inside the tape's declared band is enumerated in `data-scale`
- [ ] Both contacts are attached, measured off the render, and declared in the markup
- [ ] The `NO DATE` leader terminates where the gold stops
- [ ] Card rows are legible at 432 px thumb width
- [ ] Nothing on the frame states or implies a result
- [ ] `alaskaaihq.com` present, counter reads `08 / 09`

---

## SLIDE 09 — CLOSE

**1. Beat.** CLOSE, one ask, and the ask is the argument rather than a
housekeeping request. The deck has established that Alaska supplied the distance
and that the answer arrives on somebody else's timetable, so the only honest
thing to hand a reader is the choice that follows from it.

**2. Copy, final.**
- headline, Archivo 96 px, two lines,
  `Alaska supplied the distance.` / `The finding has no date.` (53 ch, C23)
- body, Instrument Serif 36 px,
  `ACUASI director Cathy Cahill describes nurses going into a community, taking samples, and getting the medication back before the nurses leave. That is a line, not a loop.` (168 ch, 28 words, C29, C09)
- the ask, Instrument Serif 56 px, two lines,
  `A longer loop, or a shorter line?` / `Which does Alaska need next?` (61 ch)
- wordmark, Archivo 88 px, `ALASKA.AI` set as the brand mark in the display band
- counter `09 / 09`, watermark

**3. Reader takeaway.** The capability is real, the answer is somewhere else,
and the thing Alaska actually needs is a different shape.

**4. Layout map.** Headline col 1 to 8 rows 2 to 3 on the sky band. Body col 1
to 6 row 4. The ask col 1 to 8 rows 6 to 7, with a gold rule beneath it. The
wordmark and Polaris sit at col 9 to 12 row 8. Focal point is the Polaris in the
last chock at 880, 1080. Eye path is headline, body, the ask, then the mark.
Quiet zone is the sky at col 9 to 12 rows 1 to 3, 16 percent. The single
permitted grid violation is the track running out of the bottom left corner,
which breaks the margin toward the reader rather than toward the next swipe,
because there is no next swipe.

**4a. Lower-third treatment.** The bottom band carries the tyre track turning
out of the frame at the bottom left corner, toward the reader rather than off
the right edge, which is the only frame in the deck where the motif does that
and is how a reader feels the deck end. Its trough walls are modelled by the
deck's key at 24 degrees all the way to the cut. The last chock sits on the
shoulder at the right with the Polaris seated in it as the deck's final gold, and
its long cast runs down and right at 28 degrees at 2.25 times its height across
the hachured slope and aspect field. One dashed phantom arc leaves the chock and
runs a short way into the gravel without closing, the deck's last mark and its
last open form. The band holds mass, modelled relief, the continuity device and
the argument's final image at once.

**5. Depth plan.** The deck's six cues at their most settled. Focal plane at the
chock, y 1080. The treeline is closer to the camera here than on any other frame
because the pan has reached the end of the apron, which gives the close a
naturally more enclosed feeling without changing the camera.

**6. Continuity device state.** Track OPEN TOWARD THE READER, out of the bottom
left corner. Phantom is the last mark in the deck, one unclosed arc. Gold on the
Polaris in the last chock and on the ask's rule, two marks. Archivo wdth 74, the
narrowest the deck goes, because the argument has come down to one question.

**7. Technique stack.** akhachure over the shoulder as the deck. Gradient solids
for the chock. The Polaris is a four point star drawn as SVG so the film grade
never shifts it, with a 30 px halo ring at low opacity. The phantom arc uses
`pathLength="100"` so both its ends land on full dashes. Neon layering is
explicitly NOT used, the Polaris is a flat brand mark. Grain and grade as the
deck.

**8. Data-in-art mapping.** The Polaris is seated in the last chock because the
chocks have meant the flight's two ends since slide 01 (C03). The phantom arc
carries no quantity and is declared `[design]`. The 527 crowns continue.

**9. Palette assignment.** As the deck. Gold on two marks, about 0.5 percent of
frame area. The phantom arc is `#9FB3C4`, unfilled, unlit. Headline and ask both
`#F4F8FF` on the sky band, body `#C9C2B4`.

**10. Type spec.** Headline Archivo 96 px wdth 74 wght 600, fitted
`{min: 88, max: 100, maxLines: 2}`, authored `<br>` after `distance.`. Body
Instrument Serif 36 px. The ask Instrument Serif 56 px, leading 1.24, two lines
with an authored break after the question mark. Wordmark Archivo 88 px wdth 74.
Counter and watermark as the deck.

**11. Anchor spec.** The literal anchor is the last chock with the Polaris in
it. The annotation is the gold rule beneath the ask with 45 degree cut
terminals, matching the terminal flourish used deck-wide. No leaders on this
frame.

**11a. Wordless claim.** The mark that has run through every frame leaves
toward the reader and one line beside it does not close. Region A, the track's
exit at the bottom left `[80, 1150, 300, 160]`. Region B, the unclosed phantom
arc `[700, 1150, 300, 160]`. `reads: "differ"`.

**12. Reference intent.** The last frame of a field record, where the person
holding the camera has stood up and is about to walk back to the truck.

**13. Risk flags.** Six elements compete in the bottom third on this frame, the
headline having descended, the ask, the wordmark, the Polaris, the coordinates
and the watermark, which is exactly the busy-art-under-text pair arriving by a
different door. Mitigation, a hard split with type held at col 1 to 8 and the
mark and its craft at col 9 to 12, and the headline stays on the SKY band rather
than descending onto the shoulder. If the first render comes back under 0.90 the
honest repair is to lift the ask by 60 px rather than to shrink the reserve.
Second risk, the ask could read as rhetorical. Mitigation, it names a real
choice a reader in Alaska can hold a position on.

**14. Acceptance checklist.**
- [ ] Exactly ONE ask appears on the frame, and it is a question
- [ ] The headline reads in two lines with the break after `distance.`
- [ ] The track exits the bottom LEFT corner, not the right edge
- [ ] The Polaris is seated in the last chock and is SVG, not canvas
- [ ] The phantom arc does not close and carries no terminator
- [ ] Gold appears on exactly two marks
- [ ] No source note of any kind appears anywhere on the frame
- [ ] `alaskaaihq.com` present, counter reads `09 / 09`

---

## BUILD RECONCILIATION

Written BEFORE any pixel critic was spawned, per the hard ordering rule, because
a critic measuring a render against superseded numbers spends a third of its
findings on things the build already changed.

### EVERY DOSSIER NUMBER THE BUILD CHANGED

| What the dossier said | What shipped | Why |
|---|---|---|
| Horizon at 506, apron at 940 | **Horizon at 620, apron at 1000** | At 506 the body copy on slide 02 crossed the horizon glow and the punched reserve behind it read as a flat plate, which is the exact defect the reserve exists to prevent. Raising the horizon gives every frame a type zone the art never enters, which is cheaper and truer than reserving harder. Every frame moved together, so the panorama still seams. |
| Spruce ranks at 54 and 86 px | **38 and 58 px** | The treeline's spikes rose into the body copy's last line on slides 03 and 07. Lowering them also reads as more distance, which suits a wide apron. |
| S01 headline `1,000 kilometres out of Nenana, back to the same airport.` in 2 lines | **`1,000 km of blood. Out of Nenana. Back to Nenana.` in 3** | The planned line ran 30 characters and Archivo at wdth 118 needs about 20 characters a line to hold the display floor. The shipped cover is also the stronger hook, because the repetition of one place name is a shape a thumb reads before it reads words. |
| S02 headline `8 hours 47 minutes aloft. The wheels stopped where they started.` | **`8 h 47 min aloft. Back at Nenana.`** | Same fit limit. `AK.fitText` bottomed out at `min` and set four lines against a declared two, which the engine reports and which is how a 2026-08-12 deck shipped missing a sentence. |
| S03 headline `Every volunteer gave two samples. One flew. One stayed.` | **`Two samples each. One flew. One stayed.`** | Same fit limit, twice. The shipped version is three short lines and reads better at 432 px. |
| S02 body sat on the sky with no reserve | **Body on the sky, mono block on the apron, PUNCHED** | The sky band could not hold five stacked blocks once the horizon moved. |
| S01 track `enters bottom right, cut by the right edge` | **crosses the shoulder and is cut by the right edge** | A trough whose polyline starts mid frame gets a blunt square cap from the wall fill, which read as a drawn artefact. Running it off both edges removes the cap and keeps the edge tease. |
| S01 `527 lit crowns, one per minute aloft`, declared in `__akAssert` | **DROPPED. The crowns ship as surface texture with no count claim.** | Measured, not guessed. The repoussoir clod and the track walls are drawn over the shoulder BY DESIGN, and a probe found 24 of 176 sampled centres carrying no mark, so the frame showed 152 where the declaration said 527. A declaration the composited picture contradicts is the defect, not the drawing. The duration is carried in type on slides 02 and 08 instead, where it is checkable. |
| S04 was to be the deck's GPU PBR frame | **Canvas 2D, FRONT elevation, parallel projection** | The frame prints a dimension and a dimension is a quantity, and 3D data honesty says a quantity never goes through a perspective camera. A front elevation makes the 31 foot span the horizontal dimension, so the dimension call measures the thing it names. The scale is solved from the lock, 840 px for 31 feet, 27.096 px per foot, and `window.__akAssert` reads its `actual` back off that constant rather than off a typed literal. THE DECK SHIPS NO GPU FRAME, and that is a decision rather than a failure. The GPU path was proven working this run on a probe (snapshot ok, 88,119 lit pixels, 1.6 s a frame) and was not used because perspective would have made the dimension dishonest. |
| S05 closure tick with a short leader | **A gold disc with a fine ring, no stem** | A stem running up toward words IS a leader, and qa.py correctly failed it because its label was 232 px away. This is a mark on the ground, so it is drawn as one. |
| S08 `data-encodes` on the filled half against the empty half | **NO encoding declaration on that frame** | Measured and dropped. The probe returned dE 2.5 against a 4.0 floor and reported that 64 percent of region A and 35 percent of region B is ground that measured TYPE sits on, so it was reading the reserve and not the encoding. A declaration that cannot be evidence is worse than none. The claim is real and it is left to the pixel critics, who can read. |
| S08 card rotated 7 degrees with a 4 percent keystone | **Axis aligned, with a lifted leading edge** | Rotated mono rows at 28 px cost more legibility than the perspective bought, and legibility is this run's second target. |
| S08 tape band `[1116,1152]` | **`[1140,1156]`** | The axis census could not separate the day ticks from the band's own texture at the wider band. The ticks were also drawn heavier, at 2.5 px. |
| Light pools carried on `fillRect` | **`APRON.litPool`, an ellipse with the ramp built on a CIRCLE inside a transform** | A lit pool is not a rectangle. And Canvas has no elliptical gradient, so pouring a circular ramp into an ellipse stops the paint on the short axis while the ramp still carries alpha and leaves a hard arc, which qa.py caught on seven frames and printed the repair for. |
| Nothing under a punched reserve | **`APRON.baseWash`, a full height graded wash laid before the buffer composites** | What a punch REVEALS matters as much as the punch. On the first build it revealed bare body background, so five frames showed a flat dark rectangle behind their copy, which is the plate the doctrine bans. |
| S02 `DURATION PER UAF AND ACUASI` plus the body | both shipped | no change |
| S06 attribution `NEIL ROBINSON, ITA SCIENCE AND MEDICAL, TO UAF` | **`NEIL ROBINSON, ITA, TO UAF`** | The longer string ran under the sun disc and failed worst point contrast at 3.3. |
| S03 `SEALED BOXES, AND A TRACK TO PROVE IT NEVER LANDED` | **cut from slide 03** | It sat on the treeline with no reserve. C16 is carried on slide 04 instead. |
| S07 body without a reserve | **`data-reserve`** | The treeline crossed its last line. |
| The claims index as planned | **regenerated from `copy.json`** | `plan_drift_check` found nine drifts between the planned index and what the frames print. The build is the artifact, so the index was corrected rather than the deck. |

### ROWS THE FIRST PASS OF THIS TABLE MISSED

Added after round one, and the omission is the finding. SIX of the nine critics
opened a defect that amounted to "this diverged from the dossier and the
reconciliation table, which claims to list every dossier number the build
changed, is silent on it." A table that is trusted and incomplete is worse than
no table, because it spends a critic's attention proving something the build
already knew. Every divergence below was real and none of it was written down.

| What the dossier said | What shipped | Why |
|---|---|---|
| S03 body `Staff from the Interior Region EMS Council drew the blood the day before at UAF. The samples were anonymised, chilled, and split into two groups, one flown and one held on the ground as a control.` | **`The Interior Region EMS Council drew the blood at UAF the day before. It was anonymised and chilled, then split into two groups.`** | Length. The planned sentence set six lines in the frame's 760 px column and pushed the mono block onto the treeline. Nothing in the claim changed: the EMS Council is still the agent, the day before is still the day, and the two groups are still two. The flown/control split is carried by the two labelled boxes, which is the frame's whole drawing. |
| S03 a paired tube rack, cut by the right frame edge | **Not drawn** | It was the frame's only carrier of C14 as drawing rather than as type, and cutting it at the edge was the device that kept the pairing sourced without claiming a count. It lost its place to the two boxes, which carry the same claim more legibly at 432 px. Recorded here so a later round does not re-add it believing it was forgotten. |
| S05 headline in 2 lines, break after `cargo.` | **2 lines, one sentence each: `A circle tests the cargo.` / `A line delivers the care.`** | The build first authored four lines, which split verb from object and broke the doctrine's three line cap. Fixed in round one. |
| S06 headline `The distance was the point.` / `Alaska had the distance.` | **3 authored lines carrying BOTH sentences** | The build shipped only the first sentence and no row was written. The half that went missing was the Alaska half, on the one frame whose declared job is to carry a position, in an Alaska deck. Restored in round one at 3 lines and a smaller display size, which is what the frame can hold above the treeline. |
| S06 one gold hairline on the sun's rim, naming C02 | **ZERO gold on the frame; the hairline is crown `#A8946F` and `data-ink` declares gold ABSENT** | The gold law is that a mark traces to a claim id PRINTED ON ITS OWN FRAME, and a breather prints no claim id, so the mark was never entitled to be gold. It also read as a detached yellow crescent, which made the sun look gold rimmed, and a gold sun in a deck where gold means the record destroys the law. Printing a date on the breather to license the mark was the other way out and is worse: a breather that acquires a fixture stops being a breather. |
| S07 body ends `...analysed on site, under identical conditions.` | **ends `...analysed on site.`** | The trailing clause is not in the source. Dropping it is the safer reading and it should have been recorded when it was dropped. |
| S07 headline in 2 lines, break after `building` | **3 lines** | The same `AK.fitText` limit as S01, S02 and S03, and the same reason those three have rows. |
| S08 seven card rows plus a serif body paragraph | **Nine card rows, no serif body** | `RESULTS / ONCE EVALUATION IS COMPLETE` and `JOURNAL / SUBMISSION INTENDED` carry C23 and C24 inside the card's own grammar, which is tighter than the paragraph they replaced and legible at 432 px. |
| S08 gold on the `8 H 47 MIN` cell | **Uniform card ink on every value; the frame's gold is the tape** | A gold cell inside a card of black cells reads as the card's own emphasis rather than as the deck's record ink, and the tape is the frame's measured axis. |
| S09 headline `Alaska supplied the distance.` / `The finding has no date.` | **First sentence as the headline; the second in Instrument Serif 40 px phantom slate** | The build demoted the second sentence to 26 px mono caps, which made the deck's second thesis sentence the smallest non-decorative string on its last frame at 4.2 to 4.7:1. Round one kept the phantom colouring, which is a good idea, and moved it into the serif register at 40 px in sentence case, which also clears the deck's mono-never-lowercase absolute. |

### WHAT ROUND ONE CHANGED, AND WHY IT WAS MOSTLY CHASSIS

Nine verdicts came back `revise`. The defects clustered hard, so most of the
repair is in `assets/js/akapron.js` and `assets/js/akengrave.js`, where one edit
reaches every frame.

| Defect, and how many frames reported it | Repair | Measured reason |
|---|---|---|
| The punched reserve reads as a lighter rectangle (5 frames: 02, 04, 05, 07, 09) | `baseWash` is built from `ground()`'s own gradient recipe and carries its own scale-graded fleck field; `AKENGRAVE.boxesFor` measures per LINE BOX via a `Range`; punch blur 10 to 26 | Two causes. The wash was a hand-picked ramp sitting several percent above the apron it stood in for, and a MATCHED but FLAT reveal is still findable because the grain stops inside it. Separately `boxesFor` measured the ELEMENT, so a 900 px div holding 600 px of ragged copy reserved 300 px of empty rectangle and the punch knocked a hole where there was nothing to protect. |
| No cast anywhere carries a readable 28 degree edge (6 frames) | `cast()` builds the union at full alpha in a 2x buffer and composites once, then lays a second shorter union over the near half | Sixteen translucent copies smeared onto the frame never acquire a terminator: every step is another three percent ramp. One critic said the chocks appeared to EMIT light. A shadow's terminator is its argument, and two hard edged tones model a cast where twenty soft ones model nothing. |
| A dead stippled apron meeting the hachure at a hard seam (5 frames) | A far hachure pass at grid 16, two passes, alpha 0.13, `lenMul` 0.52, over one long lit sweep, overlapping the shoulder pass by 34 px | One full-strength pass over the whole plane was tried FIRST and was worse than the defect: the frame read as fur, and it kept the reserve visible, because a reserve is found by the fact that the texture stops inside it. A receding graded surface needs DIRECTION, not coverage. Stroke length relative to spacing is what separates gravel from grass, which is what `lenMul` is for. The shoulder pass is byte for byte what it was, because every critic who looked at it called it the best ground this house has shipped. |
| A mechanical sawtooth treeline (2 frames) | Per-tree jitter off the grid, a per-tree height multiplier that only ever SHORTENS (0.42 to 1.00), and an asymmetric profile | A fixed period with a symmetric triangle at every node is a comb. One critic noted it sat close enough to a waveform to be mistaken for the sensor trace this deck refuses to draw. The multiplier shortens only because the rank ceilings were already lowered once to keep spruce out of the S02 body block. |
| The chock is a flat sticker (01, 02), a smudge (06), invisible (09) | `APRON.chock`, one modelled prop with a top plane, a shadow end, a painted front, ribs, a chamfer highlight and a rope eye | A filled polygon in a bright hue is a SHAPE, not a THING. It was authored inline twice and drawn four ways, and a prop drawn four ways is four props. |
| S02: the return is invisible, so the deck's thesis is absent from the frame built to carry it | `returnOffset(gx) = 86 * tanh((gx - 1480) / 430)`, crossing the outbound at local x 400, with the crushed lobe drawn between the two centrelines | A constant 40 px gap against a 210 px track is a 19 percent shift the frame cannot resolve, and both troughs were cut to the same depth so the overlap never darkened. It read as the two walls of ONE rut, identical in structure to slide 01's. A return has to CROSS, and the lobe then pinches to nothing exactly where they do. |
| S02: the leader makes the drawn rut read as the measured 1,000 km | The leader now leaves the DISCLOSURE, and `1,000 KM` gets its own free rule with 45 degree cut terminals, touching nothing | A gold quantity joined by a rule to a mark on the ground is the grammar of a dimension call, and a dimension call says "this thing is that long". The frame says the route is not published 40 px above. The two statements were contradicting each other inside 200 px of frame. |
| S05: the closed return's join is a square-cornered rectangle | Leg, turn and leg back are ONE polyline with a real 54 px radius, sampled continuously by the height field | Two troughs both ending at the same x get blunt caps from the wall fill, and the deck's hinge mark read as a slab on the focal point of the frame the whole deck exists for. A tyre that turns leaves curvature. |
| S08: the blank rule strikes through `ATMOSPHERIC PRESSURE` | Per-row rule start; that row begins at x 534 | 20 characters of 28 px mono run to about x 506 and the shared start was x 430, so the rule crossed seven glyphs at mid height and read as CANCELLED. The record says that channel was logged and its values not published, which is the opposite. The rule is a blank and not a quantity, so a shorter one is honest. |
| S08: the two halves are not in the same hand | All five channel rows get the full-width hairline the filled rows carry | Same-hand setting is the mitigation the dossier's own risk flag names as the thing keeping the empty rows PENDING rather than BROKEN. The only difference between the halves is now that one has values in it. |
| S08: the phantom tail ends inside the frame | Tape body and dash both run past the canvas; dash start 704 to 718 | The dash period is 57, so where the line meets the edge is determined: from 704, `(1080-704) mod 57 = 34`, which lands in a GAP, and the phantom appeared to peter out. From 718 it is 20, solidly inside a 30 px dash. A line that ends where the page ends has no terminator; one that fades out before the page ends has given itself one. |
| S04: the wordless claim is not in the picture | A bay cutaway holding a payload box at the SAME solved constant (1.7 ft = 46 px at 27.096 px/ft), three full-height door breaks, per-wheel lit pools, an airframe cast, a tapered wing, spinner cones and prop discs, and the fin pinned symmetric | Field 11a declares that a very large machine was moved to carry a very small thing, and only the large machine was drawn, so the span had nothing to be large AGAINST and the claim collapsed to "here is an aeroplane". The fin leaned, and in a declared parallel projection carrying a printed dimension a lean is an error, not perspective. |
| S09: the deck ends on a sign-off rather than an image | The chock moves x 860 to x 700 and is lit, the Polaris follows it, the arc is re-centred on it at r 200 and widened to 2.5 | The chock was three values of dark brown on dark brown gravel, 12 px above the cap line of an 88 px white wordmark, and no critic could find its silhouette at any size. With it invisible the arc's only apparent centre was the Polaris, so the deck's last open form read as brand ornament. |
| Aerial perspective lerped per hachure row | Banded in six steps | Not taste. `qa.py`'s paint census holds 160 entries, and a fresh colour literal per row flooded it and EVICTED `#FFC72C`, so two frames failed the ink law reporting no gold on frames that plainly had gold on them. Six bands times the seven step ramp is 42 literals, and it is also how an engraver cuts distance. |
| S07: a 4 px terminal dot on the leader | No terminal dot | The dot was centred on the 6 px gold indicator and covered it completely. The ink census measured the frame's only gold as ZERO pixels, so the fix for a missing leader had erased the mark the leader was drawn to point at. The gold square is its own terminator. |

### ROUND TWO, INCLUDING TWO ROUND ONE REPAIRS DELETED

The second sweep returned `revise` on all nine again, with slides 02 and 03 at
4.0. **The two worst findings on the deck were both things round one added.**
That is the round's real lesson and it is worth more than the repairs: a fix
aimed at a named defect can land a bigger one, and only a fresh adversarial read
catches it. Neither was visible to the machine gates, which were green.

| Defect | Repair | Measured reason |
|---|---|---|
| S02: the relocated leader reads as A PLOTTED ROUTE (round one's own doing) | DELETED, along with the figure's rule | Moving the leader off the gold figure was right in principle, because a quantity roped to a mark on the ground is a dimension call. Re-originating it at the disclosure made it a 1,020 px hairline at 37 degrees across the whole lower right quadrant, which at 432 px is the most prominent non-type mark on the slide, and it sat directly beneath the sentence "THE ROUTE IS NOT." The frame drew the one thing this deck exists to refuse. Its 37 degrees also put a second angle family into a deck whose entire discipline is one angle. |
| S02: the figure's "free rule" reads as a dimension bar (round one's own doing) | DELETED | A rule with 45 degree cut terminals is not a flourish, it is technique 73. In gold, directly under a gold quantity, on the frame that refuses to draw a length, it reads as an unlabelled scale bar saying "this bar is 1,000 km". It was also a third gold mark where the checklist allows two. The frame now makes three statements and ropes none of them to another. |
| The ground reads as straw, stubble, fur or a mown hayfield (5 critics) | A dark counter-stroke per lit stroke, offset opposite the key at half weight; plus a sparse population of lit convex chips | The decisive diagnosis came last: every mark in the field was LIGHTER than its ground, so nothing was ever occluded by anything. A population of pale needles with no dark counterpart is a crop whatever its length or weight. A stone is legible because it casts into its own bed. Shorter, heavier and rotation-jittered had all been tried first and none of them was the cause. |
| A hard bright rule under the treeline on the PUNCHED frames only | `baseWash` carries the treeline's own value through that band | Round one built the wash from `ground()`'s stops so the two could not drift apart, and that made it peak at exactly the horizon, because the apron's top edge is its brightest part. But the ART there is the treeline, a dark silhouette drawn over it, so a punch revealed a bright ridge where the frame is dark. The unpunched frame did not show it, which is what identified the cause. |
| The chock is modelled but reads as a dustpan | Top plane in a lighter VALUE of the front's own gold, three shallow grooves instead of eight full-height ribs, top plane depth 0.26 to 0.13 of face height | One material means one hue: a bone top plane on a gold face reads as a pale card lying on a yellow wedge. Eight even dark strokes across a face are bristles. And a top plane nearly as deep as the face is tall is not what a camera kneeling at 620 mm sees. |
| S03: the table stands in a void, and both boxes are pasted on the plank | An attached contact at every foot, a five step seating stack under each box, and the table raised 40 px | The table's own cast is 2.25 x 226 px = 508 px along the light vector, so nearly all of it was off the bottom of the frame: the legs ran down into the unlit band and simply stopped. A long cast cannot staple an object to the ground; a short hard contact under the foot can. |
| S03: the two boxes are not the same value | The dense crosshatch's alpha drops 0.30 to 0.13 | The dossier's claim is ONE RECORD MARK ON A MATCHED PAIR. The crosshatch was darkening the flown box 12 to 15 percent, so a reader was shown two different objects one of which was tagged. The difference is now purely the surface code and the seal. |
| S03: both leaders start inside the object they point at | DELETED | Each plate already lies on its own box, so the association is positional and the line was redundant furniture. The control leader terminated in the middle of a flat box face on nothing at all, and at 432 px both read as scratches on the frame's two focal objects. |
| S03: the seal has an open-cut stem | Stem dropped, darker gold outline added | The gold law wants a form terminated at both ends. The stem's lower end was an open cut and it was visually identical to the two leader hairlines beside it, so the seal read as a luggage tag. |
| S07: the hangar reads as a dumpster | Eave 604 to 430, the lit top plane deleted, a left return wall whose edges converge down toward the horizon | The eave sat 20 px ABOVE a horizon of 620, which put the roofline at the height of distant spruce, and a lit top plane was drawn. A camera kneeling at 620 mm cannot see the roof of a hangar thirty metres away. |
| S07: the bench and analyser are three flat rectangles on the frame's focal anchor | Three planes, a top chamfer, a lit bench nosing and an attached contact | The raw-default-rectangle failure landing on the one object the frame is about. |
| S08: five blanks, two left edges | One common edge at x 558 | Round one moved only the offending row, leaving four blanks at x 430 and one at x 534, so the card ran two rule logics at once and the ragged edge was visible at 432 px. "The same hand ruled both halves" has to survive inspection. |
| S09: the phantom sentence is set IN slate | Type returns to bone; a dashed unterminated slate rule under it states the register | A glyph is a filled shape, and the phantom register is only ever an OPEN form. It was the one place in nine frames where the phantom was a solid, and it put a third type colour into the lower band. The idea was right, so the SHAPE carries it instead. |
| S09: the chock overlaps the wordmark | Moved laterally to x 300, into the departing track's own path | Raising it 40 px was not enough. At 432 px the chock and the logotype fused into one object, a gold star badge on a wordmark, which is the exact failure the move was meant to repair arriving from the other side. |
| The apron is uniform: direction but no tonal variation | Two lobe periods, pure functions of global x, laid as a GRADIENT | Sampled into 8 px fillRects each strip had its own flat alpha and adjacent strips banded, so the cure for a uniform apron was a frame of corduroy, which is worse. A gradient interpolates between its stops. |
| S03 foot contacts: a circular ramp poured into an ellipse | The ramp built on a CIRCLE inside a transform | The chassis learned this once already on `litPool`, and the same mistake was made again eighty lines away. `qa.py` caught it on four fills and printed the repair. |

### WHAT DID NOT DIVERGE

The one light never moved. Azimuth 208, elevation 24, key to fill 3.5 to 1, with
every cast running down and right at 28 degrees at 2.25 times object height, on
all nine frames. The gold law held, one to three marks a frame, every one of them
on a sealed form, and the phantom register appears on frames 08 and 09 only and
is always dashed, unfilled and unlit. The panorama seams hold, because no slide
authors its own horizon. No frame states or implies a result, no frame draws a
route shape, no frame draws a sensor value, and the range comparison appears
nowhere.

### WHAT THE MACHINE SAYS ABOUT THE STANDING WEAKNESS

Nine frames, `qa.py` zero fails and ZERO WARNS. None of the five defect classes
`trend_check` named fired on any frame, which is the thing this run set out to
do in `plan.md`. `bespoke_check` median pairwise art similarity 0.251 against a
0.60 fail, max pair 0.450, with a standing warn that the drawn share sits at 50
percent against a 45 percent floor.

### GATE STATUS

Written by `python scripts/gate_status.py --run-dir out/2026-09-18 --sync
out/2026-09-18/storyboard.md`, never by hand, and re-synced after EVERY round
that changes an artifact.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-09-18. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[PASS] qa.py          PASS, 0 fails, 0 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] reconciled     BUILD RECONCILIATION present, 20 table row(s), 7413 chars
[PASS] caption_check  PASS, 867 chars, hook 125, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 61 authored slide strings all present in the render; alaskaaihq.com on every slide; no banned slide string
[PASS] aggregate      aggregate_check: PASS -- 3 aggregate assertion(s) detected, 5 declared -> out/2026-09-18/aggregate_report.json
[PASS] plan_drift     plan_drift_check: PASS -- 25 claims indexed, 0 declared counts checked, 6 body quote(s) checked, 0 drift(s)
[PASS] bespoke        bespoke_check: WARN -- 9 slides, median pairwise art similarity 0.251 (fail at 0.60), max pair 0.448, drawn share 50% (12 drawn vs 12 blocky
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] ledger_guard   LEDGER GUARD: PASS, 7 cron-written file(s) untouched
[PASS] docket_dates   docket dates clean at 2026-09-18: 384 assertions over 6 fixtures and 31 ledger items
[WARN] gas_watch      44 day(s) on record, 37 verified, no gaps, latest 2026-09-13, EIA through 202605 over 131 months, model misses by 6.82%, which is 5 days old
[WARN] gas_watch_live MAINTENANCE, checked 2026-09-18T07:12:28Z
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-09-18 (198 generated files)
[PASS] assemble       9 slides, pdf vector 5.42 MB, 9 thumbs, sources verified
[n/a ] score          score_report.json missing
[FAIL] ship_gate      score_report.json missing. The run cannot ship or stop until it has been scored. ITERATE, do not stop. weakest: ?
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 1 FAIL row(s). Fix the artifact, not the sentence.
```

