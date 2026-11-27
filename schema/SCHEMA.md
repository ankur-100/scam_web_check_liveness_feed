# SG Scam Intelligence: canonical schema (draft v0.1, 2026-11-26)

Machine-readable definition: `sg_scam_intel.schema.json` (JSON Schema 2020-12).
Fit-test against real data: `build_examples.py` → `examples/*.json` (inputs in `../data/fixtures/`).
Status: **draft for discussion.** The pipeline design (storage, scheduling, checker deployment, feed transport)
has not been decided. This document fixes *what* the records mean, not *how* they are produced.

---

## 1. Design goals

1. **One model for very different sources.** SPF advisories (reports carrying domains), the MAS Investor Alert List
   (listings of entities with websites, phones and emails), open phishing feeds (bare URLs with a status), and
   narrative-only sources (CSA RSS, police.gov.sg news).
2. **Lifecycle that no source provides.** No SG source carries `active` / `expires`. The schema keeps three time
   axes apart and derives status from them (§4):
   - *what the source claims* (published, modified, listed, delisted)
   - *what we ingested* (first/last seen by us)
   - *what we observed* (DNS / RDAP / HTTP liveness)
3. **Three different entity roles.** The **issuer** (who warned, e.g. SPF, MAS), the **impersonated** entity
   (e.g. LTA) and the **fictitious brand** (a scam platform name). SPF's `Brand` tag mixes the last two.
4. **Provenance.** Every indicator traces to sightings, and each sighting to its source, its report and the raw record hash.
5. **Safe blocking.** Shared platforms (pages.dev, blogspot) and compromised legitimate sites must never be blocked
   at the registrable domain. `block_scope` records the narrowest safe level.
6. **A pollable output.** A monotonic change log (`feed_event.seq`) that consumers read with `since=<seq>`.
   Exports to STIX 2.1 and MISP (§9).

## 2. Record types

```
                 publishes                     asserts (role=ioc|official|mention_benign)
   entity ───────────────────► source ◄──────────────── sighting ──────────────► indicator
     ▲  ▲                         │ yields                  │ (optional)              │  ▲
     │  │ impersonated /          ▼                         ▼                         │  │ observed by
     │  └── fictitious ───────  report ──── extracts ───────────────────────────────►─┘  │
     │       (via brand map)      │ issuer_entity_id                                     liveness_check
     └────────────────────────────┘                                                    (append-only)
   indicator/report/entity changes ──► feed_event (seq cursor, denormalised snapshot)
```

| Record | Identity | Mutability | One per… |
|---|---|---|---|
| `entity` | `entity_id` = primary official registrable domain (`lta.gov.sg`); `<domain>#<slug>` for a programme without its own domain; `brand:<slug>` fictitious; `placeholder:<slug>` | slowly changing (registry) | organisation / scam brand |
| `source` | `source_id` slug (`spf-icanact`) | config | feed we poll |
| `report` | `<source_id>:<native_id>` | updated when source modifies; `withdrawn` if it vanishes | advisory / listing / news item |
| `indicator` | `ind_` + sha1(`type:normalised_value`)[:16] | **derived**, recomputed | observable (domain, URL, phone…) |
| `sighting` | `sig_` + sha1(`source|report|indicator`)[:16] | updated on re-ingest; `removed_at` on disappearance | (source, report, indicator) triple |
| `liveness_check` | `check_id` | **immutable** | each check run |
| `feed_event` | `seq` (monotonic int) | immutable | each change emitted |

## 3. Normalisation & identity rules

