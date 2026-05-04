---
name: customer-feedback-analysis
description: Capture and analyze customer feedback from won-deal interviews (JTBD methodology — Bob Moesta), churn surveys, G2/Capterra/TrustRadius reviews, and support tickets — extract themes via qualitative coding, surface sentiment + frequency patterns, route to product / marketing / `icp-refinement-loop`. Use when ≥5 customer interviews completed, when churn-survey responses accumulate, when product reviews land, or when `conversation-intelligence` flags feature-request patterns crossing threshold.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, optimization, customer-feedback, jtbd, function-6]
related_skills:
  - icp-definition
  - icp-refinement-loop
  - positioning-strategy
  - conversation-intelligence
  - competitive-intelligence
  - kpi-reporting
  - pipeline-stages
inputs_required:
  - customer-feedback-source-corpus
  - customer-segment-tags
  - feedback-classification-taxonomy
  - frequency-thresholds
  - run-purpose-tag
deliverables:
  - extracted-themes-with-verbatim-evidence
  - sentiment-and-frequency-aggregation
  - per-segment-pattern-breakdown
  - product-feedback-routing
  - icp-implications-flagged
  - customer-feedback-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Customer Feedback Analysis

Extract structured themes from unstructured customer feedback (won-deal JTBD interviews, churn surveys, G2/Capterra/TrustRadius reviews, support tickets), aggregate sentiment + frequency patterns, and route per theme class — product feedback to backlog (Linear/Jira); ICP-implications to `icp-refinement-loop` (function-6); positioning-implications to `positioning-strategy` (function-1); competitive mentions to `competitive-intelligence` (function-1). Hard rule: every extracted theme references a verbatim customer quote with source — never paraphrase as the primary record.

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Customer feedback is goldmine data founders rarely synthesize. Won customers tell you why they bought (JTBD); churned customers tell you why they left; review-site reviewers tell the public what they want from the category. This skill: pulls the corpus across sources; runs qualitative-coding-grade theme extraction; aggregates by frequency + sentiment + segment; routes per theme class. Goal: every actionable customer signal gets to the right team (product / marketing / sales) within the same week it surfaces.

## When to Use

- "We just completed 8 won-deal JTBD interviews — extract themes."
- "Q2 churn survey responses landed — analyze."
- "G2 reviews on us + competitors — what are customers saying about the category?"
- "Support ticket themes from last quarter — feed product priorities."
- "Conversation intelligence flagged 6 HubSpot-integration requests — confirm + route."
- Triggered by ≥5 new feedback items in any source.
- Quarterly cadence default.

## Inputs Required

1. **Customer feedback source corpus** — won-deal interview transcripts (JTBD-style) / churn-survey responses / G2/Capterra/TrustRadius review text / support ticket samples.
2. **Customer segment tags** — per customer: ICP tier / segment / closed-won-or-churned state / deal size / cohort.
3. **Feedback classification taxonomy** — house-built default (8 classes; see Quick Reference); user can extend.
4. **Frequency thresholds** — e.g., theme ≥3 mentions in 30d → product alert.
5. **Run purpose tag**.

## Quick Reference

| Theme class | Detection signal | Default routing |
|---|---|---|
| **Pain-job-anchor** | Customer describes the underlying job they hired the product for (JTBD lens — Bob Moesta) | → `icp-definition` (P-T-O refinement) + `positioning-strategy` |
| **Forces-of-progress** (push / pull / habit / anxiety) | Why they switched / what pulled them / what held them in the status quo / what worried them. Sale happens when **F1 (push) + F2 (pull) > F3 (habit) + F4 (anxiety)**. | → `positioning-strategy` (counter-anxiety messaging) + `icp-refinement-loop` |
| **Positive outcome / value realized** | "Saved X hours" / "ramp time dropped" / "team adopted in week 1" | → `kpi-reporting` (value-realization KPIs) + marketing (case-study source) |
| **Feature request** | "Wish you had X" / "we worked around X" | → product backlog (Linear/Jira) + frequency aggregation |
| **Bug / friction** | "Broke when X" / "couldn't figure out Y" | → product backlog (priority sorted) |
| **Pricing reaction** | "Worth it" / "expensive at X" / specific dollar friction | → `revenue-forecasting` ACV reality-check |
| **Competitor mention** | Named competitor referenced (positive or negative) | → `competitive-intelligence` (function-1) |
| **Champion language** (won-deal interviews) | What did the champion actually say to internal stakeholders to win the deal | → `cold-email-sequence` framework defaults (use champion language in copy) |

