"""Map real records from each source into the v0.1 schema and validate them.

Not the pipeline: this is a fit-test showing the schema holds real data from
SPF icanact (snapshot_full), MAS IAL (snapshot_full), Phishing.Database (active_list),
PhishStats (event_stream), plus a real DNS+RDAP liveness check.

run: .venv/bin/python schema/build_examples.py
"""
import hashlib, json, re, sys, os, datetime as dt, urllib.request
from pathlib import Path
import tldextract, phonenumbers, jsonschema, dns.resolver

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / "data" / "fixtures"   # persistent inputs (scratchpad is wiped on restart)
OUT = ROOT / "schema" / "examples"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "sources"))
import sgfilter  # token tiers shared with the global-feed filter

NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
iso = lambda d: d.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z") if d else None
EXT = tldextract.TLDExtract(include_psl_private_domains=True)
KNOWN_PLATFORMS = {"blogspot.com", "blogspot.sg", "pages.dev", "edgeone.dev", "wpenginepowered.com",
                   "github.io", "netlify.app", "vercel.app", "web.app", "firebaseapp.com", "weebly.com", "wixsite.com"}
TTL_DAYS = {"url": 30, "hostname": 90, "domain": 90, "ipv4": 14, "ipv6": 14, "phone": 180, "email": 180, "entity_name": 365}
CHECKABLE = {"url", "hostname", "domain", "ipv4", "ipv6"}
AUTH_CONF = {"authoritative": 90, "regulator": 90, "industry": 75, "commercial": 70, "community": 60, "academic": 50}
SPF_CAT = {"Investment": "investment", "Job": "job", "Banking Related Phishing": "phishing.banking",
           "Non-Banking Related Phishing": "phishing.non_banking", "Phishing": "phishing.unspecified",
           "E-Commerce": "ecommerce", "Malware": "malware", "Loan": "loan", "Visa": "visa", "Impersonation": None}
SERVICE = {"onemotoring/lta", "ezlink", "paynow", "cdc-voucher", "simplygo"}
PATH_KIT = re.compile(r"/(?:bank|banks|b)/(dbs|posb|ocbc|uob|citi|hsbc|maybank|scb?)(?=/|$)")

def h16(s): return hashlib.sha1(s.encode()).hexdigest()[:16]
def ind_id(t, v): return f"ind_{h16(t + ':' + v)}"
def sig_id(src, rep, ind): return f"sig_{h16(f'{src}|{rep or ''}|{ind}')}"
def defang(v): return v.replace("http", "hxxp").replace(".", "[.]")

# ---- brand -> entity resolution (uses agent output when present) ----
BRAND_MAP = {}
bm = ROOT / "registry" / "spf_brand_map.json"
if bm.exists():
    for r in json.load(open(bm)):
        BRAND_MAP[r["brand_value"]] = r
FALLBACK_GOV = {"LTA": "lta.gov.sg", "SPF": "police.gov.sg", "IRAS": "iras.gov.sg", "ICA": "ica.gov.sg",
                "CPF": "cpf.gov.sg", "NEA": "nea.gov.sg", "MHA": "mha.gov.sg", "HTX": "htx.gov.sg"}
def resolve_brand(b):
    r = BRAND_MAP.get(b)
    if r:
        if r["resolution"] == "real_entity" and r.get("entity_id"): return "real", r["entity_id"], (r.get("sector") or "")
        if r["resolution"] == "fictitious_scam_brand": return "fict", "brand:" + re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-"), ""
        return "other", None, ""
    m = re.search(r"\(([A-Z]{2,5})\)", b)
    if m and m.group(1) in FALLBACK_GOV: return "real", FALLBACK_GOV[m.group(1)], "gov.statboard"
    return "unresolved", None, ""

# ---- host analysis + SG signals ----
RX = {t: {k: re.compile(v) for k, v in d.items()} for t, d in (("A", sgfilter.TIER_A), ("B", sgfilter.TIER_B))}
def host_info(hostname):
    r = EXT(hostname)
    reg = r.top_domain_under_public_suffix or hostname
    shared = bool(r.is_private) or reg in KNOWN_PLATFORMS or any(hostname.endswith("." + p) for p in KNOWN_PLATFORMS)
    return {"hostname": hostname, "registrable_domain": reg, "tld": r.suffix.split(".")[-1] if r.suffix else "",
            "is_shared_platform": shared, "is_compromised_legit": None,
            "block_scope": "registrable_domain" if (hostname == reg and not shared) else "hostname",
            "idn_unicode": hostname.encode().decode("idna") if "xn--" in hostname else None}
