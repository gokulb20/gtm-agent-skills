---
name: icp-definition
description: Define a tiered Ideal Customer Profile using a 100-point weighted scorecard, Buyer/Champion/User/Blocker role mapping, Pain-Trigger-Outcome chains, an anti-ICP boundary, and a trigger event library. Produces an ICP one-pager an SDR can apply in 2 minutes. Use when the user mentions ICP creation/refinement, qualification rules, sales-marketing alignment on target customer, or pre-outbound ICP grounding.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, icp, ideal-customer-profile, segmentation, qualification, function-1]
related_skills:
  - market-research
  - competitor-analysis
  - positioning-strategy
  - channel-strategy
  - competitive-intelligence
inputs_required:
  - product-description
  - beachhead-segment-from-market-research
  - geography
  - pricing-and-acv-range
  - sales-motion-plg-or-sales-led-or-hybrid
deliverables:
  - icp-one-pager
  - 100-point-qualification-scorecard
  - buyer-champion-user-blocker-role-map
  - pain-trigger-outcome-chain
  - tier-1-2-3-named-account-examples
  - anti-icp-boundary-definition
  - trigger-event-library
  - sdr-qualification-handoff-doc
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# ICP Definition

Produce a tiered, scored, evidence-backed Ideal Customer Profile that drives every downstream GTM decision. The output is a scoring rubric, a role map, a pain chain, and an anti-ICP boundary — written tightly enough that a new SDR or AI agent can apply it on day one without judgment calls.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Most "ICPs" are aspirational marketing language that doesn't survive contact with real lead lists. This skill produces the ICP that survives: tiered (1/2/3 + Anti-ICP), reverse-engineered from won deals where possible, scored on a 100-point rubric, and shipped with a 2-minute SDR qualification handoff doc.

## When to Use

- "Define our ICP" / "Who should we target?"
- "Tighten our ICP based on what's actually working"
- "What makes a lead qualified?" / "When should an SDR disqualify?"
- Sales/marketing alignment on target customer
- Pre-outbound grounding before lead sourcing
- "Who should we say no to?" (anti-ICP definition)
- Persona work — buyer + champion + user + blocker mapping

## Inputs Required

1. **Product description** — what it does, for whom, the outcome.
2. **Beachhead segment** — from `market-research` if run, or buyer hypothesis.
3. **Geography**.
4. **Pricing model + ACV range**.
5. **Sales motion** — PLG / sales-led / hybrid.
6. **Last 10 won deals** (optional, **highest-value**) — companies + roles you sold to. With this we extract real ICP; without it we're guessing.
7. **Last 5 lost deals** (optional, very high-value).
8. **Anti-customers** (optional) — who you regret selling to.

## Quick Reference

| Concept | Value |
|---|---|
| **Scorecard weights** | Pain 25 / Trigger 20 / WTP 20 / Reach 15 / TTV 10 / Strategic 10 = 100 |
| **Tier cutoffs** | Tier 1 ≥75, Tier 2 55–74, Tier 3 40–54, Anti-ICP <40 |
| **Firmographic target** | 500–5,000 candidate accounts (wider = unfocused; narrower = unscalable) |
| **Roles required** | Buyer (Economic) / Champion / User (End) / Blocker — fill all four |
| **Pain-Trigger-Outcome** | chronic problem → current workaround + cost → acute event in last 90d → measurable success state |
| **Workaround analysis** | What they do today / Cost (time, money, risk, accuracy, reputation) / Dream state in 90 days |
| **Trigger types** | Funding / Hiring / Leadership / Tech / Public commitment / Competitor adoption / Compliance / Growth / Pain signals / Buying-window (budget refresh, audit cycle, quarter-end, migration, post-fundraise) |
| **Trigger axes** | `Type: need` (pain becomes acute) vs. `Type: buy` (budget/process opens). Both axes scored. |
| **Anti-ICP lenses** | Firmographic / Pain (too small) / Buyer (wrong role) / Trigger (none → nurture only) |
| **SDR qualify time** | 2 minutes using the handoff doc |
| **Confidence rubric** | High: ≥30 deals OR ≥30 buyer interviews · Medium: 10–29 · Low: 1–9 · Hypothesis-only: 0 |

## Procedure

### 1. Anchor in evidence
Pull last 10–20 won deals if they exist. Capture per deal: company, size, stage, geography, tech stack, decision-maker role, champion role, pain in their words, trigger, time-to-close, ACV, reference willingness. If 0 customers → mark "hypothesis-only", skip to step 2 with confidence cap Low.

### 2. Define the buyer firmographic
Industry (specific, not "B2B SaaS"), employee/revenue size, stage, geography, tech-stack signals, operating model. Test: produces 500–5,000 candidate accounts. Outside range → re-scope.

