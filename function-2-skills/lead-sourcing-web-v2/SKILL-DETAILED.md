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

Source leads from the open web — job boards, news, press releases, RFPs, podcast guest lists, regulatory filings, GitHub orgs — by translating ICP trigger criteria into web search queries and scraper jobs. The output is a list of accounts (and sometimes contacts) tagged with the trigger evidence (permalink + date) that prompted their inclusion. Where Apollo and LinkedIn surface stable databases, this skill surfaces the *event* — the specific public artifact that says a company is in-market right now.

> *The worked example uses a fictional product (ComplianceCove) for illustration. The trigger taxonomy, search-query patterns, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Lead schema, source adapter contract, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`. This skill assumes it.*

## Purpose

Most database-driven sourcing skills (Apollo, Clay, Sales Nav) miss triggers that live in unstructured text — a job post requiring "Salesforce admin (we're migrating off HubSpot)" reveals stack-replacement intent that no firmographic database tags; an RFP for "vendor risk management platform" published on a procurement portal is the strongest possible buying signal but invisible to LinkedIn; a podcast appearance by a Director of Engineering discussing a pain point is high-value personalization grounding nobody else surfaces. This skill operationalizes that hunt: build precise web queries, scrape source pages, extract company + (sometimes) contact + the citation that justifies inclusion. Every record ships with a citation URL or it doesn't ship.

## When to Use

- "Find companies hiring Salesforce admins in last 30 days where the job post mentions migration."
- "Companies that issued an RFP for [topic] in last 90 days."
- "Show me companies that issued a press release about expansion in the last 60 days."
- "Find Directors of Engineering who appeared as guests on technical podcasts about Kubernetes."
- "Crunchbase, AngelList, Product Hunt — find stealth-stage SaaS companies in our ICP."
- "GitHub orgs of size N+ that recently published code in language X."
- Triggers Apollo can't see; stealth-stage / regional / niche-vertical companies database tools undercount.

### Do NOT use this skill when

- The play is firmographic-stable; database-driven sourcing (`lead-sourcing-apollo`, `lead-sourcing-clay`) is cheaper and more complete.
- The trigger is role-based (recent hires, leadership change) — `lead-sourcing-linkedin` (Sales Nav surfaces these directly).
- The user wants 1,000+ records — web scraping at that scale is slow, expensive, and legally fraught. Database sourcing first.
- The query is purely about contact discovery, not trigger discovery — `data-enrichment` (Hunter, Clearbit) is the right tool.
- No SerpAPI / Google CSE / Bing API key AND no scraper service AND no BYO list — the skill can produce *queries* but cannot fetch results.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | ICP scorecard | yes (or flag ungrounded) | `icp-definition-v2` output | Trigger library is the primary input from ICP. |
| 2 | Search infrastructure | one of: SerpAPI / Google CSE / Bing News API / Apify scrapers / BYO link list | env or user input | Determines mode. |
| 3 | Trigger criteria + source priorities | yes | user / ICP | "Job posts mentioning 'Salesforce' migration" / "RFPs in industry X" / "Series A press releases" / "GitHub orgs in language Y." |
| 4 | Cost budget | yes (default `SOURCING_RUN_USD_CAP=$25`) | env or user | SerpAPI ~$0.005/query; Apify scrapers vary; Google CSE 100 free/day then $5/1000. |
| 5 | Run purpose tag | yes | user | Stamped on every record's `source_run_id`. |
| 6 | Time-window override (optional) | no | user | "Last 30 days only" — narrower windows reduce noise but may miss slower-moving signals. |

### Fallback intake script

> "Web sourcing finds companies via the trigger that prompts inclusion — a job post, a press release, an RFP, a podcast appearance. Three modes:
> - API mode: I run SerpAPI / Google CSE / Bing / Apify queries directly.
> - Manual mode: I produce reproducible search queries you run; you give me the result URLs.
> - BYO mode: you have a list of source URLs (job posts, news links); I extract company + contact from each.
>
> What trigger are we hunting? (job-post text, press release, RFP, podcast guest, GitHub activity, regulatory filing, other?) And the time window — last 30/60/90 days?
>
> Cost cap (default $25)?"

### Input validation rules

- ICP firmographic absent → `confidence: low`; default provenance `[unverified — needs check]`; flag run as ICP-ungrounded.
- No search-API key AND no scraper AND no BYO list → produce search queries only; refuse to fabricate result URLs.
- Trigger criteria empty → block; this skill is trigger-driven by definition. Without a trigger, route to `lead-sourcing-apollo` for firmographic search.
- Time-window > 12 months on a press/news trigger → warn; trigger half-life is 6–12 months max.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Trigger Events for Sales Success** (2009) | Craig Elias | The intellectual core: timing-based events drive prioritization. Web sources expand the trigger taxonomy beyond what databases tag (job-post text, RFP issuance, podcast appearance, regulatory filing). |
| **Job-post-as-tech-stack-revealer** (industry-standard) | n/a — convention since Stack Overflow developer survey culture, ~2008 | A company hiring a "Salesforce admin (Pardot experience required)" reveals their stack more reliably than a tech-detection tool. House extension: parse for "migration," "replacing," "moving off" keywords as displacement signals. |
| **News-driven outreach** (industry-standard) | n/a | Press release / news mention is a publicly-disclosed change of state — the highest-quality basis for an outreach personalization hook. The skill captures the article URL + date as the citation. |
| **Citation-grade provenance** (house-built) | Crewm8 | Every web-sourced record ships with the source URL it came from. No URL = no record. This is the trigger-skill version of the function-2 anti-fabrication contract. |

## Tools and Sources

### Search APIs

| Tool | Purpose | Cost (typical) |
|---|---|---|
| SerpAPI | Google search at scale, news vertical | $0.005/query |
| Google Custom Search Engine | Cheaper Google search, lower volume | 100 free/day, then $5/1000 |
| Bing News Search API | News-specific search, sometimes catches what Google misses | ~$3/1000 |

### Scraper / structured-source tools

| Tool | Purpose |
|---|---|
| Apify (job board scrapers, Crunchbase, etc.) | Pre-built scrapers per source |
| Custom scrapers (cheerio / Playwright) | When Apify doesn't have a pre-built; user-managed |
| RSS feeds | Cheap, high-quality for press releases / blog posts |
| GitHub API | Org / repo discovery |
| EDGAR / SEC filings | US public-company regulatory filings |

### Manual / BYO sources

| Source | Notes |
|---|---|
| Hand-curated link list | User has 200 URLs; skill extracts company + signal from each. |
| Boolean keyword strategy | User runs queries themselves, drops result URLs back. |

### Source priority rule

For trigger evidence: **direct primary source (job board, official press release, RFP portal) within last 90 days** > **news article citing the trigger within 90 days** > **secondary aggregator (Indeed, Glassdoor) citing the trigger** > **agent inference (`[unverified — needs check]`)**. NEVER cite a URL that doesn't resolve. NEVER paraphrase a trigger without preserving the source URL.

### Trigger taxonomy + canonical sources

| Trigger | Canonical sources |
|---|---|
| Stack-replacement (job-post text) | LinkedIn Jobs, Indeed, Glassdoor, BuiltIn, Greenhouse JSON feeds |
| Funding announcement | Crunchbase News, TechCrunch, FT, official press release |
| Leadership hire | LinkedIn (cross to `lead-sourcing-linkedin`), company blog, news |
| RFP issuance | Government procurement portals (FBO, sam.gov), industry-specific RFP aggregators |
| Compliance / regulatory filing | EDGAR (US), Companies House (UK), industry regulators |
| Podcast guest | Podcast directories, Listen Notes, Spotify search |
| Open-source activity | GitHub API, OSS Insights |
| Conference speaker | Conference websites, scraped programs |
| Layoff announcement | layoffs.fyi, news, WARN filings (US) |

## Procedure

### 1. Confirm ICP grounding

Read ICP scorecard from `icp-definition`. Trigger library is the key input — for each ICP trigger, identify its canonical web source(s) per the taxonomy above. **Rationale**: web sourcing is trigger-led, not firmographic-led; without trigger criteria, this skill has nothing to do.

### 2. Determine mode

Search-API key set + Apify subscription → API mode. Else partial → API for available, manual for unavailable. Else nothing → query-and-recipe-only output. **Rationale**: web sources fragment more than databases; mode-mixing is normal.

### 3. Translate trigger criteria → search queries

For each trigger, generate Boolean query strings tuned to the canonical source. Examples:
- Stack-replacement: `site:linkedin.com/jobs "Salesforce admin" ("migrating from" OR "moving off" OR "replacing")`
- Funding: `"Series B" "raised" filetype:html (after:2026-02-04)` (90-day window)
- RFP: `"Request for Proposal" "vendor risk management" filetype:pdf (last 90 days)`
- Podcast guest: `"Director of Engineering" "Kubernetes" site:listennotes.com`

Store queries as reproducible `search_query_set`. **Rationale**: queries are the audit handle; they're more durable than the result list.

### 4. Pre-flight: discover()

Run a sample query (5–10 results) for each trigger to validate signal-to-noise; report sample to user with provenance tags. Surface combined query count and estimated cost:

```
3 trigger queries × ~30 results each = ~90 source URLs.
SerpAPI cost: 90 × $0.005 = $0.45.
Apify scraper for company-page extraction: 90 × $0.01 = $0.90.
Sample of 5 results per trigger: [list with [verified: serpapi] tags]
Proceed?
```

### 5. Execute search batch

Run queries (API mode) or instruct user (manual). Capture per-result: source URL, source date, snippet, the trigger that matched. **Rationale**: the per-result metadata is the citation provenance.

### 6. Extract company + (sometimes) contact

For each source URL: visit / scrape (per source-specific scraper); extract company name, company domain, location, sometimes a contact (job-post poster, press-release contact, podcast host). Domain resolution from company name uses a deterministic rule (homepage scrape → about page → "/contact" page) and falls back to `[unverified — needs check]` when ambiguous. **Rationale**: web sourcing produces accounts first, contacts second; cold-email skill will pair with `data-enrichment` for contact-finding.

### 7. Normalize to Lead schema

For each extracted record:
- Map company fields per conventions §1.
- Stamp `provenance_company: [verified: <source>:<url>]`.
- For triggers, the `signals` entry's `evidence_url` is the trigger source URL — non-negotiable; no URL → no signal.
- For person fields: `[verified]` only when extracted directly (job-post poster name + LinkedIn); else NULL.
- Construct `personalization_hook` directly from the trigger source — this is THE differentiator: the trigger IS the hook.

**Rationale**: web sourcing's value is hook-rich records; this is the one sourcing skill that pre-populates personalization hooks from the source itself.

### 8. Dedup against existing CRM

Same priority as Apollo: `linkedin_url` > `email` > `phone` for person; `company_domain` for company. Web sourcing typically produces only company-level records; dedup-on-company is the common case.

### 9. Push + emit run summary

Push per §9. Run summary highlights: queries run, sources matched, trigger breakdown (per-trigger result counts), missing-contact-fields report (records with company but no contact — typical for web), recommended next skill (`data-enrichment` to find contacts at the discovered companies, then `lead-sourcing-linkedin` for fresh role data, then `lead-scoring`).

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: <api | manual | byo>
  search_query_set:
    - trigger: stack-replacement
      query: "site:linkedin.com/jobs ..."
      source: serpapi
    - trigger: rfp-issuance
      query: "..."
      source: serpapi
  cost:
    serpapi_usd: <float>
    apify_usd: <float>
    total_usd: <float>
    cap_usd: <float>
  matched_sources_count: <int>
  pulled_count: <int>
  pushed_count:
    company: <int>
    person: <int>
    interaction_research: <int>
    review_queue: <int>
  trigger_breakdown:
    stack_replacement: <int>
    rfp_issuance: <int>
    funding_announcement: <int>
    leadership_hire: <int>
    podcast_guest: <int>
    other: <int>
  missing_contact_fields: <int>   # companies with no contact discovered
  warnings: [<string>]
  next_skill_recommendation: data-enrichment | lead-sourcing-linkedin | lead-scoring

leads:
  - lead_id: <uuid>
    company: <[verified: <source>]>
    company_domain: <[verified: <source>] or [unverified — needs check]>
    company_size_band: <[verified: <source>] if scraped from about-page>
    contact_name: <typically null for web-sourcing>
    email: null
    email_status: unverified
    signals:
      - type: stack-replacement | rfp-issuance | funding-announcement | ...
        source: <serpapi-news | linkedin-jobs | crunchbase | ...>
        date: <ISO from source>
        evidence_url: <permalink — REQUIRED>
        strength: strong | medium | weak
        half_life_days: <per trigger taxonomy>
        detail: <verbatim or one-sentence summary from source>
    personalization_hook:
      text: <constructed from the trigger source itself>
      source_url: <same as signal evidence_url>
      source_date: <same>
      provenance: [verified: <source>]
    source: web-search-batch | apify-job-scraper | byo-link-list
    source_run_id: <run_id>
    freshness_date: <ISO>
```

