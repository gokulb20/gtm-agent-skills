---
name: lead-sourcing-linkedin
description: Source leads via LinkedIn Sales Navigator by translating role-based and trigger-based ICP criteria (recent hires, leadership changes, "years in current company" filters) into Sales Nav search URLs and filter recipes, executing via session-based tools (PhantomBuster, HeyReach) or manual CSV export, and normalizing to the function-2 Lead schema with strict ToS-compliance. Use when the play is role/trigger-driven (recent VP hires, leadership shifts, active LinkedIn presence), when Sales Nav surfaces signals Apollo can't see, or when LinkedIn URL is required as the dedup key.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, lead-sourcing, linkedin, sales-navigator, function-2]
related_skills:
  - icp-definition
  - lead-sourcing-apollo
  - lead-sourcing-clay
  - lead-sourcing-web
  - data-enrichment
  - lead-scoring
inputs_required:
  - icp-scorecard-from-icp-definition
  - linkedin-sales-nav-seat-or-session-tool
  - role-or-trigger-criteria
  - cost-budget-credits-or-dollar
  - run-purpose-tag
deliverables:
  - sales-nav-search-url-and-filter-recipe
  - normalized-lead-records-with-provenance-tags
  - phantombuster-or-heyreach-job-spec
  - cost-and-coverage-report
  - sourcing-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Lead Sourcing — LinkedIn

Source leads via LinkedIn Sales Navigator's role- and trigger-based search filters, with strict ToS compliance. Emit Sales Nav URLs + filter recipes, execute via session-based tools (PhantomBuster, HeyReach) or manual CSV export, normalize to the function-2 Lead schema. LinkedIn URL is treated as the primary person dedup key.

> *Worked example uses MetricMojo [hypothetical] (fictional); procedure is vertical-agnostic. Shared rules in `function-2-skills/function-2-conventions.md`.*

## Purpose

Sales Navigator is the source for fresh role and trigger signals — recent hires, leadership shifts, currently-active LinkedIn presence. Apollo lags LinkedIn 30–90 days on people moves; for trigger-based plays this skill is sharper. Unlike Apollo, LinkedIn has **no public Search API**: every operating mode either emits a search URL the user runs in Sales Nav, runs a job through a session-based tool, or ingests a CSV. Direct scraping is forbidden by LinkedIn's User Agreement; the skill MUST refuse it.

## When to Use

- "Find VPs of Marketing who started their current role in the last 90 days."
- "Who at our target accounts recently posted on LinkedIn about [topic]?"
- "Source Sales leaders at Series B SaaS — Sales Nav has fresher data than Apollo."
- "We have a Sales Nav seat — give me the search filters to run."
- "I exported 500 contacts from Sales Nav; ingest and push to CRM."
- Trigger-based plays — leadership change, recent posts about a pain topic, hiring spikes visible only on profiles.
- Pre-outreach when LinkedIn URL is required (cold-email keys personalization on LinkedIn handle).

## Inputs Required

1. **ICP scorecard** from `icp-definition`. Role map and trigger library are the primary inputs.
2. **LinkedIn access** — one of: Sales Nav seat / `PHANTOMBUSTER_API_KEY` / `HEYREACH_API_KEY` / Sales Nav CSV / BYO list. No direct LinkedIn API exists.
3. **Role or trigger criteria** — e.g. "VP Marketing started in current role <90d" or "Director of Engineering posting about Kubernetes."
4. **Cost budget** — default `SOURCING_RUN_USD_CAP=$25`. Sales Nav itself is seat-based; Agent reads vendor docs at runtime; pricing changes — verify live before any spend.
5. **Run purpose tag** — short string for cost attribution + replay.
6. (Optional) Geographic/persona overrides on top of ICP.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | API-substitute (PhantomBuster/HeyReach) / Manual (Sales Nav UI export) / BYO (CSV) |
| **Direct scraping** | REFUSED. Forbidden by LinkedIn ToS. Hard rule. |
| **Primary merge key** | `linkedin_url` — highest-confidence in this skill |
| **Sales Nav UI cap** | 25 leads/page; 1,000 results per search; daily search limits per session |
| **Trigger filters** | "Years in Current Position <1 year", "Posted on LinkedIn past 30d", "Changed jobs past 90d", "Company headcount growth >10%" |
| **Boolean keyword search** | Supports AND OR NOT and quotes — useful for narrow plays |
| **Email coverage** | Sales Nav rarely surfaces email → `data-enrichment` is mandatory next step |
| **PhantomBuster pacing** | 50–100 profiles/day per session is "safe"; aggressive use risks account flag |
| **Privacy-mode profiles** | Returned as "LinkedIn Member" — count, don't push as persons |
| **Compliance** | Public-profile content only; session-based tools acceptable; direct-scraping refused |

