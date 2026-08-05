#!/usr/bin/env python3
"""gaswatch_collect.py, the Cook Inlet Gas Watch daily collector.

Appends exactly one JSON object per day to ledger/gaswatch.jsonl. That file is
a daily numeric record of Southcentral Alaska's natural gas position, published
as open data beside the docket. The docket tracks discrete decisions on a scale
of months; this tracks the physical system on a scale of days. They are
siblings, so gas watch records never go into ledger/docket.json.

Three free feeds, no keys:
  CINGSA public dashboard   measured storage inventory and deliverability
  api.weather.gov           6.5 day hourly forecast, Anchorage grid AER 143,236
  data.rcc-acis.org         PANC observed daily HDD, for next day reconciliation

WHAT THIS TOOL WILL NOT DO. It never issues a safety verdict. It publishes
measured storage, modeled demand, and the derived residual, and it names the
size of what is not public. A compressor failure or a sanded well can produce
curtailment on a day the numbers looked survivable, so a published verdict
would be a credibility loss the data cannot carry. No field in the record
answers whether the region makes it through a cold snap, and none ever should.

WHY THIS RUNS ON ITS OWN SCHEDULE and not as a carousel phase. CLAUDE.md says a
failed run commits evidence and does not merge. That is right for editorial
output and wrong for a time series. If a carousel run fails its quality gates on
a Tuesday, Tuesday's storage reading would be lost permanently, and a missed day
is the one irreversible failure this project has. The collector is deliberately
boring, cheap, and indifferent to whether the day's story was any good.

Exit codes, so .github/workflows/gaswatch.yml can tell the cases apart:
  0  wrote a verified record, or skipped because one already stands for the day
  1  unexpected error, nothing written
  2  wrote an unverified record, a fetch failed or the source is stale
  3  an unverified record already stands for this date and this attempt also
     failed, so nothing was written

Run:
  python3 scripts/gaswatch_collect.py --self-test     # hermetic, no network
  python3 scripts/gaswatch_collect.py --dry-run       # fetch, print, write nothing
  python3 scripts/gaswatch_collect.py                 # append one record
"""

import argparse
import collections
import html
import json
import os
import re
import sys
import time
import traceback
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

COLLECTOR_VERSION = "1.0"

UA = "AlaskaAI-GasWatch/1.0 (+https://alaskaaihq.com; docket@alaskaaihq.com)"

CINGSA_URL = "https://cingsa.com/operations/PublicDashBoard.html"
NWS_HOURLY = "https://api.weather.gov/gridpoints/AER/143,236/forecast/hourly"
ACIS_URL = "https://data.rcc-acis.org/StnData"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "ledger", "gaswatch.jsonl")
MODEL_CONFIG = os.path.join(REPO, "config", "gaswatch_model.json")

# The CINGSA dashboard holds today's snapshot and nothing else. No archive, no
# JSON endpoint, no history of any kind. If its stamp is older than this, the
# page has stopped moving and the number must not be presented as current.
STALE_HOURS = 36

TIMEOUT = 45
RETRIES = 3
BACKOFF = (2, 4, 8)

# NWS hourly returns a partial first and last day. A day with fewer hours than
# this cannot produce an honest mean temperature, so it is dropped rather than
# averaged over whatever hours happened to be in the window.
MIN_HOURS_PER_DAY = 20

SUSTAINED_COLD_HDD = 55
DESIGN_DAY_APPROACH_MMCFD = 350


# ------------------------------------------------------------------ time

def alaska_tz():
    """America/Anchorage, or a fixed offset if tzdata is missing.

    The CINGSA stamp is Alaska local with no offset on it and the workflow runs
    on a UTC machine, so comparing the two naively would put the stale guard
    eight or nine hours off. The fallback picks AKDT, the smaller offset, which
    makes a stamp look older rather than younger. The guard errs toward flagging
    staleness, never toward hiding it.
    """
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("America/Anchorage")
    except Exception:
        return timezone(timedelta(hours=-8))


def now_utc():
    return datetime.now(timezone.utc)


def iso_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------ fetch

class Probe:
    """One external call and everything needed to audit it later.

    Provenance is per call, in the spirit of the docket's claim ids. A record
    that says a number is 6,456,905 also says where it came from, when it was
    pulled, and whether that pull worked.
    """

    def __init__(self, name, url, method="GET"):
        self.name = name
        self.url = url
        self.method = method
        self.status = "pending"
        self.http_status = None
        self.fetched_utc = None
        self.error = None
        self.attempts = 0

    def as_dict(self):
        d = {
            "name": self.name,
            "url": self.url,
            "method": self.method,
            "fetch_status": self.status,
            "fetched_utc": self.fetched_utc,
            "http_status": self.http_status,
            "attempts": self.attempts,
        }
        if self.error:
            d["error"] = self.error
        return d


