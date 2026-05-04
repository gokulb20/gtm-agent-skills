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

Watch active outreach campaigns and make real-time adjustment decisions against pre-defined thresholds. Pulls reply rate, bounce rate, complaint rate, per-channel performance, and sender reputation feeds; auto-pauses on hard-threshold breach (Google/MS bulk-sender rules); surfaces A/B test results when statistically meaningful; recommends copy swaps when channel-skill metrics indicate broken copy. Owns the campaign state machine: `draft` → `active` → `paused` → `completed` / `aborted`. Reply-rate is the primary metric (Apple MPP made opens noise).

> *The worked example uses a fictional product (WorkflowDoc) for illustration — same product as function-1, in a third role: WorkflowDoc as the seller monitoring an active 7-touch multi-channel cadence. The metrics, thresholds, and procedures are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Touch / Cadence / Campaign schemas, sender reputation thresholds, deliverability baseline (Apple MPP), compliance, anti-fab, push-to-CRM routing — live in `function-3-skills/function-3-conventions.md`. This skill assumes it.*

## Purpose

Outbound campaigns drift. Sender reputation degrades subtly; reply rates plateau; one bad list pollutes a domain that took weeks to warm. Without active monitoring, a campaign that was healthy on day 3 can be a deliverability disaster by day 14. This skill: (1) reads the metrics_summary on each active campaign at user-defined cadence (default daily), (2) compares against thresholds for reply / bounce / complaint / reputation, (3) makes one of four decisions per campaign — continue / slow-down / swap-copy / pause, (4) when an A/B test runs, calls statistical significance and recommends a winner, (5) writes every decision to the campaign's adjustments_log so the audit trail is complete. Goal: catch problems early, ship A/B results when meaningful, never let a campaign ship through a complaint-rate spike.

## When to Use

- "Monitor my active campaign and tell me when something needs attention."
- "We have a copy A/B test running — when's it ready to call?"
- "Our complaint rate looks high — should I pause?"
- "Daily review of all active campaigns."
- "Reply rate plateaued at 2.5% on day 8 — diagnose."
- Daily / weekly oversight cadence on active programs.
- Reputation drift detection and pause decisions.

### Do NOT use this skill when

- No campaigns are active — there's nothing to monitor; recommend launching via `multi-channel-cadence` first.
- The user wants ad-hoc one-off metrics (just want a snapshot, not ongoing monitoring) — produce a snapshot report but don't claim "monitoring" — that requires recurring.
- The user wants attribution analytics across campaigns over time — that's `channel-performance` (function-6); this skill is real-time / per-campaign.
- The user wants to *change* a campaign's strategy mid-flight (rewrite copy, change targeting) — recommend `cold-email-sequence` rewrite mode + new cadence; don't try to surgery active sends.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Active campaign id(s) | yes | user / CRM query | One or many campaigns. |
| 2 | Reply + disposition data stream | yes | sending platforms (Smartlead/Instantly/Lemlist/HeyReach/Dripify/JustCall/etc.) + CRM | Webhook or polling. Replies, bounces, opens (informational), unsubscribes, complaints, call dispositions. |
| 3 | Sender reputation feeds | yes | `GOOGLE_POSTMASTER_OAUTH_TOKEN`, `MICROSOFT_SNDS_API_KEY`, `TALOSINTEL_API_KEY` | Read-only; daily refresh acceptable (these update slowly). |
| 4 | Threshold overrides | optional | user | Defaults from `.env` per conventions §8.4. User can tighten for high-stakes campaigns. |
| 5 | Run purpose tag | yes | user | Stamped on every adjustment decision. |
| 6 | A/B test config (optional) | no | user | Variant ids + traffic split + significance test method (default Bayesian for n<200). |

### Fallback intake script

