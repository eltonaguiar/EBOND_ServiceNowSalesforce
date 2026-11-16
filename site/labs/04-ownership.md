---
layout: default
title: Ownership and loops
lab: 4
time: 20 min
level: Design
order: 4
permalink: /labs/04-ownership/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#objective">Objective</a></li>
      <li><a href="#owners">Who owns what</a></li>
      <li><a href="#loops">Why loops happen</a></li>
      <li><a href="#manual">A person edits a record</a></li>
      <li><a href="#prove">Prove it</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>If both sides always copy every field, they argue forever. Pick an owner for each field. Ignore the echo of your own write.</p>
</div>

## Objective {#objective}

You can say, for each field, which system wins, and you can show that one save does not bounce.

## Who owns what {#owners}

| Field | Owner | Other side |
|-------|-------|------------|
| Subject / short description | Salesforce | ServiceNow displays it. A ServiceNow edit of the title is a conflict, not a silent overwrite. |
| Priority | Salesforce | Map High/Medium/Low to urgency 1/2/3 when pushing. Do not map ServiceNow `priority` and `urgency` as if they were the same field. |
| State, assignment group, work notes | ServiceNow | Salesforce does not push these back. |
| Description | Last writer, only if the sync-source flag says a human edited it | Do not copy it on the echo. |

## Why loops happen {#loops}

1. Salesforce creates a Case and posts an Incident with `u_sync_source = salesforce`.
2. That insert fires the ServiceNow business rule.
3. If the rule does not check the flag, it PATCHes the Case.
4. The Case update fires the Flow or the trigger, which posts the Incident again.

The lab stops that in two places:

- ServiceNow rule returns when `u_sync_source` is `salesforce`.
- Salesforce trigger skips when `Snow_Sync_Source__c` is `servicenow`.

Correlation ids stop duplicates. They do not stop this loop. Both are required.

## A person edits a record {#manual}

If an agent types in the Incident description, set `u_sync_source` to `servicenow` (or clear it) before save so the rule is allowed to run. If Salesforce later sends a new description, Salesforce owns that push and should set the flag back to `salesforce`.

Do not use `setWorkflow(false)` to "make it quiet." That also skips the rules you still want. The flag is the smaller switch.

## Prove it {#prove}

<ul class="check">
<li>Create a Case. Exactly one Incident. Exactly one follow-up write, or none, on the Case. Not a stream of updates.</li>
<li>System log (<code>syslog.list</code>) has no repeating EBOND error for that number.</li>
<li>You can point at each field and name the owner.</li>
</ul>
