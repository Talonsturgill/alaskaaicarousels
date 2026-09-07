# SELECTION — 2026-09-06 — Carousel No. 52

## THE STORY

**Alaska's fisheries surveys are being handed to machines, and the hard part is not whether the
machine can see the fish. It is whether it sees them the same way the ship did.**

Two documents, twelve days apart, one question.

On September 3rd, 2026 NOAA Fisheries published a 23-author framework for modernizing
fisheries-independent surveys with autonomous vehicles, stereo cameras, eDNA and machine-read
otoliths. It was led by the Alaska Fisheries Science Center's Stan Kotwicki and fourteen of its
twenty-three authors are AFSC. Its argument is not "the robots are ready." Its argument is transition
under calibration, with overlap, slowly.

On September 15th, 2026 the North Pacific Fishery Management Council's Partial Coverage Fishery
Monitoring Advisory Committee meets to review the draft 2027 Annual Deployment Plan, the document
that sorts Alaska's small-boat fixed-gear fleet into three pools and decides, boat by boat, whether
a human rides along or a camera watches and somebody reviews the video later.

They are the same question asked at two altitudes. Who or what does the looking, and what happens to
the record when the looker changes.

## THE THESIS

A survey is not a measurement. It is the SAME measurement, repeated, for decades. Its whole value is
its sameness, because a stock assessment reads the difference between this year and last year and
can't tell a change in the fish from a change in the instrument. So replacing a ship with a robot is
not an upgrade problem, it is a continuity problem, and it is the one problem a better sensor makes
worse rather than better.

And Alaska is being asked to change the instrument in exactly the years the fish are moving north.

That is the sentence the deck is built to earn. It is not anti-machine and the deck never is. NOAA's
own framework says the same thing more politely, which is why the framework is the story rather than
the press release about it.

## WHY THIS ONE, against the four criteria

**1. Concrete Alaska impact.** Every groundfish quota in the Bering Sea and the Gulf of Alaska is set
off these surveys. This is the largest fishery in the United States by volume and the survey time
series is the instrument that governs it. There is no bigger measurement in Alaska.

**2. Visual potential.** Very high, and specifically high for the compositional problem this run is
attacking (see plan.md). A survey grid is geometry. A ship track and a Saildrone track over the same
polygon is a comparison a reader gets with no words. A seabed, a deck, a trawl path and an otolith
are all objects that sit LOW in a frame, which is exactly the composition this run set out to build.
The 0.006 percent of seabed figure is a quantity begging to be drawn honestly. Three monitoring pools
are three basins.

**3. Tangibility.** A boat, a camera, a person on a deck, a fish, an ear bone. Nothing here is abstract.

**4. Would an Alaskan send this to a coworker?** Yes, and to a specific list of them. Kodiak, Dutch
Harbor, Sitka, Juneau, the Council's own advisory panel, and every Seattle-based Alaska fleet office.
The September 15th date makes it forwardable rather than merely interesting.

## DEDUPE GATE

`python scripts/dedupe_check.py` run with the candidate's entities and keywords. Exit 0. Three SOFT
OVERLAPS, no LIKELY DUPLICATE. Strongest match No.44, 2026-08-29, jaccard 0.043, one shared entity
("noaa fisheries"). Read in full, as the script demands:

**No.44 (2026-08-29), "Written Before the Water."** The Woods Hole / Oregon State / UAF Chukchi Sea
acoustic glider, Unit 595, and its published eight-class call library. Its angle was recorded as "A
CLASSIFIER REPORTS WHAT IT WAS TAUGHT TO NAME. THE LIST WAS WRITTEN BEFORE THE GLIDER WENT IN THE
WATER." Different water (Chukchi, not Bering), different animals (marine mammals, not groundfish),
different institution, different instrument, and a different argument. No.44 is about the CATEGORIES
a model can report. This deck is about the CONTINUITY of a record when its instrument changes. A
reader who saw both would recognise them as siblings on a beat, not as the same deck twice, and the
storyboard states the divergence on its face.

**No.29 (2026-08-08)**, the Sitka Tribe's Redoubt Lake escapement counter, is 29 days back and inside
the window. Its angle was THE SHAPE OF THE MONEY, a working instrument disqualified from funding by
working. Also distinct. Shares no entity with this candidate.

Verdict: not a duplicate, no UPDATE frame required, and the beat overlap is disclosed in the
storyboard header rather than hidden.

## RUNNER-UP, and it is a strong one

**Alaska Native corporation 8(a) contracts are where the federal AI money with an Alaska name on it
actually is.** From the FPDS-NG public ATOM feed, which is keyless and primary and which this run
discovered works where sam.gov and govtribe both 403. Koniag Emerging Technologies holds
W519TC26CA019, "Artificial Intelligence (AI) Rapid Support (AIRS)" for the Army's Chief Digital and
Artificial Intelligence Office, $5,267,244.80, place of performance Anchorage, ultimate completion
May 25th, 2031, 8(a) sole source. Around it, a cluster of Koniag subsidiary obligations signed
between August 27th and September 4th against the September 30th lapse.

Nobody has written this and it is genuinely surprising. It was passed over for two honest reasons and
neither is that it is weak. First, the scout's FPDS pulls paginate and returned implausibly short
result sets, so no total, rank or completeness claim could be published without a careful re-pull, and
a deck whose spine is "here is the pattern" needs the pattern to be provably the whole pattern.
Second, a deck about ANCSA 8(a) contracting is a fairness problem before it is a data problem, and it
deserves a run that can give it the room rather than one that arrives at it as a second choice.

**Queued.** It is written into `prompts/NEXT_RUN.md` for the next run, with the re-pull requirement
stated as a precondition rather than a suggestion.

## ALSO CONSIDERED, and why not today

- **FERC accepts the DeepGreen Cook Inlet subsea-compute permit, P-15423-000, comments close November
  2nd.** Real, actionable, and a genuine material development on a tracked item. It went to the docket
  instead of the deck. Data centres, land and grid have taken seven of the last thirty days on this
  page and No.39 ran DeepGreen sixteen days ago. The November 2nd deadline is far enough out that a
  later run can carry it without the reader losing the window.
- **DOE Genesis Mission, one Alaska row out of 637.** A beautiful single number. AURORA-AI itself was
  decked on August 12th, twenty-five days back and inside the dedupe window.
- **Executive Order 14421, a national grid emergency grounded in AI load growth that never says
  Alaska.** The hook archetype, the half nobody is arguing about, was burned on September 4th, and
  the Alaska applicability is an open question rather than a finding.
- **Deep learning doubles the permafrost damage estimate to $261 billion.** Shares the Permafrost
  Discovery Gateway and Woodwell with No.43, nine days back.
- **The Alaska Tribal Health System's own AI baseline survey, and the University of Alaska symposium
  panel on Alaska Native language and data sovereignty.** The most editorially interesting unworked
  lane on the whole sweep, and the reason it is not today's deck is that its documents are May 2026
  and 2025. It needs a live development, and the September 25th to 27th symposium may be it.

## THE DECK

Nine slides. Working title **"The Same Question, Asked Twice."** Final title is the directors room's
to sharpen, but the deck ships nine and the close carries the September 15th date.
