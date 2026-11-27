#!/usr/bin/env python3
"""Parse gov.sg Trusted Sites page tables -> rows json; diff with mirror allowlist."""
import re, html, json, sys
from urllib.parse import urlparse
page, allow, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(page, encoding='utf-8', errors='replace').read()
def txt(x): return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', x)).replace('(opens in new tab)', '').split())
tok = re.finditer(r'<h2[^>]*>(.*?)</h2>|<p[^>]*>(Table \d+:[^<]*)</p>|<tr[^>]*>(.*?)</tr>', s, re.S)
sec = cap = None; rows = []
for m in tok:
    if m.group(1) is not None: sec = txt(m.group(1))
    elif m.group(2) is not None: cap = txt(m.group(2))
    else:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', m.group(3), re.S)
        hrefs = re.findall(r'href="([^"]+)"', m.group(3))
        vals = [txt(c) for c in cells]
        if vals and vals[0] == 'Website Name': continue
        rows.append({'section': sec, 'table': cap, 'name': vals[0] if vals else '', 'url': hrefs[0] if hrefs else (vals[1] if len(vals) > 1 else '')})
def host(u):
    u = u.strip()
    if '://' not in u: u = 'http://' + u
    return urlparse(u).hostname.lower()
for r in rows: r['host'] = host(r['url'])
# short-link bullets
for name, h in (('Go.gov.sg short link for official Government websites', 'go.gov.sg'),
                ('For.sg short link for healthcare institution websites', 'for.sg'),
                ('For.edu.sg short link for education institution websites', 'for.edu.sg')):
    if ('http://' + h).lower() in s.lower() or h in s.lower():
        rows.append({'section': 'How to Verify an Official Government Website', 'table': 'short-link bullets', 'name': name, 'url': 'http://' + h, 'host': h})
m = re.search(r'Last updated on [0-9]{1,2} [A-Za-z]+ [0-9]{4}', txt(s))
al = [l.strip().lower() for l in open(allow) if l.strip()]
reg = lambda h: h[4:] if h.startswith('www.') else h
page_regs = set(reg(r['host']) for r in rows)
res = {'last_updated': m.group(0) if m else None, 'rows': rows,
       'mirror_count': len(al), 'mirror_not_on_page': sorted(set(al) - page_regs),
       'page_not_in_mirror': sorted(page_regs - set(al))}
json.dump(res, open(out, 'w'), indent=1)
from collections import Counter
print(res['last_updated'], len(rows), 'rows', Counter(r['table'] for r in rows))
print('mirror', len(al), 'mirror_not_on_page', res['mirror_not_on_page'], 'page_not_in_mirror', res['page_not_in_mirror'])
