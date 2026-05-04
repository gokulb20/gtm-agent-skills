# Function 6 — Reporting & Optimization Conventions

This file is the shared rules document for every skill in `function-6-skills/`. All five skills (`kpi-reporting`, `customer-feedback-analysis`, `channel-performance`, `ab-testing-messaging`, `icp-refinement-loop`) MUST reference this document by name in their `## Inputs Required` and Pitfalls sections rather than redefining the schema, the regime-selection rules, or the attribution standards locally.

> *The worked examples in function-6 skills use the fictional product **WorkflowDoc** for illustration. The schemas, routing rules, threshold defaults, attribution standards, and procedures are vertical-agnostic and apply to any B2B GTM context.*

---

## 1. Why this file exists

Functions 1–5 each produce primary entities (companies, leads, conversations, deals). **Function 6 is read-mostly**: it consumes function-3 outreach metrics, function-4 reply patterns, function-5 pipeline + forecast state, and customer feedback corpora — then writes back analytical artifacts (KPI reports, A/B test results, channel reallocations, ICP deltas, theme extractions). All five skills:

- Read the **same upstream metric records** and risk diverging on field names, freshness expectations, or which "reply rate" they mean.
- Produce **analytical / advisory `interaction:research`** records (not new `company` / `person` entities) and risk diverging on tag conventions, source-tag prefixes, or provenance routing.
- Apply **statistical / attribution / experimentation** discipline (regime selection, attribution methods, confidence floors) where one skill drifting infects every downstream consumer.
- Inherit from upstream functions (1–5) on schemas (ICP scorecard, Lead record, Reply taxonomy, Pipeline stages) — without a centralized inheritance map the skills re-derive them and drift.

One conventions file kills five sources of drift. This file is **NOT** a skill — no frontmatter, no SKILL.md / SKILL-DETAILED.md split. It is a shared reference doc per CLAUDE.md "When to add a `function-N-conventions.md`".

---

## 2. Shared schemas

These are the canonical shapes every function-6 skill emits or consumes. Skills MUST reference fields by name rather than redefine them.

### 2.1 KPI record (produced by `kpi-reporting`, consumed by all)

```yaml
kpi_record:
  report_id: <uuid>
  cadence: <weekly | biweekly | monthly>
  window_start: <ISO date>
  window_end: <ISO date>
  north_star:
    metric: <e.g. pipeline-generated-revenue>
    value: <float>
    unit: <usd | count | rate>
    wow_abs: <float>
    wow_pct: <float>
    trend_4w: <up | flat | down>
  leading_metrics:
    - { name, channel, value, wow_abs, wow_pct, benchmark_value, benchmark_source, freshness_date }
  lagging_metrics:
    - { name, value, wow_abs, wow_pct, benchmark_value, benchmark_source, freshness_date }
  whats_working: [ { finding, context, recommended_action, linked_skill } ]
  whats_not: [ { finding, context, recommended_action, linked_skill } ]
  per_channel: [ { channel, volume, reply_rate, meeting_rate, cpm, cpd_last_touch, cpd_multi_touch } ]
  pipeline_snapshot:
    stage_distribution: { new, contacted, engaged, meeting, discovery, proposal, closed_won, closed_lost }
    stuck_count: <int>
    cycle_time_per_stage: { stage: median_days }
    win_rate_per_tier: { tier-1, tier-2, tier-3 }
  provenance: <see §6>
```

### 2.2 ABTestRun (produced by `ab-testing-messaging`, consumed by `kpi-reporting`, `channel-performance`)

