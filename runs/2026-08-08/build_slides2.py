#!/usr/bin/env python3
"""Slides 02, 03, 04, 07, 08, 09 for No.29. Each carries its own drawing code."""
import pathlib
OUT = pathlib.Path("out/2026-08-08/slides"); OUT.mkdir(parents=True, exist_ok=True)

HEAD = """<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>
html,body{margin:0;padding:0;width:1080px;height:1350px;overflow:hidden;background:#04080D}
#art{position:absolute;left:0;top:0;width:1080px;height:1350px}
.lyr{position:absolute;left:0;top:0;width:1080px;height:1350px}
.kick{font-family:Archivo;font-variation-settings:'wdth' 62,'wght' 600;
 font-size:26px;letter-spacing:.11em;text-transform:uppercase;color:#8FA36A}
.hl{font-family:'Instrument Serif';font-weight:400;color:#F4F8FF;line-height:1.0;letter-spacing:-.02em}
.it{font-family:'Instrument Serif';font-style:italic;color:#A9BFA0}
.bd{font-family:Archivo;font-variation-settings:'wdth' 100,'wght' 400;
 font-size:34px;line-height:1.38;color:#D8E4DE}
.inst{font-family:Archivo;font-variation-settings:'wdth' 62,'wght' 500;
 font-size:26px;letter-spacing:.02em;color:#D8E4DE}
.mn{font-family:'JetBrains Mono';font-weight:400;font-size:20px;letter-spacing:.08em;
 color:#8FA36A;font-variant-numeric:tabular-nums lining-nums}
.log{position:absolute;left:80px;bottom:44px}
.ctr{position:absolute;right:80px;top:64px;color:#C9D6CE}
.crd{position:absolute;left:80px;bottom:16px;font-size:18px;color:#3E5248}
.gold{color:#FFC72C}
</style>
<canvas id="art" width="2160" height="2700"></canvas>
"""
TAIL = """
<script src="@@ASSETS@@/js/noise.js"></script>
<script src="@@ASSETS@@/js/aktype.js"></script>
<script src="@@ASSETS@@/js/akpost.js"></script>
<script>
%s
window.renderReady = new Promise(function(res){
  (async function(){ await document.fonts.ready; draw();
    if (window.__fit) window.__fit(); res(); })();
});
</script>
"""

COMMON = """
function px(cx){ cx.setTransform(2,0,0,2,0,0); }
function vgrad(cx,stops){ var g=cx.createLinearGradient(0,0,0,1350);
  for(var i=0;i<stops.length;i++) g.addColorStop(stops[i][0],stops[i][1]);
  cx.fillStyle=g; cx.fillRect(0,0,1080,1350); }
function motes(cx,seed,n,alo,ahi){ var r=AK.rng(seed);
  for(var i=0;i<n;i++){ var x=r()*1080,y=r()*1350,s=0.5+r()*2.0;
    cx.globalAlpha=alo+r()*(ahi-alo); cx.fillStyle='#8FA36A';
    cx.beginPath(); cx.arc(x,y,s,0,6.2832); cx.fill(); } cx.globalAlpha=1; }
function caustic(cx,seed,x0,y0,w,h,alpha,scale){
  AK.reseed(seed); cx.save(); cx.beginPath(); cx.rect(x0,y0,w,h); cx.clip();
  cx.globalCompositeOperation='screen';
  for(var y=y0;y<y0+h;y+=3){ for(var x=x0;x<x0+w;x+=3){
      var v=AK.fbm2(x/scale,y/scale,3);
      if(v>0.30){ cx.fillStyle='rgba(192,138,62,'+(alpha*(v-0.30)*2.2).toFixed(3)+')';
        cx.fillRect(x,y,3,3); } } }
  cx.restore(); }
function grain(cx,seed){ var t=document.createElement('canvas'); t.width=96;t.height=96;
  var tc=t.getContext('2d'), id=tc.createImageData(96,96), r=AK.rng(seed);
  for(var i=0;i<96*96;i++){ var v=118+(r()*74-37);
    id.data[i*4]=v;id.data[i*4+1]=v;id.data[i*4+2]=v;id.data[i*4+3]=17; }
  tc.putImageData(id,0,0);
  cx.globalCompositeOperation='overlay'; cx.fillStyle=cx.createPattern(t,'repeat');
  cx.fillRect(0,0,1080,1350); cx.globalCompositeOperation='source-over'; }
/* two-part contact shadow cast onto a ground that is LIT first */
function litPool(cx,x,y,rx,ry,c0,c1){ var g=cx.createRadialGradient(x,y,0,x,y,rx);
  g.addColorStop(0,c0); g.addColorStop(1,c1);
  cx.save(); cx.translate(x,y); cx.scale(1,ry/rx); cx.fillStyle=g;
  cx.beginPath(); cx.arc(0,0,rx,0,6.2832); cx.fill(); cx.restore(); }
function contact(cx,x,y,w,h){
  var g=cx.createLinearGradient(0,y,0,y+h*3.4);
  g.addColorStop(0,'rgba(6,14,12,0.86)'); g.addColorStop(1,'rgba(6,14,12,0)');
  cx.fillStyle=g; cx.beginPath();
  cx.ellipse(x,y+h*0.5,w*0.66,h*1.5,0,0,6.2832); cx.fill();
  cx.fillStyle='rgba(4,10,9,0.92)';
  cx.beginPath(); cx.ellipse(x,y,w*0.46,h*0.34,0,0,6.2832); cx.fill(); }
"""


