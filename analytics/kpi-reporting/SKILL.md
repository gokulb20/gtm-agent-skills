---
name: kpi-reporting
description: Produce a weekly GTM KPI report with north-star metric, leading + lagging indicators, what's-working/what's-not, WoW deltas, and recommended actions. Use when the user says "weekly GTM report", "board snapshot", "SDR metrics", or "what's working this week."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Analytics, KPI-Reporting, Weekly-Report, Metrics]
    related_skills: [campaign-management, pipeline-stages, revenue-forecasting, channel-performance, icp-refinement-loop]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# KPI Reporting

Produce the recurring GTM KPI report: north-star metric with trend, leading + lagging tables, per-channel summary, pipeline snapshot, what's-working/what's-not, WoW deltas + benchmarks, recommended actions. One screen (≤450 words top section); deeper data linked. Apple-MPP-aware: open rate excluded.

## When to Use

- Weekly GTM review — standard report
- Board update needs a snapshot
- SDR/AE coaching — activity vs outcome data
- Q3 retro — what worked, what didn't
- Something's off in pipeline — check the report
- User says "weekly GTM report" or "board snapshot"

## Quick Reference

| Concept | Value |
|---|---|
| North-star (default) | Pipeline-generated revenue (weighted pipeline added in window) |
| Leading metrics | Touches sent / meetings booked / replies / discovery completion rate |
| Lagging metrics | Closed-won revenue / deal count / win rate / forecast accuracy |
| Activity-vs-outcome pairing | Every leading metric paired with an outcome metric |
| WoW material-change flag | ±20% |
| Open rate exclusion | Appears only with "noisy metric" caveat; never as KPI |
| One-screen rule | ≤450 words top section; deeper data linked |

## Procedure

1. **Validate window + sources.** Pull data from functions 3/4/5/6 for the window. Flag freshness gaps. See `${HERMES_SKILL_DIR}/references/metric-definitions.md`.
2. **Compute north-star + trend.** Pipeline-generated revenue this period vs last vs 4-week avg. Express as: dollar + WoW % + 4w trend direction.
3. **Compute leading + lagging tables.** Each metric: value + WoW absolute + WoW % + trend + benchmark. Activity paired with outcome.
4. **Per-channel summary.** From channel-performance data: volume + reply/acceptance/connect rate + CPM trend.
5. **Pipeline snapshot.** From pipeline-stages: stage distribution + stuck deals + cycle times + win rate per tier.
6. **What's-working / what's-not.** 2–3 wins (improving WoW) + 2–3 concerns (degrading). Per finding: 1-line context + 1-line recommended action. See `${HERMES_SKILL_DIR}/references/report-template.md`.
7. **Recommended actions per finding.** Wins: "double down on X." Concerns: "investigate Y" with specific next step + named skill.
8. **Compose one-screen report.** ≤450 words top: north-star + tables + what's-working/not. Deeper linked.
9. **Push + deliver.** Full report as `interaction:research`. Deliver via Slack/email/Notion per config. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Open rate as KPI — Apple MPP noise; report only with explicit caveat
- Touches sent as success metric — pair with replies/meetings/deals
- One-screen → 12 pages — discipline matters; deeper data linked
- Cherry-picking what's working — always include what's-not
- Recommended actions vague — "improve email" → useless; "re-run data-enrichment for stale phones" → actionable
- Forecast accuracy not surfaced — surface MAPE periodically

## Verification

1. Every metric value traces to a source skill's run
2. Activity-vs-outcome pairing enforced
3. One-screen ≤450 words
4. What's-working + what's-not each have 2–3 items
5. Recommendations are specific (named action + named skill)
