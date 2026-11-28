/* akinterval.js — house furniture for No.126, TWO TO SIXTEEN (2026-11-27).
 *
 * The deck's continuity motif is THE INTERVAL RAIL: a graduated rail cut into a
 * dark trough at the foot of every frame, whose state changes with the story.
 * This file draws only that rail and the fixed frame furniture (kicker,
 * counter, site watermark, grain). Every slide's art is its own code; nothing
 * here draws a picture.
 *
 * GEOMETRY. The trough spans x 108 to 964, y 1190 to 1232. Inside it:
 *   - the BRACKET strip, y 1197 to 1211, where a raised lit bar shows a span;
 *   - the TICK strip, y 1214 to 1228, where every tick and notch is drawn.
 * Only the tick strip is a measured band (`data-scale` band [1214, 1228]),
 * so a bracket's long body never reads as an undeclared mark (qa.py census).
 * Labels are DOM, set by the slide, under the trough at y >= 1236.
 *
 * USAGE
 *   IV.frame({ n: 3, kicker: 'THE DEN MODEL' });     // DOM furniture
 *   IV.rail(cx, { x0: 120, x1: 952, v0: 0, v1: 16,
 *                 ticks: [0, 2, 4, ...], bracket: [2, 16], notch: 8,
 *                 dashedFrom: 8, gold: '#FFC72C' });
 *   IV.x(spec, v) -> design px of value v
 */
