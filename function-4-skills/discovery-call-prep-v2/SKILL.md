---
name: discovery-call-prep
description: Produce a 1-page founder/AE briefing for an upcoming discovery call — recipient profile, ICP fit + tier rationale, signals + hooks, MEDDPICC slots populated from existing intel, 3 discovery question genres (open / pain-quantify / next-step), 3 likely objections with pre-staged responses, competitive context, and recommended call agenda. Use when a meeting books from `reply-classification`'s positive label, when a call is scheduled <48h out and intel needs refreshing, when a high-stakes Tier-1 call needs a deep brief, or when a call rescheduled and prior briefing is stale.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, conversation-management, discovery-prep, briefing, function-4]
related_skills:
  - reply-classification
  - lead-scoring
  - data-enrichment
  - icp-definition
  - positioning-strategy
  - competitor-analysis
  - competitive-intelligence
  - objection-handling-library
  - handoff-protocol
  - pipeline-stages
inputs_required:
  - meeting-context-and-time
  - lead-record-with-history
  - prior-cadence-and-reply-thread
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - competitor-context
  - run-purpose-tag
deliverables:
  - 1-page-founder-briefing
  - meddpicc-slot-snapshot
  - 3-discovery-questions-per-genre
  - 3-likely-objections-with-responses
  - call-agenda-recommendation
  - competitive-context-section
  - discovery-prep-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Discovery Call Prep

Produce a 1-page founder/AE briefing for an upcoming discovery call: recipient profile, ICP fit + tier rationale, signals + hooks, MEDDPICC slots populated from existing intel, 3 discovery questions per genre (open / pain-quantify / next-step), 3 likely objections with pre-staged responses from `objection-handling-library`, competitive context, and recommended call agenda. Goal: founder walks into the call having read 1 page and knowing exactly what they're trying to learn and what to push on.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Discovery calls fail when the founder hasn't refreshed context since the meeting was booked. They also fail when the briefing is 8 pages and the founder skims the first paragraph. This skill produces ONE PAGE — fits a single screen — with everything a founder needs in 90 seconds of pre-call review. MEDDPICC slots are populated from existing intel (most are pre-filled by function-1 + function-2); discovery questions are tailored to fill the empty MEDDPICC slots; objections are pre-staged so the founder isn't reaching mid-call.

## When to Use

- "Discovery call booked with Esme at Stitchbox tomorrow 2pm — prep me."
- "Reschedule pushed our call to Friday — refresh the briefing."
- "5 calls on the calendar this week — pre-prep all of them."
- "High-stakes Tier-1 call — give me the deep brief."
- "Founder hand-off: I'm taking this call from the SDR's cadence."
- Triggered by `reply-classification` flagging a `positive` reply with meeting request.
- Pre-call refresh window (24–48h before scheduled call).

## Inputs Required

1. **Meeting context** — scheduled time, channel (video / phone), attendees (founder + recipient + others).
2. **Lead record** — full Lead schema from function-2 + scoring rationale.
3. **Prior cadence + reply thread** — every Touch sent + every reply received. Provides conversational context.
4. **ICP P-T-O chain** from `icp-definition` — pain anchors for question genre 2.
5. **Positioning message house** from `positioning-strategy` — value-prop anchors for the call.
6. **Competitor context** from `competitor-analysis` and `competitive-intelligence` — known/likely competitors; battle-card excerpts for the tier-1 ones.
7. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Briefing length** | 1 page (≤450 words / one screen). Hard ceiling. |
| **MEDDPICC slots** | Metrics / Economic Buyer / Decision Criteria / Decision Process / **Paper Process** (procurement / legal / security / contract steps revealed; `unknown — ask`) / Identify Pain / Champion / Competition. 8 slots — each populated from existing intel OR labeled `unknown — ask in call`. |
| **Discovery question genres** | (1) open-discovery (3 questions: their world / pain context) · (2) pain-quantify (3 questions: cost of doing nothing) · (3) next-step (3 questions: decision process / champion / timeline) |
| **Objection prep** | 3 most-likely objections per recipient profile; pre-staged responses pulled from `objection-handling-library` |
| **Competitive context** | 1–3 likely competitors (per their stack signals + reply intel); 1-line counter-positioning per competitor |
| **Briefing freshness** | ≤48h old at call time; stale → re-prep |
| **Apple-MPP-aware** | Don't include "they opened your email N times" — opens are noise (reply rate is the signal) |
| **Hook restatement** | Briefing surfaces the original verified hook + which Touch the recipient replied to — establishes context for founder |
| **Anti-fabrication hard rule** | Every named entity in the briefing carries provenance; "Esme mentioned X" requires the reply or call note saying X |

