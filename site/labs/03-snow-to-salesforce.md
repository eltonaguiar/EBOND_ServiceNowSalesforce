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
      <li><a href="#bg">Background <span class="req">[R]</span></a></li>
      <li><a href="#path">1. Choose your integration path <span class="req">[R]</span></a>
        <ol class="toc-list">
          <li><a href="#optA">1.1A Flow Designer + Salesforce spoke (low-code)</a></li>
          <li><a href="#optB">1.1B iPaaS connector (no-code)</a></li>
          <li><a href="#optC">1.1C Coded REST Message + business rule</a></li>
        </ol>
      </li>
      <li><a href="#eca">2. External Client App <span class="req">[R]</span></a></li>
      <li><a href="#rest">3. REST Message <span class="req">[R · C]</span></a></li>
      <li><a href="#rule">4. Async business rule <span class="req">[R · C]</span></a></li>
      <li><a href="#prove">5. Prove it <span class="req">[R]</span></a></li>
      <li><a href="#bulk">6. Linking existing tickets (bulk) <span class="req">[O]</span></a></li>
      <li><a href="#notes">7. Post-lab notes <span class="req">[O]</span></a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>ServiceNow tells Salesforce "this Incident changed." Salesforce finds the Case by the Incident id and updates it. It does not create a second Case.</p>
</div>

<div class="note">
<span class="label">Mandatory vs optional</span>
<p>Each section is marked with a tag. Do the sections marked <code>[R]</code>; skip the rest if they do not apply.</p>
<ul>
<li><code>[R]</code> — <strong>Required</strong> for everyone doing this lab.</li>
<li><code>[R · C]</code> — Required <strong>only if you chose path 1.1C</strong> (coded REST Message + business rule). Skip it if you picked 1.1A or 1.1B.</li>
<li><code>[O]</code> — <strong>Optional</strong>. Only do it if your situation needs it.</li>
</ul>
</div>

## Background {#bg} <span class="req">[R]</span>

<p>This lab is the return path to Lab 2. In Lab 2 a Salesforce Case created an Incident and stored the Case link on the Incident in <code>u_ebond_sf_case_id</code>. This lab makes a change on the Incident flow back and update that Case. The match key is <code>Snow_Sys_Id__c</code> on the Case.</p>

<div class="note">
<span class="label">What if an Incident has no u_ebond_sf_case_id</span>
<h3 id="unlinked">What if an Incident has no <code>u_ebond_sf_case_id</code></h3>
<p><code>u_ebond_sf_case_id</code> is the link between an Incident and a Salesforce Case. It holds the Salesforce record Id (the 18-character <code>500…</code> value) of the Case that created the Incident.</p>
<ul>
<li>If the field is <strong>empty</strong>, the Incident is <strong>not linked to Salesforce</strong>. This lab's business rule and the REST call both depend on that field being set, so an empty value means <strong>nothing happens</strong>: ServiceNow will not call Salesforce, and Salesforce has no way to find the owning Case.</li>
<li>This is expected for any Incident that was created manually in ServiceNow, by email, or by another integration — those Incidents never came from a Salesforce Case, so there is no Case to update. The field is intentionally left blank for them.</li>
<li>Every path below guards on this. Unlinked Incidents are simply skipped, never written back.</li>
</ul>
<p>So the presence of <code>u_ebond_sf_case_id</code> is the definitive signal of "this Incident belongs to a Salesforce Case." If it is missing, the Incident is independent of Salesforce and will never be written back.</p>
</div>

## 1. Choose your integration path {#path} <span class="req">[R]</span>

<p>Three ways exist to make ServiceNow update Salesforce. They all need the same OAuth setup in Section 2, but they differ in how much code you write. Pick <strong>one</strong>, then follow only that subsection below (1.1A, 1.1B, or 1.1C).</p>

<div class="note">
<span class="label">Which one to pick — realistic guidance</span>

<h4>What this lab was originally for</h4>
<p>This lab is a <strong>teaching integration</strong>: one field-mapping direction (Incident → Case), one trigger (Incident created/updated), one sync rule, and a small fixed set of fields. It is deliberately simple so you can see the mechanics of an OAuth client-credentials call, a REST message, and a business-rule guard — not because a production fleet should be built this way.</p>