def http(probe, data=None, headers=None):
    """Fetch with backoff, recording the outcome on the probe.

    NWS answers with an occasional 500 or 503 and CINGSA sits behind a CDN, so a
    single transient failure must not cost the day. Retries are bounded and a
    4xx is not retried, because a 403 or a 404 will not fix itself in eight
    seconds.
    """
    return http_bytes(probe, data=data, headers=headers).decode("utf-8", "ignore")


def http_bytes(probe, data=None, headers=None):
    """The same fetch, undecoded, for payloads that are not text.

    The EIA bulk dataset is a zip archive, and decoding it as utf-8 before
    unzipping would corrupt it. Text callers go through http(), which decodes.
    """
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    last = None
    for attempt in range(RETRIES):
        probe.attempts = attempt + 1
        try:
            req = urllib.request.Request(probe.url, data=data, headers=h,
                                         method=probe.method)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                body = resp.read()
                probe.http_status = resp.status
                probe.status = "ok"
                probe.fetched_utc = iso_z(now_utc())
                return body
        except urllib.error.HTTPError as exc:
            last = exc
            probe.http_status = exc.code
            # Retry a server error, a rate limit, and a redirect that surfaced
            # as an error, which is what a CDN interstitial looks like from
            # here. A plain 4xx is not retried, because a 403 or a 404 will not
            # fix itself in eight seconds.
            if not (exc.code >= 500 or exc.code == 429 or 300 <= exc.code < 400):
                break
        except Exception as exc:
            last = exc
        if attempt < RETRIES - 1:
            time.sleep(BACKOFF[min(attempt, len(BACKOFF) - 1)])
    probe.status = "failed"
    probe.fetched_utc = iso_z(now_utc())
    probe.error = f"{type(last).__name__}: {last}"
    raise RuntimeError(f"{probe.name} fetch failed, {probe.error}")


# ------------------------------------------------------------------ CINGSA

def cingsa_cells(raw):
    """Flatten the dashboard to an ordered list of non empty text cells.

    Parse by row label, never by position. The labels are stable and the table
    order is not guaranteed. Flattening to cells also survives the page's mixed
    formatting, where some rows sit on one line and others are broken across
    four, which a line oriented regex does not.
    """
    txt = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"<[^>]+>", "|", txt)
    txt = html.unescape(txt)
    cells = (re.sub(r"\s+", " ", c).strip() for c in txt.split("|"))
    return [c for c in cells if c]


def _number(cell):
    if not re.fullmatch(r"-?[\d,]+(?:\.\d+)?", cell):
        return None
    return float(cell.replace(",", ""))


def row(cells, label, count, lo=0, hi=None):
    """The `count` numbers that follow `label`, searched inside cells[lo:hi].

    The window matters. Design Capacity and Maximum Contracted Capacity each
    appear twice on the page, once in the injection and withdrawal table in
    Mcf/d and once in the storage volume table in Mcf. A parser that takes the
    first match reads a rate as a volume. The caller passes the section bounds.
    """
    hi = len(cells) if hi is None else hi
    for i in range(lo, min(hi, len(cells))):
        if cells[i].lower() != label.lower():
            continue
        got = []
        for cell in cells[i + 1:hi]:
            val = _number(cell)
            if val is None:
                break
            got.append(val)
            if len(got) == count:
                break
        if len(got) == count:
            return got if count > 1 else got[0]
    raise ValueError(
        f"CINGSA layout changed, could not read {count} number(s) after "
        f"row label {label!r}"
    )


