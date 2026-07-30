-- Publish WHY beacons were refused, alongside how many were counted.
--
-- The drop reasons existed after 0001 but only someone with SQL access could
-- read them, so a figure of zero still needed a human to interpret it and the
-- interpretation on offer was a guess. That is the same failure as the one the
-- drop table was built to fix, one level up: the collector stopped answering
-- 204 to everything, and then the STATS endpoint took over being uninformative.
--
-- A zero should explain itself. views 0 with drops {"dnt-header": 3} is a
-- counter working exactly as designed and three readers exercising an opt-out.
-- views 0 with drops {} is a counter nothing is reaching. Those are opposite
-- conclusions and they were previously indistinguishable from the outside.
--
-- Aggregate counts by reason, which is all page_view_drops holds. No path, no
-- referrer, no address, no user agent, so publishing this cannot expose a
-- reader. Consistent with the rest of the endpoint being public.
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
  ),
  dwin as (
    select r.reason
    from public.page_view_drops r, bounds b
    where r.at >= now() - make_interval(days => b.d)
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
            where device is not null group by device) t), '{}'::jsonb),
    -- Why the uncounted were not counted. Reasons only, never a reader.
    'drops', coalesce((
      select jsonb_object_agg(reason, n)
      from (select reason, count(*) as n from dwin group by reason) t), '{}'::jsonb)
  );
$function$;

-- create or replace does not reset privileges, but restating them keeps this
-- file correct if it is ever applied to a project that never ran 0001.
revoke all on function public.readership_stats(integer) from public, anon, authenticated;
grant execute on function public.readership_stats(integer) to service_role;
