# Recovered transcript digest: private_G1_travel_brokers (agent a929bb1e015197516)

### [user]
You are sub-agent G1 of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_G1_travel_brokers.json
Scratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/

YOUR ENTITIES
Tier 1:
1. Singapore Airlines (singaporeair.com): fraud/phishing notices (fake websites, emails, social-media giveaways, fake KrisFlyer), official channels. Scoot (flyscoot.com) as a quick child record only if it has its own scam/fraud page, else alias.
2. Changi Airport Group (changiairport.com; check changiairportgroup.com): scam notices (e.g. fake Changi giveaway/lost-luggage pages), official channels.
3. moomoo Singapore (verify SG domain/path, e.g. moomoo.com/sg). SPF brand-tag string: "MooMoo". Look for anti-fraud pages listing official channels, fake apps/groups.
4. Tiger Brokers Singapore (tigerbrokers.com.sg; check itiger.com). SPF brand-tag string: "Tiger Brokers".
5. UOB Kay Hian (uobkayhian.com; UTRADE). SPF brand-tag string: "UOB Kay Hian". (A fake domain uobkhs.com appeared in an SPF advisory - never visit it.)
6. Phillip Securities / POEMS (poems.com.sg; phillip.com.sg).
Brokers often publish lists of fake websites/apps/WhatsApp-Telegram groups impersonating them - capture counts, dates and samples (as text; never visit them).
Tier 2 (quick, at most 4): uSMART Securities Singapore (SPF brand-tag string "uSMART"; CAUTION: `usmartsg.sg` was listed by SPF as a SCAM domain - do not visit; confirm the real domain from official pages or the MAS Financial Institutions Directory), MoneySmart (moneysmart.sg; SPF brand-tag string "MoneySmart"; fake domains money-sm.art, moneysmart.money, moneysmart.click, moneysmart.one - do not visit), Chan Brothers Travel (SPF brand-tag string "Chan Brothers"), FSMOne/iFAST, Webull SG, Syfe/Endowus/StashAway.

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

### [user]
<system-reminder>
Your final report is delivered through SubagentHandback: when your work is complete, call SubagentHandback({message: <your full report>}) and then stop. Only a SubagentHandback call reaches your caller as your result; plain text you write at the end is not delivered.
</system-reminder>

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md", "description": "Read the sub-agent brief"}

### [tool_result]
# Sub-agent brief: SG private-sector entity registry (shared by all groups)

You are building part of a registry of Singapore organisations -> their official domains/subdomains -> every page
where they publish scam/security-alert information. It feeds a Singapore scam-intelligence pipeline: official domains
become an ALLOWLIST for detecting lookalikes; scam-alert pages become SOURCES. Today is 2026-11-25.

## Step 0
Read `/home/ankur/scamtrends_feed/registry/FORMAT.md` (section 1 "Entity record" and "Ground rules") and follow it
strictly. Skim `/home/ankur/scamtrends_feed/sources/03_community_commercial.md` (earlier survey; reuse its facts, but
re-open any page before citing it). If the Read/Write tools time out (hook issue), use Bash (cat, heredoc, python).

## Output
Write a JSON ARRAY of entity records to your output path (rewrite it after each entity so partial work survives).
Validate: `python3 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py <your output>`
until it prints "0 problems". Raw downloads go in your group's scratch subfolder.

## Per-entity method (light volume: <=15 requests per site, >=1 s between requests to the same host)
1. Fetch homepage + robots.txt with curl and a normal browser UA:
   UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
   curl -sL -A "$UA" --max-time 30 -o FILE -w '%{http_code} %{url_effective}\n' URL
2. Sitemaps: from robots `Sitemap:` lines (else try /sitemap.xml once). Grep URLs for
   `scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect`. <=10 sitemap files per site.
3. WebSearch, e.g. `site:<domain> scam`, `<brand> Singapore official SMS sender ID`, `<brand> Singapore scam alert`,
   `<brand> official websites list`.
4. Open each candidate page (curl; if JS-rendered and curl gets only a shell, WebFetch once). Record: what it is,
   number of dated items, newest date, whether it lists CONCRETE indicators (fake domains/URLs, phone numbers, emails,
   sender IDs, apps, social handles, bank accounts) vs narrative only, and one short verbatim sample (<=200 chars).
5. Collect allowlist facts from the entity's OWN pages: official domains ("our official websites are..."),
   login/payment hosts seen in links (e.g. internet-banking.x.com.sg), SMS sender IDs / short codes, hotlines (esp.
   anti-scam/fraud hotlines), official app names (as in app-store links on the site), social accounts linked from the
   site footer, official email sender domains/addresses, short-link domains.

## Field rules
- entity_id: primary official registrable domain (eTLD+1), lowercase, no www (e.g. `dbs.com.sg`, `sc.com`, `grab.com`).
  If the SG business lives under a path of a global domain (e.g. sc.com/sg, dhl.com/sg-en, moomoo.com/sg) the
  entity_id is still that registrable domain; country "SG"; say so in notes.
  Sub-brand with its OWN registrable domain AND its own scam/security pages -> separate record with parent_entity_id
  (e.g. POSB posb.com.sg -> parent dbs.com.sg). Otherwise fold it into aliases. A product without its own domain gets a
  `<parent>#<slug>` record only if it has dedicated scam/security pages; otherwise it is just an alias.
- aliases: common names/abbreviations AND the exact SPF brand-tag strings given for your group (e.g. "Ninjavan",
  "DBS PayLah", "MooMoo", "SPX") so a mechanical brand map can join on them.
- sector: exactly one value from FORMAT.md. parent_entity_id: registrable domain of the parent if relevant, else null.
- official_domains: ONLY registrable domains (eTLD+1; no www, no paths) confirmed on the entity's OWN pages, either
  (a) explicitly stated as official, or (b) the domain serving the official site, or a login/app/payment host linked
  from the official site's own navigation. Say in notes which are (a) vs (b). Never add a domain from memory or from a
  third-party page. If an official page lists third-party/partner hosts as legitimate (e.g. a qualtrics.com survey
  host), put the exact FQDN in official_hosts, NOT the third party's registrable domain in official_domains; explain
  in notes.
- official_hosts: notable FQDNs seen in official links (login, internet banking, payment, tracking, help centre),
  e.g. internet-banking.dbs.com.sg. Only hosts you actually saw.
