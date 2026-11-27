"""Merge research registry files into canonical schema records + a human-readable registry table.

inputs  (registry/):  entities_*.json (FORMAT §1), spf_brand_map.json (§3), hosts_ct.json (§2)
outputs (registry/merged/): entities.json, sources.json, hosts.json (schema-validated), REGISTRY.md, allowlist.txt
run: .venv/bin/python registry/merge_registry.py
"""
import glob, json, re, datetime as dt
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]; REG = ROOT / "registry"; OUT = REG / "merged"; OUT.mkdir(exist_ok=True)
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
schema = json.load(open(ROOT / "schema" / "sg_scam_intel.schema.json"))
V = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
ID_RE = re.compile(schema["$defs"]["entity_id"]["pattern"])
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def load(p):
    try: return json.load(open(p))
    except (FileNotFoundError, json.JSONDecodeError) as e: print(f"skip {Path(p).name}: {e.__class__.__name__}"); return []

# ---- entities from research files ----
ents, prov = {}, {}
for f in sorted(glob.glob(str(REG / "entities_*.json"))):
    for r in load(f):
        eid = (r.get("entity_id") or "").lower()
        if not ID_RE.match(eid): print(f"  bad entity_id {eid!r} in {Path(f).name}"); continue
        oc = r.get("official_channels") or {}
        e = ents.setdefault(eid, {"record_type": "entity", "entity_id": eid, "name": r.get("name") or eid, "abbr": r.get("abbr"),
                                  "aliases": [], "kind": "programme" if "#" in eid else "organisation", "sector": r.get("sector") or "other",
                                  "country": r.get("country") or "SG", "parent_entity_id": r.get("parent_entity_id"),
                                  "official": {k: [] for k in ("domains", "hosts", "sms_sender_ids", "hotlines", "short_link_domains", "social")},
                                  "scam_info_source_ids": [], "external_ids": {"spf_brand_tag_ids": [], "opensanctions_id": None, "sgdi_url": None, "uen": None},
                                  "evidence": [], "verified_at": NOW, "notes": r.get("notes") or None})
        prov.setdefault(eid, set()).add(Path(f).stem)
        def add(lst, vals): lst.extend(v for v in (vals or []) if v and v not in lst)
        add(e["aliases"], r.get("aliases")); add(e["evidence"], r.get("evidence"))
        add(e["official"]["domains"], [d.lower() for d in r.get("official_domains") or []])
        add(e["official"]["hosts"], [h.lower() for h in r.get("official_hosts") or []])
        for k in ("sms_sender_ids", "hotlines", "short_link_domains", "social"): add(e["official"][k], oc.get(k))
        e["_scam_info"] = e.get("_scam_info", []) + (r.get("scam_info") or [])
        e["_apps"] = e.get("_apps", []) + (oc.get("apps") or [])

# ---- SPF brand map: aliases + tag ids; fictitious brands become brand:<slug> entities ----
bmap = load(REG / "spf_brand_map.json")
brand_to_entity = {}
for b in bmap:
    res, eid = b.get("resolution"), (b.get("entity_id") or "").lower() or None
    if res == "real_entity" and eid and ID_RE.match(eid):
        e = ents.setdefault(eid, {"record_type": "entity", "entity_id": eid, "name": b["brand_value"], "abbr": None, "aliases": [],
                                  "kind": "organisation", "sector": b.get("sector") or "other",
                                  "country": "SG" if b.get("is_singapore_entity") else "ZZ", "parent_entity_id": None,
                                  "official": {k: [] for k in ("domains", "hosts", "sms_sender_ids", "hotlines", "short_link_domains", "social")},
                                  "scam_info_source_ids": [], "external_ids": {"spf_brand_tag_ids": [], "opensanctions_id": None, "sgdi_url": None, "uen": None},
                                  "evidence": [], "verified_at": NOW, "notes": None})
        prov.setdefault(eid, set()).add("spf_brand_map")
        if b["brand_value"] not in e["aliases"]: e["aliases"].append(b["brand_value"])
        for d in b.get("official_domains") or []:
            d = d.lower()
            tgt = e["official"]["domains"] if d.count(".") <= 2 and not d.startswith(("www.",)) else e["official"]["hosts"]
            if d not in tgt: tgt.append(d)
        brand_to_entity[b["brand_value"]] = eid
    elif res == "fictitious_scam_brand":
        eid = "brand:" + slug(b["brand_value"])
        ents.setdefault(eid, {"record_type": "entity", "entity_id": eid, "name": b["brand_value"], "abbr": None, "aliases": [b["brand_value"]],
                              "kind": "fictitious_brand", "country": "ZZ", "parent_entity_id": None,
                              "official": {k: [] for k in ("domains", "hosts", "sms_sender_ids", "hotlines", "short_link_domains", "social")},
                              "scam_info_source_ids": [], "external_ids": {"spf_brand_tag_ids": [], "opensanctions_id": None, "sgdi_url": None, "uen": None},
                              "evidence": b.get("evidence") or [], "verified_at": NOW, "notes": b.get("notes")})
        brand_to_entity[b["brand_value"]] = eid
    else:
        brand_to_entity[b["brand_value"]] = None
    if brand_to_entity.get(b["brand_value"]) and b.get("tag_id"):
        ids = ents[brand_to_entity[b["brand_value"]]]["external_ids"]["spf_brand_tag_ids"]
        if b["tag_id"] not in ids: ids.append(b["tag_id"])

