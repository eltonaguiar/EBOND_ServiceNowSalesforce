# FILES_TO_TOUCH — final-v6 review and implementation manifest

## Baseline

- Repo: `eltonaguiar/EBOND_ServiceNowSalesforce`
- Review branch/worktree: `review/final-v6`
- Baseline main: `42b86eb` (merge of Pages lab PR #5)
- Review target: `2026-11-16-SWARM/07_final_review4/`

## Review round changes (already created in this branch)

| Path | Action |
|---|---|
| `2026-11-16-SWARM/07_final_review4/FINAL_V6_REVIEW.md` | Created: independent synthesis, blockers, dispositions, exit gate. |
| `2026-11-16-SWARM/07_final_review4/DESIGN.md` | Created: progressive hybrid design, ownership/correlation contract, auth/failure/validation model. |
| `2026-11-16-SWARM/07_final_review4/TESTING_PLAN.md` | Replaced: fail-closed repository gate, Salesforce/ServiceNow/live acceptance matrices. |
| `2026-11-16-SWARM/07_final_review4/PLAN.md` | Replace with v6 scope/decisions. |
| `2026-11-16-SWARM/07_final_review4/IMPLEMENTATION_STEPS.md` | Replace with ordered, code-backed v6 tasks. |
| `2026-11-16-SWARM/07_final_review4/EVIDENCE_INDEX.md` | Replace with official-resource and baseline evidence. |
| `README.md` | Modified: live-validation-pending status, validation-status section, SN→SF typo, Jekyll layout wording. |
| `site/_layouts/default.html` | Modified: global validation-pending banner, IntegrationHub wording. |
| `site/index.md` | Modified: capstone is intended/validation-pending, not claimed working. |
| `tests/test_docs_links.py` | Modified: added live-validation-status regression test. |

## Implementation tasks referenced by the implementation plan

### Salesforce metadata

| Path | Task |
|---|---|
| `lab/salesforce/force-app/main/default/triggers/CaseTrigger.trigger` | Add `after update`; delegate to `afterChange`. |
| `lab/salesforce/force-app/main/default/classes/CaseTriggerHandler.cls` | Add `afterChange` with owned-field delta; remove sticky `Snow_Sync_Source__c` handling. |
| `lab/salesforce/force-app/main/default/classes/CaseEscalationQueueable.cls` | Remove source-flag skip; add per-record status/error handling; preserve chunking and bounded chaining. |
| `lab/salesforce/force-app/main/default/classes/SnowIncidentService.cls` | Use stored `Snow_Sys_Id__c` for updates; safe JSON; validation; transient/4xx/redaction policy; status helpers. |
| `lab/salesforce/force-app/main/default/classes/SnowCalloutMock.cls` | Extend mock to return distinct create/update/error responses and count calls. |
| `lab/salesforce/force-app/main/default/classes/CaseTriggerHandlerTest.cls` | Add after-update, human-edit-after-integration, and correlation-only tests. |
| `lab/salesforce/force-app/main/default/classes/CaseEscalationQueueableTest.cls` | Add per-record failure and retry-count tests. |
| `lab/salesforce/force-app/main/default/classes/SnowIncidentServiceTest.cls` | Add update/duplicate/special-character/400/429/500 tests with the expanded mock. |
| `lab/salesforce/force-app/main/default/objects/Case/fields/Snow_Sys_Id__c.field-meta.xml` | Keep External ID + Unique; verify length. |
| `lab/salesforce/force-app/main/default/objects/Case/fields/Snow_State__c.field-meta.xml` | Create or confirm ID of the ServiceNow state mirror. |
| `lab/salesforce/force-app/main/default/objects/Case/fields/Snow_Resolution__c.field-meta.xml` | Create or confirm long-text area mirror. |
| `lab/salesforce/force-app/main/default/objects/Case/fields/Snow_Sync_Status__c.field-meta.xml` | Create or confirm status field. |
| `lab/salesforce/force-app/main/default/objects/Case/fields/Snow_Sync_Error__c.field-meta.xml` | Create or confirm redacted error field. |
| `lab/salesforce/force-app/main/default/classes/SnowIncidentRest.cls` and `SnowIncidentRestTest.cls` | Remove as part of choosing the standard external-ID callback; remove both class and test/metadata. |
| `lab/salesforce/force-app/main/default/classes/Snow_Number__c.field-meta.xml` (expected path) | Confirm field metadata path is `objects/Case/fields/`. |

### ServiceNow artifacts

| Path | Task |
|---|---|
| `lab/servicenow/business_rule_async_sync.js` | No `previous`; condition-builder `changes()`; `JSON.stringify`; no `current.update()`; record to `SyncLog`. |
| `lab/servicenow/scripted_rest_bond_case.js` | Use `GlideRecordSecure`, source+ID lookup, unique correlation, 201/200/400 responses, explicit ACL notes. |
| `lab/servicenow/rest_message_notes.md` | Exact endpoint, client-credentials OAuth, `Snow_*`-only JSON body, no `u_sf_case_id` typo, no Subject/Description reverse writes. |
| `lab/servicenow/sync_log.md` | New: table/field checklist for `u_ebond_sync_log` and redacted logging rules. |
| `lab/servicenow/script_include_sync_log.js` | New: reusable `SyncLog`/truncate helper referenced by the Business Rule. |
| `lab/README.md` | Align field names and path with the canonical dictionary; remove `Snow_Sync_Source__c`/`u_sync_source`. |
| `lab/scripts/curl_level1.sh` | Fail closed on non-201 and non-200/204 as appropriate; require integration identity; no admin automation. |

### Documentation and contract tests

| Path | Task |
|---|---|
| `2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md` | Replace with canonical `u_ebond_sf_case_id`/`Snow_*` matrix and ownership rules. |
| `2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md` | Correct free/entitlement claims for IntegrationHub/speaks. |
| `2026-11-16-SWARM/03_DONE/INTEGRATION/lab_levels_beginner_path.md` | Align Levels to canonical fields and authentication paths. |
| `2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_salesforce_outbound_to_sn.md` | Flow must use an asynchronous/callout-safe path; align fields; remove raw Basic admin recommendation. |
| `2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md` | Use current org OAuth/client-credentials path; JSON-safe body; align fields. |
| `2026-11-16-SWARM/03_DONE/BESTPRACTICES/field_ownership_and_manual_edits.md` | Replace persistent-flag loops with owned-field deltas and single-owner matrix. |
| `2026-11-16-SWARM/03_DONE/BESTPRACTICES/reliability_retries_idempotency.md` | Scope what is implemented vs designed; correction both HTTP and transport error checks. |
| `2026-11-16-SWARM/03_DONE/BESTPRACTICES/security_identity_secrets.md` | Redaction specifics for Apex/JS/XML; external client/OAuth distinction. |
| `2026-11-16-SWARM/03_DONE/BESTPRACTICES/rate_limits_monitoring_logging.md` | Preserve the v5 truncation fix; add current API/version verification guidance. |
| `2026-11-16-SWARM/03_DONE/TESTING/qa_test_plan.md` | Replace checkbox-only QA with the v6 acceptance matrix and evidence boundary. |
| `site/labs/01-table-api.md`, `02-salesforce-to-snow.md`, `03-snow-to-salesforce.md`, `04-ownership.md` | Align code, field names, JSON body, ownership, and loop-guard descriptions to the final design. |
| `tests/test_lab_contract.py` | Add source-level regression assertions for after-update, JSON safety, no sticky source flags, and single callback API. |
| `tests/test_docs_links.py` | Expand to all Markdown/Jekyll link targets and add required stable URLs. |
| `.github/workflows/validate.yml` | Add both shell directories, secret scan file types, actionlint, and `--strict`. |
| `site/Gemfile` (new) | Reproducible `github-pages`/Jekyll build bundle for local verification. |

### Cross-repository follow-up (separate PR, human-gated)

| Repository | Path | Change |
|---|---|---|
| `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` | `docs/cross-cutting.md` | Point the EBOND beginner-path link to the stable Jekyll `.../labs/00-instances/` URL; do not add a second section. |

## Non-targets

- Do not add `README.MD` or a second Jekyll workflow, v1 root `docs/` layouts, or `x_snc_ebond_*` field prefixes.
- Do not port or re-enable synchronous after-save callouts from the v1 branch.
- Do not open a second Pages deployment source root.
- Do not create or retain `u_sync_source`/`Snow_Sync_Source__c` as the loop guard.
- Do not use `setWorkflow(false)` as the teaching default.
- Do not edit the ServiceNow learning repo from this PR; that is a separate human-approved cross-repository PR.
