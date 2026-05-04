# Push-to-CRM Mapping — Channel Performance

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Channel performance report | `interaction` (type: research) | `relevance` = per-channel CPM/CPD + attribution + marginal-CAC + ranking + reallocation + Bullseye; `tags: "#channel-performance"` |
| Per-channel attribution detail | `interaction` (type: research) | `relevance` = last-touch + multi-touch breakdown; `tags: "#channel-attribution"` |
| Reallocation recommendation | `interaction` (type: research) | `relevance` = source + target + shift amount + risk; `tags: "#channel-reallocation"` |
| Bullseye refresh | `interaction` (type: research) | `relevance` = never-tested channel + cost-to-test; `tags: "#bullseye-refresh"` |

## Source Tag
`source: "skill:channel-performance:v2.1.0"`

## Example Push — Quarterly Review

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#channel-performance",
    "relevance": "Q2 channel review. Email: CPM $37.50 / CPD $150 (LT) $135 (MT) / marginal high. LinkedIn: CPM $58 / CPD $233 / $250 / marginal low. Call: CPM $133 / CPD $480 / $420. Recommend: shift 15% email→LinkedIn. Bullseye: web-sourced ring-2 test.",
    "source": "skill:channel-performance:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: campaign-management:run_<id>]` + `[user-provided]` (costs) | Standard mapping |
| `[unverified — needs check]` (insufficient data) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; reallocation deferred |
| `[hypothetical]` | Never pushes |
