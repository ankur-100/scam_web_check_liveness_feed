#!/usr/bin/env bash
# Egress proxy for scam-site probes (SCOPE.md §6). Usage: bin/egress_proxy.sh start|stop|status
# Optional: SGINTEL_UPSTREAM_PROXY=http://[user:pass@]host:port to exit from another IP; SGINTEL_VANTAGE=<label>.
cd "$(dirname "$0")/.." || exit 1
PIDF=logs/egress_proxy.pid; mkdir -p logs
case "$1" in
  start) if [ -f $PIDF ] && kill -0 "$(cat $PIDF)" 2>/dev/null; then echo "running (pid $(cat $PIDF))"; exit 0; fi
         setsid nohup .venv/bin/python -m sgintel proxy >> logs/egress_proxy.out 2>&1 < /dev/null & echo $! > $PIDF; sleep 1
         kill -0 "$(cat $PIDF)" 2>/dev/null && echo "started (pid $(cat $PIDF))" && tail -1 logs/egress_proxy.out || { echo "failed"; tail -5 logs/egress_proxy.out; exit 1; } ;;
  stop)  [ -f $PIDF ] && kill "$(cat $PIDF)" 2>/dev/null && rm -f $PIDF && echo stopped || echo "not running" ;;
  status) [ -f $PIDF ] && kill -0 "$(cat $PIDF)" 2>/dev/null && echo "running (pid $(cat $PIDF))" && cat logs/egress_proxy.state.json || { echo "not running"; exit 1; } ;;
  *) echo "usage: $0 start|stop|status"; exit 2 ;;
esac
