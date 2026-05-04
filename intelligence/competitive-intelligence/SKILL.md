---
name: competitive-intelligence
description: Operationalize competitor monitoring with signal scoring (Strength × Decision-relevance), tiered watch-lists, alert routing, intel-to-action workflow, and battle-card refresh cycles. Produces a continuous monitoring system. Use when the user says "track our competitors going forward", "set up competitor alerts", or "how often should we update battle cards."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Intelligence, Competitive-Intelligence, Monitoring, Signals, Alerts]
    related_skills: [competitor-analysis, market-research, positioning-strategy, icp-definition]
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

# Competitive Intelligence

Stand up an ongoing competitive monitoring system: watch-list + signal taxonomy + alert cadence + intel-to-action workflow + battle-card refresh cycle. The output of `competitor-analysis` is a snapshot; this skill produces a system that prevents competitive moves from surprising the GTM team.

## When to Use

- User wants ongoing competitor tracking / monitoring setup
- Alert system design ("How should we be notified when X happens?")
- Signal interpretation ("Is this competitor move actually meaningful?")
- Battle-card refresh cadence decisions
- Win-rate diagnostic ("Are we losing more deals to X — what changed?")
- Quarterly competitive review prep

## Quick Reference

| Concept | Detail |
|---|---|
| Signal score | Strength (1–5) × Decision-relevance (1–5) = 1–25 |
| Action thresholds | ≤4 log only / 5–9 weekly digest / 10–15 24h alert / 16–20 leadership immediate / 21–25 strategic event |
| Watch-list ceiling | 8 competitors max; 4 is often the sweet spot |
| Signal categories | Product / Positioning / Pricing / Capital / Hiring / Customer / Channel-GTM / Content / Sentiment / Win-Loss |
| Battle-card refresh | Quarterly minimum; touch-up on score ≥10; full refresh on ≥16 |
| Ownership rule | One person owns the system or it dies |

## Procedure

1. **Confirm and tier the watch-list.** Pull from `competitor-analysis`. Top 3 Direct → heavy. Direct 4–6 → medium. Substitute → light. Cap at 8 actively monitored. See `${HERMES_SKILL_DIR}/references/watch-list-construction.md`.
2. **Select 4–6 categories per competitor.** Direct top-3: Product + Positioning + Pricing + Hiring + Sentiment + Win/Loss. Others: subset. See `${HERMES_SKILL_DIR}/references/signal-taxonomy.md`.
3. **Map detection methods.** Per (competitor × category): detection tool, URL/query, cadence, owner. This is the operating manual.
4. **Set up alerts and infrastructure.** Visualping on top-3 homepage/pricing/about. LinkedIn Sales Nav alerts. Crunchbase alerts. RSS for blogs/changelogs. Slack `#ci-alerts`. Signal log in Notion/Linear.
5. **Define alert routing rules.** Per signal type: recipient, channel, SLA. Override: score ≥16 → leadership immediately. See `${HERMES_SKILL_DIR}/references/alert-routing.md`.
6. **Define cadences.** Real-time / Daily (15 min) / Weekly (digest) / Bi-weekly (card touch-up if ≥10) / Monthly (synthesis) / Quarterly (re-tier + full refresh).
7. **Build intel-to-action workflow.** Detected → Scored → Logged → Routed → Triaged → Action (None / Card update / Positioning review / Product input / Strategic decision) → Tagged for quarterly. See `${HERMES_SKILL_DIR}/references/intel-workflow.md`.
8. **Set battle-card refresh cycle.** Quarterly calendar + score-driven + pattern-driven + new-Direct trigger. See `${HERMES_SKILL_DIR}/references/refresh-cycle.md`.
9. **Build the signal log.** Standard format. Pre-populate from `competitor-analysis`. See `${HERMES_SKILL_DIR}/references/signal-log-format.md`.
10. **Define quarterly review template.** Watch-list re-tier + top-5 signals + win/loss shifts + battle-card refreshes + strategic implications.

## Pitfalls

- Building a system the team won't use — over-engineering kills CI faster than under-engineering
- Watching too many competitors — 8 is ceiling; 4 is often the sweet spot
- Confusing volume with insight — 50 signals/week is not better than 10 if 40 score ≤4
- Skipping the log — patterns over time are the value; one-off alerts aren't
- Reacting to every signal — 70%+ should result in "no action — log only"
- Annual battle-card refresh — quarterly minimum; markets move faster
- Treating CI as marketing-only — it's GTM-wide: marketing, sales, product all consume it

## Verification

1. Watch-list tiered with monitoring intensity per tier
2. Every watched competitor has 4–6 named detection categories
3. Alert routing defines who-reads-what-when
4. Signal log has ≥5 historical entries
5. Battle-card refresh has trigger rules
6. One person owns the whole system
