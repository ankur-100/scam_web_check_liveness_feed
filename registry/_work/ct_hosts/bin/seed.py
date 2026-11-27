#!/usr/bin/env python3
"""Manual host classification -> data/seed.json (consumed by build_hosts.py).
Each row: host, registrable_domain, discovered_via, scam_relevant, owner_entity_id, notes.
Trusted-sites rows are appended from data/web/trusted_rows.json."""
import json, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def R(host, reg, via, rel, owner, notes=""):
    return {"host": host, "registrable_domain": reg, "discovered_via": via,
            "scam_relevant": rel, "owner_entity_id": owner, "notes": notes}

TS = "also on gov.sg Trusted Sites list"
rows = [
 # ---------------- scamshield.gov.sg (full CT set) ----------------
 R("www.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "yes", "scamshield.gov.sg",
   "ScamShield one-stop anti-scam portal (SPF+NCPC+OGP): /resources/scam-alert/, /check-for-scams/, anti-scam resource guide, bank anti-scam hotlines; " + TS + " (Table 1)"),
 R("scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "yes", "scamshield.gov.sg",
   "apex of ScamShield portal; wildcard *.scamshield.gov.sg certs 2020-05-19..2026-07-23 (crt.sh)"),
 R("guide.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "yes", "scamshield.gov.sg",
   "ScamShield user guide (search-indexed /llms-full.txt)"),
 R("wa-bot.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "maybe", "scamshield.gov.sg",
   "name suggests ScamShield WhatsApp bot endpoint (backend, not public content; no GET)"),
 R("dashboard.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "maybe", "scamshield.gov.sg",
   "ScamShield dashboard (search snippet: admin dashboard used by police to verify reports); login app, no GET"),
 R("dashboardguide.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "maybe", "scamshield.gov.sg",
   "guide for the ScamShield dashboard"),
 R("dashboard-staging.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "no", "scamshield.gov.sg", "staging environment; no GET"),
 R("dashboard-vapt.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "no", "scamshield.gov.sg", "VAPT (pen-test) environment; no GET"),
 R("status.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "no", "scamshield.gov.sg", "service status page"),
 R("grafana-new.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "no", "scamshield.gov.sg", "internal monitoring; no GET"),
 R("app.beta.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "maybe", "scamshield.gov.sg", "beta web app; certs stop 2026-01"),
 R("app-beta.scamshield.gov.sg", "scamshield.gov.sg", "crt.sh", "maybe", "scamshield.gov.sg", "beta web app; only certs Feb-Mar 2024"),
 # ---------------- scamshield.org.sg / scamshield.sg (legacy ScamShield domains) ----------------
 R("www.scamshield.org.sg", "scamshield.org.sg", "crt.sh", "yes", "scamshield.gov.sg",
   "ScamShield Bot microsite (/about-bot, /bot-faqs, /set-up-bot per search); 01_sg_official.md: 302 -> www.scamshield.gov.sg"),
 R("scamshield.org.sg", "scamshield.org.sg", "crt.sh", "yes", "scamshield.gov.sg",
   "apex of ScamShield Bot microsite; wildcard *.scamshield.org.sg certs to 2026-09"),
 R("scamshield.sg", "scamshield.sg", "crt.sh", "maybe", "scamshield.gov.sg",
   "2020-era ScamShield app address (search: Nov-2020 Mothership article pointed to scamshield.sg; app built by OGP for NCPC); Cloudflare/LE certs to 2026-08"),
 R("www.scamshield.sg", "scamshield.sg", "crt.sh", "maybe", "scamshield.gov.sg", "legacy ScamShield app site; certs stop 2024-08"),
 R("api.scamshield.sg", "scamshield.sg", "crt.sh", "no", "scamshield.gov.sg", "legacy ScamShield app API (Amazon certs 2020-2024); backend, no GET"),
 R("classifier-api.scamshield.sg", "scamshield.sg", "crt.sh", "no", "scamshield.gov.sg", "legacy ScamShield SMS classifier API (certs 2020-2024); backend, no GET"),
 R("grafana.scamshield.sg", "scamshield.sg", "crt.sh", "no", "scamshield.gov.sg", "internal monitoring; single cert Feb 2023"),
 # ---------------- icanactagainstscams.gov.sg (SPF) ----------------
 R("www.icanactagainstscams.gov.sg", "icanactagainstscams.gov.sg", "crt.sh", "yes", "icanactagainstscams.gov.sg",
   "SPF 'I Can ACT Against Scams' site: /scam-trends advisories with scam_site_urls + Brand/Category tags (baseline feed, ../FINDINGS.md); parent police.gov.sg"),
 R("icanactagainstscams.gov.sg", "icanactagainstscams.gov.sg", "crt.sh", "yes", "icanactagainstscams.gov.sg", "apex; wildcard cert 2025-08..2025-10"),
 R("www.beta.icanactagainstscams.gov.sg", "icanactagainstscams.gov.sg", "crt.sh", "maybe", "icanactagainstscams.gov.sg",
   "beta site (certs Oct-Nov 2025; also inside a shared multi-SAN Isomer cert seen via certspotter)"),
 R("stg.icanactagainstscams.gov.sg", "icanactagainstscams.gov.sg", "crt.sh", "no", "icanactagainstscams.gov.sg", "staging; no GET"),
 R("www.stg.icanactagainstscams.gov.sg", "icanactagainstscams.gov.sg", "crt.sh", "no", "icanactagainstscams.gov.sg", "staging; no GET"),
 # ---------------- AntiScam Pango (GovTech) ----------------
 R("pango.gov.sg", "pango.gov.sg", "search", "yes", "pango.gov.sg",
   "AntiScam Pango (GovTech on-device scam-message detector, Android beta 4 Nov 2026) official site per tech.gov.sg release; parent tech.gov.sg; also in crt.sh"),
 R("www.pango.gov.sg", "pango.gov.sg", "crt.sh", "yes", "pango.gov.sg", "AntiScam Pango site (www)"),
 R("api.pango.gov.sg", "pango.gov.sg", "crt.sh", "no", "pango.gov.sg", "app API backend; no GET"),
 R("api.stg.pango.gov.sg", "pango.gov.sg", "crt.sh", "no", "pango.gov.sg", "staging API; no GET"),
 R("api.dev.pango.gov.sg", "pango.gov.sg", "crt.sh", "no", "pango.gov.sg", "dev API; no GET"),
 # ---------------- NCPC ----------------
 R("www.ncpc.org.sg", "ncpc.org.sg", "crt.sh", "yes", "ncpc.org.sg",
   "National Crime Prevention Council: anti-scam campaigns/resources (e.g. /xiamthescams); " + TS + " (Table 4)"),
 R("ncpc.org.sg", "ncpc.org.sg", "crt.sh", "yes", "ncpc.org.sg", "apex; wildcard *.ncpc.org.sg certs 2018-2026"),
 R("link.ncpc.org.sg", "ncpc.org.sg", "crt.sh", "maybe", "ncpc.org.sg", "cPanel/LE certs 2022-08..2024-08 only; purpose unknown (link hub?)"),
 R("ncpc.gov.sg", "ncpc.gov.sg", "crt.sh", "maybe", "ncpc.org.sg", "old NCPC .gov.sg domain; only certs 2015-08..2016-01 (+wildcard)"),
 R("xiamthescams.sqkii.com", "sqkii.com", "search", "yes", "ncpc.org.sg",
   "#XiamTheScams NCPC/SPF/MHA anti-scam web game built by vendor Sqkii, ran 24 Oct 2024-22 Jan 2025 (search); vendor-hosted"),
 # ---------------- scamalert.sg (NCPC legacy) ----------------
 R("www.scamalert.sg", "scamalert.sg", "crt.sh", "yes", "ncpc.org.sg",
   "NCPC ScamAlert portal, retired into ScamShield Suite (Sep 2024); 01_sg_official.md: 301 -> www.scamshield.gov.sg; scraped corpus 2016-20 exists"),
 R("scamalert.sg", "scamalert.sg", "crt.sh", "yes", "ncpc.org.sg",
   "apex; wildcard *.scamalert.sg certs 2018-2026; cPanel service names (cpanel/cpcalendars/cpcontacts/webdisk/webmail/mail/autodiscover, also under forms./lp./makeathon./quiz.) collapsed here, all certs ended 2018-2022"),
 R("quiz.scamalert.sg", "scamalert.sg", "crt.sh", "yes", "ncpc.org.sg", "NCPC scam quiz; certs 2020-07..2025-01"),
 R("www.quiz.scamalert.sg", "scamalert.sg", "crt.sh", "yes", "ncpc.org.sg", "certs 2020-07..2021-10"),
 R("forms.scamalert.sg", "scamalert.sg", "crt.sh", "maybe", "ncpc.org.sg", "forms (scam report/feedback?); certs 2020-12..2024-09"),
 R("www.forms.scamalert.sg", "scamalert.sg", "crt.sh", "maybe", "ncpc.org.sg", "certs 2020-12..2021-10"),
 R("lp.scamalert.sg", "scamalert.sg", "crt.sh", "maybe", "ncpc.org.sg", "landing pages (campaign); certs 2020-08..2024-08"),
 R("www.lp.scamalert.sg", "scamalert.sg", "crt.sh", "maybe", "ncpc.org.sg", "certs 2020-08..2021-09"),
 R("makeathon.scamalert.sg", "scamalert.sg", "crt.sh", "maybe", "ncpc.org.sg", "Anti-Scam Makeathon event site; certs 2019-09..2021-06"),
 R("www.makeathon.scamalert.sg", "scamalert.sg", "crt.sh", "maybe", "ncpc.org.sg", "certs 2019-09..2021-06"),
 # ---------------- SPF / MHA ----------------
 R("www.police.gov.sg", "police.gov.sg", "search", "yes", "police.gov.sg",
   "SPF: /advisories/scams, media-hub news (354 scam advisories in sitemap), scam & cybercrime briefs"),
 R("eservices1.police.gov.sg", "police.gov.sg", "search", "yes", "police.gov.sg",
   "SPF e-services: online police report for scams (/phub/eservices/landingpage/police-report per search); report_portal"),
 R("www.mha.gov.sg", "mha.gov.sg", "search", "maybe", "mha.gov.sg", "MHA newsroom: anti-scam speeches/COS, E-commerce Marketplace Transaction Safety Ratings"),
 # ---------------- CSA ----------------
 dict(R("www.csa.gov.sg", "csa.gov.sg", "crt.sh", "yes", "csa.gov.sg",
   "CSA/SingCERT alerts & advisories (RSS), /GoSafeOnline, report-a-phishing-email, SG Cyber Safe Seniors; latest issuance 2026-11-19 per certspotter (crt.sh lagging)"), cert_last_seen="2026-11-19"),
 R("csa.gov.sg", "csa.gov.sg", "crt.sh", "yes", "csa.gov.sg", "apex; wildcard *.csa.gov.sg certs 2019-2026"),
 # ---------------- MAS ----------------
 R("www.mas.gov.sg", "mas.gov.sg", "link", "yes", "mas.gov.sg", "MAS Investor Alert List at /ial (from sources/01_sg_official.md)"),
 R("eservices.mas.gov.sg", "mas.gov.sg", "crt.sh", "maybe", "mas.gov.sg",
   "MAS e-services: Financial Institutions Directory (/fid, allowlist) and the IAL search backend used by third-party scrapers (not probed)"),
 R("www.moneysense.gov.sg", "moneysense.gov.sg", "search", "yes", "moneysense.gov.sg", "MoneySense (MAS financial education): /scams/, how-to-spot-an-investment-scam; parent mas.gov.sg"),
 # ---------------- OGP / GovTech / MDDI / IMDA ----------------
 R("reports.open.gov.sg", "open.gov.sg", "crt.sh", "maybe", "open.gov.sg",
   "OGP product reports: /scamshield/overview, /scamshield/metrics, /scamshield/updates (search); host is multi-product"),
 R("products.open.gov.sg", "open.gov.sg", "search", "maybe", "open.gov.sg", "OGP product pages incl. /scamshield; name also present in crt.sh open.gov.sg set"),
 R("www.open.gov.sg", "open.gov.sg", "search", "maybe", "open.gov.sg", "OGP site: /products/scamshield"),
 R("ask.gov.sg", "ask.gov.sg", "search", "maybe", "ask.gov.sg",
   "AskGov Q&A platform: ScamShield FAQ at /scamshield and AntiScam Pango help at /pango; multi-agency host (crt.sh q=ask.gov.sg 502 twice on 2026-11-25)"),
 R("go.ask.gov.sg", "ask.gov.sg", "search", "maybe", "ask.gov.sg", "AskGov short links, e.g. go.ask.gov.sg/scamshield"),
 R("www.tech.gov.sg", "tech.gov.sg", "search", "maybe", "tech.gov.sg",
   "GovTech: /products-and-services/for-citizens/scam-prevention/ (ScamShield, SATIS, Pango) + technews scam explainers"),
 R("phishmon.gcsoc.tech.gov.sg", "tech.gov.sg", "crt.sh", "maybe", "tech.gov.sg",
   "GovTech GCSOC phishing-monitoring service (name); internal, certs 2023-03..2025-05; no GET"),
 R("stg.phishmon.gcsoc.tech.gov.sg", "tech.gov.sg", "crt.sh", "no", "tech.gov.sg", "staging of phishmon; certs end 2025-05"),
 R("dev.phishmon.gcsoc.tech.gov.sg", "tech.gov.sg", "crt.sh", "no", "tech.gov.sg", "dev of phishmon; certs end 2025-05"),
 R("www.smartnation.gov.sg", "smartnation.gov.sg", "search", "maybe", "smartnation.gov.sg", "/initiatives/scamshield"),
 R("www.mddi.gov.sg", "mddi.gov.sg", "search", "maybe", "mddi.gov.sg", "/other-pages/anti-scam-efforts/ (lists SIMCardHowMany, ScamShield, roadshow)"),
 R("www.imda.gov.sg", "imda.gov.sg", "search", "maybe", "imda.gov.sg", "/how-we-can-help/anti-scam-measures (SMS sender ID, SSIR)"),
 R("services2-ctoaascam-ez.in.imda.gov.sg", "imda.gov.sg", "crt.sh", "no", "imda.gov.sg", "keyword false positive ('ctoaas'+'cam'); internal"),
 R("services2-ctoaascam-ez-stg.in.imda.gov.sg", "imda.gov.sg", "crt.sh", "no", "imda.gov.sg", "keyword false positive; internal staging"),
 R("www.digitalforlife.gov.sg", "digitalforlife.gov.sg", "search", "maybe", "digitalforlife.gov.sg", "IMDA Digital for Life: scam-spotting learning resources, festival; parent imda.gov.sg"),
 R("form.gov.sg", "form.gov.sg", "search", "maybe", "open.gov.sg",
   "FormSG platform; hosts IMDA/GovTech SIMCardHowMany postpaid-SIM checker (anti-scam tool, beta 26 Feb 2026) at a form path; multi-tenant host"),
 R("www.gov.sg", "gov.sg", "search", "maybe", "gov.sg", "hosts the Trusted Sites allowlist (/trusted-sites/, last updated 6 Nov 2026) and scam explainers"),
 # ---------------- community / non-official ----------------
 R("checkmate.sg", "checkmate.sg", "search", "yes", "checkmate.sg", "CheckMate: volunteer-run (bettersg) WhatsApp scam/misinformation checker; NOT official. crt.sh: ~57 names; infra (admin, api.backend, portkey, stripe, webhook, whatsapp, evals, datasets, workspace, corporate, line, qr, ref, screenshots, files, data, certificates, measure, hi) + staging.* collapsed here"),
 # ---------------- unknown-owner scam-keyword .sg registrations (CT) ----------------
 R("scam.sg", "scam.sg", "crt.sh", "maybe", None,
   "owner unknown (no web-search hits); CT shows an app stack (accounts/clerk/dashboard/cms/crawl4ai/searxng/browserless/n8n/verified.) => looks like a private scam-check service; not visited (non-official)"),
 R("scams.sg", "scams.sg", "crt.sh", "maybe", None, "owner unknown; Sectigo DV certs 2025-01..2026-10 (+wildcard); not visited (non-official)"),
]
# scam.sg subdomains (collapsed into record notes except user-facing names)
for h, n in [("www.scam.sg", "certs 2023-12..2026-04"), ("verified.scam.sg", "certs 2024-08..2026-10"),
             ("dashboard.scam.sg", "certs 2024-09..2026-07; children accounts./clerk./dev. dashboard.scam.sg")]:
    rows.append(R(h, "scam.sg", "crt.sh", "maybe", None, "owner unknown; " + n + "; not visited"))

extra = os.path.join(W, "data/seed_extra.json")
if os.path.exists(extra):
    rows += json.load(open(extra))

# ---------------- Trusted Sites list ----------------
tr = json.load(open(os.path.join(W, "data/web/trusted_rows.json")))
have = {r["host"] for r in rows}
REL = {"www.ncpc.org.sg": "yes", "www.scamshield.gov.sg": "yes", "go.gov.sg": "maybe", "www.mlc.sg": "maybe"}
seen = set()
for t in tr["rows"]:
    h = t["host"]
    if h in have or h in seen:
        continue
    seen.add(h)
    tab = (t["table"] or "").split(":")[0]
    note = f"gov.sg Trusted Sites list ({tab}: {t['name']}; page last updated 6 Nov 2026) - ALLOWLIST entry (official/associated site), not a scam-info source"
    if h == "go.gov.sg":
        note = "gov.sg Trusted Sites list (official short-link bullet) - ALLOWLIST: official Government short-link domain used in scam-verification advice"
    if h == "www.mlc.sg":
        note += "; Media Literacy Council publishes online-falsehood/scam literacy material"
    parts = h.split(".")
    reg = ".".join(parts[-3:]) if h.endswith((".gov.sg", ".org.sg", ".com.sg", ".edu.sg")) else ".".join(parts[-2:])
    owner = {"dsta.x0pa.ai": "dsta.gov.sg", "rpace.floralms.com": "rp.edu.sg", "asmc.asean.org": None}.get(h, reg)
    if h in ("dsta.x0pa.ai", "rpace.floralms.com", "asmc.asean.org"):
        note += "; vendor/third-party-hosted, owner inferred from list entry name"
    rows.append(R(h, reg, "trusted_sites_list", REL.get(h, "no"), owner, note))
for m in tr.get("mirror_not_on_page", []):
    if m not in have and m not in seen:
        rows.append(R(m, m, "trusted_sites_list", "no", m,
                      "only in GitHub mirror elliotwutingfeng/GovSGTrustedSites allowlist.txt, NOT on current official page (stale?) - ALLOWLIST"))
json.dump(rows, open(os.path.join(W, "data/seed.json"), "w"), indent=1)
print(len(rows), "seed rows")
