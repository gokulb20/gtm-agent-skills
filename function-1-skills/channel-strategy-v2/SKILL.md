---
name: channel-strategy
description: Identify and prioritize go-to-market channels using Weinberg's Bullseye Framework (19 channels, three rings), CAC/LTV-per-channel math, channel-fit-by-ICP scoring, and stage-appropriate selection. Produces a focused 1–3 channel bet with experiment design, budget split, and kill criteria. Use when the user mentions channel selection, channel prioritization, channel-mix planning, or stage-transition channel decisions.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, channel-strategy, bullseye, channel-mix, traction, function-1]
related_skills:
  - icp-definition
  - positioning-strategy
  - market-research
  - competitor-analysis
  - competitive-intelligence
inputs_required:
  - icp-from-icp-definition
  - acv-and-pricing
  - sales-motion-plg-or-sales-led-or-hybrid
  - stage-or-arr-band
  - geography
deliverables:
  - 19-channel-inventory-evaluation
  - channel-fit-by-icp-matrix
  - bullseye-allocation-outer-middle-inner
  - cac-ltv-viability-table-per-channel
  - top-3-channel-deep-dives
  - per-channel-experiment-design
  - budget-allocation-plan
  - kill-and-scale-criteria-per-channel
  - stage-graduation-plan
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Channel Strategy

Decide where to spend GTM time, energy, and budget. Replace channel-by-familiarity with structured analysis: 19 channels evaluated, ICP-fit scored, CAC/LTV checked, Bullseye plan delivered. The deliverable is a focused 1–3 channel bet with experiment design, budget, and kill criteria.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Most teams spread thin across 5+ channels and do none well. This skill enforces Bullseye discipline (3 channels in the middle ring, 1 in the inner ring), pairs 1 compounding + 1 linear channel for sustainable growth, and kills channels that fail CAC math before they drain budget.

## When to Use

- "Which channels should we use?" / "We're doing too many — what to cut?"
- "How should we allocate budget across X, Y, Z?"
- "Should we try TikTok / podcasts / events?" (new-channel evaluation)
- "We're at $1M ARR — should we add channels?" (stage transition)
- "Channel X isn't working — should we kill it?" (underperformance diagnosis)
- Pre-fundraise channel narrative ("Show our channel logic to investors")

## Inputs Required

1. **ICP** — paste from `icp-definition` or describe segment + roles.
2. **ACV** — average annual contract value.
3. **Sales motion** — PLG / sales-led / hybrid.
4. **Stage / ARR** — pre-revenue / <$1M / $1–5M / $5M+.
5. **Geography**.
6. **Existing channels** (optional, high-value) — what you've tried, results.
7. **Budget** (optional) — monthly GTM spend available.
8. **Founder time + team** (optional).

## Quick Reference

### The 19 Bullseye channels (Weinberg's *Traction*)
1. Targeting blogs · 2. Publicity · 3. Unconventional PR · 4. SEM (paid search) · 5. Social and display ads · 6. Offline ads · 7. SEO · 8. Content marketing · 9. Email marketing · 10. Engineering as marketing · 11. **Viral marketing** (k-factor, refer-a-friend) · 12. Business development · 13. Sales (outbound) · 14. Affiliate programs · 15. Existing platforms · 16. Trade shows · 17. Offline events · 18. Speaking engagements · 19. Community building

| Concept | Detail |
|---|---|
| **Bullseye rings** | Outer (all 19 considered) → Middle (3 tested cheaply, ≤$1k each) → Inner (1 doubled-down) |
| **CAC viability** | Payback <12 months; LTV/CAC >3 (David Skok / SaaS canon) |
| **Channel-fit-by-ICP** | 1–5 each on Buyer presence / Buyer attention / Decision context. Sum ≥8 to qualify. |
| **Compounding vs. linear** | Compounding: SEO, content, community, eng-as-marketing, brand. Linear: outbound, paid, trade shows. **Run 1 of each at every stage.** |
| **Stage rule** | 1–3 channels drive 80% of acquisition at any stage. The rest are noise. |
| **Brian Balfour Four Fits** | Market-Product × Product-Channel × Channel-Model × Model-Market — when channel is failing despite tactics, another fit is broken |

## Procedure

### 1. Brainstorm the outer ring (all 19)
Force consideration of every channel. 1-line annotation each: "How would this work for us?"

### 2. Apply hard filters
Cut on CAC math / motion fit / stage fit / capital constraint / time constraint. Survivors: 6–10.

### 3. Score channel-fit-by-ICP
Score 1–5 on Buyer presence, Buyer attention, Decision context. Sum 3–15. Cut anything <8. Survivors: 4–7.

