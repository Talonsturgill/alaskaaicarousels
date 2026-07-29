#!/usr/bin/env python3
"""
Shrink carousel.pdf by resampling its art layer, without touching the type.

A carousel.pdf is built by Chromium's print engine and comes out layered: one
full-page JPEG per page carrying the generative art, with the headline and body
type sitting on top as real vector text. Measured on 2026-07-26, that JPEG is
76 percent of the file, the fonts are half a percent, and the rest is vector
paths. So the only thing worth touching is the art layer.

The embedded JPEG is 2160 px across a 810 pt page, which is 192 DPI, and the
page is displayed at 1080 px. That is 2x the pixels anyone sees. Resampling to
1620 px is still 1.5x native and takes about half the file with it.

WHAT THIS WILL NOT DO:

- It never rewrites the content streams, so the vector text is untouched by
  construction. It still extracts the text before and after and refuses to
  write a file whose text changed by even one character.
- It only touches plain DCTDecode DeviceRGB images with no soft mask. Anything
  with alpha, an ICC profile or an unusual filter is left exactly as it is,
  because a PDF that is smaller and wrong is worse than a big one.
- It refuses any image that lands below the PSNR floor. This is a second
  generation of lossy encoding on already-lossy data, which is why the floor is
  higher here than for the WebP pass.
- It refuses to write a PDF that got bigger, changed page count, or changed
  page dimensions.

The historical PDFs cannot be regenerated: their source HTML lives in the
gitignored out/ directory. They are recoverable from git history and nowhere
else, so every check above fails closed.

Usage:
    python scripts/shrink_pdfs.py --run 2026-07-28
    python scripts/shrink_pdfs.py --all --dry-run
    python scripts/shrink_pdfs.py --all
"""
from __future__ import annotations

import argparse
import io
import math
import sys
from pathlib import Path

try:
    import pikepdf
    import pypdf
    from PIL import Image, ImageChops
except ImportError as exc:
    sys.exit(f"needs pikepdf, pypdf and Pillow: {exc}")

REPO = Path(__file__).resolve().parents[1]
RUNS = REPO / "runs"

# 1620 px across an 810 pt page is 144 DPI, still 1.5x the 1080 px the page is
# actually displayed at. Going to 1080 would be exactly native with no headroom
# for a reader who zooms, which is not a trade worth 2 MB.
TARGET_WIDTH = 1620
JPEG_QUALITY = 85
# Higher than the 40 dB used for the slide WebP on purpose: that pass encoded
# once from a lossless master, this one re-encodes something already lossy.
PSNR_FLOOR = 42.0
MIN_SAVING = 0.10          # below this the churn is not worth a rewrite


def psnr(a: Image.Image, b: Image.Image) -> float:
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


def art_images(pdf) -> list:
    """Every image XObject this tool considers safe to resample."""
    found, seen = [], set()

    def walk(res, depth=0):
        if res is None or depth > 6:
            return
        for _, x in (res.get("/XObject") or {}).items():
            if x.objgen in seen:
                continue
            seen.add(x.objgen)
            sub = str(x.get("/Subtype"))
            if sub == "/Form":
                walk(x.get("/Resources"), depth + 1)
            elif sub == "/Image":
                # Conservative on purpose. Alpha, exotic colour spaces and
                # non-JPEG filters all get left alone rather than guessed at.
                if (str(x.get("/Filter")) == "/DCTDecode"
                        and str(x.get("/ColorSpace")) == "/DeviceRGB"
                        and x.get("/SMask") is None
                        and x.get("/Mask") is None
                        and int(x.get("/Width", 0)) > TARGET_WIDTH):
                    found.append(x)

    for page in pdf.pages:
        walk(page.get("/Resources"))
    return found


def page_text(path: Path) -> list[str]:
    r = pypdf.PdfReader(str(path))
    return [(p.extract_text() or "") for p in r.pages]


def page_boxes(pdf) -> list[tuple]:
    return [tuple(round(float(v), 3) for v in p.MediaBox) for p in pdf.pages]


