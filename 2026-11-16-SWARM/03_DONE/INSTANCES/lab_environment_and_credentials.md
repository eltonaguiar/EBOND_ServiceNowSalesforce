---
agent: ebond-v2
domain: INSTANCES
phase: 1
status: done
spans: [BESTPRACTICES]
evidence:
  - path: 2026-11-16-SWARM/evidence/INSTANCES/lab_env_vars_template.md
  - verified_at: 2026-11-16T20:40:00Z
---

# Lab environment & credential handling

This note standardizes how the lab stores and uses secrets so nothing sensitive is committed to git.

## What to keep (non-secret) in the repo

- Instance/org URLs (e.g. `https://dev123456.service-now.com`, `https://mycompany-dev-ed.my.salesforce.com`)
- Usernames and **integration user/service account names**
- API version references, field/API names (e.g. `Case`, `Incident`, `Subject`, `Short_description`)

## What must never go into git

- Passwords, security tokens, OAuth client secrets, private keys.
- Live API keys / session tokens.
- `.env` files, `credentials.json`, or DB dumps.

## Local secret storage

- Keep secrets in a local `.env` file (gitignored) or your OS secret manager.
- Example `.env` (gitignored) for the lab scripts:

```bash
# ServiceNow
SN_INSTANCE_URL=https://dev123456.service-now.com
SN_ADMIN_USER=admin
SN_ADMIN_PASSWORD=***

# Salesforce
SF_USERNAME=you@example.com
SF_PASSWORD=***
SF_OAUTH_CLIENT_ID=3MVG...
SF_OAUTH_CLIENT_SECRET=***
```

Replace each `***` with the real secret from your local secret manager; never commit populated values.

## Platform-native secret handling (preferred for production-shaped flows)

- **ServiceNow:** use **Connection & Credential aliases** (Integration Hub) or a credential record; reference the alias in REST messages/flows rather than hard-coding.
- **Salesforce:** use **Named Credentials** for outbound callouts (store the auth info inside the named credential), or a connected app with OAuth client-credentials/refresh flow.

## Reference

- `.gitignore` at repo root ignores `.env`, `*.pem`, `credentials*.json`, etc.
- Scripts read env vars via `os.environ` / a small loader; they never read secrets from repo files.
