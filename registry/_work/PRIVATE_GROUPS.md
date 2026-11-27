## Registry: SG local banks + ABS

You are sub-agent A of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_A_banks_local.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/A/

YOUR ENTITIES (all Tier 1 = deep):
1. DBS Bank / POSB, incl. digibank, PayLah!, DBS digital token. SPF brand-tag strings to put in aliases: "DBS", "DBS PayLah". Start points: https://www.dbs.com.sg/personal/scam-defence/recent-scams-fraud.page (earlier survey: 13 dated alerts, newest "SMS Phishing Alert" 2026-08-28; re-verify), the "Scams & Frauds Alert Archives" page, the scam-defence hub, and any page on verifying official DBS/POSB channels (SMS sender IDs / short codes, official websites, official apps, hotlines incl. the anti-scam hotline). Note dbs.com.sg robots.txt has ~1000 Disallow lines and no Sitemap line (try /sitemap.xml once). POSB (posb.com.sg): separate child record (parent dbs.com.sg) ONLY if POSB has its own scam/security pages; otherwise alias + include posb.com.sg in DBS official_domains if confirmed. Look for dbs.com (group) and any other SG-used domains confirmed on DBS pages.
2. OCBC Bank (ocbc.com; check whether ocbc.com.sg is used). Start: https://www.ocbc.com/personal-banking/security/security-advisories.page (earlier: dozens of dated editions, latest 2025-06-12; re-check), official SMS sender IDs, anti-scam hotline, OCBC app names, Money Lock / kill switch pages, "Be A Pro Against Cons". (Context only: ScamShield posted an alert on 2026-11-20 about fake "OCBC card suspended" SMSes.)
3. UOB (uob.com.sg; uobgroup.com). Start: https://www.uob.com.sg/personal/digital-banking/news-and-announcements.page, security/anti-scam pages, official SMS sender ID(s), UOB TMRW app, go.uob.com/reportscam (report portal). SPF brand-tag string: "UOB".
4. The Association of Banks in Singapore (abs.org.sg): anti-scam/consumer-protection pages, PayNow consumer page, scam-related media releases, any lists of bank hotlines/official channels. sector "other" (industry association; note it owns the PayNow scheme). Optional programme record `abs.org.sg#paynow` (sector "payments") only if PayNow has dedicated scam/security content.

Cross-check bank hotlines against ScamShield's page https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ (gov page; you may add it to evidence as corroboration, but each bank's own page must be the primary evidence).

Give these the depth they deserve (they are the most-impersonated SG brands), but stay within the brief's request budget. When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

## Registry: other SG banks

You are sub-agent B of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_B_banks_other.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/B/

YOUR ENTITIES
Tier 1 (deep): for each find security/fraud hub, latest scam alerts (dated list?), official SMS sender IDs, anti-scam/fraud hotline, official apps, official domains/login hosts, social accounts.
1. Citibank Singapore (citibank.com.sg)
2. HSBC Singapore (hsbc.com.sg)
3. Standard Chartered Singapore (SG pages under sc.com/sg -> entity_id "sc.com"; check whether any separate SG registrable domains are used)
4. Maybank Singapore (verify the primary SG domain: maybank2u.com.sg and/or maybank.com.sg)
5. Trust Bank Singapore (verify domain, e.g. trustbank.sg)
6. GXS Bank (verify, e.g. gxs.com.sg)
7. MariBank Singapore (verify domain)
Tier 2 (quick, at most 3, pick ones with SG security/scam pages): CIMB Singapore (cimb.com.sg), Bank of China Singapore, ICBC Singapore, RHB Singapore, HL Bank, YouTrip, Atome.

Cross-check bank hotlines against ScamShield's page https://www.scamshield.gov.sg/bank-s-anti-scam-hotline/ (gov page; may be added to evidence as corroboration; each bank's own page must be primary evidence).

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

## Registry: SG telcos

You are sub-agent C of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_C_telco.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/C/

