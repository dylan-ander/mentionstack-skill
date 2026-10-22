# mentionstack-skill

A GEO/AEO/SEO toolkit for Claude Code. Live DataForSEO research, scientific content briefs, humanized drafts, keyword research, schema markup, meta tags, and full SEO audits.

Built by [Dylan Ander](https://github.com/dylan-ander). Forked from [nowork-studio/toprank](https://github.com/nowork-studio/toprank) (MIT).

## Install

```
/plugin marketplace add dylan-ander/mentionstack-skill
/plugin install mentionstack@dylanander
```

Skills show up as `/mentionstack:<skill-name>`.

## Skills

| Skill | What it does |
|-------|-------------|
| `content-writer` | DataForSEO-driven blog posts and landing pages. Writes a brief first (hypothesis, target keywords, target LLMs, expected outcome), waits for your approval, then drafts with humanization rules and a banned-words check. |
| `seo-analysis` | Full SEO audit from Google Search Console and PageSpeed: quick wins, technical issues, 30-day plan. |
| `keyword-research` | Keyword discovery, intent classification, topic clusters, content calendar. |
| `meta-tags-optimizer` | Title tags, meta descriptions, OG/Twitter cards with A/B variations. |
| `schema-markup-generator` | JSON-LD: FAQ, HowTo, Article, Product, LocalBusiness. |
| `setup-cms` | Connect WordPress, Strapi, Contentful, or Ghost. |
| `gemini` | Second opinion from Google Gemini CLI. |

## Setup

Bring your own keys. Set them as env vars or put them in `~/.mentionstack/.env`. Nothing is sent anywhere except the provider APIs.

| Var | Needed for |
|-----|-----------|
| `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | content-writer, keyword research ([dataforseo.com](https://dataforseo.com), pay as you go) |
| `PAGESPEED_API_KEY` | seo-analysis (optional) |
| Google Search Console auth (`gcloud auth application-default login`) | seo-analysis. See `seo/seo-analysis/references/gsc_setup.md` |
| `WP_*`, `STRAPI_*`, `CONTENTFUL_*`, `GHOST_*` | setup-cms (optional) |
| Gemini CLI installed | gemini skill |

Python deps: `pip install -r requirements.txt`

## Client profiles

`content-writer` keeps a per-brand profile (voice, ICP, competitors) at `~/.mentionstack/clients/<name>.json`. First run asks you the questions and saves it. Profiles stay local.

## Feedback

Open an issue or PR. Reviews welcome.

## License

MIT. See [LICENSE](LICENSE).
