#!/usr/bin/env python3
"""trend_check.py, the repeat-offender report.

WHY THIS EXISTS (2026-07-29). Phase 12 closes on INCIDENTS and not on PATTERNS.
It walks the run that just happened, finds that run's deviations, and fixes
them. Nothing in the machine ever looked across runs, so a defect had to hurt
again before anyone looked at it again, and "again" was only noticed when an
agent happened to read the right sentence of prose in a prior ledger entry.

Measured on the corpus the day this was written:
  - Artwork craft was the weakest criterion in 16 of 19 scored runs, and was
    the target of exactly 2 upgrade entries in those 19 runs.
  - Runs 2026-07-25 and 2026-07-29 were both capped at 6.9 by the same CLASS
    of defect, text against SVG or canvas geometry that the DOM-only gate
    could not see. Four days apart. The gate that sees it was built on the
    second occurrence, reactively, after it had cost a second scoring cap.

This script does not judge and does not gate. It reports what keeps happening
and how long since anyone did something about it, so that Phase 1 can plan
against the standing weakness and Phase 12 has to either fix the top offender
or say in the dated email why it is deferring it again. A deferral that nobody
can see is how a defect survives sixteen runs.

Reads runs/<date>/score_report.json and runs/<date>/machine_qa.json, plus
ledger/upgrades.json to answer "when was this last actually worked on".
Everything is best effort: nineteen runs produced twenty seven spellings of
the top level keys, three shapes of hard_fails and two spellings of half the
criterion names, so every read goes through a normaliser and a file that
cannot be parsed is reported rather than skipped silently.

Exit status is 0 unless --require is passed, which exits 1 when an offender
has gone unaddressed for longer than --stale runs. Advisory by default,
because a new check that blocks a ship on its first day is a check that gets
disabled.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------- normalising

def canon(name):
    """Fold the spellings of one criterion into a single key.

    Nineteen runs produced 'Artwork craft & genuine detail', 'Artwork craft and
    genuine detail', and 'Artwork craft and genuine detail (6 of 10)'. Without
    this they count as three different criteria and the trend disappears.
    """
    s = str(name).lower()
    s = s.split("(")[0]          # drop a trailing score or gloss
    s = s.split(":")[0]          # drop a trailing reason
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split()).strip()


PRETTY = {}          # canon key -> the longest spelling actually seen


def remember(name):
    k = canon(name)
    if k and len(str(name)) > len(PRETTY.get(k, "")):
        PRETTY[k] = str(name).split("(")[0].split(":")[0].strip()
    return k


NONE_ISH = re.compile(r"^\s*(none|no hard fail|n/?a|zero)\b", re.I)


def iter_hard_fails(s):
    """Yield hard-fail texts across every container shape the corpus uses.

    Nineteen runs produced four: a list of strings, a list of {rule,status}
    rows where only a FAILing row counts, the bare string
    'none (all 13 rules pass...)', and {'any': false, 'checked': [...]}.
    Iterating the string form character by character invented four hard fails
    named n, o, n and e on run 2026-07-10, which is exactly the kind of
    fabricated trend this script exists to avoid.
    """
    for key in ("hard_fails", "hard_fails_as_scored"):
        v = s.get(key)
        if v is None:
            continue
        if isinstance(v, str):
            if not NONE_ISH.match(v):
                yield v
            continue
        if isinstance(v, dict):
            if v.get("any") is False or v.get("present") is False:
                continue
            for sub in ("failures", "fails", "failed", "hard_fails"):
                for item in (v.get(sub) or []):
                    if str(item).strip():
                        yield str(item)
            continue
        for h in (v or []):
            if isinstance(h, dict):
                if str(h.get("status", "")).strip().upper().startswith("FAIL"):
                    yield str(h.get("rule") or h.get("evidence") or "")
            elif str(h).strip() and not NONE_ISH.match(str(h)):
                yield str(h)


def match_weakest(raw, score_keys):
    """Resolve a free-text weakest-criterion line to one of the run's criteria.

    The scorers gloss it: 'Artwork craft and genuine detail (6 of 10, weight
    0.16)' and 'Artwork craft and genuine detail, at 6, with Legibility at 5
    driven by a defect since repaired.' Canonicalising the raw string alone
    invents a new criterion per gloss, so match against what the run's own
    report card actually contains and keep the longest match.
    """
    c = canon(raw)
    if not c:
        return None
    if c in score_keys:
        return c
    hits = [k for k in score_keys if c.startswith(k) or k in c]
    if hits:
        return max(hits, key=len)
    toks = set(c.split())
    best, score = None, 0
    for k in score_keys:
        overlap = len(toks & set(k.split()))
        if overlap > score:
            best, score = k, overlap
    return best if score >= 2 else (c or None)


def first(d, *keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return None


def as_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- run records

def load_runs(runs_dir):
    """One record per run directory, with everything already normalised."""
    out, broken = [], []
    for d in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        sp = d / "score_report.json"
        if not sp.exists():
            continue
        try:
            s = json.loads(sp.read_text())
        except Exception as e:
            broken.append((d.name, f"score_report.json {e}"))
            continue

        rec = {"date": d.name, "scores": {}, "weakest": None, "hard_fails": [],
               "total": None, "threshold": None, "qa": None}

        rec["total"] = as_float(first(s, "weighted_total", "weighted_score",
                                      "weighted_score_as_scored", "raw_weighted_score"))
        rec["threshold"] = as_float(first(s, "threshold", "ship_threshold",
                                          "threshold_applied"))

        for c in (s.get("criteria") or []):
            if not isinstance(c, dict):
                continue
            nm = c.get("name")
            sc = as_float(first(c, "score", "score_0_10"))
            if nm and sc is not None:
                rec["scores"][remember(nm)] = sc

        w = first(s, "weakest_criterion")
        if not w:
            wc = s.get("weakest_criteria")
            if isinstance(wc, list) and wc:
                w = wc[0]
        if w:
            remember(w)
            rec["weakest"] = match_weakest(w, set(rec["scores"]))
        elif rec["scores"]:
            # Derive it rather than lose the run: three reports state no
            # weakest criterion at all but carry a full report card.
            lo = min(rec["scores"].values())
            rec["weakest"] = sorted(k for k, v in rec["scores"].items() if v == lo)[0]

        rec["hard_fails"] = [t for t in iter_hard_fails(s) if t.strip()]

        # A capped run whose report never listed its hard fails is still a
        # capped run: 2026-07-25 carries only cap_reason, and dropping it would
        # have hidden half of the recurring pair this script was built to find.
        cap = first(s, "cap_reason", "cap_reason_as_scored")
        if cap:
            rec["cap_reason"] = str(cap)
            if not rec["hard_fails"] and not NONE_ISH.match(str(cap)):
                rec["hard_fails"].append(str(cap))
                rec["cap_only"] = True

        qp = d / "machine_qa.json"
        if qp.exists():
            try:
                q = json.loads(qp.read_text())
                rec["qa"] = q
            except Exception as e:
                broken.append((d.name, f"machine_qa.json {e}"))

        out.append(rec)
    return out, broken


# ------------------------------------------------------------------- upgrades

def upgrade_touches(ledger_path):
    """canon-ish token -> sorted run_dates of upgrades that mention it.

    Matching is on the upgrade's own free text (change + trigger + area),
    because the ledger has no structured link to a rubric criterion. It is a
    heuristic and it is reported as one: the column is called 'last worked'
    and not 'fixed'.
    """
    touches = defaultdict(set)
    try:
        u = json.loads(ledger_path.read_text())
    except Exception:
        return touches
    for e in (u.get("entries") or []):
        date = e.get("run_date")
        blob = " ".join(str(e.get(k, "")) for k in ("change", "trigger", "area", "kind"))
        blob = canon(blob)
        for tok in set(blob.split()):
            if len(tok) > 3:
                touches[tok].add(date)
    return touches


def last_worked(crit_key, touches, upto):
    """Most recent run_date whose upgrade text mentions this criterion's words."""
    words = [w for w in crit_key.split() if len(w) > 3 and w not in ("genuine", "platform")]
    if not words:
        return None
    dates = set()
    for w in words:
        dates |= touches.get(w, set())
    dates = sorted(d for d in dates if d and d <= upto)
    return dates[-1] if dates else None


