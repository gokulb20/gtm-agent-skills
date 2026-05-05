# Threshold Defaults — Conversation Intelligence

## Frequency Thresholds (per pattern class)

| Pattern class | Default threshold | Window | Env var override |
|---|---|---|---|
| Competitor mention | 3 per entity / 30d | Rolling 30d | CONV_INTEL_COMPETITOR_THRESHOLD |
| Pricing pushback | 4 / 30d | Rolling 30d | CONV_INTEL_PRICING_THRESHOLD |
| Feature request | 5 / 30d | Rolling 30d | CONV_INTEL_FEATURE_THRESHOLD |
| Champion language | 2 per deal | Per-deal | — |
| Blocker signal | 1 per deal | Per-deal | — |

## Confidence Floor

- **0.7** — extractions below this confidence flagged for manual review
- No auto-routing or downstream dispatch for confidence <0.7

## Aggregation Window

- Default: 30d rolling
- User-overridable via `CONV_INTEL_AGGREGATION_WINDOW_DAYS`
- 7d too narrow (misses trends); 90d too wide (includes stale signal)

## Dedup Rules

- Same conversation: dedup by transcript_id + pattern class + timestamp
- Same quote appearing in multiple runs: keep earliest extraction
- Already extracted within last 7d: push dedup notice only
