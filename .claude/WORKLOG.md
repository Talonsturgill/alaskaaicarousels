# WORKLOG: readership measurement (2026-07-29)

Goal: stop guessing. Know whether anyone reads this, what brings them, and
which beats land, without collecting anything about the reader.

## Why self-hosted rather than a third party

Supabase project gsuvfpnyzebycqhsekus (alaska-ai-dashboard) is ACTIVE_HEALTHY
and already serves the scanner's four public edge functions, so the collector
costs nothing new and no third party holds the audience. The deciding reason
is the feedback loop: a hosted dashboard is a thing you must remember to
visit, whereas data in this project can be read BY THE ROUTINE and printed
into the daily Gmail draft. instincts.json currently grades the machine's own
homework with zero audience input; this is what closes that loop.

Site is GitHub Pages behind Fastly, not Cloudflare, so CDN analytics is not
available without moving DNS.

## Privacy stance (this is the point, not a footnote)

A publication that lectures about honesty must not ship surveillance. So:
- NO cookies, NO localStorage, NO fingerprint, NO visitor id of any kind.
- The raw IP is never stored. The user agent is never stored.
- Referrer is reduced to its HOST before storage (a full referrer URL can leak
  private context). Query strings are dropped except an explicit campaign tag.
- Honour Do Not Track and Global Privacy Control, and send nothing on either.
- Because no personal data is processed, no consent banner is needed, and we
  say so publicly on /privacy/ rather than burying it.

Consequence accepted: with no visitor id there are no unique-visitor counts.
Pageviews, referrers and campaigns answer the actual questions, so that is a
fair trade rather than a loss.

## Known limitation, to state plainly and not paper over

A JavaScript beacon measures HUMANS, not crawlers. LLM and search crawlers do
not run JS, so this will not measure AI crawler traffic at all. Measuring that
needs server logs, which GitHub Pages does not provide. This answers "does
anyone read it", not "do the bots fetch it".

## Build order

1. **Collector**: migration adding `page_views` (new name, no collision with
   the 11 scanner/dashboard tables) with RLS, plus a public `track` edge
   function (verify_jwt false, same posture as the scan-* functions) that
   derives a coarse device class and country, stores neither IP nor UA, and
   filters obvious bots.
2. **Beacon**: ~15 lines in site.js. One send per pageview, sendBeacon,
   no-op on localhost and on DNT/GPC.
3. **Disclosure**: /privacy/ page stating exactly what is and is not
   collected. Ships WITH the collector, never after; collecting before
   disclosing would be the exact hypocrisy this repo exists to avoid.
4. **The loop**: read_stats.py queries recent days; gmail_draft.py prints the
   block into the daily draft so the numbers arrive without anyone visiting a
   dashboard.

## Constraints

- House rules: no em/en dashes, no emoji, straight quotes, NO PROSE COLONS.
  Every new page goes through the punctuation and colon gates.
- docs/videos/* is a HARD GUARD. Do not touch.
- Do NOT modify the four existing scan-* edge functions or any existing table.
  New table, new function, additive only.
- Never store a secret in docs/. The beacon uses the public anon posture the
  scan functions already use.

## Status

| # | Slice | Status |
|---|-------|--------|
| 1 | collector, table + track function | DONE |
| 2 | beacon in site.js | DONE |
| 3 | /privacy/ disclosure page | DONE |
| 4 | read_stats.py + daily draft block | DONE |

## Shipped, with one honest gap

country never populates. GitHub Pages plus Supabase supply no geo header, so
the column is reserved rather than functional and /privacy/ says so outright.
Region and city were declined on purpose.

Verified after deploy: 2 rows from 5 test requests. The GPTBot request, the
Do Not Track request and a junk path were all correctly NOT recorded, and the
LinkedIn hit stored linkedin.com as a bare host with its campaign tag.
