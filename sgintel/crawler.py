"""Rolling scheduler over `endpoint`: due-first queue, adaptive intervals, per-host politeness (fetch.py)."""
import json, random, time, datetime as dt
from .normalize import iso, now, parse_ts, sha256
from . import fetch, ingest
from .parsers.core import PARSERS

PRIORITY = {"hot": 0, "daily": 1, "weekly": 2, "monthly": 3, "manual": 9}
MAX_ERRORS = 6

def due(con, limit=None, tier=None, source=None):
    q = "SELECT * FROM endpoint WHERE enabled=1 AND (next_due_at IS NULL OR next_due_at<=?)"; a = [iso(now())]
    if tier: q += " AND tier=?"; a.append(tier)
    if source: q += " AND endpoint_id IN (SELECT endpoint_id FROM source WHERE source_id=?)"; a.append(source)
    rows = sorted(con.execute(q, a).fetchall(), key=lambda r: (PRIORITY[r["tier"]], r["next_due_at"] or ""))
    return rows[:limit] if limit else rows

def schedule(con, ep, changed, error):
    iv = ep["interval_s"]
    if error: iv = min(ep["max_interval_s"], iv * 2)
    elif changed: iv = max(ep["min_interval_s"], iv // 2)
    else: iv = min(ep["max_interval_s"], int(iv * 1.5))
    nxt = now() + dt.timedelta(seconds=iv * random.uniform(0.9, 1.1))
    return iv, iso(nxt)

def run_endpoint(con, ep, cx):
    ep = dict(ep); ep["params"] = json.loads(ep["params"]) if ep["params"] else {}
    srcs = [dict(r) for r in con.execute("SELECT * FROM source WHERE endpoint_id=? OR source_id=?", (ep["endpoint_id"], ep["params"].get("source_id", "")))]
    t0 = now(); log = {"http_status": None, "bytes": 0, "sha256": None, "changed": 0, "error": None, "n_reports": 0, "n_indicators": 0}
    if not fetch.robots_ok(ep["url"]):
        con.execute("UPDATE endpoint SET enabled=0, disabled_reason='robots.txt disallow' WHERE endpoint_id=?", (ep["endpoint_id"],))
        log["error"] = "robots.txt disallow"
    else:
        req_params = None
        if ep["parser"] == "phishstats":
            kws = ep["params"]["keywords"]; cur = ep["params"].get("cursor", 0) % len(kws)
            req_params = {"_where": f"(url,like,~{kws[cur]}~)", "_sort": "-id", "_size": ep["params"].get("page_size", 50)}
            ep["params"]["cursor"] = cur + 1
        r = fetch.get(ep["url"], ep["etag"], ep["last_modified"], params=req_params)
        log.update(http_status=r["status"], bytes=len(r["body"]), error=r["error"])
        if r["status"] == 304: pass
        elif r["status"] and 200 <= r["status"] < 300 and r["body"]:
            h = sha256(r["body"]); log["sha256"] = h
            if h != ep["last_sha256"] or ep["parser"] == "phishstats":
                log["changed"] = 1
                try:
                    res = PARSERS[ep["parser"]](r["body"], srcs[0] if srcs else {"url": ep["url"], "name": ep["url"]}, ep)
                    for child in res["state"].get("children", []):   # sitemap index -> child sitemaps inherit the discovery source
                        con.execute("""INSERT OR IGNORE INTO endpoint(url,host,fetch_kind,parser,tier,interval_s,min_interval_s,max_interval_s,next_due_at,params)
                                       VALUES (?,?,?,?,?,?,?,?,?,?)""", (child, ep["host"], "sitemap", "sitemap", ep["tier"], ep["interval_s"], ep["min_interval_s"],
                                       ep["max_interval_s"], iso(now()), json.dumps({**ep["params"], "source_id": srcs[0]["source_id"] if srcs else None})))
                    for s in srcs:
                        nr, ni = ingest.apply(con, s, ep, res, cx); log["n_reports"] += nr; log["n_indicators"] += ni
                except Exception as e:
                    log["error"] = f"parse: {type(e).__name__}: {str(e)[:200]}"; log["changed"] = 0
            con.execute("UPDATE endpoint SET etag=?, last_modified=?, last_sha256=? WHERE endpoint_id=?", (r.get("etag"), r.get("last_modified"), h, ep["endpoint_id"]))
        elif not log["error"]:
            log["error"] = f"HTTP {r['status']}"
    err = bool(log["error"]); iv, nxt = schedule(con, ep, log["changed"], err)
    con.execute("""UPDATE endpoint SET interval_s=?, next_due_at=?, last_fetched_at=?, params=?,
                   last_changed_at=CASE WHEN ? THEN ? ELSE last_changed_at END,
                   consecutive_unchanged=CASE WHEN ? THEN 0 ELSE consecutive_unchanged+1 END,
                   consecutive_errors=CASE WHEN ? THEN consecutive_errors+1 ELSE 0 END WHERE endpoint_id=?""",
                (iv, nxt, iso(t0), json.dumps(ep["params"]) if ep["params"] else None, log["changed"], iso(t0), log["changed"], err, ep["endpoint_id"]))
    con.execute("UPDATE endpoint SET enabled=0, disabled_reason='too many errors: '||? WHERE endpoint_id=? AND consecutive_errors>=?",
                (log["error"] or "", ep["endpoint_id"], MAX_ERRORS))
    con.execute("INSERT INTO fetch_log(endpoint_id,started_at,http_status,bytes,sha256,changed,duration_ms,error,n_reports,n_indicators) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (ep["endpoint_id"], iso(t0), log["http_status"], log["bytes"], log["sha256"], log["changed"], int((now() - t0).total_seconds() * 1000),
                 log["error"], log["n_reports"], log["n_indicators"]))
    con.commit()
    return log

