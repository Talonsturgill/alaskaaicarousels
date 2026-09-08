# SCOUT MERGE — 2026-09-07 — run No. 53

Six scouts spawned, each capped at 20 WebSearch calls. All six returned; Beat C
came in last, after the merge was first drafted, and its findings are folded
into the runner-up list below.

## THE HEADLINE RESULT, and it changes the deck for the better

The queued brief made completeness a PRECONDITION. Beat D answered it, and the
answer is **NOT ESTABLISHED, with a proof rather than a suspicion.**

Two things came out of that work.

**First, run No. 52 was wrong about why its result sets looked short.** FPDS
returns 10 entries per page and the fetch layer's summariser only ever reports
the first 5 or 6. Stepping `start` by 5 instead of 10 recovers the hidden half.
Every "five entries" observation was a reading artifact, not an FPDS defect.
That correction is worth carrying forward on its own.

**Second, and this is the deck.** FPDS phrase search is not internally
consistent, and it can be shown in two queries:

| query | phrase, vendor state Alaska | records |
|---|---|---|
| A | `"ARTIFICIAL INTELLIGENCE"` | **24** |
| B | `"ARTIFICIAL INTELLIGENCE, AND MACHINE LEARNING"` | **25** |

B's phrase is a STRICT SUPERSET of A's. Any description containing B's string
necessarily contains A's. Same field, same filter. Yet the narrower query
returns MORE records, and it surfaces three contracts that A's complete
enumeration never shows, including the largest Alaska-named AI contract found
all day. A subset returning more than its own superset is impossible for a
correct index.

The apparent mechanism, fitting four independent cases. **When "ARTIFICIAL
INTELLIGENCE" is followed immediately by a comma, FPDS phrase matching fails.**
The three misses all read `ARTIFICIAL INTELLIGENCE,`. The hits all read
`ARTIFICIAL INTELLIGENCE (AI)`.

So the deck cannot publish a total, a rank, a share or a "most of", exactly as
the brief instructed. It publishes something better. A comma is hiding a
twenty million dollar artificial intelligence contract from the public's own
search for artificial intelligence contracts.

Counts that ARE established (rel=last offset plus the final page, confirmed by
paging to ZERO ENTRIES): A=24, B=25, place-of-performance Alaska plus "artificial
intelligence"=1, place-of-performance Alaska plus "machine learning"=9,
vendor-state Alaska plus "machine learning"=42, Koniag actions signed August
25th to September 7th=30.

## THE CONTRACT THE COMMA HID

**Leisnoi Professional Services LLC**, subsidiary of the ANCSA village
corporation for **Woody Island** in the Kodiak Archipelago.

- PIID **HQ003425CE092**, Washington Headquarters Services, the office that runs
  the Pentagon building
- "A NON-PERSONAL SERVICES CONTRACT TO PROVIDE INFORMATION TECHNOLOGY,
  ARTIFICIAL INTELLIGENCE, AND MACHINE LEARNING PROGRAM SUPPORT SERVICES"
- **$20,632,119.41** obligated across 8 actions, exactly its ceiling, to the cent
- 8(a) sole source, awarded September 11th, 2025
- **Period of performance ends September 10th, 2026**, two days after this run
- NAICS 541512, Computer Systems Design Services

SOFTEST LINK, flagged by the scout and sent to the fact-checker as such. The
Leisnoi Professional Services to Leisnoi, Inc. parent relationship rests on the
shared name and a shared Anchorage address in FPDS and usaspending, NOT on a
corporate page stating it.

## THE SEVEN-YEAR KODIAK CHAIN

The same requirement sentence has been bought from Kodiak-connected entities
since 2019, handed on without a gap.

| when | who | contract | obligated |
|---|---|---|---|
| 2019-2020 | Tuknik Government Services | 140D0419C0047 | $9,479,118.55 (floor) |
| 2020-2021 | Tuknik Government Services | 140D0421C0002, for the DOD CIO's Joint AI Center | $24,210,536.43 |
| Mar 2025 to Sep 10th 2025 | Koniag IT Systems | HQ003425CE012 | $12,022,390.38 |
| Sep 11th 2025 to Sep 10th 2026 | Leisnoi Professional Services | HQ003425CE092 | $20,632,119.41 |

