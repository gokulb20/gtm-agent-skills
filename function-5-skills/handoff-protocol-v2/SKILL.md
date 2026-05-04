---
name: handoff-protocol
description: Hand off SAL-eligible leads / opportunities from SDR to AE (or SDR to founder) with a complete briefing package — 1-page founder briefing (from `discovery-call-prep`), MEDDPICC slot snapshot, full conversation history, pre-staged objection responses, and explicit acceptance criteria for the receiving rep. Tracks acceptance / rejection / takeback per SiriusDecisions SAL norms. Use when a deal advances to Meeting / Discovery and the SDR is handing to AE, when a Tier-1 founder-led prospect needs handing to founder for the close, or when bulk handoff of a campaign's positive replies needs orchestration.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, pipeline, sdr-ae-handoff, briefing, function-5]
related_skills:
  - reply-classification
  - discovery-call-prep
  - pipeline-stages
  - lead-scoring
  - objection-handling-library
  - conversation-intelligence
  - kpi-reporting
inputs_required:
  - sal-eligible-lead-or-opportunity
  - receiving-rep-identity
  - prior-cadence-and-reply-history
  - meeting-context-when-applicable
  - acceptance-criteria
  - run-purpose-tag
deliverables:
  - handoff-package-with-1-page-briefing
  - meddpicc-slot-snapshot
  - conversation-history-transcript
  - pre-staged-objection-responses
  - acceptance-criteria-checklist
  - acceptance-or-rejection-tracking
  - handoff-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Handoff Protocol

Package and deliver an SAL-eligible lead from SDR to AE (or SDR to founder, or AE to CSM) with a complete briefing: 1-page founder briefing, MEDDPICC slot snapshot, full prior-conversation history, pre-staged objection responses, and explicit SAL acceptance criteria the receiving rep checks before accepting. Per SiriusDecisions / Forrester SAL norms: handoffs are explicit acceptance events, not silent assignments. Tracks acceptance / rejection / takeback in audit trail.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Silent handoffs are how deals die. SDR books a meeting, slips it into AE's calendar without context, AE walks in cold, deal stalls. This skill: produces an explicit handoff package that the receiving rep MUST formally accept (with checklist) or reject (with reason); rejections route back to the SDR for fixes; takebacks (deal returned post-acceptance) tracked separately. Goal: zero "I didn't know" moments at handoff + accountability tracking that improves SDR-AE alignment over time.

## When to Use

- "Esme positive reply + meeting booked — hand off to AE for the discovery call."
- "Tier-1 founder-led prospect ready for founder takeover."
- "Bulk handoff: 8 positive replies from this week's campaign."
- "AE rejected the handoff — reroute / fix / try again."
- "Deal closed-won — hand off to CSM for onboarding."
- Triggered by `pipeline-stages` advancing to Meeting / Discovery / Closed-Won.
- Post-`discovery-call-prep` when briefing is ready to deliver.

## Inputs Required

1. **SAL-eligible lead or opportunity** — from `lead-scoring` (SAL gate passed) OR `pipeline-stages` (advanced to handoff trigger stage).
2. **Receiving rep identity** — AE / founder / CSM, with their preferred briefing format + delivery channel.
3. **Prior cadence + reply history** — full conversation context (all Touches sent + all replies received).
4. **Meeting context** (when applicable) — booked meeting details from `discovery-call-prep`.
5. **Acceptance criteria** — SAL checklist or custom criteria the receiving rep evaluates.
6. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **Standard handoff package** | (1) 1-page briefing (from `discovery-call-prep`) · (2) MEDDPICC snapshot · (3) full conversation history · (4) pre-staged objections · (5) SAL acceptance checklist |
| **SAL acceptance criteria (SiriusDecisions / Forrester)** | SAL is rejected only for procedural / clerical / definitional reasons; otherwise accepted with 24–72h follow-up SLA. This skill defines the *definitional* threshold as: ICP fit confirmed + trigger present + within half-life + decision-maker / champion identified + no hard disqualifiers (anti-ICP firmographic, DNC, role-based email). |
| **Acceptance states** | `pending` (delivered, awaiting rep) → `accepted` / `rejected` (with reason) / `takeback` (rep returns deal post-acceptance) |
| **Rejection routing** | Back to SDR with rejection reason (e.g. "missing decision_process", "wrong segment for me") for fix-then-resubmit |
| **Takeback rule** | Allowed within 7 days post-acceptance; after 7d the receiving rep owns the deal |
| **Briefing freshness** | ≤24h at handoff (per `HANDOFF_FRESHNESS_HOURS=24`); else re-prep via `discovery-call-prep` |
| **Delivery channel** | Slack / email / dashboard alert — per receiving rep's preference |
| **Audit trail** | Every handoff event (delivered / accepted / rejected / takeback) logged for SDR-AE alignment KPIs |

## Procedure

