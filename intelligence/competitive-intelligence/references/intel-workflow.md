# Intel-to-Action Workflow

## Flow

```
SIGNAL DETECTED
    ↓
SCORE (Strength × Decision-relevance)
    ↓
ROUTE (per Alert Routing Rules)
    ↓
TRIAGE (within cadence window)
    ↓
ACTION:
  ├── Battle-card update (if affects sales messaging)
  ├── Positioning revisit (if affects category framing)
  ├── Product roadmap input (if affects competitive feature gaps)
  ├── No action — log only (most common, ~70% of signals)
  └── Strategic review (rare, score ≥21)
    ↓
LOG (in signal log; tagged for quarterly review)
```

## Critical Rule

Every signal must end up in the log, even "no action" ones. The pattern over time is more valuable than any individual signal.
