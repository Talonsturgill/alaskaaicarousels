# SCOUT MERGE — 2026-09-11 — Carousel No. 56

Six scouts, all six returned, all six spent their 25 WebSearch calls exactly and
then worked by WebFetch. No beat came back empty. The search budget held.

## What each beat found, ranked inside the beat

### Beat A — Power and compute
1. **Southcentral enters the heating season about 3 Bcf below ideal storage,
   which Enstar characterises as roughly 18 days of winter demand, and the
   published emergency sequence curtails large commercial and industrial load
   before residential.** Homer News, September 10th. BlueCrest's Cosmopolitan
   gas slipped to Q1 2027; a Nikiski LNG import project is not before Q4 2029.
   Enstar is in emergency arbitration with HEX Operating and is negotiating
   gas-sharing arrangements with Matanuska Electric and Chugach Electric that
   would not be filed with the Regulatory Commission of Alaska. Regional
   context, Alaska Public Media September 9th: about 70 Bcf a year, about 70
   percent of regional electricity from gas, more than 150,000 Enstar customers
   supplied almost entirely by Hilcorp, gas about $11 per mcf against a
   Japan-Korea spot price of $24.
2. GVEA's all-in residential rate is 34.55 cents per kilowatt-hour effective
   September 2026, fuel component 18.049 cents after a 2.6 cent drop, against
   the five cents per kilowatt-hour the state has quoted to court data centres.
   Board voted 4 to 3 on August 25th to keep chasing a 60 MW, $80 million
   turbine.
3. NTIA opened a BEAD location true-up in Anchorage September 3rd, more than
   5,000 additional Alaska locations potentially eligible out of $21 billion.
4. AGDC will ask the Legislature for $2.5 million in 2027 for a program letting
   Alaskans invest in the pipeline directly.

### Beat B — Research and Indigenous AI
1. UAA stood up AI@UAA inside a new LIFT Center, announced twice on September
   10th by two different officials, with the second statewide AI symposium
   September 25th to 27th carrying a panel on Alaska Native languages and data
   sovereignty. The whole cited AI capacity portfolio is $780,000 of NSF money
   plus a $29,998.84 conference grant.
2. UAA's AI and Robotics Lab bought a 19-electrode dry EEG rig, announced
   September 9th.
3. ONR put $3 million into a fourth phase of UAF's ARCTIC program, September
   1st, total $33 million, running to 2031. No AI component claimed.
4. BACKGROUND, and the best scale anchor found all run: UAF's Chinook cluster
   holds 48 GPUs, 40 L40S and 8 H100, on a $910,418 NSF award. That is the
   documented academic AI compute of the entire state. Dated 2024.

### Beat C — AI in the field
1. Ryan Air took $4.1 million of Rural Health Transformation money for
   autonomous cargo drones and eVTOL aircraft serving Bethel and Dillingham.
2. NOAA published the Navy's Year 9 Arctic incidental harassment authorization
   September 10th, effective September 14th.
3. The Alaska Volcano Observatory lowered Kupreanof to UNASSIGNED on September
   8th and explicitly refused to go to GREEN for insufficient ground-based
   coverage.
4. A UAF study of ex-Typhoon Merbok found Kuskokwim Bay nearly doubles a surge
   over 140 miles while Bristol Bay damps it. The scout flags that it uses no
   AI or machine learning.

### Beat D — Policy and money
Did not return before selection. See DEAD ENDS below.

### Beat E — Robotics and national with Alaska teeth
1. The Rural Health Transformation technology slice, named line items: a
   statewide AI imaging network across 21 acute care hospitals at over $3.1
   million, the first robotic-assisted surgery in southern Southeast Alaska at
   $6.5 million, and $250,000 for the framework for drone pharmaceutical
   delivery across 94,000 square miles. Weekly Friday tranches now total $207
   million across 217 projects.
2. Three NSF AI awards totalling $4,787,612 started September 1st at UAA and
   UAF, the largest a reinforcement-learning bioprocess digital twin for
   recovering rare earths from coal mining waste.
