# Source catalog: SG scope & polling plan (2026-11-26T06:40:23Z)

**native** = SG publisher, SG-only content: ingested as-is. **filtered** = global feed: every item must pass `sg_filter_pass()` (SG brand/service token in host, or SG bank kit path; `.sg` ccTLD alone is rejected). **allowlist** = official-channel pages: feed the allowlist, never the IOC stream.

| scope | hot (≤1h) | daily | weekly | monthly | total |
|---|---|---|---|---|---|
| native | 3 | 48 | 122 | 140 | 313 |
| filtered | 2 | 5 | 0 | 0 | 7 |
| allowlist | 0 | 0 | 43 | 0 | 43 |

363 sources over 363 distinct endpoints (shared sitemaps/feeds fetched once).

## Filtered (global feeds → SG filter)

| source | tier | parser | licence |
|---|---|---|---|
| phishdb-links-new-today | hot | url_list | MIT |
| phishdb-links-active | daily | url_list | MIT |
| phishdb-domains-active | daily | url_list | MIT |
| phishing-army-extended | daily | url_list | GPL-3.0 generator; upstream ToU |
| phishdestroy | daily | url_list | CC-BY-4.0 |
| openphish-community | daily | url_list | OpenPhish community ToU |
| phishstats-api | hot | phishstats | free tier, 50 req/day anon |

## Native: structured indicator sources

| source | publisher | tier | parser |
|---|---|---|---|
| spf-icanact | Singapore Police Force | hot | spf_icanact |
| mas-ial-opensanctions | Monetary Authority of Singapore | daily | mas_opensanctions |

## Native: machine discovery endpoints (RSS / sitemap)

