# EBOND — ServiceNow ⇄ Salesforce Integration Lab

A hands-on lab that shows how to provision a **free ServiceNow Developer instance** and a **free Salesforce Developer org**, and bond them together into a working proof-of-concept (POC) integration using out-of-the-box (OOTB) workflows and low-code methods — following platform and integration best practices.

> **Live lab site:** https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/

## What this repo is

This repository is the working copy of the EBOND ServiceNow↔Salesforce integration lab. It is organized with the **AGENT_FOLDERFRAMEWORK** dated-SWARM layout so work happens in isolated worktrees per round, with review phases producing `final v1 → final v2 → final v3 …` refinements. The lab content lives under [`2026-11-16-SWARM/`](2026-11-16-SWARM/) and the static GitHub Pages site lives under [`site/`](site/).

## How to use the lab

1. **Read the mission & charter** — [`2026-11-16-SWARM/00_CHARTER.md`](2026-11-16-SWARM/00_CHARTER.md)
2. **Provision your free instances** — see `03_DONE/INSTANCES/`:
   - [ServiceNow Developer instance setup](2026-11-16-SWARM/03_DONE/INSTANCES/servicenow_dev_instance_setup.md)
   - [Salesforce Developer org setup](2026-11-16-SWARM/03_DONE/INSTANCES/salesforce_dev_org_setup.md)
3. **Choose an integration approach** — `03_DONE/INTEGRATION/` compares OOTB and custom approaches:
   - [Integration architecture options](2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md)
   - [Beginner path (Level 1→4)](2026-11-16-SWARM/03_DONE/INTEGRATION/lab_levels_beginner_path.md)
   - ServiceNow → Salesforce outbound REST pattern
   - Salesforce → ServiceNow outbound pattern
   - Integration Hub (Salesforce spoke) low-code pattern
   - Salesforce Connect external objects
4. **Run the step-by-step POC** — [Incident ↔ Case synchronization walkthrough](2026-11-16-SWARM/03_DONE/WORKFLOWS/step_by_step_poc_incident_case_sync.md)
5. **Apply best practices & QA** — `03_DONE/BESTPRACTICES/` and `03_DONE/TESTING/`

## Repository layout

| Path | Purpose |
|------|---------|
| `README.md` | This index; links to the live GitHub Pages site. |
| `site/` | Static content deployed to GitHub Pages (the lab landing page). |
| `.github/workflows/gh-pages.yml` | GitHub Actions workflow that builds and deploys `site/` to Pages. |
| `2026-11-16-SWARM/` | Dated lab notebook (charter, domains, deliverables, review phases, templates). |
| `tools/swarm/swarm_librarian.py` | Canonical scaffold / collect / index / validate tooling. |

## Round / review model

Each round is a worktree. A reviewer agent then produces `final v2`, `final v3`, … per round until feedback is folded in and implementation + test plans are ready. Phase folders for those reviews already exist under the SWARM (`04_final_review/` … `07_final_review4/`).

## Integrations at a glance

| Approach | Kind | Best when |
|----------|------|-----------|
| ServiceNow **REST Message** → Salesforce REST API | Outbound, scripted | Real-time SP→SF, full control, no extra licensing |
| Salesforce **Flow / Apex** → ServiceNow REST API | Outbound | Real-time SF→SP, record-triggered flows |
| **Integration Hub** + Salesforce spoke | Low-code | Citizen-developer flows, reuse across spokes |
| **Salesforce Connect** external objects | Query-time federation | Read-only, live views of ServiceNow data inside Salesforce |
| Import Sets / Scheduled jobs | Batch | Bulk backfill, not real-time |

## Security note

No credentials are stored in this repository. The lab documents using the platforms' native secret handling (ServiceNow Connection & Credential aliases, Salesforce Named Credentials) and env/local secrets for any scripts. See `03_DONE/BESTPRACTICES/security_identity_secrets.md`.

## License / disclaimer

Educational lab content for proof-of-concept use. Free-tier terms, feature availability, and rate limits change over time; verify against the current official documentation before relying on specifics (notable "verify current terms" flags are called out in the docs).
