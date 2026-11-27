"""Derived indicator lifecycle (SCHEMA.md §4) computed from sightings + liveness, with feed_event emission."""
import json, datetime as dt
from .normalize import iso, parse_ts, now

TTL_DAYS = {"url": 30, "hostname": 90, "domain": 90, "ipv4": 14, "ipv6": 14, "phone": 180, "email": 180, "entity_name": 365}
CHECKABLE = {"url", "hostname", "domain"}
AUTH_CONF = {"authoritative": 90, "regulator": 90, "industry": 75, "commercial": 70, "community": 60, "academic": 50}
EVENT_FIELDS = ("status", "valid_until", "liveness_state", "confidence", "revoked")

def recompute(con, indicator_id, t=None):
    t = t or now()
    ind = con.execute("SELECT * FROM indicator WHERE indicator_id=?", (indicator_id,)).fetchone()
    sig = con.execute("""SELECT s.*, src.lifecycle_semantics sem, src.authority auth FROM sighting s
                         JOIN source src USING(source_id) WHERE indicator_id=?""", (indicator_id,)).fetchall()
    if not ind or not sig: return
    roles = {s["role"] for s in sig}
    allow = con.execute("""SELECT 1 FROM entity_official WHERE kind IN ('domain','host','email','hotline')
                           AND value IN (?,?,?) LIMIT 1""", (ind["value"], ind["hostname"] or "", ind["registrable_domain"] or "")).fetchone() \
        or any(s["role"] == "official" and s["sem"] is not None and con.execute("SELECT sg_scope FROM source WHERE source_id=?", (s["source_id"],)).fetchone()[0] == "allowlist" for s in sig)
    ioc = [s for s in sig if s["role"] == "ioc"]
    firsts = [s["source_first_seen"] or s["first_ingested_at"] for s in sig]
    lasts = []
    for s in sig:   # presence in a snapshot_full source is NOT freshness; active_list presence is
        live_presence = s["last_ingested_at"] if s["sem"] == "active_list" and not s["removed_at"] else None
        lasts.append(s["source_last_seen"] or live_presence or s["source_first_seen"] or s["first_ingested_at"])
    first_seen, last_seen = min(firsts), max(lasts)
    srcs = {s["source_id"]: s["auth"] for s in (ioc or sig)}
    conf = min(100, max(AUTH_CONF.get(a, 50) for a in srcs.values()) + 5 * (len(srcs) - 1))
    anchor = max(x for x in (last_seen, ind["last_live_at"]) if x)
    vu = parse_ts(anchor) + dt.timedelta(days=TTL_DAYS.get(ind["type"], 90))
    lv, reg_exp = ind["liveness_state"] or ("unknown" if ind["type"] in CHECKABLE else "not_applicable"), parse_ts(ind["registration_expires_at"])
    revoked = bool(ioc) and all(s["removed_at"] for s in ioc if s["sem"] == "snapshot_full") and any(s["sem"] == "snapshot_full" for s in ioc)
    if allow or (not ioc and "official" in roles): st, why = "allowlisted", "matches official channel"
    elif not ioc: st, why = "unverified", "no ioc sighting (role unknown/mention) — not on IOC feed"
    elif revoked: st, why = "revoked", "authoritative source withdrew it"
    elif lv == "live": st, why = "active", f"site {ind['site_bucket']}: {ind['site_reason']}" if "site_bucket" in ind.keys() and ind["site_bucket"] else "liveness=live"
    elif lv in ("dead", "parked", "suspended", "sinkholed", "blocked"):
        dropped = reg_exp and t > reg_exp + dt.timedelta(days=45)
        held = "hold" in (ind["registry_status"] or "").lower()
        site = f"taken down: {ind['site_reason']}" if "site_reason" in ind.keys() and ind["site_reason"] else f"liveness={lv}"
        st, why = ("expired", "registration lapsed") if dropped else ("inactive", "registrar hold (takedown)" if held else site)
    elif lv == "not_applicable": st, why = ("active", "uncheckable type; within TTL") if t <= vu else ("expired", "uncheckable type; TTL elapsed")
    else: st, why = ("unverified", "not yet checked / inconclusive") if t <= vu else ("expired", "no activity evidence within TTL")
    new = {"status": st, "status_reason": why, "first_seen": first_seen, "last_seen": last_seen, "valid_until": iso(vu),
           "confidence": conf, "revoked": int(revoked), "liveness_state": lv,
           "first_reported_at": min((s["source_first_seen"] for s in ioc if s["auth"] in ("authoritative", "regulator") and s["source_first_seen"]), default=None)}
    changed = [k for k in new if (ind[k] if k in ind.keys() else None) != new[k]]
    if not changed: return
    ev = [k for k in changed if k in EVENT_FIELDS]
    ver = ind["version"] + (1 if ev else 0)
    con.execute(f"UPDATE indicator SET {', '.join(k + '=?' for k in new)}, version=?, updated_at=? WHERE indicator_id=?",
                (*new.values(), ver, iso(t), indicator_id))
    if ev and st != "allowlisted" and ioc:
        emit(con, "status_change" if "status" in ev and ind["status"] != st else "upsert", indicator_id, ver, ev, ind["status"], t)

def snapshot(con, indicator_id):
    i = dict(con.execute("SELECT * FROM indicator WHERE indicator_id=?", (indicator_id,)).fetchone())
    rel = con.execute("SELECT entity_id, relation FROM indicator_entity WHERE indicator_id=?", (indicator_id,)).fetchall()
    cats = [r[0] for r in con.execute("SELECT category FROM indicator_category WHERE indicator_id=?", (indicator_id,))]
    srcs = con.execute("""SELECT DISTINCT s.source_id, s.report_id, r.url, r.published_at, src.publisher_entity_id FROM sighting s
                          JOIN source src USING(source_id) LEFT JOIN report r USING(report_id) WHERE s.indicator_id=? AND s.role='ioc'""", (indicator_id,)).fetchall()
    keep = ("indicator_id", "type", "value", "value_defanged", "registrable_domain", "block_scope", "status", "status_reason", "first_seen",
            "last_seen", "valid_until", "confidence", "liveness_state", "last_checked_at", "last_live_at", "registration_expires_at")
    keep += tuple(k for k in ("impersonation_kind", "site_bucket", "site_reason", "site_flag", "bucket_since") if k in i)
    out = {k: i[k] for k in keep}
    out |= {"categories": cats, "impersonated_entity_ids": sorted({r[0] for r in rel if r[1] in ("impersonates", "lookalike")}),
            "fictitious_brand_ids": sorted({r[0] for r in rel if r[1] == "fictitious_brand"}),
            "issuer_entity_ids": sorted({s["publisher_entity_id"] for s in srcs if s["publisher_entity_id"]}),
            "sources": [dict(s) for s in srcs], "tlp": "TLP:CLEAR"}
    return out

def emit(con, op, indicator_id, version, changed, prev, t=None):
    con.execute("""INSERT INTO feed_event(emitted_at, op, object_type, object_id, version, changed_fields, previous_status, snapshot)
                   VALUES (?,?,?,?,?,?,?,?)""", (iso(t or now()), op, "indicator", indicator_id, version, json.dumps(changed), prev,
                                               json.dumps(snapshot(con, indicator_id), ensure_ascii=False)))
