#!/usr/bin/env python3
# usage: tx.py FILE [regex [width]] -> visible text (stdlib). With regex: print context snippets.
import sys,re,html
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
s=re.sub(r'(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>',' ',s)
s=re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>|</tr>|</td>|</dt>|</dd>|</a>','\n',s)
s=re.sub(r'(?i)<a\s[^>]*href="([^"#][^"]*)"[^>]*>',r' [\1] ',s) if '-l' in sys.argv else s
t=html.unescape(re.sub(r'<[^>]+>',' ',s))
t=re.sub(r'[ \t\r\f\v\xa0]+',' ',t); t='\n'.join(l.strip() for l in t.split('\n') if l.strip())
args=[a for a in sys.argv[2:] if a!='-l']
if not args: print(t)
else:
    pat=args[0]; w=int(args[1]) if len(args)>1 else 150; seen=set()
    for m in re.finditer(pat,t,re.I):
        sn=t[max(0,m.start()-w):m.end()+w].replace('\n',' | ')
        k=sn[:60]
        if k in seen: continue
        seen.add(k); print('..',sn)
