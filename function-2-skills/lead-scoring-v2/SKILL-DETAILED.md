---
name: lead-scoring
description: Score each Lead record against the ICP scorecard from `icp-definition` plus BANT and CHAMP qualification frameworks plus a trigger-strength-and-recency formula, write the score + priority + tier + rationale directly onto the person record, and emit a per-run scoring interaction with the math. Use when sourced + enriched leads need outreach prioritization, when a discovery-call decision needs evidence-backed qualification, when the SDR/AE hand-off requires a 1-line tier label per record, or when the team wants the same 100-pt rubric applied retroactively to closed deals to validate ICP cutoffs.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, lead-scoring, qualification, bant, champ, function-2]
related_skills:
  - icp-definition
  - data-enrichment
  - lead-sourcing-apollo
  - lead-sourcing-clay
  - lead-sourcing-linkedin
  - lead-sourcing-web
  - icp-refinement-loop
  - pipeline-stages
inputs_required:
  - enriched-lead-records-from-data-enrichment-or-sourcing
  - icp-scorecard-rubric-from-icp-definition
  - tier-cutoffs-from-icp-definition
  - run-purpose-tag
  - bant-or-champ-data-availability-flags
deliverables:
  - per-lead-score-and-tier-and-priority
  - score-rationale-with-per-dimension-breakdown
  - bant-and-champ-status-per-record
  - tier-distribution-report
  - sales-accepted-lead-handoff-criteria-applied
  - scoring-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Lead Scoring

Score each enriched Lead against the 100-point ICP scorecard from `icp-definition`, layer in BANT (Budget, Authority, Need, Timing) and CHAMP (Challenges, Authority, Money, Prioritization) qualification, weight by trigger strength × recency, write the result directly onto the person record (`score`, `priority`, `icp_tier`), and emit a scoring run interaction with the full math. The output is what an SDR / AE accepts at the function-5 hand-off — a 1-line label they can act on without re-litigating the score.

> *The worked example uses a fictional product (BalanceBox) for illustration. The 100-pt scorecard, BANT, CHAMP, and trigger formulas are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Lead schema, source adapter contract, dedup, compliance, anti-fabrication tagging, push-to-CRM routing — live in `function-2-skills/function-2-conventions.md`. This skill assumes it.*

## Purpose

Sourcing produces a list, enrichment makes it usable, scoring makes it actionable. This skill closes the function-2 loop: every lead gets a deterministic score (100-pt ICP rubric), a qualification status (BANT + CHAMP), a tier (1/2/3/anti-ICP), a priority (hot/warm/cold), and a rationale paragraph the SDR can read in 10 seconds. The scoring math is reproducible — the same record scored next month against the same rubric gets the same score (modulo trigger decay), so re-scoring after re-enrichment yields a clean diff. Without this skill, sourced + enriched lists land in the CRM as undifferentiated rows; with it, they land as a triaged outreach queue.

## When to Use

- "Score these 326 enriched leads against our ICP."
- "Tier 1 / 2 / 3 our weekly sourcing batch."
- "We need an SAL hand-off for these 80 candidates."
- "Apply our 100-pt scorecard to the 25 leads I'm calling tomorrow."
- "Re-score the leads we sourced 60 days ago — triggers may have decayed."
- "Run the scorecard retroactively against closed-won deals to validate cutoffs."
- Pre-outreach prioritization after `data-enrichment`.
- Pre-discovery-call qualification snapshot.

### Do NOT use this skill when

- The records are unenriched (no verified email, no hook, no firmographic) — score will be artificially capped; run `data-enrichment` first.
- The ICP scorecard rubric doesn't exist — `icp-definition` is the prerequisite. Refuse to fabricate weights.
- The user wants to "just score one lead manually" — overkill; use the rubric directly.
- The list has fewer than ~10 records and the user is in the room with them — manual judgment is faster.
- The intent is to score across categories the rubric doesn't cover (intent-data signals, account-based scoring) — extend `icp-definition` first; don't introduce ad-hoc dimensions.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Enriched Lead records | yes | `data-enrichment` output (or sourcing skill if scoring without enrichment, with `confidence: low`) | Records must conform to function-2 Lead schema. |
| 2 | ICP scorecard rubric | yes | `icp-definition-v2` output | 100-pt weighted dimensions (Pain / Trigger / WTP / Reach / TTV / Strategic) + tier cutoffs. |
| 3 | Tier cutoffs | yes (default Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10; T1 ≥75 / T2 55–74 / T3 40–54 / Anti-ICP <40) | `icp-definition` or user override | The skill reads from the ICP one-pager; user overrides allowed but logged. |
| 4 | Run purpose tag | yes | user | Stamped on every record's scoring run. |
| 5 | BANT / CHAMP data availability flags | yes | user / records | Booleans: `bant_data_present` / `champ_data_present`. If false, BANT/CHAMP fields populated as `unknown` and flagged for hand-off conversation. |
| 6 | Trigger decay overrides (optional) | no | user | "Treat all triggers as fresh (no decay)" — for retroactive scoring of closed deals where decay is irrelevant. |

