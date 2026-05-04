# Function 3 — Outreach Execution Conventions

This file is the shared rules document for every skill in `function-3-skills/`. All six skills (`email-infrastructure-setup`, `cold-email-sequence`, `linkedin-outreach`, `cold-calling`, `multi-channel-cadence`, `campaign-management`) MUST reference this document by name in their `## Inputs Required` and `## Guardrails` sections rather than redefining the schemas, capacity caps, or compliance rules locally.

> *The worked examples in function-3 skills use a fictional product (WorkflowDoc) for illustration — same product as function-1, in a third role: WorkflowDoc as the seller actively executing outreach against the leads function-2 sourced and scored. The schemas, cadence patterns, copy frameworks, and procedures are vertical-agnostic and apply to any B2B GTM context.*

---

## 1. Why this file exists

Function-1 produced documents (briefs, canvases). Function-2 produced records (Leads, all conforming to one schema). Function-3 produces **executions** — actual touches sent to actual humans. That changes four things:

- **Heterogeneous artifacts, but one shared object.** Each skill produces a different artifact (DNS records, email copy, LinkedIn message, call script, cadence config, campaign metrics). The shared atomic unit is the **Touch** (one outreach event). Cadence orchestrates touches; campaign-management monitors them.
- **Compliance is the dominant constraint.** Google + Microsoft's Feb 2024 bulk sender requirements, Apple Mail Privacy Protection, CAN-SPAM, GDPR, TCPA, CASL, LinkedIn ToS — these all bite at execution time, not list time.
- **Deliverability is upstream of everything.** Perfect copy from a domain with bad reputation gets zero replies. `email-infrastructure-setup` is foundational.
- **Fabrication risk is worse.** Function-2 could fabricate companies (caught by provenance rules). Function-3 can fabricate facts *about real prospects in copy sent to them*. Defense: the personalization-hook contract from `data-enrichment` is enforced — copy MUST refuse to ship using an `[unverified — needs check]` hook.

---

## 2. Shared schemas — Touch, Cadence, Campaign

### 2.1 Touch (one outreach event)

| Field | Type | Required | Notes |
|---|---|---|---|
| `touch_id` | UUID | yes | Internal ID. Generated when scheduled. |
| `campaign_id` | UUID | yes | Parent campaign run. |
| `cadence_id` | UUID | yes | The cadence this touch belongs to. |
| `lead_id` | UUID | yes | From function-2 Lead schema. |
| `channel` | enum | yes | `email` / `linkedin-connect` / `linkedin-message` / `linkedin-inmail` / `call` / `voicemail` / `sms` |
| `touch_type` | enum | yes | `opener` / `follow-up-1` / `follow-up-2` / `break-up` / `reply-handler` |
| `sequence_position` | int | yes | Position within the cadence (1-indexed). |
| `scheduled_for` | ISO datetime | yes | Includes timezone. |
| `sent_at` | ISO datetime | when sent | Wall-clock send time. |
| `content` | object | yes | See content sub-schema. |
| `status` | enum | yes | `draft` / `scheduled` / `sent` / `bounced` / `replied` / `unsubscribed` / `opted-out` / `error` |
| `metrics` | object | when sent | See metrics sub-schema. |
| `sender` | object | yes | `email` / `linkedin_handle` / `phone_e164` + `reputation_score` |
| `compliance` | object | yes | See compliance sub-schema. |
| `provenance` | object | yes | Per-field tags per CLAUDE.md anti-fab rule. |

**`content` sub-schema** (channel-specific):
```yaml
# email
subject: <string, ≤8 words for cold>
body: <string, target 25-125 words>
word_count: <int>
personalization_hook_used: <ref to data-enrichment hook source_url>
framework: ccq | aida | rta | bant-opener | custom
mobile_formatted: <bool — bullets, short paragraphs, ≤2-line opener>

# linkedin-connect / linkedin-message
note: <string, ≤300 chars for connection request, no link>
hook_text: <verbatim from data-enrichment>
framework: ccq | warm-intro | event-based | content-engagement

# call / voicemail
opener_script: <string, 9-second opener>
discovery_questions: [<string>, ...]
voicemail_script: <string, ≤15 seconds spoken>
gatekeeper_handler: <string, response patterns>
framework: cc20 | sandler-pain-funnel | tactical-empathy
```

