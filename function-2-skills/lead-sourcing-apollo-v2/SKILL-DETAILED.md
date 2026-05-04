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

Translate a defined ICP into an Apollo search, pull a cost-quoted batch of contacts, normalize them to the function-2 Lead schema, and push companies + persons + a run-history interaction to the CRM. Operates in three modes — direct API, manual export, or BYO CSV — and degrades gracefully between them so a user without an API key still gets a usable list.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *This skill follows the shared rules in `function-2-skills/function-2-conventions.md` — Lead schema, source adapter contract, three-mode pattern, dedup keys, compliance baseline, anti-fabrication tagging, and push-to-CRM routing all live there. Read it once; this skill assumes it.*

## Purpose

Apollo is the most common B2B database for outbound SDRs, so it is the spine of any function-2 sourcing run. This skill does three things: (1) translates an ICP scorecard's firmographic + role + trigger criteria into a precise Apollo filter set, (2) quotes the candidate count and credit cost before any pull happens, and (3) normalizes Apollo's raw fields into the canonical Lead schema so `data-enrichment` and `lead-scoring` can act on the records without source-specific glue. The goal is a list of qualified, deduped, provenance-tagged people — not 4,000 unfiltered email addresses.

## When to Use

- "Build me a list of 500 leads matching our ICP."
- "We have an Apollo seat — pull contacts for these accounts."
- "I have an Apollo CSV export, can you ingest it?"
- "Source SDRs at Series B SaaS companies in the US."
- "I need the search filters to run in Apollo manually."
- "Take this list of 300 companies and find the VP of Support at each."
- "We have a list from a friend's CRM — clean it up and push to ours."
- Pre-outreach list-build when ICP exists and Apollo is the chosen data source.

### Do NOT use this skill when

