# usage: python3 -I tx.py FILE [start_kw] [nchars]  -> visible text
import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>',' ',s)
t=html.unescape(re.sub(r'(?s)<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
kw=sys.argv[2] if len(sys.argv)>2 and sys.argv[2] else None
n=int(sys.argv[3]) if len(sys.argv)>3 else 3000
i=t.find(kw) if kw else 0
if i<0: i=0
print(f'[len={len(t)} start={i}]', t[i:i+n])
