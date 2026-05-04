# 9-Label Reply Taxonomy

## Canonical Labels

| # | Label | Definition | Embedded objection? | Dispatch target | Cadence-state effect |
|---|---|---|---|---|---|
| 1 | `positive` | Clear interest, agreement to next step, or proposed meeting | Rare | discovery-call-prep (meeting) / follow-up-management (next step) | exit-globally |
| 2 | `not-now` | Interest but wrong timing; may include resume date | Common | objection-handling-library (if embedded) + follow-up-management | pause-with-resume |
| 3 | `not-interested` | Hard no, may name reason | Common | objection-handling-library (capture intel only) | exit-permanent (12mo) |
| 4 | `wrong-person` | Not the right buyer; may name referral | Rare | data-enrichment | exit-globally on this recipient |
| 5 | `unsubscribe` | Explicit opt-out request | Never | none (state change is action) | exit-permanent + global cross-channel |
| 6 | `out-of-office` | Auto-reply with return date | Never | follow-up-management | pause-with-resume |
| 7 | `referral` | Names different person to contact | Never | data-enrichment | nurture-park original; new cadence on referral |
| 8 | `question` | Specific question — often soft objection | Sometimes | objection-handling-library (light) | continue |
| 9 | `unclear` | Doesn't fit above with confidence ≥ floor | Possibly | manual-review | defer-manual |

## Pre-classification Short-circuits

Applied BEFORE LLM call, deterministically:

- `Auto-Submitted` header OR body "out of office" / "OOO" / "vacation" → `out-of-office` (confidence 0.99)
- Regex-strong unsubscribe phrases (`\b(unsubscribe|remove me|stop|opt out|opt-out)\b`) → `unsubscribe` (confidence 0.95)
- Bounce auto-reply (5xx / "delivery has failed") → NOT a reply; route to channel skill

## Multi-language Rule

Classify in source language. Always preserve `body_raw`. Translate only a one-sentence summary to English. Unsupported language → default `unclear` + `[unverified — needs check: language]` provenance tag.

## Multi-label Edge Case

Two distinct intents (e.g., "not now AND already using X") → dominant intent = label, secondary signal captured in `embedded_objection` for objection-handling-library.
