"""Contained HTTP probe of a listed scam site (SCOPE.md §6, policy P1). Fails closed if the egress proxy is down.

One GET per hop, through the egress proxy only: no JavaScript, no rendering, no sub-resources, no cookies kept, no forms,
<=5 redirects (each recorded), body read capped at 256 KB and kept only as title + sha256 + signature hits.
Mobile-Chrome UA + en-SG so the response is what an SG phone user would be served (kits often cloak on UA).
Bare hosts follow Chrome's HTTPS-first behaviour: https, then http if https fails or its certificate is invalid.
"""
import html, http.cookiejar, json, os, re, socket, urllib.parse, warnings
import requests, urllib3
from .normalize import ROOT, sha256

PROXY = os.environ.get("SGINTEL_PROBE_PROXY", "http://127.0.0.1:18080")
UA = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
BODY_CAP, MAX_REDIRECTS, TIMEOUT = 256 * 1024, 5, (10, 20)
SIG_VERSION = "v1.4-2026-11-26"   # signatures below are first-pass; calibrate against the 50-site sample (SCOPE.md §8.5)

SIGS = {   # group -> regexes over lowercased title + text of the final response
  "host_interstitial": [r"suspected phishing", r"phishing site ahead", r"reported for (?:potential )?phishing", r"flagged as (?:a )?phishing"],
  "bot_challenge": [r"<title>just a moment\.\.\.</title>", r"cf-chl-|challenge-platform|cf_chl_opt", r"attention required! \| cloudflare",
                    r"checking (?:if the site connection is secure|your browser)", r"ddos-guard", r"sgcaptcha|/\.well-known/sgcaptcha"],
  "parked_or_for_sale": [r"this domain (?:name )?(?:is|may be) for sale", r"buy this domain", r"domain(?: name)?\b.{0,60}?\b(?:is|may be) for sale",
                         r"premium domain(?: name)? .{0,60}for sale", r"domain (?:is )?parked", r"parked (?:free|domain)",
                         r"sedoparking|parkingcrew|bodis\.com|afternic|hugedomains|dan\.com/|undeveloped\.com", r"this domain has (?:expired|been registered)",
                         r"domain (?:name )?has expired", r"renew (?:this|your) domain", r"is parked free, courtesy of",
                         r"wsimg\.com/parking|parking-lander|parkingpage\.namecheap|sedo\.com/(?:park|search)|afternic\.com/forsale|/lander\b.{0,40}parking"],
  "host_suspended": [r"this account has been suspended", r"(?:this )?(?:website|web site|site|domain) (?:is|has been) (?:suspended|disabled|taken down)",
                     r"suspendedpage\.cgi", r"hosting (?:account )?(?:has )?expired"],
  "seized": [r"seized by the (?:federal bureau|fbi|united states|u\.s\.)", r"this (?:domain|website|site) has been seized", r"domain (?:name )?seized",
             r"seizure warrant", r"seized (?:pursuant|in accordance|as part of)"],
  "default_page": [r"<title>welcome to nginx!?</title>", r"<title>apache2? \w* ?default page", r"<title>test page for the (?:apache|nginx)",
                   r"<title>iis windows server</title>", r"<title>web server's default page</title>", r"<title>it works!</title>",
                   r"<title>google public dns</title>", r"<title>default web site page</title>"],
  "platform_removed": [r"there isn't a github pages site here", r"no such app", r"herokucdn\.com/error-pages", r"deployment_not_found|deployment_disabled|this deployment (?:has been disabled|cannot be found)",
                       r"site not found.{0,200}(?:netlify|firebase)", r"(?:netlify|firebase).{0,200}site not found", r"the train has not arrived",
                       r"there is nothing here yet", r"project not found", r"this site (?:is no longer available|was deleted)", r"blog has been removed"],
  "origin_down": [r"error 10(?:16|01)", r"origin dns error", r"web server is down", r"connection timed out.{0,80}cloudflare", r"origin is unreachable"],
}
SIGS = {g: [re.compile(p, re.S) for p in ps] for g, ps in SIGS.items()}
BENIGN_REDIRECT = {"google.com", "bing.com", "yahoo.com", "baidu.com", "example.com", "microsoft.com", "youtube.com", "facebook.com", "about:blank"}


