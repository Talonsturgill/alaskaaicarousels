#!/usr/bin/env python3
"""gaswatch_build.py, the shared library behind the Cook Inlet Gas Watch page.

scripts/site_build.py is an assembler. Reading the series, deriving every
displayed figure, drawing the chart, and building the page components live
here, the same way scripts/docket_build.py carries that load for the docket.

THE RULE THIS FILE EXISTS TO ENFORCE. Not one numeral on the published page is
typed by a human or a language model. Every figure is computed in figures()
from the committed record and interpolated at build time, and numeral_lint()
fails the build if a number appears on the page that does not trace back to the
data that produced it. Maintainer's instruction, 2026-08-05, and the reason is
sound. A model writing "storage sits near half of design" into prose is exactly
how a wrong number ships, and prose drifts from data silently.

The page never publishes a safety verdict. Not a shortfall prediction, not an
all clear. It publishes measured storage, modeled demand, the derived residual,
and the size of what is not public. See CLAUDE.md, hard rules.

Run:
  python3 scripts/gaswatch_build.py --self-test
"""

import argparse
import html as _html
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gaswatch_collect as gc  # noqa: E402  the model and its arithmetic live there

LEDGER = os.path.join(REPO, "ledger", "gaswatch.jsonl")
MODEL_CONFIG = os.path.join(REPO, "config", "gaswatch_model.json")

SCHEMA_VERSION = "1.0"

# How many days the day by day table shows. Read by display_numerals too, since
# the caption counts the rows it renders rather than the whole series.
TABLE_LIMIT = 14

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def esc(s):
    return _html.escape(str(s), quote=True)


