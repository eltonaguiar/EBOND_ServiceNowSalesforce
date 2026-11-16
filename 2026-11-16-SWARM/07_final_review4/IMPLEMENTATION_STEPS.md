# IMPLEMENTATION_STEPS — final-v6 remediation

> **For agentic workers:** execute task-by-task with the test-driven workflow. Each task is independently testable. Do not edit peer branches. Keep the nickname and live-validation-pending boundary until live evidence exists.

Header for every new/edited file follows the existing front-matter/template conventions.

## Task 1 — Public status, link, secret, and strict validation gate

The boundary regression test and README/site status changes are already in this branch. Verify and seal them.

- [ ] Step 1: confirm the status contract passes and the full suite is green
  Run: `python3 -m pytest tests -q`
  Expected: `7 passed`.

- [ ] Step 2: expand `tests/test_docs_links.py` to check every tracked Markdown file (recursively) and the site's expected Jekyll pages
  ```python
  def test_all_markdown_relative_links_resolve():
      import re
      from pathlib import Path
      broken = []
      for md in ROOT.rglob("*.md"):
          text = md.read_text(errors="ignore")
          for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
              if target.startswith(("http://", "https://", "#", "mailto:")):
                  continue
              path = (md.parent / target.split("#")[0]).resolve()
              if not path.exists():
                  broken.append(f"{md.relative_to(ROOT)} -> {target}")
      assert broken == []
  ```
  Run: `python3 -m pytest tests/test_docs_links.py -q`
  Expected before fix: fails because the dated SWARM links are intentionally excluded from the student path or because some MD references point at missing/renamed files. Resolve by editing the references, not by filtering them out.

- [ ] Step 3: make `validate.yml` run strict SWARM validation, both shell directories, actionlint, and secret scanning across all source types
  Replace the validate job run block:

  ```yaml
      - name: Validate SWARM (strict)
        run: |
          python3 tools/swarm/swarm_librarian.py validate \
            --dir 2026-11-16-SWARM --repo-root . --strict

      - name: Shell syntax (both script directories)
        run: |
          set -euo pipefail
          for f in lab-scripts/*.sh lab/scripts/*.sh; do
            [ -e "$f" ] && bash -n "$f" && echo "OK $f"
          done

      - name: Actionlint
        uses: rhysd/actionlint@v1
        with:
          args: .github/workflows

      - name: Secret scan (broad extension coverage)
        run: |
          set -euo pipefail
          HITS=$(grep -rInE \
            "(api[_-]?key|secret|password|passwd|token|BEGIN [A-Z ]*PRIVATE KEY)[=:].{8,}" \
            --include=*.md --include=*.html --include=*.yml --include=*.yaml \
            --include=*.sh --include=*.py --include=*.js --include=*.cls \
            --include=*.trigger --include=*.xml \
            --exclude-dir=.git . || true)
          HITS=$(printf '%s' "$HITS" | grep -v 'verify current' | grep -v 'Never commit' || true)
          if [ -n "$HITS" ]; then echo "$HITS"; exit 1; fi
          echo "Secret scan: clean"
  ```

- [ ] Step 4: fix all strict SWARM evidence warnings
  Run: `python3 tools/swarm/swarm_librarian.py validate --dir 2026-11-16-SWARM --repo-root . --strict`
  Expected: `0 error(s), 0 warning(s)`. Correct evidence paths to repo-relative paths or official URLs; do not weaken the validator.

## Task 2 — Canonical correlation/ownership contract

- [ ] Step 1: update `03_DONE/INTEGRATION/data_model_field_mapping.md` and site `04-ownership.md` to use `u_ebond_sf_case_id` / `Snow_Sys_Id__c` / `Snow_Number__c` and the single-owner matrix defined in `DESIGN.md §6`.

- [ ] Step 2: update `03_DONE/INTEGRATION/integration_architecture_options.md` and `pattern_integrationhub_salesforce_spoke.md` to state that IntegrationHub/Salesforce spoke require a separate subscription (PDI preview available) and are not free core prerequisites.

- [ ] Step 3: update `03_DONE/INTEGRATION/lab_levels_beginner_path.md`, `pattern_salesforce_outbound_to_sn.md`, and `pattern_sn_outbound_rest_to_salesforce.md` to use the canonical field names, an async/callout-safe Salesforce Flow path, and OAuth/client-credentials wording that matches the current org's External Client App experience (verified against the live org before merging).

