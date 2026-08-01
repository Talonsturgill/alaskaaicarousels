#!/usr/bin/env bash
# Pull every Alaska record from USAC E-Rate open data. No auth, no key, no rate limit hit
# at this volume. Re-runnable: USAC refreshes the source tables weekly.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p data
Y_FROM=${1:-2016}; Y_TO=${2:-2026}
api () { curl -sS --max-time 300 -G "https://opendata.usac.org/resource/$1.json" \
          --data-urlencode "\$where=$2" --data-urlencode "\$limit=50000" -o "$3"; }
for Y in $(seq "$Y_FROM" "$Y_TO"); do
  api hbj5-2bpj "state='AK' AND funding_year='$Y'"      "data/ak_$Y.json"     # line items
  api qdmp-ygft "state='AK' AND funding_year='$Y'"      "data/frn_$Y.json"    # provider + bids
  api tuem-agyq "org_state='AK' AND funding_year='$Y'"  "data/recip_$Y.json"  # who receives it
  api upfy-khtr "ben_state='AK' AND funding_year='$Y'"  "data/disc_$Y.json"   # discount, rural flag
  echo "  $Y done"
done
api 7i5i-83qf "physical_state='AK'" "data/entities_ak.json"                   # addresses
echo "all years fetched"
