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
    for key in ("record_average_direction", "record_average_gap_pct"):
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
    # The axis. Same bounds call the chart makes, on the same two series, so
    # the ticks are authorised by the data rather than by their appearance.
    if len(rows) >= 2:
        for vals in ([round(r["cingsa"]["inventory_mcf"] / 1_000_000, 2) for r in rows],
                     [remodel(r, model)[0].get("peak_modeled_demand_mmcfd")
                      for r in rows]):
            have = [v for v in vals if v is not None]
            if not have:
                continue
            _, _, ticks = nice_bounds(min(have) * 0.98, max(have) * 1.02)
            rendered += [f"{t:g}" for t in ticks] + [str(t) for t in ticks]
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

def nice_bounds(lo, hi, ticks=4):
    """Axis bounds and tick values on round numbers, computed not chosen."""
    # A span that is flat, or so narrow it is flat relative to its own
    # magnitude, cannot produce a readable axis and rounds badly besides.
    # Storage barely moves day to day, so this is the ordinary case early in
    # the series, not an exotic one.
    if hi - lo <= max(abs(lo), abs(hi), 1.0) * 1e-4:
        hi = lo + max(abs(lo) * 0.01, 1.0)
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


def chart_svg(series, model, w=920, panel_h=150, gap=34):
    """Storage and modeled demand as small multiples on a shared time axis.

    TWO PANELS, ONE SCALE EACH. The first draft of this plotted both on one
    frame with storage on the left axis and demand on the right, which is a
    dual axis chart. The alignment of two y scales is arbitrary, so the reader
    sees a correlation the data never claimed. Small multiples say the same
    thing without inventing the relationship.

    Colour. Both marks are the site's brand accents. Against the panel surface
    they clear the 3 to 1 contrast floor and, being one series per panel, there
    is no adjacent pair to separate, which is the case the categorical
    lightness band is scoped to. Deeper in band steps of the same hues were
    generated and rejected as less legible on a surface this close to black.

    Below two points there is no trend to draw, so the caller falls back to the
    meter and the stat tiles rather than plotting a line through one dot.
    """
    # Storage rounded to the two decimals the table shows. The direct label
    # renders this value with :g, so an unrounded 6.423571 would have printed
    # every digit on the chart and matched nothing the lint could authorise.
    pts = [(r["date"], round(r["cingsa"]["inventory_mcf"] / 1_000_000, 2),
            remodel(r, model)[0].get("peak_modeled_demand_mmcfd"))
           for r in series
           if r.get("verified") and (r.get("cingsa") or {}).get("inventory_mcf")]
    if len(pts) < 2:
        return ""

    pad_l, pad_r, pad_b = 64, 16, 30
    iw = w - pad_l - pad_r
    n = len(pts)
    h = panel_h * 2 + gap + pad_b
    MONO = 'font-size="11" font-family="JBMono,monospace"'

    def x(i):
        return pad_l + iw * i / (n - 1)

    def panel(top, vals, title, unit, colour, fill_id):
        have = [(i, v) for i, v in vals if v is not None]
        if not have:
            return ""
        lo, hi, ticks = nice_bounds(min(v for _, v in have) * 0.98,
                                    max(v for _, v in have) * 1.02)

        def y(v):
            return top + panel_h - panel_h * (v - lo) / (hi - lo)

        # Solid hairlines one shade off the surface. Dashed grid reads as a
        # threshold when it is only a grid.
        g = "".join(
            f'<line x1="{pad_l}" y1="{y(t):.1f}" x2="{pad_l + iw}" y2="{y(t):.1f}" '
            f'stroke="#152a44" stroke-width="1"/>'
            f'<text x="{pad_l - 10}" y="{y(t) + 4:.1f}" text-anchor="end" '
            f'fill="#8da2be" {MONO}>{t:g}</text>' for t in ticks)
        d = " ".join(f'{"M" if k == 0 else "L"}{x(i):.1f},{y(v):.1f}'
                     for k, (i, v) in enumerate(have))
        area = (f'{d} L{x(have[-1][0]):.1f},{top + panel_h} '
                f'L{x(have[0][0]):.1f},{top + panel_h} Z')
        # One direct label, on the latest point, which is the value a reader
        # came for. A number on every point is noise.
        li, lv = have[-1]
        return f"""<path d="{area}" fill="url(#{fill_id})"/>{g}
<path d="{d}" fill="none" stroke="{colour}" stroke-width="2"
 stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="{x(li):.1f}" cy="{y(lv):.1f}" r="4.5" fill="{colour}"
 stroke="#0a1626" stroke-width="2"/>
<text x="{pad_l}" y="{top - 8}" fill="#f4f8ff" {MONO}>{title}</text>
<text x="{pad_l + iw}" y="{top - 8}" text-anchor="end" fill="#8da2be" {MONO}>{unit}</text>
<text x="{x(li) - 9:.1f}" y="{y(lv) - 10:.1f}" text-anchor="end" fill="{colour}"
 {MONO}>{lv:g}</text>"""

    top1, top2 = 22, 22 + panel_h + gap
    p1 = panel(top1, [(i, p[1]) for i, p in enumerate(pts)],
               "MEASURED STORAGE", "Bcf", "#ffc72c", "gwA")
    p2 = panel(top2, [(i, p[2]) for i, p in enumerate(pts)],
               "MODELED PEAK DEMAND", "MMcf per day", "#5ac8f0", "gwB")

    dates = "".join(
        f'<text x="{x(i):.1f}" y="{h - 9}" '
        f'text-anchor="{"start" if i == 0 else "end"}" fill="#8da2be" {MONO}>'
        f'{pts[i][0]}</text>' for i in (0, n - 1))

    return f"""<svg viewBox="0 0 {w} {h}" width="100%" role="img"
 aria-label="Two charts sharing one time axis. Measured Cook Inlet storage
 inventory in Bcf, and modeled peak daily demand in MMcf per day. The same
 values are in the table below."
 style="max-width:100%;height:auto;display:block">
<defs>
<linearGradient id="gwA" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#ffc72c" stop-opacity=".20"/>
<stop offset="1" stop-color="#ffc72c" stop-opacity="0"/></linearGradient>
<linearGradient id="gwB" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#5ac8f0" stop-opacity=".16"/>
<stop offset="1" stop-color="#5ac8f0" stop-opacity="0"/></linearGradient>
</defs>
{p1}{p2}{dates}</svg>"""