def ordinal(n):
    """House style takes the ordinal, month first. August 10th, never 10 August."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def long_month(ym):
    """EIA stamps months as 202605. A reader wants May 2026."""
    return f"{MONTHS[int(ym[4:6]) - 1]} {ym[:4]}"


def short_date(iso):
    """Aug 6th. The axis has no room for the full form and the house rule is
    about the ordinal and the order, not the length of the month name."""
    d = date.fromisoformat(iso)
    return f"{MONTHS[d.month - 1][:3]} {ordinal(d.day)}"


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{MONTHS[d.month - 1]} {ordinal(d.day)}, {d.year}"


# ------------------------------------------------------------------ reader

def load_series(path=LEDGER):
    """Every date's standing record, oldest first.

    Lines are append only, so a repair line for a date follows the unverified
    line it replaces. Last write wins per date, which is the same resolution
    gaswatch_collect.standing() applies, kept consistent on purpose so the page
    and the collector never disagree about which line counts.
    """
    if not os.path.exists(path):
        return []
    by_date = {}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"{path} line {lineno} is not valid JSON, {exc}")
            by_date[rec["date"]] = rec
    return [by_date[d] for d in sorted(by_date)]


def latest_verified(series):
    for rec in reversed(series):
        if rec.get("verified"):
            return rec
    return None


def continuity(series):
    """Missing calendar days between the first and last record."""
    if len(series) < 2:
        return []
    have = {r["date"] for r in series}
    first = date.fromisoformat(series[0]["date"])
    last = date.fromisoformat(series[-1]["date"])
    out, cur = [], first
    while cur <= last:
        if cur.isoformat() not in have:
            out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


# ------------------------------------------------------------------ figures

def figures(series, model, figs=None):
    """Every number the page displays, computed once, in one place.

    Pass `figs` to reuse a dict a caller already built. A whole site build
    computed this four times and reparsed the 4,599 day weather record nine
    times, because home_strip, page_body, feed and site_build each asked
    independently for the same answer from the same two inputs.

    If a figure is not in this dict it does not go on the page. That is what
    makes numeral_lint() able to prove the page carries nothing invented.
    """
    if figs is not None:
        return figs
    hist, hdd_series = gc.load_hdd_history(model, REPO)
    facts = gc.backtest_facts(model, hdd_series)
    anchors = model.get("calibration_anchors", {})

    verified = [r for r in series if r.get("verified")]
    latest = latest_verified(series)

    f = {
        "days_of_record": len(series),
        "verified_days": len(verified),
        "unverified_days": len(series) - len(verified),
        "missing_days": len(continuity(series)),
        "first_date": series[0]["date"] if series else None,
        "last_date": series[-1]["date"] if series else None,
        "model_version": model["version"],
        "schema_version": SCHEMA_VERSION,
        "base_mmcfd": model["base_mmcfd"],
        "slope_mmcfd_per_hdd": model["slope_mmcfd_per_hdd"],
        "hdd_base_f": model["hdd_base_f"],
        "hdd_record_days": hist["days"],
        "hdd_record_start": hist["start_date"],
        "hdd_record_end": hist["end_date"],
        "not_public_count": len(model.get("not_public", [])),
        "fit_months": (model.get("fit") or {}).get("months"),
        "fit_mean_error_pct": (model.get("fit") or {}).get("mean_error_pct"),
        # The first history entry is the original fit, not a revision of
        # anything, so counting it published "3 revisions" for two revisions.
        "model_revisions": max(0, len(model.get("model_history", [])) - 1),
    }

    # The scoreboard for the model itself. Every day the collector records what
    # the forecast said against what the weather did, so the error is measured
    # rather than asserted. These are the numbers that justify a refit, or
    # refuse to. At zero checks they are absent, and the page says so instead
    # of implying an accuracy nobody has earned yet.
    checks = [r.get("reconciliation") or {} for r in series]
    scored = [c for c in checks
              if c.get("forecast_hdd65") is not None and c.get("actual_hdd65") is not None]
    f["accuracy_checks"] = len(scored)
    if scored:
        errs = [abs(c["forecast_hdd65"] - c["actual_hdd65"]) for c in scored]
        f["mean_abs_hdd_error"] = round(sum(errs) / len(errs), 1)
        f["worst_hdd_error"] = round(max(errs), 1)
        # What that error is worth in gas, which is the units a reader cares
        # about. Degree days are the input; MMcf per day is the output.
        f["mean_abs_demand_error_mmcfd"] = round(
            sum(errs) / len(errs) * model["slope_mmcfd_per_hdd"], 1)
    balanced = [c for c in checks if c.get("non_cingsa_supply_mmcfd") is not None]
    f["balance_days"] = len(balanced)
    f.update(eia_crosscheck(model, series))
    f.update({f"anchor_{k}": v for k, v in anchors.items()
              if isinstance(v, (int, float))})
    for bid, vals in facts.items():
        for k, v in vals.items():
            f[f"{bid.replace('-', '_')}_{k}"] = v

    if latest:
        cin = latest["cingsa"]
        der, rec = remodel(latest, model)
        f.update({
            "as_of": latest["date"],
            "inventory_mcf": cin["inventory_mcf"],
            "inventory_bcf": round(cin["inventory_mcf"] / 1_000_000, 2),
            "inventory_pct_of_design": cin["inventory_pct_of_design"],
            "design_mcf": cin["storage_design_mcf"],
            "design_bcf": round(cin["storage_design_mcf"] / 1_000_000, 1),
            "inventory_delta_mcf": cin["inventory_delta_mcf"],
            # The day's movement, which is the whole reason a daily record
            # beats a snapshot. Absolute value here; the direction is a word.
            "inventory_delta_mmcf": round(abs(cin["inventory_delta_mcf"]) / 1000, 1),
            "withdrawal_operating_mmcfd": round(
                cin["withdrawal_operating_mcfd"] / 1000, 1),
            "withdrawal_restriction_mcfd": cin["withdrawal_restriction_mcfd"],
            "injection_in_progress_mmcfd": round(
                cin["injection_in_progress_mcfd"] / 1000, 1),
            "source_timestamp": cin.get("source_timestamp"),
            "peak_forecast_date": der.get("peak_forecast_date"),
            "peak_forecast_hdd": der.get("peak_forecast_hdd"),
            "peak_modeled_demand_mmcfd": der.get("peak_modeled_demand_mmcfd"),
        })
        # How much of a day's supply nothing public measures. This is the size
        # of the hole, stated as a number rather than as an adjective.
        if rec.get("non_cingsa_supply_mmcfd") is not None and rec.get("modeled_demand_mmcfd"):
            f["balance_date"] = rec["date"]
            f["non_cingsa_supply_mmcfd"] = rec["non_cingsa_supply_mmcfd"]
            f["modeled_demand_mmcfd"] = rec["modeled_demand_mmcfd"]
            f["storage_withdrawal_mmcfd"] = rec["storage_withdrawal_mmcfd"]
            f["unmeasured_share_pct"] = round(
                rec["non_cingsa_supply_mmcfd"] / rec["modeled_demand_mmcfd"] * 100, 1)
    # Comparisons are computed for the same reason numerals are. A page that
    # says "a minority" in prose is asserting a fact about two figures, and it
    # would keep saying it after those figures crossed over.
    for key in ("record_average_direction", "record_average_gap_pct",
                "inventory_delta_direction", "residual_regime"):
        try:
            f[key] = _comparison(key, f)
        except KeyError:
            pass
    monthly = model.get("not_public_monthly_source") or {}
    f["not_public_with_monthly_source"] = len(monthly)
    return {k: v for k, v in f.items() if v is not None}


EIA_LEDGER = os.path.join(REPO, "ledger", "gaswatch_eia.json")


def eia_crosscheck(model, series, path=EIA_LEDGER):
    """The monthly external check, recomputed here rather than stored.

    Two things the project could not do before. The demand model gets compared
    against observed Alaska deliveries to residential, commercial and electric
    power consumers, and storage outside CINGSA falls out of Alaska statewide
    working gas less the volume this page measures daily.

    Every figure is computed from the committed EIA file and the committed HDD
    record, so the same no-typed-numeral rule covers it.
    """
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        eia = json.load(fh)
    s = eia.get("series") or {}
    month = eia.get("latest_month")
    if not month or not s:
        return {}

    _, hdd_series = gc.load_hdd_history(model, REPO)
    by_month = {}
    for d, v in hdd_series:
        by_month.setdefault(d[:4] + d[5:7], []).append(v)

    sectors = ("residential_mmcf", "commercial_mmcf", "electric_power_mmcf")
    pairs = []
    for ym, days in sorted(by_month.items()):
        # Every sector must be present. Summing with a zero default counted a
        # month that had two sectors of three as though the third were zero,
        # which quietly dragged the published ratio. EIA genuinely publishes
        # sectors at different times, so this is the ordinary case, not an edge.
        if not all(ym in s.get(k, {}) for k in sectors):
            continue
        # Only whole months. A partial month of degree days against a full
        # month of deliveries would read as the model running light. Calendar
        # length, not a flat 28, since the record grows by being extended mid
        # month and its trailing month is therefore always short.
        if not gc.is_whole_month(ym, len(days)):
            continue
        pairs.append((sum(gc.demand_exact(v, model) for v in days),
                      sum(s[k][ym] for k in sectors)))
    if not pairs:
        return {}
    modeled = sum(p[0] for p in pairs)
    observed = sum(p[1] for p in pairs)

    out = {
        "eia_latest_month": month,
        "eia_months_checked": len(pairs),
        "eia_model_ratio": round(modeled / observed, 2),
        "eia_model_gap_pct": round(abs(modeled / observed - 1) * 100),
        "eia_model_runs": "high" if modeled > observed else "low",
    }
    # The storage figures come from Form EIA-191, which can lag the delivery
    # series that sets latest_month. Missing months are absent rather than
    # fatal, so a normal reporting lead cannot take the whole site build down.
    storage = {
        "eia_ak_working_gas_bcf": ("ak_working_gas_mmcf", 1000, 1),
        "eia_ak_capacity_bcf": ("ak_working_gas_capacity_mmcf", 1000, 1),
        "eia_storage_fields": ("ak_storage_field_count", 1, 0),
    }
    for key, (sid, div, places) in storage.items():
        val = s.get(sid, {}).get(month)
        if val is not None:
            out[key] = round(val / div, places) if div != 1 else val
    # Storage outside CINGSA needs a CINGSA reading in the same month EIA
    # reports. Until the daily record is old enough to overlap, this stays
    # absent rather than differencing two different months.
    same_month = [r for r in series if r.get("verified")
                  and r["date"][:4] + r["date"][5:7] == month]
    # Both halves have to be present. EIA-191 storage lags the delivery series
    # that sets latest_month, which the loop above already allows for, so this
    # differenced a figure against a key that was legitimately absent.
    if same_month and "eia_ak_working_gas_bcf" in out:
        cingsa_bcf = same_month[-1]["cingsa"]["inventory_mcf"] / 1_000_000
        out["eia_non_cingsa_storage_bcf"] = round(
            out["eia_ak_working_gas_bcf"] - cingsa_bcf, 1)
    return out


NUMERAL_RE = r"\d[\d,]*(?:\.\d+)?"


def tokens(blob):
    """Numerals as the lint sees them, so both sides never disagree.

    The allowed set was built by hand-formatting values while the lint used a
    regex, and the two drifted apart on the first negative figure. A residual
    of -16.5 was authorised as "-16.5" and read off the page as "16.5", since
    the pattern does not take the sign. One tokenizer, used by both.
    """
    return {t.replace(",", "").rstrip(".") for t in re.findall(NUMERAL_RE, blob)}


def display_numerals(series, model):
    """What the day by day table and the chart legitimately render.

    figures() covers the latest reading, which WAS every reading on launch day,
    so this gap did not exist for exactly one day and then became fatal. On the
    second reading the table draws a row per day and the chart draws an axis,
    carrying storage figures and tick values figures() never produced. The lint
    would have called them invented and site_build calls that a hard fail, so
    the nightly rebuild would have died and taken the commit step with it,
    stranding the day's collection uncommitted. CINGSA keeps no archive, so that
    day would have been gone.

    Every value here comes from the same transformation the renderer applies to
    the same record, so a numeral is still authorised by data and never by a
    literal typed in to silence a complaint.
    """
    rendered = []
    rows = [r for r in series
            if r.get("verified") and (r.get("cingsa") or {}).get("inventory_mcf")]
    for r in rows:
        cin = r["cingsa"]
        der, rec = remodel(r, model)
        # The date column too. figures() carries the first and last date, so
        # every date between them was unauthorised the moment the series grew a
        # middle. Both renderings, the ISO the table prints and the long form
        # prose and captions use.
        rendered += [r["date"], long_date(r["date"])]
        for v in (round(cin["inventory_mcf"] / 1_000_000, 2),
                  cin["inventory_pct_of_design"],
                  der.get("peak_modeled_demand_mmcfd"),
                  rec.get("non_cingsa_supply_mmcfd")):
            # Both renderings of the same value. A table cell prints a float
            # straight, so round(x, 1) reaches a reader as "112.0", while the
            # chart formats with :g and the same value reads "112".
            if v is not None:
                rendered += [str(v), f"{v:g}"]
    # The axis and the chart's own values, taken from the same definition the
    # chart draws from. Recomputing them here is how the residual panel's ticks
    # came out unauthorised the moment it was added.
    pts, live = chart_data(series, model)
    for pl in (live or []):
        for t in pl["ticks"]:
            rendered += [f"{t:g}", str(t)]
        for _i, v in pl["have"]:
            rendered += [f"{v:g}", str(v)]
    for pt in (pts or []):
        rendered += [pt[0], long_date(pt[0]), short_date(pt[0])]

    # The table caption counts the rows it shows, which is not verified_days
    # once the series outgrows the window. It read "14 verified readings" with
    # nothing authorising 14.
    rendered.append(str(min(len(rows), TABLE_LIMIT)))
    return tokens(" ".join(rendered))


def allowed_numerals(figs, model, extra_strings=(), series=()):
    """Every numeral that may legally appear in page prose.

    Built from the data itself, never by adding a literal to silence the lint.
    A number reaches this set only because something computed it.
    """
    # Only computed values and the model's NUMERIC fields. Feeding the whole
    # config in let a number typed into a _spec or note string authorise itself
    # on the page, which is exactly the hand-written figure this lint exists to
    # stop. The season-integral note mentions 71.6, and that was enough to let
    # "Storage sits at 71.6 Bcf" through.
    # Data authorises a numeral; prose does not. Feeding the whole config in
    # let a number typed into a note authorise itself on the page, which is the
    # hand-written figure this lint exists to stop. Filtering to numbers alone
    # was too blunt, since ISO dates in `input` are data too. So the rule is by
    # KEY, and these keys hold sentences.
    PROSE_KEYS = {"_spec", "description", "note", "reason", "purpose",
                  "honesty_note", "refit_procedure", "calibration", "fit_source",
                  "source_stated_label", "identity", "no_typed_numbers_rule",
                  "not_public_note", "limits"}

    def data_only(node):
        if isinstance(node, dict):
            return {k: data_only(v) for k, v in node.items() if k not in PROSE_KEYS}
        if isinstance(node, list):
            return [data_only(v) for v in node]
        return node

    blob = json.dumps([figs, data_only(model), list(extra_strings)])
    # An ISO date in the data renders on the page as "August 5th, 2026", whose
    # day part is "5" and not the zero padded "05" the ISO string carries. The
    # rendered form is still the data, so expand it here rather than letting a
    # date trip a lint aimed at invented figures.
    blob += " ".join(long_date(d) for d in
                     sorted(set(re.findall(r"\d{4}-\d{2}-\d{2}", blob))))
    return tokens(blob) | display_numerals(series, model)


UNDERCLAIMS = ("not fit to observed", "not fitted to observed",
               "calibrated to two published figures", "moves only when a person",
               "only when a person moves it", "working hypothesis",
               "nothing here learns")


def underclaims(model):
    """Prose in the model config that sells the model short of what it is.

    The overclaim guard beside this one has a twin problem nobody thought to
    check for. When the model improved, four strings kept describing the old
    two point calibration, and they ship inside the published feed. One of them
    said the coefficients move only when a person moves them, which stopped
    being true the day the monthly workflow started refitting them.

    A false modesty is still a false claim, and it is the harder one to notice,
    because nothing looks wrong about a page being careful. So it is only an
    error when a fit exists to contradict it, which keeps the rule honest if
    the model is ever deliberately unfitted again.
    """
    if not model.get("fit"):
        return []
    hits = []
    for key, val in (model.get("_spec") or {}).items():
        low = val.lower() if isinstance(val, str) else ""
        hits += [f"_spec.{key}: {w}" for w in UNDERCLAIMS if w in low]
    for key in ("calibration", "fit_source"):
        low = str(model.get(key, "")).lower()
        hits += [f"{key}: {w}" for w in UNDERCLAIMS if w in low]
    return hits


def remodel(rec, model):
    """(derived, reconciliation) recomputed from a record's measured inputs.

    A record stamps the model that produced its numbers. That is what makes the
    ledger auditable and it is why the ledger itself is never rewritten. The
    page is a different promise. It publishes one formula and tells the reader
    every figure traces back to it, so a modeled peak carried over from
    yesterday's coefficients is a number they cannot reproduce from what they
    were just shown. That was live for a day after the first refit.

    Measured values are never touched. Only what the model computed is computed
    again, from the same stored inputs, with the coefficients being published.
    """
    der = dict(rec.get("derived") or {})
    recon = dict(rec.get("reconciliation") or {})
    if der.get("peak_forecast_hdd") is not None:
        der["peak_modeled_demand_mmcfd"] = gc.demand(der["peak_forecast_hdd"], model)
    if recon.get("actual_hdd65") is not None:
        recon["modeled_demand_mmcfd"] = gc.demand(recon["actual_hdd65"], model)
        w = recon.get("storage_withdrawal_mmcfd")
        if w is not None:
            recon["non_cingsa_supply_mmcfd"] = round(
                recon["modeled_demand_mmcfd"] - w, 1)
    return der, recon


def residual_by_day(series, model):
    """Derived non CINGSA supply, keyed by the day it DESCRIBES.

    The balance resolves one day in arrears, because it needs that day's
    observed degree days and a day's weather is only observed once the day is
    over. So the record for August 6th carries the residual FOR August 5th, and
    its reconciliation object says so in its own `date` field. Read straight off
    the record instead, and the one figure nobody else publishes is misdated by
    a day, every day.

    This lives in one place because the same mistake was made twice
    independently, once in the table and once in the chart, and fixed twice in
    parallel. A third reader of this data would have made it a third time.

    Verified is the only filter. A residual needs a reconciliation, not an
    inventory reading, so a record whose storage figure did not come through
    still describes the day before it perfectly well.
    """
    on_day = {}
    for r in series:
        if not r.get("verified"):
            continue
        recon = remodel(r, model)[1]
        if recon.get("date") and recon.get("non_cingsa_supply_mmcfd") is not None:
            on_day[recon["date"]] = recon["non_cingsa_supply_mmcfd"]
    return on_day


def blank(v):
    """A value the model could not produce yet shows as an empty cell.

    Never the word None, which is machine spill, and never a zero, which a
    reader would take for a measurement of nothing."""
    return "" if v is None else v


def _comparison(key, vals):
    """The one place a comparison word is decided, so page and test agree."""
    if key == "cingsa_share_word":
        d, c = vals["design_bcf"], vals["eia_ak_capacity_bcf"]
        return "minority" if d * 2 < c else "majority" if d * 2 > c else "half"
    if key == "record_average_direction":
        return ("light" if vals["record_average_day_mmcfd"]
                < vals["anchor_published_average_day_mmcfd"] else "heavy")
    if key == "inventory_delta_direction":
        d = vals["inventory_delta_mcf"]
        return "into storage" if d > 0 else ("out of storage" if d < 0 else "either way")
    if key == "residual_regime":
        # The residual is demand minus MEASURED storage withdrawal, so on a day
        # the field is filling the withdrawal is negative and the residual comes
        # out ABOVE demand. The ratio is then over one hundred percent, which is
        # correct arithmetic and reads as an error unless the page says why.
        w = vals["storage_withdrawal_mmcfd"]
        return "filling" if w < 0 else ("drawing" if w > 0 else "flat")
    if key == "record_average_gap_pct":
        published = vals["anchor_published_average_day_mmcfd"]
        return round(abs(vals["record_average_day_mmcfd"] - published)
                     / published * 100, 1)
    raise KeyError(key)


def spell(n):
    """Small counts read as words when they open a sentence.

    Derived from the value, never typed, so it still moves with the data.
    """
    words = ["none", "one", "two", "three", "four", "five",
             "six", "seven", "eight", "nine"]
    return words[n].capitalize() if 0 <= n < len(words) else str(n)


def noun(n, singular, plural=None):
    """Just the noun, agreeing with n. For a label that sits beside its number."""
    return singular if n == 1 else (plural or singular + "s")


def count(n, singular, plural=None):
    """A counted noun that agrees with its number. One day, two days."""
    return f"{n} {noun(n, singular, plural)}"


def numeral_lint(page_html, allowed):
    """Numerals in visible prose that trace back to nothing in the data.

    SVG is excluded because chart geometry is pixel coordinates, which are
    computed but meaningless as figures. The chart's own text labels are linted
    separately by passing them through as prose.
    """
    # Keep the chart's text labels, drop its geometry. Stripping the whole SVG
    # meant a typed numeral in an axis or a direct label was never linted, while
    # the docstring claimed those labels were covered.
    def keep_svg_text(m):
        return " ".join(re.findall(r"(?s)<text[^>]*>(.*?)</text>", m.group(0)))

    txt = re.sub(r"(?s)<svg.*?</svg>", keep_svg_text, page_html)
    txt = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", txt)
    txt = re.sub(r"(?s)<!--.*?-->", " ", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _html.unescape(txt)
    bad = []
    for tok in re.findall(NUMERAL_RE, txt):
        if tok.replace(",", "").rstrip(".") not in allowed:
            bad.append(tok)
    return bad


# ------------------------------------------------------------------ chart

def nice_bounds(lo, hi, ticks=4, min_span=0.0):
    """Axis bounds and tick values on round numbers, computed not chosen.

    min_span is the honesty control. Storage moved 6.50 to 6.54 Bcf on the
    first two days of the record, which is three tenths of one percent of a
    13 Bcf field, and an axis fitted to the data drew that as a climb across
    the full height of the panel. A reader saw a mountain where the field had
    barely moved. Given a floor tied to the field itself, a flat record renders
    flat, which is true, and a real winter drawdown fills the panel on its own
    without anyone choosing a range.
    """
    # A span that is flat, or so narrow it is flat relative to its own
    # magnitude, cannot produce a readable axis and rounds badly besides.
    # Storage barely moves day to day, so this is the ordinary case early in
    # the series, not an exotic one.
    if hi - lo <= max(abs(lo), abs(hi), 1.0) * 1e-4:
        hi = lo + max(abs(lo) * 0.01, 1.0)
    if min_span and hi - lo < min_span:
        mid = (lo + hi) / 2.0
        lo, hi = mid - min_span / 2.0, mid + min_span / 2.0
    span = hi - lo
    raw = span / max(1, ticks)
    mag = 10 ** int(f"{raw:e}".split("e")[1])
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    start = step * int(lo / step) if lo >= 0 else step * (int(lo / step) - 1)
    # Walk until the last tick is at or above hi. Stopping at the last tick
    # below hi is how a data point ends up drawn above the top gridline, which
    # is what the self-test caught the first time this was written.
    vals, v = [], start
    while True:
        vals.append(round(v, 6))
        if v >= hi - step * 1e-9:
            break
        v += step
    return vals[0], vals[-1], vals


# The label size the chart draws at, in the units of its own viewBox, and what
# that costs in space. One JBMono character advances 0.6 of its size, and two
# labels want a little air between them or they read as one. Both frames draw
# at the same label size, so both measure with these.
LABEL_SIZE = 11
CHAR_W = LABEL_SIZE * 0.6
LABEL_AIR = LABEL_SIZE * 1.45

PANEL_SPEC = [
    # title, unit, colour, gradient id, index into a point, minimum axis span.
    ("MEASURED STORAGE", "Bcf", "#ffc72c", "gwA", 1, None),
    ("MODELED PEAK DEMAND", "MMcf per day", "#5ac8f0", "gwB", 2, 40.0),
    ("NON CINGSA SUPPLY, DERIVED", "MMcf per day", "#9664e6", "gwC", 3, 60.0),
]


def chart_data(series, model):
    """(points, live panels with their axes) or (None, None) below two days.

    ONE definition, because chart_svg draws these and display_numerals has to
    authorise every numeral they put on the page. Computed twice they drift,
    and the numeral lint then calls the chart's own axis invented, which is
    exactly what happened when the residual panel was added.
    """
    rows = [r for r in series
            if r.get("verified") and (r.get("cingsa") or {}).get("inventory_mcf")]
    if len(rows) < 2:
        return None, None

    # Off the whole series, not the plotted rows: a record with no storage
    # reading cannot be a point on the storage panel and still carries a sound
    # residual for the day before it.
    residual_on = residual_by_day(series, model)

    pts = []
    for r in rows:
        der = remodel(r, model)[0]
        pts.append((r["date"],
                    round(r["cingsa"]["inventory_mcf"] / 1_000_000, 2),
                    der.get("peak_modeled_demand_mmcfd"),
                    residual_on.get(r["date"])))

    design = round((rows[-1]["cingsa"].get("storage_design_mcf") or 0) / 1_000_000, 1)
    live = []
    for title, unit, colour, fid, idx, min_span in PANEL_SPEC:
        have = [(i, p[idx]) for i, p in enumerate(pts) if p[idx] is not None]
        # The same rule the whole chart follows, applied per panel. One point
        # is not a trend, and a 132px panel holding a single dot with its label
        # hanging into the axis says less than no panel at all. The residual
        # resolves a day in arrears, so it is always the last to qualify.
        if len(have) < 2:
            continue
        # A tenth of the field for storage. Below that the panel draws noise.
        span = min_span if min_span is not None else max(design * 0.10, 0.4)
        lo, hi, ticks = nice_bounds(min(v for _, v in have) * 0.98,
                                    max(v for _, v in have) * 1.02,
                                    min_span=span)
        live.append({"title": title, "unit": unit, "colour": colour, "fid": fid,
                     "idx": idx, "have": have, "lo": lo, "hi": hi, "ticks": ticks})
    return pts, live


def chart_svg(series, model, w=920, panel_h=110, gap=38, pad_l=62, mode="wide"):
    """The record so far, as small multiples on one time axis.

    THREE PANELS, ONE SCALE EACH. An early draft put storage and demand on one
    frame with two y scales, which is a dual axis chart. The alignment of two
    scales is arbitrary, so the reader sees a correlation the data never
    claimed. Small multiples say the same thing without inventing it.

    TWO GEOMETRIES, ONE DRAWING. The same function draws a wide frame and a
    narrow one, and CSS puts exactly one of them in the layout. This is not a
    style preference. Text inside a viewBox scales with the frame, so a 920
    wide chart squeezed into a 316px phone card renders 11px mono at about 4px,
    and the fix that shipped first was to floor the plot at 600px and let the
    CARD scroll sideways. That floor meant a phone reader never saw more than
    half the series at once, and the shape of a trend is the one thing this
    picture is for. A frame drawn at phone proportions needs no floor and no
    scroll, so the whole record is on screen at a glance. Nothing about the
    data changes between the two, only the box it is drawn in. Both read the
    same chart_data, so the axes, the ticks and the values are identical.

    The narrow frame is not the wide one shrunk. Its plot area is squarer, so
    the same series climbs at a steeper angle, which is a property of every
    responsive chart and worth naming. The guard against a misleading slope is
    on the Y axis, where nice_bounds holds a minimum span tied to the thing
    measured, and that guard is the same in both frames. The date axis carries
    fewer labels because fewer fit, and the number is measured against the
    frame rather than chosen.

    The third panel is the residual, non CINGSA supply, which is the figure no
    other public source publishes and which was in the table and missing from
    the picture.

    HONEST AXES. Each panel takes a minimum span tied to the thing it measures,
    so a day when nothing moved renders as a day when nothing moved. Fitted to
    the data alone, the first two readings, 6.50 and 6.54 Bcf of a 13 Bcf
    field, drew as a climb across the whole panel.

    Colour. Both marks are the site's brand accents and clear the 3 to 1
    contrast floor on this surface. One series per panel, so there is no
    adjacent pair to separate and no legend box to draw; the panel title names
    what is plotted.

    Below two points there is no trend to draw, so the caller falls back to the
    meter and the stat tiles rather than plotting a line through one dot.
    """
    pts, live = chart_data(series, model)
    if not pts:
        return ""
    pad_r, pad_b = 18, 34
    iw = w - pad_l - pad_r
    n = len(pts)
    MONO = f'font-size="{LABEL_SIZE}" font-family="JBMono,monospace"'
    INK, MUTE, GRID = "#f4f8ff", "#8da2be", "#152a44"

    def x(i):
        return pad_l + iw * i / (n - 1)

    h = panel_h * len(live) + gap * (len(live) - 1) + pad_b + 22

    # A gradient id has to be unique in the DOCUMENT, and the chart ships twice.
    # Sharing gwA between the frames left two elements holding one id, which is
    # invalid and resolves to whichever came first, so the narrow frame drew the
    # wide frame's fill and only worked by looking identical.
    def gid(pl):
        return pl["fid"] if mode == "wide" else f'{pl["fid"]}-{mode}'

    # cols is one y column per panel, every day in order, None where the panel
    # has no value for that day. The readout moves a single marker to these, so
    # the marker count no longer grows with the record.
    body, tops, cols = "", {}, []
    for k, pl in enumerate(live):
        title, unit, colour, fid = pl["title"], pl["unit"], pl["colour"], gid(pl)
        have, lo, hi, ticks = pl["have"], pl["lo"], pl["hi"], pl["ticks"]
        top = 22 + k * (panel_h + gap)
        tops[pl["idx"]] = (top, colour)

        def y(v, top=top, lo=lo, hi=hi):
            return top + panel_h - panel_h * (v - lo) / (hi - lo)

        # EVERY GRIDLINE, NOT EVERY NUMBER. nice_bounds decides the ticks from
        # the data, and six of them in a 68 unit panel is a label every 13
        # units for type 11 units tall, which smears into one grey band. The
        # lines all stay, because the grid is the reference a reader measures
        # against; the labels thin to what the panel can hold. Computed from
        # the panel height, so a frame can be made shorter without anyone
        # remembering to retune this.
        every = 1
        if len(ticks) > 1:
            room = panel_h / (len(ticks) - 1)
            while room * every < LABEL_AIR:
                every += 1
        grid = "".join(
            f'<line x1="{pad_l}" y1="{y(t):.1f}" x2="{pad_l + iw}" y2="{y(t):.1f}" '
            f'stroke="{GRID}" stroke-width="1"/>'
            + (f'<text x="{pad_l - 10}" y="{y(t) + 4:.1f}" text-anchor="end" '
               f'fill="{MUTE}" {MONO}>{t:g}</text>' if j % every == 0 else "")
            for j, t in enumerate(ticks))
        d = " ".join(f'{"M" if j == 0 else "L"}{x(i):.1f},{y(v):.1f}'
                     for j, (i, v) in enumerate(have))
        area = (f'{d} L{x(have[-1][0]):.1f},{top + panel_h} '
                f'L{x(have[0][0]):.1f},{top + panel_h} Z')
        li, lv = have[-1]
        # A high last reading put this value on top of the unit label in the
        # panel's top right corner. Measured, not guessed: above the dot when
        # there is room, below it when there is not.
        lab_y = y(lv) - 11
        if lab_y < top + 11:
            lab_y = y(lv) + 17
        # The endpoint value in INK with a keyed dot beside it, never in the
        # series colour. A light accent is illegible as text on this surface,
        # and identity belongs to the mark rather than to the letters.
        body += f"""<path d="{area}" fill="url(#{fid})"/>{grid}
