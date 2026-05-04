---
name: cold-calling
description: Generate cold-call scripts (9-second opener, discovery questions, gatekeeper-handler, ≤15-second voicemail) and orchestrate dial sessions via JustCall / Aircall / Orum / Dialpad with TCPA-compliant DNC scrubbing, quiet-hours enforcement, mobile-vs-landline routing, and call-disposition logging. Use when Tier-1 SAL-eligible prospects have verified `phone_status: mobile | landline` (NOT `dnc | invalid`), when email + LinkedIn channels have plateaued, when high-stakes accounts need live-voice contact, or when a multi-channel cadence requires a call leg.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, cold-calling, dialer, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - cold-email-sequence
  - linkedin-outreach
  - multi-channel-cadence
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list-with-phone-status
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - dialer-platform-or-manual-mode
  - dnc-scrub-result
  - run-purpose-tag
deliverables:
  - 9-second-opener-script
  - discovery-question-set
  - gatekeeper-handler-script
  - voicemail-drop-script-≤15-seconds
  - touch-records-conforming-to-conventions-2-1
  - dial-list-with-tcpa-clearance
  - call-disposition-log
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cold Calling

Produce TCPA-compliant cold-call scripts and orchestrate dial sessions for Tier-1 prospects whose phone numbers are verified and DNC-scrubbed. Outputs: 9-second opener, discovery question set, gatekeeper handler, ≤15-second voicemail drop, and per-recipient Touch records. Hard rules: no calls to `phone_status: dnc | invalid`; no calls before 8am or after 9pm recipient local (TCPA); SMS to mobile requires explicit prior consent.

> *Worked example uses WorkflowDoc (fictional, function-1 carry-over) as the seller; procedure is vertical-agnostic. Shared rules in `function-3-skills/function-3-conventions.md`.*

## Purpose

Cold calling is the most expensive channel per touch but converts at 3–5x email when the contact is verified, the prospect is Tier-1, and the script is human. It is also the most-regulated outbound channel — TCPA fines are per-violation. This skill generates the 9-second opener, discovery questions (Bosworth + Sandler Pain Funnel), gatekeeper handler, and ≤15-second voicemail drop; gates every dial on DNC scrubbing + quiet hours + verified phone status. Goal: a dial session that converts conversations into meetings without exposing the user to TCPA risk.

## When to Use

- "Add cold-calls to our Tier-1 cadence."
- "Email reply rate plateaued at 2% — let's call the high-fit prospects."
- "I need a 9-second opener and voicemail drop for our dial session today."
- "JustCall configured — set up a dial campaign for 50 prospects."
- "Founder-led calls — give me the discovery questions."
- Pre-launch with verified mobile / landline phones; post-no-show rescue.

## Inputs Required

1. **Scored + enriched Lead list** from `lead-scoring`. Must carry `phone`, `phone_status`, score, tier, signals.
2. **ICP P-T-O chain** from `icp-definition`.
3. **Positioning message house** from `positioning-strategy`.
4. **Dialer platform** — one of: `JUSTCALL_API_KEY`, `AIRCALL_API_KEY`, `ORUM_API_KEY`, `DIALPAD_API_KEY`, `CONNECTANDSELL_API_KEY`, or manual / native phone (BYO).
5. **DNC scrub result** from `DNC_COM_API_KEY` or `CONTACTCENTERCOMPLIANCE_API_KEY` — mandatory before US calling.
6. **Run purpose tag**.
7. (Optional) Sales rep identity.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | API (JustCall/Aircall/Orum/Dialpad) / Manual (paste-ready) / BYO (native phone) |
| **Hard gates** | DNC scrub mandatory; quiet hours 8am–9pm recipient local (TCPA); verified phone status |
| **Phone-status drops** | `dnc` (always); `invalid`; `unverified` (route to data-enrichment) |
| **9-second opener** | Greet → state cold-call honestly → 5s purpose → permission ask. ≤30 words. |
| **Discovery framework** | Bosworth pain → impact → buying-vision + Sandler Pain Funnel (4–6 questions) |
| **Gatekeeper response** | 3 patterns: specific-pain reply / honest cold-call / permission-ask. NEVER pretend. |
| **Voicemail drop** | ≤15 seconds spoken (≤45 words). Name + reason + callback x2. |
| **Cadence** | Default 3 attempts over 5 days; D+0 / D+2 / D+4 |
| **Caps** | 80 calls/rep/day (warn above 100); 40 voicemails/rep/day |
| **Connect rate target** | 8–12% healthy; <6% = bad targeting/list/timing |
| **Voicemail-to-callback** | 1–3% (compounding across multi-touch) |
| **Optimal time** | Mid-day 10am–noon, 2pm–4pm recipient local; Tue–Thu best |
| **Compliance** | TCPA hours, DNC scrub ≤30 days old, B2B-cellphone treated as restricted by default |

## Procedure

### 1. Validate prerequisites + determine mode
Read scored Leads with phone_status; load ICP P-T-O + message house; verify DNC scrub for US recipients. Dialer API key → API mode; else seat → manual; else BYO → runbook. Block on gate failures.

