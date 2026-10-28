/* aklath.js — the undriven survey lath on the parcel's litter, under one off-camera flash.
 * (Alaska.Ai, No.97, 2026-10-27.) An ES module for akthree slides: the deck's two bookends (01 and 09)
 * share this scene, this camera and this flash, so the only things that change between them are the
 * ground's season and the closed field book, which is the point of the bookend.
 *
 *   const THREE = await import('@@ASSETS@@/js/three.module.min.js');
 *   const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
 *   const L = (await import('@@ASSETS@@/js/aklath.js')).init(THREE, AKT);
 *   const gl = document.createElement('canvas'); gl.width = 2160; gl.height = 2700;
 *   const R = AKT.setup(gl, {w: 1080, h: 1350, bg: 0x030508, exposure: 1.0});
 *   const S = L.build(R, {season: 'litter' | 'snow', book: false | true, seed});
 *   L.camera(R);                     // the locked camera both frames share
 *   S.points                         // world anchors: tagCentre, rollCentre, lathFar, lathNear, foot
 *
 * Units are metres. The ground is y = 0. The lath lies on the litter on a diagonal, its pointed end
 * toward the lens. The flash is a SpotLight up and to the left of the lens, decay 2, so the pool falls
 * off by the inverse square and the top of the frame is ground far enough away to be night.
 * Every texture is drawn on a canvas from a seed, nothing is loaded, nothing calls Math.random.
 * Text never goes in here; type stays DOM.
 */