## Task 3 — Salesforce trigger/Handler: create + owned-field updates

- [ ] Step 1: write the failing regression test in `CaseTriggerHandlerTest.cls`
  ```apex
  @isTest
  static void ownedFieldUpdateEnqueuesUpdate() {
      Case c = new Case(Subject = 'Original', Origin = 'Phone', Priority = 'Low');
      insert c;
      c = [SELECT Id, Subject, Description, Priority, Snow_Sys_Id__c FROM Case WHERE Id = :c.Id];
      c.Subject = 'Changed by human';
      Test.setMock(HttpCalloutMock.class, new SnowCalloutMock());
      Test.startTest();
      CaseTriggerHandler.afterChange(new List<Case>{ c }, new Map<Id, Case>{ c.Id => c });
      Test.stopTest();
      Case stored = [SELECT Snow_Sys_Id__c, Snow_Sync_Status__c FROM Case WHERE Id = :c.Id];
      System.assertNotEquals(null, stored.Snow_Sys_Id__c, 'existing correlation should be used');
      System.assertEquals('Success', stored.Snow_Sync_Status__c);
  }
  ```
  Run: `sf apex run test --test-level RunLocalTests --target-org ebond-lab --result-format human`
  Expected: fails (no `afterChange` method).

- [ ] Step 2: implement `CaseTrigger.trigger`
  ```apex
  trigger CaseTrigger on Case (after insert, after update) {
      if (Trigger.isInsert) {
          CaseTriggerHandler.afterChange(Trigger.new, null);
      } else if (Trigger.isUpdate) {
          CaseTriggerHandler.afterChange(Trigger.new, Trigger.oldMap);
      }
  }
  ```

- [ ] Step 3: implement `CaseTriggerHandler.cls`
  ```apex
  public with sharing class CaseTriggerHandler {
      public static void afterChange(List<Case> rows, Map<Id, Case> oldById) {
          List<Case> eligible = new List<Case>();
          for (Case c : rows) {
              if (String.isBlank(c.Subject)) {
                  continue;
              }
              Case old = oldById == null ? null : oldById.get(c.Id);
              if (old == null) {
                  if (String.isBlank(c.Snow_Sys_Id__c)) {
                      eligible.add(c);
                  }
                  continue;
              }
              if (c.Subject != old.Subject || c.Description != old.Description || c.Priority != old.Priority) {
                  eligible.add(c);
              }
          }
          if (!eligible.isEmpty()) {
              System.enqueueJob(new CaseEscalationQueueable(eligible));
          }
      }
  }
  ```

- [ ] Step 4: run the test suite and confirm the new test passes
  Run: `sf apex run test --test-level RunLocalTests --target-org ebond-lab --result-format human`
  Expected: create and owned-update tests pass; correlation-only update test also passes (Task 4/6).

## Task 4 — Queueable status/correlation updates and per-record error capture

- [ ] Step 1: write failing tests for correlation-only no-op and per-record failure
  ```apex
  @isTest
  static void correlationOnlyUpdateDoesNotEnqueue() {
      Case c = new Case(Subject = 'Inbound', Origin = 'Phone',
          Snow_Sys_Id__c = 'a9e30c7dc61122760116894de7bcc7bd');
      insert c;
      Test.setMock(HttpCalloutMock.class, new SnowCalloutMock());
      Test.startTest();
      CaseTriggerHandler.afterChange(
          new List<Case>{ c },
          new Map<Id, Case>{ c.Id => c });
      Test.stopTest();
      System.assertEquals(0, SnowCalloutMock.instance().callCount());
  }

  @isTest
  static void failedCaseWritesErrorStatus() {
      Case c = new Case(Subject = 'Bad', Origin = 'Phone', Priority = 'Low');
      insert c;
      Test.setMock(HttpCalloutMock.class, new SnowCalloutMock(400, '{"error":"bad request"}'));
      Test.startTest();
      System.enqueueJob(new CaseEscalationQueueable(new List<Id>{ c.Id }));
      Test.stopTest();
      Case stored = [SELECT Snow_Sync_Status__c, Snow_Sync_Error__c FROM Case WHERE Id = :c.Id];
      System.assertEquals('Error', stored.Snow_Sync_Status__c);
      System.assertNotEquals(null, stored.Snow_Sync_Error__c);
  }
  ```
  Run: `sf apex run test --test-level RunLocalTests --target-org ebond-lab --result-format human`
  Expected: fails (no `instance()`/status fields).

