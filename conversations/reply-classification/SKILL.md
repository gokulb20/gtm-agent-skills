---
name: reply-classification
description: Classify inbound replies into a 9-label taxonomy with confidence scores and route to downstream skills. Use when the user says "triage replies", "classify inbox", "sort campaign responses", or "categorize inbound messages."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Conversations, Reply-Triage, Classification, Routing]
    related_skills: [objection-handling-library, discovery-call-prep, follow-up-management, pipeline-stages]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Reply Classification

Classify each inbound reply (email, LinkedIn, SMS, call disposition) into one of nine routing labels with confidence, then dispatch to the right downstream skill or manual review.

## When to Use

- Campaign generating reply volume that needs triage
- Bulk reply categorization for a sales rep or founder inbox
- Pre-discovery-call-prep confirmation of positive classification
- Low-confidence reply needs human review
- Founder inbox overwhelmed — sort hot vs warm vs dead
- User says "triage today's replies" or "categorize campaign responses"

## Quick Reference

| Concept | Value |
|---|---|
| 9-label taxonomy | positive / not-now / not-interested / wrong-person / unsubscribe / out-of-office / referral / question / unclear |
| Confidence floor | 0.75 default; below routes to manual review |
| Cadence-exit triggers | positive (handoff) / not-interested (12mo cooldown) / unsubscribe (forever) / wrong-person (re-enrich) |
| Pre-classify short-circuits | Auto-reply header → out-of-office; unsubscribe regex → unsubscribe; bounce → route to channel skill |
| Routing | positive → discovery-call-prep; objection → objection-handling-library; not-now/OOO → follow-up-management; referral → data-enrichment |

## Procedure

1. **Ingest reply.** Read text + headers + cadence context. Detect channel, sender, timestamp, parent Touch.
2. **Pre-classify on hard signals.** Auto-reply header → `out-of-office`. Unsubscribe phrases → `unsubscribe`. Bounce → route back to channel skill (not a reply).
3. **LLM-backed classification.** Pass reply + 1-line cadence context to LLM. Output: `{label, confidence, rationale, embedded_objection}`. See `${HERMES_SKILL_DIR}/references/taxonomy.md`.
4. **Confidence gate.** ≥0.75 → proceed. <0.75 → route to manual review queue with LLM best guess + rationale. Never auto-act on uncertain.
5. **Cadence-state effects.** positive/not-interested/unsubscribe → exit cadence. not-now → pause with resume date. wrong-person → exit + flag data-enrichment. question/referral → cadence continues + route reply.
6. **Dispatch to next skill.** positive → discovery-call-prep. embedded objection → objection-handling-library. not-now/OOO → follow-up-management. referral → data-enrichment. See `${HERMES_SKILL_DIR}/references/routing-map.md`.
7. **Push to CRM + emit run summary.** Per-reply `interaction:reply` with classification + confidence. PATCH person record with reply state. Run summary: total replies, label distribution, manual-review count. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Auto-acting on low-confidence classifications — always route <0.75 to manual review
- Confusing OOO with not-interested — pre-classify via header signals before LLM
- Missing embedded objections — "not now, already using X" is BOTH not-now AND competitor objection
- Treating bounces as replies — route to channel skill instead
- Ignoring cadence context — "yes" means different things at touch 1 vs touch 5
- Unsubscribe only on received channel — must exit ALL channels globally
- Multi-language assumption — classify in source language, translate summary only

## Verification

1. Every reply classified or routed to manual review (no silent drops)
2. No confidence <0.75 auto-acted on
3. Pre-classification rules applied before LLM call
4. Cadence-state effects propagated per label
5. Push to CRM emitted: per-reply interaction + person PATCH + run record
