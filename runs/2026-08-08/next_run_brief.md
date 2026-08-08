# NEXT RUN BRIEF — queued by the 2026-08-08 run (No.29, incomplete)

**Written by the 2026-08-08 showrunner, not by the maintainer.** The 08-08 run
did NOT ship a deck. It got as far as a complete, gated storyboard and three
rendered slides, then ran out of context budget before the art build finished.
Nothing was merged to main.

**This brief is unusually valuable, because almost all the expensive work is
already done and committed.** A run that picks this up starts at Phase 5 with a
storyboard that has already passed `dossier_check`, claims that have already
passed `claims_check`, and a raymarched hero scene that already renders.

## THE STORY, ALREADY SELECTED AND ALREADY VERIFIED

The Sitka Tribe of Alaska's AI video escapement counter at the Redoubt Lake
weir, and the funding structure that will not pay for it because it works.

**Everything you need is on the branch `claude/carousel-2026-08-08`:**

- `runs/2026-08-08/claims.json` — **38 verified claims, claims_check PASS,
  18 primary.** Seven claims were killed and the reasons are recorded. Do not
  re-run the fact-checker unless you change the story. Re-verify freshness only.
- `runs/2026-08-08/storyboard.md` — **a complete 9-slide storyboard,
  dossier_check PASS 9/9**, with full camera arithmetic, palette hexes, type
  spec, continuity state table, data-in-art mappings and per-slide acceptance
  checklists.
- `runs/2026-08-08/selection.md` — the dedupe reasoning and the hard rules.
- `runs/2026-08-08/treatments/` — the two losing pitches, summarised.
- `runs/2026-08-08/slides/` — slides 01, 05 and 06 as built HTML.
- `runs/2026-08-08/render/` — those three rendered at 2x.
- `runs/2026-08-08/build_slides.py` — the generator.

## THE THESIS, AND THE DEVICE THAT CARRIES IT

**The system is not broken, and that is the problem.**

The deck is a single continuous underwater take at the weir. One world, one
light, nine camera positions. **Slides 05 and 06 are the same camera, the same
scene function, the same fish at the same world position, and between them the
key light falls from 8:1 to 1:1.** Nothing about the object breaks. Only the
light that makes it legible is gone. That is the install grant existing and the
operating money not existing, rendered rather than written.

Three directors pitched blind and independently agreed on four things, which is
the strongest signal the room has ever produced. All four are settled:

1. **C13, the 80.2 percent mean average precision, is struck from the deck
   entirely.** Two incommensurable accuracy numbers can't collide if only one of
   them exists. Do not reinstate it to "balance" C22.
2. Instrument Serif + Archivo + JetBrains Mono. Fraunces stays out.
3. `aksdf` over `akthree`, because there is no GL context to fail and therefore
   no fallback to slide into.
4. A tannin-water palette from the story's material world.

## WHAT IS ALREADY BUILT AND WORKING

`out/2026-08-08/probe/` and the three slide files carry a **validated aksdf
scene** of the Redoubt chute world, 9 primitives, rendering in about 10 to 12
seconds per frame at 440x660 internal. It produces a genuinely lit aperture
between dark weir pickets on a lit bed with real cast shadows. The composition
the storyboard describes, a rationing gate drawn as light between bars, works.

Two engineering findings that cost this run real time and should not be
rediscovered:

- **`aksdf` material `emissive` must be an ARRAY `[r,g,b]`, not a scalar.**
  Passing a number makes `S.mul` index a number, every channel goes NaN, the
  pixel writes 0, and the surface renders black with no console error. This is
  the same class of silent failure as the `lerpHex` nesting instinct.
- **A far emissive plane is not visible down a 2.4 m tunnel from an off-axis
  camera.** The acceptance half-angle is about 5 degrees and the camera sits
  about 21 degrees off axis. The fix that works is a short emissive plug just
  inside the mouth, which is also physically right for translucent polyethylene.

## WHAT REMAINS

