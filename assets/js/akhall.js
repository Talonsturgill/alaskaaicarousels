/* akhall.js -- the illustrative lecture hall of No.79 (2026-10-06), one seat per student.
 *
 * Deck furniture, like akfield.js and akmetrology.js: it builds the SAME hall for every frame that
 * shows it (01 the cited seat, 02 the whole bowl, 07 the seats behind the microphone), so the count
 * on 02 and the seat on 01 are one model and one seeded sample. It draws no slide: each frame owns
 * its camera, its light, its grade and its type.
 *
 * THE FAN LAW. Row r (0 to 69) holds 81 + 2r seats. Sum over the 70 rows = 70*81 + 2*(69*70/2) =
 * 5,670 + 4,830 = 10,500 exactly, the "more than 10,500 students" of the claim, drawn and counted.
 * Beyond row 69 the treads continue bare (EXTRA_ROWS), which is how "more than" is drawn without
 * being counted. Fan 66 degrees, front radius 36.4 m, row pitch 0.90 m, rise 0.30 m, four radial
 * aisles of 1.2 m. World: the fan's apex is at z = -FRONT_R on the centre line, row 0's centre seat
 * sits at the origin, rows climb toward +z and +y, seats face the stage (toward -z).
 *
 * THE SAMPLE. 150 cited seats are drawn by a seeded Fisher-Yates shuffle (mulberry32, seed
 * 20261006) without replacement; the first 119 of them carry a gold sheet (used AI). Positions mean
 * nothing; only the counts do (storyboard honesty guards).
 *
 *   const H = (await import('@@ASSETS@@/js/akhall.js')).init(THREE);
 *   const L = H.layout();                      // seats, cited, gold, hero
 *   const hall = H.build(R, { rows: [0, 69], extraRows: 12, shadows: true });
 */
