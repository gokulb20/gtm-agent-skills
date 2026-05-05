# Date Parsing Rules — Follow-Up Management

## Parsing Matrix

| Reply phrase | Parsed date | Provenance |
|---|---|---|
| Explicit ISO date ("March 15, 2027") | 2027-03-15 | `[verified: reply-text]` |
| Quarter phrase ("Q1 2027") | First business day of mid-quarter (2027-01-15) | `[verified: reply-text + agent-rule]` |
| Holiday phrase ("after the holidays") | First business day post Jan 1 | `[verified: reply-text + agent-rule]` |
| Season phrase ("late spring") | First business day mid-season (~May 20) | `[unverified — needs check]` |
| Month-only ("in May") | First business day of stated month (forward year) | `[verified: reply-text + agent-rule]` |
| "Next month" / "next quarter" | First business day next calendar period | `[verified: reply-text + agent-rule]` |
| No date phrase (not-now) | Default 60d | `[unverified — agent-rule]` |
| No date phrase (tried-similar-failed) | Default 90d | `[unverified — agent-rule]` |
| OOO return date | Return date + 1 business day | `[verified: reply-text + agent-rule]` |

## Holiday-Window Collision Rule

Resume dates that land during major holidays (Dec 24–Jan 1, etc.) shift to the first post-holiday business day, not the literal parsed date.

## Multi-Language Rule

Non-English date phrases ("después de las fiestas") need locale-aware parsing. If locale unknown, flag `[unverified — needs check]` and surface for user confirmation if Tier-1.