# ------------------------------------------------------------------ defects

QA_CLASS = re.compile(r"^\s*([a-z][a-z ,/-]{2,44}?)\s*(?:[:(]|$)", re.I)


def qa_classes(rec):
    """Coarse class label for each shipped warn and fail on a run."""
    out = []
    q = rec.get("qa") or {}
    for s in (q.get("slides") or []):
        for level in ("fails", "warns"):
            for msg in (s.get(level) or []):
                m = QA_CLASS.match(str(msg))
                label = (m.group(1) if m else str(msg)[:40]).strip().lower()
                out.append((level, label))
    return out


HARD_FAIL_CLASSES = (
    ("text against geometry", ("overran", "off its plate", "off its knockout", "sat entirely off",
                               "painted over", "collision", "overlap", "clipped", "occluded",
                               "covered", "crossed by", "escaped", "hangs off", "hanging off")),
    ("contrast", ("contrast", "unreadable", "washes out", "illegible")),
    ("safe zone / crop", ("safe zone", "cut off", "offscreen", "margin")),
    ("sourcing", ("claim", "unsourced", "source", "citation")),
    ("house rule", ("em dash", "en dash", "emoji", "colon", "hashtag")),
)


def classify_hard_fail(text):
    t = str(text).lower()
    for label, needles in HARD_FAIL_CLASSES:
        if any(n in t for n in needles):
            return label
    return "other"