def crawl(con, limit=None, tier=None, source=None, verbose=True):
    cx = ingest.Ctx(con); out = []
    for ep in due(con, limit, tier, source):
        log = run_endpoint(con, ep, cx); out.append(log)
        if verbose: print(f"  [{ep['tier']:7}] {ep['parser']:17} {str(log['http_status']):4} chg={log['changed']} rep+{log['n_reports']:<4} ind+{log['n_indicators']:<5} "
                          f"{(log['error'] or '')[:40]:40} {ep['url'][:80]}", flush=True)
    if out:
        post = post_crawl(con, cx)
        if verbose: print("  post-crawl:", post)
        from . import output
        o = output.emit(con, {"kind": "crawl", "endpoints": len(out), "changed": sum(l["changed"] for l in out),
                              "errors": sum(bool(l["error"]) for l in out), "new_publications": sum(l["n_reports"] for l in out),
                              "followup_fetched": post["followup"]["fetched"], "followup_with_sites": post["followup"]["with_sites"],
                              "new_sites": post["new_sites"]})
        if verbose: print("  output:", o)
    return out

def post_crawl(con, cx=None, followup_limit=None):
    """SCOPE.md cycle: self-heal dedup -> source roles -> fetch newly discovered publications -> targets -> queue new sites."""
    from . import dedup, roles, followup, target, liveness
    out = {"dedup": dedup.merge_indicators(con), "roles": roles.refresh(con)}
    out["followup"] = followup.run(con, followup_limit or followup.PER_RUN, cx)
    if out["followup"]["with_sites"]: out["roles2"] = roles.refresh(con)      # a watched publisher just started listing sites
    out["targets"] = target.resolve(con); out["new_sites"] = liveness.schedule_new(con)
    return out

def daemon(con, max_sleep=60, site_batch=60):
    from . import liveness, probe
    while True:
        crawl(con)
        rows = liveness.due(con, site_batch)
        if rows and probe.proxy_alive():
            from . import output
            res = liveness.run(con, rows); print("  site checks:", res, flush=True)
            output.emit(con, {"kind": "liveness", "checked": len(rows), "results": res})
        elif rows: print(f"  WARNING: {len(rows)} site checks due but egress proxy is down - skipped (fail-closed)", flush=True)
        nxt = con.execute("SELECT MIN(next_due_at) FROM endpoint WHERE enabled=1").fetchone()[0]
        wait = max(5, min(max_sleep, (parse_ts(nxt) - now()).total_seconds())) if nxt else max_sleep
        time.sleep(wait)
