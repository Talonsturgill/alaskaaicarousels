#!/usr/bin/env python3
"""tonal_arc_check.py -- does the contact sheet carry the tonal arc the CRAFT PLAN declared?

WHY THIS EXISTS (2026-10-04, the first weekly machine pass).

The storyboard's CRAFT PLAN has declared a `Tonal arc:` line since 2026-09-26, and
dossier_check.py holds the line to saying where the deck peaks and where it is
darkest. Nothing ever measured whether the BUILD delivered it. In the week of
September 28th to October 3rd the flow critic's `craft.cross_frame` list named
cause e, "no tonal or density arc across the deck", on all six shipped decks
(week_digest.py's cross-frame table, which is new the same day), and twice it
named the exact miss a number can see:

    2026-10-02  "The planned tonal arc (lit peak on 04 ...) doesn't show on the
                 contact sheet. 04 is mid-dark and no brighter than 03."
                 Measured: 04 mean L* 17, fifth of nine; 07 is brightest at 26.
    2026-09-30  "lift 01/02, make 05 brightest, darken and cool 07."
                 Measured: the declared darkest, 07, is fifth darkest of nine.
    2026-10-01  "tonal arc does not read." Measured: the nine frames span
                 11 to 16 L*, one tone.

The flow critic saw each of those at round 1 of its review, after the build, and
the craft cycle then had one pass to fix it. This puts the same reading in front
of every reader from the first render: the declared peak and darkest frames and
where each one actually measures.

WHAT IS MEASURED. Each frame's mean CIE L* at contact-sheet scale (box-downsampled
to 216x270, which is what a contact sheet and a thumb show). Mean lightness is
what "the lit peak" and "the darkest close" mean on a sheet of nine. It is NOT a
judgement of warmth, of a highlight, or of a frame that is dark with one bright
object, and the critic is still the judge of those: on 2026-10-03 it said "05 is
not the noon peak" of a frame that measures brightest of nine, because the miss
it meant was colour.

SO IT WARNS AND NEVER FAILS. A WARN names the frame, its rank and its L*, and the
frame that actually holds the place. It fires when:
  - no declared peak frame is in the brightest two, or within PEAK_TOL L* of the
    brightest frame;
  - no declared darkest frame is in the darkest two, or within PEAK_TOL L* of the
    darkest frame;
  - the whole sheet spans less than FLAT_SPAN L* (one tone, whatever the line says).
Calibrated on the eight shipped decks that carry a Tonal arc line (2026-09-26 to
2026-10-03): it warns on 09-26, 09-30, 10-01 and 10-02 and passes the other four.
The flow critic named the same miss in words on 09-30, 10-01 and 10-02; 09-26 has
no flow review on record. Today's deck (2026-10-04) passes.

The line is read the way authors write it: clauses split at commas, semicolons,
"then", "while", "but" and an "and" that does not join two frame numbers; in a
clause with a peak word (brightest, lightest, highest key, peak, peaks) the frame
numbers after the word are the peak, and likewise for darkest, lowest key,
trough. A peak word that describes a mark rather than a frame ("the brightest
type on 08", "the only bright point", "the brightest ground on 02", "one warm
gold peak on 09") is skipped. When the line names a frame-level extreme outright
("the highest key", "the brightest frame"), that wins over a looser peak word in
another clause. A line with no darkest word whose author wrote the dark end as
"low" or "low key" (2026-10-01, 2026-10-02) has those frames read as its darkest,
and a side the line still never names is a WARN, not a pass on half the census
(Codex review of PR #417). Frames are two-digit numbers, which is how every
storyboard writes them.

    python3 scripts/tonal_arc_check.py --run-dir out/2026-10-04 [--render-dir ...] [--json]
    python3 scripts/tonal_arc_check.py --self-test

Read-only. Exit 0 when it measured (PASS or WARN, the verdict is printed and in
--json), 2 when it could not look (no storyboard, no Tonal arc line, no renders).
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

PEAK_TOL = 3.0      # L* within which a declared frame shares the extreme
TOP_N = 2           # a declared peak (or darkest) may sit this far from the extreme by rank
FLAT_SPAN = 8.0     # a sheet whose frames span less than this many L* reads as one tone
SHEET_W, SHEET_H = 216, 270

ARC_RE = re.compile(r"^\s*[-*]?\s*Tonal arc:\s*(\S.*)$", re.M | re.I)
CRAFT_HEAD_RE = re.compile(r"^##\s+CRAFT PLAN\b.*$", re.M)
_MARK = r"(?!\s+(?:\w+\s+)?(?:type|point|points|object|accent|accents|glint|glints|highlight|" \
        r"highlights|halo|star|lamp|mark|marks|word|words|figure|numeral|line|lines|ground)\b)"
PEAK_RE = re.compile(r"\b(?:brightest|lightest|highest[- ]key|peaks?)\b" + _MARK, re.I)
DARK_RE = re.compile(r"\b(?:darkest|lowest[- ]key|trough)\b" + _MARK, re.I)
# A frame-level extreme said outright; when a side has one, it is that side's declaration.
STRONG_RE = re.compile(r"\b(?:highest|lowest)[- ]key\b|\b(?:brightest|lightest|darkest)\s+frame\b", re.I)
# "one warm gold peak": a counted thing is an object in the frame, not the frame.
ONE_RE = re.compile(r"\bone\s+(?:\w+\s+){0,2}$", re.I)
# The dark end as authors also write it, read only when no darkest word is present.
LOW_RE = re.compile(r"\blow(?:[- ]key)?\b", re.I)
FRAME_RE = re.compile(r"\b(0[1-9]|1[0-9])\b")
CLAUSE_RE = re.compile(r"[,;]|\bthen\b|\bwhile\b|\bbut\b|\band\b(?!\s+(?:0[1-9]|1[0-9])\b)", re.I)


def arc_line(text):
    """The Tonal arc line inside the CRAFT PLAN section, else the first anywhere."""
    m = CRAFT_HEAD_RE.search(text)
    if m:
        nxt = re.search(r"^##\s", text[m.end():], re.M)
        block = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
        a = ARC_RE.search(block)
        if a:
            return a.group(1).strip()
    a = ARC_RE.search(text)
    return a.group(1).strip() if a else None


def declared(line):
    """({peak frames}, {darkest frames}) as the line names them."""
    found = {"peak": ([], []), "dark": ([], []), "low": ([], [])}   # (strong, any) frame lists
    for clause in CLAUSE_RE.split(line):
        for rx, side in ((PEAK_RE, "peak"), (DARK_RE, "dark"), (LOW_RE, "low")):
            m = rx.search(clause)
            if not m or ONE_RE.search(clause[:m.start()]):
                continue
            after = FRAME_RE.findall(clause[m.end():])
            nums = [int(n) for n in (after or FRAME_RE.findall(clause[:m.start()])[-1:])]
            found[side][1].extend(nums)
            if STRONG_RE.match(clause, m.start()):
                found[side][0].extend(nums)

    def pick(side):
        strong, loose = found[side]
        return set(strong or loose)

    peaks, darks = pick("peak"), pick("dark")
    if not darks:
        darks = pick("low")
    return peaks, darks


def lstar(path):
    a = np.asarray(Image.open(path).convert("RGB").resize((SHEET_W, SHEET_H), Image.BOX),
                   dtype=np.float64) / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    y = lin @ np.array([0.2126, 0.7152, 0.0722])
    f = np.where(y > 216 / 24389, np.cbrt(y), (24389 / 27 * y + 16) / 116)
    return float((116 * f - 16).mean())


def frames(rdir):
    """{n: path} for slide-NN.png, else slide-NN.webp (a shipped runs/<date>/). Never
    a render.py canvas layer (slide-NN.canvas.png)."""
    out = {}
    for ext in ("png", "webp"):
        for p in sorted(Path(rdir).glob("slide-[0-9][0-9].%s" % ext)):
            out.setdefault(int(p.stem.split("-")[1]), p)
    return out


def judge(line, L):
    """Return (verdict, lines, data) for a declared line and {frame: L*}."""
    peaks, darks = declared(line)
    order = sorted(L, key=lambda k: -L[k])            # brightest first
    hi, lo = L[order[0]], L[order[-1]]
    span = hi - lo
    msgs, warns = [], 0

    def rank_bright(n):
        return order.index(n) + 1

    def rank_dark(n):
        return len(order) - order.index(n)

    for name, want, rank, extreme, holder, near in (
            ("peak", peaks, rank_bright, hi, order[0], lambda v: v >= hi - PEAK_TOL),
            ("darkest", darks, rank_dark, lo, order[-1], lambda v: v <= lo + PEAK_TOL)):
        known = sorted(n for n in want if n in L)
        missing = sorted(n for n in want if n not in L)
        if missing:
            msgs.append("[NOTE] the line names %s frame(s) %s that have no render"
                        % (name, ", ".join("%02d" % n for n in missing)))
        if not known:
            warns += 1
            msgs.append("[WARN] the line declares no measurable %s frame, so half the arc "
                        "can't be checked; name the frame that holds it" % name)
            continue
        best = min(known, key=rank)
        if rank(best) <= TOP_N or near(L[best]):
            msgs.append("[PASS] %s: %02d measures L* %.1f, %s of %d by %s"
                        % (name, best, L[best], _ord(rank(best)), len(L),
                           "lightness" if name == "peak" else "darkness"))
        else:
            warns += 1
            msgs.append("[WARN] %s: the plan puts it on %s, and %02d measures L* %.1f, %s of %d "
                        "by %s; %02d holds that place at L* %.1f. Re-key %02d or say in the "
                        "reconciliation that the arc moved"
                        % (name, ", ".join("%02d" % n for n in known), best, L[best],
                           _ord(rank(best)), len(L),
                           "lightness" if name == "peak" else "darkness",
                           holder, extreme, best))
    if span < FLAT_SPAN:
        warns += 1
        msgs.append("[WARN] one tone: the sheet spans L* %.1f to %.1f (%.1f, under %.1f), so no "
                    "declared arc can read on it" % (lo, hi, span, FLAT_SPAN))
    data = {"line": line, "peaks": sorted(peaks), "darkest": sorted(darks),
            "lstar": {"%02d" % k: round(v, 1) for k, v in sorted(L.items())},
            "brightest": "%02d" % order[0], "darkest_measured": "%02d" % order[-1],
            "span": round(span, 1), "warns": warns}
    return ("WARN" if warns else "PASS"), msgs, data


def _ord(n):
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))


def run(run_dir, render_dir=None):
    run_dir = Path(run_dir)
    sb = run_dir / "storyboard.md"
    if not sb.exists():
        return None, "storyboard.md missing in %s" % run_dir
    line = arc_line(sb.read_text(encoding="utf-8"))
    if not line:
        return None, "no 'Tonal arc:' line in the storyboard's CRAFT PLAN"
    rdir = Path(render_dir) if render_dir else (
        run_dir / "render" if (run_dir / "render").is_dir() else run_dir)
    fr = frames(rdir)
    if len(fr) < 3:
        return None, "fewer than three rendered frames in %s" % rdir
    L = {n: lstar(p) for n, p in fr.items()}
    return judge(line, L), None


def report(verdict, msgs, data):
    out = ["TONAL ARC -- the CRAFT PLAN's line against each frame's mean L* at contact-sheet scale",
           "  declared: %s" % data["line"][:300],
           "  declared peak %s, declared darkest %s" % (
               ", ".join("%02d" % n for n in data["peaks"]) or "none",
               ", ".join("%02d" % n for n in data["darkest"]) or "none"),
           "  measured: " + "  ".join("%s %.0f" % (k, v) for k, v in data["lstar"].items()),
           "  brightest %s, darkest %s, span %.1f L*" % (
               data["brightest"], data["darkest_measured"], data["span"])]
    out += ["  " + m for m in msgs]
    out.append("VERDICT: %s, %d warn(s). A census for the flow critic and the craft cycle; "
               "it never fails a run." % (verdict, data["warns"]))
    return "\n".join(out)


def self_test():
    bad = 0

    def ok(label, cond, extra=""):
        nonlocal bad
        print("  %s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond else "  " + str(extra)))
        bad += 0 if cond else 1

    p, d = declared("dim on 01, warm lift on 02, darkest trough on 03, brightest peak on 04, "
                    "even plateau on 05, then it falls through 07 to the dark reverse shot on 08")
    ok("brightest peak and darkest trough are read", p == {4} and d == {3}, (p, d))
    p, d = declared("low and cool on 01, brightening through 02 to the noon peak on 05, mid on 06, "
                    "closing darkest on 09 with Polaris the only bright point")
    ok("the number after the peak word is the peak, not one before it", p == {5} and d == {9}, (p, d))
    p, d = declared("the bright overcast morning peak on 06 and 07, dusk on 08, the darkest close on 09")
    ok("'06 and 07' stays one clause", p == {6, 7} and d == {9}, (p, d))
    p, d = declared("the deck's highest key on paper 03 and its darkest field on ink 04, dark with "
                    "the brightest type on 08")
    ok("'highest key' counts, 'brightest type' does not", p == {3} and d == {4}, (p, d))
    p, d = declared("the lit range peaks on 06, calm close")
    ok("a verb 'peaks' counts", p == {6} and d == set(), (p, d))
    p, d = declared("low key on 01, the brightest ground on 02, cooler even plan on 03, the highest "
                    "key on 05, the darkest on 06, dark with the brightest type on 08, one warm gold "
                    "peak on 09")
    ok("2026-09-28: component peaks drop out and 'highest key' is the peak", p == {5} and d == {6},
       (p, d))
    p, d = declared("low key and cool 01 to 03, the lit peak on 04, steady 05, the breather drops low "
                    "on 06, warmest on 07 and 08 (manila), calm low key close on 09")
    ok("2026-10-02: a dark end written 'low key' is read as the darkest", p == {4} and
       d == {6, 9}, (p, d))
    p, d = declared("the lit peak on 05, low on 07, the darkest close on 09")
    ok("'low' is ignored when a darkest word is present", d == {9}, (p, d))

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        def deck(name, levels, line):
            r = root / name
            (r / "render").mkdir(parents=True)
            (r / "storyboard.md").write_text("# deck\n\n## CRAFT PLAN\n| slide | a | b |\n|---|---|---|\n"
                                             "Tonal arc: %s\n\n## SLIDE 01\n" % line)
            rng = np.random.default_rng(7)
            for i, v in enumerate(levels, 1):
                a = np.clip(v + rng.normal(0, 6, (SHEET_H * 2, SHEET_W * 2, 3)), 0, 255).astype(np.uint8)
                Image.fromarray(a).save(r / "render" / ("slide-%02d.png" % i))
                Image.fromarray(a).save(r / "render" / ("slide-%02d.canvas.png" % i))
            return r

        good = deck("good", [30, 60, 90, 140, 120, 80, 40],
                    "dark on 01, the lit peak on 04, falling to the darkest close on 01")
        (v, msgs, data), err = run(good)
        ok("a sheet that carries its arc PASSES", v == "PASS" and not err, msgs)
        ok("a canvas layer is never read as a frame", len(data["lstar"]) == 7, data["lstar"])
        # The 2026-10-02 shape: the declared peak measures fifth.
        bad_peak = deck("badpeak", [60, 40, 45, 55, 30, 75, 95, 70, 45],
                        "low key 01 to 03, the lit peak on 04, warmest on 07, calm low close on 09")
        (v, msgs, data), err = run(bad_peak)
        ok("a declared peak that measures mid-sheet WARNS and names the real peak",
           v == "WARN" and any("[WARN] peak" in m and "07 holds that place" in m for m in msgs), msgs)
        flat = deck("flat", [38, 40, 41, 39, 42, 40, 38, 41, 39],
                    "dark on 01, the lit peak on 05, the darkest close on 09")
        (v, msgs, data), err = run(flat)
        ok("a one-tone sheet WARNS whatever the line says",
           v == "WARN" and any("one tone" in m for m in msgs), msgs)
        nodark = deck("nodark", [30, 60, 90, 140, 120, 80, 40],
                      "quiet on 01, the lit peak on 04, a calm close on 07")
        (v, msgs, data), err = run(nodark)
        ok("a line that never names its dark end WARNS rather than passing half the census",
           v == "WARN" and any("no measurable darkest" in m for m in msgs), msgs)
        none = root / "none"
        (none / "render").mkdir(parents=True)
        (none / "storyboard.md").write_text("## CRAFT PLAN\nno arc here\n")
        res, err = run(none)
        ok("no Tonal arc line means it could not look", res is None and "Tonal arc" in err, err)
    print("\ntonal_arc_check self-test: " + ("all passed" if not bad else "%d FAILED" % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run-dir")
    ap.add_argument("--render-dir")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.run_dir:
        ap.error("--run-dir is required (or --self-test)")
    res, err = run(a.run_dir, a.render_dir)
    if res is None:
        if a.json:
            print(json.dumps({"verdict": "n/a", "error": err}))
        else:
            print("TONAL ARC -- could not look: %s" % err)
        return 2
    verdict, msgs, data = res
    if a.json:
        print(json.dumps(dict(data, verdict=verdict, lines=msgs), indent=2))
    else:
        print(report(verdict, msgs, data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
