---
title: 2. Out-of-Box Integration Methods
---

# 2. Out-of-Box Integration Methods

"Out-of-box" (OOB) means using each platform's **native, declarative/low-code** integration features — no custom middleware and (ideally) little or no code. You should understand the full menu before deciding what to build.

## 2.1 The decision framework

Ask three questions:

1. **Direction** — who initiates? (ServiceNow → Salesforce, or Salesforce → ServiceNow)
2. **Trigger** — event-driven (a record changes) or scheduled/batch?
3. **Latency** — real-time, near-real-time, or batch?

Then map to the matrix below.

## 2.2 ServiceNow OOB integration tools

| Tool | Direction | Type | Notes |
|------|-----------|------|-------|
| **Table API** (`/api/now/table/<table>`) | Inbound | REST | Standard CRUD on any table; the workhorse for external callers |
| **Scripted REST API** | Inbound | REST | Custom endpoints with your own request/response shape and security |
| **REST Message** | Outbound | REST | Declarative outbound call definition (endpoint, auth, method, content) |
| **SOAP Message** | Outbound | SOAP | Legacy; use REST unless the target only speaks SOAP |
| **Flow Designer + IntegrationHub spokes** | Outbound / orchestration | Low-code | Spokes wrap third-party APIs into drag-and-drop actions |
| **Service Graph Connector for Salesforce** | Outbound (CMDB-aligned) | Low-code | Syncs Salesforce org/users/objects into the CMDB via a spoke |
| **Import Sets + Transform Map** | Inbound (batch) | Batch | Staging table → field mapping → target table; coalesce prevents dupes |
| **Remote Tables** | Inbound (virtual) | Read-through | External data queried as if a native table (no local copy) |
| **Inbound Email / Inbound Action** | Inbound | Email | Create records from email (not used here) |
| **MID Server** | Both | Connectivity | For **on-prem** targets only — *not needed* for cloud-to-cloud |

> **For this lab:** the two OOB paths that matter are (a) **REST Message + Flow Designer** (ServiceNow → Salesforce) and (b) **Table API** (Salesforce → ServiceNow).

### REST Message (outbound) — what it is

A REST Message is a reusable definition of:
- **Endpoint** — e.g. `https://<MyDomain>.my.salesforce.com/services/data/v60.0/`
- **Authentication** — Basic, or OAuth 2.0 (via an OAuth Application Registry profile / credential record)
- **HTTP methods** (GET/POST/PATCH) with headers and content templates

You then invoke it from a Business Rule, a Flow, or a script via `RESTMessageV2`.

### Table API (inbound) — what it is

Every ServiceNow table is automatically exposed at:

```
https://<instance>.service-now.com/api/now/table/<table_name>
```

with standard verbs (`GET`/`POST`/`PUT`/`PATCH`/`DELETE`), `sysparm_*` query parameters, and JSON payloads. Access is governed by the **ACLs on the table** and the authenticated user's **roles** — so you control who can create Incidents by creating a dedicated integration user with only the needed roles.

## 2.3 Salesforce OOB integration tools

| Tool | Direction | Type | Notes |
|------|-----------|------|-------|
| **Named Credentials** | Outbound | Auth + endpoint | Stores endpoint + auth (OAuth/Basic) so Apex/Flow never hardcode secrets |
| **External Services** | Outbound | Low-code | Import an OpenAPI schema; generates invocable Apex for Flow |
| **Platform Events** | Outbound (pub) / Inbound (sub) | Event-driven | Decoupled, high-volume event bus |
| **Change Data Capture** | Outbound (event) | Event-driven | Emits events on record change (subset of objects) |
| **Salesforce Connect (External Objects)** | Inbound (virtual) | OData | Real-time access to external tables without copying data |
| **Outbound Message** | Outbound | SOAP (legacy) | Deprecated in favor of Platform Events / Flow |
| **Apex callout** (`HttpRequest`) | Outbound | Code | Escape hatch when no declarative option fits (covered in Level 4) |
| **Remote Site Settings** | Outbound | Allowlist | Prerequisite: the target host must be allowlisted |

> **For this lab:** the two OOB paths that matter are (a) **Named Credential + Flow/Apex callout** (Salesforce → ServiceNow) and (b) **Platform Events** as the event-driven alternative.

## 2.4 The IntegrationHub "spoke" reality check

IntegrationHub uses **spokes** — packages of prebuilt actions and connection setup for a given vendor. The **Salesforce spoke** would let you drag a "Create Case" action into a Flow without writing a REST call.

- ✅ Conceptually ideal for the ServiceNow → Salesforce direction.
- ⚠️ Spokes ship with the platform, but **which spokes are entitled** depends on your subscription. A PDI includes IntegrationHub, but the Salesforce spoke may be absent.
- **Therefore:** this lab implements the direction with a plain **REST Message + OAuth** (always available) and documents the spoke as the "if your instance has it" upgrade path.

## 2.5 Which method for which direction — summary

| Direction | OOB method (recommended) | Code required | Secret handling |
|-----------|--------------------------|---------------|-----------------|
| Salesforce → ServiceNow | **Named Credential + Flow/Apex** → Table API | Flow: none; Apex: little | Named Credential |
| ServiceNow → Salesforce | **REST Message + OAuth** invoked by Flow Designer | None (Flow) | OAuth profile + credential |
| ServiceNow → Salesforce (if entitled) | IntegrationHub Salesforce spoke | None | Connection & Credential Alias |
| Event-driven (either way) | Platform Events (SF) / Events + Scripted REST (SN) | Some | Named Credential / OAuth |

## 2.6 "Do it" — prove the OOB path before writing custom code

A quick smoke test before Level 4:

1. **Salesforce → ServiceNow (inbound):** from a terminal, `curl` the Table API with your integration user's basic auth:

   ```bash
   curl -u "itil_integration:<password>" \
     -H "Content-Type: application/json" \
     -X POST "https://devNNNNNN.service-now.com/api/now/table/incident" \
     -d '{"short_description":"OOB smoke test from curl","category":"software"}'
   ```

   Expect a JSON response containing a new `sys_id` and `number` (e.g. `INC0010001`).

2. **ServiceNow → Salesforce (outbound):** create a REST Message pointing at the Salesforce REST API's `sobjects/Case` endpoint and invoke it from a background script (Level 4 covers the full setup).

> Both smoke tests use **basic auth only for convenience** — the production-grade OAuth setup is the whole point of Levels 3-4 and the Security section.

## 2.7 When OOB is not enough

OOB covers a lot, but you reach for **custom bonding** (Level 4) when you need:
- A specific OAuth flow the declarative tool doesn't expose.
- Fine-grained control over the request/response or error handling.
- Bidirectional sync with **correlation and loop prevention** (the PoC's real substance).
