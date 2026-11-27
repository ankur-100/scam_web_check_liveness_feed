#!/usr/bin/env python3
"""upsert.py rec.json  -> insert/replace record(s) by entity_id in the entities file, then validate."""
import json, sys, subprocess
OUT = "/home/ankur/scamtrends_feed/registry/entities_gov_economic_social.json"
try: data = json.load(open(OUT))
except Exception: data = []
new = json.load(open(sys.argv[1])); new = new if isinstance(new, list) else [new]
idx = {r["entity_id"]: i for i, r in enumerate(data)}
for r in new:
    if r["entity_id"] in idx: data[idx[r["entity_id"]]] = r
    else: data.append(r)
json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
subprocess.run(["python3", "/home/ankur/scamtrends_feed/registry/validate_registry.py", OUT])
