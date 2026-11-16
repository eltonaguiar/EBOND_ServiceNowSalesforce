---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [INSTANCES, WORKFLOWS]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md
  - verified_at: 2026-11-16T20:45:00Z
---

# Data model & field mapping

The POC syncs **ServiceNow Incident** ⇄ **Salesforce Case**. This is the canonical mapping used by every pattern. Adjust field names to match your instance and the integration user's permissions.

## Object pair

| ServiceNow | Salesforce |
|-------------|------------|
| `incident` (Incident) | `Case` |

## Core field mapping

| ServiceNow field | Salesforce field | Direction | Notes |
|------------------|------------------|-----------|-------|
| `number` (INC0010001) | `CaseNumber` | read-only | System-generated on each side; correlate via id fields below |
| `short_description` | `Subject` | both | Title line |
| `description` | `Description` | both | Body |
| `priority` (1–5) | `Priority` | SN→SF | Map value sets below (1–5 → High/Medium/Low); `urgency` is a separate SN choice, not mapped here |
| `state` | `Status` | SN→SF | Map state enums (e.g. New/In Progress/Resolved → New/Working/Closed) |
| `assigned_to` | `OwnerId` | SN→SF | optional; may need user/owner mapping |
| `category` | `Type` | SN→SF | optional category fit |
| `sys_id` | `x_snc_ebond_sn_incident_id__c` | SN→SF | **Correlation key** on SF record |
| `x_snc_ebond_sf_case_id` | `Id` | SF→SN | **Correlation key** on SN record |

## Correlation keys (critical for sync)

To avoid duplicate/loop sync:

- Store the ServiceNow `sys_id` on the Salesforce record (custom field).
- Store the Salesforce `Id` on the ServiceNow record (custom field).
- All apps check the correlation key first: if it exists, **update** the existing counterpart; if not, **create** (and then persist the key). Correlation keys make operations **idempotent** (no duplicates on retry). They do **not** by themselves stop sync loops — apply the source-flag/delta guards in `step_by_step_poc_incident_case_sync.md` Phase 3 and `03_DONE/BESTPRACTICES/field_ownership_and_manual_edits.md`.

## Value-set mapping table (example)

| SN priority | SF priority |
|-------------|-------------|
| 1 – Critical | High |
| 2 – High | High |
| 3 – Moderate | Medium |
| 4 – Low | Low |
| 5 – Planning | Low |

| SN state | SF status |
|----------|-----------|
| New | New |
| In Progress | Working |
| On Hold | On Hold |
| Resolved | Closed |
| Closed | Closed |

## Notes

- Use **picklist/choice** matching; if a value doesn't map, log it (see best practices).
- Keep the mapping in one file so every pattern and the POC walkthrough reference the same source of truth.
- For the **field-ownership** and **manual-edit** policies that govern how this mapping is applied in both directions, see `03_DONE/BESTPRACTICES/field_ownership_and_manual_edits.md`.

## PDI correction (round 5)

`x_snc_ebond_sf_case_id` cannot be created on a free PDI. `x_snc_` is a ServiceNow vendor scope prefix, and a PDI cannot publish that scope. The runnable lab uses a global dictionary field instead:

| Side | Runnable field | Replaces |
|------|----------------|----------|
| ServiceNow incident | `u_ebond_sf_case_id` | `x_snc_ebond_sf_case_id` |
| Salesforce Case | `Snow_Sys_Id__c` (External Id, unique) | `x_snc_ebond_sn_incident_id__c` |

Keep the v3 names only if you later own a scope you can actually create. Do not hard-code `x_snc_ebond`.
