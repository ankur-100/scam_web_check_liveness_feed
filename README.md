# sgintel — Singapore impersonating-site liveness feed

sgintel tracks **websites that impersonate real Singapore organisations**, as named in official scam advisories. The main source is the
SPF "I can ACT against scams" site; ICA, MOM, police.gov.sg, ScamShield, Ninja Van and other publishers are also covered.
For every site it records:

- the publication(s) that named it, and who published them;
- the **one authentic organisation and website it imitates**;
- whether it is still up, in the three states a Chrome user would meet:

| State | Meaning | Examples of evidence |
|---|---|---|
| **(a) taken down** | not reachable | domain deleted, registrar hold, DNS zone removed, FBI seizure banner, parked or for sale, hosting platform removed the app |
| **(b) flagged** | still serving, but behind a warning the user can click through | Cloudflare "Suspected Phishing" page, invalid TLS certificate (Safe Browsing too, once enabled) |
| **(c) live** | serving normally, no warning seen | page loads |
| inconclusive | can't tell from this vantage point yet | timeouts, bot challenges, geo-blocks, a first takedown signal awaiting its confirming re-check |

The pipeline polls the publishers on their update cycles, finds new advisories, extracts the sites they name and re-checks every site on
a schedule. It writes rolling JSONL and text outputs (see [Outputs](#outputs)).

> **Handle with care.** The database, `out/` and the logs contain **live scam URLs**. Use the `value_defanged` field (`example[.]com`) when
> displaying or sharing them, and never open them in a normal browser.

## Status (2026-11-27)

| Sites | (c) live | (b) flagged | (a) taken down | inconclusive | total |
|---|---|---|---|---|---|
| named in impersonation advisories ("listing") | 52 | 4 | 325 | 36 | 417 |
| MAS Investor Alert List ("adjacent", unlicensed entities) | 130 | 1 | 590 | 177 | 898 |

`sgintel check` passes all 17 assertions. Open items: the 50-site calibration against a real browser view (SCOPE.md §8.5); the polling
daemon is built but **not started**; Safe Browsing is built but **off** (decision D6).

## Quick start

```bash
cd ~/scamtrends_feed
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt     # skip if .venv exists

# one-time: database + registry (entities, official domains, publisher pages, poll tiers)
.venv/bin/python -m sgintel init
.venv/bin/python -m sgintel load
.venv/bin/python -m sgintel import --source mas-ial-opensanctions --file data/fixtures/mas_ial_source.json   # robots.txt blocks polling it

# every scam-site probe leaves through the egress proxy; the pipeline refuses to probe without it
bin/egress_proxy.sh start

# one full pass by hand
.venv/bin/python -m sgintel crawl          # poll due publishers -> follow-up -> targets -> queue new sites -> write outputs
.venv/bin/python -m sgintel liveness -v    # check due sites -> write outputs
.venv/bin/python -m sgintel check          # integrity + acceptance assertions (exit 1 on failure)

# or run continuously (crawl + due site checks in a loop, until stopped)
bin/sgintel_daemon.sh start                # stop | status

# or as self-sustaining systemd user services (restart on crash, start at boot; user lingering is on)
bin/egress_proxy.sh stop                   # free :18080 first if the script-started proxy is running
cp bin/sgintel-*.service ~/.config/systemd/user/ && systemctl --user daemon-reload
systemctl --user enable --now sgintel-proxy sgintel-daemon
systemctl --user status sgintel-daemon ; tail -f logs/sgintel_daemon.log
```

## How it works

```
publishers (icanact, police.gov.sg sitemap, ICA/MOM pages, RSS …)
   │  crawl: tiered adaptive poller (hot ≈1h · daily · weekly · monthly); robots.txt, 2 s per host, conditional GET
   ▼
reports (publications) ──follow-up──► newly discovered advisory pages are fetched and scanned for sites
   │  ingest: canonicalise, dedup by unique keys, decide role (scam site / official / mention)
   ▼
indicator + sighting (per source and publication) ──► v_site (sites from listing publishers)
   │  target.py: one primary impersonated entity per site (brand tag > look-alike token > publisher itself)
   ▼
liveness.py ── DNS over HTTPS + RDAP + one contained GET via the egress proxy (+ Safe Browsing when enabled)
   │  two axes (reach × flag) → (a) / (b) / (c) / inconclusive; soft takedown signals need a second check ≥6 h later
   ▼
feed_event (site.listed / live / flagged / taken_down / resurrected / target_changed) ──► out/ (JSONL + TXT)
```

**Publisher roles** (`source.listing_role`, recomputed after every crawl):

| Role | What it covers | Polling |
|---|---|---|
| `listing` | names impersonating sites | normal tiers |
| `adjacent` | MAS Investor Alert List | normal tiers |
| `watch` | the same publishers' narrative pages | monthly; promoted automatically if they start naming sites |
| `reference` | official-channel pages | feed the allowlist |
| `parked` | generic global phishing feeds | disabled |

**Re-check cadence:**

| State | Re-checked |
|---|---|
| live / flagged | every 6 h in the first week after listing, then daily |
| taken down | at 1, 3 and 7 days, then weekly; archived after 90 days without serving (watching for resurrection) |
| inconclusive | at 1 h, 6 h, 24 h, then daily |

## Probe and safety policy

These rules were agreed in SCOPE.md §6 (decisions D1 and D2).

**Egress proxy** (`sgintel/egress_proxy.py`, `127.0.0.1:18080`):
- loopback only;
- GET/HEAD and CONNECT only, on ports 80/443 only;
- refuses private, loopback and cloud-metadata addresses;
- caps each connection at 4 MB and logs every decision to `logs/egress.jsonl`;
- probes exit from **this host's IP** unless `SGINTEL_UPSTREAM_PROXY=http://[user:pass@]host:port` is set.

**Probe** (`sgintel/probe.py`):
- sends one GET per hop, with no JavaScript, rendering, sub-resources, cookies or form submission;
- follows at most 5 redirects;
- reads at most 256 KB and keeps only the title, a SHA-256 hash and signature hits;
- uses a mobile-Chrome UA with `en-SG`.

**DNS:** sites are resolved via DNS-over-HTTPS (`dns.google`), because this VM's system resolver silently drops many scam domains.

**Publisher crawling:**
- official sites only;
- robots.txt honoured;
- no bot-protection bypass.

The Directus backend behind icanact was never probed.

## Outputs

Every crawl, liveness run and daemon loop appends to `out/`. Contract: [`schema/site_feed.schema.json`](schema/site_feed.schema.json)
(JSON Schema 2020-12, `site-feed/1.0`).

| File | Rolls | Contents |
|---|---|---|
| `out/sites-current.txt` | rewritten each run | **plain-text table of every site**: state, site (defanged), what it spoofs (target / authentic site), reason, last checked, publisher |
| `out/reports/run-report-YYYY-MM-DD.txt` | daily, one block appended per run | state totals, new listings, every transition (site, old → new, reason, target, publisher), what's due next |
| `out/events/site-events-YYYY-MM-DD.jsonl` | daily, append-only | one `SiteEvent` per state change; resume from the last `seq` you processed |
| `out/snapshots/sites-YYYY-MM-DD.jsonl` | rewritten each run | one `SiteRecord` per site (end-of-day state); `out/sites-latest.jsonl` is the newest copy |

Snapshots are kept 30 days, and events and reports 365 days.

The fields of a `SiteRecord`:

| Group | Fields |
|---|---|
| identity | `site_id`, `type`, `value`, `value_defanged`, `hostname`, `registrable_domain`, `is_shared_platform`, `listing_role`, `lifecycle_status` |
| `impersonation` | `kind` (clone / brand_abuse / fictitious / multiple / unresolved), `target_entity_id`, `target_name`, `target_method`, `authentic_hosts[]`, `other_brands[]`, `targets[]` (every candidate with its authentic hosts) |
| `provenance` | `publishers[]`, `publications[]`, `first_published_at`, `first_listed_at` |
| `liveness` | `bucket`, `chrome_state` (a/b/c), `reason`, `reach`, `flag`, `bucket_since`, `last_checked_at`, `last_live_at`, `next_check_at`, `evidence{…}` |
| `registration` | `registry_status[]`, `expires_at` |

Other views:
- `data/SITES.md`: a human report (`sgintel sites`);
- `v_site_status` in `data/sgintel.db`: one row per site;
- `sgintel export --since SEQ`: all feed events as JSONL on stdout.

## Commands

| Command | What it does |
|---|---|
| `init`, `load` | create schema; load registry → entities, official domains (allowlist), sources, endpoints |
| `crawl [--limit N] [--tier T] [--source ID]` | poll due publisher endpoints, then the post-crawl cycle and outputs |
| `cycle [--followup N]` | post-crawl cycle only: roles → follow-up → targets → queue new sites |
| `followup [--limit N]` | fetch discovered publications (scam-titled first) and extract sites |
| `liveness [--limit N] [--scope all\|listing] [--policy P1\|P0] [--workers 8] [-v]` | check due sites; `P0` = DNS/RDAP only, no HTTP |
| `roles`, `targets` | recompute publisher roles / impersonation targets |
| `dedup` | self-heal near-duplicates, re-apply role rules to history, write `data/DEDUP.md` |
| `check` | 17 assertions: no duplicates, every site has a publication, ≤1 primary target, no authentic host in the site set, every state has evidence, … |
| `sites`, `output`, `stats`, `catalog`, `export` | reports and outputs |
| `import --source ID --file F` | ingest an operator-supplied snapshot (for sources whose polling robots.txt forbids) |
| `proxy`, `daemon` | long-running processes; use `bin/egress_proxy.sh` / `bin/sgintel_daemon.sh` |

Environment variables:

| Variable | Purpose |
|---|---|
| `SGINTEL_UPSTREAM_PROXY` | route probes out through another IP |
| `SGINTEL_VANTAGE` | label for that vantage |
| `SGINTEL_SAFEBROWSING=1` and `SGINTEL_SAFEBROWSING_KEY=…` | enable Safe Browsing v5 (free, non-commercial use; use Web Risk for commercial use) |
| `SGINTEL_PROXY_LISTEN` / `SGINTEL_PROBE_PROXY` | proxy listen address / proxy URL used by the probe |

## Repository layout

```
sgintel/            the pipeline package (CLI: python -m sgintel)
  db.py             SQLite schema, migrations, views (v_site, v_site_status, provenance/dedup views)
  catalog.py        registry -> sources/endpoints/poll tiers     crawler.py   scheduler, post-crawl cycle, daemon
  fetch.py          polite fetcher for official sites            parsers/     icanact RSC, RSS, sitemap, HTML, MAS, feeds
  ingest.py         role rules, entity links                    normalize.py ids, canonical values, extraction
  roles.py          publisher roles                              followup.py  discovered-publication fetcher
  target.py         impersonation target resolver                lifecycle.py indicator status/TTL
  egress_proxy.py   contained egress                             probe.py     contained GET + page signatures
  doh.py            DNS-over-HTTPS                               liveness.py  two-axis verdicts, cadence, site events
  safebrowsing.py   Safe Browsing v5 (off)                       output.py    rolling out/ files     sites.py  SITES.md
bin/                egress_proxy.sh, sgintel_daemon.sh
schema/             site_feed.schema.json (output contract); sg_scam_intel.schema.json + SCHEMA.md (v0.1 data model)
registry/           entity/official-domain registry (266 entities); merged/ is what `load` reads
data/               sgintel.db (+ pre-scope backup), fixtures/, CATALOG.md, DEDUP.md, SITES.md
out/                rolling outputs        logs/  crawl, liveness, follow-up, egress logs
sources/, raw/      source survey notes and raw captures     extract.py  standalone icanact extractor
```

## Documents

| File | Read it for |
|---|---|
| [SCOPE.md](SCOPE.md) | **the mandate**: objective, state definitions, contact policy, decisions D1–D7, acceptance criteria, implementation status and findings (§11) |
| [FINDINGS.md](FINDINGS.md) | how the icanact feed works (Next.js RSC stream, Directus fields, no expiry/status fields) |
| [SOURCES.md](SOURCES.md), `sources/` | survey of SG and global scam-indicator sources |
| [PIPELINE.md](PIPELINE.md) | the original crawler and relational design (pre-scope; still accurate for crawl and dedup) |
| `schema/SCHEMA.md` | v0.1 record types and lifecycle semantics |
| `registry/FORMAT.md` | registry record format |

## Known limits

- **One vantage point.** Every verdict comes from this host via `dns.google`. Kits that block datacenter or non-SG visitors can look dead or
  inconclusive from here (each record carries `evidence.vantage`).
- **Safe Browsing is off.** Some (c) sites may already show Chrome's red warning; `flag = not_checked` marks that.
- **Page signatures are first-pass** (`sig_version`). A few "live" sites look repurposed (unrelated content), and the calibration sample
  should settle them.
- **Targets.** When no registry brand fits, the target is read from the advisory itself ("Fake Banking Websites Impersonating DBS and UOB",
  "URLs impersonating Singapore Pools' websites"). Brands outside the registry become `text:<name>` entities (e.g. AXS, Domino's), with any
  official domain the advisory cites. 36 of 417 listing sites stay `unresolved`, because their advisories are generic
  ("Investment Scams Promising High Returns") or name two brands with nothing in the URL to choose between them (DBS/UOB).
- **Narrative-page extraction** relies on wording ("fake website …", "impersonating …"). Sites named without such wording are missed.
- **Host.** The project runs on gpu25. Moving it means copying `data/`, `out/` and `registry/merged/` and restarting the proxy.
