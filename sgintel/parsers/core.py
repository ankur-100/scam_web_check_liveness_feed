"""Source adapters. Each returns {"reports":[...], "indicators":[...], "complete":bool, "state":{...}}.
indicator dict: type,value,host,raw, report_native_id, role ('ioc'|'official'|None=decide by context), ctx (text window),
source_first_seen, source_last_seen, source_status, categories[], brands_raw[]"""
import html, json, re, sys, xml.etree.ElementTree as ET
from ..normalize import ROOT, parse_host_or_url, norm_phone, extract_indicators, sg_filter_pass, refang, split_names

sys.path.insert(0, str(ROOT)); import extract as spf_extract   # noqa: E402
SPF_CAT = {"Investment": "investment", "Job": "job", "Banking Related Phishing": "phishing.banking", "Non-Banking Related Phishing": "phishing.non_banking",
           "Phishing": "phishing.unspecified", "E-Commerce": "ecommerce", "Malware": "malware", "Loan": "loan", "Visa": "visa", "Impersonation": "impersonation"}
R = lambda: {"reports": [], "indicators": [], "complete": False, "state": {}}
def ind(t, v, host, raw, **kw): return {"type": t, "value": v, "host": host, "raw": raw, "role": None, "ctx": None, "report_native_id": None,
                                        "source_first_seen": None, "source_last_seen": None, "source_status": None, "categories": [], "brands_raw": [], **kw}

