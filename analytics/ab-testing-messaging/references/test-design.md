# Test Design Template — A/B Testing

## Test Contract Fields

| Field | Description |
|---|---|
| Test ID | Unique identifier (e.g., ab_t1_opener_2026-05-22) |
| Hypothesis | One sentence (e.g., "Vision opener converts ≥3pp higher than Pain") |
| Variable | What changes between variants (ONE only) |
| Variant A (control) | Copy/config for control arm |
| Variant B (treatment) | Copy/config for treatment arm |
| Traffic split | Default 50/50; hash-based allocation |
| Primary metric | Reply rate (never open rate) |
| Secondary metrics | Meeting rate, positive-reply rate |
| Regime | Low-volume or high-volume (with justification) |
| Significance method | Bayesian or frequentist |
| Thresholds | Bayesian: P(B>A)>X; Frequentist: p<Y AND effect≥Z |
| Min n/arm | 50 |
| Max duration | 14 days |
| Analysis plan | When + how significance will be checked |

## Allocation Method

Hash-based per recipient: `variant = hash(recipient_id + test_id) % 100 < split_pct ? A : B`

Same recipient always gets same variant if test re-runs. If allocation changed mid-test, data is contaminated.