export function init(THREE) {
  const H = {};
  const ROWS = 70, FRONT_R = 36.4, PITCH = 0.90, RISE = 0.30, FAN = 66 * Math.PI / 180;
  const AISLES = 4, AISLE_W = 1.2, EXTRA_ROWS = 12, SEED = 20261006;
  H.CONST = { ROWS, FRONT_R, PITCH, RISE, FAN, AISLES, AISLE_W, EXTRA_ROWS, SEED };

  function mulberry(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  H.rng = mulberry;

  H.seatsInRow = r => 81 + 2 * r;
  H.radius = r => FRONT_R + r * PITCH;

  /* Seat centres along each row's arc, skipping the four aisles. The usable arc is the row's arc
   * minus four aisle widths, split into five equal banks (sections); seats are spread evenly over
   * the usable length so every row's count is exact whatever its radius. */
  function rowAngles(r) {
    const rho = H.radius(r), n = H.seatsInRow(r);
    const arc = rho * FAN, usable = arc - AISLES * AISLE_W, pitch = usable / n;
    const banks = AISLES + 1, perBank = [];
    let left = n;
    for (let b = 0; b < banks; b++) { const k = Math.round(left / (banks - b)); perBank.push(k); left -= k; }
    const out = [];
    let s = -arc / 2;
    for (let b = 0; b < banks; b++) {
      for (let k = 0; k < perBank[b]; k++) { out.push((s + pitch * (k + 0.5)) / rho); }
      s += perBank[b] * pitch + AISLE_W;
    }
    return { angles: out, pitch };
  }
  H.rowAngles = rowAngles;

  let cache = null;
  H.layout = function () {
    if (cache) return cache;
    const seats = [];
    const jr = mulberry(SEED + 7);
    for (let r = 0; r < ROWS; r++) {
      const { angles, pitch } = rowAngles(r);
      const rho = H.radius(r), y = r * RISE;
      for (const th of angles) {
        const x = rho * Math.sin(th), z = rho * Math.cos(th) - FRONT_R;
        const yaw = th + Math.PI + (jr() - 0.5) * 2 * (1.5 * Math.PI / 180);
        seats.push({ i: seats.length, r, th, x, y, z, yaw, pitch, upTilt: jr() * 0.10 });
      }
    }
    // the cited sample: seeded shuffle, first 150 cited, first 119 of those gold
    const idx = seats.map(s => s.i), rr = mulberry(SEED);
    for (let k = idx.length - 1; k > 0; k--) { const j = Math.floor(rr() * (k + 1)); const t = idx[k]; idx[k] = idx[j]; idx[j] = t; }
    const citedList = idx.slice(0, 150), goldList = citedList.slice(0, 119);
    const cited = new Set(citedList), gold = new Set(goldList);
    // the cover's seat: the gold seat in the lowest row within the centre bank (|theta| under 20 deg)
    let hero = null;
    for (const i of goldList) {
      const s = seats[i];
      if (Math.abs(s.th) < 20 * Math.PI / 180 && s.r >= 2 && (!hero || s.r < hero.r || (s.r === hero.r && Math.abs(s.th) < Math.abs(hero.th)))) hero = s;
    }
    const sheetYaw = new Map(), sr = mulberry(SEED + 11);
    for (const i of goldList) sheetYaw.set(i, (sr() - 0.5) * 0.7);
    cache = { seats, cited, gold, citedList, goldList, hero, sheetYaw };
    return cache;
  };

  /* Local seat frame: origin on the tread at the seat's centre, +z toward the stage (the seat's
   * front), +x to the seat's right as you sit, y up. Every part below is placed in this frame. */
  H.PARTS = {
    standard: { size: [0.055, 0.60, 0.48], at: [0.255, 0.30, -0.02] },
    arm:      { size: [0.075, 0.028, 0.40], at: [0.255, 0.615, 0.0] },
    back:     { size: [0.47, 0.56, 0.065], at: [0, 0.70, -0.21], rotX: -0.17 },
    panUp:    { size: [0.45, 0.40, 0.060], at: [0, 0.56, -0.12], rotX: 0.0 },
    panDown:  { size: [0.45, 0.065, 0.42], at: [0, 0.445, 0.05], rotX: 0.05 },
    sheet:    { size: [0.21, 0.004, 0.297], at: [0, 0.493, 0.06], rotX: 0.05 }
  };

  const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpE = new THREE.Euler(),
        tmpP = new THREE.Vector3(), tmpS = new THREE.Vector3(1, 1, 1);
  /* world matrix of a part of seat s, with an optional extra local rotation about x */
  H.partMatrix = function (s, part, extraRotX, extraYaw) {
    const p = H.PARTS[part];
    const seat = new THREE.Matrix4().makeRotationY(s.yaw).setPosition(s.x, s.y, s.z);
    const local = new THREE.Matrix4();
    tmpE.set((p.rotX || 0) + (extraRotX || 0), extraYaw || 0, 0);
    tmpQ.setFromEuler(tmpE);
    tmpP.set(p.at[0], p.at[1], p.at[2]);
    local.compose(tmpP, tmpQ, tmpS);
    return seat.multiply(local);
  };
  /* a local point on seat s -> world Vector3 */
  H.seatPoint = function (s, lx, ly, lz) {
    const m = new THREE.Matrix4().makeRotationY(s.yaw).setPosition(s.x, s.y, s.z);
    return new THREE.Vector3(lx, ly, lz).applyMatrix4(m);
  };

  /* A box with every edge rounded: a rounded rectangle in x-y extruded along z with a bevel of the
   * same radius, so the outer size is exactly w x h x d. `cup` bends it about the y axis (z += cup *
   * x^2), which is how an upholstered back or a pan cushion is moulded; normals are recomputed. */
  function rrect(w, h, r) {
    const sh = new THREE.Shape(), x = -w / 2, y = -h / 2;
    sh.moveTo(x + r, y); sh.lineTo(x + w - r, y); sh.quadraticCurveTo(x + w, y, x + w, y + r);
    sh.lineTo(x + w, y + h - r); sh.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    sh.lineTo(x + r, y + h); sh.quadraticCurveTo(x, y + h, x, y + h - r);
    sh.lineTo(x, y + r); sh.quadraticCurveTo(x, y, x + r, y);
    return sh;
  }
  function rounded(w, h, d, r, cup, axis) {
    r = Math.min(r == null ? 0.018 : r, d / 2 - 0.002, w / 4, h / 4);
    const g = new THREE.ExtrudeGeometry(rrect(w - 2 * r, h - 2 * r, Math.min(r, (Math.min(w, h) - 2 * r) / 2.2)),
      { depth: d - 2 * r, bevelEnabled: true, bevelThickness: r, bevelSize: r, bevelSegments: 4, curveSegments: 6, steps: 1 });
    g.center();
    if (axis === 'horizontal') g.rotateX(-Math.PI / 2);      // a pan: its thickness becomes y
    if (cup) {
      const pa = g.attributes.position;
      for (let k = 0; k < pa.count; k++) { const x = pa.getX(k); pa.setZ(k, pa.getZ(k) + cup * x * x); }
      pa.needsUpdate = true;
    }
    g.computeVertexNormals();
    return g;
  }
  H.rounded = rounded;
  /* The cast end standard: a side profile in (z, y) extruded along x and bevelled. A splayed foot, a
   * tapering upright and a rounded armrest bracket. */
  function standardGeom() {
    const sh = new THREE.Shape();
    sh.moveTo(-0.20, 0.0); sh.lineTo(0.16, 0.0); sh.quadraticCurveTo(0.20, 0.0, 0.19, 0.03);
    sh.lineTo(0.10, 0.08); sh.lineTo(0.08, 0.50); sh.quadraticCurveTo(0.20, 0.55, 0.20, 0.585);
    sh.lineTo(0.20, 0.60); sh.lineTo(-0.16, 0.60); sh.quadraticCurveTo(-0.20, 0.60, -0.20, 0.57);
    sh.lineTo(-0.12, 0.08); sh.lineTo(-0.20, 0.03); sh.lineTo(-0.20, 0.0);
    const g = new THREE.ExtrudeGeometry(sh, { depth: 0.035, bevelEnabled: true, bevelThickness: 0.008,
      bevelSize: 0.006, bevelSegments: 3, curveSegments: 8 });
    g.translate(0, 0, -0.0175); g.rotateY(Math.PI / 2); g.translate(0, -0.30, 0);   // profile z,y; centred on the part's origin
    g.computeVertexNormals();
    return g;
  }
  function armGeom() { return rounded(0.075, 0.032, 0.40, 0.014); }
  H.geoms = function () {
    return {
      standard: standardGeom(), arm: armGeom(),
      back: rounded(0.47, 0.56, 0.075, 0.03, 0.22),
      panUp: rounded(0.45, 0.40, 0.065, 0.026, 0.10),
      panDown: rounded(0.45, 0.42, 0.065, 0.026, -0.10, 'horizontal'),
      sheet: new THREE.BoxGeometry(...H.PARTS.sheet.size)
    };
  };

  /* Treads and risers for rows [r0, r1] plus extra bare rows: one BufferGeometry, front edge of
   * each tread toward the stage, riser below it. Nosing is a separate thin strip so it can take its
   * own lighter material. */
  H.treads = function (r0, r1, extra, segs) {
    segs = segs || 160;
    const pos = [], nor = [], nos = [], nosN = [];
    const half = FAN / 2 + 0.01;
    for (let r = r0; r <= r1 + extra; r++) {
      const rho = H.radius(r), y = r * RISE, yPrev = (r - 1) * RISE;
      const rIn = rho - PITCH / 2, rOut = rho + PITCH / 2;
      for (let k = 0; k < segs; k++) {
        const a0 = -half + (2 * half) * k / segs, a1 = -half + (2 * half) * (k + 1) / segs;
        const P = (rr, a, yy) => [rr * Math.sin(a), yy, rr * Math.cos(a) - FRONT_R];
        // tread top
        const q = [P(rIn, a0, y), P(rOut, a0, y), P(rOut, a1, y), P(rIn, a1, y)];
        pos.push(...q[0], ...q[1], ...q[2], ...q[0], ...q[2], ...q[3]);
        for (let t = 0; t < 6; t++) nor.push(0, 1, 0);
        // riser at the front edge, facing the stage (toward the apex)
        const rq = [P(rIn, a0, yPrev), P(rIn, a0, y), P(rIn, a1, y), P(rIn, a1, yPrev)];
        pos.push(...rq[0], ...rq[2], ...rq[1], ...rq[0], ...rq[3], ...rq[2]);
        const am = (a0 + a1) / 2;
        for (let t = 0; t < 6; t++) nor.push(-Math.sin(am), 0, -Math.cos(am));
        // nosing strip: 3 cm on the tread at the front edge, raised 2 mm
        const n0 = P(rIn, a0, y + 0.002), n1 = P(rIn + 0.035, a0, y + 0.002), n2 = P(rIn + 0.035, a1, y + 0.002), n3 = P(rIn, a1, y + 0.002);
        nos.push(...n0, ...n1, ...n2, ...n0, ...n2, ...n3);
        for (let t = 0; t < 6; t++) nosN.push(0, 1, 0);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    const gn = new THREE.BufferGeometry();
    gn.setAttribute('position', new THREE.Float32BufferAttribute(nos, 3));
    gn.setAttribute('normal', new THREE.Float32BufferAttribute(nosN, 3));
    return { tread: g, nosing: gn };
  };

  H.materials = function (o) {
    o = o || {};
    return {
      wool:   new THREE.MeshStandardMaterial({ color: o.wool || 0x1D3B47, roughness: 0.96, metalness: 0 }),
      woolLit:new THREE.MeshStandardMaterial({ color: o.woolLit || 0x2A5260, roughness: 0.94, metalness: 0 }),
      birch:  new THREE.MeshPhysicalMaterial({ color: o.birch || 0xA88A64, roughness: 0.46, metalness: 0, clearcoat: 0.3, clearcoatRoughness: 0.4 }),
      alu:    new THREE.MeshStandardMaterial({ color: o.alu || 0x5C6670, roughness: 0.38, metalness: 0.6 }),
      tread:  new THREE.MeshStandardMaterial({ color: o.tread || 0x20262C, roughness: 0.92, metalness: 0 }),
      nosing: new THREE.MeshStandardMaterial({ color: o.nosing || 0x5E6A72, roughness: 0.7, metalness: 0.1 }),
      gold:   new THREE.MeshStandardMaterial({ color: 0xFFC72C, roughness: 0.62, metalness: 0, emissive: 0x3a2a00, emissiveIntensity: o.goldGlow != null ? o.goldGlow : 0.25 }),
      paper:  new THREE.MeshStandardMaterial({ color: 0xE9EEF2, roughness: 0.8, metalness: 0 })
    };
  };

  /* Build the hall into R.scene. opts.rows [r0, r1] limits the seated rows (a close camera does
   * not need the back of the house); opts.filter(seat) can thin further. opts.blankSheet puts a
   * paper sheet (not gold) on the given seat index. Returns the meshes and the seats drawn. */
  H.build = function (R, opts) {
    opts = opts || {};
    const L = H.layout();
    const M = opts.materials || H.materials(opts.colors);
    const r0 = (opts.rows || [0, ROWS - 1])[0], r1 = (opts.rows || [0, ROWS - 1])[1];
    const pick = L.seats.filter(s => s.r >= r0 && s.r <= r1 && (!opts.filter || opts.filter(s)));
    const parts = ['standard', 'arm', 'back'];
    const geoms = H.geoms();
    const mats = { standard: M.alu, arm: M.birch, back: M.wool, panUp: M.wool, panDown: M.woolLit, sheet: M.gold };
    const out = { meshes: {}, seats: pick, layout: L, materials: M };
    const up = pick.filter(s => !L.cited.has(s.i)), down = pick.filter(s => L.cited.has(s.i));
    const sheets = down.filter(s => L.gold.has(s.i));
    const lists = { standard: pick, arm: pick, back: pick, panUp: up, panDown: down, sheet: sheets };
    for (const part of ['standard', 'arm', 'back', 'panUp', 'panDown', 'sheet']) {
      const list = lists[part];
      if (!list.length) continue;
      const mesh = new THREE.InstancedMesh(geoms[part], mats[part], list.length);
      list.forEach((s, k) => {
        let m;
        if (part === 'panUp') m = H.partMatrix(s, part, -s.upTilt, 0);
        else if (part === 'sheet') m = H.partMatrix(s, part, 0, L.sheetYaw.get(s.i));
        else m = H.partMatrix(s, part, 0, 0);
        mesh.setMatrixAt(k, m);
      });
      mesh.instanceMatrix.needsUpdate = true;
      mesh.castShadow = opts.shadows !== false; mesh.receiveShadow = opts.shadows !== false;
      R.scene.add(mesh);
      out.meshes[part] = mesh;
    }
    if (opts.treads !== false) {
      const t = H.treads(Math.max(0, r0 - 1), Math.min(ROWS - 1, r1), r1 >= ROWS - 1 ? (opts.extraRows != null ? opts.extraRows : EXTRA_ROWS) : 0, opts.treadSegs);
      const tm = new THREE.Mesh(t.tread, M.tread); tm.receiveShadow = true; tm.castShadow = opts.shadows !== false;
      const nm = new THREE.Mesh(t.nosing, M.nosing); nm.receiveShadow = true;
      R.scene.add(tm); R.scene.add(nm);
      out.meshes.tread = tm; out.meshes.nosing = nm;
    }
    return out;
  };

  return H;
}
