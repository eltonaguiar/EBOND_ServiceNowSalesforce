---
agent: v1-bond-lab
domain: INSTANCE_SETUP
phase: 1
status: done
spans: [DOCS_SITE]
evidence:
  - path: docs/01-free-instances.md
    verified_at: 2026-11-16T20:30:00Z
  - url: https://developer.servicenow.com
    verified_at: 2026-11-16T20:30:00Z
  - url: https://developer.salesforce.com/signup
    verified_at: 2026-11-16T20:30:00Z
  - path: 2026-11-16-SWARM/evidence/CROSSCUTTING/sources.json
    verified_at: 2026-11-16T20:30:00Z
---

# INSTANCE_SETUP — free instance provisioning

Deliverable: `docs/01-free-instances.md`.

## What was done

- Documented ServiceNow **PDI** signup, what it includes (Table API, Flow Designer, IntegrationHub, OAuth registry, update sets), and its ~10-day inactivity reclaim lifecycle.
- Documented the three free Salesforce paths — **Developer Edition**, **Trailhead Playground**, **Scratch org** — with a recommendation (Developer Edition for a stable PoC) and a comparison table.
- Added a side-by-side platform comparison and the key "Named Credential asymmetry" note.

## Key decisions / rationale

- **Developer Edition over scratch org**: permanent and full-featured, so the PoC survives across sessions; scratch orgs are the better fit only for source-driven CI/CD, noted for later rounds.
- **"Verify at review time" flags**: IntegrationHub spoke entitlement, Salesforce daily API limits, and OAuth grant types are release-dependent and are explicitly marked ⚠️ rather than asserted.

## Open items for review

- Confirm the current PDI IntegrationHub spoke catalog.
- Confirm the current Salesforce Developer Edition daily API request limit.
