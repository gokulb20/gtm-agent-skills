---
name: multi-channel-cadence
description: Compose 5–9 touches across email + LinkedIn + cold call into a single 14–21 day cadence — calling `cold-email-sequence`, `linkedin-outreach`, and `cold-calling` for channel-specific copy/scripts, then orchestrating per-recipient sequencing with channel-isolation rules, capacity-cap respect across channels, branch logic on early replies, and exit conditions. Use when a Tier-1 cadence needs more than email alone, when channels are complementary (email lands → LI connection → call), when reply rate on email-only or LI-only has plateaued, or when account-based plays require coordinated multi-thread coverage.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, cadence, multi-channel, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - email-infrastructure-setup
  - cold-email-sequence
  - linkedin-outreach
  - cold-calling
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - active-channel-skills-ready-flags
  - sender-pool-and-rep-pool
  - run-purpose-tag
  - cadence-template-or-default
deliverables:
  - 5-to-9-touch-multi-channel-cadence
  - per-channel-touch-handoffs-to-channel-skills
  - cadence-config-conforming-to-conventions-2-2
  - cross-channel-capacity-plan
  - branch-and-exit-rules
  - cadence-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Multi-Channel Cadence

Compose a 5–9 touch cadence across email + LinkedIn + cold call channels, calling each channel-specific skill for the actual copy/scripts and orchestrating per-recipient sequencing. Owns cross-channel rules: channel-isolation, per-day spacing, capacity-cap aggregation, branch logic on early replies, exit conditions. Output is a Cadence record + dispatched per-channel Touch handoffs.

> *Worked example uses WorkflowDoc (fictional, function-1 carry-over) as the seller; procedure is vertical-agnostic. Shared rules in `function-3-skills/function-3-conventions.md`.*

## Purpose

Single-channel cadences ceiling out at the channel's max response rate. Multi-channel (email + LI + call layered) lifts response rate 30–60% over best single channel. But composition is hard: same-day double-touches read as harassment; channel-isolation matters; capacity caps are per-channel and must aggregate; branch logic on replies must exit the right cadence on the right channel. This skill orchestrates without writing copy itself — calls the three channel skills and arranges them.

## When to Use

- "Build a full multi-channel cadence for our Tier-1 list."
- "Email reply rate plateaued at 2.5% — add LinkedIn and call legs."
- "Account-based campaign — reach 3 contacts per company across all channels."
- "I want a cadence template I can re-use."
- "Compose email touches 1 + 2 + 4, LinkedIn connect at touch 3, cold call at touch 5."
- Pre-launch when single-channel reply rate isn't enough.
- Tier-1 plays where channel diversity reduces dependency on any one signal.

## Inputs Required

1. **Scored + enriched Lead list** from `lead-scoring`.
2. **ICP P-T-O chain** + **positioning message house** (passed through to channel skills).
3. **Channel skills' ready flags** — email (infrastructure ready), LinkedIn (account safety + URL coverage), call (phone + DNC).
4. **Sender pool + rep pool** from `email-infrastructure-setup` + dialer config.
5. **Run purpose tag**.
6. **Cadence template** (optional; default `email-li-call-7touch-21d`).

## Quick Reference

| Concept | Value |
|---|---|
| **Default template** | `email-li-call-7touch-21d` (7 touches over 21 days, E + LI-connect + E + Call + E + LI-msg + E-breakup) |
| **Template library** | email-only / email+LI / email+LI+call / tier-1-9touch / abm-3thread / email-fatigue-relief / gdpr-light |
| **Channel-isolation rule** | Don't reference one channel's content in another's body. "As I emailed you" = forbidden. |
| **Per-day spacing** | Max 1 touch per recipient per day; exception: email + LI-connect on D+0 |
| **Capacity aggregation** | Per-channel caps respected: email 30/day/mailbox, LI 80/week, call 80/rep/day |
| **Multi-channel reply target** | ≥6% by D+10 (vs ~3% email-only floor) |
| **Branch rules** | li-connect-accepted → swap next email to LI-message; email-bounce → drop email touches keep others |
| **Exit conditions** | reply-positive, reply-negative, bounce, unsubscribed, manual-stop, cap-hit |
| **Re-touch rule** | No record touched in any channel within 90 days (per conventions §7) |
| **GDPR (EU/UK)** | Auto-swap to `gdpr-light-4touch-21d` template |
| **Account-based plays** | Stagger across reps to avoid same-account same-week pile-up |

## Procedure

### 1. Validate prerequisites
Read scored Leads; check channel skills' ready flags; load ICP P-T-O + message house. Block only if zero channels ready.

### 2. Determine mode (per channel)
Each channel inherits its own mode (API / manual / BYO). Cadence record carries per-channel mode metadata.

