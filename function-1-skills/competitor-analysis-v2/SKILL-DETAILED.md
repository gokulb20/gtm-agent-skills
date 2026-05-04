---
name: competitor-analysis
description: Map a competitive landscape by tiering competitors, profiling each on positioning/pricing/strengths/weaknesses, applying Helmer's 7 Powers and segment-ownership analysis, and producing usable battle cards. Use when the user needs head-to-head competitive maps, battle cards for sales enablement, structural moat analysis, alternative-to positioning research, or pre-launch competitive landscape grounding.
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

Turn a list of names into a structured competitive view that GTM, product, and sales can act on. Produces tiered competitor profiles, head-to-head differentiation, structural moat assessment, and battle cards that hold up in real sales conversations. Goal: decision-grade competitive clarity, not encyclopedic completeness.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Competitor Analysis turns a list of names into a structured competitive view that GTM, product, and sales can act on. It produces tiered competitor profiles, head-to-head differentiation, structural moat assessment, and battle cards that hold up in real sales conversations.

The goal is not encyclopedic completeness — it is **decision-grade competitive clarity**: which competitors matter, how they actually win and lose, where the user has durable advantage, and which competitors should be ignored.

## When to Use

Trigger this skill when the user requests:
- Competitor mapping ("Who are our competitors?", "Map the landscape")
- Head-to-head comparison ("How do we stack against X?")
- Battle cards for sales ("Build a battle card for [competitor]")
- Moat analysis ("What's our defensibility?")
- "Alternative to" positioning research
- Pre-launch competitive landscape
- Loss-reason investigation ("Why are we losing to X?")
- Pricing benchmark research

**Do NOT use this skill when:**
- The user wants ongoing monitoring → use `competitive-intelligence`
- The user wants their own positioning rewritten → use `positioning-strategy`
- The user wants market sizing → use `market-research`
- The user is asking for FUD or unverified competitor claims — refuse and redirect to evidence-based analysis

## Inputs Required

### Parameterized inputs

| Field | Profile path | Required |
|---|---|---|
| Product description | `{{profile.product.description}}` | Yes |
| Category | `{{profile.market.category}}` | Yes |
| Target segments | `{{profile.market.segments}}` | Yes |
| Geography | `{{profile.market.geography}}` | Yes |
| Known competitors | `{{profile.competitors.named}}` | Optional |
| **Lost deals (real alternatives chosen by buyer)** | `{{profile.customers.lost_deals}}` | **Optional but ASK FOR FIRST** — per Dunford, real alternatives come from real buyers. Loss data is the highest-fidelity source. |
| **Won deals (what buyer was about to use)** | `{{profile.customers.won_deals}}` | **Optional but ASK FOR FIRST** — same source of truth principle |
| Pricing | `{{profile.product.pricing_model}}` | Yes |

### Fallback intake flow

If the customer profile is missing or sparse, collect conversationally:

> To map your competition, I need:
>
> 1. **Your product** — one paragraph: what it does, for whom, the outcome.
> 2. **Category** — what market are you competing in? (e.g., "AI sales agents", "marketing automation for B2B SaaS")
> 3. **Target segments** — who you're selling to (firmographic + role).
> 4. **Geography** — where you compete.
> 5. **Pricing** — your model and ACV range.
>
> **Highest-leverage — ask first:**
> 6. **Last 5 losses** — who beat you and why. Specifically: was it a named product, a person they hired, a tool they already had, or did they keep doing it manually? *(This is the most valuable data point. Per Dunford, real alternatives come from real buyers — not industry databases.)*
> 7. **Last 5 wins** — who/what they were about to use if they hadn't bought from us.
>
> **Also helpful:**
> 8. **Competitors you already know about** — name 3–10. Don't filter; include "weird" ones.

**Critical:** if won/lost deals don't exist, flag and recommend running `competitive-intelligence` first or a 5-conversation win/loss interview loop. Proceeding without buyer input caps the analysis at Medium confidence — the alternatives list will be desk-research-grade, not buyer-validated.

### Input validation rules

- If `competitors.named` is empty AND no segments given → push back: "I need either competitors you've encountered OR a segment to research. Otherwise the search is unbounded."
- If `category` is internal-jargon (e.g., "intelligent customer engagement platform") → ask: "What category do buyers use to describe this? What do they Google?"
- If user lists >20 competitors → push back: "20+ is too many. The skill works best with a tiered set. Let me classify what you have first."
- If user describes a competitor as "we have no real competitors" → flag it: "Every product has substitutes. Status quo / spreadsheets / DIY count. Let's identify them."

---

## Frameworks Used

### 1. Competitor Tiering (4 categories)

Not every competitor matters equally. Classify before profiling.

| Tier | Definition | Signal |
|---|---|---|
| **Direct** | Same product, same buyer, same job | Buyers actively compare; appears in 3+ deals |
| **Indirect** | Different product, same buyer, same job | Buyer considers as alternative path to outcome |
| **Substitute** | **Anything the buyer would do if your product didn't exist** — includes DIY, manual processes, existing tools, hiring a person, doing nothing, or shifting budget elsewhere (per Dunford's *Obviously Awesome* competitive-alternatives lens) | "We just use spreadsheets", "hire a freelancer", "keep ignoring it", "spend the budget on sales hiring instead" |
| **Aspirational** | Adjacent, larger, or future competitor | Could enter the market; inspires buyer expectations |

**Rule:** if tiering is unclear, default to Direct + Substitute first. Indirect and Aspirational are advanced; don't waste cycles if Direct list isn't solid.

**Substitute is load-bearing for downstream positioning.** `positioning-strategy` consumes the Substitute tier directly as Dunford-style "competitive alternatives" — the framing the buyer uses when comparing options. A weak Substitute list (only DIY, missing the hire/do-nothing/shift-budget cases) produces weak positioning. Force completeness across all 4 substitute categories below in Procedure Step 1.

