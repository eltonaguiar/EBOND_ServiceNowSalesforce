---
agent: ebond-v2
domain: BESTPRACTICES
phase: 1
status: done
spans: [INTEGRATION, WORKFLOWS]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/lab_levels_beginner_path.md
  - path: 2026-11-16-SWARM/03_DONE/BESTPRACTICES/security_identity_secrets.md
  - verified_at: 2026-11-16T21:15:00Z
---

# Field ownership, system of record & manual edits

Once an integration is **bi-directional**, the hardest problems are not transport but **who owns which field**, **how to stop loops**, and **how to respect human edits**. This is the design model for the POC.

## 1. System-of-record matrix (recommended for the lab)

| Field | Owner | Policy |
|-------|-------|--------|
| Subject | Salesforce | Sync → SN `short_description`; SN never overwrites human edits here |
| Priority | Salesforce | Sync → SN `priority`/`urgency` |
| Account / Contact links | Salesforce | Sync → SN related fields |
| State (status) | ServiceNow | Sync → SF `Status`; SF does not overwrite |
| Assignment group | ServiceNow | Sync → SF (optional) |
| Resolution / Work notes | ServiceNow | Sync → SF Description/Resolution if mapped; otherwise SN-only |
| Description | **Shared** | Sync both ways **only** when last-modified is newer on the sender; otherwise skip. Use a source flag to break ties. |

## 2. Correlation IDs (the linchpin)

- ServiceNow stores the Salesforce **Case Id** (`correlation_id` or a custom field).
- Salesforce stores the ServiceNow **sys_id/number** (custom field).
- Every sync checks the key first: exists → **update**; missing → **create** and persist the key. This makes operations **idempotent** and prevents duplicate counterpart records on retry.

## 3. Loop prevention

- **Source flag:** on the receiving side set `u_synced_from_integration = true` (or equivalent) when writing from the integration; triggers skip records carrying that flag.
- **Timestamp comparison:** only propagate when the sender's `sys_updated_on` / `LastModifiedDate` is newer than the receiver's last-applied sync.
- **Delta only:** fire outbound triggers only when an owned field actually changed; ignore the update if mapped fields are unchanged (convergence guard).

## 4. Manual edits vs integration

- **Owned fields:** integration always wins (the owner's value propagates); human edits on non-owned fields are preserved.
- **Protected fields:** a field edited by a human after sync should not be blindly overwritten by the next integration push. Use last-modified comparison; if the human's edit is newer, keep it and log a conflict.
- **Conflict log:** write a row (error/conflict table) with the field, both values, timestamps, and resolution so there is an audit trail.
- **Explicit push:** where confusing, require a manual "push to ServiceNow/Salesforce" action or scheduled reconciliation rather than continuous auto-write.

## 5. Interaction with other best practices

- Secrets and identity: `security_identity_secrets.md`.
- Retries/idempotency (correlation key behavior): `reliability_retries_idempotency.md`.
- Values that don't map should log warnings (QA plan), never silently drop.
