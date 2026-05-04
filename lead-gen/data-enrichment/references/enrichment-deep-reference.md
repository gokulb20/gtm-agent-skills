# Data Enrichment: Deep Reference

## Email Verification Waterfall

The verification cascade — try each gate in order, lowest cost first. Failing any gate downgrades the verdict.

1. **Syntax check** — local, free. Rejects malformed addresses.
2. **MX record lookup** — local DNS, cheap. Rejects domains with no mail server.
3. **Verifier API call** (MillionVerifier / NeverBounce / ZeroBounce / Hunter) — returns `valid`, `invalid`, `risky`, `catch-all`, `role-based`, `unknown`.
4. **Catch-all domain detection** — if verifier returns `valid` but domain is accept-all (accepts any address), downgrade to `email_status: catch-all-domain`.
5. **Role-address detection** — `info@`, `sales@`, `support@`, `hello@` → `email_status: role-based`.

### Mapping to Lead Schema

| Verifier Result | `email_status` |
|---|---|
| valid | `verified` |
| risky / unknown | `risky` |
| catch-all | `catch-all-domain` |
| role-based | `role-based` |
| invalid | `invalid` |
| (no verifier configured) | `unverified` |

### Verifier Cost Comparison

| Tool | Cost/1000 | Notes |
|---|---|---|
| MillionVerifier | ~$1.50 | Cheapest, accurate; primary for batch |
| NeverBounce | ~$3 | Higher accuracy on edge cases |
| ZeroBounce | ~$5 | Most expensive; "AI scoring" for risky |
| Hunter Verifier | Included w/ Hunter API | When already pulling patterns |

### Catch-All Domain Rule

Domains like `@apple.com`, `@meta.com`, `@goldmansachs.com` accept any email pattern. Verifier returns `valid` for every address. ALWAYS downgrade to `email_status: catch-all-domain` regardless of verifier verdict. Treat replies as the real validation.

## Phone Discovery and Classification

| Tool | What It Returns |
|---|---|
| Hunter (find phone) | Often landline/main; mobile rare |
| Lusha | Mobile-rich but expensive (~$0.10/contact) |
| Apollo (carry-over) | Sometimes has mobile flagged |

### Phone Status Mapping

| Result | `phone_status` |
|---|---|
| Mobile confirmed | `mobile` |
| Landline confirmed | `landline` |
| VoIP detected | `voip` |
| DNC listed (US) | `dnc` — strip from active record |
| Not found | `unverified` |
| Invalid format | `invalid` |

## Personalization Hook Capture

### Permission Flags

| Source | Flag | What It Gives |
|---|---|---|
| LinkedIn recent posts | `linkedin_recent_posts` | Prospect's own words — best hook quality. Requires Sales Nav or Apify session. |
| News / press search | `news_search` | Recent press mentions, funding, hires. |
| Company blog | `company_blog_scrape` | Public posts authored by prospect. |
| Podcast guest lists | `podcast_guest_search` | Prospect appeared on podcast — very high open-rate. |
| G2 review | `g2_review_search` | Public reviews of competitor. |

### Hook Rule (Hard)

A personalization hook ships ONLY with a citable source URL + date. No URL → no hook → `personalization_hook: null` with `[unverified — needs check]` reason.

The 9-second reading budget means hooks must be specific + recent + provable. Clichéd quotes with no source read as fabricated.

## Worked Example (Fictional — All Entities `[hypothetical]`)

**Product:** HelpdeskPro [hypothetical]
**Input:** 50 leads from sourcing run
**Results:**
- Email: 31 verified / 8 risky / 5 catch-all / 4 role-based / 2 invalid
- Phone: 9 mobile / 14 landline / 15 not found / 1 DNC-stripped
- Hook: 31 with citable URL / 19 no source (review queue)

**Hook example:** "Northstar CS [hypothetical] just hired their first VP of CX (announced 2026-04-19)." Source: news.example.com/northstar-vp-cx-hire-2026 [hypothetical].

## Push-to-CRM Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Verified email + phone + hook | `person` (PATCH) | `contactEmail`, `contactPhone`, `contactLinkedIn`, `contactAbout` (hook), `tags: "#enriched #email-verified"` |
| Hook source URL + date | `interaction` (research) | `relevance` = hook + URL + date; `tags: "#personalization-hook #function-2"` |
| Run record | `interaction` (research) | `relevance` = run summary; `tags: "#enrichment-run #function-2"` |
| `[unverified — needs check]` | `interaction` (research) ONLY | `tags: "#unverified #review-required #data-enrichment"` |

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | PATCH person fields |
| `[unverified — needs check]` | Only `interaction:research`; person NOT patched |
| `[hypothetical]` | Never push |

## Best-Effort Mode (No Verifier)

When no verifier is configured: run syntax + MX + pattern detection (`info@` → role-based; `@gmail.com` with company domain → personal-email flag). Cannot promote past `email_status: unverified`. Tag everything `[unverified — needs check]`. 100% to review queue. Recommend configuring MillionVerifier before next pass.
