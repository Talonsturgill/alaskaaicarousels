# QUEUED ASSIGNMENT for the next run

Written 2026-09-06 by run No. 52. This brief is for ONE run. Archive it into
`runs/<date>/next_run_brief.md` at ship time.

## THE STORY

**The federal AI money with an Alaska name on it is not a data center. It is an 8(a) contract.**

Run No. 52's Beat D scout found this on the FPDS-NG public ATOM feed, which is keyless, fetchable and
primary, and which works from this environment where sam.gov, govtribe and defense.gov all answer a
bot with a 403. It is the best unworked lead the sweep produced and no Alaska outlet has written it.

The anchor record, read out of the feed and safe to cite as an individual action:

    PIID W519TC26CA019
    Koniag Emerging Technologies LLC
    U.S. Army, for the Deputy to the Chief Digital and Artificial Intelligence Office
    "ARTIFICIAL INTELLIGENCE (AI) RAPID SUPPORT (AIRS) IN SUPPORT OF DEPUTY TO THE CHIEF
     DIGITAL ARTIFICIAL INTELLIGENCE OFFICE (CDAO) ENTERPRISE PROGRAMS"
    $5,267,244.80
    8(a) sole source
    place of performance Anchorage 99503
    signed May 29th, 2026, current completion May 28th, 2027, ultimate completion May 25th, 2031

Around it, a cluster of Koniag subsidiary obligations signed August 27th to September 4th, 2026
against the September 30th lapse date, including $4,388,379.84 to Koniag IT Systems from GSA for
cloud modernization, $1,864,975.79 to Koniag Technology Solutions from USDA, $1,346,350.73 to Koniag
IT Systems from the Rural Housing Service, and $679,233.27 of incremental DOE funding to Koniag
Emerging Technologies.

For historical contrast, also in the feed: PIID 140D0421C0002, Tuknik Government Services LLC of
Anchorage, roughly $24.2 million obligated across 2020 and 2021 for "IT, artificial intelligence (AI),
and machine learning (ML) programmatic support services" for the DOD CIO's Joint Artificial
Intelligence Center, 8(a) sole source, place of performance Alexandria, Virginia.

## THE ANGLE, and the fairness the story requires

The question is not whether any of this is proper. All of it is lawful, 8(a) is the mechanism Congress
built, and the profits of an ANCSA corporation flow to Alaska Native shareholders and village
corporations by design. Say all of that on the face of the deck, early, not as a hedge at the end.

The question is what "Alaska AI" means. This page has spent seven of thirty days on land, grid and
data centres, arguing about megawatts that may never be built, while the largest AI contracts actually
signed with Alaska entities were being obligated quietly, on a schedule set by the federal fiscal
year, for work whose place of performance is sometimes Anchorage and sometimes Virginia. The deck's
job is to put those two pictures beside each other honestly.

The natural visual is one map with two colours, vendor headquarters against place of performance, and
a September calendar strip with obligations piling against the September 30th wall.

## PRECONDITION, not a suggestion

**The FPDS ATOM feed paginates and No. 52's pulls came back with implausibly short result sets.** One
Alaska place-of-performance week query returned five entries. Every individual PIID, amount and date
above was read out of the feed and is safe, but this deck's whole spine is a PATTERN, and a pattern
claim needs the pattern to be provably complete.

So before this ships, the fact-checker must re-pull with explicit pagination, or cross-check against
usaspending.gov, and establish the denominator. **Do not publish a total, a rank, a share, or any
sentence of the form "most of" or "the largest" until that is done.** If the re-pull cannot establish
completeness, ship the deck about the ONE contract and say plainly that the full picture is not
public, which is itself a true and interesting thing about federal procurement data.

Field syntax that worked, space-joined:
`POP_STATE_NAME`, `VENDOR_ADDRESS_STATE_NAME`, `DESCRIPTION_OF_REQUIREMENT`, `PIID`,
`SIGNED_DATE:[YYYY/MM/DD,YYYY/MM/DD]`, against
`https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&templateName=1.5.3&q=...&feedmax=100`

Also useful and measured the same run, `https://r.jina.ai/<pdf-url>` renders agency PDFs to clean
text where WebFetch returns raw bytes.

## WHAT THIS BRIEF DOES NOT WAIVE

Every gate still binds exactly as written. The dedupe gate, the claims gate, the caption gates, the
scoring hard fails and the completion gate. Koniag and Alaska Native corporation contracting have not
appeared in `ledger/topics.json`, so the dedupe gate should pass cleanly, but run it and read it.

If the September 30th lapse date has already passed by the time this runs, that is not a reason to
drop the story. It is a reason to change the frame from a forward deadline to a closed year, and the
completed obligation record is a better document than a pending one.
