"""Apply a parser result to the DB: dedup by unique keys, role classification, entity linking, removal detection."""
import json, re, email.utils
from .normalize import (iso, now, parse_ts, ind_id, sig_id, defang, host_info, sg_signals, fingerprint, sha256, EXT, canonical)
from .db import J
from . import lifecycle

SCAM_CTX = re.compile(r"fake|fraud|scam|phish|bogus|spoof|impersonat|malicious|unauthori[sz]ed|not (?:an? )?(?:official|legitimate)|"
                      r"do not (?:click|visit|reply)|look-?alike|counterfeit|fictitious|illegal", re.I)
CAT = {"investment": "investment", "job": "job", "phishing.banking": "phishing.banking", "phishing.non_banking": "phishing.non_banking",
       "phishing.unspecified": "phishing.unspecified", "ecommerce": "ecommerce", "malware": "malware", "loan": "loan", "visa": "visa",
       "Investor Alert List": "unlicensed_financial"}
from .parsers.core import SPF_CAT
FAKE_NEAR = re.compile(r"fake|spoof|fraudulent|bogus|impersonat|phishing|look-?alike|not (?:an? )?official", re.I)
def near(ctx, raw, w=60):
    i = (ctx or "").find(raw or "\0")
    return (ctx or "")[max(0, i - w): i + len(raw) + w] if i >= 0 else ""

# Narrative pages: the site must be named *as* a fake site - a website-noun phrase, not just a scam word somewhere nearby
# ("fake 5-star reviews", "malicious app ... Source: www.x.com" and cited blog links do not qualify).
SITE_NOUN = r"(?:web ?sites?|sites?|urls?|links?|domains?|web ?pages?|pages?|portals?|addresses)"
SITE_NEAR = re.compile(rf"(?:fake|phishing|fraudulent|bogus|malicious|scam|spoof(?:ed)?|counterfeit|look-?alike|impersonati\w*|unofficial)\W+(?:\w+\W+){{0,3}}{SITE_NOUN}\b"
                       rf"|impersonat\w+|resembl\w+ (?:the )?\w+(?: \w+)? {SITE_NOUN}|claim(?:s|ing|ed)? to be|not (?:affiliated|associated) with"
                       rf"|{SITE_NOUN} (?:that|which) (?:impersonat|mimic|pretend|pos)\w*", re.I)

def named_as_fake(ctx, raw):
    i = (ctx or "").find(raw or "\0")
    if i < 0: return False
    before, after = ctx[max(0, i - 140): i], ctx[i + len(raw): i + len(raw) + 60]
    if re.search(r"(?:source|reference|read more|more information|learn more)\s*[:\-]?\s*(?:\(?\w+\)?\s*)?$", before, re.I): return False   # citation
    if re.search(r"(?:instagram|facebook|telegram|tiktok|whatsapp|social media)\s+(?:\w+\s+){0,2}(?:accounts?|handles?|profiles?)\W+(?:\w+\W+){0,3}$", before, re.I): return False
    tail = before[-90:]
    if re.search(r"\b(?:may|might|could|can)\b", tail, re.I) and re.search(r"\b(?:like using|for instance|for example|such as using)\b\W*$", tail, re.I):
        return False                                     # hypothetical illustration ("fraudsters may ... like using Go0gle.com")
    return bool(SITE_NEAR.search(before + " " + raw + " " + after))

RESTRICTED_SG = (".gov.sg", ".edu.sg", ".mil.sg")          # SGNIC-restricted: cannot be registered by a scammer

def benign_ref(host):
    if not host: return False
    reg = EXT(host).top_domain_under_public_suffix or host
    return reg in BENIGN_REF or host == "gov.sg" or host.endswith(RESTRICTED_SG) or bool(re.search(r"x{3}|(?:^|\.)example\.", host))

