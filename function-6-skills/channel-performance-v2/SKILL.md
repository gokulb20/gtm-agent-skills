---
name: channel-performance
description: Analyze per-channel performance across email / LinkedIn / cold call / web-sourcing-driven channels and recommend budget / effort reallocation. Computes cost-per-meeting and cost-per-deal per channel, applies marginal-CAC analysis (standard microeconomics — the equimarginal principle, ~19th-century — applied per modern Marketing Mix Modeling practice), references Bullseye Framework (Weinberg & Mares — already used by `channel-strategy` in function-1) for refresh recommendations. Use when ≥2 channels have run for 90+ days, when per-channel ROI is unclear, when budget reallocation is being considered, or when a previously-promising channel has plateaued and needs re-evaluation.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, optimization, channel-performance, attribution, function-6]
related_skills:
  - channel-strategy
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - lead-sourcing-web
  - multi-channel-cadence
  - campaign-management
  - revenue-forecasting
  - kpi-reporting
inputs_required:
  - per-channel-campaign-metrics-90d-plus
  - per-channel-cost-data
  - closed-deal-attribution-data
  - current-channel-budget-allocation
  - run-purpose-tag
deliverables:
  - per-channel-cost-per-meeting-and-cost-per-deal
  - marginal-cac-analysis
  - channel-roi-ranking
  - budget-reallocation-recommendations
  - bullseye-framework-refresh
  - channel-performance-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Channel Performance

Analyze per-channel performance (email / LinkedIn / cold call / web-sourced) across 90+ days of campaign data, compute cost-per-meeting + cost-per-deal per channel, run marginal-CAC analysis, rank channels by ROI, and recommend budget / effort reallocation. References Weinberg & Mares Bullseye Framework (already used by function-1 `channel-strategy`) for refresh-worthy channels. Hard rule: never recommend reallocation on <90d data per channel — early signals are noise.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

