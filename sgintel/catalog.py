"""Load registry -> entity/alias/allowlist tables; build endpoint + source catalog with SG scope and poll tiers."""
import json, re, urllib.parse
from pathlib import Path
from .normalize import ROOT, iso, now, parse_ts
from .db import J

TIER = {"hot": (3600, 900, 3 * 3600), "daily": (86400, 6 * 3600, 3 * 86400),
        "weekly": (7 * 86400, 2 * 86400, 14 * 86400), "monthly": (30 * 86400, 14 * 86400, 60 * 86400)}
SCAM_KW = r"scam|fraud|phish|impersonat|fake|hoax|spoof|beware|advisor|alert|unsolicited|vigilant|security-notice"
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# Global / non-registry feeds (sources/02_generic_feeds.md, SOURCES.md). sg_scope=filtered pass through sg_filter_pass().
PDB = "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/"
EXTERNAL = [
  # id, name, publisher, url, fetch_kind, parser, tier, authority, scope, semantics, licence, params
  ("spf-icanact", "SPF I can ACT: Scam Trends", "police.gov.sg", "https://www.icanactagainstscams.gov.sg/scam-trends", "html_rsc", "spf_icanact", "hot", "authoritative", "native", "snapshot_full", "SG Gov terms (unverified)", None),
  ("mas-ial-opensanctions", "MAS Investor Alert List (OpenSanctions mirror)", "mas.gov.sg", "https://data.opensanctions.org/datasets/latest/sg_mas_investor_alert/source.json", "json", "mas_opensanctions", "daily", "regulator", "native", "snapshot_full", "CC-BY-NC-4.0", None),
  ("phishdb-links-new-today", "Phishing.Database links NEW today", "github.com#phishing-database", PDB + "phishing-links-NEW-today.txt", "txt", "url_list", "hot", "community", "filtered", "append_only", "MIT", {"status": "NEW"}),
  ("phishdb-links-active", "Phishing.Database links ACTIVE", "github.com#phishing-database", PDB + "phishing-links-ACTIVE.txt", "txt", "url_list", "daily", "community", "filtered", "active_list", "MIT", {"status": "ACTIVE"}),
  ("phishdb-domains-active", "Phishing.Database domains ACTIVE", "github.com#phishing-database", PDB + "phishing-domains-ACTIVE.txt", "txt", "url_list", "daily", "community", "filtered", "active_list", "MIT", {"status": "ACTIVE"}),
  ("phishing-army-extended", "Phishing Army extended blocklist", "phishing.army", "https://phishing.army/download/phishing_army_blocklist_extended.txt", "txt", "url_list", "daily", "community", "filtered", "active_list", "GPL-3.0 generator; upstream ToU", None),
  ("phishdestroy", "PhishDestroy destroylist", "github.com#phishdestroy", "https://raw.githubusercontent.com/phishdestroy/destroylist/main/list.json", "json", "url_list", "daily", "community", "filtered", "append_only", "CC-BY-4.0", None),
  ("openphish-community", "OpenPhish community feed", "openphish.com", "https://openphish.com/feed.txt", "txt", "url_list", "daily", "community", "filtered", "active_list", "OpenPhish community ToU", None),
  ("phishstats-api", "PhishStats API (SG keyword rotation)", "phishstats.info", "https://api.phishstats.info/api/phishing", "api", "phishstats", "hot", "community", "filtered", "event_stream", "free tier, 50 req/day anon",
   {"keywords": ["carousell", "paylah", "singpass", "posb", "dbs", "ocbc", "uob", "singpost", "ninjavan", "onemotoring", "simplygo", "ezlink", "paynow", "singtel", "starhub", "cpf", "iras", "sgarrival", "shopee-sg", "lazada-sg"], "cursor": 0, "page_size": 50}),
]
EXTERNAL_PUBLISHERS = {"github.com#phishing-database": "Phishing.Database (mitchellkrogza)", "github.com#phishdestroy": "PhishDestroy",
                       "phishing.army": "Phishing Army", "openphish.com": "OpenPhish", "phishstats.info": "PhishStats"}

