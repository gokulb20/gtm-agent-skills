---
name: campaign-management
description: Monitor active multi-channel cadences in real-time — pull reply rate, bounce rate, complaint rate, sender reputation, per-channel performance — and make pause / slow-down / swap-copy decisions against pre-defined thresholds. Surfaces A/B test results when statistically meaningful and auto-pauses on hard-threshold breach (Google/MS bulk-sender complaint rate, bounce rate, Postmaster Tools "Bad" reputation). Use when one or more campaigns are active and need ongoing human-in-loop oversight, when a campaign's metrics need a daily / weekly review, when an A/B test on copy needs decision-making, or when reputation drift requires a campaign pause.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, campaign-monitoring, optimization, function-3]
related_skills:
  - email-infrastructure-setup
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - multi-channel-cadence
  - reply-classification
  - channel-performance
  - kpi-reporting
inputs_required:
  - active-campaign-id-or-list
  - reply-and-disposition-data-stream
  - sender-reputation-feeds
  - threshold-overrides
  - run-purpose-tag
deliverables:
  - real-time-campaign-metrics-summary
  - pause-or-slow-down-decisions
  - a-b-test-results-with-significance
  - reputation-drift-alerts
  - copy-swap-recommendations
  - campaign-state-transitions-log
  - campaign-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Campaign Management

Watch active outreach campaigns and make real-time adjustment decisions against pre-defined thresholds. Pulls reply rate, bounce rate, complaint rate, per-channel performance, and sender reputation feeds. Auto-pauses on hard-threshold breach (Google/MS bulk-sender rules); surfaces A/B test results when statistically meaningful; recommends copy swaps when channel-skill metrics indicate broken copy. Owns the campaign state machine. Reply-rate is the primary metric (Apple MPP made opens noise).

> *Worked example uses WorkflowDoc (fictional, function-1 carry-over) as the seller; procedure is vertical-agnostic. Shared rules in `function-3-skills/function-3-conventions.md`.*

## Purpose

Outbound campaigns drift. Sender reputation degrades subtly; reply rates plateau; one bad list pollutes a domain that took weeks to warm. Without active monitoring, a campaign healthy on day 3 can be a deliverability disaster by day 14. This skill: reads metrics_summary on each active campaign at user-defined cadence (default daily), compares against thresholds, makes one of four decisions (continue / slow-down / swap-copy / pause), calls A/B test winners at significance, writes every decision to adjustments_log. Goal: catch problems early, ship A/B results when meaningful, never let a campaign ship through a complaint-rate spike.

## When to Use

- "Monitor my active campaign and tell me when something needs attention."
- "A/B test running — when's it ready to call?"
- "Our complaint rate looks high — should I pause?"
- "Daily review of all active campaigns."
- "Reply rate plateaued at 2.5% on day 8 — diagnose."
- Daily / weekly oversight cadence; reputation drift detection.

## Inputs Required

1. **Active campaign id(s)** — one or many.
2. **Reply + disposition data stream** — sending platforms (Smartlead, Instantly, Lemlist, HeyReach, Dripify, JustCall, etc.) + CRM. Webhook or polling.
3. **Sender reputation feeds** — `GOOGLE_POSTMASTER_OAUTH_TOKEN`, `MICROSOFT_SNDS_API_KEY`, `TALOSINTEL_API_KEY`. Daily refresh.
4. **Threshold overrides** (optional) — defaults from `.env` per conventions §8.4.
5. **Run purpose tag**.
6. (Optional) A/B test config — variant ids + traffic split + significance method (default Bayesian for n<200).

## Quick Reference

