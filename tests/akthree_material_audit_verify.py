#!/usr/bin/env python3
"""akthree_material_audit_verify.py -- the reconstruction behind AKT.audit,
AKT.mat.glass and render.py's static metal scan (2026-10-09, weekly pass).

WHAT IT RECONSTRUCTS. Two akthree material mistakes cost No.80 and No.82 four
critic rounds between them:
  - a metal with too little environment: No.80's aluminium conductor (metalness
    0.92, hand-rolled renderer, no environment at all) came out black rubber;
    No.82's steel headplate read matte at envMapIntensity 0.9 under
    AKT.environment intensity 0.34 (0.31 effective) and as steel at 2.8;
  - glass: No.82's 0.22-opacity pale shells cast a full shadow over the broth
    and washed it as milk with their own lit albedo.

  python3 tests/akthree_material_audit_verify.py      # exit 0 = every check holds

It writes six slides of exactly those kinds, runs the REAL render.py and qa.py
over them, and reads machine_qa.json:
  01 No.82 reconstruction, steel at 0.9 x 0.34      -> metal WARN (must FAIL to pass clean)
  02 the same scene at 2.8 x 0.34 (No.82's fix)     -> no material WARN
  03 AKT steel with no environment                  -> metal WARN
  04 a pale 0.22-opacity shell added with AKT.add   -> shadow WARN and milk WARN
  05 the same shell built with AKT.mat.glass()      -> no material WARN, and the
                                                       mesh casts and takes no shadow
  06 a hand-rolled three scene, metalness 0.92, no
     environment anywhere (No.80)                   -> metal WARN from the static scan
and a parity check: slide 02's scene renders the same pixels with git HEAD's
akthree.js as with the new one, so no existing slide changes.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f7c144ec7631a00f511ffde0424c0fff2a25f001"  # main before the 2026-10-09 weekly pass
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="@@ASSETS@@/fonts/fonts.css">
<style>*{margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;background:#05080f}
canvas{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;left:96px;top:96px;font-family:"Manrope",sans-serif;font-size:40px;color:#eef4fc}
.w{position:absolute;right:96px;bottom:96px;font-family:"JetBrains Mono",monospace;font-size:24px;color:#cfd8e6}</style>
</head><body><canvas id="scene" width="2160" height="2700"></canvas>
<div class="t">Material audit reconstruction</div><div class="w">SLIDE_NO / 06</div>
<script type="module">
window.renderReady = (async () => {
  const THREE = await import('@@ASSETS@@/js/three.module.min.js');
"""

AKT_SCENE = """  const AKT = (await import('AKT_URL')).init(THREE);
  const R = AKT.setup(document.getElementById('scene'), { w:1080, h:1350, bg:0x05080f, exposure:1.1 });
  ENV
  AKT.rig(R, AKT.rigs.arcticNight);
  AKT.ground(R, { color: 0x1a2a3c, y: 0 });
  BODY
  AKT.frame(R, { from:[3.2,2.4,4.6], look:[0,0.8,0], fov:45 });
  await AKT.snapshot(R);
  return true;
})();
</script></body></html>"""

STEEL = """const plate = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.3, 64),
    AKT.mat.steel({ color: 0x8a96a3, roughness: 0.2, metalness: 0.95, envMapIntensity: EMI }));
  plate.position.y = 0.6; AKT.add(R, plate);"""

SHELL = """const broth = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 0.9, 64), AKT.mat.clay(0x6b4a2e));
  broth.position.y = 0.45; AKT.add(R, broth);
  const shell = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 1.4, 64, 1, true), MAT);
  shell.name = 'vessel shell'; shell.position.y = 0.7; AKT.add(R, shell);
  window.__shellShadow = [shell.castShadow, shell.receiveShadow];"""

HIDDEN_GROUP = """
  const ghost = new THREE.Group(); ghost.visible = false;
  ghost.add(new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 1.4, 64, 1, true), PALE_MAT));
  AKT.add(R, ghost);"""

PALE = ("new THREE.MeshStandardMaterial({ color: 0xd8e6f2, roughness: 0.05, metalness: 0, "
        "transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false })")

HAND = """  const c = document.getElementById('scene');
  const renderer = new THREE.WebGLRenderer({ canvas: c, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(2); renderer.setSize(1080, 1350, false);
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x05080f);
  const cam = new THREE.PerspectiveCamera(45, 1080 / 1350, 0.1, 100);
  cam.position.set(3, 2, 4); cam.lookAt(0, 0.5, 0);
  const key = new THREE.DirectionalLight(0xffffff, 3); key.position.set(4, 6, 3); scene.add(key);
  scene.add(new THREE.AmbientLight(0x334455, 1));
  const tube = new THREE.Mesh(new THREE.TorusGeometry(0.8, 0.12, 32, 128),
    new THREE.MeshStandardMaterial({ color: 0xc8ccd0, metalness: 0.92, roughness: 0.3 }));
  tube.position.y = 0.6; scene.add(tube);
  renderer.render(scene, cam);
  return true;
})();
</script></body></html>"""


def akt(no, env, body, akt_url="@@ASSETS@@/js/akthree.js"):
    return (HEAD.replace("SLIDE_NO", "%02d" % no)
            + AKT_SCENE.replace("AKT_URL", akt_url).replace("ENV", env).replace("BODY", body))