def write(n, body, js, attr=""):
    (OUT / f"slide-{n:02d}.html").write_text(
        HEAD + f"<body{attr}>\n" + body + (TAIL % (COMMON + js)))


def fx(n, fov, key, dolly):
    return (f'<div class="mn log">SHOT {n:02d} / 09 . FOV {fov} . KEY {key} . '
            f'DOLLY {dolly}</div>\n<div class="mn ctr">{n:02d} / 09</div>\n'
            f'<div class="mn crd" data-decorative>56&#176;51\'N 135&#176;10\'W</div>')


# ============================================================ 02 THE INSTRUMENT
write(2, f"""<div class="lyr">
<div class="kick" style="position:absolute;left:80px;top:120px">THE INSTRUMENT</div>
<div id="h" class="hl" style="position:absolute;left:80px;top:180px;width:900px;font-size:84px">One camera. One chute.<br>One fish at a time.</div>
<div class="bd" style="position:absolute;left:80px;top:404px;width:600px">KCAW describes a white polyethylene plastic chute with a video camera on the side. A float in the lagoon carries battery packs, solar panels and a Starlink system. The data reaches the Tribe's office in Sitka immediately.</div>
<div class="mn" style="position:absolute;left:80px;top:700px;width:600px;line-height:1.5">SALMON VISION . A COLLABORATIVE EFFORT<br>OF FOUR ORGANISATIONS (C17)</div>
{fx(2,68,'5 TO 1','2.22 M')}</div>""", """
function draw(){
  var cx=document.getElementById('art').getContext('2d'); px(cx);
  vgrad(cx,[[0,'#0A1614'],[0.55,'#08110F'],[1,'#04080D']]);
  motes(cx,20260808+2,190,0.04,0.13);
  AKPOST.grade(cx,{exposure:1.02,saturation:0.95,contrast:1.06});
  // lit bed pool the chute sits in, then the flank, then the shadow into it
  litPool(cx,470,1130,520,150,'rgba(46,66,44,0.55)','rgba(46,66,44,0)');
  caustic(cx,20260808+2,0,980,1080,370,0.16,52);
  // the chute flank driving out of the bottom right corner, 3/4 view
  var A=[218,946],B=[1080,1128],C=[1080,1350],D=[196,1148];
  var g=cx.createLinearGradient(218,946,1080,1200);
  g.addColorStop(0,'#3A4438'); g.addColorStop(0.45,'#242C24'); g.addColorStop(1,'#121A16');
  cx.fillStyle=g; cx.beginPath(); cx.moveTo(A[0],A[1]); cx.lineTo(B[0],B[1]);
  cx.lineTo(C[0],C[1]); cx.lineTo(D[0],D[1]); cx.closePath(); cx.fill();
  // top face, catching the key
  var g2=cx.createLinearGradient(196,880,1080,1060);
  g2.addColorStop(0,'#8E9A86'); g2.addColorStop(1,'#3E4A3C');
  cx.fillStyle=g2; cx.beginPath(); cx.moveTo(196,894); cx.lineTo(1080,1042);
  cx.lineTo(1080,1128); cx.lineTo(218,946); cx.closePath(); cx.fill();
  // ribbed stiffeners down the flank, line-weight hierarchy
  AK.reseed(20260808+2);
  for(var i=0;i<16;i++){ var t=i/15, x=218+t*862, y=946+t*182;
    cx.strokeStyle='rgba(10,18,15,'+(0.30+0.24*Math.abs(Math.sin(i))).toFixed(2)+')';
    cx.lineWidth=(i%4===0)?3:1.25;
    cx.beginPath(); cx.moveTo(x,y); cx.lineTo(x-16,y+198); cx.stroke(); }
  // the counting camera housing on the wall, with its own contact shadow
  contact(cx,392,1006,120,20);
  var hg=cx.createLinearGradient(330,930,430,1000);
  hg.addColorStop(0,'#4E5A4A'); hg.addColorStop(1,'#161E18');
  cx.fillStyle=hg; cx.beginPath();
  cx.ellipse(380,966,54,30,-0.19,0,6.2832); cx.fill();
  cx.fillStyle='#0C1210'; cx.beginPath(); cx.ellipse(380,966,20,13,-0.19,0,6.2832); cx.fill();
  cx.fillStyle='rgba(255,227,174,0.55)'; cx.beginPath();
  cx.ellipse(372,960,6,4,-0.19,0,6.2832); cx.fill();
  // the float above, on the surface, with the uplink dashed to it
  cx.fillStyle='#0C1210'; cx.fillRect(742,300,190,26);
  cx.fillStyle='#1C2620'; cx.fillRect(742,326,190,10);
  cx.fillStyle='#2E3A2C';
  cx.beginPath(); cx.moveTo(788,300); cx.lineTo(824,262); cx.lineTo(866,262);
  cx.lineTo(842,300); cx.closePath(); cx.fill();
  cx.setLineDash([9,7]); cx.strokeStyle='rgba(110,165,255,0.55)'; cx.lineWidth=2;
  cx.beginPath(); cx.moveTo(838,336); cx.lineTo(760,700); cx.lineTo(430,940); cx.stroke();
  cx.setLineDash([]);
  // the fish tail from slide 01, now sharp, entering at the right edge
  cx.fillStyle='#0C1210'; cx.beginPath();
  cx.moveTo(1080,830); cx.quadraticCurveTo(1006,858,962,846);
  cx.quadraticCurveTo(1000,884,1080,900); cx.closePath(); cx.fill();
  grain(cx,20260808+2);
  window.__akLeaders=[{target:'the counting camera housing',at:[380,966],to:[380,966]}];
}
window.__fit=function(){ AK.fitText(document.getElementById('h'),{min:62,max:88,maxLines:2}); };
""", ' data-contacts=\'[{"what":"the camera housing on the chute wall",'
     '"shadow":[[332,996,120,20]],"ground":[[332,1064,120,20]]}]\'')

