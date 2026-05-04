---
name: positioning-strategy
description: Define product positioning using April Dunford's "Obviously Awesome" 5-component framework, JTBD-based wedge construction, message house architecture, value-by-role variations, and a for-and-against wedge against named competitors. Produces a positioning canvas, message house, role-specific value props, and competitive wedges. Use when the user needs positioning definition, repositioning, message hierarchy, value-prop articulation, or competitive wedge sharpening.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, positioning, messaging, value-proposition, dunford, function-1]
related_skills:
  - market-research
  - competitor-analysis
  - icp-definition
  - channel-strategy
  - competitive-intelligence
inputs_required:
  - product-description
  - icp-from-icp-definition
  - competitive-landscape-from-competitor-analysis
  - pricing-model-and-acv-range
deliverables:
  - positioning-canvas-dunford-5-component
  - alternatives-analysis-including-status-quo
  - unique-value-attributes-table
  - best-fit-icp-statement-for-positioning
  - market-category-claim
  - wedge-statement-with-3-test-diagnostic
  - message-house-pillar-architecture
  - value-props-by-role-buyer-champion-user
  - for-and-against-wedge-per-top-3-competitor
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Positioning Strategy

Define what your product is, who it's for, what it's better at, and against what alternatives — clearly enough that a buyer understands the wedge in 10 seconds and a sales rep, marketer, or AI agent can produce on-brand messaging without inventing it. The deliverable is not a tagline — it's a positioning canvas, a message house, and a wedge, all evidence-backed.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

This skill operationalizes April Dunford's framework (the gold-standard B2B positioning method) with explicit alternatives analysis, value attributes, and a tested wedge against the buyer's most likely default choice. Without it, positioning floats — every team member has a different version, outbound copy is invented per email, and competitive deals are won or lost on improvisation.

## When to Use

Trigger this skill when the user requests:
- Positioning definition for a new product or new launch
- Repositioning ("Our positioning isn't working — fix it")
- Message hierarchy ("What do we lead with vs. supporting messages?")
- Value proposition articulation ("Help me write our value prop")
- Competitive wedge sharpening ("How do we position against [competitor]?")
- Sales messaging audit / consolidation
- Pre-launch positioning grounding (after market-research + competitor-analysis + ICP)

**Do NOT use this skill when:**
- The user wants market sizing → `market-research`
- The user wants competitor profiles → `competitor-analysis`
- The user wants buyer profile → `icp-definition`
- The user wants cold email copy specifically → `cold-email-sequence` (planned)
- The user wants brand identity / visual / voice → outside scope; route to brand work

## Inputs Required

### Parameterized inputs

| Field | Profile path | Required |
|---|---|---|
| Product description | `{{profile.product.description}}` | Yes |
| ICP (from icp-definition) | `{{profile.icp}}` | Yes |
| Competitive landscape (from competitor-analysis) | `{{profile.competitors}}` | Yes |
| Pricing | `{{profile.product.pricing_model}}` | Yes |
| **Best-fit** customer quotes (rave / refer / would be reference) | `{{profile.customers.best_fit_quotes}}` | Optional, **highest-value** |
| Won-deal customer quotes (any won deal) | `{{profile.customers.won_deal_quotes}}` | Optional, second-highest-value |
| Lost-deal customer quotes | `{{profile.customers.lost_deal_quotes}}` | Optional, very high-value |
| Workaround Analysis from icp-definition | `{{profile.icp.workaround_analysis}}` | Optional, high-leverage (feeds Alternatives Analysis directly) |
| Existing positioning materials | `{{profile.positioning.current}}` | Optional |
| Brand voice guide | `{{profile.brand.voice}}` | Optional |

### Fallback intake flow

> To produce useful positioning, I need:
>
> 1. **Product** — what it does, in 2 sentences
> 2. **ICP** — who is your beachhead customer (or paste your ICP doc)
> 3. **Top 3 competitors / alternatives** — including the status quo (DIY, spreadsheets, "do nothing")
> 4. **Pricing** — model + ACV
>
> **High-leverage optional:**
> 5. **Best-fit customer quotes** — quotes from customers who *rave about you, would refer you, and would actively be a reference*. Per Dunford, these are the customers whose perception reveals the true value. 5+ best-fit quotes = great. This unlocks "buyer language" that beats anything we'd invent. **Distinct from "any won deal"** — a customer who bought but doesn't evangelize tells you something different (often: positioning is loose enough to land non-best-fit deals).
> 6. **Any-won-deal quotes** — broader, second-tier evidence
> 7. **Lost-deal quotes** — what they said when they didn't buy
> 8. **Workaround Analysis from `icp-definition`** — current workaround / cost / dream state. Each workaround entry becomes an alternative in Step 1.
> 9. **Current positioning materials** — homepage hero, sales deck slide 1, deck objection slide. If provided, ask: "What about the current positioning isn't working? (Conversion / win-rate / market shift / other)"

### Input validation rules

- If ICP is missing → push back: "Positioning without ICP is for-everyone-and-no-one. Run `icp-definition` first." (If user insists, proceed with reduced confidence and flag.)
- If competitive landscape is missing → push back: "Positioning is relative to alternatives. I need your top 3 competitors including status quo. We can run `competitor-analysis` first if needed."
- If product description is generic ("AI-powered platform for [industry]") → ask for the specific job the product does.
- If user has zero customer quotes → flag: positioning will use inferred buyer language; mark confidence as Low (hypothesis-only) — see Confidence Rubric below.
- If user provides won-deal quotes but cannot name **3+ best-fit customers** (rave / refer / would be reference) → flag: positioning is being built from "customer base" not "best-fit base" — confidence cap Medium. The artifact will land deals broadly but will not be the sharp wedge Dunford's framework is designed to produce.

---

## Frameworks Used

### 1. April Dunford's "Obviously Awesome" Positioning (the spine)

From *Obviously Awesome* (Dunford, 2019). The dominant framework in B2B positioning. Five components:

