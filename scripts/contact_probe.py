#!/usr/bin/env python3
"""Measure a contact shadow off the RENDER, and write the declaration for it.

WHY THIS EXISTS (2026-08-26, run No.41). Five of that run's nine slides
declared their `data-contacts` rects wrong, in one systematic way: the ground
rect was placed directly BELOW the shadow rect, which lands it at the dark
outer edge of the lit pool while the shadow rect sits near the pool's bright
centre. Three of the five measured NEGATIVE separation -- the declared shadow
was LIGHTER than the declared ground -- and slide 03's declared pair was 118px
from where the marker actually drew. Each was diagnosed by hand with a
throwaway script that profiled a horizontal line through the object's base,
found the cast trough and the pool peak and paired them side by side at the
same y. That script was written and thrown away several times in one run, and
under the five round cap a repair loop that costs a round is a repair loop that
has to become a first-build tool.

Then the other half of the same run: the declarations that DID fail the 4.0 L*
floor were repaired by widening the pool and deepening the cast until they
measured plus thirty, and five pixel critics read the result as a detached
black hole inside a spotlight with no light source. A gate floor was treated as
a target. So this prints the structure as well as the number: how far the cast
trough sits from the object's own base (a contact shadow is ATTACHED; a gap is
what reads as a hole), and how wide the lit pool is around it.

It measures in the GATE'S OWN TERMS -- qa.py's CIELAB conversion, at qa.py's
432px feed width, on the same PNG the gate reads -- by importing qa.py rather
than restating it, so a number printed here is the number the gate will report.
It judges nothing and gates nothing. It hands the author a measured rect pair
and the profile it came from.

    # propose a declaration for the object whose base is at design px (872,1044)
    python3 scripts/contact_probe.py --render-dir out/2026-08-26/render \\
        --slide 4 --base 872,1044

    # a LONG foot (a block's cut wall, a slab edge) casts toward the viewer:
    # profile DOWN from the base line instead of along it, or let it pick
    python3 scripts/contact_probe.py --render-dir out/2026-09-27/render \\
        --slide 3 --base 453,1012 --axis v

    # measure every declaration a built deck already carries
    python3 scripts/contact_probe.py --render-dir out/2026-08-26/render \\
        --slides-dir out/2026-08-26/slides --verify

Exit 0 always unless it can't read what it was pointed at. This is a tool,
not a gate: qa.py owns the verdict.
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
QA_PATH = ROOT / ".claude" / "skills" / "carousel-engine" / "qa.py"

# Default declaration size in design px, matching what the decks already write.
RECT_W, RECT_H = 26, 10
# How far either side of the object base to look for the CAST, and then for the
# lit GROUND to pair it with. The cast window is deliberately tight: a contact
# shadow is attached to its object, so the darkest pixel 150px away is some
# other piece of art and pairing with it is how a declaration ends up 118px
# from where the marker actually drew. The ground window is wider, because the
# lit pool that gives the cast something to subtract from is wider, but it is
# still bounded to the object's own plate rather than the whole frame.
CAST_SPAN = 48
SPAN = 96
# A contact shadow is attached. Past this many design px between the object
# base and the darkest point of its cast, the cast reads as a separate object.
DETACH_PX = 24
# The vertical read (2026-09-27, run No.70). For an object whose foot is a LONG
# line across the frame -- a DEM block's cut wall standing on a table, a slab
# edge -- the horizontal search reads along the object's own base and finds no
# pool, because the cast and the lit ground are stacked in FRONT of the foot,
# down the frame. No.70's slides 01 and 03 read dL 1.6 and 3.7 ("floats") that
# way; profiled downward they read 17.9 and 16.3, which qa.py confirmed. The
# cast must start within DETACH_PX below the base; lit ground within VSPAN.
VSPAN = 64
# THE OBJECT'S OWN COLOUR (2026-10-11, weekly machine pass). Both reads take the
# BRIGHTEST pixels in their window as the lit ground, and an object's lit face
# is often the brightest thing there. Three runs in four days proposed a ground
# rect ON the object: No.81 slide 01 (the tag face, dL 59 for a cast the silt
# shows at dL 6.5), No.83 slide 09 (the card's lit corner) and No.84 slide 09
# (the gold can's lit side, dL 59.5 against a cast that reads 13 down from the
# foot). So the probe samples the object just above the base, and a ground rect
# whose pixels share that colour is on the object, not the ground: auto takes
# the other axis when it is clear, and either way the note says so. The sample
# is trusted only when it is one albedo (an L* spread under OBJ_SPREAD); a pole
# thinner than the sample, or a base given below the foot, mixes surfaces and
# gives no verdict, so the probe then behaves exactly as it did before.
OBJ_SAMPLE_W = 12      # design px across, centred on the base x
OBJ_SAMPLE_H = 18      # design px tall ...
OBJ_SAMPLE_GAP = 4     # ... ending this far above the base (skips the antialiased foot)
OBJ_SPREAD = 10.0      # L* p90 minus p10 above which the sample is not one surface
OBJ_DE = 12.0          # CIELAB distance, L* at HALF weight (shading moves L*, albedo moves a*b*)
OBJ_FRAC = 0.30        # share of a ground rect's pixels that match: the rect is on the object
# Measured on the defects and on No.84's nine good declarations: on-object
# ground rects matched 0.35 to 0.72 of their pixels, every lit-ground rect a
# probe kept matched 0.00 to 0.25 (tests/contact_probe_verify.py, case 5).


def load_qa():
    spec = importlib.util.spec_from_file_location("ak_qa", QA_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


QA = load_qa()


class Frame:
    """One rendered slide, in the gate's colour space at the gate's feed width."""

    def __init__(self, png, design_w, design_h):
        im = Image.open(png).convert("RGB")
        self.s = QA.FEED_W / float(design_w)
        feed = im.resize((QA.FEED_W, max(1, int(round(design_h * self.s)))),
                         Image.LANCZOS)
        self.rgb = np.asarray(feed)
        self.lab = QA._srgb_to_lab(self.rgb)
        self.L = self.lab[..., 0]
        self.design_w, self.design_h = design_w, design_h

    def median_L(self, rect):
        """Median L* of a design-px rect, exactly as qa.contact_reads takes it."""
        x, y, w, h = rect
        x0, y0 = max(0, int(x * self.s)), max(0, int(y * self.s))
        x1 = min(self.L.shape[1], int((x + w) * self.s))
        y1 = min(self.L.shape[0], int((y + h) * self.s))
        if x1 <= x0 or y1 <= y0:
            return None, 0
        band = self.L[y0:y1, x0:x1]
        return float(np.median(band)), band.size

    def lab_px(self, rect):
        """The CIELAB pixels of a design-px rect at feed scale, as (n, 3)."""
        x, y, w, h = rect
        x0, y0 = max(0, int(x * self.s)), max(0, int(y * self.s))
        x1 = min(self.L.shape[1], int((x + w) * self.s))
        y1 = min(self.L.shape[0], int((y + h) * self.s))
        if x1 <= x0 or y1 <= y0:
            return np.zeros((0, 3))
        return self.lab[y0:y1, x0:x1].reshape(-1, 3)

    def profile(self, cy, h, cx, span):
        """Median L* per column across a horizontal band, in design px.

        Returns (xs, ls): xs are design-px column centres, ls the median L* of
        the band at each. This is the line the hand-written scripts drew.
        """
        y0 = max(0, int(cy * self.s))
        y1 = min(self.L.shape[0], max(y0 + 1, int((cy + h) * self.s)))
        x0 = max(0, int((cx - span) * self.s))
        x1 = min(self.L.shape[1], int((cx + span) * self.s))
        if x1 <= x0:
            return np.zeros(0), np.zeros(0)
        cols = np.median(self.L[y0:y1, x0:x1], axis=0)
        cols = smooth3(cols)  # a 3px mean, so one stray feed pixel is not a trough
        xs = (np.arange(x0, x1) + 0.5) / self.s
        return xs, cols


def smooth3(a):
    """A 3-sample mean with EDGE padding. np.convolve(mode="same") pads with
    zeros, which pulls the first and last samples a third of the way to L*=0:
    on a vertical read the first row IS the base line, so that fake dark end
    beat the real cast in the argmin and put the shadow rect on the foot."""
    if a.size < 3:
        return a
    return np.convolve(np.pad(a, 1, mode="edge"), np.ones(3) / 3.0, mode="valid")


def vprofile(fr, cx, w, y0, span):
    """Median L* per ROW across a band w design px wide centred on cx, from y0
    down span design px. Returns (ys, ls), ys in design px row centres."""
    x0 = max(0, int((cx - w / 2.0) * fr.s))
    x1 = min(fr.L.shape[1], max(x0 + 1, int((cx + w / 2.0) * fr.s)))
    r0 = max(0, int(y0 * fr.s))
    r1 = min(fr.L.shape[0], int((y0 + span) * fr.s))
    if r1 <= r0:
        return np.zeros(0), np.zeros(0)
    rows = smooth3(np.median(fr.L[r0:r1, x0:x1], axis=1))
    return (np.arange(r0, r1) + 0.5) / fr.s, rows


def propose_v(fr, base_x, base_y, span=VSPAN, rect=(RECT_W, RECT_H),
              cast_span=DETACH_PX):
    """The vertical read: the cast just below a long foot, lit ground below it."""
    w, h = rect
    ys, ls = vprofile(fr, base_x, w, base_y, span + h)
    if ys.size < 8:
        return {"error": "the base line falls outside the frame"}
    near = np.where(ys - base_y <= max(cast_span, h))[0]
    if not near.size:
        return {"error": "no ground within the cast window"}
    i_dark = int(near[int(np.argmin(ls[near]))])
    idx = np.where(ys - ys[i_dark] >= h)[0]
    if not idx.size:
        return {"error": "no ground clear of the cast within the span"}
    i_lit = int(idx[int(np.argmax(ls[idx]))])
    sy, gy = float(ys[i_dark]), float(ys[i_lit])
    x = int(round(base_x - w / 2.0))
    # the rect never climbs above the foot onto the object's own face
    shadow = [x, int(round(max(float(base_y), sy - h / 2.0))), w, h]
    ground = [x, int(round(gy - h / 2.0)), w, h]
    ls_med, ns = fr.median_L(shadow)
    lg_med, ng = fr.median_L(ground)
    out = {
        "axis": "v", "shadow": [shadow], "ground": [ground],
        "shadow_L": None if ls_med is None else round(ls_med, 1),
        "ground_L": None if lg_med is None else round(lg_med, 1),
        "px": [ns, ng], "trough_x": round(float(base_x), 1),
        "trough_y": round(sy, 1), "peak_y": round(gy, 1),
        "detach_px": round(max(0.0, sy - base_y), 1),
    }
    if ls_med is not None and lg_med is not None:
        out["dL"] = round(lg_med - ls_med, 1)
    return out


def object_colour(fr, base_x, base_y):
    """The object's own colour, sampled just ABOVE its base: {'lab', 'spread'},
    or None when the sample leaves the frame or is not one surface."""
    rect = (base_x - OBJ_SAMPLE_W / 2.0, base_y - OBJ_SAMPLE_GAP - OBJ_SAMPLE_H,
            OBJ_SAMPLE_W, OBJ_SAMPLE_H)
    if rect[1] < 0:
        return None
    px = fr.lab_px(rect)
    if px.shape[0] < 12:
        return None
    lo, hi = np.percentile(px[:, 0], [10, 90])
    if hi - lo > OBJ_SPREAD:
        return None
    return {"lab": [round(float(v), 1) for v in np.median(px, axis=0)],
            "spread": round(float(hi - lo), 1)}


def on_object(fr, rect, sig):
    """Share of a design-px rect's pixels within OBJ_DE of the object colour."""
    px = fr.lab_px(rect)
    if sig is None or not px.shape[0]:
        return 0.0
    o = np.asarray(sig["lab"])
    d = np.sqrt(((px[:, 0] - o[0]) / 2.0) ** 2 + (px[:, 1] - o[1]) ** 2
                + (px[:, 2] - o[2]) ** 2)
    return float((d <= OBJ_DE).mean())


