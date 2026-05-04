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

Establish the foundation that every other email skill depends on: dedicated outbound domain(s) separated from the brand domain, properly authenticated (SPF + DKIM + DMARC), warmed up to ≥70 reputation score, and configured for Google/Microsoft Feb 2024 bulk-sender compliance. Emits the binary `readiness_flag` that `cold-email-sequence` checks before scheduling any send. Without this skill green, no other email skill ships.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The DNS, warmup, and reputation procedures are vertical-agnostic and apply to any B2B GTM context.*

> *Shared rules — Touch / Cadence / Campaign schemas, capacity caps, deliverability baseline (Google/MS 2024, Apple MPP), compliance, anti-fab — live in `function-3-skills/function-3-conventions.md`. This skill assumes it.*

## Purpose

Bad email infrastructure is the silent killer of outbound programs. Even perfect copy from a domain with bad SPF alignment lands in spam. Even a warmed domain that hits 50 sends/day from cold start gets blacklisted. This skill: (1) separates the cold-outbound sending from the brand domain so reputation damage is contained, (2) publishes the four DNS records that authenticate sends (SPF, DKIM, DMARC, optionally BIMI), (3) configures RFC 8058 one-click List-Unsubscribe so Google and Microsoft accept the bulk-sender obligations, (4) runs a 14+ day warmup ramp to legitimize the new sender, (5) emits the readiness flag the rest of function-3 gates on. Goal: a sending posture that survives the Feb 2024 enforcement era.

## When to Use

- "Set up a new outbound domain for our cold email program."
- "Our deliverability tanked — audit and fix."
- "Migrating from Outreach.io to Smartlead — set up the new infrastructure."
- "Google sent us a bulk-sender warning email."
- "Adding a second outbound domain to scale volume."
- Pre-launch foundation work for any new outbound program.
- Recovery after a complaint-rate spike or a blacklist event.

### Do NOT use this skill when

- Sending volume is genuinely <50/week and from a single user mailbox — the brand domain is fine; warmup-grade infrastructure is overkill.
- The user is on a transactional email service (Postmark, SendGrid for app email) — those are different from cold outbound; this skill is for cold sends.
- Primary brand domain is the chosen sending domain — refuse with explanation: cold outbound from the brand domain risks brand-domain reputation; recommend dedicated outbound domain.
- The user's DNS provider is unsupported and they have no admin access — produce DNS records as a paste-ready blob; they execute manually.

## Inputs Required

### Table

| # | Input | Required | Source | Notes |
|---|---|---|---|---|
| 1 | Primary brand domain | yes | user | E.g. `workflowdoc.com`. The skill registers/configures `workflowdoc-mail.com` or `workflowdoc-team.com` (variant — never the brand domain). |
| 2 | Sending platform choice | yes | user | Smartlead / Instantly / Lemlist / Outreach / Salesloft / native (Gmail Workspace / M365). Determines the DKIM key source and per-platform SPF includes. |
| 3 | DNS provider access | yes | user | API key (`CLOUDFLARE_API_KEY` / `GODADDY_API_KEY` / etc.) for automated mode; admin login for manual mode; paste-ready blob output if neither. |
| 4 | Jurisdiction + physical address | yes | user | CAN-SPAM (US), GDPR (EU/UK), CASL (CA) — physical address required in email footer; surfaces here. |
| 5 | Target daily volume | yes | user | Drives sender count and ramp schedule. <30/day = single sender; 30–200/day = 2–4 senders; 200+ = enterprise mode (multi-domain). |
| 6 | Run purpose tag | yes | user | Stamped on the infrastructure record. |
| 7 | Existing infrastructure (optional) | no | user / DNS lookup | If migrating, pull existing SPF/DKIM/DMARC for diff. |

### Fallback intake script

