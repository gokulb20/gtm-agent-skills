---
name: channel-strategy
description: Identify and prioritize go-to-market channels using Gabriel Weinberg's Bullseye Framework, CAC/LTV-per-channel scoring, channel-fit-by-ICP analysis, and stage-appropriate channel selection. Produces a tested channel allocation plan, channel-fit matrix, experiment design, and budget guidance. Use when the user needs channel selection, channel prioritization, channel-mix planning, or wants to know which channels to test next.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [gtm, channel-strategy, bullseye, channel-mix, traction, function-1]
related_skills:
  - icp-definition
  - positioning-strategy
  - market-research
  - competitor-analysis
  - competitive-intelligence
inputs_required:
  - icp-from-icp-definition
  - acv-and-pricing
  - sales-motion-plg-or-sales-led-or-hybrid
  - stage-or-arr-band
  - geography
deliverables:
  - 19-channel-inventory-evaluation
  - channel-fit-by-icp-matrix
  - bullseye-allocation-outer-middle-inner
  - cac-ltv-viability-table-per-channel
  - top-3-channel-deep-dives
  - per-channel-experiment-design
  - budget-allocation-plan
  - kill-and-scale-criteria-per-channel
  - stage-graduation-plan
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Channel Strategy

Decide where to spend GTM time, energy, and budget — which acquisition channels to test, which to scale, which to ignore, and how to allocate effort given ICP, motion, and stage. Replaces channel-by-familiarity with a structured analysis: 19 channels evaluated, ICP-fit scored, CAC/LTV viability checked, Bullseye plan delivered.

> *The worked example uses a fictional product (WorkflowDoc) for illustration. The frameworks, scoring rubrics, and procedure are vertical-agnostic and apply to any B2B GTM context.*

## Purpose

Most teams pick channels by founder-bias, last-job-experience, or whatever's hyped this quarter. The output of this skill is the opposite: a focused 1–3 channel bet with rigorous fallbacks, kill criteria, and a plan for stage transitions.

The deliverable is not a "do everything" matrix. It's a focused experiment design that will produce signal in 8–12 weeks.

## When to Use

Trigger this skill when the user requests:
- Channel selection ("Which channels should we use?")
- Channel prioritization ("We're doing too many — what to cut?")
- Channel-mix planning ("How should we allocate budget across X, Y, Z?")
- New-channel evaluation ("Should we try TikTok / podcasts / events?")
- Stage transition ("We're at $1M ARR — should we add channels?")
- Underperformance diagnosis ("Channel X isn't working — should we kill it?")
- Pre-fundraise channel narrative ("Show our channel logic to investors")

**Do NOT use this skill when:**
- The user wants ongoing performance tracking → `channel-performance` (planned, Tier 6)
- The user wants to reallocate spend after data exists → `channel-performance`
- The user wants to source leads from a specific tool → `lead-sourcing-apollo` (planned)
- The user wants paid-ad creative → outside scope

## Inputs Required

### Parameterized inputs

| Field | Profile path | Required |
|---|---|---|
| ICP (firmographic + roles) | `{{profile.icp}}` | Yes |
| ACV / pricing | `{{profile.product.acv_range}}` | Yes |
| Sales motion | `{{profile.gtm.motion}}` | Yes |
| Stage / ARR | `{{profile.company.arr}}` | Yes |
| Geography | `{{profile.market.geography}}` | Yes |
| Existing channels (if any) | `{{profile.gtm.current_channels}}` | Optional |
| Existing channel performance data | `{{profile.gtm.channel_performance}}` | Optional, high-value |
| Budget available for GTM | `{{profile.gtm.budget}}` | Optional but helpful |
| Founder time available | `{{profile.gtm.founder_time}}` | Optional |
| Sales/marketing headcount | `{{profile.gtm.team}}` | Optional |

### Fallback intake flow

> To pick the right channels, I need:
>
> 1. **ICP** — paste your ICP doc OR describe the buyer segment + roles
> 2. **ACV** — average annual contract value
> 3. **Motion** — PLG / sales-led / hybrid
> 4. **Stage** — pre-revenue / <$1M ARR / $1M–$5M ARR / $5M+ ARR
> 5. **Geography** — where you sell
>
> **High-leverage optional:**
> 6. **Existing channels and what's working / not** — what you've tried, results
> 7. **Budget** — monthly spend available for GTM
> 8. **Team** — founder doing it alone, marketing hire, sales team, etc.

### Input validation rules

- If ACV is <$1k AND motion is "sales-led" → push back: "ACV doesn't support sales-led motion. Either re-price or shift to PLG/marketing-led."
- If user wants to test 5+ new channels simultaneously → push back: "Channel-spreading is the #1 reason early-stage GTM fails. Bullseye says start with 3, narrow to 1."
- If user has 0 customers AND wants paid ads → push back: "Run founder-led channels first. Paid ads optimize for conversion you don't have yet."
- If user is pre-PMF AND wants to scale a channel → push back: "Scaling pre-PMF burns capital. Prove channel-product fit first."

---

## Frameworks Used

### 1. Gabriel Weinberg's Bullseye Framework (*Traction*, Weinberg & Mares, 2015)

The dominant channel-selection framework. Three rings, applied sequentially:

```
                   ┌─────────────────────┐
                   │  OUTER RING (19)     │
                   │  Brainstorm every    │
                   │  channel — even      │
                   │  ones that seem off  │
                   └──────────┬──────────┘
                              ↓
                   ┌─────────────────────┐
                   │  MIDDLE RING (3)     │
                   │  Cheap experiments   │
                   │  in 3 promising     │
                   │  channels (≤$1k each)│
                   └──────────┬──────────┘
                              ↓
                   ┌─────────────────────┐
                   │  INNER RING (1)      │
                   │  Double-down on the  │
                   │  one channel that    │
                   │  works best          │
                   └─────────────────────┘
```

