# STORYBOARD — Carousel No. 9 — 2026-07-16
## "First You Spend the Land" (working title / PDF document title)

## DECK HEADER

**Thesis (one sentence).** Alaska is being asked to build the ground for a
data-center boom it does not yet have, and the first thing spent is not
power or water but public land, handed to the state's own developer for
free, purpose to be decided later.

**PDF document title (<= 60 chars):** "First You Spend the Land. Then You Decide What For."
(51 chars incl. spaces; fallback short title "First You Spend the Land").

**Arc (9 slides, one line each).**
1. COVER, position stated over an empty warm plat (hook).
2. THE DEAL, seller and buyer are the same government, $0, no bid (pays slide 1).
3. PURPOSE IS A WORD, 41 pages name uses that are only listed (Ruaro quote).
4. THE BOOM WE DO NOT HAVE, 8 vs 639 ISOTYPE (breather + keepable data).
5. ONE CELL, the biggest real proposal fills 1 of 31 squares (scale).
6. THE TOWN PULLS THE OTHER WAY, Houston ban vote + 6 to 1 override.
7. SIX DAYS APART, Aug 13 ban vote vs Aug 19 comment close (keepable, gold peak).
8. THE ORDER IS THE ARGUMENT, every deed field filled but USE (synthesis).
9. CLOSE, hand the blank to the reader, one debate question.
Emotional temperature: cool-analytic (1 to 3), warms to indictment at 7
(the gold collision), resolves to a direct challenge at 9.

**Slide-count rationale.** 9 slides = 1 cover + 7 content + 1 close, inside
the 8 to 10 default; the argument has exactly seven evidentiary beats (deal,
purpose, boom, scale, town, collision, order) and collapses below that.

**Continuity system (3 devices, all fresh vs the last 2 decks).**
- DEVICE A, THE UNIT-SQUARE PLAT (motif evolution + progress). A 2:1
  dimetric land slab of 30 solid + 1 dashed unit cells recurs as the deck
  chassis; its state changes per slide. STATE TABLE:
  - S1 empty plat, one faint ghost pad, USE blank.
  - S2 empty plat under a $0 / NO BID deed stamp.
  - S3 cells wear floating use-labels; still empty; ghost pads dashed.
  - S4 the SAME unit cell becomes the ISOTYPE mark (8 amber vs 639 grey).
  - S5 exactly ONE cell occupied and extruded (STAK), 30 empty.
  - S6 the plat crossed by a Houston BAN barrier; a 6 to 1 tally.
  - S7 plat recedes/dims; two lit date-cells on a timeline strip.
  - S8 the deed ledger fully filled, USE line blank and largest.
  - S9 full quiet plat, one amber "you are here" cell, USE becomes an open
    field with a gold caret.
- DEVICE B, THE USE: ____ BLANK TRUTH-LINE (motif + argument). A ruled deed
  line labeled USE stays permanently blank while every other field fills;
  appears on S1, S2, S3, S8, S9. On S9 it becomes the reader's open field.
- DEVICE C, THE CORRIDOR EDGE-TEASE (swipe cue). The doubled rail (dashed) +
  Parks Highway (solid) corridor is cut by the right frame edge on S1, S3,
  S5, S7 and completes on the next slide; resolves into the plat on S9.

**Variety-ledger check (required divergence, from ledger/artwork.json).**
Last 4 hero structures = autonomy-ring, FIRM/SOFT type-weight ledger,
fixed-y waterline cross-section, uncomputed relief survey-plate. THIS deck =
a 2:1 DIMETRIC UNIT-SQUARE LAND PLAT (Cabinet Extrusion #39 + ISOTYPE #28 +
#38 dimetric lighting + #67 phantom dashes), none of the four. Atmosphere =
WARM-GROUND loam (last 3 were cool drafting-blueprint, sonar-navy,
graphite-bone: diverges). Continuity = plat-motif + USE-blank + corridor
edge-tease (last 2 were waterline+sonar, camera-over-relief+confidence-meter:
diverges). Hook = stated-position + permanent-blank (last 3 were big-number
monument, place-paradox, withheld-gap: diverges; the blank is PERMANENT, not
a withheld reveal). Palette = warm loam + spruce + survey-amber + reserved
gold (last 3 were blue+copper, navy+cyan, graphite+phantom+gold: diverges).
Type = Instrument Serif + Manrope + JetBrains Mono (last 2 were
Fraunces+SpaceGrotesk+JBMono, Archivo+Manrope+JBMono: diverges;
serif+sans+mono dodges the two-sans crime).

**Variance dials.** design_variance 4 (dimetric plat + deed-line conceit is
a distinct move, not a wild one); visual_density 3 (generous negative space,
the empty land IS the argument); type_temperature 5 (warmest register in the
series, an Instrument Serif warm-ground editorial deck). Distinct from r7
(4/3/4) and r8 (5/3/3).

**Palette + type system (full).**
- Base register (warm-dark, not pure black): #100C08 -> #1A130B -> #2A2015
  (loam-black, 3 elevation steps).
- Ground cell tops (real land): loam #6E5334, warmer face #8A5A3C; spruce
  vegetation accent #2F5D45. Side faces two shades darker by facing.
- Empty-cell fill #17110A; grid hairline #4A3A24.
- Survey-stake AMBER (workhorse accent): #E8973A (stamps, corridors, the 8
  Alaska marks, the 6 yes-votes, key-light warmth).