<path d="{d}" fill="none" stroke="{colour}" stroke-width="2"
 stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="{x(li):.1f}" cy="{y(lv):.1f}" r="4.5" fill="{colour}"
 stroke="#0a1626" stroke-width="2"/>
<text x="{pad_l}" y="{top - 9}" fill="{INK}" {MONO}>{title}</text>
<text x="{pad_l + iw}" y="{top - 9}" text-anchor="end" fill="{MUTE}" {MONO}>{unit}</text>
<text x="{x(li) - 10:.1f}" y="{lab_y:.1f}" text-anchor="end" fill="{INK}"
 {MONO}>{lv:g}</text>"""
        # The readout's y positions for this panel, taken now while the scale
        # is in scope. Computed after the loop they were all zero.
        col = [None] * n
        for i, v in have:
            col[i] = round(y(v), 1)
        cols.append(col)

    # Ordinal dates, house style, and never more than will fit.
    #
    # Measured against the room each label actually takes rather than against
    # one spacing constant. The first label is start anchored, the last is end
    # anchored and the ones between are centred, so three labels the same
    # distance apart occupy three different spans, and a constant tuned on the
    # wide frame printed "Aug 11th" through "Aug 13th" the first time the
    # narrow frame drew a nine day record.
    def label(i):
        """(left edge, right edge, anchor) for the date mark at day i."""
        txt = short_date(pts[i][0])
        px = min(max(x(i), pad_l + 2), pad_l + iw - 2)
        wide_as = len(txt) * CHAR_W
        if i == 0:
            return px, px + wide_as, "start"
        if i == n - 1:
            return px - wide_as, px, "end"
        return px - wide_as / 2, px + wide_as / 2, "middle"

    # The ends first, because they carry the range and are never dropped, then
    # as many interior marks as clear everything already placed.
    marks = [0] + ([n - 1] if n > 1 else [])
    taken = [label(i) for i in marks]
    for i in range(max(1, n // 6), n - 1, max(1, n // 6)):
        lo_i, hi_i, _a = label(i)
        if all(hi_i + LABEL_AIR <= t[0] or lo_i - LABEL_AIR >= t[1] for t in taken):
            taken.append((lo_i, hi_i, "middle"))
            marks.append(i)
    dates = "".join(
        f'<text x="{min(max(x(i), pad_l + 2), pad_l + iw - 2):.1f}" y="{h - 11}" '
        f'text-anchor="{label(i)[2]}" '
        f'fill="{MUTE}" {MONO}>{short_date(pts[i][0])}</text>' for i in sorted(marks))

    # The readout layer. One crosshair snapping to the nearest date and one
    # readout carrying every series for it, so the pointer never has to land on
    # a 2px line. Values are written by script from a payload the numeral lint
    # does not scan, and every one of them is already in the table below, so
    # the readout enhances and never gates.
    #
    # ONE SURFACE, NOT ONE PER DAY. This was a hit rect, a crosshair and three
    # dots for every day in the record, which is markup that grows forever: at
    # a year it was 374 KB of chart and each day's target was under a pixel
    # wide on a phone, so the thing a finger was meant to aim at had become
    # untouchable at exactly the length that most needed it. Now one rect takes
    # the whole plot, one line and one marker per panel move to the nearest
    # day, and the geometry travels as numbers in the payload. The markup stops
    # growing and a thumb dragged across the chart reads it day by day.
    #
    # ONE TAB STOP, whatever the length. Every day used to take tabindex="0",
    # which reads fine at three days and becomes 365 tab presses to get PAST
    # the chart inside a year. The surface is a slider, arrow keys move a day
    # at a time, Home and End jump to the ends, and Tab leaves in one press.
    dx = iw / max(1, n - 1)
    hit = (f'<rect class="gw-hit" x="0" y="16" width="{w}" '
           f'height="{h - pad_b - 16:.1f}" fill="transparent" tabindex="0" '
           f'role="slider" aria-label="Day by day readout, drag or use the '
           f'arrow keys to read one day" aria-valuemin="0" '
           f'aria-valuemax="{n - 1}" aria-valuenow="{n - 1}" '
           f'aria-valuetext="{esc(long_date(pts[-1][0]))}"/>')
    rules = (f'<line class="gw-cross" x1="0" y1="16" x2="0" '
             f'y2="{h - pad_b:.1f}" stroke="{INK}" stroke-width="1" '
             f'opacity="0"/>')
    dots = "".join(
        f'<circle class="gw-mk" cx="0" cy="0" r="4" fill="{pl["colour"]}" '
        f'stroke="#0a1626" stroke-width="2" opacity="0"/>' for pl in live)
    # Built from the panels that are live rather than typed three times, so a
    # panel can never carry a fill in another panel's colour.
    defs = "".join(
        f'<linearGradient id="{gid(pl)}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{pl["colour"]}" stop-opacity=".10"/>'
        f'<stop offset="1" stop-color="{pl["colour"]}" stop-opacity="0"/>'
        f'</linearGradient>' for pl in live)
    payload = json.dumps({
        "n": n, "w": w, "x0": pad_l, "dx": round(dx, 4), "m": mode,
        "d": [long_date(p[0]) for p in pts],
        "s": [{"t": pl["title"], "c": pl["colour"],
               "v": [("%g" % p[pl["idx"]]) if p[pl["idx"]] is not None else None
                     for p in pts],
               "y": cols[k]}
              for k, pl in enumerate(live)],
    })

    return f"""<div class="gw-plot gw-{mode}" data-gw-plot='{esc(payload)}'>
