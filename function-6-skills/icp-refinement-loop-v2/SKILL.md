---
name: icp-refinement-loop
description: Refine the ICP scorecard from `icp-definition` after ≥30 closed deals using actual won/lost patterns — recompute tier cutoffs, re-tune dimension weights, surface segment shifts, and propose ICP delta with evidence. Hard rule: never refine ICP with <30 closed deals (insufficient evidence). Use when ≥30 deals have closed since last refinement, when forecast accuracy audits show systemic over/under-prediction by segment, when win rate by tier doesn't match scorecard predictions, or when the team needs an explicit "what changed about who we win" report.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, optimization, icp-refinement, learning-loop, function-6]
related_skills:
  - icp-definition
  - lead-scoring
  - pipeline-stages
  - revenue-forecasting
  - competitive-intelligence
  - conversation-intelligence
  - kpi-reporting
  - customer-feedback-analysis
inputs_required:
  - closed-won-and-closed-lost-records-min-30
  - current-icp-scorecard-and-tier-cutoffs
  - lost-reasons-from-pipeline-stages
  - segment-tags-on-deals
  - run-purpose-tag
deliverables:
  - icp-delta-recommendations-with-evidence
  - tier-cutoff-recalibration
  - dimension-weight-re-tuning-suggestions
  - segment-shift-report
  - retroactive-rescoring-proposal-when-applicable
  - icp-refinement-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# ICP Refinement Loop

Periodically refine the ICP scorecard from `icp-definition` using actual won/lost patterns from ≥30 closed deals. Recomputes tier cutoffs (do won deals score where the rubric says they should?), re-tunes dimension weights (which dimensions actually predict close?), surfaces segment shifts (are we winning more in adjacent verticals than the original ICP captures?). Hard rule: refusal to refine ICP with <30 closes (insufficient signal). Recommendations propagate back to `icp-definition` (rubric update) and `lead-scoring` (re-tier the active pipeline).

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

