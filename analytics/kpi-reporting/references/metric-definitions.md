# Metric Definitions — KPI Reporting

## North-Star Metric

**Pipeline-generated revenue** — sum of weighted-pipeline added in the reporting window. Proxies near-term close-bound deal flow.

## Leading Metrics (predict outcomes)

| Metric | Source | Calculation |
|---|---|---|
| Touches sent | campaign-management (f3) | Count of outbound touches in window, per channel |
| Meetings booked | pipeline-stages (f5) | Count of meetings scheduled in window |
| Replies received | reply-classification (f4) | Count of classified replies in window |
| Discovery completion rate | pipeline-stages (f5) | % of Meeting-stage deals that completed discovery |

## Lagging Metrics (outcomes)

| Metric | Source | Calculation |
|---|---|---|
| Closed-won revenue | pipeline-stages (f5) | Sum of deal values closed in window |
| Closed-won deal count | pipeline-stages (f5) | Count of deals closed in window |
| Win rate per tier | pipeline-stages (f5) | % of deals closed-won by ICP tier |
| Forecast accuracy | revenue-forecasting (f5) | MAPE of most recent forecast vs actuals |

## Per-Channel KPIs

| Metric | Channel | Source |
|---|---|---|
| Reply rate | Email | campaign-management |
| Acceptance rate | LinkedIn | linkedin-outreach |
| Connect rate | Cold call | cold-calling |
| Meeting rate per channel | All | pipeline-stages |

## Activity-vs-Outcome Pairing

Every leading metric MUST be reported alongside its outcome:
- "800 touches sent" → "AND got 32 replies (4%) and 8 meetings (25% reply-to-meeting)"
- "60 LI connects" → "AND 11 accepted (18%) and 4 meetings"

## WoW Delta Convention

- Show absolute + % change
- Flag when ±20% (material)
- Surface 4-week trend AND industry benchmark
