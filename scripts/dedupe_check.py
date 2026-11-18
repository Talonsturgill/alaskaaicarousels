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
    30-day hard-fail rule is still the showrunner's call. Pure stdlib, offline.

THE EARLIER TIER (2026-11-17, weekly machine pass; queue items 2026-10-24 and
2026-11-17). ledger/topics.json's own _spec binds a 90-day repeat rule and a
120-day matching scan, and this tool searched only the routine's 30 days, so a
same-story repeat at 31 to 90 days passed with no signal, twice: No.95 missed
No.64 (34 days, the KPB weather-modification ordinance; the scorer caught it
at Phase 10 after the art was built) and No.117 missed No.77 (44 days, the
Bristol Bay tower counts; found by reading the technique library, and the
deck was reframed as an UPDATE mid directors room). So every run now also
prints entries from day 31 to day 120 (--earlier-window, the _spec's matching
scan) in their own section, each tagged by band. A LIKELY DUPLICATE inside the
_spec's 90 days also exits 1 (stop and read; frame it as an UPDATE with the
material new development named, or pick another story). One at 91 to 120 days
is printed for context and does not change the exit code. --scout-brief adds
the same 31 to 120 days as a compact block (headline and the first five
entities, about 15 KB more on 2026-11-17's ledger: 20.8 to 35.8 KB).

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

# ledger/topics.json _spec: "No topic may repeat within 90 days" and "compare
# ... every entry from the last 120 days". tests/dedupe_earlier_verify.py fails
# if the _spec's wording moves away from these two numbers.
SPEC_REPEAT_DAYS = 90
SPEC_MATCH_DAYS = 120

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

    shared = cand["tokens"] & entry_tokens
    union = cand["tokens"] | entry_tokens
    jaccard = (len(shared) / len(union)) if union else 0.0

    # Containment, not just Jaccard. A candidate is much smaller than a full
    # ledger entry's blob (a handful of entities and keywords against every
    # field of a past run), so even a candidate whose every token appears in
    # the entry topped out around Jaccard 0.37 and the 0.30 LIKELY DUPLICATE
    # trigger was mathematically unreachable: a word-for-word repeat of
    # yesterday's deck scored SOFT OVERLAP and exit 0. Containment measures how
    # much of the SMALLER set is in the larger, so a repeat scores near 1.0.
    #
    # Calibrated on the real ledger: a genuine repeat (candidate rebuilt from a
    # past entry) scores containment 1.0, while the highest any DIFFERENT story
    # reaches for a substantial candidate is 0.49, so 0.50 separates cleanly.
    # The shared-token floors keep a tiny two-token candidate that happens to
    # sit inside a big entry from tripping on coincidence.
    denom = min(len(cand["tokens"]), len(entry_tokens)) or 1
    containment = len(shared) / denom

    if (len(entity_hits) >= 2 or jaccard >= 0.30
            or (len(shared) >= 5 and containment >= 0.50)):
        verdict = "LIKELY DUPLICATE"
    elif (entity_hits or keyword_overlap or jaccard >= 0.12
            or (len(shared) >= 4 and containment >= 0.30)):
        verdict = "SOFT OVERLAP"
    else:
        verdict = "clear"

    return {
        "verdict": verdict,
        "entity_hits": entity_hits,
        "keyword_overlap": keyword_overlap,
        "jaccard": round(jaccard, 3),
        "containment": round(containment, 3),
    }


def run(cand, entries, ref_date, window, exclude_date, newer_than=0):
    """Entries from `window` days back to `newer_than` days back (exclusive of
    newer_than, so the earlier tier starts the day after the main window)."""
    lo = ref_date - _dt.timedelta(days=window)
    hi = ref_date - _dt.timedelta(days=newer_than + 1) if newer_than else ref_date
    results = []
    for e in entries:
        rd_raw = e.get("run_date")
        if not rd_raw:
            continue
        try:
            rd = _parse_date(rd_raw)
        except ValueError:
            continue
        if rd < lo or rd > hi:
            continue
        if exclude_date and rd == exclude_date:
            continue
        s = score_entry(cand, e)
        if s["verdict"] == "clear":
            continue
        s.update(run_date=rd_raw, carousel_no=e.get("carousel_no"),
                 topic=e.get("topic", ""), headline=e.get("headline", ""),
                 date_distance=(ref_date - rd).days)
        results.append(s)
    order = {"LIKELY DUPLICATE": 0, "SOFT OVERLAP": 1}
    results.sort(key=lambda r: (order[r["verdict"]], -len(r["entity_hits"]), -r["jaccard"]))
    return results


def scout_brief(args):
    """The ALREADY COVERED block every scout brief carries, from the full ledger
    fields. The topic is the one field that is cut (it runs to 1,500 characters);
    entities and keywords, the fields a scout matches a lead against, never are."""
    try:
        with open(args.topics, encoding="utf-8") as fh:
            ledger = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print("dedupe_check: cannot read %s: %s" % (args.topics, exc), file=sys.stderr)
        return 2
    ref = _parse_date(args.date) if args.date else _dt.date.today()
    lo = ref - _dt.timedelta(days=args.window)
    rows = []
    for e in ledger.get("entries", []):
        try:
            rd = _parse_date(e.get("run_date", ""))
        except ValueError:
            continue
        if lo <= rd <= ref:
            rows.append((rd, e))
    rows.sort(key=lambda r: r[0])
    print("ALREADY COVERED in the last %d days to %s (a new URL for the same story is the "
          "same story; only bring one back with a MATERIAL new development since its date, "
          "and say what it is). Match a lead against the ENTITIES and KEYWORDS, which are "
          "complete; the topic line is cut." % (args.window, ref.isoformat()))
    for rd, e in rows:
        topic = " ".join(str(e.get("topic", "")).split())
        if len(topic) > 230:
            topic = topic[:230].rsplit(" ", 1)[0] + " ..."
        print("- %s No.%s: %s" % (rd.isoformat(), e.get("carousel_no", "?"),
                                  e.get("headline") or topic))
        if e.get("headline"):
            print("  topic: %s" % topic)
        for f in ("entities", "keywords"):
            v = e.get(f) or []
            if isinstance(v, list) and v:
                print("  %s: %s" % (f, "; ".join(str(x) for x in v)))
    ew = getattr(args, "earlier_window", 0) or 0
    if ew > args.window:
        elo = ref - _dt.timedelta(days=ew)
        ehi = ref - _dt.timedelta(days=args.window + 1)
        early = sorted(((rd, e) for rd, e in
                        ((_safe_date(e.get("run_date", "")), e) for e in ledger.get("entries", []))
                        if rd and elo <= rd <= ehi), key=lambda r: r[0])
        if early:
            print("")
            print("EARLIER, %d to %d days back (ledger/topics.json binds a %d-day repeat rule: a "
                  "lead on one of these stories inside %d days comes back only as an UPDATE with "
                  "the material new development named). Headline and the first five entities:"
                  % (args.window + 1, ew, SPEC_REPEAT_DAYS, SPEC_REPEAT_DAYS))
            for rd, e in early:
                ents = e.get("entities") or []
                # the first five entities: the ones a ledger writer lists first are the
                # story's own (agency, place, project); the full list is in the ledger
                ents = "; ".join(str(x) for x in ents[:5]) if isinstance(ents, list) else str(ents)
                head = e.get("headline") or " ".join(str(e.get("topic", "")).split())[:160]
                print("- %s No.%s: %s | %s" % (rd.isoformat(), e.get("carousel_no", "?"), head, ents))
    return 0


def _safe_date(s):
    try:
        return _parse_date(s)
    except (ValueError, TypeError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Phase 4 pre-flight dedupe signal.")
    ap.add_argument("--entities", default="", help="comma-separated candidate entities")
    ap.add_argument("--keywords", default="", help="comma-separated candidate keywords")
    ap.add_argument("--desc", default="", help="free-text candidate description")
    ap.add_argument("--topics", default="ledger/topics.json")
    ap.add_argument("--date", default=None, help="reference date YYYY-MM-DD (default today)")
    ap.add_argument("--window", type=int, default=30, help="lookback days (default 30)")
    ap.add_argument("--earlier-window", type=int, default=SPEC_MATCH_DAYS,
                    help="also scan from the day after --window back to this many days, in a "
                         "section of its own (default %d, ledger/topics.json's matching scan; "
                         "0 = off). A LIKELY DUPLICATE inside %d days exits 1"
                         % (SPEC_MATCH_DAYS, SPEC_REPEAT_DAYS))
    ap.add_argument("--exclude-date", default=None,
                    help="skip ledger entries on this run_date (e.g. the candidate's own row)")
    ap.add_argument("--run-dir", default=None,
                    help="derive the fingerprint from the RUN ITSELF (claims.json story, "
                         "copy.json headlines and slide labels) instead of hand-typed "
                         "strings. Added 2026-08-09 after run No.30 answered this gate "
                         "about a candidate it then discarded, and shipped a Phase 4 PASS "
                         "that described a story the run was no longer making. A gate you "
                         "can answer about the wrong question is not a gate.")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--scout-brief", action="store_true",
                    help="print the ALREADY COVERED block for the Phase 2 scout briefs: "
                         "every entry in the window with its headline and its entities "
                         "and keywords IN FULL, and no candidate needed. Added 2026-10-25 "
                         "after run No.96's hand-built list cut each topic at 230 "
                         "characters, lost No.87's Burgum clause, and three of six "
                         "scouts brought back the story No.87 had covered.")
    args = ap.parse_args(argv)
    if args.scout_brief:
        return scout_brief(args)

    def _split(s):
        return [x.strip() for x in s.split(",") if x.strip()]

    entities, keywords = _split(args.entities), _split(args.keywords)
    desc = args.desc
    if args.run_dir:
        import os as _os
        ents, kws, bits = [], [], []
        cj = _os.path.join(args.run_dir, "claims.json")
        yj = _os.path.join(args.run_dir, "copy.json")
        try:
            with open(cj, encoding="utf-8") as fh:
                cd = json.load(fh)
            bits.append(cd.get("story", ""))
            for c in cd.get("claims", []):
                o = (c.get("source_outlet") or "").strip()
                if o and o not in ents:
                    ents.append(o)
        except Exception as exc:
            print("dedupe_check: cannot read %s: %s" % (cj, exc), file=sys.stderr)
            return 2
        try:
            with open(yj, encoding="utf-8") as fh:
                yd = json.load(fh)
            bits.append(yd.get("document_title", ""))
            bits.append(yd.get("deck_summary_line", ""))
            for sl in yd.get("slides", []):
                for k in ("kicker", "headline", "body"):
                    if sl.get(k):
                        bits.append(sl[k])
                for lab in sl.get("labels", []) or []:
                    bits.append(lab)
        except Exception:
            pass
        desc = (desc + " " + " ".join(b for b in bits if b)).strip()
        entities = entities + ents
    if not entities and not keywords and not desc.strip():
        ap.error("supply at least one of --entities / --keywords / --desc")

    try:
        with open(args.topics, encoding="utf-8") as fh:
            ledger = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print("dedupe_check: cannot read %s: %s" % (args.topics, exc), file=sys.stderr)
        return 2

    ref = _parse_date(args.date) if args.date else _dt.date.today()
    excl = _parse_date(args.exclude_date) if args.exclude_date else None
    cand = build_candidate(entities, keywords, desc)
    if not cand["tokens"]:
        ap.error("candidate has no distinctive tokens after stopword removal")

    results = run(cand, ledger.get("entries", []), ref, args.window, excl)
    likely = [r for r in results if r["verdict"] == "LIKELY DUPLICATE"]
    earlier = []
    if args.earlier_window and args.earlier_window > args.window:
        earlier = run(cand, ledger.get("entries", []), ref, args.earlier_window, excl,
                      newer_than=args.window)
        for r in earlier:
            r["band"] = ("inside the %d-day repeat rule" % SPEC_REPEAT_DAYS
                         if r["date_distance"] <= SPEC_REPEAT_DAYS else
                         "%d to %d days, matching scan only" % (SPEC_REPEAT_DAYS + 1, args.earlier_window))
    likely_earlier = [r for r in earlier if r["verdict"] == "LIKELY DUPLICATE"
                      and r["date_distance"] <= SPEC_REPEAT_DAYS]
    code = 1 if (likely or likely_earlier) else 0

    if args.json:
        print(json.dumps({"reference_date": ref.isoformat(), "window_days": args.window,
                          "earlier_window_days": args.earlier_window,
                          "candidate_tokens": sorted(cand["tokens"]),
                          "matches": results, "earlier": earlier}, indent=2))
        return code

    print("dedupe_check: candidate vs ledger/topics.json, window %d days ending %s"
          % (args.window, ref.isoformat()))
    print("candidate fingerprint: %s" % ", ".join(sorted(cand["tokens"])))
    if not results:
        print("  no overlap with any in-window entry.%s" % (
            "" if earlier else " CLEAR to proceed (still confirm by eye)."))
        if earlier:
            _print_earlier(earlier, likely_earlier, args.window, args.earlier_window)
            _print_strongest(earlier)
        return code
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
              "room; within 30 days pick a different story or reframe as a material UPDATE." % len(likely))
    else:
        print("\n  soft overlaps only; confirm by eye that the angle/entities are genuinely distinct.")
    if earlier:
        _print_earlier(earlier, likely_earlier, args.window, args.earlier_window)
    _print_strongest(results + earlier)
    return code


