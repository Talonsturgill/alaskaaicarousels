#!/usr/bin/env python3
"""Read-only daily audit of the LIVE Gas Watch, its source, and its cron.

Exit 0: healthy or explicitly disclosed maintenance. Exit 2: repair/attention
required. No ledger writes, inferred readings, account changes or messages.
"""
import argparse
import json
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import gaswatch_collect as gc

SITE = "https://alaskaaihq.com"
RUNS_URL = ("https://api.github.com/repos/Talonsturgill/alaskaaicarousels/"
            "actions/workflows/gaswatch.yml/runs?per_page=30")


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# One row per endpoint the audit could not read. A blocked endpoint is a FAIL,
# never a skip: the checks that needed it are not run, and nothing about it may
# read as healthy. What it no longer does is take the OTHER endpoints' checks
# down with it (2026-09-27: CINGSA's firewall answered one fetch with a 307 and
# the whole audit collapsed to one row, reporting nothing about the live page,
# the feed or the cron that had all answered 200).
ENDPOINTS = {
    "feed": ("live JSON reachable",
             "Retry /gas-watch.json and check the Pages deployment. Its checks were NOT run."),
    "page": ("live page reachable",
             "Retry /gas-watch/ and check the Pages deployment. Its checks were NOT run."),
    "source": ("source reachable",
               "Retry CINGSA; if its firewall refuses this network, read the production "
               "collector's job log and archived snapshot instead. Source checks were NOT run. "
               "Do not change the collector's User-Agent."),
    "runs": ("cron runs reachable",
             "Use authenticated GitHub tools and --runs-json if API-limited. Cron checks were NOT run."),
}


