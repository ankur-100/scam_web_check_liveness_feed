# Recovered transcript digest: private_G2_insurers_media (agent a55d50fb9aafdbb70)

### [user]
You are sub-agent G2 of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_G2_insurance_media.json
Scratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2/

YOUR ENTITIES
Tier 1 insurers: find fraud/scam advisories (fake agents, fake policy/claims SMS, impersonation), official channels, apps.
1. Great Eastern (greateasternlife.com)
2. Prudential Singapore (prudential.com.sg)
3. AIA Singapore (aia.com.sg)
4. Income Insurance (income.com.sg)
5. Singlife (singlife.com)
Tier 1 media: fake-news investment ads impersonate these. Want (a) pages where the outlet warns about scams impersonating itself (fake articles/sites/ads, deepfakes, fake social accounts) - capture any listed fake domains as text only, never visit them; (b) its scam-news topic page and RSS feed if one exists (kind "news_releases", note "media coverage topic feed").
6. SPH Media (verify primary domain, e.g. sph.com.sg) and The Straits Times (straitstimes.com; parent_entity_id = SPH Media's domain). SPF brand-tag string: "The Straits Times".
7. Mediacorp (mediacorp.sg) and CNA (channelnewsasia.com; parent_entity_id "mediacorp.sg"). SPF brand-tag string: "CNA" (7 SPF advisories about fake CNA-styled investment articles).
8. Mothership (mothership.sg)
Tier 2 (quick, at most 3): The Business Times, Lianhe Zaobao, TODAY, FWD Singapore, Manulife Singapore, HSBC Life Singapore.

Note: ST is partly paywalled; only read what is publicly visible. Respect robots.txt (some news sites disallow AI crawlers; if robots disallows generic user-agents for a path, don't fetch it).

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
{"command": "cat /home/ankur/scamtrends_feed/registry/FORMAT.md; echo ----; ls -la /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/", "description": "Read the format spec and list work folder"}

### [tool_use Bash]
{"command": "wc -l /home/ankur/scamtrends_feed/sources/03_community_commercial.md; grep -n -i -E \"insur|great eastern|prudential|aia|income|singlife|straits|mediacorp|cna|mothership|sph|zaobao|today|business times|fwd|manulife|hsbc life|media\" /home/ankur/scamtrends_feed/sources/03_community_commercial.md | head -80", "description": "Search earlier survey for my entities"}

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
1:# Non-government Singapore scam sources: community, media, industry, commercial, academic, open-source
22:| 2 | [reportsmishing/Smishing-Dataset-IMC25](https://github.com/reportsmishing/Smishing-Dataset-IMC25) | UCL et al., IMC '25 / academic | Labelled smishing texts: sender type, network, language, named entity (impersonated brand), scam type, lure principles | 33,869 rows global; **~190 SG-relevant** (23 on SGP networks; DBS 69, OCBC 40, Singpass 24, POSB 8, IRAS 8, Singtel 7, UOB 6, SingPost 3, CPF 3) | CSV (9.5 MB) on GitHub raw | `time` field is free-form ("Today 8:48 AM"). Only 157 rows have ISO dates, earliest 2021-09-17 | **CC BY 4.0** | Low share, but SG brands are tagged | **Medium-low.** URLs redacted to `<URL>`, so no domains. Good for SG lure templates and brand priors. Cleanest licence here |
23:| 3 | Group-IB SG reports: [Immediate Era (2025-10-21)](https://www.group-ib.com/blog/immediate-era-fraud-singapore/), [SingPost delivery scams](https://www.group-ib.com/blog/fake-delivery-scams-singapore/), [SupportGoWhere phishing PR](https://www.group-ib.com/media-center/press-releases/phishing-campaign-targeting-singapore/) | Group-IB / commercial TI | Campaign narratives with **counts**: 52 redirect domains and 119 fake-news domains (Immediate Era); 107 sites incl. 85 SingPost look-alikes (delivery) | Domain lists **not published**. Only 1 example domain appears in the Immediate Era text | HTML narrative. IOCs "available to customers in the TI portal" | 2025-10-21 | Group-IB site ToS, proprietary | High | **Low as data, high as context.** Gives ground-truth scale for validating coverage |
36:| 16 | Media (Straits Times, CNA, Mothership) | Publishers | Domains appear only when **echoing government advisories** (e.g. [Mothership 2026-04](https://mothership.sg/2026/04/mha-imda-6-fake-news-websites-blocked/) lists 6 MHA/IMDA-blocked *hostile-information* sites, not scam sites) | n/a | HTML; ST paywalled | Live | Publisher copyright | High | **Nil incremental.** Redundant with SPF/MHA sources |
45:- The Google DeepMind × GovTech Gemma scam-detector (announced 2026-10-14) reportedly comes with a "public dataset of anonymised scam conversation patterns". It is **not on HF under google/govtech** as of today. Re-check later; it would also count as quasi-government.
78:  - `Today 8:48 AM | "Singtel!:We inform you in writing that the invoice for <DATE_TIME> has been paid twice … request a refund: <URL>" | singtel | telecom`
81:- Immediate Era (2025-10-21): Google-Ads malvertising using deepfakes of SG officials, Convertri-hosted redirectors and IP-geofenced cloaking to SG. Group-IB says 3,808 SG clicks and 685 redirected in a month. It counts **52 intermediary + 119 fake-news domains**, but publishes only the example `razudai.com` (in a gated URL with gclid parameters). The rest is "available to Group-IB customers in the Threat Intelligence portal".

### [tool_use Bash]
{"command": "cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py; ls /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/; ls /home/ankur/scamtrends_feed/registry/", "description": "Read the validator and list registry folders"}

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
allowlist.txt
brand_context.txt
brand_snips.txt
crtsh.py
ct
ctnames.py
econ
gh_repo.json
img
kwfilter.py
log_a.txt
log_b.txt
log_c.txt
log_d.txt
log_e.txt
log_f.txt
pages
pagetext.py
private
__pycache__
scan
sgdi
sgdi_agencies.json
sgdi_fetch.py
sgdi_lists.json
sgdi_lta.html
sgdi_ministries.html
sgdi_min_mddi.html
sgdi_min_mfa.html
sgdi_min_mha.html
sgdi_min_mindef.html
sgdi_min_minlaw.html
sgdi_min_pmo.html
sgdi_organs-of-state.html
sgdi_statutory-boards.html
sitemap_scan.py
smscheck_chunk.js
sms_

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/; head -50 pagetext.py; echo ----; head -40 kwfilter.py; echo ----; python3 -c \"\nimport json\nd=json.load(open('/home/ankur/scamtrends_feed/registry/spf_brands.json'))\nprint(type(d), len(d))\nitems = d if isinstance(d,list) else d.get('brands', d)\nimport re\nfor b in (items if isinstance(items,list) else []):\n    s=json.dumps(b)\n    if re.search(r'(?i)straits|cna|mediacorp|mothership|insur|great eastern|prudential|aia|income|singlife|zaobao|today|business times|fwd|manulife|hsbc', s):\n        print(s[:700]); print()\n\"", "description": "Inspect helper scripts and SPF brands relevant to my group"}

### [tool_result]
#!/usr/bin/env python3
"""Fetch a public page; print status, title, date hints, rel=alternate feeds, and visible text."""
import re, subprocess, sys, html, time, json, hashlib, os
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')
os.makedirs(CACHE, exist_ok=True)

def get(url, timeout=40):
    fn = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + '.html')
    p = subprocess.run(['curl', '-sS', '-L', '--max-redirs', '5', '-A', UA, '-m', str(timeout), '--compressed',
                        '-w', '\n__META__%{http_code} %{url_effective}', url], capture_output=True)
    raw = p.stdout; i = raw.rfind(b'\n__META__')
    meta = raw[i+9:].decode().split(' ', 1) if i >= 0 else ['0', url]
    body = raw[:i] if i >= 0 else b''
    open(fn, 'wb').write(body)
    time.sleep(0.8)
    return int(meta[0]) if meta[0].isdigit() else 0, meta[1] if len(meta) > 1 else url, body.decode('utf-8', 'replace')

def text_of(h):
    h = re.sub(r'(?is)<(script|style|noscript|svg|head)\b.*?</\1>', ' ', h)
    h = re.sub(r'(?is)<(nav|footer)\b.*?</\1>', ' ', h)
    h = re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>|</div>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    t = re.sub(r'[ \t\r\f\v]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()

if __name__ == '__main__':
    maxc = int(os.environ.get('MAXC', '3000'))
    for url in sys.argv[1:]:
        code, final, h = get(url)
        title = re.search(r'(?is)<title[^>]*>(.*?)</title>', h)
        print('=' * 100); print('URL:', url); print('STATUS:', code, 'FINAL:', final)
        print('TITLE:', html.unescape(title.group(1).strip())[:200] if title else None)
        for m in re.findall(r'(?is)<link[^>]+rel=["\']alternate["\'][^>]*>', h)[:6]: print('ALT:', m[:250])
        for m in re.findall(r'(?is)<meta[^>]+(?:published|modified|date|og:updated)[^>]*>', h)[:6]: print('META:', m[:200])
        for m in re.findall(r'"date(?:Published|Modified)"\s*:\s*"([^"]+)"', h)[:4]: print('JSONLD date:', m)
        t = text_of(h)
        print('TEXTLEN:', len(t)); print(t[:maxc])
----
import json,re,sys,os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ctnames import load
KW=re.compile(r'scam|fraud|phish|ncpc|shield|cyber|spam|alert|report|eservice|ial|investor|safe|ocha|harm|pango|ask|verify|check|crime|asc|antiscam', re.I)
for z in sys.argv[1:]:
    o=load(f'ct/crtsh_{z}.json')
    hits=[n for n in o if KW.search(n[:-len(z)])]
    print(f'### {z}: {len(o)} names, {len(hits)} keyword-ish hits')
    for n in sorted(hits): d=o[n]; print(f'   {n:55s} {d["first"]}..{d["last"]} exp {d["last_exp"]} n={d["n"]}')
----
<class 'list'> 159
{"brand_value": "CNA", "tag_id": "8d3f3eb7-bdf7-4395-845f-1b8ee6bbaec4", "count": 7, "categories": ["Investment"], "sample_domains": ["truedesignsolutions.shop", "zenvaroe.com", "avernovat.com", "databaiouzuma.com"], "sample_titles": ["Advisory: Beware of Fake CNA Investment Schemes", "Advisory: Beware of Investment Scams Impersonating CNA"]}

{"brand_value": "The Straits Times", "tag_id": "13cead50-154f-4ef4-b46a-f5357d1c730d", "count": 1, "categories": ["Investment"], "sample_domains": ["strikeathletics.pro"], "sample_titles": ["Advisory: Scam Websites Impersonating The Straits Times for Fake Investments"]}

{"brand_value": "Alvopetro", "tag_id": "634af37e-b795-4f4d-87a1-908b9b83f144", "count": 1, "categories": ["Investment"], "sample_domains": ["autonomo-income.com", "aloilvip.shop"], "sample_titles": ["Advisory: Beware of Investment Scams Impersonating Legitimate Companies"]}

{"brand_value": "Hochschild", "tag_id": "be7d49d8-7aae-4bfc-8710-6e66ae19210f", "count": 1, "categories": ["Investment"], "sample_domains": ["autonomo-income.com", "aloilvip.shop"], "sample_titles": ["Advisory: Beware of Investment Scams Impersonating Legitimate Companies"]}

{"brand_value": "VanguardETFs", "tag_id": "29527920-f4d0-4b5d-b6c8-fbe16cecf22c", "count": 1, "categories": ["Investment"], "sample_domains": ["volleyport.life", "vanguardetfs.xyz"], "sample_titles": ["Advisory: Beware of Fake CNA Investment Schemes"]}

### [tool_use ToolSearch]
{"query": "select:WebSearch,WebFetch", "max_results": 2}

### [tool_result]


### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2 && cat > /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2/g2.py <<'EOF'\n#!/usr/bin/env python3\n\"\"\"G2 helper: polite fetch (browser UA, >=1.1s sleep), raw saved under G2/raw/.\nUsage:\n  g2.py page URL...            status/title/feeds/dates + visible text (MAXC env)\n  g2.py links URL [regex]      hrefs (from saved or fresh fetch) matching regex (default social/app/login)\n  g2.py robots URL             robots.txt summary (UA * groups + Sitemap lines)\n  g2.py sitemap URL [maxfiles] fetch sitemap(s) (index -> children up to maxfiles), grep scam keywords\n  g2.py grep URL regex [ctx]   fetch page, print visible-text lines matching regex\n\"\"\"\nimport re, subprocess, sys, html, time, hashlib, os, gzip\nUA = \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\nD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw'); os.makedirs(D, exist_ok=True)\nKW = re.compile(r'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect', re.I)\n_cache = {}\ndef fn_of(url):\n    slug = re.sub(r'[^A-Za-z0-9]+', '_', url.split('://', 1)[-1])[:90]\n    return os.path.join(D, slug + '_' + hashlib.md5(url.encode()).hexdigest()[:6])\ndef get(url, timeout=30):\n    if url in _cache: return _cache[url]\n    fn = fn_of(url)\n    p = subprocess.run(['curl', '-sS', '-L', '--max-redirs', '6', '-A', UA, '-m', str(timeout), '--compressed',\n                        '-H', 'Accept-Language: en-SG,en;q=0.9',\n                        '-o', fn, '-w', '%{http_code} %{url_effective}'], input=None, capture_output=True) if False else \\\n        subprocess.run(['curl', '-sS', '-L', '--max-redirs', '6', '-A', UA, '-m', str(timeout), '--compressed',\n                        '-H', 'Accept-Language: en-SG,en;q=0.9', '-o', fn, '-w', '%{http_code} %{url_effective}', url],\n                       capture_output=True)\n    meta = p.stdout.decode(errors='replace').split(' ', 1)\n    code = int(meta[0]) if meta and meta[0].isdigit() else 0\n    final = meta[1] if len(meta) > 1 else url\n    try: body = open(fn, 'rb').read()\n    except FileNotFoundError: body = b''\n    if body[:2] == b'\\x1f\\x8b':\n        try: body = gzip.decompress(body)\n        except Exception: pass\n    time.sleep(1.1)\n    r = (code, final, body.decode

### [tool_result]
ok

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; G=./g2.py; python3 $G robots https://www.greateasternlife.com; python3 - <<'EOF'\nimport sys; sys.argv=['x']; exec(open('g2.py').read().split(\"if __name__ == '__main__':\")[0])\ncode, final, h, err = get('https://www.greateasternlife.com/sg/en/personal-insurance.html')\nprint(code, final, len(h))\nimport re\nt=text_of(h, keep_navfoot=True)\nfor ln in t.splitlines():\n    if re.search(r'scam|fraud|secur|official|hotline|whatsapp|app|1800|6248|\\+65', ln, re.I): print('  T:', ln.strip()[:200])\nEOF\npython3 $G links https://www.greateasternlife.com/sg/en/personal-insurance.html", "description": "Great Eastern robots, homepage text and links"}

### [tool_result]
## robots https://www.greateasternlife.com 200 https://www.greateasternlife.com/robots.txt bytes 866
User-Agent: *
    Disallow: */errors*
Sitemap: https://www.greateasternlife.com/achievers/geachievers-en-sitemap.xml
Sitemap: https://www.greateasternlife.com/bn/en/bn-en-sitemap.xml
Sitemap: https://www.greateasternlife.com/id/in/id-in-sitemap.xml
Sitemap: https://www.greateasternlife.com/my/en/my-en-sitemap.xml
Sitemap: https://www.greateasternlife.com/sg/en/sg-en-sitemap.xml
Sitemap: https://www.greateasternlife.com/sg/zh/sg-zh-sitemap.xml
Sitemap: https://www.greateasternlife.com/greateasternwomensrun/wr-en-sitemap.xml
Sitemap: https://www.greateasternlife.com/sg/adviser/adp-gels-sitemap.xml
Sitemap: https://www.greateasternlife.com/my/en/my-en-video-sitemap.xml
Sitemap: https://www.greateasternlife.com/private/en/sitemap.xml
Sitemap: https://www.greateasternlife.com/private/sc/sitemap.xml
Sitemap: https://www.greateasternlife.com/private/tc/sitemap.xml
200 https://www.greateasternlife.com/sg/en/personal-insurance.html 112154
  T: Announcement : Beware of impersonators claiming to be from Great Eastern or Great Eastern Financial representatives. Protect yourself against scams. Refer to our Security Advisory page (https://www.gr
  T: National schemes > MediSave-approved">
  T: MediSave-approved
  T: National schemes > MediSave-approved">
  T: MediSave-approved
  T: <span class=\"leo-icon leo-icon--color-icon leo-icon--custom-size\" data-width=\"48px\" data-height=\"48px\" data-type=\"external-link\">&nbsp;&nbsp;</span><span class=\"leo-font-bold font-size-inheri
  T: This link will bring you to a third-party website which Great Eastern has no control ("3rd Party Website"). Any use of the 3rd Party Website will be subject to and any information you provide will be 
  T: Local 1800 248 2888
  T: Overseas +65 6248 2888
  T: Product enquiries +65 6248 2211
  T: Great Eastern App
  T: Great Eastern Rewards App
  T: Great Eastern App
  T: App Store
  T: Great Eastern Rewards App
  T: App Store
  T: Privacy and security
## https://www.greateasternlife.com/sg/en/personal-insurance.html 200 https://www.greateasternlife.com/sg/en/personal-insurance.html
   https://uip.greateasternlife.com/econnect-new/#/login
   https://www.facebook.com/greateasternsingapore
   https://www.instagram.com/greateasternsg/
   https://www.tiktok.com/@greateasternsg
   https://www.linkedin.com/company/great-eastern-group
   https://www.youtube.com/GreatEasternSG
   https://greateasternsg.app.link/geapp/download/GE_page

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; G=./g2.py; python3 - <<'EOF'\nimport re,html\nexec(open('g2.py').read().split(\"if __name__ == '__main__':\")[0])\ncode, final, h, err = get('https://www.greateasternlife.com/sg/en/personal-insurance.html')\nt=text_of(h, keep_navfoot=True)\ni=t.find('Announcement')\nprint(t[i:i+600])\nfor m in re.findall(r'''href\\s*=\\s*[\"']([^\"']+)[\"']''', h):\n    if re.search(r'apple|play\\.google|security|scam|fraud|privacy|app\\.link|onelink|contact', m, re.I): print('  L:', html.unescape(m))\nEOF\nPICK='sg-en' python3 $G sitemap https://www.greateasternlife.com/sg/en/sg-en-sitemap.xml 2", "description": "Great Eastern announcement text and SG sitemap keyword grep"}

### [tool_result]
Announcement : Beware of impersonators claiming to be from Great Eastern or Great Eastern Financial representatives. Protect yourself against scams. Refer to our Security Advisory page (https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html) for more information. 
 Skip to main content 
 Personal Insurance 
 Products
 Life and health
 Life and health > Life">
 Life 
 Life and health > Health">
 Health 
 Life and health > Personal accident">
 Personal accident 
 Life and health > Critical illness">
 Critical illness 
 Wealth
 Wealth > Retirement income">
 Reti
  L: https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html
  L: /sg/en/corporate-solutions/contact-us-form.html
  L: /sg/en/customer-services/contact-us.html
  L: https://greateasternsg.app.link/geapp/download/GE_page
  L: https://greateasternsg.app.link/geapp/download/GE_page
  L: /sg/en/privacy-and-security-policy.html
## sitemap https://www.greateasternlife.com/sg/en/sg-en-sitemap.xml -> 200 1247 locs
## total urls 1247; keyword hits 169
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/customer-advisory-alliance-medinet-cyber-incident.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/dps-policyholders.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/eldershield-policyholders.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/general-public.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html
   https://www.greateasternlife.com/sg/en/about-us/investor-relations/email-alerts.html
   https://www.greateasternlife.com/sg/en/customer-services/dependants-protection-scheme-dps/apply-for-policy-top-up.html
   https://www.greateasternlife.com/sg/en/customer-services/dependants-protection-scheme-dps/change-payment-method-and-cpf-authorisation-for-dps.html
   https://www.greateasternlife.com/sg/en/customer-services/dependants-protection-scheme-dps/make-a-health-declaration-for-dps.html
   https://www.greateasternlife.com/sg/en/customer-services/dependants-protection-scheme-dps/opt-out-of-dps.html
   https://www.greateasternlife.com/sg/en/customer-services/dependants-protection-scheme-dps/reinstate-policy-for-dps.html
   https://www.greateasternlife.com/sg/en/customer-services/home-protection-scheme-hps/apply-for-exemption-from-hps.html
   https://www.greateasternlife.com/sg/en/personal-insurance/financial-planning/my-protection-explorer.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/lifestyle-protection.html
   https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html
   https://www.greateasternlife.com/sg/en/about-us/media-centre/media-releases/gefa-offer-advisory-securities-structured-deposits.html
   https://www.greateasternlife.com/sg/en/about-us/media-centre/media-releases/great-ev-protect.html
   https://www.greateasternlife.com/sg/en/about-us/media-centre/media-releases/my-protection-explorer.html
   https://www.greateasternlife.com/sg/en/about-us/media-centre/media-releases/singtel-home-protect.html
   https://www.greateasternlife.com/sg/en/about-us/media-centre/media-releases/singtel-home-protect-flexi.html
   https://www.greateasternlife.com/sg/en/about-us/sustainability/conducting-our-business-responsibly/cybersecurity-and-data-protection.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/10-things-to-know-about-pre-planning.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/2025-wrapped.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/4-reasons-need-life-insurance.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/5-reasons-you-should-change-your-will-as-you-age.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/5-things-for-end-of-life-planning.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/5-tips-to-prevent-sports-injuries-in-kids.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/6-reasons-to-buy-term-insurance-before-you-are-30.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/am-i-overpaying-for-insurance-in-singapore.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/are-low-premiums-the-only-sexy-thing-in-life-insurance.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/blue-zone-living-to-be-100-part-2.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/critical-illness-insurance-5-common-misconceptions-you-may-have.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/dear-young-singaporeans-why-wont-you-swipe-right-on-me.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/financial-planning.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/food-revelations-personality-test.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/how-great-life-multiplier-protects-grandparents-and-grandchildren.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/how-much-inheritance-should-you-leave-your-children.html
   https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/life-protection/how-to-leave-a-legacy-when-you-dont-have-millions.htm

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; ls raw | grep sg_en_sg_en_sitemap; f=$(ls raw/*sg_en_sg_en_sitemap* | head -1); grep -o '<loc>[^<]*</loc>' $f | sed 's/<[^>]*>//g' | grep -i -E 'scam|fraud|phish|impersonat|fake|beware|advisory|vigilant|sender|official-|security' | grep -v -i 'lifepedia/life-protection'; echo; grep -c '<lastmod>' $f; MAXC=6000 python3 g2.py page https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html", "description": "Refine GE sitemap grep and read Security Advisory page"}

### [tool_result]
www_greateasternlife_com_sg_en_sg_en_sitemap_xml_289f7c
https://www.greateasternlife.com/sg/en/privacy-and-security-policy.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/customer-advisory-alliance-medinet-cyber-incident.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/dps-policyholders.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/eldershield-policyholders.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/general-public.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html
https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html
https://www.greateasternlife.com/sg/en/about-us/media-centre/media-releases/gefa-offer-advisory-securities-structured-deposits.html
https://www.greateasternlife.com/sg/en/about-us/sustainability/conducting-our-business-responsibly/cybersecurity-and-data-protection.html
https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/career/why-financial-advisory-endures-as-a-career.html
https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/lifestyle-protection/be-wary-of-sms-phishing-scams-impersonating-land-transport-authority-lta.html
https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/4-tips-to-steer-clear-of-scams.html
https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-family-from-insurance-services-scams-singapore.html
https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-spot-investment-scam-singapore.html
https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/why-earning-more-does-not-always-lead-to-long-term-financial-security-in-singapore.html

1247
==========================================================================================
URL: https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html
STATUS: 200 FINAL: https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html 
BYTES: 87610 TITLE: Security Advisory | Privacy and Security Policy | Great Eastern Singapore
TEXTLEN: 10494
Skip to main content 
 Personal Insurance 
 Products
 Life and health
 Life and health > Life">
 Life 
 Life and health > Health">
 Health 
 Life and health > Personal accident">
 Personal accident 
 Life and health > Critical illness">
 Critical illness 
 Wealth
 Wealth > Retirement income">
 Retirement income 
 Wealth > Wealth accumulation">
 Wealth accumulation 
 Wealth > Our funds">
 Our funds 
 National schemes
 National schemes > Dependants' Protection Scheme">
 Dependants' Protection Scheme 
 National schemes > Great Legacy Programme">
 Great Legacy Programme 
 National schemes > MediSave-approved">
 MediSave-approved 
 Lifestyle
 Lifestyle > Travel">
 Travel 
 Lifestyle > Car">
 Car 
 Lifestyle > Home">
 Home 
 Lifestyle > Maid">
 Maid 
 Prestige series
 Prestige series > Prestige series">
 Prestige series 
 Life and health > Life">
 Life 
 Life and health > Health">
 Health 
 Life and health > Personal accident">
 Personal accident 
 Life and health > Critical illness">
 Critical illness 
 National schemes > Dependants' Protection Scheme">
 Dependants' Protection Scheme 
 National schemes > Great Legacy Programme">
 Great Legacy Programme 
 National schemes > MediSave-approved">
 MediSave-approved 
 Wealth > Retirement income">
 Retirement income 
 Wealth > Wealth accumulation">
 Wealth accumulation 
 Wealth > Our funds">
 Our funds 
 Lifestyle > Travel">
 Travel 
 Lifestyle > Car">
 Car 
 Lifestyle > Home">
 Home 
 Lifestyle > Maid">
 Maid 
 Prestige series > Prestige series">
 Prestige series 
 Explore
 QuickLinks > Financial planning">
 Financial planning 
 Reach for Great financial expertise and award-winning financial tools
 QuickLinks > Rewards and promotions">
 Rewards and promotions 
 Always here to surprise and delight you
 QuickLinks > Lifepedia">
 Lifepedia 
 Insurance and financial planning knowledge in digestible nuggets
 Corporate Solutions 
 For employees">
 For employees 
 For business">
 For business 
 Corporate wellbeing">
 Corporate wellbeing 
 Contact us">
 Contact us 
 About Us 
 Brand">
 Brand 
 Leadership">
 Leadership 
 Sustainability">
 Sustainability 
 Great Eastern Cares">
 Great Eastern Cares 
 Media Centre">
 Media Centre 
 Investor Relations">
 Investor Relations 
 Awards">
 Awards 
 Contact Us 
 Self-service guides 
 Log in
 Profile
 View portfolio">View portfolio 
 View profile">View profile 
 Change Password">Change Password 
 Sign Out">Sign Out 
 Search 
 Clear 
 Search 
 Popular searches 
 Critical illness ,
 GREAT CareShield ,
 Claims 
 Your search history 
 No search history
 Privacy and Security Policy 
 Security Advisory 
 Security Advisory</h2>\r\n<p>Great Eastern is committed to ensuring your security when you transact with us. We will never ask customers to:</p>\r\n<ol>\r\n<li>Disclose passwords, PINs or One-Time Passwords (OTPs)</li>\r\n<li>Transfer money to bank accounts not listed on our website<br>\r\n(Premium payments should be made through our <a href=\"/content/corp-site/sg/en/customer-services/payment/make-renewal-or-regular-premium-payments.html\">official payment channels</a>)</li>\r\n<li>Download unfamiliar applications or remote-access software</li>\r\n<li>Keep a transaction secret or act under pressure or threats</li>\r\n</ol>\r\n<p>For your peace of mind, our staff or financial representatives can send a follow-up email after a call at your request, to verify if the call is legitimate. In certain instances, we&nbsp;may send an email before we call.</p>\r\n"}}" data-query-param-personalise="false" id="text-52fce0bf17" class="cmp-text leo-mt-xl ">
 Security Advisory
 Great Eastern is comm

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; python3 - <<'EOF'\nimport re,html\nexec(open('g2.py').read().split(\"if __name__ == '__main__':\")[0])\ncode, final, h, err = get('https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html')\nt=text_of(h, keep_navfoot=True)\n# drop the escaped-json duplicates\nlines=[l for l in t.splitlines() if '\\\\r\\\\n' not in l and '\\\\\"' not in l]\nt2='\\n'.join(lines)\ni=t2.find('Check and Report')\nif i<0: i=t2.find('Hang up the call')\nprint(t2[i:i+5000])\nprint('-----LINKS')\nfor m in re.findall(r'''href\\s*=\\s*[\"']([^\"']+)[\"']''', h):\n    m=html.unescape(m)\n    if re.search(r'false-message|advisory|scam|fraud|apple|play\\.google|mailto|tel:', m, re.I): print('  L:', m)\nEOF", "description": "Extract rest of GE Security Advisory page"}

### [tool_result]
Check and Report A Suspicious Activity / Scam 
 Verify the source of communication 
 Check against Great Eastern’s official communication channels .
 Check if an SMS message from Great Eastern carries the "Likely Scam" identifier
(note : All official Great Eastern numbers are registered with the SMS Sender ID Registry and will not appear as “Likely Scam).
 Use the ScamShield app to check if a suspicious call, message or link is a scam.
 To report a suspicious activity / scam,
 Call the Great Eastern Customer Service hotline at 1800 248 2888 (9am to 5.30pm, Mondays to Fridays)
 Call the ScamShield Helpline at 1799, which is available 24/7. Alternatively, report a scam using the ScamShield app or website 
 Lodge a police report if a scam results in any financial loss
 To prevent unauthorized access to your Great Eastern app or eConnect account, you are strongly encouraged to 
 Change your password(s) immediately using the Forgot your password link on the login page
 Monitor your account(s) for unusual or unauthorised activity.
 Great Eastern’s Official Communication Channels 
 Displayed Customer Service Numbers on Caller IDs 
 Main: 6248 2888
 Group Insurance: 6248 2112
 Web Domains 
 greateasternlife.com
 greateasterngeneral.com
 greateasternfa.com.sg
 greateasternwomensrun.com
 Email Domains 
 xxx@greateasternlife.com
 xxx@e.greateasternlife.com (marketing)
 xxx@s.greateasternlife.com (servicing)
 xxx@sg.greateasternlife.com
 xxx@greateasterngeneral.com
 Financial Advisors (representatives)
 xxx@rep-sg.greateasternlife.com
 xxx@rep.GreatEasternFA.sg
 SMS Domains 
 GE-LIFE
 GE-GENERAL
 WhatsApp Business Account 
 Great Eastern’s official WhatsApp business account features a blue verification badge 
 WhatsApp Number: 8227 6993 (marketing)
 You will be redirected to an external link
">
 External Link Notification 
 This link will bring you to a third-party website which Great Eastern has no control ("3rd Party Website"). Any use of the 3rd Party Website will be subject to and any information you provide will be governed by the terms of the 3rd Party Website, including those relating to confidentiality, data privacy and security.
 Proceed 
 Contact us 
 Weekdays 9.00am to 5.30pm
 Local 1800 248 2888 
 Overseas +65 6248 2888 
 Product enquiries +65 6248 2211 
 About us 
 Company profile 
 Investor relations 
 Media Centre 
 Sustainability 
 Careers 
 Corporate 
 Financial representative 
 Financial Representative 
 Find a Financial Representative 
 Great Eastern Financial Advisers (GEFA) 
 Great Eastern Private Partners 
 Lifehub sign in 
 SurGE sign in 
 Check out our digital services 
 Great Eastern App
 Great Eastern Rewards App
 Great Eastern App
 Available on the 
 App Store 
 Get it on 
 Google Play 
 Great Eastern Rewards App
 Available on the 
 App Store 
 Get it on 
 Google Play 
 Terms and conditions 
 Marketing consent preferences 
 Privacy and security 
 Other Policies and Notices 
 Copyright © 2026 Great Eastern Holdings Limited (Reg No 1999 03008M)
 Great Eastern Holdings Ltd | The Great Eastern Life Assurance Company Limited | Great Eastern General Insurance Ltd
 Singapore 
 English 
 Select your country and language
 Singapore 
 English 
 中文 
 Malaysia 
 English 
 Malaysia (Takaful) 
 English 
 Bahasa 
 Indonesia 
 Bahasa 
 Indonesia 
 Brunei 
 English
-----LINKS
  L: https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html
  L: https://www.scamshield.gov.sg/check-for-scams/how-to-check-for-scams-on-scamshield-app/
  L: tel:18002482888
  L: https://www.scamshield.gov.sg/
  L: tel:18002482888
  L: tel:+6562482888
  L: tel:+6562482211

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; f=$(ls raw/*sg_en_sg_en_sitemap* | head -1); python3 - \"$f\" <<'EOF'\nimport re,sys\nx=open(sys.argv[1]).read()\nfor blk in re.findall(r'<url>(.*?)</url>', x, re.S):\n    if re.search(r'security-advisory|false-message|insurance-services-scams|medinet|general-public|steer-clear', blk):\n        print(re.sub(r'\\s+',' ',blk)[:300])\nEOF\ngrep -o -E 'https?://(apps\\.apple\\.com|play\\.google\\.com)[^\"'\"'\"' ]*' raw/*greateasternlife_com_sg_en_privacy_and_security_policy_security_advisory* | sort -u\nMAXC=2500 python3 g2.py page https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html 2>&1 | grep -v -E '^ (Life|Health|Wealth|National|Lifestyle|Prestige|Personal|Critical|Retirement|Our funds|Dependants|Great Legacy|MediSave|Travel|Car|Home|Maid|Explore|QuickLinks|Financial|Reach|Rewards|Always|Lifepedia|Insurance and|Corporate|For |Contact|About|Brand|Leadership|Sustain|Great Eastern Cares|Media|Investor|Awards|Self|Log in|Profile|View|Change|Sign|Search|Clear|Popular|GREAT|Claims|Your search|No search)' | head -60", "description": "GE sitemap lastmods, app links, eFiling false-message alert"}

### [tool_result]
 <loc>https://www.greateasternlife.com/sg/en/privacy-and-security-policy/customer-advisory-alliance-medinet-cyber-incident.html</loc> <lastmod>2026-10-24</lastmod> <changefreq>monthly</changefreq> <priority>0.5</priority> 
 <loc>https://www.greateasternlife.com/sg/en/privacy-and-security-policy/general-public.html</loc> <lastmod>2025-06-20</lastmod> <changefreq>monthly</changefreq> <priority>0.5</priority> 
 <loc>https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html</loc> <lastmod>2026-10-27</lastmod> <changefreq>monthly</changefreq> <priority>0.5</priority> 
 <loc>https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html</loc> <lastmod>2025-10-15</lastmod> <changefreq>monthly</changefreq> <priority>0.5</priority> 
 <loc>https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/4-tips-to-steer-clear-of-scams.html</loc> <lastmod>2023-12-07</lastmod> <changefreq>monthly</changefreq> <priority>0.5</priority> 
 <loc>https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-family-from-insurance-services-scams-singapore.html</loc> <lastmod>2026-01-08</lastmod> <changefreq>monthly</changefreq> <priority>0.5</priority> 
==========================================================================================
URL: https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html
STATUS: 200 FINAL: https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html 
BYTES: 79277 TITLE: False message on removal of e-filing | Privacy and Security Policy | Great Eastern Singapore
TEXTLEN: 6628
Skip to main content 
 Products
 GRE

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; python3 - <<'EOF'\nimport re,html\nexec(open('g2.py').read().split(\"if __name__ == '__main__':\")[0])\ncode, final, h, err = get('https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.html')\nt=text_of(h, keep_navfoot=True)\nlines=[l for l in t.splitlines() if '\\\\r\\\\n' not in l and '\\\\\"' not in l]\nt2='\\n'.join(lines)\ni=t2.find('Security Advisory')\nj=t2.find('You will be redirected')\nprint(code, t2[i:j][:2500])\nEOF\ngrep -l -i 'apple.com\\|play.google' raw/* | head; grep -o -h -i -E '(apps\\.apple\\.com|itunes\\.apple\\.com|play\\.google\\.com)[^\"&]{0,120}' raw/* | sort -u | head", "description": "Read GE eFiling false-message alert and find app store links"}

### [tool_result]
200 Security Advisory 
 False message on removal of e-filing 
 Great Eastern is aware of a false message circulating regarding removal of e-filing 
 Great Eastern is aware of a false message circulating on WhatsApp claiming that electronic filing submission (e-file) process for Parkway East Hospital, Mount Elizabeth Hospital, Mount Elizabeth Novena, and Gleneagles Hospital has been removed. e-file is a national Ministry of Health (MOH) system for submitting electronic claims from accredited facilities, such as hospitals and specialist clinics, to Integrated Shield Plan (IP) insurers. This system is mandatory and cannot be suspended by any insurer, including Great Eastern.
Great Eastern is investigating the source of this false message. Customers seeking or planning treatment can be assured their IP benefits and claim processes remain unchanged.
Customers are encouraged not to rely on unverified messages and to contact our customer service centre or their Financial Representative for any clarification.

### [tool_use WebSearch]
{"query": "Great Eastern Singapore scam alert impersonation fake website greateasternlife.com", "mode": "standard"}

### [tool_result]
Web search results for query: "Great Eastern Singapore scam alert impersonation fake website greateasternlife.com"

Links: [{"title":"greateasternlife.com","url":"https://greateasternlife.com/content/GreatEastern/sg/en/index.html"},{"title":"digital services","url":"https://greateasternlife.com/sg/en/personal-insurance/get-help/digital-services.html"},{"title":"Security Advisory","url":"https://greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html"},{"title":"20240109 swift intervention by great eastern ocbc and anti scam centre","url":"https://police.gov.sg/Media-Room/News/20240109_swift_intervention_by_great_eastern_ocbc_and_anti_scam_centre"},{"title":"20240109 swift intervention by great eastern ocbc and anti scam centre","url":"https://www.police.gov.sg/Media-Hub/News/2024/20240109_swift_intervention_by_great_eastern_ocbc_and_anti_scam_centre"},{"title":"greateasternlife.com","url":"https://greateasternlife.com/playday"},{"title":"20240109 swift intervention by great eastern ocbc and anti scam centre","url":"https://www.police.gov.sg/media-hub/news/2024/20240109_swift_intervention_by_great_eastern_ocbc_and_anti_scam_centre"},{"title":"greateasternlife.com","url":"https://greateasternlife.com/sg/en/personal-insurance/lifepedia/medical-coverage/hospitalisation.html"},{"title":"how to protect family from insurance services scams singapore","url":"https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-family-from-insurance-services-scams-singapore.html"},{"title":"greateasternlife.com","url":"https://greateasternlife.com/sg/en/personal-insurance/rewards.html"},{"title":"security policy","url":"https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html"},{"title":"greateasternlife.com","url":"https://greateasternlife.com/content/GreatEastern/bn/en/index.html"},{"title":"20241107 police advisory on phishing scams involving the impersonation of sp group","url":"https://www.police.gov.sg/media-room/news/20241107_police_advisory_on_phishing_scams_involving_the_impersonation_of_sp_group"},{"title":"security advisory","url":"https://www.greateasternlife.com/my/en/other-policies-and-notices/security-advisory.html"},{"title":"20241111 police advisory on impersonation scam variation","url":"https://police.gov.sg/Media-Room/News/20241111_police_advisory_on_impersonation_scam_variation"},{"title":"20180405 others advisory fake sg police website cid","url":"https://police.gov.sg/Media-Room/News/20180405_others_advisory_fake_sg_police_website_cid"},{"title":"20210217 police advisory phishing scams involving fake singtel website","url":"https://www.police.gov.sg/media-hub/news/2021/20210217_police_advisory_phishing_scams_involving_fake_singtel_website"},{"title":"www.greateasternlife.com","url":"https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/medical-coverage/disability.html"},{"title":"scam alert","url":"https://www.scamshield.gov.sg/resources/scam-alert/"}]

Based on the search results, here's what I found about Great Eastern scam alerts:

## Scam Alert Information

Great Eastern has been alerted of scammers impersonating as Great Eastern to direct recipients of emails to receive a cash refund. This email is not sent by Great Eastern, and you should not respond to the email.

## Key Security Warnings

Scammers may target you through SMS or emails and direct you to a phishing website to trick you into disclosing your Singpass login.

Be wary of messages claiming issues with your account or social media posting offering free gifts purportedly from Great Eastern, and do not click on any suspicious links which can be phishing links that lead you to fake Websites.

## How to Verify the Legitimate Website

If you wish to access the Great Eastern website, please type www.greateasternlife.com directly in your browser.

## Getting Help

For assistance, you can contact Great Eastern at 1800 248 2888 or wecare-sg@greateasternlife.com. Additionally, you can call the 24/7 ScamShield Helpline at 1799 if you are unsure if something is a scam.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2; python3 - <<'EOF'\nimport re,html\nexec(open('g2.py').read().split(\"if __name__ == '__main__':\")[0])\nfor u in ['https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html',\n          'https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-family-from-insurance-services-scams-singapore.html']:\n    code, final, h, err = get(u)\n    t=text_of(h, keep_navfoot=True)\n    lines=[l.strip() for l in t.splitlines() if '\\\\r\\\\n' not in l and '\\\\\"' not in l]\n    print('=====',u,code,final)\n    for m in re.findall(r'\"date(?:Published|Modified)\"\\s*:\\s*\"([^\"]+)\"', h)[:2]: print('JSONLD', m)\n    for m in re.findall(r'(?i)(?:published|updated|date)[^<]{0,40}(20\\d\\d)', h)[:3]: pass\n    hit=False\n    for i,l in enumerate(lines):\n        if re.search(r'scam|phish|fake|impersonat|www\\.|@|official|hotline|1800|SMS|whatsapp|never', l, re.I) and len(l)>15:\n            print('  ', l[:260])\nEOF", "description": "GE security-policy page and insurance-scams article"}

### [tool_result]
===== https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html 200 https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html
   Before entering your user ID and password, you should always ensure that the website you are visiting belongs to Great Eastern. This can be verified by the URL displayed in your browser as well as the Great Eastern's URL in its digital certificate. To verify t
   4. Avoiding Hoax Emails (Phishing emails)
   6. Protect yourself from Smishing (SMS Phishing)
   7. Vishing (Voice Phishing)
   Never use the same password for other web-based services (Financial or Non-Financial) such as for email, online services, particularly when they related to different websites.
   Malicious program (or malware) is usually sent as an attachment or URL link (when clicked, will redirect to websites embedded with malicious contents) in emails claiming to be from someone you know, or disguised as genuine software coming from an official site
   4. Avoiding Hoax Emails (Phishing emails)
   Phishing are fraud emails sent by fraudsters which trick you into providing your personal information, or downloading a virus that can steal your information.
   When in doubt or suspicious about the authenticity of the request, do not provide personal or financial information, always double-check with Great Eastern. Contact us via our official channels: www.greateasternlife.com. Never rely on any information or link f
   Never click onto a link in an email to go to the GE login page. Always access GE by typing the full website address www.greateasternlife.com into your browser.
   Never send sensitive information by email.
   Never download files from PCs or sites which you aren't sure about its safety.
   Never blindly type commands that others tell you to type, or go to web addresses mentioned by strangers, or run pre-fabricated programs or scripts
   Customers are also encouraged to use the latest versions of Internet browsers available, which may provide advanced security features such as anti-phishing and forged website identification. If such features are available, customers are advised to turn them on
   6. Protect yourself from Smishing (SMS Phishing)
   Smishing or SMS Phishing is a phishing scam used in mobile devices. Fraudsters send you text messages that contain different methods of capturing your personal banking information by pretending to be representatives of legitimate organisations.
   You receive unsolicited text messages (SMS) from representatives claiming to be from organisations such as your Bank, Insurance company or Internet Service Provider. When you call or reply back, they ask questions that lead you to reveal personal banking infor
   Never reply to SMSes, calls or emails on transactions that you did not perform. Do not reply to a text message that asks for your confidential information either.
   Never click on any website links found in unsolicited SMS or multi-media messages (MMS) from unknown sources. Do not reply to such SMSes and delete them immediately.
   7. Vishing (Voice Phishing)
   Vishing (also known as Voice Phishing) is a form of phishing, where the attacker uses a phone call to lure you into giving your personal or policy information. The phone call can either be live or automated.
   You receive a suspicious call or voice mail claiming that your policy account will be cancelled if you do not call their hotline and enter your personal information.
   Validate that the calls you receive about Great Eastern policy account are from trustworthy sources by contacting our customer service hotline.
   Some smart phones have features that allow data synchronisation between your mobile device and online storage or cloud services in near real time. Information that could be synchronized includes SMS, email, etc.
   If you have enabled the abovementioned data synchronisation, sensitive information sent via SMS or emails by financial institutions (FIs), such as one-time passwords (OTPs), could be accessed by criminals if your login credentials to the online storage or clou
   If you suspect that security breaches may have occurred and online transaction(s) might have been fraudulently accessed please do not hesitate to call our Hotline help: 1800 - 248 2888 or E-mail us at : wecare-sg@greateasternlife.com .
   Local 1800 248 2888
===== https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-family-from-insurance-services-scams-singapore.html 200 https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-family-from-insurance-services-scams-singapore.html
   How to protect your family from insurance services scams in Singapore
   How to protect your family from insurance services scams in Singapore
   Financial Literacy 101: How to spot an insurance services scam and what you should do
   By the time the caller ends the conversation, some people find themselves sharing sensitive information, making payments, or even transferring their own money. Not because they were careless, but because the interaction sounded official, procedural, and famili
   These are not get-rich-quick frauds. They are insurance services scams , designed to resemble routine insurance housekeeping and administrative follow-ups.
   According to the Singapore Police Force’s Mid-Year Scam and Cybercrime Brief 2025, insurance services scams emerged as a distinct scam category in 2025, with 791 reported cases and approximately S$21.3 million in losses in the first half of 2025 alone . That s
   What is an insurance services scam?
   An insurance services scam involves scammers impersonating insurance staff or service administrators and convincing you that there is an issue with an insurance service linked to your name.
   The scam escalates when the caller guides you into actions that cause financial loss, such as:
   What distinguishes insur

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)