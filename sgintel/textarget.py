"""Impersonation target read from the advisory itself (title, then wording near the URL).

Publishers usually say what a listed site imitates ("Fake Banking Websites Impersonating DBS and UOB", "URLs impersonating
Singapore Pools' websites", "Police Advisory On Phishing Scams Involving Fake AXS Websites"). This works whether or not the
brand is in our registry. Returns brand names (strings); target.py maps them to registry entities or creates a text entity.
"""
import re

GENERIC = {"brands", "brand", "popular", "popular brands", "legitimate", "legitimate companies", "reputable", "reputable brands", "legitimate brands",
           "events", "companies", "hotel", "hotel reservation", "hotel reservation services", "online", "banks", "banking", "government", "officials", "authorities",
           "investment", "online shopping", "e-commerce", "job", "you", "victims", "others", "well-known", "famous", "trusted", "e-wallet",
           "e-wallets", "emerging", "suspicious", "unusual", "high", "financial institutions", "social media", "mobile", "game", "gaming", "crypto",
           "cryptocurrency", "promising high returns", "high returns", "delivery", "parcel", "bank", "telco", "platform", "platforms", "the", "a", "an", "fake", "phishing", "scam", "scams"}
STOP = {"websites", "website", "sites", "site", "and", "or", "mobile", "apps", "app", "applications", "application", "investment", "investments",
        "scams", "scam", "schemes", "scheme", "accounts", "account", "cryptocurrency", "phishing", "job", "jobs", "with", "via", "on", "for",
        "to", "in", "other", "deals", "promising", "offering", "targeting", "pages", "page", "platforms", "brands", "services", "messages", "calls", "links", "urls"}
PREFIX = re.compile(r"^(?:SPF\s*\|\s*)?(?:Police Advisory|Scam Advisory|Public Advisory|Advisory|Job Scam Alert|Scam Alert)\s*(?:On\b|on\b|[:–\-|])?\s*", re.I)
NAME = r"[\"“'‘`*]*([A-Z0-9][\w’'&\.\-]*(?:\s+(?:of\s+)?[A-Z0-9][\w’'&\.\-]*){0,5})[\"”'’`*]*"   # case-sensitive: proper names
I = lambda w: "(?i:" + w + ")"
TITLE_RX = [
    re.compile(I(r"impersonat(?:ing|ion of|es|e)") + r"\s+(?:the\s+)?" + NAME + r"(?:\s+and\s+" + NAME + ")?"),
    re.compile(r"\b" + I("fake") + r"\s+" + NAME + r"(?:\s+and\s+" + NAME + ")?"),
    re.compile(NAME + r"\s+" + I("impersonation")),
]
NEAR_RX = [
    re.compile(I(r"impersonating") + r"\s+" + NAME + r"['’]s?\s+" + I("websites?")),
    re.compile(I(r"resembl\w*\s+(?:the\s+)?(?:genuine\s+|official\s+)?(?:website\s+of\s+)?") + NAME),
    re.compile(I(r"similar to the official") + r"\s+" + NAME + r"(?:\s+or\s+" + NAME + ")?"),
    re.compile(I(r"impersonating\s+(?:legitimate brands such as\s+)?(?:the\s+)?") + NAME),
    re.compile(I(r"(?:posing|masquerading|purporting to be|claiming to be)(?:\s+as)?\s+(?:the\s+)?") + NAME),
]


def _clean(n):
    toks = (n or "").strip(" .,:;\"“”'‘’`*-").split()
    out = []
    for t in toks:
        if t.lower().strip(".,") in STOP: break
        out.append(t)
    n = re.sub(r"['’]s?$", "", " ".join(out).strip(" .,:;-")).strip()
    if not n or n.lower() in GENERIC or len(n) < 2: return None
    return n


def names_from(title, near="", body=""):
    """-> (names, where) ; names in order of appearance, 'title' preferred over 'text'."""
    t = PREFIX.sub("", title or "").strip()
    for rx in TITLE_RX:
        m = rx.search(t)
        if m:
            out = [x for x in (_clean(g) for g in m.groups()) if x]
            if out: return out, "title"
    for rx in NEAR_RX:
        m = rx.search(near or "")
        if not m and body: m = rx.search(body)
        if m:
            out = [x for x in (_clean(g) for g in m.groups()) if x]
            if out: return out, "text"
    return [], None
