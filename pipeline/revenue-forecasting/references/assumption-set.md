# Assumption Set Template — Revenue Forecasting

## Required Fields

Every forecast MUST carry these assumptions explicitly:

| Field | Description | Source |
|---|---|---|
| Stage probabilities | Per-stage close rate used | Historical closes or defaults |
| Probability source | "calibrated from N closes" or "default — unverified" | CRM data or hardcoded |
| Average cycle time per stage | Days per stage transition | Historical data |
| Deal-value distribution | Median, mean, top-decile | Active pipeline |
| Confidence tier | High / Medium / Low / Hypothesis-only | Based on n historical closes |
| Horizon | 30 / 60 / 90 days | User-configured |
| Cycle-time exclusions | Which deals excluded as implausible | Rule-based |
| Top-10 concentration | % of forecast from top 10 deals | Computed |

## Confidence Rubric

| Tier | Historical closes (won + lost) | Implication |
|---|---|---|
| High | ≥30 | Rates are calibrated; forecast is defensible |
| Medium | 10–29 | Directional; rates may have sampling error |
| Low | 1–9 | Rates are mostly defaults; flag loudly |
| Hypothesis-only | 0 | No basis; treat as scenario exercise |

## Default Probability Flag

When using default probabilities (not calibrated), the forecast record MUST include:
- `confidence: low`
- `using_default_probabilities: true`
- Tags: `#unverified #review-required #default-rates`
