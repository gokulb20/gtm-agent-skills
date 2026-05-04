---
name: email-infrastructure-setup
description: Set up and verify the email infrastructure — purchase / configure dedicated outbound domain(s), publish SPF + DKIM + DMARC, configure RFC 8058 one-click List-Unsubscribe, run a 14+ day warmup, and emit the readiness flag that gates `cold-email-sequence` and `multi-channel-cadence`. Use when a new outbound program is starting, when a primary domain's deliverability has degraded, when migrating sending platforms, or when Google/Microsoft Feb 2024 bulk-sender enforcement breaks an existing sender.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, outreach, deliverability, dns, warmup, function-3]
related_skills:
  - cold-email-sequence
  - multi-channel-cadence
  - campaign-management
inputs_required:
  - primary-brand-domain
  - sending-platform-choice
  - dns-provider-access-or-credentials
  - jurisdiction-and-physical-address
  - target-daily-volume
  - run-purpose-tag
deliverables:
  - dedicated-outbound-domain-list
  - spf-dkim-dmarc-records-published
  - rfc-8058-one-click-unsubscribe-config
  - warmup-schedule-and-state
  - sender-reputation-baseline-report
  - email-infrastructure-readiness-flag
  - infrastructure-setup-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Email Infrastructure Setup

Establish the foundation every other email skill depends on: dedicated outbound domain(s) separated from the brand domain, properly authenticated (SPF + DKIM + DMARC), warmed up to ≥70 reputation score, and configured for Google/Microsoft Feb 2024 bulk-sender compliance. Emits the binary `readiness_flag` that `cold-email-sequence` checks before scheduling any send.

> *Worked example uses WorkflowDoc (fictional, function-1 carry-over) as the seller; procedure is vertical-agnostic. Shared rules in `function-3-skills/function-3-conventions.md`.*

## Purpose

Bad email infrastructure is the silent killer of outbound programs. Even perfect copy from a domain with bad SPF alignment lands in spam. This skill: separates cold-outbound from the brand domain (reputation isolation), publishes the four DNS records that authenticate sends (SPF, DKIM, DMARC, MX), configures RFC 8058 one-click List-Unsubscribe (Google/MS 2024 mandatory), runs a 14+ day warmup ramp, emits the readiness flag the rest of function-3 gates on. Goal: a sending posture that survives the Feb 2024 enforcement era.

## When to Use

- "Set up a new outbound domain for our cold email program."
- "Our deliverability tanked — audit and fix."
- "Migrating from Outreach.io to Smartlead — set up the new infrastructure."
- "Google sent us a bulk-sender warning email."
- "Adding a second outbound domain to scale volume."
- Pre-launch foundation for any new outbound program.
- Recovery after complaint-rate spike or blacklist event.

## Inputs Required

1. **Primary brand domain** — e.g. `workflowdoc.com`. Skill registers/configures a variant (e.g. `workflowdoc-mail.com`) — never the brand domain.
2. **Sending platform choice** — Smartlead / Instantly / Lemlist / Outreach / Salesloft / native Gmail Workspace / native M365.
3. **DNS provider access** — `CLOUDFLARE_API_KEY` / `GODADDY_API_KEY` / `NAMECHEAP_API_KEY`, or admin login, or paste-ready blob output.
4. **Jurisdiction + physical address** — CAN-SPAM (US), GDPR (EU/UK), CASL (CA) footer requirements.
5. **Target daily volume** — drives sender count and ramp schedule.
6. **Run purpose tag**.
7. (Optional) Existing infrastructure for migration diff.

## Quick Reference

