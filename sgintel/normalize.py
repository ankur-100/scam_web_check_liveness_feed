"""Normalisation + identity (SCHEMA.md §3). Single source of truth for IDs, hosts, SG signals, fingerprints."""
import hashlib, re, sys, unicodedata, datetime as dt, urllib.parse
from pathlib import Path
import tldextract, phonenumbers

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))
import sgfilter  # noqa: E402  (token tiers shared with the global-feed filter)

EXT = tldextract.TLDExtract(include_psl_private_domains=True)
KNOWN_PLATFORMS = {"blogspot.com", "blogspot.sg", "pages.dev", "edgeone.dev", "wpenginepowered.com", "github.io",
                   "netlify.app", "vercel.app", "web.app", "firebaseapp.com", "weebly.com", "wixsite.com", "workers.dev",
                   "glitch.me", "000webhostapp.com", "r2.dev", "framer.website", "webflow.io"}
SERVICE = {"onemotoring/lta", "ezlink", "paynow", "cdc-voucher", "simplygo"}
PATH_KIT = re.compile(r"/(?:bank|banks|b)/(dbs|posb|ocbc|uob|citi|hsbc|maybank|scb?)(?=/|$)")
RX = {t: {k: re.compile(v) for k, v in d.items()} for t, d in (("A", sgfilter.TIER_A), ("B", sgfilter.TIER_B))}

now = lambda: dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
def iso(d): return d.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z") if d else None
def parse_ts(s):
    if not s: return None
    try: return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError: return None
h16 = lambda s: hashlib.sha1(s.encode()).hexdigest()[:16]
sha256 = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()
def ind_id(t, v): return f"ind_{h16(t + ':' + v)}"
def sig_id(src, rep, ind): return f"sig_{h16(f'{src}|{rep or ''}|{ind}')}"
def defang(v): return v.replace("http", "hxxp").replace(".", "[.]")
def refang(s): return re.sub(r"\[\.\]|\(\.\)|\{\.\}|\[dot\]", ".", s.replace("hxxp", "http").replace("[:]", ":"), flags=re.I)

def host_info(hostname):
    r = EXT(hostname); reg = r.top_domain_under_public_suffix or hostname
    shared = bool(r.is_private) or reg in KNOWN_PLATFORMS or any(hostname.endswith("." + p) for p in KNOWN_PLATFORMS)
    return {"hostname": hostname, "registrable_domain": reg, "tld": (r.suffix or "").split(".")[-1], "is_shared_platform": shared,
            "block_scope": "registrable_domain" if (hostname == reg and not shared) else "hostname"}

def parse_host_or_url(raw):
    """-> (type, normalised value, hostname) or None"""
    s = refang(raw.strip()).strip("<>\"'()[],;").rstrip("/.")
    if not s or " " in s: return None
    try: u = urllib.parse.urlsplit(s if "://" in s else "http://" + s)
    except ValueError: return None
    try: host = (u.hostname or "").lower().removeprefix("www.")
    except ValueError: return None
    if not host or "." not in host or not re.fullmatch(r"[a-z0-9.\-¡-￿]+", host): return None
    try: host = host.encode("idna").decode() if not host.isascii() else host
    except UnicodeError: return None
    r = EXT(host)
    if not r.suffix: return None
    scheme = u.scheme if u.scheme in ("http", "https") else "http"
    if u.path not in ("", "/") or u.query:
        return "url", f"{scheme}://{host}{u.path}{'?' + u.query if u.query else ''}", host
    return ("domain" if r.top_domain_under_public_suffix == host else "hostname"), host, host

def norm_phone(raw, region="SG"):
    try:
        n = phonenumbers.parse(raw.strip(), region)
        return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164) if phonenumbers.is_possible_number(n) else None
    except phonenumbers.NumberParseException: return None

def sg_signals(value, hostname, native):
    full = value.split("://")[-1]; path = full[len(hostname):] if full.startswith(hostname) else ""
    brand, service, pathk = [], [], []
    for k, rx in RX["A"].items():
        if k == "ccTLD .sg": continue
        if rx.search(hostname): (service if k in SERVICE else brand).append(k)
        elif path and rx.search(path): pathk.append(k)
    pathk += [f"kit:/bank/{m}" for m in PATH_KIT.findall(path)]
    if sgfilter.SG_CTX.search(full):
        brand += [k + "+sgctx" for k, rx in RX["B"].items() if rx.search(full)]
    sg_tld = hostname.endswith(".sg")
    score = min(1.0, 0.6 * bool(native) + 0.3 * bool(brand or service) + 0.2 * bool(pathk) + 0.1 * sg_tld)
    return {"sg_tld": sg_tld, "brand_tokens": brand, "service_tokens": service, "path_tokens": pathk,
            "sg_native_source": bool(native), "score": round(score, 2)}