| Component | Definition | Output |
|---|---|---|
| **Competitive alternatives** | What the customer would do if you didn't exist | Named list including status quo |
| **Unique attributes** | Features only you have (or have meaningfully more of) | Feature list |
| **Value (and proof)** | Outcomes the unique attributes produce that customers care about | Value list with evidence |
| **Best-fit ICP** | Customer segment that values these attributes most | ICP segment |
| **Market category** | Frame of reference that signals "what kind of thing is this" | Category label |

**Critical rule:** positioning is *relative to alternatives*. Skipping the alternatives analysis is the most common failure mode. A "great" feature is only great relative to what the customer would otherwise use.

### 2. Category Design Choices (after Lochhead, Ramadan, Peterson, Maney — *Play Bigger*)

Note on attribution: the **adoption-lifecycle / chasm** framework in Geoffrey Moore's *Crossing the Chasm* is about innovators → early adopters → early majority → late majority → laggards, not about category-frame choice. The category-design choices below are closer to **Play Bigger / Category Design** (Lochhead et al., 2016) and Dunford's category-design discussion in *Sales Pitch*. Moore's contribution to this skill is the **positioning statement template** used in §3 (the wedge format).

Categories signal who the product is for. Choosing the right category frame is consequential:

| Frame type | When to use | Risk |
|---|---|---|
| **Existing established category** | Buyer recognizes the label; you're a better option | Easier to position; harder to differentiate from incumbents |
| **Subcategory of existing** | Buyer recognizes parent; you're a specialized version | Right balance for most products; "X for Y" pattern |
| **New category** | Buyer doesn't yet recognize; you're creating the frame | High risk, high reward; expensive; only justified when alternatives genuinely don't fit |
| **Cross-category** | Buyer compares against multiple unrelated categories | Confusing; usually means positioning is unfocused |

**Decision rule:** default to subcategory. New-category claims need extra evidence and budget.

### 3. JTBD-Based Wedge Construction

A wedge is a single, specific point of distinction sharp enough to flip a buyer's default choice. The format derives from **Geoffrey Moore's positioning statement template** in *Crossing the Chasm* — "For (target customer) who (need), our (product/category) is (key benefit). Unlike (primary alternative), our product (statement of differentiation)." — extended with Dunford's alternatives terminology.

Format: **"For [ICP] who are doing [job-to-be-done], [our product] is [category] that [unique value], unlike [alternative] which [trade-off]."**

Test your wedge against three diagnostic questions:
1. **Specific?** Could a competitor paste this on their site? If yes, it's too generic.
2. **Defensible?** Can we prove the unique value with evidence?
3. **Sharp?** Does it flip a buyer who's currently leaning toward an alternative?

If any answer is no, sharpen the wedge.

### 4. Message House (Pillar Architecture)

Standard PR/comms framework. Once positioning is set, message hierarchy looks like:

```
                 [PRIMARY MESSAGE]
                       (one sentence, the wedge in plain language)
                              |
        --------------------------------------------
        |                     |                    |
  [PILLAR 1]            [PILLAR 2]           [PILLAR 3]
  (a sub-message that proves primary; usually maps to top buyer values)
       |                     |                    |
   [PROOF]              [PROOF]             [PROOF]
   (evidence: case study, data, demo, customer quote)
```

Why pillars beat features: messages stack. A buyer remembers 1 primary + 3 sub-messages. They don't remember 12 features.

### 5. Value-by-Role Variation

The 4 roles from `icp-definition` care about different things. Same product, three different value statements:

| Role | What they need to hear | Hooks |
|---|---|---|
| **Buyer (Economic)** | ROI, risk reduction, strategic alignment | Outcome metrics, vendor comparisons, business case |
| **Champion** | "This will make me look good" + visible quick wins | Career-relevant outcomes, internal launch story |
| **User (End)** | "This won't make my life harder" | Workflow ease, time saved, learning curve |

Note: Blocker (security/legal/procurement) needs *information*, not positioning. Surface their needs in trust pages, security packs, contracts — not in core messaging.

### 6. For-and-Against Wedge (vs. each named competitor)

Generic positioning fails on contact with deals. For each top-3 competitor:

```
vs. [Competitor]
WHEN buyer is: [trait]
WE WIN BECAUSE: [specific factor]
THEY ATTACK US WITH: "[expected critique]"
WE COUNTER WITH: "[response]"
THE QUESTION THAT FLIPS IT: "[discovery question]"
```

This connects positioning directly to sales reality. A positioning skill that doesn't produce this is academic.

### 7. Buyer Language Audit

Positioning works when it sounds like the buyer, not like internal jargon.

Sources of buyer language:
- Won-deal call recordings or notes
- Sales discovery transcripts
- Inbound lead form free-text
- G2 reviews of competitors (the "what I love" sections)
- Reddit / community threads about the pain
- Customer support tickets

**Rule:** every load-bearing word in positioning should appear in at least 3 buyer-source quotes, OR be flagged as "internal language — needs validation."

### 8. Confidence Rubric (evidence-base-aware)

The output template stamps `Confidence: [H/M/L]`. This maps directly to the evidence base, not vibes:

| Confidence | Evidence base | What it means downstream |
|---|---|---|
| **High** | ≥5 best-fit (rave/refer/reference) customer quotes AND every load-bearing word verified in buyer source | Wedge can be used in outbound copy, sales decks, and homepage as-is |
| **Medium** | 2–4 best-fit quotes OR 1–2 load-bearing words still flagged for testing | Use in sales motion + outbound; flag uncertain language for A/B testing |
| **Low** | 0 best-fit quotes (positioning built from interviews or inferred language) | Stamp output `#positioning-hypothesis`; plan to re-run after first 5 deals |

**Why best-fit, not just won-deal:** per Dunford, positioning hardens around the customers who *love* the product (rave, refer, are references). A customer who bought but isn't an evangelist may have bought *despite* loose positioning — using their language can dilute the wedge.

---

## Tools and Sources

### For positioning research

