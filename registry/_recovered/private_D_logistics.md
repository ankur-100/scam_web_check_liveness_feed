# Recovered transcript digest: private_D_logistics (agent a0e5e0e0d9d522643)

### [user]
You are sub-agent D of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_D_logistics.json
Scratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/

YOUR ENTITIES (delivery-scam brands; SPF advisories impersonate several of them)
Tier 1:
1. SingPost (singpost.com). SPF brand-tag string: "SingPost". Start: https://www.singpost.com/online-security-you (earlier survey: dated 2022-02-28; official domain singpost.com; look-alike examples www.singpost.com.xyz.com, www.singpost.net, www.singpost.org; sender IDs SGPOST/SINGPOST) - re-verify, and look for newer scam notices (tracking-page banners, newsroom, FAQ).
2. Ninja Van Singapore (verify domain, e.g. ninjavan.co with /en-sg). SPF brand-tag string: "Ninjavan".
3. SPX Express Singapore (verify domain, e.g. spx.sg). SPF brand-tag string: "SPX".
4. J&T Express Singapore (verify domain, e.g. jtexpress.sg)
5. Qxpress Singapore (verify domain)
6. DHL Singapore (SG pages under dhl.com/sg-en -> entity_id "dhl.com"; DHL has fraud-awareness pages - record the SG version and any official-domain statements)
7. Lalamove Singapore (SG pages under lalamove.com -> entity_id "lalamove.com"; verify). SPF brand-tag string: "Lalamove".
8. Park N Parcel (verify domain). SPF brand-tag string: "Park N Parcel".
9. uParcel (verify domain, e.g. uparcel.sg). SPF brand-tag string: "uParcel".
Tier 2 (quick, at most 2, only if they have SG scam pages): Pickupp SG, FedEx SG (fedex.com/en-sg), UPS SG, Aramex SG.

For delivery brands, look specifically for: "we will never ask you to pay via SMS link" statements, official tracking hosts, official SMS sender IDs, official WhatsApp numbers, and any listed fake websites/numbers.

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
{"command": "cat /home/ankur/scamtrends_feed/registry/FORMAT.md; echo ----; ls -la /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/", "description": "Read FORMAT.md and list work folder"}

