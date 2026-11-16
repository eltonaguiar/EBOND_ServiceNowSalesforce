---
agent: ebond-round2
domain: CROSSCUTTING
phase: 2
status: done
evidence:
  - path: README.md
  - path: site/index.html
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/data_model_field_mapping.md
  - path: .github/workflows/gh-pages.yml
  - verified_at: 2026-11-16T20:45:00Z
---

# Round 2 review of v1

v1 published a usable notebook and a Pages landing page. It does not yet let a student deploy the POC.

## Findings

| ID | Severity | Evidence | Finding |
|----|----------|----------|---------|
| R1 | Blocker | repo root has no `lab/` before this round | No Apex, no Scripted REST, no REST Message body, no curl. The step-by-step doc describes clicks only. |
| R2 | High | `data_model_field_mapping.md` lines 33-34 | Correlation fields use scoped prefix `x_snc_ebond_*`. A free PDI lab is global. Those names will not exist unless a scoped app is published, which a PDI cannot do to the Store. |
| R3 | High | `03_DONE/TESTING/` | QA is prose. Nothing fails a commit if a link or class is dropped. |
| R4 | Medium | `site/index.html` | Pages site is a link list into GitHub blobs. A student who opens the Pages URL never sees a command. |
| R5 | Medium | `link_crosscutting_plan.md` | Target file is correct (`docs/cross-cutting.md`, Integrations section). Insertion point and Contents line were not pinned to line numbers, so a later edit can land in the wrong heading. |
| R6 | Low | `gh-pages.yml` | Deploy path `site/` matches Pages source `/` with `build_type=workflow`. Permissions and `deploy-pages@v4` are valid. No contract test job. |
| R7 | Low | v1 pattern docs | Integration Hub spoke is correctly marked license-sensitive. Connected App vs External Client App (Spring '26 creation block) is not stated. |

## What v1 got right

- Isolation layout matches folderframework-v3 (dated SWARM, phase folders, librarian).
- Secrets stay out of git (`.gitignore` covers `.env`, pem, keys).
- One-way-first beginner path matches the simpler lab the user pasted (curl → Flow → Scripted REST → field ownership).
- Pages URL is already in `README.md` line 5.

## v2 response

R1, R2, R3, R6 are closed in this round under `lab/`, `tests/`, and `.github/workflows/ci.yml`. R4 is closed by `site/lab.html`. R5 is closed by the patched plan in `05_final_reviewv2/cross_cutting_patch.md`. R7 is documented in `lab/README.md` (External Client App, not Connected App).