| publisher | kind | tier | url |
|---|---|---|---|
| AIA Singapore | sitemap | daily | https://www.aia.com.sg/en/sitemap.xml |
| Central Narcotics Bureau | rss | daily | https://www.cnb.gov.sg/mediaroom/news/rss.xml |
| Central Provident Fund Board | sitemap | daily | https://www.cpf.gov.sg/sitemap.xml |
| Citibank Singapore | sitemap | daily | https://www.citibank.com.sg/sitemap.xml |
| Competition and Consumer Commission of Singapore | sitemap | daily | https://www.ccs.gov.sg/sitemap.xml |
| Consumers Association of Singapore | sitemap | daily | https://www.case.org.sg/sitemap.xml |
| Cyber Security Agency of Singapore | rss | daily | https://www.csa.gov.sg/alerts-and-advisories/advisories/rss.xml |
| Cyber Security Agency of Singapore | rss | daily | https://www.csa.gov.sg/alerts-and-advisories/alerts/rss.xml |
| Enterprise Singapore | sitemap | daily | https://www.enterprisesg.gov.sg/sitemap.xml |
| GXS Bank Pte. Ltd. | sitemap | daily | https://www.gxs.com.sg/sitemap.xml |
| Gov.sg (Singapore Government portal) | rss | daily | https://www.gov.sg/explainers/rss.xml |
| Government Technology Agency | rss | daily | https://www.tech.gov.sg/technews/rss.xml |
| Health Sciences Authority | sitemap | daily | https://www.hsa.gov.sg/sitemap.xml |
| Immigration & Checkpoints Authority | sitemap | daily | https://www.ica.gov.sg/sitemap/sitemap.xml |
| Inland Revenue Authority of Singapore | sitemap | daily | https://www.iras.gov.sg/sitemap |
| M1 Limited | sitemap | daily | https://www.m1.com.sg/sitemap-en-support.xml |
| MariBank Singapore Private Limited | sitemap | daily | https://www.maribank.sg/sitemap.xml |
| Ministry of Digital Development and Information | rss | daily | https://www.mddi.gov.sg/newsroom/rss.xml |
| Ministry of Finance | sitemap | daily | https://www.mof.gov.sg/sitemap.xml |
| Ministry of Home Affairs | rss | daily | https://www.mha.gov.sg/media-room/newsroom/rss.xml |
| Ministry of Law | rss | daily | https://www.mlaw.gov.sg/feed.xml |
| Ministry of Manpower | sitemap | daily | https://mom.gov.sg/others.xml |
| Ministry of Manpower | sitemap | daily | https://mom.gov.sg/newsroom.xml |
| Ministry of Sustainability and the Environment | sitemap | daily | https://www.mse.gov.sg/sitemap.xml |
| Monetary Authority of Singapore | sitemap | daily | https://data.opensanctions.org/datasets/latest/sg_mas_investor_alert/targets.simple.csv |
| Monetary Authority of Singapore | sitemap | daily | https://www.mas.gov.sg/sitemap.xml |
| National Crime Prevention Council | rss | daily | https://www.ncpc.org.sg/media-releases/rss.xml |
| Ninja Van Singapore (Ninja Logistics Pte. Ltd.) | sitemap | daily | https://www.ninjavan.co/sitemap.xml |
| OCBC Bank (Oversea-Chinese Banking Corporation) | sitemap | daily | https://www.ocbc.com/sitemap.xml |
| Prudential Assurance Company Singapore | sitemap | daily | https://www.prudential.com.sg/en/sitemap.xml |
| Singapore Airlines | sitemap | daily | https://www.singaporeair.com/content/dam/sia/root/sitemap/sg.xml |
| Singapore Civil Defence Force | sitemap | daily | https://www.scdf.gov.sg/sitemap/sitemap.xml |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | sitemap | daily | https://www.judiciary.gov.sg/sitemap/sitemap.xml |
| Singapore Customs | sitemap | daily | https://www.customs.gov.sg/sitemap.xml |
| Singapore Police Force | sitemap | daily | https://www.police.gov.sg/sitemap/sitemap.xml |
| Singapore Prison Service | rss | daily | https://www.sps.gov.sg/media/rss.xml |
| Singapore Telecommunications Limited (Singtel) | sitemap | daily | https://www.singtel.com/sitemap-support.xml |
| Skills and Workforce Development Agency | sitemap | daily | https://www.swda.gov.sg/sitemap.xml |
| The Straits Times | sitemap | daily | https://www.straitstimes.com/sitemap.xml |
| United Overseas Bank (UOB) Singapore | sitemap | daily | https://www.uob.com.sg/personal/sitemap.xml |
| ScamShield | rss | hot | https://www.scamshield.gov.sg/resources/scam-alert/rss.xml |
| ScamShield | rss | hot | https://www.scamshield.gov.sg/resources/scam-bulletins/rss.xml |
| Accounting and Corporate Regulatory Authority | sitemap | weekly | https://www.acra.gov.sg/sitemap.xml |
| CDC Vouchers Scheme | sitemap | weekly | https://vouchers.cdc.gov.sg/sitemap.xml |
| Changi Airport Group (Singapore Changi Airport) | sitemap | weekly | https://www.changiairport.com/sitemap.xml |
| Circles.Life (Circles Asia) Singapore | sitemap | weekly | https://www.circles.life/sg/sitemap_index.xml |
| Civil Aviation Authority of Singapore | sitemap | weekly | https://www.caas.gov.sg/sitemap.xml |
| Community Development Councils | sitemap | weekly | https://www.cdc.gov.sg/sitemap.xml |
| Council for Estate Agencies | sitemap | weekly | https://www.cea.gov.sg/sitemap.xml |
| DBS Bank (Singapore) | sitemap | weekly | https://www.dbs.com.sg/sitemap-personal-2026.xml |
| Gambling Regulatory Authority of Singapore | sitemap | weekly | https://www.gra.gov.sg/sitemap.xml |
| Grab Singapore (Grab Holdings) | sitemap | weekly | https://www.grab.com/sg/sitemap.xml |
| Great Eastern Life Assurance (Great Eastern Singapore) | sitemap | weekly | https://www.greateasternlife.com/sg/en/sg-en-sitemap.xml |
| HSBC Bank (Singapore) Limited | sitemap | weekly | https://www.hsbc.com.sg/sitemaps-pages.xml |
| HealthHub | sitemap | weekly | https://www.healthhub.sg/sitemap.xml |
| Housing & Development Board | sitemap | weekly | https://www.hdb.gov.sg/sitemap.xml |
| Income Insurance Limited | sitemap | weekly | https://www.income.com.sg/sitemap.xml |
| Intellectual Property Office of Singapore | sitemap | weekly | https://www.ipos.gov.sg/sitemap.xml |
| J&T Express Singapore | sitemap | weekly | https://www.jtexpress.sg/sitemap.xml |
| Ministry of Education | sitemap | weekly | https://www.moe.gov.sg/sitemap.xml |
| Ministry of Health | sitemap | weekly | https://www.moh.gov.sg/sitemap.xml |
| Ministry of Manpower | sitemap | weekly | https://mom.gov.sg/passes-and-permits.xml |
| Ministry of Social and Family Development | sitemap | weekly | https://www.msf.gov.sg/sitemap.xml |
| National Council of Social Service | sitemap | weekly | https://www.ncss.gov.sg/sitemap.xml |
| National University Health System | sitemap | weekly | https://www.nuhs.edu.sg/sitemap/sitemap.xml |
| Network for Electronic Transfers (Singapore) Pte Ltd | sitemap | weekly | https://www.nets.com.sg/sitemap.xml |
| People's Association | sitemap | weekly | https://www.pa.gov.sg/sitemap.xml |
| Personal Data Protection Commission | sitemap | weekly | https://www.pdpc.gov.sg/sitemap.xml |
| Phillip Securities Pte Ltd (POEMS by PhillipCapital) | sitemap | weekly | https://www.poems.com.sg/page-sitemap.xml |
| Phillip Securities Pte Ltd (POEMS by PhillipCapital) | sitemap | weekly | https://www.poems.com.sg/announcements-sitemap.xml |
| Public Transport Voucher (PTV) Exercise | sitemap | weekly | https://www.mot.gov.sg/sitemap.xml |
| SP Group (Singapore Power) | sitemap | weekly | https://www.spgroup.com.sg/sitemap.xml |
| ScamShield | sitemap | weekly | https://www.scamshield.gov.sg/sitemap.xml |
| Shopee Singapore | sitemap | weekly | https://help.shopee.sg/sitemap.xml |
| Singapore Food Agency | sitemap | weekly | https://www.sfa.gov.sg/sitemap.xml |
| Singapore Health Services (SingHealth) | sitemap | weekly | https://www.singhealth.com.sg/sitemap-index.xml |
| Singapore Life Ltd. (Singlife) | sitemap | weekly | https://singlife.com/sitemap.xml |
| Singapore Police Force | sitemap | weekly | https://www.police.gov.sg/docs/spf/spf/media-room/statistics/mid-year-scam-and-cybercrime-brief-2026/mid-year-scam-and-cybercrime-brief-2026.pdf?sfvrsn=370b33ae_0 |
| Singapore Post Limited (SingPost) | sitemap | weekly | https://www.singpost.com/sitemap.xml |
| Singapore Telecommunications Limited (Singtel) | sitemap | weekly | https://www.singtel.com/sitemap-explore.xml |
| Singapore Tourism Board | sitemap | weekly | https://www.stb.gov.sg/sitemap.xml |
| StarHub Ltd | sitemap | weekly | https://www.starhub.com/personal.xml |
| The Straits Times | sitemap | weekly | https://www.straitstimes.com/sitemap/2025/02/feeds.xml |
| Tiger Brokers (Singapore) Pte. Ltd. | sitemap | weekly | https://www.itiger.com/sitemap.xml |
| Trust Bank Singapore Limited | sitemap | weekly | https://trustbank.sg/sitemap.xml |
| UOB Kay Hian Private Limited (Singapore) | sitemap | weekly | https://uobkh.com.sg/sitemap.xml |
| Urban Redevelopment Authority | sitemap | weekly | https://www.ura.gov.sg/sitemap.xml |
| uParcel Singapore | sitemap | weekly | https://www.uparcel.sg/blog-sitemap.xml |

## Native: pages (HTML hash + indicator extraction)