# ================================================= 03 THE RATIONING INSTRUMENT
iso = []
for i in range(100):
    r, c = divmod(i, 10)
    iso.append((r, c))
write(3, f"""<div class="lyr">
<div class="kick" style="position:absolute;left:80px;top:120px">WHAT THE COUNT DECIDES</div>
<div id="h" class="hl" style="position:absolute;left:80px;top:180px;width:520px;font-size:84px">This number sets a household's legal limit.</div>
<div class="bd" style="position:absolute;left:80px;top:474px;width:500px">Alaska Department of Fish and Game raised the Redoubt annual subsistence limit to 100 sockeye per household, effective 12{'&#58;'}01 a.m. on July 1st, 2026. Feldpausch told KCAW the limit was 50 before.</div>
<div class="mn" style="position:absolute;left:80px;top:754px">ANNUAL LIMIT (C6)</div>
<div class="mn" style="position:absolute;left:80px;top:820px;width:470px;line-height:1.5">ABOUT 35 PERCENT OF ALL SUBSISTENCE SOCKEYE HARVEST IN SOUTHEAST ALASKA HAPPENS HERE, ON UNPUBLISHED FOREST SERVICE AND FISH AND GAME DATA (C33)</div>
<div class="mn" style="position:absolute;left:610px;top:1206px">50 BEFORE . 100 NOW (C24)</div>
{fx(3,44,'7 TO 1','3.53 M')}</div>""", """
function draw(){
  var cx=document.getElementById('art').getContext('2d'); px(cx);
  vgrad(cx,[[0,'#08120F'],[0.5,'#0A1614'],[1,'#050B0A']]);
  AKPOST.grade(cx,{exposure:1.04,saturation:0.96,contrast:1.07});
  // one-point tunnel: the machine's own optical axis. Far mouth 275x328 at centre.
  var cxs=540, cys=675, hw=137.6, hh=164;
  var near=[[-980,-1180],[2060,-1180],[2060,2530],[-980,2530]];
  for(var s=14;s>=1;s--){
    var t=s/14, w=hw+(980-hw)*t*t, h=hh+(1180-hh)*t*t;
    var v=0.055+0.10*(1-t);
    cx.fillStyle='rgb('+Math.round(v*255*0.62)+','+Math.round(v*255*0.86)+','+Math.round(v*255*0.72)+')';
    cx.beginPath(); cx.rect(cxs-w,cys-h,w*2,h*2); cx.fill();
    cx.strokeStyle='rgba(8,16,13,0.55)'; cx.lineWidth=(s%3===0)?2.5:1;
    cx.stroke();
  }
  // the lit far aperture, the only pure light in the frame
  var ag=cx.createRadialGradient(cxs,cys,10,cxs,cys,190);
  ag.addColorStop(0,'#F8FBF6'); ag.addColorStop(0.55,'#FFE3AE'); ag.addColorStop(1,'rgba(255,227,174,0)');
  cx.fillStyle=ag; cx.fillRect(cxs-260,cys-300,520,600);
  cx.fillStyle='#F4F8FF'; cx.fillRect(cxs-hw,cys-hh,hw*2,hh*2);
  // caustic mottling on the receding floor, and the floor grade
  caustic(cx,20260808+3,0,900,1080,450,0.13,46);
  // one fish crossing left of centre, silhouette, with a belly shadow on the floor
  cx.save(); cx.translate(452,742); cx.rotate(0.06);
  cx.fillStyle='rgba(6,12,10,0.55)';
  cx.beginPath(); cx.ellipse(6,196,190,26,0,0,6.2832); cx.fill();
  cx.fillStyle='#0C1210'; cx.beginPath();
  cx.moveTo(-300,0); cx.quadraticCurveTo(-150,-64,90,-46);
  cx.quadraticCurveTo(250,-30,318,0); cx.quadraticCurveTo(250,32,90,48);
  cx.quadraticCurveTo(-150,66,-300,0); cx.closePath(); cx.fill();
  cx.beginPath(); cx.moveTo(-300,0); cx.lineTo(-386,-62); cx.lineTo(-364,0);
  cx.lineTo(-386,62); cx.closePath(); cx.fill();
  cx.restore();
  // ISOTYPE: 100 same-size sockeye, 50 snow + 50 sockeye red, on a lit shelf
  var ox=610, oy=880, cw=46, ch=34;
  litPool(cx,832,1196,290,66,'rgba(52,72,48,0.60)','rgba(52,72,48,0)');
  cx.fillStyle='#141E1A'; cx.fillRect(600,1178,470,10);
  for(var i=0;i<100;i++){
    var r=Math.floor(i/10), c=i%10;
    var x=ox+c*cw, y=oy+r*ch;
    cx.fillStyle=(i<50)?'#F4F8FF':'#C4402C';
    cx.beginPath();
    cx.moveTo(x,y+9); cx.quadraticCurveTo(x+14,y+2,x+27,y+9);
    cx.quadraticCurveTo(x+14,y+16,x,y+9); cx.closePath(); cx.fill();
    cx.beginPath(); cx.moveTo(x+27,y+9); cx.lineTo(x+34,y+3);
    cx.lineTo(x+34,y+15); cx.closePath(); cx.fill();
    cx.fillStyle='rgba(6,12,10,0.34)';
    cx.beginPath(); cx.ellipse(x+17,y+20,15,3,0,0,6.2832); cx.fill();
  }
  grain(cx,20260808+3);
  window.__akLeaders=[{target:'the far aperture the count is read at',at:[540,675],to:[540,675]}];
}
window.__fit=function(){ AK.fitText(document.getElementById('h'),{min:62,max:88,maxLines:3}); };
""", ' data-contacts=\'[{"what":"the isotype shelf",'
     '"shadow":[[600,1188,470,22]],"ground":[[600,1240,470,22]]}]\'')

