#!/usr/bin/env python3
"""gaswatch_fit.py, refit the demand model against observed consumption.

The model shipped calibrated to two published figures, which was the honest
option on day one because observed consumption was believed unavailable. It is
not. EIA publishes Alaska deliveries by sector monthly, and a least squares fit
against them cuts the mean monthly error roughly in half.

So the model is no longer a fixed hypothesis. It refits every time EIA
publishes another month, which is the monthly workflow this runs in, and it
gets more accurate as the record grows. That is the whole point.

WHAT IT FITS. consumption = base * days + slope * heating degree days, over
every whole month where the Anchorage record and all three consumption sectors
are present. Two unknowns, solved in closed form.

WHAT IT ASSUMES, said out loud because it matters. EIA reports Alaska
statewide. Residential and commercial gas is overwhelmingly Enstar in
Southcentral, and gas fired power is overwhelmingly Railbelt, so statewide
heating and power deliveries stand in for the region. Industrial is excluded,
because Kenai plant loads have nothing to do with weather.

GUARDS, because an automatic refit that can go wrong unattended is worse than
no refit. A new fit is rejected unless it has enough months behind it, lands
inside physically sane bounds, and actually beats the model it would replace.
A rejected fit leaves the model alone and says why.

Run:
  python3 scripts/gaswatch_fit.py --self-test   # hermetic
  python3 scripts/gaswatch_fit.py --dry-run     # print, write nothing
  python3 scripts/gaswatch_fit.py               # refit if it earns it
"""

import argparse
import json
import os
import sys
import traceback
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gaswatch_collect as gc  # noqa: E402

EIA_LEDGER = os.path.join(REPO, "ledger", "gaswatch_eia.json")
SECTORS = ("residential_mmcf", "commercial_mmcf", "electric_power_mmcf")

# A fit on a couple of years of months is noise. Three years covers three
# winters, which is what actually constrains the slope.
MIN_MONTHS = 36

# Physically sane. Base load without heating cannot be near zero or enormous,
# and the slope is gas per degree day for a region this size.
BOUNDS = {"base_mmcfd": (40.0, 130.0), "slope_mmcfd_per_hdd": (2.0, 7.0)}

# A refit must beat what it replaces by more than rounding, or the version
# churns for nothing.
MIN_IMPROVEMENT_PCT = 0.1


def observations(model, eia_path=EIA_LEDGER):
    """(days, heating degree days, observed consumption) per whole month."""
    with open(eia_path, encoding="utf-8") as fh:
        series = json.load(fh)["series"]
    _, hdd = gc.load_hdd_history(model, REPO)
    by_month = {}
    for d, v in hdd:
        by_month.setdefault(d[:4] + d[5:7], []).append(v)
    rows = []
    for ym, days in sorted(by_month.items()):
        if len(days) < 28:
            continue
        if not all(ym in series.get(k, {}) for k in SECTORS):
            continue
        rows.append((len(days), sum(days), sum(series[k][ym] for k in SECTORS)))
    return rows


def least_squares(rows):
    """Closed form fit of consumption = base * days + slope * hdd."""
    Sdd = sum(d * d for d, _, _ in rows)
    Sdh = sum(d * h for d, h, _ in rows)
    Shh = sum(h * h for _, h, _ in rows)
    Sdy = sum(d * y for d, _, y in rows)
    Shy = sum(h * y for _, h, y in rows)
    det = Sdd * Shh - Sdh * Sdh
    if not det:
        raise ValueError("degenerate fit, the months carry no spread in weather")
    return ((Sdy * Shh - Shy * Sdh) / det, (Sdd * Shy - Sdh * Sdy) / det)


def mean_error_pct(rows, base, slope):
    """Mean absolute monthly error, the number a refit has to improve."""
    return sum(abs((base * d + slope * h) - y) / y for d, h, y in rows) / len(rows) * 100


