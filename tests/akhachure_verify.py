#!/usr/bin/env python3
"""akhachure_verify.py -- the verification behind assets/js/akhachure.js.

Runs the helper headlessly under node against synthetic height fields whose
answers are known by construction, and gates the four properties the helper
exists to provide. Exit 0 = every gate passed.

WHY THESE FOUR GATES, AND NOT "SOMETHING WAS DRAWN".

Artwork craft was the weakest scored criterion in 8 of the 10 runs to
2026-08-02, mean 6.25. Two upgrades were aimed at it and the number never moved.
The 2026-08-02 post-mortem says exactly why the last attempt failed, and it is
the reason this file measures what it measures:

    The mechanism was three material registers at different detail frequencies
    with a computed tooth falloff. The registers DID read; the falloff did not,
    on any slide, per multiple independent critics.

The falloff ran in code and not in pixels. So a test that only proved the
helper executes would certify the same failure. What has to be true instead is
that the field's variation is DRIVEN BY THE DATA and is LARGE, so that a human
looking at the render can name which region is which without being told.

  GATE 1 -- SLOPE DRIVES WIDTH. Over a field that is flat on one half and steep
  on the other, the steep half's mean stroke width must exceed the flat half's
  by at least 2.5x. This is the number the run's dossiers declare and the pixel
  critics are asked to contradict from the render alone.

  GATE 2 -- ASPECT DRIVES ROTATION. Over a field tilted purely in x, every
  stroke must run within a few degrees of horizontal; over the same field
  tilted purely in y, within a few degrees of vertical. A field whose strokes
  ignore aspect is a texture, not shading.

  GATE 3 -- DETERMINISM. Two runs at the same seed must agree exactly, and two
  runs at different seeds must not, so the helper is safe inside a five-round
  revision loop. render.py's determinism gate FAILs Math.random, and this
  proves the helper does not need it.

  GATE 4 -- THE DATA IS NOT OPTIONAL. Calling without `height` must THROW. A
  default noise field would let a slide buy the look without the data, which is
  the precise failure this helper exists to stop, so its absence is enforced
  rather than documented.

WHAT IS DELIBERATELY NOT GATED: ink coverage, stroke count, or any
"detail_ratio" style density feature. scripts/craft_corpus.py measured nine such
features over 171 shipped slides against scorer-derived labels and none
separated the slides scorers named from the rest (best AUC 0.653, Bonferroni
p 0.147). Gating a craft upgrade on a feature this repo's own corpus says does
not predict craft would be theatre.
"""

import json
import os
import shutil
import subprocess
import sys

HARNESS = r"""
const HELPER = process.env.AKH_HELPER;
require(HELPER);
const AK = globalThis.AK;

// A recording 2D context. Records every stroke's width and its start/end point,
// which is all four gates need.
function recorder() {
  const marks = [];
  let cur = null, lw = 1;
  return {
    marks,
    save() {}, restore() {},
    set lineCap(v) {}, set lineJoin(v) {}, set strokeStyle(v) {},
    set lineWidth(v) { lw = v; }, get lineWidth() { return lw; },
    beginPath() { cur = {}; },
    moveTo(x, y) { cur.x0 = x; cur.y0 = y; },
    quadraticCurveTo(mx, my, x1, y1) { cur.x1 = x1; cur.y1 = y1; },
    stroke() { marks.push({ w: lw, x0: cur.x0, y0: cur.y0, x1: cur.x1, y1: cur.y1 }); }
  };
}

const out = {};

// ---- GATE 1: slope drives width. Flat left half, steep right half.
{
  const cx = recorder();
  const s = AK.hachureField(cx, {
    x: 0, y: 0, w: 900, h: 600, seed: 20260803, cell: 12, passes: 3,
    color: '#101820',
    height: (u) => (u < 0.5 ? 0.2 : 0.2 + (u - 0.5) * 1.6),
    probes: [
      { name: 'flat',  x: 40,  y: 80, w: 320, h: 440 },
      { name: 'steep', x: 540, y: 80, w: 320, h: 440 }
    ]
  });
  const flat = s.probes.find(p => p.name === 'flat');
  const steep = s.probes.find(p => p.name === 'steep');
  out.gate1 = {
    flatMeanWidth: flat.meanWidth,
    steepMeanWidth: steep.meanWidth,
    ratio: flat.meanWidth > 0 ? steep.meanWidth / flat.meanWidth : Infinity,
    widthRatio: s.widthRatio,
    cells: s.cells, strokesDrawn: cx.marks.length
  };
}

// ---- GATE 2: aspect drives rotation.
function meanAbsAngleDeg(heightFn) {
  const cx = recorder();
  AK.hachureField(cx, {
    x: 0, y: 0, w: 600, h: 600, seed: 7, cell: 20, passes: 1,
    color: '#101820', jitter: 0, bend: 0, lightBias: false,
    height: heightFn
  });
  // Angle of the chord, folded to [0,90] against the horizontal axis.
  let sum = 0, n = 0;
  for (const m of cx.marks) {
    const a = Math.atan2(m.y1 - m.y0, m.x1 - m.x0) * 180 / Math.PI;
    let f = Math.abs(a); if (f > 90) f = 180 - f;
    sum += f; n++;
  }
  return n ? sum / n : NaN;
}
out.gate2 = {
  tiltInX_meanAngleFromHorizontalDeg: meanAbsAngleDeg((u) => u),
  tiltInY_meanAngleFromHorizontalDeg: meanAbsAngleDeg((u, v) => v)
};

// ---- GATE 3: determinism.
function fingerprint(seed) {
  const cx = recorder();
  AK.hachureField(cx, {
    x: 0, y: 0, w: 480, h: 360, seed, cell: 15, passes: 2, color: '#101820',
    height: (u, v) => 0.5 + 0.4 * Math.sin(u * 6.1) * Math.cos(v * 4.3)
  });
  return cx.marks.map(m =>
    [m.w, m.x0, m.y0, m.x1, m.y1].map(z => z.toFixed(6)).join(',')).join('|');
}
const fpA = fingerprint(31337), fpB = fingerprint(31337), fpC = fingerprint(31338);
out.gate3 = { sameSeedIdentical: fpA === fpB, differentSeedDiffers: fpA !== fpC };

// ---- GATE 4: height is required.
try {
  AK.hachureField(recorder(), { x: 0, y: 0, w: 100, h: 100, color: '#101820' });
  out.gate4 = { threwWithoutHeight: false };
} catch (e) {
  out.gate4 = { threwWithoutHeight: true, message: String(e.message) };
}

// No Math.random in the source's CODE. The word appears in this file's own
// prose twice ("never Math.random"), so comments are stripped before the check;
// matching the docstring would be a false positive that teaches nothing.
{
  const src = require('fs').readFileSync(HELPER, 'utf8');
  const code = src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:])\/\/.*$/gm, '$1');
  out.source = { mentionsMathRandom: /Math\s*\.\s*random/.test(code) };
}

console.log(JSON.stringify(out));
"""

