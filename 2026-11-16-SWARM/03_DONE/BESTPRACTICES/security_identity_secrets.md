---
agent: ebond-v2
domain: BESTPRACTICES
phase: 1
status: done
spans: [INSTANCES]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INSTANCES/lab_environment_and_credentials.md
  - verified_at: 2026-11-16T20:55:00Z
---

# Security, identity & secrets

Foundational rules for the integration POC and any production-shaped version.

## Identity & least privilege

- Use **integration/service accounts** with the minimum permission to read/write the synced objects — never a full admin in production.
- On ServiceNow grant the integration user REST API access and `incident` read/create/update at most.
- On Salesforce grant the integration user CRUD on `Case` (and the correlation fields) plus access to the Connected App only.

## Secrets

- **Never commit** passwords, OAuth client secrets, security tokens, or keys (see `lab_environment_and_credentials.md`).
- Use ServiceNow **Connection & Credential aliases** (Integration Hub) or credential records for outbound auth.
- Use Salesforce **Named Credentials** for callouts so credentials live in the named credential object, not in code.
- For local scripts, read secrets from a gitignored `.env` / OS keychain.
- Rotate the Connected App secret if it ever appears in a commit or log (and scrub git history).

## Network / API hygiene

- Use **HTTPS** everywhere; only the official platform endpoints.
- Bind Connected App OAuth scopes to what the integration needs (e.g. `api` + refresh).
- Consider restricting the integration user's profile/permissionsets rather than using the admin profile.

## Auditing

- Turn on API/flow logging for the integration user in dev.
- Keep an error/retry table (see reliability doc) that is auditable.
- Never log full bodies that contain tokens; redact `Authorization` headers.

## Reference

- ServiceNow credentials: platform **Connection & Credential aliases**.
- Salesforce: **Named Credentials** + **Connected App** OAuth.
- See enforcement `2026-11-16-SWARM/03_DONE/BESTPRACTICES/reliability_retries_idempotency.md` and `rate_limits_monitoring_logging.md`.