def table_html(series, model, limit=TABLE_LIMIT):
    """The table view twin. Every plotted value readable without the chart.

    This is also the form a reporter actually wants, since it can be copied
    into a story without reading pixels off a line.
    """
    rows = [r for r in series if r.get("verified")][-limit:]
    if not rows:
        return ""
    body = ""
    gaps = 0
    for r in rows:
        cin = r["cingsa"]
        der, rec = remodel(r, model)
        if der.get("peak_modeled_demand_mmcfd") is None or \
                rec.get("non_cingsa_supply_mmcfd") is None:
            gaps += 1
        body += (
            f'<tr><td>{esc(r["date"])}</td>'
            f'<td>{round(cin["inventory_mcf"] / 1_000_000, 2)}</td>'
            f'<td>{cin["inventory_pct_of_design"]}</td>'
            f'<td>{blank(der.get("peak_modeled_demand_mmcfd"))}</td>'
            f'<td>{blank(rec.get("non_cingsa_supply_mmcfd"))}</td></tr>')
    # An empty cell is deliberate (see blank()), but on a short table it reads
    # as data this page failed to collect rather than as a figure the model had
    # no input for. One sentence, shown only when a cell is actually empty, and
    # it names no specific input so no arrangement of the data can falsify it.
    gap_note = (" A blank cell is a figure the model had no input for that day,"
                " not a reading that went missing." if gaps else "")
    return f"""<div class="gw-table" data-reveal>
<table>
<caption>The most recent {count(len(rows), "verified reading")}. Storage and percent of
design are measured. Modeled peak and non CINGSA supply are model output.{gap_note}</caption>
<thead><tr><th scope="col">Date</th><th scope="col">Storage Bcf</th>
<th scope="col">Percent of design</th><th scope="col">Modeled peak MMcf/d</th>
<th scope="col">Non CINGSA supply MMcf/d</th></tr></thead>
<tbody>{body}</tbody></table></div>"""


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

    print("the numeral lint")
    model = gc.load_model(MODEL_CONFIG)
    figs = figures(load_series(), model)
    allowed = allowed_numerals(figs, model, ["CC BY 4.0"])
    check("a figure drawn from the data passes",
          not numeral_lint(f"<p>Storage holds {figs.get('inventory_bcf')} Bcf.</p>",
                           allowed))
    planted = numeral_lint("<p>Storage sits at 87.3 percent of design.</p>", allowed)
    check("a number nothing computed is caught", bool(planted), str(planted))
    check("chart geometry is not mistaken for prose",
          not numeral_lint(chart_svg(load_series(), model), allowed))
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
    return f"""<div class="gw-gauge" data-reveal>
<div class="gw-gauge-top">
  <div>
    <div class="gw-hero">{pct}<span>%</span></div>
    <div class="gw-hero-lab">of design capacity, measured</div>
  </div>
  <div class="gw-gauge-side">
    <div class="gw-side-num">{f["inventory_bcf"]} <span>of {f["design_bcf"]} Bcf</span></div>
    <div class="gw-side-lab">Cook Inlet storage, read {long_date(f["as_of"])}</div>
  </div>
</div>
<div class="gw-gauge-track"><div class="gw-gauge-fill" style="width:{pct}%"></div>
<div class="gw-gauge-mark" style="left:{pct}%"></div></div>
<div class="gw-gauge-foot"><span>empty</span>
<span>full, {f["design_bcf"]} Bcf</span></div>
</div>"""


