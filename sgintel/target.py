"""Impersonation target resolver (SCOPE.md §4): every site gets exactly one primary authentic target, or an explicit
no-target kind. Candidates already stored in indicator_entity (report_tag brands, lookalike tokens) are ranked; the
winner is marked is_primary=1 on an 'impersonates' row (partial unique index ux_primary_target enforces one).

Order: lookalike token that agrees with a brand tag > single brand tag > single lookalike > publisher itself (when the
publisher is the impersonated brand, e.g. ICA listing fake SG Arrival Card sites) > unresolved (review queue).
Kind: clone (target has an authentic site) | brand_abuse (investment/job/loan lure, or target without an own site)
      | fictitious (only fictitious brands named) | unresolved.
"""
import json
from collections import Counter
from .normalize import iso, now

GENERAL_ISSUERS = {"police.gov.sg", "scamshield.gov.sg", "csa.gov.sg", "mas.gov.sg", "gov.sg", "mha.gov.sg", "ncpc.gov.sg", "mddi.gov.sg", "mci.gov.sg"}
BRAND_ABUSE_CATS = {"investment", "job", "loan", "unlicensed_financial"}


def resolve(con, ids=None, emit=True):
    ent = {e: dict(kind=k, can=c, parent=p) for e, k, c, p in con.execute("SELECT entity_id, kind, canonical_entity_id, parent_entity_id FROM entity")}
    canon = lambda e: (ent.get(e) or {}).get("can") or e
    own = {e for (e,) in con.execute("SELECT DISTINCT entity_id FROM entity_official WHERE kind IN ('domain','host')")}
    has_site = lambda e: e in own or (ent.get(e) or {}).get("parent") in own
    ids = ids or [r[0] for r in con.execute("SELECT indicator_id FROM v_site")]
    stats, t = Counter(), iso(now())
    for iid in ids:
        prev = (con.execute("SELECT entity_id FROM indicator_entity WHERE indicator_id=? AND is_primary=1", (iid,)).fetchone() or [None])[0]
        # brand tags come from the publications themselves (report_entity), never from rows this resolver rewrites
        rep = con.execute("""SELECT DISTINCT re.entity_id, re.role FROM sighting s JOIN report_entity re ON re.report_id=s.report_id
                             WHERE s.indicator_id=? AND s.role='ioc'""", (iid,)).fetchall()
        tags = {canon(e) for e, ro in rep if ro == "impersonated"}; fict = {canon(e) for e, ro in rep if ro == "fictitious_brand"}
        con.execute("DELETE FROM indicator_entity WHERE indicator_id=? AND relation='impersonates' AND IFNULL(method,'')<>'report_tag'", (iid,))
        for e in tags: con.execute("INSERT OR IGNORE INTO indicator_entity(indicator_id,entity_id,relation,method,score) VALUES (?,?,'impersonates','report_tag',1.0)", (iid, e))
        for e in fict: con.execute("INSERT OR IGNORE INTO indicator_entity(indicator_id,entity_id,relation,method,score) VALUES (?,?,'fictitious_brand','report_tag',1.0)", (iid, e))
        looks = sorted(((r["score"] or 0, canon(r["entity_id"]), r["method"]) for r in
                        con.execute("SELECT entity_id, method, score FROM indicator_entity WHERE indicator_id=? AND relation='lookalike'", (iid,))), reverse=True)
        cats = {c for (c,) in con.execute("SELECT category FROM indicator_category WHERE indicator_id=?", (iid,))}
        pubs = {p for (p,) in con.execute("""SELECT DISTINCT src.publisher_entity_id FROM sighting s JOIN source src USING(source_id)
                                             WHERE s.indicator_id=? AND s.role='ioc' AND src.listing_role IN ('listing','adjacent')""", (iid,)) if p}
        primary = method = None; score = None
        agree = [l for l in looks if l[1] in tags]
        if agree: primary, method, score = agree[0][1], f"lookalike+tag:{agree[0][2]}", 0.95
        elif len(tags) == 1: primary, method, score = next(iter(tags)), "report_tag", 0.9
        elif not tags and looks and len({l[1] for l in looks if l[0] == looks[0][0]}) == 1:
            primary, method, score = looks[0][1], f"lookalike:{looks[0][2]}", looks[0][0]
        elif not tags and not looks and not fict:
            selfp = [canon(p) for p in pubs if p not in GENERAL_ISSUERS and (ent.get(p) or {}).get("kind") in ("organisation", "programme")]
            if len(selfp) == 1: primary, method, score = selfp[0], "publisher_self", 0.6
        if primary: kind = "brand_abuse" if (cats & BRAND_ABUSE_CATS) or not has_site(primary) else "clone"
        elif fict and not tags: kind = "fictitious"
        else: kind = "unresolved"
        con.execute("UPDATE indicator_entity SET is_primary=0 WHERE indicator_id=? AND is_primary=1", (iid,))
        if primary:
            con.execute("""INSERT INTO indicator_entity(indicator_id, entity_id, relation, method, score, is_primary) VALUES (?,?,?,?,?,1)
                           ON CONFLICT(indicator_id, entity_id, relation) DO UPDATE SET is_primary=1, method=excluded.method, score=excluded.score""",
                        (iid, primary, "impersonates", method, score))
        con.execute("UPDATE indicator SET impersonation_kind=? WHERE indicator_id=?", (kind, iid))
        stats[kind] += 1; stats["method:" + (method or "none").split(":")[0]] += 1
        if emit and prev and prev != primary:
            from .liveness import site_event
            site_event(con, iid, "site.target_changed", prev, t); stats["target_changed"] += 1
    con.commit()
    return dict(stats)
