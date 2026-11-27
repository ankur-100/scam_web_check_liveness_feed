# Scope redraw and mandate: impersonating-site liveness (v1, 2026-11-26)

Status: **approved 2026-11-26; implemented (see §11).** Decisions: D1 = P1 contained probe; D2 = local egress proxy on this host
(upstream hook for a separate exit IP); D6 = Safe Browsing client built but switched off; D3/D4/D5/D7 = recommended defaults.
Supersedes the "collect every scam indicator" scope in SOURCES.md and PIPELINE.md. Those stay as the inventory record.

## 1. Mandate

> Track every **impersonating website** that a Singapore advisory publisher names in a publication.
> For each site, record the **publication link(s)**, the **publisher**, and the **one authentic site it imitates**.
> Keep a current, evidence-backed **liveness verdict** in the three states a Chrome user would meet:
> **(a) taken down**, **(b) flagged by the browser but bypassable**, **(c) fully live**.
> Keep sweeping all qualifying publishers on their update cycles so that new listings are picked up and checked promptly.

Everything else we have collected becomes reference data (for authentic sites) or is parked.

## 2. What changes from the current build

| Component | Decision | Why |
|---|---|---|
| Poller (catalog tiers, adaptive interval, robots, conditional GET) | **Keep unchanged** | Still needed to discover new publications |
| Entity registry (266 entities, per-brand `entity_id` = primary official domain) | **Keep**. It becomes the "authentic site" table | Target mapping joins straight to `entity_official` |
| Allowlist (756 official hosts) | **Keep** | Stops authentic sites being treated as impersonators, and defines the target's real site |
| report / sighting / provenance view / dedup / `check` | **Keep** | A publication is a report. Publication ↔ site is a sighting |
| Indicator types | **Narrow** to `domain`, `hostname`, `url` | Phones, emails, sender IDs, bank accounts and handles are out of scope (stored, not processed) |
| Sources | **Re-role** into listing / watch / reference / parked (§3) | Only listing publishers feed the site set |
| Liveness (DNS + RDAP → dead/live/inconclusive) | **Replace** with a 2-axis model projected to a/b/c (§5) | The current model can't express "flagged" or "resolves but suspended" |
| Generic global feeds (Phishing.Database, PhishStats, PhishDestroy, Phishing Army, OpenPhish) | **Park** (D5) | Their entries have no publication behind them |
| MAS Investor Alert List | **Adjacent**, pending decision (D4) | Lists unlicensed-entity sites, not impersonation as such |

## 3. Which publishers are in scope

**Qualification rule.** A source is a *listing publisher* if:
1. it publishes discrete items (advisory, alert or notice), each with its own stable URL (the "link per publication");
2. at least one item names a specific impersonating site (domain or URL);
3. the publisher is authoritative: an SG agency, the impersonated brand itself, or a regulator or established media outlet;
4. it is SG-relevant.

Narrative pages from the same publishers stay on a monthly **watch** sweep. If one starts listing sites, the source is promoted automatically. This keeps the polling function the same.

What the current DB shows (counts are before reclassification, so the 1–5-site rows still need checking):

| Role | Publisher / source | Publications | Sites |
|---|---|---|---|
| **Primary** | SPF icanactagainstscams.gov.sg/scam-trends | 211 | 319 |
| Listing | ICA SG Arrival Card advisory (fake SGAC sites) | 1 | 62. **Defect:** currently stored as `role=unknown`, must be `ioc` |
| Listing (small) | MOM 5 · Grab 3 · SGH 2 · Ninja Van 2 · M1 2 · Prudential 2 · UOB · Singtel · J&T · CPF · CAAS · PSD · EnterpriseSG · ICA media releases · Straits Times | 1 each | 1–5 each |
| Adjacent (D4) | MAS Investor Alert List (OpenSanctions mirror; refresh blocked by robots.txt) | 770 | 898 |
| Watch | police.gov.sg media releases (only benign mentions so far), ScamShield alerts (no URLs), other narrative pages | – | 0 |
| Reference | gov.sg Trusted Sites, brands' official-domain pages | – | authentic hosts only |
| Parked | Phishing.Database 672+61, PhishStats 19, PhishDestroy 15, Phishing Army 4 | none | – |