| Source | What it's good for | Cost |
|---|---|---|
| **Won-deal call transcripts (Gong, Chorus, Fathom)** | Real buyer language at point of decision | Paid |
| **Discovery call recordings** | Pain in buyer's words | Paid |
| **G2 / Capterra reviews of competitors** | Buyer language about pain and value | Free |
| **Reddit / Hacker News / community Slacks** | Unfiltered buyer sentiment | Free |
| **Wynter** | Test positioning copy with target ICP | Paid |
| **CXL / 5 Second Test / UsabilityHub** | Quick positioning clarity tests | Freemium |
| **Customer Advisory Board / customer interviews** | Highest-signal validation | Time-intensive |
| **Inbound lead form free-text fields** | "Why are you here?" answers | Free (your CRM) |

### For competitive positioning

| Source | What it's good for |
|---|---|
| **Competitor homepages + Wayback Machine** | What they claim, how it changes |
| **Competitor sales decks (often public on SlideShare/Speaker Deck)** | How they position in deals |
| **Their G2/Capterra reviews — "what I love" + "what I dislike"** | Their real strengths and weaknesses |
| **Their case studies** | Their best ICP and outcomes |

### For category research

| Source | What it's good for |
|---|---|
| **G2 categories + sub-categories** | Established labels |
| **Crunchbase tags** | Emerging clustering |
| **Analyst reports (Gartner / Forrester / IDC)** | Category names and sub-categories |
| **Y Combinator / accelerator companies** | Where new categories form |

### Frameworks references (read these directly if positioning quality matters)

- **April Dunford — *Obviously Awesome*** (book) and *Sales Pitch* (book)
- **Geoffrey Moore — *Crossing the Chasm*** (book) — for the positioning template
- **Lochhead, Ramadan, Peterson, Maney — *Play Bigger*** (book) — for category-design choices
- **Andy Raskin — Strategic Narrative** (essays) — Name the Enemy / Why Now / Promised Land / Obstacles / Evidence
- **Bob Moesta — *Demand-Side Sales 101*** — Four Forces of Progress (push / pull / anxiety / habit)
- **Eugene Schwartz — *Breakthrough Advertising*** — market sophistication / awareness levels

---

## Procedure

### Step 1: Identify alternatives (Dunford component 1)

List EVERY realistic alternative the buyer could choose. Include:
- Direct competitors (named)
- Indirect competitors / adjacent categories
- DIY / status quo (build internally, hire person, spreadsheets, do nothing)

**If `icp-definition` produced a Workaround Analysis (Pain step), use it directly.** Each named workaround in that analysis becomes an alternative entry in this table — and the workaround's *cost* (time / money / risk / accuracy / reputation) becomes the trade-off column. This is the cleanest path to a Dunford-style alternatives table; the workaround IS what the buyer would do without you.

**Rule:** if your "alternatives" list has fewer than 4, you haven't dug deep enough. The status quo is the most common alternative for early-stage products and is often missing from analyses.

### Step 2: List unique attributes (Dunford component 2)

Features ONLY you have, or that you have meaningfully more of than any alternative. Rule out:
- "We have integrations" → competitors do too
- "Easy to use" → unmeasurable, unprovable
- "Built by ex-[famous-company]" → not a product attribute

Each attribute should be:
- Specific (not "advanced AI")
- Verifiable (a buyer could fact-check)
- Differentiating (no alternative has it, or has it meaningfully)

### Step 3: Map attributes to value (Dunford component 3)

For each unique attribute, answer: "Why does this matter to the buyer?" — twice. Drill from feature → benefit → outcome.

| Attribute | What it does | Why buyer cares (outcome) | Proof |
|---|---|---|---|
| [feature] | [behavior] | [outcome] | [case study / data point] |

If the "why buyer cares" sounds like a feature description, drill deeper.

### Step 4: Choose best-fit ICP (Dunford component 4)

This is *not* the full ICP — it's the segment within the ICP that values the unique attributes most. Often narrower than the operational ICP.

### Step 5: Choose market category (Dunford component 5)

Apply the Play Bigger / Dunford category-design framework: existing / subcategory / new / cross.

Test the category claim against:
- **5-second test:** does the buyer recognize the category in 5 seconds?
- **Search test:** does anyone Google this term?
- **Competition test:** are there G2 categories or analyst reports for it?

Default to subcategory. Justify any new-category claim with explicit evidence.

### Step 6: Construct the wedge

Use the JTBD wedge format (Moore's positioning template extended with Dunford's alternatives). Apply the 3 diagnostic tests (specific / defensible / sharp). Iterate until all three are passing.

### Step 7: Build the message house

Primary message (1 sentence) + 3 pillars + 3 proof points per pillar. Use the alternatives + value + buyer-language-audit work to anchor.

### Step 8: Generate value-by-role variations

For Buyer / Champion / User, write 3 variations of the value prop. Same wedge, different lens.

### Step 9: Build for-and-against wedges (top 3 competitors)

For each competitor from `competitor-analysis`, fill the for-and-against template.

### Step 10: Buyer-language audit

Highlight every load-bearing word in the positioning. Verify against won-deal quotes / G2 / community sources. Flag anything internal-only.

### Step 11: Route downstream

Recommend next skill.

---

## Output Template

---

### Positioning: [Product Name]

**Prepared:** [date]
**Best-fit ICP segment:** [from icp-definition]
**Confidence:** [H/M/L]

---

**1. Alternatives Analysis**

| Alternative | Type (Direct/Indirect/Status quo) | What buyer gets | Trade-off |
|---|---|---|---|

**2. Unique Attributes**

| Attribute | Specific (not generic)? | Verifiable? | Differentiating? |
|---|---|---|---|

**3. Attribute → Value → Outcome → Proof**

| Attribute | What it does | Outcome buyer cares about | Proof |
|---|---|---|---|

**4. Best-Fit ICP for Positioning**

[1–2 sentences: narrower than operational ICP if applicable]

**5. Market Category**

| Component | Choice | Rationale |
|---|---|---|
| Frame type | Subcategory of [parent] / New / etc. | |
| Category label | | |
| 5-second test | Pass / Fail | |
| Search test | Pass / Fail | |
| G2/analyst recognition | Pass / Fail | |

