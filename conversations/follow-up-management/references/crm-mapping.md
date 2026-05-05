# Push-to-CRM Mapping — Follow-Up Management

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-recipient schedule | `interaction` (type: research) | `relevance` = trigger + parsed-date + flow + framework + scheduled-touch ref; `tags: "#follow-up-scheduled #flow-<type>"` |
| Nurture cadence definition | `interaction` (type: research) | `relevance` = touches + day_offsets + frameworks; `tags: "#nurture-cadence"` |
| Person state PATCH | `person` (PATCH) | `next_followup_at`, `nurture_state`, `cadence_state`, `last_no_show_at` |
| No-show rescue trigger | `interaction` (type: research) | `relevance` = no-show event + rescue flow; `tags: "#no-show-rescue"` |
| Run record | `interaction` (type: research) | `relevance` = triggers + flow distribution + scheduled-touch count |

## Source Tag
`source: "skill:follow-up-management:v2.1.0"`

## Example Push — Resume Scheduled

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#follow-up-scheduled #flow-not-now-with-date",
    "relevance": "Follow-up scheduled for esme@stitchbox.com. Trigger: not-now reply with date Q1 2027. Parsed: 2027-01-15. Flow: single resume. Channel: email. Framework: resurrection.",
    "source": "skill:follow-up-management:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` + `[verified: reply-text]` | Standard mapping |
| `[unverified — needs check]` (ambiguous date) | Pushes ONLY as `interaction:research` with `#unverified #review-required`; person PATCH deferred |
| `[hypothetical]` | Never pushes |
