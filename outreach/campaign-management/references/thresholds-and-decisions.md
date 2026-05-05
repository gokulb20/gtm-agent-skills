# Thresholds & Decision Rubric

## Threshold Table

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

## Decision Rubric

### Pause
Any pause threshold hit → state `active → paused`. User must explicitly acknowledge before resume.

**Immediate actions:**
- Stop all sends on affected channel
- High-priority notification to user
- Diagnosis recommendation (audit recent batches)

### Slow-Down
Any warn threshold hit AND no pause-threshold hit → reduce daily volume by 50%; flag for re-eval in 24h.

**Actions:**
- Reduce email volume from 30/mailbox to 15
- Continue LI + call unchanged (unless those channels triggered)
- Log slow-down with trigger reason

### Swap-Copy
Reply rate / acceptance / connect rate below floor by D+10/D+7/cumulative AND deliverability healthy → call channel skill rewrite mode.

**Diagnosis before recommending:**
1. Audit recent copy against cliché + buzzword blocklists
2. Audit hook quality (% of hooks `[verified]` vs `[unverified]`)
3. Audit recipient quality (Tier-1 SAL vs other)

**Recommend one of:**
- Copy rewrite (if blocklist violations found)
- Re-enrichment (if hooks weak)
- Re-tier (if recipients drifted to Tier-2/3)

### Continue
All metrics nominal → no action; log "monitoring" entry.

## Notification Priority

| Decision | Notification |
|---|---|
| Pause | Immediate, high-priority (Slack/email) |
| Slow-down | Next monitoring cycle |
| Swap-copy | With diagnosis + recommendation |
| Continue | Periodic summary (daily/weekly) |

## Adjustments Log Entry Format

```yaml
- timestamp: <ISO>
  decision: continue | slow-down | swap-copy | pause | resume | abort
  triggers: [<list of threshold breaches>]
  metrics_snapshot: <full metrics at decision time>
  action_taken: <e.g. "Reduced daily volume from 200 to 100">
  reason: <one-sentence>
```

## State Machine

```
draft → active → paused → completed
                ↓         ↑
              aborted   (user ack to resume)
```

- `paused → active`: requires explicit user acknowledgment
- `active → aborted`: user manual decision; not reversible
- All transitions logged in adjustments_log

## Source Priority for Decisions

1. Complaint rate (Google Postmaster + Microsoft SNDS + sending platform)
2. Bounce rate (sending platform)
3. Postmaster Tools reputation drop
4. Reply rate trend
5. A/B test results (only when significant)
