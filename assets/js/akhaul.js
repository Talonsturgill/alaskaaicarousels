/* akhaul.js — THE PLAIN WEST OF THE HAUL ROAD, Carousel No.112's GPU world (2026-11-11).
 *
 * One snow plain, one sky, one light, for the deck's rendered frames (01, 06,
 * 09). ES module, because akthree is one:
 *
 *   const THREE = await import('@@ASSETS@@/js/three.module.min.js');
 *   const AKT   = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
 *   const AKH   = (await import('@@ASSETS@@/js/akhaul.js')).init(THREE, AKT);
 *   const R = AKT.setup(glCanvas, {w:1080, h:1350, exposure:1.0});
 *   AKH.camera(R, {height:1.6, pitch:1.0, fov:50});       // looks due south (-z)
 *   AKH.plain(R, {seed:112011, near:1, far:3200});
 *   AKH.light(R, {stage:'twilight'});
 *   const hy = AKH.horizonY(R);                             // screen y of the horizon
 *   AKH.sky(R, {horizonY: hy, stage:'twilight'});
 *
 * WORLD. Metres; x east, y up, z north, the camera at the origin looking south
 * (-z) across the plain west of the Dalton. Nothing in this file is data: the
 * plain is an illustration of tundra snow (wind sastrugi from 200 degrees, low
 * drifts, a long swell) and the slides print no measurement on it.
 *
 * LIGHT. One key, the south sky glow at azimuth 180 and elevation 3 (the sun is
 * below the horizon at Milepost 390 in mid November at this hour), and a
 * hemisphere fill in the sky's own cobalt. The stage only changes intensities
 * and colours: twilight (01), deep (06), night (09, with an aurora fill from
 * above). The key never moves.
 *
 * GEOMETRY. The mesh is a FRUSTUM GRID: rows spaced geometrically in distance
 * and columns fanned to the field of view, so vertex density is highest where
 * the camera is closest. Sastrugi amplitude fades with distance so far rows
 * never alias into a comb.
 */
