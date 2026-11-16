---
agent: v1-bond-lab
domain: SECURITY
phase: 1
status: done
spans: [CUSTOM_INTEGRATION]
evidence:
  - path: docs/06-security-best-practices.md
    verified_at: 2026-11-16T20:35:00Z
  - url: https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm
    verified_at: 2026-11-16T20:35:00Z
  - url: https://docs.servicenow.com/bundle/washingtondc-platform-security/page/administer/security/concept/oauth-2-0.html
    verified_at: 2026-11-16T20:35:00Z
---

# SECURITY — best practices

Deliverable: `docs/06-security-best-practices.md`.

## What was done

- Secrets: never in code/Git; `.gitignore` covers `.env`, `*.pem`, `credentials.json`.
- Auth: prefer OAuth 2.0 over Basic auth; Basic auth scoped to the documented Levels 1–2 smoke tests.
- Least privilege: dedicated integration users + minimal OAuth scopes on both sides.
- Guardrails: Remote Site Settings + Permission Set→principal mapping (Salesforce); ACLs + CORS (ServiceNow).
- Rate/governor limits with mitigations (cache tokens, batch, async).
- Reliability: idempotency, error handling, backoff retries, timeouts, audit logging.
- A pre-flight security checklist (reused as the QA gate).

## Key decisions / rationale

- The **Permission Set → External Credential principal** mapping is listed as a first-class guardrail, not a footnote — it is the most common silent-failure point for Salesforce callouts.

## Open items for review

- Confirm the ServiceNow inbound OAuth grant type (client credentials vs password) on current releases.