def sg_signals(full, hostname, native):
    path = full[len(hostname):] if full.startswith(hostname) else ""
    brand, service, pathk = [], [], []
    for k, rx in RX["A"].items():
        if k == "ccTLD .sg": continue
        if rx.search(hostname): (service if k in SERVICE else brand).append(k)
        elif path and rx.search(path): pathk.append(k)
    pathk += [f"kit:/bank/{m}" for m in PATH_KIT.findall(path)]
    ctx = bool(sgfilter.SG_CTX.search(full))
    for k, rx in RX["B"].items():
        if ctx and rx.search(full): brand.append(k + "+sgctx")
    sg_tld = hostname.endswith(".sg")
    score = min(1.0, 0.6 * native + 0.3 * bool(brand or service) + 0.2 * bool(pathk) + 0.1 * sg_tld)
    return {"sg_tld": sg_tld, "brand_tokens": brand, "service_tokens": service, "path_tokens": pathk,
            "sg_native_source": bool(native), "score": round(score, 2)}

def parse_host_or_url(raw):
    s = raw.strip().lower().rstrip("/")
    u = urllib.parse.urlsplit(s if "://" in s else "http://" + s)
    host = (u.hostname or "").removeprefix("www.")
    if not host: return None
    host = host.encode("idna").decode() if not host.isascii() else host
    if u.path not in ("", "/") or u.query:
        return "url", f"{u.scheme}://{host}{u.path}{'?' + u.query if u.query else ''}", host
    return ("domain" if EXT(host).top_domain_under_public_suffix == host else "hostname"), host, host
import urllib.parse

# ---- record factories ----
def new_indicator(t, v, raw, host, native):
    rec = {"record_type": "indicator", "indicator_id": ind_id(t, v), "type": t, "value": v,
           "value_defanged": defang(v), "values_raw": [raw], "host": host_info(host) if host else None,
           "sg_signals": sg_signals(v.split("://")[-1], host, native) if host else
                         {"sg_tld": False, "brand_tokens": [], "service_tokens": [], "path_tokens": [], "sg_native_source": bool(native), "score": 0.6 if native else 0.0},
           "impersonated_entity_ids": [], "fictitious_brand_ids": [], "lookalike_of": [], "categories": [],
           "issuer_entity_ids": [], "report_ids": [], "source_ids": [], "n_sightings": 0,
           "liveness": {"state": "unknown" if t in CHECKABLE else "not_applicable", "state_since": None, "last_checked_at": None,
                        "last_live_at": None, "consecutive_failures": 0, "last_check_id": None,
                        "registration_expires_at": None, "registry_status": []},
           "revoked": False, "tlp": "TLP:CLEAR", "created_at": iso(NOW), "updated_at": iso(NOW), "version": 1}
    return rec
def new_sighting(ind, src, rep, role, first, last, status, raw):
    return {"record_type": "sighting", "sighting_id": sig_id(src, rep, ind["indicator_id"]), "indicator_id": ind["indicator_id"],
            "source_id": src, "report_id": rep, "role": role, "source_first_seen": first, "source_last_seen": last,
            "source_status": status, "first_ingested_at": iso(NOW), "last_ingested_at": iso(NOW), "removed_at": None, "raw": raw}

