"""Canonical public pricing contract. Standard library only; no network or writes.

Producer vendors these exact bytes with a source commit/hash lock. A pricing
receipt is a mechanical check, never buyer approval or a retrospective verdict.
"""
from decimal import Decimal, InvalidOperation
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'config/pricing_policy.json'
VERSION = '2026-10-25.1'
EXPECTED_POLICY = {
    'schema_version': 1, 'policy_version': VERSION, 'currency': 'USD',
    'project_minimum_usd': 8000, 'business_retainer_minimum_monthly_usd': 8000,
    'below_minimum': 'reject_or_rescope',
    'third_party_costs': 'separate_from_business_retainer',
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate pricing field: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Nonfinite pricing value: ' + value)
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError('Malformed pricing JSON') from error


def load_policy(path=POLICY):
    try:
        raw = Path(path).read_bytes()
        policy = strict_json(raw)
    except OSError as error:
        raise ValueError('Missing pricing policy') from error
    if policy != EXPECTED_POLICY or any(type(policy[k]) is not type(v) for k, v in EXPECTED_POLICY.items()):
        raise ValueError('Unrecognized pricing policy; update the versioned contract explicitly')
    return policy, digest(raw)


def money(value):
    if type(value) not in (int, float):
        raise ValueError('Price must be a finite numeric USD amount')
    try:
        number = Decimal(str(value))
        if not number.is_finite() or number < 0 or number != number.quantize(Decimal('.01')):
            raise ValueError('Price needs finite nonnegative USD cents')
    except InvalidOperation as error:
        raise ValueError('Malformed USD amount') from error
    return number


def exact_keys(value, keys, name):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError('Unrecognized ' + name + ' pricing fields')


def validate_offer(offer, policy_path=POLICY):
    policy, _ = load_policy(policy_path)
    exact_keys(offer, ('policy_version', 'currency', 'project', 'business_retainer', 'third_party'), 'offer')
    if offer['policy_version'] != policy['policy_version'] or offer['currency'] != 'USD':
        raise ValueError('Offer must use the current pricing policy and USD')
    project = offer['project']
    exact_keys(project, ('mode', 'amount_usd'), 'project')
    if project['mode'] not in ('quote', 'floor'):
        raise ValueError('Unrecognized project pricing mode')
    if money(project['amount_usd']) < policy['project_minimum_usd']:
        raise ValueError('Project below USD 8,000 minimum; reject or rescope, never auto-inflate')
    retainer = offer['business_retainer']
    if retainer is not None:
        exact_keys(retainer, ('mode', 'amount_usd', 'interval', 'optional'), 'business retainer')
        if (retainer['mode'] not in ('quote', 'floor') or retainer['interval'] != 'month'
                or retainer['optional'] is not True):
            raise ValueError('Business retainer must be optional and monthly')
        if money(retainer['amount_usd']) < policy['business_retainer_minimum_monthly_usd']:
            raise ValueError('Business retainer below USD 8,000/month minimum; reject or rescope')
    if not isinstance(offer['third_party'], list):
        raise ValueError('Third-party costs must be a distinct list')
    labels = set()
    for row in offer['third_party']:
        exact_keys(row, ('label', 'amount_usd', 'interval', 'payer'), 'third-party')
        label = row['label']
        if (not isinstance(label, str) or not label.strip() or len(label) > 100
                or re.search(r'[$<>\r\n]|\b(?:retainer|care)\b', label, re.I)
                or label.casefold() in labels):
            raise ValueError('Third-party cost needs a distinct provider/service label, never a retainer')
        labels.add(label.casefold())
        money(row['amount_usd'])
        if row['interval'] not in ('month', 'year', 'one_time') or row['payer'] not in ('client', 'alaska_ai'):
            raise ValueError('Third-party cost needs an explicit billing interval and payer')
    return offer


def dollars(value):
    number = money(value)
    return '$' + (format(number, ',.0f') if number == number.to_integral() else format(number, ',.2f'))


def render_offer(offer, policy_path=POLICY):
    validate_offer(offer, policy_path)
    project = offer['project']
    if project['mode'] == 'quote':
        text = 'Project estimate: ' + dollars(project['amount_usd']) + ' USD.'
    else:
        text = ('Projects start at ' + dollars(project['amount_usd'])
                + ' USD. This is a minimum, not an exact quote; scope and price require agreement.')
    rows = ['<p data-price-kind="project">' + text + '</p>']
    retainer = offer['business_retainer']
    if retainer is not None:
        text = ('Optional business retainer: ' if retainer['mode'] == 'quote'
                else 'Optional business retainers start at ')
        text += dollars(retainer['amount_usd']) + ' USD/month.'
        if retainer['mode'] == 'floor':
            text += ' This is a minimum, not an exact quote.'
        rows.append('<p data-price-kind="business_retainer">' + text + '</p>')
    for row in offer['third_party']:
        interval = {'month': '/month', 'year': '/year', 'one_time': ' one time'}[row['interval']]
        payer = 'client' if row['payer'] == 'client' else 'Alaska AI'
        rows.append('<p data-price-kind="third_party">Third-party ' + html.escape(row['label'])
                    + ': ' + dollars(row['amount_usd']) + ' USD' + interval
                    + '; paid by ' + payer + '. Separate from any business retainer.</p>')
    data = canonical(offer).decode().replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return ('<section id="offer-pricing" data-policy-version="' + offer['policy_version']
            + '"><h2>Project pricing</h2>' + ''.join(rows) + '</section>'
            + '<script id="pricing-offer" type="application/json">' + data + '</script>')


class OfferHTML(HTMLParser):
    def __init__(self, markup=''):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.hidden = []
        self.text = []
        self.raw_offer = []
        self.in_offer = False
        self.markup = markup
        self.section_offsets = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        row = dict(attrs)
        if len(row) != len(attrs):
            raise ValueError('Duplicate HTML attributes in proposal')
        self.ids.append(row.get('id'))
        concealed = ('hidden' in row or 'inert' in row or row.get('aria-hidden') == 'true'
                     or bool(re.search(r'(?:display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?:\D|$))', row.get('style', ''), re.I))
                     or tag in ('head', 'template', 'script', 'style', 'noscript'))
        if row.get('id') == 'offer-pricing':
            if concealed or any(hidden for _, hidden in self.stack):
                raise ValueError('Pricing section must be visible in the proposal body')
            line, column = self.getpos()
            self.section_offsets.append(sum(len(s) for s in self.markup.splitlines(keepends=True)[:line - 1]) + column)
        if row.get('id') == 'pricing-offer':
            if tag != 'script' or row.get('type') != 'application/json':
                raise ValueError('Malformed embedded pricing offer')
            self.in_offer = True
        if tag in ('script', 'style'):
            self.hidden.append(tag)
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.stack.append((tag, concealed))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break
        if tag == 'script':
            self.in_offer = False
        if self.hidden and tag == self.hidden[-1]:
            self.hidden.pop()

    def handle_data(self, value):
        if self.in_offer:
            self.raw_offer.append(value)
        if not self.hidden:
            self.text.append(value)


OFFER_LABEL = r'(?:first[ -](?:stage|slice|release)(?:\s+estimate)?|project\s+(?:estimate|price|fee)|(?:build|implementation)\s+(?:estimate|price|fee)|pilot(?:\s+(?:estimate|price|fee))?|business\s+retainer|optional\s+care)'
LOW_OFFER = re.compile('(' + OFFER_LABEL + r')(?:[^$.;]{0,60}\$\s*|\s*:?\s*USD\s+)(\S+)', re.I)


def check_rendered(raw, offer, policy_path=POLICY):
    validate_offer(offer, policy_path)
    try:
        markup = raw.decode('utf-8') if isinstance(raw, bytes) else raw
        parsed = OfferHTML(markup)
        parsed.feed(markup)
        parsed.close()
        if parsed.ids.count('offer-pricing') != 1 or parsed.ids.count('pricing-offer') != 1:
            raise ValueError('Exactly one visible pricing section and embedded offer required')
        if strict_json(''.join(parsed.raw_offer)) != offer:
            raise ValueError('Rendered offer differs from structured offer')
        expected = render_offer(offer, policy_path)
        if (markup.count(expected) != 1 or len(parsed.section_offsets) != 1
                or not markup[parsed.section_offsets[0]:].startswith(expected)):
            raise ValueError('Rendered price/wording differs from the canonical visible offer')
        # Existing calculators may contain rates, costs and scenarios. A second
        # labeled project/care offer may not undercut the canonical offer.
        extra = OfferHTML()
        extra.feed(markup.replace(expected, '', 1))
        text = ' '.join(extra.text)
        for match in LOW_OFFER.finditer(text):
            label, token = match[1], match[2].rstrip('.,;:')
            if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d{1,2})?', token):
                raise ValueError('Unrecognized rendered offer price')
            amount = money(float(token.replace(',', '')))
            if amount < 8000:
                raise ValueError('Rendered proposal contains a below-minimum project or retainer')
            target = offer['business_retainer'] if re.search(r'retainer|care', label, re.I) else offer['project']
            if target is None or target['mode'] != 'quote' or amount != money(target['amount_usd']):
                raise ValueError('Additional rendered quote differs from the structured offer')
    except (UnicodeError, TypeError) as error:
        raise ValueError('Malformed rendered pricing') from error
    return offer


