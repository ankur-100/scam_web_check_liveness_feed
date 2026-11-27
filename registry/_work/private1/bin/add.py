#!/usr/bin/env python3
# usage: add.py REC.json  -> stores record in recs/, rebuilds entities_private_1.json, validates
import json,sys,os,subprocess
W='/home/ankur/scamtrends_feed/registry/_work/private1'
OUT='/home/ankur/scamtrends_feed/registry/entities_private_1.json'
ORDER=['dbs.com.sg','posb.com.sg','ocbc.com','uob.com.sg','abs.org.sg','abs.org.sg#paynow',
 'citibank.com.sg','hsbc.com.sg','sc.com','maybank2u.com.sg','trustbank.sg','gxs.com.sg','maribank.sg',
 'singtel.com','dash.com.sg','starhub.com','m1.com.sg','simba.sg','circles.life',
 'grab.com','gojek.com','comfortdelgro.com','smrt.com.sg','sbstransit.com.sg','ezlink.com.sg','nets.com.sg','spgroup.com.sg']
for fn in sys.argv[1:]:
    r=json.load(open(fn))
    recs=r if isinstance(r,list) else [r]
    for rec in recs:
        json.dump(rec,open(f"{W}/recs/{rec['entity_id'].replace('#','__')}.json",'w'),indent=1,ensure_ascii=False)
allr={}
for f in os.listdir(f'{W}/recs'):
    r=json.load(open(f'{W}/recs/{f}')); allr[r['entity_id']]=r
ids=[i for i in ORDER if i in allr]+sorted(i for i in allr if i not in ORDER)
tmp=OUT+'.tmp'; json.dump([allr[i] for i in ids],open(tmp,'w'),indent=1,ensure_ascii=False); os.replace(tmp,OUT)
p=subprocess.run(['python3','/home/ankur/scamtrends_feed/registry/validate_registry.py',OUT],capture_output=True,text=True)
print(p.stdout[-1500:])
