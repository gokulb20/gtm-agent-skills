---
name: icp-definition
description: Define a tiered Ideal Customer Profile using a 100-point weighted scorecard, Buyer/Champion/User/Blocker role mapping, Pain-Trigger-Outcome chains with workaround analysis, an anti-ICP boundary, and a trigger event library. Produces an ICP an SDR can apply in 2 minutes. Use when the user says "define our ICP", "who should we target", or "when should we disqualify."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Intelligence, ICP, Ideal-Customer-Profile, Segmentation, Qualification]
    related_skills: [market-research, competitor-analysis, positioning-strategy, channel-strategy, competitive-intelligence]
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

# ICP Definition

Produce a tiered, scored, evidence-backed Ideal Customer Profile that drives every downstream GTM decision — written tightly enough that a new SDR can apply it on day one without judgment calls.

## When to Use

- User asks to define or refine their ICP
- User wants qualification rules or sales-marketing alignment on target customer
- Pre-outbound grounding before lead sourcing
- Anti-ICP definition — "who should we say no to"
- Persona work — buyer + champion + user + blocker mapping
- User says "what makes a lead qualified" or "when should an SDR disqualify"

## Quick Reference

| Concept | Value |
|---|---|
| Scorecard weights | Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10 = 100 |
| Tier cutoffs | Tier 1 ≥75, Tier 2 55–74, Tier 3 40–54, Anti-ICP <40 |
| Roles required | Buyer (Economic) / Champion / User (End) / Blocker — fill all four |
| Pain-Trigger-Outcome | chronic problem → workaround + cost → acute event → measurable success state |
| Trigger types | `Type: need` (pain acute) vs `Type: buy` (budget/process opens). Both required. |
| Anti-ICP lenses | Firmographic / Pain / Buyer / Trigger |
| SDR qualify time | 2 minutes using handoff doc |

## Procedure

1. **Anchor in evidence.** Pull last 10–20 won deals. Capture company, size, role, pain, trigger, ACV. If 0 customers → mark "hypothesis-only", confidence cap Low.
2. **Define buyer firmographic.** Industry (specific), size range, stage, geography, tech-stack signals, operating model. Test: produces 500–5,000 candidate accounts.
3. **Fill four roles.** Buyer / Champion / User / Blocker — title patterns, what they care about, what kills the deal, where to find them. See `${HERMES_SKILL_DIR}/references/role-map.md`.
4. **Build Pain-Trigger-Outcome chain.** In buyer language. Include Workaround Analysis: what they do today, cost (time/money/risk/accuracy/reputation), 90-day dream state. See `${HERMES_SKILL_DIR}/references/pain-trigger-outcome.md`.
5. **Build trigger library.** 5–10 specific triggers, each tagged Strength + `Type: need` or `buy` + named detection source. At least one buy-trigger required.
6. **Run 100-point scorecard.** Apply to ≥9 accounts (3 best-fit, 3 mid, 3 anti-ICP). If scores cluster, re-tune weights. See `${HERMES_SKILL_DIR}/references/scorecard-rubric.md`.
7. **Define Anti-ICP.** 4 boundaries (firmographic / pain / buyer / trigger), each with rule + rationale.
8. **Generate Tier 1/2/3 examples.** 3 named accounts per tier with score breakdown.
9. **Produce ICP one-pager + SDR handoff.** Single document, 2-minute usable. See `${HERMES_SKILL_DIR}/references/sdr-handoff-template.md`.

## Pitfalls

- Aspirational ICP — describing the customer you wish you had vs. the one you actually win
- One-role ICP — missing champion or blocker causes stalled deals
- Pain without trigger — buyer hurts but isn't acting; pain alone doesn't fund a deal
- Skipping Anti-ICP — sales wastes capacity chasing fit-but-misqualified accounts
- Generic firmographic — "B2B SaaS" is not a firmographic; be specific
- Static ICP — re-run every 6 months minimum, faster if motion changes
- Logo lust — "we want BigCo" is wishful thinking, not ICP work

## Verification

1. SDR can qualify a lead in 2 minutes using the handoff doc
2. Marketing can write outbound sequences using Pain-Trigger-Outcome directly
3. Anti-ICP is specific enough that 3 disqualifiers can be stated without thinking
4. 100-pt scorecard differentiates won from lost deals when applied retroactively
