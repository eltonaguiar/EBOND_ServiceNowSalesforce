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

The gear icon is at the top right of Salesforce, next to the bell. Click it. A Setup Menu opens. Click **Setup**, not **Setup for current app**. That opens Setup. It is not the same screen as the Case you create later.

In Setup, open **Object Manager**. Search `case`. Open the row whose API name is **Case**, not Case Related Issue. Then **Fields & Relationships** → New.

Do not type `__c` in Field Name. Salesforce adds that suffix. `Snow_Sys_Id__c` fails because the name you typed already contains two underscores in a row. Type `Snow_Sys_Id`. The API name becomes `Snow_Sys_Id__c`.

The wizard is four steps. The checkboxes in the table are on **Step 2 of 4, Enter the details**. They are not on a later security page.

<details class="glossary">
<summary>The four steps, the defaults, and what changes if you do not take them</summary>

<p>Using the defaults is the right call for this lab, except the two Step 2 boxes on <code>Snow_Sys_Id</code> and the Step 4 layout boxes. Those are called out below. Everything else can stay as Salesforce pre-fills it.</p>

<h3>Step 1 — Choose the field type</h3>
<p>Purpose: pick how the value is stored. This lab uses <strong>Text</strong> for all three fields. A Text field stores the Case Id, the INC number, and the sync flag as characters.</p>
<p>Default: nothing is selected until you click Text. If you pick Number, Formula, or Lookup instead, the later steps change and the lab fields will not match the code. Do not.</p>

<h3>Step 2 — Enter the details</h3>
<table>
<thead><tr><th>Setting</th><th>Purpose</th><th>Default</th><th>If you change it</th></tr></thead>
<tbody>
<tr><td>Field Label</td><td>The name on the screen.</td><td>Blank.</td><td>Users see a different label. The API name does not have to match the label.</td></tr>
<tr><td>Length</td><td>How many characters the text field holds.</td><td>Often 255 if you do not type one. This lab uses 32, 40, and 20.</td><td>Too short and a Case Id or INC number will not save. Too long only wastes a little room. It does not hide the field.</td></tr>
<tr><td>Field Name</td><td>The stem of the API name. Do not type <code>__c</code>.</td><td>Copied from the label, with spaces turned into underscores.</td><td>Typing <code>Snow_Sys_Id__c</code> fails. Two underscores in a row are not allowed in the name you type.</td></tr>
<tr><td>Required</td><td>A Case cannot be saved without this value.</td><td>Unchecked. Leave it.</td><td>If you check it, you cannot create a Case until the integration has already written the value. The first save would fail. That blocks the lab.</td></tr>
<tr><td>Unique</td><td>Two Cases cannot store the same value.</td><td>Unchecked. Check it only on <code>Snow_Sys_Id</code>, case insensitive.</td><td>Without it, two Cases can point at one Incident and you will not notice. Checking it on the other two fields is harmless but not needed.</td></tr>
<tr><td>External ID</td><td>Marks the field as the id from another system, so an upsert can find the Case by that value.</td><td>Unchecked. Check it only on <code>Snow_Sys_Id</code>.</td><td>Without it, ServiceNow cannot patch the Case by sys_id in Lab 3. The field can still be displayed. It just cannot be the match key.</td></tr>
<tr><td>Auto add to custom report type</td><td>Adds the new field to custom report types that already include Case.</td><td>Checked. Leave it.</td><td>Unchecking it does not delete the field. A custom report type created earlier may not offer the column until you add it by hand. Standard reports can still use the field.</td></tr>
<tr><td>Default value</td><td>A value written when a new Case is created and nobody sets the field.</td><td>Blank. Leave it.</td><td>A default would stamp every new Case with a fake sys_id or sync flag. Leave it empty so only the integration writes those.</td></tr>
</tbody>
</table>

