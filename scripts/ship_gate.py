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
import html
import json
import re
import sys
from pathlib import Path

# One reader for the scorer's weakest-criterion value, shared with
# trend_check.py and gmail_draft.py. runs/2026-09-14 wrote it as an object
# where the schema declares a string, and three separate readers each took the
# container as a name (2026-09-23).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from trend_check import (weakest_criterion_fix,  # noqa: E402
                         weakest_criterion_name)

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


# THE CRAFT FLOOR (2026-09-25, owner: make artwork craft the strongest area).
#
# Artwork craft averaged 6.7 over the first 68 scored runs and never passed 8.
# Two facts explain it, both measured. craft_corpus.py found no pixel feature
# that separates the slides scorers named (best AUC 0.62), so no image gate can
# catch it. And 43 of 63 runs shipped with art at 7 or under because the TOTAL
# cleared the threshold: the only repair loop this gate ran was for a failing
# total, so once the other criteria carried the deck nothing ever asked the art
# for more. The scorer's art complaints were read, filed in FIELD_NOTES, and
# shipped past, run after run.
#
# So a passing total no longer ends it while the art is under CRAFT_FLOOR and
# rounds remain under the five-round cap. The run owes ONE targeted craft cycle:
# repair the frames the scorer named in artwork_weakest_frames, re-render,
# re-run the gates, re-score, and record it in score_report.json as
#   "craft_cycle": {"frames": [8, 3], "art_before": 7.0, "art_after": 7.5}
# after which the floor is closed whatever art_after says. It is one cycle and
# never more, it never blocks a ship after that cycle (NO EMPTY RUNS), and it
# stands down at the round cap, where the cap's own rule is to ship as-is.
CRAFT_FLOOR = 8.5
CRAFT_FLOOR_FROM = "2026-09-26"   # runs before the rule are not re-judged by it
ROUND_CAP = 5


def _art_score(score):
    crit = score.get("criteria")
    if not isinstance(crit, list):
        return None      # malformed; craft_floor fails closed on None
    for c in crit:
        # The rubric's own criterion, "Artwork craft & genuine detail", matched
        # in full after normalizing case and "&"/"and"; not any name that merely
        # contains or starts like it (Codex on PR #401).
        # runs/2026-07-31 wrote it HTML-escaped ("&amp;"), so unescape first.
        name = " ".join(w for w in re.findall(
            r"[a-z]+", html.unescape(str(c.get("name", ""))).lower())
            if w != "and") if isinstance(c, dict) else ""
        if name == "artwork craft genuine detail":
            v = c.get("score")
            # A range check, not math.isfinite, which raises OverflowError on
            # a huge JSON integer (Codex on PR #401); NaN and Infinity fail it.
            if (isinstance(v, (int, float)) and not isinstance(v, bool)
                    and 0 <= v <= 10):
                return float(v)
    return None


# Past runs recorded the editing-round count under several names (a survey of
# runs/ on 2026-09-25 found these, Codex on PR #401). The routine asks for
# revision_rounds; the others are read so a run that wrote an older shape is
# not ordered past the cap. Codex review rounds (merge.review_rounds,
# codex_review.rounds) are a different count and are deliberately not read.
_ROUND_KEYS = ("revision_rounds", "rounds_used", "editing_rounds", "review_rounds",
               "rounds_of_revision", "rounds", "round", "revision_round")
_ROUND_NESTED = (("rounds", "revision_rounds_completed"), ("final", "revision_rounds"),
                 ("result", "rounds"), ("outcome", "rounds"))


