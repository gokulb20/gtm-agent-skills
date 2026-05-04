---
name: handoff-protocol
description: Hand off SAL-eligible leads from SDR to AE with a complete briefing package and SiriusDecisions SAL acceptance tracking. Use when the user says "hand off to AE", "handoff this deal", "SAL acceptance", or "SDR to AE transfer."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Pipeline, SDR-AE-Handoff, Briefing, SAL]
    related_skills: [reply-classification, discovery-call-prep, pipeline-stages, lead-scoring, objection-handling-library]
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

# Handoff Protocol

Package and deliver an SAL-eligible lead from SDR to AE with a complete briefing: 1-page briefing, MEDDPICC snapshot, conversation history, pre-staged objections, and explicit SAL acceptance criteria. Per SiriusDecisions/Forrester norms: handoffs are explicit acceptance events, not silent assignments.

## When to Use

- Positive reply + meeting booked — hand off to AE
- Tier-1 founder-led prospect ready for founder takeover
- Bulk handoff of campaign's positive replies
- AE rejected the handoff — reroute/fix
- Deal closed-won — hand off to CSM
- User says "hand off to AE" or "SAL acceptance needed"

## Quick Reference

| Concept | Value |
|---|---|
| Handoff package | 1-page briefing + MEDDPICC + conversation history + objections + SAL checklist |
| SAL acceptance criteria | ICP fit confirmed + trigger present + within half-life + DM/champion identified + no hard disqualifiers |
| Acceptance states | pending → accepted / rejected (with reason) / takeback |
| Rejection routing | Back to SDR with reason for fix-then-resubmit |
| Takeback rule | Allowed within 7d post-acceptance; after 7d needs manager approval |
| Briefing freshness | ≤24h at handoff (HANDOFF_FRESHNESS_HOURS=24) |

## Procedure

1. **Validate prerequisites.** Confirm SAL-eligible per lead-scoring or pipeline stage. Load receiving rep identity + preference. See `${HERMES_SKILL_DIR}/references/sal-criteria.md`.
2. **Pull/refresh briefing.** Pull discovery-call-prep briefing. Check freshness ≤24h. Stale → re-prep.
3. **Assemble handoff package.** 5 components: briefing, MEDDPICC snapshot, conversation history, pre-staged objections, SAL checklist. See `${HERMES_SKILL_DIR}/references/package-template.md`.
4. **Run pre-delivery SAL gates.** Verify 4 SAL criteria pass. If any fail, route back to SDR — don't deliver unaccept-able handoff.
5. **Deliver via rep's channel.** Slack DM / email / dashboard per preference. Include accept/reject mechanism.
6. **Track acceptance state.** pending → accepted (PATCH deal owner) / rejected (route to SDR with reason) / no response within 24h (escalate).
7. **Handle takebacks.** Within 7d: mark takeback, route back to SDR. After 7d: manager approval required.
8. **Push to CRM.** `interaction:handoff` with package + state + audit trail. PATCH deal owner on acceptance. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Silent handoffs — calendar invite without briefing = AE walks in cold
- Auto-accepting on silence — no reply ≠ accept; escalate
- Stale briefings at handoff — >24h → re-prep
- No rejection reason captured — require reason at rejection for learning
- Multiple AEs assigned same deal — single owner per deal

## Verification

1. Every handoff has delivery event + acceptance event
2. SAL pre-checks pass before delivery
3. Rejection reasons captured; deal owner PATCHed only on accept
4. Takeback events tracked with timestamps
