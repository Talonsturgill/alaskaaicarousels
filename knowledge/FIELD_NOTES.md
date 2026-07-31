# FIELD NOTES - living learnings

Append-only. Each run's retro adds dated entries: what worked, what failed,
what the human changed, new techniques discovered, sources to consider.
Newest first. Keep entries terse and actionable; promote stable lessons
into the doctrine/library files and prune here.

---

## 2026-07-22 - site change (maintainer session, not a run)

- THE SITE NOW CARRIES THE BOTTLENECK SCANNER. site_build.py gained scan_html()
  (a homepage section right after the hero, a one-field form that GETs to
  scan/) and scan_page() (the scan/ page, full form + polling + result iframe),
  plus a footer link, a sitemap entry, and an llms.txt line. Both are emitted
  by EVERY build, so a routine rebuild keeps them without knowing anything.
  The backend (Supabase Edge Functions, scanner schema, API-triggered scan
  routine) lives in the alaska-ai-scanner repo. If a build fails inside these
  functions, fix the build. Never remove the section or the page to ship.
- The .subscribe input styling now also covers input[type=text] (the scanner
  form field). Cosmetic, shared, safe.
- NOTE. The previously deployed pages had background-image:url(none), the film
  grain asset had been missing in a prior build environment. This rebuild
  re-embedded the noise data URI from assets/, which is the script working as
  designed, not a regression.

## 2026-07-21 - run retro (Carousel No. 13, "A Better Ear Is Not a Recovery", 8.77)

- FULL-STUDIO RUN, no usage-limit degradation. 6 scouts + fact-checker + 3 treatment-directors +
  copywriter + 5 pixel critics + flow-critic + scorer all ran. Shipped 8.77 vs 8.3, vector PDF 7.8MB,
  9 slides, zero hard fails.
- STORY. First marine-mammal / endangered-species acoustic-AI deck of the series: NOAA Fisheries +
  Microsoft AI for Good + ADF&G built a deep-learning dual-stage detector-then-classifier (contrastive
  audio-language models + active learning) to hear rare Cook Inlet beluga calls in a ship-noisy inlet and
  firm up daily presence; a separate NOAA-led effort (USGS, Microsoft AI for Good, Naval Research Lab)
  adds satellite detection. Deliberate NET-NEW pivot off the fatigued data-center beat (Nos 1,4,6,10) and
  every recent cold-infrastructure hero. Thesis "a better ear is not a recovery" (hearing is not healing).
- FACT-CHECK sharpened the honesty spine. The acoustic paper's full text is paywalled (Wiley 403), so the
  method is asserted only from the abstract and NO detection-accuracy percentage is claimed (none exists).
  The fact-checker corrected the population framing: NOAA says the best estimate 331 "may be stabilizing
  and possibly increasing" YET the population "has not recovered as expected" -> the deck draws neither a
  "still crashing" curve nor a recovery hockey stick; the S7 chart shows the ~80% collapse (1,300 1979 ->
  279 2018), a small hedged 331 uptick in a dashed uncertainty band, and a dotted 1979 baseline rule so the
  gap IS the argument. Dropped the scout's unproven "116,103 caribou" (fallback story) and fixed an author
  affiliation.
- CRAFT. New chassis: a continuous underwater Cook Inlet depth-world (camera descent + mono depth readout as
  progress) carried by a SINGLE warm gold "call" that changes state but NEVER multiplies (a clearer signal
  is not more whales), sealing into the Polaris; the water reads visibly UNCHANGED S1 vs S8, and the S8
  boundary box shows noise/prey/habitat as arrows that stop at the wall with no intake port. Story-art
  fusion 9, variety 9, flow SHIP (sequence_reads_as_one, motif_reads_across_all_9). Two new techniques + 3
  instincts logged.
- HERO / GROWTH EDGE (recurring). Artwork-craft capped at 7 again: the S3 beluga shipped as the DESIGNED
  CANVAS FALLBACK because the akthree GPU path false-negatived. Lesson (new instinct): an akthree object
  composited over a TRANSPARENT background makes AKT.snapshot's black-frame sentinel read empty samples as
  a dead frame and silently drop to the fallback; render the subject on an OPAQUE in-palette bg and
  composite the whole frame, or make the 2D illustration the hero on purpose. The fallback beluga reads
  clearly as a beluga but flat; Phase 12 candidate = a bounded akthree object-hero-on-opaque-bg helper.
- PIXEL CATCHES machine QA missed (qa PASS 0/0): S2 top-heavy with a dead lower band; S4 core metaphor not
  reading (faint noise band + gold needle reading as the mooring cable) PLUS a gold SHIP NOISE readout;
  S8 gold leaking onto the SHIP NOISE/PREY/HABITAT input labels; S3 body wrapping to 8 lines. New instinct:
  audit every secondary label for accent-color leak before render (gold = the call ONLY). All fixed and
  re-verified to ship; RECORD-SYNC caught one drift (S7 "2008 endangered" -> "2008 listed endangered")
  reconciled before ship.
- DOCKET: no new AI-infrastructure decision (a beluga-monitoring story is not infrastructure). Material
  in-window update tracked: the City of Houston ban ordinance vs the AIDEA Mat-Su data-center park (Aug 13
  council vote added). Re-verified STAK (comment closed, pending final decision), AKLNG (third special
  session July 27), Air Force EUL (no award as of July 19). docket_alerts result noted at ship.
- NEXT: a published beluga-model accuracy number or a Sealaska Tlingit-AI-translator second source remain
  strong future angles; the akthree-on-opaque-bg object-hero helper would retire the chronic flat-hero cap.



- FULL-STUDIO RUN, no usage-limit degradation. 6 scouts + fact-checker + 3 treatment-directors +
  copywriter + 5 pixel critics + flow-critic + scorer all ran. Shipped 8.55 vs 8.3, vector PDF 2.2MB,
  9 slides, zero hard fails.
- STORY. The first education deck of the series: the rules for AI in Alaska's classrooms are being
  written now. In-window anchor = Kenai Peninsula Borough School District's proposed AI policy (KBBI,
  July 8), which already spent $8,300 on MagicSchool before the governing policy exists. Deliberate
  net-new pivot away from the fatigued data-center/power beat (Nos 1,4,6,10) and the covered
  salmon/volcano/wildfire/Navy/minerals/SAR/permafrost topics. The DEED 2025 K-12 AI framework (32nd
  state, 7 principles, 6-step process) is the keepable backbone, stamped "CONTEXT, NOT NEWS."
- FACT-CHECK KILLED A TEMPTING LEAD. The in-window Space Force GBRD radar award ($423M, 2 Alaska
  radars, July 17) looked strong but the fact-checker confirmed NONE of the primary/trade sources say
  AI or ML; it is analog-to-digital radar digitization. Building an "AI" deck on it would have
  fabricated the premise. Dropped. (NSF minerals in-window = hard dedupe with No.8; STAK/AIDEA =
  fatigue.) Runner-up NOAA YOLOv11 salmon-bycatch (fully verified, primary NOAA) passed over for
  salmon+CV adjacency to No.2 (11 days prior) + background date.
- CRAFT. New chassis: a gradebook-page editorial substrate + an evolving pencil motif whose length
  encodes the shrinking runway to the fall deadline, with ONE rendered akthree pencil-on-lit-gradebook
  still-life as the depth hero and 8 flat editorial slides (argued). Diverges from all last-4 heroes.
  Flow-critic SHIP 8.3, sequence-reads-as-one. New technique + 3 instincts logged.
- PIXEL/FLOW CATCHES machine QA missed: S5 headline "not ink." washed out on the lit cream page
  (fixed with a DOM Deep-Sea-Scrim, not the fading gradient); S5 gradebook ruled lines + half-written
  line were absent and the tip read gold (added lines, darkened the nib); S6 headline overprinted the
  ISOTYPE grid (SVG marks are invisible to qa.py's text-only collision check) and a big dead mid-card
  band (relocated the 32/50 strip down, freed the headline full width); two bodies (S2/S4) wrapped to
  4 lines; the pencil motif dropped out on S4/S6 (flow-critic; added the pencil to both). All fixed
  and re-verified.
- SCORER (8.55). Weakest = artwork craft (7): one moderately-rendered hero carrying 8 flat slides,
  and the pencil still reads a touch like a gold rod without a fully distinct graphite writing tip
  (logged growth edge). Legibility 7: low-contrast accent furniture (gold counter on paper ~1.5:1,
  red-on-cream) darkened before ship. Alaska authenticity 9.
- DOCKET: no new AI-infrastructure decision item (an education-policy story is not infrastructure).
  Re-verified STAK (comment window closed July 17, DNR weighing) and AIDEA Houston (open to Aug 19);
  both accurate. docket_alerts result noted at ship.
- NEXT: if KPBSD adopts the policy at the start of the school year, that is a clean UPDATE angle. The
  Sealaska Tlingit AI translator and the ANLC ChatGPT-DEI grant story remain strong untouched
  language-AI angles once corroborated with a second readable source.

## 2026-07-20 - craft refresh (run 12 pre-research pass)

- Platform numbers RECONFIRMED, nothing to change: document/carousel posts remain
  the highest-reach native format (~6.6% ER), saves are the dominant 2026 signal
  (~5x a like), dwell 15 to 20s, 8 to 10 slides the sweet spot, 1080x1350 the
  ratio. (dataslayer/oktopost/contentdrips 2026.)
- One marginally-fresh craft handle for the keepable data slide, consistent with
  the 07-19 annotation note: 2026 editorial dataviz desks frame good annotation as
  "deliberate subtraction, not addition" (FT chief data reporter) - place titles,
  labels, gridlines, color so each element supports comprehension or is cut; one
  primary annotation reads first, all others stay visibly secondary. Reinforces
  existing practice; no gate change.

---

## 2026-07-17 - run 9 retro (Carousel No. 9, "No Road Out. Quinhagak Flies Its Own Eyes", 9.07)

- FULL-STUDIO RUN, no usage-limit degradation. 6 scouts + fact-checker + 3 treatment-directors + copywriter + 5 pixel critics + flow-critic + scorer all ran. Shipped 9.07 vs 8.3, vector PDF 7.86MB, 9 slides, zero hard fails.
- STORY. Quinhagak's Nalaquq (Native-owned Qanirtuuq subsidiary) trains its own FAA Part 107 drone pilots in the roadless Y-K Delta and owns its own machine vision (a real search-and-rescue boat-detection CNN plus a polarized-lens salmon counter). Deliberate hard break from 8 straight cold-infrastructure/instrument decks: a warm, human, place-rooted sovereignty story. Runner-up (AIDEA Houston 30-sq-mi free-land data-center giveaway, fully verified) was passed over for variety and tracked on the docket instead.
- HONESTY-AS-EDGE, again. The fact-checker's make-or-break call: the AI is REAL but narrow. Training is human-piloted (Part 107), NOT autonomous; the ML is two Nalaquq prior JCMC tools; reindeer thermal and archaeology are human-read, NOT AI. Rendered the split AS DESIGN (S7 MACHINE-vs-HUMAN equal-panels ledger plus a standing PILOT/HUMAN tag on the hero, no invented percentage). Scorer and flow both read the modesty as the spine, not a hedge. New instinct (honesty-quarantine-as-design).
- CRAFT: the chronic flat-hero weakness is RESOLVED. S6 AK3D software-3D thermal river-valley (heightfield plus akpost grade) with a white-hot CNN boat detection read as genuine dimensional relief (artwork-craft 8, not the usual 7). Two framing lessons: brighten the valley floor (near-black reads as a dead void) and raise the horizon so terrain fills the lower half. New instinct (ak3d-terrain-hero-resolves-flat). New technique logged (Thermal Search-Grid motif).
- PIXEL CATCH machine QA missed: all 12 S4 ISOTYPE trainees rendered gold, blowing the gold budget and killing the highlighted figure's distinction; recolored 11 to muted slate. New instinct (isotype-neutral-not-accent). The HAND-LAUNCHED leader also read as a strikethrough over its label (rerouted).
- DOCKET: added the AIDEA Houston land-giveaway item; refreshed STAK (comment window closes today 4:30pm), AKLNG (Dunleavy called a THIRD special session, rejecting the corporate tax), GVEA (outcome still unconfirmed), Air Force EUL. docket_alerts SENT 1 subscriber email (4 alerts) because BUTTONDOWN_API_KEY is set and STAK's deadline is inside 48 hours.
- DELIVERABLE GAP (Phase 12 candidate for next run): gmail_draft.py reads copy.json["post_copy"] and ["aftercare"], but the copywriter contract emits "caption" (text lives in caption.txt) and NO aftercare list, so BOTH the post-copy block and the aftercare checklist rendered EMPTY in the first payload. Caught at draft time by the showrunner and hand-fixed (added post_copy = caption + hashtags, and a 6-item aftercare list, to copy.json). Permanent fix: either make gmail_draft.py fall back to caption.txt + a default aftercare when the keys are missing, OR add post_copy/aftercare to the copywriter's required output schema. Recurs every run until fixed.
- NEXT: STAK final DNR decision lands after 7/17; GVEA LM6000 outcome still worth a hard re-check; AIDEA Houston comment window to 8/19; a Nalaquq published accuracy number or the Sealaska Tlingit-AI translator would be strong future update angles.

## 2026-07-15 - run 8 retro (Carousel No. 8, "The Uncomputed Ground", 8.78)

- FULL-STUDIO RUN, recovered mid-run. Today's earlier No.7 died on the account
  weekly limit; this run's canary Beat B scout ran fine (limit reset past 5pm
  UTC), so the fan-out spawned, but 3 scouts (A/C/E) then hit a SESSION limit
  ("resets 11:50pm UTC"). Beat B + D + F completed with enough coverage, the
  maintainer confirmed the reset, and the full studio ran end to end
  (fact-checker, 3 treatment-directors, copywriter, 5 pixel critics, flow-critic,
  scorer). Lesson reconfirmed: a CANARY probe before a 6-way fan-out cheaply
  distinguishes "layer dead" from "layer alive" and its result is not wasted.
- STORY. NSF named a UAF-led coalition its Critical Mineral Accelerator Engine
  ($15M now, up to $160M/10yr if milestones met) to use AI to help locate deposits
  and biological methods to extract them. Sharpest honest angle: the AI headlining
  it is a single sourced sentence with no model, dataset, or site named yet, and
  the $160M is a milestone-gated ceiling. Honesty-as-edge (like No.2, No.5).
- FACT-CHECK CAUGHT THREE SHIP-STOPPERS the scouts/community-signal had wrong: NANA
  is a PARTNER, not a co-owner; "biomining"/mine-waste-recovery/remediation are NOT
  on the page (say "biological methods for extracting minerals"); and the sources
  name NO specific mine/district, so do NOT connect the Engine to Ambler/Pebble.
  Trust only fetched text; the Beat F community framing was a useful angle guide but
  several of its "facts" did not survive the fact-check.
- CRAFT. New continuity motif that landed: a CONFIDENCE METER that evolves per beat
  and never lies to 100%, plus a strict gold=real / phantom-blue=promise TRUTH COLOR
  CODE (story-art fusion scored 9). New technique: the Uncomputed Prospectivity
  Survey-Plate. Two new instincts (confidence-meter-honesty-motif, truth-color-code).
- WEAKEST = artwork craft (7.5). The deliberately flat/graded 2D relief (argued in
  the dossier since the thesis is an unfinished survey) shipped but read as a graded
  2D map with a grid overlay, not the dimensional plate the storyboard argued for.
  Same rendered-ladder growth edge as No.7. PARKED as a Phase 12 upgrade candidate: a
  reusable relief-depth helper (directional hillshade + atmospheric layering + interior
  texture) so future map-hero decks get real depth without GL risk. New instinct logged
  (relief-depth-not-just-grade).
- PIXEL/FLOW held: 7/9 shipped first pass; S2 body overflowed to 7 lines and ended on
  a fragment (tightened), S8 body grazed the coastline and had an ambiguous bare
  "Engine" (fixed with a scrim + "chief executive"). Flow-critic flagged the S6->S7
  junction (no open loop); fixed with an S7 kicker bridge ("WHAT THE CLIMB IS FOR").
- DATE BOUNDARY. No.7 shipped as 2026-07-14 earlier today; this run dated 2026-07-15
  to avoid colliding with the committed runs/2026-07-14 artifacts (same rolling-forward
  as No.7 off No.6).

## 2026-07-13 - run 6 retro (Carousel No. 6, "The Interior's Power Math")