| Type | Normalised `value` | Notes |
|---|---|---|
| `domain` | lowercase IDNA (punycode) host where host == registrable domain (PSL **incl. private section**) | `drbypass-proxy.pages.dev` is a *domain* because `pages.dev` is a PSL private suffix |
| `hostname` | lowercase IDNA host with labels above the registrable domain, `www.` stripped | `iras.nakadaniko.com.sg` |
| `url` | `scheme://host/path?query`, host normalised, fragment dropped | kit paths matter (`/bank/dbs/…`) |
| `phone` | E.164 (`phonenumbers`, default region SG) | MAS `phonenumber_s` is free text: split on `;,/\n` |
| `email` | lowercase | |
| `entity_name` | lowercase, trimmed; split MAS name fields on `,;/` and drop parts that are domains | |
| `sms_sender_id`, `app_package`, `social_handle`, `bank_account`, `crypto_address` | as published | reserved; no current source populates them except official channels |

`host` block:
- `registrable_domain` is the PSL eTLD+1 with private suffixes.
- `is_shared_platform` = PSL-private suffix OR on a curated list. `blogspot.sg` is **not** in the PSL; keep a
  curated list: blogspot.*, pages.dev, edgeone.dev, wpenginepowered.com, github.io, netlify.app, vercel.app,
  web.app, firebaseapp.com, weebly.com, wixsite.com…
- `block_scope` = `registrable_domain` only when the host *is* the registrable domain and not a platform. Otherwise
  `hostname`, or `url` for kit paths on legitimate hosts.
- `is_compromised_legit` = a brand label on an unrelated legitimate domain (subdomain abuse). Needs evidence, so it is
  null by default.

`lookalike_of[]` relates an indicator to an `entity` with a `method`:
- `brand_token`: brand in the registrable label.
- `subdomain_abuse`: brand only in a subdomain label (`iras.nakadaniko.com.sg`).
- `path_kit`: e.g. `/bank/dbs/`.
- `service_token`: onemotoring, erp, paynow, cdc, sgac…
- `levenshtein` / `homoglyph`: for later.

Official domains from the registry make a value **allowlisted** (§4), so it is never emitted as an IOC.

## 4. Lifecycle and status rules

### 4.1 Source lifecycle semantics (`source.lifecycle_semantics`)
| Semantics | Example | Presence in a poll means… | `sighting.source_last_seen` = |
|---|---|---|---|
| `snapshot_full` | SPF icanact, MAS IAL | the source **still lists it**. This says nothing about whether the site is up. SPF never removes advisories. | the record's `modified_at` (source's last assertion), **not** our poll time |
| `active_list` | Phishing.Database ACTIVE | the source re-tested it and believes it **is live now** | our poll time while present; `removed_at` when it drops off |
| `event_stream` | PhishStats | per-item `date` / `date_update` | source's `date_update` |
| `append_only` | CSA RSS | item exists | item date |

So re-ingesting an unchanged SPF advisory **does not** refresh `last_seen`. Otherwise every SPF domain would stay
"fresh" forever.

### 4.2 Indicator times
- `first_seen` = min over sightings of (`source_first_seen` ?? `first_ingested_at`).
- `last_seen` = max over sightings of (`source_last_seen` ?? (our poll time, but only for `active_list` and still present) ?? `source_first_seen`).
- `first_reported_at` = earliest authoritative report `published_at`.
- `valid_until` = max(`last_seen`, `liveness.last_live_at`) + **TTL(type)**: url 30d · hostname/domain 90d ·
  ip 14d · phone/email 180d · entity_name 365d (policy parameters, to be agreed).

### 4.3 Liveness verdict (one `liveness_check`)
| Evidence | Verdict |
|---|---|
| DNS NXDOMAIN, or RDAP status contains `clientHold` / `serverHold` | `dead` (fingerprint `registrar_hold` when held) |
| DNS answer **and** host is a shared platform (wildcard DNS) with no HTTP evidence | `inconclusive` |
| DNS answer, HTTP 2xx/3xx serving content, no parking/takedown fingerprint | `live` |
| parking page / sinkhole NS or IP / hosting "suspended" page / ISP block page / browser phishing interstitial | `parked` / `sinkholed` / `suspended` / `blocked` |
| redirect to the impersonated entity's official site | `redirect_benign` |
| DNS TIMEOUT or SERVFAIL alone | `inconclusive`. **A timeout proves nothing.** On this VM held domains time out instead of returning NXDOMAIN. |
| type not checkable (phone, email, entity_name) | `not_applicable` |

