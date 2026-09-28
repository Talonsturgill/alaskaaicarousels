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
 *     {w, h, d: Float32Array} in the CAMERA's units (whatever near and far are
 *     in: metres for this deck's scenes, kilometres for an AKBLOCK frame) at the
 *     renderer's backing resolution. `focus`'s o.focus is in the same units.
 *     The colour frame must already be on R.renderer's canvas; this does not
 *     disturb it (it renders into a target and restores state).
 *
 *   AKSTROBE.focus(dst, src, depth, o)
 *     A thin-lens focus pull. Six pre-blurred copies of `src` (radii 0 to
 *     o.maxR design px) are gathered per pixel by circle of confusion
 *     coc = o.k * |d - o.focus| / d, with d and o.focus both in the camera's units
 *     (the ratio makes o.k unit-free). The near field gets its OWN coc map,
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
    var W = o.w == null ? 1080 : o.w, H = o.h == null ? 1350 : o.h;
    var rnd = mulberry((o.seed == null ? 20260928 : o.seed) * 31 + (o.slide == null ? 1 : o.slide) * 7919);
    var n = o.count == null ? 900 : o.count;            // 0 is a real request: an empty layer
    var layer = o.layer || "all";
    var focusZ = o.focusZ == null ? 0.45 : o.focusZ;    // 0 near .. 1 far; 0 is a real request
    var sx = o.strobe ? o.strobe[0] : 180, sy = o.strobe ? o.strobe[1] : 120;
    var reach = Math.max(1, o.reach == null ? 1500 : o.reach);   // a reach of 0 would divide by zero
    var tint = o.tint || null;                          // null: the atlas's own white, the strobe's colour
    var gain = o.gain != null ? o.gain : 1;
    var windRad = (o.windDeg != null ? o.windDeg : 12) * Math.PI / 180;
    var at = sprites(), out = [];
    if (tint) {
      // an explicit tint recolours each atlas level once: the sprite's alpha kept, its colour replaced
      at = at.map(function (c) {
        var t = document.createElement("canvas"); t.width = c.width; t.height = c.height;
        var g = t.getContext("2d"); g.drawImage(c, 0, 0);
        g.globalCompositeOperation = "source-in";
        g.fillStyle = "rgb(" + tint[0] + "," + tint[1] + "," + tint[2] + ")"; g.fillRect(0, 0, t.width, t.height);
        return t;
      });
    }
    cx.save();
    cx.globalCompositeOperation = o.blend || "screen";
    for (var i = 0; i < n; i++) {
      // every candidate draws ALL its random numbers before any filter (Codex, PR #407), so changing
      // layer, avoid or fade only removes flakes from one shared field and never reshuffles it
      var z = Math.pow(rnd(), 0.8);                     // more far flakes than near
      var x = rnd() * (W + 200) - 100, y = rnd() * (H + 200) - 100;
      var ra = rnd();
      x += (y / H) * Math.tan(windRad) * -80;           // the wind slants the field
      if (layer === "front" && z > focusZ * 0.6) continue;
      if (layer === "far" && z < focusZ) continue;
      var dz = Math.abs(z - focusZ);
      var near = z < focusZ;
      // size: far flakes are points, near flakes are big soft discs
      var r = near ? 2.2 + (focusZ - z) / focusZ * (o.nearR == null ? 26 : o.nearR) : 0.7 + (1 - z) * 2.2;
      if (inRects(x, y, r + 2, o.avoid)) continue;
      var lvl = Math.min(4, Math.floor(dz / Math.max(0.05, focusZ) * 5 * (near ? 1 : 0.35)));
      // backscatter: brighter nearer the strobe axis, falling off with distance
      var dl = Math.hypot(x - sx, y - sy);
      var lit = Math.max(0.08, 1 - dl / reach);
      var a = (near ? 0.30 + 0.25 * ra : 0.45 + 0.4 * ra) * lit * gain;
      if (near) a *= Math.max(0.35, 1 - (focusZ - z) * 1.2);
      if (o.fade) a *= o.fade(x, y);
      if (a < 0.02) continue;
      cx.globalAlpha = Math.min(1, a);
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
    /* THE COLOUR PASS'S OWN DEPTH (Codex, PR #407, seven rounds). Every earlier version swapped the
     * scene's materials for a depth shader, and each round found one more thing a swap can't know:
     * instancing, face side, lines, points and sprites, skinning and morph targets, a material
     * hidden by its own `visible`. So nothing is swapped. The scene renders exactly as the colour
     * pass does, into a target carrying a depth texture, and a second full-screen pass turns that
     * depth buffer into linear distance. Whatever the colour pass drew, and nothing it did not, is
     * what the focus map sees. Objects flagged userData.noDepth are still left out. */
    var dt = new THREE.DepthTexture(W, H);
    dt.type = THREE.UnsignedIntType;
    var rt = new THREE.WebGLRenderTarget(W, H, { depthTexture: dt, depthBuffer: true });
    var hidden = [];
    scene.traverse(function (m) { if (m.userData && m.userData.noDepth && m.visible) { m.visible = false; hidden.push(m); } });
    /* A VISIBLE SURFACE IS IN THE FOCUS MAP EVEN IF IT SKIPS DEPTH WRITES (Codex, PR #407). Glass,
     * a contact decal or a sprite drawn with depthWrite false paints colour and leaves the depth
     * behind it, so its pixels would take the focus of whatever it covers. For this one render such
     * materials write depth, scene.overrideMaterial included when the colour pass used one.
     * ONLY WHERE THEY PAINTED (Codex, PR #407, next round): a blended sprite's clear texels or an
     * opacity-zero mesh must not become a blur occluder, so each one also gets an alpha test for
     * the render (kept if its own is stricter) and a fragment with nothing to show writes nothing.
     * A custom ShaderMaterial has no alpha test to borrow; userData.noDepth leaves any surface out. */
    var unwritten = [], VISIBLE_ALPHA = 1 / 255;
    function writeDepth(mt) {
      if (!mt || mt.depthWrite !== false || unwritten.some(function (u) { return u.mt === mt; })) return;
      unwritten.push({ mt: mt, alphaTest: mt.alphaTest });
      mt.depthWrite = true;
      if (!(mt.alphaTest >= VISIBLE_ALPHA)) mt.alphaTest = VISIBLE_ALPHA;
    }
    if (scene.overrideMaterial) writeDepth(scene.overrideMaterial);
    else scene.traverse(function (m) {
      if (!m.visible || !m.material) return;
      (Array.isArray(m.material) ? m.material : [m.material]).forEach(writeDepth);
    });
    // restored below exactly as the caller had it bound: target, cube face and mip level (Codex, PR #407)
    var oldTarget = renderer.getRenderTarget(), oldFace = renderer.getActiveCubeFace(), oldMip = renderer.getActiveMipmapLevel();
    // and the ACTIVE viewport and scissor, which setRenderTarget would reload from the target itself
    var oldVp = new THREE.Vector4(), oldSc = new THREE.Vector4(), oldScT = renderer.getScissorTest();
    renderer.getViewport(oldVp); renderer.getScissor(oldSc);
    var oldTone = renderer.toneMapping;
    renderer.setRenderTarget(rt);
    renderer.clear(true, true, true);                    // whatever the caller's autoClear policy: far everywhere first
    // a colour frame drawn to the canvas through a custom viewport or scissor gets its depth through the
    // same rectangle, so the two align (Codex, PR #407); the full-canvas default is a no-op
    if (!oldTarget) { renderer.setViewport(oldVp); renderer.setScissor(oldSc); renderer.setScissorTest(oldScT); }
    renderer.render(scene, camera);
    renderer.setScissorTest(false);
    hidden.forEach(function (m) { m.visible = true; });
    unwritten.forEach(function (u) { u.mt.depthWrite = false; u.mt.alphaTest = u.alphaTest; });
    var q = new THREE.ShaderMaterial({
      uniforms: { tD: { value: dt }, uNear: { value: near }, uFar: { value: far },
                  uPersp: { value: camera.isPerspectiveCamera ? 1 : 0 } },
      vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
      fragmentShader:
        "uniform sampler2D tD; uniform float uNear; uniform float uFar; uniform float uPersp; varying vec2 vUv;\n" +
        "void main(){ float d = texture2D(tD, vUv).x;\n" +
        " float z = uPersp > 0.5 ? (uNear * uFar) / (uFar - d * (uFar - uNear)) : uNear + d * (uFar - uNear);\n" +
        " float t = d >= 1.0 ? 1.0 : clamp((z - uNear) / (uFar - uNear), 0.0, 1.0);\n" +
        " float v = t * 65535.0; float hi = floor(v / 256.0); float lo = v - hi * 256.0;\n" +
        " gl_FragColor = vec4(hi / 255.0, lo / 255.0, 0.0, 1.0); }",
      depthTest: false, depthWrite: false
    });
    q.toneMapped = false;
    var qs = new THREE.Scene(), oc = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    var quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), q);
    quad.frustumCulled = false; qs.add(quad);
    var rt2 = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType, depthBuffer: false });
    renderer.toneMapping = THREE.NoToneMapping;
    renderer.setRenderTarget(rt2);
    renderer.render(qs, oc);
    var buf = new Uint8Array(W * H * 4);
    renderer.readRenderTargetPixels(rt2, 0, 0, W, H, buf);
    renderer.setRenderTarget(oldTarget, oldFace, oldMip);
    renderer.setViewport(oldVp); renderer.setScissor(oldSc); renderer.setScissorTest(oldScT);
    renderer.toneMapping = oldTone;
    rt.dispose(); rt2.dispose(); dt.dispose(); q.dispose(); quad.geometry.dispose();
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
    var W = depth.w, H = depth.h, sc = o.scale == null ? 2 : o.scale;
    var maxR = (o.maxR == null ? 9 : o.maxR) * sc, k = (o.k == null ? 12 : o.k) * sc, f = o.focus;   // 0 is a real request
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
    nearC.width = (W + 3) >> 2; nearC.height = (H + 3) >> 2;   // ceil: x >> 2 and y >> 2 index the last rows too
    var nq = nearC.getContext("2d"), nimg = nq.createImageData(nearC.width, nearC.height);
    // every cell opaque before the blur (Codex, PR #407): a transparent neighbour would leave the blurred
    // red channel near full strength with only its alpha attenuated, a hard halo instead of a falloff
    for (var ai = 3; ai < nimg.data.length; ai += 4) nimg.data[ai] = 255;
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      var dd = depth.d[y * W + x];
      var cc = Math.min(maxR, k * Math.abs(dd - f) / Math.max(0.1, dd));
      coc[y * W + x] = cc;
      if (dd < f) {
        // max-pool the foreground CoC over each 4 x 4 cell (Codex, PR #407): a near feature thinner
        // than a cell must still bleed its blur over the in-focus background around it
        var q = ((y >> 2) * nearC.width + (x >> 2)) * 4;
        var v = maxR > 0 ? Math.round(255 * cc / maxR) : 0;
        if (v > nimg.data[q]) nimg.data[q] = v;
        nimg.data[q + 3] = 255;
      }
    }
    nq.putImageData(nimg, 0, 0);
    var nb = document.createElement("canvas"); nb.width = nearC.width; nb.height = nearC.height;
    var nbq = nb.getContext("2d");
    nbq.filter = "blur(" + Math.max(1, maxR / 8).toFixed(1) + "px)";
    nbq.drawImage(nearC, 0, 0);
    var nd = nbq.getImageData(0, 0, nb.width, nb.height).data;
    // an opaque source stays opaque: the blur's own falloff at the frame edge is not the layer's alpha.
    // A source that really carries transparency keeps it, blurred with the colour (Codex, PR #407).
    var src0 = imgs[0], opaque = true;
    for (var ai = 3; ai < src0.length; ai += 4) if (src0[ai] < 255) { opaque = false; break; }
    var out = dst.createImageData(W, H), od = out.data;
    for (y = 0; y < H; y++) for (x = 0; x < W; x++) {
      var idx = y * W + x;
      var nn = nd[(((y >> 2) * nb.width) + (x >> 2)) * 4] / 255 * maxR;
      var r = Math.max(coc[idx], nn * 1.6);
      var t = maxR > 0 ? Math.min(levels - 1, r / maxR * (levels - 1)) : 0;   // maxR 0: the sharp level everywhere
      var l0 = Math.floor(t), l1 = Math.min(levels - 1, l0 + 1), fr = t - l0;
      var p = idx * 4, A = imgs[l0], B = imgs[l1];
      od[p] = A[p] + (B[p] - A[p]) * fr;
      od[p + 1] = A[p + 1] + (B[p + 1] - A[p + 1]) * fr;
      od[p + 2] = A[p + 2] + (B[p + 2] - A[p + 2]) * fr;
      od[p + 3] = opaque ? 255 : A[p + 3] + (B[p + 3] - A[p + 3]) * fr;
    }
    dst.putImageData(out, 0, 0);
    return { focus: f, maxR: maxR / sc };
  };

  global.AKSTROBE = S;
})(typeof window !== "undefined" ? window : globalThis);
