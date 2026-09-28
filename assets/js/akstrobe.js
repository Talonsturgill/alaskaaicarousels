/* akstrobe.js — THE NIGHT STROBE, Carousel No.71's shared furniture (2026-09-28).
 *
 * Deck furniture for a night location shoot: nine separate sets, each its own
 * subject, held together by ONE light and ONE weather. Every slide composes its
 * own scene in its own file; nothing here draws a slide. bespoke_check strips
 * `<script src>` as harness, so the shared snowfall and the shared lens do not
 * read as nine slides of the same art, and they shouldn't: the weather is the
 * same weather because it is the same night.
 *
 *   AKSTROBE.LIGHT
 *     The declared strobe. Azimuth 300, elevation 35 (lit from the upper left,
 *     casts fall to the lower right), key to fill 6 to 1. `dir2` is the
 *     screen-space direction light TRAVELS (toward the lower right), for 2D
 *     frames that cast by hand. Declared once, never varied per slide.
 *
 *   AKSTROBE.snow(cx, o)
 *     The weather clock. Flakes caught by a flash: near flakes are large soft
 *     defocused discs, far flakes are small hard points, and every flake is
 *     brighter the nearer it sits to the strobe's axis (backscatter). One seed,
 *     one wind (12 degrees toward screen left) for the whole deck. `o.layer`
 *     'front' draws only flakes nearer than the focal plane (for plan inserts,
 *     where the weather sits between the lens and the map); 'all' draws both.
 *     `o.avoid` is a list of [x,y,w,h] design-px rects the flakes must not land
 *     on (type reserves): a flake over a letter is noise, not weather.
 *     Returns the drawn flakes as [{x,y,r,a}] in design px.
 *
 *   AKSTROBE.depthPass(THREE, R)
 *     Renders the scene's LINEAR camera distance, packed into two 8-bit
 *     channels (16 bits over [near, far]), reads it back and returns
 *     {w, h, d: Float32Array} in metres at the renderer's backing resolution.
 *     The colour frame must already be on R.renderer's canvas; this does not
 *     disturb it (it renders into a target and restores state).
 *
 *   AKSTROBE.focus(dst, src, depth, o)
 *     A thin-lens focus pull. Six pre-blurred copies of `src` (radii 0 to
 *     o.maxR design px) are gathered per pixel by circle of confusion
 *     coc = o.k * |d - o.focus| / d. The near field gets its OWN coc map,
 *     max-dilated and blurred, so a defocused foreground bleeds over the sharp
 *     plane behind it instead of cutting out like a sticker (technique 99).
 *     `dst` is a 2D context at backing resolution with identity transform.
 */
