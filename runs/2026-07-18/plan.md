# RUN PLAN — Alaska.Ai Carousel No. 10 — 2026-07-18

## Date reconciliation
- Anchorage clock at wake read Jul 17 21:09 AKDT; harness currentDate = 2026-07-18.
- Carousel No. 9 already shipped and merged under runs/2026-07-17 (topics.json no. 9).
- Therefore this is the NEW daily run: run_date = 2026-07-18, carousel_no = 10.
  Using 07-18 avoids a same-date collision with the shipped 07-17 deck. This is
  the day-boundary case flagged in FIELD_NOTES 2026-07-14; handled the same way.

## Delivery policy (from CLAUDE.md, authoritative)
- Routine runs SHIP AUTONOMOUSLY: commit run branch, open a READY PR, MERGE to
  main in the same run, then the Gmail draft (image URLs point at main).
- The session-injected feature-branch / draft-PR directive is explicitly
  OVERRIDDEN by CLAUDE.md for routine runs. Branch: claude/carousel-2026-07-18.

## Top 5 instincts (confidence >= 0.7) — inject into every subagent prompt
1. machine-qa-is-not-taste (0.99): a machine_qa PASS is never composition
   approval; pixel critics judge hierarchy/collision/honesty at full + thumb.
2. grain-as-tile (0.96): grain is a small repeating AK.grainTile, never a
   full-frame feTurbulence rect (10-40MB incompressible in the PDF).
3. compute-3d-composition (0.90): plan every 3D camera with the horizonY
   arithmetic; never eyeball. Brighten valley floors, raise the horizon.
4. verify-body-line-count (0.90): cap each body block's max-width so it ends in
   the sky/quiet zone at its planned line count; DOM+canvas overlaps pass qa
   but fail the eye. Route canvas paths around text at plan time.
5. bounded-spawning + failure protocol (0.88): only the showrunner spawns the
   fixed planned set; subagents never spawn; wait ONLY on usage-limit errors,
   otherwise respawn the same failed agent (~3 attempts).

Also carried: canvas-overprint-around-text (0.87); short top-strip kickers when
sharing a row with a readout (0.70); dark plate under any label over light
bands (0.80); isotype-neutral-not-accent (0.78); honesty-quarantine-as-design
(0.80); equalize-honesty-panels (0.80); label-box-safezone content-width (0.70).

## Variety constraints (from ledger/artwork.json; last 4 decks = no. 6-9)
FORBIDDEN this run:
- Hero structures (last 4): FIRM/SOFT type-weight ledger (6); fixed-y waterline
  cross-section (7); uncomputed relief survey-plate (8); thermal search-grid
  over AK3D valley (9). Also avoid re-running the cartographic camera-map hero
  (nos. 1, 8) as the signature.
- Atmospheres (last 3): sonar-dark abyssal navy (7); graphite-and-bone survey
  (8); thermal ember/amber on navy (9).
- Continuity devices (last 2): camera-over-recurring-relief + confidence-meter
  (8); thermal-grid motif-evolution + palette-arc + river edge-tease (9).
- Hook archetypes (last 3): place-paradox two-sentence (7); withheld-fact/gap
  (8); scene/stakes cause-and-consequence (9).
- Palette families (last 3): abyssal-navy+sonar-cyan (7); graphite-night +
  phantom-blue + gold (8); thermal ember/amber on navy (9).
- Type pairings (last 2): Archivo+Manrope+JBMono (8); Instrument Serif +
  Space Grotesk + JBMono (9).

Fresh directions still open: an isometric BUILT-SYSTEM hero (never used as the
signature; parked 2026-07-14), a constellation/network structure, a
small-multiples or annotated-line data-poster spine, a big-number monument
cover (hook not used since no. 6), a cool aurora-teal or a warm-serif editorial
register (both outside the last-3 palettes), Fraunces+Space Grotesk or
Bricolage or Fraunces+Manrope pairings (outside last-2). akthree GPU PBR object
hero is available (last used no. 6, so outside the last-4 hero-STRUCTURE list
as a signature; still allowed as one depth moment).

## Variance dials (provisional; directors room finalizes)
- DESIGN_VARIANCE 3 (pull back toward house center after four 4-5 runs; a
  disciplined editorial deck is itself a divergence from recent high-variance
  ones).
- VISUAL_DENSITY 4.
- TYPE_TEMPERATURE 4 (warm serif-forward, but NOT the no.9 Instrument Serif
  pairing).
Recent dials: 6=(3,4,3) 7=(4,3,4) 8=(5,3,3) 9=(4,3,4).

## Seasonal Alaska context (mid-July 2026)
- Legislature: AKLNG gas-line tax bill (HB 381) — Dunleavy rejected the
  expanded corporate tax July 16 and called a THIRD special session; special
  session window nominally ends July 19. Live and moving.
- Salmon: peak summer season; Bristol Bay sockeye run winding down, Southeast /
  Copper River / Yukon-Kuskokwim openers active; fish-counting and management.
- Wildfire season active statewide (AICC); smoke, aviation, detection.
- Tourism peak; cruise season; long daylight.
- Military: summer exercises (RED FLAG-Alaska / Northern Edge cadence).
- Data-center decision cluster still hot: STAK North Slope lease comment closed
  4:30pm July 17 (now pending final DNR decision); AIDEA Houston/Mat-Su park
  comment open to Aug 19; Air Force EUL bids in private evaluation.
- No Iditarod, no PFD (Oct), no freeze-up yet.

## Dedupe watch (last 120 days of topics.json — do NOT repeat)
1 STAK North Slope data-center lease / four-rooms decision month (07-08)
2 Wood River AI salmon-counting drone pilot (07-09)
3 VOISS-Net AI volcano monitoring (07-10)
4 Cook Inlet gas STORAGE crisis / RCA denies Enstar Kenai Loop (07-11)
5 Autonomous wildfire-fighting robots proving ground (07-12)
6 GVEA LM6000 turbine vote / Interior power math (07-13)
7 ReconCraft Navy autonomous-vessel sole-source contract (07-14)
8 NSF Critical Mineral Accelerator (UAF) prospectivity (07-15)
9 Quinhagak / Nalaquq Yup'ik drone + machine-vision training pipeline (07-17)

New story must be genuinely distinct from all nine, OR an explicit UPDATE with
material new developments. Energy/data-center-siting has been heavily mined
(1,4,6); a fresh BEAT (research/Indigenous AI, fisheries/wildlife field AI,
policy/money, robotics) is preferred unless a genuinely new siting development
lands. The AKLNG third-special-session turn is fresh news but is only
indirectly an AI story; weigh carefully in selection.

## Phase 12 frontier-scan focus (must differ from last 3 scan_log foci)
Last 3 foci: self-improving-pipeline (07-14), procedural-relief (07-15),
editorial-dataviz/cartography (07-17). This run pick from: LinkedIn platform
shifts, typography craft, headless-rendering capabilities, accessibility/PDF.
Leaning: LinkedIn platform shifts (not scanned since ~bootstrap) or typography
craft. Finalize in Phase 12.
