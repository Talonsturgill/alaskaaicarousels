# SCOUT MERGE — No. 38 — 2026-08-20

Six scouts spawned, one per beat. Window August 10th to August 20th, 2026.

ENVIRONMENT NOTE, carried to Phase 12. The session's WebSearch budget (200
calls) was exhausted inside Phase 2. WebFetch continued to work throughout, and
the Federal Register JSON API and full-text HTML endpoints answered cleanly
where the site's own HTML pages redirect to an unblock page. This is the fourth
run in seven to lose WebSearch, and FIELD_NOTES already named the cause on
2026-08-19. It is now a standing defect, not an incident.

## The candidates, ranked after dedupe

### 1. SELECTED — Proclamation 11055 and Alaska's drone-in-a-box network (Beat C)

President Trump signed Proclamation 11055 on August 13th, 2026, published in
the Federal Register on August 19th. It puts a 100 percent ad valorem duty on
imported uncrewed aircraft over 25 kilograms, on any UAS that integrates a
thermal imager, and on UAS docking stations, with 25 percent on aircraft at or
under 25 kilograms. The first tranche bites at 12:01 a.m. eastern on September
3rd, 2026. A second tranche on components follows February 9th, 2027.

The Alaska teeth are the point. Alaska DOT&PF's ARROW and SOAR programs are
built on precisely the two categories drawing the 100 percent rate, docking
stations and thermal-camera aircraft, flown beyond visual line of sight over
villages that have no road. A thermal drone team was working a live search near
Port Armstrong the week the proclamation was signed.

Primary source verified in-session at
https://www.federalregister.gov/documents/full_text/html/2026/08/19/2026-16979.html

Dedupe: SOFT OVERLAP only, strongest match No.13 at jaccard 0.016 on the single
shared entity NOAA Fisheries. Clean.

### 2. RUNNER-UP, and queued for the next run — DeepGreen's underwater AI data center in Cook Inlet (Beat A)

DeepGreen Cook Inlet SPV LLC, a Delaware company whose parent was formed in
January 2026, has a preliminary permit application pending at FERC for roughly
1,650 acres of Cook Inlet seabed west of Nikiski, proposing a 100 megawatt data
center of 66 subsea compute hives powered by as many as 350 marine hydrokinetic
turbines, in 45 to 166 feet of water. It describes tying into the Alaska Energy
Authority's $400 million, 38 mile Cook Inlet PowerLink. AEA chief executive
Curtis Thayer told the Anchorage Daily News on August 19th, "It's extremely
disappointing that they would send something to FERC without contacting us."
FERC sent a deficiency letter on June 18th for omitting the dimensions and
composition of the platform, the turbine array and the compute hives, and for
failing to notify the City of Kenai and to identify all affected tribes and
Alaska Native corporations.

This is the most visually promising story of the sweep and it is not being made
today, for two reasons. dedupe_check returns a LIKELY DUPLICATE against No.25
(the FERC and Alaska Energy Authority Bradley Lake docket, 16 days ago) on two
shared entities, and No.37 shipped a data centre deck yesterday. Running a
third data centre frame inside 48 hours is a variety failure whether or not the
dedupe gate technically clears.

The sourcing is also currently one Anchorage Daily News article. FERC eLibrary
requires JavaScript and returns nothing to a fetcher, no Federal Register notice
exists for the application yet, and the Maine Monitor page that carries the
deficiency letter language fails with a header overflow. A queued run has time
to solve that.

QUEUED via prompts/NEXT_RUN.md.

### 3. Considered and declined — the August 18th primary result (Beats A, D, F)

Jonathan Kreiss-Tomkins, running on a data centre moratorium, led a 17 candidate
field with about 21.7 percent, and Ballot Measure 1 passed with about 71 percent,
restoring a $2,000 individual contribution cap. His largest single donor gave
$100,000, fifty times the new cap.

Declined on two grounds. It is a compound of No.17 (the Anthropic employee
donations), No.21 (AS 15.13.070(b), APOC and Ballot Measure 1 before the vote)
and No.37 (data centre politics), so it would have to ship as an UPDATE on three
separate prior decks at once. And its sharpest edge, whether the new cap binds
before the November general, is exactly the fact the scouts could NOT verify:
Alaska Beacon says the measure takes effect after this year's elections, Bolts
says it takes effect immediately on approval, and the initiative text could not
be reached. A deck whose best line is an unresolved conflict is a deck that has
to lead with a hedge.

## Everything else the sweep verified, held for later runs

- AURORA-AI, a $725,000 DOE award to UAF's Alaska Center for Energy and Power
  aimed at more than 200 islanded rural microgrids, with Cordova Electric as the
  pilot. Already covered as No.20 and No.31.
- NOAA's first complete aerial survey of ice seals across their whole U.S.
  range, 58 flights, 39,663 kilometres, more than 1.5 million image sets, more
  than 26 terabytes, machine detection better than 90 percent in thermal frames.
  Flown April to June 2025, resurfaced during NOAA Technology Week August 17th
  to 21st, 2026. Strong future deck; the survey itself is out of window.
- UAF's five year federal renewal of its Arctic and Homeland Defense university
  affiliated research centre, announced August 19th, naming nuclear blast,
  volcanic and seismic detection and critical minerals.
- Nine of seventeen governor candidates answered an Alaska Beacon survey on AI
  use in official communications. The largest single bloc among them was unsure.
- Bristol Bay's drone plus computer vision escapement trial against nine ADF&G
  counting towers that have been hand-clicked since 1955.
- AFCEC-26-R-0006, the Air Force request for lease proposals for AI data centres
  at JBER, Eielson and Clear, archived July 14th, 2026 with no award posted. A
  different solicitation from the AFCEC-26-R-0009 Eielson lease in No.23. An
  award here is the highest value pending item on the power beat.
- The Alaska Court System's AVA probate chatbot, which slipped from three months
  to more than fifteen, had its 91 question evaluation cut to 16, and
  hallucinated a nonexistent Alaska law school. January 2026, unused, and nobody
  has written the follow up.

## Claims that did NOT survive and must not be printed

- "Anthropic gave $372,000 to a candidate for Alaska governor." The company gave
  nothing. Six employees gave personally, and Anthropic told Northern Journal the
  donations were personal and not company directed.
- The Alaska Landmine's claim that Tom Begich's largest donor invests in Terra
  Energy Center, and its 1.25 gigawatt figure for that plant. Single source,
  uncorroborated.
- A News-Miner op-ed's assertion that HB 47 became law in June 2026 criminalizing
  AI generated child sexual abuse material and deepfake harassment. If true it
  would contradict No.37's framing that Alaska has no deepfake law. Neither
  akleg.gov nor legiscan could be reached to check. Left unresolved and unused.
- The "doctored hat" image in the Wilson campaign coverage was reported as an
  "AI attack." Swapping text on a hat needs no generative model, so the framing
  outruns the evidence.
- Reddit was unreachable, so nothing in this run is sourced to r/alaska,
  r/anchorage or r/juneau, and no claim about forum sentiment may be made.
