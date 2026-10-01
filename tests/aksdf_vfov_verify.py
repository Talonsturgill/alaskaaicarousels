#!/usr/bin/env python3
"""aksdf_vfov_verify.py -- AKSDF's camera is HORIZONTAL-fov, and `cam.vfov`
frames by height (2026-10-01, run No.74).

WHAT IT RECONSTRUCTS. AKSDF.render maps screen x in [-1, 1] to the focal
length and scales screen y by H / W, so `cam.fov` spans the WIDTH. No.74 framed
its ballot tray by vertical arithmetic, and on a 4:5 portrait frame, where the
true vertical field is 1.25x the planned one in tan(half angle), that cost two
misframed renders before anyone read the camera code. The header
said nothing. Now the header says it, `cam.vfov` exists for height-planned
frames, and AKSDF.focal() is the one focal length both the renderer and
AKTRAY.project use.

  python3 tests/aksdf_vfov_verify.py      # exit 0 = every check holds

Node only, the real aksdf.js and aktray.js, no browser.

  legacy    focal({fov}) is BIT-IDENTICAL to the old 1 / tan(fov * pi / 180 / 2)
            for every fov any shipped deck used, so no existing frame moves
  fov-h     with fov 40, a point 20 degrees off axis horizontally projects
            onto the frame's right edge (the reconstruction: the same point
            20 degrees off VERTICALLY lands well inside, not on, the top edge)
  vfov      with vfov 40, a point 20 degrees off axis vertically projects
            onto the frame's top edge
  equiv     vfov v gives the same focal length as fov 2 atan(tan(v/2) W/H)
  wins      vfov wins when both are given
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROBE = r"""
const fs = require('fs');
const ROOT = process.argv[process.argv.length - 1];
const scope = {};
const load = f => (new Function('window', 'globalThis',
  fs.readFileSync(ROOT + '/assets/js/' + f, 'utf8'))).call(scope, scope, scope);
load('aksdf.js'); load('aktray.js');
const S = scope.AKSDF, T = scope.AKTRAY, out = {};
const W = 540, H = 675, box = [0, 0, 1080, 1350], internal = [W, H];

out.legacy_bad = [];
for (const f of [34, 40, 46, 50, 52, 58, 64, 0, undefined]) {
  const old = 1 / Math.tan(((f || 50) * Math.PI / 180) / 2);
  const now = S.focal({fov: f}, W, H);
  if (old !== now) out.legacy_bad.push(String(f));
}
const tan20 = Math.tan(20 * Math.PI / 180);
const cam = {pos: [0, 0, 0], look: [0, 0, -1]};
out.h_right = T.project(Object.assign({fov: 40}, cam), box, internal, [tan20, 0, -1]);
out.h_top = T.project(Object.assign({fov: 40}, cam), box, internal, [0, tan20, -1]);
out.v_top = T.project(Object.assign({vfov: 40}, cam), box, internal, [0, tan20, -1]);
const hEq = 2 * Math.atan(Math.tan(20 * Math.PI / 180) * W / H) * 180 / Math.PI;
out.equiv = Math.abs(S.focal({vfov: 40}, W, H) - S.focal({fov: hEq}, W, H));
out.wins = S.focal({vfov: 40, fov: 70}, W, H) === S.focal({vfov: 40}, W, H);
console.log(JSON.stringify(out));
"""


def main():
    p = subprocess.run(["node", "-", str(ROOT)], input=PROBE,
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("  BAD  node failed\n" + p.stderr[-1200:])
        return 1
    r = json.loads(p.stdout.strip().splitlines()[-1])
    checks = [
        ("legacy fov focal length bit-identical", not r["legacy_bad"],
         "differs for %s" % r["legacy_bad"] if r["legacy_bad"] else "9 of 9 identical"),
        ("fov 40: 20 deg horizontal lands on the right edge",
         abs(r["h_right"][0] - 1080) < 1e-6, "x = %.4f" % r["h_right"][0]),
        ("fov 40: 20 deg VERTICAL does not reach the top (defect)",
         r["h_top"][1] > 100, "y = %.1f, inside the frame: the vertical field is wider than the number" % r["h_top"][1]),
        ("vfov 40: 20 deg vertical lands on the top edge",
         abs(r["v_top"][1]) < 1e-6, "y = %.6f" % r["v_top"][1]),
        ("vfov equals its horizontal equivalent", r["equiv"] < 1e-12, "|d fl| = %.2e" % r["equiv"]),
        ("vfov wins over fov", r["wins"], str(r["wins"])),
    ]
    ok = True
    for name, good, detail in checks:
        print("  %s  %-56s %s" % ("ok  " if good else "BAD ", name, detail))
        ok = ok and good
    print("AKSDF VFOV: " + ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
