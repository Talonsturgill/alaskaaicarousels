#!/usr/bin/env python3
"""akthree_ground_edge_verify.py -- the reconstructions behind AKT.audit's
ground_edge and fog_seam findings and qa.py's WARNs on them (2026-11-17,
weekly machine pass).

THE DEFECTS. A GPU frame's ground ends inside the picture, or its fog meets a
sky of another colour, and a critic names the line a round later: No.98 06
(fog 0x070D16 over bg 0x050A12 drew a hard tonal edge behind the copy; fog set
to bg removed it), No.108 01 and 09 (a patch edge, four pixel rounds), No.116
08 (a lighter trapezoid and a curved mesh boundary, the flow critic's cause d
at ship).

THE FIXTURES, run through the REAL render.py and qa.py:
  01 a 20 m terrain plane, no fog, its far edge in frame      -> ground edge WARN
  02 the same with THREE.Fog closing before the edge          -> clean
  03 the same plane with a wall standing in front of the edge -> clean (raycast)
  04 the same plane with userData.edgeShown = true            -> clean
  05 No.98 06: an 80 m floor, fog 0x070D16 over bg 0x050A12   -> fog seam WARN
  06 the No.98 repair: fog set to bg                           -> clean
  07 a terrain plane past the frustum, camera pitched down     -> clean

  python3 tests/akthree_ground_edge_verify.py   # exit 0 = all hold
No network. Writes only into a temp directory.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
EDGE, SEAM = "the ground ends inside the picture", "fog and sky disagree"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#05080f}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;left:96px;top:96px;font:600 40px sans-serif;color:#eef4fc}</style>
</head><body><canvas id="scene" width="2160" height="2700"></canvas>
<div class="t">Ground edge reconstruction</div>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('@@ASSETS@@/js/three.module.min.js');
  const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
  const R = AKT.setup(document.getElementById('scene'), { w:1080, h:1350, bg:BG, exposure:1.1 });
  AKT.rig(R, AKT.rigs.arcticNight);
BODY
  await AKT.snapshot(R);
  return true;
})();
</script></body></html>"""

TERRAIN = """  const g = new THREE.PlaneGeometry(20, 20, 40, 40); g.rotateX(-Math.PI / 2);
  const t = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: 0x2a3d5c, roughness: 0.9 }));
  t.name = 'terrain'; AKT.add(R, t);
  AKT.frame(R, { from: [0, 3.2, 8], look: [0, 0.5, -4], fov: 50 });
"""
FOG = "  R.scene.fog = new THREE.Fog(0x05080f, 6, 14);\n"
WALL = """  const w = new THREE.Mesh(new THREE.BoxGeometry(30, 12, 0.5), AKT.mat.clay(0x3a2a1e));
  w.position.set(0, 6, -8.5); AKT.add(R, w);
"""
SHOWN = "  t.userData.edgeShown = true;\n"
FLOOR98 = """  const f = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0x1a2533 }));
  f.rotation.x = -Math.PI / 2; f.name = 'floor'; AKT.add(R, f);
  R.scene.fog = new THREE.Fog(FOGC, 6, 30);
  AKT.frame(R, { from: [0, 2.2, 7], look: [0, 1.4, 0], fov: 45 });
"""
DOWN = """  const g = new THREE.PlaneGeometry(200, 200, 20, 20); g.rotateX(-Math.PI / 2);
  const t = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: 0x2a3d5c, roughness: 0.9 }));
  t.name = 'terrain'; AKT.add(R, t);
  AKT.frame(R, { from: [0, 6, 6], look: [0, 0, 0], fov: 40 });
"""

CASES = [
    ("terrain edge in frame, no fog (No.116 08)", EDGE, "0x05080f", TERRAIN),
    ("terrain edge behind closing fog", None, "0x05080f", TERRAIN + FOG),
    ("terrain edge behind a wall", None, "0x05080f", TERRAIN + WALL),
    ("terrain edge declared edgeShown", None, "0x05080f", TERRAIN + SHOWN),
    ("No.98 06: fog 0x070D16 over bg 0x050A12", SEAM, "0x050A12", FLOOR98.replace("FOGC", "0x070D16")),
    ("No.98 repair: fog = bg", None, "0x050A12", FLOOR98.replace("FOGC", "0x050A12")),
    ("terrain past the frustum, pitched down", None, "0x05080f", DOWN),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="groundedge_"))
    sl = tmp / "slides"
    sl.mkdir()
    for i, (_, _w, bg, body) in enumerate(CASES, 1):
        (sl / f"slide-0{i}.html").write_text(HEAD.replace("BG", bg).replace("BODY", body))
    try:
        subprocess.run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sl),
                        "--out-dir", str(tmp / "render")], capture_output=True, text=True, timeout=600)
        subprocess.run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(tmp / "render")],
                       capture_output=True, text=True, timeout=300)
        qa = json.loads((tmp / "render" / "machine_qa.json").read_text())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    by = {s["file"]: s for s in qa["slides"]}
    ok = True
    for i, (name, needle, _bg, _b) in enumerate(CASES, 1):
        s = by.get(f"slide-0{i}.html")
        if s is None:
            ok = False
            print("[BROKE] %-44s -> slide never rendered" % name)
            continue
        hits = [w for w in s["warns"] + s["fails"] if EDGE in w or SEAM in w]
        good = (len(hits) == 1 and needle in hits[0]) if needle else not hits
        ok &= good
        print("[%s] %-44s -> %s" % ("HOLD" if good else "BROKE", name, hits[0][:150] if hits else "clean"))
    print("akthree_ground_edge_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
