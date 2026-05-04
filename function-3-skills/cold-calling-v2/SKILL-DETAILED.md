---
name: cold-calling
description: Generate cold-call scripts (9-second opener, discovery questions, gatekeeper-handler, ≤15-second voicemail) and orchestrate dial sessions via JustCall / Aircall / Orum / Dialpad with TCPA-compliant DNC scrubbing, quiet-hours enforcement, mobile-vs-landline routing, and call-disposition logging. Use when Tier-1 SAL-eligible prospects have verified `phone_status: mobile | landline` (NOT `dnc | invalid`), when email + LinkedIn channels have plateaued, when high-stakes accounts need live-voice contact, or when a multi-channel cadence requires a call leg.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, cold-calling, dialer, function-3]
related_skills:
  - icp-definition
  - positioning-strategy
  - lead-scoring
  - data-enrichment
  - cold-email-sequence
  - linkedin-outreach
  - multi-channel-cadence
  - campaign-management
  - reply-classification
inputs_required:
  - scored-and-enriched-lead-list-with-phone-status
  - icp-pain-trigger-outcome-chain
  - positioning-message-house
  - dialer-platform-or-manual-mode
  - dnc-scrub-result
  - run-purpose-tag
deliverables:
  - 9-second-opener-script
  - discovery-question-set
  - gatekeeper-handler-script
  - voicemail-drop-script-≤15-seconds
  - touch-records-conforming-to-conventions-2-1
  - dial-list-with-tcpa-clearance
  - call-disposition-log
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cold Calling

Produce TCPA-compliant cold-call scripts and orchestrate dial sessions for Tier-1 prospects whose phone numbers are verified and DNC-scrubbed. Outputs: 9-second opener, discovery question set, gatekeeper handler, ≤15-second voicemail drop, and per-recipient Touch records ready for `multi-channel-cadence` to layer with email + LinkedIn or for standalone call-only campaigns. Hard rules: no calls to `phone_status: dnc | invalid`; no calls before 8am or after 9pm recipient local (TCPA); SMS to mobile requires explicit prior consent.

> *The worked example uses a fictional product (WorkflowDoc) for illustration — same product as function-1, in a third role: WorkflowDoc as the seller running cold calls against function-2's Tier-1 SAL-eligible prospects. The frameworks, TCPA compliance posture, and procedure are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Touch / Cadence / Campaign schemas, three-mode pattern, capacity caps, compliance baseline (TCPA, DNC, quiet hours), anti-fab for copy, push-to-CRM routing — live in `function-3-skills/function-3-conventions.md`. This skill assumes it.*

## Purpose

Cold calling is the most expensive channel per touch but converts at 3–5x email when the contact is verified, the prospect is Tier-1, and the script is human. It is also the most-regulated outbound channel — TCPA fines are per-violation. This skill: (1) generates a 9-second opener that respects "the pattern interrupt" psychology, (2) produces a discovery question set anchored in ICP P-T-O language, (3) writes a ≤15-second voicemail drop optimized for callbacks, (4) handles gatekeepers without pretending or lying, (5) gates every dial on DNC scrubbing + quiet hours + verified phone status. Goal: a dial session that converts conversations into meetings without exposing the user to TCPA risk.

## When to Use

- "Add cold-calls to our Tier-1 cadence."
- "Email reply rate plateaued at 2% — let's call the high-fit prospects."
- "I need a 9-second opener and voicemail drop for our dial session today."
- "We have JustCall configured — set up a dial campaign for 50 prospects."
- "Founder-led calls — give me the discovery questions to ask."
- Pre-launch when a Tier-1 segment has verified mobile / landline phones.
- Post-meeting-no-show rescue calls.

### Do NOT use this skill when