# ============================================================== 04 BREATHER
write(4, f"""<div class="lyr">
<div class="kick" style="position:absolute;left:80px;top:928px">THE SURFACE</div>
<div id="h" class="hl" style="position:absolute;left:80px;top:986px;width:820px;font-size:96px">The power and the uplink float on top.</div>
<div class="mn" style="position:absolute;left:80px;top:1192px">SOLAR . BATTERY . STARLINK (C27)</div>
{fx(4,72,'4 TO 1 DIFFUSE','6.57 M')}</div>""", """
function draw(){
  var cx=document.getElementById('art').getContext('2d'); px(cx);
  vgrad(cx,[[0,'#0B1A16'],[0.46,'#0A1614'],[1,'#04080D']]);
  AKPOST.grade(cx,{exposure:1.05,saturation:0.94,contrast:1.04});
  // Snell's window. Critical angle 48.6 deg from vertical -> rim at 41.4 deg
  // elevation. Inside is sky, outside the surface is a mirror. Rim crosses the
  // centreline at y 620 by the camera table.
  var cxs=540, cyr=620, R=520;
  var wg=cx.createRadialGradient(cxs,cyr-120,20,cxs,cyr-120,R);
  wg.addColorStop(0,'#FFE9C4'); wg.addColorStop(0.42,'#C7C69A');
  wg.addColorStop(0.80,'#5C7A54'); wg.addColorStop(1,'#243A2C');
  cx.save(); cx.beginPath(); cx.ellipse(cxs,cyr-120,R,R*0.62,0,0,6.2832); cx.clip();
  cx.fillStyle=wg; cx.fillRect(0,0,1080,1350);
  // refracted shoreline crush at the rim, a real optical detail
  AK.reseed(20260808+4);
  for(var i=0;i<140;i++){ var a=AK.rng(20260808+4+i)()*6.2832;
    var rr=R*(0.86+Math.random*0); }
  cx.restore();
  // the rim itself, a hard optical edge
  cx.strokeStyle='rgba(255,233,196,0.40)'; cx.lineWidth=3;
  cx.beginPath(); cx.ellipse(cxs,cyr-120,R,R*0.62,0,0,6.2832); cx.stroke();
  // mirror zone outside the window: the underside of the surface
  cx.save(); cx.globalCompositeOperation='multiply';
  var mg=cx.createLinearGradient(0,0,0,700);
  mg.addColorStop(0,'#1A2A22'); mg.addColorStop(1,'#0A1614');
  cx.fillStyle=mg;
  cx.beginPath(); cx.rect(0,0,1080,760);
  cx.ellipse(cxs,cyr-120,R,R*0.62,0,0,6.2832);
  cx.fill('evenodd'); cx.restore();
  // ripple bands crawling across the ceiling
  caustic(cx,20260808+4,0,120,1080,640,0.20,64);
  // the float slab, black against the daylight, cut by the right edge
  cx.fillStyle='#0C1210';
  cx.beginPath(); cx.moveTo(700,392); cx.lineTo(1080,352); cx.lineTo(1080,438);
  cx.lineTo(700,470); cx.closePath(); cx.fill();
  cx.fillStyle='#0A100E';
  cx.beginPath(); cx.moveTo(700,470); cx.lineTo(1080,438); cx.lineTo(1080,470);
  cx.lineTo(700,502); cx.closePath(); cx.fill();
  cx.fillStyle='#111A16';
  cx.beginPath(); cx.moveTo(768,392); cx.lineTo(846,336); cx.lineTo(944,330);
  cx.lineTo(880,388); cx.closePath(); cx.fill();
  // weir picket tops in the near field, rim-lit from below by the chute glow
  AK.reseed(20260808+40);
  for(var i=0;i<9;i++){
    var x=40+i*126+((i*37)%17), w=44+((i*13)%12);
    var g=cx.createLinearGradient(x,880,x,1350);
    g.addColorStop(0,'#101A16'); g.addColorStop(0.42,'#0A120F'); g.addColorStop(1,'#060C0A');
    cx.fillStyle=g; cx.fillRect(x,880+((i*23)%46),w,470);
    cx.fillStyle='rgba(255,227,174,0.16)'; cx.fillRect(x,880+((i*23)%46),w,5);
    cx.fillStyle='rgba(255,227,174,0.07)'; cx.fillRect(x+w-4,884+((i*23)%46),4,460);
  }
  grain(cx,20260808+4);
}
window.__fit=function(){ AK.fitText(document.getElementById('h'),{min:70,max:100,maxLines:2}); };
""", ' data-breather')

