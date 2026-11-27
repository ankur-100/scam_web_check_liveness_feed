# Generic phishing / scam / malicious-URL feeds — SG-filterability

Captured 2026-11-25. Samples in
`/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/feeds/` (scratch, may be gone).
Tagger used for all counts: `sources/sgfilter.py` (copy of the scratch script; usage `python3 sgfilter.py NAME FILE...`).
Rules followed: documented public endpoints only, no accounts/keys, one download per feed (plus the
documented JSON variant of Phishunt), malicious URLs never visited.

## TL;DR

- **Only one free, no-key feed has real SG volume: Phishing.Database** (mitchellkrogza / PyFunceble-tested).
  445 unique SG-targeted hosts in `phishing-links-ACTIVE.txt` (dbs/paylah 250, "singapore" 77, carousell 52,
  posb 30, singtel 28, paynow 15, singpost 4). But **no timestamps and no brand field** — lifecycle comes only
  from the ACTIVE/INACTIVE split and git history.
- Every other open feed yields **0–30 SG-targeted entries**. Most open feeds are dominated by
  Western/crypto/Polish/Indonesian brands. SG-native phishing (Carousell→PayNow/DBS kits, PayLah, Singtel,
  SingPost) is under-represented in global community feeds.
- **Host geolocation ≠ SG targeting.** PhishStats `countrycode=SG` (100/100 sample: 97 Tencent Cloud SG) and
  urlscan `page.country:SG AND task.tags:phishing` (100/100: Tencent EdgeOne `*.edgeone.dev`) returned
  **0 SG-brand hits**. Treat IP/ASN-in-SG as noise, not a filter.
- **`.sg` ccTLD ≠ SG targeting either**: 144 of 201 TierA hits in Phishing.Database domains are `.sg` hosts,
  overwhelmingly compromised SG SME sites / `blogspot.sg` hosting *non-SG* phish (Office365, KeyBank…).
  Useful as a separate "SG-hosted" label, not as "SG-targeted".
- **2026 access changes:** abuse.ch (URLhaus/ThreatFox/MalwareBazaar) file exports return **410 Gone without a
  free Auth-Key since 2026-10-21**; PhishTank new-user registration still closed (since 2020) and anonymous
  `online-valid.csv.bz2` returned a placeholder image; urlscan anonymous search blocks wildcards and
  `verdicts.*`; OTX search needs a key; PhishStats moved to a JSON API (CSV gone, 50 req/day anon).
- Brand-tagged feeds with lifecycle fields (OpenPhish Premium, APWG eCX, PhishTank, Netcraft, CheckPhish
  feeds) are all gated (paid / membership / closed registration).

## Comparison table

SG-tgt = entries matching a TierA SG-brand token (excl. ccTLD-only), measured on today's sample.
"Lifecycle" = first_seen / last_seen / online-status / takedown fields.

