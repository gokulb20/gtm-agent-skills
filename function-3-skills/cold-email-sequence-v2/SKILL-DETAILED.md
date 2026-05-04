---
name: cold-email-sequence
description: Write cold email sequences (5–7 touch, 14–21 day) using the CCQ copy framework, Pain-Trigger-Outcome openers, mobile-first formatting, and a hard ban on cliché openers. Gates every touch on the personalization-hook contract from `data-enrichment` (no verified hook → no send) and on `email_status` (no risky/catch-all/invalid sends). Use when a Tier-1/2 lead list is enriched and scored, when an ICP-grounded outbound burst is being planned, or when an existing sequence's reply rate is below the 3% floor and copy needs a structured rewrite.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, cold-email, sequence-design, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - email-infrastructure-setup
  - multi-channel-cadence
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - email-infrastructure-readiness-flag
  - sender-pool-and-domain-warmup-state
  - run-purpose-tag
deliverables:
  - 5-to-7-touch-email-sequence-with-copy
  - per-touch-content-with-provenance
  - touch-records-conforming-to-conventions-2-1
  - cadence-config-handoff-to-multi-channel-cadence
  - cliche-and-buzzword-audit-log
  - sequence-run-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cold Email Sequence

Produce a 5–7 touch cold email sequence (14–21 day arc) that ships through the function-3 channel adapter contract — `prepare → send → track`. Each Touch is generated using a named copy framework (CCQ default), grounded in the recipient's verified personalization hook, formatted mobile-first, and audited for clichés before send. Hard rule: a Touch with `[unverified — needs check]` hook provenance is BLOCKED from sending and pushed to the review queue instead.

> *The worked example uses a fictional product (WorkflowDoc) for illustration — same product as function-1, in a third role: WorkflowDoc as the seller actively executing outreach against function-2's Tier-1 leads. The frameworks, sequence patterns, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Touch / Cadence / Campaign schemas, three-mode pattern, capacity caps, deliverability baseline, compliance, anti-fab for copy, push-to-CRM routing — live in `function-3-skills/function-3-conventions.md`. This skill assumes it.*

## Purpose

Cold email is the cheapest scalable outbound channel, so it is the spine of any function-3 cadence. This skill does three things: (1) translates ICP Pain-Trigger-Outcome + positioning message house into a 5–7 touch sequence, (2) generates per-touch copy using a named framework (CCQ default) grounded in the recipient's verified hook from `data-enrichment`, (3) audits each draft against a cliché blocklist + word-count + mobile-formatting rules before scheduling. Goal: a sequence that ships ≥3% reply rate (the floor below which copy is broken) without burning sender reputation.

## When to Use

- "Write a cold email sequence for our Tier-1 outbound list."
- "Our reply rate is 1.5% — diagnose and rewrite the copy."
- "I have 80 enriched leads and need a 5-touch sequence ready for Smartlead."
- "Generate variants for A/B testing the opener."
- "I'm sending from Gmail directly — give me drafts and a per-touch runbook."
- Pre-launch copy generation when leads are enriched + scored.
- Sequence rewrite after `campaign-management` flags reply-rate floor breach.

### Do NOT use this skill when

- The lead list is unscored — run `lead-scoring` first; this skill refuses to ship copy targeting unscored leads.
- Email infrastructure isn't ready (`email-infrastructure-setup` precondition fails: warmup score <70, domain age <14d, SPF/DKIM/DMARC not aligned). Skill produces drafts + a "do not send yet" warning rather than scheduled sends.
- The recipient's `personalization_hook` is `[unverified — needs check]` AND the user can't supply a hook → skill produces a generic-fallback template flagged "low-quality copy"; recommend re-enrichment before send.
- The recipient's `email_status` is in [`risky`, `role-based`, `catch-all-domain`, `invalid`] → skill refuses; route to LinkedIn or re-verify.
- The trigger is purely transactional (existing customer expansion, partner re-engagement) — different skill family; cold-email-sequence is for cold contacts.
- Volume <5 recipients — hand-write rather than use this skill.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Scored + enriched Lead list | yes | `lead-scoring` output (with `data-enrichment` upstream) | Each Lead must carry `personalization_hook`, `email_status`, `signals`, `score`, `tier`. |
| 2 | ICP Pain-Trigger-Outcome chain | yes | `icp-definition-v2` output | The pain language used in opener variants. |
| 3 | Positioning message house | yes | `positioning-strategy-v2` output | Value-prop language used in body + CTA variants. |
| 4 | Email infrastructure readiness flag | yes | `email-infrastructure-setup-v2` output | Boolean: warmup ≥70, age ≥14d, SPF+DKIM+DMARC aligned. Gates send. |
| 5 | Sender pool + per-mailbox warmup state | yes | `email-infrastructure-setup` artifact | Used to spread load + enforce per-mailbox cap. |
| 6 | Run purpose tag | yes | user | E.g. "q2-tier1-vp-marketing-burst". Stamped on every Touch and the campaign record. |
| 7 | Sequence length override (optional) | no | user | Default 5–7; user can set 3 (warm follow-up) to 9 (deep nurture). |
| 8 | Framework override (optional) | no | user | Default CCQ; alternates AIDA, RTA, BANT-opener. |
| 9 | A/B variant request (optional) | no | user | "Two opener variants for Touch 1" produces two drafts; campaign-management does the actual split. |