# ========================================================= 07 MEASURED RECORD
write(7, f"""<div class="lyr">
<div class="kick" style="position:absolute;left:80px;top:120px">THE MEASURED RECORD</div>
<div id="h" class="hl" style="position:absolute;left:80px;top:180px;width:820px;font-size:84px">What this weir has actually measured.</div>
<div class="it" style="position:absolute;left:80px;top:352px;width:430px;font-size:28px;line-height:1.4">around 800 in the early 1980s, recalled by Feldpausch, not a published count (C26)</div>
<div class="mn" style="position:absolute;left:614px;top:352px;width:392px;line-height:1.5">THE WEIR HAD COUNTED 7,791 BY JUNE 29TH, 2026. THE DEPARTMENT'S PAGE DOES NOT SAY WHETHER A PERSON OR THE MACHINE COUNTED THEM. (C11)</div>
<div class="it" style="position:absolute;left:614px;top:520px;width:392px;font-size:26px;line-height:1.4">Fish and Game projected more than 40,000 for the 2026 season on June 30th. A projection is not a count, so it gets no bar. (C12)</div>
{fx(7,'FLAT','3 TO 1 RAKING','0.00 M')}</div>""", """
function draw(){
  var cx=document.getElementById('art').getContext('2d'); px(cx);
  vgrad(cx,[[0,'#08120F'],[0.62,'#0A1614'],[1,'#050B09']]);
  AKPOST.grade(cx,{exposure:1.03,saturation:0.95,contrast:1.06});
  // LIT ground, raked from screen-left at 34 deg, then bars cast INTO it
  var lg=cx.createLinearGradient(60,720,1020,1250);
  lg.addColorStop(0,'#22322A'); lg.addColorStop(0.5,'#16241E'); lg.addColorStop(1,'#0A1210');
  cx.fillStyle=lg; cx.fillRect(0,700,1080,650);
  AK.reseed(20260808+7);
  for(var i=0;i<5200;i++){ var x=AK.rng(20260808+7+i)()*1080, y=700+AK.rng(20260808+700+i)()*650;
    cx.fillStyle='rgba(180,200,170,0.035)'; cx.fillRect(x,y,1.6,1.6); }
  var base=1186, maxh=430, MAX=229000;
  var bars=[{lab:'EARLY 1980s',val:800,ph:true,note:'ABOUT 800'},
            {lab:'2023',val:153406,note:'153,406'},
            {lab:'2024',val:210253,note:'210,253'},
            {lab:'2025',val:229000,hi:true,note:'NEARLY 229,000'},
            {lab:'2026',val:0,none:true,note:'NO BAR'}];
  var bw=118, gap=48, x0=104;
  for(var i=0;i<bars.length;i++){
    var b=bars[i], x=x0+i*(bw+gap), h=Math.round(maxh*b.val/MAX);
    if(b.none){
      cx.strokeStyle='#6E7F6A'; cx.lineWidth=3;
      cx.beginPath(); cx.moveTo(x,base); cx.lineTo(x+bw,base); cx.stroke();
      continue;
    }
    if(b.ph){
      cx.setLineDash([30,5,6,5,6,5]); cx.strokeStyle='#4A5C2E'; cx.lineWidth=2.5;
      cx.strokeRect(x,base-Math.max(h,4),bw,Math.max(h,4)); cx.setLineDash([]);
      continue;
    }
    contact(cx,x+bw*0.5,base+7,bw,13);
    var fg=cx.createLinearGradient(x,base-h,x+bw,base);
    if(b.hi){ fg.addColorStop(0,'#F4F8FF'); fg.addColorStop(1,'#B9C6BC'); }
    else { fg.addColorStop(0,'#2A3A30'); fg.addColorStop(1,'#16241E'); }
    cx.fillStyle=fg; cx.fillRect(x,base-h,bw,h);
    // the lit side face, so a bar is a solid and not a fillRect
    cx.fillStyle=b.hi?'#8C9A90':'#0E1814';
    cx.beginPath(); cx.moveTo(x+bw,base-h); cx.lineTo(x+bw+16,base-h-11);
    cx.lineTo(x+bw+16,base-11); cx.lineTo(x+bw,base); cx.closePath(); cx.fill();
    cx.fillStyle=b.hi?'#FFFFFF':'#35473B';
    cx.beginPath(); cx.moveTo(x,base-h); cx.lineTo(x+16,base-h-11);
    cx.lineTo(x+bw+16,base-h-11); cx.lineTo(x+bw,base-h); cx.closePath(); cx.fill();
  }
  // engraved baseline and a printed scale bar
  cx.strokeStyle='#3E5248'; cx.lineWidth=2;
  cx.beginPath(); cx.moveTo(80,base); cx.lineTo(1000,base); cx.stroke();
  cx.strokeStyle='rgba(220,240,220,0.10)'; cx.lineWidth=1;
  cx.beginPath(); cx.moveTo(80,base+2); cx.lineTo(1000,base+2); cx.stroke();
  for(var v=0;v<=200000;v+=50000){
    var y=base-Math.round(maxh*v/MAX);
    cx.strokeStyle='rgba(110,127,106,0.5)'; cx.lineWidth=1;
    cx.beginPath(); cx.moveTo(80,y); cx.lineTo(96,y); cx.stroke();
  }
  grain(cx,20260808+7);
  window.__akLeaders=[{target:'the empty 2026 baseline tick',
                       at:[x0+4*(bw+gap)+59,base], to:[x0+4*(bw+gap)+59,base]}];
}
window.__fit=function(){ AK.fitText(document.getElementById('h'),{min:62,max:88,maxLines:2}); };
""")

