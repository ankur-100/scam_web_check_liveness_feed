#!/usr/bin/env python3
"""Second batch of manual host rows -> data/seed_extra.json (read by seed.py)."""
import json, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def R(host, reg, via, rel, owner, notes="", first=None, last=None):
    r = {"host": host, "registrable_domain": reg, "discovered_via": via,
         "scam_relevant": rel, "owner_entity_id": owner, "notes": notes}
    if first or last:
        r["cert_first_seen"], r["cert_last_seen"] = first, last
    return r

rows = []
# ---- csa.gov.sg full CT set (crt.sh 2026-11-26), beyond www/apex already in seed.py ----
CSA = {
 "faqs.csa.gov.sg": ("maybe", "CSA FAQ host; single cert 2022-03 only"),
 "web.csa.gov.sg": ("no", "legacy web host; certs 2019-11..2022-11"),
 "www-origin.csa.gov.sg": ("no", "origin for www (CDN); certs to 2024-02"),
 "www-origin-uat.csa.gov.sg": ("no", "UAT origin"),
 "www-stg.csa.gov.sg": ("no", "staging; single cert 2018-01"),
 "origin1-www.csa.gov.sg": ("no", "old origin; cert 2019-08 only"),
 "www.origin1-www.csa.gov.sg": ("no", "old origin; cert 2019-08 only"),
 "web-intranet.csa.gov.sg": ("no", "intranet; certs 2022-10..2023-10"),
 "web-intranet-uat.csa.gov.sg": ("no", "intranet UAT"),
 "ihp.csa.gov.sg": ("no", "Internet Hygiene Portal (website/email security ratings, incl. DMARC); not scam advisories"),
 "www.ihp.csa.gov.sg": ("no", "IHP www; certs to 2023-07"),
 "api.ihp.csa.gov.sg": ("no", "IHP API"),
 "enterpriseapi.ihp.csa.gov.sg": ("no", "IHP enterprise API"),
 "ihp-stg.csa.gov.sg": ("no", "IHP staging (+ wildcard *.ihp-stg)"),
 "www.ihp-stg.csa.gov.sg": ("no", "IHP staging"),
 "api.ihp-stg.csa.gov.sg": ("no", "IHP staging API"),
 "enterpriseapi.ihp-stg.csa.gov.sg": ("no", "IHP staging API"),
 "nc3.csa.gov.sg": ("no", "unidentified system 'nc3' (single cert 2026-02)"),
 "dev-nc3.csa.gov.sg": ("no", "dev of nc3"),
 "uat-nc3.csa.gov.sg": ("no", "UAT of nc3"),
 "logpipe.amrs.nc3.csa.gov.sg": ("no", "log pipeline (internal)"),
 "uat.logpipe.amrs.nc3.csa.gov.sg": ("no", "log pipeline UAT (internal)"),
 "dev-cardinal.csa.gov.sg": ("no", "unidentified system 'cardinal' (dev)"),
 "uat-cardinal.csa.gov.sg": ("no", "unidentified system 'cardinal' (UAT)"),
 "pslc.csa.gov.sg": ("no", "unidentified 'pslc' site (Sectigo DV certs 2025-04..2026-10)"),
 "www.pslc.csa.gov.sg": ("no", "www of pslc"),
}
for h, (rel, n) in CSA.items():
    rows.append(R(h, "csa.gov.sg", "crt.sh", rel, "csa.gov.sg", n))