<div class="gw-tip" hidden></div>
<svg viewBox="0 0 {w} {h}" width="100%" role="img"
 aria-label="{esc(len(live))} charts sharing one time axis, covering
 {esc(long_date(pts[0][0]))} to {esc(long_date(pts[-1][0]))}. Measured Cook Inlet
 storage in Bcf, modeled peak daily demand, and derived non CINGSA supply, both
 in MMcf per day. Every value is in the table below.">
<defs>{defs}</defs>
{body}{dates}{rules}{dots}{hit}</svg>
</div>"""


# THE NARROW FRAME, in the units of its own viewBox. Measured against a phone
# rather than picked. A 390px viewport leaves a 316px card once the page gutter
# and the card padding are taken out, so a 370 wide frame renders 11 unit mono
# at about 9px, which is read at arm's length. The plot area is 310 by 68 per
# panel, near four and a half to one against the wide frame's seven and a half,
# so the panels stay tall enough to carry their own gridline labels and the
# slope does not run away from the truth.
NARROW = {"w": 370, "panel_h": 68, "gap": 34, "pad_l": 42}


def chart_html(series, model):
    """Both frames of the chart. CSS puts exactly one of them in the layout.

    Returns "" when the record is too short to plot, which is the caller's
    signal to fall back to the meter and the table.
    """
    wide = chart_svg(series, model)
    if not wide:
        return ""
    return wide + chart_svg(series, model, mode="narrow", **NARROW)


def table_html(series, model, limit=TABLE_LIMIT):
    """The table view twin. Every plotted value readable without the chart.

    This is also the form a reporter actually wants, since it can be copied
    into a story without reading pixels off a line.
    """
    rows = [r for r in series if r.get("verified")][-limit:]
    if not rows:
        return ""
    # Keyed by the day the figure is ABOUT, so a value can never land on a row
    # it does not describe. Keying the cell to the record instead put August
    # 5th's 141.7 on the August 6th row while the prose above the table, which
    # reads balance_date, said August 5th in the same breath. Built from the
    # WHOLE series rather than the displayed window, because the residual for
    # the oldest visible row is carried by the record before it.
    residual = residual_by_day(series, model)
    body = ""
    gaps = 0
    for r in rows:
        cin = r["cingsa"]
        der, _ = remodel(r, model)
        resid = residual.get(r["date"])
        if der.get("peak_modeled_demand_mmcfd") is None or resid is None:
            gaps += 1
        body += (
            f'<tr><td>{esc(r["date"])}</td>'
            f'<td>{round(cin["inventory_mcf"] / 1_000_000, 2)}</td>'
            f'<td>{cin["inventory_pct_of_design"]}</td>'
            f'<td>{blank(der.get("peak_modeled_demand_mmcfd"))}</td>'
            f'<td>{blank(resid)}</td></tr>')
    # An empty cell is deliberate (see blank()), but on a short table it reads
    # as data this page failed to collect rather than as a figure the model had
    # no input for. One sentence, shown only when a cell is actually empty, and
    # it names no specific input so no arrangement of the data can falsify it.
    gap_note = (" A blank cell is a figure the model had no input for that day,"
                " not a reading that went missing." if gaps else "")
    # The note lives OUTSIDE the scrolling wrapper on purpose. It used to be a
    # <caption> inside the table, which meant it took the TABLE's intrinsic
    # width, 684 px at five columns, and on a 390 px phone the sentence was
    # clipped mid-word with no way to read it but to drag the numbers sideways.
    # The columns are wide because they are numbers and have to scroll; a
    # paragraph of prose does not, so it wraps to the reader's own width and the
    # table keeps its accessible name through aria-describedby.
    return f"""<div class="gw-table" data-reveal>