def proxy_alive():
    u = urllib.parse.urlsplit(PROXY)
    try: socket.create_connection((u.hostname, u.port), timeout=2).close(); return True
    except OSError: return False


def vantage():
    try: return json.loads((ROOT / "logs" / "egress_proxy.state.json").read_text()).get("vantage")
    except (OSError, ValueError): return "unknown"


def _session():
    s = requests.Session(); s.trust_env = False; s.proxies = {"http": PROXY, "https": PROXY}
    s.cookies.set_policy(http.cookiejar.DefaultCookiePolicy(allowed_domains=[]))   # keep no cookies, even across redirects
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                      "Accept-Language": "en-SG,en;q=0.9", "Accept-Encoding": "gzip, deflate"})
    return s


def _egress(tag, detail):
    """Map the egress proxy's "<code> <Tag> <detail>" refusals onto the same codes as direct network errors."""
    tag, detail = (tag or "").lower(), (detail or "").strip()[:80]
    if tag == "blocked": return {"error": "egress_blocked", "detail": detail}
    if tag == "dns": return {"error": "dns_nxdomain" if detail == "nxdomain" else "dns_error", "detail": detail}
    if tag == "connect": return {"error": {"refused": "connection_refused", "timeout": "timeout"}.get(detail, "connect_failed"), "detail": detail}
    return {"error": f"egress_{tag}", "detail": detail}


def _exc(e):
    m = str(e)
    p = re.search(r"Tunnel connection failed: (\d{3}) (\w+) ?([^'\")]*)", m)
    if p: return _egress(p.group(2), p.group(3))
    if isinstance(e, requests.exceptions.SSLError): return {"error": "tls_handshake_failed", "detail": m[:120]}
    if isinstance(e, (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout)): return {"error": "timeout", "detail": type(e).__name__}
    if isinstance(e, requests.exceptions.TooManyRedirects): return {"error": "redirect_loop"}
    if "refused" in m.lower(): return {"error": "connection_refused"}
    if "reset" in m.lower() or "aborted" in m.lower(): return {"error": "connection_reset", "detail": m[:80]}
    return {"error": "network_error", "detail": f"{type(e).__name__}: {m[:100]}"}


def _read(r):
    body = b""
    for chunk in r.iter_content(16384):
        body += chunk
        if len(body) >= BODY_CAP: break
    r.close(); return body[:BODY_CAP]


def _one(s, url, verify):
    """GET one URL following redirects manually. -> dict(hops, final, body, tls_ok)"""
    hops, cur = [], url
    for _ in range(MAX_REDIRECTS + 1):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
                r = s.get(cur, allow_redirects=False, stream=True, timeout=TIMEOUT, verify=verify)
        except requests.RequestException as e:
            hops.append({"url": cur, **_exc(e)}); return {"hops": hops, "final": None, "body": b""}
        egress = r.headers.get("X-SGIntel-Egress")
        hop = {"url": cur, "status": r.status_code, "ctype": r.headers.get("Content-Type", "")[:60], "server": r.headers.get("Server", "")[:40]}
        if egress:
            hop |= _egress(egress, (r.reason or "").split(" ", 1)[-1] if " " in (r.reason or "") else ""); r.close(); hops.append(hop)
            return {"hops": hops, "final": None, "body": b""}
        loc = r.headers.get("Location")
        if r.is_redirect and loc:
            r.close(); nxt = urllib.parse.urljoin(cur, loc); hop["location"] = nxt[:300]; hops.append(hop)
            if urllib.parse.urlsplit(nxt).scheme not in ("http", "https"): return {"hops": hops, "final": None, "body": b"", "stop": "non_http_redirect"}
            cur = nxt; continue
        body = _read(r)
        nxt = _soft_redirect(body, cur) if 200 <= r.status_code < 300 and len(body) < 8192 else None
        if nxt:                                   # meta refresh / one-line location= stub: read from source, JS is never executed
            hop["location"] = nxt[:300]; hop["soft_redirect"] = True; hops.append(hop); cur = nxt; continue
        hops.append(hop)
        return {"hops": hops, "final": hop, "body": body}
    return {"hops": hops, "final": None, "body": b"", "stop": "redirect_loop"}


