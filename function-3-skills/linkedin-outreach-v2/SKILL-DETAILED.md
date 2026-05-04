---
name: linkedin-outreach
description: Execute LinkedIn outreach via Sales Navigator + session-based tools (HeyReach, Dripify, MeetAlfred) — connection requests with ≤300 char notes, follow-up messages to existing connections, InMails for high-value targets — with strict LinkedIn ToS compliance (no direct scraping), weekly rate limits, and the personalization-hook contract from `data-enrichment` enforced. Use when email is the wrong channel (risky/catch-all email status, or email-fatigued segments), when LinkedIn URL is the strongest identity signal in the Lead schema, when the play is relationship-first social-selling, or when multi-channel cadence requires a LinkedIn leg.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, linkedin, social-selling, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - lead-sourcing-linkedin
  - cold-email-sequence
  - multi-channel-cadence
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list-with-linkedin-urls
  - icp-pain-trigger-outcome-chain
  - user-linkedin-account-or-session-tool
  - run-purpose-tag
  - cadence-position-context
deliverables:
  - connection-request-notes-≤300-chars
  - follow-up-message-templates-to-connections
  - inmail-templates-for-high-value-targets
  - touch-records-conforming-to-conventions-2-1
  - per-touch-content-with-provenance
  - linkedin-cadence-config-handoff
  - account-safety-state-report
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# LinkedIn Outreach

Execute LinkedIn-channel touches — connection requests, messages to existing connections, occasional InMails — through session-based automation tools (HeyReach, Dripify, MeetAlfred) or manual Sales Nav UI. Hard-codes LinkedIn ToS compliance (NO direct scraping), respects weekly rate limits to protect the user's account, and gates every touch on the personalization-hook contract from `data-enrichment`. The output is Touch records ready for `multi-channel-cadence` to layer with email or for standalone LinkedIn-only sequences.

> *The worked example uses a fictional product (WorkflowDoc) for illustration — same product as function-1, in a third role: WorkflowDoc as the seller running LinkedIn outreach against function-2's Tier-1 leads. The frameworks, ToS compliance posture, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Touch / Cadence / Campaign schemas, three-mode pattern, capacity caps (LI weekly limits), compliance, anti-fab for copy, push-to-CRM routing — live in `function-3-skills/function-3-conventions.md`. This skill assumes it.*

## Purpose

LinkedIn is the second-most-common outbound channel after email and the *first* choice when emails bounce or get filtered. This skill: (1) translates a Lead's LinkedIn URL + verified hook into a connection-request note (≤300 chars) or message, (2) picks the right LI play (connection-with-note vs. cold InMail vs. message-to-connection vs. content-engagement-then-connect), (3) routes execution through session-based tools that respect ToS — never direct scraping. Goal: sustainable LI outreach that respects weekly limits, protects the user's account, and converts at the 8–15% connection-acceptance rate that good copy + good targeting produces.

## When to Use

- "Send LinkedIn outreach to our 60 Tier-1 prospects with verified LinkedIn URLs."
- "Email is the wrong channel — these are catch-all-domain emails."
- "Add a LinkedIn leg to our existing cadence."
- "I have HeyReach configured — set up a connection-request campaign."
- "We're running social-selling — relationship-first sequence."
- Pre-launch when LinkedIn URL coverage is high (>80% of list).
- Email-fatigued segments where reply rate has plateaued <2%.

### Do NOT use this skill when

