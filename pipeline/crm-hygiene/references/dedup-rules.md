# Dedup Rules — CRM Hygiene

## Person Dedup Priority

Per function-2 conventions §6:

1. **linkedin_url** — highest confidence unique identifier
2. **email** — second priority (may be role-based or shared)
3. **phone** — third priority (may change frequently)

Process: Group by linkedin_url first. Within unmatched, group by email. Within unmatched, group by phone.

## Company Dedup Priority

1. **company_domain** (apex domain; strip `www.`, protocols, subdomains)

Process: Group by apex domain. Surface collision candidates.

## Merge Recommendation

When two records collide:
- **Keep:** Record with highest-tier provenance + most-recent freshness
- **Merge into:** Older/lower-provenance record
- **Action:** Merge interactions from merge-target into keep-record. Then archive merge-target.

## Source-Run Dedup

Two records from the same sourcing run with identical data → merge.
From different runs → may legitimately reflect different point-in-time states (preserve recent).

## User Authorization Required

Dedup merges + record deletions ALWAYS require user authorization before application. Never auto-merge.