- **Shipped 8.69 vs 8.3** (9 slides, vector PDF 3.26MB), zero hard fails, 1 pixel round (all 9 reviewed; S2/S3/S4 had blocker/major issues, all fixed + re-verified) + 1 flow round (SHIP, 8.2) + 1 post-score fix. Story: GVEA's July 13 board vote on a second ~$120M LM6000 gas turbine, framed "Firm power, soft load" -- a member-owned Interior co-op asked to finance firm gas capacity on member debt while the AI loads that make firm power feel urgent (Air Force EULs at Eielson/Clear/JBER) are still proposals. Deliberate pivot to a flat editorial FIRM/SOFT type-weight ledger + one rendered turbine, after four straight energy/monitoring/robotics decks.
- **The winning frame was the essayist's, strengthened by the other two directors.** "Firm power, soft load" (a portable rule-of-thumb) beat "the megawatt mortgage" (data-journalist) and "the phantom load" (systems-illustrator); the phantom-load idea was GRAFTED in (the SOFT column drawn in drafting phantom-dashes), and all three converged on the rendered LM6000 object as the depth hero. Synthesis > any single pitch.
- **Fact-check recovered claims the fact-checker dropped on dead URLs.** The fact-checker returned 19 verified claims but dropped the GVEA fuel-spike (its guessed alaskasnewssource/ADN URLs 404'd). A quick showrunner re-fetch with the REAL URLs (gvea primary via search + alaskasnewssource + KUAC) recovered the +61%/$45.74/$2.50-to-$5.10 backdrop (c19-c24) that became the emotional core (S5). Lesson: when the fact-checker drops a claim for a fetch failure (not a falsehood), retry the URL yourself before abandoning a strong beat.
- **Honesty firewall as a DESIGN problem, not just a copy one.** The load-bearing S3 ("what the paper reports" vs "what the co-op says") FAILED the pixel critic because the attributed data-center panel rendered larger/brighter than GVEA's own words -- visual favoritism inverting the honesty point. Fix: identical panels (same top, min-height, plate, quote glyphs). New instinct logged (equalize-honesty-panels).
- **Rendered object hero needs a text scrim, not text-shadow.** S4's body copy over the akthree steel turbine dropped below 4.5:1 (pixel BLOCKER) despite a shadow; a Deep-Sea-Scrim DOM gradient behind the text column fixed it while keeping the object big. Also: the first lathe profile read as a propane bottle; a bell intake + casing seams + a rear exhaust stack + a control cabinet made it read as an industrial turbine package. Two new instincts (render-object-text-scrim; and reshape-for-silhouette). Weakest rubric criterion again = artwork craft (7): the turbine still reads slightly generic as a chrome vessel; parked as a reusable LM6000-specific object-hero detail kit.
- **The dividing-rule motif carried the whole argument.** A FIRM(solid)/SOFT(ghost) vertical rule that migrates per beat and SEALS into a gold "closed door" at synthesis (executive session) then splits open into the close question read as one evolving object across the filmstrip (flow critic confirmed motif + palette-arc). Generalizes to any two-sided / certain-vs-speculative story.
- **Recurring fixes that held:** fixed-width centered label boxes tripped the safe-zone gate on their BOX edges (S2); content-width nowrap fixed it (new instinct). Instrument-Serif-italic-only again false-FAILed render.py's upright-400 font probe; the offscreen upright-loader span cleared it (the parked 07-10 probe fix is now worth landing as a real engine change -- Phase 12 candidate).

## 2026-07-13 - craft refresh (run 6 pre-research pass)

- **"Bounce rate" is now named as an explicit tracked document-post signal** (dataslayer Feb 2026, digitallybugged 2026 guide): the algorithm reportedly reads whether a viewer swipes past slide 1, and a high slide-1-to-slide-2 dropoff suppresses reach. This is a sharper articulation of our existing "steepest drop is 1 to 2 / cover must earn the swipe" rule, not a new lever. Practical restatement for the directors room: the cover's ONLY job is to buy the second slide, and slide 2 must pay immediately (no agenda beat). Nothing to change in the gates.
- Everything else reconfirms current practice: documents remain the top organic format (~6.6% ER), saves ~5x a like / ~2x a comment in reach value, 8 to 10 slides and 15 to 20s dwell the save-optimal band. No doctrine change.

---

## 2026-07-12 - run 5 retro (Carousel No. 5, "First Machine to the Fire")

- **Shipped 8.54 vs 8.3** (9 slides, vector PDF 2.3MB), zero hard fails, 1 pixel round + confirmed fixes + 1 flow round. Story: Alaska as the world's proving ground for autonomous wildfire robots (XPRIZE Autonomous track finals via UAF ACUASI on a 1,000 sq km range; five finalists; September 2026 verdict). Deliberate break from four straight energy/infrastructure/monitoring decks.
- **The Dryad/XPRIZE story that collapsed in run 4 survived in run 5** because the frame changed: the deck is built on the VERIFIED structure (xprize.org roster, ACUASI/UAF partner, 1,000 km2, prize architecture, FAA test-site status), and Dryad's self-reported detect-and-suppress demo is one attributed data point (S6, "Dryad says" + NOT INDEPENDENTLY VERIFIED), never the thesis. The climax is the honest open verdict (S8), not the demo. Fact-check-before-select resolved the finalist count too: FIVE Autonomous finalists (Dryad's own "final three" contradicts xprize.org and was dropped).
- **New hero/motif that landed: the closing Autonomy Ring** - a discrete cyclic control-system loop (detect/decide/dispatch/douse) that doubles as an explicit N/4 progress counter and seals gold at the verdict. Flow critic caught that brightness-only arc increments read as a static logo; fix = dim (gray) unlit arcs + an explicit "N / 4" label. New instinct logged. Generalizes to any process/loop story.
- **Two honesty catches by the pixel critics** that qa.py can't see: S3 lit "fire-season" bars rendered gold after akpost (fixed to redder #E8531F to match the split bar and clear the gold budget), and S4's warm convergence point sat exactly on the Dryad row (favoritism for the one company featured later; moved above the roster, all five nodes equal). Both were composition/honesty, not machine-detectable.
- **Rendered akthree hero** (backlit quadcopter over fire-lit dusk) shipped with an AK3D fallback; weakest criterion (artwork craft, 7) is that it still reads slightly flat. A warm rim light from the key direction + a scale bump made it read as a quadcopter rather than a smear (new instinct). Parked for Phase 12: a reusable rim-light + profile-clarity helper for object heroes.
- Canvas-vs-DOM overprint recurred and was again caught only by eye (S5 loop arcs vs block plates, S8 body vs closed ring), not qa.py. Confirmed-instinct bumped.

---

## 2026-07-12 - craft refresh (run 5)

- Named, reusable frameworks drive SAVES on LinkedIn carousels (a coined "The N-Thing Method" reads as a portable thinking tool). Reinforces giving each deck a named thesis/frame on the cover, not just a headline. Consider a coined frame when the story has a clean structural spine.
- 8 to 10 slides remains the save-optimal band with roughly 15 to 20 seconds dwell; nothing here changes current practice. Consistency of the visual system across every slide (background, type, accent, grid) is repeated as the top design driver, which the constellation system already enforces.

---

## 2026-07-11 - THE 3D UPGRADE (maintainer-directed dev session, post run 4)

- **The 2D-to-3D leap landed.** Empirical probes overturned the standing "WebGL experimental"
  assumption: SwiftShader/ANGLE (Vulkan "Subzero") renders a full PBR frame (MeshStandardMaterial,
  2048px PCFSoft shadows, ACES, AA) at 2160x2700 in ~70ms in this container. Forum lore said 24-31s;
  measure, do not inherit. Four new committed benches: akthree (GPU PBR + procedural IBL + brand
  rigs/materials), aksdf (CPU SDF raymarcher for organic sculpted heroes), akpost (film-grade post:
  correct op order, IGN dither, masked grain, unsharp), akcolor (OKLCH ramps + gradient-map
  underpainting). TECHNIQUE_LIBRARY 87-90; DESIGN_DOCTRINE gained THE RENDERED LADDER; proof deck at
  examples/proof-3d (3 slides, qa PASS).
- **Two bugs the bench now encodes forever:** (1) three.js setPixelRatio must precede setSize or the
  backing store silently drops to 1x (all early probes were unknowingly 1080p); (2) a nested block
  comment in a JS header killed a module load with a bare "Unexpected token" page error; node --check
  everything committed.
- **Scene-authoring lessons from the proofs:** emissive tubes at tone-mapped exposure balloon into
  washed bands (keep emissive intensity <= ~2.5 and radius small); SDF carved tunnels go near-black
  without an indirect floor; light-bottomed renders need dark-ink footer furniture (contrast gate
  caught it).
- **Enforcement wired (same session, maintainer prompt):** qa.py now FAILS dead canvases (near-uniform
  pixels = failed GL frame) and sub-1.5x canvas backing; rubric + pixel-critic enforce THE RENDERED
  LADDER; master prompt names the gates. The dead-canvas gate's first reconstruction run caught a real
  bug: probing webglOK on the render target froze the context without preserveDrawingBuffer and blinded
  the sampler. Probes get throwaway canvases, forever.
- **Parked, high-value next steps:** matcap + G-buffer deferred pass for ak3d (per-pixel normals,
  Blender-clay look without GPU); APCA text-contrast auto-solver; saliency-map focal-hierarchy QA
  check (Itti-Koch downsample: assert the intended focal wins); strata-texture helper (run 4 retro);
  llvmpipe lane (--use-angle=gl) as a SwiftShader hedge if Chromium's deprecation ever lands.

## 2026-07-11 - run 4 retro (Carousel No. 4, "The Cook Inlet Gas Machine")

- **Shipped 8.90 vs 8.3** (9 slides, vector PDF 2.94MB), zero hard fails, 1 pixel round + 1 flow round.
  Story: the July 10 RCA denial of Enstar's $240M Cook Inlet gas STORAGE prudency request, framed as
  Alaska's supply ceiling meeting AI's gigawatt demand. NEW hero: a subsurface engineering cutaway
  ("the gas machine") on a panorama-spine, with a reservoir-lens state machine and a valve open->shut motif.
- **Fact-check-before-select earned its keep again**: the two topically-fresher candidates collapsed under
  scrutiny (Dryad XPRIZE wildfire = company-PR-only sourcing + vague AK site; MONTIS avalanche drone = NOT AI,
  it is remote-piloted, and "first DOT"/"replaces helicopters" were unsupported). Ordering claims before
  selection saved the run from building a deck on PR. A well-sourced important story beat two novel thin ones.
- **The canvas-vs-DOM-text blind spot recurred at scale** and is now the dominant defect class: qa.py PASSED a
  deck where in-section DOM readouts and canvas labels overlapped body text and sat on the low-contrast ochre
  band (S2 legend on homes, S3 curve labels on body, S4 readouts ~1.5:1 on ochre, S6 SUSPENDED, S7 flag-label
  mash, S8 context on ochre). Fixes: a `.plate-dark` CSS class for DOM readouts, canvas knockout chips for
  canvas labels, and capping body max-width so the body ENDS in the sky zone. Two new instincts logged.
- **State-change motif needs geometry, not rotation**: the flow critic found the 8-spoke valve looked identical
  rotated; an amber lock-bar across the hub made "shut" read at 432px. Motif carriers must change SHAPE.
- **Honesty guardrails held**: c10/c11 (op-ed rate stats) kept off every slide; c12 (2027) used once, tagged
  op-ed; c13 quoted verbatim with the "different units, not one sum" guardrail directly under the S8 bars; no
  derived MW anywhere. The Bcf-vs-GW adjacency (all three directors flagged it) is defused on-slide.
- **Curly-apostrophe false-positive, again**: three pixel critics flagged "smart quotes"; source grep showed
  ZERO curly/dash bytes on all 9 slides (straight U+0027/U+0022). Fraunces/Manrope render straight apostrophes
  with a slight curl. Always verify quote/dash violations at SOURCE level (run-1 lesson, re-confirmed).
- **Weakest criterion = artwork craft (7)**: flat strata gradient bands, plain elliptical lenses, and S1/S9
  lower-third dead zones. PARKED for Phase 12 as a reusable strata-texture/rim-light helper (within-band fbm
  mottling + lens rim-light + dead-zone fill) so every future cutaway/landscape deck gets it for free.
- Docket: added the Enstar Cook Inlet gas storage item (RCA denial). GVEA (Jul 13) and AKLNG (Jul 16) re-fetch
  failed (429/503/403) and were carried forward; both resolve within days and are worth a hard re-check next run.

## 2026-07-11 - Phase 12 (automation retro + frontier scan)

- **APPLIED - knockout-plate canvas-label helper (`assets/js/aklabel.js`).** The durable form of this run's
  dominant hand-fix. `AK.canvasLabel(cx,x,y,text,{color,align})` draws an opaque plate under the glyphs so a
  canvas label's contrast depends on (text, plate) only, not the strata beneath; `AK.rectsOverlap` keeps stacked
  in-scene labels from merging. Verified: same text/colour that shipped at ~1.9:1 on ochre reads ~8.5:1 with the
  helper; ENSTAR/HILCORP that merged into "ENSTAHILCORP" now sit on separate plates. Opt-in; no gate touched.
- **PARKED - canvas-text-aware QA gate.** The real gap is that canvas-DRAWN text is invisible to EVERY gate
  (text_collisions/contrast_estimate/busy-art tripwire all walk render.py's DOM text_nodes; canvas ink has no
  node). A gate that could see it needs OCR or stroke/edge heuristics that would false-positive on dense
  sectional artwork (strata hatching, valve wheels, curves). Not a safely-boundable ~100-line change. Revisit
  only with a bounded discriminator (e.g. require in-scene labels to register a DOM "shadow rect" the gate can
  read, turning canvas labels back into checkable boxes). Meanwhile `aklabel.js` removes the incentive to draw
  raw canvas text. Recommended to maintainer: a contrast floor for `data-decorative` labels over light bands, or
  a house rule that in-scene labels use `AK.canvasLabel` (both are threshold/policy = maintainer's call).
- **PARKED (frontier, procedural-art scan) - strata-texture / rim-light craft helper.** Weakest rubric this run
  = artwork craft (7): flat gradient bands, plain elliptical lenses, dead lower-thirds. The scan confirmed the
  math is ALREADY committed in noise.js (`AK.fbm2/fbm3/warp2`); Quilez's fbm article gives the geological
  parameter (H=1, gain=0.5, ~5-6 octaves) for rock-like spectra, and relief needs only a cheap gradient-of-fbm
  rim-light. So the parked helper is a thin painterly LAYER over existing primitives, not new deps: (1) clip to
  a band path, paint low-alpha fbm mottling (gain 0.5, 5 oct) tinted +/- 8% luminance; (2) rim-light a filled
  lens/shape by stroking its upper-left arc with a lighter tint at ~0.5 alpha; (3) fill dead lower-thirds with a
  very low-alpha warp2 field. Held because it is a SECOND assets/js change the day after a 4-upgrade day; land
  it next run as the sole improvement slot, verified by rendering an opt-in demo slide. Sources:
  https://iquilezles.org/articles/fbm/ , https://iquilezles.org/articles/warp/

## 2026-07-11 - craft refresh (run 4 pre-research pass)

- **Named, reusable frameworks drive saves (new actionable handle).** Multiple 2026 carousel roundups (Oktopost, Morphica, SocialPilot) converge that the highest-save decks hand the reader a NAMED, portable thinking tool ("The 3-C Framework", "The RICE Method") they can carry and reuse, not just a story. For us that means: when the story allows, give the deck ONE named lens or rule-of-thumb the reader keeps (a coined term, a 3-part test, a checklist), stated once and reinforced on the close. Save-value is our whole strategy, so this is a real lever, not fluff. Does not change gates.
- Platform numbers otherwise hold: documents remain the top organic format (~4.5% ER, ~45% over video, ~6x reach of link posts, ~3x save rate of text), 4:5 portrait, 6-10 slides the sweet spot, caption under ~150 words driving INTO the deck, personal-profile edge persists (aftercare note for the human, not a design change).

## 2026-07-10 - parked frontier + minor candidates (upgrade-engineer, editorial-dataviz/cartography scan)

- **Concentric-radial-rings seasonal small multiple (parked technique).** A
  recent Bloomberg guide wraps the calendar year into a ring per small chart;
  concentric rings each encode a variable (weekly share, avg high temp,
  precipitation) and a seasonal peak reads as a bulge. Portable to offline,
  seeded, static SVG/Canvas. Strong fit for any AK deck with a seasonal
  quantity (fishing openers, daylight swing, eruption cadence, PFD timing).
  TECHNIQUE_LIBRARY candidate, not an engine change; promote when a deck's
  story lands on a cyclical/seasonal number.
  Source: https://www.anychart.com/blog/2026/07/10/data-graphics-pull-their-weight/
- **Data-journalist map design space (parked reference).** "How do Data
  Journalists Design Maps to Tell Stories?" analyzes 462 journalistic maps from
  five outlets into an eight-dimension design space (article properties + map
  visual/interactive features) plus common editorial rationales. A checklist
  for the treatment-directors when a deck goes cartographic (framing/crop,
  annotation, focus+context, projection intent). Reference, not code.
  Source: https://arxiv.org/abs/2508.10903
- **Style-aware font probe (parked minor fix).** render.py's font-loaded check
  builds its `document.fonts.check()` spec as weight + size + family with NO
  font-style, so an italic-only display face (Instrument Serif italic this run)
  false-FAILs the upright-400 probe; self-corrected in-slide by loading both
  faces. Fix: pass the element's computed font-style into the check spec so the
  probe tests the face actually used. Bounded and correct, but it edits a hard
  gate and was not defect-forced this run, so it was held (daily cadence favors
  0-1 upgrades and two reactive fixes spent the budget). Land it a day the
  budget is open; verify no shipped slide's font check changes verdict.

## 2026-07-10 - run 3 retro (Carousel No. 3, "The Machine That Hears a Mountain Think")

- Story: AVO volcano-monitoring AI (VOISS-Net + VolcSARvatory) with the live Great Sitkin
  eruption peg (3 volcanoes elevated at once, Jul 3 AVO update). First instrument-register deck
  (Space Grotesk + JBMono + obsidian/phosphor); evolving seismic-trace conductor motif.
- **Canvas-over-DOM-text is a QA blind spot**: qa.py checks DOM line boxes only, so the S3
  flightpath arc crossed body copy and machine QA PASSED it; pixel critics caught it. New
  instinct logged: route canvas paths around text blocks at PLAN time and make critics check
  canvas-vs-text explicitly.
- **Motif connective tissue**: the flow critic found the conductor trace read on ~6 of 9 frames;
  adding low-alpha enter/exit strokes on S3/S6/S7 stitched the film together. Lesson: a motif's
  TRANSFORMATION states are not enough; draw the connections.
- Fact-checker corrections that mattered: $6.3M is a shared NASA award (7 projects), Great Sitkin
  is 5,708 ft (not 5,709), Shishaldin elevation unfetchable so the Arc Index shows "not listed"
  (honest omission beats invention).
- fitText everywhere prevented all wrap-collisions this run (0 vs 4 last run); the recurring
  defect class appears closed by the committed helper.

## 2026-07-10 - craft refresh (run 3 pre-research pass)

- **Personal profile carousels earn ~63% more engagement than company-page carousels** (dataslayer/linkboost 2026). Alaska.Ai posts from a page; the human should consider cross-posting the deck from a personal profile, or at minimum knows the page handicap is real. Aftercare-relevant, not a design change.
- **Buffer 2026 State of Social Media (52M+ posts)** reports a median LinkedIn carousel engagement rate far above single-format medians; the wide spread confirms carousels as the highest-ceiling format but says nothing new to change the build. Documents still #1 (~6.6% ER convergent).
- **Year-over-year platform contraction is steeper than the mid-2025 read**: views ~-50%, engagement ~-25%, follower growth ~-59% (dataslayer Feb 2026). Reinforces judging against OUR trailing median and the keepable-artifact strategy over applause. Nothing to change in the machine.

## 2026-07-09 - run 2 retro (Carousel No. 2, "One River, Two Ways to Count It")

- **Shipped 8.83 vs 8.3** (9 slides, vector PDF 4.94MB), zero hard fails, one pixel-refinement
  round + a passing flow round. Story: the Wood River AI drone + computer-vision salmon-counting
  pilot vs Bristol Bay's 70-year hand-count towers. Full worker roster ran (6 scouts, fact-checker,
  3 treatment-directors, copywriter, 5 pixel critics, flow critic, scorer) with no usage-limit
  degradation this time; parallel critics earned their keep (caught 3 things machine_qa passed).
