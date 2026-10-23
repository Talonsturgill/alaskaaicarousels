# CINGSA incident fixture

`2026-10-23-malformed.html` is the complete, unchanged HTTP 200 response from
[run 40012058262](https://github.com/Talonsturgill/alaskaaicarousels/actions/runs/40012058262/job/120614643660),
downloaded from [artifact 12526472936](https://github.com/Talonsturgill/alaskaaicarousels/actions/runs/40012058262/artifacts/12526472936).
`2026-10-23-source.json` is the original collector provenance, including its
parse failure, fetch time and SHA-256. The HTML retains its CRLF bytes and hash
`a36c4b616fb8a6670282d3f6770bb267abd6c0b15edac104cf9285b9aae4e905`.

The source defines Available Injection Capacity as Operating Injection Capacity
less nominations. Its cell contains literal `0]`, which is not a measurement.
The neighboring withdrawal cell is `123,033`. The separate inventory table
defines beginning and ending balances for the nomination day and reports
`7,725,313` and `7,682,346`. Neither inventory depends on that injection cell.

Collector contract from version 1.3: `verified` certifies fresh, validated
inventory, design volume and inventory change. Capacity cells are validated
independently against labeled columns and whole Mcf/d syntax. Invalid cells and
their dependent rates are null with `field_errors`; `data_status` is `partial`.
`fetch_status: ok` in the CINGSA block denotes a readable response, while the
source probe records `partial`, field errors and the response hash. Exit 5
retains verified storage while the workflow and live audit still report the
upstream defect. Stale storage remains unverified and unavailable.

The tests use the historical valid fixture in `gaswatch_collect.FIXTURE`, this
captured incident, and explicit mutations for hypothetical source changes.
They do not infer a replacement for `0]` or assert that upstream was repaired.