### 4.4 Derived `indicator.status`
```
allowlisted   value or registrable domain ∈ official domains/hosts of an entity        (never on the IOC feed)
revoked       the authoritative source withdrew it (report withdrawn / MAS delisting) or it is a false positive
active        liveness = live      | uncheckable type and now ≤ valid_until
inactive      liveness ∈ {dead, parked, suspended, sinkholed, blocked} and the registration has not lapsed
              (status_reason e.g. "registrar hold (takedown)")
expired       registration lapsed (> RDAP expires_at + 45d grace) | never/inconclusively checked and now > valid_until
unverified    never/inconclusively checked and now ≤ valid_until
```
`inactive` = **we know it is down**. `expired` = **we have no current evidence**. A re-registration after the
domain drops (new RDAP `registered_at`) should start a new lifecycle (open question Q5).

### 4.5 Real observations from the fit-test (2026-11-25/26)
- `feevr.top`, `feekt.top` (SPF LTA advisory, July 2026): RDAP `client hold`, registration expires 2027-06-30 /
  2027-07-01. Status **inactive (registrar hold)**: the "taken down" marker SPF's feed lacks.
- `drbypass-proxy.pages.dev` (SPF, 2026-11-24): resolves to Cloudflare, but pages.dev is a platform, so the verdict
  is **inconclusive** until an HTTP or content check.
- `iras.nakadaniko.com.sg`: subdomain abuse on a probably-compromised SG small business, so `block_scope=hostname`.
  Never checked, last SPF assertion 2026-04, so **expired**.
- A WP Engine random label resolves (wildcard DNS confirmed). Direct DNS to 1.1.1.1 is blocked on this VM, so the system resolver is used.

## 5. Category taxonomy (v0.1)
| Code | From SPF `Scam Category` | Other sources |
|---|---|---|
| `investment` | Investment | |
| `job` | Job | |
| `phishing.banking` | Banking Related Phishing | bank kit URLs from open feeds (`/bank/dbs/`) |
| `phishing.non_banking` | Non-Banking Related Phishing | |
| `phishing.unspecified` | Phishing (legacy value) | generic open-feed phishing |
| `impersonation.government` | Impersonation, when an impersonated entity is `gov.*` | |
| `impersonation.other` | Impersonation, otherwise | |
| `ecommerce` / `malware` / `loan` / `visa` | same names | |
| `unlicensed_financial` | n/a | MAS Investor Alert List |
| `romance`, `fake_friend_call`, `tech_support`, `crypto`, `other` | reserved, to align with SPF annual-statistics scam types (verify exact list) | |

Always keep `categories_raw` verbatim.

## 6. Feed contract (`feed_event`)
Consumers poll `GET …/events?since=<seq>`. Each event:
`{seq, emitted_at, op: upsert|status_change|revoke|delete, object_type, object_id, version, changed_fields, previous_status, snapshot}`.
The indicator `snapshot` is denormalised for direct use:
```json
{"indicator_id","type","value","value_defanged","registrable_domain","block_scope",
 "status","status_reason","first_seen","last_seen","valid_until","confidence","categories",
 "impersonated_entity_ids","issuer_entity_ids","report_ids","tlp",
 "liveness":{"state","last_checked_at","last_live_at","registration_expires_at"}}
```
Events are emitted when status, valid_until, liveness.state, the impersonation set or confidence change, and not
for every re-ingest. Allowlisted indicators are never emitted on the IOC stream.

## 7. Source mappings

