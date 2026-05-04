# LinkedIn ToS Compliance & Ban Precedents

## HeyReach Dec 2024 Incident

LinkedIn deleted HeyReach's company page (16.4k followers). Founder, CTO, CRO, CMO all banned. February 2025: cease & desist + API revoked. Northlight reports 40% of HeyReach-associated accounts restricted in Q1 2026.

Same wave hit Apollo + Seamless.ai (March 2024).

## Legal Landscape

| Case | Outcome |
|---|---|
| hiQ v. LinkedIn (9th Cir. Apr 2022) | Public scraping ≠ CFAA violation |
| hiQ v. LinkedIn (Nov 2022 settlement) | Permanent injunction — hiQ admitted User Agreement breach |
| Bright Data v. Meta (Jan 2024) | Logged-in scraping = enforceable ToS violation |

**Implication**: Public scraping is not a federal crime but IS a User Agreement breach. Logged-in scraping is enforceable. Fake accounts for logged-in data = wire-fraud-adjacent. LI can ban + sue.

## LinkedIn Outreach API — Does NOT Exist

- **SNAP (LinkedIn's partner API)**: gated to CRM vendors; paused new partners Aug 2025
- **Messaging API**: prohibits cold automation
- Any tool claiming "API mode" = unofficial reverse-engineered access = ban risk

## ToS Compliance Rules

1. **No direct scraping** — use Sales Navigator + session-based tools on user's own credentials
2. **No buying connections** or InMails outside the platform
3. **Connection-request notes**: ≤300 chars; no sales pitches; no URLs
4. **Account safety**: respect weekly limits; if flagged, pause 7 days
5. **Treat the account like production infrastructure** — every connection = years of network

## Mode Risk Tiers

| Mode | Risk | Notes |
|---|---|---|
| ✅ Manual / native (Sales Nav UI) | None | PRIMARY mode |
| ⚠️ Real-browser / desktop session (Northlight, Linked Helper, Dux-Soup, PhantomBuster browser) | Low-medium | Runs from user's browser/IP |
| 🔴 Cloud automation (Expandi, Dripify, Waalaxy, MeetAlfred, Octopus) | High | HeyReach precedent; ban risk |
| 🔴 "API" mode | REFUSE | No LinkedIn outreach API exists |

## What to Do If User Insists on Cloud Mode

1. Surface HeyReach Dec 2024 precedent explicitly
2. Require explicit risk acknowledgment (persisted as `interaction:research` with `#linkedin-cloud-risk-ack`)
3. Cap at 80/week regardless of tool's advertised capacity
4. Log the decision for audit trail