# -------------------------------------------------------------------- report

def build(runs, window, touches):
    recent = runs[-window:] if window else runs
    n = len(recent)
    latest = recent[-1]["date"] if recent else ""

    weakest_count = defaultdict(int)
    appear = defaultdict(int)
    totals = defaultdict(list)
    for r in recent:
        if r["weakest"]:
            weakest_count[r["weakest"]] += 1
        for k, v in r["scores"].items():
            appear[k] += 1
            totals[k].append(v)

    criteria = []
    for k in sorted(set(list(weakest_count) + list(appear))):
        vals = totals.get(k, [])
        lw = last_worked(k, touches, latest)
        since = None
        if lw:
            after = [r["date"] for r in runs if r["date"] > lw]
            since = len(after)
        criteria.append({
            "criterion": PRETTY.get(k, k),
            "key": k,
            "weakest_in": weakest_count.get(k, 0),
            "of_runs": n,
            "mean": round(sum(vals) / len(vals), 2) if vals else None,
            "last": vals[-1] if vals else None,
            "last_upgrade": lw,
            "runs_since_upgrade": since,
        })
    criteria.sort(key=lambda c: (-c["weakest_in"], c["mean"] if c["mean"] is not None else 99))

    capped = [r for r in recent if r["hard_fails"]]
    hf = defaultdict(list)
    for r in capped:
        for t in r["hard_fails"]:
            hf[classify_hard_fail(t)].append(r["date"])

    shipped = defaultdict(set)
    for r in recent:
        for level, label in qa_classes(r):
            shipped[(level, label)].add(r["date"])

    return {
        "window": n,
        "runs": [r["date"] for r in recent],
        "criteria": criteria,
        "hard_fail_classes": {k: sorted(set(v)) for k, v in
                              sorted(hf.items(), key=lambda kv: -len(set(kv[1])))},
        "capped_runs": [r["date"] for r in capped],
        "shipped_qa_classes": {f"{lvl}:{lab}": sorted(d) for (lvl, lab), d in
                               sorted(shipped.items(), key=lambda kv: -len(kv[1]))},
        "totals": [{"date": r["date"], "total": r["total"], "threshold": r["threshold"]}
                   for r in recent],
    }