### 3. Pick or compose cadence template
User-supplied OR default `email-li-call-7touch-21d`. Adapt per recipient if a channel is unavailable for that recipient (no LI URL → swap LI touch for email).

### 4. Filter recipient list (cross-channel)
Drop records that fail every channel's gate; apply tier filter; apply re-touch rules (90d any-channel cooldown); auto-swap to `gdpr-light` for EU/UK.

### 5. Pre-flight: cross-channel capacity check
Compute per-channel touches needed; compare to per-channel caps × pool × duration. Surface to user if any channel over-capacity.

### 6. Dispatch to channel skills
For each touch position, call channel skill's `prepare()` with lead + position + sender + branch context. Each channel skill returns Touch[draft] with own provenance.

### 7. Validate cross-channel rules
Per-day spacing; channel-isolation (no body cross-references); quiet hours (per channel); capacity-cap distribution.

### 8. Build Cadence + Campaign records
Per conventions §2.2 / §2.3. Branch rules (li-connect-accepted, email-bounce) and exit conditions explicit.

### 9. Push to CRM + run summary
Cadence + Campaign as `interaction:research`; per-touch records pushed by their channel skills. Run summary: template, eligible-recipient count, per-channel headroom, per-recipient variants. Recommend `campaign-management`.

## Output Format

- 5–9 touch cadence config per conventions §2.2 (template instance + branch rules + exit conditions)
- Per-recipient touch list with channel + day_offset + framework + scheduled_for
- Per-recipient variant record when template adapted (no LI URL → swap; EU/UK → gdpr-light; no phone → drop call)
- Cross-channel capacity plan (per-channel headroom)
- Cadence + Campaign records ready for `campaign-management` to monitor
- Run record: filter results, capacity headroom, dispatched-touch count, recommended next skill

## Done Criteria

1. Channel readiness checked; cadence proceeds with available channels.
2. Cadence template chosen; validated against conventions §2.2.
3. Recipient filter applied (cross-channel); per-recipient variants documented.
4. Cross-channel capacity check passed.
5. Per-touch dispatch to channel skills successful; provenance propagated.
6. Cross-channel rules validated (spacing / isolation / quiet hours / capacity).
7. Cadence + Campaign records built per conventions §2.2 / §2.3 with branch rules + exit conditions.
8. Push to CRM emitted; run summary one-screen; recommends `campaign-management`.

## Pitfalls

- **Same-day double-touches.** Email + call same day = harassment.
- **Channel-isolation broken.** "As I LinkedIn-messaged you" feels invasive.
- **Treating LI connect as a touch with content.** Connection request is artifact + ≤300 chars; conversation is the follow-up message.
- **Linear cadence without branch logic.** Multi-channel without branches doesn't beat single-channel.
- **Cadence too long (9+).** Nuisance; reply rate drops past T7.
- **Cadence too short (<5).** Leaves conversion on the table.
- **Capacity overrun across channels.** Don't promise touches you can't deliver per-day.
- **Skipping the break-up.** Cleanest reply-rate boost in second half.
- **No exit conditions.** Cadences that don't exit on reply-positive book meetings into already-replied threads.
- **Account-based without coordination.** Three reps cold-calling same account same week = bad signal.
- **Manual-mode capacity miscalculations.** Optimistic estimates without user confirmation.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (recipients, companies, hook references, dates) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. This skill propagates from channel skills; ensure provenance flows through correctly.

## Verification

Cadence is real when: every touch dispatched to correct channel skill with full context; cross-channel capacity caps respected at every per-day window; channel-isolation rule passes (no body cross-references); per-day spacing rule passes; branch rules trigger correctly; exit conditions fire on first-trigger; re-running same input produces same cadence shape.

## Example

**User prompt:** "Build a full multi-channel cadence for 50 Tier-1 SAL-eligible prospects. WorkflowDoc `[hypothetical]` to Heads of Support. Default 7-touch / 21-day."
**What should happen:** Channels ready (email ✓ LI ✓ call ✓). Filter 50 → 43 `[hypothetical]` (4 re-touch, 3 EU/UK swap to gdpr-light, 5 no-phone swap to email-li-only). Capacity: email 12% / LI-connect 54% / LI-msg 19% / call 2% `[hypothetical]`. Dispatch 303 touches `[hypothetical]` across 3 channels via channel skills (`cold-email-sequence`, `linkedin-outreach`, `cold-calling`). Branch rules active: LI-connect-accepted → swap T6 to LI-message; email-bounce → drop email touches. Recommend `campaign-management` (target multi-channel reply ≥6% by D+10).

