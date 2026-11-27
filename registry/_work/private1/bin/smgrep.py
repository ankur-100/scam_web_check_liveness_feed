#!/usr/bin/env python3
# usage: smgrep.py FILE [extra_regex] -> URLs (with lastmod) matching scam keywords; also lists child sitemaps
import sys,re
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
pat=re.compile(r'scam|fraud|phish|secur|impersonat|fake|beware|official|sender|vigilant|alert|protect|advisor|kill-switch|money-lock'+('|'+sys.argv[2] if len(sys.argv)>2 else ''),re.I)
if '<sitemapindex' in s: print('INDEX:',re.findall(r'<loc>\s*([^<\s]+)',s)[:60])
n=0
for m in re.finditer(r'<url>(.*?)</url>',s,re.S):
    n+=1; b=m.group(1); loc=re.search(r'<loc>\s*([^<\s]+)',b); lm=re.search(r'<lastmod>([^<]+)',b)
    if loc and pat.search(loc.group(1)): print((lm.group(1)[:10] if lm else '-'),loc.group(1))
print('TOTAL urls',n)
