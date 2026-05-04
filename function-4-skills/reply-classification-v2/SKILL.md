---
name: reply-classification
description: Classify every inbound reply (email / LinkedIn / SMS / call disposition) into a routing label — `positive` / `not-now` / `not-interested` / `wrong-person` / `unsubscribe` / `out-of-office` / `referral` / `question` / `unclear` — with explicit confidence score, then dispatch to the next skill (`objection-handling-library`, `discovery-call-prep`, `follow-up-management`, or manual review). Use when an active campaign starts generating replies, when bulk reply triage is needed for a sales rep / founder inbox, or when classification confidence below the threshold needs human review.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, conversation-management, reply-triage, classification, function-4]
related_skills:
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - multi-channel-cadence
  - campaign-management
  - objection-handling-library
  - discovery-call-prep
  - follow-up-management
  - pipeline-stages
inputs_required:
  - inbound-reply-text-or-disposition
  - prior-cadence-context
  - lead-record
  - classification-confidence-floor
  - run-purpose-tag
deliverables:
  - per-reply-classification-with-confidence
  - routing-recommendation-per-reply
  - manual-review-queue-for-low-confidence
  - cadence-exit-trigger-on-applicable-replies
  - reply-classification-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Reply Classification

Classify each inbound reply (email body, LinkedIn message, SMS, call disposition) into one of nine standard routing labels with an explicit confidence score, then dispatch to the right downstream skill. Hard rule: classifications below the confidence floor (default 0.75) route to manual review rather than auto-acting. Owns the cadence-exit trigger when reply class warrants exit.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over) as the seller; procedure is vertical-agnostic. function-4 worked examples chain — same WorkflowDoc cadence whose touches function-3 sent now generates replies this skill triages.*

## Purpose

Sales teams without classification triage all inbound the same way (founder reads each, decides each). That works at 5 replies/week and breaks at 50. This skill: reads reply text + cadence context, classifies into a 9-label taxonomy, attaches confidence, dispatches to the right skill (`objection-handling-library` / `discovery-call-prep` / `follow-up-management`), and routes low-confidence to manual review. Goal: founder reads only what needs founder judgment; everything else routes deterministically.

## When to Use

- "Triage today's 30 replies — sort into hot / warm / not-now / dead."
- "We have 200 replies from a campaign — categorize and route."
- "Founder inbox is full — classify what needs human attention."
- "Reply just came in — is this a meeting request or a polite no?"
- Active campaigns generating reply volume.
- Pre-discovery-call-prep — confirm `positive` classification before prepping.

## Inputs Required

1. **Inbound reply** — email body / LI message text / SMS / call disposition string. Include reply timestamp + sender identity.
2. **Prior cadence context** — which Touch this is replying to, which campaign, recipient's `lead_id`.
3. **Lead record** — score, tier, signals, prior reply history (if any).
4. **Confidence floor** — default `REPLY_CLASSIFICATION_CONFIDENCE_FLOOR=0.75`; below routes to manual review.
5. **Run purpose tag** — short string for batch attribution.

## Quick Reference

| Concept | Value |
|---|---|
| **9-label taxonomy** | `positive` / `not-now` / `not-interested` / `wrong-person` / `unsubscribe` / `out-of-office` / `referral` / `question` / `unclear` |
| **Confidence floor** | 0.75 default; below routes to manual review (never auto-act on uncertain) |
| **Cadence-exit triggers** | `positive` (handoff) / `not-interested` (12mo cooldown) / `unsubscribe` (forever) / `wrong-person` (re-enrich) |
| **Cadence-continue but pause-touch** | `not-now` (resume per stated date) / `out-of-office` (resume after OOO date) / `question` (handle then continue) |
| **Routing** | `positive` → `discovery-call-prep`; `not-now`/`question` → `objection-handling-library` (if objection embedded); `referral` → `data-enrichment` (find new contact); `unsubscribe` → unsub-honor + global exit |
| **Reply latency target** | Classify within 1h of reply receipt; founder-attention SLAs depend on it |
| **Multi-language** | Classify in source language; capture verbatim; translate one-sentence summary for English-only operators |
| **Apple-MPP / iOS Mail Privacy** | Auto-replies (OOO, vacation) recognized via header signals + body patterns; tagged `out-of-office` not `not-interested` |

## Procedure

### 1. Ingest reply
Read reply text + headers + cadence context. Detect channel (email / LI / SMS / call disposition). Identify sender, timestamp, parent Touch.

### 2. Pre-classify on hard signals
Auto-reply detection (header `Auto-Submitted`, body patterns): → `out-of-office`. Unsubscribe phrases ("remove me", "unsubscribe"): → `unsubscribe` with high confidence. Bounce auto-reply: → `bounce` (route back to channel skill, NOT a Touch reply).

