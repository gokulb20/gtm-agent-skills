---
name: lead-sourcing-web
description: Source leads from the open web — job boards, news, press releases, RFPs, podcast guest lists, regulatory filings — by translating ICP triggers (often invisible to Apollo / LinkedIn) into web search queries and scraper jobs, normalizing results to the function-2 Lead schema with citation-grade provenance. Use when the buying trigger is text-based (job-post wording, press announcements, RFP issuance, court filings), when target accounts are stealth-stage or regional, or when database-only sourcing produces empty firmographics.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, lead-sourcing, web-research, job-boards, news, function-2]
related_skills:
  - icp-definition
  - lead-sourcing-apollo
  - lead-sourcing-clay
  - lead-sourcing-linkedin
  - data-enrichment
  - lead-scoring
  - market-research
inputs_required:
  - icp-scorecard-from-icp-definition
  - serp-or-cse-api-key-or-byo-source-list
  - trigger-criteria-and-source-priorities
  - cost-budget-credits-or-dollar
  - run-purpose-tag
deliverables:
  - normalized-lead-records-with-citation-provenance
  - search-query-set-reproducible
  - trigger-evidence-permalinks
  - missing-contact-fields-report
  - sourcing-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Lead Sourcing — Web

Source leads from the open web — job boards, news, press releases, RFPs, podcast guest lists, regulatory filings, GitHub orgs — by translating ICP trigger criteria into web search queries and scraper jobs. Output: a list of accounts (and sometimes contacts) tagged with the trigger evidence (permalink + date) that prompted inclusion. Where Apollo and LinkedIn surface stable databases, this skill surfaces the *event*.

> *Worked example uses ComplianceCove [hypothetical] (fictional); procedure is vertical-agnostic. Shared rules in `function-2-skills/function-2-conventions.md`.*

## Purpose

Database-driven sourcing (Apollo, Clay, Sales Nav) misses triggers that live in unstructured text — a job post requiring "Salesforce admin (we're migrating off HubSpot)" reveals stack-replacement intent; an RFP for "vendor risk management platform" is the strongest possible buying signal but invisible to LinkedIn; a podcast guest discussing a pain is high-value personalization grounding. This skill operationalizes that hunt: build precise web queries, scrape source pages, extract company + (sometimes) contact + the citation that justifies inclusion. Every record ships with a citation URL or it doesn't ship.

## When to Use

- "Find companies hiring Salesforce admins where the job post mentions migration."
- "Companies that issued an RFP for [topic] in last 90 days."
- "Companies that issued a press release about expansion in the last 60 days."
- "Find Directors of Engineering who appeared as guests on technical podcasts."
- "Crunchbase, AngelList, Product Hunt — find stealth-stage SaaS companies."
- "GitHub orgs of size N+ that recently published code in language X."
- Triggers Apollo can't see; stealth-stage / regional / niche-vertical companies database tools undercount.

## Inputs Required

1. **ICP scorecard** from `icp-definition`. Trigger library is the primary input.
2. **Search infrastructure** — one of: `SERPAPI_KEY` / `GOOGLE_CSE_API_KEY` + `GOOGLE_CSE_CX` / Bing News API / Apify scrapers / BYO link list.
3. **Trigger criteria + source priorities** — "job posts mentioning 'Salesforce' migration" / "RFPs in industry X" / "Series A press releases" / "GitHub orgs in language Y."
4. **Cost budget** — default `SOURCING_RUN_USD_CAP=$25`. Agent reads vendor docs at runtime; pricing changes — verify live before any spend.
5. **Run purpose tag** — short string for cost attribution + replay.
6. (Optional) Time-window override (default 90d for press, 30d for job posts).

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | API (SerpAPI/CSE/Apify) / Manual (queries-only) / BYO (link list) |
| **Citation rule** | Every signal carries an `evidence_url` that resolves. No URL → no signal. |
| **Trigger taxonomy** | stack-replacement / funding / leadership-hire / RFP / compliance / podcast-guest / OSS-activity / conference-speaker / layoff |
| **Half-lives** | Press: 6mo · Job post: 3mo · Funding: 12mo · RFP: 90d (until submission deadline) · Podcast: 12mo |
| **Trigger differentiator** | Trigger IS the personalization hook — web-sourced records ship with hooks pre-constructed |
| **Boolean precision** | Site-restricted queries (`site:linkedin.com/jobs`, `site:sam.gov`) → primary sources; unrestricted → aggregator-spam |
| **Cost (typical run)** | Agent reads vendor docs at runtime; pricing changes — verify live before any spend. |
| **Output focus** | Companies first, contacts rare — pair with `data-enrichment` / `lead-sourcing-linkedin` |
| **Compliance** | robots.txt respected; paywall/login-wall not scraped (search snippet only); aggressive same-domain scraping paced |

