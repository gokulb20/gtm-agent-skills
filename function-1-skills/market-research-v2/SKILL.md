---
name: market-research
description: Research and size a target market by classifying market type, framing the category via JTBD, building a triangulated TAM/SAM/SOM with explicit confidence labels, scoring segments via a bowling-pin rubric, and identifying whitespace. Use when the user mentions market sizing, category framing, segment analysis, demand validation, whitespace mapping, or needs a defensible market view before GTM execution.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, market-research, market-sizing, segmentation, whitespace, function-1]
related_skills:
  - icp-definition
  - competitor-analysis
  - positioning-strategy
  - channel-strategy
  - competitive-intelligence
inputs_required:
  - product-description
  - geography-of-scope
  - customer-type-hypothesis
  - pricing-model-and-acv-range
deliverables:
  - market-type-diagnosis
  - category-and-jtbd-statement
  - tam-sam-som-with-confidence-labels
  - segment-breakdown-with-bowling-pin-scores
  - whitespace-opportunity-cards
  - risks-and-assumptions-register
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Market Research

Produce a directional but defensible market view for GTM planning — category, sizing, segments, demand, whitespace — anchored in evidence with confidence labels. The deliverable is the foundation downstream skills (`icp-definition`, `positioning-strategy`, `channel-strategy`) build on.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Most early-stage market views are aspirational marketing language with hidden assumptions and false precision. This skill replaces that with a tight, opinionated brief: market type → category framing → triangulated sizing → segment scoring → whitespace → risks register. Every number carries a confidence tag; every load-bearing claim is in the assumptions register.

## When to Use

- "How big is this market?" / "Help me size this"
- "What category should we claim?" / "What market are we actually in?"
- "Break this market into segments" / "Who are the distinct buyer groups?"
- "Is there real demand?" / "Is this opportunity large enough?"
- "Where are the gaps in this category?"
- Pre-GTM grounding before `competitor-analysis`, `icp-definition`, `positioning-strategy`, or `channel-strategy`
- Investor or board-prep market overviews
- Geographic expansion analysis

## Inputs Required

1. **Product description** — what it does, for whom, the outcome (1–2 sentences).
2. **Geography** — named regions, not "global" (push back if user says "global").
3. **Customer type hypothesis** — at least a directional segment (size + industry + function).
4. **Pricing model + ACV range** — directional ranges acceptable.
5. **Time horizon** (optional) — defaults to 12 months.
6. **Existing customers / pilots** (optional, high-value) — names + segment patterns.

## Quick Reference

| Concept | Definition / Formula |
|---|---|
| **Market type** (Steve Blank) | existing / resegmented / new / clone — picks sizing approach |
| **TAM** | Total spend if every eligible buyer in scope bought at user pricing |
| **SAM** | TAM filtered to segments + geographies the user can reach with current motion |
| **SOM (3yr)** | Realistic 3-year capture given competitive density + motion + resourcing |
| **Bottom-up sizing** | # of target accounts × ACV × adoption % |
| **Top-down sizing** | Industry report figure × segment share |
| **Triangulation rule** | Use ≥2 methods; reconcile if disagree by >2x; single-method caps at Medium confidence |
| **Confidence labels** | `[H]` / `[M]` / `[L]` on every number — required, not optional |
| **JTBD format** | "When [situation], buyer wants to [motivation], so they can [outcome]" |
| **Bowling-pin score** | Pain + Urgency + Reach + Reference + Capacity, 1–5 each = /25 |
| **Whitespace lenses** | Segment / use-case / pricing / experience |

## Procedure

### 1. Diagnose market type
Apply Steve Blank's framework. Output one of `{existing, resegmented, new, clone}` with rationale. This determines which sizing methods are valid.

### 2. Frame the category
Three artifacts: (a) category claim — buyer-recognizable label (verify against G2/Capterra), (b) 2–4 adjacent categories, (c) JTBD statement. If buyers can't recognize the category in 5 seconds, prefer JTBD framing.

