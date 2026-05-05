#!/usr/bin/env python3
"""Push ab-testing-messaging records to CRM via agentic-app API.

Reads JSON from stdin, routes to the appropriate CRM adapter,
and POSTs each record to CRM_URL/api/push.

Source tag: skill:ab-testing-messaging:v2.1.0
"""

import json
import os
import sys
import urllib.request
import urllib.error

SKILL_NAME = "ab-testing-messaging"
SKILL_VERSION = "2.1.0"
SOURCE_TAG = f"skill:{SKILL_NAME}:{SKILL_VERSION}"


def get_crm_url() -> str:
    return os.environ.get("CRM_URL", "http://localhost:4210")


def get_token() -> str:
    return os.environ.get("AGENTIC_APP_TOKEN", "")


def push_record(record: dict) -> dict:
    crm_url = get_crm_url()
    token = get_token()
    record["source"] = SOURCE_TAG

    url = f"{crm_url}/api/push"
    data = json.dumps(record).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        return {"error": True, "status": e.code, "body": body}
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return {"error": True, "message": str(e)}


def main():
    adapter = os.environ.get("GTM_CRM_ADAPTER", "agentic-app")
    if adapter == "none":
        print("CRM adapter set to 'none', skipping push.", file=sys.stderr)
        return

    try:
        records = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(records, list):
        records = [records]

    results = [push_record(r) for r in records]
    json.dump(results, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
