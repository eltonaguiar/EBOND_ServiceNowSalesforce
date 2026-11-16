# EBOND progressive integration lab — final-v6 design

> **Status:** implementation-ready design; live integration not yet certified.  
> **Baseline:** `42b86eb`  
> **Student site:** https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/

## 1. Purpose and success criteria

Build a beginner-friendly, multi-level lab that starts with two free development environments and ends with a narrowly scoped, bidirectional Salesforce Case ↔ ServiceNow Incident proof of concept. Each level must be independently useful, contain exact steps and expected results, and state whether its evidence comes from repository tests, mocks, or live instances.

The design is complete when:

- a fresh learner can provision the environments without paid middleware;
- Levels 0–2 prove connectivity and one-way creation;
- the advanced path proves create, update, idempotent replay, and ServiceNow-to-Salesforce callback;
- integration writes settle without a loop and do not suppress later human edits;
- field ownership, correlation, security, failure handling, cleanup, and troubleshooting are explicit;
- optional OOB/subscription methods are compared honestly and are not required for the free core;
- the README, Jekyll site, and ServiceNow Learning cross-cutting page link to the stable lab.

## 2. Non-goals

- Production-grade high-volume middleware, exactly-once delivery, or multi-object master-data management.
- Account/Contact/Opportunity synchronization in the first implementation.
- A MID Server for this public cloud-to-cloud path.
- A second GitHub Pages theme/workflow or a second correlation/API model.
- A claim that IntegrationHub, the Salesforce spoke, Apex deployment, or live E2E behavior is available/passing without evidence.
- Automatic merge of the final review. A human remains the merge gate.

## 3. Approaches and decision

### A. Documentation-only

Keep the conceptual Levels 1–4. This is easy but leaves the public “working POC” claim unsupported. Rejected.

### B. Code-first capstone

Deploy the Apex/ServiceNow skeleton immediately. This provides real artifacts but skips beginner credential/HTTP lessons and currently carries create-only and loop-suppression defects. Rejected as the sole path.

### C. Hybrid progressive lab — selected

Retain the Jekyll Labs 0–5 and add a corrected, testable implementation behind them. Start with Table API CRUD, add Salesforce Flow and Apex alternatives, then add the controlled callback. Use one dictionary, one callback endpoint, and behavior-based acceptance tests. Optional Workflow Studio/IntegrationHub material remains a comparison track.

## 4. Repository and documentation boundaries

- `site/`: canonical student-facing Jekyll lab. Existing `/labs/00-instances/` through `/labs/05-troubleshooting/` URLs remain stable.
- `lab/`: deployable Salesforce and ServiceNow reference artifacts plus the local smoke script. This is reference source, not evidence of a successful deployment.
- `tests/`: repository contracts, documentation/link checks, and source-level regression guards. These do not replace Apex or ServiceNow tests.
- `2026-11-16-SWARM/03_DONE/`: durable domain deliverables and links to the canonical lab/design.
- `2026-11-16-SWARM/07_final_review4/`: final design, implementation plan, file manifest, test plan, evidence index, and review history.
- `.github/workflows/`: one Jekyll Pages deployment, one repository contract workflow, and one strict SWARM validation workflow.
- `README.md`: repository index and current validation status. It must not call the capstone working until the live gate passes.

## 5. Progressive learner path

### Lab 0 — Instances, releases, identities, and safety

1. Request a ServiceNow PDI and Salesforce Developer Edition org; record the PDI family, Salesforce org/My Domain, and selected REST API version.
2. Confirm nonproduction data only and back up ServiceNow work using source control or Update Sets.
3. Create least-privilege integration identities. Admin may be used only for setup, not as the automation identity.
4. Configure local secret entry and native credential stores. Do not save credentials in the repository, screenshots, Postman exports, or shell history.
5. Verify PDI wake behavior and record the current Developer Site inactivity guidance rather than treating it as a permanent guarantee.

**Gate:** both environments are reachable, the integration identities have only the required access, and no secret appears in Git or logs.

### Lab 1 — Table API CRUD and HTTP evidence

1. Use curl or Postman with the integration identity to GET a bounded Incident list.
2. POST one Incident to `/api/now/table/incident`; require HTTP 201, a `Location` header, and a returned `sys_id`/number.
3. GET by `sys_id`, PATCH the Incident, and independently read back each mapped value.
4. Repeat with malformed JSON, wrong credentials, and insufficient authorization.
5. DELETE the test Incident and require 204, or document a no-delete cleanup policy if ACLs intentionally forbid deletion.

**Gate:** exact status codes and read-back values pass; a 200 response alone is never accepted without checking the body and expected record.

### Lab 2A — Salesforce Flow one-way create

