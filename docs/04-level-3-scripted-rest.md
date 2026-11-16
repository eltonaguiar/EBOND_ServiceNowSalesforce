---
title: 4. Level 3 — Scripted REST API (More Control)
---

# 4. Level 3 — Scripted REST API (More Control)

The generic Table API exposes **every** field and relies on the caller to get it right. A **Scripted REST API** gives you a custom endpoint with your own validation, field mapping, defaults, and business logic — and lets you start storing the **correlation ID** that Level 4 will need.

## Why Scripted REST over the Table API

| | Table API | Scripted REST API |
|---|-----------|-------------------|
| Endpoint | `/api/now/table/incident` (fixed) | `/api/<namespace>/<api_id>/<path>` (yours) |
| Surface | Entire table + all fields | Only what you expose |
| Logic | None | Validation, transforms, defaults, multi-table |
| Security | Table ACLs only | Custom ACL + your own checks |

## Do it (ServiceNow)

1. Navigate to **System Web Services → Scripted Web Services → Scripted REST APIs** → **New**.
2. Name it (e.g. `Salesforce Case Sync`), set an **API ID** (e.g. `sf_case_sync`), set **Protection policy** appropriately.
3. In the **Resources** related list → **New**:
   - HTTP Method: `POST`
   - Relative path: `/create_incident`
   - Requires authentication: yes (Basic or OAuth depending on your level)

4. Script:

   ```javascript
   (function process(request, response) {
       var body = request.body.data;

       if (!body || !body.short_description) {
           response.setStatus(400);
           response.setBody({error: "short_description is required"});
           return;
       }

       // Loop guard: if a Case already created this Incident, update instead of duplicate
       var gr = new GlideRecord('incident');
       if (body.salesforce_id) {
           gr.addQuery('u_correlation_id', body.salesforce_id);
           gr.query();
           if (gr.next()) {
               // update existing
               gr.short_description = body.short_description;
               gr.description = body.description || gr.description;
               gr.update();
               response.setStatus(200);
               response.setBody({sys_id: gr.getUniqueValue(), number: gr.number, updated: true});
               return;
           }
       }

       gr.initialize();
       gr.short_description = body.short_description;
       gr.description = body.description || '';
       gr.urgency = body.urgency || '3';
       gr.impact = body.impact || '3';
       gr.u_correlation_id = body.salesforce_id || '';   // store SF Case Id for later two-way use
       gr.u_origin = 'salesforce';
       var sysId = gr.insert();

       response.setStatus(201);
       response.setBody({sys_id: sysId, number: gr.number});
   })(request, response);
   ```

5. Test via **REST API Explorer** or Postman against:
   `https://YOUR-PDI.service-now.com/api/<namespace>/sf_case_sync/create_incident`

## Verify

- `POST` with a valid `short_description` → 201 with `sys_id` + `number`.
- `POST` with an empty body → 400 with the error JSON.
- `POST` the same `salesforce_id` twice → 200 with `updated: true`, and **still one** Incident (idempotent upsert).

## What you just gained

- **Validation** before write.
- **Idempotent upsert** keyed on the Salesforce Id — the seed of the correlation + loop-guard pattern in Level 4.
- A **narrower, safer surface** than the raw table.

> `u_correlation_id` / `u_origin` are custom fields — create them on `incident` first (Configure → Fields, or `sys_dictionary`). Level 4 formalizes their use.
