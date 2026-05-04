---
name: follow-up-management
description: Manage post-reply nurture, scheduling, and re-engagement for `not-now`, `out-of-office`, and warm-but-not-now recipients. Owns the 30/60/90-day nurture cadence library, calendar-aware re-engage scheduling, and the parsing of stated resume dates from reply text. Use when `reply-classification` flags a `not-now` reply with stated resume date, when an `out-of-office` reply needs scheduled resume after the OOO end date, when a meeting no-show needs rescue, or when a Tier-1/2 recipient parked in nurture needs the next touch scheduled.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, conversation-management, follow-up, nurture, function-4]
related_skills:
  - reply-classification
  - objection-handling-library
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - multi-channel-cadence
  - campaign-management
  - pipeline-stages
  - lead-scoring
inputs_required:
  - classified-reply-or-cadence-trigger
  - lead-record
  - calendar-or-scheduling-tool-access
  - default-nurture-cadence-or-override
  - run-purpose-tag
deliverables:
  - per-recipient-resume-or-nurture-schedule
  - parsed-resume-date-from-reply-text
  - scheduled-follow-up-touch-handoff
  - nurture-cadence-config-when-applicable
  - meeting-no-show-rescue-flow
  - follow-up-management-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Follow-Up Management

Schedule the right follow-up at the right time for recipients who replied `not-now` (with or without stated date), bounced through `out-of-office`, parked in nurture, or no-showed a discovery call. Owns the parsing of natural-language resume dates from reply text ("Q1 2027" → 2027-01-15), the 30/60/90-day standard nurture cadences, and the meeting-no-show rescue flow. Hands off scheduled touches to channel skills (`cold-email-sequence`, `linkedin-outreach`) to actually execute.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

After a reply that isn't a hard no, the most-common failure mode is forgetting. Founder reads "ping me in March" on October 15, doesn't write it down, calendar moves on, March arrives without action. This skill: parses the resume date from reply text (or applies sensible defaults), schedules the resume touch on the right channel + right cadence, schedules nurture touches in between for warm recipients, and handles the no-show rescue (a 24h-window touch designed to recover the meeting). Goal: zero "I forgot to follow up" failures across the active prospect base.

## When to Use

- "Esme replied 'ping me in Q1 2027' — schedule the resume."
- "OOO auto-reply with return date next Tuesday — pause + resume."
- "Meeting no-show — rescue flow."
- "Tier-1 recipient parked in nurture — schedule the 30/60/90 cadence."
- "Bulk schedule resume touches for the 12 not-now replies from this campaign."
- Triggered by `reply-classification` on `not-now` / `out-of-office` labels.
- Post-cadence-completion when a recipient is high-fit but didn't engage yet.

## Inputs Required

1. **Classified reply or cadence trigger** — from `reply-classification` (`not-now`, `out-of-office`, `question` resolved to nurture) OR meeting-no-show event OR cadence-completion event.
2. **Lead record** — score, tier, signals, prior cadence + reply history.
3. **Calendar / scheduling tool access** — `CALENDLY_API_KEY` / `CAL_COM_API_KEY` / `GOOGLE_CALENDAR_OAUTH_TOKEN` (for meeting-related follow-ups); else manual mode.
4. **Default nurture cadence** — `FOLLOW_UP_NURTURE_DEFAULT_DAYS=30` (with 30/60/90 standard); user can override per recipient.
5. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Resume-date sources** | (a) explicit date in reply text → parse + use · (b) implied window ("next quarter", "after the holidays") → resolve to specific date · (c) no date → default 60d for `not-now` / 90d for `tried-similar-failed` / OOO end date for `out-of-office` |
| **Nurture cadence library** | `30-60-90-light` (3 touches: 30d / 60d / 90d, low-friction email) · `90-180-365-deep` (3 touches over a year for re-engagement) · `meeting-no-show-rescue` (1 touch within 24h, 1 follow-up at 7d) |
| **Date parsing** | Natural language → ISO. "Q1 2027" → 2027-01-15. "After Christmas" → 2027-01-05 (US). "Late spring" → 2027-05-20. "Next month" → first business day next calendar month. Provenance: `[verified: reply-text]` for explicit; `[unverified — needs check]` for inferred. |
| **Resume-touch channel** | Same channel as original reply, unless explicitly redirected ("email me at X@Y" overrides). |
| **Resume-touch framework** | "Resurrection" framework (function-3 cold-email touch 7) — different angle than original cadence; reference the prior conversation. |
| **No-show rescue window** | Within 24h of missed meeting; tone: low-stakes, single CTA to reschedule. |
| **Nurture content** | Light, value-first; not sales pitches. Industry insight / case-study link / brief check-in. |
| **Capacity-cap respect** | Resume + nurture touches count against the same per-channel caps as cold cadences |

## Procedure

### 1. Validate inputs
Read trigger event + lead record + cadence/reply history. Confirm trigger type (not-now / OOO / nurture / no-show) + recipient identity.