**User prompt:** "LinkedIn account is amber — set up cadence anyway."
**What should happen:** Drop LI touches. Use `email-only-5touch-19d` template per recipient. Surface LI channel as not-ready. Recommend `linkedin-outreach` cool-down before next run.

**User prompt:** "ABM cadence: 20 named accounts × 3 contacts each."
**What should happen:** `abm-3thread-21d` template. 60 recipients dispatched in coordinated threads (no same-account same-day across reps). Cross-thread dedup if same recipient in multiple threads. Surface account-level coordination plan.

## Linked Skills

- Cadence dispatched, monitor → `campaign-management`
- Email channel needs copy → `cold-email-sequence`
- LI channel needs copy → `linkedin-outreach`
- Call channel needs scripts → `cold-calling`
- Email infrastructure breaks mid-cadence → `email-infrastructure-setup`
- Replies arriving → `reply-classification` (planned)
- Meeting booked → `discovery-call-prep` (planned)
- Run produced 0 dispatches → `data-enrichment` or `lead-scoring`

## Push to CRM

After dispatching, persist agent-actionable cadence + campaign records to agentic-app via `POST ${CRM_URL}/api/push`. This skill pushes only cadence + campaign records; per-touch records are pushed by their channel skills. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Cadence definition (template instance per campaign) | `interaction` (type: `research`) | `relevance` = template + per-recipient variants + branch rules + exit conditions; `tags: "#cadence-definition #function-3"` |
| Campaign run record | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#multi-channel-cadence-run #function-3"` |
| Active campaign reference on each recipient | `person` (PATCH via dedup key) | `active_cadence_id`, `active_campaign_id`, `tags` updated to include `#in-active-cadence` |
| Per-recipient variant record (when adapted) | `interaction` (type: `research`) | `relevance` = "Recipient X uses variant Y because Z"; `tags: "#cadence-variant #function-3"` |
| `[unverified — needs check]` (channel skill blocks) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #multi-channel-cadence"`; per-recipient variant set to "blocked" |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
# Channel-skill API keys per their .env (Smartlead, HeyReach, JustCall, etc.)
SENDS_PER_DOMAIN_PER_DAY_CAP=30
LINKEDIN_CONNECTS_PER_WEEK_CAP=80
CALLS_PER_REP_PER_DAY_CAP=80
CAMPAIGN_TOTAL_RECIPIENTS_CAP=500
CAMPAIGN_DAILY_VOLUME_CAP=200
```

### Source tag

`source: "skill:multi-channel-cadence:v2.0.0"`

### Example push (cadence definition)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#cadence-definition #function-3",
    "relevance": "Cadence cad_email-li-call-7touch-21d_v1 [hypothetical] active in campaign cmp_workflowdoc_t1_mc_2026-05-22 [hypothetical] (WorkflowDoc [hypothetical]). Template: email-li-call-7touch-21d (7 touches over 21 days). Channels: email (Smartlead) + LI (HeyReach) + call (JustCall). Branches: LI-connect-accepted → swap T6 to LI-message; email-bounce → drop email touches keep others. Exit on: reply-positive / reply-negative / bounce / unsubscribed / manual-stop. 38 recipients standard / 3 GDPR-light / 5 no-call-swap [hypothetical].",
    "source": "skill:multi-channel-cadence:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#multi-channel-cadence-run #function-3",
    "relevance": "Multi-channel cadence run cmp_workflowdoc_t1_mc_2026-05-22 [hypothetical] (WorkflowDoc [hypothetical]). Template: email-li-call-7touch-21d. Filter: 50 → 43 eligible [hypothetical] (4 re-touch / 3 EU/UK swapped / 5 no-call swap). Channel readiness: email ✓ / LI ✓ / call ✓. Capacity: email 12% / LI-connect 54% / LI-msg 19% / call 2% [hypothetical]. 303 touches dispatched [hypothetical] across 3 channels. Recommended next: campaign-management (target multi-channel reply rate ≥6% by D+10).",
    "source": "skill:multi-channel-cadence:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Cadence proceeds; pushes per standard mapping. |
| `[unverified — needs check]` (from channel skills) | Cadence variant set to "blocked" for affected recipients; pushes ONLY as `interaction:research` with `#unverified #review-required #multi-channel-cadence` tags. |
| `[hypothetical]` | Never proceeds; never pushes. Local artifact only. |

### When NOT to push

- Cadence drafted but never dispatched (user paused at pre-flight) — local artifact; do not push.
- Zero channels ready — push run record with `#blocked-no-channel-ready`; no cadence record.
- All recipients filtered out (zero eligible) — push run record with `#zero-eligible`; no per-recipient variants.
- `[unverified]` on channel-skill output — see provenance routing.
- `[hypothetical]` — never.
