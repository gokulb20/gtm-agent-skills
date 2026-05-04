# Push-to-CRM Mapping — Market Research

## Entity Mapping

| Deliverable | Entity | Notes |
|---|---|---|
| Beachhead segment + full Market Brief | `interaction` (type: research) | One per skill run; `relevance` = full brief; tags `#market-research #beachhead-defined` |
| Named Tier 1 candidate accounts | `company` | `tags: "#beachhead-candidate #market-research"`, `priority: warm` |
| Whitespace hypotheses with named target accounts | `interaction` (type: note) | One per whitespace card; tags `#whitespace #market-research` |

If no specific accounts are named, push only the research interaction. Do not invent accounts.

## Source Tag
`source: "skill:market-research:v2.1.0"`

## Example Push — Research Interaction

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "relevance": "Market Brief: Resegmented market in AI-powered support knowledge management. TAM $186M (bottom-up, Medium confidence). Beachhead: Series B SaaS, 100–300 emp, US, support team 5–15.",
    "tags": "#market-research #beachhead-defined",
    "source": "skill:market-research:v2.1.0"
  }'
```

## Example Push — Tier 1 Candidate Company

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Stitchbox",
    "industry": "SaaS",
    "tags": "#beachhead-candidate #market-research",
    "priority": "warm",
    "relevance": "Series B SaaS, 100–300 emp, support team 5–15, US — matches beachhead segment.",
    "source": "skill:market-research:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: research) tagged `#unverified #review-required #market-research` |
| `[hypothetical]` | Does NOT push. Local artifact only |

## When NOT to Push
- No beachhead identified (skill incomplete)
- TAM <$1M ("do not pursue" recommendation, not CRM data)
- User explicitly asked for analysis only (`--no-push`)
