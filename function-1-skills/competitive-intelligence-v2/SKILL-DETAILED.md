---
name: competitive-intelligence
description: Build and operate an ongoing competitive monitoring system using signal scoring with explicit thresholds, watch-list construction, alert cadences, and intel-to-action workflows. Produces a monitoring playbook, signal taxonomy, alert routing rules, and battle-card refresh cycles. Use when the user needs continuous competitor tracking, alert systems, signal interpretation rules, or wants to operationalize what `competitor-analysis` produced as a one-time snapshot.
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

Operationalize one-time competitor analysis into a continuous monitoring system. Watch-list + signal taxonomy + alert cadence + intel-to-action workflow + refresh cycle — so competitive moves don't surprise the GTM team mid-deal. The output of `competitor-analysis` is a snapshot; the output of this skill is a system.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Without ongoing CI, battle cards rot, win-rate quietly drops, and the team learns about competitor moves from lost deals instead of from monitoring. This skill defines what to watch, how often, what counts as a meaningful signal, who gets alerted, and what action gets taken.

## When to Use

Trigger this skill when the user requests:
- Setting up competitive monitoring ("Track our competitors going forward")
- Alert system design ("How should we be notified when X happens?")
- Signal interpretation ("Is this competitor move actually meaningful?")
- Battle-card refresh cadence ("How often should we update cards?")
- Win-rate diagnostic ("Are we losing more deals to X — what changed?")
- Pre-launch monitoring readiness ("We're launching — how do we watch the response?")
- Quarterly competitive review prep

**Do NOT use this skill when:**
- The user wants a first-time competitor map → `competitor-analysis`
- The user wants positioning rewritten in response to a move → `positioning-strategy`
- The user wants market-level monitoring (vs. competitor-specific) → `market-research`
- The user wants help interpreting a single specific event without standing up a system → just use `competitor-analysis` light-touch

## Inputs Required

### Parameterized inputs

| Field | Profile path | Required |
|---|---|---|
| Existing competitor map (from competitor-analysis) | `{{profile.competitors.tiered_list}}` | Yes |
| ICP | `{{profile.icp}}` | Yes |
| Battle cards (from competitor-analysis) | `{{profile.competitors.battle_cards}}` | Optional, high-value |
| Sales motion | `{{profile.gtm.motion}}` | Yes |
| Team capacity for monitoring | `{{profile.gtm.team}}` | Optional |
| Current monitoring tools | `{{profile.competitors.monitoring_stack}}` | Optional |
| Win/loss data feed | `{{profile.customers.win_loss_feed}}` | Optional, very high-value |
| Stage / ARR | `{{profile.company.arr}}` | Yes |
| Risk tolerance | `{{profile.gtm.risk_tolerance}}` | Optional (default: balanced) |

### Fallback intake flow

