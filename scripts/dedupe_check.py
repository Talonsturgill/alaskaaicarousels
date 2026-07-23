#!/usr/bin/env python3
"""Phase 4 pre-flight dedupe signal for the Alaska.Ai carousel routine.

WHY THIS EXISTS
    The Phase 4 DEDUPE GATE is a semantic judgment the showrunner makes by
    reading ledger/topics.json. On 2026-07-23 the intended lead (the XPRIZE
    Wildfire autonomous-response finals) was a near-exact repeat of Carousel
    No. 5 (2026-07-12) but slipped the first pass because the showrunner read
    the ledger entry's TRUNCATED title ("Alaska as the world's proving ground
    for ...") instead of the full topic/angle/entities/keywords text. It was
    caught only by luck. This tool removes the luck: given a candidate's
    entities/keywords (or a short free-text description), it greps the FULL
    text of every ledger entry inside the dedupe window and prints the entries
    that share the candidate's distinctive fingerprint, loudest first.

WHAT IT IS NOT
    It does NOT replace or weaken the human dedupe gate. It is an advisory
    pre-flight signal: a LIKELY DUPLICATE match (exit 1) means "stop and read
    this entry in full before the directors room", not "auto-reject". The
    90-day hard-fail rule is still the showrunner's call. Pure stdlib, offline.

USAGE
    python scripts/dedupe_check.py --entities "XPRIZE Wildfire, ACUASI, Dryad" \
                                   --keywords "wildfire, autonomous drone"
    python scripts/dedupe_check.py --desc "free text description of the candidate"
    # options: --topics PATH  --date YYYY-MM-DD (reference, default today)
    #          --window 120    --exclude-date YYYY-MM-DD (skip a ledger entry,
    #          e.g. the candidate's own already-appended row)  --json

EXIT CODES
    1  at least one ledger entry inside the window is a LIKELY DUPLICATE
       (read it in full before proceeding)
    0  no likely duplicate (soft overlaps, if any, are printed for review)
    2  usage / input error
"""

import argparse
import datetime as _dt
import json
import re
import sys

# Ubiquitous AK+AI terms that appear in nearly every deck; they carry no
# discriminating signal, so they are dropped before overlap is measured. This
# is a NOISE floor, not a gate: distinctive named entities (ANTHC, XPRIZE,
# ACUASI, Cerner ...) are never stopped, so real collisions still surface.
_STOP = {
    # generic english
    "the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "at", "by",
    "with", "as", "is", "are", "be", "its", "it", "this", "that", "from",
    "into", "over", "under", "not", "no", "vs", "via", "how", "who", "what",
    # ubiquitous domain terms (present across the whole ledger)
    "ai", "artificial", "intelligence", "machine", "learning", "ml", "model",
    "models", "alaska", "alaskan", "alaskas", "state", "statewide", "us",
    "2025", "2026", "data",
}

# Fields whose combined text is grepped. Order matters only for display.
_TEXT_FIELDS = ("topic", "angle", "headline")
_LIST_FIELDS = ("entities", "keywords")


def _norm(s):
    """Lowercase, strip punctuation to spaces, collapse whitespace."""
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _tokens(s):
    """Distinctive word tokens of a string (stopwords + 1-char dropped)."""
    return {t for t in _norm(s).split() if t not in _STOP and len(t) > 1}


def _phrases(items):
    """Normalized whole phrases from a list of entity/keyword strings,
    keeping only phrases that still carry a non-stopword token."""
    out = []
    for it in items:
        p = _norm(it)
        if p and _tokens(p):
            out.append(p)
    return out


def _entry_blob(entry):
    """Full normalized searchable text of a ledger entry (all fields)."""
    parts = []
    for f in _TEXT_FIELDS:
        parts.append(str(entry.get(f, "")))
    for f in _LIST_FIELDS:
        v = entry.get(f, [])
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
        else:
            parts.append(str(v))
    return _norm(" ".join(parts))


def _phrase_in(phrase, blob):
    """Whole-phrase (word-boundary) containment of a normalized phrase."""
    return re.search(r"(?:^| )" + re.escape(phrase) + r"(?:$| )", blob) is not None


def _parse_date(s):
    return _dt.date.fromisoformat(s)


def build_candidate(entities, keywords, desc):
    ent_phrases = _phrases(entities)
    kw_phrases = _phrases(keywords)
    tok = set()
    for p in ent_phrases + kw_phrases:
        tok |= _tokens(p)
    tok |= _tokens(desc or "")
    return {
        "entity_phrases": ent_phrases,
        "keyword_tokens": {t for p in kw_phrases for t in _tokens(p)},
        "tokens": tok,
    }