- scam_info: one object per useful page (aim 2-6 per Tier-1 entity, 1-2 per Tier-2): scam hub, latest-scams/alerts
  list, official-channels/sender-ID page, fake-indicator lists, report-fraud page. Keys EXACTLY:
  url, kind, lists_indicators, access, machine_url, item_count, latest_item_date, verified, sample, notes.
  * kind: advisory_feed (dated list of alerts) | alert_page (single alert/notice) | scam_faq (generic guidance hub)
    | official_channels (the entity's genuine domains/numbers/sender IDs) | fake_indicator_list (lists fake
    domains/numbers/apps/accounts) | news_releases (press releases; also media "scams" topic pages) | report_portal
    | statistics.
  * lists_indicators: types of CONCRETE identifiers on the page, from: domain, url, phone, email, sms_sender_id, app,
    social_handle, bank_account, entity_name. [] = narrative only. For kind=official_channels these are the types of
    GENUINE identifiers listed; for every other kind they are SCAM indicators (don't count the entity's own hotline as
    "phone" on an alert page). Write "(official)" or "(fake)" in notes when ambiguous.
  * access: html | rss | atom | sitemap | json_api_documented | csv | pdf. machine_url: RSS/Atom/sitemap/CSV/PDF URL
    that lets a machine discover or read the page (e.g. the sitemap file containing it), else null.
  * item_count: integer count of dated alerts/items on the page (null if not a list).
    latest_item_date: ISO YYYY-MM-DD (or YYYY-MM) of the newest item; null if undated.
  * verified: "2026-11-25 HTTP <status>" from your own fetch (append " via WebFetch" if that is how you read it).
  * sample

### [tool_use Bash]
{"command": "cat /home/ankur/scamtrends_feed/registry/FORMAT.md; echo ----; ls -la /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/", "description": "Read FORMAT.md and list work folder"}

### [tool_use Bash]
{"command": "grep -n -i -E \"singapore airlines|singaporeair|scoot|changi|moomoo|tiger|uob kay hian|uobkh|phillip|poems|usmart|moneysmart|chan brothers|fsmone|ifast|webull|syfe|endowus|stashaway\" /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -80", "description": "Grep earlier survey for my entities"}

### [tool_result]
# Registry output format (shared by all research agents)

Each agent writes ONE JSON file (a top-level array) to `/home/ankur/scamtrends_feed/registry/`.
Keep to these keys exactly so the files can be merged mechanically. Unknown → `null` or `[]`,
never invented. Every factual claim must be backed by an `evidence` URL you actually opened.

## 1. Entity record (`entities_<partition>.json`)

`entity_id` is the entity's **primary official registrable domain**, lowercase, no scheme/www
(e.g. `police.gov.sg`, `scdf.gov.sg`, `dbs.com.sg`, `whatsapp.com`). This makes IDs deterministic
across agents. A programme without its own domain uses `<parent domain>#<slug>`
(e.g. `ica.gov.sg#sg-arrival-card`).

```json
{
  "entity_id": "police.gov.sg",
  "name": "Singapore Police Force",
  "abbr": "SPF",
  "aliases": ["Singapore Police Force (SPF)", "Police"],
  "sector": "gov.ministry | gov.statboard | gov.organ | gov.dept | gov.programme | gov.court | quasi_gov | bank | payments | telco | logistics | ecommerce | marketplace | transport | utility | retail | travel | media | brokerage | insurance | healthcare | tech_platform | crypto | other",
  "parent_entity_id": "mha.gov.sg",
  "country": "SG",
  "official_domains": ["police.gov.sg"],
  "official_hosts": ["www.police.gov.sg", "eservices.police.gov.sg"],
  "scam_info": [
    {
      "url": "https://www.police.gov.sg/Media-Room/News",
      "kind": "advisory_feed | alert_page | scam_faq | official_channels | fake_indicator_list | news_releases | report_portal | statistics",
      "lists_indicators": ["domain", "url", "phone", "email", "sms_sender_id", "app", "social_handle", "bank_account", "entity_name"],
      "access": "html | rss | atom | sitemap | json_api_documented | csv | pdf",
      "machine_url": "https://www.police.gov.sg/sitemap/sitemap.xml",
      "item_count": 354,
      "latest_item_date": "2026-11-20",
      "verified": "2026-11-25 HTTP 200",
      "sample": "short verbatim excerpt or example indicator",
      "notes": ""
    }
  ],
  "official_channels": {
    "sms_sender_ids": [], "hotlines": [], "short_link_domains": [], "social": []
  },
  "evidence": ["https://... page that confirms the official domains"],
  "notes": ""
}
```

`lists_indicators: []` means the page is narrative only (no concrete scam indicators).

## 2. Host-discovery record (`hosts_ct.json`), for the subdomain/CT agent only

```json
{
  "host": "www.scamshield.gov.sg",
  "registrable_domain": "scamshield.gov.sg",
  "discovered_via": "crt.sh | certspotter | sitemap | search | trusted_sites_list | link",
  "cert_first_seen": "2023-...", "cert_last_seen": "2026-...",
  "resolves": true, "a_records": ["..."],
  "http_status": 200, "title": "...",
  "scam_relevant": "yes | maybe | no",
  "owner_entity_id": "scamshield.gov.sg",
  "notes": ""
}
```

## 3. Brand-resolution record (`spf_brand_map.json`), for the brand agent only

Input: `registry/spf_brands.json` (159 SPF `Brand` tag values with counts, categories, sample domains, titles).

```json
{
  "brand_value": "Land Transport Authority (LTA)",
  "tag_id": "uuid from input",
  "resolution": "real_entity | fictitious_scam_brand | generic_or_placeholder | ambiguous",
  "entity_id": "lta.gov.sg",
  "official_domains": ["lta.gov.sg", "onemotoring.lta.gov.sg"],
  "is_singapore_entity": true,
  "sector": "gov.statboard",
  "confidence": "high | medium | low",
  "evidence": ["https://..."],
  "notes": "e.g. 'scam domains imitate OneMotoring/ERP payments'"
}
```

## Ground rules (all agents)
- Use only public, user-facing pages, robots.txt, sitemaps, RSS/Atom, published downloads, documented APIs,
  public certificate-transparency search (crt.sh, certspotter), DNS lookups, and web search.
- Do NOT probe undocumented backend/CMS/API paths, brute-force paths, port-scan, log in or register.
  An earlier attempt to query an undocumented CMS API was blocked by policy. If any action is blocked, stop
  that line of work and report it. Don't work around it.
- Do NOT visit scam/malicious domains. Official sites only.
- Light request volume. Normal browser User-Agent. Respect robots.txt.
- Scratch downloads go in `/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/`.
----
total 96
drwxrwxr-x  2 ankur ankur  4096 Nov 25 18:12 .
drwxrwxr-x 11 ankur ankur  4096 Nov 25 18:14 ..
-rw-rw-r--  1 ankur ankur  9545 Nov 25 18:12 BRIEF.md
-rw-rw-r--  1 ankur ankur 62621 Nov 25 17:57 dbs_robots.txt
-rw-rw-r--  1 ankur ankur     3 Nov 25 18:10 _empty.json
-rw-rw-r--  1 ankur ankur  5497 Nov 25 18:10 validate.py

### [tool_result]
(Bash completed with no output)

### [tool_use Bash]
{"command": "ls -la /home/ankur/scamtrends_feed/sources/ 2>&1 | head; wc -l /home/ankur/scamtrends_feed/sources/03_community_commercial.md; head -60 /home/ankur/scamtrends_feed/sources/03_community_commercial.md; echo ----; cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py", "description": "Skim survey file and read validator"}

