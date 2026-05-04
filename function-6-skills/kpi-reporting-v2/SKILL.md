---
name: kpi-reporting
description: Produce a weekly (or biweekly / monthly) GTM KPI report — north-star + leading + lagging metrics across function-3 outreach + function-4 conversations + function-5 pipeline + function-6 ROI. Surfaces what's working, what's not, with WoW deltas + benchmark comparisons. Apple-MPP-aware (open rate excluded from primary metrics; reply / meeting / closed-won rates instead). Use for the standing weekly GTM review, when a board update needs a snapshot, when SDR/AE coaching needs activity-vs-outcome data, or when a campaign retro requires structured KPIs.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, optimization, kpi-reporting, weekly-report, function-6]
related_skills:
  - campaign-management
  - pipeline-stages
  - revenue-forecasting
  - channel-performance
  - icp-refinement-loop
  - conversation-intelligence
  - handoff-protocol
inputs_required:
  - reporting-window
  - source-data-from-functions-3-4-5-6
  - benchmark-data-historical-or-industry
  - delivery-channel-and-recipients
  - run-purpose-tag
deliverables:
  - weekly-or-monthly-kpi-report
  - north-star-metric-with-trend
  - leading-and-lagging-metric-tables
  - what-is-working-and-what-is-not-section
  - wow-deltas-and-benchmarks
  - recommended-actions-per-finding
  - kpi-report-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# KPI Reporting

Produce the recurring (weekly default) GTM KPI report: north-star metric with trend, leading + lagging metric tables, channel performance summary, pipeline state, what's-working / what's-not section, WoW deltas + benchmark comparisons, recommended actions per finding. One screen for the standing review; deeper details linked. Apple-MPP-aware: open rate excluded from primary metrics; reply / meeting / closed-won rates are the truth. Hard rule: any metric that can be gamed by activity inflation (touches sent without quality) is reported alongside an outcome metric (replies / meetings / deals).

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Weekly GTM reviews drown in numbers OR cherry-pick one metric to look good. This skill: produces the same report shape every week so trends are visible; uses leading + lagging metric framing so activity isn't confused with outcomes; flags what's-working AND what's-not (not just one); attaches a recommended action per finding. Goal: a 2-minute read founders + sales leaders use to make next week's decisions, not a 12-page deck nobody finishes.

## When to Use

- "Generate this week's GTM report."
- "Monthly pipeline + outreach review for the board."
- "SDR weekly 1:1 prep — give me activity + outcome data."
- "Q3 retro — what worked, what didn't?"
- "Something's off in the pipeline — what's the report say?"
- Recurring cadence (weekly / biweekly / monthly per `KPI_REPORT_CADENCE`).
- Triggered ad-hoc by founder / sales leader.

## Inputs Required

1. **Reporting window** — last 7d (weekly) / 14d (biweekly) / 30d (monthly).
2. **Source data from functions 3 / 4 / 5 / 6** — campaign metrics, pipeline state, forecast, channel performance, ICP refinement state, conversation intel patterns.
3. **Benchmark data** — historical (prior-period for WoW) + industry baselines (where available; 3% reply / 8% LI acceptance / 8% call connect / 15% meeting-to-deal).
4. **Delivery channel + recipients** — Slack / email / Notion / dashboard per `KPI_REPORT_CADENCE` config.
5. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **North-star metric (default)** | Pipeline-generated revenue (sum of weighted-pipeline added in window) — proxies near-term close-bound deal flow |
| **Leading metrics** (predict outcomes) | Touches sent / meetings booked / replies received / discovery completion rate |
| **Lagging metrics** (outcomes) | Closed-won revenue / closed-won deal count / closed-lost analysis / forecast accuracy |
| **Per-channel KPIs** | Reply rate (email) / acceptance rate (LI) / connect rate (call) / meeting-rate per channel |
| **Pipeline KPIs** | Stage distribution / stuck-deal count / cycle-time per stage / win-rate per tier |
| **Activity-vs-outcome pairing** | Every leading metric paired with an outcome — "we sent 800 touches" must be paired with "and got X replies / Y meetings" |
| **WoW delta convention** | Show absolute + % change; flag when ±20% (material) |
| **Benchmark comparison** | Compare to historical (last N weeks rolling avg) + industry; surface both |
| **Apple-MPP / open rate exclusion** | Open rate appears ONLY as an explicitly-noisy metric, never as a KPI |
| **Cadence default** | Weekly (`KPI_REPORT_CADENCE=weekly`); deliver Monday 9am report TZ |
| **One-screen rule** | Top section ≤450 words / single screen; deeper data linked |

## Procedure

### 1. Validate reporting window + sources
Pull data from functions 3 / 4 / 5 / 6 for the window. Confirm freshness. Insufficient data per source → flag explicitly (e.g., "channel-performance has only 3d in window" — surface with caveat).

### 2. Compute north-star metric + trend
Pipeline-generated revenue this window vs last window vs rolling 4-week avg. Express as: dollar amount + WoW % change + 4w-trend direction (up / flat / down).

