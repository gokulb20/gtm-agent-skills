# Function 4 — Conversation Management Conventions

This file is the shared rules document for every skill in `function-4-skills/`. All four skills (`reply-classification`, `objection-handling-library`, `discovery-call-prep`, `follow-up-management`) MUST reference this document by name in their `## Inputs Required` and `## Pitfalls`/`## Push to CRM` sections rather than redefining the reply taxonomy, the objection library, the confidence floors, or the cadence-state effects locally.

> *The worked examples in function-4 skills use a fictional product (WorkflowDoc) for illustration — same product as function-1/2/3, in its fourth role: WorkflowDoc as the seller now triaging real human replies to the cadences function-3 sent. The taxonomies, schemas, confidence floors, and routing logic are vertical-agnostic and apply to any B2B GTM context.*

---

## 1. Why this file exists

Function-1 produced documents. Function-2 produced records (Leads, all conforming to one schema). Function-3 produced executions (Touches sent to real humans). Function-4 produces **interpretations** — labels and routing decisions on top of inbound reply text.

That changes four things and makes a conventions file necessary:

- **Shared atomic unit: the Reply.** All four skills read the same reply object. `reply-classification` writes labels onto it; `objection-handling-library` matches embedded objections against the canonical 12-library; `discovery-call-prep` consumes positive labels; `follow-up-management` consumes not-now / OOO labels. If any of them disagrees on the field names, label values, or confidence semantics, the pipeline fragments silently.
- **Fabrication risk shifts mode.** Function-3's risk was inventing facts in copy *sent* to people; function-4's risk is inventing facts *about* what people said. A confident wrong classification pushes a Tier-1 prospect into "exit-permanent" cadence-state — silently. The defense is two-layer provenance: reply text is `[user-provided]` (came from a real human); classification is `[verified: llm-classifier:run_<id>]` with confidence; below floor → manual review.
- **The skills route to each other constantly.** `reply-classification` dispatches to `objection-handling-library` / `discovery-call-prep` / `follow-up-management`. They each write back to the person record's `cadence_state`. Without a single source of truth for which label routes where and what each does to the person record, the four skills will drift the moment one is updated.
- **Function-4 is the boundary between outbound (1–3) and pipeline (5–6).** A `positive` label is the trigger for a stage advance in `pipeline-stages` (function-5). A `not-interested` label feeds `customer-feedback-analysis` (function-6) loss-reason data. Centralizing the label semantics here prevents downstream functions from re-defining them.

---

## 2. Shared schemas — Reply, ReplyClassification, ObjectionMatch, DiscoveryBriefing, FollowUpSchedule

These are the canonical record shapes. Every function-4 skill normalizes its inputs to these, and writes its outputs in these shapes. The agentic-app CRM stores them across `interaction:reply` / `interaction:research` / `person` PATCH records.

### 2.1 Reply (the atomic input)

| Field | Type | Required | Notes |
|---|---|---|---|
| `reply_id` | UUID | yes | Internal ID. Generated at receipt. Format: `rpl_<YYYY-MM-DD>_<short>`. |
| `parent_touch_id` | UUID | yes | The Touch from function-3 this reply is responding to. |
| `parent_cadence_id` | UUID | yes | Inherited from the Touch. |
| `parent_campaign_id` | UUID | yes | Inherited from the Touch. |
| `lead_id` | UUID | yes | The function-2 Lead this reply is from. |
| `channel` | enum | yes | `email` / `linkedin-message` / `linkedin-inmail` / `sms` / `call-disposition` |
| `received_at` | ISO datetime | yes | Wall-clock timestamp of reply receipt. |
| `sender_identity` | object | yes | `{email, name, linkedin_url, phone}` — at least one. Matches against Lead. |
| `body_raw` | string | yes | Verbatim reply text — never modified, never translated in place. |
| `body_normalized` | string | yes | Whitespace-cleaned, signature-stripped variant for classification. Original always preserved. |
| `body_language` | enum | yes | ISO-639-1 (`en`, `es`, `fr`, etc.). Detected, not assumed. |
| `headers` | object | optional | Email-specific. `Auto-Submitted`, `In-Reply-To`, `References`. Used for OOO detection. |
| `is_auto_reply` | bool | yes | Pre-classification result from header inspection. Drives `out-of-office` short-circuit. |
| `dedup_key` | string | yes | `<lead_id>:<channel>:<sha1(body_normalized)[:12]>`. Same reply received twice never re-classifies. |
| `provenance` | object | yes | See §8. |

