---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [BESTPRACTICES, WORKFLOWS]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_integrationhub_salesforce_spoke.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_salesforce_connect_external_objects.md
  - verified_at: 2026-11-16T20:45:00Z
---

# Integration architecture options

This is the decision core of the lab. You generally choose one primary **realtime** path plus optional **batch** backfill. All options below use only the free tiers and platform-native capabilities.

## Decision tree

```text
Need bidirectional sync between ServiceNow and Salesforce?
│
├─ Realtime, event-driven (record created/updated) →
│   ├─ ServiceNow → Salesforce :  REST Message (outbound) or Integration Hub spoke
│   └─ Salesforce → ServiceNow :  Flow/Apex callout or inbound scripted REST API
│
├─ Query-time federation (read-only, "live view") →
│   └─ Salesforce Connect external objects over ServiceNow OData
│
└─ Bulk / historical backfill →
    └─ Batch: ServiceNow import set / scheduled job, or SF bulk API
```

## Option comparison

| Option | Direction | Low-code? | Realtime? | Notes |
|--------|-----------|-----------|-----------|-------|
| **A. ServiceNow REST Message → SF REST API** | SN→SF | Scripted (RESTMessageV2) | ✅ | Full control; no extra licensing; needs a SF connected app + OAuth |
| **B. Salesforce Flow/Apex → SN REST API** | SF→SN | Flow (with Apex invocable for callout) | ✅ | Uses SF Named Credentials; SN exposes a scripted REST API |
| **C. Integration Hub + Salesforce spoke** | SN→SF (and back) | ✅ Very low-code | ✅ | Best for citizen devs; spoke availability/credential alias varies on dev instance |
| **D. Salesforce Connect external objects** | SF reads SN live | Partial (set up in SF) | Query-time | Read-only federation; good for reporting, not writes |
| **E. Batch (import sets / scheduled)** | Both | ✅ | ❌ | Best for backfill, not realtime |

## Recommended POC combo

Use **A + B** (bi-directional REST, fully under our control, minimal moving parts) as the primary lab path, with **C** documented as the low-code alternative and **D** as the read-only option. Document field mapping once (see `data_model_field_mapping.md`) and reuse it across patterns.

For a guided beginner route (Level 1→4: curl → Flow → Scripted REST → bi-directional), see `lab_levels_beginner_path.md`.

## Should you use an iPaaS instead?

Tools like Workato / MuleSoft / Zapier can host this integration with less code, but they are typically **not free** and add a third party. For a free, self-contained POC the platform-native REST + low-code paths are the most instructive and lowest-cost.
