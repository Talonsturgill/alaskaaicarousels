#!/usr/bin/env python3
"""Emit the nine bespoke slides for Alaska.Ai No.29 (2026-08-08).

A build script is not a template. Every slide below carries its OWN drawing
code and its OWN composition; the only thing shared across 01, 05 and 06 is the
world function `scene(p)`, which is the deck's whole argument (same object, same
camera, different light). bespoke_check measures the outcome and is run after.
"""
import pathlib

OUT = pathlib.Path("out/2026-08-08/slides")
OUT.mkdir(parents=True, exist_ok=True)

SCENE = open("/tmp/claude-0/-home-user-alaskaaicarousels/"
             "cc990278-905f-50ef-bbab-33b7654353ab/scratchpad/scene.js").read()

HEAD = """<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
html,body{{margin:0;padding:0;width:1080px;height:1350px;overflow:hidden;background:#04080D}}
#art{{position:absolute;left:0;top:0;width:1080px;height:1350px}}
.lyr{{position:absolute;left:0;top:0;width:1080px;height:1350px}}
.kick{{font-family:Archivo;font-variation-settings:'wdth' 62,'wght' 600;
  font-size:26px;letter-spacing:.11em;text-transform:uppercase;color:#8FA36A}}
.hl{{font-family:'Instrument Serif';font-weight:400;color:#F4F8FF;
  line-height:1.0;letter-spacing:-.02em}}
.it{{font-family:'Instrument Serif';font-style:italic;color:#A9BFA0}}
.bd{{font-family:Archivo;font-variation-settings:'wdth' 100,'wght' 400;
  font-size:34px;line-height:1.38;color:#D8E4DE}}
.mn{{font-family:'JetBrains Mono';font-weight:400;font-size:20px;
  letter-spacing:.08em;color:#8FA36A;font-variant-numeric:tabular-nums lining-nums}}
.log{{position:absolute;left:80px;bottom:44px}}
.ctr{{position:absolute;right:80px;top:64px;color:#C9D6CE}}
.crd{{position:absolute;left:80px;bottom:16px;font-size:18px;color:#3E5248}}
.gold{{color:#FFC72C}}
</style>
<canvas id="art" width="2160" height="2700"></canvas>
"""

FOOT = """
<script>
window.renderReady = new Promise(function(res){{
  (async function(){{
    await document.fonts.ready;
    draw();
    if (window.__fit) window.__fit();
    res();
  }})();
}});
</script>
"""


def slide(n, body_html, script, extra_body_attr=""):
    p = OUT / f"slide-{n:02d}.html"
    p.write_text(HEAD.format() + f"<body{extra_body_attr}>\n" + body_html +
                 "\n<script src=\"@@ASSETS@@/js/noise.js\"></script>"
                 "\n<script src=\"@@ASSETS@@/js/aktype.js\"></script>"
                 "\n<script src=\"@@ASSETS@@/js/aksdf.js\"></script>"
                 "\n<script src=\"@@ASSETS@@/js/akpost.js\"></script>\n"
                 "<script>\n" + script + "\n</script>\n" + FOOT.format())
    return p


# ---------------------------------------------------------------- shared bits
def log_line(n, fov, key, dolly):
    return (f'<div class="mn log">SHOT {n:02d} / 09 . FOV {fov} . '
            f'KEY {key} . DOLLY {dolly}</div>')


COUNTER = '<div class="mn ctr">{n:02d} / 09</div>'
COORDS = ('<div class="mn crd" data-decorative>56&#176;51\'N 135&#176;10\'W</div>')

