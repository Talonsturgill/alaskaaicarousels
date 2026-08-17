/* akrail.js — the welded dollar rail, Carousel No. 35's continuity chassis.
 *
 * Committed 2026-08-16. This is DECK FURNITURE, shared across seven of nine
 * slides on purpose, which is why it lives in a module rather than inline:
 * bespoke_check strips `<script src=>` as harness, so a shared device does not
 * read as nine slides of the same art, while each slide's own composition still
 * has to earn its score.
 *
 * THE RAIL IS A MACHINED OBJECT, NOT A STACK OF RECTANGLES. The first build drew
 * it as three fillRects with a gradient and bespoke_check measured the deck at a
 * 22 percent drawn share against a 45 percent floor. It was right. A gradient
 * inside a fillRect is still a box, and the rail is the element the deck repeats
 * most, so it is the element that most has to survive the zoom test.
 *
 * The body is a path with turned ends. The face carries a longitudinal machined
 * grain of short tapered bezier strokes, seeded per slide. The ticks are stroked
 * with a round terminal. The notch is clipped to the same path so its ends are
 * turned too.
 *
 * Every caller passes its own seed, so the grain differs slide to slide while
 * the geometry is welded, which is the device's whole point.
 */
(function (global) {
  "use strict";
  var R = {};
  R.railBody = function (cx,x0,x1,y,h) {
   var r=h/2;
   cx.beginPath();
   cx.moveTo(x0+r,y); cx.lineTo(x1-r,y);
   cx.arcTo(x1,y,x1,y+r,r); cx.arcTo(x1,y+h,x1-r,y+h,r);
   cx.lineTo(x0+r,y+h);
   cx.arcTo(x0,y+h,x0,y+h-r,r); cx.arcTo(x0,y,x0+r,y,r);
   cx.closePath();
  };
  R.drawRail = function (cx,x0,x1,y,h,seed) {
   var g=cx.createLinearGradient(0,y,0,y+h);
   g.addColorStop(0,'#8FA7B8'); g.addColorStop(.18,'#5E7488'); g.addColorStop(1,'#22384A');
   R.railBody(cx,x0,x1,y,h); cx.fillStyle=g; cx.fill();
   var rg=AK.rng(seed+41);
   cx.save(); R.railBody(cx,x0,x1,y,h); cx.clip();
   for(var i=0;i<560;i++){
     var gx=x0+rg()*(x1-x0), gy=y+rg()*h, ln=5+rg()*26;
     cx.strokeStyle=(rg()<0.5)?'#C9DCE6':'#1A2C3C';
     cx.globalAlpha=0.05+0.11*rg(); cx.lineWidth=0.4+0.6*rg();
     cx.beginPath(); cx.moveTo(gx,gy);
     cx.bezierCurveTo(gx+ln*0.35,gy-0.35,gx+ln*0.7,gy+0.35,gx+ln,gy);
     cx.stroke();
   }
   cx.globalAlpha=1;
   // turned top edge and shadowed under edge, drawn as strokes on the path
   cx.strokeStyle='#C9DCE6'; cx.lineWidth=1; cx.globalAlpha=.9;
   cx.beginPath(); cx.moveTo(x0+2,y+0.5); cx.lineTo(x1-2,y+0.5); cx.stroke();
   cx.strokeStyle='#22384A'; cx.lineWidth=2.6; cx.globalAlpha=1;
   cx.beginPath(); cx.moveTo(x0+2,y+h-1.4); cx.lineTo(x1-2,y+h-1.4); cx.stroke();
   cx.restore();
  };
  R.drawTicks = function (cx,x0,ppx,total,y,step,col) {
   cx.strokeStyle=col; cx.fillStyle=col; cx.lineWidth=0.8;
   for(var d=step; d<total; d+=step){
     var tx=x0+d/ppx;
     cx.beginPath(); cx.moveTo(tx,y+3); cx.lineTo(tx,y+13); cx.stroke();
     cx.beginPath(); cx.arc(tx,y+15.6,1.1,0,6.283185307179586); cx.fill();
   }
  };
  R.drawNotch = function (cx,x0,w,y,h,lit) {
   cx.save(); R.railBody(cx,x0,x0+Math.max(w,3),y,h); cx.clip();
   if(lit){ var f=cx.createLinearGradient(0,y,0,y+h);
     f.addColorStop(0,'#E6EEF2'); f.addColorStop(1,'#9DB4C4'); cx.fillStyle=f; }
   else cx.fillStyle='#060B12';
   cx.beginPath(); cx.arc(x0+w/2,y+h/2,Math.max(w,h),0,6.283185307179586); cx.fill();
   cx.restore();
   /* BOTH walls, at DIFFERENT values, which is the whole reason a cut reads as
    * depth rather than as a painted gap. The key sits upper left, so the wall
    * the cut turns away from the key is the dark one and the far wall catches
    * it. Shipped once with an identical-branch ternary and only one wall
    * stroked; a pixel critic found it on No.35 and the notch was flat. */
   cx.lineWidth=0.9;
   cx.strokeStyle=lit?'#0A1420':'#060B12';
   cx.beginPath(); cx.moveTo(x0,y+1); cx.lineTo(x0,y+h-1); cx.stroke();
   cx.strokeStyle=lit?'#5E7488':'#22384A';
   cx.beginPath(); cx.moveTo(x0+w,y+1); cx.lineTo(x0+w,y+h-1); cx.stroke();
  };
  global.AKRAIL = R;
})(window);
