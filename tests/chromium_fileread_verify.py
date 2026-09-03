#!/usr/bin/env python3
"""chromium_fileread_verify.py -- the reconstruction behind launch_chromium's
file:// capability probe (2026-09-02).

WHAT IT RECONSTRUCTS. The SKILL contract documents
`fetch("@@ASSETS@@/geo/alaska-state.geo.json")` as the way a slide gets a map,
and a chrome-headless-shell refuses that fetch even with
--allow-file-access-from-files, while the full browser honours it. The 2026-08-27
fix ordered the candidate list full-binary-first, which is right and is not
enough: Playwright 1.57 stopped shipping Chromium and now manages Chrome for
Testing, headless as chrome-headless-shell
(https://playwright.dev/docs/release-notes). When a container refresh moves the
binaries out from under the `chromium-*` glob, the ordering has nothing left to
order and the fallback returns the shell. That failure is silent: the browser
launches, the page loads, every gate is green, and only the geodata is gone.

So launch_chromium now PROBES the capability instead of assuming it from the
path, and this file proves both halves on the machine it runs on.

  python tests/chromium_fileread_verify.py       # exit 0 = the probe holds

  1. the shell on this box really does refuse a file:// fetch  (the defect)
  2. the full browser really does allow it                     (the control)
  3. _can_read_disk answers no to 1 and yes to 2               (the probe)
  4. launch_chromium returns a browser that passes the probe   (the wiring)
"""

import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "carousel-engine"))

from playwright.sync_api import sync_playwright              # noqa: E402
from render import CHROMIUM_ARGS, _can_read_disk, launch_chromium   # noqa: E402

SHELL_PATS = ["/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell",
              "/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/"
              "chrome-headless-shell",
              "/opt/pw-browsers/chrome-headless-shell-*/chrome-headless-shell-linux64/"
              "chrome-headless-shell"]
FULL_PATS = ["/opt/pw-browsers/chromium-*/chrome-linux/chrome",
             "/opt/pw-browsers/chrome-*/chrome-linux64/chrome"]


def first(pats):
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[0]
    return None


def main():
    shell, full = first(SHELL_PATS), first(FULL_PATS)
    ok = True
    with sync_playwright() as p:
        if full is None:
            print("  SKIP no full browser on this machine; nothing to control against")
            return 0
        b = p.chromium.launch(executable_path=full, args=CHROMIUM_ARGS)
        got, why = _can_read_disk(b)
        print("  %s full browser %s -> %s" % ("ok  " if got else "BAD ", full, why))
        ok &= got
        b.close()

        if shell is None:
            print("  note: no headless shell on this machine, defect half not "
                  "reproducible here (the probe is still what protects the run)")
        else:
            b = p.chromium.launch(executable_path=shell, args=CHROMIUM_ARGS)
            got, why = _can_read_disk(b)
            print("  %s headless shell %s -> %s"
                  % ("ok  " if not got else "BAD ", shell, why))
            ok &= not got
            b.close()

        b = launch_chromium(p)
        got, why = _can_read_disk(b)
        print("  %s launch_chromium picked a browser that reads the disk (%s)"
              % ("ok  " if got else "BAD ", why))
        ok &= got
        b.close()

    print("\nfile:// capability probe: %s" % ("HOLDS" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