> "Email infrastructure is foundational — every other email skill depends on this being green. Three modes:
> - Automated: I configure DNS via your provider's API and your sending platform's API.
> - Guided: I produce a step-by-step DNS-paste blob + sending-platform setup checklist; you click through.
> - Audit-only: I check your existing setup and flag what's broken (no changes).
>
> Two questions:
> - Brand domain (e.g. `workflowdoc.com`)? I'll set up a dedicated outbound variant (e.g. `workflowdoc-mail.com`).
> - Sending platform — Smartlead, Instantly, Lemlist, native Gmail Workspace, or other?"

### Input validation rules

- Brand domain absent → block; can't propose a sender domain without it.
- User chose brand domain as sender → refuse; explain reputation-isolation rationale; offer 2–3 variant options.
- Target daily volume >5,000 to a single mailbox provider (Gmail/Yahoo) → trigger Google + Microsoft 2024 bulk-sender mode (mandatory: DMARC enforced, one-click List-Unsubscribe, complaint rate <0.3%); add ramp time.
- DNS provider unsupported AND no admin access → produce paste-ready blob; do NOT silently skip.
- Physical address absent for CAN-SPAM jurisdiction → block until provided (legal requirement for cold outbound footer).

## Frameworks Used

| Framework | Author | What we apply |
|---|---|---|
| **SPF / DKIM / DMARC stack** | IETF: RFC 7208 (SPF), RFC 6376 (DKIM), RFC 7489 (DMARC) | The three authentication records that every Touch's sending domain MUST publish. SPF lists allowed sending IPs; DKIM signs the message body; DMARC tells receivers what to do with non-authenticated mail and aggregates reports. |
| **One-click List-Unsubscribe** | IETF RFC 8058 (2017) | The `List-Unsubscribe` + `List-Unsubscribe-Post` headers that let Gmail / Outlook show a one-click unsubscribe button. Mandatory under Google + Microsoft Feb 2024 rules for bulk senders. |
| **Google + Microsoft Feb 2024 bulk sender requirements** | Google + Microsoft (industry-standard; published Oct 2023, enforced Feb 2024) | Authentication required, one-click unsubscribe, complaint rate <0.3% (warning at 0.1%), domain alignment between From: and DKIM. The skill encodes these as hard preconditions for the readiness flag. |
| **Domain warmup methodology** (industry-standard, codified) | Smartlead / Mailreach / Warmup Inbox playbooks | A new domain ramps from 5 sends/day to capacity over 14–30 days, with reciprocal reads + replies + folder-moves to build positive reputation. Deterministic schedule per `WARMUP_SCORE_THRESHOLD`. |
| **Sender reputation scoring** (industry-standard, free tools) | Google Postmaster Tools, Microsoft SNDS, Cisco TalosIntel | Read-only signals that inform `readiness_flag` decisions and `campaign-management` ongoing monitoring. Never the only signal — always cross-check. |
| **Domain reputation isolation** (house-built — operational best practice) | Crewm8 — codified industry consensus | Cold outbound is sent from a *separate* domain (not the brand domain) so reputation damage is contained. The brand domain handles transactional + reply traffic; the outbound domain handles cold sends. |

## Tools and Sources

### Domain registration + DNS

| Tool | Purpose |
|---|---|
| Cloudflare | DNS API + DDoS protection; preferred for new domains. |
| Namecheap / GoDaddy | Registration + basic DNS API; common existing setups. |
| Google Workspace / Microsoft 365 | DKIM key generation when sending platform is the mailbox provider itself. |

### Sending platform (DKIM key source)

| Platform | DKIM provisioning |
|---|---|
| Smartlead | Generates DKIM key per added domain; user pastes record into DNS. |
| Instantly | Same; explicit setup wizard. |
| Lemlist | Same. |
| Native Gmail Workspace | Google generates DKIM; admin enables in Workspace console. |
| Native M365 | Same on Microsoft side. |

### Authentication audit

