# Push-to-CRM Mapping — ICP Refinement Loop

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| ICP refinement report | `interaction` (type: research) | `relevance` = cutoff calibration + weight re-tuning + segment shifts + lost-reason patterns + retroactive proposal; `tags: "#icp-refinement"` |
| Per-recommendation evidence | `interaction` (type: research) | `relevance` = recommendation + evidence (deal counts + IDs + rates); `tags: "#icp-refinement-recommendation"` |
| User authorization queue | `interaction` (type: research) | `relevance` = pending recommendations + auth status; `tags: "#manual-review #icp-refinement-auth"` |
| Lost-reason pattern | `interaction` (type: research) | `relevance` = competitor + deal count + lost-rate; `tags: "#lost-to-competitor-pattern"` |
| Confidence rubric upgrade | `interaction` (type: research) | `relevance` = old → new tier + evidence (n closes); `tags: "#confidence-rubric-upgrade"` |

## Source Tag
`source: "skill:icp-refinement-loop:v2.1.0"`

## Example Push — Refinement Run

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#icp-refinement",
    "relevance": "ICP refinement Q2-2026 (47 closes). (1) T1 cutoff: 8/30 wins scored <75 → recommend 72. (2) Trigger weight 20→30 (correl 0.68). (3) 8 Healthcare wins → segment decision. (4) 7 lost-to-Guru → competitive-intel. (5) Retroactive: 4 T2→T1 / 2 T1→T2. Confidence: Hypothesis → Medium.",
    "source": "skill:icp-refinement-loop:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: closed-deals:n=<N>]` | Standard mapping |
| `[unverified — needs check]` (ambiguous evidence or marginal n) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; user auth required before rubric update |
| `[hypothetical]` | Never pushes |
