---
agent: ebond-v2
domain: BESTPRACTICES
phase: 1
status: done
spans: [TESTING]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/TESTING/qa_test_plan.md
  - verified_at: 2026-11-16T20:55:00Z
---

# Rate limits, monitoring & logging

## Rate limits

- **Salesforce:** daily API request limits apply (check your org: Settings → Company Information / “API Request” usage). For a DE org keep integration volume low; spread requests; use Composite/Bulk endpoints when batching on larger volumes.
- **ServiceNow:** the platform enforces per-minute/per-user API thresholds. Keep outbound call volume modest and add retry-on-429.
- Always read the `Retry-After`/`RateLimit-*` headers if present and honor them.

## Monitoring

- **ServiceNow:** watch instance diagnostics (API usage, flow error counts). Log flow failures to a custom error table for visibility.
- **Salesforce:** use Setup → System Overview / usage dashboards; inspect flow runs (Flow Debug), Apex logs, and the debug log for callouts.
- Cross-check the **error queue** (see reliability doc) as the single source of truth for failed integrations.

## Logging

- Log: timestamp, direction, correlation key, endpoint, HTTP status, latency, retry count.
- **Redact** Authorization headers and any tokens.
- Use structured log lines (JSON) where easy to parse.
- Keep logs out of git; store in the platform or a scratch log location.

## Alerting (POC-level)

- A simple scheduled flow/job that counts recent error-queue rows and flags if > 0 for X minutes.
- Optional: surface a simple “integration health” panel on the lab site (see `03_DONE/PAGES/`).
