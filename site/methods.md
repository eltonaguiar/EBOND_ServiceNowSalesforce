---
layout: default
title: Methods
order: -1
permalink: /methods/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#matrix">What you can use</a></li>
      <li><a href="#pick">What this lab uses</a></li>
      <li><a href="#skip">What to skip on the free tier</a></li>
    </ol>
  </div>
</nav>

## What you can use {#matrix}

| Method | Direction | Free-tier? | This lab |
|--------|-----------|------------|----------|
| Table API | into ServiceNow | Yes | Lab 1 and the Apex default |
| Scripted REST | into ServiceNow | Yes | Optional. More control, same result. |
| Flow HTTP Callout | Salesforce → ServiceNow | Yes, on an async path | Alternate to Apex in Lab 2 |
| Apex Queueable + Named Credential | Salesforce → ServiceNow | Yes | Lab 2 default |
| REST Message + async Business Rule | ServiceNow → Salesforce | Yes | Lab 3 |
| Integration Hub spoke | either | Often **no** on a PDI | Not the POC path |
| Salesforce Connect | read ServiceNow inside Salesforce | License-sensitive | Read-only option, not this POC |
| Connected App | into Salesforce | New ones blocked since Spring '26 | Do not use |
| Salesforce Functions | either | Retired | Do not use |

## What this lab uses {#pick}

One-way first. [Lab 1]({{ '/labs/01-table-api/' | relative_url }}) posts JSON and an Incident appears. That proves the network and the password before any automation.

Then Salesforce pushes with a Named Credential, because the password stays in Salesforce setup, not in Apex. The call runs in a Queueable so it happens after the Case is saved.

Then ServiceNow pushes back with a REST Message. The business rule is **async**, and it returns immediately if `u_sync_source` is `salesforce`. That is the loop guard.

## What to skip on the free tier {#skip}

Integration Hub REST steps need a plugin a PDI may refuse to activate. If **Flow Designer → REST step** is missing, you did not fail the lab. Use the Table API.

A guest Site for the webhook is unauthenticated. Do not expose the Case endpoint that way. Use an integration user.
