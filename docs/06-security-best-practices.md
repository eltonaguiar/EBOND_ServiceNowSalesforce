---
title: 6. Security & Best Practices
---

# 6. Security & Best Practices

An integration PoC that ignores security teaches the wrong habits. These rules apply on day one — developer instance or not.

## 6.1 Secrets — never in code, never in Git

| ❌ Bad | ✅ Good |
|--------|---------|
| Client secret in an Apex class / Script Include | Salesforce **Named/External Credential** |
| Password in a ServiceNow script | ServiceNow **REST Message + OAuth profile** / **credential record** |
| `.env` or `credentials.json` committed | `.gitignore` (already in this repo) + a secrets store |
| Integration token pasted in a README | Reference "set your own in Setup" instructions |

The repo's `.gitignore` already excludes `.env`, `*.pem`, `credentials.json`, etc. Treat any accidental secret as **compromised** and rotate it.

## 6.2 Authentication: prefer OAuth 2.0 over Basic auth

- **Basic auth** (Levels 1–2) is fine only for the first smoke test; it stores a username/password with no scoping or revocation.
- **OAuth 2.0** (Level 4) — short-lived access tokens + refresh, scoped, revocable — is the production shape.
- ServiceNow side: **Application Registry** is both the OAuth client (outbound to Salesforce) and provider (inbound from Salesforce).
- Salesforce side: **Connected App** (provider) + **Named Credential** (client).

## 6.3 Least privilege

- Create a **dedicated integration user** on each side — never run as `admin` or a full system profile.
  - ServiceNow: minimal role (e.g. `itil` + read on reference tables) for the client-credentials token.
  - Salesforce: "API Only System Integrations" or a minimal custom profile, with access only to `Case` and the fields it touches.
- Scope the OAuth app to only the needed scopes (`api`, `refresh_token`) — never `full`.
- **ACLs on the ServiceNow table** are the real gate for inbound Table API writes; the integration user's roles determine what it can create.

## 6.4 Network & platform guardrails

- **Salesforce Remote Site Settings** must allowlist the ServiceNow instance URL — also your *allowlist* for what Apex can call.
- **Salesforce Permission Set → External Credential principal** mapping is what actually authorizes a Named Credential callout (the Level 2 gotcha).
- **ServiceNow CORS / allowed origins** (browser flows) and the instance's outbound rules govern what the platform will reach.
- Use **TLS/HTTPS** everywhere; both platforms enforce it on public endpoints.

## 6.5 Rate limits & governor limits

| Platform | Limit | Mitigation |
|----------|-------|------------|
| Salesforce | Daily API request limit (org-wide); Apex governor limits (CPU, callouts, DML) | Batch, cache tokens, avoid callouts in loops |
| ServiceNow | REST API rate limits / semaphores; session quotas | Async patterns (`executeAsync`), avoid tight retry loops |
| Both | OAuth token endpoint rate limits | Cache the access token until expiry; refresh only when needed |

## 6.6 Reliability patterns

- **Idempotency & correlation** — the external-ID + origin-check pattern (Level 4 §5.6) prevents duplicates *and* loops.
- **Error handling** — check HTTP status; log the body; surface failures in a queue/retry rather than silently dropping.
- **Retries with backoff** — for transient failures (429/5xx), retry with exponential backoff and a max-attempt cap.
- **Timeouts** — set sane timeouts on both callouts so a hung endpoint doesn't exhaust Apex governor limits or ServiceNow threads.
- **Audit logging** — log correlation ID + remote ID on both sides so any sync state can be traced.

## 6.7 Data & environment hygiene

- **Synthetic data only** — no real customer records in a PDI/Dev org.
- **Treat instances as disposable** — document setup as steps (this lab does) so you can rebuild in minutes.
- **Separate config from code** — ServiceNow: an **Update Set** or source control; Salesforce: source-driven format (scratch org + `sf` CLI) where possible.

## 6.8 Pre-flight security checklist

- [ ] No secret in any code file, README, or commit.
- [ ] OAuth in use (or Basic auth only for the documented Levels 1–2 smoke tests).
- [ ] Dedicated integration users with minimal roles on both sides.
- [ ] Remote Site Settings + Permission Set allowlist configured (Salesforce).
- [ ] Correlation + origin-check loop guard in place.
- [ ] Error handling + logging on both callouts.
- [ ] `.gitignore` present and effective.