<h3>Step 3 — Establish field-level security</h3>
<p>Purpose: which profiles can see the field, and which can edit it. This is not the page layout. A user can have the field on the layout and still not see it if Visible is unchecked for their profile.</p>
<p>Default: Visible is checked for the profiles Salesforce pre-selects, including System Administrator. Read-only is unchecked. Use that. You are the admin creating and reading the Case. Do not build a permission set for this lab.</p>
<p>If you clear Visible for your profile, the field is still stored. You will not see it on the layout, and a report will hide the column for you. The API, running as a user who is allowed to see it, can still read it. This lab does not need that split.</p>

<h3>Step 4 — Add to page layouts</h3>
<p>Purpose: which Case screens show the field. The field already exists before you reach this step.</p>
<p>Default: the boxes may all be checked. Leave them checked. If you uncheck one, that screen does not show the field. Close Case Layout is only the close screen. Case Layout is the page you open for a new or open Case.</p>
<p>An unchecked box does not remove the field from the database, the API, Flow, Apex, or a report that includes the field. If you only check Close Case Layout, the UI shows the value when you close a Case, not when you open one. QA then means a report with that column, an API read, or adding the field to Case Layout.</p>

</details>

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

Setup → Quick Find `named credentials`. Open **Named Credentials** under Security. An empty list, "You don't have any named credentials," is expected. Click **New** at the right. The page has three tabs: Named Credentials, External Credentials, and External Auth Identity Providers. Start on External Credentials if you are creating the login first, then come back to Named Credentials → New.

1. Open the **External Credentials** tab. Click **New**. Label is the display name. Type `EBOND ServiceNow`. A space is fine there. Name is the API name. Change it to `EBOND_ServiceNow`. No spaces. Salesforce may copy the label, space included, into Name. If you save that, you get a red unexpected-error banner, not a clear "no spaces" message. Fix Name, then Save.
2. Authentication Protocol: pick **Basic Authentication**. Not Custom. The list also has AWS Signature Version 4, JWT, No Authentication, and OAuth 2.0. Those are for other kinds of login. This lab sends the PDI username and password, which is Basic Authentication. Custom means you build the header yourself. Do not start there.
3. Save. The Principals list appears only after the save. A principal is the login this credential will use. It is not a user you create. Click **New** on Principals. The form is three boxes, not a username form yet.
   - Parameter Name: `PDI_admin`. No space. A space here can fail the same way Name did.
   - Sequence Number: `1`. This is the first and only principal. Salesforce uses the number to decide order if you add more later.
   - Identity Type: **Named Principal**. That means one shared PDI login for every Salesforce user who is allowed to use this credential. **Per User Principal** means each Salesforce user types their own ServiceNow password. Do not pick that for this lab.
   After you pick Named Principal, Username and Password appear on this same form. They are not a second screen. Username is the PDI user, `admin`. Password is the PDI password. Save. Do not put the password in a screenshot.
4. The principal page has no Manage Assignments button. That button is on a permission set. Setup → **Users** → **Permission Sets**, or Quick Find `permission sets`. Click **New**. Label `EBOND ServiceNow`. API name `EBOND_ServiceNow`. License: leave it at **--None--**. Do not pick a permission set license. That dropdown is for paid features such as Sales Cloud. This set only grants the principal. A license here would block the assignment unless your user already has that license. Save. <div class="eli5">
<span class="label">ELI5</span>
<p>A principal is the ServiceNow login stored on the credential. A permission set is a badge you pin on a Salesforce user. The badge is what allows that user to use the stored login. Without the badge, the login exists and the user still cannot use it. You use a permission set when a profile does not already grant the thing, and you do not want to edit the profile. System Administrator does not already grant this principal.</p>
</div>

