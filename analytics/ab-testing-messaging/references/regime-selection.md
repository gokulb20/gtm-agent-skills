# Regime Selection — A/B Testing

## Dual-Regime Block

| Regime | Trigger | Significance method | MIN_EFFECT_SIZE_PP | Sample guidance | What it produces |
|---|---|---|---|---|---|
| **Low-volume** | <1,000/arm/14d expected | Bayesian | 3.0 | n ≥ 50/arm; ~150 typical | Directional signal only |
| **High-volume** | ≥5,000/arm/14d expected | Frequentist two-proportion z-test | 1.0 | ~6,700/arm at 4% baseline + 1pp MDE | Shippable winner |

**Mid-zone (1,000–5,000/arm/14d):** Default to low-volume for safety. User can override.

## Internal-Inconsistency Rule

A test at <1,000/arm with MIN_EFFECT_SIZE_PP=1.0 will be perpetually inconclusive — the math doesn't support detecting 1pp lifts. The skill MUST surface this at design time and force a regime choice.

## Sample-Size Benchmarks (two-proportion z-test, 80% power, 5% alpha)

| Baseline | MDE | Required n/arm |
|---|---|---|
| 4% | 1.0pp | ~6,700 |
| 4% | 2.0pp | ~1,800 |
| 4% | 3.0pp | ~850 |
| 5% | 1.0pp | ~7,900 |
| 5% | 0.5pp | ~31,195 |

## Bayesian Threshold Note

- **0.95 is industry-canonical** (Optimizely default; Dynamic Yield)
- **0.85 is house default** — pragmatic floor for low-traffic B2B
- Skills MUST flag the canonical-vs-pragmatic gap when calling winners at 0.85 ≤ posterior < 0.95
