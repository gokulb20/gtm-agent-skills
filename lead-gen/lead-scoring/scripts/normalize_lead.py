#!/usr/bin/env python3
"""normalize_lead.py — Normalizes a raw lead record to the canonical lead schema.

Usage:
    cat raw_leads.json | python normalize_lead.py [--source apollo-api]

Reads raw lead records from stdin (JSON array), normalizes each to the
canonical Lead schema per the function-2 conventions. Outputs normalized
records to stdout.

Normalizations applied:
- Title cleanup (strip "@ Foo | Investor" suffixes)
- Seniority inference from title
- Function inference from title + department
- Company domain extraction (apex domain, strip www)
- Email status defaulting
- Provenance tagging based on source
"""
import json
import re
import sys
import argparse


# Seniority inference patterns
SENIORITY_MAP = {
    r"\b(cxo|c[- ]?level|chief|ceo|cto|cfo|coo|cpo|cro|cmo)\b": "c-level",
    r"\bvp\b|\bvice president\b": "vp",
    r"\bdirector\b": "director",
    r"\bmanager\b|\bhead of\b": "manager",
    r"\bintern\b": "intern",
}

# Function inference patterns
FUNCTION_MAP = {
    r"\bsales\b|\bbdr\b|\bsdr\b|\bae\b": "sales",
    r"\bmarketing\b|\bgrowth\b|\bdemand gen\b": "marketing",
    r"\bengineering\b|\bdev\b|\bdeveloper\b|\bcto\b": "engineering",
    r"\bops\b|\boperations\b": "ops",
    r"\bhr\b|\bpeople\b|\btalent\b": "hr",
    r"\bfinance\b|\baccounting\b|\bfp[& ]?a\b": "finance",
    r"\bsupport\b|\bcustomer success\b|\bcx\b": "support",
    r"\blegal\b|\bcounsel\b": "legal",
    r"\bproduct\b|\bpm\b": "product",
}


def infer_seniority(title: str) -> str:
    """Infer seniority from title string."""
    title_lower = title.lower()
    for pattern, seniority in SENIORITY_MAP.items():
        if re.search(pattern, title_lower):
            return seniority
    return "unknown"


def infer_function(title: str, department: str = "") -> str:
    """Infer function from title and department."""
    combined = f"{title} {department}".lower()
    for pattern, function in FUNCTION_MAP.items():
        if re.search(pattern, combined):
            return function
    return "other"


def clean_title(title_raw: str) -> str:
    """Strip common suffixes from raw titles."""
    # Remove "@ Company | Investor" patterns
    cleaned = re.sub(r"\s*@\s*\S+.*$", "", title_raw)
    # Remove trailing pipe-separated roles
    cleaned = re.sub(r"\s*\|.*$", "", cleaned)
    return cleaned.strip()


def extract_apex_domain(domain: str) -> str:
    """Extract apex domain, strip subdomains except www."""
    if not domain:
        return ""
    domain = domain.lower().strip()
    # Remove protocol
    domain = re.sub(r"^https?://", "", domain)
    # Remove path
    domain = domain.split("/")[0]
    # Remove www
    domain = re.sub(r"^www\.", "", domain)
    return domain


def normalize_record(raw: dict, source: str) -> dict:
    """Normalize a single raw record to the canonical Lead schema."""
    title_raw = raw.get("title", raw.get("contactTitle", ""))
    title_normalized = clean_title(title_raw)

    return {
        "lead_id": raw.get("lead_id", ""),
        "linkedin_url": raw.get("linkedin_url", raw.get("contactLinkedIn", "")),
        "email": raw.get("email", raw.get("contactEmail", "")),
        "phone": raw.get("phone", raw.get("contactPhone", "")),
        "email_status": raw.get("email_status", "unverified"),
        "phone_status": raw.get("phone_status", "unverified"),
        "contact_name": raw.get("contact_name", raw.get("contactName", raw.get("name", ""))),
        "title_raw": title_raw,
        "title_normalized": title_normalized,
        "seniority": raw.get("seniority") or infer_seniority(title_normalized),
        "function": raw.get("function") or infer_function(title_normalized, raw.get("department", "")),
        "company": raw.get("company", raw.get("organization_name", "")),
        "company_domain": extract_apex_domain(
            raw.get("company_domain", raw.get("website", raw.get("organization_website", "")))
        ),
        "company_size_band": raw.get("company_size_band", raw.get("companySize", "")),
        "company_industry_normalized": raw.get("company_industry_normalized", raw.get("industry", "")),
        "company_location": raw.get("company_location", raw.get("location", "")),
        "company_funding_stage": raw.get("company_funding_stage", ""),
        "signals": raw.get("signals", []),
        "personalization_hook": raw.get("personalization_hook"),
        "provenance_company": raw.get("provenance_company", "unverified"),
        "provenance_person": raw.get("provenance_person", "unverified"),
        "provenance_email": raw.get("provenance_email", "unverified"),
        "source": source,
        "source_run_id": raw.get("source_run_id", ""),
        "freshness_date": raw.get("freshness_date", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Normalize raw lead records")
    parser.add_argument("--source", default="unknown",
                        help="Source tag for provenance (e.g. apollo-api, linkedin-sales-nav)")
    args = parser.parse_args()

    raw_records = json.load(sys.stdin)
    if not isinstance(raw_records, list):
        print("ERROR: Expected JSON array from stdin", file=sys.stderr)
        sys.exit(1)

    normalized = [normalize_record(r, args.source) for r in raw_records]
    print(json.dumps(normalized, indent=2))


if __name__ == "__main__":
    main()
