# SCOUT MERGE — 2026-08-15 — Carousel No. 34

Six scouts, all six returned. The session's WebSearch budget was exhausted at
200 calls partway through the sweep, so the later half of every beat ran on
WebFetch alone. Every beat still returned findings.

## The candidate set, ranked

### 1. SELECTED. S. 5171, the Children's Artificial Intelligence Toy Safety Act
Beat D. In window, August 5th, 2026. TWO primary sources.

Senate Commerce held Executive Session 24 on August 5th at 10:00 a.m. in
SR-253. Five bills on the agenda, and three of the five are AI bills:
S. 4199 Youth AI Privacy Act, S. 4407 CHATBOT Act, S. 5171 Children's
Artificial Intelligence Toy Safety Act of 2026. The other two are S. 737
SCREEN Act and S. 1748 Kids Online Safety Act.

S. 5171 is Sen. Tammy Duckworth's, cosponsored by Sen. Lisa Murkowski of
Alaska, and Duckworth's office announced the same day that it passed the
committee. What the bill DOES is the sharpest fact in it. It does not set a
standard, ban anything or require a disclosure. It requires the FTC and the
CPSC to deliver Congress a coordinated PLAN on AI-enabled toys, and directs
the National Academies to STUDY risks to children's physical, mental,
emotional and social well-being.

Quotes on the record. Duckworth, "These AI chatbots were never meant to be
used by young children, yet they're being embedded inside toys by the
thousands." Murkowski, "AI-enabled toys have the potential to significantly
impact the physical, mental, and emotional development of our children."

The Alaska counterweight, from beats B, D and F independently. Alaska's own
statute book on this is close to empty. An August 10th ADN op-ed by Roger
Kaye of Fairbanks records House Bill 47, which criminalized AI-generated
child sexual abuse material and deepfake harassment and became law in June
2026, and House Concurrent Resolution 3, which would have created an AI task
force and stalled. The docket's own watch queue shows SB 2, "AI, DEEPFAKES,
CYBERSECURITY, DATA XFERS," sitting in Senate State Affairs since January
22nd, 2025 with no action. Kaye writes that roughly 30 states passed election
deepfake disclosure laws ahead of the 2026 midterms and that some states now
require companion chatbots to disclose they are not human or therapists.

Why this one. It is the only in-window item where an Alaskan is the ACTOR
rather than the recipient. It collides with nothing in the 30 day window,
`dedupe_check` returns soft overlaps only at jaccard 0.006 to 0.031. And
every deck since No.24 has been about land, power, money or ballots; this one
is about a kid's bedroom, which is the largest available divergence in
subject as well as in art.

### 2. RUNNER-UP. NSF's $4.74 million to UAA and UAF for AI plus microbes
Beats B and E converged on it independently, both against the NSF Award API,
which is primary. Awards 2614749 (UAA, $3,824,575, PI Brandon R. Briggs),
2614751 (UAF, $913,037, PI Srijan Aggarwal) and 2614750 (Montana Tech,
$1,260,800), all dated August 5th, 2026, running September 1st, 2026 to
August 31st, 2030, to pull rare earth elements out of coal mining waste using
bioprocessing and AI. Led out of ANCHORAGE, which is unusual.

Set aside on DEDUPE FRESHNESS rather than on quality. No.33 shipped
yesterday on an NSF AI funding rule, and No.24 shipped twelve days ago on
critical minerals and AI. This story sits at the intersection of both. It is
the strongest story the machine is holding back and it should be first in the
queue when the window clears.

### 3. RUNNER-UP. The FAA's $875 million SMART award
Beat C. August 10th. The FAA awarded Air Space Intelligence $875 million to
build a national airspace management system, and the same company's Flyways
has run at Alaska Airlines since 2021 across about 1,500 daily flights,
credited with about a million gallons of fuel a year. Set aside because the
sourcing is one NPR story carried by Alaska Public Media, the figures are
airline and vendor claims, and the carrier is headquartered in Seattle.

## Everything else the sweep returned, kept for the docket and later runs

- **Beat A.** Alaska Pipeline Company and Enstar are in emergency arbitration
  with HEX Operating over discretionary Cook Inlet gas. Enstar projects
  entering winter 3 Bcf short. No source in the file mentions data centers or
  AI; the connection is inference and the deck refuses it.
- **Beat A.** AEA's board sent a $400 million Bradley Lake expansion
  financing package to the Railbelt utilities, displacing 1.5 Bcf a year by
  2031. Already tracked in the docket as a FERC matter.
- **Beat A and D.** STAK Energy's ADL 422741 still has no Final Finding and
  Decision, 29 days after the extended comment deadline. More than 500
  comments, fewer than a dozen supportive.
- **Beat B and E.** UA's second statewide AI symposium runs September 25th to
  27th at UAA, free and public, seeded by a $29,998.84 UA Faculty Initiative
  Fund award, closing with a statewide AI advisory council strategy session.
- **Beat C.** Juneau's 2026 glacial outburst flood ran on instruments and
  crested at 14.7 feet, over a foot under forecast. NOT an AI story; nothing
  fetched describes machine learning anywhere in it.
- **Beat C.** Alaska's Department of Health began paying out its $272,174,856
  Rural Health Transformation award on August 7th, with AI-enabled tools and
  drones on the allowable-use list. Awards post every Friday. A standing
  weekly feed worth watching.
- **Beat D.** The ANA AI3 Action Institute cooperative agreement,
  HHS-2026-ACF-ANA-NAI-0035, closes August 27th at $2.5M to $3.5M for one
  award, with Alaska Native villages and regional corporations eligible.
  Already tracked in the docket.
- **Beat F.** Six Anthropic employees gave $372,000 to a candidate for
  governor, who is also the only candidate calling for a moratorium on new
  Alaska data centers. Set aside because No.21 and No.17 already covered the
  donations and every named entity is theirs.
- **Beat F.** Reddit is entirely unfetchable from this environment. Hacker
  News carried no Alaska AI item in the window. The ADN letters index is the
  working community-signal surface and should replace Reddit in the beat.

## Sources worth promoting into config/sources.yaml

Named by three or more scouts independently.

- `https://www.research.gov/awardapi-service/v1/awards.json?awardeeStateCode=AK`
  NSF Award API. Keyless, full abstracts, dollar figures, PI names. It
  surfaced the run's strongest held-back story days before any outlet.
- `https://www.northernjournal.com/` Northern Journal. Fetches cleanly where
  alaskabeacon.com returns 403 and carries the same reporting.
- `https://www.petroleumnews.com/section/utilities` Contract-level Cook Inlet
  detail no general outlet carries.
- `https://www.adn.com/opinions/letters/` The working community-signal
  surface now that Reddit is closed.
- `https://simpler.grants.gov/search?query=artificial+intelligence`
  Federal AI opportunities with deadlines, floors and eligibility text.
- `https://www.commerce.senate.gov/hearings` Markup agendas published before
  they happen, which is where an Alaska cosponsor becomes visible early.