# The 2D atmosphere every slide lays down first, then AKPOST.grade, THEN any
# raymarch composite. Grading after a GL/SDF composite costs ~34s (instinct).
ATMOS = """
function atmos(cx, seed, fogTop, fogBot, dz){
  var g = cx.createLinearGradient(0,0,0,1350);
  g.addColorStop(0, fogTop); g.addColorStop(0.62, fogBot); g.addColorStop(1, '#04080D');
  cx.fillStyle = g; cx.fillRect(0,0,1080,1350);
  var r = AK.rng(seed);
  for (var i=0;i<220;i++){                 // silt motes, near field
    var x = r()*1080, y = 200 + r()*1150, s = 0.5 + r()*1.9;
    cx.globalAlpha = 0.05 + r()*0.10;
    cx.fillStyle = '#8FA36A';
    cx.beginPath(); cx.arc(x,y,s,0,6.2832); cx.fill();
  }
  cx.globalAlpha = 1;
}
function grain(cx, seed){
  var t = document.createElement('canvas'); t.width = 96; t.height = 96;
  var tc = t.getContext('2d'), id = tc.createImageData(96,96), r = AK.rng(seed);
  for (var i=0;i<96*96;i++){
    var v = 118 + (r()*74 - 37);
    id.data[i*4]=v; id.data[i*4+1]=v; id.data[i*4+2]=v; id.data[i*4+3]=17;
  }
  tc.putImageData(id,0,0);
  var pat = cx.createPattern(t,'repeat');
  cx.globalCompositeOperation = 'overlay';
  cx.fillStyle = pat; cx.fillRect(0,0,1080,1350);
  cx.globalCompositeOperation = 'source-over';
}
function shafts(cx, n, alpha, ox, oy, spread, seed){
  var r = AK.rng(seed);
  cx.save(); cx.globalCompositeOperation = 'screen';
  for (var i=0;i<n;i++){
    var a = -1.9 + (i/(n-1||1))*spread + (r()-0.5)*0.05;
    var w = 26 + r()*40, L = 900 + r()*420;
    cx.save(); cx.translate(ox,oy); cx.rotate(a);
    var g = cx.createLinearGradient(0,0,0,-L);
    g.addColorStop(0,'rgba(192,138,62,'+alpha+')');
    g.addColorStop(1,'rgba(192,138,62,0)');
    cx.fillStyle = g;
    cx.beginPath(); cx.moveTo(-w*0.30,0); cx.lineTo(w*0.30,0);
    cx.lineTo(w*1.5,-L); cx.lineTo(-w*1.5,-L); cx.closePath(); cx.fill();
    cx.restore();
  }
  cx.restore();
}
"""

# The one light rig the whole deck shares, expressed for the raymarcher.
RAY = """
function rayFrame(cx, opts){
  var r = AKSDF.render(cx, {
    scene: scene, width: opts.w, height: opts.h, box:[0,0,1080,1350],
    cam: opts.cam, light: [-0.34,0.86,0.38],
    mats: {
      1:{color:[0.013*opts.g,0.022*opts.g,0.019*opts.g], spec:0.05},
      2:{color:[0.17*opts.g,0.18*opts.g,0.172*opts.g], spec:0.20,
         emissive:[0.085*opts.e,0.079*opts.e,0.064*opts.e]},
      3:{color:[0.02,0.02,0.02], spec:0.0,
         emissive:[2.60*opts.e,2.16*opts.e,1.48*opts.e]},
      4:{color:[0.014*opts.g,0.020*opts.g,0.018*opts.g], spec:0.40},
      5:{color:[0.013*opts.g,0.019*opts.g,0.017*opts.g], spec:0.50},
      6:{color:[0.012*opts.g,0.017*opts.g,0.015*opts.g], spec:0.10}
    },
    sky:[0.006,0.013,0.015], fog:0.135,
    keyColor:[1.00,0.92,0.76], shadowColor:[0.055,0.095,0.085],
    seed: 20260808, deadlineMs: 12000, maxSteps: 96, eps: 0.0015
  });
  window.__akHero = {rung:'aksdf', scene:'redoubt-chute', internal:[opts.w,opts.h],
                     primitives:9, shadows:r.shadows, ao:r.ao,
                     degraded:!(r.shadows && r.ao)};
  return r;
}
function probe(cx, rect){                 // median L* of a region, feed scale
  var d = cx.getImageData(rect[0]*2, rect[1]*2, rect[2]*2, rect[3]*2).data, v=[];
  for (var i=0;i<d.length;i+=16){
    var R=d[i]/255,G=d[i+1]/255,B=d[i+2]/255;
    var Y=0.2126*R+0.7152*G+0.0722*B;
    v.push(Y<=0.008856?903.3*Y:116*Math.pow(Y,1/3)-16);
  }
  v.sort(function(a,b){return a-b;});
  return Math.round(v[Math.floor(v.length/2)]*10)/10;
}
"""

