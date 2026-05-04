---
name: ab-testing-messaging
description: Design and run A/B tests on messaging variables (subject lines, opener angles, hooks, CTAs, sequence length, send-time) — compute minimum sample size up front, design one-variable-at-a-time tests, run Bayesian (n<200/arm) or frequentist z-test (n≥200/arm), call winners only at significance + minimum effect size, ship the winner via the channel skill. Use when an active campaign needs messaging optimization, when a new copy hypothesis needs validation before scaling, when reply rate has plateaued and a copy refresh is in flight, or when a sample-size estimate is needed before launching a test.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, optimization, ab-testing, experimentation, function-6]
related_skills:
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - multi-channel-cadence
  - campaign-management
  - kpi-reporting
  - icp-refinement-loop
inputs_required:
  - test-hypothesis-and-variable
  - variant-copy-or-config
  - traffic-split-and-allocation-method
  - primary-and-secondary-metrics
  - significance-method-and-thresholds
  - run-purpose-tag
deliverables:
  - sample-size-estimate-pre-launch
  - test-design-document
  - significance-call-with-method-and-numbers
  - winner-recommendation-or-inconclusive-stop
  - shipped-winner-handoff-to-channel-skill
  - ab-test-design-and-result-interaction-records
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# A/B Testing — Messaging

Design and run A/B tests on outreach messaging variables (subject lines / opener angles / hooks / CTAs / sequence length / send-time) with proper statistical discipline: minimum sample size estimated up front, one-variable-at-a-time test design, Bayesian (n<200/arm, low-volume regime) or frequentist z-test (n≥200/arm, high-volume regime) significance call, winner shipped only when both significance AND the regime-appropriate minimum effect size are met (1pp in high-volume regime, 3pp in low-volume). Hard rule: never ship a "winner" on n<50/arm — that's coin-flip noise.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Sales teams A/B test badly: change three things at once, ship the "winner" at n=20, declare significance on p=0.06, optimize on open rate (Apple MPP noise). This skill enforces the discipline: compute minimum detectable effect (MDE) and sample size BEFORE launching, force one-variable-at-a-time, use Bayesian for small samples (n<200/arm), use frequentist z-test for larger, require BOTH significance + minimum effect size to ship, surface inconclusive after 14d so tests don't run forever. Optimizes on reply rate (the truth), not opens (noise).

## When to Use

- "Does CCQ + Pain or CCQ + Vision opener convert better?"
- "Test 5-touch vs 7-touch sequence length."
- "Subject line: 'Quick question' vs 'New VP CX seat?'"
- "What sample size do I need to detect a 1pp lift?"
- "Test running for 14d, what does the data say?"
- Pre-launch when a copy hypothesis needs validation before scaling.
- Triggered by `campaign-management` swap-copy decision.

## Inputs Required

1. **Test hypothesis + variable** — explicit hypothesis ("Vision opener converts higher than Pain"); ONE variable changes between variants.
2. **Variant copy / config** — variant A (control) + variant B (treatment) ready-to-ship via channel skill.
3. **Traffic split + allocation method** — 50/50 default; allocation by recipient hash for randomness; user can override (e.g., 80/20 to limit treatment risk).
4. **Primary + secondary metrics** — primary always reply rate (Apple MPP-aware); secondary may include meeting rate, positive-reply rate.
5. **Significance method + thresholds** — auto-pick: Bayesian if expected n<200/arm; frequentist z-test if ≥200/arm. Override via env (`AB_TEST_BAYESIAN_THRESHOLD=0.85`, `AB_TEST_FREQUENTIST_P=0.05`, `AB_TEST_MIN_EFFECT_SIZE_PP=1.0`).
6. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **One-variable rule** | Only ONE thing differs between A and B (subject OR opener OR CTA — not multiple) |
| **Primary metric** | Reply rate (open rate is noise — Apple MPP) |
| **Sample size method** | Pre-launch MDE calc (two-proportion z-test). For 4% baseline + 1pp MDE + 80% power + 5% alpha → **~6,700/arm (frequentist)**. Bayesian needs less but is directional, not shippable. *Internal-inconsistency warning: a test running at ~1,500/arm with `MIN_EFFECT_SIZE_PP=1.0` will be perpetually inconclusive — the math doesn't support detecting effects that small. Use the dual-regime block below.* |
| **Dual-regime sample-size block** | **Low-volume regime (<1,000/arm/14d):** Bayesian threshold + `MIN_EFFECT_SIZE_PP=3.0` — only large lifts detectable; accept directional signals only. **High-volume regime (≥5,000/arm/14d):** frequentist z-test + `MIN_EFFECT_SIZE_PP=1.0` + ~6,700/arm minimum for shippable winners. Pick regime up front based on expected campaign volume. |
| **Bayesian threshold (n<200/arm)** | `P(B > A) > 0.85` AND effect size ≥ regime-dependent MES. *Caveat: **0.95 is industry-canonical** (Optimizely default; statistics.tools / Dynamic Yield / JobCannon). **0.85 is a documented low-volume floor** — Optimizely allows configuration down to 0.70 for low-traffic sales tests. House default is 0.85; flag the canonical-vs-pragmatic gap to the user when calling winners.* |
| **Frequentist threshold (n≥200/arm)** | Two-proportion z-test p<0.05 AND effect size ≥1pp |
| **Minimum n per arm** | 50 (below = call inconclusive regardless of result) |
| **Maximum test duration** | 14d default; longer = drift / external factors confound |
| **Allocation** | Hash-based per recipient; same recipient always gets same variant if test re-runs |
| **Apple MPP exclusion** | Open rate not a valid optimization target; use reply / meeting rate |
| **Winner-shipping** | Auto-handoff to channel skill (cold-email-sequence rewrite mode) on winner call; allocates remaining traffic 100% to winner |
| **Inconclusive policy** | After max duration, no winner: stop test; ship higher-volume variant by default; document inconclusive |

