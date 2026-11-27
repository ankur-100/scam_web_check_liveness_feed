"""Extract the ScamShield / I-can-ACT scam-advisory feed from the public /scam-trends page.

The site is Next.js App Router backed by Directus. The listing page server-renders the
*entire* collection into the RSC flight stream (self.__next_f.push) as the prop
`scamAdvisories`; pagination (?page=N, 8/page) is client-side only. One GET = full feed.

usage: python extract.py [saved.html]    -> advisories_raw.json, advisories.jsonl
"""
import json, re, sys, unicodedata, urllib.request

BASE = "https://www.icanactagainstscams.gov.sg"

def fetch():
    req = urllib.request.Request(BASE + "/scam-trends", headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode()

def flight_bytes(html):
    out = b""
    for c in re.findall(r'self\.__next_f\.push\((\[.*?\])\)</script>', html, re.S):
        a = json.loads(c)
        if len(a) > 1 and isinstance(a[1], str):
            out += a[1].encode()
    return out

def rows(b):
    """RSC rows: `<hexid>:<json>\\n`, or `<hexid>:T<hexbytelen>,<text>` (length-prefixed, no newline)."""
    i, R = 0, {}
    while i < len(b):
        j = b.index(b":", i); rid = b[i:j].decode(); i = j + 1
        if b[i:i+1] == b"T":
            k = b.index(b",", i); n = int(b[i+1:k], 16)
            R[rid] = b[k+1:k+1+n].decode(); i = k + 1 + n
        else:
            k = b.find(b"\n", i); k = len(b) if k < 0 else k
            R[rid] = b[i:k].decode(); i = k + 1
    return R

def advisories(html):
    R = rows(flight_bytes(html))
    for v in R.values():
        if '"scamAdvisories"' in v:
            idx = v.index('"scamAdvisories"')
            recs, _ = json.JSONDecoder().raw_decode(v, v.index(":", idx) + 1)
            for r in recs:  # long markdown bodies are hoisted into T rows and referenced as "$<id>"
                c = r.get("content")
                if isinstance(c, str) and re.fullmatch(r"\$[0-9a-f]+", c):
                    r["content"] = R.get(c[1:])
            return recs
    raise ValueError("scamAdvisories prop not found - page structure changed")

# Port of the site's own slug builder (page chunk module 238)
_PFX = re.compile(r"^\s*(?:(?:public|scam|advisory|alert)\s+)*(?:advisory|alert)\s*:\s*", re.I)
_LEAD = re.compile(r"^(?:beware of|advisory on|alert on|watch out for|protect yourself from|be wary of|"
                   r"be alert to|stay alert to|be cautious of|stay vigilant against|guard against)\s+(?=\S+\s+\S)", re.I)
def slug(rec):
    t = _LEAD.sub("", _PFX.sub("", rec.get("title") or "")).strip()
    t = (t[:1].upper() + t[1:]) if t else (rec.get("title") or "")
    t = "".join(ch for ch in unicodedata.normalize("NFKD", t) if not unicodedata.combining(ch)).lower()
    t = re.sub(r"[^a-z0-9]+", "-", re.sub(r"['’]", "", t)).strip("-")
    if len(t) > 60:
        cut = t[:60]
        t = cut if t[60] == "-" else (cut[:cut.rfind("-")] if cut.rfind("-") > 0 else cut)
    id8 = rec["id"][:8].lower()
    return f"/scam-trends/{t}-{id8}" if t else f"/scam-trends/{id8}"

GOV = re.compile(r"\((?:LTA|SPF|IRAS|ICA|CPF|NEA|MOM|MOH|HDB|MAS|SCDF|CSA|MINDEF|MOE|HTX|MHA|SGAC|PTVE)\)"
                 r"|Gov\.sg|Singpass|CDC Vouchers|SimplyGo|SingHealth|Authority|Board\b|Ministry|Agency", re.I)

def normalize(r):
    tags = [t["scamsexposed_tags_id"] for t in r.get("tags") or [] if t.get("scamsexposed_tags_id")]
    urls = r.get("scam_site_urls")
    urls = json.loads(urls) if isinstance(urls, str) and urls else (urls or [])  # stringified JSON array
    brands = [t["value"] for t in tags if t["key"] == "Brand"]
    return {
        "id": r["id"],
        "url": BASE + slug(r),
        "published": r.get("date_created"),
        "modified": r.get("date_updated"),
        "title": r.get("title"),
        "scam_categories": [t["value"] for t in tags if t["key"] == "Scam Category"],
        "impersonated_brands": brands,
        "impersonated_gov_entities": [b for b in brands if GOV.search(b)],
        "scam_domains": urls,
        "images": [BASE + f"/api/assets/{i['directus_files_id']['id']}/{i['directus_files_id']['filename_disk']}"
                   for i in r.get("images") or [] if i.get("directus_files_id")],
        "body_md": r.get("content"),
        # always-null passthroughs kept so schema drift is visible
        "_occurrences": r.get("occurrences"),
        "_sort": r.get("sort"),
        "_tag_ids": {t["value"]: t["id"] for t in tags},
    }

if __name__ == "__main__":
    html = open(sys.argv[1]).read() if len(sys.argv) > 1 else fetch()
    recs = advisories(html)
    json.dump(recs, open("advisories_raw.json", "w"), indent=1, ensure_ascii=False)
    with open("advisories.jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(normalize(r), ensure_ascii=False) + "\n")
    print(len(recs), "advisories;", sum(1 for r in recs if not r.get("content") or r["content"].startswith("$")), "unresolved bodies")
