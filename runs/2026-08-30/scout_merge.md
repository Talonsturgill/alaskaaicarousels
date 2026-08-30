# SCOUT MERGE — 2026-08-30 — Carousel No. 45

Six scouts, one per beat, each capped at 25 WebSearch calls. All six returned. Total search
spend 149 of the session's ~200, leaving headroom for the claims gate and the Phase 12 scan,
which is what the cap exists to protect.

## THE CONVERGENCE

Three scouts working different beats independently surfaced the same story, and all three
hit the same wall.

- **Beat C** ranked Alaska's Rural Health Transformation technology awards first, and wrote
  that the state's full award list "downloads but is binary and I have no spreadsheet or
  shell tool in this agent, so I could not enumerate which awardee holds the 21-hospital AI
  imaging contract or the drone-delivery planning award."
- **Beat E** ranked it first and wrote "the specific awardee behind the $6.5M Southern
  Southeast robotic surgery line is unnamed in these findings. Do not guess the hospital."
- **Beat D** ranked it second, reached the same summary PDF, and stopped at the totals.

Convergence across three independent beats is the strongest salience signal this run
produced. The shared wall is the story's opening.

## WHAT THE SHOWRUNNER DID WITH IT

Downloaded `ak_rhtp_awardsnotice_2026.xlsx` from the state's own URL (HTTP 200, 72,209
bytes) and parsed it. One sheet, "Notice of Intent to Award", 185 award rows,
$181,871,366.36. Eight awards totalling $12,012,936 name a machine that reads, decides or
flies, which is 6.61 percent, about one dollar in fifteen. The parse is committed as
`rhtp_awards.csv` and `rhtp_parsed.json` so a reader can repeat it.

It also surfaced something the state's own summary cannot see. One row carries the
initiative spelled "Spark Technology & Innovation" with an ampersand rather than the word,
so it sits outside the state's own Spark tally. The fact-checker is checking whether the
published summary counts 36 or 37, because only then is the consequence assertable.

## BY BEAT

**A, Power and compute.** ENSTAR president John Sims told a joint House and Senate Resources
hearing on August 20th the utility is 18 days short of gas for the coming winter at normal
temperatures, and the emergency curtailment order cuts gas to power generation before gas to
homes. DNR issued BlueCrest a Notice of Required Immediate Action on August 21st over the
undeveloped Tyonek resource. Strong material, high entity overlap with No.27, see
selection.md.

**B, Research and Indigenous AI.** AURORA-AI at UAF and Cordova, a hard duplicate of No.31.
Also $6.56 million of AI-titled NSF awards to UA campuses in six weeks, adjacent to No.41.
The University of Alaska holds its first statewide AI symposium September 25th to 27th with
a session on Alaska Native language sovereignty. A 2026 paper records that no policy
governing AI use in the Alaska Tribal Health System has been formally implemented, which is
worth queueing.

**C, AI in the field.** The RHTP awards, first. Then infrared drones on the Mukluk fireline
at Tok on August 22nd, with fire season extended to September 14th in three protection
areas. This run's runner-up.

**D, Policy and money.** The AIDEA Houston conveyance comment window extended to 5:00 p.m.
September 14th with more than 2,000 comments already filed. Duplicate of No.27 for deck
purposes, and it is tracked on the docket, which is the right surface.

**E, Robotics and national with Alaska teeth.** The RHTP awards, first. Then FAA BEYOND
Phase 2, announced August 27th and 28th, doubling the program's lead participants with
proposals due September 10th. UAF is one of the eight incumbents, which connects directly to
the Tanana Chiefs drone award naming ACUASI and BVLOS waivers.

**F, Community signal.** No community argument attached to the RHTP awards, which is itself
the finding. Hacker News is genuinely dry on Alaska AI rather than broken, having followed
New York's data centre moratorium hard and said nothing about Alaska's. ADN ran 23 letters in
the window and not one touches AI, data centres, surveillance or electricity. The argument
Alaskans are actually having is about data centres and surveillance, and this deck has run
that argument four times in two weeks.

## ROUTES CONFIRMED, AND TWO CORRECTIONS TO sources.yaml

Two scouts independently contradicted the standing `refuses_automated_fetch` record and
should be believed, since each pulled full article text:

- **newsminer.com fetches at the ARTICLE level.** Beat F pulled a signed August 27th letter
  and a June 11th news story verbatim. The section index rate limits with a 429, which is
  probably what produced the original record.
- **muni.org fetches at the PAGE level.** Both Beat A and Beat F pulled real content,
  including the Assembly worksession item AM 524-2026. Only the search and notice index
  paths fail.

Newly confirmed and worth promoting: the NSF award API (`api.nsf.gov`, keyless, full
abstracts and exact dollars), the Federal Register JSON API and its raw text endpoint (the
HTML pages now 302 to a block host), `health.alaska.gov` for the weekly award PDF and the
spreadsheet, `akfireinfo.com`, `highergov.com` as the working sam.gov mirror, and
`aws.state.ak.us/OnlinePublicNotices` browsed from the front page rather than searched.

Confirmed dead: reddit.com entirely, cms.gov 403, transportation.gov 403, law.alaska.gov
403, thecentersquare.com behind a 402 paywall host, alaskabeacon.com 403 with the
alaskapublic.org republication as the route around it.