def decide_role(t_, v, host, raw, ctx, src, cx):
    """Shared by ingest + reclassify. Order: allowlist > benign reference / e-mail fragment > allowlist-page default > phones >
    fake-list page default > named-as-fake within +-80 chars (narrative pages) > default."""
    owner = cx.official_owner(v, host) if t_ in ("domain", "hostname", "url", "email") else (cx.allow.get(v) if t_ == "phone" else None)
    if t_ == "email" and not owner: owner = cx.official_owner(v.split("@")[-1], v.split("@")[-1])
    if owner: return "official" if src["default_role"] == "official" else "mention_benign"
    if t_ in ("domain", "hostname", "url"):
        if benign_ref(host): return "mention_benign"
        if raw and ctx and re.search(re.escape(raw) + r"\s*(?:@|\[at\]|\(at\))", ctx): return "mention_benign"   # part of an e-mail address
    if src["sg_scope"] == "allowlist": return "ioc" if FAKE_NEAR.search(near(ctx, raw)) else "official"
    if t_ == "phone" and src["page_kind"] != "fake_indicator_list": return "unknown"
    if src["page_kind"] == "fake_indicator_list" and src["default_role"] == "ioc" and t_ in ("domain", "hostname", "url"):
        return "ioc"                                       # e.g. ICA's fake-SGAC annex: rows carry no per-row scam words
    if t_ in ("domain", "hostname", "url"):              # narrative page: the site itself must be named as fake/phishing nearby
        if ctx and named_as_fake(ctx, raw) and src["authority"] in ("authoritative", "regulator", "industry"): return "ioc"
    elif ctx and SCAM_CTX.search(ctx) and src["authority"] in ("authoritative", "regulator", "industry"): return "ioc"
    return "official" if src["default_role"] == "official" else "unknown"

# Reference links that appear on fake-site list pages (app stores, socials, search) - never the listed scam site itself.
BENIGN_REF = {"apple.com", "google.com", "google.org", "youtube.com", "facebook.com", "instagram.com", "x.com", "twitter.com", "linkedin.com",
              "tiktok.com", "telegram.org", "t.me", "wa.me", "whatsapp.com", "microsoft.com", "adobe.com", "w3.org", "schema.org", "gov.sg",
              "bit.ly", "tinyurl.com", "wikipedia.org", "asiaone.com", "straitstimes.com", "channelnewsasia.com", "todayonline.com",
              "mothership.sg", "zaobao.com.sg", "kkday.me", "kkday.com", "airdroid.com", "viagogo.com", "app.link", "sgcarmart.com",
              "globalcyberalliance.org", "bleepingcomputer.com", "bitdefender.com", "anomali.com", "virustotal.com", "urlscan.io"}

GENERIC_TOKENS = {"gov", "www", "mail", "home", "online", "group", "bank", "global", "asia", "app", "apps", "info", "news", "help",
                  "service", "services", "support", "login", "my", "the", "sg", "singapore", "com", "net", "org", "official", "life", "tech",
                  "link", "pass", "smart", "care", "health", "safe", "check", "go", "for", "one", "pay", "money", "sense", "trust", "live",
                  "shop", "store", "travel", "air", "post", "express", "parcel", "vouchers", "voucher", "redeem", "ask", "data", "open", "mol",
                  "case", "chat", "payment", "payments", "epayment", "epayments", "station", "home", "card", "cards", "plus", "hub"}

def ts(s):
    if not s: return None
    d = parse_ts(s) if "T" in s or re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) else None
    if d is None and re.fullmatch(r"\d{4}-\d{2}-\d{2}", s or ""): return s + "T00:00:00Z"
    if d is None:
        try: d = email.utils.parsedate_to_datetime(s)
        except (TypeError, ValueError): return None
    if d.tzinfo is None: return d.isoformat() + "Z"
    return iso(d)

