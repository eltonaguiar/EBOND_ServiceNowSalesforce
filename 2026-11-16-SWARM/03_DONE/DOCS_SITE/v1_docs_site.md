---
agent: v1-bond-lab
domain: DOCS_SITE
phase: 1
status: done
spans: [CROSSCUTTING]
evidence:
  - path: .github/workflows/pages.yml
    verified_at: 2026-11-16T20:35:00Z
  - path: _config.yml
    verified_at: 2026-11-16T20:35:00Z
  - path: index.md
    verified_at: 2026-11-16T20:35:00Z
  - url: https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
    verified_at: 2026-11-16T20:35:00Z
---

# DOCS_SITE — GitHub Pages + README

Deliverables: `index.md`, `_config.yml`, `.github/workflows/pages.yml`, root `README.MD`, `docs/00`–`08`.

## What was done

- Wired GitHub Pages via the canonical **GitHub Actions** deploy (`configure-pages` → `jekyll-build-pages` → `upload-pages-artifact` → `deploy-pages`). The repo's Pages source is already `workflow` (branch `main`, path `/`), so this workflow is the deploy path.
- Jekyll config mirrors the proven `ServiceNow_Learning_TSOM` site (`jekyll-theme-minimal` + `jekyll-relative-links` + `jekyll-optional-front-matter`), excluding the SWARM folder and `tools/` from the site.
- Root `README.MD` links the live Pages URL and documents the repo layout and collaboration model.
- Site publishes at https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/ **after merge to `main`**.

## Key decisions / rationale

- **Jekyll + minimal theme** over a heavier docs theme: lowest-risk, consistent with the existing TSOM Pages site, and review-friendly for round 1. A `just-the-docs` upgrade is a candidate for a later round.

## Open items for review

- Decide whether to switch to `just-the-docs` remote theme for a search + nav sidebar in a later round.
