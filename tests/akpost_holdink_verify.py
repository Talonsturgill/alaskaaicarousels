#!/usr/bin/env python3
"""akpost_holdink_verify.py -- the house grade's gold drift and AKPOST.holdInk
(2026-10-21, weekly machine pass).

WHAT IT RECONSTRUCTS. No.92's critics called the flag gold lemon on 04, 05 and
09 for three rounds. 09 drew its crest before AKPOST.grade; 05's line was a
three.js tube under tone mapping, fog and a sill. Measured here: AKPOST.grade's
defaults move a flat #FFC72C patch about 20 dE76 and turn its Lab hue from 85 to
97 degrees. AKPOST.holdInk turns that hue back and keeps the graded light.

    python3 tests/akpost_holdink_verify.py      # exit 0 = every check holds

  drift     the defect: #FFC72C through the default grade lands 15 dE or more
            from itself, its hue 8 degrees or more toward yellow. If a later
            grade stops doing this, this check FAILS and says the helper may
            no longer be needed.
  hold      after holdInk the patch's hue is within 1.5 degrees of #FFC72C's,
            its L* within 1 of the graded L*, and it sits much nearer the ink.
  shaded    a gold ramp (the ink at 30 to 100 percent over the dark ground,
            graded) keeps its order of lightness after the hold.
  spared    ground, snow, aurora green, an olive ground, copper and a salmon
            orange, all graded alongside, come through byte for byte. (An amber
            the grade carries to within a few degrees of gold moves with it, as
            akpost.js says; `rect` keeps it out.)
  region    with `rect` only the pixels inside it move.
  contract  a bad hex or an unknown option throws.
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

JS = r"""
() => {
  const W = 640, H = 200;
  const PATCHES = { gold: '#FFC72C', snow: '#F4F8FF', aurora: '#3CE6B4', olive: '#6B6B3A',
                    copper: '#B8703C', orange: '#FF8C42' };
  const names = Object.keys(PATCHES);
  const paint = (g) => {
    g.fillStyle = '#070B11'; g.fillRect(0, 0, W, H);
    names.forEach((k, i) => { g.fillStyle = PATCHES[k]; g.fillRect(10 + i * 70, 20, 50, 50); });
    for (let i = 0; i < 10; i++) {          // a shaded gold ramp, 30 to 100 percent
      g.globalAlpha = 0.3 + 0.7 * i / 9; g.fillStyle = PATCHES.gold;
      g.fillRect(10 + i * 40, 120, 30, 30); g.globalAlpha = 1;
    }
  };
  const mk = () => { const c = document.createElement('canvas'); c.width = W * 2; c.height = H * 2;
                     const g = c.getContext('2d'); g.scale(2, 2); paint(g); return g; };
  const G = { w: W, h: H, grain: { amount: 0 }, dither: false, sharpen: 0, vignette: 0 };
  const px = (g, x, y) => Array.from(g.getImageData(x * 2, y * 2, 1, 1).data.slice(0, 3));
  const read = (g) => {
    const o = {}; names.forEach((k, i) => { o[k] = px(g, 35 + i * 70, 45); });
    o.ramp = []; for (let i = 0; i < 10; i++) o.ramp.push(px(g, 25 + i * 40, 135));
    o.ground = px(g, 600, 180); return o;
  };
  const graded = mk(); AKPOST.grade(graded, G);
  const before = read(graded);
  const ret = AKPOST.holdInk(graded, { hex: '#FFC72C' });
  const after = read(graded);
  // region: hold only the left half
  const g2 = mk(); AKPOST.grade(g2, G);
  AKPOST.holdInk(g2, { hex: '#FFC72C', rect: [0, 0, 200, 100] });
  const reg = { inGold: px(g2, 35, 45), rampOutside: px(g2, 25 + 9 * 40, 135) };
  const throws = (f) => { try { f(); return false; } catch (e) { return e instanceof TypeError; } };
  const contract = { hex: throws(() => AKPOST.holdInk(g2, { hex: 'gold' })),
                     unknown: throws(() => AKPOST.holdInk(g2, { hex: '#FFC72C', tol: 9 })) };
  return { before, after, ret, reg, contract };
}
"""


def lab(rgb):
    def lin(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(float(c)) for c in rgb)
    X = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    Y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    Z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856451679 else t / 0.12841854934 + 4 / 29
    fx, fy, fz = f(X), f(Y), f(Z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def hue(rgb):
    L, a, b = lab(rgb)
    return math.degrees(math.atan2(b, a)) % 360


def de(p, q):
    return math.dist(lab(p), lab(q))


def main():
    from playwright.sync_api import sync_playwright
    from render import launch_chromium
    with sync_playwright() as p:
        b = launch_chromium(p)
        pg = b.new_page()
        pg.set_content("<html><body></body></html>")
        pg.add_script_tag(path=str(ROOT / "assets" / "js" / "akpost.js"))
        r = pg.evaluate(JS)
        ver = b.version
        b.close()
    bad = 0

    def ok(label, cond, extra):
        nonlocal bad
        print("  %s  %s  %s" % ("ok  " if cond else "FAIL", label, json.dumps(extra)))
        bad += 0 if cond else 1

    GOLD = [255, 199, 44]
    bf, af = r["before"], r["after"]
    print("Chromium", ver, " holdInk returned", r["ret"])
    ok("drift: the default grade moves #FFC72C 15 dE or more and 8 degrees toward yellow",
       de(bf["gold"], GOLD) >= 15 and hue(bf["gold"]) - hue(GOLD) >= 8,
       {"graded": bf["gold"], "dE": round(de(bf["gold"], GOLD), 1),
        "hue": [round(hue(GOLD), 1), round(hue(bf["gold"]), 1)]})
    ok("hold: the patch's hue returns to within 1.5 degrees of the ink's",
       abs(hue(af["gold"]) - hue(GOLD)) <= 1.5, {"held": af["gold"], "hue": round(hue(af["gold"]), 1)})
    ok("hold: L* stays between the graded L* and the ink's own (the gamut's give)",
       min(lab(bf["gold"])[0], lab(GOLD)[0]) - 0.5 <= lab(af["gold"])[0] <= max(lab(bf["gold"])[0], lab(GOLD)[0]) + 0.5,
       [round(lab(bf["gold"])[0], 1), round(lab(af["gold"])[0], 1), round(lab(GOLD)[0], 1)])
    ok("hold: the patch sits within a third of the graded drift's distance from the ink",
       de(af["gold"], GOLD) <= de(bf["gold"], GOLD) / 3,
       [round(de(bf["gold"], GOLD), 1), round(de(af["gold"], GOLD), 1)])
    Ls = [lab(c)[0] for c in af["ramp"]]
    ok("shaded: the gold ramp keeps its order of lightness",
       all(Ls[i] < Ls[i + 1] + 0.3 for i in range(len(Ls) - 1)), [round(x, 1) for x in Ls])
    spared = {k: (bf[k], af[k]) for k in ("snow", "aurora", "olive", "copper", "orange", "ground")}
    ok("spared: ground, snow, aurora, olive, copper and orange come through byte for byte",
       all(v[0] == v[1] for v in spared.values()), spared)
    ok("region: rect moves the gold inside it and nothing outside it",
       r["reg"]["inGold"] == af["gold"] and r["reg"]["rampOutside"] == bf["ramp"][9],
       r["reg"])
    ok("contract: a bad hex and an unknown option throw", all(r["contract"].values()), r["contract"])
    print("\nakpost_holdink_verify: " + ("all passed" if not bad else "%d FAILED" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
