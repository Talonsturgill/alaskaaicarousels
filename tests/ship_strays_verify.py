#!/usr/bin/env python3
"""Prove ship_images.py refuses to ship render.py's canvas layers as frames.

WHY THIS EXISTS
    render.py writes slide-NN.canvas.png beside every render (the art layer
    alone, read by qa.py). Run No.76 (2026-10-03) copied render/slide-*.png
    into runs/<date>/ for the ship step, which took the nine canvas layers
    along. ship_images.py's glob, slide-*.png, matched them, converted them to
    slide-NN.canvas.webp, and printed OK over eighteen slide files in a run
    directory about to merge to main. The showrunner caught it by eye and had
    to improvise a guarded delete under runs/.

WHAT IT CHECKS (each in a throwaway git repo carrying a copy of the script, so
nothing under this repo's runs/ is ever touched)
    1. RED CASE, the No.76 copy: real frames plus canvas layers. The upgraded
       script exits 1, names the layers and the remedy, converts the nine
       frames, and never writes a slide-NN.canvas.webp. --base runs the same
       case against the pre-upgrade script and shows it exit 0 with the
       canvas webps written (the defect, reproduced).
    2. A run that is already converted but still carries canvas layers fails
       too (the "already converted" path used to skip error reporting).
    3. --drop-png also fails while strays remain.
    4. --drop-canvas-layers removes exactly the untracked canvas layers, then
       the normal pass is OK and the run holds nine frames and nothing else.
    5. Guards: a TRACKED canvas layer is refused and left in place; another
       non-frame name (slide-03 copy.png) is reported and never deleted;
       --drop-canvas-layers with --all is rejected.
    6. A clean run (frames only) converts and exits 0 exactly as before.

USAGE
    python3 tests/ship_strays_verify.py            # out/2026-10-03/render if present,
                                                   # else synthetic frames (out/ is gitignored)
    python3 tests/ship_strays_verify.py --render-dir out/<date>/render
    python3 tests/ship_strays_verify.py --base HEAD~1   # also reproduce the defect

Exit 0 = HOLDS, 1 = a defect is present.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATE = "2026-10-03"


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)


def make_repo(tmp: Path, script_src: str, render: Path, canvas: bool,
              frames: int = 9) -> Path:
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "scripts").mkdir(parents=True)
    (tmp / "scripts" / "ship_images.py").write_text(script_src)
    run = tmp / "runs" / DATE
    run.mkdir(parents=True)
    for i in range(1, frames + 1):
        shutil.copy(render / f"slide-{i:02d}.png", run / f"slide-{i:02d}.png")
        if canvas and (render / f"slide-{i:02d}.canvas.png").exists():
            shutil.copy(render / f"slide-{i:02d}.canvas.png",
                        run / f"slide-{i:02d}.canvas.png")
    sh(["git", "init", "-q"], tmp)
    sh(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q",
        "--allow-empty", "-m", "init"], tmp)
    return run


def ship(tmp: Path, *args):
    return sh([sys.executable, "scripts/ship_images.py", "--run", DATE, "--no-verify",
               *args], tmp)


def names(run: Path):
    return sorted(p.name for p in run.iterdir() if p.is_file())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render-dir", default=str(REPO / "out" / DATE / "render"))
    ap.add_argument("--base", default=None,
                    help="git rev of the pre-upgrade script, to reproduce the defect")
    ap.add_argument("--frames", type=int, default=9)
    a = ap.parse_args()
    render = Path(a.render_dir)
    synth = None
    if not (render / "slide-01.canvas.png").exists():
        # out/ is gitignored, so a later checkout has no No.76 renders. Build a
        # stand-in with the same names: noisy frames (so the encoder has real
        # work) and a canvas layer beside each.
        from PIL import Image
        synth = tempfile.TemporaryDirectory()
        render = Path(synth.name)
        for i in range(1, a.frames + 1):
            Image.effect_noise((216, 270), 40 + i).convert("RGB").save(
                render / f"slide-{i:02d}.png")
            Image.effect_noise((216, 270), 90 + i).convert("RGB").save(
                render / f"slide-{i:02d}.canvas.png")
        print(f"(no canvas layers in {a.render_dir}; using {a.frames} synthetic frames)")
    new_src = (REPO / "scripts" / "ship_images.py").read_text()
    n = a.frames
    fails = []

    def check(label, ok, detail=""):
        print(f"[{'HOLD' if ok else 'FAIL'}] {label}{(' -- ' + detail) if detail else ''}")
        if not ok:
            fails.append(label)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        if a.base:
            old_src = sh(["git", "show", f"{a.base}:scripts/ship_images.py"], REPO).stdout
            run = make_repo(td / "base", old_src, render, True, n)
            p = ship(td / "base")
            cw = [x for x in names(run) if ".canvas." in x]
            check("BASE reproduces the defect: exit 0 with canvas webps written",
                  p.returncode == 0 and any(x.endswith(".canvas.webp") for x in cw),
                  f"rc={p.returncode}, canvas files {len(cw)}: {cw[:3]}")

        # 1. red case
        run = make_repo(td / "r1", new_src, render, True, n)
        p = ship(td / "r1")
        nm = names(run)
        check("1 red case exits 1", p.returncode == 1, f"rc={p.returncode}")
        check("1 names the canvas layers and the remedy",
              "slide-01.canvas.png" in p.stderr and "--drop-canvas-layers" in p.stderr,
              p.stderr.strip().splitlines()[0][:160] if p.stderr.strip() else "no stderr")
        check("1 never writes a canvas webp", not any(x.endswith(".canvas.webp") for x in nm))
        check("1 frames still converted",
              all(f"slide-{i:02d}.webp" in nm for i in range(1, n + 1)))

        # 2. already converted, layers still present
        p = ship(td / "r1")
        check("2 already-converted run with layers still exits 1",
              p.returncode == 1 and "canvas" in p.stderr, f"rc={p.returncode}")

        # 3. --drop-png fails while strays remain
        p = ship(td / "r1", "--drop-png")
        check("3 --drop-png fails while strays remain", p.returncode == 1, f"rc={p.returncode}")

        # 4. guarded removal, then clean
        p = ship(td / "r1", "--drop-canvas-layers")
        check("4 --drop-canvas-layers exits 0", p.returncode == 0,
              (p.stdout + p.stderr).strip()[-160:])
        p = ship(td / "r1")
        nm = names(run)
        check("4 normal pass OK afterwards", p.returncode == 0, f"rc={p.returncode}")
        frames = [x for x in nm if x.startswith("slide-")]
        check("4 run holds frames only",
              frames == [f"slide-{i:02d}.webp" for i in range(1, n + 1)], str(frames[:4]))

        # 5a. tracked layer refused
        run = make_repo(td / "r5", new_src, render, True, 2)
        sh(["git", "add", f"runs/{DATE}/slide-01.canvas.png"], td / "r5")
        sh(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m",
            "ship a layer"], td / "r5")
        p = ship(td / "r5", "--drop-canvas-layers")
        check("5 tracked canvas layer refused, nothing deleted",
              p.returncode == 1 and (run / "slide-01.canvas.png").exists()
              and (run / "slide-02.canvas.png").exists(),
              (p.stderr.strip().splitlines() or [""])[0][:160])
        # 5b. other non-frame names reported, never deleted
        run = make_repo(td / "r6", new_src, render, False, 3)
        shutil.copy(run / "slide-03.png", run / "slide-03 copy.png")
        p = ship(td / "r6")
        check("5 'slide-03 copy.png' fails the pass and is not converted",
              p.returncode == 1 and not (run / "slide-03 copy.webp").exists(),
              f"rc={p.returncode}")
        p = ship(td / "r6", "--drop-canvas-layers")
        check("5 --drop-canvas-layers leaves it alone and still exits 1",
              p.returncode == 1 and (run / "slide-03 copy.png").exists(), f"rc={p.returncode}")
        p = sh([sys.executable, "scripts/ship_images.py", "--all", "--drop-canvas-layers"],
               td / "r6")
        check("5 --drop-canvas-layers with --all rejected", p.returncode == 2,
              f"rc={p.returncode}")

        # 6. clean run unchanged
        run = make_repo(td / "r7", new_src, render, False, n)
        p = ship(td / "r7")
        check("6 clean run exits 0 with og.jpg and n webps",
              p.returncode == 0 and (run / "og.jpg").exists()
              and len([x for x in names(run) if x.endswith(".webp")]) == n,
              f"rc={p.returncode}")

    print(f"\n{'HOLDS' if not fails else 'DEFECT'}: {len(fails)} failing check(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