def _mark_object(fr, rec, sig):
    """Stamp a read with how much of its ground rect is the object itself."""
    if sig is None or "error" in rec or not rec.get("ground"):
        return rec
    frac = on_object(fr, rec["ground"][0], sig)
    rec["ground_on_object"] = round(frac, 2)
    return rec


def best_axis(fr, base_x, base_y, axis="auto", span=None, rect=(RECT_W, RECT_H),
              cast_span=None):
    """'h', 'v', or 'auto': both reads, the higher dL wins, the other is kept.
    span and cast_span left as None take each axis's own default (SPAN and
    CAST_SPAN along the base, VSPAN and DETACH_PX down from it); a value the
    caller passed is honoured on whichever axis reads.

    A read whose ground rect is on the object (object_colour, OBJ_FRAC) loses
    to one whose ground is clear of it, whatever its dL: a dL measured against
    the object's own lit face is not a contact reading. When both or neither
    are on the object, the higher dL wins as before."""
    hk = {"span": SPAN if span is None else span,
          "cast_span": CAST_SPAN if cast_span is None else cast_span}
    vk = {"span": VSPAN if span is None else span,
          "cast_span": DETACH_PX if cast_span is None else cast_span}
    sig = object_colour(fr, base_x, base_y) if fr is not None else None
    if axis == "h":
        return _mark_object(fr, propose(fr, base_x, base_y, rect=rect, **hk), sig)
    if axis == "v":
        return _mark_object(fr, propose_v(fr, base_x, base_y, rect=rect, **vk), sig)
    h = _mark_object(fr, propose(fr, base_x, base_y, rect=rect, **hk), sig)
    v = _mark_object(fr, propose_v(fr, base_x, base_y, rect=rect, **vk), sig)
    dh, dv = h.get("dL"), v.get("dL")
    oh = h.get("ground_on_object", 0.0) >= OBJ_FRAC
    ov = v.get("ground_on_object", 0.0) >= OBJ_FRAC
    if oh != ov and dh is not None and dv is not None:
        win, lose = (v, h) if oh else (h, v)
        win = dict(win)
        win["object_fallback"] = {"axis": lose.get("axis"), "dL": lose.get("dL"),
                                  "ground_on_object": lose.get("ground_on_object"),
                                  "object_lab": sig["lab"]}
    else:
        win, lose = (v, h) if dv is not None and (dh is None or dv > dh) else (h, v)
    if "error" not in lose:
        win = dict(win)
        win["alternative"] = {"axis": lose.get("axis", "h"), "dL": lose.get("dL"),
                              "shadow": lose["shadow"], "ground": lose["ground"]}
    return win