**6. Wedge Statement**

```
For [ICP] who are doing [JTBD],
[product] is [category]
that [unique value],
unlike [alternative] which [trade-off].
```

Diagnostic:
- Specific? [Yes/No + reason]
- Defensible? [Yes/No + evidence]
- Sharp? [Yes/No + flip-test]

**7. Message House**

```
                  PRIMARY: [one sentence]
                          |
        ---------------------------------------
        |                |                    |
   PILLAR 1:       PILLAR 2:           PILLAR 3:
   [sub-message]   [sub-message]       [sub-message]
        |                |                    |
   PROOF:          PROOF:              PROOF:
   - [point]       - [point]           - [point]
```

**8. Value Prop by Role**

```
=== BUYER (Economic) ===
Headline: [outcome-led]
Body: [ROI / risk / strategy framing]
Proof: [business outcome]

=== CHAMPION ===
Headline: [career-relevant outcome]
Body: [internal launch story / quick win framing]
Proof: [champion success story]

=== USER (End) ===
Headline: [workflow ease]
Body: [time saved / friction removed]
Proof: [user testimonial]
```

**9. For-and-Against (per top-3 competitor)**

```
vs. [Competitor]
WHEN buyer is: [trait]
WE WIN BECAUSE: [specific factor]
THEY ATTACK US WITH: "[expected critique]"
WE COUNTER WITH: "[response]"
THE QUESTION THAT FLIPS IT: "[discovery question]"
```

**10. Buyer-Language Audit**

| Load-bearing phrase | Verified in won-deal / G2 / community? | Source quote |
|---|---|---|

**11. Recommended Next Step**

[Named follow-on skill + 1-sentence rationale]

---

## Worked Example

> *The example below uses **WorkflowDoc**, a fictional AI-native runbook authoring tool for B2B SaaS support teams. The fictional product is shared across all six function-1 skills so the worked examples interlock. The frameworks below apply to any B2B GTM context.*

**Input:**

> Product: WorkflowDoc `[hypothetical]` — AI-native runbook authoring for B2B SaaS support teams
> ICP: Series B SaaS, 100–300 emp, US, support team 5–15
> Top 3 competitors: Guru `[hypothetical]`, Stonly `[hypothetical]`, Notion `[hypothetical]` (status quo)
> Pricing: $400/seat/year `[hypothetical]`, ACV $3.2k–$6k `[hypothetical]`
> Won-deal quotes: 4 deals `[hypothetical]` worth of recorded calls + post-call notes

### Output:

> **Provenance note for the agent reading this example:** every named entity below (companies, people, dollar figures, dates, percentages, customer quotes, named tools) is `[hypothetical]` — i.e., fictional content for illustration. Inline tags appear at first mention and on key fact-bearing assertions. **In real user output, the agent must apply the same per-entity tagging discipline using `[user-provided]` / `[verified: <source>]` / `[unverified — needs check]` as appropriate** (see `## Guardrails` provenance rule). Do NOT replicate the worked example's specific-sounding-but-fictional pattern in real output without grounding tags.

---

### Positioning: WorkflowDoc

**Prepared:** 2026-04-30
**Best-fit ICP segment:** Series B SaaS, 100–300 emp, support team 5–15, support manager-led purchase, Notion not deeply embedded
**Confidence:** Medium-High (4 won-deal calls is small but high-fidelity sample)

**1. Alternatives Analysis**

| Alternative | Type | What buyer gets | Trade-off |
|---|---|---|---|
| Guru | Direct | Verified knowledge platform; strong integrations | Pricing: $25k–$80k typical ACV; AI authoring bolted on, not native; setup is 4–8 weeks |
| Stonly | Direct | Decision-tree authoring | Decision-tree format ≠ runbook prose; reactive AI; positioned for support+onboarding |
| Notion (status quo, deeply embedded) | Substitute | Already paid for; everyone uses it; cheap | Generic structure; not support-team-specific; AI is search/summarize, not authoring |
| Hire a Knowledge Manager | Status quo | Dedicated headcount writes runbooks | $80–120k salary; people-dependency; 6 months to ramp |
| Confluence + improve our process | Status quo | Already paid; no new vendor | Same authoring problem; no AI; manual update burden |
| Document360 | Direct (lighter) | KB software | Less support-team specific; weaker AI |
| Do nothing | Status quo | $0 cost | Knowledge stays in heads; senior people churn → loss; new rep ramp stays at 90 days |

**2. Unique Attributes**

| Attribute | Specific? | Verifiable? | Differentiating? |
|---|---|---|---|
| AI-native authoring (drafts from past tickets, not from prompts) | ✅ Specific to ticket-source ingestion | ✅ Demoable | ✅ No competitor does this; Guru AI requires manual prompt-then-edit |
| Native Zendesk + Intercom ingestion (auto-parse closed tickets into runbook drafts) | ✅ Named integrations | ✅ Demoable | ✅ Guru integrates but doesn't ingest tickets as draft source |
| Support-team-only pricing model ($400/seat) | ✅ Specific | ✅ Public | ✅ No competitor prices for support-team specifically |
| Auto-staleness detection (flags runbooks where outcomes diverge from current tickets) | ✅ Specific behavior | ✅ Demoable | ✅ Guru has manual verification only |

**3. Attribute → Value → Outcome → Proof**

| Attribute | What it does | Outcome buyer cares about | Proof |
|---|---|---|---|
| AI-native authoring from tickets | Drafts runbooks from real ticket history | 8x faster knowledge capture; senior support manager freed from "writing runbooks every Friday" | Stitchbox: 12 hrs/week recovered for senior manager |
| Auto-staleness detection | Flags drift between runbook and ticket reality | Reduces escalations from "runbook said X but X is wrong"; cuts CSAT-killing wrong answers | Plant: 38% drop in incorrect Tier 1 resolutions |
| Native ticket-system ingestion | No data import; auto-syncs from Zendesk/Intercom | Time-to-first-runbook = 1 day, not 4 weeks | All 4 paid pilots had first runbook within Day 2 |
| Support-team pricing | $400/seat = $4–6k ACV for typical team | Fits Series B budget; doesn't require board approval | Average sales cycle: 3.5 weeks (vs. industry 12–16 weeks for KB tools) |

