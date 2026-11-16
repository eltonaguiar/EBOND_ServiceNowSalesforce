---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [WORKFLOWS, TESTING]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_salesforce_outbound_to_sn.md
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - verified_at: 2026-11-16T21:15:00Z
---

# Beginner path — Level 1 → 4

A progressive, lab-first route. It intentionally starts with the **simplest possible** setup (a raw HTTP POST into ServiceNow's Table API) and adds complexity one step at a time, mapping each level to the pattern docs in this folder.

> Companion to `integration_architecture_options.md`. The level framing here is pedagogical; the architecture doc is the decision reference.

## Integration types (quick map)

| Type | In this lab | Risk |
|------|-------------|------|
| One-way (uni-directional) | Level 1–3 | Low; no loops |
| Two-way (bi-directional) | Level 4 + POC | Loops / conflicts / last-writer-wins |
| Field ownership (system of record) | Level 4 | Prevent overwrites; use correlation IDs + timestamps |
| Manual edits vs integration | Level 4 | Use flags + last-modified comparison + protected fields |

## Common methods (used across levels)

- **ServiceNow Table API** (`/api/now/table/incident`) — standard CRUD, easiest to start.
- **ServiceNow Scripted REST API** — custom endpoint with your own JavaScript/validation/transforms.
- **ServiceNow Outbound REST Message + Business Rule** — ServiceNow pushes data out.
- **Salesforce Flow + HTTP Callout** — low-code no-code outbound.
- **Salesforce Apex Callouts** — code-based, more control.
- **Integration Hub Spokes** — prebuilt, often requires paid license; note for free PDI labs (see `pattern_integrationhub_salesforce_spoke.md`).

---

## Level 1 — Simplest one-way: curl / Postman → Table API

**Goal:** prove connectivity + Basic Auth; create an Incident directly in ServiceNow with no Salesforce automation.

1. Note your PDI URL: `https://YOUR-PDI.service-now.com`.
2. POST with Basic Auth (`admin` + PDI password):
   ```bash
   curl -u admin:'YOURPDIPASSWORD' \
     -H "Content-Type: application/json" -H "Accept: application/json" \
     -d '{"short_description":"Lab L1 from curl","description":"one-way demo",
           "urgency":"2","impact":"2","category":"inquiry"}' \
     https://YOUR-PDI.service-now.com/api/now/table/incident
   ```
3. Expect **201** with the new **number** and **sys_id**.
4. Verify in ServiceNow: Incident > All (record appears).
5. In REST API Explorer, use Table API → Create ` record (POST), tableName=`incident` to generate exact request + code samples.

**Why one-way:** data moves only client→ServiceNow; ServiceNow does not call back.
**Usage:** this is the entry gate for the lab; also the smoke test in the QA plan.

## Level 2 — One-way: Salesforce Flow HTTP Callout → Table API

**Goal:** real Salesforce → ServiceNow push using low-code (still one-way).

1. **Salesforce setup**
   - Create an **External Credential** (Named Credentials → External Credentials → New). Authentication protocol: **Custom** (for Basic Auth), add a principal storing the ServiceNow username/password.
   - Create a **Named Credential** pointing at `https://YOUR-PDI.service-now.com`, linked to the External Credential; grant via a Permission Set that maps to the principal.
2. **Create a Record-Triggered Flow** on Case (After Save, Create or Update):
   - Add **Action → Create HTTP Callout**, pointing at the Named Credential.
   - Method POST; path `/api/now/table/incident`.
   - Body maps Case fields → Incident fields (Subject→short_description, Description→description, …).
   - Optional: store the returned `sys_id`/number in a custom Case field for correlation.
3. Activate; create a Case; verify the Incident appears in the PDI.

**Breadcrumbs:** SF Setup → Quick Find “Named Credentials” / “Flows”; SN Incident list to verify.
**Maps to:** `pattern_salesforce_outbound_to_sn.md` (low-code variant).

## Level 3 — Scripted REST API on ServiceNow (more control)

**Goal:** replace the generic Table API with a custom endpoint that validates, maps, and seeds default values (e.g. store the Salesforce Id for later bi-directional use).

1. ServiceNow: **System Web Services > Scripted Web Services > Scripted REST APIs** → New (name, API ID).
2. Add a Resource: POST, relative path `/create_incident`:
   ```javascript
   (function process(request, response) {
     var body = request.body.data || {};
     if (!body.short_description) { response.setStatus(400); response.setBody({error:"short_description required"}); return; }
     var gr = new GlideRecord('incident');
     gr.initialize();
     gr.short_description = body.short_description;
     gr.description = body.description || '';
     gr.urgency = body.urgency || '3';
     gr.setValue('x_snc_ebond_sf_case_id', body.salesforce_id || '');  // canonical SN correlation field
     var sysId = gr.insert();
     response.setStatus(201);
     response.setBody({sys_id: sysId, number: gr.number});
   })(request, response);
   ```
3. Test via REST API Explorer / Postman against `/api/<namespace>/<api_id>/create_incident`.

**Why Scripted vs Table API:** custom validation/transforms; avoid exposing full table; multi-table operations. Still one-way inbound.
**Maps to:** the inbound side of Pattern B (SF→SN).

## Level 4 — Bi-directional concepts + field ownership + manual edits

**Goal:** understand the mechanics needed to go two-way without chaos. Full build-out is the POC walkthrough; the ownership/conflict model is in `03_DONE/BESTPRACTICES/field_ownership_and_manual_edits.md`.

- **Correlation IDs:** store the SF Case Id in the SN correlation field `x_snc_ebond_sf_case_id`, and the SN `sys_id`/number on the SF Case.
- **Loop prevention:** in Business Rules/Flows, check a flag (e.g. `u_synced_from_integration`) and compare `sys_updated_on` / `LastModifiedDate` before pushing back.
- **Outbound from ServiceNow:** an Outbound REST Message (System Web Services > Outbound > REST Message) to Salesforce's REST API, triggered by a Business Rule — only when owned fields change and the inbound flag is not set.
- **Manual edits:** integration wins on owned fields; human edits on non-owned fields are preserved until the owner updates them; log conflicts; option to require an explicit "push" action.

## Recommended ordering

1. Level 1 (connectivity + Basic Auth).
2. Level 2 (Salesforce Flow / Named Credentials) — or continue with Postman while learning credentials.
3. Level 3 (Scripted REST) to add the correlation field.
4. Level 4 + POC (bi-directional: Outbound REST Message + Business Rule).
