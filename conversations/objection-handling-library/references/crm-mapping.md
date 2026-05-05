# Push-to-CRM Mapping — Objection Handling Library

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-objection match + variants | `interaction` (type: reply-response) | `relevance` = matched label + confidence + variants + framework + cadence action; `tags: "#objection-handling #obj-<label> #conversations"` |
| Cadence-state change | `person` (PATCH) | `cadence_state`, `next_followup_at`, `last_objection_class` |
| Competitor mention captured | `interaction` (type: research) | `relevance` = competitor + reply context; `tags: "#competitor-signal"` |
| New-objection-pattern flag | `interaction` (type: research) | `relevance` = unmatched text + best-match attempts; `tags: "#new-objection-pattern #manual-review"` |
| Run record | `interaction` (type: research) | `relevance` = total objections + match distribution + new-pattern count |

## Source Tag
`source: "skill:objection-handling-library:v2.1.0"`

## Example Push — Matched Objection

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#objection-handling #obj-already-using-competitor #conversations",
    "relevance": "Objection matched: already-using-competitor (Guru) confidence 0.92. Framework: counter-position. 3 variants generated. Cadence action: nurture-90d.",
    "source": "skill:objection-handling-library:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` + `[verified: llm-match:run_<id>]` | Standard mapping |
| `[unverified — needs check]` (match <0.7) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; cadence action deferred |
| `[hypothetical]` | Never pushes |