def parse_cingsa(raw):
    cells = cingsa_cells(raw)

    stamp_at = None
    for i, cell in enumerate(cells):
        if cell.lower().startswith("last updated"):
            stamp_at = i
            break
    if stamp_at is None or stamp_at + 1 >= len(cells):
        raise ValueError("CINGSA layout changed, no Last Updated stamp")
    try:
        stamp = datetime.strptime(cells[stamp_at + 1], "%m/%d/%Y %H:%M")
    except ValueError as exc:
        raise ValueError(
            f"CINGSA layout changed, unreadable Last Updated value "
            f"{cells[stamp_at + 1]!r}, {exc}"
        )
    stamp = stamp.replace(tzinfo=alaska_tz())

    # The storage volume heading is the boundary between the two tables. Rate
    # rows are before it, volume rows after it.
    split = None
    for i, cell in enumerate(cells):
        if cell.lower().startswith("storage volume"):
            split = i
            break
    if split is None:
        raise ValueError("CINGSA layout changed, no Storage Volume heading")

    inj_design, wd_design = row(cells, "Design Capacity", 2, hi=split)
    inj_fac, wd_fac = row(cells, "Facility Capacity", 2, hi=split)
    inj_res, wd_res = row(cells, "Physical Restrictions", 2, hi=split)
    inj_op, wd_op = row(cells, "Operating Capacity", 2, hi=split)
    inj_av, wd_av = row(cells, "Available Capacity", 2, hi=split)

    design_volume = row(cells, "Design Capacity", 1, lo=split)
    begin = row(cells, "Beginning Inventory", 1, lo=split)
    end = row(cells, "Ending Inventory", 1, lo=split)

    # Published identity, worth asserting because a silent layout shuffle that
    # still parses would otherwise pass every other check in this file.
    if abs((inj_fac - inj_res) - inj_op) > 1 or abs((wd_fac - wd_res) - wd_op) > 1:
        raise ValueError(
            "CINGSA layout changed, operating capacity is not facility less "
            "physical restrictions, so the rows did not land where expected"
        )
    # Unit guard. Every check above passes if CINGSA restates the table in
    # MMcf instead of Mcf, because the rows still parse and the identities
    # still hold; every number would just be a thousand times too small and
    # nothing would say so. The published field is 13 million Mcf, so a band
    # this wide only trips on a unit change or a decimal shift, never on
    # ordinary operations.
    if not 1_000_000 <= design_volume <= 100_000_000:
        raise ValueError(
            f"CINGSA units changed, storage design volume reads {design_volume:,.0f} "
            f"which is outside the plausible band for Mcf")
    if not 0 <= end <= design_volume * 1.05:
        raise ValueError(
            f"CINGSA units changed, ending inventory reads {end:,.0f} against a "
            f"design volume of {design_volume:,.0f}")
    if not 1_000 <= wd_fac <= 10_000_000:
        raise ValueError(
            f"CINGSA units changed, facility withdrawal capacity reads "
            f"{wd_fac:,.0f} which is outside the plausible band for Mcf/d")

    note = ""
    for i, cell in enumerate(cells):
        if cell.lower().startswith("operational notes"):
            parts = []
            for nxt in cells[i + 1:]:
                if nxt.lower().startswith("note to user"):
                    break
                parts.append(nxt)
            note = " ".join(parts).strip()
            break

    return {
        "fetch_status": "ok",
        "source_timestamp": stamp.replace(tzinfo=None).isoformat(),
        "source_timestamp_utc": iso_z(stamp),
        "inventory_mcf": int(end),
        "inventory_delta_mcf": int(end - begin),
        "storage_design_mcf": int(design_volume),
        "inventory_pct_of_design": round(end / design_volume * 100, 1),
        "withdrawal_design_mcfd": int(wd_design),
        "withdrawal_operating_mcfd": int(wd_op),
        "withdrawal_available_mcfd": int(wd_av),
        "withdrawal_restriction_mcfd": int(wd_res),
        "injection_design_mcfd": int(inj_design),
        "injection_operating_mcfd": int(inj_op),
        "injection_available_mcfd": int(inj_av),
        # Available is operating less nominations, so the difference is the
        # nominated injection actually in progress for the day.
        "injection_in_progress_mcfd": int(inj_op - inj_av),
        "injection_restriction_mcfd": int(inj_res),
        "operational_note": note,
    }


# ------------------------------------------------------------------ forecast

def parse_forecast(payload, model):
    props = json.loads(payload)["properties"]
    by_day = collections.defaultdict(list)
    for period in props["periods"]:
        unit = period.get("temperatureUnit")
        if unit != "F":
            raise ValueError(
                f"NWS changed units, expected F and got {unit!r}. Degree days "
                f"computed on Celsius would be silently wrong."
            )
        # startTime carries the Alaska offset, so the first ten characters are
        # already the Alaska local date.
        by_day[period["startTime"][:10]].append(period["temperature"])

    out = []
    for day in sorted(by_day):
        temps = by_day[day]
        if len(temps) < MIN_HOURS_PER_DAY:
            continue
        mean = sum(temps) / len(temps)
        hdd = round(max(0.0, model["hdd_base_f"] - mean), 1)
        out.append({
            "date": day,
            "hours": len(temps),
            "mean_temp_f": round(mean, 1),
            "min_temp_f": min(temps),
            "hdd65": hdd,
            "modeled_demand_mmcfd": demand(hdd, model),
        })
    if not out:
        raise ValueError("NWS returned no complete forecast days")
    return out, props.get("updateTime")


def parse_acis_hdd(payload):
    rows = json.loads(payload).get("data", [])
    if rows and rows[0][1] not in ("M", "T", "", None):
        return float(rows[0][1])
    return None


# ------------------------------------------------------------------ model

def demand(hdd, model):
    """Modeled regional demand in MMcf/d at the given heating degree day count."""
    return round(demand_exact(hdd, model))


def demand_exact(hdd, model):
    """Unrounded demand. Use this wherever a figure is rounded once at the end.

    Rounding twice is how a published number drifts from the one a reader
    reproduces from the formula, so intermediate steps stay exact.
    """
    return model["base_mmcfd"] + model["slope_mmcfd_per_hdd"] * hdd


