/* akglobe.js — an orbital Earth for slide heroes (added 2026-11-06 for No.107,
 * slides 01, 05 and 09). ES module, used beside akthree.js:
 *
 *   const THREE = await import('@@ASSETS@@/js/three.module.min.js');
 *   const AKT   = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);
 *   const AKG   = (await import('@@ASSETS@@/js/akglobe.js')).init(THREE, d3, topojson);
 *   const tex   = await AKG.textures('@@ASSETS@@', { snowLat: 57, seed: 7 });
 *   const earth = AKG.earth(R, tex, { sun: AKG.sunDir(-16, -105) });
 *   ... AKT.snapshot(R) ...
 *   const p = AKG.project(R, -150, 61);   // {x, y, visible} in design px
 *
 * What it does, and why each part exists:
 * - textures(): rasterises world-land-110m plus the detailed Natural Earth 10m
 *   Alaska polygon into one 4096 x 2048 plate carree ALBEDO, a ROUGHNESS map
 *   (open ocean smooth enough to carry a low-sun glint, land matte) and a BUMP
 *   map. Over Alaska the bump comes from the committed state DEM (ak-state-dem,
 *   0.08 x 0.04 degree cells) so the Alaska Range catches a raking sun; elsewhere
 *   land gets a soft fbm relief and the coast a bevel from a blurred land mask.
 *   November albedo: land north of a ragged snow line is snow, south of it dark
 *   spruce and tundra, so the latitude reads at a glance.
 * - earth(): the sphere (MeshStandardMaterial with those maps, PBR) and an
 *   atmosphere shell (back-face fresnel, additive, green-first rim) whose colour
 *   is the caller's.
 * - project(): lon/lat to design px through the scene camera, with a horizon
 *   test, so a slide can draw crisp 2D work (a gold coastline, leaders, labels)
 *   after the GL draw-down and the grade, exactly over the rendered surface.
 * - coastRings(): the Alaska polygon's rings as [lon, lat] arrays.
 *
 * Mapping: lon/lat -> (cos(lat)cos(lon), sin(lat), -cos(lat)sin(lon)), which is
 * three's SphereGeometry UV convention with u = (lon + 180) / 360, so the plate
 * carree canvas maps onto the sphere with no seam offset. Deterministic: every
 * noise call is seeded.
 */