> "Campaign management runs in the background while your campaigns are active. Three things I need:
> - Campaign id(s) to monitor (or 'all active').
> - How to access metrics: webhook from your sending platforms, or polling cadence (default: every 4h).
> - Threshold overrides? Defaults are conservative — bounce rate pause at 5%, complaint rate pause at 0.3%, reply rate floor 3%."

### Input validation rules

- No active campaigns → block with explanation; recommend `multi-channel-cadence` to launch first.
- Sender reputation feeds unavailable → degrade to bounce + complaint + reply only; warn user; reputation-drift detection limited.
- A/B test config without traffic-split → block; require explicit split.
- Threshold overrides out of safe range (e.g. complaint rate cap >0.3%) → warn but allow; user takes the risk.
- Polling cadence <1h → block (excessive; rate-limits sending platforms).

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Apple Mail Privacy Protection (MPP) metrics posture** | Apple — iOS 15 (2021) | Apple Mail pre-fetches images, inflating open rates and triggering tracking pixels at fetch. **Open rate is noise, never primary.** Reply rate is the primary metric; meeting rate is the ground truth. The skill reports opens but never optimizes against them. |
| **Sender reputation thresholds** (industry-codified) | Google Postmaster Tools, Microsoft SNDS, Cisco TalosIntel published guidance | "Bad" Postmaster reputation OR red SNDS OR negative TalosIntel = pause threshold. "Medium" Postmaster = warn threshold. Cross-check; never pause on a single source. |
| **Google + Microsoft Feb 2024 bulk-sender rules** | Google + Microsoft (industry-standard, enforced Feb 2024) | Complaint rate <0.3% (warning at 0.1%); authentication aligned; one-click List-Unsubscribe present. Hard pause on complaint-rate breach. |
| **A/B test significance — Bayesian (default for n<200)** | Bayesian inference (Bernoulli model) | For two-variant tests on reply rate where samples are <200 per arm, Bayesian credibility intervals avoid the "wait for 99% confidence and ship nothing" problem. Recommend a winner when posterior probability > 0.85 and effect size meaningfully larger than the cost of the swap. |
| **A/B test significance — frequentist (n>200)** | Standard two-proportion z-test or chi-square | When samples are large enough, use the standard test at p<0.05; report effect size (absolute pp) and confidence interval, not just "significant". |
| **Campaign state machine** (house-built, codified) | Crewm8 | Five states: `draft` → `active` → `paused` → `completed` / `aborted`. Transitions are explicit, audited, and reversible (paused → active resumable; aborted not). Hard rule: state transitions logged in `adjustments_log` with reason. |
| **Adjustment decision rubric** (house-built) | Crewm8 — codified ops practice | Four decisions per monitoring cycle: (a) **continue** (all metrics nominal), (b) **slow-down** (warning thresholds — reduce daily volume by 50% pending re-eval), (c) **swap-copy** (reply rate <3% by D+10 — call `cold-email-sequence` rewrite), (d) **pause** (any pause threshold breached — stop until user acknowledges). Decision logged with metrics snapshot. |

## Tools and Sources

### Sending platforms (metrics source — read-only)

| Tool | Metrics provided |
|---|---|
| Smartlead | Reply, bounce, complaint, unsubscribe, open (informational), click |
| Instantly | Same |
| Lemlist | Same |
| HeyReach / Dripify | Connection-acceptance, message-reply, profile-view |
| JustCall / Aircall | Connect rate, voicemail count, conversation duration, disposition |

### Reputation feeds (read-only, daily refresh)

| Tool | What it shows |
|---|---|
| Google Postmaster Tools | Domain + IP reputation; spam rate per Google's view; authentication results; encrypted vs plain ratio |
| Microsoft SNDS | IP reputation per Microsoft's view (less granular than Google) |
| Cisco TalosIntel | Public IP reputation; secondary signal |
| EasyDMARC reports | DMARC alignment over time; identifies third-party-sender misconfig |

### A/B test infrastructure