## Worked Example

> *All entities below are tagged `[hypothetical]` — fictional, illustrative.*

**User prompt**: "Find companies that issued RFPs for vendor risk management in last 90 days. We're pitching ComplianceCove [hypothetical]. SerpAPI configured. $15 budget."

**Step 1 — ICP grounding**: ComplianceCove ICP from `icp-definition`:
- Firmographic: regulated industries (FinServ, Healthcare, Government), 200–10,000 emp, US.
- Roles: Buyer = CISO / VP Security / Director of Vendor Management; Champion = Security Operations Manager.
- Trigger: RFP issuance for vendor risk management (high-strength) — primary; SOC2 audit cycle approaching (medium); recent compliance-officer hire (medium).
- Anti-ICP: <50 emp; non-US; consultancies that themselves do vendor risk for others.

**Step 2 — Mode**: SerpAPI configured → API mode for primary trigger; Apify generic-page-scraper for company extraction.

**Step 3 — Search queries**:
```yaml
- trigger: rfp-issuance
  query: '"Request for Proposal" ("vendor risk management" OR "third-party risk management" OR "TPRM") (after:2026-02-04)'
  source: serpapi
- trigger: rfp-issuance
  query: 'site:sam.gov "vendor risk" (after:2026-02-04)'
  source: serpapi
- trigger: rfp-issuance (industry-specific aggregator)
  query: 'site:bidnetdirect.com "TPRM" (after:2026-02-04)'
  source: serpapi
```

