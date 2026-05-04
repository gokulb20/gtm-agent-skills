# Push-to-CRM Mapping — Pipeline Stages

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Stage transition | `interaction` (type: stage-change) | `relevance` = from→to + trigger + gate result + prior duration; `tags: "#stage-change #stage-<to>"` |
| Deal PATCH | `deal` (PATCH) | `stage`, `stage_entered_at`, `prior_stage_duration_days`, `meddpicc_slots_filled`, `lost_reason` |
| Stuck-deal flag | `interaction` (type: research) | `relevance` = deal id + time-in-stage + missing element; `tags: "#stuck-deal"` |
| Bulk audit report | `interaction` (type: research) | `relevance` = correct/wrong distribution + per-deal recs; `tags: "#pipeline-audit"` |

## Source Tag
`source: "skill:pipeline-stages:v2.1.0"`

## Example Push — Stage Advance

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#stage-change #stage-meeting",
    "relevance": "Deal advanced Engaged → Meeting. Trigger: meeting booked 2026-06-02T14:00. Gate: meeting scheduled ✓. Prior stage duration: 8d.",
    "source": "skill:pipeline-stages:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: <source>]` or `[user-provided]` | Standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required`; deal PATCH deferred |
| `[hypothetical]` | Never pushes |