### 2. Filter recipient list
Drop `phone_status: dnc | invalid | unverified`; apply tier filter (default Tier-1 SAL); drop unknown-timezone records; drop called-within-90d records.

### 3. Pre-flight: capacity check
Compute total dials vs `CALLS_PER_REP_PER_DAY_CAP × rep_count × duration`. Surface; recommend multi-rep / extended duration if over.

### 4. Generate scripts
Per recipient: 9s opener (≤30 words; pattern-interrupt + name + purpose + permission); 4–6 discovery questions (Bosworth + Sandler); gatekeeper handler (3 patterns, never lie); voicemail (≤15s / ≤45 words). Audit: word-count + cliché blocklist + no-pretend rule + hook citation.

### 5. Compose Touch records + schedule
Per conventions §2.1: channel `call`/`voicemail`; full provenance; scheduled_for (TCPA 8am–9pm recipient local); compliance metadata. API: campaign created in dialer; manual: dial list + script library; BYO: per-recipient runbook.

### 6. Capture call disposition
Per dial: `connected-positive` / `connected-not-now` / `connected-not-interested` / `voicemail-left` / `no-answer` / `wrong-person` / `bad-number`. Route per disposition (positive → discovery-call-prep; not-interested → objection-handling-library; bad-number → data-enrichment).

### 7. Push to CRM + run summary
Per dial: `interaction:outreach` with disposition. Run record: dial volume, connect rate, conversation rate, meeting-booked rate, recommended next skill.

## Output Format

- Per-recipient 4-script bundle: opener (≤30 words) + discovery questions (4–6) + gatekeeper handler (3 patterns) + voicemail drop (≤45 words)
- Touch records per conventions §2.1 with full TCPA + DNC compliance metadata
- Dial list with TCPA-clearance flags
- Cadence config (3-attempt default over 5 days; respecting recipient local TCPA hours)
- Run record: filter results, capacity headroom, audit log, recommended next skill
- Per-dial disposition log
- Review queue: blocked records (DNC, invalid, unverified) as `interaction:research`

## Done Criteria

1. Mode determined; dialer or runbook prepared.
2. DNC scrub completed for all US recipients within 30 days; recorded.
3. Recipient filter applied: DNC dropped, invalid/unverified phones dropped, tier filter, called-within-90d filter.
4. Capacity check passed.
5. Per-recipient scripts generated with framework attribution and audit-pass.
6. Hook citation enforced (or downgrade to honest cold-call pattern).
7. Touch records assembled per conventions §2.1 with TCPA hours respected, jurisdiction tagged.
8. Scheduled (API) or handed off (manual / BYO); push to CRM emitted; run summary one-screen.

## Pitfalls

- **Calling DNC numbers.** TCPA fines $500–$1500 per violation. Hard rule.
- **Calling outside 8am–9pm recipient local.** Same.
- **SMS to mobile without prior consent.** Same.
- **Buzzword opener.** "I'm calling to discuss strategic value" → instant hangup.
- **Pretending prior conversation.** "Following up on our chat" when there was none — dishonest, illegal in some jurisdictions, erodes trust.
- **No permission ask.** "Hi Marcus `[hypothetical]`, I'm calling about WorkflowDoc `[hypothetical]`..." launches into pitch.
- **Voicemail >15 seconds.** Long voicemails get deleted.
- **Skipping discovery to pitch.** "We do X for Y, can we book a demo?" fails.
- **Calling the same recipient daily.** 1–2 attempts/week max.
- **Treating voicemail-only as zero-value.** Voicemails compound; multi-touch shows persistence.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (recipients, companies, hook references, dates, customer outcomes) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Hook URLs gate the opener and voicemail; absence forces honest cold-call pattern with no specific reference. Phone numbers MUST be `[verified]` from data-enrichment; agent-inferred phones BLOCKED.
- **Calling a number with `[unverified]` provenance.** Phone-status verification mandatory.

## Verification

The run is real when: 100% of dials have DNC scrub ≤30 days old; 100% within TCPA 8am–9pm recipient local hours; every Touch's `provenance.copy` resolves to hook URL OR is honest cold-call pattern; connect rate ≥6% (below = broken); zero "pretend prior conversation" violations; voicemail word count ≤45.

## Example

**User prompt:** "Set up cold-call session for 50 Tier-1 SAL-eligible prospects. WorkflowDoc `[hypothetical]` to Heads of Support at Series B SaaS. JustCall configured. DNC.com scrub completed."
**What should happen:** Validate scrub timestamp ≤30d. Filter 50 → 43 eligible `[hypothetical]` (2 DNC caught, 1 invalid, 4 called within 90d). Capacity check: 129 dials `[hypothetical]` over 5d × 400/day max = 6% utilization `[hypothetical]`. Generate 4-script bundles per recipient (9s opener + 4–6 discovery questions + gatekeeper handler + voicemail). Audit: 0 cliché / 0 pretend / 0 hook-citation failures. Schedule via JustCall: 3-dial cadence (D+0/D+2/D+4) at recipient local 10:30am or 2:30pm. Recommend `campaign-management` (target connect rate ≥8%).

