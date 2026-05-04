# Push-to-CRM Mapping — Competitive Intelligence

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Watch-list competitors | `company` | `tags: "#competitor #ci-tier:direct"` etc.; only if not already created by `competitor-analysis` |
| Each scored signal (≥10) | `interaction` (type: note) | `relevance` = signal; tags `#ci-signal #competitor:<slug> #category:<x> #ci-score:<n>` |
| Signal taxonomy + alert routing | `interaction` (type: research) | One-time setup; tagged `#ci-system-config` |
| Quarterly review summary | `interaction` (type: research) | One per quarter; tagged `#ci-quarterly` |

Push every signal score ≥10 (24h alert threshold). Signals 5–9 stay local; <5 dropped.

## Source Tag
`source: "skill:competitive-intelligence:v2.1.0"`

## Example Push — High-Score Signal

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Guru",
    "tags": "#ci-signal #competitor:guru #category:pricing #ci-score:18",
    "relevance": "Guru added new pricing tier ($30/user Enterprise) detected via Visualping. Strength: 5. Decision-relevance: 4. Total: 20. Action: refresh battle-card pricing column.",
    "source": "skill:competitive-intelligence:v2.1.0"
  }'
```

## Special Routing

Signal scores ≥21 (strategic event): push to CRM **and** tag `#ci-strategic-event #re-run-needed` to trigger `competitor-analysis` re-run.

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction` tagged `#unverified #review-required #competitive-intelligence` |
| `[hypothetical]` | Does NOT push. Local artifact only |

## When NOT to Push
- Signal score <10 (stays in local log)
- Sentiment-only signals without a named action
