# SCOUT MERGE — run 2026-08-28, Carousel No. 43

Six beats, 150 WebSearch calls spent (25 each, the cap held). ~40 searches
remain for later phases, which is what the cap exists to protect.

## THE CONVERGENCE

Beats B and C, working independently on different briefs, both returned the
same story as their strongest finding: **the Permafrost Discovery Gateway's
near-real-time Arctic lake drainage tracker, and the roughly 30 lakes it
flagged in northwestern Alaska in June and July 2026.** Beat C supplied the
detail Beat B did not have, that the near-real-time tracker itself launched on
August 13th, 2026, and that the Alaska Beacon republished the authors' account
on August 27th. Two scouts arriving at one story from different directions is
the strongest signal this process produces.

## CANDIDATE 1 (SELECTED) — the lakes that drained while the winter was cold

Anna Liljedahl (UAF affiliated professor, Woodwell Climate) and Ingmar Nitze
(Alfred Wegener Institute) published a first-person account on August 26th,
2026 of a machine learning pipeline that reads aerial photography going back to
the late 1940s against modern satellite imagery to detect Arctic lake drainage
as the surface signature of ice-rich permafrost giving way.

- ~30 lakes affected by drainage in northwestern Alaska, June to July 2026,
  despite a cold 2025-26 winter
- ~4,600 lakes in the Seward and Baldwin peninsulas study region
- ~200 of those lost more than 25 percent of their area in summer 2018 alone
- 4,000,000+ Arctic lakes mapped and actively monitored
- 70,000,000 thermokarst ponds across the Alaska tundra
- imagery record starts in the late 1940s; satellite from the 1970s
- Arctic warming 2 to 3 times the global average
- ~80 percent of Alaska land underlain by permafrost, 140+ Arctic communities
  built on it
- near-real-time drainage tracker launched on the Gateway August 13th, 2026

Sources: The Conversation (authored BY the researchers, so primary),
Alaska Beacon republication, Phys.org, Woodwell Climate project page, NCEAS.

DEDUPE: clean. `dedupe_check` returns soft overlaps only, strongest No.41
(2026-08-26) at jaccard 0.017 on the single shared entity UAF. No permafrost,
thermokarst, lake or Arctic-observation story anywhere in the 30-day window.

## CANDIDATE 2 (RUNNER-UP) — the rural health order, itemised at last

CMS announced $160 million across 142 Alaska projects on August 25th, 2026
under the Rural Health Transformation Program, and this time the line items are
machines: $6.5M for robotic-assisted surgery in southern Southeast Alaska for
the first time, $3.1M+ for AI imaging at 21 acute-care hospitals, $250,000 to
build the framework for drone pharmaceutical delivery across ~94,000 square
miles where winter medication runs take 5 to 14 days.

DEDUPE: LIKELY DUPLICATE against No.35 (2026-08-16, 12 days), jaccard 0.102,
three shared entities. No.35's whole angle was that the state published a MENU
of what the money may buy and the first order bought X-ray machines, with
fourteen of nineteen awards unitemised. This announcement is the answer to that
deck's open question, which makes it a legitimate and even elegant UPDATE, but
an UPDATE all the same, and a genuinely distinct story exists.

## RULED OUT, with reasons

**Canyon Creek (Beat A).** FERC accepted Chugach Electric's preliminary permit
for a 6.3 MW Kaplan turbine on Canyon Creek on August 26th, comments close
October 20th. Excellent material, and the contrast against gigawatt AI pitches
is real. It is also the same deck as No.25 (2026-08-04, 24 days ago), which was
a FERC hydro comment window on the Kenai Peninsula sized against AI data centre
demand that names no megawatts. `dedupe_check` returned it as a LIKELY
DUPLICATE at jaccard 0.047 sharing FERC, Kenai Peninsula, Railbelt, capacity,
generation and hydroelectric. Beat D also read the FERC notice in full and
confirms it makes no mention of data centres, AI or load growth, so the AI hook
would be entirely ours to assert. Two independent reasons to pass.

**AURORA-AI (Beats B, C and D all returned it).** No.20 on 2026-07-30 was
literally "278 federal AI projects. Alaska has one," and that one row was
AURORA-AI. 29 days, inside the window. The new material is real (Phase One
starts October 1st, $325K of $725K to UAF, Phase Two needs ~$7M, Cordova's
river-cooled modular data centre) but it is an UPDATE and the candidate above
is not. NOTE FOR A LATER RUN, flagged by Beat E: UAF's own release says
$725,000 total and Alaska's News Source on August 28th says $325,000. Those are
reconcilable as total-versus-UAF-share, but nobody should ship either figure
without reading both again.

**The governor's race AI money (Beat F).** Alaska's August 18th top-four
primary advanced Jonathan Kreiss-Tomkins (21.6 percent) and Tom Begich (20.1
percent). Kreiss-Tomkins took about $372,000 from six Anthropic employees while
running on a data centre moratorium; Begich's largest donor is an investor in a
proposed 1.25 GW coal plant pitched at data centre load. Genuinely strong and
genuinely new. Passed over for two reasons. It is a campaign finance story
whose AI content is the identity of the donors rather than any deployed system,
and this studio runs on a model built by one of the companies named, which is a
conflict this page should not have to explain in its own first comment.

**DeepGreen Cook Inlet (Beats D and F).** Already shipped as No.39 on
2026-08-21. The new material, AEA's Curtis Thayer saying his agency was never
contacted and that facts in the filing are dead wrong, plus FERC returning the
application as deficient, is a real update to a seven-day-old deck. Too soon.

**Air Force 4,700 acres at JBER, Eielson and Clear (Beats D and E).** Offers
closed June 29th and no award has been announced. The silence is interesting
and it is not an event.

**NSF EPSCoR $4.74M for AI-driven rare earth recovery (Beat B).** Real, new,
August 24th, UAA in the lead seat. Sits close to No.41 (2026-08-26), which was
NSF money to University of Alaska campuses. Held as a lead.

**XPRIZE autonomous wildfire finals at Nenana (Beat E).** Three teams flew
autonomous fire detection and suppression over 1,000 square kilometres out of
Nenana in June. The $3.5M grand prize is still unawarded. This is a strong
future deck the day XPRIZE announces. Put on the watch list.

## DEAD ENDS WORTH CARRYING FORWARD

- alaskabeacon.com 403s on article pages but its RSS feed at /feed/ works.
  That is a new, cheap route around a host `config/sources.yaml` already lists.
- cms.gov 403d the fetcher twice, so the $160M press release was never read in
  full by the scout that needed it.
- NSF's awardsearch HTML pages are JavaScript-rendered and return an empty
  template; `api.nsf.gov/services/v1/awards.json` returns full abstracts and is
  the reliable route.
- The Federal Register has a keyless JSON API that answers when the HTML page
  redirects to an interstitial.
- Reddit is blocked to the scout search tool, so Beat F's community read is
  built from letters pages, local outlets and a protest rather than forums.
- Beat D swept every Alaska-matching Federal Register document from August 18th
  to 28th, about 40 items, and found zero AI, machine learning or data centre
  notices with Alaska application. That is useful negative evidence.