### 3. LLM-backed classification (when not pre-classified)
Pass reply text + 1-line cadence context to LLM. Required output: `{label, confidence: 0–1, rationale: 1 sentence, embedded_objection: <text or null>}`. Prompt is deterministic — same reply produces same classification (modulo LLM nondeterminism, which seeds use mitigates).

### 4. Confidence gate
- Confidence ≥ floor (0.75): proceed with classification.
- Confidence < floor: route to manual review queue with the reply + LLM's best guess + rationale; do NOT auto-act.

### 5. Cadence-state effects
- `positive` / `not-interested` / `unsubscribe` → exit cadence on this recipient.
- `not-now` → pause cadence; resume at date parsed from reply (or 90d if unspecified).
- `wrong-person` → exit cadence; flag for `data-enrichment` correction.
- `out-of-office` → pause; resume after OOO end date.
- `question` / `referral` → cadence continues; route reply to handler.
- `unclear` → cadence continues; manual review.

### 6. Dispatch to next skill
- `positive` + meeting requested → `discovery-call-prep` (with reply context).
- `not-now` / `not-interested` with embedded objection → `objection-handling-library`.
- `referral` → `data-enrichment` to find the named contact.
- `question` → `objection-handling-library` (treats Q as light objection).
- `out-of-office` / `unsubscribe` → no handler (cadence state change is the action).

### 7. Push to CRM + emit run summary
Per conventions: per-reply `interaction:reply` with classification + confidence + rationale + dispatched-to. PATCH person record with reply state. Run summary: total replies, label distribution, confidence distribution, manual-review count, dispatched-to counts.

## Output Format

- Per-reply classification: label + confidence + rationale + embedded objection (if any) + dispatched-to-skill
- Manual review queue: low-confidence replies with LLM's best guess + rationale (for human override)
- Cadence-state-change log: per-recipient cadence exits / pauses with reason
- Run record: reply volume, label distribution, confidence histogram, dispatched-to summary, manual-review count
- Recommended next skill per dispatched reply

## Done Criteria

1. Every inbound reply classified or routed to manual review (no silent drops).
2. Confidence floor honored — no auto-act on `confidence < 0.75`.
3. Pre-classification rules (auto-reply, unsubscribe phrase, bounce) applied before LLM call.
4. Cadence-state effects propagated (exit / pause / continue) per label.
5. Dispatch to downstream skill happened for applicable labels with full context.
6. Push to CRM emitted: per-reply interaction + person PATCH + run record.
7. Manual review queue surfaced to user.

## Pitfalls

- **Auto-acting on low-confidence classifications.** "Looks like not-interested but I'm 60% sure" → manual review, never auto-exit cadence.
- **Confusing OOO with not-interested.** Auto-replies have header signals — pre-classify before LLM.
- **Missing embedded objections.** "Not now, we're already using X" is BOTH `not-now` AND a competitor objection — both flagged.
- **Treating bounces as replies.** Bounces are channel-skill concerns; route back, don't classify as reply.
- **Single-language assumption.** Multi-language reply needs source-language classification + English summary; never silently translate body.
- **Ignoring cadence context.** "Yes, that works" means different things at touch 1 (positive interest) vs touch 5 (already-engaged confirmation); context matters.
- **Auto-honoring unsubscribe only on the channel that received it.** Unsubscribe is a global signal — exit ALL channels for that recipient (courteous + GDPR-aligned even where not legally required).
- **Skipping manual review on edge cases.** Sarcasm, questions-that-look-like-objections, half-replies that trail off — when in doubt, route to human.
- **Not handling referrals as a referral.** "I'm not the right person, talk to Marcus" should trigger `data-enrichment` for Marcus, not just exit on the original recipient.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (recipients, companies, dates, embedded objection text, classification rationale) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Reply text itself is `[user-provided]` (came from a real human); classification is `[verified: llm-classifier:run_<id>]` with confidence; never invent reply content.
- **Classification drift across runs.** Same reply should produce the same label; if LLM nondeterminism is creating drift, lock seed or batch-classify.

## Verification

Run is real when: every reply has a classification record OR a manual-review queue entry; no `confidence < 0.75` was auto-acted on; cadence states updated correctly per label (sample-check 5 random); unsubscribe replies trigger global cross-channel exit; LLM rationale resolves to actual reply content (not invented).

## Example

**User prompt:** "30 replies came in overnight from our WorkflowDoc Tier-1 cadence. Triage them."
**What should happen:** Pre-classify (3 OOO via header, 2 unsubscribe phrases, 1 bounce → routed to channel skill). LLM-classify the remaining 24. Distribution: 4 positive (→ discovery-call-prep), 6 not-now (4 with embedded objection → objection-handling-library; 2 pure timing → follow-up-management), 5 not-interested (cadence exit), 2 referral (→ data-enrichment for the named alternative contact), 4 question (→ objection-handling-library), 3 unclear (manual review). Confidence: 27 ≥0.75; 3 below floor → manual review. Cadence states updated; person records patched. 7 dispatched to next skills.

