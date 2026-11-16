---
agent: ebond-v2
domain: PAGES
phase: 1
status: done
spans: [INTEGRATION, CROSSCUTTING]
evidence:
  - url: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/
  - path: https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/blob/main/docs/cross-cutting.md
  - verified_at: 2026-11-16T21:00:00Z
---

# Plan — link this lab from the ServiceNow_Learning cross-cutting page

The existing ServiceNow learning site has a **Cross-Cutting Platform Skills** page at:

`https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/`

It is built by **Jekyll** from `docs/cross-cutting.md` in the repo `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` (Pages build type = workflow, source `main`). The page already has an **Integrations** section, so it is the natural anchor for linking to the EBOND integration lab.

## What to change

1. **File:** `docs/cross-cutting.md` in the ServiceNow_Learning repo.
2. **Where:** inside the **Integrations** section (after the "Integration Toolset" table and/or after the "Integration Best Practices Decision Flow"), add a short subsection titled e.g. `### ServiceNow ⇄ Salesforce Integration Lab (EBOND)`.
3. **Content:** 2–4 lines describing the lab plus links:

   ```markdown
   ### ServiceNow ⇄ Salesforce Integration Lab
   Hands-on lab: free ServiceNow Developer instance + free Salesforce Developer org bonded
   into a POC (Incident ⇄ Case sync) with OOTB workflows and best practices.
   - Live lab site: https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
   - Repo: https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce
   - Core patterns: REST (SN→SF), Salesforce Flow/Apex (SF→SN), Integration Hub spoke, Salesforce Connect
   ```

4. Optionally add `- [Integrations](#integrations)` already exists; no change to Contents needed unless you add a new heading anchor (if you add a new heading, add it to the Contents list).
5. **Deploy:** commit + push to `main` of the ServiceNow_Learning repo → its Pages workflow rebuilds, and the cross-cutting page will include the new section.

## Acceptance criteria

- [ ] Cross-cutting page renders a link to the EBOND lab site.
- [ ] Link opens the live Pages site.
- [ ] No other content in the page is disturbed.

## Owner / timing

- To be executed in a follow-up round once the EBOND Pages site is live. This file is the documented plan so any future agent can apply it deterministically.
