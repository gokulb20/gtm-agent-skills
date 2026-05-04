---
name: conversation-intelligence
description: Track patterns across conversation surfaces (call transcripts from Gong/Chorus/Grain/Fathom, reply text, meeting notes) for competitor mentions, pricing pushback, feature requests, champion language, blocker signals — and aggregate into pattern-frequency alerts when a signal crosses threshold. Use when a meeting transcript becomes available and intel needs extraction, when a campaign's reply corpus needs pattern aggregation, when competitive mentions are frequent enough to feed `competitive-intelligence` (function-1), or when product feedback patterns warrant routing to product team.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, pipeline, conversation-intelligence, pattern-mining, function-5]
related_skills:
  - reply-classification
  - objection-handling-library
  - discovery-call-prep
  - competitive-intelligence
  - icp-refinement-loop
  - customer-feedback-analysis
  - kpi-reporting
inputs_required:
  - conversation-source-transcripts-or-replies
  - pattern-taxonomy
  - frequency-thresholds-per-pattern-class
  - run-purpose-tag
deliverables:
  - per-conversation-pattern-extraction
  - cross-conversation-pattern-aggregation
  - frequency-threshold-alerts
  - routing-recommendations-per-pattern-class
  - conversation-intelligence-interaction-record
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Conversation Intelligence

Extract structured intel from unstructured conversation surfaces (call transcripts, reply text, meeting notes) — competitor mentions, pricing pushback, feature requests, champion language, blocker signals — and aggregate into pattern-frequency alerts when a class crosses threshold. Routes per pattern: competitor mentions → `competitive-intelligence` (function-1); pricing → `revenue-forecasting` ACV reality-check; feature requests → product team / `customer-feedback-analysis` (function-6); patterns affecting ICP → `icp-refinement-loop` (function-6).

> *Worked example uses WorkflowDoc (fictional, function-1/3 carry-over); procedure is vertical-agnostic.*

## Purpose

Sales conversations contain pattern data founders rarely synthesize. One call mentions Guru → noise; ten in a quarter → competitive priority. One prospect requests integration with HubSpot → noise; twelve do → product backlog input. This skill: extracts patterns per conversation; aggregates across the corpus; surfaces threshold-crossings as alerts; routes per pattern class to the right downstream skill. Goal: convert qualitative conversation noise into quantitative routing signals.

## When to Use

- "Gong transcript just dropped from Esme's call — extract intel."
- "Pull patterns from this campaign's 200 replies."
- "Are we hearing the Guru objection more often this quarter?"
- "Feature requests aggregated this month — prioritize."
- "Champion language patterns across closed-won deals — what do champions actually say?"
- Triggered when a conversation source (transcript, reply, note) lands.
- Scheduled corpus-wide aggregation (weekly default).

## Inputs Required

1. **Conversation source** — Gong/Chorus/Grain/Fathom transcript ID OR reply text from `reply-classification` OR meeting note text.
2. **Pattern taxonomy** — house-built default (5 classes; see Quick Reference); user can extend per ICP.
3. **Frequency thresholds per pattern class** — defaults: competitor mention ≥3 in 30d → `competitive-intelligence` alert; feature request ≥5 in 30d → product alert; pricing pushback ≥4 in 30d → `revenue-forecasting` alert.
4. **Run purpose tag**.

## Quick Reference

| Pattern class | Detection signal | Default routing |
|---|---|---|
| **Competitor mention** | Named competitor (from `competitor-analysis` taxonomy) appears in transcript / reply | → `competitive-intelligence` (function-1) |
| **Pricing pushback** | "expensive" / "out of budget" / "negotiate" / specific dollar pushback | → `revenue-forecasting` ACV reality-check + `objection-handling-library` for response |
| **Feature request** | "I wish" / "do you have" / specific named missing feature | → product team route (out-of-skill) + `customer-feedback-analysis` (function-6) |
| **Champion language** | Strong-affirmation phrases ("we definitely need this" / "this would solve our X problem") | → `discovery-call-prep` (champion-confirm signal) + `kpi-reporting` (champion-rate KPI) |
| **Blocker signal** | "IT/security/legal/procurement" gating language | → `discovery-call-prep` (blocker-prep mode) + `pipeline-stages` (extends Discovery duration estimate) |

