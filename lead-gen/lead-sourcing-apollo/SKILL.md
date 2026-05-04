---
name: lead-sourcing-apollo
description: Source B2B leads from Apollo by translating an ICP scorecard into firmographic and persona filters, quoting cost before pulling, normalizing to the canonical Lead schema, and pushing companies + persons + run-history interactions to the CRM. Use when the user wants to build an outbound list grounded in a defined ICP, has an Apollo seat or API key, has an Apollo CSV export, or has any list to ingest and normalize.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [GTM, Lead-Sourcing, Apollo, Outbound]
    related_skills: [icp-definition, lead-sourcing-clay, lead-sourcing-linkedin, lead-sourcing-web, data-enrichment, lead-scoring]
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
  - name: APOLLO_API_KEY
    prompt: "Apollo API key"
    help: "https://app.apollo.io/settings/integrations"
    required_for: "Apollo API mode sourcing"
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Lead Sourcing — Apollo

Translate a defined ICP into an Apollo search, pull a cost-quoted batch of contacts, normalize to the canonical Lead schema, and push to CRM. Operates in three modes — API, manual export, or BYO CSV — degrading gracefully.

## When to Use

- User wants to build an outbound list grounded in a defined ICP
- User has an Apollo seat or API key and wants to pull contacts
- User has an Apollo CSV export to ingest and normalize
- "Source SDRs at Series B SaaS companies in the US"
- User needs search filters to run manually in Apollo
- User has a BYO list from another CRM to clean up and push

## Quick Reference

| Concept | Value |
|---|---|
| Modes | API (key set) / Manual export (seat, no key) / BYO (any list) |
| Adapter contract | `discover()` → count + cost; `pull()` → records; `normalize()` → Lead schema |
| Quote-before-pull | Mandatory — never `pull()` without `discover()` + user confirm |
| First-batch default | ≤500 records — validate filter quality before expanding |
| Cost cap | `gtm.sourcing_run_usd_cap` (default $25); record cap 2000 |
| Dedup priority | `linkedin_url` > `email` > `phone` (person); `company_domain` (company) |
| Apollo "verified" email | Hint, not verdict — always pair with `data-enrichment` verifier |
| Provenance tags | `[verified: apollo-api]` / `[user-provided]` / `[unverified — needs check]` |
| Compliance | EU → `gdpr_basis: legitimate-interest`; role-addresses → sidecar; DNC → strip |

## Procedure

1. **Confirm ICP grounding.** Read ICP scorecard from `icp-definition`. Extract firmographic, role map, triggers, anti-ICP. If absent → flag ICP-ungrounded, `confidence: low`.
2. **Determine mode.** `APOLLO_API_KEY` set → API. Else seat → manual export. Else any list → BYO. Else → filter recommendations only.
3. **Translate ICP → Apollo filter set.** Map industry → `organization_industries`; size → `organization_num_employees_ranges`; geography → `person_locations`; funding → `organization_latest_funding_stage`; tech → `currently_using_any_of_technology_uids`; titles → `person_titles`; seniority → `person_seniorities`; anti-ICP → `not_organization_*`. Store as reproducible `source_query`.
4. **Pre-flight: discover().** Surface candidate count, estimated USD, sample of 5. Wait for explicit authorization. Never bypass. Reference `${HERMES_SKILL_DIR}/references/` for Apollo filter mapping details.
5. **Pull.** Page through results, respect rate limits (~60 req/min, backoff on 429), cap at `gtm.sourcing_run_record_cap`. Stamp `source_run_id` and `source: apollo-api` on every record.
6. **Normalize.** Map to Lead schema. Tag provenance per field. Construct `personalization_hook` ONLY with citable URL — never invent. Run `${HERMES_SKILL_DIR}/scripts/normalize_lead.py` per record.
7. **Dedup against CRM.** Merge by `linkedin_url` > `email` > `phone` for person; `company_domain` for company. Run `${HERMES_SKILL_DIR}/scripts/dedup_leads.py`. Log every merge.
8. **Apply compliance filters.** EU → `gdpr_basis: legitimate-interest`. Role-address emails → sidecar. DNC phones → strip.
9. **Push to CRM + emit run summary.** Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. Push `company` + `person` + `interaction:research` for verified/user-provided; `interaction:research` only for unverified. Emit one-screen run summary.

## Pitfalls

- Pulling without a quote — always `discover()` first; cost cap is a hard stop
- Trusting Apollo's "verified" email flag — pair with real verifier in `data-enrichment`
- Inventing personalization hooks — hooks ship with citable URLs or they don't ship
- Ignoring company-size-adjusted seniority — "VP" at 50 people ≠ "VP" at 5,000
- Blasting role addresses — `info@`, `sales@` → sidecar, never active push
- Filters too tight then over-loosened — loosen one dimension at a time and re-discover

## Verification

1. `source_query` filter object is reproducible — running it again returns the same candidates ± new entrants
2. Every record carries provenance tags on every named field — no untagged fields
3. Run record's costs match Apollo's billing dashboard ± rounding
4. `[unverified — needs check]` records landed in review queue, not active prospect list
