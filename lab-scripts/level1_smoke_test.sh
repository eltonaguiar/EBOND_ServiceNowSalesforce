#!/usr/bin/env bash
# Level 1 smoke test — POST an Incident into the ServiceNow Table API.
# Best: run from a shell where you have exported your lab env vars
#   (see 2026-11-16-SWARM/03_DONE/INSTANCES/lab_environment_and_credentials.md).
set -euo pipefail

: "${SN_INSTANCE_URL:?Set SN_INSTANCE_URL (e.g. https://devXXXXXX.service-now.com)}"
: "${SN_ADMIN_USER:?Set SN_ADMIN_USER}"
: "${SN_ADMIN_PASSWORD:?Set SN_ADMIN_PASSWORD}"

BODY='{"short_description":"Lab Level 1 smoke test","description":"created via level1_smoke_test.sh","urgency":"2","impact":"2","category":"inquiry"}'

STATUS=$(curl -s -o /tmp/sn_lvl1_body.json -w '%{http_code}' \
  -u "$SN_ADMIN_USER:$SN_ADMIN_PASSWORD" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d "$BODY" \
  "$SN_INSTANCE_URL/api/now/table/incident")

echo "HTTP $STATUS"

if [ "$STATUS" != "201" ]; then
  echo "FAILED (expected 201). Response body:"
  cat /tmp/sn_lvl1_body.json
  exit 1
fi

python3 -c '
import json
d = json.load(open("/tmp/sn_lvl1_body.json"))
r = d["result"]
print("OK — created Incident", r["number"], "sys_id", r["sys_id"])
'