def backtest_facts(model, series):
    """Recompute every published calibration figure from the committed record.

    Nothing here is typed. config/gaswatch_model.json records what these
    should come out as, and the self-test fails when code and config disagree,
    which is what stops a figure nobody computed from reaching the page.
    """
    anchors = model.get("calibration_anchors", {})
    design_day = anchors.get("published_design_day_mmcfd")
    facts = {}

    hdd_anchor = anchors.get("published_design_day_hdd65")
    if hdd_anchor is not None:
        facts["published-design-day"] = {
            "mmcfd": round(demand_exact(hdd_anchor, model), 2),
        }

    if series:
        peak_date, peak_hdd = max(series, key=lambda r: (r[1], r[0]))
        over = sum(1 for _, v in series
                   if design_day is not None
                   and demand_exact(v, model) >= design_day)
        facts["record-maximum-day"] = {
            "date": peak_date,
            # Degree days are whole numbers in the record, so keep them
            # whole. 77.0 on a published page is machine spill.
            "hdd65": int(peak_hdd) if float(peak_hdd).is_integer() else peak_hdd,
            "mmcfd": round(demand_exact(peak_hdd, model), 1),
            "days_at_or_above_design_day": over,
        }

        mean_hdd = sum(v for _, v in series) / len(series)
        facts["record-average-day"] = {
            "mean_hdd65": round(mean_hdd, 1),
            "mmcfd": round(demand_exact(mean_hdd, model), 1),
        }

    for bt in model.get("backtests", []):
        if bt["id"] != "season-integral":
            continue
        lo, hi = bt["input"]["start"], bt["input"]["end"]
        window = [v for d, v in series if lo <= d <= hi]
        if window:
            facts["season-integral"] = {
                "days": len(window),
                "season_hdd65": sum(window),
                "bcf": round(sum(demand_exact(v, model) for v in window) / 1000.0, 1),
            }
    return facts


def load_model(path):
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    for key in ("version", "base_mmcfd", "slope_mmcfd_per_hdd", "hdd_base_f"):
        if key not in cfg:
            raise ValueError(f"{path} is missing required key {key!r}")
    return cfg


def load_hdd_history(model, base_dir=REPO):
    """The committed Anchorage HDD record, as an ordered list of (date, hdd).

    Stored as a start date plus one integer per day, because the series was
    verified contiguous with no missing values at fetch time. That is a fifth
    the size of dated pairs and it makes a gap impossible to represent, which
    is the right shape for something every published calibration figure is
    recomputed from.
    """
    rel = model.get("hdd_history")
    if not rel:
        raise ValueError("model config names no hdd_history file")
    with open(os.path.join(base_dir, rel), encoding="utf-8") as fh:
        hist = json.load(fh)
    start = datetime.fromisoformat(hist["start_date"]).date()
    series = [((start + timedelta(days=i)).isoformat(), float(v))
              for i, v in enumerate(hist["daily"])]
    if len(series) != hist["days"] or series[-1][0] != hist["end_date"]:
        raise ValueError(
            f"{rel} is inconsistent, {len(series)} days computed against "
            f"{hist['days']} declared, ending {series[-1][0]} against "
            f"{hist['end_date']} declared")
    return hist, series


def model_block(cfg):
    """The model stamped into every record, so a record is self describing."""
    keep = ("version", "formula", "base_mmcfd", "slope_mmcfd_per_hdd",
            "hdd_base_f", "calibration", "fit_source", "measured", "modeled",
            "not_public", "mass_balance")
    return {k: cfg[k] for k in keep if k in cfg}


# ------------------------------------------------------------------ ledger

def read_ledger(path):
    if not os.path.exists(path):
        return []
    records = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path} line {lineno} is not valid JSON, {exc}")
    return records


def standing(records, date):
    """The record that currently stands for a date, or None.

    Lines are append only and never rewritten, so when a repair line follows an
    unverified line for the same date, the last one wins.
    """
    found = None
    for rec in records:
        if rec.get("date") == date:
            found = rec
    return found


def forecast_hdd_for(records, date):
    """What the most recent earlier record predicted for this date."""
    for rec in reversed(records):
        if rec.get("date", "") >= date:
            continue
        for day in rec.get("forecast") or []:
            if day.get("date") == date:
                return day.get("hdd65")
    return None


def append_record(path, record):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, separators=(",", ":"), sort_keys=False) + "\n")


# ------------------------------------------------------------------ build

