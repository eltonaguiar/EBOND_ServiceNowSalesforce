---
agent: ebond-v2
domain: TESTING
phase: 1
status: done
spans: [INTEGRATION, WORKFLOWS]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/WORKFLOWS/step_by_step_poc_incident_case_sync.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - verified_at: 2026-11-16T21:00:00Z
---

# QA test plan

Gateway: **fail-closed** — an undefined mapping or a non-2xx response must not silently pass.

## 1. Environment readiness

- [ ] SN instance reachable, admin login works.
- [ ] SF org reachable, login works.
- [ ] Integration users exist on both sides with least-privilege access.
- [ ] Connected App (SF) and REST message (SN) auth tests pass.

## 2. ServiceNow → Salesforce (Pattern A)

- [ ] Create Incident in SN → Case created in SF with correct mapped fields (Subject, Description, Priority, Status).
- [ ] SN record stores the returned SF Case `Id`.
- [ ] Creating a second Incident creates a separate Case (no collisions).
- [ ] Update on SN (priority change) updates the linked Case.
- [ ] Retry does **not** create a duplicate Case (idempotency).

## 3. Salesforce → ServiceNow (Pattern B)

- [ ] Create Case in SF → Incident created in SN with mapped fields.
- [ ] SF record stores the returned SN `sys_id`.
- [ ] Update Case in SF → linked Incident updates.
- [ ] Retry does **not** create a duplicate Incident.

## 4. Loop & convergence

- [ ] After a full create→update cycle the system settles (no runaway update loop).
- [ ] Mapped fields unchanged ⇒ no outgoing call (delta guard).

## 5. Error handling

- [ ] Invalid payload → recorded in error queue, no crash.
- [ ] Simulated 5xx/429 → retry with backoff, then escalate.
- [ ] Secret handling: no credentials in logs/payloads.

## 6. Data mapping completeness

- [ ] Every mapped field per `data_model_field_mapping.md` verified both directions.
- [ ] Unmapped values leave a logged warning.

## 7. Performance sanity

- [ ] API usage stays within DE org limits for the test run.
- [ ] No timeout/thread exhaustion during batched manual test (e.g. 20 records).

## Exit criteria

All checkboxes pass; error queue empty after the test suite; no secrets in repo/logs.
