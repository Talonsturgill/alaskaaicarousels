#!/usr/bin/env python3
"""Lossless inline membership encoding, exercised with the shipped decoder."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import ask_answers as aa


class Memberships(unittest.TestCase):
    def decode(self, value):
        source = (ROOT / 'scripts/site_build.py').read_text()
        start = source.index('  function expandMemberships(data)')
        end = source.index('  try { expandMemberships(DATA);', start)
        js = source[start:end] + '\nlet data=JSON.parse(require("fs").readFileSync(0,"utf8"));expandMemberships(data);console.log(JSON.stringify(data));'
        result = subprocess.run(['node', '-e', js], input=json.dumps(value), capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stderr)
        return json.loads(result.stdout)

    def test_real_record_memberships_are_lossless(self):
        original = aa.build()
        snapshot = copy.deepcopy(original)
        packed = aa.ship(original)
        restored = self.decode(packed)
        self.assertEqual(original, snapshot)
        for key in ('facets', 'views'):
            self.assertEqual(restored[key], original[key])
        legacy_size = len(json.dumps(dict(packed, facets=original['facets'], views=original['views']), separators=(',', ':')).encode())
        packed_size = len(json.dumps(packed, separators=(',', ':')).encode())
        self.assertGreater(legacy_size - packed_size, 10000)

    def test_legacy_numeric_strings_unknowns_order_and_duplicates(self):
        fixture = {'index': [{'id': 'long-id'}, {'id': '02'}],
                   'facets': {'a': [{'ids': ['02', 'long-id', 'unknown']}]},
                   'views': [{'ids': ['long-id', 'long-id']} ]}
        self.assertEqual(self.decode(fixture), fixture)
        restored = self.decode(aa.ship(fixture))
        del restored['membership_refs']
        self.assertEqual(restored, fixture)

    def test_invalid_refs_and_unknown_versions_fail(self):
        for ref in (-1, 2, 0.5, None, True):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                self.decode({'membership_refs': 1, 'index': [{'id':'a'}], 'views':[{'ids':[ref]}]})
        with self.assertRaises(ValueError):
            self.decode({'membership_refs': 2})

    def test_duplicate_ids_fail(self):
        with self.assertRaises(ValueError):
            aa.ship({'index':[{'id':'a'}, {'id':'a'}]})

    def test_synthetic_growth_roundtrips(self):
        rows = [{'id': 'synthetic-docket-item-%04d' % n} for n in range(1000)]
        fixture = {'index': rows, 'views': [{'ids':[r['id'] for r in rows]}], 'facets': {}}
        self.assertEqual(self.decode(aa.ship(fixture))['views'], fixture['views'])

if __name__ == '__main__':
    unittest.main()