## Procedure

### 1. Validate inputs + assemble recipient profile
Read meeting context + lead record + cadence/reply thread. Confirm meeting <48h (else re-prep). Profile (≤80 words): name, title, company, ICP tier+score, hook (verified URL), most-recent reply context.

### 2. Populate MEDDPICC slots from existing intel
Metrics (from ICP P-T-O + reply figures); Economic Buyer (from role map); Decision Criteria (from positioning house); Decision Process (`unknown — ask`); Paper Process (procurement / legal / security / contract steps revealed; default `unknown — ask`); Identify Pain (from ICP P-T-O); Champion (from role map); Competition (from tech-stack + competitive-intelligence). Provenance per slot; `unknown` → routes to discovery question.

### 3. Generate 3 questions per genre
- **Open-discovery**: 3 questions on current state, anchored to verified pain.
- **Pain-quantify**: 3 questions on cost ("What does extra 6 weeks of ramp cost you?").
- **Next-step**: 3 questions on decision process / champion / timeline.

Questions reference verified pain anchors; never invent customer outcomes.

### 4. Pre-stage 3 likely objections + competitive context
3 most-likely objections per recipient profile; pull responses from `objection-handling-library` (framework attribution + 1–2 sentence variant). 1–3 likely competitors; per competitor: 1-line counter-positioning + 1-line "if they push back, ask:" question.

### 5. Recommended call agenda + push
Agenda (3 bullets): 5 min mutual context + open-discovery / 15 min pain-quantify / 5–10 min next-step. Push briefing as `interaction:research`; PATCH person with `discovery_briefing_at` + `next_meeting_at`.

## Output Format

- 1-page briefing (≤450 words / single-screen) with sections: profile / MEDDPICC / questions / objections / competitive / agenda
- MEDDPICC slot table — 8 slots (Metrics / Economic Buyer / Decision Criteria / Decision Process / Paper Process / Identify Pain / Champion / Competition); populated + `unknown` flags
- Discovery questions × 3 genres × 3 questions = 9 total
- Objection prep × 3 with response variants
- Competitive context × 1–3 competitors with counter-positioning
- Recommended call agenda
- Briefing freshness timestamp
- Recommended next skill (`pipeline-stages` after call to advance stage; `objection-handling-library` if specific objection needs deeper prep)

## Done Criteria

1. Meeting context validated; briefing within 48h of call time.
2. Recipient profile section ≤80 words; full provenance on every named entity.
3. MEDDPICC slots populated from existing intel; `unknown` slots flagged for discovery.
4. 3 questions × 3 genres = 9 questions generated; questions reference verified pain anchors.
5. 3 likely objections pre-staged with responses from `objection-handling-library`.
6. Competitive context section with 1–3 competitors + counter-positioning.
7. Call agenda recommended (≤3 bullets).
8. Briefing total ≤450 words; pushed to CRM as `interaction:research`; person PATCH with timestamps.

## Pitfalls

