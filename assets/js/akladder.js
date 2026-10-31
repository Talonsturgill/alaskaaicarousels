/* akladder.js — THE UNIT LADDER, Carousel No.100's shared furniture (2026-10-30).
 *
 * One 100 kW cabinet is the unit; a fixed 10 by 10 pad of them is a course of
 * 10 MW. This file holds what every frame of the deck shares and nothing that
 * draws a frame: the palette, the fixtures, the ladder ticker under the
 * counter, the one ember key, the cabinet and gravel textures, and the
 * orthographic framing that keeps every height in its true ratio. Each slide
 * composes its own scene in its own file.
 *
 *   AKL.PAL, AKL.GOLD          the deck palette (storyboard PALETTE)
 *   AKL.KEY                    the one key: azimuth 248, elevation 22
 *   AKL.UNIT                   cabinet size in metres {w: 1.8, h: 2.0, d: 0.9}
 *   AKL.fixtures(n, o)         wordmark, Polaris, counter, site, coordinates
 *   AKL.ticker(marks, o)       the log ladder ticker, 0.1 MW to 3,000 MW
 *   AKL.tickerScale(marks)     the matching data-scale entry (for checking)
 *   AKL.grain(o)               grain as a DOM tile above the art
 *   AKL.keyDir()               world unit vector TOWARD the key (x east, z south)
 *   AKL.doorFace(THREE, n, o)  CanvasTexture of n cabinet fronts side by side
 *   AKL.gravel(THREE, o)       CanvasTexture of frost gravel
 *   AKL.ortho(THREE, R, o)     orthographic camera placing a world point at a
 *                              screen point at s px per metre
 *   AKL.sky(THREE, o)          CanvasTexture sky gradient for scene.background
 *
 * Determinism: every texture is seeded through AK.rng / AK.simplex2.
 */
