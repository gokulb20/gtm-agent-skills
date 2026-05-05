# A/B Testing Methods

## Bayesian (Default for n<200 per arm)

Used when sample sizes are small — avoids "wait for 99% confidence and ship nothing" problem.

### Method

- Bernoulli model on reply rates
- Compute posterior distribution for each variant
- Recommend winner when: `P(variant_b > variant_a) > 0.85` AND effect size ≥1pp

### When to Call

- After D+10 of cadence (earliest meaningful data)
- Re-check every monitoring cycle until winner or D+14

### Inconclusive by D+14

- Stop the test
- Ship the higher-volume variant by default
- Log as "inconclusive — no winner declared"

## Frequentist z-test (n≥200 per arm)

Standard two-proportion z-test for larger samples.

### Method

- Null hypothesis: variant rates are equal
- Test at p<0.05 (two-tailed)
- Require effect size ≥1pp (absolute percentage points)
- Report: p-value, effect size, 95% confidence interval

### When to Call

- After D+10 of cadence
- Only when both arms have n≥200

## Common Pitfalls

1. **n<50 per arm** — statistically meaningless; do NOT ship a "winner"
2. **Multiple arms** — two variants is the sweet spot; three+ explodes data requirements
3. **Testing on open rate** — Apple MPP makes this noise; test on reply rate only
4. **Best time to send experiments** — noisy due to MPP; only meaningful on reply rate
5. **Peeking** — checking significance repeatedly inflates false-positive rate; Bayesian is more robust to this

## Effect Size Requirements

- Minimum: ≥1 percentage point (absolute)
- Rationale: smaller effects are not worth the operational cost of a variant swap
- Report effect size alongside significance — "significant but tiny" is not actionable

## Example Decision

```
Variant A (CCQ + Pain): 4.1% reply rate (n=180, 7 replies)
Variant B (CCQ + Vision): 6.2% reply rate (n=180, 11 replies)
Method: Bayesian
Posterior P(B > A) = 0.96
Effect size: 2.1pp
Recommendation: ship variant B for remaining cadence
```
