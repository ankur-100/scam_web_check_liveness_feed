# Singapore official / regulator scam-data sources: catalogue

Compiled 2026-11-25. Purpose: find sources that complement the icanactagainstscams.gov.sg `/scam-trends` feed (209 SPF advisories, Aug 2025 to Nov 2026, already in `../advisories.jsonl`).

How this was gathered: user-facing pages, robots.txt, sitemaps, RSS, published downloads, the documented data.gov.sg v2 API, the GitHub REST API, and OpenSanctions' published bulk files. No undocumented backend or CMS endpoints were requested. Where a page's own backend is named below, the name comes from third-party open-source code. I did not call it.

## Bottom line

- **No SG government body publishes a machine-readable scam domain, URL or phone IOC feed.** The operational lists sit behind closed doors: SPF SATIS (52,200 malicious websites disrupted in 1H 2026), the National Scams List (shared with banks and telcos), OCHA directions, ScamShield app reports, and the IMDA/GRA blocking lists.
- The **only official list with per-entity IOCs** (websites, phones, emails, dates) is the **MAS Investor Alert List**, and OpenSanctions republishes it daily as clean bulk files.
- **SPF news (police.gov.sg)** can backfill icanact's history: 354 scam-advisory URLs from 2021 to 2026, all listed in a public sitemap. Most IOCs in them are inside images, though.
- **CSA has real RSS feeds** (alerts and advisories). They are low on IOCs but the cleanest feed format available.
- Several **allowlists** are useful for spotting look-alike brands: gov.sg Trusted Sites, MAS FID, the SSIR organisation list, the ScamShield bank hotlines, the MinLaw moneylender list, and ACRA UEN on data.gov.sg.
- **data.gov.sg has no scam IOC datasets.** It only has aggregate crime counts, and those are out of date.

## Ranked table (ranked by usefulness for an SG scam-domain/IOC dataset)