- [ ] Step 2: replace `CaseEscalationQueueable.cls`
  ```apex
  public class CaseEscalationQueueable implements Queueable, Database.AllowsCallouts {
      private static final Integer BATCH = 10;
      private final List<Id> caseIds;

      public CaseEscalationQueueable(List<Id> caseIds) {
          this.caseIds = caseIds == null ? new List<Id>() : caseIds;
      }

      public void execute(QueueableContext ctx) {
          Integer take = Math.min(BATCH, caseIds.size());
          List<Id> chunk = new List<Id>();
          for (Integer i = 0; i < take; i++) {
              chunk.add(caseIds[i]);
          }
          List<Case> rows = [
              SELECT Id, Subject, Description, Priority, Snow_Sys_Id__c
              FROM Case
              WHERE Id IN :chunk
          ];
          List<Case> updates = new List<Case>();
          for (Case c : rows) {
              try {
                  Map<String, Object> body = SnowIncidentService.syncCase(c);
                  updates.add(new Case(
                      Id = c.Id,
                      Snow_Sys_Id__c = (String) body.get('sys_id'),
                      Snow_Number__c = (String) body.get('number'),
                      Snow_Sync_Status__c = 'Success',
                      Snow_Sync_Error__c = null
                  ));
              } catch (SnowIncidentService.CalloutException ex) {
                  updates.add(new Case(
                      Id = c.Id,
                      Snow_Sync_Status__c = 'Error',
                      Snow_Sync_Error__c = truncate(ex.getMessage(), 4000)
                  ));
              }
          }
          if (!updates.isEmpty()) {
              update updates;
          }
          if (caseIds.size() > BATCH) {
              List<Id> rest = new List<Id>();
              for (Integer i = BATCH; i < caseIds.size(); i++) {
                  rest.add(caseIds[i]);
              }
              System.enqueueJob(new CaseEscalationQueueable(rest));
          }
      }

      public static String truncate(String value, Integer max) {
          if (value == null) return null;
          return value.length() <= max ? value : value.substring(0, max);
      }
  }
  ```

- [ ] Step 3: run all Apex tests; verify green. The update/no-op and error status tests must pass.

## Task 5 — `SnowIncidentService`: use stored correlation, JSON-safe payload, status handling

- [ ] Step 1: write tests for update-vs-create, duplicate replay, special characters, and transient retries
  Extend `SnowCalloutMock` (below) and add:
  ```apex
  @isTest
  static void syncCaseUsesStoredSysId() {
      Case c = new Case(Subject = 'Update', Origin = 'Phone',
          Snow_Sys_Id__c = 'a9e30c7dc61122760116894de7bcc7bd');
      insert c;
      Test.setMock(HttpCalloutMock.class, new SnowCalloutMock());
      Map<String, Object> body = SnowIncidentService.syncCase(c);
      System.assertEquals('a9e30c7dc61122760116894de7bcc7bd', (String) body.get('sys_id'));
      System.assertEquals('PATCH', SnowCalloutMock.instance().lastMethod());
  }
  ```

