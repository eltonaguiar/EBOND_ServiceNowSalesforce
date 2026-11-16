---
agent: ebond-v2
domain: INSTANCES
phase: 1
status: done
spans: [INTEGRATION]
evidence:
  - url: https://developer.service-now.com
  - url: https://www.servicenow.com/products/developer-program.html
  - path: 2026-11-16-SWARM/evidence/INSTANCES/sn_instance_setup_checklist.md
  - verified_at: 2026-11-16T20:40:00Z
---

# ServiceNow Developer instance setup (free)

This guide provisions a **free personal ServiceNow Developer instance** usable for the integration POC. It costs nothing, includes a full platform UI (including Flow Designer / App Engine Studio), and is the standard way to practice ServiceNow development.

## 1. Create the program account

1. Go to **https://developer.service-now.com** and sign up with a valid email (or sign in if you already have a ServiceNow account).
2. Complete the developer program registration (accept the terms; the program is free for learning and development).
3. After sign-in you land on the developer portal dashboard.

## 2. Request your instance

1. From the portal dashboard choose **Manage / Request instance** (or the "Request an instance" action).
2. Pick an instance type — for this lab **"ServiceNow Developer Instance"** (the standard personal instance) is what you want. Some portals also offer **"Sub-Production"** or size options; the default Developer Instance is sufficient.
3. Select a release/version (choose the latest stable or a version your integration target is compatible with).
4. Click **Create / Request**. Provisioning usually takes a few minutes.

## 3. Instance URL + admin credentials

- Your instance URL looks like: `https://<your-instance>.service-now.com` (e.g. `https://dev123456.service-now.com`).
- The **instance URL**, **admin username** (often `admin`), and **auto-generated password** are shown in the portal (Dashboard → Your instance). Save them in your own secret store — **not** in git.
- You can reset the admin password from the portal at any time.

## 4. What you get (free tier highlights)

| Feature | Availability |
|---------|--------------|
| Full platform UI (lists, forms, navigation) | ✅ |
| **App Engine Studio (AES)** + Flow Designer | ✅ |
| Scripted REST APIs + REST Messages (outbound) | ✅ |
| Tables: Incident, Case, User, etc. | ✅ |
| **Integration Hub** (spokes/actions) | Typically available; spoke availability and premium credentials vary — verify in your instance |
| MID Server (on-prem) | Not needed for cloud-to-cloud (`ServiceNow → Salesforce`) |

## 5. Important lifecycle facts

- **Weekly reset:** free developer instances are often reset on a schedule (commonly weekly, sometimes on request). Re-apply any setup that isn't versioned after a reset.
- **Keep it active:** log into the instance regularly (the portal y can deactivate idle instances).
- Because resets happen, **version all configuration** (update sets, source control, and this repo's docs) so a reset is painless.

## 6. Verify before the integration steps

- [ ] You can log into `https://<instance>.service-now.com` as admin.
- [ ] **REST API Explorer** loads (`/api/now/...` endpoints respond).
- [ ] You can create a record in the **Incident** table (`incident`).
- [ ] (Optional) Integration Hub / Flow Designer opens without errors.

> 💡 Record your instance URL, but **never** commit your admin password. Use a local env file or your secret manager.
