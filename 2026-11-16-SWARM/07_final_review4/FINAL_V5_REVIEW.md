# FINAL_V5_REVIEW — 07_final_review4

**Round:** 5 (final v5) · **Agent:** kilo (independent review) · **Date:** 2026-11-16

## Independent review (Round 5)

A fresh read-only pass over the full `03_DONE/` set and the published surface found two residual defects that the v3/v4 reviews did not cover. Verdict: **implement** after these two (non-blocking, but they hurt a copy-paste reader).

## Findings adopted (this round)

### N1 — truncated Salesforce rate-limit bullet (formatting)
- **Where:** `03_DONE/BESTPRACTICES/rate_limits_monitoring_logging.md` — the Salesforce bullet was cut mid-sentence ("…when batching on- **ServiceNow:**").
- **Fix:** split into two clean bullets (Salesforce limits vs ServiceNow thresholds).

### N2 — generic correlation-field reference (consistency)
- **Where:** `03_DONE/BESTPRACTICES/field_ownership_and_manual_edits.md` still said "(`correlation_id` or a custom field)", while the canonical mapping (`data_model_field_mapping.md`) and v3 field-alignment use the concrete custom field `x_snc_ebond_sf_case_id`.
- **Fix:** replace with the concrete field name so the ownership doc, mapping doc, and Level-3 script all agree.

## Re-verified this round

- `swarm_librarian.py validate --dir 2026-11-16-SWARM --repo-root .` → 0 errors / 0 warnings.
- `git grep -n "correlation_id"` → only the canonical `x_snc_ebond_sf_case_id` references remain (no stray generic `correlation_id`).
- `git grep -n "batching on-"` → no matches (truncation resolved).
- Secret scan clean; no new secrets; only two Markdown lines + this doc changed.

## Carried open items (unchanged — require live instances)

1. Integration Hub Salesforce spoke entitlement on a current PDI.
2. Salesforce DE org data storage + daily API limit.
3. ServiceNow inbound OAuth grant type on current release.
4. Salesforce REST API version pin (`v58.0+` → current).

## Status

`final v5` — the only remaining items are the four live-instance "verify current terms" flags above; content, plan, and test artifacts are otherwise complete and validated.
