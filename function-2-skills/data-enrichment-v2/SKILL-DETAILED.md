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

Decorate raw Lead records — typically from a sourcing skill or a BYO list — with verified email statuses, phone numbers (mobile/landline classified), normalized social links, and citable personalization hooks. The output is a Lead record `lead-scoring` can score with confidence and `cold-email-sequence` (function-3) can write a 25–50-word opener against without inventing context.

> *The worked example uses a fictional product (HelpdeskPro) for illustration. The verifier waterfall, hook-capture rules, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Lead schema, source adapter contract, three-mode pattern, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`. This skill assumes it.*

## Purpose

Sourcing skills produce *candidate* records — names, titles, claimed emails — but most fields aren't trustworthy at outreach time. Email verification rates from third-party databases are optimistic; phone numbers are stale; "personalization hooks" mentioned in raw output are usually agent-invented. This skill is the gate: verify what's verifiable, classify what isn't, capture hooks only when they have a citable source, and tag everything per the function-2 provenance contract so downstream skills know what they can trust.

## When to Use

- "Verify these 500 emails before we send."
- "We have 200 leads but no phone numbers."
- "Find a personalization hook for each of these prospects."
- "Re-verify the leads we sourced 6 months ago."
- "Clean up this BYO list before scoring."
- "Apollo gave us 'verified' emails; should we trust them?"
- Pre-scoring quality gate after any sourcing run.
- Pre-outreach freshness pass before high-effort sequences.

### Do NOT use this skill when

- The list has no `email` and no `linkedin_url` — there's nothing to verify or hook off. Run `data-enrichment` AFTER a sourcing skill, not as one.
- The user wants to score without verification (rare, sometimes urgent) — skip directly to `lead-scoring` with `email_status: unverified` carried through.
- The verification load is < 20 records — manual is faster than configuring a verifier.
- The records are already enriched within the freshness window (≤90 days for emails, ≤180 days for hooks).

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Lead records | yes | Output of any sourcing skill or BYO file | Must conform to function-2 Lead schema. |
| 2 | Verifier access | one of: API key / CSV upload / "best-effort" | env: `MILLION_VERIFIER_API_KEY` / `NEVERBOUNCE_API_KEY` / `ZEROBOUNCE_API_KEY` / `HUNTER_API_KEY` | Determines mode (§3 of conventions, applied to enrichment). |
| 3 | Hook-source permissions | yes | user | Booleans for: `linkedin_recent_posts`, `news_search`, `podcast_guest_search`, `company_blog_scrape`, `g2_review_search`. Defaults: news + linkedin if available, others off. |
| 4 | Cost budget | yes (default `SOURCING_RUN_USD_CAP=$25`) | env or user | Verification + enrichment combined; aborts above cap without override. |
| 5 | Run purpose tag | yes | user | One short string for cost attribution and replay. |
| 6 | Freshness override (optional) | no | user | "Re-verify even records ≤30 days old" — for high-stakes runs. |

### Fallback intake script

> "I'll enrich these leads in three passes: email verification, phone discovery, and personalization-hook capture. Each can run in API mode (if a key is set), via CSV upload (if you've already verified externally), or best-effort (flag everything `[unverified — needs check]`).
>
> Two questions: which hook sources are you comfortable with — LinkedIn recent posts, news search, company blog, podcast guest lists? And what's the cost cap? (default $25/run)"

### Input validation rules

- Lead records missing `email` AND `linkedin_url` → cannot be enriched; surface as a "skip list" and recommend `lead-sourcing-*`.
- No verifier configured AND no CSV upload → Best-effort mode: re-classifies obvious patterns (`info@` → role-based; `@gmail.com` for B2B contact → personal-email flagged) but cannot promote `email_status` past `unverified`. Run summary warns no real verification happened.
- Hook permission flags all `false` → skill enriches emails/phones only; sets `personalization_hook: null` on every record with `[unverified — needs check]` reason "no hook sources permitted".
- Records already verified within freshness window AND no override → skip them, count in summary as `skipped_fresh`.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Email verification waterfall** (industry-standard, formalized) | Crewm8 (compiled from MillionVerifier / NeverBounce / ZeroBounce documentation) | Syntax → MX record → SMTP handshake → catch-all detection → role-address detection. Each step is a gate; failing any gate downgrades the verdict. |
| **Catch-all domain rule** (industry-standard) | n/a — convention across verifiers | Domains accepting any address mark every email "valid" syntactically. Treat as `email_status: catch-all-domain`, never `verified`. Replies are the real validation. |
| **Verified hook rule** (house-built, derived from cold-email research) | Crewm8 — informed by *Cold Email Wizardry* (Lavender, public essay on the 9-second / 25–50-word constraint) | A personalization hook ships ONLY with a citable source URL. No URL → no hook. The 9-second reading budget means hooks must be specific + recent + provable, or they read as fabricated and trigger the recipient's mental spam filter. |
| **GDPR legitimate-interest tagging** (statute-derived) | EU Regulation 2016/679 Recitals 47, 70 | EU/UK contact → tag `gdpr_basis: legitimate-interest`; flag opt-out mechanism required at outreach time. |

## Tools and Sources

### Email verification (waterfall — try in order, lowest cost first)

| Tool | Cost / 1000 | Notes |
|---|---|---|
| MillionVerifier | ~$1.50 | Cheapest, accurate; primary recommendation for batch. |
| NeverBounce | ~$3 | Slightly higher accuracy on edge cases; secondary. |
| ZeroBounce | ~$5 | Highest cost, "AI scoring" for risky cases; tertiary. |
| Hunter Verifier | included w/ Hunter API | When already pulling email patterns from Hunter. |

### Phone discovery

| Tool | Notes |
|---|---|
| Hunter (find phone) | Often returns landline/main; mobile rare. |
| Apollo (already pulled) | Sometimes has mobile flagged; carry over the `phone_status: mobile` if Apollo provided it. |
| Lusha | Mobile-rich but expensive (~$0.10/contact). |
| ZoomInfo | Mobile-rich, enterprise pricing. |

### Personalization-hook sources

| Source | Permission flag | What it gives |
|---|---|---|
| LinkedIn recent posts (last 90d) | `linkedin_recent_posts` | A sentence the prospect actually wrote — best hook quality. Requires Sales Nav or ApiFy with session. |
| News / press search (Google CSE, SerpAPI) | `news_search` | Recent press mentions, funding, hires, RFPs. |
| Company blog | `company_blog_scrape` | Public posts authored by the prospect (rare but valuable). |
| Podcast guest lists | `podcast_guest_search` | The prospect appeared on a podcast in the last 12 months — very high open-rate. |
| G2 review profile | `g2_review_search` | Public reviews the prospect (or someone at their company) wrote about a competitor. |

### Source priority rule

For any single field: **live verifier within last 30 days** > **CSV with verifier results** > **upstream sourcing skill's flag** > **agent inference (`[unverified — needs check]`)**. Never fabricate a verifier verdict; never invent a hook URL.

## Procedure

### 1. Triage the input batch

Group records by enrichment need: (a) needs email verify only, (b) needs phone, (c) needs hook, (d) all three, (e) already-fresh-skip. Surface counts to user. **Rationale**: knowing the per-lead operation count drives cost estimate accuracy.

### 2. Cost-quote across all three passes

`discover_email_verify(records) + discover_phone(records) + discover_hook(records, permissions)` → combined estimate. Surface to user with per-pass breakdown. **Rationale**: enrichment is cheaper per-lead than sourcing, but bulk costs add up; user decides which passes to skip if budget tight.

### 3. Email verification waterfall

For each record with an email:
- Syntax check (cheap, local).
- MX record lookup (cheap, local).
- Verifier API call → returns one of: `valid`, `invalid`, `risky`, `catch-all`, `role-based`, `unknown`.
- Map to Lead schema `email_status`: `valid` → `verified`; `risky`/`unknown` → `risky`; `catch-all` → `catch-all-domain`; `role-based` → `role-based`; `invalid` → `invalid`.
- Stamp `provenance_email: [verified: <verifier>:run_<id>]` for `valid`; `[unverified — needs check]` for `risky`/`unknown`.

**Rationale**: this is the most consequential operation in the skill — wrong here = bounced sends + reputation damage to the sending domain.

### 4. Phone discovery + classification

For each record without a verified phone:
- If upstream sourcing skill flagged a phone, classify it (mobile vs landline vs voip) using a lookup service.
- Else attempt Hunter / Lusha (cost-permitting and permitted).
- Stamp `phone_status: mobile | landline | voip | dnc | unverified | invalid`.
- Cross-reference DNC list if `is_us` and phone discovered.

**Rationale**: cold-call (function-3) needs mobile-vs-landline distinction; SMS needs explicit consent (TCPA).

### 5. Personalization-hook capture

For each record (subject to permission flags):
- Pull last 5–10 LinkedIn posts (if permitted + tool available); pick the most recent that's substantive (not a repost).
- Search news for `"<contact_name>" "<company>"` in last 90 days; pick top result with permalink.
- Search podcast directories for `<contact_name>` as guest in last 12 months.
- For each candidate, capture: source URL, source date, one-sentence summary in the prospect's own words (verbatim quote preferred).
- Stamp `provenance` `[verified: <source>]` IF a permalink was captured; otherwise NULL the hook and `[unverified — needs check]` the reason.

**Rationale**: the verified-hook rule is the single biggest defense against fabricated openers in function-3. If the agent can't cite, it can't write a "saw your post on..." line.

### 6. Compliance pass

Per §7 of conventions: tag EU/UK contacts `gdpr_basis: legitimate-interest`; flag personal-email B2B contacts (`@gmail.com` etc. paired with company domain mismatch); confirm `phone_status: dnc` strips the phone from the active list.

### 7. Dedup re-check

After enrichment, some records may now be merge-candidates that weren't before (e.g., a freshly-found `linkedin_url` matches an existing record). Re-run dedup against CRM; log merges. **Rationale**: enrichment fills the merge keys; dedup must run again.

### 8. Push patched records to CRM

Per §9 of conventions: PATCH existing person/company records with new email_status, phone, phone_status, linkedin, hooks. Push an `interaction:research` per run with the verification log + provenance summary. Records still `[unverified]` after enrichment go to review queue.

### 9. Emit the run summary + missing-fields report

One-screen output: emails verified / risky / invalid; phones found / DNC; hooks captured (with-URL count) vs hook-failed (no-URL count); cost spent; missing-fields report (records that still lack email or hook); recommended next skill (`lead-scoring`).

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  inputs:
    record_count: <int>
    source_run_ids: [<uuid>, ...]   # traces back to upstream sourcing runs
  passes_run: [email | phone | hook]
  cost:
    email_verify_usd: <float>
    phone_discovery_usd: <float>
    hook_capture_usd: <float>
    total_usd: <float>
    cap_usd: <float>
  results:
    email:
      verified: <int>
      risky: <int>
      catch_all: <int>
      role_based: <int>
      invalid: <int>
      already_fresh_skipped: <int>
    phone:
      mobile_found: <int>
      landline_found: <int>
      voip_flagged: <int>
      dnc_stripped: <int>
      not_found: <int>
    hook:
      with_citable_url: <int>
      no_citable_url_skipped: <int>
  missing_fields_report:
    no_email_no_linkedin: <int>   # cannot be enriched; surface to user
    still_no_hook: <int>
  warnings: [<string>]
  next_skill_recommendation: <lead-scoring | re-source-via-X | etc.>

leads:
  # PATCHed records — only fields that changed are highlighted
  - lead_id: <uuid>
    email_status: verified | risky | invalid | catch-all-domain | role-based
    provenance_email: [verified: million-verifier:run_<id>]
    phone: <e164>
    phone_status: mobile | landline | voip | dnc | unverified
    provenance_phone: <...>
    linkedin_url: <if newly found>
    personalization_hook:
      text: "<verbatim or summary, dated, sourced>"
      source_url: <permalink>
      source_date: <ISO>
      provenance: [verified: <source>]
    freshness_date: <ISO>
```

