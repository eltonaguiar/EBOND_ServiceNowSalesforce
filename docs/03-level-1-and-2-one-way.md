---
title: 3. Level 1–2 — One-Way Sync (Postman → Table API → Salesforce Flow)
---

# 3. Level 1–2 — One-Way Sync into ServiceNow

Levels 1 and 2 are deliberately **one-way**: data flows into ServiceNow, and ServiceNow is the **system of record** for the new Incident. No callbacks, no loops, minimal moving parts.

## Level 1 — Postman / curl → ServiceNow Table API

**Goal:** prove connectivity and Basic Auth by creating an Incident from outside ServiceNow.

### Do it

1. Note your PDI URL: `https://YOUR-PDI.service-now.com`.
2. Using **Postman**, **curl**, or the built-in **REST API Explorer** (`System Web Services → REST → REST API Explorer`), send a `POST`:

   - URL: `https://YOUR-PDI.service-now.com/api/now/table/incident`
   - Auth: **Basic Auth** — username `admin`, password (your PDI password)
   - Headers: `Content-Type: application/json`, `Accept: application/json`
   - Body:

     ```json
     {
       "short_description": "Lab Level 1 - Test from Postman",
       "description": "Incident created via the Table API. One-way integration demo.",
       "urgency": "2",
       "impact": "2",
       "category": "inquiry"
     }
     ```

   ```bash
   # curl equivalent
   curl -u "admin:<password>" \
     -H "Content-Type: application/json" \
     -X POST "https://YOUR-PDI.service-now.com/api/now/table/incident" \
     -d '{"short_description":"Lab Level 1 - Test from Postman","urgency":"2","impact":"2"}'
   ```

3. Expect a **201** response containing the new `number` (e.g. `INC0010001`) and `sys_id`.

### Verify

- In ServiceNow, open **Incident → All** (or `incident.list`) and confirm the record appears.

**Why one-way:** data moves client → ServiceNow; ServiceNow never calls back.

> **Tip:** the REST API Explorer generates the exact request and code samples for the Table API — use it instead of typing by hand.

---

## Level 2 — Salesforce Flow HTTP Callout → ServiceNow

**Goal:** a *real* Salesforce → ServiceNow one-way integration using **low-code** tools (a Record-Triggered Flow + HTTP Callout). The tricky part is wiring credentials, so it's spelled out fully.

### 2a. Set up credentials in Salesforce (the gotcha step)

Salesforce's modern pattern separates the **endpoint + auth** into two objects linked by a **Permission Set**:

1. Setup → **Named Credentials** → **External Credentials** tab → **New**:
   - Label: `ServiceNow Basic Auth`
   - Authentication Protocol: **Custom** (for Basic Auth).
   - On the new External Credential, add a **Principal** and store the ServiceNow username + password (or a pre-encoded Basic Auth token as a custom header).
2. Setup → **Named Credentials** → **Named Credentials** tab → **New**:
   - Label: `ServiceNow`
   - URL: `https://YOUR-PDI.service-now.com`
   - External Credential: `ServiceNow Basic Auth`
   - Allow callouts to the `https://YOUR-PDI.service-now.com` host.
3. Create a **Permission Set** that maps to the External Credential principal, and assign it to the user running the Flow (or the integration user). This is what actually *authorizes* the callout.

> ⚠️ If you skip the Permission Set mapping, the callout fails with an authentication error even though the credential "looks" correct.

### 2b. Create a Record-Triggered Flow

1. Setup → **Flows** → **New Flow** → **Record-Triggered Flow**.
2. Object: **Case**; Trigger: **A record is created or updated**; Entry conditions: none (or filter later).
3. Add an **Action → Create HTTP Callout**:
   - Named Credential: `ServiceNow`
   - Method: `POST`
   - Path: `/api/now/table/incident`
   - Body (map Case → Incident):

     | Case field | Incident field |
     |------------|----------------|
     | Subject | `short_description` |
     | Description | `description` |
     | Priority | `impact` / `urgency` (see mapping note) |
     | Origin | `category` |
4. Optionally capture the response and write the ServiceNow `sys_id`/`number` back to a **custom field** on the Case (e.g. `ServiceNow_SysId__c`) — this is your first correlation hook.
5. **Save and Activate** the Flow.

### Verify

- Create a Case in Salesforce → open **Incident → All** in ServiceNow → the Incident appears with mapped fields.

**Why still one-way:** Salesforce is the source; ServiceNow is the destination. The next level adds control on the receiving side; Level 4 makes it two-way.

---

## Mapping note (priority)

ServiceNow `impact`/`urgency` use a 1–3 scale by default; Salesforce `Priority` is High/Medium/Low. Decide the mapping explicitly and document it (e.g. High → impact 1/urgency 1). Inconsistent priority mapping is a classic integration bug — record yours in `08-appendix.md`'s field map.
