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
6. Open `incident.list` and refresh. The row is there.

Headers the explorer sets for you, and that you must set yourself later: `Accept: application/json` and `Content-Type: application/json`. Missing them returns 400.

## Same call from a terminal {#curl}

Replace the host. Use your scratch-note password. Do not save this line in the repo.

```bash
curl -sS -u 'admin:YOUR_PASSWORD' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -X POST 'https://devNNNNN.service-now.com/api/now/table/incident' \
  -d '{"short_description":"Lab 1 — curl","urgency":"2","impact":"2"}'
```

The repo script `lab/scripts/curl_level1.sh` does the same thing if `SN_INSTANCE`, `SN_USER`, and `SN_PASSWORD` are set in your shell.

## Prove it {#prove}

<ul class="check">
<li>Response status 201.</li>
<li>Body contains <code>number</code> starting with <code>INC</code>.</li>
<li>The Incident list shows that number.</li>
<li>Nothing in Salesforce changed. This step is one-way on purpose.</li>
</ul>
