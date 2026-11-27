"""Google Safe Browsing v5 lookup (urls:search) - the source of Chrome's red "dangerous site" interstitial.

Built but OFF in the current layer (SCOPE.md decision D6). Turn on with:
    SGINTEL_SAFEBROWSING=1  SGINTEL_SAFEBROWSING_KEY=<Google Cloud API key>
Free, non-commercial use only (Safe Browsing ToS); an institutional/commercial deployment must switch to Web Risk.
Queries go to Google, never to the scam host. <=50 URLs per call; responses cached for the server's cacheDuration.
"""
import os, time, requests

ENDPOINT = "https://safebrowsing.googleapis.com/v5/urls:search"
KEY = os.environ.get("SGINTEL_SAFEBROWSING_KEY")
ENABLED = os.environ.get("SGINTEL_SAFEBROWSING") == "1" and bool(KEY)
REASON = {"SOCIAL_ENGINEERING": "sb_social_engineering", "MALWARE": "sb_malware", "UNWANTED_SOFTWARE": "sb_unwanted_software",
          "POTENTIALLY_HARMFUL_APPLICATION": "sb_potentially_harmful_app"}
_cache = {}   # url -> (expires_epoch, [threatTypes])


def lookup_url(value, typ):
    return value if typ == "url" else f"http://{value}/"


def lookup(urls):
    """-> {url: {"threats": [...]} | {"error": "..."}}; {} when disabled."""
    if not ENABLED: return {}
    out, todo, t = {}, [], time.time()
    for u in urls:
        c = _cache.get(u)
        if c and c[0] > t: out[u] = {"threats": c[1], "cached": True}
        else: todo.append(u)
    for i in range(0, len(todo), 50):
        batch = todo[i:i + 50]
        try:
            r = requests.get(ENDPOINT, params=[("urls", u) for u in batch] + [("key", KEY)], timeout=20)
            r.raise_for_status(); j = r.json()
        except (requests.RequestException, ValueError) as e:
            for u in batch: out[u] = {"error": f"{type(e).__name__}: {str(e)[:80]}"}
            continue
        ttl = float((j.get("cacheDuration") or "300s").rstrip("s") or 300)
        hits = {}
        for th in j.get("threats") or []:     # matches may be host-suffix/path-prefix expressions of a requested URL
            for u in batch:
                if th.get("url") and (th["url"] == u or u.startswith(th["url"]) or th["url"].rstrip("/") in u):
                    hits.setdefault(u, set()).update(th.get("threatTypes") or [])
        for u in batch:
            types = sorted(hits.get(u, []))
            _cache[u] = (t + ttl, types); out[u] = {"threats": types}
    return out