```yaml
ab_test_run:
  test_id: <uuid>
  campaign_id: <ref campaign-management>
  variable: <subject | opener | hook | cta | sequence-length | send-time>
  variant_a: { copy_or_config, allocation_pct }
  variant_b: { copy_or_config, allocation_pct }
  hypothesis: <one sentence>
  primary_metric: reply-rate          # never open-rate (Apple MPP)
  secondary_metrics: [meeting-rate, positive-reply-rate]
  regime: <low-volume | high-volume>  # see §4
  significance_method: <bayesian | frequentist-z>
  thresholds:
    bayesian_threshold: <float>       # default 0.85; canonical 0.95 (see §9)
    frequentist_alpha: <float>        # default 0.05
    min_effect_size_pp: <float>       # regime-dependent — see §9
  min_n_per_arm: 50
  max_duration_days: 14
  per_arm_results: [{ arm, n, conversions, rate }]
  significance_call: { method, posterior_or_p, effect_size_pp, winner | inconclusive, regime }
  ship_action: <ship-winner | hold | inconclusive-default>
  provenance: <see §6>
```

### 2.3 Theme record (produced by `customer-feedback-analysis`, consumed by `kpi-reporting`, `icp-refinement-loop`)

```yaml
theme:
  theme_id: <uuid>
  theme_class: <pain-job-anchor | forces-of-progress | positive-outcome | feature-request
                | bug-friction | pricing-reaction | competitor-mention | champion-language>
  related_entity: <competitor name | feature name | outcome name | null>
  verbatim_quote: <string>            # MANDATORY — see anti-fab §6
  source_id: <transcript / survey / review URL or ID>
  source_position: <timestamp | line | permalink>
  sentiment: <positive | negative | neutral | mixed>
  customer_segment: <ICP tier / industry / size band>
  customer_state: <won | churned | active | prospect>
  frequency: <int>                    # mentions across the corpus
  per_segment_concentration: { segment_name: pct }
  routing: [<icp-definition | positioning-strategy | competitive-intelligence
            | revenue-forecasting | cold-email-sequence | product-backlog>]
  provenance: <see §6>
```

### 2.4 ChannelMetrics (produced by `channel-performance`, consumed by `kpi-reporting`, `icp-refinement-loop`)

```yaml
channel_metrics:
  channel: <email | linkedin | cold-call | web-sourced | event | other>
  window_start / window_end: <ISO date>
  volume: { touches_sent, replies, meetings, deals_closed_won }
  cost_breakdown:
    tool_subscription: <usd>
    per_touch_credits: <usd>
    rep_time_hours: <float>
    rep_loaded_cost_per_hour: <usd>
    allocated_share: <float 0–1>
  cost_per_meeting: <usd>
  cost_per_deal_last_touch: <usd>
  cost_per_deal_multi_touch: <usd>
  marginal_cac_estimate: <usd>        # see §5
  diminishing_returns_position: <headroom | near-cap | at-cap>
  trend_90d: <improving | stable | degrading>
  provenance: <see §6>
```

### 2.5 ICPRefinementProposal (produced by `icp-refinement-loop`, consumed by `kpi-reporting`)

```yaml
icp_refinement_proposal:
  proposal_id: <uuid>
  basis_n_closes: <int>               # MUST be ≥30 — see §10
  tier_cutoff_changes: { tier-1: { from, to }, tier-2: { from, to }, tier-3: { from, to } }
  dimension_weight_changes: [{ dimension, from, to, correlation_with_won }]
  segment_shifts: [{ from_segment, to_segment, evidence }]
  anti_icp_boundary_changes: <text>
  retroactive_rescoring_recommended: <bool>
  confidence: <hypothesis | low | medium | high>
  provenance: <see §6>
```

---

## 3. Reporting cadence + freshness rules

| Skill | Default cadence | Trigger overrides | Reads from window |
|---|---|---|---|
| `kpi-reporting` | weekly (`KPI_REPORT_CADENCE=weekly`) | board snapshot / SDR 1:1 prep / campaign retro | last 7d (weekly) / 14d (biweekly) / 30d (monthly) |
| `customer-feedback-analysis` | quarterly + on-trigger (≥5 new items per source) | won-deal interview batch / churn-survey window close / G2 batch | the corpus delivered |
| `channel-performance` | quarterly | budget-reallocation request / `revenue-forecasting` accuracy audit | last 90d minimum (50-meetings floor as fallback) |
| `ab-testing-messaging` | per-test, ad-hoc | active-campaign optimization / `campaign-management` swap-copy | per-test 14d max |
| `icp-refinement-loop` | quarterly (`ICP_REFINEMENT_AUDIT_QUARTERLY=true`) | `revenue-forecasting` accuracy audit / Tier-1 win-rate drift | since last refinement run |

