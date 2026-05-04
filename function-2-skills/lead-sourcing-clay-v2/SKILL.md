---
name: lead-sourcing-clay
description: Source leads via Clay's table-based orchestration of Apollo, Hunter, Clearbit, Apify, and other data providers in a single workflow, with cost-aware multi-source chaining, dedup, and provenance tagging. Use when the user has a Clay seat or API key and wants Apollo + email-finder + tech-stack + verifier results in one pull, when a single-source skill (`lead-sourcing-apollo`) misses fields Clay can fill in-flow, or when a Clay table already exists and needs to push to the CRM.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, lead-sourcing, clay, orchestration, function-2]
related_skills:
  - icp-definition
  - lead-sourcing-apollo
  - lead-sourcing-linkedin
  - lead-sourcing-web
  - data-enrichment
  - lead-scoring
inputs_required:
  - icp-scorecard-from-icp-definition
  - clay-api-key-or-seat-or-table-export
  - target-account-or-firmographic-criteria
  - cost-budget-credits-or-dollar
  - run-purpose-tag
deliverables:
  - normalized-lead-records-with-provenance-tags
  - clay-table-spec-reproducible
  - multi-source-cost-and-coverage-report
  - dedup-merge-log
  - sourcing-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Lead Sourcing — Clay

Use Clay's table-based orchestration to combine multiple data providers (Apollo for firmographic search, Hunter for emails, BuiltWith for tech, MillionVerifier for deliverability) in a single workflow. Output is a list of normalized, provenance-tagged Lead records — same schema as `lead-sourcing-apollo` produces, but with multi-source enrichment baked in.

