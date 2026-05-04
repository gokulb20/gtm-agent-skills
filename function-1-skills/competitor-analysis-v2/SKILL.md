---
name: competitor-analysis
description: Map a competitive landscape by tiering competitors (Direct/Indirect/Substitute/Aspirational), profiling positioning/pricing/strengths/weaknesses, applying Helmer's 7 Powers and segment ownership, synthesizing win/loss patterns, and producing 1-page battle cards. Use when the user mentions competitor mapping, head-to-head comparison, battle cards, moat analysis, or pre-launch competitive grounding.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, competitor-analysis, battle-cards, positioning, moats, function-1]
related_skills:
  - market-research
  - icp-definition
  - positioning-strategy
  - competitive-intelligence
inputs_required:
  - product-description
  - market-category
  - target-segments
  - geography
  - pricing-model
deliverables:
  - tiered-competitor-list
  - per-competitor-profile-set
  - head-to-head-comparison-matrix
  - helmer-7-powers-moat-analysis
  - segment-ownership-map
  - win-loss-pattern-synthesis
  - top-3-battle-cards
  - strategic-implications-summary
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Competitor Analysis

Turn a list of names into a structured competitive view that GTM, product, and sales can act on. Tiered profiles, head-to-head differentiation, structural moat assessment, and battle cards that survive real sales conversations. Goal: decision-grade competitive clarity.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Most competitor analyses are encyclopedic and useless: 15 competitors profiled to the same depth, no tiering, no honest moat call, FUD in the battle cards. This skill produces the opposite: 3–6 Direct competitors profiled with sources, Helmer's 7 Powers honestly applied (most early-stage products have 0), and battle cards a rep can use mid-call.

## When to Use

- "Who are our competitors?" / "Map the landscape"
- "How do we stack against X?"
- "Build a battle card for [competitor]"
- "What's our defensibility / moat?"
- Pre-launch competitive landscape
- Loss-reason investigation ("Why are we losing to X?")
- Pricing benchmark research
- "Alternative-to" positioning research

## Inputs Required

1. **Product description** — what it does, for whom, the outcome.
2. **Category** — buyer-recognized label, not internal jargon.
3. **Target segments** — firmographic + role.
4. **Geography**.
5. **Pricing model + ACV range**.
6. **Known competitors** (optional) — 3–10 names, including weird ones.
7. **Last 5 wins** (optional, high-value) — who you beat and why.
8. **Last 5 losses** (optional, very high-value) — who beat you and why. Most valuable data point.

## Quick Reference

