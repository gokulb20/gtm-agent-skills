#!/usr/bin/env python3
"""Push structured records to agentic-app CRM via POST /api/push."""
import json
import os
import sys
import urllib.request
import urllib.error


def push(records: list[dict], source: str = "") -> dict:
    """Push a list of records to agentic-app CRM.

    Each record must have an 'entity_type' field: 'company', 'person', or 'interaction'.
    """
    crm_url = os.environ.get("GTM_CRM_URL", os.environ.get("CRM_URL", "http://localhost:4210"))
    token = os.environ.get("AGENTIC_APP_TOKEN", "")
    if not token:
        return {"status": "error", "message": "AGENTIC_APP_TOKEN not set"}

    results = {"pushed": 0, "errors": [], "skipped": 0}
    for record in records:
        entity_type = record.pop("entity_type", "interaction")
        record["source"] = record.get("source", source)
        data = json.dumps(record).encode()
        req = urllib.request.Request(
            f"{crm_url}/api/push",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    results["pushed"] += 1
                else:
                    results["errors"].append({"status": resp.status, "record": record.get("company", "unknown")})
        except urllib.error.URLError as e:
            results["errors"].append({"error": str(e), "record": record.get("company", "unknown")})
        except Exception as e:
            results["errors"].append({"error": str(e), "record": record.get("company", "unknown")})

    return results


if __name__ == "__main__":
    source_tag = sys.argv[1] if len(sys.argv) > 1 else ""
    data = json.load(sys.stdin)
    if isinstance(data, dict):
        data = [data]
    for record in data:
        record.setdefault("entity_type", "interaction")
    result = push(data, source=source_tag)
    print(json.dumps(result, indent=2))
    if result["errors"]:
        sys.exit(1)