| Feed | Endpoint | Access (2026-11) | Format | Brand field | Country/geo | Lifecycle fields | Volume (sample) | Update | Licence | SG-tgt measured | SG-filterability |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Phishing.Database** | `raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-{links,domains}-ACTIVE.txt` (+INACTIVE, NEW-today, NEW-last-hour) | free, no key (GitHub) | txt, 1/line | no | no | ACTIVE/INACTIVE/INVALID status (PyFunceble re-test); NEW-today / NEW-last-hour; git history = first-seen | 789,054 links / 392,178 domains active | multiple/day | MIT | **links: 633 entries / 445 hosts; domains: 54** | **High (keyword)** — URL path keeps kit paths like `/bank/dbs/`, `/posb/`, `/singtel/` |
| PhishDestroy destroylist | `raw.githubusercontent.com/phishdestroy/destroylist/main/list.json` | free, no key | JSON list of domains (live page shows timestamp/registrar/IP) | no | no (IP on live page) | append-only; detect time on live page only | 233,711 | continuous | CC-BY-4.0 | 14 (+436 Shopee-ID) | Medium — domain-only keyword |
| ScamSniffer scam-database | `raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/domains.json` (+ `blacklist/archive/YYYY-MM-DD.json`) | free, no key; real-time API by contact | JSON list | no | no | daily archive files = first-seen date; **7-day publication delay** | 363,150 | daily | GPL-3.0 | 11 (mostly crypto noise) | Low — Web3 drainers only |
| Phishing Army (extended) | `phishing.army/download/phishing_army_blocklist_extended.txt` | free, no key | txt domains | no | no | none (current snapshot) | 146,516 | not stated | generator GPL-3.0; list inherits upstream terms (PhishTank/OpenPhish ToU) | 4 | Low–Med; aggregator of PhishTank/OpenPhish/CERT.PL/Phishunt/urlscan/PhishStats/… |
| PhishStats API | `api.phishstats.info/api/phishing?_where=(url,like,~kw~)` | free anon 50 req/day; key for more | JSON | no (title only) | **countrycode, ASN, ISP, IP** | `date`, `date_update`, `http_code`, `domain_registered_n_days_ago`, score | — (query) | 90 min | free use (see site) | `countrycode=SG`: 1/100; `~paylah~`: 1; `~carousell~`: 19 (2025-12→2026-06); `~singpass~`: 0 | Med — server-side URL `like` query works; geo field is a trap |
| TweetFeed | `raw.githubusercontent.com/0xDanielLopez/TweetFeed/master/{today,week,month,year}.csv` | free, no key | CSV: date,user,type,value,tags,tweet | no (hashtags) | no | tweet date | 95,911 rows/yr (81,729 url/domain) | ~15 min | see repo | 2 hosts | Low |
| OpenPhish Community | `openphish.com/feed.txt` = `raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt` | free, ToU | txt URLs | **no** (brand/geo/ASN/language only in Premium) | no | none | 300 | 12 h | ToU (non-commercial) | 0 (2 Shopee-ID) | Low on community tier; Premium would be High |
| Phishunt | `phishunt.io/feed.{txt,json,csv}`, `/api/v1/domains`, `/api/v1/campaigns` | free, no key, 10 req/s | JSON/CSV/TXT/STIX | **`company`** (fixed ~60-brand list, none SG) | country, ASN, org | `first_seen`, `date`, multi-source verdict flags | 792 | hourly | not stated | 0 | Low — brand list has no SG brands |
| CERT Polska warning list | `hole.cert.pl/domains/v2/domains.{txt,csv,json,xml}` | free, no key | txt/csv/json | no | no | InsertDate / DeleteDate (csv/json), 6-month retention | 127,084 | 5 min | free incl. commercial | 1 (FP) | None — Polish-targeted by scope |
| PhishTank | `data.phishtank.com/data/[appkey/]online-valid.{csv,json}.bz2` | **registration closed since 2020**; anon "a few downloads/day" — today returned a placeholder JPEG | csv/json/xml | **`target`** | IP/CIDR/ASN in details | submission_time, verification_time, `online` | n/a (blocked) | hourly | Cisco ToU | not measured | High *if* you already hold a key |
| URLhaus (abuse.ch) | `urlhaus-api.abuse.ch/v2/files/exports/<AUTH-KEY>/recent.csv` | **free Auth-Key required since 2026-10-21** (legacy URL → 410) | CSV | no (tags, threat) | no | dateadded, url_status online/offline, last_online | n/a | 5 min | CC0 | not measured | Low for phishing (malware-distribution URLs); useful for APK droppers |
| ThreatFox | `threatfox-api.abuse.ch/v2/files/exports/<KEY>/recent.csv` | free Auth-Key | CSV | malware family | no | first_seen, last_seen, ≤6 months | n/a | 5 min | CC0 | — | Low |
| MalwareBazaar | API `mb-api.abuse.ch/api/v1/` (key); `datalake.abuse.ch/malware-bazaar/{hourly,daily}/` (no key, zipped samples) | free Auth-Key for API | JSON | signature/tags | **`origin_country`** (uploader) | first_seen | n/a | hourly | CC0 | — | Med for SG Android-malware scams: `file_type:apk` + tags/signature + `origin_country:SG` |
| urlscan.io search | `urlscan.io/api/v1/search/?q=…` | anon: 30-day window, no wildcards, no `verdicts.*`; free account unlocks wildcards; brand fields Pro-only | JSON | `task.tags`, Pro `brand.*`/`visible.brandname` | `page.country`, `page.asn` | task.time, domainAgeDays, tlsAgeDays | 10,000+ phishing-tagged SG-hosted /30d | live | ToS | 0/100 (SG-hosted query) | Med with free account (`page.domain:*dbs*` etc.); High with Pro brand fields |
| AlienVault OTX | `otx.alienvault.com/api/v1/search/pulses` | **key required** (403 anon) | JSON | pulse tags, `targeted_countries` | yes (pulse-level) | created/modified | — | live | ToS | not measured | Med (pulse-level, sparse) |
| crt.sh | `crt.sh/?q=%25kw%25&output=json` | free, no key | JSON | — | — | not_before/not_after | — | live | free | `%singpass%`: 23 legacy certs only (all real gov.sg); `%paylah%`: 502 | Low via crt.sh (infix search unreliable); High via self-hosted Certstream |
| Certstream / CT tail | `certstream-server-go` (self-host; Calidog public server unreliable) | free, self-host | websocket JSON | — | — | cert issuance time = earliest signal | ~all new certs | real-time | OSS | not measured | **High** for *pre-attack* typosquats of SG brands |
| dnstwist-style permutation | `dnstwist` tool on SG brand domains | free tool | — | implicit (seed brand) | — | registration date via WHOIS/RDAP | — | on demand | Apache-2.0 | not run | High precision for lookalikes; misses `carousell.<random>.shop` style |
| Google Safe Browsing | v4/v5 Lookup API | free Google Cloud key, non-commercial | JSON | threatType only | no | none | lookup only | — | ToS | — | Verification only (is URL flagged?) |
| Spamhaus DBL / SURBL | DNS zones `dbl.spamhaus.org`, `multi.surbl.org` | free low-volume non-commercial (DQS key for Spamhaus) | DNS lookup | return code = category | no | none | lookup only | — | usage policy | — | Verification/enrichment only |
| Chainabuse (TRM) | `api.chainabuse.com/v0/reports` | key (contact); geolocation Pro-only | JSON | scam category | Pro only | createdAt | — | live | proprietary | — | Low–Med (crypto/investment) |
| CryptoScamDB | `github.com/cryptoscamdb` | repo stale | — | — | — | — | ~6.5k (legacy) | inactive | — | — | Not worth it |
| CheckPhish / Bolster | `checkphish.bolster.ai` | free key 25 scans/day; no free feed | JSON | brand | yes | — | lookup only | — | ToS | — | Verification only |
| Netcraft | report API / browser ext; feeds commercial | paid | — | brand | yes | yes | — | — | — | — | High but paid |
| APWG eCX | `apwg.org/ecx` | membership ($1.5k+) or Researcher Data Grant | API | **brand**, URL, confidence | — | dates | 100s–1000s/day | live | member terms | — | High — best brand-tagged option via research grant |
| GASA Global Signal Exchange | `gasa.org/global-signal-exchange` | vetted orgs only | platform | signal type | — | — | 135M+ signals | live | partner terms | — | Potentially High; institutional route (cf. SG gov/FI partners) |
| APCERT / SingCERT / AusCERT | — | no public feed found; AusCERT Malicious URL Feed = members | — | — | — | — | — | — | — | — | n/a |

