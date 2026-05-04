#!/usr/bin/env python3
"""Push to CRM — reads JSON from stdin, routes to CRM adapter.

Usage:
    echo '{"tags":"#cold-calling #function-3", "relevance":"..."}' | \
        python3 push_to_crm.py

Reads AGENTIC_APP_TOKEN and CRM_URL from environment.
Default CRM_URL: http://localhost:4210
"""

import json
import os
import sys
import urllib.request
import urllib.error


def push_to_crm(payload: dict) -> dict:
    crm_url = os.environ.get("CRM_URL", "http://localhost:4210")
    token = os.environ.get("AGENTIC_APP_TOKEN", "")

    url = f"{crm_url}/api/push"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"CRM push failed: {e.code} {e.reason}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"CRM unreachable: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    payload = json.load(sys.stdin)

    if "source" not in payload:
        payload["source"] = "skill:cold-calling:v2.1.0"

    result = push_to_crm(payload)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