**User prompt:** "This reply came in: 'Thanks but we're already using Guru, please remove me.'"
**What should happen:** Pre-classify catches "remove me" → `unsubscribe` with confidence 0.95 (regex-strong match). Cadence exits globally for this recipient on all channels. LLM also notes embedded competitor mention (Guru) — capture as `[verified: reply-text]` competitor signal for `competitive-intelligence` (function-1) feed. No further outreach forever per global unsubscribe respect. Push: `interaction:reply` with classification + competitor-signal sub-record.

**User prompt:** "Reply: 'Sounds interesting but I'm out till March 15. Ping me then.'"
**What should happen:** LLM classifies as `not-now` with confidence 0.92, rationale: "expressed interest, named specific resume date." Parsed resume date: 2026-03-15. Cadence pauses; resume scheduled for 2026-03-16 (day after stated date). Person record: `next_followup_at: 2026-03-16`, `last_reply_class: not-now-with-date`. Routed to `follow-up-management` to schedule the resume touch.

## Linked Skills

- `positive` reply with meeting request → `discovery-call-prep`
- `not-now` / `not-interested` with embedded objection → `objection-handling-library`
- `not-now` pure timing or `out-of-office` → `follow-up-management`
- `referral` → `data-enrichment` (find the named contact)
- `wrong-person` → `data-enrichment` (correct existing record)
- `unsubscribe` → global cross-channel exit; no handler skill
- Low-confidence (<0.75) → manual review queue
- Active campaign generating replies → `campaign-management` (feeds reply-rate metric)
- Pipeline stage advance triggered by `positive` → `pipeline-stages`

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-4-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-reply classification | `interaction` (type: `reply`) | `relevance` = label + confidence + rationale + embedded objection + dispatched-to-skill; `tags: "#reply #class-<label> #function-4"` |
| Cadence-state change (exit / pause / continue) | `person` (PATCH via dedup key) | `last_reply_class`, `last_reply_at`, `cadence_state: exited | paused | active`, `next_followup_at` if applicable |
| Manual review queue entry | `interaction` (type: `research`) | `relevance` = reply + LLM's best guess + rationale + confidence; `tags: "#manual-review #reply-classification #function-4"` |
| Run record (batch classification summary) | `interaction` (type: `research`) | `relevance` = label distribution + confidence histogram + dispatched counts; `tags: "#reply-classification-run #function-4"` |
| Embedded competitor / objection signal | `interaction` (type: `research`) | `relevance` = signal text + classification + parent reply id; `tags: "#competitor-signal #function-4"` (feeds `competitive-intelligence`) |
| `[unverified — needs check]` (low confidence) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #reply-classification"`; person PATCH deferred |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
ANTHROPIC_API_KEY=     # or OPENAI_API_KEY
REPLY_CLASSIFICATION_CONFIDENCE_FLOOR=0.75
```

### Source tag

`source: "skill:reply-classification:v2.0.0"`

### Example push (positive reply)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#reply #class-positive #function-4 #cadence-exit",
    "relevance": "Reply classified positive at 2026-05-29T08:14 with confidence 0.94. Reply text: \"Yes, this lands at the right time — open to a 15-min call next Tuesday afternoon.\" Rationale: explicit interest + meeting time proposed. Cadence exited; dispatched to discovery-call-prep with proposed time 2026-06-02 PM PT. Parent Touch: tch_2026-05-22_email_001.",
    "source": "skill:reply-classification:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#reply-classification-run #function-4",
    "relevance": "Reply classification batch 2026-05-29_morning. 30 replies received. Pre-classified: 3 OOO / 2 unsubscribe / 1 bounce. LLM-classified 24: 4 positive / 6 not-now / 5 not-interested / 2 referral / 4 question / 3 unclear. Confidence: 27 ≥0.75 / 3 to manual review. Dispatched: 4 → discovery-call-prep / 4 → objection-handling-library (embedded objections) / 2 → follow-up-management / 2 → data-enrichment (referrals). Cadence states: 9 exited / 4 paused / 17 active.",
    "source": "skill:reply-classification:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (reply text from real human) + `[verified: llm-classifier:run_<id>]` (classification) | Standard mapping. |
| `[unverified — needs check]` (confidence <0.75) | Pushes ONLY as `interaction:research` with `#unverified #review-required #reply-classification` tags. Person PATCH deferred until manual review confirms. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Reply already classified within 1h (dedup) — push the dedup record only.
- Bounce auto-reply — route to channel skill; not a reply event for this skill.
- Drafts of LLM responses (not the user's actual reply) — never push.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