## Per-feed notes

### Phishing.Database (best open source)
- 789,054 ACTIVE links, 392,178 ACTIVE domains; plus INACTIVE / INVALID / NEW-today / NEW-last-hour lists.
  ACTIVE = still resolving/responding in PyFunceble's last test (not "verified phish"). MIT.
- SG-targeted (links): 633 entries / **445 unique hosts**. By brand (unique hosts): dbs/paylah/digibank 250,
  "singapore" 77, carousell 52, posb 30, singtel 28, paynow 15, singpost 4, ocbc 3, gov-sg 2, uob 1, singpass 1.
  TLDs of those hosts: .com 102, **.top 50, .shop 30**, .life 29, .id 21, .info 20, .app 17, .xyz 11 — overlaps
  SPF advisory TLD set (.top/.shop/.cfd/.vip).
- Examples: `https://dbsbank-sg.club`, `https://paylahsg.info`, `https://carousell-sg.checkout75104.online/bank/dbs/…`,
  `https://check-singpost.homes`, `https://paynow-carousells.firebaseapp.com/dbs/index.html`,
  `posb-sg.com`, `ocbcc-sg-bankiingsg.com`, `mysingtel-app-manager.com`.
- Precision: 40-host random spot check ≈ 75–80 % genuinely SG-targeted. False positives come mainly from the
  generic `singapore` token (e.g. M&T kit with `country=singapore` param, Malaysian/Indonesian lures),
  `vcbdigibank` (Vietcombank), and US/UK "mytax" pages (now moved to TierB).
