# Sub-agent brief: SG private-sector entity registry (shared by all groups)

You are building part of a registry of Singapore organisations -> their official domains/subdomains -> every page
where they publish scam/security-alert information. It feeds a Singapore scam-intelligence pipeline: official domains
become an ALLOWLIST for detecting lookalikes; scam-alert pages become SOURCES. Today is 2026-11-25.

## Step 0
Read `/home/ankur/scamtrends_feed/registry/FORMAT.md` (section 1 "Entity record" and "Ground rules") and follow it
strictly. Skim `/home/ankur/scamtrends_feed/sources/03_community_commercial.md` (earlier survey; reuse its facts, but
re-open any page before citing it). If the Read/Write tools time out (hook issue), use Bash (cat, heredoc, python).

## Output
Write a JSON ARRAY of entity records to your output path (rewrite it after each entity so partial work survives).
Validate: `python3 /tmp/claude-1003/-home-ankur/d6fae8d2-b05b-46ce-92ff-521ba4485ee2/scratchpad/registry_work/private/validate.py <your output>`
until it prints "0 problems". Raw downloads go in your group's scratch subfolder.

## Per-entity method (light volume: <=15 requests per site, >=1 s between requests to the same host)
1. Fetch homepage + robots.txt with curl and a normal browser UA:
   UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
   curl -sL -A "$UA" --max-time 30 -o FILE -w '%{http_code} %{url_effective}\n' URL
2. Sitemaps: from robots `Sitemap:` lines (else try /sitemap.xml once). Grep URLs for
   `scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect`. <=10 sitemap files per site.
3. WebSearch, e.g. `site:<domain> scam`, `<brand> Singapore official SMS sender ID`, `<brand> Singapore scam alert`,
   `<brand> official websites list`.
4. Open each candidate page (curl; if JS-rendered and curl gets only a shell, WebFetch once). Record: what it is,
   number of dated items, newest date, whether it lists CONCRETE indicators (fake domains/URLs, phone numbers, emails,
   sender IDs, apps, social handles, bank accounts) vs narrative only, and one short verbatim sample (<=200 chars).
5. Collect allowlist facts from the entity's OWN pages: official domains ("our official websites are..."),
   login/payment hosts seen in links (e.g. internet-banking.x.com.sg), SMS sender IDs / short codes, hotlines (esp.
   anti-scam/fraud hotlines), official app names (as in app-store links on the site), social accounts linked from the
   site footer, official email sender domains/addresses, short-link domains.

## Field rules
- entity_id: primary official registrable domain (eTLD+1), lowercase, no www (e.g. `dbs.com.sg`, `sc.com`, `grab.com`).
  If the SG business lives under a path of a global domain (e.g. sc.com/sg, dhl.com/sg-en, moomoo.com/sg) the
  entity_id is still that registrable domain; country "SG"; say so in notes.
  Sub-brand with its OWN registrable domain AND its own scam/security pages -> separate record with parent_entity_id
  (e.g. POSB posb.com.sg -> parent dbs.com.sg). Otherwise fold it into aliases. A product without its own domain gets a
  `<parent>#<slug>` record only if it has dedicated scam/security pages; otherwise it is just an alias.
- aliases: common names/abbreviations AND the exact SPF brand-tag strings given for your group (e.g. "Ninjavan",
  "DBS PayLah", "MooMoo", "SPX") so a mechanical brand map can join on them.
- sector: exactly one value from FORMAT.md. parent_entity_id: registrable domain of the parent if relevant, else null.
- official_domains: ONLY registrable domains (eTLD+1; no www, no paths) confirmed on the entity's OWN pages, either
  (a) explicitly stated as official, or (b) the domain serving the official site, or a login/app/payment host linked
  from the official site's own navigation. Say in notes which are (a) vs (b). Never add a domain from memory or from a
  third-party page. If an official page lists third-party/partner hosts as legitimate (e.g. a qualtrics.com survey
  host), put the exact FQDN in official_hosts, NOT the third party's registrable domain in official_domains; explain
  in notes.
- official_hosts: notable FQDNs seen in official links (login, internet banking, payment, tracking, help centre),
  e.g. internet-banking.dbs.com.sg. Only hosts you actually saw.
