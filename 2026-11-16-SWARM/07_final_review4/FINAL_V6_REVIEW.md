# FINAL_V6_REVIEW — independent synthesis and implementation gate

**Round:** 6  
**Reviewer:** `review/final-v6` isolated worktree  
**Baseline:** `42b86eb` (`main`, merge of Pages lab PR #5)  
**Date:** 2026-11-16

## Verdict

**Do not describe the current capstone as a working or deployable bidirectional POC yet.** The repository has a useful progressive Jekyll lab, a good free-PDI field-prefix correction, a sensible Queueable starting point, and green repository contract tests. It does not yet prove the advertised behavior. The required work is specific and bounded; the hybrid design and implementation/test plans in this directory are the gate for the next implementation round.

This is not a request to restart the lab or merge another branch wholesale. Preserve the current `README.md` + `site/` + SWARM structure and remediate the current code and documentation in place.

## Review protocol and evidence

- Inspected `main` at `42b86eb`, the earlier peer branches, and the open review history. The independent branch comparison covered `8e7b1ad`, `43816d9`, `4e67e74`, and `0b87c99`; later rounds were re-checked on the current baseline.
- Ran `python3 -m pytest tests -q`: **6 passed**. These tests check file presence and selected strings; they do not execute Apex or ServiceNow behavior.
- Ran `python3 tools/swarm/swarm_librarian.py validate --dir 2026-11-16-SWARM --repo-root .`: **0 errors, 60 warnings**. `--strict` therefore fails and remains the required clean gate.
- Confirmed the EBOND Pages URL and the ServiceNow Learning cross-cutting URL return content. The cross-cutting source link was added by commit `80ce195165728eaf39f59761a3c78a38476fe510` in the learning repository.
- No live ServiceNow or Salesforce instance was accessed. No Apex deployment, ServiceNow execution, credential setup, or end-to-end success is claimed by this review.

## Findings that block the capstone

| ID | Severity | Evidence | Required disposition |
|---|---|---|---|
| V6-B1 | Blocker | `lab/salesforce/force-app/main/default/triggers/CaseTrigger.trigger:1` is `after insert` only; `CaseTriggerHandler.cls` has no update path. | Add after-update handling for Salesforce-owned fields and test both create and update. Correlation-only writes must not enqueue another callout. |
| V6-B2 | Blocker | `CaseEscalationQueueable.cls:26` skips `Snow_Sync_Source__c == 'servicenow'`; `business_rule_async_sync.js:2` returns when `u_sync_source == 'salesforce'`; neither marker is reliably consumed/reset. | Replace persistent source suppression with owned-field delta detection. Add a human-edit-after-integration-write test in both directions. |
| V6-B3 | High | `site/labs/03-snow-to-salesforce.md:73-77` interpolates unescaped Subject/Description into a JSON template; the Business Rule uses `setStringParameterNoEscape`. Quotes and newlines can produce invalid JSON. | Build the body as an object and call `JSON.stringify`; test quotes, apostrophes, Unicode, CR/LF, and backslashes. |
| V6-B4 | High | `rest_message_notes.md:35` filters `u_sf_case_id`, while the canonical field is `u_ebond_sf_case_id`; the script sends `state`, but the documented JSON omits it. | Use one field dictionary and one payload contract. Send only ServiceNow-owned mirror fields, including the explicitly designed state/resolution fields. |
| V6-B5 | High | `SnowIncidentRest.cls` implements a custom Apex REST endpoint, but `rest_message_notes.md` calls Salesforce's standard external-ID Case PATCH instead. | Keep the standard `/sobjects/Case/Snow_Sys_Id__c/{sys_id}` PATCH for this lab and remove the unused Apex REST class/test. Do not maintain two callback contracts. |
| V6-B6 | High | `data_model_field_mapping.md` and `field_ownership_and_manual_edits.md` disagree with the runnable `u_`/`Snow_*` model; `site/labs/04-ownership.md:40` makes Description last-writer while other docs make Salesforce the owner. | Adopt one dictionary and field-ownership matrix across the notebook, Jekyll pages, Apex, scripts, and tests. |
| V6-B7 | High | `SnowIncidentService.cls` performs lookup-then-create without a unique/atomic ServiceNow upsert; the tests use a single mock and do not exercise concurrent/replayed creates. | Make the ServiceNow correlation field unique, define duplicate-response reconciliation, and use the custom Scripted REST upsert for the advanced path. Document the Table API lookup/create race instead of claiming atomicity. |
| V6-B8 | High | `README.md:3`, `site/index.md:10`, and `FINAL_V5_REVIEW.md:26` imply working/deployable status without live evidence. | Mark the capstone as review/live-validation-pending until the acceptance matrix passes. Repository tests and mock tests must be reported separately from live results. |
| V6-B9 | Blocker | `business_rule_async_sync.js:1,8` uses `previous`, but ServiceNow documents that async Business Rules have no previous-record object. It also recommends avoiding `current.update()` in Business Rules. | Put `changes()` conditions in the async rule's condition builder, do not reference `previous`, and write diagnostics to a separate sync-log record rather than recursively updating `current`. |

## Reliability, security, and QA gaps

| ID | Severity | Evidence | Required disposition |
|---|---|---|---|
| V6-R1 | High | `CaseEscalationQueueable.cls:25-40` processes a batch without per-record error capture; the ServiceNow rule only logs non-2xx responses. The prose advertises retries/idempotency that the code does not implement. | Add per-record status/error fields, bounded retry semantics for 408/429/5xx, no blind retry for other 4xx, redacted logs, and a manual replay path. A scheduled retry is a separate hardening task, not an implied existing feature. |
| V6-R2 | Medium | `SnowIncidentService.cls:74` includes a full response body in an exception; the ServiceNow script logs a full response body. | Log status, correlation ID, and a bounded/redacted error summary only. Never log Authorization headers, credential principals, access tokens, or response bodies containing secrets. |
| V6-R3 | Medium | The architecture notebook says all options use free tiers, while current ServiceNow documentation says IntegrationHub and the Salesforce spoke require a separate subscription, with PDI preview available. | Keep the core lab free; label Workflow Studio base actions separately from entitlement-dependent spokes and verify installed-spoke/API versions before optional exercises. |
| V6-Q1 | High | `tests/test_lab_contract.py` checks strings such as `enqueueJob` and `upsert row`; no test proves update propagation, echo convergence, subsequent human edits, malformed-input handling, or retries. Apex tests have not been run by this review. | Add behavior-focused Apex mocks and ServiceNow test steps. Execute them in the actual free org/PDI before the live-ready claim. |
| V6-Q2 | Medium | `tests/test_docs_links.py` covers only two READMEs; `validate.yml` checks only `lab-scripts/*.sh`; its secret scan omits Apex, JavaScript, and XML. Baseline SWARM validation has 60 evidence warnings. | Scan all relevant Markdown/site links, both script directories, all source file types, and require `swarm_librarian.py validate --strict` to pass. |
| V6-Q3 | Medium | `lab/scripts/curl_level1.sh` prints any HTTP response and exits successfully on HTTP errors; `lab-scripts/level1_smoke_test.sh` uses admin credentials. | Consolidate on one fail-closed Level-1 script using a least-privilege integration user, safe secret entry, expected 201 validation, `sys_id`/number assertions, and cleanup instructions. |

## Approaches considered

1. **Documentation-only progressive lab.** Lowest complexity and useful for concepts, but it would leave the advertised runnable POC unproven and the current misleading status intact. Rejected as the final state.
2. **Merge the runnable capstone directly.** The Queueable skeleton and Jekyll lab are valuable, but direct adoption would preserve the create-only trigger, persistent loop guards, competing APIs, and unverified claims. Rejected.
3. **Hybrid progressive remediation (selected).** Keep Labs 0–2 as the beginner path, make Level 3 the validated/idempotent path, and make Level 4 the ownership/callback capstone. Use the standard Salesforce external-ID PATCH, one correlation dictionary, and behavior tests before any live-ready claim.

## Selected design in one paragraph

Salesforce owns Case `Subject`, `Description`, and `Priority`; ServiceNow owns Incident state/resolution/work information. Salesforce after-insert/after-update automation enqueues work only when those owned fields require synchronization. The Queueable writes through the Named Credential and records correlation/status fields; those integration-owned Salesforce updates do not satisfy the owned-field trigger condition. ServiceNow's asynchronous Business Rule uses its condition builder—not the unavailable `previous` object—to detect ServiceNow-owned changes and PATCHes the Case by the unique external ID `Snow_Sys_Id__c`, with a `JSON.stringify` body containing only `Snow_*` mirror fields. That callback likewise does not satisfy the Salesforce-owned trigger condition. This structural design prevents echoes without a sticky `u_sync_source` or `Snow_Sync_Source__c` flag and allows later human edits. The background rule uses a short-timeout `execute()` because it needs the response, writes diagnostics to a separate sync-log table, and never calls `current.update()`.

## Exit gate for the next implementation round

- The five canonical artifacts in this directory are updated to v6 and contain no placeholders or contradictory field/API names.
- Independent review finds no unresolved documentation/design blocker.
- Repository validation is green, including strict SWARM validation and expanded link/secret/shell checks.
- Apex mock tests and ServiceNow tests pass on the actual free instances; create, update, replay, convergence, subsequent-human-edit, JSON-special-character, and failure-path cases have recorded evidence.
- The Pages site and README distinguish mock/repository results from live results until that evidence exists.
- The learning site's beginner-path link targets the stable Jekyll lab URL, not a dated SWARM source path.

**Current status:** design/review deliverable, not live-integration certification. See `DESIGN.md`, `PLAN.md`, `IMPLEMENTATION_STEPS.md`, `FILES_TO_TOUCH.md`, `TESTING_PLAN.md`, and `EVIDENCE_INDEX.md`.
