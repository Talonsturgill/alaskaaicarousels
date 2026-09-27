/* akblock.js -- a physiographic BLOCK DIAGRAM from a committed DEM, for akthree.
 *
 * Added 2026-09-27 (run No.70, "the Lobeck block"). The house had a DEM in
 * three forms (AKS.loadDEM for scribed plan views, akvalley ridgeline strokes,
 * akrelief hillshade) and no way to make one into an OBJECT: a milled block
 * with cut walls standing on a table, the way Lobeck and Davis drew landforms
 * and the way a relief model sits in a hearing room. That is a PBR job, so this
 * module builds three.js meshes and leaves lights, camera and snapshot to
 * akthree.
 *
 *   import * as AKBLOCKmod from '@@ASSETS@@/js/akblock.js';
 *   const AKBLOCK = AKBLOCKmod.init(THREE);
 *   const dem = await AKBLOCK.loadDEM('@@ASSETS@@/geo/ak-kachemak-dem');
 *   const blk = AKBLOCK.build(dem, { origin:[lon,lat], bearing:43.5,
 *                                    u:[-1.5,10.5], v:[-8,0], step:0.03, ve:2 });
 *   AKT.add(R, blk.group);
 *
 * FRAME. The block lives in a local (u, v) frame in KILOMETRES: u runs along
 * `bearing` (degrees clockwise from north) from `origin`, v runs 90 degrees
 * counter-clockwise from u (to the LEFT of u). World: x = u, z = -v, y = height
 * in km times `ve`. With bearing 90 that is x = east, z = -north, the ordinary
 * north-up plan. Any other bearing lets one wall of the block be a SECTION
 * along an arbitrary line (a tunnel, a pipeline), which is the point.
 *
 * HONESTY. Vertical exaggeration is a parameter and the slide must print it.
 * Heights are the DEM's, bilinear, with no noise added: invented sub-cell
 * relief would be fabricated geography. Water is found by the DEM's own
 * flatness (sea at or below `seaLevel`, a lake by `lakes: [{level, bbox}]`),
 * never painted in by hand.
 *
 * PLATE CARREE, CELL CENTRES: column i is lon west + i*dlon, row j is lat
 * north - j*dlat, exactly as the DEM json's own `projection` string says.
 */
