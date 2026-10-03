#!/usr/bin/env python3
"""week_digest.py, what the scorer and the flow critic kept saying this week, counted.

WHY THIS EXISTS (owner, 2026-10-02)

The weekly machine pass is meant to fix "the things that really need to be fixed based on the
recurring themes that it saw during the week ... based on actual output". `trend_check.py` already
counts which CRITERION keeps being weakest and which machine-QA defect classes keep shipping. What
nothing counted is WHY the art keeps scoring where it does, which the scorer and the flow critic
write down on every run. This reads every shipped run in the window and puts in front of the
upgrade engineer:

  THE TREND      trend_check.py's own report over the same window, verbatim.
  THE CAUSES     the flow critic's `craft.weakest_frames`, counted by its own cause letter (a the
                 same drawing on too many frames, b the largest object least modelled, c a dead
                 region, d a texture artifact, e no tonal arc). These are labels the critic chose,
                 so this count is exact. Its `craft.cross_frame` list (one defect over several
                 frames, where causes a and e live) is counted in its own table (2026-10-04).
  THE THEMES     a word match over the scorer's artwork notes, `artwork_weakest_frames` and one
                 sentence fix, counted by runs. It finds candidates and says so. The engineer reads
                 the evidence before believing a count.
  THE EVIDENCE   each run's craft cycle (art before and after), the scorer's weakest frames and
                 fix verbatim, and the open queue.

    python3 scripts/week_digest.py --date 2026-10-09 [--days 7] [--out out/2026-10-09/week_digest.md]
    python3 scripts/week_digest.py --self-test
"""
import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUNS = REPO / "runs"
QUEUE = REPO / "knowledge" / "MACHINE_QUEUE.md"
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

CAUSES = {
    "a": "the same drawing or texture on more than three frames",
    "b": "the largest object least modelled, or a flat fallback",
    "c": "a dead or eventless region, above all the lower third",
    "d": "a texture artifact (fur, stripes, moire, a reserve edge, banding)",
    "e": "no tonal or density arc across the deck",
}

THEMES = [
    ("the depth frame does not deliver depth (2.5D, flat chart)",
     r"2\.5d|depth frame|flat (?:2d )?(?:step )?chart|zero yaw|no riser"),
    ("no contact shadow, or an object that floats",
     r"contact shadow|no (?:visible |legible )?shadow|\bfloat(?:s|ing)?\b"),
    ("a dead, flat or empty region, the lower third above all",
     r"lower third|dead (?:zone|region|band|space)|eventless|empty (?:band|region|third)"),
    ("a flat gradient or fill where a material belongs",
     r"gradient band|plain (?:grey|gray)|flat (?:fill|grey|gray)|untextured|featureless"),
    ("a texture artifact (moire, banding, stripes, fur, a reserve edge)",
     r"moir|banding|stripes?\b|\bfur\b|reserve edge|artifact|aliasing"),
    ("the same drawing, texture or mottle on many frames",
     r"same (?:drawing|texture|mottle|treatment)|repeated (?:texture|drawing)|fbm mottle|four of nine"),
    ("the tonal arc or the exposure peak",
     r"tonal arc|exposure|contact sheet"),
    ("type crowding or colliding with the art",
     r"touch(?:es|ing) (?:the )?glyph|crowd|collid|busy art|under (?:the )?text"),
]
THEME_RX = [(n, re.compile(p, re.I)) for n, p in THEMES]


