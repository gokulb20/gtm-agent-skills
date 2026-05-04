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

Compose a 5–9 touch cadence across email + LinkedIn + cold call channels, calling each channel-specific skill (`cold-email-sequence`, `linkedin-outreach`, `cold-calling`) for the actual copy/scripts and orchestrating the per-recipient sequencing. Owns the cross-channel rules: channel-isolation (don't reference one channel's content in another's body), per-day spacing (no two touches same day), capacity-cap aggregation across channels, branch logic on early replies, and exit conditions. Output is a Cadence record per conventions §2.2 + dispatched per-channel Touch handoffs.

> *The worked example uses a fictional product (WorkflowDoc) for illustration — same product as function-1, in a third role: WorkflowDoc as the seller running a full multi-channel cadence against function-2's Tier-1 SAL-eligible prospects. The frameworks, channel-stacking rules, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Touch / Cadence / Campaign schemas, three-mode pattern, cross-channel capacity caps, compliance, anti-fab, push-to-CRM routing — live in `function-3-skills/function-3-conventions.md`. This skill assumes it.*

## Purpose

Single-channel cadences ceiling out at the channel's maximum response rate. Multi-channel cadences (email + LI + call layered) lift response rate 30–60% over best single channel — because different prospects respond on different channels, and persistence across channels signals seriousness. But composition is hard: same-day double-touches read as harassment; channel-isolation matters (don't quote your email in a LI message); capacity caps are per-channel and must aggregate; branch logic on replies must exit the right cadence on the right channel. This skill orchestrates without writing copy itself — it calls the three channel skills for their artifacts and arranges them.

## When to Use

- "Build a full multi-channel cadence for our Tier-1 list."
- "Email reply rate plateaued at 2.5% — add LinkedIn and call legs."
- "Account-based campaign — reach 3 contacts per company across all channels."
- "I want a cadence template I can re-use for future campaigns."
- "Compose email touches 1 + 2 + 4, LinkedIn connect at touch 3, cold call at touch 5."
- Pre-launch when single-channel reply rate isn't enough.
- Tier-1 plays where channel diversity reduces dependency on any one signal.

### Do NOT use this skill when

- Volume is small enough (<30 leads) that single-channel + manual judgment beats orchestration overhead.
- One channel is broken (e.g. email infrastructure not ready, or LI account amber) — fix that channel first; multi-channel can't paper over single-channel infrastructure issues.
- The user wants a custom cadence that bends channel-isolation rules ("quote my email in the LI follow-up") — refuse; channel-isolation is a guardrail.
- The cadence is purely reactive (e.g., "follow up after a meeting no-show") — that's a different skill family (function-4 follow-up-management).

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Scored + enriched Lead list | yes | `lead-scoring` (with `data-enrichment` upstream) | Same input as channel skills. |
| 2 | ICP P-T-O chain | yes | `icp-definition-v2` | Passed through to channel skills. |
| 3 | Positioning message house | yes | `positioning-strategy-v2` | Passed through. |
| 4 | Active channel skills ready flags | yes | each channel skill | Email: infrastructure ready? LI: account safety green + LI URLs verified? Call: phones verified + DNC scrubbed? Cadence skips channels not ready per recipient. |
| 5 | Sender pool + rep pool | yes | `email-infrastructure-setup` + dialer config | Used for cross-channel capacity planning. |
| 6 | Run purpose tag | yes | user | |
| 7 | Cadence template (optional) | no | user / library | "tier-1-multi-channel-21d" / "ABM-3-thread-30d" / custom; default = standard 7-touch / 21-day. |

### Fallback intake script

> "Multi-channel cadence composes email + LinkedIn + cold call into one 14–21 day flow.
>
> Three channel-readiness checks:
> - Email infrastructure (`email-infrastructure-setup` flag = green)?
> - LinkedIn account safety green + URL coverage on list?
> - Phone coverage verified + DNC-scrubbed?
>
> I'll skip channels per-recipient if their gate fails (e.g., a lead with no LI URL gets email + call only).
>
> Default cadence template is 7-touch over 21 days. Want a custom template, or use the default?"

### Input validation rules

