# Impersonating-site status (2026-11-27T06:11:39Z)

Sites named in publications of **listing** publishers: **417**; **adjacent** (MAS Investor Alert List): 898.
Checks so far: 2819 ({'P1': 2819}); vantage: direct:gpu25|doh:dns.google; Safe Browsing: OFF (D6) - flag axis from host interstitial + TLS only; signatures v1.4-2026-11-26.

Buckets: **(a) taken down** = not reachable (whatever the flag) · **(b) flagged** = serving behind a bypassable warning · **(c) live** = serving, no warning seen · inconclusive = not decidable from this vantage yet.

## 1. Current state

| | (c) live | (b) flagged | (a) taken down | inconclusive | not yet checked | total |
|---|---|---|---|---|---|---|
| listing | 52 | 4 | 325 | 36 | 0 | 417 |
| adjacent | 130 | 1 | 590 | 177 | 0 | 898 |

Of the listing sites marked inconclusive, **1** are soft takedown signals (NXDOMAIN, dead delegation, no address, bare 404, origin down) waiting for the confirming second check ≥6 h later; they move to (a) if it agrees.

### Reasons (listing sites)

| bucket | reason | n |
|---|---|---|
| (c) live | serving | 47 |
| (c) live | serving_via_redirect | 5 |
| (b) flagged | host_interstitial | 4 |
| (a) taken down | dns_nxdomain | 180 |
| (a) taken down | dns_dead_delegation | 47 |
| (a) taken down | no_address | 38 |
| (a) taken down | registry_hold | 21 |
| (a) taken down | origin_down | 16 |
| (a) taken down | platform_removed | 5 |
| (a) taken down | parked_or_for_sale | 4 |
| (a) taken down | registration_lapsed | 4 |
| (a) taken down | sinkhole_ip | 3 |
| (a) taken down | http_gone | 3 |
| (a) taken down | seized | 2 |
| (a) taken down | connection_refused | 1 |
| (a) taken down | server_default_page | 1 |
| inconclusive | timeout | 10 |
| inconclusive | tls_handshake_failed | 8 |
| inconclusive | geo_or_ip_block | 7 |
| inconclusive | bot_challenge | 5 |
| inconclusive | dns_error_at_proxy | 1 |
| inconclusive | connect_failed | 1 |
| inconclusive | redirect_loop | 1 |
| inconclusive | no_address_unconfirmed | 1 |
| inconclusive | empty_response | 1 |
| inconclusive | dns_servfail | 1 |

## 2. By publisher (listing)

| publisher | sites | (c) live | (b) flagged | (a) taken down | inconclusive |
|---|---|---|---|---|---|
| police.gov.sg | 338 | 19 | 4 | 289 | 26 |
| ica.gov.sg#sg-arrival-card | 62 | 32 | 0 | 21 | 9 |
| mom.gov.sg | 7 | 0 | 0 | 6 | 1 |
| ica.gov.sg | 2 | 0 | 0 | 2 | 0 |
| ninjavan.co | 2 | 0 | 0 | 2 | 0 |
| prudential.com.sg | 2 | 0 | 0 | 2 | 0 |
| psd.gov.sg | 1 | 0 | 0 | 1 | 0 |
| enterprisesg.gov.sg | 1 | 0 | 0 | 1 | 0 |
| swda.gov.sg | 1 | 1 | 0 | 0 | 0 |
| sgh.com.sg | 1 | 0 | 0 | 1 | 0 |
| scamshield.gov.sg | 1 | 0 | 0 | 1 | 0 |

## 3. By impersonated target (listing, top 30)