export function init(THREE, d3, topojson) {
  const G = {};
  const RAD = Math.PI / 180;

  G.xyz = function (lon, lat, r) {
    r = r || 1;
    const la = lat * RAD, lo = lon * RAD;
    return new THREE.Vector3(r * Math.cos(la) * Math.cos(lo), r * Math.sin(la),
                             -r * Math.cos(la) * Math.sin(lo));
  };

  // Direction TO the sun from the subsolar point (declination, subsolar lon).
  G.sunDir = function (decl, subLon) { return G.xyz(subLon, decl, 1).normalize(); };

  // Seeded value noise + fbm, enough for albedo mottling and bump.
  function hash(i, j, s) {
    // 32-bit integer products (Math.imul): a float product past 2^53 drops the low bits,
    // the hash stops mixing and the snow printed as long brushed streaks
    let h = (Math.imul(i, 374761393) + Math.imul(j, 668265263) + Math.imul(s, 2147483647)) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
  }
  function vnoise(x, y, s) {
    const i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j;
    const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy);
    const a = hash(i, j, s), b = hash(i + 1, j, s), c = hash(i, j + 1, s), d = hash(i + 1, j + 1, s);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function fbm(x, y, s, oct) {
    let t = 0, amp = 0.5, f = 1;
    for (let k = 0; k < (oct || 5); k++) { t += amp * vnoise(x * f, y * f, s + k * 17); f *= 2.03; amp *= 0.5; }
    return t;
  }
  G.fbm = fbm;

  function boxBlur(src, w, h, r) {
    const tmp = new Float32Array(w * h), out = new Float32Array(w * h);
    for (let y = 0; y < h; y++) {
      let acc = 0; const row = y * w;
      for (let x = -r; x <= r; x++) acc += src[row + Math.min(w - 1, Math.max(0, x))];
      for (let x = 0; x < w; x++) {
        tmp[row + x] = acc / (2 * r + 1);
        acc += src[row + Math.min(w - 1, x + r + 1)] - src[row + Math.max(0, x - r)];
      }
    }
    for (let x = 0; x < w; x++) {
      let acc = 0;
      for (let y = -r; y <= r; y++) acc += tmp[Math.min(h - 1, Math.max(0, y)) * w + x];
      for (let y = 0; y < h; y++) {
        out[y * w + x] = acc / (2 * r + 1);
        acc += tmp[Math.min(h - 1, y + r + 1) * w + x] - tmp[Math.max(0, y - r) * w + x];
      }
    }
    return out;
  }

  G.coastRings = function (akFeature) {
    const rings = [];
    const geom = akFeature.geometry;
    const polys = geom.type === 'MultiPolygon' ? geom.coordinates : [geom.coordinates];
    polys.forEach(p => p.forEach(r => rings.push(r)));
    return rings;
  };

  /* textures(assetsBase, opts) -> {albedo, rough, bump, akFeature, mask, W, H}
   * opts: snowLat (deg, default 57), seed, ocean [deep, shelf] hex, land hexes. */
  G.textures = async function (base, opts) {
    opts = opts || {};
    const reg = opts.region || { west: -180, east: 180, south: -90, north: 90 };
    const W = opts.W || 4096;
    const H = opts.H || Math.round(W * (reg.north - reg.south) / (reg.east - reg.west));
    const seed = opts.seed || 7;
    const cLon = (reg.west + reg.east) / 2;
    const [world, ak, demMeta, demBuf] = await Promise.all([
      fetch(base + '/geo/world-land-110m.json').then(r => r.json()),
      fetch(base + '/geo/alaska-state.geo.json').then(r => r.json()),
      fetch(base + '/geo/ak-state-dem.json').then(r => r.json()),
      fetch(base + '/geo/ak-state-dem.bin').then(r => r.arrayBuffer()),
    ]);
    const land0 = topojson.feature(world, world.objects.land);
    // Split into polygons and rewind any whose spherical area exceeds a
    // hemisphere: under a rotated projection d3 reads a mis-wound ring as the
    // whole globe minus the island, which paints the oceans as land.
    const polysIn = [];
    (land0.features || [land0]).forEach(f => {
      const g = f.geometry; const ps = g.type === 'MultiPolygon' ? g.coordinates : [g.coordinates];
      ps.forEach(p => polysIn.push(p));
    });
    const polysOut = polysIn.map(p => {
      const f = { type: 'Feature', geometry: { type: 'Polygon', coordinates: p } };
      return d3.geoArea(f) > 2 * Math.PI ? p.map(r => r.slice().reverse()) : p;
    });
    const land = { type: 'Feature', geometry: { type: 'MultiPolygon', coordinates: polysOut } };
    const akFeature = ak.features[0];
    const pscale = W / ((reg.east - reg.west) * RAD);
    const proj = d3.geoEquirectangular().rotate([-cLon, 0]).scale(pscale)
      .translate([W / 2, pscale * reg.north * RAD]).precision(0.1);
    // land mask
    const mc = document.createElement('canvas'); mc.width = W; mc.height = H;
    const mx = mc.getContext('2d');
    mx.fillStyle = '#000'; mx.fillRect(0, 0, W, H);
    const path = d3.geoPath(proj, mx);
    mx.fillStyle = '#fff';
    mx.beginPath(); path(land); mx.fill();
    // Alaska from the detailed polygon: erase the coarse 110m shape west of
    // 141W (stopping at 168.5W so Chukotka survives), then fill the fine 10m
    // polygon, which also carries the panhandle and the Aleutians.
    const c0 = proj([-168.5, 72.5]), c1 = proj([-141.0, 51.0]);
    mx.fillStyle = '#000'; mx.fillRect(c0[0], c0[1], c1[0] - c0[0], c1[1] - c0[1]);
    mx.fillStyle = '#fff'; mx.beginPath(); path(akFeature); mx.fill();
    const mdat = mx.getImageData(0, 0, W, H).data;
    // Alaska alone: its 10m coast stays sharp; the coarse 110m land around it is
    // feathered wide so its straight segments never read as facets
    const ac = document.createElement('canvas'); ac.width = W; ac.height = H;
    const acx = ac.getContext('2d'); acx.fillStyle = '#fff'; acx.beginPath(); d3.geoPath(proj, acx)(akFeature); acx.fill();
    const adat = acx.getImageData(0, 0, W, H).data;
    const mask = new Float32Array(W * H);
    for (let i = 0; i < W * H; i++) mask[i] = mdat[i * 4] / 255;
    const akM = new Float32Array(W * H);
    for (let i = 0; i < W * H; i++) akM[i] = adat[i * 4] / 255;
    const akNear = boxBlur(akM, W, H, 3);
    const near = boxBlur(mask, W, H, 6);     // coastal bevel
    const far = boxBlur(near, W, H, 18);     // shelf / distance to land

    // DEM sampler (bilinear), returns metres or null outside
    const dem = new Int16Array(demBuf);
    function demAt(lon, lat) {
      const fx = (lon - demMeta.west) / demMeta.dlon, fy = (demMeta.north - lat) / demMeta.dlat;
      if (fx < 0 || fy < 0 || fx > demMeta.cols - 1.001 || fy > demMeta.rows - 1.001) return null;
      const i = Math.floor(fx), j = Math.floor(fy), u = fx - i, v = fy - j, c = demMeta.cols;
      const a = dem[j * c + i], b = dem[j * c + i + 1], d = dem[(j + 1) * c + i], e = dem[(j + 1) * c + i + 1];
      return a * (1 - u) * (1 - v) + b * u * (1 - v) + d * (1 - u) * v + e * u * v;
    }

    const snowLat = opts.snowLat != null ? opts.snowLat : 57;
    const ocDeep = new THREE.Color(opts.oceanDeep || 0x071a2c), ocShelf = new THREE.Color(opts.oceanShelf || 0x10324a);
    const snow = new THREE.Color(opts.snow || 0xd8e2ea), snowShade = new THREE.Color(opts.snowShade || 0x9fb2c2);
    const spruce = new THREE.Color(opts.spruce || 0x1e2a24), tundra = new THREE.Color(opts.tundra || 0x4a4a3c);
    const albedo = document.createElement('canvas'); albedo.width = W; albedo.height = H;
    const rough = document.createElement('canvas'); rough.width = W; rough.height = H;
    const bump = document.createElement('canvas'); bump.width = W; bump.height = H;
    const ai = albedo.getContext('2d').createImageData(W, H);
    const ri = rough.getContext('2d').createImageData(W, H);
    const bi = bump.getContext('2d').createImageData(W, H);
    const tmp = new THREE.Color(), oc = new THREE.Color();
    const s8 = (v) => 255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055);
    const maskS = boxBlur(mask, W, H, 1);
    const maskWide = boxBlur(boxBlur(mask, W, H, 4), W, H, 4);
    const bumpF = new Float32Array(W * H);
    const otherLand = opts.otherLand != null ? opts.otherLand : 1;
    const clRef = Math.cos(((reg.north + Math.max(reg.south, 40)) / 2) * RAD);
    const akWide = otherLand < 1 ? boxBlur(boxBlur(akM, W, H, 8), W, H, 8) : null;
    for (let y = 0; y < H; y++) {
      const lat = reg.north - (y + 0.5) * (reg.north - reg.south) / H;
      const cl = Math.cos(lat * RAD);
      for (let x = 0; x < W; x++) {
        const lon = reg.west + (x + 0.5) * (reg.east - reg.west) / W;
        // noise space in degrees of arc about the patch centre, at one reference latitude:
        // lon * cos(lat) far from the prime meridian shears with latitude (at 190W it slid
        // five cells per degree north) and printed the snow as long diagonal streaks
        const nx = (lon - cLon) * clRef * 1.6, ny = lat * 1.6;
        const k = y * W + x;
        const isAk = akNear[k] > 0.02;
        const m = isAk ? maskS[k] : maskWide[k];
        const n = fbm(nx * 1.0, ny * 1.0, seed, 3);
        const landness = isAk ? THREE.MathUtils.smoothstep(m, 0.3, 0.7) : THREE.MathUtils.smoothstep(m, 0.25, 0.75);
        let h = 0, isLand = landness > 0.5;
        // land colour
        let e = (lon >= -170 && lon <= -129.12 && lat >= 54.04 && lat <= 72) ? demAt(lon, lat) : null;
        // DEM inside its own box, feathered over 1.5 degrees into a soft fbm relief
        // outside it, so the box's edge never prints as a seam
        // land outside the DEM gets a soft, low relief so it reads as terrain and not as a paper cut-out
        const fr = opts.otherRelief != null ? opts.otherRelief * fbm(nx * 2.2, ny * 2.2, seed + 3, 3) : 0.0;
        let wDem = 0;
        if (e != null) {
          const dEdge = Math.min(lon + 170, -129.12 - lon, lat - 54.04, 72 - lat);
          wDem = THREE.MathUtils.smoothstep(dEdge, 0, 4.0);
        }
        h = landness > 0.02 ? (wDem * Math.max(0, e || 0) / 5563 + (1 - wDem) * fr) : 0;
        const sl = snowLat + (n - 0.5) * 6 - h * 14;
        const sn = THREE.MathUtils.smoothstep(lat, sl - 1.5, sl + 1.5);
        // noise frequencies stay under the texture's Nyquist (about 39 px a degree at the
        // default patch): finer octaves alias into a brushed, striped lay on the snow
        tmp.copy(spruce).lerp(tundra, fbm(nx * 0.9, ny * 0.9, seed + 9, 3));
        const sc = snowShade.clone().lerp(snow, 0.6 + 0.4 * fbm(nx * 1.1, ny * 1.1, seed + 5, 3));
        tmp.lerp(sc, sn);
        if (lat > 74) tmp.lerp(snow, 0.85);
        if (lat > 83) tmp.lerp(snowShade, THREE.MathUtils.smoothstep(lat, 83, 86));
        // land that is not Alaska steps down (opts.otherLand, 0..1 of Alaska's albedo),
        // feathered off Alaska's own coast so the 141W line never prints as a cut
        if (otherLand < 1) tmp.multiplyScalar(otherLand + (1 - otherLand) * Math.min(1, akWide[k] * 1.6));
        // ocean colour: shelf lighter near land; sea ice in the far north (November)
        const shelf = Math.min(1, far[k] * 3.2);
        oc.copy(ocDeep).lerp(ocShelf, shelf * 0.8);
        oc.lerp(snowShade, THREE.MathUtils.smoothstep(lat, 71, 76) * 0.7);
        tmp.lerp(oc, 1 - landness);
        const p = k * 4;
        // THREE.Color holds LINEAR values; the albedo canvas is an sRGB texture,
        // so encode before writing (writing linear bytes darkened every hue twice)
        ai.data[p] = s8(tmp.r); ai.data[p + 1] = s8(tmp.g); ai.data[p + 2] = s8(tmp.b); ai.data[p + 3] = 255;
        const rv = Math.round(235 * landness + (lat > 72 ? 180 : (opts.oceanRough != null ? opts.oceanRough : 80)) * (1 - landness));
        ri.data[p] = ri.data[p + 1] = ri.data[p + 2] = rv; ri.data[p + 3] = 255;
        bumpF[k] = (isAk ? 0.12 * near[k] : 0.0) + 0.88 * Math.pow(h, 0.7);
      }
    }
    // soften the bump by two cells so DEM cells and mask steps never print as blocks
    const bumpS = boxBlur(bumpF, W, H, opts.bumpBlur != null ? opts.bumpBlur : 2);
    for (let k = 0; k < W * H; k++) {
      const bv = Math.max(0, Math.min(255, 255 * bumpS[k]));
      bi.data[k * 4] = bi.data[k * 4 + 1] = bi.data[k * 4 + 2] = bv; bi.data[k * 4 + 3] = 255;
    }
    albedo.getContext('2d').putImageData(ai, 0, 0);
    rough.getContext('2d').putImageData(ri, 0, 0);
    bump.getContext('2d').putImageData(bi, 0, 0);
    const mk = (c, srgb) => { const t = new THREE.CanvasTexture(c); if (srgb) t.colorSpace = THREE.SRGBColorSpace;
      t.anisotropy = 8; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter; return t; };
    return { albedo: mk(albedo, true), rough: mk(rough, false), bump: mk(bump, false),
             akFeature, land, mask, W, H, demAt, region: reg };
  };

  /* earth(R, tex, opts) -> {mesh, shell, sun}
   * opts: sun (Vector3 toward sun), sunColor, sunIntensity, fill, bumpScale,
   * atmo (hex), atmoStrength, segments. */
  G.earth = function (R, tex, opts) {
    opts = opts || {};
    const seg = opts.segments || 256;
    const mat = new THREE.MeshStandardMaterial({ map: tex.albedo, roughnessMap: tex.rough, roughness: 1,
      metalness: 0, bumpMap: tex.bump, bumpScale: opts.bumpScale != null ? opts.bumpScale : 6 });
    const rg = tex.region || { west: -180, east: 180, south: -90, north: 90 };
    const geo = new THREE.SphereGeometry(1, seg, Math.max(16, Math.round(seg * (rg.north - rg.south) / (rg.east - rg.west))),
      (rg.west + 180) * RAD, (rg.east - rg.west) * RAD, (90 - rg.north) * RAD, (rg.north - rg.south) * RAD);
    const mesh = new THREE.Mesh(geo, mat);
    // the globe takes no shadow map: at a grazing sun the depth compare printed diagonal acne
    // stripes across flat snow, and every cast on it is drawn in 2D from projected paths
    mesh.castShadow = false; mesh.receiveShadow = !!opts.receiveShadow;
    R.scene.add(mesh);
    const sun = new THREE.DirectionalLight(opts.sunColor || 0xffe2c0, opts.sunIntensity || 3.2);
    const sd = (opts.sun || G.sunDir(-16, -105)).clone().normalize();
    sun.position.copy(sd.clone().multiplyScalar(6));
    sun.target.position.set(0, 0, 0);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    const sc = sun.shadow.camera; sc.left = -1.6; sc.right = 1.6; sc.top = 1.6; sc.bottom = -1.6; sc.near = 2; sc.far = 10;
    sun.shadow.bias = -0.0006; sun.shadow.normalBias = 0.01;
    R.scene.add(sun); R.scene.add(sun.target);
    const fill = new THREE.HemisphereLight(opts.fillSky || 0x2a4a6a, opts.fillGround || 0x05080f, opts.fill != null ? opts.fill : 0.18);
    R.scene.add(fill);
    // atmosphere: back-face fresnel shell, additive, brighter on the lit limb
    const atmoCol = new THREE.Color(opts.atmo || 0x3ce6b4), atmoCol2 = new THREE.Color(opts.atmo2 || 0x5ac8f0);
    const shellMat = new THREE.ShaderMaterial({
      uniforms: { c1: { value: atmoCol }, c2: { value: atmoCol2 }, sunDir: { value: sd },
                  strength: { value: opts.atmoStrength != null ? opts.atmoStrength : 1.0 },
                  night: { value: opts.atmoNight != null ? opts.atmoNight : 0.25 } },
      vertexShader: `varying vec3 vN; varying vec3 vW; void main(){ vN = normalize(mat3(modelMatrix)*normal);
        vec4 w = modelMatrix*vec4(position,1.0); vW = w.xyz; gl_Position = projectionMatrix*viewMatrix*w; }`,
      fragmentShader: `uniform vec3 c1; uniform vec3 c2; uniform vec3 sunDir; uniform float strength; uniform float night;
        varying vec3 vN; varying vec3 vW;
        void main(){ vec3 V = normalize(cameraPosition - vW); float f = 1.0 - abs(dot(V, vN));
          float rim = pow(f, 3.2); float lit = clamp(dot(normalize(vW), sunDir)*0.8+0.35, 0.0, 1.0);
          vec3 col = mix(c1, c2, smoothstep(0.55, 1.0, f)); float a = rim * strength * mix(night, 1.0, lit);
          gl_FragColor = vec4(col * a, a); }`,
      side: THREE.BackSide, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false });
    const shell = new THREE.Mesh(new THREE.SphereGeometry(opts.shellR || 1.035, 128, 64), shellMat);
    R.scene.add(shell);
    // inner haze on the lit surface near the limb (front faces, very light)
    const hazeMat = shellMat.clone(); hazeMat.side = THREE.FrontSide;
    hazeMat.uniforms = THREE.UniformsUtils.clone(shellMat.uniforms);
    hazeMat.uniforms.strength.value = (opts.hazeStrength != null ? opts.hazeStrength : 0.45);
    const haze = new THREE.Mesh(new THREE.SphereGeometry(1.004, 128, 64), hazeMat);
    R.scene.add(haze);
    return { mesh, shell, haze, sun, sunDir: sd };
  };

  /* project(R, lon, lat, alt) -> {x, y, visible, facing} in design px.
   * visible: on the camera side of the limb (the surface normal faces the eye). */
  G.project = function (R, lon, lat, alt) {
    const p = G.xyz(lon, lat, 1 + (alt || 0));
    const toEye = R.camera.position.clone().sub(p);
    const facing = p.clone().normalize().dot(toEye.normalize());
    const v = p.clone().project(R.camera);
    return { x: (v.x + 1) / 2 * R.w, y: (1 - v.y) / 2 * R.h, visible: facing > 0, facing };
  };

  /* Screen circle of the globe's limb (approximate, for star masking). */
  G.limbTest = function (R) {
    const cam = R.camera.position;
    return function (x, y) {
      const ndc = new THREE.Vector3(x / R.w * 2 - 1, 1 - y / R.h * 2, 0.5).unproject(R.camera);
      const dir = ndc.sub(cam).normalize();
      const b = cam.dot(dir), c = cam.dot(cam) - 1.05 * 1.05;
      return b * b - c > 0 && b < 0;   // ray hits the shell
    };
  };

  return G;
}
