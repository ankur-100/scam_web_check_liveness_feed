# icanactagainstscams.gov.sg/scam-trends — feed structure

Captured 2026-11-25 (latest record 2026-11-24). Raw captures in `raw/`, extractor in `extract.py`.

## TL;DR

- **One GET returns the whole feed.** `/scam-trends` server-renders all **209** advisories
  (2025-08-28 → 2026-11-24) into the Next.js RSC flight stream as the prop `scamAdvisories`.
  `?page=N` just sets `initialPage`. The client shows 8 per page and filters in the browser.
  `?page=2` carries the identical 209 records. There's no need to crawl the detail pages.
- **No lifecycle fields.** There's no `status`, `active`, `expires`, `valid_until`, `severity` or
  `reported_by` field. Nothing in the 209 bodies says something like "expired", "taken down" or
  "Update:". The only time fields are `date_created` and `date_updated`.
- **Classification is a key/value tag list with two keys only:** `Scam Category` (10 values) and
  `Brand` (159 values). **`Brand` is the *impersonated* entity, not the issuing agency.**
  "LTA ×18" means 18 advisories about scams *posing as* LTA. LTA did not publish them.
- **The issuer is effectively always SPF.** 124 of 209 bodies open with "Singapore Police Force (SPF)
  has observed …", 31 with "We …", and the rest are also SPF phrasings ("The SPF observes …").
  No agency other than SPF issues anything here. **SCDF does not appear anywhere** (not as issuer,
  not as brand).
- These are not CVEs. They're consumer-scam advisories whose only machine-readable indicators of
  compromise (IOCs) are domain names (`scam_site_urls`).

## Transport: how the data reaches the browser

| Layer | Finding |
|---|---|
| Framework | Next.js App Router. HTML has `self.__next_f.push([1,"…"])` script tags whose concatenation is the RSC flight stream |
| Backend | Directus CMS. Field names `directus_files_id`, `filename_disk`; junction `scamsexposed_tags_id` → collection is likely `scamsexposed` with an M2M `scamsexposed_tags` |
| Listing prop | Row `8:` → `["$","$L16","1",{"scamAdvisories":[…209…],"initialPage":N}]` |
| Long text | Bodies are hoisted into length-prefixed text rows `<id>:T<hex byte len>,<markdown>` and referenced as `"content":"$17"`. 192 of 209 are hoisted and 17 are inline. **Rows are NOT newline-separated after a T row**, so you need a byte-level stream parser (see `rows()` in extract.py) |
| Pagination | Client-only: `useState(8*initialPage)`, "Load More" adds 8 more |
| Client filter | Search on `title`/`content` substring plus tag match. The filter chips come from unique `Scam Category` tags |
| Displayed date | `date_updated ?? date_created`, formatted `DD MMM YYYY`. Page header "Last updated" = newest of these |
| Images | `/api/assets/{file_id}/{filename_disk}`. A Next route proxies Directus assets (screenshots of the scam sites) |
| Detail page | `/scam-trends/{slug}-{id[:8]}`. Rendered HTML plus JSON-LD (`Article` + `BreadcrumbList`) plus OG `article:published_time/modified_time`. **No extra fields** beyond the listing record |
| Slug | `slug(title)` strips "Advisory:" and leading "Beware of / Protect yourself from …", applies NFKD, lowercases, hyphenates, caps at 60 characters on a word boundary, then appends `-{id[:8]}`. Ported in `extract.py:slug()`, verified 8/8 against real links |

Not examined: the Directus REST API (`/api/items/...`, `/api/fields/...`). My probe GETs to those
paths were blocked by the session's permission policy, so I never made them. Directus collections
usually have a `status` (published/draft/archived) field. The server query probably filters on it
and doesn't project it, so an archive or "inactive" state may exist on the backend but is **not
exposed to the public**. This is unverified.

## Record schema (exactly as served)