- **Fact-checker saved us from two errors the scouts carried**: ADF&G is NOT a project partner
  ("isn't directly involved at this stage"), and the run forecast is 44.05M not 41.5M. Re-fetching
  every URL and dropping the unverifiable (BBRSDA dates, exact GVEA cents/kWh, the 4:30pm deadline
  time) kept the deck honest. Lesson reinforced: trust only fetched text, never scout summaries.
- **Honesty as the edge, not a hedge**: the deck's whole thesis is that the AI is UNPROVEN (in
  training). The gold UNPROVEN scorecard cell, the "CONF 0.00 UNTRAINED" cover tag, and "every
  number the fleet trusts came from a human hand" scored best-in-class story-art fusion (9). A
  thin-but-true frame beat a hyped one.
- **Display-headline wrap is the new slide-3 defect class**: four headlines (S1/S4/S7/S8) wrapped
  an extra line into the body and machine_qa-FAILED as overprint, all because the headline
  container was narrower than its longest line. New instinct logged; fix is full-width or downsize
  + verify line count pre-render.
- **Empty lower thirds** cost a craft point. Several slides left the bottom third dead. New
  instinct: budget the lower third (readout / caption / anchor / intentional quiet), do not default.
- **Canvas ctx.filter="blur()" works headless** for a discrete DOF foreground pass (S5 reeds);
  keep the focal layer outside the filtered save/restore. Cheap, reliable repoussoir blur.
- **NEW technique invented**: SpawningSockeye (added to TECHNIQUE_LIBRARY) -- a side-profile
  spawning sockeye SVG icon (humped dorsal, kype, olive-green head, forked tail) that reads as
  salmon at 432px and doubles as the deck's data anchor (the fish wears both counting marks).
- Story note: the drone pilot has NO published accuracy number yet; when the team reports one
  (or ADF&G formally joins), that is a strong UPDATE angle. GVEA July 13 turbine vote, STAK July 17
  comment close, and AKLNG July 16 vote all resolve within days -- docket-worthy follow-ups.

## 2026-07-09 - craft refresh (run 2 pre-research pass)

- Platform numbers hold, nothing new vs run 1's craft note: documents still the
  #1 format (6.6 to 7.0% ER, ~5x reach of static, 12.92% of all saves), 8-10
  slides, 15-20s dwell the ranking signal. (dataslayer/contentdrips/postunreel 2026.)
- **Echogram as a portable visual language (NEW craft handle)**: imaging-sonar
  fish counting compresses hundreds of sonar video frames into a single
  "echogram" band (time on one axis, range on the other, each fish a bright
  streak). This is a real, drawable, information-dense motif for any AK
  fisheries-AI deck: a seeded streak field where streak COUNT encodes the fish
  number and density encodes run strength, with a flat 2D axis. Portable to
  offline Canvas. (arxiv 2502.05129 "Counting Fish with Temporal Representations
  of Sonar Video"; arxiv 2505.06637 multimodal foundation AI for wild salmon in
  Indigenous rivers.) Parked as a technique candidate; only used if the story lands there.

## 2026-07-08 - run 1 retro (Carousel No. 1, "Four Rooms, One Open Door")

- **Shipped 8.64 vs 8.3** (9 slides, vector PDF 10.74MB) after one revision
  cycle. Round 0 scored 6.9: the scorer caught a slide-3 DOM text overlap
  (body line over a bar label) that machine QA passed - the
  machine-qa-is-not-taste instinct, confirmed the hard way.
- **DEGRADED run**: a session usage limit blocked ALL worker subagents
  mid-run (treatment directors, copywriter, pixel critic, flow critic).
  Showrunner authored the treatment/copy and self-reviewed; the objective
  gates (render QA, caption lint) and the scorer (which recovered later)
  still ran. Fallback held, but solo review missed a collision the scorer
  caught: parallel critics are not optional at full quality.
- **d3 zoom trap (new instinct)**: fitExtent to a small lon/lat bbox
  polygon renders a giant fill disc + mis-scaled map. Manual zoom (baseline
  full-state fit, then scale x zoom and re-translate onto the target) with
  a STROKE-ONLY coastline is the reliable recipe (slides 2 and 7).
- **data-decorative does not inherit**: mark the leaf text element (span,
  b, appended SVG text), not the parent div.
- **pypdf/cryptography panic**: the container's Debian cryptography 41
  rust binding panics on import, killing the vector PDF path;
  `pip install --user --upgrade cryptography` fixes it. Consider adding to
  bootstrap.sh.
- Scorer false-positive to remember: serif fonts render straight U+0027 as
  a typographic apostrophe glyph; verify quote characters with grep at the
  SOURCE level before treating as a hard fail.
- Story note: the STAK docket (ADL 422741) final decision lands after Jul
  17 - next run should check it for an update angle; Bristol Bay AI
  sockeye counting is the parked runner-up (claims c64-c77, fully
  verified).

## 2026-07-08 - craft refresh (run 1 pre-research pass)

- **360Brew is live as THE ranker** (LinkedIn Engineering, ~Mar 2026):
  distribution now runs on meaning/intent matching, not keywords. On-slide
  vector text and a topically explicit caption directly feed ranking;
  reinforces the vector-text hard gate. (dataslayer.ai 2026 algorithm
  review.)
- **AuthoredUp 3M-post study (Mar 2025 to Feb 2026)**: documents earn 39%
  more reach / 30% more engagement than the average post; documents are
  12.92% of all saves (2.6x their content share); only 4.88% of creators
  post documents regularly. Format edge persists. (contentdrips 2026-07-01.)
- **Q1 2026 softening**: carousel reach declining quarter over quarter
  while infographic-style posts hit 28.6% of top-1% posts. The keepable
  data-slide mandate is now the growth edge, not a nice-to-have.
- Mid-2026 "authenticity update": engagement bait, pods, and link spam
  penalized harder; polls effectively dead (0.07% ER). Nothing to change
  for us; confirms educational + native strategy.

## 2026-07-08 - framework build (engine smoke test lessons)

- **Grain economics**: full-frame feTurbulence grain rasterizes to a 10-40MB
  incompressible bitmap in the printed PDF. Always `AK.grainTile()` as a
  repeating background. (Encoded in TECHNIQUE_LIBRARY #2 and noise.js docs.)
- **Vector text survives blend modes**: Chromium's print engine keeps HTML/
  SVG text as vector even under mix-blend-mode overlays - but canvas text
  always rasterizes. Text in DOM/SVG, art in canvas. (Engine SKILL.md.)
- **`#map svg { display: block }`** - inline SVG baseline space overflowed
  the page by ~5px; the engine's body_overflow gate caught it. Always
  display:block full-bleed SVGs.
- **AlbersUsa inversion is a trap**: us-atlas TopoJSON is pre-projected and
  the inversion params are not recoverable reliably. We committed genuinely
  unprojected sources instead (Natural Earth 10m state outline via
  world-atlas; plotly unprojected counties for the 29 boroughs). Winding
  must satisfy the d3 spherical convention - rewind any ring whose
  geoArea > π.
- **3D composition must be computed, not eyeballed**: horizonY =
  cy + tan(−pitch)·f; a peak d units above the camera at distance D lands
  (d/D)·f px above the horizon. First two terrain attempts buried the
  range in the bottom 15% of frame. (Math now in ak3d.js header.)
- **Machine QA passed a slide the eye failed** (terrain crammed low, spec
  row colliding with ridge): objective gates catch errors, only pixel
  critics catch composition. Both layers are mandatory.
- **Simultaneous-contrast illusion**: bright strokes bounding a dark region
  make it read lighter than an identical fill elsewhere. Sample pixels
  before declaring a fill bug (we chased a phantom for four bisections).
- **Contrast estimator limits**: qa.py's bbox-median method under-detects
  text over busy varied art. The pixel critic must check worst-case
  contrast visually; the estimator is a tripwire only.

## 2026-07-08 - patterns adopted from the GitHub scout pass

- Instincts ledger (ECC pattern): ledger/instincts.json, confidence-scored
  lessons injected into future runs. Prune < 0.5 confidence after 8 runs.
- Variance dials + anti-repetition (taste-skill pattern): in the dossier
  header + artwork ledger.
- Claims-file fact-checking (Loki shape): claims.json with atomic claims,
  evidence URL + verbatim quote each; slides carry claim-ids.
- Completion gate (planning-with-files pattern): out/<run>/run_state.json
  phases must all be "done" with artifacts existing before merge/delivery.
- Critic text transcription (OCR-wave pattern, no deps): pixel critics
  transcribe every visible word from the PNG and diff against the dossier
  copy - catches font fallback, tofu, truncation that DOM checks miss.
- Candidates parked for later: microsoft/flint-chart (chart spec language),
  pyiqa (BRISQUE gate; heavy torch dep), meodai/heerich (SVG voxel mode),
  self-hosted Postiz (publish automation), pretext (text layout lib).

## 2026-07-09 - parked frontier + friction candidates (typography scan)

- **Variable-font WIDTH-axis fitting (parked).** Archivo and Unbounded carry
  a variable `wdth` axis; fit-to-width.js binary-searches the width axis
  (not just font-size) to fit a line, preserving optical size and cap-height
  while narrowing letterforms. Would complement AK.fitText (fit wdth first,
  then font-size) for headlines where shrinking type reads as timid.
  Not bounded enough to land in one daily upgrade slot; revisit when a deck
  needs a wide poster headline held at a fixed size.
  Source: https://github.com/Lorp/fit-to-width
- **Pre-flight colon lint (parked friction fix).** scripts/site_build.py
  refuses prose colons on emitted pages; run 2026-07-09 hit it twice (a
  docket history note, the first_comment article-title colon) and had to
  rephrase at SHIP time. A cheap lint over ledger notes / emitted copy run
  earlier in the pipeline would surface it before ship. The gate is correct
  and must not weaken; this only moves the catch earlier. Bound it to the
  same colon rule site_build already enforces before implementing.

## 2026-07-12 - parked frontier candidates (accessibility / PDF scan)

- **Per-slide alt text surfaced in the Gmail draft (parked, highest-value).**
  In 2026 LinkedIn has no native organic image carousel; the only swipeable
  format is a document post (PDF/PPTX/DOCX), which LinkedIn RE-RENDERS into
  images. That means embedded PDF tags do NOT carry to the LinkedIn viewer;
  the reach/accessibility lever is the ALT TEXT typed into LinkedIn's upload
  UI per slide. The machine could emit a short factual alt string per slide
  (from the dossier + transcribed copy) and print them in the Gmail draft so
  the maintainer pastes them at upload. Parked because it needs a copy source
  of truth (dossier vs pixel-critic transcription) and gmail_draft.py work
  beyond one bounded daily slot; not a defect. Sources:
  https://www.oktopost.com/blog/linkedin-carousel-pdf-best-practices/ ,
  https://socialbee.com/blog/how-to-post-linkedin-carousels/
- **PDF /Lang + Marked flag in assemble.py (parked, near-bounded).** The
  public-site PDF (alaskaaihq.com) has no document language set; a screen
  reader guesses pronunciation. assemble.py already writes Title/Author/
  Creator metadata (lines 96-97) but no /Lang or /Marked. Setting
  writer's viewer prefs / catalog /Lang "en-US" is a ~2-line pypdf change
  that helps the site PDF (LinkedIn rasterizes, so no LinkedIn effect). Held
  because it touches the vector-PDF writer path and must be verified to not
  disturb the vector-text output the hard-fail gate checks; low value, so it
  waits for a slot where assemble.py is already open. Full PDF/UA tagging
  (structure tree, per-image alt, reading order) is a large unbounded effort
  on vector-drawn pages with no semantic DOM and is NOT recommended. Source:
  https://www.grackledocs.com/en/a-guide-to-wcag-standards-for-pdfs/

## 2026-07-13 - parked frontier candidate (headless-rendering scan)

- **Pin chromium-headless-shell / re-baseline on any Playwright upgrade
  (parked, watch item).** Playwright v1.49 removed Chromium's OLD headless
  mode; the NEW headless mode (real Chrome without a window) renders
  screenshots DIFFERENTLY and the Playwright team explicitly says to update
  all screenshot expectations after upgrading. Playwright ships a separate
  chromium-headless-shell build (install --only-shell) that keeps the old,
  lighter, deterministic behavior render.py currently relies on. This engine
  pins nothing and re-baselines nothing, so a future Playwright/Chromium bump
  in the cloud environment could silently shift PNG output, kerning, WebGL
  behavior, and every pixel gate's baseline at once. Parked (not a defect
  today; the installed Playwright still uses the shell path): when the
  environment's Playwright is upgraded, either pin chromium-headless-shell or
  re-verify examples/demo-deck + examples/proof-3d visually and re-baseline
  the busy-art/contrast noise floors BEFORE trusting a green run. Sources:
  https://github.com/microsoft/playwright/issues/33566 ,
  https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/check

## 2026-07-14 - craft refresh (LinkedIn saves + isometric geometry)

- Saves are among the strongest 2026 LinkedIn distribution signals, and a
  clear NUMBERED framework (a titled, enumerated set the reader can act on)
  is one of the most consistently SAVED B2B document formats. When a story
  supports it honestly, a numbered spine (N steps / N rooms / N forces) is a
  save-bait structure worth reaching for, without ever faking enumeration.
  Sources: https://www.oktopost.com/blog/linkedin-carousel-pdf-best-practices/ ,
  https://www.socialpilot.co/blog/linkedin-carousel
- Isometric projection (three axes at 120 degrees, equal foreshortening) is
  a fresh hero geometry available to this deck series: pseudo-3D depth from
  a purely 2D SVG/Canvas draw, no GL frame required, and it reads as a
  built system (a grid, a campus, a network) rather than a camera-map or a
  raymarched hero. Keep line-weight and shading layered per the doctrine
  ladder. Source: https://fastercapital.com/content/Visualization-Techniques--Isometric-Projection--A-New-Angle-on-Data-Visualization.html

## 2026-07-14 - retro (Carousel No. 7, "The Anchorage Address", 8.95)

- DEGRADED SOLO RUN. All studio subagents (scout, fact-checker, treatment,
  copywriter, pixel-critic, flow-critic, scorer, upgrade-engineer) died on the
  account weekly usage limit ("resets 5pm UTC"). Main-loop WebSearch/WebFetch
  and the Gmail/GitHub MCP tools kept working, so the showrunner ran every
  phase solo and still shipped. The binding risk in that mode is main-loop
  budget, not any one subagent; the pipeline degrades to a one-operator studio
  cleanly.
- STORY. An Alaska-incorporated, Anchorage-HQ, Native-owned SBA 8(a) firm
  (ReconCraft) won a $24.96M sole-source Navy contract for autonomous
  low-profile vessels, built in Clackamas, Oregon. The sharpest honest angle
  was the gap between Alaska's paper footprint (ownership, 8(a), address) and
  its physical one (the Oregon shipyard). FAR 19.805-1(b)(2) tied the
  sole-source basis directly to the 8(a) status.
- CRAFT. The waterline-as-both-physics-and-argument metaphor carried the deck
  on one fixed-y line plus sonar rings, no GL required. Canvas-2D orthographic
  hero instead of a rendered-ladder GPU hero, by reliability choice; that is
  the run's scored growth edge.
- HONESTY GUARDRAIL. ALPV spec figures are the vessel CLASS's documented
  numbers (Leidos/DIU/Marine program), not ReconCraft's unspecified design, and
  every specs slide says so. Autonomy framed as uncrewed remote plus waypoint
  today with future autonomy, never full AI self-piloting.
- DATE BOUNDARY. Trigger fired at Anchorage 2026-07-13 20:10 after the 07-13
  edition had already shipped; dated this run 2026-07-14 to avoid a same-date
  collision. Watch for this at the day boundary.

## 2026-07-17 - upgrade-engineer scan (parked candidates)

- PARKED (frontier, editorial cartography): 2026 news-graphics desks converge
  on MINIMALIST maps for the map-hero decks this studio ships (akgeo.js). A
  reusable convention set worth building when a map-heavy deck's artwork-craft
  is the growth edge: calm background (warm light grey / soft beige / very pale
  blue), ONE to two accent colors for the focal region only, LIGHT relief
  (soft gradient or faint contour-inspired lines, simple water texture) instead
  of a loud high-contrast hillshade, label ONLY narrative-referenced features,
  a small locator inset (globe/wider-context highlighting the focal region),
  and an optional scale bar. News-map content analysis puts real desks at scale
  bar 31.2% / inset 28.1% / legend 25% / north arrow 18.8% prevalence, so an
  inset + light relief are the highest-leverage additions. Overlaps the parked
  relief-depth helper (2026-07-15) and map design-space reference (2026-07-10);
  build as one akgeo helper with A/B across two map decks before adopting.
  Sources: https://www.onestopmap.com/blog/minimalist-editable-vector-maps/ ,
  https://www.researchgate.net/publication/405348439_Designing_Maps_in_News_Stories_A_Longitudinal_Visual_Content_Analysis_of_Cartographic_Design_in_US_Data_Journalism
