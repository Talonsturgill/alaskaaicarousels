# Forward-looking offer pricing

`pricing_policy.json` and `../scripts/pricing_contract.py` are the canonical
public contract, version `2026-10-25.1`. Leadflow vendors identical bytes with
an immutable source commit and SHA-256 lock. Neither side fetches or installs
dependencies at runtime. Updating this contract requires a deliberate version
change and synchronized producer pin, not a second pricing policy.

A project quote is at least USD 8,000. Optional business retainers are at least
USD 8,000 per month. Third-party hosting/pass-through charges have their own
amount, interval and payer and do not satisfy or inherit the retainer minimum.
The minimum is a floor, not a target. Reject/rescope smaller purchases; never
automatically increase a fee or inflate effort/value to pass. If an exact quote
is not justified, floor mode states "Projects start at" and that scope/price
still require agreement.

Every new offer uses this exact shape (no extra or inferred price fields):

```json
{
  "policy_version": "2026-10-25.1",
  "currency": "USD",
  "project": {"mode": "quote", "amount_usd": 8000},
  "business_retainer": null,
  "third_party": [
    {"label": "provider hosting", "amount_usd": 25, "interval": "month", "payer": "client"}
  ]
}
```

Use `render_offer(offer)` to produce the visible pricing section and embedded
JSON, then `release_manifest(directory, offer)` to generate pricing-release.json.
The manifest binds every public artifact and every HTML/HTM page to its offer,
policy version, policy bytes and exact render hash. A receipt is a mechanical
check only. It grants no buyer approval. New nested HTML, alternate filenames,
changed JavaScript, missing policy, stale receipts and unrecognized pricing fail.
Keep offer pages under docs/awesomeproposal; marked offers outside it fail.

The production gate runs unconditionally immediately before Pages configuration
and upload. It covers push, manual dispatch and workflow_run publication through
the same deploy job. The PR workflow also runs standard-library regressions and
the actual release gate. Workflow access/permissions and review settings are
unchanged. This does not prevent a privileged maintainer from changing/removing
the workflow; configuring repository protections is outside this patch.

`pricing_historical_baseline.json` freezes 64 existing public artifact paths and
SHA-256 hashes from hosting commit 3a6f3b8a3711d62e1cb33d22a32a48fc8a1f5ce4.
Its digest is fixed in the gate. It may never be expanded from a PR head. Any
changed/deleted historical file fails. New/modified offers receive no historical
exemption. An unrelated editorial release may preserve these exact historical
bytes, including the known Alyeska USD 5,796 and Tutka USD 2,760 violations. That
preservation is explicitly not pricing compliance, readiness or retrospective
approval. No historical page or email is rewritten.

Roll out only after owner review: verify these exact branch checks, merge the
hosting gate first, verify its real Pages check on the merged head, then pin
Leadflow to that verified canonical commit and merge the producer consumer.
Confirm one future approved export's exact manifest/HTML through PR pricing,
Pages pre-upload gate, live-byte verification and draft-readiness check. Never
use a sent offer or existing email as an acceptance fixture. A local test or a
draft PR alone is not enforcement or a rollout claim.

Limits: HTML checks validate canonical markup and typed pricing using a parser;
they do not execute arbitrary application JavaScript or prove browser-visible
CSS layout. Existing producer browser/reviewer gates remain required for actual
new delivery. New unmarked commercial pages outside the governed proposal
namespace are outside this pricing gate's classification; do not publish offers
there. Arbitrary external tools are not intercepted by producer code; the native
hook, supported CLIs, release gate and later readback enforce their own paths.
