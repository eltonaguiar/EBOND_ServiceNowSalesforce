---
agent: ebond-v2
domain: INSTANCES
phase: 1
status: done
spans: [INTEGRATION]
evidence:
  - url: https://developer.salesforce.com/signup
  - url: https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm&type=5
  - path: 2026-11-16-SWARM/evidence/INSTANCES/sf_org_setup_checklist.md
  - verified_at: 2026-11-16T20:40:00Z
---

# Salesforce Developer org setup (free)

This guide provisions a **free Salesforce Developer Edition (DE) org** — the sandbox-friendly, API-enabled environment for building and testing the integration POC.

## 1. Sign up

1. Go to **https://developer.salesforce.com/signup** and fill the form.
2. Use a **real, unique email** (you'll confirm by email) and a username that looks like an email (Salesforce usernames are email-formatted).
3. Complete the CAPTCHA and submit.

## 2. Verify email + set password

1. Check your inbox for the confirmation email and click the link.
2. Set a password. Your **username** is the email-formatted value you chose; your password is what you just set.
3. You may be asked to verify your identity via a code — complete it.

## 3. Log in to your DE org

- Login URL: **https://login.salesforce.com**
- Enter your username (email-formatted) + password → **Log In**.
- Your DE org has a `my.salesforce.com` / `.lightning.force.com` URL (e.g. `https://mycompany-dev-ed.my.salesforce.com`).

## 4. What you get (Developer Edition highlights)

| Feature | Availability |
|---------|--------------|
| **Lightning Platform** + Flow builder | ✅ |
| **Connect App** (for API/OAuth) | ✅ |
| REST & SOAP APIs (Salesforce & Salesforce) | ✅ |
| **Named Credentials** (for outbound callouts) | ✅ |
| Standard objects: Case, Account, Contact, User | ✅ |
| **Dev Hub** (for scratch orgs) | ✅ (some DE orgs enable this) |
| Salesforce CLI (`sf`) | Local tool; works against DE orgs |

## 5. Lifecycle facts

- **Idle expiry:** DE orgs can be deactivated after a period of inactivity (historically ~7 days). Log in periodically to keep it active and "reactivate" if needed.
- **Limits:** DE orgs have daily API request and storage limits. Check **Setup → Company Information** (or the "API Request" usage panel) for the current numbers. Keep integration traffic modest for a POC.
- **Trial/permissions:** some features require enabling permissions — enable them in Setup when the integration needs them.

## 6. Verify before integration steps

- [ ] You can log into `login.salesforce.com` with your username/password.
- [ ] **Setup → App Manager** opens.
- [ ] You can create a **Case** record.
- [ ] (Recommended) Install **Salesforce CLI** (`sf`) and connect it to your org for versioned source control:
  `sf org login web --alias myDevOrg` (or device/username flows).

## Breadcrumbs (Setup → Quick Find)

- Named Credentials → **Named Credentials** (with **External Credentials** tab)
- Flows → **Flows**
- Connected App → **App Manager** (or Setup → App Manager)
- Object/fields → **Object Manager**
- Limits/usage → Setup → **Company Information** (API Request usage)

> 💡 Never commit your password, security token, or connected-app secrets. Use Named Credentials / env vars as described in the best-practices docs.
