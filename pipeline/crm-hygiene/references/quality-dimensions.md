# Quality Dimensions — CRM Hygiene

## Wang & Strong (1996) Framework

Wang & Strong define 15 data-quality dimensions across 4 categories. This skill applies the 4 most operationally critical for CRM:

### Intrinsic — Accuracy
- Data is correct and represents the real-world entity
- Check: email validation, phone format, company domain resolution
- Violation: bounced email still marked verified

### Contextual — Completeness
- Required fields are populated per entity's current stage
- Check: required-field map per stage (from pipeline-stages gates)
- Violation: deal in Discovery missing champion_name

### Contextual — Timeliness
- Data is within freshness window
- Check: email-verified ≤90d, phone ≤12mo, title ≤6mo
- Violation: title from 18-month-old sourcing run, person has since been promoted

### Representational — Consistency
- Same value represented the same way across copies
- Check: industry normalized to Apollo taxonomy, title cleaned, domain lowercased
- Violation: same person tagged "SaaS" on one record and "Software" on another

## Severity Tiers

| Tier | Meaning | Action |
|---|---|---|
| P0 | Blocks scoring/forecasting | Immediate fix or flag |
| P1 | Degrades quality | Batch fix |
| P2 | Cosmetic | Defer |