### 3.1 Freshness floors (hard rules)

| Source data | Min window | Behavior below |
|---|---|---|
| `channel-performance` channel data | 90d OR 50 meetings | Refusal — partial diagnostic only, no reallocation recommendations |
| `icp-refinement-loop` closed deals | ≥30 closes (won + lost) | Refusal — `ICP_REFINEMENT_MIN_CLOSED_DEALS=30` |
| `ab-testing-messaging` arm | n ≥ 50 / arm | Inconclusive regardless of significance result |
| `customer-feedback-analysis` per-source corpus | 5 items per source | Surface individual items only — no aggregation, no theme claims |
| `kpi-reporting` per-channel data | 7d (weekly cadence) | Flag explicitly; report still produced with the gap surfaced |

### 3.2 Open-rate exclusion (universal)

Apple MPP made open rate noise. **No function-6 skill uses open rate as a primary metric.** Reply / meeting / closed-won / acceptance / connect rates are the truth. Open rate may appear ONLY with an explicit "noisy metric" caveat in `kpi-reporting`, never as a KPI, A/B test primary metric, or channel-comparison metric.

---

## 4. A/B test routing — Bayesian-vs-frequentist regime selection

Per traffic volume, every test runs in one of two regimes. Regime is picked **up front** at design time based on expected campaign volume per arm over the 14-day max duration. Mid-test regime changes are forbidden (data contamination).

### 4.1 Regime table

| Regime | Trigger | Significance method | `MIN_EFFECT_SIZE_PP` | Sample-size guidance | What it produces |
|---|---|---|---|---|---|
| **Low-volume** | <1,000/arm/14d expected | Bayesian | `3.0` | n ≥ 50/arm minimum; ~150/arm typical | Directional signal only — NOT shippable as a precise lift; user accepts the regime up front |
| **High-volume** | ≥5,000/arm/14d expected | Frequentist two-proportion z-test | `1.0` | ~6,700/arm minimum at 4% baseline + 1pp MDE + 80% power + 5% alpha | Shippable winner with stated confidence |

**Mid-zone (1,000–5,000/arm/14d):** default to low-volume regime for safety. User can override to high-volume if planning to extend duration to reach the n-per-arm minimum.

### 4.2 Internal-inconsistency rule

A test running at <1,000/arm with `MIN_EFFECT_SIZE_PP=1.0` is mathematically inconclusive on small effects — the math doesn't support detecting 1pp lifts at that volume. The skill MUST surface this to the user at design time and force a regime choice before launch.

### 4.3 Concrete sample-size benchmarks (two-proportion z-test, 80% power, 5% alpha)

| Baseline | MDE (absolute pp) | Required n per arm |
|---|---|---|
| 4% | 1.0pp | ~6,700 |
| 4% | 2.0pp | ~1,800 |
| 4% | 3.0pp | ~850 |
| 5% | 0.5pp | ~31,195 |
| 5% | 1.0pp | ~7,900 |

Reverse table — what 1,500/arm can detect at 4% baseline: ~2.0pp MDE. (1,500/arm cannot detect 1pp lifts.)

---

## 5. Attribution standards

### 5.1 Closed-deal attribution methods (use BOTH)

Multi-touch attribution (`ChannelMetrics.cost_per_deal_multi_touch`) is computed alongside last-touch (`cost_per_deal_last_touch`). They tell different stories:

- **Last-touch**: deal credited to the channel of the last touch before reply/meeting. Simple, often biases toward email (cheapest closing channel).
- **Multi-touch (weighted)**: first 30% / middle 40% / last 30% of touches across the journey. Surfaces channels doing setup work that other channels finish.

Skills (especially `channel-performance`, `kpi-reporting`) MUST surface both. Don't pick one as truth.

### 5.2 Marginal-CAC framing (canonical correction per F6-CP1, 2026-05-04)

Marginal CAC (the expected cost of acquiring the next deal at current spend level) is **standard microeconomics — the equimarginal principle (~19th-century)** widely applied in modern **Marketing Mix Modeling (MMM)** practice. It is NOT an Aaron Ross or Mark Roberge concept.

- Aaron Ross (*Predictable Revenue*, 2011) popularized **outbound sales specialization** + the SDR/AE split.
- Mark Roberge (*Sales Acceleration Formula*, 2015) popularized **engineering rigor in sales process** (hiring formula, training formula).
- Neither owns marginal-CAC. Use the framing: *"marginal-CAC analysis (standard microeconomics — the equimarginal principle, ~19th-century — applied per modern MMM practice)."*

### 5.3 Time-cost allocation (universal)

Rep time is a real channel cost, not "free labor". Every channel cost calculation in function-6 includes:

```
channel_cost = tool_subscription + per_touch_credits + (rep_hours × rep_loaded_cost_per_hour × allocated_share)
```

A channel with no tool subscription (cold call) but heavy rep time is often more expensive per meeting than a channel with high tool spend but automated touches.

---

## 6. Anti-fabrication tagging — function-6-specific

The universal four-tag rule applies (`[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`). Function-6 has three specific risks worth calling out:

### 6.1 Aggregated metrics still need provenance

A "75% reply rate this week" composed by aggregating across 12 campaigns is `[verified: campaign-management:run_<id>,run_<id>,...]` only if every contributing run is verified. If even one contributing run is `[unverified]`, the aggregate downgrades to `[unverified — needs check]` and tags `#metric-aggregation-unverified`.

### 6.2 Theme extraction without verbatim is forbidden

`customer-feedback-analysis` MUST cite a verbatim quote with source ID + timestamp/permalink for every extracted theme. Paraphrased themes ("they said the product was confusing") with no quote default to `[unverified — needs check]` and never get pushed as actionable signal — only as `interaction:research` with `#unverified #review-required`.

### 6.3 A/B test winners need raw numbers

Significance calls in `ab-testing-messaging` MUST include raw n per arm + conversions per arm + posterior (Bayesian) or p-value (frequentist) + effect size. A "winner" call without the underlying numbers is `[unverified — needs check]`. The `ABTestRun.significance_call` shape forces all four fields.

### 6.4 ICP-refinement proposals need the closes count

`icp-refinement-loop` writes `basis_n_closes` to every proposal. If `<30`, the proposal is refusal-flagged and pushes only as `interaction:research` with `#unverified #insufficient-evidence`. The `ICPRefinementProposal.confidence` field follows `icp-definition`'s confidence rubric (Hypothesis / Low / Medium / High).

### 6.5 Function-6-specific provenance routing (extends CLAUDE.md universal rule)

| Provenance | Push behavior |
|---|---|
| `[verified: <function-skill>:run_<id>]` (metric values from upstream skill runs) + `[user-provided]` (cost data, customer transcripts) | Pushes per the standard mapping (see §7) |
| `[unverified — needs check]` (data freshness gap, missing verbatim, insufficient n) | Pushes ONLY as `interaction:research` with `#unverified #review-required #<skill-name>` tags; downstream routing deferred |
| `[hypothetical]` | Does NOT push. Local artifact only (worked examples) |

---

## 7. Push-to-CRM conventions for function-6