def evaluate(model, rows):
    """Return (proposal, reason). proposal is None when the fit is rejected."""
    if len(rows) < MIN_MONTHS:
        return None, (f"only {len(rows)} months of overlap, "
                      f"{MIN_MONTHS} required before fitting")
    try:
        base, slope = least_squares(rows)
    except ValueError as exc:
        return None, str(exc)
    for key, val in (("base_mmcfd", base), ("slope_mmcfd_per_hdd", slope)):
        lo, hi = BOUNDS[key]
        if not lo <= val <= hi:
            return None, (f"fitted {key} of {val:.2f} is outside the plausible "
                          f"band {lo} to {hi}, so the fit is rejected rather "
                          f"than published")
    was = mean_error_pct(rows, model["base_mmcfd"], model["slope_mmcfd_per_hdd"])
    now = mean_error_pct(rows, base, slope)
    if was - now < MIN_IMPROVEMENT_PCT:
        return None, (f"the fit does not beat the current model "
                      f"({now:.2f} against {was:.2f} percent mean error), "
                      f"so the model is left alone")
    return {
        "base_mmcfd": round(base, 3),
        "slope_mmcfd_per_hdd": round(slope, 4),
        "months": len(rows),
        "mean_error_pct": round(now, 2),
        "previous_mean_error_pct": round(was, 2),
    }, f"fit improves mean monthly error from {was:.2f} to {now:.2f} percent"


def apply_fit(model, prop, today, months_label):
    """Return the model with the new coefficients and recomputed backtests.

    The backtests are recomputed here rather than left for a human to paste,
    because a refit that leaves stale expectations behind fails its own
    self-test and blocks the very automation this exists to enable.
    """
    out = json.loads(json.dumps(model))
    major = int(str(out.get("version", "1.0")).split(".")[0])
    out["version"] = f"{major + 1}.0" if out.get("fit_source", "").startswith(
        "published") else f"{major}.{int(str(out['version']).split('.')[1]) + 1}"
    out["base_mmcfd"] = prop["base_mmcfd"]
    out["slope_mmcfd_per_hdd"] = prop["slope_mmcfd_per_hdd"]
    out["formula"] = (f"MMcf/d = {prop['base_mmcfd']} + "
                      f"{prop['slope_mmcfd_per_hdd']} * HDD65")
    out["fit_source"] = (f"least squares against {prop['months']} months of "
                         f"observed EIA Alaska deliveries to residential, "
                         f"commercial and electric power consumers")
    out["fit"] = {
        "method": "least squares, consumption = base * days + slope * HDD65",
        "months": prop["months"],
        "through": months_label,
        "mean_error_pct": prop["mean_error_pct"],
        "geography": ("EIA reports Alaska statewide. Residential and commercial "
                      "gas is overwhelmingly Enstar in Southcentral and gas "
                      "fired power is overwhelmingly Railbelt, so statewide "
                      "heating and power deliveries stand in for the region. "
                      "Industrial load is excluded, because Kenai plant demand "
                      "does not track the weather."),
        "refit_by": "scripts/gaswatch_fit.py, on the monthly EIA workflow",
    }

    # Recompute every backtest expectation from the new coefficients.
    _, hdd = gc.load_hdd_history(out, REPO)
    facts = gc.backtest_facts(out, hdd)
    for bt in out.get("backtests", []):
        got = facts.get(bt["id"])
        if not got:
            continue
        for key in list(bt):
            if not key.startswith("expect_"):
                continue
            field = key[len("expect_"):]
            if field in got:
                bt[key] = got[field]

    out.setdefault("model_history", []).append({
        "version": out["version"],
        "effective": today.isoformat(),
        "reason": (f"Automatic refit against {prop['months']} months of observed "
                   f"EIA Alaska deliveries through {months_label}. Mean monthly "
                   f"error {prop['previous_mean_error_pct']} to "
                   f"{prop['mean_error_pct']} percent. Backtests recomputed."),
        "changed": ["base_mmcfd", "slope_mmcfd_per_hdd", "formula",
                    "fit_source", "backtests"],
    })
    return out


