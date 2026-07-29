#!/usr/bin/env python3
"""
Ship-weight image encoder for runs/<date>/.

The render engine screenshots every slide at 2x (2160x2700) into lossless PNG,
which is right for the pixel-critic review loop and wrong for everything after
it. Those PNGs averaged 4 MB each, nine per deck, and the public site serves
them straight off raw.githubusercontent.com. That was ~34 MB per run in git and
a ~40 MB archive page for a reader on a phone in Bethel.

This converts the shipped copies to WebP at full 2x resolution. Measured on
runs/2026-07-26: 36.42 MB of slide PNGs became 4.09 MB of WebP, 8.9x smaller,
at PSNR 42 to 44 dB across the deck. Above 40 dB is the visually lossless
threshold, and the slides are displayed at a fraction of their native width,
so the encode is invisible and the page stops being a download.

Social scrapers are the exception. LinkedIn, Slack and Facebook still treat
WebP og:image inconsistently, so slide 1 also ships as og.jpg and every
og:image and schema.org image points at that, never at the WebP.

Usage:
    python scripts/ship_images.py --run 2026-07-28      # one run
    python scripts/ship_images.py --all                 # backfill every run
    python scripts/ship_images.py --all --dry-run       # report, change nothing

Exit 0 on success, 1 if any run failed to convert.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("Pillow is required: pip install Pillow")

REPO = Path(__file__).resolve().parents[1]
RUNS = REPO / "runs"

# q92 measured at PSNR 42-44 dB on real 2x decks, which is where nearly every
# full-size slide lands. It is a starting point, not a promise: the encoder
# measures what it produced and escalates until the file clears the floor.
#
# It has to work that way because the decks are not one kind of picture. A flat
# graphic with big type sails through q92; a slide that is mostly generative
# noise or a 5x-downscaled thumb carries high-frequency detail in every pixel
# and needs more. Escalating per file beats one global quality that is either
# too lossy for the hard slides or wasteful for the easy ones.
WEBP_LADDER = (92, 96, 98)   # then lossless
WEBP_METHOD = 6              # slowest, smallest. ~1.2s per 2x slide, once per run.
OG_QUALITY = 88              # og.jpg, read by scrapers at card size
PSNR_FLOOR = 40.0            # visually lossless

# Only these get converted. Everything else in a run is text or already small.
SLIDE_GLOB = "slide-*.png"
EXTRAS = ("contact_sheet.png",)


def psnr(a: Image.Image, b: Image.Image) -> float:
    """Peak signal-to-noise ratio between two RGB images, in dB."""
    hist = ImageChops.difference(a.convert("RGB"), b.convert("RGB")).histogram()
    mse = n = 0
    for ch in range(3):
        for value, count in enumerate(hist[ch * 256:(ch + 1) * 256]):
            mse += count * value * value
            n += count
    if not n:
        return 100.0
    mse /= n
    return 100.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)


def encode(src: Path, dst: Path, verify: bool) -> tuple[int, int, float, str]:
    """PNG -> WebP at native resolution, escalating quality until the result
    clears PSNR_FLOOR. Returns (before, after, psnr_db, how).

    Without --verify there is nothing to escalate against, so it takes the
    first rung and reports no measurement."""
    im = Image.open(src).convert("RGB")
    before = src.stat().st_size

    if not verify:
        im.save(dst, "WEBP", quality=WEBP_LADDER[0], method=WEBP_METHOD)
        return before, dst.stat().st_size, float("nan"), f"q{WEBP_LADDER[0]}"

    for q in WEBP_LADDER:
        im.save(dst, "WEBP", quality=q, method=WEBP_METHOD)
        db = psnr(im, Image.open(dst))
        if db >= PSNR_FLOOR:
            return before, dst.stat().st_size, db, f"q{q}"

    # Nothing lossy cleared the floor. Lossless WebP still beats PNG on these,
    # and correctness of the shipped pixel outranks the last few hundred KB.
    im.save(dst, "WEBP", lossless=True, quality=100, method=WEBP_METHOD)
    return before, dst.stat().st_size, 100.0, "lossless"


def convert_run(run: Path, dry: bool, keep_png: bool, verify: bool) -> dict:
    """Convert one runs/<date>/ in place. Idempotent: a run whose PNGs are
    already gone reports zero work rather than failing."""
    slides = sorted(run.glob(SLIDE_GLOB))
    thumbs = sorted((run / "thumbs").glob("*.png")) if (run / "thumbs").is_dir() else []
    extras = [run / name for name in EXTRAS if (run / name).exists()]
    todo = slides + thumbs + extras

    result = {"run": run.name, "files": 0, "before": 0, "after": 0,
              "worst_psnr": float("inf"), "og": False, "errors": [], "escalated": 0}
    # Nothing to convert AND the og.jpg already exists means genuinely no work.
    # But an already-converted run whose og.jpg is missing still has the one
    # repair below to do, and returning here skipped it, so the "repairs a
    # missing og.jpg on re-run" the block below advertises never actually ran.
    if not todo and (run / "og.jpg").exists():
        return result

    for src in todo:
        dst = src.with_suffix(".webp")
        try:
            if dry:
                # "after" stays 0: nothing was encoded, so any number here
                # would be invented. The report prints a dash for it.
                result["before"] += src.stat().st_size
                result["files"] += 1
                continue
            before, after, db, how = encode(src, dst, verify)
            result["before"] += before
            result["after"] += after
            result["files"] += 1
            if verify and db < result["worst_psnr"]:
                result["worst_psnr"] = db
            if how != f"q{WEBP_LADDER[0]}":
                result["escalated"] += 1
            if after >= before:
                result["errors"].append(
                    f"{src.name} got bigger as webp ({mb(before)} -> {mb(after)})")
            if not keep_png:
                src.unlink()
        except Exception as exc:                       # noqa: BLE001
            result["errors"].append(f"{src.name}: {exc}")

    # og.jpg: the one raster the social scrapers and schema.org consumers read.
    # Built from slide 1 whether or not it has already been converted, so a
    # re-run of an already-converted run still repairs a missing og.jpg.
    cover_png, cover_webp = run / "slide-01.png", run / "slide-01.webp"
    cover = cover_png if cover_png.exists() else (cover_webp if cover_webp.exists() else None)
    if cover and not dry:
        try:
            im = Image.open(cover).convert("RGB").resize((1080, 1350), Image.LANCZOS)
            im.save(run / "og.jpg", "JPEG", quality=OG_QUALITY, optimize=True,
                    progressive=True, subsampling=0)
            result["og"] = True
        except Exception as exc:                       # noqa: BLE001
            result["errors"].append(f"og.jpg: {exc}")
    elif cover and dry:
        result["og"] = True

    return result


def mb(n: float) -> str:
    return f"{n / 1048576:.2f}M"


def drop_pngs(run: Path, dry: bool) -> dict:
    """Reclaim the PNG originals in one run, but only where a WebP sibling
    already exists AND decodes at the same dimensions.

    Encoding and reclaiming are deliberately separate steps. Deleting the only
    raster master of a shipped deck on the strength of a filename would be a
    bad trade, so this re-opens both files and compares them before unlinking
    anything. A PNG whose WebP is missing, truncated or the wrong size is left
    exactly where it is and reported."""
    freed = kept = 0
    skipped = []
    for png in sorted(list(run.glob("*.png")) + list((run / "thumbs").glob("*.png"))):
        webp = png.with_suffix(".webp")
        if not webp.exists():
            skipped.append(f"{png.name}: no webp")
            kept += png.stat().st_size
            continue
        try:
            with Image.open(png) as a, Image.open(webp) as b:
                if a.size != b.size:
                    skipped.append(f"{png.name}: size {a.size} vs webp {b.size}")
                    kept += png.stat().st_size
                    continue
                b.load()          # force a full decode; catches truncation
        except Exception as exc:  # noqa: BLE001
            skipped.append(f"{png.name}: {exc}")
            kept += png.stat().st_size
            continue
        freed += png.stat().st_size
        if not dry:
            png.unlink()
    return {"run": run.name, "freed": freed, "kept": kept, "skipped": skipped}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", help="a single run date, e.g. 2026-07-28")
    g.add_argument("--all", action="store_true", help="backfill every run")
    ap.add_argument("--dry-run", action="store_true", help="report, change nothing")
    ap.add_argument("--keep-png", action="store_true",
                    help="write the webp but leave the png in place")
    ap.add_argument("--verify", action="store_true", default=True,
                    help="compute PSNR per file and escalate below the floor (default on)")
    ap.add_argument("--no-verify", dest="verify", action="store_false")
    ap.add_argument("--drop-png", action="store_true",
                    help="reclaim PNG originals that already have a verified WebP sibling, "
                         "instead of encoding")
    args = ap.parse_args()

    if args.all:
        runs = sorted(d for d in RUNS.iterdir() if d.is_dir())
    else:
        one = RUNS / args.run
        if not one.is_dir():
            print(f"FAIL no such run: runs/{args.run}", file=sys.stderr)
            return 1
        runs = [one]

    if args.drop_png:
        print(f"ship_images --drop-png: {len(runs)} run(s)"
              f"{', DRY RUN' if args.dry_run else ''}\n")
        print(f"{'run':14s} {'reclaimed':>10s} {'kept':>10s}")
        freed = kept = 0
        problems = []
        for run in runs:
            d = drop_pngs(run, args.dry_run)
            freed += d["freed"]
            kept += d["kept"]
            problems += [f"{d['run']}/{s}" for s in d["skipped"]]
            if d["freed"] or d["kept"]:
                print(f"{d['run']:14s} {mb(d['freed']):>10s} {mb(d['kept']):>10s}")
        print(f"\n{'TOTAL':14s} {mb(freed):>10s} {mb(kept):>10s}")
        for p in problems:
            print(f"  kept, unverified: {p}", file=sys.stderr)
        print("\nOK")
        return 0

    tag = ("DRY RUN, nothing written" if args.dry_run
           else f"WebP q{WEBP_LADDER[0]} floor {PSNR_FLOOR} dB")
    print(f"ship_images: {len(runs)} run(s), {tag}\n")
    print(f"{'run':14s} {'files':>5s} {'before':>9s} {'after':>9s} {'shrink':>7s} "
          f"{'min dB':>7s} {'esc':>4s}")

    tb = ta = 0
    failed = []
    for run in runs:
        r = convert_run(run, args.dry_run, args.keep_png, args.verify)
        if not r["files"]:
            print(f"{r['run']:14s} {'-':>5s} {'already converted':>27s}")
            continue
        tb += r["before"]
        ta += r["after"]
        ratio = r["before"] / r["after"] if r["after"] else 0
        worst = r["worst_psnr"]
        db_s = f"{worst:.1f}" if worst != float("inf") else "-"
        shrink = f"{ratio:.1f}x" if not args.dry_run else "-"
        print(f"{r['run']:14s} {r['files']:5d} {mb(r['before']):>9s} "
              f"{mb(r['after']) if not args.dry_run else '-':>9s} {shrink:>7s} {db_s:>7s} "
              f"{r['escalated'] or '':>4}")
        for e in r["errors"]:
            print(f"  ! {e}", file=sys.stderr)
            failed.append(f"{r['run']}/{e}")

    if ta and not args.dry_run:
        print(f"\n{'TOTAL':14s} {'':5s} {mb(tb):>9s} {mb(ta):>9s} "
              f"{tb / ta:6.1f}x   saved {mb(tb - ta)}")
    elif args.dry_run:
        print(f"\n{'TOTAL':14s} {'':5s} {mb(tb):>9s}  (would convert)")

    if failed:
        print(f"\nFAIL {len(failed)} file(s) did not convert cleanly", file=sys.stderr)
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