### Fallback intake script

> "Scoring needs the ICP scorecard from `icp-definition` plus enriched records from `data-enrichment`. If either is missing, the score will be artificially capped or hypothesis-only.
>
> Two questions:
> - Do you have BANT / CHAMP data captured per lead (recent discovery calls, intent signals)? If not, those dimensions will be `unknown` and flagged for the SDR conversation.
> - Run purpose tag for this batch?"

### Input validation rules

- Records absent → block; nothing to score.
- ICP scorecard absent → refuse to fabricate weights; recommend `icp-definition` first; offer to produce a placeholder rubric clearly labeled `[hypothetical]` for hypothesis-mode runs only.
- Records lack required fields (e.g. no `company_size_band`, no `signals`, no `email_status`) → score-cap that lead at 60/100 (Tier 2 max) and flag the missing field.
- Tier cutoffs differ from ICP one-pager → log the override; warn user.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **100-point ICP weighted scorecard** (house-built) | Crewm8, codified in `icp-definition` | Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10 = 100. The rubric weights are owned by `icp-definition`; this skill *applies* them and trusts that ownership. |
| **BANT** (1950s, popularized by IBM Sales School) | IBM Corporation — sales training curriculum, 1950s/60s; widely attributed to IBM, no single author | Budget / Authority / Need / Timing. The original 4-question qualifier; still a clean mental shortcut for SDR triage. Each dimension has 3 states: `confirmed` / `inferred` / `unknown`. |
| **CHAMP** (~2014) | InsightSquared (Zorian Rotenberg + colleagues) | Challenges / Authority / Money / Prioritization. Reorders BANT to lead with pain (Challenges) rather than budget — better for buyer-led sales motions. Same 3-state schema. The skill runs both BANT and CHAMP because they surface different gaps in the qualification picture. |
| **Trigger strength × recency formula** (house-built) | Crewm8 | The 20-pt Trigger dimension in the rubric is decomposed: `trigger_score = base_strength × decay(days_since_event, half_life)`. A `strong` funding event from 11 months ago scores `strong (0.9) × decay(330d, 365d) = 0.9 × 0.10 = 0.09 → ~2/20`. Without decay, stale facts inflate scores. |
| **Sales-Accepted-Lead handoff criteria** (industry-standard, codified by SiriusDecisions and Aberdeen Group ~2010) | SiriusDecisions / Forrester | Output passes the SAL bar when: ICP fit confirmed, trigger present, decision-maker identified, no hard disqualifiers. The SDR / AE accepts or rejects based on these gates; this skill makes acceptance evidence explicit. |

## Tools and Sources

This skill is pure compute — it does not call external APIs. Its inputs are:
- **Lead records** (in-memory or read from CRM via `GET /api/people?...`).
- **ICP scorecard JSON** (from `icp-definition` artifact).
- **CRM PATCH** target (`POST /api/push` with the same dedup keys updates existing person records).

### Source priority rule

For any field used in scoring: **enriched + verified provenance** > **sourced + verified** > **enriched + user-provided** > **sourced + user-provided** > **`[unverified — needs check]`**. Records keyed off `[unverified]` fields score-cap; never score off `[hypothetical]`.

## Procedure

### 1. Validate inputs

Confirm Lead records have required fields (per conventions §1) and ICP scorecard rubric is loaded. Flag any records where critical fields are `[unverified — needs check]` — they will score-cap. **Rationale**: scoring-on-fabrications produces fabricated tiers; the validation step is the firewall.

### 2. Apply the 100-pt scorecard per dimension

For each lead, compute each of the 6 weighted dimensions:

