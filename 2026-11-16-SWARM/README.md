# 2026-11-16-SWARM — ServiceNow ⇄ Salesforce free-integration lab

Dated artifact folder implementing the **Swarm / Isolated-Worktree Framework** (see `eltonaguiar/AGENT_FOLDERFRAMEWORK`). Domains are generic/config-driven (see `swarm_domains.txt`) — `INSTANCE_SETUP`, `OOB_INTEGRATION`, `CUSTOM_INTEGRATION`, `SECURITY`, `DOCS_SITE`, plus `CROSSCUTTING`.

| Phase | Where | Who | Status |
|-------|-------|-----|--------|
| 0 – Charter | `00_CHARTER.md` | kilo (lead) | done |
| 1 – Isolated attempt | `03_DONE/<DOMAIN>/` | kilo (`v1-bond-lab`) | done (this round) |
| 2 – First peer review | `04_final_review/` | reviewers | pending (next round) |
| 3 – Second pass | `05_final_reviewv2/` | reviewers | pending |
| 4 – Subset synthesis | `06_final_review3/` | synthesizer | pending |
| 5 – Final plan | `07_final_review4/` | synthesizer | draft present |

## Rules that bite if ignored

- **Evidence-linked**: every `03_DONE` deliverable carries front-matter with `agent`/`domain`/`evidence`.
- **No silent overwrites**: reviewers add new files; they never edit a peer's deliverable.
- **Markdown + small JSON only**: no `.env`, keys, or generated `_site/`.
- **Final plan is a draft until review**: `07_final_review4/*` here is the round-1 draft, to be refined by `finalv2`/`finalv3`.

## Tooling

`tools/swarm/swarm_librarian.py` — `scaffold` (generic `--domains`), `collect`, `index`, `validate`.