| # | Source | Publisher | Entities | ~Records | Machine-readable? | Freshness | Key fields | Licence / ToU |
|---|---|---|---|---|---|---|---|---|
| 1 | MAS Investor Alert List (IAL), https://www.mas.gov.sg/ial | MAS | Unregulated or impersonating investment entities: names, aliases, **websites, phones, emails**, addresses | **924 entities**. 786 have websites (~1,055 URL tokens), 500 have phones, 256 have emails | MAS: no. It is a JS search widget (`bundle.search-ial.1.0.0.js`). **OpenSanctions bulk: yes**: `https://data.opensanctions.org/datasets/latest/sg_mas_investor_alert/{targets.simple.csv, entities.ftm.json, targets.nested.json, source.json, index.json}` | Latest addition 17 Nov 2026. 30 additions in 2026, 66 in 2025. OpenSanctions re-crawls daily | `date_s`/`date_dt` (listing date; missing on 156 records), `modifieddate_dt`, `approveddate_dt`, `website_s`, `phonenumber_s`, `email_s`, `alternativename_s`, `formername_s`, `notes_s` (34 say "impersonates a financial institution…", naming the brand), `relatedunregulatedpersons_s`. No status or expiry field | MAS site ToU. OpenSanctions files are **CC-BY-NC 4.0** (commercial use needs a licence) |
| 2 | SPF News / police advisories, https://www.police.gov.sg/media-hub/news | Singapore Police Force | Scam advisories, enforcement releases, brands impersonated. Few literal URLs in the text | Sitemap: 4,203 news URLs, **956 scam-related, 354 "advisory"** (2021: 45, 2022: 61, 2023: 57, 2024: 53, 2025: 70, 2026: 67) | **Sitemap**: `https://www.police.gov.sg/sitemap/sitemap.xml` (from robots.txt, no lastmod). No RSS. Pages have JSON-LD `datePublished` | Daily. Latest 2026-11-23 | URL slug contains `YYYYMMDD_title`. JSON-LD datePublished. Body text plus infographic images | Gov.sg ToU. robots.txt disallows `/api/`, `/RestApi/`, `/sitefinity`, search |
| 3 | icanactagainstscams.gov.sg /scam-trends (baseline) | SPF / MHA | Advisories with `scam_site_urls`, brand and category tags | 209 | (already reverse-engineered) | Aug 2025 to Nov 2026 | see `../FINDINGS.md` | n/a |
| 4 | CSA Alerts & Advisories, https://www.csa.gov.sg/alerts-and-advisories/ | Cyber Security Agency / SingCERT | Vulnerability alerts, advisories (a few on scams/phishing) | Alerts RSS: 200 items. Advisories RSS: 117 items, **19 mention scam/phish** | **RSS (documented via `<link rel=alternate>`)**: `https://www.csa.gov.sg/alerts-and-advisories/alerts/rss.xml`, `https://www.csa.gov.sg/alerts-and-advisories/advisories/rss.xml` | Alerts latest 20 Nov 2026 (AL-2026-167). Advisories latest 13 Nov 2026 (AD-2026-017) | `title, link, guid, pubDate, category, description` | Gov.sg ToU. robots allows all except /search. Sitemap `https://www.csa.gov.sg/sitemap.xml` |
| 5 | ScamShield "Scam Alert", https://www.scamshield.gov.sg/resources/scam-alert/ | SPF + NCPC + OGP (ScamShield suite; **scamalert.sg 301 → scamshield.gov.sg**) | Short brand-level alerts (e.g. OCBC, SingHealth, OneMotoring phishing) | 10 live alerts (28 Aug to 20 Nov 2026). Older ones appear to rotate out | No feed. **Sitemap** `https://www.scamshield.gov.sg/sitemap.xml` (88 URLs, with lastmod). Isomer static site. URL pattern `/resources/scam-alert/alert-DDmonYY/` | ~weekly. Latest 20 Nov 2026 | Title, date, body. **No URLs/phones** (guidance only, e.g. "SMSes from OCBC should reflect OCBC as the Sender ID") | Gov.sg ToU. robots: allow all except /search |
| 6 | ScamShield bulletins, briefs, ESSR | SPF / ScamShield | Monthly Scams Bulletins (PDF), Scams & Cybercrime Briefs, E-Commerce Scams Situation Report (top-10 platforms by losses/cases) | 2026 bulletins: 3 issues (Jan to Mar). ESSR 1H 2026 (24 Aug 2026) | PDF under `scamshield.gov.sg/files/...` (e.g. `/files/2026_scams_bulletin/msb_mar_2026.pdf`) | Monthly/semi-annual, irregular | Scam type, platform, losses. No IOCs | Gov.sg ToU |
| 7 | SPF Scam & Cybercrime Briefs (statistics), https://www.police.gov.sg/media-hub/statistics | SPF | Aggregate stats: cases, losses, scam types, platforms, disruption counts | Semi-annual. Mid-Year 2026 = 37-page PDF | PDF (e.g. `/-/media/SPF/Advisories/Scams/Annual-Scam-and-Cybercrime-Brief-2025.pdf`) | Mid-Year 2026 PDF created 26 Aug 2026 | Aggregates only | Gov.sg ToU |
| 8 | Gov.sg Trusted Sites (**allowlist**), https://www.gov.sg/trusted-sites/ | Gov.sg / MDDI | Legit gov-associated sites, healthcare, town councils, events, short-link domains | ~119 table rows, ~112 non-.gov.sg external domains | HTML tables. Third-party: `https://raw.githubusercontent.com/elliotwutingfeng/GovSGTrustedSites/main/allowlist.txt` (115 lines, BSD-3, pushed 2026-11-20) | Page updated 6 Nov 2026 | Org name, URL, category | Gov.sg ToU |
| 9 | SSIR List of Organisations with ≥1 whitelisted Sender ID (**allowlist**), https://smsregistry.sg/web/org/public-listing (linked from sgnic.sg/smsregistry/list-of-organisations) | SGNIC (IMDA subsidiary) | Organisation names only. **No sender IDs**. "Sender ID Query" page has no public lookup | 68 pages × 50 ≈ **3,400 orgs** | Paginated HTML (`data-target-url="/web/org/public-listing"`, 50/page). No download | "Last Updated: 24 Nov 2026 23:59" (daily) | Org name only | SGNIC disclaimer ("for general information… not liable") |
| 10 | MAS Financial Institutions Directory (**allowlist**), https://eservices.mas.gov.sg/fid | MAS | Licensed FIs by licence type, with website, address, phone, UEN | Thousands (e.g. 1,583 CMS licensees, 20 full banks) | HTML only. **MAS says there is no public API.** Third-party scraper `elliotwutingfeng/MASRegulatedFinancialInstitutions` (Go, BSD-3, run it yourself; no committed output) | Live | Name, licence, website, address | MAS ToU |
| 11 | ScamShield bank anti-scam hotlines (**phone allowlist**), https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ | ScamShield | 8 banks' official hotline numbers | 8 | HTML | Updated 20 May 2026 | Bank, number | Gov.sg ToU |
| 12 | MinLaw Registry of Moneylenders: list of licensed moneylenders (**allowlist** vs loan scams), https://rom.mlaw.gov.sg/information-for-borrowers/list-of-licensed-moneylenders-in-singapore/ | Ministry of Law | Licensed moneylenders, approved business addresses and websites | ~100+ | PDF via `go.gov.sg/mlaw-rom-list-licensed-moneylenders` (half-yearly "as at" snapshots, e.g. 1 Jul 2025) | Half-yearly | Name, licence, address, website | Gov.sg ToU |
| 13 | data.gov.sg | GovTech + agencies | **No scam IOC datasets.** Only aggregates: "Cases Recorded for Selected Major Offences" (`d_9dd5f0c8049d549380e7f8d8d42a3a6a`, includes "Cheating Related Offences", **stale: ends 2020**), UML & harassment, ACRA UEN registry (collection 1, updated 2026-11-16) | 1,370 collections scanned | Documented API: `https://api-production.data.gov.sg/v2/public/api/collections?page=N`, `.../datasets/{id}/metadata`, `https://data.gov.sg/api/action/datastore_search?resource_id=…` (returns 403 to Python-urllib UA; curl UA OK) | n/a | n/a | Singapore Open Data Licence |
| 14 | Agency scam pages: CPF, IRAS, ICA, SingPost, OCBC/DBS, ABS | Various | Ad-hoc warnings. Occasional single IOC (CPF: sender `welcome@timespaceccg.com`, 21 Jun 2025) | Handful each | HTML only, no feeds | Irregular (OCBC latest 12 Jun 2025) | Free text | Site ToU |
| 15 | Not published (for completeness) | — | OCHA directions/blocked content (only counts in parliament replies: >150,000 items disrupted, >90% scams). SATIS takedowns. National Scams List. IMDA/GRA gambling block lists (>3,800 sites blocked by end 2024; SPF took over from 1 Jan 2025). ScamShield app/bot report DB. GoGovSG Directory (login, gov officers only). IMDA SSIR sender-ID list | — | **No** | — | — | — |

