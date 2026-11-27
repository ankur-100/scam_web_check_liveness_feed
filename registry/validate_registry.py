#!/usr/bin/env python3
"""Validate a partial entities JSON file against registry/FORMAT.md (entity records).
Usage: python3 validate.py <file.json> [more.json ...]
"""
import json, re, sys

TOP_KEYS = ["entity_id", "name", "abbr", "aliases", "sector", "parent_entity_id", "country",
            "official_domains", "official_hosts", "scam_info", "official_channels", "evidence", "notes"]
SECTORS = set("gov.ministry gov.statboard gov.organ gov.dept gov.programme gov.court quasi_gov bank payments "
              "telco logistics ecommerce marketplace transport utility retail travel media brokerage insurance "
              "healthcare tech_platform crypto other".split())
SI_KEYS = ["url", "kind", "lists_indicators", "access", "machine_url", "item_count", "latest_item_date",
           "verified", "sample", "notes"]
KINDS = set("advisory_feed alert_page scam_faq official_channels fake_indicator_list news_releases report_portal statistics".split())
INDS = set("domain url phone email sms_sender_id app social_handle bank_account entity_name".split())
ACCESS = set("html rss atom sitemap json_api_documented csv pdf".split())
OC_KEYS_REQUIRED = ["sms_sender_ids", "hotlines", "short_link_domains", "social"]
OC_KEYS_EXTRA_OK = ["apps", "emails"]  # additive extension, flagged to caller
DOM_RE = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
ID_RE = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+(#[a-z0-9-]+)?$")
DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

def err(msgs, eid, m):
    msgs.append(f"[{eid}] {m}")

def check(rec, msgs, seen):
    eid = rec.get("entity_id", "?")
    keys = list(rec.keys())
    for k in TOP_KEYS:
        if k not in rec:
            err(msgs, eid, f"missing key {k}")
    for k in keys:
        if k not in TOP_KEYS:
            err(msgs, eid, f"unknown top-level key {k}")
    if not isinstance(eid, str) or not ID_RE.match(eid):
        err(msgs, eid, "entity_id not a lowercase registrable domain (optionally #slug)")
    if eid in seen:
        err(msgs, eid, "duplicate entity_id")
    seen.add(eid)
    if rec.get("sector") not in SECTORS:
        err(msgs, eid, f"bad sector {rec.get('sector')}")
    for k in ("aliases", "official_domains", "official_hosts", "scam_info", "evidence"):
        if not isinstance(rec.get(k), list):
            err(msgs, eid, f"{k} must be a list")
    for d in rec.get("official_domains") or []:
        if not DOM_RE.match(d) or d.startswith("www."):
            err(msgs, eid, f"official_domains entry not a bare registrable domain: {d}")
    base = eid.split("#")[0]
    if rec.get("official_domains") and base not in rec["official_domains"]:
        err(msgs, eid, f"entity_id domain {base} not in official_domains")
    for h in rec.get("official_hosts") or []:
        if not DOM_RE.match(h):
            err(msgs, eid, f"official_hosts entry not a hostname: {h}")
    for e in rec.get("evidence") or []:
        if not str(e).startswith("http"):
            err(msgs, eid, f"evidence not a URL: {e}")
    if not rec.get("evidence"):
        err(msgs, eid, "evidence is empty")
    for i, si in enumerate(rec.get("scam_info") or []):
        for k in SI_KEYS:
            if k not in si:
                err(msgs, eid, f"scam_info[{i}] missing {k}")
        for k in si:
            if k not in SI_KEYS:
                err(msgs, eid, f"scam_info[{i}] unknown key {k}")
        if si.get("kind") not in KINDS:
            err(msgs, eid, f"scam_info[{i}] bad kind {si.get('kind')}")
        if si.get("access") not in ACCESS:
            err(msgs, eid, f"scam_info[{i}] bad access {si.get('access')}")
        li = si.get("lists_indicators")
        if not isinstance(li, list) or any(x not in INDS for x in li):
            err(msgs, eid, f"scam_info[{i}] bad lists_indicators {li}")
        ic = si.get("item_count")
        if ic is not None and not isinstance(ic, int):
            err(msgs, eid, f"scam_info[{i}] item_count must be int or null")
        d = si.get("latest_item_date")
        if d is not None and not DATE_RE.match(str(d)):
            err(msgs, eid, f"scam_info[{i}] latest_item_date not ISO: {d}")
        if not str(si.get("url", "")).startswith("http"):
            err(msgs, eid, f"scam_info[{i}] url not http(s)")
        v = si.get("verified")
        if not (isinstance(v, str) and v.startswith("2026-")):
            err(msgs, eid, f"scam_info[{i}] verified should look like '2026-11-25 HTTP 200' (got {v})")
    oc = rec.get("official_channels")
    if not isinstance(oc, dict):
        err(msgs, eid, "official_channels must be an object")
    else:
        for k in OC_KEYS_REQUIRED:
            if not isinstance(oc.get(k), list):
                err(msgs, eid, f"official_channels.{k} must be a list")
        for k in oc:
            if k not in OC_KEYS_REQUIRED + OC_KEYS_EXTRA_OK:
                err(msgs, eid, f"official_channels unknown key {k}")
            elif not isinstance(oc[k], list):
                err(msgs, eid, f"official_channels.{k} must be a list")

def main():
    total, allmsgs, seen = 0, [], set()
    for fn in sys.argv[1:]:
        data = json.load(open(fn))
        if not isinstance(data, list):
            print(f"{fn}: top level must be an array"); sys.exit(1)
        for rec in data:
            check(rec, allmsgs, seen)
        total += len(data)
        print(f"{fn}: {len(data)} records")
    for m in allmsgs:
        print("  -", m)
    print(f"TOTAL {total} records, {len(allmsgs)} problems")
    sys.exit(1 if allmsgs else 0)

if __name__ == "__main__":
    main()
