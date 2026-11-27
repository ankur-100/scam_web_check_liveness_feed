# Recovered transcript digest: private_B_other_banks (agent ae4bc76bdc8b4c8a9)

### [user]
You are sub-agent B of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_B_banks_other.json
Scratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B/

YOUR ENTITIES
Tier 1 (deep): for each find security/fraud hub, latest scam alerts (dated list?), official SMS sender IDs, anti-scam/fraud hotline, official apps, official domains/login hosts, social accounts.
1. Citibank Singapore (citibank.com.sg)
2. HSBC Singapore (hsbc.com.sg)
3. Standard Chartered Singapore (SG pages under sc.com/sg -> entity_id "sc.com"; check whether any separate SG registrable domains are used)
4. Maybank Singapore (verify the primary SG domain: maybank2u.com.sg and/or maybank.com.sg)
5. Trust Bank Singapore (verify domain, e.g. trustbank.sg)
6. GXS Bank (verify, e.g. gxs.com.sg)
7. MariBank Singapore (verify domain)
Tier 2 (quick, at most 3, pick ones with SG security/scam pages): CIMB Singapore (cimb.com.sg), Bank of China Singapore, ICBC Singapore, RHB Singapore, HL Bank, YouTrip, Atome.

Cross-check bank hotlines against ScamShield's page https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ (gov page; may be added to evidence as corroboration; each bank's own page must be primary evidence).

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

### [user]
<system-reminder>
Your final report is delivered through SubagentHandback: when your work is complete, call SubagentHandback({message: <your full report>}) and then stop. Only a SubagentHandback call reaches your caller as your result; plain text you write at the end is not delivered.
</system-reminder>

### [assistant text]
I'll start by reading the brief as instructed.

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
{"command": "cat /home/ankur/scamtrends_feed/registry/FORMAT.md; echo ----; ls -la /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/", "description": "Read the registry format spec and list work folder"}

### [tool_use Bash]
{"command": "wc -l /home/ankur/scamtrends_feed/sources/03_community_commercial.md; grep -n -i -E 'citi|hsbc|standard chartered|sc\\.com|maybank|trust bank|trustbank|gxs|maribank|mari bank|cimb|bank of china|icbc|rhb|hl bank|hlbank|youtrip|atome|scamshield|anti-scam hotline' /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -100", "description": "Search earlier survey for my entities"}

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
146 /home/ankur/scamtrends_feed/sources/03_community_commercial.md
3:Captured 2026-11-25. Scope excludes SG government sources (SPF/ICAAS, MAS, ScamShield, ScamAlert/NCPC, CSA) and global phishing feeds. Those are covered elsewhere.
39:- HuggingFace (API search for `singapore`/`scam`/`smishing`/`scamshield`): the "ScamShield"-named datasets are Indian/generic and unrelated to SG ScamShield.
95:  - Net: these sites are not a defensible scam-phone source. ScamShield (government) is the authoritative SG source for numbers.
98:- **Singtel**: the "List of official Singtel web domains" says all `*.singtel.com` domains are official and adds ≈45 partner domains. Examples: `singtelcrm.com`, `singteltvgo.com`, `portal.singtelge.com`, `gomo.sg`, `heya.sg`, `dash.com.sg`, `gxs.com.sg`, `e-station2.axs.com.sg`, `singtelcares.syd1.qualtrics.com`. Machine-extractable from the page's JSON component.
142:1. Keep the SPF ICAAS feed as the primary SG domain source. Add the other agent's government feeds (ScamShield, MAS IAL, ScamAlert).

### [tool_use Bash]
{"command": "sed -n 80,146p /home/ankur/scamtrends_feed/sources/03_community_commercial.md; echo ----; cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py", "description": "Read survey bank section and validator"}

### [tool_result]
### 3. Group-IB (commercial threat intel)
- Immediate Era (2025-10-21): Google-Ads malvertising using deepfakes of SG officials, Convertri-hosted redirectors and IP-geofenced cloaking to SG. Group-IB says 3,808 SG clicks and 685 redirected in a month. It counts **52 intermediary + 119 fake-news domains**, but publishes only the example `razudai.com` (in a gated URL with gclid parameters). The rest is "available to Group-IB customers in the Threat Intelligence portal".
- Delivery scams: SingPost impersonation infrastructure of 107 sites (85 SingPost look-alikes, registered 2020-12-25 → 2021-03-01), plus Groups 2/3 (80+ sites). No list.
- Resecurity (2024-06-26, Singpass identity theft) has **zero IOCs** (verified). Cyfirma's SG items are APT-flavoured press coverage, with no public IOC appendix found.

### 4–8. Phone-number lookup sites
- Sample records as displayed:
  - callchecker: `65473046 — 7 reports`, `31050283 — 4 reports`; recent rows `Scam | 21 Jul 2026 | "Investment Scammer"`.
  - numbers.online: `+6572149849 — 40 reports, 1 source, risk Low, 2d ago`; a run of `+656250xxxx` numbers with 1–3 reports each.
  - whoseno: `65976392 — 10 reports — Critical activity 99/100`, `31391311 — 9 reports — 90/100`.
  - spamcalls: `+6564224930 — 7 requests`.
- Caveats:
  - Many listed numbers are likely legitimate businesses or telemarketers. +65 6xxx blocks dominate, and "reports" ≠ "scam".
  - callchecker has visible abuse (personal-vendetta comments).
  - numbers.online **ToS explicitly bans scraping, bulk extraction and building a competing database**. Its free API key is per-number lookup only.
  - Net: these sites are not a defensible scam-phone source. ScamShield (government) is the authoritative SG source for numbers.

### 9. Corporate allowlists (negative set)
- **Singtel**: the "List of official Singtel web domains" says all `*.singtel.com` domains are official and adds ≈45 partner domains. Examples: `singtelcrm.com`, `singteltvgo.com`, `portal.singtelge.com`, `gomo.sg`, `heya.sg`, `dash.com.sg`, `gxs.com.sg`, `e-station2.axs.com.sg`, `singtelcares.syd1.qualtrics.com`. Machine-extractable from the page's JSON component.
- **SingPost** (page dated 2022-02-28): official = `singpost.com`. It gives look-alike examples **not** to trust: `www.singpost.com.xyz.com`, `www.singpost.net`, `www.singpost.org`. Sender-ID variants `SGPOST`/`SINGPOST`.
- **Carousell** (via search result; the page itself returned 403): only `carousell.com`/`carousell.sg` are genuine. Examples of fakes: `carousellpay.com`, `carousell-pay.com`, `carousell.pay-sg.com`, `carousell.xxx.com`.
- **Shopee** `[Scam Advisory]` help-centre series (articles 76743, 76788, 76790, 76811, 125081, 166953, 204789): official email only `@shopee.com`. **No IOCs and no dates** in the articles.
- Use: whitelist these, and use the look-alike patterns as typosquat-detector test cases.

### 10. Bank pages
- DBS sample: `SMS Phishing Alert — Date: 28 August 2026 — "Scammers use phishing SMSes messages urging you to resolve unauthorised PayNow transactions. These phishing SMSes ask you to call a phone number in the SMS."` (the number is not given).
- Another DBS sample: `Token Activation Phishing Alert — 16 March 2026 (Updated 15 August 2026)`.
- DBS also has a "Scams & Frauds Alert Archives" page.
- OCBC: the "Be A Pro Against Cons" editions are narrative only. The only numbers present are OCBC's own hotlines.
- UOB: links out to scamalert.sg and `go.uob.com/reportscam`.
- All three: **no fake domains or scam numbers**. They are useful only as a timeline of MOs that banks flagged (dates + titles) and as allowlists (`dbs.com.sg`, `ocbc.com`, `internet.ocbc.com`, `uob.com.sg`, `uobgroup.com`).

### 11–12. scam.sg and RecordOwl (SG commercial directories)
- scam.sg is a reputation and SEO platform over ACRA data. It says itself that "a lower score does not mean a business is a scam". Its T&C prohibits republishing, reproducing and redistributing content. Not an IOC source.
- RecordOwl `/scam-sg` mostly mirrors the MAS Investor Alert List and stops at 2025-02-12. Its three "editorial" entries include a named private individual with a mobile number. Avoid it.
  - Sample: `MAS Investor Alert List | 12 Feb 2025 | Bitsafew`.
  - Sample: `RecordOwl Editorial | 11 Aug 2026 | url.sg / SG61Vouchers Phishing — Fake SG61 Government Voucher Site`.

### 14. Commercial and gated (worth a procurement conversation, not scraping)
- **Whoscall ASI (Gogolook)**: API and data feeds for number and domain verification, plus SDK and white-label. Claims 2.6B numbers/domains and 7M+ scam sites, sourced from "government partners, organizations, and real-time reports". It is the engine behind StarHub ScamSafe. Pricing by application only.
- **ScamAdviser**: Trust-Score API and data feed. RapidAPI tiers: Basic free (20 req/mo), Pro $39/mo (10k), Ultra $199 (100k), Mega $499 (300k). The site is Cloudflare-challenged, so I could not read its ToS. ScamAdviser co-produces the GASA reports.
- **GASA State of Scams in Singapore 2024** (with Feedzai, published 2025-02-25): the full report is **members-only** and survey-based. The 2025 SEA report is also gated. The PDF links seen in search now return 404.
- **Global Signal Exchange** (GASA + Google + Oxford Information Labs): membership-based signal sharing. GovTech and SPF joined, so SG scam-site signals flow there, but access is restricted.
- **Trend Micro ScamCheck / Scam Radar** (SG launch 2025-08-26): in-app only, with no public list. Its SG press releases are survey statistics.
- **Ensign InfoSec**: its "fraud awareness" page covers only scams impersonating Ensign itself. Its patented phishing-domain detection is not public.

---