## Per-source notes

### 1. MAS Investor Alert List (best official IOC source)
- Page: https://www.mas.gov.sg/ial (canonical https://www.mas.gov.sg/investor-alert-list), "Last updated on 17 Sep 2026" (page chrome). It renders through the JS widget `/html/search/js/bundle.search-ial.1.0.0.js`.
- The data behind the page is a Solr-style JSON response (`responseHeader`/`response.docs`). OpenSanctions archives it verbatim as `source.json`. The open-source scraper `elliotwutingfeng/MASInvestorAlertList` (scraper.go L34) calls `https://eservices.mas.gov.sg/statistics/api/v1/ialsearch?…`, and the MAS statistics area does advertise "APIs for developers". However, **MAS does not document ialsearch, and I did not call it.** **Recommended access is the OpenSanctions bulk files**: `index.json` lists versioned artifacts, e.g. `https://data.opensanctions.org/artifacts/sg_mas_investor_alert/20261124203206-lin/source.json`. OpenSanctions shows 902 targets and 1,947 FtM entities, updated 2026-11-24, last change 2026-11-17.
- **Caveat (policy change):** a notice on the page says "MAS will no longer publish on the Investor Alert List the names and online identifiers (such as websites and messaging channels) of entities who impersonate MAS-regulated financial institutions." So new impersonation entries stop, and 34 legacy impersonation notes remain.
- Website values are messy free text: newline or `;` separated, sometimes with paths or no scheme (`www.5g2s.top`, `https://panel.nodecheap.biz/dashboard/terms`). Phones are also messy (`41604300110 ; \n6531590515`).
- Samples (verbatim from source.json):
  - id 6018: `Domain Group Pte. Ltd.` | website `www.5g2s.top` | date `16 Nov 2026`
  - id 6017: `Handsworth Advisory Pte Ltd, Vaulterro.com` | `https://handsworthadvisory.com/\nhttps://vaulterro.com/` | `+65 3106 7983` | `contact@handsworthadvisory.com …` | `600 North Bridge Road, Parkview Square, Singapore 188778` | `02 Nov 2026`
  - id 6005: `www.expeditioninvm.net , www.expeditioninv.com` | notes: "This entity impersonates a financial institution that is regulated by MAS, Expedition Investment Management Pte. Ltd.. …" | `05 Aug 2026`