Function-6 produces **analytical / advisory artifacts**, not new entities. The primary push entity is `interaction` (type: `research`). Skills NEVER push synthetic `company` / `person` records — even when the analysis names them, the entity record is owned by the upstream function (1–5) that originated it. Function-6 may PATCH existing person/company tags with feedback signals (e.g., `customer-feedback-analysis` tagging a person with `#champion-language-source`).

### 7.1 Entity routing per skill

| Skill | Primary push | Secondary push |
|---|---|---|
| `kpi-reporting` | `interaction:research` (full report; `tags: "#kpi-report #report-<cadence> #function-6"`) | per-finding `interaction:research`; per-rep coaching slice |
| `customer-feedback-analysis` | `interaction:research` per theme + per run (`tags: "#customer-feedback #theme-<class> #function-6"`) | PATCH on existing `person` (champion-language source) / `company` (feedback signal); product-backlog routing if `LINEAR_API_KEY` set |
| `channel-performance` | `interaction:research` (full report; `tags: "#channel-performance #function-6"`) | per-channel `interaction:research`; reallocation recommendation; Bullseye-refresh recommendation |
| `ab-testing-messaging` | `interaction:research` at launch (test design) + at call (test result) | shipped-winner action `interaction:research`; PATCH campaign config |
| `icp-refinement-loop` | `interaction:research` (proposal with delta + evidence; `tags: "#icp-refinement-proposal #function-6"`) | retroactive-rescoring proposal; PATCH `icp-definition` artifact reference |

### 7.2 Source tag

Every push carries `source: "skill:<skill-name>:v<version>"` (e.g. `skill:kpi-reporting:v2.0.0`).

### 7.3 Named-product vs non-product hygiene (per CLAUDE.md rule #6)

Function-6 rarely names new products; when it surfaces a competitor mention from feedback or a competitor outperforming in a test, that's an `interaction:research` referencing the existing entity (function-1 `competitor-analysis` owns the canonical record). Never push synthetic competitor `company` records from function-6.

### 7.4 When NOT to push

- Insufficient data (per §3.1 freshness floors) — push refusal record only; no recommendations.
- Provenance `[unverified — needs check]` — see §6.5.
- Provenance `[hypothetical]` — never.
- Already-pushed within last cadence window (dedup by `report_id` / `test_id` / `proposal_id`) — push dedup notice.

---

## 8. Inheritance from upstream functions (1–5)

Every function-6 skill declares these inheritance edges. If the upstream skill / data has not been run, function-6 skills can still operate but flag output as `confidence: low` and tag `[unverified — needs check]` aggressively.

| Function-6 skill | Reads from |
|---|---|
| `kpi-reporting` | `campaign-management` (touches/reply/meeting metrics — function-3); `pipeline-stages` (stage distribution, stuck deals, win rate per tier — function-5); `revenue-forecasting` (forecast vs actual, MAPE — function-5); `channel-performance` (per-channel KPIs — function-6); `conversation-intelligence` (patterns — function-4); `customer-feedback-analysis` (themes — function-6) |
| `customer-feedback-analysis` | Won-deal interview transcripts (`conversation-intelligence` — function-4); churn surveys (external tool); G2/Capterra/TrustRadius reviews (external API); support tickets (external); ICP firmographic + Pain-Trigger-Outcome chain from `icp-definition` (function-1, including the **Workaround Analysis** sub-component which is consumed when classifying forces-of-progress themes) |
| `channel-performance` | `campaign-management` 90d+ metrics (function-3); per-channel cost data (`user-provided`); closed-deal attribution from `pipeline-stages` (function-5); current channel-bet artifact from `channel-strategy` (function-1) |
| `ab-testing-messaging` | `campaign-management` campaign records + active variants (function-3); `cold-email-sequence` framework defaults (function-3 — for designing variants); outcome metrics (function-3 + function-4 reply classification) |
| `icp-refinement-loop` | Closed-won/lost records (function-5 `pipeline-stages`); current ICP scorecard + tier cutoffs (function-1 `icp-definition` — including the 100-pt scorecard rubric and the **Workaround Analysis**); lost reasons from `pipeline-stages`; segment tags on deals (function-2 `lead-scoring`); `customer-feedback-analysis` themes (this function) |

