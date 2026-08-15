# DIRECTORS ROOM BRIEF — carousel No. 33, 2026-08-14

Shared by all three treatment directors. Your lens is in your own prompt.

## THE STORY

NSF opened its State and Regional Artificial Intelligence Infrastructure Hubs
program (solicitation NSF 26-513) on August 4th, 2026. NSF announced it as a
$100 million initiative (C10) while the solicitation itself puts anticipated
funding at $40 million to $100 million (C11). It anticipates 10 awards per
cycle (C12) and expects proposals to request $4 million to $12 million over
5 years (C13). Full proposals are due November 4th, 2026 (C06), which is 82
days from this run date (C07).

Two rules decide the shape of it, and they are the deck:
1. "Only one award per state or multi-state region will be made." (C01)
2. "An institution may appear as a participant in at most one proposal." (C03)
   If it appears on more, only the first is reviewed and "All others will be
   returned without review." (C04)

NSF's own stated reason for the program is that access to AI infrastructure
remains highly uneven across the nation (C08 in the solicitation, C09 in the
announcement, and the two are worded differently, so match the quote to the
URL you cite and never blend them).

## THE THESIS TO DRAMATIZE

The remedy is distributed at a flat rate and the problem it names is not flat.
One award per state treats Alaska and Rhode Island as the same size of need,
though Alaska's land area is about 552 times Rhode Island's (C23, C24).
Alaska's whole claim on the program is one application, and the only date that
matters is November 4th.

## CORRECTIONS THE FACT-CHECKER FORCED, AND THEY BIND YOU

The adversarial pass killed three framings that were in the first version of
this brief. Do not reintroduce any of them. They are in the `killed` array of
claims.json with the reasoning.

- **Cost sharing.** The verified sentence is that inclusion of VOLUNTARY
  COMMITTED cost sharing is prohibited (C05). That bars a proposer from
  pledging match inside the proposal. It is routine NSF boilerplate and it does
  NOT stop Alaska or a university from spending its own money on compute. Any
  treatment that says NSF forbids Alaska to add money is wrong and will be
  rejected.
- **The money.** Never write that NSF is spending $100 million. The
  announcement says $100 million, the solicitation says $40 million to $100
  million, and the honest sentence carries both.
- **Institution counts.** No source was verified for how many research
  universities any state has. The size argument is carried by LAND AREA and
  nothing else.
- **A missed cycle is not exclusion.** The solicitation sets subsequent
  deadlines on the first Wednesday in November (C22). The deck must not imply
  Alaska is shut out forever if November 4th passes. The argument is about the
  cap, not about a cliff.

The private-land contrast (the AIDEA parcel, the North Slope campus) has been
DROPPED entirely, because the DNR notice does not state a compute end use and
asserting one would misrepresent a primary document. Do not build it back in.

Be FAIR to NSF. One award per state is a defensible design choice with an
obvious rationale, geographic spread. The argument is not that anyone did
something shady. It is that a flat remedy for an uneven problem leaves the
unevenness roughly where it was. That is a structural observation and it
survives being generous to the agency.

Nothing in the record says Alaska has applied, is applying, or has been refused.
Do not imply any of those. The window is open and the cap is written.

## USE ONLY VERIFIED CLAIMS

`out/2026-08-14/claims.json` is the only source of truth. Every number and every
quote on a slide carries a claim-id. If it is not in claims.json, it does not
exist. Read `out/2026-08-14/selection.md` and `out/2026-08-14/scout_merge.md`
for context on why this story and not another.

## THE STANDING WEAKNESS THIS RUN IS ATTACKING

Read `out/2026-08-14/plan.md` for the trend report in full. The short version.

**Artwork craft and genuine detail has been the weakest scored criterion in 7 of
the last 10 runs, mean 6.0, and 6.0 again last run.** The failure has a shape.
No. 32 shipped a beautiful concept (a letterpress composing stone) and still
scored 6.0, because the whole craft budget went into ONE technique run across
all nine slides. No. 31 did the same with a scale rail. The decks read as one
good idea nine times rather than nine drawings.

Your treatment is graded on whether it fixes that. Three commitments bind you:

1. **A TECHNIQUE BENCH, NOT A TECHNIQUE.** Name at least FIVE distinct
   TECHNIQUE_LIBRARY techniques and assign each to specific slides. No single
   technique may carry more than four of the nine slides.
2. **DRAWN SHARE ABOVE 65 PERCENT.** `bespoke_check.py` fails under 45. The
   bespoke reference deck measures 82. A gradient inside a fillRect is still a
   box, and the maintainer's own words for the failure mode were "blocky, almost
   like a kid was drag and dropping shapes into the slides."
3. **THE BOTTOM BAND IS DESIGNED FIRST.** Two of the five recurring defect
   classes (top-loaded composition, outside safe zone) are the same defect twice,
   and the scorer has named the dead lower zone in six consecutive runs. Every
   slide's lower third carries something with modelled tone, planned before its
   hero is planned.