<h4>The best pick for maintainability, by situation</h4>
<ul>
<li><strong>Small team, no advanced developers, few fields, one direction → choose 1.1B</strong> (iPaaS). The vendor maintains the connector; a business analyst can map fields in a UI; upgrades and auth are handled for you. Best long-term maintainability with the least specialized skill. Cost is the factor to weigh.</li>
<li><strong>You have ServiceNow admins (not developers) and want the integration to live inside ServiceNow → choose 1.1A</strong> (Flow + Salesforce spoke). No custom code to review, deploy, or version; the Flow is the artifact. Great when you want the logic close to the source of the trigger and you already pay for IntegrationHub spokes.</li>
<li><strong>You need very specific, complex, or unusual behavior — custom fields per source, conditional logic, retries, transformations, multiple directions, audit hooks → choose 1.1C</strong> (coded). Code is the most flexible and the only option that fully controls bytes on the wire. It demands real developers to maintain, and it is the hardest to hand off. This is the right choice only when the other two cannot express the requirement.</li>
</ul>

<h4>Realistic best practice</h4>
<p>For a <strong>simple, one-direction, few-field</strong> integration like this lab, the maintainable production answer is usually <strong>1.1A</strong> (inside ServiceNow, no third system) or <strong>1.1B</strong> (iPaaS) — not the coded path. Choose the coded path only when business logic exceeds what a declarative tool can express, or when no extra platform/license is acceptable. In real projects a common pattern is also to run a small number of coded or spoke flows for the few high-complexity integrations and let an iPaaS handle the long tail of simple ones.</p>

<h4>What you learn by trying each other type</h4>
<ul>
<li>Try <strong>1.1C</strong> (coded) if you want to understand exactly what every option does under the hood: the OAuth token exchange, the REST/HTTP mechanics, the PATCH, and the loop guard. It is the best for debugging when a spoke or iPaaS misbehaves.</li>
<li>Try <strong>1.1A</strong> (Flow + spoke) if you want to see how the same result is achieved declaratively — and how a Flow replaces the JavaScript, making the logic visible to admins instead of locked in a script.</li>
<li>Try <strong>1.1B</strong> (iPaaS) if you want to see a third-party connector hide all the auth and REST details, and learn how field mapping moves out of code into a UI.</li>
</ul>
</div>

<details id="optA">
<summary><strong>1.1A — ServiceNow Flow Designer + Salesforce spoke</strong> (low-code, recommended)</summary>
<p>Replace the REST Message and the JavaScript business rule with a <strong>Flow</strong> built visually in Flow Designer, using IntegrationHub's official <strong>Salesforce spoke</strong> action ("Update Case").</p>
<ul>
<li>Trigger: <code>incident</code> record, async, when <code>u_ebond_sf_case_id</code> is not empty (same filter as the coded rule).</li>
<li>Action: Salesforce spoke → <strong>Update Case</strong>, then map <code>Subject</code>, <code>Description</code>, <code>Snow_Number__c</code>, and <code>Snow_Sync_Source__c</code>.</li>
<li>The loop guard is a Flow condition (skip when <code>u_sync_source = salesforce</code>) instead of the <code>if</code> in code.</li>
<li>No hand-written REST Message, no JavaScript. The credentials still come from the External Client App (Section 2).</li>
<li><strong>Then:</strong> skip Sections 3 and 4 (they are the coded path) and go to Section 5, Prove it.</li>
</ul>
</details>

<details id="optB">
<summary><strong>1.1B — Integration platform / iPaaS connector</strong> (no-code)</summary>
<p>Use a visual integration platform that ships prebuilt ServiceNow ⇄ Salesforce connectors, so no scripting or custom endpoint code is involved. Examples: Workato, Tray.io, Zapier, Automate.io, or Dell Boomi.</p>
<ul>
<li>You configure a trigger (Incident updated) and a field mapping in a UI; the platform handles auth and the call.</li>
<li>No REST Message and no business rule in ServiceNow.</li>
<li>Trade-offs: adds a third system and a license, and you still register credentials on both ends (including the External Client App in Section 2).</li>
<li><strong>Then:</strong> skip Sections 3 and 4 and go to Section 5, Prove it.</li>
</ul>
</details>

