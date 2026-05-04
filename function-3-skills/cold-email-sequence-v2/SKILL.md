---
name: cold-email-sequence
description: Write cold email sequences (5–7 touch, 14–21 day) using the CCQ copy framework, Pain-Trigger-Outcome openers, mobile-first formatting, and a hard ban on cliché openers. Gates every touch on the personalization-hook contract from `data-enrichment` (no verified hook → no send) and on `email_status` (no risky/catch-all/invalid sends). Use when a Tier-1/2 lead list is enriched and scored, when an ICP-grounded outbound burst is being planned, or when an existing sequence's reply rate is below the 3% floor and copy needs a structured rewrite.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, cold-email, sequence-design, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - email-infrastructure-setup
  - multi-channel-cadence
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - email-infrastructure-readiness-flag
  - sender-pool-and-domain-warmup-state
  - run-purpose-tag
deliverables:
  - 5-to-7-touch-email-sequence-with-copy
  - per-touch-content-with-provenance
  - touch-records-conforming-to-conventions-2-1
  - cadence-config-handoff-to-multi-channel-cadence
  - cliche-and-buzzword-audit-log
  - sequence-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cold Email Sequence

Produce a 5–7 touch cold email sequence (14–21 day arc) that ships through the function-3 channel adapter contract. Each Touch uses a named copy framework (CCQ default), is grounded in the recipient's verified personalization hook, formatted mobile-first, and audited for clichés before send. Hard rule: a Touch with `[unverified — needs check]` hook provenance is BLOCKED and routed to review queue.

> *Worked example uses WorkflowDoc (fictional, function-1 carry-over) as the seller; procedure is vertical-agnostic. Shared rules in `function-3-skills/function-3-conventions.md`.*

## Purpose

Cold email is the cheapest scalable outbound channel and the spine of any function-3 cadence. This skill translates ICP P-T-O + positioning into a 5–7 touch sequence, generates per-touch copy grounded in `data-enrichment`'s verified hooks, and audits each draft against cliché + buzzword + word-count rules before scheduling. Goal: a sequence that ships ≥3% reply rate (the floor below which copy is broken) without burning sender reputation.

## When to Use

- "Write a cold email sequence for our Tier-1 outbound list."
- "Reply rate is 1.5% — diagnose and rewrite the copy."
- "I have 80 enriched leads and need a 5-touch sequence ready for Smartlead."
- "Generate variants for A/B testing the opener."
- "Sending from Gmail directly — give me drafts and a per-touch runbook."
- Pre-launch copy generation when leads are enriched + scored.
- Sequence rewrite after `campaign-management` flags reply-rate floor breach.

## Inputs Required

1. **Scored + enriched Lead list** from `lead-scoring` (with `data-enrichment` upstream). Each Lead must carry `personalization_hook`, `email_status`, `signals`, `score`, `tier`.
2. **ICP Pain-Trigger-Outcome chain** from `icp-definition`.
3. **Positioning message house** from `positioning-strategy`.
4. **Email infrastructure readiness flag** from `email-infrastructure-setup` (warmup ≥70, age ≥14d, SPF/DKIM/DMARC aligned). Gates send.
5. **Sender pool + per-mailbox warmup state**.
6. **Run purpose tag** for cost attribution + replay.
7. (Optional) Sequence length override (3–9), framework override, A/B variant request.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | API (Smartlead/Instantly/Lemlist) / Manual (paste-ready) / BYO (Gmail/Outlook native) |
| **Default sequence** | 5–7 touches over 14–21 days; day_offsets 0/3/7/11/15/19/45 |
| **Default framework** | CCQ — house framework (Context-verified hook / Compliment-or-Connection / Question — one CTA), inspired by Instantly 2026 / Boomerang practitioner data; not industry-canonical |
| **Word targets** | Subject ≤8 words; opener body 50–80; later touches 40–100 |
| **Subject-line tier** | Subject ≤8 words is the cap; 1–5 words is Lavender's documented sweet spot, 6–8 acceptable, anything >8 = bin |
| **Per-touch frameworks** | T1 CCQ+Pain; T2 CCQ+Vision; T3 RTA (Resource-Then-Ask); T4 Compelling-Event; T5 Outcome-proof; T6 Break-up; T7 Resurrection (D+45) |
| **Hard hook rule** | `personalization_hook [verified: <url>]` OR Touch BLOCKED from sending |
| **Hard email_status rule** | Drop `risky` / `role-based` / `catch-all-domain` / `invalid` |
| **Cliché blocklist** | "I hope this finds you well" / "I noticed" / "we help X do Y" / multi-question CTAs |
| **Buzzword blocklist** | flexibility, visibility, scalable, strategic, leverage, synergy, robust, holistic |
| **Mobile format** | ≤2-line opener / one CTA / ≤4-line paragraphs / ≤3-line signature |
| **Quiet hours** | Default 8pm–8am recipient local + weekday-only; configurable per ICP — Belkins 2025 found 8–11pm peak (6.52% reply) for some segments. Override only with engagement data. |
| **Per-domain cap** | 30/day (50 absolute ceiling) |
| **Primary metric** | Reply rate per Instantly Benchmark 2026: ≥3% floor (broken/needs fix); 5–10% solid; 10%+ excellent; 15%+ best-in-class on tight segments. Open rate = noise (Apple MPP). |

