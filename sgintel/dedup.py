"""Cross-record duplicate detection + conservative auto-merge. Writes data/DEDUP.md."""
import difflib, json
from .normalize import canonical, ind_id
from .db import cols
from . import lifecycle
from collections import defaultdict
from .normalize import ROOT, iso, now

def run(con, write=True):
    mi = merge_indicators(con); mi |= reclassify(con)
    L = [f"Indicator self-heal: {mi}", "", f"# Duplicate / conflict report ({iso(now())})", ""]
    # 1. entities that are the same organisation under two ids (share >=2 official domains, or near-identical programme slugs)
    shared = defaultdict(set)
    for v, e in con.execute("SELECT value, entity_id FROM entity_official WHERE kind='domain'"): shared[v].add(e)
    pairs = defaultdict(int)
    for v, es in shared.items():
        es = sorted(es)
        for i in range(len(es)):
            for j in range(i + 1, len(es)): pairs[(es[i], es[j])] += 1
    merged = []
    par = {e: p for e, p in con.execute("SELECT entity_id, parent_entity_id FROM entity")}
    nsrc = defaultdict(int, {e: n for e, n in con.execute("SELECT publisher_entity_id, COUNT(*) FROM source GROUP BY 1")})
    for (a, b), n in pairs.items():
        related = par.get(a) == b or par.get(b) == a or a.split("#")[0] == b.split("#")[0]
        if n >= 2 and not related:
            keep, drop = sorted((a, b), key=lambda e: (-nsrc[e], len(e)))
            merged.append((drop, keep, f"share {n} official domains"))
    progs = [e for (e,) in con.execute("SELECT entity_id FROM entity WHERE entity_id LIKE '%#%'")]
    for i, a in enumerate(progs):
        for b in progs[i + 1:]:
            if a.split("#")[0] == b.split("#")[0] and difflib.SequenceMatcher(None, a, b).ratio() >= 0.93:
                keep, drop = sorted((a, b), key=lambda e: (-nsrc[e], len(e))); merged.append((drop, keep, "near-identical programme id"))
    for drop, keep, why in merged:
        con.execute("UPDATE entity SET canonical_entity_id=? WHERE entity_id=?", (keep, drop))
        con.execute("INSERT OR IGNORE INTO entity_alias SELECT ?, alias, alias_norm, origin, spf_tag_id FROM entity_alias WHERE entity_id=?", (keep, drop))
    L += ["## 1. Entity duplicates (auto-merged via canonical_entity_id)", ""] + [f"- `{d}` → `{k}` ({w})" for d, k, w in merged] + [""]
    conf = con.execute("SELECT * FROM v_official_conflict").fetchall()
    L += [f"## 2. Allowlist values claimed by unrelated entities: {len(conf)}", ""] + [f"- {r['kind']} `{r['value']}`: {r['a']} / {r['b']}" for r in conf[:40]] + [""]
    dup_src = con.execute("""SELECT lower(replace(replace(url,'https://',''),'www.','')) u, COUNT(*) n FROM source GROUP BY u HAVING n>1""").fetchall()
    L += [f"## 3. Sources with the same URL under different ids: {len(dup_src)} (blocked by UNIQUE(url); IPOS dup from two agents collapsed)", ""]
    shared_ep = con.execute("SELECT url, json_extract(params,'$.refs') n FROM endpoint WHERE json_extract(params,'$.refs')>1 ORDER BY n DESC").fetchall()
    L += [f"## 4. Endpoints referenced by >1 registry page (fetched once): {len(shared_ep)}", ""] + [f"- {r['n']}× {r['url']}" for r in shared_ep[:15]] + [""]
    sc = con.execute("SELECT * FROM v_shared_channel ORDER BY n DESC").fetchall()
    L += [f"## 4b. Legitimately shared official channels (not conflicts): {len(sc)}", ""] + [f"- {r['kind']} `{r['value']}` × {r['n']} entities" for r in sc[:15]] + [""]
    rd = con.execute("""SELECT d.a, d.b, ra.title ta, rb.title tb FROM v_report_dup d JOIN report ra ON ra.report_id=d.a JOIN report rb ON rb.report_id=d.b""").fetchall()
    L += [f"## 5. Same advisory published by two sources (fingerprint match): {len(rd)}", ""] + [f"- {r['a']} ≈ {r['b']}  \n  “{r['ta'][:90]}”" for r in rd[:30]] + [""]
    ic = con.execute("SELECT * FROM v_ioc_conflict").fetchall()
    L += [f"## 6. IOC sightings that hit the allowlist (suppressed as allowlisted): {len(ic)}", ""] + [f"- `{r['value']}` (official: {r['entity_id']})" for r in ic[:30]] + [""]
    gran = con.execute("""SELECT registrable_domain, GROUP_CONCAT(DISTINCT type) t, COUNT(*) n FROM indicator WHERE registrable_domain IS NOT NULL
                          AND indicator_id IN (SELECT indicator_id FROM sighting WHERE role='ioc') GROUP BY 1 HAVING n>1 ORDER BY n DESC LIMIT 15""").fetchall()
    L += ["## 7. Same registrable domain at several granularities (kept: different block_scope)", ""] + [f"- {r['registrable_domain']}: {r['n']} ({r['t']})" for r in gran]
    con.commit()
    if write: (ROOT / "data" / "DEDUP.md").write_text("\n".join(L) + "\n")
    return {**mi, "entity_merges": len(merged), "official_conflicts": len(conf), "report_dups": len(rd), "ioc_allowlist_hits": len(ic), "shared_endpoints": len(shared_ep)}


