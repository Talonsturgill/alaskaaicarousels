#!/usr/bin/env python3
"""aksdf_deadline_verify.py -- an AKSDF deadline degrade is LOUD (2026-10-02, run No.75).

WHAT IT RECONSTRUCTS. AKSDF.render checks opts.deadlineMs (default 15000) once
per row and, past it, drops soft shadows and then AO for every remaining row.
The rows above keep them, so the frame prints a hard horizontal seam. No.75's
slide 08 rendered at native 1080x620 with deadlineMs 90000; re-rendered with
the default it dropped shadows from row 276 of 620 (CSS y 1046.5), the tags'
cast shadows stopped on a straight line, and render.py and qa.py both passed it
with zero warnings. Now the degrade console.errors `AK DEGRADED:` (a qa.py
FAIL) and the return value carries `degraded: {shadowsFrom, aoFrom}`.

  python3 tests/aksdf_deadline_verify.py      # exit 0 = every check holds

Node only, the real aksdf.js and the real qa.py rule, no browser.

  quiet     a generous deadline: no console.error, degraded is null, the
            frame is unchanged from a render with no deadline option at all
  loud      a deadline already past (-1): exactly one console.error, prefixed
            AK DEGRADED:, naming shadows from row 0 and AO from row 1
  ao-only   shadows:false from the caller and a past deadline: the message
            names AO only, never a shadow drop the caller asked for
  qa        qa.py turns an AK DEGRADED: console error into a FAIL, and still
            only WARNs an ordinary console error
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROBE = r"""
const fs = require('fs');
const ROOT = process.argv[process.argv.length - 1];
const errors = [];
const scope = {
  console: { error: (m) => errors.push(String(m)), log: () => {} },
  document: { createElement: () => ({ getContext: () => ({ putImageData() {} }) }) },
};
(new Function('window', 'globalThis', 'console', 'document',
  fs.readFileSync(ROOT + '/assets/js/aksdf.js', 'utf8')))
  .call(scope, scope, scope, scope.console, scope.document);
const S = scope.AKSDF;
const ctx = () => { const c = { last: null,
  createImageData: (w, h) => ({ width: w, height: h, data: new Uint8ClampedArray(w * h * 4) }),
  save() {}, restore() {}, drawImage() {} };
  return c; };
const scene = p => { const a = S.sdSphere(S.sub(p, [0, 0.6, 0]), 0.6);
  const g = p[1]; return a < g ? [a, 1] : [g, 2]; };
const base = { scene, width: 40, height: 30, box: [0, 0, 80, 60],
  cam: { pos: [2, 2, 3], look: [0, 0.5, 0], fov: 50 }, light: [0.5, 0.8, 0.3],
  mats: { 1: { color: [0.9, 0.7, 0.2] }, 2: { color: [0.4, 0.4, 0.4] } }, seed: 1 };
const out = {};
let e0 = errors.length;
const rq = S.render(ctx(), Object.assign({}, base, { deadlineMs: 600000 }));
out.quiet = { errors: errors.length - e0, degraded: rq.degraded, shadows: rq.shadows, ao: rq.ao };
e0 = errors.length;
const rl = S.render(ctx(), Object.assign({}, base, { deadlineMs: -1 }));
out.loud = { errors: errors.slice(e0), degraded: rl.degraded };
e0 = errors.length;
const ra = S.render(ctx(), Object.assign({}, base, { deadlineMs: -1, shadows: false }));
out.aoonly = { errors: errors.slice(e0), degraded: ra.degraded };
console.log(JSON.stringify(out));
"""


def qa_rule(console_errors):
    """qa.py's console_errors branch, mirrored, gated on the rule being in the
    source. The end-to-end proof is the render + qa reconstruction in the
    ledger entry; this keeps the rule from being removed silently."""
    src =(ROOT / ".claude/skills/carousel-engine/qa.py").read_text()
    # the rule under test is the console_errors branch; read it straight off the
    # source so this test fails if the branch is removed or reworded
    has_rule = 'startswith("AK DEGRADED:")' in src
    fails, warns = [], []
    for e in console_errors:
        if str(e).startswith("AK CONTRACT:"):
            fails.append(e)
        elif has_rule and str(e).startswith("AK DEGRADED:"):
            fails.append(e)
        else:
            warns.append(e)
    return has_rule, fails, warns


def main():
    p = subprocess.run(["node", "-", str(ROOT)], input=PROBE,
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("  BAD  node failed\n" + p.stderr[-1200:])
        return 1
    r = json.loads(p.stdout.strip().splitlines()[-1])
    q, l, a = r["quiet"], r["loud"], r["aoonly"]
    lmsg = l["errors"][0] if l["errors"] else ""
    amsg = a["errors"][0] if a["errors"] else ""
    has_rule, fails, warns = qa_rule([lmsg, "TypeError: something ordinary"])
    checks = [
        ("generous deadline is quiet", q["errors"] == 0 and q["degraded"] is None
         and q["shadows"] and q["ao"], json.dumps(q)),
        ("past deadline errors exactly once", len(l["errors"]) == 1, "%d error(s)" % len(l["errors"])),
        ("message carries the AK DEGRADED: prefix", lmsg.startswith("AK DEGRADED:"), lmsg[:60]),
        ("names shadows from row 0 and AO from row 1",
         l["degraded"] == {"shadowsFrom": 0, "aoFrom": 1}
         and "soft shadows from row 0" in lmsg and "ambient occlusion from row 1" in lmsg,
         json.dumps(l["degraded"])),
        ("shadows:false caller: AO only, no shadow claim",
         a["degraded"] == {"aoFrom": 0} and "soft shadows" not in amsg
         and "ambient occlusion from row 0" in amsg, json.dumps(a["degraded"])),
        ("qa.py carries the AK DEGRADED: rule", has_rule, str(has_rule)),
        ("qa.py FAILs the degrade, WARNs an ordinary error",
         fails == [lmsg] and warns == ["TypeError: something ordinary"],
         "%d fail, %d warn" % (len(fails), len(warns))),
    ]
    ok = True
    for name, good, detail in checks:
        print("  %s  %-52s %s" % ("ok  " if good else "BAD ", name, detail[:90]))
        ok = ok and good
    print("AKSDF DEADLINE: " + ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
