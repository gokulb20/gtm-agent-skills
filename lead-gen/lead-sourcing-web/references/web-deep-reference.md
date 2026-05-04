# Lead Sourcing — Web: Deep Reference

## Trigger Taxonomy and Canonical Sources

| Trigger | Canonical Sources | Search Pattern |
|---|---|---|
| Stack-replacement (job-post text) | LinkedIn Jobs, Indeed, Glassdoor, Greenhouse | `site:linkedin.com/jobs "Salesforce admin" ("migrating from" OR "moving off")` |
| Funding announcement | Crunchbase News, TechCrunch, official press release | `"Series B" "raised" (after:<date>)` |
| Leadership hire | LinkedIn, company blog, news | Cross to `lead-sourcing-linkedin` for primary |
| RFP issuance | sam.gov, bidnetdirect.com, industry aggregators | `site:sam.gov "vendor risk" (after:<date>)` |
| Compliance / regulatory | EDGAR (US), Companies House (UK) | `site:sec.gov "..."` |
| Podcast guest | Listen Notes, Spotify | `"<name>" "<topic>" site:listennotes.com` |
| OSS activity | GitHub API | REST API queries |
| Conference speaker | Conference websites | `"<name>" "<event>" site:<conf-domain>` |
| Layoff | layoffs.fyi, WARN filings, news | `"<company>" layoff (after:<date>)` |

## Three-Mode Degradation

### API Mode
`SERP_API_KEY` or `GOOGLE_CSE_API_KEY` set + Apify subscription. Run queries programmatically, scrape result pages. Provenance: `[verified: serpapi:<url>]` or `[verified: apify-page-scraper:<url>]`.

### Manual Mode
No search API keys. Skill outputs reproducible search queries with site-restrictions and Boolean operators. User runs queries, drops result URLs back. Skill ingests via BYO mode.

### BYO Mode
User has hand-curated URL list. Skill visits each via Apify, extracts company + signal.

## Worked Example (Fictional — All Entities `[hypothetical]`)

**Product:** ComplianceCove [hypothetical]
**ICP:** Regulated industries, 200–10,000 emp, US; trigger: RFP for vendor risk management

**Search queries:**
```yaml
- trigger: rfp-issuance
  query: '"Request for Proposal" ("vendor risk management" OR "TPRM") (after:2026-02-04)'
  source: serpapi
- trigger: rfp-issuance
  query: 'site:sam.gov "vendor risk" (after:2026-02-04)'
  source: serpapi
- trigger: rfp-issuance
  query: 'site:bidnetdirect.com "TPRM" (after:2026-02-04)'
  source: serpapi
```

**Results:** 38 source URLs → 32 companies extracted → 30 pushed (5 dedup; 4 review-queue ambiguous domain; 2 dropped 404).
**Trigger breakdown:** 32 rfp_issuance.
**Missing contacts:** 30/30 (typical for web-sourcing).
**Personalization hook example:** "Mercer-Lake Bank [hypothetical] issued an RFP for Vendor Risk Management Platform on 2026-04-15, deadline 2026-06-01."

## Push-to-CRM Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-web #icp-tier-pending #trigger-<type>"`, `relevance` includes trigger evidence URL |
| Each unique person (rare) | `person` | `contactName`, `contactTitle`, `contactLinkedIn` |
| Trigger evidence per record | `interaction` (research) | `relevance` = trigger detail + source URL + date; `tags: "#trigger-<type> #function-2"` |
| Run record | `interaction` (research) | `relevance` = run summary; `tags: "#web-sourcing-run #function-2"` |
| Paywalled/404'd/ambiguous | `interaction` (research) ONLY | `tags: "#unverified #review-required #lead-sourcing-web"` |

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Full push; every signal has citation URL |
| `[unverified — needs check]` | Only `interaction:research`; source URL preserved but no company/person |
| `[hypothetical]` | Never push |

## Compliance and Ethics

- robots.txt respected — abort if violation detected mid-run
- Paywall/login-wall: capture title + snippet from search excerpt only; never scrape past paywall
- Aggressive same-domain scraping: pace requests to avoid IP blocks
- Government procurement (sam.gov, EDGAR): public records, fair game
- Multi-language sources: capture verbatim + English summary; preserve original URL
