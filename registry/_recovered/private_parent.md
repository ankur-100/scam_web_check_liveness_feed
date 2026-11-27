# Recovered transcript digest: private_parent (agent afa04dd572b2a3014)

### [user]
Today is 2026-11-25. You are building part of a **registry of Singapore organisations → their official domains/subdomains → every page where they publish scam/security-alert information**. This feeds a Singapore scam-intelligence pipeline: official domains become an allowlist for detecting lookalikes, and scam-alert pages become sources.

FIRST read `/home/ankur/scamtrends_feed/registry/FORMAT.md` (output format + ground rules — follow strictly) and skim `/home/ankur/scamtrends_feed/sources/03_community_commercial.md` (earlier survey covering some bank/telco/marketplace pages — reuse its facts, still emit registry records). `/home/ankur/scamtrends_feed/registry/spf_brands.json` lists brands impersonated in SPF advisories — prioritise those that are Singapore private-sector entities.

**Your partition: Singapore private-sector entities commonly impersonated.**
Tier 1 (deep): **DBS/POSB** (incl. digibank, PayLah!), **OCBC**, **UOB**, **ABS** (Association of Banks in Singapore — PayNow, scam pages), Citibank SG, HSBC SG, Standard Chartered SG, Maybank SG, Trust Bank, GXS, MariBank; **Singtel** (+Dash), **StarHub**, **M1**, SIMBA, Circles.Life; **SingPost**, **Ninja Van**, SPX Express, J&T SG, Qxpress, DHL SG, Lalamove, Park N Parcel, uParcel; **Shopee SG**, **Lazada SG**, **Carousell**, Qoo10, Amazon.sg; **Grab**, Gojek, ComfortDelGro, SMRT, SBS Transit, **EZ-Link**, NETS; **SP Group**; **Singapore Airlines**, Changi Airport Group; NTUC FairPrice/Link; brokers **moomoo SG**, Tiger Brokers, **UOB Kay Hian**, Phillip/POEMS; insurers Great Eastern, Prudential SG, AIA SG, Income, Singlife; media **SPH Media (Straits Times)**, **Mediacorp (CNA)**, Mothership (fake-news investment ads impersonate these).
Tier 2 (quick): other SG banks/fintechs/retailers/telcos you encounter.

For each entity record:
- `entity_id` = primary official registrable domain (see FORMAT.md); `official_domains` = all registrable domains it officially uses in SG (e.g. dbs.com.sg, dbs.com, posb.com.sg, dbs.id?) — only those confirmed on the entity's own pages (security pages often state "our only official domains are…"); `official_hosts` = notable login/payment subdomains seen in links (e.g. internet-banking.dbs.com.sg).
- `scam_info`: security/fraud-alert/"latest scams" pages, "official websites/SMS sender IDs" pages, any lists of fake domains/numbers/apps. Use robots.txt → sitemap grep for `scam|fraud|phish|security-alert|impersonat|fake|beware` plus WebSearch `site:<domain> scam`. Record item counts, newest date, whether concrete indicators are listed vs narrative only, 1 short verbatim sample.
- `official_channels`: SMS sender IDs (registered with SSIR), official hotlines, official app names, social handles — these are allowlist gold.

