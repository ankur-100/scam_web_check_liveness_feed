"""Rolling file outputs, written after every pipeline run (crawl cycle, liveness run, daemon loop, `sgintel output`).
Contract: schema/site_feed.schema.json (site-feed/1.0).

  out/events/site-events-YYYY-MM-DD.jsonl    append-only SiteEvent lines, filed by event date; resumable by `seq`
  out/snapshots/sites-YYYY-MM-DD.jsonl       every site's SiteRecord, rewritten each run (last write = end-of-day state)
  out/sites-latest.jsonl                     copy of the newest snapshot
  out/reports/run-report-YYYY-MM-DD.txt      append-only, one plain-text block per run

out/.event_cursor holds the last exported seq; a file lock serialises concurrent writers (crawl + liveness processes).
Retention: snapshots 30 days, events and reports 365 days (only files matching these names are ever pruned).
"""
import datetime as dt, fcntl, json, os, re, shutil
from collections import Counter
from .normalize import ROOT, iso, now

SCHEMA_VERSION = "site-feed/1.0"
OUT = ROOT / "out"
RETAIN = {"snapshots": 30, "events": 365, "reports": 365}
STATE = {"taken_down": "a", "flagged": "b", "live": "c"}
ARR = ("authentic_hosts", "other_brands", "publications", "publishers", "listing_roles")
LABEL = {"live": "(c) live", "flagged": "(b) flagged", "taken_down": "(a) taken down", "inconclusive": "inconclusive", None: "unchecked"}


def _arr(v):
    if isinstance(v, list): return v
    if not v: return []
    try: x = json.loads(v); return x if isinstance(x, list) else [x]
    except ValueError: return [v]


def evidence(c):
    if c is None: return None
    dns = json.loads(c["dns"] or "{}"); fp = json.loads(c["fingerprints"] or "{}"); http = json.loads(c["http"] or "null") or []
    fin = next((a["final"] for a in reversed(http) if a.get("final")), None)
    return {"checked_at": c["checked_at"], "vantage": c["vantage"], "probe_policy": c["probe_policy"], "dns_rcode": dns.get("rcode"),
            "resolver": dns.get("resolver"), "addresses": (dns.get("a") or []) + (dns.get("aaaa") or []),
            "http_status": fin.get("status") if fin else None, "final_url": fin.get("url") if fin else None,
            "page_title": (fp.get("title") or None), "tls": fp.get("tls"), "flag_reasons": fp.get("flag_reasons") or [],
            "signatures": fp.get("sig") or [], "sig_version": fp.get("sig_version")}


def site_record(r, ev=None):
    """v_site_status row (or a stored event snapshot of one) -> SiteRecord."""
    r = dict(r); g = r.get
    roles = _arr(g("listing_roles"))
    return {
        "record": "site", "schema_version": SCHEMA_VERSION, "site_id": g("indicator_id"), "type": g("type"), "value": g("value"),
        "value_defanged": g("value_defanged") or "", "hostname": g("hostname") or "", "registrable_domain": g("registrable_domain"),
        "is_shared_platform": bool(g("is_shared_platform")), "listing_role": "listing" if "listing" in roles else "adjacent",
        "impersonation": {"kind": g("impersonation_kind"), "target_entity_id": g("target_entity_id"), "target_name": g("target_name"),
                          "target_method": g("target_method"), "authentic_hosts": _arr(g("authentic_hosts")), "other_brands": _arr(g("other_brands"))},
        "provenance": {"publishers": [p for p in _arr(g("publishers")) if p], "publications": [p for p in _arr(g("publications")) if p],
                       "first_published_at": g("first_published_at"), "first_listed_at": g("first_listed_at")},
        "liveness": {"bucket": g("site_bucket"), "chrome_state": STATE.get(g("site_bucket")), "reason": g("site_reason"), "reach": g("site_reach"),
                     "flag": g("site_flag"), "bucket_since": g("bucket_since"), "consecutive_checks_in_bucket": g("bucket_streak") or 0,
                     "last_checked_at": g("last_checked_at"), "last_live_at": g("last_live_at"), "next_check_at": g("next_check_at"), "evidence": ev},
        "registration": {"registry_status": [s for s in _arr(g("registry_status")) if isinstance(s, str)], "expires_at": g("registration_expires_at")},
        "lifecycle_status": g("status") or "unverified"}


def event_record(e):
    snap = json.loads(e["snapshot"] or "null")
    tc = e["event"] == "site.target_changed"
    return {"record": "event", "schema_version": SCHEMA_VERSION, "seq": e["seq"], "emitted_at": e["emitted_at"], "event": e["event"],
            "site_id": e["object_id"], "previous": e["previous_status"],
            "current": (snap or {}).get("target_entity_id" if tc else "site_bucket"),
            "site": site_record(snap) if snap and snap.get("type") else None}


def _day(ts): return (ts or iso(now()))[:10]


def _prune():
    pat = {"snapshots": r"sites-(\d{4}-\d{2}-\d{2})\.jsonl$", "events": r"site-events-(\d{4}-\d{2}-\d{2})\.jsonl$", "reports": r"run-report-(\d{4}-\d{2}-\d{2})\.txt$"}
    cut = {k: (now() - dt.timedelta(days=d)).date().isoformat() for k, d in RETAIN.items()}
    for sub, rx in pat.items():
        for f in (OUT / sub).glob("*"):
            m = re.match(rx, f.name)
            if m and m.group(1) < cut[sub]: f.unlink()


