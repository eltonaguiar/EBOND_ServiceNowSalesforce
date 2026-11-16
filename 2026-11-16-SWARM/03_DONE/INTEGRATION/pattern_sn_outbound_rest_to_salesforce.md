---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [BESTPRACTICES]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - url: https://developer.salesforce.com/docs/atlas.en-us.240.0.api_rest.meta/api_rest/intro_what_is_rest_api.htm
  - verified_at: 2026-11-16T20:45:00Z
---

# Pattern A — ServiceNow → Salesforce outbound REST

Create/update a Salesforce record from ServiceNow using a **REST Message** against the Salesforce REST API. This is the most verbose — control path and the backbone of the POC.

## Prerequisites

- Salesforce **Connected App** with OAuth. For non-interactive, server-to-server calls use the **JWT bearer flow** (connected-app certificate) as the default. The OAuth **username-password grant** is disabled for new Connected Apps — use it only where your org still explicitly permits it.
- Salesforce **integration user** with permission to read/write target objects (e.g. `Case`).
- At least one Salesforce API version confirmed (e.g. `v58.0`+; use current).

## ServiceNow side

1. **Create a REST Message**
   - Module: *REST Messages* (`sys_rest_message`).
   - Endpoint: `https://<org>.my.salesforce.com/services/data/v<ver>/sobjects/Case`
   - Method: `POST` (or `PATCH` using `/Case/{Id}`).
2. **Add HTTP headers** — `Authorization: Bearer <token>`, `Content-Type: application/json`.
3. **Auth** — either:
   - handle the OAuth token exchange in a Script Include (build the signed JWT assertion and call `/services/oauth2/token` to mint a token; cache it and set the Bearer header), or
   - reference a **Connection & Credential alias** if you use Integration Hub style credentials.
4. **Call from a Business Rule / Flow / Script Include** with `RESTMessageV2`:

```javascript
var msg = new sn_ws.RESTMessageV2('sf_create_case', 'default');
msg.setStringParameterNoEscape('Subject', current.short_description.getDisplayValue());
msg.setStringParameterNoEscape('Description', current.description.getDisplayValue());
var resp = msg.execute();
var body = resp.getBody();      // JSON, includes Case Id
var status = resp.getStatusCode(); // 201 = created
```

> **Auth wiring:** attach the OAuth credential to the REST Message (Connection & Credential alias) **or** inject the Bearer token in code before executing: `msg.setRequestHeader('Authorization', 'Bearer ' + token);` Otherwise the request returns `401`.

5. **Store the returned Salesforce `Id`** on the ServiceNow record (e.g. a field `x_snc_ebond_sf_case_id`) so updates can route to the right Salesforce record.

## Salesforce side

- Enable the Connected App and grant the integration user access.
- Confirm the OAuth token endpoint returns a valid token; verify a manual `curl` against `sobjects/Case` before wiring ServiceNow.

## Getting the token (reference snippet)

Use the **JWT bearer flow** (current, standard for new Connected Apps):

```bash
# 1. Build a signed JWT assertion for the connected app's certificate
#    (subject = integration user's username, aud = token endpoint, exp < 5 min)
export SF_AUD=https://login.salesforce.com
export SF_SUB=yourintegrationuser@example.com
# export JWT=<jwt assertion string>          # created with your private key
# 2. Exchange the assertion for an access_token
curl -sX POST https://login.salesforce.com/services/oauth2/token \
  -d grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer \
  -d assertion="$JWT" \
  -d client_id=$SF_CLIENT_ID
```

Store the returned `access_token` in a Script Include or credential alias; refresh before it expires. The older **username-password grant** (`grant_type=password`) is **legacy** and disabled for new Connected Apps — avoid it unless your org explicitly allows it and you accept the higher risk of long-lived credentials.

## Failure handling

- Non-2xx status → log and queue a retry (see best-practices reliability doc).
- Use a correlation/idempotency key (e.g. the SN sys_id) in a custom SF field to avoid duplicate Case creation on retry.

## Verify

- [ ] A new SN Incident triggers creation of a SF Case with mapped fields.
- [ ] The Case gets the desired record type / status.
- [ ] Retry path does not create duplicates.
