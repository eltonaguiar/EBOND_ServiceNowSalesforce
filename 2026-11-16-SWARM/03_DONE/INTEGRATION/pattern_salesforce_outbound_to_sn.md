---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [BESTPRACTICES, WORKFLOWS]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - url: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_callouts_rest_named_credentials.htm
  - verified_at: 2026-11-16T20:45:00Z
---

# Pattern B — Salesforce → ServiceNow outbound

Create/update a ServiceNow record from Salesforce using a **Flow** (with an invocable Apex callout) against ServiceNow's REST API. This gives the reverse direction of the POC.

## Prerequisites

- ServiceNow **scripted REST API** exposing custom endpoints (or use base table APIs like `/api/now/table/incident`).
- A ServiceNow **integration user / basic auth** or OAuth for the API. For a POC, an API-only user with the right `snc_platform_rest_api_access` / table permissions works.
- Salesforce **Named Credential** pointing at `https://<instance>.service-now.com` with the auth (username/password or OAuth). Named Credentials keep secrets out of code.

## Apex invocable (reference)

```apex
public with sharing class SN_IncidentCallout {
    @InvocableMethod(label='Create ServiceNow Incident' description='Create incident in ServiceNow')
    public static List<String> createIncident(List<Request> reqs) {
        List<String> out = new List<String>();
        for (Request r : reqs) {
            HttpRequest req = new HttpRequest();
            req.setEndpoint('callout:MyServiceNow/api/now/table/incident');
            req.setMethod('POST');
            req.setHeader('Content-Type','application/json');
            req.setBody(JSON.serialize(new Map<String,Object>{
                'short_description' => r.subject,
                'description' => r.body
            }));
            Http http = new Http();
            HttpResponse res = http.send(req);
            out.add(res.getBody());
        }
        return out;
    }
    public class Request {
        @InvocableVariable public String subject;
        @InvocableVariable public String body;
    }
}
```

> `callout:MyServiceNow` is the Named Credential. Always prefer it over hard-coded endpoints/credentials.

## Flow wiring

1. Create a **Record-Triggered Flow** on `Case` (after-save).
2. Add an **Action** node calling the invocable Apex.
3. Pass `Case.Subject` / `Case.Description` into the action; store the returned SN `sys_id` back on the Case (custom field `x_snc_ebond_sn_incident_id__c`).

## ServiceNow side

- Expose the endpoint used (OOTB table APIs are fine for a POC; a scripted REST API is cleaner for explicit mapping/validation).
- Grant the integration user create access to `incident`.

## Verify

- [ ] A new Salesforce Case creates an Incident in ServiceNow.
- [ ] Mapping matches `data_model_field_mapping.md`.
- [ ] Secret stays inside the Named Credential; no creds in Apex/Flow.
