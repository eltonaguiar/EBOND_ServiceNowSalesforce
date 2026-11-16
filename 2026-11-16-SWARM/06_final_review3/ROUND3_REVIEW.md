# ROUND3_REVIEW — 06_final_review3

**Round:** 3 (final v3) · **Agent:** kilo · **Date:** 2026-11-16

## Verdict

**implement** — v2 is complete and coherent; four concrete defects fixed in this round, one carried as an open verification item.

## Findings fixed (with evidence)

### F1 — Correlation field name bug (blocking for reproducibility)
- **Where:** `03_DONE/INTEGRATION/lab_levels_beginner_path.md` Level 3 script used `gr.correlation_id`, which is **not** a valid ServiceNow `incident` field (the standard field is `sys_mod_count`/`number`; there is no OOB `correlation_id`).
- **Fix:** changed to the custom field `x_snc_ebond_sf_case_id` (the correlation key already defined in `data_model_field_mapping.md`), and updated the Level-4 note + `field_ownership_and_manual_edits.md` to use the same concrete name.
- **Why it matters:** a reader following the script verbatim would hit an "invalid field" error; consistency with the mapping doc is required for the loop-guard to work.

### F2 — Salesforce OAuth password-grant deprecation (accuracy)
- **Where:** `03_DONE/INTEGRATION/pattern_sn_outbound_rest_to_salesforce.md` used `grant_type=password` as the primary token snippet.
- **Fix:** added a ⚠️ deprecation warning and elevated **client-credentials** / **JWT bearer** as the preferred flows.

### F3 — POC loop prevention under-specified (correctness)
- **Where:** `03_DONE/WORKFLOWS/step_by_step_poc_incident_case_sync.md` Phase 3 stated "the correlation-key gate usually suffices" for loop prevention.
- **Fix:** replaced with the three-pronged guard (source flag + timestamp comparison + delta guard) already documented in `field_ownership_and_manual_edits.md`. A correlation key prevents *duplicates*, not *loops*.

### F4 — Rate-limit bullet truncation (formatting)
- **Where:** `03_DONE/BESTPRACTICES/rate_limits_monitoring_logging.md` — the Salesforce bullet was cut mid-sentence ("…when batching on- **ServiceNow:**").
- **Fix:** split into two clean bullets.

## Carried (open) verification items

These are deliberate "verify current terms" flags, unchanged in v3, to be resolved with live instances in a later round:

1. Integration Hub Salesforce spoke availability/entitlement on a current PDI.
2. Salesforce Developer Edition data storage + daily API request limit.
3. ServiceNow inbound OAuth grant type on current release.
4. Salesforce REST API version (docs use `v58.0+`; bump to current org version).

## Checklist

- [x] Every changed file keeps valid agent/domain front-matter (no new deliverables added).
- [x] No secrets committed (scanned).
- [x] `swarm_librarian.py validate --dir 2026-11-16-SWARM` exits 0.
- [x] Changes are additive/consistent with `data_model_field_mapping.md` (single source of truth).
- [x] INDEX regenerated.

## Evidence

- Field-name consistency: `data_model_field_mapping.md` §Correlation keys defines `x_snc_ebond_sf_case_id` (SN record) and `x_snc_ebond_sn_incident_id__c` (SF record).
- Salesforce OAuth deprecation: username-password flow is being retired; client-credentials/JWT are the machine-to-machine alternatives (Salesforce OAuth docs).
