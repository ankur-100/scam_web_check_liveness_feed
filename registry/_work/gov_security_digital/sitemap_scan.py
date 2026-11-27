#!/usr/bin/env python3
"""Light, polite robots.txt -> sitemap(s) -> keyword grep for a list of official hosts.
Only fetches robots.txt, the sitemaps it declares (or /sitemap.xml as the
conventional fallback), and nested sitemap indexes. No other paths."""
import gzip, json, os, re, subprocess, sys, time
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
KW = re.compile(r'scam|fraud|phish|impersonat|fake|hoax|spoof|beware|advisor|alert|unsolicited|cyber', re.I)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scan')
os.makedirs(OUT, exist_ok=True)
MAX_SITEMAPS = int(os.environ.get('MAX_SITEMAPS', '60'))

def fetch(url, timeout=40):
    p = subprocess.run(['curl', '-sS', '-L', '--max-redirs', '5', '-A', UA, '-m', str(timeout), '--compressed',
                        '-w', '\n__META__%{http_code} %{url_effective} %{content_type}', url], capture_output=True)
    raw = p.stdout; idx = raw.rfind(b'\n__META__'); time.sleep(1.0)
    if idx < 0: return 0, url, b'', p.stderr.decode('utf-8', 'replace')[:200]
    meta = raw[idx + 9:].decode('utf-8', 'replace').split(' ', 2)
    return (int(meta[0]) if meta[0].isdigit() else 0), (meta[1] if len(meta) > 1 else url), raw[:idx], (meta[2] if len(meta) > 2 else '')

def parse_sitemap(b):
    if b[:2] == b'\x1f\x8b':
        try: b = gzip.decompress(b)
        except Exception: pass
    txt = b.decode('utf-8', 'replace')
    entries = []
    for m in re.finditer(r'<(url|sitemap)\b[^>]*>(.*?)</\1>', txt, re.S):
        loc = re.search(r'<loc>\s*(.*?)\s*</loc>', m.group(2), re.S); lm = re.search(r'<lastmod>\s*(.*?)\s*</lastmod>', m.group(2), re.S)
        if loc:
            u = loc.group(1).replace('&amp;', '&').strip()
            if u.startswith('<![CDATA['): u = u[9:-3]
            entries.append((u, lm.group(1).strip() if lm else None))
    return '<sitemapindex' in txt, entries

def scan(host):
    res = {'host': host, 'robots': None, 'robots_status': None, 'sitemaps_declared': [], 'sitemaps_fetched': [], 'n_urls': 0, 'hits': [], 'newest_lastmod': None}
    code, final, body, _ = fetch(f'https://{host}/robots.txt')
    res['robots_status'] = code
    if code == 200:
        res['robots'] = body.decode('utf-8', 'replace')[:4000]
        res['sitemaps_declared'] = re.findall(r'(?im)^\s*sitemap:\s*(\S+)', res['robots'])
    queue = list(res['sitemaps_declared']) or [f'https://{host}/sitemap.xml']
    urls = {}; seen = set()
    while queue and len(seen) < MAX_SITEMAPS:
        sm = queue.pop(0)
        if sm in seen: continue
        seen.add(sm)
        c, f, b, ct = fetch(sm)
        n = 0
        if c == 200:
            is_idx, ents = parse_sitemap(b)
            for u, lm in ents:
                if is_idx: queue.append(u)
                else: urls[u] = lm; n += 1
        res['sitemaps_fetched'].append(f'{sm}[{c}:{n if c==200 else "-"}]')
    res['n_urls'] = len(urls)
    res['hits'] = sorted([(u, lm) for u, lm in urls.items() if KW.search(u)], key=lambda t: t[1] or '')
    lms = [lm for lm in urls.values() if lm]
    res['newest_lastmod'] = max(lms) if lms else None
    json.dump(res, open(os.path.join(OUT, host + '.json'), 'w'), indent=1)
    json.dump(urls, open(os.path.join(OUT, host + '.urls.json'), 'w'))
    print(f"== {host}: robots={code} declared={len(res['sitemaps_declared'])} fetched={len(seen)} urls={len(urls)} hits={len(res['hits'])} newest_lastmod={res['newest_lastmod']}")
    print('   sitemaps:', ', '.join(res['sitemaps_fetched'])); sys.stdout.flush()

if __name__ == '__main__':
    for h in sys.argv[1:]:
        try: scan(h)
        except Exception as e: print('ERR', h, e)
