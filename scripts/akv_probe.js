#!/usr/bin/env node
/* akv_probe.js -- settle an akvalley camera station in one call, before any render.
 *
 * WHY THIS EXISTS (upgrade 2026-09-24, run No.67). The first akvalley deck
 * solved its camera stations by guess-and-render until a throwaway node
 * harness was written in scratch, and two whole pixel-critic rounds were still
 * lost to stations that a number would have refused: slide 04 was re-solved
 * 70 km north, OFF the DEM, where V.camera silently assumed 100 m of ground and
 * the haze took the whole frame; slide 08 was flown over flats whose relief
 * lay outside the DEM crop, and never cleared the critics. Both are facts about
 * the station, measurable before a pixel is drawn. This is that harness,
 * committed and tested.
 *
 * It loads assets/js/akvalley.js with a file-backed fetch (no browser, no new
 * dependency) and prints JSON:
 *   camera        lon, lat, ground and altitude in metres, heading, pitch, cy
 *   onDem         whether the DEM exists under the camera
 *   cropDepthKm   V.cropDepth: how far ahead the whole frame width is on the DEM
 *   bottomRowKm   forward ground distance under the frame's bottom row
 *                 (left, centre, right); null means that ray found no ground
 *   nearReliefM   p10-to-p90 height range, true metres, of the ground the
 *                 bottom edge opens onto (bottom-row distance out to twice
 *                 that, frame-wide). Flat near ground read as ruled paper or
 *                 a void to every critic round on the first akvalley deck;
 *                 this is the number to compare stations by
 *   nearTextureM  the same ground's LOCAL relief: p10-to-p90 of each point
 *                 minus the mean of a 1.6 km box round it, so a regional
 *                 slope across flats does not pass for ridges and sloughs
 *   offDemShare   share of lower-third sample rays that leave the DEM before
 *                 meeting ground (the crop edge is low in the frame)
 *   solve         for "aim": the solved pitch and how far the far-ground row
 *                 missed yFar (V.aim returns its best try silently)
 *   targets       each named lon/lat: screen x, y, depth, inFrame, visible
 *   problems      things that are wrong with this station, in words
 * It REPORTS; it decides nothing and is not a gate. Exit 0 always, except
 * --self-test, which exits 1 on a failed assertion.
 *
 * USAGE
 *   node scripts/akv_probe.js '{"aim": {"target": [-149.0821, 64.5486],
 *        "heading": 182, "distKm": 48, "agl": 9000, "fov": 58,
 *        "yTarget": 860, "farKm": 84, "yFar": 560, "VE": 3},
 *        "targets": {"ENN": [-149.0821, 64.5486]}}'
 *   node scripts/akv_probe.js '{"camera": {"lon": -149.1, "lat": 64.1,
 *        "agl": 3200, "heading": 2, "pitch": -9, "fov": 70, "cy": 884}}'
 *   node scripts/akv_probe.js --expr 'return V.squareRing(AP[0], AP[1], 31.6)'
 *        (free form, V and AP in scope, the scratch harness's old job)
 *   node scripts/akv_probe.js --self-test
 * "W"/"H" default to 1080 x 1350. "aim" and "camera" take exactly the options
 * V.aim and V.camera take, so a probed station pastes straight into a slide.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const ASSETS = path.join(ROOT, "assets");
const AP = [-149.0821, 64.5486]; // ENN, the FAA point the first deck used

async function loadV() {
  global.window = global;
  global.fetch = async (p) => {
    const f = String(p).replace("@@ASSETS@@", ASSETS);
    const b = fs.readFileSync(f);
    return {
      json: async () => JSON.parse(b.toString()),
      arrayBuffer: async () => b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength),
    };
  };
  // stations are built with silent: true, so akvalley's own off-DEM
  // console.error stays quiet here; the probe reports onDem itself
  require(path.join(ASSETS, "js", "akvalley.js"));
  return global.AKV.load("@@ASSETS@@");
}

function hW(V, x, z) { const ll = V.lonlatOf(x, z); return V.heightAt(ll[0], ll[1]); }

/* march the ray through screen pixel (px, py) until it meets the ground.
 * Returns {km, h} (forward horizontal distance, true metres) or
 * {km: null, why: "sky" | "offDem"}. */
