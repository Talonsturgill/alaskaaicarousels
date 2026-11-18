#!/usr/bin/env python3
"""render_recycle_verify.py -- render.py relaunches its browser every few slides,
survives one crash per slide, and records each slide's memory (2026-11-17,
weekly machine pass; queue item 2026-11-13, repeat 2).

WHAT IT RECONSTRUCTS. No.114's first full nine-slide render was OOM-killed
(exit 137) and took the worker with it; batches of three were clean, and No.115
and No.117 rendered every pass in threes by hand.

  python3 tests/render_recycle_verify.py      # exit 0 = every check holds

  cli       --recycle-every -1 exits 2 before launching a browser.
  recycle   five light slides at the default: the browser is relaunched once
            after slide 3 and every record carries mem.peak_pss_mb.
  off       --recycle-every 0 relaunches nothing.
  renderer  a renderer process is SIGKILLed while slide 02 waits in its
            renderReady (what the kernel's OOM killer does to the largest
            process): the render relaunches, renders slide 02 again, exits 0,
            and the record keeps the first attempt's error under crash_retry;
            qa.py WARNs on it.
  browser   the browser's own main process is SIGKILLed during slide 02: same
            outcome. Before this change both cases FAILED the call (measured on
            the parent commit: exit 1, 'Target crashed' / browser closed).
"""

import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
sys.path.insert(0, str(ENGINE))

HEAD = ('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;'
        'width:1080px;height:1350px;background:#0b1118;color:#E8EEF4;font:48px sans-serif}'
        '</style></head><body><canvas id="c" width="2160" height="2700" style="position:absolute;'
        'inset:0;width:1080px;height:1350px"></canvas><h1 style="position:absolute;left:96px;'
        'top:160px;margin:0">Slide %s</h1><script>\n'
        'const cx = document.getElementById("c").getContext("2d");\n'
        'const g = cx.createLinearGradient(0, 0, 0, 2700); g.addColorStop(0, "#14304a"); '
        'g.addColorStop(1, "#05080f"); cx.fillStyle = g; cx.fillRect(0, 0, 2160, 2700);\n'
        'for (let i = 0; i < 4000; i++) { cx.fillStyle = "rgba(200,220,255," + ((i * 7919) %% 97) / 900 + ")"; '
        'cx.fillRect((i * 2654435761) %% 2160, (i * 40503) %% 2700, 3, 3); }\n')


def slide(n, wait_ms=0, marker=False):
    body = HEAD % n
    if wait_ms:
        body += ("window.renderReady = (async () => { %s await new Promise(r => setTimeout(r, %d)); "
                 "return true; })();\n" % ("document.title = 'AKCRASHME';" if marker else "", wait_ms))
    return body + "</script></body></html>"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=600)


def children(root):
    kids = {}
    for n in os.listdir("/proc"):
        if n.isdigit():
            try:
                st = open("/proc/%s/stat" % n).read()
                kids.setdefault(int(st.rsplit(")", 1)[1].split()[1]), []).append(int(n))
            except (OSError, ValueError, IndexError):
                pass
    out, stack = [], [root]
    while stack:
        x = stack.pop()
        out.append(x)
        stack += kids.get(x, [])
    return out[1:]


def cmdline(pid):
    try:
        return open("/proc/%d/cmdline" % pid, "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")
    except OSError:
        return ""


def render_with_kill(sd, od, which):
    """Start render.py; once slide-02 is loading, SIGKILL one process, once."""
    proc = subprocess.Popen([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd),
                             "--out-dir", str(od)], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True)
    lines, killed = [], []

    def reader():
        for ln in proc.stdout:
            lines.append(ln)

    th = threading.Thread(target=reader, daemon=True)
    th.start()
    t0 = time.time()
    while proc.poll() is None and not killed and time.time() - t0 < 120:
        if any("slide-01.html" in ln for ln in lines):
            time.sleep(1.5)          # slide 02 is now inside its 6 s renderReady wait
            for pid in children(proc.pid):
                c = cmdline(pid)
                if which == "renderer" and "--type=renderer" in c and "--extension-process" not in c:
                    os.kill(pid, signal.SIGKILL); killed.append(pid)
                elif which == "browser" and "chrome" in c and "--type=" not in c:
                    os.kill(pid, signal.SIGKILL); killed.append(pid)
                if killed and which == "browser":
                    break
            break
        time.sleep(0.1)
    proc.wait(timeout=600)
    th.join(timeout=5)
    return proc.returncode, "".join(lines), killed