**4. Best-Fit ICP for Positioning**

Series B SaaS, 100–300 emp, US, support team 5–15, with **active support pain caused by team growth** (recent headcount surge OR new VP/Director of Support OR outsourced support added in last 6 months). Support Operations Manager is the champion. Notion or Confluence is present but NOT company-wide entrenched.

**5. Market Category**

| Component | Choice | Rationale |
|---|---|---|
| Frame type | **Subcategory of existing** | "AI-native support runbook authoring" within existing "knowledge management for support" parent |
| Category label | "AI-native support runbook authoring" | |
| 5-second test | Pass | Buyers recognize "support runbooks" instantly; AI-native modifier is intuitive |
| Search test | Pass | "Runbook software for support" + "AI knowledge base for support team" both have search volume |
| G2/analyst recognition | Partial | G2 has "Knowledge Management" parent; sub-category is emerging |

We are NOT claiming a new category. We are positioning as the AI-native, support-team-specific subcategory of the established knowledge management space.

**6. Wedge Statement** `[hypothetical — entire wedge below is illustrative]`

```
For Series B SaaS support teams of 5–15 who are drowning in tribal knowledge
and watching new reps take 90+ days to ramp,
WorkflowDoc is AI-native support runbook software
that turns your closed tickets into a self-updating runbook library in days,
unlike Guru which requires 4–8 weeks of manual content migration
and a $25k+ contract built for a sales-and-support combined use case you don't have.
```

Diagnostic:
- **Specific?** Pass — names ICP precisely; cites named competitor Guru explicitly; references measurable outcome (90-day ramp; 4–8 weeks migration)
- **Defensible?** Pass — ticket-ingestion is demonstrable in <5 min; pricing comparison is public; Guru's bolt-on AI is dated 2024 in their public materials
- **Sharp?** Pass — flip-test: a Series B head of support comparing tools should leave thinking "Guru is built for someone bigger than me."

**7. Message House**

```
              PRIMARY:
   "Turn your closed tickets into a self-updating
    support runbook library — in days, not weeks."
                        |
        --------------------------------------------
        |                  |                       |
   PILLAR 1:          PILLAR 2:               PILLAR 3:
   "AI-native,        "Built for support,     "Live in days,
    not bolt-on."      not for everyone."      not weeks."
        |                  |                       |
   PROOF:              PROOF:                  PROOF:
   - 8x faster         - $400/seat (vs.        - First runbook in Day 2
     authoring vs.       $25k+ Guru ACV)         (Stitchbox, Plant,
     Guru               - Built around          Paymet, Dovere — 4/4)
   - Auto-detects       support workflow,     - Native Zendesk +
     stale runbooks     not sales              Intercom (no manual
   - From tickets,      enablement             import)
     not prompts        - Champion: Support    - 3.5 wk sales cycle
                        Ops Manager, not        avg
                        IT/CTO
```

**8. Value Prop by Role**

```
=== BUYER (Economic) — VP/Director of Support ===
Headline: Cut new-rep ramp from 90 days to 30 — without hiring a knowledge manager.
Body: Stitchbox's support team grew from 6 to 14 in six months. Their senior manager was
spending Fridays writing runbooks. Now those runbooks write themselves from closed tickets.
Result: 12 hours/week recovered, escalation rate down 22%, and CSAT held flat through
team doubling.
Proof: 4 customer references; case study showing 90% reduction in "where do I find the
runbook for X" Slack questions.

=== CHAMPION — Support Operations Manager ===
Headline: Be the person who fixed knowledge management — without a six-month implementation.
Body: Pilot live in 1 week. First 10 runbooks generated from your closed tickets in Day 2.
Demonstrable internal win in 30 days. Run a Loom for your VP at week 2 showing time saved.
Proof: Champion success: Tashia (Stitchbox Support Ops) presented results to her CXO at
day 30 — got cited as top operational improvement of Q2.

=== USER (End) — Tier 1/2 Support Specialist ===
Headline: Find the right runbook in your queue, not in 4 places.
Body: Auto-suggested runbooks appear in your Zendesk ticket sidebar. Trust them — they're
auto-flagged when they go stale. Spend less time hunting; resolve more tickets at Tier 1.
Proof: User survey at Plant: 78% of reps said "I escalate less now."
```

**9. For-and-Against**

```
vs. Guru
WHEN buyer is: Series B SaaS, support team <20, mid-market budget ($5–15k for tooling)
WE WIN BECAUSE: Guru's $25k+ ACV is built for combined sales+support at 500+ emp scale.
                Their AI authoring was bolted on in 2024 onto a 2017 architecture — manual-
                prompt-then-edit, not ticket-ingestion.
THEY ATTACK US WITH: "We have AI features too, plus 8 years of enterprise trust and
                     deeper integrations."
WE COUNTER WITH: "Guru is the right answer if you're scaling sales+support combined to 500+.
                  We're built for support teams under 20 specifically. Their AI workflow
                  starts with a prompt; ours starts with your closed tickets."
THE QUESTION THAT FLIPS IT: "Show me a runbook your team drafted from a real ticket in
                              under 5 minutes — what was the prompt your authoring
                              workflow required?"

vs. Stonly
WHEN buyer is: Wants prose runbooks (not decision trees); budget under $20k; AI-first
WE WIN BECAUSE: Decision-tree authoring is great for FAQs; runbook prose is what
                support engineers actually need. Our AI is generative-first; theirs
                is reactive.
THEY ATTACK US WITH: "Decision trees are more interactive and reduce wrong answers."
WE COUNTER WITH: "Decision trees work for customer-facing FAQs. For complex internal
                  troubleshooting, your team needs prose with branching context — which
                  we generate, and Stonly doesn't."
THE QUESTION THAT FLIPS IT: "When your most senior engineer documents a complex bug-
                              triage workflow, do they draw a flowchart, or write a
                              runbook?"

vs. Notion (status quo, deeply embedded)
WHEN buyer is: Notion already deployed company-wide; team of <8 support; tight budget
WE WIN BECAUSE: When pain is acute (rapid growth, high escalation rate, new VP of
                Support hired), generic Notion structure breaks down. We're additive,
                not replacement.
THEY ATTACK US WITH: "We already pay for Notion. Why add another tool?"
WE COUNTER WITH: "Notion is your wiki for everyone. We're the runbook system for your
                  support team. The AI authoring saves your senior person 10+ hours
                  per week — that's the case for a $500/month line item."
THE QUESTION THAT FLIPS IT: "How much of your senior support manager's week is spent
                              writing or re-writing Notion pages? What would they do
                              with that time back?"
```