| Concept | Value |
|---|---|
| **Primary metric** | Reply rate (cumulative + per-channel). Open rate = noise (Apple MPP). |
| **Reply-rate floor (cold email)** | 3% by D+10 |
| **Reply-rate floor (multi-channel)** | 6% by D+10 |
| **LI acceptance floor** | 12% by D+7 |
| **Call connect floor** | 6% cumulative |
| **Bounce thresholds** | Pause at 5%; warn at 2% |
| **Complaint thresholds** | Pause at 0.3%; warn at 0.1% (Google/MS Feb 2024) |
| **Postmaster Tools** | Pause if "Bad"; warn on Medium-trending-down |
| **SNDS** | Pause on red; warn on yellow |
| **State machine** | draft → active → paused → completed / aborted |
| **Decisions** | continue / slow-down / swap-copy / pause / resume / abort |
| **A/B method** | Bayesian (n<200/arm); frequentist z-test (n≥200/arm); winner needs effect ≥1pp + significance |
| **Polling default** | Daily cumulative metrics for active + 4h sender-reputation-only (Postmaster/SNDS/TalosIntel light pings, no per-send polling); daily for paused. 4h-per-send polling is rate-limit risk on most ESPs (Smartlead/Instantly/HeyReach) — use cumulative. |
| **Reputation cross-check** | Multi-source convergent signal triggers pause; single-source = warn |

## Procedure

### 1. Pull current metrics per campaign
24h + cumulative metrics from sending platforms; per-channel disaggregation; sender reputation (Postmaster + SNDS + Talos) + 7d trend; per-recipient progress; DMARC alignment if available.

### 2. Compare against thresholds + make decision
Per conventions §8.4 + `.env` defaults. Apply rubric per campaign:
- **Pause** if any pause threshold hit. State `active → paused`. User ack to resume.
- **Slow-down** if warn threshold + no pause. Reduce volume 50% for 24h; re-eval next cycle.
- **Swap-copy** if reply rate / acceptance / connect rate below floor by D+10/D+7 AND deliverability healthy. Call channel skill rewrite mode.
- **Continue** if all metrics nominal.

### 3. A/B test significance check
n<200/arm: Bayesian; recommend winner if `P(b>a) > 0.85` AND effect ≥1pp. n≥200/arm: z-test at p<0.05 + effect ≥1pp. By D+14 inconclusive: stop, ship higher-volume variant by default.

### 4. Diagnose plateau (when swap-copy triggered)
Audit recent touch copy against cliché + buzzword blocklists; audit hook quality; audit recipient quality. Recommend: copy rewrite / re-enrichment / re-tier per diagnosis.

### 5. Write adjustments_log + notify user
Per conventions §2.3: every decision (incl. "continue") logged with timestamp, decision, triggers, metrics_snapshot, action_taken, reason. Notify: pause = immediate high-priority; slow-down = next cycle; swap-copy = with diagnosis; continue = periodic summary.

### 6. Push to CRM + schedule next cycle
`interaction:research` per decision. PATCH Campaign state + metrics_summary if changed. Default polling: daily cumulative + 4h sender-reputation-only for active; daily for paused.

## Output Format

- Per-campaign decision (continue / slow-down / swap-copy / pause / resume / abort)
- Metrics snapshot per campaign (reply / bounce / complaint / reputation + per-channel disaggregation)
- A/B test results (when applicable) with method, posterior or p-value, effect size, recommendation
- Reputation drift alerts (Postmaster + SNDS + Talos cross-check)
- Adjustments_log entries (per conventions §2.3)
- User notifications (pause = immediate high-priority; slow-down = next cycle; continue = periodic summary)
- Run record: monitored count, decisions summary, alerts emitted, next cycle ETA

## Done Criteria

1. Active campaigns enumerated; metrics pulled per campaign; reputation feeds pulled (or `[unverified]` flagged).
2. Decision rubric applied; one of {continue, slow-down, swap-copy, pause} chosen.
3. A/B tests evaluated when applicable; winner called only at significance + effect-size thresholds.
4. Plateau diagnosis run when swap-copy triggered.
5. Adjustments_log entry written per campaign per cycle (including "continue").
6. User notified per priority routing.
7. CRM push: state transitions + metrics summary updated; one `interaction:research` per decision; next cycle scheduled.

## Pitfalls