def derive(ind, sightings, sources, now=NOW):
    """Lifecycle rules (SCHEMA.md §4). Ingestion of an unchanged snapshot_full record does NOT refresh last_seen."""
    firsts, lasts = [], []
    for s in sightings:
        sem = sources[s["source_id"]]["lifecycle_semantics"]
        f = s["source_first_seen"] or s["first_ingested_at"]
        l = s["source_last_seen"] or (s["last_ingested_at"] if sem in ("active_list",) and not s["removed_at"] else None) or f
        firsts.append(f); lasts.append(l)
    ind["first_seen"], ind["last_seen"] = min(firsts), max(lasts)
    ind["source_ids"] = sorted({s["source_id"] for s in sightings}); ind["n_sightings"] = len(sightings)
    base = max(AUTH_CONF[sources[s]["authority"]] for s in ind["source_ids"])
    ind["confidence"] = min(100, base + 5 * (len(ind["source_ids"]) - 1))
    lv = ind["liveness"]
    anchor = max(x for x in [ind["last_seen"], lv["last_live_at"]] if x)
    vu = dt.datetime.fromisoformat(anchor.replace("Z", "+00:00")) + dt.timedelta(days=TTL_DAYS[ind["type"]])
    ind["valid_from"], ind["valid_until"] = ind["first_seen"], iso(vu)
    reg_exp = lv.get("registration_expires_at")
    if ind["revoked"]: st, why = "revoked", "source withdrew"
    elif lv["state"] == "live": st, why = "active", "liveness=live"
    elif lv["state"] in ("dead", "parked", "suspended", "sinkholed", "blocked"):
        # positive evidence it is down: inactive (not expired) while the registration exists and could be revived
        dropped = reg_exp and now > dt.datetime.fromisoformat(reg_exp.replace("Z", "+00:00")) + dt.timedelta(days=45)
        held = any("hold" in x.lower() for x in lv.get("registry_status", []))
        st = "expired" if dropped else "inactive"
        why = "registration lapsed" if dropped else ("registrar hold (takedown)" if held else f"liveness={lv['state']}")
    elif lv["state"] == "not_applicable": st, why = ("active" if now <= vu else "expired"), "uncheckable type; TTL from last sighting"
    else: st, why = ("unverified", "not yet checked / inconclusive") if now <= vu else ("expired", "no activity evidence within TTL")
    ind["status"], ind["status_reason"] = st, why
    return ind

# ---- liveness: DNS + RDAP only (no HTTP to scam hosts) ----
RES = dns.resolver.Resolver(); RES.lifetime = 8  # system resolver (direct :53 to public resolvers is blocked on this VM)
def check(ind):
    host = ind["host"]["hostname"]; d = {"rcode": "NOERROR", "a": [], "aaaa": [], "cname": [], "ns": []}
    try:
        ans = RES.resolve(host, "A")
        d["a"] = sorted(r.to_text() for r in ans)
        d["cname"] = [ans.canonical_name.to_text().rstrip(".")] if ans.canonical_name.to_text().rstrip(".") != host else []
    except dns.resolver.NXDOMAIN: d["rcode"] = "NXDOMAIN"
    except dns.resolver.NoAnswer: d["rcode"] = "NODATA"
    except dns.exception.Timeout: d["rcode"] = "TIMEOUT"
    except dns.resolver.NoNameservers: d["rcode"] = "SERVFAIL"
    rd = None
    if not ind["host"]["is_shared_platform"]:
        reg = ind["host"]["registrable_domain"]
        try:
            req = urllib.request.Request(f"https://rdap.org/domain/{reg}", headers={"Accept": "application/rdap+json", "User-Agent": "sg-scam-intel-schema-test/0.1"})
            j = json.load(urllib.request.urlopen(req, timeout=20))
            ev = {e.get("eventAction"): e.get("eventDate") for e in j.get("events", [])}
            norm = lambda t: iso(dt.datetime.fromisoformat(t.replace("Z", "+00:00"))) if t else None
            rd = {"status": j.get("status", []), "registered_at": norm(ev.get("registration")), "expires_at": norm(ev.get("expiration")),
                  "registrar": next((v[3] for e in j.get("entities", []) if "registrar" in e.get("roles", [])
                                     for v in (e.get("vcardArray", [None, []])[1]) if v[0] == "fn"), None), "error": None}
        except Exception as e:
            rd = {"status": [], "registered_at": None, "expires_at": None, "registrar": None, "error": f"{type(e).__name__}: {str(e)[:80]}"}
    hold = rd and any(s.replace(" ", "").lower() in ("clienthold", "serverhold") for s in rd["status"])
    if d["rcode"] == "NXDOMAIN" or hold: verdict = "dead"
    elif d["a"] and ind["host"]["is_shared_platform"]: verdict = "inconclusive"   # wildcard DNS on platforms: needs HTTP/content check
    elif d["a"]: verdict = "live"
    else: verdict = "inconclusive"                                                 # TIMEOUT/SERVFAIL alone proves nothing
    c = {"record_type": "liveness_check", "check_id": f"chk_{h16(ind['indicator_id'] + iso(NOW))}", "indicator_id": ind["indicator_id"],
         "checked_at": iso(NOW), "checker": {"version": "schema-fit-0.1", "vantage": "azure-vm (non-SG)", "resolver": "system (Azure DNS via systemd-resolved)"},
         "dns": d, "rdap": rd, "tls": None, "http": None, "fingerprints": ["registrar_hold"] if hold else [], "verdict": verdict}
    lv = ind["liveness"]; lv.update(state=verdict if verdict not in ("error", "inconclusive") else "unknown", state_since=iso(NOW), last_checked_at=iso(NOW),
                                    last_check_id=c["check_id"], registration_expires_at=rd and rd["expires_at"],
                                    registry_status=(rd or {}).get("status", []))
    if verdict == "live": lv["last_live_at"] = iso(NOW)
    else: lv["consecutive_failures"] += 1
    return c

