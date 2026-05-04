# Cross-Channel Capacity Planning

## Per-Channel Capacity Caps

| Cap | Default | Notes |
|---|---|---|
| SENDS_PER_DOMAIN_PER_DAY_CAP | 30 | Absolute ceiling 50; new domains start at 5 and ramp |
| SENDS_PER_MAILBOX_PER_DAY_CAP | 30 | Per individual mailbox |
| LINKEDIN_CONNECTS_PER_WEEK_CAP | 80 | LI soft cap ~100; stay below |
| LINKEDIN_MESSAGES_PER_WEEK_CAP | 200 | To existing connections |
| LINKEDIN_INMAIL_PER_MONTH_CAP | 50 | Depends on Sales Nav seat tier |
| CALLS_PER_REP_PER_DAY_CAP | 80 | Warn above 100; productive ceiling |
| VOICEMAILS_PER_REP_PER_DAY_CAP | 40 | |
| CAMPAIGN_TOTAL_RECIPIENTS_CAP | 500 | Force tier-segmentation above this |
| CAMPAIGN_DAILY_VOLUME_CAP | 200 | Across channels |

## Cross-Channel Capacity Calculation

### Step 1: Compute per-channel touches needed

```
email_touches = email_touches_per_recipient × eligible_recipients
li_touches = li_touches_per_recipient × eligible_recipients
call_touches = call_touches_per_recipient × eligible_recipients
```

### Step 2: Compute per-channel headroom

```
email_headroom = email_touches / (sender_pool × per_domain_cap × duration_days)
li_connect_headroom = li_connects / (li_weekly_cap × duration_weeks)
li_message_headroom = li_messages / (li_msg_weekly_cap × duration_weeks)
call_headroom = call_touches / (rep_pool × call_cap × duration_days)
```

### Step 3: If any channel over-capacity

Recommend one of:
- **Tier-segment**: drop Tier-2/3 recipients
- **Extend duration**: spread touches over more days
- **Expand pool**: add sender mailboxes / reps
- **Swap to lighter template**: fewer touches per recipient

## Channel-Isolation Rule

A touch on channel A does NOT directly quote or reference content sent on channel B.

**Forbidden phrases:**
- "As I emailed you yesterday..."
- "Following up on my LinkedIn message..."
- "I sent you a voicemail last week about..."

**Allowed:**
- Same hook/theme referenced independently on different channels
- Implicit continuity (recipient recognizes the name/topic)

**Rationale:**
1. Feels surveillance-y to the recipient
2. Recipients track different channels in different mental contexts
3. Breaks trust before it's established

## Per-Day Spacing Rule

- Max 1 touch per recipient per day
- **Exception**: email + LI-connect on D+0 is acceptable (LI connection is artifact-only, no message)
- Never two same-channel touches same day
- If two touches land same day (template error), spread by 1 day in either direction

## Quiet Hours by Channel

| Channel | Quiet hours (recipient local) |
|---|---|
| Email | 8pm–8am |
| LinkedIn | 8pm–8am weekdays; weekends optional |
| Cold call | Before 8am AND after 9pm (TCPA hard rule for US) |
| SMS | 8pm–8am AND TCPA hours |

## Provenance Routing

| Provenance | Cadence behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Cadence proceeds; pushes per standard mapping |
| `[unverified — needs check]` (from channel skills) | Cadence variant set to "blocked" for affected recipients |
| `[hypothetical]` | Never proceeds; never pushes |