| Concept | Detail |
|---|---|
| **Tiers** | Direct (same product, same buyer, same job) / Indirect (different product, same job) / **Substitute (Dunford-style alternatives — anything the buyer would do if you didn't exist: DIY, status quo, hire a person, do nothing, shift budget elsewhere)** / Aspirational (adjacent or larger) |
| **Substitute categories (must surface ≥1 from each)** | (a) DIY/manual — spreadsheets, email, internal tools, notebook · (b) Hire a person — agency, FTE, consultant, intern · (c) Do nothing / accept the problem · (d) Shift budget elsewhere — "we'd spend $X on sales hiring instead" |
| **Helmer's 7 Powers** | Scale Economies / Network Economies / Counter-Positioning / Switching Costs / Branding / Cornered Resource / Process Power |
| **Power test** | Each Power = a benefit AND a barrier. Most early-stage products have 0–1. |
| **Tier targets** | 3–6 Direct, 2–4 Indirect, 2–4 Substitute, 1–2 Aspirational |
| **Profile minimums** | Positioning + best-fit customer + 3 strengths + 3 weaknesses + pricing + 1 recent move |
| **Battle card** | 1 page; 1 wedge; 1 flip-question; 1 proof |
| **Source-priority** | Internal win/loss > customer interviews > G2/community > competitor materials > analyst reports |
| **Pricing rule** | Pricing pages lie. Triangulate Vendr / Reddit / internal sales conversations. |
| **No-FUD rule** | Every weakness needs a citation (G2 review, customer quote, public source) |

## Procedure

### 1. Build candidate list — buyer input first, then desk research
**First, pull buyer-validated alternatives.** Ask the user: "In deals you lost, what did the buyer go with instead? In deals you won, what were they about to use?" If absent, flag and recommend `competitive-intelligence` or a win/loss interview loop before full profiling.

**Then cast wide via desk research.** Add anything from G2/Capterra, Reddit "X alternatives" threads, accelerator batches.

**Critically, force ≥1 entry from each of 4 Substitute categories** (Dunford's competitive-alternatives lens):
- DIY / manual (spreadsheets, email, internal tools, notebook)
- Hire a person (outsourced agency, FTE, consultant, intern)
- Do nothing / accept the problem (status quo, low priority, ignore)
- Shift budget elsewhere ("we'd spend $X on sales hiring instead")

Goal: 15–25 raw candidates. The "shift budget elsewhere" lens is the most-missed alternative; it's what budget actually competes against in B2B.

### 2. Tier into 4 categories
Direct (3–6) / Indirect (2–4) / Substitute (2–4) / Aspirational (1–2). If Direct <3 → research more. If Direct >6 → trim to top 5.

### 3. Profile Direct + Substitute
Each gets: one-line positioning (their words), best-fit customer, 3 evidenced strengths, 3 evidenced weaknesses, pricing (range + model), 1 recent move. **No fabrication** — write "Insufficient data" if absent.

### 4. Head-to-head matrix
Top 5 + user across: positioning / best-fit ICP / pricing tier / sales motion / 3–5 category-specific capabilities.

### 5. Apply Helmer's 7 Powers
Top 3 competitors + user. Each Power needs benefit AND barrier evidence. **Be honest:** most early-stage products have 0 Powers — that's a head start, not a moat. Say so.

### 6. Map segment ownership
Per segment from `market-research`: owner / runner-up / user position (Leader / Challenger / Niche / Absent) / rationale. Surface whitespace.

### 7. Porter's 5 Forces (1 paragraph)
Sanity-check structural attractiveness — rivalry / buyer power / supplier power / new entrants / substitutes. Verdict on category.

### 8. Win/loss patterns (if data exists)
3–5 win patterns + 3–5 loss patterns + 1+ disqualifier. Sample-size confidence per pattern. If no data, replace with hypothesis section to validate after first 10 deals.

### 9. Battle cards (top 3 Direct)
Use the standard template. Paste-ready into CRM/playbook. 1 wedge, 1 flip-question, 1 proof per card.

### 10. Strategic implications
3–5 implications. Each: observation → so what → recommended action.

### 11. Route downstream
Recommend next skill with carry-forward inputs.

## Output Format

- Competitive Landscape one-pager (sections 1–10 above)
- Per-competitor profile blocks (Direct + Substitute)
- Head-to-head matrix
- Helmer 7 Powers table (top-3 + user, with benefit + barrier evidence)
- Segment ownership map
- Porter's 1-paragraph diagnostic
- Win/loss patterns + disqualifiers
- Battle cards (top 3 Direct, 1 page each)
- Strategic implications table
- Recommended next skill + carry-forward

## Done Criteria

1. Tiered list with right counts (3–6 / 2–4 / 2–4 / 1–2).
2. Direct + Substitute profiled with all 6 minimum fields, every claim cited.
3. Head-to-head matrix across top 5 + user.
4. Helmer 7 Powers honestly applied (benefit + barrier evidence per Power held).
5. Segment ownership map identifies ≥1 whitespace.
6. Porter's diagnostic produced.
7. Win/loss: 3–5 + 3–5 + 1+ disqualifier (or hypothesis section if no data).
8. Battle cards (top 3) on 1 page each.
9. Strategic implications: 3–5 with action.

## Pitfalls

- **FUD in battle cards.** Reps over-attack and lose deals. Every weakness must cite a source.
- **Manufactured moats.** Saying "we have switching costs" when you don't is malpractice. Most early-stage products have 0 Powers.
- **Skipping substitutes.** "Spreadsheets + a VA + status quo" wins more deals than any named competitor in many B2B categories.
- **Feature comparison theater.** Long checkboxes lose to "what job does the buyer hire each tool for?"
- **Pricing pages believed.** Real ACVs come from internal sales conversations or Vendr — not the published list.
- **Magic Quadrant worship.** Slow, political. One signal, not truth.
- **Battle cards reps won't use.** 1 wedge + 1 question + 1 proof beats 5 pages of feature trivia.
- **Stale snapshots.** Date every profile. >90 days = recommend `competitive-intelligence` for ongoing tracking.
- **"We have no real competitors"** is a marketing failure, not a market reality. Force substitute analysis.
- **Ignoring buyer-journey shifts.** Competitors at evaluation stage may differ from substitutes at "do nothing" stage.
- **Fabricating named entities (anti-fabrication / provenance rule).** Every named entity in output (competitor names, customer counts like "5,000+ customers", pricing, funding rounds, dates, G2 review counts/excerpts, recent moves) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. **Highest-fabrication-risk skill in this repo** — without a live research tool at runtime, default to `[unverified — needs check]`. A battle card with fabricated numbers loses deals when the buyer fact-checks.

## Verification

The analysis is real when the user can name their top 3 Direct competitors and the wedge against each, every weakness has a source, battle cards fit on 1 page with 1 wedge + 1 flip-question + 1 proof, the Helmer analysis is honest (no fake moats), the segment ownership map identifies at least one whitespace, and strategic implications drive ≥3 actions (not just observations). If any of these fails, re-run the relevant step.

## Example

**User prompt:** "Map our competitors. We sell AI runbook software for SaaS support teams; main competitors are Guru and Stonly."
**What should happen:** Build wider candidate list (Guru, Stonly, Document360, Notion, Confluence, status-quo DIY, Glean as aspirational). Tier into 4 categories. Profile Direct + Substitute with G2/Wayback/Reddit sources. Apply Helmer 7 Powers honestly — likely user has 0 Powers (head start, not moat). Segment ownership map shows mid-market Series B underserved. Battle cards for Guru, Stonly, Notion-as-substitute. Strategic implication: 12–18 month window before incumbents catch up on AI-native authoring; invest in switching-cost integrations (Zendesk/Intercom).

**User prompt:** "We have no real competitors — totally new category."
**What should happen:** Push back. Every product has substitutes (status quo, manual, DIY, adjacent). Force a 5+ alternative list including the status quo. Surface that "no competitors" usually means the buyer hasn't been researched. Produce a real landscape grounded in substitutes; recommend `market-research` re-run if category is genuinely new.

**User prompt:** "Why are we suddenly losing to X?"
**What should happen:** Pull last 10 deals where X was involved. Check Wayback Machine for X's positioning changes (last 90 days). Scan their changelog + LinkedIn for product moves + new hires. Run sentiment scan on G2 (last 30 days). Output: hypothesis with confidence labels — most likely 1–2 trigger events explain the shift (pricing change, new feature, leadership hire). Recommend `competitive-intelligence` for ongoing detection.

## Linked Skills

- Sharpen positioning vs. top competitors → `positioning-strategy`
- Refine ICP from win patterns → `icp-definition`
- Stand up ongoing monitoring → `competitive-intelligence`
- Re-run with whitespace from segment-ownership gaps → `market-research`

## Push to CRM

After producing per-competitor profiles and battle cards, persist agent-actionable records via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env`.

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each **named-product** competitor (Direct, or product-Substitute like Notion / Confluence) | `company` | `tags: "#competitor #competitor-tier:direct"` (or `:substitute`); `priority: cold` |
| Each **non-product alternative** (DIY / hire / do-nothing / shift-budget) | `interaction` (type: `research`) | `relevance` = description + buyer validation quote if available; tagged `#alternative #type:non-product #tier:substitute`. **No `company` record.** |
| Per-competitor profile (named products only) | `interaction` (type: `research`) | `relevance` = full profile; tagged `#competitor-profile` |
| Battle card (top 3) | `interaction` (type: `note`) | One per competitor; tagged `#battle-card`; `relevance` = card |
| Helmer + segment-ownership synthesis | `interaction` (type: `research`) | One; tagged `#strategic-analysis` |

Indirect / Aspirational: profile as interactions only — do not push as company records (CRM pollution).
**Why the split:** pushing "Outsourced VA" or "Do Nothing" as a `company` record creates fake prospects in the CRM. Non-product alternatives are insights, not entities.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:competitor-analysis:v2.0.0"`

### Example push (Direct competitor)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Guru",
    "website": "https://getguru.com",
    "industry": "SaaS",
    "tags": "#competitor #competitor-tier:direct",
    "priority": "cold",
    "relevance": "Direct competitor — knowledge management. Position: enterprise wiki for sales/support. Agent reads vendor docs at runtime; pricing changes — verify live before any spend. Strength: 6+ years brand, 5,000+ customers. Weakness: pre-LLM authoring UX (G2 reviews 2024–25); mid-market underserved (pushes upmarket). Helmer: Branding (partial), Switching Costs (medium). Segment ownership: 500+ emp.",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### Example push (Battle card)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Guru",
    "tags": "#battle-card #competitor:guru",
    "relevance": "BATTLE CARD — Guru\nWHEN buyer is: 100–300 emp SaaS, support-team-led purchase\nWE WIN BECAUSE: AI-native authoring; per-support-seat pricing\nTHEY ATTACK US WITH: \"You are a startup; we have 5,000 customers\"\nWE COUNTER WITH: \"We are AI-native from day one — their authoring UX is pre-LLM\"\nFLIP QUESTION: \"How long does it take your reps to author a new runbook today?\"",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### Example push (non-product alternative — interaction, not company)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#alternative #type:non-product #tier:substitute",
    "relevance": "ALTERNATIVE: DIY via spreadsheets + Slack channels. Observed in 2 lost deals (Series A SaaS with <5 support staff). Buyer quote: \"We are not ready to buy a tool; we will run this in a spreadsheet for 6 months.\" Switching cost is zero (no procurement, no IT). Beats us when: budget unavailable, team <5, pain hasn't yet hit acute trigger.",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #competitor-profile`. Critical for this skill — competitor pricing, customer counts, funding rounds, and recent moves are the highest-fabrication-risk fields. Inferred values go to the review queue, never to a live battle card. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #competitor-profile #competitor:guru",
    "relevance": "Agent reads vendor docs at runtime; pricing changes — verify live before any spend. 5,000+ customers [unverified — needs check] — claim from competitor website, not independently verified.",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### When NOT to push

- User claims "no competitors" and skill couldn't surface alternatives — do not pollute CRM.
- Aspirational / Indirect tier — keep as local artifact only.
- Non-product alternatives (DIY, hire, do-nothing, shift-budget) — these go to `interaction` only, never to `company` records, even when listed in the Substitute tier. They're insights, not prospects.