| Concept | Value |
|---|---|
| **Min-corpus-size floor** | 5 feedback items per source (won interviews / churn / reviews) for theme extraction; below = surface individual items, no aggregation |
| **JTBD interview methodology** | Bob Moesta (*Demand-Side Sales 101*, 2020) — 4-forces interview frame in canonical order: pushes (current pain), pulls (new-product attraction), habits (status-quo gravity), anxieties (worries about switching). Sale fires when **F1(push) + F2(pull) > F3(habit) + F4(anxiety)**. |
| **Verbatim quote rule** | Every extracted theme MUST cite a verbatim quote with source ID + timestamp/permalink |
| **Sentiment scoring** | Per-theme: positive / negative / neutral / mixed |
| **Frequency aggregation** | Default 30d window; user-overridable |
| **Per-segment breakdown** | Themes by ICP tier / segment / cohort — surface where patterns concentrate |
| **Product backlog routing** | Auto-route to Linear if `LINEAR_API_KEY` set; else surface for manual triage |
| **ICP-implication threshold** | Theme appears in ≥30% of won-deal interviews in a segment → ICP-implication flag for `icp-refinement-loop` |
| **Anti-fab hard rule** | Themes ALWAYS reference verbatim quotes; paraphrasing as the primary record forbidden |

## Procedure

### 1. Validate inputs + classify per item
Pull feedback corpus per source. Min-corpus-size ≥5 per source for aggregation; below → individual items only. LLM-backed per-item classification against 8-class taxonomy: identify themes present, extract verbatim quote + source position + sentiment + related entity (competitor / feature name).

### 2. Aggregate + analyze per theme
Group by theme class + related entity; count frequency; segment by customer cohort / tier / segment. Per theme: sentiment distribution (% positive/negative/mixed); frequency vs threshold; per-segment concentration.

### 3. Route per theme class
Pain-job-anchor → `icp-definition` + `positioning-strategy`. Forces-of-progress → `positioning-strategy` + `icp-refinement-loop`. Positive outcome → `kpi-reporting` + case-study source. Feature request → product backlog (Linear/Jira via API). Bug → product backlog priority-sorted. Pricing → `revenue-forecasting`. Competitor → `competitive-intelligence`. Champion language → `cold-email-sequence` copy bank.

### 4. ICP-implication check
Theme appears in ≥30% of won-deal interviews within a segment → flag for `icp-refinement-loop`.

### 5. Compose report + push
Per theme class: top themes by frequency + verbatim samples + sentiment + per-segment breakdown + routing. Push per-theme records (`interaction:research` with verbatim + provenance) + parent run report. PATCH person/company tags with feedback signals.

## Output Format

- Per-theme extraction with verbatim quotes + source + sentiment + frequency
- Per-class theme aggregation with per-segment breakdown
- Routing recommendations per theme class to relevant downstream skill
- ICP-implication flags (themes ≥30% in segment of won-deal interviews)
- Product backlog items (when `LINEAR_API_KEY` set, auto-create issues)
- Run record + recommended downstream skills triggered

## Done Criteria

1. Min-corpus-size per source validated (≥5 items per source for aggregation; individual items if below).
2. Per-feedback-item theme classification complete with verbatim quotes.
3. Cross-corpus aggregation per theme class + per segment.
4. Sentiment + frequency analysis per theme.
5. Routing per theme class triggered to correct downstream skills.
6. ICP-implication flags surfaced when threshold crossed.
7. Push to CRM emitted; product backlog routed (when configured).

## Pitfalls

