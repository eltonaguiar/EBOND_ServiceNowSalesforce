# Runnable lab — Case ⇄ Incident

Round 2 adds code you can deploy. Round 1 docs stay the narrative. Field names here supersede the scoped `x_snc_ebond_*` names in the v1 mapping: a free PDI is global, so ServiceNow fields use the `u_` prefix.

## Correlation fields

| Side | Field | Role |
|------|-------|------|
| Salesforce Case | `Snow_Sys_Id__c` | External Id + unique. ServiceNow `sys_id`. |
| Salesforce Case | `Snow_Number__c` | Incident number. |
| Salesforce Case | `Snow_Sync_Source__c` | `salesforce` or `servicenow`. Loop guard. |
| ServiceNow incident | `u_ebond_sf_case_id` | Salesforce Case Id. Global dictionary field. Do not use `x_snc_ebond_sf_case_id` on a PDI. |
| ServiceNow incident | `u_sync_source` | `salesforce` or `servicenow`. Loop guard. |
| ServiceNow incident | `correlation_id` | OOTB copy of the Case Id. |

## Path

1. Level 1 — `scripts/curl_level1.sh` posts to the Table API. Confirms Basic auth and a 201.
2. Level 2 — deploy `salesforce/` (`sf project deploy start --source-dir force-app`). Create Named Credential `EBOND_ServiceNow` (External Credential, client credentials or custom Basic) aimed at the PDI. Grant External Credential Principal Access.
3. Level 3 — Apex calls the Table API (`/api/now/table/incident`), not a scoped Scripted REST path. It looks up `u_ebond_sf_case_id` and then POST or PATCH. Optional: paste `servicenow/scripted_rest_bond_case.js` only if you want a custom endpoint; do not point Apex at `x_ebond` unless that scope exists on your instance.
4. Level 4 — create REST Message `EBOND Salesforce Case` from `servicenow/rest_message_notes.md` and an async business rule from `servicenow/business_rule_async_sync.js`.

Salesforce auth inbound: External Client App, not a Connected App. JWT bearer or client credentials. My Domain URL only.

## Tests

Apex tests mock the callout. They do not need a live PDI.

```bash
sf apex run test --test-level RunLocalTests --code-coverage --target-org lab
```

Repo QA (no orgs required):

```bash
python3 -m pytest tests -q
```