### 3. Fill the four roles
Buyer / Champion / User / Blocker. Each gets: title patterns, seniority, what they care about, what kills the deal, where to find them. **Don't skip Blocker** — it's the #1 reason mid-market+ deals stall.

### 4. Build the Pain-Trigger-Outcome chain
In buyer language. Every Pain claim maps to a real customer quote (or is flagged hypothesis). Include a **Workaround Analysis**: what they do today, the cost (time / money / risk / accuracy / reputation), and the 90-day dream state. The workaround is itself a competitive alternative — it feeds positioning + competitor-analysis downstream.

### 5. Build the trigger library
5–10 specific triggers, each tagged Strength + `Type: need` or `buy` + named detection source (Crunchbase / LinkedIn / BuiltWith / etc.). Include at least one buying-window trigger (budget refresh, audit cycle, quarter-end, migration moment, post-fundraise). No "we'll know it when we see it."

### 6. Run the 100-point scorecard
Apply to ≥9 accounts (3 best-fit, 3 mid, 3 anti-ICP). If scores cluster (no separation), the rubric weights are wrong — re-tune.

### 7. Define Anti-ICP
4 boundaries (firmographic / pain / buyer / trigger), each with rule + rationale. Anti-ICP cannot be empty.

### 8. Generate Tier 1/2/3 examples
3 named accounts per tier with score breakdown. Real if available; otherwise "hypothetical" tag.

### 9. Produce the ICP one-pager + SDR handoff
Single document, 2-minute usable. Includes: firmographic, roles, P-T-O, trigger library, scorecard rubric, anti-ICP, Tier examples, qualification handoff (Tier 1 signals / Tier 2 signals / hard disqualifiers / 3 discovery questions).

## Output Format

- ICP one-pager (sections 1–9 above)
- 100-point qualification scorecard (rubric + per-dimension weights)
- 4-role map (Buyer / Champion / User / Blocker cards)
- Pain-Trigger-Outcome chain
- Trigger event library table (5–10 entries with Strength + Source)
- Anti-ICP boundary table (4 lenses)
- Tier 1 / 2 / 3 / Anti-ICP named account examples with score breakdown
- 2-minute SDR qualification handoff
- Recommended next skill + carry-forward inputs

## Done Criteria

1. Firmographic produces 500–5,000 candidate accounts.
2. All four roles filled (Buyer / Champion / User / Blocker).
3. Pain-Trigger-Outcome in buyer language; quotes mapped or flagged hypothesis. Workaround Analysis populated (current workaround / cost / dream state).
4. Trigger library has 5–10 entries with named detection sources, each tagged `Type: need` or `buy`. At least one buying-window trigger.
5. 100-pt scorecard applied to ≥9 accounts; tiers separate cleanly.
6. Anti-ICP has 4 boundaries (firmographic / pain / buyer / trigger).
7. Tier examples named with score breakdown.
8. SDR qualification handoff fits on 1 page.
9. Validated against ≥10 buyer conversations (or won deals) — otherwise output stamped as hypothesis-only.

## Pitfalls

- **Aspirational ICP.** Describing the customer you wish you had vs. the one you actually win. Won deals override the user's stated ICP.
- **One-role ICP.** Naming only the buyer. In B2B, no champion = stalled deal. No blocker thinking = procurement kills you in week 6.
- **Pain without trigger.** Buyer hurts but isn't acting. Pain alone doesn't fund a deal.
- **Skipping Anti-ICP.** Sales spends capacity chasing fit-but-misqualified accounts.
- **Generic firmographic.** "B2B SaaS" is not a firmographic. "Series B SaaS, 100–300 emp, US, Zendesk + 5+ support staff" is.
- **Static ICP.** Re-run every 6 months minimum, faster if motion changes.
- **Sample size of 1.** One big customer is an outlier until proven. Don't ICP from a single deal.
- **Logo lust.** "We want [BigCo] as a customer" is not ICP work — it's wishful thinking.
- **Don't ICP what you can't reach.** Reachability is in the score for a reason. Perfect-fit but unreachable = Tier 3 at best.
- **Vague triggers.** "We're triggered when they need us" is useless. Force concrete, datable, observable events.
- **Fabricating named entities (anti-fabrication / provenance rule).** Every named entity in output (companies, people, quotes, dates, dollar figures, customer counts, named tools) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. Without a live research tool at runtime, default to `[unverified — needs check]` — never invent specifics like "Acme Corp Series B 60d ago" to fill the trigger library or Tier examples.

## Verification

The ICP is real when an SDR can qualify a lead in 2 minutes using the handoff doc, marketing can write outbound sequences using the Pain-Trigger-Outcome statements directly, the Anti-ICP boundaries are specific enough that 3 disqualifiers can be stated without thinking, and the 100-pt scorecard differentiates won from lost deals when applied retroactively. If any of these is "no," re-run the relevant step.

