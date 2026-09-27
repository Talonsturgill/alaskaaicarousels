#!/usr/bin/env python3
"""word_ban.py — the words the owner banned never reach a published surface.

    python scripts/word_ban.py --run out/<date>      the caption, copy.json and the docket
    python scripts/word_ban.py --self-test

WHY THIS EXISTS

The owner, 2026-09-27: "on both automations ban the words 'gap' and 'matters' and 'pattern'".
The list is `banned_words` in config/brand.yaml and this file never types a word of it. Each is
matched as a whole word in any case, so "Singapore" is not "gap", and "matter" in "no matter" or
"subject matter" is not "matters". A compound counts, because "wage-gap" still prints the word.

Substring matching, which the banned_phrases gate uses, would not do here: every one of these is
short enough to sit inside another word, and "gap" sits inside Singapore.

WHAT IS EXEMPT, because it is somebody else's words and a quotation is never rewritten: a
passage inside straight double quotes, a URL, and a sentence the run's claims.json carries
inside a claim's `verbatim` text. A source whose own title carries one of the words goes in
straight quotes in the first comment, which is what a title is.

WHERE IT RUNS
  - caption_check.py fails the caption and every reader-facing string in copy.json, slides and
    first comment included, while the caption room and the copywriter write them
  - gate_status.py's `word_ban` row runs `--run` on the run directory, which reads those again
    and the docket: any item updated after SINCE and any history note dated after it

SINCE is 2026-09-27, the last deck and docket update before the rule. The docket's older prose is
not failed, because published copy is not rewritten without the owner. A run that updates an
older item rewords it on the way through.

EXIT CODES: 0 clean, 1 a banned word, 2 nothing to read.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BRAND = REPO / "config" / "brand.yaml"
DOCKET = REPO / "ledger" / "docket.json"
SINCE = "2026-09-27"

QUOTED = re.compile(r'"[^"\n]*"')
URL = re.compile(r"https?://\S+|www\.\S+")
SENTENCE = re.compile(r"[^.!?\n]+[.!?]?")


def words(path=None):
    """The banned words from brand.yaml. Parsed like caption_check's banned_phrases, so the gate
    has no dependency of its own. Raises ValueError when the list is missing or empty."""
    p = Path(path) if path else BRAND
    raw = p.read_text(encoding="utf-8")
    m = re.search(r"(?m)^(\s*)banned_words:\s*$", raw)
    if not m:
        raise ValueError("%s has no banned_words: block, which is where the owner's banned "
                         "words live" % p)
    indent = len(m.group(1))
    out = []
    for line in raw[m.end():].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if len(line) - len(line.lstrip()) <= indent and not line.lstrip().startswith("-"):
            break
        item = re.match(r"\s*-\s*(.+?)\s*$", line)
        if not item:
            break
        out.append(item.group(1).strip().strip('"').strip("'"))
    if not out:
        raise ValueError("%s: banned_words is empty" % p)
    return out


def matcher(banned):
    alternatives = "|".join(re.escape(w) for w in sorted(banned, key=len, reverse=True))
    return re.compile(r"\b(?:%s)\b" % alternatives, re.I)


def _squash(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def hits(text, quotes=(), banned=None):
    """Each banned word in `text` that the house wrote, with the words around it."""
    rx = matcher(banned if banned is not None else words())
    spans = [m.span() for m in QUOTED.finditer(text)] + [m.span() for m in URL.finditer(text)]
    squashed = [_squash(q) for q in quotes if q and q.strip()]
    out = []
    for m in rx.finditer(text):
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            continue
        sentence = next((s.group(0) for s in SENTENCE.finditer(text)
                         if s.start() <= m.start() < s.end()), "")
        if sentence.strip() and any(_squash(sentence).strip(" .!?") in q for q in squashed):
            continue
        around = text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ").strip()
        out.append("%r in \"...%s...\"" % (m.group(0), around))
    return out


def _load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _verbatims(run_dir):
    raw = _load(run_dir / "claims.json")
    rows = raw.get("claims") if isinstance(raw, dict) else raw
    return tuple(str(c.get("verbatim") or "") for c in (rows or []) if isinstance(c, dict))


def check_run(run_dir, banned=None):
    """Every banned word in a run's caption and copy.json reader prose. None with no copy."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import caption_check
    copy = _load(run_dir / "copy.json")
    caption = run_dir / "caption.txt"
    if copy is None and not caption.exists():
        return None
    banned = banned if banned is not None else words()
    quotes = _verbatims(run_dir)
    surfaces = []
    if caption.exists():
        surfaces.append(("caption", caption.read_text(encoding="utf-8")))
    if isinstance(copy, dict):
        surfaces += [("copy.json %s" % path, s) for path, s in caption_check.copy_prose(copy)]
    out = []
    for where, text in surfaces:
        for h in hits(text, quotes, banned):
            out.append("%s: %s. The owner banned it on 2026-09-27 (config/brand.yaml "
                       "banned_words). Say the specific thing instead" % (where, h))
    return out


