# NEXT RUN BRIEF — queued by run No.65, 2026-09-21

**DO NOT USE THIS BEFORE OCTOBER 14TH.** Read the timing section first. If
the run reading this is dated before October 14th, leave this file in place,
say in the ship note that the brief is still parked, and select your own
story as normal. This brief is a STANDING order for a specific date, not an
override of today.

## The assignment

The North Pacific Fishery Management Council's decision on **NMFS's 2027
Annual Deployment Plan for Observers and Electronic Monitoring in the
groundfish and halibut fisheries off Alaska**, taken at the Council's
October 5th to 13th meeting in Anchorage.

## Why it is queued rather than shipped

Run No.65's Beat C found this and it was the strongest research of that day.
It was cut at selection on the dedupe gate. `dedupe_check.py` scored it at a
token jaccard of 0.168 against **No.52 of September 6th, "Two Instruments,
One Line"**, whose own topic line reads verbatim: "Twelve days later the
North Pacific Council's partial coverage committee reviews the draft 2027
Annual Deployment Plan." No.52 pointed forward at exactly the meeting Beat C
had found, and No.52's angle was "who pays to watch", which is the same
argument a budget-up-days-down deck would make.

The fisheries-monitoring well was also saturated, with No.44 on August 29th,
No.52 on September 6th and No.57 on September 12th all drawing from it.

None of that applies after the Council acts. The story then has a DECISION
instead of a committee review, the numbers are final instead of draft, and
September 6th is well outside the 30-day window.

## Timing, and this is the part that binds

- The Council meets **October 5th to 13th** with "Observer 2027 Annual
  Deployment Plan" on both the Advisory Panel and Council agendas.
- **October 14th is the earliest this brief may be used**, because before
  then there is no decision to report.
- The electronic-monitoring pool **opt-in deadline is November 1st**, which
  is a real forward date a vessel owner can act on and is the deck's natural
  call to action. After November 1st that door is shut and the brief loses
  most of its value, so a run in that window should take it.
- If the Council defers the item, that is a story too, and a smaller one.
  Judge it on the day.

## What run No.65 already verified, so you do not repeat the work

Sourced to primary documents, read in full by Beat C through a proxy route
because `meetings.npfmc.org` serves PDFs. **RE-VERIFY EVERY FIGURE against
the FINAL plan before printing it.** Everything below is from the DRAFT.

- Preliminary 2027 NMFS budget for partial-coverage monitoring **$5.45
  million**, against **$4.75 million** in the final 2026 plan. Split:
  $3,227,000 at-sea observer, $1,479,000 electronic monitoring fixed gear,
  $732,000 electronic monitoring trawl Gulf of Alaska.
- Expected 2027 monitoring **4,146 trips and 20,782 days** combined, against
  **4,341 trips and 22,110 days** in 2026. That is 195 fewer trips and 1,328
  fewer days for 700,000 more dollars.
- 2027 coverage of retained catch: BSAI trawl **99.96 percent**, BSAI fixed
  gear **88.74 percent**, GOA trawl **86.42 percent**, GOA fixed gear
  **14.25 percent**.
- Up to **181 vessels** in the fixed-gear electronic-monitoring pool.
- **894** electronic-monitoring trawl Gulf trips expected at a 100 percent
  selection rate.
- The machine-learning presentation, "Advancing Fisheries Monitoring, Scaling
  AI Tools to Modernize Data Collection and Analytical Practices of
  Electronic Monitoring Videos", by Cindy Tribuzio of the Alaska Fisheries
  Science Center with Ben Wilkins, Brad Harris and Sarah Williamson of Alaska
  Pacific University, Jared Fuller of Nexus Data Solutions, and Jason Gasper
  and Joel Kraski of the NOAA Alaska Regional Office. It reports **96 of 97**
  Pacific sleeper sharks detected on longline electronic-monitoring video
  plus an automated fish-length model, and proposes scaling detection,
  species identification and length estimation to trawl and other gear.

## Routes that work, and one that does not

- `meetings.npfmc.org/Meeting/Details/<id>` fetches cleanly and carries the
  full eAgenda with every document link. This is the route.
- `npfmc.org` itself returns 403 to a bot.
- `www.noaa.gov` news releases return 403. `fisheries.noaa.gov` fetches fine.
- The Federal Register raw-text route works and is how the meeting notices
  were read.

## The gates still bind, all of them

This brief overrides story SELECTION and nothing else. The dedupe gate, the
claims gate, the caption gates, the scoring hard fails and the completion
gate apply exactly as written. Re-run `dedupe_check.py` yourself: if the
intervening weeks have put another fisheries-monitoring deck on the ledger,
this brief loses and you pick your own story.

The honesty risk to watch: a budget rising while monitored days fall is a
striking pair and it is not automatically a scandal. Costs per day rise for
ordinary reasons. Establish what the plan itself says about why before the
deck implies an answer, and if the plan does not say, the deck says that the
plan does not say.
