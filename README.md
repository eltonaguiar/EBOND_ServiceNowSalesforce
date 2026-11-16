# EBOND — ServiceNow ⇄ Salesforce Integration Lab

A progressive hands-on lab that shows how to provision a **free ServiceNow Developer instance** and a **free Salesforce Developer org**, then bond them through proof-of-concept (POC) integration exercises using out-of-the-box (OOTB) workflows and low-code methods — following platform and integration best practices.

> **Live lab site:** https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/

## Validation status

**Live integration validation pending.** Repository structure tests and Apex callout mocks are not end-to-end certification. The final-v6 review identified create/update, loop-prevention, JSON-serialization, and async-Business-Rule defects in the current capstone; use the [final-v6 review](2026-11-16-SWARM/07_final_review4/FINAL_V6_REVIEW.md), [design](2026-11-16-SWARM/07_final_review4/DESIGN.md), and [test plan](2026-11-16-SWARM/07_final_review4/TESTING_PLAN.md) before claiming a working bidirectional deployment.

## What this repo is

This repository is the working copy of the EBOND ServiceNow↔Salesforce integration lab. It is organized with the **AGENT_FOLDERFRAMEWORK** dated-SWARM layout so work happens in isolated worktrees per round, with review phases producing `final v1 → final v2 → final v3 …` refinements. The lab content lives under [`2026-11-16-SWARM/`](2026-11-16-SWARM/) and the static GitHub Pages site lives under [`site/`](site/).

## How to use the lab

Do the lab on the site. Do not start from the raw markdown files.

1. **Open the lab** — https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/ — table of contents, then Labs 0–5.
2. **Source notebook** (not the student path) — [`2026-11-16-SWARM/00_CHARTER.md`](2026-11-16-SWARM/00_CHARTER.md). Instance notes also live under `03_DONE/INSTANCES/`:
   - [ServiceNow Developer instance setup](2026-11-16-SWARM/03_DONE/INSTANCES/servicenow_dev_instance_setup.md)
   - [Salesforce Developer org setup](2026-11-16-SWARM/03_DONE/INSTANCES/salesforce_dev_org_setup.md)
3. **Choose an integration approach** — `03_DONE/INTEGRATION/` compares OOTB and custom approaches:
   - [Integration architecture options](2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md)
   - [Beginner path (Level 1→4)](2026-11-16-SWARM/03_DONE/INTEGRATION/lab_levels_beginner_path.md)
   - [ServiceNow → Salesforce outbound REST pattern](2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md)
   - [Salesforce → ServiceNow outbound pattern](2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_salesforce_outbound_to_sn.md)
   - [Integration Hub (Salesforce spoke) low-code pattern](2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_integrationhub_salesforce_spoke.md)
   - [Salesforce Connect external objects](2026-11-16-SWARM/03_DONE/INTEGRATION/pattern_salesforce_connect_external_objects.md)
4. **Run the step-by-step POC** — [Incident ↔ Case synchronization walkthrough](2026-11-16-SWARM/03_DONE/WORKFLOWS/step_by_step_poc_incident_case_sync.md)
5. **Apply best practices & QA** — `03_DONE/BESTPRACTICES/` and `03_DONE/TESTING/`
6. **Review the reference implementation (v5, capstone validation pending)** — [`lab/README.md`](lab/README.md). Repository contracts: `python3 -m pytest tests -q`; live gates are in the final-v6 test plan.

## Repository layout

| Path | Purpose |
|------|---------|
| `README.md` | This index; links to the live GitHub Pages site. |
| `site/` | Jekyll source for the student-facing GitHub Pages lab. |
| `.github/workflows/gh-pages.yml` | GitHub Actions workflow that builds `site/` with Jekyll and deploys it to Pages. |
| `2026-11-16-SWARM/` | Dated lab notebook (charter, domains, deliverables, review phases, templates). |
| `tools/swarm/swarm_librarian.py` | Canonical scaffold / collect / index / validate tooling. |

## Round / review model

Each round is a worktree. A reviewer agent then produces `final v2`, `final v3`, … per round until feedback is folded in and implementation + test plans are ready. Phase folders for those reviews already exist under the SWARM (`04_final_review/` … `07_final_review4/`).

## Integrations at a glance

| Approach | Kind | Best when |
|----------|------|-----------|
| ServiceNow **REST Message** → Salesforce REST API | Outbound, scripted | Real-time SN→SF, full control, no extra licensing |
| Salesforce **Flow / Apex** → ServiceNow REST API | Outbound | Real-time SF→SP, record-triggered flows |
| **Integration Hub** + Salesforce spoke | Low-code | Citizen-developer flows, reuse across spokes |
| **Salesforce Connect** external objects | Query-time federation | Read-only, live views of ServiceNow data inside Salesforce |
| Import Sets / Scheduled jobs | Batch | Bulk backfill, not real-time |

## Security note

No credentials are stored in this repository. The lab documents using the platforms' native secret handling (ServiceNow Connection & Credential aliases, Salesforce Named Credentials) and env/local secrets for any scripts. See `03_DONE/BESTPRACTICES/security_identity_secrets.md`.

## License / disclaimer

Educational lab content for proof-of-concept use. Free-tier terms, feature availability, and rate limits change over time; verify against the current official documentation before relying on specifics (notable "verify current terms" flags are called out in the docs).