# ======================================================== 08 UNCHECKED NUMBER
write(8, f"""<div class="lyr">
<div class="kick" style="position:absolute;left:80px;top:120px">THE UNCHECKED NUMBER</div>
<div id="h" class="hl" style="position:absolute;left:80px;top:180px;width:600px;font-size:84px">Nobody has published a count of the counter.</div>
<div class="bd" style="position:absolute;left:80px;top:474px;width:560px">Feldpausch told KCAW the program has reached <span class="it" style="font-size:36px">"about a 95% confidence interval"</span> on counting sockeye through the system. That is an operator's self report in a radio interview. A confidence interval is not an accuracy metric. No published Redoubt validation was found.</div>
<div class="mn" style="position:absolute;left:80px;top:788px">C22 . C38</div>
{fx(8,44,'2 TO 1','10.21 M')}</div>""", """
function draw(){
  var cx=document.getElementById('art').getContext('2d'); px(cx);
  vgrad(cx,[[0,'#0A1614'],[0.5,'#08120F'],[1,'#04080D']]);
  AKPOST.grade(cx,{exposure:1.03,saturation:0.96,contrast:1.06});
  // chute floor in raking key, the band the cast shadow crosses
  var fgd=cx.createLinearGradient(0,940,1080,1350);
  fgd.addColorStop(0,'#1A2A22'); fgd.addColorStop(1,'#080F0D');
  cx.fillStyle=fgd; cx.fillRect(0,940,1080,410);
  caustic(cx,20260808+8,0,940,1080,410,0.12,44);
  // the fish, macro, one tack-sharp focal plane on the eye at (703,727)
  cx.save(); cx.translate(703,727);
  // full-length cast shadow travelling down-right at the global 34 degrees
  cx.save(); cx.rotate(0.59); cx.fillStyle='rgba(5,11,9,0.62)';
  cx.beginPath(); cx.ellipse(120,300,620,54,0,0,6.2832); cx.fill(); cx.restore();
  var bg=cx.createLinearGradient(-620,-160,540,190);
  bg.addColorStop(0,'#0A100E'); bg.addColorStop(0.42,'#16241E');
  bg.addColorStop(0.72,'#22342A'); bg.addColorStop(1,'#0C1512');
  cx.fillStyle=bg; cx.beginPath();
  cx.moveTo(-660,10); cx.quadraticCurveTo(-330,-150,60,-118);
  cx.quadraticCurveTo(420,-92,560,6); cx.quadraticCurveTo(420,104,60,132);
  cx.quadraticCurveTo(-330,164,-660,10); cx.closePath(); cx.fill();
  // dorsal hump and tail
  cx.fillStyle='#1B2B23'; cx.beginPath();
  cx.moveTo(-190,-116); cx.quadraticCurveTo(-90,-196,60,-120); cx.closePath(); cx.fill();
  cx.fillStyle='#0C1512'; cx.beginPath();
  cx.moveTo(-660,10); cx.lineTo(-806,-116); cx.lineTo(-770,10);
  cx.lineTo(-806,136); cx.closePath(); cx.fill();
  // wet fresnel rim along the lit shoulder
  cx.strokeStyle='rgba(255,227,174,0.42)'; cx.lineWidth=4;
  cx.beginPath(); cx.moveTo(-330,-136); cx.quadraticCurveTo(60,-150,430,-40); cx.stroke();
  // the eye, the only tack-sharp thing in the frame
  cx.fillStyle='#F4F8FF'; cx.beginPath(); cx.arc(392,-30,17,0,6.2832); cx.fill();
  cx.fillStyle='#04080D'; cx.beginPath(); cx.arc(392,-30,9,0,6.2832); cx.fill();
  cx.restore();
  // near-field readout housing, unresolvably blurred, bleeding off the right
  cx.save(); cx.filter='blur(38px)';
  var hg=cx.createLinearGradient(880,760,1080,1180);
  hg.addColorStop(0,'#2A3830'); hg.addColorStop(1,'#0A1210');
  cx.fillStyle=hg; cx.beginPath();
  cx.moveTo(890,742); cx.lineTo(1080,700); cx.lineTo(1080,1210); cx.lineTo(902,1160);
  cx.closePath(); cx.fill();
  cx.fillStyle='rgba(110,165,255,0.30)'; cx.fillRect(946,900,120,64);
  cx.restore(); cx.filter='none';
  // the drafting leader to the adipose fin's own coordinates
  var FIN=[703-150,727-124];
  cx.strokeStyle='rgba(220,240,220,0.16)'; cx.lineWidth=6;
  cx.beginPath(); cx.moveTo(300,1042); cx.lineTo(430,960); cx.lineTo(FIN[0],FIN[1]); cx.stroke();
  cx.strokeStyle='#A9BFA0'; cx.lineWidth=1.5;
  cx.beginPath(); cx.moveTo(300,1042); cx.lineTo(430,960); cx.lineTo(FIN[0],FIN[1]); cx.stroke();
  cx.fillStyle='#A9BFA0'; cx.beginPath(); cx.arc(FIN[0],FIN[1],4,0,6.2832); cx.fill();
  grain(cx,20260808+8);
  window.__akLeaders=[{target:'the adipose fin',at:FIN,to:FIN}];
}
window.__fit=function(){ AK.fitText(document.getElementById('h'),{min:62,max:88,maxLines:3}); };
""")

