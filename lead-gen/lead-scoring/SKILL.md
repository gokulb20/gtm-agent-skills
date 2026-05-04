---
name: lead-scoring
description: Score each Lead record against the ICP scorecard plus BANT and CHAMP qualification frameworks plus a trigger-strength-and-recency formula, write score + priority + tier + rationale onto the person record, and emit a per-run scoring interaction. Use when sourced + enriched leads need outreach prioritization, when a discovery-call decision needs evidence-backed qualification, or when the SDR/AE hand-off requires a tier label per record.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [GTM, Lead-Scoring, Qualification, BANT, CHAMP]
    related_skills: [icp-definition, data-enrichment, lead-sourcing-apollo, lead-sourcing-clay, lead-sourcing-linkedin, lead-sourcing-web]
    requires_tools: [terminal]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
      - key: gtm.sourcing_run_usd_cap
        description: Max spend per scoring run
        default: "25"
      - key: gtm.sourcing_run_record_cap
        description: Max records per scoring run
        default: "2000"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing scores to CRM"
---

# Lead Scoring

Score each enriched Lead against the 100-point ICP scorecard from `icp-definition`, layer in BANT and CHAMP qualification, weight by trigger strength × recency, write the result onto the person record (`score`, `priority`, `icp_tier`), and emit a scoring run interaction with the full math. Pure compute — no external API keys needed.

## When to Use

- "Score these enriched leads against our ICP"
- "Tier 1 / 2 / 3 our weekly sourcing batch"
- User needs SAL hand-off for candidates
- Re-score leads sourced 60+ days ago — triggers may have decayed
- Retroactively score closed-won deals to validate ICP cutoffs
- Pre-outreach prioritization after `data-enrichment`

## Quick Reference

| Concept | Value |
|---|---|
| Rubric weights | Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10 = 100 |
| Tier cutoffs | T1 ≥75 / T2 55–74 / T3 40–54 / Anti-ICP <40 |
| Trigger formula | `trigger_score = base_strength × decay(days_since_event, half_life)` |
| BANT / CHAMP | Each dimension: `confirmed | inferred | unknown`. BANT adj: 4 confirmed +5; 3+ +3; mostly unknown −5 |
| SAL gates (Tier-1) | ICP fit + trigger present + decision-maker IDed + no hard disqualifiers |
| Score-cap rule | `[unverified]` field → cap at 60 (Tier-2 max), route to review |
| Healthy distribution | 10–20% T1 / 30–45% T2 / 25–35% T3 / 5–15% Anti-ICP |
| CRM score mapping | 75–100 → 5; 55–74 → 4/3; 40–54 → 2; <40 → 1 |

## Procedure

1. **Validate inputs.** Confirm Lead records have required fields and ICP scorecard is loaded. Flag records with `[unverified]` critical fields — they will score-cap. Reference `${HERMES_SKILL_DIR}/references/` for rubric dimension definitions.
2. **Apply 100-pt scorecard per dimension.** Compute Pain (P-T-O chain), Trigger (strength × decay), WTP (firmographic + funding), Reach (verified email/phone/linkedin), TTV (role + stage + stack friction), Strategic (logo, vertical anchor). Per-dimension rationale one-liner.
3. **Apply BANT and CHAMP in parallel.** Populate Budget/Authority/Need/Timing AND Challenges/Authority/Money/Prioritization (`confirmed | inferred | unknown`). Apply BANT adjustment to base score.
4. **Compute final score, tier, priority.** `final_score = scorecard_total + bant_adjustment` (capped 100). Apply tier cutoffs from `icp-definition`.
5. **Apply SAL criteria (Tier-1 only).** Check 4 gates: ICP fit ≥75 / trigger within half-life / decision-maker identified / no hard disqualifiers. Pass all → `sal_eligible: true`.
6. **Tier distribution + per-record rationale.** Aggregate tier counts; flag suspicious distribution (>50% T1 = rubric too lenient; <2% T1 = source too wide). Compose 2–3 sentence rationale per record.
7. **PATCH person + emit run interaction.** Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. PATCH `score`, `priority`, tier tags. Emit `interaction:research` with full math. `[unverified]` records to review queue. Run `${HERMES_SKILL_DIR}/scripts/dedup_leads.py` if needed.

## Pitfalls

- Scoring `[unverified]` records as if verified — score-cap is the feature; never bypass
- Tuning rubric weights inside the scoring run — that's `icp-definition`'s job; drift ruins comparability
- Ignoring trigger decay — "raised Series B 14 months ago" scoring 80 means decay isn't running
- Treating Tier-1 count as a target — T1 ratio is an output, not an input
- Skipping the SAL gate — Tier-1 by score doesn't mean SAL-ready; 4-gate check is the contract
- Mixing rubrics across product lines — each ICP gets its own scoring run

## Verification

1. Re-running same record set with same rubric produces same scores ± trigger-decay drift
2. Every score rationale references actual record signals — no invented details
3. Tier distribution is justified by source — sourcing output and scoring ratios are coherent
4. SAL eligibility computed per Tier-1 and failed gates named
5. Rubric weights match `icp-definition` artifact verbatim
