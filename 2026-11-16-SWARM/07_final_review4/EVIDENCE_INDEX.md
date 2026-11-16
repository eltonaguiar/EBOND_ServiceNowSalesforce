# EVIDENCE_INDEX — final-v6

Each claim links to a repo path, live URL, commit SHA, or official documentation. Access date for product docs: 2026-11-16. Credentials and unredacted response bodies are never stored.

## Baseline review evidence

| Claim | Evidence |
|---|---|
| Review baseline | `main` commit `42b86eb` (merge of Pages lab PR #5). |
| Earlier branch comparison | Reviewed `8e7b1ad` (main), `43816d9` (v1-bond-lab), `4e67e74` (round2), `0b87c99` (v3-review). |
| Current repository tests | `python3 -m pytest tests -q` → 6 passed on baseline; 7 passed after adding the status regression. |
| SWARM validation baseline | `swarm_librarian.py validate --dir 2026-11-16-SWARM --repo-root .` → 0 errors, 60 warnings. `--strict` is the required gate. |
| Live Pages site | https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/ (200). |
| Cross-cutting page + source link | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/ ; source commit `80ce195165728eaf39f59761a3c78a38476fe510` in the learning repo. |
| Status honesty | `README.md` and `site/_layouts/default.html` show `Live integration validation pending`; `tests/test_docs_links.py::test_live_validation_status_is_visible` enforces this until the live gate passes. |

## Official ServiceNow references

| Topic | URL |
|---|---|
| PDI access/activity/reclaim | https://developer.servicenow.com/print_page.do?release=australia&category=developer-program&identifier=accessing-your-pdi&module=guide |
| Table API | https://www.servicenow.com/docs/r/api-reference/rest-apis/c_TableAPI.html |
| Table API HTTP response codes | https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/r_RESTAPIHTTPResponseCodes.html |
| Scripted REST good practices | https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/scripted-rest-good-practices.html |
| Scripted REST request ACL | https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/t_WbSvcOpRqACL.html |
| GlideRecordSecure | https://www.servicenow.com/docs/r/api-reference/server-api-reference/c_GlideRecordSecure |
| RESTMessageV2 | https://www.servicenow.com/docs/r/api-reference/server-api-reference/c_RESTMessageV2API.html |
| Business Rules (async, no `previous`) | https://www.servicenow.com/docs/r/api-reference/business-rules-classic/c_BusinessRules.html |
| OAuth inbound | https://www.servicenow.com/docs/r/platform-security/authentication/oauth-inbound.html |
| Third-party OAuth provider | https://www.servicenow.com/docs/r/api-reference/web-services/t_UseAThirdPartyOAuthProvider.html |
| IntegrationHub | https://www.servicenow.com/docs/r/integrate-applications/integration-hub/integrationhub.html |
| Salesforce spoke | https://www.servicenow.com/docs/r/integrate-applications/integration-hub/salesforce-spoke.html |
| Correlation ID model | https://www.servicenow.com/docs/r/integrate-applications/integration-hub-remote-process-sync/correlation.html |
| ATF REST steps | https://www.servicenow.com/docs/r/application-development/automated-test-framework-atf/rest-test-steps.html |

## Salesforce references (to be verified against the current org, 2026-11-16)

| Topic | Required verification |
|---|---|
| Developer Edition signup | Current `developer.salesforce.com/signup` flow and My Domain URL. |
| External Client App / Connected App experience | Current Setup path for the org release; do not mix Connected App client-credentials instructions with External Client App screens unless they are the same object in that release. |
| Named/External Credentials | Confirm Basic `*` and OAuth 2.0 client-credentials options available in the current metadata/UI. |
| Flow HTTP Callout async path | Confirm the record-triggered Flow "Run Asynchronously" option/namespace for the org release. |
| Apex callout/timeout/Queueable limits | Confirm current limits for the deployed org; adjust batching and timeouts. |
| External ID upsert PATCH | `PATCH /services/data/<version>/sobjects/Case/Snow_Sys_Id__c/<sys_id>`; confirm current REST API version. |
| Apex test coverage/deploy | `--test-level RunLocalTests`, code coverage output, and Salesforce deployment threshold. |

The implementation plan and `DESIGN.md` treat these Salesforce-specific labels as version-dependent and require verification before merging; they are not asserted as fixed facts in this review.

## Key repository evidence paths

- `2026-11-16-SWARM/07_final_review4/FINAL_V6_REVIEW.md`
- `2026-11-16-SWARM/07_final_review4/DESIGN.md`
- `2026-11-16-SWARM/07_final_review4/PLAN.md`
- `2026-11-16-SWARM/07_final_review4/IMPLEMENTATION_STEPS.md`
- `2026-11-16-SWARM/07_final_review4/FILES_TO_TOUCH.md`
- `2026-11-16-SWARM/07_final_review4/TESTING_PLAN.md`
- `tests/test_docs_links.py`
- `README.md`
- `site/_layouts/default.html`
- `site/index.md`
