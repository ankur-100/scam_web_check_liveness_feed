#!/usr/bin/env python3
"""Page analyzer: python3 pa.py [-n SNIPS] [-c CTX] [-h HEAD] [-k REGEX] url ...
robots-checked polite fetch; prints status, title, last-updated, dates, keyword snippets from main content,
linked hosts, social links, phone numbers."""
import re, sys, html, time, os, hashlib, json
from urllib.parse import urlparse
from urllib import robotparser
import requests
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept-Language": "en-SG,en;q=0.9"})
RP = {}; HERE = os.path.dirname(os.path.abspath(__file__)); PG = os.path.join(HERE, "pages")
KW = re.compile(r"scam|phish|fraud|impersonat|fake|hoax|spoof|beware|unsolicited|never ask|will never|will not|official (?:website|channel|account|sms|sender)|sender id", re.I)
DATE = re.compile(r"\b(\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|\d{4}-\d{2}-\d{2})\b")
def allowed(u):
    p = urlparse(u); base = f"{p.scheme}://{p.netloc}"
    if base not in RP:
        rp = robotparser.RobotFileParser()
        try:
            r = S.get(base + "/robots.txt", timeout=20)
            txt = r.text if r.status_code == 200 and "<html" not in r.text[:500].lower() else ""
        except Exception: txt = ""
        rp.parse(txt.splitlines()); RP[base] = rp; time.sleep(0.5)
    return RP[base].can_fetch(UA, u)
def text_of(t):
    t = re.sub(r"(?is)<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>|<!--.*?-->|<nav\b.*?</nav>|<header\b.*?</header>|<footer\b.*?</footer>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>|</div>|</td>", " \n", t)
    x = html.unescape(re.sub(r"<[^>]+>", " ", t)).replace("\xa0", " ")
    x = re.sub(r"[ \t\r\f\v]+", " ", x); x = re.sub(r"\n\s*\n+", "\n", x); return x
def fetch(u):
    fn = os.path.join(PG, hashlib.md5(u.encode()).hexdigest()[:12] + ".html")
    if os.path.exists(fn):
        return json.load(open(fn + ".json")), open(fn, encoding="utf-8", errors="replace").read()
    if not allowed(u): return {"status": "DISALLOWED by robots", "final": u}, ""
    try:
        r = S.get(u, timeout=40, allow_redirects=True)
        meta = {"status": r.status_code, "final": r.url, "ctype": r.headers.get("content-type", "")}
        b = r.text if ("html" in meta["ctype"] or "xml" in meta["ctype"] or not meta["ctype"]) else ""
    except Exception as e: meta, b = {"status": "ERR " + type(e).__name__, "final": u}, ""
    time.sleep(float(os.environ.get("PA_DELAY", "1.2")))
    open(fn, "w").write(b); json.dump(meta, open(fn + ".json", "w")); return meta, b
def main():
    a = sys.argv[1:]; nsn, ctx, head, kw = 10, 220, 0, KW
    while a and a[0].startswith("-"):
        if a[0] == "-n": nsn = int(a[1])
        elif a[0] == "-c": ctx = int(a[1])
        elif a[0] == "-h": head = int(a[1])
        elif a[0] == "-k": kw = re.compile(a[1], re.I)
        a = a[2:]
    for u in a:
        meta, t = fetch(u)
        print("=" * 90); print("URL", u, "->", meta.get("status"), meta.get("final"))
        if not t: continue
        ti = re.search(r"(?is)<title[^>]*>(.*?)</title>", t); print("TITLE", re.sub(r"\s+", " ", html.unescape(ti.group(1))).strip()[:150] if ti else None)
        print("METADATES", re.findall(r'(?i)"(?:datePublished|dateModified)"\s*:\s*"([^"]+)"', t)[:4], re.findall(r'(?i)<meta[^>]+(?:published|modified)[^>]+content="([^"]+)"', t)[:4])
        mm = re.search(r"(?is)<main\b[^>]*>(.*)</main>", t)
        x = text_of(mm.group(1) if mm else t); full = text_of(t)
        print("MAIN", bool(mm), "LEN", len(x))
        print("LASTUPD", re.findall(r"(?i)last (?:updated|modified|reviewed)(?: on)?:?\s*([0-9]{1,2} [A-Za-z]+ [0-9]{4})", full)[:3])
        ds = DATE.findall(x); print(f"DATES(n={len(ds)})", ds[:25])
        if head: print("HEAD>>", x[:head].replace("\n", " | "))
        n = 0; last = -999
        for m in kw.finditer(x):
            if m.start() - last < ctx: continue
            last = m.start(); print("  ..", x[max(0, m.start() - ctx):m.end() + ctx].replace("\n", " "))
            n += 1
            if n >= nsn: break
        print("KW_HITS", len(kw.findall(x)))
        links = re.findall(r'href="([^"#]+)"', t)
        print("HOSTS", sorted(set(urlparse(l).netloc for l in links if l.startswith("http"))))
        print("SOCIAL", sorted(set(l for l in links if re.search(r"facebook\.com|instagram\.com|twitter\.com|//x\.com|t\.me/|tiktok\.com|youtube\.com|linkedin\.com|whatsapp\.com|telegram", l))))
        print("KWLINKS", sorted(set(l for l in links if re.search(r"(?i)scam|phish|fraud|impersonat|fake|beware|advisor|alert|rss|feed", l)))[:40])
        print("PHONES", sorted(set(re.findall(r"(?<!\d)(?:\+65[ -]?)?(?:1800|6\d{3}|8\d{3}|9\d{3})[ -]?\d{3,4}(?:[ -]?\d{3,4})?(?!\d)", x)))[:15])
if __name__ == "__main__": main()
