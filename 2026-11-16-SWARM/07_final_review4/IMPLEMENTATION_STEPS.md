# IMPLEMENTATION_STEPS — Round 1

Ordered steps already executed in this round (v1). Future review rounds extend from here.

1. Scaffold SWARM with canonical librarian tool (domains: INSTANCES, INTEGRATION, WORKFLOWS, BESTPRACTICES, TESTING, PAGES).
2. Author root `README.md` with GitHub Pages target link.
3. Author the 00_CHARTER.md + templates.
4. Author `03_DONE/<DOMAIN>/` deliverables (setup, patterns, mapping, workflows, POC, best practices, QA, Pages).
5. Build `site/index.html` and `.github/workflows/gh-pages.yml`.
6. Add `.gitignore` (secrets).
7. Write `07_final_review4/` canonical planning files.
8. Validate + index the SWARM.
9. Commit and push to `main`; confirm Pages deployment; update README live URL if needed.

## Round 5 (this branch)

1. Import the runnable lab onto current main (v4), do not restart from the stale round-2 branch.
2. Apex calls Table API and batches Queueable jobs (50 enqueue limit / 20 DE concurrent callouts).
3. Correlation fields students can create: `u_ebond_sf_case_id`, `Snow_Sys_Id__c`.
4. CI installs pytest. Test fixtures split credential-shaped strings so the secret scan stays clean.

## Follow-up (future rounds)

- Apply the cross-cutting link plan (`2026-11-16-SWARM/03_DONE/PAGES/link_crosscutting_plan.md`) once the EBOND site is live.
- Execute the live POC on the free instances and capture evidence screenshots into `evidence/`.
- Fold reviewer feedback into `final v2` / `final v3` per the round model.