- All channel skills' readiness flags fail → block; recommend single-channel only with the available channel.
- Lead list has 0% LI URL coverage → drop LI touches from cadence; warn user.
- Lead list has 0% verified phone coverage → drop call touches; warn user.
- Cadence length outside [3, 9] → block; explain (3 is minimum for cold; 9+ becomes nuisance).
- Two touches scheduled on same day for same recipient → audit failure; auto-spread by 1 day each direction.
- Same-day call + email scheduled → flag (allowed for SAL warm-prospects, not cold openers).

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Cold Calling 2.0 cadence patterns** | Aaron Ross & Marylou Tyler — *Predictable Revenue* (2011) | The 5–7 touch / 14–21 day cadence as the canonical structure for cold outreach; SDR/AE handoff norms when meetings book mid-cadence. |
| **Sequence pattern library** (industry-standard, codified) | Outreach.io, Salesloft, Smartlead, Lemlist published cadence libraries | Standard 5–7 step shapes that consistently produce 5–10% reply rates: opener → follow-up → resource share → value-prop pivot → social proof → break-up → resurrection. Multi-channel weaves LI + call into this template. |
| **Channel-isolation rule** (house-built — reputational best practice) | Crewm8 | A touch on channel A does NOT directly quote or reference content sent on channel B in the body of channel B's touch. Reasoning: (a) feels surveillance-y to the recipient, (b) recipients track different channels in different mental contexts. Touches reference each other implicitly via hook continuity, not explicitly via "as I emailed you yesterday." |
| **Per-day spacing rule** (industry-standard) | Convention | No two touches same recipient same day, except: email + LI connection request acceptable if email is opener and LI is follow-up artifact; never two same-channel touches same day. |
| **Branch logic patterns** (house-built, codified) | Crewm8 | Standard branches: `if email-bounce → exit cadence + flag for re-enrichment`; `if reply-positive → exit + handoff`; `if LI-connect-accepted → swap LI message in for next email touch`; `if email-opens-but-no-reply by D+10 → swap-in different opener angle`. |
| **Capacity-cap aggregation** (house-built) | Crewm8 | Cross-channel capacity is computed AS A POOL: a recipient who got an email today doesn't also count against LI cap (different cap), but the per-rep daily call cap is shared across all reps assigned. |
| **Trigger Events for Sales Success** | Craig Elias (2009) | Cadence pacing reflects trigger half-life: a 60-day-old hire trigger justifies aggressive 14-day cadence; a 9-month-old funding trigger justifies softer 21-day cadence. |

## Tools and Sources

This skill is a composer; it doesn't talk to outreach platforms directly. Its operations are:
- Read channel skills' readiness flags + capacity headroom.
- Generate Cadence record (per conventions §2.2).
- Dispatch per-channel Touch handoffs (call channel skills with cadence position context).
- Track cross-channel exit conditions.

### Channel skill handoff contract

```
multi-channel-cadence.compose(lead, cadence_template) →
  for each touch_position in template:
    channel_skill = lookup_skill(touch_position.channel)
    channel_skill.prepare(lead, position, sender) → Touch[draft]
    accumulate Touches into Cadence record
```

Each channel skill maintains its own provenance, audit, and capacity gates; this skill's job is composition + dispatch.

### Cadence template library

| Template | Length | Duration | Channel mix | Use case |
|---|---|---|---|---|
| `email-only-5touch-19d` | 5 | 19d | E E E E E | Hook-rich list; email infrastructure mature |
| `email-li-5touch-19d` | 5 | 19d | E LI-connect E E E | Standard multi-channel light |
| `email-li-call-7touch-21d` | 7 | 21d | E LI-connect E Call E LI-message E | Standard multi-channel full |
| `tier-1-9touch-30d` | 9 | 30d | E LI-connect E Call E LI-message Call E E (break-up) | Tier-1 SAL-eligible prospects |
| `abm-3thread-21d` | 21 | 21d | 3 threads × (E LI-connect E Call E LI-message E) per company | Account-based; 3 contacts per company |
| `email-fatigue-relief-3touch-7d` | 3 | 7d | LI-connect Call E | When email channel is fatigued |
| `gdpr-light-4touch-21d` | 4 | 21d | E E E (break-up with explicit opt-out) | EU/UK recipients; conservative pacing |

## Procedure

### 1. Validate prerequisites

Read scored Lead list; check channel skills' readiness flags; load ICP P-T-O + message house. If at least one channel is ready, proceed (skip unavailable channels per recipient). If zero channels ready, block.

### 2. Determine mode (per channel)

Each channel inherits its own mode (API / manual / BYO) from its skill. The cadence record carries the per-channel mode metadata.