- Lead list lacks `phone_status: mobile | landline` for >50% — block; route to `data-enrichment` (Hunter / Lusha) for phone discovery.
- Any record has `phone_status: dnc | invalid` → drop those records (skill enforces); never call DNC numbers.
- Recipient timezone unknown → block until known (TCPA hard hours).
- Volume target exceeds `CALLS_PER_REP_PER_DAY_CAP` (default 80) without a clear multi-rep plan.
- The user wants automated SMS to mobiles without prior consent → REFUSE per TCPA.
- Tier-2 / Tier-3 prospects — cold calls don't ROI at lower-tier conversion rates; recommend keeping email/LI.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Scored + enriched Lead list | yes | `lead-scoring` (with `data-enrichment` upstream) | Must carry `phone`, `phone_status`, score, tier, signals, P-T-O context. |
| 2 | ICP P-T-O chain | yes | `icp-definition-v2` | Pain language for opener + discovery. |
| 3 | Positioning message house | yes | `positioning-strategy-v2` | Value-prop language; light-touch in voicemail. |
| 4 | Dialer platform | one of: `JUSTCALL_API_KEY`, `AIRCALL_API_KEY`, `ORUM_API_KEY`, `DIALPAD_API_KEY`, `CONNECTANDSELL_API_KEY`, or manual phone use (BYO mode) | Determines mode. |
| 5 | DNC scrub result | yes | `DNC_COM_API_KEY` or `CONTACTCENTERCOMPLIANCE_API_KEY` (mandatory before US calling) | Hard gate; calls without scrubbing not allowed. |
| 6 | Run purpose tag | yes | user | Stamped on every Touch. |
| 7 | Sales rep identity (optional) | no | user | Calls from named rep affect cadence + voicemail script. |

### Fallback intake script

> "Cold calling has three modes:
> - API mode: dialer (JustCall, Aircall, Orum, Dialpad) configured; I create the dial list and orchestrate the session via the dialer's API.
> - Manual mode: dialer seat without API; I produce the dial list as paste-ready CSV + script library; rep runs the session.
> - BYO mode: native phone (cellphone or desk phone); I produce the per-recipient runbook with script + recipient context.
>
> Two prerequisites I need:
> - Phone status verified for most records (`mobile` or `landline`)?
> - DNC scrub result available for US recipients? (TCPA hard requirement.)"

### Input validation rules

