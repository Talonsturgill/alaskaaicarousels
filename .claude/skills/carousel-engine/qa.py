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
  - DECLARED CONTACT SHADOW DOES NOT READ (FAIL): opt-in. A slide may name, on
    <body data-contacts>, the region its contact shadow occupies and the ground
    that shadow is supposed to darken; this measures both at feed scale in
    CIELAB and FAILs below 4.0 L* of separation, WARNs below 8.0. Added
    2026-08-05 after run No.26 made the contact corollary its declared attack,
    built the shadow exactly as specified in #1A0F08 at alpha 0.55, laid it on
    a table already near #0B0906 for a 1.2 L* composite, and shipped an object
    four pixel critics said was floating while machine QA reported 0 fails. A
    shadow is a subtraction and needs something to subtract from; nothing here
    had ever asked whether a declared depth cue survived compositing.
  - LEADER LANDS ON NOTHING (FAIL): opt-in. A slide declares each drafting
    leader in window.__akLeaders as {target, at:[x,y], to:[x,y]} -- the feature's
    own coordinates and where the leader ends -- and this FAILs when the two are
    more than LEADER_LAND_PX apart. Added 2026-08-07 after run No.28's slide 06
    shipped two detail-circle leaders pointing at void through two pixel critics,
    a flow critic and the first scoring cycle: their tails were fixed pixel
    deltas from each circle's own centre, so the target was never named anywhere
    and no reviewer could tell a leader reaching something small from one
    reaching nothing. A pixel test cannot answer it (the landing tick puts ink at
    the terminus); declared arithmetic can.
  - LEADER CARRIES NO LABEL (FAIL): the other end of the same declaration. The
    leader also names `from`, where the line meets its label, and `label`, that
    annotation text verbatim, and this FAILs when the label was never drawn or
    is drawn more than LEADER_LABEL_PX from where the line arrives. Added
    2026-08-14 after run No.33 shipped three annotation elements with no
    terminal value at all (S01's leader off the Rhode Island ring into bare
    sheet, S07's dimension call printing none of its declared values, S08's
    stamp leader descending into empty paper) at PASS, 0 fails, 0 warns, with
    the leader gate returning ok on all three because all three landed on their
    targets. The gate could see one end of its own subject.
  - STALE RENDER (FAIL): render.py records the SHA1 of the source that produced
    each PNG, and this FAILs when that file has changed since. Added 2026-08-14
    after run No.33 applied two repairs to source and then re-rendered a
    different `--only` subset, so both were silent no-ops and the flow critic
    reviewed the pre-repair contact sheet and reported both repairs as still
    broken. Two hashes, so it can't false-fail.
  - DECLARED maxLines EXCEEDED (FAIL): AK.fitText records every call's declared
    {min, max, maxLines} and what the element actually rendered; this FAILS a
    block that set more lines than it declared, or that bottomed out at `min`
    without satisfying its own constraint. Added 2026-08-12 after five slides of
    run No.31 overran their declared line counts (`min` authored higher than the
    box width could hold) and slide 08's three-line clamp swallowed "It is for
    the grid.", the sentence carrying the deck's whole thesis, with machine QA
    reporting PASS, 0 fails, 0 warns. data-fit-overflow had marked the element
    since the helper was written and nothing had ever read it.
  - SELF-ASSERTED MEASUREMENT DISAGREES WITH THE DRAWING (FAIL): opt-in. A slide
    declares, in window.__akAssert, {what, expect, actual, tol} -- what its type
    claims and what its geometry computed -- and this FAILS when the two are
    further apart than the declared tolerance. Added 2026-08-12 after run No.31
    printed an 840px dimension that was exact to the pixel over a scene whose two
    masses were 266px apart (twenty feet drawn as about six) and two map frame
    widths wrong by 7 and 25 percent, all past every gate here.
  - UNSEEDED RANDOMNESS (FAIL): consumes render.py's determinism source scan
    and FAILS a slide whose inline script calls Math.random() or the crypto
    random APIs instead of the seeded AK.rng(seed) / AK.reseed(seed) the slide
    contract requires; clock reads (Date.now, new Date(), performance.now) are
    a WARN. Added 2026-08-01 after a stipple field shipped on Math.random()
    through five render rounds on a deck about a public record, caught by a
    human running grep. Every other check here reads one screenshot, so an
    irreproducible slide is invisible to all of them.
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
import hashlib
import json
import math
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


WORST_CELL_PX = 64      # device-px width of the cell the worst-point walk samples
WORST_MIN_INK = 0.04    # a cell needs this much glyph ink before it is judged
WORST_MIN_BG = 200      # a cell needs this many background pixels to estimate one
WORST_FAIL = 3.0        # worst-cell ratio on primary text that is a FAIL
WORST_WARN = 4.5        # the rubric's own hard-fail line, reported as a WARN below it


def contrast_worst_cell(img_arr, node, scale):
    """Contrast at the WORST POINT of a text node, not averaged over its bbox.

    Added 2026-07-31. contrast_estimate() takes ONE background value, the median
    of the non-ink pixels across the whole bounding box. On a flat ground that is
    right. On a GRADED ground it is the thing that hides the defect: a line set
    across an engraved sheet that runs from dark at one end to lit at the other
    averages to a comfortable ratio while its lit end is unreadable. The rubric's
    hard-fail rule says "below 4.5:1 AT WORST POINT" and the machine gate was
    measuring a mean, so for three runs (2026-07-25, 2026-07-29, 2026-07-31) the
    only reader who caught it was the scorer, at the ship gate, where a fix costs
    a whole revision cycle and caps the score at 6.9.

    Walks each line box in WORST_CELL_PX-wide cells, estimates the background
    from that CELL's own non-ink pixels, and returns the minimum ratio over every
    cell carrying real glyph ink, or None if nothing was measurable. Tightens the
    existing check; it never raises a ratio the old one reported.
    """
    color = parse_css_color(node.get("color"))
    if color is None:
        return None
    lines = node.get("lines") or [[node["x"], node["y"], node["w"], node["h"]]]
    H, W = img_arr.shape[:2]
    lt = rel_luminance(color)
    worst = None
    for bx, by, bw, bh in lines:
        y0, y1 = max(0, int(by * scale)), min(H, int((by + bh) * scale))
        if y1 - y0 < 8:
            continue
        gx0, gx1 = max(0, int(bx * scale)), min(W, int((bx + bw) * scale))
        for cx0 in range(gx0, gx1, WORST_CELL_PX):
            cx1 = min(cx0 + WORST_CELL_PX, gx1)
            if cx1 - cx0 < 16:
                continue
            cell = img_arr[y0:y1, cx0:cx1, :3].astype(float)
            ink = np.abs(cell - np.array(color)).sum(axis=2) < BUSY_INK_DIST
            if ink.mean() < WORST_MIN_INK or ink.mean() > 0.75:
                continue
            bgm = ~_dilate(ink, BUSY_DILATE)
            if int(bgm.sum()) < WORST_MIN_BG:
                continue
            bg = np.median(cell[bgm], axis=0)
            lb = rel_luminance(bg)
            lo, hi = min(lt, lb), max(lt, lb)
            r = (hi + 0.05) / (lo + 0.05)
            worst = r if worst is None else min(worst, r)
    return worst


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


