---
agent: v1-bond-lab
domain: CUSTOM_INTEGRATION
phase: 1
status: done
spans: [OOB_INTEGRATION, SECURITY]
evidence:
  - path: docs/03-level-1-and-2-one-way.md
    verified_at: 2026-11-16T20:35:00Z
  - path: docs/04-level-3-scripted-rest.md
    verified_at: 2026-11-16T20:35:00Z
  - path: docs/05-level-4-bidirectional.md
    verified_at: 2026-11-16T20:35:00Z
  - url: https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/concept/oauth-2-0.html
    verified_at: 2026-11-16T20:35:00Z
---

# CUSTOM_INTEGRATION — leveled bonding path (Levels 1–4)

Deliverables: `docs/03-level-1-and-2-one-way.md`, `docs/04-level-3-scripted-rest.md`, `docs/05-level-4-bidirectional.md`.

## What was done

- Adopted a **progressive level structure** (peer-supplied approach) over a flat section list:
  - **Level 1** — Postman/curl → Table API (one-way, Basic Auth).
  - **Level 2** — Salesforce Flow HTTP Callout via **External Credential + Named Credential + Permission Set** (the modern Salesforce credential pattern).
  - **Level 3** — Scripted REST API with validation + idempotent upsert keyed on a correlation field.
  - **Level 4** — bidirectional Case ⇄ Incident with OAuth 2.0, field ownership, and loop guard.
- Incorporated the **field-ownership / system-of-record** and **manual-edits vs integration** concepts that the first draft under-weighted.
- Documented the **loop guard** (origin flag + correlation ID) and full happy-path sequence.

## Key decisions / rationale

- **Basic Auth for Levels 1–3, OAuth for Level 4** — matches the pedagogical arc (simplest first) and the security section's "basic auth is dev-only" rule.
- **External Credential + Permission Set** is the correct current Salesforce setup and was missing from the first draft; now spelled out as the Level 2 "gotcha".

## Open items for review

- Verify the exact Named/External Credential UI labels on the current Salesforce release (they have shifted across releases).
- Confirm whether the Apex trigger vs Flow invocation is preferable as the default Level 4 recommendation.