**Step 4 — discover()**:
> "3 queries × sample of 5 each → 15 results. ~38 unique source URLs estimated for full run.
> SerpAPI: ~$0.20. Apify page extraction: ~$0.40. Total: ~$0.60. Sample:
> - [Mercer-Lake Bank [hypothetical] RFP for TPRM — sam.gov, dated 2026-04-15] [verified: serpapi]
> - [Avalon Health Systems [hypothetical] RFP for vendor-risk platform — corporate procurement portal, 2026-03-22] [verified: serpapi]
> ...
> Proceed full run?"

User: "Yes."

**Step 5 — Execute search batch**: 3 queries return 38 unique source URLs (after dedup of result-overlap).

**Step 6 — Extract company + contact**: Apify generic-page-scraper visits each URL. Of 38:
- 32 → company name + domain extracted cleanly.
- 4 → company name extracted but domain ambiguous (multiple candidates) → `[unverified — needs check]`.
- 2 → page no longer accessible (404 / paywall) → drop.

For one record:
```yaml
company: "Mercer-Lake Bank" [hypothetical]
company_domain: "mercerlakebank.com"
company_size_band: "1001-5000"   # extracted from about-page
company_industry_normalized: "banking / financial services"
company_location: "Charlotte, NC, US"
provenance_company: [verified: serpapi]
provenance_domain: [verified: apify-page-scraper]
contact_name: null
email: null
signals:
  - type: rfp-issuance
    source: sam.gov
    detail: "Issued RFP 'Vendor Risk Management Platform' on 2026-04-15. Submission deadline 2026-06-01."
    date: 2026-04-15 [verified: serpapi]
    evidence_url: "https://sam.gov/opp/abc123/view" [hypothetical]
    strength: strong
    half_life_days: 90
personalization_hook:
  text: "Mercer-Lake Bank [hypothetical] issued an RFP for a Vendor Risk Management Platform on 2026-04-15 with a 2026-06-01 submission deadline."
  source_url: "https://sam.gov/opp/abc123/view"
  source_date: 2026-04-15
  provenance: [verified: serpapi]
source: web-search-batch
source_run_id: web_2026-05-04_rfp1
freshness_date: 2026-05-04
```

