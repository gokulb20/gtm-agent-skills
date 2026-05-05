---
name: channel-strategy
description: Identify and prioritize go-to-market channels using Weinberg's Bullseye Framework, CAC/LTV-per-channel math, channel-fit-by-ICP scoring, and stage-appropriate selection. Produces a focused 1–3 channel bet with experiment design and kill criteria. Use when the user says "which channels should we use", "we're doing too many channels", or "should we try TikTok for B2B."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Intelligence, Channel-Strategy, Bullseye, Channel-Mix, Traction]
    related_skills: [icp-definition, positioning-strategy, market-research, competitor-analysis, competitive-intelligence]
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

# Channel Strategy

Decide where to spend GTM time, energy, and budget. Replace channel-by-familiarity with structured analysis: 19 channels evaluated, ICP-fit scored, CAC/LTV checked, Bullseye plan delivered with experiment design and kill criteria.

## When to Use

- User asks "Which channels should we use?" or "We're doing too many — what to cut?"
- Budget allocation across channels or new-channel evaluation
- Stage transition ("We're at $1M ARR — should we add channels?")
- Underperformance diagnosis ("Channel X isn't working — should we kill it?")
- Pre-fundraise channel narrative

## Quick Reference

| Concept | Detail |
|---|---|
| 19 Bullseye channels | Targeting blogs · Publicity · Unconventional PR · SEM · Social ads · Offline ads · SEO · Content · Email · Eng-as-marketing · Viral · BD · Sales (outbound) · Affiliate · Existing platforms · Trade shows · Offline events · Speaking · Community |
| Bullseye rings | Outer (19 considered) → Middle (3 tested, ≤$1k each) → Inner (1 doubled-down) |
| CAC viability | Payback <12 months; LTV/CAC >3 (David Skok) |
| Channel-fit-by-ICP | Buyer presence / Buyer attention / Decision context, 1–5 each; sum ≥8 to qualify |
| Compounding vs. linear | Compounding: SEO, content, community. Linear: outbound, paid. Run 1 of each at every stage |
| Stage rule | 1–3 channels drive 80% of acquisition at any stage |

## Procedure

1. **Brainstorm outer ring (all 19).** Force consideration of every channel. 1-line annotation each. See `${HERMES_SKILL_DIR}/references/19-channels.md`.
2. **Apply hard filters.** Cut on CAC math / motion fit / stage fit / capital / time constraint. Survivors: 6–10.
3. **Score channel-fit-by-ICP.** 1–5 on buyer presence, attention, decision context. Cut anything <8. Survivors: 4–7. See `${HERMES_SKILL_DIR}/references/channel-fit-matrix.md`.
4. **Pick middle ring (3 channels).** Likely-best + alternative + wildcard. Force ≥1 compounding + ≥1 linear.
5. **Design experiments per channel.** Hypothesis / budget / duration / success / kill / owner / tools. See `${HERMES_SKILL_DIR}/references/experiment-template.md`.
6. **CAC/LTV viability per channel.** Cost per lead × lead-to-close → CAC. Payback = CAC / monthly ACV. Kill channels failing math.
7. **Allocate founder time + budget.** Time as resource. Budget reserves 20–30% for tests.
8. **Build Bullseye plan.** Outer / middle / inner (TBD post-results).
9. **Stage graduation plan.** At next ARR milestone, which channels get added/swapped?
10. **Kill / scale / iterate criteria.** Specific, measurable, time-bound per channel.

## Pitfalls

- Channel-of-the-month — chasing hype without ICP-fit math
- "Channel that worked at last company" is hypothesis, not answer
- Over-investing in compounding pre-PMF — SEO at 0 customers wastes capital
- Cutting compounding too early — SEO/content take 6–12 months; killing at week 8 is the most common mistake
- No kill criteria — channels quietly underperform for 6+ months and drain budget
- Spreading thin — 5 mediocre channels < 2 great ones
- All-linear mix — outbound + paid + ads = no compounding base

## Verification

1. All 19 channels considered and 1-line annotated
2. 3 channels in middle ring with explicit experiment design
3. CAC/LTV checked per top-3 channel
4. Kill/scale/iterate criteria per channel
5. ≥1 compounding + ≥1 linear in the mix
6. Stage-graduation plan covers next 2 stages