- **Pain (25 pts)**: How acute is the pain this product solves for this contact? Drawn from `signals[]` and `personalization_hook` (which encodes a recent pain or trigger). Rubric per `icp-definition`'s P-T-O chain.
- **Trigger (20 pts)**: Apply the trigger-strength × recency formula. Sum across active signals; cap at 20.
- **WTP / ACV match (20 pts)**: Does company size + funding stage + revenue band suggest fit with the product's price point? Off the firmographic.
- **Reach (15 pts)**: Email verified? Phone? LinkedIn URL? Multiple channels? Each adds points up to 15.
- **TTV / Time-to-value (10 pts)**: Does the contact's role + company stage suggest a fast or slow path to value? (Buyer + low-friction stack = high; IT-led buying + entrenched contract = low.)
- **Strategic (10 pts)**: Logo value, vertical anchoring, follow-on sale potential. Drawn from named-account list or expansion patterns.

Per-dimension rationale written as a one-liner ("Pain 22/25: hook references RFP issuance with submission deadline within 30 days — acute"). **Rationale**: each dimension is auditable; "score: 78" without breakdown is opaque.

### 3. Apply BANT

For each lead, populate:
- **Budget**: `confirmed` (explicit budget signal, e.g. RFP), `inferred` (firmographic suggests spend capacity), `unknown`.
- **Authority**: `confirmed` (decision-maker by title), `inferred` (champion in role with influence), `unknown`.
- **Need**: `confirmed` (signal explicit pain), `inferred` (firmographic + trigger pattern), `unknown`.
- **Timing**: `confirmed` (deadline visible — RFP submission, audit cycle), `inferred` (trigger event recent), `unknown`.

A BANT-rich record where all four are `confirmed` gets a +5 score boost (capped at 100); 3+ confirmed = +3; mostly inferred = no boost; mostly unknown = -5 penalty.

### 4. Apply CHAMP (in parallel)

Same three-state schema, different framing:
- **Challenges**: pain validation (overlaps Need but framed as articulated problem).
- **Authority**: same as BANT.
- **Money**: same as Budget.
- **Prioritization**: timing in buyer's language ("we're solving this in Q2").

CHAMP often surfaces gaps BANT hides: `Need: confirmed` but `Prioritization: unknown` means the buyer agrees they have the problem but isn't actively solving — important nuance for cadence selection.

### 5. Compute final score and tier

`final_score = scorecard_total + bant_adjustment` (capped at 100). Apply tier cutoffs from `icp-definition`:
- ≥ T1 cutoff → `tier-1`, `priority: hot`
- T2 range → `tier-2`, `priority: warm`
- T3 range → `tier-3`, `priority: cold`
- < T3 cutoff → `anti-icp`, `priority: cold`, flag for nurture or disqualification

### 6. Apply Sales-Accepted-Lead criteria

For Tier-1 records, run the SAL gates:
- ICP fit confirmed (scorecard ≥ 75) ✓
- Trigger present and within half-life ✓
- Decision-maker or champion identified (BANT Authority ≥ inferred) ✓
- No hard disqualifiers (anti-ICP firmographic match, DNC phone-only contact, role-based email) ✓

Records passing all 4 gates → `sal_eligible: true`. Records failing any → flag the failed gate; don't strip the Tier-1 status (still high-priority) but warn at hand-off.

**Rationale**: SAL is the contract between SDR and AE; making the contract visible per record cuts hand-off friction.

### 7. Surface tier distribution report

Aggregate counts: how many T1 / T2 / T3 / Anti-ICP. Flag if distribution is suspicious — e.g. 80% T1 means the rubric is too lenient or the source pre-filtered (re-tune); 5% T1 means the source is wide (loosen filters or re-source). **Rationale**: distribution shape is the QA signal for the scoring + sourcing pipeline.

### 8. Score-rationale write per record

For each record, compose a 2–3-sentence rationale: top 3 contributing dimensions, 1 weakness if any, recommended next step. The SDR reads this in 10 seconds at hand-off. **Rationale**: opaque scores get re-litigated; transparent scores get acted on.

### 9. PATCH the person record + emit run interaction

Push per §9 of conventions: PATCH `score`, `priority`, `tier` tags onto the existing `person` record. Emit one `interaction:research` per scoring run (full math + per-dimension breakdown + tier distribution + SAL eligibility per Tier-1). Records that were `[unverified — needs check]` going in stay routed to review queue.

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  inputs:
    record_count: <int>
    upstream_run_ids: [<sourcing run, enrichment run, ...>]
    icp_scorecard_version: <from icp-definition artifact>
  rubric:
    weights: { pain: 25, trigger: 20, wtp: 20, reach: 15, ttv: 10, strategic: 10 }
    tier_cutoffs: { t1: 75, t2: 55, t3: 40 }
  bant_data_available: <bool>
  champ_data_available: <bool>
  decay_applied: <bool>
  tier_distribution:
    tier_1: <int>
    tier_2: <int>
    tier_3: <int>
    anti_icp: <int>
  sal_eligible_count: <int>
  warnings:
    - <e.g. "60% T1 — re-tune rubric or check source pre-filter">
    - <e.g. "30% records score-capped due to [unverified] fields — re-enrich first">
  next_skill_recommendation: <multi-channel-cadence | data-enrichment-recapture | icp-refinement-loop | etc.>

