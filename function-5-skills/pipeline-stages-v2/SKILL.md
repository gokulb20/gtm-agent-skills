---
name: pipeline-stages
description: Move deals through the 8-stage B2B pipeline (New → Contacted → Engaged → Meeting → Discovery → Proposal → Closed-Won / Closed-Lost) using deterministic stage-gate rules, MEDDPICC slot completion as advance criteria, and reply / meeting / proposal events as triggers. Owns deal-state machine and stage-transition audit trail. Use when a reply / meeting / proposal event triggers a stage advance, when a deal needs stage-gate audit (which slots are filled, what's missing), when bulk pipeline cleanup classifies deals into correct stages, or when stage definitions need refresh.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, pipeline, deal-management, stages, function-5]
related_skills:
  - reply-classification
  - discovery-call-prep
  - handoff-protocol
  - lead-scoring
  - crm-hygiene
  - revenue-forecasting
  - conversation-intelligence
inputs_required:
  - deal-or-lead-record
  - state-change-trigger-event
  - stage-definitions
  - meddpicc-slot-data-when-applicable
  - run-purpose-tag
deliverables:
  - stage-transition-decision-with-rationale
  - meddpicc-gate-audit-per-deal
  - bulk-pipeline-classification-when-applicable
  - stage-transition-interaction-record
  - missing-slot-flags-for-stuck-deals
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Pipeline Stages

Move deals through 8 canonical pipeline stages with deterministic gates: New → Contacted → Engaged → Meeting → Discovery → Proposal → Closed-Won / Closed-Lost. Each stage has explicit entry criteria (event triggers + MEDDPICC slots + data quality requirements). Hard rule: a deal cannot advance to the next stage until its gates are met; stuck deals get flagged with the specific missing element rather than auto-advanced. Owns the deal-state machine + audit trail.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic. Pipeline stages chain from function-3/4 events (sends → replies → meetings → proposals).*

## Purpose

Pipelines drift when stage definitions are vibes. "Engaged" means different things to different reps; "Discovery" varies by founder; deals park in stages they don't belong to. This skill: applies one explicit stage definition with explicit gates, advances deals only when gates are met, surfaces the specific missing-slot per stuck deal so it's actionable. Goal: an honest pipeline a founder can forecast off and an AE can prioritize off.

## When to Use

- "Reply just classified positive — advance the deal to Meeting stage."
- "Audit the pipeline — which deals are in the wrong stage?"
- "Esme just signed the proposal — move to Closed-Won."
- "Bulk classify all 47 active deals into correct stages."
- "Why is this deal stuck in Discovery for 6 weeks?"
- Triggered by `reply-classification` (positive → advance) / meeting booked / proposal sent / contract signed.
- Pipeline review cadence (weekly).

## Inputs Required

1. **Deal or Lead record** — current stage, MEDDPICC slot data, history of touches + replies + meetings.
2. **State-change trigger event** — reply class, meeting booked, proposal sent, contract signed, or manual user action.
3. **Stage definitions** — default 8-stage from `.env` (`DEAL_STAGE_DEFINITIONS`); user-overridable.
4. **MEDDPICC slot data** — populated by `discovery-call-prep` and updated post-call.
5. **Run purpose tag**.

## Quick Reference

| Stage | Entry criteria (gates) | Typical exit | Avg duration |
|---|---|---|---|
| **New** | Lead created in CRM (from function-2) | Touch sent → Contacted | <7 days |
| **Contacted** | ≥1 outreach Touch sent (function-3) | Reply received → Engaged | 14–21 days (or expires to no-reply) |
| **Engaged** | Reply received (any class except `unsubscribe` / `not-interested`) | Meeting booked → Meeting | 7–14 days |
| **Meeting** | Discovery call scheduled | Meeting completed → Discovery | <14 days from booking |
| **Discovery** | Meeting held; ≥5 of 8 MEDDPICC slots populated | All 8 slots populated → Proposal | 14–30 days |
| **Proposal** | Proposal / quote sent; deal value confirmed | Signed → Closed-Won OR explicit no → Closed-Lost | 14–60 days |
| **Closed-Won** | Contract signed; revenue booked | (terminal — handoff to CSM) | n/a |
| **Closed-Lost** | Explicit no OR 90d silence post-Proposal | (terminal — feeds `icp-refinement-loop`) | n/a |

| Concept | Value |
|---|---|
| **MEDDPICC 8 slots** | Metrics / Economic Buyer / Decision Criteria / Decision Process / Paper Process (procurement / legal / security / contract steps revealed; `unknown — ask`) / Identify Pain / Champion / Competition |
| **MEDDPICC slot threshold for Discovery → Proposal** | All 8 slots populated (not all "confirmed", but at least "inferred") |
| **Stuck-deal detection** | Stage duration > 2× avg → flag with specific missing slot/event |
| **Stage-skip prohibition** | Cannot skip stages (e.g. Engaged → Proposal). All transitions must walk linearly OR jump to Closed-Lost |
| **Closed-Lost reasons** | `no-budget` / `no-authority` / `no-need` / `no-timing` / `lost-to-competitor` / `unresponsive` (90d silence) |
| **Audit trail** | Every transition logged in `interaction:stage-change` with trigger + previous-stage-duration |
| **Bulk classification** | Replays all deals through gate logic; surfaces deals in wrong stage |

## Procedure

### 1. Validate inputs
Read deal record + trigger event + stage definitions. Confirm trigger maps to a stage transition or audit request.

### 2. Identify current stage + check stuck status
Pull current stage; compute time-in-stage; flag if >2× avg duration → stuck-deal.

### 3. Match trigger to candidate transition
Trigger: `reply-positive` → potential New/Contacted/Engaged → Engaged/Meeting transition.
Trigger: `meeting-booked` → potential Engaged → Meeting transition.
Trigger: `meeting-completed` → potential Meeting → Discovery transition.
Trigger: `proposal-sent` → potential Discovery → Proposal transition.
Trigger: `contract-signed` → potential Proposal → Closed-Won transition.
Trigger: `not-interested` reply OR 90d silence post-Proposal → Closed-Lost.
Trigger: `manual-stage-set` → user-driven; still gate-checked.

### 4. Apply stage gates
For the candidate transition: check entry criteria for the target stage. Required fields per `CRM_HYGIENE_REQUIRED_FIELDS_PER_STAGE` from env. MEDDPICC slot count for Discovery → Proposal threshold.

If gates met → advance.
If gates NOT met → block transition; surface the specific missing element; flag for `crm-hygiene` (data) or `discovery-call-prep` (MEDDPICC) or `objection-handling-library` (engagement).

### 5. Stage-skip + reverse-transition handling
- Reverse transitions (Discovery → Engaged due to stalled discovery) allowed but logged with reason.
- Stage-skip prohibited unless target is Closed-Lost (escape hatch).

### 6. Bulk classification mode
When invoked for pipeline audit (not single-trigger): iterate every active deal, replay gate logic against current state, surface deals in wrong stage with recommended correct stage. Don't auto-correct without user authorization.

### 7. Update Deal record + push to CRM
On approved transition: PATCH deal record with new stage + transition timestamp. Push `interaction:stage-change` with trigger + previous-stage-duration + entered-stage-with-rationale.

### 8. Recommended next skill
- → Engaged: monitor in `campaign-management`; may need `objection-handling-library`.
- → Meeting: prep with `discovery-call-prep`.
- → Discovery: track MEDDPICC completion; `conversation-intelligence` from call transcripts.
- → Proposal: forecast in `revenue-forecasting`; may need `handoff-protocol` if SDR → AE.
- → Closed-Won: handoff to CSM / onboarding (out of function-5 scope; surface).
- → Closed-Lost: feed `icp-refinement-loop`; capture lost-reason for analysis.

## Output Format

- Stage transition decision (advance / block / reverse) with rationale per gate
- MEDDPICC gate audit per Discovery / Proposal stage check
- Stuck-deal flags (deal id + time-in-stage + specific missing element)
- Bulk classification report (when in audit mode): correct-stage / wrong-stage distribution + recommendations
- Deal record PATCH (new stage, timestamp, prior-stage-duration)
- Run record: triggers processed, transitions executed, stuck deals flagged, recommended next skills

## Done Criteria

1. Trigger validated; candidate transition identified.
2. Stage gates checked; transition advanced or blocked with specific missing element.
3. Stage-skip prohibition enforced (only Closed-Lost is the escape).
4. Stuck-deal flag emitted when time-in-stage >2× avg.
5. Deal record PATCHed; `interaction:stage-change` pushed.
6. Recommended next skill surfaced per new stage.
7. Bulk-mode (when applicable): all active deals replayed; wrong-stage report surfaced.

## Pitfalls

- **Vague stage definitions.** "Engaged" needs an explicit entry event (a reply was received), not "feels engaged."
- **Auto-advancing without gate checks.** Reply-positive without booked meeting ≠ Meeting stage.
- **Stage-skipping.** Discovery → Closed-Won without Proposal is data corruption; flag for review.
- **Letting stuck deals linger.** Time-in-stage >2× avg is the canary; surface AND name the missing element.
- **Closed-Lost without a reason.** Lost-reason feeds `icp-refinement-loop`; missing reason = wasted learning.
- **Reverse-transitions silently.** Allowed but MUST be logged with explicit reason (otherwise pipeline shuffles).
- **MEDDPICC threshold treated as binary.** "All 8 populated" doesn't mean "all confirmed" — inferred is acceptable for Proposal entry; threshold for Closed-Won is stricter (≥6 confirmed, including Paper Process).
- **Stage definitions vary across sales motions.** PLG deals may compress (Engaged ↔ Discovery skip Meeting); enterprise expand. User can override defaults; surface the override.
- **Bulk-classification auto-corrects.** Always require user authorization before mass stage updates — moves are visible across the org.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (deals, recipients, MEDDPICC slot content, dates, lost-reasons) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Stage-change rationale references actual events (reply id, meeting id, proposal id); never invent triggers.
- **Treating CSM handoff as part of pipeline.** Closed-Won is terminal in this skill; downstream is out of scope.

## Verification

Run is real when: every transition has a documented trigger event + gate-check result; stuck-deal flags name specific missing elements; bulk-classification recommendations reference real deal records; reverse-transitions logged with reason; no stage-skips except to Closed-Lost. Negative test: pick 5 random `interaction:stage-change` records; trace each back to the trigger event in the CRM — if any transitions appear without source events, advance logic broke.

## Example

**User prompt:** "Esme just replied positive and booked a discovery call for next Tuesday — advance the deal."
**What should happen:** Trigger: `meeting-booked` event. Current stage: Engaged (positive reply already moved it from Contacted). Candidate transition: Engaged → Meeting. Gate: meeting scheduled with confirmed time → ✓. Advance. PATCH deal: stage=Meeting, transition_at=now, prior_stage_duration=8d. Push `interaction:stage-change`. Recommended next: `discovery-call-prep` for the Tuesday meeting.

**User prompt:** "Audit the pipeline — show me deals in wrong stages."
**What should happen:** Bulk-classification mode. Iterate 47 active deals, replay gate logic. Findings: 3 deals in Discovery missing MEDDPICC slots (recommend stay-in-Discovery + flag for slot completion); 2 deals in Engaged with no reply (recommend revert to Contacted + check if reply was missed); 1 deal in Proposal stuck 78 days (>2× avg 30d) — flag stuck, recommend force decision (proposal-update OR move to Closed-Lost-unresponsive). Surface all to user; await authorization before applying.

**User prompt:** "Move the Acme deal to Closed-Lost. Reason: lost to Guru."
**What should happen:** User-driven transition. Candidate: current_stage → Closed-Lost. Gate: lost-reason required → "lost-to-competitor" with named competitor "Guru". Advance. PATCH deal: stage=Closed-Lost, lost_reason=lost-to-competitor, lost_competitor=Guru, transition_at=now. Push `interaction:stage-change`. Route lost-reason to `icp-refinement-loop` (function-6) and competitor mention to `competitive-intelligence` (function-1) for pattern aggregation.

## Linked Skills

- Stage advance triggered by reply → upstream `reply-classification`; meeting prep → `discovery-call-prep`
- Discovery slot completion → upstream from `discovery-call-prep` updates
- Stuck-deal hygiene → `crm-hygiene`; forecast → `revenue-forecasting`; handoff → `handoff-protocol`
- Conversation intel from meeting → `conversation-intelligence`
- Closed-Lost analysis → `icp-refinement-loop`; lost to competitor → `competitive-intelligence`

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-5-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Stage transition (advance / reverse / Closed) | `interaction` (type: `stage-change`) | `relevance` = from-stage → to-stage + trigger + gate result + prior duration; `tags: "#stage-change #stage-<to-stage> #function-5"` |
| Deal record PATCH | `deal` (PATCH via deal_id) | `stage`, `stage_entered_at`, `prior_stage_duration_days`, `meddpicc_slots_filled` (count), `lost_reason` if applicable |
| Stuck-deal flag | `interaction` (type: `research`) | `relevance` = deal id + time-in-stage + specific missing element + recommendation; `tags: "#stuck-deal #function-5"` |
| Bulk classification report | `interaction` (type: `research`) | `relevance` = counts of correct-stage / wrong-stage + per-deal recommendations; `tags: "#pipeline-audit #function-5"` |
| Run record | `interaction` (type: `research`) | `relevance` = triggers processed + transitions executed + flags surfaced; `tags: "#pipeline-stages-run #function-5"` |
| `[unverified — needs check]` | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #pipeline-stages"`; deal PATCH deferred |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
DEAL_STAGE_DEFINITIONS=new,contacted,engaged,meeting,discovery,proposal,closed-won,closed-lost
CRM_HYGIENE_REQUIRED_FIELDS_PER_STAGE=     # JSON; per-stage required-field map
```

### Source tag

`source: "skill:pipeline-stages:v2.0.0"`

### Example push (stage advance)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#stage-change #stage-meeting #function-5",
    "relevance": "Deal deal_stitchbox_2026-05 advanced from Engaged → Meeting on 2026-05-30. Trigger: meeting booked for 2026-06-02T14:00 PT [verified: calendar event id evt_h7k]. Gate: meeting scheduled with confirmed time ✓. Prior stage duration: 8 days (within 7–14d typical). Recommended next: discovery-call-prep for the 2026-06-02 meeting.",
    "source": "skill:pipeline-stages:v2.0.0"
  }'
```

### Example push (stuck-deal flag)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#stuck-deal #function-5",
    "relevance": "Deal deal_acme_2026-03 stuck in Proposal stage 78 days (>2× avg 30d). Last stage event: proposal sent 2026-03-13. No reply received since. Missing element: explicit go/no-go decision OR proposal update. Recommendation: force-decision via outreach OR move to Closed-Lost-unresponsive (90d silence rule). Surface to user.",
    "source": "skill:pipeline-stages:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (manual stage set) or `[verified: <source>]` (event-triggered with referenced event id) | Standard mapping. |
| `[unverified — needs check]` (trigger event missing or ambiguous) | Pushes ONLY as `interaction:research` with `#unverified #review-required #pipeline-stages` tags; deal PATCH deferred. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Trigger event maps to no candidate transition (e.g. negative reply on Engaged stage) — no transition; do not push stage-change.
- Bulk classification produced 0 wrong-stage findings — push run record with `#pipeline-clean`; no per-deal flags.
- Stuck-deal already flagged within last 7d — dedup; do not double-flag.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