def home_strip(series, model, prefix="", figs=None):
    """The storage meter for the homepage, under the docket.

    Same figures dict as the page, so the two can never disagree. It renders
    nothing at all when there is no verified reading, because a homepage is the
    last place to explain an absence.
    """
    f = figures(series, model, figs)
    if "as_of" not in f:
        return ""
    pct = f["inventory_pct_of_design"]
    return f"""<h2 data-reveal><a href="{prefix}gas-watch/">Cook Inlet Gas Watch</a></h2>
<p class="sub" data-reveal>How much gas Southcentral has in the ground, read every
day and kept. CINGSA publishes today's number and no history, so this record
exists only because it is collected daily.</p>
<div class="gw-gauge" data-reveal>
<div class="gw-gauge-top">
  <div>
    <div class="gw-hero">{pct}<span>%</span></div>
    <div class="gw-hero-lab">of design capacity, measured</div>
  </div>
  <div class="gw-gauge-side">
    <div class="gw-side-num">{f["inventory_bcf"]} <span>of {f["design_bcf"]} Bcf</span></div>
    <div class="gw-side-lab">read {long_date(f["as_of"])}</div>
  </div>
</div>
<div class="gw-gauge-track"><div class="gw-gauge-fill" style="width:{pct}%"></div>
<div class="gw-gauge-mark" style="left:{pct}%"></div></div>
<div class="gw-gauge-foot"><span>empty</span>
<span>full, {f["design_bcf"]} Bcf</span></div>
</div>
<div class="ctarow" data-reveal><a class="cta ghost" href="{prefix}gas-watch/">OPEN THE GAS WATCH</a></div>"""


def page_body(today, site_url, series, model, meta, prefix="../", figs=None):
    """The Gas Watch page.

    Structure follows what a reporter on deadline needs, in order. What the
    number is, when it was read, where it came from, how the modeled parts were
    derived, and what nobody can see. The methodology is not an appendix here,
    it is the product.
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
    svg = chart_svg(series, model)
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

    # The model's live scoreboard. At zero checks it says zero, because an
    # accuracy figure nobody has earned yet is exactly the kind of claim this
    # page refuses to make.
    if f.get("accuracy_checks"):
        scoreboard = (
            f'Across {count(f["accuracy_checks"], "day")} the forecast behind it '
            f'has been off by {f["mean_abs_hdd_error"]} degree days on average, '
            f'about {f["mean_abs_demand_error_mmcfd"]} MMcf per day of gas.')
        scoreboard = " " + scoreboard
    else:
        # Say nothing rather than narrate the site's own newness. A sentence
        # promising that a check "lands shortly" is scaffolding on a page meant
        # to outlive the week it launched, and the paragraph reads fine without
        # it. The figure appears on its own once there is one to report.
        scoreboard = ""

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
        balance = f"""<h2 data-reveal>What is not measured by anyone</h2>