1. Create the correlation/mirror fields and the Named/External Credential using the documented authentication option for the learner's org.
2. Use a record-triggered Flow with a **Run Asynchronously** path for the HTTP callout.
3. POST a create-only payload through the Named Credential.
4. Parse the response and update `Snow_Sys_Id__c` and `Snow_Number__c` on the original Case.
5. Restrict the trigger to creation, or to the explicitly owned fields, so correlation updates do not re-fire the callout.

**Gate:** one new Case creates one Incident and stores the returned identifiers. This level does not claim update, retry, or bidirectional support.

### Lab 2B — Salesforce Apex Queueable alternative

1. Keep callouts out of the trigger. The trigger only selects new records or changes to Salesforce-owned fields and enqueues one bulk Queueable.
2. The Queueable performs the callout, checks status/body, and writes correlation and integration-status fields.
3. Chunk work within documented callout/Queueable limits; use per-record error capture instead of failing an entire batch silently.
4. Run Apex `HttpCalloutMock` tests before the live exercise.

**Gate:** insert and owned-field update work, correlation-only updates do not enqueue, and a human edit after an integration update still enqueues.

### Lab 3 — Correlation, validation, and idempotent upsert

1. Keep the Table API GET-then-POST/PATCH example as a teaching step, explicitly noting that PATCH is not an upsert and lookup/create has a race.
2. For the advanced endpoint, validate the remote Case ID, source, required fields, lengths, and allowed mappings.
3. Query source + remote ID; return 201 on first create and 200 with the same `sys_id` on replay.
4. Use `GlideRecordSecure`, explicit `REST_Endpoint` ACLs, and a unique correlation field to enforce the lab's one-to-one mapping. Document the remaining concurrency/transaction limitations.
5. Test malformed input, unauthorized callers, duplicate replay, and source-ID collisions.

**Gate:** repeated identical requests do not create a second Incident, negative requests fail closed, and the response contains no credentials.

### Lab 4 — ServiceNow-owned callback and convergence

1. Test the Salesforce external-ID PATCH manually before automation.
2. Use the standard endpoint `/services/data/<version>/sobjects/Case/Snow_Sys_Id__c/<sys_id>`; do not add the parallel custom Apex REST endpoint.
3. Configure an async Business Rule as a legacy/scripting exercise. Use its condition builder for ServiceNow-owned field changes; do not reference `previous`.
4. Because the background rule needs the HTTP result, use `execute()` with an explicit short timeout. Do not call `executeAsync()` and then pretend later lines are nonblocking.
5. Build the JSON body with `JSON.stringify` and include only ServiceNow-owned `Snow_*` mirror fields.
6. Record outcome in a separate sync-log table. Do not call `current.update()` and do not use `setWorkflow(false)` as the default loop guard.
7. Verify one callback produces no further outbound Salesforce call, then edit the Case again and verify later human work is not suppressed.

**Gate:** create, update, replay, callback, convergence, special-character payloads, and subsequent human edits pass with recorded evidence.

### Lab 5 — Methods, troubleshooting, and hardening

Compare Workflow Studio base actions, IntegrationHub Salesforce spoke, direct REST, Salesforce Connect/federation, and batch reconciliation. Confirm subscription, plugin, spoke, and API-version availability before any optional exercise. Add bounded retry scheduling, reconciliation, dashboards, and production deployment guidance only after the core lab is stable.

## 6. Canonical correlation and ownership contract

### Identifiers

| System | Field | Rule |
|---|---|---|
| ServiceNow Incident | `u_ebond_sf_case_id` | String(18), unique for the lab, stores the 18-character Salesforce Case ID. |
| Salesforce Case | `Snow_Sys_Id__c` | Text(32), External ID + Unique, stores the ServiceNow `sys_id`. |
| Salesforce Case | `Snow_Number__c` | Text(40), stores the display Incident number; not a correlation key. |

Do not also use `x_snc_ebond_*`, `u_sf_case_id`, `Correlation_Id__c`, or a second custom Apex callback in this implementation. ServiceNow `correlation_id` may be discussed as an OOB one-to-one correlation field, but it is not a uniqueness constraint, sync state, or loop guard and is not a second source of truth in this lab.

### Field ownership

| Data | Owner | Destination behavior |
|---|---|---|
| Case `Subject` → Incident `short_description` | Salesforce | Salesforce-owned delta triggers outbound sync. ServiceNow callback never writes Case `Subject`. |
| Case `Description` → Incident `description` | Salesforce | Same owner and trigger rule; no last-writer-wins mode in the core lab. |
| Case `Priority` → Incident impact/urgency | Salesforce | Use one documented mapping table; do not equate Salesforce Priority directly with ServiceNow `priority` while also fixing impact independently. |
| Incident state/resolution/work information → Case `Snow_*` mirror fields | ServiceNow | Async rule condition detects owned changes; Salesforce does not push these fields back. |
| Correlation and integration status | Integration | Updates never trigger business-field synchronization. |
| All other fields | Local to each system | No implicit mapping. Unknown values fail closed or are logged as unmapped. |

