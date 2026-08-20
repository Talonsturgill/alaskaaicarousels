---
name: carousel-engine
description: Render engine + QA harness for Alaska.Ai LinkedIn carousel slides. Turns per-slide HTML/CSS/SVG/Canvas art into exact 1080x1350 PNGs (2x scale), a vector-text PDF for LinkedIn upload, feed-size thumbnails, and a contact sheet — with objective machine QA (render errors, missing fonts, clipped/offscreen/tiny text, contrast estimates, safe-zone violations). Use whenever building or reviewing carousel slides. The engine is a HARNESS, not a template — every deck's art is bespoke code written per run.
---

# carousel-engine — render + QA harness

The quality layer is fixed; the art is not. Slides are hand-coded HTML files
(one per slide) using any mix of CSS, SVG, Canvas 2D, D3, and the committed
art libraries. This engine renders them deterministically, checks them
objectively, and assembles the deliverables.

## Pipeline (per run)

```bash
bash .claude/skills/carousel-engine/bootstrap.sh          # once per session; installs pip deps

# 1. write slides to      out/<run>/slides/slide-01.html ... slide-NN.html
python .claude/skills/carousel-engine/render.py \
    --slides-dir out/<run>/slides --out-dir out/<run>/render        # PNGs + render_report.json
python .claude/skills/carousel-engine/qa.py --render-dir out/<run>/render   # machine_qa.json, exit!=0 on FAIL
python .claude/skills/carousel-engine/assemble.py \
    --slides-dir out/<run>/slides --render-dir out/<run>/render \
    --out-dir out/<run>/final --title "<document title>"            # carousel.pdf (VECTOR text) + contact sheet + thumbs
```

Prove the deck is bespoke before shipping it:

```bash
python scripts/bespoke_check.py --slides-dir out/<run>/slides
```

"The engine is a HARNESS, not a template" was true and unmeasured until
2026-08-05, when a run shipped nine slides at 0.940 median pairwise art-code
similarity (bespoke reference: 0.049) and justified it in its own storyboard.
The gate measures the outcome, not the method, so generating the HTML is still
fine and nine frames sharing one drawing function is not.

Re-render only fixed slides with `--only 3,7`. Read every report; never ship a
FAIL. `qa.py` warnings are advisories for the pixel critics, not free passes.

`--only` is a sharp tool. render.py records the SHA1 of the source that made
each PNG, prints `STALE:` for any slide whose file has changed since, and qa.py
**FAILS** that slide, because a PNG that no longer matches its HTML sends a
reviewer a picture that does not exist. Run No.33 applied two repairs to source
and then re-rendered a different subset, so both were silent no-ops and the flow
critic reviewed the pre-repair contact sheet and reported both repairs as still
broken. The remedy is always the same, re-render the slide and re-run qa.

## Slide HTML contract

- One file per slide: `slide-01.html`, `slide-02.html`, ... Design for the
  viewport: exactly **1080x1350 CSS px**. `margin: 0`; nothing may scroll.
- Reference committed assets ONLY via the `@@ASSETS@@` token (the engine
  resolves it to an absolute `file://` path):
  ```html
  <link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
  <script src="@@ASSETS@@/js/noise.js"></script>      <!-- AK.simplex2/fbm2/warp2/rng -->
  <script src="@@ASSETS@@/js/aktype.js"></script>      <!-- AK.fitText display fit-to-box -->
  <script src="@@ASSETS@@/js/aklabel.js"></script>     <!-- AK.canvasLabel knockout-plate labels -->
  <script src="@@ASSETS@@/js/ak3d.js"></script>        <!-- AK3D software 3D renderer -->
  <script src="@@ASSETS@@/js/zdog.min.js"></script>    <!-- Zdog pseudo-3D (no GPU) -->
  <script src="@@ASSETS@@/js/d3.v7.min.js"></script>
  <script src="@@ASSETS@@/js/topojson-client.min.js"></script>
  ```
  Geodata via `fetch("@@ASSETS@@/geo/alaska-state.geo.json")` (boroughs,
  us-states, world-land, alaska-places also available). **NO external URLs,
  no CDNs, no Google Fonts** — render.py rejects any `http(s)://` reference.
