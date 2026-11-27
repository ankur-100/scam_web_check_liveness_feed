#!/usr/bin/env python3
"""Fetch a public page; print status, title, date hints, rel=alternate feeds, and visible text."""
import re, subprocess, sys, html, time, json, hashlib, os
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')
os.makedirs(CACHE, exist_ok=True)
def cpath(url): return os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + '.html')
def get(url, timeout=40):
    p = subprocess.run(['curl', '-sS', '-L', '--max-redirs', '5', '-A', UA, '-m', str(timeout), '--compressed',
                        '-w', '\n__META__%{http_code} %{url_effective}', url], capture_output=True)
    raw = p.stdout; i = raw.rfind(b'\n__META__')
    meta = raw[i+9:].decode().split(' ', 1) if i >= 0 else ['0', url]
    body = raw[:i] if i >= 0 else b''
    open(cpath(url), 'wb').write(body)
    open(cpath(url) + '.meta', 'w').write(' '.join(meta))
    time.sleep(0.8)
    return int(meta[0]) if meta[0].isdigit() else 0, meta[1] if len(meta) > 1 else url, body.decode('utf-8', 'replace')
def cached(url):
    return open(cpath(url), encoding='utf-8', errors='replace').read()
def cfdecode(e):
    k = int(e[:2], 16); return ''.join(chr(int(e[i:i+2], 16) ^ k) for i in range(2, len(e), 2))
def text_of(h):
    h = re.sub(r'(?is)<(script|style|noscript|svg|head)\b.*?</\1>', ' ', h)
    h = re.sub(r'(?is)<(nav|footer)\b.*?</\1>', ' ', h)
    h = re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>|</div>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    t = re.sub(r'[ \t\r\f\v]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()
if __name__ == '__main__':
    maxc = int(os.environ.get('MAXC', '3000'))
    for url in sys.argv[1:]:
        code, final, h = get(url)
        title = re.search(r'(?is)<title[^>]*>(.*?)</title>', h)
        print('=' * 100); print('URL:', url); print('STATUS:', code, 'FINAL:', final)
        print('TITLE:', html.unescape(title.group(1).strip())[:200] if title else None)
        for m in re.findall(r'(?is)<link[^>]+rel=["\']alternate["\'][^>]*>', h)[:6]: print('ALT:', m[:250])
        for m in re.findall(r'(?is)<meta[^>]+(?:published|modified|date|og:updated)[^>]*>', h)[:6]: print('META:', m[:200])
        for m in re.findall(r'"date(?:Published|Modified)"\s*:\s*"([^"]+)"', h)[:4]: print('JSONLD date:', m)
        for e in sorted(set(re.findall(r'data-cfemail="([0-9a-f]+)"', h))): print('CFEMAIL:', cfdecode(e))
        t = text_of(h)
        print('TEXTLEN:', len(t)); print(t[:maxc])
