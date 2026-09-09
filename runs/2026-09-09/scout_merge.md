# SCOUT MERGE — 2026-09-09 — Carousel No. 54

Six scouts, all six returned. 148 of the session's WebSearch calls spent here
(A 25, B 25, C 25, D 25, E 25, F 23), plus 4 in Phase 1. Every scout hit or
neared its cap, which is what the cap is for.

## A ROUTE THAT WORKS, worth carrying forward

Four of six scouts independently found the same wall and the same way round it.
`federalregister.gov` document HTML pages 302-redirect to
`unblock.federalregister.gov` and cannot be read. Two routes fetch cleanly and
should be the default from now on:

- `https://www.govinfo.gov/content/pkg/FR-<YYYY-MM-DD>/html/<doc-number>.htm`
  for full text
- `https://www.federalregister.gov/api/v1/documents.json` for search and
  metadata, and `/documents/full_text/text/<Y>/<M>/<D>/<doc>.txt` for raw text

Also confirmed dead to WebFetch this run, across scouts: alaskabeacon.com (403,
route around it via alaskapublic.org), rca.alaska.gov (403), defense.gov
contracts (403), sam.gov (JS shell), regulations.gov (403), nsf.gov award pages
(JS shell, but `api.nsf.gov/services/v1/awards.json` returns the same record
with full abstracts and is primary), newsminer.com (429 under repeat fetches),
transportation.gov (403), agu.org (403). Reddit remains unreachable and was not
attempted.

## THE CANDIDATE FIELD

### 1. EO 14421 AND THE DOE SCOPE DOCKET  [Beat D, PICKED]

A national emergency declared over foreign-made grid equipment, whose stated
reason names artificial intelligence and data centers, and whose scope is being
written right now in a docket that closes October 9th.

- Executive Order 14421 of August 26th, 2026, "Declaring a National Emergency To
  Secure the United States Bulk-Power System", published August 31st at
  91 FR 55995.
- The order's own reason, verbatim, is demand side. "The rapid growth of
  advanced manufacturing, data centers, artificial intelligence, and defense
  production has increased the Nation's dependence on abundant, reliable
  electricity and magnified the consequences of a successful attack or supply
  disruption on the bulk-power system."
- The order defines its own reach in Section 5(a), independently, with no
  reference to the Federal Power Act. "(i) facilities and control systems
  necessary for operating an interconnected electric energy transmission network
  (or any portion thereof); and (ii) electric energy from generation facilities
  needed to maintain electric system reliability. For the purpose of this order,
  this definition includes transmission lines rated at 69,000 volts (69 kV) or
  more, but does not include facilities used in the local distribution of
  electric energy."
- Covered equipment reaches substation transformers, grid-connected inverters,
  battery energy storage, uninterruptible power supplies, protective relaying,
  high voltage circuit breakers, generation turbines and industrial control
  systems.
- 120 days for the Secretary of Energy to publish implementing rules, 180 days
  for recommended Federal Acquisition Regulation revisions.
- On September 9th, 2026, TODAY, DOE's Office of Cybersecurity, Energy Security,
  and Emergency Response published the Request for Information that will set the
  scope, at 91 FR 57322 to 57328, docket DOE-HQ-2026-1123, RIN 1901-AB79.
  Comments due October 9th, 2026. Its question A-2 asks respondents to
  "Identify any equipment-specific voltage, capacity, connectivity, function,
  location, or criticality thresholds that would improve clarity without
  creating material security gaps."
- VERIFIED BY THE SHOWRUNNER DIRECTLY, both documents, on govinfo. The words
  Alaska, Hawaii, islanded, non-contiguous and interconnection appear in neither
  the order nor the RFI.

WHY IT IS THE PICK. The hinge is one word in the order's own definition,
"interconnected". Alaska's Railbelt is not interconnected to any grid outside
Alaska, so whether the order reaches it is a live question with no published
answer, and the single document that will answer it is open for comment for
thirty more days and asks for exactly the criteria that would settle it. That is
a forward, actionable, structural Alaska story with a named docket, a named
deadline, and a fork a reader can take a side on.

### 2. FERC DOCKETS DEEPGREEN'S COOK INLET SUBSEA DATA CENTER  [Beats A, D, E]

Found independently by three scouts, which is the strongest confidence signal in
the sweep. FERC accepted DeepGreen Cook Inlet SPV, LLC's preliminary permit
application, Project No. P-15423-000, published at 91 FR 56879 on September 4th.
First hard specification on the federal record: 330 to 350 marine hydrokinetic
turbines, 66 modular subsea-compute hives, an approximately 3.5-mile 115 kV
hybrid power and fiber-optic armored subsea cable landing in the Nikiski
Industrial Corridor, 100 MW estimated annual generation. Comments, motions to
intervene and COMPETING APPLICATIONS due 5:00 p.m. Eastern November 2nd, 2026.
The same promoter's Maine sibling, P-15424-000 at Eastport, is 4.8 MW, 16
turbines and 34 pods, closing October 19th.

