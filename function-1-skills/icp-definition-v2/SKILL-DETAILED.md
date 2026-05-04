---
name: icp-definition
description: Define and refine an Ideal Customer Profile using a 100-point weighted scoring system, Buyer/Champion/User/Blocker role mapping, Pain-Trigger-Outcome chains, and explicit anti-ICP boundaries. Produces a tiered ICP (Tier 1/2/3 + Anti-ICP) ready for lead sourcing, scoring, and qualification. Use when the user needs ICP creation, ICP refinement, qualification rules, sales/marketing alignment on target customer, or pre-outbound ICP grounding.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, icp, ideal-customer-profile, segmentation, qualification, function-1]
related_skills:
  - market-research
  - competitor-analysis
  - positioning-strategy
  - channel-strategy
  - competitive-intelligence
inputs_required:
  - product-description
  - beachhead-segment-from-market-research
  - geography
  - pricing-and-acv-range
  - sales-motion-plg-or-sales-led-or-hybrid
deliverables:
  - icp-one-pager
  - 100-point-qualification-scorecard
  - buyer-champion-user-blocker-role-map
  - pain-trigger-outcome-chain
  - tier-1-2-3-named-account-examples
  - anti-icp-boundary-definition
  - trigger-event-library
  - sdr-qualification-handoff-doc
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# ICP Definition

Produce a tiered, scored, evidence-backed Ideal Customer Profile that drives every downstream GTM decision: who to target, who to ignore, what messaging to use, what qualifies a lead, and when to disqualify. The output is a scoring rubric, a role map, a pain chain, and an anti-ICP boundary — written tightly enough that a new SDR or AI agent can apply it on day one without judgment calls.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

ICP Definition produces a **tiered, scored, evidence-backed Ideal Customer Profile** that drives every downstream GTM decision. A useful ICP is not a paragraph — it is a scoring rubric, a role map, a pain chain, and an anti-ICP boundary, written tightly enough that a new SDR or an AI agent can apply it on day one without judgment calls.

This skill exists because most "ICPs" are aspirational marketing language that doesn't survive contact with real lead lists. We produce ICPs that survive.

## When to Use

Trigger this skill when the user requests:
- ICP creation ("Define our ICP", "Who should we target?")
- ICP refinement ("Tighten our ICP based on what's actually working")
- Qualification rules for SDRs / AEs ("What makes a lead qualified?")
- Sales/marketing alignment on target customer
- Pre-outbound grounding before lead sourcing
- Anti-ICP definition ("Who should we say no to?")
- Persona work (buyer + champion + user + blocker mapping)

**Do NOT use this skill when:**
- The user wants market sizing → use `market-research`
- The user wants ongoing ICP refinement from conversion data → use `icp-refinement-loop` (planned, Tier 6)
- The user wants to score individual leads → use `lead-scoring` (planned, Tier 2)
- The user wants positioning → use `positioning-strategy`

## Inputs Required

### Parameterized inputs

| Field | Profile path | Required |
|---|---|---|
| Product description | `{{profile.product.description}}` | Yes |
| Beachhead segment (from market-research) | `{{profile.market.beachhead_segment}}` | Yes (if exists) |
| Geography | `{{profile.market.geography}}` | Yes |
| Pricing | `{{profile.product.pricing_model}}` + `{{profile.product.acv_range}}` | Yes |
| Won deals (named accounts + roles) | `{{profile.customers.won_deals}}` | Optional, **highest-value input** |
| Lost deals | `{{profile.customers.lost_deals}}` | Optional, very high-value |
| Sales motion | `{{profile.gtm.motion}}` | Yes (PLG / sales-led / hybrid) |
| Decision maker hypothesis | `{{profile.icp.dm_hypothesis}}` | Optional |
| Existing ICP doc (for refinement) | `{{profile.icp.current}}` | Optional |

### Fallback intake flow

If the customer profile is missing:

> To define a usable ICP, I need:
>
> 1. **Product** — what it does, for whom, the outcome (1–2 sentences)
> 2. **Beachhead segment** — if you've done market research, your priority segment. If not, your buyer hypothesis.
> 3. **Pricing** — model + ACV range
> 4. **Sales motion** — PLG / sales-led / hybrid
> 5. **Geography**
>
> **High-leverage optional:**
> 6. **Last 10 won deals** — company names + roles you sold to. This is the single most valuable input. With this, we extract real ICP. Without it, we're guessing.
> 7. **Last 5 lost deals** — who and why
> 8. **Anti-customers** — who you regret selling to (refunds, churn, support burden)

**If won deals exist, ask for them.** A real ICP is reverse-engineered from real revenue, not forward-engineered from theory.

### Input validation rules

- If buyer hypothesis is too broad (e.g., "VPs of Sales" with no qualifiers) → push back: "VP of Sales at a 50-person SaaS is not the same buyer as VP of Sales at a 5,000-person manufacturer. Pick a segment first."
- If user has 0 customers → flag: "ICP is hypothesis-only. Tag confidence as Low. Plan to re-run after first 10–20 customers."
- If `acv_range` doesn't match `motion` (e.g., $500 ACV + sales-led with 6 reps) → push back: "Economics don't support the motion. Resolve before defining ICP."
- If user lists 4+ separate ICPs → push back: "Multi-ICP at the start is dilution. Pick one beachhead. The others are post-PMF expansion."

---

## Frameworks Used

### 1. The 100-Point ICP Scorecard (weighted)

A house-built rubric that gives every account in scope a 0–100 fit score. Tiers are determined by score, not vibes.

| Dimension | Weight | What it measures | How to score |
|---|---|---|---|
| **Pain severity** | 25 | How acute is the problem this account experiences | 5 = nice-to-have, 15 = blocks a goal, 25 = blocks growth/breaks workflow |
| **Trigger strength** | 20 | Is something making it "now"? | 0 = no trigger, 10 = soft trigger, 20 = active trigger event in last 90 days |
| **Willingness to pay** | 20 | Can and will they pay our ACV? | 5 = below floor, 12 = within range, 20 = priority budget category |
| **Reachability** | 15 | Can we reach the decision maker? | 5 = cold-only, no community, 10 = mixed, 15 = warm intros / active community |
| **Time to value** | 10 | How fast will they see ROI? | 2 = months, 6 = weeks, 10 = days |
| **Strategic fit** | 10 | Are they a reference-class win for the next segment? | 2 = nobody-cares, 6 = useful logo, 10 = unlocks a segment |

