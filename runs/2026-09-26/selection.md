# Selection, run 2026-09-26 (No.69)

## Decision
**Alaska News, the AI-drafted statewide newsroom, and the one human name on its review labels.**

AlaskaNews.com (Communities News LLC, a team of five in Anchorage) drafts most of its articles with AI personas (Walter, Maggie, Bill, Melinda) from public meetings and records. It says its tool has sat through 1,258 recorded public meetings and 3,092 hours of audio (C04, C05), it has published more than 5,000 articles (C29), and it prints a provenance line under every article saying whether a human reviewed it (C12, C26). Its own AI policy admits some articles publish unread (C24) and that its footer once told every reader an article was "reviewed by editors" regardless (C25).

This run measured that label on every article in the outlet's 48-hour news sitemap: 90 articles (C47); 73 "Reviewed by Cale Green" (C48); 6 edited but "No full editor review is on record" (C49); 9 "AI-assisted. No editor review is on record" (C50); 2 with no AI label (C51). Cale Green is the only human name on any review label (C56; bylines were captured for only 19 of 90 rows, so no byline claim is made). Walter's own words to the Anchorage Press frame it: "Source access is not the same thing as editorial judgment" (C38).

Why it wins:
1. Alaska impact: it is the highest-volume news operation covering Alaska public bodies right now, and its model answers the state's structural coverage gap (C06 to C08). Anchorage Press, GeekWire and Alaska Public Media all covered it inside the window; community salience is real (Beat F).
2. Visual potential: quantity (90, 73, 1,258 meetings, 3,092 hours), a pipeline (meeting audio to transcript to draft to label), a single human name as a physical object, places (location tags across the state).
3. Tangibility: a primary measurement anyone can reproduce from the outlet's own pages.
4. An Alaskan would send it to a coworker: every reporter, clerk, assembly member and PIO in the state is now being covered by it.

Position the deck takes: the machine solved READING, and the label shows where the bottleneck moved, to judgment, which here is one person. The label is the right invention; the question is whether one name can carry it, and whether "reviewed by" should become the norm for every AI-drafted story in Alaska.

Honesty guards (write into the storyboard):
- Never imply an unreviewed article is wrong or a reviewed one is right. The label is a claim about process, not accuracy.
- Never imply the reviews did not happen. The deck reports what the labels SAY.
- The measurement is a 48-hour snapshot on September 26th; labels can change when an editor reviews later. Say "on September 26th" / "over 48 hours".
- Masthead backgrounds (a former Dunleavy spokesperson, a pollster) appear only with the outlet's own recusal statements (C15, C17), or not at all.
- Pronouns: refer to Cale Green by name or role ("the editor-in-chief"), never by a gendered pronoun.

## Dedupe gate
`dedupe_check.py --entities "Alaska News, Walter, Lee Brown, Lucas Brown, Cale Green, Anchorage Press, Nat Herz, Valdez" --keywords "AI agent, local news, journalism, newsroom, AI-generated articles, public records, reporting"`: strongest match No.50 at jaccard 0.007, SOFT OVERLAP on the word "public" only, zero shared entities. Read by eye: unrelated (a DNR land conveyance). No journalism or AI-newsroom topic in the ledger at any date. PASS.

## Runner-up
Cook Inlet gas crunch testimony (C58 to C65): survives with attribution, but overlaps No.56 (Cook Inlet storage, September 11th) and the Gas Watch beat, and its AI angle is secondhand. Second runner-up: UA regents draft AI policy (C66 to C68), which would need UPDATE framing against No.61 and rests on one syndicated source.

## Queued brief
prompts/NEXT_RUN.md (NPFMC 2027 Annual Deployment Plan) is parked until October 14th and stays in place.

## Directors room (lenses rotated off No.68's cartographer, editorial-essayist, historian-of-the-future)

- SYSTEMS-ILLUSTRATOR, "The Inspection Station": the newsroom as a production line whose only light is one tungsten lamp over an inspection station, a brass inspection tag as the label. Strongest idea: the lamp IS judgment. Weakest: a factory metaphor turns one named editor into "a narrow place", which the honesty guards forbid, and three GPU frames plus a loupe composite plus an unproven relief bench.
- DATA-JOURNALIST, "Reviewed By": one kraft tag per article, a 48-hour panorama cord, the found label as the cover. Strongest: one physical unit per article and shape-coded states; the finding that the seven newest articles are all unreviewed (a queue, not a verdict). Weakest: the tag on seven frames, and a private person's name at 128 px on the cover.
- CINEMATOGRAPHER, "The Focus Pull": one rendered committee-room table after the gavel, 90 draft pages in publication order, clips as provenance, the focal plane moving per slide. Strongest: depth itself carries the argument, and the cover is the machine's own admission. Weakest: an invented set, and seven mark families risk a sampler.

SYNTHESIS. The cinematographer's set, camera and focus pull are the spine; the data-journalist's rule of one object per article and shape-coded states become the clips and flags; the systems-illustrator's lamp-as-judgment is the one key light. The cover is Walter's sentence (the machine's own admission), which keeps a private person's name off the cover. Masterful depth frame 02 was prototyped before the dossiers; see PROTOTYPE FINDINGS in the storyboard.
