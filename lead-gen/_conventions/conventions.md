# Function 2 — Lead Generation Conventions

This file is the shared rules document for every skill in `function-2-skills/`. All five skills (`lead-sourcing-apollo`, `lead-sourcing-clay`, `lead-sourcing-linkedin`, `lead-sourcing-web`, `data-enrichment`, `lead-scoring`) MUST reference this document by name in their `## Inputs Required` and `## Guardrails` sections rather than redefining the schema, the adapter contract, or the dedup keys locally.

> *The worked examples in function-2 skills use a fictional product (WorkflowDoc) for illustration. The schemas, adapter contracts, scoring rubrics, and procedures are vertical-agnostic and apply to any B2B GTM context.*

---

## Why this file exists

Function-1 skills are mostly self-contained — each produces a different artifact (market brief, ICP, positioning canvas). Function-2 skills are tightly coupled — all five read from and write to the **same Lead record**. If `lead-sourcing-apollo` says a Lead has `{name, email, company, title}` and `lead-sourcing-linkedin` says `{full_name, work_email, employer, role}`, `lead-scoring` ends up with two incompatible shapes and the whole pipeline breaks. One conventions file kills five sources of drift.

---

## 1. Shared Lead Schema

This is the canonical record. Every sourcing skill normalizes its raw output to this shape. `data-enrichment` decorates it. `lead-scoring` writes its scoring fields onto it. The agentic-app CRM stores it across `company` + `person` + `interaction` records.

### 1.1 Identity

| Field | Type | Required | Notes |
|---|---|---|---|
| `lead_id` | UUID | yes | Internal ID. Generated at first push. |
| `linkedin_url` | string | strongly recommended | **Primary merge key for person dedup.** Most stable identifier. |
| `email` | string | recommended | Secondary merge key. |
| `phone` | string | optional | Tertiary merge key (mobile preferred). |
| `email_status` | enum | yes if email present | `unverified` / `verified` / `risky` / `role-based` / `invalid` / `catch-all-domain` |
| `phone_status` | enum | yes if phone present | `unverified` / `verified` / `mobile` / `landline` / `voip` / `dnc` |

### 1.2 Person

| Field | Type | Required | Notes |
|---|---|---|---|
| `contact_name` | string | yes | Full name as captured. |
| `contact_first_name` / `contact_last_name` | string | parsed at normalize time | Supports personalization tokens. |
| `title_raw` | string | yes | The string the source returned ("Founder & CEO @ Foo \| Investor"). Preserve verbatim. |
| `title_normalized` | string | yes | Stripped, deduped (`VP Marketing`). |
| `seniority` | enum | yes | `c-level` / `vp` / `director` / `manager` / `ic` / `intern` / `unknown` |
| `function` | enum | yes | `sales` / `marketing` / `engineering` / `ops` / `hr` / `finance` / `support` / `legal` / `product` / `executive` / `other` |
| `linkedin_headline` | string | optional | Powers personalization hooks. |

### 1.3 Company

| Field | Type | Required | Notes |
|---|---|---|---|
| `company` | string | yes | Display name. |
| `company_domain` | string | yes | **Primary merge key for company dedup.** Apex domain only — strip subdomains except `www`. |
| `company_size_band` | string | yes | `1-10` / `11-50` / `51-200` / `201-500` / `501-1000` / `1001-5000` / `5001+` |
| `company_size_exact` | int | optional | When source provides headcount. |
| `company_industry_normalized` | string | yes | Map to Apollo's industry taxonomy as the canonical reference; record the source's raw value alongside. |
| `company_location` | string | yes | "City, State, Country" preferred. |
| `company_founded_year` | int | optional | |
| `company_revenue_band` | string | optional | `<1M` / `1-10M` / `10-50M` / `50-250M` / `250M+` |
| `company_funding_stage` | string | optional | `bootstrapped` / `seed` / `series-a` / ... / `public` / `acquired` |
| `company_tech_stack` | array<string> | optional | From BuiltWith/Wappalyzer. |

### 1.4 Signals (the *why* a lead is on the list)

| Field | Type | Required | Notes |
|---|---|---|---|
| `signals` | array of objects | yes (≥1) | See sub-schema below. |
| `personalization_hook` | string | strongly recommended | One sentence, dated, source-attributed. The "9 seconds, 25–50 words" foundation that the cold-email skill draws on. |
| `trigger_events` | array<string> | optional | References to entries in the `icp-definition` trigger library (e.g. `series-b-funding`, `vp-support-hire`). |