leads_patched:
  - lead_id: <uuid>
    person_dedup_key: <linkedin_url or email>
    score: <int 0-100>
    priority: hot | warm | cold
    icp_tier: tier-1 | tier-2 | tier-3 | anti-icp
    sal_eligible: <bool>
    score_rationale_short: "<2–3 sentences for hand-off>"
    score_rationale_full:
      pain: "{pts}/25 — {detail}"
      trigger: "{pts}/20 — {detail with decay math}"
      wtp: "{pts}/20 — {detail}"
      reach: "{pts}/15 — {detail}"
      ttv: "{pts}/10 — {detail}"
      strategic: "{pts}/10 — {detail}"
      bant_adjustment: "{+/- pts}"
    bant_status:
      budget: confirmed | inferred | unknown
      authority: <...>
      need: <...>
      timing: <...>
    champ_status:
      challenges: <...>
      authority: <...>
      money: <...>
      prioritization: <...>
    score_freshness_date: <ISO>
```

## Worked Example

> *All entities below are tagged `[hypothetical]` — fictional, illustrative.*

**User prompt**: "Score these 80 enriched leads from a recent BalanceBox [hypothetical] sourcing run. ICP from icp-definition. BANT data partial — we have firmographic + trigger but no discovery-call notes."

**Step 1 — Validate inputs**: 80 records loaded; ICP scorecard loaded (BalanceBox: FP&A automation; Tier-1 cutoff 75; Pain/Trigger/WTP/Reach/TTV/Strategic = 25/20/20/15/10/10). 12 records have `[unverified — needs check]` on at least one critical field → flagged for score-cap.

**Step 2 — Apply 100-pt scorecard per dimension**: For one record:
```yaml
contact_name: "Esme Liang" [hypothetical]
title: "VP Finance Operations"
company: "Forge Robotics" [hypothetical]
company_size_band: "201-500"
company_funding_stage: "series-c"
signals:
  - type: leadership-change
    detail: "VP Finance hired 60d ago"
    date: 2026-03-04
    strength: strong
    half_life_days: 90
personalization_hook:
  text: "Esme started as VP Finance Ops 2026-03-04 (60d); LinkedIn hire announcement public."

scoring breakdown:
  pain: 18/25  ("VP Finance arrival typically triggers FP&A tooling review within 90d — supported by ICP P-T-O")
  trigger: 12/20  (strong (0.9) × decay(60d, 90d) = 0.9 × 0.33 = 0.30 → 6/20 raw; +6 boost for 'within window of FP&A tooling decision' = 12/20)
  wtp: 16/20  (Series C, 201-500 emp, ICP ACV band $40-80k matches stage spend)
  reach: 13/15  (email verified, LinkedIn verified, phone unverified)
  ttv: 8/10  (new VP = high-friction Q1, but typical FP&A decision velocity at this size = medium-fast)
  strategic: 5/10  (mid-market not strategic; some logo value)
  raw_total: 72
  bant_adjustment: -2  (BANT-thin: budget unknown, authority confirmed, need inferred, timing inferred)
  final_score: 70
  tier: tier-2
  priority: warm
