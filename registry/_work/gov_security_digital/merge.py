#!/usr/bin/env python3
"""Assemble entities/*.json (one record each) into the registry file, in a stable order, then validate."""
import json, glob, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/ankur/scamtrends_feed/registry/entities_gov_security_digital.json'
recs = []
for f in sorted(glob.glob(os.path.join(D, 'entities', '*.json'))):
    recs.append(json.load(open(f)))
order = json.load(open(os.path.join(D, 'order.json'))) if os.path.exists(os.path.join(D, 'order.json')) else []
recs.sort(key=lambda r: (order.index(r['entity_id']) if r['entity_id'] in order else 999, r['entity_id']))
tmp = OUT + '.tmp'
json.dump(recs, open(tmp, 'w'), indent=1, ensure_ascii=False)
os.replace(tmp, OUT)
r = subprocess.run([sys.executable, '/home/ankur/scamtrends_feed/registry/validate_registry.py', OUT], capture_output=True, text=True)
print(r.stdout[-3000:])
