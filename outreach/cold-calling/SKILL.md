---
name: cold-calling
description: Generate cold-call scripts (9-second opener, discovery questions, gatekeeper-handler, ≤15-second voicemail) and orchestrate dial sessions with TCPA-compliant DNC scrubbing, quiet-hours enforcement, and call-disposition logging. Use when Tier-1 SAL-eligible prospects have verified phone_status, email+LinkedIn channels have plateaued, high-stakes accounts need live-voice contact, or multi-channel cadence requires a call leg.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Outreach, ColdCalling, Dialer, TCPA, DNC]
    related_skills: [cold-email-sequence, linkedin-outreach, multi-channel-cadence, campaign-management]
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

# Cold Calling

Produce TCPA-compliant cold-call scripts and orchestrate dial sessions for Tier-1 prospects with verified phone numbers. Outputs: 9-second opener, discovery questions, gatekeeper handler, ≤15-second voicemail drop. Hard rules: no calls to DNC/invalid; no calls before 8am or after 9pm recipient local; SMS to mobile requires prior consent.

## When to Use

- Tier-1 SAL-eligible prospects have verified mobile/landline phones
- Email + LinkedIn channels have plateaued (<2% reply)
- High-stakes accounts need live-voice contact
- JustCall/Aircall/Orum configured — need dial campaign setup
- Founder-led calls — need discovery questions and opener
- Multi-channel cadence needs a call leg
- Post-meeting no-show rescue

## Quick Reference

| Concept | Value |
|---|---|
| Hard gates | DNC scrub mandatory; quiet hours 8am–9pm recipient local; verified phone status |
| Phone-status drops | `dnc` (always); `invalid`; `unverified` → data-enrichment |
| 9-second opener | Greet → state cold-call honestly → 5s purpose → permission ask. ≤30 words |
| Discovery framework | Bosworth pain→impact→buying-vision + Sandler Pain Funnel (4–6 questions) |
| Gatekeeper response | 3 patterns: specific-pain / honest cold-call / permission-ask. NEVER pretend |
| Voicemail drop | ≤15 seconds spoken (≤45 words). Name + reason + callback x2 |
| Cadence | 3 attempts over 5 days; D+0/D+2/D+4 |
| Caps | 80 calls/rep/day (warn >100); 40 voicemails/rep/day |
| Connect rate target | 8–12% healthy; <6% = bad targeting/list/timing |
| Voicemail-to-callback | 1–3% (compounding across multi-touch) |
| Optimal time | 10am–noon, 2pm–4pm recipient local; Tue–Thu best |
| Compliance | TCPA hours, DNC scrub ≤30 days old, B2B-cellphone treated as restricted |

## Procedure

1. **Validate prerequisites + determine mode** — Read scored Leads with phone_status; load ICP P-T-O + message house; verify DNC scrub for US recipients. Dialer API → API mode; seat → manual; BYO → runbook. Block on gate failures.
2. **Filter recipient list** — Drop `phone_status: dnc | invalid | unverified`; apply tier filter (Tier-1 SAL); drop unknown-timezone; drop called-within-90d.
3. **Pre-flight: capacity check** — Compute total dials vs `CALLS_PER_REP_PER_DAY_CAP × rep_count × duration`. Surface; recommend multi-rep/extended if over.
4. **Generate scripts** — Per recipient: 9s opener (≤30 words); 4–6 discovery questions (Bosworth + Sandler); gatekeeper handler (3 patterns); voicemail (≤45 words). See `${HERMES_SKILL_DIR}/references/call-scripts-framework.md`. Audit: word-count + cliché blocklist + no-pretend rule + hook citation.
5. **Compose Touch records + schedule** — Per conventions §2.1: channel `call`/`voicemail`; full provenance; scheduled_for (TCPA 8am–9pm); compliance metadata. Reference `${HERMES_SKILL_DIR}/references/tcpa-compliance.md`.
6. **Capture call disposition** — Per dial: `connected-positive` / `connected-not-now` / `connected-not-interested` / `voicemail-left` / `no-answer` / `wrong-person` / `bad-number`. Route per disposition.
7. **Push to CRM + run summary** — Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. Per dial as `interaction:outreach` with disposition. Run record: dial volume, connect rate, meeting-booked rate, recommended next skill.

## Pitfalls

- **Calling DNC numbers** — TCPA fines $500–$1500 per violation
- **Calling outside 8am–9pm recipient local** — same penalty
- **SMS to mobile without prior consent** — same penalty
- **Pretending prior conversation** — dishonest, illegal in some jurisdictions
- **No permission ask** — launching into pitch in second 3
- **Voicemail >15 seconds** — long voicemails get deleted
- **Skipping discovery to pitch** — "We do X for Y, can we book a demo?" fails

## Verification

1. 100% of dials have DNC scrub ≤30 days old; 100% within TCPA 8am–9pm recipient local hours
2. Every Touch's provenance resolves to hook URL or is honest cold-call pattern; connect rate ≥6%
3. Zero "pretend prior conversation" violations; voicemail word count ≤45