### 3. Set market boundaries
Geography (named), customer type (firmographic filters), use cases (included + excluded), time horizon, buyer persona scope. If undefined, return to intake.

### 4. Build directional sizing
Use ≥2 methods from {bottom-up, top-down, value-theory, analogous}. Show the math. Tag every assumption with source + confidence. Reconcile if methods disagree by >2x. **Never produce a single TAM number without showing the math.**

### 5. Segment with bowling-pin scoring
Produce 3–7 segments. Score each (1–5) on pain / urgency / reach / reference value / capacity. Highest-scoring = beachhead candidate. Carry forward to `icp-definition`.

### 6. Gather demand signals
Sweep: search demand (Google Trends), community pain (Reddit/HN/community Slacks), hiring signals (LinkedIn job postings), capital signals (Crunchbase), review-site momentum (G2), internal signals (highest weight). Synthesize into 5–10 signals tagged `[H/M/L]`.

### 7. Identify whitespace
Apply 4-lens diagnostic (segment / use-case / pricing / experience). 3–5 hypotheses, each with: who it serves, why incumbents ignore, why we can address, validation needed.

### 8. Synthesize + risks register
Produce the brief. Every load-bearing claim → an assumption flag. List ≥3 ways the market view could be wrong.

### 9. Route downstream
Recommend the next skill with rationale and inputs to carry forward.

## Output Format

- Market Brief one-pager (sections 1–9 above)
- Sizing model with method-by-method table + reconciliation
- Segment breakdown table with bowling-pin scores
- Demand signals table with strength labels
- Whitespace cards (3–5)
- Risks & Assumptions register
- Recommended next skill + carry-forward inputs

## Done Criteria

1. Market type diagnosed with rationale.
2. TAM/SAM/SOM with ≥2 methods + reconciliation note + per-number confidence label.
3. 3–7 segments scored on the bowling-pin rubric; beachhead identified.
4. 5–10 demand signals collected with `[H/M/L]` strength.
5. 3–5 whitespace hypotheses with validation cards.
6. Risks register filled (every load-bearing claim flagged).
7. Recommended next skill named with carry-forward inputs.

## Pitfalls

- **Treating TAM as a GTM plan.** TAM is a check. SAM and SOM drive decisions.
- **Mixing categories without boundaries.** Pick one primary frame; explicitly exclude the others.
- **Confusing Reddit upvotes with purchasing intent.** User interest ≠ buying behavior.
- **Single-source sizing.** Caps at Medium confidence. Always triangulate.
- **Over-relying on analyst reports for emerging categories.** Gartner/Forrester lag.
- **Ignoring substitutes and status quo.** "Spreadsheets + a VA" is a real competitor in many B2B categories.
- **False precision.** Three decimal places on a number with 50% uncertainty is malpractice.
- **Skipping the assumptions register.** Hidden assumptions silently break later.
- **Pilot enthusiasm ≠ market validation.** Apply bowling-pin scoring even when early customers love the product.
- **Founder default to top-down.** Top-down is unreliable for new and resegmented markets.
- **Fabricating named entities (anti-fabrication / provenance rule).** Every named entity in output (TAM/SAM/SOM numbers, named segments, comparable companies, growth rates, analyst-report figures) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. Without a live research tool at runtime, default to `[unverified — needs check]` — never invent specifics like "$4.2B TAM growing 18% CAGR" without a citation.

## Verification

The brief is real when the user can defend their TAM/SAM/SOM to a skeptical investor without rebuilding the math, can name their beachhead segment with rationale, can articulate which assumption (if invalidated) would change the strategy, and downstream skills can use the output without re-research. If any of these is "no," re-run the relevant step.

## Example

