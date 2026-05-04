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

Use Clay's table-based orchestration to combine multiple data providers (Apollo for firmographic search, Hunter for emails, Clearbit for enrichment, BuiltWith for tech stack, MillionVerifier for deliverability) in a single workflow. Output is a list of normalized, provenance-tagged Lead records — same schema as `lead-sourcing-apollo` produces, but with multi-source enrichment baked in rather than deferred to `data-enrichment`.

> *The worked example uses a fictional product (RouteIQ) for illustration. The Clay table spec, multi-source cost rules, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Lead schema, source adapter contract, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`. This skill assumes it.*

## Purpose

Clay is the meta-adapter that most modern outbound teams have standardized on because wiring Apollo + Hunter + Clearbit + a verifier directly is expensive in dev time and credits. This skill: (1) translates an ICP into a Clay table spec — search source + enrichment columns + verifier + writeback, (2) costs the multi-provider workflow before any rows materialize, (3) executes the table (or hands a reproducible spec to the user for manual execution), (4) normalizes Clay's per-column outputs into the function-2 Lead schema. Clay overlaps with `lead-sourcing-apollo` + `data-enrichment`; this skill is the one-pass alternative when the user has Clay credits.

## When to Use

- "We have Clay — pull our list there and run it through verifiers in the same flow."
- "Source from Apollo + find phone via Hunter + check tech stack via BuiltWith — all in one go."
- "Build me a Clay table for our ICP."
- "I have an existing Clay table; push the rows to our CRM."
- "Pulling from Apollo separately then enriching feels wasteful — do it together."
- Multi-source orchestration when the cost model favors Clay over direct-API.

### Do NOT use this skill when

- The play is single-source (just Apollo, just LinkedIn) — `lead-sourcing-apollo` is cheaper and simpler.
- The user has direct API access to all the underlying providers AND wants tighter control over each adapter — direct-API is more flexible than Clay's column-builder.
- Trigger-based plays where Sales Nav is the primary source — `lead-sourcing-linkedin` is sharper for fresh role/leadership signals.
- The user has zero Clay access and isn't paying for the seat — degrade to direct-API skills.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | ICP scorecard | yes (or flag ungrounded) | `icp-definition-v2` output | Provides firmographic, role, trigger library, anti-ICP. |
| 2 | Clay access | one of: API key / seat / existing-table-export | env: `CLAY_API_KEY` or user-uploaded CSV | Determines mode. |
| 3 | Provider config | yes | user / Clay seat | Which providers to chain (Apollo + Hunter? + Clearbit? + verifier?). Each adds cost and coverage. |
| 4 | Target account list **or** firmographic criteria | yes | user / ICP | Either named-account list or filter set. |
| 5 | Cost budget | yes (default `SOURCING_RUN_USD_CAP=$25`) | env or user | Aborts above cap without explicit override. |
| 6 | Run purpose tag | yes | user | Stamped on every record's `source_run_id`. |

### Fallback intake script

> "Clay is good for chaining sources — Apollo + email finder + verifier in one table. Three modes: I can run it directly via Clay API key, give you a Clay table recipe to run in the UI yourself, or ingest a CSV from a Clay table you've already run.
>
> Which providers should be in the chain? Default for a typical SaaS ICP: Apollo (firmographic + persona) → Hunter (email pattern + verifier) → BuiltWith (tech stack) → MillionVerifier (deliverability). Each adds ~$0.05–0.20 per row.
>
> Cost cap (default $25/run) and a one-line purpose tag?"

### Input validation rules

- ICP firmographic absent → `confidence: low`; default provenance to `[unverified — needs check]`; flag run as ICP-ungrounded.
- Clay API key absent AND user has no seat AND no CSV → degrade to filter recommendations + Clay table spec for manual execution.
- Provider chain has no firmographic source → block; the chain must start with a search source (Apollo, Crunchbase, or named-account list).
- Provider chain has no verifier → warn; emails will land `email_status: unverified` and require `data-enrichment` follow-up.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Predictable Revenue** (2011) | Aaron Ross & Marylou Tyler | ICP-driven outbound discipline; never spray. |
| **Trigger Events for Sales Success** (2009) | Craig Elias | Timing-based prioritization within ICP-fit. Clay's column-by-column trigger fetch (recent funding, recent hires) makes triggers materialize as discrete columns. |
| **Multi-source orchestration pattern** (house-built) | Crewm8 | The Clay table = search source × enrichment columns × verifier × writeback. Each step is a column with its own provenance tag. The contract: every column writes back to the Lead schema's named fields, never invents new ones. |
| **Cost-aware quote-before-pull** (house-built) | Crewm8 | Clay charges per-row per-column. Estimate by counting active columns × estimated row count × Clay's per-credit cost. Show breakdown by provider before authorizing. |

## Tools and Sources

### Primary

| Tool | Mode | Purpose |
|---|---|---|
| Clay API | API mode | Programmatic table creation / row materialization. |
| Clay UI (manual) | Manual export mode | User builds table in Clay's UI from skill's spec, exports CSV. |
| Clay table CSV (BYO) | BYO mode | User has an existing Clay-run table; ingest as-is. |

### Provider chain (typical components, executed inside Clay)

| Layer | Provider | Cost (typical) | What it adds |
|---|---|---|---|
| Search | Apollo (via Clay) | ~$0.04/row | Firmographic + persona |
| Search | Crunchbase (via Clay) | ~$0.05/row | Funding events, stage |
| Email | Hunter (via Clay) | ~$0.03/row | Email pattern guess |
| Email | LeadMagic (via Clay) | ~$0.04/row | Better catch-all detection |
| Phone | Lusha (via Clay) | ~$0.10/row | Mobile-rich |
| Tech | BuiltWith (via Clay) | ~$0.02/row | Tech stack |
| Verifier | MillionVerifier (via Clay) | ~$0.0015/row | Deliverability |

### Source priority rule

For overlapping fields (e.g. email from Apollo and Hunter both): **verifier-checked > Hunter pattern guess > Apollo claim**. Clay's own `valid` flag is the verifier verdict only when MillionVerifier or NeverBounce is in the chain. Otherwise mark `email_status: unverified`.

### Clay-specific knowledge

- Clay tables are persistent — they re-run when columns refresh; preserve the `clay_table_id` in the run record so the user can replay.
- Clay charges per *unique* row materialized per column run; re-running the same row on the same column within ~24h is free.
- Clay's "find email" composite column tries Hunter → LeadMagic → Findymail in sequence; treat it as a waterfall and capture which provider hit.
- Clay's writeback step (push to CRM) can be configured inside the table — but skill maintains its own push to keep the function-2 contract uniform; skip Clay's webhook writeback.
- Clay rate-limits API mode at ~100 rows/sec; back off on 429.

## Procedure

### 1. Confirm ICP grounding

Read ICP scorecard from `icp-definition`. If absent → flag ungrounded, `confidence: low`. **Rationale**: same as Apollo skill — the rest is mechanical translation.

### 2. Determine mode

`CLAY_API_KEY` set → API mode. Else seat → manual mode (output table spec). Else CSV → BYO mode. Else → spec-only output.

### 3. Choose the provider chain

Default for a typical SaaS ICP: Apollo (search) → Hunter (email) → BuiltWith (tech-stack signal) → MillionVerifier (verifier). Adjust per ICP signals: if funding is a key trigger, add Crunchbase; if mobile is required (cold-call play), add Lusha. Surface the chain to user with per-provider cost.

### 4. Translate ICP → Clay table spec

Specify: search-step filters (Apollo or Crunchbase), enrichment columns (Hunter find-email, BuiltWith tech-detect, etc.), verifier column (MillionVerifier check), output column-set matching Lead schema. Store as reproducible `clay_table_spec`. **Rationale**: spec is the artifact the user replays; it's the value even when the run itself fails.

### 5. Pre-flight: discover()

For API mode: create the Clay table with `dry_run: true` (Clay's preview), get expected row count + total credits across columns. For manual mode: instruct user to paste filters into Clay's UI; user reports preview row count. Surface combined cost breakdown by provider:

```
Apollo search: 340 rows × $0.04 = $13.60
Hunter find email: 340 × $0.03 = $10.20
BuiltWith tech: 340 × $0.02 = $6.80
MillionVerifier: 340 × $0.0015 = $0.51
Total: ~$31.11. Cap: $25 — over by $6. Reduce row count, remove a column, or raise cap.
```

**Rationale**: multi-provider cost scales linearly per column; surprises are big.

### 6. Materialize the table

Run the table (API mode) or wait for user to run it (manual). Capture `clay_table_id` and `clay_run_id`. Respect rate limits, capture per-column timing for debugging.

### 7. Normalize to Lead schema

For each row, map columns → Lead fields (per conventions §1). Tag provenance per field per §8: each Clay column emits its own provenance — Apollo column → `[verified: clay-apollo:run_<id>]`; Hunter email column → `[verified: clay-hunter:run_<id>]`; verifier column promotes `email_status` to `verified` if Clay returned `valid`. **Rationale**: multi-source = multi-provenance; each field traces to its specific provider.

### 8. Dedup against existing CRM

Same as Apollo procedure: `linkedin_url` > `email` > `phone` for person; `company_domain` for company. Log merges.

### 9. Compliance + push + summary

Apply compliance filters (§7 of conventions). Push per §9 — `company` + `person` + `interaction:research` (Clay table snapshot URL or full spec). Emit run summary with per-provider cost breakdown, dedup log, recommended next skill (`lead-scoring` — Clay-orchestrated runs typically don't need separate `data-enrichment`).

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: <api | manual | byo>
  source: clay-api | clay-manual | clay-byo-csv
  clay_table_id: <id, replay key>
  clay_run_id: <id>
  clay_table_spec:
    search_step: <apollo | crunchbase | named-account-list>
    columns: [<find-email>, <tech-detect>, <verifier>, ...]
    filters: <reproducible filter object>
  cost:
    by_provider:
      apollo: <usd>
      hunter: <usd>
      builtwith: <usd>
      verifier: <usd>
    total_usd: <float>
    cap_usd: <float>
  candidate_count: <int from preview>
  pulled_count: <int>
  pushed_count:
    company: <int>
    person: <int>
    interaction_research: <int>
    review_queue: <int>
  dedup_merge_log: [...]
  warnings: [<string>]
  next_skill_recommendation: <lead-scoring | data-enrichment-only-for-hooks | etc.>

leads:
  # Same Lead schema as lead-sourcing-apollo, but with multi-source provenance:
  # provenance_company: [verified: clay-apollo:run_<id>]
  # provenance_email: [verified: clay-million-verifier:run_<id>]
  # provenance_signals[].source: clay-builtwith / clay-crunchbase / etc.
```