def _as_count(v):
    """A round count, or None. JSON admits Infinity and NaN, and int() of either
    raises, which would crash the gate before it reports (Codex on PR #401)."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v if 0 <= v <= 99 else None
    if isinstance(v, float):
        if not (0 <= v <= 99) or v != int(v):    # also rejects NaN and Infinity
            return None
        return int(v)
    if isinstance(v, str) and re.fullmatch(r"\s*\d{1,2}\s*", v):
        return int(v)
    return None


def _round_counts(d):
    if not isinstance(d, dict):
        return []
    vals = [_as_count(d.get(k)) for k in _ROUND_KEYS]
    vals += [_as_count(d[a].get(b)) for a, b in _ROUND_NESTED if isinstance(d.get(a), dict)]
    return [v for v in vals if v is not None]


def _rounds_used(run, score):
    vals = _round_counts(score)
    try:
        vals += _round_counts(json.loads((run / "run_state.json").read_text()))
    except (OSError, ValueError):
        pass
    return max(vals) if vals else 0


def craft_floor(run, score):
    """{'status': 'n/a'|'met'|'closed'|'capped'|'open', 'reason': str}."""
    date = run.name
    if len(date) == 10 and date[4] == "-" and date < CRAFT_FLOOR_FROM:
        return {"status": "n/a", "reason": "run predates the craft floor"}
    art = _art_score(score)
    if art is None:
        # Fail closed (Codex on PR #401): a report that drops, renames or
        # mis-types the artwork criterion would otherwise walk past the floor.
        return {"status": "open", "reason": (
            "the score report carries no numeric 'Artwork craft & genuine detail' "
            "criterion, so the craft floor can't be judged. Re-score against "
            "config/scoring_rubric.yaml with every criterion present.")}
    if art >= CRAFT_FLOOR:
        return {"status": "met", "reason": "artwork craft %.1f" % art}
    cyc = score.get("craft_cycle")
    bad = _craft_cycle_problem(cyc, _deck_slides(run), art) if cyc is not None else None
    if cyc is not None and bad is None:
        return {"status": "closed", "reason": "one craft cycle ran on frames %s (art %s -> %s)"
                % (cyc["frames"], cyc["art_before"], cyc["art_after"])}
    rounds = _rounds_used(run, score)
    if rounds >= ROUND_CAP:
        return {"status": "capped", "reason": "artwork craft %.1f, but the run is at the %d-round cap"
                % (art, ROUND_CAP)}
    wf = score.get("artwork_weakest_frames")
    frames = [f.get("slide") for f in wf if isinstance(f, dict)] if isinstance(wf, list) else []
    return {"status": "open", "reason": (
        "the total passes but artwork craft is %.1f, under the %.1f craft floor, with %d of %d "
        "rounds used. Run ONE craft cycle on the frames the scorer named (%s), re-render, re-gate, "
        "re-score, and record score_report.craft_cycle {frames, art_before, art_after}.%s"
        % (art, CRAFT_FLOOR, rounds, ROUND_CAP, frames or "see its artwork notes",
           (" The craft_cycle on file does not count: %s." % bad) if bad else ""))}


def _deck_slides(run):
    """The slide numbers this run actually built: slides/slide-NN.html in the
    working dir, or the flat slide-NN.webp/png files Phase 11 archives under
    runs/<date>/ (it does not copy slides/, Codex on PR #401)."""
    out = set()
    for d in (run / "slides", run / "final", run):
        if not d.is_dir():
            continue
        for p in d.iterdir():
            m = re.fullmatch(r"slide-(\d{2})\.(?:html|webp|png)", p.name)
            if m:
                out.add(int(m.group(1)))
    return out


def _craft_cycle_problem(cyc, slides, art):
    """Why a craft_cycle record can't close the floor, or None. The record is
    the only evidence the repair AND the re-score happened (Codex on PR #401),
    so it has to agree with the run it sits in:
    - every frame it names is a slide this deck built, so "frames": [20] on a
      nine-slide deck repairs nothing and closes nothing;
    - both scores are present and numeric, since a record without art_after is
      a repair that was never re-scored;
    - the report it sits in carries the better of the two, because the routine
      keeps the higher-scoring version, so a record whose scores the report
      doesn't show was not written from the re-score.
    It is NOT checked against the report's artwork_weakest_frames: by the time
    the gate reads it that list is the RE-score's, and a repair that worked has
    taken its frame off it."""
    if not isinstance(cyc, dict):
        return "it is not an object"
    fr = cyc.get("frames")
    if (not isinstance(fr, list) or not fr
            or not all(isinstance(n, int) and not isinstance(n, bool) for n in fr)):
        return "frames must be a nonempty list of slide numbers"
    if not slides:
        return "the run has no slides/slide-NN.html to check its frames against"
    missing = sorted(set(fr) - slides)
    if missing:
        return "frames %s are not slides in this deck (it has %d)" % (missing, len(slides))
    for k in ("art_before", "art_after"):
        v = cyc.get(k)
        if not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 10:
            return "%s must be the artwork-craft score, a number from 0 to 10" % k
    best = max(cyc["art_before"], cyc["art_after"])
    if abs(best - art) > 0.05:
        return ("the report scores artwork craft %.1f, but the better of art_before and "
                "art_after is %.1f; record the cycle from the re-score in this report" % (art, best))
    return None


def self_test():
    import tempfile
    ok = True
    def rep(art, **kw):
        d = {"criteria": [{"name": "Artwork craft & genuine detail", "score": art, "weight": 0.16}]}
        d.update(kw)
        return d
    cases = [
        ("2026-09-25", rep(7.0), {}, "n/a"),
        ("2026-09-26", rep(9.0), {}, "met"),
        ("2026-09-26", rep(7.5, artwork_weakest_frames=[{"slide": 4}]), {"revision_rounds": 3}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [4], "art_before": 7.5, "art_after": 7.5}), {}, "closed"),
        ("2026-09-26", rep(8.0, craft_cycle={"frames": [4, 8], "art_before": 7.0, "art_after": 8.0}), {}, "closed"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [20], "art_before": 7.5, "art_after": 7.5}), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [4], "art_before": 7.0, "art_after": 7.0}), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [4], "art_before": 7.5, "art_after": 7.5},
                           _no_slides=True), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"skipped": "no time"}), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [4], "art_before": 7}), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [], "art_before": 7, "art_after": 8}), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": ["04"], "art_before": 7, "art_after": 8}), {}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [4], "art_before": 7, "art_after": "8"}), {}, "open"),
        ("2026-09-26", rep(7.5), {"revision_rounds": 5}, "capped"),
        ("2026-09-26", {"criteria": []}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft", "score": "7"}]}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft", "score": True}]},
         {"revision_rounds": 5}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft", "score": float("inf")}]}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft", "score": 11}]}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork accessibility", "score": 9}]}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Non-artwork criterion", "score": 9}]}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "ARTWORK CRAFT & GENUINE DETAIL", "score": 9}]}, {}, "met"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft and genuine detail", "score": 9}]}, {}, "met"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft &amp; genuine detail", "score": 9}]}, {}, "met"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craftsmanship", "score": 9}]}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft", "score": 9}]}, {}, "open"),
        ("2026-09-26", {"criteria": 4}, {}, "open"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft & genuine detail", "score": 10 ** 400}]},
         {}, "open"),
        ("2026-09-26", rep(7.5, revision_rounds=10 ** 400), {"revision_rounds": 5}, "capped"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft accessibility", "score": 9}]}, {}, "open"),
        ("2026-09-26", rep(7.5, artwork_weakest_frames=4), {}, "open"),
        ("2026-09-26", rep(7.5, round=5), {}, "capped"),
        ("2026-09-26", rep(7.5, revision_rounds=float("inf")), {"revision_rounds": float("nan")}, "open"),
        ("2026-09-26", rep(7.5, revision_rounds=float("inf")), {"revision_rounds": 5}, "capped"),
        ("2026-09-26", rep(7.5, revision_round=5), {}, "capped"),
        ("2026-09-26", {"criteria": [{"name": "Artwork craft", "score": float("nan")}]},
         {"revision_rounds": 5}, "open"),
        ("2026-09-26", rep(7.5, craft_cycle={"frames": [4], "art_before": 7.5, "art_after": 7.5},
                           _no_slides=True, _flat=True), {}, "closed"),
        ("2026-09-25", {"criteria": []}, {}, "n/a"),
        ("2026-09-26", rep(7.5), {"rounds_used": 5}, "capped"),
        ("2026-09-26", rep(7.5, rounds={"revision_rounds_completed": 5}), {}, "capped"),
        ("2026-09-26", rep(7.5, revision_rounds="5"), {}, "capped"),
        ("2026-09-26", rep(7.5), {"merge": {"review_rounds": 5}}, "open"),
    ]
    with tempfile.TemporaryDirectory() as t:
        for date, sc, rs, want in cases:
            d = Path(t) / ("case%02d" % len(list(Path(t).iterdir()))) / date
            (d / "slides").mkdir(parents=True)
            flat = sc.pop("_flat", False)
            if flat:                     # the runs/<date>/ archive layout
                for n in range(1, 10):
                    (d / ("slide-%02d.webp" % n)).write_text("")
                (d / "slide-01-thumb.webp").write_text("")
            if not sc.pop("_no_slides", False):
                for n in range(1, 10):   # a nine-slide deck
                    (d / "slides" / ("slide-%02d.html" % n)).write_text("")
            (d / "run_state.json").write_text(json.dumps(rs))
            got = craft_floor(d, sc)["status"]
            flag = "ok  " if got == want else "FAIL"
            ok &= got == want
            print("  %s %s art=%s rounds=%s -> %s (want %s)" % (
                flag, date, _art_score(sc), rs.get("revision_rounds"), got, want))
    print("ship_gate self-test: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    if "--self-test" in sys.argv:
        return self_test()
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
        floor = craft_floor(run, score)
        out["craft_floor"] = floor
        if floor["status"] == "open":
            out["reason"] = floor["reason"]
            _emit(out, args.json)
            return 1
        out["may_ship"] = True
        out["reason"] = "scored %.2f against a threshold of %.2f" % (
            total if total is not None else -1, threshold)
        if floor["status"] != "n/a":
            out["reason"] += "; craft floor " + floor["status"] + ", " + floor["reason"]
        _emit(out, args.json)
        return 0

    raw_weakest = (score.get("weakest_criterion")
                   or score.get("weakest_criteria"))
    weakest, _ = weakest_criterion_name(raw_weakest)
    weakest = weakest or "(not named by the scorer)"
    # A top-level fix wins; otherwise take the one carried INSIDE an
    # object-shaped weakest_criterion, which those reports have instead of a
    # top-level one. Reading only the name printed "no fix" about a report
    # that stated the fix plainly, and the fix is the whole point of the field.
    fix = (score.get("one_sentence_fix") or score.get("fix_next_time")
           or weakest_criterion_fix(raw_weakest)
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
    if (out.get("craft_floor") or {}).get("status") == "open":
        print()
        print("  THE CRAFT FLOOR. The deck passes; its art does not yet. This is one")
        print("  targeted cycle on the scorer's named frames, never more, and it never")
        print("  blocks a ship once recorded.")
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
