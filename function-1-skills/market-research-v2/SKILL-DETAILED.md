---
name: market-research
description: Research and size a target market for GTM planning by defining the category, estimating demand, segmenting buyers, and identifying whitespace using TAM/SAM/SOM modeling, JTBD framing, Steve Blank market-type diagnosis, and Geoffrey Moore segment scoring. Use when the user needs market sizing, category framing, segment analysis, demand validation, whitespace mapping, or a structured market overview before go-to-market execution.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, market-research, market-sizing, segmentation, whitespace, strategy, function-1]
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
  - category-definition-and-jtbd-statement
  - tam-sam-som-sizing-model
  - segment-breakdown-with-bowling-pin-scores
  - demand-signals-summary
  - whitespace-opportunity-cards
  - risks-and-assumptions-register
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Market Research

Research and size a target market so downstream GTM work (ICP, positioning, channel selection) is anchored in evidence instead of guesswork. Produces a directional but defensible market view: enough rigor to make a real decision without false precision.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Market Research is the entry point for GTM market intelligence. It establishes the category, market boundaries, market size assumptions, segment structure, and whitespace opportunities so downstream GTM work is anchored in evidence instead of guesswork.

This skill produces a **directional but defensible market view**: enough rigor that a founder, GTM lead, or investor can make a real decision, but without false precision that ignores how shaky early-stage data actually is.

## When to Use

Trigger this skill when the user explicitly requests or implies need for:
- Market sizing ("How big is this market?", "Help me size this")
- Category framing ("What market are we actually in?", "What category should we claim?")
- Segment analysis ("Break this market into segments", "Who are the distinct buyer groups?")
- Demand validation ("Is there real demand?", "Is this opportunity large enough?")
- Whitespace mapping ("Where are the gaps in this category?", "What's underserved?")
- Pre-GTM grounding (before running competitor-analysis, icp-definition, positioning-strategy, or channel-strategy)
- Investor or board-prep market overviews
- Geographic expansion analysis

**Do NOT use this skill when:**
- The user has an existing ICP and just wants to refine messaging → use `positioning-strategy`
- The user wants to compare specific competitors head-to-head → use `competitor-analysis`
- The user wants to set up ongoing monitoring → use `competitive-intelligence`
- The user has already validated the market and needs lead generation → route to Function 2 (`lead-sourcing-*`)

## Inputs Required

### Parameterized inputs

| Field | Profile path | Required |
|---|---|---|
| Product description | `{{profile.product.description}}` | Yes |
| Geography | `{{profile.market.geography}}` | Yes |
| Customer type hypothesis | `{{profile.market.customer_type}}` | Yes |
| Pricing model | `{{profile.product.pricing_model}}` | Yes |
| ACV range | `{{profile.product.acv_range}}` | Yes |
| Time horizon | `{{profile.market.time_horizon}}` | Optional (default: 12 months) |
| Evidence sources | `{{profile.market.evidence_sources}}` | Optional |
| Existing customers | `{{profile.customers.won_deals}}` | Optional but high-value |
| Stage of company | `{{profile.company.stage}}` | Optional (default: early-stage) |

### Fallback intake flow

If any required field is missing, collect it conversationally before proceeding:

> To produce a useful market view, I need 4 things:
>
> 1. **Product** — what does it do, who is it for, and what outcome does it produce? (1–2 sentences)
> 2. **Geography** — what region or markets are in scope? (e.g., US-only, North America, English-speaking)
> 3. **Buyer hypothesis** — who do you think buys this? (role + company type)
> 4. **Economics** — rough ACV or pricing model? (Even a range is fine: <$1k, $1–10k, $10–50k, $50k+)
>
> Optional but high-leverage:
> 5. Time horizon (now / 12 months / 3 years)
> 6. Any existing customers or paid pilots — even 1–2 names helps a lot
> 7. Specific evidence sources you trust (analyst reports, customer interviews, internal data)

**Do not proceed with sizing if items 1–4 are missing.** Push back instead: "I can give you a real market view once you tell me [missing items]. Without those, anything I produce will be too generic to use."

### Input validation rules

- If `geography` is "global" → push back: "Global is too broad for a useful TAM. Pick the 1–3 markets you'll actually sell in for the next 12 months."
- If `customer_type` is "everyone" or "all businesses" → push back: "I need at least a directional segment to anchor sizing. Common starting cuts: company size, industry, or function."
- If `acv_range` is missing → proceed but flag all sizing as "directional only" until economics are confirmed.
- If `pricing_model` conflicts with `customer_type` (e.g., $50k ACV + "SMBs under 10 employees") → flag the mismatch and ask the user to resolve before sizing.