## Example

**User prompt:** "Define our ICP. We're a $4k-ACV AI tool for SaaS support teams; 4 paid pilots so far."
**What should happen:** Pull pilot data (Plant, Stitchbox, Paymet, Dovere). Build firmographic from the pattern (Series B SaaS, 100–300 emp, support team 5–15, US). Fill all four roles — Buyer = VP/Director of Support, Champion = Support Ops Manager, User = Tier 1/2 specialist, Blocker = IT Security/Procurement. Write Pain-Trigger-Outcome anchored in pilot call quotes. Trigger library: 8 triggers including "Series B funding <90 days," "VP of Support hire," "outsourced support added." Score the 4 wins (should land 80+). Anti-ICP: companies <50 emp, fully outsourced support, IT-led buying, >500 emp + entrenched contract. Confidence: Medium (4 wins is small but consistent).

**User prompt:** "We have 0 customers. Build a hypothesis ICP."
**What should happen:** Skill marks all output "hypothesis-only," confidence cap Low, recommends 8–10 buyer interviews before claiming higher confidence. Triggers built conservatively. Trigger library smaller but specific. Plan to re-run after first 10 closed deals.

**User prompt:** "Tighten our ICP — we're winning some, losing some, can't tell why."
**What should happen:** Pull last 10–20 won + 5–10 lost deals. Apply 100-pt scorecard retroactively. Look for separation — wins should score >60, losses <55. If they don't, the rubric weights are wrong (re-tune). Anti-ICP gets sharpened from the loss patterns. Output: tightened ICP + the specific anti-ICP rules that would have prevented the recent losses.

## Linked Skills

- Sharpen positioning against this ICP → `positioning-strategy`
- Source leads matching the firmographic + triggers → `lead-sourcing-apollo` (planned)
- Score individual leads against the 100-pt rubric → `lead-scoring` (planned)
- Pick channels that reach the buyer / champion → `channel-strategy`
- Refresh ICP from new conversion data after 30+ deals → `icp-refinement-loop` (planned)
- Map competitors that own current ICP segments → `competitor-analysis`

## Push to CRM

After producing the ICP one-pager and tier examples, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Tier 1 example accounts | `company` | `score: 5, priority: hot, tags: "#icp-tier-1 #beachhead"` |
| Tier 2 example accounts | `company` | `score: 3, priority: warm, tags: "#icp-tier-2"` |
| Tier 3 example accounts | `company` | `score: 2, priority: cold, tags: "#icp-tier-3"` |
| Anti-ICP examples | `company` | `score: 1, priority: cold, tags: "#anti-icp"` |
| Full ICP one-pager | `interaction` (type: `research`) | `relevance` = full ICP doc; tags `#icp-definition` |
| Buyer/Champion/User/Blocker role cards | `interaction` (type: `note`) | One per role; tags `#icp-role:buyer` etc. |

If a tier example has a known decision-maker name + LinkedIn, push as a `person` (use `contactName`/`contactLinkedIn` — push API auto-creates the link to the company).

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:icp-definition:v2.0.0"`

### Example push (Tier 1 account + champion contact)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "website": "https://stitchbox.com",
    "industry": "SaaS",
    "score": 5,
    "priority": "hot",
    "tags": "#icp-tier-1 #beachhead",
    "contactTitle": "Support Operations Manager",
    "relevance": "Tier 1 ICP — 87/100. Series B SaaS, 100–300 emp, support team 5–15, growing 30%+ YoY. Pain: tribal knowledge across 8 sources; trigger: outsourced support added 60d ago; champion: Support Ops Manager. See ICP v2.0.0.",
    "source": "skill:icp-definition:v2.0.0"
  }'
```

### Example push (Anti-ICP entry)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "[2,000-emp enterprise w/ entrenched Guru contract]",
    "score": 1,
    "priority": "cold",
    "tags": "#anti-icp #firmographic-out-of-bounds",
    "relevance": "Anti-ICP per ICP v2.0.0: >500 emp + entrenched Guru/Stonly contract. Sales cycle 6mo+, reachability 5/15. Nurture only on contract-renewal trigger.",
    "source": "skill:icp-definition:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above (real `company` / `person` / `interaction` records, normal priority/score) |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #icp-definition`. Never as `company` / `person`. Held for human review; the dashboard review-queue filter is a follow-up agentic-app task. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example unverified push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #icp-definition",
    "relevance": "Tier 1 candidate Acme Corp [unverified — needs check] — no source for firmographic; needs research before activation.",
    "source": "skill:icp-definition:v2.0.0"
  }'
```

### When NOT to push

- ICP marked "hypothesis-only" (0 customers) — push the research interaction but skip Tier company examples; they're speculative.
- Confidence: Low — tag research interaction `#icp-low-confidence` so downstream skills downweight.