def check_docket(items, banned=None):
    """The docket prose a run writes after SINCE: an item updated after it, a note dated after it."""
    banned = banned if banned is not None else words()
    out = []
    for it in items:
        who = it.get("id", "?")
        texts = []
        if str(it.get("last_updated") or "") > SINCE:
            texts += [(f, str(it.get(f) or "")) for f in ("title", "summary", "access_note")]
            texts += [("date label %s" % k.get("date", "?"), str(k.get("label") or ""))
                      for k in (it.get("key_dates") or []) if isinstance(k, dict)]
        texts += [("history %s" % h.get("date"), str(h.get("note") or ""))
                  for h in (it.get("history") or [])
                  if isinstance(h, dict) and str(h.get("date") or "") > SINCE]
        for where, text in texts:
            for h in hits(text, (), banned):
                out.append("docket %s %s: %s. The owner banned it on 2026-09-27 "
                           "(config/brand.yaml banned_words). Say the specific thing instead"
                           % (who, where, h))
    return out


def self_test():
    failures = 0

    def ok(name, cond, detail=""):
        nonlocal failures
        print(("ok    " if cond else "FAIL  ") + name + ("" if cond else "  " + str(detail)))
        failures += 0 if cond else 1

    banned = words()
    ok("the list is brand.yaml's, and it carries the three words the owner named",
       {"gap", "matters", "pattern"} <= {w.lower() for w in banned}, banned)
    for text in ("The gap between the two filings is nine days.", "Why it matters for Homer.",
                 "A pattern of late filings.", "Two GAPS in the record.", "PATTERNS repeat.",
                 "The wage-gap figure."):
        ok("caught: " + text, len(hits(text, (), banned)) == 1, hits(text, (), banned))
    for text in ("Singapore filed first.", "No matter what the assembly decides.",
                 "The subject matter of the hearing.", 'The report says "the gap is widening".',
                 "https://example.com/the-gap/", "The patterned glass facade."):
        ok("kept: " + text, not hits(text, (), banned), hits(text, (), banned))
    verbatim = "Staff identified a pattern of incomplete applications in the second quarter."
    ok("a sentence a claim quotes verbatim is the source's sentence",
       not hits("Staff identified a pattern of incomplete applications.", (verbatim,), banned))

    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        (d / "claims.json").write_text(json.dumps({"claims": [{"id": "c1", "verbatim": verbatim}]}))
        (d / "caption.txt").write_text("The assembly voted. Here is why it matters.\n")
        (d / "copy.json").write_text(json.dumps({
            "document_title": "Homer, nine days", "post_copy": "", "deck_summary_line": "",
            "first_comment": "Sources\nKBBI, the vote, https://example.com/gap",
            "slides": [{"n": 1, "headline": "Four filings, one pattern"}]}))
        found = check_run(d, banned)
        ok("a run's caption and slide are each caught",
           len(found) == 2 and found[0].startswith("caption")
           and any("headline" in f for f in found), found)
        ok("...and a URL in the first comment is not", not any("first_comment" in f for f in found))

    items = [{"id": "after", "last_updated": "2026-09-28", "title": "t",
              "summary": "The assembly will take up utility matters.", "access_note": "",
              "key_dates": [], "history": []},
             {"id": "before", "last_updated": "2026-09-27", "title": "t",
              "summary": "The assembly will take up utility matters.", "access_note": "",
              "key_dates": [], "history": [{"date": "2026-09-28", "note": "The gap closed."}]}]
    found = check_docket(items, banned)
    ok("a docket item updated after the rule is judged, and one before it is not",
       any(f.startswith("docket after summary") for f in found)
       and not any("before summary" in f for f in found), found)
    ok("...and a history note dated after the rule is judged whatever the item",
       any(f.startswith("docket before history 2026-09-28") for f in found), found)

    print("\nword_ban self-test: %s" % ("all passed" if not failures else "%d FAILED" % failures))
    return 1 if failures else 0


def main():
    args = sys.argv[1:]
    if args == ["--self-test"]:
        return self_test()
    if len(args) != 2 or args[0] != "--run":
        print("usage: word_ban.py --run <run dir> | --self-test", file=sys.stderr)
        return 2
    run_dir = Path(args[1])
    found = check_run(run_dir)
    if found is None:
        print("word_ban: no caption.txt or copy.json in %s" % run_dir, file=sys.stderr)
        return 2
    docket = _load(DOCKET)
    items = (docket.get("items") if isinstance(docket, dict) else docket) or []
    found += check_docket(items)
    for f in found:
        print("word_ban: " + f)
    print("word_ban: %d banned word(s) in %s and the docket" % (len(found), run_dir))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