FEED_W = 432          # the thumb width the doctrine's legibility test uses

# NO PASS/FAIL THRESHOLD ON WHETHER AN ENCODING *WORKS*, DELIBERATELY. See
# encoding_reads() for the calibration that killed the two obvious candidates.
# That block MEASURES and does not judge, and anyone adding a quality threshold
# must first show it separates a known-bad encoding from a known-good one on
# real renders.
#
# ENC_DIFFER_MIN_DE IS NOT THAT THRESHOLD. It answers a strictly narrower and
# purely mechanical question -- did the probe measure ANYTHING -- and it is only
# ever applied to a direction THE SLIDE ITSELF DECLARED. See the DIRECTION
# CONTRACT block in encoding_reads() for the fit.
ENC_DIFFER_MIN_DE = 4.0
ENC_READS_VALUES = ("differ", "same")


def _srgb_to_lab(a):
    """sRGB 0..255 -> CIELAB. Written out rather than imported: the engine's
    dependency surface is part of its reliability and slides stay offline."""
    a = a.astype(np.float64) / 255.0
    lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    t = (lin @ m.T) / np.array([0.95047, 1.0, 1.08883])
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], -1)


def _rank_auc(x, y):
    """Mann-Whitney AUC folded to 0.5..1. 0.5 = the two sets are one set."""
    allv = np.concatenate([x, y])
    order = np.argsort(allv, kind="mergesort")
    sv = allv[order]
    ranks = np.empty(len(allv), float)
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    n1 = len(x)
    u1 = ranks[:n1].sum() - n1 * (n1 + 1) / 2.0
    a = u1 / (n1 * len(y))
    return max(a, 1.0 - a)


def encoding_reads(img_arr, enc, design_w, design_h):
    """MEASURE a declared wordless encoding. Deliberately does not judge it.

    Built 2026-07-29 to close the standing artwork-craft weakness (lowest
    criterion in 16 of the first 19 runs) by testing whether a slide's art
    actually carries the argument it claims. Two candidate metrics were
    calibrated against real renders, using that run's own hero as the
    known-bad (the scorer: the column "reads as one uniform amber extrusion",
    its declared steel-below-brass-above material change did not survive) and
    slide 07's sodium-to-slate ownership boundary as the known-good (a turn
    the scorer and the flow critic both called the deck's best fusion beat).

    BOTH METRICS FAILED TO SEPARATE THEM, and in the worst direction:

      known-bad  S03 steel vs brass    dE 49.0  AUC 0.87  visible 58/83 pct
      known-good S07 sodium vs slate   dE 12.2  AUC 0.77  visible 54/53 pct

    Colour separability is HIGHER on the broken encoding than on the working
    one, because the steel really is a different colour where you can see it;
    it just reads as a glassy plinth rather than as half the object. And the
    occlusion fraction is LOWER on the working one, because a deliberate
    composition puts type over its own art. Any threshold drawn through these
    numbers passes the defect and fails the success.

    The real defect is semantic, about shape, proportion and context ("is this
    read as part of the object"), and none of that is a colour statistic. So
    this function returns numbers for the pixel critics and the scorer to read,
    and qa.py raises no FAIL from them. That is the honest state of the art
    here, and it is recorded so the next attempt starts from the evidence
    rather than from the same intuition. Making it a gate needs encoding
    declarations across the back catalogue so a threshold can be FITTED rather
    than guessed, which is a corpus exercise, not a slot at the end of a run.

    THE DIRECTION CONTRACT (2026-08-08). Everything above is still true about
    JUDGING an encoding, and none of it is being softened. What run No.29 proved
    is that a probe can fail one step earlier, before any semantics are in play:
    slides 05 and 06 declared the deck's central wordless claim, the two probe
    rectangles were computed from the STORYBOARD'S CAMERA ARITHMETIC instead of
    measured off a render, and they landed on empty water about 300 design px
    left of where the aperture actually drew. The declaration reported dE 0.9 /
    AUC 0.58, the deck's own build gate never gated anything, and the scorer
    caught it at the ship gate and made it the run's one_sentence_fix. The same
    failure had already happened once earlier in that run, on a probe pair that
    reported the DARK frame as brighter than the lit one.
    The light itself was fine: measured off the shipped pixels the aperture runs
    98.3 L* lit against 26.9 L* unlit. The rectangle was wrong.

    So a slide now says WHICH WAY its declaration should read, and that one word
    is checked:

      "reads":"differ"  the two regions must be tellable apart
      "reads":"same"    an absence or sameness claim; they should match

    A declaration with no `reads` is a FAIL, not a pass. It is the same rule
    caption_check.py applies to a missing --ledger and a missing brand.yaml: a
    check that cannot look is a failure, not a stale green. An encoding that
    states no direction is a number nobody can be wrong about, which is exactly
    what shipped. The repair is one word, and typing it is the point: you cannot
    write "differ" without going and looking at what the render actually did.
    Slides that declare no encoding at all are untouched; the contract stays
    opt-in.

    THE FLOOR IS FITTED, NOT GUESSED, over every data-encodes line in the
    shipped corpus (runs/*/machine_qa.json, 19 declarations across 7 runs):

      the DIFFER claims that worked        dE 12.1, 15.0, 15.7, 15.9, 20.8,
                                              23.7, 24.7, 25.3, 27.6, 31.9, 73.6
      the low cluster, all SAMENESS or
        ABSENCE claims where a small dE
        is the CORRECT answer              dE 0.4 'three ticks stand alone with
                                              nothing drawn between them',
                                              1.6, 2.2, 4.6 'three equal
                                              swellings on a bare plate', 4.9
      the known DEFECT, run No.29          dE 0.9 and dE 3.5, both probes off
                                              their own aperture

    4.0 sits under every confirmed working differ claim by a factor of three and
    over the run No.29 defect, and the low cluster is not in its way because
    those claims declare "same" and are not gated. Note what this floor
    deliberately does NOT do: the 2026-07-29 known-bad, the steel-below-brass
    column the scorer said read as one uniform extrusion, measured dE 49.0 and
    PASSES here, correctly, because this is not a judgment of whether the
    encoding works. The calibration above still stands; nothing here revisits it.
    No threshold is drawn for "same", because the corpus has no known-bad for
    that direction to fit one against, and guessing is what this docstring
    exists to prevent.

    Returns (verdict, detail) where verdict is "info", "warn" or "fail".
    """
    if enc.get("error"):
        return "warn", f"declaration did not parse ({enc['error']})"
    ra, rb = enc.get("a") or [], enc.get("b") or []
    if not ra or not rb:
        return "warn", "declaration names no regions"

    im = Image.fromarray(img_arr)
    s = FEED_W / float(design_w)
    feed = np.asarray(im.resize((FEED_W, max(1, int(round(design_h * s)))), Image.LANCZOS))

    def take(rects):
        out = []
        for r in rects:
            x, y, w, h = r
            x0, y0 = max(0, int(x * s)), max(0, int(y * s))
            x1 = min(feed.shape[1], int((x + w) * s))
            y1 = min(feed.shape[0], int((y + h) * s))
            if x1 > x0 and y1 > y0:
                out.append(feed[y0:y1, x0:x1].reshape(-1, 3))
        return np.concatenate(out) if out else np.zeros((0, 3))

    A, B = take(ra), take(rb)
    va = enc.get("a_visible_frac")
    vb = enc.get("b_visible_frac")
    # Visible AREA, not declared area: a region can be large and still unseen.
    area_a = len(A) * (va if va is not None else 1.0)
    area_b = len(B) * (vb if vb is not None else 1.0)

    bits = []
    if va is not None:
        bits.append(f"visible {va:.0%}/{vb:.0%}")
    bits.append(f"seen {int(area_a)}/{int(area_b)}px at {FEED_W}w")

    if len(A) < 12 or len(B) < 12:
        return "warn", "region too small to measure at feed scale, " + ", ".join(bits)

    la, lb = _srgb_to_lab(A), _srgb_to_lab(B)
    ma, mb = np.median(la, 0), np.median(lb, 0)
    axis = mb - ma
    n = float(np.linalg.norm(axis))
    auc = _rank_auc(la @ axis / n, lb @ axis / n) if n > 1e-9 else 0.5
    bits.insert(0, f"dE {n:.1f}, AUC {auc:.2f}")
    detail = f"'{enc.get('claim', '')}': " + ", ".join(bits)

    # THE DIRECTION CONTRACT. See the docstring for the fit and for why this is
    # not the quality threshold the calibration rejected.
    reads = str(enc.get("reads") or "").strip().lower()
    if reads not in ENC_READS_VALUES:
        said = "nothing" if not reads or reads == "any" else repr(enc.get("reads"))
        return "fail", (
            "the declaration says %s about which way it should read, so no "
            "check on it is possible and the number below is not evidence. Add "
            '"reads":"differ" (the two regions must be tellable apart) or '
            '"reads":"same" (an absence or sameness claim). Measured %s'
            % (said, detail))
    if reads == "differ" and n < ENC_DIFFER_MIN_DE:
        return "fail", (
            "%s. The slide declares reads:\"differ\" and the two regions are "
            "%.1f dE apart at %dpx wide, under the %.1f floor: at feed scale "
            "these are one population, so this probe is measuring the same "
            "thing twice. The usual cause is a region computed from the "
            "storyboard's camera arithmetic rather than MEASURED off a render. "
            "Open the PNG, find where the feature actually drew, and author the "
            "rects from that."
            % (detail, n, FEED_W, ENC_DIFFER_MIN_DE))

    return "info", detail