def assess(feed, page, source, runs, now, unreachable=None, ledger=None):
    """Audit what could be read. `feed`, `page`, `source` or `runs` may be None
    when `unreachable` names why; every check that needed it is withheld and
    the endpoint itself is reported as a FAIL, so the verdict can't pass."""
    checks = []
    unreachable = dict(unreachable or {})
    for key, value in (("feed", feed), ("page", page), ("source", source), ("runs", runs)):
        if value is None:
            unreachable.setdefault(key, "not read")

    def add(name, passed, detail, remedy, warning=False):
        checks.append({"name": name, "status": "PASS" if passed else ("WARN" if warning else "FAIL"),
                       "detail": detail, "remedy": remedy if not passed else ""})

    for key in ENDPOINTS:
        if key in unreachable:
            add(ENDPOINTS[key][0], False, unreachable[key], ENDPOINTS[key][1])
    has_feed, has_page = feed is not None, page is not None
    has_source, has_runs = source is not None, runs is not None
    feed = feed if has_feed else {}
    page = page if has_page else ""

    today = now.astimezone(gc.alaska_tz()).date()
    series = feed.get("series") or []
    dates = [r["date"] for r in series]
    if has_feed:
        add("live dataset", bool(series) and len(set(dates)) == len(dates) == feed.get("count"),
            f"{len(series)} daily records", "Rebuild from the canonical ledger and verify Pages deployment.")
        missing = []
        for offset in range(3):
            day = today - timedelta(days=offset)
            # Give the current Alaska morning time to capture its first posting.
            if offset == 0 and now.astimezone(gc.alaska_tz()).hour < 12:
                continue
            if day.isoformat() not in dates:
                missing.append(day.isoformat())
        add("recent calendar days", not missing, ", ".join(missing) or "last three days accounted for",
            "Run the repaired collector to append explicit missing-day records. Never invent storage.")
        polluted = [r["date"] for r in series if not r.get("verified") and (
            any((r.get("cingsa") or {}).get(k) is not None for k in gc.MEASURED) or
            any((r.get("derived") or {}).get(k) is not None for k in
                ("storage_withdrawal_mmcfd", "non_cingsa_supply_mmcfd", "days_cover_at_peak")))]
        add("unverified storage stays empty", not polluted, ", ".join(polluted) or "no carried-forward measurements",
            "Repair the collector and append corrections; preserve original ledger lines.")

    stale = maintenance = False
    if has_source:
        add("source capacity fields valid", not source.get("field_errors"),
            ", ".join(source.get("field_errors") or {}) or "all capacity fields readable",
            "Inspect CINGSA's archived source. Keep affected rates unavailable; do not infer corrections.")
        source_age = (now - stamp(source["source_timestamp_utc"])).total_seconds() / 3600
        stale = source_age > gc.STALE_HOURS
        maintenance = gc.maintenance_pause(source, ["cingsa_stale"] if stale else [], today.isoformat())
        add("source freshness", not stale, f"source {source['source_timestamp']} Alaska, {source_age:.1f} hours old",
            "Check CINGSA and its archived snapshots. Keep missing storage unverified; disclose upstream unavailability.",
            warning=maintenance)
    verified = [r for r in series if r.get("verified")]
    latest = max(verified, key=lambda r: r["date"]) if verified else None
    if latest:
        cin = latest["cingsa"]
        if has_page:
            hero = re.search(r'class="gw-hero">([\d.]+)', page)
            add("live headline agrees", bool(hero) and float(hero.group(1)) == cin["inventory_pct_of_design"],
                f"last verified {latest['date']}, {cin['inventory_pct_of_design']} percent",
                "Rebuild the page from the current ledger, deploy and read the live headline again.")
        if has_source:
            matches = (latest["date"] == source["source_timestamp"][:10] and
                       cin.get("inventory_mcf") == source.get("inventory_mcf"))
            add("source reading published", matches or stale,
                f"published {latest['date']}; source {source['source_timestamp']}",
                "Inspect collector logs and source snapshots, repair the parser or rerun collection, then deploy.",
                warning=source_age < 2)
    elif has_feed:
        add("verified storage exists", False, "no verified reading in live data",
            "Diagnose the collector and source; never substitute modeled or prior-day storage.")
    unavailable = stale or (latest and any(d > latest["date"] for d in dates))
    # Without the source, a gap is only knowable from the feed itself; an
    # unknown gap is withheld rather than read as "no gap to disclose".
    if has_page and (has_feed or has_source) and (has_source or unavailable):
        add("source gap disclosed", not unavailable or 'id="gw-source-status"' in page,
            "source notice present" if 'id="gw-source-status"' in page else "no source notice",
            "Explain unavailable readings briefly beside the chart, then rebuild and deploy.")
    if has_page and has_feed:
        has_chart = '<div class="gw-chart"' in page and 'data-gw-plot=' in page
        add("history chart present", len(verified) < 2 or has_chart,
            "chart present" if has_chart else "fewer than two readings" if len(verified) < 2 else "chart missing",
            "Rebuild and deploy the history chart. Keep unavailable storage empty in the published data.")

    if has_feed:
        forecasts = [r for r in series if r.get("forecast") and r.get("forecast_source_updated")]
        newest = max(forecasts, key=lambda r: r["forecast_source_updated"]) if forecasts else None
        forecast_age = (now - stamp(newest["forecast_source_updated"])).total_seconds() / 3600 if newest else None
        add("weather forecast current", forecast_age is not None and forecast_age <= 36,
            f"forecast age {forecast_age:.1f} hours" if forecast_age is not None else "no forecast",
            "Inspect NWS fetch logs; retry weather collection independently of unavailable storage.")
        if has_page:
            shown = re.search(r'gw-num">\s*([\d.]+)\s*</div>\s*<div class="gw-lab">'
                              r'\s*MMcf/d modeled peak ahead', page)
            expected = (max(gc.demand(d["hdd65"], feed["model"]) for d in newest["forecast"])
                        if newest and feed.get("model") else None)
            add("live modeled peak agrees", bool(shown) and expected is not None and float(shown.group(1)) == expected,
                f"page {shown.group(1) if shown else 'missing'}, computed {expected}",
                "Rebuild and deploy the page from the latest forecast and model; verify the live value.")
        reconciled = gc.reconciliation_index(series)
        overdue = []
        for record in series:
            day = datetime.fromisoformat(record["date"]).date()
            if not 2 <= (today - day).days <= 7:
                continue
            obs = reconciled.get(record["date"]) or {}
            if obs.get("actual_hdd65") is None or (record.get("verified") and
                    obs.get("non_cingsa_supply_mmcfd") is None):
                overdue.append(record["date"])
        add("observations and true-ups", not overdue, ", ".join(overdue) or "available observations reconciled",
            "Retry ACIS observations. Compute supply only where verified same-day storage exists.")

    if has_runs:
        production = sorted([r for r in runs.get("workflow_runs", [])
                             if r.get("head_branch") == "main" and r.get("event") != "pull_request"],
                            key=lambda r: r["created_at"], reverse=True)
        recent = production[0] if production else None
        run_age = (now - stamp(recent["created_at"])).total_seconds() / 3600 if recent else None
        add("cron is running", run_age is not None and run_age <= 18,
            f"last run {run_age:.1f} hours ago" if recent else "no production run found",
            "Inspect workflow enablement and logs, repair the workflow, and dispatch a production run.")
        completed = next((r for r in production if r.get("status") == "completed"), None)
        add("cron completed successfully", bool(completed) and completed.get("conclusion") == "success",
            f"{completed.get('conclusion')}: {completed.get('html_url')}" if completed else "no completed run",
            "Read the failed job logs and fix the cause. A maintenance notice does not excuse a failed job.")
    diagnosis = timing_diagnosis(source if has_source else None, runs if has_runs else None, checks,
                                 ledger, now)
    verdict = "FAIL" if any(c["status"] == "FAIL" for c in checks) else ("MAINTENANCE" if maintenance else
              ("WARN" if any(c["status"] == "WARN" for c in checks) else "PASS"))
    report = {"checked_utc": gc.iso_z(now), "verdict": verdict, "checks": checks,
              "last_verified_date": latest["date"] if latest else None,
              "maintenance_window": gc.maintenance_window(source.get("operational_note") or "") if has_source else None}
    if unreachable:
        report["unreachable"] = sorted(unreachable)
    if diagnosis:
        report["diagnosis"] = diagnosis
    return report