## Worked Example

> *All entities below are tagged `[hypothetical]` — fictional, illustrative.*

**User prompt**: "I have 50 leads from a recent sourcing run for HelpdeskPro [hypothetical]. Verify their emails and capture personalization hooks. MillionVerifier and SerpAPI are configured."

**Step 1 — Triage**: 50 records loaded.
- 50/50 have email (need verify).
- 12/50 already have phone (skip phone pass for those).
- 50/50 need hook (none captured upstream).
- All 50 fit within 30-day freshness; no skips.

**Step 2 — Cost quote**:
> "Email verify: 50 × $0.0015 = $0.08 (MillionVerifier).
> Phone discovery: 38 × $0.05 = $1.90 (Hunter find-phone).
> Hook capture: 50 × ~$0.04 SerpAPI calls + ~$0.02 LinkedIn fetch = ~$3.00.
> Total: ~$4.98. Cap: $25. Proceed?"

User: "Yes."

**Step 3 — Email waterfall**:
| Result | Count |
|---|---|
| valid → `verified` | 31 |
| risky → `risky` | 8 |
| catch-all (e.g. `@apple.com`-style) → `catch-all-domain` | 5 |
| role-based (e.g. `info@helpdeskpro-customer.com`) → `role-based` | 4 |
| invalid → `invalid` | 2 |

