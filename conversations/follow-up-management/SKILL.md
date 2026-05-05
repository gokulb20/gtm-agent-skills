---
name: follow-up-management
description: Schedule resume touches, nurture cadences, and no-show rescue flows for not-now, out-of-office, and warm-but-not-now recipients. Use when the user says "schedule follow-up", "parse resume date", "no-show rescue", or "nurture this lead."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Conversations, Follow-Up, Nurture, Scheduling]
    related_skills: [reply-classification, objection-handling-library, pipeline-stages, lead-scoring]
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

# Follow-Up Management

Schedule the right follow-up at the right time for not-now recipients, OOO auto-replies, nurture-parked leads, and meeting no-shows. Owns date parsing from reply text, the 30/60/90-day nurture library, and the no-show rescue flow.

## When to Use

- Not-now reply with stated resume date — schedule the resume
- OOO auto-reply with return date — pause + resume
- Meeting no-show — rescue flow within 24h
- Tier-1/2 recipient parked in nurture — schedule next touch
- Bulk schedule resume touches for not-now replies
- User says "schedule follow-up" or "parse resume date"

## Quick Reference

| Concept | Value |
|---|---|
| Resume-date sources | Explicit date → parse; implied window → resolve; no date → default 60d |
| Nurture cadences | 30-60-90-light (3 touches) / 90-180-365-deep (3 touches) / no-show-rescue (24h + 7d) |
| Date parsing | Natural language → ISO. "Q1 2027" → 2027-01-15. "After holidays" → Jan 5. Provenance: explicit = [verified]; inferred = [unverified] |
| Resume channel | Same as original reply unless redirect detected |
| No-show rescue window | Within 24h of missed meeting; tone: low-stakes, single CTA |
| Capacity-cap respect | Resume + nurture touches count against per-channel caps |

## Procedure

1. **Validate inputs.** Read trigger event + lead record + cadence/reply history. Confirm trigger type (not-now / OOO / nurture / no-show).
2. **Parse resume date.** Extract date/window from reply text. Pattern-match phrases. Default per matrix when ambiguous. Tag provenance. See `${HERMES_SKILL_DIR}/references/date-parsing.md`.
3. **Pick follow-up flow.** not-now with date → single resume. not-now without → 60d. OOO → resume after return+1. nurture → 30-60-90-light. no-show → rescue. See `${HERMES_SKILL_DIR}/references/nurture-cadences.md`.
4. **Generate touches.** Hand off to channel skill (cold-email-sequence / linkedin-outreach) with cadence position context. Channel skill produces copy.
5. **Schedule + capacity check.** Compute new touches against per-channel weekly caps. Over capacity → surface for user. Schedule via channel skill API.
6. **Update lead record.** PATCH person: `next_followup_at`, `nurture_state`, `cadence_state`.
7. **Push to CRM + emit run summary.** Per-recipient `interaction:research` with schedule + provenance. Run summary: triggers processed, flow distribution. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Forgetting the parsed date — ALWAYS PATCH person record with next_followup_at
- Default 60d when reply named a specific date — honor stated date
- No-show rescue at 7 days instead of 24 hours — window matters
- Nurture touches that pitch — nurture is value-first; pitches trigger unsubscribes
- Re-engaging on not-interested — hard no = exit-permanent; follow-up does NOT re-engage
- Holiday-window resume — "Q1 2027" arriving Dec 24 → schedule Jan 5, not Dec 25

## Verification

1. Every trigger has a scheduled resume OR documented archive decision
2. Resume dates trace to reply text or documented default
3. Channel-skill handoffs succeeded with cadence position context
4. Person records patched with next_followup_at + nurture_state + cadence_state
5. Capacity checks passed at schedule time
