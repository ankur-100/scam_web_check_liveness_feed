#!/usr/bin/env python3
"""Resolve hosts via the system resolver using dig (A records, CNAME chain, rcode).
usage: dns.py <dns.json> host [host ...]   (merges into dns.json)
resolves: true (A present) / false (NXDOMAIN or NOERROR without A) / null (timeout/SERVFAIL = unknown)"""
import json, re, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
out = sys.argv[1]
hosts = sys.argv[2:]
def q(h):
    try:
        p = subprocess.run(["dig", "+time=5", "+tries=2", "+noall", "+comments", "+answer", h, "A"],
                           capture_output=True, text=True, timeout=30)
        t = p.stdout
    except subprocess.TimeoutExpired:
        return h, {"resolves": None, "a_records": [], "note": "DNS TIMEOUT (unknown)"}
    m = re.search(r"status: (\w+)", t)
    st = m.group(1) if m else ("TIMEOUT" if "timed out" in t or p.returncode == 9 else f"rc{p.returncode}")
    a, cn = [], []
    for line in t.splitlines():
        if line.startswith(";") or not line.strip(): continue
        f = line.split()
        if len(f) >= 5 and f[3] == "A": a.append(f[4])
        if len(f) >= 5 and f[3] == "CNAME": cn.append(f[4].rstrip("."))
    if a: res = True
    elif st in ("NXDOMAIN", "NOERROR"): res = False
    else: res = None
    note = f"DNS {st}" + (f" CNAME {' -> '.join(cn)}" if cn else "")
    if res is None: note += " (unknown, not treated as non-resolving)"
    return h, {"resolves": res, "a_records": a, "status": st, "cname": cn, "note": note}
db = json.load(open(out)) if os.path.exists(out) else {}
with ThreadPoolExecutor(8) as ex:
    for h, r in ex.map(q, hosts):
        db[h] = r
json.dump(db, open(out, "w"), indent=1, sort_keys=True)
from collections import Counter
print(Counter(str(db[h]["resolves"]) for h in hosts), Counter(db[h].get("status") for h in hosts))