def reconcile(records, recon_date, actual_hdd, model):
    """Yesterday's forecast against yesterday's weather, and the mass balance.

    D = P + W, so P = D - W. D is modeled from the observed degree days and W is
    the measured CINGSA inventory draw for that same day, which means non CINGSA
    supply falls out as a derived daily number. Strictly what comes out is field
    production plus any Hilcorp storage draw combined, which is why the field is
    never called production.

    It resolves one day in arrears because observed HDD is not available until
    the day is over. That lag is the honest version. Running the balance against
    a forecast would put a modeled number on both sides.
    """
    block = {
        "date": recon_date,
        "forecast_hdd65": forecast_hdd_for(records, recon_date),
        "actual_hdd65": actual_hdd,
        "error": None,
        "modeled_demand_mmcfd": None,
        "storage_withdrawal_mmcfd": None,
        "non_cingsa_supply_mmcfd": None,
        "basis": "observed HDD from ACIS PANC, measured inventory draw from the "
                 "CINGSA record committed for that date",
    }
    if block["forecast_hdd65"] is not None and actual_hdd is not None:
        block["error"] = round(block["forecast_hdd65"] - actual_hdd, 1)
    if actual_hdd is None:
        return block

    block["modeled_demand_mmcfd"] = demand(actual_hdd, model)
    prior = standing(records, recon_date)
    if not prior or not prior.get("verified"):
        return block
    delta = (prior.get("cingsa") or {}).get("inventory_delta_mcf")
    if delta is None:
        return block

    # A negative inventory delta is a draw, which is a positive withdrawal.
    withdrawal = round(-delta / 1000.0, 1)
    block["storage_withdrawal_mmcfd"] = withdrawal
    block["non_cingsa_supply_mmcfd"] = round(
        block["modeled_demand_mmcfd"] - withdrawal, 1)
    return block


def build_record(model, records, now, ak_today):
    """Fetch everything, derive everything, return the record and its probes."""
    probes = []
    flags = []

    cingsa_probe = Probe("cingsa_dashboard", CINGSA_URL)
    probes.append(cingsa_probe)
    cingsa = None
    stale = False
    try:
        cingsa = parse_cingsa(http(cingsa_probe))
        age = now - datetime.fromisoformat(cingsa["source_timestamp_utc"].replace("Z", "+00:00"))
        cingsa["source_age_hours"] = round(age.total_seconds() / 3600, 1)
        stale = age > timedelta(hours=STALE_HOURS)
    except Exception as exc:
        if cingsa_probe.status == "ok":
            # The fetch worked and the parse did not, which means the layout
            # moved. Report the failure rather than guessing at positions.
            cingsa_probe.status = "parse_failed"
            cingsa_probe.error = f"{type(exc).__name__}: {exc}"
        cingsa = {
            "fetch_status": cingsa_probe.status,
            "error": cingsa_probe.error,
            "source_timestamp": None,
        }

    verified = cingsa["fetch_status"] == "ok" and not stale
    if cingsa["fetch_status"] != "ok":
        flags.append("cingsa_fetch_failed")
    if stale:
        flags.append("cingsa_stale")

    # The record is keyed to the CINGSA nomination day it describes, so the
    # evening run and the following morning's retry resolve to the same day and
    # the idempotency check can see them as one. With no usable stamp there is
    # no nomination day to key to, so an unverified record falls back to the
    # Alaska date it was collected on.
    if verified:
        date = cingsa["source_timestamp"][:10]
    else:
        date = ak_today

    return date, cingsa, verified, stale, flags, probes


def finish_record(date, cingsa, verified, flags, probes, model, records, now):
    forecast, forecast_updated = [], None
    fc_probe = Probe("nws_hourly_forecast", NWS_HOURLY)
    probes.append(fc_probe)
    try:
        forecast, forecast_updated = parse_forecast(http(fc_probe), model)
    except Exception as exc:
        if fc_probe.status == "ok":
            fc_probe.status = "parse_failed"
            fc_probe.error = f"{type(exc).__name__}: {exc}"

    recon_date = (datetime.fromisoformat(date) - timedelta(days=1)).strftime("%Y-%m-%d")
    acis_probe = Probe("acis_panc_hdd", ACIS_URL, method="POST")
    probes.append(acis_probe)
    actual_hdd = None
    try:
        body = json.dumps({
            "sid": "PANC", "sdate": recon_date, "edate": recon_date,
            "elems": [{"name": "hdd", "interval": "dly",
                       "base": model["hdd_base_f"]}],
        }).encode("utf-8")
        actual_hdd = parse_acis_hdd(
            http(acis_probe, data=body,
                 headers={"Content-Type": "application/json"}))
    except Exception as exc:
        if acis_probe.status == "ok":
            acis_probe.status = "parse_failed"
            acis_probe.error = f"{type(acis_probe.error or exc).__name__}: {exc}"

    derived = {
        "peak_forecast_date": None,
        "peak_forecast_hdd": None,
        "peak_modeled_demand_mmcfd": None,
        "forecast_window_demand_bcf": None,
        "storage_withdrawal_mmcfd": None,
        "non_cingsa_supply_mmcfd": None,
        "days_cover_at_peak": None,
        "days_cover_note": "Inventory divided by modeled peak demand. It is "
                           "arithmetic on storage alone and takes no account of "
                           "the withdrawal capacity ceiling, field supply, or "
                           "deliverability. It is not a measure of adequacy.",
    }

    if forecast:
        peak = max(forecast, key=lambda d: d["hdd65"])
        derived["peak_forecast_date"] = peak["date"]
        derived["peak_forecast_hdd"] = peak["hdd65"]
        derived["peak_modeled_demand_mmcfd"] = peak["modeled_demand_mmcfd"]
        derived["forecast_window_demand_bcf"] = round(
            sum(d["modeled_demand_mmcfd"] for d in forecast) / 1000.0, 2)
        if peak["hdd65"] >= SUSTAINED_COLD_HDD:
            flags.append("sustained_cold_in_forecast")
        if peak["modeled_demand_mmcfd"] >= DESIGN_DAY_APPROACH_MMCFD:
            flags.append("demand_approaching_design_day")

    if cingsa.get("fetch_status") == "ok":
        if cingsa["withdrawal_restriction_mcfd"] > 0:
            flags.append("withdrawal_restriction_active")
        if cingsa["injection_restriction_mcfd"] > 0:
            flags.append("injection_restriction_active")
        if cingsa["inventory_delta_mcf"] < 0:
            flags.append("inventory_declined")
        derived["storage_withdrawal_mmcfd"] = round(
            -cingsa["inventory_delta_mcf"] / 1000.0, 1)
        if derived["peak_modeled_demand_mmcfd"]:
            derived["days_cover_at_peak"] = round(
                (cingsa["inventory_mcf"] / 1000.0)
                / derived["peak_modeled_demand_mmcfd"], 1)

    # non_cingsa_supply stays null on the collection day by design. The balance
    # needs observed degree days, and today's are not observed yet. It resolves
    # in the reconciliation block one day later.

    record = {
        "date": date,
        "collected_utc": iso_z(now),
        "collector_version": COLLECTOR_VERSION,
        "verified": verified,
        "cingsa": cingsa,
        "forecast": forecast,
        "forecast_source_updated": forecast_updated,
        "derived": derived,
        "reconciliation": reconcile(records, recon_date, actual_hdd, model),
        "model": model_block(model),
        "sources": [p.as_dict() for p in probes],
        "flags": sorted(set(flags)),
    }
    return record


