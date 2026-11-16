---
layout: default
title: Table API
lab: 1
time: 15 min
level: One-way
order: 1
permalink: /labs/01-table-api/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#objective">Objective</a></li>
      <li><a href="#explorer">REST API Explorer</a></li>
      <li><a href="#namespace">What "now" means</a></li>
      <li><a href="#curl">Same call from a terminal</a></li>
      <li><a href="#prove">Prove it</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>You send a JSON note to ServiceNow. An Incident appears. Salesforce is not involved yet. This is the smallest proof the instance accepts outside traffic.</p>
</div>

## Objective {#objective}

HTTP 201 from `POST /api/now/table/incident`, and a new row on the Incident list. Data moves only into ServiceNow.

## REST API Explorer {#explorer}

1. In the PDI filter, open **System Web Services > REST > REST API Explorer**.
2. Namespace **now**, API Name **Table API**, API version leave default.
3. Pick **Create a record (POST)**. Table name `incident`.
4. Request body:

```json
{
  "short_description": "Lab 1 — from the explorer",
  "description": "One-way create. ServiceNow is the system of record for this Incident.",
  "urgency": "2",
  "impact": "2",
  "category": "inquiry"
}
```

5. Send. Status should be **201**. Copy `result.number` and `result.sys_id`.

<details class="glossary" id="namespace">
<summary>What the namespace "now" means — and what it is not</summary>

<div class="eli5">
<span class="label">ELI5</span>
<p>The URL has three different kinds of word in it. <code>now</code> is the mailbox ServiceNow owns. <code>table</code> is the kind of letter (create or read a record). <code>incident</code> is which drawer the letter goes in. There is no "incident" namespace. Incident is a table.</p>
</div>

<p><code>POST /api/now/table/incident</code> is read as: call a platform API (<code>now</code>), use the Table API (<code>table</code>), on the Incident table (<code>incident</code>).</p>

<h3>Namespace versus scope</h3>

<p>People mix these up because a private app gets one string that is used as both. They are not the same job.</p>

<table>
<thead><tr><th></th><th>Application scope</th><th>Namespace</th></tr></thead>
<tbody>
<tr><td>Job</td><td>Security boundary. Who may read, write, or run your tables and scripts.</td><td>Name prefix. Stops two apps from using the same technical name, and routes a URL to the right API.</td></tr>
<tr><td>Where it lives</td><td>A row in <code>sys_scope</code>. Every business rule and table points at one.</td><td>A string on the URL or on a script class, such as <code>now</code> or <code>sn_ws</code>.</td></tr>
<tr><td>Global</td><td>Global is a real scope. Apps in it skip cross-scope checks.</td><td>Global has no prefix of its own. That is why ServiceNow uses names like <code>now</code> to keep its own APIs from colliding.</td></tr>
<tr><td>Examples</td><td>Global, Human Resources: Core, a custom app record.</td><td><code>now</code>, <code>sn_sc</code>, <code>x_acme_hr</code>.</td></tr>
</tbody>
</table>

<p>When you create a scoped app, ServiceNow makes a scope name such as <code>x_company_appname</code>. That string is both the lock on the tables and the prefix on the REST URL. A free PDI cannot create a scope that starts with <code>x_snc_</code>. That prefix is ServiceNow's.</p>

<h3>There is no incident namespace</h3>

<p>Use <code>incident</code> only as the table name, after <code>/api/now/table/</code>. Other tables in the same namespace: <code>sys_user</code>, <code>change_request</code>, <code>sc_request</code>. Same mailbox, different drawer.</p>

<h3>Other namespaces you will actually see</h3>

<table>
<thead><tr><th>Namespace</th><th>Example URL</th><th>Use it when</th></tr></thead>
<tbody>
<tr><td><code>now</code></td><td><code>/api/now/table/incident</code></td><td>This lab. Plain create, read, update, delete on a table you are allowed to touch. Also Attachment API and Import Set API.</td></tr>
<tr><td><code>sn_sc</code></td><td><code>/api/sn_sc/servicecatalog/items</code></td><td>You want to order a catalog item the way the portal does, not insert an Incident row by hand.</td></tr>
<tr><td><code>sn_chg_rest</code></td><td><code>/api/sn_chg_rest/v1/change</code></td><td>Change-specific actions. Do not use it to create an Incident.</td></tr>
<tr><td>your company code, or <code>x_…</code></td><td><code>/api/&lt;code&gt;/bond/case</code></td><td>You wrote a Scripted REST API. Global scope uses the company code from the system property <code>glide.appcreator.company.code</code>. A scoped app uses its scope name. Not <code>now</code>.</td></tr>
</tbody>
</table>

<p><code>sn_ws</code> is a script namespace, not a URL. <code>sn_ws.RESTMessageV2</code> is how a business rule calls out. You will not pick it in REST API Explorer.</p>

<h3>How to see what this instance actually has</h3>