| Concept | Value |
|---|---|
| **Modes** | Automated (DNS API) / Guided (paste-ready blob) / Audit-only (read existing) |
| **Reputation isolation** | Cold outbound from `brand-mail.com` variant, NEVER from brand domain |
| **DNS records** | SPF, DKIM (≥2048-bit), DMARC (start `p=none`), MX, rDNS/PTR |
| **One-click List-Unsubscribe** | RFC 8058 — `List-Unsubscribe-Post: List-Unsubscribe=One-Click` (Google/MS 2024 mandatory) |
| **DMARC ramp** | `p=none` (Day 0) → `p=quarantine` (Day +30 if reports clean) → `p=reject` (high-stakes only) |
| **Warmup duration** | 21–30 days for new/cold domains; 14-day floor only for aged/warmed domains; 30-day floor for >200/day target volume |
| **Warmup score threshold** | ≥70 to flip readiness flag |
| **Domain age threshold** | ≥14 days |
| **Postmaster Tools gate** | "High" or "Medium" only; "Low"/"Bad" → extend warmup |
| **Daily caps** | Start 5/day → ramp +5 every 5 days → 30/day after 14 days |
| **Bulk-sender mode** | >5,000/day to Gmail/Yahoo (Google Feb 2024) OR Microsoft (May 5, 2025) → mandatory DMARC + 0.3% complaint cap. Microsoft non-compliance bounces with `550; 5.7.515 Access denied, sending domain does not meet the required authentication level.` |
| **Complaint thresholds** | Practitioner target 0.10% / Google enforcement ceiling 0.30% (dual-tier — hold the program well below 0.10%; 0.30% triggers enforcement) |
| **Reputation cross-check** | Google Postmaster + Microsoft SNDS + TalosIntel + MXToolbox |
| **Footer (US)** | Physical postal address mandatory (CAN-SPAM) |
| **Footer (EU/UK)** | Legitimate-interest statement + opt-out link + DPO contact (GDPR) |
| **Footer (CA)** | Identification + opt-out (CASL) |

## Procedure

### 1. Audit existing infrastructure
Pull current SPF/DKIM/DMARC via MXToolbox if migrating. Surface alignment + key age + DMARC policy. Fix obvious mis-config before new setup.

### 2. Choose dedicated outbound domain(s)
Propose 2–3 brand variants (`<brand>-mail.com`, `get<brand>.com`, `<brand>-team.com`). NOT the brand domain. For >200/day, plan 2+ outbound domains for rotation.

### 3. Register + configure DNS
Per outbound domain: register via Cloudflare/Namecheap/GoDaddy; publish SPF (`v=spf1 include:<platform> -all`), DKIM (≥2048-bit, sending-platform-generated), DMARC (`p=none; rua=...`), MX, rDNS. Watch SPF 10-lookup limit.

### 4. Configure RFC 8058 one-click List-Unsubscribe
Both headers on every send: `List-Unsubscribe: <mailto:>, <https:>`, `List-Unsubscribe-Post: List=Unsubscribe=One-Click`. Process unsub within 24h. Mandatory under Google/MS 2024 for >5k/day senders.

### 5. Configure jurisdiction-aware footers
US: physical address (CAN-SPAM). EU/UK: LIA + opt-out + DPO (GDPR). CA: identification + opt-out (CASL). Templates feed `cold-email-sequence` per recipient jurisdiction.

### 6. Initiate warmup ramp
Day 0: enable platform's warmup feature; cap 5/day. Day +5: 10/day. Day +10: 20/day. Day +14: 30/day if Postmaster Medium+. No shortcuts.

### 7. Run reputation baseline (Day +14)
Pull Google Postmaster (domain + IP), Microsoft SNDS, TalosIntel, MXToolbox audit. Want Postmaster High/Medium, SNDS green/yellow, TalosIntel neutral+, MXToolbox no red flags.

### 8. Emit readiness flag
All gates pass → `readiness_flag: true` + `ready_for_sends_per_day: <int>`. Any gate fails → flag false + enumerated failed gates + remediation per gate.

### 9. Push to CRM + handoff
`interaction:research` with full audit + readiness flag. Run summary. If green → recommend `cold-email-sequence`. If broken → remediation steps.