## Procedure

### 1. Validate prerequisites + determine mode
Read scored Leads, ICP P-T-O, message house, infrastructure readiness flag. API key → API mode; seat → manual; native → BYO. Block if any gate fails.

### 2. Filter recipient list
Drop bad `email_status`; drop unverified hooks (route to review queue); apply tier filter; split GDPR jurisdiction (EU/UK get cadence variant with LIA + opt-out).

### 3. Pre-flight: capacity check
Compute `eligible × sequence_length` vs `per-domain cap × pool × duration`. Surface; wait for authorization if over capacity.

### 4. Generate per-touch copy + audit
Per recipient × position: pick framework per touch default; draw verified hook; compose subject (≤8 words) + body (within target); inject List-Unsubscribe header (RFC 8058) + physical address (CAN-SPAM US) or LIA + opt-out (GDPR EU/UK). Each draft passes cliché + word-count + mobile-format + buzzword audit; failures regenerate; second-fail surfaces for user review.

### 5. Compose Touch records + build cadence
Per conventions §2.1 / §2.2: full provenance on `content` / `compliance` / `provenance.copy`; `scheduled_for` (quiet-hours + weekday); 5–7 touches at default day_offsets.

### 6. Schedule + push to CRM + run summary
API → create sequence in tool; manual → paste-ready config + copy; BYO → per-touch runbook. Per conventions §11: scheduled Touches as `interaction:research` (sent record pushed by `track()` post-send). One-screen summary: eligible count, dropped counts, capacity headroom, audit flags, recommended next skill.

## Output Format

- Per-recipient, per-touch copy (subject + body + framework + word-count + provenance)
- Touch records conforming to conventions §2.1 (full compliance metadata)
- Cadence config conforming to conventions §2.2 (positions, day_offsets, exit conditions)
- Run record: filter results, capacity headroom, audit log, sender-pool load, recommended next skill
- Review queue: blocked Touches (unverified hook / blocked infrastructure) as `interaction:research`
- (BYO mode) per-touch runbook with native-send instructions + manual status-mark workflow

## Done Criteria

1. Mode determined (api / manual / byo); sending platform identified.
2. Prerequisites validated: scoring exists, P-T-O loaded, message house loaded, infrastructure ready.
3. Recipient filter applied: bad `email_status` dropped, unverified hooks routed to review, tier filter, GDPR split.
4. Capacity check passed (or user authorized over-cap); per-domain cap respected.
5. Per-touch copy generated with framework attribution and provenance.
6. Cliché + word-count + mobile-format + buzzword audit run; failures regenerated or surfaced.
7. Touch records assembled per conventions §2.1 with full compliance metadata.
8. Cadence built per conventions §2.2; scheduled or handed off; push to CRM emitted; run summary one-screen.