---

## Frameworks Used

This skill operationalizes five established frameworks. Apply them in order.

### 1. Steve Blank's Market-Type Diagnostic

Before sizing anything, classify the market type — sizing methods differ by type:

| Market Type | Definition | Sizing Approach |
|---|---|---|
| **Existing market** | Known category, known competitors, known buyers | Top-down from analyst reports + bottom-up cross-check |
| **Resegmented market** | New positioning inside an existing category (low-cost or niche) | Top-down for parent category × segment share assumption |
| **New market** | Category does not yet exist; buyer behavior is being created | Bottom-up only; analogous market comparison; no top-down |
| **Clone market** | Proven elsewhere, new geography | Reference market × geographic adjustment factor |

**Why this matters:** founders default to top-down sizing for everything. New markets have no reliable top-down data; using analyst numbers there is fiction.

### 2. Christensen's Jobs-to-be-Done (JTBD) Market Framing

When category labels are unclear or contested, frame the market by the *job* the customer hires the product to do, not the product feature set. This produces:
- A buyer-language category description
- A truer competitor set (anything else hired for the same job, including DIY/spreadsheets)
- A more durable market definition (jobs are stable; categories shift)

Use when: customer says "we're a new category" or "we don't fit existing categories cleanly."

JTBD statement format: *"When [situation], I want to [motivation], so I can [outcome]."*

### 3. TAM / SAM / SOM (with confidence labeling)

Definitions used in this skill:

- **TAM (Total Addressable Market):** total spend if every eligible buyer in scope bought the product, at the user's pricing. Theoretical ceiling.
- **SAM (Serviceable Addressable Market):** TAM filtered to the segments and geographies the user can actually reach with their current motion.
- **SOM (Serviceable Obtainable Market):** realistic 3-year capture given competitive density, motion strength, and resourcing.

**Calculation methods (use at least 2 and triangulate):**