**The 19 channels (Weinberg's canon, *Traction*):**

1. Targeting blogs (guest posts, niche blogs)
2. Publicity (PR, press)
3. Unconventional PR (stunts, viral)
4. Search engine marketing (SEM / paid search)
5. Social and display ads
6. Offline ads (billboards, radio, print)
7. Search engine optimization (SEO)
8. Content marketing
9. Email marketing
10. Engineering as marketing (free tools, calculators)
11. Viral marketing (built-in product virality, k-factor, refer-a-friend loops)
12. Business development (partnerships, integrations)
13. Sales (outbound — cold email, cold call)
14. Affiliate programs
15. Existing platforms (App stores, Shopify app store, etc.)
16. Trade shows
17. Offline events (meetups, dinners, conferences)
18. Speaking engagements (podcasts, talks)
19. Community building (Slack, Discord, Reddit threads)

**Weinberg's rule:** the channel that works for you is rarely the obvious one. Most founders default to 1–2 channels they personally know; the bullseye forces consideration of the others.

### 2. Stage-Appropriate Channel Selection

Channels work differently by stage. Don't pick a $5M ARR channel at $50k ARR.

| Stage | Channel character | Recommended channels |
|---|---|---|
| Pre-PMF (0–$100k ARR) | Founder-led, manual, signal-rich | 1:1 outbound (sales), founder-led content, founder events, hand-built community |
| Early ($100k–$1M ARR) | Repeatable, narrow | Outbound at scale, niche communities, partnerships, content marketing (early) |
| Growth ($1M–$5M ARR) | Scaling 1–2 winners + testing 1–2 new | Add: paid acquisition, broader content, podcast/speaking, business development |
| Scale ($5M+ ARR) | Multi-channel, paid-led | Add: brand spend, broad PR, events, large partnerships |

**Stage rule:** at any stage, expect 1–3 channels to drive 80% of acquisition. The rest are noise.

### 3. CAC/LTV Viability Check (per channel — David Skok benchmarks)

A channel only makes sense if **CAC payback < 12 months** (B2B benchmark; David Skok / *For Entrepreneurs*) and **LTV/CAC > 3** in steady state.

For each channel, estimate:
- **Cost per qualified lead** (rough)
- **Lead → close rate**
- **Resulting CAC**
- **CAC vs. ACV ratio**
- **Payback period**

Channels that fail CAC math are killed before testing — no amount of optimization fixes a $500 cold-email CAC for a $400 ACV product.

### 4. Channel-Fit-by-ICP Matrix (3-dim)

Different ICPs reach through different channels. Score each channel on three dimensions:

| Dimension | Score 1–5 | Question |
|---|---|---|
| **Buyer presence** | | Does our buyer use/consume this channel? (Where do they hang out?) |
| **Buyer attention** | | Are they receptive to messaging here? (Or is this pure entertainment?) |
| **Decision context** | | Does the channel reach them when they're in buying mindset? (Or never?) |

Sum: 3–15. **Channels scoring <8 = not for this ICP.**

### 5. Channel-Motion Compatibility

Some channels don't work for some motions. Force a check:

| Motion | Best channels | Worst channels |
|---|---|---|
| **PLG** | SEO, content, communities, integrations marketplaces, viral loops, free tools | Outbound sales (works but expensive at low ACV), trade shows |
| **Sales-led ($10k–$50k ACV)** | Outbound, targeted content, niche communities, partnerships, events | Mass paid ads, broad SEO |
| **Sales-led ($50k+ ACV)** | Outbound (heavy), events, account-based marketing, executive networking, speaking | Paid social, broad content |
| **Hybrid** | Outbound + content + community (compounding) | Anything that doesn't compound |

### 6. Founder-Time vs. Capital Tradeoff

Channels are either **time-intensive** or **capital-intensive**:

| Time-intensive (founder-led) | Capital-intensive (paid) |
|---|---|
| Founder-led outbound | Paid search |
| Founder-led content | Paid social |
| Speaking / podcasts | Display ads |
| Community participation | Sponsorships |
| Hand-built partnerships | Trade shows |

**Pre-funding rule:** time-intensive only. Capital-intensive channels need both budget AND ICP-fit data first.

### 7. Compounding vs. Linear Channels (Brian Balfour / Reforge)

| Compounding (effort accrues) | Linear (1:1 input/output) |
|---|---|
| SEO | Cold outbound |
| Content marketing | Paid ads |
| Community building | Trade shows |
| Engineering as marketing | Sales calls |
| Brand / publicity | Direct mail |

**Strategic rule:** at every stage, run 1 compounding channel + 1 linear channel. The compounding channel funds future stages; the linear channel funds today.

### 8. Brian Balfour's Four Fits (mental model)

For long-run channel viability, fits must align: **Market-Product fit** (your ICP) × **Product-Channel fit** (the product distributes well through this channel) × **Channel-Model fit** (the economics work) × **Model-Market fit** (your business model fits the market). When channel is failing despite tactics, one of the other fits is the problem.

---

## Tools and Sources

### Channel research and selection

| Source | What it's good for | Cost |
|---|---|---|
| ***Traction* by Weinberg & Mares** | The Bullseye framework reference | Book |
| **Brian Balfour / Reforge** | Channel-product fit thinking | Paid (Reforge) |
| **First Round / a16z / OpenView blogs** | Stage-specific channel benchmarks | Free |
| **Lenny's Newsletter** | B2B/PLG channel essays | Freemium |
| **Demand Curve** | Paid-acquisition benchmarks | Free content |
| **G2 / Capterra reviews of competitors** | Where their customers found them ("how did you hear") | Free |

### Channel-specific tooling

| Channel | Primary tool | Cost |
|---|---|---|
| Outbound (cold email) | Apollo / Smartlead / Instantly | Paid |
| LinkedIn outbound | Sales Nav + Phantombuster / HeyReach | Paid |
| SEO | Ahrefs / Semrush / Ubersuggest | Paid (essential at scale) |
| Content | Notion + ConvertKit / Substack | Mixed |
| Paid search | Google Ads + Microsoft Ads | Paid |
| Paid social | Meta Ads + LinkedIn Ads | Paid |
| Community | Slack / Discord / Circle / Tribe | Mixed |
| Podcasts | Podchaser / Listen Notes (find shows) | Freemium |
| Events | Luma / Meetup / Eventbrite | Mixed |
| Partnerships | Partnerstack / Crossbeam / Reveal | Paid |

### CAC/LTV calculation

| Source | What it's good for |
|---|---|
| **Paddle / ChartMogul / Mosaic** | LTV calculation |
| **Internal CRM + ad platforms** | CAC tracking |
| **Capchase Cents** | B2B benchmarks for CAC/LTV by ACV tier |
| **David Skok — *For Entrepreneurs*** | Canonical SaaS CAC/LTV benchmarks (3:1 LTV:CAC, <12mo payback) |

### Benchmarks (don't trust without internal data)

- **OpenView SaaS Benchmarks** (annual) — CAC, LTV, channel-mix benchmarks by ACV tier
- **SaaStr surveys**
- **Bessemer State of the Cloud**
- **First Round State of Startup**

---

## Procedure

### Step 1: Brainstorm the outer ring (all 19)

Apply the 19-channel inventory. Force consideration of every channel — even the ones that "obviously won't work." This is where surprises live.

For each, write 1 sentence: "How would this work for us?" — even if speculative.

### Step 2: Apply hard filters

Cut channels that fail any of:
- **CAC math:** rough estimate suggests CAC > 6 months payback
- **Motion fit:** clearly wrong for this motion (e.g., trade shows for $20 ACV PLG)
- **Stage fit:** clearly wrong for this stage (e.g., paid ads pre-PMF)
- **Capital constraint:** budget unavailable
- **Time constraint:** team capacity unavailable

Output: 6–10 channels survive.

### Step 3: Score remaining channels (channel-fit-by-ICP)

For each surviving channel, score 1–5 on the 3 dimensions (buyer presence, attention, decision context). Sum = 3–15.

Cut anything <8. Output: 4–7 channels.

### Step 4: Pick middle ring (3 channels)

From the 4–7 surviving, pick 3 to test. Diversify: try not all-outbound or all-content. Mix:
- 1 likely-best channel (highest score)
- 1 high-potential alternative (good score, founder familiar)
- 1 wildcard (different mechanism, learning value)

### Step 5: Design experiments per channel

For each of the 3 middle-ring channels, define:

```
Channel: [name]
Hypothesis: We can acquire [N] qualified leads at [<$X CAC] in [Y weeks]
Test budget: $[amount] (or [N] hours of founder time)
Test duration: [weeks]
Sample size needed: [N events: clicks / replies / meetings]
Success criteria: [specific, measurable]
Kill criteria: [specific, measurable]
Owner: [person]
Tools needed: [list]
```

### Step 6: CAC/LTV viability check (per top channel)

Run the math for each:
- Cost per lead (estimate)
- Lead → close rate (use industry benchmark + adjust for ICP)
- CAC = cost / close rate
- Payback period = CAC / monthly ACV
- LTV/CAC ratio (need LTV estimate; flag if unknown)

Channels that fail are killed even if they scored well on fit.

### Step 7: Decide founder-time allocation

For each test channel, allocate weekly hours of founder/team time. Time is a resource — don't over-commit.

### Step 8: Build the Bullseye plan

Output the canonical Bullseye view: outer (19) / middle (3 + experiments) / inner (TBD after results).

### Step 9: Plan stage graduation

Map: at the next stage ($X ARR / Y customers), which channels get added or swapped?

### Step 10: Define kill / scale criteria

For each channel:
- **Kill if:** [specific metric below threshold by week N]
- **Scale if:** [specific metric above threshold by week N]
- **Iterate if:** [middle range]

### Step 11: Route downstream

Recommend next skill (typically lead-sourcing or sequence-building for the chosen channel).

---

## Output Template

---

### Channel Strategy: [Product Name]

**Prepared:** [date]
**Stage:** [pre-PMF / early / growth / scale]
**ICP:** [from icp-definition]
**ACV:** [$X]
**Motion:** [PLG / sales-led / hybrid]
**Confidence:** [H/M/L]

---

**1. Outer Ring — All 19 Channels Evaluated**

| # | Channel | Stage fit | Motion fit | Note |
|---|---|---|---|---|
| 1 | Targeting blogs | | | |
| 2 | Publicity | | | |
| 3 | Unconventional PR | | | |
| 4 | SEM / paid search | | | |
| 5 | Social and display ads | | | |
| 6 | Offline ads | | | |
| 7 | SEO | | | |
| 8 | Content marketing | | | |
| 9 | Email marketing | | | |
| 10 | Engineering as marketing | | | |
| 11 | Viral marketing | | | |
| 12 | Business development | | | |
| 13 | Sales (outbound) | | | |
| 14 | Affiliate programs | | | |
| 15 | Existing platforms | | | |
| 16 | Trade shows | | | |
| 17 | Offline events | | | |
| 18 | Speaking engagements | | | |
| 19 | Community building | | | |

**2. Channels Surviving Hard Filters** (6–10)

| Channel | Why surviving |
|---|---|

**3. Channel-Fit-by-ICP Scoring**

| Channel | Buyer presence (1-5) | Buyer attention (1-5) | Decision context (1-5) | Total (/15) | Pass (≥8)? |
|---|---|---|---|---|---|

**4. Middle Ring — 3 Channels to Test**

| # | Channel | Why this one | Experiment budget |
|---|---|---|---|
| 1 (likely-best) | | | |
| 2 (alternative) | | | |
| 3 (wildcard) | | | |

**5. CAC/LTV Viability Check**

| Channel | Est. cost/lead | Lead→close % | Est. CAC | Payback (mo) | LTV/CAC | Viable? |
|---|---|---|---|---|---|---|

**6. Per-Channel Experiment Design**

```
=== Channel: [Name] ===
Hypothesis:
Test budget:
Duration:
Sample size:
Success criteria:
Kill criteria:
Owner:
Tools:
Playbook:
  Step 1:
  Step 2:
  Step 3:
```

(repeat for top 3)

**7. Founder-Time / Team Allocation**

| Channel | Hours/week (founder) | Hours/week (other team) | Total |
|---|---|---|---|

**8. Recommended Budget Split**

| Channel | Monthly $ | % of GTM budget |
|---|---|---|

**9. Kill / Scale Criteria**

| Channel | Kill if | Scale if | Iterate if |
|---|---|---|---|

**10. Stage Graduation Plan**

| Trigger | Action |
|---|---|

**11. Recommended Next Step**

[Named skill + 1-sentence rationale]

---

## Worked Example

> *The example below uses **WorkflowDoc**, a fictional AI-native runbook authoring tool for B2B SaaS support teams. The fictional product is shared across all six function-1 skills so the worked examples interlock. The frameworks below apply to any B2B GTM context.*

**Input:**

> Product: WorkflowDoc `[hypothetical]` — AI-native runbook authoring for B2B SaaS support teams
> ICP: Series B SaaS, 100–300 emp, US, support team 5–15
> ACV: $4k average `[hypothetical]`
> Motion: Hybrid (PLG trial → sales-assist for >10 seats)
> Stage: Early ($150k ARR `[hypothetical]`, 4 paid pilots `[hypothetical]`)
> Geography: US only
> Existing channels: founder-led outbound (cold email + LinkedIn) — driving all 4 pilots
> Budget: $5k/month `[hypothetical]` for GTM
> Team: 1 founder doing GTM, 1 part-time content contractor

### Output:

> **Provenance note for the agent reading this example:** every named entity below (CAC/LTV figures, named communities and conferences, channel benchmarks, named tools, dollar budgets, attendance numbers) is `[hypothetical]` — i.e., fictional content for illustration. In real user output, the agent must apply the per-entity tagging discipline using `[user-provided]` / `[verified: <source-or-url>]` / `[unverified — needs check]` as appropriate (see `## Guardrails` provenance rule). Channel benchmarks and community sizes are common fabrication points — never quote one without a citation.

---

### Channel Strategy: WorkflowDoc

**Prepared:** 2026-04-30
**Stage:** Early ($150k ARR)
**ICP:** Series B SaaS, 100–300 emp, US, support team 5–15
**ACV:** $4k
**Motion:** Hybrid (PLG → SLG)
**Confidence:** Medium-High

---

**1. Outer Ring — All 19 Channels**

| # | Channel | Stage fit | Motion fit | Note |
|---|---|---|---|---|
| 1 | Targeting blogs | ✓ | ✓ | Niche CX/support blogs (Support Driven, CX Accelerator) — possible |
| 2 | Publicity | ✗ | – | Pre-newsworthy; defer |
| 3 | Unconventional PR | ✗ | – | Defer to scale stage |
| 4 | SEM / paid search | ✗ | △ | $4k ACV doesn't support paid search ($300+ CPC for "support runbook software") |
| 5 | Social and display ads | ✗ | – | LinkedIn ads possible later; B2B targeting too expensive at this ACV/stage |
| 6 | Offline ads | ✗ | ✗ | – |
| 7 | SEO | △ | ✓ | Compounding; takes 6–12mo; viable bet for $1M ARR target |
| 8 | Content marketing | ✓ | ✓ | Founder-led content + part-time contractor available |
| 9 | Email marketing | – | ✓ | Inbound nurture; need traffic first |
| 10 | Engineering as marketing | △ | ✓ | "Free runbook generator from your tickets" tool — strong fit but engineering cost |
| 11 | Viral marketing | ✗ | △ | B2B support tooling has weak inherent virality; defer |
| 12 | Business development | △ | ✓ | Zendesk / Intercom marketplace + agency partnerships — viable but slow |
| 13 | **Sales (outbound)** | **✓✓** | **✓✓** | **Already working — 4/4 pilots from outbound** |
| 14 | Affiliate programs | ✗ | – | Premature |
| 15 | Existing platforms | △ | ✓ | Zendesk + Intercom marketplaces specifically — high ICP-fit |
| 16 | Trade shows | △ | △ | Customer Service Festival, CX events — expensive for early stage |
| 17 | Offline events | ✓ | ✓ | Small dinners with VPs of Support — high signal, low cost |
| 18 | Speaking engagements | ✓ | ✓ | Podcasts (Customer Service Secrets, Support Driven podcast) |
| 19 | **Community building** | **✓** | **✓** | **Support Driven Slack + CX Accelerator — high ICP-density** |

**2. Channels Surviving Hard Filters**

| Channel | Why surviving |
|---|---|
| Sales (outbound) | Currently driving 100% of revenue; clear winner |
| Community (Support Driven Slack, CX Accelerator) | ICP-density extremely high; founder-time only |
| Speaking (podcasts) | Founder availability; low cost; reaches buyers |
| Content marketing | Compounding; team capacity exists |
| SEO | Compounding play for next stage |
| Targeting blogs (niche guest posts) | Founder-led; supports content channel |
| Engineering as marketing | High potential but engineering cost; defer |
| Existing platforms (Zendesk/Intercom marketplaces) | Aligned with PLG; slow but worth seeding |
| Offline events (small dinners) | Founder time + travel cost; high signal |

**3. Channel-Fit-by-ICP Scoring**

| Channel | Buyer presence | Buyer attention | Decision context | Total (/15) | Pass? |
|---|---|---|---|---|---|
| Sales (outbound) | 5 | 3 | 4 | 12 | ✓ |
| Community (Support Driven) | 5 | 5 | 3 | 13 | ✓ |
| Speaking (podcasts) | 4 | 5 | 3 | 12 | ✓ |
| Content marketing | 4 | 4 | 2 | 10 | ✓ |
| SEO | 3 | 4 | 4 | 11 | ✓ |
| Targeting blogs | 4 | 4 | 3 | 11 | ✓ |
| Existing platforms (marketplaces) | 4 | 3 | 4 | 11 | ✓ |
| Engineering as marketing | 3 | 4 | 3 | 10 | ✓ |
| Offline events (dinners) | 3 | 5 | 4 | 12 | ✓ |

All survive (none below 8). Move to selection.

**4. Middle Ring — 3 Channels to Test**

| # | Channel | Why this one | Experiment budget |
|---|---|---|---|
| 1 (likely-best) | **Sales (outbound) — accelerated** | Already proven; 4/4 wins; need to scale this from founder-only to systematic | $1.5k/mo (Apollo + Smartlead + tools) |
| 2 (alternative) | **Community (Support Driven Slack)** | ICP density is extraordinary; aligns with positioning; founder-time channel | $0 cost; 5 hrs/week founder time |
| 3 (wildcard) | **Speaking (podcasts)** | Reaches buyers + champions during commute; compounds; tests messaging | $500/mo (Podchaser + production); 4 hrs/wk founder |

**5. CAC/LTV Viability Check**

| Channel | Cost/lead | Lead→close% | CAC | Payback (mo) | LTV/CAC | Viable? |
|---|---|---|---|---|---|---|
| Sales outbound (current) | $80 | 5% | $1,600 | 4.8 | 5x est. | ✓ |
| Community (engaged member → lead) | $0 (time) | 12% (warm) | $400 (time-equiv) | 1.2 | High | ✓ |
| Podcasts | $250 | 2% (slow lead) | $12,500 (raw) per direct deal | 38 | <1x direct | ⚠️ As direct, fails. As compounding/brand, possibly viable. |

**Note on podcasts:** raw direct CAC fails. Justified ONLY as compounding brand/awareness play. Allocate as wildcard, not primary.

**6. Per-Channel Experiment Design**

```
=== Channel 1: Sales (outbound) — accelerated ===
Hypothesis: Systematizing the founder-led outbound playbook into Apollo + Smartlead +
            scoring will produce 12+ qualified meetings/month at <$200 CPM.
Test budget: $1,500/mo (Apollo + Smartlead + email infra)
Duration: 90 days (3 cohorts)
Sample size: 1,500 prospects/month outbound
Success: 12+ booked meetings/month by month 3; 30% reply rate; 60%+ deliverability
Kill: <4 meetings/month by week 8; deliverability <50% (means infra problem)
Owner: Founder (week 1), then Founder + Apollo automation (week 4+)
Tools: Apollo (sourcing), Smartlead (sending), Clay (enrichment), Hubspot (CRM)
Playbook:
  Step 1: Build trigger-based lists (recent Series B + new VP of Support hire)
  Step 2: Founder writes sequence v1; iterate weekly on subject + first-line
  Step 3: 5-touch cadence over 14 days; reply → founder-handles
  Step 4: Track per-segment performance; cut underperforming firmographics

=== Channel 2: Community (Support Driven Slack) ===
Hypothesis: Active participation in Support Driven (8k+ Support managers) plus 1 high-
            value content drop/month will surface 5+ inbound leads/month within 90 days.
Test budget: $0 cash; 5 hours/week founder time
Duration: 90 days
Sample size: ~500 active members reached/week (organic)
Success: 5+ inbound leads/month attributed to community by month 3; 2+ of those
         convert to pilot.
Kill: 0 inbound after 60 days OR community moderators flag promotional behavior
      (means we've over-promoted).
Owner: Founder
Tools: Slack, Notion (track threads and conversations)
Playbook:
  Step 1: Founder participates 3x/week in #support-leadership and #knowledge-management
          channels — answer real questions, no pitching
  Step 2: 1 high-value drop per month (template, framework, anonymized data) to that
          community — non-promotional
  Step 3: When relevant, casually mention "we built X for this" in 1 of 10 conversations
  Step 4: Track DMs and inbound with UTM-tagged signup URL

=== Channel 3: Podcasts (wildcard) ===
Hypothesis: Founder appears on 4 niche CX/Support podcasts per quarter — generates 10+
            inbound brand-aware leads per month within 6 months (compounding).
Test budget: $500/mo (Podchaser + light production)
Duration: 6 months (compounding play, slow data)
Sample size: 12 podcast appearances over 6 months
Success: 10+ inbound brand-aware leads/month by month 6; 1+ of these in pilot stage.
Kill: <3 podcast bookings in first 90 days (means we can't get on shows; either ICP
      isn't there or pitch is wrong); OR 0 inbound at month 4.
Owner: Founder + part-time contractor (research + outreach)
Tools: Podchaser, Listen Notes, simple PR tracker
Playbook:
  Step 1: Identify 30 podcasts in CX/Support/CS space; rank by audience density
  Step 2: Pitch 5/week with personalized angle; aim for 4 bookings/month
  Step 3: Develop 3 hook stories that map to message house pillars
  Step 4: Each appearance includes a free-tool / template offer with UTM-tagged URL
```

**7. Founder-Time Allocation**

| Channel | Founder hrs/wk | Team hrs/wk | Total |
|---|---|---|---|
| Sales outbound | 8 (calls, replies) | – | 8 |
| Community | 5 (engagement + content drop) | 2 (contractor: research) | 7 |
| Podcasts | 4 (recording + prep) | 6 (contractor: research + outreach) | 10 |
| **Total** | **17** | **8** | **25** |

Founder GTM time = 17 hrs/wk (manageable for 1 founder also doing product/customers).

**8. Budget Split**

| Channel | Monthly $ | % |
|---|---|---|
| Sales outbound (tools + infra) | $1,500 | 30% |
| Community | $0 | 0% |
| Podcasts (tools + light production) | $500 | 10% |
| Reserve (testing, ad-hoc) | $1,500 | 30% |
| Other tooling (CRM, analytics) | $1,500 | 30% |
| **Total** | **$5,000** | **100%** |

**9. Kill / Scale Criteria**

| Channel | Kill if | Scale if | Iterate if |
|---|---|---|---|
| Sales outbound | <4 meetings/mo by week 8 | 15+ meetings/mo by week 12 (then 2x budget, hire SDR by month 6) | 4–10 meetings/mo |
| Community | 0 inbound by day 60 OR flagged as promotional | 10+ inbound by month 3 (then add 2nd community: CX Accelerator) | 1–4 inbound by day 60 |
| Podcasts | <3 bookings by day 90 OR 0 inbound by month 4 | 10+ inbound by month 6 (then expand: 8 podcasts/qtr; pursue speaking) | Mid-range; reassess pitch |

**10. Stage Graduation Plan**

| Trigger | Action |
|---|---|
| At $500k ARR (first SDR hire) | Sales-outbound team of 2; founder retains community + podcasts |
| At $1M ARR | Add: SEO investment (compounding); add: Zendesk/Intercom marketplace push |
| At $2M ARR | Add: small offline dinners (10 cities/year); evaluate paid LinkedIn ads |
| At $5M ARR | Reassess: paid search + content scale + brand publicity |

**11. Recommended Next Step**

→ `lead-sourcing-apollo` (planned). Channel allocation locked. Next: build the Apollo trigger-based lead lists for the outbound channel using firmographic + trigger filters from `icp-definition`.

---

## Heuristics

- **One channel will drive 80% of growth at any stage.** Find that one before optimizing.
- **Channel-spreading is the #1 early-stage GTM failure mode.** Picking 5 channels = doing none well.
- **Founder-time is the most expensive and highest-leverage GTM resource.** Allocate it like budget, with kill criteria.
- **Compounding channels (SEO, content, community) require 6–12 months. Don't kill them in week 4.**
- **Linear channels (outbound, paid) deliver fast but stop when you stop spending. Don't lean on them alone.**
- **The channel that worked at your last company probably doesn't work for your current ICP.** Re-test, don't assume.
- **A channel that fails CAC math doesn't get tested.** No amount of optimization fixes economics.
- **"What channel should I use?" is usually answered by "Where does my ICP already hang out?"** Find that, prioritize that.
- **Speaking + community + content is the durable B2B founder-led mix.** Outbound funds today; these fund tomorrow.
- **Stage graduation matters.** $500k ARR channels ≠ $5M ARR channels. Plan transitions in advance.

## Edge Cases

### Founder is non-technical, no eng resources
- "Engineering as marketing" channel scores 0; cut from consideration.
- Other channels weight up.

### B2C product
- Bullseye still applies but channel set shifts (paid social, influencers, app stores).
- This skill is B2B-focused; flag if user is B2C and adjust.

### Highly regulated industries
- Trade shows, speaking, and direct relationships gain weight.
- Cold outbound may face stricter compliance (HIPAA, GDPR — especially in healthcare/finance/EU).
- Community building becomes harder (compliance, anonymity).

### Marketplace / two-sided
- Run channel strategy twice: once per side.
- Channels that work for one side may fail for the other.

### Plateau / stuck-at-stage
- User has tried channels A and B; nothing is scaling.
- Force re-examination of ICP and positioning before adding channels.
- "Channel-product fit" requires ICP-product fit first.

### Heavily funded with mandate to grow fast
- Capital-intensive channels become viable earlier.
- But: still must prove channel-product fit before scaling spend. $1M wasted on un-PMF paid spend is common.

### Niche / vertical product
- Mass channels (paid search, broad social) usually fail.
- Niche communities + speaking + targeted outbound usually win.
- Force buyer-density check on every channel.

### International / non-English markets
- Channel availability shifts dramatically (LinkedIn in some markets, WeChat in others).
- Re-run channel-fit-by-ICP for the geography.
- Localization cost is real.

## Failure Modes and Recovery

| Failure mode | Symptom | Recovery |
|---|---|---|
| User wants to "do everything" | 6+ channels in middle ring | Force Bullseye discipline. Pick 3. Others become "test next quarter." |
| User defaults to founder-favorite channel | "We're going to do podcasts because [founder] loves podcasts" | Run channel-fit-by-ICP audit. If podcasts score <8, surface the bias. |
| Channel doesn't compound but treated as if it does | Heavy reliance on cold email, no compounding play | Force at least 1 compounding channel in the mix. |
| CAC math impossible (ACV too low) | $50 ACV product on paid LinkedIn | Push back: economics don't work. Either re-price or shift channel. |
| User insists on a clearly bad channel | "We must do trade shows" for $500 ACV PLG product | Show the math. Force kill criteria. Allow 1 test if budget allows; keep tight. |
| All chosen channels are linear | Outbound + paid + ads | Force at least 1 compounding channel. Otherwise growth caps. |
| Channel was working but performance is dropping | CTR / reply rate / conversion declining | Run `channel-performance` (planned, Tier 6) for diagnostic. |
| ICP shift but channel mix didn't | Channels picked for old ICP still in use | Re-run this skill with new ICP input. |

## Pitfalls

- **Channel-of-the-month** — chasing whatever's hyped without ICP-fit math.
- **Confusing "channel works for them" with "channel works for us"** — competitor's channel mix isn't your channel mix.
- **Treating channel-product fit as a known input** — until you've run experiments, fit is hypothesis.
- **Over-investing in compounding channels at pre-PMF** — SEO at 0 customers wastes capital.
- **Cutting compounding channels too early** — SEO/content take 6–12 months; killing at week 8 is the most common mistake.
- **No kill criteria** — channels that quietly underperform for 6+ months drain budget.
- **Over-relying on benchmarks** — industry CAC numbers anchor expectations but your ICP is unique.
- **Spreading thin** — running 5 mediocre channels instead of 2 great ones.
- **Skipping the wildcard slot** — middle ring should include 1 unfamiliar channel; learning value is real.

## Verification

Channel strategy is complete when:
1. All 19 channels have been considered (even if quickly cut).
2. 3 channels are in the middle ring with explicit experiment design.
3. Each channel has CAC/LTV viability checked.
4. Each channel has kill / scale / iterate criteria.
5. Founder-time and budget allocations are explicit and feasible.
6. Stage-graduation plan exists for the next 2 stages.
7. At least 1 compounding channel + 1 linear channel are in the mix.

## Done Criteria

1. 19-channel inventory evaluated (each at least 1-line annotated).
2. Hard filters applied; 6–10 channels survive.
3. Channel-fit-by-ICP scoring complete; 4–7 channels pass ≥8.
4. Middle ring picks 3 channels (likely-best + alternative + wildcard).
5. CAC/LTV viability table per top-3 channel; non-viable killed.
6. Per-channel experiment designed (hypothesis / budget / duration / sample / success / kill / owner / tools / playbook).
7. Founder-time allocation table; total feasible.
8. Budget split adds to 100%.
9. Kill / scale / iterate criteria per channel.
10. Stage-graduation plan for next 2 stages.

## Eval Cases

**Eval 1 — B2B SaaS, $5–10k ACV, sales-led, early stage:**
*Input:* CRM software for SMB law firms, $4k ACV, $200k ARR, US, founder-led GTM
*Expected output:* Bullseye prioritizes outbound + niche legal communities + content marketing. Cuts paid search (CPC too high for ACV), trade shows (ABA conferences viable later). Stage graduation: SEO at $1M ARR, paid LinkedIn at $5M.

**Eval 2 — PLG product, $200 ACV, growth stage:**
*Input:* Async standup tool for engineering teams, $200/team/month ACV, $2M ARR, 2k self-serve signups/month
*Expected output:* Bullseye prioritizes SEO + content + integrations marketplace + community. Cuts outbound (CAC math fails at $200 ACV unless very efficient). Engineering as marketing scores high (free tools).

**Eval 3 — Enterprise, $100k+ ACV, post-PMF:**
*Input:* Compliance automation for biotech HR teams, $80k ACV, $3M ARR, US/EU
*Expected output:* Bullseye prioritizes ABM outbound + speaking + small executive events + analyst influence. Mass channels cut. Founder-led conferences/networks weighted high.

**Eval 4 — Founder wants podcasts but data says outbound:**
*Input:* User insists on podcasts as primary channel; data + ICP-fit suggests outbound is the answer.
*Expected output:* Skill respectfully surfaces the bias, runs full analysis, shows outbound scoring higher. Recommends podcasts as wildcard (3rd ring), not primary. User can override but understands the trade-off.

## Guardrails

**On provenance (anti-fabrication — universal rule):**
- **Every named entity in output carries an inline provenance tag** at first mention and on any fact-bearing assertion. Allowed tags: `[user-provided]` / `[verified: <source-or-url>]` / `[hypothetical]` / `[unverified — needs check]`. Untagged named entities are a contract violation. Named entities include: CAC/LTV figures, named communities and conferences, channel benchmarks, named tools, dollar budgets, named team members.
- **No silent assertion.** If you don't have a source and didn't get it from the user, default to `[unverified — needs check]` — never to a confident-looking specific (e.g., never invent "Support Driven Slack has 8,000 members" without a citation).
- **Tool-grounding rule:** if no live research tool is available at runtime, every external-fact assertion (community sizes, conference attendance, benchmark CAC numbers, channel CPC averages) defaults to `[unverified — needs check]`. The agent does NOT invent specifics to fill the channel-fit-by-ICP scoring table.
- **Worked example warning.** Worked examples in this skill contain specific-sounding-but-fictional channel data, tagged `[hypothetical]`. Do NOT replicate that pattern in real user output without the provenance tags + grounding above.

**On evidence:**
- CAC estimates flagged when based on benchmarks vs. internal data.
- Channel-fit scores reflect actual buyer behavior, not founder assumption.
- Cite data sources when using industry benchmarks.

**On scope:**
- Maximum 3 channels in middle ring. Force discipline.
- One ICP per channel-strategy run. Multi-ICP requires multiple runs.

**On bias:**
- Founder-favorite channel is hypothesis, not answer.
- "Channel that worked at last company" is hypothesis.
- Force buyer-presence verification, not just buyer-presence claim.

**On capital allocation:**
- Pre-PMF push back on capital-intensive channels.
- Below $1M ARR push back on broad mass channels.
- Always reserve 20–30% of budget for tests / wildcards.

**On time horizons:**
- Compounding channels need 6–12 months. Set expectations.
- Linear channels deliver in 4–8 weeks. Set expectations.
- Don't promise outbound results in week 1 or SEO results in month 2.

**On stage realism:**
- Pre-PMF prioritizes signal over scale (1:1 conversations).
- Early stage prioritizes repeatability over volume.
- Don't optimize for scale before proving repeatability.

## Linked Skills

| Condition | Next skill | Inputs to carry forward |
|---|---|---|
| Outbound prioritized | `lead-sourcing-apollo` (planned) | Firmographic filters, trigger queries, anti-ICP from icp-definition |
| Email sequences needed | `cold-email-sequence` (planned) | Wedge, role-specific hooks, Pain language |
| LinkedIn outreach needed | `linkedin-outreach` (planned) | Champion role hooks, message pillars |
| Performance tracking after launch | `channel-performance` (planned) | Kill/scale criteria, expected baselines |
| Content channel chosen | `content-strategy` (planned — gap to flag) | Topic clusters mapped to ICP pain |
| Community channel chosen | `community-playbook` (planned — gap to flag) | Target communities + engagement playbook |

---

## Push to CRM

Channel strategy is a **plan and budget**, not entity records. Push the plan as a research interaction so downstream channel-execution skills (`lead-sourcing-apollo`, `cold-email-sequence`, `linkedin-outreach`, `channel-performance`) can read it as their input. Reads `CRM_URL` and `AGENTIC_APP_TOKEN` from `.env` (see `function-1-skills/.env.example`).

### Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Bullseye allocation (outer/middle/inner ring) + budget | `interaction` (type: `research`) | `relevance` = full plan; tags `#channel-strategy #bullseye` |
| Per-channel experiment design (top 3) | `interaction` (type: `note`) | One per channel; tagged `#channel-experiment #channel:<name>` — picked up by execution skills |
| CAC/LTV viability table | `interaction` (type: `note`) | tagged `#channel-economics` |
| Kill criteria + stage-graduation plan | `interaction` (type: `note`) | tagged `#channel-kill-criteria` — read by `channel-performance` (planned) on its scheduled review |

Channel strategy does **not** push `company` or `person` records — those come from `lead-sourcing-apollo` once a channel is picked.

### Env contract

```
CRM_URL=http://localhost:4210
AGENTIC_APP_TOKEN=
```

### Source tag

`source: "skill:channel-strategy:v2.0.0"`

### Example push (Bullseye plan + budget)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#channel-strategy #bullseye",
    "relevance": "CHANNEL PLAN v2.0.0 (2026-04-30) — stage: pre-PMF→early ($150k ARR target)\nMiddle ring (3 tested): (1) Outbound to Series B SaaS support leaders — 200 accounts/wk, $2.5k budget, 8wk; (2) Support Driven Slack community — founder participation, $0, 12wk; (3) Podcasts as wildcard — 6 appearances, $500 prep, 12wk.\nInner ring candidate: outbound (decision after 8wk).\nBudget split: outbound $2.5k (50%), community $0 (founder time 5h/wk), podcasts $500 (10%), reserve $2k (40%).\nKill criteria: outbound CAC >$2k after 8wk = kill; community no inbound after 12wk = de-prioritize; podcast no measurable lift after 12wk = wildcard fail (acceptable).\nCompounding/linear pairing: community + podcasts compound; outbound is linear.\nStage graduation: at $1M ARR add SEO investment + Zendesk/Intercom marketplace push.\nFails CAC math (excluded): paid social, paid search, trade shows.",
    "source": "skill:channel-strategy:v2.0.0"
  }'
