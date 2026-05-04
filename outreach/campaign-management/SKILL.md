---
name: campaign-management
description: Monitor active multi-channel cadences in real-time — pull reply rate, bounce rate, complaint rate, sender reputation — and make pause/slow-down/swap-copy decisions against pre-defined thresholds. Surfaces A/B test results when statistically meaningful and auto-pauses on hard-threshold breach. Use when campaigns need ongoing oversight, metrics need daily/weekly review, A/B tests need decision-making, or reputation drift requires a pause.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Outreach, CampaignMonitoring, Optimization, A/B Testing]
    related_skills: [email-infrastructure-setup, cold-email-sequence, linkedin-outreach, cold-calling, multi-channel-cadence]
    requires_tools: [terminal]
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

# Campaign Management

Watch active outreach campaigns and make real-time adjustment decisions against pre-defined thresholds. Auto-pauses on hard-threshold breach (Google/MS complaint rate, Postmaster "Bad" reputation). Reply rate is the primary metric (Apple MPP made opens noise).

## When to Use

- Active campaign(s) need ongoing human-in-loop oversight
- A/B test running — when's it ready to call?
- Complaint rate looks high — should I pause?
- Daily/weekly review of all active campaigns
- Reply rate plateaued at 2.5% on day 8 — diagnose
- Reputation drift detection and pause decisions

## Quick Reference

| Concept | Value |
|---|---|
| Primary metric | Reply rate (cumulative + per-channel). Open rate = noise |
| Reply-rate floor (cold email) | 3% by D+10 |
| Reply-rate floor (multi-channel) | 6% by D+10 |
| LI acceptance floor | 12% by D+7 |
| Call connect floor | 6% cumulative |
| Bounce thresholds | Pause 5%; warn 2% |
| Complaint thresholds | Pause 0.3%; warn 0.1% (Google/MS Feb 2024) |
| Postmaster Tools | Pause if "Bad"; warn on Medium-trending-down |
| SNDS | Pause on red; warn on yellow |
| State machine | draft → active → paused → completed / aborted |
| Decisions | continue / slow-down / swap-copy / pause / resume / abort |
| A/B method | Bayesian (n<200/arm); frequentist z-test (n≥200/arm) |
| Polling default | Daily cumulative + 4h sender-reputation-only for active |
| Reputation cross-check | Multi-source convergent signal triggers pause; single-source = warn |

## Procedure

1. **Pull current metrics per campaign** — 24h + cumulative from sending platforms; per-channel disaggregation; sender reputation (Postmaster + SNDS + Talos) + 7d trend. Reference `${HERMES_SKILL_DIR}/references/thresholds-and-decisions.md`.
2. **Compare against thresholds + make decision** — Per conventions §8.4 + `.env` defaults. Pause if any pause threshold hit; slow-down if warn only; swap-copy if reply rate below floor AND deliverability healthy; continue if all nominal.
3. **A/B test significance check** — n<200/arm: Bayesian, recommend winner if `P(b>a) > 0.85` AND effect ≥1pp. n≥200/arm: z-test at p<0.05 + effect ≥1pp. D+14 inconclusive: stop, ship higher-volume variant. See `${HERMES_SKILL_DIR}/references/ab-testing-methods.md`.
4. **Diagnose plateau (when swap-copy triggered)** — Audit recent copy against cliché + buzzword blocklists; audit hook quality; audit recipient quality. Recommend: copy rewrite / re-enrichment / re-tier.
5. **Write adjustments_log + notify user** — Every decision (incl. "continue") logged with timestamp, triggers, metrics_snapshot, action_taken, reason. Pause = immediate high-priority; slow-down = next cycle; swap-copy = with diagnosis.
6. **Push to CRM + schedule next cycle** — Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py` per decision. PATCH Campaign state + metrics_summary if changed. Default: daily cumulative + 4h reputation for active; daily for paused.

## Pitfalls

- **Optimizing on open rate** — Apple MPP made it noise
- **Ignoring complaint-rate spikes** — Google/MS Feb 2024 hard rule; pause at 0.3%
- **Slow-down without re-eval** — becomes silent under-performance
- **Calling A/B winners early** — n<50 = noise
- **Treating reputation feeds as gospel** — cross-check; pause on convergent signal
- **Not logging "continue" decisions** — audit trail incomplete

## Verification

1. Every active campaign has a decision logged with metrics_snapshot at the timestamp; all pause-threshold breaches resulted in actual state transitions
2. Sender reputation feeds were pulled from named tools (or `[unverified]` flagged); A/B test winners have explicit posterior/p-value AND effect size
3. Re-running same monitoring cycle on same metrics produces same decision (deterministic)