def slides():
    env034 = "AKT.environment(R, { intensity: 0.34 });"
    return {
        1: akt(1, env034, STEEL.replace("EMI", "0.9")),
        2: akt(2, env034, STEEL.replace("EMI", "2.8")),
        3: akt(3, "", STEEL.replace("EMI", "1.0")),
        4: akt(4, env034, SHELL.replace("MAT", PALE)),
        5: akt(5, env034, SHELL.replace("MAT", "AKT.mat.glass()")),
        6: HEAD.replace("SLIDE_NO", "06") + HAND,
        # Codex, PR #422: glass() inside a material ARRAY still leaves the shadow pass
        8: akt(8, env034, SHELL.replace("MAT", "[AKT.mat.glass(), AKT.mat.clay(0x6b4a2e)]")),
        # Codex, PR #422: a pale shell under an INVISIBLE group is never drawn, so never audited
        9: akt(9, env034, STEEL.replace("EMI", "2.8") + HIDDEN_GROUP),
        # Codex, PR #422: the static scan covers every metalness above 0.5, 0.55 included
        10: HEAD.replace("SLIDE_NO", "10") + HAND.replace("metalness: 0.92", "metalness: 0.55"),
    }


HIDDEN_GROUP = HIDDEN_GROUP.replace("PALE_MAT", PALE)

MATERIAL_WARNS = ("metal with nothing to reflect", "transparent shell casts a shadow",
                  "transparent shell washes")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))


def main():
    checks = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        sd, rd = td / "slides", td / "render"
        sd.mkdir()
        for n, html in slides().items():
            (sd / ("slide-%02d.html" % n)).write_text(html)
        r = run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd),
                 "--out-dir", str(rd), "--timeout", "120000"])
        print(r.stdout[-1500:])
        if r.returncode != 0:
            print(r.stderr[-2000:])
        checks.append((r.returncode == 0, "render.py rendered the nine reconstruction slides"))
        q = run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(rd)])
        mq = json.loads((rd / "machine_qa.json").read_text())
        rep = json.loads((rd / "render_report.json").read_text())
        warns = {int(s["file"][6:8]): [w for w in s["warns"] if w.startswith(MATERIAL_WARNS)]
                 for s in mq["slides"]}
        for n, w in sorted(warns.items()):
            print("  %02d: %s" % (n, [x[:60] for x in w] or "no material warn"))

        def has(n, prefix):
            return any(w.startswith(prefix) for w in warns.get(n, []))

        checks.append((has(1, "metal with nothing to reflect"),
                       "01 No.82 reconstruction (0.9 x 0.34 = 0.31) WARNs as an unlit metal"))
        checks.append((not warns.get(2), "02 No.82's fix (2.8 x 0.34 = 0.95) passes clean"))
        checks.append((has(3, "metal with nothing to reflect"),
                       "03 a metal with no environment at all WARNs"))
        checks.append((has(4, "transparent shell casts a shadow") and has(4, "transparent shell washes"),
                       "04 a pale shell added with AKT.add WARNs for its shadow and its milk"))
        checks.append((not warns.get(5), "05 the same shell from AKT.mat.glass() passes clean"))
        checks.append((not warns.get(8), "08 glass() inside a material array passes clean (no shadow warn)"))
        checks.append((not warns.get(9), "09 a pale shell under an invisible group is not audited"))
        checks.append((has(10, "metal with nothing to reflect"),
                       "10 a hand-rolled metal at 0.55 WARNs from the static scan"))
        checks.append((has(6, "metal with nothing to reflect"),
                       "06 No.80's hand-rolled metal with no environment WARNs (static scan)"))
        mat_fails = [f for s in mq["slides"] for f in s["fails"]
                     if re.search(r"metal|transparent shell|akthree_audit", f)]
        other = sorted({f[:70] for s in mq["slides"] for f in s["fails"]})
        print("  qa exit %d; fails unrelated to the audit (the bare test slides): %s"
              % (q.returncode, other))
        checks.append((not mat_fails, "the audit adds WARNs only, never a FAIL"))

        # the glass helper really leaves the shadow pass, read in the page
        from playwright.sync_api import sync_playwright
        sys.path.insert(0, str(ENGINE))
        from render import launch_chromium, resolve_html
        rs = td / "resolved"
        rs.mkdir()
        # pinned to main before the 2026-10-09 pass; HEAD would compare the code with itself (Codex, PR #422)
        head_js = run(["git", "show", "%s:assets/js/akthree.js" % BASELINE]).stdout
        (td / "akthree_head.js").write_text(head_js)
        (sd / "slide-07.html").write_text(akt(2, "AKT.environment(R, { intensity: 0.34 });",
                                              STEEL.replace("EMI", "2.8"),
                                              akt_url=(td / "akthree_head.js").as_uri()))
        with sync_playwright() as p:
            b = launch_chromium(p)
            shots = {}
            for name in ("slide-05.html", "slide-02.html", "slide-07.html"):
                page = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
                page.goto(resolve_html(sd / name, rs).as_uri(), wait_until="load", timeout=120000)
                page.evaluate("() => window.renderReady")
                if name == "slide-05.html":
                    flags = page.evaluate("() => window.__shellShadow")
                    checks.append((flags == [False, False],
                                   "AKT.add takes an AKT.mat.glass() mesh out of the shadow pass both "
                                   "ways (castShadow, receiveShadow = %s)" % flags))
                else:
                    shots[name] = page.evaluate(
                        "() => document.getElementById('scene').toDataURL('image/png')")
                page.close()
            b.close()
        checks.append((shots.get("slide-02.html") == shots.get("slide-07.html"),
                       "parity: a scene without the new helper renders the same pixels with git "
                       "HEAD's akthree.js"))
        audit = {n: [a.get("kind") for a in s.get("akthree_audit") or []]
                 for n, s in ((int(x["file"][6:8]), x) for x in rep["slides"])}
        print("  akthree_audit kinds: %s" % audit)
    bad = 0
    for ok, m in checks:
        print(("PASS " if ok else "FAIL ") + m)
        bad += 0 if ok else 1
    print("%d/%d checks hold" % (len(checks) - bad, len(checks)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