function rayGround(V, cam, px, py) {
  const a = (px - cam.cx) / cam.f, b = -(py - cam.cy) / cam.f;
  let d = [cam.F[0] + a * cam.R[0] + b * cam.U[0], cam.F[1] + a * cam.R[1] + b * cam.U[1],
           cam.F[2] + a * cam.R[2] + b * cam.U[2]];
  const n = Math.hypot(d[0], d[1], d[2]); d = d.map((v) => v / n);
  let t = 0, prev = 0;
  while (t < 400) {
    const step = Math.max(0.02, t * 0.004);
    t += step;
    const x = cam.pos[0] + d[0] * t, y = cam.pos[1] + d[1] * t, z = cam.pos[2] + d[2] * t;
    const h = hW(V, x, z);
    if (h === null) return { km: null, why: "offDem" };
    if (y <= h / 1000 * cam.VE) {
      // one bisection pass back into the last step, enough for a report
      let lo = prev, hi = t;
      for (let i = 0; i < 12; i++) {
        const m = (lo + hi) / 2, xm = cam.pos[0] + d[0] * m, ym = cam.pos[1] + d[1] * m, zm = cam.pos[2] + d[2] * m;
        const hm = hW(V, xm, zm);
        if (hm !== null && ym <= hm / 1000 * cam.VE) hi = m; else lo = m;
      }
      const xh = cam.pos[0] + d[0] * hi, zh = cam.pos[2] + d[2] * hi;
      const fwd = (xh - cam.pos[0]) * cam.fwdH[0] + (zh - cam.pos[2]) * cam.fwdH[1];
      return { km: fwd, h: hW(V, xh, zh) };
    }
    if (d[1] >= 0 && y > 12 * cam.VE) return { km: null, why: "sky" };
    prev = t;
  }
  return { km: null, why: "sky" };
}

function pct(a, p) {
  if (!a.length) return null;
  const s = a.slice().sort((x, y) => x - y);
  return s[Math.min(s.length - 1, Math.max(0, Math.round(p * (s.length - 1))))];
}