### 1. Validate prerequisites
Confirm lead is SAL-eligible per `lead-scoring` OR pipeline stage triggers handoff. Receiving rep identity + delivery preference loaded.

### 2. Pull / refresh briefing
Pull current `discovery-call-prep` briefing for this lead. Check freshness (`HANDOFF_FRESHNESS_HOURS=24`). Stale → re-prep.

### 3. Assemble handoff package
- 1-page briefing (`discovery-call-prep` output).
- MEDDPICC slot snapshot (current state, populated + unknown).
- Full conversation history (all Touches sent + replies received in chronological order).
- Pre-staged objection responses (from `objection-handling-library`).
- SAL acceptance checklist (4 SiriusDecisions criteria + any custom).

### 4. Run SAL acceptance gates pre-delivery
Verify the 4 SAL criteria pass before delivery. If any fail (e.g., no champion identified), surface as a fix-needed-first issue and route back to SDR; do NOT deliver an unaccept-able handoff.

### 5. Deliver handoff via receiving rep's channel
Slack DM / email / dashboard alert per preference. Include: package + acceptance checklist + accept/reject buttons (or reply-keyword pattern).

### 6. Track acceptance state
Mark handoff `pending`. On rep response:
- **Accept** → handoff_state = `accepted`; deal owner transitions; PATCH deal/person.
- **Reject (with reason)** → handoff_state = `rejected`; route back to SDR with reason; SDR fixes + resubmits.
- **No response within 24h** → escalate (Slack ping, manager flag).

### 7. Handle takebacks
If receiving rep returns the deal within 7d post-acceptance: mark `takeback`; surface reason; route back to SDR for re-engage OR re-route to different AE. After 7d, takebacks not allowed without manager approval.

### 8. Push to CRM + emit handoff record
Per conventions: `interaction:handoff` with package + acceptance state + audit trail. PATCH deal record with new owner upon acceptance.

## Output Format

- Handoff package: 1-page briefing + MEDDPICC snapshot + conversation history + objections + SAL checklist
- Acceptance state per handoff (pending / accepted / rejected / takeback) with timestamp + rep identity
- Rejection reason (when applicable) + fix recommendation routed to SDR
- Takeback record (when applicable) within 7-day window
- Audit log entry per handoff event
- Run record: handoffs delivered, accept rate, reject rate, takeback rate, recommended next skill

## Done Criteria

1. SAL eligibility verified; briefing freshness checked (re-prep if >24h).
2. Handoff package assembled (5 components).
3. Pre-delivery SAL acceptance gates pass (or fix-first routed back to SDR).
4. Delivery via receiving rep's preferred channel.
5. Acceptance state tracked: pending → accepted / rejected (with reason) / takeback.
6. Rejection / takeback rerouted to SDR; deal owner PATCHed on acceptance.
7. Push to CRM emitted; audit log entry created.

## Pitfalls

- **Silent handoffs.** Calendar invite without briefing = AE walks in cold. Delivery + acceptance is the protocol.
- **Auto-accepting on rep silence.** No reply ≠ accept. Escalate, don't assume.
- **Stale briefings at handoff.** >24h → re-prep cheaply rather than deliver stale context.
- **No rejection reason captured.** "Rejected" without reason has no learning value; require reason at rejection.
- **Takeback >7d.** After 7d, the receiving rep has had material time; takebacks need manager approval.
- **Skipping pre-delivery SAL check.** Delivering a handoff that fails SAL criteria embarrasses the SDR and wastes AE time.
- **Multiple AEs assigned same deal.** Round-robin without dedup = AEs fight over leads. Single owner per deal.
- **CSM handoff treated like AE handoff.** Closed-Won → CSM is a different package (less sales context, more onboarding context); consider light-handoff variant.
- **Bulk handoffs without per-rep load check.** Handing 12 deals to one AE in a day overloads them; spread.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (recipient, company, briefing claims, MEDDPICC content, conversation history) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Briefing references actual prior touches + replies; never invent conversation context.
- **Not feeding rejection reasons to KPIs.** Rejection rate by SDR + by reason is gold for `kpi-reporting` SDR-coaching loops.

## Verification

Run is real when: every handoff has a delivery event + an acceptance event (within 24h or escalated); SAL pre-checks pass before delivery; rejection reasons captured; deal owner PATCHed only on accept; takeback events tracked. Negative test: pick 5 random handoffs; trace each from delivery → response → state. If any have unexplained "accepted" without rep response or "rejected" without reason, audit broke.

## Example

**User prompt:** "Esme positive reply + Tuesday discovery call booked — hand off to AE Jordan."
**What should happen:** Pull SAL eligibility (passes — Tier-1 score 87, trigger fresh, champion = Esme herself, no disqualifiers). Pull `discovery-call-prep` briefing for the Tuesday call (freshness 4h ✓). Assemble handoff package. Pre-delivery SAL check: 4/4 ✓. Deliver via Slack DM to Jordan with accept/reject buttons. Track pending → wait for response. Jordan responds "accept" within 30 min. Mark accepted; PATCH deal: owner=Jordan, handoff_at=now. Recommend `pipeline-stages` to advance Engaged → Meeting if not already; `discovery-call-prep` if Jordan needs personalized refresh.

