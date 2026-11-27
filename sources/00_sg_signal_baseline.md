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