# LATE POST OR BROKEN COLLECTOR (2026-11-01, weekly machine pass). Queue item
# 2026-09-30 reached repeat 17: on run after run the first audit FAILed because
# CINGSA posted the day's reading in the Alaska evening, after the last
# collection that had run, and the showrunner re-derived that from timestamps
# by hand each time before dispatching gaswatch.yml (204 on every try since
# October 20th). The audit already holds both timestamps, so it now says which
# shape it is looking at. It changes NO status and NO verdict: a reading the
# live page lacks is still a FAIL until it is collected and deployed. It only
# names the cause and the remedy on the checks that the late post explains.
LATE_CHECKS = ("source reading published", "recent calendar days")
DISPATCH = "gh workflow run gaswatch.yml --ref main"
# THE DEPLOY LAG IS NOT A COLLECTOR FAULT (2026-11-27 weekly pass, queue item
# 2026-11-18 at repeat 2: No.118, 119, 121, 126). The first diagnosis compared
# run START against CINGSA's stamp, so a collection that had already committed
# the reading, with Pages a few minutes behind, read as "collector, parser or
# Pages at fault", and so did a clean run that fetched before CINGSA served a
# reading it had stamped earlier. The audit now reads main's ledger (a read,
# never a write) and asks the question directly: did a collection record this
# posting? Still NO status and NO verdict moves; only the named cause does.
LEDGER_URL = ("https://api.github.com/repos/Talonsturgill/alaskaaicarousels/"
              "contents/ledger/gaswatch.jsonl?ref=main")