def tier_for(kind, latest, has_machine):
    age = (now() - parse_ts(latest + "T00:00:00Z" if latest and len(latest) == 10 else (latest + "-01T00:00:00Z" if latest and len(latest) == 7 else None))).days if latest and len(latest) in (7, 10) else None
    fresh = lambda d: age is not None and age <= d
    if kind == "fake_indicator_list": t = "daily" if fresh(365) else "weekly"
    elif kind in ("advisory_feed", "news_releases"): t = "daily" if fresh(90) else "weekly"
    elif kind == "alert_page": t = "weekly" if fresh(365) else "monthly"
    elif kind == "official_channels": t = "weekly"
    else: t = "monthly"
    if has_machine and t == "daily": t = "weekly"      # discovery happens via its sitemap/RSS endpoint
    return t

def upsert_endpoint(con, url, fetch_kind, parser, tier, params=None):
    host = urllib.parse.urlsplit(url).hostname or ""
    iv, lo, hi = TIER[tier]
    row = con.execute("SELECT endpoint_id, tier FROM endpoint WHERE url=?", (url,)).fetchone()
    if row:   # same URL requested by several sources: keep the hottest tier
        order = list(TIER)
        if order.index(tier) < order.index(row["tier"]):
            con.execute("UPDATE endpoint SET tier=?, interval_s=?, min_interval_s=?, max_interval_s=? WHERE endpoint_id=?", (tier, iv, lo, hi, row["endpoint_id"]))
        if params: con.execute("UPDATE endpoint SET params=json_patch(COALESCE(params,'{}'), ?) WHERE endpoint_id=?", (J(params), row["endpoint_id"]))
        return row["endpoint_id"]
    cur = con.execute("""INSERT INTO endpoint(url, host, fetch_kind, parser, tier, interval_s, min_interval_s, max_interval_s, next_due_at, params)
                         VALUES (?,?,?,?,?,?,?,?,?,?)""", (url, host, fetch_kind, parser, tier, iv, lo, hi, iso(now()), J(params)))
    return cur.lastrowid

