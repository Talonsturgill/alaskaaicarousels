#!/usr/bin/env python3
"""reuse_census_verify.py -- render.scan_reuse and qa.reuse_census (2026-10-06,
weekly machine pass).

WHY. The flow critic named cause a, the same drawing on more than three frames,
across frames on 6 of 6 decks from September 30th to October 5th, and runs/
kept nothing a week could count it from. render.py now records each slide's
helper calls and the shape hash of each sizeable function; qa.py folds them into
machine_qa.json's `reuse` census. A RECORD, never a gate.

  python3 tests/reuse_census_verify.py      # exit 0 = every check holds

  copied    one drawing function pasted into five slides with different
            numbers, colours and comments hashes to ONE shape on five frames
  limit     a function on three frames and a helper on three frames are not
            listed (the limit is MORE than three)
  alias     a module helper is named by its file, whatever the slide binds it
            to, and THREE.* is never recorded
  plumbing  fitText, grainTile, AKPOST.grade, akthree.setup and the noise and
            colour primitives are left out
  real      today's deck (out/<date>/slides, when present) lists akhall.build,
            the 10,500-seat hall shared by frames 01, 02, 05 and 07
  record    the census never adds a fail or a warn: qa.py's totals are
            summed from the slide rows only
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / ".claude" / "skills" / "carousel-engine"
sys.path.insert(0, str(ENGINE))

COMB = """
// the spruce comb, slide {n}
function drawComb(cx, x0, y0) {{
  cx.strokeStyle = '{col}';
  for (let i = 0; i < {count}; i++) {{
    const x = x0 + i * {pitch}, h = 40 + 30 * Math.sin(i * 0.37) + AK.simplex2(i * 0.1, {n});
    cx.beginPath(); cx.moveTo(x, y0); cx.lineTo(x - 6, y0 - h * 0.6); cx.lineTo(x, y0 - h);
    cx.lineTo(x + 6, y0 - h * 0.6); cx.closePath(); cx.stroke();
    for (let k = 0; k < 9; k++) {{ cx.moveTo(x, y0 - k * h / 9); cx.lineTo(x + (k % 2 ? 7 : -7), y0 - k * h / 9 - 4); }}
  }}
  return {count};
}}
"""
ONCE = """
function seatRow(cx, r) {{
  let acc = 0;
  for (let s = 0; s < {n}0; s++) {{ acc += Math.cos(s * 0.1 + r) * 12.5 + Math.sin(s * 0.2) * 3.25;
    cx.fillRect(r * 4 + s * 3, 400 + Math.round(acc) % 40, 2, 2); cx.fillRect(r * 4 + s * 3 + 1, 402, 1, 1); }}
  return acc * {n};
}}
"""


def slide(n, comb=True, once=False, hall=True):
    body = ""
    if comb:
        body += COMB.format(n=n, col=["#123456", "#FFC72C", "#B0C4D0", "#2E363E", "#E4ECF2"][n % 5],
                            count=20 + n, pitch=7 + n * 0.5)
    if once:
        body += ONCE.format(n=n)
    mod = ""
    if hall:
        mod = ("const THREE = await import('@@ASSETS@@/js/three.module.min.js');\n"
               "const AKT = (await import('@@ASSETS@@/js/akthree.js')).init(THREE);\n"
               "const H%d = (await import('@@ASSETS@@/js/akhall.js')).init(THREE);\n"
               "H%d.build(R, {rows: [0, 69]}); new THREE.Mesh(); THREE.Vector3.prototype.set(0,0,0);\n"
               "AKT.setup(c, {}); AK.fitText(h, {}); AKPOST.grade(cx, {}); AKC.mixOklab('#000', '#fff', 0.5);\n" % (n, n))
    return ("<html><body><script src='@@ASSETS@@/js/noise.js'></script><script>" + body
            + "</script><script type='module'>window.renderReady = (async () => {\n" + mod
            + "})();</script></body></html>")


def main():
    from render import scan_reuse
    from qa import reuse_census
    checks = []
    # five slides: the comb on 1-5, the hall on 1-4 only, seatRow on 1-3 only
    recs = []
    for n in range(1, 6):
        html = slide(n, comb=True, once=n <= 3, hall=n <= 4)
        recs.append({"file": "slide-%02d.html" % n, "reuse": scan_reuse(html, "slide-%02d.html" % n)})
    recs.append({"file": "slide-06.html"})                       # an old record with no reuse field
    c = reuse_census(recs)
    fnames = {"/".join(f["names"]): f["slides"] for f in c["functions"]}
    calls = {h["call"]: h["slides"] for h in c["helpers"]}
    checks.append(("copied: one comb in five slides is one shape on five frames",
                   fnames.get("drawComb") == [1, 2, 3, 4, 5], str(fnames)))
    checks.append(("limit: a function on three frames is not listed", "seatRow" not in fnames, ""))
    checks.append(("alias: the hall is named by its file on four frames",
                   calls.get("akhall.build") == [1, 2, 3, 4], str(calls)))
    allcalls = {x for r in recs for x in (r.get("reuse") or {}).get("calls", [])}
    checks.append(("alias: THREE.* is never recorded",
                   not any(x.startswith(("THREE.", "three")) for x in allcalls), str(sorted(allcalls))))
    checks.append(("plumbing: setup, fitText, grade and colour mixing are left out of the census",
                   "akthree.setup" in allcalls and
                   not ({"akthree.setup", "AK.fitText", "AKPOST.grade", "AKC.mixOklab"} & set(calls)),
                   str(sorted(calls))))
    checks.append(("record: slides recorded counts only rows carrying the field", c["recorded"] == 5, str(c["recorded"])))
    # a helper on exactly three frames is not listed
    c3 = reuse_census(recs[:3])
    checks.append(("limit: the hall on three frames is not listed", "akhall.build" not in
                   {h["call"] for h in c3["helpers"]}, ""))
    today = sorted((ROOT / "out").glob("2026-10-06/slides/slide-*.html"))
    if today:
        rr = [{"file": p.name, "reuse": scan_reuse(p.read_text(), p.name)} for p in today]
        ct = reuse_census(rr)
        hall = {h["call"]: h["slides"] for h in ct["helpers"]}.get("akhall.build")
        checks.append(("real: No.79's hall helper on frames 01, 02, 05 and 07", hall == [1, 2, 5, 7], str(hall)))
    qa_src = (ENGINE / "qa.py").read_text()
    checks.append(("record: qa.py's totals are summed from the slide rows only",
                   'out["fails"] = sum(len(s["fails"]) for s in out["slides"])' in qa_src
                   and 'out["reuse"] = reuse_census(' in qa_src, ""))
    bad = 0
    for name, ok, detail in checks:
        print(("  ok   " if ok else "  BAD  ") + name + ("" if ok or not detail else ": " + detail[:300]))
        bad += 0 if ok else 1
    print("%d/%d checks hold" % (len(checks) - bad, len(checks)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