<p class="prose" data-reveal>Demand equals field production plus storage
withdrawal. Storage withdrawal is measured, and demand is modeled, so
everything that is not CINGSA falls out by subtraction. On
{long_date(f["balance_date"])} that residual came to
{f["non_cingsa_supply_mmcfd"]} MMcf per day against modeled demand of
{f["modeled_demand_mmcfd"]} MMcf per day, which is
{f["unmeasured_share_pct"]} percent of the region's gas arriving from sources
no public feed reports daily. That share is the size of the hole in the public
record, and it is the reason this page draws no conclusion about adequacy.</p>
<p class="prose" data-reveal>Strictly, the residual is field production plus any
Hilcorp storage movement combined. The two cannot be separated from public data,
which is why the field is named non_cingsa_supply and is never called
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
                  f" of observed Alaska deliveries to homes, businesses and power"
                  f" plants, and refitted every time another month is published."
                  f" It misses those months by {f['fit_mean_error_pct']} percent"
                  f" on average, measured against the same record it is fitted"
                  f" to.")

    # Same shape. This whole paragraph is about the published design day, so it
    # belongs to that anchor and goes with it if the anchor is ever dropped.
    planning_gap = ""
    if "anchor_published_design_day_mmcfd" in f:
        planning_gap = f"""<p class="prose" data-reveal>It sits below the published
planning figures, and that is expected rather than a problem. A design day of
{f["anchor_published_design_day_mmcfd"]} MMcf per day is a peak carrying margin
for a system operator to build against. This predicts what the region actually
uses, which is a different question, and the gap between them is published here
instead of tuned away.</p>"""

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
<p class="prose" data-reveal>It also widens the picture. Through
{long_month(f["eia_latest_month"])} Alaska held {f["eia_ak_working_gas_bcf"]} Bcf
of working gas across {count(f["eia_storage_fields"], "storage field")}, against
{f["eia_ak_capacity_bcf"]} Bcf of capacity. CINGSA is the only one that reports
daily, and its {f["design_bcf"]} Bcf field is the one read here every morning.
The rest surfaces monthly at best, which is why the daily record starts here.</p>"""

    if f.get("eia_months_checked"):
        not_public_note = (
            f"{spell(f['not_public_with_monthly_source'])} of them do have monthly "
            f"statewide figures, which is what the model above is fitted to. What "
            f"no source gives is a daily regional number, and that is the gap "
            f"that matters here.")
        crosscheck = f"""<h2 data-reveal>Fitted to what Alaska burned</h2>
<p class="prose" data-reveal>The US Energy Information Administration publishes
Alaska gas deliveries and underground storage monthly.
{count(f["eia_months_checked"], "month")} of those deliveries to homes,
businesses and power plants are what the demand model is fitted to, and each new
month refits it. So the estimate answers to measured consumption rather than to a
design document. The figures are statewide and lag about two months, which is why
they correct the model rather than replace anything here.</p>
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

<h2 data-reveal>The model, in full</h2>
<p class="prose" data-reveal>Regional demand in MMcf per day is
{f["base_mmcfd"]} plus {f["slope_mmcfd_per_hdd"]} times heating degree days on a
base of {f["hdd_base_f"]} degrees Fahrenheit. Version {f["model_version"]}.{fitted}</p>
{planning_gap}
<p class="prose" data-reveal>Every figure below is recomputed at build time from
{f["hdd_record_days"]:,} days of observed Anchorage degree days covering
{long_date(f["hdd_record_start"])} to {long_date(f["hdd_record_end"])}. Nothing
on this page is a number somebody typed.</p>
<ol class="claims" data-reveal>{bt_rows}</ol>
<p class="prose" data-reveal>Across that record the model averages
{f["record_average_day_mmcfd"]} MMcf per day{against_average}. The coldest
day in the record is {long_date(f["record_maximum_day_date"])} at
{f["record_maximum_day_hdd65"]:g} degree days, which models to
{f["record_maximum_day_mmcfd"]} MMcf per day.{over_design}</p>

