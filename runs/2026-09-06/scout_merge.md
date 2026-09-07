# SCOUT MERGE — 2026-09-06 — six beats, 24 stories

Six scouts returned. Search budget spent: A 24, B 22, C 25, D 23, E 25, F 25. Roughly 144 of 200,
which leaves the rest of the run its margin.

## The shortlist the showrunner actually weighed

**1. NOAA writes the rulebook for putting machines into Alaska's fisheries surveys (Beat C).**
September 3rd, 2026 NOAA Fisheries feature announcing a 23-author framework led by the Alaska
Fisheries Science Center's Stan Kotwicki, published in ICES Journal of Marine Science. 14 of 23
authors are AFSC. Saildrones ran acoustic-only Bering Sea pollock surveys when COVID grounded the
ships; stereo drop cameras survey untrawlable rockfish habitat; near-infrared machine ageing reads a
pollock otolith in 30 to 50 seconds against a human at a microscope. The framework's argument is
incremental transition under calibration, not replacement.

**2. The camera-or-observer decision for Alaska's 2027 fishing year, September 15th (Beat C).**
Federal Register notice 2026-17762, published August 31st, sets the North Pacific Fishery Management
Council's Partial Coverage Fishery Monitoring Advisory Committee to meet September 15th, 8:30 a.m. to
4 p.m. Alaska time, to review the draft 2027 Annual Deployment Plan for Observers and Electronic
Monitoring. That plan sorts the partial-coverage fleet into three pools, No Selection, EM Trip
Selection and Observer Trip Selection.

**3. Alaska Native corporation 8(a) contracts are where the AI money with an Alaska name on it
actually is (Beat D).** FPDS-NG ATOM feed, keyless and primary. Koniag Emerging Technologies holds
W519TC26CA019, "Artificial Intelligence (AI) Rapid Support (AIRS)" for the Army CDAO, $5,267,244.80,
place of performance Anchorage, ultimate completion May 25th, 2031. A cluster of Koniag subsidiary
obligations lands August 27th to September 4th against the September 30th lapse.

**4. FERC accepts the Cook Inlet subsea-compute permit, P-15423-000, comments close November 2nd
(Beats D and E).** 330 to 350 marine hydrokinetic turbines, 66 subsea compute hives, 100 MW, a
3.5-mile 115 kV hybrid cable into the Nikiski Industrial Corridor.

**5. DOE Genesis Mission, one Alaska row out of 637 (Beat D).** AURORA-AI at UAF, $725,000, Phase One
starts October 1st, Cordova Electric as the live test system, roughly 100 kW modular data centers
folded into village microgrids.

**6. Deep learning doubles the permafrost damage estimate to $261 billion (Beat C).** UConn-led, in
Earth's Future September 3rd, by finally measuring how TALL Arctic buildings are.

**7. Anchorage funds the crime center 8 to 4 and postpones its rules to September 15th (Beats E, F).**

**8. UA's statewide AI symposium, September 25th to 27th, whose Friday panel reads "Rural connectivity
and compute, Alaska Native language and data sovereignty, and why locally controlled models matter"
(Beats B, F).** Behind it, the Alaska Tribal Health System's own baseline survey: 35 percent had never
heard of AI, 12 percent had used it, 48 percent doubted it would improve outcomes.

## What the sweep KILLED, and why that matters

Beat C killed the NSF award batch outright by reading `ledger/topics.json` itself: the AI critical
minerals awards and the explainable-AI bathymetry award all shipped in No.41 on August 26th. Beat D
independently confirmed it. That is the dedupe gate working two beats upstream of where it lives.

Beats A, B, D, E and F all reported Hacker News empty for Alaska, and all five spent one query or
none, which is the sources.yaml rule doing its job. Reddit was attempted by nobody.

## Route intelligence worth keeping (folded into the ship note for sources.yaml)

- **FPDS-NG public ATOM feed is the working SAM.gov substitute** and is primary. Field syntax that
  works, space-joined: `POP_STATE_NAME`, `VENDOR_ADDRESS_STATE_NAME`, `DESCRIPTION_OF_REQUIREMENT`,
  `PIID`, `SIGNED_DATE:[YYYY/MM/DD,YYYY/MM/DD]`. It paginates, so no total may be inferred from one pull.
- **`r.jina.ai/<pdf-url>` renders agency PDFs to text**, which WebFetch cannot do. This is the missing
  route for most primary documents on the policy beat.
- **`aws.state.ak.us/OnlinePublicNotices/Notices/Search.aspx`** returns roughly eleven days of every
  state notice in one fetchable page and is also the partial route around rca.alaska.gov's 403.
- **`api.nsf.gov/services/v1/awards/<ID>.json`**, the per-award endpoint, returns the full abstract.
- **northernjournal.com now redirects to anchoragepress.com.** sources.yaml still points at the old host.
- **akleg.gov 403s** with no route found, and **law.alaska.gov/press/releases 403s**. Both are new.
- **agupubs.onlinelibrary.wiley.com 403s.** New.
- **ARCUS appears to have sunset**, last post September 30th, 2025. **ACUASI's news page is stale since
  January 2024.** Both are listed sources that no longer produce.

## Dead ends the run should not re-walk

Reddit (measured dead twice). Hacker News for any Alaska beat. sam.gov, govtribe, defense.gov/Contracts,
rca.alaska.gov article pages, alaskabeacon.com direct, fcc.gov/document, ntia.gov (503 today),
harvestmidstream.com, mea.coop/news, acuasi.alaska.edu/news, aoos.org (nothing since June),
adfg.alaska.gov (nothing since August 14th).
