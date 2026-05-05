#!/usr/bin/env python3
"""Push structured records to CSV files for offline CRM use."""
import csv
import json
import os
import sys
from datetime import datetime


def push(records: list[dict], output_dir: str = ".") -> dict:
    """Write records to CSV files organized by entity type."""
    os.makedirs(output_dir, exist_ok=True)
    results = {"written": 0, "files": []}

    by_type: dict[str, list[dict]] = {}
    for record in records:
        entity_type = record.pop("entity_type", "interaction")
        by_type.setdefault(entity_type, []).append(record)

    for entity_type, recs in by_type.items():
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        filepath = os.path.join(output_dir, f"{entity_type}_{timestamp}.csv")

        all_keys = set()
        for rec in recs:
            all_keys.update(rec.keys())
        fieldnames = sorted(all_keys)

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for rec in recs:
                writer.writerow(rec)

        results["written"] += len(recs)
        results["files"].append(filepath)

    return results


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./crm_exports"
    data = json.load(sys.stdin)
    if isinstance(data, dict):
        data = [data]
    for record in data:
        record.setdefault("entity_type", "interaction")
    result = push(data, output_dir=output_dir)
    print(json.dumps(result, indent=2))
