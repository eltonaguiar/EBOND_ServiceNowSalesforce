# PLAN — ServiceNow ⇄ Salesforce Free Integration Lab

## Problem statement

There is no single, free, end-to-end resource that walks a learner through standing up a ServiceNow PDI and a Salesforce Developer org and bonding them into a real (loop-safe, securely-authenticated) integration — covering both out-of-box and custom methods with best practices.

## Root causes addressed

- **Cost barrier:** both platforms offer free dev instances, but the integration path is usually taught with paid middleware.
- **Concept gap:** one-way vs two-way, field ownership, and manual-edits-vs-integration are rarely taught explicitly, yet they are what make a sync safe.
- **Secret hygiene:** tutorials often hardcode tokens; this lab mandates Named/External Credentials + OAuth.
- **Discoverability:** the existing TSOM cross-cutting page teaches the decision framework but points at no hands-on lab.

## Proposed solution

A GitHub Pages lab (this repo) organized as four progressive levels plus supporting sections:

1. **Levels 1–2:** one-way Salesforce/Postman → ServiceNow (Table API → Flow HTTP callout).
2. **Level 3:** Scripted REST API with validation + correlation.
3. **Level 4:** bidirectional Case ⇄ Incident with OAuth 2.0, field ownership, loop guard.
4. **Supporting:** OOB menu, security, testing, appendix; plus a plan to link the lab from the TSOM cross-cutting page.

## Phased rollout

- **Phase A (done, this branch):** draft all nine docs, wire Pages, scaffold SWARM, draft this plan.
- **Phase B (next rounds):** peer review → `finalv2`/`finalv3` → correct facts, tighten steps, add click-by-click where flagged.
- **Phase C:** merge to `main`, confirm Pages deploy, execute the TSOM cross-cutting link PR.
- **Phase D (optional, later):** switch Pages to `just-the-docs` for search + nav; add a Service Graph Connector section.

## Risks and mitigations

| Risk | Mitigation |
|------|-----------|
| Free-tier entitlements drift (spokes, API limits) | Flagged ⚠️ in-line; verification items tracked in `08-appendix.md` §8.6 |
| Salesforce credential UI labels shift across releases | Documented as the Level 2 "gotcha"; verify at review |
| Dead link if lab merges after the TSOM PR | Precondition gates the TSOM PR on the lab's Pages deploy |
| Secrets accidentally committed | `.gitignore` + pre-flight checklist + `git grep` QA gate |

## Success metrics

- All 10 charter success criteria (S1–S10) satisfied.
- The leveled lab is reproducible end-to-end by a fresh agent in ≤2.5h using only this repo + the two free signups.
- The TSOM cross-cutting page links the lab and the link resolves.
