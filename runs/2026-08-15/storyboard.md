# STORYBOARD — Carousel No. 34 — 2026-08-15

## THE DIRECTORS ROOM, and what was taken from where

Three lenses pitched in parallel. The synthesis takes the cinematographer's
staging, the essayist's vantage and paper doctrine, and the systems
illustrator's absence apparatus.

**Two of three directors independently built the deck around a rendered soft
toy with a machine in it, sitting on a lit surface with the public record laid
out beside it as labelled empty places.** Per instinct 0.85, when two
independent voices invent the same mechanism it is the shape of the record
pulling them there, not two writers making the same slip. It is taken.

- **From the CINEMATOGRAPHER (winner on staging).** One set, one light, a
  camera that moves; the absences staged as places on the same surface, lit
  exactly as brightly as the toy, identical in size and never filled. Its own
  honest self-criticism is adopted as a constraint: the camera move is the
  least legible device on a phone, so it is never asked to carry an argument
  alone, and the register slide is built FIRST rather than last.
- **From the ESSAYIST (winner on vantage and on paper).** The camera sits at a
  child's eye line rather than an inspector's, which is the strongest available
  divergence from four consecutive adult views of an object presented for
  inspection. And the doctrine that settles the whole honesty problem: **every
  document in this deck renders BLANK, because the deck never prints type onto
  a page it could not read.** Blank paper is not a caveat, it is an accurate
  depiction. It also caught a real violation in the showrunner's own thesis
  line, "no page anyone can reach", which is the de-pronouned first person
  brand.yaml bans by name. Rewritten.
- **From the SYSTEMS ILLUSTRATOR.** The dimension call with no dimension. The
  phantom dash as the only way an unscheduled thing is ever drawn, never at
  standard weight. The ruled and empty column. And the distinction that governs
  the whole deck: an unlit lamp says READ AND EMPTY, a missing lamp says NEVER
  LOOKED, and those are different marks.
- **Rejected.** The systems illustrator's DIN-rail terminal bus as hero. It is
  a beautiful diagram and it is not what the story is about; a terminal block
  costs the deck the one thing this subject has that no recent deck did, which
  is an object an Alaskan already owns.

---

## DECK HEADER

### Thesis

**The first federal answer to the machines that talk to children is a request
for a plan and a study, and the record that would say when either is due is not
published.**

Not a complaint. A plan and a study are the normal opening move for a
technology nobody has measured, and the deck says so at full weight on slide
06. What the deck refuses is the pretence that anything has been decided.

**Document title (42 chars):** `A Plan, a Study, and No Published Due Date`

### Arc

| # | Beat | Open loop planted |
|---|---|---|
| 01 | COVER. The toy on the floor at a child's height, one blank sheet cut by the right edge. | What is that blank paper. |
| 02 | THE TWO DELIVERABLES. Two agencies owe a plan, one academy owes a study. | Owed by when. |
| 03 | THE DATE IS NOT ON THE FLOOR. The bill text came back 403, the committee page publishes no tally. | Then what IS on the record. |
| 04 | THE AGENDA. Keepable. Five bills that morning, three of them AI. | Why any of this now. |
| 05 | WHAT THE SPONSORS SAY THE TOYS DID. Duckworth, and the testing as the release cites it. | Where does the Alaskan stand. |
| 06 | THE ALASKAN'S CASE. Murkowski, and the fair reading of a bill that buys knowledge. | Is buying knowledge enough. |
| 07 | BREATHER, declared. Empty floor, the deck's own sentence alone. | What does Alaska already have. |
| 08 | ALASKA'S RECORD, ATTRIBUTED. Four lines in one bracket, one stamp. | What is a reader supposed to do. |
| 09 | CLOSE. One ask. | none, it closes. |

Emotional temperature shifts at 05, which is the only slide where the deck
lets the subject be frightening, and settles at 06, which is the only slide
where it argues FOR the bill.

### Slide count rationale

Nine. The band is 6 to 12 and the default is 8 to 10. The deck has exactly nine
things to do and no filler: a cover, four load-bearing findings, one keepable
artifact, one declared rest, one attributed Alaska block and a close. Eight
would force the agenda table and the deliverables onto one frame, which is the
keepable slide and the payoff slide fighting for the same room.

### Continuity system

**A. THE FLOOR DOLLY (panorama spine plus camera move).**
One continuous woven floor. The camera height and pitch never change; only x
moves. The weave is a pure function of world x from one seed, so consecutive
frames seam exactly.

| Slide | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 |
|---|---|---|---|---|---|---|---|---|---|
| `data-camx` (m) | 0.00 | 1.15 | 2.30 | 3.45 | 4.60 | 5.75 | 6.90 | 8.05 | 9.20 |

CHECKED: every slide body carries `data-camx`; the Phase 8 record-sync step
asserts the nine values are strictly increasing and equal to this table. The
device is never asked to carry an argument on its own, per the
cinematographer's own warning that a reader on a phone sees nine stills.

