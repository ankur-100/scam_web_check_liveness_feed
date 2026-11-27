#!/usr/bin/env python3
"""Compose registry/hosts_ct.json (FORMAT.md section 2) from:
   data/seed.json (manual classification), data/ct_digest.json + data/ct/crtsh_*.json (CT dates),
   data/dns/dns.json (resolution), data/web/http.json (one root GET)."""
import json, glob, os, sys
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/home/ankur/scamtrends_feed/registry/hosts_ct.json"
KEYS = ["host", "registrable_domain", "discovered_via", "cert_first_seen", "cert_last_seen", "resolves",
        "a_records", "http_status", "title", "scam_relevant", "owner_entity_id", "notes"]

def load(p, default):
    try: return json.load(open(p))
    except FileNotFoundError: return default

ct = {}  # name -> [first, last]
def upd(n, a, b):
    if n not in ct: ct[n] = [a, b]; return
    f, l = ct[n]
    ct[n] = [min(x for x in (f, a) if x) if (f or a) else None, max(x for x in (l, b) if x) if (l or b) else None]
for n, (a, b) in load(os.path.join(W, "data/ct_digest.json"), {"names": {}})["names"].items():
    upd(n, a, b)
for f in glob.glob(os.path.join(W, "data/ct/crtsh_*.json")):
    for r in load(f, []):
        nb = r["not_before"][:10]
        for n in r["name_value"].lower().split("\n"):
            n = n.strip()
            if n: upd(n, nb, nb)

seed = load(os.path.join(W, "data/seed.json"), [])
dns = load(os.path.join(W, "data/dns/dns.json"), {})
http = load(os.path.join(W, "data/web/http.json"), {})
out, seen = [], set()
for s in seed:
    h = s["host"].lower()
    if h in seen: continue
    seen.add(h)
    rec = {k: None for k in KEYS}
    rec.update({k: v for k, v in s.items() if k in KEYS})
    if s.get("cert_first_seen") is None and s.get("cert_last_seen") is None:
        rec["cert_first_seen"] = rec["cert_last_seen"] = None
    rec["host"] = h
    c = ct.get(h)
    if c:
        f0, l0 = rec.get("cert_first_seen"), rec.get("cert_last_seen")
        rec["cert_first_seen"] = min(x for x in (f0, c[0]) if x) if (f0 or c[0]) else None
        rec["cert_last_seen"] = max(x for x in (l0, c[1]) if x) if (l0 or c[1]) else None
    d = dns.get(h)
    if d:
        rec["resolves"] = d["resolves"]           # true / false / null(timeout/unknown)
        rec["a_records"] = d.get("a_records") or []
    else:
        rec["a_records"] = rec.get("a_records") or []
    w = http.get(h)
    if w:
        rec["http_status"] = w.get("http_status")
        rec["title"] = w.get("title")
        extra = []
        if w.get("final_url"): extra.append(f"root GET -> {w['final_url']}")
        if w.get("error"): extra.append(f"root GET error: {w['error']}")
        if extra:
            rec["notes"] = ((rec.get("notes") or "") + (" | " if rec.get("notes") else "") + "; ".join(extra))
    if d and d.get("note"):
        rec["notes"] = ((rec.get("notes") or "") + (" | " if rec.get("notes") else "") + d["note"])
    rec["notes"] = rec.get("notes") or ""
    out.append({k: rec.get(k) for k in KEYS})
json.dump(out, open(OUT + ".tmp", "w"), indent=1, ensure_ascii=False)
os.replace(OUT + ".tmp", OUT)
from collections import Counter
print(len(out), "records;", Counter(r["scam_relevant"] for r in out), Counter(r["discovered_via"] for r in out))