Secondary target: legibility and platform fitness (weakest 3 of 10, never worked
on). qa.py's text-collision check is DOM-only, so any label set against canvas or
SVG geometry can collide freely and still pass. Every art-band label in your
treatment ships on an opaque knockout plate by default.

## WHY THIS STORY SUITS AN ATTACK ON ARTWORK CRAFT

The rule pays no attention to area, population or existing capacity. So the art
can draw the thing the rule refuses to see. Alaska is the largest state and its
allocation is identical to the smallest. That is cartographic, material and
physical, not diagrammatic. Committed true lon/lat Alaska geodata, all 29
boroughs, a 40-place gazetteer and the canonical projection are in `assets/geo/`,
and `akrelief.js`, `akthree.js`, `aksdf.js`, `akcolor.js` and `akpost.js` are on
the bench.

BEWARE the obvious trap. A story about money and slots and deadlines invites a
deck of rectangles, bars and calendars. That is exactly the failure this run is
attacking. If your treatment's strongest image is a bar chart or a grid of
boxes, it is the wrong treatment.

## VARIETY CONSTRAINTS, HARD

FORBIDDEN HERO STRUCTURES (last 4)
- THE LIT APERTURE (29), backlit slot in tannin water, aksdf, dollying camera
- THE OPEN TREAD (30), stepped instrument on lit birch floor, orthographic
- THE FALLING FRAME (31), scale itself as the variable, nine rungs and back
- THE LOCKED CHASE (32), letterpress composing stone, fixed 30 degrees

FORBIDDEN ATMOSPHERES (last 3)
- NORTH WINDOW HIGH KEY (30), broad interior daylight, key 300/26, 2.4 to 1
- TAILRACE SLATE AND COPPER WINDING (31), cold slate, key 305/21, matte copper
- LOCKUP RAKE (32), single hard sodium work lamp, key 292/24, 6 to 1, no fog

FORBIDDEN CONTINUITY DEVICES (last 2, plus one still fresh)
- No. 31's rung-by-rung relabelling scale rail
- No. 32's locked-chase furniture grammar and wet-ink specular register
- No. 30's floor-datum plinth and its clay-and-stone substance code

FORBIDDEN HOOK ARCHETYPES (last 3, plus one)
- THE MEASURE THAT STOPS (30), No. 31's question-first archetype,
  THE HONEST WITNESS (32), and THE DISQUALIFYING VIRTUE (29) is also spent

FORBIDDEN PALETTE FAMILIES (last 3)
- BIRCH FLOOR AND NORTH WINDOW (30), TAILRACE SLATE AND COPPER (31),
  TYPE METAL AND NEWSPRINT (32)
- Practical read: three consecutive decks spent gold #FFC72C as a
  single-meaning accent, and two of the last three sat on a near-black cold
  base. Both are due for a break. Gold stays as a brand anchor, but find it a
  different job, or a much smaller one.

FORBIDDEN TYPE PAIRINGS (last 2)
- No. 31: Unbounded + Fraunces + Archivo wdth 62
- No. 32: Instrument Serif + Archivo (78/100) + JetBrains Mono
- Instrument Serif, Archivo and JetBrains Mono have each appeared in three of
  the last five decks. Retire at least two of them. The committed library also
  holds Space Grotesk, Manrope, Bricolage Grotesque and Unbounded.

## VARIANCE DIALS, SET BY THE SHOWRUNNER

- design_variance 5 (No. 32 ran 4; the standing weakness demands further out)
- visual_density 5 (No. 32 ran 4, No. 30 ran 2; density is the dial that buys
  genuine detail in every region, which is the criterion that keeps losing)
- type_temperature 5 (No. 32 ran 2, No. 30 ran 3.5; this deck's type gets
  warmth and expression rather than institutional cool)

Density 5 carries a known cost. Budget the bottom band and the 80px safe zone
in the plan, not in a repair pass.

## DECK SHAPE

9 slides (1 cover, 7 content, 1 close). Cover 12 words or fewer. Slide 2 pays
off immediately. A breather exists and is declared. A keepable data slide
exists. Single-ask close carrying "sources in comments" and alaskaaihq.com set
small in the mono face near the brand mark. At least 2 continuity devices.

## WHAT TO RETURN

ONE complete deck treatment, conceived through your assigned lens:
- the deck's thesis in one sentence and a title of 60 characters or fewer
- the NAMED hero structure, with a paragraph on how it diverges from all four
  forbidden ones, specifically
- the NAMED atmosphere, with its key azimuth, elevation and key-to-fill ratio
- the NAMED hook archetype and the cover line
- the palette family with hex per role, and where gold appears if at all
- the type pairing, with the axes you are loading
- the continuity devices, at least two, with their state across all 9 slides
- a slide-by-slide arc, one line each, naming the technique assigned to each
  slide and the claim-ids it rests on
- the technique bench, at least five named library entries with numbers
- your honest risk list

Do NOT write full dossiers. The showrunner synthesizes, then writes them.
Do NOT spawn subagents.
