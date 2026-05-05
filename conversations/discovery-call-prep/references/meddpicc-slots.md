# MEDDPICC 8-Slot Framework

## The 8 Slots

| Slot | What it captures | Typical source | Default if unknown |
|---|---|---|---|
| **Metrics** | Quantified pain / expected outcome | ICP P-T-O + reply figures | `unknown — ask` |
| **Economic Buyer** | Who has budget authority | Role map from data-enrichment | `unknown — ask` |
| **Decision Criteria** | What they evaluate solutions on | Positioning house | `unknown — ask` |
| **Decision Process** | Steps from interest to signed contract | Discovery call extraction | `unknown — ask` |
| **Paper Process** | Procurement / legal / security / contract steps | Discovery call extraction | `unknown — ask` (security review likely if enterprise) |
| **Identify Pain** | Core problem in buyer language | ICP P-T-O + reply text | `unknown — ask` |
| **Champion** | Internal advocate who sells for you | Role map + reply signals | `unknown — ask` |
| **Competition** | Known/likely alternatives | Tech-stack signals + competitive-intel | `unknown — ask` |

## Slot Completion Rules

- Each slot must be populated from existing intel OR labeled `unknown — ask`
- `unknown — ask` is a valid populated value — it routes to a discovery question
- Never invent slot content. Provenance per slot.
- For Discovery → Proposal stage advance: ≥5 of 8 slots populated (pipeline-stages gate)
- For Proposal → Closed-Won: ≥6 confirmed, including Paper Process

## Discovery Question Mapping

`unknown` slots directly generate the discovery questions:
- Decision Criteria unknown → "What does your team evaluate when choosing a solution like this?"
- Decision Process unknown → "Walk me through how a decision like this typically gets made at your company."
- Paper Process unknown → "What does the vendor onboarding process look like internally?"
