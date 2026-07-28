#!/usr/bin/env python3
"""
Gate on claims.json before a deck is built from it.

Why this exists: the fact-checker is an agent, and for eighteen runs nothing
checked what it returned. It drifted. Across the back catalogue the claim
container has been named claims, verified_claims, docket_claims, and twice the
story's codename. The same field has been claim, text or statement, and
source_url, url or evidence_url. One run nested url, outlet and date inside an
evidence object. Four runs recorded no per-slide copy at all.

None of that was visible, because nothing downstream read the file closely
enough to complain. The site published anyway and the verification record
silently rendered empty on 14 of 18 decks.

This runs right after Phase 3 and says plainly whether the file the deck is
about to be built from can carry a page. It is deliberately strict about the
handful of fields the public site depends on and quiet about everything else,
so the fact-checker keeps its freedom to record more than the minimum.

Usage:
    python scripts/claims_check.py --date 2026-07-28
    python scripts/claims_check.py --file out/2026-07-28/claims.json
    python scripts/claims_check.py --all          # audit the back catalogue

Exit 0 clean, 1 on a hard failure, 2 if the file cannot be read at all.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import site_build as sb  # noqa: E402  the tolerant reader the site actually uses

# What a deck page needs to render a verification record worth publishing.
MIN_CLAIMS = 3
MIN_SOURCED_RATIO = 0.80     # of claims that survive, this share must carry a URL
MIN_PRIMARY = 1              # at least one primary document, or say why not

CANON = """Pin claims.json to this shape. Extra fields are welcome; these are read:

{
  "run_date": "YYYY-MM-DD",
  "story": "one line naming the story these claims belong to",
  "claims": [{
    "id": "C01",
    "claim": "one atomic factual sentence, no colon, no em dash",
    "value": "the number or date the claim turns on, e.g. 1,566 customers",
    "verbatim": "the exact string on the page that proves it",
    "source_url": "https://...",
    "source_outlet": "who published it",
    "source_is_primary": true,
    "date_of_source": "YYYY-MM-DD",
    "fetched": true,
    "confidence": 0.97
  }],
  "killed": [{"claim": "...", "why": "..."}]
}

source_url, source_outlet and source_is_primary are what the public source
archive and the per-deck verification record are built from. A claim with no
source_url is dropped from the page, because that section IS the sourcing."""


def check(path: Path) -> tuple[int, list[str], list[str], dict]:
    """Returns (exit_code, failures, warnings, stats)."""
    try:
        doc = json.loads(path.read_text())
    except Exception as exc:                                       # noqa: BLE001
        return 2, [f"cannot read {path}: {exc}"], [], {}

    claims = sb.normalize_claims(doc)
    raw = sb._claim_rows(doc)
    fails, warns = [], []

    stats = {
        "raw": len(raw),
        "usable": len(claims),
        "primary": sum(1 for c in claims.values() if c["source_is_primary"]),
        "with_outlet": sum(1 for c in claims.values() if c["source_outlet"]),
        "with_date": sum(1 for c in claims.values() if c["date_of_source"]),
    }

    if not raw:
        fails.append("no claim list found. Name the array \"claims\".")
        return 1, fails, warns, stats

    if stats["usable"] < MIN_CLAIMS:
        fails.append(f"only {stats['usable']} claims carry both a statement and a "
                     f"source_url, need at least {MIN_CLAIMS}")

    if stats["raw"]:
        ratio = stats["usable"] / stats["raw"]
        if ratio < MIN_SOURCED_RATIO:
            fails.append(f"{stats['raw'] - stats['usable']} of {stats['raw']} claims "
                         f"have no usable source_url ({ratio:.0%} sourced, "
                         f"need {MIN_SOURCED_RATIO:.0%}). They will not render.")

    if stats["usable"] and stats["primary"] < MIN_PRIMARY:
        fails.append("no claim is marked source_is_primary. This publication's whole "
                     "argument is that it reads the filing, so either set the flag or "
                     "go find the primary document.")

    # Warnings: the page still builds, but it reads worse.
    if stats["usable"] and stats["with_outlet"] < stats["usable"]:
        warns.append(f"{stats['usable'] - stats['with_outlet']} claims have no "
                     f"source_outlet and will show as \"Uncredited source\"")
    if stats["usable"] and stats["with_date"] < stats["usable"]:
        warns.append(f"{stats['usable'] - stats['with_date']} claims have no "
                     f"date_of_source")

    # The shape the site reads natively, so drift gets named the day it happens
    # rather than being discovered eighteen runs later.
    if not isinstance(doc.get("claims"), list):
        found = next((k for k in doc if isinstance(doc.get(k), list)
                      and doc[k] and isinstance(doc[k][0], dict)), "?")
        warns.append(f"claim array is named {found!r}, not \"claims\". It was read, "
                     f"but pin it to \"claims\".")
    sample = (doc.get("claims") or raw)[0]
    for want, alts in (("claim", ("text", "statement")),
                       ("source_url", ("url", "evidence_url")),
                       ("source_outlet", ("outlet", "publisher")),
                       ("source_is_primary", ("primary", "credibility", "tier"))):
        if want not in sample:
            used = next((a for a in alts if a in sample), None)
            if used:
                warns.append(f"field {used!r} was read as {want!r}; pin it to {want!r}")
            elif want in ("claim", "source_url"):
                warns.append(f"no {want!r} field found on the first claim")

    return (1 if fails else 0), fails, warns, stats


def report(label: str, code: int, fails, warns, stats) -> None:
    verdict = {0: "PASS", 1: "FAIL", 2: "UNREADABLE"}[code]
    print(f"[{verdict}] {label}  {stats.get('usable', 0)}/{stats.get('raw', 0)} usable, "
          f"{stats.get('primary', 0)} primary, {stats.get('with_outlet', 0)} with outlet")
    for f in fails:
        print(f"    FAIL  {f}")
    for w in warns:
        print(f"    warn  {w}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--date", help="checks out/<date>/claims.json then runs/<date>/")
    g.add_argument("--file", help="an explicit path")
    g.add_argument("--all", action="store_true", help="audit every run in runs/")
    ap.add_argument("--schema", action="store_true", help="print the pinned schema")
    args = ap.parse_args()

    if args.schema:
        print(CANON)
        return 0

    if args.all:
        worst = 0
        for d in sorted((REPO / "runs").iterdir()):
            f = d / "claims.json"
            if f.exists():
                code, fails, warns, stats = check(f)
                report(d.name, code, fails, [], stats)
                worst = max(worst, code)
        print("\nBack-catalogue audit only. A nonzero result here does not block a "
              "ship; it names what the tolerant reader is having to paper over.")
        return 0

    if args.file:
        path = Path(args.file)
    else:
        path = REPO / "out" / args.date / "claims.json"
        if not path.exists():
            path = REPO / "runs" / args.date / "claims.json"

    code, fails, warns, stats = check(path)
    report(str(path.relative_to(REPO) if path.is_relative_to(REPO) else path),
           code, fails, warns, stats)
    if code:
        print()
        print(CANON)
    return code


if __name__ == "__main__":
    sys.exit(main())