If `icp-definition` (function-1) has not been run, `customer-feedback-analysis` and `icp-refinement-loop` can still operate but flag output as **ungrounded** until the ICP exists.

---

## 9. Threshold defaults

The canonical defaults — overridable via env vars per skill, but skills MUST surface the override to the user when it deviates from the canonical.

| Threshold | Default | Env var | Notes |
|---|---|---|---|
| Bayesian P(B>A) winner threshold | `0.85` | `AB_TEST_BAYESIAN_THRESHOLD` | **0.95 is industry-canonical** (Optimizely default; statistics.tools / Dynamic Yield / JobCannon). 0.85 is a documented low-volume floor — Optimizely allows configuration down to 0.70 for low-traffic sales tests. The 0.85 house default is a pragmatic floor for B2B sales-volume regimes. Skills MUST flag the canonical-vs-pragmatic gap to the user when calling winners at 0.85 ≤ posterior < 0.95. |
| Frequentist alpha | `0.05` | `AB_TEST_FREQUENTIST_P` | Industry-standard p<0.05 |
| `MIN_EFFECT_SIZE_PP` (low-volume regime) | `3.0` | `AB_TEST_MIN_EFFECT_SIZE_PP` | Regime-dependent (see §4) |
| `MIN_EFFECT_SIZE_PP` (high-volume regime) | `1.0` | same | Regime-dependent (see §4) |
| Min n per arm (A/B test) | `50` | — | Below = inconclusive regardless of significance |
| Max test duration | `14d` | — | Longer = drift / external confounds |
| ICP refinement min closed deals | `30` | `ICP_REFINEMENT_MIN_CLOSED_DEALS` | Below = refusal |
| Channel performance min window | `90d` (or 50 meetings, whichever earlier) | — | Below = refusal / partial diagnostic only |
| Customer feedback min corpus per source | `5` | — | Below = individual items only, no aggregation |
| ICP-implication theme threshold | `≥30%` of won-deal interviews in a segment | — | Triggers `icp-refinement-loop` flag |
| KPI report one-screen budget | `≤450 words` (top section) | — | Deeper data linked, not embedded |
| KPI WoW material-change flag | `±20%` | — | Below = note; above = flag |
| Budget reallocation per quarter cap | `10–25%` shift | — | Smaller on weak signals; larger on convergent (CPD + marginal-CAC + reply-trend aligned) |

---

## 10. Routing logic — which signal triggers which function-6 skill

Deterministic, not vibe-based. Per signal, the canonical owner skill is:

| Signal / trigger | Owner skill | Why |
|---|---|---|
| Standing weekly review / board snapshot / SDR coaching prep | `kpi-reporting` | The recurring report-shape contract |
| ≥5 new feedback items in any source (interview / churn / review / ticket) | `customer-feedback-analysis` | Owns theme extraction + verbatim discipline |
| ≥2 channels with 90d+ data + budget question | `channel-performance` | Owns the CPM/CPD + marginal-CAC + Bullseye refresh |
| Active campaign messaging optimization / new copy hypothesis | `ab-testing-messaging` | Owns regime selection + significance discipline |
| ≥30 closed deals since last refresh / forecast accuracy audit shows segment miscalibration | `icp-refinement-loop` | Owns the rubric vs reality recompute |
| Reply rate plateaued | `ab-testing-messaging` (then `kpi-reporting` for trend context) | Test → confirm |
| Tier-1 win rate dropped 6pp+ WoW persistent 2+ weeks | `kpi-reporting` flags → `icp-refinement-loop` | Pattern detection then refinement |
| Conversation-intel flagged feature-request pattern crossing threshold | `customer-feedback-analysis` | Theme extraction + product-backlog routing |
| Lost-to-competitor rate spike in a segment | `icp-refinement-loop` (anti-ICP boundary check) + `competitive-intelligence` (function-1) | Both owners run their lane |
| Forecast MAPE > 30% at confidence-medium | `kpi-reporting` flags → `revenue-forecasting` recalibration (function-5) + `icp-refinement-loop` | Segment-driven miscalibration |

