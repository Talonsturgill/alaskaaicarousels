#!/usr/bin/env python3
"""Read-only daily audit of the LIVE Gas Watch, its source, and its cron.

Exit 0: healthy or explicitly disclosed maintenance. Exit 2: repair/attention
required. No ledger writes, inferred readings, account changes or messages.
"""
import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import gaswatch_collect as gc

SITE = "https://alaskaaihq.com"
RUNS_URL = ("https://api.github.com/repos/Talonsturgill/alaskaaicarousels/"
            "actions/workflows/gaswatch.yml/runs?per_page=30")


def stamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def assess(feed, page, source, runs, now):
    checks = []

    def add(name, passed, detail, remedy, warning=False):
        checks.append({"name": name, "status": "PASS" if passed else ("WARN" if warning else "FAIL"),
                       "detail": detail, "remedy": remedy if not passed else ""})

    today = now.astimezone(gc.alaska_tz()).date()
    series = feed.get("series") or []
    dates = [r["date"] for r in series]
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
        hero = re.search(r'class="gw-hero">([\d.]+)', page)
        add("live headline agrees", bool(hero) and float(hero.group(1)) == cin["inventory_pct_of_design"],
            f"last verified {latest['date']}, {cin['inventory_pct_of_design']} percent",
            "Rebuild the page from the current ledger, deploy and read the live headline again.")
        matches = (latest["date"] == source["source_timestamp"][:10] and
                   cin.get("inventory_mcf") == source.get("inventory_mcf"))
        add("source reading published", matches or stale,
            f"published {latest['date']}; source {source['source_timestamp']}",
            "Inspect collector logs and source snapshots, repair the parser or rerun collection, then deploy.",
            warning=source_age < 2)
    else:
        add("verified storage exists", False, "no verified reading in live data",
            "Diagnose the collector and source; never substitute modeled or prior-day storage.")
    unavailable = stale or (latest and any(d > latest["date"] for d in dates))
    add("source gap disclosed", not unavailable or 'id="gw-source-status"' in page,
        "source notice present" if 'id="gw-source-status"' in page else "no source notice",
        "Explain unavailable readings briefly beside the chart, then rebuild and deploy.")
    has_chart = '<div class="gw-chart"' in page and 'data-gw-plot=' in page
    add("history chart present", len(verified) < 2 or has_chart,
        "chart present" if has_chart else "fewer than two readings" if len(verified) < 2 else "chart missing",
        "Rebuild and deploy the history chart. Keep unavailable storage empty in the published data.")

    forecasts = [r for r in series if r.get("forecast") and r.get("forecast_source_updated")]
    newest = max(forecasts, key=lambda r: r["forecast_source_updated"]) if forecasts else None
    forecast_age = (now - stamp(newest["forecast_source_updated"])).total_seconds() / 3600 if newest else None
    add("weather forecast current", forecast_age is not None and forecast_age <= 36,
        f"forecast age {forecast_age:.1f} hours" if forecast_age is not None else "no forecast",
        "Inspect NWS fetch logs; retry weather collection independently of unavailable storage.")
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
    verdict = "FAIL" if any(c["status"] == "FAIL" for c in checks) else ("MAINTENANCE" if maintenance else
              ("WARN" if any(c["status"] == "WARN" for c in checks) else "PASS"))
    return {"checked_utc": gc.iso_z(now), "verdict": verdict, "checks": checks,
            "last_verified_date": latest["date"] if latest else None,
            "maintenance_window": gc.maintenance_window(source.get("operational_note") or "")}


def fetch(url):
    req = Request(url, headers={"User-Agent": gc.UA, "Cache-Control": "no-cache"})
    with urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site-url", default=SITE)
    ap.add_argument("--output", help="write the audit JSON for the daily run's gate")
    ap.add_argument("--runs-json", help="GitHub API workflow-runs response, if fetched through a connector")
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    base = args.site_url.rstrip("/")
    try:
        feed = json.loads(fetch(base + "/gas-watch.json"))
        page = fetch(base + "/gas-watch/")
        source = gc.parse_cingsa(fetch(gc.CINGSA_URL))
        runs = json.loads(Path(args.runs_json).read_text() if args.runs_json else fetch(RUNS_URL))
        report = assess(feed, page, source, runs, now)
    except Exception as exc:
        report = {"checked_utc": gc.iso_z(now), "verdict": "FAIL", "checks": [{
            "name": "live audit completed", "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}",
            "remedy": "Retry the unavailable endpoint. Use authenticated GitHub tools and --runs-json if API-limited. Do not claim the live page was checked."}]}
    report["site_url"] = base
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + "\n")
    for check in report["checks"]:
        print(f"[{check['status']}] {check['name']}: {check['detail']}")
        if check["remedy"]:
            print(f"  Next: {check['remedy']}")
    print(f"GAS WATCH LIVE: {report['verdict']}")
    return 2 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