## Licence and terms caveats (read before ingesting anything)
- **CC BY 4.0, clean:** IMC'25 smishing dataset only. Attribute Agarwal, Papasavva, Suarez-Tangil & Vasek (IMC '25).
- **No licence, so all rights reserved:**
  - zeyalt scamalert.sg scrape: fine for internal research. Do **not** redistr

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [assistant text]
Setting up a fetch helper and pulling homepages + robots.txt for all Tier-1 banks (one host at a time, ≥1 s apart).

### [tool_use Bash]
{"command": "B=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\nmkdir -p $B\ncat > $B/f.sh <<'EOF'\n#!/bin/bash\n# usage: f.sh URL OUTFILE   -> prints \"code effective_url size\"\nUA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\nr=$(curl -sL -A \"$UA\" -H \"Accept-Language: en-SG,en;q=0.9\" --compressed --max-time 30 -o \"$2\" -w '%{http_code} %{url_effective}' \"$1\")\necho \"$r $(stat -c %s \"$2\" 2>/dev/null) <- $1\"\necho \"$(date -Is) $r <- $1\" >> $(dirname \"$2\")/fetchlog.txt\nEOF\nchmod +x $B/f.sh\ncd $B\n# fetch per host sequentially, hosts in parallel\n( ./f.sh https://www.citibank.com.sg/robots.txt citi_robots.txt; sleep 1.5; ./f.sh https://www.citibank.com.sg/ citi_home.html ) > o1.txt 2>&1 &\n( ./f.sh https://www.hsbc.com.sg/robots.txt hsbc_robots.txt; sleep 1.5; ./f.sh https://www.hsbc.com.sg/ hsbc_home.html ) > o2.txt 2>&1 &\n( ./f.sh https://www.sc.com/robots.txt sc_robots.txt; sleep 1.5; ./f.sh https://www.sc.com/sg/ sc_home.html ) > o3.txt 2>&1 &\n( ./f.sh https://www.maybank2u.com.sg/robots.txt mbb2u_robots.txt; sleep 1.5; ./f.sh https://www.maybank2u.com.sg/ mbb2u_home.html ) > o4.txt 2>&1 &\n( ./f.sh https://www.maybank.com.sg/ mbbsg_home.html ) > o4b.txt 2>&1 &\n( ./f.sh https://trustbank.sg/robots.txt trust_robots.txt; sleep 1.5; ./f.sh https://trustbank.sg/ trust_home.html ) > o5.txt 2>&1 &\n( ./f.sh https://www.gxs.com.sg/robots.txt gxs_robots.txt; sleep 1.5; ./f.sh https://www.gxs.com.sg/ gxs_home.html ) > o6.txt 2>&1 &\n( ./f.sh https://www.maribank.sg/robots.txt mari_robots.txt; sleep 1.5; ./f.sh https://www.maribank.sg/ mari_home.html ) > o7.txt 2>&1 &\n( ./f.sh https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ scamshield_bankhotline.html ) > o8.txt 2>&1 &\nwait\ncat o1.txt o2.txt o3.txt o4.txt o4b.txt o5.txt o6.txt o7.txt o8.txt", "description": "Fetch homepages and robots.txt for Tier-1 banks", "timeout": 120000}

