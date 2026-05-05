# Scenario Math — Revenue Forecasting

## Weighted Pipeline (Base Scenario)

For each in-horizon deal:
```
contribution = deal_value × stage_probability
```

Sum all contributions = base forecast.

## Conservative Scenario

Filter to:
- Proposal-stage deals at historical close rate
- Explicit user-committed deals at 90% (acknowledging late surprises)

```
conservative = Σ(proposal_deals × historical_proposal_close_rate) + Σ(commits × 0.90)
```

## Aggressive Scenario

```
aggressive = conservative + Σ(≥Discovery_deals × min(base_prob + 0.15, 1.0)) - Σ(≥Discovery_deals × base_prob)
```

Cap: each deal's probability capped at base+15pp to limit upside inflation.

## Cycle-Time Gating

Exclude deals from in-horizon calculation when:
- New stage + closing in <14d
- Contacted + closing in <7d
- Engaged + closing in <3d

These deals are mathematically in the horizon but operationally implausible.

## Default Stage Probabilities

When no historical data exists:

| Stage | Default probability |
|---|---|
| New | 2% |
| Contacted | 5% |
| Engaged | 10% |
| Meeting | 20% |
| Discovery | 35% |
| Proposal | 60% |

These are **guesses**. Flag as `[unverified — needs check]`. Calibrate from history ASAP.

## MAPE Calculation

For forecast-accuracy audit:
```
MAPE = (1/n) × Σ(|actual - forecast| / |actual|) × 100
```

For early-stage with thin history (n<10), supplement with WMAPE (volume-weighted) to avoid division-by-zero issues.
