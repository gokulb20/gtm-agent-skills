---
name: data-enrichment
description: Enrich raw Lead records with verified emails, phone numbers, social links, and citable personalization hooks via a verifier waterfall, deliverability classification, and source-tracked hook capture. Use when a sourcing skill has produced a list with unverified emails, missing phones, or no personalization hooks; when a BYO list needs schema repair before scoring; or when stale records need re-verification before an outreach run.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, lead-enrichment, email-verification, personalization, function-2]
related_skills:
  - lead-sourcing-apollo
  - lead-sourcing-clay
  - lead-sourcing-linkedin
  - lead-sourcing-web
  - lead-scoring
  - icp-definition
inputs_required:
  - lead-records-from-sourcing-skill-or-byo
  - verifier-api-key-or-csv-upload
  - hook-source-permission-flags
  - cost-budget-credits-or-dollar
  - run-purpose-tag
deliverables:
  - patched-lead-records-with-verified-status
  - email-verification-log
  - personalization-hook-with-citable-source
  - missing-fields-report
  - enrichment-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Data Enrichment

Decorate raw Lead records with verified email statuses, phone numbers (mobile/landline classified), normalized social links, and citable personalization hooks. The output is a Lead record `lead-scoring` can score with confidence and `cold-email-sequence` can write a 25–50-word opener against without inventing context.