| Method | Formula | When to use | Confidence ceiling |
|---|---|---|---|
| Top-down | Industry report figure × segment share | Mature categories with analyst coverage | Medium (anchors to others' assumptions) |
| Bottom-up | # of target accounts × ACV × adoption % | Always, when buyers can be counted | High (assumptions are visible) |
| Value-theory | (Customer count) × (annual value created) × (capture rate) | Net-new categories, B2B with measurable ROI | Medium-high |
| Analogous | Reference market × adjustment factor | Clone markets, new geographies | Low-medium (reference choice matters) |

**Confidence labeling rule:** every sizing number must be tagged `[high]`, `[medium]`, or `[low]` confidence based on source quality and method count. Single-method sizing caps at Medium.

### 4. Bowling-Pin Segment Sequencing (after Geoffrey Moore) + 5-dimension scoring rubric

The **bowling-alley / bowling-pin metaphor** is from Geoffrey Moore's *Inside the Tornado* (1995): segments are not equal, and a beachhead win supplies reference momentum to the next segment, which supplies it to the next. Moore's own segment-evaluation criteria are *target customer characterization* — compelling reason to buy, decision-maker accessibility, whole-product feasibility, partner/ally presence, and competitive density.

The **5-dimension 25-point rubric below is a simplified house-built scorecard inspired by Moore's logic**, not Moore's original criteria:

| Dimension | What it measures |
|---|---|
| Pain severity | How acute is the problem for this segment |
| Urgency / triggers | Is there an event making it "now" |
| Reachability | Can the user reach this buyer with available motion |
| Reference value | Will winning this segment unlock the next |
| Economic capacity | Can they pay |

Sum → 5–25 score. The highest-scoring segment is the **head pin (beachhead)**. The next 2–3 are downstream pins reachable through the beachhead's reference power.

For deeper sequencing decisions (whole-product gaps, partner ecosystems), apply Moore's full target-customer characterization separately.

### 5. Whitespace Diagnostic (4 lenses)

Underserved opportunities cluster in four places. Check each:
- **Segment whitespace** — buyer types incumbents ignore (often: SMBs, regulated industries, non-English markets, prosumer)
- **Use-case whitespace** — adjacent jobs the category doesn't serve
- **Pricing whitespace** — gaps in pricing tiers (often: between $0 and $20k/yr; or above $200k where seat-based stops working)
- **Experience whitespace** — implementation, onboarding, support, integrations where incumbents are weak

For each whitespace candidate, document: (a) who it serves, (b) why incumbents ignore it, (c) why the user can address it, (d) what it would take to validate.

---

## Tools and Sources

Named tools and sources for each step. Use the primary; fall back to alternatives if access or budget is constrained.

### Category definition and market mapping

| Source | What it's good for | Cost | Notes |
|---|---|---|---|
| **G2 / Capterra / TrustRadius** | Existing category labels, vendor lists, segment counts | Free | Best starting point for established categories |
| **CB Insights** | Category trees, taxonomy, market reports | Paid (expensive) | Best for emerging categories |
| **Crunchbase** | Company-level data, category tags, funding signals | Freemium | Good for competitive landscape |
| **Gartner / Forrester / IDC** | Analyst category definitions, Magic Quadrants | Paid (very expensive) | Use sparingly; analyst categories often lag the market |

### Market sizing

| Source | What it's good for | Cost | Notes |
|---|---|---|---|
| **Statista** | Pre-built market size estimates by category | Paid | Useful anchor; verify methodology |
| **IBISWorld** | Industry-level sizing and growth | Paid | Best for traditional industries |
| **PitchBook** | Private market activity, investment flows | Paid (expensive) | Signal of where capital sees opportunity |
| **SEC EDGAR** | Public company segment revenue (10-K, 10-Q filings) | Free | Underused; gold for adjacent-category sizing |
| **Census / OECD / World Bank** | Account-count denominators (firms by size, industry) | Free | Bottom-up sizing foundation |

### Demand validation

| Source | What it's good for | Cost | Notes |
|---|---|---|---|
| **Google Trends** | Search interest over time, geography | Free | Use for category-level demand direction |
| **Exploding Topics** | Emerging trend discovery | Freemium | Good for "is this momentum real" |
| **Reddit / Hacker News / Indie Hackers** | Buyer pain in their words | Free | Read 20+ threads in target community |
| **Glassdoor / LinkedIn job postings** | Hiring patterns = budget signal | Free | "If buyers are hiring for this skill, the budget exists" |
| **AnswerThePublic / SEMrush** | Search query landscape | Freemium | What buyers actually ask |

### Technographic / firmographic enrichment

| Source | What it's good for | Cost |
|---|---|---|
| **BuiltWith / Wappalyzer** | Tech stack data per company | Freemium |
| **Apollo / ZoomInfo / Clearbit** | Firmographic counts, contact data | Paid |
| **HG Insights / Enlyft** | Tech adoption at scale | Paid |

### Buyer research (when budget allows)

| Source | What it's good for | Cost |
|---|---|---|
| **Userinterviews.com / Respondent** | Recruit B2B interviewees | Paid per interview ($75–200) |
| **Wynter** | B2B message testing with target buyers | Paid |
| **Internal CRM + customer calls** | The single highest-signal source | Free — **use first if available** |

**Source-priority rule:** internal data (customer calls, CRM, support tickets) > primary research (interviews) > free public (Reddit, G2, LinkedIn) > paid databases (Crunchbase, PitchBook) > analyst reports.

---

## Procedure

### Step 1: Diagnose market type

Apply Steve Blank's market-type framework. Output: one of `{existing, resegmented, new, clone}` with rationale.

This determines which sizing methods to use in Step 4. Do not skip.

### Step 2: Define the market frame

Produce three artifacts:
1. **Category claim** — the label buyers use (verify against G2/Capterra; use customer-language, not internal-language)
2. **Adjacent categories** — 2–4 categories that buyers may compare against
3. **JTBD statement** — *"When [situation], buyer wants to [motivation], so they can [outcome]"*

**Decision rule:** if buyers can't recognize the category in 5 seconds, prefer JTBD framing over a novel category claim.

### Step 3: Set market boundaries

Specify and document:
- **Geography** (named regions, not "global")
- **Customer type** (firmographic filters: size, industry, function)
- **Use cases included** (and explicitly excluded)
- **Time horizon** (current / 12mo / 3yr)
- **Buyer persona scope** (primary buyer + influencers)

If any of these is undefined, return to fallback intake before proceeding.

### Step 4: Build directional sizing

Use at least two methods from the framework table. Output a sizing model with:
- Each calculation shown
- Every assumption labeled with source and confidence (`[H/M/L]`)
- Reconciliation if methods disagree by >2x (explain why)

**Do not produce a single TAM number without showing the math.**

### Step 5: Segment the market

Apply the 5-dim bowling-pin scoring rubric (1–5 on each dimension per segment). Produce 3–7 segments. For each:
- Buyer count (firmographic)
- Average willingness to pay (range)
- Pain intensity (1–5)
- Urgency (1–5)
- Reachability (1–5)
- Reference value to next segment (1–5)
- Economic capacity (1–5)

Mark the highest-scoring segment as the **beachhead candidate**. This becomes a key input to `icp-definition`.

### Step 6: Gather demand signals

Run a structured signal sweep across these channels (use the Tools table):
- **Search demand** — Google Trends 12-month direction; top queries; keyword volume
- **Community pain** — 10+ Reddit/HN/community threads; tagged by pain pattern
- **Hiring signals** — LinkedIn job postings mentioning the problem or category
- **Capital signals** — funding rounds in adjacent companies (Crunchbase)
- **Review-site momentum** — G2 category growth, new entrants in last 12 months
- **Internal signals** — if the user has any: inbound interest, organic signups, sales calls (highest weight)

Synthesize into 5–10 demand signals with strength labels (`[H/M/L]`).

### Step 7: Identify whitespace

Apply the 4-lens whitespace diagnostic (segment / use-case / pricing / experience). Document 3–5 hypotheses. For each, fill the validation card:

```
Whitespace: [name]
Lens: [segment / use-case / pricing / experience]
Who it serves: [buyer description]
Why incumbents ignore it: [reason]
Why we can address it: [unique angle]
Validation needed: [3-5 questions or experiments]
Confidence: [high / medium / low]
```

### Step 8: Synthesize into market view

Produce the final brief using the Output Template (below). Critical: include the **Risks & Assumptions register** explicitly. Every load-bearing claim must have an assumption flag.

### Step 9: Route downstream

Based on outputs, recommend the next skill (see Linked Skills). Always state the recommended next step.

---

## Output Template

Fill every section. If a section cannot be filled with evidence, write "Insufficient data — see Risks register" — never fabricate.

---

### Market Brief: [Product Name]

**Prepared:** [date]
**Geography:** [scope]
**Time horizon:** [period]
**Confidence overall:** [high / medium / low]

---

**1. Market Type**
Type: [existing / resegmented / new / clone]
Rationale: [2–3 sentences]

**2. Category Definition**
Primary category (buyer-recognized): [label]
Adjacent categories: [list]
JTBD statement: When [situation], buyer wants to [motivation], so they can [outcome].

**3. Market Boundaries**
Geography: [list]
Customer type: [firmographic filters]
Included use cases: [list]
Excluded use cases: [list]

**4. Sizing Model**

| Layer | Number | Method | Key assumptions | Confidence |
|---|---|---|---|---|
| TAM | $X | [method] | [list] | [H/M/L] |
| SAM | $Y | [method] | [list] | [H/M/L] |
| SOM (3yr) | $Z | [method] | [list] | [H/M/L] |

Reconciliation note: [if methods disagreed by >2x]

**5. Segment Breakdown**

| Segment | Buyer count | Avg ACV | Pain | Urgency | Reach | Ref value | Capacity | Score | Tier |
|---|---|---|---|---|---|---|---|---|---|
| [name] | [#] | [$] | [1–5] | [1–5] | [1–5] | [1–5] | [1–5] | [/25] | [Beachhead/Pin 2/Pin 3/Defer] |

**6. Demand Signals**

| Signal | Source | Direction | Strength |
|---|---|---|---|
| [observation] | [tool/source] | [up/flat/down] | [H/M/L] |

**7. Whitespace Opportunities**

[Use the validation card format from Step 7. List 3–5.]

**8. Risks & Assumptions**

| Assumption | Confidence | What would change the view |
|---|---|---|
| [claim] | [H/M/L] | [validating event] |

**9. Recommended Next Step**

[Named follow-on skill + 1-sentence rationale]

---

## Worked Example

> *The example below uses **WorkflowDoc**, a fictional AI-native runbook authoring tool for B2B SaaS support teams. The fictional product is shared across all six function-1 skills so the worked examples interlock. The frameworks below apply to any B2B GTM context.*

**Input (fallback intake — customer answers in chat):**

> Product: A workflow documentation tool `[hypothetical]` for B2B SaaS support teams. Helps support managers turn tribal knowledge into searchable, AI-queryable runbooks.
> Geography: US only
> Buyer hypothesis: VPs of Customer Support at 50–500 employee SaaS companies
> Pricing: $400/seat/year `[hypothetical]`, typical deployment 8–15 seats; ACV $3.2k–$6k `[hypothetical]`
> Time horizon: 12 months
> Existing customers: 4 paid pilots `[hypothetical]` in last 6 months

### Output:

> **Provenance note for the agent reading this example:** every named entity below (TAM/SAM/SOM dollar figures, segment sizes, growth rates, comparable companies, named tools, analyst-report numbers) is `[hypothetical]` — i.e., fictional content for illustration. Market sizing is fabrication-prone — invented numbers look authoritative even when they're guesses. In real user output, the agent must apply the per-entity tagging discipline using `[user-provided]` / `[verified: <source-or-url>]` / `[unverified — needs check]` as appropriate (see `## Guardrails` provenance rule). Never quote a TAM figure externally without a citation.

---

### Market Brief: WorkflowDoc

**Prepared:** 2026-04-30
**Geography:** US
**Time horizon:** 12 months
**Confidence overall:** Medium

**1. Market Type**
Type: **Resegmented market.** This is a niche play inside the broader knowledge management / internal documentation category (Notion, Guru, Confluence are incumbents). The resegmentation angle is "support-team-first, AI-native" — the parent category exists; the angle is new.

**2. Category Definition**
Primary category: **AI-powered support knowledge management.** Buyers will compare against Guru, Stonly, Document360.
Adjacent: Internal wiki tools (Notion, Confluence), customer-facing help centers (Intercom Help, Zendesk Guide), workflow automation (Tango, Scribe).
JTBD: When a new support rep needs to resolve a complex ticket and the knowledge isn't in the help center, they want to find a vetted runbook fast, so they can resolve without escalating.

**3. Market Boundaries**
Geography: US
Customer type: B2B SaaS, 50–500 employees, Series A–C
Included use cases: Internal support runbooks, escalation playbooks, product knowledge for support teams
Excluded: Customer-facing help centers, sales enablement, engineering docs

**4. Sizing Model**

| Layer | Number | Method | Key assumptions | Confidence |
|---|---|---|---|---|
| TAM | $186M | Bottom-up: 12,400 US SaaS firms (50–500 emp, Crunchbase) × $15k avg ACV | $15k = 30 seats × $500. Conservative seat count. | Medium |
| TAM cross-check | $210M | Top-down: 5% of $4.2B knowledge mgmt category (G2 + Statista) for support-specific slice | 5% slice estimate is the weakest assumption | Low |
| SAM | $52M | TAM filtered to firms with >5 support staff (BuiltWith + LinkedIn estimate ~3,500 firms) × $15k | Support team size proxy uses LinkedIn job postings | Medium |
| SOM (3yr) | $5.2M | 10% capture of SAM in 3 years | Assumes 1 enterprise AE + product-led adoption motion | Low |

Reconciliation note: TAM bottom-up ($186M) and top-down ($210M) within 13% — both methods triangulate to ~$200M TAM. Confident at directional level; not confident on category-slice methodology.

**5. Segment Breakdown**

| Segment | Buyer count | Avg ACV | Pain | Urgency | Reach | Ref value | Capacity | Score | Tier |
|---|---|---|---|---|---|---|---|---|---|
| Series B SaaS, 100–300 emp, growing support team | 1,800 | $5k | 5 | 4 | 4 | 4 | 4 | 21 | **Beachhead** |
| Series C/D SaaS, 300–500 emp, mature support | 700 | $20k | 4 | 3 | 3 | 5 | 5 | 20 | Pin 2 |
| Series A SaaS, 50–100 emp, support of 2–5 | 6,200 | $2.5k | 3 | 3 | 5 | 2 | 2 | 15 | Pin 3 (defer; ACV too low) |
| Enterprise SaaS, 500+ emp | 200 | $50k+ | 4 | 2 | 1 | 5 | 5 | 17 | Defer (sales cycle too long for stage) |

**6. Demand Signals**

| Signal | Source | Direction | Strength |
|---|---|---|---|
| "Support runbook" search volume up 67% YoY | Google Trends | Up | Medium |
| 14 of last 20 r/CustomerSuccess threads mention "tribal knowledge" pain | Reddit | Up | High |
| 230+ "Support Operations Manager" job postings mention runbook/knowledge mgmt | LinkedIn | Up | High |
| Guru raised $30M, Stonly $22M in last 18 months | Crunchbase | Up | Medium |
| 4 paid pilots from cold outbound in 6 months (internal data) | Internal | Up | High |

**7. Whitespace Opportunities**

```
Whitespace: AI-native runbook authoring
Lens: Experience
Who it serves: Support managers without time to write/update runbooks
Why incumbents ignore it: Guru/Stonly built pre-LLM; their authoring is manual-first
Why we can address it: AI-native from day one; ingest tickets → draft runbook
Validation needed: Will support managers trust AI-drafted runbooks? What's the human-review loop?
Confidence: Medium
```

```
Whitespace: Support-team-first pricing
Lens: Pricing
Who it serves: Support teams under 30 seats
Why incumbents ignore it: Notion/Confluence price for company-wide deployment ($10-15/user broad)
Why we can address it: Per-support-seat pricing at $30-50/seat captures more value from a smaller, higher-pain audience
Validation needed: 5 pricing-sensitivity interviews with VPs of Support
Confidence: High
```

```
Whitespace: Mid-market (Series B/C) underserved
Lens: Segment
Who it serves: 100–300 employee SaaS firms with growing support teams
Why incumbents ignore it: Guru pushes upmarket; Notion treats them as generic users
Why we can address it: Stage-specific feature focus, support-team go-to-market
Validation needed: Conversion rates from beachhead pilots; expansion rates
Confidence: High
```

**8. Risks & Assumptions**

| Assumption | Confidence | What would change the view |
|---|---|---|
| ACV of $5k holds at scale (currently 4 pilots) | Medium | First 10 paid customers — does median ACV stay >$4k? |
| 5% support-specific slice of broader KM category | Low | Better data from analyst report or internal customer survey |
| 30 seats avg deployment | Medium | Cohort analysis from first 20 customers |
| AI-drafted runbooks will be trusted by users | Low | Pilot customer NPS specifically on AI-drafted vs manual runbooks |
| Guru/Stonly will not move down to mid-market quickly | Medium | Quarterly competitor pricing/positioning check |

**9. Recommended Next Step**

→ `icp-definition`. The beachhead segment (Series B SaaS, 100–300 emp, growing support team) is sized and scored. Next: define the buyer persona, champion, user, and qualification rules for that specific segment. Carry forward: segment definition, ACV assumption, pain signals, named demand evidence.

---

## Heuristics

- **Directional confidence beats fake precision.** $186M with assumptions visible > $173.4M with hidden methodology.
- **Size the reachable market, not the biggest one.** TAM is a check; SAM and SOM drive decisions.
- **Internal data > everything else.** Four paid pilots tell you more than any analyst report.
- **If the methods disagree by >2x, you don't have a sizing — you have a research problem.** Resolve before publishing the number.
- **Buyer interviews trump analyst taxonomy.** If 10 buyers can't agree what category your product is in, you're looking at JTBD framing, not category framing.
- **Demand signals compound.** No single signal is reliable. 5+ signals pointing the same direction is.
- **A segment that "loves" the product but never closes is not a segment.** Pain + urgency + capacity, all three, or it doesn't make the bowling pin.
- **Whitespace that everyone can see is not whitespace.** If 3 incumbents are about to ship the feature, it's a roadmap item, not a market gap.

## Edge Cases

### Net-new categories (no analyst data)
- Skip top-down sizing. Use bottom-up + value-theory only.
- Frame the market by JTBD, not category.
- Use analogous markets carefully — name the reference and the adjustment factor.
- Confidence cap: cannot exceed Medium.

### Multi-product companies
- Size per use case, not at the whole-company level.
- Each product gets its own market brief.
- If the user pushes for a unified TAM, produce it but flag it as "additive sum, not a real addressable market."

### Sparse-data verticals (e.g., regulated industries, non-English markets)
- Triangulate via: regulators (counts of licensed firms), industry associations (member counts), payment processors (transaction volume), and direct interviews.
- Confidence cap: Medium.
- Document the data scarcity explicitly in the Risks register.

### Services + software hybrids
- Separate product TAM from services revenue potential.
- Show two layers: pure-product SOM and product+services SOM.
- This affects motion choice (sales-led vs. PLG) downstream.

### Geographic expansion
- Treat each new market as a clone-market analysis.
- Use the home-market data as the reference; apply adjustment factors for: (a) market maturity, (b) buyer willingness-to-pay differences, (c) competitive density, (d) GTM cost differential.

### Conflicting data sources
- Use confidence weighting: internal > primary research > free public > paid databases > analyst reports.
- Show both numbers; pick the higher-confidence one as primary; note the discrepancy.
- Never silently average them.

## Failure Modes and Recovery

| Failure mode | Symptom | Recovery |
|---|---|---|
| User can't define geography | "We sell globally" / "wherever the customer is" | Pin them to top 2–3 actual markets they'd target in next 12 months. If they can't, escalate: this means GTM strategy doesn't exist yet — note in deliverable. |
| User can't size buyer count | No firmographic data; no Apollo/Crunchbase access | Use SEC EDGAR + LinkedIn job postings as proxy. Confidence cap: Low. |
| Analyst reports unavailable (paywall) | Need Gartner/Forrester | Use G2 category data + Crunchbase company counts. Statista as anchor if available. |
| User is in stealth and won't share details | Limited input | Produce a generic category-level view with explicit "no proprietary inputs" caveat. Recommend re-running once stealth ends. |
| TAM comes back too small to matter | SOM <$1M, market unattractive | Push back: "The market as scoped is too small for VC-grade GTM. Options: (a) re-scope wider, (b) accept lifestyle-business economics, (c) reconsider the product." Don't paper over. |
| TAM comes back implausibly large | Top-down number reads as $50B+ for a niche tool | Apply bottom-up sanity check. If gap >5x, the top-down method is wrong — likely category mismatch. Re-run Step 2. |
| Customer has an existing TAM number from elsewhere | "Our deck says $40B TAM" | Recompute independently first. Then reconcile. If your number is materially different, surface the gap with methodology comparison; don't just defer. |
| Segments don't differentiate clearly | All segments score similarly on bowling pin | Insufficient data — recommend user interviews. Note in deliverable: "Segmentation requires 5–10 buyer interviews to differentiate further." |

## Pitfalls

- **Treating a broad TAM as a GTM plan.** TAM is a check, not a strategy.
- **Mixing multiple categories without defining boundaries.** Pick one primary frame.
- **Confusing user interest with purchasing intent.** Reddit upvotes ≠ paid conversions.
- **Over-relying on one analyst report.** Especially Gartner/Forrester for emerging categories — they lag.
- **Ignoring substitutes and status quo.** "Spreadsheets + a VA" is a real competitor for most B2B tools.
- **Sizing what's measurable instead of what matters.** If your real beachhead is a specific operations niche, don't size the whole industry because the data is easier to find.
- **False precision.** Three decimal places on a number where the input has 50% uncertainty is malpractice.
- **Skipping the assumption register.** Every TAM has assumptions. If they're not written down, they will silently break later.

## Verification

The skill output is complete and useful when:
1. The user can name their market type, category, and JTBD in one sentence.
2. The user can defend their TAM/SAM/SOM number to a skeptical investor or board member without rebuilding the math.
3. The user has a named beachhead segment with rationale.
4. The user has 3–5 whitespace hypotheses they can validate next quarter.
5. The user knows which assumption, if invalidated, would change the strategy.
6. Findings are usable as input to `icp-definition` and `positioning-strategy` without re-research.

If any of these is "no," the skill has not finished its job — re-run the relevant step.

## Done Criteria

1. Market type diagnosed and labeled.
2. TAM/SAM/SOM produced with at least 2 sizing methods + reconciliation.
3. Every sizing number tagged with confidence (`[H/M/L]`).
4. 3–7 segments scored on the 5-dim bowling-pin rubric; beachhead identified.
5. 5–10 demand signals collected with strength labels.
6. 3–5 whitespace hypotheses documented with validation cards.
7. Risks & Assumptions register filled (every load-bearing claim flagged).
8. Recommended next skill named with rationale.

## Eval Cases

The skill should be tested against three reference scenarios. (Full eval inputs/outputs in `evals/` — not bundled here.)

**Eval 1 — Mature category, rich data:**
*Input:* CRM software for SMB law firms, US, $150–400/user/month
*Expected output shape:* TAM/SAM/SOM with high confidence, top-down + bottom-up triangulation within 1.5x, named incumbents (Clio, MyCase, PracticePanther), 3–4 segments differentiable, clear beachhead.

**Eval 2 — Niche vertical, sparse data:**
*Input:* Compliance automation for biotech HR teams, North America, $40k ACV
*Expected output shape:* TAM with Medium confidence, bottom-up only (top-down flagged unreliable), 1–2 segments, whitespace likely strong on segment dimension, Risks register dense with "needs primary research."

**Eval 3 — Net-new category:**
*Input:* AI agent orchestration platform for non-technical founders, global English-speaking, ACV unclear
*Expected output shape:* JTBD framing dominant (category is unstable), value-theory sizing + analogous (e.g., reference: low-code platforms), confidence cap at Medium, push-back to user on geography ("global" too broad), strong Risks register.

## Guardrails

**On provenance (anti-fabrication — universal rule):**
- **Every named entity in output carries an inline provenance tag** at first mention and on any fact-bearing assertion. Allowed tags: `[user-provided]` / `[verified: <source-or-url>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged named entities are a contract violation. Named entities include: market sizing numbers (TAM/SAM/SOM), named segments with company counts, comparable companies, analyst-report figures, growth rates, named tools/sources.
- **No silent assertion.** If you don't have a source and didn't get it from the user, default to `[unverified — needs check]` — never to a confident-looking specific (e.g., never invent "$4.2B TAM growing 18% CAGR" without a citation).
- **Tool-grounding rule:** market sizing is fabrication-prone. If no live research tool (analyst reports, Crunchbase, public filings) is available at runtime, every external-fact assertion (TAM/SAM/SOM numbers, segment sizes, growth rates, comparable companies' revenue) defaults to `[unverified — needs check]`. The agent does NOT invent percentages to fill the template.
- **Worked example warning.** Worked examples in this skill contain specific-sounding-but-fictional market figures, tagged `[hypothetical]`. Do NOT replicate that pattern in real user output without the provenance tags + grounding above.

**On evidence and confidence:**
- Every number gets a confidence label (`[H/M/L]`). No exceptions.
- Distinguish sourced facts from inference. If the agent infers, the inference is labeled.
- Do not present speculative numbers as facts.
- Triangulate methods. A TAM from a single method gets confidence cap Medium.

**On scope:**
- Avoid claiming exact market size when only directional evidence exists.
- Separate advisory output from investment-grade diligence — flag if the user needs the latter.
- Do not confuse "interesting" with "addressable" — if the user can't reach the market with their motion and budget, it is not in SOM.

**On framing:**
- Use buyer language for category (verified against G2/community), not internal product language.
- If category language is unstable, prefer JTBD framing.
- Don't manufacture a category. New-category claims trigger an extra confidence penalty.

**On bias:**
- The user's existing TAM number is not the answer. Recompute independently before reconciling.
- Pilot enthusiasm is not market validation. Apply bowling-pin scoring even when early customers love the product.
- Confirmation bias check: list 3 ways the market view could be wrong (this is the Risks register).

**On commercial sensitivity:**
- Respect public-source boundaries. Do not scrape paywalled content the user hasn't purchased access to.
- Cite sources where possible.
- If the user has shared internal data, do not include it verbatim in outputs that may be shared externally — paraphrase or reference.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Beachhead segment identified, no ICP defined yet | `icp-definition` | Segment definition, ACV, buyer-count, pain signals, demand evidence |
| Competitive landscape unclear | `competitor-analysis` | Category, geography, segments, named adjacents |
| Category settled, positioning unclear | `positioning-strategy` | Category, JTBD, segments, whitespace |
| Channel selection needed | `channel-strategy` | ICP signals, ACV, time horizon, geography |
| Ongoing monitoring needed | `competitive-intelligence` | Competitor list, signal types, cadence |
| Market is too small or wrong | Loop back: re-scope geography or customer type, re-run market-research |

---

## Push to CRM

After producing the Output Template above, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`). The full Market Brief is stored locally as the skill artifact; only the records below get pushed.

### Mapping

| Deliverable | Entity | Notes |
|---|---|---|
| Beachhead segment (named accounts, if any) | `interaction` (type: `research`) | One per skill run — full Market Brief in `relevance` |
| Tier 1 candidate accounts named in segment breakdown | `company` | `tags: #beachhead-candidate`, `priority: warm`, no `score` (set in `icp-definition`) |
| Whitespace hypotheses with named target accounts | `interaction` (type: `note`) | Each whitespace card → one note; tagged `#whitespace #market-research` |

If no specific accounts are named, push only the research interaction. Do not invent accounts to fill the schema.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=        # required only if server has AGENTIC_APP_TOKEN set
```

### Source tag

Stamp every record with: `source: "skill:market-research:v2.0.0"`

### Example push (research interaction — always emitted)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "relevance": "Market Brief 2026-04-30: Resegmented market in AI-powered support knowledge management. TAM $186M (bottom-up, Medium confidence). Beachhead: Series B SaaS, 100–300 emp, US, support team 5–15. JTBD: when a new support rep needs to resolve a complex ticket and the knowledge isn't in the help center, they want to find a vetted runbook fast, so they can resolve without escalating. Top whitespace: AI-native runbook authoring, support-team-first pricing, mid-market underserved. See skill artifact for full sizing model and Risks register.",
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
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #market-research`. TAM/SAM/SOM numbers, segment sizes, growth rates, comparable-company revenues without citations flow here for human review before being quoted externally. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

The `#unverified #review-required` scaffold is in this skill file now; the dashboard review-queue surfacing is a follow-up agentic-app task. Until the dashboard is built, the tag at least keeps inferred market figures out of decks and board updates.

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #market-research",
    "relevance": "TAM estimate $4.2B [unverified — needs check] — agent inferred from category mid-points, no Gartner/Forrester citation. SAM (US-only Series B-D) $620M [unverified — needs check] — derived from TAM, inherits its uncertainty. Growth rate 18% CAGR [unverified — needs check] — no source. Hold for verification before quoting externally.",
    "source": "skill:market-research:v2.0.0"
  }'
```

### When NOT to push

- No beachhead identified (skill incomplete)
- TAM <$1M (deliverable is a "do not pursue" recommendation, not CRM data)
- User explicitly asked for analysis only (flag: `--no-push`)
