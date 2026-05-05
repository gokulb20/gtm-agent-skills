---
name: channel-performance
description: Analyze per-channel performance and recommend budget reallocation using cost-per-meeting, cost-per-deal, marginal-CAC analysis, and Bullseye Framework refresh. Use when the user says "channel performance review", "which channel should get more budget", "compare channels", or "Bullseye refresh."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Analytics, Channel-Performance, Attribution, Budget-Allocation]
    related_skills: [channel-strategy, campaign-management, revenue-forecasting, kpi-reporting, icp-refinement-loop]
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

# Channel Performance

Analyze per-channel performance across 90+ days of data, compute cost-per-meeting + cost-per-deal, run marginal-CAC analysis, rank by ROI, and recommend budget reallocation. References Weinberg & Mares Bullseye Framework. Hard rule: never recommend reallocation on <90d data.

## When to Use

- Quarterly channel performance review
- Should we cut/invest in a specific channel
- Budget reallocation for next quarter
- Bullseye refresh — which channels haven't we tried
- User says "channel performance review" or "which channel gets more budget"

## Quick Reference

| Concept | Value |
|---|---|
| Min data per channel | 90d OR 50 meetings; below = refusal |
| CPM | (channel cost) / (meetings booked) |
| CPD | (channel cost) / (closed-won deals) |
| Attribution | Last-touch + multi-touch (first 30% / middle 40% / last 30%) — surface both |
| Marginal CAC | Next-dollar expected return; equimarginal principle (~19th-c) applied per MMM practice |
| Budget reallocation cap | 10–25% shift per quarter (no whiplash) |
| Open rate exclusion | Apple MPP noise; reply/meeting/deal rates only |

## Procedure

1. **Validate inputs.** Pull per-channel metrics ≥90d. Below threshold → flag and analyze others. See `${HERMES_SKILL_DIR}/references/attribution-methods.md`.
2. **Compute per-channel cost.** Tool subscription + per-touch credits + rep time × loaded cost × allocated share. See `${HERMES_SKILL_DIR}/references/cost-calculation.md`.
3. **Attribute closed deals.** Two methods: last-touch + multi-touch weighted. Surface both; don't pick one as truth.
4. **Compute CPM + CPD.** Per channel + per attribution method.
5. **Marginal CAC analysis.** Per channel: estimate next-dollar return based on diminishing-returns curve. Channel near-cap = high marginal CAC. See `${HERMES_SKILL_DIR}/references/marginal-cac.md`.
6. **ROI ranking + reallocation.** Rank by CPD and by marginal CAC. When rankings agree → strong recommendation. Disagree → nuanced. Recommend 10–25% shift.
7. **Bullseye refresh.** Reference Weinberg & Mares 19 channels. Flag never-tested ring-2 candidates. Per channel: estimated cost-to-test + expected return.
8. **Push to CRM.** Full report as `interaction:research`. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Cutting a channel after one bad month — require 90d+
- Last-touch as the truth — over-credits email; always show multi-touch
- Ignoring rep time cost — cold call is expensive when you cost hours
- Whiplash reallocation (50%+ in one quarter) — cap at 25%
- Open rate in channel comparison — Apple MPP noise
- Channels with small samples treated equally — surface uncertainty

## Verification

1. Every channel has ≥90d data OR is flagged insufficient
2. Cost computation includes rep time allocation
3. Both attribution methods surfaced
4. Rankings reproducible from the data
5. Reallocation recommendations sized within 10–25%
