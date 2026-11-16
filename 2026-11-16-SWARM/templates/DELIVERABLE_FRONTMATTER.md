# Deliverable front-matter template

Copy the block below to the top of every `03_DONE/<DOMAIN>/` deliverable file.

```yaml
---
agent: ebond-v2
domain: <DOMAIN>            # one of swarm_domains.txt (uppercase)
phase: 1
status: done                # done | in_progress | blocked
spans: []                  # other domains if cross-cutting
evidence:
  - path: <repo-relative path>
  - sha: <commit SHA, optional>
  - url: <live URL, optional>
  - verified_at: <UTC ISO timestamp>
---
```

Notes:
- `domain` must match a domain in `swarm_domains.txt`.
- Evidence may be a path, URL, SHA, or pasted query+result. Never cite /tmp paths; keep small redacted evidence in the SWARM `evidence/<DOMAIN>/` folder.
- No secrets, `.env`, or full dumps.
