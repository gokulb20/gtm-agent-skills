# Weight Tuning — ICP Refinement Loop

## Dimension Correlation Analysis

For each of the 6 ICP dimensions (Pain / Trigger / WTP / Reach / TTV / Strategic):

1. **Compute correlation** between each dimension's score and the `closed_won` outcome (binary: 1 for won, 0 for lost)
2. **Rank dimensions** by correlation strength
3. **Propose weight adjustments** preserving total = 100

## Example Re-tuning

| Dimension | Current weight | Correlation with closed_won | Proposed weight | Rationale |
|---|---|---|---|---|
| Pain | 25 | 0.62 | 25 | High correlation; maintain |
| Trigger | 20 | 0.68 | 30 | Highest correlation; increase |
| WTP | 20 | 0.45 | 20 | Moderate; maintain |
| Reach | 15 | 0.38 | 15 | Moderate; maintain |
| TTV | 10 | 0.41 | 10 | Moderate; maintain |
| Strategic | 10 | 0.12 | 5 | Near-zero; decrease |
| **Total** | **100** | — | **105→100** | Redistribute +5 |

## Overfitting Guard

- Don't optimize to perfectly predict the last 30 deals at the expense of generalizability
- A good rubric captures 70–80% of the signal; the residual is context-specific
- If proposed weight changes total >15 points shifted, surface as "significant change — validate on next quarter before full adoption"
