# Push-to-CRM Mapping — Customer Feedback Analysis

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-theme extraction | `interaction` (type: research) | `relevance` = theme class + verbatim + source + sentiment + entity + confidence; `tags: "#customer-feedback #theme-<class>"` |
| Cross-corpus aggregation | `interaction` (type: research) | `relevance` = per-class frequency + segment breakdown + thresholds; `tags: "#feedback-aggregation"` |
| ICP-implication flag | `interaction` (type: research) | `relevance` = theme + segment + frequency + recommended ICP refinement; `tags: "#icp-implication"` |
| Product backlog routing | `interaction` (type: research) | `relevance` = item + frequency + severity + issue link; `tags: "#product-backlog-routed"` |
| Champion language | `interaction` (type: research) | `relevance` = verbatim + source + recommended use; `tags: "#champion-copy-bank"` |

## Source Tag
`source: "skill:customer-feedback-analysis:v2.1.0"`

## Example Push — Theme Extraction

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#customer-feedback #theme-champion-language",
    "relevance": "Theme from JTBD interview. Class: champion-language. Verbatim: \"I told my VP this would cut new-hire ramp from 8 weeks to 3.\" Sentiment: positive. Route: copy bank.",
    "source": "skill:customer-feedback-analysis:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (transcript) + `[verified: <source-id>]` (extraction) | Standard mapping |
| `[unverified — needs check]` (no verbatim or confidence <0.7) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; no downstream routing |
| `[hypothetical]` | Never pushes |
