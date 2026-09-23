#!/usr/bin/env python3
"""THE RUN IS NOT OVER UNTIL THE DECK SHIPS.

Run No.34 (2026-08-15) scored 7.51 against a threshold of 8.3, and the
showrunner responded by writing an excellent post-mortem, emailing it, and
stopping. Every artifact was honest. The ledger was accurate. The PR body
explained the shortfall in detail. And no carousel went out, on a day when
there was a complete deck, a verified story, green machine gates and a named,
finite list of defects sitting in the scorer's own report.

That is the failure this file exists to make impossible.

NO EMPTY RUNS is the routine's oldest law, and the degradation ladder spells
out what to do when the work is not good enough:

    (a) ship all 9 slides
    (b) reduced deck, floor of 6
    (c) fewer review rounds, disclosed
    (d) post-mortem with no deck

Step (d) is for when there is NOTHING TO SHIP: no story survived the claims
gate, the network was gone, the engine would not render. It is not for a deck
that needs another round. A below-threshold score is a work order, not a
verdict, and the run answers it by going back to Phase 8 and fixing the named
defects until the score clears. "The score is low" is a reason to keep
working, and it is never on its own a reason to stop.

So this gate refuses the one move that ended run No.34: reaching the ship step
with score.ship false and treating that as a finished run. It exits non-zero,
and it prints the scorer's own weakest criterion and fix line, because those
are the instructions for the next round.

  python scripts/ship_gate.py --run-dir out/<date>
      exit 0  the run may ship, merge and mail a post-ready draft
      exit 1  the run may NOT stop here; iterate and re-score
      exit 2  a genuine (d): asserted, justified and recorded

A real (d) has to be declared out loud and in writing, in the run directory,
by a human or by a run that can name a blocker no amount of iteration fixes:

    out/<date>/NO_DECK.md   first line: BLOCKER: <one sentence>

Writing that file to silence this gate, when a deck exists and the only
problem is that it is not good enough yet, is the specific dishonesty this
whole module is here to prevent. If a deck rendered, it is not a (d).
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _num(score, *keys, default=None):
    """Scorers spell these differently run to run; gmail_draft.py carries the
    same alias list and the same scar tissue behind it."""
    for k in keys:
        v = score.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return default


def _flag(score, *keys, default=None):
    for k in keys:
        v = score.get(k)
        if isinstance(v, bool):
            return v
    return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    run = Path(args.run_dir)

    out = {"run_dir": str(run), "may_ship": False, "reason": None}

    blocker = run / "NO_DECK.md"
    slides = sorted((run / "slides").glob("slide-*.html"))
    renders = sorted((run / "render").glob("slide-*.png"))

    if blocker.exists():
        first = blocker.read_text().strip().splitlines()[0] if blocker.read_text().strip() else ""
        if not first.startswith("BLOCKER:"):
            out["reason"] = ("NO_DECK.md exists but its first line does not start "
                             "with 'BLOCKER:'. A ladder step (d) is a claim, and a "
                             "claim has to be stated.")
            _emit(out, args.json)
            return 1
        # A (d) is only honest when there is genuinely nothing to ship. A deck
        # that rendered is a deck, whatever it scored.
        if len(renders) >= 6:
            out["reason"] = ("NO_DECK.md declares a post-mortem run, but %d slides "
                             "RENDERED in %s. That is a deck. Ladder step (d) is for "
                             "when there is nothing to ship, not for a deck that "
                             "needs another round. Delete NO_DECK.md and iterate."
                             % (len(renders), run / "render"))
            _emit(out, args.json)
            return 1
        out["may_ship"] = False
        out["reason"] = "declared blocker: " + first
        _emit(out, args.json)
        return 2

    sp = run / "score_report.json"
    if not sp.exists():
        out["reason"] = ("score_report.json missing. The run cannot ship or stop "
                         "until it has been scored.")
        _emit(out, args.json)
        return 1
    try:
        score = json.loads(sp.read_text())
    except ValueError as e:
        out["reason"] = "score_report.json does not parse (%s)" % type(e).__name__
        _emit(out, args.json)
        return 1

    total = _num(score, "weighted_total", "weighted_score",
                 "weighted_total_after_repairs", "weighted_score_as_scored")
    threshold = _num(score, "threshold", "ship_threshold", "threshold_applied",
                     "threshold_used", default=8.3)
    ship = _flag(score, "ship", "ships", "passes", "passes_as_scored")
    if ship is None and total is not None:
        ship = total >= threshold

    out.update({"weighted_total": total, "threshold": threshold, "ship": bool(ship),
                "slides": len(slides), "renders": len(renders)})

    if ship:
        out["may_ship"] = True
        out["reason"] = "scored %.2f against a threshold of %.2f" % (
            total if total is not None else -1, threshold)
        _emit(out, args.json)
        return 0

    weakest = score.get("weakest_criterion") or "(not named by the scorer)"
    fix = (score.get("one_sentence_fix") or score.get("fix_next_time")
           or "(the scorer named no fix; read its criterion notes)")
    lows = [c for c in score.get("criteria", [])
            if isinstance(c, dict) and isinstance(c.get("score"), (int, float))]
    lows.sort(key=lambda c: (c["score"], -float(c.get("weight") or 0)))
    out["weakest_criterion"] = weakest
    out["one_sentence_fix"] = fix
    out["work_order"] = [
        {"criterion": c.get("name"), "score": c.get("score"), "weight": c.get("weight")}
        for c in lows[:4]]
    out["reason"] = (
        "scored %s against a threshold of %s. This run does NOT stop here."
        % ("%.2f" % total if total is not None else "?", "%.2f" % threshold))
    _emit(out, args.json)
    return 1


def _emit(out, as_json):
    if as_json:
        print(json.dumps(out, indent=2))
        return
    if out["may_ship"]:
        print("SHIP GATE: PASS -- %s" % out["reason"])
        return
    print("SHIP GATE: STOP -- %s" % out["reason"])
    if out.get("weakest_criterion"):
        print()
        print("  A below-threshold score is a WORK ORDER, not a verdict. The deck")
        print("  exists and the defects are named. Go back to Phase 8, fix them,")
        print("  re-render, re-run the gates and re-score. Do not write a")
        print("  post-mortem, do not merge, and do not mail a DO NOT POST draft")
        print("  as though the run were finished. Ladder step (d) is for when")
        print("  there is nothing to ship, and a deck that rendered is a deck.")
        print()
        print("  weakest criterion : %s" % out["weakest_criterion"])
        print("  the scorer's fix  : %s" % out["one_sentence_fix"])
        if out.get("work_order"):
            print("  lowest scores, heaviest first:")
            for c in out["work_order"]:
                print("    %-42s %s/10 at weight %s"
                      % (c["criterion"], c["score"], c["weight"]))


if __name__ == "__main__":
    sys.exit(main())
