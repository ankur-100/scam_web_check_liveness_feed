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
| 8 | [spamcalls.net +65](https://spamcalls.net/en/country-code/65) | Hello World Digital (DE) / crowdsourced | +65 numbers with high request activity; 90-day report chart | Very low (peak 5 reports/day on 2026-11-08) | HTML | 2026-11 | Has ToS (not reviewed); robots blocks `/search`, `/activity` | Medium | **Very low** |
| 9 | **Corporate official-domain allowlists**: [Singtel scam advisory](https://www.singtel.com/personal/support/scam-advisory), [SingPost online security](https://www.singpost.com/online-security-you), Carousell, Shopee help centre | Brand owners | Domains and channels that **are** legitimate, plus a few look-alike *patterns* | Singtel ≈45 official/partner domains (e.g. `singtel.com`, `singtelcrm.com`, `gomo.sg`, `heya.sg`, `dash.com.sg`, `portal.singtelge.com`). SingPost and Carousell give patterns only | HTML (the Singtel list is in a JSON component blob) | Singtel live; SingPost page dated 2022-02-28 | Corporate site terms | High | **Medium as a negative set** for allowlisting and false-positive suppression on brand-impersonation matches |
| 10 | Bank alert pages: [DBS Recent Scams & Fraud](https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page), [OCBC Security advisories](https://www.ocbc.com/personal-banking/security/security-advisories.page), [UOB News & announcements](https://www.uob.com.sg/personal/digital-banking/news-and-announcements.page) | Banks | Narrative scam alerts (MO, red flags) | DBS 13 dated alerts; OCBC ~dozens of dated editions; UOB undated | HTML | DBS 2026-08-28 ("SMS Phishing Alert"); OCBC latest dated advisory 2025-06-12 | Bank site terms | High | **Very low.** **Zero scam domains or numbers** in any of the three. They only name the bank's own domains/hotlines (allowlist value) |
| 11 | [scam.sg](https://www.scam.sg/) (+ [/watchlist](https://www.scam.sg/watchlist)) | OnScam (SG) Pte Ltd / commercial "business trust" platform | TrustScore profiles of 621k ACRA entities; Watchlist = 811 items (17 MAS alerts + 794 news headlines, many not scam-related) | See left | HTML (Next.js); no public API | Watchlist 2026-11-05 | **T&C: must not republish, reproduce, copy or redistribute.** robots `Content-Signal: ai-train=no` | High | **Very low.** Not an IOC list. "Low score" is explicitly *not* a scam verdict |
| 12 | [RecordOwl /scam-sg](https://recordowl.com/scam-sg) | RecordOwl / SG business directory | 848 "scam reports": **845 are a mirror of the MAS Investor Alert List** (latest 2025-02-12, stale), plus 3 editorial | 848 | HTML, paginated (5 pages × 15) | Editorial 2026-11-20; MAS mirror stops at 2025-02-12 | Site terms (not reviewed). Editorial entries **name private individuals with phone numbers** | High | **Very low.** Get the MAS IAL from MAS directly |
| 13 | [NUS SMS Corpus](https://github.com/kite1988/nus-sms-corpus) | NUS WING (Chen & Kan 2013) / academic | **Legitimate** SG SMS (ham), not scams | 55,835 EN + 31,465 ZH | SQL/XML/JSON zips; also on Kaggle | 2015-03-09 release | Free for research, cite the paper | 100% SG | **Low.** Useful only as an SG-English/Singlish ham baseline for text classifiers |
| 14 | Commercial gated feeds: [Whoscall Anti-Scam Intelligence](https://web.whoscall.com/partners/asi) (Gogolook), [ScamAdviser API/feed](https://www.scamadviser.com/scamadviser-api), Trend Micro ScamCheck "Scam Radar", [GASA State of Scams in SG](https://gasa.org/knowledge-base/reports/state-of-scams-in-singapore-report-2024), Global Signal Exchange | Vendors / alliances | Numbers + domains (Whoscall claims 2.6B entries and 7M scam sites; powers StarHub ScamSafe); trust-score API; survey statistics | n/a | API/data feed **by partnership only** (Whoscall). ScamAdviser via RapidAPI (free 20 req/mo; $39/mo for 10k) or direct contract. GASA reports **members-only**. GSE **members-only** (GovTech/SPF are members) | n/a | Proprietary | Mixed | **Potentially high, but not public.** Procurement decision, not scraping |
| 15 | Community forums/groups: HardwareZone EDMW scam threads, r/singapore, Telegram/Facebook "SG scam alert" groups | Community | Ad-hoc screenshots of SMS/links/numbers in posts | Unknown | HTML threads (HWZ guest-readable); Reddit not reachable from this tool | HWZ "New Scam Variants" thread started 2025-01-04 | HWZ and Reddit ToS restrict automated collection (Reddit Data API terms apply). No credible standing Telegram/FB list found. SPF itself warns about *fake* "official" Telegram channels | High | **Very low** for structured data |
| 16 | Media (Straits Times, CNA, Mothership) | Publishers | Domains appear only when **echoing government advisories** (e.g. [Mothership 2026-04](https://mothership.sg/2026/04/mha-imda-6-fake-news-websites-blocked/) lists 6 MHA/IMDA-blocked *hostile-information* sites, not scam sites) | n/a | HTML; ST paywalled | Live | Publisher copyright | High | **Nil incremental.** Redundant with SPF/MHA sources |

**Searched for, but no SG-specific dataset exists or could be found:**
- HuggingFace (API search for `singapore`/`scam`/`smishing`/`scamshield`): the "ScamShield"-named datasets are Indian/generic and unrelated to SG ScamShield.
- Kaggle: no SG scam dataset beyond the NUS SMS corpus.
- GitHub:
  - `dehan97/spam_classifier` claims "Singaporean spam SMS", but its README/data could not be retrieved.
  - `LIZIHAO-NTU/PE6201_…` "ScamLens SG" is an NTU course project with **90 synthetic** messages only.
  - `arjunjono/NeuraShield-SG` is a detector, not data.
- The Google DeepMind × GovTech Gemma scam-detector (announced 2026-10-14) reportedly comes with a "public dataset of anonymised scam conversation patterns". It is **not on HF under google/govtech** as of today. Re-check later; it would also count as quasi-government.

**Could not assess (blocked, not bypassed):**
- ScamAdviser and Scam-Detector.com: Cloudflare interactive challenge, even for robots.txt.
- Carousell help centre: 403 to non-browser clients.
- Lookout blog on SingPost/Singtel phishing: 403.
- M1 scam page: Radware bot manager.
- Crime Science (BMC) page: JS challenge. I read the White Rose eprint PDF instead.

---

## Per-source notes and sample records

### 1. scamalert.sg scrape (Lwin Tun & Birks, Leeds), the best open SG scam-text corpus
- Raw URL: `https://raw.githubusercontent.com/zeyalt/Crime-Script-Analysis-NLP/master/Data/scam_raw_dataset.csv`. The same folder also has `scam_data_1..4.csv` (cleaned stages).
- Columns: `submission_details` ("<submitter> | DD Mon YYYY"), `scam_type`, `incident_description` (free text), `scammer_details` ("Name: … Contact: …").
- Paper: *Supporting crime script analyses of scams with NLP*, Crime Science 12:1 (Feb 2023). It states that 4,660 reports were extracted covering 20 Jul 2016 – 19 Jul 2020. The "Availability of data" section links only this repo. Acknowledges NCPC.
- Scam-type distribution: Impersonation 1,477; Online Purchase 786; Internet Love 708; Investment 272; Phishing 248; Home/Room Rental 222; Credit-for-Sex 202; Money Mule 125; Job 118; Loan 101; Cyber Extortion 88; Lottery 84; …
- **Parsing gotcha:** the committed CSV contains unresolved `<<<<<<< HEAD / ======= / >>>>>>>` blocks. Keep the HEAD side and the file parses to exactly 4,660 rows.
- **PII:** submitter names, victim-supplied bank account numbers and phone numbers are present. Redact them before any redistribution.
- Samples (submitter names redacted by me):
  - `[redacted] | 02 Aug 2017 | Phishing Scam | Name: Singapore Police Contact: (blank) | "i received a call from 87243492 and it was an automated phone message saying there was something wrong with my NRIC validity…"`
  - `[redacted] | 25 May 2017 | Online Purchase Scam | Name: Thevalueshopping | "Beware of Carousell seller "Thevalueshopping" selling Lego at lowest price! I paid through ibanking $600 deposit into seller OCBC account [redacted]…"`
  - `Anonymous | 17 Jul 2020 | Impersonation Scam | Contact: 923329855137 | "They call me by whatsapp … Whatsapp profile was DBS logo … they say my card was blocked"`
- Usefulness: gives historical SG phone IOCs, seller handles and typed MO text. Domains are rare and old. The underlying scamalert.sg stories are an NCPC (government-linked) property, so the other agent's ScamAlert coverage is the live successor.

### 2. IMC'25 "Fishing for Smishing" dataset (CC BY 4.0)
- `dataset/final_dataset_output.csv`. Columns: `time, sender_id, telephone_number_type, original_network_name, original_network_country, text, translation, language, url_shortener, named_entity, scam_type, lure_principles`.
- Built from public user-report platforms. URLs and numbers are placeholder-redacted (`<URL>`, `<US_BANK_NUMBER>`, `<DATE_TIME>`).
- SG subset ≈ 193 rows (network = SGP, or named_entity is an SG brand). Of these, banking 130, government 48, delivery 6, telecom 5.
- Samples:
  - `2022-04-13 | SGP | "SingaPost : Your Reffrence Number <US_BANK_NUMBER> Is ready for collection, Or you can add an address … <URL>" | singapost | delivery`
  - `18:28 | "Fr DBS : There a withdrawal SGD 369 from your DBS/POSB Paylah! on <DATE_TIME> at 18:28 If unauthorised, visit <URL> stop process" | dbs/posb | banking`
  - `Today 8:48 AM | "Singtel!:We inform you in writing that the invoice for <DATE_TIME> has been paid twice … request a refund: <URL>" | singtel | telecom`

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
  - zeyalt scamalert.sg scrape: fine for internal research. Do **not** redistribute it. The upstream text is NCPC/submitter content containing PII.
- **Research citation request:** NUS SMS Corpus (cite Chen & Kan 2013; the authors ask you to email them on use).
- **Explicit anti-scraping or anti-reproduction terms:**
  - numbers.online: no scraping, no bulk extraction, no competing database.
  - scam.sg: no republish, reproduce or redistribute; `ai-train=no`.
  - HWZ and Reddit: forum ToS and Reddit Data API terms.
  - Cloudflare-protected sites (ScamAdviser, Scam-Detector): treat the challenge as a "no automated access" signal.
- **Proprietary/gated:** Group-IB, Whoscall, ScamAdviser feed, GASA, GSE. Use requires a contract or membership.
- **PII and defamation risk:** phone-lookup and directory sites list numbers and sometimes names of private persons, with unverified accusations. Do not republish without verification. Prefer government-attributed IOCs for anything shared.

## Recommendation for the dataset
1. Keep the SPF ICAAS feed as the primary SG domain source. Add the other agent's government feeds (ScamShield, MAS IAL, ScamAlert).
2. Add a **brand allowlist table** from the corporate pages (Singtel's ≈45 domains, SingPost/Carousell/Shopee/DBS/OCBC/UOB official domains), plus the published look-alike patterns as typosquat test cases.
3. Use the **IMC'25 SG subset** (CC BY) and, internally only, the **2016–2020 scamalert scrape** as lure-text and MO corpora for classifier or triage work. Neither is an IOC feed.
4. If live non-government SG IOCs are needed, the realistic path is a **partner feed**: Whoscall ASI (already SG-deployed via StarHub), ScamAdviser data feed, or GSE membership. Group-IB has the best SG campaign-level domain sets but sells them.
5. Re-check later for the DeepMind × GovTech anonymised scam-conversation dataset (announced Oct 2026, not yet located).