> *Worked example uses a fictional product (HelpdeskPro [hypothetical]); procedure is vertical-agnostic. Shared rules — Lead schema, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`.*

## Purpose

Sourcing produces *candidate* records — names, titles, claimed emails — but most fields aren't trustworthy at outreach time. This skill is the gate: verify what's verifiable, classify what isn't, capture hooks only when they have a citable source, and tag everything per the function-2 provenance contract so downstream skills know what they can trust.

## When to Use

- "Verify these 500 emails before we send."
- "We have 200 leads but no phone numbers."
- "Find a personalization hook for each of these prospects."
- "Re-verify the leads we sourced 6 months ago."
- "Clean up this BYO list before scoring."
- Pre-scoring quality gate after any sourcing run.
- Pre-outreach freshness pass before high-effort sequences.

## Inputs Required

1. **Lead records** — output of any sourcing skill or BYO file; conforms to function-2 Lead schema.
2. **Verifier access** — one of: `MILLION_VERIFIER_API_KEY`, `NEVERBOUNCE_API_KEY`, `ZEROBOUNCE_API_KEY`, `HUNTER_API_KEY`, CSV upload, or "best-effort" (degrade).
3. **Hook-source permissions** — booleans for `linkedin_recent_posts`, `news_search`, `podcast_guest_search`, `company_blog_scrape`, `g2_review_search`. Defaults: news + linkedin if available.
4. **Cost budget** — default `SOURCING_RUN_USD_CAP=$25`; aborts above cap without override.
5. **Run purpose tag** — short string for cost attribution + replay.
6. (Optional) Freshness override for stale-list re-verification.

## Quick Reference

| Concept | Value |
|---|---|
| **Three passes** | Email verify → Phone discovery → Hook capture |
| **Verifier waterfall** | Syntax → MX → SMTP → catch-all → role-based detection |
| **Email status enum** | `verified` / `risky` / `catch-all-domain` / `role-based` / `invalid` / `unverified` |
| **Phone status enum** | `mobile` / `landline` / `voip` / `dnc` / `unverified` / `invalid` |
| **Hook rule** | Permalink + date OR null. No URL → no hook. |
| **Verifier cost (typical)** | Agent reads vendor docs at runtime; pricing changes — verify live before any spend. |
| **Catch-all rule** | Verifier "valid" + accept-all domain → `catch-all-domain` (never `verified`) |
| **Freshness windows** | Email: 90d; phone: 12mo; hook: 90d. Override available. |
| **Compliance** | EU contacts → `gdpr_basis: legitimate-interest`; DNC → strip phone; role-addresses → never Tier-1 |
| **Push routing** | PATCH person fields for verified; `interaction:research` only for `[unverified — needs check]` |

## Procedure

### 1. Triage the input batch
Group records by enrichment need: email-verify-only / phone / hook / all-three / fresh-skip. Surface counts to user.

### 2. Cost-quote across passes
`discover_email_verify + discover_phone + discover_hook` → combined estimate with per-pass breakdown. User chooses passes if budget tight.

### 3. Email verification waterfall
For each record: syntax → MX → verifier API → map result to `email_status` enum. Stamp `provenance_email: [verified: <verifier>:run_<id>]` for `valid`; `[unverified — needs check]` for `risky`/`unknown`.

### 4. Phone discovery + classification
Hunter / Lusha lookup; classify mobile / landline / voip; cross-check DNC for US contacts. Stamp `phone_status` accordingly.

### 5. Personalization-hook capture
Within permission flags: pull LinkedIn recent posts → news search → podcast guest list → company blog → G2 review. Capture source URL + date + verbatim text. **Hooks ship with permalink OR null** — no URL, no hook.

### 6. Compliance pass
EU/UK contacts → `gdpr_basis`; personal-email B2B mismatch flagged; `phone_status: dnc` strips phone from active record.

### 7. Dedup re-check
Newly-discovered LinkedIn URLs / emails may collide with existing CRM records; re-run dedup, log merges.

### 8. Push patched records
PATCH person/company fields per conventions §9. `interaction:research` per run with verification log; `[unverified — needs check]` records to review queue.

### 9. Emit run summary + missing-fields report
One-screen output with per-pass results, costs, missing-fields, recommended next skill (`lead-scoring`).

## Output Format

- PATCHed Lead records (only changed fields shown in run summary)
- Email verification log (per-record verdict + provenance)
- Phone classification log
- Personalization hook entries (text + URL + date) OR null with reason
- Missing-fields report (records that still lack email or hook)
- Run record: costs, counts per pass, dedup merges, warnings, next-skill recommendation
- Review queue: `[unverified — needs check]` records as `interaction:research`

## Done Criteria

1. Input records triaged with counts surfaced per pass.
2. Cost quoted across passes; user authorization received before any spend.
3. Every record's `email_status` traces to a verifier run_id (or `[unverified — needs check]` if best-effort).
4. Personalization hooks ship with permalink + date OR null with reason — no fabricated openers.
5. Compliance pass run (GDPR, DNC, role-address); dedup re-checked post-enrichment.
6. `[unverified — needs check]` records routed to review queue, NOT patched onto person.
7. Run summary one-screen with cost vs cap and next-skill recommendation.

## Pitfalls

- **Trusting upstream verifier flags.** Apollo's "verified" is hint-quality. Always re-verify with a real verifier before high-effort sends.
- **Inventing hooks.** "Saw your post on X" with no URL is a hallucinated opener. Hooks ship with citable URL or they ship null.
- **Verifying once and forgetting.** Email lists decay ~30%/year; re-verify the active list quarterly.
- **Catch-all noise.** `@apple.com`, `@meta.com` style domains mark every email valid; treat as `catch-all-domain` regardless of verifier verdict.
- **Spending on records that can't be enriched.** Cap budget per record; no email AND no LinkedIn → skip and surface.
- **DNC complacency.** TCPA fines per-violation. Strict strip on `phone_status: dnc`.
- **Hook-source overreach.** Scraping LinkedIn private posts violates ToS. Only public-profile content.
- **Pattern-guessed emails treated as verified.** Hunter's pattern guess is best-guess; verify before promoting past `risky`.
- **Mobile/landline confusion.** SMS to landline isn't delivered; cold-call to DNC mobile is illegal.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (contact names, hook URLs, news sources, dates, verifier verdicts) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No verifier or news API → default to `[unverified — needs check]`. NEVER promote `email_status` past `unverified` without a real verifier verdict; NEVER ship a hook string without a permalink.
- **Silent budget overspend.** Cumulative cost adds up; cap is a hard stop.

## Verification

The run is real when: every patched record's `email_status` traces to a verifier run_id; every personalization hook has a permalink that resolves; the missing-fields report lists which records still need work and why; `lead-scoring` can apply BANT/CHAMP and the 100-pt scorecard without `[unverified — needs check]` field gaps capping scores. Negative test: pick 5 hooks at random; click each `source_url`. If any 404 or describe an unrelated event, hook capture is broken.

## Example

**User prompt:** "Verify emails and capture hooks for these 50 [hypothetical] leads from a recent sourcing run. MillionVerifier and SerpAPI configured [hypothetical]. $5 [hypothetical] cap."
**What should happen:** Triage (50 [hypothetical] need verify, 38 [hypothetical] need phone, 50 [hypothetical] need hook). Cost quote ~$5 [hypothetical] — proceed. MillionVerifier returns 31 verified / 8 risky / 5 catch-all / 4 role-based / 2 invalid [hypothetical]. Hunter find-phone returns 9 mobile / 14 landline / 1 DNC-stripped / 15 not-found [hypothetical]. SerpAPI hook capture: 31 records [hypothetical] get a citable hook (news/LinkedIn permalink + date [hypothetical]), 19 [hypothetical] get `personalization_hook: null` with `[unverified — needs check]` reason "no result in last 90d" [hypothetical]. Push 48 [hypothetical] patched persons, 1 [hypothetical] run interaction, 19 [hypothetical] review-queue items. Recommend `lead-scoring`.

**User prompt:** "I don't have a verifier configured but I want to clean up this BYO list."
**What should happen:** Best-effort mode. Run syntax + MX + pattern detection (`info@` → role-based; `@gmail.com` paired with company domain → personal-email flag). Cannot promote past `email_status: unverified` for anything; no hook capture (no SerpAPI [hypothetical]). Tag everything `[unverified — needs check]` per the tool-grounding rule. 100% [hypothetical] to review queue. Run summary recommends configuring MillionVerifier before next pass. Agent reads vendor docs at runtime; pricing changes — verify live before any spend.

**User prompt:** "Re-verify these 500 [hypothetical] leads we sourced 9 [hypothetical] months ago — they're stale."
**What should happen:** Freshness override enabled. Re-run all three passes on every record. Expected: ~30% [hypothetical] of emails downgrade (`verified` → `risky`/`invalid`) due to job changes. ~10% [hypothetical] get a new LinkedIn URL via re-fetch. Hooks all re-captured (old hooks expired [hypothetical]). Surface attrition rate: if >40% [hypothetical] emails decayed, flag the source as quality-degraded [hypothetical] and recommend channel-performance review.

## Linked Skills

- Records enriched, ready to score → `lead-scoring`
- Too many missing email/linkedin → re-source via `lead-sourcing-apollo` / `lead-sourcing-linkedin`
- Hook capture rate <30%, need richer signals → `lead-sourcing-linkedin` (Sales Nav)
- BYO list still lacks core fields → `lead-sourcing-web` (research mode)
- List is stale (>9 months) → re-run `data-enrichment` with freshness override
- Verifier disagreement patterns → `channel-performance` (planned, function-6)

## Push to CRM

After enrichment, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push` (PATCH semantics — push API auto-merges by dedup key). Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Verified email + phone + hook for an existing person | `person` (PATCH via dedup key) | `contactEmail`, `contactPhone`, `contactLinkedIn`, `contactAbout` (hook text), `tags` updated to include `#enriched #email-verified` |
| Hook source URL + date | `interaction` (type: `research`) | `relevance` = hook text + URL + date; `tags: "#personalization-hook #function-2"` |
| Run record (verification log, costs, missing-fields report) | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#enrichment-run #function-2"` |
| `[unverified — needs check]` (no hook source, ambiguous email) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #data-enrichment"` |

