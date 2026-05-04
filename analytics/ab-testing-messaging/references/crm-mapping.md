# Push-to-CRM Mapping — A/B Testing Messaging

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Test design (at launch) | `interaction` (type: research) | `relevance` = hypothesis + variants + split + metrics + method + thresholds; `tags: "#ab-test-design"` |
| Test result (at call) | `interaction` (type: research) | `relevance` = method + n per arm + rates + posterior/p-value + effect + winner/inconclusive; `tags: "#ab-test-result"` |
| Shipped-winner action | `interaction` (type: research) | `relevance` = winner + traffic shift + handoff; `tags: "#ab-test-ship-winner"` |
| Inconclusive declaration | `interaction` (type: research) | `relevance` = outcome + underpowered + default action; `tags: "#ab-test-inconclusive"` |

## Source Tag
`source: "skill:ab-testing-messaging:v2.1.0"`

## Example Push — Winner

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#ab-test-result #ab-test-ship-winner",
    "relevance": "A/B test result: n=180/arm. A: 4.1% (7). B: 7.2% (13). Bayesian P(B>A)=0.96. Effect: 3.1pp. WINNER: B (CCQ+Vision). Ship 100% to B.",
    "source": "skill:ab-testing-messaging:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (variants) + `[verified: campaign-management:run_<id>]` (metrics) | Standard mapping |
| `[unverified — needs check]` (metric source uncertain) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; significance call deferred |
| `[hypothetical]` | Never pushes |
