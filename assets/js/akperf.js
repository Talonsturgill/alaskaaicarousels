/* akperf.js — a machined perforated plate for akthree scenes (No.118, 2026-11-18).
 *
 * One plate, three frames (No.118 slides 01, 02, 09): the same hole grid, the
 * same pitch, the same punched set, seen by different cameras. It lives here
 * because a slide can't share code with a sibling file (SKILL.md), and three
 * hand copies of a 360-hole builder would drift.
 *
 *   const AKP = (await import('@@ASSETS@@/js/akperf.js')).init(THREE);
 *   const grid = AKP.grid({ rows: 12, cols: 30, pitch: 0.34, punched: (r, c) => ... });
 *   const P = AKP.plate(grid, { thickness: 0.07, mat, dimpleMat, slugs: false });
 *   scene.add(P.group);  P.holes -> [{r, c, x, y, punched}] in plate-local units
 *
 * The plate lies in local XY with its FRONT face at z = +thickness/2, centred
 * on the origin; holes are true through-holes (ExtrudeGeometry shape holes),
 * so light behind the plate reaches the front only through the punched bores
 * and a shadow-casting light behind it projects the punched set as a gobo.
 * Blind positions get a shallow dimple: a dark disc and a chamfer ring.
 * Deterministic: no Math.random anywhere.
 */
export function init(THREE) {
  const AKP = {};

  AKP.grid = function (o) {
    const rows = o.rows, cols = o.cols, pitch = o.pitch;
    const margin = o.margin != null ? o.margin : pitch * 0.9;
    const w = cols * pitch + 2 * margin - pitch, h = rows * pitch + 2 * margin - pitch;
    const holes = [];
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      holes.push({ r, c,
        x: -w / 2 + margin + c * pitch,
        y: h / 2 - margin - r * pitch,
        punched: !!o.punched(r, c) });
    }
    return { rows, cols, pitch, margin, w, h, holes,
      radius: o.radius != null ? o.radius : pitch * 0.30 };
  };

  function roundRect(s, w, h, rr) {
    const x0 = -w / 2, y0 = -h / 2;
    s.moveTo(x0 + rr, y0);
    s.lineTo(x0 + w - rr, y0); s.quadraticCurveTo(x0 + w, y0, x0 + w, y0 + rr);
    s.lineTo(x0 + w, y0 + h - rr); s.quadraticCurveTo(x0 + w, y0 + h, x0 + w - rr, y0 + h);
    s.lineTo(x0 + rr, y0 + h); s.quadraticCurveTo(x0, y0 + h, x0, y0 + h - rr);
    s.lineTo(x0, y0 + rr); s.quadraticCurveTo(x0, y0, x0 + rr, y0);
  }

  AKP.plate = function (g, o) {
    o = o || {};
    const t = o.thickness || 0.07;
    const shape = new THREE.Shape();
    roundRect(shape, g.w, g.h, Math.min(g.w, g.h) * 0.04);
    const segs = o.segments || 20;
    for (const hl of g.holes) {
      if (!hl.punched) continue;
      const p = new THREE.Path();
      p.absarc(hl.x, hl.y, g.radius, 0, Math.PI * 2, true);
      shape.holes.push(p);
    }
    const geo = new THREE.ExtrudeGeometry(shape, { depth: t, bevelEnabled: true,
      bevelThickness: t * 0.18, bevelSize: g.radius * 0.16, bevelSegments: 2,
      curveSegments: segs });
    geo.translate(0, 0, -t / 2);
    const group = new THREE.Group();
    const mat = o.mat || new THREE.MeshStandardMaterial({ color: 0x8c979e, metalness: 0.85, roughness: 0.32 });
    const plate = new THREE.Mesh(geo, mat);
    plate.castShadow = true; plate.receiveShadow = true;
    group.add(plate);
    const front = t / 2 + t * 0.18;
    // blind dimples: a dark recessed disc plus a lit chamfer ring
    const dMat = o.dimpleMat || new THREE.MeshStandardMaterial({ color: 0x2a333b, metalness: 0.7, roughness: 0.55 });
    const rMat = o.ringMat || new THREE.MeshStandardMaterial({ color: 0xb8c2c8, metalness: 0.9, roughness: 0.22 });
    const disc = new THREE.CircleGeometry(g.radius * 0.86, 28);
    const ring = new THREE.TorusGeometry(g.radius * 0.93, g.radius * 0.09, 6, 36);
    for (const hl of g.holes) {
      if (hl.punched) continue;
      const d = new THREE.Mesh(disc, dMat); d.position.set(hl.x, hl.y, front + 0.0015);
      const rg = new THREE.Mesh(ring, rMat); rg.position.set(hl.x, hl.y, front + 0.001);
      d.receiveShadow = true; group.add(d); group.add(rg);
    }
    // optional steel slugs seated in the punched bores (the plate at rest)
    const slugs = [];
    if (o.slugs) {
      const sMat = o.slugMat || new THREE.MeshStandardMaterial({ color: 0xaeb8c0, metalness: 0.9, roughness: 0.28 });
      const sg = new THREE.CylinderGeometry(g.radius * 0.97, g.radius * 0.97, t * 1.25, 28);
      sg.rotateX(Math.PI / 2);
      for (const hl of g.holes) if (hl.punched) {
        const s = new THREE.Mesh(sg, sMat); s.position.set(hl.x, hl.y, t * 0.08);
        s.castShadow = true; s.receiveShadow = true; group.add(s); slugs.push(s);
      }
    }
    return { group, plate, holes: g.holes, front, thickness: t, slugs };
  };

  /* Brushed grain as a DataTexture: horizontal streaks, seeded, so steel reads
   * as machined rather than as grey plastic. rng is AK.rng(seed). */
  AKP.brushed = function (rng, size) {
    size = size || 512;
    const data = new Uint8Array(size * size * 4);
    const rowV = new Float32Array(size);
    for (let y = 0; y < size; y++) rowV[y] = 0.82 + 0.18 * rng();
    for (let y = 0; y < size; y++) {
      let run = 0.9 + 0.1 * rng();
      for (let x = 0; x < size; x++) {
        if (rng() < 0.02) run = 0.88 + 0.12 * rng();
        const v = Math.max(0, Math.min(255, Math.round(255 * rowV[y] * run)));
        const i = (y * size + x) * 4;
        data[i] = data[i + 1] = data[i + 2] = v; data[i + 3] = 255;
      }
    }
    const tex = new THREE.DataTexture(data, size, size);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.needsUpdate = true;
    return tex;
  };

  return AKP;
}