def shrink(path: Path, dry: bool) -> dict:
    out = {"file": path.parent.name, "before": path.stat().st_size, "after": 0,
           "images": 0, "worst": float("inf"), "skipped": [], "error": None}

    before_text = page_text(path)
    pdf = pikepdf.open(path)
    before_boxes = page_boxes(pdf)
    targets = art_images(pdf)
    if not targets:
        out["error"] = "nothing resamplable (already shrunk, or no plain RGB art layer)"
        # An untouched file is unchanged, not emptied. Leaving "after" at zero
        # made the report claim a 100 percent saving on a file it correctly
        # refused to open, which is the most alarming possible way to say
        # "did nothing".
        out["after"] = out["before"]
        return out

    # A raster-fallback PDF carries its type baked into the page image, so
    # page_text returns "" for every page and the identity check at the end
    # compares [""] to [""] and always passes: it is blind to the headline type
    # being resampled inside the DCTDecode art layer, protected only by a global
    # PSNR average that under-reports exactly at text edges. Refuse rather than
    # shrink behind a guarantee that does not hold. The master stays; an oversize
    # raster PDF is the size gate's concern, not this one's. A vector PDF has
    # real extractable text, so the identity check there is meaningful.
    if not any(t.strip() for t in before_text):
        pdf.close()
        out["error"] = ("raster PDF, no text layer to verify type integrity; "
                        "keeping the master rather than resampling type-bearing art")
        out["after"] = out["before"]
        return out

    for x in targets:
        try:
            raw = x.read_raw_bytes()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            h = max(1, round(im.height * TARGET_WIDTH / im.width))
            small = im.resize((TARGET_WIDTH, h), Image.LANCZOS)
            buf = io.BytesIO()
            small.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True,
                       progressive=True, subsampling=0)
            data = buf.getvalue()
            if len(data) >= len(raw):
                out["skipped"].append("re-encode was not smaller")
                continue
            check = psnr(im, Image.open(io.BytesIO(data)).convert("RGB").resize(
                im.size, Image.LANCZOS))
            if check < PSNR_FLOOR:
                out["skipped"].append(f"{check:.1f} dB below floor")
                continue
            out["worst"] = min(out["worst"], check)
            if not dry:
                x.write(data, filter=pikepdf.Name("/DCTDecode"))
                x.Width, x.Height = TARGET_WIDTH, h
            out["images"] += 1
        except Exception as exc:                                   # noqa: BLE001
            out["skipped"].append(str(exc)[:70])

    if not out["images"] or dry:
        out["after"] = out["before"]
        return out

    tmp = path.with_suffix(".pdf.tmp")
    pdf.save(tmp, linearize=True)
    pdf.close()

    # Everything below fails closed: the original stays on disk unless the
    # rewrite is provably the same document with a lighter art layer.
    try:
        after = pikepdf.open(tmp)
        if len(after.pages) != len(before_text):
            raise ValueError(f"page count {len(after.pages)} != {len(before_text)}")
        if page_boxes(after) != before_boxes:
            raise ValueError("page dimensions changed")
        after.close()
        if page_text(tmp) != before_text:
            raise ValueError("extracted text changed, the type is not intact")
        size = tmp.stat().st_size
        if size >= out["before"]:
            raise ValueError("result was not smaller")
        if (out["before"] - size) / out["before"] < MIN_SAVING:
            raise ValueError(f"saving under {MIN_SAVING:.0%}, not worth the rewrite")
    except Exception as exc:                                       # noqa: BLE001
        tmp.unlink(missing_ok=True)
        out["error"] = str(exc)
        out["after"] = out["before"]
        return out

    tmp.replace(path)
    out["after"] = path.stat().st_size
    return out


def mb(n: float) -> str:
    return f"{n / 1048576:.2f}M"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", help="a single run date")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.all:
        pdfs = sorted(RUNS.glob("*/carousel.pdf"))
    else:
        one = RUNS / args.run / "carousel.pdf"
        if not one.exists():
            print(f"FAIL no such file: {one}", file=sys.stderr)
            return 1
        pdfs = [one]

    print(f"shrink_pdfs: {len(pdfs)} file(s), art layer to {TARGET_WIDTH}px "
          f"q{JPEG_QUALITY}, floor {PSNR_FLOOR} dB"
          f"{', DRY RUN' if args.dry_run else ''}\n")
    print(f"{'run':14s} {'before':>8s} {'after':>8s} {'saved':>7s} {'imgs':>5s} {'min dB':>7s}")

    tb = ta = 0
    problems = []
    for p in pdfs:
        r = shrink(p, args.dry_run)
        tb += r["before"]
        ta += r["after"]
        worst = "-" if r["worst"] == float("inf") else f"{r['worst']:.1f}"
        saved = f"{(r['before'] - r['after']) / r['before'] * 100:.0f}%" if r["before"] else "-"
        print(f"{r['file']:14s} {mb(r['before']):>8s} {mb(r['after']):>8s} "
              f"{saved:>7s} {r['images']:5d} {worst:>7s}")
        if r["error"]:
            print(f"    kept as-is: {r['error']}")
            problems.append(r["file"])
        for s in r["skipped"]:
            print(f"    skipped an image: {s}")

    print(f"\n{'TOTAL':14s} {mb(tb):>8s} {mb(ta):>8s} "
          f"{(tb - ta) / tb * 100 if tb else 0:6.0f}%   saved {mb(tb - ta)}")
    if problems:
        print(f"\n{len(problems)} file(s) left untouched. That is the safe outcome, "
              f"not a failure.")
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
