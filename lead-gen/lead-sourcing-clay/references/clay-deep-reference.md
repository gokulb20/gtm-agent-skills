# Lead Sourcing — Clay: Deep Reference

## Provider Chain Options and Costs

| Layer | Provider | Typical Cost/Row | What It Adds |
|---|---|---|---|
| Search | Apollo (via Clay) | ~$0.04 | Firmographic + persona |
| Search | Crunchbase (via Clay) | ~$0.05 | Funding events, stage |
| Email | Hunter (via Clay) | ~$0.03 | Email pattern guess |
| Email | LeadMagic (via Clay) | ~$0.04 | Better catch-all detection |
| Phone | Lusha (via Clay) | ~$0.10 | Mobile-rich |
| Tech | BuiltWith (via Clay) | ~$0.02 | Tech stack |
| Verifier | MillionVerifier (via Clay) | ~$0.0015 | Deliverability |

Source priority for overlapping fields: **verifier-checked > Hunter pattern guess > Apollo claim**.

## Three-Mode Degradation

### API Mode
`CLAY_API_KEY` set. Programmatic table creation and row materialization. Rate limit ~100 rows/sec; backoff on 429.

### Manual Mode
Clay seat but no API key. Skill outputs reproducible `clay_table_spec` — search-step filters paste-ready, ordered list of columns to add, output column-set. User runs in Clay UI, exports CSV.

### BYO Mode
User has existing Clay table CSV. Skill ingests, preserves Clay's column-attribution where present, defaults to `[user-provided]` if attribution lost.

## Worked Example (Fictional — All Entities `[hypothetical]`)

**Product:** RouteIQ [hypothetical]
**ICP:** Fleet ops directors at mid-market trucking companies in TX/OK/AR

**Provider chain:** Apollo + Crunchbase + Hunter + MillionVerifier
**Budget conflict:** Full chain ~$34.87 on 287 rows, over $25 cap. User drops Crunchbase → ~$20.52.

**Table spec:**
```yaml
search_step:
  provider: clay-apollo
  filters:
    organization_industries: ["transportation/trucking/railroad", "logistics & supply chain"]
    organization_num_employees_ranges: ["51,200", "201,500"]
    organization_locations: ["Texas", "Oklahoma", "Arkansas"]
    person_titles: ["VP Operations", "Director of Fleet", "Fleet Operations Manager"]
columns:
  - name: find_email
    provider: clay-hunter
    inputs: [first_name, last_name, company_domain]
  - name: verify_email
    provider: clay-millionverifier
    inputs: [find_email.email]
```

**Results:** 287 rows → 281 normalized → 273 pushed (8 dedup merges).
**Multi-source provenance:** company `[verified: clay-apollo]`, email `[verified: clay-million-verifier]`.
**Email status:** 198 verified / 41 risky / 12 catch-all / 30 invalid.
**Recommended next:** `lead-scoring` directly (Clay run replaces separate enrichment).

## Push-to-CRM Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-clay #icp-tier-pending"` |
| Each unique person (verified/user-provided) | `person` | `contactName`, `contactTitle`, `contactEmail`, `contactPhone`, `contactLinkedIn` |
| Run record (table_id, spec, per-provider costs) | `interaction` (research) | `relevance` = run summary; `tags: "#clay-sourcing-run #function-2"` |
| `[unverified — needs check]` (provider failed) | `interaction` (research) ONLY | `tags: "#unverified #review-required #lead-sourcing-clay"` |

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Full push; multi-source provenance flattened at push time |
| `[unverified — needs check]` | Only `interaction:research` with review tags |
| `[hypothetical]` | Never push |

## Clay-Specific Knowledge

- Tables are persistent; re-run when columns refresh; preserve `clay_table_id` for 30-day replay
- Re-running same row × same column within ~24h is free (caching)
- "Find email" composite column tries Hunter → LeadMagic → Findymail in sequence; capture which provider hit
- Clay's writeback step can push to CRM directly, but skill maintains own push for provenance contract uniformity
- Clay's "valid" flag is real verification only when MillionVerifier/NeverBounce is in the chain
- Clay's "find email" waterfall: Hunter → LeadMagic → Findymail default; capture per-provider attribution

## Dedup and Freshness Rules

Same as Apollo skill: `linkedin_url` > `email` > `phone` (person); `company_domain` (company).
On collision: keep higher-tier provenance + more recent `freshness_date`.

When NOT to push: provider outage left >50% rows incomplete → abort; route everything to review queue.