Open the permission set. In the settings list, click **External Credential Principal Access**. Click **Edit**. The principal starts on the left, under Available. Select `EBONDServiceNow - PDI_admin` and click the Add arrow so it moves to Enabled on the right. Click **Save**. A checkmark is not how this screen works. The arrow is. Then, still on the permission set, click **Manage Assignments**. The list is empty until you click **Add Assignment**. Check your user. The profile is System Administrator. Click Next, then Assign. One assignment is enough. Expires On can stay blank. To see which user you are, click the round picture at the top right, click your name, then **User Detail**. That is the user the permission set must list. Being System Administrator does not skip this step. Without it, the call fails even though the credential exists. Salesforce will not say the password was wrong. It will say you are not allowed to use the principal.
5. The Related Named Credentials list is empty until you do this step. Back on the **Named Credentials** tab → **New**.
   - Label can be `EBOND ServiceNow` or `EBOND_ServiceNow`.
   - Name must be `EBOND_ServiceNow`, with the underscore. The callout uses this box, not the Label. If the box shows `EBONDServiceNow`, type the underscore in before Save.
   - URL is your own ServiceNow dev instance, not this lab's. This run used `https://dev296154.service-now.com`. A trailing slash is fine. No path after the host.
   - Enabled for Callouts: on.
   - External Credential: `EBOND ServiceNow`.
   - Client Certificate: leave blank.
   - Generate Authorization Header: checked.
   - Allow Formulas in HTTP Header and HTTP Body: leave unchecked.
   - Outbound Network Connection: leave `--None--`.
   - Allowed Namespaces for Callouts: leave empty. `namespaceA, namespaceB` is placeholder text, not a value to type.
   Save.
6. You do not also need a Remote Site Setting for that host.

## Pick one path {#pick}

Do not do both. Two paths would both create an Incident for the same Case.

| Path | Do this if | Skip |
|------|------------|------|
| Flow | You do not want to install code. Click-only. | The Apex section. |
| Apex | You want the repo code, or the Flow HTTP action is missing. | The Flow section. |

The Named Credential above is required for either path. After you finish one path, create a new Case and check ServiceNow. That is the proof. The other path is optional reading, not a second setup.

| | Flow | Apex |
|--|------|------|
| Who can change it later | An admin who can open Flow. No deploy. | Someone who can edit and deploy Apex. |
| What you see | The field mapping is on the screen. | The mapping is in a class. You read code to see it. |
| Risk | Easy to put the call on the wrong path. The save then fails with uncommitted work. | Easy to forget the test, or to deploy to the wrong org. |
| Bulk | Fine for one Case at a time. Awkward if 200 Cases save at once. | The repo code batches the calls. That is why it exists. |
| If the HTTP action is missing | You cannot finish this path. | You still can. |
| This lab | Pick this if you want the click path. | Pick this if you want the same result with code you can rerun. |

## Flow path (no Apex) {#flow}

Use this only if you picked Flow above.

