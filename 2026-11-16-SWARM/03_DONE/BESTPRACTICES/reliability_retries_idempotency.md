---
agent: ebond-v2
domain: BESTPRACTICES
phase: 1
status: done
spans: [INTEGRATION]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md
  - verified_at: 2026-11-16T20:55:00Z
---

# Reliability — retries, idempotency, failure handling

## Retries

- On transient failures (5xx, timeouts, rate-limit 429) **retry with exponential backoff + jitter**.
- On 4xx (bad request/auth) fix the payload — do not blindly retry.
- Cap retries; escalate to an error queue after N attempts.
- Use async paths where possible: SN `RESTMessageV2.executeAsync()`, SF `Queueable`/scheduled path.

## Idempotency (critical)

- Never create a duplicate counterpart on retry. Use the **correlation keys** documented in `data_model_field_mapping.md`:
  - SF custom field `x_snc_ebond_sn_incident_id__c` stores the SN `sys_id`.
  - SN custom field `x_snc_ebond_sf_case_id` stores the SF `Id`.
- Pattern: lookup by correlation key → exists? *update* : *create* and persist the key.

## Sync-loop prevention

- Only propagate changes that originated on the other side or that satisfy a meaningful delta.
- Optionally use a "source" flag/field to mark records written by the integration, and skip triggers on those writes.
- Add a **convergence guard**: ignore updates that don't change mapped fields (compare before/after).

## Failure handling / error queue

- On final failure, write a retry/error row (e.g. a SN table or SF custom object) with: payload identifier, correlation key, error status, timestamp, retry count.
- Provide a scheduled job to retry the error queue.
- Alert on sustained failures (logs/dashboards).

## Timeouts & payload size

- Keep payloads small; paginate large pulls.
- Set explicit timeouts to avoid hanging threads.
- Follow platform limits (see `rate_limits_monitoring_logging.md`).
