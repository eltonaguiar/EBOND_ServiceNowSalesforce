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
| Edited the Incident, Case unchanged, no log line | Rule never ran: still guarded on `u_sync_source`, or Insert/Update wrong, or rule inactive | See [Case did not update](#no-update). Run the background probe first. |
| Edited the Incident, Case unchanged, `EBOND patch failed` in syslog | Rule ran; the HTTP call failed | Run the background probe to get the status code, then match it in the table above. |
| REST step missing in Flow Designer | Integration Hub not on the PDI | Stay on Table API. That is not a failed lab. |

## Case did not update after editing the Incident {#no-update}

Work these in order. Each one splits the problem in half, so stop as soon as you get a different result.

**1. Prove the REST call works, without the business rule.** In ServiceNow open **System Definition → Scripts - Background** (or `sys.scripts.do`), paste this and click **Run script**:

```javascript
var r = new sn_ws.RESTMessageV2('EBOND Salesforce Case', 'patch_case');
r.setStringParameterNoEscape('snow_sys_id', 'PASTE_THE_INCIDENT_SYS_ID_HERE');
r.setStringParameterNoEscape('subject', 'probe from background script');
r.setStringParameterNoEscape('description', 'probe');
r.setStringParameterNoEscape('number', 'INC_YOUR_NUMBER');
r.setHttpTimeout(20000);
var resp = r.execute();
gs.info('STATUS=' + resp.getStatusCode());
gs.info('BODY=' + resp.getBody());
gs.info('ERR=' + resp.getErrorMessage());
```

Read the result:

| STATUS | Meaning | Next |
|---|---|---|
| `200` or `204` | REST message, OAuth, endpoint and body are all correct | The problem is the **rule**, not the REST setup. Go to step 2. |
| `401` | OAuth token rejected | Re-check the OAuth profile and the External Client App consumer key/secret. |
| `404` | Wrong My Domain, or `Snow_Sys_Id__c` is not the External ID on the Case | Confirm the Case shows **ServiceNow Sys Id** filled in. |
| `400` | Body rejected — usually a missing `Content-Type: application/json` or a broken `${param}` | Compare the Content field to Lab 3 Step 3. |
| Exception, no status | The REST Message or method name does not resolve | Names are case sensitive: `EBOND Salesforce Case` / `patch_case`. |

**2. If step 1 returned 200, check the rule.** All four must be true:

- The rule is **Active**.
- **When to run** = `async`, and on the **Advanced** tab **Update is checked** and **Insert is unchecked**.
- The **Script** no longer contains `current.u_sync_source == 'salesforce'`. That guard returns on every edit of a Flow-created Incident, so the write-back can never fire.
- **Filter** = `u_ebond_sf_case_id` is not empty.

**3. If the rule is correct, make a NEW edit.** An async rule only runs on future changes; it does not replay the edit you already made. Change the short description again (add a space, save) and wait five to ten seconds.

**4. Still nothing? Look for the log line.** Open `syslog.list` filtered on message contains `EBOND`. A `EBOND patch failed NNN` entry means the rule ran and the HTTP call failed. No entry at all means the rule never ran — go back to step 2 and re-read the Advanced tab.

**5. Confirm the direction.** The Case only changes when the Incident is edited **after** the rule was fixed. If Salesforce still shows the old Subject, also confirm you are looking at the right Case — match `ServiceNow Sys Id` on the Case to the Incident's `sys_id`, not the Case number.

## Where to look {#logs}

- ServiceNow: `syslog.list`, filter message contains `EBOND`. Outbound HTTP log is **System Logs > Outbound HTTP Requests**.
- Salesforce: Setup → **Debug Logs** for the user who created the Case. Also **Named Credentials** → principal access on the permission set.
- Apex tests in the repo do not call your PDI. A green `sf apex run test` does not prove Lab 2 against your instance. The Case you create does.
