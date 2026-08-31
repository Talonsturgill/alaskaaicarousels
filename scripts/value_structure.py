#!/usr/bin/env python3
"""Measure a slide's VALUE STRUCTURE, the notan, off the rendered pixels.

WHY THIS EXISTS. Artwork craft has been the weakest scored criterion in 9 of
the 10 runs before 2026-08-31, mean 6.65, while every other criterion sat above
8. The two defect classes that kept shipping inside a green machine_qa were
"busy art under text" and "top-loaded composition", 4 runs in 10 each. They are
not two problems. They are one problem, which is that detail gets spread evenly
across a frame instead of being organised into masses, and no gate in this repo
could see it, because every existing check reads the thumb for LEGIBILITY and
none reads it for STRUCTURE.

The classical fix is older than the defect. A picture that holds at thumbnail
size resolves into a small number of value masses. The rules, from the Phase 1
craft refresh of 2026-08-31:

  1. One mass predominates and covers MORE THAN HALF the frame.
  2. The remaining masses are NOT divided evenly. One takes more than the other.
  3. The darks are WELDED into one connected shape rather than scattered as
     separate marks of similar weight.
  4. Detail is added INSIDE a mass and never breaks it. Losing the structure
     while adding detail is the single most common cause of a weak one.

This script measures 1, 2 and 3 directly, plus a fourth thing the doctrine
already demands and nothing measured, which is whether the dominant mass
actually reaches the bottom third of the frame. A dominant mass that lives only
in the top of the frame IS top-loaded composition, stated as geometry rather
than as taste.

HOW IT MEASURES. It reads the render, resamples to 432px wide (FEED_W, the same
feed scale qa.py judges at) and converts to CIELAB L*, the same perceptual axis
qa.py uses for contact shadows, so a number here means what a number there
means. It then clusters L* into three masses with 1D k-means rather than fixed
thresholds, because a notan is about the picture's OWN masses and a dark deck
and a light deck do not share a threshold. The darkest mass is then SQUINTED,
blurred and re-thresholded, before its connected components are counted, and
that step is load bearing rather than cosmetic (see squint() for why).

IT REPORTS. It does not gate, and it is deliberately not wired into
gate_status.py. The thresholds below are the craft rules written down, not a
pass mark anyone voted on, and a deliberate composition can break any of them
for a reason. Read the numbers, look at the frame, decide. Exit is 0 when every
slide met every rule, 2 when something wants a human's eye, and 1 only when the
script itself broke.

CALIBRATION, and the bar any default-on check has to clear. Google's Tricorder
rule is that a check enabled by default must sit under about 10 percent
effective false positives, must be actionable, and must earn its way from
opt-in. Measured on 2026-08-31 against runs/2026-08-30, the deck immediately
before this script existed, which scored 8.79 overall with 7.0 on artwork
craft, its best in ten runs. The first version of this script flagged 9 of 9,
which is a 100 percent false positive rate and would have taught a run to work
around its own machine. After the squint step it flags 1 of 9, and that one is
slide 06, whose composition the instinct ledger already records as having gone
wrong. That is the evidence for keeping it, and it is one deck of evidence,
which is why this reports and does not gate.

USAGE
    python scripts/value_structure.py --render-dir out/<date>/render
    python scripts/value_structure.py --render-dir out/<date>/render --slide 4
    python scripts/value_structure.py --render-dir out/<date>/render --json
"""

import argparse
import glob
import json
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

FEED_W = 432              # the thumb width the doctrine's legibility test uses
N_MASSES = 3              # a notan is two to four masses; three is the house default
DOMINANT_MIN = 0.50       # rule 1, one mass covers more than half
UNEVEN_MIN_RATIO = 1.25   # rule 2, the two lesser masses differ by at least this
WELD_MAX_BLOBS = 4        # rule 3, the darks read as one shape, not a scatter
BLOB_FLOOR_FRAC = 0.0015  # a dark blob under this share of the frame is speckle
SQUINT_R = 3              # box blur radius at 432px, about what squinting merges
BOTTOM_THIRD_MIN = 0.18   # rule 4, the dominant mass must reach the lower band


