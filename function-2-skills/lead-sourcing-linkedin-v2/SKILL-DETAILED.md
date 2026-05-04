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

Source leads via LinkedIn Sales Navigator's role- and trigger-based search filters, with strict ToS compliance. The skill emits Sales Nav search URLs + filter recipes the user (or a session-based tool like PhantomBuster / HeyReach) can execute, then normalizes the resulting CSV into the function-2 Lead schema. LinkedIn URL is treated as the primary person dedup key — making this skill the highest-quality source for any field that downstream skills will key on.

> *The worked example uses a fictional product (MetricMojo) for illustration. The Sales Nav filter patterns, ToS-compliance rules, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Lead schema, source adapter contract, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`. This skill assumes it.*

## Purpose

Sales Navigator is the source for fresh role and trigger signals — recent hires, leadership shifts, promotion patterns, currently-active LinkedIn presence. Apollo lags LinkedIn by 30–90 days on people moves; for trigger-based plays this skill is sharper. Unlike Apollo, LinkedIn has **no public Search API**: every operating mode here either emits a search URL the user runs in the Sales Nav UI, runs a job through a session-based tool (PhantomBuster, HeyReach) that uses the user's own LinkedIn session, or ingests a CSV the user already exported. Direct scraping is forbidden by LinkedIn's User Agreement and the skill MUST refuse it.

## When to Use

- "Find VPs of Marketing who started their current role in the last 90 days."
- "Who at our target accounts recently posted on LinkedIn about [topic]?"
- "Source a list of Sales leaders at Series B SaaS companies — Sales Nav has fresher data than Apollo."
- "We have a Sales Nav seat — give me the search filters to run."
- "I exported 500 contacts from Sales Nav; ingest and push to CRM."
- Trigger-based plays — leadership change, recent posts about a pain topic, hiring spikes visible only on profiles.
- Pre-outreach when LinkedIn URL is required (cold-email skill keys personalization on LinkedIn handle).

### Do NOT use this skill when

- The play is purely firmographic with no role-freshness need — `lead-sourcing-apollo` is cheaper and similar-quality on stable contacts.
- Trigger is invisible to LinkedIn (job-board postings, RFP issuance, regional press) — `lead-sourcing-web`.
- The user has neither a Sales Nav seat nor a CSV nor a PhantomBuster/HeyReach setup — degrade gracefully (output search URL only) rather than fail.
- The user wants direct LinkedIn scraping — refuse. Forbidden by ToS; legal and account-suspension risk. Recommend Sales Nav + PhantomBuster session-mode instead.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | ICP scorecard | yes (or flag ungrounded) | `icp-definition-v2` output | Role map and trigger library are the primary inputs from ICP. |
| 2 | LinkedIn access | one of: Sales Nav seat / PhantomBuster API key / HeyReach API key / Sales Nav CSV / BYO list | env or user input | Determines mode (no direct LinkedIn API exists). |
| 3 | Role or trigger criteria | yes | user / ICP | E.g. "VP of Marketing started in current role <90d" or "Director of Engineering posted about Kubernetes in last 30d." |
| 4 | Cost budget | yes (default `SOURCING_RUN_USD_CAP=$25`) | env or user | Sales Nav itself is seat-based (no per-record cost); PhantomBuster ~$0.02/profile; HeyReach is subscription. |
| 5 | Run purpose tag | yes | user | Stamped on every record's `source_run_id`. |
| 6 | Geographic / persona overrides (optional) | no | user | Applied on top of ICP. |

### Fallback intake script

> "LinkedIn has no public search API, so I work in three modes: I emit a Sales Nav search URL + filter recipe you (or PhantomBuster / HeyReach with your session) can run, OR I ingest a CSV you've already exported.
>
> Which do you have? Sales Nav seat? PhantomBuster / HeyReach? CSV? Tell me about your access and I'll degrade gracefully — at minimum I can give you the filter recipe.
>
> What role / trigger criteria are we hunting? (e.g. 'VP Sales started in current role <90d' or 'Director of Engineering posting about Kubernetes')."

### Input validation rules

- ICP firmographic absent → `confidence: low`; default provenance `[unverified — needs check]`; flag run as ICP-ungrounded.
- No Sales Nav seat AND no PhantomBuster/HeyReach AND no CSV → produce search URL + filter recipe only; refuse to fabricate records.
- Direct-scraping requested → REFUSE. Output: ToS explanation + recommended session-based tool path.
- "Years in current company" filter requested but no Sales Nav seat → unobtainable signal in standard LinkedIn (free); refuse with explanation.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Trigger Events for Sales Success** (2009) | Craig Elias | LinkedIn is the trigger-richest source — leadership changes, role tenure, hiring sprees are visible in profiles before press. The skill prioritizes triggers over firmographic stability when ranking searches. |
| **Predictable Revenue** (2011) | Aaron Ross & Marylou Tyler | ICP-driven outbound; persona work translated into Sales Nav role + seniority filters. |
| **Years-in-current-company trigger** (industry-standard, Sales Nav UI-encoded) | n/a — convention since Sales Nav 2014 release | The "Years in Current Company: <1 year" filter is the cleanest LinkedIn-native trigger for "recent move" plays. House convention: pair with "company funding stage" or "hire announcement search" for trigger-amplification. |
| **LinkedIn ToS compliance posture** (statute / contract) | LinkedIn User Agreement (current version) | Direct-scraping forbidden. Session-based tools using user's own credentials are acceptable. The skill encodes this as a hard rule, not a guideline. |

## Tools and Sources

### Primary

| Tool | Mode | Purpose |
|---|---|---|
| LinkedIn Sales Navigator (UI) | Manual | User runs search, exports CSV. The richest filter UX. |
| PhantomBuster (Sales Nav Search Export Phantom) | API-substitute | Runs Sales Nav search via user's session; outputs CSV. Charged per profile. |
| HeyReach (LinkedIn Profile Scraper) | API-substitute | Similar; subscription-based. |
| Sales Nav CSV (BYO) | BYO | User ran search in UI, drops CSV; skill normalizes. |

### Secondary

| Tool | Notes |
|---|---|
| LinkedIn URL list (BYO) | A list of profile URLs, no other data; PhantomBuster's "Profile Scraper" Phantom enriches one-by-one. |
| Apify LinkedIn scraper | An option, but legal posture is unclear — recommend Sales Nav + PhantomBuster instead. |

### Source priority rule

For any field: **Sales Nav search export within last 7 days** > **PhantomBuster session-based export within 14 days** > **BYO CSV with `[user-provided]` tag** > **agent inference (`[unverified — needs check]`)**. NEVER scrape LinkedIn directly. NEVER fabricate a LinkedIn URL.

### Sales Nav-specific filter knowledge

- **"Years in Current Company" / "Years in Current Position"** — the cleanest trigger-recency filters Sales Nav offers. `<1 year` for "just changed roles."
- **"Posted on LinkedIn"** — date-bounded post activity filter; surfaces actively-engaged contacts (cold outreach to active LinkedIn users replies higher).
- **"Senior Hire Trends"** — Sales Nav surfaces leadership-change patterns at the company level; pair with role filter for trigger-amplification.
- **"Spotlights"** filters: "Changed jobs in past 90 days," "Posted on LinkedIn in past 30 days," "Mentioned in the news" — all trigger-rich and Sales Nav-exclusive.
- **"Company Headcount Growth"** — surfaces companies expanding, often pair with role filter to find new hires at growing companies.
- **Boolean search in `Keywords`** — supports `AND OR NOT` and quotes; powerful for narrow plays ("Director of Engineering" AND ("Kubernetes" OR "k8s") NOT "intern").
- **Account list export** — Sales Nav's company-list feature exports up to 1,000 accounts at a time; useful for reverse-targeting once you have a named-account list.

## Procedure

### 1. Confirm ICP grounding

Read ICP scorecard from `icp-definition`. Extract role map (especially title patterns + seniority) and trigger library (especially the recency-sensitive triggers). If absent → flag ungrounded.

### 2. Determine mode

Sales Nav seat AND PhantomBuster/HeyReach API key → API-substitute mode (full automation). Else seat alone → manual mode (output search URL). Else CSV → BYO mode. Else → URL + recipe only. Direct-scraping requested → refuse with explanation.

### 3. Translate ICP → Sales Nav filter set

Map field-by-field:
- ICP role titles → Sales Nav `Title` (with Boolean operators for variants).
- ICP seniority → `Seniority Level`.
- ICP function → `Function`.
- ICP geography → `Geography` (city / state / country).
- ICP industry → `Industry`.
- ICP company size → `Company Headcount`.
- Trigger: recent role change → `Years in Current Position: Less than 1 year`.
- Trigger: active LinkedIn presence → `Spotlights: Posted on LinkedIn in past 30 days`.
- Trigger: leadership change at company → `Spotlights: Changed jobs in past 90 days`.
- Trigger: company expansion → `Company Headcount Growth: > 10%`.
- Anti-ICP exclusions → `Industry: NOT [...]`, `Title: NOT intern`.

Output: a reproducible Sales Nav search URL (Sales Nav encodes filters in URL params) + a human-readable filter recipe. **Rationale**: the URL is the audit handle; the recipe is the user-facing instruction set.

### 4. Pre-flight: discover()

For API-substitute mode (PhantomBuster): submit a small-batch job (50 profiles) to validate the search; report back actual count and per-profile cost. For manual mode: instruct user to paste URL into Sales Nav, report the result count Sales Nav displays. Surface to user:

```
Sales Nav search matches ~310 contacts at ~95 companies.
PhantomBuster batch cost: 310 × $0.02 = $6.20.
Sample of 5 profiles: [list with [verified: linkedin-sales-nav] tags]
Proceed with [310] [50 sample first] [refine filters]?
```

### 5. Execute (or hand off)

- **API-substitute mode**: submit PhantomBuster / HeyReach Phantom; collect CSV when done; ingest.
- **Manual mode**: user runs search, exports up to 25 leads/page (Sales Nav UI cap); submits CSV when ready.
- **BYO mode**: user uploads existing CSV.

### 6. Normalize to Lead schema

For each profile:
- Map fields per conventions §1.
- LinkedIn URL is the primary identity field — promote it to top of merge-key priority.
- Stamp provenance: `[verified: linkedin-sales-nav:run_<id>]` for fields the export contained; `[verified: phantombuster:run_<id>]` for PhantomBuster-pulled fields; `[user-provided]` for BYO; `[unverified — needs check]` for inferred (e.g. parsing email from a LinkedIn signal that doesn't surface email directly).
- Note: Sales Nav export does NOT include email by default. Email status will be `unverified` for almost all records — `data-enrichment` is the mandatory next step before outreach.

**Rationale**: LinkedIn data is high-confidence on identity (LinkedIn URL, name, title, company) but thin on contactable fields (email, phone). Provenance accurately reflects this.

### 7. Dedup against existing CRM

Per §6 of conventions, but with `linkedin_url` doubled in priority — it is THE merge key for this skill. Person-level merges are common because LinkedIn is the most-authoritative source.

### 8. Apply compliance filters

Per §7 of conventions: GDPR EU tagging; ToS reminder in run record (only public-profile content used); flag any `personal-email` mismatches; `phone_status` typically `unverified` (LinkedIn rarely surfaces phone).

### 9. Push + emit run summary

Push per §9. Run summary highlights: filter URL, profile count, dedup merges, role-recency distribution (a Sales Nav-specific signal — "of the 273 records, 180 changed roles in last 90d"), recommended next skill (`data-enrichment` is mandatory before outreach because emails are absent or unverified).

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: <api-substitute (phantombuster|heyreach) | manual | byo>
  source: linkedin-sales-nav-csv | phantombuster | heyreach | byo-csv
  sales_nav_search_url: <full URL with filter params>
  sales_nav_filter_recipe: <human-readable filter description>
  cost:
    tool_cost_usd: <float>
    cap_usd: <float>
  candidate_count: <int>
  pulled_count: <int>
  pushed_count:
    company: <int>
    person: <int>
    interaction_research: <int>
    review_queue: <int>
  trigger_breakdown:
    recent_role_change: <int>
    active_poster: <int>
    company_growth: <int>
  warnings: [<string>]
  next_skill_recommendation: data-enrichment

leads:
  - lead_id: <uuid>
    linkedin_url: <primary identity, [verified: linkedin-sales-nav]>
    contact_name, title, function, seniority: <[verified: linkedin-sales-nav]>
    email: null   # Sales Nav export rarely includes
    email_status: unverified
    company, company_domain: <[verified: linkedin-sales-nav]>
    signals:
      - type: leadership-change
        source: linkedin-sales-nav
        date: <ISO from "started in current role" field>
        evidence_url: <linkedin profile URL>
        strength: strong
        half_life_days: 90
    personalization_hook: null   # data-enrichment will capture
    source: linkedin-sales-nav-csv | phantombuster | ...
    source_run_id: <run_id>
    freshness_date: <ISO>
```