### 3. Compute leading + lagging metric tables
- **Leading**: touches sent (per channel) / replies received / meetings booked / discovery completions.
- **Lagging**: closed-won revenue / closed-won deal count / win rate / forecast vs actual / cycle time per stage.
Each metric: this-period value + WoW absolute + WoW % + trend arrow + benchmark comparison.

### 4. Per-channel summary
Pull from `channel-performance` (per skill) + recent `campaign-management` decisions. Per channel: volume + reply/acceptance/connect rate + cost-per-meeting trend.

### 5. Pipeline state snapshot
Pull from `pipeline-stages`. Stage distribution (deal counts) + stuck-deal flags + cycle-time averages + win rate per tier.

### 6. What's-working / what's-not section
Identify 2–3 wins (metrics improving WoW with positive direction) + 2–3 concerns (metrics degrading or flagged by upstream skills). Per finding: 1-line context + 1-line recommended action.

### 7. Recommended actions per finding
- Wins: "double down on X" with specific tactic (e.g., scale variant B from successful A/B test).
- Concerns: "investigate Y" with specific next step (e.g., re-run `data-enrichment` for stale-email cluster surfaced).

### 8. Compose one-screen report
Top section ≤450 words: north-star + leading-metric table + lagging-metric table + what's-working / what's-not. Deeper details linked (per-channel detail / pipeline detail / forecast detail).

### 9. Push to CRM + deliver
Per conventions: full report as `interaction:research`. Deliver via configured channel (Slack webhook / email / Notion / dashboard).

## Output Format

- North-star metric with trend (this week / last week / 4w avg)
- Leading metrics table (touches / replies / meetings / discovery completions per channel)
- Lagging metrics table (closed-won revenue + count / win rate / forecast accuracy)
- Per-channel summary (reply / acceptance / connect rates + cost-per-meeting trend)
- Pipeline state snapshot (stage distribution + stuck-deal flags + cycle times + win rate per tier)
- What's-working (2–3 wins) + What's-not (2–3 concerns) sections with recommended actions
- One-screen report (≤450 words top); deeper data linked
- Recommended next skill per concern flagged

## Done Criteria

1. Reporting window validated; data freshness confirmed per source.
2. North-star metric + trend computed.
3. Leading + lagging metrics computed; activity-vs-outcome pairing enforced.
4. Per-channel + pipeline state snapshots pulled.
5. What's-working + what's-not sections each have 2–3 items with recommended actions.
6. One-screen report ≤450 words; deeper data linked.
7. Push to CRM emitted; delivered via configured channel.

## Pitfalls

- **Open rate as KPI.** Apple MPP made it noise; report only with explicit "noisy metric" caveat.
- **Touches sent as a success metric.** Activity inflation looks great until you check replies / meetings / deals. Always pair.
- **One-screen → 12 pages.** Discipline matters; deeper data linked, not embedded.
- **WoW comparisons only.** Single-week comparisons are noisy; surface 4w trend AND industry benchmark.
- **Cherry-picking what's working.** Always include what's-not; founder wants both.
- **Recommended actions vague.** "Improve email" → useless. "Re-run data-enrichment for the 23 stale-email cluster surfaced last week" → actionable.
- **Per-channel comparison without normalization.** Email volume is 10x LinkedIn; raw reply count favors email; rates favor neither. Show rates.
- **Pipeline snapshot without context.** "47 deals in pipeline" needs prior-period comparison + cycle-time trend.
- **Closed-won deal count without revenue context.** 5 small deals ≠ 1 big deal; report both.
- **Forecast accuracy not surfaced.** Hidden in `revenue-forecasting`; surface MAPE periodically.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (metric values, dates, channel labels, recommendations) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Metric values are `[verified: <function-skill>:run_<id>]`; never invent numbers.
- **Not coordinating with `channel-performance` cadence.** Channel-performance is quarterly; KPI report is weekly. Don't duplicate analysis; reference.

## Verification

Report is real when: every metric value traces to a source skill's run; activity-vs-outcome pairing enforced; one-screen ≤450 words; what's-working + what's-not each have 2–3 items; recommendations are specific (named action + named skill); WoW deltas + 4w trend + benchmark all present. Negative test: read the report aloud in 2 minutes — does the listener leave knowing what to do this week? If no, the recommendations are too vague.

## Example

**User prompt:** "Generate this week's GTM report."
**What should happen:** Pull last-7d data. North-star: $42K pipeline added this week (up 18% WoW; up 11% vs 4w avg). Leading: 800 email touches sent → 32 replies (4% rate, on baseline) → 8 meetings booked (25% reply-to-meeting); 60 LI connects → 11 accepted (18% acceptance, above 12% floor) → 4 meetings; 50 calls → 6 connects → 2 meetings (slow week on calls — 4% connect rate vs 8% target). Lagging: 3 closed-won at $34K total revenue this week; win rate per Tier-1 12% (down from 18% last quarter — flag). Pipeline: 47 active deals; 1 stuck (78d in Proposal — flagged by `pipeline-stages`); cycle-time Discovery → Proposal averaging 32d (up from 28d).

What's working:
- Email reply rate at baseline despite +20% volume — copy held quality.
- LI acceptance 18% well above 12% floor — Vision-opener variant from A/B test shipping well.