def srgb_to_lstar(arr):
    """sRGB bytes to CIELAB L*, the same perceptual axis qa.py measures in."""
    c = arr.astype(np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    y = lin[..., 0] * 0.2126729 + lin[..., 1] * 0.7151522 + lin[..., 2] * 0.0721750
    fy = np.where(y > 0.008856, np.cbrt(y), (903.3 * y + 16.0) / 116.0)
    return np.where(y > 0.008856, 116.0 * fy - 16.0, 903.3 * y)


def kmeans_1d(values, k, iters=60, seed=7):
    """Cluster L* into k masses. Deterministic, seeded, no dependency."""
    v = values.ravel()
    lo, hi = float(v.min()), float(v.max())
    if hi - lo < 1e-6:
        return np.zeros(v.shape, dtype=np.int64), np.array([lo])
    # seed centres on quantiles rather than at random, so the same frame always
    # yields the same masses and a re-run is a re-measurement, not a re-roll.
    centres = np.quantile(v, [(i + 0.5) / k for i in range(k)])
    for _ in range(iters):
        d = np.abs(v[:, None] - centres[None, :])
        lab = np.argmin(d, axis=1)
        moved = 0.0
        for i in range(k):
            sel = v[lab == i]
            if sel.size:
                nc = float(sel.mean())
                moved = max(moved, abs(nc - centres[i]))
                centres[i] = nc
        if moved < 1e-4:
            break
    order = np.argsort(centres)          # darkest mass first
    remap = np.zeros(k, dtype=np.int64)
    remap[order] = np.arange(k)
    return remap[lab], centres[order]


def squint(mask, radius):
    """Blur a mask and re-threshold it, which is what squinting at a picture does.

    THIS STEP IS THE WHOLE POINT AND IT WAS MISSING FROM THE FIRST VERSION.
    Counting connected components on raw dark pixels measures the wrong thing
    for any art built from hatching, stipple or engraving, because a hatched
    passage is hundreds of separate thin marks that no reader perceives as
    separate. Measured on 2026-08-31 against No.45, a deck that scored 8.79 with
    its best artwork craft mark in ten runs, raw component counting called all
    nine slides scattered. The craft instruction has always said to SQUINT
    first, and squinting is a low pass filter. So blur, then threshold, then
    count what a reader would actually see as one shape.
    """
    if radius < 1:
        return mask
    f = mask.astype(np.float32)
    pad = np.pad(f, radius, mode="edge")
    # separable box blur via cumulative sums, cheap and dependency free
    c = np.cumsum(pad, axis=0)
    c = np.vstack([np.zeros((1, c.shape[1]), np.float32), c])
    f = (c[2 * radius + 1:, :] - c[:-(2 * radius + 1), :]) / (2 * radius + 1)
    c = np.cumsum(f, axis=1)
    c = np.hstack([np.zeros((c.shape[0], 1), np.float32), c])
    f = (c[:, 2 * radius + 1:] - c[:, :-(2 * radius + 1)]) / (2 * radius + 1)
    return f >= 0.5


def count_blobs(mask, floor_px):
    """Connected components (4-neighbour) above a size floor. No scipy here."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    sizes = []
    for y0 in range(h):
        row = mask[y0]
        for x0 in np.nonzero(row & ~seen[y0])[0]:
            n = 0
            q = deque([(y0, int(x0))])
            seen[y0, x0] = True
            while q:
                y, x = q.popleft()
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if n >= floor_px:
                sizes.append(n)
    sizes.sort(reverse=True)
    return sizes


def measure(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    fh = max(1, int(round(h * FEED_W / float(w))))
    feed = np.asarray(im.resize((FEED_W, fh), Image.LANCZOS))
    lab = srgb_to_lstar(feed)

    flat, centres = kmeans_1d(lab, N_MASSES)
    masses = flat.reshape(lab.shape)
    total = masses.size
    fracs = [float((masses == i).sum()) / total for i in range(N_MASSES)]

    order = np.argsort(fracs)[::-1]      # biggest mass first
    dominant_i = int(order[0])
    dom = fracs[dominant_i]
    lesser = sorted([fracs[int(order[1])], fracs[int(order[2])]], reverse=True)
    ratio = (lesser[0] / lesser[1]) if lesser[1] > 1e-9 else float("inf")

    dark = squint(masses == 0, SQUINT_R)
    blobs = count_blobs(dark, max(1, int(BLOB_FLOOR_FRAC * total)))

    band = masses[int(fh * 2 / 3):, :]
    bottom_share = float((band == dominant_i).sum()) / max(1, band.size)

    findings = []
    if dom < DOMINANT_MIN:
        findings.append("no mass predominates, biggest is %.0f%% of the frame and the rule is over 50" % (dom * 100))
    if ratio < UNEVEN_MIN_RATIO:
        findings.append("the two lesser masses are near equal at %.0f%% and %.0f%%, which reads as clutter"
                        % (lesser[0] * 100, lesser[1] * 100))
    if len(blobs) > WELD_MAX_BLOBS:
        findings.append("the darks are scattered across %d separate shapes, the rule is welding them into one"
                        % len(blobs))
    elif not blobs and fracs[0] > 0.04:
        # ZERO welded shapes is NOT a pass, and reading it as one was this
        # script's own first bug, found on 2026-08-31 against No.45's high key
        # deck. It means every dark pixel in the frame belongs to a blob under
        # the speckle floor, so the darkest mass exists only as scattered
        # crumbs. That is precisely the failure the weld rule is for, the thumb
        # that reads as unrelated marks rather than as one picture. A frame with
        # genuinely almost no dark, under half a percent, is exempt.
        findings.append("the darkest mass is %.1f%% of the frame yet survives no squint, so it is spread as "
                        "crumbs rather than gathered into a shape" % (fracs[0] * 100))
    if bottom_share < BOTTOM_THIRD_MIN:
        findings.append("the dominant mass fills only %.0f%% of the bottom third, which is a top-loaded frame"
                        % (bottom_share * 100))

    return {
        "slide": os.path.basename(path),
        "masses_pct": [round(f * 100, 1) for f in fracs],
        "mass_lstar": [round(float(c), 1) for c in centres],
        "dominant_pct": round(dom * 100, 1),
        "dominant_is": ["dark", "mid", "light"][dominant_i],
        "lesser_ratio": round(ratio, 2) if ratio != float("inf") else None,
        "dark_blobs": len(blobs),
        "dark_blob_pct": [round(100.0 * b / total, 1) for b in blobs[:6]],
        "dominant_in_bottom_third_pct": round(bottom_share * 100, 1),
        "findings": findings,
        "ok": not findings,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--render-dir", required=True)
    ap.add_argument("--slide", type=int, default=None, help="measure one slide number only")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    pat = "slide-%02d.png" % a.slide if a.slide else "slide-*.png"
    files = sorted(glob.glob(os.path.join(a.render_dir, pat)))
    if not files:
        print("value_structure: no renders matched %s in %s" % (pat, a.render_dir), file=sys.stderr)
        return 1

    rows = [measure(f) for f in files]

    if a.json:
        print(json.dumps({"feed_width": FEED_W, "slides": rows}, indent=1))
    else:
        print("VALUE STRUCTURE at %dpx feed width, three masses, k-means on CIELAB L*" % FEED_W)
        print("  masses are printed darkest first. dom is the biggest mass.\n")
        for r in rows:
            flag = "ok  " if r["ok"] else "LOOK"
            print("  [%s] %s  masses %s  dom %.0f%% (%s)  lesser ratio %s  dark shapes %d  bottom third %.0f%%"
                  % (flag, r["slide"], r["masses_pct"], r["dominant_pct"], r["dominant_is"],
                     r["lesser_ratio"], r["dark_blobs"], r["dominant_in_bottom_third_pct"]))
            for f in r["findings"]:
                print("        %s" % f)
        bad = [r for r in rows if not r["ok"]]
        print("\nvalue structure: %d of %d slides hold their masses" % (len(rows) - len(bad), len(rows)))
        if bad:
            print("what to do about it: fix the COMPOSITION, never the threshold. A frame with no")
            print("dominant mass needs mass moved into one, not a darker filter. Scattered darks")
            print("need welding into one shape. A thin bottom third needs the mass carried down,")
            print("not a plate laid over it. A deliberate exception is fine and belongs in the")
            print("dossier's field 4 with the reason.")

    return 2 if any(not r["ok"] for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
