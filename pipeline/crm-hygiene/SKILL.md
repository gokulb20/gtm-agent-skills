---
name: crm-hygiene
description: Audit and maintain CRM data quality — required-field gates, dedup, normalization, stale-record flagging, and orphan cleanup. Use when the user says "run hygiene audit", "dedup CRM", "normalize industries", or "pipeline gate failed on missing fields."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Pipeline, CRM, Data-Quality, Hygiene, Dedup]
    related_skills: [data-enrichment, lead-scoring, pipeline-stages, kpi-reporting]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# CRM Hygiene

Audit and maintain CRM data quality using Wang & Strong's four operationally critical dimensions: Accuracy, Completeness, Timeliness, Consistency. Surfaces required-field violations, dedup candidates, normalization fixes, stale records, and orphaned interactions. Hard rule: never auto-merge or auto-delete without user authorization.

## When to Use

- Weekly hygiene audit on the CRM
- Pipeline stage advance failed on missing required fields
- 3 records for the same person — dedup
- Industry tagging inconsistent — normalize
- Bulk import validation before scoring
- User says "run hygiene audit" or "dedup CRM"

## Quick Reference

| Concept | Value |
|---|---|
| Quality dimensions (Wang & Strong, 1996) | Accuracy / Completeness / Timeliness / Consistency |
| Dedup priority — person | linkedin_url > email > phone |
| Dedup priority — company | company_domain (apex; strip www.) |
| Freshness windows | Email 90d / Phone 12mo / Title 6mo |
| Severity tiers | P0 (blocks scoring/forecasting) / P1 (degrades) / P2 (cosmetic) |
| Auto-fix scope | Normalization + orphan cleanup only. Dedup merges ALWAYS require user OK |

## Procedure

1. **Define audit scope.** Full CRM or targeted record set. Pull entity counts. See `${HERMES_SKILL_DIR}/references/quality-dimensions.md`.
2. **Completeness audit.** Per entity, check required fields per stage. List violations with severity. P0 first.
3. **Dedup audit.** Group by linkedin_url → email → phone (person); domain (company). Surface merge candidates with priority-based recommendation. See `${HERMES_SKILL_DIR}/references/dedup-rules.md`.
4. **Consistency audit.** Industry vs Apollo taxonomy; title normalization; domain cleanup. Propose fixes.
5. **Timeliness audit.** Email >90d → flag for re-verification. Phone >12mo. Title >6mo. Signal half-life.
6. **Orphaned-interaction cleanup.** Find interactions with missing parent person/company. Re-link or archive.
7. **Compile violation report.** Group by severity P0/P1/P2. Each with fix + auto-fix-eligibility.
8. **Apply auto-fix + push.** Normalization + orphans auto-apply. Dedup merges deferred for user authorization. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Auto-merging without user authorization — merges destroy data
- Auto-deleting stale records — flag for re-verify, don't archive
- Aggressive normalization losing information — preserve raw alongside normalized
- Dedup priority ignored — use linkedin_url > email > phone per function-2 conventions
- Treating freshness as binary — 95-day email isn't dead, it's likely-stale

## Verification

1. Every violation traces to a real record + field
2. Dedup merge plans use documented priority
3. Normalization preserves originals alongside normalized
4. Auto-applied fixes have audit-log entries
5. Deferred actions surfaced for explicit user authorization
