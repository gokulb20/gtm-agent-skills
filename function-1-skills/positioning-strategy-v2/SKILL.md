---
name: positioning-strategy
description: Define product positioning using Dunford's 5-component framework, JTBD-based wedge construction, message house architecture, value-by-role variations, and a for-and-against wedge against named competitors. Produces a positioning canvas + message house + wedge — evidence-backed and sales-usable. Use when the user mentions positioning, repositioning, message hierarchy, value-prop articulation, or competitive wedge sharpening.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, positioning, messaging, value-proposition, dunford, function-1]
related_skills:
  - market-research
  - competitor-analysis
  - icp-definition
  - channel-strategy
  - competitive-intelligence
inputs_required:
  - product-description
  - icp-from-icp-definition
  - competitive-landscape-from-competitor-analysis
  - pricing-model-and-acv-range
deliverables:
  - positioning-canvas-dunford-5-component
  - alternatives-analysis-including-status-quo
  - unique-value-attributes-table
  - best-fit-icp-statement-for-positioning
  - market-category-claim
  - wedge-statement-with-3-test-diagnostic
  - message-house-pillar-architecture
  - value-props-by-role-buyer-champion-user
  - for-and-against-wedge-per-top-3-competitor
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Positioning Strategy

Define what your product is, who it's for, what it's better at, and against what alternatives — evidence-backed and clear enough that a buyer understands the wedge in 10 seconds. Output: positioning canvas + message house + wedge + role-specific value props + for-and-against vs. each top competitor.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Most positioning lives in someone's head, drifts every quarter, and produces inconsistent outbound copy. This skill operationalizes April Dunford's framework with explicit alternatives analysis, value attributes, and a wedge sharp enough to flip a buyer's default choice. The deliverable is not a tagline — it's the underlying logic that makes every downstream message coherent.

## When to Use

- Positioning definition for a new product or new launch
- "Our positioning isn't working — fix it" (repositioning)
- "What do we lead with vs. supporting messages?" (message hierarchy)
- "Help me write our value prop"
- "How do we position against [competitor]?" (competitive wedge sharpening)
- Sales messaging audit / consolidation
- Pre-launch positioning grounding (after `market-research` + `competitor-analysis` + `icp-definition`)

## Inputs Required

1. **Product description** — what it does, in 2 sentences.
2. **ICP** — from `icp-definition`. Push back if missing.
3. **Top 3 competitors / alternatives** — including status quo / DIY. Push back if competitive landscape is missing.
4. **Pricing model + ACV range**.
5. **Best-fit customer quotes** (optional, **highest-value**) — quotes from customers who *rave, refer, and would be a reference*, not just any won deals. 5+ unlock real buyer language. If you can't name 3+ customers who'd actively refer / be a reference, flag confidence cap as Medium.
6. **Lost-deal customer quotes** (optional, very high-value) — what they said when they didn't buy.
7. **Workaround Analysis from `icp-definition`** (optional but high-leverage) — current workaround + cost feeds directly into Alternatives Analysis.
8. **Existing positioning materials** (optional) — homepage hero, sales deck slide 1.

## Quick Reference

| Concept | Detail |
|---|---|
| **Dunford 5 components** | Competitive alternatives / Unique attributes / Value (and proof) / Best-fit ICP / Market category |
| **Category frame types** | Existing / Subcategory (default) / New (high-risk) / Cross-category (avoid) |
| **Wedge format** | "For [ICP] who are doing [JTBD], [product] is [category] that [unique value], unlike [alternative] which [trade-off]" — Geoffrey Moore's positioning template + Dunford alternatives |
| **Wedge diagnostic** | Specific (no competitor could paste it) / Defensible (provable with evidence) / Sharp (flips a default choice) |
| **Alternatives floor** | ≥4 entries including status quo / DIY |
| **Message house** | 1 primary + 3 pillars + ≥2 proofs/pillar |
| **Roles for value variation** | Buyer (Economic) / Champion / User (End). Blocker gets information, not positioning. |
| **Buyer-language audit** | Every load-bearing word in ≥3 buyer-source quotes, OR flagged "internal language — needs validation" |
| **Re-position trigger** | ICP shift / major competitor move / win-rate drop / 6 months minimum |

## Procedure

### 1. Identify alternatives (Dunford component 1)
Direct competitors + indirect / adjacent + DIY / status quo. **≥4 alternatives.** Status quo is the most common alternative for early-stage products.

### 2. List unique attributes (Dunford component 2)
Features ONLY you have, or have meaningfully more of. Each: specific (not "advanced AI") / verifiable (a buyer could fact-check) / differentiating (no alternative has it).

### 3. Map attributes to value (Dunford component 3)
Drill: feature → benefit → outcome → proof. If the "why buyer cares" still sounds like a feature, drill again. Every value claim has proof (case study / data / customer quote / demoable feature).