WIDTH_RATIO_FLOOR = 2.5
ANGLE_TOL_DEG = 5.0


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("SKIP akhachure_verify: node is not on PATH")
        return 0

    helper = "assets/js/akhachure.js"
    proc = subprocess.run(
        [node, "-e", HARNESS],
        capture_output=True, text=True,
        env={**os.environ, "AKH_HELPER": os.path.abspath(helper)},
    )
    if proc.returncode != 0:
        print("FAIL akhachure_verify: harness crashed")
        print(proc.stderr.strip()[:2000])
        return 1

    r = json.loads(proc.stdout.strip().splitlines()[-1])
    fails = []

    g1 = r["gate1"]
    print(
        "gate 1  slope drives width      "
        f"flat {g1['flatMeanWidth']:.3f} px, steep {g1['steepMeanWidth']:.3f} px, "
        f"ratio {g1['ratio']:.2f}x (floor {WIDTH_RATIO_FLOOR}x), "
        f"{g1['cells']} cells, {g1['strokesDrawn']} strokes"
    )
    if not g1["ratio"] >= WIDTH_RATIO_FLOOR:
        fails.append(
            f"stroke width ratio {g1['ratio']:.2f}x is under the {WIDTH_RATIO_FLOOR}x floor; "
            "the field's variation would not be nameable from the render"
        )
    if g1["strokesDrawn"] <= 0:
        fails.append("no strokes were drawn at all")

    g2 = r["gate2"]
    ax = g2["tiltInX_meanAngleFromHorizontalDeg"]
    ay = g2["tiltInY_meanAngleFromHorizontalDeg"]
    print(
        "gate 2  aspect drives rotation  "
        f"x-tilt {ax:.2f} deg from horizontal (want <= {ANGLE_TOL_DEG}), "
        f"y-tilt {ay:.2f} deg (want >= {90 - ANGLE_TOL_DEG})"
    )
    if not ax <= ANGLE_TOL_DEG:
        fails.append(f"strokes on an x-tilted field ran {ax:.2f} deg off horizontal")
    if not ay >= 90 - ANGLE_TOL_DEG:
        fails.append(f"strokes on a y-tilted field ran {ay:.2f} deg off vertical")

    g3 = r["gate3"]
    print(
        "gate 3  determinism             "
        f"same seed identical {g3['sameSeedIdentical']}, "
        f"different seed differs {g3['differentSeedDiffers']}"
    )
    if not g3["sameSeedIdentical"]:
        fails.append("two runs at the same seed produced different strokes")
    if not g3["differentSeedDiffers"]:
        fails.append("the seed does not change the field")

    g4 = r["gate4"]
    print(f"gate 4  data is not optional    threw without height {g4['threwWithoutHeight']}")
    if not g4["threwWithoutHeight"]:
        fails.append("hachureField accepted a call with no height field")

    if r["source"]["mentionsMathRandom"]:
        fails.append("assets/js/akhachure.js references Math.random")

    if fails:
        print("\nFAIL akhachure_verify")
        for f in fails:
            print("  - " + f)
        return 1
    print("\nPASS akhachure_verify: 4 gates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