<details id="optC">
<summary><strong>1.1C — Coded REST Message + business rule</strong> (documented below)</summary>
<p>This is the fully coded path that the rest of this page (Sections 3 and 4) documents: a hand-written <strong>REST Message</strong> and an <strong>async business rule</strong> in JavaScript that PATCHes the Case. It is the most code-heavy option; use it if you want to see exactly what the Flow/spoke or iPaaS does under the hood.</p>
<ul>
<li><strong>Then:</strong> follow Sections 3 and 4, then Section 5, Prove it.</li>
</ul>
</details>

## 2. External Client App {#eca} <span class="req">[R]</span>

<p>Do this in Salesforce. Do not create a Connected App. This step is required for every path in Section 1.</p>

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

## 3. REST Message {#rest} <span class="req">[R · C]</span>

<p>Only for path <strong>1.1C</strong> (coded). If you chose 1.1A or 1.1B, skip to Section 5.</p>

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

## 4. Async business rule {#rule} <span class="req">[R · C]</span>

<p>Only for path <strong>1.1C</strong> (coded). If you chose 1.1A or 1.1B, skip to Section 5.</p>

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

## 5. Prove it {#prove} <span class="req">[R]</span>

<ul class="check">
<li>REST Message test against a known <code>Snow_Sys_Id__c</code> returns 200, not 404.</li>
<li>Edit the Incident short description by hand. Set <code>u_sync_source</code> to blank or <code>servicenow</code> first, or the rule will skip.</li>
<li>The Case subject changes. <code>Snow_Sync_Source__c</code> becomes <code>servicenow</code>.</li>
<li>No second Case was created.</li>
</ul>

## 6. Linking existing tickets (bulk) {#bulk} <span class="req">[O]</span>

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

## 7. Post-lab notes {#notes} <span class="req">[O]</span>

<details>
<summary><strong>So it runs — now what? What to keep out, and how to trust it</strong> <em>(tap to open)</em></summary>

<p>Practical notes for going beyond the lab. These apply whichever path you chose in Section 1. The recurring theme: the integration only acts on Incidents that are <em>meant</em> to be linked, and you keep that "who is eligible" decision explicit so it is easy to audit and change.</p>

<h4>Keeping certain tickets out of the integration (e.g. confidential)</h4>
<p>Say some Incidents are highly confidential or, for a business reason, will never be associated to a Case. You do not want them ebonded at all — no link written, no call to Salesforce. The clean way is to stop them <strong>before</strong> anything negotiates, not to delete a link afterward. Pick one of these depending on your path:</p>
<ul>
<li><strong>1.1C (coded):</strong> add an exclusion to the business-rule <em>filter</em> (the query on the rule), not just to the script body. For example a filter like <code>u_ebond_sf_case_id ISNOTEMPTY AND category != 'confidential'</code> — or add a first check in the script that returns early for the excluded set. Filtering at the rule level means the script never even runs for excluded rows.</li>
<li><strong>1.1A (Flow + spoke):</strong> add the same condition to the Flow's <em>trigger</em> or an entry condition, e.g. <code>category != 'confidential'</code> (and, as in the lab, <code>u_ebond_sf_case_id</code> is not empty). Excluded Incidents never start the Flow.</li>
<li><strong>1.1B (iPaaS):</strong> set an exclusion filter on the connector's trigger/recipe (e.g. "only when category is not confidential"), so the platform never fetches or forwards those records.</li>
</ul>
<p>Common exclusion keys: a <code>category</code> or <code>assignment_group</code> value, a confidentiality/security flag field, records created by a specific source, or a specific list of <code>sys_id</code>s. Whatever you use, the important thing is that <strong>the rule lives in one obvious place</strong> and is versioned — so a reviewer can see exactly which tickets are exempt and why.</p>

<h4>Auditing and safeguarding</h4>
<ul>
<li>Log every decision: record when a link is written or skipped, with the reason (e.g. "excluded: category=confidential"). A simple <code>gs.log</code> or flow log line makes incidents reviewable.</li>
<li>Never overwrite an existing <code>u_ebond_sf_case_id</code> blindly. If a ticket is already linked, decide whether a re-link is intended before writing over it.</li>
<li>Keep credentials out of repos and screenshots. The External Client App consumer secret and the ServiceNow basic-auth password never belong in code or in a committed image.</li>
<li>Test exclusions explicitly: create a confidential Incident, confirm the integration leaves it untouched (no link, no call, no log of a write).</li>
</ul>
</details>
