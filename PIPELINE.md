# sgintel pipeline: crawler + relational store (v0.1, 2026-11-26)

> **2026-11-26:** scope narrowed to impersonating-site liveness. See `SCOPE.md` (mandate, decisions, §11 implementation status). The crawler and dedup described here still run unchanged; generic feeds are parked and narrative pages are on a monthly watch.

Code: `sgintel/` · DB: `data/sgintel.db` (SQLite, WAL) · generated reports: `data/CATALOG.md`, `data/DEDUP.md`
Run: `.venv/bin/python -m sgintel {init|load|crawl|daemon|liveness|dedup|export --since N|import|stats}`

## 1. Which sources are SG-native and which need filtering

| Scope | Count | What | Ingestion rule |
|---|---|---|---|
| **native** | 313 sources | SPF icanact, MAS IAL, ICA SGAC annex, ScamShield/MHA/CSA/NCPC/… RSS, agency and SG-brand sitemaps and scam pages | everything ingested. Roles: explicit (structured feeds) or context rule (narrative pages) |
| **filtered** | 7 sources | Phishing.Database (NEW-today, links ACTIVE, domains ACTIVE), Phishing Army, PhishDestroy, OpenPhish, PhishStats | each item must pass `sg_filter_pass()`: an SG brand/service token in the host, or an SG bank kit path. A `.sg` ccTLD alone is **rejected**, because those are mostly compromised SMEs phishing non-SG brands |
| **allowlist** | 43 sources | official-channel pages (genuine domains, sender IDs, hotlines) | feed `entity_official`, never the IOC stream |

Global brands from the SPF tag map (WhatsApp, NVIDIA, TikTok…) contribute **allowlist entries only**. Their scam
pages are not SG-specific and are not crawled. Full per-source table: `data/CATALOG.md`.

## 2. Why relational (and not NoSQL)
Every source normalises into the schema v0.1 records (entity, source, report, indicator, sighting, liveness_check,
feed_event), so a relational store with constraints fits. The only semi-structured residue (raw source records,
page bodies, sg_signals) lives in JSON-in-TEXT columns, so no document store is needed. DDL is Postgres-portable:
swap TEXT JSON for JSONB when moving off SQLite.

## 3. Duplicate handling ("cross-verify duplicacy")
| Layer | Mechanism |
|---|---|
| same observable from many sources | `indicator UNIQUE(type,value)` + deterministic `ind_…` id; each source adds a `sighting` (`UNIQUE(source,report,indicator)`) |
| same advisory re-ingested | `report UNIQUE(source_id,native_id)`; body hash detects edits (`status=updated`) |
| same advisory on two sites | `report.fingerprint` (normalised title + month) → view `v_report_dup` |
| same page/feed for several registry entries | `endpoint UNIQUE(url)`: 28 sitemaps/feeds shared by 2–9 pages are fetched **once** |
| same page listed twice | `source UNIQUE(url)` (the IPOS double entry collapsed) |
| same organisation under two ids | `dedup.py` auto-merge via `entity.canonical_entity_id` (`uobkh.com`→`uobkh.com.sg`; MOT voucher programme ids) |
| domain claimed by unrelated entities | `v_official_conflict` review queue (10, all legitimate shared platforms: go.gov.sg, redeem.gov.sg, HealthHub, Link); `v_shared_channel` (gov.sg sender ID ×83) |
| scam indicator that is actually official | `v_ioc_conflict`; lifecycle forces `allowlisted`, never emitted |

## 4. Polling: scheduled tiers + rolling adaptive poller
Tier is set from page kind and recency (`catalog.tier_for`):
| Tier | Base interval (min–max) | Gets |
|---|---|---|
| hot | 1h (15min–3h) | SPF icanact, ScamShield scam-alert RSS, Phishing.Database NEW-today, PhishStats (20-keyword rotation ≈ 48 req/day, under the 50 anonymous limit) |
| daily | 24h (6h–3d) | agency RSS, fake-indicator lists updated in the last year, advisory feeds updated in the last 90d, global blocklists |
| weekly | 7d (2–14d) | official-channel pages, alert pages updated in the last year, stale advisory feeds, sitemaps |
| monthly | 30d (14–60d) | FAQs, statistics, report portals, old alerts |
| manual | n/a | robots-disallowed endpoints (OpenSanctions); operator runs `sgintel import` |

Rolling poller (`crawler.daemon`): a due-first queue. After each fetch the interval halves on change, grows ×1.5
when unchanged, doubles on error, all within the tier bounds and with ±10% jitter. After 6 consecutive errors the
endpoint is disabled with a reason. Politeness: robots.txt honoured (cached 24h), at least 2 s between requests to a host, conditional
GET (ETag / If-Modified-Since), content-hash short-circuit, 120 MB cap. Deploy as `daemon` under systemd, or
`crawl` from cron every 5–10 min. Liveness runs separately: `sgintel liveness` (DNS + RDAP only, rechecking active
indicators every 24h and inactive ones weekly).

## 5. Known limits / decisions pending
- **OpenSanctions robots.txt disallows automated agents**, so MAS IAL refresh is manual (`import`) until we pick an
  option: OpenSanctions API key or licence, scheduled human download, or asking MAS for a feed.
- Narrative-page indicator roles use a keyword-context rule (SCHEMA §10 Q6). Candidates for a local-LLM classifier.
- No HTTP to scam hosts (Q3), so shared-platform hosts stay `unverified` until that is decided.
- JS-only and bot-protected pages (HDB, IMDA, PDPC, Carousell, FairPrice, M1, SIMBA…) yield titles or nothing.