**10. Buyer-Language Audit**

| Load-bearing phrase | Verified? | Source |
|---|---|---|
| "Tribal knowledge" | ✅ Yes | Stitchbox call: "all the knowledge is tribal — it's in Tashia's head"; appears in 7/14 r/CustomerSuccess threads |
| "New rep ramp" | ✅ Yes | Plant: "our problem is rep ramp — 90 days to productive"; common in CX content |
| "Self-updating runbook" | ⚠️ Internal language | Not yet validated against buyer quotes — flagged for testing |
| "Closed tickets" | ✅ Yes | Universal language in support tooling |
| "Runbook" | ✅ Yes | All 4 won-deal calls used the term |
| "Authoring" | ⚠️ Mixed | Buyer says "writing" more than "authoring" — consider adjusting public copy |

**11. Recommended Next Step**

→ `channel-strategy`. Positioning is locked. Next: identify channels where this messaging will compound (Support Driven Slack, CX Accelerator, support leader LinkedIn community), then route to `cold-email-sequence` (planned) for channel execution.

---

## Heuristics

- **Positioning is relative, not absolute.** Always defined against alternatives. Never in a vacuum.
- **The status quo is the most-chosen alternative.** "Do nothing / use spreadsheets / hire a person" wins more deals than any named competitor.
- **A great wedge is sharp enough to fail in some segments — and that's a feature.** "For everyone" = positions against no one = positions against nothing.
- **Every load-bearing word should come from a buyer quote.** Internal language is the most common failure mode.
- **Subcategory is almost always the right frame.** New-category claims need 10x the evidence and budget.
- **Pillars stack; features don't.** A buyer remembers 1 + 3. Not 12.
- **If your wedge could be pasted on a competitor's website without anyone noticing, it's not a wedge.**
- **Champion language matters more than buyer language for early-stage GTM.** Champions sell internally; buyers sign off.
- **Re-position when ICP shifts, not on a calendar.** Annual repositioning = drift; trigger-based = signal.
- **Dunford's framework includes a 6th "bonus" component — relevant trends — that can amplify positioning if (and only if) the trend has a clear, obvious link to your market.** Use sparingly. Trend-layering without that link makes positioning "cool but confusing" (Dunford's words). The "diet muffin → paleo snack" example: same product, repositioned around a trend the buyer was already living. The wrong move is claiming AI-native / agentic / web3 framing because it's hot, when the buyer doesn't yet use that vocabulary for the job.
- **Positioning is not marketing.** It shapes product roadmap, sales strategy, and CS onboarding — not just messaging copy. Best-positioning hits product priorities ("we double down on the unique attribute"), sales scripts ("we lead discovery with the flip question"), and CS playbooks ("we onboard around the value, not the feature"). Marketing is the most visible artifact, not the only consumer.

## Edge Cases

### Multi-product company
- Position each product separately. Don't unify.
- Company-level positioning is a separate exercise (corporate brand) and shouldn't drive product messaging.

### Net-new category (truly novel product)
- Subcategory framing usually still works — find the closest parent.
- True new-category requires 10–18 months of category-creation work + paid education budget.
- If user insists on new-category, push back unless: (a) clear funding for education, (b) >3 substitute alternatives identified, (c) proof points already exist.

### Two-sided marketplace / platform
- Position twice — supply side and demand side.
- They have different ICPs, different alternatives, different value props.

### PLG product
- User and Buyer often compress; position primarily for User.
- Champion role weakens (no internal-buying journey); replaced by "viral spread mechanism" if it exists.
- Wedge often emphasizes time-to-value over enterprise-grade.

### Highly regulated industries
- Add a "Trust" pillar to the message house (compliance / certifications).
- Blocker role information surfaces in pillars, not as standalone.

### Repositioning an existing brand
- Audit current positioning + customer perception (Wynter test).
- Map old → new positioning explicitly to track drift.
- Plan customer/employee comms for the change.

### Adjacent product expansion
- Don't reuse the parent product's positioning.
- Run skill fresh for the new product. Different ICP, different alternatives.

### Crowded category, undifferentiated product
- Force the alternatives analysis to be honest. If you have 0 unique attributes, the issue isn't positioning — it's product strategy. Surface this to user.
- Don't manufacture differentiation. Ship the diagnostic instead.

## Failure Modes and Recovery

| Failure mode | Symptom | Recovery |
|---|---|---|
| Positioning sounds like every competitor's | Could paste on their homepage | Force unique-attribute audit. If nothing is truly unique, surface as a product strategy problem, not a positioning problem. |
| Buyer language is internal jargon | "Synergies," "next-generation," "intelligent platform" | Pull 3 won-deal quotes and 3 G2 quotes. Rewrite using those exact words. |
| Category claim is too ambitious | Trying to create a new category without budget | Default to subcategory. New-category claims require explicit justification + capital. |
| ICP is too broad | Wedge mentions everyone | Narrow to beachhead. The wedge isn't a marketing-to-everyone tool — it's for the next 50 deals. |
| Alternatives missing status quo | Only named competitors listed | Force "do nothing / DIY / spreadsheets" as alternative. Often it's #1. |
| Value props are feature lists | "We have AI, integrations, and dashboards" | Drill: "And so what? And so what?" twice. Stop at outcome. |
| User can't articulate what they DON'T want to be | Trying to be everything to everyone | Force trade-offs. Great positioning includes "we are not for X." |
| Internal stakeholders disagree on positioning | CEO says X, sales says Y, marketing says Z | Take won-deal quotes as the tiebreaker. Buyer evidence > internal opinions. |
| Wedge fails diagnostic tests | Generic, undefendable, unsharp | Iterate. The wedge is the most important output; spend the time. |