When two skills could plausibly run, prefer the one whose freshness floor is met (§3.1).

---

## 11. Cost-awareness rules

**None apply at the function-6 skill level.** Function-6 is read-mostly: it consumes upstream data and produces analytical artifacts. There is no per-record API spend, no scraper credits, no `SOURCING_RUN_USD_CAP` to honor.

The cost discipline that DOES live in function-6:

- `channel-performance` reports cost-per-meeting + cost-per-deal per channel (it MEASURES cost; doesn't spend it). Cost data is `[user-provided]`.
- `kpi-reporting` references upstream credits-used (from function-2 sourcing skills' run records) for cost-per-lead trend; it doesn't itself spend.
- `ab-testing-messaging` doesn't spend on the test itself — variants ship via the channel skill (function-3), which honors that function's cost rules.

If a function-6 skill ever needs a paid LLM call for theme extraction (e.g., `customer-feedback-analysis` calling Anthropic / OpenAI), it inherits the function's `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` env vars and reads vendor docs at runtime — pricing changes; never hardcode a per-token rate.

---

## 12. WorkflowDoc worked-example continuity

Function-1 used WorkflowDoc as the company being analyzed. Function-2 flipped the camera so WorkflowDoc became the seller. Function-6 keeps the seller frame: **WorkflowDoc is the seller running its outreach + post-sale loop**, and function-6 is the team doing the GTM review on its own pipeline.

Worked examples in function-6 skills chain across:

1. `kpi-reporting` (this function) → produces weekly report on WorkflowDoc's GTM funnel: Tier-1 win rate, channel mix, cycle-time per stage.
2. `customer-feedback-analysis` (this function) → extracts themes from 8 won-deal JTBD interviews + 12 churn responses + G2 reviews on WorkflowDoc + Guru / Stonly competitors. Surfaces forces-of-progress (push / pull / habit / anxiety) and routes ICP-implications back to `icp-refinement-loop`.
3. `channel-performance` (this function) → 90-day per-channel review on WorkflowDoc's email / LinkedIn / cold call. Marginal-CAC analysis recommends 15% shift email→LinkedIn; Bullseye refresh suggests web-sourced as a ring-2 test.
4. `ab-testing-messaging` (this function) → tests CCQ+Pain vs CCQ+Vision opener on WorkflowDoc's active cadence. Low-volume regime (300/arm) → Bayesian + MES 3.0 → directional winner (Vision) feeds back to `cold-email-sequence` framework defaults.
5. `icp-refinement-loop` (this function) → after 47 closed deals, recomputes WorkflowDoc's ICP scorecard against actuals; surfaces tier cutoff drift and recommends weight retuning.

Every fictional entity (target company names, contact names, signal sources, dates, dollar figures, competitor names, customer quotes) is tagged `[hypothetical]` inline at first mention per the worked-example tagging convention. The seller (WorkflowDoc) and its named ICP companies (Stitchbox, Helio, Volaris) inherit `[hypothetical]` from the function-1/2/3 worked examples and re-tag on any fact-bearing assertion (specific dollar figures, dates, statistics).

The frameworks, regime selection, attribution standards, and threshold defaults are vertical-agnostic and apply to any B2B GTM context.

---

## Document version

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-05-04 | Initial draft alongside F6 skill-fix pass (F6-CFA1 / F6-CP1 / F6-AB1 / F6-AB2). Codifies regime selection (§4), marginal-CAC framing correction (§5.2), Moesta forces vocabulary push/pull/habit/anxiety (§2.3), Bayesian threshold canonical-vs-pragmatic gap (§9). |