- PARKED (reactive, deferred): AK3D landscape-hero framing helper. The S6
  terrain hero this run needed two hand-reframes (valley too low + too dark,
  large near-black dead mid-band; fixed by brightening the valley floor and
  raising the horizon via smaller cy / lower pitch magnitude). Reusable
  helper = auto-place horizon in the upper third and lift valley-floor
  luminance above a dead-band threshold, mirroring AKT.objectHero (2026-07-12).
  Edits shared 3D craft; wants multi-deck A/B, so held to an improvement slot,
  not forced into a daily budget. Instinct ak3d-terrain-hero-resolves-flat
  already logged.
- MAINTAINER NOTE (not an upgrade): config/scoring_rubric.yaml criteria
  weights sum to 1.10, so weighted totals run ~10% high vs a nominal 0-10
  scale (this run 9.07; normalized ~8.25). Renormalizing weights or restating
  the 8.3 threshold is a gate change and is the maintainer's call, not made
  autonomously.

## 2026-07-18 - retro (Carousel No. 10, "On the grid, or off it", 8.90)

- STORY. The kitchen-table data-center question, corrected: will an Alaska data
  center raise your power bill? The honest answer splits on one wire. Off-grid
  North Slope (STAK) self-generates behind the meter, disconnected from the
  Railbelt, so it CANNOT raise city bills (the misconception behind 500-plus
  angry comments). The on-grid project the state just advanced (AIDEA's ~30 sq
  mi Mat-Su transfer, July 16-17) can, and there a big load either spreads fixed
  costs and LOWERS rates (per a Launch Alaska op-ed) or competes for scarce gas
  and RAISES them, decided by the rate deal. The gap: Anchorage adopted AO
  2026-27 (10 to 2) while the statewide bill HB 259 sits in the House Energy
  Committee. Both Beat A and Beat F independently converged on this as the
  send-to-a-coworker story.
- CRAFT. New hero: an ISOMETRIC WIRING-DIAGRAM built-system with ONE conduit
  motif that changes shape every slide (cut/junction/severed/snap/fork/baseline/
  dormant/solid-vs-dashed/sealed) + a gold progress tick + edge-tease. The
  strongest story-art fusion move: the off-grid subject rendered as a DETACHED
  slate slab with NO glow makes "disconnected = cannot touch your bill" legible
  at 432px with zero words (story-art fusion scored 9). Fresh iso hero, never a
  series signature; diverged from all last-4 heroes; offline pure-Canvas iso, no
  GL race.
- GROWTH EDGE (recurring). Artwork-craft capped at 7 again: the S5 FORK hero,
  the deck's own designated depth showcase, read as a FLAT two-arrow schematic.
  The iso chassis broke the flat-hero weakness on S3/S4 (raised slabs/boxes with
  three-face light + cast shadows read dimensional) but NOT on S5, where a flat
  gold disc + a barely-visible DOF-blurred grid stayed flat. Lesson (new
  instinct iso-focal-node-needs-raised-base): give the one hero node a genuinely
  raised 3D pedestal (three-face base + real contact shadow) and make the DOF
  grid present enough to read. Held to a logged lesson, not re-opened post-score.
- HONESTY. C4 (Chugach 1%/yr, 2.3% in 2025, $2.5M per 1%) is an attributed
  Launch Alaska op-ed, flagged on-slide on S5 ("Launch Alaska argues") AND inside
  the S6 card frame ("PER A LAUNCH ALASKA OP-ED, ADN, APRIL 2026"); the two rate
  arrows were rendered EQUAL so the deck favors neither outcome. AO 2026-27
  (adopted, solid gold, 10-to-2 bar) vs HB 259 (in committee, dashed phantom
  void) encodes "Anchorage acted, the state has not" without overclaiming. No
  AKLNG-buyer claim. Fact-checker caught and corrected SB 250 -> HB 259 and
  dropped an unverifiable Cook-Inlet-gas-share figure.
- RECORD-SYNC. copy_sync_check caught 6 real drifts after the pixel-polish
  hand-edits (readout "MMcf gas / day" -> "per day"; the shortened S4 parcel;
  the S6 kicker/card-header/annotations that are separate rendered elements);
  reconciled copy.json to the shipped render before ship. The check earns its
  place every run there is a hand-edit.
- MAINTAINER WATCH-ITEM (from the scorer). This is the 4th deck touching
  data-centers-and-electricity (Nos. 1, 4, 6, 10). The frame here is genuinely
  distinct (ratepayer economics / on-off-grid), but if audience data shows topic
  fatigue, space these out.

## 2026-07-18 - upgrade-engineer scan (LinkedIn platform focus, parked candidates)

Frontier focus = LinkedIn platform / algorithm 2026 (rotated off the last three:
self-improving-pipeline 07-14, procedural-relief 07-15, editorial-dataviz 07-17).
The whole document-carousel strategy is REVALIDATED, not threatened: PDF/document
posts remain the single highest-reach native format (reported ~6.60% engagement;
3-6x the reach of text/image/video), and the March 2026 "Authenticity Update" +
the 360Brew ranking model reward exactly what this studio already makes (topical
depth, real dwell time, honest non-baity copy). Current specs are compliant:
9 slides sits in the reported 8-10 sweet spot (engagement drops after slide 10);
2160x2700 is portrait 4:5, the recommended feed ratio; the 80px safe zone beats
the >=50px minimum. No machine change is bounded enough for the daily budget
(the reactive copy_sync_check fix took the slot), so the levers are PARKED:

- PARKED (strategy -> possible scorer/gate improvement): SAVES are the dominant
  2026 ranking signal (reported ~5x the reach of a like, ~2x a comment), and
  infographics are now the single most common format among top-1% posts (28.6%).
  The lever is SAVE-WORTHINESS: is any single slide a keepable, screenshot-worthy
  reference on its own? The routine already prizes "a keepable data slide"; the
  bounded upgrade candidate is to make it explicit -- a storyboard-gate line and
  a scorer descriptor asking "would a reader SAVE this slide as a standalone
  reference?" Wants careful wording so it does not become a checkbox; hold to an
  improvement slot. Sources: https://www.oktopost.com/blog/linkedin-carousel-pdf-best-practices/ ,
  https://www.dataslayer.ai/blog/linkedin-algorithm-february-2026-whats-working-now
- PARKED (maintainer strategy note, NOT a machine change): the external-link
  penalty escalated in 2026 -- posts with an outbound link see ~60% less reach,
  and as of early 2026 even the "link in first comment" workaround reportedly
  carries a residual penalty. This studio puts source URLs in the first comment
  for integrity, which is non-negotiable, so this is a disclosure for the
  maintainer, not something the machine should auto-change. Possible mitigations
  worth a human decision: post the sources comment a few minutes AFTER the deck
  rather than instantly, or lead the caption with the debate/question and keep
  the link block purely in the comment (already the practice). Source:
  https://www.dataslayer.ai/blog/linkedin-algorithm-february-2026-whats-working-now
- CONFIRMED, NO ACTION: dwell time is heavily weighted and each swipe counts, so
  the tightly-paced one-point-per-slide + alternating text/visual rhythm the
  storyboard gate already enforces is the correct dwell play; polls collapsed to
  ~0.07% engagement (the studio never uses them). Nothing to change.

## 2026-07-18 - reactive gap for next Phase 12 (gmail_draft copy fields)

- RECURRED (logged 2026-07-17, bit again 2026-07-18): scripts/gmail_draft.py
  reads copy.get('post_copy') and copy.get('aftercare'), but the copywriter
  agent + Phase 6 emit 'caption' (the post text) and no 'aftercare'. Result:
  the "Paste the post copy" block and the Aftercare checklist render EMPTY in
  the draft unless the showrunner hand-adds post_copy=caption and an aftercare
  list to copy.json before running gmail_draft. The showrunner patched it in
  the moment this run. Bounded permanent fix for a future Phase 12: make
  gmail_draft.py fall back post_copy -> caption when post_copy is absent, and
  synthesize a default aftercare checklist from CAROUSEL_CRAFT (or have the
  copywriter emit both fields). Weakens no gate; removes a recurring manual
  step. Held this run because Phase 12's daily budget was taken by the
  copy_sync_check list-form fix.

## 2026-07-19 - craft refresh (annotation hierarchy on data slides)

Fresh EuroVis 2026 practitioner study on visualization annotation, useful for
this studio's keepable data slide:
- Attention plan, not a pile: pick ONE primary annotation, give it the strongest
  placement and emphasis so it reads first; keep every other annotation
  consistently secondary via lighter weight and reduced salience. Busy-ness reads
  as amateur.
- Annotate next to the data, not in a detached legend or keyed list. For any
  small-multiples panel, label in place rather than off to the side.
- LinkedIn platform side: no change from the 2026-07-18 scan (documents still the
  highest-reach format, saves the dominant signal, 7 to 10 slides the sweet spot).
  Logged nothing new there.

## 2026-07-19 - run retro (Carousel No. 11, permafrost digital twin, 8.81)

Story: a Penn State physics-informed ML digital twin of ONE Utqiagvik permafrost
road embankment (two buried 1 km fiber cables, 3 winters of thermal/seismic data).
Chosen as a net-new topic over an in-window STAK data-center re-touch (11 days after
No.1, would have been the 5th data-center deck) to protect feed variety. Single-source
(Phys.org; the JGR paper was paywalled/HTTP 402), framed honestly on-slide and in the
first comment; ~5 weeks old, framed as recent research not breaking news.

- WON: the first genuinely rendered PBR hero of the recent series (S4 akthree cable-in-
  gravel still-life, film-graded), which the scorer said resolves the flat-hero weakness
  flagged across Nos. 8-10. Best-in-class story-art fusion per the scorer: the lone gold
  tick on a vast empty plain plus the SOURCED vs NOT CHECKED evidence tags render the
  single-source honesty as a visual argument.
- FIBER-CORE CRAFT: an emissive core tube placed INSIDE a larger jacket tube renders
  invisible. Place the glowing core riding the jacket top CROWN (center y ~ jacket_center
  + 0.85*radius) so it reads as a lit fiber, and keep the emissive hue cyan with bloom
  strength <= ~0.45 or it blows out to white/chrome (pixel critic flagged the white read).
- THREE ENGINE-CRAFT GOTCHAS (now instincts): (1) a classic body <script> runs before
  later-in-body elements exist -> getElementById(grain) returned null and failed 8 of 9
  slides; put touched elements before the scripts. (2) canvas fillText labels fail
  copy_sync_check AND the vector-PDF contract; set every label in DOM/SVG. (3) an inline
  appended <svg> needs display:block or it trips body_overflow (S1/S9).
- WATCH-ITEM (scorer): factual weight scored 7 (single-source) and dead lower zones on
  S5/S8/S9 held artwork-craft at 8. Next permafrost-style deck: corroborate a second
  independent source before build, and fill empty diagram regions with graded texture/depth.
- REACTIVE GAP STILL OPEN (logged 2026-07-17/18, held again): gmail_draft.py reads
  copy.get('post_copy') and copy.get('aftercare'); copy.json now carries both (added this
  run), but the permanent fallback fix in gmail_draft.py is still a Phase 12 candidate.
  [RESOLVED by upgrade(2026-07-19): gmail_draft.py now falls back post_copy -> caption and
  synthesizes a default aftercare checklist when the fields are absent.]

### Phase 12 PARKED candidates (2026-07-19)

- PARKED - slide-authoring "element referenced before it is defined" lint. D1 this run:
  a classic (non-module) body <script> ran at parse time and did getElementById on a
  grain <div> placed AFTER it, failing 8 of 9 slides ("Cannot read properties of null").
  render.py already hard-fails on this (page_errors -> exit 1), but late (post-render). A
  pre-flight static lint could catch it earlier, BUT a reliable one must model defer /
  module (deferred by default) / DOMContentLoaded / script-after-element guards or it
  false-positives, so it is parked. Bounded near-term win instead: a SKILL.md slide
  contract rule -- "any element a parse-time classic script touches must appear before
  that script, OR wrap the script in DOMContentLoaded / make it type=module / place it
  last in body." Sources: https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById
- PARKED - body_overflow diagnostic hint. D3 this run: an inline appended <svg> carries a
  baseline line-box and tripped render.py body_overflow on S1/S9 (fixed by
  "#map svg { display:block }"). render.py already hard-fails body_overflow; the marginal
  improvement is to append "(common cause: an inline <svg>/<canvas> baseline line-box; try
  display:block on it)" to the body_overflow message so the author does not rediscover the
  one-line fix. Held: diagnostic-only, no defect can ship, low ROI for an upgrade slot.

## 2026-07-19 - reactive gap for next Phase 12 (score_report key names)

gmail_draft.py reads score.get('ship'), score.get('threshold'), and
score.get('weakest_criterion'), but the scorer agent emits 'ships',
'ship_threshold', and 'weakest_criteria' (list). Result this run: the draft
first rendered the orange "Shipped below threshold. 8.81 / 10 vs ?. Weakest: ?"
banner even though 8.81 is ABOVE the 8.3 threshold. The showrunner hand-added
the alias keys (ship/threshold/weakest_criterion) to score_report.json and
regenerated. Bounded permanent fix for a future Phase 12: make gmail_draft.py
accept either key spelling (ship||ships, threshold||ship_threshold,
weakest_criterion||weakest_criteria[0]), OR have the scorer emit both. Weakens
no gate; removes a wrong-banner risk. Held this run (Phase 12 budget spent on
the two applied fixes).
[RESOLVED by upgrade(2026-07-20): gmail_draft.py now resolves ship via
ship||ships, threshold via threshold||ship_threshold, and weakest via
weakest_criterion||weakest_criteria[0] through a local _alias() helper, so an
agent-native score_report renders the correct banner with no hand-editing.]

## 2026-07-20 - Carousel No. 12 "Written in Pencil" (8.55, shipped, merged)

Clean run: no usage-limit degradation, no environment breakage, no retries; the
akthree GPU pencil hero (S5) rendered. Scorer weakest criterion was artwork
craft (7): 8 of 9 slides are deliberately flat editorial argument with one
rendered hero, and the hero reads slightly like a gold rod without a fully
distinct graphite writing tip (logged growth edge, not gate-level).

- COMPOSITION BLIND SPOT (recurring, confirmed via machine_qa.json): S6's
  headline overprinted the ISOTYPE grid of SVG <rect> marks and BOTH the
  text-vs-text collision gate (07-08) and the PNG busy-art edge-density
  tripwire (07-10) passed it clean -- only the pixel critic caught it. The grid
  rects are low-contrast enough that bg edge density under the headline glyphs
  stayed below the 0.03 warn floor. Same class as canvas/SVG art invisible to
  the DOM text-vs-text walk.
- Minor recurring (authoring discipline, not gate-level): two bodies wrapped to
  4 lines vs a 3-line dossier target (render.py reports line boxes); several
  data-decorative kickers/labels at 18-23px pass qa as data-decorative;
  low-contrast gold counters (~1.5-2.9:1) on lit-paper slides pass qa because
  they are data-decorative furniture (parked 07-11 contrast-floor idea).

### Phase 12 PARKED candidates (2026-07-20)

Frontier focus: typography / layout craft (last touched 2026-07-09; distinct
from the last four foci procedural-relief 07-15, editorial-dataviz 07-17,
LinkedIn-platform 07-18, headless-Chromium 07-19).

- PARKED - SVG/DOM TEXT-HALO helper (the aklabel.js analogue for vector text).
  aklabel.js gives canvas-drawn labels an opaque knockout plate, but DOM/SVG
  text sitting over SVG marks (this run's S6 headline over the ISOTYPE grid; any
  label over relief/chart marks) has no equivalent. The settled dataviz
  technique is a TEXT HALO: a contrasting-color outline behind the glyphs so
  contrast depends on (text, halo) not the art beneath. Concrete portable
  implementation, no new dep: SVG <text> with stroke=<halo-color>,
  stroke-width ~= 0.12-0.18em, stroke-linejoin=round, and paint-order="stroke
  fill" so the halo paints behind the fill (single element, no duplicate);
  halo color auto-picked near-black/near-white from the text luminance, mirroring
  aklabel's plate rule. Held: it is an IMPROVEMENT not a reactive fix (the daily
  0-1 budget was taken by the score-key fix), and it edits shared rendering craft
  wanting a multi-deck A/B. Sources:
  https://data.europa.eu/apps/data-visualisation-guide/text-halos ,
  https://courses.ems.psu.edu/geog486/node/557
- PARKED - text-over-SVG-mark QA warn (bounding the S6 blind spot). A gate that
  intersected primary text boxes against non-text SVG marks (<rect>/<path>/
  <circle>/<line>) would catch the ISOTYPE-grid overprint the two existing gates
  miss, BUT it false-positives on the many slides where text legitimately sits
  over background panels, cards, and chips. Not safely boundable this run without
  a mark-intent attribute (a data-mark or data-overlap-ok on the art, analogous
  to the text-side data-overlap-ok the 07-08 gate already honors). Bounded near
  term is authoring guidance instead: put a halo (above helper) under any
  headline that crosses a mark field. Held pending the intent-attribute design.
- PARKED - tabular lining figures on number-heavy stat slides. Datawrapper /
  Type Network confirm tabular figures (font-feature-settings "tnum" 1, or a
  lining/tabular numeral style) align numerals in columns and all-cap headline
  settings; several stat slides (S8 borough list, S6 step numbers) would read
  cleaner with tnum locked on. Craft note, not a gate. Sources:
  https://www.datawrapper.de/blog/fonts-for-data-visualization ,
  https://typenetwork.com/articles/opentype-at-work-figure-styles
- RECONFIRMED (no change): CSS text-wrap: balance/pretty still do NOT guarantee
  a headline line count nor prevent overflow, and pretty ignores widows (Chrome
  for Developers / MDN, Sept 2025) -- so aktype.js AK.fitText (JS binary-search
  fit-to-box) remains the correct headline mechanism, unchanged since 07-09. The
  4-line body overflow is authoring discipline, not a wrap-CSS fix.

