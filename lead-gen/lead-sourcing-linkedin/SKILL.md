---
name: lead-sourcing-linkedin
description: Source leads via LinkedIn Sales Navigator by translating role-based and trigger-based ICP criteria into Sales Nav search URLs and filter recipes, executing via session-based tools or manual CSV export, and normalizing to the canonical Lead schema with strict ToS compliance. Use when the play is role/trigger-driven, when Sales Nav surfaces signals Apollo can't see, or when LinkedIn URL is required as the dedup key.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [GTM, Lead-Sourcing, LinkedIn, Sales-Navigator]
    related_skills: [icp-definition, lead-sourcing-apollo, lead-sourcing-clay, lead-sourcing-web, data-enrichment, lead-scoring]
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
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Lead Sourcing — LinkedIn

Source leads via Sales Navigator's role- and trigger-based search filters with strict ToS compliance. Emit search URLs + filter recipes, execute via session-based tools (PhantomBuster, HeyReach) or manual CSV export, normalize to the Lead schema. LinkedIn URL is the primary person dedup key. Direct scraping is refused.

## When to Use

- "Find VPs who started their current role in the last 90 days"
- User wants role/trigger-driven plays — leadership shifts, recent hires, active LinkedIn presence
- Sales Nav surfaces signals Apollo can't see (fresh role changes, posts)
- User has a Sales Nav seat and needs search filters
- User exported Sales Nav CSV and wants it ingested
- LinkedIn URL is required as the primary dedup key

## Quick Reference

| Concept | Value |
|---|---|
| Modes | API-substitute (PhantomBuster/HeyReach) / Manual (Sales Nav UI) / BYO (CSV) |
| Direct scraping | REFUSED — forbidden by LinkedIn ToS, hard rule |
| Primary merge key | `linkedin_url` — highest-confidence in this skill |
| Sales Nav UI cap | 25 leads/page; 1,000 results per search |
| Trigger filters | "Years in Current Position <1 year", "Posted on LinkedIn past 30d", "Changed jobs past 90d" |
| Email coverage | Sales Nav rarely surfaces email — `data-enrichment` mandatory next |
| PhantomBuster pacing | 50–100 profiles/day per session is safe |
| Compliance | Public-profile content only; session-based tools acceptable; direct-scraping refused |

## Procedure

1. **Confirm ICP grounding.** Read ICP scorecard from `icp-definition`. Extract role map and trigger library. If absent → flag ungrounded.
2. **Determine mode.** Sales Nav seat + PhantomBuster/HeyReach key → API-substitute. Else seat alone → manual (output URL). Else CSV → BYO. Else → URL + recipe only. Direct-scraping requested → REFUSE.
3. **Translate ICP → Sales Nav filter set.** Map titles → `Title` (Boolean); seniority → `Seniority Level`; function → `Function`; geography → `Geography`; trigger-recency → `Years in Current Position <1 year`; active-poster → `Spotlights: Posted on LinkedIn past 30d`. Output: search URL + recipe. Reference `${HERMES_SKILL_DIR}/references/` for Sales Nav filter patterns.
4. **Pre-flight: discover().** Small-batch PhantomBuster job (50 profiles) or user reports UI count. Surface count, cost, sample of 5. Wait for explicit authorization.
5. **Execute.** API-substitute: submit Phantom, collect CSV. Manual: user runs search, exports. BYO: user uploads CSV.
6. **Normalize to Lead schema.** LinkedIn URL is primary identity. Stamp provenance: `[verified: linkedin-sales-nav]` for native fields; `[user-provided]` for BYO. Email typically absent → tag `unverified`. Run `${HERMES_SKILL_DIR}/scripts/normalize_lead.py`.
7. **Dedup + compliance + push.** `linkedin_url` doubled in priority as merge key. Run `${HERMES_SKILL_DIR}/scripts/dedup_leads.py`. GDPR EU tagging; ToS reminder in run record. Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. Summary recommends `data-enrichment` MANDATORY next.

## Pitfalls

- Direct LinkedIn scraping — forbidden by ToS; account-suspension and legal risk; REFUSE
- Skipping `data-enrichment` — LinkedIn rarely provides email; outreach without enrichment will bounce
- Promoting Sales Nav recency past freshness — "started 5 days ago" may be 5 weeks ago in reality
- Inventing LinkedIn URLs — profile URLs are predictable but fabricating them is forbidden
- Ignoring session-safety — aggressive PhantomBuster usage flags accounts; pace 50–100/day
- Mistaking "LinkedIn Member" privacy-mode profiles as skip-able — surface count, don't suppress

## Verification

1. `sales_nav_search_url` resolves to the same filter set on replay
2. Every record's LinkedIn URL is canonical (`/in/<handle>`, no tracking params)
3. Provenance tags accurately reflect source path (Sales Nav vs PhantomBuster vs BYO)
4. `data-enrichment` is recommended before any outreach run
5. Privacy-mode and partial profiles routed to review queue
