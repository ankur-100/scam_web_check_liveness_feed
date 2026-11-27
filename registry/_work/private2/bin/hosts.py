import re,sys,collections
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
c=collections.Counter(h.lower() for h in re.findall(r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',s))
print(sorted(c.items(),key=lambda x:-x[1])[:60])
