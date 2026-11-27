"""sgintel CLI.  .venv/bin/python -m sgintel <cmd>
  init | load | catalog | crawl [--limit N] [--tier T] [--source ID] | daemon | dedup | export [--since SEQ] | stats | check
  SCOPE.md (impersonating-site liveness):
  proxy                         run the egress proxy (all scam-site probes leave through it; fail-closed without it)
  cycle [--followup N]          roles -> discovery follow-up -> targets -> queue new sites (also runs after every crawl)
  roles | targets | followup [--limit N]
  liveness [--limit N] [--policy P1|P0] [--scope all|listing] [--workers 8] [-v]
  sites                         site report -> data/SITES.md
  output                        write rolling outputs now (out/events, out/snapshots, out/reports; schema/site_feed.schema.json)"""
import argparse, json, sys
from collections import Counter
from . import db, catalog, crawler, liveness, dedup, roles, target, followup, sites as sitesrep
from .normalize import ROOT, iso, now

def catalog_report(con):
    rows = con.execute("""SELECT s.sg_scope, s.page_kind, s.default_role, s.source_id, s.url, s.licence, e.name pub, e.country, ep.tier, ep.fetch_kind, ep.parser,
                          ep.interval_s FROM source s JOIN endpoint ep USING(endpoint_id) LEFT JOIN entity e ON e.entity_id=s.publisher_entity_id""").fetchall()
    L = [f"# Source catalog: SG scope & polling plan ({iso(now())})", "",
         "**native** = SG publisher, SG-only content: ingested as-is. **filtered** = global feed: every item must pass `sg_filter_pass()` "
         "(SG brand/service token in host, or SG bank kit path; `.sg` ccTLD alone is rejected). **allowlist** = official-channel pages: "
         "feed the allowlist, never the IOC stream.", ""]
    c = Counter((r["sg_scope"], r["tier"]) for r in rows)
    L += ["| scope | hot (≤1h) | daily | weekly | monthly | total |", "|---|---|---|---|---|---|"]
    for sc in ("native", "filtered", "allowlist"):
        L.append(f"| {sc} | " + " | ".join(str(c[(sc, t)]) for t in ("hot", "daily", "weekly", "monthly")) + f" | {sum(v for (s, _), v in c.items() if s == sc)} |")
    eps = con.execute("SELECT COUNT(*) FROM endpoint").fetchone()[0]
    L += ["", f"{len(rows)} sources over {eps} distinct endpoints (shared sitemaps/feeds fetched once).", ""]
    L += ["## Filtered (global feeds → SG filter)", "", "| source | tier | parser | licence |", "|---|---|---|---|"]
    L += [f"| {r['source_id']} | {r['tier']} | {r['parser']} | {r['licence'] or ''} |" for r in rows if r["sg_scope"] == "filtered"]
    L += ["", "## Native: structured indicator sources", "", "| source | publisher | tier | parser |", "|---|---|---|---|"]
    L += [f"| {r['source_id']} | {r['pub']} | {r['tier']} | {r['parser']} |" for r in rows if r["sg_scope"] == "native" and r["parser"] in ("spf_icanact", "mas_opensanctions")]
    L += ["", "## Native: machine discovery endpoints (RSS / sitemap)", "", "| publisher | kind | tier | url |", "|---|---|---|---|"]
    L += [f"| {r['pub']} | {r['fetch_kind']} | {r['tier']} | {r['url']} |" for r in sorted(rows, key=lambda r: (r["tier"], r["pub"] or "")) if r["page_kind"] == "feed" and r["sg_scope"] == "native" and r["parser"] in ("rss", "sitemap")]
    L += ["", "## Native: pages (HTML hash + indicator extraction)", "", "| publisher | page kind | default role | tier | url |", "|---|---|---|---|---|"]
    L += [f"| {r['pub']} | {r['page_kind']} | {r['default_role']} | {r['tier']} | {r['url'][:110]} |" for r in sorted(rows, key=lambda r: (r["sg_scope"], r["pub"] or "", r["page_kind"])) if r["page_kind"] != "feed"]
    (ROOT / "data" / "CATALOG.md").write_text("\n".join(L) + "\n")
    return c