Koniag IT Systems completed September 10th, 2025. Leisnoi began September 11th,
2025. One day, same contracting office, same requirement. Tuknik is a wholly
owned subsidiary of Koniag Government Services, which lists 28 subsidiaries,
one of them named **Koniag AI Solutions, LLC**.

## WHERE THE WORK ACTUALLY HAPPENS

- Place of performance Alaska plus "artificial intelligence" returns **exactly
  one** record. W519TC26CA019, Koniag Emerging Technologies, **$5,267,244.80**,
  8(a) sole source, Army ACC-Rock Island for the Deputy to the CDAO, place of
  performance **Anchorage 99503**, signed May 29th, 2026, current completion
  May 28th, 2027, potential end **May 25th, 2031**. NAICS 518210. Confirmed
  twice, FPDS and the usaspending API, to the cent.
- Place of performance Alaska plus "machine learning" returns **9**, every one
  of them University of Alaska Fairbanks, every one NASA, Fairbanks, totalling
  **$1,187,674.80**. Auroral substorms, flood and landslide mapping, Jupiter's
  magnetosphere.
- Everything else lands in Alexandria, Falls Church, Arlington, Washington DC,
  Aberdeen Proving Ground, Baltimore, Durham, Annapolis.

Two very different things are both called Alaska AI.

## THE FISCAL WALL

30 Koniag-family contract actions signed August 25th to September 7th, 2026,
across 12 federal agencies (DOE, GSA, USDA, State, SSA, Coast Guard, EPA, USPTO,
USCIS, ITC, Bureau of Engraving and Printing, Rural Housing Service). Roughly
two a day against the September 30th wall.

Inside it, DOE contract 89303026CIM000014. In June its ceiling rose from
$24,524,561.40 to $34,301,950.89, an increase of **$9,777,389.49**, on a
modification whose entire stated purpose reads **"THE PURPOSE OF THIS
MODIFICATION IS TO ADD AI TOOL."** On September 3rd it took another $679,233.27.

## THE FAIRNESS, WHICH GOES EARLY AND ON THE FACE OF THE DECK

All of this is lawful. 8(a) is the mechanism Congress built. What the deck can
say precisely, rather than sentimentally, from Beat B's primary reads.

**The statutory point, and it is the precise one most people get wrong.**
43 U.S.C. 1606(i) requires 70 percent sharing among all twelve regional
corporations of revenue from timber and the subsurface estate. **Services and
government contracting revenue are not covered.** Technology earnings are not
7(i) money. They reach Alaska Native shareholders through the dividend, the
settlement trust, hiring and the education foundation of the one corporation
that earned them.

Koniag's own return channels, from Koniag and KMXT primaries.

- **$33 per share** dividend, distributed January 27th, 2026
- **$1,200** Elder Benefit to original shareholders 62 and older
- **$46,013,900** Shareholder Settlement Trust, after a $3,117,600 contribution
- **4,700+** shareholders today, up from 3,400 at incorporation in 1971
- Koniag Education Foundation, **$10 million+** awarded, **4,000+** scholarships,
  **158** current recipients. Koniag Government Services is a named donor.

And what the work is worth to the buyer. An AWS case study puts Koniag
Government Services' AI and automation for the Army's procurement office at
**$37 million a year** and **687,000 labour hours** saved, at roughly 750
employees and about $800 million annual revenue.

## THE COUNTERWEIGHT, which ships in the deck

A deck that shows only the flattering side of 8(a) revenue reads as a brochure.

- **Koniag Government Services took a $63 million one-year DHS contract
  effective August 6th, 2026 to run a national ICE call center** in Adams,
  Tennessee, population about 600. (Alaska Beacon via Kodiak Daily Mirror.)
- **The register in which Alaskans actually litigate this.** Three Bering
  Straits Native Corporation shareholders petitioned BSNC to divest from ICE
  detention contracts, gathering 102 shareholder and descendant signatures plus
  20 others, against roughly $587 million in BSNC revenue from ICE and Homeland
  Security contracts over a decade. BSNC declined to comment on contract
  details. Expect this reaction rather than be surprised by it.
