# Recovered transcript digest: private_A_local_banks_abs (agent a0061efef86ca7dac)

### [user]
You are sub-agent A of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_A_banks_local.json
Scratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A/

YOUR ENTITIES (all Tier 1 = deep):
1. DBS Bank / POSB, incl. digibank, PayLah!, DBS digital token. SPF brand-tag strings to put in aliases: "DBS", "DBS PayLah". Start points: https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page (earlier survey: 13 dated alerts, newest "SMS Phishing Alert" 2026-08-28; re-verify), the "Scams & Frauds Alert Archives" page, the scam-defence hub, and any page on verifying official DBS/POSB channels (SMS sender IDs / short codes, official websites, official apps, hotlines incl. the anti-scam hotline). Note dbs.com.sg robots.txt has ~1000 Disallow lines and no Sitemap line (try /sitemap.xml once). POSB (posb.com.sg): separate child record (parent dbs.com.sg) ONLY if POSB has its own scam/security pages; otherwise alias + include posb.com.sg in DBS official_domains if confirmed. Look for dbs.com (group) and any other SG-used domains confirmed on DBS pages.
2. OCBC Bank (ocbc.com; check whether ocbc.com.sg is used). Start: https://www.ocbc.com/personal-banking/security/security-advisories.page (earlier: dozens of dated editions, latest 2025-06-12; re-check), official SMS sender IDs, anti-scam hotline, OCBC app names, Money Lock / kill switch pages, "Be A Pro Against Cons". (Context only: ScamShield posted an alert on 2026-11-20 about fake "OCBC card suspended" SMSes.)
3. UOB (uob.com.sg; uobgroup.com). Start: https://www.uob.com.sg/personal/digital-banking/news-and-announcements.page, security/anti-scam pages, official SMS sender ID(s), UOB TMRW app, go.uob.com/reportscam (report portal). SPF brand-tag string: "UOB".
4. The Association of Banks in Singapore (abs.org.sg): anti-scam/consumer-protection pages, PayNow consumer page, scam-related media releases, any lists of bank hotlines/official channels. sector "other" (industry association; note it owns the PayNow scheme). Optional programme record `abs.org.sg#paynow` (sector "payments") only if PayNow has dedicated scam/security content.

Cross-check bank hotlines against ScamShield's page https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ (gov page; you may add it to evidence as corroboration, but each bank's own page must be the primary evidence).

Give these the depth they deserve (they are the most-impersonated SG brands), but stay within the brief's request budget. When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

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
{"command": "cat /home/ankur/scamtrends_feed/registry/FORMAT.md; echo ----; ls -la /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/", "description": "Read FORMAT.md and list the private work folder"}

