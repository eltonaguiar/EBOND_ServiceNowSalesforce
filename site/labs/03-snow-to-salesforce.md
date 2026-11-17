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
      <li><a href="#bulk">Linking existing tickets (bulk)</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>ServiceNow tells Salesforce "this Incident changed." Salesforce finds the Case by the Incident id and updates it. It does not create a second Case.</p>
</div>

## Objective {#objective}

Changing an Incident that already has `u_ebond_sf_case_id` updates the matching Case. The match key is `Snow_Sys_Id__c`.

### What if an Incident has no `u_ebond_sf_case_id`

`u_ebond_sf_case_id` is the link between an Incident and a Salesforce Case. It holds the Salesforce record Id (the 18-character `500…` value) of the Case that created the Incident.

- If the field is **empty**, the Incident is **not linked to Salesforce**. This lab's business rule and the REST call both depend on that field being set, so an empty value means **nothing happens**: ServiceNow will not call Salesforce, and Salesforce has no way to find the owning Case.
- This is expected for any Incident that was created manually in ServiceNow, by email, or by another integration — those Incidents never came from a Salesforce Case, so there is no Case to update. The field is intentionally left blank for them.
- The async rule guards on this (filter `u_ebond_sf_case_id` is not empty, plus the `if (!current.u_ebond_sf_case_id) return;` check). It only acts on Incidents that have a link. Unlinked Incidents are simply skipped.

So the presence of `u_ebond_sf_case_id` is the definitive signal of "this Incident belongs to a Salesforce Case." If it is missing, the Incident is independent of Salesforce and will never be written back.

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

<div class="note">
<span class="label">Screenshot</span>
<p>Save <code>03-external-client-app.png</code>, <code>03-rest-message-200.png</code>, and <code>03-case-after-update.png</code> into <a href="https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce_RUN/blob/main/README.MD">the run repo</a>. Cover the consumer secret.</p>
</div>

## Prove it {#prove}

<ul class="check">
<li>REST Message test against a known <code>Snow_Sys_Id__c</code> returns 200, not 404.</li>
<li>Edit the Incident short description by hand. Set <code>u_sync_source</code> to blank or <code>servicenow</code> first, or the rule will skip.</li>
<li>The Case subject changes. <code>Snow_Sync_Source__c</code> becomes <code>servicenow</code>.</li>
<li>No second Case was created.</li>
</ul>

## Linking existing tickets (bulk) {#bulk}

<details>
<summary>Rough steps to link existing Salesforce Cases to existing Incidents</summary>

This lab links one Incident at a time as it is created. If you already have Case in both systems and want to link them retroactively, here is the rough shape. Scope it to your need — do not blindly link everything.

1. **Decide the scope of what should be linked.** Examples:
   - Only **active** Incidents (state 1–3) with a matching Case.
   - Only Incidents of a certain **type / category / assignment group** (e.g. `category = inquiry`, or a specific `assignment_group`).
   - Only Incidents **created in the last N days**.
   - Only Incidents that arrive from a specific source (e.g. the Salesforce flow).
   An un-scoped link of *all* Incidents is usually wrong: many are unrelated to Salesforce.
2. **Define the match key.** Decide which field links a Case to an Incident. In this lab the field is `u_ebond_sf_case_id` = Salesforce Case Id, and the reverse is `Snow_Sys_Id__c` on the Case. Match on one real identifier (Case Id, or Case Number).
3. **Build the relation in ServiceNow.** For each Incident in scope, set `u_ebond_sf_case_id` to the matching Case's Id. Do this with a scripted business rule / scheduled job, a bulk Scripted REST call, or the REST API Explorer in bulk — not by hand for hundreds of rows.
4. **Backfill the SF field.** For each linked Incident, set the Case's `Snow_Number__c` and `Snow_Sys_Id__c` (and `Snow_Sync_Source__c`) so the link is visible from the Salesforce side too. This is the reverse of step 3.
5. **Sync matching status.** Once links exist, run a reconciliation so open Incidents update their Cases (and vice versa) — reuse the PATCH business rule logic from this lab for one-way, or a scheduled sync for two-way.
6. **Test on a sample first.** Link a handful, verify the Case updates, then widen the scope. Always keep a rollback (a saved copy of the original `u_ebond_sf_case_id` / Case fields before you overwrite them).

> Reminder: creating a link does not create a duplicate Case. It only connects the two existing records. Keep the loop guard (`u_sync_source`) in mind so a bulk link does not trigger a write-back loop.
</details>