> *Worked example uses a fictional product (RouteIQ [hypothetical]); procedure is vertical-agnostic. Shared rules — Lead schema, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`.*

## Purpose

Clay is the meta-adapter most modern outbound teams have standardized on because wiring Apollo + Hunter + Clearbit + a verifier directly is expensive in dev time and credits. This skill translates an ICP into a Clay table spec, costs the multi-provider workflow before any rows materialize, executes the table (or hands a reproducible spec to the user), and normalizes per-column outputs into the function-2 Lead schema. Goal: a one-pass alternative to `lead-sourcing-apollo` + `data-enrichment` when the user has Clay credits.

## When to Use

- "We have Clay — pull our list there and run it through verifiers in the same flow."
- "Source from Apollo + find phone via Hunter + check tech stack via BuiltWith — all in one go."
- "Build me a Clay table for our ICP."
- "I have an existing Clay table; push the rows to our CRM."
- "Pulling from Apollo separately then enriching feels wasteful — do it together."
- Multi-source orchestration when the cost model favors Clay over direct-API.

## Inputs Required

1. **ICP scorecard** from `icp-definition`. If absent, run flagged ICP-ungrounded with `confidence: low`.
2. **Clay access** — one of: `CLAY_API_KEY` env var, Clay seat (manual mode = output table spec), or existing Clay-table CSV (BYO).
3. **Provider config** — which providers to chain (Apollo + Hunter + BuiltWith + verifier? + Crunchbase? + Lusha?). Each adds cost and coverage.
4. **Target account list OR firmographic criteria.**
5. **Cost budget** — default `SOURCING_RUN_USD_CAP=$25`. Aborts above cap without override.
6. **Run purpose tag** — short string for cost attribution + replay.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | API (key set) / Manual (Clay seat, output spec) / BYO (table CSV) |
| **Default chain** | Apollo (search) → Hunter (email) → BuiltWith (tech) → MillionVerifier (verifier) |
| **Per-row cost** | Agent reads vendor docs at runtime; pricing changes — verify live before any spend. |
| **Cost rule** | Multi-provider cost scales linearly per row × per column. Always quote per-provider before pull. |
| **Free re-run window** | ~24h on the same row × column (Clay's caching) |
| **Provenance** | Each Clay column emits its own provenance per row — flatten only at push time. |
| **Source priority for overlapping fields** | Verifier-checked > Hunter pattern guess > Apollo claim |
| **Replay handle** | `clay_table_id` — preserve in run record for 30-day refresh. |
| **Skip writeback to CRM via Clay** | Skill maintains push to keep function-2 source-tag and provenance contract uniform. |

## Procedure

### 1. Confirm ICP grounding
Read ICP scorecard from `icp-definition`. If absent → flag ungrounded, default provenance `[unverified — needs check]`.

### 2. Determine mode
`CLAY_API_KEY` set → API mode. Else seat → manual mode (output spec). Else CSV → BYO mode. Else → spec-only output.

### 3. Choose the provider chain
Default: Apollo + Hunter + BuiltWith + MillionVerifier. Adjust per ICP — funding-trigger play needs Crunchbase, mobile-required play needs Lusha. Surface per-provider cost.

### 4. Translate ICP → Clay table spec
Specify: search-step filters, enrichment columns, verifier column, output column-set matching Lead schema. Store as reproducible `clay_table_spec`.

### 5. Pre-flight: discover()
For API mode: `dry_run: true` Clay preview returns row count + per-column credits. For manual mode: user reports preview row count from UI. Surface combined cost broken down by provider. Wait for explicit authorization.

### 6. Materialize the table
Run the table (API) or wait for user (manual). Capture `clay_table_id` and `clay_run_id`. Respect rate limits (~100 rows/sec; backoff on 429).

### 7. Normalize to Lead schema
Map columns → Lead fields. Each column emits its own provenance — Apollo column → `[verified: clay-apollo:run_<id>]`, Hunter → `[verified: clay-hunter:run_<id>]`, verifier promotes `email_status` to `verified` only if Clay returned `valid` from MillionVerifier/NeverBounce.

### 8. Dedup against existing CRM
Same priority as Apollo skill: `linkedin_url` > `email` > `phone` for person; `company_domain` for company.

### 9. Compliance + push + summary
Apply compliance filters (§7 of conventions). Push per §9 — `company` + `person` + `interaction:research` (Clay table snapshot or full spec). Run summary with per-provider cost breakdown, dedup log, recommended next skill (typically `lead-scoring` directly since Clay-orchestrated runs replace separate enrichment for verified emails).

## Output Format

- Reproducible `clay_table_spec` (search step + columns + filters)
- `clay_table_id` for replay
- Lead records (full schema, multi-source provenance per field)
- Run record: per-provider cost breakdown, candidate count, pulled/pushed counts, dedup log, warnings, next-skill recommendation
- Sidecar: role-address emails (not pushed)
- Review queue: rows with provider-failure or ambiguous attribution as `interaction:research`

## Done Criteria

1. Mode determined and stated; `clay_table_id` captured for replay.
2. `clay_table_spec` stored and reproducible.
3. Provider chain confirmed; per-provider cost surfaced before any spend.
4. `discover()` quote shown with breakdown by provider; explicit user authorization received.
5. Every Lead field carries column-specific provenance tags — multi-source provenance preserved.
6. Dedup performed against existing CRM; merges logged.
7. Compliance filters applied; `[unverified — needs check]` routed to review queue (not active push).
8. Run summary one-screen with per-provider breakdown; cost stayed under cap (or override logged).

## Pitfalls

- **Adding columns without quoting.** Per-column cost compounds; always re-quote on chain change.
- **Skipping the verifier column.** Saving a fraction of a cent per row to ship `email_status: unverified` records is false economy. Agent reads vendor docs at runtime; pricing changes — verify live before any spend.
- **Treating Clay's "valid" flag without verifier in chain.** It's just provider-claimed; not real verification.
- **Letting Clay handle the CRM writeback.** Breaks function-2's source-tag and provenance contract.
- **Multi-source provenance collapse.** Each column has its own provenance; flatten incorrectly and audit value is lost.
- **Treating Clay table as one-time artifact.** It's reproducible — preserve `clay_table_id` for replay.
- **Re-pulling within 24h thinking it costs.** Clay won't re-bill column on same row inside 24h; sample-and-iterate cheaply.
- **Inventing rows when a provider returns nulls.** Coverage gaps are signal, not failure; never fabricate.
- **Provider outage handling.** When Hunter/Lusha is down, blank rows go to review queue — never silently fill them.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, emails, dates, signal sources) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Each Clay column has its own provenance; flatten incorrectly and the contract breaks.
- **Silent column overspend.** Cap is a hard stop; never bypass.

## Verification

The run is real when: the `clay_table_id` resolves to the same table on replay; every Lead field carries its column-specific provenance; per-provider costs sum to total ± rounding; `lead-scoring` can consume the records without re-enrichment for typical ICPs (verified email column replaces separate `data-enrichment` step); `[unverified]` records landed in review queue.

## Example

**User prompt:** "Pull leads from Clay for our RouteIQ [hypothetical] ICP — fleet ops directors at mid-market trucking companies in TX/OK/AR. We have Clay API key. $25 [hypothetical] budget."
**What should happen:** Read ICP from `icp-definition`. Default chain (Apollo + Crunchbase + Hunter + verifier) preview = ~$35 [hypothetical], over $25 [hypothetical] cap. Skill surfaces options: drop a column, reduce rows, or raise cap. User drops Crunchbase. Materialize 287 [hypothetical] rows at ~$20.52 [hypothetical]. Normalize 281 [hypothetical] (3 [hypothetical] dropped, 3 [hypothetical] in-run dupes). Dedup against CRM (8 [hypothetical] collisions). Push 273 [hypothetical] persons + 94 [hypothetical] companies + 1 [hypothetical] run interaction. Multi-source provenance: company [verified: clay-apollo], email [verified: clay-million-verifier]. Recommend `lead-scoring` directly.

**User prompt:** "I have a Clay seat but no API key. Give me the table spec to run myself."
**What should happen:** Manual mode. Skill outputs reproducible `clay_table_spec` — search-step filters paste-ready, ordered list of columns to add, output column-set. User runs in Clay UI, exports CSV. Skill ingests via `normalize`, preserves Clay's column-attribution where present, flags rows with attribution loss as `[user-provided]`.

**User prompt:** "We already ran a Clay table; here's the CSV. Push it to our CRM."
**What should happen:** BYO mode. Read the CSV, infer column → Lead schema mapping, preserve any Clay attribution columns (they encode per-row provenance), default to `[user-provided]` if attribution lost. Tag every row's source as `clay-byo-csv`. Push companies + persons + run interaction. Recommend `data-enrichment` only for hook capture if hooks weren't in the original Clay table.

## Linked Skills

- Verified emails + tech in run, ready to score → `lead-scoring`
- No verifier column in chain → `data-enrichment` (verifier pass only)
- Hooks needed but not in chain → `data-enrichment` (hook capture pass only)
- Clay coverage thin (industry-specific) → `lead-sourcing-web`
- Trigger-based fresh play → `lead-sourcing-linkedin`
- ICP not grounded → `icp-definition`
- Run produced 0 rows → `market-research` (re-evaluate beachhead) OR loosen filters

## Push to CRM

After materializing the Clay table and normalizing, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company in pull | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-clay #icp-tier-pending"` (lead-scoring updates tags later) |
| Each unique person (verified or user-provided) | `person` | `contactName`, `contactTitle`, `contactEmail`, `contactPhone`, `contactLinkedIn` |
| Run record (table_id, spec, per-provider costs) | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#clay-sourcing-run #function-2"` |
| `[unverified — needs check]` (provider failed for that row) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #lead-sourcing-clay"`; never `company`/`person` |

