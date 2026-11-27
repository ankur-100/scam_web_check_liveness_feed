import re,sys,subprocess,time
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
for url in sys.argv[1:]:
    p=subprocess.run(['curl','-sS','-L','-A',UA,'-m','40','--compressed','-w','\n__META__%{http_code}',url],capture_output=True)
    raw=p.stdout.decode('utf-8','replace'); i=raw.rfind('\n__META__'); code=raw[i+9:]; t=raw[:i]
    items=re.findall(r'<(item|entry)\b.*?</\1>',t,re.S|re.I)
    items=re.findall(r'<item\b.*?</item>|<entry\b.*?</entry>',t,re.S|re.I)
    def g(tag,s):
        m=re.search(rf'<{tag}[^>]*>(.*?)</{tag}>',s,re.S); return re.sub(r'<!\[CDATA\[|\]\]>','',m.group(1)).strip() if m else None
    dates=[g('pubDate',x) or g('updated',x) or g('published',x) for x in items]
    sc=[x for x in items if re.search(r'scam|fraud|phish|impersonat|fake',x,re.I)]
    print('==',url,'HTTP',code,'items',len(items),'scamkw',len(sc))
    print('   newest',dates[0] if dates else None,'| oldest',dates[-1] if dates else None)
    for x in sc[:6]: print('   *',(g('pubDate',x) or g('updated',x)),'|',(g('title',x) or '')[:110],'|',g('link',x) or re.search(r'href="([^"]+)"',x).group(1) if re.search(r'href="([^"]+)"',x) else g('link',x))
    time.sleep(1)