**`metrics` sub-schema** (populated post-send):
```yaml
opened_at: [<ISO>, ...]   # NOTE: noisy due to Apple MPP; report, don't optimize
clicked_at: [<ISO>, ...]
replied_at: <ISO>
reply_classification: positive | not-now | not-interested | wrong-person | unsubscribe-request | bounce-auto-reply
bounced_at: <ISO>
bounce_type: hard | soft | spam-block
unsubscribed_at: <ISO>
complaint_at: <ISO>   # spam button hit
```

**`compliance` sub-schema**:
```yaml
recipient_jurisdiction: us | eu | uk | ca | au | other
gdpr_basis: legitimate-interest | consent | not-applicable
has_unsubscribe: <bool, required for email + bulk SMS>
has_physical_address: <bool, required for US email>
list_unsubscribe_header: <string for email — RFC 8058 one-click>
honors_dnc: <bool, for calls>
honors_quiet_hours: <bool>
recipient_local_timezone: <string>
```

### 2.2 Cadence (the sequence template)

| Field | Type | Notes |
|---|---|---|
| `cadence_id` | UUID | |
| `name` | string | Human-readable (e.g. "tier-1-multi-channel-21d"). |
| `description` | string | What this cadence is for. |
| `target_segment` | object | ICP tier filter, signal filter, geography filter. |
| `total_touches` | int | Default 5–7 for cold; 3 for warm follow-up. |
| `duration_days` | int | Default 14–21 days. |
| `touches` | array | See `touch_template` sub-schema. |
| `exit_conditions` | array | `reply-positive` / `reply-negative` / `bounce` / `unsubscribed` / `manual-stop` / `cap-hit`. |
| `gdpr_variant` | bool | If true, opt-out + legitimate-interest language injected into every email touch. |
| `branch_rules` | array | E.g. "if Touch 2 (LinkedIn connect) accepted → skip Touch 4 (cold call)". |

**`touch_template` sub-schema**:
```yaml
position: <int>
day_offset: <int from cadence start>
hour_local: <int 9-17 default — quiet hours respected>
channel: email | linkedin-connect | ...
touch_type: opener | follow-up-1 | break-up | ...
template_ref: <skill-name + framework — points to which skill produces the copy>
fallback_action: skip | manual-task | swap-channel
```

### 2.3 Campaign (the run-level container)

| Field | Type | Notes |
|---|---|---|
| `campaign_id` | UUID | |
| `name` | string | |
| `purpose_tag` | string | E.g. "q2-tier1-vp-marketing-burst". |
| `cadence_id` | UUID | |
| `recipients` | array<lead_id> | |
| `recipient_count` | int | |
| `state` | enum | `draft` / `active` / `paused` / `completed` / `aborted` |
| `started_at`, `ended_at` | ISO | |
| `caps_applied` | object | Snapshot of capacity caps at launch time. |
| `sender_pool` | array | Senders rotated through to spread load. |
| `metrics_summary` | object | See below. |
| `adjustments_log` | array | Every `campaign-management` decision (pause, slow-down, swap copy). |

**`metrics_summary`** (campaign-management writes; **reply rate is primary**):
```yaml
total_touches_sent: <int>
reply_rate: <float>           # PRIMARY metric
positive_reply_rate: <float>  # downstream truth
meeting_rate: <float>         # ground truth
bounce_rate: <float>          # MUST stay <0.05 (5%); hard pause at 0.05
complaint_rate: <float>       # MUST stay <0.003 (0.3%); hard pause at 0.003
unsubscribe_rate: <float>
open_rate: <float>            # REPORTED but never optimized (Apple MPP)
```

---

## 3. Channel adapter contract

Channel-specific sending skills (`cold-email-sequence`, `linkedin-outreach`, `cold-calling`) MUST expose three named operations — analogous to function-2's `discover/pull/normalize` but for outreach:

```
prepare(lead, cadence_position, sender) → Touch[draft] + readiness_check + estimated_capacity_use
send(touch_draft) → Touch[sent] + delivery_metadata + warnings
track(touch) → Touch[updated metrics] + status_changes
```

- **`prepare`** is mandatory before `send`. It runs precondition checks (deliverability for email; account safety for LinkedIn; DNC for calls) and surfaces warnings before any send happens.
- **`send`** must respect capacity caps. Aborts gracefully when a cap would be exceeded; queues for next eligible window.
- **`track`** updates the Touch with delivery metadata, reply classification feeds, and reputation-impact signals.