- **Optimizing on open rate.** Apple MPP made it noise.
- **Ignoring complaint-rate spikes.** Google/MS Feb 2024 hard rule; pause at 0.3%.
- **Slow-down without re-eval.** Becomes silent under-performance. Pause without notification — user needs to know to ack.
- **Auto-resume after manual pause.** Don't override user judgment.
- **Calling A/B winners early.** n<50 = noise.
- **Treating reputation feeds as gospel.** Feeds disagree; cross-check; pause on convergent signal. Adjusting too frequently = theater (daily + hard-pauses is right cadence).
- **Letting LI account amber linger.** 7-day cool-down non-negotiable.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (campaigns, metrics values, dates, decision rationale, reputation verdicts) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. NEVER invent a Postmaster Tools verdict, a metric value, or a decision rationale without the source.
- **Not logging "continue" decisions.** Audit trail incomplete if only changes logged.

## Verification

The monitoring run is real when: every active campaign has a decision logged with metrics_snapshot at the timestamp; all pause-threshold breaches resulted in actual state transitions (not just warnings); sender reputation feeds were pulled from the named tools (or `[unverified]` flagged); A/B test winners (when called) had explicit posterior / p-value AND effect size; re-running the same monitoring cycle on the same metrics produces the same decision (deterministic).

## Example

**User prompt:** "Daily review of our active WorkflowDoc `[hypothetical]` campaign cmp_workflowdoc_t1_mc_2026-05-22 `[hypothetical]`."
**What should happen:** Pull D+8 metrics: 152 emails sent `[hypothetical]`, reply rate 7.9% `[hypothetical]` ✓, bounce 2.6% `[hypothetical]` (above 2% warn), complaint 0, Postmaster Medium stable, LI acceptance 39% `[hypothetical]` ✓, call connect 12.5% `[hypothetical]` ✓. Decision: slow-down (bounce-rate warn, no pause). Action: reduce email to 15/mailbox/day for 24h; re-eval D+9 at 10am UTC. Slack alert sent. Adjustments_log entry written. State stays active.

**User prompt:** "Complaint rate just spiked — should I pause?"
**What should happen:** Pull cumulative + 24h complaint metrics. If 24h spike >0.3% pause threshold AND Postmaster shows "Low" or worse → state `active → paused` immediately; high-priority notification; recommend list-quality audit (recent batches likely have wrong-audience signals); user must ack to resume.

**User prompt:** "A/B test on subject line — call it."
**What should happen:** Pull per-variant reply rates. n=180/180 per arm `[hypothetical]`. Bayesian: variant B 6.2% vs variant A 4.1% `[hypothetical]`, posterior P(B>A) = 0.96 `[hypothetical]`, effect 2.1pp `[hypothetical]`. Recommendation: ship variant B for remainder. Traffic shifted 100% to B; decision logged.

## Linked Skills

- Pause + infrastructure suspect → `email-infrastructure-setup` (recovery mode)
- Swap-copy + copy weak → `cold-email-sequence` (rewrite mode)
- Swap-copy + hooks weak → `data-enrichment` (re-enrichment); list weak → `lead-scoring` (re-tier)
- Replies arriving → `reply-classification` (planned); meetings booked → `discovery-call-prep` (planned)
- Long-term attribution → `channel-performance` (planned); weekly KPI → `kpi-reporting` (planned)
- LI account amber → `linkedin-outreach` (cool-down); new launch → `multi-channel-cadence`

## Push to CRM

