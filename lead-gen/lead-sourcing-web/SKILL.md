---
name: lead-sourcing-web
description: Source leads from the open web — job boards, news, press releases, RFPs, podcast guest lists, regulatory filings — by translating ICP triggers into web search queries and scraper jobs, normalizing results to the canonical Lead schema with citation-grade provenance. Use when the buying trigger is text-based, when target accounts are stealth-stage or regional, or when database-only sourcing produces empty firmographics.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [GTM, Lead-Sourcing, Web-Research, Job-Boards, News]
    related_skills: [icp-definition, lead-sourcing-apollo, lead-sourcing-clay, lead-sourcing-linkedin, data-enrichment, lead-scoring, market-research]
    requires_tools: [terminal]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
      - key: gtm.sourcing_run_usd_cap
        description: Max spend per sourcing run
        default: "25"
      - key: gtm.sourcing_run_record_cap
        description: Max records per sourcing run
        default: "2000"
required_environment_variables:
  - name: SERP_API_KEY
    prompt: "SerpAPI key"
    required_for: "Web search sourcing"
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Lead Sourcing — Web

Source leads from the open web by translating ICP trigger criteria into web search queries and scraper jobs. Output: accounts (and sometimes contacts) tagged with citation-grade trigger evidence (permalink + date). Where Apollo and LinkedIn surface databases, this skill surfaces the *event*.

## When to Use

- "Find companies hiring Salesforce admins where the job post mentions migration"
- "Companies that issued an RFP for [topic] in last 90 days"
- "Find Directors of Engineering who appeared on technical podcasts"
- Triggers Apollo can't see — RFPs, press releases, job-post text, regulatory filings
- Target accounts are stealth-stage, regional, or niche-vertical
- Database-only sourcing produces empty firmographics

## Quick Reference

| Concept | Value |
|---|---|
| Modes | API (SerpAPI/CSE/Apify) / Manual (queries-only) / BYO (link list) |
| Citation rule | Every signal carries an `evidence_url` that resolves — no URL, no signal |
| Trigger taxonomy | stack-replacement / funding / leadership-hire / RFP / compliance / podcast-guest / OSS-activity |
| Half-lives | Press: 6mo · Job post: 3mo · Funding: 12mo · RFP: 90d |
| Trigger differentiator | Trigger IS the personalization hook — web-sourced records ship with hooks pre-constructed |
| Boolean precision | Site-restricted queries (`site:linkedin.com/jobs`, `site:sam.gov`) → primary sources |
| Output focus | Companies first, contacts rare — pair with `data-enrichment` / `lead-sourcing-linkedin` |
| Compliance | robots.txt respected; paywall/login-wall not scraped; aggressive same-domain scraping paced |

## Procedure

1. **Confirm ICP grounding.** Read ICP scorecard from `icp-definition`. For each trigger, identify canonical web source per taxonomy. Reference `${HERMES_SKILL_DIR}/references/` for trigger-source mapping.
2. **Determine mode.** Search-API + Apify → API mode. Else partial → mode-mix. Else → query-recipe-only output.
3. **Translate triggers → search queries.** Generate Boolean queries with site restrictions per trigger. Store as reproducible `search_query_set`. Examples: stack-replacement → `site:linkedin.com/jobs "Salesforce admin" ("migrating from" OR "moving off")`; RFP → `site:sam.gov "vendor risk" (after:<date>)`.
4. **Pre-flight: discover().** Run sample query (5–10 results) per trigger. Surface samples with provenance + cost. Wait for explicit authorization.
5. **Execute search batch + extract.** Run queries (API) or instruct user (manual). For each source URL: scrape via Apify; extract company, domain, sometimes contact. Domain resolution falls back to `[unverified — needs check]`.
6. **Normalize to Lead schema.** Map fields per conventions. Stamp `provenance_company: [verified: <source>:<url>]`. Every signal's `evidence_url` is non-negotiable. Construct `personalization_hook` from the trigger source. Run `${HERMES_SKILL_DIR}/scripts/normalize_lead.py`.
7. **Dedup + push + summary.** Dedup on `company_domain` for company-only records. Run `${HERMES_SKILL_DIR}/scripts/dedup_leads.py`. Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. Summary: queries, trigger breakdown, missing-contact report, recommended next skill (`data-enrichment` / `lead-sourcing-linkedin`).

## Pitfalls

- Citing an unresolvable URL — re-check at push time; 404 = drop, not fudge
- Generic queries returning aggregators — restrict by site or use canonical-source whitelists
- Missing the trigger time window — 14-month-old "raised Series B" isn't a trigger
- Pushing accounts without contacts as outreach-ready — pair with `data-enrichment` next
- robots.txt violations — respect them; reputational and legal risk
- Confusing speculation for citation — "likely a buyer" is not a citation; the URL is

## Verification

1. Every record's `signals[].evidence_url` resolves to a page describing the trigger as claimed
2. Every personalization hook's `source_url` matches the signal evidence URL
3. `search_query_set` is reproducible — same queries catch new entrants without rebuild
4. `data-enrichment` and/or `lead-sourcing-linkedin` recommended as follow-ups
5. `[unverified]` records routed to review queue with original URL preserved
