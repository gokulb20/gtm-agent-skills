---
name: crm-hygiene
description: Maintain CRM data quality — required-field gates per stage, dedup (linkedin_url > email > phone for person; domain for company), industry/title normalization, stale-record flagging, and orphaned-interaction cleanup. Wang & Strong (1996) define 15 data-quality dimensions in 4 categories (Intrinsic / Contextual / Representational / Accessibility); this skill applies the four most operationally critical for CRM hygiene: Accuracy (Intrinsic), Completeness + Timeliness (Contextual), and Consistency (Representational). Use when CRM is approaching deduplication chaos, when a pipeline stage advance fails on missing required fields, when an audit reveals data drift, or when scheduled (weekly) hygiene cleanup is due.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, crm, data-quality, hygiene, function-5]
related_skills:
  - data-enrichment
  - lead-scoring
  - pipeline-stages
  - lead-sourcing-apollo
  - lead-sourcing-clay
  - lead-sourcing-linkedin
  - lead-sourcing-web
  - kpi-reporting
inputs_required:
  - crm-state-or-targeted-record-set
  - required-field-rules-per-entity-and-stage
  - dedup-merge-priority
  - freshness-thresholds-per-field
  - run-purpose-tag
deliverables:
  - hygiene-violation-report
  - dedup-merge-plan
  - normalization-fixes-proposed
  - stale-record-flags
  - orphaned-interaction-cleanup-list
  - hygiene-pass-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# CRM Hygiene

Audit and maintain the agentic-app CRM's data quality. Wang & Strong (1996) define 15 dimensions in 4 categories (Intrinsic / Contextual / Representational / Accessibility); this skill applies the four most operationally critical for CRM hygiene: Accuracy (Intrinsic), Completeness + Timeliness (Contextual), and Consistency (Representational). Surfaces required-field violations per stage, dedup candidates by canonical merge priority, normalization fixes (industry / title / domain), stale records past freshness, and orphaned interactions. Hard rule: never auto-merge or auto-delete without user authorization — surface violations + recommended fixes; user approves bulk apply.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

CRMs degrade. Duplicates accumulate (same person from Apollo + LinkedIn + BYO list); industries get tagged 5 different ways; old emails go stale without flag; interactions orphan when the parent person record gets merged. This skill: runs scheduled (weekly default) audits + on-demand checks; surfaces violations grouped by severity; produces fix plans the user authorizes before bulk-apply. Goal: a CRM clean enough that `lead-scoring`, `pipeline-stages`, and `revenue-forecasting` produce trustworthy outputs.

## When to Use

- "Run weekly hygiene audit on the CRM."
- "Pipeline stage advance failed — required fields missing on a deal."
- "We have 3 records for the same person — dedup."
- "Industry tagging is inconsistent — normalize."
- "100 leads from a sourcing run; check + clean before scoring."
- Scheduled cadence (weekly default).
- Triggered by `pipeline-stages` gate failure on required fields.
- Post-bulk-import validation.

## Inputs Required

1. **CRM state or targeted record set** — full CRM scan OR specific record ids OR a sourcing run output.
2. **Required-field rules per entity and stage** — from `.env` (`CRM_HYGIENE_REQUIRED_FIELDS_PER_STAGE`). E.g., Discovery requires `champion_identified`; Proposal requires `deal_value`.
3. **Dedup merge priority** — per function-2 conventions §6: `linkedin_url > email > phone` for person; `company_domain` for company.
4. **Freshness thresholds per field** — email 90d / phone 12mo / title 6mo / signal half-lives per function-2 conventions §6.
5. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Quality dimensions applied (Wang & Strong, 1996 — 15 dim / 4 categories)** | Accuracy (Intrinsic — data correct) / Completeness (Contextual — required fields present) / Timeliness (Contextual — within freshness window) / Consistency (Representational — same value across copies). Operational subset of the full Wang & Strong framework. |
| **Dedup priority — person** | `linkedin_url` > `email` > `phone` (per function-2 conventions §6) |
| **Dedup priority — company** | `company_domain` (apex; strip `www.`) |
| **Normalization targets** | Industry (Apollo taxonomy as canonical) / Title (cleaned: strip suffixes, normalize seniority) / Domain (apex; lowercase) |
| **Freshness windows** | Email-verified: 90d / Phone: 12mo / Title: 6mo / Signal half-lives: per function-2 §6 |
| **Severity tiers** | P0 (blocks scoring/forecasting) / P1 (degrades quality) / P2 (cosmetic) |
| **Orphaned interaction** | Interaction with `person_id` or `company_id` that no longer exists (post-merge or post-delete) |
| **Auto-fix scope** | Normalization + orphan cleanup only. Dedup merges + record deletions ALWAYS require user authorization. |
| **Audit frequency** | Weekly default; on-demand for triggered cleanup |

## Procedure

### 1. Define audit scope
Full CRM OR targeted record set OR sourcing-run-output. Pull entity counts; estimate audit duration.

### 2. Completeness audit (per stage)
For each entity, check required fields per its current stage. E.g., a deal in Discovery missing `champion_name` → P0 violation (blocks Proposal advance per `pipeline-stages`). List violations with severity.

