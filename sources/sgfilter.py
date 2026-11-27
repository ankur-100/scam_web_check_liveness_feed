#!/usr/bin/env python3
"""SG-signal tagger for URL / domain lists.

Usage: sgfilter.py NAME FILE [FILE...]   (one URL or domain per line; JSON list ok)
Prints per-token hit counts (tiered) and examples.
Tiers:
  A  = SG-native, high precision (unique SG brand / ccTLD / SG gov term)
  B  = SG brand but ambiguous short token (dbs, uob, lta, iras, ica, cpf, grab, hdb, mom) -> counted
       raw AND "with SG context" (co-occurs with sg/singapore/gov-sg/.sg in the same host/URL)
  R  = SEA-regional brands (shopee, lazada, grab*) - not SG-specific
"""
import json, re, sys, collections
from urllib.parse import urlsplit

B = r'(?<![a-z0-9])'   # left boundary (non-alnum)
E = r'(?![a-z0-9])'    # right boundary

TIER_A = {
    'ccTLD .sg':      r'\.sg(?=$|[:/?#])',
    'singpass':       r'(?<![a-z0-9])(my)?singpass',
    'singpost':       r'singpost|sgpost|singapore-?post',
    'ocbc':           B + r'(my)?ocbc',
    'posb':           B + B + r'posb(?=bank|[^a-z0-9]|$)',
    'dbs-bank':       r'dbsbank|dbs-?bank|digibank|paylah|' + B + r'(dbs-?sg|sg-?dbs)' + E,
    'uob-sg':         r'uobgroup|uob-?bank|' + B + r'(uob-?sg|sg-?uob)' + E,
    'ninjavan':       r'ninja-?van',
    'carousell':      r'carou-?sell',
    'simplygo':       r'simply-?go',
    'singtel':        r'singtel',
    'starhub':        r'starhub',
    'onemotoring/lta':r'onemotoring|one-motoring|' + B + r'(lta-?gov|lta-?sg|sg-?lta)' + E,
    'ezlink':         B + r'ez-?link',
    'paynow':         B + r'paynow',
    'cdc-voucher':    r'cdc-?voucher|redeem-?cdc|' + B + r'cdc-?sg' + E,
    'cpf-sg':         B + r'(cpf-?board|cpf-?sg|sg-?cpf|cpf-?gov)' + E,
    'iras-sg':        B + r'(iras-?gov|iras-?sg|sg-?iras)' + E,
    'ica-sg':         r'sgarrival|sg-arrival|' + B + r'(ica-?gov|ica-?sg|sg-?ica)' + E,
    'gov-sg term':    B + r'(gov-?sg|govsg|sg-?gov)' + E + r'|\.gov\.sg',
    'singapore':      r'(?<!ap-)(?<!ap)singapore|singapura',
    'spf/police':     B + r'(police-?sg|sg-?police|spf-?gov)' + E,
    'hdb-sg':         B + r'(hdb-?gov|hdb-?sg|sg-?hdb|myhdb)' + E,
}
TIER_B = {   # ambiguous short tokens, word-bounded
    'dbs': B + r'dbs' + E,
    'uob': B + r'uob' + E,
    'lta': B + r'lta' + E,
    'iras': B + r'iras' + E,
    'ica': B + r'ica' + E,
    'cpf': B + r'cpf' + E,
    'hdb': B + r'hdb' + E,
    'grab': B + r'grab(pay|food|car|taxi)?' + E,
    'mytax(IRAS portal or US/UK tax)': B + r'mytax',
}
TIER_R = {
    'shopee': r'shopee',
    'lazada': r'lazada',
}
SG_CTX = re.compile(r'(?<![a-z0-9])sg(?![a-z0-9])|singapore|\.sg(?=$|[:/?#])|gov-?sg|sgd' )

def load(paths):
    for p in paths:
        with open(p, encoding='utf-8', errors='replace') as f:
            head = f.read(1)
            f.seek(0)
            if head == '[':
                for x in json.load(f):
                    yield str(x)
            else:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(('#', '!')):
                        yield line

def norm(s):
    s = s.lower()
    if '://' not in s:
        s = 'http://' + s
    try:
        u = urlsplit(s)
        host = (u.hostname or '')
        return host, host + u.path + ('?' + u.query if u.query else '')
    except Exception:
        return s, s

def main():
    name, files = sys.argv[1], sys.argv[2:]
    comp = {t: {k: re.compile(v) for k, v in d.items()} for t, d in
            (('A', TIER_A), ('B', TIER_B), ('R', TIER_R))}
    n = 0
    hits = collections.defaultdict(list)
    anyA, anyBctx, anyR = set(), set(), set()
    tgtd = set()
    for raw in load(files):
        n += 1
        host, full = norm(raw)
        for k, rx in comp['A'].items():
            tgt = host if k == 'ccTLD .sg' else full
            m = rx.search(tgt)
            if m and k != 'ccTLD .sg':
                a, b = m.start(), m.end()
                while a > 0 and tgt[a-1].isalnum(): a -= 1
                while b < len(tgt) and tgt[b].isalnum(): b += 1
                if b - a > 24:   # brand buried in random hash/base64 -> noise
                    m = None
            if m:
                hits['A:' + k].append(raw); anyA.add(raw)
                if k != 'ccTLD .sg': tgtd.add(raw)
        ctx = bool(SG_CTX.search(full))
        for k, rx in comp['B'].items():
            if rx.search(full):
                hits['B:' + k].append(raw)
                if ctx:
                    hits['B:' + k + '+sgctx'].append(raw); anyBctx.add(raw)
        for k, rx in comp['R'].items():
            if rx.search(full):
                hits['R:' + k].append(raw); anyR.add(raw)
    uh = {norm(x)[0] for x in anyA}
    th = {norm(x)[0] for x in tgtd}
    print(f'   SG-TARGETED (TierA excl. ccTLD-only) entries = {len(tgtd)}, unique hosts = {len(th)}')
    print(f'   unique hosts in TierA = {len(uh)}; non-.sg TierA hosts = {len([h for h in uh if not h.endswith(".sg")])}')
    print(f'== {name}: {n} entries | TierA-any={len(anyA)} | TierB+SGctx={len(anyBctx - anyA)} (extra) | Regional={len(anyR)}')
    for k in sorted(hits):
        v = hits[k]
        ex = list(dict.fromkeys(v))[:4]
        print(f'  {k:22s} {len(v):6d}  e.g. {ex}')

if __name__ == '__main__':
    main()
