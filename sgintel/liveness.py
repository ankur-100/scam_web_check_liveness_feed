"""Impersonating-site liveness (SCOPE.md §5). Each check measures two axes and projects them to Chrome-facing buckets.

  reach : gone | serving | unknown            flag : flagged | clear | not_checked | unknown
  bucket: taken_down   reach=gone (whatever the flag; Safe Browsing listings outlive takedowns)
          flagged      reach=serving and flag=flagged     (bypassable warning, scam behind it)
          live         reach=serving and flag in clear/not_checked
          inconclusive anything else (timeouts, bot challenges, cloaking signs, unconfirmed soft-gone)

Evidence per check -> liveness_check row (dns, rdap, http hops, fingerprint, sb, vantage, policy). Soft "gone" signals
(NXDOMAIN, no address, bare 404/410, 5xx/origin down, refused) need a second observation >=6h later; hard ones
(registry hold/lapse, sinkhole IP, parked/suspended/platform-removed page) count at once.
Policies: P0 = DNS+RDAP(+SB) only; P1 = P0 + contained HTTP probe via the egress proxy (default, decision D1).
"""
import ipaddress, json, threading, urllib.request, datetime as dt, urllib.parse
import concurrent.futures as cf
import dns.resolver, dns.exception
from .normalize import iso, now, parse_ts, h16, EXT
from . import lifecycle, probe, safebrowsing, doh

