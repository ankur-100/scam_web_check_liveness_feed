"""Polite HTTP fetcher: robots.txt (cached 24h), per-host spacing, conditional GET, size cap. Official/feed URLs only —
never used against indicator (scam) hosts."""
import time, urllib.parse, urllib.robotparser, requests

UA = "Mozilla/5.0 (compatible; sgintel-crawler/0.1; SG scam-advisory aggregation research)"
PER_HOST_GAP_S = 2.0
MAX_BYTES = 120 * 1024 * 1024
_last_hit, _robots = {}, {}
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept-Language": "en-SG,en;q=0.9"})

def robots_ok(url):
    u = urllib.parse.urlsplit(url); base = f"{u.scheme}://{u.netloc}"
    rp, ts = _robots.get(base, (None, 0))
    if rp is None or time.time() - ts > 86400:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = S.get(base + "/robots.txt", timeout=15)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            rp.parse([])
        _robots[base] = (rp, time.time())
    return rp.can_fetch(UA, url)

def get(url, etag=None, last_modified=None, params=None, timeout=45):
    host = urllib.parse.urlsplit(url).hostname
    wait = PER_HOST_GAP_S - (time.time() - _last_hit.get(host, 0))
    if wait > 0: time.sleep(wait)
    h = {}
    if etag: h["If-None-Match"] = etag
    if last_modified: h["If-Modified-Since"] = last_modified
    t0 = time.time()
    try:
        r = S.get(url, headers=h, params=params, timeout=timeout, stream=True)
        body = b""
        for chunk in r.iter_content(1 << 16):
            body += chunk
            if len(body) > MAX_BYTES: r.close(); return {"status": r.status_code, "error": "size cap exceeded", "body": b"", "ms": int((time.time()-t0)*1000)}
        return {"status": r.status_code, "body": body, "etag": r.headers.get("ETag"), "last_modified": r.headers.get("Last-Modified"),
                "final_url": r.url, "ctype": r.headers.get("Content-Type", ""), "ms": int((time.time() - t0) * 1000), "error": None}
    except requests.RequestException as e:
        return {"status": None, "body": b"", "error": f"{type(e).__name__}: {str(e)[:120]}", "ms": int((time.time() - t0) * 1000)}
    finally:
        _last_hit[host] = time.time()