def _load(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def run_dirs(root, date, days):
    end = dt.date.fromisoformat(date)
    start = end - dt.timedelta(days=days - 1)
    return [p for p in sorted(root.glob("*")) if p.is_dir() and DATE_RE.fullmatch(p.name)
            and start <= dt.date.fromisoformat(p.name) <= end]


def art_text(score):
    parts = []
    for c in score.get("criteria") or []:
        if isinstance(c, dict) and "artwork" in html.unescape(str(c.get("name", ""))).lower():
            parts.append(str(c.get("notes") or c.get("why") or ""))
    for w in score.get("artwork_weakest_frames") or []:
        if isinstance(w, dict):
            parts.append(f"{w.get('problem', '')} {w.get('fix', '')}")
    parts.append(str(score.get("one_sentence_fix") or ""))
    return " ".join(parts)


def digest(root, date, days, queue_text, trend_text):
    runs = run_dirs(root, date, days)
    causes = {k: {} for k in CAUSES}
    # THE DECK-LEVEL CAUSES WERE NOT COUNTED (2026-10-04, the first weekly pass).
    # The flow critic files a cause in TWO places: `weakest_frames` (one frame
    # each) and `cross_frame` (one defect spanning several frames). Only the
    # first was read, so the week of 2026-09-28 to 10-03 showed cause e (no
    # tonal arc) at 0 runs while `cross_frame` named it on all six, and cause a
    # (the same drawing on many frames) at 1 run while `cross_frame` named it on
    # five. Those two causes are deck-level by definition; this table is where
    # they live.
    cross = {k: {} for k in CAUSES}
    themes = {n: [] for n, _ in THEMES}
    evidence = []
    for run in runs:
        score = _load(run / "score_report.json") or {}
        flow = _load(run / "flow_review.json") or {}
        for w in ((flow.get("craft") or {}).get("weakest_frames") or []):
            if isinstance(w, dict) and str(w.get("cause", "")).strip().lower() in causes:
                causes[str(w["cause"]).strip().lower()].setdefault(run.name, []).append(w.get("slide"))
        for w in ((flow.get("craft") or {}).get("cross_frame") or []):
            k = str(w.get("cause", "")).strip().lower() if isinstance(w, dict) else ""
            if k in cross:
                sl = w.get("slides") if isinstance(w.get("slides"), list) else []
                cross[k].setdefault(run.name, []).append(
                    (sl, str(w.get("problem") or w.get("fix") or "")))
        text = art_text(score)
        for name, rx in THEME_RX:
            if rx.search(text):
                themes[name].append(run.name)
        evidence.append((run.name, score))
    n = len(runs)
    L = [f"# The week's machine digest, {n} shipped run(s) to {date}", "",
         "Computed by `scripts/week_digest.py` from `runs/`. Every number here is counted, never typed.", "",
         "## The trend (trend_check.py, same window)", "", "```", trend_text.rstrip(), "```", "",
         "## The flow critic's causes, by its own label", "",
         f"| cause | runs (of {n}) | frames | runs and frames |", "|---|---|---|---|"]
    for k in sorted(causes, key=lambda k: (-len(causes[k]), k)):
        hits = causes[k]
        frames = sum(len(v) for v in hits.values())
        detail = "; ".join(f"{d} {','.join(str(s) for s in v)}" for d, v in sorted(hits.items()))
        L.append(f"| {k}, {CAUSES[k]} | {len(hits)} | {frames} | {detail} |")
    L += ["", "## The flow critic's cross-frame causes, deck level", "",
          "Its `craft.cross_frame` list: one defect spanning several frames. Causes a and e live here.", "",
          f"| cause | runs (of {n}) | frames named | runs, slides and problem |", "|---|---|---|---|"]
    for k in sorted(cross, key=lambda k: (-len(cross[k]), k)):
        hits = cross[k]
        frames = sum(len(sl) for v in hits.values() for sl, _ in v)
        detail = "; ".join(
            f"{d} [{','.join(str(s) for s in sl)}] {p.replace('|', '/')[:90]}"
            for d, v in sorted(hits.items()) for sl, p in v)
        L.append(f"| {k}, {CAUSES[k]} | {len(hits)} | {frames} | {detail} |")
    L += ["", "## The scorer's themes, a word match by runs", "",
          "It finds candidates. Read the evidence below before believing a count.", "",
          f"| theme | runs (of {n}) | runs |", "|---|---|---|"]
    ranked = sorted(((t, r) for t, r in themes.items() if r), key=lambda x: (-len(x[1]), x[0]))
    for t, r in ranked:
        L.append(f"| {t} | {len(r)} | {', '.join(r)} |")
    if not ranked:
        L.append("| none matched | 0 | |")
    L += ["", "## Each run's craft cycle, weakest frames and fix", ""]
    for name, s in evidence:
        cc = s.get("craft_cycle") or {}
        L.append(f"**{name}**: craft cycle art {cc.get('art_before', '-')} to {cc.get('art_after', '-')}, "
                 f"frames {cc.get('frames', '-')}")
        for w in s.get("artwork_weakest_frames") or []:
            if isinstance(w, dict):
                L.append(f"- slide {w.get('slide')}: {str(w.get('problem', ''))[:300]}")
        if s.get("one_sentence_fix"):
            L.append(f"- fix: {str(s['one_sentence_fix'])[:400]}")
        L.append("")
    open_q = [ln for ln in queue_text.splitlines() if ln.startswith("- [ ] ")]
    L += ["## The queue, open items", ""] + (open_q or ["- none"]) + [""]
    data = {"runs": n,
            "causes": {k: len(v) for k, v in causes.items()},
            "cross_frame": {k: len(v) for k, v in cross.items()},
            "themes": [{"theme": t, "runs": len(r)} for t, r in ranked]}
    return "\n".join(L), data


def trend(days):
    try:
        out = subprocess.run([sys.executable, str(REPO / "scripts" / "trend_check.py"), "--window", str(days)],
                             capture_output=True, text=True, timeout=300)
        return out.stdout or out.stderr
    except Exception as exc:                       # noqa: BLE001
        return f"trend_check.py could not run: {exc}"


def self_test():
    bad = 0

    def ok(label, cond, extra=""):
        nonlocal bad
        print(f"  {'ok  ' if cond else 'FAIL'}  {label}{'' if cond else '  ' + extra}")
        bad += 0 if cond else 1

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for name in ("2026-10-01", "2026-10-02", "2026-09-20"):
            d = root / name
            d.mkdir()
            (d / "score_report.json").write_text(json.dumps({
                "criteria": [{"name": "Artwork craft &amp; genuine detail", "score": 6.5,
                              "notes": "04 remains a 2.5D step chart with no contact shadow"}],
                "artwork_weakest_frames": [{"slide": 4, "problem": "the lower third is a flat grey band"}],
                "one_sentence_fix": "restage 04 in akthree", "craft_cycle": {"art_before": 6.5, "art_after": 7.0,
                                                                            "frames": [4]}}))
            (d / "flow_review.json").write_text(json.dumps({"craft": {"weakest_frames": [
                {"slide": 4, "cause": "b"}, {"slide": 8, "cause": "C"}, {"slide": 9, "cause": "z"}],
                "cross_frame": [{"cause": "E", "slides": [3, 4, 6], "problem": "the arc | does not read"},
                                {"cause": "a", "slides": [1, 2]}, {"cause": "q", "slides": [5]}, "junk"]}}))
        text, data = digest(root, "2026-10-02", 7, "## Open\n- [ ] 2026-10-01 | repeat: 1 | x\n", "TREND x")
        th = {t["theme"]: t["runs"] for t in data["themes"]}
        ok("a run outside the window is not read", data["runs"] == 2, str(data))
        ok("the flow critic's causes are counted by its own label, any case",
           data["causes"]["b"] == 2 and data["causes"]["c"] == 2 and data["causes"]["a"] == 0, str(data))
        ok("an unknown cause letter is not counted", sum(data["causes"].values()) == 4, str(data))
        ok("the cross-frame causes are counted apart, by runs, any case",
           data["cross_frame"]["e"] == 2 and data["cross_frame"]["a"] == 2
           and sum(data["cross_frame"].values()) == 4 and data["causes"]["e"] == 0, str(data))
        ok("the cross-frame table carries its slides, frames and an escaped problem",
           "| e, no tonal or density arc across the deck | 2 | 6 |" in text
           and "[3,4,6] the arc / does not read" in text, text[text.find("cross-frame"):][:600])
        ok("an escaped criterion name is still read as artwork",
           th.get("the depth frame does not deliver depth (2.5D, flat chart)") == 2, str(th))
        ok("the lower third and the contact shadow are their own themes",
           th.get("a dead, flat or empty region, the lower third above all") == 2
           and th.get("no contact shadow, or an object that floats") == 2, str(th))
        ok("the trend, the craft cycle, the fix and the queue reach the digest verbatim",
           "TREND x" in text and "6.5 to 7.0" in text and "restage 04" in text and "repeat: 1" in text)
        e, _ = digest(root, "2026-08-01", 7, "", "")
        ok("an empty week says so rather than failing", "0 shipped run(s)" in e and "none matched" in e)
    live, _ = digest(RUNS, "2026-10-02", 7, "", "")
    ok("the live corpus digests", "## The flow critic's causes" in live)
    print("\nweek_digest self-test: " + ("all passed" if not bad else f"{bad} FAILED"))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    text, data = digest(RUNS, a.date, a.days, QUEUE.read_text(encoding="utf-8") if QUEUE.exists() else "",
                        trend(a.days))
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"week_digest: {data['runs']} run(s), causes {data['causes']}, written to {a.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
