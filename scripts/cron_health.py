#!/usr/bin/env python3
"""Daily read-only supervision of every scheduled workflow on production main.

Run after bootstrap: python3 scripts/cron_health.py --output out/<date>/cron_health.json
Reads GitHub runs AND job steps, then checks public output against a fresh main
snapshot. It never dispatches, edits data, or treats a green PR as collection.
Exit 2 requires the AI routine to diagnose, repair, and repeat this audit.
"""
import argparse
import html
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import yaml  # already installed by the daily routine's bootstrap

REPO = Path(__file__).resolve().parents[1]
REPOSITORY = "Talonsturgill/alaskaaicarousels"
SITE = "https://alaskaaihq.com"
GRACE = timedelta(hours=8)  # GitHub has delayed the weekly job over six hours.
MAX_RUNNING = timedelta(hours=2)
KINDS = ("enabled", "schedule", "completion", "steps")
OUTPUT_IDS = {"pages:enabled", "pages:completion", "pages:steps", "pages:revision",
              "live:gas-watch/", "live:gas-watch.json", "output:power",
              "output:power-utility", "output:docket-watch", "output:weather", "output:gas-model"}


def stamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return parsed


def iso(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO, timeout=120)


def scheduled_crons(contents):
    data = yaml.load(contents, Loader=yaml.BaseLoader)
    triggers = data.get("on", {})
    schedules = triggers.get("schedule", []) if isinstance(triggers, dict) else []
    if any(set(s) != {"cron"} for s in schedules):
        raise ValueError("Review unsupported schedule options")
    return sorted(s["cron"] for s in schedules)


def inventory(ref=None):
    """Read every schedule, including jobs added after this checker ships."""
    if ref:
        files = git("ls-tree", "-r", "--name-only", ref, ".github/workflows").decode().splitlines()
        read = lambda p: git("show", f"{ref}:{p}").decode()
    else:
        files = [str(p.relative_to(REPO)) for p in (REPO / ".github/workflows").glob("*")]
        read = lambda p: (REPO / p).read_text()
    found = {}
    for path in sorted(files):
        if not path.endswith((".yml", ".yaml")):
            continue
        crons = scheduled_crons(read(path))
        if crons:
            found[Path(path).name] = crons
    if not found:
        raise ValueError("No scheduled workflows found; the inventory is incomplete")
    return found


def schedule_activated(name, crons, ref):
    """Find when this schedule reached main, ignoring unrelated workflow edits."""
    path = ".github/workflows/" + name
    history = git("log", "--first-parent", "--format=%H%x09%cI", ref, "--", path).decode().splitlines()
    activated = None
    for line in history:
        sha, committed = line.split("\t")
        # A previous deletion ends the current incarnation of this workflow.
        if not git("ls-tree", "--name-only", sha, "--", path).strip():
            break
        if scheduled_crons(git("show", f"{sha}:{path}").decode()) != sorted(crons):
            break
        activated = stamp(committed)
    if activated is None:
        raise ValueError(f"Cannot establish when {name}'s schedule became active")
    return activated


def field_values(field, low, high):
    """GitHub's numeric POSIX cron fields. Unknown syntax fails visibly."""
    values = set()
    for part in field.split(","):
        base, sep, step = part.partition("/")
        step = int(step) if sep else 1
        if step <= 0:
            raise ValueError("cron step must be positive")
        if base == "*":
            start, end = low, high
        elif "-" in base:
            start, end = map(int, base.split("-"))
        else:
            start = int(base)
            end = high if sep else start
        if not low <= start <= end <= high:
            raise ValueError(f"unsupported cron field {field}")
        values.update(range(start, end + 1, step))
    return values


def last_due(crons, cutoff):
    """Most recent scheduled occurrence older than the dispatch grace window."""
    candidates = []
    for cron in crons:
        fields = cron.split()
        if len(fields) != 5:
            raise ValueError(f"unsupported cron {cron}")
        minutes, hours, dom, months, dow = [field_values(f, *bounds) for f, bounds in
            zip(fields, [(0, 59), (0, 23), (1, 31), (1, 12), (0, 7)])]
        dow = {d % 7 for d in dow}
        for offset in range(366 * 5):  # includes leap-day schedules
            day = cutoff - timedelta(days=offset)
            md, wd = day.day in dom, (day.weekday() + 1) % 7 in dow
            # POSIX: restricted day-of-month and weekday are alternatives.
            matches = (md or wd) if fields[2] != "*" and fields[4] != "*" else md and wd
            if day.month not in months or not matches:
                continue
            times = [day.replace(hour=h, minute=m, second=0, microsecond=0)
                     for h in hours for m in minutes]
            eligible = [t for t in times if t <= cutoff]
            if eligible:
                candidates.append(max(eligible))
                break
        else:
            raise ValueError(f"no occurrence found for {cron}")
    return max(candidates)


