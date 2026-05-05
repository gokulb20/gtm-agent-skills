# TCPA Compliance & DNC Rules

## TCPA (Telephone Consumer Protection Act) — 47 USC § 227

### Hard Rules

1. **National DNC Registry**: scrub before any cold-call run. Personal mobile numbers on DNC require prior consent.
2. **State DNC lists**: scrub for relevant states (TX, FL, MA have stricter rules).
3. **Quiet hours**: 8am–9pm recipient local time. Hard rule for calls.
4. **SMS to mobile**: prior express written consent required for marketing SMS.
5. **B2B-to-B2B-cellphone**: gray area; treat as TCPA-restricted by default.
6. **Prerecorded auto-dial**: illegal without consent (TCPA § 227(b)).
7. **"Press 1 to be removed"**: honor immediately; mark `phone_status: dnc-internal`.

### DNC Scrub Requirements

| Requirement | Value |
|---|---|
| Freshness | ≤30 days old (recommended); some states require shorter |
| Sources | DNC.com API, ContactCenterCompliance.com, internal DNC list |
| Frequency | Before every dial campaign; stale scrubs = compliance risk |
| Cost of violation | $500–$1,500 per call (statutory damages) |

### Recipient Mid-Call Requests

- "Stop calling" → honor immediately; mark internal-DNC
- "How did you get my number?" → honest answer: "<source>"; never lie
- "Send me an email instead" → comply; mark preference

## Jurisdiction-Specific DNC

| Jurisdiction | Requirement |
|---|---|
| US (Federal) | National DNC Registry; TCPA hours 8am–9pm |
| US (State) | TX, FL, MA, CO, OR have additional state DNC lists |
| Canada (CRTC) | National DNCL; similar quiet hours |
| UK (CTPS/TPS) | Corporate TPS / Telephone Preference Service |
| Australia | Do Not Call Register; similar rules |

## Call Disposition Codes

| Disposition | Next action |
|---|---|
| `connected-positive` | Exit cadence; handoff to discovery-call-prep (function-4) |
| `connected-not-now` | Schedule callback per prospect's stated timing |
| `connected-not-interested` | Exit cadence; flag for objection-handling-library (function-4) |
| `voicemail-left` | Mark in cadence; next touch may reference VM |
| `no-answer` | Next dial attempt next business day |
| `wrong-person` | Flag data-enrichment for correction |
| `bad-number` | Mark `phone_status: invalid`; route for re-verification |

## Power Dialer Considerations

- Orum / ConnectAndSell: multi-line parallel dialing increases connect rate
- "Click to take" UX required — ensures rep is human-paced when prospect connects
- TCPA: prerecorded auto-dial without consent is illegal
- Each rep still respects 80/day connection-attempt cap

## Provenance for Phone Numbers

| Provenance | Dial behavior |
|---|---|
| `[verified: mobile\|landline]` from data-enrichment within 12 months | Dial proceeds |
| `[user-provided]` | Dial proceeds |
| `[unverified — needs check]` | Dial BLOCKED; route to data-enrichment for verification |
| `[hypothetical]` | Never dials; never pushes |