### [tool_result]
[1]   Done                    ( ./f.sh https://www.citibank.com.sg/robots.txt citi_robots.txt; sleep 1.5; ./f.sh https://www.citibank.com.sg/ citi_home.html ) > o1.txt 2>&1
[5]   Done                    ( ./f.sh https://www.maybank.com.sg/ mbbsg_home.html ) > o4b.txt 2>&1
[6]   Done                    ( ./f.sh https://trustbank.sg/robots.txt trust_robots.txt; sleep 1.5; ./f.sh https://trustbank.sg/ trust_home.html ) > o5.txt 2>&1
[7]   Done                    ( ./f.sh https://www.gxs.com.sg/robots.txt gxs_robots.txt; sleep 1.5; ./f.sh https://www.gxs.com.sg/ gxs_home.html ) > o6.txt 2>&1
[8]-  Done                    ( ./f.sh https://www.maribank.sg/robots.txt mari_robots.txt; sleep 1.5; ./f.sh https://www.maribank.sg/ mari_home.html ) > o7.txt 2>&1
[9]+  Done                    ( ./f.sh https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ scamshield_bankhotline.html ) > o8.txt 2>&1
[2]   Done                    ( ./f.sh https://www.hsbc.com.sg/robots.txt hsbc_robots.txt; sleep 1.5; ./f.sh https://www.hsbc.com.sg/ hsbc_home.html ) > o2.txt 2>&1
[4]+  Done                    ( ./f.sh https://www.maybank2u.com.sg/robots.txt mbb2u_robots.txt; sleep 1.5; ./f.sh https://www.maybank2u.com.sg/ mbb2u_home.html ) > o4.txt 2>&1
[3]+  Done                    ( ./f.sh https://www.sc.com/robots.txt sc_robots.txt; sleep 1.5; ./f.sh https://www.sc.com/sg/ sc_home.html ) > o3.txt 2>&1
200 https://www.citibank.com.sg/robots.txt 1540 <- https://www.citibank.com.sg/robots.txt
200 https://www.citibank.com.sg/ 298402 <- https://www.citibank.com.sg/
200 https://www.hsbc.com.sg/robots.txt 822 <- https://www.hsbc.com.sg/robots.txt
200 https://www.hsbc.com.sg/ 209050 <- https://www.hsbc.com.sg/
200 https://www.sc.com/robots.txt 2106 <- https://www.sc.com/robots.txt
200 https://www.sc.com/sg/ 487055 <- https://www.sc.com/sg/
404 https://www.maybank2u.com.sg/robots.txt 293 <- https://www.maybank2u.com.sg/robots.txt
200 https://www.maybank2u.com.sg/ 394 <- https://www.maybank2u.com.sg/
200 https://www.maybank2u.com.sg/ 394 <- https://www.maybank.com.sg/
200 https://trustbank.sg/robots.txt 116 <- https://trustbank.sg/robots.txt
200 https://trustbank.sg/ 81918 <- https://trustbank.sg/
200 https://www.gxs.com.sg/robots.txt 43 <- https://www.gxs.com.sg/robots.txt
200 https://www.gxs.com.sg/ 126047 <- https://www.gxs.com.sg/
200 https://www.maribank.sg/robots.txt 22 <- https://www.maribank.sg/robots.txt
200 https://www.maribank.sg/ 130470 <- https://www.maribank.sg/
200 https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ 412055 <- https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\nfor f in citi_robots.txt hsbc_robots.txt sc_robots.txt trust_robots.txt gxs_robots.txt mari_robots.txt; do echo \"=== $f\"; cat $f; echo; done\necho \"=== mbb2u_home\"; cat mbb2u_home.html; echo; echo \"=== mbb2u robots\"; cat mbb2u_robots.txt", "description": "Show robots.txt files and Maybank homepage"}

### [tool_result]
=== citi_robots.txt
User-agent: *
Disallow: /GlobalMobile/NPSSurvey/SGGCB/index.htm
Disallow: https://www.citibank.com.sg/citigoldcircle/referral.htm
Disallow: https://www.citibank.com.sg/citigoldcircle/referee.htm
Disallow: https://www.citibank.com.sg/landing_page/member-get-member/ctpmgm1a/index.htm
Disallow: https://www.citibank.com.sg/landing_page/member-get-member/ctpmgm1b/index.htm
Disallow: https://www.citibank.com.sg/gcb/landing_page/member-get-member/index.htm
Disallow: https://www.citibank.com.sg/gcb/landing_page/friend/member-get-member/index.htm
Disallow: https://www.citibank.com.sg/wealth-management/referral-program/
Disallow: https://www.citibank.com.sg/wealth-management/citigold/privilges-and-offers/citigold-referral-program/
Disallow: https://www.citibank.com.sg/gcb/landing_page/member-get-member/index.htm
Disallow: https://www.citibank.com.sg/citigoldcircle
Disallow: https://www.citibank.com.sg/ctpmgm1a
Disallow: https://www.citibank.com.sg/ctpmgm1b
Disallow: https://www.citibank.com.sg/rbmgm
Disallow: https://www.citibank.com.sg/mgmatm
Disallow: https://www.citibank.com.sg/loans/mortgage/manage-mortgage
Disallow: https://www.citibank.com.sg/loans/mortgage/referral-program/
Disallow: https://www.citibank.com.sg/gcb/mortgages/homerefer.htm
Disallow: https://www.citibank.com.sg/loans/mortgage/citi-home-loan-contact-us
Disallow: https://www.citibank.com.sg/commercialbank/static/promo_mgm.htm


Sitemap: https://www.citibank.com.sg/sitemap-index.xml
Sitemap: https://www.citibank.com.sg/sitemap.xml

=== hsbc_robots.txt
User-agent: *
Disallow: /*?code=
Disallow: /*?WABFormEntryCommand=
Disallow: /1/*
Disallow: /*?demologin=
Disallow: /content/dam/hsbc/hk/docs/*
Disallow: /messages/
Disallow: /*ep_testing
Disallow: /*ep_login
Disallow: /ep_docs/*.pdf
Disallow: /ep_internal/*.pdf
Disallow: /*hsbc-token-testing*
Disallow: /cms-dashboard*
Disallow: /cms-admin*
Disallow: /content/dam/hsbc/ar/promos*
Disallow: /content/dam/hsbc/gr/promos*
Disallow: /content/dam/hsbc/ca/promos*
Disallow: /content/dam/hsbc/om/promos*
Disallow: /content/dam/hsbc/am/promos*
Disallow: /branch-login/*
Disallow: /staff-emergency-comms/*.html
Disallow: /remote-access-instructions/*.html
Disallow: /remote-access/logon
Disallow: /remote-access/*.html
Disallow: /cgi-bin
Disallow: /*.pdf$

sitemap: https://www.hsbc.com.sg/sitemaps.xml
=== sc_robots.txt
User-agent: *
Disallow: /_document/
Disallow: /_documents/
Disallow: /_footers/
Disallow: /_images/
Disallow: /_redirect/
Disallow: /_scripts/
Disallow: /_ssi/
Disallow: /_themes/
Disallow: /_tools/
Disallow: /*/_document/
Disallow: /*/_documents/
Disallow: /*/_footers/
Disallow: /*/_images/
Disallow: /*/_redirect/
Disallow: /*/_scripts/
Disallow: /*/_ssi/
Disallow: /*/_themes/
Disallow: /*/_tools/
Disallow: /*/edm/
Disallow: /*/employee-banking/*
Disallow: /*/interact/
Disallow: /*/interact/*
Disallow: /ch/
Disallow: /ng/investment/*
Disallow: /*?step=
Disallow: /*?productName=
Disallow: /*?pid=
Disallow: /cn/investment/funds/*


Sitemap: https://www.sc.com/ae/sitemap.xml
Sitemap: https://www.sc.com/bw/sitemap.xml
Sitemap: https://www.sc.com/bd/sitemap.xml
Sitemap: https://www.sc.com/bn/sitemap.xml
Sitemap: https://www.sc.com/bh/sitemap.xml
Sitemap: https://www.sc.com/ci/sitemap.xml
Sitemap: https://www.sc.com/cn/en/sitemap.xml
Sitemap: https://www.sc.com/cn/sitemap.xml
Sitemap: https://www.sc.com/fk/sitemap.xml
Sitemap: https://www.sc.com/gm/sitemap.xml
Sitemap: https://www.sc.com/gh/sitemap.xml
Sitemap: https://www.sc.com/hk/sitemap.xml
Sitemap: https://www.sc.com/hk/zh/sitemap.xml
Sitemap: https://www.sc.com/id/sitemap.xml
Sitemap: https://www.sc.com/in/sitemap.xml
Sitemap: https://www.sc.com/je/sitemap.xml
Sitemap: https://www.sc.com/jo/sitemap.xml
Sitemap: https://www.sc.com/ke/sitemap.xml
Sitemap: https://www.sc.com/lk/sitemap.xml
Sitemap: https://www.sc.com/mx/sitemap.xml
Sitemap: https://www.sc.com/my/sitemap.xml
Sitemap: https://www.sc.com/ng/sitemap.xml
Sitemap: https://www.sc.com/np/sitemap.xml
Sitemap: https://www.sc.com/pe/sitemap.xml
Sitemap: https://www.sc.com/pk/sitemap.xml
Sitemap: https://www.sc.com/sg/sitemap.xml
Sitemap: https://www.sc.com/sl/sitemap.xml
Sitemap: https://www.sc.com/tz/sitemap.xml
Sitemap: https://www.sc.com/tw/sitemap.xml
Sitemap: https://www.sc.com/ug/sitemap.xml
Sitemap: https://www.sc.com/vn/sitemap.xml
Sitemap: https://www.sc.com/zm/sitemap.xml
Sitemap: https://www.sc.com/zw/sitemap.xml
Sitemap: https://www.sc.com/en/sitemap.xml
=== trust_robots.txt
# *
User-agent: *
Allow: /

# Host
Host: https://trustbank.sg

# Sitemaps
Sitemap: https://trustbank.sg/sitemap.xml

=== gxs_robots.txt
Sitemap: https://www.gxs.com.sg/sitemap.xml
=== mari_robots.txt
User-agent: *
Allow: /
=== mbb2u_home
<html>
<head>
<title>Welcome to Maybank Singapore</title>
<meta name="description" content="Maybank Singapore"> 
<meta name="keywords" content="maybank2u.com.sg, Maybank Singapore">
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<meta http-equiv="refresh" content="0;url=https://www.maybank2u.com.sg/en/personal/index.page" />
</head>
<body>
</body>
</html>

=== mbb2u robots
<HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html;charset=ISO-8859-1"><TITLE>Not Found</TITLE></HEAD>
<H1>Not Found</H1> The requested object does not exist on this server. The link you followed is either outdated, inaccurate, or the server has been instructed not to let you have it.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\n( ./f.sh https://www.citibank.com.sg/sitemap-index.xml citi_smi.xml; sleep 1.5; ./f.sh https://www.citibank.com.sg/sitemap.xml citi_sm.xml ) > p1.txt 2>&1 &\n( ./f.sh https://www.hsbc.com.sg/sitemaps.xml hsbc_sm.xml ) > p2.txt 2>&1 &\n( ./f.sh https://www.sc.com/sg/sitemap.xml sc_sm.xml ) > p3.txt 2>&1 &\n( ./f.sh https://www.maybank2u.com.sg/en/personal/index.page mbb_home.html; sleep 1.5; ./f.sh https://www.maybank2u.com.sg/sitemap.xml mbb_sm.xml ) > p4.txt 2>&1 &\n( ./f.sh https://trustbank.sg/sitemap.xml trust_sm.xml ) > p5.txt 2>&1 &\n( ./f.sh https://www.gxs.com.sg/sitemap.xml gxs_sm.xml ) > p6.txt 2>&1 &\n( ./f.sh https://www.maribank.sg/sitemap.xml mari_sm.xml ) > p7.txt 2>&1 &\nwait 2>/dev/null\ncat p1.txt p2.txt p3.txt p4.txt p5.txt p6.txt p7.txt\nfor f in citi_smi.xml citi_sm.xml hsbc_sm.xml sc_sm.xml mbb_sm.xml trust_sm.xml gxs_sm.xml mari_sm.xml; do echo \"== $f: $(head -c 300 $f | tr '\\n' ' ')\"; done", "description": "Fetch sitemaps for Tier-1 banks", "timeout": 120000}

### [tool_result]
200 https://www.citibank.com.sg/sitemap-index.xml 364 <- https://www.citibank.com.sg/sitemap-index.xml
200 https://www.citibank.com.sg/sitemap.xml 72229 <- https://www.citibank.com.sg/sitemap.xml
200 https://www.hsbc.com.sg/sitemaps.xml 189 <- https://www.hsbc.com.sg/sitemaps.xml
200 https://www.sc.com/sg/sitemap.xml 25389 <- https://www.sc.com/sg/sitemap.xml
200 https://www.maybank2u.com.sg/en/personal/index.page 53594 <- https://www.maybank2u.com.sg/en/personal/index.page
404 https://www.maybank2u.com.sg/sitemap.xml 293 <- https://www.maybank2u.com.sg/sitemap.xml
200 https://trustbank.sg/sitemap.xml 27641 <- https://trustbank.sg/sitemap.xml
200 https://www.gxs.com.sg/sitemap.xml 33936 <- https://www.gxs.com.sg/sitemap.xml
200 https://www.maribank.sg/sitemap.xml 140171 <- https://www.maribank.sg/sitemap.xml
== citi_smi.xml: <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> <sitemap> <loc> https://www.citibank.com.sg/sitemap.xml </loc> <lastmod>2018-04-25</lastmod> </sitemap> <sitemap> <loc> https://www.citibank.com.sg/sitemap-href.xml </lo
== citi_sm.xml: <?xml version="1.0" encoding="utf-8"?><!--Generated by Screaming Frog SEO Spider 24.3--> <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">   <url>     <loc>https://www.citibank.com.sg/about-us/awards</loc>     <lastmod>2026-10-23</lastmod>     <changefreq>monthly</changefreq>     <p
== hsbc_sm.xml: <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">     <sitemap>                     <loc>https://www.hsbc.com.sg/sitemaps-pages.xml</loc>     </sitemap> </sitemapindex>
== sc_sm.xml: <?xml version="1.0" encoding="UTF-8"?><!-- sitemap-generator-url="http://www.arnebrachhold.de" sitemap-generator-version="4.0.8" --> <!-- generated-on="25 Nov 2026 10:10 am" --> <sitemapindex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/si
== mbb_sm.xml: <HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html;charset=ISO-8859-1"><TITLE>Not Found</TITLE></HEAD> <H1>Not Found</H1> The requested object does not exist on this server. The link you followed is either outdated, inaccurate, or the server has been instructed not to let you have it.  
== trust_sm.xml: <?xml version="1.0" encoding="UTF-8"?> <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0" xmlns:image="http://www.google.com
== gxs_sm.xml: <?xml version="1.0" encoding="UTF-8"?> <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">     <url>         <loc>https://www.gxs.com.sg</loc>         <lastmod>2026-11-24T09:03:40.392Z</lastmod>     </url>     <url>         <loc>https://www.
== mari_sm.xml: <?xml version="1.0" encoding="UTF-8"?> <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> <url><loc>https://www.maribank.sg/</loc><lastmod>2026-11-25</lastmod><changefreq>weekly</changefreq></url> <url><loc>https://www.maribank.sg/product/mari-savings-account</loc><lastmod>2026-11-25</last

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\nPAT='scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect'\necho \"== citi_smi\"; cat citi_smi.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//'\necho \"== citi_sm\"; grep -o '<loc>[^<]*</loc>' citi_sm.xml | sed 's/<[^>]*>//g' | grep -iE \"$PAT\"\necho \"== sc_sm (index)\"; grep -o '<loc>[^<]*</loc>' sc_sm.xml | sed 's/<[^>]*>//g' | head -40\necho \"== trust_sm\"; grep -o '<loc>[^<]*</loc>' trust_sm.xml | sed 's/<[^>]*>//g' | grep -iE \"$PAT\"\necho \"== gxs_sm\"; grep -o '<loc>[^<]*</loc>' gxs_sm.xml | sed 's/<[^>]*>//g' | grep -iE \"$PAT\"\necho \"== mari_sm\"; grep -o '<loc>[^<]*</loc>' mari_sm.xml | sed 's/<[^>]*>//g' | grep -iE \"$PAT\"; echo \"mari total: $(grep -c '<loc>' mari_sm.xml)\"", "description": "Grep sitemaps for scam/security URLs"}

### [tool_result]
== citi_smi


== citi_sm
https://www.citibank.com.sg/citigold/wealth-solutions/protect-your-family-income
https://www.citibank.com.sg/digital-banking/secured-banking/enhanced-security
https://www.citibank.com.sg/digital-banking/secured-banking/money-lock
https://www.citibank.com.sg/gcb/ready_credit/rc_card_security.htm
https://www.citibank.com.sg/insurance/insurance-solutions/protection-plan
https://www.citibank.com.sg/investments/investment-products/fixed-income-securities
https://www1.citibank.com.sg/life-and-money/protect
https://www1.citibank.com.sg/insurance/articles/future/investing-101-wealth-creation-protection
https://www1.citibank.com.sg/insurance/articles/future/bridging-the-protection-gap-at-different-stages-of-life
https://www1.citibank.com.sg/digital-banking/secured-banking
https://www1.citibank.com.sg/digital-banking/secured-banking/
https://www1.citibank.com.sg/credit-cards/manage-your-card/card-security
https://www.citibank.com.sg/wealth-management/wealth-insights/why-is-asset-and-wealth-protection-important
https://www.citibank.com.sg/wealth-management/wealth-insights/ways-to-achieve-financial-security
https://www.citibank.com.sg/wealth-management/wealth-insights/financial-fraud-how-to-stay-safe-from-scams
https://www.citibank.com.sg/static1/static/prevention-protection/
https://www.citibank.com.sg/static1/static/atm-security/
https://www.citibank.com.sg/personal-banking/online-services/secure-banking/online-security-tips/
== sc_sm (index)
https://www.sc.com/sg/sitemap-misc.xml
https://www.sc.com/sg/sitemap-pt-page-2017-02.xml
https://www.sc.com/sg/sitemap-market-outlook-2026-11.xml
https://www.sc.com/sg/sitemap-pt-page-2021-01.xml
https://www.sc.com/sg/sitemap-pt-page-2026-01.xml
https://www.sc.com/sg/sitemap-market-outlook-2024-09.xml
https://www.sc.com/sg/sitemap-pt-page-2017-05.xml
https://www.sc.com/sg/sitemap-pt-page-2016-12.xml
https://www.sc.com/sg/sitemap-pt-page-2026-11.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-11.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-03.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-02.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-04.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-05.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-06.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-07.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-08.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-09.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-10.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-11.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2025-12.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-01.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-02.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-03.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-04.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-05.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-06.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-07.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-08.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-09.xml
https://www.sc.com/sg/sitemap-pt-gcf-article-2026-10.xml
https://www.sc.com/sg/sitemap-market-outlook-2026-10.xml
https://www.sc.com/sg/sitemap-pt-page-2026-10.xml
https://www.sc.com/sg/sitemap-market-outlook-2026-09.xml
https://www.sc.com/sg/sitemap-pt-page-2026-09.xml
https://www.sc.com/sg/sitemap-pt-page-2024-12.xml
https://www.sc.com/sg/sitemap-pt-page-2021-11.xml
https://www.sc.com/sg/sitemap-pt-page-2023-01.xml
https://www.sc.com/sg/sitemap-pt-page-2019-08.xml
https://www.sc.com/sg/sitemap-pt-page-2023-03.xml
== trust_sm
https://trustbank.sg/security/
https://trustbank.sg/faqs/security/
== gxs_sm
https://www.gxs.com.sg/security
https://www.gxs.com.sg/news-press/gxs-bank-customers-have-an-additional-protection-against-scams-with-the-launch-of-money-lock
== mari_sm
https://www.maribank.sg/security/use-your-credit-card-safely
https://www.maribank.sg/security/scam-advisories-investment-scams
https://www.maribank.sg/security/scam-advisories-gois
https://www.maribank.sg/security/scam-advisories-job-scams
https://www.maribank.sg/security/identifying-and-reporting-scams
https://www.maribank.sg/security/freeze-account-activities
https://www.maribank.sg/security/detecting-impersonation-scam
https://www.maribank.sg/security/scam-advisories-business-email-compromise-scams
https://www.maribank.sg/security/security-best-practices
https://www.maribank.sg/security
https://www.maribank.sg/security/detecting-card-transaction-scam
https://www.maribank.sg/info/latest-security-alerts
https://www.maribank.sg/info/latest-security-alerts/detecting-and-responding-to-deepfake-scams
https://www.maribank.sg/info/latest-security-alerts/latest-malware-and-scam-tactics
https://www.maribank.sg/info/latest-security-alerts/anti-malware-security-features
https://www.maribank.sg/info/latest-security-alerts/dangers-of-downloading-applications-from-third-party-or-dubious-sites
https://www.maribank.sg/info/latest-security-alerts/beware-sms-phishing-scams-involving-singpass
https://www.maribank.sg/info/latest-security-alerts/unauthorised-card-transactions-made-using-contactless-payment-methods-in-singapore
https://www.maribank.sg/info/latest-security-alerts/scams-revolving-around-digital-manipulation
https://www.maribank.sg/info/e-payment-user-protection-guidelines
https://www.maribank.sg/help-centre/article/10028-how-can-i-manage-my-notifications-and-alerts-preferences
https://www.maribank.sg/help-centre/article/10040-i-forgot-my-secure-pin-what-should-i-do
https://www.maribank.sg/help-centre/article/10042-how-do-i-change-my-secure-pin
https://www.maribank.sg/help-centre/article/10180-what-are-anti-malware-security-features
https://www.maribank.sg/help-centre/article/10182-what-are-official-android-app-stores
https://www.maribank.sg/help-centre/article/10853-how-are-my-deposits-being-protected
https://www.maribank.sg/help-centre/article/10047-can-

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 - <<'EOF'\nimport re\nh=open('citi_home.html',encoding='utf-8',errors='replace').read()\nlinks=set(re.findall(r'href=[\"\\']([^\"\\']+)[\"\\']',h))\nfrom urllib.parse import urlparse\nhosts={}\nfor l in links:\n    if l.startswith('http'):\n        hosts.setdefault(urlparse(l).netloc,[]).append(l)\nfor k in sorted(hosts): print(k, len(hosts[k]), hosts[k][:2] if 'citi' not in k else '')\nprint('---- security-ish links')\nfor l in sorted(links):\n    if re.search(r'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect|contact',l,re.I): print(l)\nprint('---- text snippets')\nt=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S)\nt=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'\\s+',' ',t)\nfor m in re.finditer(r'(scam|fraud|hotline|1800|\\+65 ?6\\d{3}|6225 ?5225)',t,re.I):\n    print('..',t[max(0,m.start()-120):m.end()+120])\nEOF", "description": "Extract hosts and security links from Citi homepage"}

### [tool_result]
 1 ['https://']
itunes.apple.com 1 ['https://itunes.apple.com/sg/app/citibank-sg/id370773317?mt=8']
jobs.citi.com 1 
play.google.com 1 ['https://play.google.com/store/apps/details?id=com.citibank.mobile.sg&hl=en']
www.citibank.com.sg 97 
www.citiworldprivileges.com 1 
www.facebook.com 1 ['https://www.facebook.com/citisingapore']
www.findmyciti.com 1 
www.forrester.com 1 ['https://www.forrester.com/about-us/objectivity/']
www.instagram.com 1 ['https://www.instagram.com/citisingapore']
www.ipb.citibank.com.sg 2 
www.sdic.org.sg 2 ['https://www.sdic.org.sg/', 'https://www.sdic.org.sg/?icid&#61;SGHOAR9ENHOMECALK']
www.youtube.com 1 ['https://www.youtube.com/CitiSG']
www1.citibank.com.sg 17 
---- security-ish links
https://www.citibank.com.sg/static/contact?lid=SGENCBGGNFOTLContactUs
https://www.citibank.com.sg/static1/static/prevention-protection/?lid=SGENCBLCIFOTLCreditCardAndFraud
https://www1.citibank.com.sg/digital-banking/secured-banking/?lid=SGENCBGGNFOTLSECURITYTIPS
---- text snippets
.. s targeted advertising. Confirm Terms and Conditions Privacy Disclaimers Notices Security Security Tips Credit Card and Fraud Banking Information Fees &amp; Rates (For Singapore Clients)" data-ctaposition="undefined" data-destinationurl="https:/

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\n( ./f.sh https://www1.citibank.com.sg/digital-banking/secured-banking/ citi_secured.html; sleep 1.5; ./f.sh https://www1.citibank.com.sg/credit-cards/manage-your-card/card-security citi_cardsec.html ) > q1.txt 2>&1 &\n( ./f.sh https://www.citibank.com.sg/static1/static/prevention-protection/ citi_prevprot.html; sleep 1.5\n  ./f.sh https://www.citibank.com.sg/static/contact citi_contact.html; sleep 1.5\n  ./f.sh https://www.citibank.com.sg/wealth-management/wealth-insights/financial-fraud-how-to-stay-safe-from-scams citi_fraudart.html; sleep 1.5\n  ./f.sh https://www.citibank.com.sg/personal-banking/online-services/secure-banking/online-security-tips/ citi_sectips.html; sleep 1.5\n  ./f.sh https://www.citibank.com.sg/digital-banking/secured-banking/enhanced-security citi_enhsec.html ) > q2.txt 2>&1 &\nwait 2>/dev/null; cat q1.txt q2.txt", "description": "Fetch Citibank SG security candidate pages", "timeout": 180000}

### [tool_result]
000 https://www1.citibank.com.sg/digital-banking/secured-banking/  <- https://www1.citibank.com.sg/digital-banking/secured-banking/
200 https://www1.citibank.com.sg/credit-cards/manage-your-card/card-security 396689 <- https://www1.citibank.com.sg/credit-cards/manage-your-card/card-security
200 https://www.citibank.com.sg/static1/static/prevention-protection/ 12513 <- https://www.citibank.com.sg/static1/static/prevention-protection/
200 https://www.citibank.com.sg/static/contact 207212 <- https://www.citibank.com.sg/static/contact
200 https://www.citibank.com.sg/wealth-management/wealth-insights/financial-fraud-how-to-stay-safe-from-scams 205632 <- https://www.citibank.com.sg/wealth-management/wealth-insights/financial-fraud-how-to-stay-safe-from-scams
200 https://www.citibank.com.sg/personal-banking/online-services/secure-banking/online-security-tips/ 364564 <- https://www.citibank.com.sg/personal-banking/online-services/secure-banking/online-security-tips/
200 https://www.citibank.com.sg/digital-banking/secured-banking/enhanced-security 261709 <- https://www.citibank.com.sg/digital-banking/secured-banking/enhanced-security

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\ncat > tx.py <<'EOF'\nimport re,sys,html\ndef text(fn):\n    h=open(fn,encoding='utf-8',errors='replace').read()\n    h=re.sub(r'(?is)<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>','',h)\n    h=re.sub(r'(?i)<br\\s*/?>|</p>|</li>|</h\\d>|</div>|</tr>','\\n',h)\n    t=re.sub(r'<[^>]+>',' ',h); t=html.unescape(t)\n    t=re.sub(r'[ \\t\\r\\f\\v]+',' ',t); t=re.sub(r'\\n\\s*\\n+','\\n',t)\n    return t\nif __name__=='__main__':\n    fn=sys.argv[1]; t=text(fn)\n    if len(sys.argv)>2:\n        pat=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 150\n        seen=set()\n        for m in re.finditer(pat,t,re.I):\n            s=t[max(0,m.start()-w):m.end()+w].replace('\\n',' | ')\n            k=s[:80]\n            if k in seen: continue\n            seen.add(k); print('..',s)\n    else:\n        print(t)\nEOF\necho \"=== prevention-protection\"; python3 tx.py citi_prevprot.html | head -120", "description": "Create text extractor and read Citi prevention page"}

### [tool_result]
=== prevention-protection
 
 Credit Card Fraud Prevention Tips – Citibank Singapore 
 Credit Card FRAUD PREVENTION & PROTECTION
 Home 
 |
 Fraud: Prevention & Protection
 Protect yourself against fraud: Tips and measures.
 Citi takes the prevention of fraud very seriously with measures in place for your protection and security. Card activation ensures that you have consented for your new or replaced cards to be activated for usage, Citi Alerts notifies you of transactions that are made to your accounts while 3D Secure authenticates all purchases made online to prevent fraudulent misuse of your account.
 Fraud prevention is a shared responsibility and you can further prevent and protect yourself against fraud:
 Keep your card safe. 
 Citibank 24-hour card emergency number: +65 6225 5225.
 Sign on your credit card as soon as you receive it.
 Ensure your card is always kept safely with you.
 Check your account balance regularly.
 Ensure that the correct card is returned to you after any purchase.
 Do not disclose your card or financial details or lend your ATM/Credit card to anyone (including strangers, suspicious websites and telemarketers).
 Do not write down your PIN or choose a PIN that is easily associated with you e.g. your birth date.
 Travel and shop safely. 
 Be wary of strangers and pick pockets.
 Ensure that merchants are reputable.
 Update your contact details (mobile number and email address) to ensure that you are kept informed of your account activities.
 Online safety. 
 Install the latest antivirus and anti malware software version on your mobile phone or computer.
 Do not save your online banking login details on your browsers, clearing your browser's cache and history after each session.
 Do not open email attachments, install software or run programs from unknown sources.
 Protect your card from double swiping. 
 The magnetic stripe on your credit or debit card contains sensitive payment card data. 
 To protect your information, the magnetic stripe of your credit or debit card should not be swiped on Point-of-Sale readers or Electronic Cash Registers which is known as “double swiping”.
 Inserting or dipping a chip-enabled credit or debit card in a payment card terminal for payment is not considered as double swiping. 
 For more information on double swiping, please visit -->
 http://www.abs.org.sg/docs/library/abs_faq_double_swiping.pdf -->

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\necho \"=== online-security-tips (len $(python3 tx.py citi_sectips.html | wc -c))\"; python3 tx.py citi_sectips.html | grep -v '^\\s*$' | awk 'length>2' | sed -n 1,400p | grep -iE -A2 'scam|fraud|alert|phish|sms|sender|official|hotline|1800|6225|beware|impersonat|malware|20[12][0-9]' | head -150", "description": "Read Citi online security tips page highlights"}

### [tool_result]
=== online-security-tips (len 79778)
 As the first step to protect your accounts, we’ll educate you on the different types of fraud
 that exist – from discovering how to spot
 and stop fraud, to the additional preventive steps that you can take.
 Always remember to check that the citibank.com.sg website has a valid certificate marked Citigroup
 Inc. [US] and a padlock
--
 Security Alert
 How You Can
 Protect Yourself
--
 Latest Security Alert 
 Security Alerts and Information
 Customers of Citibank Singapore Limited are advised to check this page regularly for the latest security alerts and/or
 news. If you are unsure whether any call, email or SMS is genuinely from Citibank, please contact us immediately and
 refrain from taking any further action. Whilst Citibank strives to provide you with the latest security alerts and/or news,
 please note that this webpage and the examples of scams/phishing listed here are not exhaustive. For latest news on
 scams/phishing, please refer to www.scamalert.sg which is a website owned and operated by the National Crime
 Prevention Council of Singapore.
 Introducing new security updates on your Citi Mobile ® App
 Date: 15 September 2023
 With the increase and prevalence of malware scams, scammers are employing increasingly sophisticated tactics to deceive users into installing malicious apps (malware) on their devices. Once a malicious app is installed, scammers can remotely access your device and steal sensitive information, including personal data and banking credentials to perform fraudulent monetary transactions.
 WHAT CITI IS DOING FOR YOU
 As part of our ongoing efforts to provide you with a safe and secure banking environment, we have introduced a new security update on the Citi Mobile ® App.
--
HOW TO PROTECT YOURSELVES FROM MALWARE?
 1) Be Vigilant — Stay Safe and Not Sorry: If the price of an offer is too good to be true, it probably is. Be vigilant and verify the legitimacy of the offer with the company via official sources. Consult your family, friends, or colleagues if you are unsure.
 2) Avoid Installing Unknown Apps: Refrain from downloading apps from third-party websites and only download from official app stores like Apple AppStore and Google Play Store. Malicious apps may request for permissions, such as “Accessibility Services”, that are unrelated to their intended functionalities. Review app permissions carefully during installation and reject any suspicious requests.
 3) Be Wary of Unusual Payment Requests: Be cautious if the offers require you to use unconventional payment methods, such as gift cards or cryptocurrency. These methods are often favoured by scammers because they are difficult to trace and reverse.
4) Share with Care: Always verify the legitimacy of the offer before sharing with your family, friends, and colleagues. If in doubt, avoid sharing it or enlist their assistance in helping you verify the legitimacy.
WHAT TO DO IF YOU FALL VICTIM TO A MALWARE SCAM?
1) Switch your Device to Flight Mode: If you suspect your device has been infected by malware, switch your device to the flight mode immediately to disconnect from the Internet. This will prevent the scammers from further accessing your device remotely.
2) Activate Kill Switch immediately: On a secondary/uncompromised device, login to the Citi Mobile ® App > Settings & More > Activate Kill Switch. Alternatively you can login to Citibank Online or call Citiphone +65 6225 5225 to activate Kill Switch. Click here for more information on activating Kill Switch.
3) Identified Unauthorised Transactions: If there are any unauthorised transactions detected in your bank account(s), contact Citiphone immediately at +65 6225 5225.
4) Report the incident to the police: Reach out to the police and lodge a report.
 5) Run an anti-virus scan on your device: Use an anti-virus software which you have downloaded from verified or legitimate sources to scan and remove any malware detected in your device to ensure that known malware in your device is identified and removed.
 Keep your cards safe when travelling abroad
 Date: 13 June 2022
 Thinking about travelling abroad any time soon? With the announcement of the simpler Vaccinated Travel Framework,
 Singaporeans will now be able to travel abroad easily. If you are planning to travel abroad, please be reminded to stay
 vigilant during your travels and to keep your credit and debit cards safe to avoid any fraud or theft.
 Follow these tips while travelling abroad:
 Do not leave your handbags/wallets and cards
