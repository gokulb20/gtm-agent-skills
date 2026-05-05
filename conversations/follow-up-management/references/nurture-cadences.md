# Nurture Cadence Library — Follow-Up Management

## Standard Cadences

### 30-60-90-light
- **Purpose:** Warm not-now without imminent resume date
- **Touches:** 3 (day 30 / day 60 / day 90)
- **Tone:** Low-friction email, value-first (industry insight / case-study link / brief check-in)
- **Channel:** Email (default)
- **Framework:** nurture-light

### 90-180-365-deep
- **Purpose:** Re-engagement for cold-aged leads (6mo+ silence)
- **Touches:** 3 (day 90 / day 180 / day 365)
- **Tone:** Different angle than original cadence; reference prior conversation
- **Framework:** resurrection (from cold-email-sequence touch 7)

### meeting-no-show-rescue
- **Purpose:** Recover a missed discovery call
- **Touches:** 2 (within 24h + day 7 if no reply)
- **Tone:** Low-stakes, single CTA to reschedule; no nag
- **Channel:** Email (default)
- **Framework:** rescue-tone

## Default Nurture Days
`FOLLOW_UP_NURTURE_DEFAULT_DAYS=30` (configurable via env)

## Archive Rule
Nurture-aged recipients past 12 months without engagement → mark `archived`. Re-engagement beyond 365d is rarely worth it.