DEPLOY_GRACE_MIN = 30   # a Pages deploy has taken 3 to 8 minutes here
STAMP_LEAD_MIN = 60     # CINGSA served a stamped reading 19+ minutes late (No.118)


def recorded_on_main(source, ledger):
    """The ledger record on main that holds this posting, or None."""
    for rec in reversed(ledger or []):
        cin = rec.get("cingsa") or {}
        if cin.get("source_timestamp") == source.get("source_timestamp") or (
                rec.get("verified") and rec.get("date") == (source.get("source_timestamp") or "")[:10]
                and cin.get("inventory_mcf") is not None
                and cin.get("inventory_mcf") == source.get("inventory_mcf")):
            return rec
    return None


def timing_diagnosis(source, runs, checks, ledger=None, now=None):
    """{'kind': ..., ...} when a LATE_CHECKS row is not PASS and both the
    source and the cron runs were read, else None. Kinds:
    late_post: no production collection has started since CINGSA's stamp, or
      (main's ledger read) every one since succeeded inside STAMP_LEAD_MIN of
      the stamp and none recorded the posting.
    deploy_pending: main's ledger already holds the posting; Pages has not
      redeployed (2026-11-27 weekly pass: four runs read this as a fault).
    collection_running: a collection after the stamp is still running.
    collected_after_post: a collection after the stamp finished and the
      posting is neither live nor on main, so the collector or the parser is
      at fault (or a run failed)."""
    hit = [c for c in checks if c["name"] in LATE_CHECKS and c["status"] != "PASS"]
    # Anchored on the source's own reading being unpublished: a stale source
    # (CINGSA not posting) passes that row, and a missing day then is not a
    # late post, whatever the timestamps say.
    if not any(c["name"] == LATE_CHECKS[0] for c in hit):
        return None
    if source is None or runs is None or not source.get("source_timestamp_utc"):
        return None
    posted = stamp(source["source_timestamp_utc"])
    production = sorted([r for r in runs.get("workflow_runs", [])
                         if r.get("head_branch") == "main" and r.get("event") != "pull_request"
                         and r.get("created_at")],
                        key=lambda r: r["created_at"], reverse=True)
    newest = production[0] if production else None
    out = {"source_posted_utc": gc.iso_z(posted),
           "newest_collection_utc": newest["created_at"] if newest else None,
           "checks": [c["name"] for c in hit]}
    if newest is None or stamp(newest["created_at"]) < posted:
        out["kind"] = "late_post"
        out["remedy"] = (
            "LATE POST, not a stopped collector: CINGSA posted this reading at "
            f"{out['source_posted_utc']}, after the newest production collection "
            f"({out['newest_collection_utc'] or 'none found'}). Dispatch the collector on main "
            f"({DISPATCH}, or the Actions API workflow_dispatch), wait for the run and the "
            "Pages deployment, then rerun this audit. An incident is for a dispatch that "
            "can't run (403) or a run that fails.")
    else:
        after = [r for r in production if stamp(r["created_at"]) >= posted]
        first, last = after[-1], after[0]
        out["first_run_after_post"] = {k: first.get(k) for k in
                                       ("created_at", "status", "conclusion", "html_url")}
        out["main_ledger"] = "read" if ledger is not None else "not read"
        seen = recorded_on_main(source, ledger)
        done = [r for r in after if r.get("status") == "completed"]
        lead = (stamp(last["created_at"]) - posted).total_seconds() / 60
        if seen is not None:
            collected = seen.get("collected_utc") or ""
            out["kind"] = "deploy_pending"
            out["recorded_on_main_utc"] = collected or None
            age = (now - stamp(collected)).total_seconds() / 60 if (collected and now) else None
            out["remedy"] = (
                "DEPLOY LAG, not a collector fault: the collector recorded this posting "
                f"(collected {collected or 'at an unrecorded time'}) and it is in main's "
                "ledger/gaswatch.jsonl, so the live site simply has not redeployed. "
                + (f"That was {age:.0f} minutes ago, longer than a Pages deployment takes "
                   f"({DEPLOY_GRACE_MIN} minutes): read the pages.yml run for that commit, rerun "
                   "or repair it, then rerun this audit."
                   if age is not None and age > DEPLOY_GRACE_MIN else
                   "Wait for the Pages deployment of that commit, then rerun this audit. "
                   "Don't dispatch another collection."))
        elif len(done) < len(after) and not any(r.get("conclusion") not in (None, "success")
                                                  for r in done):
            out["kind"] = "collection_running"
            # Name a run that is actually unfinished, not the earliest one after
            # the posting, which may already have completed (Codex, PR #518).
            running = next(r for r in after if r.get("status") != "completed")
            out["remedy"] = (
                f"A production collection started at {running['created_at']} after CINGSA posted "
                f"at {out['source_posted_utc']} and has not finished: wait for it and the Pages "
                "deployment, then rerun this audit.")
        elif (ledger is not None and done and lead <= STAMP_LEAD_MIN and
              all(r.get("conclusion") == "success" for r in done)):
            # CINGSA stamps a reading before the dashboard serves it (No.118:
            # stamped 01:00Z, still the old posting at 01:19Z). A clean run that
            # started inside that lead and wrote nothing most likely fetched
            # before the posting existed: no run has seen it yet.
            out["kind"] = "late_post"
            out["stamp_lead_minutes"] = round(lead, 1)
            out["remedy"] = (
                "LATE POST behind its own stamp: every production collection since CINGSA's "
                f"stamp ({out['source_posted_utc']}) succeeded, the newest started {lead:.0f} "
                f"minutes after it, and main's ledger has no record of this posting, so none of "
                "them saw it (CINGSA stamps a reading before its dashboard serves it). Dispatch "
                f"the collector on main ({DISPATCH}), wait for the run and Pages, then rerun this "
                f"audit. If a run that starts more than {STAMP_LEAD_MIN} minutes after the stamp "
                "also records nothing, it is the collector or the parser.")
        else:
            out["kind"] = "collected_after_post"
            out["remedy"] = (
                f"NOT a timing problem: a production collection started at {first['created_at']} "
                f"({first.get('status')}, {first.get('conclusion')}), after CINGSA posted at "
                f"{out['source_posted_utc']}, and the reading is still not live"
                + (" or in main's ledger. " if ledger is not None else
                   ". Main's ledger was NOT read, so a Pages deploy lag is not ruled out: check "
                   "whether that run committed the reading before calling it a fault. ")
                + (f"Read the log of the newest run after the post ({last.get('html_url')}); "
                   "the collector or the parser is at fault."))
    for c in hit:
        c["remedy"] = (c["remedy"] + " " if c["remedy"] else "") + out["remedy"]
    return out