- **Paraphrasing instead of verbatim.** Themes need actual customer language; "they said X" without quote = useless.
- **Aggregating below threshold.** 4 churn responses don't make a pattern; surface individuals.
- **Sentiment scoring without verbatim grounding.** "Negative" without the actual phrase = unverifiable.
- **Routing feature requests without frequency check.** Single-customer requests are noise; aggregate first.
- **Ignoring per-segment breakdown.** A theme appearing 20% across all customers but 60% in one segment is segment-specific signal.
- **JTBD interview without 4-forces frame.** Just "why did you buy?" misses anxieties + habit (status-quo gravity). Use Moesta's 4-forces (push / pull / habit / anxiety).
- **Treating reviews as truth.** Review-site reviews are biased (highly satisfied or dissatisfied). Combine with interviews + surveys for honest signal.
- **Missing champion-language goldmine.** Won-deal interviews surface what champions said internally — pure copy material for `cold-email-sequence`.
- **Routing to product backlog without context.** "User wants X" → useful. "12 customers in segment Y, here's the verbatim" → actionable.
- **Multi-language feedback handled in English only.** International customers need source-language extraction + English summary.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (customer names, themes, feature names, competitor mentions, dates) must carry `[user-provided]` (interview / survey / review text from real customers) + `[verified: <source>]` for the extracted relationship; verbatim quote required. NEVER invent customer quotes.
- **Skipping ICP-implication check.** Themes ≥30% in won-deal segments are ICP gold; don't treat all themes equally.

## Verification

Run is real when: every extracted theme cites a verbatim quote + source; aggregation thresholds met before pattern-claims; per-segment breakdown surfaces where patterns concentrate; ICP-implication flags trace to ≥30% threshold; product backlog routes (when configured) created actual Linear/Jira issues. Negative test: pick 5 random themes; resolve each verbatim quote against the source — if any quote can't be located in source, extraction fabricated.

## Example

**User prompt:** "8 won-deal JTBD interviews completed this quarter — analyze."
**What should happen:** Pull 8 transcripts. Per interview: classify against 8 themes using 4-forces structure. Findings:
- **Pain-job-anchor** (8/8 interviews): "WorkflowDoc is the runbook surface for support teams growing past 10 reps" — consistent core JTBD ✓ confirmed.
- **Pushes**: "knowledge fragmentation across tools" (7/8) / "new-hire ramp pain" (6/8) — strong pull-context.
- **Pulls**: "single search surface" (6/8) / "ownership clarity" (4/8).
- **Anxieties**: "what if our team doesn't adopt" (5/8) / "another tool to maintain" (3/8) — counter-anxiety messaging gap → `positioning-strategy` flag.
- **Habits**: "we considered just better Slack channels" (4/8) — DIY-status-quo gravity as primary alternative; route to `positioning-strategy` competitive-alternatives section.
- **Champion language**: "I told my VP this would cut new-hire ramp from 8 weeks to 3" (5/8) — gold for `cold-email-sequence` copy bank.
- **Competitor mentions**: Guru (3/8) — already in competitive-intelligence; Stonly (2/8) — increasing.
- **ICP-implication**: 6/8 in mid-market 100–300 emp segment → confirms current ICP, no shift needed.
Push run record + per-theme records (15+ themes total). Route champion-language to copy bank; counter-anxiety gap to `positioning-strategy`.

**User prompt:** "Q2 churn survey responses (12 churned customers) — analyze."
**What should happen:** Pull 12 responses. Themes:
- **Pricing reaction** (5/12): "fair pricing but renewal felt expensive at scale" — route to `revenue-forecasting` ACV reality-check.
- **Bug / friction** (7/12): mobile experience cited (6/12 of those), search relevance (4/12) — route to product backlog as priority items.
- **Forces-of-habit (returning to)**: "moved back to Notion as primary" (4/12), "built internal wiki" (3/12) — status-quo gravity pulled them back; surface as competitive intelligence.
- **ICP-implication**: 8/12 churned customers were sub-100-employee — suggests ICP boundary is correctly tighter (>100 emp); validate via `icp-refinement-loop` if pattern persists.

**User prompt:** "G2 reviews this month (15 reviews on WorkflowDoc + 30 on competitors) — analyze."
**What should happen:** Pull G2 corpus. WorkflowDoc reviews: positive themes (single-search-surface 12/15 / fast onboarding 8/15) → marketing case-study source. Negative themes (mobile UX 5/15 → product backlog). Competitor reviews on Guru / Stonly: surface common feature requests + bugs from competitor users — direct competitive intel for `competitive-intelligence` battle-card refresh + counter-positioning input for `positioning-strategy`.

## Linked Skills

