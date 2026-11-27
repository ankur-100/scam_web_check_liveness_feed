#!/bin/bash
# usage: fetch.sh urls.txt out.tsv  -- one GET per official homepage, record status/final URL/title
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
while read -r u; do
  [ -z "$u" ] && continue
  body=$(curl -sS -L -m 20 -A "$UA" -o /dev/stdout -w '\n__META__%{http_code} %{url_effective}' "$u" 2>&1 | head -c 400000)
  meta=$(printf '%s' "$body" | grep -a '__META__' | tail -1 | sed 's/__META__//')
  title=$(printf '%s' "$body" | tr '\n' ' ' | grep -aoi '<title[^>]*>[^<]*' | head -1 | sed 's/<title[^>]*>//' | cut -c1-90)
  printf '%s\t%s\t%s\n' "$u" "$meta" "$title"
done < "$1" > "$2"
