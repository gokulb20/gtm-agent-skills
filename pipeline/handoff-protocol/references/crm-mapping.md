# Push-to-CRM Mapping — Handoff Protocol

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Handoff event | `interaction` (type: handoff) | `relevance` = state + rep + SAL result + reason if rejected; `tags: "#handoff #handoff-<state>"` |
| Handoff package | `interaction` (type: research) | `relevance` = package or pointer; `tags: "#handoff-package"` |
| Deal owner change | `deal` (PATCH) | `owner_rep_id`, `handoff_accepted_at`, `prior_owner_rep_id`, `handoff_count` |
| Rejection route | `interaction` (type: research) | `relevance` = rejection reason + fix recommendation; `tags: "#handoff-rejected #sdr-fix-needed"` |

## Source Tag
`source: "skill:handoff-protocol:v2.1.0"`

## Example Push — Accepted

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#handoff #handoff-accepted",
    "relevance": "Handoff SDR Will → AE Jordan. Delivered via Slack. SAL pre-check 4/4 ✓. Accepted 28 min. Deal owner transitioned.",
    "source": "skill:handoff-protocol:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: <source>]` or `[user-provided]` | Standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required`; deal PATCH deferred |
| `[hypothetical]` | Never pushes |