def score_entry(cand, entry):
    blob = _entry_blob(entry)
    entry_kw_tokens = {t for kw in entry.get("keywords", []) for t in _tokens(str(kw))}
    entry_tokens = _tokens(blob)

    entity_hits = sorted({p for p in cand["entity_phrases"] if _phrase_in(p, blob)})
    keyword_overlap = sorted(cand["keyword_tokens"] & entry_kw_tokens)

    union = cand["tokens"] | entry_tokens
    jaccard = (len(cand["tokens"] & entry_tokens) / len(union)) if union else 0.0

    # Classification. Distinctive named-entity overlap is the strongest
    # signal (two or more distinct named entities in common ~= the same story);
    # a high distinctive-token Jaccard is the secondary trigger.
    if len(entity_hits) >= 2 or jaccard >= 0.30:
        verdict = "LIKELY DUPLICATE"
    elif entity_hits or keyword_overlap or jaccard >= 0.12:
        verdict = "SOFT OVERLAP"
    else:
        verdict = "clear"

    return {
        "verdict": verdict,
        "entity_hits": entity_hits,
        "keyword_overlap": keyword_overlap,
        "jaccard": round(jaccard, 3),
    }


def run(cand, entries, ref_date, window, exclude_date):
    lo = ref_date - _dt.timedelta(days=window)
    results = []
    for e in entries:
        rd_raw = e.get("run_date")
        if not rd_raw:
            continue
        try:
            rd = _parse_date(rd_raw)
        except ValueError:
            continue
        if rd < lo or rd > ref_date:
            continue
        if exclude_date and rd == exclude_date:
            continue
        s = score_entry(cand, e)
        if s["verdict"] == "clear":
            continue
        s.update(run_date=rd_raw, carousel_no=e.get("carousel_no"),
                 topic=e.get("topic", ""), headline=e.get("headline", ""))
        results.append(s)
    order = {"LIKELY DUPLICATE": 0, "SOFT OVERLAP": 1}
    results.sort(key=lambda r: (order[r["verdict"]], -len(r["entity_hits"]), -r["jaccard"]))
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="Phase 4 pre-flight dedupe signal.")
    ap.add_argument("--entities", default="", help="comma-separated candidate entities")
    ap.add_argument("--keywords", default="", help="comma-separated candidate keywords")
    ap.add_argument("--desc", default="", help="free-text candidate description")
    ap.add_argument("--topics", default="ledger/topics.json")
    ap.add_argument("--date", default=None, help="reference date YYYY-MM-DD (default today)")
    ap.add_argument("--window", type=int, default=120, help="lookback days (default 120)")
    ap.add_argument("--exclude-date", default=None,
                    help="skip ledger entries on this run_date (e.g. the candidate's own row)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args(argv)

    def _split(s):
        return [x.strip() for x in s.split(",") if x.strip()]

    entities, keywords = _split(args.entities), _split(args.keywords)
    if not entities and not keywords and not args.desc.strip():
        ap.error("supply at least one of --entities / --keywords / --desc")

    try:
        with open(args.topics, encoding="utf-8") as fh:
            ledger = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print("dedupe_check: cannot read %s: %s" % (args.topics, exc), file=sys.stderr)
        return 2

    ref = _parse_date(args.date) if args.date else _dt.date.today()
    excl = _parse_date(args.exclude_date) if args.exclude_date else None
    cand = build_candidate(entities, keywords, args.desc)
    if not cand["tokens"]:
        ap.error("candidate has no distinctive tokens after stopword removal")

    results = run(cand, ledger.get("entries", []), ref, args.window, excl)
    likely = [r for r in results if r["verdict"] == "LIKELY DUPLICATE"]

    if args.json:
        print(json.dumps({"reference_date": ref.isoformat(), "window_days": args.window,
                          "candidate_tokens": sorted(cand["tokens"]),
                          "matches": results}, indent=2))
        return 1 if likely else 0

    print("dedupe_check: candidate vs ledger/topics.json, window %d days ending %s"
          % (args.window, ref.isoformat()))
    print("candidate fingerprint: %s" % ", ".join(sorted(cand["tokens"])))
    if not results:
        print("  no overlap with any in-window entry. CLEAR to proceed (still confirm by eye).")
        return 0
    for r in results:
        print("\n  [%s] No.%s %s (%s)" % (r["verdict"], r["carousel_no"], r["run_date"], r["headline"]))
        print("    topic: %s" % r["topic"][:140])
        if r["entity_hits"]:
            print("    shared entities: %s" % ", ".join(r["entity_hits"]))
        if r["keyword_overlap"]:
            print("    shared keywords: %s" % ", ".join(r["keyword_overlap"]))
        print("    token jaccard: %s" % r["jaccard"])
    if likely:
        print("\n  >> %d LIKELY DUPLICATE match(es). READ each in full before the directors "
              "room; within 90 days pick a different story or reframe as a material UPDATE." % len(likely))
        return 1
    print("\n  soft overlaps only; confirm by eye that the angle/entities are genuinely distinct.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
