#!/usr/bin/env python3
"""akthree_faceted_verify.py -- the reconstruction behind AKT.creaseNormals, AKT.audit's
`faceted` finding and qa.py's WARN on it (2026-11-24, weekly machine pass).

THE DEFECT. three r170's ExtrudeGeometry is non-indexed and computes one normal per
face, so every curve segment of a wall and every bevel segment shades as its own flat
band. No.118 slide 02's bore walls printed as horizontal bands for two critic rounds
(cured by raising curve segments to 72), No.123's GPU module was named for flat-shaded
edges, and No.122's caliper read as box primitives: the flow critic's cause b, "the
largest object least modelled", on four of five runs in the week to November 24th.

THE FIXTURES, run through the REAL render.py and qa.py:
  01 a bored ring, ExtrudeGeometry, 32 curve segments, 2-segment bevel  -> WARN
  02 the same ring after AKT.creaseNormals(geo, 40)                     -> clean
  03 BoxGeometry, CylinderGeometry, AKT.lathe and AKT.extrude defaults  -> clean
     (no false alarm on three's smooth primitives or the bench's own helpers)
  04 the ring of 01 marked userData.faceted = true                      -> clean
and, in node on the same three build, a numeric check that creasing removes at least 98 percent
of the ring's 6 to 40 degree steps and keeps every 90 degree corner of a square prism hard.

  python3 tests/akthree_faceted_verify.py [--work-dir DIR]   # exit 0 = all hold
No network. Writes only into --work-dir (default a temp directory).
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
NEEDLE = "curved surface shades as flat bands"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#05080f}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;left:96px;top:96px;font:600 40px sans-serif;color:#eef4fc}</style>
</head><body><canvas id="scene" width="2160" height="2700"></canvas>
<div class="t">Faceted normals reconstruction</div>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('@@ASSETS@@/js/three.module.min.js');
  const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
  const R = AKT.setup(document.getElementById('scene'), { w:1080, h:1350, bg:0x0b1420, exposure:1.1 });
  AKT.environment(R, { intensity: 0.8 });
  AKT.rig(R, AKT.rigs.arcticNight);
  AKT.ground(R, { color: 0x1a2a3c, y: 0 });
  function ring() {
    const s = new THREE.Shape(); s.absarc(0, 0, 1, 0, Math.PI * 2, false);
    const h = new THREE.Path(); h.absarc(0, 0, 0.42, 0, Math.PI * 2, true); s.holes.push(h);
    const g = new THREE.ExtrudeGeometry(s, { depth: 0.35, bevelEnabled: true, bevelSize: 0.04,
      bevelThickness: 0.04, bevelSegments: 2, curveSegments: 32 });
    g.rotateX(-Math.PI / 2); g.translate(0, 0.4, 0); return g;
  }
BODY
  AKT.frame(R, { from: [2.6, 2.4, 3.4], look: [0, 0.4, 0], fov: 40 });
  await AKT.snapshot(R);
  return true;
})();
</script></body></html>"""

RAW = """  const m = new THREE.Mesh(ring(), AKT.mat.clay(0x8a96a0)); m.name = 'bored ring'; AKT.add(R, m);"""
PRIMS = """  const b = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.6, 0.6), AKT.mat.clay(0x6b4a2e)); b.position.set(-1.1, 0.3, 0); b.name = 'box'; AKT.add(R, b);
  const c = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.7, 32), AKT.mat.clay(0x6b6a2e)); c.position.set(1.1, 0.35, 0); c.name = 'cylinder'; AKT.add(R, c);
  const l = AKT.lathe([[0.2, 0], [0.34, 0.3], [0.22, 0.6]], AKT.mat.clay(0x4a6b2e)); l.position.set(0, 0, -1); l.name = 'lathe'; AKT.add(R, l);
  const e = AKT.extrude([[0, 0], [0.8, 0], [0.8, 0.3], [0.4, 0.6], [0, 0.3]], 0.2, AKT.mat.clay(0x2e4a6b)); e.position.set(-0.4, 0, 0.8); e.name = 'extrude plaque'; AKT.add(R, e);
  const s = new THREE.Shape(); s.absarc(0, 0, 0.3, 0, Math.PI * 2, false);
  const d = new THREE.Mesh(AKT.extrude([[0,0],[1,0],[1,1]], 0.1, AKT.mat.clay(0x777777)).geometry, AKT.mat.clay(0x777777)); d.position.set(0.6, 0, 0.9); d.name = 'extrude tri'; AKT.add(R, d);
  const disc = AKT.extrude(s.getPoints(48).map(p => [p.x, p.y]), 0.12, AKT.mat.clay(0x997755)); disc.position.set(1.2, 0, -0.9); disc.name = 'extrude disc'; AKT.add(R, disc);"""
CREASED = """  const g = ring(); AKT.creaseNormals(g, 40);
  const m = new THREE.Mesh(g, AKT.mat.clay(0x8a96a0)); m.name = 'bored ring creased'; AKT.add(R, m);"""
MARKED = RAW.replace("AKT.add(R, m);", "m.userData.faceted = true; AKT.add(R, m);")