for s in ["a1", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b4"]:
    for pre in ("", "www."):
        rows.append(R(f"{pre}ssix-{s}.csa.gov.sg", "csa.gov.sg", "crt.sh", "no", "csa.gov.sg",
                      "one of 10 'ssix-*' sites (Sectigo DV certs 2025-01..2026-03; likely exercise/test infrastructure)"))
# ---- CSA legacy domains ----
rows.append(R("www.gosafeonline.sg", "gosafeonline.sg", "crt.sh", "yes", "csa.gov.sg",
              "legacy CSA GoSafeOnline cyber-hygiene/scam-awareness portal (content now at www.csa.gov.sg/GoSafeOnline); Amazon certs 2012-04..2026-08"))
rows.append(R("gosafeonline.sg", "gosafeonline.sg", "crt.sh", "yes", "csa.gov.sg", "apex of legacy GoSafeOnline"))
rows.append(R("singcert.org.sg", "singcert.org.sg", "crt.sh", "maybe", "csa.gov.sg",
              "legacy SingCERT domain (cPanel/Entrust certs 2014..2022-11); cPanel service names collapsed here"))
rows.append(R("www.singcert.org.sg", "singcert.org.sg", "crt.sh", "maybe", "csa.gov.sg", "legacy SingCERT www; certs end 2022-11"))
# ---- police.gov.sg report e-services (keyword filter 'eservice' = online police report incl. scams) ----
# dates recovered from digest crt.sh q=police.gov.sg (2026-11-25); prod hosts only, sit/uat/qa/stg omitted
POL = [("eservices.police.gov.sg", "2018-04-23", "2024-04-11", "maybe", "original e-services host; certs end 2024-04 (superseded by eservices1-5)"),
       ("eservices2.police.gov.sg", "2021-04-23", "2026-09-27", "maybe", "SPF e-services cluster 2"),
       ("eservices3.police.gov.sg", "2022-05-31", "2024-06-04", "maybe", "SPF e-services cluster 3; certs end 2024-06"),
       ("eservices4.police.gov.sg", "2024-01-22", "2025-12-22", "maybe", "SPF e-services cluster 4"),
       ("eservices5.police.gov.sg", "2024-01-23", None, "maybe", "SPF e-services cluster 5")]
for h, f, l, rel, n in POL:
    rows.append(R(h, "police.gov.sg", "crt.sh", rel, "police.gov.sg",
                  n + "; police e-report portal family (www.<name> alias also in CT; sit/uat/qa/stg variants omitted). No scam-named hosts among 127 police.gov.sg CT names (crt.sh %.police.gov.sg 2026-11-26)", f, l))
# ---- unknown-owner keyword .sg domains ----
rows.append(R("phishing.sg", "phishing.sg", "crt.sh", "maybe", None,
              "owner unknown (no web-search hits); Cloudflare; subdomains read./resources./www. active to 2026-10; could be a phishing-awareness/simulation vendor; not visited (non-official)"))
for h in ("www.phishing.sg", "read.phishing.sg", "resources.phishing.sg"):
    rows.append(R(h, "phishing.sg", "crt.sh", "maybe", None, "owner unknown; not visited (non-official)"))
rows.append(R("cybersafe.sg", "cybersafe.sg", "crt.sh", "maybe", None,
              "owner unknown; cPanel/Cloudflare, earlier staged at cybersafe.sg.ewr.com.sg (SG web agency); subdomains old./sm./sm-dev. + cPanel service names; not visited (non-official)"))
rows.append(R("www.cybersafe.sg", "cybersafe.sg", "crt.sh", "maybe", None, "owner unknown; not visited"))
rows.append(R("checkscam.sg", "checkscam.sg", "crt.sh", "maybe", None,
              "owner unknown; only LE certs 2023-06 (+wildcard); NXDOMAIN now -> retired/lapsed registration"))

# ---- checkmate.sg (community, non-official): user-facing names only; ~45 infra/staging names collapsed ----
CM = [("www.checkmate.sg", "yes", "CheckMate site (www)"),
      ("scam-game.checkmate.sg", "yes", "scam-awareness game (+wildcard), single cert 2026-10-03 - new"),
      ("game.checkmate.sg", "maybe", "game host (+wildcard), cert 2026-07"),
      ("search.checkmate.sg", "maybe", "search of checked messages? certs 2026-02..2026-08"),
      ("checkers.checkmate.sg", "maybe", "volunteer checkers portal"),
      ("accounts.cpf.checkmate.sg", "maybe", "'cpf' tenant (accounts/clerk + cpf.staging) certs 2025-11..2026-09 - possibly a CPF-focused deployment; unverified")]
for h, rel, n in CM:
    rows.append(R(h, "checkmate.sg", "crt.sh", rel, "checkmate.sg", "CheckMate (volunteer, NOT official); " + n))

# ---- SSIR (SGNIC) ----
rows.append(R("smsregistry.sg", "smsregistry.sg", "certspotter", "maybe", "sgnic.sg",
              "Singapore SMS Sender ID Registry (SGNIC/IMDA): public list of organisations with registered sender IDs at /web/org/public-listing (allowlist vs SMS spoofing). crt.sh 502 x2 on 2026-11-26; certspotter (current certs only): apex + *.smsregistry.sg 2026-07, feature./staging./testing. envs",
              None, "2026-07-18"))
# ---- Online Safety Commission (2026) - online-harms reporting, not scam-specific ----
for h, rel, n in [("www.osc.gov.sg", "maybe", "Online Safety Commission site (online-harms relief; overlaps impersonation, not scam-specific)"),
                  ("report.osc.gov.sg", "maybe", "OSC online-harms report portal (certs from 2026-04)"),
                  ("osc.gov.sg", "maybe", "apex")]:
    rows.append(R(h, "osc.gov.sg", "crt.sh", rel, "osc.gov.sg", n + "; found via guessed-zone CT query; preprod-/uat-report, osc-int* omitted"))
rows.append(R("www.dnc.gov.sg", "dnc.gov.sg", "crt.sh", "no", "pdpc.gov.sg",
              "Do Not Call Registry (telemarketing opt-out), checked via guessed-zone CT query; not a scam-info source; portal.dnc.gov.sg also in CT"))
# ---- infra aliases revealed by DNS CNAMEs of icanactagainstscams (codename 'scamsexposed') ----
for h, n in [("scamsexposed-cf.app.optical.gov.sg", "CNAME target of www.icanactagainstscams.gov.sg"),
             ("scamsexposed-cf.staging.optical.gov.sg", "CNAME target of stg.icanactagainstscams.gov.sg"),
             ("p-gvt-gasp-scamsexposed.on.tc2.airbase.tech.gov.sg", "CNAME target of www.beta.icanactagainstscams.gov.sg"),
             ("s-gvt-gasp-scamsexposed.on.tc2.airbase.tech.gov.sg", "CNAME target of www.stg.icanactagainstscams.gov.sg")]:
    reg = "optical.gov.sg" if "optical" in h else "tech.gov.sg"
    rows.append(R(h, reg, "link", "no", "icanactagainstscams.gov.sg",
                  n + " (DNS); hosting alias revealing internal project codename 'scamsexposed'; not a separate site, no GET"))
json.dump(rows, open(os.path.join(W, "data/seed_extra.json"), "w"), indent=1)
print(len(rows), "extra rows")
