---
name: discovery-call-prep
description: Produce a 1-page founder/AE briefing for an upcoming discovery call with MEDDPICC slots, discovery questions, objection prep, and competitive context. Use when the user says "prep me for this call", "brief me for the meeting", "discovery call tomorrow", or "refresh the briefing."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Conversations, Discovery-Prep, Briefing, MEDDPICC]
    related_skills: [reply-classification, objection-handling-library, pipeline-stages, handoff-protocol]
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

# Discovery Call Prep

Produce a 1-page founder/AE briefing for an upcoming discovery call: recipient profile, MEDDPICC slots, 9 discovery questions, 3 pre-staged objections, competitive context, and recommended agenda. Hard ceiling: ≤450 words.

## When to Use

- Discovery call booked and briefing needed
- Call rescheduled and prior briefing is stale (>48h)
- High-stakes Tier-1 call needs deep brief
- 5+ calls on the calendar — batch prep
- Founder hand-off from SDR cadence
- User says "prep me for this call" or "brief me for the meeting"

## Quick Reference

| Concept | Value |
|---|---|
| Briefing length | 1 page (≤450 words / single screen) |
| MEDDPICC 8 slots | Metrics / Economic Buyer / Decision Criteria / Decision Process / Paper Process / Identify Pain / Champion / Competition |
| Discovery questions | 3 per genre: open-discovery / pain-quantify / next-step (9 total) |
| Objection prep | 3 most-likely objections with pre-staged responses |
| Briefing freshness | ≤48h at call time; stale → re-prep |
| Competitive context | 1–3 likely competitors with 1-line counter-positioning each |

## Procedure

1. **Validate inputs + assemble profile.** Read meeting context + lead record + cadence/reply thread. Confirm meeting <48h. Profile ≤80 words: name, title, company, ICP tier+score, hook, most-recent reply. See `${HERMES_SKILL_DIR}/references/profile-template.md`.
2. **Populate MEDDPICC slots.** Fill from existing intel (function-1 + function-2 data). Each slot: populated or `unknown — ask`. See `${HERMES_SKILL_DIR}/references/meddpicc-slots.md`.
3. **Generate 3 questions per genre.** Open-discovery (current state), pain-quantify (cost of doing nothing), next-step (decision process/champion/timeline). Anchor to verified pain.
4. **Pre-stage 3 objections + competitive context.** Pull from objection-handling-library. 1–3 likely competitors with counter-positioning lines.
5. **Recommend call agenda + push.** 3 bullets: 5min context / 15min pain-quantify / 5–10min next-step. Push briefing as `interaction:research`. PATCH person with timestamps. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- 8-page briefings — founder reads first paragraph only; 1 page is the discipline
- Including open rate — Apple MPP made it noise; reply rate is the signal
- Inventing MEDDPICC slot content — unknown is honest; ask in the call
- Stale briefing — >48h → re-prep cheaply
- Missing reply context — founder needs "they replied to Touch 2 with X"
- Over-prepping objections — 3 likely is enough; 8 is paralysis

## Verification

1. Total word count ≤450; every named entity has provenance
2. MEDDPICC slot content traces to real data or `unknown`
3. Questions reference verified pain anchors (not generic)
4. 3 objections + 9 questions + 1–3 competitors all present
5. Freshness timestamp ≤48h