- Pain-job-anchor + ICP-implications → `icp-definition` + `icp-refinement-loop`
- Forces-of-progress + counter-anxiety → `positioning-strategy`; competitor mentions → `competitive-intelligence`
- Positive outcomes + champion language → `cold-email-sequence` framework defaults + marketing case-study source + `kpi-reporting` value-realization KPI
- Feature requests / bugs → product backlog (Linear/Jira via API) + aggregated frequency tracking
- Pricing reactions → `revenue-forecasting` ACV reality-check
- Conversation-intel feature requests upstream from → `conversation-intelligence`; trends feed → `kpi-reporting`

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-6-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-theme extraction with verbatim | `interaction` (type: `research`) | `relevance` = theme class + verbatim quote + source ID + sentiment + related entity + confidence; `tags: "#customer-feedback #theme-<class> #function-6"` |
| Cross-corpus aggregation | `interaction` (type: `research`) | `relevance` = per-class frequency + per-segment breakdown + threshold-crossings; `tags: "#feedback-aggregation #function-6"` |
| ICP-implication flag | `interaction` (type: `research`) | `relevance` = theme + segment + frequency + recommended ICP refinement; `tags: "#icp-implication #function-6"` (feeds `icp-refinement-loop`) |
| Product backlog routing | `interaction` (type: `research`) | `relevance` = item + frequency + severity + Linear/Jira issue link if created; `tags: "#product-backlog-routed #function-6"` |
| Champion language for copy bank | `interaction` (type: `research`) | `relevance` = verbatim champion quote + source + recommended use in `cold-email-sequence`; `tags: "#champion-copy-bank #function-6"` |
| Run record | `interaction` (type: `research`) | `relevance` = corpus stats + theme distribution + routes triggered; `tags: "#customer-feedback-analysis-run #function-6"` |
| `[unverified — needs check]` (theme without verbatim) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #customer-feedback-analysis"` |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
ANTHROPIC_API_KEY=     # or OPENAI_API_KEY (for theme extraction)
G2_API_KEY=            # if pulling G2 reviews directly
LINEAR_API_KEY=        # if auto-routing product feedback
PRODUCT_REVIEW_RSS_URLS=
```

### Source tag

`source: "skill:customer-feedback-analysis:v2.0.0"`

### Example push (theme extraction)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#customer-feedback #theme-champion-language #function-6",
    "relevance": "Theme extracted from JTBD interview transcript jtbd_2026-06-15_esme. Class: champion-language. Verbatim quote: \"I told my VP this would cut new-hire ramp from 8 weeks to 3 weeks — that math made the budget conversation easy.\" Source: interview transcript @ 28:42. Sentiment: positive. Related entity: ramp-time outcome. Recommended use: feed to cold-email-sequence copy bank as champion-language pattern (replicates 5/8 won-deal interviews this quarter — strong signal).",
    "source": "skill:customer-feedback-analysis:v2.0.0"
  }'
```

### Example push (ICP-implication)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#icp-implication #function-6",
    "relevance": "ICP-implication flag from Q2 churn analysis. Theme: \"sub-100-employee size mismatch\" appears in 8/12 churn responses (67%). Segment: <100 employees. Recommendation: validate via icp-refinement-loop — current ICP boundary at >100 emp may be correctly tight; this churn pattern confirms it. Verbatim sample: \"we were too small to need WorkflowDoc's full surface; should have stayed on Notion.\" Routes to icp-refinement-loop for next quarterly run.",
    "source": "skill:customer-feedback-analysis:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (transcript / survey / review text) + `[verified: <source-id>]` (extraction reference with verbatim) | Standard mapping. |
| `[unverified — needs check]` (theme without verbatim quote OR confidence <0.7) | Pushes ONLY as `interaction:research` with `#unverified #review-required #customer-feedback-analysis` tags; no downstream routing. |
| `[hypothetical]` | Never pushes. Local artifact only. |

### When NOT to push

- Corpus below min-size per source — push individual feedback items (no aggregation); skip cross-corpus claims.
- Theme extraction returned 0 themes (rare for ≥5 items) — push run record with `#no-themes-extracted`; investigate corpus quality.
- Already analyzed same source within last 7d (dedup) — push dedup notice only.
- `[unverified]` (no verbatim) — see provenance routing.
- `[hypothetical]` — never.
