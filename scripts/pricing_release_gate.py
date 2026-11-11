#!/usr/bin/env python3
"""Gate the exact Pages upload. Historical exceptions are fixed path/hash pairs."""
import argparse
import json
from pathlib import Path
import sys

from pricing_contract import POLICY, digest, load_policy, strict_json, verify_release

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'config/pricing_historical_baseline.json'
# This digest is fixed in the introducing change; never rebuild/expand the
# baseline from a PR head or treat an unchanged path alone as an exemption.
BASELINE_SHA256 = 'c38c6bc8c1c22d2e93af5fd36de09b431d19d97063b89fc53c81fc0b66ecba6d'


def check(root=ROOT):
    root = Path(root)
    policy_path = root / 'config/pricing_policy.json'
    load_policy(policy_path)
    try:
        raw = (root / 'config/pricing_historical_baseline.json').read_bytes()
    except OSError as error:
        raise ValueError('Missing immutable historical pricing baseline') from error
    if digest(raw) != BASELINE_SHA256:
        raise ValueError('Historical baseline changed; new offers may never be grandfathered')
    baseline = strict_json(raw)
    proposal_root = root / 'docs/awesomeproposal'
    if not proposal_root.is_dir() or proposal_root.is_symlink():
        raise ValueError('Missing proposal artifact root')
    failures, preserved, checked = [], [], []
    known = baseline['artifacts']
    current = {}
    for path in sorted(proposal_root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Proposal symlink rejected: ' + str(path))
        if path.is_file():
            current[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    # Deleting a historical page is a historical change too.
    for name in sorted(set(known) - set(current)):
        failures.append('Preserved historical artifact missing: ' + name)
    for name in sorted(set(known) & set(current)):
        if known[name] != current[name]:
            failures.append('Preserved historical artifact changed: ' + name)
    directories = {Path(name).parts[2] for name in current if len(Path(name).parts) >= 4}
    for name in current:
        if len(Path(name).parts) < 4:
            failures.append('Unrecognized proposal path: ' + name)
    for slug in sorted(directories):
        prefix = 'docs/awesomeproposal/' + slug + '/'
        files = {name: value for name, value in current.items() if name.startswith(prefix)}
        historic = {name: value for name, value in known.items() if name.startswith(prefix)}
        if files == historic and historic:
            preserved.append(slug)
            continue
        try:
            verify_release(proposal_root / slug, policy_path)
            checked.append(slug)
        except (ValueError, KeyError, TypeError, OSError) as error:
            failures.append(slug + ': ' + str(error))
    # Pricing manifests/markers outside the managed publication namespace are
    # never silently skipped. Other editorial pages have no offer contract.
    for path in (root / 'docs').rglob('*'):
        if path.is_symlink():
            continue
        if path.is_file() and not path.is_relative_to(proposal_root):
            if path.name == 'pricing-release.json' or (path.suffix.lower() in ('.html', '.htm')
                    and any(token in path.read_bytes() for token in (b'pricing-offer', b'offer-pricing'))):
                failures.append('Offer outside governed proposal namespace: ' + str(path.relative_to(root)))
    return dict(ok=not failures, policy_version=load_policy(policy_path)[0]['policy_version'],
                scope='Forward-looking release pricing only; preserved history is not certified compliant.',
                historical_unchanged=preserved, checked_current_offers=checked, failures=failures,
                known_historical_violations=baseline['known_violations'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = check(args.root)
    except (ValueError, KeyError, TypeError, OSError) as error:
        result = dict(ok=False, failures=[str(error)])
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
