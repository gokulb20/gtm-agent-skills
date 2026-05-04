---
name: competitor-analysis
description: Map a competitive landscape by tiering competitors into Direct/Indirect/Substitute/Aspirational, profiling positioning/pricing/strengths/weaknesses, applying Helmer's 7 Powers and segment ownership, and producing 1-page battle cards. Use when the user says "who are our competitors", "build a battle card", or "what's our moat."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Intelligence, Competitor-Analysis, Battle-Cards, Moats, Positioning]
    related_skills: [market-research, icp-definition, positioning-strategy, competitive-intelligence]
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

# Competitor Analysis

Turn a list of names into a structured competitive view that GTM, product, and sales can act on. Tiered profiles, head-to-head differentiation, structural moat assessment, and battle cards that survive real sales conversations.

## When to Use

- User asks "Who are our competitors?" or "Map the landscape"
- User wants head-to-head comparison or battle cards
- User asks about defensibility / moat analysis
- Pre-launch competitive grounding or loss-reason investigation
- Pricing benchmark or "alternative-to" positioning research
- User claims "we have no competitors" — force substitute analysis

## Quick Reference

| Concept | Detail |
|---|---|
| Tiers | Direct (same product/buyer/job) / Indirect (different product, same job) / Substitute (Dunford-style alternatives: DIY, hire, do-nothing, shift budget) / Aspirational |
| Substitute categories (≥1 each) | DIY/manual · Hire a person · Do nothing · Shift budget elsewhere |
| Helmer's 7 Powers | Scale Economies / Network Economies / Counter-Positioning / Switching Costs / Branding / Cornered Resource / Process Power — each needs benefit AND barrier |
| Tier targets | 3–6 Direct, 2–4 Indirect, 2–4 Substitute, 1–2 Aspirational |
| Battle card | 1 page; 1 wedge; 1 flip-question; 1 proof |
| No-FUD rule | Every weakness needs a citation |

## Procedure

1. **Build candidate list.** Pull buyer-validated alternatives first (lost deals, won deals). Then desk research (G2, Reddit, Crunchbase). Force ≥1 entry from each of 4 Substitute categories. Goal: 15–25 raw candidates.
2. **Tier into 4 categories.** Direct 3–6 / Indirect 2–4 / Substitute 2–4 / Aspirational 1–2. If Direct <3 → research more.
3. **Profile Direct + Substitute.** Each gets: positioning, best-fit customer, 3 strengths, 3 weaknesses, pricing, 1 recent move. No fabrication — write "Insufficient data" if absent. See `${HERMES_SKILL_DIR}/references/competitor-profiling.md`.
4. **Head-to-head matrix.** Top 5 + user across positioning / ICP / pricing / motion / 3–5 capabilities.
5. **Apply Helmer's 7 Powers.** Top 3 + user. Each Power needs benefit AND barrier evidence. Be honest — most early-stage products have 0–1. See `${HERMES_SKILL_DIR}/references/helmer-7-powers.md`.
6. **Map segment ownership.** Per segment: owner / runner-up / user position / rationale. Surface whitespace.
7. **Porter's 5 Forces.** 1-paragraph sanity-check on structural attractiveness.
8. **Win/loss patterns.** 3–5 each + 1+ disqualifier. If no data, replace with hypothesis section.
9. **Battle cards (top 3 Direct).** 1 page each: 1 wedge, 1 flip-question, 1 proof. See `${HERMES_SKILL_DIR}/references/battle-card-template.md`.
10. **Strategic implications + route downstream.** 3–5 implications (observation → so what → action). Recommend next skill.

## Pitfalls

- FUD in battle cards — every weakness must cite a source
- Manufactured moats — most early-stage products have 0 Powers; say so
- Skipping substitutes — "spreadsheets + status quo" wins more deals than named competitors
- Feature comparison theater — long checkboxes lose to "what job does the buyer hire each tool for"
- Pricing pages believed — real ACVs come from Vendr/Reddit/internal sales, not published lists
- Battle cards reps won't use — 1 wedge + 1 question + 1 proof beats 5 pages of feature trivia

## Verification

1. User can name top 3 Direct competitors and the wedge against each
2. Every weakness has a source citation
3. Battle cards fit on 1 page with 1 wedge + 1 flip-question + 1 proof
4. Helmer analysis is honest — no fake moats
5. Segment ownership map identifies ≥1 whitespace
6. Strategic implications drive ≥3 actions, not just observations