# ---- scam_info pages -> source records ----
ACCESS = {"html": "html", "rss": "rss", "atom": "atom", "sitemap": "sitemap", "json_api_documented": "api_documented", "csv": "csv", "pdf": "pdf"}
SEM = {"advisory_feed": "append_only", "news_releases": "append_only", "alert_page": "append_only", "fake_indicator_list": "snapshot_full",
       "official_channels": "snapshot_full", "scam_faq": "snapshot_full", "report_portal": "snapshot_full", "statistics": "append_only"}
def authority(e):
    s = e.get("sector", "")
    if e["entity_id"] == "mas.gov.sg": return "regulator"
    if s.startswith("gov.") or s == "quasi_gov": return "authoritative"
    return "industry"
sources = {}
for eid, e in ents.items():
    for si in e.pop("_scam_info", []):
        url = si.get("url") or ""
        if not url.startswith("http"): continue
        sid = slug(eid.split("#")[0].split(".")[0] + "-" + re.sub(r"^https?://[^/]+", "", url))[:60] or slug(eid)
        sid = sid if sid not in sources else (sid[:52] + "-" + str(len(sources)))
        sources[sid] = {"record_type": "source", "source_id": sid, "name": f"{e['name']}: {si.get('kind')}", "publisher_entity_id": eid,
                        "url": url, "machine_url": si.get("machine_url"), "access": ACCESS.get(si.get("access"), "html"), "auth": "none",
                        "authority": authority(e), "sg_scope": "native" if e.get("country") == "SG" else "mixed", "sg_filter_id": None,
                        "lifecycle_semantics": SEM.get(si.get("kind"), "snapshot_full"),
                        "provides_times": ["published"] if si.get("latest_item_date") else ["none"], "licence": None, "terms_url": None,
                        "tlp": "TLP:CLEAR", "poll_interval_s": None, "parser": None, "parser_version": None,
                        "notes": "; ".join(x for x in [f"kind={si.get('kind')}", f"indicators={','.join(si.get('lists_indicators') or []) or 'none'}",
                                                        f"items={si.get('item_count')}", f"latest={si.get('latest_item_date')}", f"verified={si.get('verified')}",
                                                        si.get("notes") or ""] if x)}
        sources[sid]["_kind"], sources[sid]["_ind"], sources[sid]["_sample"] = si.get("kind"), si.get("lists_indicators") or [], si.get("sample")
        e["scam_info_source_ids"].append(sid)
    apps = e.pop("_apps", [])
    if apps: e["notes"] = ((e.get("notes") or "") + f" | official apps: {', '.join(apps)}").strip(" |")
    if e.get("sector") is None: e.pop("sector", None)

hosts = load(REG / "hosts_ct.json")