export function init(THREE, AKT) {
  const L = {};

  function rng(seed) {                                   // mulberry32, same as noise.js
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0; let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function vnoise(seed) {                                // smooth value noise, 2D, for textures
    const r = rng(seed), P = new Float32Array(256 * 256);
    for (let i = 0; i < P.length; i++) P[i] = r();
    const at = (x, y) => P[((y & 255) << 8) | (x & 255)];
    const s = t => t * t * (3 - 2 * t);
    const n = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), fx = s(x - xi), fy = s(y - yi);
      const a = at(xi, yi), b = at(xi + 1, yi), c = at(xi, yi + 1), d = at(xi + 1, yi + 1);
      return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy; };
    return (x, y, oct) => { let v = 0, amp = 0.5, f = 1, tot = 0;
      for (let o = 0; o < (oct || 4); o++) { v += amp * n(x * f, y * f); tot += amp; amp *= 0.5; f *= 2.03; }
      return v / tot; };
  }
  const hex = h => [((h >> 16) & 255) / 255, ((h >> 8) & 255) / 255, (h & 255) / 255];
  const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];

  /* THE LOCKED CAMERA. Height 0.55 m, looking down at the lath's tagged end; the top ray meets the
   * ground about 6.5 m out, so the upper frame is far litter at the flash's inverse-square tail. */
  L.CAM = { from: [0.02, 0.50, 0.84], look: [0.36, 0.0, -0.62], fov: 33 };
  L.FLASH = { pos: [-0.30, 0.84, -0.02], aim: [0.30, 0.0, -0.26] };
  L.camera = function (R) {
    AKT.frame(R, { from: L.CAM.from, look: L.CAM.look, fov: L.CAM.fov });
    R.camera.near = 0.05; R.camera.far = 30; R.camera.updateProjectionMatrix();
  };

  /* ground albedo: dark wet soil and moss under the litter, or snow with litter showing through */
  function groundTexture(season, seed) {
    const N = 2048, c = document.createElement('canvas'); c.width = c.height = N;
    const g = c.getContext('2d'), img = g.createImageData(N, N), d = img.data;
    const f = vnoise(seed), f2 = vnoise(seed + 7);
    const soil = hex(0x17110c), moss = hex(0x262a1c), umber = hex(0x3a2416), snow = hex(0xe9eef1), shade = hex(0xb9c6cf);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const u = x / N * 48, v = y / N * 48;
      const a = f(u, v, 5), b = f2(u * 3.1, v * 3.1, 3);
      let col = mix(soil, moss, Math.max(0, Math.min(1, (a - 0.42) * 3.2)));
      col = mix(col, umber, Math.max(0, (b - 0.62) * 2.2));
      if (season === 'snow') {
        const m = f2(u * 0.7 + 9, v * 0.7, 4);
        const cover = Math.max(0, Math.min(1, (m - 0.36) * 5.0));
        col = mix(col, mix(shade, snow, b), cover);
      }
      const k = (y * N + x) * 4;
      d[k] = col[0] * 255; d[k + 1] = col[1] * 255; d[k + 2] = col[2] * 255; d[k + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    return t;
  }

  /* a birch leaf: ovate, serrate, a midrib and seven pairs of straight veins; white so instanceColor tints it */
  function leafTexture(seed) {
    const N = 256, c = document.createElement('canvas'); c.width = c.height = N;
    const g = c.getContext('2d'), r = rng(seed);
    g.clearRect(0, 0, N, N);
    g.save(); g.translate(N / 2, N * 0.94);
    g.beginPath();
    const pts = [];
    for (let i = 0; i <= 80; i++) {
      // up the right edge from the petiole to the tip, then back down the left: ovate, widest a third of
      // the way up, pointed tip, a doubly serrate margin
      const t = i / 80, side = t <= 0.5 ? 1 : -1, s = t <= 0.5 ? t * 2 : (1 - t) * 2;   // s: 0 base .. 1 tip
      const w = Math.pow(Math.sin(Math.PI * Math.pow(s, 0.72)), 0.9) * 0.36;
      const ser = 1 + (s > 0.08 && s < 0.97 ? 0.07 * Math.abs(Math.sin(i * 1.9)) + 0.03 * Math.sin(i * 4.3) : 0);
      pts.push([side * w * ser * N, -s * N * 0.86]);
    }
    g.moveTo(pts[0][0], pts[0][1]);
    for (const p of pts) g.lineTo(p[0], p[1]);
    g.closePath();
    g.fillStyle = '#f2ece2'; g.fill();
    g.clip();
    // veins: a midrib and straight laterals, darker; a mottled blade
    for (let i = 0; i < 900; i++) {
      g.fillStyle = 'rgba(120,90,60,' + (0.04 + r() * 0.08).toFixed(3) + ')';
      g.beginPath(); g.arc((r() - 0.5) * N * 0.8, -r() * N * 0.86, 1 + r() * 4, 0, Math.PI * 2); g.fill();
    }
    g.strokeStyle = 'rgba(96,70,44,0.55)'; g.lineWidth = 3;
    g.beginPath(); g.moveTo(0, 0); g.lineTo(0, -N * 0.84); g.stroke();
    g.lineWidth = 1.4; g.strokeStyle = 'rgba(96,70,44,0.42)';
    for (let k = 1; k <= 7; k++) {
      const y0 = -N * 0.84 * (k / 8.4);
      for (const s of [-1, 1]) { g.beginPath(); g.moveTo(0, y0); g.lineTo(s * N * 0.32, y0 - N * 0.13); g.stroke(); }
    }
    g.restore();
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }

  /* sawn pine, grain along the length, one knot, the top end cut square */
  function pineTexture(seed) {
    const W = 2048, H = 96, c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d'), img = g.createImageData(W, H), d = img.data, f = vnoise(seed);
    const lit = hex(0xc9a473), dark = hex(0x8c6438);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const w = f(x / 260, y / 30, 3);
      const kx = x - 1320, ky = y - 40, kd = Math.hypot(kx * 0.6, ky);
      const swirl = kd < 60 ? Math.sin(kd * 0.5) * (1 - kd / 60) * 3 : 0;
      // growth rings run the length; the warp stays small so they never close into a fingerprint
      // ring pitch wanders and each ring has its own strength, so the board never reads as ruled
      const rc = y + w * 5 + swirl * 6 + f(x / 900, y / 18, 2) * 22;
      const grain = 0.5 + 0.5 * Math.sin(rc * 0.62), amp = 0.3 + 0.7 * f(x / 320, rc / 9, 2);
      const streak = f(x / 520, y / 2.5, 2) - 0.5, resin = Math.max(0, f(x / 1400, y / 5, 1) - 0.72) * 2.2;
      let col = mix(lit, dark, Math.pow(grain, 3) * 0.26 * amp + streak * 0.24 + resin * 0.5 + (f(x / 60, y / 6, 2) - 0.5) * 0.10);
      if (kd < 9) col = mix(col, hex(0x5b3c1e), 1 - kd / 9);
      const k = (y * W + x) * 4;
      d[k] = col[0] * 255; d[k + 1] = col[1] * 255; d[k + 2] = col[2] * 255; d[k + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }

  /* kraft card with fibre tooth and a reinforcement ring around the eyelet */
  function kraftTexture(seed) {
    const N = 512, c = document.createElement('canvas'); c.width = N; c.height = N / 2;
    const g = c.getContext('2d'), img = g.createImageData(N, N / 2), d = img.data, f = vnoise(seed), r = rng(seed + 3);
    const base = hex(0xc8a779), lee = hex(0xa88757);
    for (let y = 0; y < N / 2; y++) for (let x = 0; x < N; x++) {
      const v = f(x / 9, y / 9, 3) * 0.6 + f(x / 2.2, y / 30, 2) * 0.4;
      const col = mix(base, lee, Math.max(0, Math.min(1, (v - 0.35) * 1.4)));
      const k = (y * N + x) * 4;
      d[k] = col[0] * 255; d[k + 1] = col[1] * 255; d[k + 2] = col[2] * 255; d[k + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    for (let i = 0; i < 260; i++) { g.strokeStyle = 'rgba(90,64,34,' + (0.08 + r() * 0.12).toFixed(3) + ')'; g.lineWidth = 0.6;
      const x = r() * N, y = r() * N / 2, a = r() * Math.PI; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * 8, y + Math.sin(a) * 8); g.stroke(); }
    g.strokeStyle = 'rgba(122,97,66,0.9)'; g.lineWidth = 10; g.beginPath(); g.arc(N * 0.1, N / 4, 22, 0, Math.PI * 2); g.stroke();
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    return t;
  }

  L.build = function (R, o) {
    o = o || {};
    const season = o.season || 'litter', seed = o.seed || 20261027, r = rng(seed);
    const S = { points: {} };
    const snow = season === 'snow';

    /* light: one off-camera flash, and almost nothing else */
    const flash = new THREE.SpotLight(0xfff6e8, snow ? 4.2 : 5.2, 0, 0.56, 0.98, 2.0);
    flash.position.set(...L.FLASH.pos);
    flash.target.position.set(...L.FLASH.aim);
    flash.castShadow = true;
    flash.shadow.mapSize.set(4096, 4096);
    flash.shadow.camera.near = 0.3; flash.shadow.camera.far = 6;
    flash.shadow.bias = -0.00025; flash.shadow.radius = 5;
    R.scene.add(flash); R.scene.add(flash.target);
    R.scene.add(snow ? new THREE.HemisphereLight(0x8a9cb2, 0x2a3240, 0.34) : new THREE.HemisphereLight(0x1a2433, 0x07090c, 0.10));   // snow throws cool fill into its own casts
    // a faint bounce from the camera's right so a lee face sits two steps down, not in black
    const bounce = new THREE.DirectionalLight(0x9fb0c4, 0.34); bounce.position.set(1.4, 0.7, 1.6); R.scene.add(bounce);
    R.scene.fog = new THREE.FogExp2(0x030508, 0.34);

    /* the ground */
    const gtex = groundTexture(season, seed);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(9, 9, 1, 1),
      new THREE.MeshStandardMaterial({ map: gtex, roughness: snow ? 0.82 : 0.92, metalness: 0 }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(0.2, 0, -2.2);
    AKT.add(R, ground, { cast: false });

    /* the litter: three curl variants of one birch leaf, instanced */
    const ltex = leafTexture(seed + 11);
    const leafMat = new THREE.MeshStandardMaterial({ map: ltex, alphaTest: 0.5, alphaToCoverage: true, side: THREE.DoubleSide,   // MSAA feathers the serrations
      roughness: snow ? 0.7 : 0.48, metalness: 0 });
    const amber = hex(0xc98a3e), mid = hex(0x8e5a2b), lee = hex(0x5a3a20), gold2 = hex(0xb07a30), snowc = hex(0xe8edf0);
    const curls = [0.10, 0.22, 0.34];
    const PER = 3600;
    const inLath = (x, z) => {                          // keep leaves from poking up through the lath
      const ax = -0.52, az = 0.56, bx = 0.36, bz = -0.22;
      const vx = bx - ax, vz = bz - az, t = Math.max(0, Math.min(1, ((x - ax) * vx + (z - az) * vz) / (vx * vx + vz * vz)));
      return Math.hypot(x - (ax + vx * t), z - (az + vz * t)) < 0.026
        || Math.hypot(x - 0.40, z + 0.25) < 0.085;        // and off the tag, so the bookend's blank tag always reads
    };
    curls.forEach((cu, ci) => {
      const geo = new THREE.PlaneGeometry(1, 1, 8, 8);
      geo.rotateX(-Math.PI / 2);
      const p = geo.attributes.position;
      for (let i = 0; i < p.count; i++) {
        const x = p.getX(i), z = p.getZ(i);
        p.setY(i, cu * (x * x) * 1.6 + 0.10 * cu * (z + 0.5) * (z + 0.5));
      }
      geo.computeVertexNormals();
      const mesh = new THREE.InstancedMesh(geo, leafMat, PER);
      const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), sc = new THREE.Vector3(), ps = new THREE.Vector3();
      const col = new THREE.Color();
      let n = 0;
      while (n < PER) {
        // denser near the pool, thinning with distance (the camera only sees the pool well)
        const rr = Math.pow(r(), 0.62) * 1.9, th = r() * Math.PI * 2;
        const x = 0.12 + Math.cos(th) * rr * 1.2, z = -0.18 + Math.sin(th) * rr;
        if (inLath(x, z)) continue;
        const s = 0.03 + r() * 0.024;
        e.set((r() - 0.5) * 0.24, r() * Math.PI * 2, (r() - 0.5) * 0.24);
        q.setFromEuler(e); sc.set(s, s * (0.8 + r() * 0.5), s);
        ps.set(x, 0.0015 + s * 0.07 + r() * 0.006 + n / PER * 0.004, z);   // a tilted leaf's low edge stays above the ground
        m4.compose(ps, q, sc); mesh.setMatrixAt(n, m4);
        const u = r(); let c = u < 0.18 ? mix(lee, hex(0x2c1c10), r()) : u < 0.42 ? mix(mid, lee, r() * 0.7) : mix(mix(amber, mid, r() * 0.8), gold2, r() * 0.5);
        if (snow && r() < 0.4) c = mix(c, snowc, 0.3 + r() * 0.3);   // first snow dusts the litter
        col.setRGB(c[0], c[1], c[2], THREE.SRGBColorSpace); mesh.setColorAt(n, col);
        n++;
      }
      mesh.instanceMatrix.needsUpdate = true; mesh.instanceColor.needsUpdate = true;
      AKT.add(R, mesh);
    });

    /* twigs */
    const twigMat = new THREE.MeshStandardMaterial({ color: 0x3a2a1c, roughness: 0.9 });
    for (let i = 0; i < 46; i++) {
      const rr = Math.pow(r(), 0.7) * 2.0, th = r() * Math.PI * 2;
      const x = 0.05 + Math.cos(th) * rr * 1.2, z = -0.5 + Math.sin(th) * rr, len = 0.08 + r() * 0.22, a = r() * Math.PI;
      if (inLath(x, z) || inLath(x + Math.cos(a) * len, z + Math.sin(a) * len)) continue;
      const pts = [];
      for (let k = 0; k <= 4; k++) { const t = k / 4;
        pts.push(new THREE.Vector3(x + Math.cos(a) * len * t + (r() - 0.5) * 0.01, 0.006 + r() * 0.004, z + Math.sin(a) * len * t + (r() - 0.5) * 0.01)); }
      const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 16, 0.0016 + r() * 0.0018, 6), twigMat);
      AKT.add(R, tube);
    }

    /* the lath: 1 m of sawn pine, 38 x 9 mm, lying flat, its point toward the lens */
    const A = new THREE.Vector3(-0.52, 0, 0.56), B = new THREE.Vector3(0.36, 0, -0.22);
    const dir = B.clone().sub(A), len = dir.length(); dir.normalize();
    const yaw = Math.atan2(-dir.z, dir.x);
    const pine = pineTexture(seed + 21);
    const wood = new THREE.MeshPhysicalMaterial({ map: pine, roughness: 0.38, metalness: 0, clearcoat: 0.5, clearcoatRoughness: 0.3 });
    const endGrain = new THREE.MeshStandardMaterial({ color: 0xb08a5c, roughness: 0.8 });
    const body = new THREE.Mesh(new THREE.BoxGeometry(len - 0.07, 0.009, 0.038),
      [endGrain, endGrain, wood, wood, wood, wood]);
    const lath = new THREE.Group();
    body.position.set(0.035, 0.0045, 0);
    lath.add(body);
    const tipShape = new THREE.Shape();
    tipShape.moveTo(0, -0.019); tipShape.lineTo(0, 0.019); tipShape.lineTo(-0.07, 0.002); tipShape.lineTo(-0.07, -0.002); tipShape.closePath();
    const tipGeo = new THREE.ExtrudeGeometry(tipShape, { depth: 0.009, bevelEnabled: false });
    tipGeo.rotateX(-Math.PI / 2);
    const tip = new THREE.Mesh(tipGeo, wood);
    tip.position.set(-(len - 0.07) / 2 + 0.035, 0, 0);
    lath.add(tip);
    const lathY = 0.0105;
    lath.position.set((A.x + B.x) / 2, lathY, (A.z + B.z) / 2);
    lath.rotation.y = yaw;
    AKT.add(R, lath);

    const far = B.clone().add(dir.clone().multiplyScalar(-0.01)); far.y = lathY + 0.009;
    S.points.lathFar = [far.x, far.y, far.z];
    S.points.lathNear = [A.x, lathY + 0.009, A.z];
    S.points.foot = [(A.x + B.x) * 0.5 + 0.12 * dir.x, 0.0, (A.z + B.z) * 0.5 + 0.12 * dir.z];

    /* the sealed flagging roll, beside the far end */
    const side = new THREE.Vector3(-dir.z, 0, dir.x);   // perpendicular, to the right of the lath's run
    const rollPos = B.clone().add(side.clone().multiplyScalar(-0.075)).add(dir.clone().multiplyScalar(-0.07));
    const roll = new THREE.Group();
    const ribbonMat = new THREE.MeshStandardMaterial({ color: 0xe8e2d4, roughness: 0.34, metalness: 0 });
    const coreMat = new THREE.MeshStandardMaterial({ color: 0x5b4632, roughness: 0.85 });
    const outer = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.026, 64, 1, true), ribbonMat);
    const capProfile = [];                                // the wound face: annular disc with wound rings in its height
    const ringGeo = new THREE.RingGeometry(0.0115, 0.03, 64, 6);
    const face1 = new THREE.Mesh(ringGeo, ribbonMat), face2 = new THREE.Mesh(ringGeo, ribbonMat);
    face1.position.y = 0.013; face1.rotation.x = -Math.PI / 2;
    face2.position.y = -0.013; face2.rotation.x = Math.PI / 2;
    const core = new THREE.Mesh(new THREE.CylinderGeometry(0.0115, 0.0115, 0.027, 32, 1, true), coreMat);
    core.material.side = THREE.DoubleSide;
    roll.add(outer, face1, face2, core);
    roll.rotation.z = Math.PI / 2; roll.rotation.y = yaw + 0.5;
    roll.position.set(rollPos.x, 0.03 + 0.003, rollPos.z);
    if (o.roll) AKT.add(R, roll);
    S.points.rollCentre = [rollPos.x, 0.033, rollPos.z];
    void capProfile;

    /* the blank tag, lying on the litter past the end, tied to the lath with cotton string */
    const tagShape = new THREE.Shape();
    const tw = 0.078, th = 0.039, ch = 0.009;
    tagShape.moveTo(0, -th / 2 + ch); tagShape.lineTo(ch, -th / 2); tagShape.lineTo(tw, -th / 2); tagShape.lineTo(tw, th / 2);
    tagShape.lineTo(ch, th / 2); tagShape.lineTo(0, th / 2 - ch); tagShape.closePath();
    const hole = new THREE.Path(); hole.absarc(0.0078, 0, 0.0028, 0, Math.PI * 2, true); tagShape.holes.push(hole);
    const tagGeo = new THREE.ShapeGeometry(tagShape, 12);
    tagGeo.rotateX(-Math.PI / 2);
    const uv = tagGeo.attributes.uv;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) / tw, (uv.getY(i) + th / 2) / th);
    const tagMat = new THREE.MeshStandardMaterial({ map: kraftTexture(seed + 31), roughness: 0.86, side: THREE.DoubleSide });
    const tag = new THREE.Mesh(tagGeo, tagMat);
    const tagPos = B.clone().add(dir.clone().multiplyScalar(0.035)).add(side.clone().multiplyScalar(0.03));
    tag.position.set(tagPos.x, 0.012, tagPos.z);
    tag.rotation.y = yaw - 0.55; tag.rotation.z = 0.04;
    AKT.add(R, tag);
    S.points.tagCentre = [tagPos.x + Math.cos(yaw - 0.55) * tw * 0.5, 0.013, tagPos.z - Math.sin(yaw - 0.55) * tw * 0.5];
    const eyelet = new THREE.Vector3(tagPos.x + Math.cos(yaw - 0.55) * 0.0078, 0.0135, tagPos.z - Math.sin(yaw - 0.55) * 0.0078);
    const tie = B.clone().add(dir.clone().multiplyScalar(-0.03)); tie.y = lathY + 0.01;
    const strPts = [eyelet,
      eyelet.clone().lerp(tie, 0.35).add(new THREE.Vector3(0.006, 0.004, 0.012)),
      eyelet.clone().lerp(tie, 0.7).add(new THREE.Vector3(-0.004, 0.006, 0.004)),
      tie,
      tie.clone().add(side.clone().multiplyScalar(-0.022)).add(new THREE.Vector3(0, -0.006, 0))];
    const string = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(strPts), 48, 0.0011, 6),
      new THREE.MeshStandardMaterial({ color: 0xd8d2c4, roughness: 0.9 }));
    AKT.add(R, string);
    const wrap = new THREE.Mesh(new THREE.TorusGeometry(0.0195, 0.0013, 6, 32),
      new THREE.MeshStandardMaterial({ color: 0xd8d2c4, roughness: 0.9 }));
    wrap.position.copy(tie); wrap.position.y = lathY + 0.0045;
    wrap.rotation.y = yaw; wrap.scale.set(1, 0.32, 1);
    AKT.add(R, wrap);

    /* snow: a skiff laid over the litter as a displaced sheet, deeper in hollows and in the lath's lee,
     * so leaves poke through where it thins; never a recoloured leaf */
    if (snow) {
      const sn = vnoise(seed + 41), SZ = 3.2, SEG = 320;
      const sg = new THREE.PlaneGeometry(SZ, SZ, SEG, SEG);
      sg.rotateX(-Math.PI / 2);
      const sp = sg.attributes.position;
      for (let i = 0; i < sp.count; i++) {
        const x = sp.getX(i) + 0.15, z = sp.getZ(i) - 0.3;
        const n = sn(x * 9 + 40, z * 9 + 40, 4), fine = sn(x * 60, z * 60, 2);
        // the lath's lee (the side away from the flash) holds a drift a few cm wide
        const ax = -0.52, az = 0.56, bx = 0.36, bz = -0.22, vx = bx - ax, vz = bz - az;
        const tt = Math.max(0, Math.min(1, ((x - ax) * vx + (z - az) * vz) / (vx * vx + vz * vz)));
        const px = ax + vx * tt, pz = az + vz * tt, dd = Math.hypot(x - px, z - pz);
        const sideSign = Math.sign((x - px) * (-vz) + (z - pz) * vx);
        const lee = sideSign > 0 && dd > 0.019 && dd < 0.07 ? (1 - (dd - 0.019) / 0.051) * 0.008 : 0;
        const mid = sn(x * 28 + 7, z * 28 + 3, 2);
        const h = Math.max(0, (n - 0.40) * 0.034) + mid * 0.0045 + fine * 0.0015 + lee;
        sp.setY(i, h - 0.0014);                       // continuous, so the skiff's edge is a smooth line where it meets the litter
        sp.setX(i, x); sp.setZ(i, z);
      }
      sg.computeVertexNormals();
      // crystal sparkle: a speckled roughness map so a few grains catch the flash
      const rc = document.createElement('canvas'); rc.width = rc.height = 1024;
      const rg = rc.getContext('2d'); rg.fillStyle = '#c4c4c4'; rg.fillRect(0, 0, 1024, 1024);
      const rr = rng(seed + 43); for (let i = 0; i < 26000; i++) { rg.fillStyle = rr() < 0.08 ? '#1a1a1a' : '#a0a0a0'; rg.fillRect(rr() * 1024, rr() * 1024, 1.2, 1.2); }
      const rtex = new THREE.CanvasTexture(rc); rtex.wrapS = rtex.wrapT = THREE.RepeatWrapping; rtex.repeat.set(10, 10);
      const skiff = new THREE.Mesh(sg, new THREE.MeshStandardMaterial({ color: 0xdce6ee, roughness: 1.0, roughnessMap: rtex, bumpMap: rtex, bumpScale: 2.5, metalness: 0 }));
      AKT.add(R, skiff);
    }

    /* the closed field book, resting across the lath on 09 */
    if (o.book) {
      const book = new THREE.Group();
      const bw = 0.095, bh = 0.15, bd = 0.011, rad = 0.004;   // 08's book, closed: a pocket field book
      // linen boards: a slate weave with paler scuffs toward the edges
      const cc = document.createElement('canvas'); cc.width = 512; cc.height = 800;
      const cg = cc.getContext('2d'), ci = cg.createImageData(512, 800), cd = ci.data, cf = vnoise(seed + 51);
      const slate = hex(0x4a5764), slateLo = hex(0x26303a), scuff = hex(0x6f7c88);   // 08's slate cover
      for (let y = 0; y < 800; y++) for (let x = 0; x < 512; x++) {
        const weave = 0.62 + 0.20 * (cf(x / 1.6, y / 1.6, 1) - 0.5) + 0.06 * (cf(x / 4, y / 4, 1) - 0.5);   // pebbled, like 08's board
        const edge = Math.min(x, 511 - x, y, 799 - y) / 40;
        let col = mix(slateLo, slate, Math.min(1, weave * 0.7 + cf(x / 30, y / 30, 3) * 0.5));
        col = mix(col, scuff, Math.max(0, (1 - Math.min(1, edge)) * 0.35 * cf(x / 6, y / 6, 2)));
        const k = (y * 512 + x) * 4; cd[k] = col[0] * 255; cd[k + 1] = col[1] * 255; cd[k + 2] = col[2] * 255; cd[k + 3] = 255;
      }
      cg.putImageData(ci, 0, 0);
      const ctex = new THREE.CanvasTexture(cc); ctex.colorSpace = THREE.SRGBColorSpace; ctex.anisotropy = 8;
      const cloth = new THREE.MeshPhysicalMaterial({ map: ctex, roughness: 0.55, sheen: 0.5, sheenColor: new THREE.Color(0x8a96a2), sheenRoughness: 0.6 });
      const pc = document.createElement('canvas'); pc.width = 64; pc.height = 256;
      const pg = pc.getContext('2d'); pg.fillStyle = '#ecede7'; pg.fillRect(0, 0, 64, 256);
      for (let i = 0; i < 256; i += 2) { pg.fillStyle = 'rgba(120,124,122,' + (0.10 + (i % 6 === 0 ? 0.12 : 0)).toFixed(2) + ')'; pg.fillRect(0, i, 64, 1); }
      const ptex = new THREE.CanvasTexture(pc); ptex.colorSpace = THREE.SRGBColorSpace;
      const block = new THREE.MeshStandardMaterial({ map: ptex, roughness: 0.92 });
      const rr = (w, h, r0) => { const s = new THREE.Shape(); const x0 = -w / 2, y0 = -h / 2;
        s.moveTo(x0 + r0, y0); s.lineTo(x0 + w - r0, y0); s.quadraticCurveTo(x0 + w, y0, x0 + w, y0 + r0);
        s.lineTo(x0 + w, y0 + h - r0); s.quadraticCurveTo(x0 + w, y0 + h, x0 + w - r0, y0 + h);
        s.lineTo(x0 + r0, y0 + h); s.quadraticCurveTo(x0, y0 + h, x0, y0 + h - r0); s.lineTo(x0, y0 + r0);
        s.quadraticCurveTo(x0, y0, x0 + r0, y0); return s; };
      const board = (y) => { const g = new THREE.ExtrudeGeometry(rr(bw, bh, rad), { depth: 0.0022, bevelEnabled: true,
          bevelThickness: 0.0006, bevelSize: 0.0008, bevelSegments: 2, curveSegments: 6 });
        g.rotateX(-Math.PI / 2);
        const uvb = g.attributes.uv; for (let i = 0; i < uvb.count; i++) uvb.setXY(i, uvb.getX(i) / bw + 0.5, uvb.getY(i) / bh + 0.5);
        const m = new THREE.Mesh(g, cloth); m.position.y = y; return m; };
      book.add(board(-bd / 2), board(bd / 2 - 0.0022));
      const pages = new THREE.Mesh(new THREE.BoxGeometry(bw - 0.002, bd - 0.0044, bh - 0.004), block);
      pages.position.x = 0.0012; book.add(pages);                      // the cream block shows at the fore edge
      // 08's gold ribbon: out of the tail edge, down onto the snow
      { const rp = new THREE.CatmullRomCurve3([new THREE.Vector3(0.012, 0.0, bh / 2 - 0.006), new THREE.Vector3(0.013, -0.003, bh / 2 + 0.006),
          new THREE.Vector3(0.016, -0.016, bh / 2 + 0.02), new THREE.Vector3(0.022, -0.021, bh / 2 + 0.045), new THREE.Vector3(0.032, -0.0205, bh / 2 + 0.072)]);
        const RW = 0.0095, RS = 60, rpos = [], ridx = [];
        for (let i = 0; i <= RS; i++) { const t = i / RS, q = rp.getPointAt(t), tg = rp.getTangentAt(t);
          const sx = new THREE.Vector3(1, 0, 0).addScaledVector(tg, -tg.x).normalize().multiplyScalar(RW / 2);   // the ribbon's width lies across the book
          rpos.push(q.x - sx.x, q.y - sx.y, q.z - sx.z, q.x + sx.x, q.y + sx.y, q.z + sx.z); }
        for (let i = 0; i < RS; i++) { const a = i * 2; ridx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
        const rg = new THREE.BufferGeometry(); rg.setAttribute('position', new THREE.Float32BufferAttribute(rpos, 3)); rg.setIndex(ridx); rg.computeVertexNormals();
        book.add(new THREE.Mesh(rg, new THREE.MeshPhysicalMaterial({ color: 0xffc72c, roughness: 0.38, sheen: 0.6, sheenColor: new THREE.Color(0xfff0c0), side: THREE.DoubleSide }))); }
      const spine = new THREE.Mesh(new THREE.CylinderGeometry(bd / 2, bd / 2, bh - 0.002, 16, 1, false, 0, Math.PI), cloth);
      void spine;
      const elastic = new THREE.Mesh(new THREE.BoxGeometry(0.0045, bd + 0.0018, bh + 0.001),
        new THREE.MeshStandardMaterial({ color: 0x15191e, roughness: 0.42 }));
      elastic.position.x = bw * 0.36; book.add(elastic);
      const at = A.clone().lerp(B, 0.78).add(side.clone().multiplyScalar(-0.07));   // beside the lath, clear of the tag at the far end
      book.position.set(at.x, lathY + 0.009 + bd / 2 - 0.0015, at.z);
      book.rotation.y = yaw + 1.18; book.rotation.z = 0.035;
      AKT.add(R, book);
      S.points.book = [at.x, lathY + 0.012, at.z];
    }
    return S;
  };

  return L;
}