- The user requests direct LinkedIn scraping → REFUSE per LinkedIn ToS; route to Sales Nav + session-based tool path.
- Lead list missing `linkedin_url [verified]` for >50% of records → block; route to `data-enrichment` or `lead-sourcing-linkedin` to capture LI URLs first.
- The user's LinkedIn account is restricted or under safety warning → pause; recommend 7+ days no-automation cool-down before resuming.
- Volume target exceeds `LINKEDIN_CONNECTS_PER_WEEK_CAP` (default 80) without a clear multi-account rotation plan — block and explain the account-safety risk.
- Recipient is in EU/UK without `gdpr_basis: legitimate-interest` → block per GDPR; recommend `data-enrichment` GDPR pass first.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Scored + enriched Lead list with LinkedIn URLs | yes | `lead-scoring` (with `data-enrichment` upstream) | Each Lead must carry `linkedin_url [verified]` + `personalization_hook` + score + tier. |
| 2 | ICP P-T-O chain | yes | `icp-definition-v2` | Pain language for opener angles. |
| 3 | Positioning message house | yes | `positioning-strategy-v2` | Value-prop language; light-touch on LI (no hard-sell tone). |
| 4 | LinkedIn account or session tool | yes | one of: `HEYREACH_API_KEY`, `DRIPIFY_API_KEY`, `MEETALFRED_API_KEY`, `LEMLIST_LI_API_KEY`, `PHANTOMBUSTER_API_KEY`, or user's Sales Nav seat (manual mode), or user's LI account directly (BYO mode) | Determines mode; never direct scraping. |
| 5 | Cadence position context | yes (in multi-channel runs) | `multi-channel-cadence` | Whether this is the opener or a follow-up to a prior email. |
| 6 | Run purpose tag | yes | user | Stamped on every Touch. |
| 7 | Connection-status flag (optional) | no | tool API | Existing connection vs. cold; drives template choice. |
| 8 | LI account safety state (optional) | no | session-tool API | Recent restrictions / warnings; blocks high-volume runs if amber/red. |

### Fallback intake script

> "LinkedIn outreach has three modes:
> - API mode (session-based): HeyReach / Dripify / MeetAlfred API key set; tool runs your session safely within weekly limits.
> - Manual mode: you have a Sales Nav seat; I produce paste-ready connection-request notes and follow-up messages; you click through.
> - BYO mode: native LinkedIn UI; per-recipient runbook with the exact note + when to send.
>
> Three checks:
> - Lead list has verified `linkedin_url` for most records?
> - Your LI account is healthy (no recent safety warnings)?
> - Are we hitting EU/UK contacts? They need `gdpr_basis: legitimate-interest` set."

### Input validation rules

- `linkedin_url [verified]` coverage <50% → block; route to `data-enrichment` / `lead-sourcing-linkedin`.
- Direct-scraping requested → REFUSE with ToS explanation; recommend session-based tool path.
- Volume × weekly LI limit conflict → block; offer reduced volume or multi-account rotation plan.
- LI account safety state ∈ [amber, red] → block; recommend 7-day cool-down.
- EU/UK recipients without `gdpr_basis: legitimate-interest` → drop those records; flag for re-enrichment.
- Connection-request note > 300 chars → block at draft stage; auto-trim to 295 chars and warn.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **CCQ — Context, Compliment/Connection, Question** (LinkedIn variant) | Lavender (Will Allred + team), adapted for LI | Same structure as cold-email but tighter — connection note ≤300 chars forces single-question close; follow-up message to a connection allows 2–3 sentences. No links in connection notes (LinkedIn flags). |
| **Predictable Revenue (LinkedIn application)** | Aaron Ross & Marylou Tyler — *Predictable Revenue* (2011) | ICP-driven persona-based outbound; never spray; SDR-AE split applies as much on LinkedIn as on email. |
| **Social Selling principles** | Daniel Disney — *The Ultimate LinkedIn Sales Guide* (2021) and Disney's published essays | Relationship-first posture: like + comment on prospect content before reaching out; lead with curiosity, not pitch; treat connections as relationships not leads. The skill encodes a "warm-up" track for high-value prospects (engage with their content before connecting). |
| **LinkedIn Social Selling Index (SSI)** | LinkedIn (official metric, public-facing) | LinkedIn's own 0–100 score for the user's profile. Higher SSI → higher acceptance rates AND fewer account-safety flags. The skill recommends profile-improvements when SSI is the bottleneck (rare; surfaced as advisory, not gating). |
| **Trigger Events for Sales Success** | Craig Elias (2009) | Same trigger taxonomy as function-2 sourcing. LinkedIn surfaces triggers (new role, post about pain, content engagement) the email channel can't see — exploit per recipient. |
| **LinkedIn ToS compliance posture** (statute / contract) | LinkedIn User Agreement (current) | NO direct scraping. Session-based tools using user's own credentials are acceptable. Weekly limits respected. The skill encodes this as a hard rule, not a guideline. |
| **Connection-request frameworks** (house-built — codified industry consensus) | Crewm8 | Three valid patterns: (1) **Warm-intro** — referenced mutual connection or context; (2) **Event-based** — references a specific recent event (hire, promotion, post, conference); (3) **Content-engagement** — earlier engaged with their content, now connecting with reference. The skill picks per recipient based on signal availability. |

