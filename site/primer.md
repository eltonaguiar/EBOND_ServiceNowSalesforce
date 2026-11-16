---
layout: default
title: Primer
order: -2
permalink: /primer/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#words">Words this lab uses</a></li>
      <li><a href="#records">The two records</a></li>
      <li><a href="#keys">Correlation keys</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>You do not need the certification vocabulary. You need six words, two records, and one shared id.</p>
</div>

## Words this lab uses {#words}

| Word | Plain meaning |
|------|----------------|
| **PDI** | Free ServiceNow instance at `devNNNNN.service-now.com`. Yours for learning. It sleeps, and ServiceNow can take it back if you ignore it. |
| **Developer Edition** | Free Salesforce org. API is on. Storage is tiny (about 5 MB). Fine for this lab. |
| **My Domain** | The Salesforce hostname you must use for APIs. It ends in `.my.salesforce.com`. |
| **Table API** | ServiceNow's built-in REST for any table. Create an Incident with `POST /api/now/table/incident`. |
| **Named Credential** | Salesforce's place to store "call this URL, with this login" so Apex does not hold a password. |
| **External Client App** | How a new Salesforce org lets another system log in. Replaces Connected Apps for new work. |
| **External Id** | A Salesforce field that is unique, so an upsert updates the same Case instead of creating a second one. |
| **sys_id** | ServiceNow's 32-character id for one record. Do not invent it. Read it from the create response. |
| **Queueable** | Apex that runs after the Case save, so the callout is allowed. A trigger cannot call out in the same save. |

## The two records {#records}

| | ServiceNow | Salesforce |
|--|------------|------------|
| Object | Incident (`incident`) | Case |
| Title | `short_description` | `Subject` |
| Body | `description` | `Description` |
| Who owns state | ServiceNow | — |
| Who owns subject | — | Salesforce |

## Correlation keys {#keys}

| Stored where | Field | Holds |
|--------------|-------|-------|
| Incident | `u_ebond_sf_case_id` | Salesforce Case Id |
| Incident | `u_sync_source` | `salesforce` or `servicenow` |
| Case | `Snow_Sys_Id__c` | Incident `sys_id` |
| Case | `Snow_Number__c` | `INC0010…` |
| Case | `Snow_Sync_Source__c` | `salesforce` or `servicenow` |

If the key already exists, update. If not, create, then write the key. That stops duplicates. It does **not** stop loops. [Lab 4]({{ '/labs/04-ownership/' | relative_url }}) does that.
