#!/usr/bin/env python3
"""akthree_far_clip_verify.py -- the reconstruction behind AKT.audit's far_clip
finding and qa.py's WARN on it (2026-10-25, weekly pass).

THE DEFECT. No.96 slide 04 laid a 6000 km sea-ice plane under a camera whose far
plane was 2000 km. The far plane cut the plane, the scene background showed
through the cut, and three critic rounds named a "tan wedge" and a hard
diagonal below the horizon before anyone looked at camera.far.

THE FIXTURES, run through the REAL render.py and qa.py:
  01 a km-scale ice plane, 6000 wide, far 2000        -> far-plane WARN
  02 the same scene with far 9000 (No.96's repair)      -> clean
  03 AKT.ground's default stage at the default framing  -> clean (no false alarm
                                                           on the ordinary scene)

  python3 tests/akthree_far_clip_verify.py     # exit 0 = all three hold
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
NEEDLE = "far plane cuts a mesh"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#05080f}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;left:96px;top:96px;font:600 40px sans-serif;color:#eef4fc}</style>
</head><body><canvas id="scene" width="2160" height="2700"></canvas>
<div class="t">Far plane reconstruction</div>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('@@ASSETS@@/js/three.module.min.js');
  const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
  const R = AKT.setup(document.getElementById('scene'), { w:1080, h:1350, bg:0xb89a70, exposure:1.1 });
  AKT.rig(R, AKT.rigs.arcticNight);
BODY
  await AKT.snapshot(R);
  return true;
})();
</script></body></html>"""

ICE = """  const ice = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000),
    new THREE.MeshStandardMaterial({ color: 0xdfe8ef, roughness: 0.6, metalness: 0 }));
  ice.name = 'sea ice plane'; ice.rotation.x = -Math.PI / 2; AKT.add(R, ice);
  AKT.frame(R, { from: [0, 32, 318], look: [0, 16, -40], fov: 25 });
  R.camera.near = 2; R.camera.far = FAR; R.camera.updateProjectionMatrix();"""

STAGE = """  AKT.ground(R, { color: 0x1a2a3c, y: 0 });
  const box = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), AKT.mat.clay(0x6b4a2e));
  box.position.y = 0.5; AKT.add(R, box);
  AKT.frame(R, { from: [3.2, 2.4, 4.6], look: [0, 0.8, 0], fov: 45 });"""

CASES = [
    ("km ice plane, far 2000 (No.96 04)", True, ICE.replace("FAR", "2000")),
    ("km ice plane, far 9000 (the repair)", False, ICE.replace("FAR", "9000")),
    ("AKT.ground default stage", False, STAGE),
]


def main():
    tmp = Path(tempfile.mkdtemp(prefix="farclip_"))
    sl = tmp / "slides"
    sl.mkdir()
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
                                    hits[0][:150] if hits else "clean"))
    print("akthree_far_clip_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