**Step 7 — Dedup**: 5 collisions against existing CRM (all on `company_domain`); 3 keep-existing, 2 enrich-existing.

**Step 8 — Compliance**: 0 EU; sam.gov sources are US-government public records — no privacy concerns.

**Step 9 — Push + summary**:
```
ComplianceCove Web Sourcing Run [hypothetical]
Run ID: web_2026-05-04_rfp1
Mode: API. Sources: SerpAPI + Apify page scraper
Queries: 3 (TPRM RFP, sam.gov, bidnetdirect.com)
Cost: $0.58 / cap $15
Matched sources: 38 → Extracted: 32 → Pushed: 30 (5 dedup; 4 routed to review-queue for ambiguous domain; 2 dropped 404)
  Companies: 30 (28 new, 2 enriched)
  Persons: 0 (no contacts in RFP source pages — typical)
  Interaction:research: 1 (run record) + 32 (per-record trigger evidence) + 4 review-queue
Trigger breakdown:
  rfp_issuance: 32 (all matched)
Missing-contact-fields: 30/30 (web-sourcing produces accounts; contacts are downstream)
Recommended next: data-enrichment OR lead-sourcing-linkedin (find CISO / VP Security at each company)
```

## Heuristics

- **The trigger IS the hook.** Web-sourced records ship with personalization hooks already constructed from the source. This is the differentiator vs Apollo/Sales Nav.
- **Citation > volume.** Better to ship 30 cited records than 300 noisy ones. Web sourcing is precision-first.
- **Source URL must resolve at push time.** A 404'd URL on a record headed to outreach embarrasses the sender. Re-check before push.
- **Trigger half-life applies even more here.** A press release from 6 months ago looks "fresh" in search results but is operationally stale.
- **Boolean precision matters.** Generic queries return aggregator-spam; site-restricted Boolean queries return signal. Always restrict to canonical sources.
- **Job-post text reveals more than tech-detection.** "Migrating from Hubspot to Salesforce" in a job description is ironclad; BuiltWith says only what's currently installed.
- **RFP triggers are the sharpest in the trigger taxonomy.** A company *announcing* it wants to buy is the strongest possible signal — but coverage is regional/industry-specific.
- **Podcast guest signal is underrated.** A Director of Engineering speaking about Kubernetes for 45 minutes is a fully-mined personalization gold mine; cost is one Listen Notes search.
- **Web sourcing has higher null-contact rate.** Plan for `data-enrichment` to follow at the company → contact step; account-list-as-deliverable is normal here.
- **Don't fight aggregator noise.** If a query returns mostly Indeed-aggregator hits, rewrite the query to skip Indeed (`-site:indeed.com`) and target the original posters.

