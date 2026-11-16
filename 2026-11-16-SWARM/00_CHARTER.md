# 00_CHARTER.md — 2026-11-16 SWARM

## Mission

Build and document a **proof-of-concept lab** that:
1. Provisions a **free ServiceNow Developer instance** (developer.service-now.com).
2. Provisions a **free Salesforce Developer org** (Developer Edition, developer.salesforce.com).
3. Bonds the two together with an integration that uses **out-of-the-box workflows and low-code methods** (plus a scripted fallback), conforming to platform and integration best practices.
4. Publishes the lab as a **GitHub Pages site** and links to it from this repo's `README.md`.

## Deliverable scope (Round 1 / v1)

- Instance provisioning guides for both free tiers.
- Comparison of integration approaches (OOTB + custom).
- A working, reproducible POC recipe: **ServiceNow Incident ⇄ Salesforce Case** bidirectional sync.
- Best-practice guidance: identity/security, reliability, rate limits, monitoring, source control.
- QA and test plan.
- GitHub Pages deploy + a plan to link the lab from the existing ServiceNow_Learning cross-cutting page.

## Non-goals

- Production deployment, paid tiers, or enterprise licensing advice.
- Storing any real credentials in this repository.
- Building a full enterprise iPaaS migration; we cover the relevant patterns and call out where an iPaaS wins.

## Domain set (from `swarm_domains.txt`)

`INSTANCES`, `INTEGRATION`, `WORKFLOWS`, `BESTPRACTICES`, `TESTING`, `PAGES`, plus `CROSSCUTTING` as the escape hatch.

## Phase gates checklist

Before `04_final_review/` is considered done, tick:

- [ ] Every `03_DONE/<DOMAIN>/` deliverable has agent/domain front-matter.
- [ ] Every claim carries evidence: a repo-relative path, a URL, or a commit SHA.
- [ ] No secrets ever committed (no `.env`, tokens, or keys).
- [ ] `swarm_librarian.py validate --dir 2026-11-16-SWARM` exits 0.
- [ ] Local git diff checked; only intended files staged.
- [ ] The Pages site builds and deploys; URL verified in README.