- [ ] Step 2: update `SnowIncidentService.cls`
  ```apex
  public with sharing class SnowIncidentService {
      public class CalloutException extends Exception {}
      public class ValidationException extends Exception {}

      public static Map<String, Object> syncCase(Case c) {
          if (c == null || c.Id == null) {
              throw new ValidationException('Case Id is required');
          }
          String sysId = c.Snow_Sys_Id__c;
          if (String.isBlank(sysId)) {
              Map<String, Object> found = lookupByCaseId(c.Id);
              if (found != null) {
                  sysId = (String) found.get('sys_id');
              }
          }
          if (String.isBlank(sysId)) {
              return createIncident(c);
          }
          return patchIncident(sysId, c);
      }

      public static String mapUrgency(String priority) {
          if (priority == 'High') return '1';
          if (priority == 'Medium') return '2';
          return '3';
      }

      private static Map<String, Object> lookupByCaseId(Id caseId) {
          String query = 'u_ebond_sf_case_id=' + EncodingUtil.urlEncode(String.valueOf(caseId), 'UTF-8');
          HttpResponse res = send('GET',
              '/api/now/table/incident?sysparm_query=' + query +
              '&sysparm_fields=sys_id,number&sysparm_limit=1', null);
          Map<String, Object> parsed = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
          List<Object> rows = (List<Object>) parsed.get('result');
          if (rows == null || rows.isEmpty()) {
              return null;
          }
          return (Map<String, Object>) rows[0];
      }

      private static Map<String, Object> createIncident(Case c) {
          return unwrap(send('POST', '/api/now/table/incident', payload(c)));
      }

      private static Map<String, Object> patchIncident(String sysId, Case c) {
          return unwrap(send('PATCH', '/api/now/table/incident/' + sysId, payload(c)));
      }

      private static Map<String, Object> payload(Case c) {
          return new Map<String, Object>{
              'u_ebond_sf_case_id' => c.Id,
              'short_description' => c.Subject,
              'description' => c.Description,
              'urgency' => mapUrgency(c.Priority),
              'impact' => '2'
          };
      }

      private static HttpResponse send(String method, String path, Map<String, Object> body) {
          HttpResponse res;
          for (Integer attempt = 0; attempt < 3; attempt++) {
              HttpRequest req = new HttpRequest();
              req.setEndpoint('callout:EBOND_ServiceNow' + path);
              req.setMethod(method);
              req.setHeader('Accept', 'application/json');
              req.setHeader('Content-Type', 'application/json');
              req.setTimeout(20000);
              if (body != null) {
                  req.setBody(JSON.serialize(body));
              }
              res = new Http().send(req);
              Integer code = res.getStatusCode();
              if (code == 408 || code == 429 || code == 500 || code == 503) {
                  if (attempt == 2) {
                      throw new CalloutException('ServiceNow transient failure after 3 attempts');
                  }
                  continue;
              }
              if (code < 200 || code >= 300) {
                  throw new CalloutException('ServiceNow HTTP ' + code + ' ' + errorSummary(res));
              }
              return res;
          }
          throw new CalloutException('ServiceNow transient failure after 3 attempts');
      }

      private static String errorSummary(HttpResponse res) {
          if (res == null || String.isBlank(res.getBody())) return 'no body';
          if (res.getBody().length() <= 500) return res.getBody();
          return res.getBody().substring(0, 500) + '…';
      }

      private static Map<String, Object> unwrap(HttpResponse res) {
          Map<String, Object> parsed = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
          Object result = parsed.get('result');
          return result instanceof Map<String, Object>
              ? (Map<String, Object>) result
              : parsed;
      }
  }
  ```

- [ ] Step 3: rewrite `SnowCalloutMock.cls` to be stateful and count calls
  ```apex
  @isTest
  public class SnowCalloutMock implements HttpCalloutMock {
      private Integer code;
      private String body;
      private Integer count = 0;
      private String lastMethod;
      private static SnowCalloutMock current;

      public SnowCalloutMock() {
          this(201, '{"result":{"sys_id":"a9e30c7dc61122760116894de7bcc7bd","number":"INC0010001"}}');
      }
      public SnowCalloutMock(Integer code, String body) {
          this.code = code;
          this.body = body;
          current = this;
      }
      public HttpResponse respond(HttpRequest req) {
          count++;
          lastMethod = req.getMethod();
          HttpResponse res = new HttpResponse();
          res.setHeader('Content-Type', 'application/json');
          res.setStatusCode(code);
          res.setBody(body);
          return res;
      }
      public Integer callCount() { return count; }
      public String lastMethod() { return lastMethod; }
      public static SnowCalloutMock instance() { return current; }
  }
  ```

- [ ] Step 4: run the whole Apex suite; fix any test assumptions that targeted one static mock.

## Task 6 — ServiceNow async Business Rule and sync-log

- [ ] Step 1: create `lab/servicenow/script_include_sync_log.js`
  ```javascript
  var SyncLog = Class.create();
  SyncLog.prototype = Object.extendsObject(AbstractAjaxProcessor, {
      record: function(incidentSysId, direction, success, statusCode, message) {
          var gr = new GlideRecord('u_ebond_sync_log');
          gr.initialize();
          gr.u_incident_sys_id = incidentSysId;
          gr.u_direction = direction;
          gr.u_success = success;
          gr.u_status_code = statusCode || 0;
          gr.u_message = String(message || '').substring(0, 4000);
          gr.insert();
      },
      type: 'SyncLog'
  });
  ```

