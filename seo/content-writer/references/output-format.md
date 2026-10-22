# Mentionstack content output format

Every blog post and landing page is delivered in this exact structure. Skipping any section is a delivery rejection.

## Output structure

The deliverable is a single Markdown document with these sections, in this order:

### 1. The article

```
# <Title — H1, primary keyword front-loaded, under 60 chars>

[First two sentences: empathetic + relatable hook. The reader must feel they
clicked the right article and want to keep reading.]

[Body — H2s and H3s as outlined in the brief. Apply the persona's mix of 1st
and 3rd person, subjective opinion and objective cited fact.]

[Outbound links inline as Markdown hyperlinks: [anchor text](https://source.example.com/page)]

[Internal interlinks inline as Markdown hyperlinks to client pages.]
```

### 2. SEO metadata block

```
## SEO metadata

- **Title tag:** <under 60 chars, primary keyword front-loaded>
- **Meta description:** <120-160 chars, includes primary keyword + benefit>
- **URL slug:** /<lowercase-hyphenated-slug>
- **Primary keyword:** <kw>
- **Secondary keywords:** <kw1>, <kw2>, <kw3>
```

### 3. Cited sources block

Every outbound link must appear here with full attribution. Order by appearance in the article.

```
## Cited sources

1. <Title> — <Publisher>, <YYYY-MM-DD> — <URL>
2. <Title> — <Publisher>, <YYYY-MM-DD> — <URL>
3. ...
```

### 4. Structured data

JSON-LD ready to paste into the page head. Always include `Article` (or `BlogPosting` for blog posts). Add `FAQPage` if the article has an FAQ section. Add `HowTo` if it's a step-by-step procedure.

```
## JSON-LD structured data

\`\`\`json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "datePublished": "YYYY-MM-DD",
  "author": { "@type": "Person", "name": "..." },
  "publisher": { "@type": "Organization", "name": "...", "logo": { "@type": "ImageObject", "url": "..." } },
  "image": "...",
  "mainEntityOfPage": "..."
}
\`\`\`
```

### 5. Interlink plan

Both directions — pages that should link TO this new piece, and pages this piece links FROM.

```
## Interlink plan

- **From this page TO:**
  - "<anchor text>" → <internal page URL>
  - "<anchor text>" → <internal page URL>
- **TO this page FROM:**
  - <internal page URL> with anchor "<text>"
  - <internal page URL> with anchor "<text>"
```

### 6. Publishing checklist

```
## Publishing checklist

- [ ] Title tag and meta description set
- [ ] URL slug configured
- [ ] JSON-LD structured data added to page head
- [ ] All outbound links verified live (HTTP 200)
- [ ] All internal interlinks placed (both directions)
- [ ] Open Graph image added
- [ ] Canonical URL set to self
- [ ] Mobile rendering verified
- [ ] Blacklist check passed (`scripts/blacklist_check.py`)
```

## Title and meta rules

- **Title tag:** under 60 chars, primary keyword in the first half. Do not pad with the brand name unless it shortens the title.
- **Meta description:** 120-160 chars. Includes the primary keyword and a benefit. Should read like an organic SERP snippet, not an ad.
- **URL slug:** lowercase, hyphenated, 3-6 words, no stopwords ("the," "a," "of") unless they meaningfully change meaning. Do not include the date or year unless evergreen-time-stamping is intentional.

## H1 / H2 / H3 rules

- **One H1 per page.** It matches the title tag's intent but does not have to match word-for-word.
- **H2s answer the searcher's questions in order of importance.** Lead with the H2 that resolves the core query, not "What is X?"
- **H3s** break up long H2s. Use them when an H2 has more than 3-4 paragraphs.
- **No skipped levels.** Never go H1 → H3.
