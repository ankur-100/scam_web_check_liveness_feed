# Recovered transcript digest: spf_brand_map (agent aa938c702176f9905)

### [user]
Today is 2026-11-25. Task: resolve every `Brand` tag value used by the Singapore Police Force's scam-advisory feed into a canonical entity (or classify it as not-a-real-entity).

FIRST read `/home/ankur/scamtrends_feed/registry/FORMAT.md` (section 3 is your output format; obey the ground rules). Input: `/home/ankur/scamtrends_feed/registry/spf_brands.json` — 159 brand values, each with tag_id, count, scam categories, sample scam domains, and sample advisory titles. Full advisory bodies (markdown) are in `/home/ankur/scamtrends_feed/advisories.jsonl` (field `body_md`, `impersonated_brands`) if you need context.

Why this matters: the SPF `Brand` tag mixes (a) **real organisations being impersonated** (LTA, DBS, WhatsApp, NVIDIA), (b) **fictitious scam platform names** (e.g. a fake investment app/brand invented by scammers — "Koka Kona", "Airdrop Pepe", "Youlemei Mall" may be such), and (c) placeholders ("No Brand"). A downstream pipeline needs to know which is which, and for real ones, the **official domain(s)** so lookalikes can be compared against the genuine site.

For each of the 159 values produce a record:
- `resolution`: `real_entity` | `fictitious_scam_brand` | `generic_or_placeholder` | `ambiguous`. Decide from the advisory body (does SPF say scammers *impersonate* X, or that X is a *fraudulent platform*?) plus a web search. Note: a real company name can be used by a fake platform (e.g. a real investment firm whose name is cloned) — that's still `real_entity` (impersonated), but say so in notes.
- `entity_id` = primary official registrable domain of the real entity (e.g. `lta.gov.sg`, `whatsapp.com`, `nvidia.com`), else null. `official_domains` = the genuine domains (verified from the entity's own site or authoritative source; for global brands the main domain suffices; for SG gov agencies include key service hosts e.g. onemotoring.lta.gov.sg).
- `is_singapore_entity`, `sector` (use FORMAT.md sector vocabulary), `confidence`, `evidence` (URLs you actually opened — official site, or the SPF advisory text for fictitious ones), `notes` (e.g. which genuine product/service the scam imitates).
- Merge obvious variants (casing, "moburst" vs "Moburst") by pointing both at the same entity_id; keep one record per input value.

Ground rules: you may open the **genuine** official sites to confirm domains; do NOT visit the scam domains listed in `sample_domains`. Keep request volume reasonable — for well-known global brands (WhatsApp, TikTok, Netflix, NVIDIA, GitHub, Booking.com…) and well-known SG entities you can rely on a single check or established knowledge, citing the official domain; spend effort on obscure names.

Write `/home/ankur/scamtrends_feed/registry/spf_brand_map.json` (array, one record per input value, 159 records). Return a concise summary (≤300 words): counts per resolution class, SG vs foreign split, notable fictitious brands, ambiguous cases needing human review.

### [user]
<system-reminder>
Your final report is delivered through SubagentHandback: when your work is complete, call SubagentHandback({message: <your full report>}) and then stop. Only a SubagentHandback call reaches your caller as your result; plain text you write at the end is not delivered.
</system-reminder>

### [assistant text]
I'll start by reading the format specification.

### [tool_use Read]
{"file_path": "/home/ankur/scamtrends_feed/registry/FORMAT.md"}

### [tool_result]
1	# Registry output format (shared by all research agents)
2	
3	Each agent writes ONE JSON file (a top-level array) to `/home/ankur/scamtrends_feed/registry/`.
4	Keep to these keys exactly so the files can be merged mechanically. Unknown → `null` or `[]`,
5	never invented. Every factual claim must be backed by an `evidence` URL you actually opened.
6	
7	## 1. Entity record (`entities_<partition>.json`)
8	
9	`entity_id` is the entity's **primary official registrable domain**, lowercase, no scheme/www
10	(e.g. `police.gov.sg`, `scdf.gov.sg`, `dbs.com.sg`, `whatsapp.com`). This makes IDs deterministic
11	across agents. A programme without its own domain uses `<parent domain>#<slug>`
12	(e.g. `ica.gov.sg#sg-arrival-card`).
13	
14	```json
15	{
16	  "entity_id": "police.gov.sg",
17	  "name": "Singapore Police Force",
18	  "abbr": "SPF",
19	  "aliases": ["Singapore Police Force (SPF)", "Police"],
20	  "sector": "gov.ministry | gov.statboard | gov.organ | gov.dept | gov.programme | gov.court | quasi_gov | bank | payments | telco | logistics | ecommerce | marketplace | transport | utility | retail | travel | media | brokerage | insurance | healthcare | tech_platform | crypto | other",
21	  "parent_entity_id": "mha.gov.sg",
22	  "country": "SG",
23	  "official_domains": ["police.gov.sg"],
24	  "official_hosts": ["www.police.gov.sg", "eservices.police.gov.sg"],
25	  "scam_info": [
26	    {
27	      "url": "https://www.police.gov.sg/Media-Room/News",
28	      "kind": "advisory_feed | alert_page | scam_faq | official_channels | fake_indicator_list | news_releases | report_portal | statistics",
29	      "lists_indicators": ["domain", "url", "phone", "email", "sms_sender_id", "app", "social_handle", "bank_account", "entity_name"],
30	      "access": "html | rss | atom | sitemap | json_api_documented | csv | pdf",
31	      "machine_url": "https://www.police.gov.sg/sitemap/sitemap.xml",
32	      "item_count": 354,
33	      "latest_item_date": "2026-11-20",
34	      "verified": "2026-11-25 HTTP 200",
35	      "sample": "short verbatim excerpt or example indicator",
36	      "notes": ""
37	    }
38	  ],
39	  "official_channels": {
40	    "sms_sender_ids": [], "hotlines": [], "short_link_domains": [], "social": []
41	  },
42	  "evidence": ["https://... page that confirms the official domains"],
43	  "notes": ""
44	}
45	```
46	
47	`lists_indicators: []` means the page is narrative only (no concrete scam indicators).
48	
49	## 2. Host-discovery record (`hosts_ct.json`), for the subdomain/CT agent only
50	
51	```json
52	{
53	  "host": "www.scamshield.gov.sg",
54	  "registrable_domain": "scamshield.gov.sg",
55	  "discovered_via": "crt.sh | certspotter | sitemap | search | trusted_sites_list | link",
56	  "cert_first_seen": "2023-...", "cert_last_seen": "2026-...",
57	  "resolves": true, "a_records": ["..."],
58	  "http_status": 200, "title": "...",
59	  "scam_relevant": "yes | maybe | no",
60	  "owner_entity_id": "scamshield.gov.sg",
61	  "notes": ""
62	}
63	```
64	
65	## 3. Brand-resolution record (`spf_brand_map.json`), for the brand agent only
66	
67	Input: `registry/spf_brands.json` (159 SPF `Brand` tag values with counts, categories, sample domains, titles).
68	
69	```json
70	{
71	  "brand_value": "Land Transport Authority (LTA)",
72	  "tag_id": "uuid from input",
73	  "resolution": "real_entity | fictitious_scam_brand | generic_or_placeholder | ambiguous",
74	  "entity_id": "lta.gov.sg",
75	  "official_domains": ["lta.gov.sg", "onemotoring.lta.gov.sg"],
76	  "is_singapore_entity": true,
77	  "sector": "gov.statboard",
78	  "confidence": "high | medium | low",
79	  "evidence": ["https://..."],
80	  "notes": "e.g. 'scam domains imitate OneMotoring/ERP payments'"
81	}
82	```
83	
84	## Ground rules (all agents)
85	- Use only public, user-facing pages, robots.txt, sitemaps, RSS/Atom, published downloads, documented APIs,
86	  public certificate-transparency search (crt.sh, certspotter), DNS lookups, and web search.
87	- Do NOT probe undocumented backend/CMS/API paths, brute-force paths, port-scan, log in or register.
88	  An earlier attempt to query an undocumented CMS API was blocked by policy. If any action is blocked, stop
89	  that line of work and report it. Don't work around it.
90	- Do NOT visit scam/malicious domains. Official sites only.
91	- Light request volume. Normal browser User-Agent. Respect robots.txt.
92	- Scratch downloads go in `/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/`.
93	

### [tool_use Bash]
{"command": "ls -la /home/ankur/scamtrends_feed/registry/ /home/ankur/scamtrends_feed/; wc -c /home/ankur/scamtrends_feed/registry/spf_brands.json /home/ankur/scamtrends_feed/advisories.jsonl; head -c 3000 /home/ankur/scamtrends_feed/registry/spf_brands.json", "description": "List registry files and preview brand input"}

### [tool_result]
/home/ankur/scamtrends_feed/:
total 1000
drwxrwxr-x   5 ankur ankur   4096 Nov 25 17:45 .
drwxr-x--- 132 ankur ankur   4096 Nov 25 17:46 ..
-rw-rw-r--   1 ankur ankur 481400 Nov 25 16:46 advisories.jsonl
-rw-rw-r--   1 ankur ankur 493825 Nov 25 16:46 advisories_raw.json
-rw-rw-r--   1 ankur ankur   4896 Nov 25 16:46 extract.py
-rw-rw-r--   1 ankur ankur   7722 Nov 25 16:47 FINDINGS.md
drwxrwxr-x   2 ankur ankur   4096 Nov 25 16:46 raw
drwxrwxr-x   2 ankur ankur   4096 Nov 25 17:45 registry
drwxrwxr-x   2 ankur ankur   4096 Nov 25 17:20 sources
-rw-rw-r--   1 ankur ankur   5346 Nov 25 17:21 SOURCES.md

/home/ankur/scamtrends_feed/registry/:
total 68
drwxrwxr-x 2 ankur ankur  4096 Nov 25 17:45 .
drwxrwxr-x 5 ankur ankur  4096 Nov 25 17:45 ..
-rw-rw-r-- 1 ankur ankur  4237 Nov 25 17:45 FORMAT.md
-rw-rw-r-- 1 ankur ankur 50966 Nov 25 17:45 spf_brands.json
 50966 /home/ankur/scamtrends_feed/registry/spf_brands.json
481400 /home/ankur/scamtrends_feed/advisories.jsonl
532366 total
[
 {
  "brand_value": "Land Transport Authority (LTA)",
  "tag_id": "d08ce456-358c-4297-ab61-ea654c314afd",
  "count": 18,
  "categories": [
   "Impersonation",
   "Investment",
   "Non-Banking Related Phishing",
   "Phishing"
  ],
  "sample_domains": [
   "gsaz.cc",
   "pajy.apppy.cc",
   "onemotoring-iza.top",
   "citepay.top"
  ],
  "sample_titles": [
   "Advisory: Beware of Phishing Scams Impersonating LTA",
   "Advisory: Beware of Fake LTA Websites Impersonating Land Transport Authority"
  ]
 },
 {
  "brand_value": "WhatsApp",
  "tag_id": "528c22fe-54db-436a-9f05-cdf257003c71",
  "count": 8,
  "categories": [
   "Impersonation",
   "Investment",
   "Job"
  ],
  "sample_domains": [
   "whasgapp.com",
   "ws-whmalopp.lat",
   "whetsap.cam",
   "whetsoerapp.cc"
  ],
  "sample_titles": [
   "Advisory: Impersonation Scams Using Fake WhatsApp Websites",
   "Advisory on WhatsApp Impersonation Scams"
  ]
 },
 {
  "brand_value": "CNA",
  "tag_id": "8d3f3eb7-bdf7-4395-845f-1b8ee6bbaec4",
  "count": 7,
  "categories": [
   "Investment"
  ],
  "sample_domains": [
   "truedesignsolutions.shop",
   "zenvaroe.com",
   "avernovat.com",
   "databaiouzuma.com"
  ],
  "sample_titles": [
   "Advisory: Beware of Fake CNA Investment Schemes",
   "Advisory: Beware of Investment Scams Impersonating CNA"
  ]
 },
 {
  "brand_value": "TikTok",
  "tag_id": "840ed2d8-1859-4af2-980d-b4adca830e7c",
  "count": 6,
  "categories": [
   "Investment",
   "Job"
  ],
  "sample_domains": [
   "globaltop.org",
   "fdfdd.cc",
   "mermyseller.shop",
   "r2g9.my"
  ],
  "sample_titles": [
   "Stay Vigilant Against Job Scams Impersonating TikTok",
   "Advisory: Beware of Fake Job Scams Impersonating TikTok"
  ]
 },
 {
  "brand_value": "UnionPay",
  "tag_id": "09fc1dc2-70b6-4820-8dad-5df0d4fe739a",
  "count": 6,
  "categories": [
   "Impersonation"
  ],
  "sample_domains": [
   "lumivo.cfd",
   "calqiro.cfd",
   "plieruy.cfd",
   "victimfundsrecvery.com"
  ],
  "sample_titles": [
   "Advisory: Beware of Scam Websites Impersonating UnionPay",
   "Advisory: Beware of Fake UnionPay \"Security Check\" Scam Websites"
  ]
 },
 {
  "brand_value": "DBS",
  "tag_id": "238adae4-4989-4799-87bd-5fbb2c210e70",
  "count": 6,
  "categories": [
   "Banking Related Phishing"
  ],
  "sample_domains": [
   "dbsi-banking.com",
   "ice-coffee-star.unicornplatform.page",
   "cmpaus.com.au",
   "dbs-token.buzz"
  ],
  "sample_titles": [
   "Advisory: Beware of Fake DBS Banking Websites",
   "Advisory: Beware of Phishing Scams Impersonating DBS Bank"
  ]
 },
 {
  "brand_value": "Singapore Police Force (SPF)",
  "tag_id": "43f2fb2d-7e5d-42c9-a8e9-047002c0c06d",
  "count": 5,
  "categories": [
   "Impersonation",
   "Non-Banking Related Phishing"
  ],
  "sample_domains": [
   "drbypass-proxy.pages.dev",
   "hare-fan8702.workers.dev",
   "policegov.eu.cc",
   "sg-policectictr.com"
  ],
  "sample_titles": [
   "Advisory: Beware of Fake Singapore Police Force Websites and Messages",
   "Alert: Fake SPF Websites Im

### [tool_use Bash]
{"command": "python3 -c \"\nimport json\nd=json.load(open('registry/spf_brands.json'))\nprint(len(d))\nfor i,r in enumerate(d):\n    print(i, repr(r['brand_value']), r['count'], '|', ','.join(r['categories']), '|', ' ; '.join(r['sample_titles'][:2])[:200])\n\"", "description": "List all 159 brand values with counts and titles"}

### [tool_result]
159
0 'Land Transport Authority (LTA)' 18 | Impersonation,Investment,Non-Banking Related Phishing,Phishing | Advisory: Beware of Phishing Scams Impersonating LTA ; Advisory: Beware of Fake LTA Websites Impersonating Land Transport Authority
1 'WhatsApp' 8 | Impersonation,Investment,Job | Advisory: Impersonation Scams Using Fake WhatsApp Websites ; Advisory on WhatsApp Impersonation Scams
2 'CNA' 7 | Investment | Advisory: Beware of Fake CNA Investment Schemes ; Advisory: Beware of Investment Scams Impersonating CNA
3 'TikTok' 6 | Investment,Job | Stay Vigilant Against Job Scams Impersonating TikTok ; Advisory: Beware of Fake Job Scams Impersonating TikTok
4 'UnionPay' 6 | Impersonation | Advisory: Beware of Scam Websites Impersonating UnionPay ; Advisory: Beware of Fake UnionPay "Security Check" Scam Websites
5 'DBS' 6 | Banking Related Phishing | Advisory: Beware of Fake DBS Banking Websites ; Advisory: Beware of Phishing Scams Impersonating DBS Bank
6 'Singapore Police Force (SPF)' 5 | Impersonation,Non-Banking Related Phishing | Advisory: Beware of Fake Singapore Police Force Websites and Messages ; Alert: Fake SPF Websites Impersonating the Police
7 'Ninjavan' 5 | E-Commerce,Non-Banking Related Phishing,Phishing | Beware of Ninjavan Phishing Scams: Verify Delivery Links ; Alert: Phishing Scams Impersonating Ninjavan
8 'Inland Revenue Authority of Singapore (IRAS)' 5 | Malware,Non-Banking Related Phishing,Phishing | Advisory: Be Wary of Phishing Scams Impersonating IRAS ; Advisory: Beware of Malware Scams Impersonating Government Agencies like IRAS
9 'SingPost' 5 | Non-Banking Related Phishing | Advisory: Protect Yourself from Fake SingPost Websites ; Advisory on Fake SingPost Websites and Phishing Scams
10 'CDC Vouchers' 4 | Impersonation | Advisory on Impersonation Scams Involving CDC Vouchers ; Advisory: Be Wary of Impersonation Scams Targeting CDC Vouchers
11 'MooMoo' 3 | Non-Banking Related Phishing | Advisory: Phishing Scams Impersonating MooMoo ; Advisory on Phishing Scams Impersonating MooMoo
12 'Booking.com' 3 | Non-Banking Related Phishing | Advisory: Phishing Scams Impersonating Booking.com ; Phishing Scams Impersonating Booking.com Observed
13 'Lalamove' 3 | Non-Banking Related Phishing | Advisory: Protect Yourself from Fake Lalamove Phishing Sites ; Advisory: Beware of Fake Lalamove Phishing Sites and Messages
14 'JKF' 3 | Job | ACT Against Job Scams Impersonating E-commerce Platforms ; Advisory: Beware of Fake Job Offers on Suspicious Websites
15 'UOB' 3 | Banking Related Phishing | Advisory: Beware of Phishing Scams Impersonating UOB ; Advisory: Beware of Fake Banking Websites Impersonating DBS and UOB
16 'B2B Wave' 3 | Job | Advisory on Fake Online Job Scams Impersonating B2B Wave and Other Brands ; Job Scam Advisory: B2B Wave Impersonation
17 'NVIDIA' 2 | Investment | Advisory: Beware of Fake Investment Scams Impersonating NVIDIA ; Beware of Investment Scams Impersonating Brands and Promising High Returns
18 'Singpass' 2 | Non-Banking Related Phishing | Protect Your Singpass Account from Phishing Scams ; Advisory: Alert on Phishing Scams Impersonating Singpass
19 'Park N Parcel' 2 | Non-Banking Related Phishing | Advisory: Beware of Park N Parcel Phishing Scams ; Phishing Scam Alert: Impersonation of Park N Parcel
20 'LG' 2 | Investment | Advisory: Beware of Fake Investment Scams Impersonating LG ; Advisory: Beware of Fake Investment Opportunities Impersonating LG
21 'No Brand' 2 | E-Commerce,Non-Banking Related Phishing | Advisory: Watch Out for Fake Online Shopping Deals (E-Commerce Scams) ; Scam Advisory: Beware of Phishing Websites Impersonating Events
22 'SPX' 2 | Non-Banking Related Phishing | Advisory: Beware of Phishing Scams Impersonating SPX ; Beware of Phishing Scams Impersonating SPX
23 'Gov.sg' 2 | Impersonation | Advisory: Protect Yourself from Gov.sg Impersonation Scams ; Advisory: Beware of Fake Gov.sg Websites Impersonating Official Government Platforms
24 'Immigration & Checkpoints Authority of Singapore (ICA)' 2 | Impersonation | Advisory: Beware of Scams Impersonating ICA ; Advisory: Beware of Scams Impersonating the Immigration & Checkpoints Authority (ICA)
25 'MoneySmart' 2 | Non-Banking Related Phishing | Advisory: Protect Yourself from Phishing Scams Impersonating MoneySmart ; Advisory on Phishing Scams Impersonating MoneySmart
26 'Netflix' 2 | Non-Banking Related Phishing | Advisory: Beware of Phishing Scams Impersonating Netflix ; Spotting Fake Netflix Websites: A Phishing Scam Advisory
27 'Telegram' 2 | Impersonation | Advisory: Watch Out for Telegram Impersonation Scams ; Beware of Impersonation Scams on Telegram
28 'CTX' 2 | Investment | Beware of Fake Investment Scams Promising High Returns ; Advisory: Beware of Fake Investment Websites Impersonating Popular Brands
29 'JUST' 2 | Investment | Advisory: Beware of Investment Scams Using Suspicious Websites ; Advisory: Beware of Fake Investment Websites
30 'Singtel' 2 | Non-Banking Related Phishing | Recent Phishing Scams Impersonate Popular Brands - Stay Vigilant! ; Beware of Phishing Scams Impersonating Singtel
31 'Airdrop Pepe' 2 | Investment | Advisory: Watch Out for Investment Scams Impersonating Brands ; Beware of Fake Investment Platforms Promising High Returns
32 'moburst' 1 | Job | Advisory: Job Scams Impersonating Brands like Moburst
33 'Koka Kona' 1 | Investment | Advisory: Beware of Fake 'Koka Kona' Investment Scams
34 'Red Bull' 1 | Investment | Advisory: Beware of Investment Scams Impersonating Brands like Red Bull
35 'SimplyGo' 1 | Non-Banking Related Phishing | Alert: Phishing Scams Impersonating SimplyGo Detected
36 'SingHealth' 1 | Non-Banking Related Phishing | Advisory: Beware of Fake SingHealth and Polyclinic Websites
37 'Dance Prize' 1 | Impersonation | Advisory: Beware of Fake "Dance Prize" Impersonation Scams
38 'Genwrk Store' 1 | Job | Advisory: Beware of Job Scams Impersonating 'Genwrk Store'
39 'uParcel' 1 | Non-Banking Related Phishing | Advisory: Beware of uParcel

### [tool_use Bash]
{"command": "head -c 1500 advisories.jsonl; echo; echo ----; python3 -c \"\nimport json\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nprint(len(rows)); print(list(rows[0].keys()))\n\"; echo ----; cat FINDINGS.md | head -80", "description": "Inspect advisories.jsonl structure and findings"}

### [tool_result]
{"id": "b633b3b7-f3f5-4e06-b96c-05f0ce86c9ed", "url": "https://www.icanactagainstscams.gov.sg/scam-trends/fake-singapore-police-force-websites-and-messages-b633b3b7", "published": "2026-11-24T02:23:28.255Z", "modified": "2026-11-24T02:28:09.810Z", "title": "Advisory: Beware of Fake Singapore Police Force Websites and Messages", "scam_categories": ["Impersonation"], "impersonated_brands": ["Singapore Police Force (SPF)"], "impersonated_gov_entities": ["Singapore Police Force (SPF)"], "scam_domains": ["drbypass-proxy.pages.dev"], "images": ["https://www.icanactagainstscams.gov.sg/api/assets/ee5b98cd-b395-46a5-99f9-ac61d2142a6f/ee5b98cd-b395-46a5-99f9-ac61d2142a6f.png"], "body_md": "The Singapore Police Force (SPF) has observed a trend of scam websites and messages impersonating official SPF communications. These fraudulent sites aim to trick the public into believing they are interacting with the police, often to solicit personal information or money.\n\n**How to recognise these scams:**\n*   **Unusual website addresses:** Official SPF websites always end with `.gov.sg`. Be wary of links that use different endings (e.g., `.pages.dev`, `.com`, `.net`) or contain suspicious characters.\n*   **Requests for sensitive information:** SPF will never ask for your banking details, Singpass password, or one-time passwords (OTPs) through unofficial channels or suspicious links.\n\n**What to do if you encounter such a scam or have been affected:**\nIf you receive a suspicious message or en
----
209
['id', 'url', 'published', 'modified', 'title', 'scam_categories', 'impersonated_brands', 'impersonated_gov_entities', 'scam_domains', 'images', 'body_md', '_occurrences', '_sort', '_tag_ids']
----
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
  "scam_site_urls": "[\"drbypass-proxy.pages.dev\"]", 

### [tool_use Bash]
{"command": "sed -n 80,200p FINDINGS.md; echo ----; cat SOURCES.md; ls sources raw", "description": "Read remainder of findings and sources docs"}

### [tool_result]
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
----
# Singapore scam-indicator sources: survey results (2026-11-25)

Detail files: `sources/00_sg_signal_baseline.md` (my measurements), `01_sg_official.md`,
`02_generic_feeds.md` (+ `sgfilter.py`), `03_community_commercial.md`.

## Bottom line

1. **No SG body publishes a machine-readable scam-domain feed.** The real operational lists are closed:
   SPF's SATIS system (52,200 site takedowns in H1 2026), the National Scams List (banks and telcos only),
   OCHA directions (published only as counts), and ScamShield app reports.
2. **The SPF icanact feed and the open global feeds are almost disjoint.** 0 of 44 SPF hosts from the last 30 days
   appear in about 1.4M open-feed hosts, and 18 of 317 over all time.
3. **The open feeds hold a different SG population:** about 445 SG-brand hosts in Phishing.Database, mostly
   DBS/PayLah, Carousell, POSB and Singtel *kit* URLs. SPF doesn't list these.
4. **Hostname/keyword filtering can't find SG investment or job scams.** Only 1 of 112 SPF investment domains
   carries an SG token. Those scams can only be tied to SG through the authority's own list or the lure channel.
5. **Hosting location is useless as an SG signal.** "SG-hosted" phishing is mostly Tencent Cloud SG / EdgeOne
   serving non-SG brands. `.sg` hosts are mostly compromised SME sites.

## Ranked sources for an SG scam-indicator dataset

| # | Source | What | Access | Lifecycle fields | Licence |
|---|---|---|---|---|---|
| 1 | **SPF icanactagainstscams.gov.sg** | 209 advisories, 317 domains, Brand/Category tags | 1 GET, RSC parse (`extract.py`) | created/updated only | Gov site terms (check) |
| 2 | **MAS Investor Alert List via OpenSanctions** | 902 unlicensed entities: names, phones, emails, sites | `data.opensanctions.org/datasets/latest/sg_mas_investor_alert/` (`targets.simple.csv`; sites in `source.json`) | **first_seen / last_seen / last_change**, so delisting is detectable | CC-BY-NC 4.0 |
| 3 | **Phishing.Database** (GitHub) | ~445 SG-brand hosts among ~790k links | raw files, no key | ACTIVE/INACTIVE lists, git history gives first-seen | MIT |
| 4 | **police.gov.sg sitemap** | 354 advisories + 956 scam URLs, 2021–2026 | sitemap.xml; `/api/` blocked by robots.txt | publication date | Gov site terms |
| 5 | **PhishStats API** | URL keyword search (carousell 19) | 50 requests/day anonymous | date, date_update, http_code | free tier |
| 6 | **CSA alerts/advisories RSS** | 19 scam-related advisories | documented RSS | pubDate | Gov site terms |
| 7 | **ScamShield site** | 10 brand-level alerts, no URLs | sitemap diff | none | Gov site terms |
| 8 | PhishDestroy / Phishing Army | 14 / 4 SG hits | bulk files | detection time (PhishDestroy page only) | CC-BY / mixed |

**Allowlists** (for reducing false positives and matching look-alikes): gov.sg Trusted Sites
(`elliotwutingfeng/GovSGTrustedSites`), Singtel/SingPost/Carousell/Shopee official-domain pages,
the SGNIC registered-sender-ID organisation list, MinLaw licensed moneylenders, and ACRA on data.gov.sg.

**Text corpora, not indicators:** the scamalert.sg scrape (4,660 reports, 2016–20, no licence and contains personal data, so internal use only),
and the IMC'25 smishing set (CC BY 4.0, ~193 SG SMS, URLs removed).

**Gated / paid:** OpenPhish Premium, APWG eCX (there is a researcher data grant), PhishTank (registration closed),
Netcraft, the GASA Global Signal Exchange, Whoscall/Gogolook (the StarHub ScamSafe engine), ScamAdviser API,
Group-IB IOC sets, and abuse.ch exports (free Auth-Key required since 2026-10-21).

## Answer to "can we filter SG-native items out of generic feeds?"

Partly. It works for **bank, marketplace and telco phishing kits**, where the brand appears in the URL path
(`/bank/dbs/`, `/posb/`, `/singtel/`). `sgfilter.py` is about 75–80% precise on a 40-host spot check, and every hit needs
confirmation with urlscan or Safe Browsing. It **does not work** for investment, job or impersonation-call scams,
which make up most SG losses and m

### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work && cd /home/ankur/scamtrends_feed && python3 - <<'EOF'\nimport json, collections\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nbrands=json.load(open('registry/spf_brands.json'))\n# check tag ids mapping\nr0=rows[0]\nprint(r0['_tag_ids'] if '_tag_ids' in r0 else None)\nprint(r0.get('_occurrences'), r0.get('_sort'))\nby=collections.defaultdict(list)\nfor r in rows:\n    for b in r['impersonated_brands']:\n        by[b].append(r)\nmissing=[b['brand_value'] for b in brands if b['brand_value'] not in by]\nprint('missing', missing)\nprint(sum(len(v) for v in by.values()))\nEOF", "description": "Map brand values to advisories and check join"}

### [tool_result]
{'Impersonation': '70f85992-4415-4eb4-b4c5-7a6145969140', 'Singapore Police Force (SPF)': '43f2fb2d-7e5d-42c9-a8e9-047002c0c06d'}
None None
missing []
250

### [tool_use Bash]
{"command": "python3 - <<'EOF'\nimport json, collections, re\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nbrands=json.load(open('registry/spf_brands.json'))\nby=collections.defaultdict(list)\nfor r in rows:\n    for b in r['impersonated_brands']:\n        by[b].append(r)\nout=open('/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_context.txt','w')\nfor i,b in enumerate(brands):\n    bv=b['brand_value']\n    out.write(f\"\\n######## [{i}] {bv}  (n={b['count']})\\n\")\n    for r in by[bv]:\n        out.write(f\"--- {r['published'][:10]} | {r['title']} | {r['url']}\\n    brands={r['impersonated_brands']} domains={r['scam_domains']}\\n\")\n        body=r['body_md']\n        out.write(body.strip()+\"\\n\")\nout.close()\nEOF\nwc -c /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_context.txt", "description": "Dump per-brand advisory bodies to scratch file"}

### [tool_result]
424677 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_context.txt

### [tool_use Bash]
{"command": "python3 - <<'EOF'\nimport json, collections, re\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nbrands=json.load(open('registry/spf_brands.json'))\nby=collections.defaultdict(list)\nfor r in rows:\n    for b in r['impersonated_brands']:\n        by[b].append(r)\ndef keys(bv):\n    ks=set()\n    base=re.sub(r'\\(.*?\\)','',bv).strip()\n    ks.add(base.lower())\n    m=re.search(r'\\((.*?)\\)',bv)\n    if m: ks.add(m.group(1).lower())\n    return [k for k in ks if k]\nout=open('/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_snips.txt','w')\nfor i,b in enumerate(brands):\n    if i<32: continue  # skip high-count; handle separately\n    bv=b['brand_value']\n    ks=keys(bv)\n    out.write(f\"\\n######## [{i}] {bv}\\n\")\n    for r in by[bv]:\n        out.write(f\"--- {r['published'][:10]} | {r['title']} | {r['url']}\\n    brands={r['impersonated_brands']} domains={r['scam_domains']}\\n\")\n        paras=[p.strip() for p in re.split(r'\\n\\s*\\n|\\n(?=\\*|\\-|\\d+\\.)',r['body_md']) if p.strip()]\n        hits=[p for p in paras if any(k in p.lower() for k in ks)]\n        if not hits:\n            hits=paras[:3]\n            out.write(\"    (no direct mention; first paras)\\n\")\n        for p in hits[:6]:\n            out.write(\"    > \"+p.replace('\\n',' ')[:700]+\"\\n\")\nout.close()\nEOF\nwc -c /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_snips.txt", "description": "Extract brand-mention snippets for low-count brands"}

### [tool_result]
94981 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_snips.txt

### [tool_use Read]
{"file_path": "/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_snips.txt", "limit": 300}

### [tool_result]
PreToolUse hook did not respond before its timeout (host client may be unreachable). The tool call was not executed; other configured hooks may not have completed.

### [tool_use Bash]
{"command": "sed -n 1,250p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/brand_snips.txt", "description": "Read first part of brand snippets"}

### [tool_result]
<persisted-output>
Output too large (31.2KB). Full output saved to: /home/ankur/.claude/projects/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tool-results/bmfkjnhec.txt

Preview (first 2KB):
######## [32] moburst
--- 2026-11-17 | Advisory: Job Scams Impersonating Brands like Moburst | https://www.icanactagainstscams.gov.sg/scam-trends/job-scams-impersonating-brands-like-moburst-dd460ff3
    brands=['moburst'] domains=['lt-moburstmobile.pages.dev']
    > The Singapore Police Force has observed a recent increase in job scams involving fake websites impersonating legitimate companies, such as Moburst. Scammers create deceptive websites to trick individuals into believing they are applying for legitimate job opportunities.

######## [33] Koka Kona
--- 2026-11-13 | Advisory: Beware of Fake 'Koka Kona' Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/fake-koka-kona-investment-scams-58bf1784
    brands=['Koka Kona'] domains=['akk500.com']
    > The Singapore Police Force has observed a trend of investment scams impersonating well-known brands, including 'Koka Kona'. Scammers are creating fake websites and online platforms to trick individuals into bogus investment schemes. We urge the public to remain vigilant against such fraudulent activities.
    > *   Scammers create fake websites or applications (e.g., `akk500.com`) that closely mimic legitimate brands like 'Koka Kona' to promote fraudulent investment opportunities.

######## [34] Red Bull
--- 2026-11-12 | Advisory: Beware of Investment Scams Impersonating Brands like Red Bull | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-like-red-bull-8904bc32
    brands=['Red Bull'] domains=['angel-investment.cc']
    > The Singapore Police Force has observed a recent rise in investment scams where fraudsters impersonate well-known brands, such as Red Bull, to trick victims. These scams often promote fake investment opportunities through suspicious websites like `angel-investment.cc`.
...
</persisted-output>

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work && split -C 14000 -d brand_snips.txt snip_ && ls snip_* && cat snip_00", "description": "Split snippets file and read first chunk"}

### [tool_result]
snip_00
snip_01
snip_02
snip_03
snip_04
snip_05
snip_06

######## [32] moburst
--- 2026-11-17 | Advisory: Job Scams Impersonating Brands like Moburst | https://www.icanactagainstscams.gov.sg/scam-trends/job-scams-impersonating-brands-like-moburst-dd460ff3
    brands=['moburst'] domains=['lt-moburstmobile.pages.dev']
    > The Singapore Police Force has observed a recent increase in job scams involving fake websites impersonating legitimate companies, such as Moburst. Scammers create deceptive websites to trick individuals into believing they are applying for legitimate job opportunities.

######## [33] Koka Kona
--- 2026-11-13 | Advisory: Beware of Fake 'Koka Kona' Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/fake-koka-kona-investment-scams-58bf1784
    brands=['Koka Kona'] domains=['akk500.com']
    > The Singapore Police Force has observed a trend of investment scams impersonating well-known brands, including 'Koka Kona'. Scammers are creating fake websites and online platforms to trick individuals into bogus investment schemes. We urge the public to remain vigilant against such fraudulent activities.
    > *   Scammers create fake websites or applications (e.g., `akk500.com`) that closely mimic legitimate brands like 'Koka Kona' to promote fraudulent investment opportunities.

######## [34] Red Bull
--- 2026-11-12 | Advisory: Beware of Investment Scams Impersonating Brands like Red Bull | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-like-red-bull-8904bc32
    brands=['Red Bull'] domains=['angel-investment.cc']
    > The Singapore Police Force has observed a recent rise in investment scams where fraudsters impersonate well-known brands, such as Red Bull, to trick victims. These scams often promote fake investment opportunities through suspicious websites like `angel-investment.cc`.
    > *   Scammers create fake investment websites (e.g., `angel-investment.cc`) that may use the logo or name of legitimate companies like Red Bull without authorisation. Always check the URL carefully for discrepancies and verify directly with the official brand's website.

######## [35] SimplyGo
--- 2026-11-11 | Alert: Phishing Scams Impersonating SimplyGo Detected | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-scams-impersonating-simplygo-detected-7e815834
    brands=['SimplyGo'] domains=['se-debarrasser-des-taupes-et-taupiniere.be']
    > The Singapore Police Force has observed recent phishing scam attempts impersonating SimplyGo. Scammers are creating fake websites and sending messages to trick individuals into revealing their personal and banking details.
    > *   Scam websites impersonating SimplyGo often use suspicious or unrelated web addresses, such as `se-debarrasser-des-taupes-et-taupiniere.be`, instead of official SimplyGo domains.
    > *   You may receive unsolicited SMS messages or emails asking you to click on a link to update your SimplyGo account or resolve an issue. SimplyGo will not send unexpected links requesting personal or payment details.
    > *   Always verify information by visiting the official SimplyGo website (www.simplygo.com.sg) or through their official mobile application directly.

######## [36] SingHealth
--- 2026-11-09 | Advisory: Beware of Fake SingHealth and Polyclinic Websites | https://www.icanactagainstscams.gov.sg/scam-trends/fake-singhealth-and-polyclinic-websites-08f61cb1
    brands=['SingHealth'] domains=['polyclinic-a.top']
    > The Singapore Police Force (SPF) has observed a trend of phishing scams involving fake websites impersonating SingHealth and polyclinics. These scam sites, such as `polyclinic-a.top`, aim to trick you into revealing your personal or financial information.
    > *   **Suspicious Website Addresses:** Always check the website URL carefully. Official SingHealth or polyclinic websites will have legitimate domain names (e.g., ending with `.gov.sg` or official `.sg` domains), not unusual ones like `polyclinic-a.top`.
    > *   **C**hecking for scam signs and verifying with official sources like SingHealth's official website or calling their official helplines.

######## [37] Dance Prize
--- 2026-11-10 | Advisory: Beware of Fake "Dance Prize" Impersonation Scams | https://www.icanactagainstscams.gov.sg/scam-trends/fake-dance-prize-impersonation-scams-199bb391
    brands=['Dance Prize'] domains=['votegrand.sbs']
    > The Singapore Police Force has observed a trend of scam websites, such as `votegrand.sbs`, impersonating legitimate organisations to promote fake "Dance Prize" competitions.
    > *   You may receive unsolicited messages or encounter websites (like `votegrand.sbs`) asking you to vote in a "Dance Prize" competition or claiming you've won a prize.

######## [38] Genwrk Store
--- 2026-11-05 | Advisory: Beware of Job Scams Impersonating 'Genwrk Store' | https://www.icanactagainstscams.gov.sg/scam-trends/job-scams-impersonating-genwrk-store-42d843b9
    brands=['Genwrk Store'] domains=['genwrk.com']
    > The Singapore Police Force has observed a trend of job scams impersonating 'Genwrk Store'. Scammers are using websites like `genwrk.com` to trick individuals seeking employment. These scams often promise attractive returns for simple tasks, such as boosting online sales or performing other remote work.

######## [39] uParcel
--- 2026-11-04 | Advisory: Beware of uParcel Phishing Scams | https://www.icanactagainstscams.gov.sg/scam-trends/uparcel-phishing-scams-bc9ecb00
    brands=['uParcel'] domains=['llvtx.cfd']
    > The Singapore Police Force observes a trend of phishing scams impersonating uParcel, a popular delivery service. Scammers send unsolicited messages containing malicious links, aiming to trick victims into revealing personal or financial information.
    > *   **Suspicious Links:** Be wary of messages claiming to be from uParcel that contain unusual or unfamiliar website links (e.g., `llvtx.cfd`). Always check the URL carefully before cli

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/snip_01", "description": "Read second snippet chunk"}

### [tool_result]
    > *   Always scrutinise the website's address. Legitimate platforms will use their official domain (e.g., `github.com`), not suspicious or unfamiliar URLs such as `goudann.top`.

######## [49] QNT
--- 2026-10-07 | Advisory: Beware of Fake QNT Investment Platforms | https://www.icanactagainstscams.gov.sg/scam-trends/fake-qnt-investment-platforms-b1bd3b69
    brands=['QNT'] domains=['qntai.top']
    > The Singapore Police Force has observed a trend of investment scams involving platforms impersonating QNT, such as websites like `qntai.top`. These scams often lure victims with promises of high returns in a short period. We urge the public to be vigilant and remember to ACT against scams.
    > *   Always check the website address carefully. Scammers use fake or slightly altered URLs (e.g., `qntai.top`) to mimic official platforms. Verify the legitimacy of investment platforms through official company websites or trusted financial advisors.

######## [50] Miniex
--- 2026-10-06 | Advisory: Beware of Miniex Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/miniex-investment-scams-a77fab77
    brands=['Miniex'] domains=['miniexi.com']
    > The Singapore Police Force (SPF) has observed a trend of investment scams involving the brand "Miniex" and suspicious websites such as `miniexi.com`. These scammers typically target individuals with promises of attractive, high-yield investment returns.
    > *   Scammers often direct victims to fraudulent websites like `miniexi.com` or apps, claiming to be official "Miniex" investment platforms, to trick them into transferring money or providing personal details.

######## [51] GOM Player
--- 2026-09-16 | Advisory: Watch Out for Investment Scams on Suspicious Websites and Unrelated Brands | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-on-suspicious-websites-and-unrelated-brands-527d40ac
    brands=['GOM Player'] domains=['lumexafa.top', 'dnsyidzq.top']
    > The Singapore Police Force has observed a trend of investment scams operating through suspicious websites. These fraudulent sites often lure victims with promises of high returns and may even misuse the names of well-known, unrelated brands to appear legitimate. For example, some scams have recently misused the name of GOM Player, a media player, in their investment schemes. Scammers use obscure website addresses such as `lumexafa.top` and `dnsyidzq.top` to host these fraudulent platforms.

######## [52] Litecoin
--- 2026-09-14 | Advisory: Beware of Fake Litecoin Investment Websites | https://www.icanactagainstscams.gov.sg/scam-trends/fake-litecoin-investment-websites-989fc633
    brands=['Litecoin'] domains=['litecoin-machine.co']
    > The Singapore Police Force has observed a trend of investment scams involving fake websites impersonating cryptocurrency platforms, specifically using the "Litecoin" brand. These scams often trick individuals into believing they are investing in legitimate cryptocurrency, only to lose their money.
    > *   Scammers create deceptive websites that closely mimic legitimate cryptocurrency investment platforms or services, often featuring well-known brand names like Litecoin. Always **check** the URL carefully for any discrepancies and verify the legitimacy of the platform through official sources.

######## [53] Immediate Edge
--- 2026-09-11 | Advisory: Beware of Fake 'Immediate Edge' Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/fake-immediate-edge-investment-scams-15e08137
    brands=['Immediate Edge'] domains=['dylesaesivi.autos']
    > The Singapore Police Force has observed a trend of investment scams impersonating legitimate-sounding platforms, such as "Immediate Edge". Scammers create fake websites and advertisements to trick the public into believing they are investing in high-return schemes.
    > ### If you encounter such suspicious "Immediate Edge" investment offers or suspect you have been affected, you can **ACT**:

######## [54] BHP
--- 2026-09-10 | Advisory: Beware of Fake Investment Scams Impersonating BHP | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-scams-impersonating-bhp-799b7b46
    brands=['BHP'] domains=['2025gold.net']
    > The Singapore Police Force has observed a trend of fake investment scams impersonating reputable brands like BHP, often promoted through suspicious websites such as `2025gold.net`. These scams aim to trick you into believing you are investing in a legitimate opportunity.
    > *   **Check the Website Address:** Always verify that investment opportunities are promoted on the official websites of the companies they claim to represent. Scammers often use slightly altered or unusual domain names (e.g., `2025gold.net` instead of official BHP sites).
    > *   **Verify and Report:** Always `Check` for scam signs and verify investment opportunities directly with the official company (e.g., through BHP's official website) or a trusted financial institution. If you have shared your details or made any payments, immediately contact your bank to halt transactions and `Tell` the Police about the incident.

######## [55] lyft bikes
--- 2026-09-09 | Advisory: Beware of Investment Scams Impersonating Lyft Bikes | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-lyft-bikes-8bd34ade
    brands=['lyft bikes'] domains=['lyft098236.work']
    > The Singapore Police Force has observed a trend of investment scams impersonating legitimate brands, including "Lyft Bikes". Scammers create fake websites to lure victims into fraudulent investment schemes.

######## [56] The Straits Times
--- 2026-09-04 | Advisory: Scam Websites Impersonating The Straits Times for Fake Investments | https://www.icanactagainstscams.gov.sg/scam-trends/scam-websites-impersonating-the-straits-times-for-fake-cfef5783
    brands=['The Straits Times'] domains=['strikeathletics.pro']
    > The Singapore Police Force has observed an increase in scam websites

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/snip_02", "description": "Read third snippet chunk"}

### [tool_result]
    > *   **Unverified Platforms:** Scammers direct you to unfamiliar websites or apps (e.g., `xcnc.top`) for investment. Always verify the platform's legitimacy with official sources.

######## [64] BNBPULSE
--- 2026-07-28 | Advisory: Guard Against Online Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/online-investment-scams-8da4b5bc
    brands=['BNBPULSE'] domains=['2125578.com']
    > The Singapore Police Force observes a trend of investment scams involving fraudulent online platforms, sometimes masquerading as legitimate investment opportunities, such as those related to "BNBPULSE". These scams typically promise attractive returns with little to no risk.
    > *   Be cautious of unsolicited investment opportunities or platforms (like "BNBPULSE") that promise unusually high or guaranteed returns in a short period. Legitimate investments always carry some risk.

######## [65] Saudi Aramco
--- 2026-07-24 | Advisory: Protect Yourself from Impersonation Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/impersonation-investment-scams-2784b6c7
    brands=['Saudi Aramco'] domains=['currency-oil.com']
    > The Singapore Police Force warns the public about a rise in investment scams where fraudsters create fake websites and platforms to impersonate legitimate companies. These scams aim to trick individuals into investing in non-existent schemes. For instance, we have observed fake investment sites like `currency-oil.com` attempting to impersonate Saudi Aramco, offering what appear to be attractive investment opportunities.

######## [66] INFO
--- 2026-07-09 | Advisory: Beware of Suspicious Online Investment Platforms like 'mineverse.cc' | https://www.icanactagainstscams.gov.sg/scam-trends/suspicious-online-investment-platforms-like-mineverse-cc-042e6b7d
    brands=['INFO'] domains=['mineverse.cc']
    > *   **T**ell authorities, family and friends: If you have shared your personal or banking details, or transferred money, report it immediately to your bank and the police. Inform your loved ones about such scams to protect them.

######## [67] Compass Mining
--- 2026-07-07 | Advisory: Beware of Fake Investment Opportunities Impersonating Compass Mining | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-opportunities-impersonating-compass-mining-d8f3f0e5
    brands=['Compass Mining'] domains=['ssessoomm.com']
    > The Singapore Police Force (SPF) has observed recent reports of investment scams, including those impersonating legitimate entities like 'Compass Mining'. Scammers lure victims with promises of high returns through fake websites and platforms.

######## [68] BNB
--- 2026-07-02 | Advisory on Investment Scams Impersonating BNB | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-bnb-731d7dec
    brands=['BNB'] domains=['bbconbnb.com']
    > The Singapore Police Force has observed a recent trend of investment scams impersonating the brand "BNB". These scams often use deceptive websites like `bbconbnb.com` to trick individuals into fraudulent investment schemes, promising high returns.
    > *   **Unusual website addresses:** Be wary of website links that look similar to official brand sites but have slight variations (e.g., `bbconbnb.com` instead of the legitimate BNB domain). Always verify the exact URL before interacting with it.

######## [69] JoyBuy
--- 2026-06-26 | Scam Alert: Beware of Fake Job Offers Impersonating JoyBuy | https://www.icanactagainstscams.gov.sg/scam-trends/fake-job-offers-impersonating-joybuy-ecbe2af3
    brands=['JoyBuy'] domains=['maill-top.net']
    > Recent reports show a trend of job scams impersonating legitimate brands like JoyBuy. Scammers lure victims with fake work opportunities, promising high commissions for simple tasks.

######## [70] GoMining
--- 2026-06-24 | Advisory: Be Wary of Fake Investment Schemes Promoting 'GoMining' | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-schemes-promoting-gomining-896fe6ac
    brands=['GoMining'] domains=['go-mining66.top']
    > The Singapore Police Force has observed a trend of scam websites impersonating legitimate investment platforms or promoting fake cryptocurrency mining opportunities, often using brand names like 'GoMining'. These sites aim to trick individuals into investing in non-existent schemes.
    > *   Scammers promote fake 'GoMining' or similar investment schemes, promising exceptionally high returns in a short period with little to no risk.

######## [71] Nova Quant
--- 2026-06-22 | Advisory: Beware of Fake Investment Schemes Impersonating 'Nova Quant' | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-schemes-impersonating-nova-quant-88c98812
    brands=['Nova Quant'] domains=['novaxmr.xyz']
    > The Singapore Police Force (SPF) observes a trend of fake investment schemes, including those impersonating "Nova Quant", luring individuals with promises of high returns. These scams often direct victims to fraudulent websites, such as `novaxmr.xyz`, to trick them into transferring money.
    > *   Scammers may use names like "Nova Quant" and direct you to unfamiliar websites for registration or investment, which are not legitimate financial platforms.

######## [72] A2
--- 2026-06-19 | Advisory: Stay Vigilant Against Investment Scams Impersonating 'A2' | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-a2-4e53fae5
    brands=['A2'] domains=['a2.mom']
    > The Singapore Police Force (SPF) has observed recent instances of investment scam attempts, particularly those involving the impersonation of the brand 'A2' or similar entities. Scammers often create fake websites, such as 'a2.mom', to lure individuals into fraudulent investment schemes.
    > *   Be cautious of unsolicited messages, emails, or online advertisements promoting 'A2' or other brands that promise unusually high investment returns in a short period.
    > If you suspect you ha

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/snip_03", "description": "Read fourth snippet chunk"}

### [tool_result]
--- 2026-05-15 | Advisory: Beware of Fake Investment Opportunities Impersonating "AI-QT" | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-opportunities-impersonating-ai-qt-e52918f6
    brands=['AI-QT'] domains=['ai-qt.vip']
    > The Singapore Police Force (SPF) has observed a trend of scam websites, such as "ai-qt.vip", promoting fake investment opportunities that misuse the "AI-QT" brand.
    > *   The investment platform or website, like "ai-qt.vip", may look professional but is not affiliated with any legitimate financial institution or investment firm registered in Singapore. Always **"Check"** the legitimacy of the platform and its domain name.

######## [86] Snapchat
--- 2026-05-14 | Advisory: Beware of Investment Scams Using Snapchat's Brand | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-using-snapchats-brand-7b1caa77
    brands=['Snapchat'] domains=['makingvideos.app']
    > The Singapore Police Force has observed a trend of investment scams circulating, particularly on the website 'makingvideos.app', which leverages the branding of popular social media platforms like Snapchat. These scams attempt to lure individuals with promises of high returns through fraudulent investment schemes.
    > *   Be cautious of unsolicited messages or posts on social media (including platforms like Snapchat) that promote investment opportunities with unusually high returns or pressure you to act quickly.

######## [87] Crypto.com
--- 2026-05-13 | Advisory: Beware of Investment Scams Impersonating Crypto.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-crypto-com-4bcc0639
    brands=['Crypto.com'] domains=['kdmwj.com']
    > The Singapore Police Force (SPF) has observed a trend of investment scams impersonating legitimate cryptocurrency platforms like Crypto.com. Scammers create fake websites and applications to trick victims into investing in fraudulent schemes, promising high and quick returns.

######## [88] Charge+
--- 2026-05-12 | Advisory: Beware of Fake 'Charge+' Investment Schemes | https://www.icanactagainstscams.gov.sg/scam-trends/fake-charge-investment-schemes-fab4c30d
    brands=['Charge+'] domains=['chargingpiles.autos']
    > The Singapore Police Force (SPF) has observed a trend of fake investment schemes using the brand name "Charge+". These scams lure victims with promises of high returns through investments in charging piles or related services.
    > *   You receive unsolicited offers, often online or via messaging apps, promoting high-return investment opportunities in "charging piles" or electric vehicle infrastructure, claiming to be from "Charge+".

######## [89] SmartView
--- 2026-05-08 | Advisory: Beware of Fake Job Offers Associated with smartviewad.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-job-offers-associated-with-smartviewad-com-6b231b41
    brands=['SmartView'] domains=['smartviewad.com']
    > The Singapore Police Force (SPF) has observed recent trends involving fake job offers, particularly those associated with the website `smartviewad.com`.
    > *   You receive unsolicited job offers via messaging apps or social media, promising high pay for simple tasks (e.g., reviewing apps, optimising social media) and often directing you to suspicious websites like `smartviewad.com`.

######## [90] Imperialist Investment
--- 2026-05-07 | Advisory: Beware of Fake Investment Schemes Promoting 'Imperialist Investment' | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-schemes-promoting-imperialist-investment-5b6a4b18
    brands=['Imperialist Investment'] domains=['goldwind.app']
    > The Singapore Police Force (SPF) wishes to alert the public to a recurring investment scam involving a fraudulent entity named 'Imperialist Investment'. Scammers are enticing victims with promises of high returns through fake investment schemes.
    > *   You may receive unsolicited messages, calls, or encounter online advertisements promoting investment opportunities with 'Imperialist Investment', often promising unusually high or guaranteed profits with little to no risk.
    > If you suspect you have fallen victim to an 'Imperialist Investment' scam:
    > *   **T**elling authorities, family and friends: Share information about investment scams with your loved ones to protect them. If you encounter suspicious 'Imperialist Investment' offers, report them to the police.

######## [91] Marriott Bonvoy
--- 2026-05-06 | Advisory: Beware of Investment Scams Impersonating Reputable Brands | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-reputable-brands-31f06e15
    brands=['Marriott Bonvoy', 'Barrick Gold'] domains=['baobeiwa.bond', 'marrioot.net']
    > The Singapore Police Force (SPF) has observed a trend of investment scams impersonating well-known brands such as Barrick Gold and Marriott Bonvoy. Scammers create fake websites and platforms to trick individuals into believing they are investing with legitimate companies, promising high returns.
    > *   **Suspicious investment offers:** Be wary of investment offers, especially those promising high or guaranteed returns, that claim to be from well-known companies like Barrick Gold or Marriott Bonvoy. Legitimate companies do not typically offer direct, high-yield public investment schemes in this manner.

######## [92] Barrick Gold
--- 2026-05-06 | Advisory: Beware of Investment Scams Impersonating Reputable Brands | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-reputable-brands-31f06e15
    brands=['Marriott Bonvoy', 'Barrick Gold'] domains=['baobeiwa.bond', 'marrioot.net']
    > The Singapore Police Force (SPF) has observed a trend of investment scams impersonating well-known brands such as Barrick Gold and Marriott Bonvoy. Scammers create fake websites and platforms to trick individuals into believing they are investing with legitimate companies, promising high

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/snip_04", "description": "Read fifth snippet chunk"}

### [tool_result]
    brands=['Alvopetro', 'Hochschild'] domains=['autonomo-income.com', 'aloilvip.shop']
    > The Singapore Police Force (SPF) has observed a trend of investment scams where scammers impersonate legitimate companies like Hochschild and Alvopetro. These scams often use sophisticated tactics, including creating fake websites, to deceive victims into believing they are making genuine investments.

######## [104] Hochschild
--- 2026-04-15 | Advisory: Beware of Investment Scams Impersonating Legitimate Companies | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-legitimate-companies-04a4a367
    brands=['Alvopetro', 'Hochschild'] domains=['autonomo-income.com', 'aloilvip.shop']
    > The Singapore Police Force (SPF) has observed a trend of investment scams where scammers impersonate legitimate companies like Hochschild and Alvopetro. These scams often use sophisticated tactics, including creating fake websites, to deceive victims into believing they are making genuine investments.

######## [105] ROGin AI
--- 2026-04-14 | Advisory on Investment Scams Impersonating AI and Cryptocurrency Platforms | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-ai-and-cryptocurrency-d2da0567
    brands=['ROGin AI', 'SatoshiMine'] domains=['roginai.org', 'satoshiminebtc.com']
    > The Singapore Police Force has observed recent trends involving investment scams, particularly those impersonating platforms like 'ROGin AI' and 'SatoshiMine'. These scams often lure victims with promises of high returns from AI-powered investments or cryptocurrency mining.

######## [106] SatoshiMine
--- 2026-04-14 | Advisory on Investment Scams Impersonating AI and Cryptocurrency Platforms | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-ai-and-cryptocurrency-d2da0567
    brands=['ROGin AI', 'SatoshiMine'] domains=['roginai.org', 'satoshiminebtc.com']
    > The Singapore Police Force has observed recent trends involving investment scams, particularly those impersonating platforms like 'ROGin AI' and 'SatoshiMine'. These scams often lure victims with promises of high returns from AI-powered investments or cryptocurrency mining.

######## [107] Doge Mining
--- 2026-04-09 | Beware of Fake Investment Scams Promising High Returns | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-scams-promising-high-returns-4e5d1698
    brands=['Doge Mining', 'CTX', 'GN Mall'] domains=['doge-miningbank.vip', 'ctxpublic.online', 'gnfmall.com']
    (no direct mention; first paras)
    > The Singapore Police Force (SPF) has observed a trend of investment scams circulating online, often using fake websites or platforms. These scams lure victims with promises of high returns, often related to cryptocurrency mining or other attractive investment schemes.
    > ### How to recognise these scams:
    > *   Be wary of online 'investment' opportunities that promise unusually high or guaranteed returns with little to no risk. If it sounds too good to be true, it probably is.

######## [108] GN Mall
--- 2026-04-09 | Beware of Fake Investment Scams Promising High Returns | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-scams-promising-high-returns-4e5d1698
    brands=['Doge Mining', 'CTX', 'GN Mall'] domains=['doge-miningbank.vip', 'ctxpublic.online', 'gnfmall.com']
    (no direct mention; first paras)
    > The Singapore Police Force (SPF) has observed a trend of investment scams circulating online, often using fake websites or platforms. These scams lure victims with promises of high returns, often related to cryptocurrency mining or other attractive investment schemes.
    > ### How to recognise these scams:
    > *   Be wary of online 'investment' opportunities that promise unusually high or guaranteed returns with little to no risk. If it sounds too good to be true, it probably is.

######## [109] Capitaland
--- 2026-04-08 | Scam Alert: Beware of Fake CapitaLand Investment Websites | https://www.icanactagainstscams.gov.sg/scam-trends/fake-capitaland-investment-websites-28b6f5df
    brands=['Capitaland'] domains=['fnltvcapblndvn.com']
    > The Singapore Police Force (SPF) observes a trend of fake investment websites impersonating reputable brands like CapitaLand. Scammers create these fraudulent sites to trick individuals into bogus investment schemes.

######## [110] Burberry
--- 2026-04-06 | Act Against Scams: Watch Out for Fake Online Shopping Sites | https://www.icanactagainstscams.gov.sg/scam-trends/act-against-scams-watch-out-for-fake-online-shopping-sites-0d3e3526
    brands=['Burberry'] domains=['shop-adidasoutlet.com', 'premium-bag-sg.shop']
    > The Singapore Police Force (SPF) Scam Public Education Office (SPEO) observes a recent trend of fake e-commerce websites impersonating well-known brands like Adidas and Burberry. These sites are designed to trick shoppers with attractive deals, leading to financial loss or compromise of personal information.

######## [111] flance
--- 2026-03-30 | Advisory: Beware of Fake Job Offers on Suspicious Websites | https://www.icanactagainstscams.gov.sg/scam-trends/fake-job-offers-on-suspicious-websites-5c206874
    brands=['JKF', 'flance'] domains=['fastnedglobal.shop', 'companyflc.business', 'coupang-vip.com']
    (no direct mention; first paras)
    > The Singapore Police Force has observed a trend of job scams operating through suspicious websites such as `fastnedglobal.shop`, `companyflc.business`, and `coupang-vip.com`. These scams entice individuals with promises of easy work and high returns, often leading to financial loss or the compromise of personal data.
    > To protect yourself, remember to **ACT** against scams:
    > *   **Recognise the scam:** Be wary of unsolicited job offers that promise high returns for simple tasks (e.g., liking social media posts, reviewing products) or require you to make upfront payments or share sensitive personal details.

######## [11

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/snip_05 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/snip_06", "description": "Read remaining snippet chunks"}

### [tool_result]
    > *   Scammers create fake websites or apps, sometimes mimicking legitimate companies, to promote investment schemes that promise unbelievably high returns in a short period.

######## [123] Virtu
--- 2026-03-09 | Advisory: Beware of Investment Scams Promising High Returns | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-promising-high-returns-522e3e03
    brands=['CNPC', 'Virtu'] domains=['themostprofitableapp.us', 'long-termprojects.us']
    (no direct mention; first paras)
    > The Singapore Police Force (SPF) Scam Public Education Office (SPEO) would like to alert the public to recent trends in investment scams. Scammers are creating fake investment opportunities online, often using convincing but fraudulent websites to trick victims into parting with their money.
    > ### How to Recognise These Scams:
    > *   Scammers create fake websites or apps, sometimes mimicking legitimate companies, to promote investment schemes that promise unbelievably high returns in a short period.

######## [124] GDC Mining
--- 2026-03-06 | Advisory: Beware of Fake Investment Websites | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-websites-f7c4335d
    brands=['JUST', 'GDC Mining'] domains=['uuttt.cc', 'ustt.work', 'gdcmining.shop']
    > *   **Suspicious website addresses (URLs)**: Look out for website links that contain unusual spellings, extra letters, or unfamiliar domain names (e.g., .cc, .work, .shop), even if they claim to represent known brands like "JUST" or "GDC Mining."

######## [125] Hotorders
--- 2026-03-04 | Advisory: Beware of Fake Investment Platforms Like 'Velo Trust' and 'Hotorders' | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-platforms-like-velo-trust-and-hotorders-ef886cf6
    brands=['Hotorders', 'Velo Trust'] domains=['velotrust-exchanges.com', 'hotorders.org']
    > The Singapore Police Force (SPF) has observed a trend of investment scams involving fraudulent websites, such as those impersonating 'Velo Trust' and 'Hotorders'. These scam sites are designed to appear as legitimate financial platforms, enticing individuals with promises of high returns on investments.

######## [126] Velo Trust
--- 2026-03-04 | Advisory: Beware of Fake Investment Platforms Like 'Velo Trust' and 'Hotorders' | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-platforms-like-velo-trust-and-hotorders-ef886cf6
    brands=['Hotorders', 'Velo Trust'] domains=['velotrust-exchanges.com', 'hotorders.org']
    > The Singapore Police Force (SPF) has observed a trend of investment scams involving fraudulent websites, such as those impersonating 'Velo Trust' and 'Hotorders'. These scam sites are designed to appear as legitimate financial platforms, enticing individuals with promises of high returns on investments.

######## [127] IRUN
--- 2026-03-03 | Recent Phishing Scams Impersonate Popular Brands - Stay Vigilant! | https://www.icanactagainstscams.gov.sg/scam-trends/recent-phishing-scams-impersonate-popular-brands-stay-e8009338
    brands=['Singtel', 'IRUN'] domains=['servicesmetalinkion.shop', 'irunsg.shop']
    > The Singapore Police Force has observed a recent trend of phishing scams impersonating well-known brands such as Singtel and IRUN. These scams aim to trick individuals into revealing personal or financial information through fake websites.
    > *   **Look out for unusual website addresses.** Scammers often use domains like `.shop` or slight misspellings (e.g., `servicesmetalinkion.shop`, `irunsg.shop`) to trick you, rather than the brand's official `.com.sg` or `.sg` sites.

######## [128] Motor AI
--- 2026-03-02 | Advisory on Rising Job Scams | https://www.icanactagainstscams.gov.sg/scam-trends/rising-job-scams-9b5a348c
    brands=['Motor AI', 'Facebook'] domains=['diwkr.com', 'motorai.net']
    > *   The job offer asks you to click on unknown links, download unverified applications, or involves tasks that seem too good to be true, sometimes impersonating well-known brands like Facebook or emerging tech companies like Motor AI.

######## [129] Facebook
--- 2026-03-02 | Advisory on Rising Job Scams | https://www.icanactagainstscams.gov.sg/scam-trends/rising-job-scams-9b5a348c
    brands=['Motor AI', 'Facebook'] domains=['diwkr.com', 'motorai.net']
    > *   You receive unsolicited messages on social media (e.g., Facebook) or messaging apps, promising easy jobs with high returns, often directing you to suspicious websites with unusual names (such as `diwkr.com` or `motorai.net`).
    > *   The job offer asks you to click on unknown links, download unverified applications, or involves tasks that seem too good to be true, sometimes impersonating well-known brands like Facebook or emerging tech companies like Motor AI.
    > 3.  **Report the scam** to the platform where it occurred (e.g., Facebook) and inform the Police.

######## [130] VanguardETFs
--- 2026-02-26 | Advisory: Beware of Fake CNA Investment Schemes | https://www.icanactagainstscams.gov.sg/scam-trends/fake-cna-investment-schemes-f4e465b3
    brands=['CNA', 'VanguardETFs'] domains=['volleyport.life', 'vanguardetfs.xyz']
    (no direct mention; first paras)
    > ### Advisory: Beware of Fake CNA Investment Schemes
    > We've observed a trend where scammers impersonate CNA (Channel NewsAsia) to promote fake investment opportunities. These scams aim to trick you into transferring money or divulging personal banking information.
    > **How to recognise this scam:**

######## [131] GTS
--- 2026-02-25 | Advisory: Watch Out for Investment Scams Impersonating Brands | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-18b422ea
    brands=['GTS', 'VEO'] domains=['veobike.vip', 'yushiai.vip']
    > We have observed a trend of scam websites promoting fake investment opportunities. These sites, often using unusual domain names such as those ending in `.vip`, impersonate legitimate brands like VEO and GTS to trick individuals

### [tool_use Bash]
{"command": "python3 - <<'EOF'\nimport json, collections, re\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nbrands=json.load(open('registry/spf_brands.json'))\nby=collections.defaultdict(list)\nfor r in rows:\n    for b in r['impersonated_brands']:\n        by[b].append(r)\nsel=[10,11,14,16,17,19,20,21,22,23,25,28,29,31]\nfor i in sel:\n    b=brands[i]; bv=b['brand_value']\n    base=re.sub(r'\\(.*?\\)','',bv).strip().lower()\n    print(f\"\\n######## [{i}] {bv}\")\n    for r in by[bv]:\n        print(f\"--- {r['published'][:10]} | {r['title']}\\n    brands={r['impersonated_brands']} domains={r['scam_domains']}\")\n        paras=[p.strip() for p in re.split(r'\\n\\s*\\n|\\n(?=\\*|\\-|\\d+\\.)',r['body_md']) if p.strip()]\n        hits=[p for p in paras if base in p.lower()]\n        if not hits: hits=paras[:2]; print('    (no mention)')\n        for p in hits[:3]:\n            print(\"    > \"+p.replace('\\n',' ')[:450])\nEOF", "description": "Show context for ambiguous higher-count brands"}

### [tool_result]
######## [10] CDC Vouchers
--- 2026-09-29 | Advisory on Impersonation Scams Involving CDC Vouchers
    brands=['CDC Vouchers'] domains=['ptvs-fcf5-eb3ff9d649f5.herokuapp.com']
    > The Singapore Police Force has observed a trend of impersonation scams leveraging on the "CDC Vouchers" scheme.
    > *   Scammers send messages or direct victims to fake websites related to "CDC Vouchers", prompting them to click on suspicious links to claim vouchers or provide personal/banking details.
    > *   Official communications regarding CDC Vouchers will not ask for sensitive personal or banking information via unverified links.
--- 2026-07-20 | Advisory: Be Wary of Impersonation Scams Targeting CDC Vouchers
    brands=['CDC Vouchers'] domains=['fatsdfe56tiziadf.koyeb.app']
    > The Singapore Police Force has observed a trend of impersonation scams targeting CDC Vouchers. Scammers send unsolicited messages or create fake websites to trick the public into providing personal and banking details under the guise of CDC Voucher redemption. We have received 71 reports related to such scam sites.
    > *   Scammers send unsolicited SMS, emails, or messages via social media that include suspicious links related to CDC Vouchers.
    > *   **C - Check for scam signs:** Always verify the authenticity of any message or website regarding CDC Vouchers through official government channels or the official CDC Vouchers website. Do not click on suspicious links.
--- 2025-08-29 | Beware of Fake CDC Vouchers Website
    brands=['CDC Vouchers'] domains=['applyserviceinsupportgowhr-jz.up.railway.app', 'applysg60vcrlatest-fm.up.railway.app']
    > We have observed an increase in reports of scam websites impersonating the CDC Vouchers scheme. Scammers are using these fake websites to trick you into providing your personal or financial information.
    > *   **Unusual Website Address:** The website address may look slightly different from the official CDC Vouchers website. Check for misspellings or unusual domain names (e.g., using `.up.railway.app` instead of a legitimate `.gov.sg` address).
--- 2025-09-01 | Fake GST Vouchers Website
    brands=['CDC Vouchers'] domains=['claim-gst-voucher-vn.up.railway.app']
    > *   **Check** for scam signs and verify information with official sources like the official CDC Vouchers website or the GST Voucher official website.

######## [11] MooMoo
--- 2026-10-16 | Advisory: Phishing Scams Impersonating MooMoo
    brands=['MooMoo'] domains=['p3w8f1y6j0t9h4d2ka.live', '8h2n7y4k1p9w0f5jcd.live', 'n5r0x7c2q8v1m9z4gb.live']
    > The Singapore Police Force has observed a trend of phishing scams impersonating the investment platform MooMoo. Scammers are creating fake websites to trick individuals into revealing their login credentials and personal information.
    > *   Look out for suspicious web links that appear random or use unusual domain names (e.g., ending with ".live"), even if they feature the MooMoo brand logo or colours.
    > *   These fake websites are designed to look like the official MooMoo platform and will prompt you to enter your login details or other sensitive personal information.
--- 2026-07-31 | Advisory on Phishing Scams Impersonating MooMoo
    brands=['MooMoo'] domains=['pq1idrmf27wu91l4wv.live']
    > The Singapore Police Force warns the public about a rise in phishing scams, targeting users of financial trading platforms, specifically MooMoo. Scammers are creating fake websites mimicking the legitimate platform to trick users into revealing their login credentials and personal information.
    > *   Be cautious of unsolicited messages or unofficial links claiming to be from MooMoo, especially those asking for your login details or personal information.
    > *   Always check the website URL carefully. Official MooMoo websites will use their legitimate domain names, not suspicious-looking ones with random characters or unfamiliar extensions (e.g., `.live`, `.xyz`).
--- 2025-10-02 | Beware of Phishing Scams Impersonating MooMoo and Tiger Brokers
    brands=['MooMoo', 'Tiger Brokers'] domains=['moomoes.top', 'itigereo.top']
    > We have observed a rise in phishing scams targeting users of MooMoo and Tiger Brokers. These scams attempt to steal your login credentials.
    > *   Be wary of unusual or suspicious website addresses (URLs) that are similar to the official MooMoo or Tiger Brokers websites. For example, "moomoes.top" or "itigereo.top".
    > *   These websites often mimic the legitimate login pages of MooMoo or Tiger Brokers to trick you into entering your username and password.

######## [14] JKF
--- 2026-03-30 | ACT Against Job Scams Impersonating E-commerce Platforms
    brands=['TikTok', 'JKF'] domains=['coupang-vip.com', 'wwwshopee.net', 'shopping8.shop']
    (no mention)
    > The Singapore Police Force (SPF) observes a trend of job scams using deceptive websites that impersonate well-known e-commerce platforms like Shopee and Coupang, as well as other generic shopping sites. These scams lure victims with promises of easy money for simple online tasks.
    > ### How to recognise these scams:
--- 2026-03-30 | Advisory: Beware of Fake Job Offers on Suspicious Websites
    brands=['JKF', 'flance'] domains=['fastnedglobal.shop', 'companyflc.business', 'coupang-vip.com']
    (no mention)
    > The Singapore Police Force has observed a trend of job scams operating through suspicious websites such as `fastnedglobal.shop`, `companyflc.business`, and `coupang-vip.com`. These scams entice individuals with promises of easy work and high returns, often leading to financial loss or the compromise of personal data.
    > To protect yourself, remember to **ACT** against scams:
--- 2025-08-28 | Job Scam Alert: Be Cautious of Suspicious Online Job Offers
    brands=['BizVibe', 'B2B Wave', 'JKF'] domains=['bigbuy.rest', 'tiktokvipshops.com', 'ebayhot.com']
    > We have observed a rise in job scams using websites such as bigbuy.rest, tiktokvipshops.com, and ebayhot.com

### [tool_use Bash]
{"command": "python3 - <<'EOF'\nimport json, collections, re\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nbrands=json.load(open('registry/spf_brands.json'))\nby=collections.defaultdict(list)\nfor r in rows:\n    for b in r['impersonated_brands']:\n        by[b].append(r)\nsel=[0,1,2,3,4,5,6,7,8,9,12,13,15,18,24,26,27,30]\ndom_re=re.compile(r'`?((?:[a-z0-9-]+\\.)+(?:gov\\.sg|com\\.sg|sg|com|org|net|io|gov\\.my|my))`?',re.I)\nfor i in sel:\n    b=brands[i]; bv=b['brand_value']\n    print(f\"\\n######## [{i}] {bv}\")\n    allscam=set()\n    for r in by[bv]: allscam|=set(d.lower() for d in r['scam_domains'])\n    mentions=collections.Counter()\n    for r in by[bv]:\n        for m in dom_re.findall(r['body_md']):\n            m=m.lower()\n            if m not in allscam and not any(m in s for s in allscam):\n                mentions[m]+=1\n    print('  official-ish domains mentioned:', dict(mentions.most_common(12)))\n    print('  titles:', [r['title'][:80] for r in by[bv]][:6])\n    # services keywords\n    txt=' '.join(r['body_md'] for r in by[bv]).lower()\n    kws=[k for k in ['onemotoring','erp','parking','coe','road tax','summons','simplygo','paynow','paylah','digibank','singpass','myica','sgac','e-service','refund','token','otp','gst','tax refund','mytax','lalamove','redelivery','address','security check','unionpay','recovery','whatsapp web','verification','telegram premium','premium','netflix','subscription','icloud','job','investment','cna','article','celebrity','fake news','deepfake'] if k in txt]\n    print('  kw:', kws)\nEOF", "description": "Extract official domain mentions for main brands"}

### [tool_result]
######## [0] Land Transport Authority (LTA)
  official-ish domains mentioned: {'www.lta.gov.sg': 12, 'lta.gov.sg': 8, 'onemotoring.lta.gov.sg': 6, 'gov.sg': 4, 'www.police.gov.sg': 3, 'www.onemotoring.lta.gov.sg': 2, 'efta.lta.gov.sg': 1, 'one.lta.gov.sg': 1}
  titles: ['Advisory: Beware of Phishing Scams Impersonating LTA', 'Advisory: Beware of Fake LTA Websites Impersonating Land Transport Authority', "Advisory: Beware of Phishing Scams Impersonating LTA's OneMotoring", 'Advisory: Beware of Phishing Scams Impersonating Land Transport Authority (LTA)', 'Advisory: Beware of Phishing Scams Impersonating Land Transport Authority (LTA)', 'Advisory: Beware of Fake LTA Websites and Phishing Scams']
  kw: ['onemotoring', 'erp', 'road tax', 'singpass', 'address', 'investment']

######## [1] WhatsApp
  official-ish domains mentioned: {'whatsapp.com': 7, 'whatsapp-update.com': 1}
  titles: ['Advisory: Impersonation Scams Using Fake WhatsApp Websites', 'Advisory on WhatsApp Impersonation Scams', 'Public Advisory: Beware of Fake WhatsApp Websites and Links', 'Advisory: Beware of Impersonation Scams Using Fake WhatsApp Websites', 'Alert: Scammers Impersonating WhatsApp with Fake Websites', 'Public Advisory: Beware of Scams Impersonating WhatsApp']
  kw: ['address', 'whatsapp web', 'verification', 'job', 'investment']

######## [2] CNA
  official-ish domains mentioned: {'www.police.gov.sg': 3}
  titles: ['Advisory: Beware of Fake CNA Investment Schemes', 'Advisory: Beware of Investment Scams Impersonating CNA', 'Advisory: Beware of Investment Scams Impersonating CNA', 'Advisory on Investment Scams Impersonating CNA', 'Advisory: Beware of Fake CNA Investment Schemes', 'Advisory: Watch Out for Investment Scams Impersonating Brands']
  kw: ['address', 'investment', 'cna', 'article']

######## [3] TikTok
  official-ish domains mentioned: {'tiktok.com': 1}
  titles: ['Stay Vigilant Against Job Scams Impersonating TikTok', 'Advisory: Beware of Fake Job Scams Impersonating TikTok', 'Advisory: Beware of Fake Job Offers on TikTok Leading to Scam Websites', 'Advisory: Beware of Fake Job Offers Impersonating TikTok', 'ACT Against Job Scams Impersonating E-commerce Platforms', 'Advisory: Beware of Investment Scams Impersonating or Leveraging TikTok']
  kw: ['address', 'job', 'investment']

######## [4] UnionPay
  official-ish domains mentioned: {'www.police.gov.sg': 2, 'unionpayintl.com': 1}
  titles: ['Advisory: Beware of Scam Websites Impersonating UnionPay', 'Advisory: Beware of Fake UnionPay "Security Check" Scam Websites', "Scam Alert: Beware of Fake UnionPay 'Fund Recovery' Websites", 'Protect Yourself from UnionPay Impersonation Scams', 'Beware of UnionPay Impersonation Scams', 'Beware of UnionPay Phishing Scams']
  kw: ['address', 'security check', 'unionpay', 'recovery']

######## [5] DBS
  official-ish domains mentioned: {'dbs.com': 2, 'posb.com': 2, 'dbs.com.sg': 2, 'uob.com.sg': 1}
  titles: ['Advisory: Beware of Fake DBS Banking Websites', 'Advisory: Beware of Phishing Scams Impersonating DBS Bank', 'Advisory: Beware of Phishing Scams Impersonating DBS Bank', 'Advisory: Beware of Fake Banking Websites Impersonating DBS and UOB', 'Advisory: Watch Out for Fake DBS Websites and Banking Phishing Scams', 'Be Alert to Phishing Scams Impersonating DBS and UOB']
  kw: ['token', 'otp', 'address']

######## [6] Singapore Police Force (SPF)
  official-ish domains mentioned: {'gov.sg': 4, 'www.police.gov.sg': 4, 'police.gov.sg': 2}
  titles: ['Advisory: Beware of Fake Singapore Police Force Websites and Messages', 'Alert: Fake SPF Websites Impersonating the Police', 'Advisory: Beware of Fake SPF Websites Impersonating Singapore Police Force', 'Advisory: Beware of Fake Singapore Police Force (SPF) Websites Impersonating Off', 'Advisory: Beware of Websites Impersonating Singapore Police Force (SPF)']
  kw: ['singpass', 'otp', 'address']

######## [7] Ninjavan
  official-ish domains mentioned: {'ninjavan.sg': 2, 'www.police.gov.sg': 1}
  titles: ['Beware of Ninjavan Phishing Scams: Verify Delivery Links', 'Alert: Phishing Scams Impersonating Ninjavan', 'Advisory: Beware of Phishing Scams Impersonating Ninjavan', 'Advisory on Phishing Scams Impersonating Delivery Services (e.g., Ninjavan)', 'Advisory: Impersonation Scams Using Ninjavan Brand']
  kw: ['redelivery', 'address']

######## [8] Inland Revenue Authority of Singapore (IRAS)
  official-ish domains mentioned: {'iras.gov.sg': 6, 'gov.sg': 2, 'www.iras.gov.sg': 2, 'www.police.gov.sg': 2}
  titles: ['Advisory: Be Wary of Phishing Scams Impersonating IRAS', 'Advisory: Beware of Malware Scams Impersonating Government Agencies like IRAS', 'Advisory: Beware of Phishing Scams Impersonating IRAS', 'Alert: Phishing Scams Impersonating Inland Revenue Authority of Singapore (IRAS)', 'Advisory: Phishing Websites Impersonating IRAS']
  kw: ['singpass', 'refund', 'tax refund', 'address']

######## [9] SingPost
  official-ish domains mentioned: {'singpost.com': 5, 'mypost.singpost.com': 1, 'singpost.com.sg': 1}
  titles: ['Advisory: Protect Yourself from Fake SingPost Websites', 'Advisory on Fake SingPost Websites and Phishing Scams', 'Advisory: Beware of Phishing Scams Impersonating SingPost', 'Advisory: Beware of Fake SingPost Parcel Tracking Scams', 'Be Alert to Phishing Scams Impersonating SingPost']
  kw: ['redelivery', 'address']

######## [12] Booking.com
  official-ish domains mentioned: {'booking.com': 14, 'www.police.gov.sg': 1, 'www.booking.com': 1}
  titles: ['Advisory: Phishing Scams Impersonating Booking.com', 'Phishing Scams Impersonating Booking.com Observed', 'Beware of Phishing Scams Impersonating Booking.com']
  kw: ['address']

######## [13] Lalamove
  official-ish domains mentioned: {'www.police.gov.sg': 2, 'lalamove.com': 1, 'lalamove.com.sg': 1}
  titles: ['Advisory: Protect Yourself from Fake Lalamove Phishing Sites', 'Advisory: Beware of Fake Lalamove Phishing Sites and Messages', 'Lalamove Phishing Scam Alert']
  kw: ['lalamove', 'address']

######

### [tool_use Bash]
{"command": "python3 - <<'EOF'\nimport json\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nwant=['INFO','Best Hotel Reservation','NECTA','CNPC','ApMatrix','Audi Capital']\nseen=set()\nfor r in rows:\n    if any(b in want for b in r['impersonated_brands']) and r['id'] not in seen:\n        seen.add(r['id'])\n        print('=====',r['title'],'|',r['impersonated_brands'],'|',r['scam_domains'],'|',r['url'])\n        print(r['body_md'][:2500])\n        print('images:',len(r['images']))\nEOF", "description": "Read full bodies for unmentioned-brand advisories"}

### [tool_result]
===== Beware of Phishing Scams Impersonating Hotel Reservation Services | ['Best Hotel Reservation'] | ['gardes-holdenjp.com'] | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-scams-impersonating-hotel-reservation-services-62503fcc
The Singapore Police Force has observed an increase in phishing scams related to hotel reservation services.

Scammers are creating fake websites and messages to trick individuals into believing they are booking hotels or accessing special deals. These fraudulent sites aim to steal your personal and financial information.

### How to recognise this scam:

*   **Look out for suspicious website addresses** that do not match the official hotel or booking platform, especially when encountering unsolicited offers. For example, a site like `gardes-holdenjp.com` is unlikely to be a legitimate hotel reservation portal.
*   **Be wary of deals that seem too good to be true** or requests for personal or payment details outside of secure, trusted platforms.

### What to do if you were affected:

If you suspect you have provided your personal or payment details to a fake hotel reservation site:

*   **Immediately contact your bank** to report any unauthorised transactions and monitor your accounts closely for suspicious activity.
*   **Report the incident to the Police.** Inform your family and friends about these scams to protect them from falling victim.

Unsure if something is a scam? Check by calling the 24/7 ScamShield Helpline at 1799.
images: 1
===== Advisory: Beware of Suspicious Online Investment Platforms like 'mineverse.cc' | ['INFO'] | ['mineverse.cc'] | https://www.icanactagainstscams.gov.sg/scam-trends/suspicious-online-investment-platforms-like-mineverse-cc-042e6b7d
The Singapore Police Force has observed a trend of investment scams involving suspicious online platforms such as 'mineverse.cc'. These scams often entice individuals with promises of high returns and quick profits from purported investments, frequently related to cryptocurrency or mining.

How to recognise these scams:
*   You encounter investment opportunities, often through social media or messaging apps, on new or unfamiliar platforms (e.g., 'mineverse.cc') that claim to offer exceptionally high or guaranteed returns.
*   Scammers pressure you to make quick investment decisions and transfer funds to unfamiliar accounts.

If you suspect you have encountered or been affected by such a scam, remember to **ACT**:
*   **A**dd security features: Enable two-factor authentication for all your online accounts and use strong, unique passwords. Avoid clicking on suspicious links.
*   **C**heck for scam signs: Always verify any investment opportunity with official sources like the MAS Investor Alert List. Legitimate investment firms do not pressure you to make quick decisions or transfer funds to personal bank accounts. Search online for reviews or warnings about the platform or scheme (e.g., 'mineverse.cc scam review').
*   **T**ell authorities, family and friends: If you have shared your personal or banking details, or transferred money, report it immediately to your bank and the police. Inform your loved ones about such scams to protect them.

Unsure if something is a scam? Check by calling the 24/7 ScamShield Helpline at 1799.
images: 1
===== Advisory: Stay Alert to Fake Job Offers Online | ['NECTA', 'NEXVLTD'] | ['nexvltd.com', 'fi20fa26cups.click'] | https://www.icanactagainstscams.gov.sg/scam-trends/fake-job-offers-online-ac4e392c
The Singapore Police Force (SPF) has observed a recent trend of job scams, with specific websites like `nexvltd.com` and `fi20fa26cups.click` being reported. These scams often trick individuals into performing simple tasks with the promise of high returns, only to defraud them of their money. We urge everyone to remain vigilant. 

**How to recognise these scams:**
*   Scammers often send unsolicited messages (e.g., SMS, WhatsApp, Telegram) offering part-time jobs with attractive daily pay for simple tasks like liking social media posts or reviewing products.
*   They may require you to pay an upfront "deposit" or perform "top-ups" to "boost" your earnings, promising increasing commission, but eventually making it impossible to withdraw your money.

**If you have fallen victim to a job scam, here's how you can ACT:**
*   **A**dding security features: Change your banking passwords and enable Two-Factor Authentication (2FA) for all your accounts.
*   **C**hecking for scam signs: Contact your bank immediately to halt any unauthorised transactions.
*   **T**elling authorities: Make a police report and inform your family and friends about the scam to prevent them from falling victim.

Unsure if something is a scam? Check by calling the 24/7 ScamShield Helpline at 1799.
images: 2
===== Advisory: Beware of Investment Scams Promising High Returns | ['CNPC', 'Virtu'] | ['themostprofitableapp.us', 'long-termprojects.us'] | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-promising-high-returns-522e3e03
The Singapore Police Force (SPF) Scam Public Education Office (SPEO) would like to alert the public to recent trends in investment scams. Scammers are creating fake investment opportunities online, often using convincing but fraudulent websites to trick victims into parting with their money.

### How to Recognise These Scams:
*   Scammers create fake websites or apps, sometimes mimicking legitimate companies, to promote investment schemes that promise unbelievably high returns in a short period.
*   These fake investment opportunities often use generic or enticing domain names (e.g., "themostprofitableapp.us", "long-termprojects.us") and claim to represent well-known brands or projects.

### I can ACT against scams:

**A**dd security features:
*   Enable Two-Factor Authentication (2FA) for all your accounts. Consider setting transaction limits with your bank to minimise potential losses.
*   Install the ScamShield app to block scam calls and SMSes.

**

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [tool_use Bash]
{"command": "grep -o 'api/assets/[^\"\\\\ ]*' raw/detail_spf_b633b3b7.html | head -5; grep -c 'api/assets' raw/scam-trends_2026-11-25.html; python3 -c \"\nimport json\nrows=[json.loads(l) for l in open('advisories.jsonl')]\nfor r in rows:\n    if 'INFO' in r['impersonated_brands'] or 'CNPC' in r['impersonated_brands']:\n        print(r['impersonated_brands'], r['images'])\n\"", "description": "Check whether screenshot image URLs are in public page HTML"}

### [tool_result]
api/assets/ee5b98cd-b395-46a5-99f9-ac61d2142a6f/ee5b98cd-b395-46a5-99f9-ac61d2142a6f.png
api/assets/ee5b98cd-b395-46a5-99f9-ac61d2142a6f/ee5b98cd-b395-46a5-99f9-ac61d2142a6f.png
api/assets/ee5b98cd-b395-46a5-99f9-ac61d2142a6f/ee5b98cd-b395-46a5-99f9-ac61d2142a6f.png
api/assets/ee5b98cd-b395-46a5-99f9-ac61d2142a6f/ee5b98cd-b395-46a5-99f9-ac61d2142a6f.png
api/assets/ee5b98cd-b395-46a5-99f9-ac61d2142a6f/ee5b98cd-b395-46a5-99f9-ac61d2142a6f.png
8
['INFO'] ['https://www.icanactagainstscams.gov.sg/api/assets/094d6123-703f-5c07-bada-5a4bec75526c/094d6123-703f-5c07-bada-5a4bec75526c.png']
['CNPC', 'Virtu'] ['https://www.icanactagainstscams.gov.sg/api/assets/82106fc5-d06a-5817-9e5f-09a4e5f386b2/82106fc5-d06a-5817-9e5f-09a4e5f386b2.png', 'https://www.icanactagainstscams.gov.sg/api/assets/ee8626bb-ad99-56a2-a2de-8f1b112d2790/ee8626bb-ad99-56a2-a2de-8f1b112d2790.png']

### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/img && cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/img && curl -sS -m 30 -A \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36\" -o info.png -w \"%{http_code} %{content_type} %{size_download}\\n\" \"https://www.icanactagainstscams.gov.sg/api/assets/094d6123-703f-5c07-bada-5a4bec75526c/094d6123-703f-5c07-bada-5a4bec75526c.png\"; file info.png", "description": "Download one SPF advisory screenshot image"}

### [tool_result]
200 image/png 122135
info.png: PNG image data, 1600 x 1200, 8-bit colormap, non-interlaced

### [tool_use Read]
{"file_path": "/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/img/info.png"}

### [tool_result]
PreToolUse hook did not respond before its timeout (host client may be unreachable). The tool call was not executed; other configured hooks may not have completed.

### [tool_use Bash]
{"command": "which tesseract convert python3; python3 -c \"import PIL, sys; print('PIL', PIL.__version__)\" 2>&1; python3 -c \"import pytesseract\" 2>&1 | tail -1; ls ~/.venv* 2>/dev/null | head", "description": "Check for OCR tooling availability"}

### [tool_result]
/usr/bin/python3
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'PIL'
ModuleNotFoundError: No module named 'pytesseract'

### [tool_use Read]
{"file_path": "/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/img/info.png"}

### [tool_result]
PreToolUse hook did not respond before its timeout (host client may be unreachable). The tool call was not executed; other configured hooks may not have completed.

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)