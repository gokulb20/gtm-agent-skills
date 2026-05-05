# Push-to-CRM Mapping — Positioning Strategy

## Entity Mapping

Positioning is a shared messaging asset, not entity records. Push as research/note interactions.

| Deliverable | Entity | Push fields |
|---|---|---|
| Positioning canvas | `interaction` (type: research) | `relevance` = full canvas; tags `#positioning #positioning-canvas` |
| Wedge + 3-test diagnostic | `interaction` (type: note) | tags `#positioning-wedge` |
| Message house | `interaction` (type: note) | tags `#message-house` |
| For-and-against wedges (top-3) | `interaction` (type: note) | One per competitor; tags `#positioning-wedge #competitor:<slug>` |
| Buyer-language audit | `interaction` (type: note) | tags `#positioning #language-audit` |

Positioning does **not** push `company` or `person` records — it operates on entities created by `icp-definition` and `competitor-analysis`.

## Source Tag
`source: "skill:positioning-strategy:v2.1.0"`

## Example Push — Positioning Canvas

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#positioning #positioning-canvas",
    "relevance": "POSITIONING CANVAS: Alternatives: Guru, Stonly, Notion, status quo. Unique: AI-native authoring; per-support-seat pricing; ticket ingestion. Best-fit ICP: Series B SaaS, 100-300 emp. Category: AI-native support runbook authoring (subcategory).",
    "source": "skill:positioning-strategy:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction` tagged `#unverified #review-required #positioning` |
| `[hypothetical]` | Does NOT push. Local artifact only |

## When NOT to Push
- ICP not yet defined
- Positioning marked "to be validated" with no proof — push as `#positioning-hypothesis` instead