<h2 data-reveal>This gets sharper the longer it runs</h2>
<p class="prose" data-reveal>It launched {long_date(f["first_date"])} with a
single day of readings, and every day adds one more. That record is the whole
point. CINGSA publishes today's number and keeps no history at all, so the
trend on this page exists only because it is collected daily and never thrown
away. One day is a dot. A month shows the shape of a drawdown. A winter shows
what a cold snap actually costs the field, and no other public source can show
you that.</p>
<p class="prose" data-reveal>The demand figure is an estimate, so rather than
ask you to trust it we fit it to what Alaska actually burned and publish how far
off it still is.{scoreboard} When the record says the estimate should move,
we move it, and every earlier version stays on file so an old number can still
be reproduced.</p>
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
.gw-gauge{background:linear-gradient(180deg,var(--panel2),var(--panel));
border:1px solid var(--line);border-top:2px solid var(--gold);border-radius:16px;
padding:24px 22px 18px;margin:20px 0 22px;}
.gw-cta{margin-bottom:34px;}
.gw-gauge-top{display:flex;justify-content:space-between;align-items:flex-end;
gap:20px;flex-wrap:wrap;margin-bottom:18px;}
/* Hero figure. Body sans rather than the serif, and proportional digits, which
   is what stops a large standalone number reading loose. */
.gw-hero{font-size:clamp(52px,9vw,86px);line-height:.92;color:var(--gold);
font-weight:700;letter-spacing:-.02em;font-variant-numeric:proportional-nums;}
.gw-hero span{font-size:.42em;color:var(--halo);margin-left:2px;font-weight:600;}
.gw-hero-lab{font-size:13px;letter-spacing:.08em;text-transform:uppercase;
color:var(--body);margin-top:9px;}
.gw-gauge-side{text-align:right;}
.gw-side-num{font-size:clamp(20px,2.6vw,26px);color:var(--snow);font-weight:600;}
.gw-side-num span{color:var(--mute);font-size:.7em;font-weight:400;}
.gw-side-lab{font-size:12px;letter-spacing:.05em;text-transform:uppercase;
color:var(--mute);margin-top:7px;}
.gw-gauge-track{position:relative;height:30px;border-radius:15px;
background:var(--deep);border:1px solid var(--line);overflow:hidden;}
/* Both stops are bright. The first version ramped from a dark gold on the
   left, which dimmed the end of the bar the eye starts at and encoded nothing,
   since the bar's LENGTH already carries the value. The sheen is decoration
   that stays out of the way of the measurement. */
.gw-gauge-fill{height:100%;border-radius:15px 0 0 15px;
background:linear-gradient(90deg,var(--gold),var(--halo));
box-shadow:0 0 18px rgba(255,199,44,.25);}
.gw-gauge-mark{position:absolute;top:-3px;bottom:-3px;width:2px;
background:var(--snow);}
.gw-gauge-foot{display:flex;justify-content:space-between;gap:10px;margin-top:9px;
font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--mute);}
.gw-gauge-foot span:last-child{color:var(--body);}
@media(max-width:560px){.gw-gauge-side{text-align:left;}}
.gw-chart{background:var(--panel);border:1px solid var(--line);border-radius:14px;
padding:16px 12px 8px;margin:18px 0;overflow-x:auto;}
.gw-table{margin:18px 0 8px;overflow-x:auto;}
.gw-table table{width:100%;border-collapse:collapse;font-size:14px;
font-variant-numeric:tabular-nums;}
.gw-table caption{caption-side:bottom;text-align:left;color:var(--mute);
font-size:13px;padding-top:10px;line-height:1.5;}
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