def text_from_html(b):
    s = b.decode("utf-8", "replace")
    title = html.unescape((re.search(r"<title[^>]*>(.*?)</title>", s, re.S | re.I) or [None, ""])[1]).strip()
    m = re.search(r"<main\b.*?</main>", s, re.S | re.I) or re.search(r"<article\b.*?</article>", s, re.S | re.I)
    s = m.group(0) if m else s
    s = re.sub(r"<(script|style|noscript|svg|nav|header|footer)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>|</tr>", "\n", s, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return title, re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", t)).strip()

def with_ctx(text, extracted, report_native_id):
    out = []
    for (t, v, host, raw) in extracted:
        i = text.find(raw); ctx = text[max(0, i - 160): i + len(raw) + 160] if i >= 0 else ""
        out.append(ind(t, v, host, raw, ctx=ctx, report_native_id=report_native_id))
    return out

# ---------------------------------------------------------------- SG-native structured sources
def spf_icanact(body, src, ep):
    r = R(); r["complete"] = True
    for a in spf_extract.advisories(body.decode("utf-8", "replace")):
        tags = [t["scamsexposed_tags_id"] for t in a.get("tags") or [] if t.get("scamsexposed_tags_id")]
        cats = [t["value"] for t in tags if t["key"] == "Scam Category"]; brands = [t["value"] for t in tags if t["key"] == "Brand"]
        r["reports"].append({"native_id": a["id"], "url": "https://www.icanactagainstscams.gov.sg" + spf_extract.slug(a), "title": a.get("title") or a["id"],
                             "body": a.get("content"), "published_at": a.get("date_created"), "modified_at": a.get("date_updated"),
                             "categories_raw": cats, "brands_raw": brands, "raw": {k: a[k] for k in a if k != "content"}})
        urls = a.get("scam_site_urls"); urls = json.loads(urls) if isinstance(urls, str) and urls else (urls or [])
        for u in urls:
            p = parse_host_or_url(u)
            if p: r["indicators"].append(ind(*p, u, role="ioc", report_native_id=a["id"], source_first_seen=a.get("date_created"),
                                             source_last_seen=a.get("date_updated"), source_status="listed", categories=cats, brands_raw=brands))
    return r

def mas_opensanctions(body, src, ep):
    r = R(); r["complete"] = True
    for d in json.loads(body)["response"]["docs"]:
        nid, first, mod = d["id"], d.get("date_dt") or d.get("modifieddate_dt"), d.get("modifieddate_dt")
        names = split_names(d.get("unregulatedpersons_s"))
        r["reports"].append({"native_id": nid, "url": d.get("url", "").replace(" ", "%20"), "title": f"Investor Alert List: {d.get('unregulatedpersons_s','').strip()}",
                             "body": None, "published_at": first, "modified_at": mod, "categories_raw": ["Investor Alert List"], "brands_raw": [],
                             "raw": {k: d.get(k) for k in ("address_s", "alternativename_s", "formername_s", "notes_s", "relatedunregulatedpersons_s")}})
        kw = dict(role="ioc", report_native_id=nid, source_first_seen=first, source_last_seen=mod, source_status="listed", categories=["Investor Alert List"])
        for n in names + [x.strip() for x in re.split(r"[;,\n]", d.get("alternativename_s") or "") if x.strip()]:
            if parse_host_or_url(n) and "." in n and " " not in n: continue
            r["indicators"].append(ind("entity_name", n.lower(), None, n, **kw))
        for w in re.findall(r"(?:https?://)?(?:[\w-]+\.)+[a-z]{2,}(?:/[^\s,]*)?", d.get("website_s") or "", re.I):
            p = parse_host_or_url(w)
            if p and "facebook.com" not in p[2]: r["indicators"].append(ind(*p, w, **kw))
        for ph in re.split(r"[;,/\n]+", d.get("phonenumber_s") or ""):
            v = norm_phone(ph) if ph.strip() else None
            if v: r["indicators"].append(ind("phone", v, None, ph.strip(), **kw))
        for em in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", d.get("email_s") or ""):
            r["indicators"].append(ind("email", em.lower(), None, em, **kw))
    return r

# ---------------------------------------------------------------- SG-native discovery / narrative
def rss(body, src, ep):
    r = R()
    try: root = ET.fromstring(body)
    except ET.ParseError: return r
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item") or root.findall(".//a:entry", ns)
    for it in items:
        g = lambda tag: (it.findtext(tag) or it.findtext(f"a:{tag}", namespaces=ns) or "").strip()
        link = g("link") or ((it.find("a:link", ns).get("href") if it.find("a:link", ns) is not None else "") or "")
        title = html.unescape(g("title")); desc = html.unescape(re.sub(r"<[^>]+>", " ", g("description") or g("summary") or g("content")))
        nid = g("guid") or g("id") or link or title
        r["reports"].append({"native_id": nid, "url": link, "title": title or nid, "body": desc, "published_at": g("pubDate") or g("published") or g("updated"),
                             "modified_at": None, "categories_raw": [c.text for c in it.findall("category") if c.text], "brands_raw": [], "raw": None})
        r["indicators"] += with_ctx(f"{title}\n{desc}", extract_indicators(f"{title}\n{desc}"), nid)
    return r

def sitemap(body, src, ep):
    r = R(); kw = re.compile((ep.get("params") or {}).get("keywords") or "scam|fraud|phish", re.I)
    try: root = ET.fromstring(body)
    except ET.ParseError:   # HTML "sitemap" page (e.g. IRAS): fall back to keyword-matching links
        base = re.match(r"https?://[^/]+", ep["url"]).group(0)
        for href, label in re.findall(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', body.decode("utf-8", "replace"), re.S | re.I):
            u = href if href.startswith("http") else base + ("" if href.startswith("/") else "/") + href
            if kw.search(u) and u.startswith(base):
                t = html.unescape(re.sub(r"<[^>]+>", "", label)).strip() or u
                r["reports"].append({"native_id": u, "url": u, "title": t[:300], "body": None, "published_at": None, "modified_at": None,
                                     "categories_raw": [], "brands_raw": [], "raw": {"from_html_sitemap": ep["url"]}})
        return r
    tag = lambda e: e.tag.split("}")[-1]
    if tag(root) == "sitemapindex":   # follow only scam-keyword children, else first 5 (budget)
        locs = [l.text.strip() for l in root.iter() if tag(l) == "loc" and l.text]
        r["state"]["children"] = [u for u in locs if kw.search(u)][:10] or locs[:5]
        return r
    for u in root:
        if tag(u) != "url": continue
        loc = next((c.text.strip() for c in u if tag(c) == "loc" and c.text), None)
        if not loc or not kw.search(loc): continue
        lastmod = next((c.text.strip() for c in u if tag(c) == "lastmod" and c.text), None)
        title = re.sub(r"[-_]+", " ", loc.rstrip("/").rsplit("/", 1)[-1].split(".")[0]).strip().capitalize() or loc
        r["reports"].append({"native_id": loc, "url": loc, "title": title, "body": None, "published_at": lastmod, "modified_at": lastmod,
                             "categories_raw": [], "brands_raw": [], "raw": {"from_sitemap": ep["url"]}})
    return r

def html_page(body, src, ep):
    r = R(); title, text = text_from_html(body)
    r["reports"].append({"native_id": src["url"], "url": src["url"], "title": title or src["name"] or src["url"], "body": text[:40000],
                         "published_at": None, "modified_at": None, "categories_raw": [], "brands_raw": [], "raw": None})
    r["indicators"] = with_ctx(text, extract_indicators(text), src["url"])
    return r

def pdf_hash(body, src, ep):
    r = R(); r["reports"].append({"native_id": src["url"], "url": src["url"], "title": src["url"].rsplit("/", 1)[-1], "body": None,
                                  "published_at": None, "modified_at": None, "categories_raw": [], "brands_raw": [], "raw": {"bytes": len(body)}})
    return r

# ---------------------------------------------------------------- global feeds (filtered)
def url_list(body, src, ep):
    r = R(); r["complete"] = src["lifecycle_semantics"] == "active_list"; status = (ep.get("params") or {}).get("status")
    s = body.decode("utf-8", "replace").lstrip()
    lines = [str(x) for x in json.loads(s)] if s.startswith("[") else [l.strip() for l in s.splitlines() if l.strip() and not l.startswith(("#", "!"))]
    r["state"]["n_total"] = len(lines)
    for l in lines:
        if not sg_filter_pass(l): continue
        p = parse_host_or_url(l)
        if p: r["indicators"].append(ind(*p, l, role="ioc", source_status=status, categories=["phishing.unspecified"]))
    return r

def phishstats(body, src, ep):
    r = R()
    try: rows = json.loads(body)
    except json.JSONDecodeError: return r
    for x in rows if isinstance(rows, list) else []:
        u = x.get("url") or ""
        if not sg_filter_pass(u): continue
        p = parse_host_or_url(u)
        if p: r["indicators"].append(ind(*p, u, role="ioc", source_first_seen=(x.get("date") or "").replace(".000Z", "Z") or None,
                                         source_last_seen=(x.get("date_update") or "").replace(".000Z", "Z") or None,
                                         source_status=f"http_code={x.get('http_code')}", categories=["phishing.unspecified"]))
    return r

PARSERS = {"spf_icanact": spf_icanact, "mas_opensanctions": mas_opensanctions, "rss": rss, "sitemap": sitemap,
           "html_page": html_page, "pdf_hash": pdf_hash, "url_list": url_list, "phishstats": phishstats}