1. Build slides 02, 03, 04, 07, 08, 09 from their dossiers. They are all
   Canvas 2D and the dossiers are complete enough to code from directly.
2. **Fix the luminance probe rectangles on 01, 05 and 06 before trusting them.**
   The ones committed are in the wrong place: they were authored from the
   storyboard's predicted screen coordinates rather than measured off a render,
   and the measured separations came out backwards (slide 06 read BRIGHTER than
   slide 05, which is the opposite of the argument). Locate the aperture from an
   actual render first, masking out DOM text, then set the rects. The 05 and 06
   gate (05 at or above 40 L* separation, 06 at or below 12) is the deck's
   central claim and it must be measured, not asserted.
3. Then the normal pipeline from Phase 7's render gate onward.

## THE CAPTION ROOM ALREADY RAN

Two candidates and a critic verdict are in the run record. Both directors
independently flagged that their assigned closing moves were burned in the
ledger, which the showrunner's brief had failed to quote. Read
`runs/2026-08-08/caption_room.md` before re-running the room, and if the story
is unchanged, prefer applying the critic's verdict to re-running it.

## THE RUNNER-UP STORY, IF YOU WANT SOMETHING FRESHER

**UAF was awarded $499,000,000 on August 7th**, contract W911NF-26-D-A013, Army
Contracting Command, for the geophysical detection of nuclear proliferation.
One bid solicited, one received. Runs to August 6th, 2031. UAF's Geophysical
Institute holds the only University Affiliated Research Center in the country
charged with that mission, and its Wilson Alaska Technical Center runs nearly
two dozen seismic and infrasound arrays worldwide.

It lost on one thing and the reason is worth respecting. **The contract face
carries no AI or ML language.** There IS documented machine learning there, and
it is remarkable: Alex Witsil generated 28,000 SYNTHETIC infrasound signals to
train explosion-detection models, published in Geophysical Research Letters
(doi 10.1029/2022GL097785), because real large explosions are too rare to train
on. That is a 2022 paper under a different funder. Connecting it to the award
announced this month would be the deck asserting something no page supports.

Run it when the statement of work is readable, or when the centre publishes
something current. Do not run it by implying the link.

## OTHER VERIFIED MATERIAL HELD BACK, WITH SOURCES

- **Fisheries Science Modernization Act**, introduced August 6th by Murkowski
  and Whitehouse, Sullivan cosponsoring. Its capacity title directs NOAA to
  establish procurement pathways encouraging AI-enabled autonomous sampling
  systems. Five of twelve endorsers are Alaska organisations. Primary is the
  Murkowski newsroom release. Weak peg (a bill two days old with no hearing
  date), strong material.
- **NSF awards 2614749 and 2614751**, $4,737,612 combined to UAA and UAF on
  August 5th, reinforcement-learning controllers on a bioprocess digital twin.
  **NSF 2608510 (GAIA)**, $1,772,170 to UAF, started August 1st.
- **XPRIZE Wildfire at Nenana.** Winner expected September 2026. No.5 already
  ran this on 2026-07-12, so September must be an explicit update on the result.
- **FCC E-Rate, docket 26-133.** More than $200 million a year to Alaska schools
  and libraries. Connectivity rather than AI, so it needs an honest frame.
- **NOAA GAIA beluga monitoring**: in June 2025 the satellite tasking timed to
  the beluga aerial abundance survey returned no imagery at all, because
  competing regional priorities including the Port of Anchorage outbid it. A
  monitoring programme losing its own scheduled observation to a port is a deck.

## ONE THING NOT TO DO

The Anthropic donations story surfaced as the lead finding of four of six
scouts and is plainly the loudest Alaska AI story of the week. **It has already
run twice**, as No.17 on July 25th and No.21 on July 31st, and No.21's own
ledger entry records that it disclosed on its cover that it was the second deck
on those donors in seven days. A third inside a fortnight is a fixation. It is
also this publication's own maker, so the call belongs to the maintainer rather
than to an unattended run. It is flagged in the 08-08 draft.
