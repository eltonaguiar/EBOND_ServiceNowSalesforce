# 00_CHARTER — Swarm 2026-11-16 (ServiceNow ⇄ Salesforce free-integration lab)

**Status:** active — Phase 1 complete (draft lab + scaffold); peer review begins next round.
**Target repo:** `eltonaguiar/EBOND_ServiceNowSalesforce`
**Pages site:** https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/ (deploys on merge to `main`)
**Framework:** `eltonaguiar/AGENT_FOLDERFRAMEWORK` — Swarm / Isolated-Worktree protocol.

## 1. Scope

Build a hands-on lab that:
1. Provisions a **free ServiceNow PDI** and a **free Salesforce Developer org**.
2. Bonds them into a **proof-of-concept integration** (canonical scenario: Case ⇄ Incident bidirectional sync).
3. Documents **out-of-box** methods (REST Message, Table API, Flow Designer/IntegrationHub, Named Credentials, External Services, Platform Events) *and* **custom** methods (REST + OAuth 2.0 callouts).
4. Enforces **best practices** (no hardcoded secrets, least privilege, rate limits, loop-safe idempotency).
5. Publishes the lab as a **GitHub Pages** site and links it from the existing TSOM cross-cutting page.

## 2. Success criteria (verifiable, evidence-linked)

| # | Criterion | How verified |
|---|-----------|--------------|
| S1 | Lab covers all seven sections with accurate, current facts | Read `docs/00`–`07`; official URLs resolve (HTTP 200) |
| S2 | Both free-instance provisioning paths are documented | `docs/01-free-instances.md` |
| S3 | Both OOB and custom integration methods are covered | `docs/02` + `docs/03` |
| S4 | Loop-safe bidirectional pattern (correlation + origin check) is specified | `docs/03-custom-bonding.md` §3.5 |
| S5 | Security section includes secrets/OAuth/least-privilege/rate-limit guidance | `docs/04` |
| S6 | An executable PoC playbook + test plan exist | `docs/05` + `docs/06` |
| S7 | GitHub Pages workflow is syntactically valid and deploys on merge | `.github/workflows/pages.yml` |
| S8 | README links the live Pages site | root `README.MD` |
| S9 | SWARM folder validates clean (structure + front-matter) | `swarm_librarian.py validate` |
| S10 | A plan exists to link this lab from the TSOM cross-cutting page | `03_DONE/DOCS_SITE/v1_tsom_crosscutting_link_plan.md` |

## 3. Non-goals (out of scope)

- No production deployment; developer instances only.
- No paid IntegrationHub Enterprise subscription — spokes documented as an *option*, not a requirement.
- No third-party middleware / iPaaS (MuleSoft, Boomi, Workato).
- No real customer data.
- No force-push or history rewrite; changes land via PR on a feature branch.

## 4. Known URLs / key files

URLs:
- Pages site: https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
- ServiceNow PDI signup: https://developer.servicenow.com
- Salesforce dev signup: https://developer.salesforce.com/signup
- TSOM cross-cutting page (link target): https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/

Key files (repo-relative):
- `README.MD`, `index.md`, `_config.yml`
- `docs/00-overview.md` … `docs/07-appendix.md`
- `.github/workflows/pages.yml`
- `2026-11-16-SWARM/` (this folder)

## 5. Agent roster

| Agent | Worktree / branch | Role | Domain | Status |
|-------|-------------------|------|--------|--------|
| kilo | `v1-bond-lab` | Scout (round 1, all domains) | INSTANCE_SETUP, OOB_INTEGRATION, CUSTOM_INTEGRATION, SECURITY, DOCS_SITE | ✅ phase 1 |
| TBD | `v2…` (future) | Reviewer | — | ☐ |
| TBD | `v3…` (future) | Reviewer / synthesizer | — | ☐ |
| TBD | `final…` (future) | Synthesizer | final_review3/4 | ☐ |

## 6. Pre-final-review checklist (tick before writing `04_final_review/`)

- [x] Every deliverable has front-matter with agent/domain/evidence
- [ ] Reviewed at least two other agents' `03_DONE/` deliverables (N/A until round 2)
- [x] Official URLs checked (HTTP 200) — see `evidence/CROSSCUTTING/sources.json`
- [ ] Live instance steps executed end-to-end (pending — documented in `docs/05`, awaiting execution)
- [x] No secrets, full dumps, or generated `_site/` committed (`.gitignore` covers these)
- [x] `swarm_librarian.py validate` passes