### 4. Choose best-fit ICP (Dunford component 4)
Often *narrower* than the operational ICP. The segment that values the unique attributes most.

### 5. Choose market category (Dunford component 5)
**Default to subcategory.** Test: 5-second test (does buyer recognize?), search test (Google volume?), G2/analyst recognition. New-category claims need 10–18 months + budget; require explicit justification.

### 6. Construct the wedge
Use the JTBD wedge format. Apply the 3 diagnostic tests (specific / defensible / sharp). Iterate until all three pass.

### 7. Build the message house
Primary (1 sentence — wedge in plain language) + 3 pillars (each maps to a top buyer value) + ≥2 proofs per pillar.

### 8. Generate value-by-role variations
Buyer / Champion / User — each gets headline + body + proof. Distinct framing, not minor word swaps. Blocker gets info in trust pages, not positioning.

### 9. For-and-against wedges (top 3 competitors)
Per competitor: WHEN buyer is X / WE WIN BECAUSE / THEY ATTACK / WE COUNTER / FLIP QUESTION. Connect positioning to sales reality.

### 10. Buyer-language audit
Every load-bearing word verified in ≥3 buyer-source quotes (won-deal calls / G2 / community), or flagged for testing.

## Output Format

- Positioning canvas (Dunford 5-component)
- Alternatives analysis (≥4 including status quo)
- Unique attributes + Attribute-Value-Outcome-Proof tables
- Best-fit ICP statement
- Market category claim with test results
- Wedge statement + 3-test diagnostic
- Message house (primary + 3 pillars + proofs)
- Value props by role (Buyer / Champion / User)
- For-and-against wedges (top 3 competitors)
- Buyer-language audit table
- Recommended next skill + carry-forward

## Done Criteria

1. Wedge passes all 3 diagnostic tests (specific / defensible / sharp).
2. Every load-bearing word verified in buyer-source quote OR flagged for testing.
3. Best-fit ICP narrower than operational ICP (positioning works for the next 50 deals).
4. Alternatives analysis includes status quo / DIY.
5. Message house: 1 primary + 3 pillars + ≥2 proofs/pillar.
6. Value-by-role variations are distinct, not minor word swaps.
7. For-and-against wedges exist for top 3 alternatives.
8. A new SDR or marketer could write outbound copy using only this document.

## Pitfalls

- **Positioning by committee.** 6 editors = mush. Single owner.
- **Tagline ≠ positioning.** Tagline is a derivative; positioning is the underlying logic.
- **Skipping alternatives analysis.** Most common failure mode. Without alternatives, positioning floats.
- **Forgetting Champion language.** Buyer-only language ignores the person actually selling internally.
- **Static positioning.** Markets move; ICPs evolve; re-position on signal, not calendar.
- **Over-claiming category creation.** "We invented a new category" without 10–18 months and budget = expensive failure.
- **Listing features as value.** Features describe the product; value describes the buyer's outcome. Drill: "and so what?" twice.
- **Same headline for buyer + user + champion.** Wrong for at least 2 of them.
- **"For everyone" positioning.** = for no one. Force trade-offs: "we are not for X."
- **Internal jargon as load-bearing words.** "Synergies / next-generation / intelligent platform" = invisible to buyers. Use their words.
- **Refusing to say no.** Great positioning includes the segments you DON'T serve.
- **Layering trends without a clear link to market.** Dunford's 5+1 model includes "relevant trends" as an *optional* amplifier — it works when the trend obviously reinforces your wedge, and fails as "cool but confusing" otherwise. Don't claim "AI-native" or "agentic" framing unless the trend genuinely reinforces your wedge AND the buyer would already use that language.
- **Treating positioning as marketing-only.** Positioning shapes product roadmap, sales strategy, and CS onboarding — not just marketing copy. If only marketing owns it, the artifact gets ignored downstream.
- **Fabricating named entities (anti-fabrication / provenance rule).** Every named entity in output (companies, people, quotes, G2 review excerpts, dates, prices, customer reference counts) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. Without a live research tool at runtime, default to `[unverified — needs check]` — never invent customer quotes ("Plant said X") or G2 review snippets to fill the buyer-language audit.

## Verification

The positioning is real when the wedge passes the 3 diagnostic tests, every load-bearing word is verified in a buyer-source quote (or flagged), the best-fit ICP is narrower than the operational ICP, alternatives include the status quo, the message house has 1 primary + 3 pillars + ≥2 proofs each, value-by-role variations are distinct, and for-and-against wedges exist for the top 3 alternatives. If any of these fails, iterate.

## Example