**User prompt:** "How big is the support knowledge management market for mid-market SaaS in the US?"
**What should happen:** Diagnose market type (resegmented within broader knowledge management). Frame category in buyer-language ("AI-powered support knowledge management"). Build TAM/SAM/SOM via bottom-up (Crunchbase US SaaS firm counts × estimated ACV) cross-checked top-down (KM category × support-specific slice). Reconcile within 2x. Score 3–5 segments on bowling-pin rubric, name the beachhead. Output 5–10 demand signals + 3–5 whitespace hypotheses + Risks register. Recommend `icp-definition` next.

**User prompt:** "We're building an AI agent platform for non-technical founders globally. Size it."
**What should happen:** Push back on "globally" — pin to top 2–3 markets. Diagnose as new market (no analyst data). Skip top-down sizing. Use bottom-up + value-theory + analogous (reference: low-code platforms). JTBD framing dominant because category is unstable. Confidence cap at Medium. Risks register dense with "needs primary research" flags.

**User prompt:** "Our deck claims a $40B TAM — sanity-check it."
**What should happen:** Recompute independently via bottom-up first. Then reconcile with the $40B claim. If gap >5x, the existing number is likely a category mismatch — surface methodology comparison, don't just defer. Output: corrected number with confidence, plus a note on what changed and why.

## Linked Skills

- Define ICP for the beachhead → `icp-definition`
- Map the competitive landscape → `competitor-analysis`
- Lock positioning around category + JTBD → `positioning-strategy`
- Pick acquisition channels → `channel-strategy`
- Set up ongoing market/competitor monitoring → `competitive-intelligence`
- Re-run with new geography or scope → loop back to `market-research`

## Push to CRM

After producing the brief, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`). The full Market Brief stays as the local artifact; only the records below get pushed.

### Mapping

| Deliverable | Entity | Notes |
|---|---|---|
| Beachhead segment + full Market Brief | `interaction` (type: `research`) | One per skill run; `relevance` = full brief; tags `#market-research #beachhead-defined` |
| Named Tier 1 candidate accounts | `company` | `tags: "#beachhead-candidate #market-research"`, `priority: warm` (no `score` — set in `icp-definition`) |
| Whitespace hypotheses with named target accounts | `interaction` (type: `note`) | One per whitespace card; tags `#whitespace #market-research` |

If no specific accounts are named, push only the research interaction. Do not invent accounts to fill the schema.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:market-research:v2.0.0"`

### Example push (research interaction)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "relevance": "Market Brief 2026-04-30: Resegmented market in AI-powered support knowledge management. TAM $186M (bottom-up, Medium confidence). Beachhead: Series B SaaS, 100–300 emp, US, support team 5–15. JTBD: when a new support rep needs to resolve a complex ticket and the knowledge isn'\''t in the help center, they want to find a vetted runbook fast. Top whitespace: AI-native runbook authoring, support-team-first pricing, mid-market underserved.",
    "tags": "#market-research #beachhead-defined",
    "source": "skill:market-research:v2.0.0"
  }'
```

### Example push (Tier 1 candidate company)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Stitchbox",
    "industry": "SaaS",
    "tags": "#beachhead-candidate #market-research",
    "priority": "warm",
    "relevance": "Series B SaaS, 100–300 emp, support team 5–15, US — matches beachhead segment from market-research v2.0.0. Pass to icp-definition for scoring.",
    "source": "skill:market-research:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #market-research`. TAM/SAM/SOM numbers, segment sizes, and growth rates without citations flow here for human review before being quoted in a deck or board update. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #market-research",
    "relevance": "TAM estimate $4.2B [unverified — needs check] — agent inferred from category mid-points, no analyst-report citation. Growth rate 18% CAGR [unverified — needs check] — no source. Hold for verification before quoting externally.",
    "source": "skill:market-research:v2.0.0"
  }'
```

### When NOT to push

- No beachhead identified (skill incomplete).
- TAM <$1M (deliverable is a "do not pursue" recommendation, not CRM data).
- User explicitly asked for analysis only (flag: `--no-push`).
