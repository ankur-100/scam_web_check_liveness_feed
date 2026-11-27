#!/usr/bin/env python3
"""Query crt.sh JSON for an identity (domain or %.domain); retry once on failure; save raw JSON.
usage: crtsh.py <outdir> <pattern> [<pattern> ...]
"""
import json, os, re, sys, time, urllib.parse
import requests

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")

def fname(outdir, pat):
    return os.path.join(outdir, "crtsh_" + re.sub(r"[^A-Za-z0-9.-]", "_", pat) + ".json")

def fetch(outdir, pat, timeout=150):
    url = "https://crt.sh/?q=" + urllib.parse.quote(pat, safe="") + "&output=json"
    last = None
    for attempt in (1, 2):  # retry once only
        t0 = time.time()
        try:
            r = requests.get(url, headers={"User-Agent": UA, "Accept": "application/json"}, timeout=timeout)
            dt = time.time() - t0
            if r.status_code == 200:
                try:
                    data = r.json()
                except ValueError:
                    data = None
                    last = f"HTTP 200 non-JSON ({len(r.content)}B) in {dt:.0f}s"
                if data is not None:
                    with open(fname(outdir, pat), "w") as f:
                        json.dump(data, f)
                    return f"OK rows={len(data)} in {dt:.0f}s (attempt {attempt})"
            else:
                last = f"HTTP {r.status_code} in {dt:.0f}s"
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:120]}"
        if attempt == 1:
            time.sleep(8)
    return "FAIL " + str(last)

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for p in sys.argv[2:]:
        print(f"{p}\t{fetch(outdir, p)}", flush=True)
        time.sleep(3)
