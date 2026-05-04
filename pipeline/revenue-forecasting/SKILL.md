---
name: revenue-forecasting
description: Forecast 30/60/90-day revenue using weighted-pipeline math, historical stage-conversion rates, and conservative/base/aggressive scenarios with explicit assumption sets. Use when the user says "forecast revenue", "board update numbers", "commit number", or "recalibrate conversion rates."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Pipeline, Forecasting, Revenue, Scenarios]
    related_skills: [pipeline-stages, lead-scoring, crm-hygiene, kpi-reporting, channel-performance]
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

# Revenue Forecasting

Produce 30/60/90-day revenue forecasts using weighted-pipeline math + historical stage-conversion rates + 3 scenarios. Each forecast carries an explicit assumption set so the user can challenge inputs, not just outputs. Hard rule: forecasts without ≥30 historical closes carry a `confidence: low` flag.

## When to Use

- Board update — produce 30/60/90 forecast with scenarios
- Quarter-end commit number
- Stage-conversion rates need recalibrating
- Forecast accuracy audit vs actuals
- User says "forecast revenue" or "what's our commit number"

## Quick Reference

| Concept | Value |
|---|---|
| Base scenario | Σ(deal_value × stage_probability) for in-horizon deals |
| Conservative | Proposal-stage + explicit commits only |
| Aggressive | Conservative + best-case ≥Discovery (cap +15pp) |
| Default stage probabilities | New 2% / Contacted 5% / Engaged 10% / Meeting 20% / Discovery 35% / Proposal 60% |
| Confidence rubric | High: ≥30 closes / Medium: 10–29 / Low: 1–9 / Hypothesis-only: 0 |
| Cycle-time gating | Don't include deals that can't realistically close in horizon |

## Procedure

1. **Validate inputs.** Pull active pipeline; load historical conversion rates (or flag use-of-defaults); confirm horizon.
2. **Filter to in-horizon deals.** Deals with expected_close_date within horizon. Exclude implausible stage-close combos. See `${HERMES_SKILL_DIR}/references/scenario-math.md`.
3. **Compute base scenario.** For each in-horizon deal: contribution = deal_value × stage_probability. Sum.
4. **Compute conservative.** Proposal-stage deals at historical rate + explicit commits at 90%.
5. **Compute aggressive.** Conservative + best-case ≥Discovery. Cap each deal's added probability at base+15pp.
6. **Per-deal contribution + top-10.** List top-10 deals by weighted contribution. Surface concentration risk if >70%.
7. **Output assumption set.** Stage probabilities used, cycle-time averages, confidence tier, source of rates. See `${HERMES_SKILL_DIR}/references/assumption-set.md`.
8. **Forecast-accuracy audit (when applicable).** Compare prior forecasts to actuals. Compute MAPE per scenario. Flag systemic over/under-forecasting.
9. **Push to CRM.** Forecast as `interaction:research` with full assumption set + per-scenario numbers. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Treating base as THE forecast — it's the middle of three; commit at conservative
- Using defaults when history exists — always calibrate from actuals
- Cycle-time blind spots — New-stage deal closing in 7d is implausible
- Top-10 dependency hidden — surface concentration risk
- Open rate in forecast — Apple MPP made it noise; stage-based math only
- Aggressive with no cap — limit upside inflation at +15pp per deal

## Verification

1. Per-scenario math reproducible from assumption set
2. Top-10 contribution sums plausibly to scenario totals
3. Confidence tier matches historical-close evidence
4. Cycle-time exclusions documented
5. Assumption set explicit (no hidden defaults)
