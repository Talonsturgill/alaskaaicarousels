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
        self.L = QA._srgb_to_lab(self.rgb)[..., 0]
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
        if cols.size >= 3:  # a 3px mean, so one stray feed pixel is not a trough
            k = np.ones(3) / 3.0
            cols = np.convolve(cols, k, mode="same")
        xs = (np.arange(x0, x1) + 0.5) / self.s
        return xs, cols


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
        "shadow": [shadow], "ground": [ground],
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
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render-dir", required=True,
                    help="the run's render dir (holds slide-NN.png + render_report.json)")
    ap.add_argument("--slides-dir", help="slide sources, for --verify")
    ap.add_argument("--slide", type=int, help="slide number, for --base")
    ap.add_argument("--base", help="cx,cy in DESIGN px: where the object meets the ground")
    ap.add_argument("--span", type=int, default=SPAN,
                    help="how far to look for the lit ground, design px")
    ap.add_argument("--cast-span", type=int, default=CAST_SPAN,
                    help="how far to look for the cast under the object, design px")
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
        rec = propose(frame(args.slide), bx, by, args.span,
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
                if rs[1] != rg[1]:
                    rec.setdefault("structure", []).append(
                        "the two rects are at different y (%d vs %d). A pool is "
                        "brightest at its centre, so a ground rect stacked "
                        "under the shadow measures the pool's dark edge and the "
                        "pair reads as no separation. Put them side by side at "
                        "the object's own base line." % (rs[1], rg[1]))
                # ... and where the pair SHOULD sit, measured off this render.
                base_x = rs[0] + rs[2] / 2.0
                best = propose(fr, base_x, rs[1], args.span,
                               (rs[2] or RECT_W, rs[3] or RECT_H),
                               cast_span=args.cast_span)
                rec["measured"] = best
                if "trough_x" in best and abs(best["trough_x"] - base_x) > rs[2]:
                    rec.setdefault("structure", []).append(
                        "the darkest point on this line is %.0f px away at x=%.0f, "
                        "not under the declared rect at x=%.0f"
                        % (abs(best["trough_x"] - base_x), best["trough_x"], base_x))
                rec["notes"] = notes(rec) + rec.get("structure", [])
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
                print("  measured  shadow %s  ground %s  ->  shadow L* %s  ground L* %s  dL %s"
                      % (m["shadow"], m["ground"], m["shadow_L"], m["ground_L"],
                         m.get("dL")))
        else:
            print("  propose   data-contacts entry:")
            print("    %s" % json.dumps({"what": "<the object standing on the plate>",
                                         "shadow": rec.get("shadow"),
                                         "ground": rec.get("ground")}))
            print("  measured  shadow L* %s  ground L* %s  dL %s  (cast trough at "
                  "x=%s, pool peak at x=%s)"
                  % (rec["shadow_L"], rec["ground_L"], rec.get("dL"),
                     rec.get("trough_x"), rec.get("peak_x")))
        for n in rec.get("notes", []):
            print("  - " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