def render(rep, top, stale):
    L = []
    L.append(f"TREND -- generated by scripts/trend_check.py over the last "
             f"{rep['window']} scored run(s), {rep['runs'][0]} to {rep['runs'][-1]}.")
    L.append("")
    L.append("REPEAT OFFENDERS (criterion, times it was the weakest, mean, last worked on)")
    L.append("  'worked' is a text match over ledger/upgrades.json prose, so it can UNDER-report:")
    L.append("  an upgrade that fixed a criterion without naming it reads as 'never'. Check before acting.")
    for c in rep["criteria"][:top]:
        if not c["weakest_in"]:
            continue
        lw = c["last_upgrade"] or "never"
        since = ("never" if c["runs_since_upgrade"] is None
                 else f"{c['runs_since_upgrade']} run(s) ago")
        flag = ""
        if c["runs_since_upgrade"] is None or c["runs_since_upgrade"] >= stale:
            flag = "  <-- STALE"
        L.append(f"  weakest {c['weakest_in']:>2}/{c['of_runs']:<2}  "
                 f"mean {c['mean'] if c['mean'] is not None else '-':<5}  "
                 f"last {c['last'] if c['last'] is not None else '-':<5}  "
                 f"{c['criterion'][:38]:38}  worked {lw} ({since}){flag}")
    if not any(c["weakest_in"] for c in rep["criteria"]):
        L.append("  none, no run in this window named a weakest criterion")

    L.append("")
    caps = rep["capped_runs"]
    L.append(f"HARD FAILS ({len(caps)} of {rep['window']} run(s) carried one)")
    if rep["hard_fail_classes"]:
        for k, dates in rep["hard_fail_classes"].items():
            rep_flag = "  <-- RECURRING" if len(dates) > 1 else ""
            L.append(f"  {len(dates):>2}x  {k:26}  {', '.join(dates)}{rep_flag}")
    else:
        L.append("  none in this window")

    L.append("")
    L.append("DEFECT CLASSES THAT KEEP SHIPPING (present in the final machine_qa)")
    shown = 0
    for k, dates in rep["shipped_qa_classes"].items():
        if len(dates) < 2:
            continue
        L.append(f"  {len(dates):>2} run(s)  {k[:52]:52}  latest {dates[-1]}")
        shown += 1
        if shown >= top:
            break
    if not shown:
        L.append("  none recurring in this window")

    L.append("")
    ts = [t for t in rep["totals"] if t["total"] is not None]
    if ts:
        line = "  " + "  ".join(f"{t['date'][5:]} {t['total']:.2f}" for t in ts[-8:])
        L.append("SCORE, most recent runs")
        L.append(line)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="repeat-offender report across shipped runs")
    ap.add_argument("--runs-dir", default=str(REPO / "runs"))
    ap.add_argument("--upgrades", default=str(REPO / "ledger" / "upgrades.json"))
    ap.add_argument("--window", type=int, default=10,
                    help="how many recent scored runs to consider (0 = all)")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--stale", type=int, default=3,
                    help="runs since an offender was last worked on before it is STALE")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--require", action="store_true",
                    help="exit 1 if a repeat offender is STALE (advisory by default)")
    args = ap.parse_args()

    runs_dir = Path(args.runs_dir)
    if not runs_dir.is_dir():
        print(f"trend_check: no runs dir at {runs_dir}", file=sys.stderr)
        return 2

    runs, broken = load_runs(runs_dir)
    if not runs:
        # Report the unreadable files BEFORE returning. Reporting them only on
        # the success path meant a directory of nothing but corrupt reports
        # printed "nothing to trend yet" and exited 0, which is a check that
        # cannot see calling itself clean.
        print("trend_check: no scored runs found (nothing to trend yet)")
        for r, p in broken:
            print(f"  [unreadable] {r}: {p}")
        return 2 if broken else 0

    touches = upgrade_touches(Path(args.upgrades))
    rep = build(runs, args.window, touches)
    rep["unreadable"] = [{"run": r, "problem": p} for r, p in broken]

    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print(render(rep, args.top, args.stale))
        for r, p in broken:
            print(f"  [unreadable] {r}: {p}")

    if args.require:
        # A "never worked on" row does NOT gate. The last-worked column is a
        # text match over upgrade prose and is known to under-report, so an
        # upgrade that fixed a criterion without naming it reads as "never".
        # Failing a ship on that is the same cry-wolf mistake as a font guard
        # that cannot tell correct usage from incorrect usage: it teaches
        # people to pass --no-verify. Only a MEASURED gap gates.
        stale = [c for c in rep["criteria"]
                 if c["weakest_in"] >= 2
                 and c["runs_since_upgrade"] is not None
                 and c["runs_since_upgrade"] >= args.stale]
        if stale:
            names = ", ".join(c["criterion"] for c in stale[:3])
            print(f"\ntrend_check: FAIL, {len(stale)} repeat offender(s) not worked on "
                  f"in {args.stale}+ runs: {names}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