| Concept | Value |
|---|---|
| **Source priority** | Transcript (Gong/Chorus/Grain/Fathom) > meeting note > reply text > inferred from context |
| **Provenance** | Each extracted pattern carries source URL or transcript timestamp + verbatim quote |
| **Aggregation window** | Default 30d rolling; user-overridable |
| **Threshold defaults** | Competitor mention: 3/30d / Pricing: 4/30d / Feature: 5/30d / Champion: 2 per deal / Blocker: 1 per deal |
| **Multi-language** | Extract verbatim in source language; one-sentence English summary added |
| **Anti-fab hard rule** | Pattern extraction must reference verbatim quote from transcript / reply; never paraphrase as the primary record |
| **Apple-MPP / non-text signals** | Open rates / clicks NOT used as conversation intel (Apple MPP makes opens noise) |

## Procedure

### 1. Validate inputs
Pull conversation source (transcript / reply / note). Confirm pattern taxonomy + thresholds loaded.

### 2. Per-conversation pattern extraction
LLM-backed extraction against the 5-class taxonomy. Output per pattern: `{class, verbatim_quote, source_timestamp_or_url, confidence: 0–1, related_entity (e.g. competitor name)}`. Confidence <0.7 → flag for manual review; do not auto-route.

### 3. Per-conversation push
For each extracted pattern, push `interaction:research` with the verbatim quote + source + class. PATCH person/company tags with new signals.

### 4. Cross-conversation aggregation (corpus-wide)
Pull all extracted patterns within aggregation window (default 30d rolling). Group by pattern class + related entity (e.g., "Guru mentions"). Count frequency.

### 5. Threshold check + alert
Per class + entity: compare frequency to threshold. If crossed → emit alert routed to the appropriate downstream skill. E.g., 4 Guru mentions in 30d → alert routed to `competitive-intelligence` with timeline + verbatim quotes; 6 HubSpot-integration requests → alert routed to product team via `customer-feedback-analysis`.

### 6. Route per pattern class
- Competitor mentions → `competitive-intelligence` signals feed.
- Pricing pushback → `revenue-forecasting` for ACV reality-check + `objection-handling-library` for response prep.
- Feature requests → `customer-feedback-analysis` (function-6) + (out-of-skill) product team channel.
- Champion language → flag in `discovery-call-prep` for champion-confirm path + `kpi-reporting` champion-rate KPI.
- Blocker signal → flag for `discovery-call-prep` blocker-prep mode + extend Discovery cycle estimate in `pipeline-stages`.

### 7. Emit run record
Per conventions: `interaction:research` with corpus stats + threshold crossings + routes triggered. Recurring artifact.

## Output Format

- Per-conversation pattern extraction (5 classes × per-conversation patterns)
- Cross-conversation aggregation (frequency per class per entity over window)
- Threshold-crossing alerts with verbatim quote evidence
- Routing recommendations per pattern class
- Per-deal champion / blocker flags PATCHed onto person/company
- Run record + recommended downstream skills triggered

## Done Criteria

1. Conversation source ingested; transcript/reply/note parsed.
2. Per-conversation patterns extracted with verbatim quotes + source timestamps.
3. Confidence floor honored (no auto-route on <0.7).
4. Per-conversation patterns pushed as `interaction:research` with provenance.
5. Cross-conversation aggregation run within window.
6. Threshold crossings emit alerts with evidence.
7. Routing per pattern class triggered to correct downstream skills.
8. Run record pushed.

## Pitfalls