--
 Beware of strangers and always check that your
 wallets/cards are in your possession.
 Be aware of common scams at your travel destination (e.g.
 elaborate begging or street vendor scams, taxi scams).
 Ensure that the correct card is returned to you after
 any purchase.
 Be alert at crowded places (e.g. trains, markets, shopping
 centres, airports etc.). Be wary of where you keep your
 wallet and watch out for people who bump into you, as
--
 please call our CitiPhone hotline available on the Citibank website.
 For Debit Cards:
 Deactivate your debit card by reporting it as lost and blocking your card(s)
--
 you immediately in the case of fraudulent activity. Do note that if you change your SIM
 card whilst overseas, Citibank will not be able to contact you.
 To update your contact details, you may log in to the Citi Mobile ® App and navigate to
--
 Enable your Citialerts to stay updated on your transactions
 Ensure that your Citialerts are enabled via Citibank Online so that you can be notified on
 any transactions on your card(s) and account(s). You will be notified on online outgoing
 funds transfer from your banking accounts which is S$1 and above.
 Note: If you have opted to receive SMS for your Citi Alerts, please ensure that you do not
 swop out your SIM card with the phone number registered with Citi.
 If you detect any unauthorised transactions on your card(s) and account(s), please report
 it to us by calling our Citi

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 tx.py citi_sectips.html > citi_sectips.txt\necho \"--- dated items\"; grep -n -iE '^\\s*Date' citi_sectips.txt | head -60\necho \"--- titles before dates\"; grep -n -B1 -iE '^\\s*Date:' citi_sectips.txt | grep -v -iE 'Date:' | head -60\necho \"--- channel facts\"; python3 tx.py citi_sectips.html '(sender id|sms from|short ?code|72484|CITI\\b|official website|official app|whatsapp|never (ask|send)|clickable link|hotline)' 160 | head -40", "description": "Extract dated alerts and channel facts from Citi security page"}