## Procedure

### 1. Validate hypothesis + variable
Confirm ONE variable differs between A and B. Multi-variable change → reject, surface to user. Confirm variable is testable (i.e., not "tone" — too fuzzy).

### 2. Pre-launch: compute sample size + MDE + pick regime
Given baseline metric (current campaign reply rate, e.g. 4%), compute sample size needed to detect MDE at 80% power, 5% alpha (two-proportion z-test). For 4% baseline + 1pp MDE this is **~6,700/arm (frequentist)**, NOT 1,500/arm — the older 1,500/arm number was off by ~4.5x. Then pick the regime explicitly:
- **Low-volume regime (<1,000/arm/14d expected):** use Bayesian + `MIN_EFFECT_SIZE_PP=3.0`. Accept directional signals only; do NOT promise shippable winners on small lifts.
- **High-volume regime (≥5,000/arm/14d expected):** use frequentist z-test + `MIN_EFFECT_SIZE_PP=1.0` + plan for ~6,700/arm minimum to actually detect 1pp.
Surface the regime choice to the user, e.g. *"Expected campaign volume 600/arm over 14d → low-volume regime. Bayesian + MES 3.0 only — we will not call a 1pp winner from this volume; the math doesn't support it."*

### 3. Pick significance method
- Expected n<200/arm at duration end → Bayesian.
- Expected n≥200/arm → frequentist z-test.
- User can override.

### 4. Design test document
Output: hypothesis + variable + variant A/B copy + traffic split + allocation method + primary+secondary metrics + significance method + minimum effect size + max duration + minimum n per arm + analysis plan. This is the test contract.

### 5. Launch test via channel skill
Hand off to channel skill (e.g., `cold-email-sequence`) with split + allocation rule. Channel skill applies allocation per recipient + executes touches.

### 6. Monitor + check stop conditions
Daily / weekly check (depends on volume): pull metrics per arm; check (a) min-n-per-arm reached, (b) significance threshold crossed, (c) max duration reached.

### 7. Significance call
- If significance + effect size ≥ threshold AND min-n-per-arm met → call winner; ship via channel skill (allocate 100% remaining traffic to winner).
- If max duration reached without significance → call inconclusive; ship higher-volume variant by default.
- If min-n not yet reached → continue test.

### 8. Push to CRM + emit result
Per conventions: test design as `interaction:research` at launch; result as `interaction:research` at call. PATCH campaign config with shipped winner.

## Output Format

- Pre-launch: sample-size estimate + MDE + significance-method recommendation
- Test design document (one-screen): hypothesis + variants + split + metrics + thresholds
- Mid-test: per-arm metrics + cumulative-sample + significance check + days-to-go estimate
- Significance call: method + numbers (posterior or p-value) + effect size + winner OR inconclusive
- Shipped winner: handoff to channel skill (auto if API mode) or manual instruction (if BYO)
- Run record: test outcome + ship action + recommended follow-up

## Done Criteria