> To set up competitive intelligence, I need:
>
> 1. **Competitor list** — your top 3–5 Direct competitors (from `competitor-analysis` if you've run it)
> 2. **ICP** — who you sell to
> 3. **Sales motion** — PLG / sales-led / hybrid
> 4. **Stage** — pre-PMF / early / growth / scale
>
> **High-leverage optional:**
> 5. **Existing battle cards** — what we'll keep refreshed
> 6. **Win/loss data** — even informal notes from last 5 wins/losses
> 7. **Monitoring tools you have access to** — Visualping, Klue, Crayon, etc.
> 8. **Who reads the alerts** — founder, sales, marketing, product

### Input validation rules

- If competitor list is missing → push back: "Run `competitor-analysis` first. Without a tiered list, monitoring is unbounded."
- If user wants to monitor 10+ competitors → push back: "Monitoring 10 well > 20 poorly. Keep watch-list to top 3 Direct + top 2 Substitutes."
- If team has no capacity to act on alerts → push back: "Alerts without action create noise fatigue. Right-size to the team that exists."
- If user is pre-PMF and asking for full CI system → suggest lightweight version (manual quarterly review + 1 alert tool).

---

## Frameworks Used

### 1. Signal Scoring Framework (Strength × Decision-Relevance)

Not all competitor news matters. Score each signal on two dimensions:

| Dimension | What it measures | Scale |
|---|---|---|
| **Strength** | How significant is this move? | 1 (rumor) → 5 (confirmed material change) |
| **Decision-relevance** | Does this affect a current decision? | 1 (interesting) → 5 (forces a response) |

**Action thresholds:**

| Score (S × R) | Action |
|---|---|
| ≤4 | Log only; review at quarterly |
| 5–9 | Brief note in weekly competitive update |
| 10–15 | Alert relevant team within 24h; may trigger battle-card touch-up |
| 16–20 | Alert leadership immediately; trigger positioning / battle-card refresh; consider GTM response |
| 21–25 | Strategic event — trigger off-cycle review; potential reposition |

This is the engine that prevents alert fatigue. Without scoring, every press release looks important; with it, 80% of signals are correctly de-prioritized.

### 2. Watch-List Construction (Tiered)

Not every competitor gets the same monitoring intensity:

| Tier (from competitor-analysis) | Monitoring intensity | Resources |
|---|---|---|
| **Direct, top 3** | Heavy — daily alerts on website / pricing / hiring; weekly on content; monthly deep-dive | Highest |
| **Direct, others (4–6)** | Medium — weekly check; monthly review | Medium |
| **Substitute / status quo** | Light — quarterly check; alert only if material shift | Low |
| **Aspirational / adjacent** | Light — quarterly check; alert if entering market | Low |

**Watch-list rules:**
- Maximum 8 competitors actively monitored
- Re-tier quarterly (some Indirect become Direct, some Direct become irrelevant)
- Add to watch-list only when justified by recent deal interaction or ICP overlap

### 3. Signal Taxonomy (What to Watch)

Standard categories for B2B competitive monitoring:

| Category | Specific signals | Detection difficulty |
|---|---|---|
| **Product** | Releases, removals, pricing changes, packaging changes, new categories | Medium |
| **Positioning** | Homepage hero, deck slide 1, key claim language | Low |
| **Pricing** | List-price changes, new tiers, discounting patterns | Medium-High (real prices hidden) |
| **Capital** | Funding rounds, M&A, layoffs, exec changes | Low |
| **Hiring** | New leadership (esp. CRO, CMO, CPO), team scale-up areas | Low |
| **Customer** | New named customer, customer churn (rare), case study patterns | Medium |
| **Channel / GTM** | Partnership announcements, integration launches, new geographies | Medium |
| **Content** | Major thought-leadership pieces, conference talks, podcasts | Low |
| **Sentiment** | G2 review trends, community chatter, employee Glassdoor | Medium |
| **Win/Loss** | Patterns in our deals (we win/lose vs. them) | High (internal) |

For each watched competitor, identify which 4–6 categories matter most. Don't track all 10 for everyone — that's noise.

### 4. Detection Mapping (Where Signals Live)

Every signal type maps to a specific detection method:

| Signal | Primary detection | Secondary |
|---|---|---|
| Website/positioning change | Visualping on key pages (home, pricing, /about) | Wayback Machine quarterly |
| Pricing change | Visualping on /pricing | Reddit / G2 reports of real ACVs |
| Product release | Their changelog + blog RSS | Twitter/LinkedIn product announcements |
| Hiring | LinkedIn company page + targeted role searches | Glassdoor for departures |
| Funding | Crunchbase + PitchBook alerts | TechCrunch / press |
| Customer wins/losses | Their case studies + LinkedIn customer logos | Won/lost deal notes (internal) |
| Sentiment | G2 reviews sorted by recent + Reddit/HN | Glassdoor (internal sentiment proxy) |
| Win/loss patterns | Internal CRM + sales call recordings | Sales rep weekly debrief |
| Partnerships | Their press releases + integration marketplaces | LinkedIn announcements |

### 5. Alert Routing Rules

Different signals go to different people. Default routing:

| Signal type | Primary recipient | Cadence |
|---|---|---|
| Pricing / positioning change | Marketing + Sales lead | <24h |
| Product release | Product + Sales lead | <48h |
| Funding / M&A | Founder / leadership | <24h |
| Hiring of key role | Founder + relevant function head | Weekly |
| Sentiment shift | Marketing | Weekly |
| Win/loss pattern emergence | Sales + Marketing | Weekly debrief |
| Partnership / integration | BD + Product | Weekly |

**Override:** any signal scoring ≥16 goes to leadership immediately, regardless of category.

### 6. Intel-to-Action Workflow

A signal isn't intel until someone decides whether and how to respond. Standard workflow:

```
SIGNAL DETECTED
    ↓
SCORE (Strength × Decision-relevance)
    ↓
ROUTE (per Alert Routing Rules)
    ↓
TRIAGE (within cadence window)
    ↓
ACTION:
  ├── Battle-card update (if affects sales messaging)
  ├── Positioning revisit (if affects category framing)
  ├── Product roadmap input (if affects competitive feature gaps)
  ├── No action — log only (most common, ~70% of signals)
  └── Strategic review (rare, score ≥21)
    ↓
LOG (in signal log; tagged for quarterly review)
```

**Critical:** every signal must end up in the log, even "no action" ones. The pattern over time is more valuable than any individual signal.

### 7. Battle-Card Refresh Cycle

Battle cards rot. Cadence rules:

| Trigger | Action |
|---|---|
| Quarterly (calendar) | Full review of all top-3 competitor cards |
| Score ≥10 signal on a competitor | Touch up affected sections within 1 week |
| Score ≥16 signal | Full card refresh within 2 weeks |
| Win/loss pattern shift detected | Review wedge sections immediately |
| New competitor enters Direct tier | Build new card; review tiering |

**Anti-pattern to avoid:** "annual" battle-card refresh. Quarterly minimum; faster on triggers.

### 8. Signal Log Format

Every captured signal gets a row:

| Field | Format |
|---|---|
| Date | YYYY-MM-DD |
| Competitor | Name |
| Category | Product / Positioning / Pricing / etc. |
| Signal | One-line description |
| Strength (1–5) | Score |
| Decision-relevance (1–5) | Score |
| Total (S×R) | Computed |
| Source | URL or "internal" |
| Action taken | None / Card update / Positioning review / etc. |
| Owner | Who handled |

The log is the institutional memory. Pattern detection happens here.

---

## Tools and Sources

### Monitoring platforms

| Tool | What it does | Cost |
|---|---|---|
| **Visualping / Wachete** | Tracks website changes (pricing, copy, headlines) | Cheap ($10–50/mo) |
| **Klue** | Full CI platform (auto-tracking, battle cards, alerts) | Paid ($$) |
| **Crayon** | CI platform (auto-collection, dashboards) | Paid ($$) |
| **Kompyte** | CI platform (lighter, more affordable) | Paid ($) |
| **Owler** | News aggregation per competitor | Freemium |
| **Crunchbase News** | Funding / M&A alerts | Freemium |

### Specific signal detection

| Source | What it's good for | Cost |
|---|---|---|
| **LinkedIn (company page + Sales Nav alerts)** | Hiring, employee growth, leadership posts | Paid for Sales Nav |
| **G2 / Capterra reviews (sorted by recent)** | Sentiment shifts, customer pain | Free |
| **Glassdoor** | Internal culture proxy, departure signals | Free |
| **Wayback Machine** | Positioning evolution over time | Free |
| **Their changelog / release notes / blog** | Product velocity and focus | Free |
| **Their job postings (parsed for skills)** | Where they're investing | Free |
| **BuiltWith / Wappalyzer** | Tech stack adoption | Freemium |
| **Reddit / HN / community Slacks** | Real customer chatter | Free |
| **Podchaser / Listen Notes** | Their podcast appearances | Freemium |
| **Common Room / Default** | Aggregate community signals | Paid |

### Internal signals (most valuable)

| Source | What it's good for |
|---|---|
| **CRM (deal-level competitor field)** | Win/loss vs. each competitor |
| **Sales call recordings (Gong, Chorus, Fathom)** | What buyers say about competitors |
| **Sales rep weekly debriefs** | Frontline intelligence |
| **Customer support tickets (mentions of competitor)** | Migration / retention signals |
| **Product analytics (signups from competitor)** | Migration patterns |

### Notification infra

| Tool | Use |
|---|---|
| **Slack channels** (#ci-alerts, #competitor-X) | Routing alerts to right team |
| **Email digests** | Weekly competitive update |
| **Notion / Linear / Asana** | Signal log + action tracking |
| **RSS readers (Feedly, Inoreader)** | Aggregate competitor blogs / changelogs |

**Stack recommendation by stage:**

- **Pre-PMF / early ($0–$500k ARR):** Visualping + Crunchbase alerts + Slack + manual log in Notion. Total: <$50/mo.
- **Early / growth ($500k–$5M ARR):** Add Sales Nav alerts + Owler + Gong/Fathom for call analysis + Slack channels per competitor. Total: $200–500/mo.
- **Growth / scale ($5M+ ARR):** Klue or Crayon as platform. Total: $1k–5k/mo + dedicated CI lead or shared role.

---

## Procedure

### Step 1: Confirm and tier the watch-list

Pull from `competitor-analysis` (or build light if missing). Confirm tiering:
- Top 3 Direct → heavy monitoring
- Direct 4–6 → medium
- Substitute → light
- Aspirational → light

Maximum 8 actively monitored. Cut if exceeding.

### Step 2: For each watched competitor, select 4–6 signal categories

Not all 10 categories matter for every competitor. Pick the ones with highest decision-relevance.

**Default selections:**
- Direct top-3: Product + Positioning + Pricing + Hiring + Sentiment + Win/Loss
- Direct others: Product + Positioning + Pricing
- Substitute: Pricing + Sentiment (mostly to detect status-quo shifts)

### Step 3: Map detection methods

For each (competitor × signal category), specify:
- Detection tool / source
- URL or query
- Cadence (real-time / daily / weekly / monthly)
- Owner

This is the operating manual. Without it, monitoring decays.

### Step 4: Set up alerts and infrastructure

Concrete setup:
- Visualping on each top-3 competitor's homepage + /pricing + /about
- LinkedIn Sales Nav alerts on each top-3 competitor's company page
- Crunchbase alerts on each top-3 + Substitute names
- RSS feeds for blogs / changelogs
- Slack channel (#ci-alerts) with routing rules
- Notion / Linear database for signal log

### Step 5: Define alert routing rules

Customize the default routing table for the team's structure. Identify:
- Who reads which signal types
- What cadence (real-time, daily digest, weekly review)
- What triggers escalation

### Step 6: Define cadences

Standard schedule:

| Cadence | Activity |
|---|---|
| Real-time | High-strength alerts (funding, exec change, pricing shift) |
| Daily | Visualping checks; Crunchbase alerts review |
| Weekly | 30-min competitive standup or async digest; signal log review |
| Bi-weekly | Battle-card touch-up if any score ≥10 signals |
| Monthly | Synthesis: which competitors moved, what patterns emerged |
| Quarterly | Full review: re-tier watch-list; refresh all battle cards; reposition if signal warrants |

### Step 7: Build intel-to-action workflow

Document the workflow per the framework. Make it concrete: who does what at each step. Avoid vague phrases like "team reviews."

### Step 8: Set battle-card refresh cycle

Apply the trigger table. Calendar-driven (quarterly) + signal-driven (score thresholds) + pattern-driven (win/loss shifts).

### Step 9: Build the signal log

Use the standard format. Pre-populate with any existing signals from `competitor-analysis`.

### Step 10: Define quarterly review template

Standard quarterly template:
- Watch-list re-tiering
- Top 5 signals from quarter (highest scores)
- Win/loss pattern shifts
- Battle-card update needs
- Strategic implications (positioning / roadmap inputs)

### Step 11: Route downstream

Recommend next skill based on findings.

---

## Output Template

---

### Competitive Intelligence System: [Product Name]

**Prepared:** [date]
**Stage:** [scope]
**Confidence:** [H/M/L]

---

**1. Watch-List (tiered)**

| Competitor | Tier | Monitoring intensity | Categories tracked |
|---|---|---|---|
| | Direct top-3 | Heavy | Product, Positioning, Pricing, Hiring, Sentiment, Win/Loss |
| | Direct other | Medium | Product, Positioning, Pricing |
| | Substitute | Light | Pricing, Sentiment |
| | Aspirational | Light | Strategic moves only |

**2. Signal Taxonomy and Categories per Competitor**

(For each watched competitor, list which categories are tracked, with rationale)

**3. Detection Mapping**

| Competitor | Category | Detection method | URL / query | Cadence | Owner |
|---|---|---|---|---|---|

**4. Alert Routing Rules**

| Signal type | Score threshold | Recipient | Channel | SLA |
|---|---|---|---|---|

**5. Cadence Schedule**

| Cadence | Activity | Owner | Time required |
|---|---|---|---|

**6. Intel-to-Action Workflow**

[Diagram or step-by-step]

**7. Battle-Card Refresh Cycle**

| Trigger | Action | Owner | SLA |
|---|---|---|---|

**8. Signal Log (initial seeding)**

| Date | Competitor | Category | Signal | S | R | Total | Source | Action | Owner |
|---|---|---|---|---|---|---|---|---|---|

**9. Quarterly Review Template**

```
=== Q[X] [YEAR] Competitive Review ===
Watch-list updates: [add/remove]
Top 5 signals this quarter (by S×R): [list]
Win/loss pattern shifts: [trends]
Battle-card refreshes completed: [list]
Strategic implications: [3–5 takeaways]
Next quarter focus: [priorities]
```

**10. Recommended Next Step**

[Named follow-on skill + 1-sentence rationale]

---

## Worked Example

> *The example below uses **WorkflowDoc**, a fictional AI-native runbook authoring tool for B2B SaaS support teams. The fictional product is shared across all six function-1 skills so the worked examples interlock. The frameworks below apply to any B2B GTM context.*

**Input:**

> Existing competitor map: Guru `[hypothetical]`, Stonly `[hypothetical]`, Document360 `[hypothetical]` (Direct); Notion `[hypothetical]`, Confluence `[hypothetical]` (Substitute) — from `competitor-analysis`
> ICP: Series B SaaS support teams (from `icp-definition`)
> Motion: Hybrid (PLG → SLG)
> Stage: Early ($150k ARR `[hypothetical]`, 4 paid pilots `[hypothetical]`)
> Existing battle cards: Guru, Stonly (built last month)
> Win/loss data: Won 3 vs. Guru, 1 vs. Stonly; Lost 1 to Notion-status-quo, 1 to Confluence DIY `[all hypothetical]`
> Monitoring tools: None currently
> Team: 1 founder + 1 part-time content contractor

### Output:

> **Provenance note for the agent reading this example:** every named entity below (competitor moves, dates, product launches, leadership hires, pricing changes, public statements, G2 review excerpts, signal sources) is `[hypothetical]` — i.e., fictional content for illustration. **Signal logs are the highest-stakes output of this skill** — they trigger downstream strategic moves (battle-card refreshes, repositioning, deal-team alerts). In real user output, the agent must apply the per-entity tagging discipline using `[user-provided]` / `[verified: <source-or-url>]` / `[unverified — needs check]` as appropriate (see `## Guardrails` provenance rule). Fabricated signals cascade into wrong actions.

---

### Competitive Intelligence System: WorkflowDoc

**Prepared:** 2026-04-30
**Stage:** Early ($150k ARR)
**Confidence:** Medium

---

**1. Watch-List**

| Competitor | Tier | Intensity | Categories tracked |
|---|---|---|---|
| Guru | Direct top-3 | Heavy | Product, Positioning, Pricing, Hiring, Sentiment, Win/Loss |
| Stonly | Direct top-3 | Heavy | Product, Positioning, Pricing, Hiring, Sentiment, Win/Loss |
| Document360 | Direct other | Medium | Product, Positioning, Pricing |
| Notion (as status quo) | Substitute | Light | Pricing, AI features (sentiment) |
| Confluence (as status quo) | Substitute | Light | AI features only |
| Glean | Aspirational | Light | Strategic moves only (could enter mid-market) |

Total: 6 watched. Within budget.

**2. Categories per Competitor (rationale)**

- **Guru** — full coverage. They're the primary threat (raised $30M; AI authoring product launching Q1 2026). Hiring matters: AI/ML hires signal feature acceleration.
- **Stonly** — full coverage. Smaller threat than Guru but moving fastest into our wedge (announced AI/ML hiring April 2026).
- **Document360** — lighter. Different ACV tier; lower risk to current deals.
- **Notion (as substitute)** — only Pricing and AI features matter. We don't compete with Notion's product roadmap broadly; we lose deals when buyer says "Notion is good enough." Watch their support-team-specific moves.
- **Confluence** — narrowest watch: only AI features. Atlassian's AI strategy is the relevant signal.
- **Glean** — quarterly check only. They're enterprise-focused now; if they move down-market, that's a re-tier event.

**3. Detection Mapping**

| Competitor | Category | Detection | URL/Query | Cadence | Owner |
|---|---|---|---|---|---|
| Guru | Product | Visualping + RSS | getguru.com/blog + changelog | Daily | Contractor |
| Guru | Positioning | Visualping | getguru.com (homepage) + /product | Daily | Contractor |
| Guru | Pricing | Visualping + Reddit | getguru.com/pricing + r/CustomerSuccess | Daily | Contractor |
| Guru | Hiring | LinkedIn Sales Nav | "Guru" + AI/ML titles | Weekly | Founder |
| Guru | Sentiment | G2 reviews (last 30 days) | g2.com/products/guru/reviews | Weekly | Contractor |
| Guru | Win/Loss | Internal CRM + Gong | "Guru" mentions in deals | Weekly | Founder |
| Stonly | Product | Visualping + RSS | stonly.com/blog | Daily | Contractor |
| Stonly | Positioning | Visualping | stonly.com (homepage) | Daily | Contractor |
| Stonly | Pricing | Visualping | stonly.com/pricing | Daily | Contractor |
| Stonly | Hiring | LinkedIn Sales Nav | "Stonly" + AI/ML titles | Weekly | Founder |
| Stonly | Sentiment | G2 reviews | g2.com/products/stonly/reviews | Weekly | Contractor |
| Stonly | Win/Loss | Internal CRM | "Stonly" mentions | Weekly | Founder |
| Document360 | Product/Pos/Pricing | Visualping | document360.com (home + /pricing) | Weekly | Contractor |
| Notion | Pricing/AI | Visualping | notion.so/pricing + Notion AI page | Weekly | Contractor |
| Confluence | AI features | RSS + Visualping | atlassian.com/software/confluence/ai | Monthly | Contractor |
| Glean | Strategic | RSS + Crunchbase | glean.com/blog + funding alerts | Monthly | Founder |

Tools cost: Visualping ($30/mo for 10 pages), LinkedIn Sales Nav ($99/mo), Gong (already paid for sales). RSS feeds via Feedly (free).

Total monthly tooling cost for CI: **~$130/mo**.

**4. Alert Routing**

| Signal type | Score threshold | Recipient | Channel | SLA |
|---|---|---|---|---|
| Pricing change | ≥5 (any) | Founder + contractor | #ci-alerts Slack | 24h |
| Positioning change (homepage hero) | ≥10 | Founder | DM + #ci-alerts | 24h |
| Product release | ≥10 | Founder | #ci-alerts | 48h |
| Funding / M&A | Always alert | Founder | DM | 24h |
| Key hire (CRO/CMO/CPO/Head of AI) | Always alert | Founder | #ci-alerts | Weekly digest |
| AI/ML engineer hires | ≥4 hires/qtr | Founder | Monthly review | Monthly |
| Win/loss shift | Pattern emerges | Founder | Weekly debrief | Weekly |
| Sentiment swing on G2 | ≥0.3 star drop or rise | Contractor | Weekly digest | Weekly |
| Score ≥16 (any) | Always | Founder | DM + immediate review | <24h |

**5. Cadence Schedule**

| Cadence | Activity | Owner | Time |
|---|---|---|---|
| Real-time | Visualping fires; Crunchbase alerts; Sales Nav alerts | Founder + contractor | <30 min reactive |
| Daily | Triage alerts, score, log | Contractor (15 min) | 15 min |
| Weekly | Mon morning competitive digest (1-pager); review signal log | Contractor → founder | 30 min synth + 15 min read |
| Bi-weekly | Battle-card touch-up if any signal ≥10 | Contractor | 1 hr |
| Monthly | Synthesis: trends, win/loss patterns | Founder | 1 hr |
| Quarterly | Full review: re-tier, refresh all cards, strategic synthesis | Founder | 4 hrs |

Total weekly time commitment:
- Contractor: 2.5 hrs/week
- Founder: 1.5 hrs/week + monthly/quarterly time

**6. Intel-to-Action Workflow**

```
SIGNAL DETECTED (Visualping fires / Sales Nav alert / G2 review / Sales rep notes a competitor mention)
    ↓
CONTRACTOR scores Strength (1-5) and Decision-relevance (1-5)
    ↓
LOG entry created in Notion CI database (date, competitor, category, signal, scores, source)
    ↓
ROUTE per Alert Routing Rules
    ↓
TRIAGE within cadence window:
   • Score ≤4: log only, surface in monthly review
   • Score 5-9: weekly digest entry
   • Score 10-15: founder reviews within 24h, may trigger battle-card touch-up
   • Score 16-20: founder + relevant team review same-day; trigger battle-card refresh
   • Score 21-25: strategic event — emergency review; potential reposition decision
    ↓
ACTION TAKEN (logged in same row):
   • None / Battle-card update / Positioning review / Product input / Strategic decision
    ↓
TAGGED for quarterly review
```

**7. Battle-Card Refresh Cycle**

| Trigger | Action | Owner | SLA |
|---|---|---|---|
| Quarterly | Full review of Guru + Stonly cards | Founder + sales support | 1 week |
| Score ≥10 signal on Guru | Touch up affected section (e.g., pricing if Guru changed prices) | Contractor (draft) → founder (approve) | 1 week |
| Score ≥16 signal | Full refresh of that competitor's card | Founder | 2 weeks |
| Win/loss pattern shift | Review wedge sections immediately | Founder | 1 week |
| New Direct competitor enters | Build new card; consider re-tier of existing | Founder | 2 weeks |

**8. Signal Log (initial seeding from competitor-analysis snapshot)**

| Date | Competitor | Category | Signal | S | R | Total | Source | Action | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 2026-04-22 | Guru | Capital | Raised $30M Series C | 5 | 4 | 20 | Crunchbase | Battle-card noted; founder reviewed | Founder |
| 2026-04-15 | Guru | Product | Announced AI-native authoring product line | 5 | 5 | 25 | Press release | **Strategic event** — accelerate GTM in next 2 quarters; lock 30+ refs | Founder |
| 2026-04-08 | Stonly | Hiring | Hiring AI/ML engineers (job postings) | 4 | 4 | 16 | LinkedIn | Watch list intensified; quarterly review flagged | Founder |
| 2026-04-02 | Stonly | Pricing | Pricing simplification | 3 | 3 | 9 | Wayback Machine | Note in weekly digest; no card update | Contractor |

**9. Quarterly Review Template**

```
=== Q[X] [YEAR] Competitive Review ===

WATCH-LIST UPDATES:
- Add: [if any]
- Remove: [if any]
- Re-tier: [if any]

TOP 5 SIGNALS THIS QUARTER (by S×R):
1. [signal] (score) — implication
2. ...

WIN/LOSS PATTERN SHIFTS:
- vs. Guru: [trend]
- vs. Stonly: [trend]
- vs. Notion (status quo): [trend]

BATTLE-CARD REFRESHES COMPLETED:
- [card] — date — what changed

STRATEGIC IMPLICATIONS (3–5):
- [observation → so what → recommended action]

NEXT QUARTER FOCUS:
- [priority 1]
- [priority 2]
```

**10. Recommended Next Step**

→ `positioning-strategy` (light revisit). Given Guru's AI-authoring announcement (signal score 25), the wedge needs to be tested under their new claim. Re-validate the "their AI is bolt-on, ours is native" angle with 2 buyer interviews in next 30 days.

Secondary: route to `ab-testing-messaging` (planned) once re-positioning is locked, to test new wedge variants in outbound.

---

## Heuristics

- **Most signals are noise.** 80% of competitor moves don't change anything. The scoring engine exists to filter the 20% that matter.
- **Internal signals beat external signals.** Sales rep saying "I'm hearing more X in deals" is higher signal than any press release.
- **Win/loss patterns are the gold standard.** A pattern of 3+ losses to the same competitor with similar buyer profiles is more important than any product launch announcement.
- **Don't over-tool.** Visualping + LinkedIn alerts + a Notion log gets you 80% of what Klue does for $0 + free tier.
- **Battle cards rot fast in active categories.** Quarterly is a floor; touch-up on every ≥10 signal.
- **One person owns the system or it dies.** Distributed CI = nobody's CI.
- **Alerts without action create fatigue.** Right-size to team capacity. Better to track 3 competitors well than 8 poorly.
- **The competitor you don't watch is the one that surprises you.** Quarterly Substitute and Aspirational checks catch entrants.
- **Hiring signals are leading indicators.** Job postings often precede product moves by 6–9 months. Watch them.
- **Pricing changes are leading indicators of strategy shifts.** Pricing is hard to change; when they change it, something is happening.
- **Sentiment shifts on G2 are lagging.** They confirm what the system should already know.

## Edge Cases

### Stealth or pre-launch competitor entering market
- Add to watch-list immediately at Direct tier (treat as new entrant).
- Detection shifts to: founder LinkedIn, job postings, beta customer mentions, domain DNS, accelerator batches.
- Confidence cap: Low until they're public.

### Competitor pivots away from category
- Re-tier or remove from watch-list.
- Document the pivot — useful for "where the category isn't going" insight.

### Acquisition / merger of two competitors
- Treat as score-25 strategic event. Refresh both cards into a single combined view.
- Re-evaluate market dynamics; may force `competitor-analysis` re-run.

### Open-source competitor with commercial offering
- Different signal categories: GitHub stars/contributors/downloads matter more than press.
- Watch their commercial offering's pricing separately.

### Competitor in different geography expanding
- Trigger condition: their hiring or partnerships in our geography.
- Add to watch-list when expansion is confirmed.

### Conflicting signals about the same competitor
- Higher-strength signal trumps lower-strength.
- Internal data > external data.
- Wait for triangulation before high-stakes action.

### Competitor goes quiet (no signals for 90+ days)
- Could mean: focused execution OR distress OR pivot.
- Increase scrutiny: check Glassdoor, LinkedIn departures, customer churn signals.
- Don't assume "no news = nothing happening."

### Public companies (10-K / 10-Q signals)
- Earnings calls are gold for direct mentions of strategy.
- Add 10-K reviews to quarterly cadence.
- Investor day presentations = strategic insight.

## Failure Modes and Recovery

| Failure mode | Symptom | Recovery |
|---|---|---|
| Alert fatigue | Team ignores Slack channel | Re-tune scoring thresholds; raise the bar to what triggers alerts; reduce watch-list size |
| Signal log empty after 30 days | No one is logging | One person owns the system; reduce friction (template + simple form); make it 5-min/day |
| Battle cards still stale | Signals come in but cards never update | Add SLA enforcement; auto-create tasks for card refresh on score ≥10 |
| Win/loss data missing | No CRM field or field unfilled | Add mandatory "competitor faced" + "win/loss reason" CRM fields; review weekly |
| Sales reps don't share intel | Insights stay in their heads | Weekly 15-min standup; reward sharing; integrate into Gong/Chorus tagging |
| Tool stack too expensive | Klue/Crayon out of budget | Downgrade to Visualping + manual; CI quality survives |
| One competitor dominates discussion | All energy spent on one, ignoring others | Quarterly re-tier; force time-budget per competitor |
| Old battle cards cited in deals | Stale data influences sales | Add "last updated" timestamp on every card; reps trained to check |
| Quarterly review gets skipped | Nobody owns it | Calendar-block; treat as quarterly board prep |

## Pitfalls

- **Building a system the team won't use.** Over-engineering kills CI faster than under-engineering.
- **Watching too many competitors.** 8 is the ceiling; 4 is often the sweet spot.
- **Confusing volume with insight.** 50 signals/week is not better than 10 if 40 of them score ≤4.
- **Skipping the log.** Patterns over time are the real value; one-off alerts aren't.
- **Reacting to every signal.** 70%+ of signals should result in "no action — log only."
- **Treating CI as a marketing function.** It's GTM-wide: marketing, sales, product all consume it.
- **Annual battle-card refresh.** Markets move faster; quarterly minimum.
- **Hidden in someone's head.** If the only person who knows competitor X is one person, the system is fragile.
- **Ignoring the status quo.** Notion / spreadsheets / "do nothing" are real competitors and need monitoring too.
- **Letting score thresholds drift.** If you keep raising the bar to reduce alerts, you stop seeing real signals. Tune carefully.

## Verification

The system is operational when:
1. Watch-list is tiered with monitoring intensity per tier.
2. Each watched competitor has 4–6 categories tracked with named detection methods.
3. Alert routing rules define who reads what, when.
4. Cadence schedule is concrete (real-time / daily / weekly / monthly / quarterly).
5. Signal log is initialized and has at least 5 historical entries.
6. Battle-card refresh cycle has trigger rules.
7. Intel-to-action workflow is documented end-to-end.
8. One person owns the system overall.
9. Tooling stack is right-sized to stage and budget.
10. Quarterly review template exists.

## Done Criteria

1. Watch-list ≤8 competitors with tiered monitoring intensity.
2. 4–6 signal categories selected per top-3 Direct.
3. Detection mapping table complete (competitor × category × tool × URL × cadence × owner).
4. Alert routing rules with score thresholds + SLAs.
5. Cadence schedule end-to-end (real-time → quarterly).
6. Intel-to-action workflow documented as a flow.
7. Battle-card refresh cycle (calendar + signal-driven + pattern-driven triggers).
8. Signal log initialized + ≥5 entries from `competitor-analysis` snapshot.
9. Quarterly review template ready for first review.
10. One named owner for the whole system.

## Eval Cases

**Eval 1 — Crowded category, multiple competitors:**
*Input:* CRM software for SMB law firms, 5 Direct competitors named, founder + small team
*Expected output:* Tiered watch-list (top 3 heavy, 2 medium), 6 categories per top-3, Visualping + LinkedIn + Crunchbase setup, quarterly + signal-driven battle-card refresh.

**Eval 2 — Single dominant competitor:**
*Input:* Niche product where 1 competitor (e.g., Salesforce in a specific category) dominates, plus 2 emerging entrants
*Expected output:* Heavy monitoring on the 1 dominant; medium on 2 emerging; explicit "what would Salesforce moving here look like" signals defined; quarterly check on adjacent BigCo plays.

**Eval 3 — Pre-launch, building from zero:**
*Input:* New product launching in 60 days; user wants monitoring system in place from day 1
*Expected output:* Lightweight system (3 competitors max, Visualping + alerts only), low-cadence (weekly), with explicit plan to scale up at $500k ARR. Avoids over-engineering.

**Eval 4 — Win-rate dropped against one competitor — diagnostic mode:**
*Input:* User reports: "We used to win 70% vs. X; now winning 30%. What changed?"
*Expected output:* Diagnostic protocol — pull last 10 deals against X, check Wayback Machine for X's positioning changes, scan their recent product releases, check pricing changes, run sentiment scan on G2, output hypothesis with confidence labels.

## Guardrails

**On provenance (anti-fabrication — universal rule):**
- **Every named entity in output carries an inline provenance tag** at first mention and on any fact-bearing assertion. Allowed tags: `[user-provided]` / `[verified: <source-or-url>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged named entities are a contract violation. Named entities include: competitor moves, dates, product launches, leadership hires, pricing changes, public statements, G2 review excerpts, signal sources.
- **No silent assertion.** If you don't have a source and didn't get it from the user, default to `[unverified — needs check]` — never to a confident-looking specific (e.g., never claim "Competitor X launched feature Y on date Z" without a URL).
- **Tool-grounding rule:** competitive intelligence is fabrication-prone — signals look authoritative even when invented. If no live research tool (web search, Visualping, news monitoring) is available at runtime, every signal-log entry defaults to `[unverified — needs check]`. The agent does NOT generate plausible-sounding signals to fill the monitoring template.
- **Worked example warning.** Worked examples in this skill contain specific-sounding-but-fictional competitor signals, tagged `[hypothetical]`. Do NOT replicate that pattern in real user output without the provenance tags + grounding above. A signal log full of fabricated entries triggers wrong strategic moves downstream.

**On signal quality:**
- Every signal logged with strength + decision-relevance scores.
- Source cited for every entry.
- Distinguish observed facts from inferred meaning.

**On scope:**
- Maximum 8 actively monitored competitors.
- Maximum 6 categories per Direct top-3.
- Re-tier quarterly.

**On tooling:**
- Right-size to stage. Pre-PMF doesn't need Klue; $5M ARR may.
- Total CI tooling spend should track to <2% of GTM budget at most stages.

**On bias:**
- Don't only watch the competitor you fear most. Substitute and Aspirational matter.
- Internal signals (sales rep intel, win/loss) get weighted equally with external signals.
- Quarterly re-tier prevents one-competitor obsession.

**On legality and ethics:**
- Public sources only. No social engineering, no impersonation, no unauthorized access.
- Don't scrape behind paywalls or logins user doesn't legitimately have access to.
- Information in battle cards must be defensible if a competitor saw it.
- No "test competitor's product as a real prospect with false identity" — refuse if requested.

**On freshness:**
- Date every signal log entry.
- Stamp battle cards with last-updated date.
- Anything >90 days old is flagged stale at quarterly review.

**On team capacity:**
- Don't design a system that requires more time than the team has.
- Better to monitor 3 competitors well than 8 poorly.
- Founder time on CI should track to <5% at early stage; scaled hire takes over at $5M+ ARR.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Major signal triggers reposition | `positioning-strategy` | Trigger event, current wedge, hypothesis update |
| Wedge needs to be A/B tested | `ab-testing-messaging` (planned) | Current wedge, signal-driven hypothesis variants |
| New competitor enters Direct tier | Loop back: `competitor-analysis` | Watch-list update, profile request |
| Win/loss pattern shifts | (Sales playbook update — planned skill) | Pattern data, wedge implications |
| Quarterly synthesis ready for board / leadership | (Reporting skill — planned) | Quarterly review output |
| Market-level shift detected (not just competitor) | `market-research` (re-run) | Signal cluster suggesting category shift |

---

## Push to CRM

This skill is the most CRM-native of the function-1 set: the **Signal Log is already a tabular schema** that maps cleanly to interactions. Every scored signal becomes an interaction. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Watch-list (tiered competitor list) | `company` | One per competitor — `tags: "#competitor #ci-tier:direct"` etc.; only push if not already a company record from `competitor-analysis` |
| Each scored signal in the log | `interaction` (type: `note`) | `relevance` = signal description; tags `#ci-signal #competitor:<slug> #category:<pricing\|hiring\|product\|...>` |
| Signal taxonomy + alert routing rules | `interaction` (type: `research`) | One-time setup interaction; tagged `#ci-system-config` |
| Quarterly review summary | `interaction` (type: `research`) | One per quarter; tagged `#ci-quarterly` |

The signal log is the **operational output** of this skill — push every signal of score ≥10 (24h alert threshold). Signals scoring 5–9 stay local in the log; <5 are dropped.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:competitive-intelligence:v2.0.0"`

### Example push (high-score signal — alert threshold)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Guru",
    "tags": "#ci-signal #competitor:guru #category:pricing #ci-score:18",
    "relevance": "2026-05-02 — Guru added new pricing tier ($30/user Enterprise) detected via Visualping on getguru.com/pricing. Strength: 5 (priced action). Decision-relevance: 4 (changes our wedge against them at mid-market). Total: 20. Action: refresh battle card pricing column; flag to AE team for active deals.",
    "source": "skill:competitive-intelligence:v2.0.0"
  }'
```

### Example push (medium signal — log only, no alert)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Stonly",
    "tags": "#ci-signal #competitor:stonly #category:hiring #ci-score:9",
    "relevance": "2026-05-02 — Stonly posted Senior PMM for Support Vertical on LinkedIn. Strength: 3 (intent signal). Decision-relevance: 3 (positioning shift watch). Total: 9. Action: log; revisit in 30d.",
    "source": "skill:competitive-intelligence:v2.0.0"
  }'
```

### Routing rule (special)

When a signal scores ≥21 (strategic event — e.g., competitor acquired, raised $50M+, killed a product line), push to CRM **and** trigger the `competitor-analysis` skill to re-run on that competitor. Set `tags: "#ci-strategic-event #re-run-needed"` so downstream skills can detect.

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #competitive-intelligence`. **Critical for this skill** — signal-log entries are the input that triggers downstream strategic moves (battle-card refreshes, repositioning, deal-team alerts). Fabricated entries here cascade into wrong actions. Always default ungrounded signals to this routing. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

The `#unverified #review-required` scaffold is in this skill file now; the dashboard review-queue surfacing is a follow-up agentic-app task. Until the dashboard is built, the tag at least keeps fabricated signals out of the alert routing pipeline (which would otherwise trigger Slack DMs to founders for events that didn't happen).

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #competitive-intelligence #competitor:guru",
    "relevance": "Signal: Guru launched AI authoring product Q1 2026 [unverified — needs check] — no Wayback URL or press citation captured. Pricing change 12% [unverified — needs check] — no Vendr/changelog source. Leadership hire (new VP Product) [unverified — needs check] — no LinkedIn URL. Hold all three before scoring or routing to alert pipeline.",
    "source": "skill:competitive-intelligence:v2.0.0"
  }'
```

### When NOT to push

- Signal score <10 (stays in local log only — pushing low-signal entries floods the CRM).
- Sentiment-only signals without a named action (per Heuristics: "sentiment shifts are lagging").
