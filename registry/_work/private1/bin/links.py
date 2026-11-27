#!/usr/bin/env python3
# usage: links.py FILE... -> hosts count, social, app-store, tel/mailto, scam-ish links
import sys,re,html
from urllib.parse import urlparse
hosts={};soc=set();apps=set();tel=set();sc=set()
for fn in sys.argv[1:]:
    s=html.unescape(open(fn,encoding='utf-8',errors='replace').read()).replace('\\/','/')
    for u in re.findall(r'https?://[^\s"\'<>\\)]+',s):
        
        try: h=(urlparse(u).hostname or "").lower()
        except ValueError: continue
        hosts[h]=hosts.get(h,0)+1
        if re.search(r'(facebook|instagram|twitter|x|linkedin|youtube|tiktok|t|telegram)\.(com|me)/',u) and not re.search(r'sharer|share\?|intent/tweet|plugins|/tr\?|dialog',u): soc.add(u.rstrip('/'))
        if re.search(r'apps\.apple\.com|itunes\.apple\.com|play\.google\.com/store|appgallery\.huawei',u): apps.add(u)
    for u in re.findall(r'(?:tel|mailto):[^"\'<> ]+',s): tel.add(u)
    for u in re.findall(r'href="([^"]+)"',s):
        if re.search(r'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect|safety|advisor|kill',u,re.I): sc.add(u)
print('HOSTS:',' '.join(f'{h}:{c}' for h,c in sorted(hosts.items(),key=lambda x:-x[1]) if h)[:2500])
print('SOCIAL:',sorted(soc)[:30]); print('APPS:',sorted(apps)[:12]); print('TEL/MAIL:',sorted(tel)[:20]); print('SCAMLINKS:',sorted(sc)[:60])
