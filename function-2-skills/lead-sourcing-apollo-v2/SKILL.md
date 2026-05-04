---
name: lead-sourcing-apollo
description: Source B2B leads from Apollo (API, manual export, or BYO list) by translating an ICP scorecard into firmographic and persona filters, quoting cost before pulling, normalizing to the function-2 Lead schema, and pushing companies + persons + run-history interactions to the CRM. Use when the user wants to build an outbound list grounded in a defined ICP, has an Apollo seat or API key, has an Apollo CSV export, or has any list to ingest and normalize.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, lead-sourcing, apollo, outbound, function-2]
related_skills:
  - icp-definition
  - lead-sourcing-clay
  - lead-sourcing-linkedin
  - lead-sourcing-web
  - data-enrichment
  - lead-scoring
inputs_required:
  - icp-scorecard-from-icp-definition
  - apollo-api-key-or-seat-or-byo-list
  - target-account-or-firmographic-criteria
  - cost-budget-credits-or-dollar
  - run-purpose-tag
deliverables:
  - normalized-lead-records-with-provenance-tags
  - apollo-search-filter-set-reproducible
  - cost-and-coverage-report
  - dedup-merge-log
  - sourcing-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Lead Sourcing — Apollo

Translate a defined ICP into an Apollo search, pull a cost-quoted batch of contacts, normalize them to the function-2 Lead schema, and push companies + persons + a run-history interaction to the CRM. Operates in three modes — direct API, manual export, or BYO CSV — and degrades gracefully so a user without an API key still gets a usable list.

> *Worked example uses a fictional product (WorkflowDoc [hypothetical]); procedure is vertical-agnostic. Shared rules — Lead schema, adapter contract, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`.*

## Purpose

Apollo is the spine of most function-2 sourcing runs. This skill translates an ICP scorecard's firmographic + role + trigger criteria into a precise Apollo filter set, quotes candidate count and credit cost before any pull, and normalizes Apollo's raw fields into the canonical Lead schema. Goal: a list of qualified, deduped, provenance-tagged people — not 4,000 unfiltered email addresses.

## When to Use

- "Build me a list of 500 leads matching our ICP."
- "We have an Apollo seat — pull contacts for these accounts."
- "I have an Apollo CSV export, can you ingest it?"
- "Source SDRs at Series B SaaS companies in the US."
- "I need the search filters to run in Apollo manually."
- "Take this list of 300 companies and find the VP of Support at each."
- "We have a list from a friend's CRM — clean it up and push to ours."
- Pre-outreach list-build when ICP exists and Apollo is the chosen source.

## Inputs Required

1. **ICP scorecard** from `icp-definition` — firmographic, role map, trigger library, anti-ICP. If absent, run flagged ICP-ungrounded with `confidence: low`.
2. **Apollo access** — one of: `APOLLO_API_KEY` env var, Apollo seat (manual export mode), or any user-supplied list (BYO mode).
3. **Target account list OR firmographic criteria** — named accounts ("source contacts at these 60 companies") or filters ("Series B SaaS, US, 100–300 emp").
4. **Cost budget** — defaults to `SOURCING_RUN_USD_CAP=$25`. Skill aborts above cap without explicit override.
5. **Run purpose tag** — short string ("q2-outbound-burst"). Stamped on every record's `source_run_id`.
6. (Optional) Persona / geography overrides applied on top of ICP.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | API (key set) / Manual export (Apollo seat, no key) / BYO (any list) |
| **Adapter contract** | `discover()` → count + cost; `pull()` → records; `normalize()` → Lead schema |
| **Quote-before-pull** | Mandatory. Never `pull()` without `discover()` + user confirm. |
| **First-batch default** | ≤500 records. Validate filter quality before expanding. |
| **Cost cap** | `SOURCING_RUN_USD_CAP` (default $25); record cap `SOURCING_RUN_RECORD_CAP=2000` |
| **Dedup priority** | `linkedin_url` > `email` > `phone` (person); `company_domain` (company) |
| **Apollo "verified" email** | Hint, not verdict. Always pair with `data-enrichment` verifier. |
| **Provenance tags** | `[verified: apollo-api]` (API), `[user-provided]` (CSV/BYO), `[unverified — needs check]` (agent-inferred) — never untagged |
| **Compliance** | EU contacts → `gdpr_basis: legitimate-interest`; role-addresses (`info@`, `sales@`) → sidecar; `phone_status: dnc` → strip |
| **Push routing** | Verified/user-provided → `company` + `person` + run `interaction`; unverified → `interaction:research` with `#unverified #review-required` only |