| target | kind | sites | live | flagged | taken down | authentic hosts |
|---|---|---|---|---|---|---|
| — none — (`None`) | fictitious/unresolved | 94 | 9 | 0 | 80 |  |
| SG Arrival Card (ICA e-Service) (`ica.gov.sg#sg-arrival-card`) | clone | 61 | 33 | 0 | 19 | ica.gov.sg, eservices.ica.gov.sg, www.ica.gov.sg |
| Land Transport Authority (`lta.gov.sg`) | brand_abuse/clone | 29 | 0 | 0 | 28 | lta.gov.sg, datamall.lta.gov.sg, onemotoring.lta.gov.sg |
| Ninja Van Singapore (Ninja Logistics Pte. Ltd.) (`ninjavan.co`) | clone | 15 | 0 | 0 | 15 | ninjavan.co, dashboard.ninjavan.co, delivery.ninjavan.co |
| CNA (Channel NewsAsia) (`channelnewsasia.com`) | brand_abuse | 14 | 0 | 0 | 13 | channelnewsasia.com, www.channelnewsasia.com |
| WhatsApp (`whatsapp.com`) | brand_abuse/clone | 14 | 0 | 0 | 13 | wa.me, whatsapp.com |
| TikTok (`tiktok.com`) | brand_abuse | 12 | 0 | 1 | 10 | tiktok.com |
| UnionPay (`unionpayintl.com`) | clone | 10 | 0 | 0 | 9 | unionpay.com, unionpayintl.com |
| Park N Parcel (ParkNParcel) (`parknparcel.com.sg`) | clone | 8 | 0 | 1 | 7 | parknparcel.com, parknparcel.com.sg, tracking.parknparcel.com |
| DBS Bank (Singapore) (`dbs.com.sg`) | clone | 7 | 1 | 0 | 2 | dbs.com, dbs.com.cn, dbs.com.hk |
| Ministry of Manpower (`mom.gov.sg`) | clone | 7 | 0 | 0 | 6 | mom.gov.sg, services.mom.gov.sg, wponline.mom.gov.sg |
| Singapore Post Limited (SingPost) (`singpost.com`) | clone | 6 | 0 | 0 | 5 | ezy2ship.net, ezyparcels.com, mysam.sg |
| CDC Vouchers Scheme (`cdc.gov.sg#cdc-vouchers`) | clone | 5 | 0 | 0 | 5 | cdc.gov.sg, redeem.gov.sg, go.gov.sg |
| Singapore Police Force (`police.gov.sg`) | clone | 5 | 0 | 0 | 2 | police.gov.sg, eservices.police.gov.sg, www.police.gov.sg |
| Moomoo Singapore (Moomoo Financial Singapore Pte. Ltd.) (`moomoo.com`) | clone | 4 | 0 | 0 | 4 | moomoo.com, invest.sg.moomoo.com, openaccount.sg.moomoo.com |
| B2B Wave (`b2bwave.com`) | brand_abuse | 4 | 1 | 0 | 3 | b2bwave.com |
| Inland Revenue Authority of Singapore (`iras.gov.sg`) | clone | 4 | 0 | 0 | 3 | iras.gov.sg, mytax.iras.gov.sg, www.iras.gov.sg |
| MoneySmart Singapore (`moneysmart.sg`) | clone | 4 | 0 | 0 | 4 | moneysmart.sg |
| Singapore Telecommunications Limited (Singtel) (`singtel.com`) | clone | 4 | 0 | 0 | 4 | dash.com.sg, gomo.sg, singtel.com |
| uSMART (`usmart.sg`) | brand_abuse | 3 | 0 | 0 | 3 | usmart.sg |
| BeReal (`bereal.com`) | brand_abuse | 3 | 0 | 0 | 3 | bereal.com |
| QUALCOMM invest (`qualcomm.com`) | brand_abuse | 3 | 0 | 0 | 3 | qualcomm.com |
| Immigration & Checkpoints Authority (`ica.gov.sg`) | clone | 3 | 0 | 0 | 2 | ica.gov.sg, vica.gov.sg, eservices.ica.gov.sg |
| Lalamove Singapore (`lalamove.com`) | clone | 3 | 0 | 0 | 3 | lalamove.co.uk, lalamove.com, lalamove.eu |
| LG (`lg.com`) | brand_abuse | 3 | 0 | 0 | 3 | lg.com |
| NVIDIA (`nvidia.com`) | brand_abuse | 3 | 0 | 0 | 2 | nvidia.com |
| Booking.com (`booking.com`) | clone | 3 | 0 | 0 | 3 | booking.com |
| Skild AI (`skild.ai`) | brand_abuse | 3 | 1 | 0 | 2 | skild.ai |
| USDT Tether (`tether.to`) | brand_abuse | 2 | 0 | 0 | 2 | tether.to |
| MalaysiaArrivalCard (`imi.gov.my#mdac`) | clone | 2 | 1 | 0 | 1 | imi.gov.my, imigresen-online.imi.gov.my |

## 4. Target resolution

Kinds: {'brand_abuse': 97, 'fictitious': 38, 'clone': 226, 'unresolved': 56}  
Methods: {'report_tag': 218, 'none': 94, 'publisher_self': 71, 'lookalike+tag': 25, 'lookalike': 9}

### Review queue: unresolved targets (56)

