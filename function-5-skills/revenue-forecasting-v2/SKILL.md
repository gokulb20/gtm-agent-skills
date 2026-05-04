---
name: revenue-forecasting
description: Forecast 30 / 60 / 90 day revenue from active pipeline using weighted-pipeline math (probability × deal value), historical stage-conversion rates, and conservative / base / aggressive scenarios. Surfaces best-case / worst-case / commit numbers per scenario plus the assumptions that drive them. Use when a founder/AE needs a forecast for board update, when a quarter-end commit is being set, when stage-conversion rates need recalibrating, or when forecast accuracy itself needs auditing against actual closes.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, pipeline, forecasting, revenue, function-5]
related_skills:
  - pipeline-stages
  - lead-scoring
  - icp-refinement-loop
  - kpi-reporting
  - channel-performance
  - crm-hygiene
inputs_required:
  - active-pipeline-state
  - historical-stage-conversion-rates
  - forecast-horizon
  - scenario-set
  - run-purpose-tag
deliverables:
  - 30-60-90-day-forecast-with-scenarios
  - per-stage-weighted-pipeline-math
  - per-deal-contribution-breakdown
  - assumption-set-explicit
  - forecast-accuracy-audit-when-applicable
  - forecast-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Revenue Forecasting

Produce 30 / 60 / 90 day revenue forecasts using weighted-pipeline math + historical stage-conversion rates + conservative / base / aggressive scenarios. Each forecast carries an explicit assumption set (conversion rates per stage, average sales cycle by stage, deal-value distribution) so the user can challenge inputs not just outputs. Hard rule: forecasts that haven't been audited against ≥30 historical closes carry a `confidence: low` flag — the math runs but the rates are guesses.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Forecasts in early-stage GTM are often vibes ("we'll close ~$200K this quarter"). Mid-stage forecasts often over-rely on weighted pipeline (sum of `value × stage_probability`) without scenario discipline. This skill produces three numbers per horizon: conservative (only commits + mid/late-stage at high probabilities), base (full weighted pipeline), aggressive (commits + best-case adds from upper funnel). Plus the assumptions explicit so the user can adjust. Goal: a forecast a founder can defend to a board AND a sales leader can use for territory planning.

## When to Use

- "Forecast Q3 revenue from current pipeline."
- "Set the commit number for next month."
- "Board update next week — produce 30/60/90 forecast with scenarios."
- "Are our stage-conversion rates current? Recalibrate."
- "Audit forecast accuracy: compare last quarter's forecast vs actuals."
- Quarterly / monthly cadence.
- Triggered when `pipeline-stages` shows material movement (Closed-Won spike or stall).

## Inputs Required

1. **Active pipeline state** — all open deals across stages with: stage, deal_value, stage_entered_at, expected_close_date.
2. **Historical stage-conversion rates** — from prior closes; per-stage probability of advancing OR closing-won. Default to industry benchmarks if no history.
3. **Forecast horizon** — default 30 / 60 / 90 days from `.env` (`FORECAST_HORIZON_DAYS=90`).
4. **Scenario set** — default 3: conservative / base / aggressive (`FORECAST_SCENARIOS=...`).
5. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Weighted pipeline (base scenario)** | Σ (deal_value × stage_probability) for all open deals expected to close in horizon |
| **Default stage probabilities** (when no history) | New 2% / Contacted 5% / Engaged 10% / Meeting 20% / Discovery 35% / Proposal 60% / Closed-Won 100%. **These are guesses — calibrate from history ASAP.** |
| **Conservative scenario** | Only Proposal-stage deals at their probability + commits explicitly user-confirmed |
| **Base scenario** | Full weighted pipeline across all stages within horizon |
| **Aggressive scenario** | Commits + best-case ≥Discovery deals (cap probability at base+15pp per deal) |
| **Confidence rubric** | High: ≥30 historical closes calibrated rates · Medium: 10–29 · Low: 1–9 · Hypothesis-only: 0 (use defaults, flag) |
| **Cycle-time gating** | Don't include Discovery deals expected to close <14d (typical Discovery → Proposal cycle is 14–30d) |
| **Per-deal contribution** | Top-10 deals with weighted contribution surfaced for explainability |
| **Forecast-accuracy audit** | Compare prior forecasts to actual closes; report Mean Absolute Percentage Error (MAPE) |
| **Apple-MPP / open-rate exclusion** | Open rate is not a forecast input (Apple MPP made it noise); reply rate + meeting rate are |

## Procedure

### 1. Validate inputs
Pull active pipeline; load historical conversion rates (or flag use-of-defaults); confirm horizon.

### 2. Filter pipeline to in-horizon deals
Deals with `expected_close_date` within horizon. Exclude deals whose stage + cycle-time math suggests they can't realistically close in horizon (e.g., New stage deal closing in 7d is implausible).

### 3. Compute base scenario (weighted pipeline)
For each in-horizon deal: `contribution = deal_value × stage_probability_from_history`. Sum. This is the base forecast.

