# TESTING_PLAN — ServiceNow ⇄ Salesforce Free Integration Lab

Verification maps to `docs/07-testing-validation.md`. Each layer has an explicit gate.

## Unit tests

- Salesforce: `IncidentSyncServiceTest` with `HttpCalloutMock`; assert field mapping + response parse. Coverage ≥75%.
- ServiceNow: ATF test with a Server Script step asserting the outbound logic ran.

## Integration tests (no code)

| # | Test | Expected |
|---|------|----------|
| 1 | Inbound Table API POST | 201 + `sys_id` + `number` |
| 2 | Inbound auth rejected (bad password) | 401 |
| 3 | Scripted REST validation (empty body) | 400 + error JSON |
| 4 | Outbound REST Message | 201/200 + Case Id |
| 5 | OAuth `Get OAuth Token` | token acquired |

## End-to-end checks

E1 SF→SN create · E2 loop guard · E3 SN→SF create · E4 update propagation · E5 idempotency · E6 manual-edit preservation · E7 negative (token invalidation). Full criteria in `docs/07` §7.4.

## Regression checks

After any change, re-run E1–E4 minimum; any refactor of outbound triggers must re-verify E2 (loop guard).

## Content/docs checks (this round's deliverable)

- `swarm_librarian.py validate` exits 0 (structure + front-matter).
- All official URLs in `evidence/CROSSCUTTING/sources.json` resolve (HTTP 200 / browser-ok).
- Pages workflow YAML parses (checked with a YAML lint; Jekyll build runs in CI on merge).
- `git grep` for secret patterns is clean.

## Manual checklist (human)

- [ ] Walk Levels 1–4 on fresh instances per `docs/05`.
- [ ] Confirm the field-ownership map matches business intent.
- [ ] Approve the TSOM cross-cutting link PR after the lab Pages site is live.
