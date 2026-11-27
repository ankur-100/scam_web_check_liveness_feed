# usage: python3 save.py NN_entityid < record.json  (record as JSON or python literal)
import json,sys,subprocess,ast
W='/home/ankur/scamtrends_feed/registry/_work/private2'
src=sys.stdin.read()
try: rec=json.loads(src)
except Exception: rec=ast.literal_eval(src)
json.dump(rec,open(f'{W}/ent/{sys.argv[1]}.json','w'),indent=1,ensure_ascii=False)
subprocess.run(['python3',f'{W}/bin/build.py'])
r=subprocess.run(['python3','/home/ankur/scamtrends_feed/registry/validate_registry.py','/home/ankur/scamtrends_feed/registry/entities_private_2.json'],capture_output=True,text=True)
print(r.stdout[-1500:],r.stderr[-500:])