## Output Format

- DNS records published (per domain): SPF / DKIM / DMARC / MX / rDNS
- One-click List-Unsubscribe config (RFC 8058)
- Footer templates per jurisdiction (US / EU / UK / CA / etc.)
- Warmup schedule + current state (day, score, cap)
- Reputation baseline (Postmaster + SNDS + TalosIntel + MXToolbox)
- `readiness_flag: true | false` + `failed_gates` if false
- Run record: full audit, recommended next skill (`cold-email-sequence` if green; remediation if not)

## Done Criteria

1. Mode determined; outbound domain(s) chosen (NOT brand domain).
2. DNS records published per domain: SPF, DKIM ≥2048-bit, DMARC `p=none` start, MX, rDNS verified.
3. RFC 8058 one-click List-Unsubscribe configured.
4. CAN-SPAM / GDPR / CASL footer templates registered.
5. Warmup initiated; ramp schedule documented.
6. Reputation baseline pulled (Postmaster + SNDS + TalosIntel + MXToolbox).
7. `readiness_flag` emitted with `ready_for_sends_per_day` (or `false` + `failed_gates`).
8. Setup record pushed; recommended next skill stated.

## Pitfalls

- **Sending from the brand domain.** Reputation contamination is unrecoverable.
- **Skipping warmup.** Day-1 cold-blast = blacklist.
- **DMARC straight to `p=reject`.** Breaks transactional + reply email; surface before strict policy.
- **1024-bit DKIM keys.** Yahoo treats as deprecated; Google deprioritizes.
- **No List-Unsubscribe header.** Auto-spam under Google 2024 rules for >5k/day senders.
- **No physical address (CAN-SPAM US).** Legal violation.
- **Single domain at high volume.** No reputation isolation; one event = whole program down.
- **Ignoring DMARC reports.** Free signal you're already paying for.
- **Treating warmup score as the only signal.** Cross-check with Postmaster Tools and SNDS.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (domains, IPs, reputation scores, dates, audit findings) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. NEVER invent a Postmaster Tools verdict, a warmup score, or a DKIM key state without the source.
- **Not retesting after changes.** DNS change → wait propagation → re-audit → confirm before flipping flag.

## Verification

Setup is real when: every DNS record resolves correctly via MXToolbox + dig; one-click unsubscribe processes a test request within 24h; physical address renders in actual sent test emails; Postmaster Tools and SNDS both show valid baseline (not "Bad" / red); warmup score climbs deterministically per ramp schedule; readiness flag flips deterministically based on gate set; a test send to real Gmail and real Outlook inboxes both land in primary tab.

## Example

**User prompt:** "Set up email infrastructure for outbound. Brand workflowdoc.com `[hypothetical]`. Smartlead. Cloudflare. Target 80 sends/day."
**What should happen:** Audit existing brand DNS (SPF for inbound exists, no outbound DKIM/DMARC). Propose `workflowdoc-mail.com` `[hypothetical]`. Register via Cloudflare API. Publish SPF (`v=spf1 include:smtp.smartlead.ai -all`), DKIM (Smartlead-generated 2048-bit), DMARC (`p=none; rua=mailto:dmarc-reports@workflowdoc.com`), MX (Smartlead), rDNS verified. Configure RFC 8058 unsub. Footer templates registered. Warmup Day 0 with cap 5/day. Day +14 baseline: Postmaster Medium, SNDS green, TalosIntel neutral, warmup score 78 `[hypothetical]`. Readiness flag TRUE, 30/day ready. Recommend `cold-email-sequence`.

**User prompt:** "Our deliverability tanked. Diagnose."
**What should happen:** Audit-only mode. Pull current Postmaster Tools (shows "Low" reputation), SNDS (yellow), MXToolbox (DMARC reports show 30% non-aligned). Surface root cause: SPF doesn't include a third-party sender being used by marketing team — DMARC failures across the board. Recommend: add the third-party sender to SPF (within 10-lookup limit) OR ack as legitimate non-aligned. Pause cold sends 7d to recover reputation. Re-audit Day +7.

