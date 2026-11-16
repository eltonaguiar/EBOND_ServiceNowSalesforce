# IMPLEMENTATION_STEPS — ServiceNow ⇄ Salesforce Free Integration Lab

Ordered steps to reproduce/execute the lab (this round documents the content; live-instance execution is the reader's path in `docs/05`).

1. **Provision instances** — ServiceNow PDI (`developer.servicenow.com`) + Salesforce Developer org (`developer.salesforce.com/signup`). → `docs/01`
2. **Level 1** — `curl`/Postman POST to `/api/now/table/incident`; confirm 201 + Incident in list. → `docs/03`
3. **Level 2** — Salesforce External Credential (Custom auth) → Named Credential → Permission Set → Record-Triggered Flow (HTTP Callout). → `docs/03`
4. **Level 3** — ServiceNow Scripted REST API `create_incident` with validation + `u_correlation_id` upsert. → `docs/04`
5. **Level 4a** — Salesforce Connected App + Named Credential (OAuth) + Apex `IncidentSyncService` + trigger (loop guard). → `docs/05`
6. **Level 4b** — ServiceNow OAuth provider + OAuth client profile + REST Message `Salesforce Case API` + Business Rule (loop guard). → `docs/05`
7. **Verify** — run the end-to-end + negative checks E1–E7. → `docs/07`
8. **Harden** — walk the pre-flight security checklist. → `docs/06`
9. **Publish** — merge to `main`; confirm Pages deploy; then execute the TSOM cross-cutting link PR. → `03_DONE/DOCS_SITE/v1_tsom_crosscutting_link_plan.md`

## Rollback plan

- Each level is additive and independent: if Level 4 misbehaves, disable the outbound trigger on the failing side (deactivate the Flow / Business Rule); Levels 1–3 remain functional.
- Secrets/tokens: revoke the OAuth token / rotate the Connected App secret; no code change required.
- Site: revert the Pages-touching commit on `main`; the previous deploy remains until a new one succeeds.

## Reproducibility note

A fresh agent can follow `docs/00`→`08` with only this repo and two free signups; no prior state is assumed. Configuration is captured as steps (not snapshots), so instances stay disposable.
