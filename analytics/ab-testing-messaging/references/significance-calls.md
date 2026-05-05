# Significance Call Rules — A/B Testing

## Decision Matrix

| Condition | Call | Action |
|---|---|---|
| Significance ✓ + effect ≥ MES ✓ + min-n ✓ | WINNER | Ship 100% remaining to winner via channel skill |
| Max duration reached, no significance | INCONCLUSIVE | Ship control (variant A) by default; document underpowered |
| Min-n not yet reached | CONTINUE | Keep test running |
| n < 50/arm at max duration | INCONCLUSIVE (forced) | Cannot call regardless of apparent significance; noise |

## Winner Call Requirements

Must include ALL of:
- Method used (Bayesian or frequentist)
- Cumulative n per arm
- Per-arm conversions and rate
- Posterior probability (Bayesian) or p-value (frequentist)
- Effect size in pp
- Regime (low-volume or high-volume)
- Whether threshold is house-default or industry-canonical

## Inconclusive Policy

After max duration with no winner:
- Ship the higher-volume variant (usually control) by default
- Document WHY inconclusive (underpowered, no effect, early peek)
- Surface estimated n needed to resolve
- Recommend next action (extend, pool campaigns, or accept no-difference)

## Apple MPP Exclusion

Open rate is NOT a valid metric for A/B test significance. Only reply rate, meeting rate, or positive-reply rate.
