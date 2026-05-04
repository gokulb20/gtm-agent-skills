---
name: positioning-strategy
description: Define product positioning using Dunford's 5-component framework, JTBD-based wedge construction, message house architecture, value-by-role variations, and for-and-against wedges against named competitors. Use when the user says "help me position", "our positioning isn't working", or "how do we position against X."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Intelligence, Positioning, Messaging, Value-Proposition, Dunford]
    related_skills: [market-research, competitor-analysis, icp-definition, channel-strategy, competitive-intelligence]
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

# Positioning Strategy

Define what your product is, who it's for, what it's better at, and against what alternatives — evidence-backed and clear enough that a buyer understands the wedge in 10 seconds.

## When to Use

- Positioning definition for a new product or new launch
- Repositioning ("Our positioning isn't working — fix it")
- Message hierarchy or value-prop articulation
- Competitive wedge sharpening ("How do we position against [competitor]?")
- Sales messaging audit / consolidation
- Pre-launch positioning grounding after market-research + competitor-analysis + ICP

## Quick Reference

| Concept | Detail |
|---|---|
| Dunford 5 components | Alternatives / Unique attributes / Value + proof / Best-fit ICP / Market category |
| Category frame types | Existing / Subcategory (default) / New (high-risk) / Cross-category (avoid) |
| Wedge format | "For [ICP] who are doing [JTBD], [product] is [category] that [unique value], unlike [alternative] which [trade-off]" |
| Wedge diagnostic | Specific / Defensible / Sharp — all three must pass |
| Alternatives floor | ≥4 entries including status quo / DIY |
| Message house | 1 primary + 3 pillars + ≥2 proofs/pillar |
| Roles for value variation | Buyer / Champion / User (Blocker gets info, not positioning) |

## Procedure

1. **Identify alternatives (Dunford component 1).** Direct + indirect + DIY/status quo. ≥4 entries. If `icp-definition` produced a Workaround Analysis, use it directly — each workaround becomes an alternative. See `${HERMES_SKILL_DIR}/references/alternatives-analysis.md`.
2. **List unique attributes (Dunford component 2).** Features only you have, or meaningfully more of. Each: specific / verifiable / differentiating.
3. **Map attributes to value (Dunford component 3).** Drill: feature → benefit → outcome → proof. If "why buyer cares" still sounds like a feature, drill again.
4. **Choose best-fit ICP (Dunford component 4).** Often narrower than operational ICP. The segment that values unique attributes most.
5. **Choose market category (Dunford component 5).** Default to subcategory. Test: 5-second test, search test, G2/analyst recognition. See `${HERMES_SKILL_DIR}/references/category-frames.md`.
6. **Construct the wedge.** Use JTBD wedge format. Apply 3 diagnostic tests (specific / defensible / sharp). Iterate until all pass. See `${HERMES_SKILL_DIR}/references/wedge-construction.md`.
7. **Build message house.** Primary (1 sentence) + 3 pillars + ≥2 proofs each. See `${HERMES_SKILL_DIR}/references/message-house.md`.
8. **Generate value-by-role variations.** Buyer / Champion / User — distinct framing, not minor word swaps.
9. **For-and-against wedges (top 3 competitors).** Per competitor: WHEN / WE WIN / THEY ATTACK / WE COUNTER / FLIP QUESTION. See `${HERMES_SKILL_DIR}/references/for-and-against.md`.
10. **Buyer-language audit.** Every load-bearing word verified in ≥3 buyer-source quotes, or flagged for testing.

## Pitfalls

- Skipping alternatives analysis — most common failure mode; without alternatives, positioning floats
- Tagline ≠ positioning — tagline is derivative; positioning is the underlying logic
- Positioning by committee — 6 editors = mush; single owner
- Listing features as value — drill: "and so what?" twice
- Same headline for buyer + user + champion — wrong for at least 2 of them
- "For everyone" positioning — = for no one; force trade-offs
- Over-claiming category creation — needs 10–18 months + budget; default to subcategory

## Verification

1. Wedge passes all 3 diagnostic tests (specific / defensible / sharp)
2. Every load-bearing word verified in buyer-source quote or flagged
3. Alternatives include status quo / DIY
4. Message house: 1 primary + 3 pillars + ≥2 proofs/pillar
5. A new SDR could write outbound copy using only this document
