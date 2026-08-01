# What Alaska schools pay for internet

An open, reproducible price check on every school and library internet circuit in
Alaska, built from federal E-Rate filings that are public and that almost nobody reads.

**Headline, funding year 2026.** A 100 Mbps dedicated internet circuit costs a median
of **$1,975/month** at a USAC-flagged Urban site and **$70,000/month** at a Rural one.
Same bandwidth, same year, same service class. **35x.** Satellite service is filed in
39 of those same rural communities at **$1,800/month**.

Statewide this is **$197,482,402 a year** of pre-discount billing across 644 circuits,
205 communities and 25 providers.

## Why it matters

Federal rule **47 CFR 54.511(b)** already prohibits a provider from charging a school
more than its "lowest corresponding price" to a similarly situated non-residential
customer. The FCC's first enforcement action under that rule, against AT&T/BellSouth in
2016, concerned districts charged **400-500%** above the lowest available rate. And in
*Wisconsin Bell v. United States ex rel. Heath* (decided 9-0 on 21 February 2025) the
Supreme Court held that E-Rate reimbursement requests are claims under the False Claims
Act, in a case about overcharging schools.

The honest catch: LCP needs a *similarly situated* customer to compare against, and in a
village with one seller that customer may not exist. That is a market-structure problem,
not a paperwork one. What changed is that satellite now supplies a comparator.

## Run it

```bash
./fetch.sh              # pull all Alaska records from USAC (no auth needed)
python3 pipeline.py     # -> circuits_v2.csv, one row per circuit-recipient
python3 test_pipeline.py  # 19 assertions incl. an external reconciliation
python3 bundle.py       # -> build/bundle2.json for the web page
```

Only dependency is Python 3 standard library. `fetch.sh` needs `curl`.

## Method, in one paragraph

Five USAC tables are joined so a district's bill lands on the village that actually
holds the circuit, not the hub town it bills from: FRN line items (price, speed),
FRN status (provider, bid count, contract date), recipients of service (which school),
discount calculations (discount rate, USAC's own Rural/Urban flag), and supplemental
entity information (physical city). Price per megabit is computed **per circuit** --
unit monthly cost divided by speed -- so a six-school district stays comparable to a
one-school district. Communities are geocoded against the US Census place gazetteer.

## The six traps

Each of these silently produces a wrong answer. They are handled in `pipeline.py` and
asserted in `test_pipeline.py`.

| # | Trap | Consequence if missed |
|---|------|----------------------|
| 1 | `total_monthly_cost` is a **per-unit** cost, not the bill | understates multi-site districts by up to 6x |
| 2 | Every line item is published **twice** (Original + Current) | 6,156 of Alaska's 6,706 duplicate; naive sums double the state's bill |
| 3 | `monthly_quantity = 0` marks **one-time equipment** | 3,380 Alaska rows have no bandwidth and must not price per megabit |
| 4 | Not every circuit is **internet** | Saint Mary's buys 100 Mbps of transit for $75,000/mo *and* a 10 Gbps campus loop for $900/mo. Both file as "Fiber"; only `purpose` separates them |
| 5 | Not every circuit is the same **product** | Wrangell's schools buy dedicated Ethernet, its library a shared cable modem. Comparing them would be dishonest |
| 6 | The **outlier filter** (not in the data -- in the literature) | published K-12 broadband research drops circuits above $150/Mbps as implausible. In rural Alaska that is near the median, so national method silently deletes the problem. Nothing is dropped here |

Traps 4 and 5 were each found by verifying a headline before publishing it, and each
would have produced a genuinely misleading claim.

## The check that says it is right

Lower Kuskokwim School District's circuits, summed from these line items and annualised,
come to **$101,040,000**. Its contract has been independently reported at about
**$101 million a year**. `test_pipeline.py` asserts that match on every run, so if USAC
changes the feed the tests fail loudly instead of quietly publishing a wrong number.

## Limits

Pre-discount billed amounts, not districts' net cost -- E-Rate reimburses 60-90% -- but
this *is* what the federal program pays out. Schools and libraries only, not households.
Circuit-to-recipient matching is complete for FY2023-2026, so per-community figures are
FY2026 while the trend uses all years. Where a circuit serves several sites, dollars
split by USAC's own allocation where present and evenly otherwise. A peer benchmark is
withheld where fewer than three comparable circuits exist. And a high price is not proof
of a bad deal: a village with no fibre has no cheaper dedicated option to buy.

One further caution, stated because it cuts against the finding: where a single provider
holds most of a comparison cell, the peer median simply reflects that provider's price,
so matching the median is not evidence a price is competitive.

## Sources

All public, no authentication.

- USAC E-Rate open data — `opendata.usac.org` (tables `hbj5-2bpj`, `qdmp-ygft`, `tuem-agyq`, `upfy-khtr`, `7i5i-83qf`)
- US Census place gazetteer, Alaska
- State of Alaska community geodata
- 47 CFR 54.511 — Ordering services
- Prior art: **Connect K-12** (Connected Nation and Funds For Learning), which covers
  district bandwidth nationally against the FCC 1 Mbps-per-student goal. This work is
  narrower and deeper: one state, village level, with the provider named.
