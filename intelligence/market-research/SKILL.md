---
name: market-research
description: Research and size a target market by classifying market type, framing the category via JTBD, building a triangulated TAM/SAM/SOM with explicit confidence labels, scoring segments via a bowling-pin rubric, and identifying whitespace. Use when the user says "how big is this market", "help me size this", or "what category should we claim."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Intelligence, Market-Research, Market-Sizing, Segmentation, Whitespace]
    related_skills: [icp-definition, competitor-analysis, positioning-strategy, channel-strategy, competitive-intelligence]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter to use (agentic-app | csv | none)"
        default: "agentic-app"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Market Research

Produce a directional but defensible market view for GTM planning — category, sizing, segments, demand, whitespace — anchored in evidence with confidence labels.

## When to Use

- User asks "How big is this market?" or "Help me size this"
- User needs category framing or segment analysis
- User wants demand validation or whitespace mapping
- Pre-GTM grounding before competitor-analysis, icp-definition, or positioning-strategy
- Investor or board-prep market overviews
- Geographic expansion analysis

## Quick Reference

| Concept | Definition |
|---|---|
| Market type (Steve Blank) | existing / resegmented / new / clone — picks sizing approach |
| TAM / SAM / SOM | Total → reachable → realistic 3yr capture; ≥2 methods, reconcile if >2x gap |
| Confidence labels | `[H]` / `[M]` / `[L]` on every number — required |
| JTBD format | "When [situation], buyer wants to [motivation], so they can [outcome]" |
| Bowling-pin score | Pain + Urgency + Reach + Reference + Capacity, 1–5 each = /25 |
| Whitespace lenses | Segment / use-case / pricing / experience |

## Procedure

1. **Diagnose market type.** Apply Steve Blank's framework: existing / resegmented / new / clone. Output with rationale; determines valid sizing methods.
2. **Frame the category.** Produce (a) buyer-recognizable category label verified against G2/Capterra, (b) 2–4 adjacent categories, (c) JTBD statement. If buyers can't recognize in 5 seconds, prefer JTBD framing.
3. **Set boundaries.** Geography (named, not "global"), customer type (firmographic), use cases (included + excluded), time horizon, buyer persona scope. If undefined, return to intake.
4. **Build directional sizing.** Use ≥2 methods from {bottom-up, top-down, value-theory, analogous}. Show math. Tag every assumption with source + confidence. Reconcile if methods disagree by >2x. See `${HERMES_SKILL_DIR}/references/sizing-frameworks.md`.
5. **Segment with bowling-pin scoring.** Produce 3–7 segments. Score each 1–5 on pain/urgency/reach/reference/capacity. Highest = beachhead. See `${HERMES_SKILL_DIR}/references/segmentation-rubric.md`.
6. **Gather demand signals.** Sweep search, community, hiring, capital, review-site, and internal signals. Synthesize 5–10 tagged `[H/M/L]`.
7. **Identify whitespace.** Apply 4-lens diagnostic (segment/use-case/pricing/experience). 3–5 hypotheses with validation cards. See `${HERMES_SKILL_DIR}/references/whitespace-examples.md`.
8. **Synthesize + risks register.** Every load-bearing claim → assumption flag. ≥3 ways the market view could be wrong.
9. **Route downstream.** Recommend next skill with carry-forward inputs.

## Pitfalls

- Treating TAM as a GTM plan — SAM and SOM drive decisions
- Single-source sizing — caps at Medium confidence; always triangulate
- Confusing Reddit upvotes with purchasing intent
- Over-relying on analyst reports for emerging categories — Gartner/Forrester lag
- False precision — 3 decimal places on 50%-uncertain numbers is malpractice
- Skipping the assumptions register — hidden assumptions silently break later

## Verification

1. User can defend TAM/SAM/SOM to a skeptical investor without rebuilding the math
2. Beachhead segment named with rationale
3. User knows which assumption, if invalidated, would change the strategy
4. Downstream skills can use output without re-research
