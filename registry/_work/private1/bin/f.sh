#!/bin/bash
# usage: f.sh URL OUTFILE -> "code effective_url size <- URL" ; polite 1.2s pause; logs to fetchlog
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
r=$(curl -sL -A "$UA" -H "Accept-Language: en-SG,en;q=0.9" --compressed --max-time 30 -o "$2" -w '%{http_code} %{url_effective}' "$1")
echo "$r $(stat -c %s "$2" 2>/dev/null) <- $1"
echo "$(date -Is) $r <- $1" >> /home/ankur/scamtrends_feed/registry/_work/private1/fetchlog.txt
sleep 1.2