- **8-page briefings.** Founder reads first paragraph + skims. 1 page is the discipline.
- **Including open rate.** Apple MPP made it noise. Reply rate + reply text is the signal.
- **Inventing MEDDPICC slot content.** When champion is unknown, say `unknown — ask`; don't guess.
- **Generic discovery questions.** Anchor every question to a verified pain or signal from THIS recipient.
- **Stale briefing.** >48h old → re-prep cheaply rather than walk in with old intel.
- **Missing reply context.** Founder needs "they replied to Touch 2 with X" — establishes continuity in the call's first 30 seconds.
- **Skipping competitive context.** Even if no competitor mentioned in reply, the recipient's tech stack usually points at one.
- **Over-prepping objections.** 3 likely is enough; 8 is paralysis. Handle the rest live with `objection-handling-library`.
- **Briefing inflation per Tier-2/3.** Tier-1 deserves the deep brief; Tier-2/3 should be lighter (or skip the call).
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (recipient, company, prior reply quotes, MEDDPICC slot content, competitor mentions, dates) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Briefing claims like "Esme mentioned X" require the reply text saying X; never invent.
- **Not handing off to `pipeline-stages` post-call.** The call's outcome (advance / stall / disqualify) is a stage trigger; close the loop.

## Verification

Briefing is real when: total word count ≤450; every named entity has provenance; MEDDPICC slot content traces to a real Lead-record field or reply text or `unknown`; questions reference verified pain anchors (not generic); 3 objections + 3 questions × 3 genres + 1–3 competitors all present; freshness timestamp ≤48h. Negative test: hide the briefing; ask the founder to paraphrase what they expect to learn — if they can answer in <60 sec, briefing did its job.

## Example

**User prompt:** "Discovery call booked with Esme at Stitchbox tomorrow 2pm PT. Prep me."
**What should happen:** 1-page briefing produced:
- **Profile (62 words):** Esme Liang [verified: data-enrichment], VP Customer Support @ Stitchbox [hypothetical], Tier-1 / 87 score. Hook: VP CX hire 2026-04-19 [verified: news url]. Replied to Touch 2 (LI connection-with-note) on 2026-05-29 with: "Yes, this lands at right time — open to 15-min Tuesday."
- **MEDDPICC (8 slots):** Metrics (typical 6-8wk new-hire ramp at Series B SaaS support [verified: ICP P-T-O]) / Economic Buyer (VP Support, likely Esme herself [verified: role map]) / Decision Criteria (`unknown — ask`) / Decision Process (`unknown — ask`) / Paper Process (`unknown — ask`; security review likely given enterprise data) / Pain (knowledge fragmentation across 8+ tools [verified: ICP signal]) / Champion (Esme + Support Ops Manager [inferred from role map]) / Competition (Guru detected in stack [verified: BuiltWith via data-enrichment]).
- **9 questions** across 3 genres tailored to Stitchbox.
- **3 objections + responses:** already-using-Guru / no-budget-Q4 / wrong-time-of-quarter (each with 1-line counter from objection-handling-library).
- **Competitive:** Guru (1-line counter-position from message house: "Guru optimizes for Q&A discovery; WorkflowDoc handles run-book execution — different jobs.").
- **Agenda:** 5 min context / 15 min pain-quantify / 5–10 min next-step.

**User prompt:** "Pre-prep all 5 calls this week."
**What should happen:** Batch run for the 5 booked meetings. Per recipient: profile + MEDDPICC + questions + objections + competitive + agenda. All briefings ≤450 words; 5 push to CRM. Recommend re-running 24h before each respective meeting if briefing >48h at call time.

**User prompt:** "Call rescheduled from Tuesday to Friday — refresh."
**What should happen:** Detect rescheduled meeting + check briefing freshness. If >48h old at new call time, re-pull latest reply thread + recheck competitive intel + regenerate. If <48h, lightly refresh competitive section only and update freshness timestamp.

## Linked Skills

