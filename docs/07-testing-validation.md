---
title: 7. Testing & Validation
---

# 7. Testing & Validation

QA is part of the deliverable, not an afterthought. Every claim in this lab is verified by one of the checks below.

## 7.1 Test layers

| Layer | Salesforce | ServiceNow |
|-------|-----------|------------|
| Unit | Apex test class (`@isTest`) with mock callouts (`HttpCalloutMock`) | **ATF** (Automated Test Framework) + script assertions |
| Integration | Manual callout to the live Table API / Scripted REST | REST Message test from the UI or background script |
| End-to-end | Trigger a Case → observe Incident (and reverse) | Trigger an Incident → observe Case (and reverse) |
| Negative | Token/limit failure handling | HTTP error status handling |

## 7.2 Unit tests

### Salesforce — Apex test with mock callout

```apex
@isTest
private class IncidentSyncServiceTest {
    private class MockHttp implements HttpCalloutMock {
        public HTTPResponse respond(HTTPRequest req) {
            HTTPResponse res = new HTTPResponse();
            res.setStatusCode(201);
            res.setHeader('Content-Type', 'application/json');
            res.setBody('{"result":{"sys_id":"abc123","number":"INC0010001"}}');
            return res;
        }
    }

    @isTest
    static void createIncident_mapsFieldsAndReturnsBody() {
        Test.setMock(HttpCalloutMock.class, new MockHttp());
        Case c = new Case(Subject = 'Unit test case');
        String result = IncidentSyncService.createIncident(c);
        System.assert(result.contains('INC0010001'));
    }
}
```

**Coverage:** Salesforce requires ≥75% Apex coverage to deploy to production — write tests *with* the feature, not after.

### ServiceNow — ATF

1. **Automated Test Framework → Tests → New**.
2. Add a **Server Script** step that creates a test Incident and asserts the outbound logic ran (e.g., a log entry or a flag field set).
3. Run in a suite; ATF rolls back DB changes by default.

## 7.3 Integration tests (no code)

| # | Test | Action | Expected |
|---|------|--------|----------|
| 1 | Inbound Table API | `curl -u sf_integration:pw -X POST .../api/now/table/incident -d '{"short_description":"t1"}'` | JSON with `sys_id` + `number` |
| 2 | Inbound auth rejected | same `curl` with wrong password | 401 |
| 3 | Scripted REST validation | POST empty body to `/create_incident` | 400 with error JSON |
| 4 | Outbound REST Message | run the REST Message from its UI | Salesforce returns 201/200 + Case Id |
| 5 | OAuth token | `Get OAuth Token` on the profile | access token acquired, no error |

## 7.4 End-to-end checks

| # | Scenario | Steps | Pass criteria |
|---|----------|-------|---------------|
| E1 | SF → SN create | Create Case (Origin=Manual) | Exactly one Incident, `u_correlation_id` = Case Id |
| E2 | Loop guard | After E1, observe | No new Case created back in Salesforce |
| E3 | SN → SF create | Create Incident as a normal user | Exactly one Case, `Correlation_Id__c` = Incident sys_id |
| E4 | Update propagation | Edit Incident short description | Linked Case updates; no duplicate |
| E5 | Idempotency | Re-fire the same update twice | Still one Case, one Incident |
| E6 | Manual-edit preservation | Edit a ServiceNow-owned field (State) | Not overwritten by a later Salesforce sync |
| E7 | Negative | Invalidate the Salesforce token, edit an Incident | Error logged on ServiceNow; no crash; no partial dup |

## 7.5 Regression checks

After any change, re-run at minimum **E1–E4**. The correlation/loop guard is the highest-risk area — any refactor of the outbound triggers must re-verify E2.

## 7.6 QA gate (definition of done)

A round is "done" only when:

- [ ] All unit tests pass (Apex coverage ≥75%; ATF suite green).
- [ ] Integration tests 1–5 pass.
- [ ] End-to-end checks E1–E7 pass with evidence (screenshots/logs).
- [ ] No secrets in the repo (`git grep` for key patterns is clean).
- [ ] Results documented in `2026-11-16-SWARM/evidence/` and linked from deliverables.

## 7.7 Reporting findings

- Put redacted evidence (JSON responses, screenshots, log excerpts ≤256 KB) into `2026-11-16-SWARM/evidence/<DOMAIN>/`.
- Reference the file paths from the corresponding `03_DONE/<DOMAIN>/` deliverable front-matter.
