"""Source roles under SCOPE.md §3. Recomputed after every crawl, so a watched page that starts naming scam sites is promoted.

listing   - publishes items that name specific impersonating sites (feeds v_site)
adjacent  - lists sites, but they are not impersonation as such (MAS Investor Alert List: unlicensed entities)
watch     - same publishers' narrative pages; swept monthly in case they start listing sites
reference - official-channel pages (authentic hosts / allowlist)
parked    - generic global feeds with no publication behind an entry; polling disabled
"""
import json
from collections import Counter

FIXED = {"spf-icanact": "listing", "mas-ial-opensanctions": "adjacent"}
PARK_REASON = "parked: out of scope (SCOPE.md §3)"
ORDER = ["hot", "daily", "weekly", "monthly", "manual"]


def refresh(con):
    listing = {s for (s,) in con.execute("""SELECT DISTINCT s.source_id FROM sighting s JOIN indicator i USING(indicator_id)
        WHERE s.role='ioc' AND s.report_id IS NOT NULL AND i.type IN ('domain','hostname','url') AND i.status <> 'allowlisted'""")}
    changes = Counter()
    for sid, scope, cur in con.execute("SELECT source_id, sg_scope, listing_role FROM source").fetchall():
        role = FIXED.get(sid) or ("parked" if scope == "filtered" else "reference" if scope == "allowlist"
                                  else "listing" if sid in listing else "watch")
        if role != cur:
            con.execute("UPDATE source SET listing_role=? WHERE source_id=?", (role, sid))
            changes[f"{cur}->{role}"] += 1
    # endpoint consequences (discovery endpoints - rss/sitemap/feeds - keep their tier: that is how new publications are found)
    for ep in con.execute("SELECT * FROM endpoint").fetchall():
        p = json.loads(ep["params"] or "{}")
        roles = {r for (r,) in con.execute("SELECT listing_role FROM source WHERE endpoint_id=? OR source_id=?", (ep["endpoint_id"], p.get("source_id") or ""))}
        if roles == {"parked"}:
            if ep["enabled"]:
                con.execute("UPDATE endpoint SET enabled=0, disabled_reason=? WHERE endpoint_id=?", (PARK_REASON, ep["endpoint_id"])); changes["endpoint parked"] += 1
        elif ep["fetch_kind"] in ("html", "pdf") and roles and roles <= {"watch"} and ORDER.index(ep["tier"]) < ORDER.index("monthly"):
            p["tier_before_watch"] = ep["tier"]
            con.execute("UPDATE endpoint SET tier='monthly', interval_s=30*86400, min_interval_s=14*86400, max_interval_s=60*86400, params=? WHERE endpoint_id=?",
                        (json.dumps(p), ep["endpoint_id"])); changes["page -> monthly watch"] += 1
        elif "listing" in roles and p.get("tier_before_watch"):
            from .catalog import TIER
            t = p.pop("tier_before_watch"); iv, lo, hi = TIER[t]
            con.execute("UPDATE endpoint SET tier=?, interval_s=?, min_interval_s=?, max_interval_s=?, params=? WHERE endpoint_id=?",
                        (t, iv, lo, hi, json.dumps(p), ep["endpoint_id"])); changes["page promoted back"] += 1
    con.commit()
    return dict(changes)
