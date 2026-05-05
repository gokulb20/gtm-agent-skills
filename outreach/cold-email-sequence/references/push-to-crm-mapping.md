# Push-to-CRM Mapping & Curl Examples

## Entity Routing

| Deliverable | Entity | Push fields |
|---|---|---|
| Each scheduled Touch (draft) | `interaction:research` | `relevance` = "Touch <position> scheduled for <ISO> via <channel> with hook <url>"; `tags: "#scheduled #cold-email #touch-<position> #function-3"` |
| Each Touch after send | `interaction:outreach` | `relevance` = subject + body excerpt + provenance; `tags: "#sent #cold-email #function-3"` |
| Cadence + campaign run record | `interaction:research` | `relevance` = run summary; `tags: "#cold-email-sequence-run #function-3"` |
| Last-touched timestamp | `person` PATCH | `last_touched_at`, `last_touched_channel: email`, tags updated |
| `[unverified]` (hook missing) | `interaction:research` ONLY | `tags: "#unverified #review-required #cold-email-sequence #blocked-no-hook"`; never `outreach` |

## Source Tag

`source: "skill:cold-email-sequence:v2.1.0"`

## Example Push (Sent Touch)

```bash
curl -X POST ${CRM_URL}/api/push \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AGENTIC_APP_TOKEN}" \
  -d '{
    "company": "Stitchbox",
    "contactName": "Esme Liang",
    "contactEmail": "esme@stitchbox.com",
    "tags": "#sent #cold-email #touch-1 #ccq-pain #function-3",
    "relevance": "Cold email sent 2026-05-05T10:00 PT. Subject: \"New VP CX seat — first 90 days?\". Framework: CCQ + Pain. Hook: Stitchbox VP CX hire 2026-04-19 [verified: news.example.com/stitchbox-vp-cx-2026]. Word count: 74. Sender: will@workflowdoc-mail.com (reputation 92). Cadence: cad_workflowdoc_t1_5touch_19d_v1.",
    "source": "skill:cold-email-sequence:v2.1.0"
  }'
```

## Example Push (Blocked — No Verified Hook)

```bash
curl -X POST ${CRM_URL}/api/push \
  -d '{
    "tags": "#unverified #review-required #cold-email-sequence #blocked-no-hook",
    "relevance": "Touch BLOCKED for Mira Chen [unverified — needs check] — personalization_hook absent. Recommend re-enrichment with linkedin_recent_posts permission OR manual hook capture, then re-run cold-email-sequence.",
    "source": "skill:cold-email-sequence:v2.1.0"
  }'
```

## When NOT to Push

- Drafts never scheduled — local artifact only
- Touches blocked at pre-flight (infrastructure, capacity, DNC, hook) — push ONLY as `interaction:research` with block reason
- `[unverified — needs check]` — provenance routing applies
- `[hypothetical]` — never push
- Recipient unsubscribed before scheduled send — drop remaining cadence Touches; push unsubscribe-honor record only