def sg_filter_pass(value):
    """Gate for sg_scope=filtered sources: tier-A SG token in host/path, or kit path. ccTLD alone is NOT enough
    (.sg hosts are mostly compromised SMEs phishing non-SG brands — sources/02_generic_feeds.md)."""
    p = parse_host_or_url(value)
    if not p: return False
    s = sg_signals(p[1], p[2], False)
    return bool(s["brand_tokens"] or s["service_tokens"] or s["path_tokens"])

def fingerprint(title, published=None):
    """Cross-source report dedup key: normalised title (+ day). Strips 'Advisory:', 'Beware of' etc."""
    t = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"^\s*(?:(?:public|scam|police)\s+)*(?:advisory|alert|news release)\s*[:\-–]\s*", "", t)
    t = re.sub(r"^(?:beware of|watch out for|be wary of|protect yourself from)\s+", "", t)
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return h16(t + "|" + (published or "")[:7])     # month granularity: same story, same month

# ---- indicator extraction from free text (narrative pages / RSS bodies) ----
DOM_RX = re.compile(r"(?<![@\w.-])((?:hxxps?|https?)(?:\[:\]|:)//(?:\[\.\]|[^\s<>\"')\]\[])+|(?:[a-z0-9-]+(?:\[\.\]|\(\.\)|\.))+(?:[a-z]{2,24})(?:/[^\s<>\"')\]]*)?)", re.I)
EMAIL_RX = re.compile(r"[\w.+-]+(?:@|\[at\]|\(at\))[\w-]+(?:(?:\.|\[\.\])[\w-]+)+", re.I)
SG_PHONE_RX = re.compile(r"(?<!\d)(?:\+65[\s-]?)?[3689]\d{3}[\s-]?\d{4}(?!\d)")
def extract_indicators(text):
    out = []
    for mo in DOM_RX.finditer(text or ""):
        m = mo.group(0)
        if (text[mo.end():mo.end() + 4]).lstrip().startswith(("@", "[at]", "(at)")): continue    # local part of an e-mail address
        p = parse_host_or_url(m)
        if p and EXT(p[2]).suffix and not re.fullmatch(r"\d+(\.\d+)+", p[2]): out.append(p + (m,))
    for m in EMAIL_RX.findall(text or ""):
        v = refang(m).lower().replace("[at]", "@").replace("(at)", "@"); out.append(("email", v, None, m))
    for m in SG_PHONE_RX.findall(text or ""):
        v = norm_phone(m); 
        if v: out.append(("phone", v, None, m))
    seen, uniq = set(), []
    for t in out:
        if (t[0], t[1]) not in seen: seen.add((t[0], t[1])); uniq.append(t)
    return uniq

LEGAL_SUFFIX = {"ltd", "pte", "pte ltd", "limited", "inc", "llc", "co", "corp", "corporation", "plc", "sdn bhd", "bhd", "gmbh", "sa", "ag", "lp", "llp", "pty"}
def canonical(t, v):
    """Identity value used for dedup. URLs: case-folded (feeds disagree on path case; raw kept in sighting.raw).
    entity_name: trimmed, trailing punctuation removed, bare legal suffixes rejected. Returns None to drop."""
    if v is None: return None
    v = v.strip()
    if t == "url": return v.lower().rstrip("/")
    if t in ("domain", "hostname"): return v.lower().strip(".").removeprefix("www.")
    if t == "email": return v.lower()
    if t == "entity_name":
        v = re.sub(r"[\s.,;:]+$", "", re.sub(r"\s+", " ", v.lower()))
        if not v or v in LEGAL_SUFFIX or len(v) < 3 or "://" in v or re.fullmatch(r"(?:https?:?|www\.?|n/?a|nil|none|-+)", v): return None
        return v
    return v

def split_names(s):
    """'ABC Pte, Ltd, XYZ Ltd' -> ['ABC Pte, Ltd', 'XYZ Ltd'] (re-attach legal-suffix fragments)."""
    out = []
    for part in [p.strip() for p in re.split(r"\s*[,;]\s*|\n", s or "") if p.strip()]:
        if out and re.sub(r"[.\s]+$", "", part.lower()) in LEGAL_SUFFIX: out[-1] = f"{out[-1]}, {part}"
        else: out.append(part)
    return out
