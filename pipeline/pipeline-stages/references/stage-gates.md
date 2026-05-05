# Stage Gate Definitions — Pipeline Stages

## 8-Stage Pipeline with Explicit Gates

| From | To | Trigger event | Required fields at target |
|---|---|---|---|
| New | Contacted | ≥1 Touch sent (function-3) | parent_touch_id |
| Contacted | Engaged | Reply received (not unsubscribe/not-interested) | reply_id, last_reply_class |
| Engaged | Meeting | Discovery call scheduled with confirmed time | meeting_id, meeting_at, meeting_channel |
| Meeting | Discovery | Meeting completed | meeting_outcome, ≥5/8 MEDDPICC populated |
| Discovery | Proposal | All 8 MEDDPICC slots populated (inferred acceptable) | deal_value, proposal_sent_at |
| Proposal | Closed-Won | Contract signed; revenue booked | contract_signed_at, closed_won_revenue |
| Proposal | Closed-Lost | Explicit no OR 90d silence | lost_reason, lost_competitor (if applicable) |
| Any | Closed-Lost | User-driven with reason | lost_reason (required) |

## MEDDPICC Thresholds

- **Discovery → Proposal:** All 8 slots populated (inferred acceptable, not all confirmed)
- **Proposal → Closed-Won:** ≥6 confirmed slots, including Paper Process
- **Engaged → Meeting:** Meeting scheduled with confirmed time (not just "interested")

## Reverse Transitions

Allowed but MUST be logged with explicit reason:
- Discovery → Engaged (stalled discovery)
- Meeting → Engaged (meeting cancelled/no-show)

## Closed-Lost Reason Taxonomy

| Reason | Code | Feeds downstream |
|---|---|---|
| No budget | no-budget | revenue-forecasting, icp-refinement-loop |
| No authority | no-authority | handoff-protocol, lead-scoring |
| No need | no-need | icp-refinement-loop |
| Bad timing | no-timing | follow-up-management |
| Lost to competitor | lost-to-competitor | competitive-intelligence, icp-refinement-loop |
| Unresponsive | unresponsive | crm-hygiene (stale data check) |