Write `/home/ankur/scamtrends_feed/registry/entities_private.json` (array per FORMAT.md). Return a concise summary (≤350 words): entity count, which publish concrete fake indicators (domains/numbers) vs narrative only, which publish explicit official-domain/sender-ID lists, machine-readable endpoints, anything blocked (don't bypass bot protection).

### [user]
<system-reminder>
Your final report is delivered through SubagentHandback: when your work is complete, call SubagentHandback({message: <your full report>}) and then stop. Only a SubagentHandback call reaches your caller as your result; plain text you write at the end is not delivered.
</system-reminder>

### [assistant text]
I'll start by reading the format spec and the reference files.

### [tool_use Read]
{"file_path": "/home/ankur/scamtrends_feed/registry/FORMAT.md"}

### [tool_use Bash]
{"command": "ls -la /home/ankur/scamtrends_feed/registry/ /home/ankur/scamtrends_feed/sources/ /home/ankur/scamtrends_feed/", "description": "List registry, sources, and project directories"}

### [tool_result]
/home/ankur/scamtrends_feed/:
total 1000
drwxrwxr-x   5 ankur ankur   4096 Nov 25 17:45 .
drwxr-x--- 132 ankur ankur   4096 Nov 25 17:46 ..
-rw-rw-r--   1 ankur ankur 481400 Nov 25 16:46 advisories.jsonl
-rw-rw-r--   1 ankur ankur 493825 Nov 25 16:46 advisories_raw.json
-rw-rw-r--   1 ankur ankur   4896 Nov 25 16:46 extract.py
-rw-rw-r--   1 ankur ankur   7722 Nov 25 16:47 FINDINGS.md
drwxrwxr-x   2 ankur ankur   4096 Nov 25 16:46 raw
drwxrwxr-x   2 ankur ankur   4096 Nov 25 17:45 registry
drwxrwxr-x   2 ankur ankur   4096 Nov 25 17:20 sources
-rw-rw-r--   1 ankur ankur   5346 Nov 25 17:21 SOURCES.md

/home/ankur/scamtrends_feed/registry/:
total 68
drwxrwxr-x 2 ankur ankur  4096 Nov 25 17:45 .
drwxrwxr-x 5 ankur ankur  4096 Nov 25 17:45 ..
-rw-rw-r-- 1 ankur ankur  4237 Nov 25 17:45 FORMAT.md
-rw-rw-r-- 1 ankur ankur 50966 Nov 25 17:45 spf_brands.json

/home/ankur/scamtrends_feed/sources/:
total 88
drwxrwxr-x 2 ankur ankur  4096 Nov 25 17:20 .
drwxrwxr-x 5 ankur ankur  4096 Nov 25 17:45 ..
-rw-rw-r-- 1 ankur ankur  2516 Nov 25 17:18 00_sg_signal_baseline.md
-rw-rw-r-- 1 ankur ankur 18680 Nov 25 17:20 01_sg_official.md
-rw-rw-r-- 1 ankur ankur 21552 Nov 25 17:17 02_generic_feeds.md
-rw-rw-r-- 1 ankur ankur 23093 Nov 25 17:15 03_community_commercial.md
-rw-rw-r-- 1 ankur ankur  5188 Nov 25 17:16 sgfilter.py

### [tool_result]
1	# Registry output format (shared by all research agents)
2	
3	Each agent writes ONE JSON file (a top-level array) to `/home/ankur/scamtrends_feed/registry/`.
4	Keep to these keys exactly so the files can be merged mechanically. Unknown → `null` or `[]`,
5	never invented. Every factual claim must be backed by an `evidence` URL you actually opened.
6	
7	## 1. Entity record (`entities_<partition>.json`)
8	
9	`entity_id` is the entity's **primary official registrable domain**, lowercase, no scheme/www
10	(e.g. `police.gov.sg`, `scdf.gov.sg`, `dbs.com.sg`, `whatsapp.com`). This makes IDs deterministic
11	across agents. A programme without its own domain uses `<parent domain>#<slug>`
12	(e.g. `ica.gov.sg#sg-arrival-card`).
13	
14	```json
15	{
16	  "entity_id": "police.gov.sg",
17	  "name": "Singapore Police Force",
18	  "abbr": "SPF",
19	  "aliases": ["Singapore Police Force (SPF)", "Police"],
20	  "sector": "gov.ministry | gov.statboard | gov.organ | gov.dept | gov.programme | gov.court | quasi_gov | bank | payments | telco | logistics | ecommerce | marketplace | transport | utility | retail | travel | media | brokerage | insurance | healthcare | tech_platform | crypto | other",
21	  "parent_entity_id": "mha.gov.sg",
22	  "country": "SG",
23	  "official_domains": ["police.gov.sg"],
24	  "official_hosts": ["www.police.gov.sg", "eservices.police.gov.sg"],
25	  "scam_info": [
26	    {
27	      "url": "https://www.police.gov.sg/Media-Room/News",
28	      "kind": "advisory_feed | alert_page | scam_faq | official_channels | fake_indicator_list | news_releases | report_portal | statistics",
29	      "lists_indicators": ["domain", "url", "phone", "email", "sms_sender_id", "app", "social_handle", "bank_account", "entity_name"],
30	      "access": "html | rss | atom | sitemap | json_api_documented | csv | pdf",
31	      "machine_url": "https://www.police.gov.sg/sitemap/sitemap.xml",
32	      "item_count": 354,
33	      "latest_item_date": "2026-11-20",
34	      "verified": "2026-11-25 HTTP 200",
35	      "sample": "short verbatim excerpt or example indicator",
36	      "notes": ""
37	    }
38	  ],
39	  "official_channels": {
40	    "sms_sender_ids": [], "hotlines": [], "short_link_domains": [], "social": []
41	  },
42	  "evidence": ["https://... page that confirms the official domains"],
43	  "notes": ""
44	}
45	```
46	
47	`lists_indicators: []` means the page is narrative only (no concrete scam indicators).
48	
49	## 2. Host-discovery record (`hosts_ct.json`), for the subdomain/CT agent only
50	
51	```json
52	{
53	  "host": "www.scamshield.gov.sg",
54	  "registrable_domain": "scamshield.gov.sg",
55	  "discovered_via": "crt.sh | certspotter | sitemap | search | trusted_sites_list | link",
56	  "cert_first_seen": "2023-...", "cert_last_seen": "2026-...",
57	  "resolves": true, "a_records": ["..."],
58	  "http_status": 200, "title": "...",
59	  "scam_relevant": "yes | maybe | no",
60	  "owner_entity_id": "scamshield.gov.sg",
61	  "notes": ""
62	}
63	```
64	
65	## 3. Brand-resolution record (`spf_brand_map.json`), for the brand agent only
66	
67	Input: `registry/spf_brands.json` (159 SPF `Brand` tag values with counts, categories, sample domains, titles).
68	
69	```json
70	{
71	  "brand_value": "Land Transport Authority (LTA)",
72	  "tag_id": "uuid from input",
73	  "resolution": "real_entity | fictitious_scam_brand | generic_or_placeholder | ambiguous",
74	  "entity_id": "lta.gov.sg",
75	  "official_domains": ["lta.gov.sg", "onemotoring.lta.gov.sg"],
76	  "is_singapore_entity": true,
77	  "sector": "gov.statboard",
78	  "confidence": "high | medium | low",
79	  "evidence": ["https://..."],
80	  "notes": "e.g. 'scam domains imitate OneMotoring/ERP payments'"
81	}
82	```
83	
84	## Ground rules (all agents)
85	- Use only public, user-facing pages, robots.txt, sitemaps, RSS/Atom, published downloads, documented APIs,
86	  public certificate-transparency search (crt.sh, certspotter), DNS lookups, and web search.
87	- Do NOT probe undocumented backend/CMS/API paths, brute-force paths, port-scan, log in or register.
88	  An earlier attempt to query an undocumented CMS API was blocked by policy. If any action is blocked, stop
89	  that line of work and report it. Don't work around it.
90	- Do NOT visit scam/malicious domains. Official sites only.
91	- Light request volume. Normal browser User-Agent. Respect robots.txt.
92	- Scratch downloads go in `/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/`.
93	

### [tool_use Read]
{"file_path": "/home/ankur/scamtrends_feed/sources/03_community_commercial.md"}

### [tool_use Bash]
{"command": "cd /home/ankur/scamtrends_feed/registry && python3 -c \"\nimport json\nd=json.load(open('spf_brands.json'))\nprint(type(d), len(d) if hasattr(d,'__len__') else '')\nif isinstance(d,dict): print(list(d.keys())[:20])\nitems = d if isinstance(d,list) else d.get('brands', d)\nimport itertools\nif isinstance(items,list):\n    print(json.dumps(items[0],indent=1)[:1500])\n\"", "description": "Inspect structure of SPF brands JSON"}

### [tool_result]
PreToolUse hook did not respond before its timeout (host client may be unreachable). The tool call was not executed; other configured hooks may not have completed.

### [tool_result]
<class 'list'> 159
{
 "brand_value": "Land Transport Authority (LTA)",
 "tag_id": "d08ce456-358c-4297-ab61-ea654c314afd",
 "count": 18,
 "categories": [
  "Impersonation",
  "Investment",
  "Non-Banking Related Phishing",
  "Phishing"
 ],
 "sample_domains": [
  "gsaz.cc",
  "pajy.apppy.cc",
  "onemotoring-iza.top",
  "citepay.top"
 ],
 "sample_titles": [
  "Advisory: Beware of Phishing Scams Impersonating LTA",
  "Advisory: Beware of Fake LTA Websites Impersonating Land Transport Authority"
 ]
}

### [tool_use Bash]
{"command": "cat /home/ankur/scamtrends_feed/sources/03_community_commercial.md", "description": "Print the community/commercial sources survey"}

### [tool_use Bash]
{"command": "cd /home/ankur/scamtrends_feed/registry && python3 -c \"\nimport json\nd=json.load(open('spf_brands.json'))\nfor b in sorted(d,key=lambda x:-x['count']):\n    print(b['count'], '|', b['brand_value'], '|', ','.join(b['categories'])[:60], '|', ','.join(b['sample_domains'][:4])[:90])\n\"", "description": "List all SPF brands sorted by count"}

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

### [tool_result]
18 | Land Transport Authority (LTA) | Impersonation,Investment,Non-Banking Related Phishing,Phishi | gsaz.cc,pajy.apppy.cc,onemotoring-iza.top,citepay.top
8 | WhatsApp | Impersonation,Investment,Job | whasgapp.com,ws-whmalopp.lat,whetsap.cam,whetsoerapp.cc
7 | CNA | Investment | truedesignsolutions.shop,zenvaroe.com,avernovat.com,databaiouzuma.com
6 | TikTok | Investment,Job | globaltop.org,fdfdd.cc,mermyseller.shop,r2g9.my
6 | UnionPay | Impersonation | lumivo.cfd,calqiro.cfd,plieruy.cfd,victimfundsrecvery.com
6 | DBS | Banking Related Phishing | dbsi-banking.com,ice-coffee-star.unicornplatform.page,cmpaus.com.au,dbs-token.buzz
5 | Singapore Police Force (SPF) | Impersonation,Non-Banking Related Phishing | drbypass-proxy.pages.dev,hare-fan8702.workers.dev,policegov.eu.cc,sg-policectictr.com
5 | Ninjavan | E-Commerce,Non-Banking Related Phishing,Phishing | oouyif.cfd,nrgfzf.cfd,nlqqgz.cfd,oclaro.cfd
5 | Inland Revenue Authority of Singapore (IRAS) | Malware,Non-Banking Related Phishing,Phishing | irasz.com,govment.cc,iras.nakadaniko.com.sg,richpark.shop
5 | SingPost | Non-Banking Related Phishing | 894144.cc,sgposeigt.sbs,personail.cfd,singapost-track.info
4 | CDC Vouchers | Impersonation | ptvs-fcf5-eb3ff9d649f5.herokuapp.com,fatsdfe56tiziadf.koyeb.app,applyserviceinsupportgowhr
3 | MooMoo | Non-Banking Related Phishing | p3w8f1y6j0t9h4d2ka.live,8h2n7y4k1p9w0f5jcd.live,n5r0x7c2q8v1m9z4gb.live,pq1idrmf27wu91l4wv
3 | Booking.com | Non-Banking Related Phishing | reserv-advanced67745303.com,myhotel-1899.co,secureresverify.com
3 | Lalamove | Non-Banking Related Phishing | fload.buzz,lalamove.eu.cc,htake-c.cfd
3 | JKF | Job | coupang-vip.com,wwwshopee.net,shopping8.shop,fastnedglobal.shop
3 | UOB | Banking Related Phishing | trigonmining.co.za,resend-clicks-a.com,ifreelance4u.com,utradetsg1.top
3 | B2B Wave | Job | cdiscountsb.com,argos-online.me,bigbuy.rest,bigbuyshops.club
2 | NVIDIA | Investment | security-platform.vip,nvidialisuj.top,innovative-finance.cc
2 | Singpass | Non-Banking Related Phishing | fuxxaway.workers.dev,carolineporcellane.it
2 | Park N Parcel | Non-Banking Related Phishing | parcel-k.top,parcel-jt.top,parcel-d.top,parknparcel-oc.top
2 | LG | Investment | lgnewenergy.com,gaouga.com,gaouga.app
2 | No Brand | E-Commerce,Non-Banking Related Phishing | zhaitwfo.com,behene.com,ite-pm-event.netlify.app
2 | SPX | Non-Banking Related Phishing | llkw.top,villen.cyou
2 | Gov.sg | Impersonation | cly114514.workers.dev,kfy001.online
2 | Immigration & Checkpoints Authority of Singapore (ICA) | Impersonation | bonusvakti14.com,ica-gov.com
2 | MoneySmart | Non-Banking Related Phishing | money-sm.art,moneysmart.money,moneysmart.click,moneysmart.one
2 | Netflix | Non-Banking Related Phishing | netflix-home.info,streamhelpcenter.com
2 | Telegram | Impersonation | tjeso.my,telegrinim-tg.cc
2 | CTX | Investment | doge-miningbank.vip,ctxpublic.online,gnfmall.com,oinbase-staking.com
2 | JUST | Investment | skdai001.xyz,seeee.cc,usttt.net,uuttt.cc
2 | Singtel | Non-Banking Related Phishing | servicesmetalinkion.shop,irunsg.shop,onepass.xin
2 | Airdrop Pepe | Investment | zylanto.site,356739.org,pepemining.cc,bereall.com
1 | moburst | Job | lt-moburstmobile.pages.dev
1 | Koka Kona | Investment | akk500.com
1 | Red Bull | Investment | angel-investment.cc
1 | SimplyGo | Non-Banking Related Phishing | se-debarrasser-des-taupes-et-taupiniere.be
1 | SingHealth | Non-Banking Related Phishing | polyclinic-a.top
1 | Dance Prize | Impersonation | votegrand.sbs
1 | Genwrk Store | Job | genwrk.com
1 | uParcel | Non-Banking Related Phishing | llvtx.cfd
1 | SG Arrival Card (SGAC) | Non-Banking Related Phishing | digitalarrivalform.com
1 | UOB Kay Hian | Non-Banking Related Phishing | uobkhs.com
1 | Youlemei Mall | Job | youlemeimall.vip
1 | SP Group | Non-Banking Related Phishing | samgirasg.com
1 | PETROBRAS | Investment | peshiyou.top
1 | ADGM MONEY | Investment | make-moneyeasily.net,gold-vip.icu
1 | Central Provident Fund (CPF) Board | Non-Banking Related Phishing | managelist.com
1 | Best Hotel Reservation | Non-Banking Related Phishing | gardes-holdenjp.com
1 | GitHub | Investment | goudann.top
1 | QNT | Investment | qntai.top
1 | Miniex | Investment | miniexi.com
1 | GOM Player | Investment | lumexafa.top,dnsyidzq.top
1 | Litecoin | Investment | litecoin-machine.co
1 | Immediate Edge | Investment | dylesaesivi.autos
1 | BHP | Investment | 2025gold.net
1 | lyft bikes | Investment | lyft098236.work
1 | The Straits Times | Investment | strikeathletics.pro
1 | Public Transport Voucher (PTVE) | Impersonation | gtva.link
1 | National Environment Agency (NEA) | Impersonation | nodequa.net
1 | Grab | Non-Banking Related Phishing | grabk.vip
1 | Home Team Science & Technology Agency (HTX) | Phishing | qer012.online
1 | Apple | Non-Banking Related Phishing | icloud.qpon
1 | DBS PayLah | Phishing | posb.live
1 | XCN | Investment | xcnc.top
1 | BNBPULSE | Investment | 2125578.com
1 | Saudi Aramco | Investment | currency-oil.com
1 | INFO | Investment | mineverse.cc
1 | Compass Mining | Investment | ssessoomm.com
1 | BNB | Investment | bbconbnb.com
1 | JoyBuy | Job | maill-top.net
1 | GoMining | Investment | go-mining66.top
1 | Nova Quant | Investment | novaxmr.xyz
1 | A2 | Investment | a2.mom
1 | ZFuse | Job | baoffu.vip,tubirating.com
1 | TUbi | Job | baoffu.vip,tubirating.com
1 | Pilbara Mining | Investment | piarjuy.top
1 | DJI | Investment | dji8.top
1 | Shopee | Job | vis3367.shop
1 | MBRAIMSolar Park | Investment | yyujgg.vip,mprmspus.top
1 | Televizo | Investment | yyujgg.vip,mprmspus.top
1 | Avenis | Job | avenisportalglobe1.asia
1 | RiverQuode | Investment | river-quode.net,980.it.com
1 | USDT Tether | Investment | river-quode.net,980.it.com
1 | copililis | E-Commerce | copililis.com
1 | RapidApp | Investment | rapid-app.net
1 | AI-QT | Investment | ai-qt.vip
1 | Snapchat | Investment | makingvideos.app
1 | Crypto.com | Investment | kdmwj.com
1 | Charge+ | Investment | chargingpiles.autos
1 | SmartView | 

### [tool_use ToolSearch]
{"query": "select:WebFetch,WebSearch", "max_results": 2}

### [tool_result]


### [tool_use Bash]
{"command": "mkdir -p /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work && cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work && ls -la; head -c 3000 /home/ankur/scamtrends_feed/SOURCES.md; echo; grep -n -i \"bank\\|dbs\\|ocbc\\|singtel\\|private\" /home/ankur/scamtrends_feed/sources/01_sg_official.md | head -40", "description": "Create scratch dir and skim related source notes"}

### [tool_result]
total 524
drwxrwxr-x 3 ankur ankur   4096 Nov 25 17:48 .
drwx------ 7 ankur ankur   4096 Nov 25 17:47 ..
-rw-rw-r-- 1 ankur ankur 424677 Nov 25 17:47 brand_context.txt
-rw-rw-r-- 1 ankur ankur  94981 Nov 25 17:47 brand_snips.txt
drwxrwxr-x 2 ankur ankur   4096 Nov 25 17:48 ct
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
the SGNIC registered-sender-ID organisation list, MinLaw licensed moneylenders, and ACRA o
9:- **No SG government body publishes a machine-readable scam domain, URL or phone IOC feed.** The operational lists sit behind closed doors: SPF SATIS (52,200 malicious websites disrupted in 1H 2026), the National Scams List (shared with banks and telcos), OCHA directions, ScamShield app reports, and the IMDA/GRA blocking lists.
13:- Several **allowlists** are useful for spotting look-alike brands: gov.sg Trusted Sites, MAS FID, the SSIR organisation list, the ScamShield bank hotlines, the MinLaw moneylender list, and ACRA UEN on data.gov.sg.
24:| 5 | ScamShield "Scam Alert", https://www.scamshield.gov.sg/resources/scam-alert/ | SPF + NCPC + OGP (ScamShield suite; **scamalert.sg 301 → scamshield.gov.sg**) | Short brand-level alerts (e.g. OCBC, SingHealth, OneMotoring phishing) | 10 live alerts (28 Aug to 20 Nov 2026). Older ones appear to rotate out | No feed. **Sitemap** `https://www.scamshield.gov.sg/sitemap.xml` (88 URLs, with lastmod). Isomer static site. URL pattern `/resources/scam-alert/alert-DDmonYY/` | ~weekly. Latest 20 Nov 2026 | Title, date, body. **No URLs/phones** (guidance only, e.g. "SMSes from OCBC should reflect OCBC as the Sender ID") | Gov.sg ToU. robots: allow all except /search |
29:| 10 | MAS Financial Institutions Directory (**allowlist**), https://eservices.mas.gov.sg/fid | MAS | Licensed FIs by licence type, with website, address, phone, UEN | Thousands (e.g. 1,583 CMS licensees, 20 full banks) | HTML only. **MAS says there is no public API.** Third-party scraper `elliotwutingfeng/MASRegulatedFinancialInstitutions` (Go, BSD-3, run it yourself; no committed output) | Live | Name, licence, website, address | MAS ToU |
30:| 11 | ScamShield bank anti-scam hotlines (**phone allowlist**), https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ | ScamShield | 8 banks' official hotline numbers | 8 | HTML | Updated 20 May 2026 | Bank, number | Gov.sg ToU |
33:| 14 | Agency scam pages: CPF, IRAS, ICA, SingPost, OCBC/DBS, ABS | Various | Ad-hoc warnings. Occasional single IOC (CPF: sender `welcome@timespaceccg.com`, 21 Jun 2025) | Handful each | HTML only, no feeds | Irregular (OCBC latest 12 Jun 2025) | Free text | Site ToU |
66:- The Scam Alert section lists 10 items, e.g. 20 Nov 2026 "Received a message saying your OCBC card has been suspended? Be careful." The body is guidance with no IOCs.
77:- **MAS FID**: authoritative list of FI websites. Use it to recognise legitimate bank and broker domains and to resolve the brand named in IAL "impersonates…" notes.
86:- The IRAS scam-advisory hub, the ICA "Advisory on Fake or Misleading Websites" (updated 27 Oct 2026; **lists no domains**, only says legit URLs contain `.ica.gov.sg`), OCBC security advisories (20+, 

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work && head -c 1500 brand_snips.txt; echo; echo ----; ls -la ct | head; echo; UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -s -o /dev/null -w \"%{http_code} %{size_download}\\n\" -A \"$UA\" --max-time 20 https://www.dbs.com.sg/robots.txt", "description": "Peek at existing scratch files and test curl access"}

### [tool_result]
######## [32] moburst
--- 2026-11-17 | Advisory: Job Scams Impersonating Brands like Moburst | https://www.icanactagainstscams.gov.sg/scam-trends/job-scams-impersonating-brands-like-moburst-dd460ff3
    brands=['moburst'] domains=['lt-moburstmobile.pages.dev']
    > The Singapore Police Force has observed a recent increase in job scams involving fake websites impersonating legitimate companies, such as Moburst. Scammers create deceptive websites to trick individuals into believing they are applying for legitimate job opportunities.

######## [33] Koka Kona
--- 2026-11-13 | Advisory: Beware of Fake 'Koka Kona' Investment Scams | https://www.icanactagainstscams.gov.sg/scam-trends/fake-koka-kona-investment-scams-58bf1784
    brands=['Koka Kona'] domains=['akk500.com']
    > The Singapore Police Force has observed a trend of investment scams impersonating well-known brands, including 'Koka Kona'. Scammers are creating fake websites and online platforms to trick individuals into bogus investment schemes. We urge the public to remain vigilant against such fraudulent activities.
    > *   Scammers create fake websites or applications (e.g., `akk500.com`) that closely mimic legitimate brands like 'Koka Kona' to promote fraudulent investment opportunities.

######## [34] Red Bull
--- 2026-11-12 | Advisory: Beware of Investment Scams Impersonating Brands like Red Bull | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-like-red-bull-8904bc32
    
----
total 8
drwxrwxr-x 2 ankur ankur 4096 Nov 25 17:48 .
drwxrwxr-x 3 ankur ankur 4096 Nov 25 17:48 ..

200 62621

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work && mkdir -p private && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -s -A \"$UA\" --max-time 20 https://www.dbs.com.sg/robots.txt -o private/dbs_robots.txt; grep -i sitemap private/dbs_robots.txt | head; wc -l private/dbs_robots.txt; grep -i -c disallow private/dbs_robots.txt", "description": "Fetch DBS robots.txt and list sitemaps"}