- Lifecycle gap: no first_seen. Workarounds: (a) poll `NEW-today` daily and stamp it yourself;
  (b) `git log` the repo to date when a line first appeared; (c) ACTIVE→INACTIVE transition gives a takedown proxy.

### PhishDestroy destroylist
- 233,711 domains, CC-BY-4.0, append-only since 2025-07. Crypto-heavy but broader than ScamSniffer.
- SG-targeted 14: `paynow-sg.cfd`, `dbssg.net`, `boc.carousellcool.cfd`, `carousell.shoproductinfob.shop`,
  `carousellref.market-receive.bond`, `singteltrading.com`. Also 436 Shopee hits — almost all Indonesian
  (`*shopeepay.com`, `bantuanshopee.biz.id`) → regional, not SG.
- The JSON list is domain-only; timestamps/registrar/IP only visible on the live page (not a documented bulk field).

### ScamSniffer
- 363,150 Web3 phishing domains, GPL-3.0, daily archive files give a first-published date (with 7-day lag).
- SG hits are mostly noise: `ocbcdefi.*` (crypto, not the bank), `cryptopunks.sg`, `nft.sg`. Genuine: `carousell.vip`,
  `carousell-sg.offer5991.bid`. Only relevant for SPF's crypto/investment-scam category.

### Phishing Army (extended)
- 146,516 domains aggregated from PhishTank, OpenPhish, CERT.PL, Phishunt, urlscan, PhishStats, StalkPhish,
  URLAbuse, AntiPhish.org; Tranco-allowlisted. No metadata.
- SG-targeted 4: `carousell.nextervis.com`, `dbsbank.loan`, `digibankmitra.edgeone.dev` (+ `dbs-secure.vercel.app` TierB).
  Useful mainly as a cheap union of several gated feeds' *current* state.

### PhishStats
- CSV feed (`phish_score.csv`) now 404; replaced by JSON API (`api.phishstats.info/api/phishing`), 50 anon req/day,
  rich fields: `countrycode, asn, isp, bgp, ip, title, date, date_update, score, http_code, tld,
  domain_registered_n_days_ago, ssl_*, tags`.
- `countrycode=SG` latest 100 (2026-11-20→24): 97 Tencent SG, 0 SG brands. Brand queries: `url like ~carousell~` → 19
  (2025-12-14→2026-06-02, e.g. `carousell.nextervis.com/bank/dbs/…`, `carousell-hk.sangiorgi.shop/…/banks/dbsnew/iframe.htm`);
  `~paylah~` → 1 (`irreversiblechoice.xyz/dbspaylah199fs-sgc/`); `~singpass~` → 0.
- Best use: periodic server-side keyword queries (one per SG brand; ~20 req/day fits anon quota) — returns dated rows.

### urlscan.io
- Anonymous: 30-day lookback, no leading wildcards/regex (403), `verdicts.malicious` blocked. Free account removes
  the wildcard block. Brand classification (`brand.*`, `visible.brandname`) is Pro-only.
- `task.tags:phishing AND page.country:SG` → 10,000+ in 30 days, but the 100 sampled were all Tencent EdgeOne SG
  edge nodes hosting non-SG lures (0 SG brands). Again: hosting geo is a trap.
- With a free account, queries like `page.domain:*carousell* AND NOT page.apexDomain:carousell.sg` or
  `page.title:"Singpass"` are the realistic route; each result has screenshot + DOM = strong labelling evidence.

### TweetFeed
- 95,911 rows/yr (44k URLs, 38k domains), hashtags only. 2 SG hosts: `digibankbydbsiidcc.univer.se`,
  `uob-bk6-…azurefd.net/S163DE_Voluntary_package.zip` (TierB). Low yield.

