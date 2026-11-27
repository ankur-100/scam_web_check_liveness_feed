"""data/SITES.md - impersonating-site status report (SCOPE.md deliverable view v_site_status)."""
import json
from collections import Counter, defaultdict
from .normalize import ROOT, iso, now
from . import probe, safebrowsing

BUCKETS = ["live", "flagged", "taken_down", "inconclusive", None]
LABEL = {"live": "(c) live", "flagged": "(b) flagged", "taken_down": "(a) taken down", "inconclusive": "inconclusive", None: "not yet checked"}


def report(con, write=True):
    rows = [dict(r) for r in con.execute("SELECT * FROM v_site_status")]
    for r in rows:
        for k in ("publications", "publishers", "listing_roles", "authentic_hosts", "other_brands"): r[k] = json.loads(r[k] or "[]")
        r["role"] = "listing" if "listing" in r["listing_roles"] else "adjacent"
    lst = [r for r in rows if r["role"] == "listing"]; adj = [r for r in rows if r["role"] == "adjacent"]
    cnt = lambda rs: Counter(r["site_bucket"] for r in rs)
    pol = Counter(c[0] for c in con.execute("SELECT probe_policy FROM liveness_check WHERE bucket IS NOT NULL"))
    van = [v for (v,) in con.execute("SELECT DISTINCT vantage FROM liveness_check WHERE bucket IS NOT NULL")]
    L = [f"# Impersonating-site status ({iso(now())})", "",
         f"Sites named in publications of **listing** publishers: **{len(lst)}**; **adjacent** (MAS Investor Alert List): {len(adj)}.",
         f"Checks so far: {sum(pol.values())} ({dict(pol)}); vantage: {', '.join(van) or '-'}; Safe Browsing: {'ON' if safebrowsing.ENABLED else 'OFF (D6) - flag axis from host interstitial + TLS only'}; "
         f"signatures {probe.SIG_VERSION}.", "",
         "Buckets: **(a) taken down** = not reachable (whatever the flag) · **(b) flagged** = serving behind a bypassable warning · "
         "**(c) live** = serving, no warning seen · inconclusive = not decidable from this vantage yet.", ""]
    L += ["## 1. Current state", "", "| | " + " | ".join(LABEL[b] for b in BUCKETS) + " | total |", "|---|" + "---|" * (len(BUCKETS) + 1)]
    for name, rs in (("listing", lst), ("adjacent", adj)):
        c = cnt(rs); L.append(f"| {name} | " + " | ".join(str(c[b]) for b in BUCKETS) + f" | {len(rs)} |")
    pend = sum(1 for r in lst if (r["site_reason"] or "").endswith("_unconfirmed"))
    L += ["", f"Of the listing sites marked inconclusive, **{pend}** are soft takedown signals (NXDOMAIN, dead delegation, no address, "
          "bare 404, origin down) waiting for the confirming second check ≥6 h later; they move to (a) if it agrees."]
    L += ["", "### Reasons (listing sites)", "", "| bucket | reason | n |", "|---|---|---|"]
    L += [f"| {LABEL[b]} | {why} | {n} |" for (b, why), n in sorted(Counter((r["site_bucket"], r["site_reason"]) for r in lst).items(), key=lambda x: (BUCKETS.index(x[0][0]), -x[1]))]
    L += ["", "## 2. By publisher (listing)", "", "| publisher | sites | " + " | ".join(LABEL[b] for b in BUCKETS[:4]) + " |", "|---|---|" + "---|" * 4]
    byp = defaultdict(list)
    for r in lst:
        for p in r["publishers"]: byp[p].append(r)
    for p, rs in sorted(byp.items(), key=lambda x: -len(x[1])):
        c = cnt(rs); L.append(f"| {p} | {len(rs)} | " + " | ".join(str(c[b]) for b in BUCKETS[:4]) + " |")
    L += ["", "## 3. By impersonated target (listing, top 30)", "", "| target | kind | sites | live | flagged | taken down | authentic hosts |", "|---|---|---|---|---|---|---|"]
    byt = defaultdict(list)
    for r in lst: byt[(r["target_entity_id"], r["target_name"])].append(r)
    for (e, n), rs in sorted(byt.items(), key=lambda x: -len(x[1]))[:30]:
        c = cnt(rs); kinds = "/".join(sorted({x["impersonation_kind"] or "?" for x in rs}))
        L.append(f"| {n or '— none —'} (`{e}`) | {kinds} | {len(rs)} | {c['live']} | {c['flagged']} | {c['taken_down']} | {', '.join(rs[0]['authentic_hosts'][:3])} |")
    L += ["", "## 4. Target resolution", "", f"Kinds: {dict(Counter(r['impersonation_kind'] for r in lst))}  ",
          f"Methods: {dict(Counter((r['target_method'] or 'none').split(':')[0] for r in lst))}", ""]
    unres = [r for r in lst if r["impersonation_kind"] == "unresolved"]
    L += [f"### Review queue: unresolved targets ({len(unres)})", "", "| site | candidate brands | publication |", "|---|---|---|"]
    L += [f"| `{r['value_defanged']}` | {', '.join(r['other_brands'][:4]) or '-'} | {(r['publications'] or [''])[0]} |" for r in unres[:60]]
    live = [r for r in lst if r["site_bucket"] in ("live", "flagged")]
    L += ["", f"## 5. Reachable now: live + flagged ({len(live)})", "", "| site (defanged) | bucket | reason | target | first published | listed by |", "|---|---|---|---|---|---|"]
    L += [f"| `{r['value_defanged']}` | {r['site_bucket']} | {r['site_reason']} | {r['target_name'] or r['impersonation_kind']} | {(r['first_published_at'] or '')[:10]} | {', '.join(r['publishers'])} |"
          for r in sorted(live, key=lambda r: r["first_published_at"] or "", reverse=True)]
    ev = con.execute("SELECT event, COUNT(*) FROM feed_event WHERE object_type='site' GROUP BY 1").fetchall()
    L += ["", "## 6. Site events emitted", "", ", ".join(f"{e}: {n}" for e, n in ev) or "-", ""]
    if write: (ROOT / "data" / "SITES.md").write_text("\n".join(L) + "\n")
    return {"listing": len(lst), "adjacent": len(adj), "listing_buckets": dict(cnt(lst)), "unresolved": len(unres)}
