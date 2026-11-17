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
      <li><a href="#bg">Background <span class="req">[R]</span></a>
        <ol class="toc-list">
          <li><a href="#unlinked">What if an Incident has no <code>u_ebond_sf_case_id</code></a></li>
        </ol>
      </li>
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
      <li><a href="#research">8. Integration complexity research <span class="req">[O]</span></a></li>
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

## Background <span class="req">[R]</span> {#bg}

<p>This lab is the return path to Lab 2. In Lab 2 a Salesforce Case created an Incident and stored the Case link on the Incident in <code>u_ebond_sf_case_id</code>. This lab makes a change on the Incident flow back and update that Case. The match key is <code>Snow_Sys_Id__c</code> on the Case.</p>

<details class="note" id="unlinked">
<summary><strong>What if an Incident has no <code>u_ebond_sf_case_id</code></strong> <em>(tap to open)</em></summary>
<p><code>u_ebond_sf_case_id</code> is the link between an Incident and a Salesforce Case. It holds the Salesforce record Id (the 18-character <code>500…</code> value) of the Case that created the Incident.</p>
<ul>
<li>If the field is <strong>empty</strong>, the Incident is <strong>not linked to Salesforce</strong>. This lab's business rule and the REST call both depend on that field being set, so an empty value means <strong>nothing happens</strong>: ServiceNow will not call Salesforce, and Salesforce has no way to find the owning Case.</li>
<li>This is expected for any Incident that was created manually in ServiceNow, by email, or by another integration — those Incidents never came from a Salesforce Case, so there is no Case to update. The field is intentionally left blank for them.</li>
<li>Every path below guards on this. Unlinked Incidents are simply skipped, never written back.</li>
</ul>
<p>So the presence of <code>u_ebond_sf_case_id</code> is the definitive signal of "this Incident belongs to a Salesforce Case." If it is missing, the Incident is independent of Salesforce and will never be written back.</p>
</details>

## 1. Choose your integration path <span class="req">[R]</span> {#path}

<p>Three ways exist to make ServiceNow update Salesforce. They all need the same OAuth setup in Section 2, but they differ in how much code you write. Pick <strong>one</strong>, then follow only that subsection below (1.1A, 1.1B, or 1.1C).</p>

<details class="note">
<summary><strong>Which one to pick — realistic guidance</strong> <em>(tap to open)</em></summary>

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

<h4>When code is effectively required</h4>
<p>ServiceNow flows and spokes are declarative: they are great at "one record triggers one call, with fixed field mapping." They become impractical, or effectively impossible, when the requirement is not that shape. Concrete situations that push you to 1.1C (coded):</p>
<ul>
<li><strong>Request signing / custom authentication headers.</strong> The spoke sets its own OAuth header. If the target expects a header you must <em>calculate</em> at runtime — an HMAC signature, a per-request token, a digest of the payload — the spoke cannot compute it. You need code to build that header. (e.g. calling a partner API that signs every request with <code>HMAC-SHA256</code> over the body.)</li>
<li><strong>Non-deterministic or dynamic payloads.</strong> The spoke maps a fixed set of fields. If which fields go in the request depends on the record — e.g. include <code>invoice_lines</code> only when a subtype flag is set, or build a nested array of line items from several related records — you are hand-assembling JSON the spoke cannot express. Code lets you construct exactly the document the API wants.</li>
<li><strong>Bulk / batch / scheduled sweeping.</strong> Flows run per record (or per schedule with limited looping). To link a whole table (e.g. reconcile 10,000 Incidents nightly, or backfill the link from Section 6) a scripted scheduled job or a Script Include is the normal tool. A flow "loop" over thousands of records is slow and brittle.</li>
<li><strong>Multi-call orchestration with compensation/retry.</strong> If one update must coordinate three downstream calls and roll back or retry with backoff on a partial failure, declarative error paths are too coarse. Code gives you try/catch, retries, and a transaction boundary.</li>
<li><strong>Parsing irregular inbound data.</strong> Receiving a CSV/XML/JSON with variable shape, extracting values with regex, or normalizing messy text is scripting territory. Spokes are built for well-formed structured calls, not parsing.</li>
<li><strong>Complex lookups and derived values.</strong> Deriving a value that needs several GlideRecord lookups, date math, or string transformation (e.g. "if the owner group is X and the category is Y, prefix the subject with …") gets unreadable in a flow but is a few clear lines in code.</li>
</ul>
<p>For all of these, the trigger may still be a flow/business rule — but the <em>heavy lifting</em> belongs in a Script Include or a scripted step. So "code is necessary" does not mean the whole integration is code; it usually means one hard step is code, and the rest stays declarative.</p>

