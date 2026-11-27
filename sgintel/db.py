"""Relational store for schema v0.1 (SQLite now; DDL kept Postgres-portable: TEXT/INTEGER/REAL + JSON-in-TEXT).

Dedup is enforced by constraints, not by convention:
  indicator(type,value) UNIQUE · sighting(source,report,indicator) UNIQUE · report(source,native_id) UNIQUE
  endpoint(url) UNIQUE (one fetch serves many sources) · source(url) UNIQUE · entity_official(kind,value,entity) PK
Cross-record duplicates that constraints can't express (same advisory on two sites, one domain claimed by two
unrelated entities, near-identical entity ids) are surfaced by views + dedup.py.
"""
import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "sgintel.db"

DDL = r"""
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS entity (
  entity_id TEXT PRIMARY KEY, name TEXT NOT NULL, abbr TEXT,
  kind TEXT NOT NULL CHECK (kind IN ('organisation','programme','fictitious_brand','placeholder')),
  sector TEXT, country TEXT NOT NULL DEFAULT 'SG',
  parent_entity_id TEXT REFERENCES entity(entity_id),
  canonical_entity_id TEXT REFERENCES entity(entity_id),      -- set when merged as a duplicate
  notes TEXT, verified_at TEXT);
CREATE TABLE IF NOT EXISTS entity_alias (
  entity_id TEXT NOT NULL REFERENCES entity(entity_id), alias TEXT NOT NULL, alias_norm TEXT NOT NULL,
  origin TEXT NOT NULL, spf_tag_id TEXT, PRIMARY KEY (alias_norm, entity_id));
CREATE TABLE IF NOT EXISTS entity_official (                   -- allowlist
  kind TEXT NOT NULL CHECK (kind IN ('domain','host','sms_sender_id','hotline','short_link_domain','social','app','email')),
  value TEXT NOT NULL, entity_id TEXT NOT NULL REFERENCES entity(entity_id), evidence TEXT,
  PRIMARY KEY (kind, value, entity_id));
CREATE INDEX IF NOT EXISTS ix_official_value ON entity_official(value);

CREATE TABLE IF NOT EXISTS endpoint (                          -- what we actually fetch (deduped by URL)
  endpoint_id INTEGER PRIMARY KEY, url TEXT NOT NULL UNIQUE, host TEXT NOT NULL,
  fetch_kind TEXT NOT NULL CHECK (fetch_kind IN ('html','html_rsc','rss','atom','sitemap','json','txt','csv','pdf','api')),
  parser TEXT NOT NULL, tier TEXT NOT NULL CHECK (tier IN ('hot','daily','weekly','monthly','manual')),
  interval_s INTEGER NOT NULL, min_interval_s INTEGER NOT NULL, max_interval_s INTEGER NOT NULL,
  next_due_at TEXT, last_fetched_at TEXT, last_changed_at TEXT, etag TEXT, last_modified TEXT, last_sha256 TEXT,
  consecutive_unchanged INTEGER NOT NULL DEFAULT 0, consecutive_errors INTEGER NOT NULL DEFAULT 0,
  enabled INTEGER NOT NULL DEFAULT 1, disabled_reason TEXT, params TEXT);           -- params: JSON
CREATE TABLE IF NOT EXISTS source (
  source_id TEXT PRIMARY KEY, name TEXT, publisher_entity_id TEXT REFERENCES entity(entity_id),
  url TEXT NOT NULL UNIQUE, endpoint_id INTEGER REFERENCES endpoint(endpoint_id),
  page_kind TEXT, access TEXT, authority TEXT NOT NULL,
  sg_scope TEXT NOT NULL CHECK (sg_scope IN ('native','filtered','allowlist')),
  sg_filter_id TEXT, lifecycle_semantics TEXT NOT NULL, default_role TEXT NOT NULL DEFAULT 'unknown',
  lists_indicators TEXT, licence TEXT, tlp TEXT NOT NULL DEFAULT 'TLP:CLEAR', notes TEXT);
CREATE TABLE IF NOT EXISTS fetch_log (
  fetch_id INTEGER PRIMARY KEY, endpoint_id INTEGER NOT NULL REFERENCES endpoint(endpoint_id),
  started_at TEXT NOT NULL, http_status INTEGER, bytes INTEGER, sha256 TEXT, changed INTEGER,
  duration_ms INTEGER, error TEXT, n_reports INTEGER, n_indicators INTEGER);

CREATE TABLE IF NOT EXISTS report (
  report_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source(source_id), native_id TEXT NOT NULL,
  url TEXT, issuer_entity_id TEXT REFERENCES entity(entity_id), title TEXT NOT NULL, summary TEXT, body_md TEXT,
  published_at TEXT, modified_at TEXT, fingerprint TEXT NOT NULL, body_sha256 TEXT,
  status TEXT NOT NULL DEFAULT 'published' CHECK (status IN ('published','updated','withdrawn')),
  first_ingested_at TEXT NOT NULL, last_ingested_at TEXT, withdrawn_at TEXT, raw TEXT,
  UNIQUE (source_id, native_id));
CREATE INDEX IF NOT EXISTS ix_report_fp ON report(fingerprint);
CREATE TABLE IF NOT EXISTS report_category (report_id TEXT NOT NULL REFERENCES report(report_id), category TEXT NOT NULL, raw TEXT,
  PRIMARY KEY (report_id, category));
CREATE TABLE IF NOT EXISTS report_entity (report_id TEXT NOT NULL REFERENCES report(report_id), entity_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('impersonated','fictitious_brand','mentioned')), PRIMARY KEY (report_id, entity_id, role));

CREATE TABLE IF NOT EXISTS indicator (
  indicator_id TEXT PRIMARY KEY, type TEXT NOT NULL, value TEXT NOT NULL, value_defanged TEXT,
  hostname TEXT, registrable_domain TEXT, tld TEXT, is_shared_platform INTEGER, block_scope TEXT,
  sg_score REAL, sg_signals TEXT,
  status TEXT NOT NULL DEFAULT 'unverified', status_reason TEXT, confidence INTEGER,
  first_seen TEXT, last_seen TEXT, first_reported_at TEXT, valid_until TEXT, revoked INTEGER NOT NULL DEFAULT 0,
  liveness_state TEXT, liveness_since TEXT, last_checked_at TEXT, last_live_at TEXT, consecutive_failures INTEGER DEFAULT 0,
  registration_expires_at TEXT, registry_status TEXT,
  version INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  UNIQUE (type, value));
CREATE INDEX IF NOT EXISTS ix_ind_regdom ON indicator(registrable_domain);
CREATE INDEX IF NOT EXISTS ix_ind_status ON indicator(status);
CREATE TABLE IF NOT EXISTS indicator_entity (indicator_id TEXT NOT NULL REFERENCES indicator(indicator_id), entity_id TEXT NOT NULL,
  relation TEXT NOT NULL CHECK (relation IN ('impersonates','fictitious_brand','lookalike')), method TEXT, score REAL,
  PRIMARY KEY (indicator_id, entity_id, relation));
CREATE TABLE IF NOT EXISTS indicator_category (indicator_id TEXT NOT NULL REFERENCES indicator(indicator_id), category TEXT NOT NULL,
  PRIMARY KEY (indicator_id, category));
CREATE TABLE IF NOT EXISTS sighting (
  sighting_id TEXT PRIMARY KEY, indicator_id TEXT NOT NULL REFERENCES indicator(indicator_id),
  source_id TEXT NOT NULL REFERENCES source(source_id), report_id TEXT REFERENCES report(report_id),
  role TEXT NOT NULL CHECK (role IN ('ioc','official','mention_benign','unknown')),
  source_first_seen TEXT, source_last_seen TEXT, source_status TEXT,
  first_ingested_at TEXT NOT NULL, last_ingested_at TEXT, removed_at TEXT, raw TEXT);
CREATE UNIQUE INDEX IF NOT EXISTS ux_sighting ON sighting(source_id, IFNULL(report_id,''), indicator_id);

CREATE TABLE IF NOT EXISTS liveness_check (
  check_id TEXT PRIMARY KEY, indicator_id TEXT NOT NULL REFERENCES indicator(indicator_id), checked_at TEXT NOT NULL,
  vantage TEXT, dns TEXT, rdap TEXT, http TEXT, fingerprints TEXT, verdict TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS feed_event (
  seq INTEGER PRIMARY KEY AUTOINCREMENT, emitted_at TEXT NOT NULL,
  op TEXT NOT NULL CHECK (op IN ('upsert','status_change','revoke','delete')),
  object_type TEXT NOT NULL, object_id TEXT NOT NULL, version INTEGER NOT NULL,
  changed_fields TEXT, previous_status TEXT, snapshot TEXT);

-- duplicate / conflict views ------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_official_conflict AS          -- same domain/host owned by unrelated, non-merged entities (review queue)
  SELECT o1.kind, o1.value, o1.entity_id AS a, o2.entity_id AS b,
         (SELECT COUNT(DISTINCT entity_id) FROM entity_official x WHERE x.kind=o1.kind AND x.value=o1.value) AS n_claimants
  FROM entity_official o1 JOIN entity_official o2 ON o1.kind=o2.kind AND o1.value=o2.value AND o1.entity_id < o2.entity_id
  JOIN entity e1 ON e1.entity_id=o1.entity_id JOIN entity e2 ON e2.entity_id=o2.entity_id
  WHERE o1.kind IN ('domain','host')
    AND IFNULL(e1.parent_entity_id,'') <> e2.entity_id AND IFNULL(e2.parent_entity_id,'') <> e1.entity_id
    AND IFNULL(e1.canonical_entity_id,'') <> e2.entity_id AND IFNULL(e2.canonical_entity_id,'') <> e1.entity_id
    AND IFNULL(e1.canonical_entity_id,e1.entity_id) <> IFNULL(e2.canonical_entity_id,e2.entity_id)
    AND substr(e1.entity_id,1,instr(e1.entity_id||'#','#')-1) <> substr(e2.entity_id,1,instr(e2.entity_id||'#','#')-1);
CREATE VIEW IF NOT EXISTS v_shared_channel AS             -- channels legitimately shared across many entities (gov.sg sender ID, go.gov.sg)
  SELECT kind, value, COUNT(DISTINCT entity_id) n FROM entity_official GROUP BY kind, value HAVING n >= 3;
CREATE VIEW IF NOT EXISTS v_report_dup AS                 -- same advisory republished by another source
  SELECT r1.report_id AS a, r2.report_id AS b, r1.fingerprint FROM report r1 JOIN report r2
  ON r1.fingerprint=r2.fingerprint AND r1.report_id < r2.report_id AND r1.source_id <> r2.source_id;
CREATE VIEW IF NOT EXISTS v_ioc_conflict AS               -- IOC that is also on the allowlist (false-positive guard)
  SELECT i.indicator_id, i.value, o.entity_id FROM indicator i
  JOIN entity_official o ON o.kind IN ('domain','host') AND (o.value=i.hostname OR o.value=i.registrable_domain)
  JOIN sighting s ON s.indicator_id=i.indicator_id AND s.role='ioc';
CREATE VIEW IF NOT EXISTS v_indicator_provenance AS        -- one row per indicator; multi-valued provenance as JSON arrays
  SELECT i.indicator_id, i.type, i.value, i.status, i.confidence, i.first_seen, i.last_seen,
    (SELECT json_group_array(DISTINCT s.source_id) FROM sighting s WHERE s.indicator_id=i.indicator_id) AS sources,
    (SELECT json_group_array(DISTINCT src.publisher_entity_id) FROM sighting s JOIN source src USING(source_id)
       WHERE s.indicator_id=i.indicator_id AND src.publisher_entity_id IS NOT NULL) AS issuer_entities,
    (SELECT json_group_array(DISTINCT s.role) FROM sighting s WHERE s.indicator_id=i.indicator_id) AS roles,
    (SELECT json_group_array(DISTINCT s.report_id) FROM sighting s WHERE s.indicator_id=i.indicator_id AND s.report_id IS NOT NULL) AS reports,
    (SELECT json_group_array(DISTINCT ie.entity_id) FROM indicator_entity ie WHERE ie.indicator_id=i.indicator_id AND ie.relation IN ('impersonates','lookalike')) AS impersonated_entities,
    (SELECT json_group_array(DISTINCT ie.entity_id) FROM indicator_entity ie WHERE ie.indicator_id=i.indicator_id AND ie.relation='fictitious_brand') AS fictitious_brands,
    (SELECT json_group_array(DISTINCT c.category) FROM indicator_category c WHERE c.indicator_id=i.indicator_id) AS categories,
    (SELECT COUNT(*) FROM sighting s WHERE s.indicator_id=i.indicator_id) AS n_sightings,
    (SELECT COUNT(DISTINCT s.source_id) FROM sighting s WHERE s.indicator_id=i.indicator_id) AS n_sources
  FROM indicator i;
CREATE VIEW IF NOT EXISTS v_feed AS                        -- current consumable IOC set
  SELECT * FROM indicator WHERE status IN ('active','unverified','inactive') AND revoked=0
    AND indicator_id IN (SELECT indicator_id FROM sighting WHERE role='ioc');
"""