## Procedure

### 1. Confirm ICP grounding
Read ICP scorecard from `icp-definition`. Extract firmographic, role map, triggers, anti-ICP. If absent → flag ICP-ungrounded, `confidence: low`, default provenance to `[unverified — needs check]`.

### 2. Determine mode
`APOLLO_API_KEY` set → API mode. Else seat → manual export mode. Else any list → BYO mode. Else → filter recommendations only. Never fail with "Apollo not configured."

### 3. Translate ICP → Apollo filter set
Map field-by-field: ICP industry → `organization_industries`; size → `organization_num_employees_ranges`; geography → `person_locations` + `organization_locations`; funding → `organization_latest_funding_stage`; tech → `currently_using_any_of_technology_uids`; titles → `person_titles`; seniority → `person_seniorities`; function → `person_departments`; anti-ICP → `not_organization_*`. Store as reproducible `source_query`.

### 4. Pre-flight: discover()
Surface to user: candidate count, estimated USD, sample of 5 with provenance tags. Wait for explicit authorization before pulling. Never bypass.

### 5. Pull
Page through results, respect rate limits (Apollo: ~60 req/min; backoff on 429), cap at `SOURCING_RUN_RECORD_CAP`. Stamp `source_run_id` and `source: apollo-api` on every record.

### 6. Normalize
Map to Lead schema (conventions §1). Tag provenance per field (§8). Construct `personalization_hook` ONLY when there is a citable URL — never invent. Title cleanup, seniority inference, function inference.

### 7. Dedup against existing CRM
Merge by `linkedin_url` > `email` > `phone` for person; `company_domain` for company. Keep higher-tier provenance + more recent freshness. Log every merge.

### 8. Apply compliance filters
EU contacts → `gdpr_basis: legitimate-interest`. Role-address emails → sidecar list. DNC phones → strip from active list.

### 9. Push to CRM + emit run summary
Per conventions §9: `company` + `person` + `interaction:research` for verified/user-provided; `interaction:research` only for unverified (review queue). One-screen run summary with cost, counts, dedup log, recommended next skill (`data-enrichment` typically).

## Output Format

- Reproducible `source_query` filter object
- Lead records (full schema, provenance-tagged on every named field)
- Run record: filter set, candidate count, credits used, pulled/pushed counts, dedup merge log, warnings, recommended next skill
- Sidecar: role-address emails (not pushed)
- Review queue: `[unverified — needs check]` records as `interaction:research`

## Done Criteria

1. Mode stated (api / manual-export / byo); `source_query` filter object stored and reproducible.
2. `discover()` quote shown; explicit user authorization received before any `pull()`.
3. Every Lead carries provenance tags on identity, person, company, email, signals — no untagged named fields.
4. Dedup performed against existing CRM; merges logged.
5. Compliance filters applied (GDPR EU, role-address sidecar, DNC strip).
6. `[unverified — needs check]` records routed to review queue, NOT active push.
7. Run summary one-screen with next-skill recommendation; cost stayed under cap (or override logged).

## Pitfalls

