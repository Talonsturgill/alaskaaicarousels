#!/usr/bin/env python3
"""
Retention for runs/. Deletes review scratch, never content.

The disk problem in this repo was never age, it was format: 96 percent of
610 MB was uncompressed slide PNGs, fixed by ship_images.py. What is left to
reclaim is small and genuinely disposable, so this is deliberately narrow.

KEPT FOREVER, because the public site serves it or the record depends on it:
    slide-NN.webp   the deck, served on every archive page
    og.jpg          the social card
    carousel.pdf    the LinkedIn upload, linked from the deck page
    claims.json     the verification record, published at /sources/
    copy.json       the article body is rebuilt from this every build
    caption.txt     the story text on the page
    score_report.json, run_state.json, plan.md, assemble_report.json

DELETED after --days (default 30), because it is review apparatus that has
already done its job and nothing public reads:
    contact_sheet.webp   the pixel-critic's contact sheet
    thumbs/              the 432px review thumbs
    storyboard.md        the planning document (can be 75 KB)
    scout_merge.md, selection.md, automation_retro.md
    gmail_payload.json, gmail_draft_id.txt

Everything remains in git history regardless, so this reclaims working tree,
not history. Run with --dry-run first; it is the default posture here.

Usage:
    python scripts/prune_runs.py --dry-run
    python scripts/prune_runs.py --days 30 --apply
"""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUNS = REPO / "runs"

SCRATCH_FILES = (
    "contact_sheet.webp", "contact_sheet.png",
    "storyboard.md", "scout_merge.md", "selection.md", "automation_retro.md",
    "gmail_payload.json", "gmail_draft_id.txt", "caption_report.json",
    "machine_qa.json",
)
SCRATCH_DIRS = ("thumbs",)

# Named so a future reader does not have to infer the rule from the code.
NEVER = ("carousel.pdf", "claims.json", "copy.json", "caption.txt",
         "score_report.json", "run_state.json", "plan.md",
         "assemble_report.json", "og.jpg")


def prune(run: Path, apply: bool) -> tuple[int, list[str]]:
    freed, gone = 0, []
    for name in SCRATCH_FILES:
        f = run / name
        if f.exists() and f.is_file():
            freed += f.stat().st_size
            gone.append(name)
            if apply:
                f.unlink()
    for name in SCRATCH_DIRS:
        d = run / name
        if d.is_dir():
            size = sum(p.stat().st_size for p in d.rglob("*") if p.is_file())
            freed += size
            gone.append(f"{name}/")
            if apply:
                shutil.rmtree(d)
    return freed, gone


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=30,
                    help="keep scratch for runs newer than this (default 30)")
    ap.add_argument("--apply", action="store_true",
                    help="actually delete. Without it, nothing is written.")
    ap.add_argument("--dry-run", action="store_true", help="explicit no-op, the default")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    cutoff = date.today() - timedelta(days=args.days)
    print(f"prune_runs: scratch older than {cutoff.isoformat()} "
          f"({args.days} days){'' if apply else ', DRY RUN'}\n")

    total, touched = 0, 0
    for run in sorted(d for d in RUNS.iterdir() if d.is_dir()):
        try:
            when = date.fromisoformat(run.name)
        except ValueError:
            continue
        if when > cutoff:
            continue
        freed, gone = prune(run, apply)
        if not gone:
            continue
        touched += 1
        total += freed
        print(f"  {run.name}  {freed / 1048576:6.2f}M  {', '.join(gone)}")

    if not touched:
        print("  nothing old enough to prune")
    else:
        print(f"\n{'freed' if apply else 'would free'} {total / 1048576:.2f}M "
              f"across {touched} run(s)")
    kept = sum(p.stat().st_size for p in RUNS.rglob("*") if p.is_file())
    print(f"runs/ is {kept / 1048576:.0f}M")
    if not apply:
        print("\nDry run. Re-run with --apply to delete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
