# Alaska homepage headlines

The homepage news strip replaces its daylight readout. It reuses Texas AI Docket's compact
carousel, with Alaska fonts and colors, previous and next controls, and no visible count or
pause icon. Headlines, source and original date fade together every five seconds. Source and
date share the heading row. Dates display in Alaska time, preserving evening publication days
across UTC midnight. Hover, focus and pressing a link hold it steady. Reduced-motion
preferences use manual navigation. Background and offscreen tabs stop their timers.

## Selection

Every story needs an explicit Alaska location or institution in its headline or bounded source
excerpt, plus AI, computing, energy or relevant technology. Alaska Airlines' brand alone and
Arctic reporting from other countries do not establish Alaska relevance. Common names such as
Kodiak, Bethel and Palmer need explicit Alaska context. Sports, promotional
items, daily newscast compilations and republished time capsules are excluded. The same tests
cover the seed, cache, responses and every queued story. An outlet's address never qualifies a
national story. Publisher headlines are attributed quotations and remain verbatim, including
punctuation. House-copy lints continue to cover all authored surrounding copy.

AI leads within each freshness group, followed by energy, then other technology.
Reports under seventy-two hours precede older reports. Independent reporting precedes university
announcements within a category. Distinct independent coverage and source age rank the remaining
choices. Identical syndicated titles and first-party announcements do not inflate coverage.
The ranking measures source coverage and freshness rather than audience readership.

Each edition keeps up to ten distinct eligible subjects. Prior appearances never lower a
story's ranking. Strong reporting can remain across refreshes or return after displacement.
Lead ordering uses the least recently shown member of the selected pool. One or two good
stories can remain without importing global news. There is no replacement quota.

Alaska's quieter beat has a fourteen-day hard limit. The original publisher date or first
observation never resets. Reports after seventy-two hours display Recent. The browser removes
expired members individually, including offline, and retains other eligible reporting. A valid
focused link stays steady while another member expires. Empty or expired pools link to the
verified article archive.

## Sources and operation

config/news_sources.json names permitted source hosts and source formats. The inputs include
KTOO, Alaska Business, Alaska Native News, Data Center Dynamics, ScienceDaily and UAF. Bounded
RSS pagination covers more of the smaller local publishing cycle. UAF's official news index
supplies only each card's title, date and short excerpt. Article pages are never fetched. A
day-only university date is stored at midnight in America/Anchorage. No model rewrites copy.

Every source respects its robots policy for the collector and named AI crawlers. A host's robots
file is read once per collection, including across paginated feeds. Responses and excerpts have
size limits. Each feed gets one attempt. ETag and Last-Modified reduce transfers. Failures and
HTTP Retry-After persist across restarts. Healthy sources continue when another is unavailable.

The collector runs at 01:23, 07:23, 13:23 and 19:23 UTC. Four scheduled editions keep the reader
experience moving if GitHub dispatches late. On load and every fifteen visible minutes, the
browser checks the public metadata. No publisher request occurs per headline transition.

Refreshes publish only ledger/news/latest.json on the news-data branch. They never rebuild the
site or write main. Non-forced ref updates and timestamp checks prevent older runs overwriting
newer data. Builds embed a validated seed for first paint. Local storage retains valid metadata.

## Release proof

news-checks.yml runs selection, parser, backoff, publication, quote-boundary, generated-site and
browser regressions on PRs. news.yml validates and publishes each production collection, probes
the same CDN bucket a reader uses, then checks the live desktop and phone carousel and its next
six-hour edition while offline. Collection success and live display are separate checks.
