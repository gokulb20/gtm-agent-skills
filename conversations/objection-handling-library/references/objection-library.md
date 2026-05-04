# 12-Objection Canonical Library

## Library Entries

| # | Label | Pattern | Default framework | Cadence action |
|---|---|---|---|---|
| 1 | already-using-competitor | "We already use X" | counter-position (Dunford) | nurture-90d |
| 2 | no-budget | "No budget for this right now" | re-discovery (Bosworth) | nurture-90d + lead-scoring re-tier |
| 3 | no-authority | "Need to check with my boss/committee" | re-discovery + champion-build | pause-with-resume |
| 4 | no-need-now | "Not looking at this right now" | feel-felt-found | nurture-90d |
| 5 | bad-timing | "Focused on X right now / Q1 / after holidays" | time-shift | pause-with-resume |
| 6 | happy-with-status-quo | "Happy with how things are" | re-discovery (probe hidden pain) | nurture-90d |
| 7 | tried-similar-failed | "We tried X, didn't work" | re-discovery (what failed) | nurture-180d |
| 8 | too-expensive | "Pricing seems high / out of budget for value" | re-discovery (ROI anchor) + counter-position | nurture-60d + revenue-forecasting flag |
| 9 | too-small | "Not your target / too small for this" | feel-felt-found or honest disqualify | exit-permanent if sub-ICP; else nurture-90d |
| 10 | send-me-email | "Send me information at X@Y" | time-shift (confirm + send) | continue (one resource-only touch) |
| 11 | wrong-person | "Not the right person — talk to Y" | n/a (route to data-enrichment) | exit-globally on this recipient |
| 12 | compliance-security-blocker | "Can't onboard vendors without security review" | time-shift + supply security collateral | pause-with-resume; discovery-prep on resume |

## Framework-to-Objection Routing Rule

Each entry has a default framework. The skill MAY pick a different framework when context warrants. If match falls below 0.7 floor, do NOT pick a framework — surface as new-objection-pattern.

## New-Objection-Pattern Handling

When ≥3 unmatched objections accumulate within 30 days, emit a library-refresh recommendation with candidate pattern name and example replies. Library expansion is a versioned change.
