import json, collections, re, sys
rows=[json.loads(l) for l in open('/home/ankur/scamtrends_feed/advisories.jsonl')]
brands=json.load(open('/home/ankur/scamtrends_feed/registry/spf_brands.json'))
by=collections.defaultdict(list)
for r in rows:
    for b in r['impersonated_brands']:
        by[b].append(r)
def keys(bv):
    ks=set(); base=re.sub(r'\(.*?\)','',bv).strip(); ks.add(base.lower())
    m=re.search(r'\((.*?)\)',bv)
    if m: ks.add(m.group(1).lower())
    return [k for k in ks if k]
maxadv=int(sys.argv[2]) if len(sys.argv)>2 else 2
maxp=int(sys.argv[3]) if len(sys.argv)>3 else 2
L=int(sys.argv[4]) if len(sys.argv)>4 else 300
for i in [int(x) for x in sys.argv[1].split(',')]:
    b=brands[i]; bv=b['brand_value']; ks=keys(bv)
    print(f"#### [{i}] {bv} (n={b['count']})")
    for r in by[bv][:maxadv]:
        print(f"-- {r['title'][:110]} | {r['url'].split('/')[-1]}\n   brands={r['impersonated_brands']}")
        paras=[p.strip() for p in re.split(r'\n\s*\n|\n(?=\*|\-|\d+\.)',r['body_md']) if p.strip()]
        hits=[p for p in paras if any(k in p.lower() for k in ks)]
        if not hits: hits=paras[:1]; print('   (no mention)')
        for p in hits[:maxp]: print('   > '+p.replace('\n',' ')[:L])