- **Pulling without a quote.** Always `discover()` first — "just give me 4,000 leads" is how teams burn $500 in credits. Cost cap is a hard stop; surface every cap hit, never bypass.
- **Trusting Apollo's "verified" email flag.** It's a hint, not a verdict. Pair with a real verifier in `data-enrichment`. Same for Apollo as a single source of truth — cross-check funding signals with Crunchbase.
- **Inventing personalization hooks.** "Saw your post on X" with no post URL is hallucination. Hooks ship with citable URLs or they don't ship.
- **Ignoring company-size-adjusted seniority.** "VP of Growth" at 50 people ≠ "VP of Growth" at 5,000.
- **Blasting role addresses.** `info@`, `sales@`, `contact@` → sidecar, never active push.
- **Filters too tight, then over-loosened.** Loosen one dimension at a time and re-discover.
- **Skipping the run record.** Without `interaction:research`, you lose cost-per-lead attribution downstream.
- **Over-pulling on first run.** 500 records is enough to validate; 4,000 is a cleanup project.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, emails, dates, dollar figures, evidence URLs) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No live API → default to `[unverified — needs check]`. Never invent specifics like a Series B funding date or a tech-stack adoption to fill the signals array.

## Verification

The run is real when: (a) the `source_query` filter object is reproducible — running it again returns the same candidates ± new entrants; (b) every record carries provenance tags on every named field; (c) the run record's costs match Apollo's billing dashboard ± rounding; (d) `data-enrichment` and `lead-scoring` can consume the records without source-specific glue; (e) `[unverified — needs check]` records landed in the review queue, not the active prospect list.

## Example

**User prompt:** "Pull leads from Apollo for our WorkflowDoc [hypothetical] ICP. We have an Apollo API key. $20 budget [hypothetical]."
**What should happen:** Read ICP from `icp-definition` (Series B SaaS [hypothetical], 100–300 emp [hypothetical], US [hypothetical], support team [hypothetical], Zendesk|Intercom [hypothetical], VP/Director/Manager seniority in support function [hypothetical]). Translate to Apollo filters. Run `discover()` → ~340 contacts [hypothetical] across ~110 companies [hypothetical], ~$7 in credits [hypothetical]. Show 5-record sample [hypothetical] with `[verified: apollo-api]` tags, ask user to confirm. After confirm, pull 340 [hypothetical], normalize 338 [hypothetical] (2 dropped [hypothetical]: missing company + within-run dupe [hypothetical]), dedup against CRM (12 merges [hypothetical]), strip 14 role-addresses [hypothetical] to sidecar, push 326 persons [hypothetical] + 110 companies [hypothetical] + 1 run interaction [hypothetical]. Recommend `data-enrichment` next.

**User prompt:** "I don't have an Apollo API key but I have a paid Apollo seat — give me the search filters."
**What should happen:** Skill detects no API key, switches to manual export mode without erroring. Outputs the exact filter set to paste into Apollo's UI (industries, employee ranges, seniority, departments, technology UIDs, geography), the column-set to enable on export, and a 4-step instruction sheet. After user uploads the resulting CSV, skill normalizes it with all fields tagged `[user-provided]`, flags `email_status: unverified` everywhere, recommends `data-enrichment` as mandatory before any outreach.

**User prompt:** "We have a 200-row list [hypothetical] from a friend's CRM. Can you clean it up and push to ours?"
**What should happen:** BYO mode. Read the CSV, infer column mapping (`Full Name` → `contact_name` [hypothetical], `Co.` → `company` [hypothetical]), confirm with user. Flag missing fields (e.g. 60% lack `linkedin_url` [hypothetical]). Tag every row `[user-provided]` with `confidence: low`. Defer `person` push until `data-enrichment` runs; push only the run record + `#byo-pending-enrichment` interactions. If no ICP, flag ungrounded and recommend `icp-definition` first.

## Linked Skills