def emit(con, run=None):
    """Flush new site events, rewrite today's snapshot, append a run block to today's text report. Returns a summary."""
    run = run or {"kind": "manual"}
    for sub in ("events", "snapshots", "reports"): (OUT / sub).mkdir(parents=True, exist_ok=True)
    with open(OUT / ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        cur_f = OUT / ".event_cursor"; cursor = int(cur_f.read_text().strip() or 0) if cur_f.exists() else 0
        evs = con.execute("SELECT * FROM feed_event WHERE object_type='site' AND seq>? ORDER BY seq", (cursor,)).fetchall()
        by_day = {}
        for e in evs: by_day.setdefault(_day(e["emitted_at"]), []).append(event_record(e))
        for day, recs in by_day.items():
            with open(OUT / "events" / f"site-events-{day}.jsonl", "a") as f:
                for r in recs: f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
        if evs: cur_f.write_text(str(evs[-1]["seq"]))
        # snapshot
        last = {c["indicator_id"]: c for c in con.execute("""SELECT c.* FROM liveness_check c JOIN (SELECT indicator_id, MAX(checked_at) m FROM liveness_check
                    WHERE bucket IS NOT NULL GROUP BY 1) x ON x.indicator_id=c.indicator_id AND x.m=c.checked_at""")}
        rows = con.execute("SELECT * FROM v_site_status ORDER BY value").fetchall()
        recs = [site_record(r, evidence(last.get(r["indicator_id"]))) for r in rows]
        T = iso(now()); snap = OUT / "snapshots" / f"sites-{_day(T)}.jsonl"; tmp = snap.with_suffix(".tmp")
        with open(tmp, "w") as f:
            for r in recs: f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
        os.replace(tmp, snap); shutil.copyfile(snap, OUT / "sites-latest.jsonl")
        # text report
        block = report_block(con, run, recs, [event_record(e) for e in evs], T)
        with open(OUT / "reports" / f"run-report-{_day(T)}.txt", "a") as f: f.write(block)
        _prune()
    return {"events_written": len(evs), "sites_in_snapshot": len(recs), "snapshot": str(snap.relative_to(ROOT)),
            "report": f"out/reports/run-report-{_day(T)}.txt"}


def report_block(con, run, recs, evs, T):
    L = [f"==== sgintel {run.get('kind', 'run')} run  {T} " + "=" * 30]
    if run.get("kind") == "crawl":
        L.append(f"publishers : {run.get('endpoints', 0)} endpoints fetched, {run.get('changed', 0)} changed, {run.get('errors', 0)} errors | "
                 f"new publications {run.get('new_publications', 0)} | follow-up pages {run.get('followup_fetched', 0)} ({run.get('followup_with_sites', 0)} naming sites) | "
                 f"new sites {run.get('new_sites', 0)}")
    if run.get("checked") is not None:
        c = Counter()
        for (b, _), n in (run.get("results") or {}).items(): c[b] += n
        L.append(f"site checks: {run['checked']} | " + ", ".join(f"{LABEL.get(b, b)} {n}" for b, n in c.items()))
    for role in ("listing", "adjacent"):
        c = Counter(r["liveness"]["bucket"] for r in recs if r["listing_role"] == role)
        pend = sum(1 for r in recs if r["listing_role"] == role and (r["liveness"]["reason"] or "").endswith("_unconfirmed"))
        L.append(f"{role:9}  : {sum(c.values())} sites | (c) live {c['live']} | (b) flagged {c['flagged']} | (a) taken down {c['taken_down']} | "
                 f"inconclusive {c['inconclusive']} (awaiting confirmation {pend}) | unchecked {c[None]}")
    kinds = Counter(e["event"] for e in evs)
    L.append(f"events     : {len(evs)} since last run" + (" (" + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items())) + ")" if evs else ""))
    shown = [e for e in evs if e["event"] != "site.listed" and e["site"] and e["site"]["listing_role"] == "listing"]
    for e in shown[:40]:
        s = e["site"]
        L.append(f"  {e['event']:20} {s['value_defanged'][:48]:48} {str(e['previous']):>12} -> {str(e['current']):<12} "
                 f"{s['liveness']['reason'] or '':24} target={s['impersonation']['target_name'] or s['impersonation']['kind']} "
                 f"by={','.join(s['provenance']['publishers'])}")
    if len(shown) > 40: L.append(f"  ... +{len(shown) - 40} more listing-site transitions (see out/events/)")
    new = [e for e in evs if e["event"] == "site.listed" and e["site"] and e["site"]["listing_role"] == "listing"]
    for e in new[:20]:
        s = e["site"]; L.append(f"  NEW LISTING  {s['value_defanged'][:60]:60} target={s['impersonation']['target_name'] or s['impersonation']['kind']} "
                                f"pub={(s['provenance']['publications'] or ['?'])[0][:90]}")
    nd = con.execute("SELECT COUNT(*) FROM endpoint WHERE enabled=1 AND (next_due_at IS NULL OR next_due_at<=?)", (T,)).fetchone()[0]
    ns = con.execute("SELECT MIN(next_check_at) FROM v_site WHERE next_check_at IS NOT NULL").fetchone()[0]
    L.append(f"next       : publisher endpoints due {nd} | next site check {ns}")
    return "\n".join(L) + "\n\n"