```

**Step 3 — BANT**:
- budget: unknown (no discovery; firmographic suggests yes but unconfirmed)
- authority: confirmed (VP Finance Ops = decision-maker)
- need: inferred (post-hire FP&A tooling pattern)
- timing: inferred (60d into role, typical 30–90d window for tooling decisions)

**Step 4 — CHAMP**:
- challenges: inferred (same as Need)
- authority: confirmed
- money: unknown
- prioritization: unknown (no signal on whether FP&A is in Esme's first-90-day priorities)

**Step 5 — Score / tier**: 70 → tier-2 / warm.

**Step 6 — SAL check**: not Tier-1, so SAL gates not run; flagged for `priority: warm` cadence.

**Step 7 — Tier distribution** (across all 80):
- tier-1: 14 (17.5%) ← SAL-eligible: 11
- tier-2: 32 (40%)
- tier-3: 24 (30%)
- anti-icp: 10 (12.5%)
Distribution healthy — Tier-1 ratio in 10–20% target band.

**Step 8 — Score rationale per record (Esme)**:
> "Tier 2 / 70 / warm. New VP Finance Ops at Series C robotics co (60 days into role, public hire announcement). FP&A tooling typically reviewed within 90 days of VP arrival — narrowing trigger window. Verified email + LinkedIn; budget and prioritization unknown — recommend warm SDR outreach with discovery focus on Q2 priorities."

**Step 9 — Push**: PATCH 80 person records with `score`, `priority`, tier tag (`#icp-tier-2` etc.); 1 interaction:research run record with full math for all 80; 12 leads (the score-capped ones) routed to review queue with `[unverified — needs check]` retained.

Run summary:
```
BalanceBox Lead Scoring Run [hypothetical]
Run ID: score_2026-05-04_e8r
Inputs: 80 records (from enrich_2026-05-04_b3, source: lead-sourcing-clay)
Rubric: ICP v2.0.0 (Pain 25/Trig 20/WTP 20/Reach 15/TTV 10/Strat 10; T1 75/T2 55/T3 40)
Tier distribution: 14 T1 (17.5%) / 32 T2 / 24 T3 / 10 Anti-ICP
SAL-eligible (T1 passing 4-gate): 11
BANT data: partial (firmographic + trigger; no discovery)
Score-capped due to [unverified] fields: 12 (routed to review queue)
Recommended next: multi-channel-cadence for the 11 SAL records (function-3); data-enrichment-recapture for the 12 capped; icp-refinement-loop after 30+ closed deals
```

## Heuristics

- **Trust the ICP rubric weights; tune them in `icp-definition`, not here.** Ad-hoc adjustments inside scoring drift the rubric across runs.
- **Score-cap on `[unverified]` is a feature.** It surfaces enrichment debt; don't bypass.
- **BANT-thin records are not low-quality records — they're gaps.** Missing BANT data is information about the SDR conversation, not the lead.
- **Trigger decay is non-negotiable.** A funding signal from 11 months ago scoring like a fresh one is the most common scoring failure mode.
- **Tier distribution shape is the rubric audit.** 10–20% T1 is healthy for a well-tuned sourcing+scoring pipeline. Outside that band, fix the rubric or the source.
- **Re-score after 60 days.** Triggers decay; titles change; emails go stale. The same record scored next quarter should score lower if nothing else changed (decay).
- **Anti-ICP is not the same as "low score."** Anti-ICP means *active disqualification* — a firmographic the rubric flags out. A Tier-3 score is "fits, but barely"; Anti-ICP is "explicitly reject."
- **Don't score across rubrics in one run.** If two product lines have different ICPs, run scoring twice; never blend rubrics within a record set.
- **CHAMP catches what BANT misses.** A record with `Need: confirmed` but `Prioritization: unknown` is a "they agree they have the problem but aren't doing anything about it" — different cadence than full BANT.
- **The hand-off rationale is the deliverable.** SDRs who can't read a score in 10 seconds will substitute their own intuition; the rationale paragraph is the contract.

## Edge Cases

