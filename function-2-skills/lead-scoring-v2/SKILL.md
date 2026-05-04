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

Score each enriched Lead against the 100-point ICP scorecard from `icp-definition`, layer in BANT (Budget, Authority, Need, Timing) and CHAMP (Challenges, Authority, Money, Prioritization) qualification, weight by trigger strength × recency, write the result directly onto the person record (`score`, `priority`, `icp_tier`), and emit a scoring run interaction with the full math.

> *Worked example uses BalanceBox [hypothetical] (fictional); procedure is vertical-agnostic. Shared rules in `function-2-skills/function-2-conventions.md`.*

## Purpose

Sourcing produces a list, enrichment makes it usable, scoring makes it actionable. This skill closes the function-2 loop: every lead gets a deterministic score (100-pt ICP rubric), a qualification status (BANT + CHAMP), a tier (1/2/3/anti-ICP), a priority (hot/warm/cold), and a rationale paragraph the SDR can read in 10 seconds. Scoring math is reproducible — re-scoring yields a clean diff. Without this, lists land as undifferentiated rows; with it, as a triaged outreach queue.

## When to Use

- "Score these 326 enriched leads against our ICP."
- "Tier 1 / 2 / 3 our weekly sourcing batch."
- "We need an SAL hand-off for these 80 candidates."
- "Re-score the leads we sourced 60 days ago — triggers may have decayed."
- "Run the scorecard retroactively against closed-won deals to validate cutoffs."
- Pre-outreach prioritization after `data-enrichment`; pre-discovery-call qualification snapshot.

## Inputs Required

1. **Enriched Lead records** from `data-enrichment` (or sourcing with `confidence: low` if no enrichment).
2. **ICP scorecard rubric + tier cutoffs** from `icp-definition` (default: Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10 = 100; T1 ≥75 / T2 55–74 / T3 40–54 / Anti-ICP <40). Refusal to fabricate weights — `icp-definition` is a hard prerequisite.
3. **Run purpose tag** — short string for cost attribution + replay.
4. **BANT / CHAMP data availability flags** — booleans for whether discovery-call data exists. If false, those dimensions populate as `unknown` and flag for SDR conversation.
5. (Optional) Trigger decay overrides for retroactive scoring of closed deals.

## Quick Reference

| Concept | Value |
|---|---|
| **Rubric weights** | Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10 = 100 |
| **Tier cutoffs** | T1 ≥75, T2 55–74, T3 40–54, Anti-ICP <40 |
| **Trigger formula** | `trigger_score = base_strength × decay(days_since_event, half_life)` |
| **BANT / CHAMP** | Each dimension: `confirmed | inferred | unknown`. BANT adj: 4 confirmed +5; 3+ +3; mostly unknown −5 |
| **SAL gates (Tier-1)** | ICP fit + trigger present + decision-maker IDed + no hard disqualifiers |
| **Score-cap rule** | `[unverified — needs check]` field → cap at 60 (Tier-2 max), route to review |
| **Healthy distribution** | 10–20% T1 / 30–45% T2 / 25–35% T3 / 5–15% Anti-ICP |
| **Re-score cadence** | After 60 days OR material new signal |
| **agentic-app score mapping** | 75–100 → 5; 55–74 → 4 or 3; 40–54 → 2; <40 → 1 |

## Procedure

### 1. Validate inputs
Confirm Lead records have required fields and ICP scorecard is loaded. Flag records with `[unverified]` critical fields — they will score-cap.

### 2. Apply 100-pt scorecard per dimension
Compute each weighted dimension per record: Pain (P-T-O chain), Trigger (strength × decay), WTP (firmographic + funding), Reach (verified email/phone/linkedin), TTV (role + stage + stack friction), Strategic (logo, vertical anchor). Per-dimension rationale one-liner.

### 3. Apply BANT and CHAMP (in parallel)
Populate Budget/Authority/Need/Timing AND Challenges/Authority/Money/Prioritization per record (each `confirmed | inferred | unknown`). Apply BANT adjustment to base score. CHAMP often surfaces gaps BANT hides — `Need: confirmed` but `Prioritization: unknown` is critical for cadence selection.