What's-not:
- Call connect 4% vs 8% target — diagnose: phone-status freshness aging? Re-run `data-enrichment` for phone re-verify on the active call list.
- Tier-1 win rate dropped 6pp → recommend `icp-refinement-loop` if pattern persists 1 more week.

Recommended actions: (1) `data-enrichment` phone re-verify run for active call list; (2) monitor Tier-1 win rate next week — if still <15%, trigger `icp-refinement-loop`.

Push report. Delivered via Slack. ≤450 words top section.

**User prompt:** "Monthly board snapshot."
**What should happen:** Same shape as weekly but 30d window. Add: closed-won YTD vs goal; pipeline coverage ratio (3x quarter target = healthy); top-3 deals by weighted-contribution to next 90d forecast. Leading-vs-lagging trend over 4 prior months for context. Recommended actions phrased at strategic level (not tactical) — "double down on LinkedIn channel" not "fix the call list".

**User prompt:** "SDR weekly 1:1 prep — Will's metrics."
**What should happen:** Per-rep slice of weekly report. Will's activity (touches sent across channels) + outcomes (replies / meetings / handoff acceptance / handoff rejection rate). Coaching recommendations: high handoff-rejection rate suggests rep is shipping low-quality SAL packages (route to `handoff-protocol` SDR-coaching loop).

## Linked Skills

- Campaign metrics → `campaign-management`; pipeline state → `pipeline-stages`; forecast → `revenue-forecasting`
- Channel performance details → `channel-performance`; ICP refinement triggers → `icp-refinement-loop`
- Conversation patterns → `conversation-intelligence`; customer feedback themes → `customer-feedback-analysis`
- SDR-AE coaching loop → `handoff-protocol` rejection-rate KPIs

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-6-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Weekly KPI report (recurring artifact) | `interaction` (type: `research`) | `relevance` = full one-screen report (≤450 words top + linked details); `tags: "#kpi-report #report-<cadence> #function-6"` |
| What's-working / what's-not finding | `interaction` (type: `research`) | `relevance` = finding + 1-line context + recommended action + linked skill; `tags: "#kpi-finding #function-6"` |
| Per-rep coaching slice | `interaction` (type: `research`) | `relevance` = rep-specific activity + outcomes + coaching recommendation; `tags: "#kpi-rep-coaching #function-6"` |
| Recommended action triggered | `interaction` (type: `research`) | `relevance` = action triggered + downstream skill called + parameters; `tags: "#kpi-action-triggered #function-6"` |
| `[unverified — needs check]` (data freshness gap) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #kpi-reporting"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
KPI_REPORT_CADENCE=weekly
KPI_REPORT_DELIVERY_DAY=monday
KPI_REPORT_TZ=America/Los_Angeles
SLACK_WEBHOOK_URL=     # or NOTION_API_KEY / GOOGLE_SHEETS_API_KEY for delivery
```

### Source tag

`source: "skill:kpi-reporting:v2.0.0"`

### Example push (weekly report)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#kpi-report #report-weekly #function-6",
    "relevance": "GTM weekly report 2026-06-01 (week 22). North-star: $42K pipeline added (+18% WoW, +11% vs 4w avg). Leading: 800 email touches → 32 replies (4%, baseline) → 8 meetings (25% reply-to-mtg); 60 LI connects → 11 accepted (18%) → 4 meetings; 50 calls → 6 connects (4%, below 8% target — flag) → 2 meetings. Lagging: 3 closed-won @ $34K; Tier-1 win rate 12% (down 6pp vs last Q — flag). Pipeline: 47 active / 1 stuck (78d in Proposal). Cycle Discovery→Proposal 32d (up from 28d). Working: email copy held quality at +20% volume; LI Vision-opener variant 18% well above 12% floor. Not working: call connect 4% (re-verify phones via data-enrichment); Tier-1 win drop (monitor; if persists trigger icp-refinement-loop). Actions: (1) data-enrichment phone re-verify; (2) Tier-1 monitor.",
    "source": "skill:kpi-reporting:v2.0.0"
  }'
```

### Example push (action triggered)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#kpi-action-triggered #function-6",
    "relevance": "KPI weekly report finding triggered action: data-enrichment phone re-verify run scheduled for active call list (60 phone numbers, last verified 90+ days ago). Triggered by call connect rate 4% (below 8% target). Linked: phone-status freshness audit feeding cold-calling capacity for next sprint.",
    "source": "skill:kpi-reporting:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[verified: <source-skill>:run_<id>]` (metric values from upstream skill runs) | Standard mapping. |
| `[unverified — needs check]` (data freshness gap; one source skill stale) | Pushes ONLY as `interaction:research` with `#unverified #review-required #kpi-reporting` tags; report flagged partial. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Reporting window has zero activity (no campaigns ran) — push minimal report with `#zero-activity` tag; still recurring artifact for trend continuity.
- Source data unavailable for >50% of metrics — push `#data-unavailable` partial report; recommend running source skills first.
- Already pushed within last 24h on same window (dedup) — push dedup notice only.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
