"""Discovery follow-up: publications found via a publisher's sitemap/RSS are fetched once and scanned for listed sites.

Before SCOPE.md the sitemap/RSS endpoints only recorded that an advisory page exists; a new police.gov.sg / ica.gov.sg
advisory naming fake websites would never have produced sites. Here each new publication page (same publisher site
only, robots.txt honoured, polite per-host spacing via fetch.py) is fetched and its text run through the same
extraction + role rules as registry pages; sightings attach to the existing report. Newest first, bounded per run,
<=3 attempts per page. Official pages only - this never touches a scam host.
"""
import json
from .normalize import EXT, iso, now, extract_indicators
from .parsers.core import text_from_html, with_ctx
from . import fetch, ingest

PER_RUN = 40
STRONG = ("scam", "fake", "phish", "fraud", "impersonat", "spoof", "fictitious", "unauthorised-website", "bogus")   # fetched first
STRONG_SQL = "(" + " OR ".join(f"lower(r.url || ' ' || r.title) LIKE '%{k}%'" for k in STRONG) + ")"


def candidates(con, limit):
    return con.execute("""SELECT r.report_id, r.native_id, r.url, r.title, r.published_at, r.raw, r.source_id, ep.host ep_host, ep.endpoint_id
        FROM report r JOIN source src USING(source_id) JOIN endpoint ep ON ep.endpoint_id=src.endpoint_id
        WHERE ep.parser IN ('rss','sitemap') AND src.sg_scope='native' AND r.url LIKE 'http%'
          AND json_extract(COALESCE(r.raw,'{}'),'$.followup.at') IS NULL
          AND COALESCE(json_extract(r.raw,'$.followup.attempts'),0) < 3
        ORDER BY (CASE WHEN REGEXP_LIKE THEN 0 ELSE 1 END), COALESCE(r.published_at, r.first_ingested_at) DESC
        LIMIT ?""".replace("REGEXP_LIKE", STRONG_SQL), (limit,)).fetchall()


def run(con, limit=PER_RUN, cx=None, verbose=False):
    cx = cx or ingest.Ctx(con); stats = {"fetched": 0, "with_sites": 0, "skipped": 0, "errors": 0}
    for r in candidates(con, limit):
        raw = json.loads(r["raw"] or "{}"); fu = raw.get("followup") or {}; fu["attempts"] = fu.get("attempts", 0) + 1
        host = (EXT(r["url"]).top_domain_under_public_suffix or ""); ep_reg = EXT(r["ep_host"]).top_domain_under_public_suffix
        if host != ep_reg:                                   # only the publisher's own site
            fu |= {"at": iso(now()), "status": "skipped_offsite"}; stats["skipped"] += 1
        elif not fetch.robots_ok(r["url"]):
            fu |= {"at": iso(now()), "status": "robots_disallow"}; stats["skipped"] += 1
        else:
            res = fetch.get(r["url"])
            ctype = (res.get("ctype") or "").lower()
            if res["status"] == 200 and res["body"] and "html" in ctype:
                title, text = text_from_html(res["body"])
                src = dict(con.execute("SELECT * FROM source WHERE source_id=?", (r["source_id"],)).fetchone())
                ep = dict(con.execute("SELECT * FROM endpoint WHERE endpoint_id=?", (r["endpoint_id"],)).fetchone())
                out = {"reports": [{"native_id": r["native_id"], "url": r["url"], "title": title or r["title"], "body": text[:40000],
                                    "published_at": r["published_at"], "modified_at": None, "categories_raw": [], "brands_raw": [], "raw": None}],
                       "indicators": with_ctx(text, extract_indicators(text), r["native_id"]), "complete": False, "state": {}}
                ingest.apply(con, src, ep, out, cx)
                n_ioc = con.execute("""SELECT COUNT(*) FROM sighting s JOIN indicator i USING(indicator_id) WHERE s.report_id=? AND s.role='ioc'
                                       AND i.type IN ('domain','hostname','url')""", (r["report_id"],)).fetchone()[0]
                fu |= {"at": iso(now()), "status": "ok", "n_extracted": len(out["indicators"]), "n_site_ioc": n_ioc}
                stats["fetched"] += 1; stats["with_sites"] += bool(n_ioc)
            elif res["status"] == 200:
                fu |= {"at": iso(now()), "status": f"skipped_ctype:{ctype[:30]}"}; stats["skipped"] += 1
            else:
                fu |= {"status": f"error:{res['status'] or res['error']}"[:80]}; stats["errors"] += 1
                if fu["attempts"] >= 3: fu["at"] = iso(now())
        raw["followup"] = fu
        con.execute("UPDATE report SET raw=? WHERE report_id=?", (json.dumps(raw, ensure_ascii=False), r["report_id"]))
        if verbose: print(f"  followup {fu.get('status'):24} sites={fu.get('n_site_ioc', '-'):<3} {r['url'][:100]}", flush=True)
        con.commit()
    return stats