### 4. Pick middle ring (3 channels)
Mix: 1 likely-best (highest score) + 1 alternative (good score, founder familiar) + 1 wildcard (different mechanism, learning value). **Force ≥1 compounding + ≥1 linear.**

### 5. Design experiments per channel
Each: hypothesis / budget / duration / sample size / success / kill / owner / tools / playbook.

### 6. CAC/LTV viability per channel
Cost per lead × lead-to-close → CAC. Payback (mo) = CAC / monthly ACV. Channels failing math are killed even if scored well.

### 7. Allocate founder time + budget
Time as a resource. Budget reserves 20–30% for tests / wildcards.

### 8. Build the Bullseye plan
Outer (19) / middle (3 + experiments) / inner (TBD post-results).

### 9. Stage graduation plan
At next ARR milestone, which channels get added or swapped?

### 10. Kill / scale / iterate criteria per channel
Specific, measurable, time-bound.

## Output Format

- Channel Strategy one-pager (sections 1–10 above)
- 19-channel inventory table with stage/motion fit + 1-line annotation
- Hard-filter survivors list with rationale
- Channel-fit-by-ICP scoring table
- Middle ring (3 channels) with experiment budgets
- CAC/LTV viability table per top-3
- Per-channel experiment block (hypothesis / budget / duration / success / kill / playbook)
- Founder-time allocation + budget split tables
- Kill/scale/iterate criteria
- Stage graduation plan
- Recommended next skill + carry-forward

## Done Criteria

1. All 19 channels considered and 1-line annotated.
2. 6–10 channels survive hard filters.
3. Channel-fit-by-ICP applied; 4–7 channels pass ≥8.
4. Middle ring picks 3 channels (likely-best + alternative + wildcard).
5. CAC/LTV viability per top-3; non-viable killed.
6. Per-channel experiments designed (full block).
7. Founder-time allocation feasible.
8. Budget split sums to 100%.
9. Kill / scale / iterate criteria per channel.
10. ≥1 compounding + ≥1 linear in the mix.
11. Stage graduation plan for next 2 stages.

## Pitfalls

- **Channel-of-the-month.** Chasing whatever's hyped (TikTok, LinkedIn DMs, X) without ICP-fit math.
- **"Channel that worked at last company"** is a hypothesis, not an answer. Re-test.
- **Treating channel-product fit as known.** Until experiments run, it's hypothesis.
- **Over-investing in compounding pre-PMF.** SEO at 0 customers wastes capital.
- **Cutting compounding too early.** SEO/content take 6–12 months. Killing at week 8 is the most common mistake.
- **No kill criteria.** Channels quietly underperform for 6+ months and drain budget.
- **Over-relying on benchmarks.** Industry numbers anchor expectations; your ICP is unique.
- **Spreading thin.** 5 mediocre channels < 2 great ones.
- **Skipping the wildcard slot.** Middle ring should include 1 unfamiliar channel — learning value is real.
- **All-linear mix.** Outbound + paid + ads = no compounding base. Force ≥1 compounding.
- **Ignoring stage.** $5M ARR channels at $50k ARR = wasted capital.
- **CAC math impossible.** $50 ACV on paid LinkedIn doesn't work. Re-price or shift channel.
- **Fabricating named entities (anti-fabrication / provenance rule).** Every named entity in output (CAC/LTV figures, named communities/conferences, channel benchmarks, named tools, dollar budgets) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. Without a live research tool at runtime, default to `[unverified — needs check]` — never invent specifics like "Support Driven Slack has 8,000 members" without a citation.

## Verification

The plan is real when all 19 channels were considered, 3 are in the middle ring with explicit experiment design, each has CAC/LTV checked, each has kill/scale/iterate criteria, founder-time and budget allocations are explicit and feasible, the stage-graduation plan covers the next 2 stages, and at least 1 compounding + 1 linear channel are in the mix.

## Example

**User prompt:** "Pick channels for our $4k-ACV AI runbook tool. Hybrid motion, $150k ARR, founder-led GTM."
**What should happen:** Evaluate all 19. Cut: paid search ($300+ CPC fails $4k ACV), trade shows (premature), affiliate/PR (pre-newsworthy). Survivors include outbound (already working — 4/4 pilots), Support Driven community (ICP density 13/15), podcasts (compounding play), content marketing, SEO (compounding for next stage). Middle ring: outbound (likely-best) + community (alternative, $0 cost) + podcasts (wildcard). CAC viability: outbound $1.6k = viable; community $0 cash = viable; podcasts fail direct math but valid as compounding. Budget $5k/mo: outbound 30%, podcasts 10%, reserve 30%, tooling 30%. Kill criteria: outbound <4 meetings/mo by wk 8; community 0 inbound by day 60; podcasts <3 bookings by day 90. Stage graduation: SEO + Zendesk marketplace at $1M ARR.