**Signal sub-schema:**
```yaml
- type: <funding | hiring | leadership-change | tech-adoption | review | job-post | press | competitor-mention | rfp | other>
  source: <e.g. "crunchbase", "linkedin-job-post", "g2-review">
  date: <ISO date — when the signal occurred, NOT when we found it>
  evidence_url: <permalink>
  strength: <strong | medium | weak>
  half_life_days: <int — see freshness rules>
  detail: <one sentence describing the signal>
```

### 1.5 Scoring (filled by `lead-scoring`, read by everything downstream)

| Field | Type | Notes |
|---|---|---|
| `icp_tier` | enum | `tier-1` / `tier-2` / `tier-3` / `anti-icp`. Cutoffs from `icp-definition`. |
| `icp_score` | int (0–100) | The 100-pt scorecard total. |
| `score_rationale` | object | Per-dimension breakdown (Pain / Trigger / WTP / Reach / TTV / Strategic). |
| `bant_status` | object | `{budget, authority, need, timing}` each `confirmed | inferred | unknown`. |
| `champ_status` | object | `{challenges, authority, money, prioritization}` same enum. |
| `priority` | enum | `hot` / `warm` / `cold` — derived from `icp_tier` + signal recency. |
| `score_freshness_date` | ISO date | When scored. Re-score after 60 days or material new signal. |

### 1.6 Provenance (the anti-fabrication scaffold — see §8)

| Field | Type | Notes |
|---|---|---|
| `provenance_company` | enum | `user-provided` / `verified` / `hypothetical` / `unverified` |
| `provenance_person` | enum | same |
| `provenance_email` | enum | same |
| `provenance_phone` | enum | same |
| `provenance_signals` | array | One entry per `signals[]` item. |
| `source` | string | e.g. `apollo-api`, `apollo-csv-export`, `linkedin-sales-nav-csv`, `byo-csv`, `clay-table` |
| `source_run_id` | UUID | Traces back to a single sourcing run. |
| `source_query` | string or object | The exact filter set used. Reproducible. |
| `freshness_date` | ISO date | When last seen alive at source. Drives re-verify cadence. |

---

## 2. Source Adapter Contract

Every sourcing skill (`lead-sourcing-apollo`, `lead-sourcing-clay`, `lead-sourcing-linkedin`, `lead-sourcing-web`) exposes the same three-method interface. This is what lets `lead-scoring` and `data-enrichment` stay source-agnostic.

```
discover(filters) → { candidate_count: int, estimated_cost_usd: float, estimated_credits: int, sample: Lead[5] }
pull(filters, limit, run_id) → { records: Lead[], cost_usd: float, credits_used: int, warnings: string[] }
normalize(raw_records) → Lead[]
```

- **`discover`** is mandatory before `pull` for any API mode that bills per record. It returns a small sample (5 leads) so the user can sanity-check filters before authorizing the spend.
- **`pull`** must respect `SOURCING_RUN_USD_CAP` and `SOURCING_RUN_RECORD_CAP` from the env contract. Aborts with a clear error if either would be exceeded.
- **`normalize`** is the only function allowed to invent fields not present in the raw response — and it must tag every invention with `[unverified — needs check]`. No silent enrichment.

The skill body wraps these three with mode selection (§3), provenance tagging (§8), dedup (§6), and the push-to-CRM step (§9).

---

## 3. Three-Mode Pattern

Every sourcing skill MUST handle three modes and degrade gracefully between them. Hard rule — "Apollo not configured" failures are forbidden.

### 3.1 API mode
The corresponding API key is set in `.env`. The skill calls the API directly, paginates, handles rate limits, manages credits. Provenance: `[verified: <api-name>]` for fields the API returns; `[unverified — needs check]` for anything the skill infers.

### 3.2 Manual export mode
The user has access to the tool (e.g. an Apollo paid seat) but no API key. The skill outputs the **exact search filters** and **column-set** the user should select in the tool's UI, plus instructions for exporting to CSV. The user runs the export, drops the CSV path back to the skill, and the skill ingests via `normalize`. Provenance: `[user-provided]` for all fields the CSV contained at the moment of export.

### 3.3 BYO list mode
The user has a list from anywhere — a friend's CRM, a conference attendee list, a scraped GitHub org, an old export. The skill:
1. Reads the file, infers the column mapping, shows the inferred mapping back to the user for confirmation.
2. Flags missing required fields (no email? no LinkedIn? no company domain?).
3. Routes those leads to `data-enrichment` to fill gaps before scoring.
4. Provenance: `[user-provided]` with `confidence: low` until enrichment promotes individual fields to `[verified: <enricher>]`.