## Pitfalls

- **Positioning by committee** — if 6 people edit the wedge, it becomes mush. Single owner.
- **Confusing tagline with positioning** — a tagline is a derivative; positioning is the underlying logic.
- **Skipping alternatives analysis** — the most common failure mode. Without alternatives, positioning floats.
- **Forgetting Champion language** — buyer language alone ignores the person actually selling internally.
- **Static positioning** — markets move; ICPs evolve; positioning must too.
- **Over-claiming category creation** — claiming "we created a new category" without the 10–18 months and budget to back it = expensive failure.
- **Listing features as value** — features describe the product; value describes the buyer's outcome.
- **Ignoring role-specific variation** — same headline for buyer + user + champion = wrong for at least 2 of them.
- **Refusing to say no** — "for everyone" positioning is for no one.
- **Layering a trend without a clear link to market** — Dunford's bonus 6th component is "relevant trends," but trend-layering without a clear link to category makes positioning "cool but confusing." Don't claim "AI-native" / "agentic" framing unless the trend genuinely reinforces the wedge AND the buyer would already use that language.
- **Treating positioning as marketing-only** — positioning shapes product roadmap, sales strategy, and CS onboarding. If only marketing owns it, the artifact gets ignored downstream.

## Verification

The positioning is complete when:
1. The wedge passes all 3 diagnostic tests (specific / defensible / sharp).
2. Every load-bearing word is verified in a buyer-source quote OR explicitly flagged for testing.
3. Best-fit ICP is narrower than the operational ICP (positioning works for the next 50 deals, not all customers).
4. Alternatives analysis includes status quo / DIY.
5. Message house has 1 primary + 3 pillars + ≥2 proofs per pillar.
6. Value-by-role variations are distinct (not minor word swaps).
7. For-and-against wedges exist for top 3 alternatives.
8. A new SDR or marketer could write outbound copy using only this document.

## Done Criteria

1. Alternatives analysis with ≥4 entries including status quo / DIY.
2. Unique attributes table — each entry specific + verifiable + differentiating.
3. Attribute → Value → Outcome → Proof table populated.
4. Best-fit ICP statement (often narrower than operational ICP).
5. Market category claim with 5-second / search / G2 tests passed.
6. Wedge statement passes 3 diagnostic tests.
7. Message house: primary + 3 pillars + ≥2 proofs/pillar.
8. Value props for Buyer / Champion / User (distinct, not minor word swaps).
9. For-and-against wedges for top 3 competitors.
10. Buyer-language audit complete; every load-bearing phrase verified or flagged.

## Eval Cases

**Eval 1 — Mature B2B SaaS with strong customer data:**
*Input:* CRM software for SMB law firms, 12 won deals with call recordings, US-only.
*Expected output:* Subcategory framing ("CRM for solo and small law practices"), wedge against Clio (their primary competitor), buyer language audit anchored in won-deal quotes, message house with 3 specific pillars, value-by-role variations distinct.

**Eval 2 — Pre-PMF with no won-deal data:**
*Input:* AI compliance automation for biotech HR teams, 0 customers, 8 buyer interviews.
*Expected output:* Positioning marked "hypothesis-only." Wedge built from interview language. Alternatives include "manual processes + audits" prominently. Plan to re-run after first 5 deals.

**Eval 3 — Repositioning request:**
*Input:* Existing product, current positioning is failing (low conversion at site). User wants to reposition for a new ICP segment.
*Expected output:* Old vs. new positioning explicitly mapped. New ICP → new alternatives → new wedge. Comms plan flagged. Champion role analysis updated.

**Eval 4 — User claims "we have no competitors":**
*Input:* Founder believes their product is in a brand-new category with no real alternatives.
*Expected output:* Skill pushes back, forces 4+ alternatives including status quo, demonstrates that "we have no competitors" is a marketing failure, not a market reality. Repositions toward subcategory framing.

## Guardrails