**User prompt:** "AE rejected the Acme handoff — reason: 'missing decision_process slot'."
**What should happen:** Mark handoff_state=rejected; reason="missing decision_process". Route back to SDR with the specific gap. SDR's task: extract decision_process from the cadence/reply history OR schedule a brief discovery to elicit it. After fix, SDR re-submits the handoff. Track for SDR-coaching KPIs (which SDRs ship handoffs that get rejected, by reason).

**User prompt:** "Bulk handoff: 8 positive replies from this week's campaign."
**What should happen:** Per recipient: SAL eligibility check + briefing freshness check + receiving rep assignment (round-robin or per-segment). Per-rep load check: don't hand 8 to one AE; spread across the AE pool. Deliver via per-rep preferred channel. Track 8 pending → 8 acceptance states. Run summary: 8 delivered, 6 accepted (avg 23 min), 1 rejected (route back to SDR), 1 still pending after 24h (escalation).

## Linked Skills

- SAL eligibility check from → `lead-scoring`
- Briefing pull / refresh → `discovery-call-prep`
- Stage transition triggers handoff → `pipeline-stages`
- Pre-staged objection responses → `objection-handling-library`
- Post-acceptance: AE owns → `pipeline-stages` for Discovery / Proposal advance
- Conversation history feeds → `conversation-intelligence`
- Acceptance / rejection KPIs → `kpi-reporting` (function-6)
- Closed-Won → CSM handoff (light-handoff variant; out-of-scope downstream)

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-5-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Handoff event (delivered / accepted / rejected / takeback) | `interaction` (type: `handoff`) | `relevance` = state + receiving rep + acceptance criteria result + reason if rejected/takeback; `tags: "#handoff #handoff-<state> #function-5"` |
| Handoff package (briefing + MEDDPICC + history + objections) | `interaction` (type: `research`) | `relevance` = full package or pointer to component artifacts; `tags: "#handoff-package #function-5"` |
| Deal owner change on acceptance | `deal` (PATCH) | `owner_rep_id`, `handoff_accepted_at`, `prior_owner_rep_id`, `handoff_count` incremented |
| Rejection reason routed to SDR | `interaction` (type: `research`) | `relevance` = rejection reason + fix recommendation + back-to-SDR flag; `tags: "#handoff-rejected #sdr-fix-needed #function-5"` |
| Run record (bulk handoff summary) | `interaction` (type: `research`) | `relevance` = handoff counts + per-rep load + acceptance distribution; `tags: "#handoff-protocol-run #function-5"` |
| `[unverified — needs check]` | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #handoff-protocol"`; deal PATCH deferred |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
HANDOFF_FRESHNESS_HOURS=24
```

### Source tag

`source: "skill:handoff-protocol:v2.0.0"`

### Example push (handoff accepted)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#handoff #handoff-accepted #function-5",
    "relevance": "Handoff for esme@stitchbox.com from SDR Will → AE Jordan. Delivered 2026-05-30T09:14 PT via Slack. SAL pre-check: 4/4 ✓ (ICP fit Tier-1 87 / trigger fresh VP CX hire 43d / champion Esme herself / no disqualifiers). Briefing freshness: 4h ✓. Jordan accepted 2026-05-30T09:42 PT (28 min). Deal owner transitioned. Recommended next: discovery-call-prep refresh for Jordan if needed; pipeline-stages already at Meeting.",
    "source": "skill:handoff-protocol:v2.0.0"
  }'
```

### Example push (handoff rejected)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#handoff #handoff-rejected #sdr-fix-needed #function-5",
    "relevance": "Handoff for marcus@acme.com REJECTED by AE Sarah. Rejection reason: \"missing decision_process slot — can't accept without knowing how Acme buys\". Routed back to SDR for fix. SDR task: extract decision_process from cadence/reply history OR schedule a brief discovery call. Track for SDR-coaching KPI (Sarah's rejection rate by reason).",
    "source": "skill:handoff-protocol:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[verified: <source>]` (briefing + handoff event tracked) or `[user-provided]` (rep response) | Standard mapping. |
| `[unverified — needs check]` (briefing references unverified context, or acceptance state ambiguous) | Pushes ONLY as `interaction:research` with `#unverified #review-required #handoff-protocol` tags; deal PATCH deferred. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- SAL pre-check fails (handoff not deliverable) → push the fix-needed flag, NOT a delivered handoff.
- Briefing too stale and re-prep failed → push `#handoff-blocked-stale-briefing` flag.
- Bulk handoff produced 0 deliverable handoffs (all blocked) → push run record with `#all-blocked`; no per-handoff records.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