# CONTACT SHADOW READ THRESHOLDS, in CIELAB L* at feed scale (432px wide).
# FITTED, not guessed, from run No.26 (2026-08-05), the run that produced the
# defect this gate exists to catch:
#
#   known-bad, the shipped defect    #1A0F08 @ a0.55 over #0B0906 -> dL 1.24
#   known-bad, measured in the final renders of the three slides the scorer
#     still called "floating-adjacent" (S01, S06, S09): the whole ground band
#     below the object varies by 1.6 to 2.0 L* end to end, i.e. no dip at all
#   known-half-good, the mid-run repair (a warm ground pool at #2A2118 under
#     the object, then the same shadow) -> dL 4.3 measured in the reconstruction
#     under out/upgrade-2026-08-05/, and the scorer's verdict on it was
#     "half landed"
#   known-GOOD, measured in the shipped render of slide 04, whose bar-base
#     shadows the scorer and the pixel critics called convincing: dL 8.1 at
#     both bars (shadow L* 81.7 / 82.7 against paper at L* 89.8 / 90.7)
#
# So FAIL below 4.0 sits under everything that has ever read at all and above
# everything that measurably did not, and WARN below 8.0 lands one tenth of an
# L* under the studio's own known-good, which is where a comfort band belongs:
# the half-landed repair warns, the shadow that convinced does not. A JND for
# two large flat patches side by side
# is about 0.4 L*, so 4.0 is an order of magnitude over it: the margin pays
# for the LANCZOS downscale to feed width, the paper tooth and film grain the
# shadow is composited into, and the fact that a blurred shadow has no edge to
# help the eye. Raising these is a tightening and is fine; lowering them is
# the maintainer's call.
# A leader may stop a little short of the feature it points at -- the drafting
# gap is real practice -- but a gap is a few px, not a journey. 24 design px is
# 2.2% of the frame width, comfortably past any intentional gap and far inside
# run No.28's misses (300 and 240 px). Tolerance, not a threshold to tune down.
LEADER_LAND_PX = 24.0


def leader_lands(ld):
    """CHECK A DECLARED LEADER AGAINST ITS DECLARED TARGET (2026-08-07).

    Run No.28's slide 06 shipped two drafting detail circles whose leader lines
    ran out into empty void, through two pixel critics, a flow critic and the
    first scoring cycle. Nobody was careless: a leader stopping in void looks
    exactly like a leader reaching something small, and the tails were authored
    as fixed pixel deltas from each circle's OWN centre
    (tail:[-70,-70,-150,-150]), so there was no place in the slide, the record
    or the pipeline where the target was ever named. There was nothing to check.

    A PIXEL test cannot answer this and was rejected rather than shipped weak:
    the leader's own landing tick puts ink at its terminus, so "is there ink
    where it ends" is always yes, and any corridor-masked variant of it would
    fire on legitimate art. What the machine CAN check is arithmetic the author
    supplies: where the leader ends, and where the feature it enlarges actually
    is. Two points, one distance. This is the same shape as the contact-shadow
    and encoding contracts -- opt-in, declared by the slide, failed only when
    the slide contradicts itself -- and the real work it does is in the
    authoring: you cannot write `at:` without going and finding the target's
    coordinates, which is exactly the step the defect skipped.

    Returns (verdict, detail): "fail" (the declaration disagrees with itself),
    "warn" (the declaration is unusable, an authoring error) or "ok".
    """
    name = ld.get("target")
    to, at = ld.get("to"), ld.get("at")
    if not name:
        return "warn", ("a leader was declared with no target name; every "
                        "leader names the feature it points at")
    if not to or not at:
        miss = "to" if not to else "at"
        return "warn", ("leader %r declares no numeric %r point (both `to`, "
                        "where the leader ends, and `at`, the target's own "
                        "coordinates, are required)" % (name, miss))
    d = math.hypot(to[0] - at[0], to[1] - at[1])
    if d > LEADER_LAND_PX:
        return "fail", ("the leader for %r ends at (%g,%g) but that feature is "
                        "declared at (%g,%g), %.0f design px away (tolerance "
                        "%.0f). Author the leader as a world-coordinate "
                        "polyline that terminates ON the target's coordinates, "
                        "not as an offset from the annotation's own centre"
                        % (name, to[0], to[1], at[0], at[1], d, LEADER_LAND_PX))
    return "ok", "leader %r lands %.1fpx from its target" % (name, d)