SOFT_REDIRECT = [re.compile(p, re.I | re.S) for p in (
    r"<meta[^>]+http-equiv=[\"']?refresh[\"']?[^>]+content=[\"']?\s*\d+\s*;\s*url=([^\"'>\s]+)",
    r"(?:window\.|document\.|top\.)?location(?:\.href)?\s*=\s*[\"']([^\"']+)[\"']",
    r"location\.(?:replace|assign)\(\s*[\"']([^\"']+)[\"']\s*\)")]

def _soft_redirect(body, base):
    s = body.decode("utf-8", "replace")
    for rx in SOFT_REDIRECT:
        m = rx.search(s)
        if m:
            u = urllib.parse.urljoin(base, html.unescape(m.group(1).strip()))
            if urllib.parse.urlsplit(u).scheme in ("http", "https") and u != base: return u
    return None


def fingerprint(body):
    s = body.decode("utf-8", "replace")
    title = html.unescape((re.search(r"<title[^>]*>(.*?)</title>", s, re.S | re.I) or [None, ""])[1]).strip()[:200]
    low = s.lower()
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", low, flags=re.S)))
    RAW = {"bot_challenge", "parked_or_for_sale", "platform_removed", "default_page"}      # infrastructure markers live in markup/script URLs
    hits = {g for g, rx in SIGS.items() for p in rx if p.search(low if g in RAW else title.lower() + " " + text)}
    has_form = bool(re.search(r"<form\b|<input\b[^>]*type=[\"']?(?:password|tel|email)", low))
    if "host_interstitial" in hits and "cloudflare" not in low: hits.discard("host_interstitial")
    in_title = {g for g, rx in SIGS.items() for p in rx if p.search(title.lower())}      # a for-sale/parked *title* is decisive
    if has_form: hits -= {"parked_or_for_sale", "host_suspended", "platform_removed", "default_page"} - in_title   # lures say "your account has been suspended"
    return {"title": title, "sha256": sha256(body), "bytes": len(body), "text_chars": len(text.strip()), "has_form": has_form,
            "sig": sorted(hits), "sig_version": SIG_VERSION}


def probe(value, typ):
    """-> {attempts:[{url, verify, hops, ...}], used: index of the deciding attempt or None, tls, fp}.
    attempts[used]["verify"] is False  <=>  the content is only reachable by clicking through Chrome's certificate warning."""
    s = _session(); attempts = []; tls = "n/a"
    plan = [value] if typ == "url" else [f"https://{value}/", f"http://{value}/"]
    def rec(a, url, verify):
        attempts.append({"url": url, "verify": verify, **{k: v for k, v in a.items() if k != "body"}})
        return {"attempts": attempts, "used": len(attempts) - 1, "tls": tls, "fp": fingerprint(a["body"])} if a["final"] else None
    for url in plan:
        a = _one(s, url, True)
        if a["final"] and any(h["url"].startswith("https") for h in a["hops"]): tls = "ok" if tls == "n/a" else tls
        done = rec(a, url, True)
        if done: return done
        if any(h.get("error") == "tls_handshake_failed" for h in a["hops"]):
            tls = "invalid"
            if typ != "url" and url != plan[-1] and len(a["hops"]) == 1: continue   # bare host: Chrome retries over http without a warning
            done = rec(_one(s, url, False), url, False)                                # the click-through view
            if done: return done
            continue
        first = a["hops"][0].get("error") if a["hops"] else None
        if first in ("egress_blocked", "dns_nxdomain", "dns_error"): break                                # policy block / DNS: http would hit the same wall
    if tls == "invalid" and typ != "url" and not any(x["url"] == plan[0] and not x["verify"] for x in attempts):
        done = rec(_one(s, plan[0], False), plan[0], False)
        if done: return done
    return {"attempts": attempts, "used": None, "tls": tls, "fp": None}