## Worked Example

> *All entities below are tagged `[hypothetical]` — fictional, illustrative.*

**User prompt**: "Find VPs of Marketing at Series B SaaS companies in the US who started their current role in the last 90 days. Use our PhantomBuster setup. We're pitching MetricMojo [hypothetical]. $20 budget."

**Step 1 — ICP grounding**: MetricMojo ICP from `icp-definition`:
- Firmographic: Series B SaaS, 100–500 emp, US.
- Roles: Buyer = VP Marketing, Champion = Marketing Ops Manager.
- Trigger: VP Marketing hire <90d (high-strength); company recently raised Series B (medium); marketing-ops tech adoption growing.
- Anti-ICP: agencies, consulting firms, <50 emp.

**Step 2 — Mode**: Sales Nav seat + PhantomBuster API key → API-substitute mode.

**Step 3 — Filter translation**:
```
Title: ("VP of Marketing" OR "Vice President, Marketing" OR "Head of Marketing")
Seniority Level: VP
Function: Marketing
Geography: United States
Industry: Computer Software, Software Development, SaaS
Company Headcount: 51-200, 201-500
Spotlights: Changed jobs in past 90 days
Years in Current Position: Less than 1 year
NOT Industry: Marketing & Advertising (excludes agencies)
```

Sales Nav URL: `https://www.linkedin.com/sales/search/people?keywords=...&...&filters=...` (full encoded URL stored as `sales_nav_search_url`).

