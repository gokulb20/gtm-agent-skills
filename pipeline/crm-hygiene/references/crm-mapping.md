# Push-to-CRM Mapping — CRM Hygiene

## Entity Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Hygiene violation report | `interaction` (type: research) | `relevance` = severity-grouped violations + fixes; `tags: "#hygiene-audit"` |
| Dedup merge plan | `interaction` (type: research) | `relevance` = per-merge group + recommendation; `tags: "#dedup-merge-plan #manual-review"` |
| Normalization fix | `person` / `company` (PATCH) | normalized field + `#normalized` tag |
| Orphan cleanup | `interaction` (PATCH) | `re_link_to: <surviving_id>` or `archived: true` + `#orphan-cleanup` |
| Stale-field flag | `person` / `company` (PATCH) | `#stale-<field> #needs-re-enrichment` tag + `next_re_enrichment_at` |

## Source Tag
`source: "skill:crm-hygiene:v2.1.0"`

## Example Push — Audit Run

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#hygiene-audit",
    "relevance": "Weekly hygiene audit. 8 P0 / 23 P1 / 15 P2. Auto-applied: 8 normalizations + 4 orphans. Deferred: 2 dedup merges + 12 stale re-verifications.",
    "source": "skill:crm-hygiene:v2.1.0"
  }'
```

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[verified: <crm-query>]` | Standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required`; no auto-fixes |
| `[hypothetical]` | Never pushes |
