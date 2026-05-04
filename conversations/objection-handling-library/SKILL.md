---
name: objection-handling-library
description: Match embedded objections to a 12-objection canonical library and produce ranked response variants with cadence-state recommendations. Use when the user says "handle this objection", "generate response variants", "match objection to library", or "we keep hearing X objection."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Conversations, Objection-Handling, Response-Variants, Sales-Frameworks]
    related_skills: [reply-classification, discovery-call-prep, follow-up-management, competitive-intelligence]
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

# Objection Handling Library

Match an embedded objection to a 12-objection canonical library, produce 2–3 response variants ranked by fit, and recommend a cadence-state action. Never invent library entries on the fly.

## When to Use

- Reply-classification flags an embedded objection
- A not-now reply needs a graceful response
- Objection patterns recur and need codified responses
- Sales reps need pre-approved objection templates
- User says "handle this objection" or "generate response variants"
- Library refresh after 30+ new objections collected

## Quick Reference

| Concept | Value |
|---|---|
| 12-objection library | already-using-competitor / no-budget / no-authority / no-need-now / bad-timing / happy-with-status-quo / tried-similar-failed / too-expensive / too-small / send-me-email / wrong-person / compliance-security-blocker |
| Match confidence floor | ≥0.7 to use library response; below = new-objection-pattern flag |
| Response frameworks | Feel-Felt-Found (empathy) / Re-discovery (Bosworth pain) / Time-shift (resume date) / Counter-position (Dunford reframe) |
| Variants per objection | 2–3 (light / medium / direct tone) |
| Cadence actions | resume-stated-date / nurture-90d / nurture-12mo / exit-permanent / re-enrich / discovery-prep |

## Procedure

1. **Validate inputs.** Read classified reply + cadence context + lead record. Confirm embedded objection present. If absent, recommend follow-up-management instead.
2. **Match against 12-library.** LLM-backed match with confidence per entry. Output: `{best_match, confidence, second_best}`. See `${HERMES_SKILL_DIR}/references/objection-library.md`.
3. **Confidence gate.** ≥0.7 → use library framework. <0.7 → flag new-objection-pattern; route to manual response; collect for refresh.
4. **Generate 2–3 response variants.** Pick framework per matched entry. Generate light/medium/direct tone variants. Each ≤80 words, one CTA. Reference verified context only. See `${HERMES_SKILL_DIR}/references/frameworks.md`.
5. **Recommend cadence-state action.** bad-timing → resume per date. already-using-competitor → nurture-90d. no-budget → nurture-90d + flag lead-scoring re-tier. compliance → discovery-prep mode.
6. **Capture intel for downstream.** Competitor mentions → competitive-intelligence. Pricing pushback → revenue-forecasting. Persistent pain → icp-refinement-loop.
7. **Push to CRM.** Per-objection `interaction:reply-response` with library match + variants + cadence action. PATCH person with new state. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Inventing library entries on the fly — flag as new-pattern instead
- Generic "I understand" responses — Feel-Felt-Found requires specifics
- Counter-positioning by attacking competitor — reframe the alternative, not the competitor
- Re-discovery on a clean not-interested — honor the no
- Multi-objection replies handled as one — match both, respond to more-removable first
- Skipping intel capture — competitor mentions are gold for competitive-intelligence

## Verification

1. Every objection has a library-match record OR new-pattern flag
2. Response variants reference only verified context (no invented quotes)
3. Cadence-state action propagated to person record
4. Intel routed to downstream skills (sample-check competitor / pricing mentions)
