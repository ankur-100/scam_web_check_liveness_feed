#!/usr/bin/env python3
"""ONE GET of https://<host>/ (redirects followed) per host; record status, final URL, <title>.
usage: http_root.py <http.json> host [host ...]   (merges; skips hosts already recorded)"""
import json, os, re, sys, html, time
import requests
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
out = sys.argv[1]
db = json.load(open(out)) if os.path.exists(out) else {}
for h in sys.argv[2:]:
    if h in db: continue
    rec = {}
    try:
        r = requests.get(f"https://{h}/", headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8",
                         "Accept-Language": "en-SG,en;q=0.9"}, timeout=25, allow_redirects=True, stream=True)
        body = b""
        for chunk in r.iter_content(16384):
            body += chunk
            if len(body) > 400000: break
        r.close()
        rec["http_status"] = r.status_code
        chain = [x.status_code for x in r.history]
        if r.url.rstrip("/") != f"https://{h}":
            rec["final_url"] = r.url + (f" (via {','.join(map(str, chain))})" if chain else "")
        t = re.search(rb"<title[^>]*>(.*?)</title>", body, re.S | re.I)
        rec["title"] = " ".join(html.unescape(t.group(1).decode("utf-8", "replace")).split())[:200] if t else None
    except Exception as e:
        rec = {"http_status": None, "title": None, "error": f"{type(e).__name__}: {str(e)[:140]}"}
    db[h] = rec
    print(f"{h:42s} {rec.get('http_status')} {rec.get('title')!r:.70} {rec.get('final_url','')[:80]} {rec.get('error','')[:80]}", flush=True)
    json.dump(db, open(out, "w"), indent=1, sort_keys=True)
    time.sleep(1.5)