Persist agent-actionable monitoring state and decisions to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-decision adjustment log entry | `interaction` (type: `research`) | `relevance` = decision + triggers + metrics snapshot + action; `tags: "#campaign-management-decision #function-3"` |
| Pause-state notification | `interaction` (type: `research`) | High-priority alert; `tags: "#alert #campaign-paused #function-3"` |
| Per-campaign state transition | PATCH on Campaign record (via `interaction:research` referencing campaign_id) | New state + transition reason |
| A/B test winner declaration | `interaction` (type: `research`) | `relevance` = method + posterior/p-value + effect size + recommendation; `tags: "#ab-test-winner #function-3"` |
| Reputation drift alert | `interaction` (type: `research`) | `relevance` = current reputation + 7d trend + cross-source check; `tags: "#reputation-alert #function-3"` |
| `[unverified — needs check]` (missing reputation feed) | `interaction` (type: `research`) | `tags: "#unverified #review-required #campaign-management"`; decision marked partial |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
GOOGLE_POSTMASTER_OAUTH_TOKEN=
MICROSOFT_SNDS_API_KEY=
TALOSINTEL_API_KEY=
EASYDMARC_API_KEY=
# Sending platform API keys per their .env (Smartlead, HeyReach, JustCall, etc.)
BOUNCE_RATE_PAUSE_THRESHOLD=0.05
BOUNCE_RATE_WARN_THRESHOLD=0.02
COMPLAINT_RATE_PAUSE_THRESHOLD=0.003
COMPLAINT_RATE_WARN_THRESHOLD=0.001
REPLY_RATE_FLOOR=0.03
```

### Source tag

`source: "skill:campaign-management:v2.0.0"`

### Example push (slow-down decision)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#campaign-management-decision #function-3 #slow-down",
    "relevance": "Campaign cmp_workflowdoc_t1_mc_2026-05-22 [hypothetical] (WorkflowDoc [hypothetical]). D+8. Decision: slow-down. Triggers: bounce-rate-warn (2.6% [hypothetical] > 2% threshold). Metrics: reply rate 7.9% [hypothetical] / bounce 2.6% [hypothetical] / complaint 0 / Postmaster Medium stable. Action: reduced email volume to 15/mailbox/day from 30 for 24h. LI + call unchanged. Re-eval D+9 at 10am UTC.",
    "source": "skill:campaign-management:v2.0.0"
  }'
```

### Example push (hard-pause)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#alert #campaign-paused #function-3",
    "relevance": "Campaign cmp_workflowdoc_t1_mc_2026-05-22 [hypothetical] (WorkflowDoc [hypothetical]). D+5. State: active → paused. Triggers: complaint-rate-pause (0.42% [hypothetical] > 0.3% threshold). Recent 24h: 152 sends [hypothetical], 0.64 complaint rate [hypothetical]. Cross-check: Postmaster Tools shows Low (was Medium yesterday) [hypothetical]. Action: stopped all email sends; LI + call unchanged. User must ack to resume. Recommend: audit recent batches for wrong-audience signals; consider list-quality review via data-enrichment.",
    "source": "skill:campaign-management:v2.0.0"
  }'
```

### Example push (A/B test winner)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#ab-test-winner #function-3",
    "relevance": "A/B test ab_t1_opener_2026-05-22 [hypothetical] on campaign cmp_workflowdoc_t1_mc_2026-05-22 [hypothetical] (WorkflowDoc [hypothetical]). D+12. Variant A (CCQ + Pain): 4.1% reply rate [hypothetical] (n=180, 7 replies [hypothetical]). Variant B (CCQ + Vision): 6.2% reply rate [hypothetical] (n=180, 11 replies [hypothetical]). Method: Bayesian. Posterior P(B > A) = 0.96 [hypothetical]. Effect size: 2.1pp [hypothetical]. Recommendation: ship variant B for remaining cadence. Action: traffic shifted 100% to variant B.",
    "source": "skill:campaign-management:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Decision logged + state transitions executed per standard mapping. |
| `[unverified — needs check]` | Decision marked partial (e.g., reputation feed unavailable); pushes as `interaction:research` with `#unverified #review-required #campaign-management` tag; decision deferred or made with explicit caveat. |
| `[hypothetical]` | Never executed; never pushed. Local artifact only. |

### When NOT to push

- Monitoring cycle ran but no decisions changed (pure "continue" across all campaigns) — push a single periodic summary `interaction:research` per day, not per cycle.
- Metrics feed unavailable for whole cycle — push `interaction:research` with `#monitoring-failed` and reason; no decisions made.
- `[unverified]` partial data — see provenance routing.
- `[hypothetical]` — never.
- User manually overrode a pause-threshold-triggered pause with `risk_accepted: true` — push the override decision with full audit trail (override IS push-worthy as accountability record).