| Tool | Purpose |
|---|---|
| MXToolbox | Resolves SPF / DKIM / DMARC records; surfaces alignment issues. |
| EasyDMARC | DMARC report aggregator; reads `rua` reports back over time. |
| Postmark Spam Check | Body content + header sanity (separate from auth). |

### Reputation monitoring

| Tool | Purpose |
|---|---|
| Google Postmaster Tools | IP + domain reputation; spam-rate per Google's view. |
| Microsoft SNDS | IP reputation per Microsoft's view (less granular than Google). |
| TalosIntel (Cisco) | Public IP reputation; secondary check. |

### Source priority rule

For deliverability decisions, in order: **Google Postmaster Tools (last 7 days)** > **Microsoft SNDS (last 7 days)** > **MXToolbox audit results** > **agent inference (`[unverified — needs check]`)**. A "Bad" reputation in Postmaster Tools is the highest-priority pause signal regardless of other indicators.

## Procedure

### 1. Audit existing infrastructure (if any)

If brand domain has prior SPF/DKIM/DMARC, pull current records via MXToolbox API. Surface: SPF includes, DKIM key age + bit length, DMARC policy + reporting alignment. **Rationale**: many "deliverability tanked" cases are mis-configured DMARC or expired DKIM keys, fixable in minutes.

### 2. Choose dedicated outbound domain(s)

For brand `workflowdoc.com`, propose 2–3 variants: `workflowdoc-mail.com`, `getworkflowdoc.com`, `workflowdoc-team.com`. **Rule**: NOT the brand domain itself; close enough to be recognizable; not so close as to look like phishing. For volumes >200/day, plan 2+ outbound domains for rotation. **Rationale**: reputation isolation. A spam complaint storm on the outbound domain leaves the brand domain unaffected.

### 3. Register and configure DNS

