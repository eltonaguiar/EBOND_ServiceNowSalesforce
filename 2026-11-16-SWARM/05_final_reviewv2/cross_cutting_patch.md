---
agent: ebond-round2
domain: PAGES
phase: 2
status: done
evidence:
  - path: /tmp/snlearn/docs/cross-cutting.md
  - url: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/cross-cutting/
  - verified_at: 2026-11-16T20:50:00Z
---

# Patch plan — ServiceNow_Learning cross-cutting page

Verified against clone of `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` at `docs/cross-cutting.md` (504 lines, Jekyll, `permalink: pretty`).

## Anchors (do not guess)

| Item | Location |
|------|----------|
| Contents list | lines 10-36. Integrations bullet already exists at the Contents entry `- [Integrations](#integrations)`. |
| Integrations section | starts line 38 `## Integrations`. |
| Toolset table | lines 42-53. |
| Decision flow | ends before line 139 `## Scripting`. |
| Salesforce track | `docs/salesforce/labs-design.md` Lab 4 is "Make a REST API Callout" — second link, optional. |

Insert the new subsection **after the Integration Best Practices Decision Flow and before `## Scripting`**. Do not insert inside the `<details>` interview block (lines 55-97).

## Contents line to add

After `- [Integrations](#integrations)` add:

```markdown
- [ServiceNow ⇄ Salesforce lab](#servicenow--salesforce-lab)
```

## Subsection to insert

```markdown
### ServiceNow ⇄ Salesforce lab

Hands-on POC: a free ServiceNow Personal Developer Instance and a free Salesforce Developer Edition org, bonded as Incident ⇄ Case.

- Live lab: https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
- Lab steps on that site: https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/lab.html
- Repo: https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce
- Runnable code: `lab/` in that repo (Table API curl, Scripted REST, Apex Queueable callout, async Business Rule). External Client App on Salesforce — do not create a Connected App (blocked for new apps since Spring '26).

This lab is the worked example for the toolset above: Table API and Scripted REST inbound, REST Message outbound, Flow HTTP Callout or Apex for the Salesforce side.
```

## Optional second link

In `docs/salesforce/labs-design.md`, under Pre-Existing Labs, add one table row pointing at the same live lab URL. Do not rewrite Lab 4.

## Deploy

Commit on a branch of the learning repo. Push. Open a PR to `main`. That repo's Pages workflow rebuilds `docs/cross-cutting/` (pretty permalink). Do not force-push.

## Acceptance

- Rendered page contains the heading and both URLs.
- Existing Integrations toolset table is unchanged.
- No secrets in the diff.