## Edge Cases

- **No ICP defined.** Flag ungrounded; produce search queries only.
- **Trigger criteria too generic** ("find SaaS companies"). Block; require specific trigger (event + time window). Suggest moving to `lead-sourcing-apollo` for firmographic-only plays.
- **API key absent for primary search source.** Fall back to manual mode (output queries for user to run); never silently fabricate URLs.
- **Source URL behind paywall.** Capture title + snippet from search excerpt; tag `[unverified — needs check]` for fields the paywall hides; route to review queue.
- **Source URL country-blocked.** Same handling as paywall; surface for user to fetch from compliant region.
- **Multi-language source page.** Capture verbatim text + agent-translated one-sentence summary; preserve original-language URL.
- **Stale URL (404).** Drop the record from active push; preserve as `interaction:research` for audit; never silently fill the gap.
- **Aggregator-only results.** Rewrite queries to exclude major aggregators; if no primary sources found, surface this and recommend trigger expansion or different source.
- **Government-procurement triggers without US scope.** sam.gov is US-only; UK = contractsfinder.service.gov.uk; EU = ted.europa.eu. Apply geography-aware source mapping.
- **GitHub-org sourcing.** Returns orgs not contacts; recommend pairing with `lead-sourcing-linkedin` for "Director of Engineering at [org]" enrichment.
- **News article citing a trigger but no clear company.** Drop; some news writes "an unnamed buyer" — not actionable.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| SerpAPI auth fails (401) | "Invalid API key" | Confirm key; do NOT retry silently. |
| SerpAPI rate limit (429) | "Too many requests" | Backoff; resume from last query. |
| Apify scraper fails on a URL | "Page extraction error" | Retry once; mark record `[unverified — needs check]` for the affected fields; preserve source URL. |
| URL 404 at extraction time | Stale link | Drop record; preserve URL in `interaction:research` for audit. |
| Paywall / login wall | empty extraction | Capture title + snippet from search; tag affected fields `[unverified — needs check]`; route to review. |
| Country-block | scraper returns "access denied" | Surface; recommend regional fetch or different source. |
| Aggregator-spam dominant | run quality poor | Rewrite queries to exclude major aggregators; rerun. |
| Cost cap mid-run | partial pull | Stop; persist what was extracted; offer raise-cap or partial-accept. |
| BYO link list with mixed-quality URLs | partial extraction | Flag URLs that failed; offer per-failure recovery (re-fetch, manual fill). |
| robots.txt forbids scraping | scraper aborts | Respect robots.txt — skip that source; surface; recommend manual fetch. |
| Multi-language source extraction fails | parser unable | Capture raw text; flag `[unverified — needs check]`; route to review for human translation. |

