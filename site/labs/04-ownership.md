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
      <li><a href="#guards">Guards, side by side</a></li>
      <li><a href="#manual">A person edits a record</a></li>
      <li><a href="#prove">Prove it</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>If both sides copy every field on every event, they argue forever. Pick an owner for each field, and make each automation fire on one event only: Salesforce on create, ServiceNow on update.</p>
</div>

## Objective {#objective}

You can say, for each field, which system wins, and you can show that one save does not bounce.

## Who owns what {#owners}

| Field | Owner | Other side |
|-------|-------|------------|
| Subject / short description | Last writer | Lab 2 sets it once when the Case is created. Lab 3 pushes `short_description` → `Subject` on every later Incident update, so a human edit in ServiceNow wins. |
| Priority | Salesforce | Lab 2 sends `urgency`/`impact`. Lab 3's body does **not** include priority, so ServiceNow never overwrites it. If you add it, map High/Medium/Low to urgency 1/2/3 — `priority` and `urgency` are not the same field. |
| State, assignment group, work notes | ServiceNow | ServiceNow only. The Lab 3 body does not send them and the Lab 2 Flow does not read them. |
| Description | Last writer | Both directions copy it. There is no echo to dodge: the Flow is create-only and the rule is update-only, so neither side re-triggers on the other's write. |

## Why loops happen {#loops}

A loop needs two edges that both fire on **update**. This lab has one edge on *create* and one on *update*, so the circle never closes by itself:

1. Salesforce creates a Case. The record-triggered Flow posts an Incident with `u_sync_source = salesforce`.
2. That **insert does not fire the business rule.** The rule is *Update only* (Lab 3, Step 1) — Insert is unchecked.
3. An agent edits the Incident. The async business rule PATCHes the Case: Subject, Description, `Snow_Number__c`, `Snow_Sync_Source__c`.
4. That **Case update does not fire the Flow.** The Flow's entry condition is “A record is created” (Lab 2).

A loop only appears if step 4 becomes an *update* trigger. Then the Flow needs its own guard: skip when `Snow_Sync_Source__c` = `servicenow`.

### Which automation are we talking about? {#which}

The phrase “that insert fires the ServiceNow business rule” names exactly one thing: row 2 below. It is a **business rule**, not a Flow and not a script include, and it belongs to **Lab 3** — Lab 2 only creates the record that Lab 3 watches.

| # | Automation | System | Type | Defined in | Fires when | Guard it carries |
|---|---|---|---|---|---|---|
| 1 | `EBOND Case to Incident` | Salesforce | Record-Triggered Flow (async path) | **Lab 2** | Case **created** — create only, never on update | The entry condition itself: *A record is created* |
| 2 | `Ebond Salesforce Incident Async` | ServiceNow | **Business rule**, `async`, after **update** | **Lab 3** | Incident **updated** (Insert unchecked) | Filter: `u_ebond_sf_case_id` is not empty; `return` when the link is empty |
| 3 | `EBOND Salesforce Case` / `patch_case` (or `patch_case_test`) | ServiceNow | REST Message + HTTP Method (outbound) | **Lab 3** | Called by row 2, never runs on its own | None — it is a pipe, not a trigger |
| 4 | OAuth Entity Profile `Salesforce OAuth Client Credentials` | ServiceNow | Credential record | **Lab 3** | Never fires; row 2 uses it to get a token | None |

## Guards, side by side {#guards}

A **guard** is the first check that makes an automation do nothing. The two systems need *different* guards, because they react to different events.

| | ServiceNow guard | Salesforce guard |
|---|---|---|
| Where it lives | The filter on *When to run*, plus the first lines of the script | The Flow's entry condition |
| What it tests | `u_ebond_sf_case_id` is not empty; Insert is off | *A record is created* on Case |
| What it stops | Saves of Incidents that have no Case to update; and pushing back the moment the Incident is created | Reacting to the Case update that ServiceNow just made |
| What it must **not** test | `u_sync_source` | — |
| Why that matters | That field is a birth label: Lab 2 stamps `salesforce` once and never changes it. Testing it would return on every later human edit and the Case would never update — the return path dies silently. | The Flow only ever sees *created* Cases, so a ServiceNow write-back cannot re-enter. |

<div class="warn">
<span class="label">The rule to remember</span>
<p>Guard on <strong>the event</strong>, not on the data. “Created vs updated” is reliable. “This field says salesforce” is not, because the field does not change when a person edits the record.</p>
<p>If you later make the Flow fire on Case <em>update</em>, both sides need a guard and they must test the <em>writer</em>: Salesforce checks <code>Snow_Sync_Source__c != 'servicenow'</code>, ServiceNow checks <code>sys_updated_by</code> against an integration user. A data field cannot tell you who changed the record just now.</p>
</div>

## A person edits a record {#manual}

No flag flipping is needed. The rule is Update-only and tests only the Case link, so any human edit to a linked Incident is pushed:

| Action | Rule runs? | Why |
|---|---|---|
| Edit the short description on a linked Incident | **Yes** | Update + link present |
| Edit an Incident with no `u_ebond_sf_case_id` | No | Filter stops it |
| Create a Case in Salesforce | No | Lab 2 inserts the Incident; Insert is unchecked on the rule |
| Update a Case in Salesforce | No | The Flow is create only |
| Save an Incident without changing anything | No | ServiceNow does not update the row, so no rule event fires |

Do not use `setWorkflow(false)` to “make it quiet.” That also skips the rules you still want. Running the rule on the update event is the smaller switch.

<div class="note">
<span class="label">Screenshot</span>
<p>Save <code>04-ownership.png</code> into <a href="https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce_RUN/blob/main/README.MD">the run repo</a>. A <code>syslog.list</code> filter on EBOND that shows one write, not a loop, is the better shot if you have it.</p>
</div>

## Prove it {#prove}

<ul class="check">
<li>Create a Case. Exactly one Incident. Exactly one follow-up write, or none, on the Case. Not a stream of updates.</li>
<li>System log (<code>syslog.list</code>) has no repeating EBOND error for that number.</li>
<li>You can point at each field and name the owner.</li>
</ul>
