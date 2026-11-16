---
agent: v1-bond-lab
domain: DOCS_SITE
phase: 1
status: done
spans: [CROSSCUTTING]
evidence:
  - path: ../../../../ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting.md
    repo: eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM
    sha: 5f1d54a
    verified_at: 2026-11-16T20:36:00Z
  - url: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/
    verified_at: 2026-11-16T20:36:00Z
---

# CROSSCUTTING — plan to link this lab from the TSOM cross-cutting page

## Goal

Update the **Cross-Cutting Platform Skills → Integrations** page so learners who reach the integration decision framework are pointed at this hands-on lab.

## Target

- **Repo:** `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`
- **File:** `docs/cross-cutting.md` (confirmed present on `main`, SHA `5f1d54a`)
- **Rendered URL:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/
- **Pages deploy:** `build_type: workflow`, branch `main`, path `/` — so the edit must land on `main` to publish.

## Precondition

This lab (`EBOND_ServiceNowSalesforce`) must be **merged to `main` and its Pages site deployed** first, so the link below is not dead. The link is:

```
https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
```

## Proposed edit

Insert immediately after the "Integration Toolset" table in the `## Integrations` section (before the `🚀 Interview Insight` details block):

```markdown
> 🧪 **Hands-on lab:** walk a real, free ServiceNow ⇄ Salesforce integration end-to-end —
> provision a PDI + a Salesforce Developer org and bond them (Table API → Flow callout →
> Scripted REST → bidirectional sync with OAuth, field ownership, and loop prevention).
> **[EBOND_ServiceNowSalesforce — Free Integration Lab](https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/)**
```

## Delivery steps

1. In the TSOM repo, create a branch off `main` (e.g. `docs/link-sn-sf-lab-2026-11-16`).
2. Make the single-file edit above.
3. Open a **PR → `main`** with title like `docs(cross-cutting): link ServiceNow⇄Salesforce free integration lab`.
4. After merge, the `workflow` Pages deploy rebuilds; verify the link renders and resolves.

## Verification

- [ ] `docs/cross-cutting.md` diff contains only the added block (no unrelated edits).
- [ ] Merged to `main`.
- [ ] https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/ renders the link.
- [ ] The link opens the lab's Pages home (200).

## Notes / risks

- The local TSOM checkout is currently on feature branch `direction-a-gaps-sam-guide-2026-11-13`, which has **no changes** to `cross-cutting.md`; do the edit on a fresh branch off `origin/main` to avoid dragging unrelated SAM-guide changes into the link PR.
- The `jekyll-relative-links` plugin rewrites repo-relative `(...)` links, but an **absolute https URL** (used above) is left untouched — safest choice for a cross-repo link.
