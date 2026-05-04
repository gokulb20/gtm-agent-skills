---
name: competitive-intelligence
description: Operationalize competitor monitoring with signal scoring (Strength × Decision-relevance), tiered watch-lists, alert routing, intel-to-action workflow, and battle-card refresh cycles. Produces a continuous monitoring system, not a snapshot. Use when the user mentions ongoing competitor tracking, alert system design, signal interpretation, battle-card refresh cadence, or win-rate diagnostics.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, competitive-intelligence, monitoring, signals, alerts, function-1]
related_skills:
  - competitor-analysis
  - market-research
  - positioning-strategy
  - icp-definition
inputs_required:
  - tiered-competitor-list-from-competitor-analysis
  - icp-from-icp-definition
  - sales-motion-plg-or-sales-led-or-hybrid
  - stage-or-arr-band
deliverables:
  - watch-list-with-monitoring-intensity-per-tier
  - signal-taxonomy-and-categories
  - detection-mapping-per-competitor
  - alert-routing-rules
  - cadence-schedule
  - intel-to-action-workflow
  - battle-card-refresh-cycle
  - signal-log-template
  - quarterly-review-template
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Competitive Intelligence

Stand up an ongoing competitive monitoring system: watch-list + signal taxonomy + alert cadence + intel-to-action workflow + battle-card refresh cycle. The output of `competitor-analysis` is a snapshot; the output of this skill is a system that prevents competitive moves from surprising the GTM team.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Without ongoing CI, battle cards rot, win-rate quietly drops, and the team learns about competitor moves from lost deals. This skill defines what to watch, how often, what counts as a meaningful signal (via a scoring rubric), who gets alerted at what threshold, and what action gets taken — sized to the team that exists.

## When to Use

- "Track our competitors going forward" / set up monitoring
- "How should we be notified when X happens?" (alert system design)
- "Is this competitor move actually meaningful?" (signal interpretation)
- "How often should we update battle cards?"
- "Are we losing more deals to X — what changed?" (win-rate diagnostic)
- Pre-launch monitoring readiness
- Quarterly competitive review prep

## Inputs Required

1. **Tiered competitor list** — from `competitor-analysis`.
2. **ICP** — from `icp-definition`.
3. **Sales motion** — PLG / sales-led / hybrid.
4. **Stage / ARR** — pre-PMF / early / growth / scale.
5. **Existing battle cards** (optional) — what we'll keep refreshed.
6. **Win/loss data feed** (optional, very high-value).
7. **Current monitoring tools** (optional) — Visualping, Klue, Crayon, etc.
8. **Team capacity** — who reads alerts, who acts.

## Quick Reference

| Concept | Detail |
|---|---|
| **Signal score** | Strength (1–5) × Decision-relevance (1–5) = 1–25 |
| **Action thresholds** | ≤4 log only / 5–9 weekly digest / 10–15 24h alert / 16–20 leadership immediate / 21–25 strategic event |
| **Watch-list ceiling** | 8 competitors max; 4 is often the sweet spot |
| **Signal categories** | Product / Positioning / Pricing / Capital / Hiring / Customer / Channel-GTM / Content / Sentiment / Win-Loss |
| **Categories per Direct top-3** | 4–6 (don't track all 10 — that's noise) |
| **Battle-card refresh** | Quarterly minimum; touch-up on score ≥10; full refresh on ≥16; new card on Direct entrant |
| **Stack by stage** | Agent reads vendor docs at runtime; pricing changes — verify live before any spend |
| **Source priority** | Internal (CRM, Gong) > External (Visualping, G2, LinkedIn) > Analyst |
| **Ownership rule** | One person owns the system or it dies |

## Procedure

### 1. Confirm and tier the watch-list
Pull from `competitor-analysis`. Top 3 Direct → heavy. Direct 4–6 → medium. Substitute → light. Aspirational → light. Cap at 8 actively monitored.

### 2. Select 4–6 categories per competitor
**Direct top-3:** Product + Positioning + Pricing + Hiring + Sentiment + Win/Loss. **Direct others:** Product + Positioning + Pricing. **Substitute:** Pricing + Sentiment.

### 3. Map detection methods
Per `(competitor × category)`: detection tool, URL/query, cadence, owner. This is the operating manual.