- **Paraphrasing instead of verbatim.** Pattern records MUST contain the actual quote; "they mentioned Guru" without the quote = useless evidence.
- **Auto-routing low-confidence extractions.** Confidence <0.7 → manual review; sarcasm + ambiguous mentions get flagged for human.
- **Double-counting same conversation across runs.** Dedup by transcript_id + pattern + timestamp.
- **Threshold trigger without timeline context.** "5 Guru mentions" — over what time? Show window + dates.
- **Treating competitor mentions as objections automatically.** A champion saying "we considered Guru and rejected them" is positive intel, not an objection. Class extraction should distinguish.
- **Aggregation window too narrow.** 7d window misses trends; 90d window includes stale signal. 30d is the default sweet spot.
- **Skipping the outbound-team-internal patterns.** Things sales-rep says ("I told them X") are also intel-worthy for `kpi-reporting` rep-coaching.
- **Multi-language extraction failure.** Non-English transcripts need source-language extraction + English summary; never silently translate primary record.
- **Patterns that always fire (background noise).** "Decision-maker" appears in every transcript — not signal. Tune taxonomy to actionable patterns.
- **Fabricating named entities (anti-fabrication / provenance rule).** Per CLAUDE.md universal rule, every named entity (competitors, features, dollar amounts, champions, blockers) must carry `[user-provided]` (transcript / reply text from real conversation) and `[verified: <source>]` for the extracted relationship; verbatim quote required. NEVER invent quotes or paraphrase as the primary record.
- **Not routing to product feedback flow.** Feature requests collected here should propagate to product backlog; surface explicitly in run record.

## Verification

Run is real when: every extracted pattern has a verbatim quote + source reference; every threshold-crossing alert has supporting evidence (per-quote list); routing to downstream skills happened for triggered alerts; aggregation window dates explicit; per-conversation patterns dedup'd within run. Negative test: pick 5 random extracted patterns; resolve each verbatim quote against the transcript timestamp / reply text. If any quote can't be located in source, extraction is fabricating.

## Example

**User prompt:** "Esme's discovery call transcript just dropped from Gong. Extract intel."
**What should happen:** Pull Gong transcript via API. LLM-extract patterns. Findings:
- Competitor mentions: Guru ("we considered Guru last year but found their search bad") @ 12:34. Stonly ("Stonly was on our shortlist briefly") @ 14:02. — Both flagged with verbatim + timestamp; routed to `competitive-intelligence`.
- Pricing pushback: none extracted.
- Feature request: "do you have a Salesforce Service Cloud integration?" @ 18:21 — routed to `customer-feedback-analysis`.
- Champion language: "this would actually save us 6 weeks of new-hire ramp" @ 22:10 — Esme confirmed as champion; flagged for `discovery-call-prep` champion-confirm.
- Blocker signal: "IT will need to do a security review before we can pilot" @ 24:45 — routed to `discovery-call-prep` blocker-prep mode + `pipeline-stages` extend Discovery cycle estimate.
Per-conversation push: 5 `interaction:research` records. PATCH Esme: `champion_status: confirmed`. PATCH Stitchbox: `blockers: [it-security-review]`.

**User prompt:** "Aggregate the last 30 days of conversation intel — what patterns crossed threshold?"
**What should happen:** Cross-conversation aggregation across all transcripts + replies in 30d window. Findings:
- **Guru mentions: 5/30d** (threshold 3) → CROSSED. Alert routed to `competitive-intelligence` with 5 verbatim quotes + timeline.
- **Stonly mentions: 2/30d** (threshold 3) → not crossed; logged for trend.
- **HubSpot-integration requests: 6/30d** (threshold 5) → CROSSED. Alert routed to `customer-feedback-analysis` + flagged for product team.
- **Pricing pushback ($X-too-high pattern): 3/30d** (threshold 4) → not crossed.
- **IT-security-review blocker: 4/30d** (threshold 1 per deal) → 4 deals flagged for blocker-prep mode.
Push run record + 2 alert records. Recommended downstream skills triggered.

**User prompt:** "Are we hearing the Guru objection more this quarter than last?"
**What should happen:** Pull Guru-mention frequency over current quarter (90d) vs prior quarter. Compare. If material delta (e.g. 12 mentions Q3 vs 4 mentions Q2 = 3x), surface as competitive-intensity alert; route to `competitive-intelligence` for battle-card refresh + `positioning-strategy` (function-1) for counter-positioning review.

## Linked Skills