### [tool_result]
--- dated items
45: Date: 15 September 2023
69: Date: 13 June 2022
134: Date: 05 MAY 2022
220: Date: 04 May 2022
313: Date: 04 May 2022
407: Date: 1 December 2021
434: Date: 3 September 2021
471: Date: 11 June 2021
518: Date: 24 May 2021
595: Date: 10 February 2021
659: Date: 19th October 2020
674: Date: 18th September 2020
782: Date: 24 th July 2020
915: Date: 24 th April 2019
944: Date: 14 th April 2019
959: Date: 5 th September 2018
986: Date: 7 th August 2018
1013: Date: 20 th July 2018
1030: Date: 20 th May 2018
--- titles before dates
44- Introducing new security updates on your Citi Mobile ® App
--
68- Keep your cards safe when travelling abroad
--
133- Be Wary of Impersonation Scams
--
219- Be Wary of Job Scams
--
312- spoofed Citibank Hotlines
--
406- Protect Yourself Against Vishing Scams
--
433- Beware of Phishing Scams
--
470- Beware of Calls from Spoof Citibank Hotlines & Fake SMSes with Spoof Citibank Headers
--
517- Social Media Impersonation Scam
--
594- Protect yourself from e-Wallet scams
--
658- Loan Scam
--
673- Social Media and E-Commerce Scams
--
781- Impersonation and Technical Support Scam
--
914- Customer Advisory – 3 rd Party Mobile Applications / Websites
--
943- Citi Email Addresses
--
958- Customer Advisory
--
985- Phishing Emails
--
1012- Customer Advisory
--
1029- SMS Phishing
--- channel facts
.. ices  |  | |  Online Services |  | |  Security Centre |  Welcome to the Security Centre. |  Your security is our priority. |  Learn how we protect your banking experience at Citi, and how you can protect yourself against |  identity theft and other security |  risks at the same time. |  As the first step to protect your accounts, we’ll educat
.. b address bar when you access Citibank Online. |  Online Security Tips |  Latest |  Security Alert |  How You Can |  Protect Yourself |  Your Role |  and Responsibility |  How Citi Protects |  You |  Contact Us  |  Latest Security Alert  |  Security Alerts and Information |  Customers of Citibank Singapore Limited are advised to check this page reg
.. fer to www.scamalert.sg which is a website owned and operated by the National Crime |  Prevention Council of Singapore. |  Introducing new security updates on your Citi Mobile ® App |  Date: 15 September 2023 |  With the increase and prevalence of malware scams, scammers are employing increasingly sophisticated tactics to deceive 
.. remotely access your device and steal sensitive information, including personal data and banking credentials to perform fraudulent monetary transactions. |  WHAT CITI IS DOING FOR YOU |  As part of our ongoing efforts to provide you with a safe and secure banking environment, we have introduced a new security update on the Cit
.. ITI IS DOING FOR YOU |  As part of our ongoing efforts to provide you with a safe and secure banking environment, we have introduced a new security update on the Citi Mobile ® App. |  To protect your online banking data, we have enhanced the Citi Mobile ® App to restrict your access in the event we detect any apps/tools with r
.. e and secure banking environment, we have introduced a new security update on the Citi Mobile ® App. |  To protect your online banking data, we have enhanced the Citi Mobile ® App to restrict your access in the event we detect any apps/tools with risky permission settings attempting to gain access to the Citi Mobile® App on 
.. ve enhanced the Citi Mobile ® App to restrict your access in the event we detect any apps/tools with risky permission settings attempting to gain access to the Citi Mobile® App on your device. |  In order for you to continue accessing the Citi Mobile ® App, you are required to disable any risky permission settings (for e.g. 
.. ect any apps/tools with risky permission settings attempting to gain access to the Citi Mobile® App on your device. |  In order for you to continue accessing the Citi Mobile ® App, you are required to disable any risky permission settings (for e.g. stop screen sharing/broadcasting/control) on the other app/tool. |  Once such r
.. settings (for e.g. stop screen sharing/broadcasting/control) on the other app/tool. |  Once such risky permission settings have been disabled, your access to the Citi Mobile ® App will no longer be restricted and you may proceed with usage of the Citi Mobile® App. |  We will be detecting the following 4 potential risky permiss
.. Once such risky permission settings have been disabled, your access to the Citi Mobile ® App will no longer be restricted and you may proceed with usage of the Citi Mobile® App. |  We will be detecting the following 4 potential risky permission settings on apps/tools attempting to access the Citi Mobile ® App on your device:
.. ay proceed with usage of the Citi Mobile® App. |  We will be detecting the following 4 potential risky permission settings on apps/tools attempting to access the Citi Mobile ® App on your device: |  1) Anti Remote Desktop Access |  2) Suspicious Accessibility Services |  3) Android Debugging via Developer Options |  4) Screen Overla
.. ly, friends, or colleagues if you are unsure. |  2) Avoid Installing Unknown Apps: Refrain from downloading apps from third-party websites and only download from official app stores like Apple AppStore and Google Play Store. Malicious apps may request for permissions, such as “Accessibility Services”, that are unrelated to their int
.. s will prevent the scammers from further accessing your device remotely. | 2) Activate Kill Switch immediately: On a secondary/uncompromised device, login to the Citi Mobile ® App > Settings & More > Activate Kill Switch. Alternatively you can login to Citibank Online or call Citiphone +65 6225 5225 to activate Kill Switch. 
.. ring your travels. |  What to do if your credit or debit card was stolen or lost overseas? |  For Credit Cards: |  Step 1 : Lock your credit card immediately via the Citi Mobile ® App so no one else |  can use it. |  To lock your card, click on “Manage” on your card on the Citi Mobile ® 

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\nsed -n 910,1075p citi_sectips.txt | awk 'length>2' | cut -c1-300", "description": "Read older Citi alert items incl. Citi email addresses"}