- Listing date histogram: 2015 to 2021 has ~40 to 100 per year, 2022 to 2024 has ~35 to 50 per year, 2025 has 66, 2026 has 30. Entries are never marked removed or expired. Since `date` is the listing date, apply your own age decay.
- SG-specific: yes, though many entities and domains are offshore.

### 2. SPF News (police.gov.sg)
- robots.txt points to `https://www.police.gov.sg/sitemap/sitemap.xml` (5,170 URLs, priority only, no lastmod). `/sitemap.xml` returns 404.
- 354 advisory URLs and 956 scam/phish/impersonation/malware/fraud URLs between 2021 and 2026. icanact's 209 records only go back to Aug 2025, so this is the **historical backfill** for brand, category and timeline labels.
- Pages carry JSON-LD `datePublished` (e.g. `2026-11-03T14:35:00Z`). The `<h1>` is a generic "Article Banner", so take the title from the URL slug or `og:title`.
- IOC density is low. In 2 sampled 2026 phishing advisories, the text had no scam domains (only `support.apple.com` guidance links). Example screenshots are images (8 to 14 per page). Texts give counts like "Police have proactively detected and blocked at least 10 such malicious websites" without naming them.
- Recent samples: `20261103_police_advisory_on_resurgence_of_phishing_scams_impersonating_courier_companies`, `20261029_police_advisory_on_scams_involving_the_impersonation_of_simba_staff`, `20261120_two_malaysian_men_to_be_charged_for_their_involvement_in_government_officials_impersonation_scam`.
- Related: `/advisories/scams` (awareness hub, updated 2 Nov 2026, no lists). `/knowledge-hub/legislation/online-harms-act-overview/*` (OCHA process, no published directions).

### 4. CSA RSS
- Two documented RSS 2.0 feeds. Item fields: `title, link, guid, pubDate, category, description`.
- Samples: "Critical Vulnerabilities in PHP | Fri, 20 Nov 2026 | /alerts/al-2026-167". "Advisory on Recent Uptick in Reported Cyber Incidents | 13 Nov 2026 | /advisories/ad-2026-017".
- Scam-relevant advisories include "SPF-CSA Joint Advisory On Cryptocurrency Scams Involving Fake Job Offers And Compromised Software Systems", "Joint Advisory on Technical Support Scams Involving the Impersonation of Microsoft", "Joint Advisory on Scams Involving Digital Manipulation", and the alert "Scammers Impersonating CSA, the SPF, and the MHA".
- Best used as a clean dated event stream and for a few brand-impersonation labels, not for domains.

### 5–6. ScamShield (scamshield.gov.sg)
- ScamAlert.sg (NCPC) is gone. `www.scamalert.sg` returns 301 to `www.scamshield.gov.sg`, and scamshield.org.sg returns 302 to the same. The ScamShield Suite (Sept 2024) absorbed the NCPC ScamAlert channels.
- The Scam Alert section lists 10 items, e.g. 20 Nov 2026 "Received a message saying your OCBC card has been suspended? Be careful." The body is guidance with no IOCs.
- The site is built with Isomer (OGP). The sitemap has lastmod, so new alerts can be detected by diffing the sitemap.
- The ScamShield app, the WhatsApp bot (go.gov.sg/scamshield-bot) and "check-for-scams" give per-query verdicts only. There is no public list or API. The WhatsApp channel is https://whatsapp.com/channel/0029Va4imcoCRs1thRkcGg1b (no Telegram link on the page).
- ESSR gives platform-level risk (1H 2026: Facebook had the highest losses at S$2.7m, Carousell the most cases). It is useful as a platform prior, not as IOCs.

