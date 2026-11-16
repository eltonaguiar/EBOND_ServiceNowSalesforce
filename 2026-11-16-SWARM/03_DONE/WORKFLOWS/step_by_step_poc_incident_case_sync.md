---
agent: ebond-v2
domain: WORKFLOWS
phase: 1
status: done
spans: [INTEGRATION, TESTING, BESTPRACTICES]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_salesforce_outbound_to_sn.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - path: 2026-11-16-SWARM/03_DONE/TESTING/qa_test_plan.md
  - verified_at: 2026-11-16T20:50:00Z
---

# Step-by-step POC — Incident ⇄ Case sync

Goal: a new ServiceNow **Incident** creates a Salesforce **Case**; a Salesforce **Case** update flows back to the Incident. This walkthrough combines **Pattern A** (SN→SF) and **Pattern B** (SF→SN).

## Phase 0 — Prerequisites

- SN instance + SF org provisioned (see `03_DONE/INSTANCES/`).
- SF Connected App + integration user ready (Pattern A).
- SN scripted REST API + integration user ready (Pattern B).
- Correlation fields exist on both sides (see mapping doc).

## Phase 1 — ServiceNow → Salesforce

1. **Add correlation fields** on `incident`: `x_snc_ebond_sf_case_id` (string).
2. **Create the SF REST Message + auth** (Pattern A). Test with a manual POST to create a Case.
3. **Create a Flow**:
   - Trigger: *Incident created* (after-save).
   - Condition: `x_snc_ebond_sf_case_id` is empty.
   - Action: call REST message → create Case, mapped fields per mapping doc.
   - Action: set `x_snc_ebond_sf_case_id` = returned Case `Id`.
4. Save/activate.

## Phase 2 — Salesforce → ServiceNow

1. **Add correlation field** on `Case`: `x_snc_ebond_sn_incident_id__c` (custom field).
2. **Create Named Credential** `MyServiceNow` → `https://<instance>.service-now.com`.
3. **Create invocable Apex** callout (Pattern B) `createIncident` / `updateIncident`.
4. **Create a Record-Triggered Flow** on `Case`:
   - Trigger: Case created (or updated).
   - If `x_snc_ebond_sn_incident_id__c` is empty → call `createIncident`, store returned `sys_id`.
   - Else → call `updateIncident` with the existing `sys_id`.
5. Save/activate.

## Phase 3 — Prevent loops

The correlation key (Phase 1/2) prevents duplicates but does **not** stop feedback loops. Gate every write-back:

1. **Source flag** — add `u_synced_from_integration` on ServiceNow and an equivalent flag on Salesforce. Set it on every record written **by** the integration; exclude those records in both record-triggered triggers so integration writes do not re-fire.
2. **Timestamp compare** — write back only when the sender's `sys_updated_on` (SN) / `LastModifiedDate` (SF) is newer than the last applied sync.
3. **Owned-field delta** — fire outbound sync only when a field owned by the sending system changed (`data_model_field_mapping.md` + `field_ownership_and_manual_edits.md`); if no owned field changed, skip.
4. **Convergence test** — create→update in both directions and confirm the system settles (no repeated writes).

## Phase 4 — Run & verify

1. Create an Incident in SN → expect a Case in SF with mapped fields; SN stores the Case Id.
2. Update the Case in SF → expect the Incident's fields to reflect it.
3. Check the correlation keys are populated on both records.
4. Run the QA test plan (`2026-11-16-SWARM/03_DONE/TESTING/qa_test_plan.md`).

## Success criteria

- [ ] Incident → Case creation works.
- [ ] Case → Incident update works.
- [ ] No duplicate records on retry (idempotency).
- [ ] No sync loop (updates settle).
- [ ] No secrets in code/logs.