NOT PICKED. The topic ran on 2026-08-21, nineteen days ago, and the dedupe rule
would force an explicit UPDATE reframe. That is available and honest, and it is
the runner-up. It loses to candidate 1 on freshness (a September 4th notice
against one published today) and on distinctness.

USED AS A SUPPORTING FACT INSTEAD. The cable is rated 115 kV, above the order's
69 kV line, which is a concrete Alaska object standing on the right side of the
threshold candidate 1 is about.

### 3. TWO FEDERAL SURVEYS DECIDE WHETHER TO KEEP ASKING ABOUT AI  [Beat D]

Also published today. Census's Business Trends and Outlook Survey clearance
notice at 91 FR 57314, OMB 0607-1022, "requests approval to repeat the
artificial intelligence (AI) supplement with minor content changes" and moves
some AI questions into core content; 1.2 million businesses in six panels,
published at national and state level plus the 25 most-populous metros, which
does not include any Alaska metro. NTIA's Internet Use Survey notice at
91 FR 57320, OMB 0660-0021, asks the public directly "Is there a need for more
data around artificial intelligence (AI)?"; 50,000 households, comments due
November 9th.

NOT PICKED, held as a strong lead for a later run. It is genuinely fresh and
genuinely uncovered, and it is a quieter story than candidate 1.

### 4. GVEA CUTS ITS FUEL RATE 12.6 PERCENT  [Beat A]

Effective September 1st, about 2.6 cents per kilowatt hour, roughly $15 a month
for an average residential member, reversing a June 1st record high. GVEA's COO
told the Alaska Municipal League on August 28th that a large flat-profile load
"can be a great addition to the electrical system and help bring costs down" but
that "the larger it gets, the more detailed the analysis gets."

NOT PICKED. Real and uncovered, but the AI connection is contextual rather than
causal, and the sourcing is a single television interview.

### 5. HARVEST MIDSTREAM SLIPS NIKISKI LNG IMPORTS TO 2029  [Beat A]

A September 1st release now targets first imports "as early as 2029" against the
first-half-2028 date Harvest published when it bought the terminal in November
2025. NOT PICKED, sourced to trade coverage of a release, and not an AI story.

### 6. EIGHT NSF AWARDS TO UA CAMPUSES ALL START SEPTEMBER 1ST  [Beats B, C]

$8,156,411 across eight awards, $6,375,759 of it AI or machine learning across
three projects: a $4.74 million AI-driven critical mineral recovery pair at UAA
and UAF, the $1,588,147 FIRE-WUI machine-learning fire weather toolkit, and a
$50,000 I-Corps award on explainable AI for satellite bathymetry. Beat C also
surfaced the $10.5 million ten-year Alaska Critical Mineral Accelerator Engine
and the $1,772,170 GAIA geophysical digital twin award.

NOT PICKED. "NSF awards to University of Alaska campuses" ran on 2026-08-26,
fourteen days ago. Different awards, same story shape, inside the window.

### 7. NPFMC'S 2027 OBSERVER DEPLOYMENT PLAN  [Beat C]

Comment opens September 11th and closes noon October 2nd; the Council votes
October 5th to 13th at the Egan Center. The 2026 plan carries $4.75 million,
4,341 trips, 181 fixed-gear and 114 trawl electronic-monitoring vessels, and
AFSC's computer-vision layer reports about 94 percent species identification
accuracy. NOT PICKED, adjacent to the 2026-09-06 deck.

### 8. THE ALASKA TRIBAL HEALTH SYSTEM'S OWN AI GOVERNANCE FRAMEWORK  [Beat B]

Published May 23rd, 2026 in the International Journal of Circumpolar Health by
ANTHC, Southcentral Foundation, Maniilaq and Stanford. Data sovereignty as the
precondition, a dual IRB review architecture, and a 2022 baseline where 35
percent of 81 respondents had never heard of AI. Out of window and excellent.
QUEUED as the strongest standing lead in the sweep for a future run.

### 9. NSF EPSCOR GRADUATE FELLOWSHIPS, AND ALASKA HAS NONE  [Beat B]

18 awards, $21,887,325, 16 EPSCoR jurisdictions since August 4th, none to an
Alaska awardee. The scout flags its own limit honestly, that this is an absence
in the award database and not a confirmed NSF decision. NOT PICKED for that
reason. An absence claim needs a source that says no, not a search that finds
nothing.

## COMMUNITY SALIENCE, from Beat F, applied rather than sourced

Beat F's measurement is that the Alaska tech argument this week is Anchorage
surveillance and Fairbanks data centers, and that the Fairbanks letters column
has gone entirely to the October 6th school board race, ten letters between
September 3rd and 8th with zero on AI, data centers or energy technology. It
also found no Alaska-specific data-center polling anywhere; every percentage in
circulation is national. That is a warning carried into the storyboard. No
national number gets an Alaska label on a slide.

Beat F's own count of Anchorage coverage, six outlets across the ideological
range in nineteen days, confirms the surveillance ordinance is the loudest
story. It ran on 2026-08-25 and is burned.