GTM teams over-invest in the channel that worked first and under-invest in channels they never tried properly. This skill: pulls per-channel metrics across enough time to be honest (90d minimum), computes cost-per-meeting + cost-per-deal honestly (allocating shared costs proportionally), applies marginal-CAC reasoning (next dollar's expected return), recommends reallocation with explicit risk flags. Goal: budget allocation decisions backed by data rather than founder narrative.

## When to Use

- "Quarterly channel performance review."
- "Email is winning — should we cut LinkedIn?"
- "Cold call cost-per-meeting is high — is it worth keeping?"
- "Budget reallocation for next quarter — which channel deserves more?"
- "Bullseye refresh — which 19 channels haven't we tried?"
- Quarterly cadence default.
- Triggered by `revenue-forecasting` accuracy audit suggesting channel-mix shift.

## Inputs Required

1. **Per-channel campaign metrics 90d+** — from `campaign-management` history. Per channel: touches sent, replies, meetings booked, deals closed.
2. **Per-channel cost data** — tool subscriptions (Smartlead, HeyReach, JustCall, etc.) + per-touch credit costs + rep time allocation (estimated hours × loaded rep cost).
3. **Closed-deal attribution data** — per closed deal, which channels touched the contact + when. Default attribution: last-touch (simple) + multi-touch (weighted).
4. **Current channel budget allocation** — dollar / time spend per channel.
5. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Min-data-per-channel floor** | 90 days OR 50 meetings booked (whichever earlier). Below = insufficient signal; refusal. |
| **Cost-per-meeting (CPM)** | (channel cost in window) / (meetings booked attributed to channel) |
| **Cost-per-deal (CPD)** | (channel cost in window) / (closed-won deals attributed to channel) |
| **Attribution methods** | Last-touch (simple, often biased toward email) + multi-touch (weighted by touch position; first 30% / middle 40% / last 30%) — surface BOTH |
| **Marginal CAC** | Expected cost of acquiring the next deal at current spend level — compares to channel's diminishing-returns curve. Standard microeconomics (the **equimarginal principle**, ~19th-century); applied per modern **Marketing Mix Modeling (MMM)** practice. *Aaron Ross popularized SDR/AE specialization; Mark Roberge popularized engineering-rigor-in-sales-process — neither owns marginal-CAC.* |
| **ROI ranking** | Sort channels by CPD ascending (lower CPD = better) AND by marginal-CAC. The two lists may disagree — surface both. |
| **Budget reallocation rule** | Recommend shifting 10–25% of budget per quarter (avoid whiplash). Smaller shifts on weaker signals; larger on convergent (CPD + marginal-CAC + reply-rate-trend all aligned). |
| **Bullseye refresh** | Reference Weinberg & Mares 19 channels (used by `channel-strategy`); flag any never-tested channels worth ring-2 experiment. |
| **Apple-MPP-aware** | Open rate excluded from any channel comparison; reply / meeting / closed-deal rates only |
| **Time-cost allocation** | Rep time included in channel cost (not just tool subscription); "free" labor is real cost |

## Procedure

### 1. Validate inputs
Pull per-channel metrics ≥90d for all channels under analysis. Below threshold per channel → flag and analyze others; surface insufficient-data channels separately.

### 2. Compute per-channel cost
Tool subscription + per-touch credit cost + rep time allocation × loaded rep cost. Allocate shared costs (sender pool maintenance, infrastructure setup amortization) proportionally.

### 3. Attribute closed deals to channels
Two methods:
- **Last-touch attribution**: deal credited to channel of the last touch before reply / meeting.
- **Multi-touch attribution**: deal credited to all touching channels weighted by position (first 30% / middle 40% / last 30%).
Surface both. Don't pick one as truth — they show different things.

### 4. Compute CPM + CPD per channel
Per channel: cost / meetings booked = CPM; cost / closed deals = CPD. Use both attribution methods.

### 5. Marginal CAC analysis
For each channel: estimate next-dollar return based on current diminishing-returns curve. A channel running near-cap (LinkedIn at 80/week) has higher marginal CAC than one with headroom. Surface marginal-CAC ranking alongside CPD ranking.

### 6. ROI ranking + reallocation recommendations
Rank channels by CPD (lower = better) and marginal CAC (lower = better). When rankings agree → strong recommendation. When they disagree (e.g., low CPD but maxed marginal — channel is great but capped) → nuanced recommendation. Recommend budget shift 10–25% per quarter (no whiplash).

### 7. Bullseye Framework refresh
Reference the 19 Weinberg & Mares channels via `channel-strategy` artifact. Flag channels never-tested OR ring-2 candidates for experiment. Per channel: estimated cost-to-test + expected return.

### 8. Push to CRM + emit performance record
Per conventions: full report as `interaction:research` with rankings + recommendations + Bullseye refresh. Recurring artifact.

## Output Format

- Per-channel CPM + CPD (both attribution methods)
- Per-channel marginal-CAC estimate
- ROI ranking by CPD + by marginal CAC (two lists; explicit when they disagree)
- Budget reallocation recommendations (10–25% shift per quarter; risk-flagged)
- Bullseye Framework refresh: never-tested channels worth ring-2 test
- Per-channel time-trend (improving / stable / degrading over 90d)
- Run record + recommended next skill

## Done Criteria

1. Min-data threshold validated per channel (90d / 50 meetings).
2. Per-channel cost computed including rep time allocation.
3. Closed-deal attribution computed via last-touch AND multi-touch methods.
4. CPM + CPD computed per channel + per attribution method.
5. Marginal-CAC analysis surfaced.
6. ROI ranking surfaced (two lists when methods disagree).
7. Budget reallocation recommendations sized 10–25% with risk flags.
8. Bullseye refresh suggestions for never-tested ring-2 channels.
9. Push to CRM emitted; recurring artifact preserved for trend analysis.

## Pitfalls

- **Cutting a channel after one bad month.** Channels are noisy short-term; require 90d+ before reallocating.
- **Last-touch attribution as the truth.** Multi-channel cadences mean last-touch over-credits the cheapest channel (usually email); always show multi-touch alongside.
- **Ignoring rep time cost.** Cold calling looks cheap until you cost rep hours at $80–150 loaded; CPM often higher than email despite lower tool spend.
- **Recommending whiplash reallocation (50%+ in one quarter).** Channels need ramp time to remobilize; cap shifts at 25%.
- **Bullseye refresh suggesting channels with no infrastructure.** Adding a new channel costs setup time; surface that cost honestly.
- **Open rate in channel comparison.** Apple MPP made it noise.
- **Channels with small sample sizes treated equally.** A channel with 3 deals' attribution can't be compared rigorously to one with 30 deals; surface uncertainty.
- **Marginal-CAC ignored.** A channel at-cap has high marginal CAC even if average CPD is low; don't double-down on a saturated channel.
- **Time-trend hidden.** A channel with declining performance over 90d behaves differently from one stable; surface the trend.
- **Confounded by audience differences.** Email run on Tier-1 vs cold call run on Tier-2 → different audiences = different baselines. Note when channel-audience confound exists.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (channels, costs, attribution numbers, dates, recommendations) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Cost data is `[user-provided]`; attribution is `[verified: campaign-management:run_<id>]` per run; never invent numbers.
- **Not coordinating with `channel-strategy`.** Function-1's `channel-strategy` is the canonical channel-bet artifact; refresh recommendations propagate back there.

## Verification

Report is real when: every channel has ≥90d data OR is flagged insufficient; cost computation includes rep time allocation; both attribution methods surfaced; rankings reproducible from the data; reallocation recommendations sized within 10–25% range and risk-flagged; Bullseye refresh references actual function-1 channel-strategy artifact. Negative test: pick 3 random recommendations; trace to supporting data + cost calc — if any "recommendation" lacks per-channel evidence, analysis broke.

## Example

**User prompt:** "Quarterly channel performance review."
**What should happen:** Pull per-channel metrics 90d. Numbers below are `[hypothetical]` — agent reads vendor docs at runtime; pricing changes — verify live before any spend. Email: 1,200 sends / 48 meetings / 12 deals @ ~$1,800 cost `[hypothetical]` (Smartlead subscription `[user-provided]` $200 + 60 rep hrs × $100/hr loaded × 0.27 share). LinkedIn: 320 connects / 24 meetings / 6 deals @ ~$1,400 `[hypothetical]` (HeyReach subscription `[user-provided]` $150 + 30 rep hrs × $100/hr × 0.42 share). Cold call: 850 dials / 18 meetings / 5 deals @ ~$2,400 `[hypothetical]` (JustCall subscription `[user-provided]` $300 + 30 rep hrs × $100/hr × 0.70 share).

CPM: Email $37.50 / LinkedIn $58.33 / Call $133.33.
CPD (last-touch): Email $150 / LinkedIn $233 / Call $480.
CPD (multi-touch): Email $135 / LinkedIn $250 / Call $420 (call gets credit for setting up the close that emails finish).

Marginal CAC: Email approaching domain cap (high marginal); LinkedIn at 40% of cap (low marginal); Call has rep-hour ceiling.

Ranking: by CPD email > LinkedIn > call. By marginal CAC LinkedIn > email > call.

Recommendation: Shift 15% of email budget to LinkedIn over Q3 (LinkedIn has headroom + lower marginal CAC); call stays flat (high CPD but only channel for Tier-1 SAL voice contact). Bullseye refresh: web-sourced (never tried at scale) worth ring-2 test for trigger-rich plays.

**User prompt:** "Should we cut cold calling?"
**What should happen:** Targeted analysis on call channel. Last-touch CPD $480 looks high. Multi-touch CPD $420 with call as middle-touch in 7 of those 5 deals — call is doing setup work email finishes. Verdict: don't cut; reduce volume 20% to focus on Tier-1 SAL prospects only (where call has 12% connect rate vs Tier-2 at 4%). Tighter targeting > complete cut.

**User prompt:** "We've only run email for 30 days — analyze."
**What should happen:** Refusal: 30d below 90d minimum. Run partial diagnostic: surface current trends (improving / stable / degrading) but explicitly NOT a performance verdict. Recommendation: collect 60+ more days before reallocation decision.

## Linked Skills

- Per-channel campaign metrics from → `campaign-management`
- Bullseye Framework + channel-bet artifact → `channel-strategy` (function-1)
- Refinement recommendations propagate back to → `channel-strategy` (function-1) for canonical artifact update
- Closed-deal attribution from → `pipeline-stages` (function-5)
- Cost-per-deal feeds → `revenue-forecasting` ACV reality-check
- ROI patterns inform → `kpi-reporting` weekly reports
- Per-tier channel performance → `icp-refinement-loop` (function-6)

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-6-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Channel performance report | `interaction` (type: `research`) | `relevance` = full report (per-channel CPM/CPD + attribution methods + marginal-CAC + ROI ranking + reallocation + Bullseye refresh); `tags: "#channel-performance #function-6"` |
| Per-channel attribution detail | `interaction` (type: `research`) | `relevance` = per-channel last-touch + multi-touch breakdown; `tags: "#channel-attribution #function-6"` |
| Reallocation recommendation | `interaction` (type: `research`) | `relevance` = source-channel + target-channel + shift amount + risk flag + projected impact; `tags: "#channel-reallocation #function-6"` |
| Bullseye refresh recommendation | `interaction` (type: `research`) | `relevance` = never-tested channel + estimated test cost + expected return; `tags: "#bullseye-refresh #function-6"` |
| `[unverified — needs check]` (insufficient data per channel) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #channel-performance"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
# No external API beyond reading campaign-management metrics from the CRM
```

### Source tag

`source: "skill:channel-performance:v2.0.0"`

### Example push (quarterly review)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#channel-performance #function-6",
    "relevance": "Q2 channel performance review (90d window 2026-04-01 to 2026-06-30). Email: CPM $37.50 / CPD last-touch $150 / multi-touch $135 / marginal CAC: high (near domain cap). LinkedIn: CPM $58.33 / CPD last-touch $233 / multi-touch $250 / marginal CAC: low (at 40% of weekly cap). Call: CPM $133.33 / CPD last-touch $480 / multi-touch $420 / call as middle-touch setup in 7/5 deals. Ranking by CPD: email > LinkedIn > call. By marginal CAC: LinkedIn > email > call. Recommendation: shift 15% of email budget to LinkedIn (has headroom + lower marginal CAC); call stays flat with tighter Tier-1 SAL focus. Bullseye refresh: web-sourced (never tested at scale) worth ring-2 trigger play.",
    "source": "skill:channel-performance:v2.0.0"
  }'
```

### Example push (insufficient data)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #channel-performance",
    "relevance": "Channel performance analysis REFUSED for partial verdict. Email channel has 30d data (below 90d minimum); LinkedIn + call meet threshold. Partial diagnostic: email reply-rate trend improving over 30d; verdict deferred to 90d. Other channels analyzed normally; recommendation withheld until email data matures.",
    "source": "skill:channel-performance:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[verified: campaign-management:run_<id>]` (metrics) + `[user-provided]` (cost data) | Standard mapping. |
| `[unverified — needs check]` (insufficient data per channel OR cost data missing) | Pushes ONLY as `interaction:research` with `#unverified #review-required #channel-performance` tags; reallocation recommendations deferred. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- All channels below 90d data threshold — push refusal record; no recommendations.
- Cost data unavailable for active channels — push partial report with `#cost-data-missing`; recommendations omitted.
- Single-channel program (only email running) — push run record with `#single-channel-no-comparison`; recommend running ring-2 channel test before reallocation analysis is meaningful.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