### 3. Pick or compose cadence template

User-supplied template OR default `email-li-call-7touch-21d`. Validate template against function-3-conventions §2.2 schema. Adjust template per recipient if a channel is unavailable for that recipient (e.g., no LI URL → swap LI touch for email touch with different angle).

### 4. Filter recipient list (cross-channel)

Apply union of channel-specific filters:
- Drop records that fail every channel's gate (no email, no LI, no phone).
- Apply tier filter.
- Apply re-touch rules per conventions §7 (no record touched in any channel within 90d; respect `not-interested` reply windows).
- For EU/UK recipients without `gdpr_basis: legitimate-interest`, swap to `gdpr-light` template.

Surface filter counts.

### 5. Pre-flight: cross-channel capacity check

Compute per-channel touches needed:
- Email touches × eligible recipients × `1 / (sender_pool × per_domain_cap × duration)` → email headroom.
- LI touches × eligible × `1 / (li_cap × duration_weeks)` → LI headroom.
- Call touches × eligible × `1 / (rep_pool × call_cap × duration)` → call headroom.

If any channel over-capacity → recommend tier-segmenting, extending duration, expanding pools, or swapping to a lighter template. Surface to user.

### 6. Dispatch to channel skills

For each touch position, call the appropriate channel skill's `prepare()` operation with: lead, cadence position, sender (from pool), branch context (whether prior touches succeeded). Each channel skill returns a Touch[draft] with its own provenance.

Touches with provenance `[unverified — needs check]` are routed to review queue per conventions §10.3 (the channel skill itself blocks; this skill propagates).

### 7. Validate cross-channel rules

Audit the assembled cadence:
- **Per-day spacing**: no two touches same day (except email + LI-connect on opener day, which is allowed if non-redundant).
- **Channel-isolation**: scan each Touch's body for explicit references to other channels (e.g., "as I emailed you yesterday"). Flag and rewrite via the channel skill.
- **Quiet-hours alignment**: each touch's `scheduled_for` respects recipient's local timezone for that channel's quiet hours (email + LI 8pm–8am; call 9pm–8am TCPA).
- **Capacity-cap distribution**: per-day touch count per channel doesn't exceed any single channel's per-day cap.

Failures → fix or surface for user.

### 8. Build Cadence + Campaign records

Compose Cadence record (template instance with per-recipient touch list) and Campaign record (run-level container with all recipients) per conventions §2.2 / §2.3. Write `branch_rules` and `exit_conditions` explicitly:
- Exit on: `reply-positive` / `reply-negative` / `bounce` / `unsubscribed` / `manual-stop` / `cap-hit-without-completion`.
- Branch on: `LI-connect-accepted` (swap next email for LI message), `email-bounce` (drop email touches, keep LI/call if available).

### 9. Push to CRM + emit run summary