class Ctx:
    """Per-run caches: allowlist, aliases, lookalike tokens."""
    def __init__(self, con):
        self.allow = {}
        from .normalize import norm_phone
        for k, v, e in con.execute("SELECT kind, value, entity_id FROM entity_official"):
            self.allow.setdefault(v.lower(), e)
            if k == "hotline":
                num = re.sub(r"\(.*?\)", "", v); p = norm_phone(num) if re.search(r"\d{4}", num) else None
                if p: self.allow.setdefault(p, e)
        for v, e in con.execute("""SELECT i.value, src.publisher_entity_id FROM sighting s JOIN indicator i USING(indicator_id)
                                   JOIN source src USING(source_id) WHERE s.role='official' AND src.sg_scope='allowlist'"""):
            self.allow.setdefault(v.lower(), e or "allowlist-page")
        self.alias = {}
        for a, e, kind, can in con.execute("SELECT alias_norm, a.entity_id, kind, canonical_entity_id FROM entity_alias a JOIN entity USING(entity_id)"):
            self.alias.setdefault(a, (can or e, kind))
        self.sector = {e: s or "" for e, s in con.execute("SELECT entity_id, sector FROM entity")}
        self.tokens = {}
        for v, e in con.execute("""SELECT o.value, o.entity_id FROM entity_official o JOIN entity en USING(entity_id)
                                   WHERE o.kind='domain' AND en.country='SG' AND en.canonical_entity_id IS NULL"""):
            tok = (EXT(v).domain or "").lower()
            if len(tok) >= 3 and tok not in GENERIC_TOKENS: self.tokens.setdefault(tok, e)
        for v, e in con.execute("""SELECT o.value, o.entity_id FROM entity_official o JOIN entity en USING(entity_id)
                                   WHERE o.kind='host' AND en.country='SG' AND en.canonical_entity_id IS NULL"""):
            lab = v.split(".")[0].lower()
            if len(lab) >= 6 and lab not in GENERIC_TOKENS and not re.search(r"\d", lab): self.tokens.setdefault(lab, e)
        self.gov = {e for (e,) in con.execute("SELECT entity_id FROM entity WHERE entity_id LIKE '%.gov.sg%'")}

    def official_owner(self, value, host):
        for v in (value, host, EXT(host).top_domain_under_public_suffix if host else None):
            if v and v.lower() in self.allow: return self.allow[v.lower()]
        return None

    def lookalikes(self, value, host):
        if not host or self.official_owner(value, host): return []
        reg = EXT(host).top_domain_under_public_suffix or host; sub = host[: -len(reg)].rstrip(".")
        words = lambda x: [w for w in re.split(r"[.\-_/]+", x.lower()) if w]
        regw, subw = words(reg.rsplit(".", 1)[0]), words(sub); path = value.split(host, 1)[-1] if "://" in value else ""
        sgctx = bool(re.search(r"(?:^|[.\-])sg(?:[.\-]|$)|singapore|\.sg$", host + "/" + path))
        govctx = "gov" in words(host)
        def hit(tok, ws, e=None):
            if len(tok) <= 4: return tok in ws and (sgctx or (govctx and e in self.gov) or len(tok) == 4)
            return any(w == tok or (len(w) <= len(tok) + 6 and (w.startswith(tok) or w.endswith(tok))) for w in ws)
        out = []
        for tok, e in self.tokens.items():
            if hit(tok, regw, e): out.append((e, "brand_token", 0.8))
            elif hit(tok, subw, e): out.append((e, "subdomain_abuse", 0.7))
            elif path and tok in words(path) and (len(tok) > 4 or sgctx): out.append((e, "path_kit", 0.6))
        return out[:5]

def categories(raw, imp_entities, ctx):
    out = set()
    for c in raw:
        m = SPF_CAT.get(c) or CAT.get(c)
        if m == "impersonation":
            m = "impersonation.government" if any(ctx.sector.get(e, "").startswith("gov") for e in imp_entities) else "impersonation.other"
        if m: out.add(m)
    return out