export function init(THREE, AKT) {
  const H = {};
  const STAGES = {
    twilight: { key: 0xEACBD3, keyI: 3.2, sky: 0x86A0D2, ground: 0x3A4C78, hemiI: 1.35,
                fog: 0x56688F, fogD: 0.0011,
                sky0: '#0B1A3A', sky1: '#18305E', sky2: '#2B3F6E', sky3: '#7D7FA3', sky4: '#C79A9E', sky5: '#E3D3CB' },
    deep:     { key: 0xC6AECF, keyI: 2.2, sky: 0x647EB6, ground: 0x2A3A64, hemiI: 0.95,
                fog: 0x34476F, fogD: 0.0016,
                sky0: '#070F26', sky1: '#10224A', sky2: '#1F3462', sky3: '#4A5885', sky4: '#8E7A93', sky5: '#B9A3AA' },
    night:    { key: 0x9C8EB0, keyI: 0.9, sky: 0x4F8FA0, ground: 0x0E1830, hemiI: 0.75,
                fog: 0x0F1C38, fogD: 0.0019,
                sky0: '#030812', sky1: '#050C1C', sky2: '#0B1730', sky3: '#13234A', sky4: '#1D2D55', sky5: '#2A3A62' }
  };
  H.STAGES = STAGES;

  function A() { if (!window.AK || !AK.simplex2) throw new Error('AKH: load noise.js first'); return window.AK; }

  /* Sastrugi, drifts and swell, in metres. u runs along the wind (from 200
   * degrees), v across it: ridges are long along u and short across v. */
  H.height = function (x, z, o) {
    const AKn = A();
    const s = (o && o.seed) || 1;
    const wd = (200 - 180) * Math.PI / 180;
    const u = x * Math.cos(wd) + z * Math.sin(wd), v = -x * Math.sin(wd) + z * Math.cos(wd);
    const dist = Math.hypot(x, z);
    const fade = Math.max(0, 1 - dist / ((o && o.detailFar) || 420));
    let r = 0, amp = 1, fu = 0.11, fv = 0.62, norm = 0;
    for (let k = 0; k < 3; k++) {
      const n = 1 - Math.abs(AKn.simplex2(u * fu + 31.7 * k + s * 0.001, v * fv - 17.3 * k));
      r += n * n * amp; norm += amp; amp *= 0.5; fu *= 2.1; fv *= 2.05;
    }
    const sast = (r / norm - 0.35) * 0.095 * fade;
    const drift = AKn.simplex2(x / 38 + 5.1, z / 52 - 2.3) * 0.22 * Math.max(0.15, 1 - dist / 1600);
    const swell = AKn.simplex2(x / 420 - 9.0, z / 520 + 4.0) * 1.1;
    /* o.mounds: [{x, z, rx, rz, h, rot}] smooth drifts added near the camera, so a
     * foreground drift is part of the same lit surface and never a separate prop */
    let m = 0;
    const md = o && o.mounds;
    if (md) for (const q of md) {
      const c = Math.cos(q.rot || 0), sn = Math.sin(q.rot || 0);
      const dx = x - q.x, dz = z - q.z;
      const a = (dx * c + dz * sn) / q.rx, b = (-dx * sn + dz * c) / q.rz;
      m += q.h * Math.exp(-(a * a + b * b) * 1.6);
    }
    return sast + drift + swell + m;
  };

  H.camera = function (R, o) {
    o = o || {};
    const h = o.height != null ? o.height : 1.6;
    const pitch = (o.pitch || 0) * Math.PI / 180;
    const yaw = (o.yaw || 0) * Math.PI / 180;   // 0 = due south (-z), positive turns west
    R.camera.fov = o.fov || 50;
    R.camera.near = o.near || 0.05;
    R.camera.far = o.far || 6000;
    const ground = H.height(0, 0, o) ;
    R.camera.position.set(o.x || 0, ground + h, o.z || 0);
    const dir = new THREE.Vector3(-Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch));
    R.camera.lookAt(R.camera.position.clone().add(dir));
    R.camera.updateProjectionMatrix();
    R.camera.updateMatrixWorld(true);
    R._akh = Object.assign({}, R._akh || {}, { yaw, pitch, seed: o.seed, mounds: o.mounds, detailFar: o.detailFar });
    return R.camera;
  };

  H.plain = function (R, o) {
    o = o || {};
    const near = o.near || 1, far = o.far || 3200;
    const NZ = o.rows || 640, NX = o.cols || 720;
    const halfFov = Math.atan(Math.tan(R.camera.fov * Math.PI / 360) * (R.w / R.h)) * 1.25;
    const yaw = (R._akh && R._akh.yaw) || 0;
    const cx0 = R.camera.position.x, cz0 = R.camera.position.z;
    const pos = new Float32Array(NX * NZ * 3);
    let p = 0;
    for (let j = 0; j < NZ; j++) {
      const t = j / (NZ - 1);
      const d = near * Math.pow(far / near, t);           // geometric rows
      const half = Math.tan(halfFov) * d + 2;
      for (let i = 0; i < NX; i++) {
        const s = (i / (NX - 1)) * 2 - 1;
        const lx = s * half, lz = -d;                       // camera-local, then yaw
        const x = cx0 + lx * Math.cos(yaw) + lz * Math.sin(yaw);
        const z = cz0 - lx * Math.sin(yaw) + lz * Math.cos(yaw);
        pos[p++] = x; pos[p++] = H.height(x, z, o); pos[p++] = z;
      }
    }
    const idx = new Uint32Array((NX - 1) * (NZ - 1) * 6);
    let q = 0;
    for (let j = 0; j < NZ - 1; j++) for (let i = 0; i < NX - 1; i++) {
      const a = j * NX + i, b = a + 1, c = a + NX, d = c + 1;
      idx[q++] = a; idx[q++] = b; idx[q++] = c; idx[q++] = b; idx[q++] = d; idx[q++] = c;   /* counter-clockwise from above: the normal points up */
    }
    /* wind-streak albedo: long streaks along the wind and patchy crust, as vertex
     * colours, so the snow carries texture where the relief is too fine to shade */
    const col = new Float32Array(NX * NZ * 3);
    const AKn = A();
    const wd = 20 * Math.PI / 180;
    for (let k = 0; k < NX * NZ; k++) {
      const x = pos[k * 3], z = pos[k * 3 + 2];
      const u = x * Math.cos(wd) + z * Math.sin(wd), v = -x * Math.sin(wd) + z * Math.cos(wd);
      const st = AKn.simplex2(u * 0.05, v * 0.9) * 0.6 + AKn.simplex2(u * 0.12, v * 2.3) * 0.4;
      const cr = AKn.simplex2(x * 0.08 + 3.3, z * 0.08 - 1.1);
      const dist = Math.hypot(x - cx0, z - cz0), f = Math.max(0, 1 - dist / 260);
      const m = 1 - (0.10 * (st * 0.5 + 0.5) + 0.07 * Math.max(0, cr)) * f;
      col[k * 3] = m; col[k * 3 + 1] = m; col[k * 3 + 2] = Math.min(1, m * 1.01);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    geo.setIndex(new THREE.BufferAttribute(idx, 1));
    geo.computeVertexNormals();
    const mat = new THREE.MeshStandardMaterial({ color: o.color || 0xE4ECF7, roughness: o.roughness || 0.78, metalness: 0, vertexColors: true });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.receiveShadow = true; mesh.castShadow = true;
    R.scene.add(mesh);
    return mesh;
  };

  H.light = function (R, o) {
    o = o || {};
    const S = STAGES[o.stage || 'twilight'];
    const el = (o.el != null ? o.el : 9) * Math.PI / 180;   // azimuth 180, from the south
    const key = new THREE.DirectionalLight(S.key, o.keyI != null ? o.keyI : S.keyI);
    const cam = R.camera.position;
    /* az 180 is due south, which is -z in this world */
    const az = (o.az != null ? o.az : 205) * Math.PI / 180;   /* clockwise from north; 180 is -z, 270 is -x */
    key.position.set(cam.x + Math.sin(az) * Math.cos(el) * 400, cam.y + Math.sin(el) * 400, cam.z - Math.cos(az) * Math.cos(el) * -400);
    key.target.position.set(cam.x, 0, cam.z - 40);
    R.scene.add(key); R.scene.add(key.target);
    const hemi = new THREE.HemisphereLight(S.sky, S.ground, o.hemiI != null ? o.hemiI : S.hemiI);
    R.scene.add(hemi);
    R.scene.fog = new THREE.FogExp2(S.fog, o.fogD != null ? o.fogD : S.fogD);
    return { key, hemi };
  };

  H.horizonY = function (R, o) {
    const yaw = (R._akh && R._akh.yaw) || 0;
    const d = (o && o.dist) || 3000;
    const c = R.camera.position;
    const x = c.x - Math.sin(yaw) * d, z = c.z - Math.cos(yaw) * d;
    return AKT.projectPoint(R, x, H.height(x, z, R._akh || {}), z).y;
  };

  /* The sky as the scene background, a screen-space gradient whose stops are
   * placed by the solved horizon so the glow sits on the land line. */
  H.sky = function (R, o) {
    o = o || {};
    const S = STAGES[o.stage || 'twilight'];
    const W = 540, Hh = 675, hy = (o.horizonY || 900) / 1350;
    const c = document.createElement('canvas'); c.width = W; c.height = Hh;
    const g = c.getContext('2d');
    const gr = g.createLinearGradient(0, 0, 0, Hh);
    const at = f => Math.max(0, Math.min(1, f));
    gr.addColorStop(0, S.sky0);
    gr.addColorStop(at(hy * 0.42), S.sky1);
    gr.addColorStop(at(hy * 0.74), S.sky2);
    gr.addColorStop(at(hy * 0.92), S.sky3);
    gr.addColorStop(at(hy * 0.985), S.sky4);
    gr.addColorStop(at(hy + 0.004), S.sky5);
    gr.addColorStop(1, S.sky5);
    g.fillStyle = gr; g.fillRect(0, 0, W, Hh);
    if (o.paint) o.paint(g, W, Hh, hy * Hh);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    R.scene.background = tex;
    return c;
  };

  return H;
}