```

### Example push (per-channel experiment for execution skill)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "company": "WorkflowDoc",
    "tags": "#channel-experiment #channel:outbound",
    "relevance": "EXPERIMENT — Outbound (8 weeks)\nTarget: 200 accounts/wk matching ICP firmographic (Series B SaaS, 100-300 emp, support 5-15, US)\nSequence: 4 touches (email + LI), Day 0/3/7/14\nVariants: 2 message frames — (a) AI-native authoring (b) per-seat pricing\nMetrics: meeting booked rate >2%, qualified pipeline $50k by week 8\nBudget: $2.5k (Apollo + Smartlead)\nKill: <1% reply rate after 4wk OR CAC >$2k after 8wk\nNext skill: lead-sourcing-apollo (firmographic filters from icp-definition v2.0.0)",
    "source": "skill:channel-strategy:v2.0.0"
  }'
```

### Provenance routing (anti-fabrication scaffold)

Per the universal provenance rule (see `## Guardrails` / CLAUDE.md), entities are tagged at runtime. Push behavior depends on tag:

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes per the standard mapping above |
| `[unverified — needs check]` | Pushes ONLY as `interaction` (type: `research`) tagged `#unverified #review-required #channel-strategy`. CAC/LTV figures, community sizes, conference attendance, benchmark CPC numbers, and named-tool prices without citations flow here for human review before adoption in budgets or experiment specs. |
| `[hypothetical]` | Does NOT push. Local artifact only. |

The `#unverified #review-required` scaffold is in this skill file now; the dashboard review-queue surfacing is a follow-up agentic-app task. Until the dashboard is built, the tag at least keeps inferred channel data out of approved budgets and kill-criteria targets.

Example:

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #channel-strategy",
    "relevance": "Outbound CAC estimate $1.6k [unverified — needs check] — agent inferred from typical mid-market hybrid; no internal historical data. Support Driven Slack 8,000 members [unverified — needs check] — no citation. Podcast audience overlap with ICP 30% [unverified — needs check] — no source. Hold for verification before locking experiment budgets and kill-criteria.",
    "source": "skill:channel-strategy:v2.0.0"
  }'
```

### When NOT to push

- ICP or positioning not defined (skill should have pushed back; if it didn't, do not push a channel plan floating free of those inputs).
- User is pre-PMF and asking for paid-channel scaling — skill should produce a "do not pursue" recommendation, not a plan; in that case push only the recommendation interaction tagged `#channel-strategy #recommendation:hold`.