### Fallback intake script

> "I'll write a cold email sequence in three modes — directly into your sending tool's API (Smartlead/Instantly/Lemlist), as paste-ready copy + cadence config for your tool's UI, or as native Gmail/Outlook drafts with a per-touch runbook.
>
> Two prerequisites I need to check:
> - Lead list scored + enriched? (Each lead needs a verified personalization hook + verified email.)
> - Email infrastructure ready? (warmup ≥70, domain ≥14 days old, SPF/DKIM/DMARC aligned.)
>
> If either is missing, I produce drafts but block the actual send with a 'do not send yet' warning."

### Input validation rules

- Lead list missing `personalization_hook [verified]` for >30% of records → warn user; recommend re-running `data-enrichment` for hook capture; produce copy only for the verified subset; route the unverified to review queue.
- `email_status` filter: drop any record in [risky, role-based, catch-all-domain, invalid]. Surface count.
- Email infrastructure flag = false → produce drafts ONLY (no scheduled sends). Run record carries `#blocked-infrastructure`.
- Lead list <5 → block; recommend manual hand-written outreach.
- Sequence length override outside [3, 9] → block; explain why (3-touch is minimum for cold; 9+ becomes nuisance).
- Run purpose tag missing → block; downstream `campaign-management` and function-6 attribution requires it.

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **CCQ — Context, Compliment/Connection, Question** | Lavender (Will Allred + team) — Lavender's published cold-email playbook | The default copy structure: open with verified Context (the hook), bridge with a Connection or specific observation, close with one focused Question. Optimized for the 9-second / 25–50-word reading budget. Each Touch uses CCQ unless an alternate framework is requested. |
| **Cold Calling 2.0** | Aaron Ross & Marylou Tyler — *Predictable Revenue* (2011) | The 5–7 touch / 14–21 day sequence shape, the role separation between SDR and AE, and the discipline of breaking up at touch 6–7 rather than chasing forever. |
| **Pain × Power × Vision opener angles** | Mike Bosworth — *Solution Selling* (1995) and *CustomerCentric Selling* (2003) | Three valid opener angles depending on what the hook reveals: Pain ("you're hitting X"), Power ("you have the authority to fix Y"), Vision ("you'd recognize the Z state"). The skill picks per recipient based on their signals + role. Bosworth's actual matrix is 9-block; we use the 3-axis simplification, labeled as such. |
| **Dunford 5-component positioning (applied to copy)** | April Dunford — *Obviously Awesome* (2019) | Each Touch's body emphasizes one of: Unique Attribute, Value-and-proof, Best-fit-ICP framing, Category framing, Competitive alternative — drawn from the message house. Variant rotation across touches keeps the sequence non-repetitive. |
| **Mental spam-filter blocklist** (house-built — derived from public Lavender data) | Crewm8 — codified from *Cold Email Wizardry 101* (Lavender's published primer) | Hard ban list: "I hope this finds you well," "I noticed," generic "we help X do Y" openers, multi-question CTAs, buzzwords (flexibility, visibility, scalable, strategic, leverage, synergy, robust, holistic). Every draft is audited against the blocklist before scheduling. |
| **Mobile-first formatting** (industry-standard, codified) | n/a — convention since iOS 14 reading-pane ubiquity | Subject ≤8 words; preview ≤90 chars; body ≤125 words; bullets when listing; one-CTA-only; signature ≤3 lines; opener ≤2 lines visible above the fold. |
| **Apple MPP-aware metrics posture** (statutory consequence) | n/a — Apple iOS 15 (2021) | Open rates are noise; this skill never optimizes against opens. Reply rate is the primary metric; meeting rate is the ground truth. |

## Tools and Sources

### Email sending platforms (any one for API mode)

| Tool | Mode | Purpose |
|---|---|---|
| Smartlead | API mode | Sequence + warmup + multi-domain rotation. Most-common modern choice. |
| Instantly | API mode | Similar to Smartlead; popular for high-volume outbound. |
| Lemlist | API mode | Strong on dynamic personalization variables. |
| Outreach.io / Salesloft | API mode (enterprise) | Larger orgs; higher cost. |
| Apollo Sequences | API mode | When user already pays for Apollo for sourcing. |

### Native send (BYO mode)
| Source | Notes |
|---|---|
| Gmail / Google Workspace | Hand-paste drafts; respect per-mailbox cap; track manually. |
| Microsoft 365 / Outlook | Same; cap is more conservative (start at 20/day). |

### Source priority rule

For copy provenance, in priority: **`personalization_hook [verified: <source-url>]`** > **`signals[]` with permalink** > **ICP P-T-O language (verified by user)** > **agent inference (`[unverified — needs check]` — BLOCKS send)**. Never fabricate a "saw your post" opener; never invent a customer outcome / number. The cliché blocklist is enforced regardless of provenance.

### Copy framework reference

| Touch | Default framework | Word target |
|---|---|---|
| 1 — Opener | CCQ + Pain angle | 50–80 |
| 2 — Follow-up #1 (D+3) | CCQ + Vision angle (different value-prop facet) | 40–70 |
| 3 — Follow-up #2 (D+7) | RTA (Resource-Then-Ask): share a resource, light ask | 50–80 |
| 4 — Mid-sequence pivot (D+11) | Compelling-Event reframe | 60–90 |
| 5 — Social-proof touch (D+15) | Outcome-based proof (specific named customer with `[verified]` or `[user-provided]` outcome) | 60–100 |
| 6 — Break-up (D+19) | Permission-based break-up; one-question close | 30–50 |
| 7 (optional) — Resurrection (D+45) | Different hook; different angle entirely | 50–80 |

## Procedure

### 1. Validate prerequisites

Read scored Lead list, ICP P-T-O, message house, email-infrastructure readiness flag. If any is missing or fails gate, block with explicit reason. **Rationale**: cold-email's three preconditions (good list, good positioning, good infrastructure) all need to be in place — copy that's perfect on top of bad targeting still fails.

### 2. Determine mode

`SMARTLEAD_API_KEY` (or `INSTANTLY_API_KEY` / `LEMLIST_API_KEY` / etc.) set → API mode. Else user has tool seat → manual mode (paste-ready cadence + copy). Else native sending → BYO mode (per-touch runbook).

### 3. Filter recipient list

Apply hard gates:
- Drop records where `email_status` ∉ [verified].
- Drop records where `personalization_hook` provenance is `[unverified — needs check]` (route to review queue).
- Apply tier filter from user input (default: tier-1 + tier-2).
- Apply GDPR-jurisdiction split: `recipient_jurisdiction: eu | uk` → cadence variant with explicit opt-out + LIA language.

Surface counts: total → eligible after gates → split by tier and jurisdiction.

### 4. Pre-flight: capacity check

Compute total touches = `eligible_count × sequence_length`. Compare to capacity (per `SENDS_PER_DOMAIN_PER_DAY_CAP × sender_pool × duration_days`). If over capacity, recommend: tier-segment (drop tier-2/3), reduce sequence length, expand sender pool, or extend duration. Surface to user; wait for authorization.

### 5. Generate per-touch copy

For each recipient × touch position:
- Pick framework per the touch's default (Touch 1 = CCQ + Pain; Touch 2 = CCQ + Vision; etc.).
- Draw verified hook from Lead's `personalization_hook` field. Stamp the hook's source URL into the Touch's `provenance.hook`.
- Compose subject (≤8 words, no clickbait, no all-caps, no emoji, no fwd:/re: spoofing).
- Compose body within word target. Apply mobile formatting (one-CTA, ≤2-line opener, bullets if listing).
- Generate the **List-Unsubscribe header** for the email (RFC 8058 one-click) per §8 of conventions.
- Append physical address (CAN-SPAM US) or LIA + opt-out language (GDPR EU/UK) per recipient jurisdiction.

**Rationale**: per-recipient per-touch copy IS the deliverable. The framework picks the structure; the hook makes it specific; the audit (next step) keeps it deliverable.

### 6. Cliché + word-count + framework audit

Each draft passes through:
- **Cliché blocklist** scan: any phrase from the blocklist (per Frameworks Used) → flag, regenerate or surface for user override.
- **Word-count check**: subject ≤8 words; body within touch's word target; signature ≤3 lines.
- **Mobile-format check**: ≤2-line opener; ≤4-line paragraphs; one CTA only.
- **Buzzword check**: ban list (flexibility, visibility, scalable, strategic, leverage, synergy, robust, holistic, cutting-edge, best-in-class, world-class).
- **CTA check**: exactly one ask, framed as a low-friction question (not a meeting demand). "Worth a 15-min look?" beats "Book time on my calendar."

Drafts failing audit are regenerated; second-fail surfaces for user review with the audit log.

### 7. Compose Touch records (per conventions §2.1)

For each generated draft, build a Touch record with full provenance: `content` (subject/body/word_count/framework), `compliance` (jurisdiction/has_unsubscribe/list_unsubscribe_header/has_physical_address), `provenance.copy` ([verified: hook-source-url] or [unverified — needs check]), `scheduled_for` (with quiet-hours + weekday-only respected). Status `draft` until scheduled.

### 8. Build cadence + schedule (or hand-off)

Compose the cadence per §2.2 of conventions: 5–7 touch positions, day_offsets (default 0/3/7/11/15/19/45), channel = email throughout (or hand off to `multi-channel-cadence` for multi-channel composition). For API mode: create the sequence in Smartlead/Instantly/Lemlist via API and schedule. For manual mode: emit cadence config + copy paste-ready. For BYO: emit per-touch runbook with native-send instructions + manual status-mark workflow.

### 9. Push to CRM + emit run summary

Per conventions §11: scheduled Touches push as `interaction:research` with `#scheduled` tag (the actual sent record gets pushed by `track()` after send). Run summary one-screen: eligible count, dropped counts (by reason), sequence length, total touches scheduled, per-domain load, capacity-cap headroom, audit-flag count, recommended next skill (`multi-channel-cadence` for layered approach; `campaign-management` for monitoring).

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: api | manual | byo
  sending_platform: smartlead | instantly | lemlist | gmail-native | ...
  inputs:
    lead_count_input: <int>
    lead_count_eligible: <int>
    lead_count_dropped:
      bad_email_status: <int>
      unverified_hook: <int>
      tier_filter: <int>
      jurisdiction_eu_uk_no_lia: <int>
  preconditions:
    infrastructure_ready: <bool>
    warmup_score_min: <int>
    domain_age_days_min: <int>
  cadence:
    sequence_length: <int>
    duration_days: <int>
    touches: [<positions, day_offsets, frameworks>]
  capacity:
    total_touches: <int>
    daily_volume_max: <int>
    sender_pool_size: <int>
    headroom: <pct of cap remaining>
  audit:
    cliche_flags: <int>
    buzzword_flags: <int>
    word_count_flags: <int>
    regenerated_drafts: <int>
    surfaced_for_review: <int>
  warnings: [<string>]
  next_skill_recommendation: <multi-channel-cadence | campaign-management | data-enrichment-recapture | ...>

per_recipient:
  - lead_id: <uuid>
    touches: [
      { position, scheduled_for, subject, body_excerpt, word_count,
        framework, hook_source_url, provenance.copy, status }
    ]
```

## Worked Example

> *All fictional entities below are tagged `[hypothetical]` — illustrative only.*

**User prompt**: "Write a 5-touch cold email sequence for our 80 Tier-1 enriched leads. Smartlead is configured. Pitching WorkflowDoc to Heads of Support at Series B SaaS companies."

**Step 1 — Validate prerequisites**: 80 leads from `lead-scoring` run with ICP scorecard v2.0.0. Email infrastructure readiness flag = true (warmup score 84, domain age 47d, SPF/DKIM/DMARC all aligned [verified: easydmarc]). Positioning message house loaded.

**Step 2 — Mode**: `SMARTLEAD_API_KEY` set → API mode.

**Step 3 — Filter**:
- Input: 80
- Drop bad email_status: 6 (3 risky, 2 catch-all, 1 invalid)
- Drop unverified hook: 11 (route to review queue)
- Drop EU/UK without LIA prep: 0 (all US in this batch)
- **Eligible: 63**

**Step 4 — Capacity**:
- 63 leads × 5 touches = 315 total touches
- Sender pool: 3 mailboxes × 30/day cap = 90/day max
- 315 / 90 = ~4 days minimum send concentration
- Cadence duration 19d gives plenty of headroom — proceed.

**Step 5 — Generate copy** (sample for one recipient, Touch 1 = CCQ + Pain):

Recipient: Esme Liang [hypothetical], VP Customer Support @ Stitchbox [hypothetical]
Hook: *"Stitchbox just hired their first VP CX (Esme, announced 2026-04-19)."* [verified: news.example.com/stitchbox-vp-cx-2026]
Pain anchor (from ICP P-T-O): *"Tribal knowledge spread across 8+ tools; new hires take 6-8 weeks to ramp."*

Subject: `New VP CX seat — first 90 days?` (5 words [verified-format])

Body (74 words):
```
Esme — congrats on landing the VP CX role at Stitchbox.

The first 90 days usually surface the same pattern at Series B support orgs:
runbooks live in 8 different tools, new hires take 6-8 weeks to ramp,
tribal knowledge walks out when senior support churns.

WorkflowDoc consolidates runbooks into one searchable surface — Stitchbox-sized
teams typically cut ramp time to 3 weeks.

Worth a 15-min look in the next two weeks?

Will [hypothetical]
```

Provenance:
- `provenance.hook`: [verified: news.example.com/stitchbox-vp-cx-2026]
- `provenance.copy.outcome_claim`: [user-provided] (user provided the "3-week ramp" customer reference)

**Step 6 — Audit**:
- Cliché flags: 0 (no "I hope this finds you well", no "I noticed", no buzzwords)
- Word count: subject 5 ✓ / body 74 (target 50–80) ✓
- Mobile format: opener 2 lines ✓ / one CTA ✓ / signature 3 lines ✓
- Compliance: List-Unsubscribe header attached, physical address in signature (US recipient, CAN-SPAM)

**Step 7 — Touch record (excerpt)**:
```yaml
touch_id: tch_2026-05-04_q9k_001_t1
campaign_id: cmp_2026-05-04_q9k
cadence_id: cad_workflowdoc_t1_5touch_19d_v1
lead_id: lea_esme_liang_stitchbox
channel: email
touch_type: opener
sequence_position: 1
scheduled_for: 2026-05-05T10:00:00-07:00   # quiet-hours + weekday respected
content:
  subject: "New VP CX seat — first 90 days?"
  body: "<full text above>"
  word_count: 74
  framework: ccq+pain-angle
  personalization_hook_used: news.example.com/stitchbox-vp-cx-2026
  mobile_formatted: true
sender:
  email: will@workflowdoc-mail.com [hypothetical]
  reputation_score: 92
compliance:
  recipient_jurisdiction: us
  gdpr_basis: not-applicable
  has_unsubscribe: true
  has_physical_address: true
  list_unsubscribe_header: "<mailto:unsubscribe@workflowdoc-mail.com>, <https://workflowdoc.example/u/abc>"
  honors_quiet_hours: true
  recipient_local_timezone: America/Los_Angeles
provenance:
  copy: [verified: news.example.com/stitchbox-vp-cx-2026]
  hook: [verified: data-enrichment:enrich_2026-05-04_t3p]
status: scheduled
```

**Step 8 — Build cadence + schedule**: Smartlead API call creates sequence `cad_workflowdoc_t1_5touch_19d_v1` with 5 touches at day_offsets 0/3/7/11/19; 63 recipients × 5 = 315 touches scheduled across the next 19 days, paced by 90/day cap.

**Step 9 — Run summary**:
```
WorkflowDoc Cold Email Sequence Run [hypothetical]
Run ID: cmp_2026-05-04_q9k
Mode: API (Smartlead). Cadence: ccq-tier1-5touch-19d
Filter: 80 → 69 (after email_status drop 6) → 58 + 5 fallback = 63 eligible (after hook drop, 11 to review)
Capacity: 315 touches / 90/day max / 19d duration = 41% headroom
Copy audit: 0 cliché flags, 0 buzzword flags, 0 word-count flags, 0 surfaced for review
Compliance: 63 US recipients (CAN-SPAM); 0 EU/UK in batch
Recommended next: campaign-management (monitor reply rate; target ≥3% by D+10)
```

## Heuristics

- **Reply rate, never open rate.** If you tune subject lines on opens, you're tuning on Apple-MPP noise. Reply rate is the primary metric — period.
- **Hook quality is everything.** A 50-word email with a verified, recent, specific hook beats a 200-word "value-prop tour" 5x on reply rate. If you can't cite the hook, send a different sequence.
- **Three opener angles, not three opener templates.** Pain / Power / Vision lets you pick per recipient based on their signals — don't run all 60 leads through the same Pain opener.
- **Touch 3 is the resource touch.** Sharing something useful (a specific tactical idea, a benchmark, a 2-min read) at touch 3 keeps the sequence from feeling like 5 sales asks in a row. Reply rate at touch 3 often beats touch 1.
- **Break up at 6, don't ghost.** A clean break-up touch ("seems like the timing's off — should I close the loop?") generates 5–10% reply rate by itself, often more than touch 4–5.
- **Mobile-first means below-the-fold matters.** 81% of cold emails are read on mobile; if your opener takes 4 lines visible, the recipient deletes before reading.
- **Buzzwords are a tax on attention.** "Strategic" / "scalable" / "leverage" each cost ~3% reply rate. Audit and replace with specifics.
- **One CTA only.** Two questions in the close — even if both are reasonable — drops reply rate to near zero. People with 80+ unread emails answer "yes" or skip; "yes, but what specifically?" is too much friction.
- **Cliché openers are a structural error, not a stylistic one.** "I hope this finds you well" tells the recipient's spam filter "this is bulk." Eliminate at the framework level, not the proofreading level.
- **Send Tuesday-Thursday, 9–11am local.** Mondays buried in Slack; Fridays deferred to next week; afternoons busy. Cadence engine respects this by default; user can override.

## Edge Cases

- **No hook for any record (rare).** If `data-enrichment` returned 0% hook coverage, this skill produces "templated" copy without per-recipient hook — but flags every Touch as `provenance.copy: [unverified — needs check]` and BLOCKS sending. Recommend re-enrichment with `linkedin_recent_posts` permission enabled before retry.
- **Multi-language recipients.** Recipient's `company_location` outside US/UK/CA → flag for translation; default to English with a courtesy line ("happy to switch to <local language> if helpful"); never auto-translate body text the agent can't verify.
- **Founder-led outreach (small volume).** Volume <30/day from a single mailbox; don't bother with sender pool. But still warm up; still audit copy.
- **Reply mid-sequence.** Touch with `replied_at` triggers cadence exit on that recipient; downstream handler (`reply-classification` / `objection-handling-library` in function-4) takes over. This skill does not classify replies.
- **Bounce mid-sequence.** `bounce: hard` → mark `email_status: invalid`, route lead to `data-enrichment` for re-verification, exit cadence on that recipient.
- **Domain reputation drops mid-sequence.** Postmaster Tools shifts to "Medium" → `campaign-management` decides whether to slow or pause. This skill respects the pause.
- **GDPR-jurisdiction recipient.** Cadence variant injected: every Touch body has explicit opt-out language + LIA reference; subject avoids "promotional" framing.
- **Sequence rewrite (existing campaign with low reply rate).** Run cliché audit on existing copy first; surface what to change before regenerating from scratch. Often 2–3 word swaps fix a sequence.
- **Brand-voice override.** User wants to enforce a specific voice ("direct, no-jokes" / "warm, conversational") → respect; audit blocklist still applies.
- **A/B variant request for one touch.** Generate 2 drafts that differ on ONE dimension (opener angle, subject, CTA wording) — not three things at once, or the test is unreadable. campaign-management runs the actual split.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Sending platform API auth fails (401) | Smartlead/Instantly returns 401 | Confirm key in env; do NOT retry silently; offer fall to manual mode (output cadence config + copy). |
| Sending platform rate limit (429) | "Too many requests" | Backoff (5s/30s/90s); resume from last successful Touch creation. |
| Email infrastructure precondition fails mid-build | warmup_score drops below 70 | Suspend scheduling; alert user; produce drafts but do not send; route to `email-infrastructure-setup`. |
| List-Unsubscribe header rejected by sending platform | RFC 8058 not supported on user's plan | Warn; provide unsubscribe URL in body footer instead; document non-compliance with one-click rule. |
| Cliché audit flags >50% of drafts | systemic copy-gen issue | Pause; surface audit log; recommend hook-quality review (drafts may be regenerating around weak hooks). |
| Recipient timezone unknown | derived from company_location empty | Flag `recipient_local_timezone: [unverified]`; default to user's timezone with warning; route to review queue. |
| Capacity cap exceeded mid-schedule | cadence requires 400 touches, 300 capacity | Stop; persist what was scheduled; offer raise-cap, sender-pool expansion, or tier-segmentation. |
| Push to CRM fails (4xx/5xx) | network or token | Persist run output to local JSON; retry on user request. |
| Recipient manually unsubscribed before scheduled send | flag captured during prep | Drop remaining Touches in cadence on that recipient; respect opt-out forever. |
| Sender mailbox replaced mid-cadence | warmup state loss | Pause that mailbox's queued Touches; flag for redistribution to remaining sender pool. |

## Pitfalls

- **Optimizing on open rate.** Apple MPP made it noise. Reply rate is primary; open rate is reported, never tuned.
- **Generic openers.** "I noticed your company..." with no specific verified detail is fabrication risk + low reply rate.
- **Long emails.** >125 words drops reply rate sharply; 50–80 is the sweet spot for openers.
- **Multiple CTAs.** "Would 15 min next Tuesday work, or would you rather I send a brief?" → both questions = no answer.
- **Buzzword stuffing.** "Scalable, strategic, robust" — each costs reply rate.
- **Cliché openers.** "I hope this finds you well" / "I noticed you're..." — pre-trained spam filter triggers in the recipient's brain.
- **Skipping the break-up.** Touch 6 break-up generates real replies; sequences ending at touch 5 leave conversion on the table.
- **Ignoring quiet hours / weekends.** Sending Sat 11pm = spam-flagged; weekday 9-11am local = best window.
- **Sending without warmup.** First-day cold-blast from a new domain = instant blacklist.
- **Sending to risky/catch-all/role-based.** Bounce rate explodes; sender reputation tanks; the skill blocks these by contract.
- **Fabricating personalization** (anti-fabrication / provenance rule). Every named entity (recipients, companies, signal references, dates, customer outcomes, dollar figures, evidence URLs) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. The personalization-hook contract from `data-enrichment` is enforced at copy-generation time: a Touch with `[unverified — needs check]` hook is BLOCKED from sending. Inventing customer outcomes, fake quotes, or "saw your post" with no URL is a hard failure.
- **Misalignment with Function-1 positioning.** Body language drifts from message house — surface in audit; recompose against positioning artifact.

## Verification

The sequence is real when: (a) every Touch's `provenance.copy` resolves to a hook URL or carries `[user-provided]` for outcome claims; (b) reply rate ≥3% by D+10 of the cadence (below this floor, copy or targeting is broken); (c) bounce rate stays <2% (warning) / <5% (pause); (d) complaint rate stays <0.1% (target) / <0.3% (pause); (e) zero touches sent during quiet hours / weekends; (f) zero touches with cliché-blocklist phrases; (g) re-running the same input next month produces the same copy framework distribution and similar audit-pass rate (skill is deterministic on framework, varies only on hook content).

Negative test: pick 5 Touches at random from the run output. Read each subject + opener line aloud. Does it sound like a real human wrote it specifically to that recipient? If any sound generic — "I noticed you're a leader in..." — copy-gen is broken; fix the framework or the hook source.

## Done Criteria

1. Mode determined and stated (api / manual / byo); sending platform identified.
2. Prerequisites validated: lead scoring exists, ICP P-T-O loaded, message house loaded, infrastructure readiness flag confirmed.
3. Recipient filter applied: bad email_status dropped, unverified hooks routed to review queue, tier filter applied, GDPR jurisdiction split applied.
4. Capacity check passed (or user authorized over-cap); per-domain daily cap respected.
5. Per-touch copy generated with framework attribution and provenance tagging.
6. Cliché + word-count + mobile-format + buzzword audit run; failures regenerated or surfaced.
7. Touch records assembled per conventions §2.1 with full compliance metadata (List-Unsubscribe header, physical address, jurisdiction, quiet-hours respect).
8. Cadence built per conventions §2.2 with day_offsets, frameworks, and exit conditions.
9. Scheduled (API mode) or handed off (manual / BYO mode); push to CRM emitted; run summary one-screen with reply-rate target and recommended next skill.

## Eval Cases

### Case 1 — full API mode, hook-rich list

Input: 60 enriched + scored Tier-1 leads (95% with verified hooks); Smartlead configured; infrastructure flag = true.

Expected: ~57 eligible after filters; 5-touch cadence × 57 = 285 touches scheduled over 19 days; reply rate ≥4% by D+10; 0 cliché flags; 0 sends during quiet hours / weekends.

### Case 2 — manual mode, hook-thin list

Input: 200 leads but only 60% have verified hooks; user has Lemlist seat, no API key.

Expected: skill outputs Lemlist-paste-ready cadence config + 5 touches × 120 hooked recipients = 600 drafts. Routes 80 unverified-hook leads to review queue. Recommends re-running `data-enrichment` with `linkedin_recent_posts` permission.

### Case 3 — BYO mode, founder-led small batch

Input: 12 Tier-1 leads (all with verified hooks); no sending platform; user wants Gmail native.

Expected: 60 drafts (5 touches × 12) presented as Gmail draft-ready blocks with day_offset send instructions; per-touch runbook with manual status-mark. Per-mailbox cap not relevant at 12 leads. Recommends `email-infrastructure-setup` to confirm SPF/DKIM/DMARC even for native Gmail.

### Case 4 — infrastructure not ready

Input: 50 leads; warmup score 55 (below 70 threshold).

Expected: skill produces drafts but BLOCKS scheduling. Run record `#blocked-infrastructure`. Recommends `email-infrastructure-setup` to complete warmup; offers to re-run automatically when readiness flag flips to true.

### Case 5 — sequence rewrite (low reply rate)

Input: existing 5-touch sequence with reply rate 1.2% (below 3% floor); same recipient list.

Expected: skill audits existing copy against cliché + buzzword + word-count rules; surfaces specific phrases to change; offers two paths — (a) targeted rewrites (often 2–3 phrase swaps) or (b) full regenerate against current framework. Recommends regenerate if hook quality is the issue, targeted rewrites if copy structure is the issue.

## Guardrails

### Provenance (anti-fabrication)

Per §10 of conventions and CLAUDE.md universal rule: every named entity in copy carries provenance. Hooks are `[verified: <source-url>]` or the Touch is BLOCKED. Customer outcomes are `[user-provided]` (user supplied) or `[verified: <case-study-url>]` or omitted. Direct quotes from real people require `[user-provided]` or `[verified]`; otherwise rephrase as generic.

The skill's strongest guardrail: a Touch with `[unverified — needs check]` provenance NEVER sends — it routes to review queue as `interaction:research` with `#unverified #review-required #needs-hook`.

### Evidence

Every cliché flag, audit failure, and provenance gate is logged in the run record. Re-runs are deterministic on framework structure; variance is in hook content (which the upstream `data-enrichment` owns).

### Scope

This skill writes email copy + schedules sequences. It does NOT verify emails (that's `data-enrichment`), classify replies (`reply-classification`, function-4), handle objections (`objection-handling-library`, function-4), or run multi-channel composition (`multi-channel-cadence`). Avoid scope creep — emit recommendations to the next skill.

### Framing

Run summary uses operational language. Per-touch rationale ties hook → angle → framework → audit-pass for auditability.

### Bias

Copy frameworks (CCQ, AIDA, etc.) embed implicit assumptions about reading culture (English-speaking, attention-scarce, mobile-first). Multi-language and non-Western markets may need framework variants; surface as a known limitation, don't pretend the framework is universal.

### Ethics

Compliance baseline (§9 of conventions) is non-negotiable: physical address (CAN-SPAM), legitimate-interest + opt-out (GDPR), no spoofed domains, one-click List-Unsubscribe (Google/MS Feb 2024). Send to a person who has unsubscribed = never.

### Freshness

Hooks decay (per `data-enrichment` half-lives). A hook captured 90+ days ago should be re-verified before send; sequence built on a stale hook reads forced.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Sequence built, ready for monitoring | `campaign-management` | Campaign id + recipient list + reply-rate target |
| Multi-channel composition desired | `multi-channel-cadence` | Cadence config + LinkedIn/call positions to layer |
| Email infrastructure not ready | `email-infrastructure-setup` | Warmup state + DNS audit |
| Replies start arriving | `reply-classification` (function-4, planned) | Reply text + Touch id |
| Objection responses needed | `objection-handling-library` (function-4, planned) | Reply classification + Touch context |
| Hook coverage <70% | `data-enrichment` | Lead list + missing-hook records |
| List unscored | `lead-scoring` | Enriched leads + ICP scorecard |
| Reply rate <3% by D+10 | `cold-email-sequence` (rewrite mode) OR `lead-scoring` (re-tier the list) | Current sequence + metrics |

## Push to CRM

After scheduling, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each scheduled Touch (draft state) | `interaction` (type: `research`) | `relevance` = "Touch <position> scheduled for <ISO> via <channel> with hook <url>"; `tags: "#scheduled #cold-email #touch-<position> #function-3"` |
| Each Touch after send | `interaction` (type: `outreach`) | `relevance` = subject + body excerpt + provenance; `tags: "#sent #cold-email #function-3"` |
| Cadence + campaign run record | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#cold-email-sequence-run #function-3"` |
| Last-touched timestamp on recipient | `person` (PATCH via dedup key) | `last_touched_at`, `last_touched_channel: email`, tags updated |
| `[unverified — needs check]` (hook missing) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #cold-email-sequence #blocked-no-hook"`; never `outreach` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
SMARTLEAD_API_KEY=     # or INSTANTLY_API_KEY / LEMLIST_API_KEY
SENDS_PER_DOMAIN_PER_DAY_CAP=30
WARMED_UP_DAYS_THRESHOLD=14
WARMUP_SCORE_THRESHOLD=70
```

### Source tag

`source: "skill:cold-email-sequence:v2.0.0"`

### Example push (sent Touch)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#sent #cold-email #touch-1 #ccq-pain #function-3",
    "relevance": "Cold email sent 2026-05-05T10:00 PT. Subject: \"New VP CX seat — first 90 days?\". Framework: CCQ + Pain. Hook: Stitchbox VP CX hire 2026-04-19 [verified: news.example.com/stitchbox-vp-cx-2026]. Word count: 74. Sender: will@workflowdoc-mail.com (reputation 92). Cadence: cad_workflowdoc_t1_5touch_19d_v1.",
    "source": "skill:cold-email-sequence:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#cold-email-sequence-run #function-3",
    "relevance": "Cold email sequence run cmp_2026-05-04_q9k. Mode: API (Smartlead). Cadence: ccq-tier1-5touch-19d. Filter: 80 input → 63 eligible (6 bad email, 11 unverified hook to review). Capacity: 315 touches over 19d / 90/day max / 41% headroom. Audit: 0 cliché / 0 buzzword / 0 word-count flags. Recommended next: campaign-management (target reply rate ≥3% by D+10).",
    "source": "skill:cold-email-sequence:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Touch sends and pushes as `interaction:outreach` per standard mapping. |
| `[unverified — needs check]` | Touch is BLOCKED from sending. Pushes ONLY as `interaction:research` with `#unverified #review-required #needs-hook` tags. Never as `outreach`. |
| `[hypothetical]` | Never sends; never pushes. Local artifact only. |

Example blocked push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #cold-email-sequence #blocked-no-hook",
    "relevance": "Touch BLOCKED for Mira Chen [unverified — needs check] — personalization_hook absent (data-enrichment ran but found no citable source in last 90d). Recommend re-enrichment with linkedin_recent_posts permission OR manual hook capture, then re-run cold-email-sequence.",
    "source": "skill:cold-email-sequence:v2.0.0"
  }'
```

### When NOT to push

- Drafts never scheduled — local artifact only; do not push.
- Touches blocked at pre-flight (infrastructure, capacity, DNC, hook) — push ONLY as `interaction:research` with the block reason; never as `outreach`.
- `[unverified — needs check]` — see provenance routing.
- `[hypothetical]` — never.
- Recipient unsubscribed before scheduled send — drop the remaining cadence Touches; push the unsubscribe-honor record only.