**Step 4 — discover()**:
PhantomBuster sample run (50 profiles) returns:
> "Sales Nav search matches ~310 contacts at ~95 companies. Sample of 5: [list]
> PhantomBuster batch cost for 310: $6.20. Cap: $20. Proceed?"

User: "Yes."

**Step 5 — Execute**: PhantomBuster Phantom completes in ~22 minutes, returns CSV with 308 profiles (2 fewer than preview — Sales Nav added a session-based dedup).

**Step 6 — Normalize**: 308 raw → 305 normalized (3 dropped — incomplete profile data). Sample record:
```yaml
contact_name: "Jordan Reyes" [hypothetical]
linkedin_url: "https://linkedin.com/in/jordan-reyes-marketing" [verified: phantombuster:run_2026-05-04_lk7]
title_normalized: "VP of Marketing"
seniority: vp
function: marketing
email: null   # not in Sales Nav export
email_status: unverified
phone: null
phone_status: unverified
company: "Brightline AI" [hypothetical]
company_domain: "brightline-ai.com"   # PhantomBuster's company website resolution
company_size_band: "51-200"
company_industry_normalized: "computer software"
provenance_company: [verified: phantombuster]
provenance_person: [verified: phantombuster]
provenance_email: [unverified — needs check]   # email field absent from source
signals:
  - type: leadership-change
    source: linkedin-sales-nav
    detail: "Started as VP of Marketing 2026-03-08 (66 days ago)"
    date: 2026-03-08 [verified: linkedin-sales-nav]
    evidence_url: "https://linkedin.com/in/jordan-reyes-marketing"
    strength: strong
    half_life_days: 90
personalization_hook: null   # data-enrichment will capture
source: phantombuster
source_run_id: lk7_2026-05-04
freshness_date: 2026-05-04
```