### OpenPhish Community
- 300 URLs per 12 h snapshot, no metadata; 0 SG hits today (2 Indonesian Shopee). Premium/Platinum add brand,
  GeoIP, ASN, language, 30-day archive (paid; "Premium Gov Feed at no cost" for law enforcement — relevant if SPF
  partner route exists).

### Phishunt
- 792 hosts, nice schema (`company`, `first_seen`, `country`, `asn`, multi-source verdicts, campaign clustering), but
  its brand dictionary (~60 brands: facebook, microsoft, allegro, dpd…) has **no SG brands** → 0 hits. Its
  `/api/v1/analyze` could still be used per-URL.

### CERT Polska
- 127,084 domains, InsertDate/DeleteDate, excellent lifecycle — but scoped to Polish targets (1 FP hit). Useful as
  a *schema model* for our own dataset, not a source.

### PhishTank
- New-user registration closed since 2020 and still closed (2026). Anonymous `online-valid.csv.bz2` returned a
  "No screenshot yet" JPEG instead of data today. Has `target` + `online` + verification timestamps — the best open
  lifecycle schema, but not obtainable without an existing key.

### abuse.ch (URLhaus / ThreatFox / MalwareBazaar)
- All legacy export URLs returned **HTTP 410** with: "Since 21 October 2026, abuse.ch file exports need an Auth-Key".
  Auth-Key is free (auth.abuse.ch). Not obtained per rules.
- URLhaus = malware *distribution* URLs (url_status online/offline, dateadded, last_online) — relevant for SPF
  "malware-enabled scams" (APK droppers served from fake tour/cruise/food sites).
- MalwareBazaar: `get_file_type apk` / `get_taginfo` + `origin_country` + signature; SG Android scam APKs
  (accessibility-abuse bankers targeting DBS digibank etc., per SPF 2026-06-18 advisory) would need manual tagging.
  Hourly/daily zipped sample batches on `datalake.abuse.ch` are keyless but contain binaries, not metadata.

### Certificate transparency (crt.sh / Certstream) and dnstwist
- crt.sh `%singpass%` returned only 23 certificates, all genuine `*.singpass.gov.sg` 2009–2017 — infix search is
  clearly truncated/unreliable; `%paylah%` → 502. Don't rely on crt.sh for substring discovery.
- Recommended: self-hosted `certstream-server-go` (v1.9 supports static-CT logs), regex on SAN for the SG brand
  token list below. This catches domains like `dbsbank-sg.club` at cert issuance, often before they appear in any
  feed — but it yields *candidates*, not confirmed phish (needs urlscan/GSB confirmation).
- dnstwist on `dbs.com.sg, singpass.gov.sg, carousell.sg, singpost.com, ocbc.com, uob.com.sg, iras.gov.sg, …`
  catches lookalikes but misses the dominant SG pattern seen here: brand as subdomain/prefix on throwaway TLDs
  (`carousell.<random>.shop`, `paylah<N>.top`).

### Gated / institutional
- APWG eCX: brand + URL + confidence since 2003; researcher data grant exists → best path to brand-tagged history.
- GASA Global Signal Exchange (Google + DNS RF): 135M+ signals, vetted orgs; plausible via SG institutional partner.
- OTX: key required (free account). Pulses have `targeted_countries`, but coverage is analyst-driven and sparse.

## Recommended SG-filter recipe

1. **Ingest** (free, no key): Phishing.Database `phishing-links-NEW-today.txt` daily + `phishing-links-ACTIVE.txt`
   weekly; PhishDestroy `list.json`; Phishing Army extended; PhishStats API keyword queries (one per brand/day).
   With free accounts (if allowed later): abuse.ch Auth-Key (URLhaus recent.csv, MalwareBazaar APK queries),
   urlscan.io wildcard brand queries, OTX.
2. **Normalise** to `(url, host, path, feed, fetched_at)`; keep the full URL — SG kit paths (`/bank/dbs/`, `/posb/`,
   `/singtel/`, `/dbs/index.html`) are the strongest signal and are lost in domain-only feeds.