export function init(THREE) {
  const B = {};
  const RAD = Math.PI / 180;

  B.loadDEM = async function (base) {
    const meta = await (await fetch(base + '.json')).json();
    const buf = await (await fetch(base + '.bin')).arrayBuffer();
    return { meta, z: new Int16Array(buf) };
  };

  /* bilinear height in metres at (lon, lat); NaN outside the grid */
  B.sampler = function (dem) {
    const m = dem.meta, z = dem.z, C = m.cols, Rr = m.rows;
    return function (lon, lat) {
      const x = (lon - m.west) / m.dlon, y = (m.north - lat) / m.dlat;
      const i = Math.floor(x), j = Math.floor(y);
      if (i < 0 || j < 0 || i >= C - 1 || j >= Rr - 1) return NaN;
      const fx = x - i, fy = y - j, k = j * C + i;
      return z[k] * (1 - fx) * (1 - fy) + z[k + 1] * fx * (1 - fy) +
             z[k + C] * (1 - fx) * fy + z[k + C + 1] * fx * fy;
    };
  };

  /* the local frame: km per degree at the origin's latitude */
  B.frame = function (origin, bearing) {
    const kx = Math.cos(origin[1] * RAD) * 111.32, ky = 111.2;
    const ex = Math.sin(bearing * RAD), ey = Math.cos(bearing * RAD);  // u, in (east, north)
    return {
      kx, ky, ex, ey,
      toLL(u, v) {            // v is to the LEFT of u: (east, north) = u*e + v*(-ey, ex)
        const E = u * ex - v * ey, Nn = u * ey + v * ex;
        return [origin[0] + E / kx, origin[1] + Nn / ky];
      },
      toUV(lon, lat) {
        const E = (lon - origin[0]) * kx, Nn = (lat - origin[1]) * ky;
        return [E * ex + Nn * ey, -E * ey + Nn * ex];
      }
    };
  };

  /* default hypsometric + slope ramp, glacial flour and low sun palette */
  const RAMP = [
    [0, [0.150, 0.205, 0.190]], [250, [0.215, 0.275, 0.255]], [500, [0.300, 0.345, 0.345]],
    [750, [0.400, 0.440, 0.455]], [950, [0.560, 0.600, 0.620]], [1150, [0.780, 0.830, 0.850]],
    [1400, [0.900, 0.940, 0.950]], [1800, [0.940, 0.965, 0.975]]];
  function ramp(e) {
    if (e <= RAMP[0][0]) return RAMP[0][1].slice();
    for (let k = 1; k < RAMP.length; k++) {
      if (e <= RAMP[k][0]) {
        const t = (e - RAMP[k - 1][0]) / (RAMP[k][0] - RAMP[k - 1][0]);
        return RAMP[k - 1][1].map((c, q) => c + (RAMP[k][1][q] - c) * t);
      }
    }
    return RAMP[RAMP.length - 1][1].slice();
  }
  B.ramp = ramp;

  /* strata texture for the cut walls: level bands keyed to world height */
  function strataTexture(o) {
    const c = document.createElement('canvas'); c.width = 64; c.height = 1024;
    const g = c.getContext('2d');
    const rng = mulberry(o.seed || 7071);
    let y = 0;
    const tones = o.tones || ['#4A5864', '#3A4852', '#56646F', '#34424C', '#44525D'];
    while (y < 1024) {
      const h = 10 + rng() * 46;
      g.fillStyle = tones[Math.floor(rng() * tones.length)];
      g.fillRect(0, y, 64, h + 1);
      g.fillStyle = 'rgba(20,28,36,0.45)'; g.fillRect(0, y, 64, 1.6);
      y += h;
    }
    /* a light drafting crosshatch over the bands, so a cut wall reads as rock in section */
    g.strokeStyle = 'rgba(20,30,40,0.35)'; g.lineWidth = 1.2;
    for (let k = -1024; k < 1088; k += 9) { g.beginPath(); g.moveTo(k, 1024); g.lineTo(k + 1024, 0); g.stroke(); }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }
  function mulberry(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  /*
   * build(dem, o) -> { group, top, lake, sea, walls, section, frame, height,
   *                    world(u, v, metres), worldLL(lon, lat, metres), dims }
   *
   * o.origin [lon,lat], o.bearing deg, o.u [u0,u1] km, o.v [v0,v1] km,
   * o.step km (grid pitch), o.ve vertical exaggeration, o.base km below sea
   * level for the block's floor (positive number), o.seaLevel metres,
   * o.lakes [{level, tol, bbox:[w,s,e,n]}], o.sectionEdge 'v0'|'v1'|'u0'|'u1'
   * names the wall that gets o.sectionMaterial instead of strata.
   */
  B.build = function (dem, o) {
    const S = B.sampler(dem), F = B.frame(o.origin, o.bearing || 90);
    const u0 = o.u[0], u1 = o.u[1], v0 = o.v[0], v1 = o.v[1];
    const step = o.step || 0.04, ve = o.ve || 2, base = o.base != null ? o.base : 0.6;
    const seaLevel = o.seaLevel != null ? o.seaLevel : 0.5;
    const NU = Math.round((u1 - u0) / step) + 1, NV = Math.round((v1 - v0) / step) + 1;
    const hm = new Float32Array(NU * NV);           // metres
    const kind = new Uint8Array(NU * NV);           // 0 land, 1 sea, 2 lake
    const lakes = o.lakes || [];
    for (let j = 0; j < NV; j++) {
      const v = v0 + (v1 - v0) * j / (NV - 1);
      for (let i = 0; i < NU; i++) {
        const u = u0 + (u1 - u0) * i / (NU - 1);
        const ll = F.toLL(u, v);
        let e = S(ll[0], ll[1]);
        if (!isFinite(e)) e = 0;
        const k = j * NU + i;
        if (e <= seaLevel) { kind[k] = 1; e = Math.max(e, -30); }
        for (const L of lakes) {
          const b = L.bbox;
          if (ll[0] >= b[0] && ll[0] <= b[2] && ll[1] >= b[1] && ll[1] <= b[3] &&
              Math.abs(e - L.level) <= (L.tol || 1.5)) { kind[k] = 2; e = L.level; }
        }
        hm[k] = e;
      }
    }
    const Y = (m) => m / 1000 * ve;
    const X = (i) => u0 + (u1 - u0) * i / (NU - 1);
    const Zc = (j) => -(v0 + (v1 - v0) * j / (NV - 1));

    /* ---- the top surface, vertex coloured ---- */
    const pos = new Float32Array(NU * NV * 3), col = new Float32Array(NU * NV * 3);
    for (let j = 0; j < NV; j++) for (let i = 0; i < NU; i++) {
      const k = j * NU + i;
      pos[k * 3] = X(i); pos[k * 3 + 1] = Y(kind[k] === 1 ? Math.min(hm[k], 0) - 25 : hm[k]);
      pos[k * 3 + 2] = Zc(j);
      const c = (o.ramp || ramp)(hm[k]);
      col[k * 3] = c[0]; col[k * 3 + 1] = c[1]; col[k * 3 + 2] = c[2];
    }
    const idx = [];
    for (let j = 0; j < NV - 1; j++) for (let i = 0; i < NU - 1; i++) {
      const a = j * NU + i, b = a + 1, c = a + NU, d = c + 1;
      /* +u is +x and +v is -z, so (a, b, c) winds counter-clockwise seen from
       * above: the normal points UP. (a, c, b) lit the underside instead. */
      idx.push(a, b, c, b, d, c);
    }
    const tg = new THREE.BufferGeometry();
    tg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    tg.setAttribute('color', new THREE.BufferAttribute(col, 3));
    tg.setIndex(idx); tg.computeVertexNormals();
    /* slope tint AFTER normals: steep faces go toward bare rock */
    const nrm = tg.getAttribute('normal');
    const rock = o.rock || [0.23, 0.28, 0.32];
    for (let k = 0; k < NU * NV; k++) {
      const ny = nrm.getY(k), s = Math.min(1, Math.max(0, (0.86 - ny) / 0.30));
      if (kind[k] !== 0) continue;
      col[k * 3] += (rock[0] - col[k * 3]) * s * 0.7;
      col[k * 3 + 1] += (rock[1] - col[k * 3 + 1]) * s * 0.7;
      col[k * 3 + 2] += (rock[2] - col[k * 3 + 2]) * s * 0.7;
    }
    tg.getAttribute('color').needsUpdate = true;
    const topMat = o.topMaterial || new THREE.MeshStandardMaterial({
      vertexColors: true, roughness: 0.88, metalness: 0.0 });
    const top = new THREE.Mesh(tg, topMat);

    /* ---- water: flat meshes over the cells the DEM itself says are water ---- */
    function waterMesh(which, yWorld, mat) {
      const wi = [];
      for (let j = 0; j < NV - 1; j++) for (let i = 0; i < NU - 1; i++) {
        const a = j * NU + i, b = a + 1, c = a + NU, d = c + 1;
        const n = (kind[a] === which) + (kind[b] === which) + (kind[c] === which) + (kind[d] === which);
        if (n >= 3) wi.push(a, b, c, b, d, c);
      }
      if (!wi.length) return null;
      const wp = new Float32Array(NU * NV * 3);
      for (let k = 0; k < NU * NV; k++) { wp[k * 3] = pos[k * 3]; wp[k * 3 + 1] = yWorld; wp[k * 3 + 2] = pos[k * 3 + 2]; }
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(wp, 3));
      g.setIndex(wi); g.computeVertexNormals();
      return new THREE.Mesh(g, mat);
    }
    const lakeMat = o.lakeMaterial || new THREE.MeshPhysicalMaterial({
      color: 0x8ccfc4, roughness: 0.14, metalness: 0.0, clearcoat: 0.6, clearcoatRoughness: 0.2 });
    const seaMat = o.seaMaterial || new THREE.MeshPhysicalMaterial({
      color: 0x0e2a3a, roughness: 0.2, metalness: 0.0, clearcoat: 0.4 });
    const lake = lakes.length ? waterMesh(2, Y(lakes[0].level) + 0.002, lakeMat) : null;
    const sea = waterMesh(1, Y(0) + 0.002, seaMat);

    /* ---- the cut walls ---- */
    const H0 = o.wallSpan || 4.0;              // world units of height the strata texture spans
    const strata = strataTexture({ seed: o.seed });
    strata.repeat.set(1, 1);
    const wallMat = o.wallMaterial || new THREE.MeshStandardMaterial({
      map: strata, roughness: 0.92, metalness: 0.0 });
    function wall(points, mat, flip) {           // points: [[x, yTop, z, s]] along the edge
      const n = points.length, wp = new Float32Array(n * 2 * 3), uv = new Float32Array(n * 2 * 2);
      for (let q = 0; q < n; q++) {
        const p = points[q];
        wp.set([p[0], p[1], p[2]], q * 6); wp.set([p[0], -base, p[2]], q * 6 + 3);
        uv.set([p[3], (p[1] + base) / H0], q * 4); uv.set([p[3], 0], q * 4 + 2);
      }
      const wi = [];
      for (let q = 0; q < n - 1; q++) {
        const a = q * 2, b = a + 1, c = a + 2, d = a + 3;
        if (flip) wi.push(a, c, b, b, c, d); else wi.push(a, b, c, b, d, c);
      }
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(wp, 3));
      g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
      g.setIndex(wi); g.computeVertexNormals();
      return new THREE.Mesh(g, mat);
    }
    const edgeTop = (k) => Math.max(pos[k * 3 + 1], Y(0));
    const e_v0 = [], e_v1 = [], e_u0 = [], e_u1 = [];
    for (let i = 0; i < NU; i++) {
      const k0 = i, k1 = (NV - 1) * NU + i, s = i / (NU - 1);
      e_v0.push([pos[k0 * 3], edgeTop(k0), pos[k0 * 3 + 2], s]);
      e_v1.push([pos[k1 * 3], edgeTop(k1), pos[k1 * 3 + 2], s]);
    }
    for (let j = 0; j < NV; j++) {
      const k0 = j * NU, k1 = j * NU + NU - 1, s = j / (NV - 1);
      e_u0.push([pos[k0 * 3], edgeTop(k0), pos[k0 * 3 + 2], s]);
      e_u1.push([pos[k1 * 3], edgeTop(k1), pos[k1 * 3 + 2], s]);
    }
    const sec = o.sectionEdge;
    const walls = {
      /* outward normals: the v0 wall faces +z, v1 faces -z, u0 faces -x, u1 faces +x */
      v0: wall(e_v0, sec === 'v0' ? o.sectionMaterial : wallMat, false),
      v1: wall(e_v1, sec === 'v1' ? o.sectionMaterial : wallMat, true),
      u0: wall(e_u0, sec === 'u0' ? o.sectionMaterial : wallMat, true),
      u1: wall(e_u1, sec === 'u1' ? o.sectionMaterial : wallMat, false)
    };
    Object.values(walls).forEach(w => { w.material.side = THREE.DoubleSide; });

    /* the floor under the block, so a shadow map sees a closed solid */
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(u1 - u0, v1 - v0),
      new THREE.MeshStandardMaterial({ color: 0x0c1c28, roughness: 1 }));
    floor.rotation.x = Math.PI / 2;
    floor.position.set((u0 + u1) / 2, -base, -(v0 + v1) / 2);

    const group = new THREE.Group();
    group.add(top); if (lake) group.add(lake); if (sea) group.add(sea);
    Object.values(walls).forEach(w => group.add(w)); group.add(floor);

    return {
      group, top, lake, sea, walls, floor, frame: F, ve, base, NU, NV, hm, kind,
      dims: { u0, u1, v0, v1, step },
      height: (u, v) => { const ll = F.toLL(u, v); return S(ll[0], ll[1]); },
      world: (u, v, m) => new THREE.Vector3(u, Y(m), -v),
      worldLL: (lon, lat, m) => { const uv = F.toUV(lon, lat); return new THREE.Vector3(uv[0], Y(m), -uv[1]); },
      /* the profile along the v = vEdge wall, as [[u, metres]] */
      profile: (vEdge, n) => {
        const out = []; n = n || 400;
        for (let q = 0; q <= n; q++) {
          const u = u0 + (u1 - u0) * q / n, ll = F.toLL(u, vEdge);
          let e = S(ll[0], ll[1]); if (!isFinite(e)) e = 0;
          out.push([u, e]);
        }
        return out;
      }
    };
  };

  return B;
}