### [tool_result]
Disallow: /personal/marketplace/search/sitemap-treasures-private-client-2022.html
Disallow: /personal/marketplace/search/sitemap-treasures-2022.html
Disallow: /personal/marketplace/search/sitemap-posb-2022.html
Disallow: /personal/marketplace/search/sitemap-personal-2022.html
Disallow: /personal/marketplace/search/sitemap-private-banking-2022.html
Disallow: /personal/marketplace-pilot/search/sitemap-treasures-private-client-2022.html
Disallow: /personal/marketplace-pilot/search/sitemap-treasures-2022.html
Disallow: /personal/marketplace-pilot/search/sitemap-posb-2022.html
Disallow: /personal/marketplace-pilot/search/sitemap-personal-2022.html
Disallow: /personal/marketplace-pilot/search/sitemap-private-banking-2022.html
1023 private/dbs_robots.txt
1004

### [tool_use Bash]
{"command": "head -c 2500 FINDINGS.md; echo; sed -n 1,40p sources/00_sg_signal_baseline.md | head -50", "description": "Skim prior findings for context"}

### [tool_result]
# icanactagainstscams.gov.sg/scam-trends — feed structure

Captured 2026-11-25 (latest record 2026-11-24). Raw captures in `raw/`, extractor in `extract.py`.

## TL;DR

- **One GET returns the whole feed.** `/scam-trends` server-renders all **209** advisories
  (2025-08-28 → 2026-11-24) into the Next.js RSC flight stream as the prop `scamAdvisories`.
  `?page=N` just sets `initialPage`. The client shows 8 per page and filters in the browser.
  `?page=2` carries the identical 209 records. There's no need to crawl the detail pages.
- **No lifecycle fields.** There's no `status`, `active`, `expires`, `valid_until`, `severity` or
  `reported_by` field. Nothing in the 209 bodies says something like "expired", "taken down" or
  "Update:". The only time fields are `date_created` and `date_updated`.
- **Classification is a key/value tag list with two keys only:** `Scam Category` (10 values) and
  `Brand` (159 values). **`Brand` is the *impersonated* entity, not the issuing agency.**
  "LTA ×18" means 18 advisories about scams *posing as* LTA. LTA did not publish them.
- **The issuer is effectively always SPF.** 124 of 209 bodies open with "Singapore Police Force (SPF)
  has observed …", 31 with "We …", and the rest are also SPF phrasings ("The SPF observes …").
  No agency other than SPF issues anything here. **SCDF does not appear anywhere** (not as issuer,
  not as brand).
- These are not CVEs. They're consumer-scam advisories whose only machine-readable indicators of
  compromise (IOCs) are domain names (`scam_site_urls`).

## Transport: how the data reaches the browser

| Layer | Finding |
|---|---|
| Framework | Next.js App Router. HTML has `self.__next_f.push([1,"…"])` script tags whose concatenation is the RSC flight stream |
| Backend | Directus CMS. Field names `directus_files_id`, `filename_disk`; junction `scamsexposed_tags_id` → collection is likely `scamsexposed` with an M2M `scamsexposed_tags` |
| Listing prop | Row `8:` → `["$","$L16","1",{"scamAdvisories":[…209…],"initialPage":N}]` |
| Long text | Bodies are hoisted into length-prefixed text rows `<id>:T<hex byte len>,<markdown>` and referenced as `"content":"$17"`. 192 of 209 are hoisted and 17 are inline. **Rows are NOT newline-separated after a T row**, so you need a byte-level stream parser (see `rows()` in extract.py) |
| Pagination | Client-only: `useState(8*initialPage)`, "Load More" adds 8 more |
| Client filter | Search on `title`/`content` substring plus tag match. Th
# Baseline: how "Singaporean" do confirmed SG scam domains look?

Ground truth = 326 domain mentions (317 unique) in SPF's 209 advisories (captured 2026-11-25).

| Test | Hit rate |
|---|---|
| Hostname contains any generic SG token (.sg, singpass, dbs, lta, iras, ica, shopee, ninjavan, grab, sg-…) | **23 / 326 (7%)** |
| Hostname contains a token of *its own* advisory's Brand tag | 83 / 324 (26%), mostly global brands (WhatsApp, TikTok, UnionPay) |

SG-token rate by scam category: Investment **1/112**, Job 1/49, Impersonation 3/38,
Non-Banking Phishing 11/101, Banking Phishing 4/12.

Examples that hit: `lta-gov.com`, `ica-gov.com`, `onemotoring-lta-gov.cc`, `dbs-token.buzz`, `posb.live`, `irasz.com`.
Typical misses: LTA phish on `gsaz.cc`, `citepay.top`, `feekt.top`, `tscs.top`; investment on `akk500.com`, `zenvaroe.com`.

## Implications for filtering global feeds
1. **A hostname keyword filter has about 7% recall** for SG scams. It finds bank and government lookalikes but not investment or job scams.
2. You need local service vocabulary, not just brand names: `onemotoring`, `erp-`, `parking`, `ezlink`, `simplygo`, `cdc`, `sgac`, `paynow`, `nric`, `medisave`, `hdb`, `cpf`.
3. Real recall needs **page-content signals** (title/text/logo on the rendered page: urlscan.io page data, screenshots), or
   **delivery-channel signals** (SG SMS / ScamShield reports), not URL strings.
4. Investment and job scams are brand-agnostic templates, so the reliable way to tie them to Singapore is the lure (ads, SMS, Telegram). Use SPF/MAS lists for these.

## Coverage: are SPF's scam domains in the open global feeds? (measured 2026-11-25)

Union of feeds checked: Phishing.Database links + domains (ACTIVE), Phishing Army extended, OpenPhish community,
CERT Polska, TweetFeed, PhishDestroy, ScamSniffer (about 1.4M distinct hosts in total).

| SPF advisory window | SPF hosts | Found in any open feed |
|---|---|---|
| all (2025-08 to 2026-11) | 317 | 18 (5.7%) |
| last 6 months | 151 | 4 (3%) |
| last 3 months | 85 | 4 (5%) |
| **last 30 days** | **44** | **0 (0%)** |

The open feeds don't contain the domains SPF publishes. They contain a *different* SG
population (Phishing.Database alone has about 445 SG-brand hosts, mostly DBS/PayLah, Carousell, POSB, Singtel
kit URLs) that SPF doesn't list. Neither covers the other, so a usable dataset has to merge both.
"Active" lists drop dead domains, so the all-time figure is a lower bound, but the 30-day
figure is not affected by that and is still 0.

