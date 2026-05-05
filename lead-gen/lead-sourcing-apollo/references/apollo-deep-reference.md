# Lead Sourcing — Apollo: Deep Reference

## Apollo API Endpoint Reference

| Endpoint | Purpose | Pagination |
|---|---|---|
| `POST /api/v1/mixed_people/search` | Persona search with firmographic filters | `page` + `per_page` (max 100) |
| `POST /api/v1/mixed_companies/search` | Firmographic-only search | `page` + `per_page` (max 100) |
| `POST /api/v1/people/match` | Lookup single person by email or LinkedIn URL | n/a |
| `POST /api/v1/organizations/enrich` | Enrich single company by domain | n/a |
| `GET /api/v1/labels` | Fetch canonical industry/technology/seniority taxonomies | n/a |

Rate limits: ~60 req/min on Pro, 120 req/min on Enterprise. `X-Rate-Limit-Remaining` header is authoritative. Credits charged per *unique* contact returned; repeating same search within ~24h costs 0 additional credits.

## ICP → Apollo Filter Mapping

| ICP Field | Apollo Filter | Notes |
|---|---|---|
| Industry | `organization_industries` | Use canonical strings from `/api/v1/labels` |
| Size band | `organization_num_employees_ranges` | Apollo bands: 1, 2-10, 11-20, 21-50, 51-100, 101-200, 201-500, 501-1000, 1001-2000, 2001-5000, 5001-10000, 10001+ |
| Geography | `person_locations` + `organization_locations` | |
| Funding stage | `organization_latest_funding_stage` | |
| Tech stack signal | `currently_using_any_of_technology_uids` | |
| Role titles | `person_titles` | Use both exact and Apollo normalized forms |
| Seniority | `person_seniorities` | c_suite → c-level, vp → vp, director → director, manager → manager, senior + entry → ic |
| Function | `person_departments` | |
| Anti-ICP | `not_organization_industries`, `not_organization_num_employees_ranges` | |

## Three-Mode Degradation

### API Mode
`APOLLO_API_KEY` set. Direct API calls with pagination, rate-limit handling, per-record cost tracking. Provenance: `[verified: apollo-api:run_<id>]`.

### Manual Export Mode
User has Apollo seat but no API key. Skill outputs:
1. Exact filter set to paste into Apollo UI
2. Column-set checklist: First Name, Last Name, Email, Email Status, LinkedIn URL, Phone, Title, Seniority, Departments, Company, Company Domain, Industry, Employees, Country, Founded Year, Latest Funding Stage, Technologies
3. 4-step instruction sheet for Search → Save → Export → Drop CSV

Provenance: `[user-provided]` for all CSV fields.

### BYO Mode
User has any list from anywhere. Skill reads CSV, infers column mapping, confirms with user, flags missing fields. Provenance: `[user-provided]` with `confidence: low` until enrichment promotes fields.

## Worked Example (Fictional — All Entities `[hypothetical]`)

**Product:** WorkflowDoc [hypothetical]
**ICP:** Series B SaaS, 100–300 emp, US, support team 5–15, Zendesk|Intercom
**Roles:** Buyer = VP/Director of Support; Champion = Support Ops Manager

**Filter translation:**
```yaml
person_titles: ["VP of Support", "Director of Support", "Head of Customer Support",
                "Support Operations Manager", "CX Operations Manager"]
person_seniorities: [vp, director, manager]
person_departments: [support, ops]
person_locations: ["United States"]
organization_industries: ["computer software", "software development"]
organization_num_employees_ranges: ["101,200", "201,500"]
organization_latest_funding_stage: ["series_b"]
currently_using_any_of_technology_uids: ["zendesk", "intercom"]
```

**discover() output:** ~340 contacts across ~110 companies, ~$7 credits.
**After pull + normalize + dedup:** 326 persons + 110 companies pushed, 12 dedup merges, 14 role-address sidecar.

## Push-to-CRM Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-apollo #icp-tier-pending"` |
| Each unique person (verified/user-provided) | `person` | `contactName`, `contactTitle`, `contactEmail`, `contactPhone`, `contactLinkedIn` |
| Run record | `interaction` (research) | `relevance` = run summary; `tags: "#apollo-sourcing-run #function-2"` |
| `[unverified — needs check]` records | `interaction` (research) ONLY | `tags: "#unverified #review-required #lead-sourcing-apollo"` |

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Full push (company/person/interaction) |
| `[unverified — needs check]` | Only `interaction:research` with review tags |
| `[hypothetical]` | Never push — local artifact only |

## Dedup and Freshness Rules

Merge keys priority: `linkedin_url` > `email` > `phone` (person); `company_domain` (company).
On collision: keep higher-tier provenance + more recent `freshness_date`.

Freshness half-lives:
- Email (verified): ~9 months
- Phone: ~12 months
- Title: ~6 months
- Funding signal: ~12 months
- Hiring signal: ~3 months
- Tech-adoption: ~6 months
- Press/news: ~6 months