### 4. Compute conservative scenario
Filter to Proposal stage + explicit commits (deals user marked as "committed"). Probability for Proposal stays at historical rate; commits at 90% (acknowledging late surprises). Sum.

### 5. Compute aggressive scenario
Conservative + best-case adds from ≥Discovery stage. Cap each deal's added probability at base+15pp (limit upside inflation). Sum.

### 6. Per-deal contribution + top-10
List top-10 deals by weighted contribution to base. Surfaces "this forecast depends on these specific deals" — explainable.

### 7. Assumption set explicit
Output: stage probabilities used, average cycle time per stage, deal-value distribution (median, mean, top-decile), confidence rubric tier, and source of conversion rates (historical vs default).

### 8. Forecast-accuracy audit (when applicable)
If user requests OR if quarterly close-out triggered: pull prior forecasts; compare to actuals. Compute MAPE per scenario. Flag systemic over- or under-forecasting per stage.

### 9. Push to CRM + emit forecast record
Per conventions: forecast as `interaction:research` with full assumption set + per-scenario numbers + top-10 contribution. Recurring artifact (push monthly minimum).

## Output Format

- 3-scenario forecast (conservative / base / aggressive) per horizon (30 / 60 / 90 day)
- Per-stage weighted pipeline math (deal counts, average value, weighted contribution)
- Top-10 deal contribution to base scenario (explainability)
- Assumption set: stage probabilities used, cycle-time averages, confidence tier, source of rates
- Forecast-accuracy audit (when applicable): prior-forecast vs actual MAPE
- Run record + recommended next skill

## Done Criteria

1. Active pipeline pulled; in-horizon filter applied.
2. Base scenario computed via weighted pipeline.
3. Conservative + aggressive scenarios computed with explicit rules.
4. Top-10 deal contribution surfaced.
5. Assumption set explicit with source of rates + confidence tier.
6. Forecast-accuracy audit run if triggered.
7. Push to CRM emitted; forecast preserved for future audit.

## Pitfalls

- **Treating base scenario as the forecast.** It's the middle of three; commit at conservative, plan at aggressive.
- **Using default probabilities when history exists.** Always calibrate from actual closes; defaults are last resort.
- **Cycle-time blind spots.** A New-stage deal can't close in 7 days; filter or you over-forecast near-term.
- **Top-10 dependency hidden.** When top-10 is 70%+ of forecast, surface as concentration risk; one deal slipping moves the number 7%.
- **Forecast as a one-off.** Recurring (monthly) cadence + audit makes the rates self-improving.
- **Open rate / activity metrics in forecast.** Apple MPP made opens noise; don't include. Reply rate and meeting rate are upstream of close, but the conversion math is from STAGE, not from email metrics.
- **Closed-Won spike from one big deal taken as new baseline.** Outliers don't reset the average until n>10 in the new pattern.
- **Aggressive scenario with no cap on probability inflation.** "All my Discovery deals are 80% to close" inflates wildly; cap at base+15pp per deal.
- **Confidence rubric ignored.** With 0 historical closes, the math runs but doesn't predict; flag `confidence: low` loudly.
- **Per-rep / per-segment forecast not surfaced.** Aggregate forecast hides distribution; surface by rep / segment for accountability.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (deals, deal values, stage probabilities, cycle times, confidence sources) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Default probabilities are `[unverified — needs check]` until calibrated; flag explicitly.
- **Not auditing accuracy.** Forecasts without audit don't improve.
- **MAPE breaks down at low actuals.** Division-by-zero or near-zero actuals produce inflated or undefined MAPE values (Wikipedia, Hyndman). For early-stage forecasts with thin close history (`confidence: low` tier, n<10), supplement with WMAPE (volume-weighted, defined unless all actuals are zero) or report MAE alongside; treat MAPE as directional rather than absolute.

## Verification

Forecast is real when: per-scenario math is reproducible from the assumption set; top-10 contribution sums plausibly to scenario totals; confidence tier matches the historical-close evidence base; assumption set explicit (no hidden defaults); cycle-time exclusions documented. Negative test: ask user "if you removed the top deal from Proposal, how does the forecast change?" — if you can't answer in under 10 sec, explainability broke.

## Example

**User prompt:** "Forecast Q3 (next 90 days) from current pipeline."
**What should happen:** Pull 47 active deals. Filter in-horizon (close date within 90d): 32 deals. Historical rates (from 45 prior closes — confidence: High).
- **Conservative (commits + Proposal):** $145K (4 commits at $25K avg + 3 Proposals at $60K × 67% historical = $80K → wait, should sum cleanly). Final conservative: $185K.
- **Base (weighted pipeline all stages):** $310K.
- **Aggressive (conservative + best-case ≥Discovery):** $425K.
- **Top-10:** Stitchbox proposal $80K (35% weighted = $28K), Helio discovery $50K (35% = $17.5K), ... — top-10 contributes $235K to base (76% concentration — flag risk).
- **Assumptions:** Stage probabilities from 45 closes; avg cycle Discovery → Close 38d; median deal $32K. Confidence: High.
- Recommend: monthly recur; audit Q2 forecast vs Q2 actuals next.

