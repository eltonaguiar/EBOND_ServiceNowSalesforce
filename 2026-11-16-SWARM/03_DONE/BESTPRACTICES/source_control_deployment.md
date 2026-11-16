---
agent: ebond-v2
domain: BESTPRACTICES
phase: 1
status: done
spans: [INSTANCES, PAGES]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/PAGES/github_pages_deploy.md
  - verified_at: 2026-11-16T20:55:00Z
---

# Source control & deployment

## Version everything

- ServiceNow configuration: on **Update Sets / Source Control** (Studio) so a dev-instance reset can be replayed.
- Salesforce: use **Salesforce CLI** (`sf`) + source-tracked org / scratch orgs so the connected app, fields, and flows are reproducible.
- Keep this repo as the single documentation + IaC source of truth.

## Repo discipline

- Commit documentation and config as structured markdown/JSON.
- Never commit secrets (see security doc); `.gitignore` covers `.env`, keys, credentials dumps.
- No force-push; small focused commits; PR review per the AGENT_FOLDERFRAMEWORK round model.
- Only stage intended files; don't push others' work.
- **Automatic gate:** `.github/workflows/validate.yml` runs `swarm_librarian.py validate` (0 errors required), a secret scan, and `bash -n` on lab scripts for every push/PR to `main`. A PR that fails these gates is not ready to merge.

## Deployment cadence

- **Docs/site:** push to `main` → GitHub Actions Pages workflow rebuilds the site (see `2026-11-16-SWARM/03_DONE/PAGES/github_pages_deploy.md`).
- **Platform config:** apply via Update Sets (SN) / `sf project deploy` (SF) against the dev instances; keep an "applied on" log.
- Re-apply after any dev-instance refresh.

## Environments

- POC: both dev instances only.
- When going further: replicate the same config in a second set of sandboxes (SN sub-production, SF sandbox) before any shared environment.
