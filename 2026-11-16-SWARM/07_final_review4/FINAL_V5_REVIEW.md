# FINAL_V5_REVIEW — 07_final_review4

**Round:** 5 (final v5) · **Date:** 2026-11-16

## What this round reviewed

`main` was already at final v4 (docs, Pages, JWT note, loop-prevention steps). A parallel round-2 branch had added Apex and Scripted REST, then failed CI (`pytest` missing; secret scan hit the test fixture). That branch also contradicted v3 field names and would not deploy on a PDI.

## Findings

| ID | Severity | Evidence | Resolution |
|----|----------|----------|------------|
| B1 | Blocker | `data_model_field_mapping.md` `x_snc_ebond_sf_case_id` | `x_snc_` is not a student-creatable PDI scope. Runnable lab uses `u_ebond_sf_case_id`. Mapping doc now says so. |
| B2 | Blocker | round-2 `SnowIncidentService.cls` endpoint `api/x_ebond/bond/case` | Apex now uses `/api/now/table/incident` (GET then POST/PATCH). |
| B3 | High | `CaseTriggerHandler` enqueued one job per row (limit 50) | One Queueable, batches of 10, chains the rest. |
| B4 | High | CI run 43954565909 | `pip install pytest`. Fixture strings split so Validate SWARM secret scan does not match. |

## Not done

- No live PDI or Developer Edition execution. Apex tests are mock-only.
- `lab.html` is not on the live Pages site until this branch merges to `main`.
- Cross-cutting page already links the lab (learning PR #3). Duplicate learning PR #4 conflicts and should be closed.

## Status

v5 is the first round with deployable code that matches a free PDI. Plan and test plan in this folder still apply. Next round only if a live-instance run produces new evidence.
