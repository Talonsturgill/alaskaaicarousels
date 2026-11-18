#!/usr/bin/env python3
"""A job that installs a Playwright browser runs on a pinned runner image.

WHY. On 2026-11-17 the scheduled headline collector (news.yml) failed at
"Install the pinned browser runtime" with "Playwright does not support
chromium on ubuntu26.04-x64": GitHub had moved ubuntu-latest to an image the
pinned Playwright versions (1.56.1, 1.49.1) do not know. A floating runner
under a pinned browser is a time bomb for every scheduled job that uses one.

RULE. Any job whose steps run `playwright install` or browser.sh must name an
explicit ubuntu-NN.NN runner, never ubuntu-latest. Exit 1 names each offender.
`--self-test` proves the rule fires on a reconstruction of the defect.
"""
import pathlib
import re
import sys

import yaml

BROWSER = re.compile(r"playwright install|browser\.sh")
PINNED = re.compile(r"^ubuntu-\d{2}\.\d{2}$")


def offenders(doc, name):
    out = []
    for job_id, job in (doc.get("jobs") or {}).items():
        steps = job.get("steps") or []
        text = "\n".join(str(s.get("run", "")) for s in steps if isinstance(s, dict))
        if not BROWSER.search(text):
            continue
        runner = str(job.get("runs-on", "")).strip()
        if not PINNED.match(runner):
            out.append(f"{name}:{job_id} installs a browser on runs-on '{runner}'; pin ubuntu-24.04")
    return out


def self_test():
    bad = yaml.safe_load("jobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - run: npx playwright install chromium\n")
    good = yaml.safe_load("jobs:\n  a:\n    runs-on: ubuntu-24.04\n    steps:\n      - run: bash .github/workflows/browser.sh 1.49.1\n")
    none = yaml.safe_load("jobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n      - run: python3 x.py\n")
    assert offenders(bad, "bad"), "floating runner under a browser install must fail"
    assert not offenders(good, "good"), "pinned runner must pass"
    assert not offenders(none, "none"), "jobs without a browser are out of scope"
    print("self-test OK")


def main():
    if "--self-test" in sys.argv:
        self_test()
        return 0
    root = pathlib.Path(__file__).resolve().parent.parent / ".github" / "workflows"
    found = []
    for f in sorted(root.glob("*.yml")):
        found += offenders(yaml.safe_load(f.read_text()) or {}, f.name)
    for line in found:
        print("FAIL", line)
    print(f"workflow runners: {'FAIL' if found else 'PASS'}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
