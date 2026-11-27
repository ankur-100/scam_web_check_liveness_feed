#!/usr/bin/env python3
"""Helpers to build records with all required keys."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
def si(url, kind, access='html', lists=None, machine_url=None, item_count=None, latest=None, verified='2026-11-26 HTTP 200', sample='', notes=''):
    return {"url": url, "kind": kind, "lists_indicators": lists or [], "access": access, "machine_url": machine_url,
            "item_count": item_count, "latest_item_date": latest, "verified": verified, "sample": sample, "notes": notes}
def rec(entity_id, name, abbr, aliases, sector, parent, domains, hosts, scam_info, channels=None, evidence=None, notes=''):
    oc = {"sms_sender_ids": [], "hotlines": [], "short_link_domains": [], "social": []}
    oc.update(channels or {})
    return {"entity_id": entity_id, "name": name, "abbr": abbr, "aliases": aliases, "sector": sector,
            "parent_entity_id": parent, "country": "SG", "official_domains": domains, "official_hosts": hosts,
            "scam_info": scam_info, "official_channels": oc, "evidence": evidence or [], "notes": notes}
def save(r):
    fn = os.path.join(D, 'entities', r['entity_id'].replace('#', '__') + '.json')
    json.dump(r, open(fn, 'w'), indent=1, ensure_ascii=False)
    print('saved', fn)