**Step 7 — Dedup**: 14 collisions against existing CRM (all on `linkedin_url`); 12 keep-existing (current data fresher), 2 replace (existing was 18mo old).

**Step 8 — Compliance**: 0 EU; ToS reminder logged ("Sales Nav-derived public-profile data only"); 0 personal-email flags (no emails in this batch).

**Step 9 — Push + summary**:
```
MetricMojo LinkedIn Sourcing Run [hypothetical]
Run ID: lk7_2026-05-04
Mode: API-substitute (PhantomBuster)
Sales Nav URL: <full url>
Filter recipe: VP Marketing, Series B SaaS, US, role started <90d
Cost: $6.16 / cap $20
Pulled: 308 → Normalized: 305 → Pushed: 291 (14 dedup merges)
  Companies: 95 (12 new, 83 enriched)
  Persons: 291 (277 new, 14 merged)
  Interaction:research: 1 (run record) + 0 review-queue
Trigger breakdown:
  recent_role_change: 305 (the filter — all matched)
  active_poster (sub-trend): 91
  company_growth (sub-trend): 47
Warning: emails absent from Sales Nav export — data-enrichment is mandatory next step
Recommended next: data-enrichment (verifier + email finder + hook capture)
```

## Heuristics

- **LinkedIn URL is the gold dedup key.** Always promote it to top of merge priority. People change jobs, emails, phones — LinkedIn URL stays.
- **Sales Nav lags reality by 2–14 days.** Profile updates take time to surface in search. Don't read "started in current role 5 days ago" as ground truth — the actual move could be 5 weeks ago.
- **Emails are absent in standard exports.** `data-enrichment` is non-optional before outreach for LinkedIn-sourced lists.
- **Active-poster filter is a leading indicator of reply rate.** People who post on LinkedIn weekly reply more often to outbound; small population but high-quality.
- **"Years in Current Position <1 year" is a 90-day trigger waterfall.** Pair with hire-announcement news and Crunchbase funding to triangulate signal strength.
- **Sales Nav UI cap of 25 leads per page = exporting 1,000 leads is 40 page-flips.** Use PhantomBuster / HeyReach for batches >100; manual for surgical pulls of 50–100.
- **Boolean keyword search beats title filter for narrow plays.** "Director of Engineering" gets you everyone; `("Director of Engineering" OR "Engineering Manager") AND ("Kubernetes" OR "k8s")` gets you the right ones.
- **Trigger amplification.** A recent role change + a recent post on a relevant topic = much higher reply rate than either alone. Surface this in run summary as a sub-tier.
- **Don't use LinkedIn-Free search.** Search results without Sales Nav are unfilterable and uncopyable; the skill assumes Sales Nav-grade access.

