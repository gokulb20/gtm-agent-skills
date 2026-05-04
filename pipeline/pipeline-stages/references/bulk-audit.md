# Bulk Audit Procedure — Pipeline Stages

## Bulk Classification Mode

When invoked for pipeline audit (not single-trigger):

1. **Iterate every active deal** — replay gate logic against current state
2. **Classify each deal** — correct-stage / wrong-stage / stuck
3. **Surface findings** — per-deal recommendation with correct stage + missing element
4. **Do NOT auto-correct** — require user authorization before mass stage updates

## Output Format

| Deal ID | Current Stage | Recommended Stage | Missing Element | Severity |
|---|---|---|---|---|
| deal_stitchbox_2026-05 | Discovery | Discovery (correct) | None | — |
| deal_acme_2026-03 | Proposal | Discovery | deal_value, decision_process | P0 |
| deal_helio_2026-04 | Engaged | Contacted | No reply received | P1 |

## Dedup Rule

Stuck-deal already flagged within last 7d — don't double-flag.

## Run Record

Push bulk-audit result as `interaction:research` with `#pipeline-audit` tag. Include: total deals audited, correct-stage count, wrong-stage count, stuck-deal count.
