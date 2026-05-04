---
name: linkedin-outreach
description: Execute LinkedIn outreach via Sales Navigator + session-based tools (HeyReach, Dripify, MeetAlfred) — connection requests with ≤300 char notes, follow-up messages to existing connections, InMails for high-value targets — with strict LinkedIn ToS compliance (no direct scraping), weekly rate limits, and the personalization-hook contract from `data-enrichment` enforced. Use when email is the wrong channel (risky/catch-all email status, or email-fatigued segments), when LinkedIn URL is the strongest identity signal in the Lead schema, when the play is relationship-first social-selling, or when multi-channel cadence requires a LinkedIn leg.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, linkedin, social-selling, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - lead-sourcing-linkedin
  - cold-email-sequence
  - multi-channel-cadence
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list-with-linkedin-urls
  - icp-pain-trigger-outcome-chain
  - user-linkedin-account-or-session-tool
  - run-purpose-tag
  - cadence-position-context
deliverables:
  - connection-request-notes-≤300-chars
  - follow-up-message-templates-to-connections
  - inmail-templates-for-high-value-targets
  - touch-records-conforming-to-conventions-2-1
  - per-touch-content-with-provenance
  - linkedin-cadence-config-handoff
  - account-safety-state-report
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# LinkedIn Outreach

Execute LinkedIn-channel touches — connection requests, messages to existing connections, occasional InMails — through manual Sales Nav UI or session-based desktop tooling. **There is no LinkedIn outreach API.** Hard-codes ToS compliance (no direct scraping, no cloud-proxy automation by default), respects weekly rate limits, gates every touch on the personalization-hook contract from `data-enrichment`, and surfaces ban-risk explicitly when users insist on cloud automation.

> *Worked example uses WorkflowDoc [hypothetical] (fictional, function-1 carry-over) as the seller; procedure is vertical-agnostic. Shared rules in `function-3-skills/function-3-conventions.md`.*

## Purpose

LinkedIn is the second-most-common outbound channel after email and the *first* choice when emails bounce. This skill translates a Lead's LinkedIn URL + verified hook into a connection-request note (≤300 chars) or message; picks the play (connect-with-note / cold InMail / message-to-connection / content-engagement); routes execution through ToS-respecting modes — **manual native is the default**. The skill does NOT recommend cloud-proxy tools; it documents what the user has configured and surfaces risk. Goal: sustainable LI outreach that protects the user's account (every connection = years of network) while converting at the 12–25% acceptance band good copy + good targeting produces.

## When to Use

- "Send LinkedIn outreach to our 60 Tier-1 prospects with verified LI URLs."
- "Email is the wrong channel — these are catch-all-domain emails."
- "Add a LinkedIn touch to our existing cadence."
- "Sales Nav configured — set up a connection-request batch."
- "Running social-selling — relationship-first sequence."; pre-launch with high LI URL coverage; email-fatigued segments (<2% reply).

## Inputs Required

