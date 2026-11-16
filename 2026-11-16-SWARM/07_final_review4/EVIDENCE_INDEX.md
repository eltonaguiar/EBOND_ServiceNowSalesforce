# EVIDENCE_INDEX — ServiceNow ⇄ Salesforce Free Integration Lab

Every material claim and where it is evidenced.

| Claim | Evidence |
|-------|----------|
| ServiceNow Table API is the inbound CRUD API | `docs/02`; `evidence/CROSSCUTTING/sources.json` (HTTP 200) |
| ServiceNow OAuth 2.0 + Application Registry | `docs/05`; `evidence/CROSSCUTTING/sources.json` |
| IntegrationHub is the low-code integration layer | `docs/02`; `evidence/CROSSCUTTING/sources.json` |
| Salesforce Connected App / OAuth | `docs/05`; `evidence/CROSSCUTTING/sources.json` (help.salesforce.com, 200) |
| Salesforce Named Credentials / External Credentials | `docs/03`, `docs/06`; Salesforce docs (browser-ok) |
| Salesforce scratch orgs / Developer Edition | `docs/01`; Salesforce docs (browser-ok) |
| Free PDI lifecycle (~10-day reclaim) | `docs/01` (⚠️ confirm on instance) |
| Loop guard pattern (correlation + origin) | `docs/05` §5.6; code samples |
| TSOM cross-cutting.md exists on `main` (SHA `5f1d54a`) | `03_DONE/DOCS_SITE/v1_tsom_crosscutting_link_plan.md` |
| Pages source is `workflow`/`main`/`/` | GitHub Pages API (recorded in `03_DONE/DOCS_SITE/v1_docs_site.md`) |

## Verification-gap items (tracked for review)

- IntegrationHub Salesforce spoke entitlement on a current PDI (⚠️).
- Salesforce Developer Edition storage + daily API limit (⚠️).
- ServiceNow inbound OAuth grant type on current release (⚠️).

These are consolidated in `docs/08-appendix.md` §8.6 and are the primary targets for the `finalv2` review round.