### [tool_use Bash]
{"command": "grep -n -i -E \"dbs|posb|ocbc|uob|abs\\.org|association of banks|paynow|scamshield\" /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -100; wc -l /home/ankur/scamtrends_feed/sources/03_community_commercial.md", "description": "Find bank-related lines in earlier survey"}

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
3:Captured 2026-11-25. Scope excludes SG government sources (SPF/ICAAS, MAS, ScamShield, ScamAlert/NCPC, CSA) and global phishing feeds. Those are covered elsewhere.
22:| 2 | [reportsmishing/Smishing-Dataset-IMC25](https://github.com/reportsmishing/Smishing-Dataset-IMC25) | UCL et al., IMC '25 / academic | Labelled smishing texts: sender type, network, language, named entity (impersonated brand), scam type, lure principles | 33,869 rows global; **~190 SG-relevant** (23 on SGP networks; DBS 69, OCBC 40, Singpass 24, POSB 8, IRAS 8, Singtel 7, UOB 6, SingPost 3, CPF 3) | CSV (9.5 MB) on GitHub raw | `time` field is free-form ("Today 8:48 AM"). Only 157 rows have ISO dates, earliest 2021-09-17 | **CC BY 4.0** | Low share, but SG brands are tagged | **Medium-low.** URLs redacted to `<URL>`, so no domains. Good for SG lure templates and brand priors. Cleanest licence here |
30:| 10 | Bank alert pages: [DBS Recent Scams & Fraud](https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page), [OCBC Security advisories](https://www.ocbc.com/personal-banking/security/security-advisories.page), [UOB News & announcements](https://www.uob.com.sg/personal/digital-banking/news-and-announcements.page) | Banks | Narrative scam alerts (MO, red flags) | DBS 13 dated alerts; OCBC ~dozens of dated editions; UOB undated | HTML | DBS 2026-08-28 ("SMS Phishing Alert"); OCBC latest dated advisory 2025-06-12 | Bank site terms | High | **Very low.** **Zero scam domains or numbers** in any of the three. They only name the bank's own domains/hotlines (allowlist value) |
39:- HuggingFace (API search for `singapore`/`scam`/`smishing`/`scamshield`): the "ScamShield"-named datasets are Indian/generic and unrelated to SG ScamShield.
67:  - `[redacted] | 25 May 2017 | Online Purchase Scam | Name: Thevalueshopping | "Beware of Carousell seller "Thevalueshopping" selling Lego at lowest price! I paid through ibanking $600 deposit into seller OCBC account [redacted]…"`
68:  - `Anonymous | 17 Jul 2020 | Impersonation Scam | Contact: 923329855137 | "They call me by whatsapp … Whatsapp profile was DBS logo … they say my card was blocked"`
77:  - `18:28 | "Fr DBS : There a withdrawal SGD 369 from your DBS/POSB Paylah! on <DATE_TIME> at 18:28 If unauthorised, visit <URL> stop process" | dbs/posb | banking`
95:  - Net: these sites are not a defensible scam-phone source. ScamShield (government) is the authoritative SG source for numbers.
105:- DBS sample: `SMS Phishing Alert — Date: 28 August 2026 — "Scammers use phishing SMSes messages urging you to resolve unauthorised PayNow transactions. These phishing SMSes ask you to call a phone number in the SMS."` (the number is not given).
106:- Another DBS sample: `Token Activation Phishing Alert — 16 March 2026 (Updated 15 August 2026)`.
107:- DBS also has a "Scams & Frauds Alert Archives" page.
108:- OCBC: the "Be A Pro Against Cons" editions are narrative only. The only numbers present are OCBC's own hotlines.
109:- UOB: links out to scamalert.sg and `go.uob.com/reportscam`.
110:- All three: **no fake domains or scam numbers**. They are useful only as a timeline of MOs that banks flagged (dates + titles) and as allowlists (`dbs.com.sg`, `ocbc.com`, `internet.ocbc.com`, `uob.com.sg`, `uobgroup.com`).
142:1. Keep the SPF ICAAS feed as the primary SG domain source. Add the other agent's government feeds (ScamShield, MAS IAL, ScamAlert).
143:2. Add a **brand allowlist table** from the corporate pages (Singtel's ≈45 domains, SingPost/Carousell/Shopee/DBS/OCBC/UOB official domains), plus the published look-alike patterns as typosquat test cases.
146 /home/ankur/scamtrends_feed/sources/03_community_commercial.md

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py; echo ----; sed -n 95,146p /home/ankur/scamtrends_feed/sources/03_community_commercial.md", "description": "Read validator and rest of survey section"}

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
----
  - Net: these sites are not a defensible scam-phone source. ScamShield (government) is the authoritative SG source for numbers.

### 9. Corporate allowlists (negative set)
- **Singtel**: the "List of official Singtel web domains" says all `*.singtel.com` domains are official and adds ≈45 partner domains. Examples: `singtelcrm.com`, `singteltvgo.com`, `portal.singtelge.com`, `gomo.sg`, `heya.sg`, `dash.com.sg`, `gxs.com.sg`, `e-station2.axs.com.sg`, `singtelcares.syd1.qualtrics.com`. Machine-e

### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/; head -30 dbs_robots.txt; echo; grep -i -n -E \"scam|fraud|secur|sitemap|personal/support|posb\" dbs_robots.txt | head -60; grep -c -i disallow dbs_robots.txt", "description": "Inspect cached DBS robots.txt for relevant rules"}

### [tool_result]
DBS Robots
User-Agent: *
Disallow: /iwov-resources/media/pdf/250108_insights_crypto_ai.pdf
Disallow: /iwov-resources/media/pdf/chf-as-funding-currency-jan-2025.pdf
Disallow: /treasures/dbs-forms/1h25-market-outlook-event-registration.page
Disallow: /personal/investments/promotions/MCA-FX-ntp-2024-promo
Disallow: /iwov-resources/media/pdf/241204_insights_crypto_digest.pdf
Disallow: /personal/searchresults.page
Disallow: /treasures/searchresults.page
Disallow: /corporate/insights/treasuryprism/NewRealities/DBS-Treasury-Report-global.pdf
Disallow: /corporate/insights/treasuryprism/pivotal/global/2024-DBS-Treasury-Report.pdf
Disallow: /treasures-private-client/searchresults.page
Disallow: /private-banking/searchresults.page
Disallow: /sme/searchresult.page
Disallow: /corporate/searchresult.page
Disallow: /index/searchresult.page
Disallow: /cgi-bin/
Disallow: /edm/
Disallow: /sg/personal/ibanking/additionalinfo/security/default.aspx
Disallow: /sg/personal/ibanking/additionalinfo/terms/default.aspx
Disallow: /sg/realtyeasy/contact/loanenquiry/default.aspx
Disallow: /personal/online-account-opening-ntb.page
Disallow: /dbsweb-forms/deposits/apply/cip?product%253D0058-MA.E0A49C1341715120A8E634DCC365627B.html
Disallow: /personal/default_chat.page
Disallow: /personal/default_flp_chat.page
Disallow: /i-bank/default_flp_chat.page
Disallow: /treasures/default_chat.page
Disallow: /treasures-private-client/default_chat.page
Disallow: /private-banking/default_chat.page
Disallow: /sites/personal/rates-online/multiplier-account.page

19:Disallow: /sg/personal/ibanking/additionalinfo/security/default.aspx
54:Disallow: /Contact/dbs/cards/credit-card-and-unsecured-loans-relief/default.page
174:Disallow: /iwov-resources/pdf/insurance/general-insurance/POSB_Staycation_Protect_10_TnC_Feb_2021.pdf
190:Disallow: /personal/support/marketplace-poc.html
194:Disallow: /personal/marketplace/search/sitemap-treasures-private-client-2022.html
195:Disallow: /personal/marketplace/search/sitemap-treasures-2022.html
196:Disallow: /personal/marketplace/search/sitemap-posb-2022.html
197:Disallow: /personal/marketplace/search/sitemap-personal-2022.html
198:Disallow: /personal/marketplace/search/sitemap-private-banking-2022.html
223:Disallow: /personal/marketplace-pilot/search/sitemap-treasures-private-client-2022.html
224:Disallow: /personal/marketplace-pilot/search/sitemap-treasures-2022.html
225:Disallow: /personal/marketplace-pilot/search/sitemap-posb-2022.html
226:Disallow: /personal/marketplace-pilot/search/sitemap-personal-2022.html
227:Disallow: /personal/marketplace-pilot/search/sitemap-private-banking-2022.html
268:Disallow: /Contact/posb/deposits/sbapp-apply/default.page
269:Disallow: /Contact/posb/deposits/smart-buddy-application/default.page
270:Disallow: /Contact/posb/deposits/teachers-smart-buddy-application/default.page
298:Disallow: /Contact/posb/deposits/existing-sb-casa-personal/default.page
299:Disallow: /Contact/posb/deposits/existing-sb-casa-personal/complete.page
300:Disallow: /Contact/Contact/posb/deposits/sb-casa-personal/default.page
301:Disallow: /Contact/Contact/posb/deposits/sb-casa-personal/complete.page
316:Disallow: /Contact/posb/deposits/sb-casa-personal-activation/default.page
317:Disallow: /Contact/posb/deposits/sb-casa-personal-activation/complete.page
319:Disallow: /Contact/posb/deposits/posbkids/default.page
324:Disallow: /Contact/posb/deposits/sb-casa-joint/default.page
422:Disallow: /Contact/posb/deposits/apply-myaccount-student/default.page
474:Disallow: /sitemap-privatebanking.xml
475:Disallow: /sitemap-tpc.xml
476:Disallow: /sitemap-treasures.xml
477:Disallow: /sitemap-personal.xml
478:Disallow: /personal/support/mb/#/
479:Disallow: /personal/support/mb/
487:Disallow: /iwov-resources/media/pdf/loans/promotions/cashline-apply/dbs-posb-cashline-sg-clr-nov-tnc.pdf
493:Disallow: /static-sitemap-personal.xml
494:Disallow: /static-sitemap-privatebanking.xml
495:Disallow: /static-sitemap-treasures.xml
496:Disallow: /static-sitemap-tpc.xml
497:Disallow: /sitemap-personal-support-microsite.xml
498:Disallow: /sitemap-common-microsite.xml
513:Disallow: /personal/support/iwov-resources/images/
514:Disallow: /personal/support/iwov-resources/dbs_cheque/misc/table.html
515:Disallow: /personal/support/delete.html
516:Disallow: /personal/support/google347d1ea42f35b783.html
517:Disallow: /personal/support/googledc215cc92bd100be.html
518:Disallow: /personal/support/redirect/
519:Disallow: /personal/support/mb/
520:Disallow: /personal/support/header-no-announcements.html
521:Disallow: /personal/support/header.html
522:Disallow: /personal/support/footer.html
523:Disallow: /personal/support/redirect/
560:Disallow: /personal/support/searchresult.html
561:Disallow: /personal/support/wealth-iwealth-application.html
562:Disallow: /personal/support/wealth-iwealth-change-fixed-deposit-maturity-instructions.html
563:Disallow: /personal/support/bank-ssb-paylah-view-card-deals.html
564:Disallow: /personal/support/wealth-iwealth-view-equity-insights.html
565:Disallow: /personal/support/loans-homeloan-account-number.html
566:Disallow: /personal/support/wealth-iwealth-enable-privacy-mode.html
567:Disallow: /personal/support/digi.html
568:Disallow: /personal/support/wealth-iwealth-gain-access-advanced-market-data.html
569:Disallow: /personal/support/bank-ibanking-replace-secure-device.html
1004

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/; grep -n -E \"^Disallow: /sitemap\\.xml|^Disallow: /$|^Disallow: /personal/scam|^Disallow: /personal/scam-defence|^Allow|scam-defence|^Disallow: /personal/$|^Disallow: /posb\" dbs_robots.txt | head; echo; grep -n -i \"user-agent\" dbs_robots.txt | head", "description": "Check robots rules for sitemap and scam-defence paths"}

### [tool_result]
989:Disallow: /personal/scam-defence/alerts-and-updates.page
990:Disallow: /personal/scam-defence/protect-yourself-now.page
991:Disallow: /personal/scam-defence/learn-about-scams.page
992:Disallow: /personal/scam-defence/how-we-protect-you.page
1010:Disallow: /
1012:Disallow: /

2:User-Agent: *
1009:User-agent: ia_archiver
1011:User-agent: archive.org_bot
1014:User-agent: AdsBot-Google

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/; sed -n 975,1020p dbs_robots.txt", "description": "Show robots.txt tail around scam-defence rules"}

### [tool_result]
Disallow: /personal/digiwealth/invest.page
Disallow: /personal/digiwealth/insure.page
Disallow: /personal/digiwealth/track.page
Disallow: /personal/digiwealth/retire.page
Disallow: /personal/digital-banking/digital-services/default.page
Disallow: /personal/digital-banking/mobile-apps/default.page
Disallow: /personal/digital-banking/payments-and-transfers/default.page
Disallow: /personal/digital-banking/promotions/default.page
Disallow: /personal/cards/promotions/default.page
Disallow: /personal/deposits/promotions/default.page
Disallow: /personal/deposits/atm-branch-services/default.page
Disallow: /personal/deposits/compare-accounts/default.page
Disallow: /personal/deposits/payments-transfers/default.page
Disallow: /personal/deposits/optimise-savings/default.page
Disallow: /personal/scam-defence/alerts-and-updates.page
Disallow: /personal/scam-defence/protect-yourself-now.page
Disallow: /personal/scam-defence/learn-about-scams.page
Disallow: /personal/scam-defence/how-we-protect-you.page
Disallow: /personal/loans/promotion/tesla-carexpo
Disallow: /personal/cards/promotion/sg-cac
Disallow: /personal/loans/promotion/tesla-bedokmall
Disallow: /personal/cards/promotion/dbs-rewards-lucky-draw-winners
Disallow: /personal/cards/promotion/cards-yuu-signup-promo



# URL Masking Details
Disallow: /personal/landing/nav/yournav/users/
Disallow: /personal/landing/nav/yournav/topics/
Disallow: /personal/landing/nav/yournav/categories/
Disallow: https://dbsweb-u05-imp-www.dbs.com.sg/
Disallow: /personal/deployment/maintenance.html
Disallow: /*1000$

User-agent: ia_archiver
Disallow: /
User-agent: archive.org_bot
Disallow: /

User-agent: AdsBot-Google
Disallow:

Sitemap: https://www.dbs.com.sg/sitemap-personal-2026.xml
Sitemap: https://www.dbs.com.sg/sme/sitemap.xml
Sitemap: https://www.dbs.com.sg/corporate/sitemap.xml
Sitemap: https://www.dbs.com.sg/sitemap-treasures-2026.xml

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\ncurl -sL -A \"$UA\" --max-time 30 -o dbs_home.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.dbs.com.sg/personal/default.page; sleep 2\ncurl -sL -A \"$UA\" --max-time 60 -o dbs_sitemap_personal_2026.xml -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.dbs.com.sg/sitemap-personal-2026.xml; sleep 2\ncurl -sL -A \"$UA\" --max-time 30 -o dbs_recent_scams.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page\nls -la", "description": "Fetch DBS homepage, personal sitemap, recent scams page"}

### [tool_result]
200 https://www.dbs.com.sg/personal/default.page 593127
200 https://www.dbs.com.sg/sitemap-personal-2026.xml 278579
200 https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page 197172
total 1060
drwxrwxr-x  2 ankur ankur   4096 Nov 25 18:15 .
drwxrwxr-x 10 ankur ankur   4096 Nov 25 18:14 ..
-rw-rw-r--  1 ankur ankur 593127 Nov 25 18:14 dbs_home.html
-rw-rw-r--  1 ankur ankur 197172 Nov 25 18:15 dbs_recent_scams.html
-rw-rw-r--  1 ankur ankur 278579 Nov 25 18:15 dbs_sitemap_personal_2026.xml

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; grep -o '<loc>[^<]*</loc>' dbs_sitemap_personal_2026.xml | sed 's/<[^>]*>//g' > dbs_sitemap_urls.txt; wc -l dbs_sitemap_urls.txt; grep -i -E 'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect' dbs_sitemap_urls.txt | head -80; echo; grep -c -i 'lastmod' dbs_sitemap_personal_2026.xml", "description": "Extract scam-related URLs from DBS personal sitemap"}

### [tool_result]
1295 dbs_sitemap_urls.txt
https://www.dbs.com.sg/personal/articles/nav/budget-spend/an-easy-guide-to-unsecured-loans
https://www.dbs.com.sg/personal/articles/nav/budget-spend/manage-your-card-security-and-spending
https://www.dbs.com.sg/personal/articles/nav/financial-planning/phishing-scam
https://www.dbs.com.sg/personal/articles/nav/financial-planning/what-you-need-to-know-about-cybersecurity
https://www.dbs.com.sg/personal/articles/nav/investing/avoid-investment-scams
https://www.dbs.com.sg/personal/articles/nav/investing/singapore-government-securities
https://www.dbs.com.sg/personal/articles/nav/protection/7-useful-tips-for-buying-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/10-tips-for-buying-term-insurance-tp
https://www.dbs.com.sg/personal/articles/nav/protection/a-guide-to-buying-car-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/5-protection-plans-for-retirement
https://www.dbs.com.sg/personal/articles/nav/protection/cancer-coverage
https://www.dbs.com.sg/personal/articles/nav/protection/10-tips-for-buying-term-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/careshield
https://www.dbs.com.sg/personal/articles/nav/protection/changes-to-ip-riders
https://www.dbs.com.sg/personal/articles/nav/protection/choosing-the-right-protection-for-your-domestic-helper
https://www.dbs.com.sg/personal/articles/nav/protection/company-and-personal-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/ElderShield-and-CareShield-Life
https://www.dbs.com.sg/personal/articles/nav/protection/endowment-plans-types-features
https://www.dbs.com.sg/personal/articles/nav/protection/enhancements-to-medishield-life
https://www.dbs.com.sg/personal/articles/nav/protection/expats-guide-to-health-insurance-in-singapore
https://www.dbs.com.sg/personal/articles/nav/protection/getting-down-to-insurance-as-married-couple
https://www.dbs.com.sg/personal/articles/nav/protection/guide-health-insurance-singapore-medishield-medisave
https://www.dbs.com.sg/personal/articles/nav/protection/guide-to-choosing-an-integrated-shield-plan
https://www.dbs.com.sg/personal/articles/nav/protection/home-contents-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/how-to-choose-travel-insurance-policy
https://www.dbs.com.sg/personal/articles/nav/protection/how-much-death-coverage-do-you-need
https://www.dbs.com.sg/personal/articles/nav/protection/dependants-protection-scheme
https://www.dbs.com.sg/personal/articles/nav/protection/first-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/how-underwriting-affects-your-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/insurance-needs-for-different-life-stages
https://www.dbs.com.sg/personal/articles/nav/protection/insurance-planning-gaps-for-parents
https://www.dbs.com.sg/personal/articles/nav/protection/homecare-costs-and-healthier-living
https://www.dbs.com.sg/personal/articles/nav/protection/insure-right-for-retirement
https://www.dbs.com.sg/personal/articles/nav/protection/ip-riders-with-cbp
https://www.dbs.com.sg/personal/articles/nav/protection/insurance-for-freelancer
https://www.dbs.com.sg/personal/articles/nav/protection/insure-early-for-lifelong-security
https://www.dbs.com.sg/personal/articles/nav/protection/is-critical-insurance-necessary
https://www.dbs.com.sg/personal/articles/nav/protection/keeping-up-with-insurance-premiums
https://www.dbs.com.sg/personal/articles/nav/protection/insure-your-travels
https://www.dbs.com.sg/personal/articles/nav/protection/making-sense-of-insurance-documents
https://www.dbs.com.sg/personal/articles/nav/protection/managing-cancer-costs-in-singapore
https://www.dbs.com.sg/personal/articles/nav/protection/microinsurance
https://www.dbs.com.sg/personal/articles/nav/protection/making-sense-of-insurance-amid-uncertain-times
https://www.dbs.com.sg/personal/articles/nav/protection/managing-your-health-premiums
https://www.dbs.com.sg/personal/articles/nav/protection/lv-ts-upgrade-article
https://www.dbs.com.sg/personal/articles/nav/protection/navigating-healthcare-costs
https://www.dbs.com.sg/personal/articles/nav/protection/should-you-consider-disability-income-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/multi-pay-critical-illness-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/tackling-costs-of-cancer-treatment
https://www.dbs.com.sg/personal/articles/nav/protection/single-or-annual-travel-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/sandwich-generation
https://www.dbs.com.sg/personal/articles/nav/protection/travel-light-with-right-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/types-of-insurance-should-women-consider
https://www.dbs.com.sg/personal/articles/nav/protection/understanding-critical-illness-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/understanding-term-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/why-insurance-is-important-and-what-should-I-get
https://www.dbs.com.sg/personal/articles/nav/protection/types-of-insurance-for-nsf
https://www.dbs.com.sg/personal/articles/nav/protection/why-insuring-your-child-early-matters
https://www.dbs.com.sg/personal/articles/nav/protection/what-happens-when-dementia-hits
https://www.dbs.com.sg/personal/articles/nav/protection/why-cancercare-insurance-is-worth-considering
https://www.dbs.com.sg/personal/articles/nav/protection/why-get-insurance-for-nsf
https://www.dbs.com.sg/personal/articles/nav/protection/your-guide-to-home-and-mortgage-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/your-first-insurance-journey
https://www.dbs.com.sg/personal/articles/nav/protection/your-quick-guide-to-life-insurance
https://www.dbs.com.sg/personal/articles/nav/protection/why-you-should-get-coverage-early
https://www.dbs.com.sg/personal/cards/credit-cards/faq-revised-credit-card-and-unsecured-credit-rules.page
https://www.dbs.com.sg/personal/deposits/bank-with-ease/3

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; grep -i -E 'scam|fraud|phish|impersonat|fake|beware|official|sender|vigilant|alert|/security|safeguard|secure-banking|digital-token|anti-' dbs_sitemap_urls.txt | grep -v '/protection/' ; echo; python3 - <<'EOF'\nimport re\nx=open('dbs_sitemap_personal_2026.xml').read()\nfor m in re.finditer(r'<url>(.*?)</url>', x, re.S):\n    blk=m.group(1)\n    loc=re.search(r'<loc>(.*?)</loc>',blk).group(1)\n    if re.search(r'scam|fraud|phish', loc, re.I):\n        lm=re.search(r'<lastmod>(.*?)</lastmod>',blk)\n        print(loc, lm.group(1) if lm else None)\nEOF", "description": "Narrow sitemap scam URLs with lastmod dates"}

### [tool_result]
https://www.dbs.com.sg/personal/articles/nav/financial-planning/phishing-scam
https://www.dbs.com.sg/personal/articles/nav/investing/avoid-investment-scams
https://www.dbs.com.sg/personal/deposits/bank-with-ease/digital-token
https://www.dbs.com.sg/personal/deposits/bank-with-ease/how-to-spot-a-scam
https://www.dbs.com.sg/personal/deposits/bank-with-ease/security-checkup
https://www.dbs.com.sg/personal/deposits/bank-with-ease/scam-defence
https://www.dbs.com.sg/personal/digital-banking/scam-defence/default.page
https://www.dbs.com.sg/personal/scam-defence/default.page
https://www.dbs.com.sg/personal/scam-defence/alerts-and-updates.page
https://www.dbs.com.sg/personal/scam-defence/learn-about-scams.page
https://www.dbs.com.sg/personal/scam-defence/how-we-protect-you.page
https://www.dbs.com.sg/personal/support/bank-digital-token-setup-face-verification.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-multiple-devices.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-push-notifications.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-setup.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-transaction.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-troubleshoot.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-additional-security.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token-no-internet.html
https://www.dbs.com.sg/personal/support/bank-ibanking-digital-token.html
https://www.dbs.com.sg/personal/support/wealth-iwealth-set-price-alerts.html
https://www.dbs.com.sg/personal/support/guide-security-on-scams-and-fraud.html
https://www.dbs.com.sg/personal/support/bank-ibanking-notification-alerts.html

https://www.dbs.com.sg/personal/articles/nav/financial-planning/phishing-scam 2026-07-28
https://www.dbs.com.sg/personal/articles/nav/investing/avoid-investment-scams 2026-08-04
https://www.dbs.com.sg/personal/deposits/bank-with-ease/how-to-spot-a-scam 2026-08-04
https://www.dbs.com.sg/personal/deposits/bank-with-ease/scam-defence 2026-08-04
https://www.dbs.com.sg/personal/digital-banking/scam-defence/default.page 2026-08-04
https://www.dbs.com.sg/personal/scam-defence/default.page 2026-08-04
https://www.dbs.com.sg/personal/scam-defence/alerts-and-updates.page 2026-08-04
https://www.dbs.com.sg/personal/scam-defence/learn-about-scams.page 2026-08-04
https://www.dbs.com.sg/personal/scam-defence/how-we-protect-you.page 2026-08-04
https://www.dbs.com.sg/personal/support/guide-security-on-scams-and-fraud.html 2026-05-14

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; python3 - <<'EOF'\nimport re,html\nx=open('dbs_recent_scams.html',encoding='utf-8',errors='replace').read()\n# strip scripts/styles\ny=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\\1>',' ',x)\nt=re.sub(r'(?s)<[^>]+>','\\n',y)\nt=html.unescape(t)\nlines=[l.strip() for l in t.split('\\n') if l.strip()]\ntxt='\\n'.join(lines)\nopen('dbs_recent_scams.txt','w').write(txt)\ni=txt.find('Recent')\nprint(len(txt))\n# locate main content\nfor kw in ['SMS Phishing Alert','Archive','Date:']:\n    print(kw, [m.start() for m in re.finditer(re.escape(kw),txt)][:20])\nEOF", "description": "Convert DBS recent-scams page to text"}

### [tool_result]
12571
SMS Phishing Alert [4192]
Archive [890]
Date: [1159, 2825, 4332, 6518, 8038, 9558, 10995]

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; sed -n '1,400p' dbs_recent_scams.txt | awk 'length($0)>0' | head -c 12571 | tail -c 12000", "description": "Print DBS recent-scams page text"}

### [tool_result]
will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
Login
Recent Scams & Fraud
Recent Scams & Frauds
Scams & Frauds Alert Archives
Recent Scams & Fraud
2025
Phishing Scams
Phishing and Impersonation Alert
Scammers are using phishing emails and impersonating DBS staff via voice calls to steal your personal data and perform unauthorised transactions on your DBS and POSB accounts and cards.
Date:
12 September 2025
What this scam looks like:
Scammers use phishing emails asking you to confirm your login location. These emails have a phishing link and urge you to contact a scammer-controlled number for further help. The scammer impersonates DBS staff and asks for your personal data like your name, number of bank accounts and credit card details.
These scammers aim to use your personal data to steal your login credentials, card details, and OTPs or digital token approvals before conducting unauthorised fund transfer or card transactions.
Protect Yourself:
Always use DBS' and POSB's official hotline number, website, and mobile apps to conduct DBS bank-related requests.
Never provide your DBS card details, digibank credentials, OTPs, or Digital Token approvals to unverified sources.
When in doubt, contact DBS Bank immediately.
Always verify directly with DBS Bank for any requests.
Remember:
DBS staff will never ask you for your login details, card information, OTPs, or Digital Token requests.
Emails and SMSes from DBS will never include clickable links.
Use DBS’ official digibank app regularly to verify that your Digital Token is tied to your approved device. When in doubt, contact DBS Bank immediately.
Contact us immediately if you suspect you're a victim of fraud.
Singapore:
https://www.dbs.com.sg/personal/bank-with-ease/contact-us
China:
400-820-8988
Hong Kong:
https://www.dbs.com.hk/personal/contact-us.page
India:
1-860-210-3456
Indonesia:
0804 1500 327
Taiwan:
(02) 6612 9889 / 0800 808 889
Phishing Alert
Scammers are using phishing emails to steal and perform unauthorised transactions on your DBS and POSB accounts and cards.
Date:
15 August 2025
What this scam looks like:
Scammers use phishing emails urging you to resolve critical issues with your DBS accounts or digital tokens. These phishing emails direct you to sites imitating DBS digibank.
These sites aim to steal your login credentials, card details, and OTPs or digital token approvals before conducting unauthorised fund transfer or card transactions.
Protect Yourself:
Always use DBS' and POSB's official hotline number, website, and mobile apps to conduct DBS bank-related requests.
Never provide your DBS card details, digibank credentials, OTPs, or Digital Token approvals to unverified sources.
When in doubt, contact DBS Bank immediately.
Always verify directly with DBS Bank for any requests.
Remember:
DBS staff will never ask you for your login details, card information, OTPs, or Digital Token requests.
Emails and SMSes from DBS will never include clickable links.
Use DBS’ official digibank app regularly to verify that your Digital Token is tied to your approved device. When in doubt, contact DBS Bank immediately.
Contact us immediately if you suspect you're a victim of fraud.
Singapore:
https://www.dbs.com.sg/personal/bank-with-ease/contact-us
China:
400-820-8988
Hong Kong:
https://www.dbs.com.hk/personal/contact-us.page
India:
1-860-210-3456
Indonesia:
0804 1500 327
Taiwan:
(02) 6612 9889 / 0800 808 889
DBS SMS Phishing Alert
Scammers are impersonating DBS through SMS to steal and perform unauthorised transactions on your DBS and POSB accounts.
Date:
06 April 2023
(Updated 30 April 2025)
Description:
Beware of phishing SMSes targeting you with fake DBS promotions, such as DBS Fixed Deposits offering 4.38% p.a. for 6 months. These SMSes may ask you to contact a phone number to learn more. However, these SMSes are scams, and the person on the other end is not a DBS representative.
The scammer may attempt to trick you into transferring money to their bank account, or they may request your DBS login information and digital token approval code. If they acquire this information, they can use it to steal your bank funds or access your account without your permission.
Never reveal sensitive details to scammers, such as your login credentials or PINs, as they can use this information to conduct unauthorized transactions on your cards or bank account.
If you have shared your Username-PIN Code combination with any non-DBS websites or mobile applications, we strongly advise changing your PIN Code immediately.
You may do so by following the instructions
here
.
Customers are advised to be mindful of such scams.
Protect Yourself:
Always use DBS' and POSB's official hotline number, website, and mobile apps to conduct DBS bank-related requests.
Never provide your DBS card details, digibank credentials, OTPs, or Digital Token approvals to unverified sources.
When in doubt, contact DBS Bank immediately.
Always verify directly with DBS Bank for any requests.
Remember:
DBS staff will never ask you for your login details, card information, OTPs, or Digital Token requests.
Emails and SMSes from DBS will never include clickable links.
Use DBS’ official digibank app regularly to verify that your Digital Token is tied to your approved device. When in doubt, contact DBS Bank immediately.
Contact us immediately if you suspect you're a victim of fraud.
Singapore:
https://www.dbs.com.sg/personal/bank-with-ease/contact-us
China:
400-820-8988
Hong Kong:
https://www.dbs.com.hk/personal/contact-us.page
India:
1-860-210-3456
Indonesia:
0804 1500 327
Taiwan:
(02) 6612 9889 / 0800 808 889
Phishing Alert
Scammers are using phishing emails to steal and perform unauthorised transactions on your DBS and POSB accounts and cards.
Date:
11 April 2025
(Updated on 25 April 2025)
What t

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; head -c 1300 dbs_recent_scams.txt; echo; echo =====; grep -o -i -E '2026[^<\"]{0,80}' dbs_recent_scams.html | sort | uniq -c | head -30; echo ====; grep -o -E '(data-[a-z-]*src|src|href)=\"[^\"]*(json|\\.page|\\.html)[^\"]*\"' dbs_recent_scams.html | grep -i -E 'scam|fraud|alert|archive|json' | sort -u | head -30", "description": "Look for 2026 content and dynamic sources in DBS page"}

### [tool_result]
Recent Scams & Fraud | DBS Singapore
You are in DBS Personal Banking
ATM & Branch
Help & Support
Accounts
Cards
Loans
Insurance
Investments
digiWealth
Digital Banking
ATM & Branch
Accounts
Cards
Loans
Insurance
Investments
digiWealth
Digital Banking
This Search function on our website will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
This Search function on our website will help you to find the information that you need easily
Login
Recent Scams & Fraud
Recent Scams & Frauds
Scams & Frauds Alert Archives
Recent Scams & Fraud
2025
Phishing Scams
Phishing and Impersonation Alert
Scammers are using phishing emails and impersonating DBS staff via voice calls to steal your personal data and perform unauthorised transactions on your DBS and POSB accounts and cards.
Date:
12 September 2025
What this scam looks like:
Scammers use phishing emails asking you to confirm your login location. These emails have 
=====
      6 2026
      1 2026)
      2 2026-04-27T10:22:08
      1 2026-06-11T11:53:07
      1 2026-09-14 17:50:50
      1 2026-09-14T17:46:48
      1 2026-09-14T17:50:50
      1 2026-09-14T18:39:27
      1 2026-09-15T17:51:23
      1 2026-10-02T15:32:20
      1 2026-11-13T15:42:58
      2 2026 DBS Bank Ltd
      5 2026\u003c/strong\u003e\u003c/p\u003e\n\u003cp\u003e\u003cstrong\u003e\u003cspan\u00
      1 2026\u003c/strong\u003e (Updated 15 August 2026)\u003c/p\u003e\n\u003cp\u003e\u003cs
====
href="https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page"

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; python3 - <<'EOF'\nimport re,html,json\nx=open('dbs_recent_scams.html',encoding='utf-8',errors='replace').read()\n# find positions of escaped content containing 2026\nfor m in re.finditer(r'Updated 15 August 2026', x):\n    s=m.start()\n    print(s, repr(x[s-3000:s-2500]))\n    break\n# find script tags with JSON\nscripts=re.findall(r'(?is)<script([^>]*)>(.*?)</script>', x)\nfor i,(attr,body) in enumerate(scripts):\n    if '2026' in body and ('\\\\u003c' in body):\n        print(i, attr[:200], len(body), body[:300].replace('\\n',' '))\nEOF", "description": "Locate JSON blob holding 2026 alerts"}

### [tool_result]
67543 '</div></div><div data-testid="spacer" class="sc-1wgeuk6 iiNIOc"></div></div><div id="RecScaFra_1" class="sc-3oljxp fypbta"><div class="sc-13rtrnd-0 ccknx flpweb-legacy"><div class="container unused rich-text-box"><div class="read-freestylecontent flp-freestyle prodDetail"><div class="flpweb-legacy"><div></div><noscript><h3>SMS Phishing Alert</h3><p>Scammers are using SMS alerts to steal and perform unauthorised transactions on your DBS accounts and cards.</p><p><strong><span>Date: </span>28 Augu'
61  id="__NEXT_DATA__" type="application/json" 84458 {"props":{"pageProps":{"pageConfig":{"meta":{"country":"sg","path":"sites/i-bank/scam-defence/recent-scams-fraud.page","last_modified_date":"2026-09-14T18:39:27","created_date":"2026-09-14T17:46:48","branchname":"personal"},"others_data":{"Page":{"Version":["3.1.1.0",0],"Page_Display_Properties":{"I

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; python3 - <<'EOF'\nimport re,html,json\nx=open('dbs_recent_scams.html',encoding='utf-8',errors='replace').read()\nnd=re.search(r'(?is)<script[^>]*id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>',x).group(1)\nd=json.loads(nd)\njson.dump(d,open('dbs_recent_scams_nextdata.json','w'),indent=1)\n# walk and collect strings containing 'Date'\nout=[]\ndef walk(o,path=''):\n    if isinstance(o,dict):\n        for k,v in o.items(): walk(v,path+'/'+k)\n    elif isinstance(o,list):\n        for i,v in enumerate(o): walk(v,path+f'[{i}]')\n    elif isinstance(o,str):\n        if 'Date' in o and ('<h3' in o or '<p' in o):\n            out.append((path,o))\nprint(len(out))\nalltxt=[]\nfor p,s in out:\n    t=html.unescape(re.sub(r'(?s)<[^>]+>','\\n',s))\n    t='\\n'.join(l.strip() for l in t.split('\\n') if l.strip())\n    alltxt.append('### '+p+'\\n'+t)\nopen('dbs_recent_scams_blobs.txt','w').write('\\n\\n'.join(alltxt))\nfor p,s in out:\n    print(p[:150], len(s))\nEOF\ngrep -n -E '^(### |Date:|[0-9]{1,2} [A-Z][a-z]+ 20[0-9]{2}|\\(Updated)' dbs_recent_scams_blobs.txt | head -80", "description": "Parse __NEXT_DATA__ alert blobs from DBS page"}

### [tool_result]
0

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; python3 - <<'EOF'\nimport re,html\nx=open('dbs_recent_scams.html',encoding='utf-8',errors='replace').read()\n# extract noscript blocks\nns=re.findall(r'(?is)<noscript>(.*?)</noscript>',x)\nprint('noscript blocks',len(ns), [len(n) for n in ns][:40])\nalltxt=[]\nfor i,n in enumerate(ns):\n    t=html.unescape(re.sub(r'(?s)<[^>]+>','\\n',n))\n    t='\\n'.join(l.strip() for l in t.split('\\n') if l.strip())\n    if len(t)>50:\n        alltxt.append(f'### noscript {i}\\n'+t)\nopen('dbs_recent_scams_noscript.txt','w').write('\\n\\n'.join(alltxt))\n# Also find the tab structure: ids like RecScaFra_\nprint(sorted(set(re.findall(r'id=\"(RecScaFra[^\"]*)\"',x))))\nprint(sorted(set(re.findall(r'id=\"([A-Za-z]*_\\d+)\"',x)))[:60])\nEOF\ngrep -n -E '^(### |Date:|[0-9]{1,2} [A-Z][a-z]+ 20[0-9]{2}|\\(Updated)' dbs_recent_scams_noscript.txt | head -80", "description": "Extract noscript alert blocks and tab ids"}

### [tool_result]
noscript blocks 2 [202, 14806]
['RecScaFra_1']
['Capa_1', 'RecScaFra_1', 'ScaFraAleArc_2']
1:### noscript 0
4:### noscript 1
7:Date:
8:28 August 2026
36:Date:
37:16 March 2026
38:(Updated 15 August 2026)
65:Date:
66:15 July 2026
93:Date:
94:15 July 2026
120:Date:
121:21 Jan 2026
148:Date:
149:8 Jan 2026

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; cat dbs_recent_scams_noscript.txt | grep -v -E '^(China:|Hong Kong:|India:|Indonesia:|Taiwan:|400-820-8988|1-860-210-3456|0804 1500 327|\\(02\\) 6612 9889 / 0800 808 889|https://www.dbs.com.hk/personal/contact-us.page)$' | awk '!seen[$0]++ || length($0)<25'", "description": "Print 2026 alert text from noscript block"}

### [tool_result]
### noscript 0
Scammers and fraudsters constantly find ways to trick consumers into giving up their banking details to provide access to their accounts. Being aware of their scam methods can help keep you safe.

### noscript 1
SMS Phishing Alert
Scammers are using SMS alerts to steal and perform unauthorised transactions on your DBS accounts and cards.
Date:
28 August 2026
What this scam looks like:
Scammers use phishing SMSes messages urging you to resolve unauthorised PayNow transactions. These phishing SMSes ask you to call a phone number in the SMS.
The scammers manning these numbers target your login credentials, card details, and OTPs or digital token approvals to taking over your account and conducting unauthorised fund transfer or card transactions.
Protect Yourself:
Always use DBS' and POSB's official hotline number, website, and mobile apps to conduct DBS bank-related requests
Never provide your DBS card details, digibank credentials, OTPs, or Digital Token approvals to unverified sources.
Always verify directly with DBS Bank for any investment-related deals.
Remember:
DBS staff will never ask you for your login details, card information, OTPs, or Digital Token requests.
Emails and SMSes from DBS will never include clickable links.
Use DBS’ official digibank app regularly to verify that your Digital Token is tied to your approved device. When in doubt, contact DBS Bank immediately.
Contact us immediately if you suspect you're a victim of fraud.
Singapore:
https://www.dbs.com.sg/personal/bank-with-ease/contact-us
Stay updated on the latest security news that might affect the way you bank online.
Token Activation Phishing Alert
Scammers are using phishing emails to steal and perform unauthorised transactions on your DBS accounts and cards.
Date:
16 March 2026
(Updated 15 August 2026)
Scammers use phishing emails urging you to resolve critical issues with your DBS accounts or digital tokens. These phishing emails direct you to sites imitating DBS digibank. These sites may instruct you not to access your DBS digibank account for a period of time.
These sites aim to steal your login credentials, card details, and OTPs or digital token approvals before taking over your account and conducting unauthorised fund transfer or card transactions.
Protect Yourself:
Remember:
Singapore:
SMS Phishing Alert
Scammers are sending phishing SMSes disguised as failed delivery notifications to trick you into adding your cards to the scammers’ mobile wallets.
Date:
15 July 2026
Scammers are sending phishing SMSes disguised as failed delivery notifications to trick you into adding your cards to the scammers’ mobile wallets. These failed delivery SMSes lead to phishing sites posing as legitimate delivery companies and requesting payment. Completing the payment process results in your card being added to a scammer’s mobile wallet, allowing unauthorized transactions.
Protect Yourself:
Always use DBS' and POSB's official hotline number, website, and mobile apps to conduct DBS bank-related requests.
Disable adding cards to mobile wallets in the DBS Digibank app. More > Manage Cards & Loans > Payment Controls > Mobile Wallet.
Remember:
Singapore:
Fake Bank Letter Alert
Scammers are posing as DBS-affiliated financial advisors and issuing fake bank letters bearing DBS' letterhead.
Date:
15 July 2026
Scammers are posing as DBS-affiliated financial advisors on various brokerage platforms and offering investment opportunities with DBS or assistance opening a DBS Bank account. These scammers may issue fake bank letters bearing DBS' letterhead and stamp to increase the believability of their scam.
Protect Yourself:
Remember:
Singapore:
Phishing Alert
Scammers are using phishing emails to steal and perform unauthorised transactions on your DBS and POSB accounts and cards.
Date:
21 Jan 2026
Scammers use phishing emails urging you to resolve critical issues with your DBS or POSB accounts or digital tokens. These phishing emails direct you to sites imitating DBS or POSB digibank.
These sites aim to steal your login credentials, card details, and OTPs or digital token approvals before conducting unauthorised fund transfer or card transactions.
Protect Yourself:
Remember:
Singapore:
Deepfake Scams Alert
Scammers are using deepfake videos on social media and phishing sites to promote investment scams.
Date:
8 Jan 2026
Scammers use deepfake videos of DBS Staff and senior leadership or fake affiliate courses to promote scams on social media and fake investment websites.
These scams could trick you into transferring your personal information or funds to scammers.
Protect Yourself:
Remember: if it seems too good to be true, it's likely a scam.
Remember:
Singapore:

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; python3 - <<'EOF'\nimport re,html\nx=open('dbs_home.html',encoding='utf-8',errors='replace').read()\nhrefs=set(html.unescape(h) for h in re.findall(r'href=\"([^\"]+)\"',x))\nhosts=set()\nfor h in hrefs:\n    m=re.match(r'https?://([^/]+)',h)\n    if m: hosts.add(m.group(1).lower())\nprint(sorted(hosts))\nprint()\nfor h in sorted(hrefs):\n    if re.search(r'scam|fraud|secur|phish|facebook|instagram|twitter|x\\.com|youtube|linkedin|tiktok|telegram|apps\\.apple|play\\.google|contact|hotline|official',h,re.I):\n        print(h)\nEOF", "description": "List hosts and scam/social links from DBS homepage"}

### [tool_result]
['dbs-digibank.onelink.me', 'internet-banking.dbs.com.sg?theme=dbs', 'sg.linkedin.com', 'www.dbs.com', 'www.dbs.com.cn', 'www.dbs.com.hk', 'www.dbs.com.sg', 'www.dbs.com.tw', 'www.dbsvonline.com', 'www.facebook.com', 'www.instagram.com', 'www.posb.com.sg', 'www.youtube.com']

/personal/scam-defence/default.page
/personal/scam-defence/protecting-yourself-online?pid=sg-dbs-pweb-footer-default-security-you-textlink
http://www.youtube.com/user/DBS/feed
https://sg.linkedin.com/company/dbs-bank
https://www.dbs.com.sg/Contact/dbs/appointment/default.page
https://www.dbs.com.sg/i-bank/bank-with-ease/contact-us?pid=sg-dbs-pweb-footer-default-contactus-textlink
https://www.dbs.com.sg/personal/investments/singapore-government-securities/default.page
https://www.dbs.com.sg/personal/loans/secured-financing/default.page
https://www.dbs.com.sg/personal/scam-defence/default.page
https://www.dbs.com.sg/personal/scam-defence/digivault
https://www.dbs.com.sg/personal/scam-defence/payment-controls
https://www.dbs.com.sg/personal/scam-defence/protecting-yourself-online
https://www.facebook.com/dbs.sg
https://www.instagram.com/dbsbank/?hl=en

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\ncurl -sL -A \"$UA\" --max-time 30 -o dbs_scam_hub.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.dbs.com.sg/personal/scam-defence/default.page; sleep 2\ncurl -sL -A \"$UA\" --max-time 30 -o dbs_protecting_online.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.dbs.com.sg/personal/scam-defence/protecting-yourself-online; sleep 2\ncurl -sL -A \"$UA\" --max-time 30 -o dbs_guide_security.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.dbs.com.sg/personal/support/guide-security-on-scams-and-fraud.html\ncat > /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A/totext.py <<'EOF'\nimport re,html,sys\ndef totext(fn, keep_noscript=True):\n    x=open(fn,encoding='utf-8',errors='replace').read()\n    tags='script|style' if keep_noscript else 'script|style|noscript'\n    y=re.sub(r'(?is)<(%s)[^>]*>.*?</\\1>'%tags,' ',x)\n    y=re.sub(r'(?is)</?noscript[^>]*>',' ',y)\n    t=html.unescape(re.sub(r'(?s)<[^>]+>','\\n',y))\n    lines=[l.strip() for l in t.split('\\n') if l.strip()]\n    return '\\n'.join(lines)\nif __name__=='__main__':\n    for fn in sys.argv[1:]:\n        open(fn.rsplit('.',1)[0]+'.txt','w').write(totext(fn))\nEOF\npython3 totext.py dbs_scam_hub.html dbs_protecting_online.html dbs_guide_security.html; wc -c dbs_scam_hub.txt dbs_protecting_online.txt dbs_guide_security.txt\ngrep -n -i -E 'sender|short code|sms from|72339|7 ?7777|1800|6327|6339|hotline|official|onelink|\\.com|apps? store|google play' dbs_scam_hub.txt dbs_protecting_online.txt dbs_guide_security.txt | grep -v 'Search function' | head -60", "description": "Fetch DBS scam hub, protecting-online, security guide pages"}

### [tool_result]
200 https://www.dbs.com.sg/personal/scam-defence/default.page 568413
200 https://www.dbs.com.sg/personal/scam-defence/protecting-yourself-online 539886
200 https://www.dbs.com.sg/personal/support/guide-security-on-scams-and-fraud.html 24879
15924 dbs_scam_hub.txt
18933 dbs_protecting_online.txt
 2995 dbs_guide_security.txt
37852 total
dbs_guide_security.txt:13:Do not download apps from unknown or unofficial sources.
dbs_guide_security.txt:16:1800 339 6963
dbs_guide_security.txt:18:(65) 6339 6963 from overseas
dbs_guide_security.txt:30:1800 339 6963
dbs_guide_security.txt:32:(65) 6339 6963 from overseas
dbs_scam_hub.txt:523:Call our 24/7 DBS Fraud Hotline immediately at 1800 339 6963.
dbs_scam_hub.txt:551:Fraudulent SMSes may ask you to call a fake hotline to "verify" suspicious transactions and steal your banking information.​
dbs_scam_hub.txt:634:Phone - 1800 111 1111
dbs_protecting_online.txt:543:https://www.dbs.com.sg/personal/bank-with-ease/contact-us
dbs_protecting_online.txt:547:https://www.dbs.com.hk/personal/contact-us.page
dbs_protecting_online.txt:575:Call us immediately at our 24-hour DBS Fraud Hotline at
dbs_protecting_online.txt:576:1800 339 6963
dbs_protecting_online.txt:578:+65 6339 6963
dbs_protecting_online.txt:609:Please call our 24-hour DBS Customer Service Hotline at 1800 339 6963 or +65 6339 6963 (Overseas) immediately for assistance. Our customer service officer will ask you to provide more details about yourself, your protected account and the transaction in order for us to commence investigations and update you.
dbs_protecting_online.txt:611:Please call our 24-hour DBS Customer Service Hotline at 1800 111 1111 or +65 6327 2265 (Overseas) immediately for assistance. Our customer service officer will ask you to provide more details about yourself, your protected account and the transaction in order for us to commence investigations and update you.
dbs_protecting_online.txt:644:Phone - 1800 111 1111

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; sed -n '/^Login$/,$p' dbs_scam_hub.txt | grep -v 'Search function' | sed -n '1,200p' | cut -c1-260", "description": "Read DBS scam-defence hub main content"}

### [tool_result]
Login
For You
Accounts
Account types
Daily use/ Multi-currency
Fixed deposits
Special savings
Retirement savings
Kids
Featured
Multiplier
My Account
SRS account
For existing customers
Manage eDocuments
Update particulars
Payments & transfers
Resources
Deposit account rates
Latest scams and frauds
NEW
Financial planning guides
Accounts - Help & Support
New to Singapore? Your starter bundle awaits.
Highlights
Secure your savings against scammers and lock your money with digiVault
SCAM DEFENCE
Account types
Daily use/ Multi-currency
Fixed deposits
Special savings
Retirement savings
Kids
See all Account types
Featured
Multiplier
My Account
SRS account
For existing customers
Manage eDocuments
Update particulars
Payments & transfers
Resources
Deposit account rates
Latest scams and frauds
NEW
Financial planning guides
Accounts - Help & Support
Highlights
Secure your savings against scammers and lock your money with digiVault
SCAM DEFENCE
New to Singapore? Your starter bundle awaits.
Cards
Compare Cards
Rebates credit cards
Miles credit cards
Rewards credit cards
Debit cards
Most popular
DBS Chromo Card
NEW
DBS yuu Card
DBS Altitude Card
POSB Everyday Card
Promotions & deals
Current promotions
Lifestyle privileges
Card rewards & services
Credit card rewards
DBS Instalment plans
Payment controls
Increase credit limit
Cash Advance
Resources
Budget and spending tips
Cards - Help and Support
Up to 5% cashback on the things you love with DBS Chromo Card
Highlights
Offset DBS Points or POSB Daily$ for Rewards Flexi eVouchers
NEW
Compare Cards
Rebates credit cards
Miles credit cards
Rewards credit cards
Debit cards
See all Cards
Most popular
DBS Chromo Card
NEW
DBS yuu Card
DBS Altitude Card
POSB Everyday Card
Promotions & deals
Current promotions
Lifestyle privileges
Card rewards & services
Credit card rewards
DBS Instalment plans
Payment controls
Increase credit limit
Cash Advance
View Card rewards & services
Resources
Budget and spending tips
Cards - Help and Support
Highlights
Offset DBS Points or POSB Daily$ for Rewards Flexi eVouchers
NEW
Up to 5% cashback on the things you love with DBS Chromo Card
Loans
Loan types
Home loans
Instant cash loans
Car loans
Education loans
Secured financing
Featured
Green Home Loan
Cashline
Personal Loan
Promotions
Current promotions
Manage your loan
My mortgage application status
Manage your existing home loan
Manage your existing car loan
Manage your education loan
Cashline limit review
Tools
Home affordability calculator
Renovation calculator
Instant cash loan picker
Resources
Financing tips
Loans – Help and Support
Lower-than-HDB rates with DBS HDB Loan
Highlights
Higher education student loan for students (MOE-approved)
NEW
Loan types
Home loans
Instant cash loans
Car loans
Education loans
Secured financing
See all Loan types
Featured
Green Home Loan
Cashline
Personal Loan
Promotions
Current promotions
Manage your loan
My mortgage application status
Manage your existing home loan
Manage your existing car loan
Manage your education loan
Cashline limit review
Tools
Home affordability calculator
Renovation calculator
Instant cash loan picker
Resources
Financing tips
Loans – Help and Support
Highlights
Higher education student loan for students (MOE-approved)
NEW
Lower-than-HDB rates with DBS HDB Loan
Insurance
Protection plans
Travel
Lifestyle
Life
Health & accident
Featured
Travellershield
SavvyEndowment
CancerCare II
Resources
Protection tips
Insurance – Help and Support
Plan with an advisor
Not sure what insurance you need? Start with digiWealth.
Protection plans
Travel
Lifestyle
Life
Health & accident
Explore More
Featured
Travellershield
SavvyEndowment
CancerCare II
Resources
Protection tips
Insurance – Help and Support
Plan with an advisor
Not sure what insurance you need? Start with digiWealth.
Investments

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; sed -n '470,640p' dbs_scam_hub.txt | cut -c1-300; echo ====LINKS; python3 - <<'EOF'\nimport re,html\nx=open('dbs_scam_hub.html',encoding='utf-8',errors='replace').read()\ni=x.find('Fraud Hotline')\nhrefs=[]\nfor h in re.findall(r'href=\"([^\"]+)\"',x):\n    h=html.unescape(h)\n    if re.search(r'scam|fraud|secur|phish|protect|digivault|payment-controls|kill|lock|money|report|police|scamshield|onelink|apps\\.apple|play\\.google',h,re.I):\n        hrefs.append(h)\nfor h in sorted(set(hrefs)): print(h)\nEOF", "description": "Read DBS hub body and scam-related links"}

### [tool_result]
Funds search
Foreign exchange rates
Grow your wealth with digiWealth, our in-app financial planner
Highlights
Aiming for early retirement? Explore regular payouts through bonds and dividend-paying stocks
Investment options
Equities
Funds
Foreign Exchange
Invest with protection
Singapore Government Securities
Explore More
Featured
CIO Insights Funds
Trade with DBS Vickers
Resources
Investment tips
Investments - Help and Support
Funds search
Foreign exchange rates
Highlights
Aiming for early retirement? Explore regular payouts through bonds and dividend-paying stocks
Grow your wealth with digiWealth, our in-app financial planner
digiWealth
Digital Banking
ATM & Branch
Help & Support
You are in DBS Personal Banking
Personal Banking
DBS
POSB
Wealth Management
DBS Treasures
DBS Treasures Private Client
DBS Private Bank
Global Wealth Management
DBS Vickers Securities
DBS Vickers Online
Institutional Banking
SME Banking
Corporate Banking
Financial Markets
Global Financial Markets
DBS Group
About DBS
Login
Home
/
Scam Defence
DBS Scam Defence
- Your security is our priority
Helping you navigate scam threats with timely alerts, security tools and practical protection tips. ​
Suspect you might be a victim of scam?
Call our 24/7 DBS Fraud Hotline immediately at 1800 339 6963.
Act fast if you suspect a scam
Get the help and tools you need to secure your accounts and respond quickly to potential scam threats.​
Safety switch
Transaction dispute​
Malware threats
ScamShield
Suspect your details have been compromised?​
Use Safety Switch to quickly disable access to your digital banking and cards while you seek assistance.​
Learn more
DBS Scam Defence​
This is our multi-layered approach to protecting your money. Advanced technology and dedicated teams work around the clock to safeguard your money, while we equip you with the tools and knowledge to protect yourself.
Scam awareness
24/7​ protection
Scam education in the community​
We make scam awareness accessible through community outreach, branch activities and neighbourhood events. From the POSB Your Neighbourhood Getai series to digital literacy and anti-scam workshops conducted with IMDA, we help Singaporeans recognise threats and stay safe.​
Specialist Anti-Scam Team
Made up of fraud prevention specialists trained to spot the early signs of scam activity, this dedicated unit reviews high-risk transactions flagged by our fraud monitoring systems and works to protect customers from scams.
Frontline staff on alert
Our branch and customer service teams undergo regular training to recognise warning signs of scams. They watch for common red flags and if something seems off, they’ll pause the transaction and ask clarifying questions —helping to protect your money before any funds leave your account.
24/7 Fraud Monitoring Systems
Our advanced surveillance systems run round-the-clock to detect unusual activity. If something suspicious is flagged, we’ll contact you and may temporarily block transactions to keep your funds safe.
Track the latest scams​
Stay ahead of evolving threats and reported incidents.​
Phishing alert​
Deepfake scam alert​
Latest scam alerts​
Beware of SMS phishing scams​
Fraudulent SMSes may ask you to call a fake hotline to "verify" suspicious transactions and steal your banking information.​
Learn more
Use security tools in digibank​
Stay a step ahead of scammers with simple, powerful tools in digibank. Elevate your security today.​
Security Hub
Access your essential security tools in one place and strengthen your protection against scams.
Learn more
SET your transfer limits
Lower your transaction limits to minimise exposure to fraudulent transactions.
Learn more
CHECK your banking alerts
Manage alerts based on your preferred transaction threshold amount.
Learn more
PROTECT your cards with Payment Controls
Secure your cards with just a few taps.
Learn more
LOCK your money with digiVault
It’s easy to secure your savings against scammers with digiVault​.
Learn more
Sharpen your scam instincts
Stay informed, spot red flags and learn how to protect yourself from scams with the resources and guides below.
Money mules scam
Offered easy money for moving funds? Learn how scammers recruit money mules and the risks of allowing others to use your bank account.
Learn more
Impersonation scam
A call from the “bank” or “government”? Learn how scammers impersonate trusted organisations to steal your personal and banking information.
Learn more
Phishing scam
Can you spot a fake website? Learn how phishing scams trick victims into revealing their login credentials, card details and security codes.
Learn more
eCommerce scam
Buying or selling things online? Learn how scammers use fake listings, payment links and QR codes to steal your money or banking details.
Learn more
Fake friend scam
Think it’s someone you know? Learn how scammers impersonate friends, relatives and acquaintances to gain your trust and ask for money.
Learn more
Job scam
Tempted by an easy job offer? Discover how scammers use high-paying job opportunities to trick victims into transferring money.
Learn more
Malware threats
Asked to download an app? Learn how malware scams infect your device and compromise your banking credentials.
Learn more
Anti-Scam Quiz
Test how prepared you are against scams!
Learn more
How DBS helps protect you from scams
We are committed to protecting your money – explore how our teams and advanced detection systems work together to detect suspicious activity and prevent scams.
Technology & measures
DBS/POSB malware protection
Transaction screening
Digital token authentication
Additional safeguards
24/7 assistance
Shared responsibility framework
For businesses
Essential anti-scam tips  (S.A.F.E.)
Scam stories by DBS & SPF
Hear real-life scam stories from our DBS staff and SPF officers on the ground.
You might also be interested in
Anti-Scam Quiz
Test your scam knowledge.
Learn more
Fraud prevention tools
Discover articles to help you better protect yourself.
Help & s

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A; awk '/^Security & You|^Protecting yourself online|^Protecting Yourself Online/{f=1} f' dbs_protecting_online.txt | head -5; grep -n -m3 -i 'protecting yourself' dbs_protecting_online.txt; sed -n '500,640p' dbs_protecting_online.txt | cut -c1-400", "description": "Read DBS protecting-yourself-online content"}

### [tool_result]
Security & You
Scheduled Maintenance
Download digibank
iOS and Android
Others
POSB
Wealth Management
DBS Treasures
DBS Treasures Private Client
DBS Private Bank
Global Wealth Management
DBS Vickers Securities
DBS Vickers Online
Institutional Banking
SME Banking
Corporate Banking
Financial Markets
Global Financial Markets
DBS Group
About DBS
Login
Home
/
Scam Defence
/
Let's bank safely together
Latest scams & fraud
Get the latest alerts and tips to protect yourself online.
Scammers use a variety of tactics to trick consumers into revealing banking details.
Knowing how these scams work can help you protect yourself and your accounts.
Overview
Recent Scams & Fraud
Contact us
ScamAlert by NCPC
Cybersecurity awareness
Get help
Overview
Overview
Recent Scams & Fraud
Contact us
ScamAlert by NCPC
Cybersecurity awareness
Get help
Recent Scams & Fraud
Find out more about the latest scams & fraud cases and how to protect yourself against them.
Find out more
Contact us immediately if you suspect you're a victim of fraud.
Singapore
https://www.dbs.com.sg/personal/bank-with-ease/contact-us
China
400-820-8988
Hong Kong
https://www.dbs.com.hk/personal/contact-us.page
India
1-860-210-3456
Indonesia
0804 1500 327
Taiwan
(02) 6612 9889 / 0800 808 889
E-Payments User Protection Guidelines
The Monetary Authority of Singapore has issued the E-Payments User Protection Guidelines (“Guidelines”) to protect users of electronic payments and encourage wider adoption of e-payments in Singapore.
The Guidelines establishes a common baseline protection that financial institutions will provide to individuals or sole proprietors from losses arising from isolated unauthorised or erroneous epayment transactions from their protected accounts. Here are some common questions about the Guidelines.
For more information on
MAS’ Guidelines
, you may refer to the
FAQ on E-Payments User Protection Guidelines by ABS
.
ScamAlert by NCPC
Anyone can be scammed and suffer financial loss.
Visit
scamalert.sg
, an initiative by the National Crime Prevention Council and learn how to protect yourself from different types of scams.
Cybersecurity Awareness by CSA
DBS Bank is the inaugural organization certified under the Cyber Trust Mark certification scheme.
We have been awarded the prestigious 'Advocate' tier as a testament and recognition of our robust cybersecurity practices and measures across the bank's digitalised business operations.
Visit
go.gov.sg/bettercybersafe
, an initiative by the Cyber Security Agency of Singapore and learn about their cybersecurity awareness campaign.
Learn more
Need Help?
Call us immediately at our 24-hour DBS Fraud Hotline at
1800 339 6963
or
+65 6339 6963
(Overseas) to report fraudulent transactions, unauthorised access to your banking account and loss of credit/debit cards.
Guide to Online Security
Guide to Card Security
Report a Security Issue
If you wish to report an alleged scam or fraud attempt to prevent others from being a victim, you can do so using our DBS digibot
here.
SafeGuard Your E-Payments
Understanding the Guidelines
Reporting & Resolution
Transaction Notifications & Alerts
How do the Guidelines protect me?
We will provide you with transaction notifications and a reporting channel so that you may be alerted of unauthorised transactions and report them when they happen.
We will investigate claims of unauthorised transactions with the aim of achieving a fair and reasonable resolution. The Guidelines do not apply to transactions which you initiated because of a scam or fraud. Such transactions will be investigated by the police.
What is a protected account?
Protected accounts are those that:
a. Are held by either individuals or sole proprietors, including those held jointly by multiple account holders; and
b. Can hold a balance of more than S$500 (or equivalent amount in another currency) at any one time, or is a credit facility, which can be used for electronic payment transactions.
What type of transactions are covered by the Guidelines?
The Guidelines cover all payments from protected accounts initiated through electronic means, and where funds are received through electronic means.
The Guidelines do not apply to transactions which you initiated because of a scam or fraud.
What are my duties as an account holder or account user?
The Guidelines set out your duties as an e-payment user to adopt good security practices. These include:
a. Keeping your contact details such as Singapore mobile number and email address with us up to date so that we can send you transaction alerts by SMS or email;
b. Opting to receive transaction notifications for all outgoing transactions of any amount.
c. Enabling alerts on any device used to receive such alerts;
d. Monitoring your transaction alerts and account statements for any unauthorised or erroneous transactions;
e. Practicing good digital security habits by protecting your access codes and not sharing with it anyone. If you need to record your access codes, keep it securely and make sure that it is only known to you and unlikely to be found by a third party;
f. Protecting access to your protected account;
g. Report to us immediately if you notice any unauthorised or erroneous transactions; Make a police report and furnish a copy of the report together with information about the unauthorised transaction us so that we can begin the investigation process;
How can I report an unauthorized transaction?
Please call our 24-hour DBS Customer Service Hotline at 1800 339 6963 or +65 6339 6963 (Overseas) immediately for assistance. Our customer service officer will ask you to provide more details about yourself, your protected account and the transaction in order for us to commence investigations and update you.
How can I report an erroneous transaction?
Please call our 24-hour DBS Customer Service Hotline at 1800 111 1111 or +65 6327 2265 (Overseas) immediately for assistance. Our customer service officer will ask you to provide more details about yourself, your pr

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [tool_use WebSearch]
{"query": "DBS POSB official SMS sender ID \"DBS\" short code site:dbs.com.sg", "mode": "standard"}

### [tool_use WebSearch]
{"query": "POSB scam alert security site:posb.com.sg", "mode": "standard"}

### [tool_result]
You've hit your session limit · resets 9:40pm (Asia/Singapore)

### [tool_result]
Web search results for query: "DBS POSB official SMS sender ID "DBS" short code site:dbs.com.sg"

Links: [{"title":"sms q","url":"https://www.dbs.com.sg/personal/deposits/bank-with-ease/sms-q"},{"title":"sms q","url":"https://www.dbs.com.sg/i-bank/deposits/bank-with-ease/sms-q"},{"title":"Use SMS \"Q\"","url":"https://www.dbs.com.sg/personal/support/general-bank-details-branch-smsq.html"},{"title":"sms q","url":"https://www.dbs.com.sg/personal/branch-services/sms-q"},{"title":"go.dbs.com","url":"https://go.dbs.com/GS1SD2022"},{"title":"Use SMS \"Q\"","url":"https://www.dbs.com.sg/personal/support/general-bank-details-branch-smsq.html?pid=sg-ps3-dsm-table"},{"title":"DBS/POSB – First bank in Singapore to introduce SMS queue system in all full-service branches","url":"https://dbs.com/newsroom/DBS_POSB_First_bank_in_Singapore_to_introduce_SMS_queue_system_in_all_full_service_branches"},{"title":"Receive Funds from Others","url":"https://dbs.com.sg/personal/support/bank-receive-funds-from-others.html"},{"title":"Digital Services","url":"https://www.dbs.com.sg/personal/support/digital-services-main.html"},{"title":"Register for Digital Services","url":"https://www.dbs.com.sg/treasures-private-client/deposits/bank-with-ease/e-services-existing-ib-customer.page"},{"title":"DBS undertakes further measures to bolster digital banking security","url":"https://www.dbs.com/newsroom/DBS_undertakes_further_measures_to_bolster_digital_banking_security"},{"title":"protecting yourself online","url":"https://www.dbs.com.sg/personal/deposits/bank-with-ease/protecting-yourself-online"},{"title":"DBS introduces SMS Banking to further enhance its suite of mobile banking offerings","url":"https://www.dbs.com/newsroom/DBS_introduces_SMS_Banking_to_further_enhance_its_suite_of_mobile_banking_offerings"},{"title":"Bank & Branch Codes","url":"https://dbs.com.sg/personal/support/bank-general-bank-branch-names-codes.html"},{"title":"posb swift code","url":"https://www.xe.com/en-au/swift-codes/countries/singapore/posb-swift-code"},{"title":"Create an Airwallex account today","url":"https://www.airwallex.com/en-sg/blog/dbs-swift-code"},{"title":"Additional Measures to Protect You Against Phishing Scams","url":"https://go.dbs.com/sg-scam-measures"}]

Based on the search results from dbs.com.sg, I found information about DBS POSB SMS services, though the results primarily show information about the SMS "Q" service for queue management at branches.

The search results show various branch-specific SMS phone numbers like 83184330 for Holland Village Branch, 83184331 for Kovan Branch, and other numbers for DBS and POSB branches.

However, regarding your specific query about the official SMS sender ID "DBS" short code, the search results contain limited information on this topic from the dbs.com.sg domain. The results mainly focus on the SMS "Q" queue service and branch phone numbers rather than the standard SMS sender ID used for outgoing DBS notifications.

For more detailed information about DBS's official SMS sender ID and short code specifications, you may need to contact DBS customer support directly or check their security/SMS settings documentation pages on the main website.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)