## 2026-07-21 - upgrade-engineer scan (generative/procedural art focus, parked candidate)

Frontier focus: generative/procedural art portable to offline Canvas/SVG (last
touched 2026-07-11; distinct from the last three foci LinkedIn-platform 07-18,
headless-Chromium 07-19, typography 07-20). Chosen to serve this run's recurring
weakness from a second angle: when the GPU akthree hero falls back to Canvas
(as S6's beluga did this run), the 2D fallback reads FLAT and caps artwork-craft
at 7. The reactive snapshot fix (below) makes the GPU path survive more often;
this parked helper would raise the FALLBACK floor so even the Canvas path reads
dimensional.

- PARKED - 2.5D RELIT-HEIGHTFIELD FORM-SHADING helper (a canvas hero that reads
  as sculpted volume with NO GPU, over the already-committed noise.js). The
  settled portable technique, all over the frontier (mattdesl ShaderLesson6,
  the pixel-art normal-map compilation arXiv 2212.09692, the web 2.5D dynamic-
  paintings pipeline arXiv 2311.15354): build a procedural HEIGHTFIELD (noise.js
  AK.fbm2 / warp2, already committed), derive a per-pixel NORMAL from the height
  gradient via a 3x3 Sobel (N = normalize(-dH/dx, -dH/dy, 1/strength)), then
  LAMBERT-shade in 2D: intensity = ambient + max(dot(N, L), 0) * diffuse, with L
  built per-pixel from a light position and a light-Z (the depth that gives the
  form its roundness) and an optional 1/(c + l*D + q*D^2) attenuation. Result: a
  flat filled silhouette becomes a shaded, dimensional form, offline, ~100 lines
  of vanilla JS, ZERO new deps (pure ImageData math over the committed noise
  primitives). This is the exact 2D analogue of akthree.objectHero's rim-carve
  and would give the Canvas fallback (and any 2D relief hero) a real sense of
  volume instead of the flat blob that keeps capping artwork-craft at 7.
  Held (PARKED, not applied) because: (1) it is an IMPROVEMENT not a reactive
  fix and the daily 0-1 budget was taken by the snapshot coverage fix below;
  (2) it edits shared rendering craft that wants a careful multi-deck A/B (pick
  light-Z / strength / ambient defaults that read across dark AND light decks)
  before it becomes a committed helper; (3) it overlaps the parked relief-depth
  helper (2026-07-15) and the strata-texture/rim-light helper (2026-07-11) --
  the three should be designed together as one form-and-relief craft module over
  noise.js rather than piecemeal. Next improvement slot after a reactive-light
  day is the place to build and A/B it. Sources:
  https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson6 ,
  https://arxiv.org/pdf/2212.09692 , https://arxiv.org/pdf/2311.15354
- NOTE (dead end, recorded so it is not re-scanned): hardware normal-mapped
  sprite lighting (SpriteIlluminator, PixiJS/Phaser normal pipelines) needs a
  WebGL fragment shader and pre-baked normal textures -- not portable to pure 2D
  canvas and off-policy (external asset pipeline). The Sobel-from-procedural-
  height path above is the offline, dependency-free form that fits this studio.

## 2026-07-22 - craft refresh (cartographic direction pass)

- If a data/choropleth slide ships this run, pick the class-interval method
  deliberately and NAME it in the dossier (natural-breaks/Jenks for skewed
  Alaska data, quantile only when comparing rank, equal-interval for evenly
  spread values); the method silently changes the map's argument. Use a
  single-hue SEQUENTIAL ramp for magnitude, a two-hue DIVERGING ramp only
  around a true midpoint. Strip decoration: no default legends, no county
  borders louder than the data. Sources:
  https://handsondataviz.org/design-choropleth.html ,
  https://www.directionsmag.com/article/3363
- LinkedIn 2026 sources reconfirm the existing numbers (8-10 slides, one idea
  per slide, hook first, single CTA, first-hour comment replies); no change to
  CAROUSEL_CRAFT.

## 2026-07-22 - retro (No.14 "The Giveaway, Surveyed", AIDEA Houston land conveyance)

- SHIPPED 8.86 vs 8.3, 9 slides, vector PDF 8.82MB, zero hard fails, honesty pass.
  Full studio ran clean end to end (6 scouts, fact-checker, 3 treatment-directors,
  copywriter, 5 pixel critics all "ship" round 1, flow-critic "ship", scorer).
- WHAT WORKED: the cartographic parcel-motif chassis (oblique AK3D boreal
  hillshade-relief + ONE gold cadastral parcel that changes state every slide +
  top-down PLAT register for data/process beats) diverged cleanly from the last 4
  decks and scored story-art-fusion 9 and variety 9. The 8-vs-639 ISOTYPE and the
  S6 "city limit stops 2 mi short of the parcel" map are the strongest fusion beats.
- HONESTY: the DNR primary notice never printed "data centers"; rendering the
  attribution as an on-slide chip (PER THE PROJECT DECISION AND LOCAL COVERAGE) and
  crediting 8/639 on-slide (AS REPORTED BY ...) turned the fact-checker's flags into
  visible design and passed the scorer honesty check. Reusable pattern.
- RECURRING CEILING (two runs now): artwork-craft capped at 7 by an underbuilt hero.
  A flat SVG polygon "raised plate" does NOT read as raised even with two stacked
  drop-shadows, and the low-poly AK3D heightfield reads coarse under zoom. Next
  LAND-hero run should build the parcel as a REAL extruded solid (side face +
  contact shadow) OR finally build+A/B the parked 2.5D relit-heightfield Sobel
  form-shading helper (parked 07-21). This is the single highest-value craft upgrade.
- Flow fix that helped: slide 5 (THE BET) originally echoed slide 3's message; trimming
  it to a lighter 2-line assertion carried by the phantom-footprints graphic fixed the
  4->5 junction and gave the dense 2-6 stretch a micro-breath. Tethering the S4 ISOTYPE
  outlier with the coord footer + edge-tease kept it inside the sequence.

## 2026-07-22 - upgrade-engineer (parked helper BUILT; editorial-cartography scan)

- APPLIED (was PARKED 2026-07-21): the 2.5D relit-heightfield Sobel form-shading helper
  is now committed as assets/js/akrelief.js (AK.reliefShade). It attacks the recurring
  artwork-craft=7 ceiling (flat hero two runs running) directly: a flat filled region
  becomes a shaded dimensional SOLID via heightfield -> 3x3 Sobel normals -> Lambert,
  zero new deps (pure ImageData over noise.js). Verified on two smoke slides (noise
  boulder std 53.2; smooth NW-lit dome std 58.4, NW/SE rim ratio 2.62), render+qa PASS,
  demo-deck + this run's slides unchanged. NEXT LAND/object-hero run: reach for
  AK.reliefShade instead of a flat SVG polygon + drop-shadows. strength is a gradient
  multiplier (noise fields ~2-6; smooth macro dome/bevel ~60-200); putImageData REPLACES
  pixels so shade on its own layer. Still open to design as one module with the parked
  relief-depth helper (07-15) and strata-texture/rim-light helper (07-11).
- FRONTIER (editorial dataviz/cartography, last touched 07-17): multidirectional
  oblique-weighted hillshade (MDOW: azimuths ~225/270/315/360, aspect-weighted) is the
  settled way to make relief read rich without one harsh light (ArcGIS Terrain Tools
  origin; MapTiler 2026-02 4-direction hillshade; Eduard Cloud v1.0 ML Swiss-style).
  Adopted as the {multidirectional:true} option in akrelief.js; single NW key stays the
  default for object roundness. Cadastral-map minimalism (one accent for the focal parcel,
  no legend/border louder than the data) reconfirmed the chip-attribution practice, no
  change. Sources:
  https://www.maptiler.com/news/2026/02/multidirectional-hillshades-and-terrain-color-ramps-for-web-maps/ ,
  https://gist.github.com/maning/28ad9ebb1dcb1ea85440 , https://eduard.earth/ ,
  https://github.com/mattdesl/lwjgl-basics/wiki/ShaderLesson6

## 2026-07-23 - craft refresh (No.15)

- LinkedIn 2026 reconfirms the settled numbers (8-10 slides, hook first, one
  idea per slide, single CTA, first-hour comment replies). Fresh data point
  worth keeping in mind, not a doctrine change: AuthoredUp's analysis of ~3M
  posts (Mar 2025 to Feb 2026) puts document/carousel engagement highest of
  any format (~6.6%, ~39% more reach, ~30% more engagement than average), and
  SAVES are now ~5x the weight of a like. Design one genuinely keepable
  reference slide per deck (the "save this" beat), and keep display type
  legible at the 432px feed thumbnail, not just at 1080. Sources:
  https://www.oktopost.com/blog/linkedin-carousel-pdf-best-practices/ ,
  https://www.getcreator.io/stats/linkedin-carousel-benchmarks
- Small multiples reconfirmed as the right form for multi-entity/multi-place
  comparison (one shared scale, a grid) over a single cluttered chart, useful
  if this run's story is multi-base or multi-region. Source:
  https://en.wikipedia.org/wiki/Small_multiple

## 2026-07-23 - retro (No.15 "Governed First", Alaska Native tribal-health AI governance)

- SHIPPED 8.90 vs 8.3, 9 slides, vector PDF 2.8MB, zero hard fails. Full studio ran
  (6 scouts, fact-checker, 3 treatment-directors, 2 caption-directors + caption-critic,
  copywriter, 5 pixel-critics, flow-critic, scorer). Machine QA PASS, caption_check PASS,
  copy_sync_check PASS.
- DEDUPE SAVE (the run's biggest lesson): the intended lead, the XPRIZE Wildfire
  autonomous-response finals near Nenana, was a near-exact dupe of No.5 (07-12, "First
  Machine to the Fire") 11 days earlier, same competition, ACUASI, 1,000 sq km range,
  detect-decide loop, September verdict. It slipped the first dedupe pass because the
  topics-list title showed truncated ("Alaska as the world's proving ground for"); caught
  only via a TECHNIQUE_LIBRARY note that named the prior deck. Three treatment-director
  pitches (all strong) were voided and the room re-tasked (via SendMessage, staying within
  the 3-director cap) onto the replacement story. FIX for next run and an upgrade candidate:
  a Phase-4 entity/keyword cross-check against the FULL topic text of the ledger, not titles.
- STARVED WINDOW, HONEST PIVOT: late-July interim + a burned top pick left the window thin
  for fresh in-window AI-core Alaska news. Went with the strongest available true story, a
  peer-reviewed IJCH paper (2026-05-23, ~9 weeks old) on how the Alaska Native tribal health
  system governs AI under Indigenous data sovereignty. Framed explicitly as governance
  context, not breaking news, and as SINGLE-SOURCE, on-deck (S8 58e evidence tags, persistent
  provenance stamp) and in the first comment. The scorer accepted the honesty as genuine craft.
- WHAT WORKED: the gold AUTHORITY SEAL chassis (a rendered akthree GPU-PBR embossed disc that
  recurs as a state machine, and ties gold=authority across the deck) diverged cleanly from
  the last 4 decks and scored story-art-fusion 9. The honesty architecture (DEPLOYED Cerner AI
  Scribe vs PROPOSED medevac model as solid-green vs dashed-slate on S4; n=31 snapshot stamp
  on S6; S7's chart that plots ONE real 2022 point and refuses to fabricate a 2025 number)
  turned a thin single source into a trustworthy deck.
- CRAFT CEILING (again): artwork-craft capped at 7 because 8 of 9 slides are flat editorial/
  data off the single rendered seal, with some dead lower zones (S2/S4/S8/S9). Next governance/
  editorial deck should give 2-3 non-hero slides real dimensional depth (a second rendered
  object, relief/emboss on a data plate, or a filled lower third) rather than leaning the whole
  depth budget on one hero.
- CAPTION streak broken at last: 6+ runs of LEGACY STANDARD / hook-context-deckpointer /
  bolted-question gave way to DEFINITION SUBVERSION + PUNCH THEN PROOF + a who-decides close.
- CHART MISREAD RISK: a verified negative-framed metric ("share who had never heard") drawn as
  a falling line on an adoption slide can read as decline at a glance; a bold "awareness rose"
  arrow label fixed it without inventing the positive number.

## 2026-07-23 - Phase 12 frontier PARK (focus: self-improving-pipeline / agentic dedup)

- SHINGLE + MinHash near-duplicate signal for dedupe_check.py (PARKED, candidate refinement).
  Today's reactive fix (scripts/dedupe_check.py) scores a candidate against the ledger by
  distinctive named-entity phrase overlap + keyword-token Jaccard. That is exactly right for
  this run's collision (XPRIZE/No.5 shared 9 named entities) and for the common case where two
  decks share proper nouns. The residual blind spot: a REWORDED near-dupe that shares almost no
  named entities or keyword vocabulary but tells the same story could still read "clear" under
  bag-of-words token overlap. The settled robustness upgrade is to add a character/token
  k-SHINGLE + MinHash-estimated Jaccard similarity signal (k=3-5 char shingles or ~5-word
  token shingles; near-dup threshold ~0.8 for full documents, but calibrate LOWER and against
  the ENTITY+ANGLE fields only for our short entries) as a SECOND cheap signal, keeping the
  cascade shape (cheap shingle screen -> shortlist -> the human reads the full entry, which is
  the studio's "LLM adjudication on candidates only" analogue). ~60 lines pure-Python stdlib,
  no deps (hash() over shingles, H=64-128 permutations via (a*h+b) mod prime). PARKED not
  applied because: (a) it is an improvement, not a reactive fix, and the daily 0-1 slot was
  taken by shipping+verifying dedupe_check.py itself; (b) it needs its own multi-case tuning to
  avoid false-positive FLOODING on a small ledger where many decks legitimately share the
  "who-decides / Alaska AI infrastructure" frame (a naive 0.8 threshold on 12 short entries is
  untuned); (c) it should be designed and A/B-verified together with, not bolted onto, the
  freshly-shipped tool. Also noted: 2026 self-improving-loop write-ups still store scars as
  PROSE reminders prepended to prompts; this studio's machinery-over-prose doctrine (a scar
  becomes an executable check, as today) is the stronger form and the scan reconfirmed it.
  Sources: https://arxiv.org/abs/2607.01601 (SemHash-LLM cascade: cheap hash screen, expensive
  check on candidates only), https://blog.nelhage.com/post/fuzzy-dedup/ (Jaccard+MinHash how-to),
  https://mattilyra.github.io/2017/05/23/document-deduplication-with-lsh.html (shingle sizes /
  LSH banding), https://www.analyticsvidhya.com/blog/2026/06/self-improving-loops/ (prose-lesson
  memory pattern, the weaker alternative to executable checks).

## 2026-07-24 - Phase 1 craft refresh (No.16)

- CONFIRM + SHARPEN (LinkedIn saves): 2026 practitioner data keeps finding that
  NAMED, reusable frameworks are the single most reliable save-driver on carousels
  ("The 3-C Framework", "The RICE Method"), because a save is a bet the reader will
  reuse the artifact. Our house move is the named motif plus a keepable data slide;
  this run, make the deck's ONE keepable slide read as a reusable tool (a named
  test, a labeled ladder, a checklist), not just a chart. Confirms existing doctrine;
  no rule change. Sources: postunreel.com/blog/linkedin-carousel-engagement-rate-statistics-2026,
  metricool 2026 study (via oktopost/socialpilot roundups).
- Nothing new on the cartography/relief craft front worth a doctrine change this pass
  (IJC 12.2 2026 covers genAI-in-cartography and 3D thematic geovis at a level already
  matched by our AK3D/hillshade bench). Parked, no action.

## 2026-07-24 - retro (No.16 "500 to Fewer Than 12. One Office Holds the Pen.", STAK North Slope revolt)

- SHIPPED 8.66 vs 8.3, 9 slides, vector PDF 3.39MB, zero hard fails. Full studio ran (6 scouts,
  fact-checker, 3 treatment-directors, 2 caption-directors + caption-critic, copywriter, 5 pixel-critics
  + a round-2 re-review, flow-critic, scorer). Machine QA PASS, caption_check PASS (898 chars), copy_sync PASS.
- THE RUN'S BIGGEST LESSON (a real miss): this is a SAME-DOCKET REVISIT of No.1 (2026-07-08), which
  anchored its four-rooms survey on this exact STAK docket (ADL 422741) with the SAME "500 wrote in,
  fewer than 12 said yes" cover. dedupe_check.py CAUGHT it (No.1 was the top match at jaccard 0.279),
  but I read the tool output with `tail -30` in Phase 4 and the No.1 line printed ABOVE the visible
  window, so I proceeded believing it cleared (I read No.10/No.14 lower down, not No.1). The scorer
  caught it from artwork.json. FIX applied this run: shipped honestly as an explicit post-comment-closure
  UPDATE (No.1 ran while comment was OPEN; the window CLOSED July 17, now pending final finding), with a
  cover peg "COMMENT CLOSED JULY 17. NOW ONE OFFICE DECIDES." and a loud maintainer flag in the email.
  PERMANENT FIXES: (1) instinct dedupe-never-tail (never tail/head the dedupe output); (2) Phase 12
  upgrade candidate: make dedupe_check print its single STRONGEST match in a LOUD summary line at the
  END of output so a tail cannot miss it.
- CRAFT WIN (the ceiling moved): distributing real depth across S3 (akthree GPU-PBR tundra-machine, lifted
  off near-black with dark-clay material + IBL + a bronze HemisphereLight bounce, low horizon, cab+bed
  pickup scale figure), S4 (honest cabinet-extruded +30% bars), S5/S7 (akrelief 2.5D relit sort cards +
  material chips), and S8 (SVG-emboss debossed unsigned-pen) got the scorer to call it "the strongest
  artwork craft the series has shipped." The hero no longer reads flat. The RESIDUAL ceiling is DEAD
  LOWER ZONES (S2/S5/S8/S9) and an intermittent comment-stack spine (flow-critic motif_reads_across_all_9
  false; partially patched with right-edge margin slivers on S4/S8). Next run: a lower-third-fill helper
  + a constant margin sliver and a visible pen-migration increment on every slide.
