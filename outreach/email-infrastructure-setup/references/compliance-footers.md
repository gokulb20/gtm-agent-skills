# Compliance Footer Templates

## CAN-SPAM (US — Email)

Required in every commercial email:

- Truthful From, To, Reply-To
- Truthful subject line (no deceptive text)
- **Physical postal address** (must be legitimate; some interpretations reject PO boxes)
- **Functional opt-out** mechanism, honored within 10 business days

### Template

```
---
WorkflowDoc
100 Market St #200
San Francisco, CA 94105

Unsubscribe: https://workflowdoc-mail.com/u/abc
```

## GDPR / UK GDPR (EU + UK — Email + LinkedIn Cold Messages)

- **Lawful basis**: legitimate interest (LIA documented) OR explicit consent
- B2B contacts at corporate domains typically legitimate-interest-eligible IF message is relevant and clear opt-out provided
- Personal email addresses (gmail, outlook, etc.) → consent-only or skip
- Right to object honored on first request
- DSAR (access, rectification, erasure) honored

### Template

```
---
We're contacting you under our legitimate interest in [ICP relevance statement].
You can opt out at any time: https://workflowdoc-mail.com/u/abc
Data protection inquiries: dpo@workflowdoc.com
```

## CASL (Canada — Email + SMS)

- Implied or express consent required
- Identification of sender + functional opt-out
- Implied consent for B2B if existing business relationship within 24 months OR conspicuous publication
- Stricter than CAN-SPAM; if in doubt, route to nurture not cold

### Template

```
---
WorkflowDoc Inc.
123 King St W, Toronto, ON M5H 3V7
Unsubscribe: https://workflowdoc-mail.com/u/abc
```

## RFC 8058 One-Click List-Unsubscribe Headers

```http
List-Unsubscribe: <mailto:unsubscribe@outbound-domain>, <https://outbound-domain.com/u/token>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

- HTTPS URL must accept POST and process within 2 business days (RFC 8058 says immediate; CAN-SPAM allows 10 days; pick the stricter)
- Mandatory under Google + Microsoft 2024 bulk-sender rules for >5k/day senders

## Provenance Routing for Push-to-CRM

| Provenance | Push behavior |
|---|---|
| `[user-provided]` or `[verified: <source>]` | Pushes as `interaction:research` per standard mapping |
| `[unverified — needs check]` | Pushes ONLY as `interaction:research` with `#unverified #review-required` tags. Readiness flag stays false |
| `[hypothetical]` | Does NOT push. Local artifact only |
