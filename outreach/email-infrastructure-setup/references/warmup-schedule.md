# Warmup Schedule & Reputation Monitoring

## Warmup Ramp Schedule

| Day | Daily Cap | Notes |
|---|---|---|
| 0 | 5 | Enable platform warmup (Smartlead Warmup, Mailreach, etc.) |
| 5 | 10 | If Postmaster Tools shows no negative signal |
| 10 | 20 | Continue monitoring |
| 14 | 30 | If reputation "High" or "Medium" in Postmaster |
| 14–30 | 30 | Warmup score should stabilize ≥70 |

### Extended ramps

- **New/cold domains**: 21–30 days
- **>200/day target volume**: 30-day floor
- **Google bulk-sender mode (>5k/day)**: 30+ days

## Exit Conditions for Readiness Flag

All must pass simultaneously:

- `warmup_score ≥ 70`
- `domain_age_days ≥ 14`
- `google_postmaster_reputation ∉ {Low, Bad}`
- `microsoft_snds ∉ {red}`
- `spf_aligned: true`
- `dkim_present: true`
- `dmarc_published: true`
- `list_unsubscribe_rfc8058: true`

## Reputation Monitoring Tools

| Tool | What it shows | Refresh |
|---|---|---|
| Google Postmaster Tools | Domain + IP reputation; spam rate per Google | Daily |
| Microsoft SNDS | IP reputation per Microsoft's view | Daily |
| TalosIntel (Cisco) | Public IP reputation; secondary check | Daily |
| MXToolbox | SPF/DKIM/DMARC record resolution | On-demand |
| EasyDMARC | DMARC report aggregator; reads rua reports | Daily |

## Reputation Baseline Template

```yaml
google_postmaster: high | medium | low | bad
microsoft_snds: green | yellow | red
talos_intel: positive | neutral | negative
baseline_date: <ISO>
```

## When to Extend Warmup

- Postmaster shows "Low" or "Bad" → extend 7+ days
- SNDS shows red → extend 7+ days
- Warmup score stalls at 50–60 → check warmup-partner pool quality; extend 7+ days
- Complaint rate >0.3% in week 1 → pause; audit list quality (not infra issue)

## Recovery After Reputation Event

1. STOP all sends immediately
2. Audit recent send batches for spam-trap / high-complaint / high-bounce
3. Remediate list quality issues
4. Extend warmup 14+ days
5. Re-pull baseline
6. Readiness flag stays false until Postmaster recovers to Medium