### 2.2 ReplyClassification (output of `reply-classification`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `reply_id` | UUID | yes | FK to Reply. |
| `label` | enum | yes | One of the 9 canonical labels — see §3. |
| `confidence` | float (0–1) | yes | LLM-emitted; below floor (default 0.75) routes to manual review. |
| `rationale` | string | yes | One sentence — must reference actual reply content, not invent. |
| `embedded_objection` | string \| null | yes | Verbatim objection text if present, else `null`. Drives routing to `objection-handling-library`. |
| `embedded_signals` | array | optional | Competitor mentions, pricing pushback, named referrals — feeds upstream. |
| `parsed_resume_date` | ISO date \| null | conditional | Required when `label = not-now` and reply contains a date phrase. See §3 + §7. |
| `dispatched_to` | enum | yes | Next skill: `objection-handling-library` / `discovery-call-prep` / `follow-up-management` / `data-enrichment` / `manual-review` / `none`. |
| `cadence_state_effect` | enum | yes | `exit-permanent` / `exit-globally` / `pause-with-resume` / `nurture-park` / `continue` / `defer-manual`. See §7. |
| `classification_run_id` | UUID | yes | Traces back to a single classification run for reproducibility. |
| `provenance` | object | yes | See §8. |

### 2.3 ObjectionMatch (output of `objection-handling-library`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `reply_id` | UUID | yes | FK to Reply. |
| `objection_text` | string | yes | Verbatim objection — same string as `ReplyClassification.embedded_objection`. |
| `best_match_label` | enum \| `new-objection-pattern` | yes | One of the 12 canonical objection labels — see §4. |
| `best_match_confidence` | float (0–1) | yes | Below floor (0.7, see §5) → `new-objection-pattern`. |
| `second_best_label` | enum \| null | optional | Surfaced when within 0.15 of primary. |
| `second_best_confidence` | float \| null | optional | |
| `framework_used` | enum | yes | `feel-felt-found` / `re-discovery` / `time-shift` / `counter-position` / `other`. |
| `response_variants` | array<object> | yes | 2–3 variants, each `{tone: light|medium|direct, body: string, word_count: int, framework_anchor: string}`. |
| `cadence_action_recommended` | enum | yes | `resume-stated-date` / `nurture-90d` / `nurture-12mo` / `exit-permanent` / `re-enrich` / `discovery-prep`. |
| `intel_captured` | array | optional | Competitor mentions, pricing signals, persistent pain — references for downstream skills. |
| `match_run_id` | UUID | yes | Traces back to a single matching run. |
| `provenance` | object | yes | See §8. |

### 2.4 DiscoveryBriefing (output of `discovery-call-prep`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `meeting_id` | UUID | yes | Internal ID. |
| `meeting_at` | ISO datetime | yes | Including timezone. |
| `meeting_channel` | enum | yes | `video` / `phone` / `in-person`. |
| `lead_id` | UUID | yes | |
| `recipient_profile` | object | yes | `{name, title, company, icp_tier, icp_score, hook_url, most_recent_reply_summary}` — ≤80 words. |
| `meddpicc` | object | yes | 8 slots (Metrics / Economic Buyer / Decision Criteria / Decision Process / **Paper Process** / Identify Pain / Champion / Competition). Each slot: `{populated: string \| null, provenance: tag, source_field: string}`. `unknown — ask` is a valid populated value. |
| `discovery_questions` | object | yes | `{open_discovery: string[3], pain_quantify: string[3], next_step: string[3]}` — 9 total. |
| `objections_pre_staged` | array<object> | yes | 3 likely objections × `{objection_label, response_excerpt, framework_used}`. Pulled from `objection-handling-library`. |
| `competitive_context` | array<object> | yes | 1–3 competitors × `{name, counter_position, pushback_question}`. |
| `agenda` | array<string> | yes | ≤3 bullets. |
| `briefing_word_count` | int | yes | Hard ceiling 450. |
| `briefing_freshness_at` | ISO datetime | yes | Must be ≤ `DISCOVERY_BRIEFING_FRESHNESS_DAYS` before meeting time. |
| `provenance` | object | yes | See §8. |

### 2.5 FollowUpSchedule (output of `follow-up-management`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `schedule_id` | UUID | yes | Internal ID. |
| `lead_id` | UUID | yes | |
| `trigger_type` | enum | yes | `not-now-with-date` / `not-now-no-date` / `out-of-office` / `nurture-park` / `re-engagement` / `meeting-no-show`. |
| `trigger_reply_id` | UUID \| null | conditional | Required for reply-driven triggers; null for cadence-completion or no-show. |
| `parsed_resume_date` | ISO date | yes | The date the resume touch is scheduled for. |
| `parse_method` | enum | yes | `explicit-reply-date` / `inferred-window` / `ooo-end-date-plus-one` / `default-60d` / `default-90d` / `tried-similar-failed-180d`. |
| `nurture_cadence_ref` | string \| null | conditional | `30-60-90-light` / `90-180-365-deep` / `meeting-no-show-rescue` / `null` for single-touch resumes. |
| `channel` | enum | yes | Same as original reply channel unless redirect detected. |
| `framework` | enum | yes | `resurrection` / `nurture-light` / `rescue-tone`. |
| `scheduled_touches` | array | yes | Each `{position, scheduled_for, channel, framework}` — handed off to channel skill. |
| `capacity_check_passed` | bool | yes | False → user must authorize over-cap or extend timeline. |
| `provenance` | object | yes | See §8. |

---

## 3. The 9-label reply taxonomy (definitive)

This is the canonical enumeration consumed by all function-4 skills. `reply-classification` owns it (writes); the other three consume specific subsets. Adding a 10th label requires updating this section AND every skill in the function in the same change set.

