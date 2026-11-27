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
import re
from .normalize import iso, now, EXT
from .textarget import names_from

GENERAL_ISSUERS = {"police.gov.sg", "scamshield.gov.sg", "csa.gov.sg", "mas.gov.sg", "gov.sg", "mha.gov.sg", "ncpc.gov.sg", "mddi.gov.sg", "mci.gov.sg"}
BRAND_ABUSE_CATS = {"investment", "job", "loan", "unlicensed_financial"}


def resolve(con, ids=None, emit=True):
    ent = {e: dict(kind=k, can=c, parent=p, name=n) for e, k, c, p, n in con.execute("SELECT entity_id, kind, canonical_entity_id, parent_entity_id, name FROM entity")}
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
        if not primary and not (fict and not tags):        # read the target from the advisory itself (textarget.py)
            cands = [_entity_for(con, n, iid, ent, canon) for n in _advisory_names(con, iid)]
            cands = list(dict.fromkeys(c for c in cands if c))
            host = (con.execute("SELECT hostname FROM indicator WHERE indicator_id=?", (iid,)).fetchone()[0] or "").lower()
            tok = lambda e: [w for w in re.findall(r"[a-z0-9]{3,}", (ent.get(e) or {}).get("name", "").lower() + " " + e.split("#")[0].split(".")[0].replace("text:", ""))]
            in_tags = [c for c in cands if c in tags]
            by_tok = [c for c in cands if any(w in host for w in tok(c))]
            if len(cands) == 1: primary, method, score = cands[0], "advisory_text", 0.85
            elif len(in_tags) == 1: primary, method, score = in_tags[0], "advisory_text+tag", 0.9
            elif len(by_tok) == 1: primary, method, score = by_tok[0], "advisory_text+token", 0.85
            for c in cands:
                if c != primary: con.execute("INSERT OR IGNORE INTO indicator_entity(indicator_id,entity_id,relation,method,score) VALUES (?,?,'impersonates','advisory_text_candidate',0.5)", (iid, c))
        if primary: kind = "brand_abuse" if (cats & BRAND_ABUSE_CATS) or not has_site(primary) else "clone"
        elif fict and not tags: kind = "fictitious"
        else:   # several real candidates and nothing to choose between them -> list them all (kind 'multiple'), never hide them
            n_c = con.execute("""SELECT COUNT(DISTINCT entity_id) FROM indicator_entity WHERE indicator_id=? AND relation='impersonates'""", (iid,)).fetchone()[0]
            kind = "multiple" if n_c >= 2 else "unresolved"
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


def _advisory_names(con, iid):
    """Brand names the advisories naming this site say it imitates (title first, then wording near the URL)."""
    host = con.execute("SELECT hostname FROM indicator WHERE indicator_id=?", (iid,)).fetchone()[0] or ""
    for title, raw, body in con.execute("""SELECT r.title, s.raw, r.body_md FROM sighting s JOIN report r ON r.report_id=s.report_id
                                           WHERE s.indicator_id=? AND s.role='ioc'""", (iid,)):
        b = body or ""; i = b.find(host)
        near = b[max(0, i - 250): i + 80] if i >= 0 else (json.loads(raw or "{}").get("ctx") or "")
        names, _ = names_from(title, near, b)
        if names: return names
    return []


def _entity_for(con, name, iid, ent, canon):
    """Registry entity for a brand name, else an auto-added text entity (text:<slug>) with any official domain the advisory cites."""
    n = name.strip(); low = n.lower()
    row = con.execute("""SELECT entity_id FROM entity_alias WHERE alias_norm=? UNION ALL SELECT entity_id FROM entity WHERE lower(name)=? OR lower(abbr)=?
                         LIMIT 1""", (low, low, low)).fetchone()
    if row: return canon(row[0])
    eid = "text:" + re.sub(r"[^a-z0-9]+", "-", low).strip("-")
    if eid not in ent:
        con.execute("INSERT OR IGNORE INTO entity(entity_id,name,kind,sector,country,notes) VALUES (?,?,?,?,?,?)",
                    (eid, n, "organisation", "other", "ZZ", "auto-added from advisory text (unverified; not in registry)"))
        con.execute("INSERT OR IGNORE INTO entity_alias VALUES (?,?,?,?,?)", (eid, n, low, "advisory_text", None))
        ent[eid] = {"kind": "organisation", "can": None, "parent": None, "name": n}
    # authentic site: an official/benign domain cited in the same advisory whose name carries the brand token
    toks = [w for w in re.findall(r"[a-z0-9]{3,}", low)] or [re.sub(r"[^a-z0-9]", "", low)]
    for (h,) in con.execute("""SELECT DISTINCT i.hostname FROM sighting s JOIN indicator i USING(indicator_id) WHERE s.role IN ('official','mention_benign')
                               AND i.type IN ('domain','hostname','url') AND s.report_id IN (SELECT report_id FROM sighting WHERE indicator_id=? AND role='ioc')""", (iid,)):
        reg = (EXT(h or "").top_domain_under_public_suffix or "") if h else ""
        if reg and any(t in reg.replace("-", "") for t in toks if len(t) >= 3):
            con.execute("INSERT OR IGNORE INTO entity_official VALUES ('domain',?,?,?)", (reg, eid, "cited in advisory"))
    return eid
