"""Run the actual collector commit steps against a failing git transport."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


class PushTests(unittest.TestCase):
    def test_actual_workflows_fail_exhausted_pushes_and_rebase_conflicts(self):
        for workflow, job in [("power.yml", "refresh"), ("power-utility.yml", "refresh"),
                              ("docket-watch.yml", "sweep")]:
            doc = yaml.load((REPO / ".github/workflows" / workflow).read_text(), Loader=yaml.BaseLoader)
            script = next(s["run"] for s in doc["jobs"][job]["steps"] if s.get("name", "").startswith("Commit"))
            for success_on, conflict, expected_rc, attempts in [(99, False, 1, 4),
                                                               (2, False, 0, 2),
                                                               (99, True, 1, 1)]:
                with self.subTest(workflow=workflow, success_on=success_on, conflict=conflict), tempfile.TemporaryDirectory() as td:
                    root = Path(td)
                    fake_git = root / "git"
                    fake_git.write_text(f"#!{sys.executable}\n" + '''
import os, sys
from pathlib import Path
command = sys.argv[1]
if command == 'diff':
    sys.exit(1)
if command == 'push':
    counter = Path(os.environ['CRON_TEST_ATTEMPTS'])
    n = int(counter.read_text()) + 1 if counter.exists() else 1
    counter.write_text(str(n))
    sys.exit(0 if n >= int(os.environ['CRON_TEST_SUCCESS_ON']) else 1)
if command == 'pull' and os.environ['CRON_TEST_CONFLICT'] == 'yes':
    sys.exit(1)
''')
                    fake_git.chmod(0o755)
                    (root / "sleep").write_text("#!/bin/sh\nexit 0\n")
                    (root / "sleep").chmod(0o755)
                    env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"],
                               CRON_TEST_ATTEMPTS=str(root / "attempts"), CRON_TEST_SUCCESS_ON=str(success_on),
                               CRON_TEST_CONFLICT="yes" if conflict else "no")
                    run = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", script], cwd=root,
                                         env=env, capture_output=True, text=True, timeout=15)
                    self.assertEqual(run.returncode, expected_rc, run.stdout + run.stderr)
                    self.assertEqual(int((root / "attempts").read_text()), attempts)


if __name__ == "__main__":
    unittest.main()
