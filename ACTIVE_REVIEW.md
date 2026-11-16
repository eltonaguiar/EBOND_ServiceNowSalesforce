# Active Review — final-v6 (independent synthesis)

Other agents and humans: this pointer tells you where the current EBOND review lives.

## Where to look

- **Review branch/worktree:** `review/final-v6`
- **Pull request:** https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce/pull/6
- **Review verdict and findings:** `2026-11-16-SWARM/07_final_review4/FINAL_V6_REVIEW.md`
- **Design:** `2026-11-16-SWARM/07_final_review4/DESIGN.md`
- **Implementation plan:** `2026-11-16-SWARM/07_final_review4/IMPLEMENTATION_STEPS.md`
- **Test/live acceptance plan:** `2026-11-16-SWARM/07_final_review4/TESTING_PLAN.md`
- **File manifest:** `2026-11-16-SWARM/07_final_review4/FILES_TO_TOUCH.md`

## Current status

**Live integration validation is pending.** The repository's structural tests pass, but the runnable bidirectional capstone has release-blocking findings (create-only Salesforce trigger, sticky loop guards, unsafe JSON, async Business-Rule `previous` usage, competing callback APIs, and an unsupported "working" claim). The final-v6 PR is the planning/review artifact; it is not a live-deployment claim and does not merge itself.

Do not start implementation from the stale `v1-bond-lab`, `round2`, or `v3-review` branches wholesale. Base implementation on `main` + this v6 review and use the canonical correlation/ownership contract in `DESIGN.md`.

## Required next steps

1. Human review and merge `review/final-v6` (PR #6) after the strict repository gate is acceptable.
2. Execute the implementation plan tasks and the live E2E acceptance matrix.
3. Update the `Live integration validation pending` status only when live evidence exists.
4. Open the separate `docs/cross-cutting.md` link-follow-up PR in `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` once the lab page is live.