## Pitfalls

- **Citing an unresolvable URL.** Re-check at push time; 404 = drop, not fudge.
- **Generic queries returning aggregators.** Always restrict by site or use canonical-source whitelists.
- **Treating job-post text as ground truth.** A job post saying "Salesforce migration" is a strong signal; a job post saying "we use Salesforce" is just stack-detection (worse than BuiltWith).
- **Missing the trigger time window.** A 14-month-old "raised Series B" press release isn't a trigger.
- **Pushing accounts without contacts as if they were ready for outreach.** Web sourcing produces the company-level signal; contact discovery is `data-enrichment` / `lead-sourcing-linkedin` next.
- **robots.txt violations.** Respect them. Reputational and legal risk.
- **Confusing speculation for citation.** "Likely a buyer because..." is not a citation. The citation is the URL.
- **Over-broad time window.** Wider windows multiply noise; default 90 days for press, 30 days for job posts.
- **Skipping per-source-domain rate limits.** Aggressive scraping of a single domain gets the IP blocked; pace and respect.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, source URLs, dates, signal evidence) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No search-API at runtime → produce queries only, refuse to fabricate result URLs. NEVER cite a URL that doesn't resolve. NEVER paraphrase a trigger without preserving the source URL.
- **Silent search overspend.** SerpAPI + Apify costs add up across triggers; cap is hard stop.

## Verification

