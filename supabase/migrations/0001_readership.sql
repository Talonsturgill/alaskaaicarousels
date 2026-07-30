-- Readership measurement for alaskaaihq.com.
--
-- Captured from the live database on 2026-07-30 rather than written from
-- memory, so this file is a record of what actually runs: every column type,
-- index definition, RLS flag and grant below was read back out of the
-- catalogue. Verified by replaying the whole file against that database, which
-- ran clean and left the invariants unchanged. Written to be idempotent so the
-- replay is the test. Not yet run against an empty project.
--
-- The design constraint that shapes every line below: this can answer WHAT was
-- read and WHERE FROM, and can never answer WHO. There is no cookie, no visitor
-- id, no IP column and no user-agent column, so there is nothing to join
-- against and no unique-visitor count is possible. That is a deliberate
-- ceiling, not a gap to fill later. /privacy/ states it publicly and this
-- schema is what makes the statement true.

-- One row per page read. Nothing here identifies a reader.
create table if not exists public.page_views (
  id        bigint generated always as identity primary key,
  at        timestamptz not null default now(),
  path      text not null,           -- query string and fragment stripped by the collector
  ref_host  text,                    -- referring HOST only, never the full URL; null when same-site or absent
  campaign  text,                    -- ?c= or ?utm_campaign=, alphanumeric only
  device    text,                    -- desktop / mobile / tablet / other, bucketed in memory from the UA
  country   text                     -- two-letter code from the edge, when the edge supplies one
);

-- Composite rather than single column, because every query in
-- readership_stats filters on the time window first and then groups.
create index if not exists page_views_at_idx on public.page_views (at desc);
create index if not exists page_views_path_at_idx on public.page_views (path, at desc);
create index if not exists page_views_ref_at_idx on public.page_views (ref_host, at desc);

-- Why a beacon did NOT get counted.
--
-- The collector answers 204 to everything on purpose, so it never tells a
-- caller whether it recorded. The cost of that was discovered the hard way: it
-- never told the OWNER either, so real visits could arrive, be answered 204,
-- and write nothing, with no way to tell which guard ate them. Reason and
-- timestamp only. No path, no referrer, no user agent, no address, nothing
-- about the reader, so this is not a shadow log of the visits that opted out.
create table if not exists public.page_view_drops (
  id     bigint generated always as identity primary key,
  at     timestamptz not null default now(),
  reason text not null
);

create index if not exists page_view_drops_at_idx on public.page_view_drops (at desc);

-- RLS on, zero policies, which denies every ordinary role outright. The edge
-- functions reach these tables as service_role, which bypasses RLS, so no
-- policy is needed and adding one would only widen the surface.
alter table public.page_views enable row level security;
alter table public.page_view_drops enable row level security;

-- RLS is the second line, not the only one.
--
-- Supabase's default privileges hand anon and authenticated the full grant set
-- on every new table in this schema, and RLS DOES NOT COVER TRUNCATE. Measured
-- on 2026-07-30 before this revoke: as anon, SELECT saw 0 of 1 rows and INSERT
-- raised 42501, both correctly blocked by RLS, but TRUNCATE SUCCEEDED. So a
-- caller holding the publishable key could not read or write a row and could
-- still empty either table outright.
--
-- Only the edge functions touch these tables and they authenticate as
-- service_role, so neither anon nor authenticated needs any privilege at all.
revoke all on public.page_views from anon, authenticated;
revoke all on public.page_view_drops from anon, authenticated;

-- Without this a future table in this schema arrives equally wide open.
alter default privileges in schema public revoke all on tables from anon, authenticated;

-- The only way readership figures leave the database.
--
-- SECURITY DEFINER so the caller needs no privilege on page_views, STABLE
-- because it only reads, and search_path pinned so a caller cannot shadow
-- public with their own schema and change what the body resolves to.
--
-- Returns aggregates exclusively. No row shape crosses this boundary, and the
-- window is clamped to 1..90 days here as well as in the edge function so a
-- junk value cannot provoke an unbounded scan.
create or replace function public.readership_stats(p_days integer default 7)
returns jsonb
language sql
stable
security definer
set search_path to 'public', 'pg_temp'
as $function$
  with bounds as (
    -- Bound the window so a caller cannot ask for an unbounded scan.
    select greatest(1, least(coalesce(p_days, 7), 90)) as d
  ),
  win as (
    select v.path, v.ref_host, v.campaign, v.device
    from public.page_views v, bounds b
    where v.at >= now() - make_interval(days => b.d)
  )
  select jsonb_build_object(
    'days', (select d from bounds),
    'views', (select count(*) from win),
    'generated_at', to_char(now() at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
    'top_paths', coalesce((
      select jsonb_agg(jsonb_build_object('path', path, 'views', n))
      from (select path, count(*) as n from win group by path
            order by count(*) desc, path limit 12) t), '[]'::jsonb),
    'top_articles', coalesce((
      select jsonb_agg(jsonb_build_object('path', path, 'views', n))
      from (select path, count(*) as n from win
            where path like '/archive/%' group by path
            order by count(*) desc, path limit 8) t), '[]'::jsonb),
    'top_decisions', coalesce((
      select jsonb_agg(jsonb_build_object('path', path, 'views', n))
      from (select path, count(*) as n from win
            where path like '/docket/%' and path <> '/docket/' group by path
            order by count(*) desc, path limit 8) t), '[]'::jsonb),
    'referrers', coalesce((
      select jsonb_agg(jsonb_build_object('host', ref_host, 'views', n))
      from (select ref_host, count(*) as n from win
            where ref_host is not null group by ref_host
            order by count(*) desc, ref_host limit 10) t), '[]'::jsonb),
    'direct', (select count(*) from win where ref_host is null),
    'campaigns', coalesce((
      select jsonb_agg(jsonb_build_object('campaign', campaign, 'views', n))
      from (select campaign, count(*) as n from win
            where campaign is not null group by campaign
            order by count(*) desc, campaign limit 10) t), '[]'::jsonb),
    'devices', coalesce((
      select jsonb_object_agg(device, n)
      from (select device, count(*) as n from win
            where device is not null group by device) t), '{}'::jsonb)
  );
$function$;

-- A SECURITY DEFINER function is executable by PUBLIC unless told otherwise,
-- and this one reads a table nobody else can read. The stats edge function
-- calls it as service_role, so that is the only grant it gets.
revoke all on function public.readership_stats(integer) from public, anon, authenticated;
grant execute on function public.readership_stats(integer) to service_role;
