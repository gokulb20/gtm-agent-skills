# Thresholds — ICP Refinement Loop

## Minimum Closed Deals

| Closes (won + lost) | Action |
|---|---|
| ≥30 | Proceed with refinement |
| 10–29 | Refusal for full refinement; offer directional spot-check via lead-scoring |
| <10 | Refusal; recommend collecting more closes before any ICP changes |

## Tier Cutoff Calibration Thresholds

| Condition | Signal | Recommendation |
|---|---|---|
| >25% of wins score < T1-cutoff (75) | Cutoff too high | Lower T1 cutoff (e.g., 75→72) |
| >25% of losses score ≥ T1-cutoff | Cutoff too low (overconfident) | Raise T1 cutoff or tighten dimension floors |
| Any wins score < Anti-ICP threshold (<40) | Rubric missing something | Deep-dive these wins; may need new dimension or trigger |
| >25% of T3 deals winning at T3 rate | T3 may be too restrictive | Consider expanding T3 criteria |

## New Segment Requirements

| Wins in uncaptured segment | Action |
|---|---|
| ≥10 | Recommend new sub-segment with own variant scorecard |
| 5–9 | Surface as emerging pattern; monitor next quarter |
| <5 | Insufficient; individual deals, not ICP signal |

## Confidence Rubric Upgrade

| Historical closes | Confidence tier |
|---|---|
| 0 | Hypothesis |
| 1–9 | Low |
| 10–29 | Medium |
| ≥30 | High |
| ≥100 | High (robust) |

## Audit Cadence

- Quarterly default (`ICP_REFINEMENT_AUDIT_QUARTERLY=true`)
- On-demand when forecast accuracy audit shows systemic miscalibration
- Minimum interval: quarterly; more frequent = noise