def load(con):
    reg = ROOT / "registry" / "merged"
    E = json.load(open(reg / "entities.json")); S = json.load(open(reg / "sources.json"))
    t = iso(now())
    # entities (two passes so parent FKs resolve)
    for e in E:
        con.execute("""INSERT INTO entity(entity_id,name,abbr,kind,sector,country,notes,verified_at) VALUES (?,?,?,?,?,?,?,?)
                       ON CONFLICT(entity_id) DO UPDATE SET name=excluded.name, abbr=excluded.abbr, sector=excluded.sector, notes=excluded.notes""",
                    (e["entity_id"], e["name"], e.get("abbr"), e["kind"], e.get("sector"), e.get("country") or "SG", e.get("notes"), e.get("verified_at")))
    for pid, name in EXTERNAL_PUBLISHERS.items():
        con.execute("INSERT OR IGNORE INTO entity(entity_id,name,kind,sector,country) VALUES (?,?,?,?,?)", (pid, name, "organisation", "other", "ZZ"))
    ids = {r[0] for r in con.execute("SELECT entity_id FROM entity")}
    for e in E:
        p = e.get("parent_entity_id")
        if p and p in ids: con.execute("UPDATE entity SET parent_entity_id=? WHERE entity_id=?", (p, e["entity_id"]))
        for a in e.get("aliases") or []:
            con.execute("INSERT OR IGNORE INTO entity_alias VALUES (?,?,?,?,?)", (e["entity_id"], a, a.strip().lower(), "registry", None))
        for tid in e["external_ids"].get("spf_brand_tag_ids") or []:
            con.execute("UPDATE entity_alias SET spf_tag_id=?, origin='spf_brand_tag' WHERE entity_id=? AND spf_tag_id IS NULL AND alias_norm IN (SELECT alias_norm FROM entity_alias WHERE entity_id=?)", (tid, e["entity_id"], e["entity_id"]))
        if e["kind"] == "fictitious_brand": continue
        off = e["official"]
        for kind, key in (("domain", "domains"), ("host", "hosts"), ("sms_sender_id", "sms_sender_ids"), ("hotline", "hotlines"),
                          ("short_link_domain", "short_link_domains"), ("social", "social")):
            for v in off.get(key) or []:
                v = v.strip(); v = v.lower() if kind in ("domain", "host", "short_link_domain") else v
                if v: con.execute("INSERT OR IGNORE INTO entity_official VALUES (?,?,?,?)", (kind, v, e["entity_id"], (e.get("evidence") or [None])[0]))
    # registry pages -> sources (+ their page endpoint and machine endpoint)
    n_src = 0
    for s in S:
        kind = re.search(r"kind=(\w+)", s["notes"]).group(1)
        latest = (re.search(r"latest=([^;]+)", s["notes"]) or [None, None])[1]; latest = None if latest in (None, "None") else latest.strip()
        inds = (re.search(r"indicators=([^;]+)", s["notes"]) or [None, ""])[1]
        mu = s.get("machine_url")
        fk = "pdf" if s["access"] == "pdf" or s["url"].lower().endswith(".pdf") else "html"
        ep = upsert_endpoint(con, s["url"], fk, "pdf_hash" if fk == "pdf" else "html_page", tier_for(kind, latest, bool(mu)))
        scope = "allowlist" if kind == "official_channels" else "native"
        role = {"fake_indicator_list": "ioc", "official_channels": "official"}.get(kind, "unknown")
        con.execute("""INSERT INTO source(source_id,name,publisher_entity_id,url,endpoint_id,page_kind,access,authority,sg_scope,lifecycle_semantics,default_role,lists_indicators,tlp,notes)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(url) DO NOTHING""",
                    (s["source_id"], s["name"], s["publisher_entity_id"] if s["publisher_entity_id"] in ids else None, s["url"], ep, kind, s["access"],
                     s["authority"], scope, s["lifecycle_semantics"], role, inds if inds != "none" else None, "TLP:CLEAR", s["notes"]))
        n_src += 1
        if mu and mu != s["url"] and mu.startswith("http"):
            is_feed = bool(re.search(r"rss|atom|feed", mu, re.I)) and "sitemap" not in mu.lower()
            mk = "rss" if is_feed else ("pdf" if mu.lower().endswith(".pdf") else "sitemap")
            mtier = "hot" if "scamshield" in mu and is_feed else ("daily" if is_feed or kind in ("advisory_feed", "fake_indicator_list", "news_releases") else "weekly")
            con.execute("UPDATE endpoint SET params=json_set(COALESCE(params,'{}'),'$.refs',COALESCE(json_extract(params,'$.refs'),0)+1) WHERE url=?", (mu,))
            mep = upsert_endpoint(con, mu, mk, {"rss": "rss", "sitemap": "sitemap", "pdf": "pdf_hash"}[mk], mtier,
                                  {"publisher_entity_id": s["publisher_entity_id"], "keywords": SCAM_KW} if mk == "sitemap" else None)
            con.execute("UPDATE endpoint SET params=json_set(COALESCE(params,'{}'),'$.refs',COALESCE(json_extract(params,'$.refs'),0)+1) WHERE endpoint_id=?", (mep,))
            con.execute("""INSERT INTO source(source_id,name,publisher_entity_id,url,endpoint_id,page_kind,access,authority,sg_scope,lifecycle_semantics,default_role,tlp,notes)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(url) DO NOTHING""",
                        ("m-" + slug(re.sub(r"^https?://", "", mu))[:58], f"{s['name'].split(':')[0]}: {mk} discovery", s["publisher_entity_id"] if s["publisher_entity_id"] in ids else None,
                         mu, mep, "feed", mk, s["authority"], "native", "append_only", "unknown", "TLP:CLEAR", f"discovery endpoint for {kind} pages"))
    for (sid, name, pub, url, fk, parser, tier, auth, scope, sem, lic, params) in EXTERNAL:
        ep = upsert_endpoint(con, url, fk, parser, tier, params)
        con.execute("""INSERT INTO source(source_id,name,publisher_entity_id,url,endpoint_id,page_kind,access,authority,sg_scope,sg_filter_id,lifecycle_semantics,default_role,licence,tlp)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(source_id) DO UPDATE SET endpoint_id=excluded.endpoint_id, url=excluded.url""",
                    (sid, name, pub if pub in ids else None, url, ep, "feed", fk, auth, scope, "sgfilter-v1" if scope == "filtered" else None, sem, "ioc", lic, "TLP:CLEAR"))
    con.commit()
    return n_src