For one record:
```yaml
contact_name: "Theo Park" [hypothetical]
email: "theo@northstar-cs.com" [hypothetical]
email_status: verified   # was 'unverified' before this run
provenance_email: [verified: million-verifier:run_2026-05-04T15:33]
```

**Step 4 — Phone discovery**: 38 records lacking phones run through Hunter find-phone:
- Mobile found: 9
- Landline found: 14
- Not found: 15
1 mobile cross-checked against US DNC and stripped (`phone_status: dnc`, phone field nullified).

**Step 5 — Hook capture** (permission flags: `linkedin_recent_posts: false` (no Sales Nav available), `news_search: true`, `podcast_guest_search: true`):
- 50 records → SerpAPI search `"<contact_name>" "<company>" site:linkedin.com OR (news 2025..2026)`.
- 31/50 → at least one citable result with permalink.
- 19/50 → no result; `personalization_hook: null` with `[unverified — needs check]` reason "no citable source found in last 90d".

For one record (with hook):
```yaml
contact_name: "Theo Park" [hypothetical]
personalization_hook:
  text: "Northstar CS [hypothetical] just hired their first VP of Customer Experience (announced 2026-04-19)."
  source_url: "https://news.example.com/northstar-vp-cx-hire-2026" [hypothetical]
  source_date: 2026-04-19
  provenance: [verified: serpapi-news]
```

