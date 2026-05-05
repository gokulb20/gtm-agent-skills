---
name: linkedin-outreach
description: Execute LinkedIn outreach via Sales Navigator + session-based tools — connection requests with ≤300 char notes, follow-up messages, InMails — with strict LinkedIn ToS compliance, weekly rate limits, and personalization-hook enforcement. Use when email is the wrong channel, LinkedIn URL is the strongest identity signal, the play is relationship-first social-selling, or multi-channel cadence requires a LinkedIn leg.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Outreach, LinkedIn, SocialSelling, ConnectionRequests]
    related_skills: [cold-email-sequence, cold-calling, multi-channel-cadence, campaign-management]
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

# LinkedIn Outreach

Execute LinkedIn-channel touches — connection requests, messages to existing connections, InMails — through session-based tools or manual Sales Nav UI. Hard-codes ToS compliance (NO direct scraping), respects weekly rate limits, gates every touch on the personalization-hook contract.

## When to Use

- Email is wrong channel — risky/catch-all email status, email-fatigued segments
- LinkedIn URL is strongest identity signal in Lead schema
- Relationship-first social-selling play
- Multi-channel cadence requires a LinkedIn leg
- Email reply rate plateaued <2% on a segment
- Pre-launch with high LI URL coverage (>80%)

## Quick Reference

| Concept | Value |
|---|---|
| Risk-tiered modes | ✅ Manual/native (PRIMARY); ⚠️ Desktop session; 🔴 Cloud automation (high ban risk); 🔴 "API" = does NOT exist |
| Connection note | ≤300 chars, NO URL, NO emoji, single CTA |
| Connection requests/week | ≤80 (default); ≤150 high-SSI only; rolling 7-day reset |
| Daily distribution | 15–25/day max; never bulk-burst |
| Free-account notes cap | 5/month (new since 2023) |
| InMail limits | 25/day Premium; 1,000/week Recruiter (Tier-1 only) |
| Account safety | Green only; amber/red = 7-day cool-down |
| Acceptance rate target | 15–25% healthy; <12% = copy/targeting broken |
| Optimal send time | Weekday 9am–5pm recipient local; Tue–Thu best |
| Hook gate | Event-based + content-engagement need citable URL |
| GDPR (EU/UK) | `gdpr_basis: legitimate-interest` + opt-out in follow-up |

## Procedure

1. **Validate prerequisites** — Read scored Leads with verified LinkedIn URLs; load ICP P-T-O + message house; check LI account state (age, SSI, dormancy). Block on gate failures. If dormant, surface activity-warmup.
2. **Determine mode (risk-tiered)** — Manual/native → PRIMARY. Desktop session → acceptable with caveats. Cloud automation → NOT recommended; surface HeyReach Dec 2024 precedent + require explicit risk-ack. "API" → REFUSE (no LinkedIn outreach API exists). Direct-scraping → REFUSE. See `${HERMES_SKILL_DIR}/references/li-tos-compliance.md`.
3. **Filter recipient list** — Drop no-LI-URL; drop EU/UK without LIA; apply tier filter; dedup against active email cadences.
4. **Pre-flight: capacity check** — Weekly: 80 connects/150 high-SSI / 200 messages / 50 InMail monthly. Enforce 5/month notes (free accounts). Distribute 15–25/day. Reference `${HERMES_SKILL_DIR}/references/li-rate-limits.md`.
5. **Pick framework + generate copy** — Warm-intro / Event-based (citable URL) / Content-engagement (prior interaction). Generic-no-context refused → review queue. Connection note ≤300 chars, no URL, single CTA. Follow-up 2–3 sentences post-accept. InMail 4–6 sentences (Tier-1 only).
6. **Compose Touch records** — Per conventions §2.1: channel `linkedin-connect/message/inmail`, full provenance, scheduled_for (weekday 9am–5pm), GDPR compliance.
7. **Schedule via tool or hand off** — Manual: paste-ready notes + per-touch schedule + runbook. Desktop: campaign at safe pace (4–5/day). Cloud (if authorized): explicit risk-ack persisted.
8. **Push to CRM + run summary** — Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`. Run summary: eligible/dropped counts, framework distribution, capacity headroom, account safety, recommended next skill.

## Pitfalls

- **Cloud tools can disappear overnight** — HeyReach Dec 2024: page deleted, founders banned, retroactive flagging
- **No LinkedIn outreach API exists** — SNAP paused new partners Aug 2025; any "API" = unofficial reverse-engineered = ban risk
- **Direct scraping is a ToS violation** — hiQ settlement Nov 2022; Bright Data v. Meta Jan 2024
- **Skipping account state pre-check** — sudden activity on dormant account = instant red flag
- **Bulk-bursting weekly cap on Day 1** — rolling 7-day reset (NOT calendar week)
- **Forgetting 5/month personalized-note cap on free accounts**
- **Generic connection notes / URLs in notes** — auto-rejected, flagged

## Verification

1. Zero notes >300 chars or with URLs; every event-based/content-engagement Touch has citable hook URL; zero sends on "API" mode
2. Rolling 7-day cap respected; daily distribution 15–25; acceptance ≥12% by D+7
3. Account safety stays green; cloud-mode runs have explicit user risk-ack persisted