```jsonc
{
  "id": "b633b3b7-f3f5-4e06-b96c-05f0ce86c9ed",   // UUID; id[:8] used in URL
  "date_created": "2026-11-24T02:23:28.255Z",     // = JSON-LD datePublished
  "date_updated": "2026-11-24T02:28:09.810Z",     // = dateModified; never null in this snapshot
  "sort": null,                                   // always null (209/209)
  "title": "Advisory: Beware of Fake Singapore Police Force Websites and Messages",
  "content": "$17",                               // ref to markdown T-row, or inline markdown
  "scam_site_urls": "[\"drbypass-proxy.pages.dev\"]", // STRINGIFIED JSON array (client JSON.parses; also accepts real array)
  "occurrences": null,                            // always null (209/209) — unused field, possibly a planned counter
  "images": [ { "directus_files_id": { "id": "<uuid>", "filename_disk": "<uuid>.png" } } ],
  "tags": [
    { "scamsexposed_tags_id": { "id": "<uuid>", "key": "Scam Category", "value": "Impersonation" } },
    { "scamsexposed_tags_id": { "id": "<uuid>", "key": "Brand", "value": "Singapore Police Force (SPF)" } }
  ]
}
```

Field coverage over 209 records: every field is present on every record. Images: 312 total
(1–n per record). Tags: 463 total.

## Classification

**Scam Category** (213 uses; 4 records have 2 categories):
Investment 69 · Non-Banking Related Phishing 68 · Impersonation 32 · Job 25 · Banking Related Phishing 7 ·
Phishing 5 · E-Commerce 4 · Malware 1 · Loan 1 · Visa 1.
"Phishing" overlaps with the two split phishing values and looks like a legacy value.

**Brand** (250 uses, 159 distinct). Combinations per record: 1 brand 170, 2 brands 27, 3–4 brands 7,
**no brand 2**, and a literal value "No Brand" in 2 more records. Values are free text, not
normalized. Casing is inconsistent ("moburst", "lyft bikes"), and there are no stable entity IDs
apart from the tag UUID, which *is* stable per value and is the best join key.

Government or public-sector brands (impersonated):
LTA 18 · SPF 5 · IRAS 5 · CDC Vouchers 4 · Singpass 2 · Gov.sg 2 · ICA 2 · SimplyGo 1 · SingHealth 1 ·
SGAC 1 · CPF Board 1 · PTVE 1 · NEA 1 · HTX 1 · MHA 1.

**Scam domains**: 1–9 per record (1: 137, 2: 45, 3: 21, more: 6). Top TLDs are com, top, cc,
cfd, shop, net and vip. They are bare hostnames (sometimes with a path), unfanged, with no scheme.

## What you can and can't derive

| Wanted | Available? | How |
|---|---|---|
| Expiry / active flag | ❌ not in payload | Infer it yourself: age since `date_updated`, plus live DNS/HTTP checks on `scam_domains` |
| Issuing agency | ❌ no field | Constant SPF. A regex on the body opener confirms it, so it isn't worth a field |
| Impersonated entity (LTA, IRAS…) | ✅ `Brand` tag | Map tag values (or tag UUIDs) to a canonical entity table. `extract.py` flags gov-looking ones with a regex; replace that with a hand-made map for production |
| Scam type | ✅ `Scam Category` tag | 10-value enum |
| IOCs | ✅ `scam_site_urls` | Must `json.loads` the string |
| Revision history | ⚠️ partial | Only latest `date_updated`. 16 records were edited a day or more after creation. To track changes, snapshot daily and diff |
| Incremental sync | ⚠️ no cursor/ETag found | Whole set each time (~570 KB HTML). Diff on `id` + `date_updated` |

## Files

- `extract.py`: fetch or parse → `advisories_raw.json` (verbatim records, bodies resolved) +
  `advisories.jsonl` (normalized: url, categories, brands, gov-brands, domains, image URLs, markdown body)
- `raw/scam-trends_2026-11-25.html`, `raw/detail_spf_b633b3b7.html`, `raw/scam-trends-page.js`: evidence

## Fragility

This works by scraping RSC internals rather than calling a contract API. Breakage signals: the prop
name `scamAdvisories` disappearing (extract.py raises), the T-row format changing, or the site moving
to client-side fetching. The prop name and field names come straight from Directus, so they should
stay stable while the CMS schema stays the same.