### [tool_result]
 caller is genuine.
 Do not give out any personal and banking information
 (i.e. User ID, password or OTP) to anyone.
 Treat them like your ATM PIN. 
 Customer Advisory – 3 rd Party Mobile Applications / Websites
 Date: 24 th April 2019
 Description: Do not use 3 rd Party Mobile Applications /
 Websites for viewing Online Banking Details
 We are aware that there are 3 rd Party Mobile Applications / Websites that
 allow customers to have a consolidated view of their financial expenses /
 transactions across multiple banks, credit card, investments, equity trades, and
 loan accounts in one place.
 Citibank would like to remind our customers not to download any 3 rd Party
 Mobile Applications / Websites to view / access your Citibank Online accounts. There
 is a potential risk of your online banking credentials being compromised as Username
 and Password has been shared with the application.
 To protect yourself, always exercise the following precautions:
 Do not download any 3 rd Party Mobile Applications to view your online
 banking details.
 Do not input your Citibank Online Username and Password when requested by such
 applications / websites.
 If already inputted, immediately change Username and Password. 
 Use of Citibank Online is personal to you and no third party should be allowed to
 access/view your account/account information via Citibank Online, whether or not you
 have consented to such third party’s access. This is to prevent any unauthorized
 access or use of your account and account information. You are responsible for
 keeping any of your log-in credentials (including User ID and Password) confidential
 and you cannot reveal your log-in credentials to any third party.
 Where you have revealed your log-in credentials to a third party, please note that
 Citibank is not liable for and you have to compensate us for any losses arising out
 of any use of your log-in credentials. In such an event, we also have the right,
 from a risk management perspective, to suspend your access to Citibank Online at any
 time.
 Citi Email Addresses
 Date: 14 th April 2019
 Description: Please note that we will send you email notifications
 from the following Citibank email addresses.
 Email Addresses 
 alerts@citibank.com.sg 
 statements@citibank.com.sg 
 advices@citibank.com.sg 
 welcome@citibank.com.sg 
 marketing@citibank.com.sg 
 services@citibank.com.sg 
 chargeback@citibank.com.sg 
 customerservice@citibank.com.sg 
 client@experience.citi.com 
 customerservice@thankyou.citi.com 
 Customer Advisory
 Date: 5 th September 2018
 Description: Be alert to emails and SMS scams.
 We would like to remind our customers to remain vigilant when responding to emails
 and SMS messages from senders masquerading as popular brands, often requesting for
 you to:
 Complete a survey or a quiz, with the promise of cash prizes, loyalty points or
 air miles.
 Provide your card number, in order to participate in the survey or quiz.
 Provide your mobile phone number.
 As a further tactic to convince victims of the authenticity of these scams, a
 One-Time Pin (OTP) will be sent to the mobile phone number that you've just
 provided. Unfortunately, with the successful solicitation of this information, the
 scammer would have gathered the necessary details to perform unauthorized
 transactions on your Citi Cards.
 To protect yourself, always exercise the following precautions:
 When clicking on a link from an email, always check that the internet address
 that you are directed to is legitimate by verifying it in the web browser. If
 you're unsure, please check this with the brand or merchant.
 Never disclose your card numbers on merchant websites that have internet
 addresses that look incorrect.
 Check if the web browser displays a Locked Padlock icon. Reputable sites would
 have these.
 Never disclose your OTP to websites that you might be unfamiliar with.
 Always check your account statements regularly to detect any unauthorized
 transactions. For a real-time view of your transactions, login to the Citi
 Mobile® App.
 Phishing Emails
 Date: 7 th August 2018
 Description: We have detected phishing emails and webpages targeting
 Citi customers. These phishing emails comes from a non-Citi email address and
 requests Citi customers click on a hyperlink to unlock / update their online banking
 / credit card account.
 If a customer falls victim to the phishing email and clicks on the hyperlink, they
 will be redirected to a page URL that is not official Citi website, requesting for a
 user's information (Username and Password), followed by a request to provide an SMS
 OTP. Such websites are used to conduct card not present transactions but may also be
 utilized in order to steal personally identifiable data, username-password
 combinations, OTPs or infect a user's device as well as fraudulent enrollment of
 Citi © Mobile Token (which may be used to carry out payments to these
 fraudsters).
 How can you protect yourself from this?
 Be alert. Minimize clicking on links in emails as these may not
 be legitimate.
 Check that you are using the official Citi website. Always type
 the Citibank Online website URL directly into the address bar of your browser.
 If you are on mobile, consider using the official 
 Citibank Mobile
 application
 Citi will never request for your PIN, password or OTP through phone
 call, email or SMS.
 Call Citiphone immediately if
 you notice unknown transactions appearing on your account.
 Customer Advisory
 Date: 20 th July 2018
 Description: SingHealth has reported a data breach affecting more
 than 1.5 million SingHealth patients. Patient data stolen included personally
 identifiable information such as names, addresses, birthdays, and NRIC numbers.
 Approximately 160,000 patients had details of medical prescriptions stolen. Stolen
 credentials may be used to conduct social engineering and phishing scams. Such scams
 utilize personally identifiable information to appear legitimate.
 How can you p

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 tx.py scamshield_bankhotline.html > ss.txt; wc -l ss.txt\ngrep -n -iE 'hotline|bank|citi|hsbc|standard|maybank|trust|gxs|mari|cimb|china|icbc|rhb|hl |hong leong|1800|\\+65|6[0-9]{3} ?[0-9]{4}|updated|last' ss.txt | head -120", "description": "Parse ScamShield bank anti-scam hotline page"}

