#!/usr/bin/env python3
"""measure_frame.py -- answer a critic's claim about a rendered frame with a
measurement, in one command.

Why this exists (2026-09-17, run No.61). A round-two pixel verdict hard-failed
slide 05 saying its porosity was inverted, and reported curly apostrophes in the
copy. Both were wrong: a luminance-run measurement put the drawing within 0.016
of its printed ratios, and a character sweep of every source found no curly
quote anywhere. Declining a verdict is the right move when the verdict is wrong,
but that run had to improvise both measurements by hand, under revision-round
pressure, and write the result into the BUILD RECONCILIATION so the NEXT run
does not go and "fix" a correct drawing. A measurement that costs ten minutes to
improvise gets skipped, and a skipped measurement means the critic wins by
assertion. This makes both cost one line.

It is a MEASURING INSTRUMENT and not a gate. It has no thresholds, it never
exits non-zero on a reading, and nothing in the pipeline depends on it. It
prints what is in the pixels and in the bytes.

  # what fraction of a ruled panel is open, straight off the render
  python scripts/measure_frame.py porosity --png out/<date>/render/slide-05.png \
      --design-w 1080 --region 112,600,232,200 --axis x

  # every curly quote / dash / ellipsis in a set of sources, with addresses
  python scripts/measure_frame.py glyphs out/<date>/slides/*.html

Add --json for a machine-readable record to paste into a reconciliation.
Exit 0 on a successful measurement, 2 when it could not measure (bad region,
unreadable file). Never 1: this is not a gate and must not read like one.
"""
import argparse
import glob
import json
import sys
import unicodedata
from pathlib import Path

# The characters house style bans outright, plus the two that get REPORTED as
# present by eye far more often than they are: the curly apostrophe and the
# curly double quote. Named, so a finding has a word a human can search for.
BANNED_GLYPHS = {
    "‘": "left curly single quote",
    "’": "right curly single quote / curly apostrophe",
    "“": "left curly double quote",
    "”": "right curly double quote",
    "–": "en dash",
    "—": "em dash",
    "…": "horizontal ellipsis",
    " ": "non-breaking space",      # legal in HTML entity form, not raw
}


def _otsu(vals):
    """Otsu's threshold over a 0..255 histogram list. No parameter to tune."""
    hist = [0] * 256
    for v in vals:
        hist[v] += 1
    total = len(vals)
    sum_all = sum(i * hist[i] for i in range(256))
    sum_b, w_b, best, thr = 0.0, 0, -1.0, 128
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_all - sum_b) / w_f
        between = w_b * w_f * (m_b - m_f) ** 2
        if between > best:
            best, thr = between, t
    return thr


def _runs(mask):
    """[(value, length)] for a boolean row."""
    out, cur, n = [], mask[0], 0
    for v in mask:
        if v == cur:
            n += 1
        else:
            out.append((cur, n))
            cur, n = v, 1
    out.append((cur, n))
    return out


def _median(xs):
    if not xs:
        return None
    s = sorted(xs)
    m = len(s) // 2
    return float(s[m]) if len(s) % 2 else (s[m - 1] + s[m]) / 2.0


def porosity(png, region, design_w, axis):
    """The open fraction of a region, measured in luminance runs.

    `region` is x,y,w,h in DESIGN px; the PNG's own width against --design-w
    gives the scale, so a region is quoted in the same numbers the slide source
    uses. Ink is the darker class of an Otsu split INSIDE the region, so a
    light-on-dark panel measures the same way a dark-on-light one does, and the
    threshold is never a parameter anyone tunes to get an answer they wanted.
    """
    from PIL import Image
    im = Image.open(png).convert("L")
    sc = im.width / float(design_w)
    x, y, w, h = [int(round(v * sc)) for v in region]
    if w < 2 or h < 2 or x < 0 or y < 0 or x + w > im.width or y + h > im.height:
        raise ValueError("region %s falls outside the %dx%d frame at scale %.3f"
                         % (region, im.width, im.height, sc))
    crop = im.crop((x, y, x + w, y + h))
    if axis == "y":                          # rule the other way
        crop = crop.transpose(Image.ROTATE_90)
        w, h = h, w
    px = list(crop.getdata())
    thr = _otsu(px)
    dark_is_ink = (sum(px) / len(px)) > thr  # the minority class is the mark
    rows, ink_px, marks, gaps = [], 0, [], []
    for r in range(h):
        row = px[r * w:(r + 1) * w]
        mask = [(v <= thr) if dark_is_ink else (v > thr) for v in row]
        ink_px += sum(1 for v in mask if v)
        rr = _runs(mask)
        marks += [n / sc for v, n in rr[1:-1] if v]
        gaps += [n / sc for v, n in rr[1:-1] if not v]
        rows.append(1.0 - sum(1 for v in mask if v) / float(w))
    total = float(w * h)
    mark_w, gap_w = _median(marks), _median(gaps)
    return {
        "png": str(png), "region": list(region), "axis": axis, "scale": sc,
        "threshold": thr, "ink_is": "dark" if dark_is_ink else "light",
        "open_fraction": round(1.0 - ink_px / total, 4),
        "open_fraction_row_median": round(_median(rows) or 0.0, 4),
        "mark_px_median": None if mark_w is None else round(mark_w, 2),
        "gap_px_median": None if gap_w is None else round(gap_w, 2),
        "pitch_px_median": None if (mark_w is None or gap_w is None)
        else round(mark_w + gap_w, 2),
        "marks_counted": len(marks),
    }