# A leader stops a drafting gap short of the WORDS as well as of the feature.
# Run No.33's one correctly built leader (slide 06, "RINGS OVERLAP FROM HERE")
# meets its label 5 design px below the label's own line box, and the three
# broken ones missed by 150 to 506 px. 32 design px is 3 percent of the frame
# width, several times any real gap and nowhere near any real miss. Tolerance,
# not a threshold to tune down.
LEADER_LABEL_PX = 32.0


def _norm_label(s):
    return " ".join((s or "").split()).upper()


def _point_to_box(px, py, b):
    dx = max(b["x"] - px, 0.0, px - (b["x"] + b["w"]))
    dy = max(b["y"] - py, 0.0, py - (b["y"] + b["h"]))
    return math.hypot(dx, dy)


def leader_labelled(ld, boxes, canvas_strings):
    """THE OTHER END OF THE LEADER, THE ONE CARRYING THE WORDS (2026-08-14).

    The 2026-08-07 contract checks the TARGET end only, so a leader can land
    exactly on its feature and still be pointing at nothing, because the end a
    reader actually reads is the other one. Run No.33 shipped three annotation
    elements with no terminal value at all, S01's leader running off the Rhode
    Island ring into bare sheet, S07's dimension call printing none of the values
    its own dossier type spec declared, and S08's correction-stamp leader
    descending into empty paper. machine_qa returned PASS at zero fails and zero
    warns, the leader gate returned ok on every one of them because every one of
    them landed on its target, and the scorer found all three by reading the
    pictures. The gate was structurally blind to half of its own subject.

    A leader is a sentence with two ends, the feature and the words about it.
    The declaration now names both. `from` is where the leader meets its label
    and `label` is that label verbatim, and this checks the two things a reader
    checks, that the words were really drawn, and that they are really where the
    line arrives.

    LIMIT, stated rather than hidden: position is verified against DOM and SVG
    text boxes, which is where the studio's labels belong and where every label
    on this run's leader slides is. A label found only among the canvas fillText
    strings passes the existence half and WARNs on the position half, because a
    canvas string is recorded with a horizontal span and no line box, so there
    is no honest box to measure to.

    Returns (verdict, detail), verdict in "ok" | "warn" | "fail".
    """
    name = ld.get("target") or "an unnamed leader"
    frm, label = ld.get("from"), ld.get("label")
    if not label:
        return "fail", ("the leader for %r declares no `label`, so nothing "
                        "states what it is pointing the reader AT. Every leader "
                        "ends in words. Declare `label` as the annotation text "
                        "verbatim and `from` as the point where the line meets "
                        "it, or delete the line" % name)
    if not frm:
        return "fail", ("the leader for %r declares the label %r and no `from`, "
                        "the point where the line meets that label, so its "
                        "reading end can't be checked" % (name, label))
    want = _norm_label(label)
    hits = [b for b in boxes if want in b["norm"] or (b["norm"] and b["norm"] in want)]
    if not hits:
        if any(want in c or (c and c in want) for c in canvas_strings):
            return "warn", ("the leader for %r carries the label %r, drawn on a "
                            "canvas. Its existence is confirmed and its POSITION "
                            "is not, because a canvas string has no line box. "
                            "Set the label as DOM or SVG text to have it checked"
                            % (name, label))
        return "fail", ("the leader for %r declares the label %r and no text on "
                        "the slide reads that, so the line ends in bare sheet. "
                        "This is the run No.33 defect, three leaders shipped "
                        "with no terminal value through a PASS at zero fails"
                        % (name, label))
    d = min(_point_to_box(frm[0], frm[1], b) for b in hits)
    if d > LEADER_LABEL_PX:
        return "fail", ("the leader for %r arrives at (%g,%g) but its label %r "
                        "is drawn %.0f design px away (tolerance %.0f), so the "
                        "line and the words it belongs to are not connected on "
                        "the page" % (name, frm[0], frm[1], label, d,
                                      LEADER_LABEL_PX))
    return "ok", "leader %r meets its label %.1fpx away" % (name, d)


def fit_holds(ft):
    """A BLOCK MUST NOT SET MORE LINES THAN IT DECLARED (2026-08-12).

    AK.fitText's contract is "shrink until this fits `maxLines` line boxes with
    no horizontal overflow"; when even `min` cannot satisfy that it clamps to
    `min`, marks the element data-fit-overflow="1" and returns fit:false. That
    attribute has existed since the helper was written and NOTHING has ever read
    it, so for every run to date an explicitly declared constraint has failed in
    silence.

    Run No.31 (2026-08-12) is what it costs. Five slides -- 02, 03, 05, 06 and
    08 -- ran past their declared line counts because `min` was authored higher
    than the box width could ever hold, two numbers picked independently that
    have to agree. On slide 08 the three-line clamp swallowed "It is for the
    grid.", the sentence carrying the deck's entire thesis, and the slide shipped
    arguing only the negative half of its own point. machine_qa returned PASS
    with zero fails and zero warns on that deck.

    This is not a taste threshold and there is nothing to tune: the slide
    declared the number and the render disagreed with it. NOT opt-in, unlike the
    leader/encoding/contact contracts, because the declaration is already there
    in every fitText call the studio has ever written. False positives are
    structurally impossible -- fit:false means the binary search bottomed out and
    `min` itself did not satisfy the author's own constraint.

    Returns (verdict, detail), verdict in "info" | "warn" | "fail".
    """
    if not isinstance(ft, dict):
        return "warn", "a fit record did not parse"
    who = ft.get("id") or ft.get("tag") or "?"
    txt = (ft.get("text") or "").strip()
    ml = ft.get("maxLines")
    lines = ft.get("lines")
    size, mn, mx = ft.get("size"), ft.get("min"), ft.get("max")
    label = "%s '%s'" % (who, txt[:44])
    if not isinstance(ml, (int, float)) or not isinstance(lines, (int, float)):
        return "warn", "fit record for %s carries no line counts" % label
    over_lines = lines > ml
    if ft.get("fit") is False or over_lines:
        why = ("it set %d lines against maxLines %d" % (lines, ml) if over_lines
               else "it could not fit maxLines %d without overflowing its box" % ml)
        # overflow_y is reported but NOT narrated: fitText only enforces height
        # on a box the author capped (fixed height + overflow hidden/clip), and
        # a normal auto-height block reports overflowY true as a matter of
        # course. Saying so in a failure message would be noise that reads like
        # a second defect.
        extra = " and overflows the box horizontally" if ft.get("overflow_x") else ""
        return "fail", (
            "AK.fitText bottomed out on %s: %s%s, at %spx (min %s, max %s). "
            "The fitter clamped to `min` rather than obeying the "
            "declaration, which is silent by design and is what shipped the "
            "2026-08-12 deck missing a whole sentence. `min` is authored higher "
            "than this box width can hold: widen the box or lower `min`."
            % (label, why, extra, size, mn, mx))
    return "info", "%s fits %d/%s lines at %spx" % (label, lines, ml, size)


