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
| `priority` → `urgency` | `Priority` | SN→SF | Map value sets (e.g. 1..5 → High/Medium/Low) |
| `state` | `Status` | SN→SF | Map state enums (e.g. New/In Progress/Resolved → New/Working/Closed) |
| `assigned_to` | `OwnerId` | SN→SF | optional; may need user/owner mapping |
| `category` | `Type` | SN→SF | optional category fit |
| `sys_id` | `x_snc_ebond_sn_incident_id__c` | SN→SF | **Correlation key** on SF record |
| `x_snc_ebond_sf_case_id` | `Id` | SF→SN | **Correlation key** on SN record |

## Correlation keys (critical for sync)

To avoid duplicate/loop sync:

- Store the ServiceNow `sys_id` on the Salesforce record (custom field).
- Store the Salesforce `Id` on the ServiceNow record (custom field).
- All apps check the correlation key first: if it exists, **update** the existing counterpart; if not, **create** (and then persist the key). This makes the flow **idempotent** and prevents ping-pong loops.

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