### 2. Hamilton Helmer's 7 Powers (Moat Framework)

From *7 Powers* (Helmer, 2016). The only durable competitive advantage comes from one or more of these 7 structural sources. A real Power requires both a **benefit** (e.g., lower cost, higher willingness-to-pay) AND a **barrier** (something the competitor cannot easily copy):

| Power | What it is | How to detect it |
|---|---|---|
| **Scale Economies** | Cost per unit declines with size | Larger competitor has lower cost-to-serve |
| **Network Economies** | Value increases with users | Marketplace / two-sided / community-driven |
| **Counter-Positioning** | New approach incumbents can't copy without cannibalizing | Incumbent locked in by their existing model (e.g., agency vs. SaaS) |
| **Switching Costs** | Cost to leave > cost to stay | Data lock-in, workflow embedment, retraining cost |
| **Branding** | Buyers pay premium for the name | Premium pricing sustained without feature lead |
| **Cornered Resource** | Unique input access | Exclusive data, key people, IP, partnerships |
| **Process Power** | Embedded operational know-how | Quality/speed gap that takes years to replicate |

**Apply to:** top 3 competitors AND the user's own product. The output is the moat assessment for each.

**Decision rule:** if the user has zero of the 7 powers, they don't have a moat — they have a head start. Say so explicitly.

### 3. Porter's 5 Forces (light application)

Use Porter's framework as a sanity check on the broader competitive structure, not as a primary tool:

- **Rivalry intensity** — how aggressive is direct competition? (price wars, feature wars, marketing spend)
- **Buyer power** — can buyers easily switch or extract concessions?
- **Supplier power** — are critical inputs concentrated? (cloud, data, talent)
- **Threat of new entrants** — how low are barriers? (capital, distribution, regulatory)
- **Substitutes** — what's the realistic alternative if the category disappeared?

Output: 1 paragraph diagnostic, not a full report.

### 4. Segment-Ownership Matrix

For each named segment from market-research, identify which competitor "owns" it (default choice). Format:

| Segment | Owner | Runner-up | User position | Rationale |
|---|---|---|---|---|
| [name] | [comp] | [comp] | [Leader/Challenger/Niche/Absent] | [why] |

This drives positioning and ICP focus downstream.

### 5. Win/Loss Pattern Analysis (when data exists)

If the user has won/lost deal data, extract:

**Win patterns:** when we win against X, the buyer typically had [trait], and the deciding factor was [factor].

**Loss patterns:** when we lose to X, the buyer typically had [trait], and the deciding factor was [factor].

**Disqualifier patterns:** deals where we should not have engaged (anti-ICP signals).

Goal: 3–5 patterns per pattern type. Less is more — patterns must be repeatable.

### 6. Battle Card Format

A battle card is a 1-pager a rep can use mid-call. Standard sections:

1. **One-line positioning** — how the competitor describes themselves
2. **Their best customer** — who buys from them and why
3. **Where they win** — segments and use cases they own
4. **Where they lose** — gaps, weak segments, common churn reasons
5. **Their attack on us** — what they say about us; how to counter
6. **Our attack on them** — our wedge; the question that flips the deal
7. **Pricing** — model, ACV, recent changes
8. **Recent moves** — last 90 days; what to watch

Format influenced by April Dunford's *Obviously Awesome* + Klue/Crayon battle-card patterns + Chris Orlob's wedge/counter/flip discovery framing.

---

## Tools and Sources

### Discovery (find competitors you don't know about yet)

| Source | What it finds | Cost | Notes |
|---|---|---|---|
| **G2 / Capterra / TrustRadius** | Direct + indirect within your category | Free | Start here. Read 50+ reviews per competitor. |
| **Crunchbase / PitchBook** | Funded competitors, recent rounds, M&A | Freemium / Paid | Capital flow signals momentum |
| **Reddit / Hacker News / community Slacks** | What buyers ACTUALLY use (often differs from G2) | Free | Search "[your category] alternatives" + "[competitor] vs" |
| **YC / Techstars / accelerator batches** | Emerging competitors before they appear in databases | Free | Last 4 batches relevant for early-stage |
| **LinkedIn search: "VP of [your buyer role]" posts** | What buyers are talking about | Free | Read 20+ posts |
| **Google: "[category] alternatives", "vs", "instead of"** | Comparison pages, third-party reviews | Free | Underused; high signal |

### Profiling (deep on each competitor)

| Source | What it finds | Cost |
|---|---|---|
| **Competitor's website** | Positioning, ICP, pricing, claims | Free |
| **Wayback Machine** | Positioning evolution, pricing changes over time | Free |
| **G2 reviews (sorted by recent)** | Real strengths, weaknesses, churn reasons | Free |
| **Glassdoor reviews** | Internal culture, sales motion, churn signals | Free |
| **LinkedIn: company page + leadership posts** | Hiring, strategy, moves | Free |
| **YouTube demos / webinars** | How they actually demo; their case studies | Free |
| **G2 Crowd PDF reports** | Side-by-side comparisons | Paid |
| **Klue / Crayon** | Battle card platforms with auto-tracking | Paid |

### Pricing (often hidden, must triangulate)