**On provenance (anti-fabrication — universal rule):**
- **Every named entity in output carries an inline provenance tag** at first mention and on any fact-bearing assertion. Allowed tags: `[user-provided]` / `[verified: <source-or-url>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged named entities are a contract violation. Named entities include: company names, person names, product names, direct quotes, statistics, dates, URLs, dollar figures, customer counts, named tools/sources, G2 review excerpts.
- **No silent assertion.** If you don't have a source and didn't get it from the user, default to `[unverified — needs check]` — never to a confident-looking specific (e.g., never fabricate a customer quote like "Plant said X" or invent a G2 review snippet).
- **Tool-grounding rule:** if no live research tool is available at runtime, every external-fact assertion defaults to `[unverified — needs check]`. The agent does NOT invent specifics to fill the buyer-language audit table — it tags the row and surfaces the missing input to the user.
- **Worked example warning.** The WorkflowDoc worked example contains many specific-sounding-but-fictional entities, customer quotes, and statistics — tagged `[hypothetical]` inside the example. Do NOT replicate that pattern in real user output without the provenance tags + grounding above.

**On evidence:**
- Every value claim has proof: case study, data point, customer quote, demoable feature.
- Buyer language audit is mandatory. Internal jargon is flagged or rewritten.
- Won-deal quotes have higher weight than any internal opinion.

**On scope:**
- One product per skill run. Multi-product positioning is multiple runs.
- One ICP segment per positioning. Multi-segment positioning produces multiple variations.

**On bias:**
- User's preferred narrative is hypothesis. Customer evidence overrides.
- Force trade-offs. "We are great at X but not Y" beats "we're great at everything."
- Confirmation bias check: list 3 ways the positioning could be wrong (e.g., what if our category framing is rejected by the market).

**On legality and ethics:**
- Positioning claims must be substantiable. "10x faster" without evidence is FTC-territory.
- Comparative claims (vs. competitors) must be defensible if quoted back to the competitor.
- Don't fabricate customer quotes or case studies. If the user doesn't have proof, mark the position as "to be validated."

**On freshness:**
- Date the positioning. Re-run when ICP shifts, when major competitor moves, when win rate drops materially, or every 6 months minimum.

**On scope of consumer (not just marketing):**
- Positioning shapes product roadmap, sales strategy, and CS onboarding — not just marketing copy. If the user owns only marketing, flag that positioning needs cross-functional buy-in (or at minimum visibility) for the artifact to actually take hold; otherwise the wedge will be in landing-page hero copy only and won't influence what gets built, sold, or onboarded.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Channel decisions next | `channel-strategy` | Wedge, primary message, role-specific value props, best-fit ICP segment |
| Cold email needs writing | `cold-email-sequence` (planned) | Wedge, pillars, buyer language quotes, role-specific hooks |
| LinkedIn outreach next | `linkedin-outreach` (planned) | Champion-role hooks, message pillars, Pain language |
| Discovery prep | `discovery-call-prep` (planned) | For-and-against wedges, flip questions per competitor |
| Battle cards needed | (Loop back to `competitor-analysis`) | For-and-against wedges become battle card seeds |
| Refinement after 30+ deals | `icp-refinement-loop` (planned) | Current positioning, conversion data |

**Upstream input contract (what we expect from `icp-definition`):**
- Best-fit ICP segment (often narrower than operational ICP)
- Pain-Trigger-Outcome chain in buyer language
- **Workaround Analysis** — current workaround / cost / dream state. Each workaround entry is consumed as an alternative in Step 1 (Alternatives Analysis), and the workaround's cost becomes the trade-off column. This is a load-bearing input for Dunford-style positioning.
- Champion role title + language
- Buyer/User/Blocker role profiles for value-by-role variation

---

## Push to CRM

Positioning is primarily a strategy artifact, not entity records. The output is a **shared messaging asset** that downstream skills (`cold-email-sequence`, `linkedin-outreach`) consume — so push it as one consolidated research interaction tagged for retrieval. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Positioning canvas (Dunford 5-component) | `interaction` (type: `research`) | `relevance` = full canvas; tags `#positioning #positioning-canvas` |
| Wedge statement + 3-test diagnostic | `interaction` (type: `note`) | tagged `#positioning-wedge` |
| Message house (primary + pillars + proofs) | `interaction` (type: `note`) | tagged `#message-house` |
| For-and-against wedges (one per top-3 competitor) | `interaction` (type: `note`) | One per competitor; `relevance` = wedge block; tags `#positioning-wedge #competitor:<slug>` |
| Buyer-language audit (flagged words to validate) | `interaction` (type: `note`) | tagged `#positioning #language-audit` — read by `ab-testing-messaging` (planned) downstream |

Positioning does **not** push `company` or `person` records — it operates on entities created by `icp-definition` and `competitor-analysis`.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:positioning-strategy:v2.0.0"`

### Example push (positioning canvas)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#positioning #positioning-canvas",
    "relevance": "POSITIONING CANVAS v2.0.0 (2026-04-30)\nAlternatives: Guru, Stonly, Notion, Confluence-DIY, status quo (Senior Manager + Slack)\nUnique attributes: AI-native authoring; per-support-seat pricing; ingest-from-tickets\nValue: reps resolve 25% more at Tier 1; new reps productive in 30d (was 90d)\nBest-fit ICP: Series B SaaS, 100–300 emp, support team 5–15, US (per icp-definition v2.0.0)\nMarket category: AI-powered support knowledge management (subcategory of KM)\nWedge: For Series B SaaS support teams who are losing knowledge as they scale, WorkflowDoc is AI-native runbook authoring that drafts from real tickets — unlike Guru and Notion, which require manual authoring no one has time for.\nLanguage flagged for validation: 'self-updating runbook', 'authoring' (re-test in next sales cycle).",
    "source": "skill:positioning-strategy:v2.0.0"
  }'
```

### Example push (per-competitor for-and-against wedge)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "Guru",
    "tags": "#positioning-wedge #competitor:guru",
    "relevance": "vs. Guru\nWHEN buyer is: Series B SaaS, support team <15, no existing wiki contract\nWE WIN BECAUSE: AI-native authoring; mid-market pricing\nTHEY ATTACK US WITH: \"You are unproven; we have 5,000 customers\"\nWE COUNTER WITH: \"They built pre-LLM. Their authoring is the bottleneck their customers complain about on G2.\"\nTHE QUESTION THAT FLIPS IT: \"How long does it take your senior support manager to write or update a runbook today?\"",
    "source": "skill:positioning-strategy:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #positioning`. Use cases: buyer-language audit phrases that haven't been confirmed in real buyer quotes; competitor "they attack us with" hypotheses without a real win/loss data point; value claims without a customer reference. Held for human review before being adopted into outbound copy or the message house. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

The `#unverified #review-required` scaffold is in this skill file now; the dashboard review-queue surfacing is a follow-up agentic-app task. Until the dashboard is built, the tag at least keeps inferred buyer language out of the active messaging asset.

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #positioning",
    "relevance": "Buyer-language audit row: load-bearing phrase \"self-updating runbook\" [unverified — needs check] — no buyer-source quote yet, flagged for next 5 discovery calls before adoption in outbound. Competitor counter-attack hypothesis: \"they will say we are unproven\" [unverified — needs check] — based on category pattern, not a real lost-deal quote.",
    "source": "skill:positioning-strategy:v2.0.0"
  }'
```

### When NOT to push

- ICP not yet defined (skill should have pushed back; if it didn't, do not push positioning that floats free of an ICP).
- Positioning marked "to be validated" because every claim is unproven — push as `#positioning-hypothesis` instead, and flag for re-run after first 5 deals.
