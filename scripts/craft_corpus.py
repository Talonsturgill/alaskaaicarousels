#!/usr/bin/env python3
"""craft_corpus.py, the artwork-craft corpus study.

WHY (2026-07-29). Artwork craft has been the weakest rubric criterion in 16 of
the first 19 runs. Two attempts to gate it have now been made and both had to
stop at the same wall: a threshold guessed from one or two examples either
fires on everything or on nothing.

  - 2026-07-26 tried an ABSOLUTE craft-density floor and rejected it, because
    it failed 48 to 60 percent of every slide the series had shipped. That run
    hand-labelled 45 slides to find out, and then threw the labels away.
  - 2026-07-29 tried colour separability and occlusion on a declared encoding.
    Calibrated against one known-bad and one known-good, BOTH metrics came out
    backwards (see qa.py encoding_reads).

The missing ingredient both times was a corpus. This script supplies one: it
derives per-slide labels from what the scorers actually wrote, computes
objective features over every shipped slide, and reports whether ANY feature
separates the slides scorers named from the slides they did not.

It is a study, not a gate. It ships no threshold. Its output is evidence for
or against gating, and the honest answer is allowed to be "no feature here
separates them", which is worth knowing and is why the labels are persisted
this time instead of being recomputed by hand every six runs.

Labels are DERIVED, so they are re-runnable and auditable: the artwork-craft
criterion notes plus the disclosed shortfalls of each score_report are scanned
for slide references. Derivation is imperfect; --dump-labels prints them for
inspection and knowledge/CRAFT_LABEL_OVERRIDES.json can correct any of them by
hand, with a reason.

Usage:
  python scripts/craft_corpus.py                 # the study
  python scripts/craft_corpus.py --dump-labels   # audit the derived labels
  python scripts/craft_corpus.py --json          # machine-readable
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / ".claude" / "skills" / "carousel-engine"))

DESIGN_W, DESIGN_H = 1080, 1350

# Words that mean the scorer is talking about the ARTWORK, not the copy, the
# sourcing or the layout. Kept deliberately tight: a note about a clipped label
# is a legibility complaint and must not be labelled an artwork failure.
CRAFT_WORDS = re.compile(
    r"\b(flat|flattened|dead\s+(?:lower|bottom|zone|quiet)|no\s+modeled|unmodeled|"
    r"does\s+not\s+read|doesn't\s+read|did\s+not\s+render|reads?\s+as\s+(?:a\s+)?"
    r"(?:plain|flat|one|uniform)|vector\s+fill|no\s+texture|no\s+detail|thins?\s+out|"
    r"inert|empty\s+(?:bottom|band|lower)|never\s+drawn|contributes?\s+(?:almost\s+)?"
    r"nothing|uniform\s+\w+\s+extrusion|simple\s+\w*\s*line-?diagram|"
    r"flat\s+(?:canvas|hero|fallback))\b", re.I)

# A scorer naming a slide FAVOURABLY is not a defect label, and the first
# derivation pass proved that matters: "S6 rendered AK3D thermal hero RESOLVES
# the chronic flat-hero weakness" and "honesty handled with GENUINE CRAFT"
# both mention a slide and both contain craft vocabulary, and both were being
# labelled as artwork failures. Praise vetoes a sentence unless it also
# carries an explicit defect verb, which keeps mixed sentences of the form
# "real PBR hero, BUT S04's lit point renders at 7px".
PRAISE = re.compile(
    r"\b(resolves?|resolved|genuine\s+craft|ship-?worthy|strongest|excellent|"
    r"admirable|outstanding|best\s+(?:in|of|fusion)|zero\s+hard\s+fails|"
    r"handled\s+with|real\s+atmosphere)\b", re.I)
DEFECT = re.compile(
    r"\b(dead|flat|thin|never\s+drawn|fails?|failed|missing|does\s+not|doesn't|"
    r"did\s+not|weak|inert|empty|docked|held\s+from|shipped\s+as\s+the\s+flat|"
    r"under|below|too\s+\w+|but)\b", re.I)

SLIDE_REF = re.compile(r"\b(?:slides?|s)\s*0*(\d{1,2})\b", re.I)


def canon_crit(name):
    s = str(name).lower().split("(")[0].split(":")[0]
    s = s.replace("&", " and ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def craft_score(report):
    for c in (report.get("criteria") or []):
        if not isinstance(c, dict):
            continue
        if "artwork craft" in canon_crit(c.get("name", "")):
            for k in ("score", "score_0_10"):
                if c.get(k) is not None:
                    try:
                        return float(c[k])
                    except (TypeError, ValueError):
                        pass
    return None


def craft_text(report):
    """Every piece of scorer prose that is plausibly about the artwork."""
    bits = []
    for c in (report.get("criteria") or []):
        if isinstance(c, dict) and "artwork craft" in canon_crit(c.get("name", "")):
            for k in ("notes", "note", "why", "justification"):
                if c.get(k):
                    bits.append(str(c[k]))
    for k in ("shortfalls_to_disclose_in_the_email", "honest_shortfalls",
              "editor_notes_for_email", "editor_notes", "one_sentence_fix", "notes"):
        v = report.get(k)
        if isinstance(v, list):
            bits += [str(x) for x in v]
        elif v:
            bits.append(str(v))
    return bits


def derive_labels(report, n_slides):
    """-> {slide_no: [reasons]} for slides the scorer named on ARTWORK grounds.

    A sentence must mention a slide AND carry craft vocabulary. Sentences are
    split first so 'slide 5's label is clipped, and the art is flat' does not
    tar slide 5 with the second clause's complaint about a different slide.
    """
    named = {}
    for blob in craft_text(report):
        for sent in re.split(r"(?<=[.;])\s+", blob):
            if not CRAFT_WORDS.search(sent):
                continue
            if PRAISE.search(sent) and not DEFECT.search(sent):
                continue
            for m in SLIDE_REF.finditer(sent):
                n = int(m.group(1))
                if 1 <= n <= n_slides:
                    named.setdefault(n, []).append(sent.strip()[:150])
    return named


# ------------------------------------------------------------------ features

def _box_down(a, k):
    h, w = a.shape[:2]
    h, w = (h // k) * k, (w // k) * k
    a = a[:h, :w]
    return a.reshape(h // k, k, w // k, k, a.shape[2]).mean(axis=(1, 3))


def features(path):
    im = Image.open(path).convert("RGB")
    if im.width != DESIGN_W:
        im = im.resize((DESIGN_W, int(im.height * DESIGN_W / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

    # Grain is high frequency and would read as craft everywhere, so the
    # modeled-tone measure runs on a box-downsampled frame, same as the
    # shipped frame_balance gate.
    d = _box_down(a, 3)
    dl = 0.2126 * d[..., 0] + 0.7152 * d[..., 1] + 0.0722 * d[..., 2]
    CELL = 9
    rows, cols = dl.shape[0] // CELL, dl.shape[1] // CELL
    cl = dl[:rows * CELL, :cols * CELL]
    cells = cl.reshape(rows, CELL, cols, CELL).transpose(0, 2, 1, 3).reshape(rows, cols, -1)
    spread = np.percentile(cells, 90, axis=2) - np.percentile(cells, 10, axis=2)
    ent = []
    for r in range(rows):
        row = []
        for c in range(cols):
            h, _ = np.histogram(cells[r, c], bins=16, range=(0, 255))
            p = h / max(1, h.sum())
            p = p[p > 0]
            row.append(float(-(p * np.log2(p)).sum() / 4.0))   # /log2(16)
        ent.append(row)
    ent = np.array(ent)
    modeled = (spread > 8) & (ent > 0.45)

    gx = np.abs(np.diff(lum, axis=1)).mean()
    gy = np.abs(np.diff(lum, axis=0)).mean()
    coarse = _box_down(a, 8)
    cg = 0.2126 * coarse[..., 0] + 0.7152 * coarse[..., 1] + 0.0722 * coarse[..., 2]
    coarse_g = (np.abs(np.diff(cg, axis=1)).mean() + np.abs(np.diff(cg, axis=0)).mean()) / 2

    lab_a = a[..., 0] - a[..., 1]
    lab_b = a[..., 1] - a[..., 2]
    p = np.histogram(lum, bins=32, range=(0, 255))[0].astype(float)
    p = p / max(1.0, p.sum())
    p = p[p > 0]

    thirds = np.array_split(modeled, 3, axis=0)
    return {
        "modeled_frac": float(modeled.mean()),
        "modeled_bottom_ratio": float(thirds[2].mean() / max(1e-6, modeled.mean())),
        "flat_frac": float((spread <= 4).mean()),
        "grad_energy": float((gx + gy) / 2),
        "detail_ratio": float(((gx + gy) / 2) / max(1e-6, coarse_g)),
        "tonal_entropy": float(-(p * np.log2(p)).sum() / 5.0),
        "chroma_spread": float((lab_a.std() + lab_b.std()) / 2),
        "hi_mass": float((lum > np.percentile(lum, 98)).mean() * 100),
        "mid_contrast": float(lum.std()),
    }


# ------------------------------------------------------------------ analysis

def rank(v):
    o = np.argsort(np.argsort(np.asarray(v, float)))
    return o.astype(float)


def spearman(x, y):
    x, y = rank(x), rank(y)
    x = x - x.mean(); y = y - y.mean()
    d = np.sqrt((x * x).sum() * (y * y).sum())
    return float((x * y).sum() / d) if d > 1e-12 else 0.0


def auc(pos, neg):
    """P(a random positive scores above a random negative), folded to 0.5..1."""
    if not len(pos) or not len(neg):
        return None
    allv = np.concatenate([pos, neg])
    order = np.argsort(allv, kind="mergesort")
    r = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    n1 = len(pos)
    a = (r[:n1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * len(neg))
    return max(a, 1 - a)


def main():
    ap = argparse.ArgumentParser(description="artwork-craft corpus study")
    ap.add_argument("--runs-dir", default=str(REPO / "runs"))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dump-labels", action="store_true")
    args = ap.parse_args()

    ov_path = REPO / "knowledge" / "CRAFT_LABEL_OVERRIDES.json"
    overrides = {}
    if ov_path.exists():
        try:
            overrides = json.loads(ov_path.read_text()).get("slides", {})
        except Exception as e:
            print(f"craft_corpus: overrides unreadable ({e})", file=sys.stderr)

    rows, decks, unreadable = [], [], []
    for d in sorted(p for p in Path(args.runs_dir).iterdir() if p.is_dir()):
        sp = d / "score_report.json"
        if not sp.exists():
            continue
        try:
            rep = json.loads(sp.read_text())
        except Exception as e:
            unreadable.append(f"{d.name}: {e}")
            continue
        slides = sorted(list(d.glob("slide-*.webp")) + list(d.glob("slide-*.png")))
        slides = [s for s in slides if re.search(r"slide-\d+\.(webp|png)$", s.name)]
        if not slides:
            continue
        cs = craft_score(rep)
        named = derive_labels(rep, len(slides))
        decks.append({"run": d.name, "craft": cs, "named": sorted(named)})
        for s in slides:
            n = int(re.search(r"slide-(\d+)", s.name).group(1))
            key = f"{d.name}/{n:02d}"
            lab = 1 if n in named else 0
            if key in overrides:
                lab = 1 if overrides[key].get("bad") else 0
            try:
                f = features(s)
            except Exception as e:
                unreadable.append(f"{key}: {e}")
                continue
            rows.append({"run": d.name, "slide": n, "key": key, "bad": lab,
                         "craft": cs, "reasons": named.get(n, []), **f})

    if args.dump_labels:
        for dk in decks:
            print(f"{dk['run']}  craft={dk['craft']}  named={dk['named'] or '-'}")
        for r in rows:
            if r["bad"]:
                print(f"  {r['key']}: {(r['reasons'] or ['(override)'])[0][:110]}")
        return 0

    if not rows:
        print("craft_corpus: no slides found")
        return 2

    feats = [k for k in rows[0] if k not in
             ("run", "slide", "key", "bad", "craft", "reasons")]
    pos = [r for r in rows if r["bad"]]
    neg = [r for r in rows if not r["bad"]]

    out = {"slides": len(rows), "named_bad": len(pos), "decks": len(decks),
           "unreadable": unreadable, "features": {}}

    # Deck-level: does the feature track the scorer's artwork-craft score?
    dmap = {}
    for r in rows:
        dmap.setdefault(r["run"], []).append(r)
    dscore, dfeat = [], {f: [] for f in feats}
    for run, rs in sorted(dmap.items()):
        if rs[0]["craft"] is None:
            continue
        dscore.append(rs[0]["craft"])
        for f in feats:
            dfeat[f].append(float(np.median([x[f] for x in rs])))

    # AUC alone is not evidence. With 24 positives against 147 negatives the
    # null standard error is about 0.064, so an eyeballed "0.65 looks like
    # signal" is barely two standard errors out, and NINE features were tried.
    # Without a multiple-comparison correction this study would manufacture a
    # gate out of noise, which is exactly the failure the last two attempts
    # made in a smaller way.
    n1, n2 = len(pos), len(neg)
    se = float(np.sqrt((n1 + n2 + 1) / (12.0 * max(1, n1) * max(1, n2)))) if pos else None
    for f in feats:
        a = (auc(np.array([r[f] for r in pos], float),
                 np.array([r[f] for r in neg], float)) if pos else None)
        z = ((a - 0.5) / se) if (a is not None and se) else None
        # two-sided normal p, then Bonferroni over the features tried
        praw = (float(math.erfc(abs(z) / math.sqrt(2))) if z is not None else None)
        out["features"][f] = {
            "slide_auc": a,
            "z_vs_chance": None if z is None else round(z, 2),
            "p_raw": None if praw is None else round(praw, 4),
            "p_bonferroni": None if praw is None else round(min(1.0, praw * len(feats)), 4),
            "deck_spearman": spearman(dfeat[f], dscore) if len(dscore) > 3 else None,
        }
    out["null_se"] = se
    out["features_tried"] = len(feats)

    # Leave-one-deck-out: a feature that only works because of one deck is not
    # a feature. Recompute the best feature's AUC with each deck withheld.
    ranked0 = sorted(feats, key=lambda f: -(out["features"][f]["slide_auc"] or 0))
    if pos and ranked0:
        bf = ranked0[0]
        loo = []
        for run in sorted(dmap):
            P = np.array([r[bf] for r in pos if r["run"] != run], float)
            N = np.array([r[bf] for r in neg if r["run"] != run], float)
            v = auc(P, N)
            if v is not None:
                loo.append(v)
        if loo:
            out["loo"] = {"feature": bf, "min": round(min(loo), 3),
                          "max": round(max(loo), 3),
                          "mean": round(float(np.mean(loo)), 3)}

    if args.json:
        print(json.dumps(out, indent=2))
        return 0

    print(f"CRAFT CORPUS -- {len(rows)} slides across {len(decks)} scored decks, "
          f"{len(pos)} labelled bad by scorer prose, {len(neg)} not.")
    print()
    print("Can any feature tell a scorer-named slide from the rest?")
    print("  slide_auc 0.50 = no signal at all, 1.00 = perfect. Anything under")
    print("  about 0.65 is noise and cannot carry a threshold.")
    print(f"  {'feature':22} {'slide_auc':>10} {'deck_rho':>10}")
    ranked = sorted(feats, key=lambda f: -(out["features"][f]["slide_auc"] or 0))
    for f in ranked:
        a = out["features"][f]["slide_auc"]
        s = out["features"][f]["deck_spearman"]
        flag = ""
        if a is not None and a >= 0.65:
            flag = "  <-- possible signal"
        print(f"  {f:22} {a if a is None else round(a,3):>10} "
              f"{s if s is None else round(s,3):>10}{flag}")
    print()
    best = ranked[0]
    bf = out["features"][best]
    ba, pb = bf["slide_auc"], bf["p_bonferroni"]
    print(f"null SE {round(out['null_se'],3)} at {len(pos)} vs {len(neg)}; "
          f"{out['features_tried']} features tried, so p is Bonferroni corrected.")
    if out.get("loo"):
        l = out["loo"]
        print(f"leave-one-deck-out on {l['feature']}: AUC ranges "
              f"{l['min']} to {l['max']} (mean {l['mean']}).")
    print()
    survives = (ba is not None and ba >= 0.65 and pb is not None and pb < 0.05)
    if not survives:
        print(f"VERDICT: NO feature separates scorer-named slides from the rest.")
        print(f"  Best is {best}, AUC {round(ba,3)}, corrected p = {pb}, and its")
        print(f"  correlation with the deck's own craft score is "
              f"{round(bf['deck_spearman'] or 0, 3)}, i.e. none.")
        print("  An objective artwork-craft gate is NOT supportable on this corpus.")
        print("  Do not ship a threshold. The numbers do not carry one.")
    else:
        print(f"VERDICT: {best} survives correction (AUC {round(ba,3)}, "
              f"p={pb}). Worth a gate proposal.")
    for u in unreadable:
        print(f"  [unreadable] {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