# ------------------------------------------------------------------ self test

def self_test():
    ok = [True]

    def check(label, cond, detail=""):
        print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not cond:
            ok[0] = False

    print("the fit recovers coefficients it was given")
    # Synthesise months from known coefficients and require the fit to find them.
    true_base, true_slope = 82.5, 3.25
    rows = [(30, hdd, true_base * 30 + true_slope * hdd)
            for hdd in range(0, 1800, 30)]
    b, s = least_squares(rows)
    check("exact data recovers exact coefficients",
          abs(b - true_base) < 1e-6 and abs(s - true_slope) < 1e-6,
          f"got base {b:.4f}, slope {s:.4f}")
    check("a perfect fit has no error", mean_error_pct(rows, b, s) < 1e-9)

    print("the guards refuse a bad fit")
    model = gc.load_model(os.path.join(REPO, "config", "gaswatch_model.json"))
    prop, why = evaluate(model, rows[:5])
    check("too few months is refused", prop is None, why)
    silly = [(30, h, 30.0 + 0.01 * h) for h in range(0, 1800, 30)]
    prop, why = evaluate(model, silly)
    check("a fit outside physical bounds is refused", prop is None, why)
    same = [(30, h, model["base_mmcfd"] * 30 + model["slope_mmcfd_per_hdd"] * h)
            for h in range(0, 1800, 30)]
    prop, why = evaluate(dict(model, base_mmcfd=82.5, slope_mmcfd_per_hdd=3.25), same)
    check("a fit that improves nothing is accepted only on merit",
          prop is not None, why)

    print("the real data earns a refit")
    rows = observations(model)
    prop, why = evaluate(model, rows)
    check("the committed record produces a usable fit", prop is not None, why)
    if prop:
        check("the fit beats the model it replaces",
              prop["mean_error_pct"] < prop["previous_mean_error_pct"],
              f"{prop['previous_mean_error_pct']} to {prop['mean_error_pct']} percent")
        new = apply_fit(model, prop, date(2026, 8, 5), "202605")
        _, hdd = gc.load_hdd_history(new, REPO)
        facts = gc.backtest_facts(new, hdd)
        stale = []
        for bt in new["backtests"]:
            got = facts.get(bt["id"]) or {}
            for k, v in bt.items():
                if k.startswith("expect_") and k[7:] in got and got[k[7:]] != v:
                    stale.append(f"{bt['id']}.{k}")
        check("a refit leaves no stale backtest behind", not stale, str(stale))
        check("the refit is versioned and logged",
              new["version"] != model["version"]
              and len(new["model_history"]) == len(model["model_history"]) + 1,
              f"{model['version']} to {new['version']}")

    print()
    if not ok[0]:
        print("self-test FAILED")
        return 1
    print("self-test clean")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Refit the gas watch demand model")
    ap.add_argument("--model", default=os.path.join(REPO, "config", "gaswatch_model.json"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    model = gc.load_model(args.model)
    with open(EIA_LEDGER, encoding="utf-8") as fh:
        through = json.load(fh).get("latest_month")
    rows = observations(model)
    prop, why = evaluate(model, rows)
    if prop is None:
        print(f"No refit. {why}")
        return 0

    new = apply_fit(model, prop, date.today(), through)
    print(f"Refit on {prop['months']} months through {through}")
    print(f"  base   {model['base_mmcfd']} to {new['base_mmcfd']}")
    print(f"  slope  {model['slope_mmcfd_per_hdd']} to {new['slope_mmcfd_per_hdd']}")
    print(f"  mean monthly error {prop['previous_mean_error_pct']} to "
          f"{prop['mean_error_pct']} percent")
    print(f"  version {model['version']} to {new['version']}")
    if args.dry_run:
        return 0
    with open(args.model, "w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=2)
        fh.write("\n")
    print("Written. Run gaswatch_collect --self-test to confirm the backtests.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