## Pitfalls

- **Optimizing on open rate.** Apple MPP made it noise. Reply rate is primary; open rate is reported, never tuned.
- **Generic openers.** "I noticed your company..." with no specific verified detail = fabrication risk + low reply rate.
- **Long emails.** >125 words drops reply rate sharply; 50–80 is sweet spot for openers.
- **Multiple CTAs.** Two questions in close = no answer.
- **Buzzword stuffing.** "Scalable, strategic, robust" — each costs reply rate.
- **Cliché openers.** "I hope this finds you well" / "I noticed" pre-trigger the recipient's spam filter.
- **Skipping the break-up.** Touch 6 break-up generates real replies; ending at touch 5 leaves conversion on the table.
- **Ignoring quiet hours / weekends.** Sat 11pm = spam-flagged.
- **Sending without warmup.** First-day cold-blast from new domain = instant blacklist.
- **Sending to risky/catch-all/role-based.** Bounce rate explodes; sender reputation tanks; the skill blocks these by contract.
- **Fabricating personalization (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (recipients, companies, signal references, dates, customer outcomes, dollar figures, evidence URLs) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. The personalization-hook contract is enforced at copy-gen time: a Touch with `[unverified]` hook is BLOCKED from sending. Never invent customer outcomes, fake quotes, or "saw your post" with no URL.
- **Misalignment with positioning.** Body language drifts from message house — surface in audit; recompose against positioning artifact.

## Verification

The sequence is real when: every Touch's `provenance.copy` resolves to a hook URL or carries `[user-provided]` for outcome claims; reply rate ≥3% by D+10 (below this = copy or targeting broken); bounce rate <2% (warn) / <5% (pause); complaint rate <0.1% (target) / <0.3% (pause); zero touches sent during quiet hours / weekends; zero touches with cliché-blocklist phrases. Negative test: pick 5 Touches; read subject + opener aloud — if any sound generic ("I noticed you're a leader in..."), copy-gen is broken.

## Example

**User prompt:** "Write a 5-touch cold email sequence for our 80 Tier-1 enriched leads. Smartlead configured. Pitching WorkflowDoc `[hypothetical]` to Heads of Support at Series B SaaS."
**What should happen:** Read prerequisites (lead-scoring + icp-definition + positioning-strategy + email-infrastructure-setup all green). Mode = API. Filter 80 → 63 eligible (drop 6 bad email_status, route 11 unverified-hook to review). Capacity: 315 touches × 5 / 90/day max / 19d duration = 41% headroom. Generate per-touch copy: T1 CCQ+Pain, T2 CCQ+Vision, T3 RTA, T4 compelling-event, T5 outcome-proof. Audit: 0 cliché flags, 0 buzzword flags. Schedule via Smartlead API. Push 315 scheduled Touch interactions + 1 run record + 11 review-queue. Recommend `campaign-management` (target ≥3% reply by D+10).

**User prompt:** "Reply rate is 1.5% on our existing 5-touch sequence — diagnose and rewrite."
**What should happen:** Audit existing copy first. Surface specific violations: 4 cliché phrases ("I hope this finds you well", "I noticed", "circle back"), 6 buzzwords (scalable, strategic, leverage), 3 multi-CTA touches, 1 touch >125 words. Propose targeted rewrites where structure is OK, full regenerate where structure broken. Most-likely root cause: hook quality (re-run `data-enrichment` with `linkedin_recent_posts` for higher hook coverage), then sequence framework rotation (Pain → Vision → RTA varies the angle).

**User prompt:** "I'm a founder sending 12 emails from Gmail. Give me drafts."
**What should happen:** BYO mode. 12 leads × 5 touches = 60 drafts. Each presented as Gmail-paste block: subject + body + day_offset send instruction. Per-touch runbook with checkbox for "sent" / "replied" / "bounced" — manual status-mark workflow because no API. Recommend `email-infrastructure-setup` to confirm SPF/DKIM/DMARC even on native Gmail (founder domains often lack DMARC).

## Linked Skills

- Sequence built, monitor → `campaign-management`; multi-channel → `multi-channel-cadence`
- Email infrastructure not ready → `email-infrastructure-setup`
- Replies arriving → `reply-classification` (planned); objections → `objection-handling-library` (planned)
- Hook coverage <70% → `data-enrichment`; list unscored → `lead-scoring`
- Reply rate <3% by D+10 → rewrite mode OR `lead-scoring` (re-tier)

## Push to CRM

After scheduling, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each scheduled Touch (draft state) | `interaction` (type: `research`) | `relevance` = "Touch <position> scheduled for <ISO> via <channel> with hook <url>"; `tags: "#scheduled #cold-email #touch-<position> #function-3"` |
| Each Touch after send | `interaction` (type: `outreach`) | `relevance` = subject + body excerpt + provenance; `tags: "#sent #cold-email #function-3"` |
| Cadence + campaign run record | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#cold-email-sequence-run #function-3"` |
| Last-touched timestamp on recipient | `person` (PATCH via dedup key) | `last_touched_at`, `last_touched_channel: email`, tags updated |
| `[unverified — needs check]` (hook missing) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #cold-email-sequence #blocked-no-hook"`; never `outreach` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
SMARTLEAD_API_KEY=     # or INSTANTLY_API_KEY / LEMLIST_API_KEY
SENDS_PER_DOMAIN_PER_DAY_CAP=30
WARMED_UP_DAYS_THRESHOLD=14
WARMUP_SCORE_THRESHOLD=70
```

### Source tag

`source: "skill:cold-email-sequence:v2.0.0"`

### Example push (sent Touch)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox [hypothetical]",
    "contactName": "Esme Liang [hypothetical]",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#sent #cold-email #touch-1 #ccq-pain #function-3",
    "relevance": "Cold email sent 2026-05-05T10:00 PT [hypothetical]. Subject: \"New VP CX seat — first 90 days?\". Framework: CCQ + Pain. Hook: Stitchbox [hypothetical] VP CX hire 2026-04-19 [hypothetical] [verified: news.example.com/stitchbox-vp-cx-2026]. Word count: 74. Sender: will@workflowdoc-mail.com [hypothetical] (reputation 92 [hypothetical]). Cadence: cad_workflowdoc_t1_5touch_19d_v1.",
    "source": "skill:cold-email-sequence:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#cold-email-sequence-run #function-3",
    "relevance": "Cold email sequence run cmp_2026-05-04_q9k. Mode: API (Smartlead). Cadence: ccq-tier1-5touch-19d. Filter: 80 input → 63 eligible (6 bad email, 11 unverified hook to review). Capacity: 315 touches over 19d / 90/day max / 41% headroom. Audit: 0 cliché / 0 buzzword / 0 word-count flags. Recommended next: campaign-management (target reply rate ≥3% by D+10).",
    "source": "skill:cold-email-sequence:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Touch sends and pushes as `interaction:outreach` per standard mapping. |
| `[unverified — needs check]` | Touch is BLOCKED from sending. Pushes ONLY as `interaction:research` with `#unverified #review-required #needs-hook` tags. Never as `outreach`. |
| `[hypothetical]` | Never sends; never pushes. Local artifact only. |

Example blocked push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #cold-email-sequence #blocked-no-hook",
    "relevance": "Touch BLOCKED for Mira Chen [hypothetical] [unverified — needs check] — personalization_hook absent (data-enrichment ran but found no citable source in last 90d). Recommend re-enrichment with linkedin_recent_posts permission OR manual hook capture, then re-run cold-email-sequence.",
    "source": "skill:cold-email-sequence:v2.0.0"
  }'
```

### When NOT to push

- Drafts never scheduled — local artifact only; do not push.
- Touches blocked at pre-flight (infrastructure, capacity, DNC, hook) — push ONLY as `interaction:research` with the block reason; never as `outreach`.
- `[unverified — needs check]` — see provenance routing.
- `[hypothetical]` — never.
- Recipient unsubscribed before scheduled send — drop the remaining cadence Touches; push the unsubscribe-honor record only.