**User prompt:** "I'm a founder, dialing 12 named accounts personally."
**What should happen:** BYO mode. Per-recipient runbook with script + recipient context card (hook + signals + tier). Founder dials at human pace. After each call, manual disposition log. Recommend `discovery-call-prep` when meetings book.

**User prompt:** "DNC scrub was 45 days ago — proceed?"
**What should happen:** BLOCK. Require fresh scrub (≤30d). Reason: TCPA hard requirement; some states require shorter scrub windows. Run resumes after refresh.

## Linked Skills

- Dial campaign running → `campaign-management`; multi-channel cadence → `multi-channel-cadence`
- Phone coverage <50% → `data-enrichment` (Hunter/Lusha phone discovery)
- Meeting booked → `discovery-call-prep` (planned); reply mid-cadence → `reply-classification` (planned)
- Connect rate <6% → rewrite scripts OR `lead-scoring` (re-tier list)

## Push to CRM

After scheduling, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each scheduled dial (draft) | `interaction` (type: `research`) | `relevance` = "Call scheduled for <ISO> via <dialer> with opener referencing <hook URL>"; `tags: "#scheduled #call #function-3"` |
| Each completed dial (with disposition) | `interaction` (type: `outreach`) | `relevance` = disposition + duration + notes + provenance; `tags: "#sent #call-<connected|voicemail|no-answer> #function-3"` |
| Cadence + campaign run record | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#cold-calling-run #function-3"` |
| Last-touched timestamp + phone_status changes | `person` (PATCH via dedup key) | `last_touched_at`, `last_touched_channel: call`, `phone_status` updated if changed |
| `[unverified — needs check]` (phone or hook) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #cold-calling"`; never `outreach` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
JUSTCALL_API_KEY=     # or AIRCALL / ORUM / DIALPAD / CONNECTANDSELL
DNC_COM_API_KEY=      # mandatory for US dialing
CONTACTCENTERCOMPLIANCE_API_KEY=
CALLS_PER_REP_PER_DAY_CAP=80
VOICEMAILS_PER_REP_PER_DAY_CAP=40
```

### Source tag

`source: "skill:cold-calling:v2.0.0"`

### Example push (completed call — connected)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Volaris [hypothetical]",
    "contactName": "Marcus Levy [hypothetical]",
    "contactPhone": "+15551234567 [hypothetical]",
    "tags": "#sent #call-connected #cc20-pain #function-3",
    "relevance": "Cold call connected 2026-05-23T10:32 ET (recipient local) [hypothetical]. Duration: 4m 12s [hypothetical]. Disposition: connect-positive — Marcus [hypothetical] interested in 3-week ramp [hypothetical]; meeting booked 2026-05-30T14:00 [hypothetical]. Hook: Volaris 250-employee milestone [verified: linkedin.com/company/volaris/posts/employee-milestone] [hypothetical demo URL]. Discovery: pain confirmed (8wk new-hire ramp [hypothetical]), urgency Q3 [hypothetical], champion identified [hypothetical]. Rep: Will [hypothetical]. Cadence: cad_workflowdoc_call_3dial_5d_v1 [hypothetical] (WorkflowDoc [hypothetical]). Recommended next: discovery-call-prep.",
    "source": "skill:cold-calling:v2.0.0"
  }'
```

### Example push (voicemail left)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#sent #call-voicemail #function-3",
    "relevance": "Voicemail left 2026-05-23T10:30 ET [hypothetical]. Drop length: 14s [hypothetical]. Hook reference: Volaris [hypothetical] 250-employee milestone [hypothetical]. Callback number repeated twice. Next attempt: D+2 (2:30pm ET).",
    "source": "skill:cold-calling:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#cold-calling-run #function-3",
    "relevance": "Cold call run cmp_call_2026-05-22_q9k [hypothetical]. Mode: API (JustCall). Cadence: call-3dial-5d-v1. Filter: 50 → 43 eligible [hypothetical] (2 DNC, 1 invalid, 4 called <90d). Capacity: 129 dials [hypothetical] / 400/day max / 6% utilization [hypothetical]. Compliance: 43/43 DNC-scrubbed, 100% TCPA-hours. Audit: 0 cliché / 0 no-pretend / 0 hook-citation failures. Recommended next: campaign-management (target connect rate ≥8%).",
    "source": "skill:cold-calling:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Dial occurs; pushes as `interaction:outreach`. |
| `[unverified — needs check]` | Dial is BLOCKED. Pushes ONLY as `interaction:research` with `#unverified #review-required #cold-calling` tags. |
| `[hypothetical]` | Never dials; never pushes. Local artifact only. |

### When NOT to push

- Drafts never scheduled — local artifact only.
- Dials blocked at pre-flight (DNC, invalid phone, unknown timezone, capacity) — push as `interaction:research` with block reason; never `outreach`.
- `[unverified]` phone or hook — see provenance routing.
- `[hypothetical]` — never.
- Quiet-hours violation attempted (rare manual-mode error) — log near-miss for audit; do NOT push as completed call.