YOUR ENTITIES
Tier 1 (deep):
1. Singtel (singtel.com). SPF brand-tag string: "Singtel". Start: https://www.singtel.com/personal/support/scam-advisory - the earlier survey found a "List of official Singtel web domains" (all *.singtel.com plus ~45 other domains/hosts, e.g. singtelcrm.com, singteltvgo.com, portal.singtelge.com, gomo.sg, heya.sg, dash.com.sg, gxs.com.sg, e-station2.axs.com.sg, singtelcares.syd1.qualtrics.com) inside a JSON component blob in that page's HTML. Extract the FULL list from the page (embedded page data is fine), apply the brief's third-party rule (Singtel-owned registrable domains -> official_domains; partner/third-party hosts -> exact FQDN in official_hosts; explain in notes). Also capture Singtel sender IDs, hotlines, scam alerts list (dated?), and any fake-indicator examples. Singtel Dash (dash.com.sg): separate child record only if it has its own scam/security pages, else alias.
2. StarHub (starhub.com): scam advisories, ScamSafe (Whoscall-powered), sender IDs, hotlines.
3. M1 (m1.com.sg): earlier survey says the M1 scam page sits behind Radware bot manager. Try once per the brief's bot rule; record the block if so, and fill what you can from M1 pages that do load.
4. SIMBA Telecom (formerly TPG Telecom SG; verify domain, e.g. simba.sg)
5. Circles.Life (verify primary domain, e.g. circles.life)
Tier 2 (quick, at most 3): MyRepublic SG, giga! (StarHub), GOMO (Singtel), Zero1, VIVIFI, redONE SG. Sub-brands get their own record only if they have their own scam pages; otherwise put them in the parent's aliases.
Also record telco pages explaining SSIR "Likely-SCAM" SMS labelling, +65 international-call prefix, ScamShield, or scam-call blocking, as scam_faq entries.

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

## Registry: SG logistics/delivery

You are sub-agent D of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_D_logistics.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/D/

YOUR ENTITIES (delivery-scam brands; SPF advisories impersonate several of them)
Tier 1:
1. SingPost (singpost.com). SPF brand-tag string: "SingPost". Start: https://www.singpost.com/online-security-you (earlier survey: dated 2022-02-28; official domain singpost.com; look-alike examples www.singpost.com.xyz.com, www.singpost.net, www.singpost.org; sender IDs SGPOST/SINGPOST) - re-verify, and look for newer scam notices (tracking-page banners, newsroom, FAQ).
2. Ninja Van Singapore (verify domain, e.g. ninjavan.co with /en-sg). SPF brand-tag string: "Ninjavan".
3. SPX Express Singapore (verify domain, e.g. spx.sg). SPF brand-tag string: "SPX".
4. J&T Express Singapore (verify domain, e.g. jtexpress.sg)
5. Qxpress Singapore (verify domain)
6. DHL Singapore (SG pages under dhl.com/sg-en -> entity_id "dhl.com"; DHL has fraud-awareness pages - record the SG version and any official-domain statements)
7. Lalamove Singapore (SG pages under lalamove.com -> entity_id "lalamove.com"; verify). SPF brand-tag string: "Lalamove".
8. Park N Parcel (verify domain). SPF brand-tag string: "Park N Parcel".
9. uParcel (verify domain, e.g. uparcel.sg). SPF brand-tag string: "uParcel".
Tier 2 (quick, at most 2, only if they have SG scam pages): Pickupp SG, FedEx SG (fedex.com/en-sg), UPS SG, Aramex SG.

For delivery brands, look specifically for: "we will never ask you to pay via SMS link" statements, official tracking hosts, official SMS sender IDs, official WhatsApp numbers, and any listed fake websites/numbers.

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

## Registry: SG ecommerce/retail

You are sub-agent E of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_E_ecommerce_retail.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/E/

