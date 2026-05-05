#!/usr/bin/env python3
"""dedup_leads.py — Deduplication using linkedin_url > email > phone priority.

Usage:
    cat leads.json | python dedup_leads.py [--existing-crm crm_dump.json]

Reads lead records from stdin (JSON array), deduplicates by merge key
priority: linkedin_url > email > phone (person-level), company_domain
(company-level). Optionally cross-checks against existing CRM records.

Output: deduplicated records + merge log to stdout (JSON).
"""
import json
import sys
import argparse


def merge_key_person(record: dict) -> str | None:
    """Return the highest-priority merge key for a person record."""
    for field in ["linkedin_url", "email", "phone"]:
        val = record.get(field, "")
        if val and val.strip():
            return val.strip().lower()
    return None


def merge_key_company(record: dict) -> str | None:
    """Return the merge key for a company record."""
    val = record.get("company_domain", "")
    return val.strip().lower() if val and val.strip() else None


def provenance_tier(provenance: str) -> int:
    """Map provenance tag to numeric tier for comparison."""
    mapping = {
        "verified": 4,
        "user-provided": 3,
        "unverified": 1,
        "hypothetical": 0,
    }
    return mapping.get(provenance, 1)


def pick_winner(existing: dict, incoming: dict) -> dict:
    """Pick the winning record between existing and incoming on collision."""
    # Prefer higher provenance tier
    existing_pt = provenance_tier(existing.get("provenance_person", "unverified"))
    incoming_pt = provenance_tier(incoming.get("provenance_person", "unverified"))
    if incoming_pt > existing_pt:
        return incoming
    if existing_pt > incoming_pt:
        return existing
    # Tie: prefer more recent freshness_date
    existing_fd = existing.get("freshness_date", "")
    incoming_fd = incoming.get("freshness_date", "")
    if incoming_fd > existing_fd:
        return incoming
    return existing


def dedup(records: list[dict], existing_crm: list[dict] | None = None) -> dict:
    """Deduplicate records against each other and optionally existing CRM."""
    seen_person: dict[str, dict] = {}
    seen_company: dict[str, dict] = {}
    merge_log: list[dict] = []
    output: list[dict] = []

    # Seed with existing CRM records if provided
    if existing_crm:
        for rec in existing_crm:
            pk = merge_key_person(rec)
            if pk:
                seen_person[pk] = rec
            ck = merge_key_company(rec)
            if ck:
                seen_company[ck] = rec

    for rec in records:
        pk = merge_key_person(rec)
        ck = merge_key_company(rec)

        if pk and pk in seen_person:
            winner = pick_winner(seen_person[pk], rec)
            merge_log.append({
                "key": pk,
                "key_type": "person",
                "kept": winner.get("contact_name", ""),
                "merged": (rec if winner is not rec else seen_person[pk]).get("contact_name", ""),
                "reason": "provenance/freshness",
            })
            seen_person[pk] = winner
            if ck:
                seen_company[ck] = winner
            continue

        if ck and ck in seen_company:
            # Company-level collision — enrich but don't block person
            merge_log.append({
                "key": ck,
                "key_type": "company",
                "kept": seen_company[ck].get("company", ""),
                "merged": rec.get("company", ""),
                "reason": "company-domain-collision",
            })

        if pk:
            seen_person[pk] = rec
        if ck:
            seen_company[ck] = rec
        output.append(rec)

    return {
        "deduplicated": output,
        "merge_log": merge_log,
        "dedup_count": len(merge_log),
    }


def main():
    parser = argparse.ArgumentParser(description="Deduplicate lead records")
    parser.add_argument("--existing-crm", default=None,
                        help="Path to JSON file with existing CRM records for cross-dedup")
    args = parser.parse_args()

    records = json.load(sys.stdin)
    if not isinstance(records, list):
        print("ERROR: Expected JSON array from stdin", file=sys.stderr)
        sys.exit(1)

    existing = None
    if args.existing_crm:
        with open(args.existing_crm) as f:
            existing = json.load(f)

    result = dedup(records, existing)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