<h4>What you learn by trying each other type</h4>
<ul>
<li>Try <strong>1.1C</strong> (coded) if you want to understand exactly what every option does under the hood: the OAuth token exchange, the REST/HTTP mechanics, the PATCH, and the loop guard. It is the best for debugging when a spoke or iPaaS misbehaves.</li>
<li>Try <strong>1.1A</strong> (Flow + spoke) if you want to see how the same result is achieved declaratively — and how a Flow replaces the JavaScript, making the logic visible to admins instead of locked in a script.</li>
<li>Try <strong>1.1B</strong> (iPaaS) if you want to see a third-party connector hide all the auth and REST details, and learn how field mapping moves out of code into a UI.</li>
</ul>
</details>

<details id="optA">
<summary><strong>1.1A — ServiceNow Flow Designer + Salesforce spoke</strong> (low-code, recommended)</summary>

<p><strong>System:</strong> you work <strong>inside ServiceNow</strong> (the PDI), not in Salesforce. You build a <strong>Flow</strong> there that calls Salesforce on your behalf using the External Client App credentials from Section 2.</p>

<p><strong>How to get there:</strong> in your ServiceNow instance, open the left navigation menu (the "All" menu, top-left) and choose <strong>Process Automation → Flow Designer</strong>. From the Flow Designer landing page, click <strong>New Flow</strong>. A dialog asks for a <strong>Flow name</strong> (and optionally Application/Description) — give it a name like <code>EBOND Update Case</code> and click <strong>Create</strong>. Then choose <strong>Flow for Record</strong> as the flow type.</p>

<ol>
<li><strong>Trigger.</strong> In the Flow's trigger step, set the table to <strong>Incident [incident]</strong>, the trigger to <strong>Record created or updated</strong>, and the condition (filter) to <strong><code>u_ebond_sf_case_id</code> is not empty</strong>. This means the Flow only runs for Incidents that are already linked to a Salesforce Case; unlinked ones are ignored (this is the same guard the coded rule uses).</li>
<li><strong>(Optional but recommended) Loop guard condition.</strong> Add a condition that the Flow also skips when <strong><code>u_sync_source</code> = <code>salesforce</code></strong>. Lab 2 set that value when it created the Incident from Salesforce, so this stop the Flow from "echoing" its own update back to Salesforce forever.</li>
<li><strong>Action — call Salesforce.</strong> Add an action of type <strong>Salesforce → Update Case</strong> (provided by the Salesforce spoke / IntegrationHub). In this action, choose the External Client App connection (from Section 2) as the credential.</li>
<li><strong>Map the fields.</strong> Tell the action which Incident value goes into which Case field:
<ul>
<li>Case <strong>Subject</strong> ← Incident <strong>short_description</strong></li>
<li>Case <strong>Description</strong> ← Incident <strong>description</strong></li>
<li>Case <strong>Snow_Number__c</strong> ← Incident <strong>number</strong></li>
<li>Case <strong>Snow_Sync_Source__c</strong> ← the fixed text <strong>servicenow</strong></li>
</ul>
The spoke matches the Case by <strong><code>Snow_Sys_Id__c</code> = Incident <code>u_ebond_sf_case_id</code></strong> — the reverse of the match key.</li>
<li><strong>Save, activate, and test.</strong> Save and activate the Flow, then edit an Incident's short description by hand (with <code>u_sync_source</code> blank or <code>servicenow</code>) and confirm the matching Case updates.</li>
</ol>

<p><strong>Then:</strong> you are done — skip Sections 3 and 4 (they are the coded path) and go to Section 5, Prove it.</p>
</details>