<table aria-describedby="gw-tablenote">
<caption class="gw-vh">Cook Inlet gas storage, day by day</caption>
<thead><tr><th scope="col">Date</th><th scope="col">Storage Bcf</th>
<th scope="col">Percent of design</th><th scope="col">Modeled peak MMcf/d</th>
<th scope="col">Non CINGSA supply MMcf/d</th></tr></thead>
<tbody>{body}</tbody></table></div>
<p class="gw-tnote" id="gw-tablenote" data-reveal>The most recent
{count(len(rows), "verified reading")}. Storage and percent of design are
measured. Modeled peak and non CINGSA supply are model output.{gap_note}</p>"""


# ------------------------------------------------------------------ feed

def feed(series, model, site_url, today, meta, figs=None):
    """The gas-watch.json envelope.

    Reuses the docket feed's meta keys exactly, so the two read as one data
    family and a consumer who parsed one can parse the other. Where the docket
    has items, this has series, one object per day, oldest first.
    """
    hist, hdd_series = gc.load_hdd_history(model, REPO)
    return {
        "name": "Cook Inlet Gas Watch",
        "description": ("A daily numeric record of Southcentral Alaska's natural "
                        "gas position. Measured storage inventory and "
                        "deliverability from the CINGSA public dashboard, modeled "
                        "regional demand from Anchorage degree days, and the "
                        "derived non CINGSA supply that falls out of the mass "
                        "balance. It publishes no safety verdict of any kind."),
        "version": SCHEMA_VERSION,
        "updated": today.isoformat(),
        "canonical": f"{site_url}/gas-watch.json",
        "documentation": f"{site_url}/gas-watch/",
        "license": meta["license"],
        "license_label": meta["license_label"],
        "attribution": meta["attribution"],
        "publisher": meta["publisher"],
        "spatial_coverage": meta["spatial_coverage"],
        "temporal_coverage": (f"{series[0]['date']}/{series[-1]['date']}"
                              if series else None),
        "count": len(series),
        "related_docket_item": f"{site_url}/docket/{meta['docket_item_id']}/",
        "warning": ("This dataset must not be used to state or imply whether the "
                    "region will make it through a cold snap. Supply side "
                    "deliverability is not public, so no adequacy conclusion can "
                    "be drawn from these numbers."),
        "model": dict(model, hdd_history_days=hist["days"],
                      hdd_history_start=hist["start_date"],
                      hdd_history_end=hist["end_date"]),
        "model_history": model.get("model_history", []),
        "crosscheck": {k: v for k, v in figures(series, model, figs).items()
                       if k.startswith("eia_")},
        "crosscheck_source": {
            "publisher": "US Energy Information Administration",
            "url": "https://api.eia.gov/bulk/NG.zip",
            "documentation": "https://www.eia.gov/opendata/",
            "note": "Monthly, Alaska statewide, lags about two months. It checks "
                    "the demand model and the storage picture. It is not a refit "
                    "and it does not close the daily gap."},
        "series": series,
    }


# ------------------------------------------------------------------ self test

def self_test():
    print("reader")
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "s.jsonl")
        with open(p, "w") as fh:
            fh.write(json.dumps({"date": "2026-08-01", "verified": True,
                                 "cingsa": {"inventory_mcf": 5_000_000,
                                            "storage_design_mcf": 13_000_000,
                                            "inventory_pct_of_design": 38.5,
                                            "inventory_delta_mcf": 1000,
                                            "withdrawal_operating_mcfd": 132117,
                                            "withdrawal_restriction_mcfd": 0,
                                            "injection_in_progress_mcfd": 1000},
                                 "derived": {"peak_modeled_demand_mmcfd": 120},
                                 "reconciliation": {}, "flags": []}) + "\n")
            fh.write(json.dumps({"date": "2026-08-03", "verified": False,
                                 "cingsa": {"fetch_status": "failed"},
                                 "reconciliation": {}, "flags": []}) + "\n")
            fh.write(json.dumps({"date": "2026-08-03", "verified": True,
                                 "cingsa": {"inventory_mcf": 5_100_000,
                                            "storage_design_mcf": 13_000_000,
                                            "inventory_pct_of_design": 39.2,
                                            "inventory_delta_mcf": 2000,
                                            "withdrawal_operating_mcfd": 132117,
                                            "withdrawal_restriction_mcfd": 0,
                                            "injection_in_progress_mcfd": 2000},
                                 "derived": {"peak_modeled_demand_mmcfd": 130},
                                 "reconciliation": {}, "flags": []}) + "\n")
        s = load_series(p)
        check("a repair line supersedes the unverified line it follows",
              len(s) == 2 and s[1]["verified"], f"{len(s)} standing records")
        check("standing records come back oldest first",
              [r["date"] for r in s] == ["2026-08-01", "2026-08-03"])
        check("a real gap is reported", continuity(s) == ["2026-08-02"],
              str(continuity(s)))

    print("axis bounds")
    # Swept rather than spot checked, because the failure mode is a data point
    # drawn outside the plotted area and it only shows up at certain spans.
    escaped = []
    for a in (0.0, 0.7, 5.0, 6.13, 99.4, 1234.0):
        for span in (0.0, 0.001, 0.4, 1.7, 13.0, 480.0):
            top = a + span
            eps = max(abs(top), 1.0) * 1e-9
            lo, hi, ticks = nice_bounds(a, top)
            if lo > a + eps or hi < top - eps or len(ticks) < 2 or ticks != sorted(ticks):
                escaped.append((a, top, lo, hi))
    check("every tested span is fully inside its axis", not escaped,
          f"36 spans swept, {len(escaped)} escaped" +
          (f", first {escaped[0]}" if escaped else ""))
    lo, hi, ticks = nice_bounds(5.0, 5.0)
    check("a flat series still produces a usable axis", hi > lo, f"{lo} to {hi}")

    print("the chart says what the data says")
    chart_model = gc.load_model(MODEL_CONFIG)
    live_rows = [r for r in load_series() if r.get("verified")]
    if len(live_rows) >= 2:
        _pts, _live = chart_data(load_series(), chart_model)
        # The residual belongs to the day it describes. The record for the 6th
        # carries the balance FOR the 5th, and plotting it on the 6th would
        # misdate the one figure nobody else publishes, every single day.
        by_date = {p[0]: p[3] for p in _pts}
        want = residual_by_day(load_series(), chart_model)
        misplaced = [d for d, v in want.items() if d in by_date and by_date[d] != v]
        # NOT a check that the keying is right. Both sides of this comparison
        # now come from residual_by_day, so it agrees with itself whatever that
        # function does, which is the same self-confirming shape that let the
        # misdating live for a day. What it still catches is chart_data losing
        # or shifting a value on the way to a point. The keying is pinned on
        # built data below, where a wrong answer has nothing to agree with.
        check("every balanced day reaches the chart intact", not misplaced,
              str(misplaced) or f"{len(want)} balanced day(s)")
        check("a panel needs two points, like the chart does",
              all(len(pl["have"]) >= 2 for pl in _live),
              str([(pl["title"], len(pl["have"])) for pl in _live]))

    # Against a BUILT series rather than the ledger, because the ledger holds
    # two balanced days today and a case that only bites on a shape the data
    # has not reached yet is not a case. Day two's record carries the balance
    # FOR day one, so a reader keying off the record puts it on day two.
    off_by_one = [
        {"date": "2026-08-01", "verified": True,
         "cingsa": {"inventory_mcf": 5_000_000, "storage_design_mcf": 13_000_000,
                    "inventory_pct_of_design": 38.5},
         "derived": {}, "reconciliation": {}, "flags": []},
        {"date": "2026-08-02", "verified": True,
         "cingsa": {"inventory_mcf": 5_100_000, "storage_design_mcf": 13_000_000,
                    "inventory_pct_of_design": 39.2},
         "derived": {},
         "reconciliation": {"date": "2026-08-01", "actual_hdd65": 12.0,
                            "storage_withdrawal_mmcfd": 40.0},
         "flags": []},
    ]
    placed = residual_by_day(off_by_one, chart_model)
    balance = remodel(off_by_one[1], chart_model)[1]["non_cingsa_supply_mmcfd"]
    check("a balance lands on the day it is about, not the day it arrived",
          placed == {"2026-08-01": balance}, str(placed))
    plotted = {p[0]: p[3] for p in chart_data(off_by_one, chart_model)[0]}
    check("the chart reads it from there",
          plotted == {"2026-08-01": balance, "2026-08-02": None}, str(plotted))
    # Same figure, same row, in the other reader. These two were written apart
    # and got the keying wrong apart, so agreement is the thing to assert.
    table_rows = re.findall(r"<tr><td>(2026-08-\d\d)</td>.*?<td>([^<]*)</td></tr>",
                            table_html(off_by_one, chart_model))
    check("and the table puts it on the same row",
          table_rows == [("2026-08-01", str(balance)), ("2026-08-02", "")],
          str(table_rows))

    # ONE tab stop, whatever the length. This is checked on a long synthetic
    # series because at today's three days the broken version and the fixed one
    # are both fine, and the difference only becomes a problem months out.
    long_series = []
    for d in range(200):
        long_series.append(
            {"date": (date(2026, 1, 1) + timedelta(days=d)).isoformat(),
             "verified": True,
             "cingsa": {"inventory_mcf": 5_000_000 + d * 1000,
                        "storage_design_mcf": 13_000_000,
                        "inventory_pct_of_design": 38.5},
             "derived": {}, "reconciliation": {}, "flags": []})
    long_svg = chart_svg(long_series, chart_model)
    stops = long_svg.count('tabindex="0"')
    surfaces = long_svg.count('class="gw-hit"')
    check("a long record still costs one tab press to skip", stops == 1,
          f"{surfaces} readout surface(s), {stops} tab stop(s)")
    check("and every day stays reachable by arrow key",
          'ArrowLeft' in GW_JS and 'ArrowRight' in GW_JS and "'End'" in GW_JS)

    # THE MARKUP MUST STOP GROWING WITH THE RECORD. A hit rect, a crosshair and
    # three dots per day is 374 KB of chart inside a year, and each day's target
    # is under a pixel wide on a phone, so the surface a finger aims at gets
    # untouchable at exactly the length that most needs it. One surface, one
    # rule, one marker per panel, and the geometry travels as numbers.
    short_svg = chart_svg(long_series[:20], chart_model)
    fixed = all(long_svg.count(sel) == short_svg.count(sel)
                for sel in ('class="gw-hit"', 'class="gw-cross"', 'class="gw-mk"'))
    check("the readout layer does not grow with the record", fixed,
          f'200 days draws {long_svg.count(chr(34) + "gw-mk" + chr(34))} marker(s), '
          f'20 days draws {short_svg.count(chr(34) + "gw-mk" + chr(34))}')

    # BOTH FRAMES, ONE READING. The page ships a wide frame and a narrow one and
    # CSS puts exactly one in the layout. They must be the same chart, since a
    # phone and a laptop disagreeing about a measurement is the worst failure
    # this page has. Same days, same values, same axis, and nothing scrolls,
    # which is the whole reason the narrow frame exists.
    both = chart_html(long_series, chart_model)
    wide_pl = json.loads(_html.unescape(
        re.findall(r"data-gw-plot='([^']*)'", both)[0]))
    narrow_pl = json.loads(_html.unescape(
        re.findall(r"data-gw-plot='([^']*)'", both)[1]))
    check("the two frames plot the same days and the same values",
          wide_pl["d"] == narrow_pl["d"]
          and [s["v"] for s in wide_pl["s"]] == [s["v"] for s in narrow_pl["s"]],
          f'{wide_pl["n"]} day(s) either way')
    check("and the narrow frame is a different box, not the wide one shrunk",
          narrow_pl["w"] < wide_pl["w"] and narrow_pl["m"] == "narrow",
          f'{wide_pl["w"]} wide against {narrow_pl["w"]}')
    # A duplicated gradient id resolves to whichever came first, so the second
    # frame would silently draw the first frame's fill.
    ids = re.findall(r'<linearGradient id="([^"]+)"', both)
    refs = re.findall(r"url\(#([^)]+)\)", both)
    check("every gradient id is unique and every fill resolves",
          len(ids) == len(set(ids)) and set(refs) <= set(ids),
          f"{len(ids)} gradient(s), {len(set(refs))} referenced")
    # THE SIDEWAYS SCROLL, which is the thing this frame exists to be rid of.
    # The old rule floored the plot at 600px and let the card scroll, so a phone
    # reader saw half the series and had to swipe for the rest. A minimum width
    # on the plot, or an overflow-x on the card, brings it straight back. Scoped
    # to the card and the plot itself and never to a thing sitting on top of
    # one, because the readout is allowed its own widths.
    floored = [rule for rule in GW_CSS.split("}")
               if any(re.search(r"\.gw-(chart|plot|wide|narrow)(\s+svg)?\s*$", sel)
                      for sel in rule.split("{")[0].split(","))
               and re.search(r"(min-width|overflow-x)\s*:", rule.split("{")[-1])]
    check("no floor forces the card to scroll sideways", not floored,
          str(floored) or "the whole series fits the frame it is drawn in")

    # A flat record has to render flat. Fitted to the data alone, two readings
    # a hundredth apart filled the panel and read as a climb.
    flat_lo, flat_hi, _t = nice_bounds(6.50 * 0.98, 6.54 * 1.02, min_span=1.3)
    check("a day when nothing moved does not fill the panel",
          (6.54 - 6.50) / (flat_hi - flat_lo) < 0.05,
          f"axis {flat_lo} to {flat_hi}, the move is "
          f"{(6.54 - 6.50) / (flat_hi - flat_lo) * 100:.1f} percent of it")
    real_lo, real_hi, _t = nice_bounds(3.1 * 0.98, 9.8 * 1.02, min_span=1.3)
    check("and a real drawdown still fills it",
          (9.8 - 3.1) / (real_hi - real_lo) > 0.6,
          f"axis {real_lo} to {real_hi}")

    print("the numeral lint")
    model = gc.load_model(MODEL_CONFIG)
    live_series = load_series()
    figs = figures(live_series, model)
    # The series goes in. Without it display_numerals contributes nothing, so
    # the axis ticks the chart draws are unauthorised and the chart check below
    # fails. It passed for a day anyway, because the chart needs two readings to
    # draw at all and the ledger held one. Same blind spot the series-length
    # cases were added to close, sitting inside the file that closed it.
    allowed = allowed_numerals(figs, model, ["CC BY 4.0"], live_series)
    check("a figure drawn from the data passes",
          not numeral_lint(f"<p>Storage holds {figs.get('inventory_bcf')} Bcf.</p>",
                           allowed))
    planted = numeral_lint("<p>Storage sits at 87.3 percent of design.</p>", allowed)
    check("a number nothing computed is caught", bool(planted), str(planted))
    check("chart geometry is not mistaken for prose",
          not numeral_lint(chart_svg(live_series, model), allowed))
    check("a typed number inside a chart TEXT label is caught",
          bool(numeral_lint("<svg><text>9182736</text></svg>", allowed)),
          "this previously passed a paragraph and certified nothing")
    check("chart geometry is still ignored",
          not numeral_lint('<svg><path d="M12.3,45.6 L78.9,10.1"/></svg>', allowed))
    # A WHOLE PAGE, on a series longer than one day. Every check above ran on
    # the live ledger, which held a single reading, and a single reading is the
    # one length at which figures() happens to cover everything the table and
    # the chart draw. On the second day the page would have carried a row per
    # date, an axis, and a caption counting rows, none of it authorised, and
    # site_build calls that a hard fail. The nightly rebuild would have died and
    # taken the commit step with it, losing a reading CINGSA cannot reissue.
    # So the lint is now exercised at the lengths the page will actually reach.
    import copy as _copy
    live = load_series()
    meta = {"license": "https://creativecommons.org/licenses/by/4.0/",
            "license_label": "CC BY 4.0", "attribution": "Alaska AI",
            "publisher": "Alaska AI", "spatial_coverage": "Alaska",
            "docket_item_id": "enstar-cook-inlet-gas-storage"}
    stretched = []
    for days in (2, 15, 60):
        sim, inv = [], 6_100_000
        for i in range(days):
            r = _copy.deepcopy(live[-1])
            r["date"] = (date(2026, 8, 5) + timedelta(days=i)).isoformat()
            inv += 37_311 if i % 3 else -52_907
            r["cingsa"]["inventory_mcf"] = inv
            r["cingsa"]["inventory_pct_of_design"] = round(inv / 13_000_000 * 100, 1)
            r["derived"]["peak_forecast_hdd"] = round(3.4 + i * 1.7, 1)
            r["derived"]["peak_modeled_demand_mmcfd"] = 999
            r["reconciliation"]["actual_hdd65"] = round(2.9 + i * 1.6, 1)
            r["reconciliation"]["storage_withdrawal_mmcfd"] = round(-31.5 + i * 4.4, 1)
            r["reconciliation"]["non_cingsa_supply_mmcfd"] = 999
            sim.append(r)
        page = page_body(date(2026, 12, 1), "https://alaskaaihq.com", sim, model,
                         meta, prefix="../")
        left = numeral_lint(page, allowed_numerals(
            figures(sim, model), model, ["CC BY 4.0"], sim))
        if left or "999" in page:
            stretched.append((days, sorted(set(left))[:4], "999" in page))
    check("a page built on a real length series invents nothing",
          not stretched, str(stretched) or "2, 15 and 60 day series all clean")

    check("a number typed into a config note does not authorise itself",
          bool(numeral_lint("<p>Storage sits at 71.6 Bcf.</p>", allowed)),
          "71.6 appears in a model config note and used to pass")

    # The maintainer asked who updates the wording when the state changes. The
    # answer has to be nobody, and this is what proves it. Every comparison the
    # prose makes is fed flipped inputs and has to flip with them. A typed word
    # would sit still and fail here.
    print("state-dependent wording follows the data")
    base = gc.load_model(MODEL_CONFIG)
    flips = [
        ("record_average_direction",
         {"record_average_day_mmcfd": 220.0, "anchor_published_average_day_mmcfd": 190},
         "heavy",
         {"record_average_day_mmcfd": 183.7, "anchor_published_average_day_mmcfd": 190},
         "light"),
        # The size of that gap is computed for the same reason its direction is.
        # It read "slightly light" in typed prose right up until a refit moved
        # the model ten percent under the anchor and the word stayed put.
        ("record_average_gap_pct",
         {"record_average_day_mmcfd": 228.0, "anchor_published_average_day_mmcfd": 190},
         20.0,
         {"record_average_day_mmcfd": 171.0, "anchor_published_average_day_mmcfd": 190},
         10.0),
        # The meter says which way the gas went. A typed word would keep
        # saying "into storage" through the entire withdrawal season.
        ("inventory_delta_direction",
         {"inventory_delta_mcf": 39723}, "into storage",
         {"inventory_delta_mcf": -51200}, "out of storage"),
        # A residual above modeled demand is not a bug, it is an injection day.
        # The page said "134.1 percent of the region's gas" on exactly such a
        # day, which is impossible as written, so the clause explaining it is
        # keyed to the sign of the measured withdrawal instead of being typed.
        ("residual_regime",
         {"storage_withdrawal_mmcfd": -38.3}, "filling",
         {"storage_withdrawal_mmcfd": 61.4}, "drawing"),
    ]
    for key, hi_in, hi_want, lo_in, lo_want in flips:
        got_hi = _comparison(key, hi_in)
        got_lo = _comparison(key, lo_in)
        check(f"{key} follows its inputs both ways",
              got_hi == hi_want and got_lo == lo_want,
              f"{got_hi} and {got_lo}, expected {hi_want} and {lo_want}")
    n = len(base.get("not_public_monthly_source") or {})
    check("the count of monthly-source items is read from config, not typed",
          spell(n).lower() in ("none", "one", "two", "three"), f"{n} recorded")

    print("the no verdict rule")
    body = page_body(date.today(), "https://alaskaaihq.com", load_series(), model,
                     {"license": "https://creativecommons.org/licenses/by/4.0/",
                      "license_label": "CC BY 4.0", "attribution": "Alaska AI",
                      "publisher": "Alaska AI", "spatial_coverage": "Alaska",
                      "docket_item_id": "enstar-cook-inlet-gas-storage"})
    banned = [w for w in ("will run out", "all clear", "shortfall is",
                          "blackout", "we will make it", "is safe", "is not safe")
              if w in body.lower()]
    check("the page states no adequacy verdict", not banned, str(banned))
    check("the page carries the limits of the data",
          "not public" in body.lower() and "verdict" in body.lower())

    # The overclaim guard. The model is two hand set coefficients fitted to two
    # published figures; nothing trains, learns, or updates itself. On a site
    # whose subject is AI, describing arithmetic as AI would be the exact
    # overclaim this publication exists to check, and it would put the one page
    # built on being checkable behind a claim that cannot be.
    # The guard bans the FALSE CLAIM rather than requiring a particular
    # disclaimer sentence. The copy should be free to read like a person wrote
    # it; what it may never say is that the model retrains itself, because
    # nothing does. Requiring a fixed sentence made the page sound like a
    # legal notice, which the maintainer was right to reject.
    overclaims = [w for w in ("our ai", "learns on its own", "self-improving",
                              "machine learning", "neural", "trains itself",
                              "fine-tunes itself", "fine tunes itself",
                              "gets smarter",
                              "continuously trained", "the ai predicts",
                              "learns automatically", "retrains")
                  if w in body.lower()]
    check("the page claims no training it does not do", not overclaims, str(overclaims))
    sells_short = underclaims(base)
    check("the config does not describe a model it outgrew",
          not sells_short, str(sells_short))
    check("that rule can still go red",
          underclaims(dict(base, fit={"months": 1}, calibration="working hypothesis"))
          == ["calibration: working hypothesis"])
    check("and it stays quiet on a model with no fit",
          underclaims({"calibration": "working hypothesis"}) == [])
    check("the page calls the demand figure an estimate",
          "estimate" in body.lower())
    check("the page still discloses what nothing reports daily",
          "not reported daily" in body.lower()
          and "enstar realtime sendout" in body.lower())
    check("no em dash, en dash, curly quote or emoji",
          not re.search("[–—‘’“”]"
                        "|[\U0001F000-\U0001FAFF]", body))
    colon_txt = re.sub(r"<[^>]+>", "\n", re.sub(r"(?s)<svg.*?</svg>", " ", body))
    colon_txt = re.sub(r"https?://\S+", " ", colon_txt)
    colon_txt = re.sub(r"\d{1,2}:\d{2}", " ", colon_txt)
    colons = [l.strip() for l in colon_txt.split("\n") if ":" in l]
    check("no prose colon, which site_build's ship gate would refuse",
          not colons, str(colons[:2]))

    print()
    if not ok[0]:
        print("self-test FAILED")
        return 1
    print("self-test clean")
    return 0


# ------------------------------------------------------------------ page

def stat(label, value, note, tone="gold"):
    return (f'<div class="gw-stat gw-{tone}"><div class="gw-num">{esc(value)}</div>'
            f'<div class="gw-lab">{esc(label)}</div>'
            f'<div class="gw-note">{esc(note)}</div></div>')


def gauge(f):
    """The storage level against the field's design capacity. The lead element.

    A bar rather than a dial, because a dial implies a red zone and a red zone
    is a verdict. This shows a measured ratio and stops there.

    It carries the hero figure because it is the one number a reader who gives
    this page four seconds will take away, and because it is measured rather
    than modeled. The figure is set in the body sans at display size, not the
    serif, and with proportional rather than tabular digits, which is what
    keeps a large standalone number from reading loose.
    """
    pct = f["inventory_pct_of_design"]
    read = long_date(f["as_of"])
    # The flag carries the reading to the fill edge, and it is pulled back
    # inside the track near either end so it cannot hang off the card.
    # Under this much fill there is no room to letter the value inside it.
    side = "is-left" if pct < 14 else ""
    # The day's movement fills the right of the reading row, which was 500px of
    # nothing. It is measured, it is directional, and it is the one fact that
    # makes a daily record worth more than a snapshot of the dashboard.
    moved = ""
    if "inventory_delta_mmcf" in f and "inventory_delta_direction" in f:
        moved = f"""
  <div class="gw-gauge-move">
    <span class="gw-gauge-of-lab">On the day</span>
    <span class="gw-gauge-move-num">{f["inventory_delta_mmcf"]}
      <i>MMcf {f["inventory_delta_direction"]}</i></span>
  </div>"""
    return f"""<figure class="gw-gauge" data-reveal>