<ol>
<li>REST API Explorer. The Namespace dropdown is the list for this instance. If a name is not in that list, do not call it.</li>
<li>Official reference: <a href="https://www.servicenow.com/docs/r/api-reference/rest-apis.html">ServiceNow REST APIs</a>. Match the family your PDI is running (this lab's instance is Australia).</li>
<li>Do not copy a namespace from a blog. Store apps and scoped apps add namespaces only after they are installed. A free PDI will not have all of them.</li>
</ol>

</details>
6. Open `incident.list` and refresh. The row is there.

Headers the explorer sets for you, and that you must set yourself later: `Accept: application/json` and `Content-Type: application/json`. Missing them returns 400.

## Same call from a terminal {#curl}

<div class="warn">
<span class="label">If your prompt is PS C:\&gt;</span>
<p>You are in PowerShell. Do not paste the Linux command. <code>curl</code> there is not curl, and <code>\</code> does not continue the line. That is the error <code>Parameter name 'u' is ambiguous</code> and then <code>-H is not recognized</code>. Use the one line below. The program name is <code>curl.exe</code>.</p>
</div>

<div class="eli5">
<span class="label">ELI5</span>
<p><code>curl</code> is a small program that sends the same web request the explorer just sent, from a terminal instead of a browser. You do not need it to pass Lab 1 if the explorer already returned 201. Use it when you want to prove the call works without the explorer filling in the headers for you.</p>
</div>

`curl` is not PowerShell, and it is not Command Prompt. It is a separate program those shells can launch. Windows 10 and 11 already include it as `curl.exe`. Linux and macOS include it as `curl`.

| Where you are | What to type | Why |
|---------------|--------------|-----|
| Linux, macOS, WSL, Git Bash | `curl` | Real curl. Backslash at the end of a line continues the command. |
| Windows PowerShell | `curl.exe` | `curl` with no `.exe` is a nickname for `Invoke-WebRequest`. That is a different command. The flags below will not work on it. |
| Windows Command Prompt | `curl.exe` | No nickname problem. Quotes work differently from PowerShell. Use the Command Prompt block below, or use PowerShell. |

WSL is a Linux terminal inside Windows. If you are in a prompt that looks like `user@machine:~$`, you are in Linux or WSL. Use the Linux block. If the prompt is `PS C:\>`, you are in PowerShell. Use `curl.exe`.

Do not save the password in a file. Type it at the prompt and clear the scrollback when you are done. If you pasted a password into a chat, change it on the Developer Site before you continue.

**Windows PowerShell — paste these two lines.** Replace `YOUR_PASSWORD`. Do not put the JSON on the `curl.exe` line.

Windows PowerShell 5.1 removes the quotes inside a `-d '{...}'` body before `curl.exe` sees them. ServiceNow then says `The payload is not valid JSON`. The password was fine. The body was not. Writing the body to a file avoids that.

```powershell
Set-Content -Path "$env:TEMP\lab1.json" -Value '{"short_description":"Lab 1 - curl","urgency":"2","impact":"2"}' -Encoding ascii
curl.exe -sS -u 'admin:YOUR_PASSWORD' -H 'Accept: application/json' -H 'Content-Type: application/json' -X POST 'https://dev296154.service-now.com/api/now/table/incident' --data-binary "@$env:TEMP\lab1.json"
```

If you would rather not use curl on Windows, this is the same call with no quoting bug:

```powershell
$pair = 'admin:YOUR_PASSWORD'
$basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$body = @{ short_description = 'Lab 1 - curl'; urgency = '2'; impact = '2' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'https://dev296154.service-now.com/api/now/table/incident' -Headers @{ Authorization = "Basic $basic"; Accept = 'application/json' } -ContentType 'application/json' -Body $body
```

**Linux, macOS, WSL, or Git Bash — do not paste this into PowerShell**

```bash
curl -sS -u 'admin:YOUR_PASSWORD' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -X POST 'https://dev296154.service-now.com/api/now/table/incident' \
  -d '{"short_description":"Lab 1 — curl","urgency":"2","impact":"2"}'
```

**Windows Command Prompt** — double quotes, and the quotes inside the JSON are escaped with a backslash.

```bat
curl.exe -sS -u admin:YOUR_PASSWORD -H "Accept: application/json" -H "Content-Type: application/json" -X POST "https://dev296154.service-now.com/api/now/table/incident" -d "{\"short_description\":\"Lab 1 - curl\",\"urgency\":\"2\",\"impact\":\"2\"}"
```

### What each piece does

| Piece | Meaning |
|-------|---------|
| `curl` or `curl.exe` | The program. On PowerShell, the `.exe` is required. |
| `-sS` | `-s` hides the progress meter. `-S` still prints an error if the call fails. Together: quiet when it works, loud when it does not. |
| `-u 'admin:YOUR_PASSWORD'` | Basic authentication. The user and password from the Developer Site, separated by a colon. This is the same login the explorer used as "Send as me". |
| `-H 'Accept: application/json'` | One header. Ask for a JSON answer. See the header note above. |
| `-H 'Content-Type: application/json'` | A second header. Tell ServiceNow the body is JSON. Missing this is a 400. |
| `-X POST` | The HTTP method. POST creates. GET would only read. |
| The URL | Host plus `/api/now/table/incident`. `now` is the namespace. `incident` is the table. Use your PDI host if it is not `dev296154`. |
| `-d '{...}'` | The body. Same fields you typed in the explorer. `-d` implies POST, but `-X POST` is here so the method is obvious. |

A 201 and a new `INC` number means it worked. Then refresh `incident.list`.

The repo script `lab/scripts/curl_level1.sh` is the Linux form. It reads `SN_INSTANCE`, `SN_USER`, and `SN_PASSWORD` from the shell. It does not run unchanged in PowerShell.

<div class="note">
<span class="label">Screenshot</span>
<p>Save <code>01-explorer-201.png</code> and <code>01-incident-list.png</code> into <a href="https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce_RUN/blob/main/README.MD">the run repo</a>. Cover nothing on these two unless a password is in the frame.</p>
</div>

## Prove it {#prove}

<ul class="check">
<li>Response status 201.</li>
<li>Body contains <code>number</code> starting with <code>INC</code>.</li>
<li>The Incident list shows that number.</li>
<li>Nothing in Salesforce changed. This step is one-way on purpose.</li>
</ul>
