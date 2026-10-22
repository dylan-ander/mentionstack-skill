#!/usr/bin/env python3
"""
DataForSEO API CLI for ad-hoc Mentionstack queries.

Loads credentials from ~/.mentionstack/credentials.env, then falls back to env vars.

Usage:
  python bin/dataforseo.py serp "<keyword>" [--location "United States"] [--language en]
  python bin/dataforseo.py keyword-data "<kw1>,<kw2>,..."
  python bin/dataforseo.py related "<seed>" [--limit 50]

All commands print full DataForSEO JSON to stdout. Errors to stderr.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
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
            v = v.strip().strip('"').strip("'")
            os.environ.setdefault(k.strip(), v)

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
    req = Request(
        f"{API_BASE}{path}",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        sys.stderr.write(f"HTTP {e.code} on {path}: {e.read().decode()}\n")
        sys.exit(1)
    except URLError as e:
        sys.stderr.write(f"Network error on {path}: {e.reason}\n")
        sys.exit(1)


def serp(keyword: str, location: str = "United States", language: str = "en") -> dict:
    return _post(
        "/serp/google/organic/live/advanced",
        [{
            "keyword": keyword,
            "location_name": location,
            "language_code": language,
            "device": "desktop",
            "depth": 20,
        }],
    )


def keyword_data(keywords: list, location: str = "United States", language: str = "en") -> dict:
    return _post(
        "/keywords_data/google_ads/search_volume/live",
        [{
            "keywords": keywords,
            "location_name": location,
            "language_code": language,
        }],
    )


def related_keywords(seed: str, location: str = "United States", language: str = "en", limit: int = 50) -> dict:
    return _post(
        "/keywords_data/google_ads/keywords_for_keywords/live",
        [{
            "keywords": [seed],
            "location_name": location,
            "language_code": language,
            "limit": limit,
        }],
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="dataforseo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("serp")
    p.add_argument("keyword")
    p.add_argument("--location", default="United States")
    p.add_argument("--language", default="en")

    p = sub.add_parser("keyword-data")
    p.add_argument("keywords", help="Comma-separated keywords")
    p.add_argument("--location", default="United States")
    p.add_argument("--language", default="en")

    p = sub.add_parser("related")
    p.add_argument("seed")
    p.add_argument("--location", default="United States")
    p.add_argument("--language", default="en")
    p.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()

    if args.cmd == "serp":
        result = serp(args.keyword, args.location, args.language)
    elif args.cmd == "keyword-data":
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        result = keyword_data(kws, args.location, args.language)
    elif args.cmd == "related":
        result = related_keywords(args.seed, args.location, args.language, args.limit)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
