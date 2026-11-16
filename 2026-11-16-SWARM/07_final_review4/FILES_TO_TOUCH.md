# FILES_TO_TOUCH — ServiceNow ⇄ Salesforce Free Integration Lab

Every path this lab creates or modifies, with purpose and risk.

| Path | Purpose | Risk |
|------|---------|------|
| `README.MD` | Root overview + live Pages link | Low |
| `index.md` | Pages home + level map | Low |
| `_config.yml` | Jekyll config (theme, excludes) | Med — wrong exclude hides docs |
| `docs/00-overview.md` … `docs/08-appendix.md` | The lab content | Med — factual accuracy |
| `.github/workflows/pages.yml` | Pages deploy (GitHub Actions) | Med — must be on `main` to run |
| `.gitignore` | Exclude secrets + `_site/` | High if missing — secret leak |
| `tools/swarm/swarm_librarian.py` | SWARM scaffold/validate tooling | Low |
| `2026-11-16-SWARM/` | Charter, deliverables, plan, evidence | Low |
| `2026-11-16-SWARM/evidence/CROSSCUTTING/sources.json` | Verified URL evidence | Low |
| `2026-11-16-SWARM/03_DONE/DOCS_SITE/v1_tsom_crosscutting_link_plan.md` | Plan to link TSOM page | Low |

## Out-of-repo (separate PR, later)

| Path | Repo | Purpose |
|------|------|---------|
| `docs/cross-cutting.md` | `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` | Add lab link in `## Integrations` |

## Safety notes

- Do not commit `_site/`, `.jekyll-cache/`, or any secret — `.gitignore` covers these.
- The Pages workflow intentionally triggers only on `main` (not feature branches) to avoid redundant deploys.
- The TSOM edit is a separate repo/PR; do not mix it into this repo's branch.
