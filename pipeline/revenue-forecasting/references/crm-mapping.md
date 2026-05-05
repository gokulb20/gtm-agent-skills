# Push-to-CRM Mapping — Revenue Forecasting

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Forecast (per horizon, per scenario) | `interaction` (type: research) | `relevance` = scenarios + assumption set + top-10 + confidence; `tags: "#revenue-forecast"` |
| Per-stage weighted breakdown | `interaction` (type: research) | `relevance` = stage / count / avg value / weighted contribution; `tags: "#weighted-pipeline"` |
| Forecast-accuracy audit | `interaction` (type: research) | `relevance` = prior vs actual + MAPE + recalibration; `tags: "#forecast-accuracy-audit"` |
| Conversion rate update | `interaction` (type: research) | `relevance` = recalibrated rates; `tags: "#conversion-rate-update"` |

## Source Tag
`source: "skill:revenue-forecasting:v2.1.0"`

## Example Push — Q3 Forecast

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#revenue-forecast",
    "relevance": "Q3 forecast (90d). Conservative $185K / Base $310K / Aggressive $425K. Top-10 = 76% (risk flag). Confidence: High (45 closes).",
    "source": "skill:revenue-forecasting:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: historical-closes:n=<N>]` | Standard mapping |
| `[unverified — needs check]` (defaults) | Pushes with `#unverified #review-required #default-rates` AND `confidence: low` |
| `[hypothetical]` | Never pushes |