### 2. Parse resume date (when applicable)
For `not-now` replies: extract date / window from reply text. Pattern-match common phrases ("Q1 2027" / "next quarter" / "after the holidays" / specific date). When ambiguous, default per the matrix in Quick Reference. Tag provenance.

### 3. Pick follow-up flow
- **`not-now` with date** → single resume touch on stated date.
- **`not-now` without date** → 60d resume (default).
- **`out-of-office`** → resume on OOO end date + 1 (next business day).
- **Nurture-park** → `30-60-90-light` cadence by default.
- **Re-engagement (cold-aged)** → `90-180-365-deep` cadence.
- **Meeting no-show** → `meeting-no-show-rescue` flow.

### 4. Generate resume / nurture touches
Hand off to channel skill (`cold-email-sequence`, `linkedin-outreach`) with: cadence position context = "resume after `not-now` of <date>" / "nurture touch <N>" / "no-show rescue". Channel skill produces copy with appropriate framework (Resurrection / nurture-light / rescue tone).

### 5. Schedule + capacity check
Compute new touches against per-channel weekly caps. If over capacity, surface for user to extend timeline or expand sender pool. Schedule via channel skill's API mode (or manual handoff).

### 6. Update Lead record
PATCH person record: `next_followup_at: <date>`, `nurture_state: <type>`, `cadence_state: paused | nurture | resurrection`.

### 7. Push to CRM + emit run summary
Per conventions: per-recipient `interaction:research` with the schedule + framework choice + provenance on the parsed date. Run summary: triggers processed, distribution by flow type, scheduled touches, recommended re-eval date.

## Output Format

- Per-recipient: parsed resume date (or default rationale) + chosen flow + scheduled touches handed off to channel skill
- Nurture cadence config when applicable (touches, day_offsets, framework)
- Capacity check result (within cap / over cap)
- Lead record patches: `next_followup_at` / `nurture_state` / `cadence_state`
- Run record: triggers processed, flow distribution, scheduled-touch count
- Recommended next skill (`campaign-management` to monitor; back to channel skill at resume time)

## Done Criteria

1. Trigger event validated; lead context loaded.
2. Resume date parsed with provenance OR default-rationale documented.
3. Follow-up flow picked per trigger + recipient state.
4. Touches generated via channel-skill handoff.
5. Capacity check passed (or user authorized over-cap).
6. Lead record patched with `next_followup_at` + `nurture_state` + `cadence_state`.
7. Push to CRM emitted; run summary one-screen.

## Pitfalls

- **Forgetting the parsed date.** Reply says "March 15"; if not stamped on the Lead, will be missed. ALWAYS PATCH.
- **Default 60d when reply named a date.** Read the reply text carefully; honor the stated date.
- **Same channel as original reply (default) without checking redirect.** "Email me at X@Y" overrides — use the redirect.
- **No-show rescue at 7 days instead of 24 hours.** Window matters; later than 48h reads as nag.
- **Nurture touches that pitch.** Nurture is value-first; pitches in nurture trigger unsubscribes.
- **Skipping capacity check for resume volume.** A campaign producing 30 not-now replies all stating "Q1 2027" creates a Q1 capacity spike — surface early.
- **Multiple resume touches for the same recipient.** Dedup by Lead — one resume per stated date.
- **Re-engaging on `not-interested`.** Hard no = exit-permanent (per `reply-classification` cadence-state effects); follow-up does NOT re-engage these.
- **Holiday-window resume.** "Q1 2027" arriving mid-December — schedule for Jan 5 (post-holiday), not Dec 25.
- **Multi-language resume parsing.** "Después de las fiestas" needs locale-aware parsing; if unknown locale, flag `[unverified — needs check]`.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (recipient, company, parsed dates, prior reply quotes, scheduled touch references) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Resume dates explicit in reply text are `[verified: reply-text]`; inferred from window phrases are `[unverified — needs check]` and surface for user confirmation if Tier-1.
- **Letting nurture-aged recipients linger past 12 months.** Re-engagement cadence beyond 365d is rarely worth it; mark `archived` instead.

## Verification

Run is real when: every trigger has either a scheduled resume touch OR a documented archive decision; resume dates trace to reply text or a documented default; channel-skill handoffs succeeded with cadence position context; person records patched with new state; capacity checks passed at schedule time. Negative test: pick 5 random scheduled resume touches; trace each to its parsed date + provenance; if any date "appeared from thin air" (no reply text or default rule), parsing is broken.

## Example

**User prompt:** "12 not-now replies from this campaign — schedule resume touches for all."
**What should happen:** Per reply, parse stated date or apply default (60d for unstated). Distribution: 7 with explicit dates (Q1 2027 / March / after holidays / etc.) → parsed; 5 with no stated date → 60d default. Per recipient: pick channel (default = original reply channel), hand off to channel skill (cold-email-sequence in resurrection mode), capacity-check the scheduled touches. PATCH 12 person records with `next_followup_at`. Push 12 `interaction:research` records. Recommend `campaign-management` to monitor when resume touches go live.

