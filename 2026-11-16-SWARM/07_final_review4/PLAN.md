# PLAN — final-v6 review and next implementation round

**Round:** 6
**Author:** isolated `review/final-v6` worktree
**Baseline:** `42b86eb`
**Approval level:** human-gated merge; this review does not merge itself.

## Problem

The repository promises a working bidirectional ServiceNow ↔ Salesforce proof of concept and a deployable reference lab. Independent review found that the runnable implementation is create-only on the Salesforce side, uses sticky source flags that suppress later human edits, builds JSON through unsafe string interpolation, provides two competing callback APIs, omits per-record failure handling, and is labeled as working without live evidence. The documentation and the Jekyll site also drift from the code.

## Goal

Deliver a progressive lab with beginner Labs 0–2, a tested/idempotent Level 3, and a structurally convergent Level 4 callback, where the repository, Apex unit tests, ServiceNow tests, and live acceptance evidence are separated and no false completion claim appears.

## Decision

Use the hybrid design in `DESIGN.md`: keep the current Jekyll `site/` model and SWARM notebook; remediate the current `lab/` implementation in place; use one canonical correlation dictionary; use the Salesforce standard external-ID PATCH as the only ServiceNow→Salesforce callback; remove the parallel custom Apex REST endpoint; rely on owned-field deltas instead of persistent loop flags; and require real Apex/ServiceNow/live tests before any live-ready claim.

## Key decisions

1. Salesforce owns Case `Subject`, `Description`, and `Priority`; ServiceNow owns state/resolution/work mirror fields.
2. Correlation: ServiceNow `u_ebond_sf_case_id` (unique) and Salesforce `Snow_Sys_Id__c` (External ID + Unique). No second custom callback or `x_snc_ebond_*` names.
3. Salesforce trigger enqueues a single Queueable for inserts and owned-field updates; correlation-only updates never enqueue.
4. ServiceNow async Business Rule uses condition-builder `changes()`, never `previous`, never `current.update()`; it builds JSON with `JSON.stringify` and writes outcomes to `u_ebond_sync_log`.
5. The callback uses the standard Salesforce external-ID endpoint. Remove `SnowIncidentRest`/`SnowIncidentRestTest` after the alternate path is no longer needed.
6. IntegrationHub and the Salesforce spoke are documented as subscription/entitlement-dependent optional paths, not free core prerequisites.
7. Live integration remains `pending` in README/site until the E2E matrix in `TESTING_PLAN.md` is executed with evidence.

## Workstreams

1. **Public status and repo contracts** — status banner, expanded link/secret/shell/strict validation.
2. **Canonical contract** — one field dictionary, ownership matrix, and endpoint contract in notebook + site.
3. **Salesforce implementation/tests** — trigger/Queueable/service/mocks and 12 behavior scenarios.
4. **ServiceNow implementation/tests** — sync log, script include, scripted REST, async rule, ATF scenarios.
5. **Live-gated E2E and evidence** — execute acceptance rows; do not claim completion until evidence exists.
6. **Cross-repository link follow-up** — stable Jekyll beginner-path link in the learning repo.

## Exit gate

- `swarm_librarian.py validate --strict` = 0 errors/0 warnings.
- Full Python contracts pass; Apex tests run on a clean Developer Edition; ATF and live E2E evidence recorded.
- No misleading live-success claims; one correlation model; one callback API; no sticky source flags.
- Human approves the review PR and the separate learning-repo link PR. The review PR alone is not deployment evidence.

See `DESIGN.md`, `IMPLEMENTATION_STEPS.md`, `FILES_TO_TOUCH.md`, `TESTING_PLAN.md`, `EVIDENCE_INDEX.md`, and `FINAL_V6_REVIEW.md`.