- **Async art must gate the screenshot**: set
  `window.renderReady = new Promise(resolve => { ...draw, then resolve() })`.
  The engine awaits it (30s cap). Without it you get a 400ms grace only.
- **Canvas = 2x backing store.** Any `<canvas>` styled at `W x H` CSS px must
  have `canvas.width = W*2; canvas.height = H*2; ctx.scale(2,2)`. Screenshots
  are taken at deviceScaleFactor 2 and the PDF embeds the canvas bitmap — a
  1x canvas ships blurry.
- **Text is HTML/SVG, never canvas.** Canvas text rasterizes in the PDF;
  HTML/SVG text stays vector, survives LinkedIn's recompression, and feeds
  LinkedIn's semantic ranker + accessibility mode. Draw art on canvas; set
  type in DOM/SVG layers above it.
- Mark intentionally-tiny or bleeding text (footers, coordinates, watermark
  type used as texture) with `data-decorative` so QA doesn't flag it:
  `<div data-decorative class="coords">61°13'N</div>`
  Both `data-decorative` and `data-overlap-ok` inherit to descendants.
- **Plates are sized from the MEASURED string, never a guessed constant**
  (2026-07-29): JetBrains Mono at 24px with 0.10em tracking advances exactly
  16.8px per character; hand-sizing at the eye's estimate of ~14 loses about
  three characters in twenty. render.py now measures every SVG `<text>` against
  the `<rect>` painted under it and qa.py FAILS three cases: the label spilling
  past its plate, an opaque `<rect>` appended AFTER it (SVG has no z-index,
  only document order), and an opaque DOM element composited above the whole
  `<svg>`. Six labels shipped off their own plates through two scoring cycles
  before this existed, because every gate inspected DOM text only.
- **A slide MAY declare what its art says without words** (2026-07-29), on
  `<body>`, and the engine will measure whether that survives to feed scale:

  ```html
  <body data-encodes='[{"claim":"material change at hour 7", "reads":"differ",
                        "a":[[732,1052,82,98]], "b":[[736,500,74,540]]}]'>
  ```

  Regions are `[x,y,w,h]` in CSS px (a CSS selector string also works). qa.py
  reports, per declaration, the CIELAB distance and rank separability between
  the two populations AT 432px WIDE, plus how much of each region is visible
  art rather than furniture. Whether the encoding WORKS is still a
  MEASUREMENT and not a gate: two candidate quality thresholds were calibrated
  against a real known-bad and a real known-good and both came out backwards
  (see `encoding_reads` in qa.py). Read the numbers, do not trust a rule
  drawn through them, and do not add one without showing it separates a
  known-bad from a known-good on real renders.
  **`reads` is REQUIRED (2026-08-08) and two things about it DO fail.** It is
  `"differ"` (the two regions must be tellable apart) or `"same"` (an absence
  or sameness claim). A declaration that omits it FAILS, because a probe that
  states no direction is a number nobody can be wrong about; and a `"differ"`
  whose regions are **under 4.0 dE apart** at feed scale FAILS, because at that
  distance the probe is measuring the same thing twice. Neither is a judgment
  of the art. **MEASURE THE RECTS OFF THE RENDERED PNG, NEVER OFF THE
  STORYBOARD'S CAMERA ARITHMETIC.** Run No.29 computed both probe boxes from
  the camera maths on slides 05 and 06, they landed on empty water ~300px left
  of where the aperture actually drew (declared x=188, actual x=468, verified
  by block-scanning the shipped PNG), the deck's central wordless claim
  reported dE 0.9 and the deck's own build gate gated nothing. The light was
  never the problem: measured on the true rect the same declaration reads
  dE 89.9. The same run had already burned one probe pair earlier the same way,
  reporting the DARK frame as brighter than the lit one. Open the PNG, find the
  feature, then write the numbers. The floor is fitted over all 19 declarations
  in `runs/*/machine_qa.json`; sameness claims are not gated because the corpus
  has no known-bad to fit against.
