"""Keep PR checks read-only without disabling independent scheduled writers.

These assertions intentionally cover the repository's block-style workflow
configuration, not arbitrary YAML. GitHub additionally validates YAML syntax.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITERS = {'power.yml': 'refresh', 'power-utility.yml': 'refresh',
           'docket-watch.yml': 'sweep'}
CONDITION = "github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'"


def check(text, writer):
    header, jobs = text.split('\njobs:\n', 1)
    assert re.search(r'^permissions:\n  contents: read\n', header, re.M)
    assert 'write-all' not in text
    blocks = re.split(r'^  ([a-zA-Z0-9_-]+):\n', jobs, flags=re.M)
    assert not blocks[0].strip()
    parsed = dict(zip(blocks[1::2], blocks[2::2]))
    assert writer in parsed
    for name, body in parsed.items():
        if name == writer:
            assert re.search(r'^    permissions:\n      contents: write\n', body, re.M)
            assert f'    if: {CONDITION}\n' in body
            assert not re.search(r'^    needs:', body, re.M)
            assert 'git push' in body
        else:
            assert not re.search(r'^    permissions:', body, re.M)
            assert not re.search(r'^    if:', body, re.M)
    assert len(re.findall(r'^\s*contents: write\s*$', text, re.M)) == 1


class CollectorPermissions(unittest.TestCase):
    def test_live_workflows(self):
        for filename, writer in WRITERS.items():
            with self.subTest(filename=filename):
                check((ROOT / '.github/workflows' / filename).read_text(), writer)

    def test_rejects_unsafe_and_broken_variants(self):
        for filename, writer in WRITERS.items():
            text = (ROOT / '.github/workflows' / filename).read_text()
            variants = [
                text.replace('permissions:\n  contents: read', 'permissions:\n  contents: write'),
                text.replace('  gate:\n', '  gate:\n    permissions:\n      contents: write\n'),
                text.replace(f'    if: {CONDITION}', '    if: always()'),
                text.replace(f'  {writer}:\n', f'  {writer}:\n    needs: gate\n'),
                text.replace('      contents: write', '      contents: read'),
            ]
            for variant in variants:
                with self.subTest(filename=filename, variant=variants.index(variant)):
                    with self.assertRaises(AssertionError):
                        check(variant, writer)


if __name__ == '__main__':
    unittest.main()