`lead-scoring` writes the `score` and `priority` fields onto the person record afterward. This skill does NOT touch score.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
MILLION_VERIFIER_API_KEY=   # or NEVERBOUNCE_API_KEY / ZEROBOUNCE_API_KEY
HUNTER_API_KEY=
SERPAPI_KEY=
SOURCING_RUN_USD_CAP=25
```

### Source tag

`source: "skill:data-enrichment:v2.0.0"`

### Example push (PATCHed person + hook interaction)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Northstar CS",
    "contactName": "Theo Park",
    "contactEmail": "theo@northstar-cs.com",
    "contactPhone": "+15551234567",
    "contactLinkedIn": "https://linkedin.com/in/theo-park-cx",
    "contactAbout": "Hook: Northstar CS just hired their first VP of CX (announced 2026-04-19). Source: news.example.com/northstar-vp-cx-hire-2026",
    "tags": "#enriched #email-verified #hook-news #function-2",
    "relevance": "Enriched in run enrich_2026-05-04_t3p. email_status: verified [verified: million-verifier]; phone_status: mobile; hook: VP CX hire 2026-04-19 [verified: serpapi-news]. Ready for lead-scoring.",
    "source": "skill:data-enrichment:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#enrichment-run #function-2",
    "relevance": "Enrichment run enrich_2026-05-04_t3p. Inputs: 50 records from apollo_2026-05-04_h7k. Cost: $4.86. Email: 31 verified / 8 risky / 5 catch-all / 4 role-based / 2 invalid. Phone: 9 mobile / 14 landline / 1 DNC-stripped. Hook: 31 with URL / 19 no source. 19 records routed to review queue. Recommended next: lead-scoring.",
    "source": "skill:data-enrichment:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §8.2:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | PATCH per the standard mapping (person field updates land on existing record). |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #data-enrichment` tags. The person record is NOT patched — hook stays null, email_status stays whatever it was. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified-hook push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #data-enrichment #hook-missing",
    "relevance": "Hook capture failed for Mira Chen [unverified — needs check]: no news/podcast result in last 90d. Person record hook field left null. Recommend re-attempt with linkedin_recent_posts permission or manual capture.",
    "source": "skill:data-enrichment:v2.0.0"
  }'
```

### When NOT to push

- Records that cannot be enriched (no email, no linkedin_url) — push the run interaction listing them, but NOT a person/company record.
- `[unverified — needs check]` — see provenance routing; person record is NOT patched.
- `[hypothetical]` — never.
- Run that produced 0 enrichments (all already-fresh) — push the run record; tag `#noop-already-fresh`.
- Verifier returned 100% `unknown` (verifier outage suspected) — abort push; surface for retry.