### 4. Compute final score, tier, priority
`final_score = scorecard_total + bant_adjustment` (capped 100). Apply tier cutoffs from `icp-definition` to derive tier and priority (hot/warm/cold).

### 5. Apply Sales-Accepted-Lead criteria (Tier-1 only)
Check 4 gates: ICP fit ≥75 / trigger within half-life / decision-maker identified / no hard disqualifiers. Pass all → `sal_eligible: true`. Fail any → flag the failed gate; don't strip Tier-1 status.

### 6. Tier distribution + per-record rationale
Aggregate tier counts; flag suspicious distribution (>50% T1 = rubric too lenient; <2% T1 = source too wide). For each record compose 2–3 sentence rationale: top 3 dimensions, 1 weakness, recommended next step.

### 7. PATCH person + emit run interaction
Push per conventions §9: PATCH `score`, `priority`, tier tags onto person. Emit one `interaction:research` per run with full math, tier distribution, SAL eligibility. `[unverified]` records to review queue.

## Output Format

- PATCHed person records: `score`, `priority`, `icp_tier` tag, `sal_eligible` flag (Tier-1)
- Per-record rationale (short hand-off version + full per-dimension breakdown)
- BANT + CHAMP status per record
- Tier distribution report with sanity-check warnings
- Run record: rubric version, distribution, SAL count, score-capped count, decay flag, next-skill recommendation
- Review queue: score-capped records as `interaction:research`

## Done Criteria

1. Inputs validated; ICP scorecard rubric loaded; trigger decay applied (or override logged).
2. 100-pt scorecard applied per dimension with auditable rationale; BANT and CHAMP populated in parallel.
3. Final score, tier, priority computed using `icp-definition`'s tier cutoffs.
4. SAL gates run on every Tier-1 record; eligibility surfaced.
5. Tier distribution reported and sanity-checked.
6. PATCH per record successful; run interaction emitted with full math.
7. `[unverified]` records score-capped and routed to review queue, NOT pushed as scored persons.

## Pitfalls

- **Scoring `[unverified]` records as if verified.** Score-cap is the feature; never bypass. Same for scoring without enrichment — cap-driven artifacts everywhere.
- **Tuning rubric weights inside the scoring run.** That's `icp-definition`'s job. Drift ruins cross-run comparability.
- **Ignoring trigger decay.** A "raised Series B 14 months ago" record scoring 80 means decay isn't running.
- **Using the score as a fact rather than evidence.** Score is a snapshot; the rationale is the evidence.
- **Treating Tier-1 count as a target.** T1 ratio is an output, not an input.
- **Skipping the SAL gate for Tier-1.** Tier-1 by score doesn't mean SAL-ready; the 4-gate check is the contract.
- **Mixing rubrics across product lines.** Each ICP gets its own scoring run.
- **Aggregating account-level scores without documenting the rule.** Pick one (max / weighted-avg / senior-contact-only) and document.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §8 and CLAUDE.md, every named entity (contact names, signals cited in rationale, dates, dollar figures) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Score rationales reference the *signals on the record* — never invent a "saw their funding announcement" detail to justify a score.
- **Scoring run without a purpose tag.** Cost-per-lead attribution downstream needs it.

## Verification

The run is real when: re-running the same record set with the same rubric produces the same scores ± trigger-decay drift; every score's rationale references actual record signals (no invented details); tier distribution is justified by source — sourcing output and scoring tier ratios are coherent; SAL eligibility per Tier-1 is computed and failed gates named; re-running 30 days later shows lower scores on records with decaying triggers; rubric weights match `icp-definition`'s artifact verbatim.

## Example

**User prompt:** "Score these 80 [hypothetical] enriched leads from a recent BalanceBox [hypothetical] sourcing run. ICP from icp-definition. BANT data partial — firmographic + trigger only, no discovery."
**What should happen:** Validate inputs (12 [hypothetical] records have `[unverified]` fields → flag for cap). Apply 100-pt scorecard per dimension; for each lead, compute Pain/Trigger/WTP/Reach/TTV/Strategic with one-liner rationale. Apply BANT (mostly `unknown` for budget/timing) and CHAMP. Compute final score with -2 to -5 [hypothetical] BANT adjustment. Apply tier cutoffs → 14 [hypothetical] T1 (17.5% [hypothetical]) / 32 [hypothetical] T2 / 24 [hypothetical] T3 / 10 [hypothetical] Anti-ICP — healthy. Run SAL gates on T1: 11 [hypothetical] pass (3 [hypothetical] fail reachability). PATCH 80 [hypothetical] person records (`score`, `priority`, tier tag); push 1 run interaction; route 12 [hypothetical] capped records to review queue. Recommend `multi-channel-cadence` for 11 [hypothetical] SAL records.