### [tool_use Bash]
{"command": "grep -n -i -E 'singpost|ninja|spx|j&t|jtexpress|qxpress|dhl|lalamove|park ?n ?parcel|uparcel|pickupp|fedex|ups|aramex|logistic|delivery|parcel' /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -80", "description": "Grep earlier survey for delivery brands"}

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
21:| 1 | [zeyalt/Crime-Script-Analysis-NLP `Data/scam_raw_dataset.csv`](https://github.com/zeyalt/Crime-Script-Analysis-NLP) | Univ. of Leeds (Lwin Tun & Birks, *Crime Science* 2023) / academic scrape of scamalert.sg | Victim scam stories + "scammer details" (name, contact) + scam type | 4,660 reports; 971 have phone-like contacts; 503 stories mention a URL | CSV (5.8 MB) on GitHub raw, **but the file contains git merge-conflict markers**. Keep the HEAD side to parse it | 2020-07-17 (range 2016-07-20 → 2020-07-17) | **No LICENSE file** (all rights reserved by default). Upstream content belongs to NCPC and the submitters. **Contains PII** (submitter names, bank account numbers) | 100% SG | **Medium.** Best open SG scam-text corpus with a type label and phone IOCs. Stale for domains |
22:| 2 | [reportsmishing/Smishing-Dataset-IMC25](https://github.com/reportsmishing/Smishing-Dataset-IMC25) | UCL et al., IMC '25 / academic | Labelled smishing texts: sender type, network, language, named entity (impersonated brand), scam type, lure principles | 33,869 rows global; **~190 SG-relevant** (23 on SGP networks; DBS 69, OCBC 40, Singpass 24, POSB 8, IRAS 8, Singtel 7, UOB 6, SingPost 3, CPF 3) | CSV (9.5 MB) on GitHub raw | `time` field is free-form ("Today 8:48 AM"). Only 157 rows have ISO dates, earliest 2021-09-17 | **CC BY 4.0** | Low share, but SG brands are tagged | **Medium-low.** URLs redacted to `<URL>`, so no domains. Good for SG lure templates and brand priors. Cleanest licence here |
23:| 3 | Group-IB SG reports: [Immediate Era (2025-10-21)](https://www.group-ib.com/blog/immediate-era-fraud-singapore/), [SingPost delivery scams](https://www.group-ib.com/blog/fake-delivery-scams-singapore/), [SupportGoWhere phishing PR](https://www.group-ib.com/media-center/press-releases/phishing-campaign-targeting-singapore/) | Group-IB / commercial TI | Campaign narratives with **counts**: 52 redirect domains and 119 fake-news domains (Immediate Era); 107 sites incl. 85 SingPost look-alikes (delivery) | Domain lists **not published**. Only 1 example domain appears in the Immediate Era text | HTML narrative. IOCs "available to customers in the TI portal" | 2025-10-21 | Group-IB site ToS, proprietary | High | **Low as data, high as context.** Gives ground-truth scale for validating coverage |
26:| 6 | [whoseno.com (SG)](https://whoseno.com/singapore/recent-lookups) | WhoseNo / crowdsourced lookup + caller-ID app | "Most reported spam numbers in SG, last 7 days" with calls, reports, activity score (0–100) | ~10 ranked numbers per page | HTML only | Rolling 7-day window (live) | Not reviewed in depth. Commercial app funnel | High | **Low** |
29:| 9 | **Corporate official-domain allowlists**: [Singtel scam advisory](https://www.singtel.com/personal/support/scam-advisory), [SingPost online security](https://www.singpost.com/online-security-you), Carousell, Shopee help centre | Brand owners | Domains and channels that **are** legitimate, plus a few look-alike *patterns* | Singtel ≈45 official/partner domains (e.g. `singtel.com`, `singtelcrm.com`, `gomo.sg`, `heya.sg`, `dash.com.sg`, `portal.singtelge.com`). SingPost and Carousell give patterns only | HTML (the Singtel list is in a JSON component blob) | Singtel live; SingPost page dated 2022-02-28 | Corporate site terms | High | **Medium as a negative set** for allowlisting and false-positive suppression on brand-impersonation matches |
35:| 15 | Community forums/groups: HardwareZone EDMW scam threads, r/singapore, Telegram/Facebook "SG scam alert" groups | Community | Ad-hoc screenshots of SMS/links/numbers in posts | Unknown | HTML threads (HWZ guest-readable); Reddit not reachable from this tool | HWZ "New Scam Variants" thread started 2025-01-04 | HWZ and Reddit ToS restrict automated collection (Reddit Data API terms apply). No credible standing Telegram/FB list found. SPF itself warns about *fake* "official" Telegram channels | High | **Very low** for structured data |
50:- Lookout blog on SingPost/Singtel phishing: 403.
74:- SG subset ≈ 193 rows (network = SGP, or named_entity is an SG brand). Of these, banking 130, government 48, delivery 6, telecom 5.
76:  - `2022-04-13 | SGP | "SingaPost : Your Reffrence Number <US_BANK_NUMBER> Is ready for collection, Or you can add an address … <URL>" | singapost | delivery`
82:- Delivery scams: SingPost impersonation infrastructure of 107 sites (85 SingPost look-alikes, registered 2020-12-25 → 2021-03-01), plus Groups 2/3 (80+ sites). No list.
99:- **SingPost** (page dated 2022-02-28): official = `singpost.com`. It gives look-alike examples **not** to trust: `www.singpost.com.xyz.com`, `www.singpost.net`, `www.singpost.org`. Sender-ID variants `SGPOST`/`SINGPOST`.
131:  - zeyalt scamalert.sg scrape: fine for internal research. Do **not** redistribute it. The upstream text is NCPC/submitter content containing PII.
143:2. Add a **brand allowlist table** from the corporate pages (Singtel's ≈45 domains, SingPost/Carousell/Shopee/DBS/OCBC/UOB official domains), plus the published look-alike patterns as typosquat test cases.

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py; sed -n 95,105p /home/ankur/scamtrends_feed/sources/03_community_commercial.md; mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D", "description": "Read validator and SingPost survey notes"}

### [tool_result]
#!/usr/bin/env python3
"""Validate a partial entities JSON file against registry/FORMAT.md (entity records).
Usage: python3 validate.py <file.json> [more.json ...]
"""
import json, re, sys

TOP_KEYS = ["entity_id", "name", "abbr", "aliases", "sector", "parent_entity_id", "country",
            "official_domains", "official_hosts", "scam_info", "official_channels", "evidence", "notes"]
SECTORS = set("gov.ministry gov.statboard gov.organ gov.dept gov.programme gov.court quasi_gov bank payments "
              "telco logistics ecommerce marketplace transport utility retail travel media brokerage insurance "
              "healthcare tech_platform crypto other".split())
SI_KEYS = ["url", "kind", "lists_indicators", "access", "machine_url", "item_count", "latest_item_date",
           "verified", "sample", "notes"]
KINDS = set("advisory_feed alert_page scam_faq official_channels fake_indicator_list news_releases report_portal statistics".split())
INDS = set("domain url phone email sms_sender_id app social_handle bank_account entity_name".split())
ACCESS = set("html rss atom sitemap json_api_documented csv pdf".split())
OC_KEYS_REQUIRED = ["sms_sender_ids", "hotlines", "short_link_domains", "social"]
OC_KEYS_EXTRA_OK = ["apps", "emails"]  # additive extension, flagged to caller
DOM_RE = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
ID_RE = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+(#[a-z0-9-]+)?$")
DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

def err(msgs, eid, m):
    msgs.append(f"[{eid}] {m}")

def check(rec, msgs, seen):
    eid = rec.get("entity_id", "?")
    for k in TOP_KEYS:
        if k not in rec:
            err(msgs, eid, f"missing key {k}")
    for k in rec:
        if k not in TOP_KEYS:
            err(msgs, eid, f"unknown top-level key {k}")
    if not isinstance(eid, str) or not ID_RE.match(eid):
        err(msgs, eid, "entity_id not a lowercase registrable domain (optionally #slug)")
    if eid in seen:
        err(msgs, eid, "duplicate entity_id")
    seen.add(eid)
    if rec.get("sector") not in SECTORS:
        err(msgs, eid, f"bad sector {rec.get('sector')}")
    for k in ("aliases", "official_domains", "official_hosts", "scam_info", "evidence"):
        if not isinstance(rec.get(k), list):
            err(msgs, eid, f"{k} must be a list")
    for d in rec.get("official_domains") or []:
        if not DOM_RE.match(d) or d.startswith("www."):
            err(msgs, eid, f"official_domains entry not a bare registrable domain: {d}")
    base = eid.split("#")[0]
    if rec.get("official_domains") and base not in rec["official_domains"]:
        err(msgs, eid, f"entity_id domain {base} not in official_domains")
    for h in rec.get("official_hosts") or []:
        if not DOM_RE.match(h):
            err(msgs, eid, f"official_hosts entry not a hostname: {h}")
    for e in rec.get("evidence") or []:
        if not str(e).startswith("http"):
            err(msgs, eid, f"evidence not a URL: {e}")
    if not rec.get("evidence"):
        err(msgs, eid, "evidence is empty")
    for i, si in enumerate(rec.get("scam_info") or []):
        for k in SI_KEYS:
            if k not in si:
                err(msgs, eid, f"scam_info[{i}] missing {k}")
        for k in si:
            if k not in SI_KEYS:
                err(msgs, eid, f"scam_info[{i}] unknown key {k}")
        if si.get("kind") not in KINDS:
            err(msgs, eid, f"scam_info[{i}] bad kind {si.get('kind')}")
        if si.get("access") not in ACCESS:
            err(msgs, eid, f"scam_info[{i}] bad access {si.get('access')}")
        li = si.get("lists_indicators")
        if not isinstance(li, list) or any(x not in INDS for x in li):
            err(msgs, eid, f"scam_info[{i}] bad lists_indicators {li}")
        ic = si.get("item_count")
        if ic is not None and not isinstance(ic, int):
            err(msgs, eid, f"scam_info[{i}] item_count must be int or null")
        d = si.get("latest_item_date")
        if d is not None and not DATE_RE.match(str(d)):
            err(msgs, eid, f"scam_info[{i}] latest_item_date not ISO: {d}")
        if not str(si.get("url", "")).startswith("http"):
            err(msgs, eid, f"scam_info[{i}] url not http(s)")
        v = si.get("verified")
        if not (isinstance(v, str) and v.startswith("2026-")):
            err(msgs, eid, f"scam_info[{i}] verified should look like '2026-11-25 HTTP 200' (got {v})")
    oc = rec.get("official_channels")
    if not isinstance(oc, dict):
        err(msgs, eid, "official_channels must be an object")
    else:
        for k in OC_KEYS_REQUIRED:
            if not isinstance(oc.get(k), list):
                err(msgs, eid, f"official_channels.{k} must be a list")
        for k in oc:
            if k not in OC_KEYS_REQUIRED + OC_KEYS_EXTRA_OK:
                err(msgs, eid, f"official_channels unknown key {k}")
            elif not isinstance(oc[k], list):
                err(msgs, eid, f"official_channels.{k} must be a list")

def main():
    total, allmsgs, seen = 0, [], set()
    for fn in sys.argv[1:]:
        data = json.load(open(fn))
        if not isinstance(data, list):
            print(f"{fn}: top level must be an array"); sys.exit(1)
        for rec in data:
            check(rec, allmsgs, seen)
        total += len(data)
        print(f"{fn}: {len(data)} records")
    for m in allmsgs:
        print("  -", m)
    print(f"TOTAL {total} records, {len(allmsgs)} problems")
    sys.exit(1 if allmsgs else 0)

if __name__ == "__main__":
    main()
  - Net: these sites are not a defensible scam-phone source. ScamShield (government) is the authoritative SG source for numbers.

### 9. Corporate allowlists (negative set)
- **Singtel**: the "List of official Singtel web domains" says all `*.singtel.com` domains are official and adds ≈45 partner domains. Examples: `singtelcrm.com`, `singteltvgo.com`, `portal.singtelge.com`, `gomo.sg`, `heya.sg`, `dash.com.sg`, `gxs.com.sg`, `e-station2.axs.com.sg`, `singtelcares.syd1.qualtrics.com`. Machine-extrac

### [assistant text]
Now let me set up a fetch helper and start with SingPost.

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncat > $D/fetch.sh <<'EOF'\n#!/bin/bash\n# usage: fetch.sh OUTFILE URL\nUA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\nD=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\nout=\"$D/$1\"; url=\"$2\"\nr=$(curl -sL -A \"$UA\" -H 'Accept-Language: en-SG,en;q=0.9' --compressed --max-time 30 -o \"$out\" -w '%{http_code} %{url_effective}' \"$url\")\necho \"$r size=$(stat -c %s \"$out\" 2>/dev/null) -> $1\"\necho \"$(date -Is) $url $r\" >> $D/fetchlog.txt\nsleep 1.2\nEOF\nchmod +x $D/fetch.sh\ncd $D && ./fetch.sh sp_home.html https://www.singpost.com/ && ./fetch.sh sp_robots.txt https://www.singpost.com/robots.txt && ./fetch.sh sp_onlinesec.html https://www.singpost.com/online-security-you\nhead -c 600 $D/sp_robots.txt; echo; grep -i sitemap $D/sp_robots.txt", "description": "Create fetch helper; fetch SingPost home, robots, security page"}

### [tool_result]
200 https://www.singpost.com/ size=156502 -> sp_home.html
200 https://www.singpost.com/robots.txt size=69 -> sp_robots.txt
200 https://www.singpost.com/online-security-you size=140520 -> sp_onlinesec.html
User-agent: *
Allow: /

Sitemap: http://www.singpost.com/sitemap.xml

Sitemap: http://www.singpost.com/sitemap.xml

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && python3 - <<'EOF'\nimport re,html\nt=open('sp_onlinesec.html',encoding='utf-8',errors='ignore').read()\n# strip scripts/styles\nt2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',t)\ntxt=html.unescape(re.sub(r'(?s)<[^>]+>',' ',t2))\ntxt=re.sub(r'\\s+',' ',txt)\ni=txt.lower().find('online security')\nprint(len(txt))\n# print main section around keywords\nfor kw in ['scam','phish','sender','official','sgpost','.net','.org','xyz','never','updated','2022','2023','2024','2025','2026']:\n    for m in re.finditer(re.escape(kw),txt,flags=re.I):\n        pass\nidx=[m.start() for m in re.finditer('(?i)scam|phish',txt)]\nprint(idx[:5], idx[-5:])\nstart=max(0,idx[0]-1500) if idx else 0\nprint(txt[start:start+9000])\nEOF", "description": "Extract text of SingPost online security page"}

### [tool_result]
6437
[361, 493, 554, 579, 601] [3326, 4069, 5190, 5247, 5278]
 Online Security & You | SingPost Personal Small Business Enterprise Help & Support Tools Sending Receiving Shop Pay Document Services Money & Health Insurance PERSONAL BUSINESS ENTERPRISE Help & Support Tools Track your item Calculate rates Locate us Check Delivery Rates Search Search POPULAR SEARCHES track item Locate Us smartpac Popstop Popstation Popdrop Scams Home Online Security & You Be Alert, Be Protected We are taking extra measures for your added security Be alert Identifying a scam Notifications Emails from SingPost FAQ Be alert against scams Cases of fraud and scam are on the rise. Scammers are using SMS and email phishing disguised as delivery notifications, targeting SingPost customers by tricking them into accessing fake websites to make payments or to provide sensitive personal information. With such phishing attempts taking the lead, SingPost is taking extra measures to protect you. If you suspect you have received such emails, calls, or SMSes, please do not respond to it or click on any links. Find out more below how to verify the authenticity of such communications. How to identify a scam attempt? How do you tell if an SMS is a scam attempt? Sender tries to impersonate SingPost with variations such as ‘SGPOST’ or ‘SINGPOST’ Web URLs don’t end with the official singpost.com You are asked to provide your personal details and/or payment online How do you tell if an Email is a scam attempt? SingPost do not send out emails requesting individuals to fill out online applications Emails sent from non-singpost.com domains Things to note Payments to SingPost can only be done via the SingPost Mobile App, at SAM machines, or any post office—never through an online link Your parcels can only be tracked on the SingPost Mobile App and singpost.com/track-items We will never request for personal or banking information such as your full name, ID number, home address, and credit card details via SMS We will never send you an SMS for non-delivery matters such as lucky draws, loans, or job offers If we are unable to deliver an item to you, you will receive a physical Non-Delivery Advice to collect the item from a post office or POPStation. Switching from SMS to Push Notifications SingPost Mobile App - Push Notifications Since 28 February 2022, we have switched from using SMS alerts to pushing out notifications from the SingPost Mobile App to inform you of service updates, for added security. The SingPost Mobile App allows you to track and manage deliveries without having to worry about landing on unsuspecting phishing sites. The mobile app features the use of mobile biometric security features, as well as in-app pin verification and OTP-required account registration as added security measures. How to enable Push Notifications? For iOS users For Android users Push Notifications enabled Please note: We will still send you an SMS only for the following situations: One-Time PIN for verification purposes or registration of SingPost Mobile App account One-Time PIN when using POPStations and POPStations-related service updates Post office digital queue tickets Customer Service follow-up for selected customer feedback and accounts Emails from SingPost Limiting the use of clickable links in emails from SingPost Emails are a common tool used by scammers in phishing attempts. A phishing email looks like an official email and tries to trick you into visiting a fake website and providing your personal and account information. It may also ask you to call a phone number and provide account information. As such, we will be limiting the use of clickable links in our emails to you. While we continue to include crucial links in our emails with you, please note that the links will only point to the following websites operated by SingPost: Singpost.com vPost.com SgLocate.com Ezyparcels.com Speedpost.com.sg MySam.sg Ezy2ship.net The list above may change from time to time, and we will notify you when there are updates to the list. The latest list will be updated on this page. Always verify that the link is legitimate Scammers may continue to impersonate SingPost to trick you into clicking links and providing personal information or payment details to them. Hence, it is critical to learn how to verify that the links you click on are legitimate. When clicking on the link, always double check the URL in the address bar of your browser. For example: SingPost’s URL is always www.singpost.com. www.singpost.com www.singpost.com/about-singpost www.singpost.com/personal SingPost’s URL should NOT look like these: www.singpost.com.xyz.com www.singpost.net www.singpost.org For your added safety, we recommend that you copy the URL from the email and paste it into the browser manually. In addition, always check that the website is secure. To do so, identify the lock symbol next to the address bar. Ensure that the URL is complete and contains the domains listed above. Be sure to look out for slight deviations in the domain name, such as 0 (zero) in place of the letter O, or use of the lowercase L for I. For instance: General FAQ What if I’m expecting a parcel/mail? How to assess the legitimacy of calls, email & SMSes? How to avoid phishing attacks? What should you do if you receive such phishing emails? How to report phishing incidents? Useful links Push Notifications FAQ What is a Push Notification and what will I receive it for? Can I request for other channels of notifications such as through email or letter? How can I view Push Notifications on the SingPost Mobile App? Do I need to login to access Push Notifications? Why is my mobile number required to register for an account on SingPost Mobile App? What happens if I turn off/disable all push notifications on my mobile device by default? I have changed my mobile phone recently; can I still receive Push Notifications on my new mobile phone? Personal Domestic International Delivery Rates Calculate Postage Busines

### [assistant text]
The page explicitly lists SingPost-operated domains. Let me dig into the FAQ accordion content, footer socials, app links, and links.

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && python3 - <<'EOF'\nimport re,html\nt=open('sp_onlinesec.html',encoding='utf-8',errors='ignore').read()\nfor kw in ['How to report phishing','How to assess the legitimacy','What should you do if you receive']:\n    i=t.find(kw)\n    seg=t[i:i+3000]\n    s=html.unescape(re.sub(r'(?s)<[^>]+>',' ',seg)); s=re.sub(r'\\s+',' ',s)\n    print('==',kw,'::',s[:900]); print()\nhrefs=sorted(set(re.findall(r'href=\"([^\"#]+)\"',t)))\nprint([h for h in hrefs if re.search(r'facebook|instagram|twitter|x\\.com|linkedin|youtube|tiktok|apple|play\\.google|telegram|whatsapp|mailto|tel:',h,re.I)])\nhosts=sorted(set(re.findall(r'https?://([a-z0-9.-]+)',t,re.I)))\nprint(hosts)\nm=re.findall(r'(?i)(last updated|updated on|published)[^<]{0,80}',t); print(m[:5])\nEOF", "description": "Extract FAQ answers, social/app links, hosts"}

### [tool_result]
== How to report phishing :: How to report phishing incidents?"],"body":[0,"<p>If you have received a suspicious email, letter, SMS or phone call purportedly from SingPost, call SingPost's hotline at 1605 to verify the authenticity of such messages.</p><p>Do not respond to them or click on any hyperlink. In the case of suspicious phone calls, you should request for the caller’s full name, telephone number and department and validate this through our Customer Service hotline at 1605.</p><p>If you suspect that you have responded to a phishing scam with personal or financial information, you are advised to:</p><ul><li data-list-item-id=\"e898c794b8c6b522b8d197d3d11c14fe3\">Lodge a police report;</li><li data-list-item-id=\"e5cbd75c3c0c49b2fdec3226c1a4dae23\">Change the passwords or PINs on all your online accounts; and</li><li data-list-item-id=\"e1d82999c82dc7bcb0c144a649475a480\">Contact your banks to stop any transa

== How to assess the legitimacy :: How to assess the legitimacy of calls, email & SMSes?"],"body":[0,"<p>SingPost does not initiate automated voice calls and our primary language of communication with customers is always English first, unless otherwise requested specifically by customer.</p><p>All official emails from SingPost will always be sent from email addresses ending with \"@singpost.com\". Emails will not be sent from personal email accounts such as Hotmail, Gmail, or other unfamiliar email domains. We also do not initiate any SMS asking you to claim a prize or to make any form of payments by clicking on a link in the SMS.</p><p>SingPost is working closely with the Singapore Police Force to take down fake websites and stop fake SMSes, to prevent the public from falling for such scams. You may lodge a police report if you receive such calls, email or SMSes.</p><p>If you have further questions, please call the SingP

== What should you do if you receive :: What should you do if you receive such phishing emails?"],"body":[0,"<p>To safeguard yourself, please be extra careful when you receive an unsolicited email or all other forms of communication asking you to provide confidential or personal information. Under no circumstances should you give personal information including credit card or banking details to third parties via email, letter, SMS, or phone until and unless you have verified the authenticity of such requests.</p><ul><li data-list-item-id=\"ed8621e570e0ae0286cbfcb6d2b4a8772\">Check the full URL to ensure that the website is legitimate. SingPost’s URL is always www.singpost.com., For example:<ul><li data-list-item-id=\"e369f5d0b117ba103a3a802f18916816d\">www.singpost.com</li><li data-list-item-id=\"eb76cd9e4736ff1627d2fac6a90665265\">www.singpost.com/corporate/about</li><li data-list-item-id=\"ee32faeaa44be8ba7501788e5cf4ea2e5\">

['https://sg.linkedin.com/company/singapore-post', 'https://www.facebook.com/singpost', 'https://www.instagram.com/mysingpost/']
['analytics.tiktok.com', 'connect.facebook.net', 'crmint.singpost.com', 'fonts.googleapis.com', 'fonts.gstatic.com', 'schema.org', 'sg.linkedin.com', 'shop.singpost.com', 'singpost.com', 'support.microsoft.com', 'www.csa.gov.sg', 'www.facebook.com', 'www.google.com', 'www.googletagmanager.com', 'www.instagram.com', 'www.mas.gov.sg', 'www.police.gov.sg', 'www.scamalert.sg', 'www.scamshield.gov.sg', 'www.singpost.com', 'www.twitter.com', 'www.w3.org', 'zn3ruhkov4cdxtyzp-singpost.siteintercept.qualtrics.com']
['updated on']

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && ./fetch.sh sp_sitemap.xml https://www.singpost.com/sitemap.xml && head -c 400 sp_sitemap.xml; echo; grep -o '<loc>[^<]*</loc>' sp_sitemap.xml | wc -l; grep -o '<loc>[^<]*</loc>' sp_sitemap.xml | grep -i -E 'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect|advisor|notice' \npython3 - <<'EOF'\nimport re\nt=open('/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/sp_home.html',encoding='utf-8',errors='ignore').read()\nhrefs=sorted(set(re.findall(r'href=\"([^\"#]+)\"',t)))\nprint([h for h in hrefs if re.search(r'facebook|instagram|twitter|x\\.com|linkedin|youtube|tiktok|apple|play\\.google|telegram|whatsapp|mailto|tel:|track|scam|secur|app',h,re.I)])\nprint(sorted(set(re.findall(r'https?://([a-z0-9.-]+)',t,re.I))))\nfor m in re.finditer(r'(?i)scam|phish|fraud',t):\n    s=t[max(0,m.start()-200):m.start()+200]\n    s=re.sub(r'(?s)<[^>]+>',' ',s); s=re.sub(r'\\s+',' ',s)\n    print('--',s)\nEOF", "description": "Fetch SingPost sitemap, grep scam URLs, check home links"}

### [tool_result]
200 https://www.singpost.com/sitemap.xml size=49612 -> sp_sitemap.xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://www.singpost.com/corporate/media-centre/singpost-underlying-net-profit-doubles-s115m-h1-fy2627</loc><lastmod>2026-11-05T23:40:36+00:00</lastmod></url>
<url><loc>https://www.singpost.com/corporate/media-centre/singpost-commemorates-60-years-singapore-egypt-bilateral-relations-specia
327
<loc>https://www.singpost.com/contact-us/data-protection</loc>
<loc>https://www.singpost.com/online-security-you</loc>
<loc>https://www.singpost.com/corporate/media-centre/singpost-appoints-bofa-securities-financial-advisor-strategic-review</loc>
['/online-security-you', '/search?q=Scams', '/search?q=track%20item', '/singpost-mobile-app', '/track-items', 'https://sg.linkedin.com/company/singapore-post', 'https://www.facebook.com/singpost', 'https://www.instagram.com/mysingpost/']
['analytics.tiktok.com', 'connect.facebook.net', 'fonts.googleapis.com', 'fonts.gstatic.com', 'schema.org', 'sg.linkedin.com', 'shop.singpost.com', 'singpost.com', 'vpost.com', 'www.facebook.com', 'www.google.com', 'www.googletagmanager.com', 'www.instagram.com', 'www.singpost.com', 'www.twitter.com', 'www.w3.org', 'zn3ruhkov4cdxtyzp-singpost.siteintercept.qualtrics.com']
-- ary">Popstop Popstation Popdrop Scams var e=document.getElementById(`search-overlay`);e?.addEventListener(`click`,t=>{t.target===e&&e
-- /search?q=Popstation" class="hover:text-primary">Popstation Popdrop Scams var e=document.getElementById(`search-overlay`);e?.addEventListener(`click`,t=>{t.target===e&&e.classList.add(`hidden`)});</scrip

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [tool_use WebSearch]
{"query": "SingPost scam advisory phishing SMS fake website 2026", "mode": "standard"}

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && ./fetch.sh sp_app.html https://www.singpost.com/singpost-mobile-app && python3 - <<'EOF'\nimport re\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nt=open(D+'sp_app.html',encoding='utf-8',errors='ignore').read()\nprint([h for h in sorted(set(re.findall(r'href=\"([^\"#]+)\"',t))) if re.search(r'apple|play\\.google|huawei|appgallery|twitter|x\\.com|track',h,re.I)])\nh=open(D+'sp_home.html',encoding='utf-8',errors='ignore').read()\nfor m in re.finditer(r'twitter\\.com[^\"\\'\\s<]*',h): print(m.group(0))\n# media centre urls in sitemap with dates\ns=open(D+'sp_sitemap.xml').read()\nmc=re.findall(r'<loc>(https://www.singpost.com/corporate/media-centre/[^<]*)</loc><lastmod>([^<]*)</lastmod>',s)\nprint(len(mc)); print(mc[:3])\nEOF", "description": "Fetch SingPost app page; extract store links and media URLs"}

### [tool_result]
Web search results for query: "SingPost scam advisory phishing SMS fake website 2026"

Links: [{"title":"20260327 advisory on phishing scams involving whatsapp messages impersonating sg post","url":"https://www.police.gov.sg/Media-Hub/News/2026/03/20260327_advisory_on_phishing_scams_involving_whatsapp_messages_impersonating_sg_post"},{"title":"20260327 advisory on phishing scams involving whatsapp messages impersonating sg post","url":"https://www.police.gov.sg/media-hub/news/2026/03/20260327_advisory_on_phishing_scams_involving_whatsapp_messages_impersonating_sg_post"},{"title":"20231101 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/11/20231101_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20231215 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/12/20231215_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20231101 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/20231101_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20231215 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/20231215_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20241122 police advisory on increase of parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2024/20241122_police_advisory_on_increase_of_parcel_delivery_phishing_scams"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://www.police.gov.sg/media-hub/news/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"},{"title":"20210116 police advsry on non banking phishing scams invlvg emails and txt msgs related to delivery","url":"https://www.police.gov.sg/media-hub/news/2021/20210116_police_advsry_on_non-banking_phishing_scams_invlvg_emails_and_txt_msgs_related_to_delivery"},{"title":"20240920 police advisory on phishing scams and usage of online messaging channels","url":"https://www.police.gov.sg/media-hub/news/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging_channels"},{"title":"20231215 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/Media-Hub/News/2023/20231215_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://www.police.gov.sg/Media-Hub/News/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"},{"title":"hub-mngr.singpost.com","url":"https://hub-mngr.singpost.com/node/52"},{"title":"20221103 police advisory on the re emergence of email phishing scams involving sg companies","url":"https://www.police.gov.sg/media-hub/news/2022/20221103_police_advisory_on_the_re-emergence_of_email_phishing_scams_involving_sg_companies"},{"title":"20241122 police advisory on increase of parcel delivery phishing scams","url":"https://police.gov.sg/media-room/news/20241122_police_advisory_on_increase_of_parcel_delivery_phishing_scams"},{"title":"WhatsApp message from SingPost about failed parcel delivery could be a scam: Police","url":"https://www.thestar.com.my/aseanplus/aseanplus-news/2026/03/27/whatsapp-message-from-singpost-about-failed-parcel-delivery-could-be-a-scam-police"},{"title":"20210413 pol advisory on non banking rel phishing scams inv spoofed emails and txt msgs rel to del","url":"https://www.police.gov.sg/Media-Hub/News/2021/20210413_pol_advisory_on_non-banking_rel_phishing_scams_inv_spoofed_emails_and_txt_msgs_rel_to_del"},{"title":"20210906 police advisory on phishing scams for parcel delivery and cheap deals","url":"https://www.police.gov.sg/media-hub/news/2021/20210906_police_advisory_on_phishing_scams_for_parcel_delivery_and_cheap_deals"}]

Based on the search results, here's what I found about SingPost scam advisories:

## Recent 2026 SingPost Phishing Scam Advisory

The Singapore Police has alerted the public to phishing scams involving WhatsApp messages that impersonate Singapore Post Limited ("SingPost"). Since March 15, 2026, at least 10 cases have been reported, with losses amounting to at least $22,000.

### How the Scam Works

In this scam variant, victims receive WhatsApp messages allegedly from SingPost informing them of failed parcel delivery due to incomplete information, and victims are told to click on an embedded link to have the parcel redelivered. The link will direct victims to a phishing website where they are prompted to provide their banking credentials, credit or debit card details, or one-time passwords.

### How to Protect Yourself

SingPost will not send you clickable links through WhatsApp or SMS requesting payments or bank account details. Members of the public should ignore dubious clickable links that are sent through WhatsApp or SMS claiming to be from SingPost.

You can call the 24/7 ScamShield Helpline at 1799 if you are unsure if something is a scam.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_result]
200 https://www.singpost.com/singpost-mobile-app size=116446 -> sp_app.html
['/search?q=track%20item', '/track-items', 'https://apps.apple.com/sg/app/singpost-mobile/id647986630', 'https://play.google.com/store/apps/details?id=com.singPost']
twitter.com/SingaporePost
148
[('https://www.singpost.com/corporate/media-centre/singpost-underlying-net-profit-doubles-s115m-h1-fy2627', '2026-11-05T23:40:36+00:00'), ('https://www.singpost.com/corporate/media-centre/singpost-commemorates-60-years-singapore-egypt-bilateral-relations-special', '2026-11-03T06:40:33+00:00'), ('https://www.singpost.com/corporate/media-centre/singpost-streamlines-shipping-eu-new-customs-requirements-take-effect', '2026-10-28T07:09:50+00:00')]

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && ./fetch.sh sp_track.html https://www.singpost.com/track-items && python3 - <<'EOF'\nimport re,html\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nh=open(D+'sp_home.html',encoding='utf-8',errors='ignore').read()\nfor m in re.finditer(r'.{120}twitter\\.com/SingaporePost.{60}',h): print('TW:',m.group(0))\nfor m in re.finditer(r'\"sameAs\"\\s*:\\s*\\[[^\\]]*\\]',h): print('SAMEAS:',m.group(0))\nt=open(D+'sp_track.html',encoding='utf-8',errors='ignore').read()\nt2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',t)\ntxt=re.sub(r'\\s+',' ',html.unescape(re.sub(r'(?s)<[^>]+>',' ',t2)))\nfor m in re.finditer(r'(?i)scam|phish|fraud|never|beware',txt):\n    print('--',txt[max(0,m.start()-250):m.start()+250])\na=open(D+'sp_app.html',encoding='utf-8',errors='ignore').read()\na2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',a)\natxt=re.sub(r'\\s+',' ',html.unescape(re.sub(r'(?s)<[^>]+>',' ',a2)))\ni=atxt.find('Popdrop Scams'); print('APP:',atxt[i:i+500])\nEOF", "description": "Fetch SingPost track page; check banners, social sameAs, app name"}

### [tool_result]
200 https://www.singpost.com/track-items size=139262 -> sp_track.html
SAMEAS: "sameAs": [
                    "https://www.facebook.com/SingaporePost",
                    "https://www.twitter.com/SingaporePost"
                ]
-- p Pay Document Services Money & Health Insurance PERSONAL BUSINESS ENTERPRISE Help & Support Tools Track your item Calculate rates Locate us Check Delivery Rates Search Search POPULAR SEARCHES track item Locate Us smartpac Popstop Popstation Popdrop Scams Home Track Your Item Track your item Track FAQ Help & Support Personal Domestic International Delivery Rates Calculate Postage Business Small Business Enterprise Property Solutions Company About SingPost Media Centre Investor Relations Careers 
APP: Popdrop Scams Home SingPost Mobile App Track packages, bill payments, shop online and more! Experience the convenience of the SingPost Mobile App, designed to simplify your mailing and payment processes. Track your item's delivery status on the move. Go cashless with ease. Pay customs duties and GST without hassle. Manage bills for selected credit cards and government agencies directly within the app. Using the SingPost Mobile App also helps protect against common SMS delivery fraud and phishing

### [tool_use WebSearch]
{"query": "site:singpost.com scam OR phishing OR fraud notice", "mode": "standard"}

### [tool_result]
Web search results for query: "site:singpost.com scam OR phishing OR fraud notice"

Links: [{"title":"20231101 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/11/20231101_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20241122 police advisory on increase of parcel delivery phishing scams","url":"https://police.gov.sg/media-room/news/20241122_police_advisory_on_increase_of_parcel_delivery_phishing_scams"},{"title":"20241122 police advisory on increase of parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2024/20241122_police_advisory_on_increase_of_parcel_delivery_phishing_scams"},{"title":"20231215 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/12/20231215_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://www.police.gov.sg/Media-Hub/News/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://www.police.gov.sg/media-hub/news/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"},{"title":"20260327 advisory on phishing scams involving whatsapp messages impersonating sg post","url":"https://www.police.gov.sg/media-hub/news/2026/03/20260327_advisory_on_phishing_scams_involving_whatsapp_messages_impersonating_sg_post"},{"title":"20240920 police advisory on phishing scams and usage of online messaging channels","url":"https://www.police.gov.sg/media-hub/news/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging_channels"},{"title":"20260327 advisory on phishing scams involving whatsapp messages impersonating sg post","url":"https://www.police.gov.sg/Media-Hub/News/2026/03/20260327_advisory_on_phishing_scams_involving_whatsapp_messages_impersonating_sg_post"},{"title":"20231101 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/Media-Hub/News/2023/20231101_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20221103 police advisory on the re emergence of email phishing scams involving sg companies","url":"https://www.police.gov.sg/media-hub/news/2022/20221103_police_advisory_on_the_re-emergence_of_email_phishing_scams_involving_sg_companies"},{"title":"20231101 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/media-hub/news/2023/20231101_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://police.gov.sg/Media-Room/News/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"},{"title":"20231101 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/Media-Room/News/20231101_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"hub-mngr-stg.singpost.com","url":"https://hub-mngr-stg.singpost.com/node/52"},{"title":"20231215 police advisory on parcel delivery phishing scams","url":"https://www.police.gov.sg/Media-Hub/News/2023/20231215_police_advisory_on_parcel_delivery_phishing_scams"},{"title":"20211220 police advisory on re emergence of phishing scams involving emails and text messages","url":"https://police.gov.sg/Media-Room/News/20211220_police_advisory_on_re-emergence_of_phishing_scams_involving_emails_and_text_messages"}]

I found search results related to SingPost scams and phishing alerts. Here's a summary of what the search revealed:

## Key Findings:

The search results primarily contain **Singapore Police Force advisories** warning the public about phishing scams impersonating SingPost, rather than official notices from SingPost itself on the singpost.com domain. However, one result from SingPost's website is included:

**From SingPost's Official Security Page:**

Scammers are using SMS and email phishing disguised as delivery notifications, targeting SingPost customers by tricking them into accessing fake websites to make payments or to provide sensitive personal information.

The website suggests checking if senders try to impersonate SingPost with variations such as 'SGPOST' or 'SINGPOST', or if web URLs don't end with the official singpost.com.

**Police Warnings:**

The most recent advisory indicates at least 505 cases involving impersonation of SingPost, with total losses amounting to at least $955,000.

The SMS Sender ID of Singapore Post is SingPost. Payments to SingPost are never through an online link, and SingPost will never request for personal or banking information via SMS.

For protection, SingPost directs people to https://www.singpost.com/online-security-you to stay alert against SingPost-related scams.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && ./fetch.sh spf_20241122.html https://www.police.gov.sg/media-hub/news/2024/20241122_police_advisory_on_increase_of_parcel_delivery_phishing_scams && python3 - <<'EOF'\nimport re,html\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nt=open(D+'spf_20241122.html',encoding='utf-8',errors='ignore').read()\nt2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',t)\ntxt=re.sub(r'\\s+',' ',html.unescape(re.sub(r'(?s)<[^>]+>',' ',t2)))\nprint(len(txt))\nfor m in re.finditer(r'(?i)sender id|ninja|spx|lalamove|park n parcel|uparcel|j&t|qxpress|dhl',txt):\n    print('--',txt[max(0,m.start()-300):m.start()+300])\nEOF", "description": "Verify SPF 2024-11-22 advisory sender-ID statement"}

### [tool_result]
200 https://www.police.gov.sg/media-hub/news/2024/11/20241122_police_advisory_on_increase_of_parcel_delivery_phishing_scams size=295263 -> spf_20241122.html
18576
-- s. The scammers will then make unauthorised purchases using the victim’s credit card details. Victims would only realise that they had been scammed when they noticed unauthorised transactions on their cards or in their bank account statements. The Police would like to advise the public that the SMS Sender ID of Singapore Post is SingPost. Payments to SingPost are never through an online link. Also, SingPost will never request for personal or banking information via SMS. If SingPost is unable to deliver an item, members of the public will receive a physical Non-Delivery Advice to collect the it

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && python3 - <<'EOF'\nimport re\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nt=open(D+'sp_onlinesec.html',encoding='utf-8',errors='ignore').read()\nprint(sorted(set(re.findall(r'\\bid=\"([^\"]+)\"',t)))[:80])\nfor m in re.finditer(r'crmint\\.singpost\\.com[^\"\\'\\s<]*',t): print('CRM:',m.group(0))\nfor m in re.finditer(r'shop\\.singpost\\.com[^\"\\'\\s<]*',t): print('SHOP:',m.group(0)); break\nh=open(D+'sp_home.html',encoding='utf-8',errors='ignore').read()\nprint(sorted(set(h2 for h2 in re.findall(r'href=\"([^\"#]+)\"',h) if re.search(r'help|support|contact|vpost|shop',h2,re.I))))\nEOF", "description": "Check SingPost page anchors and help/CRM hosts"}

### [tool_result]
['ZN_3rUHKov4cDXTYzp', 'be-alert', 'close-search', 'e11141d963dff2bcd55dec56d487fee60', 'e40b876bc8f711914ac6005089c0b65cb', 'e485924b025e7b77437488544a4764961', 'e61d0c22275d67c719fbfcabe33224a05', 'e78bee536dd0d84b377c4290dad405782', 'e7db568e62ac9d5beda1ec60a48ecfafd', 'eae87ae362861631a3fc23559401b4bd3', 'ee61a09b202581f73d63e2b81a408dee4', 'ee63e0a7df92d44a748ff204b5fd751d5', 'emails-from-singpost', 'faq', 'hero-title', 'identifying-scam', 'mobile-navigation', 'notifications', 'popularSearchList', 'radix-_r21R_0_-trigger-radix-_r21R_3_', 'radix-_r22R_1_-trigger-Pay', 'radix-_r22R_1_-trigger-Receiving', 'radix-_r22R_1_-trigger-Sending', 'radix-_r22R_1_-trigger-Shop', 'radix-_r22R_36_', 'radix-_r22R_56_', 'radix-_r22R_76_', 'radix-_r29R_6_', 'radix-_r29R_a_', 'radix-_r29R_e_', 'radix-_r29R_i_', 'radix-_r29R_m_', 'radix-_r29R_q_', 'radix-_r30R_6_', 'radix-_r30R_a_', 'radix-_r30R_e_', 'radix-_r30R_i_', 'radix-_r30R_m_', 'radix-_r30R_q_', 'radix-_r30R_u_', 'radix-_r31R_0_', 'radix-_r32R_0_', 'radix-_r33R_0_', 'search', 'search-overlay']
CRM: crmint.singpost.com/spcontactus/\&quot;&gt;Online
SHOP: shop.singpost.com/&quot;],&quot;icon&quot;:[0,&quot;&quot;],&quot;description&quot;:[0,&quot;&quot;],&quot;subMenu&quot;:[1,[[0,{&quot;label&quot;:[0,&quot;Packing
['/support', '/support/make-enquiry', '/support/service-updates', 'https://shop.singpost.com/', 'https://shop.singpost.com/gifts.html', 'https://shop.singpost.com/materials-packaging.html', 'https://shop.singpost.com/stamps.html', 'https://vpost.com/']

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && ./fetch.sh sp_svcupd.html https://www.singpost.com/support/service-updates && python3 - <<'EOF'\nimport re,html\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nt=open(D+'sp_svcupd.html',encoding='utf-8',errors='ignore').read()\nt2=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',t)\ntxt=re.sub(r'\\s+',' ',html.unescape(re.sub(r'(?s)<[^>]+>',' ',t2)))\ni=txt.find('Popdrop Scams'); print(txt[i:i+3000])\nprint('SCAMHITS', [txt[max(0,m.start()-150):m.start()+150] for m in re.finditer(r'(?i)scam|phish|fraud',txt)][:6])\ns=open(D+'sp_sitemap.xml').read()\nprint([u for u in re.findall(r'<loc>([^<]*)</loc>',s) if '/support' in u])\nEOF", "description": "Fetch SingPost service-updates page and scan for scam notices"}

### [tool_result]
200 https://www.singpost.com/support/service-updates size=616512 -> sp_svcupd.html
Popdrop Scams Home Help & Support ... Service Updates International Service Status Available: Service is currently available but please expect a delay of up to 10 working days depending on the service chosen Limited Services: Service is currently limited and subject to delays Suspended: Service is temporarily not available --> Available Service is currently available Limited to documents only Service is currently available but only documents are accepted Suspended Service is temporarily not available - We currently do not offer this service to the selected country/region Service Announcements All Years 2026 2025 2024 2023 Newest Oldest Personal Domestic International Delivery Rates Calculate Postage Business Small Business Enterprise Property Solutions Company About SingPost Media Centre Investor Relations Careers Help and Support Get Help or get in touch Personal Domestic International Delivery Rates Calculate Postage Business Small Business Enterprise Property Solutions Company About SingPost Media Centre Investor Relations Careers Help and Support Get Help or get in touch Sitemap Terms of Use Privacy Policy Online Security & You Publications © 2026 Singapore Post Limited. All Rights Reserved. 
SCAMHITS ['rack your item Calculate rates Locate us Check Delivery Rates Search Search POPULAR SEARCHES track item Locate Us smartpac Popstop Popstation Popdrop Scams Home Help & Support ... Service Updates International Service Status Available: Service is currently available but please expect a delay of up t']
['https://www.singpost.com/support/sending-an-item/sending-european-union', 'https://www.singpost.com/support/sending-an-item/digital-stamp', 'https://www.singpost.com/support/search', 'https://www.singpost.com/support/business-support/returns-logistics-quality-control', 'https://www.singpost.com/support/business-support/warehousing-fulfilment', 'https://www.singpost.com/support/business-support/international-shipping', 'https://www.singpost.com/support/business-support/domestic-delivery-distribution', 'https://www.singpost.com/support/business-support', 'https://www.singpost.com/support/managing-deliveries/collection-points', 'https://www.singpost.com/support/managing-deliveries/problems-delivery', 'https://www.singpost.com/support/managing-deliveries/customs-clearance-gst-payments', 'https://www.singpost.com/support/managing-deliveries/tracking-receiving-your-items', 'https://www.singpost.com/support/managing-deliveries', 'https://www.singpost.com/support/sending-an-item/custom-declaration', 'https://www.singpost.com/support/other-services-enquiries/pay-sam', 'https://www.singpost.com/support/other-services-enquiries/mail-redirection', 'https://www.singpost.com/support/other-services-enquiries/mail-retention', 'https://www.singpost.com/support/other-services-enquiries/privy', 'https://www.singpost.com/support/sending-an-item/overseas-mail-services-guide', 'https://www.singpost.com/support/sending-an-item/general-prohibition-dangerous-goods', 'https://www.singpost.com/support/sending-an-item/dropoff-locations', 'https://www.singpost.com/support/sending-an-item/sending-ezy2ship', 'https://www.singpost.com/support/sending-an-item/sending-united-states', 'https://www.singpost.com/support/sending-an-item/sending-overseas', 'https://www.singpost.com/support/sending-an-item/sending-within-singapore', 'https://www.singpost.com/support/sending-an-item/mailing-packaging-tips', 'https://www.singpost.com/support/other-services-enquiries', 'https://www.singpost.com/support/sending-an-item', 'https://www.singpost.com/support/service-updates', 'https://www.singpost.com/support/make-enquiry', 'https://www.singpost.com/support/sending-an-item/enhanced-liability', 'https://www.singpost.com/support']

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && grep -o -i -E '.{0,200}(scam|phish|fraud|whatsapp).{0,200}' sp_svcupd.html | grep -v -i 'popdrop' | head -5; grep -c -i 'title' sp_svcupd.html; grep -o -E '\"(title|date|publishDate|publishedDate)\":\\[0,\"[^\"]{0,120}\"' sp_svcupd.html | head -12", "description": "Grep embedded service-update data for scam items"}

### [tool_result]
ugrep: error: error at position 106
whatsapp)(?:[^\n\x80-\xbf][\x80-\xbf]*){0,200}
                 exceeds complexity limits___/


3

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && python3 - <<'EOF'\nimport re,html\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nt=html.unescape(open(D+'sp_svcupd.html',encoding='utf-8',errors='ignore').read())\nhits=[m.start() for m in re.finditer(r'(?i)scam|phish|fraud|whatsapp',t)]\nprint(len(hits))\nfor i in hits[:12]:\n    s=t[max(0,i-200):i+250]\n    if 'Popdrop' in s: continue\n    print('--',re.sub(r'\\s+',' ',s))\n# look for announcement titles\nts=re.findall(r'\"title\":\\[0,\"([^\"]{5,140})\"',t)\nprint(len(ts), ts[:40])\nEOF", "description": "Search embedded announcements for scam-related items"}

### [tool_result]
4
-- peedpost Saver International start from $7.10, and this service will be launched on 22 December.\u003c/p>","year":2025,"sticky":false},{"id":"c14a746b-29ae-4b8f-9c17-7ba7a5bbf4b3","idx":5821,"title":"Scam Alert","date":"01 Jan 2024","content":"\u003cp>Please be aware of new scam emails and SMS impersonating SingPost requesting you to click on a link, provide personal information, or make payments for fake duties. Please remain vigilant, \u003ca h
-- nched on 22 December.\u003c/p>","year":2025,"sticky":false},{"id":"c14a746b-29ae-4b8f-9c17-7ba7a5bbf4b3","idx":5821,"title":"Scam Alert","date":"01 Jan 2024","content":"\u003cp>Please be aware of new scam emails and SMS impersonating SingPost requesting you to click on a link, provide personal information, or make payments for fake duties. Please remain vigilant, \u003ca href=\"/online-security-you\">learn more\u003c/a>. \u003c/p>","year":2024,"s
0 []

### [tool_use Bash]
{"command": "D=/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D\ncd $D && python3 - <<'EOF'\nimport re,html,collections\nD='/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/'\nt=html.unescape(open(D+'sp_svcupd.html',encoding='utf-8',errors='ignore').read())\nitems=re.findall(r'\"idx\":(\\d+),\"title\":\"((?:[^\"\\\\]|\\\\.)*)\",\"date\":\"([^\"]*)\"',t)\nprint(len(items))\nprint(collections.Counter(d[-4:] for _,_,d in items))\nfor idx,ti,d in items:\n    if re.search(r'(?i)scam|phish|fraud|fake|impersonat|vigilant|beware|security',ti): print(idx,ti,d)\n# also check content for scam\nfor m in re.finditer(r'\"title\":\"((?:[^\"\\\\]|\\\\.)*)\",\"date\":\"([^\"]*)\",\"content\":\"((?:[^\"\\\\]|\\\\.)*)\"',t):\n    if re.search(r'(?i)scam|phish|fraud|impersonat',m.group(3)): print('C:',m.group(1),m.group(2),m.group(3)[:300])\nprint(items[:3])\nEOF", "description": "Count announcements and find scam-related ones"}

### [tool_result]
409
Counter({'2025': 153, '2026': 150, '2024': 105, '2023': 1})
5821 Scam Alert 01 Jan 2024
6106 Lebanon – Security situation and disruption of postal operations 05 Mar 2026
C: Scam Alert 01 Jan 2024 \u003cp>Please be aware of new scam emails and SMS impersonating SingPost requesting you to click on a link, provide personal information, or make payments for fake duties. Please remain vigilant, \u003ca href=\"/online-security-you\">learn more\u003c/a>. \u003c/p>
[('3', 'Changes to Speedpost Express shipments to the United States', '07 Oct 2025'), ('4', 'Madagascar– Service disruption resulting from demonstrations', '01 Oct 2025'), ('111', 'Brazil - Severe weather', '09 May 2024')]

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)