### 3. Dedup audit
Iterate person records: group by `linkedin_url`; within unmatched, group by `email`; within unmatched, group by `phone`. Iterate company records: group by `company_domain`. Surface dedup candidates with merge recommendations (keep highest-tier provenance + most-recent freshness per function-2 §6).

### 4. Consistency audit (normalization)
- **Industry**: scan against Apollo canonical taxonomy; flag deviations; propose normalization.
- **Title**: scan for raw vs normalized mismatches; propose cleanup (strip "@ Foo | Investor", normalize "VP" / "Vice President" variants).
- **Domain**: lowercase, strip `www.` and protocols.

### 5. Timeliness audit (freshness)
- Emails verified >90d → flag for re-verification (route to `data-enrichment`).
- Phones >12mo → flag.
- Titles >6mo → flag for re-pull from LinkedIn.
- Signals past half-life → flag with recommendation: refresh or downgrade signal weight.

### 6. Orphaned-interaction cleanup
Find interactions where `person_id` / `company_id` doesn't resolve (post-merge / post-delete). Recommend re-link to surviving record OR archive.

### 7. Compile violation report grouped by severity
P0 violations actioned first; P1 batched; P2 cosmetic deferred. Each violation: entity id + dimension + specific field + recommended fix + auto-fix-eligibility flag.

### 8. Apply auto-fix scope (with limits)
Normalization fixes (industry / title / domain) and orphaned-interaction cleanup auto-apply with audit log. Dedup merges + record deletions surface for user authorization; do NOT auto-apply.

### 9. Push to CRM + emit hygiene-pass record
Per conventions: `interaction:research` with violation report + fixes-applied + fixes-deferred-for-user. PATCH affected records (normalization + orphan cleanup); dedup merges deferred to user-authorized batch.

## Output Format

- Hygiene violation report (grouped by severity P0 / P1 / P2)
- Dedup merge plan (per record group with recommended keep + merge-target)
- Normalization fixes proposed (per field with from → to)
- Stale-record flags (per field with freshness age + recommended action)
- Orphaned-interaction cleanup list (per interaction with re-link target or archive recommendation)
- Auto-applied fixes count + deferred-to-user count
- Run record + recommended next skill (`data-enrichment` for stale fields, user authorization queue for dedup)

## Done Criteria

1. Audit scope defined; entity counts surfaced.
2. Completeness audit run per stage; P0 violations surfaced first.
3. Dedup audit run; merge candidates listed with priority-based recommendation.
4. Consistency audit (industry / title / domain) complete; normalization fixes proposed.
5. Timeliness audit complete; stale fields flagged with freshness age.
6. Orphaned-interaction cleanup list generated.
7. Auto-fix scope applied (normalization + orphans); dedup + deletions deferred to user.
8. Push to CRM emitted: violation report + fixes log + deferred-action queue.

## Pitfalls

- **Auto-merging dedup candidates without user authorization.** Merges destroy data; always require user OK.
- **Auto-deleting "stale" records.** Old isn't dead; flag for re-verification, don't archive.
- **Aggressive normalization that loses information.** "VP of Customer Experience" → "VP CX" loses domain; preserve raw alongside normalized.
- **Dedup priority ignored.** Use `linkedin_url > email > phone` per function-2 conventions; don't invent new priorities.
- **Treating freshness as binary.** A 95-day-old email isn't dead, it's likely-stale; route to `data-enrichment` for re-verify.
- **Industry normalization that reshapes audit history.** Preserve original industry value alongside normalized; downstream queries may depend on the original.
- **Skipping orphan cleanup.** Orphans inflate counts in `kpi-reporting` and confuse forecasting.
- **Cosmetic P2 violations treated as P0.** Severity ordering matters; clean deals first, cosmetic data hygiene last.
- **Bulk apply without preview.** User wants to see before/after for each fix class before authorizing batch.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (records, fields, freshness ages, dates, recommended fixes) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Audit results reference actual record states; never invent violations.
- **Ignoring source-run-id when deduplicating.** Two records from the same sourcing run with same data should merge; from different runs may legitimately reflect different point-in-time states (preserve recent).

## Verification

Run is real when: every violation traces to a real record + field; dedup merge plans use the documented priority; normalization preserves originals alongside normalized; auto-applied fixes have audit-log entries; deferred-to-user actions are surfaced for explicit authorization. Negative test: pick 5 random fixes; trace each to its detection rule + provenance; if any "fix" has no source rule, audit logic broke.

## Example

**User prompt:** "Weekly hygiene audit."
**What should happen:** Full CRM scan. Findings: 8 P0 (4 deals in Discovery missing champion_name; 2 deals in Proposal missing deal_value; 2 persons with `linkedin_url` collision); 23 P1 (12 emails >90d need re-verify; 8 industries inconsistent vs Apollo taxonomy; 3 titles raw not normalized); 15 P2 (cosmetic — domain casing, whitespace). Auto-applied: 8 industry normalizations + 3 title normalizations + 4 orphan cleanups. Deferred to user: 2 dedup merges (with merge plans) + 12 stale-email re-verifications (route to `data-enrichment`). Push hygiene-pass record. Recommend running `data-enrichment` on the 12 stale emails + user-review queue for the 2 dedup merges.

