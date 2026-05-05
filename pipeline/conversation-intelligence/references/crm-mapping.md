# Push-to-CRM Mapping — Conversation Intelligence

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-conversation extracted pattern | `interaction` (type: research) | `relevance` = pattern class + verbatim quote + source timestamp + confidence; `tags: "#conversation-intel #pattern-<class>"` |
| Threshold-crossing alert | `interaction` (type: research) | `relevance` = pattern class + frequency + window + verbatim quote list; `tags: "#threshold-alert #pattern-<class>"` |
| Champion/blocker flag | `person` / `company` (PATCH) | `champion_status`, `blockers: [...]`, tags updated |
| Run record | `interaction` (type: research) | `relevance` = corpus stats + threshold crossings + routes; `tags: "#conversation-intelligence-run"` |

## Source Tag
`source: "skill:conversation-intelligence:v2.1.0"`

## Example Push — Extracted Pattern

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#conversation-intel #pattern-competitor-mention",
    "relevance": "Pattern from Gong gong_2026-06-02_esme. Class: competitor-mention. Entity: Guru. Quote @ 12:34: \"we considered Guru last year but found their search bad\". Confidence: 0.94.",
    "source": "skill:conversation-intelligence:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (transcript) + `[verified: <transcript-id>:<timestamp>]` | Standard mapping |
| `[unverified — needs check]` (confidence <0.7) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; no PATCH or route |
| `[hypothetical]` | Never pushes |