1. Hypothesis + variable validated (one variable rule).
2. Pre-launch sample-size + MDE computed; significance method picked.
3. Test design document complete + delivered to user.
4. Test launched via channel skill; allocation method recorded.
5. Mid-test monitoring honored stop conditions (min-n, significance, max duration).
6. Significance call made with explicit method + numbers + effect size; OR inconclusive declared at max duration.
7. Winner shipped (or higher-volume variant by default on inconclusive).
8. Push to CRM emitted.

## Pitfalls

- **Multi-variable changes labeled "A/B test".** Three things differ → you can't attribute the lift. Force one-variable.
- **Optimizing open rate.** Apple MPP made it noise. Reply rate primary.
- **Calling winners early on small n.** n<50/arm = noise; n=200/arm starts being credible.
- **Stopping the moment significance crosses.** Peeking inflates false-positive rate. Pre-commit to a max-duration OR a minimum-n stop rule, then honor it.
- **Effect-size-blind significance.** "p<0.05 with 0.3pp lift" — significance + tiny effect = ship-worthless. Require both.
- **Allocation drift over time.** Hash-based allocation means same recipient gets same variant; if you change allocation mid-test, the data is contaminated.
- **Treating a 14d-inconclusive test as "no difference."** It might mean the effect is smaller than your MDE; surface the underpowered conclusion.
- **Comparing across campaigns.** Different audiences = different baselines = test contamination. Run within-campaign.
- **A/B/C/D tests with no plan.** Multi-variant tests need higher sample sizes; default to A/B until you have volume.
- **Send-time tests on open rate.** The classic Apple MPP failure mode. Send-time experiments only valid on reply rate.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (variant copy, recipients, metric values, dates, significance numbers) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Variant copy is `[user-provided]` (user designs); metric values are `[verified: campaign-management:run_<id>]`; never invent metrics.
- **Not feeding learnings to the library.** A winning opener angle should propagate to `cold-email-sequence` framework defaults; close the loop.

## Verification

Test is real when: pre-launch sample-size estimate documented; one-variable rule enforced (variant comparison shows ONE diff); allocation hash-based + reproducible; significance call references method + raw numbers + effect size; min-n + max-duration stop conditions honored; winner handoff to channel skill executed (or inconclusive default applied). Negative test: read the test design + result; can a colleague reproduce the analysis from the recorded inputs? If no, test rigor broke.

## Example

**User prompt:** "Test CCQ+Pain vs CCQ+Vision opener on our active WorkflowDoc cadence."
**What should happen:** Hypothesis: Vision-opener converts ≥3pp higher than Pain (low-volume regime). One variable: opener angle. Pre-launch: baseline reply rate 4% (from campaign history); expected campaign volume 300/arm over 14d → **low-volume regime** → Bayesian + `MIN_EFFECT_SIZE_PP=3.0`. (Frequentist 1pp would need ~6,700/arm — not available.) Surface to user: "We can detect ~3pp+ lifts directionally; sub-3pp differences will not be shippable from this volume." Test design: 50/50 split, hash-allocated, 14d max, primary metric reply rate. Launched via cold-email-sequence with allocation rule. D+10: arm A 4.1% (n=180, 7 replies); arm B 7.2% (n=180, 13 replies). Bayesian P(B>A) = 0.96 ≥ 0.85 ✓ (note: below industry-canonical 0.95; flag the gap to user); effect size 3.1pp ≥ regime MES of 3.0 ✓; min-n ≥50 ✓. Call winner B as a directional signal (low-volume regime). Ship 100% remaining traffic to B via cold-email-sequence handoff. Push test-result record. Recommend confirming the Vision-opener pattern across 2+ tests before promoting to `cold-email-sequence` framework defaults.

**User prompt:** "What sample size do I need to detect a 0.5pp lift on a 5% baseline?"
**What should happen:** Pre-launch MDE calc only. Output: for 0.5pp MDE on 5% baseline, 80% power, 5% alpha (two-proportion z-test) → **~31,195/arm (frequentist)**. Bayesian directional readouts could surface earlier but cannot ship a 0.5pp winner credibly. Surface: "Detecting <1pp lifts requires very high volume — 31k/arm is enterprise-only. For B2B sales-volume regimes, raise `MIN_EFFECT_SIZE_PP` to 1.0 or 3.0 and test for larger effects, OR aggregate across multiple campaigns." Recommend duration / volume / split needed.