## Edge Cases

- **No ICP defined.** Flag ungrounded; produce filter recipe only.
- **Direct-scraping requested.** REFUSE. Output: ToS explanation + Sales Nav + PhantomBuster recommendation. Hard rule, not a guideline.
- **PhantomBuster session expired.** Phantom returns "session error"; pause; ask user to refresh LinkedIn login in PhantomBuster; resume.
- **Sales Nav search returns >1,000 results (UI cap).** Sales Nav truncates to 1,000 viewable. Recommend tightening filters; surface the cap-hit in run.
- **Trigger filter too narrow, candidate count <10.** Loosen one filter at a time (typically the recency window first); document which filter responsible.
- **Account list export (named-account play).** Skip persona search; instead use Sales Nav's "People at these companies" via account list upload. Sales Nav supports up to 1,000 accounts/list.
- **Existing-CRM deep coverage (>50% dedup rate).** Skill warns: "Of 308 profiles, 168 already in CRM. Recommend running with `exclude_existing: true` filter or accept that this is a refresh-pull, not a new sourcing."
- **Multi-language profile.** LinkedIn surfaces title in user's profile language. Capture verbatim; agent does not auto-translate (downstream cold-email picks language).
- **Privacy-mode profiles.** Sales Nav surfaces them as "LinkedIn Member" — no name, no company. Skip these; flag as `[unverified — needs check]` count in summary.
- **Sales Nav daily-search-limit hit.** LinkedIn limits searches per session; pause; resume next day or ask user to switch session/seat.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Direct-scraping path attempted | skill internal flag | Hard refuse; ToS explanation; recommend session-based tool. |
| PhantomBuster session expired | "Session invalid" | Pause Phantom; user re-authenticates LinkedIn in PhantomBuster; resume. |
| Sales Nav search-cap (1000) hit | results truncated | Surface cap; recommend filter tightening; offer to split the search by geography or size band. |
| Sales Nav daily-limit hit | "Search limit reached" | Pause; recommend resuming next day or rotating to a different seat. |
| LinkedIn detects automation, account flagged | safety warning from PhantomBuster | Stop run immediately; warn user account-safety risk; recommend pausing automation 7 days. |
| HeyReach subscription exhausted | API 403 | Surface; recommend upgrade or switch to PhantomBuster. |
| CSV upload missing LinkedIn URL column | normalize fails | LinkedIn URL is the dedup key; require user to provide it; skill cannot proceed without. |
| Privacy-mode profiles in export | empty rows | Skip; count in summary; flag as `[unverified — needs check]`. |
| Sales Nav UI changed (column-name drift) | normalize sees unknown columns | Show column-mapping; require user confirm; warn about UI drift. |
| Push to CRM fails | 4xx/5xx | Persist results locally; retry on user request. |