### 7. SPF Scam & Cybercrime Briefs
- Mid-Year 2026 brief (PDF, 37 pp, 26 Aug 2026), for context: "SPF disrupted 47,500 scam-related mobile lines, 37,500 WhatsApp lines, 31,600 online monikers and 52,200 malicious websites" in 1H 2026. It also mentions the National Scams List (NSL, shared between police and service providers), SATIS, and Implementation Directives to Apple, Google and Meta. This shows the official IOC volume is about 100 times what is published anywhere.

### 8–12. Allowlists (for brand/look-alike detection and false-positive suppression)
- **gov.sg Trusted Sites**: categories are Government Associated (~25), Other Trusted Orgs (~60+: healthcare, town councils), Official short links (go.gov.sg, for.sg, for.edu.sg), and Events (~7). Samples: "HealthHub | https://www.healthhub.sg", "Aljunied-Hougang Town Council | https://www.ahtc.sg", "SIWW | https://www.siww.com.sg".
- **SSIR orgs**: samples "ZINGKEY PTE. LTD.", "TENCENT INTERNATIONAL SERVICE PTE. LTD.", "COMMUNICABLE DISEASES AGENCY". Names only, no sender IDs, so it is of limited use for SMS sender validation. Government agencies all use the single `gov.sg` sender ID (since 1 Jul 2024).
- **MAS FID**: authoritative list of FI websites. Use it to recognise legitimate bank and broker domains and to resolve the brand named in IAL "impersonates…" notes.
- **ACRA UEN** (data.gov.sg collection 1): entity-name resolution for "Pte Ltd" names seen in scams.
- Not checked in depth: the MOM Employment Agency directory (allowlist against job scams) and SGDI (sgdi.gov.sg, agency directory).

### 13. data.gov.sg
- Scanned all 1,370 collections with the documented v2 API. Matches for scam/fraud/phish/cyber/police/crime were only aggregate SPF crime tables (2024 refresh, data to ~2020), MinLaw moneylending counts, and SPF geo layers. No scam lists, IOCs or ScamShield data.

### 14. Agency pages
- CPF "CPF Clarifies" lists 15 entries. One scam alert (21 Jun 2025) names the sender `welcome@timespaceccg.com`. CPF also posts on Telegram (`t.me/s/CPFBoard`).
- The IRAS scam-advisory hub, the ICA "Advisory on Fake or Misleading Websites" (updated 27 Oct 2026; **lists no domains**, only says legit URLs contain `.ica.gov.sg`), OCBC security advisories (20+, latest 12 Jun 2025, no URLs), and ABS releases (PDF statements) all give guidance only.
- SingPost scam info is mostly delivered through SPF advisories (e.g. 20260327, WhatsApp impersonation of SingPost).

### 15. What is NOT public
- OCHA: police.gov.sg OCHA pages describe the process (directions, appeals, codes of practice) but publish no directions. Only aggregate counts appear in parliamentary replies.
- IMDA/SPF gambling and other DNS block lists: not published. Third-party `Singapore-Internet-Watch/singapore-blocklist` (blocklist.csv) was last pushed 2021-09-30, has no licence and is unofficial, so it is not useful.

## Suggested ingestion plan
1. **IAL**: pull OpenSanctions `source.json` daily (or `targets.simple.csv`). Parse `website_s` into domains (split on newline, `;`, `,` and whitespace, then get eTLD+1). Keep `date_dt` as first_seen and `notes_s` for the impersonated brand. Respect CC-BY-NC.
2. **SPF backfill**: diff the police.gov.sg sitemap against icanact. Fetch only new advisory URLs and take the date from JSON-LD. Use them for brand and category labels. OCR the images if you want IOCs.
3. **CSA**: poll both RSS feeds.
4. **ScamShield**: diff the sitemap for new `/resources/scam-alert/alert-*` URLs.
5. **Allowlists**: gov.sg trusted-sites (or the GovSGTrustedSites allowlist.txt), MAS FID websites, plus `*.gov.sg` and bank hotlines. Use them to suppress false positives and to seed brand look-alike matching.
