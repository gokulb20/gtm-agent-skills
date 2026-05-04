---
name: pipeline-stages
description: Move deals through an 8-stage pipeline using deterministic stage-gate rules and MEDDPICC slot completion criteria. Use when the user says "advance this deal", "audit pipeline stages", "which deals are stuck", or "move to next stage."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Pipeline, Deal-Management, Stages, MEDDPICC]
    related_skills: [reply-classification, discovery-call-prep, handoff-protocol, crm-hygiene, revenue-forecasting]
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

# Pipeline Stages

Move deals through 8 canonical pipeline stages with deterministic gates: New → Contacted → Engaged → Meeting → Discovery → Proposal → Closed-Won / Closed-Lost. Hard rule: deals cannot advance until gates are met; stuck deals get flagged with the specific missing element.

## When to Use

- Reply classified positive — advance deal
- Audit pipeline — which deals are in wrong stage
- Deal signed — move to Closed-Won
- Bulk classify active deals into correct stages
- Stuck deal investigation — why hasn't this advanced
- User says "advance this deal" or "audit pipeline stages"

## Quick Reference

| Stage | Entry gate | Avg duration |
|---|---|---|
| New | Lead created | <7d |
| Contacted | ≥1 Touch sent | 14–21d |
| Engaged | Reply received (not unsubscribe/not-interested) | 7–14d |
| Meeting | Discovery call scheduled | <14d |
| Discovery | Meeting held; ≥5/8 MEDDPICC slots | 14–30d |
| Proposal | Proposal sent; deal value confirmed | 14–60d |
| Closed-Won | Contract signed | n/a |
| Closed-Lost | Explicit no OR 90d silence post-Proposal | n/a |

| Concept | Value |
|---|---|
| Stage-skip prohibition | Cannot skip stages; only exception is jump to Closed-Lost |
| Stuck-deal detection | Time-in-stage >2× avg → flag with missing element |
| Discovery→Proposal gate | All 8 MEDDPICC slots populated (inferred acceptable) |
| Closed-Lost reasons | no-budget / no-authority / no-need / no-timing / lost-to-competitor / unresponsive |

## Procedure

1. **Validate inputs.** Read deal record + trigger event + stage definitions. Confirm trigger maps to a transition or audit request.
2. **Check stuck status.** Pull current stage; compute time-in-stage; flag if >2× avg.
3. **Match trigger to candidate transition.** reply-positive → advance; meeting-booked → advance; proposal-sent → advance; contract-signed → Closed-Won; not-interested/90d silence → Closed-Lost. See `${HERMES_SKILL_DIR}/references/stage-gates.md`.
4. **Apply stage gates.** Check entry criteria for target stage. If gates met → advance. If NOT met → block; surface missing element; flag for crm-hygiene or discovery-call-prep.
5. **Handle edge cases.** Reverse transitions allowed but logged. Stage-skip prohibited unless Closed-Lost.
6. **Bulk mode (when applicable).** Iterate every active deal, replay gate logic, surface wrong-stage deals. Don't auto-correct without authorization. See `${HERMES_SKILL_DIR}/references/bulk-audit.md`.
7. **Update deal + push.** PATCH deal with new stage + timestamp. Push `interaction:stage-change` with trigger + duration. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Vague stage definitions — each needs an explicit entry event, not "feels engaged"
- Auto-advancing without gate checks — positive reply ≠ Meeting stage without booked meeting
- Stage-skipping — Discovery → Closed-Won without Proposal is data corruption
- Letting stuck deals linger — surface AND name the missing element
- Closed-Lost without a reason — lost-reason feeds icp-refinement-loop
- Bulk auto-correct — always require user authorization before mass stage updates

## Verification

1. Every transition has documented trigger + gate-check result
2. Stuck-deal flags name specific missing elements
3. No stage-skips except to Closed-Lost
4. Deal record PATCHed; interaction:stage-change pushed
