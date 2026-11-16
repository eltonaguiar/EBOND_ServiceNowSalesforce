# TESTING_PLAN — Round 1 validation

Validates the lab content (not a live integration, which runs on the free instances).

## Static validation

- [ ] `python3 tools/swarm/swarm_librarian.py validate --dir 2026-11-16-SWARM` exits 0.
- [ ] `swarm_librarian.py index` regenerates INDEX.md.
- [ ] All `03_DONE` files have front-matter; evidence tokens resolve.
- [ ] Secret scan: `grep -rEn "(api[_-]?key|secret|password|token)[=:].{8,}"` finds none in committed files.

## Functional (per the lab's own QA plan)

- [ ] Setup guides are copy-able to a fresh SN/SF instance.
- [ ] Pattern steps reference the right endpoints/auth flows.
- [ ] Field mapping is consistent across pattern docs and the POC walkthrough.

## Site

- [ ] Pages workflow runs green on push to `main`.
- [ ] Live URL loads and links work.
- [ ] README contains the live URL.

## Exit criteria

Validator exits 0; no secrets; site live; all checks above pass.