**User prompt:** "Should we try TikTok? Our investor said B2B is winning there."
**What should happen:** Run channel-fit-by-ICP. For most B2B mid-market support / ops buyers, TikTok scores low on Buyer presence and Decision context. CAC unclear at this ACV. Surface bias ("investor said") as hypothesis to test. Recommend wildcard slot in middle ring at most ($500 budget, 8 weeks, hard kill criteria) — not primary. If buyer is Gen-Z founder/creator, scoring shifts.

**User prompt:** "We're at $200k ARR doing all-outbound. Are we missing something?"
**What should happen:** Audit current. Outbound = linear. Force ≥1 compounding channel in the mix. Run channel-fit on community / content / SEO — whichever scores highest with founder time available. Plan stage graduation: at $1M ARR add SEO investment + integrations marketplace. Not a recommendation to abandon outbound; a recommendation to pair it with a compounding channel before linear ceiling is hit.

## Linked Skills

- Outbound prioritized → `lead-sourcing-apollo` (planned)
- Email sequences for chosen channel → `cold-email-sequence` (planned)
- LinkedIn outreach → `linkedin-outreach` (planned)
- Performance tracking after launch → `channel-performance` (planned)
- Content channel chosen → `content-strategy` (planned)
- Community channel chosen → `community-playbook` (planned)
- ICP shift detected mid-execution → loop back to `icp-definition`

## Push to CRM

Channel strategy is a plan + budget, not entity records. Push the plan as a research interaction so downstream channel-execution skills (`lead-sourcing-apollo`, `cold-email-sequence`, `linkedin-outreach`, `channel-performance`) can read it as their input.

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Bullseye plan + budget | `interaction` (type: `research`) | `relevance` = full plan; tags `#channel-strategy #bullseye` |
| Per-channel experiment (top-3) | `interaction` (type: `note`) | One per channel; tags `#channel-experiment #channel:<name>` |
| CAC/LTV viability table | `interaction` (type: `note`) | tags `#channel-economics` |
| Kill criteria + stage graduation | `interaction` (type: `note`) | tags `#channel-kill-criteria` |

Channel strategy does **not** push `company` or `person` records — those come from `lead-sourcing-apollo` once a channel is picked.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:channel-strategy:v2.0.0"`

### Example push (Bullseye plan)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#channel-strategy #bullseye",
    "relevance": "CHANNEL PLAN v2.0.0 — stage: early ($150k ARR)\nMiddle ring: (1) Outbound — 200 accounts/wk, $2.5k, 8wk; (2) Support Driven Slack — founder time 5h/wk, $0, 12wk; (3) Podcasts (wildcard) — 6 appearances, $500, 12wk.\nBudget split: outbound 30%, podcasts 10%, reserve 30%, tooling 30%.\nKill: outbound CAC >$2k after 8wk; community 0 inbound after 60d; podcast 0 inbound after 4mo.\nCompounding/linear: community + podcasts compound; outbound linear.\nStage graduation: $1M ARR → add SEO + Zendesk/Intercom marketplace.\nFails CAC math (excluded): paid social, paid search, trade shows.",
    "source": "skill:channel-strategy:v2.0.0"
  }'
```

### Example push (per-channel experiment)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#channel-experiment #channel:outbound",
    "relevance": "EXPERIMENT — Outbound (8 weeks)\nTarget: 200 accounts/wk matching ICP firmographic\nSequence: 4 touches (email + LI), Day 0/3/7/14\nMetrics: meeting booked >2%, qualified pipeline $50k by week 8\nBudget: $2.5k (Apollo + Smartlead)\nKill: <1% reply after 4wk OR CAC >$2k after 8wk\nNext: lead-sourcing-apollo (firmographic filters from icp-definition v2.0.0)",
    "source": "skill:channel-strategy:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #channel-strategy`. CAC/LTV figures, community sizes, conference attendance, and benchmark CPC numbers without citations flow here for human review before being adopted in budgets. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #channel-strategy",
    "relevance": "Outbound CAC estimate $1.6k [unverified — needs check] — agent inferred from typical mid-market hybrid; no internal data. Support Driven Slack 8,000 members [unverified — needs check] — no citation. Hold for verification before locking budget.",
    "source": "skill:channel-strategy:v2.0.0"
  }'
```

### When NOT to push

- ICP or positioning not defined (skill should have pushed back; if it didn't, do not push a plan floating free of those inputs).
- User is pre-PMF asking for paid-channel scaling — skill should produce a "do not pursue" recommendation; push only the recommendation tagged `#channel-strategy #recommendation:hold`.