| Source | What it finds |
|---|---|
| **Competitor pricing page** | Public list price (often misleading at the top) |
| **Vendr / Tropic public benchmarks** | Real negotiated ACVs for SaaS |
| **G2 / Reddit threads** | Customer-reported actual prices |
| **LinkedIn AE posts** | Sometimes reveal deal sizes |
| **Internal sales (the user's reps)** | Best source — what buyers tell you the other quote was |

### Recent moves and signals

| Source | What it finds |
|---|---|
| **Visualping** | Tracks website changes (pricing, positioning, headlines) |
| **Wayback Machine** | Historical comparison |
| **Their LinkedIn company page (Posts tab)** | Product launches, hires, customer stories |
| **Their changelog / release notes** | Velocity, focus areas |
| **Crunchbase News / PitchBook** | Funding, M&A, exec changes |
| **Their job postings** | Where they're investing (engineering, GTM, geography) |

**Source-priority rule:** internal win/loss data > customer interviews > G2/community reviews > competitor's own materials > analyst reports.

### Tools that automate this (worth knowing about)

- **Klue, Crayon, Kompyte** — competitive intelligence platforms (paid, $$$)
- **Visualping, Wachete** — website change monitoring (cheap)
- **Owler** — basic competitor news aggregation (freemium)

For most early-stage GTM, manual + Visualping is enough.

---

## Procedure

### Step 1: Build the candidate list — buyer-validated first, then desk research

**Step 1a — Pull buyer input first (this is the source of truth).** Per Dunford, real alternatives come from real buyers, not industry databases. Ask the user upfront:
- "In the deals we lost, what did the buyer choose instead? Specifically — was it a named product, a person they hired, a tool they already had, or did they just keep doing it manually?"
- "In the deals we won, what were they about to use if they hadn't bought from us?"
- "When budget conversations happen, what other line items does this product compete against?"

If the user has no win/loss data and no buyer interviews to draw from, **flag and recommend** running `competitive-intelligence` first (for ongoing detection) or a 5-conversation win/loss interview loop before continuing full profiling. Mark confidence Medium for the rest of the analysis if proceeding without buyer input.

**Step 1b — Then cast wide via desk research:**
- Add anything from G2/Capterra in the same category
- Add anything Reddit/HN mentions in "X alternatives" threads
- Add 1–2 aspirational competitors (adjacent or larger)

**Step 1c — Force completeness across all 4 Substitute categories** (Dunford's competitive-alternatives lens). The agent must produce ≥1 entry for each:

| Substitute category | Examples |
|---|---|
| **DIY / manual** | Spreadsheets, email, internal tools, notebook, custom internal scripts |
| **Hire a person** | Outsourced agency, FTE, consultant, intern, virtual assistant |
| **Do nothing / accept the problem** | Status quo, low priority, "we'll deal with it later", ignore |
| **Shift budget elsewhere** | "We'd spend that $X on a sales hire / paid ads / a different tool category" |

The "shift budget elsewhere" category is the most-missed alternative — it's what budget actually competes against in B2B, and surfaces the *opportunity cost* the buyer is weighing.

Goal: 15–25 candidates raw across Direct + Indirect + Substitute + Aspirational tiers.

### Step 2: Tier the candidates

Apply the 4-tier framework. Output:
- 3–6 Direct
- 2–4 Indirect
- 2–4 Substitute
- 1–2 Aspirational

If Direct list is <3, dig deeper before profiling — likely missing competitors. If Direct is >6, score and trim to top 5.

### Step 3: Profile the Direct + Substitute tiers

For each, fill the per-competitor profile (template below). Skip or shorten Indirect and Aspirational unless user requests.

**Required minimum data per competitor:**
- One-line positioning (their words, from their site)
- Best-fit customer (size, segment, use case)
- 3 strengths (evidenced)
- 3 weaknesses (evidenced — G2 reviews are gold)
- Pricing (range + model)
- 1 recent move (<90 days)

**No fabrication.** If data is unavailable, write "Insufficient data — [what's needed]".

### Step 4: Build the head-to-head matrix

Across top 5 competitors + user's product, score:
- Positioning clarity
- Best-fit ICP
- Pricing tier (low / mid / premium)
- Sales motion (PLG / sales-led / hybrid)
- 3–5 capability dimensions specific to the category

Output: a single comparison table.

### Step 5: Apply Helmer's 7 Powers

For each top-3 competitor AND the user's product, identify which (if any) of the 7 Powers applies, with evidence (benefit + barrier).

Be honest: most early-stage products have 0–1 powers. That's not failure; it's information. Powers come from operating, not pitching.

### Step 6: Map segment ownership

Use segments from market-research (or define light segments here if missing). For each segment, identify owner, runner-up, user position. Surface gaps.

### Step 7: Apply Porter's 5 Forces (1 paragraph)

Sanity-check structural attractiveness. Is this a category worth competing in long-term, or is structural rivalry / buyer power going to crush margins?

### Step 8: Win/loss pattern analysis (if data exists)

Synthesize patterns from won/lost deals. 3–5 patterns each. Tag each pattern with confidence based on sample size.

### Step 9: Generate battle cards

For top-3 Direct competitors, produce a battle card using the format above. These should be paste-ready into a CRM or sales playbook.

### Step 10: Strategic implications

Synthesize 3–5 implications. Each implication has: observation → so what → recommended action.

### Step 11: Route downstream

Recommend next skill based on findings.

---

## Output Template

---

### Competitive Landscape: [Product Name]

**Prepared:** [date]
**Category:** [scope]
**Geography:** [scope]
**Confidence overall:** [H/M/L]

---

**1. Tiered Competitor List**

| Tier | Competitors |
|---|---|
| Direct | [list] |
| Indirect | [list] |
| Substitute | [list] |
| Aspirational | [list] |

**2. Per-Competitor Profile** (repeat for each Direct + Substitute)

```
Name: [competitor]
Tier: [Direct/Indirect/Substitute/Aspirational]
One-line positioning: [their words]
Best-fit customer: [segment + size + use case]
Pricing: [model + range, with confidence]
Strengths (evidenced):
  - [point + source]
Weaknesses (evidenced):
  - [point + source]
Recent moves (<90 days):
  - [event + date]
Threat level to user: [H/M/L]
```

**3. Head-to-Head Matrix**

| Dimension | Comp A | Comp B | Comp C | Comp D | Comp E | User |
|---|---|---|---|---|---|---|
| Positioning | | | | | | |
| Best-fit ICP | | | | | | |
| Pricing tier | | | | | | |
| Sales motion | | | | | | |
| [Capability 1] | | | | | | |
| [Capability 2] | | | | | | |
| [Capability 3] | | | | | | |

**4. Moat Analysis (Helmer's 7 Powers)**

| Competitor / User | Powers held | Evidence (benefit + barrier) | Durability |
|---|---|---|---|
| [name] | [list] | [evidence] | [years] |

**5. Segment Ownership Map**

| Segment | Owner | Runner-up | User position | Rationale |
|---|---|---|---|---|

**6. Porter's 5 Forces Diagnostic**

[1 paragraph: rivalry, buyer power, supplier power, new entrants, substitutes — with verdict on category attractiveness]

**7. Win/Loss Patterns** (if data exists)

```
Win pattern 1: When buyer is [trait], we beat [competitor] because [factor]. n=[#]
Win pattern 2: ...
Loss pattern 1: When buyer is [trait], we lose to [competitor] because [factor]. n=[#]
Loss pattern 2: ...
Disqualifier: We should not engage when [trait]. n=[#]
```

**8. Battle Cards (top 3 Direct)** — see Battle Card template below

**9. Strategic Implications**

| Observation | So What | Recommended Action |
|---|---|---|
| | | |

**10. Recommended Next Step**

[Named follow-on skill + 1-sentence rationale]

---

### Battle Card Template (used in section 8)

```
=== BATTLE CARD: [Competitor Name] ===

THEIR PITCH (one line):
[How they describe themselves, in their words]

THEIR BEST CUSTOMER:
- Segment: [size, industry, geo]
- Use case: [primary]
- Why they buy: [in customer language]

WHERE THEY WIN:
- [segment/use case 1]
- [segment/use case 2]

WHERE THEY LOSE:
- [weakness 1, evidenced]
- [weakness 2, evidenced]

THEIR ATTACK ON US:
- They will say: "[expected attack]"
- Counter: "[our response]"
- Question to flip the deal: "[discovery question]"

OUR ATTACK ON THEM:
- Our wedge: [single sentence]
- Discovery question: "[question that surfaces their weakness]"
- Proof: [case study / data point]

PRICING:
- Model: [seat/usage/flat]
- Public list: [$X]
- Real ACV (if known): [$Y, source]
- Recent changes: [if any]

RECENT MOVES (<90 days):
- [event + date + implication]

WATCH LIST (next 90 days):
- [thing to monitor]
```

---

## Worked Example

> *The example below uses **WorkflowDoc**, a fictional AI-native runbook authoring tool for B2B SaaS support teams. The fictional product is shared across all six function-1 skills so the worked examples interlock. The frameworks below apply to any B2B GTM context.*

**Input (fallback intake):**

> Product: WorkflowDoc `[hypothetical]` — AI-native runbook authoring for B2B SaaS support teams.
> Category: AI-powered support knowledge management
> Segments: Series B SaaS (100–300 emp) primary; Series C/D secondary
> Geography: US
> Pricing: $400/seat/year `[hypothetical]`; 8–15 seats typical; ACV $3.2k–$6k `[hypothetical]`
> Known competitors: Guru `[hypothetical]`, Stonly `[hypothetical]`, Document360 `[hypothetical]`
> Won deals: 4 paid pilots `[hypothetical]`, beat Guru in 3, Stonly in 1
> Lost deals: 2 lost `[hypothetical]` (1 to Notion `[hypothetical]`, 1 to "we'll DIY in Confluence" `[hypothetical]`)

### Output:

> **Provenance note for the agent reading this example:** every named entity below (competitors, customer counts, pricing figures, funding rounds, dates, G2 review counts, recent moves) is `[hypothetical]` — i.e., fictional content for illustration. **This skill is the highest-fabrication-risk skill in the repo** because battle-card outputs go directly into live sales conversations. In real user output, the agent must apply the per-entity tagging discipline using `[user-provided]` / `[verified: <source-or-url>]` / `[unverified — needs check]` as appropriate (see `## Guardrails` provenance rule). A battle card with fabricated competitor pricing or customer counts will lose deals when the buyer fact-checks.

---

### Competitive Landscape: WorkflowDoc

**Prepared:** 2026-04-30
**Category:** AI-powered support knowledge management
**Geography:** US
**Confidence overall:** Medium-High (good internal data; small sample)

---

**1. Tiered Competitor List**

| Tier | Competitors |
|---|---|
| Direct | Guru, Stonly, Document360, Stack Overflow for Teams |
| Indirect | Notion, Confluence, Slab, Slite |
| Substitute | Internal Notion + Slack channels (status quo); Outsourced VA + Google Docs |
| Aspirational | Glean (enterprise AI search), Intercom (if they bundle internal KB) |

**2. Per-Competitor Profile (top 3 Direct)** `[all entities, prices, dates, customer counts in this section are hypothetical]`

```
Name: Guru [hypothetical]
Tier: Direct
One-line positioning: "Verified company knowledge that surfaces where work happens" [hypothetical]
Best-fit customer: 200–2000 emp companies, sales/support teams, $50k+ ACV [hypothetical]
Pricing: $15/user/month Builder, $24 Enterprise. Real ACV typically $25k–$80k. [hypothetical]
Strengths:
  - Strong browser extension and Slack/Salesforce integrations (G2 #1 in this dim)
  - "Verification" workflow drives trust (cited in 60%+ G2 reviews)
  - Established brand in mid-market
Weaknesses:
  - AI authoring is bolt-on (added 2024); buyers report it feels added-on, not native (G2 reviews 2024–2025)
  - Pricing climbs fast at scale; SMB churn cited
  - Setup is heavy — multi-week implementation (Reddit/G2)
Recent moves:
  - Raised $30M Series C, Sept 2025
  - New AI-native authoring product line announced Q1 2026 — direct response to entrants like us
Threat level: High — they will move down-market with AI features

Name: Stonly
Tier: Direct
One-line positioning: "Interactive guides and decision trees for support and onboarding"
Best-fit customer: Support and onboarding teams, mid-market, $20k+ ACV
Pricing: $99/mo starter, $499/mo team, custom enterprise. Real ACV $15k–$40k.
Strengths:
  - Decision-tree authoring is best-in-class
  - Strong customer-facing AND internal use cases
  - $22M Series A (2024) signals momentum
Weaknesses:
  - Decision trees != runbook (different shape; some buyers want prose, not flowcharts)
  - Support-team-first messaging is recent; older customers were primarily onboarding teams
  - AI features are reactive, not generative-first
Recent moves:
  - Pricing simplification April 2026 (Wayback Machine)
  - Hiring AI/ML engineers (LinkedIn) — moving in our direction
Threat level: Medium-High

Name: Notion
Tier: Indirect (but appears in deal cycles)
One-line positioning: "All-in-one workspace"
Best-fit customer: Everyone (this is the problem)
Pricing: $10/user/mo Plus, $20 Business. ACV $2k–$50k+.
Strengths:
  - Brand
  - Already deployed at most target buyers (we won 0 deals where Notion was already the wiki)
  - Cheap
Weaknesses:
  - Generic — no support-team-specific features
  - AI features are search/summarize, not domain-specific runbook authoring
  - Getting structure right is a recurring user complaint
Recent moves:
  - Notion AI usage pricing rolled out 2024 — ongoing
  - No specific support-team features in roadmap (per public roadmap and recent posts)
Threat level: Medium — they won't build for support teams specifically; they win on "good enough + already here"
```

**3. Head-to-Head Matrix**

| Dimension | Guru | Stonly | Document360 | Notion | WorkflowDoc |
|---|---|---|---|---|---|
| Positioning | Verified knowledge | Interactive guides | Knowledge base software | All-in-one workspace | AI-native support runbooks |
| Best-fit ICP | Mid-market sales+support | Support+onboarding | Tech docs / KB | Generalist | Support, Series B-D SaaS |
| Pricing tier | Premium ($25k–80k) | Premium ($15k–40k) | Mid ($5k–25k) | Low ($2k–10k base) | Mid ($3k–6k) |
| Sales motion | Sales-led | Sales-led | PLG → SLG | PLG | PLG → SLG |
| AI authoring | Bolt-on (2024) | Reactive | Limited | Generic AI | Native (core) |
| Support-team focus | Partial | Yes (recent) | No | No | Yes (core) |
| Time to value | Weeks | Days-weeks | Days | Hours | Days (target) |

**4. Moat Analysis (Helmer's 7 Powers)**

| Player | Powers held | Evidence (benefit + barrier) | Durability |
|---|---|---|---|
| Guru | Switching Costs (medium), Branding (medium) | Verified-content workflow embedded in CS workflow; mid-market brand recognition | 3–5 yrs |
| Stonly | Process Power (low), Switching Costs (low) | Decision-tree IP took years to build; switching cost is moderate | 2–3 yrs |
| Notion | Branding (high), Switching Costs (medium), Network (low-medium) | Brand is strongest in category; "everyone uses Notion" effect | 5+ yrs |
| WorkflowDoc | None yet (early) | Counter-positioning candidate (AI-native vs. bolt-on) but unproven | <1 yr — head start, not moat |

Honest read: WorkflowDoc has a 12–18 month head start on AI-native authoring. That's not a moat. The path to a real Power: build Switching Costs via deep ticketing-system integrations (workflow embedment) AND Cornered Resource via proprietary runbook patterns from customer ticket data.

**5. Segment Ownership Map**

| Segment | Owner | Runner-up | User position | Rationale |
|---|---|---|---|---|
| Series B SaaS, support team 5–15 people | (No clear owner) | Guru | **Absent → strong opportunity** | Guru is overpriced for this segment; Notion is generic; gap exists |
| Series C/D SaaS, support team 15–50 | Guru | Stonly | Challenger | Possible to challenge with AI-native angle; long sales cycle |
| Series A SaaS, support team 2–5 | Notion (status quo) | Document360 | Niche | Too small to support sales motion |
| Enterprise (500+ emp) | Guru | Glean (emerging) | Absent | Defer — enterprise sales not yet built |

**6. Porter's 5 Forces Diagnostic**

Rivalry intensity is **rising** — Guru and Stonly are both moving toward AI-native, signaling the AI-first wedge has a 12–18 month window before incumbents catch up. Buyer power is **high** for buyers (low switching costs from Notion; many alternatives) but lowers once a runbook system is deployed. Supplier power is **moderate** (LLM costs are commoditizing, but quality leaders still concentrated). New-entrant threat is **high** — barriers are low (LLM + UI). Substitutes are **strong** — DIY Notion + Slack accounts for ~30% of "lost" deals. **Verdict:** category is structurally crowded but the support-team-specific niche is currently underserved. Window is real but narrow.

**7. Win/Loss Patterns**

```
Win pattern 1: When buyer is "Series B, 100–250 employees, support team 5–15, frustrated with Notion structure"
                we beat Guru/Stonly because price is ~3x lower and AI-authoring saves 10+ hrs/week. n=3
Win pattern 2: When buyer has internal champion who is "VP of Support" (not CTO/Eng)
                we win by speaking support language and not requiring eng resources. n=3 of 4 wins

Loss pattern 1: When buyer already has Notion deployed company-wide
                we lose because "good enough + already paid for" beats "better but new tool." n=1, but consistent with Reddit/G2 patterns
Loss pattern 2: When evaluation is led by IT/Procurement (not Support)
                we lose to Confluence/Notion (incumbents). n=1, low confidence

Disqualifier: Companies <50 emp with support team of 1–2 — ACV too low, won't pay $400/seat. n=multiple early conversations
```

**8. Battle Cards (top 3 Direct)** — full cards in `evals/battle-cards/` (not bundled here for brevity)

Sample (Guru):

```
=== BATTLE CARD: Guru ===

THEIR PITCH:
"Verified company knowledge that surfaces where work happens"

THEIR BEST CUSTOMER:
- Segment: 200–2000 employee SaaS, sales+support combined
- Use case: Sales enablement primarily; support secondary
- Why they buy: Verified workflow + Slack/Salesforce integrations + brand trust

WHERE THEY WIN:
- Combined sales+support knowledge bases
- Mid-market companies with budget for $25k+ tools
- Buyers who prioritize integration depth over AI-authoring speed

WHERE THEY LOSE:
- Support-only teams (don't need sales features they pay for)
- Sub-$15k ACV deals (their pricing breaks)
- Buyers wanting AI-native authoring (their AI is bolt-on, 2024 add)

THEIR ATTACK ON US:
- "We have AI features too, plus 8 years of enterprise trust."
- Counter: "Their AI was added in 2024 onto a 2017 architecture. Watch their demo — authoring is still manual-first. Ours was built AI-first." (Show side-by-side authoring demo.)
- Flip question: "Can you show me a runbook your AE drafted from a real ticket in under 5 minutes?"

OUR ATTACK ON THEM:
- Wedge: "Built for support teams, AI-first, at 1/3 the price."
- Discovery question: "How long does it currently take your team to write or update a runbook? What % of your current Guru content is out of date?"
- Proof: 4 customer references; case study showing 8x faster authoring

PRICING:
- Model: Per-seat
- Public list: $15-$24/user/month
- Real ACV: $25k–$80k
- Recent: Raised pricing 12% in Q4 2025

RECENT MOVES (<90 days):
- Raised $30M Series C (Sept 2025)
- AI authoring product line announced Q1 2026 — direct response

WATCH LIST:
- AI authoring product launch — when, what features, pricing
- Mid-market discount programs (sign of moving down-market)
- New leadership hires
```

**9. Strategic Implications**

| Observation | So What | Action |
|---|---|---|
| Guru is moving to AI-native in 6–12 months | Window to establish AI-native brand is closing | Push GTM aggressively in next 2 quarters; lock in 30+ customer references |
| 0 of 4 wins where Notion was company-wide deployed | Notion-deployed accounts are anti-ICP | Add "no existing wiki widely deployed" to ICP scoring |
| All 4 wins had VP of Support as champion | Champion role is well-defined | Build outbound around VP of Support specifically; deprioritize CTO outreach |
| Stonly hiring AI/ML engineers | Window narrowing on AI-authoring differentiation | 90-day differentiation review; keep watch on Stonly AI launch |
| No moat held yet | Head start can disappear in 12–18 months | Invest in switching-cost-creating integrations (Zendesk, Intercom, Salesforce Service Cloud) |

**10. Recommended Next Step**

→ `positioning-strategy`. With segment ownership clarified (Series B underserved) and competitor weaknesses identified, the next move is to lock positioning against Guru specifically, then sequence to `icp-definition` to refine the buyer profile.

---

## Heuristics

- **Tier before profile.** A Direct list of 3 well-profiled competitors beats 15 superficial ones.
- **Loss data > everything.** One real loss reason from a customer beats 10 G2 reviews.
- **Believe G2 negative reviews more than positive ones.** Negative reviews are usually specific; positive reviews are usually paid or vague.
- **Pricing pages lie.** Real ACVs come from internal sales conversations or Vendr-style benchmarks.
- **Most early-stage products have 0 of the 7 Powers.** Saying so is honest; making one up is malpractice.
- **The status quo is a competitor.** Spreadsheets, Notion, "we just do it manually" — these win more deals than any named competitor in many categories.
- **The most dangerous competitor is the one you haven't heard of.** Spend 30% of research time on discovery, not profiling known names.
- **Battle cards die in drawers if reps don't help build them.** Have at least one rep co-author each.
- **A weakness without evidence is FUD.** Every weakness needs a citation: G2 review, customer quote, competitor's own materials.

## Edge Cases

### Competitor is in stealth or pre-launch
- Use LinkedIn (founder's profile + posts), job postings, domain DNS, beta tester reports.
- Tag confidence as Low.
- Re-run when public.

### Competitor is much larger and more diversified
- Profile only the relevant product line; ignore the parent company's other products.
- Note resource-asymmetry as a separate risk in Strategic Implications.

### "We have no real competitors"
- Refuse the framing. Identify 5+ substitutes (status quo, manual processes, adjacent products).
- This claim usually means: (a) market doesn't exist yet, (b) user hasn't done buyer research, or (c) user is being defensive.

### Foreign-language competitors (when user is global)
- Note language barrier in profile.
- Use machine translation for positioning + reviews.
- Confidence cap: Medium (translation can miss nuance).

### Open-source competitors
- Profile differently: focus on adoption signals (GitHub stars, contributors, downloads), commercial offering (if any), community sentiment.
- Pricing analysis becomes "free + paid hosted vs. self-hosted" tradeoff.

### Competitor pivots mid-analysis
- Note pivot date. Re-run profile.
- This often signals category instability — flag in Porter's diagnostic.

### Conflicting data on the same competitor
- Surface both. Don't average.
- Default to internal sales data > customer quotes > G2 > competitor's own materials.

## Failure Modes and Recovery

| Failure mode | Symptom | Recovery |
|---|---|---|
| Direct list <3 | Either novel category or insufficient research | Run another discovery pass: G2 alternatives pages, Reddit threads, accelerator batches |
| Direct list >10 | User overcounts; many are actually Indirect/Substitute | Re-tier; trim to top 5 Direct. Move others. |
| User insists "no competitors" | Defensive or naive framing | Force substitute analysis. Status quo / DIY / spreadsheets always exist. |
| Pricing entirely opaque | Competitor hides ACVs | Triangulate from Vendr, Reddit, internal sales. Tag all pricing data with source + confidence. |
| Win/loss data missing | New product, no deals yet | Skip Section 7. Replace with hypothesis section: "We expect to win when X, lose when Y. Validate after first 10 deals." |
| User has emotional bias against a competitor | Over-criticizes weaknesses; ignores strengths | Force evidence rule: every claim cites a source. Strip non-cited claims. |
| User wants FUD in battle card | Asks for unverified attacks | Refuse. Battle cards built on FUD lose deals when reps over-attack. Replace with evidenced wedge. |

## Pitfalls

- **Feature comparison theater.** Long feature checkboxes lose to "what job does the buyer hire each tool for."
- **Mistaking a pivot for a permanent position.** Competitors change positioning yearly — date your snapshots.
- **Over-weighting analyst rankings.** Magic Quadrant placement is slow and political; use as one signal, not truth.
- **Building battle cards reps won't use.** Reps want: 1 wedge, 1 question, 1 proof. Not 5 pages of feature trivia.
- **Forgetting the buyer journey changes who matters.** Direct competitors at evaluation stage may differ from substitutes at "do nothing" stage. Map per stage if relevant.
- **Confusing "they don't do X" with weakness.** The competitor may not do X because their buyer doesn't want X. Validate weakness with buyer evidence.
- **Skipping substitutes.** "We do nothing" is the most-chosen path in many B2B categories. Profile it.

## Verification

1. The user can name their top 3 Direct competitors and the wedge against each.
2. Every claim about a competitor weakness has a source.
3. Battle cards fit on 1 page and have 1 wedge per competitor.
4. Helmer 7 Powers analysis is honest — no manufactured moats.
5. Segment ownership map is filled and identifies at least one whitespace.
6. Win/loss patterns (if data exists) are 3–5, not 15.
7. Strategic implications drive at least 3 actions, not just observations.

## Done Criteria

1. Tiered competitor list (3–6 Direct, 2–4 Indirect, 2–4 Substitute, 1–2 Aspirational).
2. Per-competitor profiles for all Direct + Substitute (positioning / best-fit customer / strengths / weaknesses / pricing / recent moves).
3. Head-to-head matrix across top 5 + user.
4. Helmer 7 Powers analysis for top-3 + user (each Power has benefit + barrier evidence).
5. Segment ownership map with user position per segment.
6. Porter's 5 Forces 1-paragraph diagnostic.
7. Win/loss patterns: 3–5 win + 3–5 loss + 1+ disqualifier (or hypothesis section if no data).
8. Battle cards (top 3 Direct) on 1 page each.
9. Strategic implications: 3–5 with observation → so-what → action.

## Eval Cases

**Eval 1 — Crowded category, well-known competitors:**
*Input:* CRM software for SMB law firms, US, $150–400/user/month, competitors named: Clio, MyCase, PracticePanther
*Expected output:* Tiered list with at least 4 Direct + 2 Substitutes (manual + spreadsheets), full battle cards for top 3, segment ownership clear, win/loss patterns inferred from G2.

**Eval 2 — Emerging category, sparse competitors:**
*Input:* AI agent orchestration for non-technical founders, global English, ACV unclear
*Expected output:* Direct list dominated by stealth/early-stage (LangChain commercial, Relevance, Lindy), substitutes prominent (DIY scripting), Helmer powers mostly absent, Porter's verdict: "structurally early, high entrant threat."

**Eval 3 — User claims no competitors:**
*Input:* User insists "we're a totally new category, no one is doing this"
*Expected output:* Skill pushes back, identifies 3+ substitutes, finds 2+ adjacent products, produces a real landscape. Output explicitly addresses the "no competitors" claim and refutes it.

## Guardrails

**On provenance (anti-fabrication — universal rule):**
- **Every named entity in output carries an inline provenance tag** at first mention and on any fact-bearing assertion. Allowed tags: `[user-provided]` / `[verified: <source-or-url>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged named entities are a contract violation. Named entities include: competitor names, customer counts ("5,000+ customers"), pricing figures, funding rounds, dates, G2 review counts/excerpts, recent moves, leadership names, public statements.
- **No silent assertion.** If you don't have a source and didn't get it from the user, default to `[unverified — needs check]` — never to a confident-looking specific (e.g., never fabricate "Guru raised $30M Series C, Sept 2025" without a Crunchbase URL).
- **Tool-grounding rule:** competitor profiling is the highest-fabrication-risk skill in this repo. If no live research tool (web search, Crunchbase MCP, G2 lookup) is available at runtime, every external-fact assertion (pricing, customer counts, funding, recent moves, review excerpts) defaults to `[unverified — needs check]`. The agent does NOT invent specifics to fill the per-competitor profile template.
- **Worked example warning.** The WorkflowDoc worked example contains many specific-sounding-but-fictional competitor data points (Guru's $25k–80k ACV, Stonly's $22M Series A, etc.) — tagged `[hypothetical]` inside the example. Do NOT replicate that pattern in real user output without the provenance tags + grounding above. A battle card with fabricated numbers loses deals when the buyer fact-checks.

**On evidence:**
- Every strength/weakness cites a source.
- Every pricing number labeled with source + confidence.
- No FUD. Unverified claims removed.
- Distinguish "we believe" from "we have evidence."

**On scope:**
- Maximum 5 competitors in the head-to-head matrix; more is unreadable.
- Battle cards stay 1 page.
- Don't profile Aspirational and Indirect tiers in detail unless requested.

**On bias:**
- User's existing competitor narrative is a hypothesis, not truth.
- Apply same rigor to user's product as to competitors.
- Force the "where they win" section — every competitor has segments they own.

**On legality:**
- Public sources only. No scraping behind logins. No competitor proprietary data the user doesn't have legitimate access to.
- Do not encourage trademark abuse in positioning ("X alternative" is legal; using X's logo in marketing without permission isn't).
- Battle card claims about competitor weaknesses must be defensible — treat them as if a customer might quote them back to the competitor.

**On freshness:**
- Date every competitor profile.
- Flag profiles >90 days old as stale and recommend `competitive-intelligence` for ongoing tracking.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Positioning unclear after analysis | `positioning-strategy` | Tiered list, top-3 weaknesses, segment ownership map |
| ICP needs sharpening based on win patterns | `icp-definition` | Win/loss patterns, segment ownership map |
| Ongoing tracking needed | `competitive-intelligence` | Tiered list, watch list per competitor, signal types |
| New whitespace identified | `market-research` (re-run for whitespace sizing) | Whitespace candidates from segment-ownership gaps |

---

## Push to CRM

After producing the per-competitor profiles and battle cards, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Each **named-product** competitor (Direct, or product-Substitute like Notion / Confluence / Document360) | `company` | `tags: "#competitor #competitor-tier:direct"` (or `:substitute`); `priority: cold` (we don't sell to them) |
| Each **non-product alternative** (DIY / hire a person / do nothing / shift budget elsewhere) | `interaction` (type: `research`) | `relevance` = description + buyer validation quote if available; tagged `#alternative #type:non-product #tier:substitute`. **No `company` record created** — this prevents fake prospects like "Outsourced VA" or "Do Nothing Inc." polluting the CRM. |
| Per-competitor profile (named products only) | `interaction` (type: `research`) | `relevance` = full profile markdown; tagged `#competitor-profile` |
| Battle card (top 3) | `interaction` (type: `note`) | One per top-3 competitor; tagged `#battle-card`; `relevance` = card content |
| Helmer 7-Powers + segment-ownership analysis | `interaction` (type: `research`) | One synthesis interaction; tagged `#strategic-analysis` |

**The named-product vs. non-product split is critical.** Earlier versions of this contract pushed *every* Substitute as a `company` record, which meant "Hire a knowledge manager" or "Use spreadsheets" became fake prospects. Don't do that. Named products (Notion, Confluence) are real entities and belong in `company`. Non-product alternatives (DIY, hiring, status quo, budget reallocation) are insights about buyer behavior and belong in `interaction`. They feed `positioning-strategy`'s Alternatives Analysis identically — the entity type is for CRM hygiene, not for changing how downstream skills consume them.

Indirect / Aspirational tiers: profile-only as interactions; do **not** push as `company` records — they will pollute the CRM.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:competitor-analysis:v2.0.0"`

### Example push (Direct competitor company record)

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
    "relevance": "Direct competitor — knowledge management category. Position: enterprise wiki for sales/support. Pricing: $15/user/month base. Strength: 6+ years brand, 5,000+ customers. Weakness: pre-LLM authoring UX; mid-market underserved (pushes upmarket). Helmer Powers: Branding (partial), Switching Costs (medium). Segment ownership: 500+ emp.",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### Example push (Battle card as interaction)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Guru",
    "tags": "#battle-card #competitor:guru",
    "relevance": "BATTLE CARD — Guru\nWHEN buyer is: 100–300 emp SaaS, support-team-led purchase\nWE WIN BECAUSE: AI-native authoring; per-support-seat pricing\nTHEY ATTACK US WITH: \"You are a startup; we have 5,000 customers\"\nWE COUNTER WITH: \"We are AI-native from day one — their authoring UX is pre-LLM\"\nTHE QUESTION THAT FLIPS IT: \"How long does it take your reps to author a new runbook today?\"",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### Example push (non-product alternative as interaction — NOT a `company` record)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#alternative #type:non-product #tier:substitute",
    "relevance": "ALTERNATIVE: DIY via spreadsheets + Slack channels (status quo).\nObserved in: 2 lost deals (Series A SaaS with <5 support staff).\nBuyer quote: \"We are not ready to buy a tool; we will run this in a spreadsheet for 6 months.\"\nSwitching cost: zero (no procurement, no IT, no champion needed).\nBeats us when: budget unavailable, team <5, pain has not yet hit acute trigger.\nFeeds positioning-strategy as a Step 1 alternatives entry; trade-off column = manual update burden + senior-rep time tax.",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

Note the omitted `company` field — non-product alternatives intentionally do NOT create a company record. The CRM stores the insight, not a fake prospect.

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above (named-product `company` records, profile/battle-card `interaction` records) |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #competitor-profile`. **Critical for this skill** — competitor pricing, customer counts, funding rounds, dates, recent moves, and G2 review excerpts are the highest-fabrication-risk fields. Inferred values go to the review queue, never to a live battle card or `company` record. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

The `#unverified #review-required` scaffold is in this skill file now; the dashboard review-queue surfacing is a follow-up agentic-app task. Until the dashboard is built, the tag at least keeps fabricated competitor data out of active battle cards (which sales reps quote in live deals — fabricated data here loses real revenue).

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #competitor-profile #competitor:guru",
    "relevance": "Guru pricing $25k–$80k ACV [unverified — needs check] — agent inferred from category, no Vendr or G2 negotiated-price confirmation. 5,000+ customers [unverified — needs check] — claim from competitor website, not independently verified. Recent move: Series C $30M Sept 2025 [unverified — needs check] — no Crunchbase URL captured. Hold for human verification before adopting in battle card.",
    "source": "skill:competitor-analysis:v2.0.0"
  }'
```

### When NOT to push

- "No competitors" claim by user (skill should have already pushed back; if not, do not pollute CRM with zero records).
- Aspirational / Indirect tier — keep these in the local artifact only.
- Non-product alternatives — push to `interaction` only, never to `company` records, even when they are listed in the Substitute tier of the analysis.
