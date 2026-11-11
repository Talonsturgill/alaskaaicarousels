"""Price boundaries, truthful floors, fail-closed rendering and stale receipts."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import pricing_contract as pricing


def offer(amount=8000, mode='quote'):
    return dict(policy_version=pricing.VERSION, currency='USD',
                project=dict(mode=mode, amount_usd=amount),
                business_retainer=None, third_party=[])


class PricingContractTests(unittest.TestCase):
    def test_historical_underpricing_rejected_without_inflation(self):
        for amount in (36 * 140 * 1.15, 2760, 0, 7999.99):
            with self.subTest(amount=amount):
                value = offer(amount)
                before = deepcopy(value)
                with self.assertRaisesRegex(ValueError, 'minimum'):
                    pricing.validate_offer(value)
                self.assertEqual(value, before)

    def test_minimum_is_not_a_target(self):
        for amount in (8000, 8000.01, 11500, 40000):
            value = offer(amount)
            self.assertIs(pricing.validate_offer(value), value)
            raw = pricing.render_offer(value).encode()
            self.assertEqual(pricing.check_rendered(raw, value), value)

    def test_floor_wording_never_claims_an_exact_quote(self):
        value = offer(mode='floor')
        rendered = pricing.render_offer(value)
        self.assertIn('Projects start at $8,000 USD', rendered)
        self.assertIn('minimum, not an exact quote', rendered)
        pricing.check_rendered(rendered, value)
        with self.assertRaises(ValueError):
            pricing.check_rendered(rendered + '<p>First slice estimate $8,000</p>', value)

    def test_optional_retainer_and_third_party_hosting_are_distinct(self):
        value = offer()
        value['third_party'] = [dict(label='provider hosting', amount_usd=25, interval='month', payer='client')]
        pricing.check_rendered(pricing.render_offer(value), value)
        value['business_retainer'] = dict(mode='quote', amount_usd=7999, interval='month', optional=True)
        with self.assertRaisesRegex(ValueError, 'retainer below'):
            pricing.validate_offer(value)
        for amount in (8000, 12000):
            value['business_retainer']['amount_usd'] = amount
            pricing.check_rendered(pricing.render_offer(value), value)
        value['business_retainer']['mode'] = 'floor'
        pricing.check_rendered(pricing.render_offer(value), value)
        value['third_party'][0]['label'] = 'business retainer hosting'
        with self.assertRaises(ValueError):
            pricing.validate_offer(value)

    def test_unknown_and_malformed_pricing_fails_closed(self):
        invalid = [None, {}, '8000', offer('8000'), offer(True), offer(float('nan')),
                   offer(float('inf')), offer(8000.001), offer(8000, 'starting-ish')]
        value = offer(); value['discount'] = 1000; invalid.append(value)
        value = offer(); value['currency'] = 'CAD'; invalid.append(value)
        value = offer(); value['policy_version'] = 'old'; invalid.append(value)
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    pricing.validate_offer(value)
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{broken'):
            with self.assertRaises(ValueError): pricing.strict_json(raw)

    def test_missing_changed_policy_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'policy.json'
            with self.assertRaisesRegex(ValueError, 'Missing'):
                pricing.validate_offer(offer(), path)
            policy = deepcopy(pricing.EXPECTED_POLICY); policy['project_minimum_usd'] = 100
            path.write_text(json.dumps(policy))
            with self.assertRaisesRegex(ValueError, 'Unrecognized'):
                pricing.validate_offer(offer(), path)

    def test_tampered_rendered_price_and_extra_offers_fail(self):
        value = offer()
        raw = pricing.render_offer(value)
        for changed in (raw.replace('$8,000', '$5,796'), raw.replace('$8,000', '$9,000'),
                        raw + '<p>First slice estimate $2,760</p>',
                        raw + '<p>Project fee $9,000</p>',
                        raw + '<p>Optional care $100/month</p>',
                        raw + '<p>Project fee USD 5,796</p>',
                        raw + '<p>Project fee $eight thousand</p>',
                        raw + '<p>Project fee $8k</p>',
                        raw + '<p>Project fee $8,000/month</p>',
                        raw + raw, raw.replace('pricing-offer', 'missing-offer')):
            with self.subTest(changed=changed[:80]):
                with self.assertRaises(ValueError): pricing.check_rendered(changed, value)
        for changed in ('<div hidden>' + raw + '</div>', '<template>' + raw + '</template>',
                        '<div style="display:none">' + raw + '</div>',
                        '<!--' + raw + '--><section id="offer-pricing">Wrong price</section>'
                        + '<script id="pricing-offer" type="application/json">' + pricing.canonical(value).decode() + '</script>'):
            with self.assertRaises(ValueError): pricing.check_rendered(changed, value)

    def test_receipt_binds_entire_html_offer_and_policy_bytes(self):
        value = offer(); raw = pricing.render_offer(value).encode()
        receipt = pricing.pricing_receipt(raw, value)
        pricing.verify_receipt(receipt, raw, value)
        with self.assertRaisesRegex(ValueError, 'Stale'):
            pricing.verify_receipt(receipt, raw + b'<!-- changed -->', value)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'policy.json'
            path.write_text(json.dumps(pricing.EXPECTED_POLICY))
            with self.assertRaisesRegex(ValueError, 'Stale'):
                pricing.verify_receipt(receipt, raw, value, path)
        altered = dict(receipt, policy_version='old')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            pricing.verify_receipt(altered, raw, value)

    def test_release_binds_every_artifact_and_every_html(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); value = offer()
            (root / 'index.html').write_text(pricing.render_offer(value))
            (root / 'app.js').write_text('// fictional artifact')
            manifest = pricing.release_manifest(root, value)
            (root / 'pricing-release.json').write_text(json.dumps(manifest))
            pricing.verify_release(root)
            (root / 'app.js').write_text('// changed artifact')
            with self.assertRaisesRegex(ValueError, 'Stale'): pricing.verify_release(root)
            (root / 'other.html').write_text('<p>Project fee $2,760</p>')
            with self.assertRaises(ValueError): pricing.release_manifest(root, value)


if __name__ == '__main__': unittest.main()
