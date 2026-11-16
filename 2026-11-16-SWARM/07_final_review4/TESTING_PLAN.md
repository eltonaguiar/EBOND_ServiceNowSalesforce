# TESTING_PLAN — final-v6 verification and live acceptance gate

> **Current evidence boundary:** the review has run repository tests only. It has not deployed Apex, configured credentials, or executed a live ServiceNow ↔ Salesforce round trip. Live checkboxes below remain acceptance steps, not claims of completion.

## 1. Fail-closed repository gate

Run from the repository root on the review branch and again on the implementation result.

### 1.1 Python contracts and status honesty

```bash
python3 -m pytest tests -q
```

Expected on the review-only branch: **7 passed**. The implementation branch must keep all existing tests green and add behavior/regression tests; the exact total must be recorded in the PR rather than hard-coded into the documentation.

The status regression test must prove that `README.md` and `site/_layouts/default.html` contain `Live integration validation pending` until live evidence is attached. Once the live gate passes, update the test and status text in the same change; do not delete the test to remove a failure.

### 1.2 SWARM structure and evidence paths

```bash
python3 tools/swarm/swarm_librarian.py validate \
  --dir 2026-11-16-SWARM --repo-root . --strict
```

Expected final result: `validate: 0 error(s), 0 warning(s) in 2026-11-16-SWARM`.

Baseline evidence: `42b86eb` returned 0 errors and 60 warnings. A zero exit code without `--strict` is not a clean gate.

### 1.3 Shell syntax

```bash
for f in lab-scripts/*.sh lab/scripts/*.sh; do
  [ -e "$f" ] && bash -n "$f"
done
```

Expected: exit 0 and no syntax errors. Both directories are required.

### 1.4 Workflow and secret checks

```bash
actionlint
```

Expected: exit 0. If actionlint is unavailable locally, the CI equivalent must run and its run URL must be attached.

The updated CI secret scan must include `*.md`, `*.html`, `*.yml`, `*.yaml`, `*.sh`, `*.py`, `*.js`, `*.cls`, `*.trigger`, and `*.xml`, while excluding only intentional documentation fixtures. Any credential-shaped hit must be reviewed; do not solve a hit by broadening exclusions.

### 1.5 Documentation and Jekyll links

Expand `tests/test_docs_links.py` to cover every tracked Markdown file and generated Jekyll page, then run:

```bash
python3 -m pytest tests/test_docs_links.py -q
```

Expected: all relative links resolve; no empty anchor targets; the README contains `https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/`; the site links `/labs/00-instances/` through `/labs/05-troubleshooting/`; no student link requires the dated SWARM folder.

Build the same Jekyll source used by Pages:

```bash
bundle exec jekyll build --source site --destination /tmp/ebond-v6-site
```

Expected: exit 0 and `/tmp/ebond-v6-site/index.html` exists. If the repository does not include a Gemfile, the implementation task must add a reproducible `github-pages` bundle or run the equivalent `actions/jekyll-build-pages` CI build and link its result. Do not claim a local Jekyll build without installing that isolated bundle.

## 2. Salesforce mock/deployment gate

Run against a clean Developer Edition org after configuring the test Named Credential and deploying only nonproduction metadata.

```bash
sf org login web --alias ebond-lab --instance-url https://YOUR_DOMAIN.my.salesforce.com
sf project deploy start \
  --source-dir lab/salesforce/force-app \
  --target-org ebond-lab \
  --test-level RunLocalTests
sf apex run test \
  --target-org ebond-lab \
  --test-level RunLocalTests \
  --code-coverage \
  --result-format human
```

Expected: deployment succeeds, all local Apex tests pass, and org-wide/namespace coverage meets Salesforce's deployment requirement (at least 75% for Apex classes, with the trigger covered by its tests). Record the command result and org release; do not paste session IDs or consumer secrets.

Required Apex scenarios:

| ID | Scenario | Expected assertion |
|---|---|---|
| SF-01 | New user-created Case | One Queueable path; one Incident response; returned `sys_id`/number stored. |
| SF-02 | User changes `Subject`, `Description`, or `Priority` after correlation | One update call to the existing Incident, not a create. |
| SF-03 | Integration writes only `Snow_*` correlation/status fields | No second Queueable and no additional HTTP call. |
| SF-04 | Human edit immediately follows an integration write | Owned-field delta still enqueues; no persistent source flag suppresses it. |
| SF-05 | Replay the same Case ID | Same ServiceNow `sys_id`; no second Incident. |
| SF-06 | Payload contains quotes, apostrophes, backslashes, Unicode, CR/LF | Valid JSON and identical read-back text. |
| SF-07 | ServiceNow returns 400 | Per-record validation error; no blind retry; no raw response-body secret logging. |
| SF-08 | ServiceNow returns 401/403 | One documented token-refresh attempt for an expired token where applicable; authorization failures are not retried blindly. |
| SF-09 | ServiceNow returns 408/429/500/503 | Bounded transient-failure path with attempt/status recording; 429 honors `Retry-After` when present. |
| SF-10 | Batch exceeds the selected chunk size | Bounded chaining/batching, no unbounded enqueue/callout use, and one record's failure does not silently discard the rest. |
| SF-11 | Empty/missing required Case data | Fail closed before a callout; useful validation message. |
| SF-12 | Standard external-ID callback updates `Snow_*` fields | 200/201 handled correctly; no custom Apex REST endpoint is required. |

The existing tests that merely check for strings such as `enqueueJob` or `upsert row` are supporting contracts, not substitutes for these assertions.

## 3. ServiceNow instance gate

Use a nonproduction PDI and a dedicated test/integration identity. Record the PDI family and REST API version.

