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
<p>You create the record in Salesforce. It is a Salesforce Case. You do not create a Case in ServiceNow. After that save, Salesforce calls ServiceNow, and ServiceNow creates an Incident. The Incident is stamped with the Salesforce Case Id, so a second save updates that same Incident instead of making another one.</p>
</div>

| You create this | In this system | It is not |
|-----------------|----------------|-----------|
| Case | Salesforce | a ServiceNow record |
| Incident | ServiceNow, created by the call | something you type in by hand in this lab |

## Objective {#objective}

A Salesforce Case insert creates or updates one ServiceNow Incident. The Incident field `u_ebond_sf_case_id` equals that Salesforce Case Id.

## ServiceNow fields {#fields-sn}

ServiceNow already has the integration fields. Incident inherits them from Task. Your Lab 1 response body showed them empty:

| Field | What it is for | This lab |
|-------|----------------|----------|
| `correlation_id` | The other system's id. One string. The usual place for a Salesforce Case Id. | Leave it alone. Pretend another integration already stores its key here. |
| `correlation_display` | The human-readable value from that other system, such as a Case number. | Leave it alone. It belongs to the same other integration. |

A custom column is normal only when `correlation_id` is already taken, or when you need your own unique index so one Case cannot create two Incidents. This lab is that situation. We add `u_ebond_sf_case_id` instead of overwriting `correlation_id`.

1. Filter: **System Definition > Tables**, open **Incident**.
2. Add a string column **EBOND SF Case Id**, column name `u_ebond_sf_case_id`, length 18. This is the stand-in. It is not a second copy of `correlation_id` for fun.
3. Add a string column **Sync source**, column name `u_sync_source`, length 20. This one is also custom. It is the loop guard, not the external id.

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
6. Activate. In Salesforce, create a Case. Subject is required. Do not create an Incident yourself.

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
<li>New Salesforce Case, subject filled in. You created this one.</li>
<li>Within a minute, the ServiceNow Incident list shows that subject. ServiceNow created this one.</li>
<li>ServiceNow Incident <code>u_ebond_sf_case_id</code> equals the Salesforce Case Id (15 or 18 characters).</li>
<li>Salesforce Case <code>Snow_Number__c</code> shows the INC number.</li>
<li>Save that same Salesforce Case again only if you are testing update. A second push must not create a second ServiceNow Incident.</li>
</ul>
