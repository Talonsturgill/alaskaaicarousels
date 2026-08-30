# SELECTION — 2026-08-30 — Carousel No. 45

## THE STORY

**Alaska's $181.9 million rural health award list is public and unreadable. Opened, it
shows that eight of 185 awards, about $12 million, buy a machine that reads, decides or
flies. Here is who got them.**

On August 25th, 2026 CMS announced $160 million across 142 Alaska projects under the Rural
Health Transformation Program, and named three technology headliners. The Alaska Department
of Health publishes the underlying record itself, weekly, as a Notice of Intent to Award
spreadsheet. On August 28th that file reached 185 awards worth $181,871,366.

Parsed, it names the awardees nobody has published:

- **$6,518,029, PeaceHealth Ketchikan Medical Center**, the first robotic assisted
  minimally invasive surgery in Southern Southeast Alaska, serving Ketchikan Gateway,
  Petersburg, Prince of Wales-Hyder and Wrangell.
- **$3,156,626, Alaska Stroke Coalition**, a statewide AI imaging network across 21 acute
  care hospitals, running on existing PACS with no new imaging hardware.
- **$430,000, Maniilaq Association**, AI clinical documentation for behavioral health
  across the North Slope and Northwest Arctic boroughs, aimed at a documentation burden the
  award text names as a driver of therapist turnover.
- **$250,000, Tanana Chiefs Conference**, a planning year for drone pharmaceutical delivery
  from the Fairbanks hub to 42 Interior villages across 94,000 square miles, where winter
  medication delays of 5 to 14 days are common, partnered with UAF's ACUASI on FAA beyond
  visual line of sight waivers.
- **$250,000, Mat-Su Regional Medical Center**, an AI assisted eight lead EEG headband to
  identify status epilepticus locally and avoid a transfer into Anchorage.
- **$141,703, Statewide Independent Living Council**, an AI assistive technology needs
  assessment tool.
- **$25,492, Kodiak Community Health Center**, AI supported clinical documentation.
- **$1,241,086, MAPHABIT INC**, the ANCHOR aging and neurodivergent remote support project.

Eight awards. $12,012,936 of $181,871,366. About one dollar in fifteen.

## WHY THIS ONE

1. **Concrete Alaska impact.** Every one of these lands somewhere nameable. A robot in
   Ketchikan serving four boroughs and census areas that currently fly patients out. A
   stroke read arriving at 21 hospitals at the same speed whether the hospital has a night
   radiologist or not. A drone framework for 42 villages where a prescription can take two
   weeks in winter.
2. **Visual potential.** The ratio is the picture. 185 cells, 8 filled. $181.9 million
   against $12.0 million. Four Friday rounds as a staircase, with a round still to come.
   And real geography, Southeast, the Interior, the Northwest Arctic, Kodiak, Mat-Su.
3. **Tangibility.** Named organisations, exact dollars to the cent, dated notification
   Fridays, and service areas listed borough by borough.
4. **Would an Alaskan send this to a coworker?** Yes, and to their hospital administrator.
   Nobody else has published the itemised list.

## THE EDGE

Three of six scouts independently reached this story, and all three hit the same wall. Beat
E wrote "the specific awardee behind the $6.5M Southern Southeast robotic surgery line is
unnamed in these findings, do not guess the hospital." Beat C wrote that the file "downloads
but is binary and I have no spreadsheet or shell tool." Beat D reached the same PDF summary
and stopped at the totals.

The file is a normal spreadsheet. It was downloaded from the state's own URL and parsed, and
the parse is committed as `rhtp_awards.csv` and `rhtp_parsed.json` so any reader can repeat
it. The deck's factual edge is that it read a public document to the end.

## DEDUPE GATE

`dedupe_check.py` returned ONE likely duplicate, **No.35, 2026-08-16, 14 days ago, "The
Menu and the First Friday"**, 2 shared entities, jaccard 0.057. Read in full, as required.

No.35's topic was Alaska's Rural Health Transformation Program, **the first Friday of
awards on August 7th, 2026, $4,500,000 across nineteen projects** out of the $272,174,856
first-year allocation, against a state program page listing drones, kiosks and AI-enabled
tools as eligible uses. Its angle was "a menu and an order are two different documents",
and its own recorded note says the briefed headline was killed by the fact-checker because
**"the state publishes the nineteen-project list only as an unparseable spreadsheet"**, so
fourteen of nineteen awards went unitemised and the deck said so at full weight.

**This run ships as an EXPLICIT UPDATE, and the update is precisely the thing No.35 could
not do.** The material new developments, all inside the window:

- Three further Friday rounds, August 14th at $30,125,610 across 37 projects, August 21st
  at $130,291,439 across 105, and August 28th at $16,862,504 across 24. The program went
  from $4.5 million to $181.9 million in three weeks.
- The CMS announcement of August 25th, 2026, which is what put the technology line items on
  the public record at all.
- The spreadsheet parsed, which itemises all 185 awards rather than five of nineteen, and
  names every awardee.

The cover carries the UPDATE on the frame, not only in the record, per the standard No.31
set. No.35 asked what the menu actually bought. This deck answers it.

Also checked and cleared or rejected:

- **AURORA-AI (UAF, Cordova, DOE Genesis Mission).** REJECTED as a hard duplicate. No.31,
  2026-08-12, 18 days ago, jaccard 0.168, 7 shared entities, and No.31 was itself already an
  explicit update to No.20. Three scouts surfaced it; the ledger settles it.
- **The AIDEA Houston 19,950 acre conveyance.** REJECTED. No.27, 2026-08-06, 24 days ago,
  carried the same acreage and the same AIDEA and DNR entities. The September 14th deadline
  is real and stays tracked on the docket, which is the right surface for it.
- **Cook Inlet gas, ENSTAR 18 days short.** REJECTED for this deck. Strong material, and the
  entity overlap with No.27 is high at jaccard 0.104 with six shared entities. No.31's own
  ledger note also warns that a gas contract with no AI content is a national story with an
  Alaska sticker, and the AI link here is an inference the deck would have to supply.
- **FAA BEYOND Phase 2.** Held. Genuinely fresh and it has a September 10th deadline, but
  it survives better as a supporting fact inside this deck, because the Tanana Chiefs award
  names ACUASI and BVLOS waivers directly.
- **Alaska's share of the Meta settlement.** REJECTED. National story with an Alaska share,
  the exact pattern the ledger has rejected before.

## RUNNER-UP

**Infrared drones on the Mukluk fireline at Tok, and a fire season extended to September
14th** (Beat C). Primary sourced throughout to akfireinfo.com, in window, genuinely
operational, and visually strong. Held back only because the machine-learning content is
thin, the drones carry infrared cameras rather than autonomy, and this deck has run three
sensing stories in the last five days. Worth queueing.

## VARIETY AND DIALS

Forbidden hero structures, atmospheres, continuity devices, hook archetypes, palette
families and type pairings are listed in plan.md and are all avoided by the treatment brief.
Dials for this run are design_variance 5, visual_density 2, type_temperature 3.