- Verify emails, find phones, capture personalization hooks → `data-enrichment`
- Score the pulled list against the ICP scorecard → `lead-scoring`
- Multi-source orchestration (Apollo + Hunter + verifier in one workflow) → `lead-sourcing-clay`
- Role/trigger play (recent VP hires, leadership shifts) → `lead-sourcing-linkedin`
- Trigger Apollo can't see (job posts, press, RFPs) → `lead-sourcing-web`
- ICP not grounded → `icp-definition`
- Run produced 0 results despite filter loosening → `market-research` (re-evaluate beachhead)
- Active campaign monitoring pull-quality over time → `campaign-management` (planned)

## Push to CRM

After pulling and normalizing, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company in pull | `company` | `website`, `industry`, `companySize` (band), `tags: "#sourced-apollo #icp-tier-pending"` (lead-scoring updates tags later) |
| Each unique person in pull (provenance verified or user-provided) | `person` | `contactName`, `contactTitle`, `contactEmail`, `contactPhone`, `contactLinkedIn` |
| Run record (filter set, cost, dedup log) | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#apollo-sourcing-run #function-2"` |
| `[unverified — needs check]` records | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #lead-sourcing-apollo"`; never `company`/`person` |

`lead-scoring` writes `score` + `priority` + tier tags onto the `person` record later via PATCH (per §9.2 of conventions). This skill does NOT set `score` on push — leaves it blank for `lead-scoring`.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
APOLLO_API_KEY=
SOURCING_RUN_USD_CAP=25
SOURCING_RUN_RECORD_CAP=2000
```

### Source tag

`source: "skill:lead-sourcing-apollo:v2.0.0"`

### Example push (verified person + company)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "website": "https://stitchbox.com",
    "industry": "Computer Software",
    "tags": "#sourced-apollo #icp-tier-pending #zendesk #series-b",
    "contactName": "Ada Bell",
    "contactTitle": "VP of Customer Support",
    "contactEmail": "ada@stitchbox.com",
    "contactLinkedIn": "https://linkedin.com/in/adabell-h",
    "relevance": "Sourced from Apollo run_2026-05-04_h7k. Filter: Series B SaaS, 100–300 emp, US, Zendesk|Intercom, Support seniority VP+. Provenance: company [verified: apollo-api], person [verified: apollo-api], email [verified: apollo-api], email_status: unverified (pending data-enrichment).",
    "source": "skill:lead-sourcing-apollo:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#apollo-sourcing-run #function-2",
    "relevance": "Apollo sourcing run run_2026-05-04_h7k. Mode: API. Filter: [Series B SaaS, 100–300 emp, US, Zendesk|Intercom, Support seniority VP+]. Cost: 340 credits / ~$7. Pulled 340 → Normalized 338 → Pushed 326 (12 dedup merges, 14 role-address sidecar). 0 review-queue records. Recommended next: data-enrichment.",
    "source": "skill:lead-sourcing-apollo:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §8.2:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above (real `company` / `person` / `interaction` records, normal priority/score). |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #lead-sourcing-apollo` tags. Never as `company` / `person`. Held for human review; the dashboard review-queue filter is a follow-up agentic-app task. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #lead-sourcing-apollo",
    "relevance": "Candidate Stitchbox VP of Support [unverified — needs check] — name not in Apollo response, agent-inferred from company-page scrape. Needs human verification before activation.",
    "source": "skill:lead-sourcing-apollo:v2.0.0"
  }'
```

### When NOT to push

- Run that returned 0 results — push the `interaction:research` run record (the *fact* of the empty run is information) but no `company` / `person`.
- BYO records with `confidence: low` and missing required fields — push `interaction:research` with `#byo-pending-enrichment` tag; defer `person` push until after `data-enrichment`.
- `[unverified — needs check]` — see provenance routing above; never as person/company.
- `[hypothetical]` — never.
- Run flagged "ICP-ungrounded" — push the run record but tag it `#icp-ungrounded` so downstream skills downweight; defer `person` push until ICP exists or user explicitly overrides.