<figcaption class="gw-gauge-head">
  <span class="gw-gauge-what">Cook Inlet storage</span>
  <span class="gw-gauge-when">read {read}</span>
</figcaption>
<div class="gw-gauge-read">
  <div class="gw-hero">{pct}<span>%</span></div>
  <div class="gw-gauge-of">
    <span class="gw-gauge-of-lab">of design capacity</span>
    <span class="gw-gauge-of-num">{f["inventory_bcf"]} <i>of {f["design_bcf"]} Bcf</i></span>
  </div>{moved}
</div>
<div class="gw-gauge-track" role="img"
 aria-label="Storage at {pct} percent of design capacity, {f["inventory_bcf"]} of {f["design_bcf"]} Bcf, read {read}.">
  <div class="gw-gauge-fill" style="--pct:{pct}%"></div>
  <div class="gw-gauge-flag {side}" style="--pct:{pct}%">
    <span class="gw-gauge-flag-num">{f["inventory_bcf"]}</span>
  </div>
</div>
<div class="gw-gauge-axis" aria-hidden="true">
  <span></span><span></span><span></span><span></span><span></span>
</div>
<div class="gw-gauge-foot">
  <span>Empty</span>
  <span class="gw-gauge-cap">Full, {f["design_bcf"]} Bcf</span>
</div>
</figure>"""


def home_strip(series, model, prefix="", figs=None):
    """The storage meter for the homepage, under the docket.

    Same figures dict as the page, so the two can never disagree. It renders
    nothing at all when there is no verified reading, because a homepage is the
    last place to explain an absence.
    """
    f = figures(series, model, figs)
    if "as_of" not in f:
        return ""
    # ONE meter, built once. The homepage and the gas watch page carried
    # separate copies of this markup, so a change to either could drift from
    # the other and the redesign would have had to be done twice.
    return f"""<h2 data-reveal><a href="{prefix}gas-watch/">Cook Inlet Gas Watch</a></h2>
<p class="sub" data-reveal>How much gas Southcentral has in the ground, read every
day and kept.</p>
{gauge(f)}
<div class="ctarow" data-reveal><a class="cta ghost" href="{prefix}gas-watch/">OPEN THE GAS WATCH</a></div>"""


def page_body(today, site_url, series, model, meta, prefix="../", figs=None,
              aside=""):
    """The Gas Watch page.

    Structure follows what a reporter on deadline needs, in order. What the
    number is, when it was read, where it came from, how the modeled parts were
    derived, and what nobody can see. The methodology is not an appendix here,
    it is the product.

    `aside` is a sibling measurement the site composes and this module does not
    own, currently the retail power price. It lands after the gas balance and
    before the methodology, because the methodology that follows describes the
    gas figures above it and nothing in the aside uses it. Passed in rather than
    built here so this module keeps depending on the gas ledger alone, which is
    what lets gaswatch_pagecheck render a reference page with no site build.
    """
    f = figures(series, model, figs)
    # Guard on a usable READING, not on a non-empty series. figures() correctly
    # drops as_of and the inventory keys when nothing is verified, and the body
    # below indexes them, so a ledger holding only unverified records raised
    # KeyError here. site_build calls this before writing any page, so that
    # crash cost the whole site, not one page.
    if not series or "as_of" not in f:
        note = ("No reading has been collected yet."
                if not series else
                f'{count(f["days_of_record"], "day")} on record, none of them '
                f'verified. A fetch failed or the source had stopped updating, '
                f'and no number is carried forward from a day that did work.')
        return (f'<div class="hero" style="min-height:auto;padding-top:9vh">'
                f'<div class="chip kind">LIVE INSTRUMENT</div>'
                f'<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">'
                f'Cook Inlet Gas Watch</h1>'
                f'<p class="tag">{note}</p></div>')

    # Below two readings there is no trend, and a line through one dot is a
    # chart pretending to know something. The meter and the tiles carry the
    # page until the series can support a plot.
    svg = chart_html(series, model)
    if svg:
        chart_block = (
            f'<div class="gw-chart" data-reveal>{svg}</div>'
            f'<p class="sub" data-reveal>CINGSA keeps no archive, so this series '
            f'exists only because it is collected daily and committed. It begins '
            f'{long_date(f["first_date"])}. Storage is measured. The peak is '
            f'model output, shown on its own scale because the two quantities '
            f'are different in kind and sharing one axis would imply a '
            f'relationship the data does not claim.</p>')
    else:
        chart_block = (
            f'<p class="sub" data-reveal>'
            f'{count(f["days_of_record"], "day")} on record, which is not yet a '
            f'trend to plot. The table below is the whole series.</p>')

    # The forecast error scoreboard lived here and shipped with the paragraph
    # that carried it. Removed 2026-08-12 at the maintainer's call, because the
    # page was crowded and this was the third accuracy figure on it. The two
    # that matter are still published: how far the model misses the months it is
    # fitted to, in "The model, in full", and how its record average compares
    # against the published average day, in the paragraph under the backtests.
    # CLAUDE.md requires the model be CHECKED rather than asserted, and both of
    # those are the check.

    stale_note = ""
    if f.get("unverified_days"):
        stale_note = (
            f'<p class="sub" data-reveal>Of {count(f["days_of_record"], "day")} on '
            f'record, {f["unverified_days"]} carry no verified reading because a fetch '
            f'failed or the source had stopped updating. Those days are marked '
            f'unverified in the data and carry no number forward from the day '
            f'before.</p>')

    balance = ""
    if "non_cingsa_supply_mmcfd" in f:
        # The regime clause is computed, never typed. The old sentence called
        # this ratio a share "of the region's gas", which caps at one hundred by
        # definition, and the page was publishing 134.1 percent of it on a summer
        # injection day. The number was right and the noun was wrong.
        regime = {
            "filling": ("It exceeds demand because the field was filling, so "
                        "some went to storage rather than a burner"),
            "drawing": ("It falls short of demand because the field was "
                        "draining, and measured storage covered the difference"),
            "flat": ("It matches demand because storage neither filled nor "
                     "drained that day"),
        }[f["residual_regime"]]
        balance = f"""<h2 data-reveal>What is not measured by anyone</h2>
<p class="prose" data-reveal>Demand equals field production plus storage
withdrawal. Withdrawal is measured, demand is modeled, and everything not CINGSA
falls out by subtraction. On {long_date(f["balance_date"])} that residual was
{f["non_cingsa_supply_mmcfd"]} MMcf per day against modeled demand of
{f["modeled_demand_mmcfd"]}, or {f["unmeasured_share_pct"]} percent, all from
sources no public feed reports daily. {regime}. That ratio is the hole in the
public record, and why this page draws no adequacy conclusion.</p>
<p class="prose" data-reveal>Strictly it is production plus any Hilcorp
storage movement, which public data can't separate,
so the field is named non_cingsa_supply and never
production.</p>"""

    bt_rows = ""
    for b in model.get("backtests", []):
        bid = b["id"].replace("-", "_")
        got = f.get(f"{bid}_mmcfd") or f.get(f"{bid}_bcf")
        unit = "Bcf" if f.get(f"{bid}_bcf") is not None else "MMcf/d"
        bt_rows += (f'<li><p><strong>{esc(b["description"])}</strong> '
                    f'The model returns {got} {unit}.</p></li>')

    not_public = "".join(f"<li><p>{esc(x.replace('_', ' '))}</p></li>"
                         for x in model.get("not_public", []))

    # The build brief called all three of these not public, and this page said
    # so. Two of them have monthly public figures, which is where the cross
    # check comes from. Correcting that is the difference between a limitation
    # and an excuse.
    # The statewide paragraph needs the EIA-191 storage series, which lags the
    # delivery series that sets latest_month. eia_crosscheck leaves those keys
    # absent on purpose when it does, and this paragraph indexed them anyway,
    # so an ordinary reporting lead crashed the whole site build. The delivery
    # months and the storage months are separate facts, so they are now
    # separate paragraphs and the second one waits for its data.
    # figures() drops every None-valued key, so an optional model field is
    # absent rather than empty. Two sentences indexed those keys anyway and
    # took the whole site build down with a KeyError. A model with no `fit`
    # block is a case underclaims() explicitly supports, and backtest_facts
    # sets days_at_or_above_design_day to None on purpose when the design day
    # anchor is gone. Both are now sentences that appear when their data does.
    fitted = ""
    if "fit_months" in f and "fit_mean_error_pct" in f:
        fitted = (f" Fitted by least squares to {count(f['fit_months'], 'month')}"
                  f" of observed Alaska deliveries, refit on each new one, and"
                  f" off by {f['fit_mean_error_pct']} percent on average.")

    # Same shape. This whole paragraph is about the published design day, so it
    # belongs to that anchor and goes with it if the anchor is ever dropped.
    planning_gap = ""
    if "anchor_published_design_day_mmcfd" in f:
        planning_gap = f"""<p class="prose" data-reveal>It sits below the published
planning figures, as expected. A design day of
{f["anchor_published_design_day_mmcfd"]} MMcf per day is a margin to build
against, not a prediction, and the gap is published rather than tuned
away.</p>"""

    # The comparison against the published average day, and its magnitude and
    # direction, all come from one anchor. _comparison already declines to set
    # the last two when it is missing, so the clause travels as a unit.
    against_average = ""
    if all(k in f for k in ("anchor_published_average_day_mmcfd",
                            "record_average_gap_pct", "record_average_direction")):
        against_average = (
            f" against the published average day of "
            f"{f['anchor_published_average_day_mmcfd']}, which is "
            f"{f['record_average_gap_pct']} percent "
            f"{f['record_average_direction']}")

    over_design = ""
    if "record_maximum_day_days_at_or_above_design_day" in f:
        over_design = (
            f" Of the {f['hdd_record_days']:,} days on file, "
            f"{spell(f['record_maximum_day_days_at_or_above_design_day']).lower()}"
            f" model at or above the published design day. That is a fact about"
            f" the weather, not a statement about whether the system coped.")

    statewide = ""
    if all(k in f for k in ("eia_ak_working_gas_bcf", "eia_storage_fields",
                            "eia_ak_capacity_bcf")):
        statewide = f"""
