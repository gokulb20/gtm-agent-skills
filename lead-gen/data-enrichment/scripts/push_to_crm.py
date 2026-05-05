#!/usr/bin/env python3
"""push_to_crm.py — Reads JSON from stdin, routes to CRM adapter.

Usage:
    cat leads.json | python push_to_crm.py [--adapter agentic-app|csv|none]

Reads lead records as JSON from stdin and pushes them to the configured
CRM adapter. For agentic-app adapter, POSTs to CRM_URL/api/push with
Authorization header from AGENTIC_APP_TOKEN.

Environment:
    CRM_URL            — agentic-app CRM endpoint (default: http://localhost:4210)
    AGENTIC_APP_TOKEN  — Bearer token for CRM push
    CRM_ADAPTER        — Adapter to use (default: agentic-app)
"""
import json
import os
import sys
import argparse
import urllib.request
import urllib.error


def push_to_agentic_app(records: list[dict], crm_url: str, token: str) -> dict:
    """Push records to agentic-app CRM via POST /api/push."""
    results = {"pushed": 0, "errors": []}
    for rec in records:
        payload = json.dumps(rec).encode("utf-8")
        req = urllib.request.Request(
            f"{crm_url}/api/push",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                results["pushed"] += 1
        except urllib.error.URLError as e:
            results["errors"].append({"record": rec.get("contactName", "unknown"), "error": str(e)})
    return results


def push_to_csv(records: list[dict], filepath: str = "crm_export.csv") -> dict:
    """Write records to CSV file as a fallback adapter."""
    import csv
    if not records:
        return {"pushed": 0, "errors": []}
    keys = list(records[0].keys())
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
    return {"pushed": len(records), "errors": []}


def main():
    parser = argparse.ArgumentParser(description="Push lead records to CRM")
    parser.add_argument("--adapter", default=os.environ.get("CRM_ADAPTER", "agentic-app"),
                        choices=["agentic-app", "csv", "none"],
                        help="CRM adapter to use")
    args = parser.parse_args()

    records = json.load(sys.stdin)
    if not isinstance(records, list):
        print("ERROR: Expected JSON array from stdin", file=sys.stderr)
        sys.exit(1)

    if args.adapter == "none":
        print(f"DRY RUN: {len(records)} records would be pushed (adapter=none)", file=sys.stderr)
        sys.exit(0)

    if args.adapter == "agentic-app":
        crm_url = os.environ.get("CRM_URL", "http://localhost:4210")
        token = os.environ.get("AGENTIC_APP_TOKEN", "")
        if not token:
            print("ERROR: AGENTIC_APP_TOKEN not set", file=sys.stderr)
            sys.exit(1)
        result = push_to_agentic_app(records, crm_url, token)
    elif args.adapter == "csv":
        result = push_to_csv(records)
    else:
        print(f"ERROR: Unknown adapter '{args.adapter}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
