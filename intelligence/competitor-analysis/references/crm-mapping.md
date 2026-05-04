# Push-to-CRM Mapping — Competitor Analysis

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Named-product competitor (Direct / product-Substitute) | `company` | `tags: "#competitor #competitor-tier:direct"` (or `:substitute`); `priority: cold` |
| Non-product alternative (DIY / hire / do-nothing / shift-budget) | `interaction` (type: research) | `relevance` = description + buyer quote; tags `#alternative #type:non-product #tier:substitute`. **No company record** |
| Per-competitor profile (named products) | `interaction` (type: research) | `relevance` = full profile; tags `#competitor-profile` |
| Battle card (top 3) | `interaction` (type: note) | One per competitor; tags `#battle-card` |
| Helmer + segment-ownership synthesis | `interaction` (type: research) | One; tags `#strategic-analysis` |

## Critical Split

Named products (Notion, Confluence) → `company` records. Non-product alternatives ("Hire a VA", "Do nothing") → `interaction` only. Pushing "Outsourced VA" as a `company` creates fake prospects.

## Source Tag
`source: "skill:competitor-analysis:v2.1.0"`

## Example Push — Direct Competitor

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Guru",
    "website": "https://getguru.com",
    "industry": "SaaS",
    "tags": "#competitor #competitor-tier:direct",
    "priority": "cold",
    "relevance": "Direct competitor — knowledge management. Strength: 6+ years brand. Weakness: pre-LLM authoring UX.",
    "source": "skill:competitor-analysis:v2.1.0"
  }'
```

## Example Push — Non-Product Alternative (interaction only, no company record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#alternative #type:non-product #tier:substitute",
    "relevance": "ALTERNATIVE: DIY via spreadsheets + Slack channels. Observed in 2 lost deals.",
    "source": "skill:competitor-analysis:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction` tagged `#unverified #review-required #competitor-profile` |
| `[hypothetical]` | Does NOT push. Local artifact only |

## When NOT to Push
- User claims "no competitors" and skill couldn't surface alternatives
- Aspirational / Indirect tier — local artifact only