The ICP defined at quarter 1 with 0 customers is a hypothesis. The ICP refined at quarter 4 with 50 customers is grounded. Between the two, founders often ride the original hypothesis longer than the data supports. This skill: pulls won/lost record patterns, runs the original scorecard against actuals, surfaces where rubric vs reality diverge, recommends targeted updates (don't rewrite the ICP — refine cutoffs, weights, or add a sub-segment). Goal: an ICP that actually predicts who you win, refreshed quarterly without over-rewriting.

## When to Use

- "Quarterly ICP refinement — we have 47 closed deals since last refresh."
- "Forecast accuracy audit shows systemic over-prediction in Tier-2 — re-tune."
- "Win rate by Tier doesn't match scorecard (Tier-1 winning 40%; rubric predicted 60%)."
- "We've expanded into Healthcare segment — does the ICP capture this?"
- "Lost-to-Guru rate is 40% in Series B — does ICP need an anti-ICP boundary update?"
- Quarterly cadence default (`ICP_REFINEMENT_AUDIT_QUARTERLY=true`).
- Triggered when `revenue-forecasting` accuracy audit shows systemic miscalibration.

## Inputs Required

1. **Closed-won + closed-lost records** — minimum 30 closes (won + lost combined) per `ICP_REFINEMENT_MIN_CLOSED_DEALS=30`.
2. **Current ICP scorecard + tier cutoffs** from `icp-definition`.
3. **Lost reasons** from `pipeline-stages` (`no-budget` / `no-authority` / `no-need` / `no-timing` / `lost-to-competitor` / `unresponsive`).
4. **Segment tags on deals** — vertical / size band / geography / stage.
5. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Min-closes hard floor** | 30 (won + lost combined). Below = refusal; insufficient signal. |
| **Audit cadence** | Quarterly default; on-demand for forecast-accuracy-driven runs |
| **Refinement scope** | (a) tier cutoff recalibration · (b) dimension weight re-tuning · (c) segment shift detection · (d) anti-ICP boundary update · (e) trigger-library refresh |
| **Tier cutoff rule** | If won deals score <T1-cutoff → cutoff too high; if Anti-ICP deals win occasionally → boundary too narrow |
| **Dimension re-tuning** | Compute correlation between each dimension's score and `closed_won` outcome; dimensions with low correlation get weight reduced; high correlation get weight increased. Total stays 100. |
| **Segment shift detection** | If wins concentrate in a segment not captured by the original firmographic, recommend new sub-segment |
| **Won-but-low-score (anti-ICP miss)** | Wins scoring <55 in original rubric flag the rubric as missing something; deep-dive recommended |
| **Lost-but-high-score (Tier-1 miss)** | Tier-1 deals losing flag the rubric as over-confident; investigate lost-reason patterns |
| **Retroactive rescoring** | After refinement, re-score the active pipeline using new rubric; surface tier shifts |
| **Confidence rubric upgrade** | Old rubric was "Hypothesis"; with 30+ closes, new rubric tier is "Medium" or "High" per `icp-definition` confidence rubric |

## Procedure

### 1. Validate inputs
Pull closed deals; confirm n ≥30. Below threshold → refusal with explanation; recommend running `lead-scoring` retroactively against won deals as a stopgap.

### 2. Score won/lost deals against current rubric
Apply the original `icp-definition` rubric to each closed deal as it was at the time of close. Generate per-deal scores. Compute distribution.

### 3. Tier cutoff calibration
- Won deals scoring <T1-cutoff: how many? If >25% of wins score below T1-cutoff → cutoff too high; recommend lowering.
- Won deals scoring <T3-cutoff (Anti-ICP territory): if any → rubric is rejecting deals you actually win; deep dive on these.
- Lost deals scoring ≥T1-cutoff: if >25% of losses score Tier-1 → cutoff too low (overconfident).

### 4. Dimension weight re-tuning
Per dimension (Pain / Trigger / WTP / Reach / TTV / Strategic): compute correlation between dimension score and `closed_won` outcome. Recommend weight adjustments preserving total 100. E.g., if Trigger correlates highly with wins (signal it predicts close), increase weight; if Strategic correlates near-zero, reduce.

### 5. Segment shift detection
Group wins by firmographic segment. If a segment not in original ICP captures significant share (e.g., 30% of wins in Healthcare when original ICP is SaaS-only), surface as new-segment recommendation.

### 6. Lost-reason pattern aggregation
Aggregate lost reasons by tier + segment. Patterns: lost-to-competitor by competitor name (feeds `competitive-intelligence`); no-budget by deal-size band (feeds `revenue-forecasting` ACV recalibration); no-need by segment (signal that ICP is over-broad in that segment).

### 7. Compose ICP delta recommendations
Rank by impact: (a) cutoff recalibrations / (b) weight re-tunings / (c) segment additions or anti-ICP boundary updates / (d) trigger library refresh from won-deal patterns. Each recommendation: evidence (deal counts + win rates) + proposed change + estimated impact.

### 8. Retroactive rescoring proposal
Compute: if we apply the new rubric to the active pipeline, how do tiers shift? Surface counts (e.g., "12 deals would move from Tier-2 to Tier-1; 8 from Tier-1 to Tier-2"). Don't auto-apply; user authorizes.

### 9. Push to CRM + emit refinement record
Per conventions: refinement report as `interaction:research`. Recommendations queued; user authorizes which to apply. On user approval: route updates to `icp-definition` (rubric file update) + `lead-scoring` (re-score active pipeline).

## Output Format

- ICP delta recommendations ranked by impact: cutoff recalibration / weight re-tuning / segment addition / anti-ICP boundary / trigger library refresh
- Per-recommendation: evidence (deal counts, win rates, distributions) + proposed change + estimated impact
- Retroactive rescoring proposal: tier-shift counts in active pipeline
- Confidence rubric upgrade (Hypothesis → Medium/High based on n)
- Lost-reason patterns + downstream routing
- Run record + recommended next skill

## Done Criteria

1. Min-closes threshold validated (≥30); refusal if below.
2. Won/lost deals scored against original rubric; distributions computed.
3. Tier cutoff calibration analyzed; recommendations surfaced if mis-calibrated.
4. Dimension weight re-tuning analyzed; correlation per dimension surfaced.
5. Segment shifts detected; new-segment recommendations surfaced.
6. Lost-reason patterns aggregated; routed to relevant downstream (competitive-intelligence, revenue-forecasting).
7. Retroactive rescoring proposal computed.
8. Confidence rubric upgrade documented.
9. Push to CRM emitted; user authorization queue surfaced.

## Pitfalls

- **Refining ICP with <30 closes.** Insufficient signal; refusal is the right move.
- **Auto-applying ICP changes.** Always require user authorization; ICP is a strategic artifact.
- **Re-tuning weights to overfit recent wins.** A good rubric generalizes; don't optimize the rubric to perfectly predict the last 30 deals at the expense of generalizability.
- **Adding new segments on n=2.** "We won two Healthcare deals; we're now a Healthcare ICP" — not yet. New segment requires n≥10 wins in segment.
- **Ignoring lost-deal patterns.** Wins teach which prospects to pursue; losses teach which to avoid. Both inform the ICP.
- **Tier-shift cascade not surfaced.** Updating cutoffs shifts tiers across the active pipeline — surface counts so user knows the operational consequence.
- **Confidence rubric not updated.** Going from Hypothesis to Medium based on 35 closes is a real upgrade; document it.
- **Not feeding lost-to-competitor to `competitive-intelligence`.** Free signal for competitive priority.
- **Re-running too often.** Quarterly minimum; more frequent = noise + ICP whiplash that confuses the team.
- **Not coordinating with positioning.** ICP shifts often imply positioning shifts; flag for `positioning-strategy` review.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (deals, segments, win rates, lost-reasons, recommendation evidence) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Recommendations cite actual deal counts + IDs; never invent evidence.
- **Treating refinement as one-shot.** It's a loop; document this run + schedule the next.

## Verification

Refinement is real when: min-closes threshold honored; per-deal scores reproducible from input data + original rubric; recommendations cite actual deal counts (sample-check 5 random); retroactive-rescoring proposal numbers add up to active pipeline count; lost-reason routing happened; user authorization queue surfaced before any rubric / scorecard update applied. Negative test: pick 3 random recommendations; trace each to the supporting deal evidence — if any "recommendation" lacks deal-count backing, refinement logic broke.

## Example

**User prompt:** "Quarterly ICP refinement — 47 closed deals since last refresh."
**What should happen:** Validate n=47 ≥30 ✓. Score 47 deals against original rubric. Findings:
- **Tier cutoff calibration:** 8/30 wins (27%) scored <T1 cutoff (75) — at the edge; recommend lowering T1 cutoff to 72 (better separation).
- **Dimension weight re-tuning:** Trigger dimension correlates 0.68 with closed_won (high); Strategic correlates 0.12 (low). Recommend Trigger weight 25 → 30; Strategic weight 10 → 5; Pain unchanged at 25; redistribute remaining +0 across WTP/Reach/TTV.
- **Segment shift:** 8 wins (17% of total) in Healthcare — not in original SaaS-only ICP. Recommend Healthcare as a sub-segment with own variant scorecard, OR explicit ICP expansion. Surface for user decision.
- **Lost-reason patterns:** lost-to-Guru 7 deals (15% of losses) — feeds `competitive-intelligence` battle-card refresh; no-budget concentrated in deals <$30K — feeds `revenue-forecasting` ACV reality-check.
- **Retroactive rescoring proposal:** New rubric applied to active pipeline (32 deals): 4 deals would shift Tier-2 → Tier-1; 2 from Tier-1 → Tier-2; 1 from Tier-3 → Tier-2.
- **Confidence rubric upgrade:** Hypothesis → Medium (n=47, 10–29 threshold met).
Push refinement record. User authorization queue: 5 items (cutoff change / weight re-tune / Healthcare decision / retroactive rescoring trigger / `competitive-intelligence` battle-card refresh).

**User prompt:** "Forecast accuracy showed Tier-2 over-predicted in Q2 — refine."
**What should happen:** Targeted refinement on Tier-2 segment. Pull Tier-2 deals from Q2 (n=22 — below 30 threshold, but combined with Tier-1 + Tier-3 = 47 ≥30). Run analysis. Findings: Tier-2 won 14% of deals vs rubric-predicted 28% — over-confident. Investigate: Tier-2 deals at <$25K ACV losing to no-budget more often than Tier-2 deals at $25K+. Recommend: tighten WTP dimension floor (min $25K ACV signal for Tier-2 entry).

**User prompt:** "Refine the ICP — 12 closes total."
**What should happen:** Refusal: n=12 below 30-close threshold. Recommendation: continue collecting closes; in interim, use `lead-scoring` to retroactively rescore the 12 closes against current rubric to spot-check directional accuracy; defer formal refinement until n≥30.

## Linked Skills

- ICP rubric source → upstream `icp-definition` (refinement updates the rubric file)
- Re-score active pipeline post-refinement → `lead-scoring` (with new rubric)
- Forecast accuracy audit triggers refinement → `revenue-forecasting`
- Lost-to-competitor patterns → `competitive-intelligence` (function-1)
- New segment recommendations → `positioning-strategy` (function-1) for messaging implications
- Lost-reason patterns affecting cadence → `cold-email-sequence` (rewrite mode for problem segments)
- Conversation pattern feeds → `conversation-intelligence` + `customer-feedback-analysis`
- Updated confidence rubric → `kpi-reporting` (data-quality KPIs)

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-6-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| ICP refinement report | `interaction` (type: `research`) | `relevance` = full report (cutoff calibration / weight re-tuning / segment shifts / lost-reason patterns / retroactive proposal); `tags: "#icp-refinement #function-6"` |
| Per-recommendation evidence record | `interaction` (type: `research`) | `relevance` = recommendation + evidence (deal counts + IDs + win rates); `tags: "#icp-refinement-recommendation #function-6"` |
| User authorization queue | `interaction` (type: `research`) | `relevance` = pending recommendations + auth status; `tags: "#manual-review #icp-refinement-auth #function-6"` |
| Lost-reason pattern routed to competitive-intelligence | `interaction` (type: `research`) | `relevance` = competitor + deal count + lost-rate; `tags: "#lost-to-competitor-pattern #function-6"` (feeds function-1) |
| Confidence rubric upgrade | `interaction` (type: `research`) | `relevance` = old → new tier + evidence (n closes); `tags: "#confidence-rubric-upgrade #function-6"` |
| `[unverified — needs check]` (refinement based on insufficient n) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #icp-refinement-loop"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
ICP_REFINEMENT_MIN_CLOSED_DEALS=30
ICP_REFINEMENT_AUDIT_QUARTERLY=true
```

### Source tag

`source: "skill:icp-refinement-loop:v2.0.0"`

### Example push (refinement run)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#icp-refinement #function-6",
    "relevance": "ICP refinement Q2-2026 (47 closes since last refresh). Findings: (1) Tier-1 cutoff: 8/30 wins (27%) scored <75 — recommend lower to 72. (2) Dimension re-tuning: Trigger correlates 0.68 with wins (recommend weight 25→30); Strategic 0.12 (recommend 10→5). (3) Segment shift: 8 wins (17%) in Healthcare — not in original SaaS-only ICP; surface for decision. (4) Lost-reasons: 7 lost-to-Guru → competitive-intelligence; no-budget concentrated <$30K → revenue-forecasting. (5) Retroactive rescore: 4 Tier-2→Tier-1 / 2 Tier-1→Tier-2 / 1 Tier-3→Tier-2. Confidence rubric: Hypothesis → Medium (n=47). User authorization queue: 5 pending items.",
    "source": "skill:icp-refinement-loop:v2.0.0"
  }'
```

### Example push (refusal — insufficient n)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#icp-refinement-refused #function-6",
    "relevance": "ICP refinement REFUSED. Closed deal count: 12 (below 30 threshold). Insufficient signal for refinement. Recommendation: continue collecting closes; in interim, use lead-scoring to retroactively rescore the 12 closes for directional spot-check; defer formal refinement until n≥30.",
    "source": "skill:icp-refinement-loop:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[verified: closed-deals:n=<N>]` (refinement based on real deal data) | Standard mapping. |
| `[unverified — needs check]` (recommendation evidence ambiguous OR n marginal) | Pushes ONLY as `interaction:research` with `#unverified #review-required #icp-refinement-loop` tags; user authorization required before any rubric update. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- n<30 closes — push refusal record; no refinement recommendations.
- Refinement attempted but recommendations identical to current rubric → push `#no-refinement-needed` record.
- User has not authorized any recommendations yet — pending auth queue stays as `interaction:research`; no rubric update applied.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