# =============================================================== SLIDE 01
s01_body = f"""
<div class="lyr">
  <div class="kick" style="position:absolute;left:80px;top:120px">REDOUBT LAKE WEIR . SITKA TRIBE OF ALASKA</div>
  <div id="h1" class="hl" style="position:absolute;left:540px;top:190px;width:462px;font-size:132px">"The system<br>is not broken.<br>That's the problem."</div>
  <div class="bd" style="position:absolute;left:540px;top:640px;width:452px;font-size:26px;
       font-variation-settings:'wdth' 62,'wght' 500;letter-spacing:.02em">Jeff Feldpausch, Sitka Tribe of Alaska, to KCAW, August 5, 2026</div>
  {log_line(1,58,'6 TO 1','0.00 M')}
  {COUNTER.format(n=1)}
  {COORDS}
</div>
"""
s01_js = SCENE + ATMOS + RAY + """
function draw(){
  var cx = document.getElementById('art').getContext('2d');
  cx.setTransform(2,0,0,2,0,0);
  atmos(cx, 20260808+1, '#0A1614', '#08110F', 0.16);
  AKPOST.grade(cx, {exposure:1.02, saturation:0.95, contrast:1.06});
  rayFrame(cx, {w:440,h:660,g:1.0,e:1.0,
                cam:{pos:[0.85,0.62,-2.15], look:[-0.16,0.40,0.34], fov:58}});
  shafts(cx, 4, 0.08, 300, 940, 0.55, 20260808+1);
  grain(cx, 20260808+1);
  window.__akProbes = {
    slot_core: probe(cx,[188,612,96,108]),
    wall_shadow: probe(cx,[430,760,90,90]),
    open_water: probe(cx,[760,240,180,180])
  };
}
window.__fit = function(){ AK.fitText(document.getElementById('h1'),{min:104,max:138,maxLines:3}); };
"""
slide(1, s01_body, s01_js,
      ' data-contacts=\'[{"what":"the chute on the lake bed",'
      '"shadow":[[300,980,300,40]],"ground":[[300,1090,300,40]]}]\''
      ' data-encodes=\'[{"claim":"every fish passes one lit gate, one at a time",'
      '"a":[[188,612,96,108]],"b":[[760,240,180,180]]}]\'')

