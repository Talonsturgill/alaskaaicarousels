# SCOUT MERGE. 2026-09-05. Carousel No. 51.

Six scouts, window 2026-08-26 to 2026-09-05. 153 WebSearch calls reported across
the six (A overshot its cap at 28 and said so). The sweep was THIN and four of
six beats returned nothing usable, which is itself the finding at daily cadence
after 50 runs on one state's AI beat.

## What each beat returned

**A, power and compute. NOTHING.** Three confirmed absences worth recording.
The Air Force AI data centre land-lease solicitation AFCEC-26-R-0006 closed for
proposals June 29th and archived July 14th, with no award, shortlist or
selection posted through September 5th. STAK Energy's North Slope lease ADL
422741 still sits on DNR's May 12th preliminary finding with comments closed
July 17th and no final finding published. GCI's Quintillion acquisition has not
moved since April. Background it flagged and correctly refused to write up as
AI, Enstar about 18 days short of winter gas with emergency arbitration against
HEX, and a September 3rd BEAD broadband redirect announcement that mentions no
AI anywhere. Dead ends, rca.alaska.gov 403, datacenterdynamics 403, newsminer
429.

**B, research and Indigenous AI. NOTHING IN WINDOW.** The UA Statewide AI
Symposium, September 25th to 27th at UAA with an AI and Alaska session on rural
connectivity and Alaska Native language sovereignty, was announced August 12th
to 17th, outside the window. UAA's RAISE mini-grant statement-of-need deadline
is September 21st. A CANAID tribal-health data-sovereignty paper published in
May. Notable negative, UAF's $3 million ONR ARCTIC award landed in window on
September 1st and mentions no AI, so the scout excluded it rather than stretch
it, which is the correct call.

**C, AI in the field. ONE, AND IT IS BURNED.** The CMS Rural Health
Transformation announcement of August 25th, $160 million across 142 Alaska
projects with $3.1 million for AI imaging at 21 hospitals and $250,000 for a
drone pharmacy framework. RHTP shipped on 08-16 and again on 08-30. Same story.

**D, policy and money. ONE, AND IT IS BURNED AND ALREADY IN THE DOCKET.** The
FERC notice accepting DeepGreen's Cook Inlet preliminary permit for filing,
published September 4th, with a November 2nd comment deadline. No.39 covered
DeepGreen on 08-21 and yesterday's run already added the notice and the
deadline to ledger/docket.json. Nothing new.

**E, robotics and national with Alaska teeth.** The same RHTP story, plus the
FAA doubling its BEYOND drone programme with UAF ACUASI continuing as a lead
site, and AURORA-AI, which is burned from 08-12.

**F, community signal. THE RUN'S ONLY LIVE LEAD.** Three findings, and the
third is the deck. An August 31st SF Standard investigation reported that six
Anthropic employees gave Jonathan Kreiss-Tomkins $372,000, more than a fifth of
his total, while he campaigns on a data centre moratorium. Also useful, the
Anchorage RTCC funding vote passed 8 to 4 on September 1st with the privacy
ordinance held off and Chief Sean Case stating an AI carve-out on the record,
excludes facial recognition, includes weapons and vehicles. Also the FNSB
moratorium going onto both the state and federal priority lists.

## Showrunner's own sweep, which is where the deck actually came from

The scouts found the SIGNAL. They did not reach the record. Three things were
run directly from here.

**1. The Federal Register API, all 43 Alaska documents in the window.** Nothing
AI-related beyond the DeepGreen notice already tracked.

**2. THE APOC CAMPAIGN DISCLOSURE DATABASE, PULLED IN FULL.**
`aws.state.ak.us/ApocReports` refuses a browser and refuses WebFetch, and
answers an ordinary HTTP client fine. The Income report was queried by
Candidate Name for report year 2026 at the default Complete, Not Amended
status, and paged out through the grid. This is the state's own record, not a
retelling of it.

    Jonathan Kreiss-Tomkins   4,604 transactions   $2,379,290.20
    Bernadette M. Wilson      2,379 transactions   $  499,391.31

The full ledger is saved at
`out/2026-09-05/evidence/apoc_kreiss_tomkins_2026_income.csv` and the derived
figures at `evidence/apoc_summary.json`.

What the record says, and every one of these is arithmetic on the state's own
rows rather than anybody's characterisation:

- Six people who list Anthropic or Anthropic PBC as their employer gave
  $372,000, which is 15.63 percent of the entire ledger. Drake Thomas $100,000,
  Daniel Ziegler $70,000, Jan Leike $70,000, Steven Bills $50,000, Evan
  Hubinger $50,000, Tao Lin $32,000. All six list California addresses, four in
  the Bay Area. Dates run February 3rd to May 7th, 2026.
- It takes the 125 LARGEST Alaska gifts in that ledger to reach the same
  $372,000.
- Alaska addresses supplied 2,705 of the 4,604 gifts, 58.8 percent of the
  count, and $632,035.75, 26.6 percent of the money. The median Alaska gift is
  $50.
- California alone supplied $969,843.36, more than Alaska.
- Anthropic is the largest employer bloc in the ledger by a wide margin. The
  largest Alaska-address employer bloc that names an actual employer is the
  State of Alaska at $8,895.
- The comparison candidate, Bernadette Wilson, is 53.2 percent Alaska money.

This independently CONFIRMS the SF Standard's $372,000 to the dollar and adds
the sixth donor's name and all six individual amounts, which that article did
not carry.

**3. THE THING THAT MAKES IT A STORY RATHER THAN A DONOR LIST.** Alaska has had
no limit on what one person may give a candidate since the Ninth Circuit struck
the $500 cap in Thompson v. Hebdon in 2021 and the Legislature never replaced
it. On August 18th, 2026 Alaskans fixed that themselves at the ballot box.

From the Division of Elections' own certified official results PDF, timestamped
8/31/2026, `elections.alaska.gov/enr26/results/ElectionSummaryReportRPT.pdf`:

    BM#1 23RCF2      YES 117,962  72.20%      NO 45,418  27.80%
    Governor primary, top four of seventeen tickets, 164,303 votes cast
      Kreiss-Tomkins / Johnson   DEM/NON   37,006   22.52%
      Begich / Hnilicka          DEM       34,172   20.80%
      Wilson / Shower            REP       16,468   10.02%
      Bronson / Church           REP       13,364    8.13%
    Turnout 166,931 of 601,104, 27.77%

Ballot Measure 1 sets $2,000 per individual per election cycle and $4,000 per
group, adjusted for inflation each decade. Alaska Public Media's Eric Stone,
reporting the night of the vote, states the law takes effect AFTER the November
general election, and that the August primary was Alaskans' only chance to vote
on it.

So the six gifts are 16 to 50 times a cap that 117,962 Alaskans have already
approved, they were legal when made, and the cap does not reach the November
3rd election they were raised to win.

## Dead ends and refusals, recorded

rca.alaska.gov 403 to two independent scouts. akleg.gov BASIS 403, and the
cron sweep's own BASIS call returned 503 today, recorded in ledger/watch.json
under `failed`. federalregister.gov refuses WebFetch and answers its JSON API
fine. Reddit unreachable, as documented. Ballotpedia returns an empty body to
WebFetch. Alaska Beacon 403. Chromium cannot reach the open internet in this
container at all, only an ordinary HTTP client can, which is worth writing down.