# ---- sources ----
SOURCES = {
  "spf-icanact": {"record_type": "source", "source_id": "spf-icanact", "name": "SPF I can ACT against scams: Scam Trends",
      "publisher_entity_id": "police.gov.sg", "url": "https://www.icanactagainstscams.gov.sg/scam-trends", "machine_url": None,
      "access": "html_rsc", "auth": "none", "authority": "authoritative", "sg_scope": "native", "sg_filter_id": None,
      "lifecycle_semantics": "snapshot_full", "provides_times": ["published", "modified"], "licence": None,
      "terms_url": "https://www.icanactagainstscams.gov.sg/terms-of-use", "tlp": "TLP:CLEAR", "poll_interval_s": 3600,
      "parser": "extract.py", "parser_version": "0.1", "notes": "Whole collection embedded as RSC prop scamAdvisories"},
  "mas-ial-opensanctions": {"record_type": "source", "source_id": "mas-ial-opensanctions", "name": "MAS Investor Alert List (OpenSanctions mirror)",
      "publisher_entity_id": "mas.gov.sg", "url": "https://www.mas.gov.sg/investor-alert-list",
      "machine_url": "https://data.opensanctions.org/datasets/latest/sg_mas_investor_alert/source.json", "access": "json", "auth": "none",
      "authority": "regulator", "sg_scope": "native", "sg_filter_id": None, "lifecycle_semantics": "snapshot_full",
      "provides_times": ["listed", "modified", "first_seen", "last_seen"], "licence": "CC-BY-NC-4.0 (OpenSanctions)", "terms_url": None,
      "tlp": "TLP:CLEAR", "poll_interval_s": 86400, "parser": None, "parser_version": None, "notes": "website_s/phonenumber_s are free text"},
  "phishdb-links-active": {"record_type": "source", "source_id": "phishdb-links-active", "name": "Phishing.Database ACTIVE links",
      "publisher_entity_id": "github.com#phishing-database", "url": "https://github.com/Phishing-Database/Phishing.Database",
      "machine_url": None, "access": "txt", "auth": "none", "authority": "community", "sg_scope": "filtered", "sg_filter_id": "sgfilter-v1",
      "lifecycle_semantics": "active_list", "provides_times": ["none"], "licence": "MIT", "terms_url": None, "tlp": "TLP:CLEAR",
      "poll_interval_s": 3600, "parser": None, "parser_version": None, "notes": None},
  "phishstats-api": {"record_type": "source", "source_id": "phishstats-api", "name": "PhishStats public API",
      "publisher_entity_id": "phishstats.info", "url": "https://phishstats.info/", "machine_url": "https://api.phishstats.info/api/phishing",
      "access": "api_documented", "auth": "none", "authority": "community", "sg_scope": "filtered", "sg_filter_id": "sgfilter-v1",
      "lifecycle_semantics": "event_stream", "provides_times": ["first_seen", "last_seen"], "licence": None, "terms_url": None,
      "tlp": "TLP:CLEAR", "poll_interval_s": 3600, "parser": None, "parser_version": None, "notes": "50 req/day anonymous"},
}

