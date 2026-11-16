---
agent: ebond-v2
domain: TESTING
phase: 1
status: done
spans: [PAGES]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/TESTING/qa_test_plan.md
  - verified_at: 2026-11-16T21:00:00Z
---

# Verification checklist

Run this before declaring any round complete.

## Repository / SWARM

- [ ] `python3 tools/swarm/swarm_librarian.py validate --dir 2026-11-16-SWARM` exits 0.
- [ ] `swarm_librarian.py index` regenerated (INDEX.md current).
- [ ] All `03_DONE` deliverables have agent/domain front-matter.
- [ ] No secrets (run a grep for keys/tokens).
- [ ] `git status` shows only intended files.

## GitHub Pages

- [ ] Pages workflow runs green on `main`.
- [ ] `https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/` loads.
- [ ] README.md contains the live site link.

## Lab content

- [ ] Both provisioning guides present and accurate (SN, SF).
- [ ] Integration patterns + mapping present.
- [ ] POC walkthrough + OOTB workflows present.
- [ ] Best practices (security/reliability/limiting/source control) present.
- [ ] QA plan present.
- [ ] Cross-cutting link plan present (see `2026-11-16-SWARM/03_DONE/PAGES/link_crosscutting_plan.md`).