(function (global) {
  'use strict';
  const IV = {};
  const TROUGH = { x: 108, y: 1190, w: 856, h: 42 };
  IV.TROUGH = TROUGH;
  IV.BAND = [1214, 1228];
  IV.BRACKET = [1197, 1211];

  IV.x = function (s, v) { return s.x0 + (v - s.v0) * (s.x1 - s.x0) / (s.v1 - s.v0); };

  function rr(cx, x, y, w, h, r) {
    r = Math.min(r, h / 2, w / 2);
    cx.moveTo(x + r, y);
    cx.arcTo(x + w, y, x + w, y + h, r);
    cx.arcTo(x + w, y + h, x, y + h, r);
    cx.arcTo(x, y + h, x, y, r);
    cx.arcTo(x, y, x + w, y, r);
    cx.closePath();
  }
  IV.roundRect = rr;

  /* The trough: a carved channel, lit on its lower lip (light from the upper
   * left falls on the far wall of a cut, which is its lower edge on screen),
   * dark on its upper wall. Painted as a stroked lip and a graded fill, never
   * a flat plate. */
  IV.trough = function (cx, o) {
    o = o || {};
    const t = TROUGH;
    cx.save();
    const g = cx.createLinearGradient(0, t.y, 0, t.y + t.h);
    g.addColorStop(0, o.top || '#02050B');
    g.addColorStop(0.55, o.mid || '#07111B');
    g.addColorStop(1, o.bottom || '#0C1A26');
    cx.beginPath(); rr(cx, t.x, t.y, t.w, t.h, 10);
    cx.fillStyle = g; cx.fill();
    // lit lower lip
    cx.beginPath();
    cx.moveTo(t.x + 10, t.y + t.h - 0.8); cx.lineTo(t.x + t.w - 10, t.y + t.h - 0.8);
    cx.strokeStyle = o.lip || 'rgba(191,216,212,0.30)'; cx.lineWidth = 1.4; cx.stroke();
    // shadowed upper wall
    cx.beginPath();
    cx.moveTo(t.x + 10, t.y + 1.2); cx.lineTo(t.x + t.w - 10, t.y + 1.2);
    cx.strokeStyle = 'rgba(0,0,0,0.55)'; cx.lineWidth = 2.2; cx.stroke();
    cx.restore();
  };

  /* The rail itself. Returns the list of drawn tick/notch positions so a slide
   * can cross-check its own `data-scale` literal against what drew. */
  IV.rail = function (cx, s) {
    IV.trough(cx, s.trough);
    const drawn = [];
    const [b0, b1] = IV.BAND;
    cx.save();
    cx.lineCap = 'butt';
    // bracket: a raised lit bar with rounded ends, its upper half lit
    if (s.bracket) {
      const xa = IV.x(s, s.bracket[0]), xb = IV.x(s, s.bracket[1]);
      const y = IV.BRACKET[0], h = IV.BRACKET[1] - IV.BRACKET[0];
      const solidEnd = s.dashedFrom != null ? IV.x(s, s.dashedFrom) : xb;
      const g = cx.createLinearGradient(0, y, 0, y + h);
      g.addColorStop(0, s.lit || '#EAF5F2');
      g.addColorStop(0.5, s.mid || '#BFD8D4');
      g.addColorStop(1, s.lee || '#4A6B78');
      cx.beginPath(); rr(cx, xa, y, solidEnd - xa, h, h / 2);
      cx.fillStyle = g; cx.fill();
      if (s.dashedFrom != null) {
        cx.setLineDash([7, 4]); cx.lineWidth = 1.6;
        cx.strokeStyle = s.mid || '#BFD8D4';
        cx.beginPath(); rr(cx, solidEnd, y + 1, xb - solidEnd, h - 2, (h - 2) / 2);
        cx.stroke(); cx.setLineDash([]);
      }
    }
    // ticks
    (s.ticks || []).forEach(v => {
      const x = Math.round(IV.x(s, v)) + 0.5;
      cx.beginPath(); cx.moveTo(x, b0); cx.lineTo(x, b1);
      cx.strokeStyle = s.tickColor || 'rgba(191,216,212,0.78)';
      cx.lineWidth = 1.6; cx.stroke();
      drawn.push(IV.x(s, v));
    });
    // gold notch: a short wedge standing in the tick strip
    (s.notch != null ? [].concat(s.notch) : []).forEach(v => {
      const x = IV.x(s, v);
      cx.beginPath();
      cx.moveTo(x - 6, b0); cx.lineTo(x + 6, b0); cx.lineTo(x + 1.5, b1); cx.lineTo(x - 1.5, b1);
      cx.closePath(); cx.fillStyle = s.gold || '#FFC72C'; cx.fill();
      drawn.push(x);
    });
    // gold sliver (a span drawn in gold inside the tick strip)
    if (s.sliver) {
      const xa = IV.x(s, s.sliver[0]), xb = IV.x(s, s.sliver[1]);
      cx.fillStyle = s.gold || '#FFC72C';
      cx.fillRect(xa, b0, Math.max(2, xb - xa), b1 - b0);
      drawn.push((xa + xb) / 2);
    }
    // free marks: [{at: px, color, w}] for rails that are not numeric
    (s.marks || []).forEach(m => {
      cx.beginPath(); cx.moveTo(m.at, b0); cx.lineTo(m.at, b1);
      cx.strokeStyle = m.color; cx.lineWidth = m.w || 3; cx.stroke();
      drawn.push(m.at);
    });
    cx.restore();
    return drawn;
  };

  /* Frame furniture in the DOM: kicker, counter, site watermark, grain. */
  IV.frame = function (o) {
    const d = document;
    if (!d.getElementById('iv-style')) {
      const st = d.createElement('style'); st.id = 'iv-style';
      st.textContent =
        '.iv-kicker{position:absolute;left:80px;top:80px;font-family:"JetBrains Mono",monospace;' +
        'font-weight:500;font-size:24px;letter-spacing:.07em;color:#9FB4B8;text-transform:uppercase;z-index:5}' +
        '.iv-counter{position:absolute;right:80px;top:80px;font-family:"JetBrains Mono",monospace;' +
        'font-weight:500;font-size:24px;letter-spacing:.07em;color:#9FB4B8;font-variant-numeric:tabular-nums;z-index:5}' +
        '.iv-site{position:absolute;left:80px;top:1288px;font-family:"JetBrains Mono",monospace;' +
        'font-size:20px;letter-spacing:.06em;color:#46545F;z-index:5}' +
        '.iv-grain{position:absolute;inset:0;mix-blend-mode:overlay;opacity:.07;pointer-events:none;z-index:4}' +
        '.iv-lab{position:absolute;top:1238px;font-family:"JetBrains Mono",monospace;font-weight:500;' +
        'font-size:24px;letter-spacing:.04em;color:#9FB4B8;transform:translateX(-50%);white-space:nowrap;z-index:5}' +
        '.iv-lab.gold{color:#FFC72C}';
      d.head.appendChild(st);
    }
    const add = (cls, txt, attrs) => {
      const el = d.createElement('div'); el.className = cls;
      if (txt != null) el.textContent = txt;
      Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
      d.body.appendChild(el); return el;
    };
    if (o.kicker) add('iv-kicker', o.kicker);
    add('iv-counter', 'ALASKA.AI ' + String(o.n).padStart(2, '0') + ' / 09');
    add('iv-site', 'alaskaaihq.com', { 'data-decorative': '' });
    const gr = add('iv-grain', null, { 'data-decorative': '' });
    if (global.AK && AK.grainOn) AK.grainOn(gr, { size: 280, strength: 44, seed: 2611270 + o.n });
    return true;
  };

  global.IV = IV;
})(window);
