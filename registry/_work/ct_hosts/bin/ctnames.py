#!/usr/bin/env python3
"""Summarise names in saved crt.sh JSON files: name -> first/last not_before, last not_after, n certs, issuers."""
import json, sys, os, collections
def load(f):
    out = collections.defaultdict(lambda: {"first": None, "last": None, "last_exp": None, "n": 0, "issuers": set()})
    for r in json.load(open(f)):
        nb, na = r["not_before"][:10], r["not_after"][:10]
        iss = r["issuer_name"].split("CN=")[-1] if "CN=" in r["issuer_name"] else r["issuer_name"]
        for n in r["name_value"].lower().split("\n"):
            n = n.strip()
            if not n: continue
            d = out[n]
            d["first"] = min(filter(None, [d["first"], nb]))
            d["last"] = max(filter(None, [d["last"], nb]))
            d["last_exp"] = max(filter(None, [d["last_exp"], na]))
            d["n"] += 1; d["issuers"].add(iss)
    return out
if __name__ == "__main__":
    for f in sys.argv[1:]:
        o = load(f)
        print(f"### {os.path.basename(f)}: {len(o)} names")
        for n in sorted(o, key=lambda x: (x.lstrip('*.').split('.')[::-1], x)):
            d = o[n]
            print(f"  {n:52s} {d['first']}..{d['last']} exp {d['last_exp']} n={d['n']} {','.join(sorted(d['issuers']))[:50]}")