- `phone_status` ∈ [unverified, invalid] for >50% → block; route to `data-enrichment` (Hunter / Lusha for phone discovery).
- DNC scrub absent for US recipients → block; mandatory before any US dialing.
- `phone_status: dnc` records → drop from active list (always).
- Recipient timezone unknown → block; TCPA quiet hours can't be enforced without timezone.
- Calls per day exceed `CALLS_PER_REP_PER_DAY_CAP` without multi-rep plan → block; recommend extending duration or expanding rep pool.
- Tier-3 / Anti-ICP prospects in dial list → drop with warning (cold-calling ROI doesn't hold below Tier-2).

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **Cold Calling 2.0** | Aaron Ross & Marylou Tyler — *Predictable Revenue* (2011) | The original SDR script genre. The 9-second opener pattern (pattern-interrupt → state purpose → permission-to-continue) and the SDR-to-AE handoff norms. |
| **Tactical empathy / mirroring / labeling** | Chris Voss — *Never Split the Difference* (2016) | When a prospect pushes back, the skill's discovery scripts use Voss's labeling technique ("It sounds like the timing isn't right") and mirroring (repeating their last 1–3 words as a question). Reduces resistance without manipulation. |
| **Solution Selling pain-questioning** | Mike Bosworth — *Solution Selling* (1995) and *CustomerCentric Selling* (2003) | Discovery questions follow Bosworth's pain → impact → buying-vision arc, not feature-by-feature. The pain anchor comes from `icp-definition`'s P-T-O chain. |
| **Sandler Pain Funnel** | David Sandler / Sandler Training (1967) — codified in *Sandler training* curricula | Discovery question structure: surface pain → quantify pain → emotional impact → urgency → consequence-of-inaction. Used in mid-call when prospect is engaged. |
| **9-second opener (industry-standard)** | n/a — convention from Predictable Revenue + Outbound Squad / 30 Minutes to President's Club | The first 9 seconds determine whether the prospect stays on the line. Pattern: greet by name → state where you got the number (or honesty: "this is a cold call") → 5-second purpose statement → permission ask. |
| **Voicemail drop framework (≤15 seconds spoken)** | Industry-standard — codified in Smartlead / Aircall / JustCall playbooks | Voicemail content: name + company (3s) + reason for call referencing the prospect's specific situation (8s) + call-back number repeated twice (4s). Total ≤15 seconds when spoken at natural pace. |
| **Gatekeeper-handling patterns** (house-built — codified industry consensus) | Crewm8 | Three valid responses to "what is this regarding?" — (1) Specific-pain-no-buzzword reply; (2) Honest "cold call" reply; (3) Permission-ask-to-continue. NEVER pretend prior conversation; NEVER use vague buzzwords. |
| **TCPA + DNC compliance posture** (statute) | TCPA (47 USC § 227); FTC + FCC DNC Registry | DNC scrubbing mandatory; quiet hours 8am–9pm recipient local; SMS to mobile requires prior express written consent; B2B-cellphone is gray-area and treated as restricted by default. |

## Tools and Sources

### Dialer platforms (any one for API mode)

| Tool | Mode | Purpose |
|---|---|---|
| JustCall | API mode | Mid-market standard; CRM integrations; good multi-line. |
| Aircall | API mode | Strong on integrations; popular with EU teams. |
| Orum | API mode | Power-dialer (parallel-line); 3–4x dial volume. |
| Dialpad | API mode | AI-augmented call notes; growing adoption. |
| ConnectAndSell | API mode (enterprise) | Higher-volume managed dial service. |

### DNC scrubbing (mandatory for US)

| Tool | Notes |
|---|---|
| DNC.com | API or CSV upload; scrub against National DNC Registry + state lists. |
| ContactCenterCompliance.com | Same; alternate source. |
| Internal DNC list | Maintained by the user; never call records on internal DNC. |

### Manual / BYO

| Source | Notes |
|---|---|
| Native cellphone / desk phone | Per-recipient runbook with script + recipient context; manual disposition logging. |

### Source priority rule

For phone validation: **`phone_status [verified: mobile|landline]` from data-enrichment within 12 months** > **`phone_status [user-provided]`** > **agent inference (`[unverified — needs check]` — BLOCKS dial)**. NEVER dial a number with `[unverified]` provenance. Never dial DNC.

## Procedure

### 1. Validate prerequisites

Read scored Lead list; confirm `phone_status` distribution; load ICP P-T-O + message house; verify DNC scrub result for US recipients. Block on any gate failure.

### 2. Determine mode

Dialer API key set → API mode. Else seat → manual mode (paste-ready dial list + scripts). Else BYO → per-recipient runbook.

### 3. Filter recipient list

Apply gates:
- Drop `phone_status: dnc` (always).
- Drop `phone_status: invalid` / `phone_status: unverified` (route to `data-enrichment` or skip).
- Apply tier filter (default tier-1 SAL-eligible only).
- Drop records with unknown timezone.
- For non-US: apply jurisdiction-specific DNC equivalent (CRTC for Canada; UK CTPS; etc.).
- Drop records previously called within 90 days (re-touch rule per conventions §7).

### 4. Pre-flight: capacity check

Compute total dials needed vs `CALLS_PER_REP_PER_DAY_CAP` × rep_count × duration. Surface to user; recommend multi-rep, extended duration, or reduced volume if over.

### 5. Generate scripts

For each recipient, the skill produces 4 script artifacts:

**(a) 9-second opener** — pattern-interrupt + name + purpose + permission. Built from recipient's specific signal (hook from `data-enrichment`) + ICP pain anchor.

**(b) Discovery question set** — 4–6 questions following Bosworth + Sandler Pain Funnel. First 2 are open / curiosity; 3–4 quantify pain; 5–6 build buying-vision.

**(c) Gatekeeper-handler** — pre-written responses to "what is this regarding?" / "send me an email" / "we don't take cold calls" — 3 valid patterns; never lie or pretend prior conversation.

**(d) Voicemail drop** — ≤15 seconds spoken (≤45 words at natural pace). Specific reason for call (referencing the recipient's hook) + callback number twice.

Apply audit:
- **Word count**: opener ≤30 words, voicemail ≤45 words.
- **Cliché blocklist**: "Just calling to check in" / "I noticed your company" / generic "we help X do Y" openers.
- **No-pretend rule**: zero phrases implying prior conversation that didn't happen.
- **Hook citation**: opener and voicemail reference a citable hook from `data-enrichment` or are flagged `[unverified — needs check]` and downgraded to "honest cold call" pattern.

### 6. Compose Touch records (per conventions §2.1)

Touch entries with channel = `call` or `voicemail`; full provenance; `scheduled_for` (TCPA hours respected: 8am–9pm recipient local); compliance metadata (DNC scrub result, jurisdiction, quiet hours respected, `is_dnc: false`).

### 7. Schedule via dialer or hand off

API mode: create dial campaign in JustCall / Aircall / Orum / Dialpad via API; dialer paces dials within capacity caps. Manual: emit dial list (paste-ready) + script library + per-recipient context cards. BYO: per-recipient runbook with script + when-to-call.

### 8. Capture call disposition

For each dial, the dialer (API mode) or rep (manual / BYO) reports disposition:
- `connected-positive` → meeting booked or interest confirmed → exit cadence on this recipient → handoff to function-4 `discovery-call-prep`.
- `connected-not-now` → schedule callback per prospect's stated timing.
- `connected-not-interested` → exit cadence; flag for `objection-handling-library` (function-4).
- `voicemail-left` → mark in cadence; next touch may be email follow-up referencing the VM.
- `no-answer` → next dial attempt next business day.
- `wrong-person` → flag for `data-enrichment` correction.
- `bad-number` → mark `phone_status: invalid`; route for re-verification.

### 9. Push to CRM + emit run summary

Per conventions §11: per-dial push as `interaction:outreach` with disposition; run record as `interaction:research`. Run summary: dial volume, connect rate, conversation rate, meeting-booked rate, recommended next skill.

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: api | manual | byo
  dialer: justcall | aircall | orum | dialpad | connectandsell | native
  inputs:
    lead_count_input: <int>
    lead_count_eligible: <int>
    lead_count_dropped:
      dnc: <int>
      invalid_phone: <int>
      unverified_phone: <int>
      tier_filter: <int>
      timezone_unknown: <int>
      called_within_90d: <int>
  preconditions:
    dnc_scrub_completed: <bool>
    timezone_known_for_all: <bool>
  capacity:
    total_dials_planned: <int>
    daily_per_rep_cap: <int>
    rep_count: <int>
    duration_days: <int>
    headroom: <pct>
  scripts:
    opener_word_count: <int>
    voicemail_word_count: <int>
    discovery_question_count: <int>
  audit:
    cliche_flags: <int>
    no_pretend_violations: <int>
    hook_citation_failures: <int>
  warnings: [<string>]
  next_skill_recommendation: <campaign-management | reply-classification | discovery-call-prep>

per_recipient:
  - lead_id: <uuid>
    phone: <e164>
    phone_status: mobile | landline
    timezone: <string>
    scripts:
      opener: <text, ≤30 words>
      discovery_questions: [<text>, ...]
      gatekeeper_responses: [<text>, ...]
      voicemail: <text, ≤45 words>
    framework: cc20 + bosworth + sandler-pain-funnel
    hook_source_url: <permalink>
    scheduled_dial_window: <ISO start> – <ISO end>
    provenance:
      copy: [verified: <hook-url>] | [unverified — needs check]
    compliance:
      dnc_scrubbed: true
      jurisdiction: us | ca | other
      tcpa_hours_respected: true
      recipient_local_timezone: <string>
```

## Worked Example

> *All fictional entities below are tagged `[hypothetical]` — illustrative only.*

**User prompt**: "Set up a cold-call session for 50 Tier-1 SAL-eligible prospects. WorkflowDoc to Heads of Support at Series B SaaS. JustCall configured. DNC.com scrub completed."

**Step 1 — Validate**: 50 leads from `lead-scoring`, all SAL-eligible, all with `phone_status: mobile | landline [verified: data-enrichment]`. ICP P-T-O loaded. DNC scrub completed [verified: dnc.com api 2026-05-20]. Timezones known for all (derived from `company_location`).

**Step 2 — Mode**: `JUSTCALL_API_KEY` set → API mode.

**Step 3 — Filter**:
- Input: 50
- DNC drop: 2 (caught by scrub)
- Invalid phone drop: 1
- Tier filter (already SAL): 0
- Timezone unknown: 0
- Called within 90d: 4
- **Eligible: 43**

**Step 4 — Capacity**: 43 dials × planned 3-attempt cadence over 5 days = 129 dials. Single rep × 80/day cap = 400/day capacity. ~6% utilization. Plenty of headroom.

**Step 5 — Generate scripts** (sample for one recipient):

Recipient: Marcus Levy [hypothetical], VP Customer Support @ Volaris [hypothetical]
Hook: *"Volaris just hit 250 employees (March 2026 LinkedIn announcement)"* [verified: linkedin.com/company/volaris/posts/employee-milestone]
Pain anchor: *"Tribal knowledge across multiple tools; new hires take 6–8 weeks to ramp."*

Opener (28 words):
```
"Hi Marcus — this is Will from WorkflowDoc [hypothetical]. This is a cold call —
mind if I take 30 seconds? I noticed Volaris just crossed 250 — typically
the support stack starts to crack. Curious how you're handling onboarding."
```

Discovery questions (Bosworth + Sandler):
```
1. How is the support team handling new-hire ramp-up these days?
2. Where do new hires get stuck most — knowledge access or process?
3. If new hires were ramping in 3 weeks instead of 8, what would that
   change for you in Q3?
4. What have you tried so far?
5. What's keeping that from working?
6. Is fixing this a priority for you in the next 90 days, or further out?
```

Gatekeeper handler (3 patterns):
```
A. "It's about new-hire ramp time — I work with VPs of Support at Series B
   companies. Marcus's name came up because Volaris just crossed 250."
B. "Honest answer: it's a cold call. I'm trying to reach Marcus for a
   30-second permission check. Is he the right person for support tooling?"
C. "Happy to send an email if that's better — what's the best address?"
```

Voicemail drop (40 words ≈ 14 seconds):
```
"Hi Marcus, Will from WorkflowDoc [hypothetical]. Calling because Volaris
just crossed 250 — typically the support stack starts to crack at that
size. Curious how you're handling new-hire ramp.

Call back at 555-123-4567 — five-five-five, one-two-three, four-five-six-seven.
Thanks Marcus."
```

Provenance: `provenance.copy: [verified: linkedin.com/company/volaris/posts/employee-milestone]`

**Step 6 — Audit**: 0 cliché flags, 0 no-pretend violations, 0 hook-citation failures. Word counts: opener 28 ≤30 ✓ / voicemail 40 ≤45 ✓.

**Step 7 — Touch record**:
```yaml
touch_id: tch_2026-05-22_call_001
campaign_id: cmp_call_2026-05-22_q9k
cadence_id: cad_workflowdoc_call_3dial_5d_v1
lead_id: lea_marcus_levy_volaris
channel: call
touch_type: opener
sequence_position: 1
scheduled_for: 2026-05-23T10:30:00-08:00   # 10:30am recipient local, weekday
content:
  opener: "<as above>"
  discovery_questions: ["<6 questions>"]
  gatekeeper_responses: ["<3 patterns>"]
  voicemail: "<≤15s drop>"
  framework: cc20+bosworth+sandler
  hook_source_url: linkedin.com/company/volaris/posts/employee-milestone [hypothetical]
sender:
  rep_name: Will [hypothetical]
  caller_id_phone: +15551234567
compliance:
  dnc_scrubbed: true
  recipient_jurisdiction: us
  tcpa_hours_respected: true
  recipient_local_timezone: America/New_York
  honors_quiet_hours: true
provenance:
  copy: [verified: linkedin.com/company/volaris/posts/employee-milestone]
  hook: [verified: data-enrichment:enrich_2026-05-04_t3p]
status: scheduled
```

**Step 8 — Schedule via JustCall**: Campaign `cad_workflowdoc_call_3dial_5d_v1` created in JustCall. 43 prospects in dial list. 3 attempt windows: D+0 (10:30am local), D+2 (2:30pm local), D+4 (10:30am local). All within TCPA 8am–9pm window.

**Step 9 — Run summary**:
```
WorkflowDoc Cold Call Run [hypothetical]
Run ID: cmp_call_2026-05-22_q9k
Mode: API (JustCall). Cadence: call-3dial-5d-v1.
Filter: 50 → 43 eligible (2 DNC, 1 invalid, 4 called within 90d)
Capacity: 129 dials over 5d / 400/day max / 6% utilization
Scripts: opener avg 27 words / voicemail avg 39 words / 6 discovery questions
Audit: 0 cliché flags / 0 no-pretend violations / 0 hook-citation failures
Compliance: 43/43 DNC-scrubbed; 100% within TCPA hours
Recommended next: campaign-management (track connect rate, target 8–12% of dials)
```

## Heuristics

- **Connect rate is the primary metric.** 8–12% (connections / dials attempted) is healthy. Below 6% = bad targeting, bad time of day, or bad list (phones gone stale).
- **Voicemail-to-callback is 1–3%.** Don't expect miracles; voicemails compound across multiple touches. Skip voicemails on attempts 4+ — diminishing returns.
- **The honest "this is a cold call" pattern beats the buzzword evasion.** Prospects respect honesty; they delete buzzword attempts.
- **9-second rule is real.** Get to the point AND ask permission within 9 seconds or they hang up.
- **Permission-ask reduces resistance.** "Mind if I take 30 seconds?" lets the prospect grant or deny — those who say yes are listening; those who say no save your time.
- **Mid-day (10am–noon, 2pm–4pm recipient local) outperforms early/late.** Avoid Monday before 10am and Friday after 3pm.
- **Mobile dials connect higher than desk lines** — but require TCPA care. Direct mobile (verified) is the highest-value channel; treat as Tier-1-only.
- **Don't pitch on the first call.** Discovery, not selling. The meeting is the only goal.
- **Voicemail tone matters more than email tone.** Conversational, lower-pitched, slower. Listen back at 1.0x; if it sounds rushed, re-record.
- **Use the prospect's name early and once more.** Twice in 30 seconds; more = manipulative; zero = unmemorable.

## Edge Cases

- **B2B mobile (cellphone) without explicit consent.** TCPA gray-area; some legal interpretations allow B2B-to-B2B-cellphone for business purposes. The skill defaults to "treat as restricted" and recommends voicemail-only on first dial; user can override per their counsel.
- **DNC scrub stale (>30 days old).** Refresh required; many states require recent scrubs (some weekly).
- **Multi-language recipient.** If recipient's likely language is not English, surface; switch script language with translation user-verified; never auto-translate.
- **Power dialer (Orum, ConnectAndSell).** Multi-line parallel dialing increases connect rate but requires "click to take" UX — ensures rep is human-paced when prospect connects (TCPA: prerecorded auto-dial without consent is illegal).
- **Number-portability** (mobile-to-VOIP migration). VOIP numbers behave like mobile for TCPA purposes; treat as restricted.
- **"Press 1 to be removed" or similar IVRs** on the recipient's line. Honor immediately; mark `phone_status: dnc-internal`.
- **Recipient asks to stop calling mid-call.** Honor immediately; mark internal-DNC.
- **Recipient asks about how you got the number.** Honest answer: "<source>". Never lie.
- **Dialer rate-limit hit.** JustCall / Aircall enforce per-account dial limits; pause; resume next day.
- **Reply mid-cadence (positive or negative on email/LI).** Pause call cadence on that recipient; route through `reply-classification` (function-4).

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Dialer API auth fails (401) | JustCall/Aircall returns 401 | Confirm key; do NOT retry silently; offer manual mode (paste-ready dial list). |
| DNC scrub API fails | API returns 503 | Retry; if still failing, BLOCK dialing until scrub completes. Cannot dial without it. |
| Recipient connected but rep hand-off failed | dialer error | Retry connection; record disposition `connect-then-drop`; flag for re-dial. |
| Voicemail box full | dialer reports failure | Mark `vm-not-left`; next dial attempt without voicemail. |
| Wrong-person on the line | gatekeeper transfer | Capture: ask for correct contact; flag `data-enrichment` for correction; mark original record. |
| Rep dialed during quiet hours (manual mode) | TCPA violation risk | Hard-stop the dial; surface error; require user retraining; log near-miss for audit. |
| TCPA quiet-hours edge (recipient travels across timezones) | timezone mismatch detected | Default to recipient's `company_location` timezone; document edge case; if frequent traveler flagged in Lead, defer to user judgment. |
| Internal DNC list not synced | risk of dialing internal-DNC | BLOCK dial until internal-DNC list refreshed against active list. |
| Mobile carrier blocked outgoing call | dialer reports "blocked" | Possible spam-flag on caller ID; check `Hiya` / `Truecaller` for caller ID reputation; remediate via dialer's caller-ID-reputation tools. |
| Dialer-side rate limit | 429 from dialer API | Backoff; resume next day or expand rep pool. |

## Pitfalls

- **Calling DNC numbers.** TCPA fines $500–$1500 per violation. Hard rule.
- **Calling outside 8am–9pm recipient local.** Same.
- **SMS to mobile without prior express written consent.** Same.
- **Buzzword opener.** "I'm calling to discuss strategic value" → instant hangup.
- **Pretending prior conversation.** "Following up on our chat last week" when there was no chat — dishonest, illegal in some jurisdictions, and erodes trust.
- **No permission ask.** "Hi Marcus, I'm calling about WorkflowDoc..." launches into pitch; prospect tunes out by second 3.
- **Voicemail >15 seconds.** Long voicemails get deleted. ≤15 spoken is the rule.
- **Skipping discovery to pitch.** "We do X for Y, can we book a demo?" — fails. The call is for discovery, not closing.
- **Calling the same recipient daily.** 1–2 attempts per week max; respect their inbox-equivalent for phone.
- **Treating voicemail-only as zero-value.** Voicemails compound; multi-touch shows persistence (in moderation).
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (recipients, companies, hook references, dates, customer outcomes, dollar figures) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. Hook URLs gate the opener and voicemail; absence forces the "honest cold call" pattern with no specific reference.
- **Calling a number with `[unverified]` provenance.** Phone-status verification is mandatory; agent inference of a number is forbidden.

## Verification

The run is real when: (a) 100% of dials have DNC scrub completed within 30 days; (b) 100% of dials within TCPA 8am–9pm recipient local hours; (c) every Touch's `provenance.copy` resolves to a hook URL or is flagged `[unverified]` (then downgraded to honest cold-call pattern); (d) connect rate ≥6% (below = bad targeting/list/timing); (e) zero "pretend prior conversation" violations in scripts; (f) voicemail word count ≤45.

## Done Criteria

1. Mode determined (api / manual / byo); dialer or runbook prepared.
2. DNC scrub completed for all US recipients within 30 days; recorded.
3. Recipient filter applied: DNC dropped, invalid/unverified phones dropped, tier filter, called-within-90d filter.
4. Capacity check passed; multi-rep / extended duration if over.
5. Per-recipient scripts generated (opener / discovery / gatekeeper / voicemail) with framework attribution and audit-pass.
6. Hook citation enforced (opener + voicemail reference verified hook OR downgrade to honest cold-call pattern).
7. Touch records assembled per conventions §2.1 with TCPA hours respected, jurisdiction tagged.
8. Scheduled (API) or handed off (manual / BYO); push to CRM emitted; run summary one-screen.

## Eval Cases

### Case 1 — full API mode, Tier-1 SAL list

Input: 50 Tier-1 SAL-eligible leads, 100% phone-verified, JustCall + DNC.com configured.

Expected: ~43–46 eligible after filters; per-recipient 4-script bundle; 3-dial cadence over 5 days; connect rate target 8–12%; voicemail-to-callback 1–3%; meeting-rate target 0.5–1.5% of dials.

### Case 2 — manual mode, founder-led calls

Input: 12 named accounts, founder will dial personally, no dialer.

Expected: per-recipient runbook with script + recipient context card; founder dials at 1.0x speed (vs power-dialer); call disposition logged manually after each attempt. Recommends `discovery-call-prep` (function-4) when meetings book.

### Case 3 — power-dialer, high-volume

Input: 200 prospects, Orum power-dialer, 3 reps.

Expected: parallel-line dialing with click-to-take UX; ~3x connect rate efficiency vs single-line; reps still each respect 80/day connection-attempt cap; TCPA hours strictly enforced across recipient timezones.

### Case 4 — DNC scrub stale

Input: scrub run 45 days ago.

Expected: BLOCK dialing; require fresh scrub (≤30 days); resume after refresh.

### Case 5 — multi-channel cadence layer

Input: existing email + LI cadence; cold call at position 5 (after email touches 1, 2 and LI connection request 3).

Expected: only the call Touch produced; opener references prior touches' framing context (without quoting them); scheduled at recipient local 10:30am; voicemail referenced if no connect.

## Guardrails

### Provenance (anti-fabrication)

Per §10 of conventions: opener and voicemail reference verified hooks OR downgrade to honest cold-call pattern. Phone numbers MUST be `[verified]` or `[user-provided]` from data-enrichment; agent-inferred phones BLOCKED. Worked-example fictional entities tagged inline.

### Evidence

Every dial has DNC-scrub timestamp + jurisdiction + TCPA-hours-respected flag. Audit-trail per dial.

### Scope

This skill writes call scripts + orchestrates dial sessions. It does NOT discover phones (`data-enrichment`), classify replies (`reply-classification` function-4), or prep meetings (`discovery-call-prep` function-4). Avoid scope creep.

### Framing

Run summary uses operational language. Per-recipient scripts auditable.

### Bias

Cold calling over-converts on US/UK markets; under-performs in EU markets where cold-call culture is more restrained. Surface; recommend email-first in those geographies.

### Ethics

TCPA compliance non-negotiable. DNC scrubbing mandatory. Quiet hours respected. SMS to mobile requires explicit prior consent. "Press 1 to be removed" honored immediately. Lying about prior conversation forbidden.

### Freshness

DNC scrubs decay (30-day max recommended; some states require shorter). Phone status decays (~12 months). Stale data = compliance risk and waste.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Dial campaign running | `campaign-management` | Campaign id + connect/conversation rates |
| Multi-channel cadence | `multi-channel-cadence` | Call cadence + email/LI positions |
| Phone coverage <50% | `data-enrichment` (Hunter/Lusha phone discovery) | Lead list + missing-phone records |
| Meeting booked from call | `discovery-call-prep` (function-4, planned) | Meeting context + recipient profile |
| Reply on email/LI mid-call-cadence | `reply-classification` (function-4, planned) | Reply text + Touch id |
| Connect rate <6% | back to this skill (rewrite scripts) OR `lead-scoring` (re-tier list) | Current scripts + connect-rate metrics |

## Push to CRM

After scheduling, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each scheduled dial (draft) | `interaction` (type: `research`) | `relevance` = "Call scheduled for <ISO> via <dialer> with opener referencing <hook URL>"; `tags: "#scheduled #call #function-3"` |
| Each completed dial (with disposition) | `interaction` (type: `outreach`) | `relevance` = disposition + duration + notes + provenance; `tags: "#sent #call-<connected|voicemail|no-answer> #function-3"` |
| Cadence + campaign run record | `interaction` (type: `research`) | `relevance` = run summary; `tags: "#cold-calling-run #function-3"` |
| Last-touched timestamp + phone_status changes | `person` (PATCH via dedup key) | `last_touched_at`, `last_touched_channel: call`, `phone_status` updated if changed |
| `[unverified — needs check]` (phone or hook) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #cold-calling"`; never `outreach` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
JUSTCALL_API_KEY=     # or AIRCALL / ORUM / DIALPAD / CONNECTANDSELL
DNC_COM_API_KEY=      # mandatory for US dialing
CONTACTCENTERCOMPLIANCE_API_KEY=
CALLS_PER_REP_PER_DAY_CAP=80
VOICEMAILS_PER_REP_PER_DAY_CAP=40
```

### Source tag

`source: "skill:cold-calling:v2.0.0"`

### Example push (completed call — connected)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Volaris",
    "contactName": "Marcus Levy",
    "contactPhone": "+15551234567",
    "tags": "#sent #call-connected #cc20-pain #function-3",
    "relevance": "Cold call connected 2026-05-23T10:32 ET (recipient local). Duration: 4m 12s. Disposition: connect-positive — Marcus interested in 3-week ramp; meeting booked 2026-05-30T14:00. Hook: Volaris 250-employee milestone [verified: linkedin.com/company/volaris/posts/employee-milestone]. Discovery: pain confirmed (8wk new-hire ramp), urgency Q3, champion identified. Rep: Will. Cadence: cad_workflowdoc_call_3dial_5d_v1. Recommended next: discovery-call-prep.",
    "source": "skill:cold-calling:v2.0.0"
  }'
```

### Example push (voicemail left)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#sent #call-voicemail #function-3",
    "relevance": "Voicemail left 2026-05-23T10:30 ET. Drop length: 14s. Hook reference: Volaris 250-employee milestone. Callback number repeated twice. Next attempt: D+2 (2:30pm ET).",
    "source": "skill:cold-calling:v2.0.0"
  }'
```

### Example push (run record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#cold-calling-run #function-3",
    "relevance": "Cold call run cmp_call_2026-05-22_q9k. Mode: API (JustCall). Cadence: call-3dial-5d-v1. Filter: 50 → 43 eligible (2 DNC, 1 invalid, 4 called <90d). Capacity: 129 dials / 400/day max / 6% utilization. Compliance: 43/43 DNC-scrubbed, 100% TCPA-hours. Audit: 0 cliché / 0 no-pretend / 0 hook-citation failures. Recommended next: campaign-management (target connect rate ≥8%).",
    "source": "skill:cold-calling:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per conventions §10.3:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Dial occurs; pushes as `interaction:outreach`. |
| `[unverified — needs check]` | Dial is BLOCKED. Pushes ONLY as `interaction:research` with `#unverified #review-required #cold-calling` tags. |
| `[hypothetical]` | Never dials; never pushes. Local artifact only. |

### When NOT to push

- Drafts never scheduled — local artifact only.
- Dials blocked at pre-flight (DNC, invalid phone, unknown timezone, capacity) — push as `interaction:research` with block reason; never `outreach`.
- `[unverified]` phone or hook — see provenance routing.
- `[hypothetical]` — never.
- Quiet-hours violation attempted (rare manual-mode error) — log near-miss for audit; do NOT push as completed call.