- **A contact shadow must have something to subtract from** (2026-08-05), and
  a slide that declares one gets measured on it:

  ```html
  <body data-contacts='[{"what":"the shut block on the table",
                         "shadow":[[236,1178,608,30]],
                         "ground":[[236,1248,608,30]]}]'>
  ```

  Same rect grammar as `data-encodes`. qa.py takes the median CIELAB L* of
  each region AT 432px WIDE and **FAILS below 4.0 L\* of separation**, WARNs
  below 8.0. OPT-IN like the encoding contract, but unlike it this one is a
  GATE, because the question is one-dimensional and the slide asked it itself:
  a FAIL is the slide contradicting its own declaration, not a taste call.
  DECLARE IT ON EVERY OBJECT THE DOSSIER SAYS SITS ON SOMETHING. Run No.26
  built the two-part shadow exactly as specified, in `#1A0F08` at alpha 0.55,
  on a table already rendering near `#0B0906`; the composite is a **1.2 L\***
  change, four pixel critics returned `contact_edge_reads: no`, and machine QA
  passed the deck with zero fails. The fix is never a stronger shadow, it is a
  LIT GROUND: put a warm pool of light under where the object sits, then cast
  into it. The same run's slide 04, whose bar shadows the critics called
  convincing, measures 8.1. Related and not gated: a silhouette stroke on a
  LIGHT object must be outside-aligned onto the dark side, because a centred
  stroke puts half its width on paper it matches.
- **A mark on a measured axis is a quantity, whatever it was drawn for**
  (2026-08-16). If a POSITION in the artwork carries a number (a money rail, a
  timeline, a bar baseline, a dated span), the slide declares the scale and
  enumerates every mark inside the strip that scale owns:

  ```html
  <body data-scale='[{"what":"the award rail","axis":"x","unit":"dollars",
                      "from":[80,0],"to":[1000,272174856],
                      "band":[1150,1172],
                      "marks":[{"at":95,"means":"the first Friday, $4.5M"},
                               {"at":249,"means":"$50M"}]}]'>
  ```

  `from`/`to` are `[design px, value]`, `band` is the strip across the axis the
  scale owns, and every mark drawn in it is listed with what it means. qa.py
  FAILS on a mark that declares no meaning, on a mark outside its own span, and
  on any run of ink in the band, at least as strong as the weakest mark you
  declared, that you did not declare, printing the VALUE its position reads as.
  Run No.35 did this defect twice in one deck through every green gate: three
  gold place ticks under a rail whose x means dollars (three REGIONS printed at
  three dollar positions), and thirteen division ticks implying twelve months
  across a ten-month budget period. Two pixel critics caught them by reading.
  There is no such thing as a decorative tick on a measured axis: give the mark
  a meaning, or draw it outside the band.
- **A leader must land on the thing it points at, and say where that is**
  (2026-08-07). EVERY drafting leader, callout rule or detail-circle tail is
  authored as a **world-coordinate polyline that terminates ON the target's own
  coordinates**, never as a fixed offset from the annotation's own centre, and
  the slide declares it:

  ```js
  var SLIVER = [BX + 2, 838];                 // the feature's own coordinates
  var leader = [[168, 884], [128, 856], SLIVER];   // bends, then the target
  window.__akLeaders = [{ target: "the 2024 sliver's dimension line",
                          at: SLIVER, to: leader[leader.length - 1],
                          from: leader[0],            // where it meets the words
                          label: "2024 SLIVER, 41 DAYS" }];   // those words
  ```

  qa.py **FAILS** when `to` and `at` are more than `LEADER_LAND_PX` (24 design
  px) apart. Opt-in like the contracts above, and like them a FAIL is the slide
  contradicting its own arithmetic. Run No.28's slide 06 shipped two detail
  circles whose leaders ran into empty void, through two pixel critics, a flow
  critic and the first scoring cycle, because their tails were
  `tail:[-70,-70,-150,-150]` from each circle's centre: the target was never
  named anywhere, so there was nothing for any reviewer or gate to check, and a
  leader stopping in void looks exactly like a leader reaching something small.
  No pixel test can settle it (the landing tick puts ink at the terminus). The
  discipline is the point: writing `at:` forces you to go find the target.