1. Setup → Quick Find `flows`. Open **Flows** under Process Automation. Click **New Flow** at the top right. Do not click Flow Trigger Explorer, and do not open an existing row such as Add Case Comment. Choose **Record-Triggered Flow**. Object **Case**. Trigger **A record is created**. Optimize for **Actions and Related Records**.
2. In Configure Start, under Optimize Flow, pick **Actions and Related Records**. Salesforce then asks if this flow calls an external system. Turn **Add Asynchronous Path** on. That adds a second branch, **Run Asynchronously**. Leave the **Run Immediately** branch empty. The call must not go there. That branch still has an unsaved Case, and the call fails.
3. On the **Run Asynchronously** branch, click the plus. Choose **Action**. At the bottom of Search Actions, click **Create HTTP Callout**. It is not one of the rows in the category list.

   First screen, New HTTP Callout:
   - Name: `EBONDCreateIncident`. No underscore and no space. This is not the Named Credential name.
   - Description: leave blank.
   - Named Credential: `EBOND_ServiceNow`.
   - Click Next.

   Second screen, Configure Invocable Action:
   - Label: `Create Incident`.
   - Method: `POST`.
   - Description: leave blank.
   - URL Path: `/api/now/table/incident`. The host is already filled from the Named Credential. Do not type the host again.
   - Set Query Parameter Keys: do not click Add Key.
   - Click Next.

   ![Filled method and path]({{ '/assets/img/02-http-callout-path-filled.png' | relative_url }})

   Third screen, Sample JSON Request. These are sample values so Salesforce learns the field names. They are not the live Case. Do these clicks in order. Review does not advance the page. Next is a separate button at the bottom right, and it does not count until Review has succeeded.

   1. Leave Description blank.
   2. Paste the JSON into Sample JSON Request.
   3. Click **Review**. The text may be red before this. That is normal.
   4. Wait until Data Structure on the right lists the six fields, each as String. If it still says No sample JSON, Review did not run. Do not change the String dropdowns.
   5. Click **Next** at the bottom right. Review does not move you forward.

   Fourth screen, Select Sample Response Method. Pick **Use Example Response**. Do not pick Connect for Schema. That one calls ServiceNow now and creates a real Incident from the sample. Click **Next**.

   Fifth screen, Sample JSON Response. This is not the same JSON as the request. The request told Salesforce what it will send. This screen tells Salesforce what ServiceNow sends back. If you paste the request here, the Flow cannot read `sys_id` or `number` from the reply. Leave Description blank. Paste the response block below into Sample JSON Response. Click **Review**. Wait until Data Structure shows `result` as an object, and `sys_id` and `number` as String. Leave `number` as String. `INC0010002` is text, not an integer. Then click **Save**. This screen ends with Save, not Next.

   ```json
   {
     "result": {
       "sys_id": "5dba2bdac3e8df54310abf0d050131a5",
       "number": "INC0010002"
     }
   }
   ```

   ![Sample JSON Request screen]({{ '/assets/img/02-http-callout-json.png' | relative_url }})

   ```json
   {
     "short_description": "Lab 2 from Flow",
     "description": "Created from a Salesforce Case",
     "urgency": "2",
     "impact": "2",
     "u_ebond_sf_case_id": "500000000000000AAA",
     "u_sync_source": "salesforce"
   }
   ```
4. The canvas now shows the action on **Run Asynchronously**. The banner says the external service was created. The Label box is red because it is empty. Fill it before anything else.
   - Label: `Create Incident`.
   - API Name: click the box. If it stays empty, type `Create_Incident`. No spaces. This is the Flow element name, not `EBONDCreateIncident`.
   - Description: leave blank.
   - Set Request Body is the JSON Salesforce will send to ServiceNow when a Case is created. It is one key, `body`, not six boxes. Click the Value box. The menu opens. Click **+ New Resource** at the top. Do not pick `$Flow`, `$User`, or another global variable. Those are not the request.

   <div class="eli5">
   <span class="label">ELI5</span>
   <p>A resource is a named value the Flow can hold. New Resource makes a box shaped like the sample request. You fill that box from the Case, then hand the whole box to ServiceNow as the request body. The sample JSON only taught Salesforce the shape. The live request should look like that shape, with this Case's values:</p>
   </div>

   ```json
   {
     "short_description": "the Case Subject",
     "description": "the Case Description",
     "urgency": "2",
     "impact": "2",
     "u_ebond_sf_case_id": "the Case Id",
     "u_sync_source": "salesforce"
   }
   ```

   On New Resource, API Name `IncidentBody`. Leave Description blank. Data Type stays Apex-Defined. Apex Class stays the generated body class. Leave Allow multiple values unchecked. Leave both Availability boxes unchecked. This dialog does not contain the six fields. Click **Done**. The Value box should then show `IncidentBody`. The six fields are set in the next step, on an Assignment before this action.
   - Leave **Manually assign variables** unchecked. That checkbox is not the request assignment. It only lets you store the reply yourself. The automatic outputs, 2XX, Default Exception, and Response Code, are enough. Checking it does not fill `short_description` or the other request fields.
   - Under Show advanced options, leave Transaction Control on **Let the flow decide**. Do not pick Always continue in current transaction. That can fail the call.
