#!/usr/bin/env python3
"""Polite robots.txt -> sitemap -> keyword sweep. Usage: python3 sweep.py host1 host2 ...
Only fetches robots.txt, sitemaps declared there (else /sitemap.xml once) and child sitemaps (<=MAX_CHILD).
Writes sweep/<host>.json (summary+matches) and sweep/<host>.urls.tsv (all urls + lastmod)."""
import gzip, json, os, re, sys, time
from urllib import robotparser
from urllib.parse import urlparse
import requests
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
KW = re.compile(r"scam|fraud|phish|impersonat|fake|hoax|spoof|beware|advisor|alert|unsolicited", re.I)
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-SG,en;q=0.9"})
MAX_CHILD = int(os.environ.get("MAX_CHILD", "40"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep")
DELAY = 0.8
def get(url):
    try: r = S.get(url, timeout=40, allow_redirects=True)
    except Exception as e: r = e
    time.sleep(DELAY); return r
def body(r):
    c = r.content
    if c[:2] == b"\x1f\x8b":
        try: c = gzip.decompress(c)
        except Exception: pass
    return c.decode("utf-8", errors="replace")
def parse(txt):
    kind = "index" if re.search(r"<(?:\w+:)?sitemapindex", txt[:5000], re.I) else "urlset"
    tag = "sitemap" if kind == "index" else "url"; items = []
    for blk in re.findall(rf"<(?:\w+:)?{tag}\b[^>]*>(.*?)</(?:\w+:)?{tag}>", txt, re.S | re.I):
        loc = re.search(r"<(?:\w+:)?loc>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</(?:\w+:)?loc>", blk, re.S | re.I)
        lm = re.search(r"<(?:\w+:)?lastmod>\s*(.*?)\s*</(?:\w+:)?lastmod>", blk, re.S | re.I)
        if loc: items.append((loc.group(1).strip().replace("&amp;", "&"), lm.group(1).strip() if lm else None))
    return kind, items
def sweep(host):
    global DELAY
    res = {"host": host, "robots_status": None, "robots": None, "sitemaps_declared": [], "sitemaps_fetched": [],
           "errors": [], "total_urls": 0, "hosts_in_sitemap": {}, "matches": []}
    base = f"https://{host}"
    r = get(base + "/robots.txt"); rp = robotparser.RobotFileParser()
    if isinstance(r, Exception): res["robots_status"] = "ERR " + type(r).__name__; rtxt = ""
    else:
        res["robots_status"] = r.status_code; rtxt = body(r) if r.status_code == 200 else ""
        if "<html" in rtxt[:600].lower(): rtxt = ""; res["robots_status"] = f"{r.status_code} (html, not robots)"
    res["robots"] = rtxt[:3000]; rp.parse(rtxt.splitlines())
    cd = re.search(r"(?im)^crawl-delay:\s*([\d.]+)", rtxt)
    DELAY = max(0.8, float(cd.group(1))) if cd else 0.8
    sms = re.findall(r"(?im)^sitemap:\s*(\S+)", rtxt); res["sitemaps_declared"] = sms
    queue = [s if s.startswith("http") else base + s for s in sms] or [base + "/sitemap.xml"]
    seen = set(); urls = []; nchild = 0
    while queue and nchild < MAX_CHILD:
        sm = queue.pop(0)
        if sm in seen: continue
        seen.add(sm)
        if not rp.can_fetch(UA, sm): res["errors"].append([sm, "robots-disallowed"]); continue
        r = get(sm); nchild += 1
        if isinstance(r, Exception): res["errors"].append([sm, "ERR " + type(r).__name__]); continue
        if r.status_code != 200: res["errors"].append([sm, r.status_code]); continue
        t = body(r)
        if "<html" in t[:600].lower() and "<urlset" not in t[:3000] and "<sitemapindex" not in t[:3000]:
            res["errors"].append([sm, "html returned"]); continue
        kind, items = parse(t); res["sitemaps_fetched"].append([sm, kind, len(items), r.url])
        if kind == "index": queue.extend(i[0] for i in items)
        else: urls.extend(items)
    res["total_urls"] = len(urls)
    for u, lm in urls:
        h = urlparse(u).netloc; res["hosts_in_sitemap"][h] = res["hosts_in_sitemap"].get(h, 0) + 1
        if KW.search(urlparse(u).path): res["matches"].append([u, lm])
    with open(f"{OUT}/{host}.urls.tsv", "w") as f:
        for u, lm in urls: f.write(f"{u}\t{lm or ''}\n")
    json.dump(res, open(f"{OUT}/{host}.json", "w"), indent=1)
    lms = sorted([m[1] for m in res["matches"] if m[1]])
    print(f"{host}: robots={res['robots_status']} decl={len(sms)} fetched={len(res['sitemaps_fetched'])} urls={len(urls)} "
          f"matches={len(res['matches'])} newest_match_lastmod={lms[-1] if lms else None} errs={res['errors'][:3]}", flush=True)
if __name__ == "__main__":
    for h in sys.argv[1:]:
        try: sweep(h)
        except Exception as e: print(h, "FAILED", e, flush=True)