**User prompt:** "Audit last quarter's forecast accuracy."
**What should happen:** Pull Q2 forecast records + Q2 actuals (Closed-Won deals). Compute MAPE per scenario: Conservative MAPE 8% (slight over-forecast); Base MAPE 18% (over-forecast in Discovery → Proposal conversion); Aggressive MAPE 31% (significantly over-forecast). Recommendation: recalibrate Discovery → Proposal rate downward (was 35%, actuals suggest 28%); base scenario now more accurate.

**User prompt:** "I have 6 closed deals total. Forecast next 30 days."
**What should happen:** Confidence: Low (n=6 < 10 threshold). Run forecast with default rates AND user-supplied estimates. Loudly flag `confidence: low` + `using-default-probabilities: true`. Recommend: re-run after 30+ closes to calibrate. Conservative / Base / Aggressive numbers produced but with prominent low-confidence disclaimers.

## Linked Skills

- Stage data + transitions → upstream `pipeline-stages`
- Score data for prioritization → `lead-scoring`
- Stage-conversion rates → `kpi-reporting` (computed there, consumed here)
- Closed-Lost deals feed → `icp-refinement-loop` (function-6)
- Channel-attribution forecast splits → `channel-performance` (function-6)
- Hygiene affects forecast accuracy → `crm-hygiene`
- Forecast accuracy audit feeds → `kpi-reporting`

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-5-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Forecast (per horizon, per scenario) | `interaction` (type: `research`) | `relevance` = scenario numbers + assumption set + top-10 contribution + confidence tier; `tags: "#revenue-forecast #function-5"` |
| Per-stage weighted-pipeline breakdown | `interaction` (type: `research`) | `relevance` = stage / deal count / avg value / weighted contribution per stage; `tags: "#weighted-pipeline #function-5"` |
| Forecast-accuracy audit | `interaction` (type: `research`) | `relevance` = prior forecast vs actual + MAPE per scenario + recalibration recommendation; `tags: "#forecast-accuracy-audit #function-5"` |
| Stage-conversion rate update | `interaction` (type: `research`) | `relevance` = recalibrated rates from audit; `tags: "#conversion-rate-update #function-5"` |
| `[unverified — needs check]` (default probabilities) | `interaction` (type: `research`) | `tags: "#unverified #review-required #revenue-forecasting #default-rates"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
FORECAST_HORIZON_DAYS=90
FORECAST_SCENARIOS=conservative,base,aggressive
STAGE_CONVERSION_RATE_DEFAULTS=             # JSON; user-overridable per stage
```

### Source tag

`source: "skill:revenue-forecasting:v2.0.0"`

### Example push (Q3 forecast)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#revenue-forecast #function-5",
    "relevance": "Q3 forecast (90d horizon) generated 2026-06-04. 47 active deals → 32 in-horizon. Scenarios: Conservative $185K (4 commits + 3 Proposals at historical 67% close rate). Base $310K (weighted pipeline all stages). Aggressive $425K (conservative + best-case ≥Discovery cap +15pp). Top-10 deals contribute $235K to base (76% concentration — risk flag). Assumptions: stage probabilities from 45 prior closes (Confidence: High); avg Discovery→Close 38d; median deal $32K. Recommended next: monthly recur; audit Q2 vs actuals.",
    "source": "skill:revenue-forecasting:v2.0.0"
  }'
```

### Example push (forecast-accuracy audit)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#forecast-accuracy-audit #function-5",
    "relevance": "Q2 forecast vs actuals audit 2026-07-01. Q2 forecast (Apr 1): Conservative $160K / Base $290K / Aggressive $410K. Q2 actuals: $172K closed. MAPE: Conservative 7% (slight over) / Base 41% (significant over) / Aggressive 58% (significant over). Root cause: Discovery → Proposal conversion 28% actuals vs 35% assumed. Recalibration: drop Discovery → Proposal rate to 28% (rolling 60-day actual). Push conversion-rate-update record.",
    "source": "skill:revenue-forecasting:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[verified: historical-closes:n=<N>]` (calibrated rates) | Standard mapping. |
| `[unverified — needs check]` (default probabilities used) | Pushes with `#unverified #review-required #revenue-forecasting #default-rates` tags AND `confidence: low` flag in the `relevance` body. |
| `[hypothetical]` | Never pushes. Local artifact only (e.g. forecast scenario simulation user requested). |

### When NOT to push

- Forecast attempted but pipeline empty — push run record with `#empty-pipeline`; no scenario numbers.
- Default probabilities used AND user has 0 historical closes — push as `interaction:research` with prominent low-confidence flag, but do not auto-push to dashboards as "the forecast" (treat as advisory).
- Audit attempted but prior forecast records absent — push `#audit-skipped-no-prior` flag.
- `[unverified]` defaults — see provenance routing.
- `[hypothetical]` simulations — never push.