def pricing_receipt(raw, offer, policy_path=POLICY):
    check_rendered(raw, offer, policy_path)
    policy, policy_hash = load_policy(policy_path)
    return dict(version=1, scope='pricing_check_only', policy_version=policy['policy_version'],
                policy_sha256=policy_hash, offer_sha256=digest(canonical(offer)),
                artifact_sha256=digest(raw if isinstance(raw, bytes) else raw.encode()))


def verify_receipt(receipt, raw, offer, policy_path=POLICY):
    if receipt != pricing_receipt(raw, offer, policy_path):
        raise ValueError('Stale pricing receipt: artifact, offer or policy changed')
    return receipt


def artifact_files(directory):
    directory = Path(directory)
    result = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError('Proposal artifacts may not be symlinks')
        if path.is_file() and path != directory / 'pricing-release.json':
            result[path.relative_to(directory).as_posix()] = digest(path.read_bytes())
    return result


def release_manifest(directory, offer, policy_path=POLICY):
    validate_offer(offer, policy_path)
    files = artifact_files(directory)
    html_files = [name for name in files if Path(name).suffix.lower() in ('.html', '.htm')]
    if not html_files:
        raise ValueError('Release needs rendered HTML')
    checks = {name: pricing_receipt((Path(directory) / name).read_bytes(), offer, policy_path)
              for name in html_files}
    return dict(version=1, policy_version=offer['policy_version'], offer=offer,
                artifacts=files, checks=checks)


def verify_release(directory, policy_path=POLICY):
    try:
        rec = strict_json((Path(directory) / 'pricing-release.json').read_bytes())
    except OSError as error:
        raise ValueError('New or modified proposal needs pricing-release.json') from error
    exact_keys(rec, ('version', 'policy_version', 'offer', 'artifacts', 'checks'), 'release')
    expected = release_manifest(directory, rec['offer'], policy_path)
    if rec != expected:
        raise ValueError('Stale release receipt: exact artifact tree or pricing policy changed')
    return rec
