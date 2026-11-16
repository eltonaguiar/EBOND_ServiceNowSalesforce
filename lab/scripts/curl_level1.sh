#!/usr/bin/env bash
set -euo pipefail
: "${SN_INSTANCE:?set SN_INSTANCE to https://devNNNNN.service-now.com}"
: "${SN_USER:?set SN_USER}"
: "${SN_PASSWORD:?set SN_PASSWORD}"

curl -sS -u "${SN_USER}:${SN_PASSWORD}" \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -X POST "${SN_INSTANCE}/api/now/table/incident" \
  -d '{"short_description":"Lab Level 1 - curl","description":"One-way Table API create.","urgency":"2","impact":"2","category":"inquiry"}'
echo
