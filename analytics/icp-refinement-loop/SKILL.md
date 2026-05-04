---
name: icp-refinement-loop
description: Refine the ICP scorecard from actual won/lost patterns after ≥30 closed deals — recompute tier cutoffs, re-tune dimension weights, surface segment shifts, propose ICP delta with evidence. Use when the user says "refine ICP", "recalibrate scorecard", "win rate doesn't match predictions", or "quarterly ICP audit."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Analytics, ICP-Refinement, Learning-Loop, Scorecard]
    related_skills: [icp-definition, lead-scoring, pipeline-stages, revenue-forecasting, competitive-intelligence, kpi-reporting]
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

# ICP Refinement Loop

Periodically refine the ICP scorecard using actual won/lost patterns from ≥30 closed deals. Recomputes tier cutoffs, re-tunes dimension weights, surfaces segment shifts. Hard rule: refusal to refine ICP with <30 closes — insufficient signal.

## When to Use

- Quarterly ICP refinement — ≥30 closed deals since last refresh
- Forecast accuracy shows systemic over/under-prediction by segment
- Win rate by tier doesn't match scorecard predictions
- Team expanded into new vertical — does ICP capture this
- User says "refine ICP" or "quarterly ICP audit"

## Quick Reference

| Concept | Value |
|---|---|
| Min-closes hard floor | 30 (won + lost combined); below = refusal |
| Refinement scope | Cutoff recalibration / weight re-tuning / segment shift / anti-ICP update / trigger refresh |
| Tier cutoff rule | >25% wins below T1-cutoff → cutoff too high; >25% losses at T1 → overconfident |
| Dimension re-tuning | Correlate each dimension score with closed_won outcome; adjust weights preserving total 100 |
| New segment requirement | ≥10 wins in segment not captured by original ICP |
| Confidence upgrade | Hypothesis → Medium (n≥30) / High (n≥100) |

## Procedure

1. **Validate inputs.** Pull closed deals; confirm n≥30. Below → refusal with explanation. See `${HERMES_SKILL_DIR}/references/thresholds.md`.
2. **Score won/lost deals against current rubric.** Apply original icp-definition rubric to each closed deal as it was at time of close. Compute distribution.
3. **Tier cutoff calibration.** Wins scoring <T1 → cutoff may be too high. Losses at T1 → cutoff may be too low. Surface recommendations if >25% misalignment. See `${HERMES_SKILL_DIR}/references/calibration-rules.md`.
4. **Dimension weight re-tuning.** Per dimension: compute correlation with closed_won. High correlation → increase weight. Near-zero → decrease. Preserve total 100. See `${HERMES_SKILL_DIR}/references/weight-tuning.md`.
5. **Segment shift detection.** Group wins by firmographic. If segment not in original ICP captures ≥10 wins → recommend new sub-segment.
6. **Lost-reason aggregation.** Aggregate lost reasons by tier + segment. lost-to-competitor → competitive-intelligence. no-budget by size → revenue-forecasting.
7. **Compose ICP delta recommendations.** Rank by impact. Each: evidence + proposed change + estimated impact. See `${HERMES_SKILL_DIR}/references/delta-template.md`.
8. **Retroactive rescoring proposal.** Compute: if new rubric applied to active pipeline, how do tiers shift? Surface counts. Don't auto-apply.
9. **Push + emit refinement record.** User authorizes which recommendations to apply. Route updates to icp-definition + lead-scoring. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Refining with <30 closes — insufficient signal; refusal is right
- Auto-applying ICP changes — always require user authorization
- Overfitting to recent wins — good rubric generalizes; don't optimize to last 30 deals at expense of generalizability
- Adding segments on n=2 — "we won two Healthcare deals" ≠ Healthcare ICP yet
- Ignoring lost-deal patterns — losses teach which to avoid
- Re-running too often — quarterly minimum; more frequent = noise + whiplash
- Not coordinating with positioning — ICP shifts imply positioning shifts

## Verification

1. Min-closes threshold honored
2. Per-deal scores reproducible from input + original rubric
3. Recommendations cite actual deal counts (sample-check 5)
4. Retroactive rescoring numbers add up to pipeline count
5. Lost-reason routing happened
6. User authorization queue surfaced before any rubric update