def _print_earlier(earlier, likely_earlier, window, earlier_window):
    print("\n  EARLIER COVERAGE, %d to %d days back (ledger/topics.json _spec: %d-day repeat "
          "rule, %d-day matching scan):" % (window + 1, earlier_window, SPEC_REPEAT_DAYS,
                                            SPEC_MATCH_DAYS))
    for r in earlier:
        print("\n  [%s, %s] No.%s %s, %d days ago (%s)" % (
            r["verdict"], r["band"], r["carousel_no"], r["run_date"], r["date_distance"],
            r["headline"]))
        print("    topic: %s" % r["topic"][:140])
        if r["entity_hits"]:
            print("    shared entities: %s" % ", ".join(r["entity_hits"]))
        if r["keyword_overlap"]:
            print("    shared keywords: %s" % ", ".join(r["keyword_overlap"]))
        print("    token jaccard: %s" % r["jaccard"])
    if likely_earlier:
        print("\n  >> %d LIKELY DUPLICATE match(es) inside %d days. READ each in full; this "
              "deck goes ahead only as an UPDATE that names the material new development since "
              "that run (selection.md and the cover), or pick another story."
              % (len(likely_earlier), SPEC_REPEAT_DAYS))


def _print_strongest(results):
    if not results:
        return
    order = {"LIKELY DUPLICATE": 0, "SOFT OVERLAP": 1}
    # in-window first at the same verdict, then inside the 90 days, then the rest;
    # inside a band the original order (most shared entities, highest jaccard)
    def band(r):
        if "band" not in r:
            return 0
        return 1 if r["date_distance"] <= SPEC_REPEAT_DAYS else 2
    results = sorted(results, key=lambda r: (order[r["verdict"]], band(r),
                                             -len(r["entity_hits"]), -r["jaccard"]))

    # LOUD final summary. results is pre-sorted strongest-first (LIKELY DUPLICATE
    # before SOFT OVERLAP, then most shared named entities, then highest jaccard),
    # so results[0] is the single strongest collision. Printing it as the LAST
    # lines makes it impossible to miss even when this output is read with `tail`
    # (the 2026-07-24 No.16 miss: the strongest match No.1 printed at the TOP and
    # a `tail` of the output truncated it). This restates the existing signal; it
    # never changes a verdict, the exit code, or the per-match list above.
    top = results[0]
    dd = top.get("date_distance")
    when = ("%d days ago" % dd) if isinstance(dd, int) else "date unknown"
    n_ent = len(top["entity_hits"])
    print("\n" + "=" * 74)
    print("  STRONGEST MATCH: No.%s %s (%s) -- %s -- %d shared entit%s, jaccard %s"
          % (top["carousel_no"], top["run_date"], when, top["verdict"],
             n_ent, "y" if n_ent == 1 else "ies", top["jaccard"]))
    print("  >> READ THIS ENTRY IN FULL before the directors room. Do NOT `tail` this output.")
    print("=" * 74)


if __name__ == "__main__":
    sys.exit(main())
