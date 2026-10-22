#!/usr/bin/env python3
"""
Scan a draft for Mentionstack-blacklisted words and phrases.

Usage:
  python blacklist_check.py <path-to-draft.md>

Exit codes:
  0 — clean, no violations
  1 — violations found, listed to stderr
  2 — usage / file-not-found error

The blacklist is read from ../references/blacklist.txt (one term per line, comments
allowed with #). Single-token entries match as case-insensitive whole words; entries
containing spaces, hyphens, or slashes match as case-insensitive substrings.
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BLACKLIST_FILE = SCRIPT_DIR.parent / "references" / "blacklist.txt"


def load_blacklist() -> list:
    if not BLACKLIST_FILE.exists():
        sys.stderr.write(f"Blacklist file missing: {BLACKLIST_FILE}\n")
        sys.exit(2)
    return [
        line.strip()
        for line in BLACKLIST_FILE.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def find_violations(text: str, blacklist: list) -> list:
    """Return list of (term, line_number, context) tuples."""
    violations = []
    lines = text.splitlines()
    for term in blacklist:
        if any(c in term for c in (" ", "-", "/")):
            pattern = re.compile(re.escape(term), re.IGNORECASE)
        else:
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)

        for match in pattern.finditer(text):
            line_num = text[: match.start()].count("\n") + 1
            ctx = lines[line_num - 1].strip() if line_num <= len(lines) else ""
            violations.append((term, line_num, ctx))

    return violations


def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: blacklist_check.py <path-to-draft.md>\n")
        sys.exit(2)

    draft_path = Path(sys.argv[1])
    if not draft_path.exists():
        sys.stderr.write(f"Draft not found: {draft_path}\n")
        sys.exit(2)

    text = draft_path.read_text()
    blacklist = load_blacklist()
    violations = find_violations(text, blacklist)

    if not violations:
        print("PASS — no banned words detected")
        return

    by_term: dict = {}
    for term, line_num, ctx in violations:
        by_term.setdefault(term, []).append((line_num, ctx))

    sys.stderr.write(
        f"FAIL — {len(violations)} violation(s) across {len(by_term)} banned term(s):\n\n"
    )
    for term in sorted(by_term):
        occurrences = by_term[term]
        sys.stderr.write(f"  '{term}' — {len(occurrences)} occurrence(s):\n")
        for line_num, ctx in occurrences[:3]:
            preview = ctx[:120] + "..." if len(ctx) > 120 else ctx
            sys.stderr.write(f"    line {line_num}: {preview}\n")
        if len(occurrences) > 3:
            sys.stderr.write(f"    ... and {len(occurrences) - 3} more\n")
        sys.stderr.write("\n")

    sys.exit(1)


if __name__ == "__main__":
    main()