- **Pete Hegseth ordered a line-by-line review of every 8(a) sole-source
  contract above $20 million** in January 2026. Leisnoi's is $20,632,119.41,
  which is **$632,119.41** above that line. No primary Pentagon document was
  reachable and NO sentence may imply this contract has actually been reviewed.

## THE MEASURED SILENCE, which is the deck's thesis made checkable

Beat F read the opinion fronts of the ADN, the Fairbanks Daily News-Miner and
Must Read Alaska on September 8th.

- **Zero** data centre or AI opinion items across all three, September 3rd to 7th.
- The most recent News-Miner community perspective on data centres is **June
  25th, 2026**.
- **Zero** public Alaskan discussion of ANCSA federal contracting anywhere in
  the window, searched five ways across six outlets.

Meanwhile, in the same ten days, the Fairbanks North Star Borough Assembly put
an AI data centre moratorium on BOTH its state and its federal 2027 legislative
priority lists, the Alaska Municipal League ran a panel on zoning for data
centres, and the delegation split in public (Sullivan for base data centres,
Murkowski against on ratepayer grounds, Dunleavy for as LNG anchor load).

**Frame it as the loud argument and the quiet one, never as "nobody is paying
attention."** Officials plainly are. The asymmetry is between institutional
venues and civic ones, and it is measurable.

An Alaskan has already said the deck's thesis on the record. Ross Johnston of
Commonwealth North, in the ADN on June 6th, 2026: "Nobody has quantified how
much of that $13.5 billion runs through 8(a) contracts." Emil Notti, ANCSA
negotiator, on 8(a) at a May 21st forum: "It is not DEI. It does not create
individual wealth. It is not corporate enrichment. It distributes earnings
broadly."

## RUNNER-UP STORIES, not taken this run

1. **The FERC comment room on DeepGreen's Cook Inlet subsea data centre.**
   Project P-15423-000, comments due 5:00 p.m. Eastern November 2nd, 2026, 330
   to 350 turbines, 66 subsea pods, 100 MW. Strong and actionable, but it is
   already a docket item refreshed today, so it is a docket update rather than
   a fresh carousel topic.
2. **Rainmaker's cloud seeding over the Kenai.** Two autonomous drones, 19
   flares, 374.3 grams of silver iodide, a claimed 19 million gallons, and four
   agencies with no permit between them. Genuinely striking and this page has
   already shipped the 374.3 grams figure.
3. **The September 1st federal cohort.** $6,375,759 of NSF AI awards to UAA and
   UAF plus $3 million ONR to ACEP, all effective the same Monday.
4. **AI watching 4 million Arctic lakes for the hour one drains.** The
   Permafrost Discovery Gateway, about 30 northwestern Alaska lakes drained in
   June and July 2026 on the Seward and Baldwin peninsulas, and the comparison
   that a lake a millennium in the making can empty in a few hours. Strong, and
   the original ran August 26th, one day before the window.
5. **MIT Lincoln Laboratory pushing data through 3.6 feet of Utqiagvik lagoon
   ice at about 1.2 kilobytes per second**, with Ukpeagvik Inupiat
   Corporation's UIC Science as the field partner. Note the honest limit, the
   machine learning is the part that is NOT finished in both of Beat C's
   stories, which is a better story than most AI coverage tells.

## DEAD ENDS worth carrying into sources.yaml

New hosts refusing an automated fetch this run: faa.gov, transportation.gov,
af.mil, tandfonline.com, ancsaregional.com, go.boarddocs.com, commerce.alaska.gov
(AOGCC), federalregister.gov document pages (redirects to an unblock host, while
its JSON API works fine). newsminer.com and army.mil returned 429. mea.coop
/news/ is a 404. rca.alaska.gov still 403s, so no Railbelt tariff or the
GCI/Quintillion approval could be checked.

Two FPDS traps to record: the feed emits no `opensearch:totalResults` and
silently ignores `feedmax`, and the fetch layer truncates pages at 5 to 6
entries, so page by 5 and read the `rel="last"` offset for the denominator.

usaspending's POST search endpoint returns 405 through WebFetch. The GET route
`api.usaspending.gov/api/v2/awards/CONT_AWD_<PIID>_9700_-NONE-_-NONE-/` works
keyless and is the second primary source for any award.