function probe(V, spec) {
  let W = spec.W || 1080, H = spec.H || 1350;
  let cam, solve = null;
  if (spec.aim) {
    cam = V.aim(Object.assign({ W, H }, spec.aim, { silent: true }));
    solve = { errPx: cam.solveErr, pitch: cam.pitch };
  } else if (spec.camera) {
    cam = V.camera(Object.assign({ W, H }, spec.camera, { silent: true }));
    cam.lon = spec.camera.lon; cam.lat = spec.camera.lat;
  } else {
    throw new Error("spec needs an 'aim' or a 'camera' object");
  }
  // measure the frame the camera actually has: W and H may be set inside
  // `aim` or `camera`, where the renderer's own options live
  W = cam.W; H = cam.H;
  const onDem = V.heightAt(cam.lon, cam.lat) !== null;
  const problems = [];
  if (!onDem) {
    problems.push(`camera at ${cam.lon.toFixed(3)}, ${cam.lat.toFixed(3)} is OFF the DEM ` +
      `(${V.meta.west.toFixed(2)} to ${V.meta.east.toFixed(2)} E, ${V.meta.south.toFixed(2)} to ` +
      `${V.meta.north.toFixed(2)} N): V.camera assumed 100 m of ground, so agl is fiction and ` +
      "cropDepth collapses; move the station onto the DEM");
  }
  if (solve) {
    if (solve.errPx > 12) {
      problems.push(`aim could not put the far ground on yFar: it misses by ${solve.errPx.toFixed(0)} px ` +
        "(V.aim returns its best try without saying so); the target row holds, the far row does not");
    }
    if (cam.targetOffDem) {
      problems.push("aim target is OFF the DEM, so the target row was solved against invented " +
        "ground (V.project's 100 m stand-in); pick a target inside the crop");
    }
    if (cam.farOffDem) {
      problems.push(`aim farKm lands OFF the DEM, so the far row was solved against invented ` +
        "ground (V.aim's 120 m stand-in); shorten farKm to inside cropDepthKm");
    }
    if (cam.pitch <= -69.75 || cam.pitch >= -2.25) {
      problems.push(`aim pitch ${cam.pitch} is at the edge of its search (-70 to -2), so the solve is ` +
        "clamped, not found; change distKm, agl or the rows");
    }
    if (Math.abs(cam.cy - H / 2) > H) {
      problems.push(`aim lens shift is ${Math.round(cam.cy - H / 2)} px (cy ${Math.round(cam.cy)}): ` +
        "a principal point that far off the frame is a camera no lens has; move the camera instead");
    }
  }
  const crop = V.cropDepth(cam, 1);
  if (crop === null) problems.push("no profile past 1 km lies wholly on the DEM (cropDepth has no safe depth)");
  const bottom = [0.02, 0.5, 0.98].map((fx) => rayGround(V, cam, W * fx, H - 1));
  bottom.forEach((r, i) => {
    if (r.km === null) {
      problems.push(`the bottom row's ${["left", "centre", "right"][i]} ray finds no ground (${r.why})`);
    }
  });
  // crop exposure in the lower third, on a 13 x 7 ray grid: a ray there that
  // leaves the DEM before meeting ground puts the crop edge low in the frame,
  // where no haze can hide it (above that, the haze exists for exactly this)
  let lowerRays = 0, off = 0;
  for (let j = 0; j < 7; j++) {
    const py = H * (2 / 3 + j / 18) - (j === 6 ? 1 : 0);
    for (let i = 0; i < 13; i++) {
      const r = rayGround(V, cam, W * (0.02 + 0.96 * i / 12), py);
      lowerRays++;
      if (r.km === null && r.why === "offDem") off++;
    }
  }
  if (off > 0) {
    problems.push(`${off} of ${lowerRays} lower-third rays leave the DEM before meeting ground: ` +
      "the crop edge sits low in the frame, where the haze can't hide it");
  }
  // NEAR-FIELD RELIEF: the ground the frame's bottom edge opens onto, from
  // the bottom row's distance d0 out to 2 x d0, across the frame's width at
  // each depth, sampled on the DEM itself. Measured on the ground rather than
  // along screen rows, because a level camera's lower third can reach from
  // 15 km to 50 km and would mix the far hills into "near".
  const hs = [], tx = [];
  const d0 = bottom[1].km;
  const hw = (W / 2) / cam.f;
  if (d0 !== null && d0 > 0) {
    for (let j = 0; j <= 12; j++) {
      const d = d0 * (1 + j / 12);
      const cxw = cam.pos[0] + cam.fwdH[0] * d, czw = cam.pos[2] + cam.fwdH[1] * d;
      for (let i = 0; i <= 24; i++) {
        // camera-space depth sets the width seen, as terrain() sizes it
        const span = V.profileDepth(cam, d);
        const s = -span * hw + 2 * span * hw * i / 24;
        const px = cxw + cam.rightH[0] * s, pz = czw + cam.rightH[1] * s;
        const h = hW(V, px, pz);
        if (h === null) continue;
        hs.push(h);
        // local texture: this point against the mean of a 1.6 km box round
        // it (the scale the terrain's own relief option lights), so a broad
        // regional slope is not mistaken for ground with something on it
        let sum = 0, n = 0;
        for (let u = -2; u <= 2; u++) for (let v = -2; v <= 2; v++) {
          const q = hW(V, px + u * 0.4, pz + v * 0.4);
          if (q !== null) { sum += q; n++; }
        }
        if (n > 12) tx.push(h - sum / n);
      }
    }
  }
  const relief = hs.length > 20 ? pct(hs, 0.9) - pct(hs, 0.1) : null;
  const texture = tx.length > 20 ? pct(tx, 0.9) - pct(tx, 0.1) : null;
  const nearKm = d0 !== null && d0 > 0 ? [d0, 2 * d0] : [];
  let horizonRow = null;
  const hp = rayCropRow(V, cam, crop);
  if (hp) horizonRow = hp;
  const targets = {};
  Object.entries(spec.targets || {}).forEach(([name, ll]) => {
    const p = V.project(cam, ll[0], ll[1], 0);
    if (!p) { targets[name] = { behind: true }; problems.push(`target ${name} is behind the camera`); return; }
    const w = V.worldOf(ll[0], ll[1]), h = V.heightAt(ll[0], ll[1]);
    const inFrame = p[0] >= 0 && p[0] <= W && p[1] >= 0 && p[1] <= H;
    const visible = h === null ? false : V.visible(cam, w[0], (h + 8) / 1000 * cam.VE, w[1]);
    targets[name] = { x: p[0], y: p[1], depthKm: V.depthOf(cam, ll[0], ll[1]), inFrame, visible,
                      onDem: h !== null };
    if (!inFrame) problems.push(`target ${name} projects out of frame at ${Math.round(p[0])}, ${Math.round(p[1])}`);
    else if (!visible) problems.push(`target ${name} is in frame but terrain hides it from the camera`);
  });
  return {
    camera: { lon: cam.lon, lat: cam.lat, groundM: onDem ? V.heightAt(cam.lon, cam.lat) : null,
              altM: cam.altM, heading: cam.heading, pitch: cam.pitch, fov: cam.fov, cy: cam.cy, VE: cam.VE },
    solve, onDem, cropDepthKm: crop,
    bottomRowKm: { left: bottom[0].km, centre: bottom[1].km, right: bottom[2].km },
    nearRangeKm: nearKm.length ? nearKm : null,
    nearReliefM: relief, nearTextureM: texture, offDemShare: lowerRays ? off / lowerRays : null,
    horizonRow, targets, problems,
  };
}