The run is real when: (a) every record's `signals[].evidence_url` resolves to a page describing the trigger as claimed; (b) every personalization hook's `source_url` is the same URL as the signal evidence (or a tighter sub-page); (c) the `search_query_set` is reproducible — running the same queries 30 days later catches new entrants without rebuild; (d) `data-enrichment` and/or `lead-sourcing-linkedin` are recommended as follow-ups for contact discovery; (e) `[unverified]` records (paywalled, 404'd, ambiguous) routed to review queue with the original URL preserved.

Negative test: pick 5 records from the run output. Click each `evidence_url`. If any 404, paywall-block, or describe an unrelated event, the extraction step is broken.

## Done Criteria

1. Mode determined and stated; search queries reproducible.
2. `discover()` sample shown; user authorization received before full run.
3. Every Lead carries citation-grade provenance — every signal has an `evidence_url` that resolves.
4. Personalization hook constructed from trigger source (web-sourcing's differentiator).
5. Dedup performed; `company_domain` is primary merge key for company-only records.
6. Compliance: robots.txt respected; paywalled/blocked sources routed to review.
7. `[unverified — needs check]` records routed to review queue with source URL preserved.
8. Run summary one-screen with trigger breakdown and missing-contact report; recommends `data-enrichment` or `lead-sourcing-linkedin` as follow-up.

## Eval Cases

### Case 1 — full API mode, RFP trigger

Input: ICP grounded; SerpAPI + Apify keys; "RFPs for vendor risk management in last 90 days"; $15 cap.

Expected: 30–50 source URLs matched; 80%+ extracted with company + domain; 100% have signal `evidence_url`; 0 contacts (typical); recommends `data-enrichment` to find CISOs at each company.

### Case 2 — manual mode, queries-only

Input: ICP grounded; no SerpAPI key; user has Google Search.

Expected: skill outputs reproducible search queries with site-restrictions and Boolean operators; user runs queries themselves, drops result URLs back; skill ingests via BYO mode; same provenance discipline.

### Case 3 — BYO link list

Input: user has 50 hand-curated URLs from a press-release feed; ICP grounded.

Expected: skill visits each URL via Apify; extracts company + signal per record; preserves original URL as evidence; 5–10 records may need review-queue routing for paywalls or extraction failures.

### Case 4 — aggregator-noise rewrite

Input: first-pass query returns 60% Indeed/Glassdoor aggregator hits.

Expected: skill detects aggregator-dominance, rewrites query with `-site:indeed.com -site:glassdoor.com` exclusions, re-runs; second pass produces signal-rich primary-source results. Cost-aware — only re-runs the affected query, not the full set.

## Guardrails

### Provenance (anti-fabrication)

Per §8 of conventions: every record's signal carries an `evidence_url`. No URL = no signal. The `personalization_hook` MUST share the same source URL as the signal it was constructed from. `[unverified — needs check]` for paywalled or extraction-failed records — the URL is preserved but field-level data is flagged. Worked-example fictional entities tagged inline.

### Evidence

Every signal has source name, ISO date, permalink, strength label, half-life. The skill is citation-grade by design.

### Scope

Sources accounts (and sometimes contacts) from the open web. Does NOT verify emails, score, or write outreach. Pairs with `data-enrichment` for contact-finding and `lead-sourcing-linkedin` for fresh role data at discovered companies.

### Framing

Run summary uses operational language. Trigger breakdown highlights signal-source distribution.

### Bias

Web sources over-index on US/EU English-language content. International coverage requires regional-source mapping; surface coverage gaps explicitly.

### Ethics

Respect robots.txt. Public records (gov procurement, EDGAR) are fair game; paywalled / login-walled content is NOT scraped — captured only via search-snippet excerpts or skipped. Aggressive same-domain scraping = pace.

### Freshness

Trigger half-life enforced (per ICP trigger library). Old trigger URLs are stale facts, not signals; skill warns when time-window pushes past trigger half-life.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Companies discovered, contacts missing | `data-enrichment` (contact discovery + verifier) | Lead records (company_domain-keyed) + ICP role map |
| Discovered companies, need fresh leadership data | `lead-sourcing-linkedin` (Sales Nav at each company) | Company list + ICP role map |
| Trigger play also needs firmographic baseline | `lead-sourcing-apollo` (cross-reference) | Company list + Apollo filter set |
| Multi-source orchestration desired | `lead-sourcing-clay` | Same trigger criteria + ICP |
| ICP not grounded | `icp-definition` | Hypothesis + product description |
| Discovered records ready to score | `lead-scoring` (after enrichment) | Enriched records + ICP scorecard |
| Trigger query produced 0 results | `market-research` (re-evaluate signal availability) | Query set + 0-result evidence |

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
    "relevance": "Web sourcing run web_2026-05-04_rfp1. Mode: API (SerpAPI + Apify). Queries: 3 (TPRM RFP general, sam.gov, bidnetdirect.com). Cost: $0.58 / cap $15. Matched sources: 38 → Extracted: 32 → Pushed: 30 (5 dedup; 4 review-queue for ambiguous domain; 2 dropped 404). Trigger breakdown: 32 rfp_issuance. Missing-contact-fields: 30/30 (typical for web). Recommended next: data-enrichment (for contacts) OR lead-sourcing-linkedin (for fresh leadership data at discovered companies).",
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