**User prompt:** "Re-score these 100 [hypothetical] leads we scored 60 [hypothetical] days ago — no enrichment changes."
**What should happen:** Same inputs, decay applied. Triggers from 60 [hypothetical] days ago have aged; expect scores 3–8 [hypothetical] points lower across the board. Some records that were T1 may drop to T2. Run summary surfaces the decay impact and recommends re-sourcing for fresh triggers via `lead-sourcing-*`.

**User prompt:** "Apply our scorecard retroactively to last quarter's 30 [hypothetical] closed-won deals — validate that the rubric works."
**What should happen:** Freshness override (no decay; the trigger that prompted the won deal is by definition relevant). Score the 30 [hypothetical] deals. If most score ≥75 [hypothetical] → rubric is calibrated. If many score <55 [hypothetical] → rubric is rejecting customers we win → cutoffs wrong, recommend `icp-refinement-loop`. Surface the worst-case won-deal score (would-have-rejected list) for ICP rethink.

## Linked Skills

- Tier-1 SAL-eligible, outreach → `multi-channel-cadence` (planned)
- Tier-2 / Tier-3 nurture → `cold-email-sequence` (planned)
- Score-capped records → `data-enrichment` (re-enrichment)
- Distribution warning, rubric re-tune → `icp-definition`
- ≥30 closed deals, refresh cutoffs → `icp-refinement-loop` (planned)
- Pipeline stage progression → `pipeline-stages` (planned)

## Push to CRM

After scoring, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push` (PATCH semantics). Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-2-skills/.env.example`).

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

(No external API keys — pure compute.)

### Source tag

`source: "skill:lead-scoring:v2.0.0"`

### Example push (PATCHed person + rationale)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Forge Robotics [hypothetical]",
    "contactName": "Esme Liang [hypothetical]",
    "contactEmail": "esme@forge-robotics.com [hypothetical]",
    "score": "3 [hypothetical]",
    "priority": "warm [hypothetical]",
    "tags": "#icp-tier-2 #scored #bant-thin #function-2",
    "relevance": "Tier 2 / 70 [hypothetical] / warm [hypothetical]. New VP Finance Ops at Series C [hypothetical] robotics co (60 [hypothetical] days into role, public hire announcement [hypothetical]). FP&A tooling typically reviewed within 90 [hypothetical] days of VP arrival — narrowing trigger window. Verified email + LinkedIn; budget and prioritization unknown — recommend warm SDR outreach with discovery focus on Q2 [hypothetical] priorities. (Pain 18 [hypothetical]/Trigger 12 [hypothetical]/WTP 16 [hypothetical]/Reach 13 [hypothetical]/TTV 8 [hypothetical]/Strategic 5 [hypothetical]; BANT -2 [hypothetical].)",
    "source": "skill:lead-scoring:v2.0.0"
  }'
```

### Example push (run record as interaction:research)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#scoring-run #function-2",
    "relevance": "Lead scoring run score_2026-05-04_e8r [hypothetical]. Inputs: 80 records (from enrich_2026-05-04_b3 [hypothetical], source: lead-sourcing-clay). Rubric: ICP v2.0.0 (Pain 25/Trig 20/WTP 20/Reach 15/TTV 10/Strat 10; T1 75/T2 55/T3 40). Tier distribution: 14 T1 (17.5%) / 32 T2 / 24 T3 / 10 Anti-ICP. SAL-eligible: 11 of 14 T1 (3 failed reachability gate). BANT data: partial. Score-capped due to [unverified] fields: 12 (routed to review queue). Decay applied. Recommended next: multi-channel-cadence for 11 SAL records.",
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