The skill body wraps these three with mode selection (§4), provenance tagging (§10), compliance gating (§9), and the push-to-CRM step (§11).

---

## 4. Three-mode pattern (adapted for outreach)

Where function-2's three modes were about *getting data in*, function-3's three modes are about *getting touches out*:

### 4.1 API mode
The outreach tool's API key is set in `.env` (Smartlead, Instantly, HeyReach, JustCall, etc.). Skill creates the campaign / sequence directly via the tool's API; touches are sent by the tool's infrastructure.

### 4.2 Manual mode
The user has a tool seat but no API key. Skill emits the cadence config, copy templates, and per-touch send instructions ready to paste into the tool's UI. User executes touches manually inside the tool; status comes back via export.

### 4.3 BYO mode (manual send / native send)
No outreach tool. Skill outputs copy + a per-touch runbook for native sending — Gmail/Outlook drafts for email, LinkedIn UI for LI, dialer for calls. **This is the most common state for early-stage founder-led outreach and must work well.** Status feedback comes from user manual marking.

Procedure entry pattern (every channel skill's first or second step):
```
if api_key set       → API mode
elif user has access → manual mode (paste-ready cadence config + copy)
elif native sending  → BYO mode (per-touch runbook)
```

`email-infrastructure-setup` is partly mode-agnostic (DNS records and warmup are the same across modes); it has a fourth output — "what tool to pick" — when the user has none.

---

## 5. Routing logic — when to use which channel skill

| Situation | Skill | Why |
|---|---|---|
| First touch to a Tier-1 prospect with `personalization_hook [verified]` | `cold-email-sequence` | Cheapest scalable channel; hook makes it sharp. |
| Prospect's `email_status` is `risky`/`catch-all-domain` but has `linkedin_url [verified]` | `linkedin-outreach` (connect first) | Email path damaged; LI is the alternate. |
| Prospect has `phone_status: mobile [verified]` AND scored Tier-1 SAL-eligible | `cold-calling` | Live-conversation conversion 3–5x email; gated on phone quality. |
| Mixed channels needed within one cadence | `multi-channel-cadence` | Composes 2–3 channel skills into a 14–21 day flow. |
| Active campaign monitoring | `campaign-management` | Ongoing — reads metrics, makes pause/swap decisions. |
| Domain not yet warmed / DNS not aligned | `email-infrastructure-setup` | Foundation; gates all email skills. |

When two channels could plausibly run, prefer the one that respects more of the recipient's autonomy: email > LinkedIn-message > LinkedIn-connect-with-note > call. Calls get parked for highest-confidence prospects only.

---

## 6. Capacity caps & sending hygiene

Function-3 is **capacity-bound, not credit-bound**. Skills MUST honor:

| Cap | Default | Notes |
|---|---|---|
| `SENDS_PER_DOMAIN_PER_DAY_CAP` | 30 | Absolute ceiling 50. New domains start at 5 and ramp. |
| `SENDS_PER_MAILBOX_PER_DAY_CAP` | 30 | Per individual mailbox. |
| `LINKEDIN_CONNECTS_PER_WEEK_CAP` | 80 | LI's soft cap is ~100; stay below. |
| `LINKEDIN_MESSAGES_PER_WEEK_CAP` | 200 | To existing connections. |
| `LINKEDIN_INMAIL_PER_MONTH_CAP` | 50 | Depends on Sales Nav seat tier. |
| `CALLS_PER_REP_PER_DAY_CAP` | 80 | Warn above 100; productive ceiling. |
| `VOICEMAILS_PER_REP_PER_DAY_CAP` | 40 | |
| `CAMPAIGN_TOTAL_RECIPIENTS_CAP` | 500 | Force tier-segmentation above this. |
| `CAMPAIGN_DAILY_VOLUME_CAP` | 200 | Across channels. |
| `WARMED_UP_DAYS_THRESHOLD` | 14 | Min domain age before cold sends. |
| `WARMUP_SCORE_THRESHOLD` | 70 | Min warmup score before cold sends. |

### Sending hygiene
- **Quiet hours**: no sends 8pm–8am recipient local time. Hard rule.
- **Weekday-only**: no Saturday/Sunday cold sends; warmup acceptable.
- **Recipient timezone alignment**: derived from `company_location`. If unknown, default to user's timezone with `[unverified — needs check]` flag on `recipient_local_timezone`.
- **Domain rotation**: when sending volume exceeds single-domain cap, rotate across a sender pool. Never bypass the per-domain cap by spawning new domains rapidly (Google reads through this).
- **Throttle ramp**: new sender starts at 5 sends/day, +5/day until reaching cap. `email-infrastructure-setup` owns the ramp schedule.

---

## 7. Freshness, dedup, re-touch rules

| Rule | Threshold |
|---|---|
| Same person, any channel, after no-reply | Min 90 days before re-engaging |
| Same person, after `not-now` reply | Resume at the date the prospect named (parsed from reply); else 90 days |
| Same person, after `not-interested` reply | Min 12 months; flag for review before re-engage |
| Same person, after `unsubscribe` | Never re-engage on email; LI/call path requires explicit user override + new compliance check |
| Same person, after `bounce: hard` | Mark `email_status: invalid`; route to `data-enrichment` for re-verification before any further email |
| Same company, different person | No global cooldown, but document multi-thread (cap 3 simultaneous threads per company) |
| Cadence completion | Park lead for 60 days minimum before next cadence |

Touch dedup key: `(lead_id, channel, sequence_position, campaign_id)` — within a campaign, no two touches collide.

---

## 8. Deliverability baseline

These are not optional. They are the cost of entry to inbox.

### 8.1 DNS / authentication (gate every email skill)
- **SPF**: published, includes the sender's actual sending IPs.
- **DKIM**: 2048-bit key minimum, current key ≤180 days old.
- **DMARC**: at minimum `p=none`; `p=quarantine` recommended after 30 days of clean reports.
- **From-address alignment**: SPF and DKIM domains align with the From: domain.
- **Reverse DNS (PTR)**: configured on sending IPs.
- **MX records**: present and resolving.

### 8.2 Google + Microsoft Feb 2024 bulk sender rules
Any sender to >5,000 messages/day to Gmail or Yahoo MUST:
- Authenticate (SPF + DKIM + DMARC).
- Maintain spam complaint rate **<0.3%** (warning at 0.1%, pause at 0.3%).
- Implement **one-click List-Unsubscribe** (RFC 8058 — `List-Unsubscribe-Post: List-Unsubscribe=One-Click`).
- Avoid spoofing Gmail in From:.
Microsoft mirrors this for Outlook/Hotmail (rolling out through 2024–2025).

### 8.3 Apple Mail Privacy Protection (Apple MPP)
Since iOS 15 (2021), Apple Mail pre-fetches all images, inflating open rates and pre-loading tracking pixels. Implications:
- **Open rate is a vanity metric.** Skills MUST NOT optimize against opens.
- **Reply rate** (and downstream meeting rate) is the primary metric.
- Apple-MPP-attributed opens are tagged in `metrics.opens_apple_mpp` if the receiver platform exposes it; campaign-management de-emphasizes them.

### 8.4 Sender reputation thresholds (campaign-management gates)
| Signal | Pause threshold | Warn threshold |
|---|---|---|
| Bounce rate (24h rolling) | 5% | 2% |
| Complaint rate (24h rolling) | 0.3% | 0.1% |
| Reply rate (cumulative) | n/a (informational) | <3% (suggests bad targeting/copy) |
| Google Postmaster reputation | "Bad" | "Medium" |
| Microsoft SNDS color | Red | Yellow |

When a pause threshold is hit, campaign-management auto-pauses the campaign and surfaces to user. Never ignored.

---

## 9. Compliance baseline

### 9.1 CAN-SPAM (US — email)
- Truthful From, To, Reply-To.
- Truthful subject (no deceptive line).
- Identification as advertisement (implicit if commercial).
- **Physical postal address** in every commercial email.
- **Functional opt-out** mechanism, honored within 10 business days.

### 9.2 GDPR / UK GDPR (EU + UK — email + LinkedIn cold messages)
- **Lawful basis**: legitimate interest (LIA documented) OR explicit consent.
- B2B contacts at corporate domains are typically legitimate-interest-eligible IF the message is relevant and a clear opt-out is provided.
- Personal email addresses (gmail, outlook, etc.) for B2B contacts → consent-only or skip.
- Right to object honored on first request.
- Recipient's right to access, rectification, erasure (DSAR).
- **`gdpr_basis: legitimate-interest`** tag on every EU/UK Touch + opt-out language in every email body.

### 9.3 CASL (Canada — email + SMS)
- **Implied or express consent** required.
- Identification of sender + functional opt-out.
- Implied consent for B2B if existing business relationship within last 24 months OR conspicuous publication of business address.
- Stricter than CAN-SPAM; if in doubt, route to nurture not cold.

### 9.4 TCPA (US — calls + SMS)
- **National DNC Registry**: scrub before any cold-call run. Personal mobile numbers on the DNC require prior consent.
- **State DNC lists**: scrub for relevant states (e.g. TX, FL, MA have stricter rules).
- **Quiet hours**: 8am–9pm recipient local time (TCPA hard rule for calls).
- **SMS to mobile**: prior express written consent required for marketing SMS.
- B2B-to-B2B-cellphone is a gray area; treat as TCPA-restricted by default.

### 9.5 LinkedIn ToS
- **No direct scraping.** Use Sales Navigator + session-based tools (HeyReach, Dripify, MeetAlfred) that operate on the user's own session.
- **No buying connections** or InMails outside the platform.
- **Connection-request notes**: ≤300 chars; do not paste sales pitches.
- **Account safety**: respect weekly limits; if account flagged, pause automation 7 days before resuming.

### 9.6 Quiet hours summary table
| Channel | Quiet hours (recipient local) | Source |
|---|---|---|
| Email | 8pm–8am | Hygiene convention (not statutory; reply rates collapse) |
| LinkedIn | 8pm–8am weekdays; weekends optional | LI engagement data |
| Cold call | 8pm–8am AND before 8am | TCPA hard rule (US); local laws vary |
| SMS | 8pm–8am AND TCPA hours | TCPA + state laws |

---

## 10. Anti-fabrication (extended for copy)

Per CLAUDE.md universal rule, every named entity in any function-3 output (recipients, companies, signal references, dates, dollar figures, evidence URLs, claimed customer outcomes, named tools) MUST carry one of four explicit provenance tags. Untagged = contract violation.

### 10.1 Function-3 specific risks (worse than function-2)

Function-3 sends content TO real people. The fabrication failure modes are:

- **Inventing personalization grounds** — "Saw your post on AI agents" when no such post exists. This damages sender reputation forever AND can trigger spam complaints AND violates legitimate-interest grounds (the message isn't actually about something they said).
- **Inventing customer outcomes / case studies** — "We helped Acme Corp save 20 hrs/week" when the case study doesn't exist or the metric is invented.
- **Misattributing quotes** — putting a quote in a real customer's mouth they never said.
- **Spoofing context** — implying prior conversation that didn't happen ("As we discussed last week...").

### 10.2 Hard rules for copy

The personalization-hook contract from `data-enrichment` is enforced at copy generation time:

- `cold-email-sequence` MUST refuse to ship a touch where `personalization_hook` provenance is `[unverified — needs check]`.
- `linkedin-outreach` MUST refuse a connect note that references a hook without a citable URL backing it.
- Customer outcomes / case studies / numbers MUST carry `[user-provided]` (the user supplied the claim) or `[verified: <url>]` (a published case study). Otherwise omit.
- Direct quotes from real people require `[user-provided]` or `[verified: <source>]`. Otherwise rephrase as a generic claim.
- Worked-example fictional entities tagged inline at first use (e.g. *"Stitchbox [hypothetical] saved 12 hrs/week..."*).

### 10.3 Push-to-CRM hygiene routing (per CLAUDE.md universal)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Touch pushes as `interaction:outreach` (sent record). |
| `[unverified — needs check]` | Touch is BLOCKED from sending. Pushes ONLY as `interaction:research` with `#unverified #review-required #needs-hook` tags. |
| `[hypothetical]` | Never sends; never pushes. Local artifact only (worked-example output). |

---

## 11. Push-to-CRM conventions for function-3

### 11.1 Entity routing per skill

| Skill | Primary push | Secondary push |
|---|---|---|
| `email-infrastructure-setup` | `interaction:research` (the setup audit + warmup state per domain) | n/a |
| `cold-email-sequence` | `interaction:outreach` per touch sent (subject, body excerpt, sent_at) | PATCH on `person` (last_touched_at, last_touched_channel) |
| `linkedin-outreach` | `interaction:outreach` per connection request / message | PATCH on `person` (last_touched_at) |
| `cold-calling` | `interaction:outreach` per dial / connect / voicemail | PATCH on `person` (last_touched_at, phone_status if changed) |
| `multi-channel-cadence` | `interaction:research` (the cadence definition) + per-touch interactions via channel skills | PATCH on `person` (active_cadence_id) |
| `campaign-management` | `interaction:research` per adjustment decision | PATCH on `campaign` (state, metrics_summary) |

### 11.2 Reply-handling routing

When a reply arrives, function-3 records the reply on the Touch. Classification + handler routing is **deferred to function-4** (`reply-classification`, `objection-handling-library`). Function-3 skills capture the raw reply and stamp `replied_at`; function-4 takes over.

### 11.3 Source tag

Every push carries `source: "skill:<skill-name>:v<version>"` (e.g. `skill:cold-email-sequence:v2.0.0`).

### 11.4 Named-product vs non-product hygiene (per CLAUDE.md rule #6)

Touch records map to real entities (people we sent to). Cadence + Campaign records are abstractions → push as `interaction:research`, never as fake `company`/`person` entities.

### 11.5 When NOT to push
- Touch failed pre-flight (deliverability gate, DNC, capacity cap) — push as `interaction:research` with `#blocked-pre-send` and the reason; never as `interaction:outreach`.
- Touch was a draft never sent — local artifact, do not push.
- `[unverified — needs check]` copy — see §10.3.
- `[hypothetical]` — never.
- Campaign in `draft` state — push the draft cadence/campaign as `interaction:research` with `#draft` tag; per-touch records skipped until `state: active`.

---

## 12. Inheritance from function-1 + function-2

Every function-3 skill declares these inputs from upstream functions in `## Inputs Required`. Hard rule: function-3 will refuse to ship outreach if the gating upstream artifact is missing.

| Function-3 skill | Function-1 input | Function-2 input | Hard gate? |
|---|---|---|---|
| All channel skills | ICP P-T-O chain (from `icp-definition`) | Lead records with score + tier (from `lead-scoring`) | YES — refuse if no scoring |
| `cold-email-sequence` | Pain language (icp-definition) + Positioning (positioning-strategy) | `personalization_hook [verified]` + `email_status` not in [risky, role-based, catch-all-domain, invalid] | YES |
| `linkedin-outreach` | Pain language (icp-definition) | `linkedin_url [verified]` + `linkedin_headline` (optional) | YES on linkedin_url |
| `cold-calling` | Pain language (icp-definition) | `phone_status: mobile | landline` (NOT `dnc | invalid`) | YES |
| `multi-channel-cadence` | All function-1 outputs | All function-2 outputs | YES |
| `email-infrastructure-setup` | n/a | n/a | (foundational; gates the others) |
| `campaign-management` | n/a | Lead records (active campaign membership) | n/a |

If `lead-scoring` has not run, function-3 skills can produce templates but refuse full execution mode and flag output as `ungrounded: true`.

---

## 13. Open conventions deferred to function-4+

These are not function-3's problem but worth flagging:

- **Reply classification** — when a person replies, function-3 stamps `replied_at` and captures the reply text. `reply-classification` (function-4) labels it (positive / not-now / not-interested / wrong-person / unsubscribe / OOO). Function-3 does NOT classify.
- **Objection handling** — when reply is `not-now` or `not-interested` with an objection, function-4's `objection-handling-library` produces the response. Function-3 does NOT respond past the cadence.
- **Discovery prep** — when reply is `positive` and a meeting is booked, `discovery-call-prep` (function-4) takes over. Function-3 closes the loop on the Touch.
- **Pipeline stage transition** — function-5 `pipeline-stages` reads function-3 Touch + function-4 reply data to advance pipeline stage.
- **Channel performance / KPI reporting** — function-6 `channel-performance` and `kpi-reporting` consume function-3's Touch / Campaign records as the substrate.

---

## Document version

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-05-04 | Initial draft alongside the 6 function-3 skills. WorkflowDoc as canonical worked-example product (chained mode). |