<details id="optB">
<summary><strong>1.1B — Integration platform / iPaaS connector</strong> (no-code)</summary>
<p><strong>System:</strong> this option runs on a <strong>third-party integration platform</strong> (not in ServiceNow or Salesforce). It hosts the connector that talks to both systems, so you do not build REST Messages or business rules in ServiceNow at all.</p>
<p><strong>How to get there:</strong> sign in to your chosen platform (e.g. Workato, Tray.io, Zapier, Automate.io, Dell Boomi) and create a new recipe/integration that connects your ServiceNow instance and your Salesforce org.</p>
<ul>
<li>You configure a trigger (<strong>Incident updated</strong>, filtered to where <code>u_ebond_sf_case_id</code> is not empty) and a field mapping in a UI; the platform handles auth and the call.</li>
<li>You connect the platform to both systems using their credentials — ServiceNow's <code>u_ebond_sf_case_id</code> user and the Salesforce External Client App from Section 2.</li>
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

## 2. External Client App <span class="req">[R]</span> {#eca}

<p><strong>System:</strong> this step is done <strong>in Salesforce</strong>. Do not create a Connected App. This step is required for every path in Section 1.</p>

<p><strong>How to get there:</strong> in Salesforce, click the <strong>gear icon (Setup)</strong> at the top-right, type <strong>App Manager</strong> in the Quick Find box, then open <strong>External Client App Manager</strong> and click <strong>New</strong>.</p>

<ol>
<li><strong>Distribution:</strong> choose <strong>Local</strong>. Enable <strong>OAuth</strong>.</li>
<li>For a server-to-server lab, enable <strong>Client Credentials</strong>.</li>
<li><strong>Assign an integration user</strong> — a Salesforce user who has API access and edit rights on Case. This is the identity ServiceNow will act as. Callback URL can be a placeholder for this flow.</li>
<li><strong>Policies → Permitted Users:</strong> choose <strong>Admin approved users are pre-authorized</strong>, then assign a permission set to that integration user (so they can actually use the app).</li>
<li><strong>Open Consumer Key and Secret.</strong> Those are the client id and client secret. They stay in ServiceNow's credential record (Section 3/4), not in a file.</li>
</ol>

Token URL (My Domain only):

```text
https://YOUR_DOMAIN.my.salesforce.com/services/oauth2/token
```

`login.salesforce.com` does not work for client credentials.

<ul class="check">
<li><strong>Check:</strong> you wrote down the <code>Consumer Key</code> and <code>Consumer Secret</code> (or know where they are) — you will need them in ServiceNow.</li>
<li><strong>Check:</strong> the integration user is set as an Admin-approved pre-authorized user, and that user has API access and edit rights on Case.</li>
</ul>

## 3. REST Message <span class="req">[R · C]</span> {#rest}

<p><strong>System:</strong> this step is done <strong>in ServiceNow</strong> (the PDI). Only for path <strong>1.1C</strong> (coded). If you chose 1.1A or 1.1B, skip to Section 5.</p>

<p><strong>How to get there:</strong> in your ServiceNow instance, open the left navigation menu (the "All" menu, top-left) and go to <strong>System Web Services → Outbound → REST Message</strong>, then click <strong>New</strong>.</p>

| Field | Value |
|-------|-------|
| Name | `EBOND Salesforce Case` |
| Endpoint | `https://YOUR_DOMAIN.my.salesforce.com/services/data/v68.0` |
| Authentication | OAuth 2.0, profile pointed at the token URL above |

<p>On the REST Message record, open the <strong>HTTP Methods</strong> tab and click <strong>New</strong> to create the method:</p>

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