- **No ICP scorecard.** Refuse to fabricate weights. Recommend `icp-definition` first. Or, if user insists on hypothesis-mode, produce a placeholder rubric labeled `[hypothetical]` and tier all records `[hypothetical]` until grounded.
- **Records all from the same source / single segment.** Tier distribution will skew. Surface it; don't auto-tune.
- **Closed-won retroactive scoring.** Use freshness-override to disable trigger decay (the trigger that prompted the deal is by definition relevant). Compare scores against tier cutoffs; if won deals score <55, the cutoffs are wrong (re-tune in `icp-definition`).
- **Multi-segment ICP.** Run scoring once per segment with the segment's rubric; merge results with segment-tag preserved.
- **PLG product (sales motion).** ICP rubric weights shift toward TTV + Reach (low-friction adoption matters more than budget). Should be encoded in `icp-definition`'s rubric; this skill applies.
- **Account-based scoring (one score per company across multiple contacts).** Aggregate per-contact scores up to company-level (max or weighted-average); document the aggregation rule.
- **Records with Tier-1 firmographic but no trigger.** They get Pain + WTP + Reach + Strategic but Trigger = 0; usually lands T2 (55–74). Flag as "fit-no-trigger" — these are nurture candidates, not active outreach.
- **Records with strong trigger but Anti-ICP firmographic.** Trigger of 18/20 + Pain 5/25 + WTP 0/20 = ~23. Stays Anti-ICP. Trigger doesn't override firmographic exclusion.
- **Records with verified email but no signals at all.** Pain/Trigger/Strategic all 0; Reach high; net ~25. Tier-3. Flag as "list pad" — usually evidence the source pulled too wide.
- **BANT/CHAMP all `unknown`.** -5 adjustment lands on top of base score. Many records here = SDR discovery conversation hasn't happened yet (normal for fresh sourcing).

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| ICP scorecard missing | rubric load fails | Refuse to fabricate; recommend `icp-definition`; offer hypothesis-mode with `[hypothetical]` tier tags. |
| Records missing required fields (e.g. no signals) | per-dimension fields default to 0 | Score-cap at 60; flag missing field; route to `data-enrichment` or `lead-sourcing-*` for re-enrichment. |
| Tier distribution wildly skewed (>50% T1 or <2%) | rubric mismatched to source | Surface; recommend rubric re-tune (back to `icp-definition`); do not auto-adjust. |
| Trigger decay produces near-zero scores | source delivered stale leads | Surface; recommend re-source from `lead-sourcing-*` for fresher triggers. |
| BANT-rich data conflicts with scorecard (BANT high, score low) | discovery-call notes vs static rubric mismatch | Trust the rubric; flag the conflict in rationale; recommend rubric review. |
| Push to CRM PATCH fails (4xx/5xx) | network or token | Persist scoring output to local JSON; retry on user request. |
| `[unverified]` field count >60% | enrichment incomplete | Recommend re-running `data-enrichment` before scoring rather than scoring-then-fixing. |
| User requests rubric override mid-run | inconsistent state | Log override; warn; complete current run; recommend updating `icp-definition` for next run rather than per-run overrides. |
| Same lead scored twice with different inputs | conflicting scores in history | Latest run wins on PATCH; preserve all runs as `interaction:research`; surface diff in run summary. |
| Score drift on re-run with same inputs | nondeterminism | Skill is deterministic by design — investigate; usually means input record's `signals[].date` was updated upstream (decay shifted). |

## Pitfalls

- **Scoring `[unverified]` records as if they were verified.** Score-cap is the feature; never bypass.
- **Tuning rubric weights inside the scoring run.** That's `icp-definition`'s job. Drift across runs ruins comparability.
- **Ignoring trigger decay.** A "raised Series B 14 months ago" record scoring 80 means the decay function isn't running.
- **Using the score as a fact rather than evidence.** Score is a snapshot; the rationale is the evidence. Hand-off conversations should reference rationale, not "the agent said 87."
- **Treating Tier-1 count as a target.** Adjusting rubric to "produce more T1" is rubric corruption. T1 ratio is an output, not an input.
- **Skipping the SAL gate for Tier-1.** Tier-1 by score doesn't mean SAL-ready; the 4-gate check is the contract.
- **Mixing rubrics across product lines.** Each ICP gets its own scoring run; never blend.
- **Scoring without enrichment.** Cap-driven artifacts everywhere; recommend enrichment first.
- **Aggregating account-level scores without documenting the rule.** Max? Weighted average? Most-senior-contact only? Pick one and write it down.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (contact names, signals cited in rationale, dates, dollar figures) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Score rationales reference the *signals on the record* — never invent a "saw their funding announcement" detail to justify a score; if the signal isn't in the record, it doesn't enter the rationale.
- **Scoring run without a purpose tag.** Cost-per-lead and channel-performance attribution downstream (function-6) needs the tag.

## Verification

The scoring run is real when: (a) re-running the same record set with the same rubric produces the same scores ± trigger-decay drift; (b) every score has a rationale paragraph that references the actual record's signals (no invented details); (c) tier distribution shape is justified by the source — sourcing skill output and scoring tier ratios are coherent; (d) SAL eligibility per Tier-1 is computed and the failed-gate (if any) is named; (e) re-running without changes 30 days later shows lower scores on records with decaying triggers (decay is working); (f) the rubric weights match `icp-definition`'s artifact verbatim.

## Done Criteria

