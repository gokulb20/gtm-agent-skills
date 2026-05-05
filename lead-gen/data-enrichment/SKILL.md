---
name: data-enrichment
description: Enrich raw Lead records with verified emails, phone numbers, social links, and citable personalization hooks via a verifier waterfall, deliverability classification, and source-tracked hook capture. Use when a sourcing skill has produced a list with unverified emails, missing phones, or no hooks; when a BYO list needs schema repair; or when stale records need re-verification before outreach.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [GTM, Lead-Enrichment, Email-Verification, Personalization]
    related_skills: [lead-sourcing-apollo, lead-sourcing-clay, lead-sourcing-linkedin, lead-sourcing-web, lead-scoring, icp-definition]
    requires_tools: [terminal]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
      - key: gtm.sourcing_run_usd_cap
        description: Max spend per enrichment run
        default: "25"
      - key: gtm.sourcing_run_record_cap
        description: Max records per enrichment run
        default: "2000"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Data Enrichment

Decorate raw Lead records with verified email statuses, phone numbers (mobile/landline classified), normalized social links, and citable personalization hooks. The output is a Lead record `lead-scoring` can score with confidence and cold-email can write an opener against without inventing context.

## When to Use

- "Verify these 500 emails before we send"
- User has leads with unverified emails, missing phones, or no personalization hooks
- BYO list needs schema repair before scoring
- Stale records need re-verification before outreach
- Pre-scoring quality gate after any sourcing run
- Pre-outreach freshness pass before high-effort sequences

## Quick Reference

| Concept | Value |
|---|---|
| Three passes | Email verify → Phone discovery → Hook capture |
| Verifier waterfall | Syntax → MX → SMTP → catch-all → role-based detection |
| Email status enum | `verified` / `risky` / `catch-all-domain` / `role-based` / `invalid` / `unverified` |
| Phone status enum | `mobile` / `landline` / `voip` / `dnc` / `unverified` / `invalid` |
| Hook rule | Permalink + date OR null — no URL, no hook |
| Catch-all rule | Verifier "valid" + accept-all domain → `catch-all-domain` (never `verified`) |
| Freshness windows | Email: 90d; phone: 12mo; hook: 90d |
| Compliance | EU → `gdpr_basis: legitimate-interest`; DNC → strip phone; role-addresses → never Tier-1 |
| Push routing | PATCH person for verified; `interaction:research` only for `[unverified — needs check]` |

## Procedure

1. **Triage the input batch.** Group records: email-verify-only / phone / hook / all-three / fresh-skip. Surface counts.
2. **Cost-quote across passes.** Estimate email verify + phone + hook. User chooses passes if budget tight. Reference `${HERMES_SKILL_DIR}/references/` for verifier cost models.
3. **Email verification waterfall.** Syntax → MX → verifier API → map result to `email_status` enum. Stamp `provenance_email: [verified: <verifier>:run_<id>]` for valid; `[unverified — needs check]` for risky/unknown.
4. **Phone discovery + classification.** Hunter / Lusha lookup; classify mobile / landline / voip; cross-check DNC for US contacts. Stamp `phone_status`.
5. **Personalization-hook capture.** Within permission flags: LinkedIn posts → news search → podcast → company blog → G2 review. Capture source URL + date + verbatim text. **Hooks ship with permalink OR null.** Run `${HERMES_SKILL_DIR}/scripts/normalize_lead.py` for field updates.
6. **Compliance pass.** EU/UK → `gdpr_basis`; personal-email B2B flagged; `phone_status: dnc` strips phone.
7. **Dedup re-check.** Newly-discovered LinkedIn URLs / emails may collide with existing CRM. Run `${HERMES_SKILL_DIR}/scripts/dedup_leads.py`. Log merges.
8. **Push patched records.** Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. PATCH person fields for verified; `interaction:research` for unverified.
9. **Emit run summary + missing-fields report.** One-screen: per-pass results, costs, missing-fields, recommended next skill (`lead-scoring`).

## Pitfalls

- Trusting upstream verifier flags — Apollo's "verified" is hint-quality; always re-verify
- Inventing hooks — "Saw your post on X" with no URL is a hallucinated opener; ship null instead
- Catch-all noise — `@apple.com` style domains mark everything valid; treat as `catch-all-domain`
- DNC complacency — TCPA fines are per-violation; strict strip on `phone_status: dnc`
- Verifying once and forgetting — email lists decay ~30%/year; re-verify quarterly
- Pattern-guessed emails treated as verified — Hunter's pattern-guess is best-guess; verify before promoting

## Verification

1. Every patched record's `email_status` traces to a verifier run_id
2. Every personalization hook has a permalink that resolves
3. Missing-fields report lists which records still need work and why
4. `lead-scoring` can apply scorecard without `[unverified]` field gaps capping scores
