# Push-to-CRM Mapping — Reply Classification

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-reply classification | `interaction` (type: reply) | `relevance` = label + confidence + rationale + embedded objection + dispatched-to; `tags: "#reply #class-<label> #conversations"` |
| Cadence-state change | `person` (PATCH) | `last_reply_class`, `last_reply_at`, `cadence_state`, `next_followup_at` |
| Manual review queue entry | `interaction` (type: research) | `relevance` = reply + LLM best guess + rationale + confidence; `tags: "#manual-review #reply-classification"` |
| Run record | `interaction` (type: research) | `relevance` = label distribution + confidence histogram + dispatched counts; `tags: "#reply-classification-run"` |
| Embedded competitor/objection signal | `interaction` (type: research) | `relevance` = signal text + classification + parent reply id; `tags: "#competitor-signal"` |

## Source Tag
`source: "skill:reply-classification:v2.1.0"`

## Example Push — Positive Reply

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#reply #class-positive #conversations #cadence-exit",
    "relevance": "Reply classified positive at 2026-05-29T08:14 with confidence 0.94. Cadence exited; dispatched to discovery-call-prep.",
    "source": "skill:reply-classification:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (reply text) + `[verified: llm-classifier:run_<id>]` | Standard mapping |
| `[unverified — needs check]` (confidence <0.75) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; person PATCH deferred |
| `[hypothetical]` | Never pushes |

## When NOT to Push
- Reply already classified within 1h (dedup)
- Bounce auto-reply (route to channel skill)
- Draft LLM responses (not the user's reply)
