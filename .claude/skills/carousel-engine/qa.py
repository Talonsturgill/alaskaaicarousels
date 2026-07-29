#!/usr/bin/env python3
"""qa.py — machine QA over rendered slides. The objective half of the review
loop; the subjective half is the pixel-critic agents reading the PNGs.

Checks per slide (consuming render_report.json + the PNGs):
  - PNG exists, exact expected pixel size
  - not blank / not near-uniform (dead render detector)
  - TEXT COLLISIONS: no two text elements' line boxes may overprint
    (FAIL when both are primary text, WARN when either is decorative).
    Added 2026-07-08 after a body-copy-over-bar-label collision passed
    every other gate and had to be caught by the scorer's eyes.
  - BUSY ART UNDER TEXT (WARN only): samples the PNG under each primary text
    line box, masks the glyph ink, and warns when the background carries
    high-contrast structured edges (a canvas/bitmap arc or texture the DOM
    collision gate cannot see). Added 2026-07-10 after canvas flightpath/orbit
    arcs crossed body copy and a headline and machine QA passed both.
  - LABEL CROSSED BY ART (FAIL): samples a thin ring around each non-decorative
    label's glyph ink and FAILS when ink of the GLYPHS' OWN VALUE touches the
    letterforms across the label (a rule, scored outline or groove edge struck
    through the text). Knockout plates and halos leave that ring clean.
    Added 2026-07-25 after four slides shipped art-band labels crossed by
    canvas-drawn geometry through two scoring cycles of PASS with zero warns.
  - TEXT UNDER AN OPAQUE PLATE (FAIL): consumes render.py's occlusion probe
    (paint-order-confirmed intersections of each line box with foreign opaque
    element boxes) and FAILS when a plate covers >=20x6px of a non-decorative
    line box. Added 2026-07-26 after an opaque DEAD plate over the bottom third
    of a subtitle and a note column run under a callout plate produced two
    consecutive hard fails while machine QA reported PASS, 0 fails, 0 warns:
    text_collisions() only compares GLYPH LINE BOXES, and a padded plate's
    background is not one.
  - FRAME BALANCE / DEAD LOWER ZONE (FAIL): compares the bottom third's
    craft-density against the slide's own frame average and FAILS a top-loaded
    composition (<55%). Added 2026-07-26 after the SIXTH consecutive scorer
    note naming "dead lower zones" as the series' artwork-craft ceiling. Every
    earlier gate here judges legibility; nothing measured composition, so the
    only reviewer who saw this was the scorer, at the ship gate, too late to
    rebuild slides -- which is why it became a note six times instead of a fix.
    data-breather on <body> demotes it to WARN (and the dossier gate checks the
    storyboard actually declared that slide a breather).
  - CANVAS RASTER TEXT (WARN only): warns when a slide draws meaningful text
    (>=4 alphabetic chars) via canvas fillText/strokeText, which ships as a
    bitmap in the vector PDF and is invisible to the ranker/copy_sync/a11y.
    Added 2026-07-19 after S7/S8 canvas labels had to be converted to DOM by hand.
  - approximate contrast of every non-decorative text node vs its local
    background (WCAG-style luminance ratio; estimate, so thresholds are
    conservative: <2.0 on primary text = FAIL, <3.5 = WARN)
  - text nodes inside the safe zone (default 80px margins at 1080x1350;
    slides may bleed decorative art, not primary text)
  - forwards render_report warnings (offscreen/clipped/tiny text, missing
    fonts, console errors)

Usage:
  python .claude/skills/carousel-engine/qa.py --render-dir out/run/render
Exit codes: 0 pass (warnings allowed), 1 any FAIL.
Writes <render-dir>/machine_qa.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SAFE_MARGIN = 80  # px at 1080-wide design size


def rel_luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def parse_css_color(s):
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)", s or "")
    if not m:
        return None
    return tuple(float(m.group(i)) for i in (1, 2, 3))


def contrast_estimate(img_arr, node, scale):
    """Estimate contrast between text color and its local background.

    The bbox contains both text and background pixels; the background is
    estimated as the median of the pixels most different from the text color
    (text coverage in a bbox is typically well under half).
    """
    color = parse_css_color(node.get("color"))
    if color is None:
        return None
    x, y = int(node["x"] * scale), int(node["y"] * scale)
    w, h = int(node["w"] * scale), int(node["h"] * scale)
    H, W = img_arr.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 - x0 < 4 or y1 - y0 < 4:
        return None
    crop = img_arr[y0:y1, x0:x1].reshape(-1, img_arr.shape[2])[:, :3].astype(float)
    if len(crop) > 20000:
        crop = crop[:: len(crop) // 20000]
    dist = np.abs(crop - np.array(color)).sum(axis=1)
    bg = np.median(crop[dist > np.percentile(dist, 55)], axis=0) if (dist > np.percentile(dist, 55)).any() else np.median(crop, axis=0)
    lt, lb = rel_luminance(color), rel_luminance(bg)
    lo, hi = min(lt, lb), max(lt, lb)
    return (hi + 0.05) / (lo + 0.05)


BUSY_INK_DIST = 90      # sum-abs RGB distance under which a pixel counts as glyph ink
BUSY_EDGE_LUM = 28      # luminance step (0..255) that counts as a "structured edge"
BUSY_DILATE = 2         # px to grow the ink mask by, to exclude anti-aliased glyph edges
BUSY_WARN = 0.03        # background edge-density above which we point the critics at the box


def _dilate(mask, k):
    m = mask.copy()
    for _ in range(k):
        n = m.copy()
        n[:-1] |= m[1:]; n[1:] |= m[:-1]
        n[:, :-1] |= m[:, 1:]; n[:, 1:] |= m[:, :-1]
        m = n
    return m


def busy_art_under_text(img_arr, node, scale):
    """WARN-level tripwire for canvas/bitmap art crossing a DOM text line box.

    text_collisions() only sees DOM/SVG text vs DOM/SVG text; canvas ink is a
    bitmap invisible to render.py's DOM walk, so structured art drawn UNDER a
    text line passes every objective gate (2026-07-10: an S3 flightpath arc
    crossed two body lines and an S4 orbit arc crossed the headline, and
    machine_qa PASSED both -- only the pixel critics caught them). This samples
    the PNG under each of a node's text line boxes, masks off the glyph ink
    (plus a 2px dilation for anti-aliased edges), and measures the fraction of
    remaining BACKGROUND pixel pairs that straddle a high-contrast luminance
    step. A solid or smooth-gradient background scores ~0; an arc, stroke, or
    dense texture crossing the text scores high. Returns the worst background
    edge density over the node's line boxes (0..1), or None if unmeasurable.
    Never a FAIL and never a threshold on legibility itself: it only points the
    pixel critics at a box to judge by eye.
    """
    color = parse_css_color(node.get("color"))
    if color is None:
        return None
    lines = node.get("lines") or [[node["x"], node["y"], node["w"], node["h"]]]
    H, W = img_arr.shape[:2]
    worst = None
    for bx, by, bw, bh in lines:
        x0, y0 = max(0, int(bx * scale)), max(0, int(by * scale))
        x1, y1 = min(W, int((bx + bw) * scale)), min(H, int((by + bh) * scale))
        if x1 - x0 < 8 or y1 - y0 < 8:
            continue
        crop = img_arr[y0:y1, x0:x1, :3].astype(float)
        lum = 0.2126 * crop[..., 0] + 0.7152 * crop[..., 1] + 0.0722 * crop[..., 2]
        ink = np.abs(crop - np.array(color)).sum(axis=2) < BUSY_INK_DIST
        if ink.mean() > 0.75:
            continue  # box is almost all ink colour (solid plate); nothing to read under
        bg = ~_dilate(ink, BUSY_DILATE)
        hd = np.abs(lum[:, 1:] - lum[:, :-1]); hb = bg[:, 1:] & bg[:, :-1]
        vd = np.abs(lum[1:, :] - lum[:-1, :]); vb = bg[1:, :] & bg[:-1, :]
        tot = int(hb.sum()) + int(vb.sum())
        if tot < 50:
            continue
        edges = int(((hd > BUSY_EDGE_LUM) & hb).sum()) + int(((vd > BUSY_EDGE_LUM) & vb).sum())
        d = edges / tot
        worst = d if worst is None else max(worst, d)
    return worst


GLYPH_RING_IN = 2       # px of anti-aliased glyph edge skipped before the ring starts
GLYPH_RING_OUT = 5      # px outer radius of the ring sampled around the glyphs
GLYPH_MIN_SPAN = 20     # min |paper - ink| luminance span to reason about at all
GLYPH_SAME_FRAC = 0.5   # ring pixel counts as foreign ink when it is this much closer to ink than paper
GLYPH_WARN = 0.02       # contaminated ring fraction that points the critics at the label
GLYPH_FAIL = 0.07       # contaminated ring fraction that, WITH extent, is a crossed label
GLYPH_FAIL_EXTENT = 0.30  # fraction of the label's columns (or rows) the contamination spans


def glyph_ink_contamination(img_arr, node, scale):
    """FAIL-grade detector for a label CROSSED by canvas/SVG geometry.

    Added 2026-07-25. busy_art_under_text() only WARNs, and only looked at
    primary text (>= 30px), so the art-band mono labels of run 2026-07-25 (24px)
    were never sampled at all: groove edges, scored slot outlines and leader
    rules ran straight through four slides' label glyphs and qa.py reported PASS
    with zero warns across TWO scoring cycles (two hard fails, score capped 6.9).

    Measures the DEFENSE rather than the busyness, which is what separates the
    defect from legitimate art-band typography: sample a thin ring around the
    glyph ink (skipping GLYPH_RING_IN px of anti-aliasing) and count ring pixels
    whose luminance is closer to the GLYPH's own value than to the local paper
    value. A knockout plate, a halo, or any deliberate contrast reserve leaves
    that ring clean (a halo is the OPPOSITE value, so it never trips). A rule,
    outline or groove edge crossing the letterforms puts ink of the glyph's own
    value directly against them, all the way across the label.

    Returns (frac, extent) where frac is the contaminated share of the ring and
    extent is the larger of the column/row span of that contamination (a rule
    crossing a label contaminates nearly every column; a single incidental blob
    contaminates few), or None when unmeasurable.
    """
    color = parse_css_color(node.get("color"))
    if color is None:
        return None
    ink_lum = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
    lines = node.get("lines") or [[node["x"], node["y"], node["w"], node["h"]]]
    H, W = img_arr.shape[:2]
    worst = None
    for bx, by, bw, bh in lines:
        # pad the box so the ring is measurable at the glyph extremes
        x0, y0 = max(0, int(bx * scale) - 3), max(0, int(by * scale) - 3)
        x1, y1 = min(W, int((bx + bw) * scale) + 3), min(H, int((by + bh) * scale) + 3)
        if x1 - x0 < 8 or y1 - y0 < 8:
            continue
        crop = img_arr[y0:y1, x0:x1, :3].astype(float)
        lum = 0.2126 * crop[..., 0] + 0.7152 * crop[..., 1] + 0.0722 * crop[..., 2]
        ink = np.abs(crop - np.array(color)).sum(axis=2) < BUSY_INK_DIST
        if ink.mean() > 0.75 or ink.sum() < 20:
            continue  # solid plate of the ink colour, or no glyph ink found
        near = _dilate(ink, GLYPH_RING_IN)
        far = _dilate(ink, GLYPH_RING_OUT)
        ring = far & ~near
        if int(ring.sum()) < 40:
            continue
        outer = ~far
        paper = float(np.median(lum[outer])) if int(outer.sum()) > 40 else float(np.median(lum[ring]))
        span = abs(paper - ink_lum)
        if span < GLYPH_MIN_SPAN:
            continue  # ink and ground are near-equal; the contrast gate owns this
        cont = np.abs(lum[ring] - ink_lum) < GLYPH_SAME_FRAC * span
        frac = float(cont.mean())
        cmask = np.zeros_like(ring)
        cmask[ring] = cont
        extent = max(float(cmask.any(axis=0).mean()), float(cmask.any(axis=1).mean()))
        if worst is None or frac > worst[0]:
            worst = (frac, extent)
    return worst


FB_DOWN = 6          # box-downsample factor: kills film grain, keeps structure
FB_CELL = 9          # downsampled px per grid cell (9*6 = 54 png px = 27 design px)
FB_LIVE = 8.0        # cell energy (0..255 luminance spread) at which a cell holds anything
FB_MODELED = 0.55    # tonal entropy at which that content is MODELED, not flat fill
FB_MARGIN = 3        # cells of the 80px safe-margin ring excluded from the bands
FB_FAIL = 0.60       # bottom-band craft density / frame craft density = top-loaded
FB_WARN = 0.80


def _box_down(a, k):
    h, w = a.shape[:2]
    h -= h % k
    w -= w % k
    return a[:h, :w].reshape(h // k, k, w // k, k, -1).mean(axis=(1, 3))


def frame_balance(img_arr):
    """Detect a TOP-LOADED composition -- the 'dead lower zone' that has capped
    artwork craft at 6-7 for six consecutive runs (ledger entries 10, 11, 13,
    14, 15, 16, 18).

    Added 2026-07-26 after the sixth consecutive scorer note naming the same
    defect. The root cause was never a missing pair of eyes, it was
    DESIGN_DOCTRINE 1's "at least one generous quiet zone per slide": an
    unbounded, unplaced licence that the directors room kept spending on the
    frame's bottom band, because that is the cheapest place to put it. The
    dossier then legitimized the empty bottom, and the pixel critics grade each
    slide against its own dossier, so the only reviewer who ever saw the defect
    was the scorer -- at the ship gate, with no budget left to rebuild slides.
    Every run it therefore became a FIELD_NOTES sentence instead of a fix.

    TWO defects share the name, and separating them is what took this from a
    note to a gate. (1) The bottom band is EMPTY (2026-07-17 S09 and
    2026-07-20 S03 both ship a bottom 40% with nothing in it; neither was ever
    named, which is its own evidence about relying on eyes). (2) The bottom
    band is OCCUPIED BUT FLAT -- grey label plates and hairlines floating on
    bare ground, which is what 2026-07-26's S05 and S08 actually are. A plain
    occupancy measure sees only (1): across the 45 scorer-labeled slides the
    dead ones' whole-frame occupancy (median 0.505) is indistinguishable from
    the rest (0.537), because every slide has quiet margins and a flat plate
    counts as "occupied".

    So a cell only counts when it carries MODELED tone. Box-downsample the PNG
    6x (film grain is high-frequency and would otherwise read as craft
    everywhere), then per 27px design cell take the robust luminance spread and
    peak local gradient (does it hold anything at all) AND the normalized
    entropy of its tonal histogram (is that content modeled or flat). A flat
    plate is bimodal and scores ~0.2; graded, textured, lit or rendered art
    scores 0.7+. Drop the safe-margin ring, then compare the bottom third's
    craft density against the slide's OWN frame average.

    Deliberately RELATIVE. An absolute craft floor was tested and rejected: it
    fails 48-60% of every slide the series has ever shipped, which makes it a
    taste judgment the machine has no business making unilaterally, and the
    doctrine's own position is that flat is a legitimate choice. The ratio
    asks only the question the scorers kept asking, which is whether the slide
    spends its craft up top and coasts. Content spread through the frame
    scores ~1.0 at any density.

    Returns (ratio, bands) or None if unmeasurable.
    """
    d = _box_down(img_arr.astype(np.float32), FB_DOWN)
    lum = 0.2126 * d[..., 0] + 0.7152 * d[..., 1] + 0.0722 * d[..., 2]
    rows, cols = lum.shape[0] // FB_CELL, lum.shape[1] // FB_CELL
    if rows < 3 * FB_MARGIN + 6 or cols < 2 * FB_MARGIN + 2:
        return None
    lum = lum[:rows * FB_CELL, :cols * FB_CELL]
    cells = lum.reshape(rows, FB_CELL, cols, FB_CELL).transpose(0, 2, 1, 3)
    cells = cells.reshape(rows, cols, FB_CELL * FB_CELL)
    # robust spread (p90-p10) ignores a lone anti-aliased pixel; the gradient
    # term keeps a single hard edge through an otherwise flat cell counted.
    spread = np.percentile(cells, 90, axis=2) - np.percentile(cells, 10, axis=2)
    gx, gy = np.abs(np.diff(lum, axis=1)), np.abs(np.diff(lum, axis=0))
    g = np.zeros_like(lum)
    g[:, :-1] += gx; g[:, 1:] += gx; g[:-1, :] += gy; g[1:, :] += gy
    gc = g.reshape(rows, FB_CELL, cols, FB_CELL).transpose(0, 2, 1, 3).reshape(rows, cols, -1)
    live = np.maximum(spread, np.percentile(gc, 98, axis=2)) >= FB_LIVE

    # modeled-tone test: normalized entropy of each cell's luminance histogram
    bins = 12
    rng = cells.max(axis=2) - cells.min(axis=2)
    q = np.clip((cells - cells.min(axis=2, keepdims=True)) /
                np.maximum(rng[..., None], 1e-6) * (bins - 1), 0, bins - 1).astype(np.int8)
    ent = np.zeros(q.shape[:2], dtype=np.float32)
    for b in range(bins):
        p = (q == b).sum(axis=2) / q.shape[2]
        ent -= np.where(p > 0, p * np.log2(np.maximum(p, 1e-12)), 0)
    ent = np.where(rng >= 2.0, ent / np.log2(bins), 0.0)

    craft = live & (ent >= FB_MODELED)
    inner = craft[FB_MARGIN:rows - FB_MARGIN, FB_MARGIN:cols - FB_MARGIN]
    band = inner.shape[0] // 3
    if band < 2:
        return None
    occ = float(inner.mean())
    if occ < 1e-6:
        return None  # the near-uniform gate above owns a truly blank frame
    bands = [float(inner[:band].mean()), float(inner[band:2 * band].mean()),
             float(inner[2 * band:].mean())]
    return bands[2] / occ, bands


OCC_FAIL_W = 20     # px of a line box's WIDTH an opaque plate must cover to FAIL
OCC_FAIL_H = 6       # px of its HEIGHT (a quarter of the 24px mono floor)
OCC_WARN_W = 12      # the tripwire band below the FAIL, for the critics' eyes
OCC_WARN_H = 4


def text_collisions(nodes, min_overlap=0.30, min_px=8):
    """Detect text-on-text overprint between distinct elements.

    Compares per-LINE boxes (render.py extracts them; falls back to the
    element bbox), skips DOM ancestor/descendant pairs, and counts a
    collision when the intersection covers >= min_overlap of the smaller
    line box in both dimensions beyond min_px. Returns
    [(i, j, overlap_ratio)] with i < j indexing `nodes`.
    """
    found = []
    for i in range(len(nodes)):
        a = nodes[i]
        a_lines = a.get("lines") or [[a["x"], a["y"], a["w"], a["h"]]]
        a_anc = set(a.get("anc") or [])
        for j in range(i + 1, len(nodes)):
            b = nodes[j]
            if i in (b.get("anc") or []) or j in a_anc:
                continue  # nested elements share ink legitimately
            b_lines = b.get("lines") or [[b["x"], b["y"], b["w"], b["h"]]]
            worst = 0.0
            for ax, ay, aw, ah in a_lines:
                for bx, by, bw, bh in b_lines:
                    ix = min(ax + aw, bx + bw) - max(ax, bx)
                    iy = min(ay + ah, by + bh) - max(ay, by)
                    if ix < min_px or iy < min_px:
                        continue
                    smaller = min(aw * ah, bw * bh)
                    if smaller <= 0:
                        continue
                    worst = max(worst, (ix * iy) / smaller)
            if worst >= min_overlap:
                found.append((i, j, worst))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render-dir", required=True)
    ap.add_argument("--safe-margin", type=int, default=SAFE_MARGIN)
    args = ap.parse_args()

    rdir = Path(args.render_dir)
    report = json.loads((rdir / "render_report.json").read_text())
    scale = report["canvas"]["scale"]
    exp_w, exp_h = report["canvas"]["px"]
    design_w, design_h = report["canvas"]["width"], report["canvas"]["height"]

    out = {"slides": [], "fails": 0, "warns": 0}
    for rec in report["slides"]:
        res = {"file": rec["file"], "fails": [], "warns": []}
        png = rdir / rec["png"]
        if not png.exists():
            res["fails"].append("png missing")
            out["slides"].append(res)
            continue
        im = Image.open(png).convert("RGB")
        if im.size != (exp_w, exp_h):
            res["fails"].append(f"size {im.size} != expected {(exp_w, exp_h)}")
        arr = np.asarray(im)
        if float(arr.std()) < 6.0:
            res["fails"].append(f"near-uniform image (std {arr.std():.1f}) — dead or empty render")

        # FRAME BALANCE / DEAD LOWER ZONE (2026-07-26). The series' longest-
        # running craft defect, and the first gate here that judges COMPOSITION
        # rather than legibility. See frame_balance() for why the measurement is
        # a distribution and not a density. Calibrated on all 162 shipped
        # full-size slides: the FAIL tier fires on 10% of them and every slide
        # it fires on is one the scorers named, or (2026-07-17 S09,
        # 2026-07-20 S03, both bottom-40%-empty) one they should have.
        fb = frame_balance(arr)
        if fb is not None:
            ratio, bands = fb
            if ratio < FB_WARN:
                where = f"top {bands[0]:.0%} / mid {bands[1]:.0%} / bottom {bands[2]:.0%} of cells carrying craft"
                msg = (f"top-loaded composition: the bottom third carries {ratio:.0%} of "
                       f"this slide's own average craft density ({where}) -- the dead "
                       f"lower zone. Extend the anchor, run the annotation furniture "
                       f"down, or move the mass; do not answer it with a bigger quiet zone")
                if ratio < FB_FAIL and not rec.get("breather"):
                    res["fails"].append(msg)
                elif rec.get("breather"):
                    res["warns"].append(msg + " [data-breather]")
                else:
                    res["warns"].append(msg)

        # CANVAS HEALTH (2026-07-11, the rendered-3D gates). Two failure modes
        # the DOM/text gates cannot see, both from the GPU-bench research:
        # (1) DEAD CANVAS: a large visible canvas whose pixels are near-uniform
        #     = a WebGL context that failed/never painted (screenshots as flat
        #     ink) or an art draw that silently threw. FAIL: no slide ships a
        #     dead art layer. A canvas that COULD NOT be sampled (no
        #     preserveDrawingBuffer) on a slide whose full-frame std is healthy
        #     only WARNs (the whole-image gate above still backstops it).
        # (2) LOW-RES BACKING: the slide contract requires 2x backing
        #     (canvas.width = cssW*2); a big canvas below 1.5x ships visibly
        #     blurry in the PDF (the three.js setSize-order trap). FAIL >=1/4
        #     of the slide below 1.5x; WARN 1.5x-1.9x.
        for cvi in rec.get("canvases", []):
            if cvi.get("area_frac", 0) < 0.25:
                continue
            tag = f"canvas {cvi['w']}x{cvi['h']}@({cvi['x']},{cvi['y']})"
            br = cvi.get("backing_ratio", 2)
            if br < 1.5:
                res["fails"].append(
                    f"low-res canvas backing ({br}x < 1.5x) on {tag} — 2x contract; ships blurry")
            elif br < 1.9:
                res["warns"].append(
                    f"canvas backing {br}x < 2x on {tag} (contract is 2x)")
            if cvi.get("sample_ok"):
                if cvi.get("variance", -1) >= 0 and cvi["variance"] < 3.0:
                    res["fails"].append(
                        f"dead canvas (pixel variance {cvi['variance']}) on {tag} — "
                        "failed GL context or empty art layer")
            else:
                res["warns"].append(
                    f"unsampleable canvas on {tag} (GL without preserveDrawingBuffer?) — "
                    "verify visually; akthree sets preserveDrawingBuffer for the gate")

        # CANVAS RASTER TEXT (2026-07-19, WARN only). Text drawn via canvas
        # fillText/strokeText is a raster bitmap: invisible to render.py's DOM
        # walk, to copy_sync_check (unless the string is an authored copy.json
        # record), to the LinkedIn ranker, and to accessibility, and it pixelates
        # in the vector PDF. render.py's init-script hook captured every drawn
        # string; warn on the MEANINGFUL ones (>= 4 alphabetic chars, so axis
        # ticks / short unit labels / numbers do not trip it), pointing the
        # author to move real labels to DOM/SVG. Never a FAIL: aklabel-style
        # in-scene labels are legitimate, but the raster-text cost is worth a
        # visible note. (2026-07-19: S7 loop labels + S8 annotations were
        # cx.fillText and only caught by hand.)
        seen_ct = set()
        for ct in rec.get("canvas_text", []):
            s = (ct.get("text") or "").strip()
            if s in seen_ct:
                continue
            seen_ct.add(s)
            if sum(c.isalpha() for c in s) >= 4:
                res["warns"].append(
                    f"canvas raster text '{s[:40]}' drawn via {ct.get('fn', 'fillText')} "
                    "-- ships as a bitmap in the vector PDF (invisible to the LinkedIn "
                    "ranker, copy_sync, and accessibility); move meaningful labels to DOM/SVG")

        for e in rec.get("page_errors", []):
            res["fails"].append(f"page error: {e}")
        for e in rec.get("console_errors", []):
            res["warns"].append(f"console error: {e}")
        for f in rec.get("fonts_missing", []):
            sty = f.get("style", "normal")
            styd = "" if sty in ("normal", None) else f" {sty}"
            res["fails"].append(f"font not loaded: {f['family']} w{f['weight']}{styd}")
        if rec.get("body_overflow"):
            res["fails"].append("body overflow (page scrolls beyond canvas)")
        for wr in rec.get("overflow_warnings", []):
            level = res["warns"] if wr["kind"] == "tiny-text" else res["fails"]
            level.append(f"{wr['kind']}: '{wr['text'][:50]}' ({wr['detail']})")

        # SVG LABEL OFF ITS OWN PLATE (2026-07-29). render.py measures every
        # SVG <text> against the <rect> painted under it. A label that spills
        # past its knockout is not a style choice: the plate exists precisely
        # because the artwork behind it cannot carry type, so every pixel that
        # escapes lands on unreadable ground, and a chip's border rule ends up
        # drawn through a letterform. 2px of tolerance absorbs subpixel bbox
        # rounding; anything past that is the arithmetic being wrong.
        for sp in rec.get("svg_plates", []):
            cov = sp.get("covered_px")
            dom = sp.get("dom_cover_frac") or 0
            if (cov and cov[0] > 4 and cov[1] > 2) or dom > 0.15:
                what = (f"a {cov[0]}x{cov[1]}px opaque rect" if cov
                        else f"an opaque DOM block over {dom:.0%} of its width")
                msg = (f"svg label painted over: '{sp['text'][:40]}' has "
                       f"{what} drawn on top of it")
                if sp.get("overlap_ok"):
                    res["warns"].append(msg + " [marked data-overlap-ok]")
                elif sp.get("decorative"):
                    res["warns"].append(msg + " [decorative]")
                else:
                    res["fails"].append(msg)
            if sp["overrun_px"] <= 2:
                continue
            o = sp["over"]
            sides = ", ".join(f"{k} {v}px" for k, v in o.items() if v > 2)
            msg = (f"svg label off its plate: '{sp['text'][:40]}' spills {sides}"
                   f" (worst {sp['overrun_px']}px)")
            if sp.get("overlap_ok"):
                res["warns"].append(msg + " [marked data-overlap-ok]")
            elif sp.get("decorative"):
                res["warns"].append(msg + " [decorative]")
            else:
                res["fails"].append(msg)

        # text-on-text overprint (the class of defect no other gate sees).
        # data-overlap-ok marks DELIBERATE layering (e.g., a chip on an
        # opaque plate crossing a display line box): demoted to WARN so the
        # pixel critics still judge it.
        tnodes = rec.get("text_nodes", [])
        for i, j, ratio in text_collisions(tnodes):
            a, b = tnodes[i], tnodes[j]
            msg = (f"text collision ({ratio:.0%} overprint): "
                   f"'{a['text'][:36]}' x '{b['text'][:36]}' "
                   f"near {max(a['x'], b['x'])},{max(a['y'], b['y'])}")
            if a.get("overlap_ok") or b.get("overlap_ok"):
                res["warns"].append(msg + " [marked data-overlap-ok]")
            elif a.get("decorative") or b.get("decorative"):
                res["warns"].append(msg + " [decorative involved]")
            else:
                res["fails"].append(msg)

        for node in rec.get("text_nodes", []):
            if node.get("decorative"):
                continue
            primary = node["font_px"] >= 30
            if (node["x"] < args.safe_margin - 8 or node["y"] < args.safe_margin - 8 or
                    node["x"] + node["w"] > design_w - args.safe_margin + 8 or
                    node["y"] + node["h"] > design_h - args.safe_margin + 8):
                res["warns"].append(
                    f"outside safe zone: '{node['text'][:40]}' at {node['x']},{node['y']} "
                    f"{node['w']}x{node['h']} (margin {args.safe_margin}px)")
            # TEXT UNDER AN OPAQUE PLATE (2026-07-26). render.py's occlusion
            # probe reports the largest patch of a line box that a foreign
            # OPAQUE element provably paints over (paint order confirmed with
            # elementsFromPoint). text_collisions() cannot see this: it
            # compares glyph line boxes, and a padded plate's BACKGROUND is
            # not a line box, so the 2026-07-26 S06 DEAD plate covering the
            # bottom third of a subtitle scored 0.21 against the 0.30 overlap
            # ratio and shipped through two scoring cycles of PASS. Covered
            # type is never a style choice; data-overlap-ok demotes it to WARN
            # so a deliberate layering stays the author's call.
            occ = node.get("occluded")
            if occ:
                ow, oh = occ.get("w", 0), occ.get("h", 0)
                if ow >= OCC_FAIL_W and oh >= OCC_FAIL_H:
                    msg = (f"text under an opaque plate: '{node['text'][:40]}' has a "
                           f"{ow}x{oh}px patch ({occ.get('frac', 0):.0%} of the line box) "
                           f"painted over by .{occ.get('by', '?')}"
                           + (f" '{occ['by_text'][:24]}'" if occ.get("by_text") else "")
                           + " -- move the plate, move the type, or knock the plate out")
                    if node.get("overlap_ok"):
                        res["warns"].append(msg + " [marked data-overlap-ok]")
                    else:
                        res["fails"].append(msg)
                elif ow >= OCC_WARN_W and oh >= OCC_WARN_H:
                    res["warns"].append(
                        f"opaque plate grazing text: '{node['text'][:40]}' has a "
                        f"{ow}x{oh}px patch covered by .{occ.get('by', '?')} -- "
                        f"pixel critic verify no glyph is cut")

            ratio = contrast_estimate(arr, node, scale)
            if ratio is not None:
                if primary and ratio < 2.0:
                    res["fails"].append(f"contrast ~{ratio:.1f} on '{node['text'][:40]}' (est.)")
                elif ratio < 3.5:
                    res["warns"].append(f"low contrast ~{ratio:.1f} on '{node['text'][:40]}' (est.)")
            # canvas/bitmap-under-text tripwire (WARN only): the DOM collision
            # gate cannot see canvas ink, so busy art crossing a text line box
            # is otherwise invisible to the machine (2026-07-10 S3/S4 arcs).
            # 2026-07-25: no longer restricted to primary (>=30px) text. The
            # art-band mono labels that shipped crossed by canvas geometry were
            # 24px, so the size filter meant the only gate that could have seen
            # them never even sampled their boxes.
            busy = busy_art_under_text(arr, node, scale)
            if busy is not None and busy >= BUSY_WARN:
                res["warns"].append(
                    f"busy art under text (bg edge density {busy:.2f}) beneath "
                    f"'{node['text'][:40]}' -- canvas/bitmap may be crossing a "
                    f"text line box; pixel critic verify legibility")

            # LABEL CROSSED BY ART (2026-07-25). The FAIL tier the run of
            # 2026-07-25 needed: foreign ink of the glyphs' own value touching
            # the letterforms across the label = a rule/outline/groove edge
            # struck through the text, whatever layer drew it. A knockout plate
            # or a halo leaves the ring clean, so protected art-band type never
            # trips. data-decorative text is out of scope (skipped above) and
            # data-overlap-ok demotes the FAIL to a WARN, so a deliberate
            # layering stays the author's call.
            gi = glyph_ink_contamination(arr, node, scale)
            if gi is not None:
                gfrac, gext = gi
                if gfrac >= GLYPH_FAIL and gext >= GLYPH_FAIL_EXTENT:
                    msg = (f"label crossed by art ({gfrac:.0%} of the ring around "
                           f"'{node['text'][:40]}' is ink of the glyphs' own value, "
                           f"spanning {gext:.0%} of the label) -- a rule, outline or "
                           f"edge is running through the letterforms; put the label on "
                           f"a knockout plate, halo it, or move the geometry")
                    if node.get("overlap_ok"):
                        res["warns"].append(msg + " [marked data-overlap-ok]")
                    else:
                        res["fails"].append(msg)
                elif gfrac >= GLYPH_WARN:
                    res["warns"].append(
                        f"art touching glyphs ({gfrac:.0%} of the ring around "
                        f"'{node['text'][:40]}', spanning {gext:.0%}) -- pixel critic "
                        f"verify the label is not crossed")

        out["fails"] += len(res["fails"])
        out["warns"] += len(res["warns"])
        out["slides"].append(res)

    out["verdict"] = "FAIL" if out["fails"] else ("WARN" if out["warns"] else "PASS")
    (rdir / "machine_qa.json").write_text(json.dumps(out, indent=2))
    for s in out["slides"]:
        flag = "FAIL" if s["fails"] else ("warn" if s["warns"] else "ok  ")
        print(f"[{flag}] {s['file']}  fails={len(s['fails'])} warns={len(s['warns'])}")
        for f in s["fails"]:
            print(f"    FAIL: {f}")
        for w in s["warns"][:6]:
            print(f"    warn: {w}")
    print(f"verdict: {out['verdict']}  (report -> {rdir / 'machine_qa.json'})")
    sys.exit(1 if out["fails"] else 0)


if __name__ == "__main__":
    main()