For one record (without hook):
```yaml
contact_name: "Mira Chen" [hypothetical]
personalization_hook: null
provenance_hook: [unverified — needs check]
hook_skip_reason: "no news/podcast result for contact in last 90d"
```

**Step 6 — Compliance**: 0 EU contacts; 1 personal-email B2B contact flagged for review (Theo's company on `@gmail.com` — likely freelance arrangement, escalate).

**Step 7 — Dedup re-check**: 2 newly-discovered LinkedIn URLs collide with existing CRM records → 2 merges logged.

**Step 8 — Push**: PATCHed 48 person records (2 dropped — invalid emails, no hook source); 1 interaction:research run record; 19 records routed to review queue (`#unverified-hook #review-required`).

**Step 9 — Run summary**:
```
HelpdeskPro Enrichment Run [hypothetical]
Run ID: enrich_2026-05-04_t3p...
Inputs: 50 records from sourcing run apollo_2026-05-04_h7k
Cost: $4.86 (cap $25)
Email: 31 verified / 8 risky / 5 catch-all / 4 role-based / 2 invalid
Phone: 9 mobile / 14 landline / 15 not found / 1 DNC-stripped
Hook: 31 with citable URL / 19 no source (review queue)
Compliance: 0 EU / 1 personal-email flag
Dedup merges: 2
Recommended next: lead-scoring (31 leads ready for Tier-1 send; 19 await human-review hook)
```

## Heuristics

- **Verify before scoring, score before outreach.** Scoring without verified emails leads to inflated Tier-1 counts that bounce in send.
- **Catch-all domains masquerade as verified.** `@apple.com`, `@meta.com`, `@goldmansachs.com` accept any pattern. If the verifier returns "valid" for a catch-all domain, downgrade to `catch-all-domain` in the Lead schema.
- **Hook freshness > hook depth.** A 1-week-old hire announcement beats a 6-month-old podcast appearance for opener quality.
- **Don't over-pay for unknowns.** A verifier returning `unknown` repeatedly on the same record means more spend won't change the answer; classify as `risky` and move on.
- **The verifier is not your friend at scale.** If you're verifying 5,000 emails monthly, the verifier sees patterns you don't (rotating IPs, throttled MX checks). Cross-rotate verifiers monthly to avoid systematic blind spots.
- **Personal email for B2B contact = signal.** A `@gmail.com` paired with a real company title is usually a freelancer or a side hustle — score-down, not delete.
- **Mobile is precious.** Mobile-discovered phones are the single highest-leverage enrichment for SDR cadence; protect them with DNC compliance.
- **Hook prose ≠ hook truth.** "Saw your insightful post on X" without a URL is a fabricated opener. The skill must NULL the hook field and route to review queue rather than ship a clichéd quote with no source.

## Edge Cases

- **No verifier configured.** Best-effort mode: pattern match (`info@`, `@gmail.com`), MX record check, but cannot promote past `email_status: unverified`. Skill flags everything `[unverified — needs check]` per the tool-grounding rule. Recommend the user configure MillionVerifier (cheap) before next run.
- **Verifier returns 100% catch-all.** Apollo or sourcing tool likely fed a domain list of catch-alls. Surface this; recommend re-sourcing with stricter firmographic.
- **Lead has multiple emails (work + personal).** Verify both. Prefer work email for outreach; keep personal in reserve. Cold email skill picks based on play.
- **EU/UK contacts.** Tag `gdpr_basis: legitimate-interest`. Hooks-from-LinkedIn-public-posts are within ToS; hooks-from-LinkedIn-private-content are NOT. Restrict permission flag accordingly.
- **Record was sourced 12 months ago.** Re-verify everything; re-pull title from LinkedIn (people change roles). Treat as a near-fresh sourcing run, not a quick patch.
- **Hook from a competitor's content.** A prospect's G2 review of `<competitor>` is a high-quality hook for a competitive opener — but only if the review is public. Tag `hook_class: competitive-review` for downstream cold-email prompt selection.
- **Verifier disagreement.** If MillionVerifier says `valid` and NeverBounce says `risky`, the lower is authoritative (be conservative). Log the disagreement for monthly verifier audit.
- **Multi-language hook source.** Hook text in non-English: capture verbatim + provide one-sentence English summary; preserve the original-language URL. Cold-email skill picks language at write time.
- **Large batch (>2000 records).** Chunk into 500-record sub-batches; surface per-batch progress; cap at `SOURCING_RUN_RECORD_CAP`.
- **Records still missing email after Hunter pattern guess.** Pattern guess + verifier check → if `verified`, promote to active; if `risky`, route to review.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Verifier auth fails (401) | "Invalid API key" | Confirm key in env; do NOT retry silently; offer to fall back to next verifier in waterfall. |
| Verifier rate limit (429) | "Too many requests" | Backoff (5s, 15s, 45s); fail after 3 retries; resume from last batch. |
| Verifier returns 5xx | Service degraded | Retry with backoff; if still failing, route batch to next verifier (NeverBounce → ZeroBounce). |
| MX lookup fails (no DNS) | DNS unavailable | Skip MX, proceed with verifier; mark records `[unverified — needs check]` for the MX dimension. |
| Hook search returns 0 results | News API empty | Try LinkedIn (if permitted) → podcast (if permitted) → company blog (if permitted) → null hook. Don't fabricate. |
| Hook search rate-limited | SerpAPI 429 | Backoff; lower batch concurrency; warn run summary. |
| LinkedIn fetch blocked | scraper banned | Disable `linkedin_recent_posts` for the rest of the run; flag in summary; recommend manual hook capture. |
| CSV upload encoding mismatch | mojibake | UTF-8 → CP1252 → Latin-1 fallback; warn user. |
| Cost cap hit mid-run | partial enrichment | Stop; persist what was enriched; flag remaining batch as `pending_enrichment` on the run record. |
| Push to CRM fails (network) | 4xx/5xx from agentic-app | Persist results to local JSON; retry on user request; never silently lose. |
| Phone discovery returns DNC | record stripped | Strip phone from active record; preserve `phone_status: dnc` for audit; surface count in summary. |
| Permission flag denied mid-run | user revokes hook source | Preserve hooks captured before revocation; null out incomplete; warn run summary. |

## Pitfalls

- **Trusting upstream verifier flags.** Apollo's "verified" is hint-quality. Always re-verify with a real verifier before high-effort sends.
- **Inventing hooks.** "Saw your post on X" with no URL is a hallucinated opener. Hooks ship with citable URL or they ship null.
- **Verifying once and forgetting.** Email lists decay ~30%/year; re-verify the active list quarterly.
- **Spending on records that can't be enriched.** Cap budget per record; if email AND linkedin_url are absent, surface and skip.
- **Catch-all noise.** `@apple.com` style domains will mark every email valid; treat as `catch-all-domain` regardless of verifier verdict.
- **DNC complacency.** TCPA fines are per-violation. Strict strip on `phone_status: dnc`.
- **Hook-source overreach.** Scraping LinkedIn private posts violates ToS. Only public posts (Sales Nav search results, public profile activity) are permitted.
- **Pattern-guessed emails treated as verified.** Hunter's pattern-guess is "best guess based on company patterns" — verify it before promoting past `risky`.
- **Mobile/landline confusion.** Sending SMS to a landline isn't billed but isn't delivered; cold-call to a mobile flagged DNC is illegal.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (contact names, hook URLs, news sources, dates, dollar figures) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. No verifier or news API → default to `[unverified — needs check]`. NEVER invent a "saw your post on..." opener.
- **Silent budget overspend.** Enrichment is cheaper per-record than sourcing but cumulative cost adds up; cap is a hard stop.

## Verification

The enrichment run is real when: (a) every patched record's `email_status` traces to a verifier run_id; (b) every personalization hook has a permalink that resolves; (c) the missing-fields report lists which records still need work and why; (d) `lead-scoring` can apply BANT/CHAMP and the 100-pt scorecard without `[unverified — needs check]` field gaps causing score caps; (e) re-running the same input batch the next day produces the same verdicts ± real-world drift.

Negative test: pick 5 hooks at random from the run output. Click each `source_url`. If any 404, return a paywall, or describe an unrelated event, the hook capture pass is broken.

## Done Criteria

1. All input records triaged (verify-needed / phone-needed / hook-needed / fresh-skip) with counts surfaced.
2. Cost quoted across all three passes; user authorization received.
3. Every record's `email_status` traces to a verifier run_id (or `[unverified — needs check]` if best-effort mode).
4. Phone status classified (mobile / landline / voip / dnc / unverified / invalid).
5. Personalization hooks ship with permalink + date OR are NULL with reason — no fabricated openers.
6. Compliance pass run (GDPR, DNC, role-address).
7. Dedup re-checked post-enrichment; merges logged.
8. `[unverified — needs check]` records routed to review queue.
9. Run summary one-screen; recommends next skill (`lead-scoring`); cost stayed under cap.

## Eval Cases

### Case 1 — full API mode, sourcing-handoff

Input: 50 leads from `lead-sourcing-apollo` run, MillionVerifier + Hunter + SerpAPI configured, $25 cap.

Expected: ~95% of records verified or classified definitively; ~50–70% with citable hooks; <5% routed to review queue. Run summary shows verifier breakdown and hook source attribution.

### Case 2 — best-effort mode (no verifier)

Input: 200 leads from BYO CSV; no verifier API keys.

Expected: all records remain `email_status: unverified`; pattern detection still flags `role-based` emails and personal-email B2B mismatches; no hook capture (no SerpAPI/LinkedIn keys); 100% records routed to review queue with `[unverified — needs check]`. Recommend configuring MillionVerifier before next run.

### Case 3 — re-verification of stale list

Input: 500 leads sourced 9 months ago; freshness override enabled.

Expected: ~30% of emails downgrade (`verified` → `risky` or `invalid`) due to job changes / domain changes; ~10% of records get a new LinkedIn URL via re-fetch; hooks all re-captured (old hooks expired). Surface attrition rate as a signal — if >40% of emails decayed, lead source has quality issues; flag to `channel-performance`.

## Guardrails

### Provenance (anti-fabrication)

Per §8 of conventions: every patched field carries provenance. Email status comes from a verifier with a run_id (`[verified: million-verifier:run_<id>]`) or is `[unverified — needs check]`. Personalization hooks ship `[verified: <source-url>]` or are NULL — there is no middle ground. Worked-example fictional entities tagged inline.

The skill MUST NOT promote `email_status` past `unverified` without a verifier verdict. The skill MUST NOT generate a hook string without a permalink. These are hard rules; failure to comply is a contract violation.

### Evidence

Every hook entry has: source URL, source date, provenance tag, the verbatim or summarized text. Every email status has: verifier name + run_id. Every phone status has: classification source.

### Scope

This skill enriches and verifies. It does NOT score (lead-scoring), source new leads (lead-sourcing-*), or write outreach (function-3). Avoid scope creep — surface a recommendation rather than doing the next skill's job.

### Framing

Run summary uses operational language. Hook text preserves the prospect's own words; agent does not paraphrase aggressively (which often introduces drift).

### Bias

Verifier accuracy varies by region (lower for non-US/EU domains). Don't aggressively strip records on a single verifier's opinion if the contact is from an under-served region; cross-check with a second verifier or surface as `risky`.

### Ethics

LinkedIn ToS: only public-profile content. GDPR: legitimate-interest tag mandatory for EU contacts. CAN-SPAM: physical-address and opt-out are downstream concerns but `is_us` flag must be set for the cold-email skill to apply.

### Freshness

Email verifies within last 30 days, hooks within last 90 days. Records older than half-life flagged for re-enrichment on next run. Stale data = bounced sends + reputation damage.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Records enriched, ready to score | `lead-scoring` | Patched Lead records + ICP scorecard |
| Too many records still missing email/linkedin → re-source | `lead-sourcing-apollo` / `lead-sourcing-linkedin` | Original ICP filters + missing-fields report |
| BYO list still lacks core fields after enrichment | `lead-sourcing-web` (research mode) | Company list + missing-fields report |
| Run shows verifier disagreement patterns | `channel-performance` (planned, function-6) | Verifier run logs across multiple runs |
| Hook capture rate < 30% — need richer signal sources | `lead-sourcing-linkedin` (Sales Nav for hooks) | Records lacking hook + permitted hook sources |
| List is stale (>9 months) | `data-enrichment` again with freshness override | Same record set |

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
| `[user-provided]` or `[verified: <source>]` | PATCH per the standard mapping (person field updates land on the existing record). |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #data-enrichment` tags. The person record is NOT patched — hook field stays null, email_status stays whatever it was. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified-hook push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #data-enrichment #hook-missing",
    "relevance": "Hook capture failed for Mira Chen [unverified — needs check]: no news/podcast result in last 90d. Person record's hook field left null. Recommend re-attempt with linkedin_recent_posts permission or manual capture.",
    "source": "skill:data-enrichment:v2.0.0"
  }'
```

### When NOT to push

- Records that cannot be enriched (no email, no linkedin_url) — push the `interaction:research` run record listing them, but NOT a person/company record.
- `[unverified — needs check]` — see provenance routing; person record is NOT patched.
- `[hypothetical]` — never.
- Run that produced 0 enrichments (all already-fresh) — push the run record; tag `#noop-already-fresh`.
- Verifier returned 100% `unknown` (verifier outage suspected) — abort push; surface for retry.
