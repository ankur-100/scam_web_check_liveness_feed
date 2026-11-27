# usage: python3 -I links.py FILE [regex]  -> unique hrefs matching regex (default social/app/tel/mailto)
import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
rx=sys.argv[2] if len(sys.argv)>2 else r'facebook|instagram|twitter|x\.com/|linkedin|youtube|tiktok|apps\.apple|play\.google|appgallery|telegram|t\.me/|whatsapp|wa\.me|mailto:|tel:'
seen=[]
for h in re.findall(r'''href\s*=\s*["']([^"']+)["']''',s):
    h=html.unescape(h)
    if re.search(rx,h,re.I) and h not in seen: seen.append(h)
for h in seen: print(h)
