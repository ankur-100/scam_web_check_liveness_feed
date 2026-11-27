#!/usr/bin/env python3
"""Merge records_*.json (dicts keyed by brand_value) with input tag_ids + SPF advisory URLs
and write registry/spf_brand_map.json (checkpointable: only resolved brands are written)."""
import json, glob, collections
BASE='/home/ankur/scamtrends_feed/'
brands=json.load(open(BASE+'registry/spf_brands.json'))
rows=[json.loads(l) for l in open(BASE+'advisories.jsonl')]
adv=collections.defaultdict(list)
for r in rows:
    for b in r['impersonated_brands']:
        adv[b].append(r['url'])
recs={}
for fn in sorted(glob.glob(BASE+'registry/_work/brand_map/records_*.json')):
    for k,v in json.load(open(fn)).items():
        recs[k]=v
RES={'real_entity','fictitious_scam_brand','generic_or_placeholder','ambiguous'}
out=[]
for b in brands:
    bv=b['brand_value']
    if bv not in recs: continue
    r=recs[bv]
    assert r['resolution'] in RES, bv
    ev=list(r.get('evidence',[]))
    for u in adv[bv][:2]:
        if u not in ev: ev.append(u)
    out.append({
        'brand_value': bv, 'tag_id': b['tag_id'], 'resolution': r['resolution'],
        'entity_id': r.get('entity_id'), 'official_domains': r.get('official_domains',[]),
        'is_singapore_entity': r.get('is_singapore_entity'), 'sector': r.get('sector'),
        'confidence': r['confidence'], 'evidence': ev, 'notes': r.get('notes','')})
json.dump(out, open(BASE+'registry/spf_brand_map.json','w'), indent=1, ensure_ascii=False)
missing=[b['brand_value'] for b in brands if b['brand_value'] not in recs]
extra=[k for k in recs if k not in {b['brand_value'] for b in brands}]
print(f"wrote {len(out)} records; missing {len(missing)}; extra keys {extra}")
print(collections.Counter(r['resolution'] for r in out))