3. **Tag tiers** (implemented in `sgfilter.py`):
   - **TierA (SG-native, high precision)**: `singpass`, `singpost|sgpost|singapore-?post`, `ocbc`(bounded),
     `posb`(bounded), `dbsbank|dbs-?bank|digibank|paylah|dbs-?sg`, `uobgroup|uob-?sg`, `ninja-?van`, `carou-?sell`,
     `simply-?go`, `singtel`, `starhub`, `onemotoring|lta-?gov|lta-?sg`, `ez-?link`, `paynow`(bounded),
     `cdc-?voucher|redeem-?cdc`, `cpf-?board|cpf-?sg`, `iras-?gov|iras-?sg`, `ica-?gov|ica-?sg|sgarrival`,
     `gov-?sg|govsg|\.gov\.sg`, `police-?sg|spf-?gov`, `hdb-?gov|myhdb`, `singapore` (excluding `ap-singapore`
     cloud-region hostnames). Reject a match if it sits inside an alnum run > 24 chars (random hashes).
   - **TierB (ambiguous short tokens, require SG context)**: `dbs, uob, lta, iras, ica, cpf, hdb, grab, mytax`
     word-bounded — accept only if the URL also contains `sg|singapore|.sg|gov-sg|sgd`. Known collisions:
     `cpf` = Brazilian tax ID (Itaú/Bradesco/Santander kits), `ica` = Swedish ICA Banken + Indonesian WhatsApp
     "grup ica" lures, `grab` = crypto "grab airdrop", `lta` = `poste.lta` Italian kit, `mytax` = US/UK tax.
   - **Regional (keep separate)**: `shopee`, `lazada`, `grab` — mostly Indonesian/Malaysian/Philippine/Brazilian
     targets (`shopee-br`, `bantuanshopee.biz.id`); only keep with SG context (`shopee.sg`, `-sg`).
   - **SG-hosted label (not SG-targeted)**: host ends `.sg`, or IP geolocates/ASN in SG. Record but don't count.
4. **Verify**: TierA+TierB-with-context candidates → urlscan.io lookup (screenshot/title/language) or GSB lookup;
   drop anything whose rendered title/brand isn't SG. Expect ~75–80 % keyword precision before verification.
5. **Lifecycle**: since open feeds lack first/last-seen, stamp `first_seen_in_feed` at ingestion and re-poll
   Phishing.Database ACTIVE/INACTIVE (or a HEAD/DNS check) to derive `last_seen_active`. Use cert `not_before`
   (CT) and RDAP creation date as an "infrastructure birth" marker. PhishStats rows already carry `date`.
6. **Join to SPF advisories**: map TierA brand → SPF impersonated-brand list (LTA, SPF, IRAS, ICA, CPF, Singpass,
   DBS, UOB, OCBC, SingPost, Ninjavan, Lazada, Shopee, Carousell, Grab, Singtel, CDC, SimplyGo) and compare TLD mix
   (.top/.shop/.cfd/.vip/.cc) as a cross-check.

## Measured SG hit counts (2026-11-25 samples)

| Feed (sample) | Entries | TierA any | **SG-targeted (excl. ccTLD-only)** | unique hosts | Regional (Shopee/Lazada) |
|---|---|---|---|---|---|
| Phishing.Database links ACTIVE | 789,054 | 888 | **633** | **445** | 113 |
| Phishing.Database domains ACTIVE | 392,178 | 201 | **54** | 54 | 50 |
| PhishDestroy | 233,711 | 29 | 14 | 14 | 441 |
| ScamSniffer | 363,150 | 22 | 11 (mostly crypto FP) | 11 | 1 |
| Phishing Army extended | 146,516 | 5 | 4 | 4 | 13 |
| TweetFeed (year) | 81,729 | 11 | 2 | 1 | 4 |
| CERT Polska | 127,084 | 1 | 1 (FP) | 1 | 0 |
| PhishStats `countrycode=SG` (100) | 100 | 1 | 1 | 1 | 0 |
| PhishStats `url~carousell~` / `~paylah~` / `~singpass~` | 19 / 1 / 0 | — | 19 / 1 / 0 | — | — |
| urlscan `phishing AND page.country:SG` (100) | 100 | 0 | 0 | 0 | 0 |
| Phishunt | 792 | 0 | 0 | 0 | 0 |
| OpenPhish community | 300 | 0 | 0 | 0 | 2 |