YOUR ENTITIES
Tier 1:
1. Shopee Singapore (shopee.sg; help.shopee.sg). SPF brand-tag string: "Shopee". Earlier survey: "[Scam Advisory]" help-centre article series (article IDs 76743, 76788, 76790, 76811, 125081, 166953, 204789); official email only @shopee.com; no dates/IOCs. The help centre is an SPA: read article pages via WebFetch if curl gets only a shell; do NOT call its JSON API. Sector "ecommerce" (or "marketplace" - pick one and be consistent).
2. Lazada Singapore (lazada.sg; help centre / scam-awareness pages)
3. Carousell (carousell.sg / carousell.com). SPF brand-tag string: "Carousell". Earlier: the help centre returned 403 to non-browser clients; search snippets said only carousell.com/carousell.sg are genuine and gave fake examples carousellpay.com, carousell-pay.com, carousell.pay-sg.com - re-verify by opening the official page (one WebFetch attempt allowed if curl is blocked); if you cannot open it, keep those fakes only in notes labelled "unverified (search snippet)".
4. Qoo10 Singapore (qoo10.sg)
5. Amazon.sg (amazon.sg): SG help pages on scams/impersonation; global amazon.com equivalents go in notes only.
6. NTUC FairPrice (fairprice.com.sg) and NTUC Link / Linkpoints (verify domain, e.g. link.sg). Use NTUC Enterprise as parent_entity_id only if its domain is confirmed. SPF brand-tag string: "NTUC FairPrice".
Tier 2 (quick, at most 3): CapitaLand (capitaland.com; SPF brand-tag string "Capitaland"; CapitaStar / eCapitaVoucher scam notices), Courts SG, Harvey Norman SG, Sheng Siong, Klook.

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

## Registry: SG transport/payments/utility

You are sub-agent F of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_F_transport_pay_util.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/F/

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

## Registry: SG travel + brokers

You are sub-agent G1 of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_G1_travel_brokers.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/G1/

YOUR ENTITIES
Tier 1:
1. Singapore Airlines (singaporeair.com): fraud/phishing notices (fake websites, emails, social-media giveaways, fake KrisFlyer), official channels. Scoot (flyscoot.com) as a quick child record only if it has its own scam/fraud page, else alias.
2. Changi Airport Group (changiairport.com; check changiairportgroup.com): scam notices (e.g. fake Changi giveaway/lost-luggage pages), official channels.
3. moomoo Singapore (verify SG domain/path, e.g. moomoo.com/sg). SPF brand-tag string: "MooMoo". Look for anti-fraud pages listing official channels, fake apps/groups.
4. Tiger Brokers Singapore (tigerbrokers.com.sg; check itiger.com). SPF brand-tag string: "Tiger Brokers".
5. UOB Kay Hian (uobkayhian.com; UTRADE). SPF brand-tag string: "UOB Kay Hian". (A fake domain uobkhs.com appeared in an SPF advisory - never visit it.)
6. Phillip Securities / POEMS (poems.com.sg; phillip.com.sg).
Brokers often publish lists of fake websites/apps/WhatsApp-Telegram groups impersonating them - capture counts, dates and samples (as text; never visit them).
Tier 2 (quick, at most 4): uSMART Securities Singapore (SPF brand-tag string "uSMART"; CAUTION: `usmartsg.sg` was listed by SPF as a SCAM domain - do not visit; confirm the real domain from official pages or the MAS Financial Institutions Directory), MoneySmart (moneysmart.sg; SPF brand-tag string "MoneySmart"; fake domains money-sm.art, moneysmart.money, moneysmart.click, moneysmart.one - do not visit), Chan Brothers Travel (SPF brand-tag string "Chan Brothers"), FSMOne/iFAST, Webull SG, Syfe/Endowus/StashAway.

When done, validate with the brief's validate.py and hand back per the brief (<=250 words).

## Registry: SG insurers + media

You are sub-agent G2 of a Singapore private-sector entity-registry task (scam-intelligence pipeline). FIRST run `cat /home/ankur/scamtrends_feed/registry/_work/<your folder>/BRIEF.md` and follow it EXACTLY (it tells you to read /home/ankur/scamtrends_feed/registry/FORMAT.md too). It contains the output format, field rules, ground rules (never visit scam domains; no undocumented APIs; no bot-protection bypass; light volume) and the hand-back format.

Output file: /home/ankur/scamtrends_feed/registry/_work/<your folder>/out_G2_insurance_media.json
Scratch folder for raw downloads: /home/ankur/scamtrends_feed/registry/_work/<your folder>/G2/

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