| site | candidate brands | publication |
|---|---|---|
| `2xtron[.]online` | - | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-on-2xtron-online-fdfddd5e |
| `356739[.]org` | brand:airdrop-pepe, channelnewsasia.com, rolex.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-b5974029 |
| `85shouyou[.]com` | - | https://www.police.gov.sg/media-hub/news/2021/09/20210928_scammers_targeting_game_accs_sellers_w_fake_e-wallet_websites |
| `aloilvip[.]shop` | alvopetro.com, hochschildmining.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-legitimate-companies-04a4a367 |
| `autonomo-income[.]com` | alvopetro.com, hochschildmining.com, income.com.sg | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-legitimate-companies-04a4a367 |
| `baobeiwa[.]bond` | barrick.com, marriott.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-reputable-brands-31f06e15 |
| `baowushouyou[.]com` | - | https://www.police.gov.sg/media-hub/news/2021/09/20210928_scammers_targeting_game_accs_sellers_w_fake_e-wallet_websites |
| `behene[.]com` | - | https://www.icanactagainstscams.gov.sg/scam-trends/fake-online-shopping-deals-e-commerce-scams-563a08b7 |
| `bestcarspage[.]com` | - | https://www.police.gov.sg/media-hub/news/2025/09/20250911_police_advisory_on_phishing_scams_perpetuated_via_social_media_platforms |
| `bianjieshouyou[.]com` | - | https://www.police.gov.sg/media-hub/news/2021/09/20210928_scammers_targeting_game_accs_sellers_w_fake_e-wallet_websites |
| `bigbuy[.]rest` | b2bwave.com, bizvibe.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-online-job-scams-impersonating-b2b-wave-and-other-bf2a0de7 |
| `case-apple[.]com` | - | https://www.police.gov.sg/media-hub/news/2026/08/20260821_police_advisory_on_apple_impersonation_cryptocurrency_account_compromise_scams |
| `chat-apple[.]com` | - | https://www.police.gov.sg/media-hub/news/2026/08/20260821_police_advisory_on_apple_impersonation_cryptocurrency_account_compromise_scams |
| `costarica-homeschool[.]com` | - | https://www.police.gov.sg/media-hub/news/2025/09/20250911_police_advisory_on_phishing_scams_perpetuated_via_social_media_platforms |
| `ctxpublic[.]online` | brand:doge-mining, brand:gn-mall, brand:pump-mining, coinbase.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-scams-promising-high-returns-4e5d1698 |
| `diwkr[.]com` | facebook.com, motor-ai.com | https://www.icanactagainstscams.gov.sg/scam-trends/rising-job-scams-9b5a348c |
| `domino-plza[.]com` | - | https://www.police.gov.sg/media-hub/news/2023/12/20231216_police_advisory_on_phishing_scams_involving_fake_dominos_pizza_websites |
| `e-station-axs[.]com` | - | https://www.police.gov.sg/media-hub/news/2025/05/20250505_police_advisory_on_phishing_scams_involving_fake_axs_websites |
| `ebayhot[.]com` | b2bwave.com, bizvibe.com | https://www.icanactagainstscams.gov.sg/scam-trends/job-scam-alert-be-cautious-of-suspicious-online-job-offers-a56c929e |
| `estation-axs[.]com` | - | https://www.police.gov.sg/media-hub/news/2025/05/20250505_police_advisory_on_phishing_scams_involving_fake_axs_websites |
| `gardes-holdenjp[.]com` | - | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-scams-impersonating-hotel-reservation-services-62503fcc |
| `herb6[.]vip` | brand:pump-mining, coinbase.com, novartis.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-websites-impersonating-popular-brands-6335bfca |
| `ifreelance4u[.]com` | dbs.com.sg, uob.com.sg | https://www.icanactagainstscams.gov.sg/scam-trends/fake-banking-websites-impersonating-dbs-and-uob-17e317a7 |
| `ite-pm-event[.]netlify[.]app` | - | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-websites-impersonating-events-f413d34c |
| `long-termprojects[.]us` | cnpc.com.cn, virtu.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-promising-high-returns-522e3e03 |
| `marrioot[.]net` | barrick.com, marriott.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-reputable-brands-31f06e15 |
| `mineverse[.]cc` | - | https://www.icanactagainstscams.gov.sg/scam-trends/suspicious-online-investment-platforms-like-mineverse-cc-042e6b7d |
| `moomoes[.]top` | itiger.com, moomoo.com | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-scams-impersonating-moomoo-and-tiger-brokers-b433ddc2 |
| `motorai[.]net` | facebook.com, motor-ai.com | https://www.icanactagainstscams.gov.sg/scam-trends/rising-job-scams-9b5a348c |
| `mprmspus[.]top` | dewa.gov.ae, televizo.net | https://www.icanactagainstscams.gov.sg/scam-trends/emerging-online-investment-scams-355047ed |
| `oinbase-staking[.]com` | brand:pump-mining, coinbase.com, novartis.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-websites-impersonating-popular-brands-6335bfca |
| `pepemining[.]cc` | bereal.com, brand:airdrop-pepe, brand:ldnbit, channelnewsasia.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-b5974029 |
| `pumpmining[.]top` | brand:pump-mining, coinbase.com, novartis.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-investment-websites-impersonating-popular-brands-6335bfca |
| `resend-clicks-a[.]com` | dbs.com.sg, uob.com.sg | https://www.icanactagainstscams.gov.sg/scam-trends/fake-banking-websites-impersonating-dbs-and-uob-17e317a7 |
| `servicesmetalinkion[.]shop` | irunsg.com, singtel.com | https://www.icanactagainstscams.gov.sg/scam-trends/recent-phishing-scams-impersonate-popular-brands-stay-e8009338 |
| `sgpools[.]app` | - | https://www.police.gov.sg/media-hub/news/2021/08/20210825_police_advisory_fake_singapore_pools_websites_and_mobile_applications |
| `sgpools[.]online` | - | https://www.police.gov.sg/media-hub/news/2021/08/20210825_police_advisory_fake_singapore_pools_websites_and_mobile_applications |
| `sigmatheta[.]org` | - | https://www.police.gov.sg/media-hub/news/2025/09/20250911_police_advisory_on_phishing_scams_perpetuated_via_social_media_platforms |
| `singapore-arrival-card[.]com` | - | https://www.ica.gov.sg/about-ica/news-and-publications/public-advisories/public-advisory-on-the-submission-of-sg-arrival-card-(sgac) |
| `spaceiseven[.]com` | - | https://www.icanactagainstscams.gov.sg/scam-trends/job-scam-alert-impersonation-of-space-seven-76d17ff4 |
| `spacesevenag[.]com` | - | https://www.icanactagainstscams.gov.sg/scam-trends/job-scam-alert-impersonation-of-space-seven-76d17ff4 |
| `themostprofitableapp[.]us` | cnpc.com.cn, virtu.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-promising-high-returns-522e3e03 |
| `tiktokvipshops[.]com` | b2bwave.com, bizvibe.com | https://www.icanactagainstscams.gov.sg/scam-trends/job-scam-alert-be-cautious-of-suspicious-online-job-offers-a56c929e |
| `utrade1sg[.]top` | dbs.com.sg, uob.com.sg, uobkh.com.sg | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-scams-impersonating-dbs-and-uob-dc0515b7 |
| `utradetsg1[.]top` | dbs.com.sg, uob.com.sg, uobkh.com.sg | https://www.icanactagainstscams.gov.sg/scam-trends/fake-banking-websites-impersonating-dbs-and-uob-17e317a7 |
| `vanguardetfs[.]xyz` | channelnewsasia.com, vanguard.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-cna-investment-schemes-f4e465b3 |
| `volleyport[.]life` | channelnewsasia.com, vanguard.com | https://www.icanactagainstscams.gov.sg/scam-trends/fake-cna-investment-schemes-f4e465b3 |
| `xinyushouyou[.]com` | - | https://www.police.gov.sg/media-hub/news/2021/09/20210928_scammers_targeting_game_accs_sellers_w_fake_e-wallet_websites |
| `yyujgg[.]vip` | dewa.gov.ae, televizo.net | https://www.icanactagainstscams.gov.sg/scam-trends/emerging-online-investment-scams-355047ed |
| `zentraiai[.]top` | - | https://www.icanactagainstscams.gov.sg/scam-trends/fake-zentrixu-investment-sites-6c52592b |
| `zhaitwfo[.]com` | - | https://www.icanactagainstscams.gov.sg/scam-trends/fake-online-shopping-deals-e-commerce-scams-563a08b7 |
| `zylanto[.]site` | brand:airdrop-pepe, channelnewsasia.com, rolex.com | https://www.icanactagainstscams.gov.sg/scam-trends/investment-scams-impersonating-brands-b5974029 |
| `e-payments[.]axs-online[.]icu` | - | https://www.police.gov.sg/media-hub/news/2025/08/20250805_police_advisory_on_resurgence_of_search_engine_phishing_cases_impersonating_axs |
| `internet-dbs[.]oysterartgalleries[.]com` | dbs.com.sg, ocbc.com, uob.com.sg | https://www.icanactagainstscams.gov.sg/scam-trends/phishing-scams-impersonating-dbs-and-uob-dc0515b7 |
| `m1cr0soft[.]1234[.]com[.]co` | - | https://www.scamshield.gov.sg/i-want-protection-from-scams/learn-to-recognise-scams/phishing-scams/ |
| `order[.]domino[.]piza[.]com` | - | https://www.police.gov.sg/media-hub/news/2023/12/20231216_police_advisory_on_phishing_scams_involving_fake_dominos_pizza_websites |