- The ICP has not been defined. Run `icp-definition` first; this skill will refuse to operate on full automation without one and produce only filter recommendations otherwise.
- The play is **role-based or trigger-based** (recent VP hires, leadership shifts, open job reqs revealing tech-stack pain) — Sales Navigator surfaces these in real time. Use `lead-sourcing-linkedin`.
- The trigger is invisible to Apollo (RFP issuance, regional press, customer-support-page hiring announcements) — use `lead-sourcing-web`.
- The user wants multi-source orchestration in one workflow (Apollo + Hunter + tech-stack + verifier) — use `lead-sourcing-clay` (Clay's meta-adapters are cheaper than wiring four APIs).
- The list already exists, is already enriched, and just needs scoring — skip to `lead-scoring`.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | ICP scorecard | yes (or flag ungrounded) | `icp-definition-v2` output | Provides firmographic, role, trigger library, anti-ICP. |
| 2 | Apollo access | one of: API key / seat / CSV / BYO list | env: `APOLLO_API_KEY` or user-uploaded file | Determines mode (§3 of conventions). |
| 3 | Target account list **or** firmographic criteria | yes | user / ICP | Either a named-account list ("source contacts at these 60 companies") or firmographic filters ("Series B SaaS, US, 100–300 emp"). |
| 4 | Cost budget | yes (default `SOURCING_RUN_USD_CAP=$25`) | env or user | Skill aborts above cap without explicit override. |
| 5 | Run purpose tag | yes | user | One short string ("q2-outbound-burst", "icp-validation-pull"). Stamped on every record's `source_run_id`. |
| 6 | Persona overrides (optional) | no | user | "Only Director-level and up" / "Skip Engineering function" — applied on top of ICP role map. |
| 7 | Geography overrides (optional) | no | user | "US/Canada only" — applied on top of ICP geography. |

### Fallback intake script (when input is missing)

> "I can pull leads from Apollo three ways: directly via API key, manually via filter export, or by ingesting a list you already have. Which do you have?
>
> If we have an ICP from `icp-definition`, I'll translate it to Apollo filters automatically. If we don't, share the firmographic + role criteria you have in mind and I'll mark the run as ICP-ungrounded.
>
> Two more things: a cost cap (default $25/run) and a one-line purpose tag for this run (e.g. `icp-validation-pull`)."

### Input validation rules

- ICP firmographic absent → `confidence: low`, `provenance` defaults to `[unverified — needs check]` for fit assertions, output flagged "ICP-ungrounded" in the run interaction.
- API key absent AND user has no Apollo seat AND no list to ingest → produce filter recommendations only; refuse to fabricate records.
- Target account list > `SOURCING_RUN_RECORD_CAP` (default 2,000) → abort and ask user to slice.
- Run purpose tag missing → block; the tag is required for downstream cost-per-lead attribution in `channel-performance`.

## Frameworks Used

The skill is operational and tool-bound; the intellectual foundation is light but real.

| Framework | Author | What we apply |
|---|---|---|
| **Predictable Revenue** (2011) | Aaron Ross & Marylou Tyler | The discipline of ICP-driven outbound — never spray, always pull against an explicit ICP. The "Cold Calling 2.0" sequence is downstream (function-3); the *list-building* discipline is upstream and applies here. |
| **Trigger Events for Sales Success** (2009) | Craig Elias | Use timing-based events (funding, hiring, leadership change, tech adoption) to prioritize within an ICP-fit list. A Tier-1 fit + fresh trigger is hot; Tier-1 fit + no trigger is nurture. |
| **Source adapter contract** (house-built) | Crewm8 | The `discover/pull/normalize` interface. Standardizes the cross-tool surface so swapping Apollo for ZoomInfo is a new adapter, not a rewrite. |
| **Cost-aware quote-before-pull** (house-built) | Crewm8 | The discipline of running `discover()` and surfacing candidate count + estimated spend before authorizing a `pull()`. |

Note: the 100-point ICP scorecard, BANT, and CHAMP are scoring frameworks — they live in `lead-scoring`, not here. This skill produces inputs to those.

## Tools and Sources

### Primary

| Tool | Mode | Purpose |
|---|---|---|
| Apollo.io People Search API | API mode | Persona + firmographic search; returns contacts with email, title, company, LinkedIn. |
| Apollo.io Organizations API | API mode | Firmographic search; returns companies with size, industry, tech stack, funding. |
| Apollo CSV export (UI) | Manual export mode | User runs the search in Apollo's UI and exports the standard "People" or "Companies" CSV. |

### Secondary / fallback

| Tool | Mode | Purpose |
|---|---|---|
| Apify Apollo scraper | API-substitute | When user has Apollo seat but no API key; runs on user's behalf via session. |
| User-supplied CSV (BYO) | BYO mode | Any list the user has from anywhere. Schema repair lives in `normalize`. |

### Source priority rule

For any single field, the source priority is: **live API call within last 7 days** > **CSV exported within last 30 days** > **BYO list with `[user-provided]` tag** > **agent inference (`[unverified — needs check]`)**. Never invent email addresses; phone-number guessing is a hard stop (legal + accuracy risk).

### Apollo-specific filter knowledge

- Apollo's `industry` taxonomy is NAICS-derived but proprietary. Use the canonical industry strings from Apollo's `/api/v1/labels` endpoint when targeting; record the source's raw value alongside the normalized value in the Lead record.
- Employee-size bands are: 1, 2-10, 11-20, 21-50, 51-100, 101-200, 201-500, 501-1000, 1001-2000, 2001-5000, 5001-10000, 10001+. Map to the Lead schema's `company_size_band` (which is coarser).
- The "verified" email flag in Apollo is optimistic — it confirms format and (sometimes) MX, not deliverability. ALWAYS pair with a second verifier in `data-enrichment` for Tier-1 sends.
- Apollo's seniority filter (`person_seniorities`) maps cleanly to the Lead `seniority` enum: c_suite → c-level, vp → vp, director → director, manager → manager, senior + entry → ic.
- Apollo's "founded year" is sometimes wrong by 1–2 years. Don't drive trigger logic off it alone; cross-check with Crunchbase if available.

### Apollo API endpoint reference

| Endpoint | Purpose | Pagination |
|---|---|---|
| `POST /api/v1/mixed_people/search` | Persona search with firmographic filters in one call | `page` + `per_page` (max 100) |
| `POST /api/v1/mixed_companies/search` | Firmographic-only search | `page` + `per_page` (max 100) |
| `POST /api/v1/people/match` | Lookup a single person by email or LinkedIn URL | n/a |
| `POST /api/v1/organizations/enrich` | Enrich a single company by domain | n/a |
| `GET /api/v1/labels` | Fetch canonical industry / technology / seniority taxonomies | n/a |

Rate limits typically: 60 req/min on Pro, 120 req/min on Enterprise. The `X-Rate-Limit-Remaining` header is authoritative; back off when it nears 0. Credits charged per *unique* contact returned, not per search call — repeating the same search within a short window costs 0 additional credits up to ~24h.

### Manual export mode — exact UI steps

When dropping into Apollo's UI:

1. **Search → People** (top nav). Apply filter set from §3 of the Procedure.
2. Click **Save Search** with a name matching the run's purpose tag (so future replays inherit it).
3. **Export → CSV** (top right). Column-set checklist:
   - Identity: First Name, Last Name, Email, Email Status, LinkedIn URL, Phone, Mobile Phone
   - Title: Title, Seniority, Departments
   - Company: Company, Company Domain, Industry, Employees, Country, State/City, Founded Year
   - Signals: Latest Funding Stage, Latest Funding Amount, Latest Funding Date, Technologies (multi-select)
4. Drop the resulting CSV into the agent's workspace. Skill ingests via `normalize` with `source: apollo-csv-export`.

This column-set covers the Lead schema's required fields. Skipping `Email Status` is the most common oversight — without it, `email_status` defaults to `unverified` for every row regardless of Apollo's view.

## Procedure

### 1. Confirm ICP grounding

Read the ICP scorecard from `icp-definition`'s output. Extract: firmographic (industry, size band, geography, stage, tech stack), role map (Buyer / Champion / User titles + seniority), trigger library, anti-ICP boundary. If absent → flag run as ICP-ungrounded, set `confidence: low`, proceed with user-supplied criteria. **Rationale**: the rest of the procedure is mechanical translation; it only produces a usable list if the ICP is real.

### 2. Determine mode

Check env: `APOLLO_API_KEY` set? → API mode. Else ask user about Apollo seat → if yes, manual export mode. Else ask if they have any list → if yes, BYO mode. Else → degrade to filter-recommendations-only output. **Rationale**: most real users won't have all keys connected; gracefully degrading is the only way the skill gets used in the wild.

### 3. Translate ICP → Apollo filter set

Map field-by-field:
- ICP industry → Apollo `organization_industries` (canonical strings).
- ICP size band → Apollo `organization_num_employees_ranges`.
- ICP geography → Apollo `person_locations` + `organization_locations`.
- ICP funding stage → Apollo `organization_latest_funding_stage`.
- ICP tech stack signal → Apollo `currently_using_any_of_technology_uids`.
- ICP role map titles → Apollo `person_titles` (use both exact strings and Apollo's normalized forms).
- ICP seniority → Apollo `person_seniorities`.
- ICP function → Apollo `person_departments`.
- Anti-ICP firmographic → Apollo `not_organization_industries`, `not_organization_num_employees_ranges`, etc.

Output: a reproducible filter object stored as `source_query` in the run record. **Rationale**: reproducibility lets `lead-scoring`'s rationale cite the exact filter set, and lets future runs replay or diff filters.

### 4. Pre-flight: discover()

Call Apollo's `mixed_people/search?per_page=5&page=1` (API mode) or instruct user to run the filter set in Apollo UI and report the candidate count (manual mode). Surface to the user:

```
Search matches ~4,200 contacts across ~620 companies.
Pulling all 4,200 ≈ $84 in Apollo credits.
Recommended: pull 500 highest-fit first (~$10), review sample, then expand.
Sample of 5: [list with [verified: apollo-api] tags]
Proceed with [500] [all 4,200] [refine filters]?
```

**Rationale**: this is the single most important habit — never trigger a `pull()` without an explicit cost confirmation. Skipping this is how teams burn $500 in credits on bad filters.

### 5. Pull the batch

Once authorized, page through Apollo's results. Respect rate limits (Apollo: 60 req/min on most plans; back off on 429). Cap at `SOURCING_RUN_RECORD_CAP`. Capture raw response IDs for provenance. Stamp `source_run_id` (UUID) and `source: "apollo-api"` (or `"apollo-csv-export"` / `"byo-csv"`) on every record. **Rationale**: the run_id is the unit of audit — one run = one cost = one ICP filter set = N records. Every downstream skill keys off it.

### 6. Normalize to the Lead schema

For each raw record:
- Map identity, person, company, signals fields per §1 of conventions.
- Tag provenance per field per §8 of conventions: API-returned fields → `[verified: apollo-api:run_<id>]`; agent-inferred fields → `[unverified — needs check]`.
- Construct `personalization_hook` ONLY when there is a citable source: an Apollo "news" event, a recent funding date, a hire date — ALL with permalink. Otherwise leave `personalization_hook: null` and tag the absence — never invent ("Saw your post on..." with no post URL is forbidden).
- Apply normalization rules: title cleanup (strip "@ Foo \| Investor" suffixes), seniority inference, function inference from title + department.

**Rationale**: this is the only function allowed to invent fields; tagging discipline here is the difference between trusted and toxic CRM data.

### 7. Dedup against existing CRM

Per §6 of conventions: merge by `linkedin_url` > `email` > `phone` for person; `company_domain` for company. Call CRM's `GET /api/people?email=...` / `GET /api/companies?domain=...` to detect collisions. On collision: keep the higher-tier provenance, the more recent `freshness_date`. Log every merge in the run record's `dedup_merge_log`.

**Rationale**: the agent-app's push API does its own dedup, but the skill should pre-flight check so the user sees collision counts in the run summary, not after-the-fact.

### 8. Apply compliance filters

Per §7 of conventions: tag EU/UK contacts `gdpr_basis: legitimate-interest`. Strip `email_status: role-based` records to a sidecar list (don't drop them; they're useful for triangulation but never Tier-1 sends). Strip `phone_status: dnc` from the active list.

**Rationale**: bake compliance in; don't push it to function-3.

### 9. Push to CRM + emit run summary

Per §9 of conventions: push `company` + `person` + `interaction:research` (the run record). Provenance routing per §8.2: only `[user-provided]` and `[verified]` push as `company` / `person`; `[unverified]` go to the review queue as `interaction:research` with `#unverified #review-required`. Emit a one-screen run summary: filter set, candidate count, credits spent, records pushed, dedup merges, review-queue count, recommended next skill (`data-enrichment` for verifications + hooks, then `lead-scoring`).

**Rationale**: the run summary is the artifact the user actually reads; everything else is audit trail.

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: <api | manual-export | byo>
  source: <apollo-api | apollo-csv-export | byo-csv>
  filters: <reproducible filter object — source_query>
  cost:
    credits_used: <int>
    estimated_usd: <float>
    cap_usd: <float from SOURCING_RUN_USD_CAP>
  candidate_count: <int from discover()>
  pulled_count: <int>
  pushed_count:
    company: <int>
    person: <int>
    interaction_research: <int>
    review_queue: <int>
  dedup_merge_log:
    - { keep: <id>, merged: <id>, key: <linkedin_url | email | phone | domain>, reason: <freshness | provenance> }
  warnings: [<string>]
  next_skill_recommendation: <data-enrichment | lead-scoring | etc.>

leads:
  - lead_id: <uuid>
    # ... full Lead schema fields per conventions §1
    provenance_company: <verified | user-provided | unverified | hypothetical>
    provenance_person: <...>
    provenance_email: <...>
    provenance_signals: [<...>]
    source: apollo-api
    source_run_id: <run_id above>
    freshness_date: <ISO>
```

## Worked Example

> *All entities below are tagged `[hypothetical]` — fictional, illustrative.*

**User prompt**: "Pull leads from Apollo for our WorkflowDoc ICP. We have an Apollo API key. $20 budget."

**Step 1 — ICP grounding**: Read WorkflowDoc's ICP from `icp-definition` output:
- Firmographic: Series B SaaS, 100–300 emp, US, support team 5–15.
- Roles: Buyer = VP/Director of Support (`vp` / `director` seniority, `support` function); Champion = Support Operations Manager (`manager`, `support` / `ops`).
- Tech-stack signal: Zendesk **OR** Intercom in current stack.
- Trigger library: Series B funding < 90 days; VP of Support hire < 60 days; outsourced support added recently.
- Anti-ICP: companies <50 emp; >500 emp + entrenched Guru/Stonly contract.

**Step 2 — Mode**: `APOLLO_API_KEY` is set → API mode.

**Step 3 — Filter translation** (`source_query`):
```yaml
person_titles: ["VP of Support", "Director of Support", "Head of Customer Support",
                "Support Operations Manager", "CX Operations Manager"]
person_seniorities: [vp, director, manager]
person_departments: [support, ops]
person_locations: ["United States"]
organization_industries: ["computer software", "software development"]
organization_num_employees_ranges: ["101,200", "201,500"]
organization_latest_funding_stage: ["series_b"]
currently_using_any_of_technology_uids: ["zendesk", "intercom"]
not_organization_num_employees_ranges: ["1,10", "11,20", "21,50", "501,1000", "1001+"]
```

**Step 4 — discover() output**:
> "Search matches ~340 contacts across ~110 companies. Pulling all 340 ≈ $7 in Apollo credits. Sample of 5: Ada Bell [hypothetical] (VP of Support @ Stitchbox [hypothetical], San Francisco, [verified: apollo-api:run_2026-05-04T14:21]), ..."
> "Proceed with all 340?"

User: "Yes."

**Step 5 — pull()**: 340 records returned, ~$7 in credits, 0 rate-limit warnings.

**Step 6 — normalize**: 340 raw → 338 normalized (2 dropped: 1 missing company, 1 dupe within run). For one record:
```yaml
contact_name: "Ada Bell" [hypothetical]
linkedin_url: "https://linkedin.com/in/adabell-h" [verified: apollo-api:run_2026-05-04T14:21]
email: "ada@stitchbox.com" [verified: apollo-api]   # email_status will be set in data-enrichment, NOT here
email_status: unverified   # Apollo's "verified" flag is not trusted; downstream verifier decides.
title_raw: "VP of Customer Support"
title_normalized: "VP of Support"
seniority: vp
function: support
company: "Stitchbox" [hypothetical]
company_domain: "stitchbox.com" [verified: apollo-api]
company_size_band: "201-500"
company_industry_normalized: "computer software"
company_funding_stage: "series_b"
company_tech_stack: ["zendesk", "salesforce", "slack"] [verified: apollo-api]
signals:
  - type: tech-adoption
    source: apollo-api
    detail: "Stitchbox runs Zendesk + Intercom"
    date: 2026-04-12 [verified: apollo-api]
    evidence_url: <apollo organization detail URL>
    strength: medium
    half_life_days: 180
personalization_hook: null   # No citable hook from Apollo data alone — data-enrichment may add one.
provenance_company: verified
provenance_person: verified
provenance_email: verified
provenance_signals: [verified]
source: apollo-api
source_run_id: <uuid>
freshness_date: 2026-05-04
```

**Step 7 — dedup**: 12 collisions against existing CRM (all on `linkedin_url`). Of 12, 9 had higher-provenance existing records → keep existing; 3 had stale existing records → replace.

**Step 8 — compliance**: 0 EU contacts in this batch; 14 role-based emails (`support@`, `cx@`) routed to sidecar list, not active push.

**Step 9 — push + summary**:
```
WorkflowDoc Apollo Sourcing Run [hypothetical]
Run ID: run_2026-05-04_h7k...
Filter: Series B SaaS, 100–300 emp, US, Zendesk|Intercom, Support seniority VP+
Cost: 340 credits / ~$7.00 (cap $20)
Pulled: 340 → Normalized: 338 → Pushed: 326 (12 dedup merges)
  Companies: 110 (4 new, 106 enriched)
  Persons: 326 (314 new, 12 merged)
  Interaction:research: 1 (this run record) + 14 review-queue (provenance unverified)
Sidecar: 14 role-based emails (not pushed)
Recommended next: data-enrichment to verify emails + capture personalization hooks for Tier-1 sends
```

## Heuristics

- **Apollo's "verified" lies sometimes.** Treat any Apollo email as `email_status: unverified` until a real verifier confirms. The Apollo flag is a hint, not a verdict.
- **Title fuzziness scales by company size.** "VP of Growth" at a 50-person company isn't a real VP. Apollo's seniority filter doesn't fix this; cross-check with `company_size_band` when seniority looks suspicious.
- **Tier-1 sends deserve API mode.** Manual CSV exports go stale fast; if the run is feeding a high-effort outreach (function-3 cold-call, founder-led cold email), prefer fresh API pulls within 7 days.
- **Don't oversize the first run.** 500 records is plenty for ICP validation. Massive first pulls produce massive cleanup work and obscure whether the filters are good.
- **The filter set IS the deliverable.** Even when the skill produces 500 records, the *reusable* artifact is the `source_query` filter object — it's what lets the team replay, refine, and audit.
- **Apollo's tech-stack data is partial.** Some logos are deeply tagged, others aren't. Don't refuse to score a lead for missing tech-stack alone.
- **Catch-all domains masquerade as verified.** `@apple.com`, `@meta.com` etc. accept any email pattern. Mark `email_status: catch-all-domain`, not `verified`, regardless of what Apollo says.
- **Trigger decay is real.** "Raised Series B 18 months ago" is not a buying trigger; it's a stale fact. Funding-trigger half-life is ~12 months; hiring-trigger half-life is ~3 months. The signal date in Apollo is the *event* date, not the *index* date — an old event observed today is still old.
- **One contact per company is rarely enough.** Pull Buyer + Champion (and sometimes User) per company in the same run; the dedup logic merges within-company on linkedin_url anyway. Multi-thread coverage is the difference between "1 reply per 80 companies" and "1 reply per 30 companies."
- **Founder-led plays need different filter shapes.** When the user is the founder doing direct outreach to other founders, drop the Buyer / Champion split and search for `c_suite` seniority within the firmographic. Compose adjustments need to follow.
- **Quiet companies are not absent companies.** Apollo's coverage of stealth-stage and pre-Seed companies is thin. If the ICP's beachhead is early-stage, Apollo will undercount; pair with `lead-sourcing-web` (Crunchbase, AngelList, Product Hunt scraping) to fill the gap.

## Edge Cases

- **No ICP defined.** Procedure step 1 fails. Run with user-supplied criteria, mark output `confidence: low` and `provenance: [unverified — needs check]` aggressively. Recommend `icp-definition` as the prerequisite skill in the run summary.
- **Named-account list (no firmographic search).** User supplies 60 company names. Skip persona search at the firmographic level; instead, for each company: resolve to `organization_id`, then `mixed_people/search?organization_ids=[...]&person_titles=[...]`. Cost is per company (cheaper for named-account plays).
- **API mode but Apollo plan has no API access.** Apollo's free tier and lower paid tiers don't include API. Detect 403 on first call → fall back to manual export mode with no user prompt; warn that subsequent runs will save effort if the plan is upgraded.
- **PLG / self-serve product (sales motion).** Persona shifts toward end-users, not buyers. Adjust seniority filter to `manager` + `ic`. Note: function-1's `icp-definition` already encodes sales motion in its scorecard; check that field before running.
- **Multi-segment ICP.** Run one Apollo search per segment; tag each lead with the segment string. Don't merge filter sets — a single search across two segments produces noisy results in Apollo.
- **No verifier configured.** `email_status: unverified` everywhere; warn the user; recommend `data-enrichment` will be the gating skill before any outreach.
- **CSV export with weird columns (BYO mode).** Show inferred column mapping back to user; let them confirm or override; flag missing fields. Tag every row `[user-provided]` with `confidence: low`. Route through `data-enrichment` before scoring.
- **Apollo returns near-duplicates** (same person, two records with different IDs, common when Apollo merges sources). Dedup at normalize time within-run on `linkedin_url`; warn count in summary.
- **Trigger filters too tight, candidate count = 0.** Loosen one filter at a time and re-discover; don't blast wider all at once. Surface the filter responsible for each step's count change.
- **Off-platform company.** Target company isn't in Apollo (common for very early-stage, regional, or non-English-language firms). On named-account list, return per-company "not found in Apollo" entries; route those to `lead-sourcing-web` for manual research. Don't silently drop them.
- **Re-pull / refresh of a previous run.** User wants to re-source the same `source_query` 30 days later to catch new entrants. Replay the filter set verbatim; dedup against previous run's records (by `linkedin_url`); push only the *delta* + a refreshed run record.
- **Mixed-confidence batch.** A single run produces some `[verified]` records (API returned them clean) and some `[unverified — needs check]` records (agent inferred missing fields). Push them on different paths per §8.2 — verified to person/company, unverified to review queue. The run summary breaks down counts on both paths.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| API auth fails (401) | "Invalid API key" | Confirm key in env; re-prompt user; do NOT retry silently. |
| API rate limit (429) | "Too many requests" | Exponential backoff (5s, 15s, 45s, 120s); fail after 4 retries; resume from last successful page. |
| API returns 0 results | candidate_count=0 | Surface the filter object back to user; offer to relax 1 filter at a time (start with tech-stack, then funding stage, then geography); never fabricate to fill quota. |
| API returns 500/503 | 5xx | Retry with backoff (max 3); if still failing, fall through to manual export mode. |
| User cancels at quote step | discover() succeeds, no pull authorized | Persist the `source_query` filter object as an `interaction:research` record so the run isn't lost; user can replay later. |
| Apollo plan doesn't include API | 403 on first call | Switch to manual export mode silently; the user gets the same filter set in the form they can paste into Apollo's UI. |
| CSV ingestion: missing email column | normalize warns | Tag rows `email: null, email_status: unverified, [unverified — needs check]`; recommend `data-enrichment` (Hunter pattern + verifier) before push. |
| CSV ingestion: column-mapping ambiguous | normalize cannot infer | Show inferred mapping; require user confirm before proceeding. |
| Push to CRM fails (network / token) | 4xx/5xx from agentic-app | Persist run output to a local JSON in the workspace; retry on user request; never silently lose a sourcing run. |
| Cost cap hit mid-pull | partial pull | Stop, persist what was pulled with a `partial: true` flag; ask user to raise cap or accept partial run. |
| CSV encoding mismatch | normalize sees mojibake (`Ã©` for `é`) | Re-decode with UTF-8 → CP1252 → Latin-1 fallback chain; warn user; record `encoding_repair: true` on the run. |
| CSV column mapping ambiguous (two columns plausibly = `company`) | normalize stalls | Show inferred mapping with confidence score per column; require user confirm before proceeding; never silently choose. |
| Apollo region-blocked for the user (e.g. EU-restricted account) | 403 on `/mixed_people/search` for certain locations | Surface the restriction; recommend `lead-sourcing-linkedin` or `lead-sourcing-web` as the cross-region fallback. |
| Within-run duplicates (same person, two Apollo IDs) | normalize sees collisions on `linkedin_url` | Dedup at normalize time; keep the record with more fields populated; warn count in summary. |
| API returns email but `email_status: unverified` from Apollo's own check | data quality flag | Flow through to `email_status: unverified` in the Lead record; do NOT promote to `verified` based on Apollo's optimistic flag. |

## Pitfalls

- **Pulling without a quote.** "Just give me 4,000 leads" without `discover()` first burns credits and produces noisy lists.
- **Trusting Apollo's email verified flag.** It's a hint, not a verdict. Pair with a real verifier in `data-enrichment`.
- **Inventing personalization hooks.** "Saw your recent post on X" with no post URL is hallucination. Hooks ship with citable URLs or they don't ship.
- **Ignoring company-size-adjusted seniority.** "VP of Growth" at 50 people ≠ "VP of Growth" at 5,000.
- **Blasting role addresses.** `info@`, `sales@` should never be in the active push.
- **Filters too tight = 0 results, then loosened too aggressively.** Loosen one dimension at a time.
- **Skipping the run record.** Without the `interaction:research` run record, you lose cost-per-lead attribution downstream.
- **Treating Apollo as a single source of truth.** Cross-check funding stage with Crunchbase when the trigger is funding-driven.
- **Over-pulling on first run.** 500 records is enough to validate filter quality; 4,000 is a cleanup project.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per §8 of conventions and CLAUDE.md, every named entity (companies, people, emails, dates, dollar figures, signal evidence URLs) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. Without a live API at runtime, default to `[unverified — needs check]`. NEVER invent specifics like a Series B funding date or a tech-stack adoption to fill the signals array.
- **Silent credit overspend.** The cost cap is a hard stop. Surface every cap hit; never bypass.

## Verification

The run is real when: (a) the `source_query` filter object is reproducible — running it again returns the same candidates ± new entrants; (b) every record carries provenance tags on every named field; (c) the run record's costs match Apollo's billing dashboard ± rounding; (d) `data-enrichment` and `lead-scoring` can consume the records without source-specific glue; (e) `[unverified — needs check]` records landed in the review queue, not the active prospect list.

Negative test: pose the run output to a colleague who didn't watch the run. Can they audit it? Can they tell *which* fields came from Apollo, *which* from agent inference, *which* from the user? If no, provenance discipline failed — re-run.

## Done Criteria

1. Mode determined and stated in run record (api / manual-export / byo).
2. `source_query` filter object stored and reproducible.
3. `discover()` quote shown to user and explicit authorization received before any `pull()`.
4. Every Lead carries provenance tags on identity, person, company, email, signals (no untagged named fields).
5. Dedup performed against existing CRM (linkedin_url > email > phone > domain); merges logged.
6. Compliance filters applied (GDPR EU tag; role-address sidecar; DNC strip).
7. `[unverified — needs check]` records routed to review queue, NOT the active person/company push.
8. Run summary one-screen, recommends next skill (`data-enrichment` typically).
9. Cost stayed under `SOURCING_RUN_USD_CAP` (or explicit override logged).

## Eval Cases

### Case 1 — full API mode, ICP grounded

Input: ICP from `icp-definition` (Series B SaaS, 100–300 emp, support team), `APOLLO_API_KEY` set, $20 cap, named-account list of 30 companies.

Expected output shape: run record with `mode: api`, `source: apollo-api`, candidate_count ≈ 60–120 (2–4 contacts per company), pulled_count = candidate_count, all leads provenance `[verified: apollo-api]`, 0 review-queue, recommended next: `data-enrichment`.

### Case 2 — manual export mode, ICP grounded

Input: same ICP, no API key, user has Apollo seat, drops a CSV after running filters in UI.

Expected output shape: run record with `mode: manual-export`, `source: apollo-csv-export`, all leads provenance `[user-provided]`, schema repair log shows column-mapping inference, recommended next: `data-enrichment` (note: emails are user-provided not API-verified, so verifier is mandatory before outreach).

### Case 3 — BYO mode, no ICP

Input: user dropped a 200-row CSV from a friend's CRM; no `icp-definition` run.

Expected output shape: run record with `mode: byo`, `source: byo-csv`, `confidence: low`, `ICP-ungrounded: true`, all leads provenance `[user-provided]` with `confidence: low`, 60% routed to review queue (missing required fields), recommended next: `icp-definition` first, then `data-enrichment`, then `lead-scoring`.

### Case 4 — partial pull, cost-cap hit

Input: ICP grounded, named-account list of 200 companies, $10 cap, API mode. `discover()` estimates ~$15 for full pull (avg 1.8 contacts per company at 1 credit each).

Expected output shape: skill surfaces the cap conflict at `discover()` time (`Estimated $15 exceeds $10 cap`), offers user three options: raise cap, accept partial run capped at first 130 companies, or re-scope. On user choosing partial: pulls 130 companies' worth of contacts (~$10), persists `partial: true` and `partial_companies_remaining: 70` on the run record, recommends raising cap or running a follow-up batch tomorrow. The 70 remaining companies are NOT silently dropped — they're listed in the run record as `pending_pull` for replay.

## Guardrails

### Provenance (anti-fabrication)

Per §8 of conventions: every named entity carries one of `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Tool-grounding rule applies: no API → all external-fact assertions default to `[unverified — needs check]`. Worked-example fictional entities tagged inline at first use.

Function-2-specific risk: sourcing skills can fabricate entire companies / contacts in ways function-1 can't. Mitigation: API mode emits raw response IDs + API call URL with `[verified: apollo-api:run_id]`; manual export emits `[user-provided]`; BYO emits `[user-provided]` with `confidence: low` until enrichment promotes individual fields. Personalization hooks ship `[verified: <source-url>]` or NOT AT ALL — agent never invents a "saw your post on..." opener.

### Evidence

Every signal entry has: source name, ISO date, permalink, strength label. Missing any → tag the signal `[unverified — needs check]` and exclude from `lead-scoring`'s signal weighting.

### Scope

This skill produces a list. It does NOT score (that's `lead-scoring`), verify emails (that's `data-enrichment`), enrich phones (also `data-enrichment`), or write outreach (function-3). Avoid scope creep — emit recommendations to the next skill rather than doing its job.

### Framing

The run record's `relevance` text and the user-facing summary use plain operational language ("pulled 326 leads, 12 dedup merges, $7 spent, 14 routed to review"). No marketing voice; this is internal SDR ops.

### Bias

The Apollo industry taxonomy reflects Apollo's view of the market. Don't treat its industry tags as ground truth — record raw + normalized values both, so downstream analysis can trace bias.

### Ethics

Compliance baseline (§7 of conventions) is non-negotiable: no LinkedIn direct scraping, GDPR opt-out for EU contacts, role-addresses never Tier-1, DNC respected.

### Freshness

All data carries `freshness_date`. Records older than the half-life rules in conventions §6 are flagged for re-pull on next run. Don't push stale data into outreach.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| List pulled, emails need verifying + hooks need capturing | `data-enrichment` | Lead records (full schema), `source_run_id` |
| List ready for outreach prioritization | `lead-scoring` | Enriched Lead records + ICP scorecard |
| Apollo wasn't right tool for this trigger play | `lead-sourcing-linkedin` (role/trigger) or `lead-sourcing-web` (job-post / press) | Filter set + un-found accounts |
| User wants Apollo + Hunter + verifier in one workflow | `lead-sourcing-clay` | Same ICP filters, Clay-translated |
| ICP not grounded; output flagged ungrounded | `icp-definition` | Hypothesis + product description |
| Run produced 0 results despite filter loosening | `market-research` (re-evaluate beachhead) | Current filter set + 0-result evidence |
| Active campaign needs to monitor pull-quality over time | `campaign-management` (function-3, future) | `source_run_id` + cost-per-lead targets |

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

Per §8.2 of conventions:

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
- BYO records with confidence:low and missing required fields — push `interaction:research` with `#byo-pending-enrichment` tag; defer `person` push to after `data-enrichment`.
- `[unverified — needs check]` — see provenance routing above; never as person/company.
- `[hypothetical]` — never.
- Run flagged "ICP-ungrounded" — push the run record but tag it `#icp-ungrounded` so downstream skills downweight; defer `person` push until ICP exists or user explicitly overrides.
