---
name: multi-channel-cadence
description: Compose 5–9 touches across email+LinkedIn+cold call into a 14–21 day cadence — calling channel skills for copy/scripts, then orchestrating per-recipient sequencing with channel-isolation rules, capacity-cap respect, branch logic, and exit conditions. Use when Tier-1 needs more than email alone, channels are complementary, reply rate on single-channel has plateaued, or account-based plays require multi-thread coverage.
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Outreach, Cadence, MultiChannel, Orchestration]
    related_skills: [cold-email-sequence, linkedin-outreach, cold-calling, campaign-management, email-infrastructure-setup]
    requires_tools: [terminal]
    config:
      - key: gtm.crm_url
        description: agentic-app CRM endpoint
        default: "http://localhost:4210"
      - key: gtm.crm_adapter
        description: "Which CRM adapter (agentic-app | csv | none)"
        default: "agentic-app"
required_environment_variables:
  - name: AGENTIC_APP_TOKEN
    prompt: "agentic-app bearer token"
    required_for: "Pushing records to CRM"
---

# Multi-Channel Cadence

Compose a 5–9 touch cadence across email+LinkedIn+cold call channels, calling each channel skill for copy/scripts and orchestrating per-recipient sequencing. Owns cross-channel rules: channel-isolation, per-day spacing, capacity aggregation, branch logic on replies, exit conditions.

## When to Use

- Tier-1 cadence needs more than email alone
- Email reply rate plateaued — add LinkedIn and call legs
- Account-based campaign — 3 contacts per company across channels
- Want a reusable cadence template
- Single-channel reply rate isn't enough; channel diversity reduces signal dependency

## Quick Reference

| Concept | Value |
|---|---|
| Default template | `email-li-call-7touch-21d` (E+LI-connect+E+Call+E+LI-msg+E-breakup) |
| Template library | email-only / email+LI / email+LI+call / tier-1-9touch / abm-3thread / gdpr-light |
| Channel-isolation rule | Don't reference one channel's content in another's body |
| Per-day spacing | Max 1 touch per recipient per day; exception: email+LI-connect on D+0 |
| Capacity aggregation | Per-channel caps: email 30/day/mailbox, LI 80/week, call 80/rep/day |
| Multi-channel reply target | ≥6% by D+10 (vs ~3% email-only) |
| Branch rules | li-connect-accepted → swap next email to LI-message; email-bounce → drop email |
| Exit conditions | reply-positive, reply-negative, bounce, unsubscribed, manual-stop, cap-hit |
| Re-touch rule | No record touched in any channel within 90 days |
| GDPR | Auto-swap to `gdpr-light-4touch-21d` template |

## Procedure

1. **Validate prerequisites** — Read scored Leads; check channel skills' ready flags (email infrastructure, LI account safety + URL coverage, phone + DNC); load ICP P-T-O + message house. Block only if zero channels ready.
2. **Determine mode (per channel)** — Each channel inherits its own mode (API/manual/BYO). Cadence record carries per-channel mode metadata.
3. **Pick or compose cadence template** — User-supplied OR default `email-li-call-7touch-21d`. See `${HERMES_SKILL_DIR}/references/cadence-templates.md`. Adapt per recipient if channel unavailable (no LI URL → swap LI touch for email).
4. **Filter recipient list (cross-channel)** — Drop records failing every channel's gate; apply tier filter; apply re-touch rules (90d any-channel cooldown); auto-swap to `gdpr-light` for EU/UK.
5. **Pre-flight: cross-channel capacity check** — Compute per-channel touches needed vs caps × pool × duration. Surface to user if any channel over-capacity. Reference `${HERMES_SKILL_DIR}/references/capacity-planning.md`.
6. **Dispatch to channel skills** — For each touch position, call channel skill's `prepare()` with lead + position + sender + branch context. Each returns Touch[draft] with own provenance. Unverified hooks propagate as blocked per conventions §10.3.
7. **Validate cross-channel rules** — Per-day spacing; channel-isolation (no body cross-references); quiet hours per channel; capacity distribution. Failures → fix or surface.
8. **Build Cadence + Campaign records** — Per conventions §2.2/§2.3. Branch rules (li-connect-accepted, email-bounce) and exit conditions explicit.
9. **Push to CRM + run summary** — Run `${HERMES_SKILL_DIR}/scripts/push_to_crm.py` for cadence + campaign records. Per-touch records pushed by channel skills. Recommend `campaign-management`.

## Pitfalls

- **Same-day double-touches** — email + call same day = harassment
- **Channel-isolation broken** — "As I LinkedIn-messaged you" feels invasive
- **Linear cadence without branch logic** — doesn't beat single-channel
- **Cadence too long (9+)** — nuisance; reply rate drops past T7
- **Cadence too short (<5)** — leaves conversion on table
- **No exit conditions** — book meetings into already-replied threads
- **Account-based without coordination** — 3 reps calling same account same week

## Verification

1. Every touch dispatched to correct channel skill with full context; cross-channel capacity caps respected at every per-day window
2. Channel-isolation rule passes (no body cross-references); per-day spacing rule passes; branch rules trigger correctly
3. Exit conditions fire on first-trigger; re-running same input produces same cadence shape (deterministic)