# ------------------------------------------------------------------ self test

# A trimmed copy of the dashboard's real markup carrying the snapshot verified
# on 2026-08-03, which is the reading the build brief independently states. The
# fixture keeps the page's mixed formatting on purpose, one row broken across
# four lines and the rest inline, because a parser that only handles the tidy
# rows would pass a tidied fixture and fail the live page.
FIXTURE = """
<table><tr>
<td class="page_title"><h1>CINGSA Dashboard</h1></td>
<td class="date"><div>Last Updated:</div><span>08/03/2026 21:00</span></td>
</tr></table>
<table class="data_table">
<tr><th class="column_title">Injection (MCFpd)</th><th>&nbsp;</th>
<th class="column_title">Withdrawal (MCFpd)</th></tr>
<tr class="data_tabletr">
    <td class="row_item">Design Capacity</td>
    <td class="data_item">225,000</td>
    <td></td>
    <td class="data_item">215,000</td>
</tr>
<tr class="data_tabletr"><td class="row_item">Maximum Contracted Capacity</td><td class="data_item">225,000</td><td></td><td class="data_item">215,000</td></tr>
<tr class="data_tabletr"><td class="row_item">Facility Capacity</td><td class="data_item">206,320</td><td></td><td class="data_item">132,117</td></tr>
<tr class="data_tabletr"><td class="row_item">Physical Restrictions</td><td class="data_item">0</td><td></td><td class="data_item">0</td></tr>
<tr class="data_tabletr"><td class="row_item">Operating Capacity</td><td class="data_item">206,320</td><td></td><td class="data_item">132,117</td></tr>
<tr class="data_tabletr"><td class="row_item">Available Capacity</td><td class="data_item">171,428</td><td></td><td class="data_item">132,117</td></tr>
</table>
<table class="data_table">
<tr><th class="column_title">Storage Volume (Mcf)</th></tr>
<tr class="data_tabletr"><td class="row_item">Design Capacity</td><td class="data_item">13,000,000</td></tr>
<tr class="data_tabletr"><td class="row_item">Maximum Contracted Capacity</td><td class="data_item">13,000,000</td></tr>
<tr class="data_tabletr"><td class="row_item">Beginning Inventory</td><td class="data_item">6,388,680</td></tr>
<tr class="data_tabletr"><td class="row_item">Ending Inventory</td><td class="data_item">6,423,571</td></tr>
<tr class="data_tabletr"><td class="row_item">Available Inventory</td><td class="data_item">6,576,429</td></tr>
</table>
<div>Operational Notes</div><div>CINGSA will be performing required semiannual
shut-in field balance &amp; maintenance from 14 Sept. 2026 until 21 Sept. 2026.
No nominations will be accepted during this time.</div>
<div>NOTE TO USER: This data is provided informationally.</div>
"""


