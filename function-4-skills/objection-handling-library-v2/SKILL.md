---
name: objection-handling-library
description: Match an embedded objection (from a `not-now` / `not-interested` / `question` reply) to a 12-objection canonical library, produce 2–3 response variants ranked by fit, and recommend a cadence-state action (resume / nurture / exit). Uses Feel-Felt-Found framing (traditional sales technique; origin commonly traced to Procter & Gamble training, 1980s), BANT-loss-reason taxonomy, and Bosworth pain-questioning to re-discover. Use when `reply-classification` flags an embedded objection, when a no-now needs a graceful response, when objection patterns recur and need codified responses, or when sales reps need pre-approved objection templates.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, conversation-management, objection-handling, function-4]
related_skills:
  - reply-classification
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - discovery-call-prep
  - follow-up-management
  - icp-definition
  - positioning-strategy
  - competitive-intelligence
inputs_required:
  - classified-reply-with-embedded-objection
  - prior-cadence-and-touch-context
  - lead-record
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - run-purpose-tag
deliverables:
  - objection-classification-against-12-library-categories
  - 2-to-3-response-variants-ranked-by-fit
  - cadence-state-action-recommendation
  - new-objection-flag-when-not-in-library
  - objection-handling-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Objection Handling Library

Match an embedded objection to a 12-objection canonical library, produce 2–3 response variants per objection ranked by fit, and recommend a cadence-state action. Uses Feel-Felt-Found framing for empathy, BANT-loss-reason taxonomy for categorization, and Bosworth pain-questioning patterns when re-discovery is the right move. Hard rule: when the objection doesn't match any library entry with confidence ≥0.7, flag as `new-objection-pattern` and route to manual response — never invent a library entry on the fly.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Objections recur. The same 12 patterns ("we're already using X", "no budget", "send me an email", "wrong time", "happy with current solution", etc.) cover 80%+ of outbound objections. This skill: matches the incoming objection to the library, produces 2–3 ranked response variants from pre-approved templates (each tied to a framework — Feel-Felt-Found / re-discovery / time-shift), and recommends what happens to the cadence (resume / pause / nurture / exit). Founders + reps stop reinventing responses; the library improves over time as new patterns surface and get codified.

## When to Use

- "We got 'we're already using Guru' — give me the response."
- "Reply has objection — generate response variants."
- "Build out our objection library for new product line."
- "Triage today's `not-now` replies — match objections, suggest responses."
- "Sales rep needs pre-approved templates for 12 common objections."
- Post-`reply-classification` when embedded objection flagged.
- Library refresh after 30+ new objections collected.

## Inputs Required

1. **Classified reply with embedded objection** from `reply-classification`. Reply text + objection text + classification confidence.
2. **Prior cadence + Touch context** — which campaign, position, channel, hook used.
3. **Lead record** — score, tier, signals, prior reply history.
4. **ICP P-T-O chain** from `icp-definition` — pain anchors for re-discovery responses.
5. **Positioning message house** from `positioning-strategy` — counter-positioning language for competitor objections.
6. **Run purpose tag**.

## Quick Reference

