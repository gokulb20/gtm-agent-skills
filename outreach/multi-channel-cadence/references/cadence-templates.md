# Cadence Template Library

## Standard Templates

### email-only-5touch-19d
- **Length**: 5 touches over 19 days
- **Channel mix**: E E E E E
- **Use case**: Hook-rich list; email infrastructure mature; no LI/phone coverage
- **Day offsets**: 0/3/7/11/19

### email-li-5touch-19d
- **Length**: 5 touches over 19 days
- **Channel mix**: E LI-connect E E E
- **Use case**: Standard multi-channel light; LI URL coverage >70%
- **Day offsets**: 0/2/5/11/19

### email-li-call-7touch-21d (DEFAULT)
- **Length**: 7 touches over 21 days
- **Channel mix**: E LI-connect E Call E LI-msg E
- **Use case**: Full multi-channel; all channels ready
- **Day offsets**: 0/2/5/9/12/16/20

| Position | Channel | Day offset | Framework |
|---|---|---|---|
| T1 | Email | 0 | CCQ + Pain |
| T2 | LinkedIn connect | 2 | Event-based |
| T3 | Email | 5 | CCQ + Vision |
| T4 | Cold call | 9 | CC20 + Sandler |
| T5 | Email | 12 | RTA / resource share |
| T6 | LinkedIn message | 16 | Post-accept follow-up |
| T7 | Email | 20 | Break-up |

### tier-1-9touch-30d
- **Length**: 9 touches over 30 days
- **Channel mix**: E LI-connect E Call E LI-msg Call E E (break-up)
- **Use case**: Tier-1 SAL-eligible prospects; high-value accounts
- **Day offsets**: 0/2/5/9/12/16/20/25/30

### abm-3thread-21d
- **Length**: 21 days
- **Channel mix**: 3 threads × (E LI-connect E Call E LI-msg E) per company
- **Use case**: Account-based; 3 contacts per company
- **Special rules**: Stagger across reps to avoid same-account same-week pile-up; cross-thread dedup if same recipient

### email-fatigue-relief-3touch-7d
- **Length**: 3 touches over 7 days
- **Channel mix**: LI-connect Call E
- **Use case**: When email channel is fatigued; short relief burst
- **Day offsets**: 0/3/7

### gdpr-light-4touch-21d
- **Length**: 4 touches over 21 days
- **Channel mix**: E E E (break-up with explicit opt-out)
- **Use case**: EU/UK recipients; conservative pacing; explicit opt-out at every touch
- **Day offsets**: 0/7/14/21

## Template Adaptation Rules

When a recipient lacks a channel, adapt the template:

| Missing channel | Adaptation |
|---|---|
| No LinkedIn URL | Swap LI touches for email with different angle/framework |
| No verified phone | Drop call touches; extend email/LI spacing |
| EU/UK without LIA | Swap to `gdpr-light-4touch-21d` |
| All channels missing for recipient | Drop recipient; surface in filter report |

## Branch Rules (All Templates)

| Condition | Action |
|---|---|
| LI-connect-accepted | Swap next scheduled email to LI-message personalized on acceptance |
| Email-bounce (hard) | Drop all email touches; keep LI + call if available |
| Reply-positive | Exit cadence on that recipient; handoff to discovery-call-prep |
| Reply-negative | Exit cadence; flag for objection-handling-library |
| Unsubscribe | Exit ALL channels (global respect, not channel-specific) |
| Manual-stop | Honor immediately; in-flight touches complete |

## Exit Conditions (All Templates)

`reply-positive` / `reply-negative` / `bounce` / `unsubscribed` / `manual-stop` / `cap-hit-without-completion`
