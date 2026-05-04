# Push-to-CRM Mapping — Channel Strategy

## Entity Mapping

Channel strategy is a plan + budget, not entity records. Push as research/note interactions.

| Deliverable | Entity | Push fields |
|---|---|---|
| Bullseye plan + budget | `interaction` (type: research) | `relevance` = full plan; tags `#channel-strategy #bullseye` |
| Per-channel experiment (top-3) | `interaction` (type: note) | One per channel; tags `#channel-experiment #channel:<name>` |
| CAC/LTV viability table | `interaction` (type: note) | tags `#channel-economics` |
| Kill criteria + stage graduation | `interaction` (type: note) | tags `#channel-kill-criteria` |

Channel strategy does **not** push `company` or `person` records — those come from lead-sourcing once a channel is picked.

## Source Tag
`source: "skill:channel-strategy:v2.1.0"`

## Example Push — Bullseye Plan

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#channel-strategy #bullseye",
    "relevance": "CHANNEL PLAN: Middle ring: (1) Outbound — 200 accounts/wk, $2.5k; (2) Community — founder time 5h/wk; (3) Podcasts (wildcard) — $500, 12wk. Kill: outbound CAC >$2k after 8wk; community 0 inbound after 60d.",
    "source": "skill:channel-strategy:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction` tagged `#unverified #review-required #channel-strategy` |
| `[hypothetical]` | Does NOT push. Local artifact only |

## When NOT to Push
- ICP or positioning not defined
- User pre-PMF asking for paid-channel scaling — push `#channel-strategy #recommendation:hold` only
