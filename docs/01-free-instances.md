---
title: 1. Provision the Free Instances
---

# 1. Provision the Free Instances

Everything in this lab runs on **free** developer instances. This section gets both standing, with the navigation breadcrumbs you'll reuse throughout.

## 1.1 Salesforce Developer Edition (free)

### Sign up

1. Go to <https://developer.salesforce.com/signup>.
2. Fill in First Name, Last Name, Email, and a unique **Username** (must look like an email, e.g. `yourname.dev@example.com` — it does not have to be a real mailbox).
3. Click **Sign Me Up**.
4. Check your email → click **Verify Account**.
5. Set password + security question.
6. (Recommended) Setup → **My Domain** → register a subdomain. This gives a stable login URL and is required for some OAuth flows.

### What you get

| Capability | Used in this lab |
|------------|------------------|
| Sales Cloud objects (Case, Account, Contact) | Case is the sync target |
| Apex, triggers, Flow | Outbound automation (Level 2/4) |
| REST / SOAP API | Inbound from ServiceNow (Level 4) |
| Named + External Credentials, Connected Apps (OAuth) | Secure outbound auth |
| Platform Events / Change Data Capture | Event-driven (optional) |
| Remote Site Settings | Allowlist ServiceNow URL |

> **Limits:** Developer Edition has limited data storage (~5 MB data / 5 MB files) and a **daily API request limit**. Ample for a PoC, but note the API limit if you plan a load test (Setup → Company Information → API Requests).

### Breadcrumbs (Salesforce)

After login → **Setup** (gear icon) → **Quick Find** box searches everything: Named Credentials, External Credentials, Flows, Object Manager, Remote Site Settings, App Manager, My Domain.

### Verify

- You can log in at `https://<MyDomain>.my.salesforce.com`.
- Setup → Company Information shows edition "Developer Edition" and your Org ID.

---

## 1.2 ServiceNow Personal Developer Instance (PDI)

### Sign up

1. Go to <https://developer.servicenow.com> and sign in (or create a free developer account).
2. Click **Request Instance** (top of the page) or use **Developer Dashboard → Manage → Instance**.
3. Choose a recent release and request it.
4. Wait a few minutes. You receive:
   - An instance URL like `https://devNNNNNN.service-now.com`.
   - Username `admin` + the password you set.
5. **Log in at least once every ~10 days** — an inactive PDI is reclaimed (you can re-request).

### What a PDI includes (relevant to this lab)

| Capability | Used in this lab |
|------------|------------------|
| Full platform (ITSM, CMDB, tables) | Incident table |
| REST API (Table API, Scripted REST API) | Inbound (Level 1/3) |
| REST Message (outbound) + OAuth registry | Outbound (Level 4) |
| Flow Designer + IntegrationHub | Low-code outbound |
| Update Sets | Move config between instances |

> ⚠️ **Verify at review time:** the exact IntegrationHub *spoke* catalog on a PDI varies by release/entitlement. Standard spokes are present; a dedicated **Salesforce spoke** may require a subscription. The lab's custom path (Level 4) needs no spokes, so the PoC is not blocked.

### Breadcrumbs (ServiceNow) — use the **All** filter / Application Navigator

| What | Where |
|------|-------|
| Table API testing | **System Web Services → REST → REST API Explorer** |
| Scripted REST APIs | **System Web Services → Scripted Web Services → Scripted REST APIs** |
| Outbound REST Message | **System Web Services → Outbound → REST Message** |
| Business Rules | **System Definition → Business Rules** |
| OAuth / Application Registry | **Application Registry** (All filter) |
| Incidents | type `incident.list` in the filter, or **Incident → All** |

### Verify

- `https://<your-instance>.service-now.com/` loads and you can log in as `admin`.
- Open **REST API Explorer** to confirm inbound REST is available.

---

## 1.3 Side-by-side comparison

| Dimension | ServiceNow PDI | Salesforce Developer Edition |
|-----------|----------------|------------------------------|
| Signup | developer.servicenow.com | developer.salesforce.com/signup |
| Cost | Free | Free |
| Expiry | ~10 days inactive (reclaimable) | Permanent |
| Inbound API | Table API, Scripted REST, SOAP | REST, SOAP, Bulk, Streaming |
| Outbound tooling | REST Message, Flow Designer, IntegrationHub | Named/External Credentials, Apex, Flow |
| OAuth role | OAuth *client* + *provider* (App Registry) | OAuth *provider* (Connected App) + *client* (Named Cred.) |
| Low-code integration | Flow Designer + spokes | Flow + External Services / Named Credentials |

> **Key asymmetry:** ServiceNow's "Named Credential"-equivalent is a **REST Message + OAuth profile / credential record**; Salesforce's is a **Named Credential**. Both exist so you never hardcode a secret in a script.
