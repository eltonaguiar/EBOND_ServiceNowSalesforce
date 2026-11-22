---
layout: default
title: Troubleshooting
lab: 5
time: Reference
level: Reference
order: 5
permalink: /labs/05-troubleshooting/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#first">First hour</a></li>
      <li><a href="#matrix">Failure matrix</a></li>
      <li><a href="#logs">Where to look</a></li>
    </ol>
  </div>
</nav>

## First hour {#first}

Most stops are one of these four: the PDI is asleep, the Salesforce host is the Lightning URL, the Named Credential principal was not granted, or the HTTP call ran before the Case save committed.

## Failure matrix {#matrix}

| What you see | Cause | Fix |
|--------------|-------|-----|
| Instance XML / "unavailable" | PDI hibernating | Wake it on the Developer Site. Recheck the URL. |
| curl 401 | Wrong password, or user locked | Reset from the Developer Site. Do not keep retrying. |
| curl 400, empty body | Missing Accept or Content-Type | Send both as `application/json`. |
| Incident missing after Case save | Flow on the sync path | Move the HTTP call to the asynchronous path. |
| `uncommitted work pending` | Callout in the same transaction as the insert | Queueable, or Flow async path. Not a before-save Flow. |
| 404 on Salesforce PATCH | `Snow_Sys_Id__c` not on that Case, or wrong My Domain | Lab 2 must have written the sys id. Host must be `.my.salesforce.com`. |
| Token call to `login.salesforce.com` fails | Client credentials requires My Domain | Use the My Domain token URL only. |
| Connected App button missing | Spring '26 block | External Client App Manager. |
| `x_snc_ebond_*` will not save | Reserved scope | Use `u_ebond_sf_case_id`. |
| Two Incidents per Case | Lookup field empty on the first write | Confirm `u_ebond_sf_case_id` is in the POST body. |
| Updates bounce | Flag not set | Lab 4. Both guards must be in place. |
| Case never updates after a human edit in ServiceNow | The Lab 3 rule is guarded on `u_sync_source`, which Lab 2 stamps `salesforce` at creation and never changes | Remove that guard. Run the rule **Update only** (Insert unchecked); guard on the Case link, not on which system created the record. |
| `u_sync_source` reads `salesforce` on every linked Incident | Expected — Lab 2 writes it as a birth label | Leave it. It is not a loop guard; the return path works from Update-only + the Case-link check. |
| REST step missing in Flow Designer | Integration Hub not on the PDI | Stay on Table API. That is not a failed lab. |

## Where to look {#logs}

- ServiceNow: `syslog.list`, filter message contains `EBOND`. Outbound HTTP log is **System Logs > Outbound HTTP Requests**.
- Salesforce: Setup → **Debug Logs** for the user who created the Case. Also **Named Credentials** → principal access on the permission set.
- Apex tests in the repo do not call your PDI. A green `sf apex run test` does not prove Lab 2 against your instance. The Case you create does.