## Procedure

### 1. Confirm ICP grounding
Read ICP scorecard from `icp-definition`. Extract role map (titles + seniority) and trigger library (recency-sensitive). If absent → flag ungrounded.

### 2. Determine mode
Sales Nav seat + PhantomBuster/HeyReach key → API-substitute mode. Else seat alone → manual mode (output URL). Else CSV → BYO. Else → URL + recipe only. Direct-scraping requested → REFUSE.

### 3. Translate ICP → Sales Nav filter set
Map role titles → `Title` (with Boolean variants); seniority → `Seniority Level`; function → `Function`; geography → `Geography`; industry → `Industry`; size → `Company Headcount`; recent-role trigger → `Years in Current Position: <1 year`; active-poster trigger → `Spotlights: Posted on LinkedIn past 30d`; company-growth → `Company Headcount Growth >10%`. Output: Sales Nav search URL + human-readable recipe.

### 4. Pre-flight: discover()
For API-substitute mode: small-batch PhantomBuster job (50 profiles) returns count + cost. For manual: user pastes URL into UI, reports result count Sales Nav displays. Surface count, cost, sample of 5 profiles. Wait for explicit authorization.

### 5. Execute (or hand off)
API-substitute: submit Phantom; collect CSV; ingest. Manual: user runs search, exports up to 25 leads/page. BYO: user uploads existing CSV.

### 6. Normalize to Lead schema
Map fields per conventions §1. LinkedIn URL is primary identity; promote it to top of merge-key priority. Stamp provenance per source path. Note: email field will be `null`/`unverified` for almost all records — this is expected.

### 7. Dedup + compliance + push
LinkedIn URL doubled in priority — it IS the merge key. Apply compliance (§7 of conventions): GDPR EU tagging; ToS-compliance reminder in run record. Push per §9. Run summary: filter URL, profile count, dedup, **trigger breakdown**, recommends `data-enrichment` MANDATORY next.

## Output Format

- Sales Nav search URL (encoded with all filter params — reproducible)
- Human-readable filter recipe
- Lead records (full schema, LinkedIn URL high-confidence, email typically absent)
- Run record: filter URL, recipe, profile count, cost, dedup log, trigger breakdown, ToS-compliance note, next-skill recommendation
- Review queue: privacy-mode profiles + ambiguous records as `interaction:research`
- (For manual mode) PhantomBuster / HeyReach job spec ready-to-paste

## Done Criteria

1. Mode determined and stated; direct-scraping requests REFUSED.
2. Sales Nav search URL + filter recipe stored and reproducible.
3. `discover()` count surfaced; user authorization received before pull.
4. Every Lead carries provenance tags; LinkedIn URL specifically `[verified]`; email correctly tagged `unverified` where absent.
5. Dedup performed; LinkedIn URL is primary merge key.
6. Compliance filters applied; ToS-compliance reminder in run record.
7. `[unverified — needs check]` records (privacy-mode, partial) routed to review queue, NOT active push.
8. Run summary one-screen with trigger breakdown; recommends `data-enrichment` next; cost stayed under cap.