- scam_info: one object per useful page (aim 2-6 per Tier-1 entity, 1-2 per Tier-2): scam hub, latest-scams/alerts
  list, official-channels/sender-ID page, fake-indicator lists, report-fraud page. Keys EXACTLY:
  url, kind, lists_indicators, access, machine_url, item_count, latest_item_date, verified, sample, notes.
  * kind: advisory_feed (dated list of alerts) | alert_page (single alert/notice) | scam_faq (generic guidance hub)
    | official_channels (the entity's genuine domains/numbers/sender IDs) | fake_indicator_list (lists fake
    domains/numbers/apps/accounts) | news_releases (press releases; also media "scams" topic pages) | report_portal
    | statistics.
  * lists_indicators: types of CONCRETE identifiers on the page, from: domain, url, phone, email, sms_sender_id, app,
    social_handle, bank_account, entity_name. [] = narrative only. For kind=official_channels these are the types of
    GENUINE identifiers listed; for every other kind they are SCAM indicators (don't count the entity's own hotline as
    "phone" on an alert page). Write "(official)" or "(fake)" in notes when ambiguous.
  * access: html | rss | atom | sitemap | json_api_documented | csv | pdf. machine_url: RSS/Atom/sitemap/CSV/PDF URL
    that lets a machine discover or read the page (e.g. the sitemap file containing it), else null.
  * item_count: integer count of dated alerts/items on the page (null if not a list).
    latest_item_date: ISO YYYY-MM-DD (or YYYY-MM) of the newest item; null if undated.
  * verified: "2026-11-25 HTTP <status>" from your own fetch (append " via WebFetch" if that is how you read it).
  * sample: short verbatim excerpt (<=200 chars) or an example indicator exactly as printed.
- official_channels: {"sms_sender_ids":[], "hotlines":[], "short_link_domains":[], "social":[], "apps":[], "emails":[]}
  (`apps` and `emails` are an agreed extension; keep them, [] if unknown).
  sender IDs exactly as stated (e.g. "DBS", "72339"); hotlines "<number as printed> (<label>)", e.g.
  "1800 339 6963 (DBS anti-scam hotline)"; social = full URLs exactly as linked from the official site; apps =
  "<App name> (<store/platform info if shown>)"; emails = addresses or "@domain" as stated.
- evidence: URLs you opened that support official_domains / official_channels. Every factual claim must trace to a URL
  you actually opened, not a search snippet. Search-snippet facts may appear only in notes, labelled
  "unverified (search snippet)".
- notes: what a pipeline engineer needs (JS-rendered page read via WebFetch, SG content under a path, etc.).
- Unknown -> null or []. NEVER invent.

Example (shape only, values illustrative):
{"entity_id":"example.com.sg","name":"Example Bank Singapore","abbr":null,"aliases":["Example"],"sector":"bank",
 "parent_entity_id":null,"country":"SG","official_domains":["example.com.sg","example.com"],
 "official_hosts":["www.example.com.sg","ibanking.example.com.sg"],
 "scam_info":[{"url":"https://www.example.com.sg/security/alerts","kind":"advisory_feed","lists_indicators":[],
   "access":"html","machine_url":"https://www.example.com.sg/sitemap.xml","item_count":12,
   "latest_item_date":"2026-10-02","verified":"2026-11-25 HTTP 200",
   "sample":"Beware of phishing SMSes asking you to ...","notes":"narrative only"}],
 "official_channels":{"sms_sender_ids":["EXAMPLE"],"hotlines":["1800 123 4567 (fraud hotline)"],
   "short_link_domains":[],"social":["https://www.facebook.com/example"],"apps":["Example SG (iOS/Android)"],
   "emails":["@example.com.sg"]},
 "evidence":["https://www.example.com.sg/security/official-channels"],"notes":""}

## Ground rules (mandatory, from FORMAT.md)
- Official sites only. NEVER visit a scam/fake/lookalike domain, even one named on an official page - record it as
  text only.
- Only public user-facing pages, robots.txt, sitemaps, RSS/Atom, published downloads, documented APIs, web search.
  Do NOT call undocumented backend/CMS/API endpoints (e.g. /api/..., help-centre JSON APIs behind SPAs, GraphQL), do
  not brute-force or guess paths, do not log in or register. Data embedded in a normal page's HTML (__NEXT_DATA__,
  JSON-LD, a JSON component blob) is fine.
- Respect robots.txt Disallow rules.
- Bot protection: if a site returns a challenge or WAF block (Cloudflare "Just a moment", Akamai/Imperva/Radware/
  PerimeterX captcha or JS challenge, WAF 403), you may try WebFetch on the same URL ONCE. If that is also blocked,
  STOP for that site: no archives/caches (web.archive.org, Google cache), no headless browsers, no proxies, no header
  tricks. Record "blocked: <host> <how>" in the entity notes and in your report. You may still add a scam_info entry
  for a blocked page found via search, with verified "2026-11-25 HTTP 403 (bot protection; not bypassed)" and
  null/[] for details you could not see.
- Budget: <=25 tool calls per Tier-1 entity, <=8 per Tier-2 entity.

## Hand-back
Call SubagentHandback with <=250 words: entity_ids written; which publish concrete FAKE indicators (types, rough
counts); which publish explicit official-domain / sender-ID / hotline lists; machine-readable endpoints
(RSS/sitemap/JSON); anything blocked or skipped.