# =============================================================== SLIDE 05
s05_body = f"""
<div class="lyr">
  <div class="kick" style="position:absolute;left:80px;top:120px">THE MONEY THAT EXISTS</div>
  <div id="h5" class="hl" style="position:absolute;left:452px;top:180px;width:548px;font-size:88px"><span class="gold">$200,000</span> paid to install it. Once.</div>
  <div class="bd" style="position:absolute;left:452px;top:520px;width:548px">A fiscal year 2024 Tribal Wildlife Grant from the U.S. Fish and Wildlife Service, titled "Artificial Intelligence for Subsistence Salmon Monitoring and Management". The Service describes the award as paying to install AI enabled video at Redoubt. That page describes installing the system. It describes nothing after that.</div>
  <div class="mn" style="position:absolute;left:452px;top:960px">GOLD MARKS MONEY THAT EXISTS.</div>
  {log_line(5,64,'8 TO 1','7.62 M')}
  {COUNTER.format(n=5)}
  {COORDS}
</div>
"""
s05_js = SCENE + ATMOS + RAY + """
function draw(){
  var cx = document.getElementById('art').getContext('2d');
  cx.setTransform(2,0,0,2,0,0);
  atmos(cx, 20260808+5, '#0C1A17', '#0A1512', 0.12);
  AKPOST.grade(cx, {exposure:1.06, saturation:0.98, contrast:1.05});
  rayFrame(cx, {w:440,h:660,g:1.0,e:1.0,
                cam:{pos:[0.85,0.62,-2.15], look:[-0.02,0.44,0.30], fov:64}});
  shafts(cx, 6, 0.10, 286, 900, 0.72, 20260808+5);
  grain(cx, 20260808+5);
  window.__akProbes = {
    slot_core: probe(cx,[188,612,96,108]),
    wall_shadow: probe(cx,[404,748,90,90]),
    open_water: probe(cx,[96,208,180,180])
  };
}
window.__fit = function(){ AK.fitText(document.getElementById('h5'),{min:64,max:92,maxLines:3}); };
"""
slide(5, s05_body, s05_js,
      ' data-contacts=\'[{"what":"the chute on the lit bed",'
      '"shadow":[[286,960,300,40]],"ground":[[286,1076,300,40]]}]\''
      ' data-encodes=\'[{"claim":"this frame is fully readable",'
      '"a":[[188,612,96,108]],"b":[[96,208,180,180]]}]\'')

# =============================================================== SLIDE 06
s06_body = f"""
<div class="lyr">
  <div class="kick" style="position:absolute;left:80px;top:120px">THE MONEY THAT DOESN'T</div>
  <div id="h6" class="hl" style="position:absolute;left:80px;top:186px;width:920px;font-size:128px">Grant money lights damage.</div>
  <div class="hl" style="position:absolute;left:80px;top:392px;width:820px;font-size:62px">"This system isn't damaged."</div>
  <div class="bd" style="position:absolute;left:80px;top:590px;width:640px">"There's lots of money out there to fix and monitor broken systems"<br><br>"there's no funding for the weir right now"</div>
  <div class="bd" style="position:absolute;left:80px;top:830px;width:640px;font-size:26px;
       font-variation-settings:'wdth' 62,'wght' 500;letter-spacing:.02em">Jeff Feldpausch, Sitka Tribe of Alaska, to KCAW, August 5, 2026</div>
  {log_line(6,64,'1 TO 1','0.00 M')}
  {COUNTER.format(n=6)}
  {COORDS}
</div>
"""
s06_js = SCENE + ATMOS + RAY + """
function draw(){
  var cx = document.getElementById('art').getContext('2d');
  cx.setTransform(2,0,0,2,0,0);
  atmos(cx, 20260808+6, '#0C1A17', '#0A1512', 0.12);
  AKPOST.grade(cx, {exposure:1.06, saturation:0.98, contrast:1.05});
  // IDENTICAL camera, IDENTICAL scene. Only the light rig changes: gain 1.00
  // to 0.16 and the polyethylene emissive to 6 percent. That is the argument.
  rayFrame(cx, {w:480,h:720,g:0.16,e:0.06,
                cam:{pos:[0.85,0.62,-2.15], look:[-0.02,0.44,0.30], fov:64}});
  shafts(cx, 2, 0.02, 286, 900, 0.72, 20260808+6);
  grain(cx, 20260808+6);
  window.__akProbes = {
    slot_core: probe(cx,[188,612,96,108]),
    wall_shadow: probe(cx,[404,748,90,90]),
    open_water: probe(cx,[96,208,180,180])
  };
}
window.__fit = function(){ AK.fitText(document.getElementById('h6'),{min:104,max:132,maxLines:1}); };
"""
slide(6, s06_body, s06_js,
      ' data-contacts=\'[{"what":"the chute on the unlit bed",'
      '"shadow":[[286,960,300,40]],"ground":[[286,1076,300,40]]}]\''
      ' data-encodes=\'[{"claim":"the object is identical and only the light changed",'
      '"a":[[188,612,96,108]],"b":[[96,208,180,180]]}]\'')

print("wrote 01, 05, 06")