INDS, SIGS, REPS, CHECKS = {}, [], [], []
def upsert(t, v, raw, host, native):
    i = ind_id(t, v)
    if i not in INDS: INDS[i] = new_indicator(t, v, raw, host, native)
    elif raw not in INDS[i]["values_raw"]: INDS[i]["values_raw"].append(raw)
    if native: INDS[i]["sg_signals"]["sg_native_source"] = True
    return INDS[i]

# 1. SPF icanact: 3 advisories (newest, an LTA one, the compromised-SME IRAS one)
spf = [json.loads(l) for l in open(ROOT / "advisories.jsonl")]
raw_by_id = {r["id"]: r for r in json.load(open(ROOT / "advisories_raw.json"))}
pick = [spf[0]] + [next(r for r in spf if any("LTA" in b for b in r["impersonated_brands"]) and len(r["scam_domains"]) > 1)] \
       + [next(r for r in spf if any("nakadaniko" in d for d in r["scam_domains"]))]
for r in pick:
    rid = f"spf-icanact:{r['id']}"
    imp, fict, cats = [], [], []
    for b in r["impersonated_brands"]:
        kind, eid, sector = resolve_brand(b)
        if kind == "real": imp.append(eid)
        elif kind == "fict": fict.append(eid)
    for c in r["scam_categories"]:
        m = SPF_CAT.get(c)
        if c == "Impersonation":
            m = "impersonation.government" if any(e.endswith(".gov.sg") or "#" in e and e.split("#")[0].endswith(".gov.sg") for e in imp) else "impersonation.other"
        if m: cats.append(m)
    ids = []
    for d in r["scam_domains"]:
        p = parse_host_or_url(d)
        if not p: continue
        t, v, host = p
        ind = upsert(t, v, d, host, native=True)
        for k, src in (("impersonated_entity_ids", imp), ("fictitious_brand_ids", fict), ("categories", cats),
                       ("issuer_entity_ids", ["police.gov.sg"]), ("report_ids", [rid])):
            ind[k] = sorted(set(ind[k]) | set(src))
        if imp and not host.endswith(".gov.sg"):
            reg = host_info(host)["registrable_domain"]; sub = host[: -len(reg)].rstrip(".")
            for e in imp:
                tok = e.split(".")[0]
                if tok in reg.replace("-", ""):
                    ind["lookalike_of"].append({"entity_id": e, "official_domain": e, "method": "brand_token", "score": 0.9})
                elif tok in sub.replace("-", ""):
                    ind["lookalike_of"].append({"entity_id": e, "official_domain": e, "method": "subdomain_abuse", "score": 0.8})
        if host.startswith("iras.") and host.endswith(".com.sg"): ind["host"]["is_compromised_legit"] = True
        SIGS.append(new_sighting(ind, "spf-icanact", rid, "ioc", r["published"], r["modified"], "listed",
                                 {"scam_site_urls_entry": d, "advisory_id": r["id"]}))
        ids.append(ind["indicator_id"])
    rr = raw_by_id[r["id"]]
    REPS.append({"record_type": "report", "report_id": rid, "source_id": "spf-icanact", "native_id": r["id"], "url": r["url"],
                 "issuer_entity_id": "police.gov.sg", "title": r["title"], "summary": (r["body_md"] or "")[:280], "body_md": r["body_md"],
                 "language": "en", "published_at": r["published"], "modified_at": r["modified"], "categories": sorted(set(cats)),
                 "categories_raw": r["scam_categories"], "impersonated_entity_ids": sorted(set(imp)), "fictitious_brand_ids": sorted(set(fict)),
                 "brand_tags_raw": r["impersonated_brands"], "indicator_ids": ids, "media": r["images"],
                 "status": "updated" if r["modified"] != r["published"] else "published", "first_ingested_at": iso(NOW),
                 "last_ingested_at": iso(NOW), "withdrawn_at": None,
                 "raw_sha256": hashlib.sha256(json.dumps(rr, sort_keys=True).encode()).hexdigest(), "tlp": "TLP:CLEAR"})

