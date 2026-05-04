---
name: conversation-intelligence
description: Extract structured intel from call transcripts and reply corpora — competitor mentions, pricing pushback, feature requests, champion language, blocker signals — and aggregate into pattern-frequency alerts. Use when the user says "extract intel from transcript", "pattern aggregation", "competitor mentions trending", or "feature requests this month."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Pipeline, Conversation-Intelligence, Pattern-Mining, Transcripts]
    related_skills: [reply-classification, competitive-intelligence, revenue-forecasting, customer-feedback-analysis]
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

# Conversation Intelligence

Extract structured intel from unstructured conversation surfaces (Gong/Chorus/Grain/Fathom transcripts, reply text, meeting notes), aggregate into pattern-frequency alerts, and route per pattern class to downstream skills.

## When to Use

- Gong transcript just dropped — extract intel
- Pull patterns from a campaign's reply corpus
- Competitor mentions trending this quarter
- Feature requests aggregated — prioritize
- Champion language patterns across closed-won deals
- User says "extract intel from transcript" or "what patterns crossed threshold"

## Quick Reference

| Pattern class | Detection signal | Default routing |
|---|---|---|
| Competitor mention | Named competitor in transcript/reply | → competitive-intelligence |
| Pricing pushback | "expensive" / "out of budget" / dollar pushback | → revenue-forecasting + objection-handling-library |
| Feature request | "I wish" / "do you have" / named missing feature | → customer-feedback-analysis + product team |
| Champion language | Strong-affirmation phrases | → discovery-call-prep (champion-confirm) + kpi-reporting |
| Blocker signal | "IT/security/legal/procurement" gating | → discovery-call-prep (blocker-prep) + pipeline-stages |

| Concept | Value |
|---|---|
| Threshold defaults | Competitor: 3/30d / Pricing: 4/30d / Feature: 5/30d |
| Aggregation window | 30d rolling default |
| Confidence floor | <0.7 → flag for manual review; no auto-route |
| Verbatim rule | Every pattern must cite actual quote + source timestamp |

## Procedure

1. **Validate inputs.** Pull conversation source (transcript/reply/note). Confirm taxonomy + thresholds loaded. See `${HERMES_SKILL_DIR}/references/pattern-taxonomy.md`.
2. **Per-conversation extraction.** LLM-backed against 5-class taxonomy. Output: `{class, verbatim_quote, source_timestamp, confidence, related_entity}`. Confidence <0.7 → manual review.
3. **Per-conversation push.** Each extracted pattern → `interaction:research` with verbatim + source + class. PATCH person/company tags.
4. **Cross-conversation aggregation.** Pull all patterns within 30d window. Group by class + entity. Count frequency.
5. **Threshold check + alert.** Per class+entity: compare frequency to threshold. Crossed → emit alert routed to downstream skill. See `${HERMES_SKILL_DIR}/references/thresholds.md`.
6. **Route per pattern class.** Competitor → competitive-intelligence. Pricing → revenue-forecasting. Feature → customer-feedback-analysis. Champion → discovery-call-prep. Blocker → pipeline-stages.
7. **Emit run record.** `interaction:research` with corpus stats + threshold crossings. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Paraphrasing instead of verbatim — pattern records MUST contain actual quote
- Auto-routing low-confidence extractions — <0.7 → manual review only
- Double-counting same conversation across runs — dedup by transcript_id
- Treating competitor mentions as objections — "we considered X and rejected them" is positive intel
- Aggregation window too narrow — 7d misses trends; 90d includes stale signal

## Verification

1. Every extracted pattern has a verbatim quote + source reference
2. Threshold-crossing alerts have supporting evidence (per-quote list)
3. Routing to downstream skills happened for triggered alerts
4. Aggregation window dates explicit; per-conversation patterns dedup'd
