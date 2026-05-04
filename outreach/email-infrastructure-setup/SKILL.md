---
name: email-infrastructure-setup
description: Set up and verify email infrastructure — dedicated outbound domains, SPF+DKIM+DMARC, RFC 8058 one-click unsubscribe, 14+ day warmup, and emit the readiness flag gating cold-email-sequence. Use when a new outbound program starts, deliverability has degraded, migrating sending platforms, or Google/Microsoft Feb 2024 enforcement breaks an existing sender.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Outreach, EmailInfrastructure, Deliverability, DNS, Warmup]
    related_skills: [cold-email-sequence, multi-channel-cadence, campaign-management]
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

# Email Infrastructure Setup

Establish the deliverability foundation every other email skill depends on: dedicated outbound domains, DNS authentication (SPF+DKIM+DMARC), RFC 8058 one-click unsubscribe, and 14+ day warmup. Emits the binary `readiness_flag` that gates `cold-email-sequence`.

## When to Use

- New outbound program needs email infrastructure from scratch
- Deliverability tanked — audit and fix existing setup
- Migrating sending platforms (Outreach.io → Smartlead, etc.)
- Google/Microsoft sent a bulk-sender warning
- Adding a second outbound domain to scale volume
- Recovery after complaint-rate spike or blacklist event
- Domain warmup score below 70 — need to complete ramp

## Quick Reference

| Concept | Value |
|---|---|
| Reputation isolation | Cold outbound from `brand-mail.com` variant, NEVER brand domain |
| DNS records required | SPF, DKIM (≥2048-bit), DMARC (start `p=none`), MX, rDNS |
| One-click List-Unsubscribe | RFC 8058 — mandatory for >5k/day (Google/MS 2024) |
| DMARC ramp | `p=none` → `p=quarantine` (Day+30 if clean) → `p=reject` (high-stakes) |
| Warmup duration | 21–30 days new/cold; 14-day floor aged domains; 30-day floor >200/day |
| Warmup score threshold | ≥70 to flip readiness flag |
| Domain age threshold | ≥14 days |
| Daily ramp caps | 5/day → +5 every 5 days → 30/day after 14 days |
| Postmaster gate | "High" or "Medium" only; "Low"/"Bad" → extend warmup |
| Complaint thresholds | Target 0.10%; Google enforcement ceiling 0.30% |
| Bulk-sender mode | >5,000/day → mandatory DMARC + 0.3% complaint cap |

## Procedure

1. **Audit existing infrastructure** — If migrating, pull current SPF/DKIM/DMARC via `${HERMES_SKILL_DIR}/references/dns-frameworks.md`. Surface mis-configs before new setup.
2. **Choose dedicated outbound domain(s)** — Propose 2–3 brand variants (`<brand>-mail.com`, `get<brand>.com`). NOT the brand domain. For >200/day plan 2+ domains for rotation.
3. **Register + configure DNS** — Per outbound domain: publish SPF, DKIM (≥2048-bit from sending platform), DMARC (`p=none; rua=...`), MX, rDNS. Watch SPF 10-lookup limit. See `${HERMES_SKILL_DIR}/references/dns-frameworks.md` for record formats.
4. **Configure RFC 8058 one-click List-Unsubscribe** — Both headers on every send. Process unsub within 24h. Mandatory under Google/MS 2024 for >5k/day senders.
5. **Configure jurisdiction-aware footers** — US: physical address (CAN-SPAM). EU/UK: LIA + opt-out + DPO (GDPR). CA: identification + opt-out (CASL). Templates in `${HERMES_SKILL_DIR}/references/compliance-footers.md`.
6. **Initiate warmup ramp** — Day 0: enable platform warmup, cap 5/day. Ramp +5 every 5 days. No shortcuts. Schedule detailed in `${HERMES_SKILL_DIR}/references/warmup-schedule.md`.
7. **Run reputation baseline (Day+14)** — Pull Google Postmaster, Microsoft SNDS, TalosIntel, MXToolbox. Cross-check; want Postmaster High/Medium, SNDS green/yellow.
8. **Emit readiness flag** — All gates pass → `readiness_flag: true` + `ready_for_sends_per_day`. Any gate fails → false + `failed_gates` + remediation.
9. **Push to CRM** — Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py` with the setup record. Infrastructure is system-state (not entity-state) — pushes as `interaction:research` only.

## Pitfalls

- **Sending from the brand domain** — reputation contamination is unrecoverable
- **Skipping warmup** — Day-1 cold-blast = instant blacklist
- **DMARC straight to `p=reject`** — breaks transactional + reply email
- **1024-bit DKIM keys** — Yahoo treats as deprecated; Google deprioritizes
- **No List-Unsubscribe header** — auto-spam under Google 2024 rules
- **No physical address (CAN-SPAM US)** — legal violation

## Verification

1. Every DNS record resolves correctly via MXToolbox + dig; one-click unsubscribe processes test request within 24h; physical address renders in test emails
2. Postmaster Tools and SNDS both show valid baseline (not "Bad"/red); warmup score climbs per ramp schedule
3. Test send to real Gmail and real Outlook inboxes both land in primary tab