- HONESTY ARCHITECTURE that worked: the SORT (S5) grading objections, the fair correction (S6, the bill
  fear is weakest because the campus self-generates off the Railbelt, labeled Alaska.Ai analysis), the
  single-source lease-doc figures hedged "per the Northern Center" on every slide, no fabricated Railbelt
  MW figure, and the unsigned pen (pending final finding). Fact-checker rejected the Shinkei robot-salmon
  lead (in-window Alaska peg paywalled + no proof the robot runs on Alaska boats) - a good save.
- CAPTION: LEDGER TALLY / INVERTED PYRAMID / PRICE broke the streak cleanly; critic's one fix removed a
  verbatim-cover-phrase leak and a "500 to 12" overstatement.
- FRONTIER SCAN PARK (Phase 12, focus: LinkedIn platform/algorithm 2026; last platform scan 2026-07-18):
  The one genuinely NEW signal since the 07-18 scan is that carousel/document COMPLETION RATE ("how many
  slides people actually view") is now an EXPLICIT feed-ranking input, not just a dwell-time proxy: decks
  that lose viewers before the end are down-ranked, so the 8-10 slide sweet spot is now enforced by
  completion, not just reach decay, and cover/S1 must state clear value to protect through-rate. LinkedIn's
  360Brew LLM-embedding retrieval (searchengineland/ALM: rebuilt Q1-2026 feed, sub-50ms embedding
  retrieval, ranks by topical MEANING not keywords) rewards a narrow consistent topic - the studio's daily
  Alaska+AI focus already maximizes this. Everything else RECONFIRMS 07-18 (doc format ~6.6% engagement /
  highest; saves > comments > likes; ~60% external-link reach penalty; 2160x2700 portrait, 80px safe zone).
  WHY PARKED (not applied): all levers are strategy/craft, not a boundable machine gate - the studio already
  ships 9 slides (compliant with 8-10) so a slide-count gate would never fire, and "cover states clear
  value" / "front-load the hook" / "topical consistency" are subjective storyboard-taste calls, not
  verifiable checks. CANDIDATE for the maintainer: fold "protect carousel completion-rate (front-load cover
  value, hold 8-10 slides, no dead final slide)" into the Phase 5 storyboard objectives and the scorer's
  through-line criterion as PROSE guidance, and reconfirm the 07-18 external-link maintainer note. Sources:
  https://searchengineland.com/linkedin-updates-feed-algorithm-llm-ranking-retrieval-471708 ,
  https://www.dataslayer.ai/blog/linkedin-algorithm-february-2026-whats-working-now ,
  https://www.socialpilot.co/blog/linkedin-algorithm

## 2026-07-25 - Phase 1 craft refresh (No.17)

- COMPLETION RATE, now with a number. The 07-24 scan established that carousel
  completion is an explicit ranking input; this pass found the practitioner
  benchmark attached to it. Well-structured carousels average about a 36 percent
  completion rate (share of viewers who reach the last slide), and completion
  falls off hard past roughly 15 slides. Our 8 to 10 band is safe. The operative
  lesson is unchanged but sharper, every slide has to earn the swipe because the
  LAST slide's view count is a ranking input, not just a courtesy. Sources:
  https://usevisuals.com/blog/linkedin-carousel-engagement-statistics-2026 ,
  https://www.oktopost.com/blog/linkedin-carousel-pdf-best-practices/
- TREAT WITH SUSPICION, do not adopt: the same practitioner posts circulate a
  claim that "exactly 7 slides perform 18 percent better than any other length"
  while ALSO reporting 5 to 10 and 9 to 12 as the sweet spot in the same article,
  and quoting a carousel engagement rate of 1.92 percent against the 6.60 percent
  figure the same tier reports elsewhere. Internally inconsistent, no method
  published. No doctrine change. CAROUSEL_CRAFT's 8-10 band stands on the tier-B
  sources.
- NEW AND DECISION-RELEVANT (feed physics for a LIGHT deck). Practitioner
  guidance converges on dark covers outperforming light ones for FEED visibility,
  because LinkedIn shrinks the cover to roughly 200px in-feed and a dark, saturated
  field holds thumbnail contrast against the platform's own light chrome better
  than a light field does. That is tier-C evidence, not tier-A, and it does not
  forbid the light register brand.yaml permits once per 8 runs. It does set the
  price of admission, if a deck goes light, the COVER must carry an unusually
  large, near-black display headline plus one saturated accent mass, and it must
  be judged at 432px before anything else gets built. Dark text on light remains
  the readability gold standard once the reader is inside the deck. Sources:
  https://carouselli.com/blog/linkedin-carousel-colors ,
  https://carouselli.com/blog/linkedin-carousel-design ,
  https://postunreel.com/blog/linkedin-carousel-design-best-practices
- Type note, no action. The 2026 print and editorial trend reporting is all
  high-contrast and maximalist serif display, which the house already owns
  through Fraunces and Instrument Serif. Nothing here the library lacks.

## 2026-07-25 - retro (No.17 "On File, Off Record", AI money in the governor race)

- SHIPPED at a raw 8.22 against the 8.0 round-3 threshold, but the SCORE OF RECORD is
  6.9, capped by two hard fails from one geometry bug. Full studio ran: 6 scouts,
  fact-checker, 3 treatment-directors, 2 caption-directors + caption-critic, copywriter,
  4 pixel-critics, flow-critic, scorer x2. Machine QA finished PASS with zero warns,
  caption_check PASS (874 chars), copy_sync PASS, vector PDF 10 pages.
- STORY. First elections and campaign-finance deck of the series, and the first time
  AI-industry money is a measurable presence in an Alaska statewide race. Six Anthropic
  employees gave 372,000 dollars of the field's largest reported haul (1.8M), and the
  largest single gift of 100,000 came from an employee who grew up in Soldotna. The
  fact-checker DEMOLISHED my intended centerpiece (the in-state vs out-of-state split
  came only from a partisan page that now 404s) and that demolition improved the deck:
  the surviving thesis is the ASYMMETRY of the record itself, that money disclosure is
  compulsory and policy disclosure is voluntary. Reframing beat patching.
- THE RUN'S BIGGEST LESSON, and it is a gate lesson not a taste lesson. qa.py's
  collision check is DOM-only, so labels drawn against canvas geometry collide freely
  and still return PASS. This deck's OWN slide-02 dossier predicted it in a risk flag
  and it still shipped on four slides across two scoring cycles. Fixed structurally:
  every art-band label now ships on an opaque knockout by default. New instinct at 0.97.
- THE SECOND LESSON is geometric and cost two full rebuild passes. (a) Azimuth 0 in an
  orthographic camera projects a slab's top face to an axis-aligned RECTANGLE, which
  rendered as pale bands with no volume; azimuth 14 deg gives two side faces and two
  interior walls per recess. (b) A recess viewed obliquely hides a band of its own floor
  equal to the depth's screen projection, so an UNCLIPPED recess reads as a raised BLOCK.
  Three pixel critics independently reported "reads proud" before the cause was found.
  Clip recess interiors to the opening polygon, and remember marks at depth project
  lower, so anything near the near edge gets clipped away (this silently ate the hero's
  fireweed and gold until it was moved to the far half).
- PROCESS DEFECT WORTH FIXING. I spawned the pixel critics BEFORE appending the build
  reconciliation, so about a third of their findings were measured against superseded
  numbers. Reconcile the record first, then review. New instinct at 0.88.
- CRAFT VERDICT, honest. Artwork craft scored 6, which is BELOW the 7 ceiling of the
  last four runs, and the reason is instructive: the distribution strategy was right
  (all ten slides carry real side faces, groove walls, AO and two-part warm shadows,
  and there are no dead lower thirds for the first time in the series) but the defects
  landed on load-bearing elements, above all the hero. Distributing depth is necessary
  and not sufficient; the thesis frame has to be the most resolved frame, not the least.
