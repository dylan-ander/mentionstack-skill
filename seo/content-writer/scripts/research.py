#!/usr/bin/env python3
"""
Mentionstack content research — runs DataForSEO calls and assembles a brief-ready
research report for a target keyword.

Usage:
  python research.py "<keyword>" [--client <name>] [--location "United States"] [--language en]

Output: JSON report to stdout containing:
  - search volume, competition, CPC for the primary keyword
  - top 10 organic SERP results
  - AI Overview content + reference URLs (when Google shows one)
  - top 20 related keywords by search volume
  - SERP shape signal (dominant content format among top results)

Errors to stderr. Exit 1 on API failure, 2 on usage error.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE = "https://api.dataforseo.com/v3"
CREDENTIALS_FILE = Path.home() / ".mentionstack" / "credentials.env"


def _load_credentials() -> tuple[str, str]:
    if CREDENTIALS_FILE.exists():
        for line in CREDENTIALS_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        sys.stderr.write(
            f"DataForSEO credentials missing. Set DATAFORSEO_LOGIN and "
            f"DATAFORSEO_PASSWORD in env or {CREDENTIALS_FILE}\n"
        )
        sys.exit(2)
    return login, password


def _post(path: str, payload: list) -> dict:
    login, password = _load_credentials()
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
    req = Request(f"{API_BASE}{path}", data=json.dumps(payload).encode(), headers=headers, method="POST")
    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        sys.stderr.write(f"HTTP {e.code} on {path}: {e.read().decode()[:500]}\n")
        sys.exit(1)
    except URLError as e:
        sys.stderr.write(f"Network error on {path}: {e.reason}\n")
        sys.exit(1)


def fetch_serp(keyword: str, location: str, language: str) -> dict:
    return _post("/serp/google/organic/live/advanced", [{
        "keyword": keyword,
        "location_name": location,
        "language_code": language,
        "device": "desktop",
        "depth": 20,
    }])


def fetch_keyword_data(keyword: str, location: str, language: str) -> dict:
    return _post("/keywords_data/google_ads/search_volume/live", [{
        "keywords": [keyword],
        "location_name": location,
        "language_code": language,
    }])


def fetch_related(seed: str, location: str, language: str, limit: int = 50) -> dict:
    return _post("/keywords_data/google_ads/keywords_for_keywords/live", [{
        "keywords": [seed],
        "location_name": location,
        "language_code": language,
        "limit": limit,
    }])


def _result_items(response: dict) -> list:
    try:
        return response["tasks"][0]["result"][0].get("items", []) or []
    except (KeyError, IndexError, TypeError):
        return []


def extract_organic(serp_response: dict) -> list:
    return [
        {
            "position": i.get("rank_absolute"),
            "url": i.get("url"),
            "title": i.get("title"),
            "snippet": i.get("description"),
            "domain": i.get("domain"),
        }
        for i in _result_items(serp_response)
        if i.get("type") == "organic"
    ][:10]


def extract_ai_overview(serp_response: dict) -> dict | None:
    for item in _result_items(serp_response):
        if item.get("type") == "ai_overview":
            refs = item.get("references") or []
            return {
                "text": item.get("text") or item.get("markdown") or item.get("asynchronous_ai_overview"),
                "references": [{"url": r.get("url"), "domain": r.get("domain"), "title": r.get("title")} for r in refs],
            }
    return None


def extract_volume(kd_response: dict, keyword: str) -> dict:
    try:
        results = kd_response["tasks"][0]["result"] or []
        for r in results:
            if (r.get("keyword") or "").lower() == keyword.lower():
                return {
                    "search_volume": r.get("search_volume"),
                    "competition": r.get("competition"),
                    "competition_index": r.get("competition_index"),
                    "cpc": r.get("cpc"),
                }
    except (KeyError, IndexError, TypeError):
        pass
    return {}


def extract_related(rel_response: dict, limit: int = 20) -> list:
    try:
        items = rel_response["tasks"][0]["result"] or []
        items = sorted(items, key=lambda x: x.get("search_volume") or 0, reverse=True)
        return [
            {
                "keyword": i.get("keyword"),
                "search_volume": i.get("search_volume"),
                "competition": i.get("competition"),
                "cpc": i.get("cpc"),
            }
            for i in items[:limit]
        ]
    except (KeyError, IndexError, TypeError):
        return []


def infer_serp_shape(organic: list) -> str:
    """Best-effort signal from titles: listicle / guide / faq / comparison / unknown."""
    if not organic:
        return "unknown"
    counts: Counter = Counter()
    for r in organic:
        t = (r.get("title") or "").lower()
        if any(t.startswith(f"{n} ") or f" {n} " in t for n in ("5", "7", "10", "12", "15", "20", "best")):
            counts["listicle"] += 1
        elif "vs" in t or "vs." in t or "compared" in t:
            counts["comparison"] += 1
        elif "how to" in t or "guide" in t:
            counts["guide"] += 1
        elif "faq" in t or "questions" in t:
            counts["faq"] += 1
        else:
            counts["other"] += 1
    top, _ = counts.most_common(1)[0]
    return top


def main() -> None:
    parser = argparse.ArgumentParser(description="Mentionstack content research")
    parser.add_argument("keyword")
    parser.add_argument("--client", default="")
    parser.add_argument("--location", default="United States")
    parser.add_argument("--language", default="en")
    args = parser.parse_args()

    sys.stderr.write(f"Researching '{args.keyword}'...\n")

    sys.stderr.write("  SERP...\n")
    serp_resp = fetch_serp(args.keyword, args.location, args.language)

    sys.stderr.write("  Keyword data...\n")
    kd_resp = fetch_keyword_data(args.keyword, args.location, args.language)

    sys.stderr.write("  Related keywords...\n")
    rel_resp = fetch_related(args.keyword, args.location, args.language)

    organic = extract_organic(serp_resp)
    report = {
        "keyword": args.keyword,
        "client": args.client,
        "location": args.location,
        "language": args.language,
        "volume": extract_volume(kd_resp, args.keyword),
        "serp": {
            "shape_signal": infer_serp_shape(organic),
            "organic": organic,
            "ai_overview": extract_ai_overview(serp_resp),
        },
        "related_keywords": extract_related(rel_resp, limit=20),
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