1. **Scored + enriched Lead list with LinkedIn URLs** from `lead-scoring` (with `data-enrichment` upstream). Each Lead needs `linkedin_url [verified]` + `personalization_hook` + score + tier.
2. **ICP P-T-O chain** from `icp-definition`; **positioning message house** from `positioning-strategy`.
3. **LinkedIn account state** — Sales Nav seat (preferred) or native LI; account age, SSI, recent-activity. Optionally a configured tool: real-browser/desktop (Northlight, Linked Helper desktop, Dux-Soup, PhantomBuster browser-mode) or — high-risk — cloud (Expandi, Dripify, Waalaxy, MeetAlfred, Octopus).
4. **Cadence position context** (multi-channel runs) from `multi-channel-cadence`; **run purpose tag**.
5. (Optional) Connection-status flag, LI account safety state.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes (risk-tiered)** | ✅ Manual / native (PRIMARY); ⚠️ Real-browser / desktop session (CDP — Northlight, Linked Helper desktop, Dux-Soup, PhantomBuster browser-mode); 🔴 Cloud automation (Expandi/Dripify/Waalaxy/MeetAlfred/Octopus/PhantomBuster cloud — high ban risk); 🔴 "API" mode = does NOT exist |
| **HeyReach precedent (Dec 2024)** | LI deleted HeyReach company page (16.4k followers); founder/CTO/CRO/CMO banned; Feb 2025 C&D + API revoked; retroactive flagging (Northlight: 40% restricted Q1 2026). Same wave: Apollo + Seamless.ai (Mar 2024). |
| **No outreach API** | SNAP is gated to CRM vendors; **paused new partners Aug 2025**. Messaging API prohibits cold automation. "API" in any tool = unofficial reverse-engineered access = ban risk. |
| **Legal landscape** | Public scraping ≠ CFAA violation (hiQ, 9th Cir. Apr 2022) BUT IS a User Agreement breach (hiQ Nov 2022 settlement + permanent injunction). Bright Data v. Meta (Jan 2024): logged-in scraping = enforceable ToS violation. Fake accounts for logged-in data = wire-fraud-adjacent. LI can ban + sue. Direct scraping: REFUSED. |
| **Connection note** | ≤300 chars, NO URL, NO emoji, single CTA. Frameworks: warm-intro / event-based / content-engagement. Generic-no-context refused. |
| **Connection requests / week** | ≤80/week default (under LI's ~100 ceiling); ≤150/week ONLY if account is verified high-SSI. Rolling 7-day reset (NOT calendar week). |
| **Daily distribution** | 15–25/day max; never bulk-burst. |
| **Personalized notes (free accounts)** | 5/month — NEW restriction since 2023. |
| **Other limits** | Profile views: 150/day free, 2,000/day Sales Nav. InMail: 25/day Premium, 1,000/week Recruiter (Tier-1 only). Group/event msg: 10/week to non-connections. Total connections: 30,000 (hard cap). |
| **Account state pre-check** | Age + SSI + recent-activity before ANY automation. Activity warmup required if dormant — sudden activity = instant red flag. |
| **Account safety** | Green only; amber/red = 7-day cool-down. |
| **Acceptance rate target** | 15–25% healthy; <12% = copy/targeting broken. |
| **Optimal send time** | Weekday 9am–5pm recipient local; Tue–Thu best. |
| **Hook gate** | Event-based + content-engagement need citable URL; missing → review queue. |
| **GDPR (EU/UK)** | `gdpr_basis: legitimate-interest` + opt-out language in follow-up. |
| **Compliance** | Per conventions §9.5 — no direct scraping, no buying connections, weekly limits respected. |

## Procedure

### 1. Validate prerequisites
Read scored Leads with verified LinkedIn URLs; load ICP P-T-O + message house; check LI account state (age, SSI, dormancy, recent activity). Block on gate failures. If dormant, surface activity-warmup before automation.

### 2. Determine mode (risk-tiered)
✅ Manual / native (Sales Nav UI or native LI) → PRIMARY. ⚠️ Real-browser / desktop session (CDP — Northlight, Linked Helper desktop, Dux-Soup, PhantomBuster browser-mode) → acceptable with caveats; runs from user's browser/IP. 🔴 Cloud automation (Expandi/Dripify/Waalaxy/MeetAlfred/Octopus/PhantomBuster cloud) → NOT recommended; surface HeyReach Dec 2024 precedent + require explicit risk-ack. 🔴 "API" mode → REFUSE (no LinkedIn outreach API exists). Direct-scraping → REFUSE.

### 3. Filter recipient list
Drop no-LI-URL; drop EU/UK without LIA; apply tier filter; dedup against active email cadences.

### 4. Pre-flight: capacity check
Weekly: `LINKEDIN_CONNECTS_PER_WEEK_CAP` (80 default; 150 high-SSI override) / `LINKEDIN_MESSAGES_PER_WEEK_CAP` (200) / `LINKEDIN_INMAIL_PER_MONTH_CAP` (50). Enforce 5/month notes (free accounts). Distribute 15–25/day. Recommend tier-segmenting or extending duration if over.

### 5. Pick framework + generate copy
Warm-intro / Event-based (citable URL) / Content-engagement (prior interaction). Generic-no-context refused → review queue. Connection note ≤300 chars, no URL, single CTA. Follow-up 2–3 sentences post-accept. InMail 4–6 sentences (Tier-1 only). Audit: char-count + cliché + no-URL + hook citation.

### 6. Compose Touch records
Per conventions §2.1: channel `linkedin-connect/message/inmail`, full provenance, scheduled_for (weekday 9am–5pm recipient local), GDPR compliance for EU/UK.

### 7. Schedule via tool or hand off
Manual / native: paste-ready notes + per-touch schedule + per-recipient runbook + manual status-mark. Desktop session: campaign created at safe pace (4–5/day distributed). Cloud (if authorized): scheduled with explicit risk-ack record persisted.

### 8. Push to CRM + run summary
Per conventions §11. Run summary: eligible/dropped counts, framework distribution, capacity headroom, account safety, mode + risk-ack status, recommended next skill.

## Output Format

- Per-recipient connection note (≤300 chars) / follow-up / InMail with framework attribution
- Touch records per conventions §2.1 with full provenance + compliance metadata
- LinkedIn cadence config (positions, day_offsets, exit conditions matching weekly caps)
- Run record: filter results, capacity headroom, framework distribution, account safety, mode + risk-ack, recommended next skill
- Review queue: weak-hook records as `interaction:research`; (Manual / native) per-recipient runbook + manual status-mark; (Cloud only) explicit risk-acknowledgment record citing HeyReach Dec 2024 precedent

## Done Criteria

1. Mode determined; "API" mode + direct-scraping refused; cloud-mode requires explicit user risk-ack; account safety green (amber/red blocks); account state pre-check passed (age + SSI + dormancy); activity warmup applied if needed.
2. Recipient filter applied: no-LI-URL / EU-no-LIA / tier / dedup against active email cadence.
3. Capacity check passed: 80/week (or 150/week high-SSI), 5/month notes for free, 15–25/day, rolling 7-day reset respected.
4. Per-recipient framework picked; generic-no-context refused.
5. Per-touch copy generated with char-count + cliché + no-URL + hook-citation audit.
6. Touch records assembled per conventions §2.1; cadence built; scheduled or handed off; push to CRM emitted; run summary one-screen.

## Pitfalls

- **Cloud automation tools can disappear overnight, taking accounts with them.** HeyReach Dec 2024: page deleted (16.4k followers), founder/CTO/CRO/CMO banned, Feb 2025 C&D + API revoked, retroactive flagging (Northlight: 40% restricted Q1 2026). Same wave hit Apollo + Seamless.ai (Mar 2024). If user insists on cloud, surface and require acknowledgment.
- **There is no LinkedIn outreach API.** SNAP gated to CRM vendors + paused new partners Aug 2025; Messaging API prohibits cold automation. Any "API mode" claim = unofficial reverse-engineered access = ban risk. Skill REFUSES "API" mode.
- **LinkedIn ToS prohibits all outreach automation; account ban = loss of every connection ever made** (often years of network). The skill documents what users have configured and surfaces risk — it does not recommend tools. Treat the account like production infrastructure.
- **Legal exposure even when scraping is "legal".** Public scraping ≠ CFAA violation (hiQ 9th Cir. Apr 2022) but IS a User Agreement breach (hiQ Nov 2022 settlement). Bright Data v. Meta (Jan 2024): logged-in scraping = enforceable ToS violation. Fake accounts for logged-in data = wire-fraud-adjacent. LI can ban + sue. Direct scraping: REFUSE.
- **Skipping account state pre-check.** Sudden activity on a dormant account = instant red flag. Warm up activity (logins, engagement) before any automation.
- **Bulk-bursting weekly cap on Day 1.** Rolling 7-day reset (NOT calendar week) — a Monday burst counts against the next 7 days. Distribute 15–25/day.
- **Forgetting the 5/month personalized-note cap on free accounts** (new since 2023; exhausting it kills mid-campaign personalization).
- **Generic connection notes / URLs in notes / connect-and-pitch combos.** Auto-rejected, flagged, or read as bait. Single-account 100+/week = account flag.
- **Skipping the post-accept follow-up / treating LI like email / InMailing everyone.** Connection is the door; the message is the conversation — less direct, more conversational. Inventing engagement context ("loved your recent post" with no URL) = anti-fab violation. Reserve InMail for Tier-1; ignoring SSI / profile health lowers acceptance.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity carries `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Hook URLs gated for event-based + content-engagement; absence routes to review queue.

## Verification

Run is real when: 0 notes >300 chars or with URLs; every event-based / content-engagement Touch has citable hook URL; 0 sends on "API" mode; cloud-mode runs have explicit user risk-ack persisted; rolling 7-day cap respected; daily distribution 15–25; 5/month note cap honored on free accounts; acceptance ≥12% by D+7; 0 sends during quiet hours / weekends; account safety stays green. Canonical "safe" path: Sales Nav subscription + manual personalized requests + `cold-email-sequence` for scale + `multi-channel-cadence` for orchestration.

## Example

**User prompt:** "Send LI connection requests to 40 Tier-1 leads with verified LI URLs. WorkflowDoc [hypothetical] to VPs of Customer Experience. Sales Nav configured — manual mode."
**What should happen:** 40 → 32 eligible (3 EU/UK no-LIA dropped, 5 in active email cadence). Account state: SSI 72, 18-month age, active last 30 days → green. Weekly headroom 80 (Sales Nav default). Framework: 0 warm-intro / 22 event-based / 4 content-engagement / 6 review (weak hooks). 32 connection requests laid out in a paste-ready runbook at ~5/day, weekday 11am recipient local, Tue–Thu preferred. Recommend `campaign-management` (target acceptance ≥15% by D+7).

**User prompt:** "Just scrape LinkedIn for VPs of Eng at FAANG and send connection requests via the API."
**What should happen:** REFUSE on two counts. (1) No LinkedIn outreach API exists — explain SNAP is paused to new partners since Aug 2025 and prohibits cold automation. (2) Direct scraping is a ToS violation (hiQ Nov 2022; Bright Data v. Meta Jan 2024). Recommend Sales Nav search via `lead-sourcing-linkedin` for sourcing + manual or real-browser session execution. Log refusal as `interaction:research` for audit. No Touches produced.

**User prompt:** "Use HeyReach to send 200 connection requests this week."
**What should happen:** Surface HeyReach Dec 2024 ban precedent (page deleted, founder/CTO/CRO/CMO banned, retroactive account flagging — Northlight Q1 2026 reports 40% restricted). Decline default; offer Sales Nav manual at 80/week (or 150/week if SSI ≥75). If user insists on a cloud tool despite risk, require explicit acknowledgment, persist a risk-ack `interaction:research` record, and cap at 80/week regardless.

## Linked Skills

- Sequence built, monitor → `campaign-management`; multi-channel → `multi-channel-cadence`
- LI URLs missing → `data-enrichment` or `lead-sourcing-linkedin`; list unscored → `lead-scoring`
- Replies arriving → `reply-classification` (planned); account amber → cool-down mode here; email-better target → `cold-email-sequence`

## Push to CRM

After scheduling, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Scheduled connection request (draft) | `interaction:research` | `relevance` = "Scheduled <ISO> with note <preview>"; `tags: "#scheduled #linkedin-connect #function-3"` |
| Touch after send | `interaction:outreach` | `relevance` = note + framework + hook URL + provenance; `tags: "#sent #linkedin-<connect|message|inmail> #function-3"` |
| Cadence + campaign run record | `interaction:research` | `relevance` = run summary + framework distribution + mode + risk-ack status; `tags: "#linkedin-outreach-run #function-3"` |
| Mode-risk acknowledgment (cloud-mode only) | `interaction:research` | `relevance` = HeyReach-precedent ack + tool + user auth; `tags: "#linkedin-cloud-risk-ack #function-3"` |
| Last-touched timestamp | `person` PATCH | `last_touched_at`, `last_touched_channel: linkedin-<type>` |
| `[unverified — needs check]` (weak hook) | `interaction:research` ONLY | `tags: "#unverified #review-required #linkedin-outreach #weak-hook"`; never `outreach` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
LINKEDIN_CONNECTS_PER_WEEK_CAP=80
LINKEDIN_CONNECTS_PER_WEEK_HIGH_SSI_CAP=150
LINKEDIN_FREE_NOTES_PER_MONTH_CAP=5
LINKEDIN_DAILY_DISTRIBUTION_MAX=25
LINKEDIN_MESSAGES_PER_WEEK_CAP=200
LINKEDIN_INMAIL_PER_MONTH_CAP=50
```

> **Tool API keys** (e.g. for desktop / cloud session tools the user has explicitly configured) are read at runtime if present. The skill does NOT recommend cloud tools; pricing for any outreach tool changes — agent reads vendor docs at runtime; verify live before any spend.

### Source tag

`source: "skill:linkedin-outreach:v2.0.0"`

### Example push (sent connection request)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Helio [hypothetical]",
    "contactName": "Nina Park [hypothetical]",
    "contactLinkedIn": "https://linkedin.com/in/nina-park-cx",
    "tags": "#sent #linkedin-connect #event-based #function-3",
    "relevance": "LinkedIn connection request sent 2026-05-22T11:00 PT. Mode: Sales Nav manual. Framework: event-based. Hook: Helio [hypothetical] VP CX hire 2026-04-08 [hypothetical]. Note (228 chars): \"Nina [hypothetical] — congrats on landing the VP CX role at Helio [hypothetical]. The first 90 days usually surface the same pattern at Series B support orgs: runbooks scattered across 8+ tools. Worth a quick chat? — Will [hypothetical]\". Sender: will-workflowdoc [hypothetical] (SSI 72). Cadence: cad_workflowdoc_li_3touch_14d_v1.",
    "source": "skill:linkedin-outreach:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#linkedin-outreach-run #function-3",
    "relevance": "LinkedIn outreach run cmp_li_2026-05-21_q9k. Mode: Sales Nav manual (PRIMARY). Cadence: linkedin-3touch-14d-v1. Filter: 40 → 32 eligible (3 EU/UK no-LIA, 5 in active email). Account safety: green; SSI 72; account age 18mo; 32/80 weekly cap (40%); daily distribution 5/day under 25 cap. Framework: 0 warm-intro / 22 event-based / 4 content-engagement / 6 review. Risk-ack: n/a (manual mode). Recommended next: campaign-management (target acceptance ≥15% by D+7).",
    "source": "skill:linkedin-outreach:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Touch sends and pushes as `interaction:outreach`. |
| `[unverified — needs check]` | Touch is BLOCKED. Pushes ONLY as `interaction:research` with `#unverified #review-required #linkedin-outreach` tags. |
| `[hypothetical]` | Never sends; never pushes. Local artifact only. |

Example blocked push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #linkedin-outreach #weak-hook",
    "relevance": "Touch BLOCKED for Mira Chen [unverified — needs check] — event-based framework requires citable hook URL; data-enrichment found no recent LI post or news. Recommend re-enrichment or switch to warm-intro framework if mutual connection exists.",
    "source": "skill:linkedin-outreach:v2.0.0"
  }'
```

### When NOT to push

- Drafts never scheduled / `[hypothetical]` worked-example output — local artifact only.
- Touches blocked at pre-flight (account safety, capacity, weak hook, dormant-no-warmup) — push as `interaction:research` with block reason.
- Direct-scraping refused / "API" mode refused — push refusal record for audit; no Touches.
- `[unverified — needs check]` — see provenance routing.
- Recipient withdrew connection request before send — drop remaining cadence Touches; push withdrawal record only.
