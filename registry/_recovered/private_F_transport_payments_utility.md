# Recovered transcript digest: private_F_transport_payments_utility (agent adccbf6085f551f69)

### [user]
You are sub-agent F of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_F_transport_pay_util.json
Scratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F/

YOUR ENTITIES
Tier 1:
1. Grab (grab.com; SG pages under grab.com/sg). SPF brand-tag string: "Grab". GrabPay, Grab safety/scam/phishing pages, official sender IDs, help-centre scam articles.
2. Gojek Singapore (SG pages under gojek.com -> entity_id "gojek.com"; verify)
3. ComfortDelGro (comfortdelgro.com; CDG Zig app; check cdgtaxi.com.sg)
4. SMRT (smrt.com.sg)
5. SBS Transit (sbstransit.com.sg)
6. EZ-Link (ezlink.com.sg): scam advisories, EZ-Link app. (SimplyGo is LTA/TransitLink = quasi-government: mention in notes only, no record.)
7. NETS (nets.com.sg)
8. SP Group (spgroup.com.sg). SPF brand-tag string: "SP Group". SP app, scam advisories, official sender IDs.
Tier 2 (quick, at most 3): Charge+ (SPF brand-tag string "Charge+"; verify domain), TADA, Ryde, City Energy, Geneco.

For transport/payment brands look specifically for: fake-app / fake-website warnings (e.g. fake EZ-Link or SimplyGo top-up sites, fake Grab driver/rewards pages), official sender IDs, official app names, and "we will never..." statements.

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
{"command": "cat /home/ankur/scamtrends_feed/registry/FORMAT.md; echo ======; ls -la /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/", "description": "Read FORMAT.md and list the private work folder"}

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
======
total 96
drwxrwxr-x  2 ankur ankur  4096 Nov 25 18:12 .
drwxrwxr-x 11 ankur ankur  4096 Nov 25 18:14 ..
-rw-rw-r--  1 ankur ankur  9545 Nov 25 18:12 BRIEF.md
-rw-rw-r--  1 ankur ankur 62621 Nov 25 17:57 dbs_robots.txt
-rw-rw-r--  1 ankur ankur     3 Nov 25 18:10 _empty.json
-rw-rw-r--  1 ankur ankur  5497 Nov 25 18:10 validate.py

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py; echo =====; wc -c /home/ankur/scamtrends_feed/sources/03_community_commercial.md; grep -n -i -E 'grab|gojek|comfort|cdg|smrt|sbs|ez-link|ezlink|nets|sp group|spgroup|charge\\+|tada|ryde|city energy|geneco|simplygo' /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -80", "description": "Read validator and grep earlier survey for my entities"}

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
=====
23093 /home/ankur/scamtrends_feed/sources/03_community_commercial.md

### [tool_use Bash]
{"command": "head -60 /home/ankur/scamtrends_feed/sources/03_community_commercial.md; grep -n -i -E 'transport|taxi|ride|payment|utility|electric|top-up|topup' /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -30; ls /home/ankur/scamtrends_feed/registry/", "description": "Skim survey file and list registry folder"}