## Worked Example

> *All entities below are tagged `[hypothetical]` — fictional, illustrative.*

**User prompt**: "Pull leads from Clay for our RouteIQ [hypothetical] ICP — fleet ops directors at mid-market trucking companies in TX/OK/AR. We have Clay API key. $25 budget."

**Step 1 — ICP grounding**: RouteIQ ICP from `icp-definition`:
- Firmographic: Trucking / Logistics, 50–500 emp, US (TX/OK/AR), $10–100M revenue.
- Roles: Buyer = VP Operations / Director Fleet, Champion = Fleet Ops Manager.
- Trigger: opened a new terminal in last 12 months OR fleet expansion (truck count growth).
- Anti-ICP: large enterprise (500+ emp) w/ existing TMS contract; pure-asset-light brokers.

**Step 2 — Mode**: `CLAY_API_KEY` set → API mode.

**Step 3 — Provider chain**:
- Apollo (search, firmographic + persona)
- Crunchbase (funding signal — RouteIQ ICP has trigger "recent expansion")
- Hunter (email find — Apollo's coverage in trucking is patchy)
- MillionVerifier (deliverability)
- (No BuiltWith — trucking SMBs aren't well-tagged in BuiltWith)

**Step 4 — Clay table spec**:
```yaml
search_step:
  provider: clay-apollo
  filters:
    organization_industries: ["transportation/trucking/railroad", "logistics & supply chain"]
    organization_num_employees_ranges: ["51,200", "201,500"]
    organization_locations: ["Texas", "Oklahoma", "Arkansas"]
    person_titles: ["VP Operations", "Director of Fleet", "Fleet Operations Manager"]
    person_seniorities: [vp, director, manager]
columns:
  - name: company_terminal_news
    provider: clay-crunchbase
    query: "{{company}} new terminal OR expansion"
  - name: find_email
    provider: clay-hunter
    inputs: [first_name, last_name, company_domain]
  - name: verify_email
    provider: clay-millionverifier
    inputs: [find_email.email]
output_columns: [contact_name, title, email, email_status,
                 company, company_domain, company_size, funding_signal,
                 linkedin_url, signals]
```

**Step 5 — discover()**:
> "Clay table preview: 287 rows.
> - Apollo search: 287 × $0.04 = $11.48
> - Crunchbase signal: 287 × $0.05 = $14.35
> - Hunter find email: 287 × $0.03 = $8.61
> - MillionVerifier: 287 × $0.0015 = $0.43
> Total: ~$34.87. Cap: $25 — over by ~$10.
> Options: (a) drop Crunchbase (skip funding-signal column) → ~$20.52; (b) reduce to 200 rows → ~$24.30; (c) raise cap. Choose?"

User: "Drop Crunchbase, run all 287."

Updated chain materializes table at ~$20.52.

**Step 6 — Materialize**: Clay table id `tbl_routeiq_2026-05-04_q9k`. 287 rows materialized. 0 rate-limit warnings. Per-column timings logged.

**Step 7 — Normalize**: 287 raw → 281 normalized (3 dropped: missing email + missing linkedin; 3 within-run dupes). Sample record:
```yaml
contact_name: "Marisol Garza" [hypothetical]
title_normalized: "Director of Fleet Operations"
seniority: director
function: ops
email: "marisol.garza@silvercreek-trans.com" [hypothetical]
email_status: verified   # MillionVerifier returned 'valid'
provenance_email: [verified: clay-million-verifier:run_2026-05-04_q9k]
phone: null
phone_status: unverified
company: "Silvercreek Transport" [hypothetical]
company_domain: "silvercreek-trans.com"
company_size_band: "51-200"
company_industry_normalized: "transportation/trucking/railroad"
company_location: "Dallas, TX, US"
provenance_company: [verified: clay-apollo:run_2026-05-04_q9k]
provenance_person: [verified: clay-apollo:run_2026-05-04_q9k]
signals:
  - type: tech-adoption
    source: clay-apollo
    detail: "No TMS detected (anti-anti-ICP signal — favorable)"
    date: 2026-05-04 [verified: clay-apollo]
    strength: weak
personalization_hook: null   # No Crunchbase column run; no other source available.
source: clay-api
source_run_id: tbl_routeiq_2026-05-04_q9k
freshness_date: 2026-05-04
```

**Step 8 — Dedup**: 8 collisions against existing CRM (all on `linkedin_url`), 6 keep-existing (higher provenance), 2 replace-with-fresher.

**Step 9 — Compliance + push + summary**:
```
RouteIQ Clay Sourcing Run [hypothetical]
Run ID: tbl_routeiq_2026-05-04_q9k
Mode: API. Providers: Apollo + Hunter + MillionVerifier (Crunchbase dropped for budget)
Cost: $20.52 / cap $25
Pulled: 287 → Normalized: 281 → Pushed: 273 (8 dedup merges)
  Companies: 94 (4 new, 90 enriched)
  Persons: 273 (266 new, 7 merged)
  Interaction:research: 1 (run record) + 0 review-queue
Email status breakdown: 198 verified / 41 risky / 12 catch-all / 30 invalid
Sidecar: 12 role-based emails (not pushed)
Recommended next: lead-scoring (281 records ready; hooks pending — consider data-enrichment for personalization-hook capture)
```

## Heuristics

- **Clay's strength is column-stacking, not search-source novelty.** Use Clay when the *combination* matters; for pure Apollo plays, `lead-sourcing-apollo` is cheaper and simpler.
- **Per-column cost is the killer.** Multi-provider chains scale linearly per row; a 5-column 1,000-row table is $100+ easily. Always quote.
- **Drop columns before reducing rows.** A column dropped from the chain still keeps the row count for replay; reducing rows truncates the addressable list permanently for that run.
- **Verifier is the cheapest column.** Always include it. The deliverability gain pays back the $0.0015/row instantly.
- **Clay's "find email" waterfall.** Hunter → LeadMagic → Findymail is the typical default; capture which provider hit per row for cost auditing.
- **Re-running is free within ~24h.** If the user reviews sample and asks for tweaks, the column re-runs don't double-bill. Take advantage.
- **Clay tables are reproducible by design.** The `clay_table_id` is the replay handle — preserve it; replays in 30 days catch new entrants without rebuild.
- **Trucking / regulated / niche ICPs:** Clay's signal coverage thins out. Cross-check with `lead-sourcing-web` rather than push thin Clay output.
- **The table spec IS the deliverable — even more than with Apollo.** Multi-source spec is the institutional knowledge; preserve and version it.

## Edge Cases

- **No ICP defined.** Flag ungrounded; produce table spec only; default provenance `[unverified — needs check]` aggressively.
- **Named-account list as search step.** Skip Apollo firmographic step; instead use a "people-from-companies" Clay column with the named list. Cost is per company, not per row.
- **Existing Clay table BYO.** User has run a table; uploads CSV. Skill ingests via `normalize`; tags provenance per the column attribution Clay's CSV usually preserves (`Source: Apollo` etc.). If column attribution is lost, default to `[user-provided]`.
- **Table spec produced but Clay run failed mid-execution.** Persist whatever rows landed; flag remainder `pending_run`; provide replay command.
- **Provider in chain returns 0 results for many rows.** Surface coverage gap by provider; e.g. "Hunter found email for 60% of rows — common in trucking; consider direct domain MX-pattern guess for the remainder."
- **User wants to use Clay's writeback (Clay → CRM directly, skipping skill).** Discourage — breaks the function-2 source-tag and provenance contract. Skill maintains its own push.
- **Clay credits exhausted.** Clay returns 402 / "credit limit"; abort; surface for user to refill.
- **PLG product, persona = end-users.** Adjust persona column filters to `manager` + `ic`; warn that Clay's coverage of IC-level contacts at SaaS companies is high quality but at trucking SMBs is patchy.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Clay API auth fails (401) | "Invalid API key" | Confirm key; do NOT retry silently. |
| Clay rate limit (429) | "Too many requests" | Backoff (5s, 30s, 90s); resume from last successful row. |
| Clay returns 5xx | service degraded | Retry with backoff; if still failing, fall back to manual mode (output spec for UI). |
| Provider in chain fails (e.g. Hunter outage) | column blank for some rows | Continue with other columns; flag affected rows; offer re-run on hit-and-miss column later. |
| Verifier disagrees with Hunter find-email confidence | email risky despite Hunter "high confidence" | Trust the verifier; Hunter confidence is heuristic, not deliverability. |
| Clay table preview returns 0 rows | filters too tight | Surface filter set; offer to relax one dimension at a time. |
| Cost cap hit during materialize | partial rows | Stop; persist what materialized; offer to raise cap or accept partial. |
| Clay credits exhausted | 402 | Abort; surface; recommend refill or fall to direct-API skills temporarily. |
| CSV ingestion: column attribution lost | normalize cannot tag provenance | Default to `[user-provided]` for the whole batch; warn user. |
| Push to CRM fails | 4xx/5xx from agentic-app | Persist run output to local JSON; retry on user request. |

## Pitfalls

- **Adding columns without quoting.** Clay's per-column cost compounds; always re-quote on chain change.
- **Skipping the verifier column.** Saving $0.0015/row to ship `email_status: unverified` records is false economy.
- **Treating Clay's "valid" flag without verifier in chain.** It's just provider-claimed; not real verification.
- **Letting Clay handle the CRM writeback.** Breaks function-2's source-tag and provenance contract; the skill maintains push.
- **Multi-source provenance collapse.** Each column has its own provenance; flatten to one tag and you lose audit value.
- **Treating Clay table as one-time artifact.** It's reproducible; preserve `clay_table_id` for replay.
- **Re-pulling within 24h thinking it costs.** Clay won't re-bill a column on the same row inside 24h; sample-and-iterate cheaply.
- **Inventing rows when a provider returns nulls.** Coverage gaps are signal, not failures; never fabricate to fill.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, emails, dates, signal sources) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Each Clay column has its own provenance; flatten incorrectly and the contract breaks.
- **Silent column overspend.** A column accidentally re-running on stale rows can rack up; cap is a hard stop.

## Verification

The run is real when: (a) the `clay_table_id` resolves to the same table on replay; (b) every Lead field carries its column-specific provenance; (c) per-provider costs sum to total ± rounding; (d) `lead-scoring` can consume the records without re-enrichment for typical ICPs (the Clay run replaces the separate `data-enrichment` step for verified emails); (e) `[unverified]` records landed in review queue.

## Done Criteria

1. Mode determined and stated (api / manual / byo) with `clay_table_id` captured.
2. Provider chain confirmed and per-provider cost surfaced before any spend.
3. `clay_table_spec` stored and reproducible.
4. `discover()` quote shown with breakdown by provider; explicit user authorization received.
5. Every Lead field carries column-specific provenance tags.
6. Dedup performed against existing CRM; merges logged.
7. Compliance filters applied; `[unverified — needs check]` routed to review queue.
8. Run summary one-screen with per-provider breakdown; cost stayed under cap (or override logged).

## Eval Cases

### Case 1 — full API mode, 4-column chain

Input: ICP grounded, `CLAY_API_KEY` set, $25 cap, default chain (Apollo + Hunter + verifier + BuiltWith).

Expected: ~250–500 rows materialized, multi-provenance Lead records, 80%+ emails verified inline, 60%+ tech-stack populated, 0 review queue. Recommends `lead-scoring` directly (skips separate enrichment).

### Case 2 — manual mode, ICP grounded

Input: same ICP, no API key, user has Clay seat.

Expected: skill outputs reproducible `clay_table_spec` for the user to paste into Clay UI; user runs the table, exports CSV, drops back to skill. Skill ingests via `normalize` with Clay's column attribution preserved → multi-source provenance retained.

### Case 3 — BYO Clay table CSV, attribution preserved

Input: user has run a Clay table, uploads CSV with provider-attribution columns.

Expected: skill normalizes preserving multi-source provenance per row; if attribution columns missing, defaults to `[user-provided]` and warns; emits run record with `mode: byo`.

### Case 4 — provider outage mid-run

Input: full chain authorized; mid-materialize, Hunter returns 503 for 30% of rows.

Expected: skill completes other columns; flags affected rows `[unverified — needs check]` for email; offers user re-run-on-Hunter command after outage clears; pushes verified rows now and routes affected to review queue.

## Guardrails

### Provenance (anti-fabrication)

Per §8 of conventions: every Clay column writes its own provenance per row. Multi-source means multi-provenance; flatten incorrectly = contract violation. No live API → table spec only, all leads `[unverified — needs check]`. Worked-example fictional entities tagged inline.

### Evidence

Each column emits source name + date + per-row evidence. Costs broken down by provider for audit.

### Scope

This skill orchestrates Clay tables. It does NOT score (lead-scoring), write outreach (function-3), or replace `data-enrichment` for hook capture (Clay can find emails but personalization hooks usually need a SerpAPI / LinkedIn pass that's friendlier in `data-enrichment`).

### Framing

Run summary uses operational language with per-provider cost transparency.

### Bias

Clay's coverage varies by industry — strong in SaaS / tech, thinner in trucking / construction / regulated industries. Surface coverage gaps; never fabricate to fill.

### Ethics

Compliance baseline (§7 of conventions). Clay's column-by-column cost transparency means the user can opt out of expensive providers without losing the search; respect user choice.

### Freshness

Table replays catch new entrants — encourage 30-day replay cadence rather than ad-hoc re-pulls.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Verified emails + tech in run; ready to score | `lead-scoring` | Lead records + ICP scorecard |
| No verifier column in chain; need verification | `data-enrichment` | Lead records (verifier pass only) |
| Hooks needed but not in chain | `data-enrichment` | Lead records (hook capture pass only) |
| Clay coverage thin (industry-specific) | `lead-sourcing-web` | Original ICP + un-found accounts |
| Trigger-based fresh play; Clay too slow | `lead-sourcing-linkedin` | Same ICP + role/trigger filters |
| ICP not grounded | `icp-definition` | Hypothesis + product description |
| Run produced 0 rows | `market-research` (re-evaluate beachhead) OR loosen filters | Filter set |

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
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping. Multi-source provenance flattened only at push time (the entity gets the highest-confidence tag for any given field). |
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