## Pitfalls

- **Direct LinkedIn scraping.** Forbidden by ToS. Account-suspension and legal risk. Hard rule — REFUSE.
- **Promoting Sales Nav recency past freshness.** "Started role 5 days ago" may be 5 weeks ago in reality.
- **Skipping `data-enrichment`.** LinkedIn rarely provides email; outreach without enrichment will mostly bounce.
- **Treating Sales Nav as a stable database.** It's a real-time index; same search next month returns different results.
- **Over-trusting active-poster filter.** Surfaces engagement, not buying intent. Pair with other triggers.
- **Inventing LinkedIn URLs.** Profile URLs follow predictable patterns but can be fabricated; never invent.
- **Ignoring session-safety.** Aggressive PhantomBuster usage flags accounts; pace 50–100 profiles/day per session.
- **Mistaking "LinkedIn Member" privacy-mode profiles for skip-able.** Surface count; don't suppress.
- **Mass-connection-request abuse.** Stay out of outreach (function-3); document for context.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, LinkedIn URLs, dates, signal evidence) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No Sales Nav export → default to `[unverified — needs check]`. NEVER invent a LinkedIn URL or a "started 90d ago" date to fill the trigger field.
- **Silent automation overspend.** PhantomBuster bills per profile; cap is hard stop.

## Verification

The run is real when: the `sales_nav_search_url` resolves to the same filter set on replay; every record's LinkedIn URL is canonical (`/in/<handle>`, no tracking params); provenance tags accurately reflect the source path; `data-enrichment` is recommended before any outreach run; privacy-mode and partial profiles routed to review queue.

## Example

**User prompt:** "Find VPs of Marketing at Series B SaaS in the US who started their current role in last 90 days. PhantomBuster set up. We're pitching MetricMojo [hypothetical]. $20 budget [hypothetical]."
**What should happen:** Read ICP. Translate to Sales Nav filters (Title VP Marketing, Seniority VP, Function Marketing, Geography US, Industry Computer Software, Company Headcount 51-500, Spotlights "Changed jobs past 90d", Years in Current Position <1 year). Output search URL. PhantomBuster sample (50) returns ~310 total [hypothetical]. Agent reads vendor docs at runtime; pricing changes — verify live before any spend. User confirms $20 budget [hypothetical] is sufficient. Confirm. Materialize 308 [hypothetical] → normalize 305 [hypothetical] (3 dropped [hypothetical]). Dedup against CRM (14 merges [hypothetical]). Push 291 persons [hypothetical] + 95 companies [hypothetical] + 1 run interaction [hypothetical]. Trigger breakdown: 305 recent-role-change [hypothetical] / 91 active-posters [hypothetical] / 47 company-growth [hypothetical]. Recommend `data-enrichment` (mandatory — emails absent).

**User prompt:** "I have a Sales Nav seat but no automation tools. Give me the search to run myself."
**What should happen:** Manual mode. Skill outputs reproducible Sales Nav URL with all encoded filters + a step-by-step recipe (which dropdowns to set, which Spotlights to enable, exact Boolean keyword string). Notes the 25-leads-per-page UI cap and recommends a maximum batch of 100 profiles before importing back. After user uploads CSV, skill normalizes with `[user-provided]` provenance for non-LinkedIn-export columns and `[verified: linkedin-sales-nav]` for native fields. Recommends `data-enrichment`.

**User prompt:** "Just scrape LinkedIn directly for VPs of Engineering at FAANG."
**What should happen:** REFUSE. Surface ToS explanation: direct scraping violates LinkedIn User Agreement, risks account suspension, and creates legal exposure. Recommend Sales Nav (use `Industry: Computer Software, Internet, Information Technology Services`, geography filters, target-account list of FAANG companies) executed via PhantomBuster's session-based Sales Nav Search Export Phantom. Log the refusal as an `interaction:research` for audit. Produce no records.

## Linked Skills

