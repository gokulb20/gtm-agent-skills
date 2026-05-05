# Lead Sourcing — LinkedIn: Deep Reference

## Sales Nav Filter Patterns

| ICP Criterion | Sales Nav Filter | Notes |
|---|---|---|
| Role titles | `Title` (with Boolean AND/OR/NOT) | Use variants: "VP Marketing" OR "Vice President, Marketing" |
| Seniority | `Seniority Level` | VP, Director, Manager, etc. |
| Function | `Function` | Marketing, Engineering, Sales, etc. |
| Geography | `Geography` | City/state/country |
| Company size | `Company Headcount` | 51-200, 201-500, etc. |
| Industry | `Industry` | |
| Recent role change | `Years in Current Position: Less than 1 year` | Cleanest trigger-recency filter |
| Active poster | `Spotlights: Posted on LinkedIn in past 30 days` | Leading indicator of reply rate |
| Leadership change | `Spotlights: Changed jobs in past 90 days` | |
| Company expansion | `Company Headcount Growth: > 10%` | |
| Anti-ICP exclusions | `Industry: NOT [...]`, `Title: NOT intern` | |

Sales Nav encodes all filters in URL parameters — the URL IS the audit handle.

## Three-Mode Degradation

### API-Substitute Mode (PhantomBuster/HeyReach)
Sales Nav seat + session-based tool API key. Tool runs search on user's behalf using their LinkedIn session. Returns CSV. Provenance: `[verified: phantombuster:run_<id>]` or `[verified: heyreach:run_<id>]`.

### Manual Mode
Sales Nav seat alone. Skill outputs:
1. Reproducible Sales Nav search URL with all encoded filter params
2. Step-by-step recipe (which dropdowns, which Spotlights, exact Boolean keyword string)
3. Column-set for export: Name, Title, Company, LinkedIn URL, Location, Seniority, Function, "Started in Current Role" date

Note: 25 leads/page UI cap; maximum 1,000 results per search; recommend batch ≤100 for manual export.

### BYO Mode
User uploads Sales Nav CSV. Skill normalizes with `[user-provided]` provenance for non-native columns.

## Worked Example (Fictional — All Entities `[hypothetical]`)

**Product:** MetricMojo [hypothetical]
**ICP:** Series B SaaS, 100–500 emp, US, VP Marketing hire <90d

**Filter recipe:**
```
Title: ("VP of Marketing" OR "Vice President, Marketing" OR "Head of Marketing")
Seniority Level: VP
Function: Marketing
Geography: United States
Industry: Computer Software, SaaS
Company Headcount: 51-200, 201-500
Spotlights: Changed jobs in past 90 days
Years in Current Position: Less than 1 year
NOT Industry: Marketing & Advertising
```

**PhantomBuster run:** 308 profiles → 305 normalized → 291 pushed (14 dedup merges).
**Trigger breakdown:** 305 recent-role-change / 91 active-posters / 47 company-growth.
**Emails:** 0 verified (Sales Nav limitation) — `data-enrichment` mandatory next.

## Push-to-CRM Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each unique company | `company` | `website`, `industry`, `companySize`, `tags: "#sourced-linkedin #icp-tier-pending"` |
| Each unique person (verified/user-provided) | `person` | `contactName`, `contactTitle`, `contactLinkedIn`, `contactEmail` (typically absent) |
| Run record | `interaction` (research) | `relevance` = run summary; `tags: "#linkedin-sourcing-run #function-2"` |
| Privacy-mode / partial profiles | `interaction` (research) ONLY | `tags: "#unverified #review-required #lead-sourcing-linkedin"` |

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Full push; note: emails typically `[unverified]` even on verified LinkedIn-source records |
| `[unverified — needs check]` | Only `interaction:research` with review tags |
| `[hypothetical]` | Never push |

## ToS Compliance Hard Rules

- **Direct scraping:** REFUSED. Forbidden by LinkedIn User Agreement. Account-suspension and legal risk.
- **Session-based tools:** Acceptable (PhantomBuster, HeyReach use user's own credentials).
- **Content scope:** Public-profile content only. Private posts forbidden.
- **Connection requests:** Stay out of outreach (function-3). LinkedIn limits ~100/week.

## Dedup and Freshness Rules

`linkedin_url` is THE primary merge key for this skill — doubled in priority vs other sourcing skills.

Freshness: Sales Nav lags reality by 2–14 days. "Started in role 5 days ago" may be 5 weeks ago in reality.

PhantomBuster pacing: 50–100 profiles/day per session is safe; aggressive usage risks account flag.
