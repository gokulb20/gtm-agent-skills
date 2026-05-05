# Calibration Rules — ICP Refinement Loop

## Tier Cutoff Calibration Process

### Step 1: Score every closed deal
Apply the original icp-definition rubric (6 dimensions, 100-point scale) to each closed deal as it was at the time of close.

### Step 2: Compute distributions
- Win score distribution: mean, median, min, max
- Loss score distribution: mean, median, min, max
- Overlap zone: where wins and losses score similarly

### Step 3: Check calibration signals

| Signal | Test | Action |
|---|---|---|
| Wins clustering below T1 | >25% of wins < 75 | Lower T1 cutoff to improve capture |
| Losses clustering at T1 | >25% of losses ≥ 75 | Raise T1 cutoff; rubric overconfident |
| Wins in Anti-ICP zone | Any wins < 40 | Deep-dive: what did rubric miss? |
| T2 wins at T1 rate | T2 win-rate ≈ T1 | T2 cutoff may be too restrictive |

### Step 4: Propose specific cutoff changes
- Each proposal: current cutoff → proposed cutoff
- Evidence: N wins/losses affected + their score distribution
- Estimated impact: how many active deals would shift tiers

## Anti-ICP Boundary Check

When lost-to-competitor rate spikes in a specific segment:
- Check if segment should be added to Anti-ICP
- Example: lost-to-Guru at 40% in Series B → add "Series B with Guru installed" as Anti-ICP condition
