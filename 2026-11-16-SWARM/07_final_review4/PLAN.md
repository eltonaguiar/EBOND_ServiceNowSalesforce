# PLAN — Round 1 (v1) final plan

**Goal:** Publish an EBOND ServiceNow⇄Salesforce integration lab with a GitHub Pages site and a doc for linking it from the ServiceNow_Learning cross-cutting page.

## Scope

- Provisioning guides (SN dev instance + SF dev org).
- Integration architecture comparison + 4 patterns (A REST SN→SF, B SF→SN, C Integration Hub spoke, D Salesforce Connect).
- Field mapping (Incident ⇄ Case), OOTB workflows, step-by-step POC.
- Best practices: security, reliability/idempotency, rate limits/monitoring, source control.
- QA test plan + verification checklist.
- GitHub Pages deploy + cross-cutting link plan.

## Key decisions

1. Primary POC path = Pattern A + B (REST both directions) with correlation-key idempotency.
2. Low-code alternative = Pattern C (Integration Hub Salesforce spoke), read-only option = Pattern D.
3. Secrets never in repo; platform-native credential handling.
4. Free-tier terms flagged "verify current" where they drift.

## Deliverables map

See `FILES_TO_TOUCH.md` for every file in this round and `EVIDENCE_INDEX.md` for backing evidence.