**User prompt:** "Pipeline stage advance just failed — Acme deal can't move from Discovery to Proposal."
**What should happen:** Targeted audit on Acme deal. Required-field check at Discovery → Proposal gate: missing `deal_value` AND `decision_process`. Surface as 2 P0 violations on this deal. Recommend: complete the missing slots via `discovery-call-prep` follow-up (decision_process can be discovery-call-extracted) + manual `deal_value` from user. After completion, retry stage advance.

**User prompt:** "Bulk import of 200 leads from a sourcing run — clean before scoring."
**What should happen:** Targeted audit on the source_run_id batch. Findings: 18 dedup candidates (15 against existing CRM, 3 within-run); 22 missing email_status (route to `data-enrichment`); 6 industry-normalization fixes; 0 P0 violations (all leads are at New stage with minimal required fields). Auto-apply normalization. Defer dedup to user (with merge plans). Recommend `data-enrichment` for the 22 missing email_status before `lead-scoring` to avoid score-cap.

## Linked Skills

- Stale fields → `data-enrichment` (re-verify)
- Required-field violations blocking pipeline → `pipeline-stages` (after fixes applied) + `discovery-call-prep` (slot completion)
- Dedup merges affect `lead-scoring` (re-score post-merge)
- Hygiene quality feeds `kpi-reporting` (data-quality KPIs)
- Sourcing-run cleanup → `lead-sourcing-*` (user can adjust source filters to reduce future violations)
- Orphan cleanup keeps `revenue-forecasting` accurate

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-5-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Hygiene violation report | `interaction` (type: `research`) | `relevance` = severity-grouped violation counts + per-violation fixes; `tags: "#hygiene-audit #function-5"` |
| Dedup merge plan (deferred for user authorization) | `interaction` (type: `research`) | `relevance` = per-merge candidate group + recommended keep + merge-target; `tags: "#dedup-merge-plan #manual-review #function-5"` |
| Auto-applied normalization fix | `person` / `company` (PATCH) | normalized field updates + tag `#normalized` added |
| Orphaned-interaction cleanup | `interaction` (PATCH or archive) | `re_link_to: <surviving_id>` OR `archived: true`; `tags: "#orphan-cleanup #function-5"` added |
| Stale-field flag | `person` / `company` (PATCH) | `tags: "#stale-<field> #needs-re-enrichment"` added; `next_re_enrichment_at` populated |
| Run record | `interaction` (type: `research`) | `relevance` = audit summary + fixes applied + deferred queue; `tags: "#crm-hygiene-run #function-5"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
CRM_HYGIENE_REQUIRED_FIELDS_PER_STAGE=     # JSON; per-stage required-field map
```

### Source tag

`source: "skill:crm-hygiene:v2.0.0"`

### Example push (audit run)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#hygiene-audit #function-5",
    "relevance": "Weekly hygiene audit 2026-06-04. Scope: full CRM (1,247 persons / 412 companies / 3,891 interactions). Findings: 8 P0 (4 deals missing champion_name in Discovery / 2 missing deal_value in Proposal / 2 person linkedin_url collisions). 23 P1 (12 emails >90d / 8 industry inconsistencies / 3 raw titles). 15 P2 (cosmetic). Auto-applied: 8 industry normalizations + 3 title normalizations + 4 orphan cleanups. Deferred to user: 2 dedup merges (plans attached) + 12 stale-email re-verifications. Recommended next: data-enrichment (stale emails) + user authorization queue (dedup merges).",
    "source": "skill:crm-hygiene:v2.0.0"
  }'
```

### Example push (dedup merge plan, deferred)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#dedup-merge-plan #manual-review #function-5",
    "relevance": "Dedup candidate group: 2 person records collide on linkedin.com/in/esme-liang-cx. Record A (id: per_001): from Apollo sourcing run apollo_2026-05-04; data_freshness: 2026-05-04; provenance: [verified: apollo-api]. Record B (id: per_087): from LinkedIn sourcing run linkedin_2026-05-22; data_freshness: 2026-05-22; provenance: [verified: phantombuster]. Recommendation: keep B (more recent freshness) + merge A's interactions into B. Awaiting user authorization to apply.",
    "source": "skill:crm-hygiene:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[verified: <crm-query>]` (audit findings) or `[user-provided]` (manual flag) | Standard mapping. |
| `[unverified — needs check]` (audit logic uncertain) | Pushes ONLY as `interaction:research` with `#unverified #review-required #crm-hygiene` tags; no auto-fixes applied. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Audit found 0 violations across all dimensions — push run record with `#crm-clean` tag; no per-violation records.
- Auto-fix attempted but failed (CRM API error) — push as `interaction:research` with `#fix-failed`; do NOT log the fix as applied.
- Dedup merge already applied within last 24h on same group — dedup the dedup-flag.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