def assert_holds(a):
    """A SLIDE'S PRINTED NUMBER AGAINST THE GEOMETRY THAT DREW IT (2026-08-12).

    Run No.31's slide 05 printed an 840px dimension rule that was exact to the
    pixel over a scene whose two masses were 266px apart, so the deck's one
    load-bearing measurement -- twenty feet -- was drawn as about six. Every gate
    passed it and it took a forensic human read to catch. The same run printed
    two map frame widths as typed constants that were wrong by 7 and 25 percent
    against the projections that actually drew the maps. One defect in two
    costumes: a NUMBER IN TYPE and the GEOMETRY IT NAMES, computed independently.

    The repair that worked on slide 05 was structural (solve the camera FROM the
    lock, so one number produces both the rule and the room) and structural
    repairs cannot be gated in general. What CAN be gated is the slide stating
    the relationship and the machine checking the slide against itself, which is
    what slide 07 improvised for its mark count via window.__akMarkCount and
    which caught 189 and then 196 before landing on an exact 200 -- except that
    it console.error'd, so it was a WARN and only worked because a human was
    watching. Here it is a FAIL.

    Opt-in and pure arithmetic on two numbers the slide supplied, so it cannot
    speak about art it does not understand, and a slide declaring nothing is not
    judged. The real work is in the authoring: `actual` has to be derived from
    whatever actually drew.

    Returns (verdict, detail), verdict in "info" | "warn" | "fail".
    """
    what = a.get("what")
    exp, act, tol = a.get("expect"), a.get("actual"), a.get("tol")
    if not what:
        return "warn", ("an assertion was declared with no `what`; every "
                        "assertion names the relationship it is locking")
    if exp is None or act is None:
        miss = "expect" if exp is None else "actual"
        return "warn", ("assertion %r declares no numeric `%s` (both are "
                        "required: `expect` is what the type claims, `actual` "
                        "is what the drawing computed)" % (what, miss))
    if tol is None:
        return "warn", ("assertion %r declares no `tol`; state the tolerance "
                        "you are willing to ship, in the same unit" % what)
    unit = (" " + a["unit"]) if a.get("unit") else ""
    d = abs(exp - act)
    if d > abs(tol):
        return "fail", (
            "%r: the slide claims %g%s and the drawing produced %g%s, %g%s "
            "apart against a declared tolerance of %g%s. The type and the "
            "geometry were computed independently; derive one FROM the other so "
            "they cannot disagree."
            % (what, exp, unit, act, unit, d, unit, abs(tol), unit))
    return "info", ("%r holds: %g vs %g%s (within %g)"
                    % (what, exp, act, unit, abs(tol)))


CONTACT_FAIL_DL = 4.0
CONTACT_WARN_DL = 8.0


def contact_reads(img_arr, con, design_w, design_h):
    """MEASURE a declared contact shadow against the ground it claims to darken.

    Built 2026-08-05. Every other gate here judges legibility, collision or
    composition. Nothing asked whether a declared DEPTH CUE survived
    compositing, so the run that made the contact edge its whole declared
    attack shipped a shadow worth 1.2 L* on top of a near-black table, four
    pixel critics reported the object floating, and machine QA returned zero
    fails. A shadow is a subtraction; it needs something to subtract from.

    Unlike encoding_reads() this one DOES fail, and the reason it can is that
    the question is one-dimensional and the slide asked it itself. "Is this
    region darker than that region" needs no semantics, no shape reading and
    no taste. A FAIL here is the slide contradicting its own declaration.

    Returns (verdict, detail), verdict in "info" | "warn" | "fail".
    """
    if con.get("error"):
        return "warn", "declaration did not parse (%s)" % con["error"]
    rs, rg = con.get("shadow") or [], con.get("ground") or []
    if not rs or not rg:
        return "warn", "declaration names no shadow/ground region"

    im = Image.fromarray(img_arr)
    s = FEED_W / float(design_w)
    feed = np.asarray(im.resize((FEED_W, max(1, int(round(design_h * s)))), Image.LANCZOS))

    def take(rects):
        out = []
        for r in rects:
            x, y, w, h = r
            x0, y0 = max(0, int(x * s)), max(0, int(y * s))
            x1 = min(feed.shape[1], int((x + w) * s))
            y1 = min(feed.shape[0], int((y + h) * s))
            if x1 > x0 and y1 > y0:
                out.append(feed[y0:y1, x0:x1].reshape(-1, 3))
        return np.concatenate(out) if out else np.zeros((0, 3))

    S, G = take(rs), take(rg)
    what = con.get("what", "") or "contact shadow"
    if len(S) < 12 or len(G) < 12:
        return "warn", ("'%s': region too small to measure at feed scale "
                        "(%d/%d px at %dw)" % (what, len(S), len(G), FEED_W))

    ls = float(np.median(_srgb_to_lab(S)[..., 0]))
    lg = float(np.median(_srgb_to_lab(G)[..., 0]))
    d = lg - ls
    bits = "'%s': shadow L* %.1f vs ground L* %.1f, dL %.1f at %dw" % (
        what, ls, lg, d, FEED_W)

    if d < CONTACT_FAIL_DL:
        extra = ""
        if lg < 12.0:
            # The exact shape of the No.26 defect, named so the fix is obvious.
            extra = (" -- the ground is already near black (L* %.1f), so there "
                     "is nothing left to subtract; light the ground first "
                     "(a warm pool under the object), then cast the shadow"
                     % lg)
        return "fail", bits + (" -- below the %.1f L* floor, the object floats"
                               % CONTACT_FAIL_DL) + extra
    if d < CONTACT_WARN_DL:
        return "warn", bits + (" -- under the %.1f L* comfort band; it reads, "
                               "barely" % CONTACT_WARN_DL)
    return "info", bits


# THE AXIS CENSUS (2026-08-16). Geometry tolerances, in design px. None of
# these is an ink threshold: the census calibrates its ink level on the marks
# the SLIDE declares, so there is no constant here to tune down or up.
CENSUS_PEAK_R = 4      # search radius around a declared mark for its own ink
CENSUS_JOIN_PX = 6     # runs closer than this are one mark, not two
CENSUS_MIN_W = 2       # a run narrower than this is an anti-aliased edge
CENSUS_MATCH_PX = 12   # a run this close to a declared mark IS that mark
CENSUS_TEXTURE_N = 10  # runs beyond 3x declared + this: the band is texture