For each new outbound domain:
- Register (if needed) via Cloudflare / Namecheap / GoDaddy.
- Publish **SPF**: `v=spf1 include:<sending-platform-spf> -all` (e.g. `include:smtp.smartlead.ai`). 2048-bit minimum if multi-include; watch the 10-lookup limit.
- Publish **DKIM**: 2048-bit key generated by sending platform; record at `<selector>._domainkey.<domain>`.
- Publish **DMARC**: start at `p=none; rua=mailto:dmarc-reports@<brand>.com; ruf=mailto:dmarc-reports@<brand>.com; pct=100; aspf=r; adkim=r`. After 30 days of clean reports, ramp to `p=quarantine`; eventually `p=reject` for high-stakes domains.
- Publish **MX**: route incoming reply traffic correctly (Gmail Workspace / M365 / sending platform's reply handler).
- Publish **rDNS / PTR**: configure on sending IPs (sending platform usually owns this; verify).
- (Optional) Publish **BIMI**: only after DMARC is at `p=quarantine` or stricter; requires VMC certificate.

### 4. Configure RFC 8058 one-click List-Unsubscribe

Configure the sending platform to add both headers on every send:
- `List-Unsubscribe: <mailto:unsubscribe@<outbound-domain>>, <https://<unsub-url>>`
- `List-Unsubscribe-Post: List=Unsubscribe=One-Click`

The HTTPS URL must accept a POST and process the unsubscribe within 2 business days (RFC 8058 says immediate; CAN-SPAM allows 10 days; pick the stricter).

**Rationale**: this is mandatory under Google + Microsoft 2024 bulk-sender rules. Without it, Gmail and Yahoo deliver to spam regardless of authentication.

### 5. Configure CAN-SPAM / GDPR footer requirements

Sending platform footer template MUST include:
- **CAN-SPAM (US)**: physical postal address (must be a legitimate address, not a PO box for some interpretations).
- **GDPR (EU/UK)**: legitimate-interest basis statement + opt-out link + DPO contact (or equivalent).
- **CASL (Canada)**: identification + opt-out + sender contact info.

The `cold-email-sequence` skill draws from this template per recipient jurisdiction.

### 6. Initiate warmup ramp

For each new sender mailbox:
- Day 0: enable platform's warmup feature (Smartlead Warmup, Mailreach, Warmup Inbox). Reciprocal reads / replies / folder-moves with other warmed mailboxes.
- Day 0: 5 sends/day cap (cold sends, if any).
- Day +5: ramp to 10/day if Postmaster Tools shows no negative signal.
- Day +10: ramp to 20/day.
- Day +14: 30/day if reputation is "High" or "Medium" in Postmaster Tools.
- Day +14 to +30: 30/day continued; warmup score should stabilize ≥70.

Exit conditions: warmup_score ≥70 AND domain age ≥14 days AND Postmaster reputation ∉ "Bad" → flip `readiness_flag: true`.

**Rationale**: there is no shortcut. Skip warmup, you blacklist. The 14-day floor is a deliverability industry consensus number.

### 7. Run reputation baseline

After Day +14:
- Pull Google Postmaster Tools reputation: domain + IP. Want "High" or "Medium". "Low" or "Bad" → extend warmup another 7 days.
- Pull Microsoft SNDS: green or yellow expected for new senders; red → extend warmup.
- Pull TalosIntel: should be neutral or positive.
- Pull MXToolbox audit: zero red flags on SPF/DKIM/DMARC.

Log baseline reputation in the infrastructure record so `campaign-management` can detect drift later.

### 8. Emit readiness flag

If all gates pass:
```yaml
readiness_flag: true
warmup_score: <int 0-100>
domain_age_days: <int>
spf_aligned: true
dkim_present: true  
dmarc_policy: none | quarantine | reject
list_unsubscribe_rfc8058: true
google_postmaster_reputation: high | medium | low | bad
microsoft_snds_color: green | yellow | red
ready_for_sends_per_day: <int>
```

If any gate fails, `readiness_flag: false` with `failed_gates: [...]` and recommended remediation per gate.

### 9. Push to CRM + handoff

Per conventions §11: push the infrastructure setup as `interaction:research` with full audit. PATCH no person/company records. Run summary: configured domains, DNS state, warmup state, reputation baseline, readiness flag, recommended next skill (`cold-email-sequence` if green; remediation steps if not).

## Output Template

```yaml
run:
  run_id: <uuid>
  purpose: <user-supplied tag>
  date: <ISO>
  mode: automated | guided | audit-only
  brand_domain: <string>
  outbound_domains: [<string>, ...]
  sending_platform: smartlead | instantly | lemlist | gmail-workspace | m365 | ...

dns_records_per_domain:
  - domain: workflowdoc-mail.com
    spf:
      record: "v=spf1 include:smtp.smartlead.ai -all"
      published: true
      lookup_count: 1
    dkim:
      selector: smartlead
      key_bits: 2048
      key_age_days: 0
      published: true
    dmarc:
      record: "v=DMARC1; p=none; rua=mailto:..."
      policy: none
      published: true
    mx: [<string>, ...]
    rdns: <ip → ptr>

list_unsubscribe:
  rfc8058_configured: true
  unsubscribe_url: https://workflowdoc-mail.com/u
  process_within_days: 1

footer_template:
  jurisdiction_us:
    physical_address: <string>
    canspam_compliant: true
  jurisdiction_eu_uk:
    legitimate_interest_statement: true
    opt_out_link: <url>
    dpo_contact: <string>
  jurisdiction_ca:
    casl_identification: true
    opt_out_link: <url>

warmup:
  start_date: <ISO>
  current_day: <int>
  current_score: <int 0-100>
  current_send_cap: <int>
  ramp_schedule: [<day, cap>, ...]
  exit_eta: <ISO>

reputation_baseline:
  google_postmaster: high | medium | low | bad
  microsoft_snds: green | yellow | red
  talos_intel: positive | neutral | negative
  baseline_date: <ISO>

readiness_flag: true | false
failed_gates: [<string>, ...]   # empty when readiness_flag=true
ready_for_sends_per_day: <int>
recommended_next_skill: cold-email-sequence | <remediation skill>
```

## Worked Example

> *All fictional entities below are tagged `[hypothetical]` — illustrative only.*

**User prompt**: "Set up email infrastructure for our outbound program. Brand domain workflowdoc.com [hypothetical]. We picked Smartlead. Cloudflare for DNS. Target ~80 sends/day."

**Step 1 — Audit existing**: workflowdoc.com [hypothetical] has SPF (`v=spf1 include:_spf.google.com -all`) for inbound, no DKIM for outbound, no DMARC. Surface: brand domain auth incomplete, but we're not sending from brand anyway.

**Step 2 — Choose outbound domain(s)**: Propose `workflowdoc-mail.com` [hypothetical]. Volume target 80/day → 1 sender, 1 domain sufficient. (At 200+/day we'd plan 2 domains for rotation.)

**Step 3 — Register + DNS**:
- Register `workflowdoc-mail.com` [hypothetical] via Cloudflare API (`CLOUDFLARE_API_KEY`).
- Publish SPF: `v=spf1 include:smtp.smartlead.ai -all`.
- Publish DKIM: Smartlead generates 2048-bit key; published at `smartlead._domainkey.workflowdoc-mail.com`.
- Publish DMARC: `v=DMARC1; p=none; rua=mailto:dmarc-reports@workflowdoc.com [hypothetical]; ruf=mailto:dmarc-reports@workflowdoc.com [hypothetical]; pct=100; aspf=r; adkim=r`.
- Publish MX: `10 mx1.smartlead.ai`, `20 mx2.smartlead.ai`.
- rDNS verified on Smartlead's sending IPs.

**Step 4 — One-click List-Unsubscribe**: Smartlead configured to attach `List-Unsubscribe: <mailto:unsubscribe@workflowdoc-mail.com>, <https://workflowdoc-mail.com/u>` and `List-Unsubscribe-Post: List=Unsubscribe=One-Click` headers. Unsub URL processes within 24h.

**Step 5 — Footer**: US recipients (CAN-SPAM): physical address `WorkflowDoc, 100 Market St #200, San Francisco, CA 94105` [hypothetical]. EU/UK template (LIA + opt-out + DPO email) registered for jurisdiction-aware send.

**Step 6 — Warmup**: Day 0 — Smartlead Warmup enabled on `will@workflowdoc-mail.com` [hypothetical]. Reciprocal warmup with Smartlead's mailbox network. Cap 5/day for first 5 days.

**Step 7 — Reputation baseline (Day +14)**:
- Google Postmaster: domain reputation "Medium" [verified: postmaster.google.com], IP reputation "Medium".
- Microsoft SNDS: green [verified: sendersupport.olc.protection.outlook.com].
- TalosIntel: neutral [verified: talosintelligence.com].
- MXToolbox: SPF aligned ✓ DKIM aligned ✓ DMARC published ✓.
- Warmup score: 78 [verified: smartlead-warmup-api].

**Step 8 — Readiness flag**: `readiness_flag: true`. Ready for 30 sends/day.

**Step 9 — Run summary**:
```
WorkflowDoc Email Infrastructure Setup [hypothetical]
Run ID: infra_2026-04-19_w0d
Mode: Automated. Cloudflare + Smartlead.
Outbound domain: workflowdoc-mail.com [hypothetical]
DNS: SPF ✓ DKIM 2048-bit ✓ DMARC p=none ✓ MX ✓ rDNS ✓
List-Unsubscribe (RFC 8058): one-click configured ✓
Footers: US (CAN-SPAM) ✓ EU/UK (GDPR LIA) ✓ CA (CASL) ✓
Warmup: Day +14, score 78, cap 30/day, no negative reputation signal
Reputation: Google Medium / Microsoft green / Talos neutral
Readiness flag: true. Ready for 30 sends/day.
DMARC ramp plan: review reports for 30 days, then move to p=quarantine.
Recommended next: cold-email-sequence (infrastructure ready).
```

## Heuristics

- **Never send cold from the brand domain.** If you do, one complaint storm tanks brand-side reputation forever. Reputation-isolate from day 1.
- **Two domains per 100 sends/day is the safe ratio.** Single-domain at 100+/day risks one bad event taking down the whole program. Rotate.
- **DKIM key rotation matters less than people think.** Once a year is fine; quarterly is overkill outside enterprise.
- **Start DMARC at p=none.** Going straight to p=reject before reading reports breaks transactional and reply-handling email you didn't know existed.
- **Warmup score 70 is the threshold.** Below that, you're sending into spam. Above 80, you're solidly in inbox.
- **The 14-day floor is real.** Some platforms claim "ready in 7 days." They lie. 14 is consensus across multiple deliverability practitioners.
- **Apple MPP doesn't fix bad reputation.** It just makes opens noisy. Reply rate is your only signal.
- **Postmaster Tools "Low" or "Bad" → stop, don't ramp.** Send less, not more, until reputation recovers.
- **Sending IP shared vs dedicated.** Shared IP at low volume (≤30/day) is fine; you live or die by the IP pool's health. Dedicated IP at low volume is overkill and harder to warm.
- **Reply handling matters.** When recipients reply, those replies need to land somewhere monitored. MX setup that drops replies = looks broken to recipients = reputation impact.

## Edge Cases

- **Existing brand domain has DKIM but it's 1024-bit.** Common pre-2017 setup. Force key rotation to 2048-bit; some providers (Yahoo notably) treat 1024-bit DKIM as deprecated.
- **DMARC reports show third-party senders we forgot about** (e.g. Mailchimp marketing emails). Surface; either add to SPF (within 10-lookup limit) or ack as legitimate non-aligned mail (different concern from cold outbound).
- **Sending from Google Workspace native (no separate platform).** Workspace handles DKIM; SPF needs Google's include; DMARC same; warmup is manual (gradual ramp by hand). Cap is conservative — start at 20/day, not 30.
- **Sending from M365 native.** Similar to Workspace. Microsoft's reputation rules slightly stricter.
- **Custom domain at a small registrar with no API.** Guided mode: paste-ready DNS blob; user clicks through their registrar UI. Add 1–2 days for round-trip.
- **DNS propagation taking >24h.** Some TLDs slow; some registrars cache aggressively. Wait; recheck; don't start warmup until records propagate.
- **Postmaster Tools shows "Low" reputation right after warmup.** Possible causes: bounced sends during warmup (list quality issue), spam-trap hit (list quality), warmup mailbox network polluted (rare). Diagnose: check bounce rate during warmup, audit warmup-partner pool.
- **Spam complaint rate >0.3% in week 1.** Pause sends; audit list quality (likely targeting issue, not infra issue); reach out to Postmaster Tools / SNDS for visibility.
- **Migration from Outreach.io to Smartlead.** Existing domain has built reputation; don't lose it — leave existing DKIM key + rotate over 30 days; introduce Smartlead's DKIM as second selector; cut over once Smartlead's selector has 14+ days of clean traffic.
- **Multi-language jurisdictions (DE/FR/JP).** Footer translations needed; LIA / opt-out language varies. Surface; produce templates for each jurisdiction the user sells into.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---|---|---|
| DNS API auth fails (401) | Cloudflare/Namecheap returns 401 | Confirm key; do NOT retry silently; offer guided mode (paste-ready DNS blob). |
| DKIM key generation fails on platform | Smartlead/Instantly internal error | Retry; if persistent, support ticket; produce SPF + DMARC alone and warn. |
| DMARC report alignment failure | reports show many `dkim=fail` / `spf=fail` | Audit SPF (10-lookup limit, missing includes), DKIM (selector mismatch); fix and re-publish. |
| Warmup score stalls at 50–60 | reputation building slowly | Extend warmup 7+ days; check warmup-partner pool quality; pause cold sends. |
| Postmaster Tools shows "Bad" | major reputation event | STOP all sends immediately; audit recent send batches for spam-trap / high-complaint / high-bounce; remediate before resuming. |
| Spam complaint spike during warmup | list-quality issue, not infra | Pause; review list source (likely needs better `data-enrichment` filtering); resume after fix. |
| RFC 8058 header rejected by sending platform | platform doesn't support one-click | Provide unsubscribe URL in body footer (CAN-SPAM compliant) but flag non-compliance with Google 2024 bulk-sender rule for >5,000/day senders. |
| MX records misconfigured | replies bouncing | Verify MX records resolve; check sending platform's reply-handling docs; fix priority order. |
| Outbound domain looks like phishing | flagged by recipients | If too close to brand (e.g. typosquat-adjacent), choose a different variant; sometimes registrar reverts. |
| Multi-domain rotation imbalance | one domain getting all the sends | Verify sending platform's load balancer; force round-robin across pool. |

## Pitfalls

- **Sending from the brand domain.** Brand-domain reputation contamination is unrecoverable.
- **Skipping warmup.** Day-1 cold-blast = blacklist.
- **DMARC straight to p=reject.** Breaks transactional + reply email; surface before strict policy.
- **1024-bit DKIM keys.** Yahoo treats as deprecated; Google deprioritizes.
- **No List-Unsubscribe header.** Auto-spam under Google 2024 rules for >5k/day senders.
- **No physical address (CAN-SPAM US).** Legal violation; cold-email-sequence will block sends.
- **Single domain at high volume.** No reputation isolation; one event = whole program down.
- **Ignoring DMARC reports.** Free signal you're already paying for; drives policy decisions.
- **Treating warmup score as the only signal.** Cross-check with Postmaster Tools and SNDS; warmup score can be gamed by warmup networks.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per conventions §10 and CLAUDE.md, every named entity (domains, IP addresses, reputation scores, dates, audit findings) must carry `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged = contract violation. NEVER invent a Postmaster Tools verdict, a warmup score, or a DKIM key state without the source.
- **Not retesting after changes.** DNS change → wait propagation → re-audit → confirm before flipping flag.

## Verification

The setup is real when: (a) every DNS record resolves correctly via independent lookup (MXToolbox + dig); (b) one-click unsubscribe processes a test request within 24h; (c) physical address renders in actual sent test emails (CAN-SPAM); (d) Postmaster Tools and SNDS both show valid baseline (not "Bad" / red); (e) warmup score climbs deterministically per the ramp schedule (not stalling, not regressing); (f) the readiness flag flips deterministically based on the gate set, not on agent vibes; (g) a test send to a real Gmail and a real Outlook inbox both land in the primary tab (not Promotions, not Spam).

## Done Criteria

1. Mode determined (automated / guided / audit-only); brand domain confirmed; outbound domain(s) chosen.
2. DNS records published per domain: SPF, DKIM (≥2048-bit), DMARC (start p=none), MX, rDNS verified.
3. RFC 8058 one-click List-Unsubscribe configured on sending platform.
4. CAN-SPAM / GDPR / CASL footer templates registered per jurisdiction.
5. Warmup initiated; ramp schedule documented; current day + score tracked.
6. Reputation baseline pulled (Google Postmaster + Microsoft SNDS + TalosIntel + MXToolbox).
7. `readiness_flag: true` only when all gates pass; otherwise `failed_gates` enumerated with remediation.
8. Infrastructure record pushed as `interaction:research`; recommended next skill stated.

## Eval Cases

### Case 1 — fresh outbound program, automated mode

Input: brand domain, Smartlead chosen, Cloudflare API key, target 80/day.

Expected: 1 outbound domain registered + DNS published in <30 min; warmup initiated Day 0; readiness flag flips on Day +14 if Postmaster reputation Medium/High; recommended next: `cold-email-sequence`.

### Case 2 — deliverability recovery (existing program)

Input: existing brand domain, complaint rate spiked to 0.5%, Postmaster Tools shows "Low".

Expected: pause all sends; audit list quality (recent batches' bounce + complaint sources); investigate warmup-partner pool; extended remediation 14+ days; readiness flag stays false until Postmaster recovers to Medium.

### Case 3 — guided mode, no DNS API access

Input: brand domain, Smartlead chosen, no Cloudflare key, user has registrar admin login.

Expected: paste-ready DNS blob (4 records: SPF, DKIM, DMARC, MX); checklist for user to paste into registrar UI; verification step after user reports done; warmup initiated only after records propagate.

### Case 4 — Google 2024 bulk-sender mode (>5k/day)

Input: target 8,000/day to consumer providers.

Expected: mandatory enforcement of all 2024 rules — DMARC required (starting p=none, ramp to quarantine within 60 days), one-click List-Unsubscribe, complaint rate <0.3% gate. 2+ domain rotation. Extended ramp (30+ days). Senior reputation monitoring (Postmaster Tools) cadence increased.

## Guardrails

### Provenance (anti-fabrication)

Per §10 of conventions: domain configurations, reputation scores, warmup states all carry provenance. NEVER invent a Postmaster Tools verdict; pull from API or flag `[unverified — needs check]`. Worked-example fictional entities tagged inline.

### Evidence

Every gate decision is backed by either a tool API call result or a `[user-provided]` confirmation. The `readiness_flag: true` claim has a fully resolvable audit trail.

### Scope

This skill sets up infrastructure. It does NOT write copy (`cold-email-sequence`), monitor active sends (`campaign-management`), or pick recipients (function-2). When infrastructure breaks during sends, this skill's advice runs the diagnose flow.

### Framing

Audit findings + remediation steps in plain operational language. No hype on "we got you to inbox" — just gate-by-gate state.

### Bias

Reputation tools have biases (Google's view ≠ Yahoo's view ≠ Microsoft's view). Use multiple; surface disagreements rather than collapse to one number.

### Ethics

Compliance baseline (§9 of conventions) is non-negotiable: physical address, opt-out, jurisdiction-aware footer.

### Freshness

Reputation is a moving target; baseline gets stale in 30 days. `campaign-management` re-pulls reputation continuously; this skill emits the baseline that gets compared against later.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Infrastructure ready (flag=true) | `cold-email-sequence` | readiness flag, warmup score, send cap, sender pool |
| Infrastructure broken mid-program | back to this skill (audit-only mode) | current state, recent metrics |
| Multi-channel cadence with email leg | `multi-channel-cadence` | readiness flag, sender pool |
| Active campaign monitoring | `campaign-management` | sender pool, baseline reputation |
| Spam complaint spike | back to this skill (recovery mode) + audit upstream `data-enrichment` | metrics, list source review |
| Migrating sending platform | back to this skill (migration mode) | existing DKIM keys, existing reputation |

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
    "relevance": "Email infrastructure setup infra_2026-04-19_w0d. Brand: workflowdoc.com. Outbound: workflowdoc-mail.com (Smartlead). DNS: SPF ✓ DKIM 2048 ✓ DMARC p=none ✓ MX ✓ rDNS ✓. List-Unsubscribe RFC 8058 ✓. Footer: CAN-SPAM US + GDPR EU/UK + CASL CA. Warmup Day +14, score 78. Postmaster Medium / SNDS green / Talos neutral. Readiness flag: TRUE. Ready 30/day. DMARC ramp to quarantine in 30d.",
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

- Audit-only mode produced no changes — push the audit findings as `interaction:research` with `#audit-only` tag; no infrastructure setup record (nothing was changed).
- Setup attempted but DNS API failed — push `interaction:research` with `#setup-failed` and detailed error; readiness stays false.
- `[hypothetical]` — never.
