# ICP Delta Template — ICP Refinement Loop

## Delta Recommendation Format

| # | Type | Current state | Proposed change | Evidence | Estimated impact |
|---|---|---|---|---|---|
| 1 | Cutoff recalibration | T1 cutoff: 75 | T1 cutoff: 72 | 8/30 wins (27%) scored <75 | 4 deals Tier-2→Tier-1; 2 deals Tier-1→Tier-2 |
| 2 | Weight re-tuning | Trigger: 20 | Trigger: 30 | Correlation 0.68 with closed_won | Higher-scoring trigger-rich deals get more weight |
| 3 | Segment addition | SaaS-only ICP | Healthcare sub-segment | 8 wins (17%) in Healthcare | New variant scorecard for Healthcare |
| 4 | Anti-ICP boundary | None for Guru users | "Guru installed at Series B" | 7 lost-to-Guru (15% of losses) | Disqualify these earlier; save rep capacity |
| 5 | Trigger library refresh | 5 triggers | Add 2 new triggers from won-deal patterns | 6/8 won deals cited "new VP CX hire within 60d" | Stronger trigger signal for Tier-1 qualification |

## Prioritization

Rank by impact (most deals affected first):
1. Cutoff recalibrations (affects all active pipeline)
2. Weight re-tunings (affects all future scoring)
3. Segment additions (affects new pipeline segment)
4. Anti-ICP boundaries (affects disqualification logic)
5. Trigger library refresh (affects sourcing quality)

## User Authorization

Each recommendation requires explicit user approval before:
- Updating the icp-definition rubric file
- Re-running lead-scoring on the active pipeline
- Changing any downstream configuration

Proposals without user authorization stay as `interaction:research` with `#manual-review #icp-refinement-auth` tags.
