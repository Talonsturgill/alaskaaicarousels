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
    python scripts/ship_images.py --run 2026-10-03 --drop-canvas-layers

Exit 0 on success, 1 if any run failed to convert or holds a file that is not
a frame (see STRAYS below).
"""
from __future__ import annotations

import argparse
import math
import re
import subprocess
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

# STRAYS: A FRAME IS slide-NN AND NOTHING ELSE (2026-10-03, No.76).
# render.py writes slide-NN.canvas.png beside every render (the art layer alone,
# for qa.py's canvas checks, since 2026-08-30). It is a diagnostic, not a frame.
# No.76 copied render/slide-*.png into runs/<date>/, SLIDE_GLOB matched the nine
# canvas layers too, this script converted them to slide-NN.canvas.webp, and
# nothing complained about eighteen slide files in a shipped run; run_guard's
# slide-*.webp census would have counted them. assemble.py and gmail_draft.py
# had each been taught the difference separately. This is the place they all
# pass through on the way to main, so it refuses here: any slide-* image whose
# name is not slide-NN.png / slide-NN.webp is never converted and fails the run
# with its remedy. --drop-canvas-layers removes exactly the canvas layers,
# untracked only, so no run has to improvise a delete under runs/.
FRAME_RE = re.compile(r"^slide-\d{2}\.(png|webp)$")
CANVAS_LAYER_RE = re.compile(r"^slide-\d{2}\.canvas\.(png|webp)$")
RUN_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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
    slides = sorted(p for p in run.glob(SLIDE_GLOB) if FRAME_RE.match(p.name))
    thumbs = sorted((run / "thumbs").glob("*.png")) if (run / "thumbs").is_dir() else []
    extras = [run / name for name in EXTRAS if (run / name).exists()]
    todo = slides + thumbs + extras

    result = {"run": run.name, "files": 0, "before": 0, "after": 0,
              "worst_psnr": float("inf"), "og": False, "errors": [], "escalated": 0}
    found = strays(run)
    if found:
        result["errors"].append(stray_message(run, found))
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


def strays(run: Path) -> list[Path]:
    """slide-* images in a run that are not frames. Never converted, never
    shipped: a canvas layer, a stray copy, anything with an extra suffix."""
    return sorted(p for p in run.glob("slide-*")
                  if p.is_file() and p.suffix.lower() in (".png", ".webp")
                  and not FRAME_RE.match(p.name))


def stray_message(run: Path, found: list[Path]) -> str:
    canvas = [p for p in found if CANVAS_LAYER_RE.match(p.name)]
    msg = (f"{len(found)} non-frame slide file(s) in runs/{run.name}: "
           f"{', '.join(p.name for p in found[:6])}{' ...' if len(found) > 6 else ''}. "
           "A frame is slide-NN.png; copy render/slide-NN.png only, never the "
           "slide-NN.canvas.png layers render.py writes beside them.")
    if canvas:
        msg += (f" Remove the canvas layers with: python scripts/ship_images.py "
                f"--run {run.name} --drop-canvas-layers")
    return msg


def git_tracked(run: Path) -> set[str] | None:
    """Names git tracks directly in this run directory, or None if git can't
    say, in which case the caller refuses rather than guesses."""
    try:
        p = subprocess.run(["git", "ls-files", "-z", "--", "."], cwd=run,
                           capture_output=True, text=True, timeout=30)
    except Exception:                                   # noqa: BLE001
        return None
    if p.returncode != 0:
        return None
    return {n for n in p.stdout.split("\0") if n and "/" not in n}


def drop_canvas_layers(run: Path, dry: bool) -> tuple[int, list[str]]:
    """Delete runs/<date>/slide-NN.canvas.{png,webp} and nothing else.

    Guards, each a refusal and never a skip-and-continue: the directory must be
    a dated run, git must be able to list what it tracks there, and NO canvas
    layer may already be tracked (a committed file under runs/ is a shipped
    artifact and is not this script's to delete). Other non-frame names are
    reported and left alone. Returns (removed, problems)."""
    if not RUN_DIR_RE.match(run.name):
        return 0, [f"refusing: {run} is not a dated run directory"]
    layers = sorted(p for p in run.iterdir()
                    if p.is_file() and CANVAS_LAYER_RE.match(p.name))
    if not layers:
        return 0, []
    tracked = git_tracked(run)
    if tracked is None:
        return 0, [f"refusing: git can't list tracked files in {run}"]
    shipped = [p.name for p in layers if p.name in tracked]
    if shipped:
        return 0, [f"refusing: tracked (shipped) canvas layer(s) {', '.join(shipped)}; "
                   "removing a committed run artifact is a decision for the owner"]
    if not dry:
        for p in layers:
            p.unlink()
    return len(layers), []


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
    ap.add_argument("--drop-canvas-layers", action="store_true",
                    help="delete untracked slide-NN.canvas.{png,webp} from ONE run "
                         "(--run only), instead of encoding")
    args = ap.parse_args()
    if args.drop_canvas_layers and (args.all or args.drop_png):
        ap.error("--drop-canvas-layers takes --run <date> alone")

    if args.all:
        runs = sorted(d for d in RUNS.iterdir() if d.is_dir())
    else:
        one = RUNS / args.run
        if not one.is_dir():
            print(f"FAIL no such run: runs/{args.run}", file=sys.stderr)
            return 1
        runs = [one]

    if args.drop_canvas_layers:
        run = runs[0]
        n, problems = drop_canvas_layers(run, args.dry_run)
        for p in problems:
            print(f"FAIL {p}", file=sys.stderr)
        left = strays(run) if not args.dry_run else []
        for p in left:
            print(f"  still not a frame, left alone: {p.name}", file=sys.stderr)
        print(f"ship_images --drop-canvas-layers runs/{run.name}: "
              f"{'would remove' if args.dry_run else 'removed'} {n}")
        return 1 if (problems or left) else 0

    if args.drop_png:
        print(f"ship_images --drop-png: {len(runs)} run(s)"
              f"{', DRY RUN' if args.dry_run else ''}\n")
        print(f"{'run':14s} {'reclaimed':>10s} {'kept':>10s}")
        freed = kept = 0
        problems = []
        stray_runs = []
        for run in runs:
            found = strays(run)
            if found:
                stray_runs.append(stray_message(run, found))
            d = drop_pngs(run, args.dry_run)
            freed += d["freed"]
            kept += d["kept"]
            problems += [f"{d['run']}/{s}" for s in d["skipped"]]
            if d["freed"] or d["kept"]:
                print(f"{d['run']:14s} {mb(d['freed']):>10s} {mb(d['kept']):>10s}")
        print(f"\n{'TOTAL':14s} {mb(freed):>10s} {mb(kept):>10s}")
        for p in problems:
            print(f"  kept, unverified: {p}", file=sys.stderr)
        if stray_runs:
            for m in stray_runs:
                print(f"  ! {m}", file=sys.stderr)
            print(f"\nFAIL {len(stray_runs)} run(s) hold files that are not frames",
                  file=sys.stderr)
            return 1
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
            # A stray is an error even when there is nothing left to encode,
            # or an already-converted run carrying canvas layers would print OK.
            for e in r["errors"]:
                print(f"  ! {e}", file=sys.stderr)
                failed.append(f"{r['run']}/{e}")
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