3. The ONR Arctic authorization with its hardware named from the proposed rule,
   two drifting ice gateway buoys, up to six 900 Hz moorings, up to 20 Argo
   floats, one REMUS 600 not on this cruise, across 639,237 square kilometres.
4. TSA opened closed roundtables on securing beyond-visual-line-of-sight drone
   flight, sign-ups close October 19th. The scout says honestly that the notice
   names no Alaska entity and this does not clear its own beat's bar.

### Beat F — Community signal
1. All three attending candidates for governor went on the record about data
   centres at a Last Frontier Republican Club forum on September 8th, splitting
   two ways, and Must Read Alaska's recap of the same event omitted the
   exchange entirely.
2. Fairbanks letters pages now carry the data centre argument as a subordinate
   clause inside October 6th election endorsements.
3. An Alaska Watchman column argues the anti-data-centre comment flood is a
   foreign bot operation. Flagged by the scout as an assertion, not a fact.
4. A four-week salience calendar of Alaska AI proceedings, September 13th to
   October 20th.

## The dedupe screen, run before any directors room

Five candidates were tested with `scripts/dedupe_check.py`. The 30-day window
is the binding editorial constraint at daily cadence and it did most of the
selecting this run.

| candidate | verdict | strongest match |
|---|---|---|
| GVEA rate math and the turbine vote | LIKELY DUPLICATE | No.47, 2026-09-01, 3 shared entities, jaccard 0.079 |
| Gubernatorial forum data centre split | LIKELY DUPLICATE | No.51, 2026-09-05, 4 shared entities, jaccard 0.103 |
| UAA AI capacity and the 48 GPUs | LIKELY DUPLICATE | No.41, 2026-08-26, 2 shared entities, jaccard 0.038 |
| ONR Arctic acoustic navigation grid | LIKELY DUPLICATE x2 | No.44, 2026-08-29, 3 shared entities, jaccard 0.078 |
| **Southcentral gas and the order of cuts** | **soft overlaps only** | No.42, 2026-08-27, 1 shared entity, jaccard 0.025 |

Every LIKELY DUPLICATE entry was read in full before the call, as the gate
requires. Three of the four are real lane collisions rather than story
collisions, and the lane is the problem: No.47's own ledger note recorded that
it was the third data-centre siting deck in fourteen days and told the next run
to change beat or acknowledge its predecessors. The governor's race was the
setting of No.51 six days ago. Arctic underwater acoustics under a NOAA
authorization was No.44 thirteen days ago.

## DEAD ENDS worth carrying forward

- **Beat D did not return.** Policy and money produced nothing for this merge.
  Its ground was substantially covered from the other side by Beats A and E,
  both of which worked the Federal Register API and the NSF award API directly,
  so the run is not blind here, but the beat is a gap and the retro should say
  so.
- The Rural Health Transformation Program is now BURNED TWICE inside the window
  (No.36 on August 16th, No.45 on August 30th), which killed the single richest
  find of the day. Beat E's $207 million across 217 projects is an increment on
  No.45's 185 projects and $181,871,366, not a new story.
- `health.alaska.gov`'s own award spreadsheet could not be parsed by any scout,
  so the named hospital behind the 21-hospital AI imaging network is still
  unknown. A session with a shell can unzip it. Worth queueing.
- `defense.gov/News/Contracts` is 403, which is a real hole three weeks before
  the federal fiscal year ends.
- `cbc.ca` is 403, and it is the one outlet carrying Yukon First Nation and
  Alaska Native reaction to the STAK lease. NEW dead route.
- `newsminer.com` rate-limits at about three rapid fetches, returning 429.
- The Federal Register API treats a multi-word `conditions[term]` as a phrase,
  so "Alaska artificial intelligence" returns zero while "Alaska" returns
  everything. Two scouts hit this independently. Query single terms and scan.
- The FNSB CivicClerk API returns FUTURE events only unless an OData date
  filter is supplied. Both facts are worth writing into sources.yaml.