def connect(path=DB_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL"); con.execute("PRAGMA foreign_keys=ON")
    return con

def init(con):
    con.executescript(DDL); con.commit(); migrate(con)

J = lambda x: None if x is None else json.dumps(x, ensure_ascii=False, sort_keys=True)

# ---- SCOPE.md (2026-11-26): impersonating-site liveness. Additive migration: ALTER TABLE only, views rebuilt on every run.
MIGRATIONS = {
  "source": [("listing_role", "TEXT")],                       # listing | adjacent | watch | reference | parked  (roles.py)
  "indicator": [("impersonation_kind", "TEXT"),               # clone | brand_abuse | fictitious | unresolved  (target.py)
                ("first_listed_at", "TEXT"),
                ("site_bucket", "TEXT"),                      # taken_down | flagged | live | inconclusive  (liveness.py)
                ("site_reason", "TEXT"), ("site_reach", "TEXT"), ("site_flag", "TEXT"),
                ("bucket_since", "TEXT"), ("bucket_streak", "INTEGER NOT NULL DEFAULT 0"), ("next_check_at", "TEXT")],
  "indicator_entity": [("is_primary", "INTEGER NOT NULL DEFAULT 0")],
  "liveness_check": [("reach", "TEXT"), ("flag", "TEXT"), ("bucket", "TEXT"), ("reason", "TEXT"), ("sb", "TEXT"), ("probe_policy", "TEXT")],
  "feed_event": [("event", "TEXT")],                          # site.listed | site.live | site.flagged | site.taken_down | site.resurrected | site.target_changed
}
SITE_TYPES = ("domain", "hostname", "url")
SITE_DDL = r"""
CREATE UNIQUE INDEX IF NOT EXISTS ux_primary_target ON indicator_entity(indicator_id) WHERE is_primary=1;
CREATE INDEX IF NOT EXISTS ix_ind_next_check ON indicator(next_check_at);
CREATE INDEX IF NOT EXISTS ix_lc_ind ON liveness_check(indicator_id, checked_at);
DROP VIEW IF EXISTS v_site_status; DROP VIEW IF EXISTS v_site;
CREATE VIEW v_site AS                  -- impersonating sites: named as a scam site in a publication of a listing/adjacent publisher
  SELECT i.* FROM indicator i
  WHERE i.type IN ('domain','hostname','url') AND i.status <> 'allowlisted'
    AND EXISTS (SELECT 1 FROM sighting s JOIN source src USING(source_id)
                WHERE s.indicator_id=i.indicator_id AND s.role='ioc' AND s.report_id IS NOT NULL
                  AND src.listing_role IN ('listing','adjacent'));
CREATE VIEW v_site_status AS           -- the deliverable: one row per site, multi-valued provenance as JSON arrays
  SELECT i.indicator_id, i.type, i.value, i.value_defanged, i.hostname, i.registrable_domain, i.is_shared_platform, i.impersonation_kind,
    (SELECT ie.entity_id FROM indicator_entity ie WHERE ie.indicator_id=i.indicator_id AND ie.is_primary=1) AS target_entity_id,
    (SELECT e.name FROM indicator_entity ie JOIN entity e USING(entity_id) WHERE ie.indicator_id=i.indicator_id AND ie.is_primary=1) AS target_name,
    (SELECT ie.method FROM indicator_entity ie WHERE ie.indicator_id=i.indicator_id AND ie.is_primary=1) AS target_method,
    (SELECT json_group_array(DISTINCT o.value) FROM indicator_entity ie JOIN entity_official o ON o.entity_id=ie.entity_id
       WHERE ie.indicator_id=i.indicator_id AND ie.is_primary=1 AND o.kind IN ('domain','host')) AS authentic_hosts,
    (SELECT json_group_array(DISTINCT ie.entity_id) FROM indicator_entity ie WHERE ie.indicator_id=i.indicator_id AND ie.is_primary=0) AS other_brands,
    (SELECT json_group_array(DISTINCT r.url) FROM sighting s JOIN report r ON r.report_id=s.report_id JOIN source src ON src.source_id=s.source_id
       WHERE s.indicator_id=i.indicator_id AND s.role='ioc' AND src.listing_role IN ('listing','adjacent')) AS publications,
    (SELECT json_group_array(DISTINCT src.publisher_entity_id) FROM sighting s JOIN source src USING(source_id)
       WHERE s.indicator_id=i.indicator_id AND s.role='ioc' AND src.listing_role IN ('listing','adjacent')) AS publishers,
    (SELECT json_group_array(DISTINCT src.listing_role) FROM sighting s JOIN source src USING(source_id)
       WHERE s.indicator_id=i.indicator_id AND s.role='ioc' AND src.listing_role IN ('listing','adjacent')) AS listing_roles,
    (SELECT MIN(COALESCE(r.published_at, s.source_first_seen)) FROM sighting s JOIN report r ON r.report_id=s.report_id
       WHERE s.indicator_id=i.indicator_id AND s.role='ioc') AS first_published_at,
    i.first_listed_at, i.site_bucket, i.site_reason, i.site_reach, i.site_flag, i.bucket_since, i.bucket_streak,
    i.last_checked_at, i.last_live_at, i.next_check_at, i.registry_status, i.registration_expires_at, i.status
  FROM v_site i;
"""

def migrate(con):
    for tbl, cols in MIGRATIONS.items():
        have = {r[1] for r in con.execute(f"PRAGMA table_info({tbl})")}
        for name, decl in cols:
            if name not in have: con.execute(f"ALTER TABLE {tbl} ADD COLUMN {name} {decl}")
    con.executescript(SITE_DDL); con.commit()

def cols(con, tbl): return [r[1] for r in con.execute(f"PRAGMA table_info({tbl})")]