# A BOUNDED RE-READ FOR A TRANSIENT REFUSAL (2026-10-01, run No.74). CINGSA's
# proxy has answered this audit's first read with an HTTP 307 and no Location
# header on three of the last five runs (2026-09-27, 09-29, 10-01), and each
# time a manual re-read seconds later answered 200 with a real page. The audit
# then reported FAIL, the showrunner re-ran it by hand, and the incident was
# re-diagnosed from scratch. So the checker re-reads a TRANSIENT failure (a 3xx
# urllib could not follow, 408, 425, 429, any 5xx, a timeout or a dropped
# connection) twice more, after 10 s and 20 s. A PERSISTENT refusal (403, 404 or
# any other 4xx) is never retried, a failure that survives all three reads is
# reported exactly as before, and every retried failure is written into the
# audit under `transient_retries` with the endpoint, so a pass after a retry is
# disclosed and never painted green silently.
RETRY_WAITS = (10, 20)
TRANSIENT_HTTP = {408, 425, 429}
RETRIED = {}


def transient(exc):
    if isinstance(exc, HTTPError):
        return 300 <= exc.code < 400 or exc.code in TRANSIENT_HTTP or exc.code >= 500
    return isinstance(exc, (URLError, TimeoutError, ConnectionError))


def fetch(url, waits=RETRY_WAITS, sleep=time.sleep, accept=None):
    headers = {"User-Agent": gc.UA, "Cache-Control": "no-cache"}
    if accept:
        headers["Accept"] = accept
    req = Request(url, headers=headers)
    for attempt in range(len(waits) + 1):
        try:
            with urlopen(req, timeout=45) as response:
                return response.read().decode("utf-8")
        except Exception as exc:
            if attempt >= len(waits) or not transient(exc):
                raise
            RETRIED.setdefault(url, []).append(f"{type(exc).__name__}: {exc}")
            sleep(waits[attempt])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site-url", default=SITE)
    ap.add_argument("--output", help="write the audit JSON for the daily run's gate")
    ap.add_argument("--runs-json", help="GitHub API workflow-runs response, if fetched through a connector")
    ap.add_argument("--ledger-jsonl", help="main's ledger/gaswatch.jsonl, if fetched through a connector "
                    "(read only for the timing diagnosis)")
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    base = args.site_url.rstrip("/")
    # Each endpoint is read on its own, so one refusal can't hide the others.
    got, unreachable = {}, {}
    readers = {
        "feed": lambda: json.loads(fetch(base + "/gas-watch.json")),
        "page": lambda: fetch(base + "/gas-watch/"),
        "source": lambda: gc.parse_cingsa(fetch(gc.CINGSA_URL)),
        "runs": lambda: json.loads(Path(args.runs_json).read_text() if args.runs_json else fetch(RUNS_URL)),
    }
    for key, read in readers.items():
        try:
            got[key] = read()
        except Exception as exc:
            unreachable[key] = f"{type(exc).__name__}: {exc}"
    try:
        report = assess(got.get("feed"), got.get("page"), got.get("source"), got.get("runs"),
                        now, unreachable)
        # A collection ran after the stamp: whether it RECORDED the posting is
        # the difference between a deploy lag and a collector fault, so read
        # main's ledger for the diagnosis. A failed read changes no check; the
        # diagnosis then says the ledger was not read.
        if (report.get("diagnosis") or {}).get("first_run_after_post"):
            try:
                text = (Path(args.ledger_jsonl).read_text() if args.ledger_jsonl else
                        fetch(LEDGER_URL, accept="application/vnd.github.raw"))
                ledger = [json.loads(line) for line in text.splitlines() if line.strip()]
            except Exception as exc:
                ledger, ledger_error = None, f"{type(exc).__name__}: {exc}"
            if ledger is not None:
                report = assess(got.get("feed"), got.get("page"), got.get("source"),
                                got.get("runs"), now, unreachable, ledger=ledger)
            else:
                report["diagnosis"]["ledger_error"] = ledger_error
    except Exception as exc:
        report = {"checked_utc": gc.iso_z(now), "verdict": "FAIL", "checks": [{
            "name": "live audit completed", "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}",
            "remedy": "Retry the unavailable endpoint. Use authenticated GitHub tools and --runs-json if API-limited. Do not claim the live page was checked."}]}
    report["site_url"] = base
    if RETRIED:
        report["transient_retries"] = {url: list(errs) for url, errs in RETRIED.items()}
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + "\n")
    for check in report["checks"]:
        print(f"[{check['status']}] {check['name']}: {check['detail']}")
        if check["remedy"]:
            print(f"  Next: {check['remedy']}")
    if report.get("diagnosis"):
        print(f"[DIAGNOSIS] {report['diagnosis']['kind']}: {report['diagnosis']['remedy']}")
    for url, errs in report.get("transient_retries", {}).items():
        print(f"[RETRIED] {url}: {len(errs)} transient failure(s) before the read that counted: "
              + "; ".join(errs))
    print(f"GAS WATCH LIVE: {report['verdict']}")
    return 2 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
