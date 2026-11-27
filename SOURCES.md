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
which make up most SG losses and most SPF advisories. For those, the authority lists (SPF, MAS) are the only
open source, and the global feeds don't cover them at all.

## Suggested pipeline (not built)

1. Daily: `extract.py` (SPF) + OpenSanctions MAS + Phishing.Database through `sgfilter.py`.
2. Normalize to `{indicator, type, source, first_seen_by_us, last_seen_by_us, brand, category, gov_entity}`.
   Our own first/last-seen stamps are the only reliable lifecycle signal, since no source except OpenSanctions has one.
3. Liveness: DNS plus an HTTP status check (no rendering) to decide active or inactive.
4. Brand → canonical entity table (LTA, IRAS, ICA, …), keyed on the SPF tag UUIDs and extended with SG service
   vocabulary (onemotoring, erp, parking, simplygo, cdc, sgac, paynow).
5. Worth applying for: APWG eCX researcher grant (brand-tagged, lifecycle-stamped, global).

## Not done / caveats
- I didn't query the Directus backend of icanact or MAS's undocumented search backend.
- Cloudflare- or 403-blocked sites were not bypassed: ScamAdviser, Scam-Detector, Carousell help centre, M1.
- Precision of `sgfilter.py` comes from a 40-host spot check, not a labelled evaluation.
- The OpenSanctions → SPF overlap (0) used regex-extracted hosts from the simple CSV, which may be mostly email
  domains. A proper comparison should use the website field in `source.json`.