### 4. Set up alerts and infrastructure
Visualping on top-3 homepage/pricing/about. LinkedIn Sales Nav alerts. Crunchbase alerts. RSS for blogs/changelogs. Slack `#ci-alerts`. Notion or Linear DB for the signal log.

### 5. Define alert routing rules
Per signal type: recipient, channel, SLA. **Override:** any score ≥16 → leadership immediately.

### 6. Define cadences
Real-time / Daily (15 min triage) / Weekly (digest + log review) / Bi-weekly (battle-card touch-up if ≥10 signals) / Monthly (synthesis) / Quarterly (re-tier + full refresh).

### 7. Build intel-to-action workflow
Detected → Scored → Logged → Routed → Triaged → Action (None / Card update / Positioning review / Product input / Strategic decision) → Tagged for quarterly. Every signal lands in the log, even "no action."

### 8. Set battle-card refresh cycle
Quarterly calendar + score-driven (≥10 touch-up, ≥16 full refresh) + pattern-driven (win/loss shift) + new-Direct trigger.

### 9. Build the signal log
Use standard format (Date / Competitor / Category / Signal / S / R / Total / Source / Action / Owner). Pre-populate from `competitor-analysis`.

### 10. Define quarterly review template
Watch-list re-tier + top-5 signals + win/loss pattern shifts + battle-card refreshes + 3–5 strategic implications + next-quarter focus.

## Output Format

- Watch-list table (tiered with monitoring intensity)
- Categories-per-competitor table with rationale
- Detection mapping table (full operating manual)
- Alert routing rules table
- Cadence schedule (real-time → quarterly)
- Intel-to-action workflow diagram
- Battle-card refresh cycle table
- Signal log seeded with ≥5 historical entries
- Quarterly review template
- Recommended next skill + carry-forward

## Done Criteria

1. Watch-list ≤8 competitors, tiered with monitoring intensity.
2. 4–6 categories selected per top-3 Direct with rationale.
3. Detection mapping complete (competitor × category × tool × URL × cadence × owner).
4. Alert routing rules with score thresholds + SLAs.
5. Cadence schedule end-to-end.
6. Intel-to-action workflow documented as a flow.
7. Battle-card refresh triggers (calendar + signal-driven + pattern-driven).
8. Signal log seeded with ≥5 entries.
9. Quarterly review template ready.
10. One named system owner.

## Pitfalls

