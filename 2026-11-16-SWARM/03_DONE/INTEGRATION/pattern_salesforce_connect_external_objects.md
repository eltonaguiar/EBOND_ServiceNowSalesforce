---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [BESTPRACTICES]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md
  - url: https://developer.salesforce.com/docs/atlas.en-us.222.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_extobj_intro.htm
  - verified_at: 2026-11-16T20:45:00Z
---

# Pattern D — Salesforce Connect external objects (read-only federation)

**Salesforce Connect** lets Salesforce query external data live via an **OData** adapter — here, ServiceNow's OData endpoint — and expose it as **external objects** without copying data.

## What you get

- A "live view" of ServiceNow tables (e.g. Incidents) inside Salesforce.
- Excellent for reports/dashboards that always reflect the latest ServiceNow data.
- Read-only for the POC (writes require custom sync; not the point of this pattern).

## Setup

1. On ServiceNow, enable **OData** (the platform exposes OData via the **Integration → Hub** or the **OData** endpoint; typically `https://<instance>.service-now.com/api/now/odata/...`). Enable the `OData` feature and ensure the integration user has read access.
2. In Salesforce, create an **External Data Source** (type = OData 4.0) pointing at the ServiceNow OData URL with the service account credentials.
3. **Validate & Sync** the external data source to define **External Objects** (each maps to a ServiceNow table like `incident`).
4. Create external objects as normal (they read through — source). You can then build Lightning reports/list views over them.

## When to use

- You primarily need ServiceNow data *visible inside Salesforce* for reporting, without maintaining a copy.
- You want minimal integration code.

## Caveats

- Not for write-back.
- Performance depends on the OData endpoint and query patterns; keep external queries targeted.
- Not a substitute for realtime bidirectional sync.

## Verify

- [ ] External object lists ServiceNow incidents.
- [ ] A Salesforce report aggregates external object data.
- [ ] ServiceNow-side OData/permissions are limited to the integration user.
