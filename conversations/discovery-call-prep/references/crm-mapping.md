# Push-to-CRM Mapping — Discovery Call Prep

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| 1-page briefing | `interaction` (type: research) | `relevance` = full briefing + meeting context + freshness; `tags: "#discovery-briefing #conversations"` |
| MEDDPICC snapshot | `interaction` (type: research) | `relevance` = 8 slots + populated/unknown + provenance; `tags: "#meddpicc-snapshot"` |
| Per-meeting timestamp | `person` (PATCH) | `discovery_briefing_at`, `next_meeting_at`, `next_meeting_channel` |
| Pre-staged objections | `interaction` (type: research) | `relevance` = 3 objections + responses; `tags: "#pre-staged-objections"` |

## Source Tag
`source: "skill:discovery-call-prep:v2.1.0"`

## Example Push — Briefing

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#discovery-briefing #conversations #tier-1",
    "relevance": "Discovery briefing for 2026-06-02T14:00 call. Profile: VP CX @ Stitchbox, Tier-1/87. MEDDPICC: Metrics ✓ / EB ✓ / DC unknown / DP unknown / PP unknown / Pain ✓ / Champion ✓ / Competition Guru. 9 questions. 3 objections. Agenda: 5/15/10.",
    "source": "skill:discovery-call-prep:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: <source>]` or `[user-provided]` | Standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required`; person PATCH deferred |
| `[hypothetical]` | Never pushes |