<p class="prose" data-reveal>Through {long_month(f["eia_latest_month"])} Alaska
held {f["eia_ak_working_gas_bcf"]} Bcf of working gas across
{count(f["eia_storage_fields"], "storage field")}, against
{f["eia_ak_capacity_bcf"]} Bcf of capacity. Only CINGSA reports daily.</p>"""

    if f.get("eia_months_checked"):
        not_public_note = (
            f"{spell(f['not_public_with_monthly_source'])} of them do have monthly "
            f"statewide figures, which is what the model above is fitted to. What "
            f"no source gives is a daily regional number, and that is the gap "
            f"that matters here.")
        crosscheck = f"""<h2 data-reveal>Fitted to what Alaska burned</h2>
<p class="prose" data-reveal>EIA publishes Alaska gas deliveries monthly. The
model is fitted to {count(f["eia_months_checked"], "month")} of them and refits
on each new one, so the estimate answers to measured consumption, not a design
document. The figures are statewide and two months behind, so they correct the
model, not the record here.</p>
{statewide}"""
    else:
        not_public_note = ""
        crosscheck = ""

    return f"""<div class="hero" style="min-height:auto;padding-top:9vh">
<div class="chip kind">LIVE INSTRUMENT &middot; {esc(meta["license_label"])}</div>
<h1 style="font-size:clamp(34px,5vw,60px);margin-top:14px">Cook Inlet Gas Watch</h1>
<p class="tag">A daily numeric record of Southcentral Alaska's gas position.
Measured storage, modeled demand, and the supply nobody publishes. Read
{long_date(f["as_of"])}, {count(f["days_of_record"], "day")} on record.</p>
</div>

{gauge(f)}

<!-- The primary action under the meter used to be GET THE JSON, which asks a
     reader to know what JSON is before they know what the needle means. Most
     people arriving here are reporters and Alaskans, not developers. The plain
     question they actually have goes first, and the file moves down beside the
     citation, where somebody who wants it is already looking. -->
<div class="ctarow gw-cta">
  <a class="cta gold" href="#what-this-is">WHAT THIS MEANS</a>
  <a class="cta ghost" href="{prefix}docket/{esc(meta["docket_item_id"])}/">THE STORAGE DECISION</a>
</div>

<div class="gw-stats" data-reveal>
{stat("MMcf/d withdrawal capacity", f["withdrawal_operating_mmcfd"], "measured")}
{stat("MMcf/d going in today", f["injection_in_progress_mmcfd"], "measured")}
{stat("MMcf/d modeled peak ahead", f.get("peak_modeled_demand_mmcfd", "n/a"),
      "model output", "blue")}
{stat(noun(f["days_of_record"], "day") + " on record", f["days_of_record"],
      "collected daily")}
</div>


<h2 id="what-this-is" data-reveal>What you are looking at</h2>
<div class="gw-lede" data-reveal>
<div><h3>The reserve</h3><p>Southcentral Alaska keeps gas in an underground field
near Kenai, run by CINGSA. Utilities fill it in summer and draw on it in winter.
The level is published once a day and never archived, so this page reads it and
keeps the history.</p></div>
<div><h3>The demand</h3><p>How much gas the region burns is not published at all.
It tracks how cold it is, so we model it from the Anchorage forecast and show the
formula and its errors rather than asking anyone to take it on faith.</p></div>
<div><h3>The gap</h3><p>Subtract what came out of storage from what the region
likely burned, and what is left came from somewhere nobody reports daily. That
residual is the number no other source publishes.</p></div>
</div>


<h2 data-reveal>This page will never tell you whether the lights stay on</h2>
<p class="prose" data-reveal>It publishes what is measured, what is modeled, and
what is missing. It does not publish a verdict. A compressor failure or a sanded
well can produce curtailment on a day these numbers looked comfortable, and
supply side deliverability is not public, so no adequacy conclusion can honestly
be drawn from what is here. Anyone using this data to say the region is fine, or
that it is not, is using it wrong.</p>

<h2 data-reveal>Day by day</h2>
{chart_block}
{table_html(series, model)}
{stale_note}

{balance}

{aside}

<h2 data-reveal>The model, in full</h2>
<p class="prose" data-reveal>Regional demand in MMcf per day is
{f["base_mmcfd"]} plus {f["slope_mmcfd_per_hdd"]} times heating degree days,
base {f["hdd_base_f"]} Fahrenheit. Version {f["model_version"]}.{fitted}</p>
{planning_gap}
<p class="prose" data-reveal>Every figure below is recomputed from
{f["hdd_record_days"]:,} days of observed Anchorage degree days,
{long_date(f["hdd_record_start"])} to {long_date(f["hdd_record_end"])}. Nothing
here is a number somebody typed.</p>
<ol class="claims" data-reveal>{bt_rows}</ol>
<p class="prose" data-reveal>Across that record the model averages
{f["record_average_day_mmcfd"]} MMcf per day{against_average}. The coldest
day in the record is {long_date(f["record_maximum_day_date"])} at
{f["record_maximum_day_hdd65"]:g} degree days, which models to
{f["record_maximum_day_mmcfd"]} MMcf per day.{over_design}</p>

{crosscheck}

<h2 data-reveal>What is not reported daily</h2>
<p class="prose" data-reveal>These are the things no public feed reports daily,
and their absence is why this page publishes numbers rather than conclusions.
{not_public_note}</p>
<ol class="claims" data-reveal>{not_public}</ol>

<h2 data-reveal>How to cite it</h2>
<p class="prose" data-reveal>The whole series is one JSON document at
<a class="proselink" href="{prefix}gas-watch.json">/gas-watch.json</a>, licensed
{esc(meta["license_label"])}
(<a class="proselink" href="{esc(meta["license"])}">license text</a>). It carries
the schema version, the model block with its full history, and one object per
day with the provenance of every external fetch behind it. Storage is measured,
demand is modeled, and each record says which is which. Version
{f["schema_version"]}. The related tracked decision is
<a class="proselink" href="{prefix}docket/{esc(meta["docket_item_id"])}/">Enstar's
Cook Inlet gas storage plan</a>.</p>
<div class="ctarow" data-reveal>
  <a class="cta ghost" href="{prefix}gas-watch.json">GET THE RAW DATA</a>
</div>"""



# The chart's readout layer. Small enough to inline, and it degrades to the
# static picture plus the table if it never runs.
#
# It wires EVERY .gw-plot on the page, because the chart ships as two frames
# and CSS decides which one is in the layout. The frame that is not shown gets
# no pointer and no focus, so wiring both costs nothing and neither one has to
# know which it is.
GW_JS = r"""
(function(){
  var plots = document.querySelectorAll('.gw-plot');
  for (var p = 0; p < plots.length; p++) wire(plots[p]);

  function wire(plot){
    var g;
    try { g = JSON.parse(plot.getAttribute('data-gw-plot')); } catch (e) { return; }
    if (!g || !g.n) return;
    var tip   = plot.querySelector('.gw-tip');
    var svg   = plot.querySelector('svg');
    var hit   = plot.querySelector('.gw-hit');
    var cross = plot.querySelector('.gw-cross');
    var marks = plot.querySelectorAll('.gw-mk');
    if (!tip || !svg || !hit || !cross) return;

    // On the narrow frame the readout is a line of type above the plot rather
    // than a card floating over it, so it never covers the shape a phone
    // reader is trying to see. It also stays put when the finger lifts, since
    // a touch pointer stops existing the moment it is raised and a readout
    // that vanishes with the thumb can never be read.
    var kept = g.m === 'narrow';
    var at = -1;

    function clear(){
      if (kept) return;
      cross.setAttribute('opacity', '0');
      for (var i = 0; i < marks.length; i++) marks[i].setAttribute('opacity', '0');
      tip.hidden = true;
      at = -1;
    }

    function show(i){
      i = i < 0 ? 0 : (i > g.n - 1 ? g.n - 1 : i);
      if (i === at) return;
      at = i;
      var x = g.x0 + g.dx * i;
      cross.setAttribute('x1', x);
      cross.setAttribute('x2', x);
      cross.setAttribute('opacity', '.5');
      for (var k = 0; k < marks.length; k++){
        var y = g.s[k] ? g.s[k].y[i] : null;
        if (y === null || y === undefined){ marks[k].setAttribute('opacity','0'); continue; }
        marks[k].setAttribute('cx', x);
        marks[k].setAttribute('cy', y);
        marks[k].setAttribute('opacity', '1');
      }
      hit.setAttribute('aria-valuenow', String(i));
      hit.setAttribute('aria-valuetext', g.d[i]);

      // textContent throughout. Series names are data, never markup.
      tip.textContent = '';
      var d = document.createElement('div');
      d.className = 'gw-tip-d';
      d.textContent = g.d[i];
      tip.appendChild(d);
      for (var s = 0; s < g.s.length; s++){
        var v = g.s[s].v[i];
        if (v === null || v === undefined) continue;
        var r  = document.createElement('div');  r.className = 'gw-tip-r';
        var ky = document.createElement('span'); ky.className = 'gw-tip-k';
        ky.style.background = g.s[s].c;
        var val = document.createElement('span'); val.className = 'gw-tip-v';
        val.textContent = v;
        var nm = document.createElement('span'); nm.className = 'gw-tip-n';
        nm.textContent = g.s[s].t;
        r.appendChild(ky); r.appendChild(val); r.appendChild(nm);
        tip.appendChild(r);
      }
      tip.hidden = false;
      place(x);
    }

    // The floating readout is anchored to the top of the plot rather than to
    // the day under the pointer. The surface spans every panel, so hanging the
    // readout above it put the whole card off the top edge. Pinned inside and
    // clamped horizontally, it can never be clipped on any day. The kept
    // readout sits in the flow and needs none of this.
    function place(x){
      if (kept) return;
      var pr = plot.getBoundingClientRect(), sr = svg.getBoundingClientRect();
      if (!sr.width) return;
      var px = (sr.left - pr.left) + sr.width * x / g.w, half = tip.offsetWidth / 2;
      tip.style.left = Math.max(half + 6, Math.min(pr.width - half - 6, px)) + 'px';
      tip.style.top = '6px';
    }

    // Screen pixels back to the day under them, through the frame's own scale.
    function dayAt(ev){
      var sr = svg.getBoundingClientRect();
      if (!sr.width || !g.dx) return 0;
      return Math.round(((ev.clientX - sr.left) * g.w / sr.width - g.x0) / g.dx);
    }

    hit.addEventListener('pointerdown', function(ev){
      show(dayAt(ev));
      try { hit.setPointerCapture(ev.pointerId); } catch (e) {}
    });
    // A mouse reads on hover. A touch pointer only exists while the finger is
    // down, so the same handler covers the drag without a mode of its own.
    hit.addEventListener('pointermove', function(ev){ show(dayAt(ev)); });
    hit.addEventListener('pointerleave', clear);
    hit.addEventListener('focus', function(){ show(at < 0 ? g.n - 1 : at); });
    hit.addEventListener('blur', clear);
    hit.addEventListener('keydown', function(ev){
      var to = ev.key === 'ArrowLeft'  ? at - 1
             : ev.key === 'ArrowRight' ? at + 1
             : ev.key === 'Home'       ? 0
             : ev.key === 'End'        ? g.n - 1 : null;
      if (to === null) return;
      ev.preventDefault();
      show(to);
    });

    // The kept readout opens on the latest day, so the strip is never an empty
    // box waiting to be discovered and the layout does not jump when it fills.
    if (kept) show(g.n - 1);
  }
})();
"""

GW_CSS = """
.gw-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));
gap:12px;margin:26px 0 30px;}
.gw-stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:16px 15px;border-top:2px solid var(--gold);}
.gw-stat.gw-blue{border-top-color:var(--blue);}
.gw-num{font-size:clamp(26px,3.6vw,36px);color:var(--snow);line-height:1.05;
font-weight:600;}
.gw-lab{font-size:12px;letter-spacing:.05em;text-transform:uppercase;
color:var(--body);margin-top:8px;line-height:1.35;}
.gw-note{font-size:11px;letter-spacing:.08em;text-transform:uppercase;
color:var(--mute);margin-top:6px;}
.gw-lede{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
gap:16px;margin:16px 0 30px;}
.gw-lede>div{background:var(--panel);border:1px solid var(--line);
border-radius:12px;padding:18px 17px;}
.gw-lede h3{font-family:Fraunces,Georgia,serif;font-size:19px;color:var(--gold);
margin-bottom:8px;font-weight:500;}
.gw-lede p{font-size:15px;color:var(--body);line-height:1.6;}
/* THE METER.
   A bar and never a dial, because a dial implies a red zone and a red zone is
   a verdict this page does not get to publish. For the same reason the fill
   carries no severity ramp: the standard meter runs accent to warning to
   danger with magnitude, and doing that here would colour 30 percent as alarm
   and 80 as safe, which is exactly the judgement the data cannot support. One
   hue at one intensity at every value. The LENGTH is the whole message.

   The unfilled track is meant to be a lighter step of the fill's own ramp, so
   the vessel reads across its full width instead of the fill floating on a
   void. On this palette that rule cannot be followed literally: gold over navy
   composites to olive at every alpha worth using, #263237 at ten percent and
   #323a36 at fifteen, which is mud. So the track is a lighter step of the
   SURFACE and the gold family is carried by a warm rim and the fill itself.
   The purpose of the rule is kept; the letter of it would have looked worse.

   No outer glow on the fill. The first pass had a 26px gold bloom that spilled
   across the empty track and turned the boundary between full and empty, the
   one edge a reader actually measures, into a brown smear. */
