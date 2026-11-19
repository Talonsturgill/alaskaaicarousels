#!/usr/bin/env python3
"""Reconstruction for aggregate_check's clock_duration and sum kinds (No.118,
2026-11-18). A right declaration must pass and each wrong one must FAIL:
a duration that ignores the time zone, a clock time its claim never carries,
and a sum that does not add up."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import aggregate_check as A

claims = {
    "C13": {"claim": "The order came out at 11:54 a.m. Alaska time on November 13th.", "value": "11:54 a.m.", "verbatim": "The order came out at 11:54 a.m. AKST."},
    "C20": {"claim": "The FAA lifted the ground stop at 8:15 p.m. Eastern time.", "value": "8:15 p.m. ET", "verbatim": "lifted the ground stop at 8:15 p.m. ET Friday."},
    "C16": {"claim": "670 flights sent back.", "value": "670 flights"},
    "C17": {"claim": "157 flights redirected.", "value": "157 flights"},
}
def run(decl):
    f, w = [], []
    A.verify(decl, claims, f, w)
    return f
base = {"slide": 1, "text": "For 261 minutes, no flight left Alaska.", "kind": "clock_duration",
        "from": {"claim": "C13", "time": "11:54 a.m.", "utc_offset": -9},
        "to": {"claim": "C20", "time": "8:15 p.m.", "utc_offset": -5}}
cases = [
    ("right clock duration passes", dict(base, n=261), False),
    ("time zone ignored fails", dict(base, n=501), True),
    ("invented endpoint fails", dict(base, n=261, to={"claim": "C20", "time": "4:15 p.m.", "utc_offset": -9}), True),
    ("right sum passes", {"slide": 3, "kind": "sum", "text": "827 flights", "members": ["C16", "C17"], "n": 827}, False),
    ("wrong sum fails", {"slide": 3, "kind": "sum", "text": "830 flights", "members": ["C16", "C17"], "n": 830}, True),
]
bad = 0
for name, decl, should_fail in cases:
    failed = bool(run(decl))
    ok = failed == should_fail
    bad += not ok
    print(("PASS " if ok else "FAIL ") + name)
sys.exit(1 if bad else 0)