## Procedure

### 1. Confirm ICP grounding
Read ICP scorecard from `icp-definition`. For each ICP trigger, identify canonical web source per taxonomy. If absent → flag ungrounded.

### 2. Determine mode
Search-API + Apify → API mode. Else partial → mode-mix (API for available, manual for unavailable). Else nothing → query-recipe-only output.

### 3. Translate trigger criteria → search queries
Per trigger, generate Boolean queries with site restrictions:
- Stack-replacement: `site:linkedin.com/jobs "Salesforce admin" ("migrating from" OR "moving off")`
- Funding: `"Series B" "raised" filetype:html (after:<date>)`
- RFP: `"Request for Proposal" "<topic>" filetype:pdf (last 90d)`
- Podcast: `"<title>" "<topic>" site:listennotes.com`

Store as reproducible `search_query_set`.

### 4. Pre-flight: discover()
Run sample query (5–10 results) per trigger. Surface samples with provenance tags + cost estimate. Wait for explicit authorization.

### 5. Execute search batch + extract
Run queries (API) or instruct user (manual). For each source URL: scrape via Apify; extract company name, domain, location, sometimes a contact. Domain resolution: homepage → about → contact pages; falls back to `[unverified — needs check]` when ambiguous.

### 6. Normalize to Lead schema
Map fields per conventions §1. Stamp `provenance_company: [verified: <source>:<url>]`. Every signal's `evidence_url` is the trigger source URL — non-negotiable. Construct `personalization_hook` directly from the trigger source (the trigger IS the hook).

### 7. Dedup + push + run summary
Per conventions §6 dedup (`company_domain` primary for company-only records); per §9 push. Run summary: queries, sources matched, **trigger breakdown**, missing-contact-fields report, recommended next skill (`data-enrichment` / `lead-sourcing-linkedin` / `lead-scoring`).

## Output Format