**User prompt:** "Build positioning for our AI runbook tool. ICP is mid-market SaaS support teams. Top competitors: Guru and Stonly."
**What should happen:** Force ≥4 alternatives including status quo (Notion/Confluence DIY, hire a knowledge manager, do nothing). List unique attributes — AI-native authoring from tickets, Zendesk/Intercom ingestion, support-team-only pricing, auto-staleness detection. Drill each to value with proof from the 4 paid pilots. Best-fit ICP: narrower than operational ICP (e.g., "Notion not deeply embedded" added). Subcategory framing ("AI-native support runbook authoring" within knowledge management). Wedge: "For Series B SaaS support teams of 5–15 who are drowning in tribal knowledge, WorkflowDoc is AI-native support runbook software that turns closed tickets into a self-updating library in days, unlike Guru which requires 4–8 weeks of manual content migration." Diagnostic: pass / pass / pass. Message house + value-by-role + for-and-against vs. Guru / Stonly / Notion-as-substitute.

**User prompt:** "Help me write our value prop. We have 0 customers."
**What should happen:** Mark positioning "hypothesis-only," confidence Medium. Substitute buyer interviews (8+ minimum) for won-deal quotes. Wedge built from interview language. Alternatives must include "manual processes + status quo" prominently. Plan to re-run after first 5 deals. Buyer-language audit flags every load-bearing word for validation.

**User prompt:** "Reposition us — current site converts at 0.4%, we think the positioning is broken."
**What should happen:** Audit current positioning + competitor positioning. Map old → new explicitly. Pull Wynter or 5 Second Test data if available. Re-run alternatives analysis (something likely missing). New ICP → new wedge → new message house. Comms plan for the change (customers / employees / partners). Don't reposition cosmetically; if the issue is product strategy (no unique attributes), surface that instead.

## Linked Skills

- Pick channels that compound the messaging → `channel-strategy`
- Convert wedge into outbound sequences → `cold-email-sequence` (planned)
- Champion-role hooks for LinkedIn → `linkedin-outreach` (planned)
- For-and-against wedges back into battle cards → loop to `competitor-analysis`
- Test wedge variants in market → `ab-testing-messaging` (planned)
- Refresh after 30+ deals → `icp-refinement-loop` (planned)

## Push to CRM

Positioning is a shared messaging asset, not entity records. Push it as research/note interactions so downstream execution skills (cold email, LinkedIn) can read it.

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Positioning canvas | `interaction` (type: `research`) | `relevance` = full canvas; tags `#positioning #positioning-canvas` |
| Wedge + 3-test diagnostic | `interaction` (type: `note`) | tags `#positioning-wedge` |
| Message house | `interaction` (type: `note`) | tags `#message-house` |
| For-and-against wedges (top-3) | `interaction` (type: `note`) | One per competitor; tags `#positioning-wedge #competitor:<slug>` |
| Buyer-language audit | `interaction` (type: `note`) | tags `#positioning #language-audit` |

Positioning does **not** push `company` or `person` records — it operates on entities created by `icp-definition` and `competitor-analysis`.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:positioning-strategy:v2.0.0"`

### Example push (positioning canvas)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#positioning #positioning-canvas",
    "relevance": "POSITIONING CANVAS v2.0.0\nAlternatives: Guru, Stonly, Notion, Confluence-DIY, status quo\nUnique attributes: AI-native authoring; per-support-seat pricing; ticket ingestion\nValue: reps resolve 25% more at Tier 1; new reps productive in 30d (was 90d)\nBest-fit ICP: Series B SaaS, 100–300 emp, support 5–15, Notion not deeply embedded\nCategory: AI-native support runbook authoring (subcategory of KM)\nWedge: For Series B SaaS support teams losing knowledge as they scale, WorkflowDoc is AI-native runbook authoring that drafts from real tickets — unlike Guru and Notion which require manual authoring no one has time for.\nFlagged for validation: 'self-updating runbook', 'authoring'.",
    "source": "skill:positioning-strategy:v2.0.0"
  }'
```

### Example push (for-and-against wedge)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Guru",
    "tags": "#positioning-wedge #competitor:guru",
    "relevance": "vs. Guru\nWHEN buyer is: Series B SaaS, support team <15, no existing wiki contract\nWE WIN BECAUSE: AI-native authoring; mid-market pricing\nTHEY ATTACK US WITH: \"You are unproven; we have 5,000 customers\"\nWE COUNTER WITH: \"They built pre-LLM. Their authoring is the bottleneck G2 reviewers complain about.\"\nFLIP QUESTION: \"How long does it take your senior support manager to write or update a runbook today?\"",
    "source": "skill:positioning-strategy:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #positioning`. Buyer-language audit rows with `[unverified — needs check]` words flow here for human validation before being adopted in outbound copy. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #positioning",
    "relevance": "Buyer-language audit row: load-bearing phrase \"self-updating runbook\" [unverified — needs check]. No buyer-source quote yet; flagged for next 5 discovery calls.",
    "source": "skill:positioning-strategy:v2.0.0"
  }'
```

### When NOT to push

- ICP not yet defined (skill should have pushed back; if it didn't, do not push positioning floating free of ICP).
- Positioning marked "to be validated" with no proof — push as `#positioning-hypothesis` instead and flag for re-run after first 5 deals.