- WHAT WORKED. The MILLED REGISTER chassis and its cut state machine (cut = the record
  exists and its length encodes dollars, scored = the record does not exist, proud =
  somebody else's decision) is genuinely inferable without instruction by slide 06, per
  the flow critic. The UNMEASURED BRACE, a dimension call with one extension line
  missing and a NOT DISCLOSED value field, is the best honest-absence device the studio
  has built. Fairness as GEOMETRY rather than as a footnote (slide 04 twinning slide 02
  at the same depth and scale, carrying the deck's largest quotation against itself) is
  the pattern to keep. And the four-register conflict disclosure (pointer chip where
  the name first appears, full plate at headline scale, caption paragraph, first-comment
  opener) should become the house pattern for any deck with a studio interest in it.
- STILL OPEN, disclosed rather than hidden: slide 02's scale bar never shipped so the
  money constant is not reader-verifiable; the hero's three money wells never shipped so
  it argues by symbol; c26 went unused; the sundial device reads weakly and should not be
  counted as a continuity device next run. The light-ground allowance is now SPENT.

## 2026-07-25 - Phase 12 frontier PARK + API-trap PARK (focus: accessibility / PDF and document formats)

Focus chosen by rotation (last accessibility/PDF scan was 2026-07-12, the stalest slot;
the last three foci were LinkedIn platform 07-24, self-improving pipelines 07-23,
editorial dataviz 07-22) and because this run's scar is a legibility defect.

- APPLIED this run (reactive, see ledger/upgrades.json): qa.py's new label-crossed-by-art
  FAIL. The scan corroborated its shape rather than inventing it: the settled rule for text
  over imagery is that the measurement must hold at the WORST-CASE point under the text, not
  on average, and the remedy ladder is scrim -> semi-opaque box behind the text -> halo or
  outline, with 4.5:1 (3:1 large) still the operative ratio. The new gate measures the ring
  immediately around the glyphs and names those three remedies in its failure message.
  Sources: https://www.nngroup.com/articles/text-over-images/ , https://webaim.org/articles/contrast/
- WORST-CASE-WINDOW CONTRAST for qa.py's contrast_estimate (PARKED, candidate tightening).
  contrast_estimate() estimates the background as the median of the pixels most unlike the
  text colour ACROSS THE WHOLE BBOX, so a dark rule or a bright specular crossing one third
  of a label is averaged away: the box-wide ratio can read a comfortable 8:1 while a 24px
  window inside it reads 1.6:1. The bounded design is to slide a window of about the cap
  height along each line box, compute the ratio per window, and report the WORST window
  (with a minimum window-ink count so a two-pixel window cannot dominate). PARKED because it
  changes an existing FAIL threshold applied to every text node in every deck, so it needs a
  multi-deck calibration pass (this run's 10 slides, demo-deck, proof-3d, and at least two
  older decks) to prove it does not flood; and because today's new ring-contamination gate
  already catches the acute case that actually shipped.
  Source: https://www.nngroup.com/articles/text-over-images/ (worst-case rule),
  https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- WCAG 3 / APCA still NOT a threshold source (checked, no action for about a year). As of
  April 2026 the WCAG 3 draft states the contrast algorithm "is yet to be determined"; APCA
  was pulled from the draft in 2023 and remains exploratory; WCAG 2.2 AA is the operative
  standard and finalisation estimates run 2029 to 2030. qa.py's WCAG2-style luminance ratios
  stay correct. Source: https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html
- TAGGED PDF for the DOWNLOADABLE artifact only (PARKED, low priority, honest payoff).
  Playwright 1.61's page.pdf() accepts tagged=True (verified against the installed signature:
  both `outline` and `tagged` are present) and Chromium has emitted tagged PDFs since Chrome
  85. But assemble.py prints ten single-page PDFs and merges them with pypdf, and a page-level
  merge carries no /StructTreeRoot, so the merged deck would gain nothing; preserving the
  structure tree across a ten-document merge is the hard half. And the platform payoff is
  ZERO: screen-reader testing of LinkedIn document posts finds the text is effectively OCR'd,
  heading levels survive only partially, alt text is acknowledged but never read out, list
  tags and reading order are lost, and there is no per-slide alt-text field for a multi-page
  PDF upload. The real payoff would be the PDF people download from alaskaaihq.com and the
  email. PDF/UA-1 remains the practical conformance target in 2026 (PDF/UA-2 tooling is still
  catching up). Sources:
  https://intopia.digital/articles/navigating-the-accessibility-challenges-of-linkedin-carousels/ ,
  https://pdfa.org/chrome-plated-pdfs-exploring-google-chromes-new-pdf-capabilities/ ,
  https://pdfa.org/european-accessibility-act-and-its-importance-for-pdf-accessibility/
- akthree TRANSPARENT-CLEAR DEFAULT (PARKED API trap, from this run's own scars, not the scan).
  This run's GL hero set scene.background = null expecting transparency and got OPAQUE BLACK,
  because a WebGLRenderer built without alpha clears black at alpha 1; a black frame on a bone
  deck, caught by eye. The bounded fix is inside AKT.setup: build the renderer with
  alpha: true always, and when opts.bg == null call renderer.setClearAlpha(0) so an
  unspecified background composites transparently over whatever the slide's 2D layer already
  drew. An explicit opts.bg still clears opaque, and AKT.snapshot's sentinel is unaffected
  (transparent pixels read as luminance 0, exactly like the black frame it already rejects).
  PARKED because it changes the shared GPU path for every future deck and deserves its own
  run's verification budget (two GL smoke slides, proof-3d, and the run deck) rather than a
  third slot in a run that already spent two on the label gate and the gate-status script.
- GOLD BEFORE AKPOST.grade comes out ACID (PARKED doctrine + helper candidate). #FFC72C drawn
  into the canvas BEFORE AKPOST.grade is pushed yellow-green by the ACES tone map. This run
  fixed it by deferring brand gold to a post-grade pass. Two durable options: a documented
  rule (brand accents are always drawn after the grade) or an akpost protected-swatch pass
  that re-asserts named brand colours after grading. Doctrine first, helper only if it recurs.
- DEPTH-PROJECTION FOOTGUN in an axonometric chassis (PARKED, TECHNIQUE_LIBRARY candidate for
  a development session). A mark placed at recess depth projects about 56 px LOWER on screen
  than the same x,z at depth 0 with this run's geom.py, so marks positioned near a recess's
  near edge fall outside the opening polygon and are silently clipped away (it ate the hero's
  fireweed inlay and gold specular until they were moved to the far half). Any depth-plan
  dossier should state, per mark, which polygon clips it and at what depth it was projected.

### 2026-07-25 (No. 17) — Phase 13/14 addendum, two lessons that arrived after the retro

Both are process lessons, and both are logged here rather than as instincts because
this run already appended 5 instincts against a 1 to 3 cap (retro deviation D10).
They are the two strongest instinct candidates for run No. 18.

- READ THE GENERATED EMAIL BODY BEFORE DELIVERING IT. The draft's score banner
  rendered "Shipped below threshold. ? / 10 vs ?. ... Fix next time: ?" because
  this run's scorer used key spellings the generator did not know. The maintainer's
  single most important number was missing from the only artifact a human reads,
  and no gate covers the email because the email IS the delivery. The
  verbatim-body rule is not a reason to skip reading it; it is the reason reading
  it matters, because the only legal fix is upstream in the generator. Fixed and
  logged as the run's third upgrade (957ff66). This is the fourth appearance of
  the same key drift (07-19, 07-20, 07-23), which is what "extend the alias list
  by one each time" buys you. The lists are now exhaustive.
- VERIFY A SUBAGENT'S VERIFICATION, ESPECIALLY WHEN IT REPORTS SUCCESS. The
  upgrade-engineer's report was strong and its central claim held under
  independent re-testing (the new gate does FAIL on a reconstruction of the
  defect and does leave the shipped deck and demo-deck clean). But its
  "correct on the flat runs/<date>/ copy too" was overstated: in flat mode the
  PNG sweep ran off a render report that flat mode does not have, so ten slide
  PNGs went unchecked while the row still printed PASS. That is the exact defect
  class the upgrade existed to prevent, sitting inside the upgrade. A confident,
  well-evidenced report is not evidence; re-running the check is.

## 2026-07-26 - Phase 1 craft refresh (No.18)

Timeboxed pass, 4 queries. Nothing overturns doctrine. Three things are new
enough to keep, and the third is load-bearing for THIS run (density dial 5).

- SAVES, with the share number attached. Documents are 12.92 percent of all
  saved posts on LinkedIn against roughly 2.6x their share of total content,
  and only 4.88 percent of creators post documents regularly. Combined with
  the settled "one save is worth about five likes in reach", this says the
  format's edge is not engagement volume, it is that the format is
  disproportionately KEPT. Keeps the house rule pointed the right way, every
  deck needs at least one genuinely keepable artifact slide. Source:
  https://contentdrips.com/blog/2026/07/linkedin-document-posts/
- ANNOTATION AS A DESIGNED LAYER, not garnish. The 2026 practitioner and
  educator interviews converge on four decisions that must be made explicitly
  per chart. (1) Audience, what context has to live ON the chart so it still
  reads when it is reused with no surrounding text. (2) Hierarchy, one primary
  annotation dominates and every secondary note is visibly subordinate.
  (3) Blend or separate, annotations either merge into the chart's own visual
  language or stand apart as a distinct layer, and the choice is made, not
  drifted into. (4) Subtraction, keep only the annotations that support the
  main message. This is the same "deliberate subtraction" note from 07-20,
  now with a decision list a dossier can actually specify. Sources:
  https://dl.acm.org/doi/full/10.1145/3772318.3790627 ,
  https://www.researchgate.net/publication/403683346
- DENSITY HAS A FLOOR, and the floor is a GAP not a font size. Current dense
  interface guidance keeps a 12 to 16 px minimum gutter even in high density
  grids, and leans on BACKGROUND CONTRAST between cells (not more rules, not
  more borders) to keep boundaries readable as density climbs. Scaled to our
  1080 canvas the practical read is, when a slide packs a matrix or a small
  multiple grid, budget the inter-cell gap FIRST and buy density out of the
  cell contents, never out of the gaps, and separate cells with a value step
  rather than adding hairlines. The stated tie-break stays "clarity beats
  density", which is the correct way to run a variance dial of 5. Sources:
  https://www.uxpin.com/studio/blog/ui-grids-how-to-guide/ ,
  https://www.alfdesigngroup.com/post/best-practices-to-design-ui-cards-for-your-website

## 2026-07-26 - retro (No.18 "One Line Out", the AI ratepayer pledge and Alaska's one signature)

- SHIPPED at a score of record 6.9 against a threshold of 8.3, merged as PR #113. Full
  studio ran: 6 scouts, fact-checker, 3 treatment-directors, 2 caption-directors +
  caption-critic, copywriter, 5 pixel-critics, flow-critic, scorer x2. Machine gates all
  green at ship (render 9/9, qa.py PASS 0/0, caption_check PASS, copy_sync 74/74,
  scanner_sync PASS, assemble vector 7.16 MB). Both hard fails the scorer found were
  repaired and verified BEFORE ship, so the shipped deck carries no known hard fail; the
  6.9 stands because the routine's 2-cycle scoring cap was spent and the deck was never
  re-priced.
- STORY. Gov. Dunleavy signed the White House Ratepayer Protection Pledge governors
  addendum on July 23, a voluntary and non binding commitment that AI data center load
  pays for its own power. Read live July 26, the 281 name signatory list carried exactly
  ONE Alaska entity, Cordova Electric Cooperative, 1,566 customers, 18 MW, not on the
  state highway system, not connected by transmission line to any other community, and
  already hosting a 150 kW data center on hydro. SB 250, the binding version, passed the
  Senate May 16 and died in House Community and Regional Affairs. Thesis, a promise is
  not an instrument.
- THE FACT-CHECKER OVERTURNED THE ENTIRE PITCH, and this is the run's best moment. The
  scouts' spine was "zero Alaska entities signed." FALSE. The fact-checker found Cordova
  by searching for utility NAMES rather than for the string "Alaska", because the one
  Alaska signatory's name does not contain the word Alaska. The replacement spine is far
  stronger than the pitch. Twelve scout claims were killed for failed verification and
  none reached a slide. New standing lesson: when checking a list for a state's presence,
  search the entities you expect to find, never the state's name.
- THE DOMINANT DEFECT, five instances of one class past a green gate. qa.py reported PASS
  with 0 fails and 0 warns while: S03 showed only FOUR of five bells (the fifth occluded
  by a label plate, against a list of five commitments); S05's twelve parcel tiles were
  clipped out of their own frame; a scotch rule crossed a headline's final period and
  rendered as a DASH on a deck that forbids dashes; S06's DEAD plate overprinted a
  subtitle (cycle 1 hard fail); and S02's counter note was clipped and struck through
  (cycle 2 hard fail, CREATED BY the cycle 1 repair to that same block). Two of the five
  were manufactured by the fix for the previous one.
- A POSITIONAL FIX DELETED A FEATURE IN ANOTHER REGION. Raising S04's pull-quote plate to
  clear the progress rail buried the slide's lit point underneath it, so the deck's
  declared spine went missing at the exact midpoint of the filmstrip. The pixel critic had
  already signed off on that slide; only the FLOW critic caught it. Logged as an instinct.
- akpost SILENTLY BLANKED AN ENTIRE CANVAS. The first S01 render passed with errors=0 and
  produced a fully black art canvas because AKPOST.grade was called with contrast as an
  object and lift/gain as hex strings where the contract wants a number and 3-element
  arrays. NaN propagated through the ImageData. The render report's canvas health block
  recorded mean 0 variance 0 and that block, read by eye, is the only thing that caught it.
- CRAFT WIN. New chassis, THE DEAD-END STRING, an akthree GPU PBR insulator string whose
  FIVE BELLS ARE the pledge's five commitments, with one governing rule across all nine
  slides (a span CARRIES, TERMINATES, or is ONLY DRAWN, always as a shape change so it
  survives 432px). Gold INVERTED to mean the promise, drawn as a phantom that never lands.
  Two slides print their own measuring rule (24 px = 1 MW, 1.7 px = 1 day) and the scorer
  verified both to within 4 px. Archivo alone plus JetBrains Mono, two families, never
  shipped in 17 prior decks, with the width axis carrying holding strength on S07.
- GROWTH EDGE, sixth consecutive run. Dead lower zones on four of nine slides, and artwork
  craft scored 6. The rendered hero is genuinely strong; the flat slides around it are
  what hold the number down. Also unshipped, S03's five planned leader lines and a
  completed camera move on S09.
- NEXT. Take the held Yup'ik speech-AI candidate. This was the third deck in nine days
  touching data centers and Alaska power cost; the 90-day ledger gate is clean but a
  reader experiences it as one long beat. Reddit was 100 percent unreachable to the
  community scout for the second run running.

## 2026-07-26 - Phase 12 frontier PARK (focus: headless-Chromium / Playwright rendering capabilities)

Rotation: last three foci were accessibility/PDF 2026-07-25, LinkedIn platform 2026-07-24,
self-improving pipelines 2026-07-23. Headless-Chromium was the stalest craft slot
(2026-07-19) and is the slot that serves this run's dominant scar, which is a
geometry/occlusion problem inside the browser. The engine's actual browser was probed,
not assumed: **Chromium 141.0.7390.37**, and it supports `text-box-trim`, `anchor-name` /
`position-area`, `text-wrap: pretty` and `corner-shape` (all probed with `CSS.supports`
in the render harness, all offline, all zero-dependency).

- **APPLIED. `document.elementsFromPoint` (the STACK, not the topmost element) is the
  correct primitive for occlusion.** Singular `elementFromPoint` answers "what would a
  click hit", which on our slides is always the full-frame `.grain`/`.edge` overlay, so
  the first draft of today's occlusion gate reported ZERO everywhere including on the
  reconstructed hard fails. Comparing the plate's depth against the text's depth in the
  returned stack is what makes the answer paint-order-true. Prior art agrees in
  principle: hit testing against overlapping objects must return ALL intersecting
  visuals, not just the first
  (https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/hit-testing-in-the-visual-layer).
  Shipped as UPGRADE 1 this run.
- **PARKED CANDIDATE, CSS ANCHOR POSITIONING for annotation plates** (Baseline 2026;
  Chrome 125+, our Chromium 141 supports it: `anchor-name`, `position-area`,
  `position-try-fallbacks`).
  https://developer.chrome.com/blog/anchor-positioning-api ,
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position-try-fallbacks
  Every instance of this run's dominant defect came from HAND-TUNED absolute
  coordinates going stale when a neighbouring string changed length. Anchoring a DEAD
  tag or a callout to the thing it names (`position-area: block-end span-inline-start`)
  makes the plate move WITH its subject instead of being re-typed by hand each repair.
  PARKED, not applied: `position-try-fallbacks` only reacts to CONTAINING-BLOCK/viewport
  overflow, not to collision with a third element, so it is an authoring-doctrine change
  (how slides are built) with real design surface, not a one-run engine edit. Needs a
  worked TECHNIQUE_LIBRARY entry and one deck's worth of trial before it becomes house
  style.
- **PARKED CANDIDATE, `text-box-trim` / `text-box-edge` (cap-height line boxes).**
  https://developer.chrome.com/blog/css-text-box-trim ,
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box-trim
  Chrome/Edge 133+, Safari 18.2+, still NOT Baseline (no Firefox as of mid-2026) — which
  does not matter to us, because our only rendering target is our own Chromium.
  `text-box: trim-both cap alphabetic` makes a text element's box equal its cap-to-
  baseline ink instead of its half-leading, which (a) makes plate padding and optical
  alignment exact rather than eyeballed, and (b) removes the false-graze band that
  forced today's occlusion gate to ignore patches under 6px tall (the rail's gold dot
  clips 3px of the sponsor line's LEADING, not a glyph). PARKED: it changes vertical
  rhythm on every text block that adopts it, so it lands as a doctrine + dossier change
  in a run that can afford to re-tune a deck, not as a silent engine default.
- **ENVIRONMENT FACT, worth knowing before it bites.** Playwright >= 1.57 switched the
  default `chromium` channel to Chrome for Testing (`chrome-headless-shell`), and the
  release notes flag that "screenshots are different" across that transition
  (https://playwright.dev/python/docs/release-notes). This box's Playwright already
  expects `chromium_headless_shell-1228`, which is absent; every render this run
  survived on `render.py`'s `launch_chromium()` fallback to `chromium-1194`. Pixels are
  stable today. The recommendation (not spent as an upgrade slot) is to record
  `browser.version` in `render_report.json` so a future pixel shift is diagnosable from
  the artifacts.
- **NOTHING FOUND worth applying on the Playwright API side.** The 2026 additions
  (WebSocket routing, canvas previews in traces, `install --list`) do not touch an
  offline, single-page, deterministic screenshot pipeline.

### 2026-07-26 (No. 18) — Phase 13 addendum, the delivery step is size-bound

The Gmail draft is the run's only deliverable to a human, and it nearly did not
ship. gmail_draft.py inlines one base64 JPEG per slide, which put the html_body
at 477 KB. The whole body must pass through ONE create_draft call, and 477 KB of
base64 is roughly 120k tokens, past what a single call can carry. Prior runs got
away with 373 KB and 530 KB; this is a wall the routine had not hit yet only
because nobody measured it.

Fixed in the moment per the FAILURE PROTOCOL, and the fix is now in the script
rather than in a session's head. gmail_draft.py gained --preview-width,
--preview-quality and --preview-mode (grid | contact | remote). Defaults are
unchanged, so nothing moves for any existing caller. `remote` emits ONE
contact-sheet image sourced from its raw URL plus the same per-slide full-res
links, which lands the body at 16 KB.

THE LESSON THAT MATTERS. The first draft went out with the contact sheet's src
hand-swapped from a data URI to a raw URL, which is exactly the kind of quiet
body edit the 2026-07-21 verbatim rule exists to forbid. The right move, taken
immediately after, was to make the SCRIPT emit that body and re-verify the
delivered bytes against the script's output (equal, timestamp aside) so the
record is true rather than merely close. If a delivery constraint forces a change
to the body, change the generator, never the draft.

### 2026-07-26 (No. 18) — the artwork-craft ceiling, root cause and fix

Six consecutive scored runs named "dead lower zones" as the ceiling on artwork
craft (ledger entries 10, 11, 13, 14, 15, 16, 18). Six times it became a
sentence in this file. It was still a sentence at the end of run 18, and the
maintainer's question was the right one, which is why not fix the cause.

THE CAUSE WAS A RULE IN OUR OWN DOCTRINE. DESIGN_DOCTRINE 1 read "at least one
generous quiet zone per slide" with no ceiling and no address. The cheapest
place to spend an unbounded licence is the bottom band of a top-loaded
composition. The dossier then wrote that empty bottom into the plan, and the
pixel critics grade each slide against its OWN dossier, so a slide that
executed a bad plan passed its acceptance checklist. The only reviewer
positioned to see it was the scorer, at the ship gate, with no budget left to
rebuild four slides. That sequencing is why it recurred, because it was structurally
guaranteed to arrive too late to fix, every single run.

WHAT THE DATA SAID, INCLUDING WHERE THE FIRST ATTEMPT WAS WRONG. A plain
emptiness measure does not separate the defect. Across the 45 scorer-labeled
slides the dead ones' whole-frame occupancy (median 0.505) is indistinguishable
from the rest (0.537), because every slide has quiet margins. Two different
defects share the name. Some slides have a bottom band that is EMPTY
(2026-07-17 S09 and 2026-07-20 S03 both ship a bottom 40% with nothing in it,
and neither was ever named by a scorer, which is its own evidence about
relying on eyes). Others have a bottom band that is OCCUPIED BUT FLAT, grey
plates and hairlines on bare ground, which is what run 18's S05 and S08 are.
Only counting cells that carry MODELED tone catches both.

An absolute craft-density floor was tested and REJECTED, because it fails 48 to 60% of
every slide the series has shipped, which makes it a taste judgment the machine
should not make alone, and the doctrine's own position is that flat is a
legitimate choice. The gate is therefore self-relative and asks only the
question the scorers kept asking, whether the slide spends its craft up top and
coasts.

THE FIX IS IN THREE PLACES, EARLIEST FIRST.
1. The doctrine clause is now bounded and placed. The quiet zone may not exceed
   about a quarter of the frame and is not the bottom band by default.
2. SLIDE_DOSSIER_SPEC field 4a, enforced by scripts/dossier_check.py at the
   Phase 5 storyboard gate, where every dossier names what the bottom band carries
   and names something with modeled tone. Here the fix costs one paragraph.
3. qa.py frame_balance(), at render time, FAILing a bottom third that carries
   under 60% of the slide's own craft density. On run 18's shipped renders it
   FAILS S05 and S08 and warns S09, against a scorer list of "slides 4, 5, 8
   and 9", with no false alarm on the rendered heroes S01 and S03.

THE LESSON THAT GENERALIZES. A defect that only the LAST reviewer in the
pipeline can see will be deferred forever, because by the time it is visible
the run cannot afford it. Moving detection earlier is worth more than looking
harder at the end. And when a defect recurs, suspect a rule that permits it
before suspecting the people following the rule.

## 2026-07-29 (No. 19) - Phase 1 craft refresh

Timeboxed platform + craft scan. Four things are genuinely new against what
CAROUSEL_CRAFT already carries.

- SAVE WEIGHT IS NOW STATED RELATIVE TO COMMENTS, not just likes. Practitioner
  syntheses of the 2026 ranking stack put a save at about 5x a like AND about
  2x a comment, with saves and sends described as the strongest distribution
  signals. We already build for saves; the new part is that a save now
  outranks the comment we design the closing question to earn. Keep the
  question (it is still the cheapest dwell extender) but the keepable slide is
  the higher-value object, which is an argument for spending the deck's one
  dense data slide well rather than trimming it.
  https://www.socialpilot.co/blog/linkedin-algorithm
- DWELL IS NOW REPORTED IN BANDS, and the spread is enormous. Posts at 61+
  seconds of dwell are reported at 15.6 percent engagement against 1.2 percent
  for 0 to 3 seconds. Roughly 70 percent of a post's total reach is described
  as decided in the first 60 to 90 minutes. Both numbers are practitioner-tier,
  not official, so they are (M) at best, but they sharpen the golden-hour
  aftercare line we already print in every email from "reply fast" to "the
  first 60 to 90 minutes decide most of it".
  https://meet-lea.com/en/blog/linkedin-algorithm-explained
- THE SLIDE-COUNT ADVICE HAS SPREAD OUT, and the conflict is unresolved.
  Oktopost's 2026 carousel guide says 5 to 15 and argues shorter and tighter
  wins; other 2026 syntheses say 9 to 12 is the sweet spot because dwell needs
  length. Our 6 to 12 band with an 8 to 10 default sits inside both. NO CHANGE
  to the doctrine, but stop treating any one practitioner number as settled.
  Oktopost also lands on a 24 pt design-tool minimum, which is our 24 px
  absolute floor by a different route, and repeats the 4:5 1080x1350 default.
  https://www.oktopost.com/blog/linkedin-carousel-pdf-best-practices/
- THE 2026 DESIGN TREND READING FAVORS WHAT WE ALREADY DO, which is worth
  knowing mostly so we do not chase it. The trend writing converges on
  texture, tactility, analog imperfection and layered depth, and away from
  flat generated-looking infographics toward "designed, with a point of view".
  That is the house position already (grain tiles, paper tooth, modeled tone,
  the rendered ladder). The one actionable read is that MATERIAL texture is
  currently a differentiator rather than a risk, which supports spending
  density on the bottom third rather than economizing there.
  https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026

### 2026-07-29 (No. 19), the plates the machine could not see

The scorer capped this run at 6.90 from an uncapped 8.33 on one hard fail, and
the hard fail was arithmetic. JetBrains Mono at 24px with 0.10em tracking
advances 16.8px per character. Every knockout plate and chip in the deck had
been hand-sized at roughly 14. Six labels hung off their own plates across
slides 04, 05 and 07, including a chip border rule drawn straight through the
"T" of PERMITS, and one annotation sat entirely off its knockout.

The reason it survived two full scoring cycles is the part worth keeping.
render.py's overlap detector inspects DOM text line boxes. Every one of these
defects was SVG text against an SVG rect, against canvas artwork, or under a
DOM block, so machine_qa reported 0 fails while the deck was visibly broken.
A gate that cannot see a whole layer will report that layer perfect forever.

The engine now measures it. render.py reports every SVG text against the rect
painted under it, against any opaque rect appended after it, and against any
opaque DOM element composited above the svg (sampled with elementsFromPoint
across the label's own box). qa.py fails all three. The checks were verified
against a purpose-built ground-truth slide carrying one spill, one painted-over
label and one correct control: both defects reported, control silent.

Fixing the first two exposed the third inside one render cycle, and every
repair produced a knock-on. Widening a chip pushed it into a legend. Raising a
plate cut the label above it. Moving slide 03's source line off the counter
landed it on the self-audit annotation. This is a family of bugs, not a bug,
and the discipline is to re-run the gate after every single move.

One craft finding did not resolve. The hero column encodes the thesis as a
material change at hour 7, steel below and brass above, and under a single
0xffb067 sodium key both materials read as one amber extrusion. Lifting the
steel to 0xe8edf0 and adding a proud collar at the seam helped; darkening the
brass to force contrast made the frame muddier and was reverted. Two materials
separated only by hue collapse under a strongly coloured key. Separate by value
and by a physical joint, and check it at 432px.

#### Phase 12 frontier scan, typography craft (2026-07-29), parked candidates

- Measure-then-size is the settled practice, and the primitive matters.
  `getComputedTextLength()` returns only the horizontal ADVANCE (glyphs plus
  letter-spacing and word-spacing, ignoring `x`), so it gives no height and no
  anchor-correct origin; `getBBox()` gives the laid-out box, and EXCLUDES
  stroke, so a haloed label needs half its stroke width added back. Leading or
  trailing whitespace in an SVG text node corrupts the box in every engine.
  Applied this run inside `AK.svgPlate`.
  https://developer.mozilla.org/en-US/docs/Web/API/SVGTextContentElement
  https://bugzilla.mozilla.org/show_bug.cgi?id=1078743
- PARKED, label auto-placement. The Vega-Lite legible-label-layout work uses an
  OCCUPANCY BITMAP (rasterise every mark once, then test candidate label boxes
  against it with bitwise ops, constant time in mark count) plus an eight-
  position model (top-left, top, top-right, right, bottom-right, bottom,
  bottom-left, left) tried in preference order, placing each label in the first
  free position and skipping gracefully when none is free. That is the
  principled answer to this run's knock-on churn, where six render cycles went
  on repairs that each collided with something else. Roughly 150 lines over the
  existing render, but it changes how slides are composed, so it wants a
  multi-deck trial rather than a daily slot.
  https://arxiv.org/html/2405.10953v1
- PARKED, the complement of the plate helper. SVG `textLength` with
  `lengthAdjust="spacingAndGlyphs"` fits the TEXT to a fixed box instead of the
  box to the text, for the case where the plate geometry is load-bearing (a
  cadastral parcel, a rail tick, a fixed chip stack). Use `spacingAndGlyphs`,
  never bare `spacing`, which can collide glyphs at tight fits. Chrome supports
  it on `tspan`; Firefox does not, which does not matter here.
  https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/text
- PARKED, craft. 2026 editorial typography uses monospace as an editorial voice
  (precision, lab-form register) rather than as a code signal, which is the
  register this studio's mono furniture already occupies, and variable optical-
  size axes open tracking automatically at small sizes where our all-caps mono
  labels are hand-tracked at a flat 0.08 to 0.12em. Worth one controlled
  comparison on a future deck.

#### Phase 13 addendum, 2026-07-29: the connector will not take "me"

First run delivering into the new mailbox (docket@alaskaaihq.com, repointed
2026-07-26). gmail_draft.py emits `to: "me"` and the routine says not to
substitute a literal address, but this Gmail connector rejects it outright with
"Invalid email address. Please provide a raw email address in the format
'user@example.com'." Omitting the recipient entirely also fails, with "At least
one recipient (To, Cc, or Bcc) must be specified." The draft was created
addressed to docket@alaskaaihq.com, which is the mailbox the connector already
authenticates as, so nothing about where it lands or what it would send from
changed. Maintainer confirmed the address in-run.

If a future connector accepts "me" again, prefer it. Until then the account
relative form cannot be used, and the honest options are the documented mailbox
or a failed delivery. Worth considering whether gmail_draft.py should emit the
resolved address alongside "me" so the showrunner is not choosing under
pressure.

Second note, same phase: the default payload is 520 KB because it inlines one
data URI per slide, and that does not fit one create_draft call. The script's
own `--preview-mode contact` (50 KB, one inline contact sheet) and
`--preview-mode remote` (18 KB, contact sheet by raw URL) exist for this.
Remote was used, because the body has to be retyped verbatim into the tool call
and every byte is a chance to drift from the script's output. The raw URLs were
verified to resolve on main first.

### 2026-07-29 (No. 19), the encoding gate that could not be built, and what it measured instead

Artwork craft has been the weakest rubric criterion in 16 of the first 19 runs.
The diagnosis was that every gate judges LEGIBILITY and nothing judges whether
the picture carries the argument it claims, so the only reviewer who ever sees
a failed encoding is the scorer, at the ship gate, too late to rebuild art.

The plan was a gate. Let a slide declare, machine-readably, what its art says
without words, then measure whether that survives to feed scale. Run No. 19's
own hero was the perfect test case: the artwork ledger said the material change
at hour 7, brushed steel below and polished brass above, was "the thesis with
zero words", and the scorer said the column read as one uniform amber extrusion.

Two metrics were calibrated against that known-bad and against slide 07's
sodium-to-slate ownership boundary, which both the scorer and the flow critic
called the deck's best fusion beat. Measured at 432px:

  known-bad  S03 steel vs brass    dE 49.0   AUC 0.87   visible 58 / 83 pct
  known-good S07 sodium vs slate   dE 12.2   AUC 0.77   visible 54 / 53 pct

Both metrics are BACKWARDS. Colour separability is higher on the broken
encoding, because the steel genuinely is a different colour where you can see
it; it just reads as a glassy plinth instead of as half the object. Occlusion
is worse on the working one, because a deliberate composition puts type over
its own art. Any threshold drawn through those numbers passes the defect and
fails the success. A gate shipped on either would have been worse than no gate,
because it would have printed "encoding verified" over exactly the failure it
was built to catch.

So the declaration contract shipped and the verdict did not. qa.py reports the
numbers into machine_qa for the pixel critics and the scorer, raises no FAIL
from them, and carries the calibration table in its docstring so the next
attempt starts from evidence.

The lesson generalises past this gate. The defects this machine has
successfully automated (text off its plate, art crossing glyphs, a dead lower
third) are all GEOMETRIC: a thing is where it should not be, and pixels answer
that directly. This one is SEMANTIC, about proportion and context and whether
a shape reads as part of an object, and colour statistics do not answer it.
Before building the next gate, ask which of the two kinds it is. If it is the
second kind, expect to measure and report rather than to judge, and expect the
honest deliverable to be a number handed to a critic rather than a threshold.

Making it a real gate needs encoding declarations across the back catalogue so
a threshold can be FITTED rather than guessed. That is a corpus exercise.

### 2026-07-29 (No. 19), the corpus finally answers the artwork-craft question

Artwork craft has been the weakest rubric criterion in 16 of the first 19 runs
and three separate attempts have now been made to gate it. This one settles
whether that is possible, with data rather than intuition, and the answer is no.

scripts/craft_corpus.py derives per-slide labels from what the scorers actually
wrote (tightened so that praise like "S6's hero RESOLVES the chronic flat-hero
weakness" is not read as a defect, which the first derivation pass did), then
computes nine objective image features over every shipped slide and asks
whether any of them separates a slide scorers named from a slide they did not.

  171 slides, 19 decks, 24 labelled bad, 147 not.

  detail_ratio          AUC 0.653   deck rho  0.15
  grad_energy           AUC 0.621   deck rho -0.18
  modeled_bottom_ratio  AUC 0.611   deck rho -0.12
  tonal_entropy         AUC 0.592
  chroma_spread         AUC 0.572
  flat_frac             AUC 0.544
  hi_mass               AUC 0.531
  modeled_frac          AUC 0.503
  mid_contrast          AUC 0.500

Null standard error at 24 against 147 is 0.064, so the best feature is 2.4
standard errors out, and nine features were tried. Bonferroni corrected p is
0.147. Leave-one-deck-out puts it between 0.619 and 0.701, so it is stable, and
stably noise. Its correlation with the deck's own artwork-craft score is 0.15.

AN OBJECTIVE ARTWORK-CRAFT GATE IS NOT SUPPORTABLE. Not "not yet", on this
corpus. Three attempts, three refutations, each more decisive than the last:
an absolute craft floor (2026-07-26, failed half of everything ever shipped),
colour separability on a declared encoding (2026-07-29 morning, came out
backwards on a known-bad against a known-good), and now nine features against
the full labelled corpus.

WHAT TO DO WITH THAT, because the answer is not to give up on the weakness.
The failure is semantic. Run 19's hero measured 49 dE between its two declared
materials and still read as one uniform amber extrusion, because what was
wrong was proportion and context, not colour. No pixel statistic answers
"does this shape read as part of that object". A competent viewer answers it
instantly.

So the declaration stays and the threshold goes to the reviewer who can
actually judge it. Dossier field 11a states the wordless claim; the pixel
critic now receives it and must return encoding_reads, at Phase 9, where there
is still budget to rebuild art. That is the same lesson 2026-07-26 wrote down
and did not fully apply: a defect only the LAST reviewer can see is deferred
forever, so move detection earlier. Machine QA measures and informs; it does
not decide.

The generalisable rule for this machine: automate the GEOMETRIC defects, where
a thing is somewhere it should not be and pixels answer directly, and route
the SEMANTIC ones to a judge with the measurements in hand. Knowing which kind
you have, before building, is worth more than the gate.

### 2026-07-30 (No. 20), craft refresh

- The 2026 benchmark picture is unchanged in substance: native documents remain
  the top engagement format (Socialinsider 7.00 percent, Oktopost's top-decile
  B2B pages post more document content than median pages). Nothing here moves a
  house rule. Sources: socialinsider.io/social-media-benchmarks/linkedin,
  oktopost.com/blog/linkedin-carousel-pdf-best-practices/
- One framing worth carrying: several 2026 write-ups describe LinkedIn moving
  from a Relationship Graph to an INTEREST Graph, where content surfaces on
  what a reader engages with rather than who they follow. If that holds, a deck
  that is legible about its SUBJECT (place names, agency names, the actual
  nouns) is doing ranking work, not just accessibility work. It is another
  argument for the machine-readable moat the site already builds.
  Source: extramiledigital.com/news/linkedin-announces-2026-algorithm-update/
- Slide-count advice is drifting up (one 2026 guide says 9 to 12, another says
  8 to 10 max because completion is penalised). Our band already spans this.
  No change; noting the drift so a future run does not read it as new.
- Craft note, relevant to this run's brief against concentrated detail: the
  landscape-painting literature is blunt that depth comes from VALUE GROUPING
  before it comes from detail. Background gets light values and minimal
  contrast, midground medium values and moderate contrast, foreground the full
  value range plus the sharpest edges and the warmest, most saturated hues. A
  deck whose craft lives in one precisely modelled object has, by construction,
  only one value group, which is why it flattens. Group the frame into three
  value bands FIRST, then spend detail inside the nearest one.
  Sources: samuelearp.com/blog/depth-in-paintings/,
  finearttutorials.com/guide/atmospheric-perspective/

### 2026-07-30 (No. 20), half the artwork diagnosis was right

The run set out to break a three-deck run of 6.90s where artwork craft was the
weakest criterion. The diagnosis was that decks 17, 18 and 19 concentrated
their craft in ONE modelled object, giving the frame one value group. The
prescription was a PLACE with three value bands, detail distributed across four
quadrants, and the drafting line voice retired. The deck scored 8.09 and
artwork craft still came in at 6.0, so the diagnosis was half right and it is
worth writing down which half.

THE HALF THAT WORKED. The single-value-group failure is measurably dead. The
mechanism was not aesthetic, it was a loop direction: the drift was filled as
bands that each ran from their own contour to the frame bottom, and the loop
ran dark-to-light, so the last and lightest band painted over everything behind
it and the entire foreground flattened to one pale mass. Inverting the loop
made the cover fall from L 0.475 at the lit crest to L 0.120 at the near edge,
with 2.9 percent of pixels within 0.03 of L 0.51 against a 12 percent ceiling.
That is a one-character fix worth more than any amount of art direction, and it
passed the machine gate in its broken state because gates measure geometry and
this was a value defect.

THE HALF THAT DID NOT. Trading one modelled object for nine fields does not by
itself produce craft; it produces nine chances to spend a detail budget that
was never spent. What shipped is one background reused nine times with
per-slide edits. The declared fall-line sastrugi, two-part contact shadows,
specular crests and scale-graded poles are in the dossier and not in the
pixels. The generalisable lesson: "distribute the detail" is a plan, not a
technique, and a plan with no per-region budget gets spent on whatever is
easiest to draw everywhere, which is a uniform hatch.

WHAT TO DO NEXT TIME. Pick ONE surface and build it properly, then reuse it.
The scorer's one-sentence fix names it exactly: one real sastrugi surface with
varying line weight, contact shadows and specular crests, applied to the three
regions holding the dead pixels, would have moved this criterion more than nine
separate compositions did.

TWO PROCESS THINGS WORTH KEEPING.

The pixel critics caught two HARD failures that the machine gate could not see
and that would have shipped: the close carried gold on both the register and
the Polaris, which destroys the entire argument that the gold has LEFT the
list, and the data slide had no literal anchor at all, which doctrine fails
outright. Both were invisible to qa.py because both are semantic. This is the
2026-07-29 routing lesson confirmed: automate the geometric defects, route the
semantic ones to a judge.

The flow critic's single highest-value note was worth more than any per-slide
fix. It identified that slide 5 was simultaneously the deck's only reorderable
slide, its only failing thumb, and the only frame that planted nothing, and
that one running-line change plus one forward-planting sentence would close all
three at once. A sequence-level reviewer finds problems that nine slide-level
reviewers structurally cannot.

AND ONE THING TO STOP DOING. The deck-summary line that brand.yaml requires has
now lapsed for three consecutive runs and the scorer capped Copy at 6.0 for it.
Either the caption room starts writing it or the config should be amended
honestly. It is no longer an oversight; it is a rule nobody enforces.

### 2026-07-30 (No. 20), addendum, the other half of the artwork fix

The retro above said "distribute the detail" is a plan and not a technique, and
that the durable version would be one real surface built properly and reused.
That is now `assets/js/aksnow.js` and it is worth recording what the building
of it taught, because two of the three lessons were not about snow.

**The metric you reach for first is often the wrong one.** The obvious gate for
a texture upgrade is "carries more fine detail than what it replaces", and that
bar FAILED the new surface (detail_ratio 0.98x). Two reasons, both instructive.
The corpus study of 2026-07-29 had already shown detail_ratio does not separate
craft (AUC 0.653, Bonferroni p 0.147), so gating on it would have been theatre.
And mechanically the old hatch WINS on ink, because it draws fifty full-width
level strokes, so requiring the replacement to out-ink it would have pushed it
back toward being a dense line field, which is the defect. The gate that works
measures the DESIGN CLAIM instead: line-weight variance, orientation spread,
and the rate at which a bright pixel sits directly above a darker one, which is
the lit-windward-plus-dark-lee structure stated as a number. That last one came
out 17x.

**A metric written for one purpose found a different, older defect.** While
calibrating, the value ladders were sampled down the frame and the old hatch
turned out to SATURATE at about 60 percent depth and then sit flat for the
entire bottom third. That is the "dead lower zone" the scorer named in six
consecutive runs, and nobody had ever measured it; it was always described. It
is now a gated feature, `low_band_range`. The general lesson is that a
calibration run is a cheap place to find defects you were not looking for, and
it is worth printing more than you plan to assert on.

**cx.filter applies per draw op.** A surface made of ~850 strokes drawn under
`cx.filter = "blur(6px)"` blurs 850 times and blew the 45s navigation budget on
S04. Drawing into an offscreen canvas and blurring once at composite fixed it
and made that slide 3x faster than it had been even before the new surface.
This will bite again; it is now in the TECHNIQUE_LIBRARY entry.

Applied to the shipped deck, lower-band tonal range improved on every slide
measured (S01 +0.028, S02 +0.031, S03 +0.055, S04 +0.012, S09 +0.086).

### 2026-07-31 (No. 21), craft refresh

- Platform picture unchanged again, third refresh running. Socialinsider still
  has native documents top at 7.00 percent against multi-image 6.45 and video
  6.00, and Oktopost's top-decile B2B pages (22.45 percent ER) still post more
  document content than median pages (5.72). No house rule moves. Recording the
  non-change so a future refresh does not re-litigate it.
  Sources: socialinsider.io/social-media-benchmarks/linkedin,
  oktopost.com/blog/linkedin-carousel-pdf-best-practices/
- Slide-count drift continues upward in the practitioner guides, one 2026 guide
  now saying 9 to 12 is the sweet spot on dwell-versus-completion grounds. Our
  band is 6 to 12 with an 8 to 10 default and already spans it. No change, and
  this is the second consecutive refresh to note the same drift.
  Source: postunreel.com/blog/linkedin-carousel-engagement-rate-statistics-2026
- CRAFT FIND, and it is the one that matters this run. LINE ENGRAVING has a
  worked-out vocabulary for exactly the problem this machine keeps failing:
  how to build ONE surface that carries modelled tone with genuine detail
  everywhere, instead of a uniform hatch. Four transferable rules.
  (1) Hatching lines WRAP THE FORM. Lay lines follow the surface they describe,
  so the direction field is the modelling, before any value is applied. A hatch
  whose direction is constant across a frame is decoration; a hatch whose
  direction follows the geometry is form. This is precisely what No. 20's
  uniform contour drift got wrong.
  (2) THE SWELLED LINE. A single stroke tapers at both ends and widens in the
  middle, and where swelled lines cross into lozenges they carry tone by
  themselves and make overlapping hatch layers unnecessary. Line-weight
  variance is the technique, not a garnish on it, which is the same conclusion
  aksnow.js reached from the other direction on 2026-07-30.
  (3) THE VOCABULARY IS THREE PARTS, not one: mainline, crossline, interdot.
  Tone is built by the RELATIONSHIP between a dominant lay, a crossing lay and
  the dots that sit in the diamonds, and the three are separately controllable.
  That is a per-region budget expressed as a drawing system.
  (4) What sets a line's thickness is the light. Thickness is a lighting
  decision made per stroke, not a global stroke weight.
  Sources: risdmuseum.org/exhibitions-events/exhibitions/brilliant-line,
  metmuseum.org/about-the-met/collection-areas/drawings-and-prints/materials-and-techniques/printmaking/engraving,
  librarycompany.org/makinganimpression/section2.html
- GUILLOCHE, same family, and it is a generative system with real parameters
  rather than an ornament. The patterns are epitrochoids and related curves
  produced by engine turning, drawn at fractions of a millimetre so the effect
  is delicate and hard to reproduce, which is the entire point of putting it on
  money. It is drawable offline in Canvas from three or four numbers, it is
  detail-dense by construction, and its parameters can carry story quantities.
  Sources: bankofcanadamuseum.ca/2020/07/the-art-of-guilloche/,
  mathpuzzle.com/MAA/13-Guilloche Patterns/mathgames_02_09_04.html