NUMERIC = r"""
const THREE = await import('@ROOT@/assets/js/three.module.min.js');
const AKT = (await import('@ROOT@/assets/js/akthree.js')).init(THREE);
const s = new THREE.Shape(); s.absarc(0, 0, 1, 0, Math.PI * 2, false);
const h = new THREE.Path(); h.absarc(0, 0, 0.42, 0, Math.PI * 2, true); s.holes.push(h);
const g = new THREE.ExtrudeGeometry(s, { depth: 0.35, bevelEnabled: true, bevelSize: 0.04,
  bevelThickness: 0.04, bevelSegments: 2, curveSegments: 32 });
function steps(geo) {
  const p = geo.attributes.position, n = geo.attributes.normal, map = new Map();
  for (let i = 0; i < p.count; i++) {
    const k = [p.getX(i), p.getY(i), p.getZ(i)].map(v => Math.round(v * 1e5)).join(',');
    if (!map.has(k)) map.set(k, []); map.get(k).push(i);
  }
  let soft = 0, hard = 0;
  for (const gr of map.values()) for (let a = 0; a < gr.length; a++) for (let b = a + 1; b < gr.length; b++) {
    const i = gr[a], j = gr[b];
    const d = n.getX(i) * n.getX(j) + n.getY(i) * n.getY(j) + n.getZ(i) * n.getZ(j);
    const ang = Math.acos(Math.max(-1, Math.min(1, d))) * 180 / Math.PI;
    if (ang > 6 && ang < 40) soft++; else if (ang >= 60) hard++;
  }
  return { soft, hard };
}
const before = steps(g); AKT.creaseNormals(g, 40); const after = steps(g);
// real corners: an unbevelled extruded square has only 90 degree edges, and every
// one of them must still be a hard split after creasing
const sq = new THREE.Shape([[0, 0], [1, 0], [1, 1], [0, 1]].map(q => new THREE.Vector2(q[0], q[1])));
const cube = new THREE.ExtrudeGeometry(sq, { depth: 1, bevelEnabled: false });
const cb = steps(cube); AKT.creaseNormals(cube, 40); const ca = steps(cube);
const corners = { before: cb.hard, after: ca.hard, soft_after: ca.soft };
const box = new THREE.BoxGeometry(1, 1, 1), out = AKT.creaseNormals(box, 40);
const indexed_ok = !out.index && out !== box && steps(out).hard > 0 && steps(out).soft === 0;
console.log(JSON.stringify({ before, after, corners, indexed_ok }));
"""

CASES = [
    ("raw ExtrudeGeometry ring (No.118 02)", True, RAW),
    ("the same ring creased (the repair)", False, CREASED),
    ("three primitives and AKT helpers", False, PRIMS),
    ("ring marked userData.faceted", False, MARKED),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir")
    a = ap.parse_args()
    own = not a.work_dir
    tmp = Path(tempfile.mkdtemp(prefix="faceted_")) if own else Path(a.work_dir)
    sl = tmp / "slides"
    sl.mkdir(parents=True, exist_ok=True)
    for i, (_, _w, body) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(HEAD.replace("BODY", body))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"),
                            "--slides-dir", str(sl), "--out-dir", str(tmp / "render")],
                           capture_output=True, text=True, timeout=300)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"),
                        "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        if own:
            shutil.rmtree(tmp, ignore_errors=True)
    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, should_warn, _b) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None:
            ok = False
            print("[BROKE] %-40s -> slide never rendered" % name)
            continue
        hits = [w for w in s["warns"] + s["fails"] if NEEDLE in w]
        good = bool(hits) if should_warn else not hits
        ok &= good
        print("[%s] %-40s -> %s" % ("HOLD" if good else "BROKE", name,
                                    hits[0][:170] if hits else "clean"))
    # the numbers, in node against the same three build and the same helper
    probe = NUMERIC.replace("@ROOT@", ROOT.as_posix())
    r = subprocess.run(["node", "--input-type=module", "-e", probe],
                       capture_output=True, text=True, timeout=120)
    try:
        nums = json.loads(r.stdout.strip().splitlines()[-1])
        b, af = nums["before"], nums["after"]
        # a crease is not transitive: two corners at one position can keep different
        # face sets where a bevel meets a wall, so a residue of steps is allowed (63 of
        # 4697 on this ring, 1.3 percent, with the area weighting)
        c = nums["corners"]
        good = (b["soft"] > 1000 and af["soft"] <= 0.02 * b["soft"]
                and c["before"] > 0 and c["after"] == c["before"] and c["soft_after"] == 0
                and nums["indexed_ok"])
        detail = ("ring: 6-40 deg steps %d -> %d; square prism: 90 deg corner pairs %d -> %d; "
                  "indexed input %s" % (b["soft"], af["soft"], c["before"], c["after"],
                                        "returned non-indexed" if nums["indexed_ok"] else "BROKEN"))
    except Exception as e:
        good, detail = False, "node probe failed: %s %s" % (type(e).__name__, r.stderr[-300:])
    ok &= good
    print("[%s] %-40s -> %s" % ("HOLD" if good else "BROKE", "creasing smooths steps, keeps corners", detail))
    print("akthree_faceted_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