- Transcript / reply source from → `reply-classification` (replies) + Gong/Chorus/Grain/Fathom (transcripts)
- Competitor mentions → `competitive-intelligence` (function-1)
- Pricing pushback → `revenue-forecasting` + `objection-handling-library`
- Feature requests → `customer-feedback-analysis` (function-6) + product team channel
- Champion language → `discovery-call-prep` (champion-confirm) + `kpi-reporting` (champion-rate KPI)
- Blocker signal → `discovery-call-prep` (blocker-prep mode) + `pipeline-stages` (extend cycle estimate)
- Quarterly trend analysis → `kpi-reporting`
- Patterns affecting ICP definition → `icp-refinement-loop` (function-6)

## Push to CRM

Persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-5-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Per-conversation extracted pattern | `interaction` (type: `research`) | `relevance` = pattern class + verbatim quote + source timestamp/URL + related entity + confidence; `tags: "#conversation-intel #pattern-<class> #function-5"` |
| Threshold-crossing alert | `interaction` (type: `research`) | `relevance` = pattern class + frequency + window + verbatim quote list + downstream-skill-routed-to; `tags: "#threshold-alert #pattern-<class> #function-5"` |
| Per-deal champion / blocker flag | `person` / `company` (PATCH) | `champion_status: confirmed | candidate`, `blockers: [...]`, tags updated |
| Run record (corpus-wide aggregation) | `interaction` (type: `research`) | `relevance` = corpus stats + threshold crossings + routes triggered; `tags: "#conversation-intelligence-run #function-5"` |
| `[unverified — needs check]` (low confidence pattern) | `interaction` (type: `research`) ONLY | `tags: "#unverified #review-required #conversation-intelligence"`; no PATCH or downstream route |

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
GONG_API_KEY=         # or CHORUS / GRAIN / FATHOM
ANTHROPIC_API_KEY=    # or OPENAI_API_KEY (for LLM extraction)
```

### Source tag

`source: "skill:conversation-intelligence:v2.0.0"`

### Example push (extracted pattern)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "tags": "#conversation-intel #pattern-competitor-mention #function-5",
    "relevance": "Pattern extracted from Gong transcript gong_2026-06-02_esme_call. Class: competitor-mention. Related entity: Guru. Verbatim quote @ 12:34: \"we considered Guru last year but found their search bad\". Confidence: 0.94. Routed to competitive-intelligence for signals feed. Sentiment: negative-on-competitor (positive-for-us).",
    "source": "skill:conversation-intelligence:v2.0.0"
  }'
```

### Example push (threshold-crossing alert)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#threshold-alert #pattern-feature-request #function-5",
    "relevance": "Threshold crossed: HubSpot-integration feature requests 6/30d (threshold 5). Window: 2026-05-04 to 2026-06-04. Sources: 6 verbatim quotes from gong_2026-05-12_arn / gong_2026-05-19_kim / rpl_2026-05-22_per_087 / rpl_2026-05-28_mar_044 / gong_2026-05-31_jen / gong_2026-06-02_esme. Routed to customer-feedback-analysis + flagged for product team. Recommended: prioritize on backlog.",
    "source": "skill:conversation-intelligence:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

| Provenance | Push behavior |
|---|---|
| `[user-provided]` (transcript/reply text from real conversation) + `[verified: <transcript-id>:<timestamp>]` (extraction reference) | Standard mapping. |
| `[unverified — needs check]` (confidence <0.7 OR quote can't be located in source) | Pushes ONLY as `interaction:research` with `#unverified #review-required #conversation-intelligence` tags; no PATCH or downstream route. |
| `[hypothetical]` | Never pushes. Local artifact only (e.g. demo extraction in worked examples). |

### When NOT to push

- Per-conversation extraction returned 0 patterns — push run record with `#no-patterns-extracted` tag; no per-pattern records.
- Aggregation found 0 threshold crossings — push run record with `#no-threshold-crossings`; no alert records.
- Already extracted same conversation within last 7d (dedup by transcript_id) — push dedup notice only.
- `[unverified]` — see provenance routing.
- `[hypothetical]` — never.