Per conventions §11: push Cadence + Campaign as `interaction:research`; per-channel Touches push via their channel skills (this skill doesn't push the per-touch records — channel skills do). Run summary: cadence template, eligible-recipient count, dropped counts (by reason), per-channel headroom, per-recipient cadence variant (if templates were adapted), recommended next skill (`campaign-management` for monitoring).

## Output Template

```yaml
run:
  run_id: <uuid>
  campaign_id: <uuid>
  cadence_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  template_used: <template name from library or "custom">
  template_length: <int touches>
  template_duration_days: <int>
  inputs:
    lead_count_input: <int>
    lead_count_eligible: <int>
    lead_count_dropped:
      no_active_channel: <int>
      tier_filter: <int>
      re_touch_rule: <int>
      eu_uk_no_lia_swapped_template: <int>
  channel_readiness:
    email: ready | not-ready
    linkedin: ready | not-ready
    call: ready | not-ready
  capacity:
    email_headroom_pct: <float>
    linkedin_headroom_pct: <float>
    call_headroom_pct: <float>
  per_recipient_variants:
    standard_template: <int>
    no_li_url_swap: <int>
    no_phone_swap: <int>
    gdpr_light_swap: <int>
  exit_conditions: [reply-positive, reply-negative, bounce, unsubscribed, manual-stop, cap-hit]
  branch_rules:
    - condition: li-connect-accepted
      action: swap-next-email-to-li-message
    - condition: email-bounce
      action: drop-email-touches-keep-others
  warnings: [<string>]
  next_skill_recommendation: campaign-management

per_recipient:
  - lead_id: <uuid>
    cadence_variant: <name>
    touches: [<position, channel, day_offset, hour_local, framework, scheduled_for, status>]
```

## Worked Example

> *All fictional entities below are tagged `[hypothetical]` — illustrative only.*

**User prompt**: "Build a full multi-channel cadence for our 50 Tier-1 SAL-eligible prospects. WorkflowDoc to Heads of Support. Default 7-touch / 21-day template."

**Step 1 — Validate**: 50 leads from `lead-scoring`. Channel readiness: email ready (`email-infrastructure-setup` flag green), LI ready (account green, 100% URL coverage), call ready (DNC scrub fresh, 90% phone coverage).

**Step 2 — Mode**: Per-channel inherited (Smartlead for email, HeyReach for LI, JustCall for call).

**Step 3 — Template**: `email-li-call-7touch-21d` (default).
```
T1 (D+0)  Email - opener (CCQ + Pain)
T2 (D+2)  LinkedIn connect - event-based
T3 (D+5)  Email - follow-up #1 (CCQ + Vision)
T4 (D+9)  Cold call - 9s opener + discovery
T5 (D+12) Email - follow-up #2 (RTA / resource share)
T6 (D+16) LinkedIn message (if connected) OR Email follow-up #3
T7 (D+20) Email - break-up
```

**Step 4 — Filter**:
- Input: 50
- No active channel (zero email + zero LI + zero phone): 0
- Tier filter: 0 (all SAL)
- Re-touch (called within 90d): 4
- EU/UK no LIA: 3 (swapped to `gdpr-light-4touch-21d`)
- Phone coverage drop: 5 (call touches replaced with email — they get `email-li-5touch-19d` variant)
- **Eligible: 43 (38 standard + 3 GDPR-light + 5 no-call swap)**

**Step 5 — Capacity check**:
- Email touches: 5 × 38 + 4 × 3 + 5 × 5 = 227 / (3 mailboxes × 30/day × 21d) = 12% utilization ✓
- LI connects: 1 × 38 + 0 × 3 + 1 × 5 = 43 / 80 weekly cap (54% — within safe range)
- LI messages: 1 × 38 = 38 / 200 weekly cap (19%)
- Calls: 1 × 38 = 38 / (1 rep × 80/day × 21d) = 2% utilization ✓
- All channels green; proceed.

**Step 6 — Dispatch to channel skills**:
- For each of 43 recipients, dispatch each touch to its channel skill:
  - 38 standard recipients × 7 touches = 266 dispatches
  - 3 GDPR-light × 4 touches = 12 dispatches
  - 5 no-call-swap × 5 touches = 25 dispatches
- Channel skills return Touch[draft]s with their own provenance + audit.

For one recipient (Esme Liang [hypothetical] @ Stitchbox [hypothetical], standard template):

```yaml
recipient: lea_esme_liang_stitchbox
cadence_variant: email-li-call-7touch-21d
touches:
  - position: 1, channel: email, day_offset: 0, hour_local: 10, framework: ccq-pain
  - position: 2, channel: linkedin-connect, day_offset: 2, hour_local: 11, framework: event-based
  - position: 3, channel: email, day_offset: 5, hour_local: 14, framework: ccq-vision
  - position: 4, channel: call, day_offset: 9, hour_local: 10:30, framework: cc20+sandler
  - position: 5, channel: email, day_offset: 12, hour_local: 9, framework: rta-resource
  - position: 6, channel: linkedin-message, day_offset: 16, hour_local: 11
  - position: 7, channel: email, day_offset: 20, hour_local: 9, framework: break-up
```

**Step 7 — Validate cross-channel rules**:
- Per-day spacing: T1 (D+0 email) and T2 (D+2 LI-connect) — 2 days apart ✓
- Channel-isolation: T3 email body doesn't reference T2 LI connect ✓ (each generated independently by its channel skill)
- Quiet hours: all touches within recipient local 8am–8pm (email/LI) and 8am–9pm (call) ✓
- Capacity: per-day per-channel limits respected ✓

**Step 8 — Cadence + Campaign records built**:
```yaml
campaign_id: cmp_workflowdoc_t1_mc_2026-05-22
cadence_id: cad_email-li-call-7touch-21d_v1
recipients: [<43 lead_ids>]
state: active
exit_conditions: [reply-positive, reply-negative, bounce, unsubscribed, manual-stop]
branch_rules:
  - condition: li-connect-accepted
    action: swap-T6-to-li-message-personalized-on-acceptance
  - condition: email-bounce
    action: drop-email-touches-keep-li-and-call
```

**Step 9 — Run summary**:
```
WorkflowDoc Multi-Channel Cadence Run [hypothetical]
Run ID: cmp_workflowdoc_t1_mc_2026-05-22
Template: email-li-call-7touch-21d (default)
Eligible: 43 (38 standard + 3 GDPR-light + 5 no-call-swap)
Dropped: 4 (re-touch rule); 3 EU/UK swapped template
Channel readiness: email ✓ / linkedin ✓ / call ✓
Capacity: email 12% / LI-connect 54% / LI-msg 19% / call 2%
Variants per recipient documented; branch rules active
Total touches dispatched: 303 across 3 channels
Recommended next: campaign-management (monitor multi-channel reply rate; target ≥6% by D+10)
```

## Heuristics

- **Multi-channel lifts response 30–60% over best single channel.** Below that, you're probably double-touching same-day or referencing channels (channel-isolation broken).
- **The first email matters most.** It frames the entire cadence; weak T1 = weak cadence regardless of subsequent touches.
- **Email + LI-connect on D+0 and D+2 is the sweet spot.** Closer = harassment; further = forgotten.
- **Calls as touch 4 outperform calls as touch 1.** By touch 4, the prospect has seen the name 3 times and is more likely to answer.
- **Break-up touches are essential.** A 7-touch cadence without a clean break-up at T7 leaves 5–10% of conversion on the table.
- **Account-based plays (3 contacts × company) need staggered cadences across contacts.** Don't have 3 reps cold-call the same company same week — coordinate.
- **Branch on LI-connect-accepted to swap a touch.** Don't email the same content twice if they accepted the connection.
- **Don't reference other channels' content explicitly.** "As I emailed you" feels like surveillance even when factually true.
- **Channel-isolation matters more for low-trust recipients (cold) than high-trust (warm).** Once they engage, channel-bridging is fine.
- **Same-day double-touches (T1 email + T1 LI-connect on D+0) are acceptable** because LI connection is artifact-only (no message yet). Two same-channel touches same day = harassment.
- **GDPR recipients get conservative cadences.** Fewer touches, longer durations, explicit opt-out at every email.

## Edge Cases

- **No LI URL for any record.** Drop all LI touches; cadence becomes email + call only. Surface; recommend `lead-sourcing-linkedin` for future runs.
- **No phone for any record.** Drop call touches; cadence becomes email + LI. Surface.
- **All channels broken (rare).** Block; can't compose multi-channel cadence; recommend single-channel mode of whichever is closest to ready.
- **Mid-cadence channel break.** E.g., email infrastructure flag flips false at T3 → pause email touches; continue LI + call if active. `campaign-management` decides resumption.
- **Reply on touch 2 (LI connect note).** Exit cadence on that recipient; route through `reply-classification`; no further touches.
- **Connection request rejected.** Exit LI sub-cadence; continue email + call legs.
- **Email bounces hard at T1.** Drop all email touches for that recipient; keep LI + call if available; flag for re-enrichment.
- **Recipient unsubscribes via email.** Exit ALL channels for that recipient (unsubscribe is global respect, not channel-specific) — though TCPA / LinkedIn ToS technically allow LI / call separately, courteous practice is global exit.
- **Cadence template requires LI but recipient has private profile.** LI touch becomes "no-op" for that recipient; cadence proceeds without it.
- **Tier-2 recipient in the list (lower-conviction).** Either drop down to `email-only-5touch-19d` template (cheaper) or accept lower expected ROI.
- **ABM 3-thread cadence: same recipient in 2 threads.** Dedupe; pick the higher-priority thread; warn user.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Channel skill returns `[unverified — needs check]` for many touches | high block rate | Surface; recommend re-enrichment for affected recipients; cadence proceeds for verified subset. |
| Capacity over for one channel | computed at pre-flight | Tier-segment, extend duration, expand pool, swap to lighter template. Surface to user. |
| Branch rule misfires | e.g., LI-connect accepted but T4 email still goes | Audit branch logic; fix; re-dispatch affected touches. |
| Mid-cadence pause requested by `campaign-management` | reputation-pause / volume-pause | Pause new dispatches; in-flight Touches complete; resume on user signal. |
| Recipient timezone changed mid-cadence (rare) | LI updates location | Re-compute remaining touches' `scheduled_for`. |
| Channel skill outage (e.g., HeyReach down) | dispatch fails | Pause that channel's touches; retry with backoff; if persistent, fallback to manual mode for that channel. |
| Cross-channel ID collision | two touches same day same recipient | Spread by 1 day in either direction; if neither shifts cleanly, surface. |
| Template adaptation produces broken cadence | e.g., dropping LI removes T2 and T6 leaving gaps | Re-validate; collapse gaps; ensure remaining touches still flow logically. |
| Manual-stop on one recipient mid-cadence | user pause | Honor immediately; in-flight Touches complete; remaining cancelled. |
| Dispatch rate exceeded | dispatching too many at once to channel skill | Throttle dispatch loop; respect channel skill's own rate limits. |

## Pitfalls

- **Same-day double-touches.** Email + call same day = harassment. Spread.
- **Channel-isolation broken.** "As I LinkedIn-messaged you" feels invasive.
- **Treating LI connect as a touch with content.** Connection request is artifact + ≤300 char note; the conversation is the follow-up message after acceptance.
- **Linear cadence without branch logic.** Multi-channel without branches doesn't beat single-channel — branches are the value.
- **Cadence too long.** 9+ touches = nuisance; reply rate drops past T7.
- **Cadence too short.** <5 touches = leaves conversion on the table.
- **Capacity overrun across channels.** A single recipient × 7 touches × 50 recipients = 350 touches; if your call cap is 80/day, that's 4+ days of just calls.
- **Skipping the break-up.** Cleanest reply-rate boost in the second half of cadence.
- **No exit conditions.** Cadences that don't exit on reply-positive book meetings into already-replied threads (looks broken).
- **Account-based without coordination.** Three reps cold-calling same account same week = bad signal to that account.
- **Fabricating named entities (anti-fabrication / provenance rule).** This skill doesn't write copy directly (channel skills do), but its cadence rationale references touches' content; ensure all references propagate provenance correctly per conventions §10. Untagged claims about touch content = contract violation.
- **Manual-mode capacity miscalculations.** Cross-channel capacity in manual mode depends on user's actual time; surface optimistic estimates as `[user-confirmed]` rather than `[verified]`.

## Verification

The cadence is real when: (a) every touch in every recipient's variant is dispatched to the correct channel skill with full context; (b) cross-channel capacity caps respected at every per-day window; (c) channel-isolation rule passes (no body cross-references); (d) per-day spacing rule passes (max 1 touch per recipient per day, exception email+LI-connect D+0); (e) branch rules trigger correctly on simulated reply-positive / LI-accept / bounce events; (f) exit conditions fire correctly on first-trigger; (g) re-running same input deterministically produces same cadence shape.

## Done Criteria

1. Channel readiness flags checked; cadence proceeds with available channels.
2. Cadence template chosen (library or custom); validated against conventions §2.2.
3. Recipient filter applied (cross-channel); per-recipient template variants documented.
4. Cross-channel capacity check passed (or user authorized over-cap).
5. Per-touch dispatch to channel skills successful; provenance propagated.
6. Cross-channel rules validated (per-day spacing, channel-isolation, quiet hours, capacity).
7. Cadence + Campaign records built per conventions §2.2 / §2.3 with branch rules + exit conditions.
8. Push to CRM emitted; run summary one-screen with template + variants + capacity headroom.
9. Recommended next skill stated (`campaign-management`).

## Eval Cases

### Case 1 — full multi-channel, all gates green

Input: 50 Tier-1 SAL leads, all channels ready, default `email-li-call-7touch-21d`.

Expected: ~43 eligible after re-touch + GDPR filters; per-recipient touches dispatched; ~300 total dispatches across 3 channels; capacity headroom comfortable; recommends `campaign-management` (target multi-channel reply rate ≥6%).

### Case 2 — partial readiness (LI account amber)

Input: 50 leads, email + call ready, LI account amber.

Expected: cadence drops LI touches; uses `email-only-5touch-19d` template per recipient; surfaces LI channel as not-ready; recommends `linkedin-outreach` cool-down before next run.

### Case 3 — ABM 3-thread cadence

Input: 20 named accounts, 3 contacts per account = 60 recipients, `abm-3thread-21d` template.

Expected: 60 recipients dispatched in coordinated threads (no same-account same-day across reps); cross-thread dedup if same recipient appears in multiple threads; surfaces account-level coordination plan.

### Case 4 — GDPR-heavy list

Input: 30 leads, 70% EU/UK, mixed `gdpr_basis: legitimate-interest` coverage.

Expected: ~21 EU/UK swap to `gdpr-light-4touch-21d`; ~9 standard template; surface GDPR coverage gap and recommend `data-enrichment` GDPR pass for remaining.

### Case 5 — branch logic test (simulated)

Input: standard cadence; simulate LI-connect-accepted at T2.

Expected: T6 (originally email) swaps to LI-message-personalized-on-acceptance; remaining cadence proceeds with the swap; branch decision logged in adjustments_log.

## Guardrails

### Provenance (anti-fabrication)

Per §10 of conventions: this skill propagates provenance from channel skills. The Cadence record's claim "we will send 300 touches" is `[user-provided]` (user authorized) + `[verified]` per channel readiness flag. Worked-example fictional entities tagged inline. No copy is generated here — copy provenance lives in channel skills.

### Evidence

Every cadence variant decision (template adaptation, channel drop, GDPR swap) is logged with reason. Branch rules + exit conditions explicit + auditable.

### Scope

This skill composes. It does NOT write copy (channel skills), monitor active runs (`campaign-management`), or classify replies (function-4). Avoid scope creep.

### Framing

Run summary uses operational language. Per-recipient cadence variants surfaced explicitly so manual review is possible.

### Bias

Default templates over-index on tech / SaaS market norms. Other industries may have different cadence-length norms (e.g., enterprise sales = longer cadences). Surface; user can override.

### Ethics

Channel-isolation rule is partly an ethics rule (recipient surveillance). Don't bend it. GDPR templates not optional for EU/UK contacts.

### Freshness

Cadence templates evolve as outbound norms shift; library should be reviewed quarterly. Compliance baseline (TCPA, GDPR, Google/MS rules) is updated by `email-infrastructure-setup` and `cold-calling`; this skill inherits.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Cadence dispatched, monitor | `campaign-management` | campaign_id + recipient list + reply-rate targets |
| Email channel needs copy | `cold-email-sequence` | per-touch context (position, framework, hook source) |
| LI channel needs copy | `linkedin-outreach` | per-touch context |
| Call channel needs scripts | `cold-calling` | per-touch context |
| Email infrastructure breaks mid-cadence | `email-infrastructure-setup` | current state + readiness gate |
| Replies start arriving | `reply-classification` (function-4, planned) | reply text + touch_id |
| Meeting booked mid-cadence | `discovery-call-prep` (function-4, planned) | meeting context |
| Single channel underperforms in cadence | back to that channel skill (rewrite) | metrics |
| Run produced 0 dispatches | `data-enrichment` (re-enrichment) or `lead-scoring` (re-tier) | filter results |

## Push to CRM

After dispatching, persist agent-actionable cadence + campaign records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`). This skill pushes only the cadence + campaign records; per-touch records are pushed by their channel skills.

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
    "relevance": "Cadence cad_email-li-call-7touch-21d_v1 active in campaign cmp_workflowdoc_t1_mc_2026-05-22. Template: email-li-call-7touch-21d (7 touches over 21 days). Channels: email (Smartlead) + LI (HeyReach) + call (JustCall). Branches: LI-connect-accepted → swap T6 to LI-message; email-bounce → drop email touches keep others. Exit on: reply-positive / reply-negative / bounce / unsubscribed / manual-stop. 38 recipients standard / 3 GDPR-light / 5 no-call-swap.",
    "source": "skill:multi-channel-cadence:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#multi-channel-cadence-run #function-3",
    "relevance": "Multi-channel cadence run cmp_workflowdoc_t1_mc_2026-05-22. Template: email-li-call-7touch-21d. Filter: 50 → 43 eligible (4 re-touch / 3 EU/UK swapped / 5 no-call swap). Channel readiness: email ✓ / LI ✓ / call ✓. Capacity: email 12% / LI-connect 54% / LI-msg 19% / call 2%. 303 touches dispatched across 3 channels. Recommended next: campaign-management (target multi-channel reply rate ≥6% by D+10).",
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
- Zero channels ready — push the run record with `#blocked-no-channel-ready`; no cadence record.
- All recipients filtered out (zero eligible) — push the run record with `#zero-eligible`; no per-recipient variants.
- `[unverified]` on channel-skill output — see provenance routing.
- `[hypothetical]` — never.
