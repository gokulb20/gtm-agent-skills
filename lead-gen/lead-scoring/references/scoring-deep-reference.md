# Lead Scoring: Deep Reference

## 100-Point ICP Scorecard Dimensions

| Dimension | Weight | What It Measures | Evidence Source |
|---|---|---|---|
| Pain | 25 pts | How acute is the pain this product solves for this contact? | `signals[]` and `personalization_hook` encoding recent pain/trigger |
| Trigger | 20 pts | Strength × recency of buying triggers | `signals[].strength` × `decay(days_since_event, half_life)` |
| WTP / ACV match | 20 pts | Does company size + funding + revenue suggest fit with product price? | Firmographic fields |
| Reach | 15 pts | Email verified? Phone? LinkedIn? Multiple channels? | `email_status`, `phone_status`, `linkedin_url` |
| TTV / Time-to-value | 10 pts | Does role + stage suggest fast or slow path to value? | Title, seniority, company stage, stack friction |
| Strategic | 10 pts | Logo value, vertical anchor, follow-on sale potential | Named-account list, expansion patterns |

## Trigger Decay Formula

```
trigger_score = base_strength × decay(days_since_event, half_life)
```

- `strong` base = 0.9, `medium` = 0.6, `weak` = 0.3
- `decay(d, h) = exp(-d * ln(2) / h)` — exponential decay with half-life
- Example: strong trigger 60 days ago with 90-day half-life: `0.9 × exp(-60 × 0.693/90) = 0.9 × 0.63 ≈ 0.57 → ~11/20`

Without decay, stale triggers inflate scores. A "raised Series B 14 months ago" record should score near zero on Trigger, not 18/20.

## BANT Qualification

| Dimension | States | Notes |
|---|---|---|
| Budget | `confirmed` / `inferred` / `unknown` | RFP = confirmed; firmographic suggests spend = inferred |
| Authority | `confirmed` / `inferred` / `unknown` | Decision-maker by title = confirmed |
| Need | `confirmed` / `inferred` / `unknown` | Signal explicit pain = confirmed |
| Timing | `confirmed` / `inferred` / `unknown` | Deadline visible = confirmed; trigger recent = inferred |

**BANT adjustment to base score:**
- All 4 confirmed: +5 (capped at 100)
- 3+ confirmed: +3
- Mostly inferred: 0
- Mostly unknown: −5

## CHAMP Qualification

| Dimension | States | Notes |
|---|---|---|
| Challenges | `confirmed` / `inferred` / `unknown` | Articulated problem (overlaps Need, framed differently) |
| Authority | same as BANT | |
| Money | same as Budget | |
| Prioritization | `confirmed` / `inferred` / `unknown` | "Solving this in Q2" = confirmed; key gap BANT hides |

**CHAMP insight:** `Need: confirmed` but `Prioritization: unknown` = buyer agrees they have the problem but isn't actively solving — different cadence than full BANT.

## SAL (Sales-Accepted-Lead) Gates

For Tier-1 records, check 4 gates:
1. **ICP fit confirmed** — scorecard ≥ 75 ✓
2. **Trigger present and within half-life** ✓
3. **Decision-maker or champion identified** — BANT Authority ≥ inferred ✓
4. **No hard disqualifiers** — no anti-ICP firmographic, no DNC phone-only, no role-based email ✓

Pass all 4 → `sal_eligible: true`. Fail any → flag the failed gate; don't strip Tier-1 status but warn at hand-off.

## Tier Cutoffs (Default from `icp-definition`)

| Tier | Score Range | Priority | CRM Score (1-5) |
|---|---|---|---|
| Tier-1 | ≥75 | hot | 5 |
| Tier-2 (high) | 65–74 | warm | 4 |
| Tier-2 (low) | 55–64 | warm | 3 |
| Tier-3 | 40–54 | cold | 2 |
| Anti-ICP | <40 | cold | 1 |

## Score-Cap Rule

Records with `[unverified — needs check]` on critical fields (email_status, personalization_hook) are capped at 60/100 (Tier-2 max) regardless of other dimensions. Routed to review queue, not pushed as scored persons.

## Healthy Tier Distribution

| Band | T1 | T2 | T3 | Anti-ICP |
|---|---|---|---|---|
| Healthy | 10–20% | 30–45% | 25–35% | 5–15% |
| >50% T1 | Rubric too lenient or source pre-filtered | | | |
| <2% T1 | Source too wide | | | |

## Worked Example (Fictional — All Entities `[hypothetical]`)

**Product:** BalanceBox [hypothetical] (FP&A automation)
**Input:** 80 enriched leads

**Sample record score breakdown:**
```
Esme Liang [hypothetical], VP Finance Ops, Forge Robotics [hypothetical]
Pain:     18/25 — VP Finance arrival triggers FP&A tooling review within 90d
Trigger:  12/20 — strong (0.9) × decay(60d, 90d) = 0.57 → ~11/20 + within-window boost
WTP:      16/20 — Series C, 201-500 emp, ICP ACV band matches
Reach:    13/15 — email verified, LinkedIn verified, phone unverified
TTV:       8/10 — medium-fast FP&A decision velocity
Strategic: 5/10 — mid-market, some logo value
Raw total: 72
BANT adj:  -2 (budget unknown, authority confirmed, need inferred, timing inferred)
Final:     70 → Tier-2 / warm
```

**Distribution:** 14 T1 (17.5%) / 32 T2 / 24 T3 / 10 Anti-ICP — healthy.
**SAL-eligible:** 11 of 14 T1 (3 failed reachability gate).

## Push-to-CRM Mapping

| Deliverable | Entity | Push fields |
|---|---|---|
| Score + priority + tier | `person` (PATCH) | `score` (1-5), `priority` (hot/warm/cold), `tags: #icp-tier-1 #sal-eligible` |
| Score rationale | `interaction` (research) | `relevance` = rationale + per-dimension breakdown; `tags: "#scoring-rationale #function-2"` |
| Run record | `interaction` (research) | `relevance` = run summary + distribution; `tags: "#scoring-run #function-2"` |
| Score-capped records | `interaction` (research) ONLY | `tags: "#unverified #review-required #lead-scoring"` |

## Provenance Routing

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | PATCH person with score |
| `[unverified — needs check]` | Only `interaction:research`; person NOT patched — score stays unset |
| `[hypothetical]` | Never push (hypothesis-mode output surfaced to user only) |
