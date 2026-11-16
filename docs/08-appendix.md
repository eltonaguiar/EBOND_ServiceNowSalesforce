---
title: 8. Appendix
---

# 8. Appendix

## 8.1 Glossary

| Term | Definition |
|------|------------|
| **PDI** | Personal Developer Instance — ServiceNow's free, disposable developer instance |
| **Developer Edition org** | Salesforce's free, permanent developer org |
| **Scratch org** | Ephemeral, source-driven Salesforce org (≤30 days), via the `sf`/`sfdx` CLI |
| **Connected App** | Salesforce OAuth provider definition (Client ID/Secret, scopes) |
| **Named Credential** | Salesforce's secure store of an endpoint + auth (no hardcoded secrets) |
| **External Credential** | Salesforce object holding the actual auth (principal + secret), linked to a Named Credential |
| **Remote Site Setting** | Salesforce allowlist entry required before an outbound callout |
| **REST Message** | ServiceNow's reusable outbound REST definition (endpoint + auth + methods) |
| **OAuth Application Registry** | ServiceNow's OAuth client/provider configuration |
| **Table API** | ServiceNow's automatic inbound REST API at `/api/now/table/<table>` |
| **Scripted REST API** | ServiceNow's custom inbound endpoint with JS logic |
| **IntegrationHub / Spoke** | ServiceNow low-code integration; spokes are vendor action packs |
| **Flow Designer** | ServiceNow's no-code automation engine |
| **Flow (Salesforce)** | Salesforce's no-code automation engine |
| **Platform Events** | Salesforce's event bus for decoupled, high-volume messaging |
| **Correlation ID** | External ID stored on both records to enable update-not-duplicate and loop prevention |
| **System of Record** | The system that *owns* a field or record and is authoritative for it |
| **Idempotency** | Repeating an operation yields the same result (no duplicate side effects) |

## 8.2 Case → Incident field map (record your decisions)

| Salesforce Case | ServiceNow Incident | Owner | Notes |
|-----------------|---------------------|-------|-------|
| Subject | short_description | Salesforce | |
| Description | description | Shared | last-writer-wins |
| Priority | impact / urgency | Salesforce | map High→1, Medium→2, Low→3 |
| AccountId / ContactId | (caller / account fields) | Salesforce | map to `caller_id` if desired |
| Status | state | ServiceNow | map at sync time |
| CaseNumber | (correlation_display) | Salesforce | informational |
| Id | u_correlation_id | Salesforce | correlation |
| Origin | u_origin | Salesforce | loop guard |

## 8.3 Official references

**ServiceNow**
- Developer portal / PDI: <https://developer.servicenow.com>
- Inbound REST (Table API): <https://docs.servicenow.com/bundle/washingtondc-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html>
- Scripted REST APIs: <https://docs.servicenow.com/bundle/washingtondc-application-development/page/integrate/custom-web-services/concept/c_ScriptedRESTAPI.html>
- OAuth 2.0: <https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/concept/oauth-2-0.html>
- IntegrationHub: <https://docs.servicenow.com/bundle/washingtondc-integrate-applications/page/administer/integrationhub/concept/integrationhub.html>
- Flow Designer: <https://docs.servicenow.com/bundle/washingtondc-build-workflows/page/administer/flow-designer/concept/flow-designer.html>

**Salesforce**
- Developer signup: <https://developer.salesforce.com/signup>
- REST API: <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm>
- Named Credentials: <https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_named_credentials.htm>
- External Credentials: <https://help.salesforce.com/s/articleView?id=sf.named_credentials_about.htm>
- Connected Apps / OAuth: <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>
- Scratch orgs: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs.htm>
- Platform Events: <https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/platform_events_intro.htm>
- Apex callouts: <https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts.htm>

## 8.4 Related learning repos

- `eltonaguiar/ServiceNow_Learning` — rapid ServiceNow learning methodology + REST Message / Remote Table labs.
- `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` — module guides; see the [Cross-Cutting Platform Skills → Integrations](https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/) page for the integration decision framework this lab operationalizes.
- `eltonaguiar/TSOM-Salesforce-DevOps-Learning` — Salesforce DevOps / CI-CD learning material.

## 8.5 Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Salesforce callout fails: "callout not allowed" | Missing Remote Site Setting | Add `https://devNNNNNN.service-now.com` |
| Named Credential callout 401/403 | Permission Set not mapped to the principal | Map the External Credential principal to a Permission Set + assign |
| `401 Unauthorized` from ServiceNow Table API | Wrong user/password or missing role | Check integration user creds + role |
| OAuth token request fails | Wrong Consumer Key/Secret or callback mismatch | Re-check Connected App + registry values |
| Duplicate records on every save | Missing origin/correlation check | Verify the loop-guard condition (Level 4 §5.6) |
| Apex "You have uncommitted work pending" | DML before callout | Do callout first, or move DML after callout |
| ServiceNow REST Message timeouts | Endpoint slow or blocked | Increase timeout; switch to `executeAsync()` |

## 8.6 Items flagged for verification (review rounds)

1. Exact IntegrationHub spoke catalog on a current PDI (Salesforce spoke entitled or not).
2. Salesforce Developer Edition data storage + daily API request limit (varies by release).
3. Whether the ServiceNow OAuth provider supports **client credentials** for inbound, or requires a different grant type on current releases.
4. Salesforce version in the REST base path (`v60.0` here — bump to the latest available in your org).
