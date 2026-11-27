import json,glob,os
W='/home/ankur/scamtrends_feed/registry/_work/private2/ent'
recs=[json.load(open(f)) for f in sorted(glob.glob(W+'/*.json'))]
out='/home/ankur/scamtrends_feed/registry/entities_private_2.json'
json.dump(recs,open(out,'w'),indent=1,ensure_ascii=False)
print(len(recs),'records ->',out)