# 2. MAS IAL: first listing with website + phone + email
mas = json.load(open(SCRATCH / "mas_ial_source.json"))["response"]["docs"]
m = next(x for x in mas if x["website_s"].strip() and x["phonenumber_s"].strip() and x["email_s"].strip())
rid = f"mas-ial-opensanctions:{m['id']}"; ids = []
first = m.get("date_dt") or m["modifieddate_dt"]
def mas_sight(ind, raw):
    for k, src in (("categories", ["unlicensed_financial"]), ("issuer_entity_ids", ["mas.gov.sg"]), ("report_ids", [rid])):
        ind[k] = sorted(set(ind[k]) | set(src))
    SIGS.append(new_sighting(ind, "mas-ial-opensanctions", rid, "ioc", first, m["modifieddate_dt"], "listed", raw)); ids.append(ind["indicator_id"])
for nm in re.split(r"\s*[,;/]\s*|\n", m["unregulatedpersons_s"]):   # MAS packs aliases/websites into the name field
    nm = nm.strip()
    if nm and not re.fullmatch(r"(?:https?://)?(?:[\w-]+\.)+[a-z]{2,}/?", nm, re.I):
        mas_sight(upsert("entity_name", nm.lower(), nm, None, True), {"field": "unregulatedpersons_s"})
for w in re.findall(r"(?:https?://)?(?:[\w-]+\.)+[a-z]{2,}(?:/[^\s,]*)?", m["website_s"], re.I):
    p = parse_host_or_url(w)
    if p: mas_sight(upsert(p[0], p[1], w, p[2], True), {"field": "website_s", "raw_value": m["website_s"][:200]})
for ph in re.split(r"[;,/\n]+", m["phonenumber_s"]):
    try:
        n = phonenumbers.parse(ph.strip(), "SG")
        if phonenumbers.is_possible_number(n):
            v = phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
            mas_sight(upsert("phone", v, ph.strip(), None, True), {"field": "phonenumber_s"})
    except phonenumbers.NumberParseException: pass
for em in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", m["email_s"]):
    mas_sight(upsert("email", em.lower(), em, None, True), {"field": "email_s"})
REPS.append({"record_type": "report", "report_id": rid, "source_id": "mas-ial-opensanctions", "native_id": m["id"], "url": m["url"].replace(" ", "%20"),
             "issuer_entity_id": "mas.gov.sg", "title": f"Investor Alert List: {m['unregulatedpersons_s']}", "summary": None, "body_md": None,
             "language": "en", "published_at": first, "modified_at": m["modifieddate_dt"], "categories": ["unlicensed_financial"],
             "categories_raw": [m["agency_custom_categories"]], "impersonated_entity_ids": [], "fictitious_brand_ids": [], "brand_tags_raw": [],
             "indicator_ids": ids, "media": [], "status": "published", "first_ingested_at": iso(NOW), "last_ingested_at": iso(NOW),
             "withdrawn_at": None, "raw_sha256": hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest(), "tlp": "TLP:CLEAR"})

# 3. Phishing.Database ACTIVE: two SG kit URLs through sgfilter tiers
hits = []
for line in open(SCRATCH / "phishdb_links_active_sg.txt", errors="ignore"):
    l = line.strip().lower()
    if ("paylah" in l or "/bank/dbs/" in l) and len(hits) < 2 and not any(l.split("/")[2] == h.split("/")[2] for h in hits if "//" in h and "//" in l):
        hits.append(line.strip())
    if len(hits) == 2: break
for u in hits:
    p = parse_host_or_url(u)
    ind = upsert(p[0], p[1], u, p[2], False)
    ind["categories"] = sorted(set(ind["categories"]) | {"phishing.banking"})
    if "dbs" in u.lower() or "paylah" in u.lower():
        ind["lookalike_of"].append({"entity_id": "dbs.com.sg", "official_domain": "dbs.com.sg", "method": "path_kit" if PATH_KIT.search(u.lower()) else "brand_token", "score": 0.7})
        ind["impersonated_entity_ids"] = sorted(set(ind["impersonated_entity_ids"]) | {"dbs.com.sg"})
    SIGS.append(new_sighting(ind, "phishdb-links-active", None, "ioc", None, None, "ACTIVE", {"list": "phishing-links-ACTIVE.txt"}))