Other publishers that "do the same task" are found by the existing sweep plus the qualification rule. No new survey is needed: the inventory is treated as exhaustive, as you asked.

## 4. Unit of record: one site, its publications, one authentic target

**Your assumption, checked against the 317 distinct SPF site values:**

| Scam category of the listing | Sites | Exactly 1 real target | >1 real brand | No real target |
|---|---|---|---|---|
| Phishing / impersonation / e-commerce / visa / malware | 167 | **148 (89%)** | 11 | 8 |
| Investment / job / loan | 157 | 99 | 22 | 36 (fictitious platforms) |

(A few sites appear under both groups.)

So "one authentic website" holds for phishing and impersonation sites. For investment and job sites, the named brand is mostly a non-SG tech platform, crypto exchange or brokerage, or an SG news outlet in fake-article lures. These sites abuse the brand rather than clone its website.

**Rule:**
- Each site has **exactly one `primary_target`**, or an explicit no-target kind. Any further brands are kept as `secondary_targets`.
- `impersonation_kind` takes one of four values:
  - `clone`: imitates a real entity that has an official site in `entity_official`;
  - `brand_abuse`: a fake platform or job using a real brand's name or logo;
  - `fictitious`: no authentic counterpart exists (40 of SPF's brand tags are fictitious);
  - `unresolved`.
- **The primary target is chosen in this order:**
  1. Look-alike token match against the brand's official hosts, e.g. `onemotoring-lta-gov.cc` → `lta.gov.sg`.
  2. A single brand tag on the publication.
  3. The publisher itself, when the publisher is the impersonated brand (ICA → fake SGAC sites; Grab → fake Grab sites).
  4. Otherwise, mark the site ambiguous and send it to the review queue.
- **Liveness unit:** the full hostname. On shared platforms (15 SPF sites on workers.dev, pages.dev, netlify.app, herokuapp.com, railway.app) this is the subdomain, never the platform domain. Where the publisher lists a path (14 ICA URLs), the listed URL is checked as well.

## 5. Liveness: three Chrome-facing states

Each check measures **two independent axes**, and both are stored:

- **Reachability**: `gone` / `serving` / `unknown`
- **Browser flag**: `flagged` / `clear` / `unknown`

Chrome's red interstitial comes from Google Safe Browsing. Since March 2024, Chrome's Standard protection checks a list held on Google's servers in real time. The Safe Browsing v5 API (`urls:search`) lets us query that status **without contacting the scam site**.

**Projection to your three buckets:**

| Bucket | Rule | What a Chrome user sees |
|---|---|---|
| **(a) TAKEN_DOWN** | reach = gone (whatever the flag) | "This site can't be reached", a suspended or parked page, or a platform 404 |
| **(b) FLAGGED_BYPASSABLE** | reach = serving AND flag = flagged | Red warning with a "visit this unsafe site" link. The scam is behind it |
| **(c) LIVE** | reach = serving AND flag = clear (or `not_checked` while Safe Browsing is off, D6) | The scam page loads normally |
| INCONCLUSIVE | any axis unknown, or signs of cloaking | Not decidable from our vantage point |

**Precedence (D3):** Safe Browsing listings outlast takedowns, so Chrome still shows the warning for a dead flagged site. We rank taken-down first because the question is "does a person who clicks through still reach the scam?". Both axes are stored, so a literal Chrome view is one query away.

**Reason codes (every verdict carries one):**

- **gone:**
  - `dns_nxdomain`: needs 2 checks at least 6 h apart; one is never enough;
  - `registry_hold`: RDAP clientHold or serverHold;
  - `no_address`, `sinkhole_ip`;
  - `platform_removed`: a pages.dev, workers.dev, netlify, heroku or vercel "not found" signature;
  - `host_suspended`, `http_gone` (404/410/451), `parked_or_for_sale`;
  - `repurposed`: the content no longer matches the target brand.
- **flagged:**
  - `sb_social_engineering`, `sb_malware`, `sb_unwanted_software`;
  - `host_interstitial`: Cloudflare "suspected phishing" page, which is also bypassable;
  - `tls_invalid`: Chrome's bypassable certificate warning (D7).
- **unknown:** `timeout`, `bot_challenge` (never solved or bypassed), `geo_or_ip_block`, `dns_timeout`.

**Cadence for re-checking sites.** This is separate from the publisher poller, which stays as it is.

| State | Re-check schedule |
|---|---|
| New listing | First check within one hot-tier cycle of ingestion |
| live / flagged | Every 6 h for 7 days, then daily |
| taken_down | At 1 d, 3 d and 7 d, then weekly until 90 days since the site was last serving (catches resurrection) |
| inconclusive | At 1 h, 6 h and 24 h, then daily |

Sites are archived after 90 days taken down, in line with the existing 90-day domain TTL.

**Events and metrics.**
- Every state change emits a feed event: `site.listed`, `site.flagged`, `site.taken_down`, `site.resurrected`, `site.target_changed`.
- These yield **time-to-flag** and **time-to-takedown**, both measured per publisher and per impersonated target.

## 6. Contact policy: the only blocking decision (D1, D2)

The standing rule so far is "no HTTP to scam hosts". That rule caps what we can classify:

| Option | What contacts the scam host | (a) | (b) | (c) |
|---|---|---|---|---|
| **P0 passive**: DNS + RDAP + Safe Browsing API | Nothing | Partial: NXDOMAIN or hold only | Flag axis only | **Not possible.** "Resolves and not flagged" also covers suspended, parked and platform-404 sites. On the 15 shared-platform sites DNS always answers |
| **P1 contained probe** | One GET per check, from a separate egress | Full | Full | Full, subject to cloaking |
| **P2 third-party render** (urlscan.io, unlisted) | urlscan's browser, not us | Full | Full | Full, plus a screenshot. Shares the URL with urlscan; quota-limited |

**Constraints on a P1 probe:**
- no JavaScript, no rendering, no assets;
- no cookies, no forms;
- at most 5 redirects, each one recorded;
- body capped at 256 KB, stored only as hash, title and signature hits;
- TLS validity recorded.

**Recommendation:** P0 + P1. Use P2 only for the calibration sample and disputed cases. Run P1 from an egress that isn't this host (proxy or VPN), because scam operators can log and block the probing IP.

**Vantage caveat.** Scam kits commonly filter by country, user agent and datacenter IP. A probe from a non-SG cloud IP can get a blank page or a 404 while SG mobile users get the kit. Every verdict therefore records its vantage. An HTTP-only "gone" (DNS still resolving, no hold, not flagged) is downgraded to inconclusive unless corroborated.

## 7. Data-model changes (relational; no NoSQL needed)

- `v_site`: a view over `indicator` restricted to domain, hostname and url with at least one listing-publisher sighting.
- `indicator_entity`:
  - new relation `impersonates`;
  - new columns `is_primary`, `impersonation_kind`;
  - a partial unique index enforcing one primary per site.
- `liveness_check`: add `reach`, `flag`, `bucket`, `reason`, `sb` (threat types, as JSON) and `probe_policy` (P0/P1/P2). `dns`, `rdap`, `http`, `fingerprints` and `vantage` already exist.
- `indicator`: `liveness_state` becomes `site_bucket` + `site_reason` + `bucket_since` + `next_check_at`. Keep `last_live_at`, `registry_status` and `registration_expires_at`.
- `source`: new column `listing_role` (listing / watch / reference / parked).
- `feed_event`: the five site event kinds from §5.

## 8. Acceptance criteria (done means all of these hold)

1. Every site named by a listing publisher exists **once**, in canonical form, with at least one publication link and its publisher.
2. Every site has exactly one primary target or an explicit no-target kind. **No authentic host ever appears as a site.**
3. Every site has a current bucket with a reason code, a vantage and an evidence row. No site waits more than one hot-tier cycle for its first check.
4. `sgintel check` is extended to fail on any of:
   - a site with no publication;
   - a site with more than one primary target;
   - an authentic host in the site set;
   - a bucket without evidence.
5. **Calibration:** a 50-site sample, stratified across a, b and c, agrees with a real-browser view (urlscan screenshots, or an isolated VM) on at least 90% of buckets. Every disagreement becomes a rule fix.
6. The feed shows timestamped transitions, from which time-to-flag and time-to-takedown are computed per publisher and per target.

## 9. Out of scope / parked

- Phones, emails, SMS sender IDs, bank accounts, social handles, app IDs: kept in the DB, not processed.
- Generic global feeds as a discovery source.
- Text corpora (scamalert.sg, IMC'25).
- Rendering or screenshots at scale.
- Takedown reporting: we observe, we don't report.
- Chrome's client-side-only warnings (look-alike-URL suggestion, HTTPS-First). These depend on the user's own browser state and can't be reproduced server-side.

## 10. Decisions needed

| # | Decision | Recommendation |
|---|---|---|
| **D1** | Contact policy | **P0 + P1**, with P2 for calibration only |
| **D2** | Egress for P1 probes | A separate proxy or VPN, not this host |
| **D6** | Safe Browsing access | A free Google Cloud API key, for non-commercial use. If this moves into an institutional product (ARENA/IAIC), switch to the Web Risk API |
| D3 | Precedence of a over b | Taken-down first. Both axes are stored, so this is low-stakes |
| D4 | MAS IAL | Keep as an adjacent listing publisher, with `impersonation_kind` defaulting to `brand_abuse`/`unresolved`, excluded from the headline impersonation metrics |
| D5 | Generic feeds | Park. Optionally add a "also seen in feed X" cross-reference column later |
| D7 | TLS-invalid sites | Count as (b), with reason `tls_invalid` |

D1, D2 and D6 were settled on 2026-11-26 (P1; local proxy; SB built but off). D3–D7 run on the recommended defaults.

## 11. Implementation status (2026-11-26)

**Built** (package `sgintel/`, CLI `python -m sgintel …`):

| Piece | Where | Notes |
|---|---|---|
| Source roles | `roles.py`, `source.listing_role` | After the backfill: listing publishers SPF (icanact + police.gov.sg advisories), ICA, MOM, ScamShield, EnterpriseSG, PSD, SWDA, SGH, Ninja Van, Prudential; 1 adjacent (MAS); 7 parked. Parked feeds' endpoints are disabled; watch-only pages moved to monthly. Recomputed after every crawl, so promotion is automatic |
| Discovery follow-up | `followup.py` | Publications found in sitemaps/RSS are now fetched (official sites only, robots.txt, 2 s/host) and scanned for sites. Scam-titled pages first, at most 40 per crawl cycle, at most 3 attempts |
| Target resolver | `target.py`, `indicator_entity.is_primary`, `indicator.impersonation_kind` | One primary target per site, enforced by the unique index `ux_primary_target`. Brand tags are read from `report_entity`, never from rows the resolver rewrites |
| Egress proxy | `egress_proxy.py`, `bin/egress_proxy.sh start\|stop\|status` | Loopback only, GET/HEAD/CONNECT, ports 80/443. Refuses non-global IPs (incl. 169.254.169.254). 4 MB cap, logs to `logs/egress.jsonl`. Upstream hook: `SGINTEL_UPSTREAM_PROXY` |
| Probe | `probe.py` | Mobile-Chrome UA, HTTPS-first for bare hosts, ≤5 redirects including static meta-refresh / `location=` stubs (read from source, never executed). Keeps title, hash and signatures only. Signatures `v1.2` |
| Liveness | `liveness.py`, `liveness_check.{reach,flag,bucket,reason,sb,probe_policy}` | Two axes → a/b/c/inconclusive. Soft-gone needs a second observation ≥6 h later. §5 cadence. `site.*` feed events |
| Safe Browsing | `safebrowsing.py` | v5 `urls:search`. Off unless `SGINTEL_SAFEBROWSING=1` and `SGINTEL_SAFEBROWSING_KEY` are set |
| Views and report | `v_site`, `v_site_status`, `sites.py` → `data/SITES.md` | `v_site_status` is the deliverable row: site, kind, target, authentic hosts, publications[], publishers[], bucket, reason, flag, timestamps |
| Acceptance checks | `sgintel check` | 7 new checks from §8 |
| Rolling outputs | `output.py`, contract `schema/site_feed.schema.json` (site-feed/1.0) | Written after every crawl, liveness run and daemon loop: `out/events/site-events-YYYY-MM-DD.jsonl` (append-only SiteEvent, resumable by `seq`), `out/snapshots/sites-YYYY-MM-DD.jsonl` + `out/sites-latest.jsonl` (all SiteRecords), `out/reports/run-report-YYYY-MM-DD.txt` (one text block per run). Retention: snapshots 30 d, events/reports 365 d |

**Deviations and findings during the build:**
1. **Resolver.** This VM's system resolver silently times out on many listed scam domains that resolve publicly (a filtering upstream resolver), and direct :53 egress is blocked. Liveness and the proxy therefore resolve via DNS-over-HTTPS (`doh.py`, Google Public DNS). The vantage is recorded as `direct:<host>|doh:dns.google`. A SERVFAIL that comes from a dead delegation (zone removed at the DNS host, e.g. Cloudflare REFUSED) is a soft-gone signal, `dns_dead_delegation`.
2. **Narrative-page false positives.** Grab's illustrative `go0gle.com`/`google.com`, e-mail fragments (`tenders.caas.gov@…`), legitimate links (bit.ly, asiaone, kkday) and `pango.gov.sg` were marked as scam sites. Fixes:
   - on narrative pages, a site must be named as fake/phishing within ±80 characters;
   - e-mail local parts are skipped;
   - `*.gov.sg`, `*.edu.sg` and `*.mil.sg` are never scam sites;
   - a small set of reference hosts is excluded.

   Fake-site list pages (e.g. ICA's SGAC annex) keep their scam-site default.
   *Revised after the publication backfill (1,556 pages, 2026-11-26).* The ±80-character rule still let through cited sources ("Source: www.airdroid.com"),
   security-blog links in CSA advisories, a CCS fake-reviews case and "fake Instagram accounts such as govh.sg". A narrative page now has to name the
   site *as* a site: a website-noun phrase ("fake/phishing/fraudulent … website/URL/link", "impersonating …", "claims to be", "not affiliated with")
   within 140 characters before or 60 after it. Citations and social-handle mentions are excluded, and so are hypothetical illustrations
   ("fraudsters may … like using Go0gle.com"). With this rule, PSD's `jobsingapore24h.com` ("a job scam website") is recovered.
3. **JS stubs.** Parked domains often serve a ~100-byte script stub. The probe follows static redirects from the stub, and infrastructure signatures are matched on raw markup (e.g. GoDaddy's `wsimg.com/parking-lander`). An unresolved stub of 512 bytes or less is `inconclusive: script_stub`, never live.
4. **Calibration checks.** The first 8 checks were made with the filtered resolver and were discarded.

**Not done yet:**
- The §8.5 calibration sample (50 sites against a real browser view; urlscan or an isolated VM).
- A `repurposed` detector (needs a first-seen content baseline).
- Retroactive cleanup of `site.live` events emitted by pre-v1.2 signatures.