### [tool_result]
62 ss.txt
1: Bank's Anti-Scam Hotline | ScamShield Website 
4: Government agencies communicate via .gov.sg websites (e.g. go.gov.sg/open).  Trusted websites (opens in new tab) 
16: Bank's Anti-Scam Hotline 
17: Bank's Anti-Scam Hotline
18: Act fast and call your bank immediately if you have lost money or shared bank details with a scammer.
19: Last updated on 20 May 2026
21: List of Bank's Anti-Scam Hotline 
23: List of Bank's Anti-Scam Hotline
24: DBS / POSB Dial 1800 339 6963 (from Singapore) or +65 6339 6963 (from overseas)
25: OCBC Dial 6363 3333 
27: UOB Dial 6255 0160 
28: Citibank Dial 6337 5519 
29: CIMB Dial 6333 7777 
30: HSBC Dial 1800 472 2669 (from Singapore) or +65 6472 2669 (from overseas)
31: Maybank Dial 1800 629 2265 (from Singapore) or +65 6533 5229 (from overseas)
32: Standard Chartered Dial 6747 7000 
33: For banks not listed here, please contact your respective bank's fraud hotline for assistance.
38: Citibank (opens in new tab) 
39: CIMB (opens in new tab) 
40: HSBC (opens in new tab) 
41: Maybank (opens in new tab) 
42: Standard Chartered (opens in new tab) 
48: © 2026 Government of Singapore, last updated on 23 November 2026
57: © 2026 Government of Singapore, last updated on 23 November 2026

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 - <<'EOF'\nimport re,html\nh=open('scamshield_bankhotline.html',encoding='utf-8',errors='replace').read()\nfor m in re.finditer(r'<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>',h,re.S):\n    txt=re.sub(r'<[^>]+>','',m.group(2)).strip()\n    if re.search(r'citi|cimb|hsbc|maybank|standard|dbs|ocbc|uob',txt,re.I) or re.search(r'citi|cimb|hsbc|maybank|sc\\.com|dbs|ocbc|uob',m.group(1),re.I):\n        print(html.unescape(txt)[:40],'->',html.unescape(m.group(1)))\nEOF", "description": "Extract bank links from ScamShield hotline page"}

### [tool_result]
DBS/POSB (opens in new tab) -> https://www.dbs.com.sg/personal/support/guide-security-on-scams-and-fraud.html
OCBC (opens in new tab) -> https://www.ocbc.com/personal-banking/security/secure-banking-ways/phishing-scams.page
UOB (opens in new tab) -> https://www.uobgroup.com/uobgroup/contact-us/index.page
Citibank (opens in new tab) -> https://www.citibank.com.sg/static/contact/
CIMB (opens in new tab) -> https://www.cimb.com.sg/en/personal/help-support/contact-us.html
HSBC (opens in new tab) -> https://www.hsbc.com.sg/help/security-centre/fraud-guide/
Maybank (opens in new tab) -> https://www.maybank2u.com.sg/en/personal/eservices/security-alerts/online-threats/measures-to-protect-you-from-scams.page
Standard Chartered (opens in new tab) -> https://www.sc.com/sg/fraud-scam/help/

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 tx.py citi_contact.html '(6337 ?5519|6225 ?5225|scam|fraud|hotline|1800|whatsapp|sms)' 160 | head -30", "description": "Find hotlines on Citi contact page"}