**User prompt:** "Test running for 14d — call it."
**What should happen:** Pull cumulative metrics. n=85/arm. Bayesian P(B>A) = 0.71 (below 0.85 threshold). Min-n ≥50 met. Max duration reached. Call: inconclusive at the agreed thresholds. Action: ship variant A (control, default to higher-volume / safer); document inconclusive conclusion; flag underpowered-test for future ("this test needed n≥150/arm to detect 1pp; we got 85"). Recommend re-running with extended duration or pooling across similar campaigns.

## Linked Skills

- Test variants shipped via → `cold-email-sequence` / `linkedin-outreach` / `cold-calling` (channel skill)
- Test result triggers — `campaign-management` (swap-copy decision)
- Winning patterns feed → `cold-email-sequence` framework defaults (over time)
- Cross-campaign learnings → `kpi-reporting` (function-6)
- Refining ICP based on which audiences responded → `icp-refinement-loop` (function-6)

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-6-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Test design (at launch) | `interaction` (type: `research`) | `relevance` = hypothesis + variant ids + split + metrics + significance method + thresholds + max duration; `tags: "#ab-test-design #function-6"` |
| Test result (at call) | `interaction` (type: `research`) | `relevance` = method + cumulative n per arm + per-arm metrics + posterior/p-value + effect size + winner OR inconclusive; `tags: "#ab-test-result #function-6"` |
| Shipped-winner action | `interaction` (type: `research`) | `relevance` = winner variant + traffic-shift action + handoff to channel skill; `tags: "#ab-test-ship-winner #function-6"` |
| Inconclusive declaration | `interaction` (type: `research`) | `relevance` = test outcome + underpowered explanation + default action; `tags: "#ab-test-inconclusive #function-6"` |
| `[unverified — needs check]` (metric source uncertain) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #ab-testing-messaging"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
AB_TEST_BAYESIAN_THRESHOLD=0.85
AB_TEST_FREQUENTIST_P=0.05
AB_TEST_MIN_EFFECT_SIZE_PP=1.0
```

### Source tag

`source: "skill:ab-testing-messaging:v2.0.0"`

### Example push (test design at launch)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#ab-test-design #function-6",
    "relevance": "A/B test ab_t1_opener_2026-05-22 launched on campaign cmp_workflowdoc_t1_mc_2026-05-22. Hypothesis: Vision-opener converts ≥3pp higher than Pain. Regime: low-volume (<1,000/arm/14d). Variable: opener angle (variant A = CCQ+Pain, variant B = CCQ+Vision). Split: 50/50 hash-allocated. Primary metric: reply rate (Apple MPP-aware). Significance: Bayesian; winner threshold P(B>A)>0.85 (house default; 0.95 industry-canonical — gap flagged) AND effect ≥3pp (low-vol regime MES). Min n/arm: 50. Max duration: 14d. Pre-launch sample-size: 150/arm Bayesian sufficient for directional signal; frequentist 1pp would require ~6,700/arm and is not available.",
    "source": "skill:ab-testing-messaging:v2.0.0"
  }'
```

### Example push (winner called)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#ab-test-result #ab-test-ship-winner #function-6",
    "relevance": "A/B test ab_t1_opener_2026-05-22 result D+10. n=180/arm. Variant A (CCQ+Pain): 4.1% (7 replies). Variant B (CCQ+Vision): 7.2% (13 replies). Method: Bayesian (low-volume regime). Posterior P(B>A) = 0.96 ≥ 0.85 house threshold ✓ (note: below industry-canonical 0.95 — caveat surfaced to user). Effect size: 3.1pp ≥ regime MES 3.0 ✓. Min-n ≥50 ✓. WINNER (directional, low-vol regime): variant B (CCQ+Vision). Action: ship 100% remaining traffic to variant B via cold-email-sequence handoff. Recommend: confirm Vision-opener pattern across 2+ tests before promoting to cold-email-sequence framework defaults.",
    "source": "skill:ab-testing-messaging:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (variants) + `[verified: campaign-management:run_<id>]` (metrics) | Standard mapping. |
| `[unverified — needs check]` (metric source missing) | Pushes ONLY as `interaction:research` with `#unverified #review-required #ab-testing-messaging` tags; significance call deferred. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Test design rejected (multi-variable change) → push `#test-design-rejected` flag with reason; no test record.
- Test paused before min-n reached (campaign halt, infrastructure issue) → push pause record; no result push.
- Test inconclusive AND default action ambiguous → push inconclusive flag with manual decision needed.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