| publisher | page kind | default role | tier | url |
|---|---|---|---|---|
| Accounting and Corporate Regulatory Authority | official_channels | official | weekly | https://www.acra.gov.sg/help-support/public-advisory-protect-yourself-against-scams/ |
| CDC Vouchers Scheme | official_channels | official | weekly | https://vouchers.cdc.gov.sg/residents/faq/ |
| CDC Vouchers Scheme | official_channels | official | weekly | https://vouchers.cdc.gov.sg/residents/how-to-claim-and-spend/ |
| Central Provident Fund Board | official_channels | official | weekly | https://www.cpf.gov.sg/member/account-services/fighting-scams/cpf-account-safeguards |
| Citibank Singapore | official_channels | official | weekly | https://www.citibank.com.sg/static/contact |
| DBS Bank (Singapore) | official_channels | official | weekly | https://www.dbs.com.sg/personal/scam-defence/protecting-yourself-online |
| DHL Singapore (DHL Group) | official_channels | official | weekly | https://www.dhl.com/sg-en/home/footer/fraud-awareness.html |
| DHL Singapore (DHL Group) | official_channels | official | weekly | https://www.dhl.com/discover/en-sg/news/phishing-site-scam-call-advisory |
| GXS Bank Pte. Ltd. | official_channels | official | weekly | https://www.gxs.com.sg/security |
| Go.gov.sg (official government link shortener) | official_channels | official | weekly | https://go.gov.sg/ |
| Go.gov.sg (official government link shortener) | official_channels | official | weekly | https://www.for.sg/ |
| Gov.sg (Singapore Government portal) | official_channels | official | weekly | https://www.gov.sg/trusted-sites/ |
| Gov.sg (Singapore Government portal) | official_channels | official | weekly | https://www.gov.sg/explainers/what-you-need-to-know-gov-sg-sms-sender-id/ |
| Government Technology Agency | official_channels | official | weekly | https://www.tech.gov.sg/technews/which-sms-links-are-scams-and-which-are-not/ |
| Great Eastern Life Assurance (Great Eastern Singapore) | official_channels | official | weekly | https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory.html |
| HSBC Bank (Singapore) Limited | official_channels | official | weekly | https://www.hsbc.com.sg/help/security-centre/fraud-guide/ |
| Income Insurance Limited | official_channels | official | weekly | https://www.income.com.sg/security-advisory |
| Monetary Authority of Singapore | official_channels | official | weekly | https://eservices.mas.gov.sg/fid |
| Moomoo Singapore (Moomoo Financial Singapore Pte. Ltd.) | official_channels | official | weekly | https://www.moomoo.com/sg/learn/scam-alert-from-moomoo-singapore |
| NTUC Link (Link Rewards / Linkpoints) | official_channels | official | weekly | https://support.link.sg/hc/en-us/articles/21169453378969-With-the-recent-scams-how-can-members-be-sure-if-the- |
| National Council of Social Service | official_channels | official | weekly | https://www.ncss.gov.sg/about-us/our-media-centre/announcements-and-advisories/scam-advisory/ |
| National Crime Prevention Council | official_channels | official | weekly | https://www.ncpc.org.sg/scamshield/ |
| OCBC Bank (Oversea-Chinese Banking Corporation) | official_channels | official | weekly | https://www.ocbc.com/personal-banking/security/secure-banking-ways/ocbc-contact-banking-channels |
| Public Transport Voucher (PTV) Exercise | official_channels | official | weekly | https://www.mot.gov.sg/news-resources/newsroom/applications-for-2025-public-transport-voucher-exercise-to-open |
| Registry of Moneylenders (Ministry of Law) | official_channels | official | weekly | https://rom.mlaw.gov.sg/information-for-borrowers/list-of-licensed-moneylenders-in-singapore/ |
| SMS Sender ID Registry (SGNIC, IMDA subsidiary) | official_channels | official | weekly | https://smsregistry.sg/web/org/public-listing |
| ScamShield | official_channels | official | weekly | https://www.scamshield.gov.sg/scid/ |
| ScamShield | official_channels | official | weekly | https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ |
| ScamShield | official_channels | official | weekly | https://www.scamshield.gov.sg/i-want-protection-from-scams/more-ways-to-protect-yourself/verify-with-official- |
| Shopee Singapore | official_channels | official | weekly | https://help.shopee.sg/portal/4/article/83757-%5BAbout-Shopee%5D-What-are-the-official-channels-to-find-inform |
| Shopee Singapore | official_channels | official | weekly | https://help.shopee.sg/portal/4/article/76476-%5BAccount-Safety%5D-How-do-I-ensure-that-I-am-shopping-on-Shope |
| Singapore Airlines | official_channels | official | weekly | https://www.singaporeair.com/en_UK/sg/global_footer/security/ |
| Singapore Civil Defence Force | official_channels | official | weekly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/SCDF's-995-number-to-be |
| Singapore Customs | official_channels | official | weekly | https://www.customs.gov.sg/news/fake-customs-website/ |
| Singapore Police Force | official_channels | official | weekly | https://www.police.gov.sg/media-hub/police-life/2026/11/know-whos-calling-spf-launches-single-caller-id-to-com |
| Singapore Post Limited (SingPost) | official_channels | official | weekly | https://www.singpost.com/online-security-you |
| Singapore Telecommunications Limited (Singtel) | official_channels | official | weekly | https://www.singtel.com/personal/support/scam-advisory#Officialdomains |
| StarHub Ltd | official_channels | official | weekly | https://corporate.starhub.com/about-us/legal-notices-and-terms/clickable-links.html |
| Tiger Brokers (Singapore) Pte. Ltd. | official_channels | official | weekly | https://www.itiger.com/sg/help/detail/Fraud%20Awareness |
| UOB Kay Hian Private Limited (Singapore) | official_channels | official | weekly | https://uobkh.com.sg/en/about/contact |
| Urban Redevelopment Authority | official_channels | official | weekly | https://www.ura.gov.sg/guidelines/best-practices/remaining-vigilant-phishing-scams/ |
| gov.sg SMS Sender ID (OGP/GovTech) | official_channels | official | weekly | https://www.sms.gov.sg/exceptions |
| gov.sg SMS Sender ID (OGP/GovTech) | official_channels | official | weekly | https://www.sms.gov.sg/check |
| AIA Singapore | advisory_feed | unknown | weekly | https://www.aia.com.sg/en/help-support/security-advisory-and-tips |
| Accounting and Corporate Regulatory Authority | alert_page | unknown | weekly | https://www.acra.gov.sg/news-events/news-announcements/acra-alert--beware-of-scam-emails/ |
| Amazon.sg (Amazon Singapore) | scam_faq | unknown | monthly | https://www.amazon.sg/gp/help/customer/display.html?nodeId=G4YFYCCNUSENA23B |
| Attorney-General's Chambers | alert_page | unknown | monthly | https://www.agc.gov.sg/newsroom/agc-media-release---public-advisory-on-scam-letter-bearing-agc-letterhead-and- |
| Attorney-General's Chambers | news_releases | unknown | weekly | https://www.agc.gov.sg/newsroom/media-statement-stern-warning-administered-for-pmo-website-hoax/ |
| CIMB Bank Berhad, Singapore | scam_faq | unknown | monthly | https://www.cimb.com.sg/en/personal/help-support/security-fraud.html |
| CNA (Channel NewsAsia) | news_releases | unknown | weekly | https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=10416 |
| CNA (Channel NewsAsia) | news_releases | unknown | weekly | https://www.channelnewsasia.com/api/v1/sitemap-news-feed |
| CapitaLand Group | scam_faq | unknown | monthly | https://www.capitaland.com/en/footer-links/scam-alert.html |
| Carousell (Singapore) | scam_faq | unknown | monthly | https://support.carousell.com/hc/en-us |
| Central Narcotics Bureau | alert_page | unknown | monthly | https://www.cnb.gov.sg/mediaroom/news/email-scam-sent-using-fake-central-narcotics-bureau-cnb-email-address/ |
| Central Narcotics Bureau | alert_page | unknown | monthly | https://www.cnb.gov.sg/mediaroom/news/anti-drug-abuse-photo-contest-email-impersonating-cnb-and-sp/ |
| Central Narcotics Bureau | alert_page | unknown | monthly | https://www.cnb.gov.sg/mediaroom/news/cnb-advisory-incidents-of-impersonation/ |
| Central Narcotics Bureau | news_releases | unknown | weekly | https://www.cnb.gov.sg/mediaroom/news/ |
| Central Provident Fund Board | alert_page | unknown | monthly | https://www.cpf.gov.sg/member/infohub/cpf-clarifies/clarifications/beware-of-scam-email-requesting-immediate-p |
| Central Provident Fund Board | news_releases | unknown | weekly | https://www.cpf.gov.sg/member/infohub/news/news-releases/joint-advisory-scams-involving-cpf-savings-and-new-me |
| Central Provident Fund Board | scam_faq | unknown | monthly | https://www.cpf.gov.sg/member/infohub/educational-resources/how-to-stay-safe-from-scams |
| Changi Airport Group (Singapore Changi Airport) | alert_page | unknown | monthly | https://www.changiairport.com/en/corporate/our-media-hub/newsroom/2019/cag-alerts-public-of-phone-scam-targett |
| Circles.Life (Circles Asia) Singapore | scam_faq | unknown | monthly | https://www.circles.life/sg/blog/safety-guide-protecting-and-reporting-against-scammer/ |
| Citibank Singapore | advisory_feed | unknown | weekly | https://www.citibank.com.sg/personal-banking/online-services/secure-banking/online-security-tips/ |
| Citibank Singapore | scam_faq | unknown | monthly | https://www.citibank.com.sg/static1/static/prevention-protection/ |
| Citibank Singapore | scam_faq | unknown | monthly | https://www.citibank.com.sg/wealth-management/wealth-insights/financial-fraud-how-to-stay-safe-from-scams |
| Civil Aviation Authority of Singapore | alert_page | unknown | monthly | https://www.caas.gov.sg/resources/media-and-publication/newsroom/caas-advisory-on-email-scam/ |
| Community Development Councils | scam_faq | unknown | monthly | https://www.cdc.gov.sg/common-flagship-programmes/law-awareness/webinars/scam-prevention-response-and-recovery |
| Competition and Consumer Commission of Singapore | fake_indicator_list | ioc | weekly | https://www.ccs.gov.sg/consumer-protection/legislation-and-guidelines/ccs-s-investigations-into-fake-online-re |
| Competition and Consumer Commission of Singapore | news_releases | unknown | weekly | https://www.ccs.gov.sg/case-register/public-register/consumer-protection--fair-trading-/ccs-takes-action-again |
| Consumers Association of Singapore | fake_indicator_list | ioc | weekly | https://www.case.org.sg/company-alert/ |
| Corrupt Practices Investigation Bureau | alert_page | unknown | monthly | https://www.cpib.gov.sg/press-room/advisory-phone-impersonation-scams/ |
| Corrupt Practices Investigation Bureau | scam_faq | unknown | monthly | https://www.cpib.gov.sg/advisory/ |
| Council for Estate Agencies | scam_faq | unknown | monthly | https://www.cea.gov.sg/consumers/rental-scams/ |
| Cyber Security Agency of Singapore | advisory_feed | unknown | weekly | https://www.csa.gov.sg/alerts-and-advisories/advisories/ |
| Cyber Security Agency of Singapore | advisory_feed | unknown | weekly | https://www.csa.gov.sg/alerts-and-advisories/alerts/ |
| Cyber Security Agency of Singapore | alert_page | unknown | weekly | https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2025-123/ |
| Cyber Security Agency of Singapore | report_portal | unknown | monthly | https://www.csa.gov.sg/singcert/reporting |
| DBS Bank (Singapore) | advisory_feed | unknown | daily | https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page |
| DBS Bank (Singapore) | scam_faq | unknown | monthly | https://www.dbs.com.sg/personal/scam-defence/default.page |
| DBS Bank (Singapore) | scam_faq | unknown | monthly | https://www.dbs.com.sg/personal/support/guide-security-on-scams-and-fraud.html |
| EZ-Link Pte Ltd | alert_page | unknown | monthly | https://ezlink.simplygo.com.sg/wordpress/wp-content/uploads/2024/01/Scam-Notice-Updated-31012024.pdf |
| Elections Department | scam_faq | unknown | monthly | https://www.eld.gov.sg/advisory.html |
| Enterprise Singapore | advisory_feed | unknown | weekly | https://www.enterprisesg.gov.sg/scam-advisory |
| GXS Bank Pte. Ltd. | news_releases | unknown | weekly | https://www.gxs.com.sg/news-press/gxs-bank-customers-have-an-additional-protection-against-scams-with-the-laun |
| Gambling Regulatory Authority of Singapore | scam_faq | unknown | monthly | https://www.gra.gov.sg/harm-minimisation/unlawful-remote-gambling-activities |
| Gambling Regulatory Authority of Singapore | scam_faq | unknown | monthly | https://www.gra.gov.sg/resources/advisories |
| Gambling Regulatory Authority of Singapore | statistics | unknown | monthly | https://www.gra.gov.sg/newsroom/enforcement-actions |
| Gojek Singapore | scam_faq | unknown | monthly | https://www.gojek.com/sg/safety |
| Gov.sg (Singapore Government portal) | scam_faq | unknown | monthly | https://www.gov.sg/explainers/ |
| Government Technology Agency | advisory_feed | unknown | weekly | https://www.tech.gov.sg/technews/ |
| Government Technology Agency | news_releases | unknown | daily | https://www.tech.gov.sg/media/govtech-launches-antiscam-pango-beta-to-help-users-spot-suspicious-scam-messages |
| Government Technology Agency | report_portal | unknown | monthly | https://www.tech.gov.sg/report-vulnerability/ |
| Government Technology Agency | scam_faq | unknown | monthly | https://www.tech.gov.sg/technews/five-ways-to-keep-your-singpass-safe/ |
| Government Technology Agency | statistics | unknown | monthly | https://www.tech.gov.sg/products-and-services/for-citizens/scam-prevention/satis/ |
| Grab Singapore (Grab Holdings) | scam_faq | unknown | monthly | https://www.grab.com/sg/phishing-2/ |
| Grab Singapore (Grab Holdings) | scam_faq | unknown | monthly | https://www.grab.com/sg/how-to-avoid-scams-fraud-and-identity-theft/ |
| Grab Singapore (Grab Holdings) | scam_faq | unknown | monthly | https://www.grab.com/sg/pay/spot-the-fake/ |
| Grab Singapore (Grab Holdings) | scam_faq | unknown | monthly | https://www.grab.com/sg/about/trust-and-safety/ |
| Great Eastern Life Assurance (Great Eastern Singapore) | alert_page | unknown | monthly | https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-advisory/false-message-efiling.htm |
| Great Eastern Life Assurance (Great Eastern Singapore) | scam_faq | unknown | monthly | https://www.greateasternlife.com/sg/en/privacy-and-security-policy/security-policy.html |
| Great Eastern Life Assurance (Great Eastern Singapore) | scam_faq | unknown | monthly | https://www.greateasternlife.com/sg/en/personal-insurance/lifepedia/savings-and-investment/how-to-protect-fami |
| HSBC Bank (Singapore) Limited | scam_faq | unknown | monthly | https://www.hsbc.com.sg/help/security-centre/ |
| Health Sciences Authority | advisory_feed | unknown | weekly | https://www.hsa.gov.sg/announcements/hsa-alert-cococurv-chocofit-hamercandy/ |
| Health Sciences Authority | alert_page | unknown | monthly | https://www.hsa.gov.sg/announcements/hsa-alerts-the-public-on-fake-tiktok-accounts/ |
| HealthHub | scam_faq | unknown | monthly | https://www.healthhub.sg/highlights-and-insights/health-safety-advisory/stay-safe-when-shopping-online |
| Housing & Development Board | scam_faq | unknown | monthly | https://www.hdb.gov.sg/security-advisory |
| Immigration & Checkpoints Authority | alert_page | unknown | weekly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/advisory-on-scams-involving-the-immigration- |
| Immigration & Checkpoints Authority | alert_page | unknown | weekly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scams-involving-ica |
| Immigration & Checkpoints Authority | alert_page | unknown | weekly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-fake-letters-bearing-ica- |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scam-callers-impersonatin |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scam-callers-impersonatin |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scam-calls-from-ica-sto |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-fake-ica-website |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scam-calls-from-ica |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scam-letters-from-ica |
| Immigration & Checkpoints Authority | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-scam-call-from-ica |
| Immigration & Checkpoints Authority | news_releases | unknown | weekly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room |
| Immigration & Checkpoints Authority | scam_faq | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/public-advisories/advisory-on-fake-or-misleading-websit |
| Infocomm Media Development Authority | news_releases | unknown | weekly | https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/enhanced-measures-against-scam-sms |
| Infocomm Media Development Authority | scam_faq | unknown | monthly | https://www.imda.gov.sg/how-we-can-help/anti-scam-measures |
| Inland Revenue Authority of Singapore | advisory_feed | unknown | weekly | https://www.iras.gov.sg/news-events/announcements/scam-advisory |
| Inland Revenue Authority of Singapore | scam_faq | unknown | monthly | https://www.iras.gov.sg/news-events/announcements/scam-advisory/phishing-email-scam |
| Inland Revenue Authority of Singapore | scam_faq | unknown | monthly | https://www.iras.gov.sg/news-events/announcements/scam-advisory/tax-refund-scam |
| Inland Revenue Authority of Singapore | scam_faq | unknown | monthly | https://www.iras.gov.sg/news-events/announcements/scam-advisory/investment-scam |
| Inland Revenue Authority of Singapore | scam_faq | unknown | monthly | https://www.iras.gov.sg/news-events/announcements/scam-advisory/fake-stamp-certificate-scam |
| Intellectual Property Office of Singapore | alert_page | unknown | monthly | https://www.ipos.gov.sg/news/news-collection/scam-alert-public-advisory-on-scammers-2024/ |
| Intellectual Property Office of Singapore | scam_faq | unknown | monthly | https://www.ipos.gov.sg/manage-ip/unsolicited-ip-services/ |
| J&T Express Singapore | scam_faq | unknown | monthly | https://www.jtexpress.sg/scam-alert |
| Lalamove Singapore | alert_page | unknown | monthly | https://www.lalamove.com/en-sg/2023-rising-phishing-scams |
| Land Transport Authority | alert_page | unknown | monthly | https://onemotoring.lta.gov.sg/content/onemotoring/home.html |
| Land Transport Authority | news_releases | unknown | weekly | https://www.lta.gov.sg/content/ltagov/en/newsroom.html |
| Lazada Singapore | scam_faq | unknown | monthly | https://helpcenter.lazada.sg/s/faq |
| M1 Limited | advisory_feed | unknown | weekly | https://www.m1.com.sg/support/security-announcement |
| M1 Limited | scam_faq | unknown | monthly | https://www.m1.com.sg/support/security-announcement/faq |
| MariBank Singapore Private Limited | advisory_feed | unknown | weekly | https://www.maribank.sg/info/latest-security-alerts |
| MariBank Singapore Private Limited | scam_faq | unknown | monthly | https://www.maribank.sg/security |
| Maybank Singapore Limited | advisory_feed | unknown | daily | https://www.maybank2u.com.sg/en/personal/eservices/security-alerts/online-threats/scams.page |
| Maybank Singapore Limited | scam_faq | unknown | monthly | https://www.maybank2u.com.sg/en/personal/eservices/security-alerts/online-threats/measures-to-protect-you-from |
| Ministry of Digital Development and Information | news_releases | unknown | weekly | https://www.mddi.gov.sg/newsroom/ |
| Ministry of Digital Development and Information | statistics | unknown | monthly | https://www.mddi.gov.sg/other-pages/anti-scam-efforts/ |
| Ministry of Education | scam_faq | unknown | monthly | https://www.moe.gov.sg/scam-alert |
| Ministry of Finance | news_releases | unknown | weekly | https://www.mof.gov.sg/news-resources/newsroom/impersonation-of-a-government-agency-or-company-registrar/ |
| Ministry of Foreign Affairs | alert_page | unknown | monthly | https://www.mfa.gov.sg/newsroom/announcements-and-highlights/advisory-on-fraudulent-activities/ |
| Ministry of Foreign Affairs | news_releases | unknown | weekly | https://www.mfa.gov.sg/newsroom/press-statements-transcripts-and-photos/mfa-spokesmans-comments-in-response-to |
| Ministry of Health | alert_page | unknown | monthly | https://www.moh.gov.sg/ |
| Ministry of Home Affairs | alert_page | unknown | weekly | https://www.mha.gov.sg/media-room/newsroom/advisory-on-fake-websites-impersonating-mha-and-home-team-agencies/ |
| Ministry of Home Affairs | news_releases | unknown | weekly | https://www.mha.gov.sg/media-room/newsroom/ |
| Ministry of Home Affairs | news_releases | unknown | weekly | https://www.mha.gov.sg/media-room/newsroom/number-of-fake-bulk-order-scams-involving-impersonation-of-saf-pers |
| Ministry of Law | alert_page | unknown | weekly | https://www.mlaw.gov.sg/advisory-on-government-officials-impersonation-scams/ |
| Ministry of Law | alert_page | unknown | monthly | https://www.mlaw.gov.sg/advisory-on-scammers-impersonating-officers-from-the-ministry-of-law/ |
| Ministry of Law | alert_page | unknown | monthly | https://www.mlaw.gov.sg/news/announcements/scam-alert-unsolicited-phone-calls-impersonating-minlaw-officers/ |
| Ministry of Law | news_releases | unknown | weekly | https://www.mlaw.gov.sg/ |
| Ministry of Manpower | advisory_feed | unknown | weekly | https://www.mom.gov.sg/newsroom/announcements/2025/2025-scam-alert-impersonation-phone-call |
| Ministry of Manpower | advisory_feed | unknown | weekly | https://www.mom.gov.sg/employment-agencies/employment-agency-publications/ea-alerts |
| Ministry of Manpower | fake_indicator_list | ioc | weekly | https://www.mom.gov.sg/transact-safely-and-securely |
| Ministry of Manpower | scam_faq | unknown | monthly | https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-domestic-worker/publications-and-resources/s |
| Ministry of Social and Family Development | scam_faq | unknown | monthly | https://www.msf.gov.sg/scam-advisory |
| Ministry of Sustainability and the Environment | advisory_feed | unknown | weekly | https://www.mse.gov.sg/latest-news/misuse-of-mse-logo-in-fraudulent-carbon-credit-trading-scam/ |
| Monetary Authority of Singapore | fake_indicator_list | ioc | weekly | https://www.mas.gov.sg/investor-alert-list |
| Monetary Authority of Singapore | news_releases | unknown | weekly | https://www.mas.gov.sg/news?content_type=Media+Releases |
| Monetary Authority of Singapore | scam_faq | unknown | monthly | https://www.mas.gov.sg/scam-advisory-page |
| Monetary Authority of Singapore | scam_faq | unknown | monthly | https://www.mas.gov.sg/regulation/combatting-scams |
| Moomoo Singapore (Moomoo Financial Singapore Pte. Ltd.) | alert_page | unknown | weekly | https://www.moomoo.com/sg/learn/beware-of-phishing-scams |
| Mothership | alert_page | unknown | weekly | https://mothership.sg/2026/08/fake-mothership-rolex-139/ |
| Mothership | alert_page | unknown | monthly | https://mothership.sg/2025/08/fake-mothership-accounts/ |
| NTUC FairPrice | scam_faq | unknown | monthly | https://help.fairprice.com.sg/hc/en-us |
| National Crime Prevention Council | news_releases | unknown | weekly | https://www.ncpc.org.sg/media-releases/ |
| National Crime Prevention Council | scam_faq | unknown | monthly | https://www.ncpc.org.sg/crime-prevention-advisories/individuals/cybercrime/ |
| National Environment Agency | advisory_feed | unknown | weekly | https://t.me/s/NEASingapore?q=scam |
| National Parks Board | alert_page | unknown | monthly | https://www.nparks.gov.sg/noticeboard/phishing-scams |
| National University Health System | scam_faq | unknown | monthly | https://www.nuhs.edu.sg/security-advisory |
| National University Hospital | scam_faq | unknown | monthly | https://www.nuh.com.sg/beware-of-scams-impersonating-nuh |
| Network for Electronic Transfers (Singapore) Pte Ltd | scam_faq | unknown | monthly | https://www.nets.com.sg/policies/security |
| Ninja Van Singapore (Ninja Logistics Pte. Ltd.) | fake_indicator_list | ioc | weekly | https://www.ninjavan.co/en-sg/parcel-scams-advisory |
| OCBC Bank (Oversea-Chinese Banking Corporation) | advisory_feed | unknown | weekly | https://www.ocbc.com/personal-banking/security/security-advisories.page |
| OCBC Bank (Oversea-Chinese Banking Corporation) | scam_faq | unknown | monthly | https://www.ocbc.com/personal-banking/security/secure-banking-ways/phishing-scams.page |
| OCBC Bank (Oversea-Chinese Banking Corporation) | scam_faq | unknown | monthly | https://www.ocbc.com/personal-banking/security/secure-banking-ways/ocbc-killswitch.page |
| POSB (DBS Bank) | advisory_feed | unknown | daily | https://www.posb.com.sg/personal/scam-defence/recent-scams-fraud.page |
| POSB (DBS Bank) | scam_faq | unknown | monthly | https://www.posb.com.sg/personal/scam-defence/default.page |
| People's Association | scam_faq | unknown | monthly | https://www.pa.gov.sg/scam-alert/ |
| Personal Data Protection Commission | alert_page | unknown | monthly | https://www.pdpc.gov.sg/media-events/advisory-on-government-official-impersonation-scams-involving-impersonati |
| Personal Data Protection Commission | alert_page | unknown | monthly | https://www.pdpc.gov.sg/media-events/advisory-on-unsolicited-robocalls |
| Personal Data Protection Commission | scam_faq | unknown | monthly | https://www.pdpc.gov.sg/individuals/resources-tips/protecting-yourself-from-spam-and-scam |
| Phillip Securities Pte Ltd (POEMS by PhillipCapital) | alert_page | unknown | monthly | https://www.poems.com.sg/announcements/security-alert-beware-of-scam-messages/ |
| Phillip Securities Pte Ltd (POEMS by PhillipCapital) | scam_faq | unknown | monthly | https://www.poems.com.sg/education/scam-awareness/ |
| Prudential Assurance Company Singapore | advisory_feed | unknown | weekly | https://www.prudential.com.sg/en/others/prusecurity/ |
| Public Service Division | alert_page | unknown | monthly | https://www.psd.gov.sg/newsroom/public-service-job-openings-reposted-on-unauthorised-job-scam-site/ |
| Registry of Moneylenders (Ministry of Law) | alert_page | unknown | weekly | https://rom.mlaw.gov.sg/advisory-on-scam-calls-impersonating-as-officers-from-the-ministry-of-law-cbs-or-the-m |
| Registry of Moneylenders (Ministry of Law) | alert_page | unknown | weekly | https://rom.mlaw.gov.sg/information-for-moneylenders/reports-of-government-official-impersonation-scam-gois/ |
| SBS Transit Ltd | alert_page | unknown | monthly | https://www.sbstransit.com.sg/ |
| SG Arrival Card (ICA e-Service) | alert_page | unknown | monthly | https://www.ica.gov.sg/about-ica/news-and-publications/media-room/public-advisory-on-fake-sg-arrival-card-webs |
| SG Arrival Card (ICA e-Service) | fake_indicator_list | ioc | daily | https://www.ica.gov.sg/about-ica/news-and-publications/public-advisories/public-advisory-on-the-submission-of- |
| SMS Sender ID Registry (SGNIC, IMDA subsidiary) | scam_faq | unknown | monthly | https://www.sgnic.sg/smsregistry/overview |
| SP Group (Singapore Power) | alert_page | unknown | monthly | https://www.spgroup.com.sg/about-us/media-resources/news-and-media-releases/Advisory-On-Fake-Emails |
| SP Group (Singapore Power) | alert_page | unknown | monthly | https://www.spgroup.com.sg/about-us/media-resources/news-and-media-releases/Recruitment-Scam |
| ScamShield | advisory_feed | unknown | weekly | https://www.scamshield.gov.sg/resources/scam-alert/ |
| ScamShield | report_portal | unknown | monthly | https://www.scamshield.gov.sg/ |
| ScamShield | scam_faq | unknown | monthly | https://www.scamshield.gov.sg/i-want-protection-from-scams/learn-to-recognise-scams/government-officials-imper |
| ScamShield | statistics | unknown | monthly | https://www.scamshield.gov.sg/resources/scam-bulletins/ |
| ScamShield | statistics | unknown | monthly | https://www.scamshield.gov.sg/resources/essr/1h-2026/ |
| Shopee Singapore | alert_page | unknown | monthly | https://help.shopee.sg/portal/4/article/204789-%5BScam-Advisory%5D-Delivery-Impersonation-Scams |
| Shopee Singapore | alert_page | unknown | monthly | https://help.shopee.sg/portal/4/article/125081-%5BScam-Advisory%5D-Marketing-Survey-WhatsApp-Scam-Messages |
| Shopee Singapore | scam_faq | unknown | monthly | https://help.shopee.sg/portal/4/article/76743-%5BScam-Advisory%5D-How-do-I-protect-myself-from-scams |
| Singapore Airlines | advisory_feed | unknown | weekly | https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/ |
| Singapore Airlines | alert_page | unknown | weekly | https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-phishing-scams-and-good |
| Singapore Civil Defence Force | alert_page | unknown | monthly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/individual-posing-as-an |
| Singapore Civil Defence Force | alert_page | unknown | monthly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/Alert-of-companies-atte |
| Singapore Civil Defence Force | alert_page | unknown | monthly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/Alert-on-Unauthorised-B |
| Singapore Civil Defence Force | alert_page | unknown | monthly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/Alert-on-Unauthorised-B |
| Singapore Civil Defence Force | alert_page | unknown | monthly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/Alert-on-Unauthorized-B |
| Singapore Civil Defence Force | alert_page | unknown | monthly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings/newsarticledetail/Alert-on-Unauthorized-B |
| Singapore Civil Defence Force | news_releases | unknown | weekly | https://www.scdf.gov.sg/home/about-scdf/media-room/latest-happenings |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | alert_page | unknown | weekly | https://www.judiciary.gov.sg/news-and-resources/news/news-details/media-advisory--public-alert--scam-involving |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | alert_page | unknown | monthly | https://www.judiciary.gov.sg/news-and-resources/news/news-details/advisory-on-impersonation-scams |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | alert_page | unknown | monthly | https://www.judiciary.gov.sg/news-and-resources/news/news-details/press-release-beware-of-phishing-emails-purp |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | alert_page | unknown | monthly | https://www.judiciary.gov.sg/news-and-resources/news/news-details/press-release-beware-of-scam-calls-and-phish |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | alert_page | unknown | monthly | https://www.judiciary.gov.sg/news-and-resources/news/news-details/advisory-on-scam-calls-and-phishing-emails-f |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | alert_page | unknown | monthly | https://www.judiciary.gov.sg/news-and-resources/news/news-details/advisory-unsolicited-messages-about-court-ma |
| Singapore Courts (Judiciary: Supreme Court, State Courts, Family Justice Courts) | news_releases | unknown | weekly | https://www.judiciary.gov.sg/news-and-resources/news |
| Singapore Customs | advisory_feed | unknown | weekly | https://www.customs.gov.sg/news/beware-of-scams/ |
| Singapore Food Agency | scam_faq | unknown | monthly | https://www.sfa.gov.sg/news-publications/newsroom/before-2024/advisory-on-phishing-scams |
| Singapore General Hospital | fake_indicator_list | ioc | weekly | https://www.sgh.com.sg/patient-services/patient-finance/spot-scam-at-sgh |
| Singapore General Hospital | news_releases | unknown | weekly | https://www.sgh.com.sg/news/patient-care/sgh-nhg-health-warn-of-fake-ads-promoting-health-products |
| Singapore General Hospital | scam_faq | unknown | monthly | https://www.sgh.com.sg/about-sgh/scam-alert |
| Singapore Health Services (SingHealth) | report_portal | unknown | monthly | https://www.singhealth.com.sg/about-singhealth/news/check-fake-news |
| Singapore Life Ltd. (Singlife) | alert_page | unknown | weekly | https://singlife.com/en/singlife-security-advisory |
| Singapore Police Force | advisory_feed | unknown | weekly | https://www.police.gov.sg/media-hub/news |
| Singapore Police Force | alert_page | unknown | weekly | https://www.police.gov.sg/media-hub/news/2026/08/20260808_police_advisory_on_phishing_scams_impersonating_the_ |
| Singapore Police Force | news_releases | unknown | weekly | https://www.police.gov.sg/media-hub/police-life/2021/11/the-anti-scam-centre---a-collaborative-approach-agains |
| Singapore Police Force | report_portal | unknown | monthly | https://www.police.gov.sg/i-witness |
| Singapore Police Force | scam_faq | unknown | monthly | https://www.police.gov.sg/advisories/scams |
| Singapore Police Force | statistics | unknown | monthly | https://www.police.gov.sg/media-hub/statistics |
| Singapore Post Limited (SingPost) | advisory_feed | unknown | daily | https://www.singpost.com/support/service-updates |
| Singapore Prison Service | alert_page | unknown | weekly | https://www.sps.gov.sg/media/advisory-on-fake-websites-impersonating--mha-and-home-team-agencies/ |
| Singapore Prison Service | news_releases | unknown | weekly | https://www.sps.gov.sg/media/ |
| Singapore Telecommunications Limited (Singtel) | advisory_feed | unknown | weekly | https://www.singtel.com/personal/support/scam-advisory |
| Singapore Telecommunications Limited (Singtel) | report_portal | unknown | monthly | https://www.singtel.com/personal/support/scam-advisory/report-scam |
| Singapore Telecommunications Limited (Singtel) | scam_faq | unknown | monthly | https://www.singtel.com/personal/products-services/lifestyle-services/my-smart-network/scamcallprotect |
| Singapore Tourism Board | alert_page | unknown | monthly | https://www.stb.gov.sg/about-stb/media-publications/media-centre/public-advisory-transact-with-licensed-travel |
| Singpass | scam_faq | unknown | monthly | https://www.singpass.gov.sg/security |
| Singtel Dash (SingCash Pte. Ltd.) | report_portal | unknown | monthly | https://dash.com.sg/report-fraud-scam |
| Skills and Workforce Development Agency | fake_indicator_list | ioc | weekly | https://www.swda.gov.sg/home/skills-career-resources/private-education-resources/alerts-and-advisories |
| Standard Chartered Bank (Singapore) Limited | report_portal | unknown | monthly | https://www.sc.com/sg/fraud-scam/help/ |
| Standard Chartered Bank (Singapore) Limited | scam_faq | unknown | monthly | https://www.sc.com/sg/fraud-scam/ |
| StarHub Ltd | news_releases | unknown | weekly | https://corporate.starhub.com/about-us/newsroom/2025/aug/starhub-launches-scamsafe-where-scam-prevention-is-ma |
| StarHub Ltd | scam_faq | unknown | monthly | https://consumer.starhub.com/personal/scamsafe |
| StarHub Ltd | scam_faq | unknown | monthly | https://www.starhub.com/personal/mobile/mobile-phones-plans/value-added-services/blockoverseascalls.html |
| The Association of Banks in Singapore | news_releases | unknown | daily | https://abs.org.sg/newsroom/press-releases |
| The Association of Banks in Singapore | scam_faq | unknown | monthly | https://abs.org.sg/consumer-banking/canny-the-anti-scam-mascot |
| The Association of Banks in Singapore | scam_faq | unknown | monthly | https://abs.org.sg/e-payments/pay-now |
| The Straits Times | alert_page | unknown | monthly | https://www.straitstimes.com/singapore/readers-beware-scammers-using-fake-st-pages-articles-that-depict-promin |
| The Straits Times | news_releases | unknown | weekly | https://www.straitstimes.com/tags/scams |
| The Straits Times | news_releases | unknown | weekly | https://www.straitstimes.com/news/singapore/rss.xml |
| Tiger Brokers (Singapore) Pte. Ltd. | alert_page | unknown | weekly | https://www.itiger.com/sg/fraud-awareness |
| Trust Bank Singapore Limited | scam_faq | unknown | monthly | https://trustbank.sg/srf/ |
| Trust Bank Singapore Limited | scam_faq | unknown | monthly | https://trustbank.sg/security/ |
| Trust Bank Singapore Limited | scam_faq | unknown | monthly | https://trustbank.sg/faqs/security/ |
| UOB Kay Hian Private Limited (Singapore) | alert_page | unknown | weekly | https://uobkh.com.sg/en/announcement/beware-of-impersonation-scam-calls |
| United Overseas Bank (UOB) Singapore | advisory_feed | unknown | weekly | https://www.uob.com.sg/personal/digital-banking/news-and-announcements.page |
| United Overseas Bank (UOB) Singapore | report_portal | unknown | monthly | https://go.uob.com/reportscam |
| United Overseas Bank (UOB) Singapore | scam_faq | unknown | monthly | https://www.uob.com.sg/personal/digital-banking/pib/security/index.page |
| Urban Redevelopment Authority | alert_page | unknown | weekly | https://www.ura.gov.sg/news/media/scam-advisory2026/ |
| gov.sg SMS Sender ID (OGP/GovTech) | report_portal | unknown | monthly | https://www.sms.gov.sg/ |
| uParcel Singapore | alert_page | unknown | weekly | https://www.uparcel.sg/blog/uparcel-scam-alert-how-to-spot-fake-delivery-messages-and-websites |
| uParcel Singapore | scam_faq | unknown | monthly | https://www.uparcel.sg/blog/how-to-avoid-falling-victim-to-cash-on-delivery-cod-scams |
| uSMART Securities (Singapore) Pte. Ltd. | alert_page | unknown | weekly | https://sg.usmartsecurities.com/news/7440654849752055826 |