def main():
    if not Path("/proc/self/smaps_rollup").exists():
        print("SKIP: needs Linux /proc")
        return 0
    from render import check_recycle_arg
    checks = []
    checks.append(("unit: check_recycle_arg refuses -1, accepts 0 and 3",
                   bool(check_recycle_arg(-1)) and not check_recycle_arg(0) and not check_recycle_arg(3), ""))
    with tempfile.TemporaryDirectory(prefix="ak-recycle-") as td:
        td = Path(td)
        r = run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(td),
                 "--out-dir", str(td / "o"), "--recycle-every", "-1"])
        checks.append(("cli: --recycle-every -1 exits 2", r.returncode == 2, r.stderr.strip()[-120:]))

        sd = td / "light"
        sd.mkdir()
        for n in range(1, 6):
            (sd / ("slide-%02d.html" % n)).write_text(slide(n))
        r = run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd), "--out-dir", str(td / "r1")])
        rel = r.stdout.count("[browser] relaunched")
        rep = json.loads((td / "r1" / "render_report.json").read_text())
        mems = [s.get("mem", {}).get("peak_pss_mb") for s in rep["slides"]]
        checks.append(("recycle: default relaunches once over five slides, exit 0",
                       r.returncode == 0 and rel == 1 and "after 3 slide(s)" in r.stdout,
                       "exit %s, %d relaunch(es)" % (r.returncode, rel)))
        checks.append(("recycle: every record carries mem.peak_pss_mb", all(isinstance(m, int) and m > 0 for m in mems),
                       str(mems)))
        checks.append(("recycle: the status line prints mem=", r.stdout.count("mem=") == 5, ""))
        r = run([sys.executable, str(ENGINE / "render.py"), "--slides-dir", str(sd), "--out-dir", str(td / "r0"),
                 "--recycle-every", "0"])
        checks.append(("off: --recycle-every 0 never relaunches", r.returncode == 0 and "relaunched" not in r.stdout,
                       "exit %s" % r.returncode))

        for which in ("renderer", "browser"):
            cd = td / ("crash-" + which)
            cd.mkdir()
            (cd / "slide-01.html").write_text(slide(1))
            (cd / "slide-02.html").write_text(slide(2, wait_ms=6000))
            (cd / "slide-03.html").write_text(slide(3))
            code, out, killed = render_with_kill(cd, td / ("rc-" + which), which)
            rep = json.loads((td / ("rc-" + which) / "render_report.json").read_text()) \
                if (td / ("rc-" + which) / "render_report.json").exists() else {"slides": []}
            s2 = next((s for s in rep["slides"] if s["file"] == "slide-02.html"), {})
            checks.append(("%s: a process was killed mid-slide" % which, bool(killed), str(killed)))
            checks.append(("%s: the call still exits 0 with all three PNGs" % which,
                           code == 0 and all((td / ("rc-" + which) / ("slide-0%d.png" % n)).exists() for n in (1, 2, 3)),
                           "exit %s; %s" % (code, out.strip().splitlines()[-3:] if out.strip() else "")))
            checks.append(("%s: slide 02 keeps the first attempt under crash_retry" % which,
                           bool(s2.get("crash_retry")) and s2.get("ok") is True, str(s2.get("crash_retry"))[:160]))
            q = subprocess.run([sys.executable, str(ENGINE / "qa.py"), "--render-dir", str(td / ("rc-" + which))],
                               capture_output=True, text=True, timeout=300)
            qa = {}
            qp = td / ("rc-" + which) / "machine_qa.json"
            if qp.exists():
                qa = json.loads(qp.read_text())
            warns = [w for sl in qa.get("slides", []) for w in sl.get("warns", []) if "browser died" in w]
            checks.append(("%s: qa.py WARNs on the retried slide" % which,
                           len(warns) == 1 or "browser died" in q.stdout, "%d warn(s)" % len(warns)))
    bad = [c for c in checks if not c[1]]
    for name, ok, det in checks:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + det) if det and not ok else ""))
    print("%d/%d checks hold" % (len(checks) - len(bad), len(checks)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