def propose(fr, base_x, base_y, span=SPAN, rect=(RECT_W, RECT_H),
            cast_span=CAST_SPAN):
    """Find the cast trough and the pool peak on the object's own base line."""
    w, h = rect
    xs, ls = fr.profile(base_y, h, base_x, span)
    if xs.size < 8:
        return {"error": "the base line falls outside the frame"}
    near = np.where(np.abs(xs - base_x) <= max(cast_span, w))[0]
    if not near.size:
        return {"error": "no ground within the cast window"}
    i_dark = int(near[int(np.argmin(ls[near]))])
    # The pool peak must be clear of the shadow rect, or the two declarations
    # overlap and the gate measures the same pixels twice.
    keep = np.abs(xs - xs[i_dark]) >= w
    if not keep.any():
        return {"error": "no ground clear of the cast within the span"}
    idx = np.where(keep)[0]
    i_lit = int(idx[int(np.argmax(ls[idx]))])
    sx, gx = float(xs[i_dark]), float(xs[i_lit])
    y = float(base_y)
    shadow = [int(round(sx - w / 2.0)), int(round(y)), w, h]
    ground = [int(round(gx - w / 2.0)), int(round(y)), w, h]
    ls_med, ns = fr.median_L(shadow)
    lg_med, ng = fr.median_L(ground)
    out = {
        "axis": "h", "shadow": [shadow], "ground": [ground],
        "shadow_L": None if ls_med is None else round(ls_med, 1),
        "ground_L": None if lg_med is None else round(lg_med, 1),
        "px": [ns, ng],
        "trough_x": round(sx, 1), "peak_x": round(gx, 1),
        "detach_px": round(abs(sx - base_x), 1),
    }
    if ls_med is not None and lg_med is not None:
        out["dL"] = round(lg_med - ls_med, 1)
    return out