# ================================================================= 09 CLOSE
write(9, f"""<div class="lyr">
<div id="h" class="hl" style="position:absolute;left:80px;top:170px;width:900px;font-size:84px">A working instrument with no line item.</div>
<div class="inst" style="position:absolute;left:80px;top:404px;width:820px;font-size:44px;letter-spacing:.06em;font-variation-settings:'wdth' 62,'wght' 600;color:#F4F8FF">SAVE THIS FOR THE NEXT FUNDING CYCLE.</div>
<div class="mn" style="position:absolute;left:80px;top:530px">SOURCES IN COMMENTS</div>
<div class="hl" style="position:absolute;left:80px;top:1150px;font-size:40px;letter-spacing:.04em">ALASKA.AI</div>
<div class="mn" style="position:absolute;left:80px;top:1206px;color:#C9D6CE">alaskaaihq.com</div>
<div class="mn log">SHOT 09 / 09 . FOV 50 . DOLLY 15.00 M TOTAL . A 15 MILE BOAT RIDE FROM SITKA (C29)</div>
<div class="mn ctr">09 / 09</div>
<div class="mn crd" data-decorative>56&#176;51'N 135&#176;10'W</div></div>""", """
function draw(){
  var cx=document.getElementById('art').getContext('2d'); px(cx);
  vgrad(cx,[[0,'#081310'],[0.5,'#060E0C'],[1,'#04080D']]);
  motes(cx,20260808+9,260,0.03,0.10);
  AKPOST.grade(cx,{exposure:1.0,saturation:0.92,contrast:1.05});
  // the pulled-back bed: one warm pool around a small aperture, heaviest fog
  litPool(cx,371,1010,420,190,'rgba(50,66,44,0.50)','rgba(50,66,44,0)');
  caustic(cx,20260808+9,120,880,620,300,0.10,58);
  // far weir line, small, receding
  for(var i=0;i<14;i++){ var x=96+i*62;
    cx.fillStyle='rgba(10,18,15,'+(0.75-i*0.02).toFixed(2)+')';
    cx.fillRect(x,832,9,132); }
  // the aperture, now 139x165, alone
  var ag=cx.createRadialGradient(371,979,8,371,979,150);
  ag.addColorStop(0,'#FFF2D6'); ag.addColorStop(0.4,'#FFE3AE'); ag.addColorStop(1,'rgba(255,227,174,0)');
  cx.fillStyle=ag; cx.fillRect(200,830,350,320);
  contact(cx,371,1068,150,18);
  cx.fillStyle='#1C2620'; cx.fillRect(292,896,158,178);
  cx.fillStyle='#FFE3AE'; cx.fillRect(301,905,139,165);
  // two surviving shaft feet, graded into the band
  cx.save(); cx.globalCompositeOperation='screen';
  for(var i=0;i<2;i++){ var a=-1.75+i*0.34;
    cx.save(); cx.translate(371,960); cx.rotate(a);
    var g=cx.createLinearGradient(0,0,0,-620);
    g.addColorStop(0,'rgba(192,138,62,0.03)'); g.addColorStop(1,'rgba(192,138,62,0)');
    cx.fillStyle=g; cx.beginPath(); cx.moveTo(-12,0); cx.lineTo(12,0);
    cx.lineTo(60,-620); cx.lineTo(-60,-620); cx.closePath(); cx.fill(); cx.restore(); }
  cx.restore();
  // the fish completing its crossing, partly in the band
  cx.fillStyle='#0A100E'; cx.beginPath();
  cx.moveTo(560,1044); cx.quadraticCurveTo(640,1016,712,1030);
  cx.quadraticCurveTo(640,1064,560,1044); cx.closePath(); cx.fill();
  // the gold Polaris, once, above the aperture on its vertical axis
  var S=[371,742], R=27;
  cx.fillStyle='#FFC72C';
  cx.beginPath();
  cx.moveTo(S[0],S[1]-R); cx.quadraticCurveTo(S[0]+4,S[1]-4,S[0]+R,S[1]);
  cx.quadraticCurveTo(S[0]+4,S[1]+4,S[0],S[1]+R);
  cx.quadraticCurveTo(S[0]-4,S[1]+4,S[0]-R,S[1]);
  cx.quadraticCurveTo(S[0]-4,S[1]-4,S[0],S[1]-R); cx.closePath(); cx.fill();
  var hg=cx.createRadialGradient(S[0],S[1],2,S[0],S[1],54);
  hg.addColorStop(0,'rgba(255,218,110,0.45)'); hg.addColorStop(1,'rgba(255,218,110,0)');
  cx.fillStyle=hg; cx.beginPath(); cx.arc(S[0],S[1],54,0,6.2832); cx.fill();
  grain(cx,20260808+9);
}
window.__fit=function(){ AK.fitText(document.getElementById('h'),{min:62,max:88,maxLines:2}); };
""", ' data-contacts=\'[{"what":"the chute in the pulled back frame",'
     '"shadow":[[296,1058,150,20]],"ground":[[296,1122,150,20]]}]\'')

print("wrote 02, 03, 04, 07, 08, 09")
