# EBOND_ServiceNowSalesforce — Free Instance Integration Lab

A hands-on lab that provisions a **free ServiceNow Personal Developer Instance (PDI)** and a **free Salesforce Developer Edition org**, then **bonds them together** into a working proof-of-concept (PoC) integration — using both **out-of-box workflows** and **custom REST/OAuth methods**, while conforming to security and platform best practices.

> **🌐 Live lab site (GitHub Pages):** https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
>
> The site is built from the `docs/` and `index.md` files in this repo and deploys automatically on merge to `main` (see [`.github/workflows/pages.yml`](.github/workflows/pages.yml)). It goes live after the first merge.

---

## What this lab covers

The lab climbs four levels (one-way → two-way), with supporting sections for the out-of-box menu, security, and testing.

| # | Topic | File |
|---|-------|------|
| 0 | Overview, architecture & core concepts (direction, field ownership, manual edits) | [`docs/00-overview.md`](docs/00-overview.md) |
| 1 | Provisioning the two free instances (with breadcrumbs) | [`docs/01-free-instances.md`](docs/01-free-instances.md) |
| 2 | Out-of-box integration methods (Table API, REST Message, spokes, Named/External Credentials, …) | [`docs/02-out-of-box-integration.md`](docs/02-out-of-box-integration.md) |
| 3 | **Level 1–2** — one-way sync (Postman → Table API → Salesforce Flow HTTP callout) | [`docs/03-level-1-and-2-one-way.md`](docs/03-level-1-and-2-one-way.md) |
| 4 | **Level 3** — Scripted REST API (validation + correlation) | [`docs/04-level-3-scripted-rest.md`](docs/04-level-3-scripted-rest.md) |
| 5 | **Level 4** — bidirectional sync, field ownership & OAuth 2.0 | [`docs/05-level-4-bidirectional.md`](docs/05-level-4-bidirectional.md) |
| 6 | Security & best practices (secrets, OAuth, least privilege, rate limits) | [`docs/06-security-best-practices.md`](docs/06-security-best-practices.md) |
| 7 | Testing & validation plan | [`docs/07-testing-validation.md`](docs/07-testing-validation.md) |
| 8 | Appendix — field map, glossary, links, troubleshooting | [`docs/08-appendix.md`](docs/08-appendix.md) |

## The two free instances at a glance

| | ServiceNow | Salesforce |
|---|---|---|
| **Free offering** | Personal Developer Instance (PDI) | Developer Edition org / Trailhead Playground / Scratch org |
| **Signup** | https://developer.servicenow.com | https://developer.salesforce.com/signup |
| **Included** | Full ITSM platform, REST/SOAP APIs, Flow Designer, scoped app dev, update sets | Full Sales Cloud objects, Apex, REST/SOAP APIs, Flow, Platform Events |
| **Lifecycle** | Reclaimed after ~10 days inactivity (re-request any time) | Developer Edition is permanent; Playgrounds are disposable; scratch orgs expire ≤30 days |
| **Ideal for** | Low-code integration + platform admin | CRM-side callouts + Apex/Flow automation |

## Repository layout

```
EBOND_ServiceNowSalesforce/
├── README.MD                 # this file
├── index.md                  # GitHub Pages home page
├── _config.yml               # Jekyll (Pages) config
├── docs/                     # the lab guide (00–07)
├── .github/workflows/pages.yml  # Pages deploy (GitHub Actions)
├── tools/swarm/swarm_librarian.py  # SWARM framework tooling
└── 2026-11-16-SWARM/         # Swarm / isolated-worktree review artifacts
    ├── 00_CHARTER.md         # scope, success criteria, roster
    ├── 01_TODO/ 02_IN_PROGRESS/ 03_DONE/   # phased agent deliverables
    ├── 04_final_review/ … 07_final_review4/ # peer-review + final plan
    └── evidence/             # redacted evidence (URLs, sources)
```

## Collaboration model

This repo follows the **Swarm / Isolated-Worktree Framework** from [`eltonaguiar/AGENT_FOLDERFRAMEWORK`](https://github.com/eltonaguiar/AGENT_FOLDERFRAMEWORK):

- Each agent works in its own isolated worktree/branch (this round: `v1-bond-lab`).
- Artifacts land in the dated `2026-11-16-SWARM/` folder with evidence-linked front-matter.
- Future rounds (`finalv2`, `finalv3`, …) peer-review and converge on a final implementation + test plan in `07_final_review4/`.

## Status

- [x] Round 1 (this branch): lab guide drafted across all seven sections, GitHub Pages wired, SWARM scaffold + phase-1 deliverables + draft plan.
- [ ] Round 2+: peer review, `finalv2`/`finalv3`, converge on the final plan in `07_final_review4/`.

## Quick start (for the reader)

1. Provision the two free instances — [docs/01](docs/01-free-instances.md).
2. Review the out-of-box menu — [docs/02](docs/02-out-of-box-integration.md).
3. Climb the levels: [Level 1–2](docs/03-level-1-and-2-one-way.md) → [Level 3](docs/04-level-3-scripted-rest.md) → [Level 4](docs/05-level-4-bidirectional.md).
4. Harden with [security](docs/06-security-best-practices.md) and verify with the [test plan](docs/07-testing-validation.md).
