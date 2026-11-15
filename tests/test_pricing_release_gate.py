"""Exercise actual release check against the immutable historical snapshot."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import pricing_contract as pricing
import pricing_release_gate as gate
from test_pricing_contract import offer


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'config').mkdir()
        for name in ('pricing_policy.json', 'pricing_historical_baseline.json'):
            shutil.copyfile(ROOT / 'config' / name, self.root / 'config' / name)
        shutil.copytree(ROOT / 'docs/awesomeproposal', self.root / 'docs/awesomeproposal')

    def new_offer(self, slug='fictional-new-offer', amount=8000):
        directory = self.root / 'docs/awesomeproposal' / slug
        directory.mkdir()
        value = offer(amount)
        (directory / 'index.html').write_text(pricing.render_offer(value))
        manifest = pricing.release_manifest(directory, value)
        (directory / 'pricing-release.json').write_text(json.dumps(manifest))
        return directory

    def test_historical_violations_are_preserved_without_ready_claim(self):
        result = gate.check(self.root)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['checked_current_offers'], [])
        self.assertEqual({v['project_usd'] for v in result['known_historical_violations']}, {5796, 2760})
        self.assertIn('not certified compliant', result['scope'])

    def test_new_path_without_contract_is_blocked(self):
        directory = self.root / 'docs/awesomeproposal/future-unknown-path/demo'
        directory.mkdir(parents=True)
        (directory / 'index.html').write_text('<p>First slice $2,760</p>')
        result = gate.check(self.root)
        self.assertFalse(result['ok'])
        self.assertIn('future-unknown-path', ' '.join(result['failures']))

    def test_new_compliant_offer_and_unrelated_release_pass(self):
        self.new_offer(amount=12000)
        (self.root / 'docs/editorial.html').write_text('<p>Unrelated editorial update</p>')
        result = gate.check(self.root)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['checked_current_offers'], ['fictional-new-offer'])

    def test_changed_new_render_or_missing_receipt_blocked(self):
        directory = self.new_offer()
        (directory / 'index.html').write_text((directory / 'index.html').read_text().replace('$8,000', '$5,796'))
        self.assertFalse(gate.check(self.root)['ok'])
        (directory / 'pricing-release.json').unlink()
        self.assertFalse(gate.check(self.root)['ok'])

    def test_historical_change_delete_and_baseline_expansion_blocked(self):
        baseline = json.loads((self.root / 'config/pricing_historical_baseline.json').read_text())
        path = self.root / baseline['known_violations'][0]['path']
        raw = path.read_bytes(); path.write_bytes(raw + b'<!-- changed -->')
        result = gate.check(self.root)
        self.assertFalse(result['ok']); self.assertIn('historical artifact changed', ' '.join(result['failures']))
        path.unlink()
        self.assertFalse(gate.check(self.root)['ok'])
        path.write_bytes(raw)
        baseline['artifacts']['docs/awesomeproposal/future/index.html'] = '0' * 64
        (self.root / 'config/pricing_historical_baseline.json').write_text(json.dumps(baseline))
        with self.assertRaisesRegex(ValueError, 'baseline changed'): gate.check(self.root)

    def test_missing_policy_and_extra_html_blocked(self):
        directory = self.new_offer()
        (directory / 'another.htm').write_text('<p>Unrecognized offer</p>')
        self.assertFalse(gate.check(self.root)['ok'])
        (self.root / 'config/pricing_policy.json').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'): gate.check(self.root)

    def test_real_pages_upload_has_unconditional_gate_before_upload(self):
        workflow = (ROOT / '.github/workflows/pages.yml').read_text()
        step = workflow.index('run: python3 scripts/pricing_release_gate.py')
        self.assertLess(step, workflow.index('uses: actions/upload-pages-artifact@v3'))
        self.assertNotIn('continue-on-error', workflow[:step])
        self.assertNotIn('if:', workflow[workflow.index('- name: Enforce proposal pricing'):step])


if __name__ == '__main__': unittest.main()