- [ ] Step 2: replace `business_rule_async_sync.js`
  ```javascript
  (function executeRule(current) {
      if (!current.u_ebond_sf_case_id) {
          return;
      }
      var payload = {
          "Snow_Number__c": current.getValue('number'),
          "Snow_State__c": current.getValue('state'),
          "Snow_Resolution__c": current.getValue('close_notes') || current.getValue('work_notes') || ''
      };
      var r = new sn_ws.RESTMessageV2('EBOND Salesforce Case', 'patch_case');
      r.setStringParameterNoEscape('snow_sys_id', current.getUniqueValue());
      r.setRequestBody(JSON.stringify(payload));
      r.setHttpTimeout(15000);
      try {
          var resp = r.execute();
          var code = resp.getStatusCode();
          new SyncLog().record(current.getUniqueValue(), 'to_salesforce',
              code >= 200 && code < 300, code,
              code >= 200 && code < 300 ? '' : String(resp.getBody() || '').substring(0, 500));
      } catch (ex) {
          new SyncLog().record(current.getUniqueValue(), 'to_salesforce',
              false, 0, String(ex.message || '').substring(0, 500));
      }
  })(current);
  ```
  Set the Business Rule to: table `incident`, `When = async`, `Insert and Update` is **not** used; use **Update**, condition builder `u_ebond_sf_case_id ISNOTEMPTY`, and add `state changes` OR `close_notes changes` OR `work_notes changes` in the condition. Do not reference `previous` or call `current.update()`.

- [ ] Step 3: update `rest_message_notes.md` to only `Snow_Number__c`, `Snow_State__c`, `Snow_Resolution__c`; remove `Snow_Sync_Source__c`, `Subject`, `Description`, `u_sf_case_id`, and the custom Apex REST endpoint.

## Task 7 — Level-3 scripted REST hardening

- [ ] Step 1: replace `scripted_rest_bond_case.js`
  ```javascript
  (function process(request, response) {
      var body = request.body.data || {};
      if (!body.salesforce_id || !body.short_description) {
          response.setStatus(400);
          response.setBody({ error: 'salesforce_id and short_description are required' });
          return;
      }
      var gr = new GlideRecordSecure('incident');
      gr.addQuery('u_ebond_sf_case_id', body.salesforce_id);
      gr.setLimit(1);
      gr.query();
      var created = false;
      if (!gr.next()) {
          gr.initialize();
          gr.u_ebond_sf_case_id = body.salesforce_id;
          created = true;
      }
      gr.short_description = body.short_description;
      if (body.description) gr.description = body.description;
      if (body.urgency) gr.urgency = String(body.urgency);
      if (body.impact) gr.impact = String(body.impact);
      gr.u_ebond_sync_source = body.source_system || 'salesforce';
      var sysId = created ? gr.insert() : (gr.update(), gr.getUniqueValue());
      response.setStatus(created ? 201 : 200);
      response.setBody({ sys_id: sysId, number: gr.getValue('number'), created: created });
  })(request, response);
  ```
- [ ] Step 2: record ACL setup (resource requires authentication; write endpoint ACL is `REST_Endpoint`; use `GlideRecordSecure`). Add repeat-request test expectations in ATF.

## Task 8 — Remove the competing callback and update `lab/README.md`

- [ ] Step 1: delete `lab/salesforce/force-app/main/default/classes/SnowIncidentRest.cls` and `SnowIncidentRestTest.cls` plus their `-meta.xml`.
- [ ] Step 2: update `lab/README.md` to remove `Snow_Sync_Source__c`, `u_sync_source`, and the custom Apex endpoint, and to point to the canonical field dictionary and `DESIGN.md`.
- [ ] Step 3: run `python3 -m pytest tests -q`; adjust `test_lab_contract.py` assertions so the single standard callback is the expected behavior.

## Task 9 — End-to-end evidence and status flip

- [ ] Step 1: run the live matrices in `TESTING_PLAN.md §3` and `§4`; record redacted evidence under `2026-11-16-SWARM/evidence/TESTING/live_results.md`.
- [ ] Step 2: update `README.md` and `site/_layouts/default.html` only after the live exit criterion in `TESTING_PLAN.md §4` is fully met. Update `tests/test_docs_links.py` in the same change so the test asserts the new verified status.
- [ ] Step 3: open the focused `docs/cross-cutting.md` PR in the ServiceNow learning repo as described in `TESTING_PLAN.md §5` once the lab is merged to `main`.

## Completion protocol

- Commit per task with concise messages.
- Run strict validation and the full Python suite after every Task.
- Push only this `review/final-v6` branch and create one PR to `main`; do not merge it yourself.
- Do not create push commits containing peer, or direct `main` changes. The separate learning-repo link PR remains a separate human-gated change.
