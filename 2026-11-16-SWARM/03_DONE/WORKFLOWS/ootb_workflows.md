---
agent: ebond-v2
domain: WORKFLOWS
phase: 1
status: done
spans: [INTEGRATION]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md
  - path: 2026-11-16-SWARM/03_DONE/WORKFLOWS/step_by_step_poc_incident_case_sync.md
  - verified_at: 2026-11-16T20:50:00Z
---

# Out-of-the-box workflows

ServiceNow and Salesforce both ship event-driven automation that can *trigger* the integration patterns. This note lists the OOTB triggers/behaviors you use without building custom frameworks.

## ServiceNow (Flow Designer) OOTB triggers

| Trigger | Use |
|---------|-----|
| **Record Created / Updated / Deleted** (table) | Fire a flow when an Incident (or any table) changes → call Pattern A/C outbound. |
| **Schedule** (cron) | Periodic reconciliation/backfill batch. |
| **REST API trigger** | Expose a scripted REST API so Salesforce can call in (Pattern B inbound). |
| **Integration Hub spokes** | Pre-built actions (e.g. Salesforce spoke) inside a flow. |
| **Events / gs.eventQueue** | Asynchronous fan-out for reliability. |

## Salesforce OOTB automation

| Automation | Use |
|------------|-----|
| **Record-Triggered Flow** (after-save) | Fire when a Case changes → call Pattern B outbound. |
| **Flow (screen/autolaunched)** | Manual or scheduled orchestrations. |
| **Apex triggers / invocable Apex** | Callout logic (Pattern B) reached from a Flow. |
| **Scheduled paths / queueable** | Asynchronous processing, retries, debouncing. |
| **Named Credentials** | Safe outbound HTTP callouts (Pattern B). |

## "Bonding" with OOTB (no custom framework)

1. Use **record-triggered flows** on both sides as the event source.
2. Use **REST** (scripted API on SN, Named Credential callout on SF) as the transport.
3. Use **correlation fields** to keep the two records linked and idempotent.
4. Use **retries + logging** (an error table / debug logs) instead of a bespoke message bus.

This combination is fully OOTB + minimal code and is exactly what the POC walkthrough implements.

## When you'd add more

- If you need guaranteed delivery/queuing at scale, you'd add either the **ECC queue/MID** pattern (on-prem) or a resilient republish job. For this cloud-to-cloud POC, record-triggered flows + retries are sufficient.
