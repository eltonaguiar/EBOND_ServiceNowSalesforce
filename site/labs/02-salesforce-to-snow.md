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
| `correlation_id` | The other system's id. One string. The usual place for a Salesforce Case Id. | Leave this field alone. We are pretending another integration already stores its key here, so we create our own equivalent field instead. |
| `correlation_display` | The human-readable value from that other system, such as a Case number. | Leave this field alone too. It belongs to that same pretend integration. We are not creating an equivalent for it. |

A custom column is normal only when `correlation_id` is already taken, or when you need your own unique index so one Case cannot create two Incidents. This lab is that situation. We add `u_ebond_sf_case_id` instead of overwriting `correlation_id`.

Two ways to open the Incident table. Either one is fine.

- Filter navigator: **System Definition > Tables**, open **Incident**.
- From an Incident form: the menu (three lines, top left of the form) → **Configure > Table**. That is the path used in this run. The form then says the table is in the **Global** application and extends **Task**.

On the Columns related list, click **New**.

1. Table `Incident [incident]`. Type **String**.
2. Column label **EBOND SF Case Id**. Column name `u_ebond_sf_case_id`. Max length 18. This is the stand-in. It is not a second copy of `correlation_id` for fun.
3. Repeat for **Sync source**, column name `u_sync_source`, length 20. That one is the loop guard, not the external id.

### Why `x_snc_` is rejected

`x_snc_ebond_sf_case_id` is not a field you are allowed to invent.

ServiceNow splits names by who owns the application:

| Prefix | Who owns it | Example |
|--------|-------------|---------|
| none, or `u_` | Global scope. `u_` is the prefix for a custom field you add in Global. | `u_ebond_sf_case_id` |
| `x_<company>_<app>_` | A scoped app created by that company. The company code is theirs. | `x_acme_bond_case_id` |
| `x_snc_` | ServiceNow. `snc` is ServiceNow's own company code. | a field inside a ServiceNow Store app |

The platform blocks `x_snc_` so a PDI cannot create a column that looks like it belongs to a ServiceNow product. If it allowed that, an update of a real ServiceNow app could collide with your column, and other instances would treat your field as if ServiceNow had shipped it. Your company code is not `snc`, so you cannot mint that prefix. Use `u_`.

## Salesforce fields {#fields-sf}

The gear icon is at the top right of Salesforce, next to the bell. Click it, then **Setup**. That opens Setup. It is not the same screen as the Case you create later.

In Setup, open **Object Manager**. Search `case`. Open the row whose API name is **Case**, not Case Related Issue. Then **Fields & Relationships** → New.

Do not type `__c` in Field Name. Salesforce adds that suffix. `Snow_Sys_Id__c` fails because the name you typed already contains two underscores in a row. Type `Snow_Sys_Id`. The API name becomes `Snow_Sys_Id__c`.

The wizard is four steps. The checkboxes below are on **Step 2 of 4, Enter the details**. They are not on a later security page.

| Field Label (what you see) | Field Name (what you type) | API name Salesforce creates | Type | Extra Details, on Step 2 |
|----------------------------|----------------------------|-----------------------------|------|--------------------------|
| ServiceNow Sys Id | `Snow_Sys_Id` | `Snow_Sys_Id__c` | Text(32) | Length 32. Unique, case insensitive. External ID checked. |
| ServiceNow Number | `Snow_Number` | `Snow_Number__c` | Text(40) | Length 40. Leave Unique and External ID unchecked. |
| Sync Source | `Snow_Sync_Source` | `Snow_Sync_Source__c` | Text(20) | Length 20. Leave Unique and External ID unchecked. |

**Step 3 of 4, field-level security.** Use the defaults. Do not build a permission set for this. You are the System Administrator who creates the Case and reads the field, and the default visible box for that profile is enough. A different integration user would need Visible, and Editable if that user writes the field. This lab does not use one.

**Step 4 of 4, Add to page layouts.** Check every Case layout. On this org that is Case (Marketing) Layout, Case (Sales) Layout, Case (Support) Layout, Case Layout, and Close Case Layout. The field is added as the last field in the first two-column section. Then click Save, or Save & New for the next field.

### What each layout box does

These boxes do not create the field. Step 2 already did that. They only choose which Case screens show it.

| Box | Purpose |
|-----|---------|
| Case Layout | The default Case page. This is the one you will open for most of this lab. |
| Case (Support) Layout | The Case page the Support app uses. |
| Case (Sales) Layout | The Case page the Sales app uses. |
| Case (Marketing) Layout | The Case page the Marketing app uses. |
| Close Case Layout | The page shown while closing a Case. Not the page for a new or open Case. |

If you do not check a box, that screen does not show the field. The field is still on the Case. The API, Flow, and Apex can still read and write it. A report can still show it, if the report includes that field and your user can see the field. An unchecked layout does not remove it from reports.

QA follows the layout you checked. If you only check Close Case Layout, the field appears when you close a Case, and it does not appear on an open Case. You can still check the value without that screen: run a report that includes `Snow_Sys_Id__c`, or call the API, or add the field to Case Layout and open an open Case. Checking every box avoids that hunt.

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