## Pitfalls

- **Direct LinkedIn scraping.** Forbidden. Account-suspension and legal risk. Hard rule.
- **Promoting Sales Nav data past freshness.** "Started in role 5 days ago" may be 5 weeks ago in reality.
- **Skipping `data-enrichment`.** LinkedIn rarely provides email; outreach without enrichment will mostly bounce.
- **Treating Sales Nav as a stable database.** It's a real-time index; same search next month returns different results. Re-run cadence matters.
- **Over-trusting the "active poster" filter.** It surfaces engagement, not buying intent. Pair with other triggers.
- **Inventing LinkedIn URLs.** Profile URLs follow predictable patterns but can be fabricated; never invent — if absent, route to review queue.
- **Ignoring session-safety.** Aggressive PhantomBuster usage gets accounts flagged; pace runs (50–100 profiles/day per session is safe).
- **Mistaking "LinkedIn Member" for skip-able.** Privacy-mode profiles count toward search results but yield no usable data; surface count, don't suppress.
- **Mass-connection-request abuse.** LinkedIn limits ~100 connection requests/week; skill stays out of outreach (function-3) but the pattern matters for context.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (companies, people, LinkedIn URLs, dates, signal evidence) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No Sales Nav export → default to `[unverified — needs check]`. NEVER invent a LinkedIn URL or a "started 90d ago" date to fill the trigger field.
- **Silent automation overspend.** PhantomBuster bills per profile; cap is a hard stop.

## Verification

The run is real when: (a) the `sales_nav_search_url` resolves to the same filter set on replay (URL contains all encoded filters); (b) every record's LinkedIn URL is canonical (no `?refId=...` query strings, just `/in/<handle>`); (c) provenance tags accurately reflect the source path (Sales Nav UI vs PhantomBuster vs HeyReach vs BYO); (d) `data-enrichment` is recommended before any outreach run; (e) `[unverified]` records (privacy-mode, partial profiles) routed to review queue.

## Done Criteria

1. Mode determined and stated; direct-scraping requests REFUSED.
2. Sales Nav search URL + filter recipe stored and reproducible.
3. `discover()` count surfaced; user authorization received before pull.
4. Every Lead carries provenance tags (LinkedIn URL specifically high-confidence; email field correctly tagged unverified).
5. Dedup performed; LinkedIn URL is primary merge key.
6. Compliance filters applied; ToS-compliance reminder in run record.
7. `[unverified — needs check]` records routed to review queue.
8. Run summary one-screen with trigger breakdown; recommends `data-enrichment` next; cost stayed under cap.

## Eval Cases

### Case 1 — full API-substitute mode (PhantomBuster), trigger-rich

