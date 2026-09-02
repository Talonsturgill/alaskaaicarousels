# SCOUT MERGE — 2026-09-01 — Carousel No. 47

Six scouts, window 2026-08-22 to 2026-09-01. Searches used, by beat: A 25, B 23,
C 25, D 27, E 25, F 22. Every beat reported hitting or nearly hitting its cap.

## THE CONVERGENCE

Two beats found the same story independently, from opposite ends. Beat D came at
it through federal procurement and Beat F came at it through community signal,
and neither knew the other was looking.

**The Fairbanks North Star Borough Assembly adopted its 2027 legislative
priorities on August 27th. Twenty five items. Exactly one of them appears on both
the state list and the federal list, and it is a request for a moratorium on
permitting, leasing or construction of new commercial data centers.**

The trigger, per KUAC and the News-Miner, is the Air Force's request for lease
proposals covering roughly 4,700 acres across Joint Base Elmendorf-Richardson,
Eielson Air Force Base and Clear Space Force Station, twelve parcels in all, for
AI data center development. Eielson sits inside the Fairbanks North Star Borough.

And the resolution as written extends the requested moratorium only to
"state-owned and municipal lands." Presiding Officer Scott Crass told KUAC by
phone that federal lands were intended as well.

Sponsor, Assemblymember Garret Armstrong, who moved it onto the state list on
August 6th. A successful amendment then replicated it onto the federal list.
Salcha resident Sarah Hollister testified for it. Mayor Grier Hopkins told
Alaska's News Source the borough heard the community "loud and clear."

## FULL CANDIDATE SLATE, ranked as the showrunner reads them

### 1. FNSB moratorium (Beats D and F) — SELECTED, see selection.md
New, in window, Interior Alaska, which is geographically distinct from the last
month of Mat-Su, Kenai and Anchorage coverage. Clean dedupe, soft overlaps only.
Real internal tension between what the text reaches and what started it. Numbers
that encode: 25 items, 1 duplicated, 4,700 acres, 12 parcels, 3 installations,
2 governments asked, 0 of the trigger parcels covered by the text.

### 2. Anthropic employee donations in the governor's race (Beat D) — RECUSED
Strongest single finding of the sweep by pure news value. Six Anthropic employees
gave $372,000 to Jonathan Kreiss-Tomkins between February and May, $521,812 in
AI-linked money against a $1.85 million haul, while his platform proposes a data
center moratorium. Not covered, deliberately. See selection.md.

### 3. AIDEA and the 19,950 acres near Houston (Beats A and F) — held
DNR extended written comment to September 14th and its own August 24th meeting
notice now says more than 2,000 written comments have arrived. Four Mat-Su city
councils declined to endorse the transfer. This is live and important, and it is
already carried on the public docket, which was refreshed this run. Held because
No.44 on August 19th covered Houston and Mat-Su opinion on data centers and this
is the same geography inside 30 days.

### 4. AURORA-AI at UAF and Cordova (Beats B and C) — KILLED BY DEDUPE
$725,000 DOE Genesis Mission award, $325,000 to UAF, Phase One starting October
1st, about $7 million sought for Phase Two, modular data centers of about 100
kilowatts. Two scouts ranked it first. `dedupe_check` returned LIKELY DUPLICATE
against No.31 on 2026-08-12, jaccard 0.169, eight shared entities. No.31 was
itself an explicit UPDATE to No.20 on 2026-07-30. That is two decks on AURORA-AI
inside the 30 day window, and No.31 already printed the amount, the mechanism,
the partners and Cordova's 170 kilowatts of computing beside the generators. The
new material here is a start date, a Phase Two ask and a refrigerator-sized box.
A third deck on it would be a reframe with no material development.

### 5. RCA denies Enstar reconsideration on $240 million Kenai Loop storage (Beat A)
3 to 2, decided August 21st, posted August 24th, with the written reasoning not
yet issued. Single-sourced to Petroleum News because rca.alaska.gov answers a bot
with 403. Held for two reasons, the sourcing and the absence of any AI content.

### 6. Chugach Canyon Creek preliminary permit (Beat A)
Federal Register, August 26th, project No. 15422, 6.3 megawatts, 14,100 megawatt
hours a year, comments due October 20th. A clean primary document in window. Held
because it is a hydro filing with no AI nexus of its own.

### 7. Rural Health Transformation technology breakdown (Beat E)
$3.1 million for AI imaging at 21 acute care hospitals, $6.5 million for robotic
surgery in southern Southeast, $250,000 to design a drone prescription framework
over about 94,000 square miles. Held. The program shipped twice already, on
August 16th and August 30th, and Beat E could not read the CMS primary because
cms.gov refused every fetch.

### 8. Loudoun County fiscal comparison op-ed (Beats A, D and F)
$1.3 billion of FY2027 data center tax revenue in one Virginia county against
Alaska's $1.9 billion of unrestricted FY2027 oil revenue. An opinion column, not
a development. Useful as the counter-argument inside another deck, not as one.

## DEAD ENDS WORTH NOT REDISCOVERING

Hosts that refused an automated fetch this run, several of them not yet in
`config/sources.yaml`'s `refuses_automated_fetch` block:

- `cms.gov` 403 on every attempt, twice, from Beat E. **Not currently in the
  block. Add it.**
- `govtribe.com` 403, which is the route to whether the JBER, Eielson and Clear
  land lease RFLP has been awarded. **Not currently in the block. Add it.**
- `newsminer.com` HTTP 429 on two attempts from Beat E, though Beat D read a
  News-Miner article successfully, so this is rate limiting rather than a wall.
- `federalregister.gov` redirects to `unblock.federalregister.gov`. The documented
  routes around it both worked, `govinfo.gov/content/pkg/FR-<date>/html/<id>.htm`
  and `federalregister.gov/api/v1/documents/<id>.json`.
- `akleg.gov`, `aws.state.ak.us` and `rca.alaska.gov` 403 to WebFetch for the
  scouts, all three already documented. Note that the SHOWRUNNER fetched
  `aws.state.ak.us` notices 224930 and 224684 successfully in Phase 3.5 this same
  run, so that one is intermittent rather than a wall.
- `sam.gov` is a JavaScript single page app and WebFetch reads only the shell.
- `alaskabeacon.com` 403, worked around through republications as documented.
- `tandfonline.com` 403, worked around through the PMC mirror.
- Facebook group content truncates on fetch and cannot be corroborated.

**Reddit was not attempted by any scout**, per the standing finding. Beat F used
Hacker News through the Algolia API instead and reports it EMPTY for Alaska in
this window, which three separate beats confirmed independently. That is now four
consecutive runs with the same result. The reachable community signal this run
came entirely from public meeting testimony and local radio, which is route 3 of
the beat's own list and the highest quality one it has.

## WHAT THE SWEEP SAYS ABOUT THE BEAT RIGHT NOW

Beat F put it best and the other five corroborate it. Alaska's live argument
about AI is not about whether the technology works. It is about permission and
pace, and about who gets to say yes. In one ten day window the Anchorage Assembly
funded $598,998.10 of crime center hardware while hearing an ordinance that would
require its own sign-off before the police buy AI tracking software, four Mat-Su
city councils declined to endorse a 19,950 acre state land transfer, and the
Fairbanks North Star Borough asked two governments at once to stop issuing
permits. Nobody quoted on the record in any minuted setting this window argued
that AI is bad. Every one of them argued about who decides.
