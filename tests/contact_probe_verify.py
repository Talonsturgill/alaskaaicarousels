#!/usr/bin/env python3
"""Does contact_probe read a contact shadow the way the gate does? (2026-08-26)

Built on a synthetic frame whose truth is known by construction: a dark plate,
one lit elliptical pool, and one cast attached to an object standing at a known
x. Three things are held.

  1. AGREEMENT. On the same rects, the probe's shadow L*, ground L* and dL are
     the numbers qa.contact_reads() reports. The probe imports qa.py rather
     than restating its colour maths, and this proves the import is doing what
     it claims, because a tool that disagrees with the gate is worse than no
     tool.
  2. THE RED CASE. Run No.41's actual mistake -- the ground rect stacked
     directly BELOW the shadow rect instead of beside it -- is reproduced here
     and measures NEGATIVE separation, and the probe names the stacking as the
     reason rather than leaving the author to guess.
  3. THE PROPOSAL. Pointed at the object's base, the probe finds the cast
     within a few px of where it was actually drawn and pairs it with lit
     ground at the same y, and that pair clears qa.py's floor.

    python3 tests/contact_probe_verify.py

Exit 0 HOLDS, exit 1 BROKEN.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import contact_probe as cp  # noqa: E402

DW, DH, SCALE = 1080, 1350, 2
POOL_X, POOL_Y, POOL_RX, POOL_RY = 540.0, 1000.0, 200.0, 26.0
CAST_X, CAST_RX, CAST_RY = 505.0, 40.0, 10.0
BASE_X, BASE_Y = 512.0, 996.0     # where the object stands, and its base line


def fixture_png(path):
    """A plate, a lit pool, and a cast attached to the object standing on it."""
    h, w = DH * SCALE, DW * SCALE
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    x, y = xx / SCALE, yy / SCALE
    v = np.full((h, w), 60.0)
    d = np.hypot((x - POOL_X) / POOL_RX, (y - POOL_Y) / POOL_RY)
    v += 150.0 * np.clip(1.0 - d, 0, 1) ** 1.5
    dc = np.hypot((x - CAST_X) / CAST_RX, (y - (POOL_Y + 2)) / CAST_RY)
    v -= 130.0 * np.clip(1.0 - dc, 0, 1)
    v = np.clip(v, 0, 255).astype(np.uint8)
    arr = np.stack([v, v, v], -1)
    Image.fromarray(arr).save(path)
    return arr


def qa_numbers(arr, shadow, ground):
    """What qa.contact_reads reports for a pair, as (shadow_L, ground_L, dL)."""
    verdict, detail = cp.QA.contact_reads(
        arr, {"what": "fixture", "shadow": [shadow], "ground": [ground]}, DW, DH)
    import re
    m = re.search(r"shadow L\* (-?[\d.]+) vs ground L\* (-?[\d.]+), dL (-?[\d.]+)", detail)
    if not m:
        return None, verdict, detail
    return tuple(float(g) for g in m.groups()), verdict, detail


def main():
    bad = []
    with tempfile.TemporaryDirectory() as d:
        rdir = Path(d)
        (rdir / "render_report.json").write_text(json.dumps(
            {"canvas": {"width": DW, "height": DH, "scale": SCALE}, "slides": []}))
        arr = fixture_png(rdir / "slide-01.png")
        fr = cp.Frame(rdir / "slide-01.png", DW, DH)

        # 2. THE RED CASE: the ground rect stacked below the shadow rect.
        shadow = [int(CAST_X) - 13, int(BASE_Y), 26, 10]
        stacked = [int(CAST_X) - 13, int(BASE_Y) + 22, 26, 10]
        nums, verdict, detail = qa_numbers(arr, shadow, stacked)
        if nums is None:
            bad.append("could not read qa.contact_reads: %s" % detail)
        elif nums[2] >= 0:
            bad.append("red case did not reproduce: stacking the ground rect "
                       "below the shadow measured dL %.1f, expected negative" % nums[2])
        elif verdict != "fail":
            bad.append("qa did not fail the red pair (%s)" % verdict)

        p_s, _ = fr.median_L(shadow)
        p_g, _ = fr.median_L(stacked)
        if nums is not None:
            got = (round(p_s, 1), round(p_g, 1), round(p_g - p_s, 1))
            if any(abs(a - b) > 0.1 for a, b in zip(got, nums)):
                bad.append("1. AGREEMENT broken: probe %s vs gate %s" % (got, nums))

        # The probe must NAME the stacking, not just report the number.
        sdir = rdir / "slides"
        sdir.mkdir()
        (sdir / "slide-01.html").write_text(
            "<html><body data-contacts='%s'></body></html>"
            % json.dumps([{"what": "the fixture object", "shadow": [shadow],
                           "ground": [stacked]}]))
        out = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "contact_probe.py"),
             "--render-dir", str(rdir), "--slides-dir", str(sdir),
             "--verify", "--json"], capture_output=True, text=True)
        if out.returncode != 0:
            bad.append("--verify exited %d: %s" % (out.returncode, out.stderr[:300]))
        else:
            rec = json.loads(out.stdout)["slides"][0]
            joined = " ".join(rec.get("notes", []))
            if "different y" not in joined:
                bad.append("the probe did not name the stacked rects: %r" % joined)
            if "floor" not in joined:
                bad.append("the probe did not name the floor the pair misses: %r" % joined)
            m = rec.get("measured", {})
            if abs(m.get("trough_x", 0) - CAST_X) > 10:
                bad.append("--verify proposed a cast at x=%s, drawn at x=%s"
                           % (m.get("trough_x"), CAST_X))

        # 3. THE PROPOSAL, from the object's base and nothing else.
        rec = cp.propose(fr, BASE_X, BASE_Y)
        if "error" in rec:
            bad.append("proposal failed: %s" % rec["error"])
        else:
            if abs(rec["trough_x"] - CAST_X) > 10:
                bad.append("proposed cast at x=%.1f, drawn at x=%.1f"
                           % (rec["trough_x"], CAST_X))
            if rec["shadow"][0][1] != rec["ground"][0][1]:
                bad.append("proposed pair is not on one line: %s %s"
                           % (rec["shadow"], rec["ground"]))
            if rec.get("dL", 0) < cp.QA.CONTACT_WARN_DL:
                bad.append("proposed pair measures dL %s, under the comfort band"
                           % rec.get("dL"))
            nums, verdict, detail = qa_numbers(arr, rec["shadow"][0], rec["ground"][0])
            if nums is None or abs(nums[2] - rec["dL"]) > 0.1:
                bad.append("gate disagrees with the proposal: %s vs dL %s"
                           % (nums, rec.get("dL")))
            if verdict == "fail":
                bad.append("the gate FAILS the pair the probe proposed: %s" % detail)
            if min(rec["px"]) < 12:
                bad.append("proposed rects are too small for the gate: %s" % rec["px"])

    if bad:
        print("BROKEN")
        for b in bad:
            print(" - " + b)
        return 1
    print("HOLDS: the probe's numbers are the gate's numbers, the stacked-rect "
          "defect measures negative and is named, and a pair proposed from the "
          "object's base alone lands on the drawn cast and clears the gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
