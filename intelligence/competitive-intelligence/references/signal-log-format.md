# Signal Log Format

## Standard Fields

| Field | Format |
|---|---|
| Date | YYYY-MM-DD |
| Competitor | Name |
| Category | Product / Positioning / Pricing / etc. |
| Signal | One-line description |
| Strength (1–5) | Score |
| Decision-relevance (1–5) | Score |
| Total (S×R) | Computed |
| Source | URL or "internal" |
| Action taken | None / Card update / Positioning review / etc. |
| Owner | Who handled |

## Example Entries (fictional — WorkflowDoc)

| Date | Competitor | Category | Signal | S | R | Total | Source | Action | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 2026-04-22 | Guru | Capital | Raised $30M Series C | 5 | 4 | 20 | Crunchbase | Battle-card noted | Founder |
| 2026-04-15 | Guru | Product | Announced AI-native authoring product line | 5 | 5 | 25 | Press release | **Strategic event** — accelerate GTM | Founder |
| 2026-04-08 | Stonly | Hiring | Hiring AI/ML engineers | 4 | 4 | 16 | LinkedIn | Watch list intensified | Founder |
| 2026-04-02 | Stonly | Pricing | Pricing simplification | 3 | 3 | 9 | Wayback Machine | Weekly digest note | Contractor |