def apply(con, src, ep, res, cx, t=None):
    t = t or now(); T = iso(t); sid = src["source_id"]; native = src["sg_scope"] == "native"
    touched, rep_ids, n_rep = set(), set(), 0
    rep_entities = {}
    for r in res["reports"]:
        rid = f"{sid}:{r['native_id']}"[:500]; rep_ids.add(rid)
        pub, mod = ts(r.get("published_at")), ts(r.get("modified_at"))
        body_h = sha256(r["body"]) if r.get("body") else None
        fp = fingerprint(r["title"], (pub or "")[:10])
        old = con.execute("SELECT body_sha256, modified_at, status FROM report WHERE report_id=?", (rid,)).fetchone()
        if old is None:
            con.execute("""INSERT INTO report(report_id,source_id,native_id,url,issuer_entity_id,title,summary,body_md,published_at,modified_at,
                           fingerprint,body_sha256,status,first_ingested_at,last_ingested_at,raw) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (rid, sid, r["native_id"][:500], r.get("url"), src["publisher_entity_id"], r["title"][:500], (r.get("body") or "")[:280] or None,
                         r.get("body"), pub, mod, fp, body_h, "published", T, T, J(r.get("raw")))); n_rep += 1
        else:
            upd = (old["body_sha256"] != body_h and body_h) or (mod and old["modified_at"] != mod)
            con.execute("""UPDATE report SET last_ingested_at=?, withdrawn_at=NULL, title=?, url=COALESCE(?,url), body_md=COALESCE(?,body_md),
                           body_sha256=COALESCE(?,body_sha256), modified_at=COALESCE(?,modified_at), fingerprint=?,
                           status=CASE WHEN ? THEN 'updated' WHEN status='withdrawn' THEN 'published' ELSE status END WHERE report_id=?""",
                        (T, r["title"][:500], r.get("url"), r.get("body"), body_h, mod, fp, 1 if upd else 0, rid))
        imp = []
        for b in r.get("brands_raw") or []:
            hit = cx.alias.get(b.strip().lower())
            if hit:
                role = "fictitious_brand" if hit[1] == "fictitious_brand" else "impersonated"
                con.execute("INSERT OR IGNORE INTO report_entity VALUES (?,?,?)", (rid, hit[0], role)); imp.append((hit[0], role))
        rep_entities[r["native_id"]] = imp
        for c in categories(r.get("categories_raw") or [], [e for e, ro in imp if ro == "impersonated"], cx):
            con.execute("INSERT OR IGNORE INTO report_category VALUES (?,?,?)", (rid, c, None))
    if res.get("complete") and src["lifecycle_semantics"] == "snapshot_full" and res["reports"]:
        con.execute(f"""UPDATE report SET status='withdrawn', withdrawn_at=? WHERE source_id=? AND withdrawn_at IS NULL
                        AND report_id NOT IN ({','.join('?' * len(rep_ids))})""", (T, sid, *rep_ids))

    seen_sig = set(); n_ind = 0
    for i in res["indicators"]:
        t_, host = i["type"], i["host"]; v = canonical(t_, i["value"])
        if v is None: continue
        role = i["role"] if i.get("role") and not cx.official_owner(v, host) else decide_role(t_, v, host, i["raw"], i.get("ctx"), src, cx)
        iid = ind_id(t_, v); hi = host_info(host) if host else {}
        if con.execute("SELECT 1 FROM indicator WHERE indicator_id=?", (iid,)).fetchone() is None:
            sgs = sg_signals(v, host, native) if host else {"sg_native_source": native, "score": 0.6 if native else 0.0}
            con.execute("""INSERT INTO indicator(indicator_id,type,value,value_defanged,hostname,registrable_domain,tld,is_shared_platform,block_scope,
                           sg_score,sg_signals,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (iid, t_, v, defang(v), host, hi.get("registrable_domain"), hi.get("tld"), int(hi.get("is_shared_platform", False)),
                         hi.get("block_scope"), sgs["score"], J(sgs), "unverified", T, T)); n_ind += 1
        elif native:
            con.execute("UPDATE indicator SET sg_score=MAX(COALESCE(sg_score,0),0.6) WHERE indicator_id=?", (iid,))
        rid = f"{sid}:{i['report_native_id']}"[:500] if i.get("report_native_id") else None
        sg = sig_id(sid, rid, iid); seen_sig.add(sg)
        con.execute("""INSERT INTO sighting(sighting_id,indicator_id,source_id,report_id,role,source_first_seen,source_last_seen,source_status,
                       first_ingested_at,last_ingested_at,raw) VALUES (?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(sighting_id) DO UPDATE SET last_ingested_at=excluded.last_ingested_at, removed_at=NULL,
                         source_last_seen=COALESCE(excluded.source_last_seen, source_last_seen), source_status=excluded.source_status,
                         role=CASE WHEN role IN ('unknown','mention_benign') THEN excluded.role ELSE role END""",
                    (sg, iid, sid, rid, role, ts(i.get("source_first_seen")), ts(i.get("source_last_seen")), i.get("source_status"), T, T,
                     J({"raw": i["raw"], "ctx": (i.get("ctx") or "")[:400] or None, "role_method": "explicit" if i.get("role") else "context_rule"})))
        if role == "ioc":
            imp = rep_entities.get(i.get("report_native_id"), [])
            for e, ro in imp:
                con.execute("INSERT OR IGNORE INTO indicator_entity(indicator_id,entity_id,relation,method,score) VALUES (?,?,?,?,?)", (iid, e, "fictitious_brand" if ro == "fictitious_brand" else "impersonates", "report_tag", 1.0))
            for e, m, sc in cx.lookalikes(v, host):
                con.execute("INSERT OR IGNORE INTO indicator_entity(indicator_id,entity_id,relation,method,score) VALUES (?,?,?,?,?)", (iid, e, "lookalike", m, sc))
            cats = categories(i.get("categories") or [], [e for e, ro in imp if ro == "impersonated"], cx)
            if any("kit:" in p for p in json.loads(con.execute("SELECT sg_signals FROM indicator WHERE indicator_id=?", (iid,)).fetchone()[0] or "{}").get("path_tokens", [])):
                cats.discard("phishing.unspecified"); cats.add("phishing.banking")
            for c in cats: con.execute("INSERT OR IGNORE INTO indicator_category VALUES (?,?)", (iid, c))
        touched.add(iid)
    if res.get("complete") and src["lifecycle_semantics"] in ("active_list", "snapshot_full") and res["indicators"]:
        gone = con.execute("SELECT sighting_id, indicator_id FROM sighting WHERE source_id=? AND removed_at IS NULL", (sid,)).fetchall()
        for g in gone:
            if g["sighting_id"] not in seen_sig:
                con.execute("UPDATE sighting SET removed_at=? WHERE sighting_id=?", (T, g["sighting_id"])); touched.add(g["indicator_id"])
    for iid in touched: lifecycle.recompute(con, iid, t)
    return n_rep, n_ind