- **And it must arrive at words** (2026-08-14). `from` and `label` are
  REQUIRED on every declared leader, and qa.py **FAILS** a leader that declares
  neither, that names a label no rendered text reads, or whose label sits more
  than `LEADER_LABEL_PX` (32 design px) from where the line arrives. Run No.33
  shipped three annotation elements with no terminal value at all, S01's leader
  running off the Rhode Island ring into bare sheet, S07's dimension call
  printing none of the values its own dossier spec declared, and S08's stamp
  leader descending into empty paper. Every gate passed the deck at zero fails
  and zero warns, and the 2026-08-07 leader gate returned ok on all three,
  because all three landed on their targets perfectly and the gate could only
  see that one end. A leader is a sentence with two ends. Set the label as DOM
  or SVG text: a canvas label's existence can be confirmed but its position
  can't, so it WARNs instead of clearing the check.
- **A printed number and the geometry it names must be checkable against each
  other** (2026-08-12). Any slide that sets a MEASUREMENT in type (a dimension
  rule, a count, a frame width, a scale bar) declares the relationship and lets
  the render decide it:

  ```js
  var FT_PX = 42;                             // one foot, solved from the lock
  window.__akAssert = [{ what: "the 20 ft lock, printed as an 840 px rule",
                         expect: 840,         // what the type claims
                         actual: 20 * FT_PX,  // what the drawing computed
                         tol: 2, unit: "px" }];
  ```

  qa.py **FAILS** when `expect` and `actual` are further apart than `tol`.
  Opt-in, and pure arithmetic on two numbers the slide supplied, so it never
  speaks about art it cannot understand. Run No.31's slide 05 printed an 840 px
  dimension that was exact to the pixel over a scene whose two masses were 266 px
  apart, so the deck's one load-bearing measurement, twenty feet, was drawn as
  about six and every gate passed it; the same run printed two map frame widths
  as typed constants that were wrong by 7 and 25 percent against the projections
  that actually drew the maps. **Better than declaring it is making it
  impossible**: solve the rig FROM the lock (one world unit is one foot, camera
  distance computed so one foot is 42 px) so the same number produces both the
  rule and the room. Declare the assertion anyway: it is what proves the
  derivation survived the next edit.
- **A text block may not set more lines than it declared** (2026-08-12).
  `AK.fitText(el, {min, max, maxLines})` records every call, and qa.py **FAILS**
  a block that ran past its own `maxLines` or bottomed out at `min` without
  satisfying its constraint. Not opt-in: the declaration is the `maxLines`
  argument you already wrote. The way it fails is always the same. `min` and
  the box width are two numbers chosen independently, `min` is set higher than
  the width can hold, the fitter clamps and overflows. And the repair is always
  the same: widen the box or lower `min`. On run No.31 it ran past on five
  slides and swallowed the sentence carrying the deck's whole thesis, with
  machine QA reporting PASS, zero fails, zero warns.
- **Text may never overprint text**: qa.py FAILS when two elements' text
  line boxes intersect (the 2026-07-08 slide-3 defect class). Deliberate
  layering (a chip on an opaque plate crossing a display line box) must be
  declared with `data-overlap-ok` on the floating element — the gate then
  warns instead, and the pixel critics judge it.