def read_declared(src):
    """The data-contacts entries a slide source carries, as qa.py sees them."""
    b = re.search(r"<body\b[^>]*>", src, re.I | re.S)
    if not b:
        return []
    m = re.search(r"data-contacts\s*=\s*(['\"])(.*?)\1", b.group(0), re.I | re.S)
    if not m:
        return []
    try:
        val = json.loads(m.group(2))
    except Exception:
        return [{"error": "data-contacts does not parse as JSON"}]
    return [val] if isinstance(val, dict) else (val or [])


def notes(rec):
    """The reading, in words. Every line names a defect run No.41 shipped."""
    out = []
    d = rec.get("dL")
    if d is not None:
        if d < QA.CONTACT_FAIL_DL:
            out.append("dL %.1f is under qa.py's %.1f L* floor: the object floats%s"
                       % (d, QA.CONTACT_FAIL_DL,
                          " -- and the shadow is LIGHTER than the ground, which "
                          "is the two rects the wrong way round or the ground "
                          "rect sitting on the pool's dark edge" if d < 0 else ""))
        elif d < QA.CONTACT_WARN_DL:
            out.append("dL %.1f clears the floor but is inside the %.1f L* "
                       "comfort band" % (d, QA.CONTACT_WARN_DL))
        else:
            out.append("dL %.1f reads" % d)
    if rec.get("detach_px", 0) > DETACH_PX:
        out.append("the darkest point of the cast is %.0f design px from the "
                   "object base: a contact shadow is ATTACHED, and a gap this "
                   "size is what five critics called a detached hole in a "
                   "spotlight" % rec["detach_px"])
    n = min(rec.get("px", [99, 99]) or [99, 99])
    if n < 12:
        out.append("a rect this small measures %d feed pixels; qa.py needs 12" % n)
    fb = rec.get("object_fallback")
    if fb:
        out.append("axis %s read dL %s, but %d percent of its ground rect is the "
                   "object's own colour (L*a*b* %s, sampled just above the base): "
                   "that rect is on the object itself, not on lit ground, so this "
                   "is the axis %s read" % (fb["axis"], fb["dL"],
                                     round(100 * (fb["ground_on_object"] or 0)),
                                     fb["object_lab"], rec.get("axis")))
    elif rec.get("ground_on_object", 0.0) >= OBJ_FRAC:
        out.append("%d percent of the ground rect is the object's own colour "
                   "(sampled just above the base): it may be on the object itself "
                   "rather than on lit ground. Look at it before declaring it, and "
                   "move --base to the foot itself if the base line crosses the "
                   "object" % round(100 * rec["ground_on_object"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render-dir", required=True,
                    help="the run's render dir (holds slide-NN.png + render_report.json)")
    ap.add_argument("--slides-dir", help="slide sources, for --verify")
    ap.add_argument("--slide", type=int, help="slide number, for --base")
    ap.add_argument("--base", help="cx,cy in DESIGN px: where the object meets the ground")
    ap.add_argument("--span", type=int, default=None,
                    help="how far to look for the lit ground, design px "
                         "(default %d along the base, %d down from it)" % (SPAN, VSPAN))
    ap.add_argument("--cast-span", type=int, default=None,
                    help="how far to look for the cast under the object, design px "
                         "(default %d along the base, %d down from it)" % (CAST_SPAN, DETACH_PX))
    ap.add_argument("--axis", choices=("h", "v", "auto"), default="auto",
                    help="--base only: h reads along the base line (a compact object), "
                         "v profiles DOWN from it (a long foot), auto reads both and "
                         "proposes the stronger (default)")
    ap.add_argument("--verify", action="store_true",
                    help="measure every declaration the built deck carries")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rdir = Path(args.render_dir)
    rep = rdir / "render_report.json"
    dw, dh = 1080, 1350
    if rep.exists():
        try:
            c = json.loads(rep.read_text()).get("canvas", {})
            dw, dh = int(c.get("width", dw)), int(c.get("height", dh))
        except Exception:
            pass

    def frame(n):
        p = rdir / ("slide-%02d.png" % n)
        if not p.exists():
            print("FAIL: %s missing" % p, file=sys.stderr)
            sys.exit(1)
        return Frame(p, dw, dh)

    out = {"design": [dw, dh], "slides": []}

    if args.base:
        if args.slide is None:
            print("FAIL: --base needs --slide", file=sys.stderr)
            sys.exit(1)
        bx, by = (float(v) for v in args.base.split(","))
        rec = best_axis(frame(args.slide), bx, by, args.axis, args.span,
                        cast_span=args.cast_span)
        rec.update({"slide": args.slide, "base": [bx, by]})
        rec["notes"] = notes(rec)
        out["slides"].append(rec)
    elif args.verify:
        if not args.slides_dir:
            print("FAIL: --verify needs --slides-dir", file=sys.stderr)
            sys.exit(1)
        for p in sorted(Path(args.slides_dir).glob("slide-*.html")):
            n = int(re.search(r"slide-(\d+)", p.name).group(1))
            decls = read_declared(p.read_text(errors="replace"))
            if not decls:
                continue
            fr = frame(n)
            for con in decls:
                rs = (con.get("shadow") or [[0, 0, 0, 0]])[0]
                rg = (con.get("ground") or [[0, 0, 0, 0]])[0]
                ls_med, ns = fr.median_L(rs)
                lg_med, ng = fr.median_L(rg)
                rec = {"slide": n, "what": con.get("what", ""),
                       "declared": {"shadow": rs, "ground": rg},
                       "shadow_L": None if ls_med is None else round(ls_med, 1),
                       "ground_L": None if lg_med is None else round(lg_med, 1),
                       "px": [ns, ng]}
                if ls_med is not None and lg_med is not None:
                    rec["dL"] = round(lg_med - ls_med, 1)
                stacked = rs[1] != rg[1]
                # ... and where the pair SHOULD sit, measured off this render.
                # A stacked pair is also read vertically: for a long foot that
                # is the right read, and the old advice to move it side by side
                # sent the author to a pair that floats.
                base_x = rs[0] + rs[2] / 2.0
                best = best_axis(fr, base_x, rs[1], "auto" if stacked else "h",
                                 args.span, (rs[2] or RECT_W, rs[3] or RECT_H),
                                 cast_span=args.cast_span)
                if not stacked and best.get("ground_on_object", 0.0) >= OBJ_FRAC:
                    # a side-by-side pair whose measured ground is on the
                    # object: read down from the base as well (2026-10-11)
                    best = best_axis(fr, base_x, rs[1], "auto", args.span,
                                     (rs[2] or RECT_W, rs[3] or RECT_H),
                                     cast_span=args.cast_span)
                rec["measured"] = best
                reads = rec.get("dL") is not None and rec["dL"] >= QA.CONTACT_WARN_DL
                if stacked and not reads:
                    rec.setdefault("structure", []).append(
                        "the two rects are at different y (%d vs %d). A pool is "
                        "brightest at its centre, so a ground rect stacked "
                        "under the shadow measures the pool's dark edge and the "
                        "pair reads as no separation. %s" % (rs[1], rg[1],
                            "Profiled DOWN from the base this foot does read "
                            "(dL %s): keep them stacked, at the measured rows."
                            % best.get("dL") if best.get("axis") == "v" else
                            "Put them side by side at the object's own base line."))
                elif stacked:
                    rec.setdefault("structure", []).append(
                        "a vertical pair (ground %d px below the shadow), the right "
                        "read for a long foot whose cast falls toward the viewer; "
                        "it reads, and the measured read below agrees on axis %s"
                        % (rg[1] - rs[1], best.get("axis")))
                if (best.get("axis") == "h" and "trough_x" in best
                        and abs(best["trough_x"] - base_x) > rs[2]):
                    rec.setdefault("structure", []).append(
                        "the darkest point on this line is %.0f px away at x=%.0f, "
                        "not under the declared rect at x=%.0f"
                        % (abs(best["trough_x"] - base_x), best["trough_x"], base_x))
                sig = object_colour(fr, base_x, rs[1])
                if sig is not None and on_object(fr, rg, sig) >= OBJ_FRAC:
                    rec.setdefault("structure", []).append(
                        "the DECLARED ground rect is %d percent the object's own "
                        "colour (L*a*b* %s, sampled just above the shadow rect): "
                        "the gate may be measuring the cast against the object "
                        "itself rather than against lit ground"
                        % (round(100 * on_object(fr, rg, sig)), sig["lab"]))
                rec["notes"] = (notes(rec) + rec.get("structure", [])
                                + [n for n in notes(best) if "object's own colour" in n])
                out["slides"].append(rec)
    else:
        print("FAIL: give either --slide N --base cx,cy or --verify", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(out, indent=2))
        return 0
    for rec in out["slides"]:
        head = "slide %02d" % rec["slide"]
        if rec.get("what"):
            head += "  %r" % rec["what"]
        print(head)
        if "declared" in rec:
            print("  declared  shadow %s  ground %s  ->  shadow L* %s  ground L* %s  dL %s"
                  % (rec["declared"]["shadow"], rec["declared"]["ground"],
                     rec["shadow_L"], rec["ground_L"], rec.get("dL")))
            m = rec.get("measured", {})
            if "shadow" in m:
                print("  measured  shadow %s  ground %s  ->  shadow L* %s  ground L* %s  dL %s  (axis %s)"
                      % (m["shadow"], m["ground"], m["shadow_L"], m["ground_L"],
                         m.get("dL"), m.get("axis")))
        else:
            print("  propose   data-contacts entry:")
            print("    %s" % json.dumps({"what": "<the object standing on the plate>",
                                         "shadow": rec.get("shadow"),
                                         "ground": rec.get("ground")}))
            if rec.get("axis") == "v":
                print("  measured  shadow L* %s  ground L* %s  dL %s  (axis v: cast "
                      "trough at y=%s, lit ground at y=%s)"
                      % (rec["shadow_L"], rec["ground_L"], rec.get("dL"),
                         rec.get("trough_y"), rec.get("peak_y")))
            else:
                print("  measured  shadow L* %s  ground L* %s  dL %s  (axis h: cast "
                      "trough at x=%s, pool peak at x=%s)"
                      % (rec["shadow_L"], rec["ground_L"], rec.get("dL"),
                         rec.get("trough_x"), rec.get("peak_x")))
            alt = rec.get("alternative")
            if alt:
                print("  other axis (%s) reads dL %s" % (alt["axis"], alt["dL"]))
        for n in rec.get("notes", []):
            print("  - " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