`lead-scoring` writes `score` + `priority` + tier tags onto the `person` record later via PATCH (per conventions §9.2). This skill does NOT set `score` on push.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
CLAY_API_KEY=
SOURCING_RUN_USD_CAP=25
SOURCING_RUN_RECORD_CAP=2000
```

### Source tag

`source: "skill:lead-sourcing-clay:v2.0.0"`

### Example push (verified person + company, multi-source provenance)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Silvercreek Transport",
    "website": "https://silvercreek-trans.com",
    "industry": "Transportation/Trucking/Railroad",
    "tags": "#sourced-clay #icp-tier-pending #trucking #tx",
    "contactName": "Marisol Garza",
    "contactTitle": "Director of Fleet Operations",
    "contactEmail": "marisol.garza@silvercreek-trans.com",
    "contactLinkedIn": "https://linkedin.com/in/marisol-garza-fleet",
    "relevance": "Sourced from Clay table tbl_routeiq_2026-05-04_q9k. Chain: Apollo + Hunter + MillionVerifier. Provenance: company [verified: clay-apollo], person [verified: clay-apollo], email [verified: clay-million-verifier], email_status: verified.",
    "source": "skill:lead-sourcing-clay:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#clay-sourcing-run #function-2",
    "relevance": "Clay sourcing run tbl_routeiq_2026-05-04_q9k. Mode: API. Chain: Apollo+Hunter+MillionVerifier (Crunchbase dropped for budget). Cost: $20.52 / cap $25. Per-provider: Apollo $11.48, Hunter $8.61, MillionVerifier $0.43. Pulled 287 → Normalized 281 → Pushed 273 (8 dedup merges, 12 role-address sidecar). 0 review-queue. Recommended next: lead-scoring.",
    "source": "skill:lead-sourcing-clay:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §8.2:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping. Multi-source provenance flattened only at push time. |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #lead-sourcing-clay` tags. Never as `company` / `person`. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified push (Hunter outage):

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #lead-sourcing-clay",
    "relevance": "Marisol Garza @ Silvercreek Transport [unverified — needs check] — Hunter outage during Clay run; email column blank. Provider returned 503 for 27 rows. Recommend re-run on hunter column when service stabilized.",
    "source": "skill:lead-sourcing-clay:v2.0.0"
  }'
```

### When NOT to push

- Run that returned 0 rows — push run record, no person/company.
- Provider outage left >50% of rows incomplete — abort push; route everything to review queue with retry recommendation.
- BYO CSV with no provider attribution — push as `interaction:research` with `#byo-attribution-lost` tag; defer person push until re-run with attribution.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
- Run flagged "ICP-ungrounded" — push run record tagged `#icp-ungrounded`; defer person push until ICP exists.