This single-owner model is deliberately simpler and safer than shared Description editing. Manual conflict handling can be taught as an optional design exercise, not by requiring learners to flip a persistent source flag.

## 7. Authentication and authorization

- **Lab 1:** Basic authentication is a contained PDI smoke-test option with a dedicated integration user, not the final automation pattern.
- **Salesforce → ServiceNow:** Named/External Credentials hold the PDI credential. Use the org-supported Basic path for the beginner exercise and OAuth 2.0 client credentials for the hardened path.
- **ServiceNow → Salesforce:** use the current Salesforce External Client App/Connected App experience supported by the org, with OAuth 2.0 client credentials or JWT bearer as verified by the implementation plan. Store consumer material only in the ServiceNow OAuth provider/credential configuration.
- **Scripted REST:** require authentication and explicit endpoint/table ACL tests. Use `GlideRecordSecure`; `web_service_admin` is for administration, not a blanket consumer role.
- **Both directions:** use HTTPS, My Domain/API hosts rather than Lightning UI hosts, least privilege, redacted logs, and negative 401/403 tests.

## 8. Failure, retry, and observability model

- Validate JSON structure and required values before creating records.
- Require expected 200/201/204 codes and validate response bodies, not status alone.
- Retry only bounded transient failures (408, 429, 5xx, transport timeout), honoring `Retry-After` where present and using capped exponential backoff with jitter.
- Refresh/reacquire an expired OAuth token once; do not blindly retry other 401/403/400 responses.
- Store correlation ID, timestamp, attempt count, status, and a bounded/redacted error summary. Provide a manual replay path before adding scheduled retries.
- Keep full response bodies, Authorization headers, client secrets, and credential principals out of logs.
- Treat async updates as potentially out of order; use last-applied timestamps/version checks in the hardening task rather than assuming arrival order.

## 9. Validation layers

1. **Repository:** strict SWARM validation, all-Markdown/site link checks, shell syntax in both script directories, actionlint, secret scanning across MD/HTML/YAML/Apex/JS/XML/shell, and Python contracts.
2. **Salesforce:** deploy to a clean Developer Edition org and run local Apex tests with callout mocks, including create/update/convergence/human-edit/error/special-character cases.
3. **ServiceNow:** ATF inbound REST requests and immediate assertions for the current instance; authorization and correlation checks. ATF does not call Salesforce and therefore is not the full E2E test.
4. **Live E2E:** scripted curl/API checks plus UI verification in both systems for every level, with cleanup and redacted evidence.
5. **Publishing:** Jekyll build, live Pages/link checks, and a separate small learning-repository PR to replace the dated beginner-path source link with the stable Jekyll URL.

## 10. Design references

ServiceNow official references reviewed 2026-11-16:

- PDI access/activity: https://developer.servicenow.com/print_page.do?release=australia&category=developer-program&identifier=accessing-your-pdi&module=guide
- Table API: https://www.servicenow.com/docs/r/api-reference/rest-apis/c_TableAPI.html
- Table API response codes: https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/r_RESTAPIHTTPResponseCodes.html
- Scripted REST security/good practices: https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/scripted-rest-good-practices.html and https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/t_WbSvcOpRqACL.html
- RESTMessageV2: https://www.servicenow.com/docs/r/api-reference/server-api-reference/c_RESTMessageV2API.html
- Business Rules: https://www.servicenow.com/docs/r/api-reference/business-rules-classic/c_BusinessRules.html
- OAuth inbound/outbound: https://www.servicenow.com/docs/r/platform-security/authentication/oauth-inbound.html and https://www.servicenow.com/docs/r/api-reference/web-services/t_UseAThirdPartyOAuthProvider.html
- IntegrationHub and Salesforce spoke: https://www.servicenow.com/docs/r/integrate-applications/integration-hub/integrationhub.html and https://www.servicenow.com/docs/r/integrate-applications/integration-hub/salesforce-spoke.html
- Correlation model: https://www.servicenow.com/docs/r/integrate-applications/integration-hub-remote-process-sync/correlation.html
- ATF REST steps: https://www.servicenow.com/docs/r/application-development/automated-test-framework-atf/rest-test-steps.html

Salesforce official references and release-specific setup labels are indexed in `EVIDENCE_INDEX.md`; implementation must verify the current org UI rather than mixing Connected App and External Client App instructions.