- **Building a system the team won't use.** Over-engineering kills CI faster than under-engineering. Right-size to capacity.
- **Watching too many competitors.** 8 is the ceiling; 4 is often the sweet spot.
- **Confusing volume with insight.** 50 signals/week is not better than 10 if 40 score ≤4.
- **Skipping the log.** Patterns over time are the value; one-off alerts aren't.
- **Reacting to every signal.** 70%+ should result in "no action — log only."
- **Annual battle-card refresh.** Markets move faster; quarterly minimum + signal-driven touch-ups.
- **Hidden in someone's head.** Single-person knowledge of competitor X = fragile system. Document.
- **Ignoring the status quo.** Notion / spreadsheets / "do nothing" need monitoring too.
- **Letting score thresholds drift.** Raising the bar to reduce alerts = stop seeing real signals. Tune carefully.
- **Treating CI as marketing-only.** It's GTM-wide: marketing, sales, product all consume it.
- **Fabricating named entities (anti-fabrication / provenance rule).** Every named entity in output (competitor moves, dates, product launches, leadership hires, pricing changes, public statements, G2 review excerpts) must carry a provenance tag — `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged entities are a contract violation. **Highest fabrication risk for signal-log entries** — without a live research tool at runtime, default to `[unverified — needs check]`. A signal log full of fabricated entries triggers wrong strategic moves downstream.

## Verification

The system is operational when watch-list is tiered with intensity per tier, every watched competitor has 4–6 named-detection categories, alert routing defines who-reads-what-when, cadence schedule is concrete, signal log has ≥5 historical entries, battle-card refresh has trigger rules, intel-to-action workflow is documented end-to-end, one person owns the whole system, the tooling stack is right-sized to stage and budget, and a quarterly review template exists.

## Example

**User prompt:** "Set up competitive intelligence for our 5 main competitors."
**What should happen:** Pull tiered list from `competitor-analysis`. Cap watch-list at 6 (top 3 Direct heavy + 2 medium + 1 substitute light). Categories per top-3: Product / Positioning / Pricing / Hiring / Sentiment / Win-Loss. Set up Visualping + LinkedIn Sales Nav + Crunchbase alerts. Build Notion signal log. Alert routing: score ≥10 → 24h Slack alert; ≥16 → founder DM. Cadence: daily 15-min triage, weekly digest, monthly synthesis, quarterly full refresh. Tooling cost: Agent reads vendor docs at runtime; pricing changes — verify live before any spend. Founder owns; one contractor scores + logs.

**User prompt:** "Are we losing more deals to Guru — what changed?"
**What should happen:** Diagnostic mode. Pull last 10 deals where Guru was involved. Check Wayback Machine for Guru positioning changes (last 90 days). Scan changelog/blog/LinkedIn for product moves + new hires. Sentiment scan G2 (last 30 days). Output: hypothesis with confidence labels — most likely 1–2 trigger events explain the shift (pricing change, AI feature launch, leadership hire). Action items: refresh battle card; flag to active deals; consider positioning revisit if score ≥16.

**User prompt:** "We're pre-PMF — set up CI without overengineering."
**What should happen:** Lightweight system. Top 3 competitors only, no Klue/Crayon. Visualping + Crunchbase alerts + Notion log. Manual quarterly review. Total cost: Agent reads vendor docs at runtime; pricing changes — verify live before any spend. Founder time: <30 min/week. Plan to scale at $500k ARR. Avoid the trap of building enterprise CI before there's a deal pipeline to protect.

## Linked Skills

- Major signal triggers reposition → `positioning-strategy`
- Wedge needs A/B test → `ab-testing-messaging` (planned)
- New competitor enters Direct tier → loop back to `competitor-analysis`
- Pattern suggests category shift → re-run `market-research`
- ICP shift detected from win/loss patterns → `icp-definition`

## Push to CRM

This skill is the most CRM-native of the function-1 set: the Signal Log is already a tabular schema that maps cleanly to interactions. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env`.

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Watch-list competitors | `company` | `tags: "#competitor #ci-tier:direct"` etc.; only push if not already created by `competitor-analysis` |
| Each scored signal | `interaction` (type: `note`) | `relevance` = signal description; tags `#ci-signal #competitor:<slug> #category:<x> #ci-score:<n>` |
| Signal taxonomy + alert routing rules | `interaction` (type: `research`) | One-time setup; tagged `#ci-system-config` |
| Quarterly review summary | `interaction` (type: `research`) | One per quarter; tagged `#ci-quarterly` |

**Push every signal score ≥10** (24h alert threshold). Signals 5–9 stay in local log; <5 dropped.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:competitive-intelligence:v2.0.0"`

### Example push (high-score signal)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Guru",
    "tags": "#ci-signal #competitor:guru #category:pricing #ci-score:18",
    "relevance": "2026-05-02 — Guru added new pricing tier ($30/user Enterprise) via Visualping on getguru.com/pricing. Strength: 5. Decision-relevance: 4. Total: 20. Action: refresh battle-card pricing column; flag to AE team.",
    "source": "skill:competitive-intelligence:v2.0.0"
  }'
```

### Example push (medium signal — log only)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Stonly",
    "tags": "#ci-signal #competitor:stonly #category:hiring #ci-score:9",
    "relevance": "2026-05-02 — Stonly posted Senior PMM for Support Vertical on LinkedIn. Strength: 3. Decision-relevance: 3. Total: 9. Action: log; revisit in 30d.",
    "source": "skill:competitive-intelligence:v2.0.0"
  }'
```

### Special routing

When a signal scores ≥21 (strategic event — competitor acquired / raised $50M+ / killed a product line), push to CRM **and** trigger `competitor-analysis` to re-run on that competitor. Tag `#ci-strategic-event #re-run-needed`.

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #competitive-intelligence`. Critical for this skill — signal-log entries are the input that triggers strategic moves; fabricated entries can drive a wrong reposition or wrong battle-card update. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #competitive-intelligence #competitor:guru",
    "relevance": "Signal: Guru launched AI authoring product Q1 2026 [unverified — needs check] — no Wayback URL or press citation captured. Pricing change 12% [unverified — needs check] — no Vendr/changelog source. Hold before triggering battle-card refresh.",
    "source": "skill:competitive-intelligence:v2.0.0"
  }'
```

### When NOT to push

- Signal score <10 (stays in local log only — pushing low-signal floods the CRM).
- Sentiment-only signals without a named action (sentiment shifts are lagging).