Input: ICP grounded; Sales Nav seat + PhantomBuster key; "VP Marketing at Series B SaaS, role started <90d"; $20 cap.

Expected: ~250–350 profiles pulled; 100% of records have `linkedin_url [verified: phantombuster]`; 95%+ have title + company [verified]; 0% have verified email (Sales Nav export limitation); trigger breakdown surfaces 100% recent-role-change; recommends `data-enrichment` mandatory.

### Case 2 — manual mode, BYO export

Input: ICP grounded; Sales Nav seat alone; user runs search in UI; uploads 80-row CSV.

Expected: skill outputs reproducible search URL + recipe; normalizes CSV with `[user-provided]` provenance for all fields; LinkedIn URL preserved as primary key; emails absent; recommends `data-enrichment` next.

### Case 3 — direct-scraping refused

Input: user prompt "scrape LinkedIn for VPs of Eng at FAANG."

Expected: skill REFUSES with ToS explanation; recommends Sales Nav (use built-in filter) or PhantomBuster (session-based); does NOT produce records; logs the refusal as an `interaction:research` for audit.

### Case 4 — privacy-mode-heavy export

Input: PhantomBuster pull of 200 profiles, 30 returned as "LinkedIn Member" (privacy-mode).

Expected: 170 normalized; 30 routed to review queue with `[unverified — needs check]` and `#privacy-mode`; run summary surfaces the privacy-mode rate; recommends tighter filters or different geography for next run.

## Guardrails

### Provenance (anti-fabrication)

Per §8 of conventions: LinkedIn URL is the highest-confidence field this skill produces; emails the lowest. Provenance accurately reflects this — `[verified: linkedin-sales-nav]` for identity fields, `[unverified — needs check]` for missing email/phone. Worked-example fictional entities tagged inline. Direct scraping → REFUSE; this is the strongest guardrail in this skill.

### Evidence

Every signal entry has source = `linkedin-sales-nav`, date from the profile's "started in role" field, evidence_url = the LinkedIn profile URL.

### Scope

This skill sources from LinkedIn. It does NOT enrich emails (data-enrichment), score (lead-scoring), or send connection requests / messages (function-3 — `linkedin-outreach`).

### Framing

Run summary uses operational language. Trigger breakdown highlights recent-role-change as the primary signal class.

### Bias

Sales Nav over-indexes on tech/SaaS; under-indexes on regulated industries (manufacturing, healthcare, government). Cross-check with `lead-sourcing-web` for non-tech ICPs.

### Ethics

LinkedIn ToS compliance is non-negotiable. Direct-scraping refused. Session-based tools (PhantomBuster, HeyReach) acceptable because they use the user's own credentials and rate-respect the platform.

### Freshness

Sales Nav data is real-time-indexed but lags 2–14 days. Re-runs catch new entrants — encourage 30-day cadence.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Profiles pulled, emails missing | `data-enrichment` (verifier + email finder + hooks) | Lead records (linkedin_url-keyed) |
| Trigger play needs firmographic depth | `lead-sourcing-apollo` (cross-reference) | Sales Nav records + Apollo filter set |
| Trigger play needs multi-source orchestration | `lead-sourcing-clay` | Same ICP filters |
| Trigger invisible to LinkedIn (job posts, RFPs, press) | `lead-sourcing-web` | Same ICP + open trigger criteria |
| ICP not grounded | `icp-definition` | Hypothesis + product description |
| Profiles ready for outreach | `lead-scoring` (after enrichment) | Enriched records + ICP scorecard |
| Run produced privacy-mode-heavy results | `lead-sourcing-apollo` (alternate firmographic source) | Same ICP filters |

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
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping. Note: emails will typically be `[unverified]` even on `[verified]` LinkedIn-source records — that's expected. |
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
- Direct-scraping refused — log the refusal as an `interaction:research` for audit; produce no records.
- Privacy-mode profiles — see provenance routing.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
- Run flagged "ICP-ungrounded" — push run record tagged `#icp-ungrounded`; defer person push.
- Account-safety warning from automation tool — abort push; surface; recommend pause.