def self_test(model_path):
    """Hermetic gate. No network, no ledger, run before anything is written.

    Two halves. The model half proves the coefficients in config still produce
    the backtests they claim, so a refit that fat fingers a number goes red on
    the commit that made it. The parser half proves the dashboard reader still
    returns the snapshot the brief independently verified, and, just as
    important, that it goes red when the page moves under it. A gate that cannot
    fail certifies nothing.
    """
    model = load_model(model_path)
    failures = []

    def check(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not ok:
            failures.append(label)

    print("model backtests, every figure recomputed from the committed record")
    hist, series = load_hdd_history(model)
    anchors = model.get("calibration_anchors", {})
    facts = backtest_facts(model, series)
    check("the HDD record is contiguous and complete",
          len(series) == hist["days"],
          f"{len(series)} days, {hist['start_date']} to {hist['end_date']}")

    for bt in model.get("backtests", []):
        bid = bt["id"]
        got = facts.get(bid)
        if got is None:
            check(f"backtest {bid} is one this code knows how to recompute",
                  False, "no recomputation defined")
            continue
        for key, want in sorted(bt.items()):
            if not key.startswith("expect_"):
                continue
            field = key[len("expect_"):]
            have = got.get(field)
            check(f"{bid}, {field.replace('_', ' ')} recomputes",
                  have == want, f"code gives {have}, config records {want}")
        anchor = bt.get("compare_to_anchor")
        if anchor:
            unit = "bcf" if "tolerance_bcf" in bt else "mmcfd"
            tol = bt.get(f"tolerance_{unit}")
            mine = got.get("bcf" if unit == "bcf" else "mmcfd")
            check(f"{bid} sits within tolerance of {anchor}",
                  abs(mine - anchors[anchor]) <= tol,
                  f"{mine} against published {anchors[anchor]}, tolerance {tol}")

    print("dashboard parser")
    parsed = parse_cingsa(FIXTURE)
    expected = {
        "inventory_mcf": 6423571,
        "inventory_delta_mcf": 34891,
        "inventory_pct_of_design": 49.4,
        "withdrawal_operating_mcfd": 132117,
        "withdrawal_restriction_mcfd": 0,
        "injection_operating_mcfd": 206320,
        "injection_in_progress_mcfd": 34892,
        "storage_design_mcf": 13000000,
    }
    for key, want in expected.items():
        check(f"parses {key}", parsed.get(key) == want,
              f"got {parsed.get(key)}, expected {want}")

    # The specific trap. Design Capacity and Maximum Contracted Capacity each
    # appear in both tables, one a rate and one a volume. A parser that takes
    # the first match reads 13,000,000 Mcf as an injection rate, or 225,000
    # Mcf/d as the storage design volume. Both directions are checked.
    check("keeps the two Design Capacity rows apart",
          parsed["injection_design_mcfd"] == 225000
          and parsed["storage_design_mcf"] == 13000000,
          f"injection {parsed['injection_design_mcfd']} Mcf/d, "
          f"storage {parsed['storage_design_mcf']} Mcf")
    check("reads the Alaska stamp",
          parsed["source_timestamp"] == "2026-08-03T21:00:00",
          parsed["source_timestamp"])
    check("keeps the operational note and drops the boilerplate",
          "semiannual shut-in" in parsed["operational_note"]
          and "NOTE TO USER" not in parsed["operational_note"],
          parsed["operational_note"][:60])

    print("the gate can still go red")
    broken = [
        ("missing row",
         FIXTURE.replace(
             '<tr class="data_tabletr"><td class="row_item">Ending Inventory</td>'
             '<td class="data_item">6,423,571</td></tr>', "")),
        ("missing stamp", FIXTURE.replace("Last Updated:", "Refreshed")),
        ("missing storage heading", FIXTURE.replace("Storage Volume (Mcf)", "Volumes")),
        # A unit change is the one mutation where every structural check still
        # passes and every number is wrong by a factor of a thousand.
        ("storage restated in MMcf, which parses but means something else",
         FIXTURE.replace("13,000,000", "13,000").replace("6,423,571", "6,424")
                .replace("6,388,680", "6,389")),
        ("deliverability restated in MMcf/d",
         FIXTURE.replace("132,117", "132").replace("206,320", "206")),
        ("rows shuffled so the published identity breaks",
         FIXTURE.replace('<td class="data_item">206,320</td><td></td>'
                         '<td class="data_item">132,117</td></tr>\n'
                         '<tr class="data_tabletr"><td class="row_item">Physical Restrictions</td>'
                         '<td class="data_item">0</td><td></td><td class="data_item">0</td></tr>',
                         '<td class="data_item">206,320</td><td></td>'
                         '<td class="data_item">132,117</td></tr>\n'
                         '<tr class="data_tabletr"><td class="row_item">Physical Restrictions</td>'
                         '<td class="data_item">9,000</td><td></td>'
                         '<td class="data_item">9,000</td></tr>')),
    ]
    for label, mutated in broken:
        try:
            parse_cingsa(mutated)
            check(f"rejects a layout change, {label}", False, "parsed anyway")
        except ValueError:
            check(f"rejects a layout change, {label}", True)

    print("forecast guards")
    celsius = json.dumps({"properties": {"periods": [
        {"startTime": "2026-08-05T06:00:00-08:00", "temperature": 14,
         "temperatureUnit": "C"}]}})
    try:
        parse_forecast(celsius, model)
        check("rejects a units switch on the forecast", False, "parsed anyway")
    except ValueError:
        check("rejects a units switch on the forecast", True)

    partial = json.dumps({"properties": {"periods": [
        {"startTime": f"2026-08-05T{h:02d}:00:00-08:00", "temperature": 50,
         "temperatureUnit": "F"} for h in range(4)]}})
    try:
        parse_forecast(partial, model)
        check("drops a partial forecast day", False, "kept it")
    except ValueError:
        check("drops a partial forecast day", True)

    full = json.dumps({"properties": {"periods": [
        {"startTime": f"2026-08-05T{h:02d}:00:00-08:00", "temperature": 45,
         "temperatureUnit": "F"} for h in range(24)]}})
    days, _ = parse_forecast(full, model)
    check("a full day models demand from its own mean",
          days[0]["hdd65"] == 20.0 and days[0]["modeled_demand_mmcfd"] == demand(20.0, model),
          f"HDD {days[0]['hdd65']} gives {days[0]['modeled_demand_mmcfd']} MMcf/d")

    print()
    if failures:
        print(f"self-test FAILED, {len(failures)} check(s) red")
        return 1
    print("self-test clean")
    return 0


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description="Cook Inlet Gas Watch daily collector")
    ap.add_argument("--ledger", default=LEDGER,
                    help="JSONL to append to, default ledger/gaswatch.jsonl")
    ap.add_argument("--model", default=MODEL_CONFIG,
                    help="model coefficients, default config/gaswatch_model.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="fetch and print the record, write nothing")
    ap.add_argument("--self-test", action="store_true",
                    help="hermetic model and parser checks, no network")
    args = ap.parse_args()

    if args.self_test:
        return self_test(args.model)

    model = load_model(args.model)
    records = read_ledger(args.ledger)
    now = now_utc()
    ak_today = now.astimezone(alaska_tz()).strftime("%Y-%m-%d")

    date, cingsa, verified, stale, flags, probes = build_record(
        model, records, now, ak_today)

    # Idempotency, before the remaining fetches so a retry costs one request.
    # A verified record for the day is final and a second run does nothing. An
    # unverified one may be repaired exactly once, by a later run that actually
    # got the number, because a transient CDN failure at 23:20 must not cost the
    # day permanently. Nothing already written is ever rewritten or reordered.
    prior = standing(records, date)
    if prior is not None:
        if prior.get("verified"):
            print(f"{date} already has a verified record, nothing to do.")
            return 0
        if not verified:
            print(f"{date} already has an unverified record and this attempt "
                  f"also failed. Not stacking a second failure.")
            for probe in probes:
                if probe.status != "ok":
                    print(f"  {probe.name}, {probe.status}, {probe.error}")
            return 3

    record = finish_record(date, cingsa, verified, flags, probes, model,
                           records, now)
    if prior is not None:
        record["supersedes_unverified"] = prior.get("collected_utc")

    if args.dry_run:
        print(json.dumps(record, indent=2))
        return 0 if verified else 2

    append_record(args.ledger, record)

    cin, der = record["cingsa"], record["derived"]
    print(f"{record['date']}  {'verified' if verified else 'UNVERIFIED'}")
    if cin.get("fetch_status") == "ok":
        print(f"  CINGSA {cin['source_timestamp']} "
              f"({cin.get('source_age_hours')}h old)  "
              f"{cin['inventory_mcf'] / 1e6:.2f} Bcf "
              f"({cin['inventory_pct_of_design']} percent of design)  "
              f"withdrawal capacity "
              f"{cin['withdrawal_operating_mcfd'] / 1000:.0f} MMcf/d")
    else:
        print(f"  CINGSA {cin.get('fetch_status')}, {cin.get('error')}")
    if der["peak_forecast_date"]:
        print(f"  peak {der['peak_forecast_date']} HDD "
              f"{der['peak_forecast_hdd']} gives "
              f"{der['peak_modeled_demand_mmcfd']} MMcf/d modeled")
    rec = record["reconciliation"]
    if rec["non_cingsa_supply_mmcfd"] is not None:
        print(f"  {rec['date']} balance, demand "
              f"{rec['modeled_demand_mmcfd']} less storage "
              f"{rec['storage_withdrawal_mmcfd']} gives non CINGSA supply "
              f"{rec['non_cingsa_supply_mmcfd']} MMcf/d")
    print(f"  flags {', '.join(record['flags']) or 'none'}")

    if not verified:
        print("  record written UNVERIFIED. No number was carried forward.",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
