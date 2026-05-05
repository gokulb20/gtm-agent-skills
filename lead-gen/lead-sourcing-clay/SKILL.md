---
name: lead-sourcing-clay
description: Source leads via Clay's table-based orchestration of Apollo, Hunter, Clearbit, and other data providers in a single workflow, with cost-aware multi-source chaining, dedup, and provenance tagging. Use when the user has a Clay seat or API key and wants multi-provider results in one pull, when single-source skills miss fields Clay can fill in-flow, or when a Clay table already exists and needs to push to CRM.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [GTM, Lead-Sourcing, Clay, Orchestration]
    related_skills: [icp-definition, lead-sourcing-apollo, lead-sourcing-linkedin, lead-sourcing-web, data-enrichment, lead-scoring]
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

# Lead Sourcing — Clay

Use Clay's table-based orchestration to combine multiple data providers (Apollo for firmographic search, Hunter for emails, BuiltWith for tech, MillionVerifier for deliverability) in a single workflow. Output: normalized, multi-source-provenance-tagged Lead records — same schema as `lead-sourcing-apollo` but with enrichment baked in.

## When to Use

- User has Clay and wants Apollo + email-finder + tech-stack + verifier in one pull
- "Build me a Clay table for our ICP"
- Single-source skill misses fields Clay can fill in-flow
- User has an existing Clay table CSV to push to CRM
- Multi-source orchestration when the cost model favors Clay over direct-API

## Quick Reference

| Concept | Value |
|---|---|
| Modes | API (key set) / Manual (Clay seat, output spec) / BYO (table CSV) |
| Default chain | Apollo (search) → Hunter (email) → BuiltWith (tech) → MillionVerifier (verifier) |
| Per-row cost | Scales linearly per row × per column; always quote per-provider before pull |
| Free re-run window | ~24h on same row × column (Clay caching) |
| Provenance | Each Clay column emits its own provenance per row — flatten only at push time |
| Source priority (overlapping fields) | Verifier-checked > Hunter pattern guess > Apollo claim |
| Replay handle | `clay_table_id` — preserve in run record for 30-day refresh |

## Procedure

1. **Confirm ICP grounding.** Read ICP scorecard from `icp-definition`. If absent → flag ungrounded, `confidence: low`.
2. **Determine mode.** `CLAY_API_KEY` set → API. Else seat → manual (output spec). Else CSV → BYO. Else → spec-only output.
3. **Choose provider chain.** Default: Apollo + Hunter + BuiltWith + MillionVerifier. Adjust per ICP — funding-trigger needs Crunchbase, mobile needs Lusha. Reference `${HERMES_SKILL_DIR}/references/` for chain options and cost models.
4. **Translate ICP → Clay table spec.** Specify search-step filters, enrichment columns, verifier column, output column-set matching Lead schema. Store as reproducible `clay_table_spec`.
5. **Pre-flight: discover().** API mode: `dry_run: true` preview. Manual: user reports UI count. Surface combined cost broken down by provider. Wait for explicit authorization.
6. **Materialize the table.** Run table (API) or wait for user (manual). Capture `clay_table_id`. Respect rate limits (~100 rows/sec, backoff on 429).
7. **Normalize to Lead schema.** Map columns → Lead fields. Each column has own provenance: `[verified: clay-apollo:run_<id>]`, `[verified: clay-hunter:run_<id>]`, etc. Run `${HERMES_SKILL_DIR}/scripts/normalize_lead.py`.
8. **Dedup against CRM.** `linkedin_url` > `email` > `phone` for person; `company_domain` for company. Run `${HERMES_SKILL_DIR}/scripts/dedup_leads.py`. Log merges.
9. **Compliance + push + summary.** Apply compliance filters. Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. Run summary with per-provider cost breakdown. Typically recommends `lead-scoring` directly (Clay replaces separate enrichment for verified emails).

## Pitfalls

- Adding columns without quoting — per-column cost compounds; always re-quote on chain change
- Skipping the verifier column — saving $0.0015/row to ship `email_status: unverified` is false economy
- Letting Clay handle CRM writeback — breaks source-tag and provenance contract; skill maintains push
- Multi-source provenance collapse — each column has its own provenance; flatten incorrectly and audit value is lost
- Inventing rows when a provider returns nulls — coverage gaps are signal, not failure
- Provider outage handling — blank rows go to review queue, never silently fill them

## Verification

1. `clay_table_id` resolves to the same table on replay
2. Every Lead field carries its column-specific provenance
3. Per-provider costs sum to total ± rounding
4. `lead-scoring` can consume records without re-enrichment for typical ICPs
5. `[unverified]` records landed in review queue
