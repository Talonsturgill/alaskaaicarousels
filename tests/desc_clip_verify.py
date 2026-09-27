#!/usr/bin/env python3
"""Does every deck page's meta description end on a complete thought? (2026-09-27)

Codex's review of PR #404 found `_desc_clip` returning a word cut when a
summary had neither a sentence end nor a late clause inside 155 characters:
2026-08-26 published "...that name none" and 2026-07-22 lost its closing
clause. The deck's hook is now the fallback. This holds that on the real
runs/ archive and on a synthetic case.

    python3 tests/desc_clip_verify.py        exit 0 HOLDS, exit 1 BROKEN
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import site_build as sb  # noqa: E402

END = (".", "?", "!")
bad = []
for r in sb.load_runs():
    d = sb._desc_clip(r.get("summary") or r["hook"], 155, fallback=r.get("hook"))
    if len(d) > 155 or not d.endswith(END):
        bad.append("%s: %r" % (r["date"], d[-70:]))
if sb._desc_clip("word " * 50, 155, fallback="A hook that reads whole.") != "A hook that reads whole.":
    bad.append("synthetic: a clause-less summary did not fall back to the hook")
if sb._desc_clip("Short and whole.", 155, fallback="Other.") != "Short and whole.":
    bad.append("synthetic: a summary that fits was replaced")
if bad:
    print("BROKEN")
    for b in bad:
        print(" - " + b)
    sys.exit(1)
print("HOLDS: every deck description ends on a complete thought within 155 characters")