| # | Label | Definition | Embedded objection? | Dispatch target | Cadence-state effect |
|---|---|---|---|---|---|
| 1 | `positive` | Recipient expressed clear interest, agreement to next step, or proposed a meeting time. | Rare — possible if "yes, but…" | `discovery-call-prep` (when meeting requested); else `follow-up-management` for the agreed-upon next step | `exit-globally` (cadence done; pipeline stage advances) |
| 2 | `not-now` | Interest signaled but timing wrong. May or may not include a stated resume date. | Common — often timing-as-objection or "we're already using X" | `objection-handling-library` (if embedded objection); `follow-up-management` (always — to schedule resume) | `pause-with-resume` |
| 3 | `not-interested` | Hard no, no opening. May or may not name a reason (already-have, no-budget, no-need). | Common — most have a reason embedded | `objection-handling-library` (capture intel; do NOT auto-respond) | `exit-permanent` (12mo cooldown) |
| 4 | `wrong-person` | Recipient is not the right buyer/decision-maker. May name a referral. | Rare | `data-enrichment` (correct existing record + find named referral) | `exit-globally` on this recipient; routing to new contact starts a fresh cadence |
| 5 | `unsubscribe` | Explicit opt-out request ("remove me", "stop", "unsubscribe"). | Never | `none` (cadence-state change is the action) | `exit-permanent` AND **global cross-channel exit** |
| 6 | `out-of-office` | Auto-reply with return date. | Never | `follow-up-management` (resume after OOO end + 1 business day) | `pause-with-resume` |
| 7 | `referral` | Names a different person to contact (not "I'm not the right person" — that's `wrong-person`). | Never | `data-enrichment` (find the named contact) + `follow-up-management` (continue with original at lower priority) | `nurture-park` on original; new cadence on referred contact |
| 8 | `question` | Asks a specific question — often a soft objection or qualification ask. | Sometimes | `objection-handling-library` (treat as light objection) | `continue` (cadence proceeds while question is handled) |
| 9 | `unclear` | Reply doesn't fit any of the above with confidence ≥ floor. | Possibly | `manual-review` | `defer-manual` |

### 3.1 Pre-classification short-circuits

These bypass the LLM and write the label deterministically. Hard rule — pre-classify BEFORE LLM call:

- `Auto-Submitted` header present OR body contains "out of office" / "OOO" / "vacation responder" → `out-of-office` (confidence 0.99)
- Body contains regex-strong unsubscribe phrases (`\b(unsubscribe|remove me|stop|opt out|opt-out)\b`) → `unsubscribe` (confidence 0.95)
- Bounce auto-reply (5xx SMTP code in body, "delivery has failed" pattern) → NOT a reply event; routes back to channel skill (function-3 owns bounces, not function-4)

### 3.2 Multi-language rule

Classify in source language; always preserve `body_raw`. Translate only a one-sentence summary to English for operator-facing displays. Never silently translate the body. If language is unsupported by the classifier, default to `unclear` and route to manual review with a `[unverified — needs check: language]` provenance tag.

### 3.3 Multi-label edge case

Replies with two distinct intents ("not now AND we're already using X") are classified by the dominant intent (`not-now`) but `embedded_objection` captures the secondary signal (the competitor mention) for `objection-handling-library` to act on.

---

## 4. The 12-objection library (canonical with framework mapping)

This is the canonical enumeration consumed by `objection-handling-library` and referenced by `reply-classification.embedded_objection`. The library is closed by default — the 12 categories cover 80%+ of B2B outbound objections (per the original house authoring assumption); patterns that don't match get tagged `new-objection-pattern` and queued for library refresh, never invented on the fly.

| # | Label | Pattern | Default framework | Cadence action |
|---|---|---|---|---|
| 1 | `already-using-competitor` | "We already use X" — names a known competitor | `counter-position` (Dunford) | `nurture-90d` (competitor switches rarely happen sooner) |
| 2 | `no-budget` | "We don't have budget for this right now" | `re-discovery` (Bosworth — surface pain bigger than budget) | `nurture-90d` AND flag `lead-scoring` re-tier (BANT update) |
| 3 | `no-authority` | "I'd need to check with my boss / committee / VP" | `re-discovery` + champion-build ask | `pause-with-resume` after authority-conversation date |
| 4 | `no-need-now` | "We're not looking at this right now" — general | `feel-felt-found` (acknowledge timing; reframe with industry pattern) | `nurture-90d` |
| 5 | `bad-timing` | "We're focused on X right now / Q1 / after the holidays" — explicit window | `time-shift` (lock specific resume date) | `pause-with-resume` per stated date |
| 6 | `happy-with-status-quo` | "We're happy with how things are" | `re-discovery` (probe for hidden pain; status quo bias is real) | `nurture-90d` |
| 7 | `tried-similar-failed` | "We tried X, didn't work" | `re-discovery` (what specifically failed; capture for `competitive-intelligence`) | `nurture-180d` |
| 8 | `too-expensive` | "Your pricing seems high" or "This is out of our budget for the value" | `re-discovery` (anchor to ROI / pain cost) + counter-position | `nurture-60d` AND flag `revenue-forecasting` ACV reality-check |
| 9 | `too-small` | "We're not your target / we're too small for this" | `feel-felt-found` (or honest disqualify) | `exit-permanent` if genuinely sub-ICP; else `nurture-90d` |
| 10 | `send-me-email` | "Send me information at X@Y" — polite redirect | `time-shift` (one-line confirm + send) | `continue` (cadence proceeds; one resource-only touch) |
| 11 | `wrong-person` | "I'm not the right person — talk to Y" — same as label-4 in §3, but stated as objection | n/a (route to `data-enrichment`) | `exit-globally` on this recipient |
| 12 | `compliance-security-blocker` | "We can't onboard new vendors without security review / SOC 2 / vendor approval" | `time-shift` + supply security collateral | `pause-with-resume` after security-review window; `discovery-call-prep` (security-prep mode) on resume |

### 4.1 Framework-to-objection routing rule

Each library entry has a default framework but the matching skill MAY pick a different framework when context warrants (rep override, specific recipient profile). If the match falls below the §5 floor (0.7), do NOT pick a framework — surface as `new-objection-pattern` and route to manual.

### 4.2 New-objection-pattern handling

When ≥3 unmatched objections accumulate within a 30-day window (counted across `objection-handling-library` runs), `objection-handling-library` emits a library-refresh recommendation with the candidate pattern name and example replies. Library expansion is a versioned change — bumping the library updates this section AND every skill that consumes the labels in the same pass.

---

## 5. Confidence floors

Two distinct floors operate at different stages. Both are configurable via env; both default to a value that prioritizes "manual review > silent wrong action".

| Floor | Default | Where used | What "below floor" means | Env var |
|---|---|---|---|---|
| **Classification floor** | **0.75** | `reply-classification` LLM output | Reply routes to manual review queue; LLM's best guess + rationale surfaced for human override. NEVER auto-acts. | `REPLY_CLASSIFICATION_CONFIDENCE_FLOOR` |
| **Objection match floor** | **0.7** | `objection-handling-library` LLM-backed match against 12-library | `new-objection-pattern` flag; route to manual response; collect for library refresh. NEVER synthesizes a "library response" without library backing. | `OBJECTION_MATCH_CONFIDENCE_FLOOR` |

### 5.1 Why two floors instead of one

Classification (9-label taxonomy) is a coarser problem than objection-matching (12-library). The former's labels are well-separated in semantic space (`positive` vs `not-interested` is rarely ambiguous); 0.75 is achievable in routine traffic. The latter often has overlap (`no-budget` vs `too-expensive` vs `tried-similar-failed` can all surface in the same reply); 0.7 is calibrated to surface secondary matches when within 0.15 of primary.

### 5.2 Override discipline

A single user override (e.g., "trust the LLM at 0.65 for this batch") is a one-time confirm, not a config change. Never lower the floor in a config file; never exceed without explicit user authorization in the run record. The run record carries the override fact + reason for traceability.

### 5.3 Confidence calibration drift

If the same reply (same `dedup_key`) produces materially different classifications across runs, calibration has drifted. The skill must seed the LLM call when reproducibility matters and surface drift in the `interaction:research` run record.

---

## 6. Routing logic (which label / objection class → which next skill)

This table is the single source of truth for cross-skill dispatch within function-4. Embedding the routing here (rather than in each skill) prevents drift when one skill is updated.

| From | To | Trigger | Inputs to carry forward |
|---|---|---|---|
| `reply-classification` | `discovery-call-prep` | `label = positive` AND meeting requested OR confirmed | `reply_id`, `parent_touch_id`, `lead_id`, proposed meeting time, embedded context |
| `reply-classification` | `objection-handling-library` | `label ∈ {not-now, not-interested, question}` AND `embedded_objection != null` | `reply_id`, `embedded_objection`, `parent_cadence_id`, `lead_id`, `prior_cadence_context` |
| `reply-classification` | `follow-up-management` | `label ∈ {not-now, out-of-office}` (always) — to schedule resume | `reply_id`, `parsed_resume_date` (if any), `lead_id`, channel of original reply |
| `reply-classification` | `data-enrichment` (function-2) | `label ∈ {wrong-person, referral}` | `reply_id`, named referral (if any), original recipient `lead_id` |
| `reply-classification` | manual-review queue | `confidence < 0.75` OR `label = unclear` | full reply + LLM best guess + rationale |
| `objection-handling-library` | `competitive-intelligence` (function-1) | competitor mention captured | competitor name, reply context, parent reply id, date |
| `objection-handling-library` | `revenue-forecasting` (function-6) | pricing pushback captured | pricing concern verbatim, reply id, recipient ICP tier |
| `objection-handling-library` | `icp-refinement-loop` (function-6, planned) | persistent pain pattern OR ≥3 unmatched objections | pattern excerpt, frequency, sample replies |
| `objection-handling-library` | `discovery-call-prep` | `compliance-security-blocker` objection AND interest signal in same reply | reply, security-objection text, recipient context |
| `objection-handling-library` | `lead-scoring` (function-2) | `no-budget` objection (BANT update) | reply, ICP tier, recommended re-score |
| `objection-handling-library` | `follow-up-management` | every matched objection that warrants resume | match label, cadence action, recommended resume window |
| `discovery-call-prep` | `pipeline-stages` (function-5) | post-call hand-off (after the call happens) | meeting outcome (advance / stall / disqualify), MEDDPICC delta |
| `discovery-call-prep` | `objection-handling-library` | objection surfaced live in call needing deeper response | live-objection text, recipient context |
| `discovery-call-prep` | `handoff-protocol` (function-5) | founder hand-off from SDR cadence | full briefing + cadence history |
| `follow-up-management` | `cold-email-sequence` (function-3) | resume touch on email channel | scheduled date, lead, framework (`resurrection`) |
| `follow-up-management` | `linkedin-outreach` (function-3) | resume touch on LI channel | scheduled date, lead, framework |
| `follow-up-management` | `cold-calling` (function-3) | resume touch on phone channel | scheduled date, lead, framework |
| `follow-up-management` | `multi-channel-cadence` (function-3) | capacity overrun | over-cap volume, suggested timeline extension |
| `follow-up-management` | `lead-scoring` (function-2) | nurture aging beyond 12mo | recommend re-tier or archive |

When two routes could plausibly fire (e.g., a `not-now` reply with embedded objection AND a stated resume date), all applicable routes fire in parallel — the receiving skills handle their own slice. `follow-up-management` schedules the resume; `objection-handling-library` produces the response variants. They do not block each other.

---

## 7. Cadence-state effects (what each label does to the person record's `cadence_state`)

The `cadence_state` field on the person record (introduced in function-3, see `function-3-conventions.md` §2 Touch + active_cadence_id PATCH) is the source-of-truth for whether a recipient is currently in active outreach. Function-4 OWNS the transitions out of `active`.

| `cadence_state` value | Meaning | Set by |
|---|---|---|
| `active` | In an active cadence; touches scheduled per the cadence definition | function-3 (set at cadence start) |
| `paused` | Pause without exit; resume scheduled. `next_followup_at` populated. | function-4 (`reply-classification` on `not-now` / `out-of-office`; `follow-up-management` finalizes the resume date) |
| `nurture` | Active long-cycle nurture (30-60-90 or 90-180-365 cadence) | function-4 (`follow-up-management` after a `not-now` without imminent resume, or post-`not-interested` long-tail re-engagement) |
| `resurrection` | One-touch resurrection scheduled (function-3 cold-email-sequence touch 7) | function-4 (`follow-up-management` for `not-now` with stated date) |
| `exited-prospect` | Out of cold cadence because they engaged (`positive`) — handed to discovery / pipeline | function-4 (`reply-classification` on `positive`) |
| `exited-not-interested` | 12-month cooldown; no outreach until cooldown ends | function-4 (`reply-classification` on `not-interested`) |
| `exited-unsubscribed` | Permanent global cross-channel exit | function-4 (`reply-classification` on `unsubscribe`) |
| `exited-wrong-person` | This recipient is wrong; new cadence may start on a referred contact | function-4 (`reply-classification` on `wrong-person`) |
| `archived` | Long-tail (>365d nurture aged out); reach via re-engagement campaign only | function-4 (`follow-up-management` archive recommendation) |

### 7.1 Hard rules per cadence-state transition

- **Any transition out of `active`** triggers a `person` PATCH carrying `last_reply_class`, `last_reply_at`, `cadence_state`, `next_followup_at` (or null), and the run id.
- **Global cross-channel exit on `unsubscribe`** — exits ALL active cadences across email, LI, phone, SMS for this recipient. Courteous baseline + GDPR-aligned even where not legally required.
- **`exited-not-interested` cooldown is 365 days** (12 months) by default; configurable per ICP via `NOT_INTERESTED_COOLDOWN_DAYS`. Re-engagement after cooldown is a `follow-up-management` decision, not automatic.
- **`paused` without `next_followup_at`** is a contract violation. If `follow-up-management` cannot parse a resume date, default to 60d AND tag the parse provenance as `[unverified — needs check]` AND surface for user confirmation if Tier-1.
- **`resurrection` is single-touch by default**. If the resurrection touch generates no reply, the cadence-state transitions to `archived` after 30d, NOT to a new cadence.
- **No skill OTHER THAN function-4 may transition cadence-state out of `active`.** Function-3 only sets it INTO `active` at cadence start; function-5+ reads it but does not write.

### 7.2 Resume date parsing rules (drives `paused` resume timing)

Owned by `follow-up-management`. Provenance per parsed value:

- Explicit ISO date in reply ("March 15, 2027", "2027-03-15") → `[verified: reply-text]`.
- Quarter phrase ("Q1 2027") → first business day of mid-quarter ("Q1 2027" → 2027-01-15) → `[verified: reply-text + agent-rule]`.
- Holiday phrase ("after the holidays") → first business day post Jan 1 (US default; locale-aware if known) → `[verified: reply-text + agent-rule]`.
- Season phrase ("late spring", "early summer") → first business day mid-season → `[unverified — needs check]`.
- Month-only ("in May") → first business day of stated month, current year if forward / next year if past → `[verified: reply-text + agent-rule]`.
- "Next month" / "next quarter" → first business day next calendar month/quarter → `[verified: reply-text + agent-rule]`.
- No date phrase → default 60d for `not-now`; 90d for `tried-similar-failed`; OOO end + 1 business day for `out-of-office`.

Holiday-window collisions (e.g., "Q1 2027" arriving Dec 24) shift to first post-holiday business day, not the literal mid-quarter date.

---

## 8. Anti-fab tagging (function-4-specific: reply text + classification both need provenance)

Per CLAUDE.md universal rule, every named entity in any function-4 output (recipients, companies, parsed dates, classification labels, objection text, response variants, MEDDPICC slot content, scheduled touches) MUST carry one of four explicit provenance tags. Untagged = contract violation. Function-4's risk profile is distinct from upstream functions — it operates on what real humans wrote, then writes interpretations on top.

| Tag | Meaning | Function-4 typical use |
|---|---|---|
| `[user-provided]` | Supplied by the user OR a real human's verbatim input — agent reproduces, doesn't invent | Reply body text always tags `[user-provided]` (came from a real human). Quoted reply excerpts in briefings. Stated resume dates explicit in reply. |
| `[verified: <source>]` | Checked via a named tool / classifier with a run id | Classification labels: `[verified: llm-classifier:run_<id>]` with confidence. Objection matches: `[verified: llm-match:run_<id>]`. Verified prior-touch references: `[verified: cadence-history:tch_<id>]`. |
| `[hypothetical]` | Explicitly illustrative, not claimed real. ALLOWED only in worked examples | Worked-example fictional entities (Stitchbox, Esme Liang, Helio, etc.) tagged inline at first mention per CLAUDE.md "Worked Example tagging" rule. |
| `[unverified — needs check]` | Agent's best inference; do not act on without human verification | Inferred MEDDPICC slot content not traced to a Lead-record field or reply text. Inferred resume-date windows ("late spring"). Low-confidence classifications (<0.75) routed to manual. |

### 8.1 The two-layer reply provenance rule

This is the function-4-specific anti-fabrication innovation. Every reply-derived artifact carries TWO provenance dimensions:

1. **The reply text itself** is `[user-provided]` because it came from a real human via the channel (email, LI, SMS, call). It is never `[verified]` — verification implies a research check, but the reply IS the source of truth.
2. **The interpretation on top** (classification label, objection match, parsed date, response variant) is `[verified: <classifier>]` with confidence, OR `[unverified — needs check]` when below floor.

Skills MUST emit both layers in the run record. A briefing line "Esme [verified: data-enrichment] mentioned ROI concerns [user-provided]" is NOT correct — the mention claim is an interpretation, so it should read: "Esme [verified: data-enrichment] mentioned ROI concerns [verified: reply-text rpl_<id>]" — with the actual reply text quoted as the underlying `[user-provided]` fact.

### 8.2 Tool-grounding rule

If no LLM classifier is available at runtime (no `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`), `reply-classification` and `objection-handling-library` cannot operate in their primary modes. Hard rule — they MUST NOT degrade to "best guess without classifier" — they degrade to "pre-classification short-circuits only" (auto-reply / unsubscribe / bounce) and route everything else to manual review.

### 8.3 Worked-example tagging convention

Every fictional entity in a function-4 worked example carries the tag inline at first mention (per CLAUDE.md universal). Subsequent uses within the same example block MAY be untagged once the section opens with a block-level disclaimer. Concretely: WorkflowDoc, Stitchbox, Esme Liang, Helio, Volaris, Tashia, Nina Park — all tagged `[hypothetical]` on first mention in any function-4 worked example.

### 8.4 Push-to-CRM hygiene routing (per CLAUDE.md universal)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (reply text) + `[verified: <classifier>:run_<id>]` (interpretation) | Standard mapping per §9. |
| `[unverified — needs check]` (any layer) | Pushes ONLY as `interaction:research` with `#unverified #review-required #<skill-name>` tags. Person PATCH deferred until manual review confirms. |
| `[hypothetical]` | Never pushes. Local artifact only. |

---

## 9. Push-to-CRM conventions (entity routing per skill)

Function-1 pushed research. Function-2 pushed records (companies, people). Function-3 pushed touches (sent records). Function-4 pushes a mix: classifications and objections are `interaction:reply` / `interaction:research`; cadence-state changes are `person` PATCH; briefings are `interaction:research`.

### 9.1 Entity routing per skill

| Skill | Primary push | Secondary push |
|---|---|---|
| `reply-classification` | `interaction:reply` per classified reply (label + confidence + rationale + dispatched-to) | PATCH on `person` (`last_reply_class`, `last_reply_at`, `cadence_state`, `next_followup_at`); `interaction:research` for run records, manual-review entries, and competitor/objection signals |
| `objection-handling-library` | `interaction:reply-response` per matched objection (library label + variants + cadence action) | PATCH on `person` (cadence_state); `interaction:research` for new-objection-pattern flags, captured intel, run records |
| `discovery-call-prep` | `interaction:research` per briefing (full ≤450-word briefing + meeting context) | PATCH on `person` (`discovery_briefing_at`, `next_meeting_at`, `next_meeting_channel`); separate `interaction:research` for MEDDPICC snapshot + pre-staged objections |
| `follow-up-management` | `interaction:research` per scheduled resume / nurture (parsed date + flow + framework + scheduled-touch ref) | PATCH on `person` (`next_followup_at`, `nurture_state`, `cadence_state`, `last_no_show_at`); `interaction:research` for run records and meeting-no-show triggers |

### 9.2 Source tag

Every push carries `source: "skill:<skill-name>:v<version>"` (e.g., `skill:reply-classification:v2.0.0`). The push API uses this for provenance and dedup-on-replay. The classification run id and objection match run id appear in `relevance` for replay traceability.

### 9.3 Named-product vs. non-product hygiene (per CLAUDE.md rule #6)

Function-4 rarely emits new `company` / `person` records — those are upstream's job. The exception is the `referral` label, where a new named contact may need a new `person` record (handed to `data-enrichment` to verify before push). Abstractions, classifications, and run records ALWAYS push as `interaction` records, never as fake `company` / `person` entities.

### 9.4 Reply dedup on replay

Replies are dedup'd by `dedup_key = <lead_id>:<channel>:<sha1(body_normalized)[:12]>`. Same reply received twice (e.g., email + email-forwarded-to-CRM) classifies once and pushes once. Replays of the same classification run id push as updates to the same `interaction:reply`, not as new records.

### 9.5 Cross-channel cadence-state PATCH atomicity

When `unsubscribe` triggers global cross-channel exit, the `person` PATCH carries `cadence_state: exited-unsubscribed` AND a list of `cadences_exited_ids: [...]` for audit. The PATCH is a single transaction — never partial.

### 9.6 When NOT to push

- Reply already classified within 1h (dedup) — push the dedup record only, not a new classification.
- Bounce auto-reply — route to channel skill (function-3); not a reply event for function-4.
- Drafts of LLM responses or briefings (not yet user-confirmed for high-stakes recipients) — local artifact, do not push.
- Meeting cancelled — push cancellation note as `interaction:research` with `#meeting-cancelled`; do not push briefing.
- Capacity exceeded with no user authorization — push run record with `#blocked-capacity`; no per-recipient schedules.
- `[unverified]` — see §8.4.
- `[hypothetical]` — never.

---

## 10. Inheritance from function-1, 2, 3 (what fields each skill reads)

Function-4 is downstream of three full functions. Every skill declares its inheritance in `## Inputs Required`. Hard rule: function-4 will refuse to act if a gating upstream artifact is missing — reply triage without a Lead record is data-stranded.

| Function-4 skill | Function-1 input | Function-2 input | Function-3 input | Hard gate? |
|---|---|---|---|---|
| `reply-classification` | n/a (label semantics defined here, not upstream) | Lead record (score, tier, signals, prior reply history) | Touch record (parent_touch_id, parent_cadence_id, cadence context) | YES — refuse if no Lead or no parent Touch |
| `objection-handling-library` | ICP P-T-O chain + Pain language (from `icp-definition`); Positioning message house (from `positioning-strategy`); Counter-positioning anchors (from `competitor-analysis`) | Lead record + score + tier | Cadence + Touch context (which Touch this is replying to; channel-isolation rule from f3 §10) | YES on ICP P-T-O for re-discovery framework; YES on positioning house for counter-position framework |
| `discovery-call-prep` | ICP P-T-O chain (icp-definition); Positioning message house; Competitor context + battle cards (`competitor-analysis` + `competitive-intelligence`) | Full Lead schema; data-enrichment hooks; lead-scoring score + tier rationale | Cadence + every Touch sent + every reply received | YES on full Lead + cadence/reply thread; refuse if briefing freshness > 48h at call time and re-prep cannot run |
| `follow-up-management` | n/a (resume rules defined here) | Lead record (score, tier, prior cadence + reply history) | Cadence + Touch context; per-channel weekly caps (f3 §6); calendar/scheduling-tool access (function-3-adjacent) | YES on lead + reply context for reply-driven triggers |

If `lead-scoring` (function-2) has not run, function-4 skills can still classify replies but flag downstream routing as `confidence: low` and tag entities `[unverified — needs check]` aggressively. If `icp-definition` (function-1) has not run, `objection-handling-library`'s re-discovery and counter-position frameworks degrade to `feel-felt-found` only.

### 10.1 Reply-back-to-Touch linkage

Every Reply has a `parent_touch_id` from function-3. The reverse linkage is also written: function-3's Touch record's `metrics.replied_at` and `metrics.reply_classification` fields are populated by `reply-classification` (a PATCH back into the function-3 Touch record). This is the only field function-4 writes into function-3's schema.

### 10.2 Channel-isolation rule (from function-3 §10) carried forward

Don't reference the channel the objection came in on within the response on a different channel. If a `not-now` reply arrived via LinkedIn, the response variants `objection-handling-library` produces for the LinkedIn channel may reference "your message" / "your reply"; the email-channel resume touch from `follow-up-management` MUST NOT reference the LinkedIn reply by channel — it can reference the topic, not the medium.

### 10.3 Cadence-state read consistency

`cadence_state` is read by function-3 (to decide "should this Touch send?") and written by function-4 (to transition out of `active`). To prevent races, function-3 reads `cadence_state` immediately before send and aborts if not `active`. Function-4's PATCH is the source of truth.

---

## 11. Open conventions deferred to function-5+

These are not function-4's problem but worth flagging so we don't accidentally encode the wrong assumption:

- **Pipeline stage transitions.** Function-4's `positive` label is a trigger for `pipeline-stages` (function-5) to advance the stage. The MEDDPICC slot population from `discovery-call-prep` informs the Discovery → Proposal stage threshold (`pipeline-stages-v2` §Quick Reference: ≥5 of 8 MEDDPICC slots populated for stage advance per the 8-slot fix). Function-4 does NOT write stage transitions — it produces the substrate function-5 reads.
- **Handoff-protocol SAL acceptance.** Function-4's `discovery-call-prep` produces the briefing that `handoff-protocol` (function-5) reads to evaluate procedural / clerical / definitional acceptance per the SiriusDecisions categorical-rejection model. Function-4 does NOT define SAL acceptance criteria.
- **CRM hygiene.** Function-4 PATCHes `person` records with cadence-state changes. `crm-hygiene` (function-5) audits the Wang & Strong Accuracy / Completeness / Timeliness / Consistency dimensions across the CRM. Function-4 must produce hygienic PATCHes (every required field populated, provenance per field) but does not run the audit.
- **Conversation intelligence.** Post-call analysis of recorded discovery calls, MEDDPICC slot completion deltas, sentiment, and talk-listen ratio is `conversation-intelligence` (function-5, planned). `discovery-call-prep` produces the pre-call briefing; `conversation-intelligence` produces the post-call retrospective. The two skills share the MEDDPICC slot schema defined in §2.4.
- **Customer feedback analysis.** Function-4's `not-interested` replies with stated loss reasons feed `customer-feedback-analysis` (function-6) for win/loss thematic clustering and forces-of-progress analysis (push / pull / habit / anxiety per Moesta). Function-4 captures the verbatim loss-reason text in `embedded_signals`; function-6 owns the clustering.
- **Channel performance attribution.** Reply-rate metrics computed at the campaign level (`campaign-management`, function-3) flow into `channel-performance` (function-6) for marginal-CAC analysis. Function-4 does NOT compute reply rates — it produces the per-reply substrate that the rate is computed on.

---

## 12. WorkflowDoc worked-example continuity

Function-1 used WorkflowDoc as the company being analyzed. Function-2 flipped the camera: WorkflowDoc as the seller prospecting. Function-3 kept the seller frame: WorkflowDoc executing outreach. Function-4 keeps the seller frame: **WorkflowDoc triaging the replies its function-3 cadences generated**. Worked examples chain across skills:

1. `reply-classification` (function-4) → 30 inbound replies from the WorkflowDoc Tier-1 cadence → triaged into 9-label distribution → dispatched
2. `objection-handling-library` (function-4) → matches embedded objections (Esme's "we're already using Guru" → `already-using-competitor` + counter-position framework + 3 variants)
3. `discovery-call-prep` (function-4) → produces 1-page briefing for Esme's Tuesday discovery call → 8-slot MEDDPICC populated from upstream intel
4. `follow-up-management` (function-4) → schedules resume touches for the 12 not-now replies; OOO + no-show flows for edge cases

The fictional cast is consistent across the function-4 worked examples:

- **Esme Liang** [hypothetical] — VP Customer Support @ Stitchbox; replies positively to Touch 2 and books a discovery call. Featured in the chained worked example for `discovery-call-prep`.
- **Stitchbox** [hypothetical] — 180-employee Series B SaaS, the canonical Tier-1 prospect.
- **Helio** [hypothetical] — secondary Tier-2 prospect; replies `not-now` with "Q1 2027" — used in `follow-up-management` resume-parsing example.
- **Volaris** [hypothetical] — Tier-2 prospect; replies `not-interested` with embedded `tried-similar-failed` objection → used in `objection-handling-library` ROI/proof-thin worked example.
- **Tashia** [hypothetical] — Stitchbox VP champion; appears in post-call intel.
- **Guru** [hypothetical-as-competitor] — competitor named in Esme's reply; counter-positioning anchor used across `objection-handling-library` and `discovery-call-prep`. (Real product name; treated as `[hypothetical]` for worked-example purposes.)

Every fictional entity tagged inline at first mention in each skill's worked example per CLAUDE.md "Worked Example tagging" rule. The inter-skill chain demonstrates real cross-skill data flow: the same reply that `reply-classification` labels as `not-now` with embedded objection drives both `objection-handling-library` (response) and `follow-up-management` (resume schedule) in parallel.

---

## Document version

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-05-04 | Initial draft alongside the function-4 LITE refresh (F4-OH1, F4-DC1 attribution + MEDDPICC fixes). 9-label taxonomy + 12-objection library + 8-slot MEDDPICC canonized. |