- Reproducible `search_query_set`
- Lead records (citation-grade signals; hook constructed from trigger source)
- Run record: queries, cost, candidate count, dedup log, trigger breakdown, missing-contact report, next-skill recommendation
- Trigger evidence interactions (one per record's signal — preserves the citation URL in CRM)
- Review queue: paywalled / 404'd / ambiguous-domain records as `interaction:research`

## Done Criteria

1. Mode determined; search queries reproducible.
2. `discover()` sample shown; user authorization received before full run.
3. Every Lead carries citation-grade provenance — every signal has an `evidence_url` that resolves.
4. Personalization hook constructed from trigger source (web-sourcing's differentiator).
5. Dedup performed; `company_domain` is primary merge key for company-only records.
6. Compliance: robots.txt respected; paywalled/blocked sources to review queue.
7. `[unverified — needs check]` records routed to review queue with source URL preserved.
8. Run summary one-screen with trigger breakdown + missing-contact report; recommends follow-up skill; cost stayed under cap.

## Pitfalls

- **Citing an unresolvable URL.** Re-check at push time; 404 = drop, not fudge.
- **Generic queries returning aggregators.** Always restrict by site or use canonical-source whitelists.
- **Treating job-post text as ground truth.** "Migrating from X" is a strong signal; "we use X" is just stack-detection.
- **Missing the trigger time window.** A 14-month-old "raised Series B" press release isn't a trigger.
- **Pushing accounts without contacts as if ready for outreach.** Web sourcing is account-first; pair with `data-enrichment` next.
- **robots.txt violations.** Respect them. Reputational and legal risk.
- **Confusing speculation for citation.** "Likely a buyer because..." is not a citation. The URL is.
- **Over-broad time window.** Wider windows multiply noise; default 90 days for press, 30 days for job posts.
- **Skipping per-domain rate limits.** Aggressive same-domain scraping gets IP-blocked.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, source URLs, dates, signal evidence) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No search-API at runtime → produce queries only, refuse to fabricate result URLs. NEVER cite a URL that doesn't resolve. NEVER paraphrase a trigger without preserving the source URL.
- **Silent search overspend.** Cap is hard stop.

## Verification

The run is real when: every record's `signals[].evidence_url` resolves to a page describing the trigger as claimed; every personalization hook's `source_url` is the same URL as the signal evidence; the `search_query_set` is reproducible — running the same queries 30 days later catches new entrants without rebuild; `data-enrichment` and/or `lead-sourcing-linkedin` are recommended as follow-ups for contact discovery; `[unverified]` records (paywalled, 404'd, ambiguous) routed to review queue with the original URL preserved. Negative test: pick 5 records, click each `evidence_url`. If any 404 or describe an unrelated event, extraction is broken.

## Example

**User prompt:** "Find companies that issued RFPs for vendor risk management in last 90 days. We're pitching ComplianceCove [hypothetical]. SerpAPI configured. $15 [hypothetical] budget."
**What should happen:** Read ICP. Generate 3 [hypothetical] queries (TPRM RFP general, sam.gov, bidnetdirect.com). Sample (5 [hypothetical] each, 15 [hypothetical] total) returns clean RFP signals. Confirm. Run full → 38 [hypothetical] source URLs after dedup. Apify extracts 32 [hypothetical] companies (4 [hypothetical] ambiguous-domain to review, 2 [hypothetical] dropped 404). Push 30 [hypothetical] companies + 32 [hypothetical] trigger-evidence interactions + 1 [hypothetical] run record + 4 [hypothetical] review-queue items. Trigger breakdown: 32 [hypothetical] rfp_issuance. Missing-contact: 30 [hypothetical]/30 [hypothetical]. Recommend `data-enrichment` (find CISO at each) OR `lead-sourcing-linkedin` (fresh role data).

**User prompt:** "I have a list of 50 [hypothetical] hand-curated press-release URLs. Extract companies and signals."
**What should happen:** BYO mode. Apify visits each URL; extracts company + domain + the press-release detail. 5 [hypothetical] URLs return 404 (preserved in run record), 3 [hypothetical] are paywalled (search-snippet only, routed to review). Push 42 [hypothetical] companies + 42 [hypothetical] trigger-evidence interactions + 1 [hypothetical] run + 8 [hypothetical] review-queue. Recommend `data-enrichment` for contact discovery.

**User prompt:** "Find SaaS companies hiring Salesforce admins where the job post mentions migration off HubSpot."
**What should happen:** Generate query: `site:linkedin.com/jobs "Salesforce admin" ("migrating from HubSpot" OR "replacing HubSpot" OR "moving off HubSpot")` (90-day window). Sample returns 8 [hypothetical] results — clean. Run full → 26 [hypothetical] job posts. Extract company + posting date + the migration phrasing as the hook. Push 24 [hypothetical] companies + trigger interactions + 1 [hypothetical] run record. Hook examples: *"Hiring Salesforce admin with experience migrating off HubSpot — posted 2026-04-22 [hypothetical] on LinkedIn Jobs."* Recommend `data-enrichment` for the IT Director / RevOps Manager at each.

## Linked Skills

- Companies discovered, contacts missing → `data-enrichment`
- Fresh leadership data at discovered companies → `lead-sourcing-linkedin` (Sales Nav per company)
- Firmographic cross-reference → `lead-sourcing-apollo`
- Multi-source orchestration → `lead-sourcing-clay`
- ICP not grounded → `icp-definition`; Records ready to score → `lead-scoring`
- Trigger query produced 0 results → `market-research`

## Push to CRM

After extracting and normalizing, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company in pull | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-web #icp-tier-pending #trigger-<type>"`, `relevance` includes the trigger evidence URL |
| Each unique person (rare for web) | `person` | `contactName`, `contactTitle`, `contactLinkedIn` (when extracted from source page) |
| Trigger evidence per record | `interaction` (type: `research`) | `relevance` = trigger detail + source URL + date; `tags: "#trigger-<type> #function-2"` |
| Run record (queries, cost, breakdown) | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#web-sourcing-run #function-2"` |
| Paywalled / 404'd / ambiguous records | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #lead-sourcing-web"`; never `company`/`person` |

`lead-scoring` writes `score` + `priority` + tier tags onto person records later — but for web-sourcing, scoring usually happens at the company level until contact discovery completes.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
SERPAPI_KEY=   # or GOOGLE_CSE_API_KEY + GOOGLE_CSE_CX
APIFY_API_KEY=
SOURCING_RUN_USD_CAP=25
SOURCING_RUN_RECORD_CAP=2000
```

### Source tag

`source: "skill:lead-sourcing-web:v2.0.0"`

### Example push (verified company + trigger evidence)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Mercer-Lake Bank",
    "website": "https://mercerlakebank.com",
    "industry": "Banking / Financial Services",
    "tags": "#sourced-web #icp-tier-pending #trigger-rfp-issuance #financial-services",
    "relevance": "Sourced from web-sourcing run web_2026-05-04_rfp1. Trigger: RFP for Vendor Risk Management Platform issued 2026-04-15 (sam.gov/opp/abc123/view), submission deadline 2026-06-01. Provenance: company [verified: serpapi], domain [verified: apify-page-scraper]. Signal strength: strong. Hook: same RFP. Recommend data-enrichment to find CISO / VP Security contacts.",
    "source": "skill:lead-sourcing-web:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#web-sourcing-run #function-2",
    "relevance": "Web sourcing run web_2026-05-04_rfp1. Mode: API (SerpAPI + Apify). Queries: 3 (TPRM RFP general, sam.gov, bidnetdirect.com). Cost: $0.58 / cap $15. Matched sources: 38 → Extracted: 32 → Pushed: 30 (5 dedup; 4 review-queue for ambiguous domain; 2 dropped 404). Trigger breakdown: 32 rfp_issuance. Missing-contact-fields: 30/30 (typical for web). Recommended next: data-enrichment OR lead-sourcing-linkedin.",
    "source": "skill:lead-sourcing-web:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §8.2:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping. Every signal has its citation URL preserved. |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #lead-sourcing-web` tags. Source URL preserved but no `company` / `person` push. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified push (paywalled source):

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #lead-sourcing-web #paywall",
    "relevance": "Trigger evidence behind paywall: https://wsj.com/example-rfp-article-2026 [unverified — needs check]. Search snippet suggests Acme Corp issued RFP for vendor-risk platform 2026-04-09, but full text inaccessible. Recommend manual fetch from compliant region or alternate source.",
    "source": "skill:lead-sourcing-web:v2.0.0"
  }'
```

### When NOT to push

- Run that returned 0 source URLs — push run record, no person/company.
- All sources paywalled/blocked — push as `interaction:research` for review queue; no person/company.
- 404'd or extraction-failed records — preserve URL in run record but don't fabricate company info.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
- Run flagged "ICP-ungrounded" — push run record tagged `#icp-ungrounded`; defer person/company push.
- robots.txt violation detected mid-run — abort; surface; never push records from violated source.