(function (global) {
  "use strict";
  var S = {};

  S.LIGHT = {
    azDeg: 300, elDeg: 35, keyToFill: 6,
    key: "#EEF2EC", fill: "#5C6F86",
    // screen-space direction light travels (az 300 lights from the upper left)
    dir2: (function () {
      var az = 300 * Math.PI / 180;
      var lx = Math.sin(az), ly = -Math.cos(az);        // where the light IS (x right, y down)
      var n = Math.hypot(lx, ly);
      return [-lx / n, -ly / n];                        // it travels the other way
    })()
  };

  function mulberry(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function inRects(x, y, r, rects) {
    if (!rects) return false;
    for (var i = 0; i < rects.length; i++) {
      var q = rects[i];
      if (x + r > q[0] && x - r < q[0] + q[2] && y + r > q[1] && y - r < q[1] + q[3]) return true;
    }
    return false;
  }

  // One soft disc sprite per blur level, built once and shared.
  var atlas = null;
  function sprites() {
    if (atlas) return atlas;
    atlas = [];
    var levels = [0, 0.35, 0.55, 0.75, 1.0];            // edge softness 0 = hard point
    for (var i = 0; i < levels.length; i++) {
      var s = 128, c = document.createElement("canvas");
      c.width = c.height = s;
      var g = c.getContext("2d");
      var soft = levels[i];
      var grd = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
      var inner = Math.max(0.02, 0.92 - soft * 0.9);
      grd.addColorStop(0, "rgba(255,255,255,1)");
      grd.addColorStop(inner, "rgba(255,255,255," + (0.95 - soft * 0.35).toFixed(3) + ")");
      grd.addColorStop(Math.min(0.999, inner + 0.08 + soft * 0.1), "rgba(255,255,255," + (0.55 - soft * 0.25).toFixed(3) + ")");
      grd.addColorStop(1, "rgba(255,255,255,0)");
      g.fillStyle = grd;
      g.beginPath(); g.arc(s / 2, s / 2, s / 2, 0, Math.PI * 2); g.fill();
      atlas.push(c);
    }
    return atlas;
  }

  S.snow = function (cx, o) {
    o = o || {};
    var W = o.w || 1080, H = o.h || 1350;
    var rnd = mulberry((o.seed || 20260928) * 31 + (o.slide || 1) * 7919);
    var n = o.count || 900;
    var layer = o.layer || "all";
    var focusZ = o.focusZ || 0.45;                      // 0 near .. 1 far
    var sx = o.strobe ? o.strobe[0] : 180, sy = o.strobe ? o.strobe[1] : 120;
    var reach = o.reach || 1500;
    var tint = o.tint || [238, 242, 236];
    var gain = o.gain != null ? o.gain : 1;
    var windRad = (o.windDeg != null ? o.windDeg : 12) * Math.PI / 180;
    var at = sprites(), out = [];
    cx.save();
    cx.globalCompositeOperation = o.blend || "screen";
    for (var i = 0; i < n; i++) {
      var z = Math.pow(rnd(), 0.8);                     // more far flakes than near
      var x = rnd() * (W + 200) - 100, y = rnd() * (H + 200) - 100;
      x += (y / H) * Math.tan(windRad) * -80;           // the wind slants the field
      if (layer === "front" && z > focusZ * 0.6) continue;
      if (layer === "far" && z < focusZ) continue;
      var dz = Math.abs(z - focusZ);
      var near = z < focusZ;
      // size: far flakes are points, near flakes are big soft discs
      var r = near ? 2.2 + (focusZ - z) / focusZ * (o.nearR || 26) : 0.7 + (1 - z) * 2.2;
      if (inRects(x, y, r + 2, o.avoid)) continue;
      var lvl = Math.min(4, Math.floor(dz / Math.max(0.05, focusZ) * 5 * (near ? 1 : 0.35)));
      // backscatter: brighter nearer the strobe axis, falling off with distance
      var dl = Math.hypot(x - sx, y - sy);
      var lit = Math.max(0.08, 1 - dl / reach);
      var a = (near ? 0.30 + 0.25 * rnd() : 0.45 + 0.4 * rnd()) * lit * gain;
      if (near) a *= Math.max(0.35, 1 - (focusZ - z) * 1.2);
      if (o.fade) a *= o.fade(x, y);
      if (a < 0.02) continue;
      cx.globalAlpha = Math.min(1, a);
      if (tint) {
        // sprites are white; a warm or cool tint is applied through a filter-free
        // multiply by drawing at the flake's alpha, tint carried by the caller's
        // blend. White is the strobe's own colour, so the default is untinted.
      }
      cx.drawImage(at[lvl], x - r, y - r, r * 2, r * 2);
      out.push({ x: x, y: y, r: r, a: a });
    }
    cx.restore();
    return out;
  };

  S.depthPass = function (THREE, R) {
    var renderer = R.renderer, scene = R.scene, camera = R.camera;
    var size = new THREE.Vector2();
    renderer.getDrawingBufferSize(size);
    var W = size.x, H = size.y;
    var near = camera.near, far = camera.far;
    var mat = new THREE.ShaderMaterial({
      uniforms: { uNear: { value: near }, uFar: { value: far } },
      vertexShader:
        "varying float vDist;\n" +
        "void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vDist = -mv.z; gl_Position = projectionMatrix * mv; }",
      fragmentShader:
        "uniform float uNear; uniform float uFar; varying float vDist;\n" +
        "void main(){ float t = clamp((vDist - uNear)/(uFar - uNear), 0.0, 1.0);\n" +
        " float v = t * 65535.0; float hi = floor(v / 256.0); float lo = v - hi * 256.0;\n" +
        " gl_FragColor = vec4(hi/255.0, lo/255.0, 0.0, 1.0); }"
    });
    var rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType });
    var oldBg = scene.background, oldFog = scene.fog, oldOverride = scene.overrideMaterial;
    var oldTone = renderer.toneMapping;
    scene.background = new THREE.Color(1, 1, 0); scene.fog = null;
    scene.overrideMaterial = mat; renderer.toneMapping = THREE.NoToneMapping;
    var hidden = [];
    scene.traverse(function (m) { if (m.userData && m.userData.noDepth && m.visible) { m.visible = false; hidden.push(m); } });
    renderer.setRenderTarget(rt);
    renderer.render(scene, camera);
    var buf = new Uint8Array(W * H * 4);
    renderer.readRenderTargetPixels(rt, 0, 0, W, H, buf);
    renderer.setRenderTarget(null);
    hidden.forEach(function (m) { m.visible = true; });
    scene.background = oldBg; scene.fog = oldFog; scene.overrideMaterial = oldOverride;
    renderer.toneMapping = oldTone;
    rt.dispose(); mat.dispose();
    var d = new Float32Array(W * H);
    for (var y = 0; y < H; y++) {
      var row = (H - 1 - y) * W;                        // GL rows are bottom-up
      for (var x = 0; x < W; x++) {
        var p = (row + x) * 4;
        var t = (buf[p] * 256 + buf[p + 1]) / 65535;
        d[y * W + x] = near + t * (far - near);
      }
    }
    return { w: W, h: H, d: d };
  };

  S.focus = function (dst, src, depth, o) {
    o = o || {};
    var W = depth.w, H = depth.h, sc = o.scale || 2;
    var maxR = (o.maxR || 9) * sc, k = (o.k || 12) * sc, f = o.focus;
    var levels = 6, radii = [];
    for (var i = 0; i < levels; i++) radii.push(maxR * i / (levels - 1));
    var imgs = [];
    for (i = 0; i < levels; i++) {
      var c = document.createElement("canvas"); c.width = W; c.height = H;
      var g = c.getContext("2d");
      if (radii[i] > 0.01) g.filter = "blur(" + (radii[i] * 0.5).toFixed(2) + "px)";
      g.drawImage(src, 0, 0, W, H);
      imgs.push(g.getImageData(0, 0, W, H).data);
    }
    // per-pixel coc, and a separate near-field coc that is dilated and blurred
    var coc = new Float32Array(W * H), nearC = document.createElement("canvas");
    nearC.width = W >> 2; nearC.height = H >> 2;
    var nq = nearC.getContext("2d"), nimg = nq.createImageData(nearC.width, nearC.height);
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var dd = depth.d[y * W + x];
      var cc = Math.min(maxR, k * Math.abs(dd - f) / Math.max(0.1, dd));
      coc[y * W + x] = cc;
      if (dd < f && (x & 3) === 0 && (y & 3) === 0) {
        var q = ((y >> 2) * nearC.width + (x >> 2)) * 4;
        var v = Math.round(255 * cc / maxR);
        nimg.data[q] = v; nimg.data[q + 3] = 255;
      }
    }
    nq.putImageData(nimg, 0, 0);
    var nb = document.createElement("canvas"); nb.width = nearC.width; nb.height = nearC.height;
    var nbq = nb.getContext("2d");
    nbq.filter = "blur(" + Math.max(1, maxR / 8).toFixed(1) + "px)";
    nbq.drawImage(nearC, 0, 0);
    var nd = nbq.getImageData(0, 0, nb.width, nb.height).data;
    var out = dst.createImageData(W, H), od = out.data;
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) {
      var idx = y * W + x;
      var nn = nd[(((y >> 2) * nb.width) + (x >> 2)) * 4] / 255 * maxR;
      var r = Math.max(coc[idx], nn * 1.6);
      var t = Math.min(levels - 1, r / maxR * (levels - 1));
      var l0 = Math.floor(t), l1 = Math.min(levels - 1, l0 + 1), fr = t - l0;
      var p = idx * 4, A = imgs[l0], B = imgs[l1];
      od[p] = A[p] + (B[p] - A[p]) * fr;
      od[p + 1] = A[p + 1] + (B[p + 1] - A[p + 1]) * fr;
      od[p + 2] = A[p + 2] + (B[p + 2] - A[p + 2]) * fr;
      od[p + 3] = 255;
    }
    dst.putImageData(out, 0, 0);
    return { focus: f, maxR: maxR / sc };
  };

  global.AKSTROBE = S;
})(typeof window !== "undefined" ? window : globalThis);
