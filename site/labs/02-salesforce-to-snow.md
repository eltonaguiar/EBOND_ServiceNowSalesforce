---
layout: default
title: Salesforce to ServiceNow
lab: 2
time: 40 min
level: One-way
order: 2
permalink: /labs/02-salesforce-to-snow/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#objective">Objective</a></li>
      <li><a href="#fields-sn">ServiceNow fields</a></li>
      <li><a href="#fields-sf">Salesforce fields</a></li>
      <li><a href="#cred">Named Credential</a></li>
      <li><a href="#flow">Flow path (no Apex)</a></li>
      <li><a href="#apex">Apex path</a></li>
      <li><a href="#prove">Prove it</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>Create a Case. Salesforce calls ServiceNow after the save. An Incident appears, stamped with the Case Id so a second save updates instead of duplicating.</p>
</div>

## Objective {#objective}

A Case insert creates or updates one Incident. The Incident field `u_ebond_sf_case_id` equals the Case Id.

## ServiceNow fields {#fields-sn}

1. Filter: **System Definition > Tables**, open **Incident**.
2. Add a string column **EBOND SF Case Id**, column name `u_ebond_sf_case_id`, length 18.
3. Add a string column **Sync source**, column name `u_sync_source`, length 20.

You cannot create `x_snc_ebond_sf_case_id` on a free PDI. `x_snc_` is ServiceNow's own scope prefix.

## Salesforce fields {#fields-sf}

Setup → **Object Manager** → **Case** → **Fields & Relationships** → New.

| Label | API name | Type | Extra |
|-------|----------|------|-------|
| ServiceNow Sys Id | `Snow_Sys_Id__c` | Text(32) | External Id, Unique |
| ServiceNow Number | `Snow_Number__c` | Text(40) | |
| Sync Source | `Snow_Sync_Source__c` | Text(20) | |

Put the three fields on the Case page layout so you can see them.

## Named Credential {#cred}

Setup → Quick Find **Named Credentials**.

1. **External Credentials** → New. Label `EBOND ServiceNow`. Protocol **Custom** if you are using Basic auth for the lab. Add a principal. Store the PDI username and password on that principal. Grant the principal to your user with a permission set (**External Credential Principal Access**).
2. **Named Credential** → New. Label and name `EBOND_ServiceNow`. URL `https://devNNNNN.service-now.com` (no path). Link the External Credential. Enable **Generate Authorization Header**.
3. You do not also need a Remote Site Setting for that host.

## Flow path (no Apex) {#flow}

Use this if you do not want to deploy code.

1. Setup → **Flows** → New → **Record-Triggered Flow**. Object **Case**. Trigger **A record is created**. Optimize for **Actions and Related Records**.
2. On the flow, open **Add Asynchronous Path** (or the path that runs after the save commits). Do not put the HTTP call on the immediate after-save path. That path still has uncommitted work and the callout fails.
3. Action → **Create HTTP Callout**. Named Credential `EBOND_ServiceNow`. Method POST. URL path `/api/now/table/incident`.
4. Body maps `Subject` → `short_description`, `Description` → `description`, and a formula or the Case Id → `u_ebond_sf_case_id`. Also send `u_sync_source` = `salesforce`.
5. Save the returned `sys_id` into `Snow_Sys_Id__c` and `number` into `Snow_Number__c` with an Update Records element. Set `Snow_Sync_Source__c` to `salesforce`.
6. Activate. Create a Case. Subject is required.

## Apex path {#apex}

The repo class `SnowIncidentService` does the same POST, then a GET by `u_ebond_sf_case_id` so a retry patches instead of inserting again. The trigger only enqueues work. The Queueable performs the callout, in batches of 10, because a trigger cannot call out and a bulk insert cannot enqueue 200 jobs.

Deploy from the repo:

```bash
sf org login web --alias lab --instance-url https://YOUR_DOMAIN.my.salesforce.com
sf project deploy start --source-dir lab/salesforce/force-app --target-org lab
```

The callout endpoint is `callout:EBOND_ServiceNow/api/now/table/incident`. The Named Credential name must match.

<div class="note">
<span class="label">Screenshot</span>
<p>Save <code>02-case-fields.png</code>, <code>02-named-credential.png</code>, and <code>02-case-and-incident.png</code> into <a href="https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce_RUN/blob/main/README.MD">the run repo</a>. No secret in the Named Credential frame. Also useful: the permission set that grants External Credential Principal Access.</p>
</div>

## Prove it {#prove}

<ul class="check">
<li>New Case, subject filled in.</li>
<li>Within a minute, Incident list shows that subject.</li>
<li>Incident <code>u_ebond_sf_case_id</code> equals the Case Id (15 or 18 characters).</li>
<li>Case <code>Snow_Number__c</code> shows the INC number.</li>
<li>Create the same Case again only if you are testing update: a second push must not create a second Incident.</li>
</ul>