| Source | → report | → indicators (role) | times | notes |
|---|---|---|---|---|
| **SPF icanact** (`spf-icanact`) | one per advisory; issuer `police.gov.sg`; categories via §5; `brand_tags_raw` → `impersonated_entity_ids` / `fictitious_brand_ids` via `registry/spf_brand_map.json` | `scam_site_urls` (string JSON) → domain/hostname/url (`ioc`) | published=`date_created`, modified=`date_updated` | snapshot_full; images → `media` |
| **MAS IAL** (`mas-ial-opensanctions` or MAS raw) | one per listing; issuer `mas.gov.sg`; `unlicensed_financial` | name(s) → `entity_name`; `website_s` free text → domains/urls; `phonenumber_s` → E.164; `email_s` → email (all `ioc`) | listed=`date_dt`, modified=`modifieddate_dt`; OpenSanctions adds first_seen/last_seen | delisting (record vanishes / OpenSanctions `last_seen` stops) → `revoked` |
| **Phishing.Database ACTIVE** (`phishdb-links-active`) | none | URL (`ioc`) after SG filter | none from source; our poll times | active_list; drop-off → `removed_at` |
| **PhishStats** (`phishstats-api`) | none | URL (`ioc`); keep asn/isp/score in `raw` | `date`, `date_update`; `http_code` → `source_status` | event_stream; 50 req/day anon |
| **CSA advisories RSS**, **police.gov.sg** news | one per item | text-extracted indicators need **role classification**: advice text quotes genuine domains ("SPF sites end with .gov.sg") → `mention_benign` | pubDate | append_only |
| **Registry** (`registry/entities_*.json`) | none | `official.domains/hosts/sms_sender_ids/hotlines` → `official` sightings (allowlist) | verified_at | drives allowlisting + lookalike matching |

## 8. Confidence (v0.1 heuristic)
Base by `source.authority`: authoritative / regulator 90 · industry 75 · commercial 70 · community 60 · academic 50.
+5 per additional independent source (cap 100). Liveness does **not** change confidence: confidence is about
"malicious", status is about "currently operating".

## 9. Interoperability
| Ours | STIX 2.1 | MISP |
|---|---|---|
| entity (organisation) | `identity` (identity_class=organization, sectors) | org / galaxy cluster |
| entity (fictitious brand) | `campaign` (name) or `x-sg-scam-brand` | galaxy cluster |
| report | `report` (+ `external_references` to the advisory URL) | event (info=title, date=published) |
| indicator | `indicator` (`pattern` `[domain-name:value = '…']`, `valid_from`=first_seen, `valid_until`, `revoked`, `confidence`) | attribute (domain/url/phone-number/email-src, `first_seen`/`last_seen`, `to_ids` = status∈{active,unverified}) |
| impersonation | `relationship` campaign `impersonates` identity | tag / galaxy relation |
| sighting | `sighting` (first_seen, last_seen, count, where_sighted_refs = source identity) | sighting |
| liveness | (`observed-data` / custom) | `phishing` object `online` yes/no, `takedown-time` |
| TLP | `marking-definition` TLP:CLEAR | `tlp:clear` tag |

## 10. Open questions for the design discussion
1. **TTLs and the 45-day post-expiry grace** (§4.2, §4.4): agree on the values per type.
2. **Checker vantage**: an SG vantage point (residential/cloud) to see SG ISP block pages and geo-fenced kits, versus this
   Azure VM. Which resolver (own recursive resolver vs cloud DNS)? TIMEOUTs on held domains argue for our own resolver.
3. **HTTP checks on scam hosts**: allowed, and from where? DNS + RDAP alone can't settle shared platforms.
   Needs a policy (no rendering, HEAD/GET root only, isolated egress?).
4. **Allowlist authority**: registry entities are curated by hand. Who approves additions?
5. **Re-registration**: same indicator with a new lifecycle, or a new `indicator_id` scoped by `registered_at`?
6. **Text-extracted indicators** from narrative sources: rules vs LLM (local Gemma/Ollama per cost preference) for role classification.
7. **Licences**: MAS via OpenSanctions is CC-BY-NC, and the SPF site's terms are unchecked. Can the aggregated feed be
   redistributed, and does TLP:CLEAR fit?
8. **Feed transport**: HTTP NDJSON change log vs TAXII 2.1 collection vs MISP feed format (or all, generated from `feed_event`).
