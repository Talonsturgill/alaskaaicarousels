/* akport.js — the Port MacKenzie bench (added 2026-10-08, No.81).
 *
 * DECK FURNITURE, shared across the frames of the deck about the University
 * of Alaska's 829-acre lease near Port MacKenzie. Classic script, global
 * AKPORT. bespoke_check strips `<script src=>` as harness, so shared
 * geometry and fixtures cost the variety budget nothing while every frame's
 * own drawing code still has to be its own.
 *
 * WHAT IT OWNS
 *   AKPORT.loadLand(assets)   the committed T14N R4W Seward Meridian sections
 *                             and the four UA parcels (assets/geo/
 *                             ak-pointmac-t14n-r4w.geo.json, from BLM
 *                             CadNSDI). Returns {sections, parcels, parts,
 *                             bounds, acres}. `acres` is summed from the
 *                             features' own record areas, so a frame that
 *                             prints 829.34 can assert it against the data.
 *   AKPORT.projector(bounds, box)  a local equal-scale projection (lon
 *                             scaled by cos of the mid latitude) fitted into
 *                             box [x, y, w, h] in design px, north up.
 *                             Returns p([lon,lat]) -> [x,y], plus .k (px per
 *                             degree of latitude) and .mPerPx.
 *   AKPORT.ringPath(cx, ring, p)  adds one lon/lat ring as a subpath; never
 *                             calls beginPath (SKILL.md, the evenodd rule).
 *   AKPORT.places             named points used as locators, lon/lat.
 *   AKPORT.fixtures(no, total, o)  wordmark, counter, site watermark.
 *
 * HONESTY. The parcels are drawn from their legal descriptions. Quarter-
 * quarter edges BLM does not publish as polygons are split from their parent
 * aliquot, so they are approximate to a few metres. Nothing in this file
 * draws a building, a plant or a data center on the land: none is designed
 * in public, and the developer's plan is confidential.
 */
(function (global) {
  "use strict";
  const AKPORT = {};

  AKPORT.loadLand = async function (assets) {
    const g = await (await fetch(assets + '/geo/ak-pointmac-t14n-r4w.geo.json')).json();
    const rings = f => (f.geometry.type === 'Polygon' ? [f.geometry.coordinates]
      : f.geometry.coordinates).map(poly => poly[0]);
    const sections = [], parts = [];
    let w = 1e9, e = -1e9, s = 1e9, n = -1e9;
    for (const f of g.features) {
      const rs = rings(f);
      if (f.properties.kind === 'section') {
        sections.push({ label: f.properties.label, rings: rs });
        for (const r of rs) for (const c of r) {
          w = Math.min(w, c[0]); e = Math.max(e, c[0]); s = Math.min(s, c[1]); n = Math.max(n, c[1]);
        }
      } else {
        parts.push({ parcel: f.properties.parcel, part: f.properties.part,
                     acres: f.properties.record_acres, rings: rs });
      }
    }
    const parcels = {};
    for (const p of parts) {
      (parcels[p.parcel] = parcels[p.parcel] || { id: p.parcel, acres: 0, parts: [] });
      parcels[p.parcel].acres += p.acres; parcels[p.parcel].parts.push(p);
    }
    for (const k in parcels) parcels[k].acres = Math.round(parcels[k].acres * 100) / 100;
    const acres = Math.round(parts.reduce((a, p) => a + p.acres, 0) * 100) / 100;
    if (Math.abs(acres - 829.34) > 0.005) throw new Error('AK CONTRACT: akport: parcel record acres sum to ' + acres + ', expected 829.34');
    return { sections, parts, parcels, acres, bounds: { w, e, s, n } };
  };

  AKPORT.projector = function (b, box, pad) {
    pad = pad || 0;
    const lat0 = (b.s + b.n) / 2, kx = Math.cos(lat0 * Math.PI / 180);
    const spanX = (b.e - b.w) * kx, spanY = (b.n - b.s);
    const k = Math.min((box[2] - 2 * pad) / spanX, (box[3] - 2 * pad) / spanY);
    const ox = box[0] + (box[2] - spanX * k) / 2, oy = box[1] + (box[3] - spanY * k) / 2;
    const p = ll => [ox + (ll[0] - b.w) * kx * k, oy + (b.n - ll[1]) * k];
    p.inv = xy => [b.w + (xy[0] - ox) / (kx * k), b.n - (xy[1] - oy) / k];
    p.k = k; p.kx = kx; p.mPerPx = 110574 / k;
    return p;
  };

  AKPORT.ringPath = function (cx, ring, p) {
    ring.forEach((c, i) => { const q = p(c); i ? cx.lineTo(q[0], q[1]) : cx.moveTo(q[0], q[1]); });
    cx.closePath();
  };

  // Locators. Port MacKenzie's deep-water dock and the Anchorage port are
  // public facilities with well-known positions; the plant has no published
  // site beyond "near Skwentna" and is never drawn as a point.
  AKPORT.places = {
    portMacKenzie: [-149.913, 61.268],
    anchorage: [-149.9003, 61.2181],
    portOfAlaska: [-149.882, 61.237],
    skwentna: [-151.18, 61.965],
  };

  AKPORT.fixtures = function (no, total, o) {
    o = o || {};
    const ink = o.ink || '#C9D3D8', dim = o.dim || '#64737B', accent = o.accent || '#FFC72C';
    const disp = o.wordmarkFont || "500 26px 'Space Grotesk'";
    const root = document.createElement('div');
    root.className = 'akport-fixtures';
    root.innerHTML = (o.wordmark === false ? '' :
      '<div class="akport-wordmark" style="position:absolute;right:80px;top:80px;font:' + disp + ';letter-spacing:0.08em;color:' + ink + '">ALASKA.AI</div>') +
      '<div class="akport-counter" style="position:absolute;right:80px;top:1236px;font:500 24px \'JetBrains Mono\';letter-spacing:0.08em;color:' + ink + ';font-variant-numeric:tabular-nums"><span style="color:' + accent + '">' +
      String(no).padStart(2, '0') + '</span> / ' + String(total).padStart(2, '0') + '</div>' +
      '<div data-decorative class="akport-site" style="position:absolute;left:80px;top:1296px;font:400 19px \'JetBrains Mono\';letter-spacing:0.06em;color:' + dim + '">alaskaaihq.com' +
      (o.coords ? '&nbsp;&nbsp;&nbsp;' + o.coords : '') + '</div>';
    document.body.appendChild(root);
    return root;
  };

  global.AKPORT = AKPORT;
})(typeof window !== 'undefined' ? window : globalThis);