<p><strong>Validate the method works before automating it.</strong> Use the <strong>Test</strong> button on the HTTP method with a real <code>sys_id</code> from Lab 2 (the Incident's unique ID) and a real <code>Snow_Sys_Id__c</code> Case link.</p>

<ul class="check">
<li><strong>Expect HTTP 200.</strong> If you get <strong>404</strong>, the <code>Snow_Sys_Id__c</code> value in the URL doesn't match a Case — double-check the Case link. If you get <strong>401</strong>, the OAuth profile/credential is wrong.</li>
<li><strong>Check the Case actually changed:</strong> open that Case in Salesforce and confirm its Subject/Description reflected the test values you sent.</li>
</ul>

## 4. Async business rule <span class="req">[R · C]</span> {#rule}

<p><strong>System:</strong> this step is done <strong>in ServiceNow</strong> (the PDI). Only for path <strong>1.1C</strong> (coded). If you chose 1.1A or 1.1B, skip to Section 5.</p>

<p><strong>How to get there:</strong> in your ServiceNow instance, open the left navigation menu (the "All" menu, top-left) and go to <strong>System Definition → Business Rules</strong>, then click <strong>New</strong>.</p>

<p>Configure the rule: <strong>Table:</strong> <code>incident</code>. <strong>When to run:</strong> <code>async</code>. <strong>Insert and Update</strong>. <strong>Filter (condition):</strong> <code>u_ebond_sf_case_id</code> is not empty.</p>

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

<p>The first line is the loop guard. Lab 2 set <code>u_sync_source</code> to <code>salesforce</code>, so the echo of that create does not call Salesforce again.</p>

<ul class="check">
<li><strong>Check you saved the rule in the right place:</strong> Table = <code>incident</code>, When = <code>async</code>, checked = Insert and Update, Filter set to <code>u_ebond_sf_case_id</code> is not empty.</li>
<li><strong>Validate it fires:</strong> edit a linked Incident's short description by hand (with <code>u_sync_source</code> blank or <code>servicenow</code>) and confirm the matching Case updates. If nothing happens, open <strong>System Logs → Application Logs</strong> and look for an <code>EBOND patch failed</code> entry — that tells you the rule ran but the call errored.</li>
</ul>

<div class="note">
<span class="label">Screenshot</span>
<p>Save <code>03-external-client-app.png</code>, <code>03-rest-message-200.png</code>, and <code>03-case-after-update.png</code> into <a href="https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce_RUN/blob/main/README.MD">the run repo</a>. Cover the consumer secret.</p>
</div>

## 5. Prove it <span class="req">[R]</span> {#prove}

<p>These checks apply no matter which path you chose. Do them to confirm your integration actually works end-to-end:</p>

<ul class="check">
<li><strong>Edit the Incident short description by hand.</strong> Set <code>u_sync_source</code> to blank or <code>servicenow</code> first (otherwise the loop guard skips the update), then change the short description and save.</li>
<li><strong>The matching Case updates.</strong> Open the Salesforce Case linked via <code>u_ebond_sf_case_id</code> and confirm its Subject reflects what you typed on the Incident.</li>
<li><strong><code>Snow_Sync_Source__c</code> becomes <code>servicenow</code></strong> on the Case.</li>
<li><strong>No second Case was created.</strong> This integration updates the existing Case — it must not create a duplicate.</li>
<li><strong>An unlinked Incident is left alone.</strong> Create/edit an Incident with an empty <code>u_ebond_sf_case_id</code>; the integration must ignore it (no call, no change).</li>
</ul>

<p>If you took the <strong>coded path (1.1C)</strong>, additionally confirm the REST Message test returned <strong>200</strong> (Section 3) and the business rule ran (Section 4). If you took <strong>1.1A</strong> or <strong>1.1B</strong>, verify the same end result (Case updates, no duplicate) through your Flow/spoke or iPaaS run history.</p>

## 6. Linking existing tickets (bulk) <span class="req">[O]</span> {#bulk}

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

## 7. Post-lab notes <span class="req">[O]</span> {#notes}

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

## 8. Integration complexity research <span class="req">[O]</span> {#research}

<details>
<summary><strong>Integration complexity — OOTB options, the true cost of insert/update/delete, and field authority</strong> <em>(tap to open)</em></summary>

<h4>Is there out-of-the-box functionality for this?</h4>
<p>Yes, in both platforms — but it covers the <strong>common, well-typed</strong> cases, not every combination. The key realization is that <strong>no vendor ships a "sync my tickets both ways forever" button</strong>; even prebuilt connectors are config, not zero work.</p>
<ul>
<li><strong>ServiceNow IntegrationHub + spokes</strong> are the OOTB low-code layer. The official <strong>Salesforce spoke</strong> (and similar spokes for common systems) provides actions like "Create Case", "Update Case", "Get Case", etc. This directly covers <strong>insert and update of a linked record</strong> — the two operations these labs already do. You map fields in the Flow, and the spoke handles auth and the REST call. That is the simplest supported path for "Case → Incident" and "Incident → linked Case".</li>
<li><strong>Salesforce Connect and external objects</strong> let Salesforce read/write external data (including other systems) as if it were custom objects, without copying records. Useful when you want Salesforce to <em>see</em> ServiceNow data live, but it is a read/linked view, not a general event-driven sync.</li>
<li><strong>Event-driven triggers (flows / business rules)</strong> are what make it "automatic". Both platforms support record-triggered flows with conditions — that is exactly the trigger/guard pattern you built. Deleting and complex transforms are where you leave OOTB and start writing logic.</li>
</ul>

<h4>Why Lab 2 and Lab 3 feel like "a lot of steps"</h4>
<p>You are not doing one simple call — you are wiring up <strong>four separate concerns</strong>, and the first time you configure any of them it is heavy:</p>
<ol>
<li><strong>Authentication/credentials</strong> (OAuth client credentials) — done once, reused by everything.</li>
<li><strong>The link between records</strong> (<code>u_ebond_sf_case_id</code> / <code>Snow_Sys_Id__c</code>) — the matching key that makes update possible at all.</li>
<li><strong>One operation per direction</strong> (insert in Lab 2; update-the-linked-Case in Lab 3) — the mapping and the trigger.</li>
<li><strong>Loop guard and direction control</strong> (<code>u_sync_source</code>) so you do not create an infinite write-back loop.</li>
</ol>
<p>The good news: <strong>steps 1 and 2 are done once</strong> and are reusable. Adding another operation (e.g. delete, or a second field set) is incremental — you add one more spoke action / REST method / rule, not a second full setup. The "lot of steps" is a one-time front-loaded cost, not a per-operation cost.</p>

<h4>What about update, delete, and other methods — is it that much work again?</h4>
<ul>
<li><strong>Update of an already-linked record</strong> — what Lab 3 does. It is one more method/action (PATCH) on the same credential and same link. Moderate extra work, not a redo.</li>
<li><strong>Delete</strong> — this is the genuinely awkward one. Deleting a Case in Salesforce should arguably cancel/close the Incident; deleting an Incident should arguably detach the Case. Neither platform's OOTB "create/update" spoke covers delete for you, and delete is often handled by <em>state change</em> (close/cancel) rather than a hard delete, because hard deletes complicate audit trails and the link itself. Expect this to need real design, not just a connector switch.</li>
<li><strong>Other methods</strong> (PATCH vs PUT vs DELETE vs multi-record) — each additional REST method is its own endpoint/spec, but they all reuse the same credential and the same record link. With the spoke, you get many of these actions "for free" in the action picker; with coded REST you add a method per operation.</li>
</ul>

<h4>Is there a simpler way than hand-wiring every REST method?</h4>
<ul>
<li><strong>Use the spoke and iPaaS for the standard verbs.</strong> If your integration is the usual "this record → create/update that record", a spoke (1.1A) or an iPaaS recipe (1.1B) gives you insert and update with almost no REST plumbing. This is the simpler path for the common case.</li>
<li><strong>Use a single integration tool for a direction.</strong> Don't mix a hand-built REST message for insert and a spoke for update for the same flow — pick one mechanism per integration so there is one place to look and debug.</li>
<li><strong>Push complexity into the source of the trigger, not the sink.</strong> The trigger/guard logic lives comfortably on the side where the record changes (ServiceNow for Incident changes, Salesforce for Case changes). Keep the "what happens" decision close to the change, and keep the "how to call the other side" as the thinnest possible adapter.</li>
<li><strong>Consider event/state synchronization instead of raw CRUD mirroring.</strong> Very often you don't need a literal delete; you need "when Case is closed, mark the Incident resolved". That is an update, which the existing mechanisms already handle. Prefer mapping state transitions over trying to mirror every REST verb.</li>
</ul>

<h4>Mass mapping: "any Incident of category/config_item/priority → a Case", and "any Case → an Incident"</h4>
<p>What you described — <em>if an Incident has category X, or configuration_item Y, or priority Z, create a Case; and maybe all Cases create an Incident</em> — is a <strong>routing/transformation policy</strong>, not a technical blocker. It is achievable, but it changes the design from "explicit link on create" to "rule-based generation":</p>
<ul>
<li><strong>Rule-based generation.</strong> Instead of only creating a Case when a user explicitly links, you add a trigger with conditions: e.g. Flow/business-rule on Incident where <code>category = inquiry</code> (or a config-item list, or a priority threshold) → create a Case and store the link back. This is the same spoke/REST flow you already built, just with a different (broader) filter and a <em>create</em> action.</li>
<li><strong>Watch for duplicates and loops.</strong> Rule-based generation makes the loop guard even more important — if "all Cases create an Incident" and "all Incidents of category X create a Case", you can create a feedback storm. You need explicit direction/guard fields (<code>u_sync_source</code>) and a dedup check (does a link already exist?) before creating.</li>
<li><strong>It's still "one rule per pattern".</strong> Each new pattern (one category, one priority band, one config-item) is a condition you add to the trigger, not a new integration. The heavy setup you already did is reused.</li>
</ul>

<h4>Field authority and overrides (which system wins on which field)</h4>
<p>A very real requirement: <strong>"System A is authoritative for field F, System B for field G."</strong> This is the classic <strong>bidirectional sync conflict</strong> problem, and there is no OOTB "resolve it for me" setting — you design it:</p>
<ul>
<li><strong>Declare a system of record per field.</strong> For each synchronized field, decide which side is the source of truth. The non-authoritative side must <em>not</em> push its value back, or you'll fight. Implement this as a guard: only send a field from the side that owns it.</li>
<li><strong>Use the direction/guard field to enforce it.</strong> The <code>u_sync_source</code> pattern you built is exactly the tool — it says "this record came from the other side, so don't echo it back." Extend that: when you receive an update from the authoritative side, apply it; when the local value changes, only push it if this side owns that field.</li>
<li><strong>Handle the conflict case explicitly.</strong> If two sides edit different fields, that's fine (each is authoritative for its own). If two sides edit the <em>same</em> field, you must pick a winner — last-write-wins is the default but is rarely what you want for important fields; a rule (e.g. priority always comes from ServiceNow) is cleaner.</li>
</ul>

<h4>Official vendor guidance</h4>
<p>These are the canonical references from the vendors; each is the authoritative source for the patterns named above:</p>
<ul>
<li><strong>ServiceNow — IntegrationHub overview:</strong> <a href="https://docs.servicenow.com/bundle/washingtondc-integrate-applications/page/administer/integrationhub/concept/integrationhub.html">docs.servicenow.com — IntegrationHub</a></li>
<li><strong>ServiceNow — Spokes (incl. Salesforce spoke):</strong> <a href="https://docs.servicenow.com/bundle/washingtondc-integrate-applications/page/administer/integrationhub/concept/use-a-spoke.html">docs.servicenow.com — Use a spoke</a></li>
<li><strong>ServiceNow — Table API / REST (for coded path):</strong> <a href="https://developer.servicenow.com/dev.m?/reference/api/rest/c_TableAPI.html">developer.servicenow.com — Table API</a></li>
<li><strong>Salesforce — External Client App / OAuth client credentials:</strong> <a href="https://help.salesforce.com/s/articleView?id=sf.connected_app_oauth_client_credentials.htm&type=5">help.salesforce.com — Client Credentials flow</a></li>
<li><strong>Salesforce — Connect (external objects, linked live data):</strong> <a href="https://help.salesforce.com/s/articleView?id=sf.platform_connect_about.htm&type=5">help.salesforce.com — Salesforce Connect</a></li>
<li><strong>Salesforce — REST API (for coded path):</strong> <a href="https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm">developer.salesforce.com — REST API</a></li>
</ul>
</details>