- Profiles pulled, emails missing → `data-enrichment` (mandatory before outreach)
- Trigger play needs firmographic depth → `lead-sourcing-apollo`
- Multi-source orchestration → `lead-sourcing-clay`
- Trigger invisible to LinkedIn (job posts, RFPs) → `lead-sourcing-web`
- ICP not grounded → `icp-definition`
- Ready for outreach prioritization → `lead-scoring` (after enrichment)

## Push to CRM

After pulling and normalizing, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company in pull | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-linkedin #icp-tier-pending"` |
| Each unique person (verified or user-provided) | `person` | `contactName`, `contactTitle`, `contactLinkedIn` (the canonical linkedin_url), `contactEmail` (typically absent — let data-enrichment fill) |
| Run record (search URL, filter recipe, trigger breakdown) | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#linkedin-sourcing-run #function-2"` |
| Privacy-mode / partial profiles | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #lead-sourcing-linkedin"`; never `company`/`person` |

`lead-scoring` writes `score` + `priority` + tier tags onto the `person` record later. This skill does NOT set `score` on push.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
PHANTOMBUSTER_API_KEY=   # or HEYREACH_API_KEY
SOURCING_RUN_USD_CAP=25
SOURCING_RUN_RECORD_CAP=2000
```

### Source tag

`source: "skill:lead-sourcing-linkedin:v2.0.0"`

### Example push (verified person + company)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Brightline AI",
    "website": "https://brightline-ai.com",
    "industry": "Computer Software",
    "tags": "#sourced-linkedin #icp-tier-pending #saas #series-b #recent-vp-hire",
    "contactName": "Jordan Reyes",
    "contactTitle": "VP of Marketing",
    "contactLinkedIn": "https://linkedin.com/in/jordan-reyes-marketing",
    "relevance": "Sourced from Sales Nav via PhantomBuster run lk7_2026-05-04. Filter: VP Marketing, Series B SaaS, US, role started <90d. Provenance: linkedin_url [verified: phantombuster], person [verified: phantombuster], email [unverified — needs check] (absent from Sales Nav export). Trigger: leadership-change (started 2026-03-08 = 66d ago, strong). Recommend data-enrichment for email + hook before outreach.",
    "source": "skill:lead-sourcing-linkedin:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#linkedin-sourcing-run #function-2",
    "relevance": "LinkedIn sourcing run lk7_2026-05-04. Mode: PhantomBuster API-substitute. Sales Nav URL: <encoded url>. Filter: VP Marketing, Series B SaaS, US, role started <90d. Cost: $6.16 / cap $20. Pulled 308 → Normalized 305 → Pushed 291 (14 dedup merges). 0 review-queue. Trigger breakdown: 305 recent-role-change / 91 active-posters / 47 company-growth. ToS-compliance reminder: Sales Nav public-profile data only. Recommended next: data-enrichment (mandatory — emails absent).",
    "source": "skill:lead-sourcing-linkedin:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §8.2:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping. Note: email will typically be `[unverified]` even on `[verified]` LinkedIn-source records — that's expected. |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #lead-sourcing-linkedin` tags. Never as `company` / `person`. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified push (privacy-mode):

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #lead-sourcing-linkedin #privacy-mode",
    "relevance": "30 profiles in lk7_2026-05-04 returned as 'LinkedIn Member' (privacy-mode) — no name, no company, no usable identity. Counted in run but not pushed as persons. Recommend tighter filters or alternate sourcing.",
    "source": "skill:lead-sourcing-linkedin:v2.0.0"
  }'
```

### When NOT to push

- Run that returned 0 profiles — push run record, no person/company.
- Direct-scraping refused — log refusal as `interaction:research` for audit; produce no records.
- Privacy-mode profiles — see provenance routing.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
- Run flagged "ICP-ungrounded" — push run record tagged `#icp-ungrounded`; defer person push.
- Account-safety warning from automation tool — abort push; surface; recommend pause.
