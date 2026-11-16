```yaml
---
agent: <worktree name>          # required
domain: DB | GHACTIONS | AUDIT | PREDICTION | CROSSCUTTING | <declared via swarm_domains.txt>
phase: 1                        # 1=scout drop, 2=first review, 3=second pass, 4=synthesis, 5=final plan
status: done | in_progress | blocked
spans: [AUDIT, GHACTIONS]       # optional; only when CROSSCUTTING
evidence:                       # required for status: done
  - path: audit_dashboard/data/db_health.json
    sha: db4cc06ed82
    verified_at: 2026-11-16T06:00:00Z
  - url: https://findtorontoevents.ca/audit/data/dashboard_data.json
    verified_at: 2026-11-16T06:00:00Z
---
```

Rules:
- `evidence.path` is repo-relative to `eltonaguiar/findtorontoevents_antigravity.ca` unless a `repo:` key says otherwise.
- `verified_at` must be within 24h for live-URL evidence at plan-approval time.
- Raw logs/JSON excerpts go in the top-level `evidence/<DOMAIN>/` folder (≤256 KB each, redacted), not in `/tmp` and not inline in the deliverable body.
- Free-form prose below the front-matter; machines only read the block above.