def _census_value(sc, p):
    (p0, v0), (p1, v1) = sc["from"], sc["to"]
    if p1 == p0:
        return None
    return v0 + (p - p0) * (v1 - v0) / float(p1 - p0)


def _census_fmt(v, unit):
    if v is None:
        return "an unreadable value"
    s = ("{:,.2f}".format(v) if abs(v) < 100 and v != int(v)
         else "{:,.0f}".format(v))
    return (s + " " + unit).strip()


def axis_census(img_arr, sc, design_w, design_h):
    """A MARK ON A MEASURED AXIS IS A QUANTITY, WHATEVER IT WAS DRAWN FOR.

    Run No.35 shipped the same defect twice in one deck and every machine gate
    passed both. Slide 07 set three gold place ticks under a rail whose x axis
    means DOLLARS, so three REGIONS were printed at three dollar positions and
    invited a dollar reading of them. Slide 02 set thirteen division ticks on a
    money rail, implying twelve equal months across a budget period that is ten
    months long. Two pixel critics found them by reading the pictures. Nothing
    mechanical could, because nothing in the run had ever written down that the
    axis was quantitative or what was sitting on it.

    So a slide with a measured axis declares it (see render.py's data-scale
    block) and enumerates the marks in its band. This checks three things:

      1. ARITHMETIC. A declared mark outside its own span is a FAIL. A mark
         with an empty `means` is a FAIL, and that is the whole point of the
         contract: on a measured axis there is no such thing as a decorative
         tick, so an author who cannot say what a mark means has found the
         defect. The value each mark reads as is PRINTED, which is the second
         forcing function -- "this tick reads as 118,000,000 dollars" is hard
         to leave in once you have seen it.

      2. THE PIXEL CENSUS. The band is sampled off the render, and any run of
         ink in it that is not within CENSUS_MATCH_PX of a declared mark is
         reported with the value its position reads as. This is what catches
         the mark nobody thought to declare, which is the actual defect both
         times.

      3. Nothing else. It does not judge whether a mark is well drawn, whether
         the scale is a good idea, or whether the axis is linear (it assumes
         linear between `from` and `to`, and a log axis must not declare one).

    THE CENSUS CALIBRATES ON THE SLIDE'S OWN INK, not on a constant, and it is
    built to UNDER-report. Two decisions, both measured against this run's real
    slide 04 (a rail with five $50M ticks hanging into a stippled plain, which
    is exactly the textured band a naive census drowns in):

      the profile is the MEDIAN down the band, not the mean. A tick crosses the
      whole band and holds its median; a stipple field is mostly empty in any
      one column and does not. Mean flagged 7 texture clusters on that slide,
      median 4.
      the threshold is the WEAKEST DECLARED MARK'S OWN INK, not a fraction of
      it. Half of it flagged 4 clusters; the full value flags 1, the notch at
      the rail's left end, which is a real mark on that axis and should be
      declared. The reconstruction of the run No.35 defect (three undeclared
      place ticks on a dollar rail) fails at every setting tried.

    So the rule is "ink in the band at least as strong as a mark you already
    admitted to, somewhere you did not declare". A mark fainter than your own
    weakest is not found. That is the right direction for a hard fail: it can
    miss, it should not invent. There is no constant here for a later run to
    quietly lower, and the stated limit is that a scale declaring NO marks
    cannot be calibrated and gets an info line instead of a census. Declaring
    one mark is what buys the check, which is the right incentive.

    Returns (verdict, detail), verdict in "info" | "warn" | "fail".
    """
    if sc.get("error"):
        return "warn", "declaration did not parse (%s)" % sc["error"]
    what = sc.get("what") or "a measured axis"
    axis = (sc.get("axis") or "x").lower()[:1]
    unit = sc.get("unit") or ""
    frm, to, band = sc.get("from"), sc.get("to"), sc.get("band")
    ok = (axis in ("x", "y") and isinstance(frm, list) and isinstance(to, list)
          and len(frm) == 2 and len(to) == 2 and isinstance(band, list)
          and len(band) == 2)
    if ok:
        try:
            frm = [float(frm[0]), float(frm[1])]
            to = [float(to[0]), float(to[1])]
            band = [float(band[0]), float(band[1])]
        except (TypeError, ValueError):
            ok = False
    if not ok or abs(to[0] - frm[0]) < 40 or band[1] - band[0] < 4:
        return "warn", ("'%s': the scale declaration is unusable. It needs "
                        '"axis":"x" or "y", "from":[px,value], "to":[px,value] '
                        'at least 40px apart, and "band":[px,px], the strip '
                        "the scale owns across the axis" % what)
    sc = dict(sc, **{"from": frm, "to": to, "band": band})

    lo, hi = min(frm[0], to[0]), max(frm[0], to[0])
    marks, bad, nameless = [], [], []
    for m in sc.get("marks") or []:
        at = m.get("at")
        if not isinstance(at, (int, float)):
            return "warn", ("'%s': a declared mark has no numeric `at`, the "
                            "position it is drawn at on this axis" % what)
        if at < lo - CENSUS_MATCH_PX or at > hi + CENSUS_MATCH_PX:
            bad.append(at)
        if not (m.get("means") or "").strip():
            nameless.append(at)
        marks.append(float(at))

    if nameless:
        return "fail", (
            "'%s': %d mark(s) on this axis declare no meaning, at %s. The axis "
            "is measured, so every mark on it is read as a quantity: these sit "
            "at %s. A mark that means nothing is not decoration here, it is a "
            "number the reader will believe. Give it a meaning or draw it "
            "outside the band."
            % (what, len(nameless), ", ".join("%g" % p for p in nameless),
               ", ".join(_census_fmt(_census_value(sc, p), unit)
                         for p in nameless[:4])))
    if bad:
        return "fail", (
            "'%s': %d declared mark(s) sit off the axis they are declared on "
            "(at %s, span %g..%g). Either the mark is not on this scale or the "
            "scale's own endpoints are wrong; both are worth knowing before a "
            "reader measures against them."
            % (what, len(bad), ", ".join("%g" % p for p in bad), lo, hi))

    if not marks:
        return "info", ("'%s': axis declared over %s to %s with no marks on "
                        "it, so there is nothing to calibrate a pixel census "
                        "against; the band is not checked"
                        % (what, _census_fmt(frm[1], unit),
                           _census_fmt(to[1], unit)))

    # THE PIXEL CENSUS. Sample the band off the render at native resolution and
    # profile it along the axis.
    ns = img_arr.shape[1] / float(design_w)
    if axis == "x":
        r0, r1 = int(band[0] * ns), int(band[1] * ns)
        c0, c1 = int(lo * ns), int(hi * ns)
    else:
        r0, r1 = int(lo * ns), int(hi * ns)
        c0, c1 = int(band[0] * ns), int(band[1] * ns)
    r0, c0 = max(0, r0), max(0, c0)
    r1, c1 = min(img_arr.shape[0], r1), min(img_arr.shape[1], c1)
    if r1 - r0 < 4 or c1 - c0 < 8:
        return "warn", ("'%s': the declared band lies outside the frame or is "
                        "too small to sample" % what)
    strip = _srgb_to_lab(img_arr[r0:r1, c0:c1])[..., 0]
    if axis == "y":
        strip = strip.T
    base = float(np.median(strip))
    # MEDIAN down the band, not mean: a mark crosses the band, texture does not.
    prof = np.median(np.abs(strip - base), axis=0)    # one value per native px
    # to design px, then a 3px box smooth (below that it is anti-aliasing)
    n = int(max(1, round(ns)))
    keep = (len(prof) // n) * n
    prof = prof[:keep].reshape(-1, n).mean(axis=1)
    k = np.ones(3) / 3.0
    prof = np.convolve(prof, k, mode="same")
    origin = lo

    def peak_at(p):
        i = int(round(p - origin))
        a, b = max(0, i - CENSUS_PEAK_R), min(len(prof), i + CENSUS_PEAK_R + 1)
        return float(prof[a:b].max()) if b > a else 0.0

    declared_ink = [peak_at(p) for p in marks]
    w = min(declared_ink)
    floor_ = float(np.median(prof))
    if w <= 0.5:
        return "warn", (
            "'%s': the slide declares a mark at %g and there is no measurable "
            "ink within %dpx of it in the band, so the census has nothing to "
            "calibrate on. Either the mark did not draw, or its declared "
            "position is not where it drew."
            % (what, marks[int(np.argmin(declared_ink))], CENSUS_PEAK_R))
    if w <= floor_ * 1.2:
        return "warn", (
            "'%s': the weakest declared mark (ink %.1f) is no stronger than the "
            "band's own texture (%.1f), so no census can separate marks from "
            "art here. Narrow the band to the strip the marks occupy, or draw "
            "the marks so a reader can tell them from the ground."
            % (what, w, floor_))

    thr = w
    runs, start = [], None
    for i, v in enumerate(prof):
        if v >= thr and start is None:
            start = i
        elif v < thr and start is not None:
            runs.append((start, i))
            start = None
    if start is not None:
        runs.append((start, len(prof)))
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] < CENSUS_JOIN_PX:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    merged = [(a, b) for a, b in merged if b - a >= CENSUS_MIN_W]

    if len(merged) > 3 * len(marks) + CENSUS_TEXTURE_N:
        return "warn", (
            "'%s': the declared band holds %d separate runs of ink against %d "
            "declared marks, which is texture rather than a mark field. The "
            "census cannot separate marks here; narrow the band to the strip "
            "the marks actually occupy."
            % (what, len(merged), len(marks)))

    undeclared = []
    for a, b in merged:
        c = origin + (a + b) / 2.0
        if all(abs(c - p) > CENSUS_MATCH_PX for p in marks):
            undeclared.append(c)

    span = "%s at %g to %s at %g" % (_census_fmt(frm[1], unit), frm[0],
                                     _census_fmt(to[1], unit), to[0])
    if undeclared:
        listed = ", ".join(
            "%g (reads as %s)" % (p, _census_fmt(_census_value(sc, p), unit))
            for p in undeclared[:5])
        more = "" if len(undeclared) <= 5 else " and %d more" % (len(undeclared) - 5)
        return "fail", (
            "'%s' runs %s, and the band holds %d mark(s) the slide does not "
            "declare: %s%s. On a measured axis a mark is a quantity whether or "
            "not it was drawn as one. Declare each with what it means, or move "
            "it out of the band."
            % (what, span, len(undeclared), listed, more))
    return "info", ("'%s' runs %s; %d declared mark(s), and the band's census "
                    "finds no others" % (what, span, len(marks)))


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

        # STALE RENDER (2026-08-14). render.py records the hash of the source
        # that made each PNG. If the file on disk has moved on since, this image
        # is not what its HTML says and every verdict below it is about a
        # picture that no longer exists. Run No.33 applied two repairs and then
        # re-rendered a different `--only` subset, so both were silent no-ops
        # and the flow critic reviewed and rejected the pre-repair sheet. Pure
        # arithmetic on two hashes, so it can't false-fail; a report written
        # before this field existed carries no source block and is skipped.
        src = rec.get("source") or {}
        sp, sha = src.get("path"), src.get("sha1")
        if sp and sha:
            try:
                cur = hashlib.sha1(Path(sp).read_bytes()).hexdigest()
            except OSError as e:
                res["warns"].append(
                    "stale render unverifiable, the source recorded for this PNG "
                    f"is no longer readable at {sp} ({e.__class__.__name__}), so "
                    "nothing here can prove the image matches its HTML")
            else:
                if cur != sha:
                    res["fails"].append(
                        f"stale render, {rec['file']} has been edited since this "
                        "PNG was made, so every judgement on this slide is about "
                        "a picture that no longer exists. Re-render it (drop "
                        "--only, or add this slide to it) and re-run qa")

        # DETERMINISM (2026-08-01). render.py scans the slide SOURCE; this is
        # the judgement. Unseeded randomness is a FAIL because it makes the
        # slide unreproducible: a repair pass repaints the field, so the render
        # a pixel critic reviewed is not the render that ships, and the shipped
        # PNG cannot be rebuilt from the committed HTML. AK.rng(seed) is the
        # one-argument replacement. Clock reads are a WARN: usually a timing
        # log, occasionally an animation phase that does feed pixels.
        for nd in rec.get("nondeterminism", []):
            where = f"line {nd['line']}: {nd['snippet']}"
            if nd["tier"] == "hard":
                res["fails"].append(
                    f"unseeded randomness: {nd['api']} in this slide's inline "
                    f"script ({where}) -- the slide contract requires seeded "
                    f"noise (AK.rng(seed) / AK.reseed(seed), seed from the run "
                    f"date) so the same source reproduces the same pixels")
            else:
                res["warns"].append(
                    f"clock read in slide script: {nd['api']} ({where}) -- if it "
                    f"feeds the artwork the slide is not reproducible; pin it to "
                    f"a constant or a seeded value")

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

        # CANVAS TEXT THAT RUNS OFF THE FRAME (2026-08-13). Canvas has no layout
        # engine, so a fillText string longer than the space left to it is simply
        # clipped at the canvas edge with no error, no overflow warning and no
        # DOM node for text_collisions to see. Run No.32 shipped exactly that on
        # slide 08: the authored string was
        #     "MORE THAN 20. TWO READS DISAGREED. C28"
        # and the render printed "MORE THAN 20. TWO READS DISA", severing the
        # claim-id and the entire uncertainty disclosure, on the one slide whose
        # honesty device that stamp WAS. render.py, qa.py, copy_sync_check and
        # aggregate_check all returned clean; the scorer found it by eye.
        #
        # This FAILS rather than warns, because a truncated string is not a taste
        # call: the slide asked for characters the frame did not give it. Only
        # axis-aligned, positively-scaled text is judged (skew/rotation and
        # mirrored transforms are skipped), since those are the cases where the
        # device-space span is exact. Text drawn inside a clip() may be
        # intentionally cropped, which this cannot see, so the check is
        # deliberately confined to the frame boundary itself.
        for ct in rec.get("canvas_text", []):
            if ct.get("skew") or ct.get("dev_right") is None:
                continue
            sx = ct.get("sx")
            if not sx or sx <= 0:
                continue
            cw = ct.get("canvas_w") or 0
            if not cw:
                continue
            s_ct = (ct.get("text") or "").strip()
            if sum(c.isalpha() for c in s_ct) < 4:
                continue
            right, left = ct.get("dev_right"), ct.get("dev_left")
            if right > cw + 0.5:
                res["fails"].append(
                    f"canvas text runs off the frame: '{s_ct[:44]}' ends "
                    f"{right - cw:.0f}px past the right edge and is CLIPPED "
                    "(canvas has no layout engine, so nothing overflows); "
                    "move it inside the margin or shorten it")
            elif left is not None and left < -0.5:
                res["fails"].append(
                    f"canvas text runs off the frame: '{s_ct[:44]}' starts "
                    f"{-left:.0f}px left of the frame and is CLIPPED; "
                    "move it inside the margin")

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

        # DECLARED ENCODING DOES NOT READ (2026-07-29). Opt-in: a slide that
        # declares nothing is not judged here, so this can never block a deck
        # that has not adopted the contract.
        for enc in rec.get("encodings", []):
            verdict, detail = encoding_reads(arr, enc, design_w, design_h)
            if verdict == "fail":
                # THE DIRECTION CONTRACT (2026-08-08). Still not a judgment of
                # whether the encoding WORKS -- no threshold through those
                # numbers survived calibration and none has been added. This
                # fails only when the declaration cannot be checked at all, or
                # when the slide contradicts the direction it declared itself.
                res["fails"].append(f"encoding declaration is not evidence: {detail}")
            elif verdict == "warn":
                # Only an AUTHORING error warns: a declaration that does not
                # parse or names a region nobody can measure.
                res["warns"].append(f"encoding declaration unusable: {detail}")
            else:
                res.setdefault("encodings", []).append(detail)

        # DECLARED CONTACT SHADOW DOES NOT READ (2026-08-05). Opt-in like the
        # encoding contract, so a deck that declares nothing is not judged
        # here. When a slide DOES declare one, the measurement is a hard gate.
        for con in rec.get("contacts", []):
            verdict, detail = contact_reads(arr, con, design_w, design_h)
            if verdict == "fail":
                res["fails"].append("contact shadow does not read: " + detail)
            elif verdict == "warn":
                res["warns"].append("contact shadow: " + detail)
            else:
                res.setdefault("contacts", []).append(detail)

        # A MARK ON A MEASURED AXIS (2026-08-16). Opt-in like the two probes
        # above: a slide that declares no scale is not judged here. When one IS
        # declared, an undeclared mark in its band is a hard fail, because the
        # reader measures it whether or not the studio meant them to. See
        # axis_census() for the calibration and for its stated limit.
        for sc in rec.get("scales", []):
            verdict, detail = axis_census(arr, sc, design_w, design_h)
            if verdict == "fail":
                res["fails"].append("a mark on a measured axis: " + detail)
            elif verdict == "warn":
                res["warns"].append("axis census: " + detail)
            else:
                res.setdefault("scales", []).append(detail)

        # LEADER LANDS ON NOTHING (2026-08-07). Opt-in, and pure arithmetic on
        # two declared points, so it cannot false-positive on an undeclared
        # slide or on art it cannot understand. See LEADER_LAND_PX for why the
        # measurement is a declaration and not a pixel test.
        for ld in rec.get("leaders", []):
            verdict, detail = leader_lands(ld)
            if verdict == "fail":
                res["fails"].append("leader lands on nothing: " + detail)
            elif verdict == "warn":
                res["warns"].append("leader declaration unusable: " + detail)
            else:
                res.setdefault("leaders", []).append(detail)

        # THE READING END OF THE LEADER (2026-08-14). The check above proves the
        # line reaches its feature; this one proves it reaches its WORDS, which
        # is the end run No.33 shipped empty three times through a PASS. See
        # leader_labelled() for the contract and for the canvas limit.
        if rec.get("leaders"):
            lboxes = []
            for t in rec.get("text_nodes", []):
                lboxes.append({"x": t["x"], "y": t["y"], "w": t["w"], "h": t["h"],
                               "norm": _norm_label(t.get("text"))})
            cstrings = [_norm_label(c.get("text"))
                        for c in rec.get("canvas_text", [])]
            for ld in rec["leaders"]:
                verdict, detail = leader_labelled(ld, lboxes, cstrings)
                if verdict == "fail":
                    res["fails"].append("leader carries no label: " + detail)
                elif verdict == "warn":
                    res["warns"].append("leader label unverifiable: " + detail)
                else:
                    res.setdefault("leaders", []).append(detail)

        # BLOCK SET MORE LINES THAN IT DECLARED (2026-08-12). Not opt-in: the
        # declaration is the maxLines argument already present in every
        # AK.fitText call. See fit_holds() for why fit:false cannot false-fail.
        for ft in rec.get("fits", []):
            verdict, detail = fit_holds(ft)
            if verdict == "fail":
                res["fails"].append("declared maxLines exceeded: " + detail)
            elif verdict == "warn":
                res["warns"].append("fit record unusable: " + detail)
            else:
                res.setdefault("fits", []).append(detail)

        # PRINTED NUMBER DISAGREES WITH THE GEOMETRY (2026-08-12). Opt-in, and
        # arithmetic on two numbers the slide itself supplied, so it can never
        # speak about a slide that declares nothing. See assert_holds().
        for a in rec.get("asserts", []):
            verdict, detail = assert_holds(a)
            if verdict == "fail":
                res["fails"].append("self-assertion failed: " + detail)
            elif verdict == "warn":
                res["warns"].append("assertion declaration unusable: " + detail)
            else:
                res.setdefault("asserts", []).append(detail)

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
            # WORST-POINT contrast (2026-07-31). The line above averages the
            # background over the whole box, which passes a line whose lit end is
            # unreadable. This measures the rubric's actual rule.
            wc = contrast_worst_cell(arr, node, scale)
            if wc is not None and (ratio is None or wc < ratio - 0.15):
                if primary and wc < WORST_FAIL:
                    res["fails"].append(
                        f"contrast {wc:.1f} at WORST POINT on '{node['text'][:40]}' "
                        f"(box mean reads {ratio:.1f}) -- the ground under this line "
                        f"is graded; give it a reserve or move it")
                elif wc < WORST_WARN:
                    res["warns"].append(
                        f"worst-point contrast {wc:.1f} on '{node['text'][:40]}' "
                        f"(box mean {ratio:.1f}) -- below the rubric's 4.5 line "
                        f"somewhere along the run of the text")
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
