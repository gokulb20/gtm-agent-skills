# LinkedIn Rate Limits & Connection Frameworks

## Rate Limits

| Metric | Limit | Notes |
|---|---|---|
| Connection requests/week | 80 (default); 150 (high-SSI ≥75) | Rolling 7-day reset, NOT calendar week |
| Daily distribution | 15–25/day max | Never bulk-burst |
| Messages to existing connections/week | 200 | |
| InMail/month | 50 | Depends on Sales Nav seat tier; Core: 50/mo |
| Free-account personalized notes | 5/month | New since 2023 restriction |
| Profile views/day | 150 (free); 2,000 (Sales Nav) | |
| Group/event messages/week | 10 to non-connections | |
| Total connections | 30,000 | Hard cap on profile |

## Connection-Request Frameworks

### Warm-Intro
- References mutual connection or specific shared context
- Acceptance rate: ~30%
- Use when a real mutual exists
- Requires: `mutual_connection [verified]` or `shared_context [verified]`

### Event-Based
- References a recent event (new role, promotion, funding, post, conference talk)
- Acceptance rate: 15–25% (highest when event is <60 days old AND specific)
- Requires: `citable_hook_url [verified]` — absence routes to review queue
- Example: "Nina — congrats on landing the VP CX role at Helio."

### Content-Engagement
- User previously engaged with recipient's LI content (liked/commented)
- References the specific post engaged with
- Acceptance rate: 12–20%
- Requires: `post_url [verified]` and `engagement_type` (like/comment)

### Generic-No-Context (FORBIDDEN)
- "I'd love to connect with another professional in <industry>"
- Acceptance rate: <5%
- Treated as the LinkedIn equivalent of "I hope this finds you well"
- Auto-rejected by this skill

## Connection Note Rules

- ≤300 chars HARD limit
- NO URLs (LinkedIn flags)
- NO emojis (perceived as bulk)
- Single CTA only
- Framework-based (warm-intro / event-based / content-engagement)

## Optimal Send Time

- Weekday 9am–5pm recipient local
- Tue–Thu best
- Afternoon often higher acceptance than morning
- Friday afternoons get worse acceptance
- Never weekends

## Account Safety State Machine

| State | Action |
|---|---|
| Green | Proceed with scheduled touches |
| Amber | Pause automation; 7-day cool-down; manual-only sends |
| Red | Stop all outreach; cool-down 7+ days; review recent volume + recipient quality |

## Provenance Routing for Push-to-CRM

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Touch sends; pushes as `interaction:outreach` |
| `[unverified — needs check]` | Touch BLOCKED; pushes as `interaction:research` with `#unverified #review-required #linkedin-outreach` |
| `[hypothetical]` | Never sends; never pushes |