- **Art may never cross a label's glyphs** (2026-07-25): qa.py samples a thin
  ring around every non-decorative label's ink and FAILS when ink of the
  GLYPHS' OWN VALUE touches the letterforms across the label, whatever layer
  drew it (a canvas groove edge, a scored outline, an SVG leader rule, a GL
  hero's specular). Text set over art needs a declared defense: an opaque
  knockout plate, a scrim on a dark ground, or a halo (a halo is the opposite
  value, so it never trips the gate). `data-overlap-ok` demotes the FAIL to a
  WARN when the layering is deliberate and you have judged it legible. This is
  the gate that DOM `text_collisions` structurally cannot be: it reads pixels,
  so canvas and SVG geometry are visible to it.
- **Nothing opaque may be painted over type** (2026-07-26): render.py hit-tests
  every non-decorative text line box against every OPAQUE element box (opaque
  background, background image, or `<img>`) using the `elementsFromPoint`
  stack, and qa.py FAILS when a foreign plate covers >= 20x6px of a line box
  (WARN from 12x4px). A padded plate's BACKGROUND is not a line box, so
  `text_collisions` cannot see this: it is how a DEAD tag came to overprint the
  bottom third of a subtitle and pass with 0 fails and 0 warns, twice. The
  text's OWN plate (an ancestor or descendant) is never its own occluder, and a
  plate the text paints ABOVE is legible and never reported. `data-overlap-ok`
  demotes the FAIL to a WARN. The remedy is to move the plate or the type,
  never to declare the overlap away.
- **An SVG label must sit inside its own plate** (2026-07-29): render.py
  measures every `<svg><text>` against the `<rect>` painted under it, against
  any opaque `<rect>` appended AFTER it (SVG has no z-index, document order IS
  the stack), and against any opaque DOM element composited above the whole
  `<svg>`; qa.py FAILs all three (WARN under `data-decorative` /
  `data-overlap-ok`). Six labels shipped off their plates in one deck because
  the plate width and the label were two separately hand-typed numbers.
  **Never type a plate width.** Build it from the label:
  `AK.svgPlate(textEl, {padX, padY, fill, stroke})` (aktype.js) measures the
  laid-out text with `getBBox`, adds padding and any stroke, and inserts the
  rect as the label's immediately preceding sibling. Call it after
  `await document.fonts.ready`, and use `AK.svgPlateAll(selector, opts)` for a
  whole set. It handles `text-anchor` and `transform`, and `minWidth` grows the
  plate symmetrically so a centred label stays centred.
- Determinism: seed all noise (`AK.reseed(seed)`, `AK.rng(seed)`). Derive the
  seed from the run date. Same inputs must reproduce the same pixels.
  **ENFORCED since 2026-08-01**: render.py scans each slide's INLINE scripts and
  qa.py FAILs `Math.random()` / `crypto.getRandomValues()` / `crypto.randomUUID()`
  (WARN on `Date.now()`, `new Date()`, `performance.now()`), naming the line. A
  vendored library loaded by `src=` is not read, and the string in body copy is
  DOM text, not script, so neither trips it. The replacement is one argument:
  `const rnd = AK.rng(<rundate int> + <slide no>)`. This exists because an
  unseeded stipple field survived five render rounds on 2026-08-01 and was caught
  by a human running grep; an unseeded field means a repair pass repaints art the
  pixel critic already reviewed, and the shipped PNG cannot be rebuilt from the
  committed HTML.
- Fonts: use `assets/fonts/fonts.css` families — Fraunces (100-900 + italic,
  opsz), JetBrains Mono (400/500/700), Space Grotesk (300-700), Archivo
  (100-900, stretch 62%-125%), Manrope (200-800), Instrument Serif (+italic),
  Bricolage Grotesque (200-800, stretch 75-100%), Unbounded (200-900).
  Never request a weight/family not declared there (QA fails missing fonts).
  No faux bold/italic.

## Hard numbers (from the knowledge base; QA enforces the starred ones)

- Canvas 1080x1350 (4:5). PDF page = same. *Body overflow = hard fail.*
- *Text floor 24px* (warn), body text >= 32px, headlines 60-110px, hook
  display 120-170px. A 1080px canvas reads at ~390px on phones (x0.36).
- Safe zone: primary text inside **80px margins** (warn outside); keep
  ~150px clear top/bottom on the panorama's text columns for platform UI.
- Contrast: body text >= 4.5:1 against its local background. QA estimates;
  the pixel critic verifies the worst-case point.
- *Canvas health (2026-07-11):* any visible canvas covering >= 25% of the
  slide FAILS qa.py if its pixels are near-uniform (dead GL frame or empty
  art layer) or its backing store is under 1.5x CSS size (WARN 1.5-1.9x).
  GL canvases must be sampleable: akthree sets preserveDrawingBuffer and
  never probes the render target (getContext fixes attributes forever).
- PDF: vector mode required (assemble_report.json `pdf_mode: "vector"`);
  target 2-25 MB.

## In this directory

- `render.py` — HTML -> PNG at 2x + in-page QA extraction (`render_report.json`)
- `qa.py` — machine gate over PNGs + report (`machine_qa.json`, exit 1 on FAIL)
- `assemble.py` — vector PDF (Chromium print + pypdf merge), contact sheet,
  432px feed thumbs (`assemble_report.json`)
- `bootstrap.sh` — pip deps (playwright, pypdf, img2pdf; Pillow/numpy present)

## PNG in the loop, WebP on the way out

Everything above stays PNG. Review happens on lossless pixels: the pixel
critics read the full-size render and the 432px thumb, and a lossy artifact in
that loop would be indistinguishable from a real type-rendering fault.

Shipping is a separate step, run at Phase 11 after the artifacts are copied to
`runs/<date>/`, never inside the render loop:

    python scripts/ship_images.py --run <date>              # encode + verify
    python scripts/ship_images.py --run <date> --drop-png   # reclaim originals

It converts to WebP at the full 2160x2700 (nothing is downscaled), measures
PSNR against the original, and escalates q92 -> q96 -> q98 -> lossless per file
until every one clears 40 dB. A deck goes from ~36 MB to ~4.5 MB. It also
writes `og.jpg`, which every og:image and schema.org image points at, because
LinkedIn and Slack still handle WebP link previews inconsistently.

The public site references `runs/<date>/slide-NN.webp`. If you change the
shipped filenames or extensions, `scripts/site_build.py` has to change with
them or every archive page goes blank.

## Art libraries (committed, offline)

- `assets/js/noise.js` — seeded simplex 2D/3D, fbm, domain warp (`AK.*`)
- `assets/js/akrelief.js` — 2.5D relit-heightfield FORM-shading (`AK.reliefShade`),
  the offline/CPU analogue of `AKT.objectHero`'s rim-carve. A flat filled region
  reads as a shaded dimensional SOLID: builds a heightfield (noise.js fbm/warp by
  default, or a `height(u,v)` callback for a dome/bevel/ridge), derives per-pixel
  normals from a 3x3 Sobel, Lambert-shades against a NW key (or the MDOW multi-
  azimuth set via `{multidirectional:true}`), maps a shadow->lit ramp, optional
  silhouette `mask`. Load AFTER noise.js. Use it for a LAND/object hero (the
  cadastral-plate / boreal-relief beat) so it stops reading flat — the recurring
  artwork-craft=7 ceiling of 2026-07-21/07-22. `strength` is a gradient multiplier
  (noise fields ~2-6; a smooth macro dome/bevel ~60-200). Writes ImageData via
  putImageData (REPLACES pixels incl. alpha), so shade onto its own layer/before
  compositing other art. Shades ART only; text stays DOM/SVG; never encode
  quantity in the relief.
  THE OPTION CONTRACT (2026-08-20): `low`/`high` are REQUIRED and named from the
  slide's palette, and ANY key it does not know THROWS after a console.error
  tagged `AK CONTRACT:` (which qa.py FAILs on, so a slide-side try/catch can't
  swallow it). Run No.38 shipped two slides in the wrong material because
  `mix: 0.30` and `light: [x,y,z]` are not options here and were silently
  dropped: there is no blend of any kind (lay the substrate down FIRST, or
  composite a finish yourself with an explicit globalAlpha), the option is
  `lights: [{az,el,w}]`, and the old default ramp was a warm stone. Copy the
  same guard (`AK.optionContract(name, opts, allowed, notes)`) into any helper
  that grows an option list.
- `assets/js/akgeo.js` — Alaska projection + regional zoom (`AKGeo.*`).
  NEVER fitExtent to a small lon/lat bbox (renders a giant fill disc);
  use `AKGeo.zoomTo(proj, geo, lonlat, targetXY, zoom)` and draw the
  coastline STROKE-ONLY at zoom > ~2.
- `assets/js/aktype.js` (display-headline fit-to-box `AK.fitText`, and
  measured SVG knockout plates `AK.svgPlate` / `AK.svgPlateAll`). Call both
  inside renderReady after `await document.fonts.ready`.
  `AK.fitText(el, {min, max, maxLines})` binary-searches font-size so a
  large headline never silently soft-wraps an extra line into the block
  below it (the recurring wrap-collision defect through 2026-07-09). Prefer
  it over hand-tuned font-size on every display headline set in a fixed box.
  `AK.svgPlate(textEl, {padX, padY, fill, stroke, strokeWidth, rx, minWidth,
  opacity, className, attrs})` sizes a chip/knockout from the label's own
  `getBBox` (plus half any stroke, which getBBox excludes) and inserts it as
  the preceding sibling, so the plate cannot disagree with the text and cannot
  go stale when the string is edited. It throws a named TypeError on misuse (a
  render hard fail) and console.errors on untrimmed text, which measures wrong
  in every engine. It does NOT check font readiness at call time: two such
  guards were built and measured on 2026-07-29 and both cried wolf on correct
  usage, so awaiting `document.fonts.ready` is on you and the qa.py gate on the
  shipped pixels is what actually catches a fallback-sized plate. Run 2026-07-29 shipped six
  labels off their plates from hand arithmetic (JetBrains Mono 24px at 0.10em
  advances 16.8px per character, the plates were sized at about 14) and one
  repair created a seventh by lengthening a string without resizing its chip.
- `assets/js/aklabel.js` — knockout-plate CANVAS labels (`AK.canvasLabel`).
  Any label drawn with `cx.fillText()` is a bitmap with no DOM node, so the
  QA gates (text_collisions, contrast_estimate, busy-art tripwire) are BLIND
  to it: run 2026-07-11 shipped-then-caught ~10 canvas labels at ~1.5:1 on
  the ochre band and two flag labels overprinting. `AK.canvasLabel(cx, x, y,
  text, {color, align})` draws an opaque plate under the glyphs so the
  label's contrast depends on (text, plate) only, not the art beneath, and
  returns the plate rect (`AK.rectsOverlap` to keep stacked labels apart).
  Include AFTER noise.js. Still prefer DOM/SVG text where layout allows (it
  stays vector in the PDF and the gates can see it); use this for labels that
  must be pinned to canvas coordinates.
- `assets/js/ak3d.js` — software 3D: perspective camera, heightfield/box
  meshes, painter's z-sort, Lambert + fog, 3D polylines & point clouds (`AK3D.*`)
- `assets/js/zdog.min.js` — Zdog round pseudo-3D engine (canvas, no GPU)
- `assets/js/three.module.min.js` (r170, MIT) + `assets/js/akthree.js` —
  the GPU PBR bench (PROVEN on SwiftShader in this container, ~70ms/frame at
  2160x2700): materials/rigs/IBL/lathe/tube/extrude. ES module: load via
  `<script type="module">` + `await import('@@ASSETS@@/js/...')`. RULES:
  akthree sets pixelRatio BEFORE size (hand-rolled three code that reverses
  them silently renders at 1x); `await AKT.snapshot(R)` and check `.ok`
  (black-frame sentinel: returns `{ok, variance, litCount}` and accepts a frame
  either via the historic 24-sample mean/variance OR via COVERAGE -- a dense
  strided lit-pixel count, so an OBJECT HERO that fills only part of the frame
  over a transparent/dark empty background is no longer wrongly judged dead and
  forced to the flat Canvas fallback; a genuinely black/empty frame still has
  litCount 0 and returns `ok:false`. Tune with `AKT.snapshot(R,{litFloor,litMin,stride})` only if needed);
  design a Canvas fallback for `AKT.webglOK()===false`;
  composite via an offscreen canvas + drawImage when mixing with 2D art.
  OBJECT HERO: for a single foreground object that must read as a SILHOUETTE
  against a darker background (the backlit-machine case), call
  `AKT.objectHero(R, group, {toward:[kx,ky,kz], keyColor, intensity, height})`
  after adding the group. It scales the hero to `height` (optional, the sane
  framing bump) and adds a separation rim on the FAR side of the subject from
  the camera, leaned toward the key direction (`toward`), so the contour is
  carved by a warm backlight rather than reading as a flat blob. A key-side
  rim ALONE leaves the profile flat -- run 2026-07-12 S6 needed exactly this
  by hand. Tune `intensity` up for marquee heroes and verify the edge visually
  (the RENDERED LADDER pixel gate still applies). `AKT.fitHeight(group,h)` is
  the standalone scale helper.
  SCREEN-SPACE ANNOTATION IS DERIVED, NEVER TYPED (2026-08-20):
  `AKT.screenBox(R, meshOrGroupOrArray, {pad, padX, padY, w, h})` returns
  `{x,y,w,h,cx,cy,rx,ry,corners,behind,offscreen}` in DESIGN px (not the 2x
  backing store) from the target's OWN local bounding boxes through its
  matrixWorld and the live camera, so a contour, bracket, callout or
  `data-encodes` rect that names a 3D part is computed from where that part
  actually drew. Run No.38's slide 06 hardcoded four screen ellipses for parts
  placed by a camera and every one of them enclosed bare foam; nine pixel
  critics found it and no gate could. `behind`/`offscreen` console.error with
  the `AK CONTRACT:` prefix (a qa.py FAIL) because both states return a
  reasonable-looking rectangle that encloses nothing. `AKT.projectPoint(R,x,y,z)`
  is the single-point form for a leader terminus.
- `assets/js/aksdf.js` — CPU SDF raymarcher (`AKSDF.*`): organic sculpted
  heroes, soft shadows + 5-tap AO + smin blends; render 480x720 internal into
  a box, ~5-15s; `deadlineMs` degrades gracefully.
- `assets/js/akpost.js` — film grade (`AKPOST.grade`): bloom -> exposure ->
  saturation -> log-contrast -> ACES -> gamma -> split-tone -> masked grain ->
  IGN dither -> unsharp. Call ONCE on the art canvas after drawing, before
  the grain tile (or use akpost's own grain and skip the tile). DOM text is
  never affected.
  **`exposure` HERE IS STOPS. `AKT.setup({exposure})` ABOVE IS A MULTIPLIER.**
  One word, two meanings, two libraries used side by side on the same slide:
  runs No.30 and No.31 both authored `exposure: 1.02`-`1.06` meaning "about
  three percent" and got `2^1.03` = 2.04x on eighteen consecutive slides, which
  bloomed copper into gold and read to five critics as five unrelated faults.
  0 is unchanged, +1 is twice as bright, -1 is half; the house grade lives in
  -0.15 to +0.06. akpost.js now THROWS (a render hard fail) past 0.75 stops and
  akthree console.errors a multiplier under 0.25, so the trap is closed from
  both ends.
- `assets/js/akcolor.js` — OKLCH engine (`AKC.*`): material ramps (chroma
  bell + warm-light/cool-shadow hue drift), OKLab gradient mixing,
  gradient-map LUT underpainting.
- `assets/js/d3.v7.min.js` + `topojson-client.min.js` — maps & dataviz
- `assets/geo/alaska-state.geo.json` — Alaska outline, true lon/lat (137 rings)
- `assets/geo/alaska-boroughs.geo.json` — all 29 boroughs/census areas
- `assets/geo/alaska-places.json` — 40+ places with lon/lat/tags + the
  canonical Alaska projection recipe:
  `d3.geoConicEqualArea().parallels([55,65]).rotate([154,0]).fitExtent(...)`
- `assets/geo/us-states-10m.json` (pre-projected AlbersUsa TopoJSON, lower-48
  context only), `assets/geo/world-land-110m.json` (unprojected TopoJSON —
  use for globes/great-circle work)

WebGL/three.js: PROVEN in this container as of 2026-07-11 (SwiftShader/ANGLE
Vulkan "Subzero"; see akthree above and examples/proof-3d). Still probe
`AKT.webglOK()` and keep a Canvas-2D fallback DESIGN per slide — headless
failure modes are silent (black frame / flat-2D fallback), which is exactly
what the snapshot sentinel catches.

## Review artifacts

The pixel critics must Read (as images): every `render/slide-XX.png` (full
size) AND `final/thumbs/slide-XX-thumb.png` (feed size) AND
`final/contact_sheet.png` (the whole deck in sequence for flow/continuity).
