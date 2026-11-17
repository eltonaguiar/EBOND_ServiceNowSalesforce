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
      <li><a href="#unlinked">What if an Incident has no <code>u_ebond_sf_case_id</code></a></li>
      <li><a href="#alt">No-code / low-code alternatives</a></li>
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

<div class="note">
<span class="label">Unlinked Incidents</span>
<h3 id="unlinked">What if an Incident has no <code>u_ebond_sf_case_id</code></h3>
<p><code>u_ebond_sf_case_id</code> is the link between an Incident and a Salesforce Case. It holds the Salesforce record Id (the 18-character <code>500…</code> value) of the Case that created the Incident.</p>
<ul>
<li>If the field is <strong>empty</strong>, the Incident is <strong>not linked to Salesforce</strong>. This lab's business rule and the REST call both depend on that field being set, so an empty value means <strong>nothing happens</strong>: ServiceNow will not call Salesforce, and Salesforce has no way to find the owning Case.</li>
<li>This is expected for any Incident that was created manually in ServiceNow, by email, or by another integration — those Incidents never came from a Salesforce Case, so there is no Case to update. The field is intentionally left blank for them.</li>
<li>The async rule guards on this (filter <code>u_ebond_sf_case_id</code> is not empty, plus the <code>if (!current.u_ebond_sf_case_id) return;</code> check). It only acts on Incidents that have a link. Unlinked Incidents are simply skipped.</li>
</ul>
<p>So the presence of <code>u_ebond_sf_case_id</code> is the definitive signal of "this Incident belongs to a Salesforce Case." If it is missing, the Incident is independent of Salesforce and will never be written back.</p>
</div>

## No-code / low-code alternatives {#alt}

<p>The coded path below (REST Message + async business rule) is one way to make ServiceNow update Salesforce. It is not the only one. The <strong>External Client App</strong> step (OAuth client credentials) is required for every option here, so do that part regardless. Choose one of the following instead of the REST Message + JavaScript.</p>

<details>
<summary><strong>Option A — ServiceNow Flow Designer + Salesforce spoke (low-code, recommended)</strong></summary>
<p>Replace the REST Message and the JavaScript business rule with a <strong>Flow</strong> built visually in Flow Designer, using IntegrationHub's official <strong>Salesforce spoke</strong> action ("Update Case").</p>
<ul>
<li>Trigger: <code>incident</code> record, async, when <code>u_ebond_sf_case_id</code> is not empty (same filter as the coded rule).</li>
<li>Action: Salesforce spoke → <strong>Update Case</strong>, then map <code>Subject</code>, <code>Description</code>, <code>Snow_Number__c</code>, and <code>Snow_Sync_Source__c</code>.</li>
<li>The loop guard is a Flow condition (skip when <code>u_sync_source = salesforce</code>) instead of the <code>if</code> in code.</li>
<li>No hand-written REST Message, no JavaScript. The credentials still come from the same External Client App (OAuth) you set up for the coded path.</li>
</ul>
</details>

<details>
<summary><strong>Option B — Integration platform / iPaaS connector (no-code)</strong></summary>
<p>Use a visual integration platform that ships prebuilt ServiceNow ⇄ Salesforce connectors, so no scripting or custom endpoint code is involved. Examples: Workato, Tray.io, Zapier, Automate.io, or Dell Boomi.</p>
<ul>
<li>You configure a trigger (Incident updated) and a field mapping in a UI; the platform handles auth and the call.</li>
<li>No REST Message and no business rule in ServiceNow.</li>
<li>Trade-offs: adds a third system and a license, and you still register credentials on both ends (including the External Client App).</li>
</ul>
</details>

<details>
<summary><strong>Option C — This lab's coded path (REST Message + business rule)</strong></summary>
<p>The rest of this page documents the fully coded approach: a hand-written <strong>REST Message</strong> and an <strong>async business rule</strong> in JavaScript that PATCHes the Case. It works and is good for understanding the mechanics, but it is the most code-heavy option. Use it if you want to see exactly what the Flow/spoke or iPaaS does under the hood.</p>
</details>

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
<p>This lab links one Incident at a time as it is created. If you already have Cases in both systems and want to link them retroactively, here is the rough shape. Scope it to your need — do not blindly link everything.</p>
<ol>
<li><strong>Decide the scope of what should be linked.</strong> Examples:
<ul>
<li>Only <strong>active</strong> Incidents (state 1–3) with a matching Case.</li>
<li>Only Incidents of a certain <strong>type / category / assignment group</strong> (e.g. <code>category = inquiry</code>, or a specific <code>assignment_group</code>).</li>
<li>Only Incidents <strong>created in the last N days</strong>.</li>
<li>Only Incidents that arrive from a specific source (e.g. the Salesforce flow).</li>
</ul>
An un-scoped link of <em>all</em> Incidents is usually wrong: many are unrelated to Salesforce.</li>
<li><strong>Define the match key.</strong> Decide which field links a Case to an Incident. In this lab the field is <code>u_ebond_sf_case_id</code> = Salesforce Case Id, and the reverse is <code>Snow_Sys_Id__c</code> on the Case. Match on one real identifier (Case Id, or Case Number).</li>
<li><strong>Build the relation in ServiceNow.</strong> For each Incident in scope, set <code>u_ebond_sf_case_id</code> to the matching Case's Id. Do this with a scripted business rule / scheduled job, a bulk Scripted REST call, or the REST API Explorer in bulk — not by hand for hundreds of rows.</li>
<li><strong>Backfill the SF field.</strong> For each linked Incident, set the Case's <code>Snow_Number__c</code> and <code>Snow_Sys_Id__c</code> (and <code>Snow_Sync_Source__c</code>) so the link is visible from the Salesforce side too. This is the reverse of step 3.</li>
<li><strong>Sync matching status.</strong> Once links exist, run a reconciliation so open Incidents update their Cases (and vice versa) — reuse the PATCH business rule logic from this lab for one-way, or a scheduled sync for two-way.</li>
<li><strong>Test on a sample first.</strong> Link a handful, verify the Case updates, then widen the scope. Always keep a rollback (a saved copy of the original <code>u_ebond_sf_case_id</code> / Case fields before you overwrite them).</li>
</ol>
<p>Reminder: creating a link does not create a duplicate Case. It only connects the two existing records. Keep the loop guard (<code>u_sync_source</code>) in mind so a bulk link does not trigger a write-back loop.</p>
</details>