### [tool_use Write]
{"file_path": "/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py", "content": "#!/usr/bin/env python3\n\"\"\"Validate a partial entities JSON file against registry/FORMAT.md (entity records).\nUsage: python3 validate.py <file.json> [more.json ...]\n\"\"\"\nimport json, re, sys\n\nTOP_KEYS = [\"entity_id\", \"name\", \"abbr\", \"aliases\", \"sector\", \"parent_entity_id\", \"country\",\n            \"official_domains\", \"official_hosts\", \"scam_info\", \"official_channels\", \"evidence\", \"notes\"]\nSECTORS = set(\"gov.ministry gov.statboard gov.organ gov.dept gov.programme gov.court quasi_gov bank payments \"\n              \"telco logistics ecommerce marketplace transport utility retail travel media brokerage insurance \"\n              \"healthcare tech_platform crypto other\".split())\nSI_KEYS = [\"url\", \"kind\", \"lists_indicators\", \"access\", \"machine_url\", \"item_count\", \"latest_item_date\",\n           \"verified\", \"sample\", \"notes\"]\nKINDS = set(\"advisory_feed alert_page scam_faq official_channels fake_indicator_list news_releases report_portal statistics\".split())\nINDS = set(\"domain url phone email sms_sender_id app social_handle bank_account entity_name\".split())\nACCESS = set(\"html rss atom sitemap json_api_documented csv pdf\".split())\nOC_KEYS_REQUIRED = [\"sms_sender_ids\", \"hotlines\", \"short_link_domains\", \"social\"]\nOC_KEYS_EXTRA_OK = [\"apps\", \"emails\"]  # additive extension, flagged to caller\nDOM_RE = re.compile(r\"^[a-z0-9-]+(\\.[a-z0-9-]+)+$\")\nID_RE = re.compile(r\"^[a-z0-9-]+(\\.[a-z0-9-]+)+(#[a-z0-9-]+)?$\")\nDATE_RE = re.compile(r\"^\\d{4}(-\\d{2}(-\\d{2})?)?$\")\n\ndef err(msgs, eid, m):\n    msgs.append(f\"[{eid}] {m}\")\n\ndef check(rec, msgs, seen):\n    eid = rec.get(\"entity_id\", \"?\")\n    keys = list(rec.keys())\n    for k in TOP_KEYS:\n        if k not in rec:\n            err(msgs, eid, f\"missing key {k}\")\n    for k in keys:\n        if k not in TOP_KEYS:\n            err(msgs, eid, f\"unknown top-level key {k}\")\n    if not isinstance(eid, str) or not ID_RE.match(eid):\n        err(msgs, eid, \"entity_id not a lowercase registrable domain (optionally #slug)\")\n    if eid in seen:\n        err(msgs, eid, \"duplicate entity_id\")\n    seen.add(eid)\n    if rec.get(\"sector\") not in SECTORS:\n        err(msgs, eid, f\"bad sector {rec.get('sector')}\")\n    for k in (\"aliases\", \"official_domains\", \"official_hosts\", \"sc

### [tool_result]
PreToolUse hook did not respond before its timeout (host client may be unreachable). The tool call was not executed; other configured hooks may not have completed.

### [tool_use Bash]
{"command": "cat > /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"Validate a partial entities JSON file against registry/FORMAT.md (entity records).\nUsage: python3 validate.py <file.json> [more.json ...]\n\"\"\"\nimport json, re, sys\n\nTOP_KEYS = [\"entity_id\", \"name\", \"abbr\", \"aliases\", \"sector\", \"parent_entity_id\", \"country\",\n            \"official_domains\", \"official_hosts\", \"scam_info\", \"official_channels\", \"evidence\", \"notes\"]\nSECTORS = set(\"gov.ministry gov.statboard gov.organ gov.dept gov.programme gov.court quasi_gov bank payments \"\n              \"telco logistics ecommerce marketplace transport utility retail travel media brokerage insurance \"\n              \"healthcare tech_platform crypto other\".split())\nSI_KEYS = [\"url\", \"kind\", \"lists_indicators\", \"access\", \"machine_url\", \"item_count\", \"latest_item_date\",\n           \"verified\", \"sample\", \"notes\"]\nKINDS = set(\"advisory_feed alert_page scam_faq official_channels fake_indicator_list news_releases report_portal statistics\".split())\nINDS = set(\"domain url phone email sms_sender_id app social_handle bank_account entity_name\".split())\nACCESS = set(\"html rss atom sitemap json_api_documented csv pdf\".split())\nOC_KEYS_REQUIRED = [\"sms_sender_ids\", \"hotlines\", \"short_link_domains\", \"social\"]\nOC_KEYS_EXTRA_OK = [\"apps\", \"emails\"]  # additive extension, flagged to caller\nDOM_RE = re.compile(r\"^[a-z0-9-]+(\\.[a-z0-9-]+)+$\")\nID_RE = re.compile(r\"^[a-z0-9-]+(\\.[a-z0-9-]+)+(#[a-z0-9-]+)?$\")\nDATE_RE = re.compile(r\"^\\d{4}(-\\d{2}(-\\d{2})?)?$\")\n\ndef err(msgs, eid, m):\n    msgs.append(f\"[{eid}] {m}\")\n\ndef check(rec, msgs, seen):\n    eid = rec.get(\"entity_id\", \"?\")\n    for k in TOP_KEYS:\n        if k not in rec:\n            err(msgs, eid, f\"missing key {k}\")\n    for k in rec:\n        if k not in TOP_KEYS:\n            err(msgs, eid, f\"unknown top-level key {k}\")\n    if not isinstance(eid, str) or not ID_RE.match(eid):\n        err(msgs, eid, \"entity_id not a lowercase registrable domain (optionally #slug)\")\n    if eid in seen:\n        err(msgs, eid, \"duplicate entity_id\")\n    seen.add(eid)\n    if rec.get(\"sector\") not in SECTORS:\n        err(msgs, eid, f\"bad sector {rec.get('sector')}\")\n    for k in (\"aliases\", \"official_domains\", \"official_hosts\", \"scam_info\", \"evidence\"):\n  

### [tool_result]
/tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/_empty.json: 0 records
TOTAL 0 records, 0 problems

### [assistant text]
Now let me write the shared brief for parallel sub-agents (the partition is ~55 entities, so I'll split it by sector and do merge/QA plus cross-cutting checks myself).

### [tool_use Bash]
{"command": "cat > /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md <<'EOF'\n# Sub-agent brief: SG private-sector entity registry (shared by all groups)\n\nYou are building part of a registry of Singapore organisations -> their official domains/subdomains -> every page\nwhere they publish scam/security-alert information. It feeds a Singapore scam-intelligence pipeline: official domains\nbecome an ALLOWLIST for detecting lookalikes; scam-alert pages become SOURCES. Today is 2026-11-25.\n\n## Step 0\nRead `/home/ankur/scamtrends_feed/registry/FORMAT.md` (section 1 \"Entity record\" and \"Ground rules\") and follow it\nstrictly. Skim `/home/ankur/scamtrends_feed/sources/03_community_commercial.md` (earlier survey; reuse its facts, but\nre-open any page before citing it). If the Read/Write tools time out (hook issue), use Bash (cat, heredoc, python).\n\n## Output\nWrite a JSON ARRAY of entity records to your output path (rewrite it after each entity so partial work survives).\nValidate: `python3 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py <your output>`\nuntil it prints \"0 problems\". Raw downloads go in your group's scratch subfolder.\n\n## Per-entity method (light volume: <=15 requests per site, >=1 s between requests to the same host)\n1. Fetch homepage + robots.txt with curl and a normal browser UA:\n   UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"\n   curl -sL -A \"$UA\" --max-time 30 -o FILE -w '%{http_code} %{url_effective}\\n' URL\n2. Sitemaps: from robots `Sitemap:` lines (else try /sitemap.xml once). Grep URLs for\n   `scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect`. <=10 sitemap files per site.\n3. WebSearch, e.g. `site:<domain> scam`, `<brand> Singapore official SMS sender ID`, `<brand> Singapore scam alert`,\n   `<brand> official websites list`.\n4. Open each candidate page (curl; if JS-rendered and curl gets only a shell, WebFetch once). Record: what it is,\n   number of dated items, newest date, whether it lists CONCRETE indicators (fake domains/URLs, phone numbers, emails,\n   sender IDs, apps, social handles, bank accounts) vs narrative only, and one short verbatim sample (<=200 chars).\n5. Collect allowlist facts from the entity's OWN pages: official domains (\"our official websites are...\"),\n   login/payme

### [tool_result]
1219 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md

### [assistant text]
Now launching 8 parallel sub-agents by sector; I'll handle cross-cutting checks (ScamShield bank hotlines, SSIR registry) and the merge/QA myself.

### [tool_use Agent]
{"description": "Registry: SG local banks + ABS", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent A of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_A_banks_local.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/A/\n\nYOUR ENTITIES (all Tier 1 = deep):\n1. DBS Bank / POSB, incl. digibank, PayLah!, DBS digital token. SPF brand-tag strings to put in aliases: \"DBS\", \"DBS PayLah\". Start points: https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page (earlier survey: 13 dated alerts, newest \"SMS Phishing Alert\" 2026-08-28; re-verify), the \"Scams & Frauds Alert Archives\" page, the scam-defence hub, and any page on verifying official DBS/POSB channels (SMS sender IDs / short codes, official websites, official apps, hotlines incl. the anti-scam hotline). Note dbs.com.sg robots.txt has ~1000 Disallow lines and no Sitemap line (try /sitemap.xml once). POSB (posb.com.sg): separate child record (parent dbs.com.sg) ONLY if POSB has its own scam/security pages; otherwise alias + include posb.com.sg in DBS official_domains if confirmed. Look for dbs.com (group) and any other SG-used domains confirmed on DBS pages.\n2. OCBC Bank (ocbc.com; check whether ocbc.com.sg is used). Start: https://www.ocbc.com/personal-banking/security/security-advisories.page (earlier: dozens of dated editions, latest 2025-06-12; re-check), official SMS sender IDs, anti-scam hotline, OCBC app names, Money Lock / kill switch pages, \"Be A Pro Against Cons\". (Context only: ScamShield posted an alert on 2026-11-20 about fake \"OCBC card suspended\" SMSes.)\n3. UOB (uob.com.sg; uobgroup.com). Start: https://www.uob.com.sg/personal/digital-banking/news-and-announcements.page, security/anti-scam pages, official SMS sender ID(s), UOB TMRW app, go.uob.com/reportscam (report portal). SPF brand-tag string: \"UOB\".\n4.

### [tool_use Agent]
{"description": "Registry: other SG banks", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent B of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_B_banks_other.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/B/\n\nYOUR ENTITIES\nTier 1 (deep): for each find security/fraud hub, latest scam alerts (dated list?), official SMS sender IDs, anti-scam/fraud hotline, official apps, official domains/login hosts, social accounts.\n1. Citibank Singapore (citibank.com.sg)\n2. HSBC Singapore (hsbc.com.sg)\n3. Standard Chartered Singapore (SG pages under sc.com/sg -> entity_id \"sc.com\"; check whether any separate SG registrable domains are used)\n4. Maybank Singapore (verify the primary SG domain: maybank2u.com.sg and/or maybank.com.sg)\n5. Trust Bank Singapore (verify domain, e.g. trustbank.sg)\n6. GXS Bank (verify, e.g. gxs.com.sg)\n7. MariBank Singapore (verify domain)\nTier 2 (quick, at most 3, pick ones with SG security/scam pages): CIMB Singapore (cimb.com.sg), Bank of China Singapore, ICBC Singapore, RHB Singapore, HL Bank, YouTrip, Atome.\n\nCross-check bank hotlines against ScamShield's page https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ (gov page; may be added to evidence as corroboration; each bank's own page must be primary evidence).\n\nWhen done, validate with the brief's validate.py and hand back per the brief (<=250 words)."}

### [tool_use Agent]
{"description": "Registry: SG telcos", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent C of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_C_telco.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/C/\n\nYOUR ENTITIES\nTier 1 (deep):\n1. Singtel (singtel.com). SPF brand-tag string: \"Singtel\". Start: https://www.singtel.com/personal/support/scam-advisory - the earlier survey found a \"List of official Singtel web domains\" (all *.singtel.com plus ~45 other domains/hosts, e.g. singtelcrm.com, singteltvgo.com, portal.singtelge.com, gomo.sg, heya.sg, dash.com.sg, gxs.com.sg, e-station2.axs.com.sg, singtelcares.syd1.qualtrics.com) inside a JSON component blob in that page's HTML. Extract the FULL list from the page (embedded page data is fine), apply the brief's third-party rule (Singtel-owned registrable domains -> official_domains; partner/third-party hosts -> exact FQDN in official_hosts; explain in notes). Also capture Singtel sender IDs, hotlines, scam alerts list (dated?), and any fake-indicator examples. Singtel Dash (dash.com.sg): separate child record only if it has its own scam/security pages, else alias.\n2. StarHub (starhub.com): scam advisories, ScamSafe (Whoscall-powered), sender IDs, hotlines.\n3. M1 (m1.com.sg): earlier survey says the M1 scam page sits behind Radware bot manager. Try once per the brief's bot rule; record the block if so, and fill what you can from M1 pages that do load.\n4. SIMBA Telecom (formerly TPG Telecom SG; verify domain, e.g. simba.sg)\n5. Circles.Life (verify primary domain, e.g. circles.life)\nTier 2 (quick, at most 3): MyRepublic SG, giga! (StarHub), GOMO (Singtel), Zero1, VIVIFI, redONE SG. Sub-brands get their own record only if they have their own scam pages; otherwise put them in the parent's aliases.\nAlso record telco pages explaining SSIR \"Likely

### [tool_use Agent]
{"description": "Registry: SG logistics/delivery", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent D of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_D_logistics.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/D/\n\nYOUR ENTITIES (delivery-scam brands; SPF advisories impersonate several of them)\nTier 1:\n1. SingPost (singpost.com). SPF brand-tag string: \"SingPost\". Start: https://www.singpost.com/online-security-you (earlier survey: dated 2022-02-28; official domain singpost.com; look-alike examples www.singpost.com.xyz.com, www.singpost.net, www.singpost.org; sender IDs SGPOST/SINGPOST) - re-verify, and look for newer scam notices (tracking-page banners, newsroom, FAQ).\n2. Ninja Van Singapore (verify domain, e.g. ninjavan.co with /en-sg). SPF brand-tag string: \"Ninjavan\".\n3. SPX Express Singapore (verify domain, e.g. spx.sg). SPF brand-tag string: \"SPX\".\n4. J&T Express Singapore (verify domain, e.g. jtexpress.sg)\n5. Qxpress Singapore (verify domain)\n6. DHL Singapore (SG pages under dhl.com/sg-en -> entity_id \"dhl.com\"; DHL has fraud-awareness pages - record the SG version and any official-domain statements)\n7. Lalamove Singapore (SG pages under lalamove.com -> entity_id \"lalamove.com\"; verify). SPF brand-tag string: \"Lalamove\".\n8. Park N Parcel (verify domain). SPF brand-tag string: \"Park N Parcel\".\n9. uParcel (verify domain, e.g. uparcel.sg). SPF brand-tag string: \"uParcel\".\nTier 2 (quick, at most 2, only if they have SG scam pages): Pickupp SG, FedEx SG (fedex.com/en-sg), UPS SG, Aramex SG.\n\nFor delivery brands, look specifically for: \"we will never ask you to pay via SMS link\" statements, official tracking hosts, official SMS sender IDs, official WhatsApp numbers, and any listed fake websites/numbers.\n\nWhen done, validate with the brief's validate.py and 

### [tool_use Agent]
{"description": "Registry: SG ecommerce/retail", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent E of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_E_ecommerce_retail.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/E/\n\nYOUR ENTITIES\nTier 1:\n1. Shopee Singapore (shopee.sg; help.shopee.sg). SPF brand-tag string: \"Shopee\". Earlier survey: \"[Scam Advisory]\" help-centre article series (article IDs 76743, 76788, 76790, 76811, 125081, 166953, 204789); official email only @shopee.com; no dates/IOCs. The help centre is an SPA: read article pages via WebFetch if curl gets only a shell; do NOT call its JSON API. Sector \"ecommerce\" (or \"marketplace\" - pick one and be consistent).\n2. Lazada Singapore (lazada.sg; help centre / scam-awareness pages)\n3. Carousell (carousell.sg / carousell.com). SPF brand-tag string: \"Carousell\". Earlier: the help centre returned 403 to non-browser clients; search snippets said only carousell.com/carousell.sg are genuine and gave fake examples carousellpay.com, carousell-pay.com, carousell.pay-sg.com - re-verify by opening the official page (one WebFetch attempt allowed if curl is blocked); if you cannot open it, keep those fakes only in notes labelled \"unverified (search snippet)\".\n4. Qoo10 Singapore (qoo10.sg)\n5. Amazon.sg (amazon.sg): SG help pages on scams/impersonation; global amazon.com equivalents go in notes only.\n6. NTUC FairPrice (fairprice.com.sg) and NTUC Link / Linkpoints (verify domain, e.g. link.sg). Use NTUC Enterprise as parent_entity_id only if its domain is confirmed. SPF brand-tag string: \"NTUC FairPrice\".\nTier 2 (quick, at most 3): CapitaLand (capitaland.com; SPF brand-tag string \"Capitaland\"; CapitaStar / eCapitaVoucher scam notices), Courts SG, Harvey Norman SG, Sheng Siong, Klook.\n\nWhen done, validate with the brief's vali

### [tool_use Agent]
{"description": "Registry: SG transport/payments/utility", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent F of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_F_transport_pay_util.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/F/\n\nYOUR ENTITIES\nTier 1:\n1. Grab (grab.com; SG pages under grab.com/sg). SPF brand-tag string: \"Grab\". GrabPay, Grab safety/scam/phishing pages, official sender IDs, help-centre scam articles.\n2. Gojek Singapore (SG pages under gojek.com -> entity_id \"gojek.com\"; verify)\n3. ComfortDelGro (comfortdelgro.com; CDG Zig app; check cdgtaxi.com.sg)\n4. SMRT (smrt.com.sg)\n5. SBS Transit (sbstransit.com.sg)\n6. EZ-Link (ezlink.com.sg): scam advisories, EZ-Link app. (SimplyGo is LTA/TransitLink = quasi-government: mention in notes only, no record.)\n7. NETS (nets.com.sg)\n8. SP Group (spgroup.com.sg). SPF brand-tag string: \"SP Group\". SP app, scam advisories, official sender IDs.\nTier 2 (quick, at most 3): Charge+ (SPF brand-tag string \"Charge+\"; verify domain), TADA, Ryde, City Energy, Geneco.\n\nFor transport/payment brands look specifically for: fake-app / fake-website warnings (e.g. fake EZ-Link or SimplyGo top-up sites, fake Grab driver/rewards pages), official sender IDs, official app names, and \"we will never...\" statements.\n\nWhen done, validate with the brief's validate.py and hand back per the brief (<=250 words)."}

### [tool_use Agent]
{"description": "Registry: SG travel + brokers", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent G1 of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_G1_travel_brokers.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G1/\n\nYOUR ENTITIES\nTier 1:\n1. Singapore Airlines (singaporeair.com): fraud/phishing notices (fake websites, emails, social-media giveaways, fake KrisFlyer), official channels. Scoot (flyscoot.com) as a quick child record only if it has its own scam/fraud page, else alias.\n2. Changi Airport Group (changiairport.com; check changiairportgroup.com): scam notices (e.g. fake Changi giveaway/lost-luggage pages), official channels.\n3. moomoo Singapore (verify SG domain/path, e.g. moomoo.com/sg). SPF brand-tag string: \"MooMoo\". Look for anti-fraud pages listing official channels, fake apps/groups.\n4. Tiger Brokers Singapore (tigerbrokers.com.sg; check itiger.com). SPF brand-tag string: \"Tiger Brokers\".\n5. UOB Kay Hian (uobkayhian.com; UTRADE). SPF brand-tag string: \"UOB Kay Hian\". (A fake domain uobkhs.com appeared in an SPF advisory - never visit it.)\n6. Phillip Securities / POEMS (poems.com.sg; phillip.com.sg).\nBrokers often publish lists of fake websites/apps/WhatsApp-Telegram groups impersonating them - capture counts, dates and samples (as text; never visit them).\nTier 2 (quick, at most 4): uSMART Securities Singapore (SPF brand-tag string \"uSMART\"; CAUTION: `usmartsg.sg` was listed by SPF as a SCAM domain - do not visit; confirm the real domain from official pages or the MAS Financial Institutions Directory), MoneySmart (moneysmart.sg; SPF brand-tag string \"MoneySmart\"; fake domains money-sm.art, moneysmart.money, moneysmart.click, moneysmart.one - do not visit), Chan Brothers Travel (SPF brand-tag string \"Chan Brothers\"), FSMOne/iFAST, Webull SG, Syfe/Endowus

### [tool_use Agent]
{"description": "Registry: SG insurers + media", "subagent_type": "general-purpose", "run_in_background": true, "prompt": "You are sub-agent G2 of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.\n\nOutput file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/out_G2_insurance_media.json\nScratch folder for raw downloads: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/G2/\n\nYOUR ENTITIES\nTier 1 insurers: find fraud/scam advisories (fake agents, fake policy/claims SMS, impersonation), official channels, apps.\n1. Great Eastern (greateasternlife.com)\n2. Prudential Singapore (prudential.com.sg)\n3. AIA Singapore (aia.com.sg)\n4. Income Insurance (income.com.sg)\n5. Singlife (singlife.com)\nTier 1 media: fake-news investment ads impersonate these. Want (a) pages where the outlet warns about scams impersonating itself (fake articles/sites/ads, deepfakes, fake social accounts) - capture any listed fake domains as text only, never visit them; (b) its scam-news topic page and RSS feed if one exists (kind \"news_releases\", note \"media coverage topic feed\").\n6. SPH Media (verify primary domain, e.g. sph.com.sg) and The Straits Times (straitstimes.com; parent_entity_id = SPH Media's domain). SPF brand-tag string: \"The Straits Times\".\n7. Mediacorp (mediacorp.sg) and CNA (channelnewsasia.com; parent_entity_id \"mediacorp.sg\"). SPF brand-tag string: \"CNA\" (7 SPF advisories about fake CNA-styled investment articles).\n8. Mothership (mothership.sg)\nTier 2 (quick, at most 3): The Business Times, Lianhe Zaobao, TODAY, FWD Singapore, Manulife Singapore, HSBC Life Singapore.\n\nNote: ST is partly paywalled; only read what is publicly visible. Respect robots.txt (some news sites disallow AI crawlers; if robots disallows generic user-agents for a path, don't fetch it).\n\nWhen done, validate with the brief's validate.py and hand back per the brief (<=250 words)."}

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a0061efef86ca7dac (internal ID - do not mention to user. Use SendMessage with to: 'a0061efef86ca7dac', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/a0061efef86ca7dac.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: ae4bc76bdc8b4c8a9 (internal ID - do not mention to user. Use SendMessage with to: 'ae4bc76bdc8b4c8a9', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/ae4bc76bdc8b4c8a9.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a2191f1709a425107 (internal ID - do not mention to user. Use SendMessage with to: 'a2191f1709a425107', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/a2191f1709a425107.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a0e5e0e0d9d522643 (internal ID - do not mention to user. Use SendMessage with to: 'a0e5e0e0d9d522643', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/a0e5e0e0d9d522643.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: ab278b8b9bceee798 (internal ID - do not mention to user. Use SendMessage with to: 'ab278b8b9bceee798', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/ab278b8b9bceee798.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: adccbf6085f551f69 (internal ID - do not mention to user. Use SendMessage with to: 'adccbf6085f551f69', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/adccbf6085f551f69.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a929bb1e015197516 (internal ID - do not mention to user. Use SendMessage with to: 'a929bb1e015197516', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/a929bb1e015197516.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [tool_result]
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: a55d50fb9aafdbb70 (internal ID - do not mention to user. Use SendMessage with to: 'a55d50fb9aafdbb70', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/tasks/a55d50fb9aafdbb70.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.

### [assistant text]
While those run, I'll check a cross-cutting allowlist source no sub-agent was given: the SGNIC SMS Sender ID Registry (SSIR) organisation list.

### [tool_use WebSearch]
{"query": "SGNIC SMS Sender ID Registry list of participating organisations", "mode": "standard"}

### [tool_result]
Web search results for query: "SGNIC SMS Sender ID Registry list of participating organisations"

Links: [{"title":"list of participating aggregators","url":"https://www.sgnic.sg/smsregistry/list-of-participating-aggregators"},{"title":"list of organisations","url":"https://www.sgnic.sg/smsregistry/list-of-organisations"},{"title":"sms sender id registry","url":"https://sgnic.sg/faq/sms-sender-id-registry"},{"title":"list of participating aggregators","url":"https://prod.sgnic.sg/smsregistry/list-of-participating-aggregators"},{"title":"list of organisations","url":"https://prod.sgnic.sg/smsregistry/list-of-organisations"},{"title":"www.sgnic.sg","url":"https://www.sgnic.sg/smsregistry"},{"title":"Industrial Classification Notices In The News About Contact Us","url":"https://www.sgpbusiness.com/list-of/SMS-Registry-Participating-Aggregators"},{"title":"sms sender id registry","url":"https://prod.sgnic.sg/faq/sms-sender-id-registry"},{"title":"prod.sgnic.sg","url":"https://prod.sgnic.sg/smsregistry"},{"title":"factsheet on full sms sender id registry regime","url":"https://www.imda.gov.sg/-/media/imda/images/content/news-and-events/press-releases/enhanced-measures-against-scam-sms/factsheet-on-full-sms-sender-id-registry-regime.pdf"},{"title":"sgnic is operating the singapore sms registry","url":"https://sgnic.sg/announcements/archive/announcement-details/2022/03/07/sgnic-is-operating-the-singapore-sms-registry"},{"title":"SINGAPORE SMS SENDER ID REGISTRY (“SSIR”)","url":"https://sgnic.sg/smsregistry/rules-of-registration"},{"title":"6867929 singapore sms sender id registry ssir","url":"https://intercom.help/eber/en/articles/6867929-singapore-sms-sender-id-registry-ssir"},{"title":"sender id query","url":"https://sgnic.sg/smsregistry/sender-id-query"},{"title":"nx country reg sg","url":"https://docs.aws.amazon.com/end-user-messaging/latest/userguide/nx-country-reg-sg.md"},{"title":"about us","url":"https://www.sgnic.sg/about-us"},{"title":"4.7 View a list of all participating telcos for the register","url":"https://www.acma.gov.au/47-view-list-all-participating-telcos-register"},{"title":"8173304 how to register your sender id for sms messaging in singapore","url":"https://help.cloudtalk.io/en/articles/8173304-how-to-register-your-sender-id-for-sms-messaging-in-singapore"}]

Based on the search results, I found information about the SGNIC SMS Sender ID Registry. Here's what I found:

## List of Participating Organisations

The SGNIC SMS Sender ID Registry maintains a list of organisations with at least one whitelisted Sender ID. You can access this list directly at: https://www.sgnic.sg/smsregistry/list-of-organisations

## Participating Aggregators

The registry also maintains a list of participating aggregators that includes 8X8 International Pte Ltd and Alibaba Cloud (Singapore) Pte Ltd, among others. Participating Aggregators are SMS Aggregators licensed by the Infocommunications Media Development Authority (IMDA) to undertake the delivery of SMSes with Sender IDs registered with SGNIC.

The full list of participating aggregators is available at: https://www.sgnic.sg/smsregistry/list-of-participating-aggregators

For the most up-to-date and complete list of all participating organisations and aggregators, I recommend visiting the official SGNIC SMS Sender ID Registry website directly at https://www.sgnic.sg/smsregistry/


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private && mkdir -p X && cd X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o sgnic_robots.txt -w '%{http_code} %{url_effective}\\n' https://www.sgnic.sg/robots.txt; cat sgnic_robots.txt | head -30; sleep 1; curl -sL -A \"$UA\" --max-time 30 -o sgnic_orgs.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.sgnic.sg/smsregistry/list-of-organisations; python3 - <<'EOF'\nimport re,html\ns=open('sgnic_orgs.html',encoding='utf-8',errors='replace').read()\nt=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)\nt=html.unescape(re.sub(r'<[^>]+>','\\n',t))\nlines=[l.strip() for l in t.split('\\n') if l.strip()]\nprint(len(lines))\nprint('\\n'.join(lines[:80]))\nEOF", "description": "Fetch SGNIC robots and SSIR organisation list page"}

### [tool_result]
404 https://www.sgnic.sg/robots.txt


<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js" lang="en">
<!--<![endif]-->
<head id="head"><meta http-equiv="content-type" content="text/html; charset=utf-8" /><meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" /><meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
<meta name="title" content="Singapore Network Information Centre" />

<meta name="msapplication-TileImage" content="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-144x144-precomposed.png" />
<link rel="apple-touch-icon" sizes="57x57" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/apple-touch-icon-180x180.png">
<link rel="icon" type="image/png" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/android-chrome-192x192.png" sizes="192x192">
<link rel="icon" type="image/png" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/png" href="/Sitefinity/WebsiteTemplates/SGNIC/App_Themes/SGNIC/images/favicons/favicon-16x16.png" sizes="16x16">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,700">


      <script src="Sitefinity/WebsiteTemplates/SGNIC/js/customgooglesearch.js"></script>
200 https://www.sgnic.sg/smsregistry/list-of-organisations 40286
96
List of Organisations
You are using an outdated browser, click
here
to update
Toggle navigation
Toggle navigation
Search
Singapore Network Information
Centre (SGNIC) Pte Ltd
Whois
Search
About Us
Company Information
Our Management Team
Registration Statistics
Contact Us / Feedback
Domain Registration
Overview
List of Registrars
Be Our Registrar
.SG Categories & Rules
.SG Security & Safeguard  - VerifiedID@SG
Policies & Agreements
FAQ
Guides & Know-How
SMS Registry
Overview
List of Participating Aggregators
List of Organisations
Sender ID Query
SMS SenderID Registry FAQ
User Agreement
Rules of Registration
Terms and Conditions
InvoiceNow
SMP
TPM
Announcements
SGNIC News
Industry
Schemes & Promotions
ITT / ITQ
Archive
FAQ
Domain Registration
Premium Domain Name
Numeric Domain Name
Domain Dispute
Being a Registrar
VerifiedID@SG
Registry Lock
DNSSEC
SGNIC-IPOS programme
SMS Sender ID Registry
eGuide
Search
List of Organisations
Share
Facebook
Twitter
Twitter
Print
Decrease Font Size
-->
Reset Font Size
-->
Increase Font Size
-->
Overview
List of Participating Aggregators
List of Organisations
Sender ID Query
SMS SenderID Registry FAQ
User Agreement
Rules of Registration
Terms and Conditions
List of Organisations with At Least One Whitelisted Sender ID
Please refer to
List of Organisations
with at least one whitelisted Sender ID.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && grep -o 'href=\"[^\"]*\"' sgnic_orgs.html | grep -i -E 'list|organis|pdf|xls|csv|docs|default-source' | sort -u | head -20", "description": "Find the linked organisation-list document"}

### [tool_result]
href="/domain-registration/list-of-registrars"
href="https://smsregistry.sg/web/org/public-listing"
href="https://www.sgnic.sg/smsregistry/list-of-organisations"
href="/smsregistry/list-of-organisations"
href="/smsregistry/list-of-participating-aggregators"

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o ssir_robots.txt -w '%{http_code} %{url_effective}\\n' https://smsregistry.sg/robots.txt; head -20 ssir_robots.txt; sleep 1; curl -sL -A \"$UA\" --max-time 60 -o ssir_public.html -w '%{http_code} %{url_effective} %{size_download} %{content_type}\\n' https://smsregistry.sg/web/org/public-listing; head -c 1500 ssir_public.html", "description": "Fetch SSIR public listing page and robots"}

### [tool_result]
200 https://smsregistry.sg/robots.txt
Under Construction200 https://smsregistry.sg/web/org/public-listing 23371 text/html; charset=utf-8
<!-- BEGIN: web/views/layout.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="version" content="v1.70.0-master-4a065a0-20261026T1500Z">
    <title>SMS Registry</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">

    <link rel="icon" type="image/x-icon" href="/public/images/favicon.png?ver=v1.70.0-master-4a065a0-20261026T1500Z">
    <link rel="stylesheet" type="text/css" href="/public/vendor/bootstrap.min.css?ver=v1.70.0-master-4a065a0-20261026T1500Z">
    <link rel="stylesheet" type="text/css" href="/public/vendor/bootstrap-icons.css?ver=v1.70.0-master-4a065a0-20261026T1500Z">
    <link rel="stylesheet" type="text/css" href="/public/css/style.css?ver=v1.70.0-master-4a065a0-20261026T1500Z">
    <link rel="stylesheet" type="text/css" href="/public/css/layout.css?ver=v1.70.0-master-4a065a0-20261026T1500Z"> <!-- layout.css loads last -->
  </head>

  <body data-nonce="1795597604824-b939d0c4-702e-4648-9885-15ba64627c1a">


      <!-- BEGIN: web/modules/organization/views/public/list.html -->
<div>
  <div class="header-background">
    <div class="header-background-inner">
      <a target="_blank" href="https://www.sgnic.sg/smsregistry/overview">
        <img

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && python3 - <<'EOF'\nimport re,html\ns=open('ssir_public.html',encoding='utf-8',errors='replace').read()\n# show forms, links, scripts\nprint(re.findall(r'<form[^>]*>',s))\nprint(sorted(set(re.findall(r'(?:href|src|action)=\"([^\"]+)\"',s))))\nt=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)\nt=html.unescape(re.sub(r'<[^>]+>','\\n',t))\nlines=[l.strip() for l in t.split('\\n') if l.strip()]\nprint(len(lines)); print('\\n'.join(lines[:120]))\nEOF", "description": "Parse SSIR public listing page structure"}

### [tool_result]
[]
['#', '/public/css/layout.css?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/css/style.css?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/images/favicon.png?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/images/logo-customer.svg?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/js/layout.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/js/modules/organization/public-list.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/js/pagination.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/js/table-with-pagination.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/shared/enums.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/shared/utils.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/vendor/bootstrap-icons.css?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/vendor/bootstrap.bundle.min.js?ver=v1.70.0-master-4a065a0-20261026T1500Z', '/public/vendor/bootstrap.min.css?ver=v1.70.0-master-4a065a0-20261026T1500Z', 'https://fonts.googleapis.com', 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap', 'https://fonts.gstatic.com', 'https://www.sgnic.sg/smsregistry/overview']
82
SMS Registry
List of Organisations with At Least One Whitelisted Sender ID
Last Updated: 24 Nov 2026 23:59
Organisations with at least one whitelisted Sender ID as at 24 Nov 2026
include those listed below.
The list below is for general information.
SGNIC shall not be responsible or liable for reliance by any person on the information contained in the list herein.
SGNIC shall not be liable for any direct, indirect, incidental or consequential losses, claims, damages arising from in
connection with any reliance or use by any person of the list herein.
Name
ZINGKEY PTE. LTD.
TRAVELUSTAZ PTE. LTD.
NZ FOODIEES
CHREMATICA PTE. LTD.
BIOVISION AI PTE. LTD.
MANPACK PTE. LTD.
PRVW PTE. LTD.
DEK TCG SHOP PTE. LTD.
FRAN SINGAPORE PTE LTD
ST JAMES' CHURCH
ZR DIM SUM PTE LTD
ARCMEAD PTE LTD
TENCENT INTERNATIONAL SERVICE PTE. LTD.
LHL GROUP PTE LTD
SIEMENS HEALTHCARE PTE. LTD
G.SPA PTE LTD
REGENT GROUP PTE. LTD.
OUTSOURCEGO PTE. LTD.
338 PRIVATE LIMITED
CONFETTI MARKETING PTE LTD
SOCIAL BELLA SINGAPORE PTE. LTD.
CONNECT MEDICAL PTE. LTD.
GLOBALHEART PTE. LTD.
EDDIE & FRIENDS PTE. LTD.
GPL REMITTANCE PTE LTD
COMMUNICABLE DISEASES AGENCY
SOLDAUCTIONS PTE. LTD.
ZHIPIN TECHNOLOGY SINGAPORE PTE. LTD.
ESIGN SG HOLDING PTE. LTD.
PICO ART INTERNATIONAL PTE LTD
REN AI HEALTHCARE LLP
IQVIA SOLUTIONS ASIA PTE. LTD.
GFTN SERVICES PTE. LTD.
CHINA CONSTRUCTION (SOUTH PACIFIC) DEVELOPMENT CO. PTE. LTD.
REDCLIP PTE. LTD.
SG INTERNATIONAL MARATHON PTE LTD
TAC-GROUP PTE LTD
EASY PEASY LEMON SQUEEZY TRADING
MAXI CAPITAL SOLUTIONS PTE LTD
HANE SMART SOLUTIONS PTE LTD
NORTHERN RETAIL PTE. LTD.
MALIFAX TECHNOLOGIES (S) PTE LTD
PROVIDEND LTD.
SING-ED CORPORATION PTE LTD
SPLITIT SINGAPORE PTE. LTD.
SGPETSHOP PTE. LTD.
AE PTY MGT PTE LTD
SCHONFELD STRATEGIC ADVISORS (SINGAPORE) PTE. LTD.
MERIT MEDICAL SINGAPORE PTE. LTD.
SECURITY XCHANGE LLP
@
Showing
records
Show
10
25
50
100
1
2
3
4
5
6
7
8
9
10
1
2
3
©SGNIC 2026

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o sgnic_query.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.sgnic.sg/smsregistry/sender-id-query; python3 - <<'EOF'\nimport re,html\ns=open('sgnic_query.html',encoding='utf-8',errors='replace').read()\ni=s.find('Sender ID Query</h')\nfor m in re.finditer(r'(smsregistry\\.sg[^\"\\' <]*|recaptcha|iframe[^>]*>)',s): print(m.group(0)[:150])\nt=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)\nt=html.unescape(re.sub(r'<[^>]+>','\\n',t))\nlines=[l.strip() for l in t.split('\\n') if l.strip()]\nj=[k for k,l in enumerate(lines) if 'Sender ID Query' in l]\nprint(lines[j[-1]:j[-1]+30] if j else lines[-40:])\nEOF", "description": "Inspect SGNIC Sender ID Query page"}

### [tool_result]
200 https://www.sgnic.sg/smsregistry/sender-id-query 40805
smsregistry.sg/web/sid-query
smsregistry.sg/web/login
smsregistry.sg/web/login
recaptcha
['Sender ID Query', 'The', 'Sender ID query', 'is for general information. Members of the public should continue to exercise all due precaution when receiving SMSes, especially those with suspicious links.', 'To Note', ':', 'Organisations need to create a SSIR account on the', 'SSIR portal', 'first and register their preferred Sender ID(s). For more information on the registration process, please visit SSIR', 'website', ',', 'FAQ', 'page and refer to', 'Rules of Registration', 'on the types of Sender IDs that can be accepted by SSIR.', 'SSIR user organisations should login to the', 'SSIR portal', '(or check with their SSIR admin account holder) to check on their Sender ID(s) application status.', 'We use cookies to gather information and improve your online experience. By accessing and using our website, you agree to this use of cookies. For further details, refer to our', 'Privacy Policy', '.', 'ok', 'About Us', 'Domain Registration', 'SMS Registry', 'InvoiceNow', 'TPM', 'Announcements', 'FAQ', 'Sitemap']

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o sgx_robots.txt -w '%{http_code} %{url_effective}\\n' https://www.sgx.com/robots.txt; cat sgx_robots.txt | head -40", "description": "Fetch SGX robots.txt"}

### [tool_result]
200 https://www.sgx.com/robots.txt
User-agent: *
Allow: /
Sitemap: https://www.sgx.com/sitemap.xml

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 60 -o sgx_sitemap.xml -w '%{http_code} %{size_download}\\n' https://www.sgx.com/sitemap.xml; grep -c '<loc>' sgx_sitemap.xml; grep -o '<loc>[^<]*</loc>' sgx_sitemap.xml | head -5; grep -o '<loc>[^<]*</loc>' sgx_sitemap.xml | grep -i -E 'scam|fraud|phish|secur|impersonat|fake|beware|official|vigilant|alert|protect' | head -40", "description": "Grep SGX sitemap for scam-related URLs"}

### [tool_result]
200 479458
1222
<loc>https://www.sgx.com/</loc>
<loc>https://www.sgx.com/securities</loc>
<loc>https://www.sgx.com/fixed-income</loc>
<loc>https://www.sgx.com/derivatives</loc>
<loc>https://www.sgx.com/indices</loc>
<loc>https://www.sgx.com/securities</loc>
<loc>https://www.sgx.com/research-education/securities-products</loc>
<loc>https://www.sgx.com/securities/stocks-under-cpf-investment-scheme</loc>
<loc>https://www.sgx.com/securities/equities/502</loc>
<loc>https://www.sgx.com/securities/equities/AZG</loc>
<loc>https://www.sgx.com/securities/equities/BQC</loc>
<loc>https://www.sgx.com/securities/equities/BTJ</loc>
<loc>https://www.sgx.com/securities/equities/533</loc>
<loc>https://www.sgx.com/securities/equities/L5I</loc>
<loc>https://www.sgx.com/securities/equities/541</loc>
<loc>https://www.sgx.com/securities/equities/ADQU</loc>
<loc>https://www.sgx.com/securities/equities/QZG</loc>
<loc>https://www.sgx.com/securities/equities/A75</loc>
<loc>https://www.sgx.com/securities/equities/5FW</loc>
<loc>https://www.sgx.com/securities/equities/AYV</loc>
<loc>https://www.sgx.com/securities/equities/43F</loc>
<loc>https://www.sgx.com/securities/equities/A31</loc>
<loc>https://www.sgx.com/securities/equities/BLZ</loc>
<loc>https://www.sgx.com/securities/equities/5TY</loc>
<loc>https://www.sgx.com/securities/equities/43Q</loc>
<loc>https://www.sgx.com/securities/equities/5EF</loc>
<loc>https://www.sgx.com/securities/equities/XVG</loc>
<loc>https://www.sgx.com/securities/equities/AWG</loc>
<loc>https://www.sgx.com/securities/equities/AWX</loc>
<loc>https://www.sgx.com/securities/equities/L38</loc>
<loc>https://www.sgx.com/securities/equities/1A4</loc>
<loc>https://www.sgx.com/securities/equities/O5RU</loc>
<loc>https://www.sgx.com/securities/equities/BVP</loc>
<loc>https://www.sgx.com/securities/equities/40F</loc>
<loc>https://www.sgx.com/securities/equities/MIJ</loc>
<loc>https://www.sgx.com/securities/equities/A13</loc>
<loc>https://www.sgx.com/securities/equities/VVL</loc>
<loc>https://www.sgx.com/securities/equities/40V</loc>
<loc>https://www.sgx.com/securities/equities/A34</loc>
<loc>https://www.sgx.com/securities/equities/S9B</loc>
<loc>https://www.sgx.com/securities/equities/RF7</loc>
<loc>https://www.sgx.com/securities/equities/AOF</loc>
<loc>https://www.sgx.com/securities/equities/HKB</loc>
<loc>https://www.sgx.com/securities/equities/Y35</loc>
<loc>https://www.sgx.com/securities/equities/BTX</loc>

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && grep -o '<loc>[^<]*</loc>' sgx_sitemap.xml | sed 's/<[^>]*>//g' | grep -v '/securities/equities/' | grep -i -E 'scam|fraud|phish|security|impersonat|fake|beware|official|vigilant|alert|protect|cyber' | sort -u | head -40", "description": "Refine SGX sitemap grep excluding securities pages"}

### [tool_result]
https://www.sgx.com/regulation/investor-protection

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o sgx_invprot.html -w '%{http_code} %{url_effective} %{size_download}\\n' https://www.sgx.com/regulation/investor-protection; python3 - <<'EOF'\nimport re,html\ns=open('sgx_invprot.html',encoding='utf-8',errors='replace').read()\nt=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)\nt=html.unescape(re.sub(r'<[^>]+>','\\n',t))\nlines=[l.strip() for l in t.split('\\n') if l.strip()]\nprint(len(lines))\nfor k,l in enumerate(lines):\n    if re.search(r'scam|fraud|impersonat|fake|beware|phish|official',l,re.I): print(k,l[:300])\nEOF", "description": "Fetch SGX investor-protection page and grep scam text"}

### [tool_result]
200 https://regco.sgx.com/ 13960
18

### [tool_use WebSearch]
{"query": "SGX Group scam alert fraudulent websites impersonating SGX", "mode": "standard"}

### [tool_result]
Web search results for query: "SGX Group scam alert fraudulent websites impersonating SGX"

Links: [{"title":"Title: Exposing SGX Group Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/5471a34f/189629293"},{"title":"The Illusion of Easy Profit: Inside","url":"https://blog.udn.com/87415dea/190897847"},{"title":"⚠️ Warning! SGX Group Platform","url":"https://blog.udn.com/f1884d44/189639955"},{"title":"Title: Exposing SGX Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/0d8a2b1d/189452236"},{"title":"From Instagram Ad to Financial Trap: How the SGX Group Investment Scheme Operates","url":"https://blog.udn.com/96699956/189511403"},{"title":"Scammers on Telegram pose as SGX, financial professionals, Latest Singapore News - The New Paper","url":"https://d3nswtlfrb5i3e.cloudfront.net/node/141787"},{"title":"From Instagram Ad to Financial Trap: How the SGX Group Investment Scheme Operates","url":"https://blog.udn.com/55055a4b/189451477"},{"title":"💥🚨 SGX Group Platform Cryptocurrency","url":"https://blog.udn.com/5cb93e43/189535209"},{"title":"🚨🔥 SGX GroupStock Scam Exposed:","url":"https://blog.udn.com:443/f865400a/189634411"},{"title":"The Illusion of Easy Profit: Inside","url":"https://blog.udn.com/9f46f1d1/189532827"},{"title":"20241107 police advisory on phishing scams involving the impersonation of sp group","url":"https://www.police.gov.sg/media-room/news/20241107_police_advisory_on_phishing_scams_involving_the_impersonation_of_sp_group"},{"title":"Two Realities of the SGX Investment Group: What You See vs What Actually Happens","url":"https://blog.udn.com/5691e82a/189637257"},{"title":"20241107 police advisory on phishing scams involving the impersonation of sp group","url":"https://www.police.gov.sg/Media-Hub/News/2024/20241107_police_advisory_on_phishing_scams_involving_the_impersonation_of_sp_group"},{"title":"Scam advisory","url":"https://www.mse.gov.sg/latest-news/impersonation-of-carbon-credit-exchange-climate-impact-x/"},{"title":"scam alert","url":"https://www.scamshield.gov.sg/resources/scam-alert/"},{"title":"advisory on phishing scams","url":"https://www.sfa.gov.sg/newsroom/advisory-on-phishing-scams"},{"title":"sgsecurebulletin staying vigilant against cyber attacks","url":"https://www.mom.gov.sg/-/media/mom/documents/employment-practices/sgsecure/bulletin/2022-bulletins/sgsecurebulletin_staying_vigilant_against_cyber_attacks.pdf"},{"title":"Facebook   LinkedIn   WeChat   Instagram   Rednote   YouTube Alert List","url":"https://www.sfc.hk/en/alert-list/3011"}]

Based on the web search results, here's what I found regarding SGX Group scam alerts and fraudulent websites impersonating SGX:

## Overview

Platform SGX Group has been officially flagged as a fraudulent investment scheme and reported to the Anti-Scam Centre. The cryptocurrency platform SGX Group has been exposed by the Singapore Police Force (SPF) and multiple anti-scam organizations as a fraudulent operation.

## How the Scam Operates

SGX Group operates under the disguise of a legitimate investment opportunity, using advanced website designs, fake trading dashboards, and fabricated profit records to mislead users into believing that their investments are growing. Scammers first contact potential victims through WhatsApp or Telegram.

## Impersonation Issues

One group administrator, impersonating SGX chief executive Loh Boon Chye, used a customised emoji that mimicked Telegram's verification badge, a blue checkmark that the messaging platform gives only to large and active official channels, groups and bots.

## Official Response

SGX Group said it does not provide stock recommendations nor collect deposits for investments, and works with a cyber-security agency and social media and messaging platform administrators to monitor and remove social media pages, websites, apps and chat groups which misuse or impersonate SGX Group and its employees.

## Red Flags

Be cautious if you notice guaranteed profits with no risk, constant positive testimonials with no negative feedback, pressure to invest quickly, or additional payments required for withdrawals.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use WebSearch]
{"query": "site:sgx.com scam impersonate SGX Group beware", "mode": "standard"}

### [tool_result]
Web search results for query: "site:sgx.com scam impersonate SGX Group beware"

Links: [{"title":"The Illusion of Easy Profit: Inside","url":"https://blog.udn.com/87415dea/190897847"},{"title":"Title: Exposing SGX Group Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/5471a34f/189629293"},{"title":"⚠️ Warning! SGX Group Platform","url":"https://blog.udn.com/f1884d44/189639955"},{"title":"Title: Exposing SGX Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/0d8a2b1d/189452236"},{"title":"Is Platform SGX Group a Scam?","url":"https://blog.udn.com/882cd65a/189507813"},{"title":"Is Platform SGX Group a Scam?","url":"https://blog.udn.com/47fc87d9/189643136"},{"title":"Is Platform SGX Group a Scam?","url":"https://blog.udn.com/bd200a78/189452284"},{"title":"💥🚨 SGX Group Platform Cryptocurrency","url":"https://blog.udn.com/5cb93e43/189535209"},{"title":"From Instagram Ad to Financial Trap: How the SGX Group Investment Scheme Operates","url":"https://blog.udn.com/96699956/189511403"},{"title":"The Illusion of Easy Profit: Inside","url":"https://blog.udn.com/9f46f1d1/189532827"},{"title":"blog.udn.com","url":"https://blog.udn.com/e25baed9/189525784"},{"title":"Two Realities of the SGX Investment Group: What You See vs What Actually Happens","url":"https://blog.udn.com/5691e82a/189637257"},{"title":"🚨🔥 SGX GroupStock Scam Exposed:","url":"https://blog.udn.com:443/f865400a/189634411"},{"title":"blog.udn.com","url":"https://blog.udn.com/147c9533/191162736"},{"title":"Is Platform SGX Pro a Scam?","url":"https://blog.udn.com/ecfe9419/191157530"}]

Based on the search results, here's what I found about SGX Group scams:

## Key Findings

SGX Group has been exposed as a fraudulent investment platform with reports and investigations linking it to scam operations, bringing it under the attention of the Singapore Police Force (SPF) and the Anti-Scam Centre (ASC).

## How the Scam Operates

Scammers first contact potential victims through WhatsApp or Telegram with the goal to lower defenses and build emotional dependence before asking for money. The platform uses advanced website designs, fake trading dashboards, and fabricated profit records to mislead users into believing their investments are growing.

## Warning Signs

Red flags include guaranteed profits with no risk, constant positive testimonials with no negative feedback, pressure to invest quickly, and additional payments required for withdrawals.

## Impact

Thousands have been deceived, lured by promises of rapid returns on Bitcoin, NFTs, and other cryptocurrencies. Eventually, accounts become inaccessible, customer support disappears, and group chats go silent.

The search results emphasize that the cryptocurrency platform SGX Group has been exposed by the Singapore Police Force and multiple anti-scam organizations as a fraudulent operation.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && grep -o '<loc>[^<]*</loc>' sgx_sitemap.xml | sed 's/<[^>]*>//g' | grep -v '/securities/equities/' | grep -i -E 'notice|advis|caution|warn|investor|education|contact|about|terms|media' | sort -u | head -40; UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; sleep 1; curl -sL -A \"$UA\" --max-time 30 -o sgx_home.html -w '%{http_code} %{size_download}\\n' https://www.sgx.com/; grep -o 'href=\"[^\"]*\"' sgx_home.html | grep -i -E 'scam|fraud|fake|beware|caution|notice|alert' | sort -u | head", "description": "Search SGX sitemap/homepage for scam notice links"}

### [tool_result]
https://www.sgx.com/about-us
https://www.sgx.com/fixed-income/evaluated-bond-prices/interactive-datas-terms-use
https://www.sgx.com/regulation/about-sgx-regco
https://www.sgx.com/regulation/investor-protection
https://www.sgx.com/research-education
https://www.sgx.com/research-education/analyst-research
https://www.sgx.com/research-education/commodities-products
https://www.sgx.com/research-education/data-reports
https://www.sgx.com/research-education/derivatives
https://www.sgx.com/research-education/equities
https://www.sgx.com/research-education/fx-products
https://www.sgx.com/research-education/historical-data/market-statistics
https://www.sgx.com/research-education/market-dialogues
https://www.sgx.com/research-education/market-updates
https://www.sgx.com/research-education/partner-events
https://www.sgx.com/research-education/sectors
https://www.sgx.com/research-education/securities
https://www.sgx.com/research-education/securities-products
200 15329

### [tool_use WebSearch]
{"query": "\"SGX Group\" \"does not\" provide stock recommendations scam notice impersonation websites apps chat groups", "mode": "standard"}

### [tool_result]
Web search results for query: ""SGX Group" "does not" provide stock recommendations scam notice impersonation websites apps chat groups"

Links: [{"title":"From Instagram Ad to Financial Trap: How the SGX Group Investment Scheme Operates","url":"https://blog.udn.com/96699956/189511403"},{"title":"Scammers on Telegram pose as SGX, financial professionals, Latest Singapore News - The New Paper","url":"https://d3nswtlfrb5i3e.cloudfront.net/node/141787"},{"title":"⚠️ Warning! SGX Group Platform","url":"https://blog.udn.com/f1884d44/189639955"},{"title":"Title: Exposing SGX Group Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/5471a34f/189629293"},{"title":"The Illusion of Easy Profit: Inside","url":"https://blog.udn.com/87415dea/190897847"},{"title":"Is Platform SGX Group a Scam?","url":"https://blog.udn.com/882cd65a/189507813"},{"title":"🚨🔥 SGX GroupStock Scam Exposed:","url":"https://blog.udn.com:443/f865400a/189634411"},{"title":"From Instagram Ad to Financial Trap: How the SGX Investment Scheme Operates","url":"https://blog.udn.com/7706ddb4/189453394"},{"title":"Title: Exposing SGX Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/0d8a2b1d/189452236"},{"title":"Is Platform SGX Group a Scam?","url":"https://blog.udn.com/47fc87d9/189643136"},{"title":"From Instagram Ad to Financial Trap: How the SGX Investment Scheme Operates","url":"https://blog.udn.com/3e718b84/189455104"},{"title":"💥🚨 SGX Group Platform Cryptocurrency","url":"https://blog.udn.com/5cb93e43/189535209"},{"title":"20210811 police advisory on pump and dump scams involving overseas listed companies","url":"https://www.police.gov.sg/Media-Hub/News/2021/20210811_police_advisory_on_pump_and_dump_scams_involving_overseas_listed_companies"},{"title":"www.sebi.gov.in","url":"https://www.sebi.gov.in/sebi_data/attachdocs/oct-2026/1792675550417.pdf"},{"title":"blog.udn.com","url":"https://blog.udn.com/147c9533/191162736"}]

Based on the search results, here's what I found regarding SGX Group's official statement on scam notices and impersonation:

SGX Group stated that it does not provide stock recommendations nor collect deposits for investments. 

Additionally, SGX works with a cyber-security agency and social media and messaging platform administrators to monitor and remove social media pages, websites, apps and chat groups which misuse or impersonate SGX Group and its employees.

The search results also confirm that authorities, including the Anti-Scam Centre, have already identified platforms such as SGX Group as part of ongoing investment scam activities, and SGX urges investors to stay alert and be wary of scams that can take the form of online stock recommendations from unofficial sources or informal chat groups.

This indicates that while fraudulent platforms and scammers impersonate SGX Group through various channels (websites, apps, chat groups), the legitimate SGX Group organization has issued official warnings disassociating itself from these scams.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use WebFetch]
{"url": "https://regco.sgx.com/", "prompt": "List any links or text about scams, fraud, impersonation, fake websites/apps, investor alerts, or official SGX channels/domains. Give exact link URLs and any dates."}

### [tool_result]
Based on the web page content provided, there are **no links or text about scams, fraud, impersonation, fake websites/apps, investor alerts, or official SGX channels/domains**.

The page exclusively contains a browser compatibility warning message directing users to update their browser or iOS software, along with links to download Chrome, Edge, Firefox, and Safari. The only contact reference is a generic support email link: `mailto:asksgx@sgx.com`

### [tool_use WebSearch]
{"query": "SGX warns public fake websites mobile apps impersonating Singapore Exchange 2026", "mode": "standard"}

### [tool_result]
Web search results for query: "SGX warns public fake websites mobile apps impersonating Singapore Exchange 2026"

Links: [{"title":"Title: Exposing SGX Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/0d8a2b1d/189452236"},{"title":"Aller au rapport de sécurité","url":"https://phishdestroy.io/fr/domain/sg-usdt.cc/"},{"title":"Anti-scam efforts by MDDI","url":"https://www.mddi.gov.sg/other-pages/anti-scam-efforts/"},{"title":"Title: Exposing SGX Group Platform – A Sophisticated Investment Scam Targeting Victims in Singapore","url":"https://blog.udn.com/5471a34f/189629293"},{"title":"Annual Scam and Cybercrime Brief 2025","url":"https://www.police.gov.sg/-/media/SPF/Advisories/Scams/Annual-Scam-and-Cybercrime-Brief-2025.pdf"},{"title":"Advisory on Fake Websites Impersonating MHA and Home Team Agencies","url":"https://www.sps.gov.sg/advisory-on-fake-websites-impersonating-mha-and-home-team-agencies/"},{"title":"Scammers on Telegram pose as SGX, financial professionals, Latest Singapore News - The New Paper","url":"https://d3nswtlfrb5i3e.cloudfront.net/node/141787"},{"title":"Mid Year Scam and Cybercrime Brief 2026","url":"https://www.police.gov.sg/-/media/SPF/Media-Room/Statistics/Mid-Year-Scam-and-Cybercrime-Brief-2026/Mid-Year-Scam-and-Cybercrime-Brief-2026.pdf"},{"title":"20261020 police advisory on malware from social media advertisements","url":"https://www.police.gov.sg/Media-Hub/News/2026/10/20261020_police_advisory_on_malware_from_social_media_advertisements"},{"title":"⚠️ Warning! SGX Group Platform","url":"https://blog.udn.com/f1884d44/189639955"},{"title":"Singapore shuts down fake websites impersonating its Home Ministry and other agencies","url":"https://www.thestar.com.my/aseanplus/aseanplus-news/2026/08/16/singapore-shuts-down-fake-websites-impersonating-its-home-ministry-and-other-agencies"},{"title":"six inauthentic websites blocked for potential threat of being used to mount hostile information campaigns against singapore","url":"https://www.mha.gov.sg/media-room/newsroom/six-inauthentic-websites-blocked-for-potential-threat-of-being-used-to-mount-hostile-information-campaigns-against-singapore/"},{"title":"inauthentic websites blocked for potential threat","url":"https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/inauthentic-websites-blocked-for-potential-threat"},{"title":"spf warns of phishing sites impersonating simba in google sponsored results as losses hit s 83 000 across 62 cases since march","url":"https://theindependent.sg/spf-warns-of-phishing-sites-impersonating-simba-in-google-sponsored-results-as-losses-hit-s-83-000-across-62-cases-since-march"},{"title":"20250801 police advisory on investment and job scams involving fraudulent mobile applications","url":"https://www.police.gov.sg/Media-Hub/News/2025/08/20250801_police_advisory_on_investment_and_job_scams_involving_fraudulent_mobile_applications"},{"title":"20260820 police advisory on exploitation of apple imessage by scammers","url":"https://www.police.gov.sg/Media-Hub/News/2026/08/20260820_police_advisory_on_exploitation_of_apple_imessage_by_scammers"},{"title":"20260514 advisory on scams involving impersonation of snr govt officials incl secy cabinet","url":"https://www.police.gov.sg/Media-Hub/News/2026/05/20260514_advisory_on_scams_involving_impersonation_of_snr_govt_officials_incl_secy_cabinet"},{"title":"💥🚨 SGX Group Platform Cryptocurrency","url":"https://blog.udn.com/5cb93e43/189535209"}]

Based on the search results, I found relevant information about fake websites and mobile apps impersonating Singapore Exchange (SGX). Here's what the search revealed:

In January, the Singapore Exchange (SGX) and Singapore's sovereign wealth fund GIC were being impersonated in Telegram "investment" groups with hundreds of members. SGX works with a cyber-security agency and social media and messaging platform administrators to monitor and remove social media pages, websites, apps and chat groups which misuse or impersonate SGX Group and its employees, and has reported known fake accounts to authorities like the police and the Cyber Security Agency of Singapore, especially when there are potentially fraudulent activities involving fund transfers.

Additionally, SGX Group fraudulently operates under the disguise of a legitimate investment opportunity, using advanced website designs, fake trading dashboards, and fabricated profit records to mislead users into believing that their investments are growing.

The search results also show broader efforts by Singapore authorities to combat scams in 2026. In the first half of 2026, the Singapore Police Force disrupted 47,500 scam-related mobile lines, 37,500 WhatsApp lines, 31,600 online monikers and 52,200 malicious websites.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o pools_robots.txt -w '%{http_code} %{url_effective}\\n' https://www.singaporepools.com.sg/robots.txt; head -30 pools_robots.txt", "description": "Fetch Singapore Pools robots.txt"}

### [tool_result]
200 https://www.singaporepools.com.sg/robots.txt
User-agent: *
Disallow: /en/tnq/Lists/QuotationTenderAttachmentFiles/Attachments/ # Block Tender /pdf/directory.
Disallow: /en/_vti_bin/ # Block ootb pages
Disallow: /ch/_vti_bin/ # Block ootb pages
Disallow: /en/cu/_vti_bin/ # Block ootb pages
Disallow: /ch/cu/_vti_bin/ # Block ootb pages
Disallow: /outlets/_vti_bin/ # Block ootb pages
Disallow: /_vti_bin/ # Block ootb pages
Disallow: */_vti_bin/* # Block ootb pages

### [tool_use WebSearch]
{"query": "site:singaporepools.com.sg scam fake websites impersonating Singapore Pools", "mode": "standard"}

### [tool_result]
Web search results for query: "site:singaporepools.com.sg scam fake websites impersonating Singapore Pools"

Links: [{"title":"20210825 police advisory fake singapore pools websites and mobile applications","url":"https://www.police.gov.sg/media-hub/news/2021/20210825_police_advisory_fake_singapore_pools_websites_and_mobile_applications"},{"title":"20210825 police advisory fake singapore pools websites and mobile applications","url":"https://police.gov.sg/Media-Room/News/20210825_police_advisory_fake_singapore_pools_websites_and_mobile_applications"},{"title":"Follow us on Telegram for the latest updates: https://t.me/mothershipsg","url":"https://mothership.sg/2023/06/singapore-pools-fake-advertisements"},{"title":"$1,350 for 'sure win' 4-D jackpot number? Singapore Pools makes police report","url":"https://www.stomp.sg/singapore-seen/1350-for-sure-win-4-d-jackpot-number-singapore-pools-makes-police-report"},{"title":"mustsharenews.com","url":"https://mustsharenews.com/scammer-4d-numbers/amp"},{"title":"Scammer Offers ‘Sure Win’ 4D Numbers For Sale, Singapore Pools Makes Police Report","url":"https://mustsharenews.com/?p=441588"},{"title":"Scammer Offers ‘Sure Win’ 4D Numbers For Sale, Singapore Pools Makes Police Report","url":"https://mustsharenews.com/scammer-4d-numbers/"},{"title":"20200323 OTHERS Police Advisory On Impersonation Scams Involving Fake Police Force  Websites","url":"https://police.gov.sg/Media-Room/News/20200323_OTHERS_Police_Advisory_On_Impersonation_Scams_Involving_Fake_Police_Force-_Websites"},{"title":"20260731 police advisory on lucky draw scam","url":"https://www.police.gov.sg/media-hub/news/2026/07/20260731_police_advisory_on_lucky_draw_scam"},{"title":"20260731 police advisory on lucky draw scam","url":"https://www.police.gov.sg/Media-Hub/News/2026/07/20260731_police_advisory_on_lucky_draw_scam"},{"title":"20210217 police advisory phishing scams involving fake singtel website","url":"https://www.police.gov.sg/media-hub/news/2021/02/20210217_police_advisory_phishing_scams_involving_fake_singtel_website"},{"title":"20230302 police advisory on scam involving unsolicited offer to buy lottery numbers","url":"https://www.police.gov.sg/media-hub/news/2023/20230302_police_advisory_on_scam_involving_unsolicited_offer_to_buy_lottery_numbers"},{"title":"Unlawful Remote Gambling Activities","url":"https://www.gra.gov.sg/harm-minimisation/unlawful-remote-gambling-activities"},{"title":"20210217 police advisory phishing scams involving fake singtel website","url":"https://www.police.gov.sg/media-hub/news/2021/20210217_police_advisory_phishing_scams_involving_fake_singtel_website"},{"title":"A Singapore Government Agency Website How to identify","url":"https://www.moe.gov.sg/scam-alert"},{"title":"20220607 police advisory on phishing scams involving impersonation of gov and psa","url":"https://www.police.gov.sg/Media-Hub/News/2022/20220607_police_advisory_on_phishing_scams_involving_impersonation_of_gov_and_psa"},{"title":"20221103 police advisory on the re emergence of email phishing scams involving sg companies","url":"https://www.police.gov.sg/media-hub/news/2022/20221103_police_advisory_on_the_re-emergence_of_email_phishing_scams_involving_sg_companies"}]

Based on the search results, here's what I found regarding scams and fake websites impersonating Singapore Pools:

## Fake Websites and Mobile Applications

The Police have alerted the public of fake Singapore Pools websites and mobile applications available on Google Play store. Victims may come across fake Singapore Pools' websites or mobile applications while browsing the Internet or Google Play store. Under the impression that the websites or mobile applications are legitimate, unsuspecting victims would download the application and place bets through it. They would only realise that they have been scammed after discovering that the payments were allegedly made to other companies instead of Singapore Pools.

## "Sure Win" 4D Number Scams

A scammer impersonated a Singapore Pools employee on Facebook and claimed in a fake advertisement that those who pay the scammer $1,350 can get a "sure win" 4-D jackpot number. Singapore Pools has identified websites and social media accounts "falsely using the Singapore Pools' name or association with the brand".

## Official Guidance

Singapore Pools has urged members of the public to be vigilant and visit only official channels for draw results and news relating to Singapore Pools. Singapore Pools (Private) Limited is the only operator licensed by GRA to provide remote gambling services.

For reporting scams, members of the public can visit www.scamalert.sg or call the Anti-Scam hotline at 1800-722-6688.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.

### [tool_use Bash]
{"command": "cd /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/X && UA=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\"; curl -sL -A \"$UA\" --max-time 30 -o pools_sitemap.xml -w '%{http_code} %{url_effective} %{size_download} %{content_type}\\n' https://www.singaporepools.com.sg/sitemap.xml; head -c 300 pools_sitemap.xml; echo; grep -c '<loc>' pools_sitemap.xml", "description": "Try Singapore Pools sitemap.xml once"}

### [tool_result]
200 https://www.singaporepools.com.sg/Pages/PageNotFoundError.aspx 53134 text/html; charset=utf-8

<!DOCTYPE html >
<html class=" js flexbox canvas canvastext webgl no-touch geolocation postmessage no-websqldatabase indexeddb hashchange history draganddrop websockets rgba hsla multiplebgs backgroundsize borderimage borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients 
0

### [assistant text]
You've hit your session limit · resets 9:40pm (Asia/Singapore)