### [tool_result]
total 92
drwxrwxr-x 3 ankur ankur  4096 Nov 25 18:14 .
drwxrwxr-x 7 ankur ankur  4096 Nov 25 18:11 ..
-rw-rw-r-- 1 ankur ankur  2516 Nov 25 17:18 00_sg_signal_baseline.md
-rw-rw-r-- 1 ankur ankur 18680 Nov 25 17:20 01_sg_official.md
-rw-rw-r-- 1 ankur ankur 21552 Nov 25 17:17 02_generic_feeds.md
-rw-rw-r-- 1 ankur ankur 23093 Nov 25 17:15 03_community_commercial.md
drwxrwxr-x 2 ankur ankur  4096 Nov 25 18:14 __pycache__
-rw-rw-r-- 1 ankur ankur  5188 Nov 25 17:16 sgfilter.py
146 /home/ankur/scamtrends_feed/sources/03_community_commercial.md
# Non-government Singapore scam sources: community, media, industry, commercial, academic, open-source

Captured 2026-11-25. Scope excludes SG government sources (SPF/ICAAS, MAS, ScamShield, ScamAlert/NCPC, CSA) and global phishing feeds. Those are covered elsewhere.
Method: WebSearch to find each source, then a direct fetch (curl with a browser UA, or WebFetch) of the public page only. I did not log in, register, or join any group. I did not visit any scam URL or bypass a bot challenge.

## Bottom line

**No non-government source we can reach publicly gives a current, machine-readable SG scam-domain list.** Every SG-specific source with real IOC volume is one of three things:
1. **Stale or academic.** The best one is a 4,660-report scrape of scamalert.sg covering 2016–2020.
2. **Redacted.** The IMC'25 smishing set replaces URLs with `<URL>`.
3. **Gated behind commercial or membership access.** This covers Group-IB, Whoscall ASI, ScamAdviser, GASA and the Global Signal Exchange.

Banks, telcos and marketplaces publish **narrative advisories and allowlists**, not blocklists. Their allowlists of official domains are useful as a **negative set** for suppressing false positives. Community phone-lookup sites are live but low-volume and noisy, and most of their ToS forbid scraping.

For the SG scam-website dataset, the SPF ICAAS feed (209 records) remains the only clean, dated, SG-attributed domain source. Nothing here replaces it. The two open datasets below are best used as **text/lure corpora and brand-frequency priors**, not as an IOC feed.

## Ranked table (by data usefulness for an SG scam-website / IOC dataset)

