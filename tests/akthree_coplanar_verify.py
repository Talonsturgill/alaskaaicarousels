#!/usr/bin/env python3
"""akthree_coplanar_verify.py -- the reconstruction behind AKT.audit's `coplanar`
finding and qa.py's WARN on it (2026-11-27, weekly machine pass).

THE DEFECT. Two opaque meshes with a flat face on the same plane, facing the same
way: the depth test can't order them, so the face prints as a dither of both
colours, and critics read it as texture. No.126 slide 08: the stripe box's end face
sat on the bevelled body's at x = 2.06 and the scorer charged "the vermilion stripe
dithers into streaks" to art; an earlier run's brass body top sat exactly on its type
bed and read as a fingerprint speckle for two rounds (FIELD_NOTES). The flow critic's
cause d, a texture artifact, reached four of six runs in the week to November 27th.

THE FIXTURES, run through the REAL render.py and qa.py:
  01 No.126 08: a bevelled AKT.extrude body and a stripe box flush with its ends -> WARN
  02 the same stripe widened past the bevel (No.126's repair)                    -> clean
  03 the flush stripe of 01 with polygonOffset on its material                   -> clean
  04 a body box whose top is exactly a plate's top (the brass bed)               -> WARN
  05 contact without coincidence: a box on the ground, a stacked box, two boxes
     side by side sharing a top plane, a cylinder against a box                  -> clean
  06 01 inside a group turned 0.3 rad (the hero's yaw)                           -> WARN
  07 01 with userData.coplanar = true on the stripe                              -> clean

  python3 tests/akthree_coplanar_verify.py [--work-dir DIR]   # exit 0 = all hold
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
NEEDLE = "coplanar faces z-fight"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#05080f}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;left:96px;top:96px;font:600 40px sans-serif;color:#eef4fc}</style>
</head><body><canvas id="scene" width="2160" height="2700"></canvas>
<div class="t">Coplanar faces reconstruction</div>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('@@ASSETS@@/js/three.module.min.js');
  const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
  const R = AKT.setup(document.getElementById('scene'), { w:1080, h:1350, bg:0x0b1420, exposure:1.1 });
  AKT.environment(R, { intensity: 0.8 });
  AKT.rig(R, AKT.rigs.arcticNight);
  AKT.ground(R, { color: 0x1a2a3c, y: 0 });
  const paint = AKT.mat.clay(0xd2d6d8), red = AKT.mat.clay(0xe0532c);
  const g = new THREE.Group();
BODY
  AKT.add(R, g);
  AKT.frame(R, { from: [5.5, 3.2, 6.5], look: [0, 1.2, 0], fov: 40 });
  await AKT.snapshot(R);
  return true;
})();
</script></body></html>"""

BODYV = """  const body = AKT.extrude([[-2.3, 0], [2.0, 0], [2.0, 1.05], [-2.3, 1.05]], 2.6, paint, { bevelSize: 0.06, bevelThickness: 0.06 });
  body.position.set(0, 1.05, -1.3); body.name = 'body'; g.add(body);"""
FLUSH = BODYV + """
  const band = new THREE.Mesh(new THREE.BoxGeometry(4.42, 0.16, 2.80), red);
  band.position.set(-0.15, 1.42, 0); band.name = 'stripe'; g.add(band);"""
WIDE = BODYV + """
  const band = new THREE.Mesh(new THREE.BoxGeometry(4.46, 0.16, 2.80), red);
  band.position.set(-0.15, 1.42, 0); band.name = 'stripe'; g.add(band);"""
OFFSET = FLUSH.replace("const band = new THREE.Mesh(new THREE.BoxGeometry(4.42, 0.16, 2.80), red);",
                       "const dec = red.clone(); dec.polygonOffset = true; dec.polygonOffsetFactor = -1; dec.polygonOffsetUnits = -1;\n"
                       "  const band = new THREE.Mesh(new THREE.BoxGeometry(4.42, 0.16, 2.80), dec);")
BED = """  const brass = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.0, 1.6), AKT.mat.clay(0xb08d3c));
  brass.position.set(0, 0.5, 0); brass.name = 'brass body'; g.add(brass);
  const bed = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.1, 1.2), AKT.mat.clay(0x2a2622));
  bed.position.set(0, 0.95, 0); bed.name = 'type bed'; g.add(bed);"""
CONTACT = """  const a = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), paint); a.position.set(-1.5, 0.5, 0); g.add(a);
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.6, 0.6), red); b.position.set(-1.5, 1.3, 0); g.add(b);
  const c = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), paint); c.position.set(0, 0.5, 0); g.add(c);
  const d = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), red); d.position.set(1, 0.5, 0); g.add(d);
  const cy = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 1, 32), AKT.mat.clay(0x6b6a2e)); cy.position.set(1, 0.5, 0.9); g.add(cy);
  const e = AKT.extrude([[0, 0], [0.8, 0], [0.8, 0.3], [0, 0.3]], 0.2, paint); e.position.set(-0.4, 0, 1.2); g.add(e);"""
TURNED = FLUSH + "\n  g.rotation.y = 0.3;"
MARKED = FLUSH.replace("band.name = 'stripe';", "band.name = 'stripe'; band.userData.coplanar = true;")

CASES = [
    ("No.126 08 flush stripe on bevelled body", True, FLUSH),
    ("stripe widened past the bevel (repair)", False, WIDE),
    ("flush stripe with polygonOffset", False, OFFSET),
    ("body top exactly on the type bed", True, BED),
    ("contact without coincidence", False, CONTACT),
    ("flush stripe in a yawed group", True, TURNED),
    ("flush stripe marked userData.coplanar", False, MARKED),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir")
    a = ap.parse_args()
    own = not a.work_dir
    tmp = Path(tempfile.mkdtemp(prefix="coplanar_")) if own else Path(a.work_dir)
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
            print("[BROKE] %-42s -> slide never rendered" % name)
            continue
        hits = [w for w in s["warns"] + s["fails"] if NEEDLE in w]
        good = bool(hits) if should_warn else not hits
        ok &= good
        print("[%s] %-42s -> %s" % ("HOLD" if good else "BROKE", name,
                                    hits[0][:200] if hits else "clean"))
    print("akthree_coplanar_verify:", "ALL HOLD" if ok else "BROKEN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