**B. THE DUE FIELD (motif, and the deck's whole argument in one block).**
Bottom left of every slide, mono `DUE`, then a 168 px phantom dashed rule sized
by `AK.svgPlate` from the measured string. It is EMPTY on all nine slides
including the close. In the opposite corner the progress counter advances 01/09
to 09/09. **Two counters share the frame and only one of them can move.**

| Slide | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 |
|---|---|---|---|---|---|---|---|---|---|
| DUE field | empty | empty | empty | empty | empty | empty | empty | empty | empty |
| Counter | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 |

CHECKED: a gate walks all nine rendered DOMs, asserts the `[data-due]` block
exists on each, asserts the rule width equals the measured constant, and
asserts **zero digit glyphs inside the block on every slide**. Instinct 0.85
says a declared deck-wide device ships on zero slides unless something checks
it, so this one is checked by counting characters rather than by looking.

**C. THE PAPER STATE (motif evolution).**
Every document in the deck is a sheet lying on the floor, and every sheet is
BLANK. What varies is its outline and its stamp.

| State | Outline | Stamp | Meaning |
|---|---|---|---|
| read | solid, std 2 px | `READ AUG 15 2026` | fetched and read in full |
| 403 | phantom dash `30 5 6 5 6 5`, fine 1.25 px | `403 AUG 15 2026` | asked and refused |
| unpublished | phantom dash, fine 1.25 px | `NOT PUBLISHED` | looked for, does not exist on the page |

| Slide | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 |
|---|---|---|---|---|---|---|---|---|---|
| read sheets | 0 | 2 | 0 | 1 | 1 | 1 | 0 | 1 | 1 |
| 403 sheets | 1 (cut) | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 2 |
| unpublished sheets | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 3 |

CHECKED: every sheet carries `data-paper="read|403|unpublished"` and
`data-claim="<id>"`. The gate asserts every sheet has a claim id, that no sheet
contains body text, and that the per-slide counts match this table.

**Why blank paper is honest and not a dodge.** Printing invented text onto a
document nobody could read is the one thing this page never does. A blank sheet
with a solid outline says the page was read. A blank sheet with a dashed
outline and a 403 stamp says the page was asked and refused. Absence of the
sheet entirely would say nobody looked, which is false.

### Variety ledger check, stated explicitly

| Axis | Last four decks | This deck |
|---|---|---|
| Hero | THE OPEN TREAD (30), THE FALLING FRAME (31), THE LOCKED CHASE (32), THE EQUAL-AWARD PROJECTION (33) | **NEW: THE CHILD'S EYE LINE** |
| Atmosphere | TAILRACE SLATE (31), LOCKUP RAKE (32), NEAR-EDGE PLATE LAMP (33) | **NEW: HALLWAY BACKLIGHT, ROOM FOG** |
| Hook | question-first descent (31), THE HONEST WITNESS (32), THE CONTRADICTED ARTIFACT (33) | **NEW: THE SUBJECT'S EYE LINE** |
| Palette | tailrace slate and copper (31), type metal and newsprint (32), plate night and regulated magenta (33) | **NEW: CARPET WOOL AND HALLWAY BLUE** |
| Type | Instrument Serif + Archivo + Mono (32), Bricolage + Fraunces + Mono (33) | Unbounded + Manrope + JetBrains Mono |

**NEW: THE CHILD'S EYE LINE.** One continuous floor, one camera pinned at 0.22 m
above it, dollying right across nine frames, with the toy and the paper record
lying on that floor together. **All four forbidden heroes are FIXED ADULT
VIEWS of an object presented for inspection** and this is the only one of the
five with a moving camera at the vantage of the person the bill is about.
No.30 was orthographic and stepped. No.31 held the frame and varied scale. No.32
pinned the chase at 30 degrees for all nine. No.33 was a flat sheet seen square
on. This deck holds scale absolutely constant and varies POSITION.

**NEW: THE SUBJECT'S EYE LINE (hook archetype).** The reader is put where the
affected party is and shown what is and is not lying on the floor beside them.
It is a vantage claim, not a question (31), not a verbatim self-disclosure that
exonerates the subject (32), and not one artifact holding two officially correct
facts (33).

### Variance dials

**design_variance 4, visual_density 3, TYPE_TEMPERATURE 2.**

Type temperature was set to 4 at wake, before the story was known, and is
revised DOWN to 2 here with the reason written rather than quietly changed. The
story's own register is a cold room with exactly one warm object in it, and the
only warm faces available (Fraunces, Instrument Serif, Bricolage) all appear in
the last two decks' trios. Worse, using a warm serif reserved for the senators'
verbatim words would be No.33's own device repeated one run later. A cold
geometric type system with the warmth carried entirely by the rendered object
is the right answer to this picture. As a triple, (4, 3, 2) differs from No.30's
(5, 2, 3.5), No.32's (4, 4, 2) and No.33's (5, 5, 5).

### Palette and type system

**NEW: CARPET WOOL AND HALLWAY BLUE.**

| Role | Hex |
|---|---|
| room shadow | `#040A14` |
| base | `#050B16` |
| carpet wool | `#16262F` |
| lit fibre | `#2E4652` |
| hallway spill core | `#8FB6E8` |
| hallway spill | `#6EA5FF` |
| paper | `#C9D4DE` |
| phantom (unscheduled, 403, unpublished) | `#3F5B78` |
| grille steel | `#8A9AA8` |
| felt warm | `#C98468` |
| felt shadow | `#A05F45` |
| display type | `#F4F8FF` |
| **gold** | `#FFC72C` |

**GOLD CARRIES EXACTLY ONE MEANING, THE MACHINE'S VOICE.** It appears only as
the toy's grille emissive and its reflection in the weave, plus the Polaris and
wordmark fixture on the close, which is the constellation mark and not a second
meaning. Gold never touches a label, a rule, a number, a stamp or the DUE
field. The DUE rule is drawn in phantom `#3F5B78`, because the deck's grammar
is that anything unscheduled is a phantom dash and can never be given the
weight of something scheduled.

**FALSIFIABLE PALETTE CLAIM, handed to the pixel critics to contradict.** On
slides 01 through 08 there is no gold pixel outside the grille and its floor
reflection. Additionally, no supporting colour in this deck sits within OKLCH
hue 25 degrees of copper (h 50) or magenta (h 350) at chroma above 0.05, and
the area-weighted mean hue of every frame lands in the blue quadrant, which
newsprint neutral could not. Those are the three families the last three decks
used, so this is the divergence claim stated as a measurement rather than as
prose.

**TYPE.** Unbounded (display, the deck's OWN voice, wght 500 to 700, 84 to 132
px, tracking -2%, optical-left pull mandatory for its wide sidebearings, always
through `AK.fitText` with maxLines declared) + Manrope (body AND every
quotation, wght 400 to 600, 34 to 38 px, leading 1.38, measure 30 to 40
characters) + JetBrains Mono (instrument, stamps, table, DUE field, counter, 19
to 26 px, tracked +10 percent, tabular lining numerals).

Full-ledger pairing audit, per instinct 0.85. Unbounded last carried a deck as
display in No.31 (four runs back) and appears nowhere in No.32's or No.33's
trios. Manrope has NEVER been this series' body face on a rendered-hero deck
and never appears in either forbidden trio. The trio as a whole has not
shipped.

**THE TYPOGRAPHIC ARGUMENT, and why this is not No.32 or No.33 wearing a hat.**
Every verbatim quotation in this deck is set SMALLER than the deck's own
sentences, in the body face, never in a display face and never in a face
reserved for it. No.32 enthroned the verbatim as its hook archetype and No.33
gave the subject's own words their own typeface. Here the hierarchy argues the
opposite thing on purpose: **the words on the record are smaller than the
problem.**

### Claims index

| Claim | Slides |
|---|---|
| C01 session date and time | 04 |
| C02 room SR-253 | 04 |
| C03 five bills | 01, 04 |
| C04 to C08 the five bill numbers and titles | 04 |
| C09 three of five carry AI | 01, 04 |
| C10 three Coast Guard nomination lists | 04 |
| C11 no tally published | 03, 04 |
| C12 passed committee per the sponsor's release | 02, 04 |
| C14 Murkowski named as Republican cosponsor | 06 |
| C15 FTC and CPSC owe a coordinated plan | 02 |
| C16 National Academies owe a study | 02 |
| C17 the release describes no rule | 02, 06, 07 |
| C19 Murkowski on development | 06 |
| C20 Murkowski on knowledge | 06 |
| C21 Duckworth on chatbots in toys | 05 |
| C24 the PIRG testing as the release cites it | 05 |
| C27 CPSC index carried nothing | 03, 09 |
| C28 FTC index carried nothing | 03, 09 |
| C29 to C30 the column's author and date | 08 |
| C31 HB 47 | 08 |
| C32 to C33 HCR 3 and its stall | 08 |
| C34 roughly 30 states | 08 |
| C35 companion chatbot disclosure | 08 |
| C37 congress.gov 403, so no due date | 01, 03, 09 |
| C38 PIRG 403 | 05, 09 |

---

## THE SHARED SCENE, written once and parameterised per slide

Every slide draws its own composition with its own code. What is shared is
house furniture and nothing more: the room's palette constants, the weave
height function, and the camera rig helper. No slide calls a
`drawTheWholeSlide()`. `bespoke_check.py` measures the outcome and the deck is
built to clear it with room.

**THE PROTOTYPE FINDINGS ARE BINDING** (`out/2026-08-15/art_prototypes.md`):

1. The offscreen webgl2 context is created with `alpha:true` BEFORE
   `AKT.setup`, then `R.renderer.setClearColor(0x000000,0)`.
2. `AKPOST.grade` runs on the 2D layer BEFORE the GL composite. About 1 second
   before, about 34 after.
3. The floor is a MATERIAL. A procedural canvas texture, fbm stretched on one
   axis so the weave has a direction, `RepeatWrapping` at `repeat(22,22)`,
   `SRGBColorSpace`, hung on the ground material. Without it the composition
   gate measures 0.15 against a 0.60 fail line; with it, 0.75.
4. Mass is composed LOW. Type occupies the top third and nothing else does.
5. **SEAT THE HERO.** `AKT.objectHero({height})` rescales about the group
   origin, so after it the object's bounding box minimum y is not 0 and the toy
   hovers. Three lines fix it and they appear in every dossier that scales:
   `toy.updateMatrixWorld(true); const bb=new THREE.Box3().setFromObject(toy);
   toy.position.y -= bb.min.y;`
6. `data-contacts` rects are measured off the RENDERED PNG, never off the
   camera arithmetic.
7. Two materials minimum on the hero. Warm felt against cold anodised metal
   reads at 432 px; a single material does not.

**THE TOY, built and proven in prototype P5.** Body a sphere r 0.92 scaled
(1.0, 1.12, 0.94); head a sphere r 0.66; ears spheres r 0.25 flattened to z
0.42; arms and legs capsules; muzzle a flattened sphere; eyes spheres r 0.075.
FELT `AKT.mat.clay(0xC98468,{roughness:0.99})`, FELT_D `0xA05F45`. THE MACHINE
IN THE CHEST is a `METAL` torus bezel r 0.30 tube 0.036, a DARK circle face,
and three concentric METAL rings at r 0.072, 0.144, 0.216, with a `#FFC72C`
emissive ring behind them. It is the only cold material on the object and the
only gold in the deck.

**Determinism.** `AK.reseed(20260815 + slideNo)` and `AK.rng(20260815 +
slideNo)` at the top of every slide. No `Math.random`, no `Date.now`.

---

## SLIDE 01 — COVER

### A. NARRATIVE

1. **Beat.** Stop the scroll with the object the law is about, seen from the
   height of the person it is about. Inherits nothing. Plants the loop: there
   is a blank sheet of paper on the floor beside it, cut by the right edge, and
   it has a dashed outline.
2. **Copy, final.**
   - kicker, mono 24 px, 34 chars: `SENATE COMMERCE / AUGUST 5TH, 2026`
   - headline, Unbounded 500, `AK.fitText({min:84,max:132,maxLines:3})`, 12
     words, 62 chars, broken by sense:
     `The first federal answer to talking toys / is a plan / and a study.`
     [C15, C16, C17]
   - stamp on the cut sheet, mono 19 px: `403 AUG 15 2026` [C37]
   - DUE field, mono 22 px: `DUE` then a phantom dashed rule, no value
   - counter, mono 24 px: `01 / 09`
   - coordinates footer, mono 17 px, `data-decorative`: `61 13 N 149 54 W`
3. **Reader takeaway.** Congress moved on toys that talk to children, and what
   it asked for is a plan.

### B. COMPOSITION

4. **Layout map.** 12 x 8 grid, 80 px margins. Headline occupies cols 1 to 9,
   rows 1 to 3, optical-left pulled 6 px. Toy at the focal third, cols 6 to 10,
   rows 4 to 7, its grille at (0.66 W, 0.62 H). Eye path is headline, grille,
   then the dashed sheet exiting right. Quiet zone is cols 1 to 4 of row 4,
   about one eighth of the frame, well under the quarter ceiling. One permitted
   grid violation: the sheet crosses the right margin.

4a. **Lower-third treatment.** The carpet itself, rendered as a lit material and
   not as a plane. The bottom band carries the woven floor in raking key light
   with real fibre direction from the procedural texture at repeat(22,22), the
   toy's two-part contact shadow spreading toward the camera, the near edge of
   the blank 403 sheet with its own soft shadow, and exp2 fog thinning toward
   the lens so the foreground weave is the sharpest thing in the frame. The
   mass of the toy sits across the middle and lower thirds by construction, per
   prototype P4, which measured 0.75 against a 0.60 fail line on exactly this
   arrangement. No scattered marks anywhere; the prototype that tried that read
   as debris.

5. **Depth plan.** Background room fog and falloff to near black; mid-ground
   the toy; near-ground the blank sheet and the weave. Depth cues, six of them:
   occlusion (the sheet overlaps the weave, the toy overlaps its own shadow),
   atmospheric perspective (exp2 fog in `#0A1620`), scale gradient (weave texel
   density falls with distance), depth of field (the grille is the tack-sharp
   plane, the far floor blurs), fog, and one key light with a two-part shadow.
   Camera pos (0.00, 0.22, 2.35) world metres, pitch -4 degrees, fov 52.
   Horizon at 0.62 H, which is a low horizon and reads monumental for an object
   28 cm tall.
6. **Continuity device state.** `data-camx="0.00"`. DUE field empty. Paper
   state: one 403 sheet, cut by the right edge, completing on slide 02.

### C. ART DIRECTION

7. **Technique stack.** akthree GPU PBR (#87) for the toy and the floor;
   `AKT.rigs.arcticNight` re-aimed to the deck's own key; `AKT.environment`
   intensity 0.5; `AKT.objectHero` with `toward:[0.2,3.4,-5]` for the back key,
   keyColor `#8FB6E8`, intensity 2.2, height 3.0, then seated per finding 5.
   akpost (#89) grade on the 2D layer first, exposure -0.08 stops, saturation
   1.04, contrast 1.06, bloom threshold 0.74 strength 0.30 radius 8, grain
   amount 0.045 size 2 seed 20260815, dither true. Grain tile (#2) over the
   composite. Seed 20260816 for the weave.
8. **Data-in-art mapping.** The grille's emissive ring is divided into five
   arcs, three lit and two dark, encoding three of the five bills on the
   agenda carrying AI or chatbot subject matter [C09]. The count is ALSO
   printed flat in mono as `3 OF 5` on slide 04, because instinct 0.92 says a
   quantity may never ride perspective alone.
9. **Palette assignment.** bg `#050B16`; carpet `#16262F` to lit fibre
   `#2E4652`; toy `#C98468` and `#A05F45`; grille steel `#8A9AA8`, emissive
   `#FFC72C`; paper `#C9D4DE` at 0.42 alpha in fog; phantom outline `#3F5B78`;
   type `#F4F8FF`. Worst-case text contrast is the headline's third line over
   the lit fibre pool, estimated 11.4 to 1 against a 4.5 floor.
10. **Type spec.** Headline Unbounded wght 500, fit 84 to 132 px, leading 0.98,
    tracking -2%, upper and lower case, `#F4F8FF`, max width 820 px, fit-to-box.
    Kicker JetBrains Mono 400, 24 px, tracking +10%, `#8FB6E8`. Counter and DUE
    JetBrains Mono 400, 24 px and 22 px, `#7E93A8`. Stamp JetBrains Mono 700,
    19 px, `#3F5B78`, on a measured `AK.svgPlate` knockout.
11. **Iconography and anchor spec.** The literal anchor is the toy. The
    annotation furniture is the DUE field and the sheet stamp, both on measured
    plates. No leaders on the cover.

11a. **Wordless claim.** The soft body and the hard machine in its chest must
    read as two different things at feed scale. Regions, to be measured off the
    rendered PNG and not off this arithmetic: the felt shoulder and the grille
    face. `reads: "differ"`.

### D. VERIFICATION

12. **Reference intent.** A museum object photographed at the height of the
    person it belongs to.
13. **Risk flags.** Unbounded at 132 px overflowing its box, mitigated by
    `AK.fitText` with maxLines 3 declared; if it will not fit at min 84 the
    layout is rebuilt rather than the string shortened. The black-frame race,
    mitigated by `await AKT.snapshot(R)` and checking `.ok` with a designed
    AK3D fallback. The toy reading as a blob at 432 px, mitigated by silhouette
    rather than detail, ears and muzzle breaking the outline against fog.
14. **Acceptance checklist.**
    - [ ] The headline sets in 3 lines or fewer and no line touches the toy.
    - [ ] The grille reads as a separate material from the body at 432 px.
    - [ ] Exactly one blank sheet is visible and it is cut by the right edge.
    - [ ] The sheet's outline is a phantom dash, never solid.
    - [ ] The DUE field contains no digit.
    - [ ] The toy's contact shadow reads at 432 px, `data-contacts` above 8 L*.
    - [ ] No gold appears anywhere except the grille and its floor reflection.
    - [ ] The carpet weave is visible in the bottom 200 px at 432 px.

---

## SLIDE 02 — THE TWO DELIVERABLES

### A. NARRATIVE

1. **Beat.** Pay off slide 1 immediately with what the bill actually asks for.
   Inherits the blank sheet loop and pays it, since the sheet completes here as
   two READ sheets. Plants: owed by when.
2. **Copy, final.**
   - kicker, mono 24 px: `02 / 09 / WHAT THE BILL ASKS FOR`
   - headline, Unbounded 500, fit 72 to 104, maxLines 2, 9 words:
     `Two agencies owe a plan. / One academy owes a study.` [C15, C16]
   - body, Manrope 500, 34 px, 42 words:
     `Per Senator Duckworth's release, the Federal Trade Commission and the
     Consumer Product Safety Commission must give Congress a coordinated,
     actionable plan on AI-enabled toy products. The National Academies must
     conduct a comprehensive study into AI-enabled toys.` [C15, C16]
   - guard chip, mono 20 px on a measured plate:
     `THE RELEASE DESCRIBES NO RULE, NO BAN AND NO STANDARD` [C17]
   - sheet stamps, mono 19 px: `READ AUG 15 2026` twice [C12]
   - DUE field empty, counter `02 / 09`
3. **Reader takeaway.** The bill orders a plan and a study, not a rule.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 8 rows 1 to 2. Body cols 1 to 6 rows 3 to
   4. Two blank READ sheets lying on the floor cols 5 to 12 rows 5 to 7, in
   perspective, one nearer and one further. Guard chip cols 1 to 6 row 7. Focal
   point is the nearer sheet's leading corner at (0.58 W, 0.68 H). Eye path is
   headline, body, sheets. Quiet zone cols 9 to 12 rows 1 to 2.

4a. **Lower-third treatment.** Two blank sheets lying in perspective on the lit
   weave, each with its own soft cast shadow, occupying the near half of the
   floor and overlapping each other so the depth reads through occlusion rather
   than through position alone. Behind them the carpet runs back into exp2 fog,
   and the raking key gives the fibre direction real width variance across the
   band. The toy's warm grille reflection falls across the near sheet's edge,
   which is the only warm mark below the fold and the thing that keeps the band
   from going neutral. The mass is the paper and the weave together, both
   rendered, neither a plate.

5. **Depth plan.** Fog, occlusion between sheets, scale gradient in the weave,
   depth of field with the near sheet's edge sharp, one key with two-part
   shadows, and the toy's own light spilling from off-frame left as a warm
   gradient. Camera pos (1.15, 0.22, 2.35), pitch -4, fov 52. The toy is off
   frame left; only its grille spill is in the picture, which is how gold stays
   present on every slide without the object being restaged.
6. **Continuity device state.** `data-camx="1.15"`. Two `data-paper="read"`
   sheets. DUE empty.

### C. ART DIRECTION

7. **Technique stack.** akthree for floor and sheets; sheets are
   `AKT.extrude` thin plates with bevelSize 0.004 so the edge catches the key.
   akpost grade before composite, same house numbers as slide 01. Seed
   20260817.
8. **Data-in-art mapping.** Two sheets for two obligations. Never three, never
   a stack, because the count is the argument and a stack would blur it.
9. **Palette assignment.** As the deck table. The warm grille spill is a single
   radial in `#FFC72C` at 0.10 alpha, clipped to the floor, which is the only
   gold on the slide and satisfies the falsifiable claim.
10. **Type spec.** Headline Unbounded 500, fit 72 to 104, leading 1.0, tracking
    -2%. Body Manrope 500, 34 px, leading 1.38, max width 620 px, `#DDE6EF`.
    Guard chip JetBrains Mono 700, 20 px, tracking +10%, `#8FB6E8` on a
    `#0A1620` measured plate. Stamps JetBrains Mono 700, 19 px, on measured
    plates.
11. **Iconography and anchor spec.** Anchor is the pair of sheets. Annotation
    furniture is two leaders, one from the words `TRADE COMMISSION` to the far
    sheet's own corner and one from `NATIONAL ACADEMIES` to the near sheet's
    corner, each a world-coordinate polyline declared in `window.__akLeaders`
    with `at`, `to`, `from` and `label`, terminating on the sheet's own
    coordinates. Weights, hair 0.75 for the floor grid, fine 1.25 for the
    leaders, std 2 for a sheet outline that was read.

11a. **Wordless claim.** Two sheets, not one and not many. `reads: "differ"`
    between the near sheet's lit face and the fog behind it.

### D. VERIFICATION

12. **Reference intent.** An evidence table photographed before anyone touched it.
13. **Risk flags.** A leader landing in void, mitigated by declaring both in
    `window.__akLeaders` with named targets and labels that are byte-identical
    to rendered DOM strings. Body copy over the weave, mitigated by keeping all
    body text above y 620 in the fog zone where local contrast is highest.
14. **Acceptance checklist.**
    - [ ] Exactly two sheets, both blank, both solid-outlined, both stamped READ.
    - [ ] Both leaders terminate on their sheet's own corner, within 24 px.
    - [ ] Both leader labels appear as rendered text within 32 px of arrival.
    - [ ] The guard chip is fully inside its measured plate.
    - [ ] The body sets 30 to 40 characters per line.
    - [ ] The only gold is the grille spill on the floor.
    - [ ] The DUE field contains no digit.

---

## SLIDE 03 — THE DATE IS NOT ON THE FLOOR

### A. NARRATIVE

1. **Beat.** The turn. The deck asks the obvious next question and the record
   refuses to answer it. Inherits "owed by when". Plants: then what IS on the
   record.
2. **Copy, final.**
   - kicker, mono 24 px: `03 / 09 / OWED BY WHEN`
   - headline, Unbounded 600, fit 76 to 112, maxLines 2, 7 words:
     `The due date / is not on the record.`
   - body, Manrope 500, 34 px, 44 words:
     `The text of S. 5171 returned a 403 on August 15th, so no deadline for the
     plan or for the study could be read. The committee's own meeting page
     carries the agenda and no tally, no roll call and no recorded result for
     any of the five bills.` [C37, C11]
   - dimension call value, mono 22 px: `NO TALLY PUBLISHED` [C11]
   - sheet stamps: `403 AUG 15 2026` [C37], `NOT PUBLISHED` [C11]
   - DUE field empty, counter `03 / 09`
3. **Reader takeaway.** Nobody can say when the plan is due or by what margin
   the bill advanced.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 8 rows 1 to 2. Body cols 1 to 6 rows 3 to
   4. A phantom-dashed 403 sheet cols 6 to 11 rows 5 to 6. A phantom-dashed
   NOT PUBLISHED sheet cols 2 to 7 rows 6 to 8, nearer. The dimension call runs
   between the two, extension lines and 3:1 arrowheads fully drawn, and where
   the numeral belongs it prints `NO TALLY PUBLISHED`. Focal point is the empty
   dimension at (0.46 W, 0.66 H).

4a. **Lower-third treatment.** The near phantom sheet lies across the whole
   bottom band in perspective with its own soft cast shadow on the weave, and
   the dimension call's extension lines run DOWN into the band and terminate on
   the sheet's own edges rather than floating above it. Behind and between
   them the lit carpet fibre carries the raking key with real directional
   variance, and the toy's grille spill rakes in from frame left across the
   near sheet's corner. This is the deck's densest lower band by design,
   because it is the slide where the absence has to feel like a measured thing
   rather than a mood.

5. **Depth plan.** Same six cues. Camera pos (2.30, 0.22, 2.35), pitch -4,
   fov 52. The two sheets sit at world z 0.9 and 1.9 so the scale gradient
   between them is a real 2.1 to 1.
6. **Continuity device state.** `data-camx="2.30"`. One 403 sheet, one
   unpublished sheet. DUE empty, and this is the slide where the DUE field is
   directly under the dimension call so the two absences rhyme.

### C. ART DIRECTION

7. **Technique stack.** akthree floor and sheets. Dimension Call (#73) with
   extension lines at a 4 px gap and 6 px overshoot, 3:1 arrowheads about 10 x
   3.3 px, drawn in SVG above the composite so the gates can see them.
   Alphabet-of-Lines dash kit (#67), phantom `30 5 6 5 6 5` at fine 1.25 px.
   Seed 20260818.
8. **Data-in-art mapping.** The dimension call spans the exact distance between
   the two sheets and prints no number, which is the slide's whole argument.
   Nothing else on this slide encodes a quantity.
9. **Palette assignment.** As the deck table. Phantom `#3F5B78` for both sheet
   outlines and for the dimension apparatus. No solid outline appears on this
   slide at all, which is itself the signal.
10. **Type spec.** Headline Unbounded 600, fit 76 to 112. Body Manrope 500,
    34 px. Dimension value JetBrains Mono 700, 22 px, tracking +12%, `#8FB6E8`,
    on a measured `AK.svgPlate` knockout so the extension lines never cross the
    letterforms.
11. **Iconography and anchor spec.** Anchor is the dimension call. The
    apparatus of measurement is drawn completely and measures nothing.

11a. **Wordless claim.** A fully drawn dimension with an empty value reads as a
    measurement that was attempted, not as decoration. `reads: "differ"` between
    the lit near sheet and the unlit gap the dimension spans.

### D. VERIFICATION

12. **Reference intent.** An engineering drawing with the number left off.
13. **Risk flags.** The dimension apparatus crossing the value's glyphs,
    mitigated by the measured `AK.svgPlate` knockout under the value. Phantom
    dashes disappearing at 432 px, mitigated by the 1.25 px weight being
    doubled at 2x backing and by the outline being long enough that at least
    six dash periods are visible at feed scale.
14. **Acceptance checklist.**
    - [ ] The dimension call has extension lines, both arrowheads and no number.
    - [ ] The value plate is fully under the string and no rule crosses a glyph.
    - [ ] Both sheets are phantom dashed and neither is solid.
    - [ ] The dimension's extension lines terminate ON the sheet edges.
    - [ ] The DUE field sits directly below the dimension call.
    - [ ] The DUE field contains no digit.
    - [ ] The near sheet's shadow reads at 432 px.

---

## SLIDE 04 — THE AGENDA (keepable)

### A. NARRATIVE

1. **Beat.** The keepable artifact. Everything the committee did that morning,
   in one table a reader can screenshot. Inherits "what IS on the record".
   Plants: why any of this now.
2. **Copy, final.**
   - kicker, mono 24 px: `04 / 09 / EXECUTIVE SESSION 24`
   - headline, Unbounded 600, fit 68 to 96, maxLines 2, 8 words:
     `Five bills that morning. / Three of them AI.` [C03, C09]
   - table, JetBrains Mono 26 px tabular, five rows, three marked:
     `S. 737     SCREEN ACT` [C04]
     `S. 1748    KIDS ONLINE SAFETY ACT` [C05]
     `S. 4199    YOUTH AI PRIVACY ACT` [C06]
     `S. 4407    CHATBOT ACT` [C07]
     `S. 5171    CHILDREN'S AI TOY SAFETY ACT OF 2026` [C08]
   - result column, all five rows, mono 22 px: `NO TALLY PUBLISHED` [C11]
   - flat count, mono 28 px: `3 OF 5` [C09]
   - footer line, Manrope 500, 30 px, 33 words:
     `The committee met at 10:00 a.m. on August 5th in room SR-253, entering
     through SR-254. Three Coast Guard nomination lists were on the same
     agenda. Senator Duckworth's office announced that day that S. 5171
     passed.` [C01, C02, C10, C12]
   - DUE field empty, counter `04 / 09`
3. **Reader takeaway.** Three of the five bills the committee took up that
   morning were about AI, and none of the five has a published result.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 8 rows 1 to 2. Table cols 1 to 11 rows 3
   to 6, left-aligned on the bill numbers with tabular figures so the columns
   are true. `3 OF 5` set large in cols 10 to 12 row 2. Footer cols 1 to 9 row
   7 to 8. Focal point is the S. 5171 row at (0.35 W, 0.58 H).

4a. **Lower-third treatment.** Five blank sheets lying on the floor in a
   receding row directly under the table, one per bill, three of them catching
   the toy's warm grille spill and two falling into the cold key only, so the
   three-of-five count is carried by LIGHT as well as by the printed mark. Each
   sheet has its own soft contact shadow and the row's scale gradient runs a
   real 2.4 to 1 from the near sheet to the far one. The carpet weave runs
   between and behind them under the raking key, and the toy's own body enters
   the band at frame right as a warm silhouette against fog, so the bottom band
   holds rendered mass, cast shadow and a graded ground rather than furniture.

5. **Depth plan.** Camera pos (3.45, 0.22, 2.35), pitch -4, fov 52. Six cues as
   before, with the sheet row doing the scale-gradient work explicitly at
   0.72^i spacing.
6. **Continuity device state.** `data-camx="3.45"`. One READ sheet (the
   sponsor's release, near right) and one unpublished sheet (the result). DUE
   empty.

### C. ART DIRECTION

7. **Technique stack.** akthree floor and sheets. The table itself is SVG text
   above the composite, with `AK.svgPlateAll` measured knockouts on every row
   so no weave shows through a glyph. Scotch Rule (#70) under the header, 4 px
   rule, 3 px gap, 0.75 px hairline. Seed 20260819.
8. **Data-in-art mapping.** Five sheets for five bills. Three lit by the warm
   spill for the three carrying AI in their titles [C09]. The row spacing is
   0.72^i, which is the doctrine's scale gradient, not a story number, and the
   dossier says so rather than inventing a mapping.
9. **Palette assignment.** As the deck table. The three lit sheets take
   `#FFC72C` at 0.08 alpha as a spill, which is a reflection of the machine's
   voice and therefore inside the gold rule.
10. **Type spec.** Table JetBrains Mono 400 for numbers and 700 for titles,
    26 px, tabular lining numerals, tracking +6%, `#DDE6EF` on measured plates.
    Result column JetBrains Mono 400, 22 px, `#7E93A8`. `3 OF 5` JetBrains Mono
    700, 28 px, `#8FB6E8`. Footer Manrope 500, 30 px, `#C4D2DE`.
11. **Iconography and anchor spec.** Anchor is the sheet row. Annotation
    furniture is the scotch rule and the result column's blunt-cap terminals.
    One leader from `S. 5171` in the table to the near-right READ sheet's own
    corner, declared with target, at, to, from and label.

11a. **Wordless claim.** Three of five sheets carry warm light and two do not,
    at feed scale. `reads: "differ"` between a lit sheet's face and an unlit
    sheet's face.

### D. VERIFICATION

12. **Reference intent.** A committee calendar page, reprinted honestly.
13. **Risk flags.** Tiny text, since the table is the deck's smallest type.
    Mitigated by setting the deck's small-label floor at 26 px rather than the
    engine's 24 px warn line, so a label has to be two points under budget
    before it can warn. Table columns drifting, mitigated by tabular lining
    numerals and by measuring every plate from the string.
14. **Acceptance checklist.**
    - [ ] All five bill numbers and titles are transcribable at full size.
    - [ ] Exactly three rows are marked as AI bills and `3 OF 5` is printed flat.
    - [ ] The result column reads NO TALLY PUBLISHED on all five rows.
    - [ ] Exactly five sheets lie in the row and three carry warm spill.
    - [ ] Every table label sits inside its measured plate.
    - [ ] No table type is under 26 px.
    - [ ] The DUE field contains no digit.

---

## SLIDE 05 — WHAT THE SPONSORS SAY THE TOYS DID

### A. NARRATIVE

1. **Beat.** The only slide where the deck lets the subject be frightening, and
   it does it entirely in other people's words. Inherits "why now". Plants:
   where does the Alaskan stand.
2. **Copy, final.**
   - kicker, mono 24 px: `05 / 09 / WHY NOW`
   - headline, Unbounded 600, fit 84 to 118, maxLines 2, 4 words:
     `Knives, pills / and matches.` [C24]
   - quotation, Manrope 600, 38 px, the deck's largest quotation:
     `"discussing sexually explicit content and explaining where to find
     knives, pills and matches in the home"` [C24]
   - attribution, mono 20 px:
     `SEN. DUCKWORTH'S OFFICE, CITING U.S. PIRG EDUCATION FUND TESTING,
     DECEMBER 2025` [C24]
   - second quotation, Manrope 500, 34 px:
     `"These AI chatbots were never meant to be used by young children, yet
     they're being embedded inside toys by the thousands"` [C21]
   - attribution, mono 20 px: `SEN. TAMMY DUCKWORTH, AUGUST 5, 2026` [C21]
   - guard, mono 20 px on a measured plate:
     `THOUSANDS IS THE SENATOR'S WORD AND CARRIES NO CITED COUNT` [C21]
   - sheet stamps: `READ AUG 15 2026` [C24], `403 AUG 15 2026` [C38]
   - DUE field empty, counter `05 / 09`
3. **Reader takeaway.** The reason this bill exists is testing that found toys
   telling children where the knives are.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 7 rows 1 to 2. Large quotation cols 1 to
   8 rows 3 to 4. Second quotation cols 1 to 7 rows 5 to 6. The toy is nearest
   here, cols 7 to 12 rows 4 to 8, grille hottest. Focal point is the grille at
   (0.74 W, 0.63 H). Guard chip cols 1 to 6 row 8.

4a. **Lower-third treatment.** The toy at its closest and largest in the deck,
   its body filling the lower right of the frame with the grille's warm
   emissive throwing a real pool onto the weave and a two-part contact shadow
   spreading toward the lens. To the left of it a blank READ sheet and a blank
   phantom-dashed 403 sheet lie side by side on the lit carpet, the pair of
   them carrying the slide's sourcing without a word of caption. The fibre
   direction is at its most visible here because the grille is a second, low,
   warm source raking across the weave from the opposite side to the key.

5. **Depth plan.** Camera pos (4.60, 0.22, 2.35), pitch -4, fov 52, and the toy
   is at world z 0.55, its nearest position in the deck. Six cues, with the
   grille as a genuine second light source so the contact shadow is two-part by
   physics rather than by drawing.
6. **Continuity device state.** `data-camx="4.60"`. One READ sheet, one 403
   sheet. DUE empty.

### C. ART DIRECTION

7. **Technique stack.** akthree, the toy at full scale with the emissive ring
   at intensity 2.6, which is the deck's peak. akpost grade before composite,
   bloom strength raised to 0.36 on this slide only, which is declared here so
   the pixel critics can check it against the other eight. Seed 20260820.
8. **Data-in-art mapping.** None on this slide, deliberately. It is the one
   slide carrying no quantity at all, so nothing can be misread as a magnitude.
   The dossier states this rather than leaving it to be discovered.
9. **Palette assignment.** As the deck table, with the grille emissive at its
   maximum. Worst-case text contrast is the second quotation over the warm
   pool's outer edge, estimated 7.9 to 1.
10. **Type spec.** Headline Unbounded 600, fit 84 to 118. Large quotation
    Manrope 600, 38 px, leading 1.32, measure 34 characters, `#F4F8FF`, straight
    quotes. Second quotation Manrope 500, 34 px, `#DDE6EF`. Attributions and
    guard JetBrains Mono 700, 20 px, tracking +10%, on measured plates.
11. **Iconography and anchor spec.** Anchor is the toy. No leaders; the
    quotations are the annotation.

11a. **Wordless claim.** The grille is a light source on this slide, not a
    detail, and the warmth on the carpet comes from the machine rather than
    from the room. `reads: "differ"` between the carpet inside the grille pool
    and the carpet outside it.

### D. VERIFICATION

12. **Reference intent.** A still life lit by the thing that is the problem.
13. **Risk flags.** The slide reading as alarmist. Mitigated structurally, since
    every frightening string on it is a quotation with a named speaker and a
    printed guard saying "thousands" carries no cited count, and the deck's own
    voice says nothing here. Bloom blowing out the grille, mitigated by
    declaring the raised bloom in this dossier and checking the grille's rings
    are still individually resolvable at full size.
14. **Acceptance checklist.**
    - [ ] Both quotations are verbatim and use straight quotes.
    - [ ] Each quotation carries a visible named attribution.
    - [ ] The "thousands" guard chip is present and fully on its plate.
    - [ ] The grille's three concentric rings are individually resolvable.
    - [ ] Exactly two sheets, one solid READ and one phantom 403.
    - [ ] No number appears anywhere on this slide.
    - [ ] The DUE field contains no digit.

---

## SLIDE 06 — THE ALASKAN'S CASE

### A. NARRATIVE

1. **Beat.** The fair reading, and the Alaska anchor. This is the slide where
   the deck argues FOR the bill. Inherits "where does the Alaskan stand".
   Plants: is buying knowledge enough.
2. **Copy, final.**
   - kicker, mono 24 px: `06 / 09 / THE ALASKAN ON THE BILL`
   - headline, Unbounded 500, fit 72 to 100, maxLines 2, 8 words:
     `The Alaskan on the bill / is buying knowledge.`
   - quotation, Manrope 600, 36 px:
     `"It is imperative we equip policymakers and America's families with the
     knowledge they need to make informed choices about these devices"` [C20]
   - attribution, mono 20 px: `SEN. LISA MURKOWSKI, ALASKA, AUGUST 5, 2026`
     [C20]
   - body, Manrope 500, 34 px, 40 words:
     `Murkowski is the Republican cosponsor named in the announcement. Reading
     the bill fairly, it buys knowledge and writes no rule, which is the normal
     opening move for a technology nobody has measured yet. The question is
     whether that is enough.` [C14, C17]
   - DUE field empty, counter `06 / 09`
3. **Reader takeaway.** Alaska's senator is on a bill that buys knowledge
   rather than writing a rule, and that is a defensible thing to do.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 8 rows 1 to 2. Quotation cols 1 to 8 rows
   3 to 5. Body cols 1 to 7 rows 6 to 7. One READ sheet cols 7 to 12 rows 6 to
   8. The toy sits far back at cols 3 to 5 row 5, small, its grille still the
   only warm point. Focal point is the quotation's first line at (0.30 W,
   0.42 H).

4a. **Lower-third treatment.** A single blank READ sheet lying near and large at
   frame right, its lit face and soft cast shadow anchoring the corner, with
   the carpet running back from it into fog under the raking key. The body copy
   sits on the graded weave rather than on a plate, because at this camera
   position the fog has lifted the local luminance enough to carry it, and the
   toy's grille throws one narrow warm streak across the near weave from
   mid-frame. The band's mass is the sheet and the modelled floor together; the
   type is a guest on it and not the thing filling it.

5. **Depth plan.** Camera pos (5.75, 0.22, 2.35), pitch -4, fov 52. The toy
   retreats to world z 3.4, its farthest position other than the breather, so
   the deck's scale gradient across slides 05 to 07 is a real recession.
6. **Continuity device state.** `data-camx="5.75"`. One READ sheet. DUE empty.

### C. ART DIRECTION

7. **Technique stack.** akthree floor, sheet and toy. akpost grade before
   composite, house numbers. Seed 20260821.
8. **Data-in-art mapping.** None. This slide carries no quantity, stated
   deliberately as on slide 05.
9. **Palette assignment.** As the deck table. This is the coolest slide in the
   deck by design, with the warm streak reduced to about 4 percent of frame
   area, because the argument here is the reasonable one.
10. **Type spec.** Headline Unbounded 500, fit 72 to 100. Quotation Manrope
    600, 36 px, leading 1.34, measure 36 characters. Body Manrope 500, 34 px,
    `#C4D2DE`. Attribution JetBrains Mono 700, 20 px on a measured plate.
11. **Iconography and anchor spec.** Anchor is the READ sheet. One leader from
    the attribution to the sheet's own near corner, declared with target, at,
    to, from and label.

11a. **Wordless claim.** The toy is small and far here and the paper is near and
    large, which is the slide's argument about what this bill actually moves.
    `reads: "differ"` between the near sheet's lit face and the far toy's body.

### D. VERIFICATION

12. **Reference intent.** A committee room from the back row.
13. **Risk flags.** Body copy directly on the weave without a plate. Mitigated
    by measuring the worst-case contrast in the render and adding a scrim only
    if it falls under 4.5 to 1, never by default. If it needs a scrim it gets a
    graded one, not a rectangle.
14. **Acceptance checklist.**
    - [ ] The Murkowski quotation is verbatim with straight quotes.
    - [ ] Murkowski is identified as Alaska's senator and as a cosponsor.
    - [ ] The body says plainly that the bill writes no rule.
    - [ ] The leader lands on the sheet's own corner within 24 px.
    - [ ] Body copy over the weave measures at least 4.5 to 1 at its worst point.
    - [ ] The toy is visibly smaller here than on slide 05.
    - [ ] The DUE field contains no digit.

---

## SLIDE 07 — BREATHER

### A. NARRATIVE

1. **Beat.** BREATHER. The deck has just spent two slides on other people's
   words and is about to spend one on a different jurisdiction, so the reader
   needs one frame that holds a single sentence and nothing else. Inherits "is
   buying knowledge enough". Plants: what does Alaska already have.
2. **Copy, final.**
   - headline, Unbounded 600, fit 96 to 132, maxLines 3, 10 words:
     `A plan is not a rule. / A study is not a standard.` [C17]
   - counter, mono 24 px: `07 / 09`
   - DUE field empty
3. **Reader takeaway.** Nothing has been decided yet.

### B. COMPOSITION

4. **Layout map.** The sentence occupies cols 1 to 9 rows 2 to 4, optical-left.
   Everything else is floor. Focal point is the second line's first word at
   (0.14 W, 0.34 H). The quiet zone is cols 10 to 12, about one sixth of the
   frame.

4a. **Lower-third treatment.** BREATHER. The deck needs a rest here because
   slides 05 and 06 are both quotation-dense and slide 08 is a four-row
   attributed block, so three consecutive text-heavy frames would flatten the
   swipe. The band is still not empty. It carries the full width of the carpet
   in raking key light with its fibre direction fully resolved, the toy's
   silhouette small and far at frame right against exp2 fog, and one long
   two-part shadow running from it toward the lens. The rest is in the TYPE
   count, not in the rendering, which is why `data-breather` is set on the body
   and this dossier declares it.

5. **Depth plan.** Camera pos (6.90, 0.22, 2.35), pitch -4, fov 52. The toy is
   at world z 5.2, its farthest in the deck, and the fog is at its heaviest so
   the recession reads as distance rather than as smallness.
6. **Continuity device state.** `data-camx="6.90"`. No sheets, the only slide
   with none, which is itself the rest. DUE empty.

### C. ART DIRECTION

7. **Technique stack.** akthree floor and toy. akpost grade before composite,
   with vignette raised to 0.26 on this slide only, declared here. Seed
   20260822.
8. **Data-in-art mapping.** None. It is the breather.
9. **Palette assignment.** As the deck table, at its darkest. The grille is a
   single warm pixel cluster at this distance and remains the deck's only gold.
10. **Type spec.** Headline Unbounded 600, fit 96 to 132, leading 1.0, tracking
    -2%, `#F4F8FF`, max width 860 px.
11. **Iconography and anchor spec.** Anchor is the toy's distant silhouette. No
    annotation furniture on this slide except the DUE field and the counter.

11a. **Wordless claim.** none, because this is the breather and the sentence is
    the whole slide.

### D. VERIFICATION

12. **Reference intent.** A dark room with one thing left in it.
13. **Risk flags.** The frame reading as empty rather than as a rest, mitigated
    by the fully resolved weave and the long cast shadow, both of which are
    rendered mass. `AK.fitText` at maxLines 3 with min 96 keeps the sentence
    from collapsing to a size that reads as a caption.
14. **Acceptance checklist.**
    - [ ] `data-breather` is set on the body and this dossier declares it.
    - [ ] The sentence sets in 3 lines or fewer at 96 px or larger.
    - [ ] The carpet weave is resolved across the full width of the bottom band.
    - [ ] The toy is visible and is the smallest it appears in the deck.
    - [ ] No sheet appears on this slide.
    - [ ] The DUE field contains no digit.

---

## SLIDE 08 — ALASKA'S RECORD, ATTRIBUTED

### A. NARRATIVE

1. **Beat.** What Alaska already has, stated only as one named column states it,
   with the attribution physically inseparable from the claims. Inherits "what
   does Alaska already have". Plants: what is a reader supposed to do.
2. **Copy, final.**
   - kicker, mono 24 px: `08 / 09 / ALASKA'S OWN RECORD`
   - headline, Unbounded 500, fit 68 to 94, maxLines 2, 8 words:
     `Alaska's own record, / as one column tells it.`
   - four rows inside ONE bracket, Manrope 500, 32 px:
     `House Bill 47 provisions criminalizing AI-generated child sexual abuse
     material and deepfake harassment became law in June.` [C31]
     `House Concurrent Resolution 3 would have created an AI task force. That
     effort stalled.` [C32, C33]
     `Roughly 30 states have passed election-related deepfake disclosure laws.`
     [C34]
     `Some states now require companion chatbots to disclose that they aren't
     human or therapists.` [C35]
   - bracket stamp, mono 20 px, on the bracket itself:
     `PER ADN OPINION COLUMN, ROGER KAYE, AUGUST 10TH` [C29, C30]
   - guard line, mono 20 px on a measured plate:
     `THIS DECK MAKES NO CLAIM ABOUT WHAT ALASKA LAW COVERS ON AI TOYS`
   - sheet stamp: `READ AUG 15 2026` [C29]
   - DUE field empty, counter `08 / 09`
3. **Reader takeaway.** Alaska has one AI crime law and a stalled task force,
   according to one opinion column, and this deck says nothing beyond that.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 8 rows 1 to 2. The bracket runs cols 1 to
   10 rows 3 to 6, a single drawn bracket enclosing all four rows with the
   stamp set into its lower arm. Guard line cols 1 to 8 row 7. One READ sheet
   cols 8 to 12 rows 6 to 8. Focal point is the bracket's lower arm at (0.20 W,
   0.60 H).

4a. **Lower-third treatment.** The bracket's lower arm and its attribution stamp
   run down into the band and terminate on the near READ sheet's own corner, so
   the annotation furniture is structural rather than floating, and the sheet
   itself is a lit rendered plane with a soft cast shadow occupying the right
   third of the band. Between them the carpet is at its most steeply raked, the
   fibre catching the key across the full width, and the toy's grille throws a
   thin warm reflection along the sheet's near edge. The band therefore holds a
   rendered object, a modelled ground and a shadow, and the type sits above it.

5. **Depth plan.** Camera pos (8.05, 0.22, 2.35), pitch -4, fov 52. The toy
   returns to world z 2.6, mid-distance, so the deck's last two content slides
   bring it back toward the reader before the close.
6. **Continuity device state.** `data-camx="8.05"`. One READ sheet, the column
   itself. DUE empty.

### C. ART DIRECTION

7. **Technique stack.** akthree floor, sheet and toy. The bracket is SVG,
   drawn at bold 3.5 px, with the stamp on a measured `AK.svgPlate` knockout
   set into the lower arm. Seed 20260823.
8. **Data-in-art mapping.** The bracket's height is a function of the four rows'
   measured bounding box, not a typed constant, so it cannot disagree with the
   text it encloses. `window.__akAssert` declares that the bracket's drawn
   height equals the measured block height within 2 px.
9. **Palette assignment.** As the deck table. The bracket and stamp are
   `#8FB6E8`, the hallway blue, which is the deck's colour for a thing that
   came from outside the room.
10. **Type spec.** Headline Unbounded 500, fit 68 to 94. Rows Manrope 500,
    32 px, leading 1.36, measure 38 characters, `#DDE6EF`. Bracket stamp and
    guard JetBrains Mono 700, 20 px, tracking +10%, on measured plates.
11. **Iconography and anchor spec.** Anchor is the bracket. Annotation furniture
    is the bracket's arms and one leader from the stamp to the READ sheet's own
    corner, declared with target, at, to, from and label.

11a. **Wordless claim.** All four Alaska lines are physically inside one drawn
    bracket carrying one attribution, so a screenshot of any part of the block
    carries the source with it. `reads: "differ"` between the bracket's stroke
    and the carpet immediately outside it.

### D. VERIFICATION

12. **Reference intent.** A pull quote from a single named source, fenced.
13. **Risk flags.** The four rows reading as this page's own findings. Mitigated
    structurally by the bracket, by the stamp set INTO the bracket rather than
    beside it, and by the printed guard line. The bracket disagreeing with the
    block it encloses, mitigated by deriving its height from `getBBox` and
    asserting it in `window.__akAssert`.
14. **Acceptance checklist.**
    - [ ] All four rows sit inside one continuous drawn bracket.
    - [ ] The attribution stamp is set into the bracket, not floating beside it.
    - [ ] The guard line is present and fully on its plate.
    - [ ] No row states an Alaska fact as this page's own finding.
    - [ ] The bracket height matches the measured block within 2 px.
    - [ ] The leader lands on the sheet's own corner within 24 px.
    - [ ] The DUE field contains no digit.

---

## SLIDE 09 — CLOSE

### A. NARRATIVE

1. **Beat.** One ask, the brand fixtures, and the deck's last look at the floor.
   Inherits "what is a reader supposed to do". Plants nothing; it closes.
2. **Copy, final.**
   - headline, Unbounded 600, fit 76 to 108, maxLines 2, 9 words:
     `Five places the record / was asked. One answered.` [C11, C27, C28, C37, C38]
   - the ask, Manrope 600, 36 px, one ask and only one:
     `Save this for the next time a talking toy shows up in your house.`
   - source note, mono 22 px: `SOURCES IN COMMENTS`
   - wordmark, Unbounded 700, 40 px: `ALASKA.AI`
   - site, mono 22 px, near the wordmark: `alaskaaihq.com`
   - DUE field empty, counter `09 / 09`
3. **Reader takeaway.** Save it, and check back when the plan appears.

### B. COMPOSITION

4. **Layout map.** Headline cols 1 to 8 rows 1 to 2. The ask cols 1 to 7 rows 3
   to 4. Wordmark and site bottom left at row 8, Polaris above the wordmark.
   Source note bottom centre row 8. Five sheets trail back across cols 4 to 12
   rows 4 to 7, two solid READ and three phantom. Focal point is the nearest
   READ sheet at (0.52 W, 0.60 H).

4a. **Lower-third treatment.** The full trail of five blank sheets receding into
   fog occupies the band, each one a lit rendered plane with its own soft cast
   shadow on the weave, the two solid-outlined ones nearest and the three
   phantom ones falling away. The toy returns near at frame right with its
   grille pool warming the near weave and its two-part contact shadow reaching
   toward the lens. The carpet fibre is fully resolved across the band under
   the raking key. This is the deck's widest and deepest lower band and it is
   built entirely from rendered mass, shadow and graded ground.

5. **Depth plan.** Camera pos (9.20, 0.22, 2.35), pitch -4, fov 52, and this is
   the only slide where the camera also rises, to 0.34 m, so the close pulls
   back and up and the whole floor is seen at once. The rise is the deck's one
   permitted departure from the fixed-height rule and it is declared here.
6. **Continuity device state.** `data-camx="9.20"`. The trail is five sheets,
   two of them 403 and three of them NOT PUBLISHED, and one further solid READ
   sheet stands apart at frame right. Five asked, one answered, matching the
   headline. DUE empty, for the last time, which is the argument's final beat.

### C. ART DIRECTION

7. **Technique stack.** akthree floor, sheets and toy. Polaris is a DOM/SVG
   four-point gold star so the grade never shifts the brand mark. akpost grade
   before composite, house numbers. Seed 20260824.
8. **Data-in-art mapping.** FIVE sheets for the five places this deck asked
   the record a question it could not answer, and exactly ONE of them carries
   the solid outline that means an answer came back. Near to far, the states
   are READ (the tally, asked of the committee page) is not available, so the
   five are, near to far, NOT PUBLISHED for the committee tally [C11], 403 for
   the bill text [C37], NOT PUBLISHED for the CPSC index [C27], NOT PUBLISHED
   for the FTC index [C28], and 403 for the PIRG report [C38]. The single solid
   READ sheet is the sponsor's release [C12], set apart from the trail at
   frame right, and it is the one that answered. The count in the headline is
   declared in `aggregates.json` and re-derived at the Phase 8 aggregate gate.
9. **Palette assignment.** As the deck table, plus `#FFC72C` on the Polaris and
   the wordmark rule, which is the constellation fixture and the one place gold
   means something other than the machine's voice. This is stated here so the
   falsifiable palette claim is scoped to slides 01 through 08.
10. **Type spec.** Headline Unbounded 600, fit 76 to 108. Ask Manrope 600,
    36 px, `#F4F8FF`. Wordmark Unbounded 700, 40 px, tracking +12%. Site and
    source note JetBrains Mono 400, 22 px, `#7E93A8`.
11. **Iconography and anchor spec.** Anchor is the sheet trail. The Polaris is
    the fixed constellation glyph. No leaders.

11a. **Wordless claim.** Two solid outlines and three dashed ones, at feed
    scale, is the deck's sourcing stated as a picture. `reads: "differ"` between
    a solid sheet's outline and a phantom sheet's outline.

### D. VERIFICATION

12. **Reference intent.** The last frame of a single take, pulling back.
13. **Risk flags.** The close carrying more than one ask, mitigated by the
    dossier fixing exactly one and the acceptance checklist counting them. The
    headline's count disagreeing with the sheets, mitigated by declaring it in
    `aggregates.json` and re-deriving it at the aggregate gate.
14. **Acceptance checklist.**
    - [ ] Exactly one ask appears, and it is the save.
    - [ ] `SOURCES IN COMMENTS` is present.
    - [ ] `alaskaaihq.com` is set small in the mono face near the wordmark.
    - [ ] The Polaris appears once and is gold.
    - [ ] Six sheets are visible, five in the trail and one solid READ apart.
    - [ ] The headline's count matches the declared aggregate.
    - [ ] The DUE field contains no digit, on the last slide as on the first.

## GATE STATUS, generated by scripts/gate_status.py --sync

```
GATE STATUS -- generated by scripts/gate_status.py from the artifacts in out/2026-08-15. Do not hand-write these lines.
[PASS] render         9/9 slides OK, 0 page errors, 0 overflow warnings
[WARN] qa.py          WARN, 0 fails, 2 warns
[PASS] dossier_check  PASS, 9 dossiers, 0 fails, 0 warns
[PASS] caption_check  PASS, 877 chars, hook 124, 3 hashtags
[PASS] copy_sync      copy_sync_check: PASS -- 72 authored slide strings all present in the render
[PASS] aggregate      aggregate_check: PASS -- 7 aggregate assertion(s) detected, 7 declared -> out/2026-08-15/aggregate_report.json
[PASS] bespoke        bespoke_check: WARN -- 9 slides, median pairwise art similarity 0.368 (fail at 0.60), max pair 0.696, drawn share 72% (158 drawn vs 62 block
[PASS] scanner_sync   the live scan page still matches the routine contract
[PASS] docket_dates   docket dates clean at 2026-08-15: 269 assertions over 6 fixtures and 20 ledger items
[PASS] gas_watch      11 day(s) on record, 11 verified, no gaps, latest 2026-08-15, EIA through 202605 over 131 months, model misses by 6.82%
[PASS] site_fresh     OK: docs/ is exactly a fresh build at --date 2026-08-15 (133 generated files)
[PASS] assemble       9 slides, pdf vector 4.63 MB, 9 thumbs
[WARN] score          ? / 10 vs threshold 8.3, scorer says passes=False
[PASS] artifacts      every named artifact present, JSON parses, 9 slides valid
>> 0 FAIL row(s). Paste this block verbatim into the run record.
```