- `positive` reply with meeting → upstream `reply-classification`; objection responses → `objection-handling-library`
- Lead context → `lead-scoring` + `data-enrichment`; competitive → `competitor-analysis` + `competitive-intelligence`
- ICP P-T-O + role map → `icp-definition`; positioning → `positioning-strategy`
- Post-call stage advance → `pipeline-stages`; founder-handoff → `handoff-protocol`
- Conversation intelligence post-call → `conversation-intelligence`

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-4-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| 1-page briefing | `interaction` (type: `research`) | `relevance` = full briefing (≤450 words) + meeting context + freshness timestamp; `tags: "#discovery-briefing #function-4"` |
| MEDDPICC slot snapshot (8 slots) | `interaction` (type: `research`) | `relevance` = each of 8 slots (Metrics / Economic Buyer / Decision Criteria / Decision Process / Paper Process / Identify Pain / Champion / Competition) + populated/unknown + provenance per slot; `tags: "#meddpicc-snapshot #function-4"` |
| Per-meeting timestamp | `person` (PATCH via dedup key) | `discovery_briefing_at`, `next_meeting_at`, `next_meeting_channel` |
| Pre-staged objection responses | `interaction` (type: `research`) | `relevance` = 3 likely objections + responses from objection-handling-library; `tags: "#pre-staged-objections #function-4"` |
| `[unverified — needs check]` (briefing references unverified context) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #discovery-call-prep"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
ANTHROPIC_API_KEY=     # or OPENAI_API_KEY (for briefing composition)
DISCOVERY_BRIEFING_FRESHNESS_DAYS=2
```

### Source tag

`source: "skill:discovery-call-prep:v2.0.0"`

### Example push (briefing)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#discovery-briefing #function-4 #tier-1",
    "relevance": "Discovery briefing for 2026-06-02T14:00 PT call. Profile: VP Customer Support @ Stitchbox, Tier-1/87. Hook: VP CX hire 2026-04-19. Replied to Touch 2 (LI connect) 2026-05-29: \"Yes, lands at right time — 15-min Tuesday.\" MEDDPICC (8 slots): Metrics ✓ / Economic Buyer ✓ / Decision Criteria unknown / Decision Process unknown / Paper Process unknown (security review likely) / Pain ✓ / Champion ✓ / Competition Guru detected. 9 discovery questions (3 open / 3 pain-quantify / 3 next-step) tailored. 3 objections pre-staged (already-using-Guru / no-budget-Q4 / wrong-time-quarter). Competitive: Guru (counter: optimizes Q&A discovery vs runbook execution). Agenda: 5/15/10. Briefing freshness: 2026-06-01T10:00 PT (<48h).",
    "source": "skill:discovery-call-prep:v2.0.0"
  }'
```

### Example push (MEDDPICC snapshot)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#meddpicc-snapshot #function-4",
    "relevance": "MEDDPICC (8 slots) for esme@stitchbox.com, call 2026-06-02. Metrics: 6-8wk new-hire ramp [verified: ICP-PTO]. Economic Buyer: VP Support (Esme) [verified: role-map]. Decision Criteria: unknown — ask. Decision Process: unknown — ask. Paper Process: unknown — ask (procurement / legal / security review steps; security likely given enterprise data). Identify Pain: knowledge fragmentation across 8+ tools [verified: ICP-signal]. Champion: Esme + Support Ops Manager [inferred: role-map]. Competition: Guru detected [verified: BuiltWith via data-enrichment].",
    "source": "skill:discovery-call-prep:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Standard mapping. |
| `[unverified — needs check]` | Briefing flagged unverified-content; pushes ONLY as `interaction:research` with `#unverified #review-required #discovery-call-prep` tags; person PATCH for freshness only. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Meeting cancelled — push cancellation note as `interaction:research` with `#meeting-cancelled`; do not push briefing.
- Meeting outside 48h freshness window — re-prep instead of pushing stale briefing.
- Briefing failed minimum-content gates (<3 questions, no MEDDPICC, etc.) — push `#briefing-incomplete` flag for manual completion.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