RES = dns.resolver.Resolver(); RES.lifetime = 8          # fallback only: system resolver filters scam domains on this VM
UA = "sgintel-liveness/0.2 (+research; RDAP)"
SOFT = {"dns_nxdomain", "no_address", "dns_dead_delegation", "http_gone", "origin_down", "connection_refused"}
H, D = dt.timedelta(hours=1), dt.timedelta(days=1)
CONFIRM_GAP, ARCHIVE_AFTER, FIRST_WEEK = 6 * H, 90 * D, 7 * D
BUCKET_TO_LV = {"live": "live", "flagged": "live", "taken_down": "dead", "inconclusive": "unknown"}
EVENT = {"taken_down": "site.taken_down", "flagged": "site.flagged", "live": "site.live"}
BENIGN_REDIRECT = probe.BENIGN_REDIRECT
SINKHOLE_IPS = {"8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "9.9.9.9", "149.112.112.112", "208.67.222.222", "208.67.220.220"}   # public resolvers used as takedown targets
_rdap_cache, _rdap_gate = {}, threading.Semaphore(2)


def rdap(reg):
    if reg in _rdap_cache: return _rdap_cache[reg]
    with _rdap_gate:
        try:
            req = urllib.request.Request(f"https://rdap.org/domain/{reg}", headers={"Accept": "application/rdap+json", "User-Agent": UA})
            j = json.load(urllib.request.urlopen(req, timeout=20))
            ev = {e.get("eventAction"): e.get("eventDate") for e in j.get("events", [])}
            r = {"status": j.get("status", []), "registered_at": ev.get("registration"), "expires_at": ev.get("expiration"), "error": None}
        except Exception as e:
            r = {"status": [], "registered_at": None, "expires_at": None, "error": f"{type(e).__name__}: {str(e)[:80]}"}
    _rdap_cache[reg] = r; return r


def dns_lookup(host):
    """DoH first (system resolver filters scam domains on this VM - see doh.py); system resolver only if DoH is unreachable."""
    d = doh.resolve(host)
    if d["rcode"] != "DOH_ERROR": return d
    return {**_system_lookup(host), "doh_error": d["comment"]}


def _system_lookup(host):
    d = {"resolver": "system", "rcode": "NOERROR", "a": [], "aaaa": []}
    for rt, key in (("A", "a"), ("AAAA", "aaaa")):
        try: d[key] = sorted(r.to_text() for r in RES.resolve(host, rt))
        except dns.resolver.NXDOMAIN: d["rcode"] = "NXDOMAIN"; return d
        except dns.resolver.NoAnswer: pass
        except dns.exception.Timeout:
            if key == "a": d["rcode"] = "TIMEOUT"; return d
        except dns.resolver.NoNameservers: d["rcode"] = "SERVFAIL"; return d
        except Exception as e: d["rcode"] = "SERVFAIL"; d["error"] = str(e)[:80]; return d
    if not d["a"] and not d["aaaa"]: d["rcode"] = "NODATA"
    return d


def _global(ip):
    try: a = ipaddress.ip_address(ip)
    except ValueError: return True
    return a.is_global and not a.is_multicast


def observe(ind, policy):
    """Network only (thread-safe, no DB). -> dict(dns, rdap, pre, probe)"""
    o = {"dns": dns_lookup(ind["hostname"]), "rdap": None, "probe": None}
    if not ind["is_shared_platform"]: o["rdap"] = rdap(ind["registrable_domain"])
    st = {s.replace(" ", "").lower() for s in (o["rdap"] or {}).get("status") or []}
    rc = o["dns"]["rcode"]; addrs = o["dns"]["a"] + o["dns"]["aaaa"]
    o["pre"] = ("registry_hold" if st & {"clienthold", "serverhold"} else "registration_lapsed" if st & {"redemptionperiod", "pendingdelete"}
                else "sinkhole_ip" if any(not _global(a) or a in SINKHOLE_IPS for a in addrs) else "dns_nxdomain" if rc == "NXDOMAIN" else "no_address" if rc == "NODATA"
                else "dns_dead_delegation" if rc == "SERVFAIL" and o["dns"].get("dead_delegation")
                else "dns_timeout" if rc == "TIMEOUT" else "dns_servfail" if rc == "SERVFAIL" or rc.startswith("RCODE_") else None)
    if o["pre"] is None and policy == "P1":
        try: o["probe"] = probe.probe(ind["value"], ind["type"])
        except Exception as e: o["probe"] = {"attempts": [], "used": None, "tls": "unknown", "fp": None, "crash": f"{type(e).__name__}: {str(e)[:120]}"}
    return o


def classify(o, ind, cx):
    """-> (reach in gone|gone_soft|serving|unknown, reason code, probe-level flag code or None)"""
    pre = o["pre"]
    if pre in ("registry_hold", "registration_lapsed", "sinkhole_ip"): return "gone", pre, None
    if pre in ("dns_nxdomain", "no_address", "dns_dead_delegation"): return "gone_soft", pre, None
    if pre: return "unknown", pre, None
    p = o["probe"]
    if p is None: return "unknown", "http_not_probed", None
    if p.get("crash"): return "unknown", "probe_crash", None
    if p["used"] is None:
        hops = [h for a in p["attempts"] for h in a["hops"]]; errs = [h["error"] for h in hops if h.get("error")]
        stops = {a.get("stop") for a in p["attempts"]}
        blocked = [h for h in hops if h.get("error") == "egress_blocked"]
        if blocked: return ("gone", "sinkhole_ip", None) if "non_global_ip" in (blocked[0].get("detail") or "") else ("unknown", "egress_blocked", None)
        if "dns_nxdomain" in errs: return "gone_soft", "dns_nxdomain", None
        if "dns_error" in errs: return "unknown", "dns_error_at_proxy", None
        if "redirect_loop" in stops or "redirect_loop" in errs: return "unknown", "redirect_loop", None
        if "non_http_redirect" in stops: return "unknown", "non_http_redirect", None
        if errs and set(errs) <= {"connection_refused", "connection_reset"}: return "gone_soft", "connection_refused", None
        if "timeout" in errs: return "unknown", "timeout", None
        if "tls_handshake_failed" in errs: return "unknown", "tls_handshake_failed", None
        return "unknown", (errs[0] if errs else "no_response"), None
    a = p["attempts"][p["used"]]; fin = a["final"]; fp = p["fp"]; st = fin["status"]; sig = set(fp["sig"])
    tls_flag = None if a["verify"] else "tls_invalid"
    hosts = [(urllib.parse.urlsplit(h["url"]).hostname or "").lower().removeprefix("www.") for h in a["hops"]]
    listed = (ind["hostname"] or "").removeprefix("www.")
    if "host_interstitial" in sig: return "serving", "host_interstitial", "host_interstitial"
    if "bot_challenge" in sig: return "unknown", "bot_challenge", None
    if "seized" in sig: return "gone", "seized", None                                   # law-enforcement seizure banner
    if "origin_down" in sig or st in (521, 522, 523, 530): return "gone_soft", "origin_down", None   # CDN up, origin gone
    if "default_page" in sig:
        return "gone", ("sinkhole_ip" if "google public dns" in (fp["title"] or "").lower() else "server_default_page"), None
    for g in ("parked_or_for_sale", "host_suspended"):
        if g in sig: return "gone", g, None
    if "platform_removed" in sig and (st >= 400 or ind["is_shared_platform"]): return "gone", "platform_removed", None
    if any(cx.official_owner(h, h) for h in hosts[1:] if h != listed): return "unknown", "redirect_to_authentic", None
    fin_reg = EXT(hosts[-1]).top_domain_under_public_suffix if hosts[-1] else None
    if hosts[-1] != listed and fin_reg in BENIGN_REDIRECT: return "unknown", "redirect_offsite_benign", None
    if st in (404, 410, 451): return "gone_soft", "http_gone", None
    if st in (401, 403): return "unknown", "geo_or_ip_block", None
    if st == 429: return "unknown", "rate_limited", None
    if st >= 500: return "gone_soft", "origin_down", None
    if 200 <= st < 300:
        if fp["bytes"] < 64: return "unknown", "empty_response", None
        if fp["bytes"] < 512 and not fp["text_chars"] and not fp["title"] and not fp.get("has_form"):
            return "unknown", "script_stub", None          # JS-only stub we do not execute (cloaking or JS redirect)
        return "serving", ("serving" if hosts[-1] == listed else "serving_via_redirect"), tls_flag
    return "unknown", f"http_{st}", None


def next_check(bucket, reason, streak, first_listed, last_live, t):
    if reason and reason.endswith("_unconfirmed"): return t + CONFIRM_GAP
    fl = parse_ts(first_listed) or t
    if bucket in ("live", "flagged"): return t + (6 * H if t - fl < FIRST_WEEK else D)
    if bucket == "taken_down":
        if t - (parse_ts(last_live) or fl) > ARCHIVE_AFTER: return None          # archived; resurrection watch ends
        return t + (D, 3 * D, 7 * D)[min(streak, 3) - 1]
    return t + (H, 6 * H, D)[min(streak, 3) - 1]


def site_event(con, iid, event, prev, t=None):
    row = con.execute("SELECT * FROM v_site_status WHERE indicator_id=?", (iid,)).fetchone()
    snap = dict(row) if row else {"indicator_id": iid}
    for k in ("authentic_hosts", "other_brands", "publications", "publishers", "listing_roles"):
        if isinstance(snap.get(k), str): snap[k] = json.loads(snap[k])
    ver = (con.execute("SELECT version FROM indicator WHERE indicator_id=?", (iid,)).fetchone() or [1])[0]
    con.execute("""INSERT INTO feed_event(emitted_at, op, object_type, object_id, version, changed_fields, previous_status, snapshot, event)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (t or iso(now()), "upsert" if event == "site.listed" else "status_change", "site", iid, ver,
                 json.dumps(["target"] if event == "site.target_changed" else ["site_bucket"]), prev, json.dumps(snap, ensure_ascii=False), event))


def schedule_new(con, t=None):
    """New sites in v_site: stamp first_listed_at, queue an immediate first check, emit site.listed."""
    T = iso(t or now()); n = 0
    for (iid,) in con.execute("SELECT indicator_id FROM v_site WHERE first_listed_at IS NULL").fetchall():
        fl = con.execute("""SELECT MIN(s.first_ingested_at) FROM sighting s JOIN source src USING(source_id)
                            WHERE s.indicator_id=? AND s.role='ioc' AND src.listing_role IN ('listing','adjacent')""", (iid,)).fetchone()[0] or T
        con.execute("UPDATE indicator SET first_listed_at=?, next_check_at=COALESCE(next_check_at, ?) WHERE indicator_id=?", (fl, T, iid))
        site_event(con, iid, "site.listed", None, T); n += 1
    con.commit(); return n


def due(con, limit=None, scope="all", t=None):
    q = """SELECT v.*, (SELECT MIN(CASE src.listing_role WHEN 'listing' THEN 0 ELSE 1 END) FROM sighting s JOIN source src USING(source_id)
                        WHERE s.indicator_id=v.indicator_id AND s.role='ioc' AND src.listing_role IN ('listing','adjacent')) AS prio
           FROM v_site v WHERE v.next_check_at IS NOT NULL AND v.next_check_at <= ?"""
    rows = [dict(r) for r in con.execute(q, (iso(t or now()),)).fetchall()]
    if scope == "listing": rows = [r for r in rows if r["prio"] == 0]
    rows.sort(key=lambda r: (r["prio"], r["site_bucket"] is not None, r["next_check_at"]))
    return rows[:limit] if limit else rows


def _write(con, ind, o, policy, vant, sbres, cx, t):
    T = iso(t); iid = ind["indicator_id"]
    reach, code, pflag = classify(o, ind, cx)
    if reach == "gone_soft":
        prev = con.execute("SELECT reach, reason, checked_at FROM liveness_check WHERE indicator_id=? AND bucket IS NOT NULL ORDER BY checked_at DESC LIMIT 1", (iid,)).fetchone()
        already = prev and prev["reach"] == "gone" and prev["reason"] in SOFT
        pending = prev and (prev["reason"] or "").endswith("_unconfirmed") and t - parse_ts(prev["checked_at"]) >= CONFIRM_GAP
        reach, code = ("gone", code) if (already or pending) else ("unknown", code + "_unconfirmed")
    sb_url = safebrowsing.lookup_url(ind["value"], ind["type"]); sb = sbres.get(sb_url)
    freasons = [safebrowsing.REASON.get(x, "sb_" + x.lower()) for x in (sb or {}).get("threats", [])] + ([pflag] if pflag else [])
    flag = "flagged" if freasons else ("unknown" if sb and sb.get("error") else "clear" if sb is not None else "not_checked")
    if reach == "gone": bucket, reason = "taken_down", code
    elif reach == "serving" and flag == "flagged": bucket, reason = "flagged", freasons[0]
    elif reach == "serving" and flag in ("clear", "not_checked"): bucket, reason = "live", code
    else: bucket, reason = "inconclusive", (code if reach != "serving" else "sb_error")
    prev_b = ind["site_bucket"]
    streak = (ind["bucket_streak"] or 0) + 1 if prev_b == bucket else 1
    last_live = T if reach == "serving" else ind["last_live_at"]
    nxt = next_check(bucket, code if reach == "unknown" else reason, streak, ind["first_listed_at"], last_live, t)
    p = o["probe"] or {}
    fpj = {"reach_code": code, "flag_reasons": freasons, "tls": p.get("tls"), **(p.get("fp") or {})}
    rd = o["rdap"]
    con.execute("""INSERT OR REPLACE INTO liveness_check(check_id, indicator_id, checked_at, vantage, dns, rdap, http, fingerprints, verdict,
                   reach, flag, bucket, reason, sb, probe_policy) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (f"chk_{h16(iid + T + policy)}", iid, T, vant, json.dumps(o["dns"]), json.dumps(rd), json.dumps(p.get("attempts")) if p else None,
                 json.dumps(fpj), bucket, reach, flag, bucket, reason, json.dumps(sb) if sb is not None else None, policy))
    con.execute("""UPDATE indicator SET site_bucket=?, site_reason=?, site_reach=?, site_flag=?, bucket_streak=?, next_check_at=?,
                   bucket_since=CASE WHEN site_bucket IS ? THEN bucket_since ELSE ? END, last_checked_at=?, last_live_at=?,
                   liveness_state=?, liveness_since=CASE WHEN liveness_state IS ? THEN liveness_since ELSE ? END,
                   consecutive_failures=CASE WHEN ?='serving' THEN 0 ELSE consecutive_failures+1 END,
                   registration_expires_at=COALESCE(?, registration_expires_at), registry_status=COALESCE(?, registry_status) WHERE indicator_id=?""",
                (bucket, reason, reach, flag, streak, iso(nxt) if nxt else None, bucket, T, T, last_live, BUCKET_TO_LV[bucket], BUCKET_TO_LV[bucket], T,
                 reach, (rd or {}).get("expires_at"), json.dumps(rd["status"]) if rd and rd["status"] else None, iid))
    ev = "site.resurrected" if prev_b == "taken_down" and bucket in ("live", "flagged") else (EVENT.get(bucket) if bucket != prev_b else None)
    if ev: site_event(con, iid, ev, prev_b, T)
    lifecycle.recompute(con, iid, t)
    return bucket, reason


def run(con, rows, policy="P1", workers=8, verbose=False):
    """Check the given v_site rows. Fail-closed: P1 refuses to run without the egress proxy."""
    from .ingest import Ctx
    if policy == "P1" and not probe.proxy_alive():
        raise SystemExit(f"egress proxy not reachable at {probe.PROXY} - start it with `python -m sgintel proxy` (no direct probes)")
    cx, t = Ctx(con), now()
    vant = (probe.vantage() if policy == "P1" else "no-http") + "|" + doh.RESOLVER
    sbres = safebrowsing.lookup([safebrowsing.lookup_url(r["value"], r["type"]) for r in rows])
    out = {}
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(observe, r, policy): r for r in rows}
        for i, f in enumerate(cf.as_completed(futs), 1):
            r = futs[f]
            try: o = f.result()
            except Exception as e: o = {"dns": {"rcode": "ERROR", "error": str(e)[:80], "a": [], "aaaa": []}, "rdap": None, "pre": "observe_error", "probe": None}
            b, why = _write(con, r, o, policy, vant, sbres, cx, now())
            out[(b, why)] = out.get((b, why), 0) + 1
            if verbose: print(f"  {b:12} {why:28} {r['value_defanged'][:70]}", flush=True)
            if i % 20 == 0: con.commit()
    con.commit()
    return out
