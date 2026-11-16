---
agent: ebond-v2
domain: PAGES
phase: 1
status: done
spans: [BESTPRACTICES]
evidence:
  - path: .github/workflows/gh-pages.yml
  - path: site/index.html
  - url: https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/
  - verified_at: 2026-11-16T21:00:00Z
---

# GitHub Pages deployment

The repo's GitHub Pages site publishes the lab landing page from the `site/` folder.

## How it works

- Pages is configured with **build type = workflow**, source `main`, root path `/`.
- The workflow `.github/workflows/gh-pages.yml` runs on push to `main`:
  1. checks out the repo,
  2. packages the `site/` directory as a Pages artifact,
  3. deploys with `actions/deploy-pages`.

## Site contents

- `site/index.html` — landing page linking to the lab docs in the repo.
- Assets live in `site/` (could be expanded with CSS/JS later).

## Updating the site

1. Edit files under `site/` (or docs under `2026-11-16-SWARM/`).
2. Commit + push to `main`.
3. The Pages workflow deploys automatically; confirm the run is green.

## Live URL

- **https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/**

## Health check

- [ ] After a push, the Actions run succeeds and the site renders.
- [ ] The URL in `README.md` matches the live site.