# ---- validate + write ----
bad = 0
for r in list(ents.values()) + [{k: v for k, v in s.items() if not k.startswith("_")} for s in sources.values()]:
    errs = list(V.iter_errors(r))
    if errs:
        bad += 1; best = jsonschema.exceptions.best_match(errs)
        print(f"  INVALID {r['record_type']} {r.get('entity_id') or r.get('source_id')}: {best.message[:140]} @ {list(best.absolute_path)}")
json.dump(sorted(ents.values(), key=lambda x: x["entity_id"]), open(OUT / "entities.json", "w"), indent=1, ensure_ascii=False)
json.dump([{k: v for k, v in s.items() if not k.startswith("_")} for s in sources.values()], open(OUT / "sources.json", "w"), indent=1, ensure_ascii=False)
json.dump(hosts, open(OUT / "hosts.json", "w"), indent=1, ensure_ascii=False)
allow = sorted({d for e in ents.values() for d in e["official"]["domains"] + e["official"]["hosts"]})
open(OUT / "allowlist.txt", "w").write("\n".join(allow) + "\n")

# ---- human-readable registry: entity -> official site -> scam pages ----
L = [f"# SG scam-information registry (generated {NOW})", "",
     f"{sum(1 for e in ents.values() if e['kind'] != 'fictitious_brand')} organisations · "
     f"{sum(1 for e in ents.values() if e['kind'] == 'fictitious_brand')} fictitious scam brands · {len(sources)} scam-info pages · "
     f"{len(allow)} allowlisted domains/hosts · {len(hosts)} CT/discovered hosts", "",
     "Legend: indicators = concrete identifiers the page lists (none = narrative only).", ""]
order = lambda e: (0 if e.get("sector", "").startswith("gov") or e.get("sector") == "quasi_gov" else 1, e.get("sector", ""), e["entity_id"])
cur = None
for e in sorted((e for e in ents.values() if e["kind"] != "fictitious_brand"), key=order):
    grp = "Government & quasi-government" if order(e)[0] == 0 else "Private sector & global brands"
    if grp != cur:
        L += ["", f"## {grp}", "", "| Entity | Sector | Official site(s) | Scam-info pages (kind · indicators · latest) | SPF brand tags |", "|---|---|---|---|---|"]; cur = grp
    site = ", ".join(e["official"]["domains"][:4]) or e["entity_id"]
    pages = "<br>".join(f"[{sources[s]['_kind']}]({sources[s]['url']}) · {','.join(sources[s]['_ind']) or 'none'} · "
                        f"{re.search(r'latest=([^;]+)', sources[s]['notes']).group(1)}" for s in e["scam_info_source_ids"]) or "—"
    tags = len(e["external_ids"]["spf_brand_tag_ids"])
    name = f"{e['name']}" + (f" ({e['abbr']})" if e.get("abbr") else "")
    L.append(f"| {name} | {e.get('sector','')} | {site} | {pages} | {tags or ''} |")
fict = sorted(e["name"] for e in ents.values() if e["kind"] == "fictitious_brand")
if fict: L += ["", "## Fictitious scam brands (SPF `Brand` tags that are scam platforms, not real organisations)", "", ", ".join(fict)]
unres = [b["brand_value"] for b in bmap if not brand_to_entity.get(b["brand_value"])]
if unres: L += ["", "## SPF brand tags not mapped (placeholder / ambiguous)", "", ", ".join(unres)]
if hosts:
    L += ["", "## Scam-relevant hosts discovered (CT logs / lists / search)", "", "| Host | Owner | Via | Resolves | HTTP | Title |", "|---|---|---|---|---|---|"]
    for h in sorted((h for h in hosts if h.get("scam_relevant") in ("yes", "maybe")), key=lambda h: (h.get("scam_relevant") != "yes", h.get("host", ""))):
        L.append(f"| {h.get('host')} | {h.get('owner_entity_id') or ''} | {h.get('discovered_via')} | {h.get('resolves')} | {h.get('http_status') or ''} | {(h.get('title') or '')[:60]} |")
open(OUT / "REGISTRY.md", "w").write("\n".join(L) + "\n")
print(f"entities={len(ents)} sources={len(sources)} hosts={len(hosts)} allowlist={len(allow)} invalid={bad} | brand tags mapped: "
      f"{sum(1 for v in brand_to_entity.values() if v)}/{len(bmap)}")