def row(check_id, ok, detail, url="", warning=False):
    return {"id": check_id, "status": "PASS" if ok else "WARN" if warning else "FAIL",
            "detail": detail, "evidence_url": url}


def production(runs, events):
    return sorted((r for r in runs if r.get("head_branch") == "main" and r.get("event") in events),
                  key=lambda r: (r["created_at"], r.get("run_attempt", 1)), reverse=True)


def completed_run(runs):
    # Skipped PR-triggered Pages workflows are not deployments.
    return next((r for r in runs if r["status"] == "completed" and r.get("conclusion") != "skipped"), None)


def completion_rows(prefix, runs, jobs, now, due=None):
    complete = completed_run(runs)
    latest = runs[0] if runs else None
    overdue = any(r["status"] != "completed" and now - stamp(r["created_at"]) > MAX_RUNNING for r in runs)
    current = bool(complete) and (due is None or stamp(complete["created_at"]) >= due)
    passed = current and complete.get("conclusion") == "success" and not overdue
    url = complete.get("html_url", "") if complete else ""
    detail = f"{complete['conclusion']} at {complete['created_at']}" if complete else "no completed production run"
    if overdue:
        detail += "; queued or running over two hours"
    pending = bool(latest and latest["status"] != "completed")
    rows = [row(prefix + ":completion", passed and not pending,
                detail + ("; newer run still pending, recheck" if pending else ""), url,
                warning=passed and pending)]
    failed = [f"{j['name']}: {s['name']} ({s.get('conclusion')})"
              for j in jobs for s in j.get("steps", [])
              if s.get("conclusion") not in ("success", "skipped", None)]
    # These are scheduled/dispatch runs, not PR validation. A skipped refresh
    # job must not let successful unit tests stand in for data collection.
    failed += [f"{j['name']} ({j.get('conclusion')})" for j in jobs
               if j.get("conclusion") != "success"]
    rows.append(row(prefix + ":steps", bool(jobs) and not failed,
                    "; ".join(failed) or ("job steps clean" if jobs else "job-step evidence missing"), url))
    return rows


def assess_workflow(name, crons, state, runs, jobs, now, activated=None):
    runs = production(runs, {"schedule", "workflow_dispatch"})
    due = last_due(crons, now - GRACE)
    scheduled = next((r for r in runs if r["event"] == "schedule"), None)
    not_due_yet = activated is not None and due < activated
    url = f"https://github.com/{REPOSITORY}/actions/workflows/{name}"
    rows = [row(name + ":enabled", state == "active", f"workflow state: {state}", url),
            row(name + ":schedule", not_due_yet or bool(scheduled) and stamp(scheduled["created_at"]) >= due,
                (f"schedule activated {iso(activated)}; first occurrence not yet due" if not_due_yet else
                 f"scheduled run due since {iso(due)}; latest " +
                 (scheduled["created_at"] if scheduled else "missing")), url)]
    return rows + completion_rows(name, runs, jobs, now, max(due, activated) if activated else due)


def fetch(url):
    request = Request(url, headers={"User-Agent": "AlaskaAI-daily-cron-audit/1.0", "Cache-Control": "no-cache"})
    with urlopen(request, timeout=45) as response:
        return response.read()