def stats(con):
    q = lambda s: con.execute(s).fetchall()
    print("endpoints by tier/enabled:", dict(Counter((r[0], r[1]) for r in q("SELECT tier, enabled FROM endpoint"))))
    print("fetches:", q("SELECT COUNT(*), SUM(changed), SUM(error IS NOT NULL) FROM fetch_log")[0][:])
    print("reports by source scope:", dict(q("SELECT s.sg_scope, COUNT(*) FROM report r JOIN source s USING(source_id) GROUP BY 1")))
    print("indicators:", q("SELECT COUNT(*) FROM indicator")[0][0], "| by status:", dict(q("SELECT status, COUNT(*) FROM indicator GROUP BY 1")))
    print("sightings by role:", dict(q("SELECT role, COUNT(*) FROM sighting GROUP BY 1")))
    print("IOC feed size (v_feed):", q("SELECT COUNT(*) FROM v_feed")[0][0], "| by type:", dict(q("SELECT type, COUNT(*) FROM v_feed GROUP BY 1")))
    print("feed events:", q("SELECT COUNT(*), MAX(seq) FROM feed_event")[0][:])

def main():
    ap = argparse.ArgumentParser(prog="sgintel"); sp = ap.add_subparsers(dest="cmd", required=True)
    for c in ("init", "load", "catalog", "daemon", "dedup", "stats", "check", "proxy", "roles", "targets", "sites", "output"): sp.add_parser(c)
    p = sp.add_parser("cycle"); p.add_argument("--followup", type=int)
    p = sp.add_parser("followup"); p.add_argument("--limit", type=int, default=followup.PER_RUN)
    p = sp.add_parser("crawl"); p.add_argument("--limit", type=int); p.add_argument("--tier"); p.add_argument("--source")
    p = sp.add_parser("liveness"); p.add_argument("--limit", type=int); p.add_argument("--policy", default="P1", choices=["P1", "P0"])
    p.add_argument("--scope", default="all", choices=["all", "listing"]); p.add_argument("--workers", type=int, default=8); p.add_argument("-v", action="store_true")
    p = sp.add_parser("import"); p.add_argument("--source", required=True); p.add_argument("--file", required=True)
    p = sp.add_parser("export"); p.add_argument("--since", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "proxy":
        from . import egress_proxy; egress_proxy.main(); return
    con = db.connect()
    if a.cmd != "init": db.migrate(con)
    if a.cmd == "init": db.init(con); print("initialised", db.DB_PATH)
    elif a.cmd == "roles": print(roles.refresh(con))
    elif a.cmd == "targets": print(target.resolve(con))
    elif a.cmd == "followup": print(followup.run(con, a.limit, verbose=True))
    elif a.cmd == "cycle": print(crawler.post_crawl(con, followup_limit=a.followup))
    elif a.cmd == "sites": print(sitesrep.report(con))
    elif a.cmd == "output":
        from . import output; print(output.emit(con))
    elif a.cmd == "load": db.init(con); n = catalog.load(con); print("sources loaded:", n, "| dedup:", dedup.run(con)); print(dict(catalog_report(con)))
    elif a.cmd == "catalog": print(dict(catalog_report(con)))
    elif a.cmd == "crawl": crawler.crawl(con, a.limit, a.tier, a.source)
    elif a.cmd == "daemon": crawler.daemon(con)
    elif a.cmd == "liveness":
        liveness.schedule_new(con); rows = liveness.due(con, a.limit, a.scope)
        out = liveness.run(con, rows, a.policy, a.workers, a.v)
        if rows:
            from . import output; output.emit(con, {"kind": "liveness", "checked": len(rows), "results": out})
        print("checked", len(rows), "|", dict(Counter({b: 0 for b, _ in out}) | Counter({b: sum(n for (bb, _), n in out.items() if bb == b) for b, _ in out})))
        for (b, why), n in sorted(out.items(), key=lambda x: -x[1]): print(f"  {b:12} {why:30} {n}")
    elif a.cmd == "dedup": print(dedup.run(con))
    elif a.cmd == "export":
        for r in con.execute("SELECT * FROM feed_event WHERE seq>? ORDER BY seq", (a.since,)):
            sys.stdout.write(json.dumps({**dict(r), "changed_fields": json.loads(r["changed_fields"] or "[]"), "snapshot": json.loads(r["snapshot"] or "null")}, ensure_ascii=False) + "\n")
    elif a.cmd == "stats": stats(con)
    elif a.cmd == "check":   # integrity assertions: every one must be 0
        checks = {
          "dup indicator (type,value)": "SELECT COUNT(*) FROM (SELECT type,value FROM indicator GROUP BY 1,2 HAVING COUNT(*)>1)",
          "dup indicator after normalisation (case/www/trailing-dot)": "SELECT COUNT(*) FROM (SELECT type, lower(trim(replace(value,'://www.','://'),'.')) v FROM indicator GROUP BY 1,2 HAVING COUNT(*)>1)",
          "dup sighting (source,report,indicator)": "SELECT COUNT(*) FROM (SELECT source_id,IFNULL(report_id,''),indicator_id FROM sighting GROUP BY 1,2,3 HAVING COUNT(*)>1)",
          "dup report (source,native_id)": "SELECT COUNT(*) FROM (SELECT source_id,native_id FROM report GROUP BY 1,2 HAVING COUNT(*)>1)",
          "dup endpoint url": "SELECT COUNT(*) FROM (SELECT url FROM endpoint GROUP BY 1 HAVING COUNT(*)>1)",
          "dup source url": "SELECT COUNT(*) FROM (SELECT lower(url) FROM source GROUP BY 1 HAVING COUNT(*)>1)",
          "indicator id != hash(type,value)": None,
          "orphan sighting (no indicator/source)": "SELECT COUNT(*) FROM sighting s LEFT JOIN indicator i USING(indicator_id) LEFT JOIN source src USING(source_id) WHERE i.indicator_id IS NULL OR src.source_id IS NULL",
          "indicator with no sighting": "SELECT COUNT(*) FROM indicator WHERE indicator_id NOT IN (SELECT indicator_id FROM sighting)",
          "allowlisted value emitted on feed": "SELECT COUNT(*) FROM v_feed f JOIN entity_official o ON o.kind IN ('domain','host') AND o.value IN (f.value, f.hostname)",
          # SCOPE.md §8 acceptance checks
          "site without a publication link": "SELECT COUNT(*) FROM v_site_status WHERE publications IS NULL OR publications='[]' OR publications='[null]'",
          "site with >1 primary target": "SELECT COUNT(*) FROM (SELECT indicator_id FROM indicator_entity WHERE is_primary=1 GROUP BY 1 HAVING COUNT(*)>1)",
          "site without a target decision": "SELECT COUNT(*) FROM v_site WHERE impersonation_kind IS NULL",
          "clone/brand_abuse site without primary target": "SELECT COUNT(*) FROM v_site_status WHERE impersonation_kind IN ('clone','brand_abuse') AND target_entity_id IS NULL",
          "authentic host in the site set": "SELECT COUNT(*) FROM v_site v JOIN entity_official o ON o.kind IN ('domain','host') AND (o.value=v.hostname OR (o.value=v.registrable_domain AND v.is_shared_platform=0))",
          "site bucket without evidence row": "SELECT COUNT(*) FROM indicator i WHERE site_bucket IS NOT NULL AND NOT EXISTS (SELECT 1 FROM liveness_check c WHERE c.indicator_id=i.indicator_id AND c.bucket IS NOT NULL)",
          "site never checked >1h after listing": "SELECT COUNT(*) FROM v_site WHERE site_bucket IS NULL AND next_check_at < strftime('%Y-%m-%dT%H:%M:%SZ','now','-1 hour')",
        }
        from .normalize import ind_id
        bad = 0
        for name, q in checks.items():
            n = sum(1 for r in con.execute("SELECT indicator_id,type,value FROM indicator") if ind_id(r[1], r[2]) != r[0]) if q is None else con.execute(q).fetchone()[0]
            bad += bool(n); print(f"  {'OK ' if n == 0 else 'FAIL'} {name}: {n}")
        print("cross-source review queues:", {"report_dup": con.execute("SELECT COUNT(*) FROM v_report_dup").fetchone()[0],
              "official_conflict": con.execute("SELECT COUNT(*) FROM v_official_conflict").fetchone()[0]})
        sys.exit(1 if bad else 0)
    elif a.cmd == "import":   # operator-supplied snapshot for sources whose automated polling is disallowed (e.g. robots.txt)
        from . import ingest
        from .parsers.core import PARSERS
        src = dict(con.execute("SELECT * FROM source WHERE source_id=?", (a.source,)).fetchone())
        ep = dict(con.execute("SELECT * FROM endpoint WHERE endpoint_id=?", (src["endpoint_id"],)).fetchone()); ep["params"] = json.loads(ep["params"] or "{}")
        res = PARSERS[ep["parser"]](open(a.file, "rb").read(), src, ep)
        print("imported", ingest.apply(con, src, ep, res, ingest.Ctx(con))); con.commit()

if __name__ == "__main__": main()