def glyphs(paths):
    """Every banned or curly character in these files, with file, line, column,
    codepoint and name. An empty list is the answer to "there are curly
    apostrophes in the copy" and it is worth exactly as much as the finding."""
    hits, read = [], []
    for p in paths:
        try:
            text = Path(p).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            hits.append({"file": str(p), "error": type(e).__name__})
            continue
        read.append(str(p))
        for ln, line in enumerate(text.splitlines(), 1):
            for col, ch in enumerate(line, 1):
                if ch in BANNED_GLYPHS:
                    hits.append({"file": str(p), "line": ln, "col": col,
                                 "char": "U+%04X" % ord(ch),
                                 "name": BANNED_GLYPHS[ch],
                                 "context": line.strip()[:70]})
                elif ord(ch) > 0x2000 and unicodedata.category(ch) in ("So", "Sk"):
                    hits.append({"file": str(p), "line": ln, "col": col,
                                 "char": "U+%04X" % ord(ch),
                                 "name": "symbol (emoji class)",
                                 "context": line.strip()[:70]})
    return {"files_read": len(read), "hits": hits}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    po = sub.add_parser("porosity")
    po.add_argument("--png", required=True)
    po.add_argument("--region", required=True, help="x,y,w,h in design px")
    po.add_argument("--design-w", type=float, default=1080.0)
    po.add_argument("--axis", choices=("x", "y"), default="x",
                    help="x = marks ruled across the region's width")
    po.add_argument("--json", action="store_true")
    gl = sub.add_parser("glyphs")
    gl.add_argument("paths", nargs="+")
    gl.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.cmd == "porosity":
        try:
            reg = [float(v) for v in a.region.split(",")]
            if len(reg) != 4:
                raise ValueError("--region takes x,y,w,h")
            rec = porosity(Path(a.png), reg, a.design_w, a.axis)
        except Exception as e:
            print("could not measure: %s" % e, file=sys.stderr)
            return 2
        if a.json:
            print(json.dumps(rec, indent=2))
        else:
            print("%s  region %s  axis %s" % (Path(a.png).name, a.region, a.axis))
            print("  open fraction   %.4f  (row median %.4f)"
                  % (rec["open_fraction"], rec["open_fraction_row_median"]))
            print("  mark / gap / pitch, design px   %s / %s / %s"
                  % (rec["mark_px_median"], rec["gap_px_median"],
                     rec["pitch_px_median"]))
            print("  %d marks measured, ink is the %s class at luminance %d"
                  % (rec["marks_counted"], rec["ink_is"], rec["threshold"]))
        return 0

    paths = []
    for p in a.paths:
        paths += sorted(glob.glob(p)) or [p]
    rec = glyphs(paths)
    if a.json:
        print(json.dumps(rec, indent=2))
    else:
        for h in rec["hits"]:
            if h.get("error"):
                print("%s: unreadable (%s)" % (h["file"], h["error"]))
            else:
                print("%s:%d:%d  %s  %s  |  %s"
                      % (h["file"], h["line"], h["col"], h["char"], h["name"],
                         h["context"]))
        print("%d file(s) read, %d finding(s)" % (rec["files_read"], len(rec["hits"])))
    return 0 if rec["files_read"] or not paths else 2


if __name__ == "__main__":
    sys.exit(main())
