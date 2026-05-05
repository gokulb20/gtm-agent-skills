---
name: ab-testing-messaging
description: Design and run A/B tests on messaging variables with proper statistical discipline — Bayesian or frequentist depending on volume, minimum sample sizes, and one-variable-at-a-time design. Use when the user says "A/B test subject lines", "test opener variants", "which variant wins", or "sample size for A/B test."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Analytics, AB-Testing, Experimentation, Messaging-Optimization]
    related_skills: [cold-email-sequence, campaign-management, kpi-reporting, icp-refinement-loop]
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

# A/B Testing — Messaging

Design and run A/B tests on outreach messaging variables (subject lines, openers, hooks, CTAs, sequence length, send-time) with proper statistical discipline. Hard rule: never ship a "winner" on n<50/arm.

## When to Use

- Active campaign needs messaging optimization
- New copy hypothesis needs validation before scaling
- Reply rate plateaued — copy refresh in flight
- Sample-size estimate needed before launching a test
- User says "A/B test subject lines" or "which variant wins"

## Quick Reference

| Concept | Value |
|---|---|
| One-variable rule | Only ONE thing differs between A and B |
| Primary metric | Reply rate (open rate is noise — Apple MPP) |
| Low-volume regime (<1k/arm/14d) | Bayesian + MIN_EFFECT_SIZE 3.0pp |
| High-volume regime (≥5k/arm/14d) | Frequentist z-test + MIN_EFFECT_SIZE 1.0pp |
| Bayesian threshold | P(B>A) >0.85 (house); 0.95 industry-canonical |
| Frequentist threshold | Two-proportion z-test p<0.05 AND effect ≥1pp |
| Min n per arm | 50; below = call inconclusive |
| Max test duration | 14d; longer = drift confounds |

## Procedure

1. **Validate hypothesis + variable.** ONE variable differs. Multi-variable → reject. Confirm testable (not "tone"). See `${HERMES_SKILL_DIR}/references/regime-selection.md`.
2. **Compute sample size + pick regime.** Given baseline rate + expected volume, compute MDE and n required. Pick low-volume or high-volume regime explicitly.
3. **Pick significance method.** Expected n<200/arm → Bayesian. ≥200/arm → frequentist. User can override.
4. **Design test document.** Hypothesis + variants + split + metrics + thresholds + max duration + min n. This is the test contract. See `${HERMES_SKILL_DIR}/references/test-design.md`.
5. **Launch via channel skill.** Hand off to cold-email-sequence/linkedin-outreach with split + allocation rule.
6. **Monitor + check stop conditions.** Daily/weekly: pull metrics per arm. Check min-n, significance, max duration.
7. **Significance call.** Significance + effect ≥ threshold + min-n → winner. Ship 100% remaining to winner. Max duration without → inconclusive (ship control). See `${HERMES_SKILL_DIR}/references/significance-calls.md`.
8. **Push to CRM.** Test design at launch; result at call. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Multi-variable changes labeled "A/B test" — can't attribute the lift
- Optimizing open rate — Apple MPP noise; reply rate only
- Calling winners early on small n — n<50 = noise
- Effect-size-blind significance — p<0.05 with 0.3pp lift = ship-worthless
- Allocation drift mid-test — hash-based; same recipient always same variant

## Verification

1. Pre-launch sample-size estimate documented
2. One-variable rule enforced
3. Significance call references method + raw numbers + effect size
4. Min-n + max-duration stop conditions honored
5. Winner handoff to channel skill executed