1. Inputs validated; ICP scorecard rubric loaded; record schema confirmed.
2. 100-pt scorecard applied per dimension per record with auditable per-dimension rationale.
3. BANT and CHAMP populated (both, in parallel) per record.
4. Trigger decay applied to all signals (or override logged).
5. Final score, tier, priority computed per record using `icp-definition`'s tier cutoffs.
6. SAL gates run on every Tier-1 record; eligibility surfaced.
7. Tier distribution reported and sanity-checked; warnings for outliers surfaced.
8. PATCH per record successful; run interaction emitted with full math.
9. Records with `[unverified — needs check]` fields are score-capped and routed to review queue, NOT pushed as scored persons.

## Eval Cases

### Case 1 — full BANT, ICP-grounded, fresh enrichment

Input: 50 enriched records from `data-enrichment`; ICP scorecard exists; BANT data captured from recent discovery calls; all fields verified.

Expected: tier distribution within 10–20% T1 / 30–45% T2 / 25–35% T3 / 5–15% Anti-ICP; 0 records score-capped; SAL eligibility computed per Tier-1; per-record rationale 2–3 sentences referencing actual signals.

### Case 2 — BANT-thin, fresh sourcing, no discovery yet

Input: 200 records straight from `lead-sourcing-apollo` + `data-enrichment`; ICP scorecard exists; no discovery call data → BANT/CHAMP mostly `unknown`.

Expected: BANT-adjustment generally negative (-3 to -5 per record); tier distribution shifted slightly downward (more T2/T3, fewer T1); rationale flags "BANT-thin — recommend SDR discovery to confirm Authority + Timing"; SAL eligibility lower than Case 1.

### Case 3 — ICP-ungrounded hypothesis mode

Input: records sourced; ICP scorecard does NOT exist (user skipped `icp-definition`).

Expected: skill REFUSES standard scoring; offers hypothesis-mode placeholder rubric labeled `[hypothetical]`; if user accepts, all records tagged `[hypothetical]` tier; output flagged `confidence: low` and `ICP-ungrounded: true`; recommends `icp-definition` as prerequisite for real scoring.

### Case 4 — retroactive scoring of closed-won deals

Input: 30 closed-won deal records (have full firmographic + trigger history); freshness-override set to disable decay.

Expected: scores cluster ≥ T1 cutoff (>75) — if not, the cutoff is wrong; recommend `icp-refinement-loop` to re-tune. Surface any won deals scoring <55 (Tier-3) — the rubric would have rejected this customer; high-value miss for ICP refinement.

### Case 5 — re-scoring after 60 days (decay test)

Input: same 100 records scored 60 days ago, no enrichment changes.

Expected: scores generally lower by 3–8 points (trigger decay); records that were T1 with old triggers may drop to T2; surface decay impact in run summary; recommend re-sourcing for fresh triggers.

## Guardrails

### Provenance (anti-fabrication)

Per §8 of conventions: scoring is pure compute; provenance discipline applies to score *justifications* — every signal cited in a rationale paragraph must exist in the record's `signals[]`. Never invent a signal to justify a score. `[unverified]` fields cause score-cap, not score-bypass. Worked-example fictional entities tagged inline.

### Evidence

Every score has per-dimension rationale; every rationale clause references a record field. Re-runs are deterministic (modulo decay) — non-determinism is a bug.

### Scope

