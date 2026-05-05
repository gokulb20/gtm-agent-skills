---
name: customer-feedback-analysis
description: Extract themes from customer feedback (JTBD interviews, churn surveys, G2 reviews, support tickets) with verbatim discipline and route per theme class. Use when the user says "analyze customer interviews", "churn survey themes", "extract JTBD themes", or "product feedback patterns."
version: 2.1.0
author: Crewm8
license: MIT
metadata:
  hermes:
    tags: [Analytics, Customer-Feedback, JTBD, Theme-Extraction]
    related_skills: [icp-definition, icp-refinement-loop, positioning-strategy, competitive-intelligence, kpi-reporting]
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

# Customer Feedback Analysis

Extract structured themes from unstructured customer feedback using qualitative coding, aggregate sentiment + frequency patterns, and route per theme class. Hard rule: every extracted theme references a verbatim customer quote — never paraphrase as the primary record.

## When to Use

- ≥5 won-deal JTBD interviews completed — extract themes
- Churn survey responses accumulated — analyze
- G2/Capterra reviews landed — what are customers saying
- Support ticket themes — feed product priorities
- Conversation intelligence flagged feature-request pattern — confirm + route
- User says "analyze customer interviews" or "churn survey themes"

## Quick Reference

| Theme class | Detection signal | Default routing |
|---|---|---|
| Pain-job-anchor | Underlying job they hired product for (JTBD) | → icp-definition + positioning-strategy |
| Forces-of-progress (push/pull/habit/anxiety) | Why they switched / what held them back / what worried them | → positioning-strategy + icp-refinement-loop |
| Positive outcome | "Saved X hours" / "ramp dropped" | → kpi-reporting + case-study source |
| Feature request | "Wish you had X" / "we worked around X" | → product backlog |
| Bug/friction | "Broke when X" / "couldn't figure out Y" | → product backlog priority |
| Pricing reaction | "Worth it" / "expensive at X" | → revenue-forecasting |
| Competitor mention | Named competitor referenced | → competitive-intelligence |
| Champion language | What champion said internally to win deal | → cold-email-sequence copy bank |

| Concept | Value |
|---|---|
| Min corpus per source | 5 items for aggregation; below → individual items only |
| JTBD methodology | Bob Moesta — 4-forces (push/pull/habit/anxiety) |
| ICP-implication threshold | Theme in ≥30% of won-deal interviews → icp-refinement-loop flag |

## Procedure

1. **Validate inputs + classify per item.** Pull corpus per source. Min ≥5 for aggregation. LLM-backed per-item classification against 8-class taxonomy. See `${HERMES_SKILL_DIR}/references/theme-taxonomy.md`.
2. **Aggregate + analyze.** Group by theme class + entity; count frequency; segment by cohort/tier. Per theme: sentiment distribution + frequency vs threshold + segment concentration.
3. **Route per theme class.** Pain → icp-definition. Forces → positioning-strategy. Feature → product backlog. Pricing → revenue-forecasting. Competitor → competitive-intelligence. Champion → copy bank. See `${HERMES_SKILL_DIR}/references/routing-map.md`.
4. **ICP-implication check.** Theme ≥30% in won-deal segment → flag for icp-refinement-loop.
5. **Push + compose report.** Per-theme records with verbatim + provenance. PATCH person/company tags with feedback signals. See `${HERMES_SKILL_DIR}/scripts/push_to_crm.py`.

## Pitfalls

- Paraphrasing instead of verbatim — themes need actual customer language
- Aggregating below threshold — 4 churn responses don't make a pattern
- JTBD without 4-forces frame — misses anxieties + habit; use Moesta's push/pull/habit/anxiety
- Missing champion-language goldmine — won-deal interviews surface pure copy material
- Multi-language handled in English only — source-language extraction + English summary
- Routing without frequency — single request is noise; aggregate first

## Verification

1. Every extracted theme cites a verbatim quote + source
2. Aggregation thresholds met before pattern-claims
3. ICP-implication flags trace to ≥30% threshold
4. Product backlog routes (when configured) created actual issues
