"""DNS-over-HTTPS resolution (Google Public DNS JSON API) for scam-site liveness and the egress proxy.

Why not the system resolver: on this VM it silently times out on many listed scam domains that resolve publicly
(the upstream resolver filters them), and direct :53 egress is blocked. A verdict must reflect what an ordinary
user's resolver returns, so liveness and the proxy resolve here. Only hostnames are sent (to Google, as with Safe
Browsing). SERVFAIL comes back with a comment / extended DNS error that separates dead delegations (zone removed
at the DNS host - a takedown signal) from transient failures.
"""
import threading, requests

URL = "https://dns.google/resolve"
RESOLVER = "doh:dns.google"
_tl = threading.local()


def _session():
    if not hasattr(_tl, "s"): _tl.s = requests.Session(); _tl.s.trust_env = False
    return _tl.s


def resolve(host):
    """-> {resolver, rcode: NOERROR|NODATA|NXDOMAIN|SERVFAIL|DOH_ERROR|RCODE_n, a, aaaa, cname, comment, ede, dead_delegation}"""
    d = {"resolver": RESOLVER, "rcode": "NOERROR", "a": [], "aaaa": [], "cname": [], "comment": None, "ede": [], "dead_delegation": False}
    for rt, key, typ in (("A", "a", 1), ("AAAA", "aaaa", 28)):
        try:
            j = _session().get(URL, params={"name": host, "type": rt}, timeout=12).json()
        except (requests.RequestException, ValueError) as e:
            d["rcode"] = "DOH_ERROR"; d["comment"] = f"{type(e).__name__}: {str(e)[:80]}"; return d
        st = j.get("Status")
        if st == 3: d["rcode"] = "NXDOMAIN"; return d
        if st == 2:
            d["rcode"] = "SERVFAIL"; d["comment"] = (j.get("Comment") or "")[:300]
            d["ede"] = sorted({e.get("info_code") for e in j.get("extended_dns_errors") or []})
            c = d["comment"].lower()
            d["dead_delegation"] = "lame delegation" in c or "refused" in c or 22 in d["ede"]   # 22 = No Reachable Authority
            return d
        if st != 0: d["rcode"] = f"RCODE_{st}"; return d
        for a in j.get("Answer") or []:
            if a.get("type") == typ: d[key].append(a["data"])
            elif a.get("type") == 5 and a["data"] not in d["cname"]: d["cname"].append(a["data"])
    if not d["a"] and not d["aaaa"]: d["rcode"] = "NODATA"
    return d