### 3.1 Table API CRUD

1. POST one Incident to `/api/now/table/incident`.
2. Assert **201**, a `Location` header, and nonempty `result.sys_id` and `result.number`.
3. GET by `sys_id`; assert **200** and exact field values.
4. PATCH `short_description`; assert **200** and read back the new value.
5. Query with `sysparm_fields=sys_id,number&sysparm_limit=1`; assert the returned record is the intended one, not merely an arbitrary 200 response.
6. DELETE the test Incident; assert **204**, or record the intentional ACL denial if deletion is outside the lab design.
7. Repeat with malformed JSON, bad credentials, and an underprivileged user; assert useful 400/401/403 behavior and no record creation.

Note for the Apex lookup test: Table API v2 returns 200 with an empty `result` array for a valid no-match query; v1 can return 404. Pin and test the version actually used.

### 3.2 Scripted REST/ATF

Create an ATF test using **Send REST Request – Inbound** with a dedicated basic-auth test identity and immediate response assertions. Add these cases:

| ID | Request | Expected result |
|---|---|---|
| SN-01 | Valid new source + Case ID payload | 201, Incident created, correlation and source values correct. |
| SN-02 | Exact replay of SN-01 | 200, same `sys_id`, exactly one matching Incident. |
| SN-03 | Missing/invalid Case ID or required field | 400 and no Incident. |
| SN-04 | No credentials or insufficient endpoint ACL | 401/403 as configured; no Incident. |
| SN-05 | Quotes/newlines/Unicode in mapped fields | Valid JSON and exact read-back. |
| SN-06 | Same remote ID with a different source system | No silent cross-source overwrite; explicit conflict behavior. |
| SN-07 | Unauthorized table/field access attempt | `GlideRecordSecure`/ACL enforcement is demonstrated. |

ATF calls only the current ServiceNow instance. It cannot validate the Salesforce side of the round trip; retain the external E2E steps below.

### 3.3 Async Business Rule/callback

- The rule is `When = async` and uses condition-builder `changes()` conditions for ServiceNow-owned fields.
- The script contains no `previous` reference and no `current.update()`.
- `execute()` has an explicit short timeout because response handling is required.
- Transport errors (`haveError()/getErrorMessage()`) and HTTP non-2xx results are captured.
- JSON is produced by `JSON.stringify`, not raw string interpolation.
- Results are written to the separate sync-log table without secrets or full response bodies.

## 4. Live end-to-end acceptance matrix

Run in order and attach redacted request/response metadata, record numbers, timestamps, and tester identity to `2026-11-16-SWARM/evidence/TESTING/live_results.md`.

| ID | Action | Pass condition |
|---|---|---|
| E2E-01 | Create a Salesforce Case through the Flow path | Exactly one linked Incident; Case stores `sys_id` and number. |
| E2E-02 | Update each Salesforce-owned field through the Apex path | Same Incident updates each time; no duplicate. |
| E2E-03 | Replay the same create/update request | Same Incident `sys_id`; count remains one. |
| E2E-04 | Change ServiceNow-owned state/resolution fields | Original Case receives only the designed `Snow_*` mirror updates. |
| E2E-05 | Observe E2E-02 and E2E-04 for at least two polling intervals | No repeating callout/error sequence; integration settles without a sticky flag reset. |
| E2E-06 | Immediately make another human Case edit after the callback | New edit still propagates; no `Snow_Sync_Source__c`/`u_sync_source` suppression. |
| E2E-07 | Use quotes, apostrophes, backslashes, Unicode, and multiline text | Both systems preserve valid content; no JSON parse error. |
| E2E-08 | Revoke/alter test credential | 401/403 is visible, no record is created, and no secret appears in logs. |
| E2E-09 | Simulate 400, 429, and 500 using mocks or a controlled test endpoint | 400 does not blind-retry; transient responses follow bounded policy; failure status is observable. |
| E2E-10 | Remove lab records and deactivate test flows/rules | No further callouts; test credentials can be rotated/deactivated; cleanup is recorded. |

**Live-ready exit criterion:** all core rows pass on the declared PDI family and Salesforce release. If any row is not run, the README and site must continue to say `Live integration validation pending` and name the unrun row.

## 5. Pages and cross-repository acceptance

1. Merge the reviewed implementation PR through the human gate; do not use the review PR itself as proof of deployment.
2. Confirm the `Deploy GitHub Pages` run on `main` succeeds.
3. GET `https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/` and every `/labs/<slug>/` page; require 200 and no placeholder/TODO text.
4. Verify README points to that live site and shows the current validation status.
5. In `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`, open a focused PR for `docs/cross-cutting.md` that keeps the existing EBOND subsection and changes only the beginner-path target to the stable Jekyll URL:

   `https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/labs/00-instances/`

6. Confirm the existing learning Pages workflow succeeds and the live cross-cutting page renders the lab site, repository, and stable beginner-path links. Do not create a duplicate EBOND section; the link already exists from learning commit `80ce195165728eaf39f59761a3c78a38476fe510`.

## 6. Evidence and completion rules

- Record commands, exit codes, run URLs, org/PDI releases, and redacted evidence paths in `EVIDENCE_INDEX.md`.
- Never record passwords, access tokens, consumer secrets, session cookies, full Authorization headers, or unredacted credential principals.
- Separate `PASSED (repository)`, `PASSED (mock)`, `PASSED (live)`, `NOT RUN`, and `FAILED`. A checkbox without evidence is not a pass.
- Keep the review/implementation PR open until repository gates pass. Keep the live-ready status blocked until every core live row passes or is explicitly scoped out with user approval.
