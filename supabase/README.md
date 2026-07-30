# Readership backend

The two endpoints and the schema behind the reader counter on
alaskaaihq.com. They run on Supabase project `gsuvfpnyzebycqhsekus`.

They live here because until 2026-07-30 they lived ONLY in the Supabase
dashboard. A publication that publishes its source archive, its claim ids and
its correction log had its one piece of reader-facing server code in a place
nobody could review, and the review would have caught things: the collector
answered 204 to every drop so a working beacon and an empty table looked
identical, and the tables carried grants that let the publishable key empty
them. Both are fixed below. Code that receives requests from readers belongs
in git.

This directory is the record of what is deployed, not the deploy mechanism.
Editing a file here changes nothing until it is deployed.

## What is here

| Path | What it is |
| --- | --- |
| `functions/track/index.ts` | The collector. Receives one beacon per page read, writes a row or a drop reason. Deployed as `track`, version 3. |
| `functions/stats/index.ts` | The public aggregate endpoint. No key, aggregates only. Deployed as `stats`, version 1. |
| `migrations/0001_readership.sql` | `page_views`, `page_view_drops`, `readership_stats`, the RLS flags and the grants. |
| `migrations/0002_publish_drop_reasons.sql` | Adds `drops` to the stats payload, so a zero says which kind of zero it is. |

The client half is gated by `tests/beacon_fires.js`, which drives a real browser
at the real `site.js` and is the only check in this system that can catch a
preflight bug. Its `--self-test` reintroduces the shipped bug and requires the
gate to go red.

Both functions run with `verify_jwt: false`, which is the trust boundary: any
caller on the internet can reach them, so neither trusts its input. `track`
validates the path, clamps every string and accepts nothing it did not ask
for. `stats` is GET only and returns nothing but counts.

## What it can and cannot answer

By construction it answers what was read and roughly where from. It cannot
answer who, and no later change should try. There is no cookie, no visitor id,
no IP column and no user-agent column, so there is nothing to join on and no
unique-visitor figure is possible. `/privacy/` says this publicly and the
schema is what makes the statement true.

The client half is not here. It is generated into `docs/site.js` by
`scripts/site_build.py`, and `scripts/read_stats.py` reads the `stats`
endpoint for the daily Gmail draft.

## The one thing that is easy to get wrong

The beacon sends `text/plain`, and that is load bearing. `application/json` is
not a CORS-safelisted content type, so it makes the browser send a preflight
first, and `sendBeacon` cannot carry the headers a preflight then negotiates.
The observed cost was twelve OPTIONS preflights from real visits with not one
POST behind them: every reader counted as zero. The collector parses the body
as JSON whatever the content type claims, so nothing is lost by declaring
`text/plain`. Do not "tidy" it back.

## Deploying a change

There is no CI for these. Deploy through the Supabase MCP tools in a session,
or the dashboard, then bump the version in the table above so this file keeps
matching reality.

After changing `track`, check that a real request still stores, because a
silent drop is the failure mode this code has already had once:

```
curl -sS -o /dev/null -w '%{http_code}\n' \
  -X POST 'https://gsuvfpnyzebycqhsekus.supabase.co/functions/v1/track' \
  -H 'origin: https://alaskaaihq.com' \
  -H 'content-type: text/plain;charset=UTF-8' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36' \
  --data '{"p":"/probe/","r":null,"c":"probe"}'
```

204 proves nothing on its own, because 204 is also what every drop returns. The
public endpoint now answers both halves of the question with no key, so start
there rather than in SQL:

```
curl -sS 'https://gsuvfpnyzebycqhsekus.supabase.co/functions/v1/stats?days=1'
```

`views` up by one means it stored. `views` flat with a new entry under `drops`
means it was refused and tells you which guard did it. `views` flat and `drops`
empty means the request never arrived at all. Then delete the probe row so it
does not land in the published figures:

```sql
delete from public.page_views where campaign = 'probe';
```

That covers the server. It does NOT cover the browser, which is where the bug
actually was, so after any change to the beacon run the gate:

```
node tests/beacon_fires.js --self-test   # must go red
node tests/beacon_fires.js               # must go green
```

## Invariants worth re-checking after any schema change

Measured on 2026-07-30. `anon` should hold nothing on either table and should
not be able to execute the aggregate function directly.

```sql
select has_table_privilege('anon','public.page_views','TRUNCATE')            as must_be_false,
       has_table_privilege('anon','public.page_views','SELECT')              as must_be_false_too,
       has_function_privilege('anon','public.readership_stats(integer)','EXECUTE') as also_false,
       has_function_privilege('service_role','public.readership_stats(integer)','EXECUTE') as must_be_true;
```

RLS alone is not enough here, which is the trap worth writing down: RLS does
NOT cover TRUNCATE. Before the revoke in `0001`, `anon` could not read a row
(SELECT saw 0 of 1) and could not write one (INSERT raised 42501) and could
still `TRUNCATE public.page_views` successfully. Supabase's default privileges
are what handed that out, so a NEW table in `public` arrives equally open
unless the default is changed, which `0001` also does.
