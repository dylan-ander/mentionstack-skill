# Changelog

## 0.2.0

- First public release. Marketplace renamed to `dylanander`. Internal notes and paths removed.


All notable changes to the Mentionstack plugin are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.2] — 2026-08-28

### Fixed

- **`seo/content-writer/SKILL.md` + `references/humanization-rules.md` — corrected the reading-level spec.** The old text said "Reading level: 10th grade. Flesch-Kincaid 60-70," but 60-70 is the Flesch Reading Ease scale, not a grade level. Replaced with the rule the readability rule actually enforced: "10th grade reading level maximum (validator rejects Flesch-Kincaid grade above 10.5 or SMOG above 12). Prefer plain short words over long ones." Updated in the Step 6 non-negotiables, the Step 7 manual review checklist, and humanization rule 7.

---

## [0.1.1] — 2026-05-07

### Fixed

- **`seo/content-writer/SKILL.md` — slug computation works on macOS.** Replaced the GNU-sed `s/[^a-z0-9]\+/-/g` pattern (which silently no-ops in BSD sed and leaves spaces in directory names) with a Python one-liner that produces the same slug across platforms. Surfaced on first real invocation when "collagen gummies for skin" became a directory with literal spaces and broke downstream file writes.
- **`seo/content-writer/references/blacklist.txt` — removed false-positive labels.** "Primary" and "Secondary" are normal SEO-jargon labels in metadata blocks ("Primary keyword: X", "Secondary keywords: Y") but were being flagged as banned in the deliverable scan. Removed both terms from the blacklist; "Tertiary" left in (less common, more often an AI tell). Both terms were already absent from body prose in the v0.1.0 humanization rules.

---

## [0.1.0] — 2026-05-07

### Initial scaffold

Forked from `nowork-studio/toprank` v0.13.0. Stripped Google Ads skills, AdsAgent MCP server config, public marketplace branding, and toprank-specific update/test infrastructure. Renamed plugin namespace from `toprank` to `mentionstack` and marketplace owner from `nowork-studio` to `dataatms`.

Skills carried over from toprank as starting points — these will be progressively re-engineered toward GEO/AEO-first delivery using DataForSEO instead of GSC:

- `seo/seo-analysis`
- `seo/content-writer`
- `seo/keyword-research`
- `seo/meta-tags-optimizer`
- `seo/schema-markup-generator`
- `seo/setup-cms`
- `gemini`

State directory moved from `~/.toprank/` to `~/.mentionstack/`.

Removed:
- `google-ads/` (4 skills — Mentionstack is not an ads agency)
- `toprank-upgrade-skill/` (toprank-specific public-marketplace update infra)
- `seo/seo-page/` (orphan, unregistered)
- `bin/toprank-update-check`, `bin/toprank-config`, `bin/toprank-change-watch`, `bin/preamble.md` (public-marketplace update infra)
- `test/`, `conftest.py`, `requirements-test.txt` (toprank-specific test harness — Mentionstack tests will be rebuilt)
- `.mcp.json` (referenced AdsAgent MCP server)
- `server.json` (registry entry for the public AdsAgent server)
