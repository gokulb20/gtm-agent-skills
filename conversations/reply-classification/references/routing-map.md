# Routing Map — Reply Classification

## Label → Downstream Skill Dispatch

| From | To | Trigger | Inputs carried forward |
|---|---|---|---|
| reply-classification | discovery-call-prep | label=positive AND meeting requested | reply_id, parent_touch_id, lead_id, proposed meeting time |
| reply-classification | objection-handling-library | label ∈ {not-now, not-interested, question} AND embedded_objection != null | reply_id, embedded_objection, parent_cadence_id, lead_id |
| reply-classification | follow-up-management | label ∈ {not-now, out-of-office} (always) | reply_id, parsed_resume_date (if any), lead_id, channel |
| reply-classification | data-enrichment | label ∈ {wrong-person, referral} | reply_id, named referral (if any), original lead_id |
| reply-classification | manual-review queue | confidence < 0.75 OR label=unclear | full reply + LLM best guess + rationale |

## Parallel Dispatch

When two routes fire (e.g., not-now with embedded objection AND stated date), all routes fire in parallel. follow-up-management schedules the resume; objection-handling-library produces response variants. They do not block each other.

## Cross-function Routing

| Signal | Route to function | Purpose |
|---|---|---|
| Competitor mention in reply | competitive-intelligence (function-1) | Signal feed |
| Pricing pushback | revenue-forecasting (function-5) | ACV reality-check |
| positive label | pipeline-stages (function-5) | Stage advance trigger |
| not-interested loss reason | customer-feedback-analysis (function-6) | Win/loss data |