# 4. PhishStats: the carousell kit record (has its own date/date_update/http_code)
ps = json.load(open(SCRATCH / "phishstats_carousell.json"))[0]
p = parse_host_or_url(ps["url"]); ind = upsert(p[0], p[1], ps["url"], p[2], False)
ind["categories"] = sorted(set(ind["categories"]) | {"phishing.banking"})
ind["lookalike_of"].append({"entity_id": "carousell.sg", "official_domain": "carousell.sg", "method": "brand_token", "score": 0.7})
ind["impersonated_entity_ids"] = sorted(set(ind["impersonated_entity_ids"]) | {"carousell.sg", "dbs.com.sg"})
SIGS.append(new_sighting(ind, "phishstats-api", None, "ioc", ps["date"].replace(".000Z", "Z"), ps["date_update"].replace(".000Z", "Z"),
                         f"http_code={ps['http_code']}", {k: ps[k] for k in ("id", "asn", "isp", "score", "domain_registered_n_days_ago", "tags")}))

# 5. Real liveness checks (DNS + RDAP) on two SPF hostnames
to_check = [i for i in INDS.values() if "spf-icanact:" + spf[0]["id"] in i["report_ids"]][:1]
to_check += [i for i in INDS.values() if i["type"] == "domain" and not i["host"]["is_shared_platform"]
             and any(r.startswith("spf-icanact") for r in i["report_ids"])][:2]
for ind in {i["indicator_id"]: i for i in to_check}.values():
    CHECKS.append(check(ind))

# derive lifecycle for every indicator
for i in INDS.values():
    derive(i, [s for s in SIGS if s["indicator_id"] == i["indicator_id"]], SOURCES)

# 6. feed events: denormalised snapshot of the first SPF indicator
def snapshot(i):
    return {k: i[k] for k in ("indicator_id", "type", "value", "value_defanged", "status", "status_reason", "first_seen", "last_seen",
                              "valid_until", "confidence", "categories", "impersonated_entity_ids", "issuer_entity_ids", "report_ids", "tlp")} | \
           {"registrable_domain": (i["host"] or {}).get("registrable_domain"), "block_scope": (i["host"] or {}).get("block_scope"),
            "liveness": {k: i["liveness"][k] for k in ("state", "last_checked_at", "last_live_at", "registration_expires_at")}}
checked = [i for i in INDS.values() if i["liveness"]["last_checked_at"]]
EVENTS = [{"record_type": "feed_event", "seq": n + 1, "emitted_at": iso(NOW), "op": "upsert", "object_type": "indicator",
           "object_id": i["indicator_id"], "version": 1, "changed_fields": ["*"], "previous_status": None, "snapshot": snapshot(i)}
          for n, i in enumerate(checked)]

# ---- validate + write ----
schema = json.load(open(ROOT / "schema" / "sg_scam_intel.schema.json"))
V = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
groups = {"sources": list(SOURCES.values()), "reports": REPS, "indicators": list(INDS.values()), "sightings": SIGS,
          "liveness_checks": CHECKS, "feed_events": EVENTS}
bad = 0
for name, recs in groups.items():
    for r in recs:
        errs = sorted(V.iter_errors(r), key=lambda e: e.path)
        if errs:
            bad += 1
            best = jsonschema.exceptions.best_match(errs)
            print(f"INVALID {name} {r.get(next(k for k in r if k.endswith('_id')), '')}: {best.message[:160]} @ {list(best.absolute_path)}")
    json.dump(recs, open(OUT / f"{name}.json", "w"), indent=1, ensure_ascii=False)
print({k: len(v) for k, v in groups.items()}, "| invalid:", bad)
for i in INDS.values():
    print(f"  {i['type']:11} {i['value'][:60]:60} status={i['status']:10} conf={i['confidence']} live={i['liveness']['state']:8} "
          f"valid_until={i['valid_until'][:10]} imp={i['impersonated_entity_ids']} sg={i['sg_signals']['score']}")
for c in CHECKS:
    print("  CHECK", c["indicator_id"], c["dns"]["rcode"], c["dns"]["a"][:2], "rdap:", (c["rdap"] or {}).get("expires_at"), (c["rdap"] or {}).get("status"), (c["rdap"] or {}).get("error"), "->", c["verdict"])
