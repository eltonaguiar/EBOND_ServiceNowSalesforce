---
agent: ebond-v2
domain: INTEGRATION
phase: 1
status: done
spans: [WORKFLOWS]
evidence:
  - path: 2026-11-16-SWARM/03_DONE/INTEGRATION/integration_architecture_options.md
  - verified_at: 2026-11-16T20:45:00Z
---

# Pattern C — Integration Hub + Salesforce spoke (low-code)

**Integration Hub** is ServiceNow's low-code integration layer. Spokes provide pre-built actions (e.g. a **Salesforce spoke** with actions like *Create/Update Case, Query Records…*). This is the most "out-of-the-box" way to call Salesforce from ServiceNow flows.

## How it works

- **Spokes** bundle authenticated connections to external systems. A **Connection & Credential alias** holds the Salesforce auth (OAuth client, username/password, or token).
- **Actions** (e.g. `Salesforce: Create Case`) become steps in **Flow Designer** triggers.
- Your flow runs the action with mapped inputs and handles the response.

## Setup

1. **Enable Integration Hub** (your dev instance may include a license/subscription or a trial).
2. **Activate the Salesforce spoke** from the Integration Hub / Store.
3. **Create a Connection & Credential alias** pointing at your SF org (OAuth client credentials or username/password). Keep the credential in the alias, never in code.
4. **Build a Flow**:
   - Trigger: e.g. *Record created* on Incident.
   - Step: *Salesforce — Create Case* action; map Incident fields → Case fields.
   - Step: capture the returned Case `Id` into an Incident field.

## When to prefer this

- Citizen developers / minimal code.
- Reuse across many spokes (ServiceNow already has many prebuilt spokes).
- You want a UI-driven connection setup instead of hand-rolled OAuth in scripts.

## Caveats

- Spoke availability and premium-credential behavior vary by instance/subscription — **verify on your dev instance**.
- You still need a Salesforce Connected App/OAuth setup for the alias.
- Less code, but also less control over custom auth flows and transport edge cases.

## Verify

- [ ] Spoke activation succeeded and the connection alias tests successfully.
- [ ] A Flow using the Salesforce action creates/updates a Case.
- [ ] Field mapping matches `data_model_field_mapping.md`.
