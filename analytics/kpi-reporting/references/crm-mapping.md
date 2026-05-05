# Push-to-CRM Mapping — KPI Reporting

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Weekly KPI report | `interaction` (type: research) | `relevance` = full one-screen report + linked details; `tags: "#kpi-report #report-<cadence>"` |
| What's-working/not finding | `interaction` (type: research) | `relevance` = finding + context + recommended action + linked skill; `tags: "#kpi-finding"` |
| Per-rep coaching slice | `interaction` (type: research) | `relevance` = rep activity + outcomes + coaching recommendation; `tags: "#kpi-rep-coaching"` |
| Action triggered | `interaction` (type: research) | `relevance` = action + downstream skill + parameters; `tags: "#kpi-action-triggered"` |

## Source Tag
`source: "skill:kpi-reporting:v2.1.0"`

## Example Push — Weekly Report

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#kpi-report #report-weekly",
    "relevance": "GTM weekly report 2026-06-01. North-star: $42K pipeline (+18% WoW). Leading: 800 email → 32 replies (4%) → 8 meetings; 60 LI → 11 accepted → 4 mtgs; 50 calls → 6 connects (4%⚠️) → 2 mtgs. Lagging: 3 closed-won @ $34K; Tier-1 win 12% (↓6pp⚠️). Working: email quality held; LI Vision 18%. Not: call 4% connect; Tier-1 win drop. Actions: data-enrichment phone re-verify; Tier-1 monitor.",
    "source": "skill:kpi-reporting:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: <source-skill>:run_<id>]` | Standard mapping |
| `[unverified — needs check]` (stale source) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; report flagged partial |
| `[hypothetical]` | Never pushes |