**User prompt:** "I have a paid Cloudflare account but no API key. Walk me through setup."
**What should happen:** Guided mode. Generate paste-ready DNS blob: 4 records as text strings. Step-by-step Cloudflare UI walkthrough. After user reports records added, skill verifies via MXToolbox (separate from Cloudflare API). Once propagated (often 1–6h), warmup initiates. Day +14 readiness check.

## Linked Skills

- Infrastructure ready (flag=true) → `cold-email-sequence`
- Infrastructure broken mid-program → back to this skill (audit-only mode)
- Multi-channel cadence with email leg → `multi-channel-cadence`
- Active campaign monitoring → `campaign-management`
- Spam complaint spike → back to this skill (recovery mode) + audit upstream `data-enrichment`
- Migrating sending platform → back to this skill (migration mode)

## Push to CRM

Persist agent-actionable infrastructure state to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-3-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Infrastructure setup record | `interaction` (type: `research`) | `relevance` = full DNS audit + warmup state + reputation baseline + readiness flag; `tags: "#email-infrastructure-setup #function-3"` |
| Readiness flag flip event (true / false) | `interaction` (type: `research`) | `relevance` = "readiness_flag flipped to <true|false> on <date> due to <gates>"; `tags: "#readiness-flag #function-3"` |
| Reputation baseline | `interaction` (type: `research`) | `relevance` = baseline values for `campaign-management` to diff against later |

This skill does NOT push `person` or `company` records — infrastructure is system-state, not entity-state.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
SMARTLEAD_API_KEY=     # or sending platform of choice
CLOUDFLARE_API_KEY=    # or DNS provider of choice
MXTOOLBOX_API_KEY=
EASYDMARC_API_KEY=
GOOGLE_POSTMASTER_OAUTH_TOKEN=
MICROSOFT_SNDS_API_KEY=
WARMUP_SCORE_THRESHOLD=70
WARMED_UP_DAYS_THRESHOLD=14
```

### Source tag

`source: "skill:email-infrastructure-setup:v2.0.0"`

### Example push (setup record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "tags": "#email-infrastructure-setup #function-3",
    "relevance": "Email infrastructure setup infra_2026-04-19_w0d [hypothetical]. Brand: workflowdoc.com [hypothetical]. Outbound: workflowdoc-mail.com [hypothetical] (Smartlead). DNS: SPF ✓ DKIM 2048 ✓ DMARC p=none ✓ MX ✓ rDNS ✓. List-Unsubscribe RFC 8058 ✓. Footer: CAN-SPAM US + GDPR EU/UK + CASL CA. Warmup Day +14, score 78 [hypothetical]. Postmaster Medium / SNDS green / Talos neutral. Readiness flag: TRUE. Ready 30/day. DMARC ramp to quarantine in 30d.",
    "source": "skill:email-infrastructure-setup:v2.0.0"
  }'
```

### Example push (readiness flag flip — unhealthy)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#readiness-flag #function-3 #unhealthy",
    "relevance": "readiness_flag flipped to FALSE on 2026-05-22. Failed gates: postmaster_reputation=Bad (was Medium 7d ago); complaint_rate=0.4% (above 0.3% pause threshold). Recommended remediation: pause all sends, audit recent batches for list-quality issues, extend warmup 14d, re-pull baseline.",
    "source": "skill:email-infrastructure-setup:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping. |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required #email-infrastructure` tags. Readiness flag stays `false`. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

### When NOT to push

- Audit-only mode produced no changes — push the audit findings as `interaction:research` with `#audit-only` tag; no infrastructure setup record.
- Setup attempted but DNS API failed — push `interaction:research` with `#setup-failed` and detailed error; readiness stays false.
- `[hypothetical]` — never.