- Ghost / listed (the one cool note = un-real): bone-grey #9AA0A6, always
  DASHED (#67 phantom kit). Virginia's 639 marks dim grey-green #6B7A70.
- Text: warm snow #F4EDE1 (body on dark), max-contrast #F8F2E8 (headline).
- Shadow hue: darkened loam #241A10 (never black).
- FLAG GOLD #FFC72C, RESERVED and budgeted <= 4% area/slide, most-saturated-
  on-smallest: Polaris star (once per slide), the $0 seal (S2), the six-days
  collision peak (S7), the close caret (S9). Gold POINTS and SEALS; it never
  fills; kept deliberately distinct from the amber workhorse.
- Type: DISPLAY Instrument Serif (roman for assertions, italic for the quote/
  deferred voice), sized by AK.fitText(min,max,maxLines<=3). BODY Manrope
  variable wght 400 to 600, 28 to 42 char lines, 32px+ . INSTRUMENT JetBrains
  Mono (deed fields, stamps, dates, coordinates, counter; small-caps tracked
  +8 to 14%). Max 2 families rendered per slide (mono is the always-allowed
  third instrument voice).

**Shared plat geometry (deterministic; seed 20260716).**
- 2:1 dimetric. tileW = 130, tileH = 65. Cell (i,j) top-diamond center:
  sx = ORX + (i - j) * 65 ; sy = ORY + (i + j) * 32.5.
- Base parcel = i in 0..5, j in 0..4 (30 solid cells) PLUS one dashed
  half-cell at (i=6, j=2) hanging past the east edge = the "to 31" ambiguity.
- Slab thickness (cabinet down) = 28px on south + east faces, drawn 2 shades
  darker by facing; rows drawn BACK-TO-FRONT (j+i ascending) for free
  occlusion. ONE global warm key from upper-right; cast shadow offset
  (+18, +12) in #241A10 at 0.28 alpha.
- Ghost/listed pad on a cell = a dashed bone-grey box, top diamond offset UP
  by h = 64px, vertical dashed edges (#67), never filled solid.
- Plat raw extent: sx in [-260, +325] (~585px), sy span ~292px. Default
  ORX = 540. ORY per slide (S1 596, S2 604, S3 300 sky-reserved lower plat,
  S5 600, S6 610, S8 small-ledger). A coordinate sentinel div prints
  ORX/ORY/scale (data-decorative) on each render for QA verification.
- ISOTYPE mark (S4) = the same top-diamond at tileW 46 / tileH 23, laid in a
  parallel field (equal area preserved, so 8 vs 639 is honest).

**Claims index (claim-id -> slides).**
- C1 (30 to 31 sq mi, $0 context): S1, S2, S8.
- C2 ($0, noncompetitive): S1, S2, S8.
- C3 (scalable data centers listed): S3.
- C4 (41 pages): S3, S8.
- C5 (comment closes 5 p.m. Aug 19): S7, S9.
- C6 (Houston ban vote Aug 13): S6, S7.
- C7 (permafrost, attributed to ordinance): S6.
- C8 (8 vs 639, per Alaska's News Source): S4.
- C9 (Ruaro quote): S3.
- C10 (north of Houston, rail + Parks Hwy): S1..S9 corridor device; named S6.
- C11 (6 to 1 override, March 2026): S6, S8.
- C12 (STAK $10B+, reportedly): S5.
- C13 (STAK 1+ GW, ~30% above urban peak): S5.
- C14 (STAK ~1 sq mi): S5.
Context claims C12 to C14 hedged "reportedly / estimated"; C16/C17 (Air
Force) NOT used (kept out to protect the tight anti-No.1 frame).

---

## SLIDE 01 — COVER

**A1 Beat.** Hook. Stop the scroll and state the position. Plants the loop
"what land, spent how?" (the boundary and the USE blank both trail off-frame).

**A2 Copy, final (draft; copywriter to polish).**
- kicker (mono, 26px): "ALASKA.AI   No. 9" (17 ch)
- headline (Instrument Serif, fit 96 to 132px, 2 lines broken by sense):
  "First you spend the land." / "Then you decide what for." (10 words)
- deed tag on the plat (mono, 22px): "USE: ______________" (blank; C3/C9 setup)
- dek (Manrope 34px, <= 2 lines): "Alaska is moving 30 to 31 square miles of
  public land to its own development bank. For free." (C1, C2)
- footer: brand "ALASKA.AI" | coords "61 48 N 149 49 W" (data-decorative) | "01 / 09"

**A3 Reader takeaway (432px).** The state is giving away land before deciding
what it is for.

**B4 Layout map.** 12x8 grid. Plat occupies rows 4 to 7, cols 2 to 11
(lower two-thirds), focal point the empty grid at the rule-of-thirds lower-
left. Headline rows 1 to 3, cols 1 to 8 (upper-left mass, asymmetric). Quiet
zone upper-right (Polaris star only). Eye path: headline (1) -> USE blank on
plat (2) -> $0 stake (3) -> corridor cut at right edge (swipe). One grid
violation: headline optical-left hangs 8px past the margin.

**B5 Depth plan.** z-stack: warm-dark base gradient (#100C08 to #1A130B) ->
Mesh Wash warm radial (low, off-canvas key upper-right) -> plat slab
(dimetric, cabinet thickness, cast shadow) -> one faint ghost pad on cell
(4,1) -> corridor thread (edge-tease) -> DOM type -> grain tile. Depth cues:
occlusion (slab faces + ghost pad over grid), atmospheric fade (far cells
lerp toward warm haze), one key light + colored cast shadow, DOF (blurred
foreground loam clod bleeding off lower-left, repoussoir). Focal plane on the
plat top face. Dimetric math per shared geometry; ORX 540, ORY 596, scale 1.0.

**B6 Continuity device state.** Plat = empty, one faint ghost pad (listed,
not built). USE blank present. Corridor cut by right edge (completes on S2).

**C7 Technique stack.** #39 Cabinet Extrusion (slab, depth 28, half-scale 45
faces) + #38 dimetric lighting (top +15L / left base / right -15L, one key) +
#67 phantom dash (ghost pad edges: dasharray 6 5, 1.25px, bone-grey) + #3
Mesh Wash (4 warm radial stops, OKLCH via AKC) + #6 Paper Tooth (surface
tooth on slab top, fractalNoise 0.04 oct 5, subtle) + #2 Grain (AK.grainTile
280, 52, seed 20260716, opacity 0.10) + #89 akpost grade on the art canvas
(IGN dither ON). Star = DOM SVG Polaris (#FFC72C). Corridor = #57 frozen dash
+ #79 cased line. Canvas at 2x backing.

**C8 Data-in-art.** 30 solid cells + 1 dashed half-cell = C1 (30 to 31). One
$0 amber stake = C2. Ghost pad dashed = C3 (listed, not built). USE blank =
C9/C3 (purpose undecided).

**C9 Palette assignment.** bg #100C08/#1A130B; slab top loam #6E5334, faces
#4E3B25/#3A2C1C; ghost dash #9AA0A6; amber stake #E8973A; text #F8F2E8
(headline) / #F4EDE1 (dek); gold #FFC72C ONLY on Polaris + the $0 stake cap.
Worst-case contrast: headline #F8F2E8 on #14100B ~ 13:1 (pass); dek #F4EDE1
on base ~ 11:1 (pass).

**C10 Type spec.** Headline Instrument Serif roman, fit 96 to 132px / maxLines
2, leading 1.0, tracking -1.5%, color #F8F2E8, max-width 860px, optical-left.
kicker JBMono 500, 26px, tracking +12%, #E8973A. dek Manrope 500, 34px,
leading 1.32, #F4EDE1, max-width 720px. USE tag JBMono 400, 22px, #C9BBA6 on
a knockout window. footer JBMono 24px, #9C907E.

**C11 Anchor spec.** The plat IS the anchor (literal surveyed parcel). Survey
furniture: crop-mark Ls at plat corners (#83), one amber stake with a tag,
coordinates footer. Corridor doubled line lower-right.

**D12 Reference intent.** "A state land survey plat photographed on a warm
studio table at dusk, one stake driven in, most of the ground still blank."

**D13 Risk flags.** (a) Headline soft-wrap into dek -> AK.fitText maxLines 2,
verify line count. (b) Ghost pad + corridor canvas art crossing the headline
box -> reserve rows 1 to 3 free of plat art at plan time (plat starts row 4).
(c) Warm palette drifting to kraft-beige slop -> keep dark base + spruce +
gold Polaris + grain. (d) Gold budget -> only Polaris + $0 cap.

**D14 Acceptance checklist.**
- [ ] Headline renders in exactly 2 line boxes, no overflow into dek.
- [ ] Plat reads as a dimensional slab (visible cabinet thickness + one cast
  shadow), not a flat grid, at full size.
- [ ] 30 solid cells + 1 dashed cell countable at full size; ratio "mostly
  empty" reads at 432px thumb.
- [ ] USE: ______ line legible and clearly blank.
- [ ] Gold appears ONLY on the Polaris star and the $0 stake cap.
- [ ] Corridor is cut by the right edge (swipe cue) and nothing primary sits
  on the cut.
- [ ] At 432px thumb the cover stops a scroll (big serif + empty warm plat).

---

## SLIDE 02 — THE DEAL

**A1 Beat.** Pay off the cover immediately (steepest drop is 1 to 2). Deliver
the concrete transaction. Loop planted: "so what will actually be built?"

**A2 Copy, final (draft).**
- kicker: "THE DEAL"
- headline (Instrument Serif, ~76px, <= 2 lines): "The seller and the buyer
  are the same government."
- deed fields (JBMono, on knockout ledger plate):
  "SELLER   State of Alaska, DNR"
  "BUYER    AIDEA, the state development authority"
  "PRICE    $0"
  "METHOD   noncompetitive, no bid"
  "USE      ______________"
- body (Manrope 32px): "Alaska's land agency is moving 30 to 31 square miles
  of state land to AIDEA, the state's own development bank. No cost. No
  competitive bid." (C1, C2)
- footer: brand | "02 / 09"

**A3 Takeaway.** The state is selling public land to itself for nothing.

**B4 Layout map.** Headline rows 1 to 2 (cols 1 to 9). Deed ledger plate
rows 3 to 5, right of center (cols 6 to 11), a knockout window over the plat.
Plat lower third, cols 1 to 8, with the $0 stamp. Body rows 6 to 7, cols 1 to
6. Focal point the $0. Quiet zone lower-right. One violation: none.

**B5 Depth plan.** Same plat, camera scale 1.05, ORX 540, ORY 604. Ledger
plate floats above the slab with a layered shadow (#45). Depth cues: plate
elevation shadow, slab occlusion, atmospheric fade, one key light. Focal
plane the ledger + $0 stamp.

**B6 Continuity state.** Plat empty (no cells occupied, the ABSENCE of a
competing bid is the point). A large amber "$0 / NO BID" deed stamp across
three cells. USE field present and blank. Corridor completes from S1 at left,
re-cuts at right.

**C7 Technique stack.** Plat as S1 (#39/#38). Deed ledger = DOM/SVG on a
Frost Panel / knockout plate (#75 hatch knockout windows). $0 stamp =
survey deed-stamp (rotated ~ -6deg, amber, #E8973A) with a small gold cap
serif = the one gold beat. Phantom dash band "NO BID" (#67) across empty
cells. Grain + akpost as house.

**C8 Data-in-art.** $0 stamp = C2 (no cost). "NO BID" band + deliberate
absence of any competing-bid marker = C2 (noncompetitive). Deed ledger rows
= C1 (acres), C2 (price/method). Empty plat = the land not yet used.

**C9 Palette assignment.** Deed plate #1A130B at 0.92 with 1px #4A3A24 top
edge. Field labels #C9BBA6 (mono), values #F4EDE1. $0 stamp #E8973A with
#FFC72C hairline. Contrast values on plate ~ 10:1 (pass).

**C10 Type spec.** headline Instrument Serif 72 to 84px / maxLines 2. Deed
labels JBMono 500 24px tracked +10% #C9BBA6; values JBMono 400 30px #F4EDE1,
tabular. body Manrope 500 32px #F4EDE1 max-width 640px (ends in sky zone,
verify 3 lines max). kicker JBMono 26px #E8973A.

**C11 Anchor spec.** The deed ledger plate is the anchor; the plat is the
supporting field. $0 stamp as the focal glyph.

**D12 Reference intent.** "A Bloomberg BW spread, arctic edition: a stamped
land deed with the price line reading zero."

**D13 Risk flags.** (a) Deed values overprinting the plat art (canvas) ->
ledger sits on an opaque knockout plate, plat art routed clear beneath. (b)
body line count -> cap max-width so body ends by y ~ 640 (above plat). (c)
gold budget -> only the $0 stamp hairline cap.

**D14 Acceptance checklist.**
- [ ] Deed ledger fully legible on its plate (>= 4.5:1), no plat art bleeding
  through the text.
- [ ] $0 reads instantly as the focal point at 432px thumb.
- [ ] USE field is present and blank in the ledger.
- [ ] No competing-bid marker anywhere on the plat (absence is intentional).
- [ ] Headline <= 2 line boxes; body <= 3, ending above the plat.
- [ ] Gold only on the $0 cap + Polaris.

---

## SLIDE 03 — PURPOSE IS A WORD

**A1 Beat.** Show the purpose is listed, not built. Carry the agency's own
concession. Loop: "how big is the boom this is cleared for?"

**A2 Copy, final (draft).**
- kicker: "WHAT IT IS FOR"
- headline (Instrument Serif ~78px): "The purpose is a word on a plat."
- body (Manrope 32px): "The 41 page decision lists scalable data centers and
  AI and robotics manufacturing among the uses. Not one is a project yet."
  (C3, C4)
- pull quote (Instrument Serif ITALIC, 44px): "There are no pre-determined
  and set land use decisions made by AIDEA." (C9)
- attribution (JBMono 24px): "RANDY RUARO, AIDEA EXECUTIVE DIRECTOR"
- footer: brand | "03 / 09"

**A3 Takeaway.** The land is being cleared for uses that are only listed.

**B4 Layout map.** Headline rows 1 to 2. Pull quote rows 3 to 4 (the still
center, cols 2 to 10) on a knockout plate. Plat lower third with floating
use-labels over empty cells. Body rows 6 to 7 cols 1 to 6. 41-page glyph
(stacked sheet edges) right margin. Focal point the italic quote.

**B5 Depth plan.** Plat camera lower and slightly descended (ORY 300 keeps
plat in lower third; scale 1.0). Ghost pads dashed on 3 cells. Depth cues:
sheet-stack occlusion, slab thickness, atmospheric fade, key light. Focal
plane the quote plate.

**B6 Continuity state.** Cells wear small floating labels ("data centers",
"AI + robotics mfg", "utility corridors") but stay empty; ghost pads dashed.
USE blank echoed under the plat. Corridor cut at right (completes S4? no,
S4 is ISOTYPE; corridor teased S3 completes on S5 track). Note: corridor
edge-tease on S3 completes on S5 per Device C list (S1,S3,S5,S7).

**C7 Technique stack.** Plat #39/#38 with #67 phantom pads. 41-page glyph =
41 thin stacked parallelograms (cabinet edge), lightest lid, #6 paper tooth.
Quote plate = knockout window (#75). Floating labels = DOM with leader dots
(#69) to cells, routed to avoid the quote box. akpost + grain.

**C8 Data-in-art.** 41 stacked sheets = C4. Floating use-labels over EMPTY
cells = C3 (listed, not built). Italic quote = C9. Ghost pads dashed =
purpose undecided.

**C9 Palette assignment.** Quote text #F8F2E8 on plate #1A130B. Body #F4EDE1.
Labels #C9BBA6. Sheets loam #6E5334 edges. Amber only on the leader dots'
target ticks (tiny). Gold only Polaris. Contrast quote ~ 13:1.

**C10 Type spec.** headline Instrument Serif 72 to 84px maxLines 2. quote
Instrument Serif italic 42 to 46px, leading 1.12, #F8F2E8, max-width 780px,
maxLines 3 (VERIFY line count vs plate). attribution JBMono 24px tracked
+12% #C9BBA6. body Manrope 500 32px max-width 620px (3 lines max, ends above
plat). labels JBMono 400 22px #C9BBA6 (data-decorative on the leaf).

**C11 Anchor spec.** The 41-sheet stack + the labeled empty plat. Leader
lines from labels to cells (#72 discipline, never crossing).

**D12 Reference intent.** "An editorial pull-quote spread over a surveyor's
table: the paperwork thick, the purpose a single unanswered line."

**D13 Risk flags.** (a) Italic quote wrapping past 3 lines into the plat ->
AK.fitText/verify; cap max-width. (b) Floating labels (canvas or DOM) over-
printing the quote -> route labels to the plat's empty cells only, quote on
its own plate. (c) leader lines crossing text -> plan clear.

**D14 Acceptance checklist.**
- [ ] Italic quote renders <= 3 lines on its plate, fully legible, exact
  verbatim wording of C9 with straight quotes.
- [ ] "41" reads on the sheet-stack (count or labeled).
- [ ] Use-labels sit over EMPTY cells (no cell shows a built structure).
- [ ] Body <= 3 lines ending above the plat; no overprint.
- [ ] Gold only on Polaris; amber only on tiny target ticks.
- [ ] Leader lines do not cross each other or any text box.

---

## SLIDE 04 — THE BOOM WE DO NOT HAVE (breather + keepable)

**A1 Beat.** The breather and the single most-savable slide. Count the boom
honestly. Loop: "so why spend 31 square miles first?"

**A2 Copy, final (draft).**
- kicker: "THE BOOM"
- headline (Instrument Serif ~72px): "The boom Alaska does not have."
- ISOTYPE labels: "ALASKA  8" (amber) / "VIRGINIA  639" (grey)
- body (Manrope 32px, short): "Alaska has 8 data centers, the fourth fewest
  of any state. Virginia has 639." (C8)
- attribution (JBMono 22px): "counts per Alaska's News Source"
- footer: brand | "04 / 09"

**A3 Takeaway.** Alaska has 8 data centers; this land is for a boom not here.

**B4 Layout map.** Headline rows 1 to 2 cols 1 to 8. ISOTYPE field rows 3 to
7: 8 amber unit-marks pulled to the upper-left, directly labeled; a dense
639-mark grey field massed right and receding. Body lower-left cols 1 to 5.
Focal point the stark 8-vs-639 asymmetry. Quiet zone around the 8 marks (they
get air; the 639 block is dense).

**B5 Depth plan.** Flatter overhead read (the ISOTYPE field is parallel,
equal-area). Minimal depth: a slight atmospheric fade into the 639 block's
far edge + one contact shadow under each amber mark. This is deliberately the
deck's calmest depth beat (breather). No ghost pads.

**B6 Continuity state.** The unit CELL becomes the unit MARK: same top-diamond
shape, same size (honest ISOTYPE). 8 amber vs 639 grey. Corridor absent here
(breather); resumes S5.

**C7 Technique stack.** #28 ISOTYPE (same-size marks, never scaled), marks =
the plat's dimetric top-diamond at tileW 46. 639 laid in a parallel dimetric
field (~27 x 24 lattice, render 639, dim grey-green #6B7A70). 8 amber marks
#E8973A with a contact shadow. akpost light; grain.

**C8 Data-in-art.** 8 amber marks vs 639 grey marks = C8, drawn at IDENTICAL
size (honest ratio, not scaled). Attribution printed (single-source).

**C9 Palette assignment.** amber marks #E8973A; grey field #6B7A70 at 0.7;
labels #F4EDE1; headline #F8F2E8; gold only Polaris. Amber-on-dark contrast
~ 6:1; label legible.

**C10 Type spec.** headline Instrument Serif 68 to 76px maxLines 2. ISOTYPE
labels JBMono 500 28px, amber for ALASKA / grey for VIRGINIA, tabular counts.
body Manrope 500 32px max-width 560px. attribution JBMono 22px #9C907E
(data-decorative).

**C11 Anchor spec.** The two labeled ISOTYPE groups. Direct labels (kill
legends per doctrine). A hairline baseline rule under both groups.

**D12 Reference intent.** "An FT ISOTYPE breather: eight marks with room to
breathe against a wall of six hundred thirty-nine."

**D13 Risk flags.** (a) 639 marks illegible at thumb -> intended (reads as a
dense block); the 8 amber marks stay countable at 432px (feed test). (b)
scaling marks for drama = honesty fail -> ALL marks identical size, enforced.
(c) 639 block overprinting labels -> labels on the group edges, clear.

**D14 Acceptance checklist.**
- [ ] All ISOTYPE marks are identical in size (8 and 639 alike); no mark is
  enlarged.
- [ ] The 8 amber marks are countable at 432px thumb; the 639 block reads as
  "vastly more" at thumb.
- [ ] Both groups directly labeled with tabular counts; attribution present.
- [ ] Headline <= 2 lines; body <= 3.
- [ ] This slide is visibly calmer/emptier than its neighbors (breather).
- [ ] Gold only on Polaris.

---

## SLIDE 05 — ONE CELL (to scale)

**A1 Beat.** The scale mismatch. The biggest real proposal fills one square.
Loop: "and the neighbors?"

**A2 Copy, final (draft).**
- kicker: "TO SCALE"
- headline (Instrument Serif ~74px): "The biggest one proposed fills one
  square."
- body (Manrope 32px): "Alaska's largest proposed AI data center, STAK on the
  North Slope, would cover about 1 square mile. Here it fills 1 of 31 cells.
  Thirty sit empty." (C14)
- scale note (JBMono 24px): "STAK, reportedly over $10 billion, would draw
  more than 1 gigawatt, about 30 percent above urban Alaska's peak." (C12,C13)
- footer: brand | "05 / 09"

**A3 Takeaway.** The largest real proposal is one square; thirty are empty.

**B4 Layout map.** Headline rows 1 to 2. Plat rows 4 to 7, ONE cell occupied
by a solid extruded block (near the corridor), 30 empty. Body cols 1 to 6
rows 6 to 7. Scale note on a mono plate near the occupied cell with a leader.
Focal point the single occupied cell against the emptiness.

**B5 Depth plan.** Plat scale 1.0, ORX 540, ORY 600. The occupied STAK block
extrudes UP (solid loam-amber, h ~ 58px) so its cast shadow proves the light;
30 cells flat/empty. Depth cues: the tall block's occlusion + cast shadow,
atmospheric fade, key light, DOF foreground clod. Corridor tracks along and
cuts at right (completes S6).

**B6 Continuity state.** Exactly ONE cell occupied and extruded (STAK, 1 sq
mi = 1 cell); the rest empty. This is the only slide with a SOLID built cell
(everything else is ghost/empty), which lands the scale point.

**C7 Technique stack.** Plat #39/#38. STAK block = solid cabinet-extruded box
(#39) with #43 gradient-solid shading, amber-warm lit face. Dimension call
(#73) "1 of 31". Scale note plate knockout (#75). akpost + grain.

**C8 Data-in-art.** One occupied cell of 31 = C14 (about 1 sq mi) mapped to 1
unit cell; explicitly "1 of 31". Scale note = C12 ($10B+, reportedly), C13
(1+ GW, ~30% above peak, hedged). 30 empty cells = the unspoken-for ground.

**C9 Palette assignment.** STAK block face #8A5A3C lit, side #4E3B25, top rim
amber #E8973A hair. Empty cells #17110A. Body #F4EDE1. Gold only Polaris.
Scale-note plate #1A130B.

**C10 Type spec.** headline Instrument Serif 70 to 80px maxLines 2. body
Manrope 500 32px max-width 620px. scale note JBMono 400 24px #C9BBA6 on plate,
tabular. dimension call JBMono 500 22px amber.

**C11 Anchor spec.** The single extruded STAK cell + the "1 of 31" dimension
call. Corridor for continuity.

**D12 Reference intent.** "A scale diagram: one built block, thirty empty
lots, drawn honest and to size."

**D13 Risk flags.** (a) Perspective foreshortening faking the 1-of-31 area ->
parallel/dimetric only, cell sizes identical, verify. (b) scale-note plate
over plat art -> knockout plate. (c) hedge words present so projections are
not asserted as fact.

**D14 Acceptance checklist.**
- [ ] Exactly one cell is occupied/extruded; the other 30 read as empty.
- [ ] "1 of 31" (or equivalent) is explicit and legible.
- [ ] STAK figures are hedged ("reportedly", "about") on the slide.
- [ ] The occupied cell is the SAME footprint as one empty cell (honest area).
- [ ] Body <= 3 lines; no overprint on the plat art.
- [ ] Gold only on Polaris.

---

## SLIDE 06 — THE TOWN PULLS THE OTHER WAY

**A1 Beat.** The local counter-force. The nearest town is moving to ban the
use the state is zoning for. Loop: "two governments, two clocks, which runs
out first?"

**A2 Copy, final (draft).**
- kicker: "THE TOWN"
- headline (Instrument Serif ~74px): "The town on the boundary wants to ban
  them."
- body (Manrope 32px): "The City of Houston has an ordinance to ban data
  centers, with a vote set for August 13. In March the Borough Assembly voted
  6 to 1 to designate parcels, overriding a mayoral veto." (C6, C11)
- attributed line (JBMono 24px): "The ordinance claims a documented risk of
  accelerated permafrost thaw." (C7)
- footer: brand | "06 / 09"

**A3 Takeaway.** The nearest town is moving to ban what the state is zoning for.

**B4 Layout map.** Headline rows 1 to 2. Plat rows 4 to 7 crossed by a hatched
BAN barrier entering from the town (left/near) edge. A 6-to-1 tally (7 marks,
6 amber + 1 grey) on a knockout plate. Body cols 1 to 6. Attributed permafrost
line small, near the barrier. Focal point the barrier cutting the plat.

**B5 Depth plan.** Plat scale 1.0, ORX 600 (shifted so the town edge is
prominent), ORY 610. The BAN barrier = a hatched vertical plane (#86 Lynch
edge / toothed barrier) standing on the plat with a small cast shadow. Depth
cues: barrier occlusion over cells, slab, fade, key light.

**B6 Continuity state.** Plat crossed by the Houston BAN barrier (red-amber
toothed). A 6 to 1 tally appears. Ghost pads still dashed behind the barrier.
Corridor completes from S5, re-cuts right (completes S7).

**C7 Technique stack.** Plat #39/#38. BAN barrier = #86 toothed/hatched edge
+ #65 cross-hatch, in a warning red-amber #C6502A (distinct from workhorse
amber, a hotter hue). 6-to-1 tally = 7 same-size marks (#28), 6 #E8973A + 1
#6B7A70, on knockout plate (#75) with mono "6 to 1". akpost + grain.

**C8 Data-in-art.** Barrier = C6 (ban ordinance, vote Aug 13). Tally 6 amber +
1 grey = C11 (6 to 1 override). Attributed line = C7 (permafrost, per the
ordinance, attributed).

**C9 Palette assignment.** Barrier #C6502A hatch on plat; tally amber #E8973A
/ grey #6B7A70 on plate #1A130B. Body #F4EDE1. Gold only Polaris. Ensure the
hotter barrier red stays clearly non-gold after akpost (instinct from run 5:
use a redder hue, #C6502A has low green, stays non-gold).

**C10 Type spec.** headline Instrument Serif 70 to 80px maxLines 2. body
Manrope 500 32px max-width 640px (VERIFY 3 lines vs the tally plate). attributed
line JBMono 400 24px #C9BBA6 on a small plate. tally label JBMono 500 24px.

**C11 Anchor spec.** The BAN barrier across the plat + the 6-to-1 tally.

**D12 Reference intent.** "A zoning-fight diagram: a red hatched ban line laid
across the state's own plat."

**D13 Risk flags.** (a) barrier red drifting to gold under akpost -> use
#C6502A (redder), verify after grade (run 5 lesson). (b) body vs tally
collision -> body max-width capped, tally on its own plate, verify line count
(instinct 4). (c) attributed framing -> the permafrost line is attributed to
the ordinance, not asserted.

**D14 Acceptance checklist.**
- [ ] The BAN barrier reads as a hostile boundary cutting the plat at 432px.
- [ ] The barrier red is clearly NOT gold after the film grade.
- [ ] 6-to-1 tally reads without counting (explicit "6 to 1" label; 6 amber, 1
  grey).
- [ ] Permafrost line is attributed to the ordinance ("claims").
- [ ] Body <= 3 lines, no overprint with the tally plate.
- [ ] Gold only on Polaris.

---

## SLIDE 07 — SIX DAYS APART (keepable, gold peak)

**A1 Beat.** The schedule collision, the deck's saturated-gold peak. Two
governments' clocks six days apart. Loop: "which order, and does it matter?"

**A2 Copy, final (draft).**
- kicker: "TWO CLOCKS"
- headline (Instrument Serif ~78px): "Two votes, six days apart."
- timeline cells: "AUG 13  Houston votes on a data-center ban" (C6) and
  "AUG 19, 5 PM  State comment window closes" (C5)
- dimension call: "6 DAYS"
- body (Manrope 32px): "The town votes on its ban six days before the state's
  comment window on the giveaway closes. They are pulling opposite ways."
- footer: brand | "07 / 09"

**A3 Takeaway.** Ban vote Aug 13, state comment closes Aug 19, six days apart.

**B4 Layout map.** Headline rows 1 to 2. A horizontal timeline strip across
rows 4 to 5 (cols 1 to 11) with two lit date-cells and a gold dimension call
"6 DAYS" spanning the gap. Plat recedes/dims to a faint band below (rows 6
to 7). Body cols 1 to 6 row 6. Focal point the gold span between the two dates.

**B5 Depth plan.** The plat DIMS to a low-contrast band (this beat is about
time, not ground); the timeline is the foreground plane. Depth cues: the two
date-cells raised on small plates with shadows, the dimmed plat as a receding
background layer, gold dimension bar in the sharp focal plane.

**B6 Continuity state.** Plat recedes/dims (deliberate); two lit date-cells on
the timeline. This is the deck's single saturated-gold moment (the 6-day span
+ the Aug 19 tick). Corridor completes from S6, re-cuts right (resolves S9).

**C7 Technique stack.** Timeline = #77 octolinear rule + #78 station ticks;
two date-cells = white-filled roundels (#78). Dimension call (#73) "6 DAYS" in
gold #FFC72C (the peak). Dimmed plat = the S5/S6 plat at 0.35 alpha, desatur-
ated. akpost + grain; aberration allowed lightly (hero-art beat).

**C8 Data-in-art.** Two date-cells = C6 (Aug 13) and C5 (Aug 19, 5 p.m.). The
"6 DAYS" dimension = the exact interval between them (13 to 19 = 6). Gold
marks the collision (budgeted peak).

**C9 Palette assignment.** timeline rule #C9BBA6; date roundels #F4EDE1 fill
with amber ring; "6 DAYS" + Aug 19 tick GOLD #FFC72C (the one saturated gold
beat, still <= 4% area). Body #F4EDE1. Dimmed plat loam at 0.35.

**C10 Type spec.** headline Instrument Serif 74 to 84px maxLines 2. date labels
JBMono 500 26px, dates tabular. "6 DAYS" JBMono 700 30px gold, tracked +8%.
body Manrope 500 32px max-width 600px.

**C11 Anchor spec.** The timeline strip with two dated roundels + the gold
6-day dimension call.

**D12 Reference intent.** "A transit-map timeline: two stops, six days apart,
the gap called out in gold."

**D13 Risk flags.** (a) canvas timeline crossing the headline -> timeline in
rows 4 to 5 only, headline rows 1 to 2. (b) gold overuse -> gold ONLY on the
6-day span + Aug 19 tick + Polaris, measured <= 4%. (c) date legibility at
thumb -> large tabular mono on roundel plates.

**D14 Acceptance checklist.**
- [ ] Both dates (Aug 13, Aug 19 5 p.m.) legible at 432px thumb.
- [ ] "6 DAYS" dimension call spans exactly between the two date-cells.
- [ ] Gold is concentrated here as the deck's peak, still <= ~4% area.
- [ ] The dimmed plat reads as a receding background, not competing with the
  timeline.
- [ ] Headline <= 2 lines; body <= 3.
- [ ] The two clocks read as "opposing" (labels make the opposition explicit).

---

## SLIDE 08 — THE ORDER IS THE ARGUMENT (synthesis)

**A1 Beat.** Synthesis. Name the sequence plainly: everything decided but the
one thing that matters. Loop: "is that backwards?"

**A2 Copy, final (draft).**
- kicker: "THE ORDER"
- headline (Instrument Serif ~72px): "Everything is decided but the one thing
  that matters."
- deed ledger, now full (JBMono):
  "SELLER  State of Alaska      BUYER  AIDEA"
  "PRICE   $0                   METHOD noncompetitive"
  "ACRES   30 to 31 sq mi       DECISION 41 pages"
  "LOCAL   Assembly 6 to 1, veto overridden"
  "USE     ______________"  (blank, largest)
- body (Manrope 32px): "The land is given now, for free. What it is for gets
  decided later. The land is spent first. The purpose, and the risk, come
  second." (C1, C2, C4, C11)
- footer: brand | "08 / 09"

**A3 Takeaway.** The land is given first; its purpose is left for later.

**B4 Layout map.** Headline rows 1 to 2. Deed ledger rows 3 to 6 (cols 2 to
10) on the main knockout plate, every field filled EXCEPT USE, which is set
large and blank on its own row (the largest element after the headline). Body
row 7. Focal point the blank USE line.

**B5 Depth plan.** The deed ledger is the hero object here (the plat recedes
to a faint watermark behind the plate). Depth: the ledger plate elevated
(#45 layered shadow), USE line embossed/rule-drawn. One key light. Minimal
plat.

**B6 Continuity state.** The deed (Device B) reaches its fullest state: all
fields answered, USE blank and dominant. The plat (Device A) is a faint
backdrop. This is the argument sealed.

**C7 Technique stack.** Deed ledger DOM/SVG on knockout plate (#75) with a
scotch rule (#70) header. USE line = a heavy ruled blank (#71 rule terminal)
with a faint phantom fill hint (#67) that stays empty. Faint plat watermark.
akpost + grain.

**C8 Data-in-art.** Ledger fields = C1 (acres), C2 (price/method), C4 (41
pages), C11 (6 to 1). The blank USE line = the whole thesis (purpose
undecided). Size hierarchy: USE blank is the largest field (its emptiness is
the point).

**C9 Palette assignment.** ledger plate #1A130B; labels #C9BBA6; values
#F4EDE1; USE rule #E8973A hairline with #F8F2E8 label; gold only Polaris.
Contrast >= 10:1.

**C10 Type spec.** headline Instrument Serif 68 to 78px maxLines 2. ledger
labels JBMono 500 22px tracked +10%; values JBMono 400 28px tabular. USE label
Instrument Serif 40px + a long ruled blank. body Manrope 500 32px max-width
640px (verify 3 lines).

**C11 Anchor spec.** The completed deed ledger with the single blank USE line
as the focal void.

**D12 Reference intent.** "A filled-out deed where the one blank line is the
loudest thing on the page."

**D13 Risk flags.** (a) ledger crowding at 8 fields -> two-column grid, verify
no value wraps into the next row (instinct 4). (b) USE blank reading as an
error rather than intent -> label it clearly "USE" and keep it ruled. (c)
canvas watermark under ledger text -> ledger on opaque plate.

**D14 Acceptance checklist.**
- [ ] All deed fields legible, no value wraps into an adjacent row.
- [ ] The USE line is visibly the largest/emptiest field, clearly blank.
- [ ] The "land first, purpose later" sequence is explicit in the body.
- [ ] Numbers match claims (30 to 31 sq mi, $0, 41 pages, 6 to 1).
- [ ] Headline <= 2 lines; body <= 3.
- [ ] Gold only on Polaris.

---

## SLIDE 09 — CLOSE (single ask)

**A1 Beat.** Hand the blank to the reader. One debatable question, one ask.
No stacking. Resolve the corridor and the plat.

**A2 Copy, final (draft).**
- headline / THE ASK (Instrument Serif ~70px, the question): "Should Alaska
  spend public land before it knows what it is for?"
- USE field: "USE:  |" (an open field with a gold caret = the reader's turn)
- civic fact (JBMono 24px): "Public comment is open through 5 p.m. August 19."
  (C5)
- source note (JBMono 22px): "Sources in comments."
- brand block: "ALASKA.AI" wordmark + gold Polaris; "alaskaaihq.com" small in
  mono near the mark.
- footer: coords "61 48 N 149 49 W" (data-decorative) | "09 / 09"

**A3 Takeaway.** A real question: should the land be spent before its purpose
is known?

**B4 Layout map.** The question centered-left rows 2 to 4 (this is a
title-card close, centered composition permitted). The full quiet plat rows
5 to 7 with one amber "you are here" cell near the resolved corridor. USE open
field with caret rows 4 to 5. Brand block bottom. Focal point the question +
the blinking-caret blank.

**B5 Depth plan.** Plat returns to the S1 establishing view (bookend), quiet,
one amber cell lit. The corridor finally resolves fully into the plat (no
edge-cut). Gentle depth: slab thickness, one cast shadow, warm haze. Focal
plane the question.

**B6 Continuity state.** Bookend: the plat as on S1 but with the USE field now
an OPEN reader field (gold caret). Corridor resolves (loop closed). Device A
and B both land on the reader.

**C7 Technique stack.** Plat #39/#38 (bookend). USE open field = ruled line +
a gold caret glyph (#FFC72C, the close gold beat). Brand block DOM/SVG.
Polaris star SVG. akpost + grain.

**C8 Data-in-art.** One amber "you are here" cell = the reader's place in the
31. Aug 19 civic fact = C5 (not the ask, a fact). The open USE field = the
reader is invited to decide.

**C9 Palette assignment.** question #F8F2E8; USE caret + Polaris GOLD #FFC72C;
"you are here" cell amber #E8973A; site + coords #9C907E mono. Contrast question
~ 13:1.

**C10 Type spec.** question Instrument Serif 64 to 74px maxLines 3 (VERIFY),
leading 1.08. USE field Instrument Serif 40px + gold caret. civic fact + source
JBMono 24px #C9BBA6. wordmark Instrument Serif 30px #F4EDE1; site JBMono 22px
#9C907E.

**C11 Anchor spec.** The bookend plat + the open USE field. The constellation
fixtures (wordmark, Polaris, site, counter, coords) all present.

**D12 Reference intent.** "A closing question card: the deed's blank line
handed to the reader with the cursor blinking."

**D13 Risk flags.** (a) question wrapping past 3 lines -> AK.fitText maxLines
3. (b) stacking asks -> ONLY the question is the ask; Aug 19 and the site are
fixtures/facts, not asks. (c) site/wordmark legibility -> mono site small but
>= 22px, near the mark.

**D14 Acceptance checklist.**
- [ ] Exactly ONE ask (the debate question); Aug 19 and the site are fixtures,
  not asks.
- [ ] alaskaaihq.com present, small, mono, near the wordmark.
- [ ] "Sources in comments" present.
- [ ] Gold Polaris + the close caret are the only gold; <= 4% area.
- [ ] Question <= 3 line boxes, fully legible at 432px thumb.
- [ ] The plat bookends S1 (recognizably the same establishing view) and the
  corridor resolves (no edge-cut).
- [ ] Counter reads 09 / 09.

---

## STORYBOARD GATE (Phase 5.4 self-review) — see storyboard_gate.md