| Concept | Value |
|---|---|
| **12-objection library** | (1) already using competitor / (2) no budget / (3) no authority / (4) no need now / (5) bad timing / (6) happy with status quo / (7) tried similar before failed / (8) too expensive / (9) too small (we're not a fit) / (10) send me email / (11) wrong person / (12) compliance/security blocker |
| **Match confidence floor** | ≥0.7 to use library response; below = `new-objection-pattern` flag |
| **Response framework — Feel-Felt-Found** | Traditional sales technique; origin commonly traced to Procter & Gamble training (1980s) — no canonical author. Acknowledge emotion ("I hear you") → reference others ("others felt the same") → resolve with insight ("what they found was…"). Used when pure empathy + reframe is right. |
| **Response framework — Re-discovery** | Bosworth pain-questioning. Surface the pain underneath the objection. Used when the stated objection isn't the real reason. |
| **Response framework — Time-shift** | Acknowledge timing; lock specific resume window with permission. Used for `bad-timing` and `not-now`. |
| **Response framework — Counter-position** | April Dunford. When objection cites a competitor, reframe the alternative (not the product). Used for `already using competitor`. |
| **Variants per objection** | 2–3 (light / medium / direct tone). Sales rep picks per relationship. |
| **Cadence-state actions** | Resume per stated date / nurture-90d / nurture-12mo / exit-permanent (per `not-interested` reply class) |
| **New-objection-pattern flag** | When ≥3 unmatched objections accumulate, route to library refresh |

## Procedure

### 1. Validate inputs
Read classified reply + cadence context + lead record. Confirm reply has embedded objection (per `reply-classification` flag). If no objection, recommend `follow-up-management` instead.

### 2. Match objection against 12-library
LLM-backed match with confidence score per library entry. Output: `{best_match_label, confidence, second_best_label, second_confidence}`. Surface secondary match when within 0.15 confidence of primary.

### 3. Confidence gate
- ≥0.7: use library response framework.
- <0.7: flag `new-objection-pattern`; route to manual response; collect for library refresh.

### 4. Generate 2–3 response variants per matched objection
Pick framework per the matched library entry (Feel-Felt-Found / re-discovery / time-shift / counter-position). Generate light, medium, direct tone variants per the framework. Each variant ≤80 words; one CTA; respects channel-isolation per conventions §10 of function-3.

Variants reference:
- Verified prior context (hook from `data-enrichment`, prior Touch content) — never invent.
- Positioning message house (for counter-positioning).
- ICP P-T-O language (for re-discovery).

### 5. Recommend cadence-state action
- `bad timing` → resume per stated date or default 60d.
- `already using competitor` → respond + nurture-90d (competitor switch is rare in <90d window).
- `no budget` → nurture-90d AND flag for `lead-scoring` re-tier (BANT update).
- `wrong person` → exit on this recipient + route to `data-enrichment` for correct contact.
- `compliance/security blocker` → respond + flag for `discovery-call-prep` (security-prep mode) if interest follows.
- `tried similar before failed` → re-discovery framework; capture what failed for `competitive-intelligence`.
- `not-interested` (definitive) → exit-permanent (12mo cooldown).

### 6. Capture intel for downstream
Competitor mentions → push to `competitive-intelligence` (function-1 feeds).
Pricing pushback → flag for `revenue-forecasting` ACV reality-check.
Persistent pain pattern → flag for `icp-refinement-loop` (function-6).

### 7. Push to CRM + emit run record
Per conventions: per-objection `interaction:reply-response` with library match + variants + cadence action. PATCH person record with new state (paused / nurture / exited).

## Output Format

- Per-objection: matched library entry + confidence + second-best (when close) + 2–3 ranked response variants
- Cadence-state action recommendation with rationale
- New-objection-pattern flag when no library match ≥0.7
- Captured intel: competitor mentions, pricing signals, persistent pain — routed to downstream skills
- Run record: total objections processed, library-match distribution, new-pattern count

## Done Criteria

1. Embedded objection identified per input (or `follow-up-management` recommended if absent).
2. Library match attempted; confidence scored; new-pattern flag if <0.7.
3. 2–3 response variants generated per matched objection; framework attribution per variant.
4. Cadence-state action recommended per objection class.
5. Intel captured + routed to relevant downstream skills (competitive-intelligence, lead-scoring, etc.).
6. Push to CRM emitted: per-objection interaction + person PATCH.

## Pitfalls

- **Inventing library entries on the fly.** When the objection doesn't match, surface as new-pattern; don't synthesize a "library response" without library backing.
- **Generic "I understand" responses.** Feel-Felt-Found requires specifics — *whose* feeling, *whose* found-what.
- **Counter-positioning by attacking the competitor.** Reframe the *alternative* (DIY / status-quo / build-vs-buy), not "competitor X is bad" — that reads desperate.
- **Re-discovery on a clean `not-interested`.** When the prospect is clearly out, re-discovery feels like badgering. Honor the no.
- **Auto-acting without rep approval on Tier-1 prospects.** High-value prospects warrant human-in-loop on the response choice.
- **Ignoring channel-isolation.** Don't reference the channel the objection came in on within the response on a different channel.
- **Skipping intel capture.** Competitor mentions are gold for `competitive-intelligence`; pricing pushback is signal for `revenue-forecasting`; persistent objections are inputs for `icp-refinement-loop`.
- **Treating "send me email" as not-interested.** It's often a polite redirect, sometimes a real interest — confidence-aware response with explicit ask.
- **Multi-objection replies handled as one.** "No budget AND we're already using X" → match both; respond to the more-removable one first.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (recipients, companies, competitors mentioned, prior touches referenced, dates) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Response variants reference verified prior context (hook from data-enrichment, prior Touch content); never invent customer outcomes or "as I mentioned in our last call" without backing.
- **Library drift.** When new patterns accumulate (≥3 unmatched in a week), schedule library refresh; don't let the new-pattern queue grow stale.

## Verification

Run is real when: every objection has a library-match record OR new-pattern flag; response variants reference only verified context (no invented quotes / outcomes / dates); cadence-state action propagated to person record; intel routed to downstream skills (sample-check on competitor / pricing mentions). Negative test: read 5 random response variants — does each sound like a real human's response, grounded in actual prior context? If any feel template-stamped, framework grounding broke.

## Example

**User prompt:** "Reply: 'Thanks but we're already using Guru and pretty happy with it.' Match + respond."
**What should happen:** Library match: `already using competitor` (Guru) with confidence 0.92. Framework: counter-position. 3 variants generated:
- Light: acknowledge Guru, ask one curiosity question about a specific pain Guru-users typically hit (per ICP P-T-O); soft CTA.
- Medium: reframe the alternative (Guru optimizes for X; WorkflowDoc users mentioned Y as the gap); offer 5-min comparison brief.
- Direct: ask explicitly what would need to be true for them to look at alternatives in 6–9mo; respect "no" if firm.

Cadence action: nurture-90d (competitor switches rarely happen sooner). Intel captured: Guru mention pushed to `competitive-intelligence` with date + reply context.

**User prompt:** "Reply: 'Interesting but we're locked in until Q1 2027.' Match."
**What should happen:** Library match: `bad timing` with explicit date, confidence 0.95. Framework: time-shift. 2 variants:
- Light: acknowledge timing; propose Q4 2026 prep call (90d before contract end); permission ask.
- Direct: lock the Q1 2027 resume; confirm the right contact + decision-maker won't change.

Cadence action: pause; resume scheduled for 2026-12-15 (60 days before stated 2027-Q1). Routed to `follow-up-management`.

**User prompt:** "Reply: 'I appreciate the outreach but I'm questioning the ROI honestly — your case studies look thin.'"
**What should happen:** Match attempt: best `tried similar before failed` (confidence 0.55), second `too expensive` (0.42). Both below floor → flag `new-objection-pattern` (specific objection: "ROI/case-study credibility"). Route to manual response. Capture for library refresh — if 2+ similar replies arrive in next 30d, propose a 13th library entry: "ROI / proof-thin objection."

## Linked Skills

- Embedded objection from reply → upstream `reply-classification`
- Competitor mention captured → `competitive-intelligence` (function-1, signal feed)
- Pricing pushback captured → `revenue-forecasting` (ACV reality-check)
- Persistent unmatched pattern → library refresh + `icp-refinement-loop`
- Wrong-person objection → `data-enrichment` (find correct contact)
- Resume scheduled → `follow-up-management`
- Compliance/security objection with interest → `discovery-call-prep` (security-prep mode)
- Library entry for `lead-scoring` re-tier (no-budget signals) → `lead-scoring`

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-4-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-objection: library match + variants + cadence action | `interaction` (type: `reply-response`) | `relevance` = matched-label + confidence + variants (3 max) + framework + cadence action; `tags: "#objection-handling #obj-<library-label> #function-4"` |
| Cadence-state change | `person` (PATCH via dedup key) | `cadence_state`, `next_followup_at`, `last_objection_class`, tags updated |
| Competitor mention captured | `interaction` (type: `research`) | `relevance` = competitor name + reply context + parent reply id; `tags: "#competitor-signal #function-4"` (feeds `competitive-intelligence`) |
| New-objection-pattern flag | `interaction` (type: `research`) | `relevance` = unmatched objection text + best-match attempts + confidences; `tags: "#new-objection-pattern #manual-review #function-4"` |
| Run record | `interaction` (type: `research`) | `relevance` = total objections + library-match distribution + new-pattern count; `tags: "#objection-handling-run #function-4"` |
| `[unverified — needs check]` | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #objection-handling"`; person PATCH deferred |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
ANTHROPIC_API_KEY=     # or OPENAI_API_KEY (for library-match LLM)
```

### Source tag

`source: "skill:objection-handling-library:v2.0.0"`

### Example push (matched objection)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#objection-handling #obj-already-using-competitor #function-4",
    "relevance": "Objection matched: already-using-competitor (Guru) with confidence 0.92. Parent reply: rpl_2026-05-29_h7k. Framework: counter-position (Dunford). 3 variants generated: light (curiosity-question on Guru-user pain), medium (reframe alternative + 5-min brief CTA), direct (explicit timing-of-evaluation ask). Cadence action: nurture-90d. Intel: Guru mention pushed to competitive-intelligence.",
    "source": "skill:objection-handling-library:v2.0.0"
  }'
```

### Example push (new-pattern flag)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#new-objection-pattern #manual-review #function-4",
    "relevance": "Unmatched objection: \"questioning the ROI honestly — your case studies look thin\". Best matches: tried-similar-before-failed (0.55) / too-expensive (0.42). Both below 0.7 floor. Routed to manual response. Pattern accumulator: 1/3 needed for library refresh. Possible new entry: 'ROI/proof-thin objection.'",
    "source": "skill:objection-handling-library:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (objection text from real reply) + `[verified: llm-match:run_<id>]` (library match) | Standard mapping. |
| `[unverified — needs check]` (match <0.7 OR variant references unverified context) | Pushes ONLY as `interaction:research` with `#unverified #review-required #objection-handling` tags. Cadence action deferred. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- No embedded objection in reply (route to `follow-up-management` instead).
- New-pattern accumulator triggered → push the flag, not response variants.
- Variants drafted but rejected by user → local artifact; do not push as `reply-response`.
- `[unverified]` → see provenance routing.
- `[hypothetical]` — never.
