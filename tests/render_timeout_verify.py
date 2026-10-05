#!/usr/bin/env python3
"""render_timeout_verify.py -- render.py names the remedy for a load timeout and
refuses a seconds-sized --timeout (2026-10-06, weekly machine pass).

WHAT IT RECONSTRUCTS. No.77 (slides 06 and 07) and No.78 (slide 06) lost renders
to page.goto timing out on the load event: the slide's own synchronous art held
it. The exception named the symptom only. No.78 also passed `--timeout 300`,
meaning seconds, to a flag in milliseconds, and page.goto failed in 0.4 s.

  python3 tests/render_timeout_verify.py      # exit 0 = every check holds

  unit      timeout_remedy() maps a Playwright goto timeout to the load remedy
            and render.py's own 'renderReady timeout' to the race remedy, and
            anything else to None; check_timeout_arg() refuses 300 and 999 and
            accepts 1000 and 45000.
  cli       render.py --timeout 300 exits 2 before launching a browser, naming
            the unit and suggesting 300000.
  shapes    three slides through the real render.py at --timeout 2000, each
            with a 6 s synchronous block: at the top of a script (FAILS, with
            the remedy), right after `await load` (FAILS, with the remedy:
            the block runs in the load continuation), and after `await load`
            plus one setTimeout 0 yield, which is the remedy (renders OK).
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
sys.path.insert(0, str(ENGINE))

HEAD = ('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;'
        'width:1080px;height:1350px;background:#0b1118}</style></head><body>'
        '<canvas width="2160" height="2700" style="position:absolute;inset:0;'
        'width:1080px;height:1350px"></canvas><script>\n')
BLOCK = "let t0 = performance.now(), acc = 0; while (performance.now() - t0 < 6000) { acc += Math.sqrt(acc + 1); }\n"
LOAD = ("await new Promise(r => (document.readyState === 'complete' ? r() : "
        "addEventListener('load', r, { once: true })));\n")
SLIDES = {
    "slide-01.html": HEAD + BLOCK + "window.renderReady = Promise.resolve(true);\n</script></body></html>",
    "slide-02.html": HEAD + "window.renderReady = (async () => {\n" + LOAD + BLOCK
                     + "return true; })();\n</script></body></html>",
    "slide-03.html": HEAD + "window.renderReady = (async () => {\n" + LOAD
                     + "await new Promise(r => setTimeout(r, 0));\n" + BLOCK
                     + "return true; })();\n</script></body></html>",
}


def main():
    from render import check_timeout_arg, timeout_remedy
    checks = []
    goto = ('Page.goto: Timeout 45000ms exceeded.\nCall log:\n  - navigating to '
            '"file:///x/slide-06.html", waiting until "load"\n')
    checks.append(("unit: a goto timeout maps to the load remedy",
                   (timeout_remedy(goto, 45000) or "").startswith("remedy: page.goto waited 45000 ms"), ""))
    checks.append(("unit: the renderReady race maps to the race remedy",
                   "30 s cap" in (timeout_remedy("Error: renderReady timeout", 45000) or ""), ""))
    checks.append(("unit: any other exception maps to nothing",
                   timeout_remedy("TypeError: AK.noise2 is not a function", 45000) is None, ""))
    checks.append(("unit: --timeout 300 and 999 refused, 1000 and 45000 accepted",
                   bool(check_timeout_arg(300)) and bool(check_timeout_arg(999))
                   and check_timeout_arg(1000) is None and check_timeout_arg(45000) is None, ""))
    with tempfile.TemporaryDirectory() as td:
        sd, od = Path(td) / "slides", Path(td) / "render"
        sd.mkdir()
        for name, html in SLIDES.items():
            (sd / name).write_text(html)
        p = subprocess.run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd),
                            "--out-dir", str(od), "--timeout", "300"], capture_output=True, text=True)
        checks.append(("cli: --timeout 300 exits 2 and names the unit",
                       p.returncode == 2 and "MILLISECONDS" in p.stderr and "300000" in p.stderr
                       and not (od / "render_report.json").exists(),
                       "exit %d: %s" % (p.returncode, p.stderr.strip()[:90])))
        p = subprocess.run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd),
                            "--out-dir", str(od), "--timeout", "2000"], capture_output=True, text=True)
        rep = {r["file"]: r for r in json.loads((od / "render_report.json").read_text())["slides"]}
    has = lambda f: any(e.startswith("remedy: page.goto waited 2000 ms") for e in rep[f]["page_errors"])
    checks.append(("shapes: a block at the top of the script fails, with the remedy",
                   has("slide-01.html"), "%d ms" % rep["slide-01.html"]["render_ms"]))
    checks.append(("shapes: a block straight after await load fails, with the remedy",
                   has("slide-02.html"), "%d ms" % rep["slide-02.html"]["render_ms"]))
    checks.append(("shapes: load, one yield, then the block renders OK (the remedy works)",
                   rep["slide-03.html"]["ok"] and not rep["slide-03.html"]["page_errors"],
                   "%d ms" % rep["slide-03.html"]["render_ms"]))
    checks.append(("shapes: render.py exits 1 on the two failing slides", p.returncode == 1, ""))
    bad = 0
    for name, ok, detail in checks:
        print(("  ok   " if ok else "  BAD  ") + name + (": " + detail if detail else ""))
        bad += 0 if ok else 1
    print("%d/%d checks hold" % (len(checks) - bad, len(checks)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
