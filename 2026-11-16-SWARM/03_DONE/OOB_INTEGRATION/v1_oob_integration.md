---
agent: v1-bond-lab
domain: OOB_INTEGRATION
phase: 1
status: done
spans: [CUSTOM_INTEGRATION, SECURITY]
evidence:
  - path: docs/02-out-of-box-integration.md
    verified_at: 2026-11-16T20:30:00Z
  - url: https://docs.servicenow.com/bundle/washingtondc-integrate-applications/page/administer/integrationhub/concept/integrationhub.html
    verified_at: 2026-11-16T20:30:00Z
  - url: https://docs.servicenow.com/bundle/washingtondc-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html
    verified_at: 2026-11-16T20:30:00Z
---

# OOB_INTEGRATION — out-of-box methods

Deliverable: `docs/02-out-of-box-integration.md`.

## What was done

- Catalogued ServiceNow OOB tools (Table API, Scripted REST, REST/SOAP Message, Flow Designer + IntegrationHub, Service Graph Connector, Import Sets, Remote Tables, MID Server) and Salesforce OOB tools (Named Credentials, External Services, Platform Events, Change Data Capture, Salesforce Connect, Outbound Message, Remote Site Settings).
- Added a **decision framework** (direction → trigger → latency) and a **method-selection matrix** for both directions.
- Included a zero-code **smoke test** for both directions (`curl` to Table API; REST Message to `sobjects/Case`).

## Key decisions / rationale

- **IntegrationHub spokes treated as optional** — the Salesforce spoke may not be entitled on a PDI, so the lab's guaranteed path is a plain REST Message + OAuth, with the spoke documented as the "if entitled" upgrade.
- **MID Server explicitly excluded** — pure cloud-to-cloud needs no MID Server; this is a common interview/design misconception, called out in the decision flow.

## Open items for review

- Confirm whether a current PDI ships the Salesforce spoke.
- Consider whether "Service Graph Connector for Salesforce" deserves its own lab section in a later round.