### [tool_result]
..   |  Get Help Anytime with Citibank Hotline & Banking tips | Citibank Singapore  |  IPB Singapore Online  |  Citibank Online  |  Sign On |  Wealth​ Management  |  Citigold  |  Citigold Private Client  |  Accredited In
.. edit  |  X  |  Search  |  Self-Service Banking Tips |  Quick Help |  Email Us |  Visit Us |  Others |  To share with us your concerns or complaints, you may call our CitiPhone Hotline (65) 6225-5225 or (65) 6224-5757 (for International Personal Bank Clients), from Mondays to Fridays, between 8a.m. to 8p.m.  |  Fraud |  FAQs |  Citi Mobile® App  |  M
.. ou may call our CitiPhone Hotline (65) 6225-5225 or (65) 6224-5757 (for International Personal Bank Clients), from Mondays to Fridays, between 8a.m. to 8p.m.  |  Fraud |  FAQs |  Citi Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotl
.. al Bank Clients), from Mondays to Fridays, between 8a.m. to 8p.m.  |  Fraud |  FAQs |  Citi Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for Interna
.. lients), from Mondays to Fridays, between 8a.m. to 8p.m.  |  Fraud |  FAQs |  Citi Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International P
.. m.  |  Fraud |  FAQs |  Citi Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients)  |    What should you do?  |  Scenari
.. raud |  FAQs |  Citi Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If 
.. ti Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If you receive an S
.. Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If you receive an SMS from Citibank (Sender n
..  |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If you receive an SMS from Citibank (Sender number: 72484) to
.. 9 OR |  (2) CitiPhone hotline: (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If you receive an SMS from Citibank (Sender number: 72484) to authorise a charge on your card/account. Reply 1 | if the charge was authorised by you. Reply 2 if the charge was not aut
.. a charge on your card/account. Reply 1 | if the charge was authorised by you. Reply 2 if the charge was not authorised by you. | You may also call Citibank at (65) 6337 5519  |  Scenario 2: | If you receive any suspicious communications claiming to be from Citibank Step 1: | Please do not click on any links provided or provide any person
.. n any links provided or provide any personal and banking information to anyone over unsolicited calls or on a suspicious website. | Step 2: | Contact the CitiPhone hotline at (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients) to report on the alleged scam or to verify if the communications are legitimate. 
.. ided or provide any personal and banking information to anyone over unsolicited calls or on a suspicious website. | Step 2: | Contact the CitiPhone hotline at (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients) to report on the alleged scam or to verify if the communications are legitimate.  |  Scenario 3: | If y
.. uspicious website. | Step 2: | Contact the CitiPhone hotline at (65) 6225 5225 or (65) 6224-5757 (for International Personal Bank Clients) to report on the alleged scam or to verify if the communications are legitimate.  |  Scenario 3: | If you suspect or detect that your account is being compromised. Step 1: | If you suspect that y
.. via the Citi Mobile ® App so that no one else can use it. | To lock your card, click “Manage” on your card on the Citi Mobile ® App. | Step 2: | Contact the Citibank Fraud hotline at (65) 6337 5519 to report on the scam accident and provide the relevant details to our fraud agents: |  • Approximate date and time of the alleged scam
.. e Citi Mobile ® App so that no one else can use it. | To lock your card, click “Manage” on your card on the Citi Mobile ® App. | Step 2: | Contact the Citibank Fraud hotline at (65) 6337 5519 to report on the scam accident and provide the relevant details to our fraud agents: |  • Approximate date and time of the alleged scam or frau
..  use it. | To lock your card, click “Manage” on your card on the Citi Mobile ® App. | Step 2: | Contact the Citibank Fraud hotline at (65) 6337 5519 to report on the scam accident and provide the relevant details to our fraud agents: |  • Approximate date and ti

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 - <<'EOF'\nimport re,html\nfrom urllib.parse import urlparse\nhosts={}\nfor fn in ['citi_home.html','citi_contact.html','citi_sectips.html','citi_enhsec.html','citi_fraudart.html','citi_cardsec.html']:\n    h=open(fn,encoding='utf-8',errors='replace').read()\n    for l in re.findall(r'(?:href|src|action)=[\"\\'](https?://[^\"\\']+)[\"\\']',h):\n        n=urlparse(html.unescape(l)).netloc.lower()\n        hosts.setdefault(n,set()).add(html.unescape(l)[:150])\nfor k in sorted(hosts):\n    if any(x in k for x in ['citi','facebook','instagram','youtube','linkedin','twitter','x.com','tiktok','apple','google','telegram','whatsapp']):\n        print(k, len(hosts[k]), sorted(hosts[k])[:3])\nEOF\necho ---; python3 tx.py citi_contact.html '(sender|whatsapp|message us|72484|chat)' 120 | head -8", "description": "Collect Citi official hosts, apps, socials, sender IDs"}

### [tool_result]
apps.apple.com 2 ['https://apps.apple.com/sg/app/citibank-ipb-sg/id463403661', 'https://apps.apple.com/sg/app/citibank-sg/id370773317']
itunes.apple.com 1 ['https://itunes.apple.com/sg/app/citibank-sg/id370773317?mt=8']
jobs.citi.com 2 ['https://jobs.citi.com/', 'https://jobs.citi.com/?lid=SGENCBLCIFOTLCareers']
marketingportal.citibank.com 14 ['https://marketingportal.citibank.com/msa/assets/sggcb/vendor/js/xfs.js', 'https://marketingportal.citibank.com/msa/assets/sggcb/vendor/js/xss.js', 'https://marketingportal.citibank.com/msa/assets/styles/uiux.theme-base-en.css']
play.google.com 1 ['https://play.google.com/store/apps/details?id=com.citibank.mobile.sg&hl=en']
www.cdn.citibank.com 29 ['https://www.cdn.citibank.com/v1/sggcb/cbol/files/012-dollar-bill.png?_=cfcd2084', 'https://www.cdn.citibank.com/v1/sggcb/cbol/files/037-home-Home.png?_=cfcd2084', 'https://www.cdn.citibank.com/v1/sggcb/cbol/files/055-mobile.png?_=cfcd2084']
www.citibank.com.sg 151 ['https://www.citibank.com.sg', 'https://www.citibank.com.sg/', 'https://www.citibank.com.sg/?icid=SGHOU23ENBHHELG']
www.citibank.com.sglid=sgencblsecatlcitibankbonst 1 ['https://www.citibank.com.sglid=SGENCBLSECATLCitibankbONST']
www.citiworldprivileges.com 1 ['https://www.citiworldprivileges.com/?lid=SGENCGGCGMITLCitiWorldPrivileges']
www.facebook.com 1 ['https://www.facebook.com/citisingapore']
www.findmyciti.com 2 ['https://www.findmyciti.com/sg', 'https://www.findmyciti.com/sg/?lid=SGENCBLCIFOTLFindMyCiti']
www.instagram.com 1 ['https://www.instagram.com/citisingapore']
www.ipb.citibank.com.sg 5 ['https://www.ipb.citibank.com.sg/SGIPB/JSO/signon/DisplayUsernameSignon.do', 'https://www.ipb.citibank.com.sg/SGIPB/JSO/username/signon/flow.action', 'https://www.ipb.citibank.com.sg/en/guide/contact-update-details/index.html']
www.youtube.com 1 ['https://www.youtube.com/CitiSG']
www1.citibank.com.sg 27 ['https://www1.citibank.com.sg/akam/13/21ce33ed', 'https://www1.citibank.com.sg/akam/13/pixel_21ce33ed?a=dD00MTc2Mjg3MzQwM2I3ZDNlMDQ4ZTA5ZGNjNjk0ZmEzYjdmNzNkZGZlJmpzPW9mZg==', 'https://www1.citibank.com.sg/credit-cards']
---
.. , from Mondays to Fridays, between 8a.m. to 8p.m.  |  Fraud |  FAQs |  Citi Mobile® App  |  Methods of Authentication |  Call us |  Message us |  To report a fraud or scam, please contact us immediately at: |  (1) Citibank Fraud hotline: (65) 6337 5519 OR |  (2) CitiP
.. 57 (for International Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If you receive an SMS from Citibank (Sender number: 72484) to authorise a charge on your card/account. Reply 1 | if the charge was authorised by you. Reply 2 if the 
.. tional Personal Bank Clients)  |    What should you do?  |  Scenario 1: | If you receive an SMS from Citibank (Sender number: 72484) to authorise a charge on your card/account. Reply 1 | if the charge was authorised by you. Reply 2 if the charge was not
.. 5 0010 9am to 5.30pm  |  Collections (Mortgages | & Auto Loan) (65) 6395 0014 9am to 5.30pm  |  Using Mass Messaging and live chat  |  Enjoy faster service and personalized assistance by messaging us on the Citi Mobile ®  App. Learn more  here . |  Get i
.. on the Citi Mobile ®  App. Learn more  here . |  Get in touch with your client advisor in the Citi Mobile ®  App via live chat. |  To share with us your concerns or complaints, you may reach us by sending a Secured Message. |  Secured Message Send us

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B\npython3 - <<'EOF'\nimport re\ns=open('citi_sm.xml').read()\nfor m in re.finditer(r'<url>(.*?)</url>',s,re.S):\n    u=m.group(1)\n    if re.search(r'online-security-tips|static/contact|enhanced-security|financial-fraud|money-lock|prevention-protection',u):\n        print(re.sub(r'\\s+',' ',re.sub(r'<[^>]+>',' ',u)).strip())\nh=open('citi_home.html',encoding='utf-8',errors='replace').read()\nprint(set(re.findall(r'https?://[a-z0-9.]*citibank\\.com\\.sg/[A-Za-z]*/?JSO[^\"\\']{0,60}',h)))\nprint(set(re.findall(r'href=\"(/SGGCB[^\"]{0,80})\"',h)))\nEOF\necho \"--- enhanced-security\"; python3 tx.py citi_enhsec.html | awk 'length>3' | grep -iE -m15 'scam|fraud|lock|kill|hotline|6337|6225|sender|sms'\necho \"--- fraud article\"; python3 tx.py citi_fraudart.html | awk 'length>3' | grep -iE -m12 'date|published|scam|fraud|hotline|6337|6225|sender|sms|official'", "description": "Check Citi sitemap entries, login hosts, other pages"}

### [tool_result]
https://www.citibank.com.sg/digital-banking/secured-banking/enhanced-security 2026-10-23 monthly 1.0
https://www.citibank.com.sg/digital-banking/secured-banking/money-lock 2026-10-23 monthly 1.0
https://www.citibank.com.sg/wealth-management/wealth-insights/financial-fraud-how-to-stay-safe-from-scams 2026-10-23 monthly 1.0
https://www.citibank.com.sg/static1/static/prevention-protection/ 2026-10-24 monthly 1.0
https://www.citibank.com.sg/static/contact 2026-10-23 monthly 1.0
https://www.citibank.com.sg/personal-banking/online-services/secure-banking/online-security-tips/ 2026-10-24 monthly 1.0
{'https://www.citibank.com.sg/SGGCB/JSO/username/signon/flow.action', 'https://www.ipb.citibank.com.sg/SGIPB/JSO/username/signon/flow.action'}
set()
--- enhanced-security
   Enhanced Security through the Citi Mobile ®  App Online Security Device (OSD) SMS 
 Please ensure your mobile number is updated if you are authentiating via SMS OTP
 When required to enter an OTP, a single-use random set of numbers will be generated by the OSD as an added level of authentication to access Citibank Online and Citi Mobile® App services. Alternatively, you may also request for the OTP to be sent to your mobile number* via SMS.*In order for you to receive the OTP successfully, it is important to update the bank with your latest mobile number.
 We have updated the Citi Mobile® App with enhanced security capabilities to provide you with a more convenient and seamless mobile banking experience. This will enable you to proceed with your transactions seamlessly and securely on this device without having to enter the Unlock Code or SMS OTP. Please note that you may deregister the enhanced security capabilities on your Citi Mobile® App at any time via ‘Enhanced Security Capabilities Deregistration’ (under ‘My Profile’) in Citibank Online.
 When you log in (using biometrics authentication or UserID and Password) to your Citi Mobile® App with the enhanced security capabilities, we will be able to recognise and authenticate you seamlessly. You will no longer be required to enter an Unlock Code or SMS OTP for your transactions on Citi Mobile® App after such registration for enhanced security capabilities, unless we require additional verification. This means lesser steps, lesser waiting time and faster processing for your banking transactions.
 Yes, you will still be able to access the Citi Mobile® App and you will continue to receive SMS OTPs to authenticate your transactions on the app. However, you will not be able to perform high-risk transactions (adhoc Payment and Transfer, Personal Information update, high value funds transfer, etc.) unless you register for enhanced security capabilities on your Citi Mobile® App.
 If you are a registered user of Citi Mobile® App with enhanced security and you wish to access your account details or perform transactions on Citibank Online, you will be prompted to authenticate your transaction securely by scanning the QR code on screen via the Citi Mobile® App and performing Biometric or Password authentication. You will no longer be required to key in your Transaction Authorisation Code or SMS One-Time PIN (“OTP”), unless Citi requires additional verification.
 I did not receive any SMS OTP when I tried to update to the enhanced security authentication feature. What might be the issue? 
 Please try to restart your device or check your airplane mode setting to ensure it is not activated. If the issue persists, please call CitiPhone Hotline for further assistance.
 Regardless of your location, you will be able to register for enhanced security capabilities on your Citi Mobile® App if you are able to receive the SMS OTPs. Make sure to update your mobile number before travelling overseas and enable international roaming services on your Singapore mobile number. If you are using a different SIM card while travelling overseas, you might not be able to register for enhanced security capabilities.
 We have updated the Citi Mobile® App with enhanced security capabilities to provide you with a more convenient and seamless mobile banking experience. This will enable you to proceed with your transactions seamlessly and securely on this device without having to enter the Unlock Code or SMS OTP.
 Can I continue receiving OTP via SMS after receiving the OSD? 
 Can I receive an OTP via SMS to an overseas mobile number? 
 Yes, the OTP via SMS can be sent to both a Singapore and overseas mobile number. Ensure that you have updated the bank with your latest mobile number.
 The OTP via SMS will not be forwarded to your new mobile number. Please update your new mobile number with the bank.
--- fraud article
 Protect your wealth from Financial Scams | Citibank Singapore 
 Financial Fraud - How to stay safe from scams
 Types of financial scams 
 Spotting financial fraud early 
 Actions to take if fraud occurs</span>" data-ctaposition="undefined" data-destinationurl="#retirement-income-last" href="#retirement-income-last">
 Actions to take if fraud occurs 
 Financial fraud is evolving—anyone can be the target including the affluent.
 Scam types include investment scams, phishing, impersonation, and more.
 Wealth signals increase your risk of social engineering scams.
 Verify offers and alerts through trusted and official channels.
 In today’s digital-first world, financial fraud is becoming more sophisticated and widespread. Scammers are no longer targeting only the uninformed. They are now using credible-looking messages and platforms to reach a wider audience. With new formats appearing regularly and tactics becoming harder to spot, it becomes important for everyone to stay informed and cautious.
 This article outlines the type of scams to be aware of, how to stay ahead of these scams, and what you need to do should you get suspicious. Future articles will explore fraud-proofing your wealth, protecting loved ones, and building layered security into your financial strategy.

### [tool_use WebSearch]
{"query": "site:citibank.com.sg scam", "mode": "standard"}

### [tool_result]
You've hit your session limit · resets 9:40pm (Asia/Singapore)

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)