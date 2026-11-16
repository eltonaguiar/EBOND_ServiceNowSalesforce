# REST Message — EBOND Salesforce Case

Create in **System Web Services > Outbound > REST Message**.

| Field | Value |
|-------|-------|
| Name | `EBOND Salesforce Case` |
| Endpoint | `https://${instance}/services/data/v68.0` |
| Authentication | OAuth 2.0 |
| OAuth profile | Application Registry pointing at the Salesforce External Client App (JWT bearer or client credentials). Token URL: `https://<MyDomain>.my.salesforce.com/services/oauth2/token` |

HTTP method record:

| Field | Value |
|-------|-------|
| Name | `patch_case` |
| HTTP method | PATCH |
| Endpoint | `https://${instance}/services/data/v68.0/sobjects/Case/Snow_Sys_Id__c/${snow_sys_id}` |
| Content | see body below |

Body (`setStringParameterNoEscape` — do not XML-escape JSON):

```json
{
  "Subject": "${subject}",
  "Description": "${description}",
  "Snow_Number__c": "${number}",
  "Snow_Sync_Source__c": "servicenow"
}
```

Do not send `Snow_Sys_Id__c` in the body. It is the external-id path segment.

Business rule that calls this method: `lab/servicenow/business_rule_async_sync.js`.
Set the rule **When = async**, table `incident`, on update. Filter: `u_sf_case_id` is not empty.