### [tool_result]
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
| 6 | [whoseno.com (SG)](https://whoseno.com/singapore/recent-lookups) | WhoseNo / crowdsourced lookup + caller-ID app | "Most reported spam numbers in SG, last 7 days" with calls, reports, activity score (0–100) | ~10 ranked numbers per page | HTML only | Rolling 7-day window (live) | Not reviewed in depth. Commercial app funnel | High | **Low** |
| 7 | [singaporenumber.com](https://singaporenumber.com/) | Independent / SG-only lookup | Per-number pages: format, number-range type, public caller reports, Disqus comments | Unknown (no index) | HTML; robots disallows `/number/*/report` | n/a | Not reviewed | High | **Low.** Lookup only, no list |
| 8 | [spamcalls.net +65](https://spamcalls.net/en/country-code/65) | Hello World Digital (DE) / crowdso

### [tool_use Bash]
{"command": "cd /home/ankur/scamtrends_feed/registry && python3 -c \"\nimport json\nd=json.load(open('spf_brands.json'))\nprint(type(d), len(d))\nitems = d if isinstance(d,list) else d.get('brands', d)\nimport re\nfor b in (items if isinstance(items,list) else items.values()):\n    s=json.dumps(b)\n    if re.search(r'grab|gojek|comfort|cdg|smrt|sbs|ez-?link|nets|sp group|charge\\+|tada|ryde|city energy|geneco|simplygo|transit', s, re.I):\n        print(s[:700]); print('--')\n\"", "description": "Look up my brands in SPF brand-tag list"}

### [tool_result]
<class 'list'> 159
{"brand_value": "SingPost", "tag_id": "955db5a1-1984-480e-8726-3ce2c4b4f6e2", "count": 5, "categories": ["Non-Banking Related Phishing"], "sample_domains": ["894144.cc", "sgposeigt.sbs", "personail.cfd", "singapost-track.info"], "sample_titles": ["Advisory: Protect Yourself from Fake SingPost Websites", "Advisory on Fake SingPost Websites and Phishing Scams"]}
--
{"brand_value": "SimplyGo", "tag_id": "74f392cc-42c6-4390-9bc6-2128c837a531", "count": 1, "categories": ["Non-Banking Related Phishing"], "sample_domains": ["se-debarrasser-des-taupes-et-taupiniere.be"], "sample_titles": ["Alert: Phishing Scams Impersonating SimplyGo Detected"]}
--
{"brand_value": "Dance Prize", "tag_id": "7616c5f8-24fc-478e-a9b7-1bbb45b7160e", "count": 1, "categories": ["Impersonation"], "sample_domains": ["votegrand.sbs"], "sample_titles": ["Advisory: Beware of Fake \"Dance Prize\" Impersonation Scams"]}
--
{"brand_value": "SP Group", "tag_id": "123eefaa-fe96-4ba4-bb83-ad97b3048c07", "count": 1, "categories": ["Non-Banking Related Phishing"], "sample_domains": ["samgirasg.com"], "sample_titles": ["Beware of Phishing Scams Impersonating SP Group"]}
--
{"brand_value": "Grab", "tag_id": "d5f00781-3f33-45f3-b7f2-436e0d433ca6", "count": 1, "categories": ["Non-Banking Related Phishing"], "sample_domains": ["grabk.vip"], "sample_titles": ["Advisory on Phishing Scams Impersonating Grab"]}
--
{"brand_value": "Charge+", "tag_id": "962cdb0c-0a5f-40f6-9fdd-58673ec40394", "count": 1, "categories": ["Investment"], "sample_domains": ["chargingpiles.autos"], "sample_titles": ["Advisory: Beware of Fake 'Charge+' Investment Schemes"]}
--

### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && cat > f.sh <<'EOF'\n#!/bin/bash\n# usage: f.sh URL OUTFILE  -- polite fetch with browser UA, 1.2s pause after\nUA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\nout=$(curl -sL -A \"$UA\" --compressed --max-time 30 -o \"$2\" -w '%{http_code} %{url_effective}' \"$1\")\necho \"$out size=$(stat -c %s \"$2\" 2>/dev/null) <- $1\"\nsleep 1.2\nEOF\nchmod +x f.sh\n./f.sh https://www.grab.com/robots.txt grab_robots.txt\n./f.sh https://www.grab.com/sg/ grab_sg_home.html\ncat grab_robots.txt | head -50", "description": "Create fetch helper; fetch Grab robots.txt and SG homepage"}

### [tool_result]
200 https://www.grab.com/robots.txt size=5788 <- https://www.grab.com/robots.txt
200 https://www.grab.com/sg/ size=471988 <- https://www.grab.com/sg/
User-agent: *

Allow: *.js
Allow: *.css

Disallow: *?faq=*

Disallow: /wp-admin/
Disallow: /sg/grab_portal/
Disallow: /sg/games/
Disallow: /sg/profile/
Disallow: /sg/grabPortal/
Disallow: /sg/fun/
Disallow: /sg/funpages/
Disallow: /sg/game_dir/
Disallow: /thank-you
Disallow: */page/*
Disallow: /grabpaymerchant/
 
Allow: /sg/wp-content/
Allow: /ph/wp-content/
Allow: /my/wp-content/
Allow: /id/wp-content/
Allow: /th/wp-content/
Allow: /vn/wp-content/
Allow: /mm/wp-content/
Allow: /wp-content/
Allow: /wp-includes/

#Sitemaps

Sitemap: https://www.grab.com/sg/sitemap.xml
Sitemap: https://www.grab.com/my/sitemap.xml
Sitemap: https://www.grab.com/ph/sitemap.xml
Sitemap: https://www.grab.com/id/sitemap.xml
Sitemap: https://www.grab.com/th/sitemap.xml
Sitemap: https://www.grab.com/vn/sitemap.xml
Sitemap: https://www.grab.com/mm/sitemap.xml
Sitemap: https://www.grab.com/kh/sitemap.xml
Sitemap: https://www.grab.com/cn/sitemap.xml
Sitemap: https://www.grab.com/global/sitemap.xml
Sitemap: https://www.grab.com/tw/sitemap.xml
Sitemap: https://www.grab.com/nextjs-sitemap/index.xml


#Duplicated URLs

Disallow: /my/blog/driver/grabcar-economy-weekly-earning-structure-klang-valley-negeri-sembilan-
Disallow: /my/blog/driver/car/grabcar-economy-weekly-earning-structure-klang-valley-negeri-sembilan-
Disallow: /my/blog/driver/grabcar-economy-weekly-earning-structure-penang-

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && sed -n 50,400p grab_robots.txt | grep -v -E '^Disallow: /(my|ph|id|th|vn|mm)/' | head -40; ./f.sh https://www.grab.com/sg/sitemap.xml grab_sg_sitemap.xml; head -c 1500 grab_sg_sitemap.xml; echo; grep -o '<loc>[^<]*</loc>' grab_sg_sitemap.xml | head -40", "description": "Show rest of Grab robots; fetch SG sitemap index"}

### [tool_result]
200 https://www.grab.com/sg/sitemap.xml size=270611 <- https://www.grab.com/sg/sitemap.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="https://www.grab.com/sg/sitemap.xsl"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<!-- Sitemap is generated on 2026-11-25 16:47:30 GMT -->
	<url>
		<loc>https://www.grab.com/sg/</loc>
		<lastmod>2026-06-29T12:24+00:00</lastmod>
		<priority>1.0</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/freecbd/</loc>
		<lastmod>2016-08-09T05:01+00:00</lastmod>
		<priority>0.9</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/grabpay-training/</loc>
		<lastmod>2016-08-09T05:01+00:00</lastmod>
		<priority>0.9</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/setting-grabtaxi-as-dbs-preferred-billing-organization/</loc>
		<lastmod>2016-08-09T05:01+00:00</lastmod>
		<priority>0.9</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/download/</loc>
		<lastmod>2026-05-11T07:23+00:00</lastmod>
		<priority>0.9</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/grabfuelterms/</loc>
		<lastmod>2016-08-09T05:02+00:00</lastmod>
		<priority>0.9</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/drive-with-grab-using-a-rental-car/</loc>
		<lastmod>2019-04-05T06:06+00:00</lastmod>
		<priority>0.9</priority>
	</url>
	<url>
		<loc>https://www.grab.com/sg/par
<loc>https://www.grab.com/sg/</loc>
<loc>https://www.grab.com/sg/freecbd/</loc>
<loc>https://www.grab.com/sg/grabpay-training/</loc>
<loc>https://www.grab.com/sg/setting-grabtaxi-as-dbs-preferred-billing-organization/</loc>
<loc>https://www.grab.com/sg/download/</loc>
<loc>https://www.grab.com/sg/grabfuelterms/</loc>
<loc>https://www.grab.com/sg/drive-with-grab-using-a-rental-car/</loc>
<loc>https://www.grab.com/sg/partnerships/</loc>
<loc>https://www.grab.com/sg/driver/transport/</loc>
<loc>https://www.grab.com/sg/grab-americanexpress/</loc>
<loc>https://www.grab.com/sg/understanding-grabchat/</loc>
<loc>https://www.grab.com/sg/unlock-sgd50-savings-grabhitch-sg-jb-5-programme/</loc>
<loc>https://www.grab.com/sg/driver/transport/taxi/</loc>
<loc>https://www.grab.com/sg/press/</loc>
<loc>https://www.grab.com/sg/privacy-policy/</loc>
<loc>https://www.grab.com/sg/gold/</loc>
<loc>https://www.grab.com/sg/whats-next-grabhitch-sg-jb/</loc>
<loc>https://www.grab.com/sg/special-national-day-incentives-map-9-august-2016/</loc>
<loc>https://www.grab.com/sg/national-day-9-august-2016-maps/</loc>
<loc>https://www.grab.com/sg/appeal/</loc>
<loc>https://www.grab.com/sg/unsubscribe/</loc>
<loc>https://www.grab.com/sg/driver/transport/sg-jb-hitch/</loc>
<loc>https://www.grab.com/sg/download/driver/</loc>
<loc>https://www.grab.com/sg/gcp12-18sep16/</loc>
<loc>https://www.grab.com/sg/brand-story/</loc>
<loc>https://www.grab.com/sg/f1-incentive-area/</loc>
<loc>https://www.grab.com/sg/gcp19_25sep16/</loc>
<loc>https://www.grab.com/sg/sentosaentry/</loc>
<loc>https://www.grab.com/sg/robo-cars-terms/</loc>
<loc>https://www.grab.com/sg/road-closure-lets-lepakmount-faber/</loc>
<loc>https://www.grab.com/sg/gcp10_16oct/</loc>
<loc>https://www.grab.com/sg/difference-grabpay-promo-jobs/</loc>
<loc>https://www.grab.com/sg/nobookingfee/</loc>
<loc>https://www.grab.com/sg/road-closure-chua-chu-kang-big-farm-walk-run-2016/</loc>
<loc>https://www.grab.com/sg/gcp24_30oct/</loc>
<loc>https://www.grab.com/sg/road-closure-notice-fire-walking-ceremony-2016/</loc>
<loc>https://www.grab.com/sg/grabwtafinalspoint/</loc>
<loc>https://www.grab.com/sg/road-closure-notice-car-free-sunday-sg-2016/</loc>
<loc>https://www.grab.com/sg/gcp31oct_6nov/</loc>
<loc>https://www.grab.com/sg/freetaxiride/</loc>

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && grep -c '<loc>' grab_sg_sitemap.xml; python3 - <<'EOF'\nimport re\ns=open('grab_sg_sitemap.xml').read()\nurls=re.findall(r'<url>\\s*<loc>([^<]*)</loc>\\s*(?:<lastmod>([^<]*)</lastmod>)?',s)\npat=re.compile(r'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect|safety|safe',re.I)\nfor u,lm in urls:\n    if pat.search(u): print(lm[:10],u)\nEOF", "description": "Grep Grab SG sitemap for scam-related URLs"}

### [tool_result]
1562
2017-06-07 https://www.grab.com/sg/safetravel/
2020-01-08 https://www.grab.com/sg/driver/transport/grabrentals/grsafetychampion/
2021-03-08 https://www.grab.com/sg/security-guide-driver/
2021-03-08 https://www.grab.com/sg/security-guide-consumer/
2018-10-15 https://www.grab.com/sg/grab-health-and-safety-carnival/
2019-01-11 https://www.grab.com/sg/bettereveryday-2018/driver/safer-rides/
2019-01-21 https://www.grab.com/sg/transport/wheels/training/safety-checklist/
2019-05-07 https://www.grab.com/sg/account-security-sg/
2019-01-24 https://www.grab.com/sg/safety-sg/
2019-05-09 https://www.grab.com/sg/keeping-your-grab-account-safe/
2019-03-07 https://www.grab.com/sg/safety/setting-the-bar/
2019-12-13 https://www.grab.com/sg/amexsecurity/
2019-07-08 https://www.grab.com/sg/driver-timeout-feature-safeguarding-responsible-delivery-partners/
2020-04-20 https://www.grab.com/sg/aiforsea/aiforsea-safety/
2025-05-27 https://www.grab.com/sg/driver/transport/rentals/gr-vehicle-damage-protection-scheme/
2024-03-14 https://www.grab.com/sg/phishing-2/
2024-03-14 https://www.grab.com/sg/how-to-avoid-scams-fraud-and-identity-theft/
2022-07-06 https://www.grab.com/sg/driver/academy/transport-grabacademy-features-safety-service-training/
2022-07-06 https://www.grab.com/sg/driver/academy/deliveries-grabacademy-features-safety-service-training/
2022-03-16 https://www.grab.com/sg/pay/stay-online-securely/
2022-03-16 https://www.grab.com/sg/pay/spot-the-fake/
2022-04-20 https://www.grab.com/sg/pay/identifying-types-of-prolific-security-issues/
2024-03-27 https://www.grab.com/sg/your-security-is-in-our-care/
2026-05-11 https://www.grab.com/sg/about/trust-and-safety/
2022-01-27 https://www.grab.com/sg/business/defence/fraud-readiness-checklist/
2022-07-28 https://www.grab.com/sg/business/defence/the-state-of-fraud-in-southeast-asia-2022-insights-for-risk-professionals/
2024-05-16 https://www.grab.com/sg/consumer/finance/security/
2022-08-01 https://www.grab.com/sg/safety-poster-drawing-competition-2022-winner-prizes-information-tcs/
2022-09-26 https://www.grab.com/sg/campaign/meet-the-super-team-protecting-your-wallet/
2022-09-15 https://www.grab.com/sg/safety-art-drawing-competition-2022-winner-prizes-tcs/
2023-03-15 https://www.grab.com/sg/driver/academy/safe-responsible-drinking-module/
2026-09-11 https://www.grab.com/sg/inside-grab/grab-conversations-data-protection-in-sea-ep-1-the-basics/
2026-09-11 https://www.grab.com/sg/inside-grab/grab-conversations-data-protection-in-sea-ep-2-thai-perspective/
2026-09-18 https://www.grab.com/sg/inside-grab/grab-conversations-data-protection-in-sea-ep-3-sg-perspective/
2026-09-11 https://www.grab.com/sg/inside-grab/grab-conversations-data-protection-in-sea-ep-4-sme-perspective/
2025-12-04 https://www.grab.com/sg/inside-grab/stories/grab-app-detects-driver-safety/
2023-03-24 https://www.grab.com/sg/safety-in-every-ride/
2023-03-31 https://www.grab.com/sg/safe-responsible-drinking-module/
2024-09-09 https://www.grab.com/sg/inside-grab/stories/this-is-the-woman-raising-the-bar-of-grabs-safety-standards/
2025-02-26 https://www.grab.com/sg/inside-grab/stories/blurring-faces-and-licence-plates-in-street-level-images-to-protect-privacy/
2025-02-26 https://www.grab.com/sg/inside-grab/stories/two-wheel-driver-partners-now-have-a-better-safety-report-in-their-apps/
2025-02-26 https://www.grab.com/sg/inside-grab/stories/grabs-in-app-speeding-alerts-are-now-harder-to-miss/
2025-12-23 https://www.grab.com/sg/inside-grab/stories/travel-safely-and-seamlessly-this-holiday-season-with-grabs-latest-travel-features/
2025-12-23 https://www.grab.com/sg/inside-grab/stories/grabdefence-anti-fraud-technology-for-southeast-asias-digital-age/
2025-02-26 https://www.grab.com/sg/inside-grab/stories/a-glimpse-into-the-cutting-edge-of-anti-fraud-research/
2025-02-26 https://www.grab.com/sg/inside-grab/stories/how-ai-raises-the-stakes-in-digital-fraud/
2026-08-26 https://www.grab.com/sg/press/others/grab-rsas-and-ndca-launch-grabacademy-ridesafe-2026-new-safety-course-designed-for-delivery-riders/
2026-05-20 https://www.grab.com/sg/press/others/grabs-commitment-to-taiwans-data-security-and-public-trust/
2026-08-26 https://www.grab.com/sg/press/others/grab-in-partnership-with-weride-officially-launch-singapores-first-autonomous-public-ride-service-in-punggol/
2025-08-15 https://www.grab.com/sg/press/others/weride-secures-strategic-equity-investment-from-grab-partners-to-deploy-robotaxis-and-autonomous-shuttles-in-southeast-asia/
2026-08-27 https://www.grab.com/sg/press/others/grab-officially-recognises-ndca-and-nphva-to-represent-platform-workers/
2023-05-25 https://www.grab.com/sg/press/others/grab-co-founder-tan-hooi-ling-to-step-down-from-official-grab-positions-by-year-end/
2023-03-17 https://www.grab.com/sg/press/others/grab-adds-audioprotect-to-its-suite-of-safety-features/
2022-11-23 https://www.grab.com/sg/enterprise-blog/grabdefence-assists-ula-in-strengthening-its-platform-against-fraud/
2022-07-06 https://www.grab.com/sg/enterprise-blog/linkaja-beef-up-its-fight-against-fraud-with-the-help-of-grabdefence/
2024-01-05 https://www.grab.com/sg/enterprise-blog/protecting-privacy-takes-precedence-with-grabmaps/
2022-05-12 https://www.grab.com/sg/press/social-impact-safety/grab-announces-three-esg-goals-for-sustainable-and-inclusive-growth/
2022-05-04 https://www.grab.com/sg/press/others/grab-singapore-is-the-first-superapp-to-secure-data-protection-trustmark-certification-by-imda/
2024-01-05 https://www.grab.com/sg/enterprise-blog/grabmaps-uses-geofencing-for-efficient-navigation-and-keeps-driver-partners-safe/
2022-02-16 https://www.grab.com/sg/press/social-impact-safety/grab-and-secura-partner-to-offer-security-training-courses-and-job-opportunities-in-security-services-for-up-to-200-driver-and-delivery-partners/
2022-01-25 https://www.grab.com/sg/enterprise-blog/whos-driving-grabdefences-fight-against-fraud/
2022-01-21 https://www.grab.com/sg/enterprise-blog/the-new-faces-of-fraud-in-sout

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && for p in phishing-2 how-to-avoid-scams-fraud-and-identity-theft pay/spot-the-fake your-security-is-in-our-care about/trust-and-safety consumer/finance/security; do n=$(echo $p | tr '/' '_'); ./f.sh \"https://www.grab.com/sg/$p/\" \"grab_$n.html\"; done; ./f.sh https://www.grab.com/nextjs-sitemap/index.xml grab_nextjs_index.xml; head -c 2000 grab_nextjs_index.xml", "description": "Fetch Grab SG scam/security candidate pages and nextjs sitemap index"}

### [tool_result]
200 https://www.grab.com/sg/phishing-2/ size=243349 <- https://www.grab.com/sg/phishing-2/
200 https://www.grab.com/sg/how-to-avoid-scams-fraud-and-identity-theft/ size=244939 <- https://www.grab.com/sg/how-to-avoid-scams-fraud-and-identity-theft/
200 https://www.grab.com/sg/pay/spot-the-fake/ size=232660 <- https://www.grab.com/sg/pay/spot-the-fake/
200 https://www.grab.com/sg/your-security-is-in-our-care/ size=218286 <- https://www.grab.com/sg/your-security-is-in-our-care/
200 https://www.grab.com/sg/about/trust-and-safety/ size=234018 <- https://www.grab.com/sg/about/trust-and-safety/
200 https://www.grab.com/sg/consumer/finance/security/ size=225879 <- https://www.grab.com/sg/consumer/finance/security/
200 https://www.grab.com/nextjs-sitemap/index.xml size=958 <- https://www.grab.com/nextjs-sitemap/index.xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/sg.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/vn.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/id.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/th.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/ph.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/mm.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/kh.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/my.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/cn.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.grab.com/nextjs-sitemap/global.xml</loc>
  </sitemap>
</sitemapindex>

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && python3 -c \"import bs4, lxml; print('bs4 ok')\" 2>&1; python3 -c \"import trafilatura; print('traf ok')\" 2>&1 | tail -1; cat > tx.py <<'EOF'\n#!/usr/bin/env python3\n# usage: tx.py FILE [maxchars]  -> visible text (scripts/styles/nav/footer removed)\nimport sys, re, html\ns = open(sys.argv[1], encoding='utf-8', errors='replace').read()\nmx = int(sys.argv[2]) if len(sys.argv) > 2 else 6000\ntry:\n    from bs4 import BeautifulSoup\n    soup = BeautifulSoup(s, 'lxml')\n    for t in soup(['script', 'style', 'noscript', 'svg', 'header', 'nav', 'footer']):\n        t.decompose()\n    txt = soup.get_text('\\n')\nexcept Exception:\n    txt = re.sub(r'(?is)<(script|style|noscript).*?</\\1>', ' ', s)\n    txt = html.unescape(re.sub(r'<[^>]+>', '\\n', txt))\nlines = [re.sub(r'\\s+', ' ', l).strip() for l in txt.split('\\n')]\nout = '\\n'.join(l for l in lines if l)\nprint(out[:mx])\nEOF\nchmod +x tx.py; ./tx.py grab_phishing-2.html 4000", "description": "Create text extractor; read Grab phishing page"}

### [tool_result]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'bs4'
ModuleNotFoundError: No module named 'trafilatura'
Learn about phishing and legitimate communications​ | Grab SG
Menu
About
Consumer
Driver
Merchant
Enterprise
About Us
Who we are and what we stand for
Inside Grab
News and stories from our official blog
Investor Relations
Information for our investors
Locations
Cities and countries we call home
Sustainability
How we deliver impact to the communities we serve
Newsroom
Latest news and announcements, fresh off the press
Grab Financial Group
Financial services that are accessible and affordable to all
Careers
Join us on our mission to drive Southeast Asia forward
GrabForGood Fund
Our endowment fund empowering the communities of Southeast Asia
Airport Guides
Travel portal provides useful guides to over 442 airports in southeast Asia
Rides
Everything to do with getting you from A to B
GrabFood
Everyday food options for every occasion
GrabMart
Find everything you need
GrabExpress
Send things easily and quickly
Grab DineOut
Discover restaurants, book tables and save with deals
GrabCoins
Exclusive privileges you'll enjoy as a Grab user
GrabGifts
Give the Gift of Grab! Practical gifts don’t have to be boring
Financial services
Simple financial products tailored for consumers
Grab For Family
Now you can track and pay for family's rides
GrabExec Limo
Your seamless and luxurious rides in Singapore
Experiences
Find Your Next Adventure in Singapore with Grab Culinary Tours.
Help Centre
Get help on account issues, job issues, accident & safety, earnings & wallet
What's New
Latest news and announcements for Grab Driver-partners
Drive with us
Be your own boss and drive on your own time
Deliver with us
Earn extra income as you help deliver food and items on-demand
Financial services
Simple financial products tailored for driver-partners
Driver Centre
Find your nearest driver centre
GrabAcademy
The one-stop to your training needs, through every phase of your partnership with us.
Help Centre
Get help on account issues, app issues issues, and more.
What's New
Latest news and announcements for Grab Merchant-partners
Partner with us
Start your journey as a merchant-partner and reach millions of consumers
Financial services
Flexible financial solutions to help you grow
Financial resources
Funding and resources for merchant-partners
GrabExpress
An on-demand delivery service that fulfils your customers’ orders seamlessly
Grab DineOut
Partner with us for Dine Out Deals, Reservations, Loyalty Solutions and more
What’s New
Latest news and announcements for Grab Enterprise partners
Grab for Business
Grab services catered to your business needs
GrabAds
Take advantage of our exposure, online-to-offline
GrabGifts
Customise Grab vouchers for your customers, guests and employees
GrabFinance
Easy access to funding for business goals
GrabExpress
Book and manage package deliveries for your company
GrabDefence
Protect your mobile app from fraud
GrabMaps
Hyperlocal mapping technology and location data solutions for businesses
Grab Singapore
GrabX
Be Our Partner
Grab Driver
Food Delivery Driver
Express Delivery Driver
Food / Mart Merchant
Pay Merchant
Help Centre
GrabX
Be Our Partner
Grab Driver
Food Delivery Driver
Express Delivery Driver
Food / Mart Merchant
Pay Merchant
Help Centre
About
About Us
Inside Grab
Investor Relations
Locations
Sustainability
Newsroom
Grab Financial Group
Careers
GrabForGood Fund
Consumer
Airport Guides
Rides
GrabFood
GrabMart
GrabExpress
Grab DineOut
GrabCoins
GrabGifts
Financial services
Grab For Family
GrabExec Limo
Experiences
Driver
Help Centre
What's New
Drive with us
Deliver with us
Financial services
Driver Centre
GrabAcademy
Merchant
Help Centre
What's New
Partner with us
Financial services
Financial resources
GrabExpress
Grab DineOut
Enterprise
What’s New
Grab for Business
GrabAds
GrabGifts
GrabFinance
GrabExpress
GrabDefence
GrabMaps
Grab Singapore
Phishing is a popular form of cyberattack that attempts to steal your money, or your identity, by getting you to reveal personal information - such as credit card numbers, bank inform

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && cat > tx.py <<'EOF'\n#!/usr/bin/env python3\n# usage: tx.py FILE [maxchars] [startmarker] -> visible text, skipping script/style/nav/header/footer\nimport sys, re\nfrom html.parser import HTMLParser\nSKIP = {'script', 'style', 'noscript', 'svg', 'nav', 'header', 'footer', 'template', 'iframe'}\nVOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}\nclass P(HTMLParser):\n    def __init__(self):\n        super().__init__(convert_charrefs=True); self.skip = 0; self.out = []; self.stack = []\n    def handle_starttag(self, tag, attrs):\n        if tag in VOID: return\n        self.stack.append(tag)\n        if tag in SKIP: self.skip += 1\n        if tag in ('p','div','li','h1','h2','h3','h4','tr','br','section','article'): self.out.append('\\n')\n    def handle_endtag(self, tag):\n        if tag in VOID: return\n        # pop to matching tag\n        if tag in self.stack:\n            while self.stack:\n                t = self.stack.pop()\n                if t in SKIP: self.skip -= 1\n                if t == tag: break\n        if tag in ('p','div','li','h1','h2','h3','h4','tr'): self.out.append('\\n')\n    def handle_data(self, d):\n        if self.skip <= 0: self.out.append(d)\ns = open(sys.argv[1], encoding='utf-8', errors='replace').read()\np = P(); p.feed(s)\ntxt = ''.join(p.out)\nlines = [re.sub(r'\\s+', ' ', l).strip() for l in txt.split('\\n')]\nout = '\\n'.join(l for l in lines if l)\nmx = int(sys.argv[2]) if len(sys.argv) > 2 else 6000\nif len(sys.argv) > 3 and sys.argv[3] in out:\n    out = out[out.index(sys.argv[3]):]\nprint(out[:mx])\nEOF\n./tx.py grab_phishing-2.html 6000 \"Phishing is a popular\"", "description": "Improve text extractor; read Grab phishing page content"}

### [tool_result]
Phishing is a popular form of cyberattack that attempts to steal your money, or your identity, by getting you to reveal personal information - such as credit card numbers, bank information, or passwords - on websites that pretend to be legitimate.
We feel the best defence is awareness and knowing what to look for. So, here are six ways to recognise a potential phishing scam:
Spelling and bad grammar
Legitimate companies and organisations usually have an editorial team to ensure customers receive high-quality, professional content. If an email message has glaring spelling or grammatical errors, it might be a scam.
Urgent call to action or threats
Be wary of emails that claim you must click, call, or open an attachment immediately. By pressuring you to reply quickly, cybercriminals hope to instil panic and fear to trick you into providing confidential information. Creating a false sense of urgency is a common trick of phishing attacks and scams.
Promise of attractive rewards
False offers of amazing deals or unbelievable prizes are commonly used by cyber criminals to encourage you to act immediately. Don’t let curiosity get the better of you and pull you into the scam!
Mismatched and misleading domains
Cyber criminals will attempt to mislead you into believing that the information you see is genuine. Check the email content properly. Inspect if the information, such as email address, message body, or links, are inconsistent or misspelt.
Pro Tip:
Be vigilant! Cybercriminals can also tempt you to visit fake websites with other methods, such as text messages or phone calls. Sophisticatedcybercriminals set up call centres to automatically dial or text numbers for potential targets.
Suspicious links or unexpected attachments
Attachments included in emails are a way to infect a user’s device with malware and steal their data. If you suspect that an email message is a scam, don’t open any links or attachments that you see. It is important to exercise caution.
Unexpected or first time senders
While it’s not unusual to receive an email from someone for the first time, especially if they are outside your organisation, this can be a sign of phishing. If you receive such an email, take a moment to examine it extra carefully before you proceed, do not click on the links and attachments and delete the email immediately if you feel something is amiss.
What should I do if I receive a phishing message?
Disconnect immediately and share the fraud number with us by calling our helpline.
Call us immediately if you have mistakenly revealed your OTP details to someone.
If you get a SMS/call asking for sensitive information, do not provide these details.
Don’t open or forward these suspicious links via email, SMS or chat.
What should I do if I've been phished?
If you have shared your credit/debit card information with a suspected fraudster, please block your card immediately by contacting your bank or through Grab app for GrabPay Card and lodge a police report for further investigation.
If you have shared your Grab app login credentials or suspect any irregular activities/charges from your account, please reset the password or GrabPIN and report it to us here.
Read other articles.
Spot the fake… website
Spotting a fake website is the first line of protection against cyberattacks. Learn the tell-tale signs now.
Learn more
Protect before you connect
It’s not an if, but a when you will be subject to a cyberattack. Find out four ways to beat these threats.
Learn more
Grab Singapore
Forward Together
3 Media Close,
Singapore 138498
Follow us and keep updated!
Singapore
Singapore
Malaysia
Indonesia
Thailand
Vietnam
Philippines
Myanmar
Cambodia
About
About Us
Inside Grab
Investor Relations
Locations
Sustainability
Newsroom
Grab Financial Group
Careers
GrabForGood Fund
Consumer
Airport Guides
Rides
GrabFood
GrabMart
GrabExpress
Grab DineOut
GrabCoins
GrabGifts
Financial services
Grab For Family
What's New
GrabExec Limo
Experiences
Driver
Help Centre
What's New
Drive with us
Deliver with us
Financial services
Driver Centre
GrabAcademy
Merchant
Help Centre
What's New
Partner with us
Financial services
Financial resources
GrabExpress
Grab DineOut
Payment Solutions
Enterprise
What's New
Grab for Business
GrabAds
GrabGifts
GrabFinance
GrabExpress
GrabDefence
GrabMaps
Business Delivery Service
Quick Links
Help Centre
Food Menu
Developer Portal
Tech Blog
Komsan Chiyadis
GrabFood delivery-partner, Thailand
Komsan Chiyadis
GrabFood delivery-partner, Thailand
COVID-19 has dealt an unprecedented blow to the tourism industry, affecting the livelihoods of millions of workers. One of them was Komsan, an assistant chef in a luxury hotel based in the Srinakarin area.
As the number of tourists at the hotel plunged, he decided to sign up as a GrabFood delivery-partner to earn an alternative income. Soon after, the hotel ceased operations.
Komsan has viewed this change through an optimistic lens, calling it the perfect opportunity for him to embark on a fresh journey after his previous job. Aside from GrabFood deliveries, he now also picks up GrabExpress jobs. It can get tiring, having to shuttle between different locations, but Komsan finds it exciting. And mostly, he’s glad to get his income back on track.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && for f in grab_how-to-avoid-scams-fraud-and-identity-theft grab_pay_spot-the-fake; do echo \"=== $f\"; grep -o '<title>[^<]*' $f.html; ./tx.py $f.html 100000 | awk '/^Grab Singapore$/{c++} c>=1' | sed -n '2,200p' | sed '/^Grab Singapore$/q' | head -90; done", "description": "Read Grab scam-avoidance and spot-the-fake pages"}

### [tool_result]
=== grab_how-to-avoid-scams-fraud-and-identity-theft
<title>
Forward Together
3 Media Close,
Singapore 138498
Follow us and keep updated!
Singapore
Singapore
Malaysia
Indonesia
Thailand
Vietnam
Philippines
Myanmar
Cambodia
About
About Us
Inside Grab
Investor Relations
Locations
Sustainability
Newsroom
Grab Financial Group
Careers
GrabForGood Fund
Consumer
Airport Guides
Rides
GrabFood
GrabMart
GrabExpress
Grab DineOut
GrabCoins
GrabGifts
Financial services
Grab For Family
What's New
GrabExec Limo
Experiences
Driver
Help Centre
What's New
Drive with us
Deliver with us
Financial services
Driver Centre
GrabAcademy
Merchant
Help Centre
What's New
Partner with us
Financial services
Financial resources
GrabExpress
Grab DineOut
Payment Solutions
Enterprise
What's New
Grab for Business
GrabAds
GrabGifts
GrabFinance
GrabExpress
GrabDefence
GrabMaps
Business Delivery Service
Quick Links
Help Centre
Food Menu
Developer Portal
Tech Blog
Komsan Chiyadis
GrabFood delivery-partner, Thailand
Komsan Chiyadis
GrabFood delivery-partner, Thailand
COVID-19 has dealt an unprecedented blow to the tourism industry, affecting the livelihoods of millions of workers. One of them was Komsan, an assistant chef in a luxury hotel based in the Srinakarin area.
As the number of tourists at the hotel plunged, he decided to sign up as a GrabFood delivery-partner to earn an alternative income. Soon after, the hotel ceased operations.
Komsan has viewed this change through an optimistic lens, calling it the perfect opportunity for him to embark on a fresh journey after his previous job. Aside from GrabFood deliveries, he now also picks up GrabExpress jobs. It can get tiring, having to shuttle between different locations, but Komsan finds it exciting. And mostly, he’s glad to get his income back on track.
=== grab_pay_spot-the-fake
<title>
Forward Together
3 Media Close,
Singapore 138498
Follow us and keep updated!
Singapore
Singapore
Malaysia
Indonesia
Thailand
Vietnam
Philippines
Myanmar
Cambodia
About
About Us
Inside Grab
Investor Relations
Locations
Sustainability
Newsroom
Grab Financial Group
Careers
GrabForGood Fund
Consumer
Airport Guides
Rides
GrabFood
GrabMart
GrabExpress
Grab DineOut
GrabCoins
GrabGifts
Financial services
Grab For Family
What's New
GrabExec Limo
Experiences
Driver
Help Centre
What's New
Drive with us
Deliver with us
Financial services
Driver Centre
GrabAcademy
Merchant
Help Centre
What's New
Partner with us
Financial services
Financial resources
GrabExpress
Grab DineOut
Payment Solutions
Enterprise
What's New
Grab for Business
GrabAds
GrabGifts
GrabFinance
GrabExpress
GrabDefence
GrabMaps
Business Delivery Service
Quick Links
Help Centre
Food Menu
Developer Portal
Tech Blog
Komsan Chiyadis
GrabFood delivery-partner, Thailand
Komsan Chiyadis
GrabFood delivery-partner, Thailand
COVID-19 has dealt an unprecedented blow to the tourism industry, affecting the livelihoods of millions of workers. One of them was Komsan, an assistant chef in a luxury hotel based in the Srinakarin area.
As the number of tourists at the hotel plunged, he decided to sign up as a GrabFood delivery-partner to earn an alternative income. Soon after, the hotel ceased operations.
Komsan has viewed this change through an optimistic lens, calling it the perfect opportunity for him to embark on a fresh journey after his previous job. Aside from GrabFood deliveries, he now also picks up GrabExpress jobs. It can get tiring, having to shuttle between different locations, but Komsan finds it exciting. And mostly, he’s glad to get his income back on track.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && cat > gx.sh <<'EOF'\n#!/bin/bash\n# Grab page main content: between nav end and footer\n./tx.py \"$1\" 400000 | python3 -c \"\nimport sys\nt=sys.stdin.read()\nend=t.find('Forward Together')\nhead=t[:end] if end>0 else t\nk=head.rfind('GrabMaps\\nGrab Singapore\\n')\nprint(head[k+len('GrabMaps\\nGrab Singapore\\n'):][:int(sys.argv[1])] if k>=0 else head[:int(sys.argv[1])])\n\" \"${2:-5000}\"\nEOF\nchmod +x gx.sh; for f in grab_how-to-avoid-scams-fraud-and-identity-theft grab_pay_spot-the-fake; do echo \"=== $f\"; python3 -c \"import re,sys;s=open('$f.html').read();m=re.search(r'<title>(.*?)</title>',s,re.S);print(m.group(1).strip() if m else None)\"; ./gx.sh $f.html 4500; done", "description": "Extract main content of Grab scam pages"}

### [tool_result]
=== grab_how-to-avoid-scams-fraud-and-identity-theft
How to avoid financial scams, fraud and theft | Grab SG
How to avoid financial scams, fraud and theft | Grab SG
Scams and fraud are unfortunate hazards of the digital age and they are getting increasingly sophisticated in their attempts to get your money or personal details.
When you know how to spot scams, you know how to protect yourself. Here are 8 things you can do to keep fraudsters at bay:
Never share your One Time Password (OTP)
Your One Time Password (OTP) is the first line of defence against potential fraudsters. Never share your OTP with anyone under any circumstances.
Do subscribe to instant alerts and notifications — it can be annoying at times, but it is important.
Choose passwords carefully and update regularly
Create passwords that are at least 8 characters long and that include a mix of lower and upper case letters, numbers and special characters.
Ideally, you should create a unique password for every account. That way, one data breach won’t put all your accounts at risk.
Never share your Reset password link
Your reset password link is a powerful tool for fraudsters who have secured your email ID through nefarious means like phishing. Please ensure the security questions for your account are strong and consistent.
A strong password is useless if a fraudster can answer all your security questions after a quick trip to your social media accounts.
Avoid opening suspicious text, pop-up windows or emails
Cybercriminals typically pretend to be reputable companies, friends, or acquaintances in a fake message, which contains a link to a phishing website.
Do not open suspicious text, pop-up windows or click on links or attachments in emails – just delete them.
Don’t make financial transactions on open public networks
Free isn’t necessarily better! Most public hotspots in public areas like airports, hotels and restaurants lower their security standards so it becomes easier for guests and travellers to access and use these networks.
Don’t shop with unfamiliar online retailers
When it comes to e-commerce, shop preferably with familiar companies. If you’re interested in purchasing a product from an unfamiliar retailer, do some research to ensure the business is legit and trustworthy.
Be wary of unusual payment requests
When you accept a credit card purchase, there is a possibility that the card or card information was stolen and is now being used for fraud. The fraudster can keep racking up charges until the true cardholder notices the unusual activity and disputes the transactions with their bank.
Pro Tip:
Review your monthly credit card statements
You should always be scanning your accounts for fraudulent activity and keeping track of your balance. It’s a good financial practice to monitor your credit card transactions regularly, and it’s easy to do whether you receive paper or digital statements.
Use apps wisely
If you use mobile apps on your smartphone to access your financial accounts, be sure to password-protect your device!
Every time you download apps or files from an unknown source, you risk loading malicious programs on your phone. Only download legitimate and credible apps from the Google Play Store and Apple Store.
Read other articles.
Fight the phish
Here are six ways to recognise a potential phishing scam and protect yourself from such an cyberattack.
Learn more
Spot the fake… website
Spotting a fake website is the first line of protection against cyberattacks. Learn the tell-tale signs now.
Learn more
Grab Singapore

=== grab_pay_spot-the-fake
Spot the fake website | Grab SG
Spot the fake website | Grab SG
In this digital age, knowing how to spot fake websites is not just helpful; it’s the key to protecting yourself online – everything from your personal identity, your financial information and logins for your email and social media.
Here are some tell-tale signs of a fake website:
Check if the URL is misspelled
One key indicator of a fake site is a misspelled URL. Fraudsters may change up a URL name slightly, like using Go0gle.com, or they may change the domain extension — like google.org instead of google.com.
Look out for
the lock
The padlock usually means that information on a site is encrypted, and browsers will consider it secure. If the address of the webpage where you submit information is unsecured – meaning it does not start with “http://” and the padlock symbol is missing from the status bar, close the page immediately.
Look beyond
the lock
There should be a padlock icon on the URL bar at the top left of your browser window. If it’s not there, it’s not a secure site and you should not provide your personal or financial details. You should also check the payment options at checkout stage to see if it has a trust seal – this symbol means the payment and brand are legitimate, and safe to do business with.
Use website
checker
When in doubt, use a website checker to verify if a website is secure. Alternatively, do a quick search on Google and you will be able to see reviews on the website searched.
Additional ways to verify a website
Besides checking for misspellings, padlocks and running the URL through a website checker, also look for the following trust indicators on a site:
A privacy policy
A return policy
Contact information for the business, like a phone number and address
What to do if you stumble upon a fraudulent website?
Report the fake site to Google Safe Browsing and leave it right away.
Do not provide any sensitive information like financial details, a login and password, verification codes, a Facebook login, or even your name and contact information.
Do not click on links from unfamiliar emails, online posts, or DMs.
Read other articles.
Protect before you connect
It’s not an if, but a when you will be subject to a cyberattack. Find out four ways to beat these threats.
Learn more
Stay online securely, we’re on guard
With the rise of ecommerce, online security is more important than ever. Explore ho

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && for f in grab_your-security-is-in-our-care grab_about_trust-and-safety grab_consumer_finance_security; do echo \"=== $f\"; python3 -c \"import re,sys;s=open('$f.html').read();m=re.search(r'<title>(.*?)</title>',s,re.S);print(m.group(1).strip() if m else None)\"; ./gx.sh $f.html 3500; done", "description": "Read Grab security/trust-and-safety pages"}

### [tool_result]
=== grab_your-security-is-in-our-care
Your security is in our care | Grab SG
Your security is in our care | Grab SG
You wouldn’t use a weak door lock to keep your home safe.
Likewise, you should secure your digital assets and accounts properly. It definitely is better to be cyber safe than sorry!
Here at Grab, your security is our priority.
Here are 3 simple things you can do to help us:
Your contact information, updated
Keep your personal details up-to-date on our Grab app so that we are able to contact you should we detect any suspicious activity or fraudulent transactions. Your account is protected with a 24/7 fraud detection engine so you can ride, dine, shop and pay, worry-free.
Set strong passwords
Choose passwords that would be difficult for others to guess and update them regularly. A strong password should include a mix of upper and lower case letters, numbers and symbols. Don’t use the same password for every account/profile, and don’t share your passwords with anyone.
Enable your push alerts
Enable push notifications from your Grab app. It definitely helps give you real-time updates on every transaction made so that you are aware and always in control of your privacy and account.
We are always here to help
We monitor your account activity to identify fraudulent activities. Beyond that, our support team is just a phone call away, 24/7! Alternatively, visit our Help Center to learn more about GrabPay and instantly find solutions to your concerns.
Remember:
Protect your wallet with GrabPIN so that only you can access your funds.
You can also secure your account with our biometrics payment features. Simply enable fingerprint scanning authentication on Android devices or Face ID authentication on iOS.
Read other articles.
Beat the scammers: How to avoid scams, fraud and identity theft
We simplify online security for you. Discover the eight things you can do to keep fraudsters at bay.
Learn more
Why is verifying your account and setting up GrabPIN important
GrabPIN and biometrics adds an additional layer of authentication to access your funds
Learn more
Grab Singapore

=== grab_about_trust-and-safety
Trust and Safety | Grab SG
Trust and Safety | Grab SG
A safer everyday for everyone
Grab’s ambition is to build a trusted and secure marketplace where entrepreneurs and consumers can participate and thrive with peace of mind. As millions continue to rely on us daily, safety remains our top priority.
You control who sees your information
Our app and backend systems employ best-in-class security frameworks that guard users’ accounts, transaction data, e-wallet, and private information.
GrabPIN second-factor authentication
Users are asked to key in their GrabPIN when accessing sensitive information in their GrabPay Wallet, or if suspicious activity is detected.
Security email alerts
Alerts are sent to the email address on the user's account when a device change is detected or a new social account is linked.
Banning of modified devices
For greater account security, those accessing their Grab account with modified devices are unable to login to their Grab driver account.
Fairplay programme
Grab FairPlay programme is a platform where Grab users are incentivised for reporting any fraudulent activities within the Grab community.
Safe Communications
Your identity and personal information are protected across all communication channels - GrabChat, VOIP Calls, and Direct Calls (number masking).
1/5
GrabPIN second-factor authentication
Users are asked to key in their GrabPIN when accessing sensitive information in their GrabPay Wallet, or if suspicious activity is detected.
2/5
Security email alerts
Alerts are sent to the email address on the user's account when a device change is detected or a new social account is linked.
3/5
Banning of modified devices
For greater account security, those accessing their Grab account with modified devices are unable to login to their Grab driver account.
4/5
Fairplay programme
Grab FairPlay programme is a platform where Grab users are incentivised for reporting any fraudulent activities within the Grab community.
Your every transaction is protected
Every payment and transaction made is valuable. Our app features are continually strengthened and protected by the latest technology and stringent processes, so users can do what they need with peace of mind.
End-to-end encryption
All personal information and payment transactions are encrypted and protected with a 24/7 fraud detection engine.
Verification through biometrics
You can enable fingerprint scanning authentication on Android devices or Face ID authentication on iOS.
Lock your card instantly
Instantly block a lost or misplaced GrabPay Card from within the Grab app.
Industry-acclaimed standards
GrabPay is PCI DSS level 1 compliant, which is the highest standard of security for payments. We apply the most stringent standards when storing, transmitting, and processing your data.
1/4
End-to-end encryption
All personal information and payment transactions are encrypted and protected with a 24/7 fraud detection engine.
2/4
Verification through biometrics
You can enable fingerprint scanning authentication on Android devices or Face ID authentication on iOS.
3/4
Lock your card instantly
Instantly block a lost or misplaced GrabPay Card from within the Grab app.
4/4
Industry-acclaimed standards
GrabPay is PCI DSS level 1 compliant, which is the highest standard of security for payments. We apply the most stringent standards when storing, transmitting, and processing your data.
A safer on-ground experience for all
No consumer or partner should have to feel unsafe while using any of our services. G
=== grab_consumer_finance_security
Security | Grab SG
Security | Grab SG
Customer
Safeguarding your wallet
Security with every payment
Security with every payment
Download the Grab app
Download the Grab app
Your wallet is in safe hands
Whether it's paying for a meal, topping up your wallet or paying for online shopping in insta

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [tool_use WebSearch]
{"query": "Grab Singapore scam advisory official SMS sender ID \"Grab\" will never ask", "mode": "standard"}

### [tool_use WebSearch]
{"query": "site:help.grab.com scam phishing Singapore", "mode": "standard"}

### [tool_result]
Web search results for query: "site:help.grab.com scam phishing Singapore"

Links: [{"title":"stay vigilant and safeguard your business from scams","url":"https://merchant.grab.com/en-sg/blog/stay-vigilant-and-safeguard-your-business-from-scams"},{"title":"phishing 2","url":"https://www.grab.com/sg/phishing-2/"},{"title":"grabs help centre asks customer to redeem fake voucher that police later flagged as phishing scam","url":"https://theindependent.sg/grabs-help-centre-asks-customer-to-redeem-fake-voucher-that-police-later-flagged-as-phishing-scam/"},{"title":"20201028 police advisory phishing scams involving fake grab ads and other fake deals","url":"https://www.police.gov.sg/media-room/news/20201028_police_advisory_phishing_scams_involving_fake_grab_ads_and_other_fake_deals"},{"title":"theindependent.sg","url":"https://theindependent.sg/?p=410240"},{"title":"20201028 police advisory phishing scams involving fake grab ads and other fake deals","url":"https://police.gov.sg/Media-Room/News/20201028_police_advisory_phishing_scams_involving_fake_grab_ads_and_other_fake_deals"},{"title":"theindependent.sg","url":"https://theindependent.sg/?p=410241"},{"title":"Learn about phishing and legitimate communications","url":"https://grab.com/ph/pay/security/phishing"},{"title":"PR Asia 2025 Singapore","url":"https://www.marketing-interactive.com/grab-removes-payment-on-gaming-sites-users-lodge-police-report-over-unauthorised-transactions"},{"title":"Watch out for suspicious emails, texts or calls that ask for your personal info","url":"https://www.grab.com/sg/keeping-your-grab-account-safe/"},{"title":"www.grab.com","url":"https://www.grab.com/sg/wp-json/wp/v2/editorial/228892"},{"title":"Anti-Phishing Tips: Guidelines on Data Protection","url":"https://www.grab.com/ph/merchant-blog/anti-phishing-tips/"},{"title":"Posted on Apr 10","url":"https://merchant.grab.com/en-my/blog/security-reminder-never-share-personal-information-and-grab-account-details"},{"title":"New variant of phishing scam in Singapore fakes Grab advertisements","url":"https://www.thestar.com.my/aseanplus/aseanplus-news/2020/10/29/new-variant-of-phishing-scam-in-singapore-fakes-grab-advertisements"},{"title":"Posted on Sep 2","url":"https://mrc2022.grab.com/blog/important-beware-of-escalating-scam-activities"},{"title":"www.grab.com","url":"https://www.grab.com/sg/wp-json/wp/v2/editorial/225572"},{"title":"20251127 four men to be charged for cheating involving fraudulent grab claims","url":"https://www.police.gov.sg/media-hub/news/2025/11/20251127_four_men_to_be_charged_for_cheating_involving_fraudulent_grab_claims"}]

I've performed the web search for your query. Here are the key findings:

## Phishing and Scam Information from Grab Help Resources

Grab advises users to double-check emails from Grab, as all legitimate emails end with @grab.com or @grabtaxi.com, and to watch out for subtle misspellings like @garb.com.

All legitimate Grab websites will always contain grab.com in the domain.

## Types of Phishing Scams in Singapore

A phishing scam variant involving fake Grab advertisements surfaced in Singapore, where victims clicking on fake Grab ads on Facebook or Instagram are directed to fake Grab websites asking for their mobile phone numbers and OTP.

The majority of transactions resulting from this scam variant were purchases of game credits on gaming websites.

## What to Do If Affected

If scammed, contact your bank immediately, file a police report online or in person at the nearest Neighbourhood Police Centre, or call 999 for urgent assistance.

## Security Tips

Phishing sites often use URLs that look correct but contain common misspellings or characters before or after the company name (e.g., www.gra8.com instead of www.grab.com). A reputable company will never ask for your password or PIN via phone or email; if they need you to reset your password, they'll send a link to a secure page on their official site.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_result]
Web search results for query: "Grab Singapore scam advisory official SMS sender ID "Grab" will never ask"

Links: [{"title":"stay vigilant and safeguard your business from scams","url":"https://merchant.grab.com/en-sg/blog/stay-vigilant-and-safeguard-your-business-from-scams"},{"title":"20201028 police advisory phishing scams involving fake grab ads and other fake deals","url":"https://www.police.gov.sg/media-room/news/20201028_police_advisory_phishing_scams_involving_fake_grab_ads_and_other_fake_deals"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://www.police.gov.sg/media-hub/news/2022/10/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"20201028 police advisory phishing scams involving fake grab ads and other fake deals","url":"https://police.gov.sg/Media-Room/News/20201028_police_advisory_phishing_scams_involving_fake_grab_ads_and_other_fake_deals"},{"title":"Scam Advisory","url":"https://www.msf.gov.sg/scam-advisory"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://www.police.gov.sg/media-hub/news/2022/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://www.police.gov.sg/Media-Hub/News/2022/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://police.gov.sg/Media-Room/News/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"20241219 police advisory on phishing scams and usage of online messaging channels","url":"https://www.police.gov.sg/media-hub/news/2024/20241219_police_advisory_on_phishing_scams_and_usage_of_online_messaging_channels"},{"title":"20220131 police advisory on scam messages circulating via sms","url":"https://www.police.gov.sg/media-hub/news/2022/01/20220131_police_advisory_on_scam_messages_circulating_via_sms"},{"title":"20260210 police advisory on phishing scams targeting singaporean travellers to malaysia","url":"https://www.police.gov.sg/media-hub/news/2026/02/20260210_police_advisory_on_phishing_scams_targeting_singaporean_travellers_to_malaysia"},{"title":"20260210 police advisory on phishing scams targeting singaporean travellers to malaysia","url":"https://www.police.gov.sg/Media-Hub/News/2026/02/20260210_police_advisory_on_phishing_scams_targeting_singaporean_travellers_to_malaysia"},{"title":"20241219 police advisory on phishing scams and usage of online messaging channels","url":"https://www.police.gov.sg/media-room/news/20241219_police_advisory_on_phishing_scams_and_usage_of_online_messaging_channels"},{"title":"Posted on Apr 10","url":"https://merchant.grab.com/en-my/blog/security-reminder-never-share-personal-information-and-grab-account-details"},{"title":"20240920 police advisory on phishing scams and usage of online messaging channels","url":"https://www.police.gov.sg/media-hub/news/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging_channels"},{"title":"Advisory on phishing scams and good cybersecurity practices","url":"https://www.singaporeair.com/en_UK/ch/corporate/newsroom/newsalert-listing/advisory-on-phishing-scams-and-good-cybersecurity-practice/"},{"title":"cpib.gov.sg","url":"https://cpib.gov.sg/advisory"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://www.police.gov.sg/media-hub/news/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"},{"title":"20240920 police advisory on phishing scams and usage of online messaging","url":"https://www.police.gov.sg/Media-Hub/News/2024/20240920_police_advisory_on_phishing_scams_and_usage_of_online_messaging"}]

Let me search more specifically for Grab's official scam advisory and SMS sender ID information:

Links: [{"title":"20221002 advisory on phishing scams involving singpass","url":"https://www.police.gov.sg/media-hub/news/2022/10/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"What you need to know: gov.sg SMS Sender ID","url":"https://www.gov.sg/explainers/what-you-need-to-know-gov-sg-sms-sender-id/"},{"title":"What you need to know: gov.sg SMS Sender ID","url":"https://www.gov.sg/article/what-you-need-to-know-govsg-sms-sender-id"},{"title":"www.reach.gov.sg","url":"https://www.reach.gov.sg/Read"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://www.police.gov.sg/Media-Hub/News/2022/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"Scam Advisory","url":"https://www.msf.gov.sg/scam-advisory"},{"title":"20260210 police advisory on phishing scams targeting singaporean travellers to malaysia","url":"https://www.police.gov.sg/media-hub/news/2026/02/20260210_police_advisory_on_phishing_scams_targeting_singaporean_travellers_to_malaysia"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://www.police.gov.sg/media-hub/news/2022/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"20221002 advisory on phishing scams involving singpass","url":"https://police.gov.sg/Media-Room/News/20221002_advisory_on_phishing_scams_involving_singpass"},{"title":"Enhanced measures against scam SMS","url":"https://imda.gov.sg/Content-and-News/Press-Releases-and-Speeches/Press-Releases/2023/Enhanced-measures-against-scam-SMS"},{"title":"A Singapore Government Agency Website","url":"https://ask.gov.sg/govsg"},{"title":"stay vigilant and safeguard your business from scams","url":"https://merchant.grab.com/en-sg/blog/stay-vigilant-and-safeguard-your-business-from-scams"},{"title":"ask.gov.sg","url":"https://ask.gov.sg/govsg/questions/clxcvyqdk0067zu1se0ji2ol8?from=quicklinks"},{"title":"Singapore Customs warns public against falling for SMS impersonation scam","url":"https://www.thestar.com.my/aseanplus/aseanplus-news/2024/09/14/singapore-customs-warns-public-against-falling-for-sms-impersonation-scam"},{"title":"A Singapore Government Agency Website","ur

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && for p in keeping-your-grab-account-safe account-security-sg security-guide-consumer; do ./f.sh \"https://www.grab.com/sg/$p/\" \"grab_$p.html\"; done; ./f.sh https://merchant.grab.com/robots.txt grabmerchant_robots.txt; cat grabmerchant_robots.txt | head -30; for f in grab_keeping-your-grab-account-safe grab_account-security-sg grab_security-guide-consumer; do echo \"=== $f\"; python3 -c \"import re,sys;s=open('$f.html').read();m=re.search(r'<title>(.*?)</title>',s,re.S);print(m.group(1).strip() if m else None)\"; ./gx.sh $f.html 3000; done", "description": "Fetch Grab account-safety pages and merchant robots.txt"}

### [tool_result]
200 https://www.grab.com/sg/keeping-your-grab-account-safe/ size=167258 <- https://www.grab.com/sg/keeping-your-grab-account-safe/
200 https://www.grab.com/sg/account-security-sg/ size=166620 <- https://www.grab.com/sg/account-security-sg/
200 https://www.grab.com/sg/security-guide-consumer/ size=172584 <- https://www.grab.com/sg/security-guide-consumer/
200 https://merchant.grab.com/robots.txt size=5878 <- https://merchant.grab.com/robots.txt
<!doctype html><html lang="en" translate="no"><head><script>const isProd=()=>"merchant.grab.com"===window.location.hostname,loadAsset=t=>new Promise((e,a)=>{t.onload=e,t.onerror=a,document.head.appendChild(t)}),loadResource=(t,e)=>new Promise((a,o)=>{const r=document.createElement(t);e&&Object.keys(e).forEach(t=>{r.setAttribute(t,e[t])}),"script"===t?(r.type="text/javascript",r.async=!0,r.defer=!0,loadAsset(r).then(a).catch(o)):"link"===t?loadAsset(r).then(a).catch(o):o(`Unsupported tag name: ${t}`)}),loadScriptOrLink=t=>{if(Array.isArray(t)){const e=t.map(t=>loadResource(t.tagName,t.attributes));return Promise.all(e)}return loadResource(t.tagName,t.attributes)};var dataDomainScript=isProd()?"a3be3527-7455-48e0-ace6-557ddbd506d5":"a3be3527-7455-48e0-ace6-557ddbd506d5-test",otAutoBlockUrl=`https://cdn-apac.onetrust.com/consent/${dataDomainScript}/OtAutoBlock.js`,tagOnetrust=[{tagName:"script",attributes:{src:otAutoBlockUrl}},{tagName:"script",attributes:{src:"https://cdn-apac.onetrust.com/scripttemplates/otSDKStub.js","data-document-language":"true",defer:"defer","data-domain-script":dataDomainScript}},{tagName:"link",attributes:{rel:"preconnect",href:"https://cdn-apac.onetrust.com"}}];const onetrustAccepted=document.cookie.match(/(?<=OptanonAlertBoxClosed=)\w+/)?.[0];var tagForLandingPageOnly=[{tagName:"link",attributes:{rel:"preload",href:isProd()?"https://assets-mobile.grab.com/mex/corex/portal/login-banner-min.webp":"https://assets-mobile.stg-myteksi.com/mex/corex/portal/login-banner-min.webp",fetchpriority:"high",as:"image",type:"image/webp"}}];tagForLandingPageOnly=onetrustAccepted?tagForLandingPageOnly:tagOnetrust.concat(tagForLandingPageOnly);var tagForAllPages=[{tagName:"link",attributes:{rel:"preconnect",href:isProd()?"https://public.grab.com":"https://public.stg-myteksi.com"}},{tagName:"link",attributes:{rel:"preconnect",href:isProd()?"https://assets-mobile.grab.com":"https://assets-mobile.stg-myteksi.com"}}],tags="/portal"===window.location.pathname?tagForLandingPageOnly.concat(tagForAllPages):tagForAllPages;"flashviz-mex.grab.com"===window.location.hostname&&window.location.pathname.includes("webview")||loadScriptOrLink(tags).then(()=>{console.log("Assets loaded successfully")}).catch(t=>{console.error("Failed to load assets:",t)})</script><script type="text/javascript">function OptanonWrapper(){}</script><script defer="defer" src="https://scribe-web-sdk.grab.com/scribe_bundle_v1.0.53.min.js"></script><title>GrabMerchant Portal</title><link rel="shortcut icon" href="/images/grabfavicon.ico"><meta name="description" content="Business made easier with all the tools you need to run and grow your Grab Merchant business, in one place. Login to the GrabMerchant Portal."/><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no"/><meta name="theme-color" content="#000000"/><meta http-equiv="Cache-control" content="no-cache, no-store, must-revalidate"><link rel="manifest" href="/manifest.json"/><base href="/"/><style>.mex-boot{position:fixed;top:0;right:0;bottom:0;left:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:"Inter Variable",Inter,Arial,sans-serif;text-align:center}.mex-boot-spin{position:relative;width:40px;height:40px;transform:rotate(45deg);animation:mex-boot-rotate 1.2s linear infinite}.mex-boot-spin i{position:absolute;display:block;width:18px;height:18px;background-color:#00b14f;border-radius:100%;opacity:.3;transform:scale(.75);transform-origin:50% 50%;animation:mex-boot-fade 1s linear infinite alternate}.mex-boot-spin i:first-child{top:0;left:0;animation-delay:0s}.mex-boot-spin i:nth-child(2){top:0;right:0;animation-delay:.4s}.mex-boot-spin i:nth-child(3){right:0;bottom:0;animation-delay:.8s}.mex-boot-spin i:nth-child(4){bottom:0;left:0;animation-delay:1.2s}.mex-boot-title{margin:12px 0 9px;color:#1a1a1a;font-weight:600;font-size:18px;line-height:1.5}.mex-boot-subtitle{margin:0 0 16px;color:#3d3d3d;font-size:16px;line-height:1.5}@keyframes mex-boot-rotate{to{transform:rotate(405deg)}}@keyframes mex-boot-fade{to{opacity:1}}</style><noscript><style>.mex-boot{display:none}</style></noscript><script defer="defer" src="/static/js/single.099a63dd.js"></script><script defer="defer" src="/static/js/main.a41d0099.js"></script><link rel="preload" href="/static/css/2817.a072ce45.css" as="style"><link rel="preload" href="/static/css/5650.67cc63d7.css" as="style"><link rel="preload" href="/static/css/5712.bb6b5108.css" as="style"><link rel="preload" href="/static/css/9866.910d6cc4.css" as="style"><link rel="preload" href="/static/css/9487.c7b1bb5f.css" as="style"><link rel="preload" href="/static/css/386.c7b1bb5f.css" as="style"><link rel="preload" href="/static/css/8948.46381f32.css" as="style"><link rel="preload" href="/static/css/3717.6d108a4e.css" as="style"><link rel="preload" href="/static/css/7736.826be3d7.css" as="style"><link rel="preload" href="/static/css/8461.826be3d7.css" as="style"><link rel="preload" href="/static/css/874.0442de74.css" as="style"><link rel="preload" href="/static/css/5747.826be3d7.css" as="style"><link rel="preload" href="/static/css/996.826be3d7.css" as="style"><link rel="preload" href="/static/css/6457.fa6d3435.css" as="style"><link rel="preload" href="/static/css/5807.d9e438eb.css" as="style"><link rel="preload" href="/static/css/8764.972529b2.css" as="style"><link rel="preload" href="/static/css/main.f88024fe.css" as="style"><link href="/static/css/main.f88024fe.css" rel="stylesheet"></head><body><noscript>You need 

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && echo \"--- tel/mailto in all grab pages\"; grep -ohE '(tel|mailto):[^\"'\"'\"' <>]+' grab_*.html | sort | uniq -c | sort -rn | head; echo \"--- social/app links (home)\"; grep -oE 'https?://(www\\.)?(facebook|instagram|twitter|x|linkedin|youtube|tiktok|t)\\.(com|me)/[^\"'\"'\"' <>]*' grab_sg_home.html | sort -u | head -20; grep -oE 'https?://(apps\\.apple\\.com|itunes\\.apple\\.com|play\\.google\\.com|appgallery\\.huawei\\.com)[^\"'\"'\"' <>]*' grab_sg_home.html grab_pay_spot-the-fake.html | sort -u | head; echo \"--- grab hosts\"; cat grab_*.html | grep -oE 'https?://[a-z0-9.-]*grab[a-z0-9.-]*\\.[a-z]+' | sed -E 's#https?://##' | sort | uniq -c | sort -rn | head -30", "description": "Extract tel/social/app/host links from Grab pages"}

### [tool_result]
--- tel/mailto in all grab pages
--- social/app links (home)
https://twitter.com/grabsg
https://www.facebook.com/Grab
https://www.instagram.com/grab_sg
https://www.instagram.com/grab_sg/
https://www.linkedin.com/company/grabapp
https://www.linkedin.com/company/grabapp/
https://www.linkedin.com/posts/grabapp_dataprotection-dptm-imda-activity-7359101062881996800-rzVY/
https://www.tiktok.com/@grabsingapore
https://www.youtube.com/c/GrabOfficialSEA
https://www.youtube.com/channel/UC0QKbvP4XKGCw5s4iSXGywQ
grab_pay_spot-the-fake.html:https://apps.apple.com/sg/app/grab-driver/id1257641454
grab_pay_spot-the-fake.html:https://apps.apple.com/sg/app/grabmerchant/id1282271764
grab_pay_spot-the-fake.html:https://apps.apple.com/sg/app/grab-superapp/id647268330
grab_pay_spot-the-fake.html:https://play.google.com/store/apps/details?id=com.grab.merchant&hl=en_SG&gl=sg
grab_pay_spot-the-fake.html:https://play.google.com/store/apps/details?id=com.grabtaxi.driver2
grab_pay_spot-the-fake.html:https://play.google.com/store/apps/details?id=com.grabtaxi.driver2&hl=en_SG&gl=sg
grab_pay_spot-the-fake.html:https://play.google.com/store/apps/details?id=com.grabtaxi.passenger&hl=en_SG&gl=sg
grab_sg_home.html:https://apps.apple.com/sg/app/grab-driver/id1257641454
grab_sg_home.html:https://apps.apple.com/sg/app/grabmerchant/id1282271764
grab_sg_home.html:https://apps.apple.com/sg/app/grab-superapp/id647268330
--- grab hosts
    981 www.grab.com
    441 assets.grab.com
     99 help.grab.com
     63 grab.onelink.me
     32 grabacademyportal.grab.com
     31 dineout.grab.com
     30 limo.grab.com
     30 investors.grab.com
     30 grabmaps.grab.com
     30 grabcn.onelnk.com
     30 grab.careers
     30 gifts.grab.com
     17 express.grab.com
     10 scribe-web-sdk.grab.com
     10 grabtaxi.atlassian.net
     10 grabdriver.onelink.me
     10 food.grab.com
     10 engineering.grab.com
     10 developer.grab.com
      7 partners.grab.com

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F && cat grab_*.html | grep -oE 'https?://(help\\.grab\\.com|grab\\.careers|grabtaxi\\.atlassian\\.net|grab\\.onelink\\.me|grabdriver\\.onelink\\.me|grabcn\\.onelnk\\.com|partners\\.grab\\.com|food\\.grab\\.com)[^\"'\"'\"' <>]*' | sort | uniq -c | sort -rn | head -25; ./f.sh https://help.grab.com/robots.txt grabhelp_robots.txt; head -30 grabhelp_robots.txt", "description": "List Grab help/partner links; fetch help.grab.com robots"}

### [tool_result]
     30 https://help.grab.com/passenger/en-sg/
     30 https://help.grab.com/merchant/en-sg/
     30 https://help.grab.com/driver/
     30 https://grabcn.onelnk.com/0UqZ
     30 https://grab.careers/
     20 https://grab.onelink.me/2695613898
     10 https://grabtaxi.atlassian.net/browse/GW-5477,
     10 https://grab.onelink.me/k45t
     10 https://grab.onelink.me/2695613898?pid=organic_web&c=organic_web&af_adset=grab_website&af_ad=sg&af_channel=download&af_sub1=footer_huawei&is_retargeting=true&af_dp=grab%3A%2F%2Fopen%3FscreenType%3DMAIN&af_force_deeplink=true&af_web_dp=https%3A%2F%2Fappgallery.huawei.com%2Fapp%2FC100447517
     10 https://grab.onelink.me/2695613898?pid=organic_web&c=organic_web&af_adset=grab_website&af_ad=sg&af_channel=download&af_sub1=footer_google_play&is_retargeting=true&af_dp=grab%3A%2F%2Fopen%3FscreenType%3DMAIN&af_force_deeplink=true&af_web_dp=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.grabtaxi.passenger
     10 https://grab.onelink.me/2695613898?pid=organic_web&c=organic_web&af_adset=grab_website&af_ad=sg&af_channel=download&af_sub1=footer_apple_store&is_retargeting=true&af_dp=grab%3A%2F%2Fopen%3FscreenType%3DMAIN&af_force_deeplink=true&af_web_dp=https%3A%2F%2Fapps.apple.com%2Fapp%2Fgrab-taxi-ride-food-delivery%2Fid647268330
     10 https://grabdriver.onelink.me/iF8S
     10 https://food.grab.com/sg/en/?utm_source=grab.com&utm_medium=referral&utm_campaign=footer-link&pid=Grab.com&c=footer-link
      7 http://partners.grab.com/ios/latest/
      3 https://help.grab.com/passenger/en-sg/115005277227
      2 https://help.grab.com/driver/en-sg
      2 https://grab.onelink.me/2695613898?pid=website&af_sub5=referral&c=gw_exp_home0_202110&af_r=https%3A%2F%2Fgifts.grab.com%2F%3Futm_campaign%3Dgw_exp_home0_202110%26utm_source%3Dgrab.com%26utm_medium%3Dreferral%26utm_content%3DGrabGifts_SG&deep_link_value=grab%3A%2F%2Fopen%3FscreenType%3DGIFTS&af_dp=grab%3A%2F%2Fopen%3FscreenType%3DGIFTS
      1 https://help.grab.com/passenger/en-sg/360026931391-Verify-my-identity-for-GrabPay-wallet
      1 https://help.grab.com/passenger/en-sg/360023805451
      1 https://help.grab.com/passenger/en-sg/115000906388-Account-and-Security
      1 https://help.grab.com/hc/en-sg/articles/115013147928-How-to-verify-my-email-address
      1 https://grab.onelink.me/2695613898?pid=organic_web&c=organic_web&af_adset=grab_website&af_ad=sg&af_channel=homepage&af_sub1=download_app&is_retargeting=true&af_dp=grab%3A%2F%2Fopen%3FscreenType%3DMAIN&af_force_deeplink=true&af_web_dp=https%3A%2F%2Fwww.grab.com%2Fsg%2Fdownload%2F
200 https://help.grab.com/robots.txt size=4288 <- https://help.grab.com/robots.txt
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/><meta http-equiv="Pragma" content="no-cache"/><meta http-equiv="Expires" content="0"/><title>Grab Help Centre</title><meta name="image" content="https://help.grab.com/assets/logo.png"><meta itemprop="name" content="Grab Help Centre"><meta itemprop="description" content="Self-serve your Grab questions. Or contact us for help on your account, past trip or order issues. Discover exciting Grab Rewards & Promos & Subscriptions now."><meta itemprop="image" content="https://help.grab.com/assets/logo.png"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="Grab Help Centre"><meta name="twitter:description" content="Self-serve your Grab questions. Or contact us for help on your account, past trip or order issues. Discover exciting Grab Rewards & Promos & Subscriptions now."><meta property="og:title" content="Grab Help Centre"><meta property="og:description" content="Self-serve your Grab questions. Or contact us for help on your account, past trip or order issues. Discover exciting Grab Rewards & Promos & Subscriptions now."><meta property="og:image" content="https://help.grab.com/assets/logo.png"><meta property="og:type" content="website"><script>function fnShowLoadFailedElement(){if(window.skipShowLoadFailedImage)return;const e=document.getElementById("load-failed");e&&e.style&&(e.style.display="block");document.getElementById("load-failed-url").innerText=window.location.href}function fnScriptOnError(){fnShowLoadFailedElement()}</script><script>!function(e,t,a,n,g){e[n]=e[n]||[],e[n].push({"gtm.start":(new Date).getTime(),event:"gtm.js"});var m=t.getElementsByTagName(a)[0],r=t.createElement(a);r.async=!0,r.src="https://www.googletagmanager.com/gtm.js?id=GTM-M9J595T",m.parentNode.insertBefore(r,m)}(window,document,"script","dataLayer")</script><script>window.scribesdk=window.scribesdk||{},["initialize","sendEvent","setAuthToken","setFacets","usePlugin"].forEach((function(i){window.scribesdk[i]=window.scribesdk[i]||function(){(window.scribesdk.q=window.scribesdk.q||[]).push([i,...arguments])}}))</script><script async id="scribe-sdk" src="https://scribe-web-sdk.grab.com/scribe_bundle_v1.0.63.min.js"></script><link rel="icon" href="/33437965/favicon.ico"><script defer="defer" src="/33437965/static/js/5683.623a4ccf.js" onerror='"function"==typeof fnScriptOnError&&fnScriptOnError()'></script><script defer="defer" src="/33437965/static/js/main.c4ce4ebf.js" onerror='"function"==typeof fnScriptOnError&&fnScriptOnError()'></script><link href="/33437965/static/media/Inter-Bold.444a7284.woff2" rel="preload" as="font" crossorigin=""><link href="/33437965/static/media/Inter-Regular.dc131113.woff2" rel="preload" as="font" crossorigin=""><link href="/33437965/static/media/Inter-SemiBold.007ad31a.woff2" rel="preload" as="font" crossorigin=""><link href="/33437965/static/css/main.95e63480.css" rel="stylesheet"></head><body><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-M9J595T&nojscript=true" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript><noscript><div style="margin-top:15%;padding:128px 24px 24px;text-align:center

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)