def merge_indicators(con):
    """Self-healing dedup: re-canonicalise every indicator; fold near-duplicates into the canonical id (sightings,
    entity links, categories, liveness history move across; nothing is lost); drop junk values."""
    moved, dropped, touched = 0, 0, set()
    for iid, t, v in con.execute("SELECT indicator_id, type, value FROM indicator").fetchall():
        cv = canonical(t, v)
        if cv == v: continue
        if cv is None:
            for tbl in ("sighting", "indicator_entity", "indicator_category", "liveness_check"): con.execute(f"DELETE FROM {tbl} WHERE indicator_id=?", (iid,))
            con.execute("DELETE FROM indicator WHERE indicator_id=?", (iid,)); dropped += 1; continue
        cid = ind_id(t, cv)
        if con.execute("SELECT 1 FROM indicator WHERE indicator_id=?", (cid,)).fetchone() is None:
            rest = [c for c in cols(con, "indicator") if c not in ("indicator_id", "value")]
            con.execute(f"INSERT INTO indicator (indicator_id, value, {', '.join(rest)}) SELECT ?, ?, {', '.join(rest)} FROM indicator WHERE indicator_id=?", (cid, cv, iid))
        for s in con.execute("SELECT * FROM sighting WHERE indicator_id=?", (iid,)).fetchall():
            new_sid = "sig_" + __import__("hashlib").sha1(f"{s['source_id']}|{s['report_id'] or ''}|{cid}".encode()).hexdigest()[:16]
            con.execute("""INSERT OR IGNORE INTO sighting SELECT ?, ?, source_id, report_id, role, source_first_seen, source_last_seen, source_status,
                           first_ingested_at, last_ingested_at, removed_at, raw FROM sighting WHERE sighting_id=?""", (new_sid, cid, s["sighting_id"]))
        for tbl, cl in (("indicator_entity", "entity_id, relation, method, score, is_primary"), ("indicator_category", "category")):
            con.execute(f"INSERT OR IGNORE INTO {tbl} (indicator_id, {cl}) SELECT ?, {cl} FROM {tbl} WHERE indicator_id=?", (cid, iid))
        con.execute("UPDATE liveness_check SET indicator_id=? WHERE indicator_id=?", (cid, iid))
        for tbl in ("sighting", "indicator_entity", "indicator_category"): con.execute(f"DELETE FROM {tbl} WHERE indicator_id=?", (iid,))
        con.execute("UPDATE feed_event SET object_id=? WHERE object_id=?", (cid, iid))
        con.execute("DELETE FROM indicator WHERE indicator_id=?", (iid,)); moved += 1; touched.add(cid)
    for cid in touched: lifecycle.recompute(con, cid)
    con.commit()
    return {"merged": moved, "dropped_junk": dropped}


def reclassify(con):
    """Re-run role + lookalike rules over stored sightings (they keep ctx), so rule fixes apply retroactively."""
    from . import ingest
    cx = ingest.Ctx(con); changed = 0
    for r in con.execute("""SELECT s.sighting_id, s.role, s.raw, i.type, i.value, i.hostname, src.page_kind, src.authority, src.default_role, src.sg_scope
                            FROM sighting s JOIN indicator i USING(indicator_id) JOIN source src USING(source_id)""").fetchall():
        raw = json.loads(r["raw"] or "{}")
        if raw.get("role_method") != "context_rule": continue
        role = ingest.decide_role(r["type"], r["value"], r["hostname"], raw.get("raw"), raw.get("ctx"), r, cx)
        if role != r["role"]: con.execute("UPDATE sighting SET role=? WHERE sighting_id=?", (role, r["sighting_id"])); changed += 1
    con.execute("DELETE FROM indicator_entity WHERE relation='lookalike'")
    for iid, v, host in con.execute("SELECT indicator_id, value, hostname FROM indicator WHERE indicator_id IN (SELECT indicator_id FROM sighting WHERE role='ioc')").fetchall():
        for e, m, sc in cx.lookalikes(v, host): con.execute("INSERT OR IGNORE INTO indicator_entity(indicator_id,entity_id,relation,method,score) VALUES (?,?,?,?,?)", (iid, e, "lookalike", m, sc))
    for (iid,) in con.execute("SELECT indicator_id FROM indicator").fetchall(): lifecycle.recompute(con, iid)
    con.commit(); return {"roles_changed": changed}