| # | Source | Owner / type | What it lists | Volume | Machine-readable | Freshness (latest seen) | Licence / terms | SG-specificity | Usefulness |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [zeyalt/Crime-Script-Analysis-NLP `Data/scam_raw_dataset.csv`](https://github.com/zeyalt/Crime-Script-Analysis-NLP) | Univ. of Leeds (Lwin Tun & Birks, *Crime Science* 2023) / academic scrape of scamalert.sg | Victim scam stories + "scammer details" (name, contact) + scam type | 4,660 reports; 971 have phone-like contacts; 503 stories mention a URL | CSV (5.8 MB) on GitHub raw, **but the file contains git merge-conflict markers**. Keep the HEAD side to parse it | 2020-07-17 (range 2016-07-20 → 2020-07-17) | **No LICENSE file** (all rights reserved by default). Upstream content belongs to NCPC and the submitters. **Contains PII** (submitter names, bank account numbers) | 100% SG | **Medium.** Best open SG scam-text corpus with a type label and phone IOCs. Stale for domains |
| 2 | [reportsmishing/Smishing-Dataset-IMC25](https://github.com/reportsmishing/Smishing-Dataset-IMC25) | UCL et al., IMC '25 / academic | Labelled smishing texts: sender type, network, language, named entity (impersonated brand), scam type, lure principles | 33,869 rows global; **~190 SG-relevant** (23 on SGP networks; DBS 69, OCBC 40, Singpass 24, POSB 8, IRAS 8, Singtel 7, UOB 6, SingPost 3, CPF 3) | CSV (9.5 MB) on GitHub raw | `time` field is free-form ("Today 8:48 AM"). Only 157 rows have ISO dates, earliest 2021-09-17 | **CC BY 4.0** | Low share, but SG brands are tagged | **Medium-low.** URLs redacted to `<URL>`, so no domains. Good for SG lure templates and brand priors. Cleanest licence here |
| 3 | Group-IB SG reports: [Immediate Era (2025-10-21)](https://www.group-ib.com/blog/immediate-era-fraud-singapore/), [SingPost delivery scams](https://www.group-ib.com/blog/fake-delivery-scams-singapore/), [SupportGoWhere phishing PR](https://www.group-ib.com/media-center/press-releases/phishing-campaign-targeting-singapore/) | Group-IB / commercial TI | Campaign narratives with **counts**: 52 redirect domains and 119 fake-news domains (Immediate Era); 107 sites incl. 85 SingPost look-alikes (delivery) | Domain lists **not published**. Only 1 example domain appears in the Immediate Era text | HTML narrative. IOCs "available to customers in the TI portal" | 2025-10-21 | Group-IB site ToS, proprietary | High | **Low as data, high as context.** Gives ground-truth scale for validating coverage |
| 4 | [callchecker.fyi/sg](https://callchecker.fyi/sg) | Unknown operator / crowdsourced phone lookup | Top-reported SG numbers + recent reports (category: Scam/Spam/Other, date, comment) | 459 reports total; top number has 7 reports | HTML only | 2026-09-29 | No API seen. robots allows the country page. Content is crowdsourced and unverified | High (SG page) | **Low.** Tiny and noisy. Comments include off-topic/defamatory posts |
| 5 | [numbers.online/browse/sg](https://numbers.online/browse/sg) | Numbers Online (UK co. 388466 per ToS) / aggregated complaints + community | SG numbers with "spam/scam signals", report counts, source count, risk label | 71 numbers, 626 reports, 22 active in the last 30 days | HTML + **documented API with a free self-service key** (per-number E.164 lookup: line type, carrier, optional risk signal) | "2d ago" (≈2026-11-23) | **ToS forbids scraping/bulk extraction and building a competing database.** robots disallows `/api/` crawling (the API itself is keyed) | High | **Low.** Use it only as a per-number enrichment API within the ToS, not as a list source |
| 6 | [whoseno.com (SG)](https://whoseno.com/singapore/recent-lookups) | WhoseNo / crowdsourced lookup + caller-ID app | "Most reported spam numbers in SG, last 7 days" with calls, reports, activity score (0–10

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o robots.txt -w '%{http_code} %{url_effective}\\n' https://www.singaporeair.com/robots.txt; sleep 1; curl -sL -A \"$UA\" --max-time 30 -o home.html -w '%{http_code} %{url_effective}\\n' https://www.singaporeair.com/en_UK/sg/home; ls -la; head -c 600 robots.txt; echo; grep -i sitemap robots.txt | head", "description": "Fetch Singapore Airlines robots.txt and homepage"}

### [tool_result]
200 https://www.singaporeair.com/robots.txt
200 https://www.singaporeair.com/en_UK/sg/home/
total 100
drwxrwxr-x 2 ankur ankur  4096 Nov 25 18:14 .
drwxrwxr-x 3 ankur ankur  4096 Nov 25 18:14 ..
-rw-rw-r-- 1 ankur ankur 88791 Nov 25 18:14 home.html
-rw-rw-r-- 1 ankur ankur  1194 Nov 25 18:14 robots.txt
User-agent: *
Disallow: /en_UK/partner-kf-upgrade-terms/
Disallow: /en_UK/ppsclub-krisflyer/stayintouch/
Disallow: /en_UK/ppsclub-krisflyer/my-personal-details/reset-pin/
Disallow: /en_UK/nz/plan-travel/local-promotions/friends-and-family/
Disallow: /sqdirect/
Disallow: /jsp/cms/
Disallow: /bin/
Disallow: /em/
Disallow: /pdf/
Disallow: /template
Disallow: /work-in-progress
Disallow: /rb_bf
Disallow: /2.2/w/w-743712/init/js/
Disallow: /showThirdPartyBooking.action
Disallow: /managebooking*
Disallow: /cookieTracker.form
Disallow: /salutationsTitles.form
Disallow: /getAirportListJson.form
Disallo
Sitemap: https://www.singaporeair.com/sitemap.xml

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && cat robots.txt | tail -20; UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o sitemap.xml -w '%{http_code} %{url_effective} %{content_type}\\n' https://www.singaporeair.com/sitemap.xml; ls -la sitemap.xml; head -c 1500 sitemap.xml; echo; grep -o '<loc>[^<]*</loc>' sitemap.xml | wc -l", "description": "Fetch SIA sitemap index"}

### [tool_result]
Disallow: /flightsearch/getTitleDetails.form
Disallow: /flightsearch/getCountryDetails.form
Disallow: /sia-service-centre/appointment/api/
Disallow: /getsiteSearchResults.form
Disallow: /siteSearch.form
Disallow: /ice/*/changeSeat
Disallow: /ice/*/getBPEmail
Disallow: /*.form$
Disallow: /*resetpassword
Disallow: /*faqCategory
Disallow: /*utm_source=
Disallow: /*category=
Disallow: /*searchparam=
Disallow: /*?id
Crawl-delay: 9

User-agent: ia_archiver
Disallow: /

Sitemap: https://www.singaporeair.com/sitemap.xml200 https://www.singaporeair.com/sitemap.xml application/xml
-rw-rw-r-- 1 ankur ankur 12154 Nov 25 18:14 sitemap.xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/application-sitemap.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/au.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/bd.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/bn.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/kh.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/cn.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/hk.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/in.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/id.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/jp.xml</loc>
<lastmod>2026-07-27</lastmod>
</sitemap>
<sitemap>
<loc>https://www.singaporeair.com/content/dam/sia/root/sitemap/my.xml</loc>
<lastmod>2026-07-27</
90

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && grep -o '<loc>[^<]*</loc>' sitemap.xml | sed 's/<[^>]*>//g' | grep -iE 'sg|root|application' ; sleep 9; UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o sg.xml -w '%{http_code} %{url_effective}\\n' https://www.singaporeair.com/content/dam/sia/root/sitemap/sg.xml; ls -la sg.xml; grep -o '<loc>[^<]*</loc>' sg.xml | wc -l; grep -o '<loc>[^<]*</loc>' sg.xml | sed 's/<[^>]*>//g' | grep -iE 'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect|advisor|notice'", "description": "Fetch SIA Singapore sitemap and grep scam URLs"}

### [tool_result]
https://www.singaporeair.com/content/dam/sia/root/sitemap/application-sitemap.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/au.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/bd.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/bn.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/kh.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/cn.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/hk.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/in.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/id.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/jp.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/my.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/mv.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/np.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/nz.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ph.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/sg.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/kr.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/lk.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/tw.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/th.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/vn.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/at.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/be.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/hr.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/dk.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/fr.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/de.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/gr.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ie.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/it.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/nl.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/no.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/pl.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/pt.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/es.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/se.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ch.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/tr.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/gb.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/sa.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ae.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/za.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/br.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ca.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/us.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/au-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/at-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/bd-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/be-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/br-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/bn-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/kh-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ca-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/cn-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/hr-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/dk-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/fr-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/gr-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/hk-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/in-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/id-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ie-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/it-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/jp-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/my-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/mv-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/mm-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/np-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/nl-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/nz-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/no-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ph-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/pl-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/pt-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/de-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/sa-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/sg-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/za-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/kr-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/es-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/lk-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/se-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/ch-destinations.xml
https://www.singaporeair.com/content/dam/sia/root/sitemap/tw-destinations.xml
https://www.sing

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re\nx=open('sg.xml').read()\nurls=re.findall(r'<url>(.*?)</url>',x,re.S)\nprint(len(urls))\nfor u in urls:\n    loc=re.search(r'<loc>(.*?)</loc>',u).group(1)\n    lm=re.search(r'<lastmod>(.*?)</lastmod>',u)\n    if 'en_UK' in loc and re.search(r'scam|phish|fraud|newsalert|global_footer/security|giveaway|social|contact-us|krisflyer-contact|cyber',loc,re.I):\n        print(loc, lm.group(1) if lm else None)\nEOF\ngrep -c 'newsalert-listing/' sg.xml", "description": "List scam-related SIA sitemap entries with lastmod"}

### [tool_result]
2226
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-GenZ23/ 2024-12-17T04:05:56Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-kff24/ 2024-12-27T03:29:24Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-12daysChristmas24/ 2024-12-27T03:49:23Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-wokf/ 2024-12-27T03:50:11Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-krisshop24/ 2024-12-27T03:51:33Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-kfxkslny25/ 2025-01-06T09:23:00Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-StefanieSunGiveaway/ 2025-02-21T03:26:52Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-10millionmembersgiveaway/ 2025-04-28T07:25:48Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-WickedGiveaway/ 2025-03-18T01:57:56Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-LGG2025/ 2025-04-07T02:37:14Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-DesPandaGiveaway/ 2025-04-28T02:04:19Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-KFTravelBuddies/ 2025-06-11T04:26:41Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-MerlynGiveaway/ 2025-07-16T02:19:35Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-nationaldaygiveaway2025/ 2025-08-05T06:09:56Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-scootgiveaway2025/ 2025-08-21T07:40:39Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/BirthdayBashGiveaway2025/ 2025-10-06T09:09:37Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/KFSocial-JackyCheung60/ 2025-11-05T02:07:49Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-12DaysofGiveaway25/ 2025-12-12T02:22:28Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-ThePerfectGiftGiveaway/ 2026-01-23T02:32:36Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/KFSocial_CNY26/ 2026-01-30T02:20:41Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-KFF26SocialGiveaway/ 2026-06-10T06:32:49Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/tnc-promo/kfsocial-ndp26tnc/ 2026-08-07T08:52:08Z
https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/kf-promo/kfsocial/ 2025-01-02T09:52:03Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/netherlands/contact-us/ 2026-09-25T06:17:30Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/france/contact-us/ 2026-09-25T07:12:24Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/germany/contact-us/ 2026-09-25T06:04:08Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/new-zealand/contact-us/ 2025-04-02T01:52:36Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/singapore/contact-us/ 2024-08-02T13:22:13Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/hongkong/contact-us/ 2024-08-02T13:22:14Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/italy/contact-us/ 2026-09-30T07:45:58Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/malaysia/contact-us/ 2025-11-14T06:13:22Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/spain/contact-us/ 2026-09-30T08:40:50Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/switzerland/contact-us/ 2025-08-23T12:45:10Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/uk/contact-us/ 2026-10-05T06:22:15Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/denmark/contact-us/ 2026-09-28T06:26:34Z
https://www.singaporeair.com/en_UK/sg/plan-travel/privileges/travel-insurance/sweden/contact-us/ 2026-09-28T06:35:39Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/ 2026-10-23T03:26:06Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/high-volume-of-customers-at-sia-service-centre-at-ion-orcha/ 2025-04-22T10:29:39Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-us-reservations-and-krisflyer-services-hotline/ 2025-04-22T10:29:00Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-singapore-airlines-flights-affected-by-typhoon-ragas/ 2025-09-23T08:06:12Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-singapore-airlines-flights-affected-the-geopolitical/ 2026-10-30T03:11:07Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-phishing-scams-and-good-cybersecurity-practice/ 2026-11-16T02:02:50Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-the-carriage-of-power-banks-on-board-sia-flights-/ 2026-04-06T05:17:09Z
https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/customer-advisory-on-delays-in-email-responses/ 2026-11-14T10:05:46Z
https://www.singaporeair.com/en_UK/sg/about-us/sustainability/social/ 2026-09-14T04:00:43Z
https://www.singaporeair.com/en_UK/sg/contact-us/ 2026-07-28T03:14:48Z
https://www.singaporeair.com/en_UK/sg/global_footer/security/ 2026-01-08T01:49:29Z
https://www.singaporeair.com/en_UK/sg/faq/accounts-and-security/krisflyer-contact-details-verification/ 202

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; sleep 9; curl -sL -A \"$UA\" --max-time 30 -o phishing_adv.html -w '%{http_code} %{url_effective}\\n' https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-phishing-scams-and-good-cybersecurity-practice/; sleep 9; curl -sL -A \"$UA\" --max-time 30 -o security.html -w '%{http_code} %{url_effective}\\n' https://www.singaporeair.com/en_UK/sg/global_footer/security/; ls -la; python3 - <<'EOF'\nimport re,html\nfor f in ['phishing_adv.html','security.html']:\n    x=open(f,errors='ignore').read()\n    x=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',x)\n    # keep main content only roughly\n    t=re.sub(r'(?s)<[^>]+>',' ',x)\n    t=html.unescape(re.sub(r'\\s+',' ',t))\n    i=t.lower().find('phishing') if 'phish' in f else t.lower().find('security')\n    print('=====',f,len(t))\n    # print region around keywords\n    for kw in ['Advisory on Phishing','phishing','scam','official']:\n        j=t.find(kw)\n        print(kw,j)\n    print(t[:200])\nEOF", "description": "Fetch SIA phishing advisory and security pages"}

### [tool_result]
200 https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-phishing-scams-and-good-cybersecurity-practice/
200 https://www.singaporeair.com/en_UK/sg/global_footer/security/
total 712
drwxrwxr-x 2 ankur ankur   4096 Nov 25 18:15 .
drwxrwxr-x 3 ankur ankur   4096 Nov 25 18:14 ..
-rw-rw-r-- 1 ankur ankur  88791 Nov 25 18:14 home.html
-rw-rw-r-- 1 ankur ankur  60219 Nov 25 18:15 phishing_adv.html
-rw-rw-r-- 1 ankur ankur   1194 Nov 25 18:14 robots.txt
-rw-rw-r-- 1 ankur ankur  74456 Nov 25 18:15 security.html
-rw-rw-r-- 1 ankur ankur 473675 Nov 25 18:14 sg.xml
-rw-rw-r-- 1 ankur ankur  12154 Nov 25 18:14 sitemap.xml
===== phishing_adv.html 4363
Advisory on Phishing -1
phishing 13
scam 22
official 1136
 Advisory on phishing scams and good cybersecurity practices | Singapore Airlines Plan travel Flying with us Travel info PPS Club & KrisFlyer Corporate Help Feedback Singapore · English Log in Sign Up
===== security.html 9992
Advisory on Phishing -1
phishing 565
scam 5147
official 1807
 Security | Singapore Airlines Plan travel Flying with us Travel info PPS Club & KrisFlyer Corporate Help Feedback Singapore · English Log in Sign Up --> Home Keeping your data safe Keeping your data

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re,html\nfor f in ['phishing_adv.html','security.html']:\n    x=open(f,errors='ignore').read()\n    x=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',x)\n    t=re.sub(r'(?s)<[^>]+>',' ',x)\n    t=html.unescape(re.sub(r'\\s+',' ',t))\n    print('=====',f)\n    # cut the footer\n    end=t.find('Follow us')\n    print(t[150: (end if end>0 else 6000)][:6500])\nEOF", "description": "Print text content of SIA advisory pages"}

### [tool_result]
===== phishing_adv.html
e Help Feedback Singapore · English Log in Sign Up --> Home HighFlyer & Corporate Newsroom News alerts Advisory on phishing scams and good cybersecurity practices Advisory on phishing scams and good cybersecurity practices The protection of our customers’ personal data is of utmost importance to us. Singapore Airlines (SIA) advises customers to remain vigilant against scams and adopt good cybersecurity practices. Common Type of Scams Scammers may: Post fake contact details on the Internet, Google Maps, wiki pages, and community forums. Impersonate SIA through phone calls, social media accounts, messaging apps, or fraudulent email addresses. They may request for personal information, flight details, login credentials, or banking and credit card details. SIA will never ask customers to disclose their password or one-time password (OTP) to us by phone, email, or SMS. Do not disclose these to anyone, including someone claiming to be a SIA employee. Only enter your OTP on our official website or mobile app. Offer fraudulent job opportunities. All available job vacancies are advertised on our official Careers portal and LinkedIn. Publish fraudulent advertisements, requests, or giveaways to collect personal data or bank card details, or to entice people to click on phishing links or open malicious email attachments. More information about scams may be found on the ScamShield website . How SIA Helps Protect Customers from Scams Our customers’ online safety and security are important to us. To protect our customers from fraudulent text messages, SIA has registered our sender IDs with Singapore’s SMS Sender ID Registry. Messages sent to Singapore mobile numbers (+65) from unregistered sender IDs will be labelled “Likely-SCAM”. However, customers should remain vigilant, even if a message does not carry this label. When customers report a potential scam, SIA will check if their booking or KrisFlyer account have been affected. Where necessary, scam sites and social media accounts that reflect contact details or impersonate SIA are reported to the relevant authorities and parties for removal. Good Cybersecurity Practices To safeguard against scams and phishing attempts: 1. Always verify before you act Access your booking or KrisFlyer account only through our official website or the SingaporeAir mobile app. Avoid clicking on links, scanning QR codes, opening attachments, or installing software at the request of unknown or suspicious senders. Do not use contact details provided by unverified sources. Customers who require assistance are advised to contact SIA using the details listed on our official website . To verify whether a call, text message, email, or social media account is genuine, or to report a suspected fake SIA website, please share the details via this link. 2. Protect your bookings and accounts Keep your registered contact details up to date. Use a strong, unique password for your KrisFlyer account and a different password for your email account. Always login to your account using our official website or mobile app . Download the SingaporeAir mobile app from an official app store. Enable two-factor authentication (2FA) for flight bookings made through the SIA website or SingaporeAir mobile app. This provides an additional layer of security by requiring a time-sensitive, randomly generated OTP before you can access customer details or change or cancel a booking. Find out more about 2FA here . More information on keeping your personal data safe may be found here . What to Do If You Suspect a Scam If you think you may have fallen victim to a scam, act immediately. Shared your banking or card details, or made a payment? Contact your bank or card issuer immediately. Disclosed your account password? Change it immediately through our official website or mobile app. Shared an OTP or noticed suspicious booking or KrisFlyer activity? Contact SIA immediately through our official contact channels . Keep screenshots, messages, and transaction records as evidence, and lodge a police report. You may also call the 24/7 ScamShield Helpline at 1799 for assistance. Updated on 16 November 2026, 0950hrs (GMT+8) First posted on 18 July 2017, 1930hrs (GMT+8) 
===== security.html
--> Home Keeping your data safe Keeping your data safe At Singapore Airlines, we take the security of your personal and financial information seriously. We're constantly enhancing our security systems, but there are several things you can do too to safeguard your privacy: Beware of latest security alerts Enable two-factor authentication (2FA) for bookings Secure your KrisFlyer account Know the telltale signs of phishing emails / SMS Email Security Latest Security Alerts Cybercriminals may try to impersonate Singapore Airlines to trick you into revealing sensitive information. For the latest security alerts, please refer to our Facebook page . Enable two-factor authentication (2FA) for bookings You can now add an extra layer of verification when you manage flight bookings. This strengthens the security of your booking from unauthorised changes. With 2FA enabled, a One-Time Password (OTP) will be required when you want to access passenger details, change flights, or cancel flights. How to enable 2FA: You will be prompted to enable 2FA on the passenger details page when you make a flight booking. 2FA cannot be turned off after booking confirmation. It is recommended that you enable or disable it before you proceed to the next page in your booking. When will 2FA be applied: Accessing passenger details Turing auto check-in on Making changes to your booking Cancelling your booking Performing OTP verification: OTP will be sent to your email address or mobile number registered in your booking. If you logged in to your KrisFlyer profile, it will be sent to the contact details registered in your KrisFlyer profile. OTP will be sent from an official Singapore Airlines account (SMS: SQbooking and Email: Singapore Airlines). D

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re,html\nfor f in ['phishing_adv.html','security.html','home.html']:\n    x=open(f,errors='ignore').read()\n    links=re.findall(r'<a\\b[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>',x,re.S)\n    print('=====',f,len(links))\n    seen=set()\n    for h,txt in links:\n        txt=re.sub(r'<[^>]+>','',txt); txt=re.sub(r'\\s+',' ',html.unescape(txt)).strip()\n        if h in seen: continue\n        seen.add(h)\n        if f=='home.html':\n            if re.search(r'facebook|instagram|twitter|x\\.com|youtube|linkedin|tiktok|apps\\.apple|play\\.google|weibo|wechat|t\\.me|threads|krisflyer|login|krisshop|kris\\.|scoot',h,re.I) or not 'singaporeair.com' in h and h.startswith('http'):\n                print(h,'|',txt[:60])\n        else:\n            if ('this link' in txt or 'here' in txt.lower() or 'official' in txt.lower() or 'contact' in txt.lower() or 'facebook' in h.lower() or 'scamshield' in h.lower() or 'career' in h.lower() or 'linkedin' in h.lower() or 'mobile app' in txt.lower() or 'Facebook' in txt):\n                print(h,'|',txt[:80])\nEOF", "description": "Extract key links from SIA pages"}

### [tool_result]
===== phishing_adv.html 24
https://www.singaporeair.com/en_UK/sg/careers/ | Careers portal
https://www.linkedin.com/jobs/singapore-airlines-jobs-worldwide/?currentJobId&#61;3245364631&amp;f_C&#61;1887052&amp;original_referer&#61;https%3A%2F%2Fwww.singaporeair.com%2F | LinkedIn.
https://www.scamshield.gov.sg/i-want-protection-from-scams/ | ScamShield website
https://www.singaporeair.com/en_UK/sg/mobile-app/ | mobile app
https://www.singaporeair.com/en_UK/sg/faq/accounts-and-security/two-factor-authentication-2fa/ | here
https://www.singaporeair.com/en_UK/sg/global_footer/security/ | here
https://www.singaporeair.com/en_UK/sg/contact-us/ | official contact channels
===== security.html 23
https://www.facebook.com/singaporeair/posts/10160143647823679 | Facebook page
https://www.singaporeair.com/en_UK/contact-us/ | contact us
https://www.singaporeair.com/feedback-enquiry/ | Contact us
===== home.html 10
/en_UK/sg/ppsclub-krisflyer/ | PPS Club & KrisFlyer

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re,html\nx=open('phishing_adv.html',errors='ignore').read()\nlinks=re.findall(r'<a\\b[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>',x,re.S)\nfor h,txt in links:\n    txt=re.sub(r'<[^>]+>','',txt); txt=re.sub(r'\\s+',' ',html.unescape(txt)).strip()\n    print(h,'|',txt[:60])\nEOF\necho ----; grep -ohE 'https?://[a-zA-Z0-9.-]*(facebook|instagram|twitter|x|youtube|linkedin|tiktok|apple|google|weibo|t|threads|krisflyer|krisshop|kris|flyscoot|tiktok|xiaohongshu)\\.[a-z.]+[^\"'\"'\"' <>]*' home.html security.html phishing_adv.html | sort | uniq -c | sort -rn | head -40; echo; grep -ohE 'https?://[a-zA-Z0-9.-]+' home.html security.html phishing_adv.html | sort | uniq -c | sort -rn | head -40", "description": "List all advisory links and external hosts"}

### [tool_result]
/ | 
/en_UK/sg/plan-travel/ | Plan travel
/en_UK/sg/flying-withus/ | Flying with us
/en_UK/sg/travel-info/ | Travel info
/en_UK/sg/ppsclub-krisflyer/ | PPS Club & KrisFlyer
/en_UK/sg/corporate/ | Corporate
/en_UK/sg/home/ | Home
/en_UK/sg/corporate/ | HighFlyer & Corporate
/en_UK/sg/corporate/newsroom/ | Newsroom
/en_UK/sg/corporate/newsroom/newsalert-listing/ | News alerts
https://www.singaporeair.com/en_UK/contact-us/ | 
https://www.singaporeair.com/en_UK/sg/careers/ | Careers portal
https://www.linkedin.com/jobs/singapore-airlines-jobs-worldwide/?currentJobId&#61;3245364631&amp;f_C&#61;1887052&amp;original_referer&#61;https%3A%2F%2Fwww.singaporeair.com%2F | LinkedIn.
https://www.scamshield.gov.sg/i-want-protection-from-scams/ | ScamShield website
https://www.singaporeair.com/en_UK/sg/faqCategory/?category&#61;17431 | 
https://www.singaporeair.com/get-help/others | 
https://www.singaporeair.com/en_UK/contact-us/ | website
https://www.singaporeair.com/get-help/others | link.
https://www.singaporeair.com/en_UK/contact-us/ | 
https://www.singaporeair.com/en_UK/sg/careers/ | 
https://www.singaporeair.com/en_UK/sg/mobile-app/ | mobile app
https://www.singaporeair.com/en_UK/sg/faq/accounts-and-security/two-factor-authentication-2fa/ | here
https://www.singaporeair.com/en_UK/sg/global_footer/security/ | here
https://www.singaporeair.com/en_UK/sg/contact-us/ | official contact channels
----
      3 https://x.com/SingaporeAir
      3 https://www.instagram.com/singaporeair
      3 https://www.facebook.com/singaporeair
      1 https://www.linkedin.com/jobs/singapore-airlines-jobs-worldwide/?currentJobId&#61;3245364631&amp;f_C&#61;1887052&amp;original_referer&#61;https%3A%2F%2Fwww.singaporeair.com%2F
      1 https://www.facebook.com/singaporeair/posts/10160143647823679
      1 https://banner-management.useinsider.com

    271 https://www.singaporeair.com
     32 https://assets.singaporeair.com
      6 https://www.googletagmanager.com
      5 https://schema.org
      4 https://www.facebook.com
      3 http://www.w3.org
      3 https://x.com
      3 https://www.wikidata.org
      3 https://www.instagram.com
      3 https://s.go-mpulse.net
      3 https://s2.go-mpulse.net
      3 https://en.wikipedia.org
      1 https://www.scamshield.gov.sg
      1 https://www.linkedin.com
      1 https://www.csa.gov.sg
      1 https://ucd-web.api.useinsider.com
      1 https://singaporeairlines.api.useinsider.com
      1 https://banner-management.useinsider.com
      1 https://api.useinsider.com

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && grep -o '.\\{200\\}https://x.com/SingaporeAir.\\{300\\}' home.html | head -2; echo; grep -oiE '(youtube|tiktok|linkedin\\.com/company|apps\\.apple|play\\.google|SingaporeAir app|KrisFlyer app)[^\"<]{0,80}' home.html | sort -u | head", "description": "Inspect social links context in SIA homepage"}

### [tool_result]
om/content/dam/sia/web-assets/icons/singapore_airlines_logo.png","@id":"https://www.singaporeair.com/#airline","url":"https://www.singaporeair.com/","sameAs":["https://www.facebook.com/singaporeair","https://x.com/SingaporeAir","https://www.instagram.com/singaporeair","https://en.wikipedia.org/wiki/Singapore_Airlines","https://www.wikidata.org/wiki/Q32245"]},{"itemListElement":[{"item":{"priceCurrency":"SGD","itemOffered":{"departureAirport":{"iataCode":"SIN","@type":"Airport","name":"Changi"},"provider":{"iataCode":"SQ"

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; for u in https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/ https://www.singaporeair.com/en_UK/sg/mobile-app/ https://www.singaporeair.com/en_UK/sg/contact-us/; do sleep 9; f=$(echo $u | sed 's#.*/\\([^/]*\\)/$#\\1#').html; curl -sL -A \"$UA\" --max-time 30 -o $f -w \"%{http_code} %{url_effective} -> $f\\n\" $u; done; python3 - <<'EOF'\nimport re,html\nx=open('newsalert-listing.html',errors='ignore').read()\nx2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',x)\nt=html.unescape(re.sub(r'\\s+',' ',re.sub(r'(?s)<[^>]+>',' ',x2)))\ni=t.find('News alerts')\nprint(t[i:i+3000])\nprint(len(re.findall(r'newsalert-listing/[a-z0-9-]+/',x)))\nEOF", "description": "Fetch SIA news alerts, mobile app, contact pages"}

### [tool_result]
200 https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/ -> newsalert-listing.html
200 https://www.singaporeair.com/en_UK/sg/mobile-app/ -> mobile-app.html
200 https://www.singaporeair.com/en_UK/sg/contact-us/ -> contact-us.html
News alerts News alerts 16 Nov 2026 Advisory on phishing scams and good cybersecurity practices 16 Nov 2026 Customer Advisory on Delays in Email Responses 30 Oct 2026 Advisory on Singapore Airlines flights affected by the geopolitical situation in the Middle East 6 Apr 2026 Advisory on the carriage of power banks on board SIA flights 5 Dec 2025 Advisory on Singapore Airlines flights affected by Typhoon Ragasa 5 Jan 2024 Advisory on US reservations and KrisFlyer Services hotline 30 Dec 2022 High Volume of Customers at SIA Service Centre at ION Orchard 
7

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re,html\nfor f in ['mobile-app.html','contact-us.html']:\n    x=open(f,errors='ignore').read()\n    links=re.findall(r'<a\\b[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>',x,re.S)\n    print('=====',f)\n    for h,txt in links:\n        if re.search(r'apple|google|huawei|appgallery|facebook|instagram|x\\.com|twitter|youtube|tiktok|linkedin|whatsapp|wa\\.me|t\\.me|telegram|line\\.me|wechat|tel:|mailto:',h,re.I):\n            txt=re.sub(r'<[^>]+>','',txt); txt=re.sub(r'\\s+',' ',html.unescape(txt)).strip()\n            print(h,'|',txt[:60])\n    x2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',x)\n    t=html.unescape(re.sub(r'\\s+',' ',re.sub(r'(?s)<[^>]+>',' ',x2)))\n    for m in re.finditer(r'(\\+65[\\s\\d]{7,12}|1800[\\s\\d]{6,10}|6[0-9]{3}\\s?[0-9]{4})',t):\n        print('PHONE', m.group(0), '::', t[max(0,m.start()-100):m.end()+40])\n    if f=='contact-us.html':\n        i=t.find('Contact us'); print(t[i:i+2500])\n    else:\n        i=t.find('SingaporeAir'); print(t[i:i+600])\nEOF", "description": "Extract apps and hotlines from SIA pages"}

### [tool_result]
===== mobile-app.html
https://apps.apple.com/sg/app/singapore-airlines/id515287841 | 
https://play.google.com/store/apps/details?id=com.amadeus.merci.client.ui&feature=nav_other | 
SingaporeAir mobile App | Singapore Airlines Plan travel Flying with us Travel info PPS Club & KrisFlyer Corporate Help Feedback Singapore · English Log in Sign Up --> Home SingaporeAir mobile app Travel made easy with the SingaporeAir mobile app The SingaporeAir Mobile App Plan, book, and manage your trips effortlessly. Designed for travellers, the SingaporeAir mobile app features handy self-service functions and personalised travel details for greater convenience on your journey. Download the app today Book flights with ease --> Search and book flights operated by Singapore Airlines or partn
===== contact-us.html

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && ls -la contact-us.html; python3 - <<'EOF'\nimport re,html\nx=open('contact-us.html',errors='ignore').read()\nx2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',x)\nt=html.unescape(re.sub(r'\\s+',' ',re.sub(r'(?s)<[^>]+>',' ',x2)))\nprint(len(t)); print(t[:4000])\nEOF\ngrep -oE '(\\+65|65)[ -]?6[0-9]{3}[ -]?[0-9]{4}' contact-us.html | sort | uniq -c", "description": "Inspect SIA contact-us page text"}

### [tool_result]
-rw-rw-r-- 1 ankur ankur 304379 Nov 25 18:16 contact-us.html
207
 Contact Us | Singapore Airlines Plan travel Flying with us Travel info PPS Club & KrisFlyer Corporate Help Feedback Singapore · English Log in Sign Up --> Contact details City / country Show more Show less 
      3 +65 6223 8888
      1 +65 6597 4501

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && grep -oE '.{300}\\+65 6223 8888.{200}' contact-us.html | head -2 | sed 's/\\\\u003c/</g; s/\\\\\"/\"/g' | head -c 1500; echo; echo ----; grep -oE '.{300}\\+65 6597 4501.{100}' contact-us.html | head -1 | sed 's/\\\\u003c/</g' | head -c 800", "description": "Get context of SIA Singapore phone numbers"}

### [tool_result]
howAddress":"no","webUrl":"","childListDesc":"French: Mon \u2013 Fri, 8am \u2013 6pm <br/>English: 24 hours daily","childListTitle":"+33  1 86 47 73 99","contentType":"mobile"},{"isShowAddress":"no","webUrl":"","childListDesc":"KrisFlyer related assistance English: 24 hours daily","childListTitle":"+65 6223 8888","contentType":"mobile"},{"isShowAddress":"no","webUrl":"https://www.singaporeair.com/get-help/others","childListDesc":"","childListTitle":"Write to us","contentType":"chat"},{"isShowAddress":"no","w
ss travel, public relations, and cargo.","additionalData":"","title":"HighFlyer and corporate contacts"}]}}},"SG":{"countryName":"Singapore","cityList":{"SIN":{"cityName":"Singapore","dataList":[{"childDataList":[{"isShowAddress":"no","webUrl":"","childListDesc":"24 hours hotline","childListTitle":"+65 6223 8888","contentType":"mobile"},{"isShowAddress":"no","webUrl":"https://www.singaporeair.com/get-help/others","childListDesc":"","childListTitle":"Write to us","contentType":"chat"},{"isShowAddress":"no","w

----
tDesc":"Local contact<br/>Mon \u2013 Sun, 7.30am \u2013 11.30pm (UTC+8)","childListTitle":"1800-2244243","contentType":"mobile","showAddressLabel":"Show Address"},{"isShowAddress":"no","webUrl":"","childListDesc":"Overseas contact<br/>Mon \u2013 Sun, 7.30am \u2013 11.30pm (UTC+8)","childListTitle":"+65 6597 4501","contentType":"mobile","showAddressLabel":"Show Address"},{"isShowAddress":"yes","webUrl":"","chil

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re\nx=open('contact-us.html',errors='ignore').read()\ni=x.find('1800-2244243')\nseg=x[i-1500:i]\nprint(re.findall(r'\"(?:countryName|cityName|title|childListTitle)\":\"([^\"]*)\"',seg))\ni=x.find('\"SG\":{\"countryName\":\"Singapore\"')\nseg=x[i:i+3000]\nprint(re.findall(r'\"(?:countryName|cityName|title|childListTitle|childListDesc)\":\"([^\"]*)\"',seg))\nEOF", "description": "Identify SIA Singapore contact entries"}

### [tool_result]
['Singapore Airlines Air Cargo', 'HighFlyer and corporate contacts', 'Singapore', 'Singapore', '+65 6223 8888', 'Write to us', 'Service Centre', 'Book an appointment to save time', 'Singapore Airlines contact centre']
['Singapore', 'Singapore', '24 hours hotline', '+65 6223 8888', '', 'Write to us', '2 Orchard Turn<br />\\r\\n#04\\u201305 ION Orchard<br />\\r\\nSingapore 238801 (Above Orchard MRT station)<br />\\r\\n<br />\\r\\n<u>Operating hours<\\/u><br />\\r\\nMon \\u2013 Sat, 9.30am \\u2013 6pm<br />\\r\\nSun, 9.30am \\u2013 5pm<br />\\r\\nClosed on the first day of Chinese New Year ', 'Service Centre', '', 'Book an appointment to save time', 'Singapore Airlines contact centre', 'Local contact<br/>Mon \\u2013 Sun, 7.30am \\u2013 11.30pm (UTC+8)', '1800-2244243', 'Overseas contact<br/>Mon \\u2013 Sun, 7.30am \\u2013 11.30pm (UTC+8)', '+65 6597 4501', 'Level 1, Arrival Hall<br />\\r\\nPassenger Terminal Building 3<br />\\r\\nChangi Airport<br />\\r\\nSingapore 819829\\u2028<br/><br />\\r\\n<u>Operating hours\\u2028<\\/u><br />\\r\\n24 hours daily<br/>\\r\\n', 'Lost & Found Services', 'Lost and found', '', 'View travel agent listing ', 'Travel agent listing', '', 'HighFlyer Business Travel Programme']

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/sia && python3 - <<'EOF'\nimport re,json\nx=open('contact-us.html',errors='ignore').read()\ni=x.find('\"SG\":{\"countryName\":\"Singapore\"')\ndec=json.JSONDecoder()\n# find start of the value\nj=x.find('{',i+4)\nobj,end=dec.raw_decode(x[j:])\nfor city in obj['cityList'].values():\n    for d in city['dataList']:\n        print('TITLE:',d.get('title'))\n        for c in d.get('childDataList',[]):\n            print('   ',c.get('childListTitle'),'|',re.sub('<[^>]+>',' ',c.get('childListDesc',''))[:80])\nEOF", "description": "Parse SIA Singapore contact JSON blob"}

### [tool_result]
TITLE: Singapore Airlines contact centre
    +65 6223 8888 | 24 hours hotline
    Write to us | 
    Service Centre | 2 Orchard Turn 
#04–05 ION Orchard 
Singapore 238801 (Above Orchard MRT statio
    Book an appointment to save time | 
TITLE: Lost and found
    1800-2244243 | Local contact Mon – Sun, 7.30am – 11.30pm (UTC+8)
    +65 6597 4501 | Overseas contact Mon – Sun, 7.30am – 11.30pm (UTC+8)
    Lost & Found Services | Level 1, Arrival Hall 
Passenger Terminal Building 3 
Changi Airport 
Singapo
TITLE: Travel agent listing
    View travel agent listing  | 
TITLE: HighFlyer and corporate contacts
    HighFlyer Business Travel Programme | 
    Public relations: public_affairs@singaporeair.com.sg | 
    Singapore Airlines Air Cargo |

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)