This skill computes significance from raw counts; doesn't depend on a tool. Optionally consume the sending platform's built-in A/B (Smartlead, Lemlist support) but normalize results into the conventions §2.3 metrics_summary shape.

### Source priority rule

For decisions: **complaint rate (Google Postmaster + Microsoft SNDS + sending platform's complaint feed)** > **bounce rate (sending platform)** > **Postmaster Tools reputation drop** > **reply rate trend** > **A/B test results (only when significant)**. Pause-thresholds always win; one-source-only triggers warn-only; multi-source triggers pause.

## Procedure

### 1. Pull current metrics for each monitored campaign

For each active campaign:
- Sending platform metrics (last 24h + cumulative): reply rate, bounce rate, complaint rate, open rate (informational), click rate, unsubscribe rate.
- Per-channel disaggregation (email vs LI vs call).
- Sender reputation: Google Postmaster, Microsoft SNDS, TalosIntel — current values + 7d trend.
- Per-recipient progress: % of cadence completed, exit-state distribution.
- DMARC alignment from EasyDMARC reports (if configured).

### 2. Compare against thresholds

Per conventions §8.4 + .env-defined defaults:

| Signal | Pause threshold | Warn threshold | Decision class |
|---|---|---|---|
| Bounce rate (24h) | 5% | 2% | hard-pause / slow-down |
| Complaint rate (24h) | 0.3% | 0.1% | hard-pause / slow-down |
| Postmaster Tools reputation | Bad | Medium-trend-down | hard-pause / slow-down |
| Microsoft SNDS color | Red | Yellow | hard-pause / warn |
| Reply rate (cumulative D+10) | n/a | <3% | swap-copy |
| Connection-acceptance (LI, D+7) | n/a | <12% | swap-copy |
| Connect rate (call, cumulative) | n/a | <6% | swap-copy / re-tier |
| LI account safety state | red | amber | hard-pause / slow-down |

### 3. Make decision per campaign

Apply rubric:
- **Pause** if any pause threshold hit. State transition `active → paused`. User must explicitly acknowledge before resume.
- **Slow-down** if any warn threshold hit AND no pause-threshold hit. Reduce daily volume by 50%; flag for re-eval in 24h.
- **Swap-copy** if reply rate / connection-acceptance / connect rate is below floor by D+10 / D+7 / cumulative AND deliverability is healthy. Call relevant channel skill in rewrite mode.
- **Continue** if all metrics nominal. No action; log "monitoring".

### 4. A/B test significance check (when applicable)

For active A/B tests:
- Compute reply rates per variant.
- If n<200 per arm: Bayesian credibility interval; recommend winner if `P(variant_b > variant_a) > 0.85` AND effect size ≥1pp.
- If n≥200 per arm: two-proportion z-test; recommend winner at p<0.05 AND effect size ≥1pp.
- If neither significant by D+14: recommend stopping the test (inconclusive); ship the higher-volume variant by default.

### 5. Diagnose plateau (reply-rate flat at <3%)

When swap-copy decision triggers, run a quick diagnosis before recommending the rewrite:
- Audit recent batch of touch copy against `cold-email-sequence`'s cliché blocklist + buzzword blocklist.
- Audit hook quality (% of hooks `[verified]` vs `[unverified — needs check]`).
- Audit recipient quality (Tier-1 SAL vs other; recent enrichment date).

Recommend: copy rewrite (if blocklist violations found), re-enrichment (if hooks weak), re-tier (if recipients drifted to Tier-2/3 mid-campaign).

### 6. Write adjustments_log entries

For every decision (including "continue"), append to the Campaign's adjustments_log per conventions §2.3:
```yaml
- timestamp: <ISO>
  decision: continue | slow-down | swap-copy | pause | resume | abort
  triggers: [<list of threshold breaches>]
  metrics_snapshot: <full metrics at decision time>
  action_taken: <e.g. "Reduced daily volume from 200 to 100" / "Called cold-email-sequence in rewrite mode" / "Awaiting user ack to resume">
  reason: <one-sentence>
```

### 7. Notify user (per their preferred channel)

Push decision to the user's notification channel (email / Slack / dashboard alert) when:
- Pause: ALWAYS notify immediately; campaign halted pending ack.
- Slow-down: notify next monitoring cycle.
- Swap-copy: notify with diagnosis + recommendation.
- Continue: include in periodic summary (daily/weekly), not per-cycle.

### 8. Push to CRM

Per conventions §11: push the campaign-management decision as `interaction:research` (one entry per decision). PATCH the Campaign record's `state` and `metrics_summary` if changed.

### 9. Schedule next monitoring cycle

Default polling cadence: every 4h for `active` campaigns; daily for `paused`. User can override per campaign.

## Output Template

```yaml
monitoring_run:
  run_id: <uuid>
  date: <ISO>
  campaigns_monitored: <int>
  decisions_summary:
    continue: <int>
    slow_down: <int>
    swap_copy: <int>
    pause: <int>
    resume: <int>
  alerts_emitted: <int>
  next_monitoring_eta: <ISO>

per_campaign:
  - campaign_id: <uuid>
    state_before: active | paused | ...
    state_after: <transition or unchanged>
    metrics_snapshot:
      reply_rate: <float>
      positive_reply_rate: <float>
      meeting_rate: <float>
      bounce_rate: <float>
      complaint_rate: <float>
      unsubscribe_rate: <float>
      open_rate: <float — REPORTED, not optimized>
      per_channel:
        email: { reply_rate, bounce_rate, complaint_rate, sends }
        linkedin: { acceptance_rate, message_reply_rate, connects, messages }
        call: { connect_rate, conversation_rate, voicemail_rate, dials }
    sender_reputation:
      google_postmaster: high | medium | low | bad
      microsoft_snds: green | yellow | red
      talos_intel: positive | neutral | negative
      trend_7d: improving | stable | degrading
    decision: continue | slow-down | swap-copy | pause | resume | abort
    triggers: [<threshold breach names>]
    action_taken: <description>
    reason: <one-sentence>
    next_review: <ISO>

ab_tests:
  - test_id: <uuid>
    campaign_id: <uuid>
    variants: [<variant a stats>, <variant b stats>]
    method: bayesian | frequentist
    posterior_or_p_value: <float>
    effect_size_pp: <float>
    recommendation: ship-variant-<x> | inconclusive-stop | continue-collecting
    confidence: <description>
```

## Worked Example

> *All fictional entities below are tagged `[hypothetical]` — illustrative only.*

**User prompt**: "Daily review of our active WorkflowDoc campaign cmp_workflowdoc_t1_mc_2026-05-22 [hypothetical]."

**Step 1 — Pull metrics** (D+8 of campaign):
- Sends sent: 152 emails, 28 LI connects, 8 calls
- Replies: 7 positive, 3 not-now, 2 not-interested → 12 total replies / 152 emails sent = **email reply rate 7.9%** ✓
- LI: 11 accepted / 28 = **connection-acceptance 39%** ✓
- Calls: 1 connected / 8 = **connect rate 12.5%** ✓
- Bounces: 4 hard / 152 = 2.6% (above 2% warn threshold)
- Complaints: 0
- Open rate: 38% (informational only)
- Postmaster Tools: Medium (was Medium 7d ago — stable)
- SNDS: green
- TalosIntel: neutral

**Step 2 — Compare against thresholds**:
- Bounce rate 2.6% > 2% warn threshold → warn (slow-down candidate)
- Complaint rate 0% — nominal
- Postmaster Medium stable — nominal
- Reply rate 7.9% — well above 3% floor
- LI acceptance 39% — well above 12% floor
- Call connect 12.5% — above 6% floor
- LI account safety: green

**Step 3 — Decision**: Slow-down. Bounce rate slightly above warn threshold; no other flags.

Action: reduce email daily volume from 30/mailbox to 15/mailbox for 24h; re-eval tomorrow. LI + call unchanged. Reason: avoid bounce-rate accumulation that could trip pause threshold (5%); list-quality issue suspected on a recent batch.

**Step 4 — A/B test check**: No A/B test active on this campaign.

**Step 5 — Diagnose** (slow-down doesn't require diagnosis; swap-copy does — skip).

**Step 6 — Adjustments log entry**:
```yaml
- timestamp: 2026-05-30T10:00:00Z
  decision: slow-down
  triggers: [bounce-rate-warn-threshold]
  metrics_snapshot:
    bounce_rate: 0.026
    bounce_count_24h: 2
    sends_24h: 30
    bounce_rate_cumulative: 0.026
  action_taken: "Reduced email daily volume from 30/mailbox/day to 15/mailbox/day for 24h. LI + call unchanged."
  reason: "Bounce rate 2.6% exceeds 2% warn threshold; preventive slow-down to avoid 5% pause threshold."
```

**Step 7 — Notify user** (Slack alert):
> "⚠️ Campaign cmp_workflowdoc_t1_mc_2026-05-22 — bounce rate 2.6% (above 2% warn). Email volume reduced to 50% for 24h. Re-eval tomorrow at 10am UTC. Reply rate healthy at 7.9%."

**Step 8 — Push to CRM**:
```bash
# interaction:research with adjustment decision
# Campaign record state stays 'active' (slow-down doesn't change state)
# metrics_summary updated
```

**Step 9 — Next monitoring cycle**: scheduled for D+9 at 10am UTC.

---

**Day +9 update** (illustrative continuation):
- Bounce rate dropped to 1.8% (below 2% warn threshold) — slow-down rescinded.
- Action: restore email volume to 30/mailbox; log `decision: continue`.

## Heuristics

- **Pause is cheap; un-pausing is cheap; ignoring a complaint-rate spike isn't.** Err on the side of pausing. The cost of a 30-minute pause is zero; the cost of letting a Postmaster reputation tank is weeks of recovery.
- **Reply rate is the primary metric.** Open rate is noise (Apple MPP). Click rate is a weak proxy. Reply is the truth.
- **3% reply rate by D+10 is the floor for cold email.** Below = broken. Multi-channel raises this to 6%.
- **Bounce rate spike usually means list quality.** Recent batch had stale emails or catch-all-domain misclassified. Audit upstream `data-enrichment`.
- **Complaint rate spike usually means messaging mismatch.** Wrong audience for the offer; copy too aggressive; subject-line clickbait. Pause + diagnose copy + re-enrichment if needed.
- **Postmaster "Medium → Low" trend is the canary.** Don't wait for "Bad"; slow down at "Medium-trending-down."
- **Don't ship A/B winners on n<50.** Statistically meaningless and ops-noisy.
- **Don't optimize across micro-arms.** Two variants is the sweet spot; three+ explodes data requirements without lifting decision quality.
- **Same-channel rate trends matter more than absolute rates.** A campaign at 4% reply rate that's been at 4% for 5 days is fine; a campaign that dropped from 7% to 4% in one day is alarming.
- **LI account safety degrades fast.** Amber-warning needs same-day pause, not next-day.
- **Apple MPP makes "best time to send" experiments noisy.** Don't run send-time experiments on open rate; only on reply rate.
- **A campaign past D+21 with no replies isn't going to magically perform.** Mark complete; learn from it; move on.

## Edge Cases

- **Sending platform's webhook fails.** Fall back to polling; degrade frequency if rate-limited; warn user about lag in detection.
- **Campaign launched without `multi-channel-cadence`** (manual launch directly to sending tool). Skill can still monitor if metrics-feed is connected; surface that the campaign lacks structured metadata for some decisions.
- **Multiple A/B tests on the same campaign**. Treat independently; surface combined risk if multi-test interactions matter.
- **Reputation drop without obvious cause.** Audit recent batches for spam-trap hits (DNS-validated patterns); audit recent unsubscribe spikes; recommend `email-infrastructure-setup` recovery mode if Postmaster shows "Bad".
- **GDPR-light cadence with low reply rate.** EU/UK reply rates structurally lower than US; adjust expectations (target ≥2% for GDPR-light vs 3% for standard).
- **Account-based campaign with high inter-account variance.** Some accounts pull ahead, some lag. Don't average — look at distribution; flag tail accounts for manual outreach.
- **Campaign past D+21 still showing positive replies.** Extension is fine for warm responders; new prospects at D+21 are stale (cadence design issue — don't add new prospects to old campaigns).
- **Sender reputation feeds disagree.** Postmaster says "Medium", SNDS says "Red" — pause; investigate (often Microsoft is more sensitive to recent bursts).
- **Volume cap hit before cadence completes.** Some recipients don't get all their touches. Flag; either extend duration or accept partial-cadence delivery on tail.
- **User overrides pause manually.** Honor; require explicit "I accept the risk" and log; don't auto-pause again on same trigger within 24h.
- **Test variant beats control by 5pp on n=30 each.** Don't ship — sample too small; recommend continuing or accepting inconclusive.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Sending platform metrics API fails | 5xx | Backoff; degrade to less frequent polling; warn user. |
| Postmaster Tools OAuth expired | 401 | Prompt for re-auth; degrade to bounce + complaint signals only. |
| Reputation feeds disagree (one source missing) | partial data | Use available sources; mark `[unverified — needs check]` for the missing dimension; warn user. |
| User-set thresholds invalid (e.g. complaint cap >0.3%) | warn at config time | Allow with explicit `risk_accepted: true` flag; log. |
| Campaign metrics inconsistent (sending platform shows 1000 sends, CRM shows 980) | reconciliation lag | Use sending platform as source of truth; surface delta; reconcile next cycle. |
| Pause decision triggered but campaign already paused | no-op | Log "no action — already paused"; do not double-pause. |
| Concurrent monitoring runs collide | two scheduler instances | Use distributed lock; second instance no-ops; warn ops. |
| A/B test variant ids mismatched | data-quality issue | Surface; refuse to call winner; require user ack. |
| User asked to abort active campaign | manual decision | State transition `active → aborted`; cancel scheduled future Touches; log; not reversible. |
| Sender reputation drops mid-cycle | Postmaster moved Medium → Bad in 12h | Pause immediately; do not wait for next polling cycle; alert via highest-priority channel. |

## Pitfalls

- **Optimizing on open rate.** Apple MPP made it noise. Reply / meeting rate only.
- **Ignoring complaint-rate spikes.** Hard rule from Google/MS Feb 2024; pause at 0.3%.
- **Slow-down without re-eval.** Slow-downs without next-cycle review become silent under-performance.
- **Pause without notification.** User needs to know; ack to resume.
- **Auto-resume after manual pause.** Manual pauses are user-judgment; don't auto-resume on threshold recovery.
- **Calling A/B winners early.** n<50 = noise; ship a "winner" that's actually a coin flip.
- **Treating reputation feeds as gospel.** Feeds disagree; cross-check; pause on convergent signal.
- **Adjusting too frequently.** Daily + a few hard-pauses is the right cadence; per-hour is theater.
- **Letting LI account amber linger.** 7-day cool-down is non-negotiable.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (campaigns, recipients, metric values, dates, decision rationale) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. NEVER invent a Postmaster Tools verdict, a metric value, or a decision rationale without the source.
- **Not logging "continue" decisions.** Audit trail is incomplete if only changes are logged; "continue" needs a record too.

## Verification

The monitoring run is real when: (a) every active campaign has a decision logged with metrics_snapshot at the timestamp; (b) all pause-threshold breaches resulted in actual state transitions (not just warnings); (c) sender reputation feeds were pulled from the named tools (or `[unverified]` flagged when unavailable); (d) A/B test winners (when called) had explicit posterior / p-value AND effect size; (e) re-running the same monitoring cycle on the same metrics produces the same decision (deterministic decision rubric).

## Done Criteria

1. Active campaigns enumerated; metrics pulled per campaign.
2. Reputation feeds pulled (or `[unverified]` flagged when unavailable).
3. Decision rubric applied per campaign; one of {continue, slow-down, swap-copy, pause} chosen.
4. A/B tests evaluated when applicable; winner called only at significance + effect-size thresholds.
5. Plateau diagnosis run when swap-copy triggered.
6. Adjustments_log entry written per campaign per cycle (including "continue").
7. User notified on pause / slow-down / swap-copy via preferred channel.
8. CRM push: state transitions + metrics summary updated; one `interaction:research` per decision.
9. Next monitoring cycle scheduled.

## Eval Cases

### Case 1 — healthy campaign mid-flight

Input: D+8 active campaign; reply rate 7.9%; bounce 2.6% (warn); complaint 0; Postmaster Medium stable.

Expected: slow-down decision (bounce-rate warn); email volume halved; re-eval next cycle. Reply / connection / call rates above floors → no swap-copy. State stays `active`.

### Case 2 — hard-pause on complaint-rate spike

Input: D+5 active campaign; complaint rate 0.42% (above 0.3% pause); reply rate 6%.

Expected: state transition `active → paused`; immediate user notification (high priority); diagnosis recommendation (audit recent batches for spam-trap or wrong-audience signals); user must explicitly ack to resume.

### Case 3 — A/B test winner declared

Input: D+12 of 21d cadence; A/B test on opener angle; n=180/180 per arm; variant B reply rate 6.2% vs variant A 4.1%.

Expected: Bayesian posterior `P(B > A)` > 0.95; effect size 2.1pp ≥ 1pp; recommend ship variant B for remaining cadence. Log decision; transition allocated traffic to B.

### Case 4 — reply rate plateau triggers swap-copy

Input: D+10 of 21d cadence; reply rate 1.8% (below 3% floor); deliverability healthy.

Expected: swap-copy decision; diagnose: hook quality (60% `[unverified]` hooks suggests `data-enrichment` weakness) + cliché audit (3 phrases caught); recommend re-enrichment + copy rewrite via `cold-email-sequence` rewrite mode.

### Case 5 — multi-campaign daily review

Input: 5 active campaigns; mixed states.

Expected: per-campaign decisions surfaced; summary: 3 continue / 1 slow-down / 1 swap-copy; no pauses; cross-campaign reputation summary (one shared sender pool — flag if shared metrics show degradation).

## Guardrails

### Provenance (anti-fabrication)

Per §10 of conventions: every metric value carries provenance — sending platform API timestamp, Postmaster Tools query timestamp, etc. NEVER invent a metric value or a reputation verdict. Worked-example fictional entities tagged inline.

### Evidence

Every decision is logged with metrics_snapshot at decision time. Adjustments_log is append-only audit trail.

### Scope

This skill monitors and decides. It does NOT write copy (`cold-email-sequence` rewrite mode does that), classify replies (`reply-classification` function-4), or do long-term attribution analysis (`channel-performance` function-6). Decisions are real-time / per-campaign.

### Framing

Decisions are operational, not advisory. "Pause" means pause, not "consider pausing." Notifications use plain ops language with metrics and threshold breach explicit.

### Bias

Threshold defaults are calibrated for US-centric SaaS markets. Other markets (EU low-volume / regulated industries) may need looser thresholds; user can override per campaign. Surface defaults explicitly so override is informed.

### Ethics

Pause-threshold breaches are non-negotiable when they reflect compliance (GDPR opt-out signal in unsub spike; Google/MS bulk-sender complaint rate). Don't bend.

### Freshness

Reputation feeds refresh slowly (Postmaster Tools daily; SNDS daily). Don't poll faster than that. Sending-platform metrics can be near-real-time but cumulative metrics need 24h+ to stabilize.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Pause triggered, infrastructure suspect | `email-infrastructure-setup` (recovery mode) | Postmaster verdict + recent metrics |
| Swap-copy triggered, copy weak | `cold-email-sequence` (rewrite mode) | Cliché audit + hook quality assessment |
| Swap-copy triggered, hooks weak | `data-enrichment` (re-enrichment) | Records lacking verified hooks |
| Swap-copy triggered, list weak | `lead-scoring` (re-tier) | Reply distribution by tier |
| Replies arriving need classification | `reply-classification` (function-4, planned) | Reply text + Touch ids |
| Long-term attribution analysis | `channel-performance` (function-6, planned) | Multi-campaign metrics history |
| Weekly KPI report | `kpi-reporting` (function-6, planned) | All campaigns' metrics summary |
| LI account safety amber | `linkedin-outreach` (cool-down) | Account state |
| New campaign launch | `multi-channel-cadence` | New cadence brief |

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
    "relevance": "Campaign cmp_workflowdoc_t1_mc_2026-05-22. D+8. Decision: slow-down. Triggers: bounce-rate-warn (2.6% > 2% threshold). Metrics: reply rate 7.9% / bounce 2.6% / complaint 0 / Postmaster Medium stable. Action: reduced email volume to 15/mailbox/day from 30 for 24h. LI + call unchanged. Re-eval D+9 at 10am UTC.",
    "source": "skill:campaign-management:v2.0.0"
  }'
```

### Example push (hard-pause)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#alert #campaign-paused #function-3",
    "relevance": "Campaign cmp_workflowdoc_t1_mc_2026-05-22. D+5. State: active → paused. Triggers: complaint-rate-pause (0.42% > 0.3% threshold). Recent 24h: 152 sends, 0.64 complaint rate. Cross-check: Postmaster Tools shows 'Low' (was Medium yesterday). Action: stopped all email sends; LI + call unchanged. User must ack to resume. Recommend: audit recent batches for wrong-audience signals; consider list-quality review via data-enrichment.",
    "source": "skill:campaign-management:v2.0.0"
  }'
```

### Example push (A/B test winner)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#ab-test-winner #function-3",
    "relevance": "A/B test ab_t1_opener_2026-05-22 on campaign cmp_workflowdoc_t1_mc_2026-05-22. D+12. Variant A (CCQ + Pain): 4.1% reply rate (n=180, 7 replies). Variant B (CCQ + Vision): 6.2% reply rate (n=180, 11 replies). Method: Bayesian. Posterior P(B > A) = 0.96. Effect size: 2.1pp. Recommendation: ship variant B for remaining cadence. Action: traffic shifted 100% to variant B.",
    "source": "skill:campaign-management:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Decision logged + state transitions executed per standard mapping. |
| `[unverified — needs check]` | Decision is marked partial (e.g., reputation feed unavailable); pushes as `interaction:research` with `#unverified #review-required #campaign-management` tag; decision deferred or made with explicit caveat. |
| `[hypothetical]` | Never executed; never pushed. Local artifact only. |

### When NOT to push

- Monitoring cycle ran but no decisions changed (pure "continue" across all campaigns) — push a single periodic summary `interaction:research` per day, not per cycle.
- Metrics feed unavailable for whole cycle — push `interaction:research` with `#monitoring-failed` and the reason; no decisions made.
- `[unverified]` partial data — see provenance routing.
- `[hypothetical]` — never.
- User manually overrode a pause-threshold-triggered pause with `risk_accepted: true` — push the override decision with full audit trail (the override IS push-worthy as accountability record).