5. Assignment is not inside the action panel. Close that panel. On the canvas, click the **+** between **Run Asynchronously** and **Create Incident**, then choose **Assignment**. That plus is the one directly above the Create Incident box.

   <div class="eli5">
   <span class="label">ELI5</span>
   <p><code>IncidentBody</code> is an empty envelope shaped like the request ServiceNow expects. It is not a Case, and it is not an Incident yet. This Assignment copies values from the Salesforce Case that just triggered the Flow into that envelope. Subject becomes <code>short_description</code>. Description becomes <code>description</code>. The Case Id becomes <code>u_ebond_sf_case_id</code>. <code>urgency</code>, <code>impact</code>, and <code>u_sync_source</code> are fixed text. The next element sends the filled envelope to ServiceNow, which creates the Incident.</p>
   </div>

   On the Assignment panel:
   - Label: `Set Incident Body`. The red box is only because this is empty.
   - API Name: `Set_Incident_Body` if it does not fill itself.
   - Description: leave blank.
   - Set Variable Values. Operator stays **Equals**. Click **Add Assignment** for each row.

   | Variable | Value |
   |----------|--------|
   | `{!IncidentBody.short_description}` | `{!$Record.Subject}` |
   | `{!IncidentBody.description}` | `{!$Record.Description}` |
   | `{!IncidentBody.urgency}` | `2` |
   | `{!IncidentBody.impact}` | `2` |
   | `{!IncidentBody.u_ebond_sf_case_id}` | `{!$Record.Id}` |
   | `{!IncidentBody.u_sync_source}` | `salesforce` |

    In the Variable box, search `IncidentBody`. Do not select the whole resource. Click the arrow beside it and pick one field for that row. Selecting the whole `IncidentBody` replaces the box instead of filling a field.    Search `$Record` in the Value box for Subject, Description, and Id. Type `2` and `salesforce` as text. Click Done. Then click **Save** on the flow. Flow Label `EBOND Create Incident`. Flow API Name `EBOND_Create_Incident`. Description blank. Do not click **Activate** yet. The saved flow stays **Inactive**.

    ![The plus above Create Incident]({{ '/assets/img/02-assignment-plus-circled.png' | relative_url }})
 5. Close the Create Incident panel with X. Do not change that panel. Body is already `IncidentBody`. Leave **Manually assign variables** unchecked.
 6. Click the **+** under **Create Incident**, above the pink end. Add **Update Records**.
    - Label: `Save Incident Ids`. API Name: `Save_Incident_Ids`. Description blank.
    - How to Find Records: **Use the Case record that triggered the flow**.
    - Set Field Values. Do not select the whole `2XX` or the whole `result`. Open **Create Incident**, then `2XX`, then `result`, and pick one field.

    <div class="eli5">
    <span class="label">ELI5</span>
    <p><code>2XX</code> is not a ServiceNow field. It is Salesforce's name for the success reply. ServiceNow answers the call with a status number. <code>200</code> through <code>299</code> means it worked. A new Incident usually comes back as <code>201</code>. Salesforce drops every success answer into one box named <code>2XX</code>. The Incident id and number are inside that box, under <code>result</code>. A <code>400</code> or <code>500</code> does not go there. Those land in <strong>Default Exception</strong>. <strong>Response Code</strong> is the raw number, such as <code>201</code>. Open <code>2XX</code>, open <code>result</code>, and pick <code>sys_id</code> or <code>number</code>. Do not pick the whole box.</p>
    </div>

    | Field | Value |
    |-------|--------|
    | ServiceNow Sys Id | `{!Create_Incident.2XX.result.sys_id}` |
    | ServiceNow Number | `{!Create_Incident.2XX.result.number}` |
    | Sync Source | `salesforce` |

    Click **Done**. Click **Save**. Do not click **Activate** yet.
 7. Activate. In Salesforce, open the app launcher (the nine dots at the left), search `cases`, and open **Cases** under Items. Click New. Subject is required. Do not create an Incident yourself. The new Case lands in Recently Viewed. If you do not see it, click the down arrow next to the list name and pick **All Cases** or **All Open Cases**.

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