.gw-gauge{position:relative;overflow:hidden;
background:
  radial-gradient(130% 160% at 0% 0%,rgba(255,199,44,.09),transparent 55%),
  linear-gradient(180deg,var(--panel2),var(--panel));
border:1px solid var(--line);border-radius:18px;
padding:20px 24px 18px;margin:20px 0 22px;
box-shadow:0 18px 44px -28px rgba(0,0,0,.9);}
.gw-gauge::before{content:"";position:absolute;inset:0 0 auto 0;height:1px;
background:linear-gradient(90deg,var(--gold),rgba(255,199,44,.16) 62%,transparent);}
.gw-cta{margin-bottom:34px;}

.gw-gauge-head{display:flex;justify-content:space-between;align-items:baseline;
gap:12px;flex-wrap:wrap;font-size:11px;letter-spacing:.14em;
text-transform:uppercase;font-family:JBMono,ui-monospace,monospace;}
.gw-gauge-what{color:var(--halo);}
.gw-gauge-when{color:var(--mute);}

/* The hero and its qualifiers sit together on the left and share a baseline.
   Right-aligning the second block put 500px of nothing between two numbers
   that describe the same reading. */
.gw-gauge-read{display:flex;align-items:flex-end;gap:20px;flex-wrap:wrap;
margin:10px 0 18px;}
.gw-hero{font-size:clamp(56px,9vw,88px);line-height:.82;color:var(--gold);
font-weight:800;letter-spacing:-.035em;font-variant-numeric:proportional-nums;}
.gw-hero span{font-size:.34em;color:var(--halo);margin-left:3px;font-weight:600;
letter-spacing:0;}
.gw-gauge-of{display:flex;flex-direction:column;gap:4px;padding-bottom:5px;
border-left:1px solid var(--line);padding-left:20px;}
.gw-gauge-of-lab{font-size:11px;letter-spacing:.12em;text-transform:uppercase;
color:var(--mute);font-family:JBMono,ui-monospace,monospace;}
.gw-gauge-of-num{font-size:clamp(20px,2.4vw,26px);color:var(--snow);
font-weight:600;font-variant-numeric:proportional-nums;line-height:1.1;}
.gw-gauge-of-num i{color:var(--mute);font-size:.7em;font-weight:400;
font-style:normal;}
/* Pushed to the far right so the reading row reads left to right as level,
   then volume, then what it did today. */
.gw-gauge-move{margin-left:auto;text-align:right;display:flex;
flex-direction:column;gap:4px;padding-bottom:5px;}
.gw-gauge-move-num{font-size:clamp(18px,2.1vw,23px);color:var(--halo);
font-weight:600;font-variant-numeric:proportional-nums;line-height:1.15;}
.gw-gauge-move-num i{display:block;color:var(--mute);font-size:.55em;
font-weight:400;font-style:normal;letter-spacing:.08em;text-transform:uppercase;
margin-top:2px;}

.gw-gauge-track{position:relative;height:38px;border-radius:7px;
background:linear-gradient(180deg,#22314a,#1a2740);
box-shadow:inset 0 1px 0 rgba(255,218,110,.22),
           inset 0 -1px 0 rgba(0,0,0,.35),
           inset 0 12px 20px -14px rgba(0,0,0,.75);}
.gw-gauge-fill{position:absolute;inset:0 auto 0 0;width:var(--pct);
border-radius:6px 2px 2px 6px;
background:linear-gradient(180deg,var(--halo),var(--gold) 58%,#e6a911);
animation:gwfill .9s cubic-bezier(.2,.75,.25,1) both;}
/* The meniscus. The one pixel a reader measures against the ticks below, so it
   is the brightest thing on the bar and nothing blooms across it. */
.gw-gauge-fill::after{content:"";position:absolute;inset:0 0 0 auto;width:2px;
background:#fff6d8;}
@keyframes gwfill{from{width:0;}to{width:var(--pct);}}
@media(prefers-reduced-motion:reduce){.gw-gauge-fill{animation:none;}}

/* The reading rides inside the fill, against its leading edge, which is where
   a reader is already looking. A flag floating above the bar collided with the
   track and needed the value repeated a third time to make sense. */
.gw-gauge-flag{position:absolute;top:0;bottom:0;left:0;width:var(--pct);
display:flex;align-items:center;justify-content:flex-end;
padding-right:10px;pointer-events:none;}
.gw-gauge-flag-num{font-size:12px;font-weight:700;letter-spacing:.06em;
color:#3a2a02;font-variant-numeric:proportional-nums;
font-family:JBMono,ui-monospace,monospace;}
/* Too little gas to letter inside, so the number steps out onto the track. */
.gw-gauge-flag.is-left{width:auto;left:var(--pct);padding-right:0;padding-left:10px;
justify-content:flex-start;}
.gw-gauge-flag.is-left .gw-gauge-flag-num{color:var(--halo);}

.gw-gauge-axis{display:flex;justify-content:space-between;height:8px;}
.gw-gauge-axis span{width:1px;height:4px;background:#22344e;}
.gw-gauge-axis span:first-child,.gw-gauge-axis span:last-child,
.gw-gauge-axis span:nth-child(3){height:8px;background:#2c4a6e;}
.gw-gauge-foot{display:flex;justify-content:space-between;gap:10px;margin-top:1px;
font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);
font-family:JBMono,ui-monospace,monospace;}
.gw-gauge-cap{color:var(--body);}
@media(max-width:560px){
  .gw-gauge{padding:18px 15px 16px;}
  .gw-gauge-read{gap:14px;}
  .gw-gauge-of{border-left:0;padding-left:0;}
  .gw-gauge-move{margin-left:0;text-align:left;flex-direction:row;
  align-items:baseline;gap:8px;flex-wrap:wrap;}
  /* One line on a phone. Stacked, the unit and its direction cost three rows
     for a figure that is a footnote to the level above it. */
  .gw-gauge-move-num i{display:inline;font-size:.6em;margin-top:0;}
}
.gw-chart{background:var(--panel);border:1px solid var(--line);border-radius:14px;
padding:16px 12px 8px;margin:18px 0;}
/* THE READOUT LAYER. An HTML chart is interactive by default, and without this
   the only way to read a middle day was to count gridlines. The crosshair
   snaps to the nearest date so the pointer aims at a day rather than at a 2px
   line, and one readout carries every panel for that day. Everything it shows
   is also in the table below, so it enhances and never gates. */
.gw-plot{position:relative;}
.gw-plot svg{display:block;width:100%;height:auto;}
/* WHICH FRAME IS IN THE LAYOUT. Exactly one, so the other leaves the tab order
   and the accessibility tree with it and nothing is announced twice.

   The old rule floored the plot at 600px and let the CARD scroll sideways,
   which kept the type legible and cost a phone reader the thing the picture is
   for. At 390px they saw a little over half the series and had to swipe to
   learn the shape of the rest. The narrow frame is drawn at phone proportions
   instead, so the whole record fits with no scroll at any width and the type
   is bigger than it was before. The breakpoint is where the wide frame stops
   fitting comfortably rather than a round number, and above it the wide frame
   renders exactly as it always has. */
.gw-narrow{display:none;}
@media(max-width:760px){
  .gw-wide{display:none;}
  .gw-narrow{display:block;}
  /* Past about a 560px card the narrow frame is scaling type up rather than
     showing more, so it stops growing and centres. */
  .gw-narrow svg{max-width:560px;margin:0 auto;}
}
/* pan-y, not none. A drag across the chart reads it day by day, and a swipe up
   the page still scrolls the page, which is the gesture a reader is far more
   likely to want on a surface this tall. */
.gw-hit{cursor:crosshair;touch-action:pan-y;}
.gw-hit:focus{outline:none;}
.gw-hit:focus-visible{outline:2px solid var(--halo);outline-offset:-2px;}
.gw-tip{position:absolute;z-index:3;pointer-events:none;min-width:190px;
background:rgba(5,11,22,.97);border:1px solid var(--line);border-radius:10px;
padding:10px 12px;box-shadow:0 18px 40px -20px #000;
transform:translate(-50%,0);}
/* On the narrow frame the readout is a line of type above the plot, not a card
   over it. A floating tooltip under a thumb covers the panel it is describing,
   and on a 316px chart there is nowhere to move it to. */
.gw-narrow .gw-tip{position:static;transform:none;min-width:0;z-index:auto;
background:none;border:0;border-radius:0;box-shadow:none;padding:0 2px 10px;
display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px;}
.gw-narrow .gw-tip-d{margin-bottom:0;width:100%;}
.gw-narrow .gw-tip-r{margin-top:0;}
/* An author display beats the hidden attribute, so the strip needs this or a
   reader with no script gets an empty box holding open space under a heading.
   The chart degrades to the picture and the table, which is the whole point of
   the readout being an enhancement. */
.gw-tip[hidden]{display:none;}
.gw-tip-d{font-size:11px;letter-spacing:.09em;text-transform:uppercase;
color:var(--mute);font-family:JBMono,ui-monospace,monospace;
margin-bottom:7px;white-space:nowrap;}
.gw-tip-r{display:flex;align-items:baseline;gap:9px;white-space:nowrap;
margin-top:5px;}
/* A short stroke of the series colour, not a filled box. At tooltip density a
   box is data-weight ink doing a label's job. */
.gw-tip-k{width:12px;height:2px;border-radius:1px;flex:none;}
/* Value leads, series name follows. The reader has the series and wants the
   number, which is the legend's hierarchy inverted. */
.gw-tip-v{color:var(--snow);font-weight:700;font-size:14px;
font-variant-numeric:proportional-nums;}
.gw-tip-n{color:var(--mute);font-size:11px;letter-spacing:.05em;
text-transform:uppercase;}
/* Five numeric columns do not fit a phone, so the wrapper scrolls. A reader
   who cannot see that it scrolls is a reader for whom the last two columns do
   not exist, so the edges carry the standard local-background scroll shadow.
   background-attachment local on the covers and scroll on the shadows is what
   makes it self-cancelling, the shadow showing only while there is more to
   reach, with no script and nothing to keep in sync. */
.gw-table{margin:18px 0 8px;overflow-x:auto;
background:
 linear-gradient(to right,var(--deep) 40%,rgba(2,6,15,0)) left center,
 linear-gradient(to left,var(--deep) 40%,rgba(2,6,15,0)) right center,
 radial-gradient(farthest-side at 0 50%,rgba(141,162,190,.42),rgba(141,162,190,0)) left center,
 radial-gradient(farthest-side at 100% 50%,rgba(141,162,190,.42),rgba(141,162,190,0)) right center;
background-repeat:no-repeat;
background-size:26px 100%,26px 100%,16px 100%,16px 100%;
background-attachment:local,local,scroll,scroll;}
.gw-table table{width:100%;border-collapse:collapse;font-size:14px;
font-variant-numeric:tabular-nums;}
.gw-vh{position:absolute;width:1px;height:1px;margin:-1px;padding:0;
overflow:hidden;clip-path:inset(50%);white-space:nowrap;border:0;}
.gw-tnote{margin:10px 0 8px;text-align:left;color:var(--mute);
font-size:13px;line-height:1.5;}
.gw-table th,.gw-table td{padding:9px 11px;border-bottom:1px solid var(--line);
text-align:right;white-space:nowrap;}
.gw-table th:first-child,.gw-table td:first-child{text-align:left;}
.gw-table thead th{color:var(--mute);font-size:11px;letter-spacing:.05em;
text-transform:uppercase;font-weight:500;}
.gw-table tbody tr:hover{background:var(--panel);}
"""


def main():
    ap = argparse.ArgumentParser(description="Cook Inlet Gas Watch page library")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    figs = figures(load_series(), gc.load_model(MODEL_CONFIG))
    print(json.dumps(figs, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
