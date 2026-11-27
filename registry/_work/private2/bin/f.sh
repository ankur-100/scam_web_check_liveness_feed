#!/bin/bash
# usage: f.sh OUTNAME URL   (saves to raw/OUTNAME, logs status)
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
W=/home/ankur/scamtrends_feed/registry/_work/private2
out="$W/raw/$1"; url="$2"
r=$(curl -sL -A "$UA" -H 'Accept-Language: en-SG,en;q=0.9' --compressed --max-time 30 -o "$out" -w '%{http_code} %{url_effective}' "$url")
echo "$r size=$(stat -c %s "$out" 2>/dev/null) -> $1"
echo "$(date -Is) $url $r" >> $W/fetchlog.txt
sleep 1.2