## Tools and Sources

### Session-based automation (preferred — ToS-respecting)

| Tool | Purpose |
|---|---|
| HeyReach | Multi-account safe; uses user's session; best for sustained outbound. |
| Dripify | Similar; strong on multi-step LI sequences. |
| MeetAlfred | Older, still solid; multi-step. |
| Lemlist (LI module) | Combined with Lemlist email; good for multi-channel. |
| PhantomBuster | More flexible but less LI-specific safety; use with care. |

### Manual sending (Sales Nav UI)

| Source | Notes |
|---|---|
| Sales Navigator | The user runs the campaign in the UI; skill produces paste-ready notes + scheduling guidance. |

### BYO mode (native LinkedIn UI)

| Source | Notes |
|---|---|
| Native LinkedIn | Per-recipient runbook: "send to {name} on day +X, note text below." Manual status-mark by user. |

### Source priority rule

For all copy provenance: **`personalization_hook [verified: <source-url>]`** > **`signals[]` with permalink** > **`linkedin_headline` (recipient's own bio text)** > **agent inference (`[unverified — needs check]` — BLOCKS send)**. Never invent a "saw your post on..." opener without the post URL.

### LinkedIn-specific knowledge

- **Connection-request notes**: ≤300 chars HARD limit. No URLs (LI flags). No emojis (perceived as bulk).
- **InMail credits**: only Sales Nav users. Use for Tier-1 prospects only; expensive (one credit each, ~$5–10 effective).
- **Weekly limits**: connection requests ~80 (LI's soft cap is ~100 — stay below); messages to existing connections ~250; InMail per Sales Nav tier (Core: 50/mo; Advanced: 50/mo; Advanced Plus: 50/mo with rollover).
- **Acceptance rate by template**: warm-intro ~30%, event-based 15–25%, content-engagement 12–20%, generic-no-context <5%.
- **Optimal send time**: weekday 9am–5pm recipient local; afternoon often higher acceptance than morning.
- **Account safety**: aggressive automation gets accounts flagged; pace conservatively; never bulk-import a connection list at once.

## Procedure

### 1. Validate prerequisites

Read scored Lead list; confirm `linkedin_url [verified]` coverage acceptable; load ICP P-T-O + message house. Check LI account safety state (via session tool or user-reported). If gates fail, block with reason.

### 2. Determine mode

Session tool API key set → API-substitute mode. Else seat → manual mode (paste-ready). Else BYO → per-recipient runbook. Direct-scraping requested → REFUSE.

### 3. Filter recipient list

Apply gates:
- Drop records without `linkedin_url [verified]`.
- Drop EU/UK records without `gdpr_basis: legitimate-interest`.
- Apply tier filter (default tier-1 + tier-2).
- For multi-channel runs, deduplicate against active email cadences.
- Check existing-connection status if tool provides it; route to "message" path if connected, "connection-with-note" if not.

### 4. Pre-flight: capacity check (weekly LI limits)

Compute requested touches per week. Compare to:
- `LINKEDIN_CONNECTS_PER_WEEK_CAP` (default 80) — for new connections.
- `LINKEDIN_MESSAGES_PER_WEEK_CAP` (default 200) — for messages to existing connections.
- `LINKEDIN_INMAIL_PER_MONTH_CAP` (default 50) — InMails.

If over capacity, recommend: tier-segment, multi-account rotation, or extended duration. Surface to user.

### 5. Pick template framework per recipient

For each recipient, pick one of three connection-request frameworks based on signal availability:

- **Warm-intro**: hook references mutual connection or specific shared context. Use when a real mutual exists.
- **Event-based**: hook references a recent event (new role, promotion, funding, post, conference talk). Highest acceptance when event is recent (<60 days) AND specific.
- **Content-engagement**: user has previously engaged with the recipient's LI content (liked / commented). Reference the specific post engaged with.

Generic "I noticed you're a leader in..." templates are forbidden (they're the LinkedIn equivalent of "I hope this finds you well").

### 6. Generate per-touch copy

For each recipient × touch position:
- Connection request: ≤300 chars, no URL, framework-based, ends with one low-friction question or stated intent.
- Follow-up message (if connection accepted): 2–3 sentences, references the original note, layers a soft value-prop reference, ends with one question.
- InMail (Tier-1 only): 4–6 sentences, similar structure to cold email but more conversational.

Apply audit:
- **Char-count gate** for connection notes (≤300 hard).
- **Cliché blocklist**: "I noticed you're a leader" / "I'd love to connect" / "saw your impressive profile" / "expand my network."
- **No-link rule** for connection notes.
- **Hook citation**: every event-based or content-engagement note must reference a citable URL in the Touch's `provenance.copy` field.

### 7. Compose Touch records (per conventions §2.1)

Touch entries with channel = `linkedin-connect` / `linkedin-message` / `linkedin-inmail`. Full provenance, scheduled_for (respecting weekday 9am–5pm recipient local), compliance metadata (GDPR for EU/UK).

### 8. Schedule via tool or hand off

API-substitute: create the campaign in HeyReach / Dripify / MeetAlfred via API; respect tool's pacing (most tools auto-pace within LI safe limits). Manual: emit paste-ready notes + per-touch send schedule. BYO: per-recipient runbook with exact note + day-offset send instruction.

### 9. Push to CRM + emit run summary

Per conventions §11: scheduled Touches as `interaction:research` with `#scheduled` (real send pushed by `track()`). Run summary: eligible count, dropped counts (by reason), framework distribution (warm-intro / event-based / content-engagement), capacity headroom, account safety state, recommended next skill.

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: api-substitute (heyreach|dripify|meetalfred|lemlist|phantombuster) | manual | byo
  inputs:
    lead_count_input: <int>
    lead_count_eligible: <int>
    lead_count_dropped:
      no_linkedin_url: <int>
      eu_uk_no_lia: <int>
      tier_filter: <int>
      already_in_active_email_cadence: <int>
  account_safety:
    state: green | amber | red
    weekly_connects_used_recent: <int>
    headroom: <int — connects available this week>
  framework_distribution:
    warm_intro: <int>
    event_based: <int>
    content_engagement: <int>
  capacity:
    weekly_connects: <int> / <cap>
    weekly_messages: <int> / <cap>
    monthly_inmails: <int> / <cap>
  warnings: [<string>]
  next_skill_recommendation: <campaign-management | multi-channel-cadence | data-enrichment-recapture>

per_recipient:
  - lead_id: <uuid>
    linkedin_url: <verified>
    cadence_position: <int>
    framework: warm-intro | event-based | content-engagement
    touch:
      channel: linkedin-connect | linkedin-message | linkedin-inmail
      content:
        note: <≤300 chars>   # for connect
        body: <full message>  # for message / inmail
        char_count: <int>
        framework: <as above>
        hook_source_url: <permalink>
      scheduled_for: <ISO>
      provenance:
        copy: [verified: <hook-url>] | [unverified — needs check]
      compliance:
        recipient_jurisdiction: us | eu | uk | ca | other
        gdpr_basis: legitimate-interest | not-applicable
```

## Worked Example

> *All fictional entities below are tagged `[hypothetical]` — illustrative only.*

**User prompt**: "Send LinkedIn connection requests to 40 of our Tier-1 leads with verified LinkedIn URLs. WorkflowDoc to VPs of Customer Experience. HeyReach configured."

**Step 1 — Validate**: 40 leads from `lead-scoring` with `linkedin_url [verified]` for all. ICP P-T-O loaded. LI account safety state: green (no recent flags). Account weekly headroom: 80 connects available, 0 used this week.

**Step 2 — Mode**: `HEYREACH_API_KEY` set → API-substitute mode.

**Step 3 — Filter**:
- Input: 40
- No linkedin_url drops: 0 (all verified)
- EU/UK no LIA drops: 3 (route to data-enrichment GDPR pass)
- Already in active email cadence: 5 (defer until email cadence completes; will layer per `multi-channel-cadence` if requested)
- **Eligible: 32**

**Step 4 — Capacity**: 32 connects this week vs cap 80 → 40% utilization, well within safe range.

**Step 5 — Framework picks**:
- 4 leads have content-engagement signals (the user previously liked/commented on their posts) → content-engagement framework.
- 22 leads have recent role-event signals (started in current role <60d) → event-based framework.
- 0 mutual-connection signals available → no warm-intro framework this run.
- 6 leads with stale/weak hooks → flagged for review queue (do NOT send generic).

**Step 6 — Generate copy** (sample for one recipient, event-based):

Recipient: Nina Park [hypothetical], VP Customer Experience @ Helio [hypothetical]
Hook: *"Started as VP CX at Helio 2026-04-08 (43 days ago); hire announcement on LinkedIn"* [verified: linkedin.com/posts/helio-vp-cx-announce]

Connection note (228 chars):
```
Nina — congrats on landing the VP CX role at Helio. The first 90 days
usually surface the same pattern at Series B support orgs: runbooks
scattered across 8+ tools. Worth a quick chat?

— Will [hypothetical]
```

Provenance:
- `provenance.copy`: [verified: linkedin.com/posts/helio-vp-cx-announce]
- Char count: 228 ✓ (≤300)
- No URL ✓
- Single CTA ✓

**Step 7 — Touch record (excerpt)**:
```yaml
touch_id: tch_2026-05-21_li_ned_001
campaign_id: cmp_li_2026-05-21_q9k
cadence_id: cad_workflowdoc_li_3touch_14d_v1
lead_id: lea_nina_park_helio
channel: linkedin-connect
touch_type: opener
sequence_position: 1
scheduled_for: 2026-05-22T11:00:00-08:00   # weekday 11am recipient local
content:
  note: "Nina — congrats on landing the VP CX role at Helio. The first 90 days usually surface the same pattern at Series B support orgs: runbooks scattered across 8+ tools. Worth a quick chat? — Will [hypothetical]"
  char_count: 228
  framework: event-based
  hook_source_url: linkedin.com/posts/helio-vp-cx-announce [hypothetical]
sender:
  linkedin_handle: will-workflowdoc [hypothetical]
  ssi_score: 72
compliance:
  recipient_jurisdiction: us
  gdpr_basis: not-applicable
  honors_quiet_hours: true
provenance:
  copy: [verified: linkedin.com/posts/helio-vp-cx-announce]
  hook: [verified: data-enrichment:enrich_2026-05-04_t3p]
status: scheduled
```

**Step 8 — Schedule via HeyReach**: Campaign `cad_workflowdoc_li_3touch_14d_v1` created via HeyReach API with 32 connection requests paced over 7 days (4–5/day at 11am recipient local). Follow-up messages scheduled D+3 (if accepted) and D+10 (if accepted).

**Step 9 — Run summary**:
```
WorkflowDoc LinkedIn Outreach Run [hypothetical]
Run ID: cmp_li_2026-05-21_q9k
Mode: API-substitute (HeyReach). Cadence: linkedin-3touch-14d-v1
Filter: 40 → 32 eligible (3 EU/UK no-LIA, 5 in active email cadence)
Account safety: green; weekly headroom 80 connects, 32 used = 40%
Framework dist: 0 warm-intro / 22 event-based / 4 content-engagement / 6 routed to review (weak hooks)
Capacity: 32 connects / 80 cap (40%) ✓
Compliance: 32 US (no GDPR overlay needed)
Recommended next: campaign-management (track acceptance rate; target 15–25%)
```

## Heuristics

- **Acceptance rate is the primary metric.** Below 12% = generic copy or wrong targeting. 15–25% = healthy. Above 25% = excellent (likely warm-intro-heavy).
- **Account safety > volume.** Always. A founder's LI account being banned is unrecoverable. Pace conservatively.
- **No URL in connection notes.** LinkedIn flags. Even if it's a public article. Wait until after acceptance to share links.
- **Reply rate to follow-up message > acceptance rate to connection.** Once connected, you've earned a 30-second read; use it well.
- **Engage before connecting (content-engagement track).** Like + comment on 2–3 of their recent posts; THEN connect with reference. Acceptance rate jumps materially.
- **Post your own content.** Acceptance rates for users with active LI presence (posting weekly, SSI ≥75) are 1.5–2x users with empty profiles.
- **InMails should be rare.** Reserve for Tier-1 prospects where connection rejected or LI URL is the only contact path. The cost (credit + perceived "spam") is real.
- **Don't connect-and-pitch in the same message.** "Hi, congrats on the role, btw can we talk about WorkflowDoc?" reads as bait. Earn the connection; pitch later.
- **Friday afternoons get worse acceptance.** Tuesday-Thursday 9am–4pm recipient local is the sweet spot.
- **Multi-account rotation has diminishing returns at small volume.** Below 100/week, single account is fine. Above 200/week, rotate 2+ accounts.

## Edge Cases

- **No verified LinkedIn URLs in batch.** Block; route to `data-enrichment` (Hunter / Apify Sales Nav lookup) or `lead-sourcing-linkedin` to populate URLs.
- **User account flagged amber.** Pause automation; recommend 7-day cool-down with manual-only sends; resume cautiously.
- **Recipient has 30k+ connections.** They probably accept everyone — acceptance rate on this segment is artificially high; don't extrapolate to other segments.
- **Recipient has private profile / restricted view.** Connection request still works but follow-up message is delivery-uncertain; use sparingly.
- **Recipient is "open to work" / actively job-searching.** Reframe: acknowledge their search context if relevant; otherwise sidestep.
- **Recipient is a competitor employee.** Surface; user decides whether to skip.
- **Multi-language profile.** Capture verbatim; if English isn't recipient's primary language, switch note to their language for materially-better acceptance (translation requires user verification).
- **Reply mid-cadence (positive or negative).** Flag for `reply-classification` (function-4); cadence exits on that recipient.
- **GDPR EU/UK recipient.** Cadence variant: explicit LIA reference + opt-out language in follow-up message body (connection notes don't have room).
- **InMail-only path** (when LI URL exists but the recipient has restricted connection requests). Use sparingly; cost-per-touch is high.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Direct-scraping path attempted | skill internal flag | Hard refuse; ToS explanation; recommend session-based tool. |
| HeyReach / Dripify session expired | "Session invalid" | Pause; user re-authenticates LinkedIn in tool; resume. |
| LinkedIn weekly limit hit | tool reports "limit reached" | Pause remaining connects until next Monday; surface; offer to extend cadence duration. |
| Account safety amber/red | session tool reports flag | Stop run; recommend 7+ day cool-down; review recent volume + recipient quality. |
| Connection accepted but follow-up message hits LI message-throttle | rare; LI rate-limits messages too | Pause messages; resume next day. |
| Recipient changed jobs mid-cadence | LinkedIn shows new company | Pause that recipient; re-evaluate ICP fit at new company; route to `data-enrichment` for refresh. |
| InMail credit exhausted | Sales Nav reports 0 credits | Surface; route to connection-with-note path or wait for next month's allotment. |
| Connection note >300 chars at draft | char-count audit | Auto-trim to 295 chars at sentence boundary; surface for review if trim drops too much. |
| Recipient with private profile rejects connection | normal | Mark `acceptance: rejected`; cadence exits on that recipient. |
| Push to CRM fails | network or token | Persist locally; retry. |

## Pitfalls

- **Direct LinkedIn scraping.** ToS violation; account-suspension risk. Hard rule — REFUSE.
- **Generic connection notes.** "I'd love to connect with another professional in <industry>" — auto-rejected.
- **URLs in connection notes.** LinkedIn flags. No exceptions.
- **Connect-and-pitch combo.** Reads as bait; lowers reply-to-message conversion.
- **Aggressive volume.** 100+/week single-account = account flag; pace below 80.
- **Skipping the post-acceptance follow-up.** Connection is the door; the message is the conversation.
- **Treating LI like email.** Tone matters more on LI; less direct, more conversational.
- **Inventing engagement context** ("loved your recent post on AI agents" with no post URL). Anti-fab violation; the post URL is the citation.
- **InMailing everyone.** InMails are expensive AND signal "couldn't get a connection" — use rarely.
- **Ignoring SSI / profile health.** Low SSI users get lower acceptance and more flags.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (recipients, companies, hook URLs, dates, customer outcomes, evidence) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Hook URLs gated for event-based and content-engagement frameworks; absence routes the Touch to review queue.
- **Skipping account-safety state check.** Sending into amber/red account = ban risk.

## Verification

The run is real when: (a) 0 connection notes exceed 300 chars; (b) 0 connection notes contain URLs; (c) every event-based or content-engagement Touch has a citable hook URL; (d) acceptance rate ≥12% by D+7 (below this floor, copy or targeting broken); (e) 0 sends during quiet hours / weekends; (f) account safety state stays green throughout the run; (g) weekly LI limits never exceeded.

## Done Criteria

1. Mode determined (api-substitute / manual / byo); direct-scraping requests REFUSED.
2. Recipient filter applied: no-LI-URL dropped, EU/UK no-LIA dropped, tier filter, dedup against active email cadence.
3. Account safety state checked; amber/red blocks run.
4. Capacity check passed: weekly limits respected; multi-account rotation if applicable.
5. Per-recipient framework picked (warm-intro / event-based / content-engagement); generic-no-context refused.
6. Per-touch copy generated with char-count + cliché + no-URL audit.
7. Touch records assembled per conventions §2.1 with provenance + compliance metadata.
8. Cadence built per conventions §2.2 with day_offsets matching weekly limits; scheduled or handed off; push to CRM emitted; run summary one-screen.

## Eval Cases

### Case 1 — full API-substitute mode, hook-rich list

Input: 40 Tier-1 leads, 100% with verified LI URLs, HeyReach configured, account healthy.

Expected: ~30–35 eligible after filters; framework distribution: 0 warm-intro / 20+ event-based / 5+ content-engagement / 5–10 review (weak hooks); 32 connection requests scheduled at safe pace (~5/day); acceptance rate target 15–25% by D+7.

### Case 2 — manual mode (Sales Nav UI, no automation)

Input: 25 Tier-1 leads, Sales Nav seat only, no automation tool key.

Expected: skill outputs paste-ready notes + per-touch send schedule; user clicks through Sales Nav UI; status tracked manually. Recommends HeyReach / Dripify for next batch.

### Case 3 — direct-scraping refused

Input: user asks to scrape LinkedIn for VPs of Eng at FAANG.

Expected: skill REFUSES with ToS explanation; recommends Sales Nav search (use `lead-sourcing-linkedin` for sourcing) + HeyReach session-based execution. Logs refusal as `interaction:research`.

### Case 4 — account safety amber

Input: 50 leads, HeyReach detects user's LI account at amber (recent restriction warning).

Expected: skill BLOCKS run; recommends 7-day cool-down; offers reduced-volume manual-only path if user insists; flags account-recovery as the priority.

### Case 5 — multi-channel cadence layer

Input: cadence already running with email Touches 1, 2, 4, 5; LI connection at position 3.

Expected: skill produces only the LI Touch (one connection request per recipient at day_offset 5); references the prior email touch in the connection note context; respects channel-isolation rules (don't reference email content directly — privacy norm).

## Guardrails

### Provenance (anti-fabrication)

Per §10 of conventions: every connection note + message carries provenance. Hooks for event-based / content-engagement frameworks MUST have citable URL; without it, route to review queue. NEVER invent a "saw your post" without the post URL. Worked-example fictional entities tagged inline.

### Evidence

Every framework choice (warm-intro / event-based / content-engagement) is backed by a specific signal in the Lead record. Generic-no-context paths are refused at framework-selection time.

### Scope

This skill writes LI copy + schedules touches. It does NOT source LI URLs (`lead-sourcing-linkedin` / `data-enrichment`), classify replies (`reply-classification` function-4), or run multi-channel composition (`multi-channel-cadence`).

### Framing

Run summary uses operational language. Per-recipient rationale (framework + hook source) auditable.

### Bias

LinkedIn over-indexes on tech / SaaS / professional-services markets; under-indexes on regulated industries (manufacturing, healthcare, government). When LI coverage is thin for an ICP, surface and recommend `lead-sourcing-web` for trigger discovery.

### Ethics

LinkedIn ToS compliance non-negotiable. No direct scraping. Account-safety > short-term volume. Weekly limits respected.

### Freshness

Hooks decay (event-based hooks have 90-day half-life per `data-enrichment`); a stale hook reads forced. Re-pull hook from `data-enrichment` if Touch scheduled >30 days after hook capture.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Sequence built, monitor active campaign | `campaign-management` | Campaign id, recipient list, acceptance rate target |
| Multi-channel composition desired | `multi-channel-cadence` | LI cadence + email/call positions to layer |
| LI URLs missing on list | `data-enrichment` or `lead-sourcing-linkedin` | Lead list + missing-URL records |
| Replies start arriving | `reply-classification` (planned) | Reply text + Touch id |
| Account safety amber | back to this skill (cool-down mode) + audit recent volume | Account state + recent run history |
| List unscored | `lead-scoring` | Enriched leads + ICP scorecard |
| Email-channel-better target | `cold-email-sequence` | Same lead list filtered for verified email |

## Push to CRM

After scheduling, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each scheduled connection request (draft) | `interaction` (type: `research`) | `relevance` = "Connection request scheduled for <ISO> with note <preview>"; `tags: "#scheduled #linkedin-connect #function-3"` |
| Each Touch after send | `interaction` (type: `outreach`) | `relevance` = note text + framework + hook URL + provenance; `tags: "#sent #linkedin-<connect|message|inmail> #function-3"` |
| Cadence + campaign run record | `interaction` (type: `research`) | `relevance` = run summary + framework distribution; `tags: "#linkedin-outreach-run #function-3"` |
| Last-touched timestamp | `person` (PATCH via dedup key) | `last_touched_at`, `last_touched_channel: linkedin-<type>` |
| `[unverified — needs check]` (weak hook) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #linkedin-outreach #weak-hook"`; never `outreach` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
HEYREACH_API_KEY=     # or DRIPIFY / MEETALFRED / LEMLIST_LI / PHANTOMBUSTER
LINKEDIN_CONNECTS_PER_WEEK_CAP=80
LINKEDIN_MESSAGES_PER_WEEK_CAP=200
LINKEDIN_INMAIL_PER_MONTH_CAP=50
```

### Source tag

`source: "skill:linkedin-outreach:v2.0.0"`

### Example push (sent connection request)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Helio",
    "contactName": "Nina Park",
    "contactLinkedIn": "https://linkedin.com/in/nina-park-cx",
    "tags": "#sent #linkedin-connect #event-based #function-3",
    "relevance": "LinkedIn connection request sent 2026-05-22T11:00 PT. Framework: event-based. Hook: Helio VP CX hire 2026-04-08 [verified: linkedin.com/posts/helio-vp-cx-announce]. Note (228 chars): \"Nina — congrats on landing the VP CX role at Helio. The first 90 days usually surface the same pattern at Series B support orgs: runbooks scattered across 8+ tools. Worth a quick chat? — Will\". Sender: will-workflowdoc (SSI 72). Cadence: cad_workflowdoc_li_3touch_14d_v1.",
    "source": "skill:linkedin-outreach:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#linkedin-outreach-run #function-3",
    "relevance": "LinkedIn outreach run cmp_li_2026-05-21_q9k. Mode: HeyReach API-substitute. Cadence: linkedin-3touch-14d-v1. Filter: 40 → 32 eligible (3 EU/UK no-LIA, 5 in active email). Account safety: green; 32/80 weekly cap (40%). Framework: 0 warm-intro / 22 event-based / 4 content-engagement / 6 review. Recommended next: campaign-management (target acceptance ≥15% by D+7).",
    "source": "skill:linkedin-outreach:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Touch sends and pushes as `interaction:outreach`. |
| `[unverified — needs check]` | Touch is BLOCKED. Pushes ONLY as `interaction:research` with `#unverified #review-required #linkedin-outreach` tags. |
| `[hypothetical]` | Never sends; never pushes. Local artifact only. |

Example blocked push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #linkedin-outreach #weak-hook",
    "relevance": "Touch BLOCKED for Mira Chen [unverified — needs check] — event-based framework requires citable hook URL; data-enrichment found no recent LI post or news. Recommend re-enrichment or switch to warm-intro framework if mutual connection exists.",
    "source": "skill:linkedin-outreach:v2.0.0"
  }'
```

### When NOT to push

- Drafts never scheduled — local artifact only.
- Touches blocked at pre-flight (account safety, capacity, weak hook) — push as `interaction:research` with block reason.
- Direct-scraping refused — push refusal record for audit; no Touches.
- `[unverified — needs check]` — see provenance routing.
- `[hypothetical]` — never.
- Recipient withdrew connection request before send (rare) — drop remaining cadence Touches; push withdrawal record only.