/* screen row of the ground straight ahead at the crop depth: where the haze
 * has to have finished by, the row the "mesa" would sit on */
function rayCropRow(V, cam, crop) {
  // no crop-safe depth means no row: null, never the ground under the camera
  if (crop === null || crop === undefined) return null;
  const x = cam.pos[0] + cam.fwdH[0] * crop, z = cam.pos[2] + cam.fwdH[1] * crop;
  const h = hW(V, x, z);
  if (h === null) return null;
  const p = V.projectWorld(cam, x, h / 1000 * cam.VE, z);
  return p ? p[1] : null;
}

function round(v) {
  // Metrics to a tenth; geographic coordinates to 1e-5 degrees (about a
  // metre), because a tenth of a degree at Nenana is kilometres and a station
  // copied from the report must land where it was measured.
  const GEO = /^(lon|lat|lon0|lat0|west|east|south|north)$/i;
  return JSON.parse(JSON.stringify(v, (k, x) => {
    if (typeof x !== "number") return x;
    if (GEO.test(k)) return Math.round(x * 1e5) / 1e5;
    return Math.round(x * 10) / 10;
  }));
}

async function selfTest() {
  const V = await loadV();
  const fails = [];
  const ok = (c, m) => { if (!c) fails.push(m); };
  const ENN = { ENN: AP };
  // RECONSTRUCTION 1, run No.67 slide 04 round 1: re-solved 70 km north of
  // the airport, past the DEM's north edge. Must be reported OFF the DEM.
  const r1 = probe(V, { aim: { target: AP, heading: 182, distKm: 70, agl: 9000, fov: 50,
                              yTarget: 900, farKm: 84, yFar: 560, VE: 3 }, targets: ENN });
  ok(!r1.onDem, "slide 04 round 1 station should be off the DEM");
  ok(r1.problems.some((p) => p.includes("OFF the DEM")), "off-DEM station should name the problem");
  // the station 04 shipped with, 48 km: on the DEM, airport in frame and seen
  const r2 = probe(V, { aim: { target: AP, heading: 182, distKm: 48, agl: 9000, fov: 58,
                              yTarget: 860, farKm: 84, yFar: 560, VE: 3 }, targets: ENN });
  ok(r2.onDem, "slide 04 shipped station should be on the DEM");
  ok(r2.targets.ENN.inFrame && r2.targets.ENN.visible, "ENN should be in frame and visible from 04's station");
  ok(Math.abs(r2.targets.ENN.y - 860) < 3, `aim should land ENN on row 860, got ${r2.targets.ENN.y}`);
  ok(!r2.problems.some((p) => p.includes("OFF the DEM")), "shipped 04 must not be called off-DEM");
  // RECONSTRUCTION 2, run No.67 slide 08: the reverse shot over the flats.
  // Its near field must measure as flatter than the cover's (slide 01), whose
  // station was chosen to put the ridge under the camera and which the
  // critics passed at 8.4.
  const s08 = probe(V, { camera: { lon: AP[0] - 0.02, lat: AP[1] - 50 / 110.57, agl: 3200, heading: 2,
                                   pitch: -9, fov: 70, cy: 884, VE: 3 } });
  const s01 = probe(V, { camera: { lon: AP[0] + 0.6, lat: AP[1] + 0.25, agl: 3600, heading: 222,
                                   pitch: -19, fov: 54, cy: 880, VE: 3 } });
  ok(s08.onDem && s01.onDem, "01 and 08 stations are on the DEM");
  ok(s08.nearTextureM !== null && s01.nearTextureM !== null, "near texture should be measured");
  ok(s08.nearTextureM < 5, `08's near ground is flats and should measure under 5 m of texture, got ${s08.nearTextureM}`);
  ok(s01.nearTextureM > 5 * s08.nearTextureM,
     `01's near texture (${s01.nearTextureM}) should be far above 08's (${s08.nearTextureM})`);
  // RECONSTRUCTION 3, run No.67 slide 09: V.aim asked for yFar 700 and
  // returned its best try, which misses that row by about 215 px, silently.
  const s09 = probe(V, { aim: { target: AP, heading: 226, distKm: 24, agl: 3600, fov: 50,
                               yTarget: 900, farKm: 70, yFar: 700, VE: 3 }, targets: ENN });
  ok(s09.solve.errPx > 100 && s09.problems.some((p) => p.includes("far ground")),
     `09's unmet yFar should be reported, residual ${s09.solve.errPx}`);
  ok(Math.abs(s09.targets.ENN.y - 900) < 3, "the target row holds even when the far row does not");
  ok(s08.bottomRowKm.centre > 5, `08's bottom row should be far out over the flats, got ${s08.bottomRowKm.centre}`);
  // a ray straight down from a camera on the DEM hits the ground under it
  const down = probe(V, { camera: { lon: AP[0], lat: AP[1], agl: 1000, heading: 0, pitch: -89,
                                    fov: 20, VE: 3 } });
  ok(down.bottomRowKm.centre !== null && Math.abs(down.bottomRowKm.centre) < 1,
     `a camera looking straight down should see ground under itself, got ${down.bottomRowKm.centre}`);
  // a camera looking at the sky finds no ground on its bottom row
  const sky = probe(V, { camera: { lon: AP[0], lat: AP[1], agl: 1000, heading: 0, pitch: 30, fov: 20,
                                   cy: 675, VE: 3 } });
  ok(sky.bottomRowKm.centre === null, "a camera pitched at the sky should find no ground");
  if (fails.length) { fails.forEach((f) => console.log("FAIL " + f)); console.log(`akv_probe self-test: ${fails.length} FAIL`); process.exit(1); }
  console.log("akv_probe self-test: PASS, 7 stations (3 reconstructed defects)");
  console.log(JSON.stringify(round({ s04_round1: { onDem: r1.onDem, problems: r1.problems.length },
    s01_nearTextureM: s01.nearTextureM, s08_nearTextureM: s08.nearTextureM, s09_aimResidualPx: s09.solve.errPx, s08_bottomRowKm: s08.bottomRowKm })));
}

(async () => {
  const args = process.argv.slice(2);
  if (args[0] === "--self-test") return selfTest();
  if (!args.length) { console.error("usage: node scripts/akv_probe.js '<station json>' | --expr '<js>' | --self-test"); process.exit(2); }
  const V = await loadV();
  if (args[0] === "--expr") {
    // eslint-disable-next-line no-eval
    const r = eval("(()=>{" + args[1] + "})()");
    // arbitrary values (a ring, a station) print at full precision
    console.log(JSON.stringify(r));
    return;
  }
  const spec = JSON.parse(args[0] === "--file" ? fs.readFileSync(args[1], "utf8") : args[0]);
  console.log(JSON.stringify(round(probe(V, spec)), null, 1));
})();