(function (global) {
  "use strict";
  var L = {};

  L.GOLD = '#FFC72C';
  L.PAL = {
    zenith: '#060E1E', skyMid: '#12223C', haze: '#8A5A48', ember: '#D08A5E',
    gravelLit: '#BDB1A0', gravelShade: '#48536A', contact: '#1C2638',
    cabLit: '#9AA3AD', cabBase: '#3B4552', cabLee: '#1F2733', seam: '#121822',
    chalkLit: '#C9CDD2', chalkLee: '#6B7480',
    ghost: '#6EA5FF', proposal: '#7CC7DD', passed: '#B4BFCC',
    snowLit: '#E9E2D6', snowLee: '#4A5A74', water: '#14243A', tundra: '#7A6E5A',
    type: '#F4F8FF', type2: '#B4BFCC', mono: '#8090A3', fixture: '#46545F'
  };
  L.KEY = { az: 248, el: 22 };
  L.UNIT = { w: 1.8, h: 2.0, d: 0.9 };

  /* World vector toward the key. x is east, z is SOUTH (so the camera in the
   * +x +z quadrant looks north-west), y up. */
  L.keyDir = function (az, el) {
    az = (az == null ? L.KEY.az : az) * Math.PI / 180;
    el = (el == null ? L.KEY.el : el) * Math.PI / 180;
    var e = Math.sin(az), n = Math.cos(az);
    return [e * Math.cos(el), Math.sin(el), -n * Math.cos(el)];
  };

  /* ---- fixtures -------------------------------------------------------- */
  L.polaris = function (x, y, s, z) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', s); svg.setAttribute('height', s);
    svg.setAttribute('viewBox', '-50 -50 100 100');
    svg.setAttribute('style', 'position:absolute;left:' + (x - s / 2) + 'px;top:' + (y - s / 2) +
      'px;z-index:' + (z || 9) + ';overflow:visible;');
    svg.setAttribute('data-decorative', '');
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', 'M0,-50 C4,-14 14,-4 50,0 C14,4 4,14 0,50 C-4,14 -14,4 -50,0 C-14,-4 -4,-14 0,-50 Z');
    p.setAttribute('fill', L.GOLD);
    svg.appendChild(p);
    document.body.appendChild(svg);
    return svg;
  };

  L.fixtures = function (n, o) {
    o = o || {};
    var css = 'position:absolute;z-index:9;font-family:"JetBrains Mono",monospace;';
    function add(txt, style, deco) {
      var d = document.createElement('div');
      d.setAttribute('style', css + style); d.textContent = txt;
      if (deco) d.setAttribute('data-decorative', '');
      document.body.appendChild(d); return d;
    }
    add('ALASKA.AI', 'left:80px;top:80px;font-family:"Archivo",sans-serif;font-stretch:75%;font-weight:700;font-size:30px;letter-spacing:0.10em;color:' + (o.ink || L.PAL.type) + ';');
    add((n < 10 ? '0' : '') + n + ' / 10', 'right:80px;top:84px;font-size:24px;letter-spacing:0.06em;color:' + (o.counter || L.PAL.type2) + ';font-variant-numeric:tabular-nums;');
    // a watermark, low contrast on the dark register; a tight dark halo keeps it findable where the art under it is light
    var halo = 'text-shadow:0 0 2px #060C18,0 0 5px #060C18,0 0 9px #060C18;';
    add('alaskaaihq.com', 'left:80px;top:1288px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || '#7A8898') + ';' + halo, true);
    if (o.coords) add(o.coords, 'right:80px;top:1288px;font-size:19px;letter-spacing:0.04em;color:' + (o.site || '#7A8898') + ';' + halo, true);
  };

  /* ---- the ladder ticker ---------------------------------------------- */
  /* A 176 px log rule under the counter: x = 824 + 176 log10(MW / 0.1) / log10(30000).
   * Rungs at 0.1 (gold notch, always), 5, 15, 100 and 3,000. `marks` are the MW
   * values this frame is about, drawn as taller snow ticks. Values that land on
   * an existing rung replace it rather than adding a second tick. */
  L.TICK = { x0: 824, x1: 1000, y: 128, h: 14 };
  L.RUNGS = [0.1, 5, 15, 100, 3000];
  L.tx = function (mw) {
    return L.TICK.x0 + (L.TICK.x1 - L.TICK.x0) * Math.log10(mw / 0.1) / Math.log10(30000);
  };
  L.ticker = function (marks, o) {
    o = o || {};
    marks = marks || [];
    var NS = 'http://www.w3.org/2000/svg', T = L.TICK;
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', 200); svg.setAttribute('height', 40);
    svg.setAttribute('viewBox', '808 112 200 40');
    svg.setAttribute('style', 'position:absolute;left:808px;top:112px;z-index:9;overflow:visible;');
    svg.setAttribute('data-decorative', '');
    function line(x1, y1, x2, y2, c, w) {
      var l = document.createElementNS(NS, 'line');
      l.setAttribute('x1', x1); l.setAttribute('y1', y1); l.setAttribute('x2', x2); l.setAttribute('y2', y2);
      l.setAttribute('stroke', c); l.setAttribute('stroke-width', w); l.setAttribute('stroke-linecap', 'butt');
      svg.appendChild(l);
    }
    var base = T.y + T.h;
    line(T.x0, base, T.x1, base, o.rule || '#56657A', 1);
    L.RUNGS.forEach(function (mw) {
      if (mw === 0.1) return;
      var hot = marks.indexOf(mw) !== -1;
      line(L.tx(mw), base - (hot ? T.h : 9), L.tx(mw), base, hot ? L.PAL.type : '#9AA6B6', hot ? 2 : 1.6);
    });
    marks.forEach(function (mw) {
      if (L.RUNGS.indexOf(mw) !== -1) return;
      line(L.tx(mw), base - T.h, L.tx(mw), base, L.PAL.type, 2);
    });
    line(T.x0 + 2, base - 11, T.x0 + 2, base, L.GOLD, 4);
    document.body.appendChild(svg);
    return svg;
  };
  /* The data-scale entry the markup must carry (body attribute, literal). Kept
   * here only so a slide can assert its markup agrees with what was drawn. */
  L.tickerScale = function (marks) {
    var T = L.TICK, all = [], seen = {};
    function m(mw, means) { var x = Math.round(L.tx(mw) * 10) / 10; if (seen[x]) return; seen[x] = 1; all.push({ at: x, means: means }); }
    m(0.1, '100 kW, the unit');
    (marks || []).forEach(function (mw) { m(mw, mw + ' MW'); });
    L.RUNGS.forEach(function (mw) { m(mw, mw + ' MW'); });
    return { what: 'the ladder ticker', axis: 'x', unit: 'log10 MW', from: [T.x0, -1], to: [T.x1, Math.log10(3000)],
             band: [T.y, T.y + T.h + 1], marks: all };
  };

  /* ---- grain ------------------------------------------------------------ */
  L.grain = function (o) {
    o = o || {};
    var d = document.createElement('div');
    d.setAttribute('style', 'position:absolute;inset:0;z-index:5;pointer-events:none;mix-blend-mode:overlay;opacity:' + (o.opacity || 0.06));
    document.body.appendChild(d);
    AK.grainOn(d, { size: 280, strength: o.strength || 40, seed: o.seed || 100 });
    return d;
  };

  /* ---- textures for the GL frames -------------------------------------- */
  /* n cabinet fronts side by side on one course face, with door seams,
   * perforation, a top grille line and a course seam at the top. `px` is the
   * texture height in px; width is px * n * aspect. Returns a CanvasTexture. */
  L.doorFace = function (THREE, n, o) {
    o = o || {};
    var aspect = (o.unitW || L.UNIT.w) / L.UNIT.h;
    var H = o.px || 256, W = Math.min(8192, Math.round(H * aspect * n));
    var c = document.createElement('canvas'); c.width = W; c.height = H;
    var g = c.getContext('2d');
    var uw = W / n, rnd = AK.rng(o.seed || 1001);
    g.fillStyle = o.base || '#7C8692'; g.fillRect(0, 0, W, H);
    for (var i = 0; i < n; i++) {
      var x0 = i * uw;
      // two doors per cabinet, a slim frame, perforation field, a grille band
      var t = Math.max(1, uw * 0.03);
      var tone = 122 + Math.floor(rnd() * 10);
      g.fillStyle = 'rgb(' + tone + ',' + (tone + 12) + ',' + (tone + 28) + ')';     // cool painted steel
      g.fillRect(x0 + t, H * 0.07, uw - 2 * t, H * 0.86);
      if (uw > 10) {
        g.fillStyle = 'rgba(16,22,32,0.55)';
        g.fillRect(x0 + uw / 2 - t * 0.5, H * 0.07, t, H * 0.86);       // door split
        if (uw > 24) {
          g.fillStyle = 'rgba(20,26,36,' + (uw < 200 ? 0.12 : 0.32) + ')';   // faint at course scale, where a dense field strobes
          var step = Math.max(3, uw / 26);
          for (var py = H * 0.16; py < H * 0.86; py += step)
            for (var px = x0 + t * 3; px < x0 + uw - t * 3; px += step) {
              if (Math.abs(px - (x0 + uw / 2)) < t * 2) continue;
              g.fillRect(px, py, step * 0.42, step * 0.42);
            }
          g.fillStyle = 'rgba(210,216,224,0.45)';                       // handle glints
          g.fillRect(x0 + uw / 2 - t * 3, H * 0.44, t * 1.2, H * 0.12);
          g.fillRect(x0 + uw / 2 + t * 1.8, H * 0.44, t * 1.2, H * 0.12);
        }
      }
      g.fillStyle = 'rgba(14,18,26,0.85)';
      g.fillRect(x0, 0, Math.max(1, t * 0.8), H);                       // cabinet seam
    }
    g.fillStyle = 'rgba(12,16,24,0.95)'; g.fillRect(0, 0, W, Math.max(2, H * 0.035));   // course seam
    g.fillStyle = 'rgba(40,46,56,1)'; g.fillRect(0, H * 0.93, W, H * 0.07);              // plinth
    var tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 8;
    return tex;
  };

  /* Frost gravel, tileable enough at the repeats used here. */
  L.gravel = function (THREE, o) {
    o = o || {};
    var S = o.px || 1024;
    var c = document.createElement('canvas'); c.width = c.height = S;
    var g = c.getContext('2d');
    var img = g.createImageData(S, S), d = img.data;
    AK.reseed(o.seed || 2026103000);
    for (var y = 0; y < S; y++) for (var x = 0; x < S; x++) {
      var u = x / S * 18, v = y / S * 18;
      var n1 = AK.simplex2(u * 3.1, v * 3.1), n2 = AK.simplex2(u * 9.7 + 31, v * 9.7 + 7);
      var pebble = Math.max(0, n1) * 0.55 + n2 * 0.25;
      var base = 0.72 + pebble * 0.35 + AK.simplex2(u * 0.6, v * 0.6) * 0.06;
      var r = 189 * base, gg = 177 * base, b = 160 * base;
      var i = (y * S + x) * 4;
      d[i] = Math.min(255, r); d[i + 1] = Math.min(255, gg); d[i + 2] = Math.min(255, b); d[i + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    var rnd = AK.rng((o.seed || 2026103000) + 7);
    for (var k = 0; k < (o.frost || 2600); k++) {            // hoarfrost specks
      g.fillStyle = 'rgba(238,244,250,' + (0.35 + rnd() * 0.5) + ')';
      g.fillRect(rnd() * S, rnd() * S, 1 + rnd() * 1.2, 1 + rnd() * 1.2);
    }
    var tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 8;
    return tex;
  };

  /* A vertical sky gradient (OKLCH-ish stops chosen by hand) for scene.background. */
  L.sky = function (THREE, o) {
    o = o || {};
    var c = document.createElement('canvas'); c.width = 8; c.height = 1024;
    var g = c.getContext('2d');
    var gr = g.createLinearGradient(0, 0, 0, 1024);
    var stops = o.stops || [[0, L.PAL.zenith], [0.55, L.PAL.skyMid], [0.86, '#3A2E3E'], [0.95, L.PAL.haze], [1, L.PAL.ember]];
    stops.forEach(function (s) { gr.addColorStop(s[0], s[1]); });
    g.fillStyle = gr; g.fillRect(0, 0, 8, 1024);
    var tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  };

  /* Orthographic camera at azimuth `az` (degrees, from +z toward +x) and
   * elevation `el`, s px per metre, placing world point `target` at screen
   * point `screen` (design px). Returns the camera (also set on R). */
  L.ortho = function (THREE, R, o) {
    var s = o.s, sx = o.screen[0], sy = o.screen[1];
    var cam = new THREE.OrthographicCamera(-sx / s, (1080 - sx) / s, sy / s, -(1350 - sy) / s, 0.1, o.far || 4000);
    var az = o.az * Math.PI / 180, el = o.el * Math.PI / 180, dist = o.dist || 1500;
    var t = o.target;
    cam.position.set(t[0] + dist * Math.sin(az) * Math.cos(el), t[1] + dist * Math.sin(el), t[2] + dist * Math.cos(az) * Math.cos(el));
    cam.lookAt(t[0], t[1], t[2]);
    cam.updateProjectionMatrix();
    R.camera = cam;
    return cam;
  };


  /* One course: a 10 by 10 pad of cabinets as a single box (18 m by 2 m by 9 m)
   * with the cabinet fronts printed on its south and east faces and a grille
   * on top. o.ghost draws the course as the upper end of a stated range (a
   * glass-thin ghost fill and its edges), never as built steel. Textures are
   * cached per THREE instance. Returns a Group whose base sits at y = 0. */
  L.course = function (THREE, o) {
    o = o || {};
    var U = L.UNIT, W = U.w * 10, D = U.d * 10, H = U.h;
    var cache = L.__cache || (L.__cache = {});   // THREE is a frozen module namespace; one THREE per page
    var g = new THREE.Group();
    if (o.ghost) {
      var gm = cache.ghostMat || (cache.ghostMat = new THREE.MeshStandardMaterial({
        color: 0x101C3A, transparent: true, opacity: o.opacity || 0.22, roughness: 0.3, metalness: 0, depthWrite: false, fog: false }));
      var gb = new THREE.Mesh(new THREE.BoxGeometry(W, H * 0.98, D), gm);
      gb.position.y = H / 2; gb.userData.noDepth = true; g.add(gb);
      var e = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(W, H * 0.98, D)),
        cache.ghostLine || (cache.ghostLine = new THREE.LineBasicMaterial({ color: 0x6EA5FF, transparent: true, opacity: 0.75, fog: false })));
      e.position.y = H / 2; g.add(e);
      return g;
    }
    if (!cache.front) {
      cache.front = L.doorFace(THREE, 10, { px: o.px || 160, seed: 11 });
      cache.side = L.doorFace(THREE, 10, { px: o.px || 160, unitW: U.d, seed: 12 });
      var c = document.createElement('canvas'); c.width = 512; c.height = 256;
      var q = c.getContext('2d'); q.fillStyle = '#2E3640'; q.fillRect(0, 0, 512, 256);
      for (var i = 0; i < 10; i++) for (var s = 0; s < 8; s++) {
        q.fillStyle = 'rgba(12,16,22,0.9)'; q.fillRect(i * 51.2 + 6 + s * 5.2, 30, 2.6, 196);
      }
      q.strokeStyle = 'rgba(10,14,20,1)'; q.lineWidth = 2;
      for (var k = 0; k <= 10; k++) { q.beginPath(); q.moveTo(k * 51.2, 0); q.lineTo(k * 51.2, 256); q.stroke(); }
      cache.top = new THREE.CanvasTexture(c); cache.top.colorSpace = THREE.SRGBColorSpace;
      cache.mFront = new THREE.MeshStandardMaterial({ map: cache.front, roughness: 0.5, metalness: 0.12, fog: false });
      cache.mSide = new THREE.MeshStandardMaterial({ map: cache.side, roughness: 0.5, metalness: 0.12, fog: false });
      cache.mTop = new THREE.MeshStandardMaterial({ map: cache.top, roughness: 0.6, metalness: 0.1, fog: false });
      cache.mDark = new THREE.MeshStandardMaterial({ color: 0x1A2028, roughness: 0.7, fog: false });
    }
    var b = new THREE.Mesh(new THREE.BoxGeometry(W, H, D),
      [cache.mSide, cache.mSide, o.top === false ? cache.mDark : cache.mTop, cache.mDark, cache.mFront, cache.mFront]);
    b.position.y = H / 2; b.castShadow = true; b.receiveShadow = true; g.add(b);
    if (o.bold) {                                   // the 100 MW seam: a proud steel band at the course top
      var band = new THREE.Mesh(new THREE.BoxGeometry(W + 0.24, 0.32, D + 0.24),
        cache.mBand || (cache.mBand = new THREE.MeshStandardMaterial({ color: 0xB8C0CA, roughness: 0.35, metalness: 0.5, fog: false })));
      band.position.y = H - 0.16; band.castShadow = true; band.receiveShadow = true; g.add(band);
    }
    return g;
  };

  global.AKL = L;
})(typeof window !== "undefined" ? window : globalThis);