Procedure entry pattern (every sourcing skill's first step):
```
if API_KEY is set: → API mode
elif user has tool access: → manual export mode (offer filter + column set)
elif user has any list: → BYO mode (offer schema repair)
else: → degrade to "produce filter recommendations only, no records"
```

---

## 4. Routing Logic — when to reach for which sourcing skill

Deterministic, not vibe-based. Order of preference depends on the trigger of the run:

| Trigger | Best-fit sourcing skill | Why |
|---|---|---|
| Known-firmographic play (e.g. "Series B SaaS, 100–300 emp, US, runs Zendesk") | `lead-sourcing-apollo` | Apollo's filter UX maps directly to firmographic ICP. |
| Multi-source orchestration (Apollo + Hunter + tech-stack + verifier in one workflow) | `lead-sourcing-clay` | Clay is the meta-adapter; cheaper than wiring 4 APIs. |
| Role-based or trigger-based play (recent VP hires, leadership shifts, open job reqs revealing pain) | `lead-sourcing-linkedin` | Sales Nav surfaces these in real time. |
| Trigger Apollo can't see (job-post text revealing tech adoption, expansion press, RFP issuance) | `lead-sourcing-web` | Web search + job board scraping. |
| User dropped a CSV / has an existing list | `lead-sourcing-apollo` (BYO mode) **or** `data-enrichment` directly | Pick whichever feels closer to the user's intent. |

When two skills could plausibly run, prefer the one that costs less per qualified lead and has higher trigger freshness for the play.

---

## 5. Cost Awareness Rules

Apollo, Clay, ZoomInfo, Hunter all charge credits per lead. Skills MUST:

1. **Quote before pulling.** `discover()` returns candidate count and `estimated_cost_usd`. The skill surfaces this to the user in plain English: *"This search matches 4,200 contacts. Pulling all of them costs ~$84 in Apollo credits. Recommended: pull the 500 highest-scoring against your ICP first (~$10), review, then expand. Proceed?"*
2. **Respect `SOURCING_RUN_USD_CAP`** (default $25). Never exceed without explicit user override (a one-time confirm, not a config change).
3. **Pull in tiers.** Default first batch ≤500 records. Materialize remainder only after the user has reviewed sample quality.
4. **Log credits used per run** to the `interaction:research` record so cost-per-lead can be calculated downstream by `channel-performance`.

---

## 6. Freshness and Dedup Rules

### Merge keys (in priority order)
1. `linkedin_url` — most stable for people. Survives email/phone changes, job changes (when re-fetched).
2. `email` — for people without LinkedIn.
3. `phone` — last resort for people.
4. `company_domain` — for companies. Apex domain only.

When two records collide on the same key but differ in fields: prefer the record with the **most recent `freshness_date`**, then the one with the higher provenance tier (`verified` > `user-provided` > `unverified` > `hypothetical`).

### Freshness cutoffs
| Field | Half-life | Behavior |
|---|---|---|
| `email` (verified) | ~9 months | Re-verify before any outreach run; downgrade to `risky` if re-verify fails. |
| `phone` | ~12 months | Re-verify before cold-call run. |
| `title_normalized` | ~6 months | Re-pull from LinkedIn before re-score. People change roles. |
| Funding signal | ~12 months | After 12 months, "raised Series B" is not a buying trigger; it is a stale fact. |
| Hiring signal | ~3 months | Open req closes; signal expires fast. |
| Tech-adoption signal | ~6 months | Adoption sticks longer but evolves. |
| Press / news signal | ~6 months | Decay aggressive — old news is no news. |

Each `signals[].half_life_days` defaults from the table above unless the source provides a more specific value.

---

## 7. Compliance Baseline

Bake these into every skill so the agent doesn't generate non-compliant lists.

- **LinkedIn ToS.** Direct scraping of LinkedIn profiles is forbidden by the User Agreement. `lead-sourcing-linkedin` MUST emit Sales Navigator search URLs and filters, never attempt direct profile scraping. If the user wants automation, route to PhantomBuster / HeyReach (which use the user's own session).
- **GDPR (EU/UK contacts).** Outreach requires a *legitimate-interest* basis. Skills tag EU/UK contacts with `gdpr_basis: legitimate-interest` and flag that the outreach copy MUST include opt-out language. Personal/non-business emails (`@gmail.com`, etc.) for EU contacts are routed to a separate review queue, not the active prospect list.
- **CAN-SPAM (US).** Cold email requires a physical address in the email and a one-click opt-out. Lead records carry no extra burden, but `cold-email-sequence` (function-3) reads `is_us` from `company_location` and applies the rule.
- **TCPA (US cold-call).** SMS to mobiles requires consent; voice calls to mobiles flagged DNC are a hard stop. `phone_status: dnc` blocks outreach at the cadence skill level.
- **Catch-all domains.** Verifiers report "valid" because the domain accepts anything. Mark `email_status: catch-all-domain`, never `verified`. Treat replies as the real validation.
- **Role addresses.** `info@`, `sales@`, `contact@`, `hello@`, `support@` etc. — never score as Tier-1 contacts. Tagged `email_status: role-based` and `priority: cold` regardless of firmographic fit.

---

## 8. Anti-Fabrication: Provenance Tagging

This is the universal anti-hallucination contract. Every named entity in any function-2 output (companies, people, emails, phone numbers, dates, dollar figures, signal evidence URLs, customer counts, named tools) MUST carry one of four explicit tags. Untagged named entities are a contract violation. The agent must default to `[unverified — needs check]` rather than asserting silently.

| Tag | Meaning |
|---|---|
| `[user-provided]` | Supplied by the user in input — agent reproduces, doesn't invent. CSV/spreadsheet imports default to this. |
| `[verified: <source>]` | Checked via a named tool with a citation URL or run ID. e.g. `[verified: apollo-api run_2026-05-04T14:21]`, `[verified: million-verifier]`. |
| `[hypothetical]` | Explicitly illustrative, not claimed as real. ALLOWED only in worked examples and when the user explicitly asked for a hypothesis ("show me what a Tier 1 lead would look like"). |
| `[unverified — needs check]` | Agent's best inference; do not act on without human verification. |

### 8.1 Tool-grounding rule
If no live research / API tool is available at runtime (no Apollo key, no SerpAPI key, no verifier), every external-fact assertion MUST default to `[unverified — needs check]`. Hard rule. An agent without web access that confidently invents a Series B funding date is a contract violation.

### 8.2 Push-to-CRM hygiene routing (see also §9)
| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping (real `company` / `person` / `interaction` records, normal priority/score). |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required` tags. Never as `company` / `person`. The dashboard review-queue scaffold lives in agentic-app/ as a follow-up; the tag contract is enforced at skill output time today. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

### 8.3 Worked-example tagging convention
Every fictional entity in a worked example carries the tag inline at first use, e.g. *"Stitchbox [hypothetical] is a 180-employee Series B SaaS company..."*. Subsequent uses of the same entity within the same example block MAY be untagged once the section has been opened with a block-level disclaimer. This trains the agent to apply the same per-entity tagging discipline to real output.

### 8.4 Function-2-specific risks
Sourcing skills can fabricate entire companies/contacts in ways function-1 skills cannot. Mitigations:
- **API mode**: emit raw API response IDs + the API call URL with `[verified: <api>:run_id]`.
- **Manual export mode**: emit `[user-provided]` for everything in the CSV; the skill never adds fields not present in the CSV without enrichment + re-tagging.
- **BYO mode**: same as manual export, plus `confidence: low` until `data-enrichment` promotes individual fields.
- **Personalization hooks**: a hook is `[verified: <source-url>]` only if the agent can cite a permalink to the source (LinkedIn post, news article, podcast episode). Otherwise it ships as `[unverified — needs check]` and `cold-email-sequence` will refuse to use it as an opener.

---

## 9. Push-to-CRM Conventions for Function 2

Function-1 skills mostly produced research. Function-2 skills produce **persons** as the primary entity. The score lives on the person record (per leadership decision 2026-05-04).

### 9.1 Entity routing per skill

| Skill | Primary push | Secondary push |
|---|---|---|
| `lead-sourcing-apollo` / `lead-sourcing-clay` | `company` (firmographic), `person` (contact) | `interaction:research` with the search-query payload |
| `lead-sourcing-linkedin` | `person` (linkedin_url is dedup key) | `interaction:research` with the Sales Nav search URL |
| `lead-sourcing-web` | `company` (typically), occasionally `person` | `interaction:research` with the trigger evidence (job post URL, news link) |
| `data-enrichment` | PATCH on existing `person` (email_status, phone, linkedin, hooks) and `company` (about, industry) | `interaction:research` with verifier provider + verdict |
| `lead-scoring` | PATCH on `person` (`score`, `priority`, `icp_tier`, `score_rationale`) | `interaction:research` with full scoring math + signal evidence |

### 9.2 Score-on-person rule
`lead-scoring` writes the canonical score onto the **person** record (using the `score` and `priority` fields agentic-app's push API already supports), with `tags` carrying the tier. Each scoring run also creates an `interaction:research` for history — so the dashboard can show "current score: 87 / hot / tier-1" and a timeline of how it got there.

### 9.3 Source tag
Every push carries `source: "skill:<skill-name>:v<version>"` (e.g. `skill:lead-sourcing-apollo:v2.0.0`). The push API uses this for provenance and de-dup-on-replay.

### 9.4 Named-product vs. non-product hygiene (per CLAUDE.md rule #6)
Only push real entities (companies, people) as `company` / `person` records. Push abstractions, insights, or non-product alternatives (DIY, "do nothing", "shift budget elsewhere") as `interaction` records only — never as fake `company` records. Function-2 sourcing skills almost always emit real entities; the rule mainly bites in `data-enrichment` when an enrichment service returns "this contact appears to use no CRM" — that's an `interaction:research` note, not a synthetic company.

### 9.5 When NOT to push
- Sourcing run that returned 0 results — push the `interaction:research` record (the *fact* of the empty run is information) but no `company` / `person`.
- Records still in BYO confidence-low state — push as `interaction:research` with `#byo-pending-enrichment` tag; defer `person` push to after enrichment.
- Provenance `[unverified — needs check]` — see §8.2.
- Provenance `[hypothetical]` — never.

---

## 10. Inheritance from Function 1

Every function-2 skill declares these inputs from function-1 in its `## Inputs Required` section. If the upstream skill has not been run, function-2 skills can still operate but flag output as `confidence: low` and tag entities `[unverified — needs check]` aggressively.

| Function-2 skill | Function-1 inputs it consumes |
|---|---|
| All sourcing skills | ICP firmographic + role map + trigger library + anti-ICP boundary (from `icp-definition`) |
| `lead-sourcing-web` | Beachhead segment + market type (from `market-research`) |
| `lead-scoring` | 100-pt scorecard rubric + tier cutoffs + Pain-Trigger-Outcome chain (from `icp-definition`); competitor-mention signal weights (from `competitor-analysis`) |
| `data-enrichment` | Persona role map (helps grade title/seniority) (from `icp-definition`) |

If `icp-definition` has not been run, function-2 sourcing skills can produce a candidate list but must flag it as **ungrounded** until the ICP exists. Mirrors the function-1 chain pattern (`market-research` → `icp-definition`).

---

## 11. WorkflowDoc Worked-Example Continuity

Function-1 used WorkflowDoc as the company being analyzed. Function-2 flips the camera: **WorkflowDoc is now the seller**, prospecting against the ICP its function-1 skills produced. Worked examples chain across skills:

1. `icp-definition` (function-1) → produces ICP scorecard for "Series B SaaS, 100–300 emp, support team 5–15, US"
2. `lead-sourcing-apollo` (function-2) → translates ICP to Apollo filters → returns 50 raw leads
3. `data-enrichment` → verifies emails, finds phones, captures personalization hooks
4. `lead-scoring` → applies 100-pt scorecard, tiers the 50 into Tier 1 / 2 / 3 / Anti-ICP
5. `cold-email-sequence` (function-3, future) → consumes scored leads + hooks to write outreach

Every fictional entity in worked examples (target company names, contact names, signal sources, dates, dollar figures) is tagged `[hypothetical]` inline.

---

## 12. Open conventions deferred to function-3+

These are not function-2's problem but worth flagging so we don't accidentally encode the wrong assumption:

- **Cadence orchestration.** When a Lead is in active outreach, who owns the record? `multi-channel-cadence` (function-3). Function-2 just produces the Lead.
- **Reply classification.** When a person replies, the Lead transitions out of "prospect" status. `reply-classification` (function-4). Function-2 doesn't define reply states.
- **Pipeline stage.** Function-2 deliveries lift a Lead to "Sourced → Enriched → Scored → Ready-for-outreach". The 7-stage sales pipeline (Lead Gen → Lead Nurturing → MQL → SAL → SQL → Closed → Post-Sales) is `pipeline-stages` (function-5). Don't bake stage transitions into function-2.

---

## Document version

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-05-04 | Initial draft alongside `lead-sourcing-apollo-v2` pilot. |