Score totals (max 100) drive tiers. **Cutoffs:**

- **Tier 1 (Primary ICP):** 75+ — full sales motion
- **Tier 2 (Secondary):** 55–74 — automated/lighter touch
- **Tier 3 (Stretch):** 40–54 — opportunistic only
- **Anti-ICP:** <40 — do not pursue

**Calibration note:** these weights are starting defaults. Tune based on what your data shows after first 30–50 deals. The framework matters more than the numbers. *(Note: this is not a canonical industry framework like MEDDIC; it's a house rubric. MEDDIC/MEDDPICC are deal-qualification frameworks distinct from this account-fit scorecard.)*

### 2. Buyer / Champion / User / Blocker Role Map

The standard "buyer + user" two-role model misses two roles that win and lose deals. We use four. (This four-role view echoes Miller-Heiman's Strategic Selling roles — Economic Buyer / Technical Buyer / User Buyer / Coach — and overlaps with MEDDIC's Champion + Economic Buyer concepts.)

| Role | Who they are | What they care about | What kills the deal |
|---|---|---|---|
| **Buyer (Economic)** | Signs the contract / approves budget | ROI, risk, strategic alignment | Cost, vendor risk, competing priorities |
| **Champion** | Internal advocate driving the purchase | Career outcome from the project succeeding | Lack of visible quick win; champion leaves |
| **User (End)** | Day-to-day operator of the product | Personal time, workflow ease, learning curve | Adoption fail; tool is harder than status quo |
| **Blocker** | Has veto or delay power (Security/IT/Procurement/Legal) | Compliance, vendor management, risk | Triggered late; gates not met |

For each ICP segment, fill all four. **Skipping the Blocker role is the #1 reason mid-market+ deals stall.**

### 3. Pain-Trigger-Outcome Chain (with Workaround Analysis)

A useful ICP has four connected statements (echoes Bosworth's Pain Chain from *Solution Selling*; popularized as "trigger event selling" by Craig Elias and Aaron Ross):

- **Pain:** the underlying chronic problem (always present)
- **Workaround:** what they do today to limp through it — and what that workaround costs them
- **Trigger:** the event that turns chronic pain into acute, "fix this now" pain
- **Outcome:** what the buyer's life looks like with the problem solved (in their words, not yours)

The Workaround sub-component is load-bearing for two reasons: (1) the workaround IS a competitive alternative in Dunford's sense (`positioning-strategy` and `competitor-analysis` consume this directly — see Linked Skills); and (2) the workaround's cost is the dollar / risk / time number that justifies the deal.

Format:

> **Pain:** [chronic problem description, in buyer language]
> **Current Workaround:** [what they do today — DIY / spreadsheet / hire someone / accept it / ignore it]
> **Cost of Workaround:** [time / money / risk / accuracy / reputation — quantified where possible]
> **Triggers:** [3–5 observable events that make this acute, each typed as `need` or `buy`]
> **Outcome (90-day dream state):** [what success looks like, in measurable terms]

Without triggers, you have an audience. With triggers + a documented workaround cost, you have an ICP that's outboundable AND justifiable to procurement.

### 4. Anti-ICP Definition (Boundary by Negation)

A great ICP says no as clearly as it says yes. Anti-ICP has four lenses:

- **Anti-firmographic:** wrong size, wrong stage, wrong industry
- **Anti-pain:** the pain is real but the cost of solving it is too low to fund the deal
- **Anti-buyer:** wrong role making the decision (e.g., IT-led when product is for marketing)
- **Anti-trigger:** absence of a trigger; not enough urgency

For each, state the rule and rationale.

### 5. Trigger Event Library (Need-Triggers vs. Buy-Triggers)

Triggers are observable, datable, and outboundable. Each trigger is one of two types:

- **`Type: need`** — pain becomes acute (the buyer now hurts enough to start looking)
- **`Type: buy`** — budget or process opens (the buyer was already in pain but a buying-window opens)

A high-fit account with a need-trigger but no buy-trigger nearby is a nurture, not an active outbound target. The split keeps SDRs from pitching into closed budget cycles. Score:

| Trigger type | Examples | Type | Strength |
|---|---|---|---|
| **Funding** | Series A/B/C raised <90 days ago | buy | High (budget unlock) |
| **Hiring** | Specific role posted (e.g., "VP of Support") | need | Medium-High |
| **Leadership change** | New CMO/CRO/CFO in <120 days | need | High (new initiatives) |
| **Tech change** | Stack switch detectable via BuiltWith | need | Medium |
| **Public commitment** | Earnings call quote, blog post, conference talk | need | Medium |
| **Competitor adopted** | A peer competitor adopted the category | need | Medium |
| **Compliance / regulatory** | New rule taking effect | need + buy | High in regulated industries |
| **Growth signal** | Headcount up 30%+ YoY, new offices | need | Medium |
| **Pain signal** | Public Glassdoor/Reddit complaints | need | Medium-High when targeted |
| **Buying window** | Budget refresh cycle / quarterly close / annual audit / migration moment / post-fundraise spend window | buy | High when timing aligns |

Output: 5–10 specific triggers for the ICP, each tagged `Type` + `Strength` + `Source`. **At least one buy-trigger required** — without it, the ICP is "interesting target" not "outboundable target."

### 6. Fit × Readiness 2x2 (tier sanity check)

A 2x2 sanity-check, drawing on the Pain / Power / Vision logic from Mike Bosworth's *Solution Selling* (the **Pain Chain** and the 9-block latent-pain → admitted-pain → vision-of-solution × power matrix). This is a simplified two-axis adaptation, not Bosworth's original grid:

|  | High Readiness | Low Readiness |
|---|---|---|
| **High Fit** | Tier 1 — full motion now | Tier 1 nurture — fit but no trigger |
| **Low Fit** | Tier 3 — opportunistic, watch | Anti-ICP |

Fit = scorecard pain + WTP + reachability. Readiness = scorecard trigger strength.

For deeper buyer-readiness work, use Bosworth's full 9-block (latent / admitted / vision × buyer / decision-maker / influencer) on opportunities already qualified by this 2x2.

### 7. Confidence Rubric (sample-size-aware)

The output template stamps `Confidence: [H/M/L]`. This is not a vibe — it maps directly to the evidence base. Use this rubric exactly:

| Confidence | Evidence base | What it means downstream |
|---|---|---|
| **High** | ≥30 won deals OR ≥30 buyer interviews | ICP is data-backed; downstream skills can act on it without hedging |
| **Medium** | 10–29 won deals or interviews | Pattern is real but small; positioning + outbound can run, but plan to re-run after another 20 deals |
| **Low** | 1–9 won deals or interviews | Working hypothesis with directional signal; tag downstream artifacts `#icp-low-confidence` |
| **Hypothesis-only** | 0 customers and 0 interviews | Theory only; recommend 8–10 buyer interviews before acting |

**Calibration note:** if entering a wholly new industry where the team has no domain knowledge, raise the bar — treat <100 conversations as Medium-at-best. (Reddit thread on the source article: "you can not talk to 5 people and have an ICP.")

---

## Tools and Sources

### For ICP discovery (when starting from theory)

| Source | What it's good for | Cost |
|---|---|---|
| **Internal CRM (won deals analysis)** | The single best source — what actually closed | Free |
| **Apollo / ZoomInfo** | Firmographic targeting, account discovery | Paid |
| **Crunchbase** | Stage, funding, growth signals | Freemium |
| **LinkedIn Sales Navigator** | Role + company filtering | Paid |
| **BuiltWith / Wappalyzer** | Tech-stack-based ICP filters | Freemium |
| **G2 reviews of category** | Who's already buying similar tools (firmographic patterns) | Free |

### For ICP validation (interviews + signal)

| Source | What it's good for | Cost |
|---|---|---|
| **Userinterviews.com / Respondent** | Recruit B2B interviewees ($75–200/interview) | Paid |
| **Internal customer calls** | Highest-signal source | Free |
| **Wynter** | Test ICP messaging with target buyers | Paid |
| **Customer support tickets** | Reveal real pain, real users (not just buyers) | Free |
| **NPS / churn interviews** | Define anti-ICP by who churned | Free |

### Validation techniques — pick the right one for the question

| Technique | Use when | Output |
|---|---|---|
| **Concept test (survey)** | You have a profile hypothesis and want directional read on relevance/clarity from many people fast | Aggregate scores on "this describes me / this is a real pain" + open-text reasons |
| **Preference test** | You have 2+ messaging variants and need to know which one resonates with the persona | Forced-choice ranking + reasoning |
| **1:1 buyer interview (30–45 min)** | You need depth on workaround, cost, dream state, buying triggers, decision dynamics | Verbatim quotes feeding Pain-Trigger-Outcome chain (highest signal) |
| **Panel recruitment (e.g., Userinterviews / Respondent)** | You don't yet have warm contacts in the persona; need to recruit cold | Source of interviewees for the techniques above |
| **Win-loss interview** | You have closed deals (won + lost) and want to surface the real why behind each | Patterns that override stated ICP; informs Anti-ICP boundaries directly |

### For trigger detection

| Source | What it's good for |
|---|---|
| **Crunchbase** | Funding events |
| **LinkedIn (job postings + leadership posts)** | Hiring + leadership change |
| **BuiltWith / Wappalyzer** | Tech adoption events |
| **Visualping** | Website / pricing changes |
| **Common Room / Default / RB2B** | Aggregate intent + signals |
| **Bombora / G2 buyer intent** | Account-level intent | Paid |

**Source-priority rule for ICP work:** internal won-deal data > customer interviews > trigger detection tools > firmographic databases > public intent data.

---

## Procedure

### Step 1: Anchor in evidence

If won deals exist, start there. Pull last 10–20 won deals. For each, capture:
- Company (name, size, industry, stage, geography)
- Tech stack (if known)
- Decision maker role + title
- Champion role + title
- Pain in their words
- Trigger that brought them in
- Time to close
- ACV
- Reference willingness

If no won deals exist, mark all output as "hypothesis-only" and skip to Step 2 with reduced confidence.

### Step 2: Define the buyer firmographic

Based on Step 1 evidence (or beachhead segment from market-research):
- Industry / vertical (specific, not "B2B SaaS")
- Company size range (employee count, revenue, or stage)
- Geography
- Tech stack signals (if relevant)
- Operating model (PLG company / sales-led / etc.)

**Test:** the firmographic should produce 500–5,000 candidate accounts in your TAM. Wider = unfocused; narrower = unscalable.

### Step 3: Define the four roles (Buyer / Champion / User / Blocker)

For each role, fill: title patterns, seniority, what they care about, what kills the deal, where to find them. Don't skip Blocker.

### Step 4: Build the Pain-Trigger-Outcome chain

In buyer language. Validate against won-deal evidence — every Pain claim should map to actual quotes from real customers.

### Step 5: Build the trigger library

5–10 specific, observable triggers. Each tagged with Strength + Source.

### Step 6: Run the 100-point scorecard

Apply the rubric to:
- 3 best-fit accounts (should score 80+)
- 3 mid-fit accounts (should score 55–74)
- 3 anti-ICP accounts (should score <40)

If scores don't separate cleanly, the rubric is wrong — re-tune weights.

### Step 7: Define Anti-ICP

4 boundaries (firmographic, pain, buyer, trigger). Each with rule and rationale.

### Step 8: Generate Tier 1 / 2 / 3 examples

3 named accounts per tier. With score breakdown showing how each landed in its tier. Real accounts if the user has them; fictional but specific if not.

### Step 9: Produce the ICP one-pager

Single document, used by SDRs/AEs/marketing. Use template below.

### Step 10: Produce the qualification handoff doc

What an SDR needs to know to qualify a lead in 2 minutes. Includes scorecard, top 3 disqualifiers, top 3 trigger questions.

### Step 11: Route downstream

Recommend next skill.

---

## Output Template

---

### ICP: [Product Name]

**Prepared:** [date]
**Beachhead segment:** [from market-research or defined here]
**Geography:** [scope]
**Confidence:** [H/M/L based on evidence available]

---

**1. Firmographic Definition**

| Dimension | Value |
|---|---|
| Industry | [specific] |
| Sub-vertical | [if applicable] |
| Size (employees) | [range] |
| Size (revenue or ACV proxy) | [range] |
| Stage | [Series A/B/C/etc., or revenue band] |
| Geography | [list] |
| Tech stack signals | [optional] |
| Operating model | [PLG / sales-led / etc.] |

Estimated account count in scope: [#]

**2. Roles (Buyer / Champion / User / Blocker)**

```
=== BUYER (Economic) ===
Title patterns: [e.g., VP of [function], CXO]
Seniority: [VP+ / Director+ / etc.]
Cares about: [3 priorities, in their language]
Kills the deal when: [3 risks]
Where to find: [LinkedIn filter / community / event]

=== CHAMPION ===
Title patterns: [e.g., Director of Operations]
Seniority: [Director / Manager / IC]
Cares about: [career outcome from this project]
Kills the deal when: [no quick win, gets pulled to other priorities]
Where to find: [LinkedIn / community]

=== USER (End) ===
Title patterns: [e.g., Operations Analyst]
Cares about: [day-to-day workflow]
Kills adoption when: [tool is harder than current way]
How to enable: [training, onboarding, docs]

=== BLOCKER ===
Title patterns: [e.g., IT Security, Legal, Procurement]
Cares about: [SOC 2, data residency, vendor management]
Kills the deal when: [triggered too late, gates not met]
How to disarm: [what to prepare in advance]
```

**3. Pain-Trigger-Outcome (with Workaround Analysis)**

```
PAIN (chronic):
[2–3 sentences in buyer language. What hurts.]

CURRENT WORKAROUND:
[What they do today to limp through it — DIY / spreadsheet / hire someone / accept it / ignore it]

COST OF WORKAROUND:
- Time: [hours/week or days/quarter]
- Money: [direct $ + opportunity cost]
- Risk: [error rate, security exposure, churn risk]
- Accuracy: [what slips through]
- Reputation: [internal trust loss, external CSAT/NPS impact]

TRIGGERS (acute, in last 90 days):
1. [observable event]  — Type: need/buy
2. [observable event]  — Type: need/buy
3. [observable event]  — Type: need/buy
4. [observable event]  — Type: need/buy
5. [observable event]  — Type: need/buy

OUTCOME (90-day dream state, in buyer language):
[What does life look like in 90 days. Measurable.]
```

**4. Trigger Library (Outboundable)**

| Trigger | Type (need/buy) | Strength | Where to detect | How to detect |
|---|---|---|---|---|
| | need/buy | H/M/L | [tool] | [query/filter] |

At least one row must be `Type: buy` (a buying-window trigger).

**5. 100-Point Scorecard**

| Dimension | Weight | Score (0–25/20/etc.) for [account] |
|---|---|---|
| Pain severity | /25 | |
| Trigger strength | /20 | |
| Willingness to pay | /20 | |
| Reachability | /15 | |
| Time to value | /10 | |
| Strategic fit | /10 | |
| **TOTAL** | /100 | |

**Tier cutoffs:**
- Tier 1: 75+
- Tier 2: 55–74
- Tier 3: 40–54
- Anti-ICP: <40

**6. Tier Examples**

| Tier | Account | Score breakdown | Why |
|---|---|---|---|
| Tier 1 | [name] | P:25 T:20 W:20 R:12 V:8 S:8 = 93 | [rationale] |
| Tier 1 | [name] | ... | ... |
| Tier 1 | [name] | ... | ... |
| Tier 2 | [name] | ... | ... |
| Tier 2 | [name] | ... | ... |
| Tier 2 | [name] | ... | ... |
| Tier 3 | [name] | ... | ... |
| Anti-ICP | [name] | P:5 T:0 W:5 R:5 V:2 S:2 = 19 | [why we say no] |

**7. Anti-ICP Boundaries**

| Lens | Rule | Rationale |
|---|---|---|
| Firmographic | Do not pursue [X] | [reason] |
| Pain | Do not pursue when pain is [Y] | [reason] |
| Buyer | Do not pursue when [Z] is the decision maker | [reason] |
| Trigger | Do not pursue without [trigger]; nurture only | [reason] |

**8. SDR Qualification Handoff**

```
=== QUICK QUALIFY (2 minutes) ===

Tier 1 signals (any 2 = Tier 1):
- [signal]
- [signal]
- [signal]

Tier 2 signals (any 2 = Tier 2):
- [signal]
- [signal]

Disqualify immediately if:
- [hard no #1]
- [hard no #2]
- [hard no #3]

Discovery questions (top 3):
1. [question that surfaces pain]
2. [question that confirms trigger]
3. [question that reveals buyer/champion]
```

**9. Recommended Next Step**

[Named follow-on skill + 1-sentence rationale]

---

## Worked Example

> *The example below uses **WorkflowDoc**, a fictional AI-native runbook authoring tool for B2B SaaS support teams. The fictional product is shared across all six function-1 skills so the worked examples interlock. The frameworks below apply to any B2B GTM context — substitute the firmographic, role titles, and pain language for your own.*

**Input:**

> Product: WorkflowDoc `[hypothetical]` — AI-native runbook authoring for B2B SaaS support teams
> Beachhead: Series B SaaS, 100–300 emp, support team 5–15 people, US
> Pricing: $400/seat/year `[hypothetical]`, ACV $3.2k–$6k `[hypothetical]`
> Sales motion: PLG → SLG (self-serve trial → sales-assist for >10 seats)
> Won deals: 4 paid pilots — Plant `[hypothetical]`, Stitchbox `[hypothetical]`, Paymet `[hypothetical]`, Dovere `[hypothetical]`
> Lost deals: 2 — lost to Notion-as-status-quo at Pixly `[hypothetical]`; lost to Confluence DIY at Glan `[hypothetical]`

### Output:

> **Provenance note for the agent reading this example:** every named entity below (companies, people, dollar figures, dates, percentages, customer counts, named tools, direct quotes) is `[hypothetical]` — i.e., fictional content for illustration. Inline tags appear at first mention and on key fact-bearing assertions, then taper for readability. **In real user output, the agent must apply the same per-entity tagging discipline using `[user-provided]` / `[verified: <source>]` / `[unverified — needs check]` as appropriate** (see `## Guardrails` provenance rule). Do NOT replicate the worked example's specific-sounding-but-fictional pattern in real output without grounding tags.

---

### ICP: WorkflowDoc

**Prepared:** 2026-04-30
**Beachhead segment:** Series B SaaS, 100–300 emp, US, support team 5–15
**Confidence:** Medium (4 wins is small but consistent pattern)

---

**1. Firmographic Definition**

| Dimension | Value |
|---|---|
| Industry | B2B SaaS |
| Sub-vertical | Workflow / DevTools / Vertical SaaS |
| Size (employees) | 100–300 |
| Size (revenue) | $5M–$30M ARR |
| Stage | Series B (some late Series A; some early Series C) |
| Geography | US, English-speaking |
| Tech stack signals | Zendesk OR Intercom for support; Slack; Notion or Confluence as wiki |
| Operating model | Sales-led OR product-led with a customer success / support team of 5+ |

Estimated account count: ~1,800 `[hypothetical]` (Crunchbase Series B SaaS, US, 100–300 emp, last 24 months funded)

**2. Roles**

```
=== BUYER (Economic) ===
Title patterns: VP of Customer Support, VP of Customer Experience, Director of Support
Seniority: VP or Director with budget authority $5k–$50k
Cares about:
  - Reducing escalation rate and time-to-resolution
  - Onboarding new support reps faster (their reps churn)
  - Showing CS leadership / CEO that they're modernizing
Kills the deal when:
  - Procurement adds 6 weeks to the timeline
  - "We already pay for Notion / Confluence company-wide"
  - No clear ROI in 90 days
Where to find: LinkedIn Sales Nav (Title + Company filter); Support Driven Slack community; Customer Service Festival; HubSpot's Service Hub user community

=== CHAMPION ===
Title patterns: Support Operations Manager, Senior Support Manager, Knowledge Manager
Seniority: Manager / Senior IC
Cares about: This project = their visible career bet. They want a launchable internal win in 6–8 weeks.
Kills the deal when: The pilot drags >60 days; champion's manager reorgs them onto another project.
Where to find: LinkedIn (title-based); Support Driven Slack; CX Accelerator community

=== USER (End) ===
Title patterns: Support Specialist, Tier 1/2 Support Engineer, Customer Success Specialist
Cares about:
  - Resolving tickets faster (their personal SLA metric)
  - Not having to ask their manager every escalation
  - Trusting that runbook info is current
Kills adoption when: Authoring a runbook takes longer than just doing the work and explaining once.

=== BLOCKER ===
Title patterns: IT Security, Compliance Officer (in regulated SaaS); Procurement (>$10k purchases)
Cares about: SOC 2 Type II; data residency; PII handling (support tickets often contain PII)
Kills the deal when: Triggered late in process; SOC 2 questionnaire arrives at week 4 of an 8-week pilot
How to disarm: Lead with security pack; pre-built SOC 2 docs; have AE prepped on data flow questions
```

**3. Pain-Trigger-Outcome (with Workaround Analysis)**

```
PAIN (chronic):
"Our team's knowledge lives in 8 different places — old Slack threads, stale Confluence pages,
the Senior Support Manager's head — and our newer reps escalate things they shouldn't because
they can't find or trust what's there. Writing or updating runbooks is always 'next week.'"

CURRENT WORKAROUND:
Senior reps answer the same 30 questions in Slack each week; new reps DM their manager;
the team intermittently writes Confluence pages that are stale within 60 days. A few teams
have hired an outsourced VA at $40/hr to "keep the wiki current" — adoption is uneven.

COST OF WORKAROUND:
- Time: Senior reps spend ~6 hrs/week answering repeat questions in Slack (~$45k/yr fully loaded)
- Money: $35–60k/yr if a VA path is taken; or 1 unhired Tier 2 because Senior reps can't graduate to harder work
- Risk: New-rep escalations leak unverified workarounds to customers; escalation rate climbs
- Accuracy: ~40% of Confluence pages stale by 90 days (sampled in pilot interviews)
- Reputation: Internal — "support team is the bottleneck" perception with engineering; external — CSAT dips during onboarding-heavy quarters

TRIGGERS (acute, last 90 days):
1. Support team headcount grew >30% in last 6 months (overwhelm tipping point)  — Type: need
2. A high-profile escalation that "should have been resolved at Tier 1"  — Type: need
3. New VP of Support hired in last 4 months (will modernize)  — Type: need
4. CSAT or first-response-time SLA missed in last quarter  — Type: need
5. Outsourced/offshore support added — knowledge transfer crisis  — Type: need
6. Series B funded in last 90 days (budget unlocked for support tooling)  — Type: buy
7. Annual budget refresh window (Q4 planning for next year's CS stack)  — Type: buy

OUTCOME (90-day dream state):
"Our reps resolve 25% more tickets at Tier 1; new reps are productive in 30 days instead of 90;
our Senior Manager spends time on strategic work instead of answering Slack questions all day.
Runbooks are current because they update themselves from real tickets."
```

**4. Trigger Library**

| Trigger | Type | Strength | Where to detect | How |
|---|---|---|---|---|
| Series B funding <90 days ago | buy | H | Crunchbase / Apollo | Filter: round_type=B, date<90d |
| Annual CS-stack budget refresh window (Q4 planning) | buy | M | Patterns from won deals; ask in discovery | "When does your Support tooling budget refresh?" |
| Posted "VP/Director of Support" in last 90 days | need | H | LinkedIn job postings + Crunchbase | Title search |
| Headcount up 30%+ YoY | need | M | LinkedIn Sales Nav (employee growth filter) | Filter |
| Hiring "Support Operations" role | need | H | LinkedIn job postings | Title search |
| Public CSAT/CX content (blog / earnings) | need | M | Manual + Visualping | Track CS leader's LinkedIn posts |
| Adopted Zendesk or Intercom <12 months | need | M | BuiltWith | Detection date filter |
| Senior Support hire churn (rapid turnover) | need | M | LinkedIn org chart deltas | Sales Nav filter |
| New SOC 2 attestation | need | M | Public trust pages | Visualping on /security pages |

**5. 100-Point Scorecard**

| Dimension | Weight | Score for "Stitchbox" `[hypothetical]` (Tier 1 won deal) |
|---|---|---|
| Pain severity | /25 | 22 — outsourced support added; knowledge transfer was breaking |
| Trigger strength | /20 | 18 — Series B 60 days prior; new VP of Support |
| Willingness to pay | /20 | 18 — $4.8k ACV deal closed in 3 weeks |
| Reachability | /15 | 12 — VP of Support active in Support Driven community |
| Time to value | /10 | 8 — 1st runbook generated in week 1 |
| Strategic fit | /10 | 9 — strong reference, similar to 12 prospects |
| **TOTAL** | /100 | **87** |

**6. Tier Examples**

| Tier | Account | Score | Why |
|---|---|---|---|
| Tier 1 | Stitchbox (won) | 87 | All pillars high; reference-class |
| Tier 1 | Plant (won) | 81 | Slightly lower trigger but strong pain |
| Tier 1 | Linear (hypothetical match) | 84 (est) | Series B/C dev tools, scaled support |
| Tier 2 | Pixly (lost) | 62 | Notion deeply embedded → Reachability 8/15, Pain 18/25 |
| Tier 2 | Glan (lost) | 58 | Pain real but Confluence DIY culture; Trigger 8/20 |
| Tier 2 | [Generic Series A SaaS, 60 emp, support of 4] | 60 (typical) | ACV constrained; Pain real but Strategic fit lower |
| Tier 3 | [Series A SaaS, support of 2–3] | 48 (typical) | ACV too low for sales motion; PLG only |
| Anti-ICP | [Enterprise 2,000 emp, mature support tooling already] | 28 | Sales cycle too long; Reachability 5/15; competing tools entrenched |

**7. Anti-ICP Boundaries**

| Lens | Rule | Rationale |
|---|---|---|
| Firmographic | Do not pursue companies <50 emp | Support team <3 → ACV too low ($1.2k) |
| Firmographic | Do not pursue companies >500 emp | Sales cycle 6mo+; we're not built for it yet |
| Pain | Do not pursue if support is fully outsourced (no internal team) | They don't author; vendor authors |
| Buyer | Do not pursue when IT/Eng leads buying decision | Wrong language; they'll buy Notion/Confluence |
| Trigger | No trigger event identified → nurture only | Spending sales time on Tier 1-fit-but-not-ready burns CAC |

**8. SDR Qualification Handoff**

```
=== QUICK QUALIFY (2 minutes) ===

Tier 1 signals (any 2 = Tier 1):
- Series B funded <90 days ago
- Hired "VP/Director of Support" in last 90 days
- Support team grew 30%+ in last 6 months OR added outsourced/offshore support
- Buyer mentions "knowledge management" or "runbooks" unprompted

Tier 2 signals (any 2 = Tier 2):
- Series A or C SaaS, 100–500 emp
- Support team 5–15 with growth signals
- Champion identified (Support Ops Manager) but no buyer engagement yet

Disqualify immediately if:
- Support is 100% outsourced
- IT/Eng is the primary buyer (wrong buyer = we lose to wikis)
- Company has >500 emp and entrenched Guru/Stonly contract
- Ticket volume <500/month (pain not severe enough)

Discovery questions:
1. "How long does it currently take a new support rep to be productive at Tier 1?"
   → Answer 60+ days = pain is real
2. "When did you last update your top-10 runbooks? When did you last write a new one?"
   → ">3 months ago" = trigger candidate
3. "Who would own this internally — your Support Ops lead, or someone in IT?"
   → Support Ops = good champion; IT = wrong buyer; redirect or disqualify
```

**9. Recommended Next Step**

→ `positioning-strategy`. ICP is now sharp. Next: lock the wedge against Guru/Notion specifically for this ICP, then route to `lead-sourcing-apollo` (planned) with the firmographic + trigger queries baked in.

---

## Heuristics

- **Won deals beat opinions.** If your won deals contradict the user's stated ICP, the won deals are right.
- **A good ICP says no more often than yes.** If everyone is "kind of in" the ICP, the ICP is too loose.
- **Triggers are the difference between an audience and an ICP.** Without triggers, you have demographics — not buyers.
- **Champion role is the most underrated.** Most lost deals are champion failures, not buyer failures.
- **Blocker role is the most underrated for mid-market+ deals.** Surface security/legal/procurement early, not in week 6.
- **The User (end-user) role is where adoption-driven churn comes from.** Buyer can love you while User refuses to use you.
- **First ICP from won deals = high signal, narrow scope.** Don't widen until you have 30+ deals.
- **Rejection makes ICP useful.** A real Anti-ICP saves more money than a great Tier 1 makes.
- **Score cutoffs matter more than weights.** Calibrate cutoffs against actual won-rate by score band.
- **Don't ICP what you can't reach.** A perfect-fit segment with no inroads is a Tier 3 at best.
- **Validation isn't "did they say yes" — it's "did they lean in?"** In a discovery / concept call, track engagement signals: did they ask follow-ups, set a next meeting unprompted, share with a colleague, or name the pain in their own words before you suggested it? A polite no beats a vague yes. A vague yes is the most expensive signal in B2B.
- **Internal pain assumptions are usually wrong.** What marketing thinks the pain is and what the buyer says hurts diverge often. Default to buyer language, not internal language, in the Pain-Trigger-Outcome chain.

## Edge Cases

### No customers yet (ICP is hypothesis-only)
- Mark all output as "hypothesis." Confidence cap: Low.
- Heavily weight buyer interviews (8–10 minimum) over theory.
- Plan re-run after first 10 customers.
- Use trigger library more conservatively — assume softer signals.

### Multiple distinct customer segments at PMF
- Pick ONE for the ICP. Document the others as "Tier 1 candidates after expansion."
- Multi-ICP at the start is dilution.
- If user resists, run the ICP for each segment as separate documents.

### PLG / self-serve product
- Buyer = User more often. Compress roles.
- Trigger detection shifts toward usage signals (signups, activation, expansion).
- Champion may emerge after activation (power user → champion).
- Anti-ICP defined more by "won't activate" than "won't buy."

### Marketplaces / two-sided products
- Two ICPs: supply-side and demand-side.
- Run skill twice. Separate documents.
- Critical: which side is the chicken-and-egg priority? Pick one for the active ICP.

### Regulated industries (healthcare, finance, defense)
- Blocker role weight increases significantly.
- Compliance-as-trigger is real (SOX, HIPAA, FedRAMP timelines).
- Sales cycles are 2–4x longer; plan ACV thresholds accordingly.

### International / multi-language
- Different ICP per language market. Don't unify.
- Reachability dimension scores lower in markets without strong communities.
- Consider localization burden in Time to Value.

### High-ACV enterprise (>$100k ACV)
- Add 2 dimensions to scorecard: champion strength (5pt) + executive sponsorship (5pt).
- Trigger weighting decreases (enterprise buyers move slowly).
- Multi-threading is required — one champion isn't enough.

## Failure Modes and Recovery

| Failure mode | Symptom | Recovery |
|---|---|---|
| ICP includes everyone | Firmographic produces 50,000+ accounts | Add tighter qualifiers; force triggers; segment by sub-vertical |
| ICP includes no one | Firmographic produces <100 accounts | Loosen one filter; usually size range or tech stack signal is too tight |
| Tiers don't separate | Scorecard scores cluster | Re-tune weights; rubric is broken if all accounts score 60–70 |
| Won deals contradict stated ICP | User claims ICP is X, won deals are Y | Trust the data. Re-run with won-deal evidence as primary input. Note discrepancy. |
| User can't name a champion | "The buyer drives the deal alone" | Push back. In B2B, no champion = stalled deal. Identify who *would* be the champion. |
| Anti-ICP is missing or vague | "We'll work with anyone good" | Force boundaries. Pick 4 disqualifiers. Without boundaries, sales wastes capacity. |
| User wants to skip Blocker role | "Procurement isn't a problem for us" | Push back if ACV >$10k or if industry is regulated. Surface Blocker now or fight it later. |
| Trigger library has no specifics | "We're triggered when they need us" | Force concrete, datable, observable events. Re-run if vague. |
| Customer interviews unavailable | User won't or can't do them | Substitute won-deal CRM analysis + community thread mining + support ticket review. Cap confidence at Medium. |

## Pitfalls

- **Aspirational ICP** — describing the customer you wish you had vs. the one you actually win.
- **One-role ICP** — only naming the buyer; missing champion, user, blocker.
- **Pain without trigger** — buyer hurts but isn't acting; pain alone doesn't fund a deal.
- **Skipping Anti-ICP** — leaves sales chasing fit-but-misqualified accounts.
- **Generic firmographic** — "B2B SaaS" is not a firmographic; "Series B SaaS, 100–300 emp, US, with Zendesk + 5+ support staff" is.
- **Static ICP** — ICP must be re-run every 6 months minimum, faster if motion changes.
- **Sample size of 1 deal** — one big customer is not an ICP; it's an outlier until proven.
- **Confusing logo desire with fit** — "we want [BigCo] as a customer" is logo lust, not ICP work.

## Verification

The ICP is complete and useful when:
1. SDR can qualify a lead in 2 minutes using the handoff doc.
2. Marketing can write outbound sequences using Pain/Trigger/Outcome statements directly.
3. Anti-ICP is specific enough that 3 disqualifiers can be stated without thinking.
4. 100-point scorecard differentiates won from lost deals when applied retroactively.
5. All 4 roles (Buyer / Champion / User / Blocker) are filled.
6. Trigger library has 5+ outboundable triggers with named detection sources.
7. The user can paste this ICP into a sales playbook and use it on day one.

## Done Criteria

1. Firmographic produces 500–5,000 candidate accounts in TAM (not wider, not narrower).
2. Buyer / Champion / User / Blocker all four filled with title patterns, what-they-care-about, and detection method.
3. Pain-Trigger-Outcome chain written in buyer language; every Pain claim mapped to real customer quote (or flagged hypothesis). **Workaround Analysis populated** (current workaround / cost across the 5 axes / 90-day dream state).
4. Trigger library has 5–10 entries, each tagged `Type` (need/buy) + Strength + named detection source. **At least one row is `Type: buy`.**
5. 100-pt scorecard applied to ≥9 accounts (3 best-fit, 3 mid, 3 anti). Tiers separate cleanly.
6. Anti-ICP has 4 boundaries (firmographic / pain / buyer / trigger), each with rule + rationale.
7. Tier 1/2/3 examples named with score breakdown.
8. SDR qualification handoff doc fits on 1 page.
9. **Validated against ≥10 won deals OR ≥10 buyer conversations.** Otherwise the entire output is stamped `Confidence: Hypothesis-only` and downstream skills must tag artifacts `#icp-low-confidence`.

## Eval Cases

**Eval 1 — Mature B2B SaaS with won deals:**
*Input:* CRM software for SMB law firms, 12 won deals over 18 months, US-only.
*Expected output:* Tight firmographic (1–10 lawyer firms, US, billing software in stack), 4 roles filled with Champion = Office Manager, Pain-Trigger-Outcome chain anchored in won-deal quotes, scorecard differentiates won/lost cleanly, anti-ICP includes "firms with >50 lawyers" (different motion).

**Eval 2 — Pre-PMF startup, no customers yet:**
*Input:* AI compliance automation for biotech HR teams, 0 customers, 8 buyer interviews completed.
*Expected output:* All sections marked "hypothesis-only." Confidence: Low. Heavy reliance on interview evidence. Trigger library small but specific. Plan to re-run after first 10 deals.

**Eval 3 — PLG product:**
*Input:* Async standup tool for engineering teams, 2,400 self-serve signups, 80 paid teams, US/EU.
*Expected output:* Buyer/User roles compressed (engineering manager often = both). Triggers shift to usage signals (3+ active members in week 1, etc.). Champion emerges from product usage data. Anti-ICP includes "teams <5" and "teams already on Slack standup bots."

## Guardrails

**On provenance (anti-fabrication — universal rule):**
- **Every named entity in output carries an inline provenance tag** at first mention and on any fact-bearing assertion. Allowed tags: `[user-provided]` / `[verified: <source-or-url>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged named entities are a contract violation. Named entities include: company names, person names, product names, direct quotes, statistics, dates, URLs, dollar figures, customer counts, named tools/sources.
- **No silent assertion.** If you don't have a source and didn't get it from the user, default to `[unverified — needs check]` — never to a confident-looking specific (e.g., never invent "Acme Corp" as a Tier 1 lookalike or fabricate a Crunchbase funding date).
- **Tool-grounding rule:** if no live research tool (web search, MCP server, file lookup) is available at runtime, every external-fact assertion defaults to `[unverified — needs check]`. The agent does NOT invent specifics to fill the template — it tags the field and surfaces the missing input to the user.
- **Worked example warning.** The WorkflowDoc worked example contains many specific-sounding-but-fictional entities (Stitchbox, Plant, Pixly, etc.). Inside the worked example they are tagged `[hypothetical]`. Do NOT replicate that pattern in real user output without the provenance tags + grounding above.

**On evidence:**
- If <10 won deals, mark confidence Medium or Low. Do not claim High confidence on hypothesis.
- Customer language in Pain/Outcome must come from real quotes (CRM notes, call transcripts, support tickets) — not invented.
- Every trigger has a named source for detection. No "we'll know it when we see it."

**On scope:**
- One ICP per skill run. Multi-ICP requests get split into multiple runs.
- Firmographic must produce 500–5,000 candidate accounts. Outside this range, push back.
- Tier examples must include real account names if available; otherwise tag as "hypothetical."

**On boundaries:**
- Anti-ICP cannot be empty. Force 4 boundaries minimum.
- The 4 boundaries must be operationally checkable (a SDR can apply them in <30 seconds).

**On bias:**
- User's stated ICP is hypothesis. Won-deal evidence overrides it.
- Don't ICP what you can't reach. Reachability is part of the score for a reason.
- Force "where they are NOT" — silence on Anti-ICP is dangerous.

**On ethics:**
- ICP definitions cannot include legally protected characteristics in B2C contexts.
- For B2B, firmographic + role + behavior is fine; demographic targeting beyond standard B2B parameters is not.
- "Anti-ICP" is about strategic fit, not about denying service to legitimate users.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Positioning needs sharpening | `positioning-strategy` | ICP firmographic, Pain-Trigger-Outcome, **Workaround Analysis (each workaround becomes an alternative entry)**, Champion language |
| Lead sourcing ready to start | `lead-sourcing-apollo` (planned) | Firmographic filters, trigger queries (split into need/buy), anti-ICP exclusions |
| Lead scoring system needed | `lead-scoring` (planned) | 100-pt scorecard (this becomes the foundation) |
| Channel decisions pending | `channel-strategy` | Reachability data per role, community presence |
| Refinement after 30+ deals | `icp-refinement-loop` (planned) | Current ICP doc, new conversion data |
| Competitor implications | `competitor-analysis` | Anti-ICP "wrong tools entrenched" patterns; **Workaround Analysis (DIY/hire/do-nothing entries become non-product alternatives)** |

---

## Push to CRM

After producing the ICP one-pager and tier examples, persist agent-actionable records to agentic-app via `POST ${CRM_URL}/api/push`. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Tier 1 example accounts (3) | `company` | `score: 5, priority: hot, tags: "#icp-tier-1 #beachhead"` |
| Tier 2 example accounts (3) | `company` | `score: 3, priority: warm, tags: "#icp-tier-2"` |
| Tier 3 example accounts (3) | `company` | `score: 2, priority: cold, tags: "#icp-tier-3"` |
| Anti-ICP examples | `company` | `score: 1, priority: cold, tags: "#anti-icp"` |
| Full ICP one-pager + scorecard rubric | `interaction` (type: `research`) | `relevance` = full ICP doc; tags `#icp-definition` |
| Buyer / Champion / User / Blocker role cards | `interaction` (type: `note`) | One note per role; tagged `#icp-role:buyer`, `#icp-role:champion`, etc. |

If a tier example account has a known decision-maker name + LinkedIn, push as a `person` linked to the company via `contactName`/`contactLinkedIn` (push API auto-creates the link).

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:icp-definition:v2.0.0"`

### Example push (Tier 1 named account with champion contact)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "website": "https://stitchbox.com",
    "industry": "SaaS",
    "score": 5,
    "priority": "hot",
    "tags": "#icp-tier-1 #beachhead",
    "contactName": "[Champion name if known]",
    "contactTitle": "Support Operations Manager",
    "contactLinkedIn": "https://linkedin.com/in/...",
    "relevance": "Tier 1 ICP — 87/100 (Pain 22 / Trigger 18 / WTP 18 / Reach 12 / TTV 8 / Strat 9). Series B SaaS, 100–300 emp, support team 5–15, growing 30%+ YoY. Pain: tribal knowledge across 8 sources; trigger: outsourced support added 60d ago; champion: Support Ops Manager. See ICP v2.0.0 for full Pain-Trigger-Outcome and Anti-ICP boundaries.",
    "source": "skill:icp-definition:v2.0.0"
  }'
```

### Example push (Anti-ICP entry)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "[2,000-emp enterprise w/ entrenched Guru contract]",
    "score": 1,
    "priority": "cold",
    "tags": "#anti-icp #firmographic-out-of-bounds",
    "relevance": "Anti-ICP per ICP v2.0.0: company size >500 emp + entrenched Guru/Stonly contract. Sales cycle 6mo+, reachability 5/15. Do not pursue — nurture only on contract renewal trigger.",
    "source": "skill:icp-definition:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above (real `company` / `person` / `interaction` records, normal priority/score) |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #icp-definition`. Never as `company` / `person` (e.g., a Tier 1 lookalike account name the agent inferred without grounding goes to the review queue, not the active prospect list). |
| `[hypothetical]` | Does NOT push. Local artifact only. |

The `#unverified #review-required` scaffold is in this skill file now; the dashboard review-queue surfacing is a follow-up agentic-app task. Until the dashboard is built, the tag at least makes unverified records filterable and prevents them from polluting the hot/warm/cold prospect tiers.

Example unverified push:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #icp-definition",
    "relevance": "Tier 1 candidate Acme Corp [unverified — needs check] — agent inferred from category but no Crunchbase/LinkedIn confirmation. Pain hypothesis: support-team scaling tribal knowledge [unverified — needs check]. Champion role hypothesis: Support Ops Manager [unverified — needs check]. Needs human verification of (a) company existence, (b) firmographic match, (c) trigger event timing before activation.",
    "source": "skill:icp-definition:v2.0.0"
  }'
```

### When NOT to push

- ICP marked "hypothesis-only" (no won deals) — push the interaction (research note) but skip company tier examples; they're speculative.
- Confidence: Low — tag the research interaction with `#icp-low-confidence` so downstream skills can downweight.