**User prompt:** "Esme just no-showed our 2pm meeting."
**What should happen:** Trigger: meeting-no-show. Flow: `meeting-no-show-rescue`. Within 24h: light single-CTA email ("Caught you at a bad moment? Happy to reschedule — here's my next 3 open windows"). 7-day follow-up if no reply. PATCH person: `last_no_show_at`, `nurture_state: no-show-rescue`. Hand off touch to `cold-email-sequence` with rescue framework.

**User prompt:** "Reply: 'Looks interesting but we're focused on H1 priorities right now. Touch base in May?'"
**What should happen:** Classified `not-now` (per reply-classification). Parse "in May" — assume current year if forward, else next year. If today is March 2026: May 2026. If today is October 2026: May 2027 (forward). Default to first business day (May 1 → May 4 if weekend). Schedule single resume touch on parsed date, channel = email (original channel), framework = resurrection (different angle than original cadence). PATCH person: `next_followup_at: 2026-05-04`. Provenance: `[verified: reply-text]` on the May reference + `[verified: agent-rule]` on the day-1 → day-4 weekend shift.

## Linked Skills

- `not-now` / `out-of-office` reply trigger → upstream `reply-classification`
- Embedded objection in not-now → `objection-handling-library` (response) + this skill (schedule)
- Resume touch execution → `cold-email-sequence` / `linkedin-outreach` (in resurrection mode)
- Capacity overrun → back to `multi-channel-cadence` for capacity replanning
- Active campaign with follow-ups → `campaign-management`
- Stage advance from positive resume reply → `pipeline-stages`
- Re-engagement aging into 12mo+ → archive recommendation; surface for `lead-scoring` re-tier

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-4-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-recipient resume / nurture schedule | `interaction` (type: `research`) | `relevance` = trigger + parsed-date + flow + framework + scheduled-touch ref; `tags: "#follow-up-scheduled #flow-<type> #function-4"` |
| Nurture-cadence definition (when applicable) | `interaction` (type: `research`) | `relevance` = touches + day_offsets + frameworks; `tags: "#nurture-cadence #function-4"` |
| Per-recipient state PATCH | `person` (PATCH via dedup key) | `next_followup_at`, `nurture_state`, `cadence_state`, `last_no_show_at` if applicable |
| Meeting-no-show rescue trigger | `interaction` (type: `research`) | `relevance` = no-show event + rescue flow scheduled; `tags: "#no-show-rescue #function-4"` |
| Run record | `interaction` (type: `research`) | `relevance` = triggers processed + flow distribution + scheduled-touch count; `tags: "#follow-up-management-run #function-4"` |
| `[unverified — needs check]` (ambiguous resume date) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #follow-up-management"`; person PATCH deferred |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
CALENDLY_API_KEY=     # or CAL_COM_API_KEY / GOOGLE_CALENDAR_OAUTH_TOKEN
FOLLOW_UP_NURTURE_DEFAULT_DAYS=30
```

### Source tag

`source: "skill:follow-up-management:v2.0.0"`

### Example push (resume scheduled)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#follow-up-scheduled #flow-not-now-with-date #function-4",
    "relevance": "Follow-up scheduled for esme@stitchbox.com. Trigger: reply rpl_2026-05-29 classified not-now with stated date 'Q1 2027'. Parsed: 2027-01-15 [verified: reply-text + agent-rule (Q1=Jan 15 default)]. Flow: single resume touch on 2027-01-15. Channel: email (original reply channel). Framework: resurrection (different angle than original cadence). Handed off to cold-email-sequence. Person PATCHed: next_followup_at=2027-01-15, nurture_state=parked, cadence_state=paused.",
    "source": "skill:follow-up-management:v2.0.0"
  }'
```

### Example push (no-show rescue)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#no-show-rescue #function-4",
    "relevance": "No-show rescue triggered for esme@stitchbox.com. Missed meeting: 2026-06-02T14:00 PT. Flow: meeting-no-show-rescue. Touch 1 scheduled within 24h: light single-CTA reschedule offer. Touch 2 scheduled D+7 if no reply. Channel: email. Tone: rescue (low-stakes, no nag). Handed off to cold-email-sequence.",
    "source": "skill:follow-up-management:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (reply text) + `[verified: <source>]` (parsed date) | Standard mapping. |
| `[unverified — needs check]` (ambiguous date phrase, multi-language locale unknown) | Pushes ONLY as `interaction:research` with `#unverified #review-required #follow-up-management` tags; person PATCH deferred until user confirms parsed date. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- `not-interested` reply (handled by `reply-classification` exit logic, not this skill).
- Recipient has unsubscribed (global cross-channel exit; no follow-up allowed).
- Trigger has no actionable recipient (e.g., bounce that should route to channel skill).
- Capacity exceeded with no user authorization for over-cap → push the run record with `#blocked-capacity`; no per-recipient schedules.
- `[unverified]` ambiguous date — see provenance routing.
- `[hypothetical]` — never.