This skill scores. It does NOT enrich (that's `data-enrichment`), source (`lead-sourcing-*`), write outreach (function-3), or re-tune the rubric (`icp-definition` / `icp-refinement-loop`). Avoid scope creep.

### Framing

Per-record rationales use plain operational language readable in 10 seconds. Run summary uses operational language with tier-distribution audit.

### Bias

Scoring inherits ICP rubric bias (the rubric weights are choices). Surface tier-distribution shape so bias is visible. Never auto-tune to flatter a sourcing run.

### Ethics

Scoring records pulled from sources with provenance baggage (e.g. paywall-bypassed scrapes) inherits that baggage; the skill won't fix upstream compliance issues but won't hide them either — score-cap and route to review.

### Freshness

Trigger decay is built in. Score-freshness-date stamped per record. Re-score recommended after 60 days or material change.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Tier-1 records SAL-eligible, ready for outreach | `multi-channel-cadence` (function-3, future) | Tier-1 records + score rationale + cadence template |
| Tier-2 / Tier-3 nurture queue | `cold-email-sequence` (function-3, future) | Records + Pain/Trigger language for opener |
| Score-capped records (need re-enrichment) | `data-enrichment` | Records + missing-fields list |
| Tier distribution warning (re-tune rubric) | `icp-definition` | Distribution shape + rubric override log |
| ≥30 closed deals — refresh ICP cutoffs | `icp-refinement-loop` (function-6, future) | Won/lost deal scoring runs + cutoff drift |
| Anti-ICP records | (no further action) | Tag for nurture-only or disqualification list |
| Lead pipeline stage progression | `pipeline-stages` (function-5, future) | SAL-eligible records → "Sales Accepted" stage |

## Push to CRM

After scoring, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push` (PATCH semantics — push API auto-merges by dedup key). Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Score + priority + tier per existing person | `person` (PATCH via dedup key) | `score` (1-5 or 0-100 per agentic-app convention), `priority` (hot/warm/cold), `tags` updated to include `#icp-tier-1` / `#icp-tier-2` / etc. and `#sal-eligible` for Tier-1 passing gates |
| Score rationale per record | `interaction` (type: `research`) | `relevance` = 2–3 sentence rationale + per-dimension breakdown; `tags: "#scoring-rationale #function-2"` |
| Run record (rubric, distribution, warnings) | `interaction` (type: `research`) | `relevance` = run summary + tier distribution + SAL count; `tags: "#scoring-run #function-2"` |
| Score-capped records (`[unverified]` blockers) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #lead-scoring"`; person record NOT patched |

### Score field convention

agentic-app's push API supports `score` as 1–5. The 100-pt scorecard maps:
- 75–100 → score: 5 (Tier-1)
- 55–74 → score: 4 (high Tier-2) / 3 (low Tier-2)
- 40–54 → score: 2 (Tier-3)
- <40 → score: 1 (Anti-ICP)

The full 0–100 score is preserved verbatim in the score-rationale interaction.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

(No external API keys needed — pure compute.)

### Source tag

`source: "skill:lead-scoring:v2.0.0"`

### Example push (PATCHed person + rationale interaction)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Forge Robotics",
    "contactName": "Esme Liang",
    "contactEmail": "esme@forge-robotics.com",
    "score": 3,
    "priority": "warm",
    "tags": "#icp-tier-2 #scored #bant-thin #function-2",
    "relevance": "Tier 2 / 70 / warm. New VP Finance Ops at Series C robotics co (60 days into role, public hire announcement). FP&A tooling typically reviewed within 90 days of VP arrival — narrowing trigger window. Verified email + LinkedIn; budget and prioritization unknown — recommend warm SDR outreach with discovery focus on Q2 priorities. (Pain 18/Trigger 12/WTP 16/Reach 13/TTV 8/Strategic 5; BANT -2.)",
    "source": "skill:lead-scoring:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#scoring-run #function-2",
    "relevance": "Lead scoring run score_2026-05-04_e8r. Inputs: 80 records (from enrich_2026-05-04_b3, source: lead-sourcing-clay). Rubric: ICP v2.0.0 (Pain 25/Trig 20/WTP 20/Reach 15/TTV 10/Strat 10; T1 75/T2 55/T3 40). Tier distribution: 14 T1 (17.5%) / 32 T2 / 24 T3 / 10 Anti-ICP. SAL-eligible: 11 of 14 T1 (3 failed reachability gate). BANT data: partial. Score-capped due to [unverified] fields: 12 (routed to review queue). Decay applied. Recommended next: multi-channel-cadence for 11 SAL records; data-enrichment-recapture for 12 capped.",
    "source": "skill:lead-scoring:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §8.2:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | PATCH per the standard mapping (score lands on existing person record). |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #lead-scoring` tags. Person record is NOT patched — score stays unset. |
| `[hypothetical]` | Does NOT push (hypothesis-mode runs surface output to user but do not write to CRM). |

Example unverified-cap push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #lead-scoring #score-capped",
    "relevance": "Score-capped at 60 (Tier 2 max) for record [unverified — needs check] — email_status: unverified AND personalization_hook: null. Cannot confidently apply Pain/Reach dimensions without enrichment. Re-run lead-scoring after data-enrichment completes for this record.",
    "source": "skill:lead-scoring:v2.0.0"
  }'
```

### When NOT to push

- Run produced 0 scored records (all blocked / score-capped) — push run record with `#all-capped` tag; no person PATCH.
- ICP-ungrounded hypothesis mode — surface to user but do not push (hypothetical scores would pollute CRM).
- `[unverified — needs check]` — see provenance routing; person not patched.
- `[hypothetical]` — never.
- Run flagged "rubric mismatch" warning — push run record but flag user to review distribution before downstream skills consume.
- Score-only delta from previous run (nothing changed) — push only the run record showing "no-op"; skip per-record PATCH.
