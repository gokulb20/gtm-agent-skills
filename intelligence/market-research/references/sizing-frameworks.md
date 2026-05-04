# Market Sizing Frameworks

## Steve Blank's Market-Type Diagnostic

Before sizing, classify market type — methods differ by type.

| Market Type | Definition | Sizing Approach |
|---|---|---|
| Existing market | Known category, known competitors, known buyers | Top-down from analyst reports + bottom-up cross-check |
| Resegmented market | New positioning inside existing category (low-cost or niche) | Top-down for parent category × segment share assumption |
| New market | Category does not yet exist; buyer behavior is being created | Bottom-up only; analogous market comparison; no top-down |
| Clone market | Proven elsewhere, new geography | Reference market × geographic adjustment factor |

Founders default to top-down for everything. New markets have no reliable top-down data; using analyst numbers there is fiction.

## TAM / SAM / SOM Definitions

- **TAM:** Total spend if every eligible buyer in scope bought at user pricing. Theoretical ceiling.
- **SAM:** TAM filtered to segments and geographies the user can reach with current motion.
- **SOM:** Realistic 3-year capture given competitive density, motion strength, resourcing.

## Calculation Methods (use ≥2, triangulate)

| Method | Formula | When to use | Confidence ceiling |
|---|---|---|---|
| Top-down | Industry report figure × segment share | Mature categories with analyst coverage | Medium |
| Bottom-up | # of target accounts × ACV × adoption % | Always, when buyers can be counted | High |
| Value-theory | Customer count × annual value created × capture rate | Net-new categories, B2B with measurable ROI | Medium-high |
| Analogous | Reference market × adjustment factor | Clone markets, new geographies | Low-medium |

## Confidence Labeling Rule

Every sizing number tagged `[high]`, `[medium]`, or `[low]` based on source quality and method count. Single-method sizing caps at Medium.

## Reconciliation Rule

If methods disagree by >2x, explain why. Don't silently average. Pick the higher-confidence one as primary and note the discrepancy.

## Provenance Tagging (Anti-Fabrication)

Every named entity in sizing output (TAM/SAM/SOM numbers, segment sizes, growth rates, comparable companies) must carry a provenance tag: `[user-provided]` / `[verified: <source>]` / `[hypothetical]` / `[unverified — needs check]`. Without a live research tool, default to `[unverified — needs check]`.
