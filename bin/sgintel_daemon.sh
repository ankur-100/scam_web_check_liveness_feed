#!/usr/bin/env bash
# Continuous polling (SCOPE.md): crawl due publisher endpoints -> post-crawl cycle (roles, follow-up, targets, new sites)
# -> due site checks via the egress proxy. Usage: bin/sgintel_daemon.sh start|stop|status
cd "$(dirname "$0")/.." || exit 1
PIDF=logs/sgintel_daemon.pid; mkdir -p logs
case "$1" in
  start) bin/egress_proxy.sh status >/dev/null || { echo "egress proxy not running: bin/egress_proxy.sh start"; exit 1; }
         if [ -f $PIDF ] && kill -0 "$(cat $PIDF)" 2>/dev/null; then echo "running (pid $(cat $PIDF))"; exit 0; fi
         setsid nohup .venv/bin/python -m sgintel daemon >> logs/sgintel_daemon.log 2>&1 < /dev/null & echo $! > $PIDF; sleep 1
         kill -0 "$(cat $PIDF)" 2>/dev/null && echo "started (pid $(cat $PIDF)); log: logs/sgintel_daemon.log" || { echo failed; tail -5 logs/sgintel_daemon.log; exit 1; } ;;
  stop)  [ -f $PIDF ] && kill "$(cat $PIDF)" 2>/dev/null && rm -f $PIDF && echo stopped || echo "not running" ;;
  status) [ -f $PIDF ] && kill -0 "$(cat $PIDF)" 2>/dev/null && echo "running (pid $(cat $PIDF))" || { echo "not running"; exit 1; } ;;
  *) echo "usage: $0 start|stop|status"; exit 2 ;;
esac
