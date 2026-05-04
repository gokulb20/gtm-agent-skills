# Push-to-CRM Mapping — ICP Definition

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Tier 1 example accounts | `company` | `score: 5, priority: hot, tags: "#icp-tier-1 #beachhead"` |
| Tier 2 example accounts | `company` | `score: 3, priority: warm, tags: "#icp-tier-2"` |
| Tier 3 example accounts | `company` | `score: 2, priority: cold, tags: "#icp-tier-3"` |
| Anti-ICP examples | `company` | `score: 1, priority: cold, tags: "#anti-icp"` |
| Full ICP one-pager | `interaction` (type: research) | `relevance` = full ICP doc; tags `#icp-definition` |
| Buyer/Champion/User/Blocker role cards | `interaction` (type: note) | One per role; tags `#icp-role:buyer` etc. |

## Source Tag
`source: "skill:icp-definition:v2.1.0"`

## Example Push — Tier 1 Account

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "website": "https://stitchbox.com",
    "industry": "SaaS",
    "score": 5,
    "priority": "hot",
    "tags": "#icp-tier-1 #beachhead",
    "contactTitle": "Support Operations Manager",
    "relevance": "Tier 1 ICP — 87/100. Series B SaaS, 100–300 emp, support team 5–15.",
    "source": "skill:icp-definition:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction` tagged `#unverified #review-required #icp-definition` |
| `[hypothetical]` | Does NOT push. Local artifact only |

## When NOT to Push
- ICP marked "hypothesis-only" (0 customers) — push research interaction only, skip Tier company examples
- Confidence: Low — tag research interaction `#icp-low-confidence`