## 5. Reachable now: live + flagged (56)

| site (defanged) | bucket | reason | target | first published | listed by |
|---|---|---|---|---|---|
| `globaltop[.]org` | flagged | host_interstitial | TikTok | 2026-11-23 | police.gov.sg |
| `lt-moburstmobile[.]pages[.]dev` | flagged | host_interstitial | moburst | 2026-11-17 | police.gov.sg |
| `parcel-d[.]top` | flagged | host_interstitial | Park N Parcel (ParkNParcel) | 2026-11-09 | police.gov.sg |
| `polyclinic-a[.]top` | flagged | host_interstitial | Singapore Health Services (SingHealth) | 2026-11-09 | police.gov.sg |
| `digitalarrivalform[.]com` | live | serving | SG Arrival Card (ICA e-Service) | 2026-10-30 | police.gov.sg |
| `managelist[.]com` | live | serving | Central Provident Fund Board | 2026-10-13 | police.gov.sg |
| `qntai[.]top` | live | serving | QNT | 2026-10-07 | police.gov.sg |
| `behene[.]com` | live | serving | unresolved | 2026-09-22 | police.gov.sg |
| `go-mining66[.]top` | live | serving | GoMining | 2026-06-24 | police.gov.sg |
| `dji8[.]top` | live | serving | DJI | 2026-06-12 | police.gov.sg |
| `thaitouristvisa[.]com` | live | serving | fictitious | 2026-04-22 | police.gov.sg |
| `expresszfundings[.]com` | live | serving | fictitious | 2026-04-17 | police.gov.sg |
| `cmpaus[.]com[.]au` | live | serving | DBS Bank (Singapore) | 2026-04-16 | police.gov.sg |
| `sell[.]sctt[.]net` | live | serving_via_redirect | Chan Brothers Travel | 2026-03-24 | police.gov.sg |
| `usttt[.]net` | live | serving | Skild AI | 2026-03-18 | police.gov.sg |
| `hotorders[.]org` | live | serving | fictitious | 2026-03-04 | police.gov.sg |
| `velotrust-exchanges[.]com` | live | serving | fictitious | 2026-03-04 | police.gov.sg |
| `earrivalform[.]com` | live | serving | MalaysiaArrivalCard | 2025-12-19 | police.gov.sg |
| `lieshou[.]vip` | live | serving | fictitious | 2025-10-08 | police.gov.sg |
| `bigbuyshops[.]org` | live | serving | B2B Wave | 2025-09-08 | police.gov.sg |
| `bestcarspage[.]com` | live | serving | unresolved |  | police.gov.sg |
| `enjoy-singaporetourism[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `enjoysingapore-pass[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `govisitsingapore[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `mysgarrivalcard[.]sg` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sbs-online[.]world` | live | serving | Skills and Workforce Development Agency |  | swda.gov.sg |
| `sg-arrivalcard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sg-go[.]tw` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sg-travelpass[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sg-visit[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sg-visitpass[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sgarrivalcard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sgarrivalonline[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sgentrycard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `sgpools[.]app` | live | serving | unresolved |  | police.gov.sg |
| `sgpools[.]online` | live | serving_via_redirect | unresolved |  | police.gov.sg |
| `sgtourism-pass[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singapore-arrivalcard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singapore-evisa[.]com` | live | serving_via_redirect | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singapore-tourisminfo[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singapore-visitcard[.]com` | live | serving_via_redirect | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singaporearrivalcard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singaporetravelcard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singaporevisitcard[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `travelaround-singapore[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `travelonline-singapore[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `travelsmarttravelfast[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `visitpass-sg[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `application[.]singaporevisa[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singapore-arrivalcard[.]visasyst[.]com` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `singapore[.]visatravel[.]jp` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `hxxp://globalsingapore[.]sg/visa-to-singapore/singapore-arrival-card` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `hxxp://ivisa[.]com/singapore-electronic-arrival-card` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `hxxp://natvisa[.]com/singapore-visa` | live | serving_via_redirect | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `hxxp://singap-arrival-card[.]com/index[` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |
| `hxxp://visagov[.]com/en/sgp-visa-for-singapore` | live | serving | SG Arrival Card (ICA e-Service) |  | ica.gov.sg#sg-arrival-card |

## 6. Site events emitted

site.flagged: 11, site.listed: 1316, site.live: 192, site.taken_down: 936, site.target_changed: 8

