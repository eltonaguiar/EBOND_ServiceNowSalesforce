---
layout: default
title: ServiceNow to Salesforce
lab: 3
time: 40 min
level: Return path
order: 3
permalink: /labs/03-snow-to-salesforce/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#objective">Objective</a></li>
      <li><a href="#eca">External Client App</a></li>
      <li><a href="#rest">REST Message</a></li>
      <li><a href="#rule">Async business rule</a></li>
      <li><a href="#prove">Prove it</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>ServiceNow tells Salesforce "this Incident changed." Salesforce finds the Case by the Incident id and updates it. It does not create a second Case.</p>
</div>

## Objective {#objective}

Changing an Incident that already has `u_ebond_sf_case_id` updates the matching Case. The match key is `Snow_Sys_Id__c`.

## External Client App {#eca}

Do this in Salesforce. Do not create a Connected App.

1. Setup → **External Client App Manager** → New.
2. Distribution **Local**. Enable OAuth.
3. For a server-to-server lab, enable **Client Credentials**. Assign an integration user who has API access and edit rights on Case. Callback URL can be a placeholder for this flow.
4. Policies → Permitted Users → **Admin approved users are pre-authorized**. Assign a permission set to that user.
5. Open **Consumer Key and Secret**. Those are the client id and client secret. They stay in ServiceNow's credential record, not in a file.

Token URL (My Domain only):

```text
https://YOUR_DOMAIN.my.salesforce.com/services/oauth2/token
```

`login.salesforce.com` does not work for client credentials.

## REST Message {#rest}

In the PDI: **System Web Services > Outbound > REST Message** → New.

| Field | Value |
|-------|-------|
| Name | `EBOND Salesforce Case` |
| Endpoint | `https://YOUR_DOMAIN.my.salesforce.com/services/data/v68.0` |
| Authentication | OAuth 2.0, profile pointed at the token URL above |

HTTP method:

| Field | Value |
|-------|-------|
| Name | `patch_case` |
| HTTP method | PATCH |
| Endpoint | `https://YOUR_DOMAIN.my.salesforce.com/services/data/v68.0/sobjects/Case/Snow_Sys_Id__c/${snow_sys_id}` |

Body. Do not put `Snow_Sys_Id__c` in the JSON. It is already in the URL.

```json
{
  "Subject": "${subject}",
  "Description": "${description}",
  "Snow_Number__c": "${number}",
  "Snow_Sync_Source__c": "servicenow"
}
```

Use **Test** on the method with a real `sys_id` from Lab 2 before you automate it. Expect 200.

## Async business rule {#rule}

**System Definition > Business Rules** → New. Table `incident`. When **async**. Insert and Update. Filter: `u_ebond_sf_case_id` is not empty.

```javascript
(function executeRule(current, previous) {
    if (current.u_sync_source == 'salesforce') {
        return;
    }
    if (!current.u_ebond_sf_case_id) {
        return;
    }
    var r = new sn_ws.RESTMessageV2('EBOND Salesforce Case', 'patch_case');
    r.setStringParameterNoEscape('snow_sys_id', current.getUniqueValue());
    r.setStringParameterNoEscape('subject', current.getValue('short_description') || '');
    r.setStringParameterNoEscape('description', current.getValue('description') || '');
    r.setStringParameterNoEscape('number', current.getValue('number') || '');
    r.setHttpTimeout(20000);
    var resp = r.execute();
    if (resp.getStatusCode() < 200 || resp.getStatusCode() >= 300) {
        gs.error('EBOND patch failed ' + resp.getStatusCode());
    }
})(current, previous);
```

The first line is the loop guard. Lab 2 set `u_sync_source` to `salesforce`, so the echo of that create does not call Salesforce again.

## Prove it {#prove}

<ul class="check">
<li>REST Message test against a known <code>Snow_Sys_Id__c</code> returns 200, not 404.</li>
<li>Edit the Incident short description by hand. Set <code>u_sync_source</code> to blank or <code>servicenow</code> first, or the rule will skip.</li>
<li>The Case subject changes. <code>Snow_Sync_Source__c</code> becomes <code>servicenow</code>.</li>
<li>No second Case was created.</li>
</ul>