def api(path):
    endpoint = f"repos/{REPOSITORY}/{path}"
    try:
        result = subprocess.run(["gh", "api", endpoint], capture_output=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return json.loads(fetch("https://api.github.com/" + endpoint))


def jobs_for(runs):
    run = completed_run(runs)
    if not run:
        return []
    result = api(f"actions/runs/{run['id']}/attempts/{run.get('run_attempt', 1)}/jobs?per_page=100")
    if result["total_count"] > len(result["jobs"]):
        raise ValueError("job list is truncated; paginate before claiming success")
    return result["jobs"]


def deployment_revision(run, docs_sha):
    """Deployment must include the latest published-file change, not just gas."""
    if not run:
        return row("pages:revision", False, "no completed deployment")
    comparison = api(f"compare/{docs_sha}...{run['head_sha']}")
    included = comparison.get("status") in ("identical", "ahead")
    return row("pages:revision", included,
               f"deployment {run['head_sha'][:12]} {'includes' if included else 'does not include'} latest docs {docs_sha[:12]}",
               run.get("html_url", ""))


def expected_ids(workflows):
    return {f"{name}:{kind}" for name in workflows for kind in KINDS} | OUTPUT_IDS


def gas_model_published(feed, model, eia, history):
    """A current deployment can still contain a page built before its inputs."""
    shown = feed.get("model", {})
    return (bool(model) and all(shown.get(k) == v for k, v in model.items())
            and shown.get("hdd_history_end") == history["end_date"]
            and shown.get("hdd_history_days") == history["days"]
            and feed.get("crosscheck", {}).get("eia_latest_month") == eia["latest_month"])


def power_published(page, residential):
    month = re.search(r'class="pwread-m">([^<]+)', page)
    price = re.search(r'class="pwread-v"><b>([\d.]+)', page)
    observed_month = html.unescape(month[1]) if month else None
    observed_price = float(price[1]) if price else None
    ok = observed_month == residential["latest_label"] and observed_price == residential["latest"]
    detail = (f"household price and month match main: {residential['latest_label']}" if ok else
              f"live household price/month {observed_price!r}/{observed_month!r}; "
              f"expected {residential['latest']!r}/{residential['latest_label']!r}")
    return ok, detail


def audit(now):
    shallow = git("rev-parse", "--is-shallow-repository").decode().strip() == "true"
    git("fetch", "--quiet", *( ["--unshallow"] if shallow else []), "origin", "main")
    main_sha = git("rev-parse", "origin/main").decode().strip()
    workflows = inventory(main_sha)
    checks, last_runs = [], {}
    states = api("actions/workflows?per_page=100")
    if states["total_count"] > len(states["workflows"]):
        raise ValueError("workflow inventory is truncated")
    states = {Path(w["path"]).name: w["state"] for w in states["workflows"]}
    for name, crons in workflows.items():
        try:
            runs = []
            for event in ("schedule", "workflow_dispatch"):
                runs += api(f"actions/workflows/{name}/runs?branch=main&event={event}&per_page=20")["workflow_runs"]
            runs = production(runs, {"schedule", "workflow_dispatch"})
            checks += assess_workflow(name, crons, states.get(name), runs, jobs_for(runs), now,
                                      schedule_activated(name, crons, main_sha))
            last_runs[name] = completed_run(runs)
        except Exception as exc:
            checks += [row(f"{name}:{kind}", False, f"audit unavailable: {exc}") for kind in KINDS]

    try:
        runs = api("actions/workflows/pages.yml/runs?branch=main&per_page=100")["workflow_runs"]
        runs = [r for r in production(runs, {"push", "workflow_run", "workflow_dispatch"})
                if r.get("conclusion") != "skipped"]
        checks.append(row("pages:enabled", states.get("pages.yml") == "active", str(states.get("pages.yml"))))
        checks += completion_rows("pages", runs, jobs_for(runs), now)
        docs_sha = git("log", "-1", "--format=%H", main_sha, "--", "docs", ".github/workflows/pages.yml").decode().strip()
        checks.append(deployment_revision(completed_run(runs), docs_sha))
    except Exception as exc:
        checks = [c for c in checks if not c["id"].startswith("pages:")]
        checks += [row("pages:" + k, False, f"audit unavailable: {exc}") for k in ("enabled", "completion", "steps", "revision")]

    page, feed = "", {}
    for route, path in [("gas-watch/", "docs/gas-watch/index.html"), ("gas-watch.json", "docs/gas-watch.json")]:
        try:
            actual = fetch(SITE + "/" + route)
            expected = git("show", f"{main_sha}:{path}")
            checks.append(row("live:" + route, actual == expected,
                              f"public bytes {'match' if actual == expected else 'differ from'} main {main_sha[:12]}", SITE + "/" + route))
            if route.endswith("/"):
                page = actual.decode()
            else:
                feed = json.loads(actual)
        except Exception as exc:
            checks.append(row("live:" + route, False, f"public output unavailable: {exc}", SITE + "/" + route))

    def data(path):
        return json.loads(git("show", f"{main_sha}:{path}"))

    for kind in ("power", "power-utility", "docket-watch", "weather", "gas-model"):
        try:
            if kind == "power":
                res = data("ledger/power.json")["sectors"]["residential"]
                ok, detail = power_published(page, res)
            elif kind == "power-utility":
                ledger = data("ledger/power_utility.json")
                trs = re.findall(r"<tr>.*?</tr>", page, re.S)
                absent = [u["name"] for u in ledger["utilities"]
                          if u.get("sectors", {}).get("residential", {}).get("cents_per_kwh") and not any(
                              html.escape(u["name"]) in tr and
                              f'{u["sectors"]["residential"]["cents_per_kwh"]:.2f}' in tr for tr in trs)]
                ok = not absent and f"charged in {ledger['data_year']}" in page
                detail = "utility year and every household price match main" if ok else f"missing/stale utility rows: {absent}"
            elif kind == "docket-watch":
                queue = data("ledger/watch.json")
                age = now - stamp(queue["generated"])
                ok = timedelta(0) <= age <= timedelta(hours=36) and not queue.get("failed")
                detail = f"queue generated {queue['generated']}; failed sources: {queue.get('failed')}"
            elif kind == "gas-model":
                ok = gas_model_published(feed, data("config/gaswatch_model.json"),
                                         data("ledger/gaswatch_eia.json"), data("config/gaswatch_hdd_history.json"))
                detail = "published model, EIA month and weather span " + ("match main" if ok else "lag or differ from main")
            else:
                hist = data("config/gaswatch_hdd_history.json")
                run = last_runs.get("gaswatch-eia.yml")
                expected_day = (stamp(run["created_at"]) - timedelta(days=2)).date() if run else now.date()
                ok = datetime.fromisoformat(hist["end_date"]).date() >= expected_day
                detail = f"weather history through {hist['end_date']}; expected at least {expected_day}"
            checks.append(row("output:" + kind, ok, detail, SITE + "/gas-watch/" if kind.startswith("power") else
                              f"https://github.com/{REPOSITORY}/tree/{main_sha}"))
        except Exception as exc:
            checks.append(row("output:" + kind, False, f"output audit unavailable: {exc}"))
    return {"schema_version": 1, "checked_utc": iso(now), "repository": REPOSITORY,
            "site_url": SITE, "main_sha": main_sha, "workflows": workflows, "checks": checks,
            "verdict": "FAIL" if any(r["status"] == "FAIL" for r in checks) else
                       "WARN" if any(r["status"] == "WARN" for r in checks) else "PASS"}


def gate(report, incidents, workflows, now):
    """No omitted checks, stale evidence, or blanket incident waiver."""
    try:
        valid = (report["schema_version"] == 1 and report["repository"] == REPOSITORY
                 and report["site_url"] == SITE and report["workflows"] == workflows
                 and -0.1 <= (now - stamp(report["checked_utc"])).total_seconds() / 3600 <= 24)
        checks = report["checks"]
        ids = [r["id"] for r in checks]
        valid = valid and len(ids) == len(set(ids)) and set(ids) == expected_ids(workflows)
        valid = valid and all(r["status"] in ("PASS", "WARN", "FAIL") for r in checks)
        if not valid:
            return "FAIL", "cron audit is stale, incomplete, or not production"
        failures = {r["id"] for r in checks if r["status"] == "FAIL"}
        if not failures:
            return ("WARN" if any(r["status"] == "WARN" for r in checks) else "PASS",
                    f"{len(workflows)} scheduled workflows audited at {report['checked_utc']}")
        if incidents is not None and not isinstance(incidents, list):
            return "FAIL", "cron incident evidence must be an array"
        covered = set()
        for incident in incidents or []:
            if not isinstance(incident, dict):
                continue
            text = lambda v: isinstance(v, str) and bool(v.strip())
            texts = lambda v: isinstance(v, list) and bool(v) and all(text(s) for s in v)
            if (incident.get("audit_checked_utc") == report["checked_utc"]
                    and incident.get("blocker") in ("upstream", "github", "credentials")
                    and text(incident.get("reason")) and texts(incident.get("attempts"))
                    and texts(incident.get("evidence_urls")) and texts(incident.get("check_ids"))
                    and set(incident["check_ids"]) <= failures
                    and all(re.fullmatch(r"https?://[^\s/]+(?:/[^\s]*)?", url)
                            for url in incident["evidence_urls"])):
                covered.update(incident["check_ids"])
        if failures <= covered:
            return "WARN", "UNRESOLVED external blockers: " + ", ".join(sorted(failures))
        return "FAIL", "repair unresolved cron checks: " + ", ".join(sorted(failures - covered))
    except (KeyError, TypeError, ValueError, AttributeError):
        return "FAIL", "cron audit or incident evidence is malformed"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    try:
        report = audit(now)
    except Exception as exc:
        report = {"checked_utc": iso(now), "verdict": "FAIL",
                  "checks": [row("audit", False, f"audit could not complete: {exc}")]}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    for check in report["checks"]:
        print(f"[{check['status']}] {check['id']}: {check['detail']}")
    print("CRON HEALTH: " + report["verdict"])
    return 2 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
