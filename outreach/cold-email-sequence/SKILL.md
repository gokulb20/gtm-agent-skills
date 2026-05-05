---
name: cold-email-sequence
description: Write cold email sequences (5–7 touch, 14–21 day) using the CCQ copy framework, Pain-Trigger-Outcome openers, mobile-first formatting, and a hard ban on cliché openers. Gates every touch on the personalization-hook contract and email_status. Use when a Tier-1/2 lead list is enriched and scored, an ICP-grounded outbound burst is being planned, or an existing sequence's reply rate is below the 3% floor.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Outreach, ColdEmail, SequenceDesign, CopyWriting]
    related_skills: [email-infrastructure-setup, linkedin-outreach, multi-channel-cadence, campaign-management]
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

# Cold Email Sequence

Produce a 5–7 touch cold email sequence (14–21 day arc) using the CCQ copy framework. Each touch is grounded in the recipient's verified personalization hook, formatted mobile-first, and audited for clichés before send. Hard rule: touch with `[unverified — needs check]` hook is BLOCKED and routed to review queue.

## When to Use

- Tier-1/2 enriched lead list ready for outbound copy
- Reply rate below 3% floor — diagnose and rewrite
- Need A/B variants for opener testing
- Sending from Gmail natively — need drafts + per-touch runbook
- Pre-launch copy generation when leads are enriched + scored
- Existing sequence flagged by campaign-management for reply-rate breach

## Quick Reference

| Concept | Value |
|---|---|
| Default sequence | 5–7 touches over 14–21 days; day_offsets 0/3/7/11/15/19/45 |
| Default framework | CCQ (Context/Compliment-or-Connection/Question) |
| Word targets | Subject ≤8 words; opener body 50–80; later touches 40–100 |
| Per-touch frameworks | T1 CCQ+Pain; T2 CCQ+Vision; T3 RTA; T4 Compelling-Event; T5 Outcome-proof; T6 Break-up; T7 Resurrection (D+45) |
| Hard hook rule | `personalization_hook [verified]` OR Touch BLOCKED |
| Hard email_status rule | Drop `risky`/`role-based`/`catch-all-domain`/`invalid` |
| Cliché blocklist | "I hope this finds you well" / "I noticed" / "we help X do Y" / multi-question CTAs |
| Buzzword blocklist | flexibility, visibility, scalable, strategic, leverage, synergy, robust, holistic |
| Mobile format | ≤2-line opener / one CTA / ≤4-line paragraphs / ≤3-line signature |
| Quiet hours | 8pm–8am recipient local + weekday-only |
| Per-domain cap | 30/day (50 absolute ceiling) |
| Primary metric | Reply rate ≥3% floor (5–10% solid; 10%+ excellent) |

## Procedure

1. **Validate prerequisites + determine mode** — Read scored Leads, ICP P-T-O, message house, infrastructure readiness flag. API key → API mode; seat → manual; native → BYO. Block if any gate fails.
2. **Filter recipient list** — Drop bad `email_status`; drop unverified hooks (route to review queue); apply tier filter; split GDPR jurisdiction. See `${HERMES_SKILL_DIR}/references/ccq-framework.md` for framework rules.
3. **Pre-flight: capacity check** — Compute `eligible × sequence_length` vs `per-domain cap × pool × duration`. Surface; wait for authorization if over capacity.
4. **Generate per-touch copy + audit** — Per recipient × position: pick framework per touch default; draw verified hook; compose subject (≤8 words) + body (within target); inject List-Unsubscribe header + physical address (CAN-SPAM) or LIA + opt-out (GDPR). Each draft passes cliché + word-count + mobile-format + buzzword audit; failures regenerate; second-fail surfaces for review.
5. **Compose Touch records** — Per conventions §2.1: full provenance on content/compliance/provenance.copy; `scheduled_for` (quiet-hours + weekday). Reference `${HERMES_SKILL_DIR}/references/push-to-crm-mapping.md` for CRM field mapping.
6. **Build cadence + schedule** — Per conventions §2.2: 5–7 touches at default day_offsets. API → create sequence in tool; manual → paste-ready config; BYO → per-touch runbook.
7. **Push to CRM + run summary** — Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py` per touch. One-screen summary: eligible count, dropped counts, capacity headroom, audit flags, recommended next skill.

## Pitfalls

- **Optimizing on open rate** — Apple MPP made it noise; reply rate is primary
- **Generic openers** — "I noticed your company…" with no specific verified detail = low reply rate
- **Long emails** — >125 words drops reply rate sharply; 50–80 is opener sweet spot
- **Multiple CTAs** — Two questions in close = no answer
- **Buzzword stuffing** — Each buzzword costs ~3% reply rate
- **Skipping the break-up** — Touch 6 break-up generates real replies

## Verification

1. Every Touch's `provenance.copy` resolves to a hook URL or carries `[user-provided]` for outcome claims; reply rate ≥3% by D+10
2. Bounce rate <2% (warn) / <5% (pause); complaint rate <0.1% (target) / <0.3% (pause)
3. Zero touches sent during quiet hours/weekends; zero touches with cliché-blocklist phrases
