"""Egress proxy for scam-site liveness probes (SCOPE.md §6, decision D2). Every probe leaves through here; nothing else does.

Policy enforced here (not trusted to the client):
  * listens on loopback only; GET/HEAD for plain HTTP, CONNECT for HTTPS; ports 80/443 only
  * resolves the target itself and refuses non-global addresses (private, loopback, link-local incl. 169.254.169.254
    cloud metadata, CGNAT, multicast, reserved) - a scam domain pointed at internal space is a sinkhole, not a target
  * connects to the vetted IP (no second resolution -> no DNS-rebinding window)
  * per-connection byte cap and idle timeout; concurrency cap; one JSON line per decision in logs/egress.jsonl
  * optional upstream (SGINTEL_UPSTREAM_PROXY=http://[user:pass@]host:port) so probes exit from another IP;
    without it, probes exit from this host's IP (recorded as the vantage)
Errors are returned as "HTTP/1.1 <code> <Tag> <detail>" so the probe can tell policy blocks from network failures.
"""
import asyncio, base64, ipaddress, json, os, socket, time, urllib.parse
from .normalize import ROOT, iso, now
from . import doh

LISTEN = os.environ.get("SGINTEL_PROXY_LISTEN", "127.0.0.1:18080")
UPSTREAM = os.environ.get("SGINTEL_UPSTREAM_PROXY") or None
ALLOWED_PORTS = {80, 443}
MAX_BYTES, IDLE_S, CONNECT_S, MAX_CONC = 4 * 1024 * 1024, 30, 10, 16
LOG = ROOT / "logs" / "egress.jsonl"
STATE = ROOT / "logs" / "egress_proxy.state.json"
HOP_HEADERS = {"proxy-connection", "proxy-authorization", "connection", "keep-alive", "te", "trailer", "upgrade"}


def ip_ok(ip):
    a = ipaddress.ip_address(ip)
    if a.version == 6 and a.ipv4_mapped: a = a.ipv4_mapped
    return a.is_global and not a.is_multicast


def log(**kw):
    with open(LOG, "a") as f: f.write(json.dumps({"ts": iso(now()), **kw}) + "\n")


async def reply(w, code, tag, detail=""):
    w.write(f"HTTP/1.1 {code} {tag} {detail}".rstrip().encode() + b"\r\nX-SGIntel-Egress: " + tag.encode()
            + b"\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
    try: await w.drain()
    except ConnectionError: pass


async def vet(host, port):
    """-> (ip, None) or (None, (code, tag, detail))"""
    if port not in ALLOWED_PORTS: return None, (403, "Blocked", f"port_{port}")
    try: ips = [str(ipaddress.ip_address(host))]                  # literal IP
    except ValueError:
        d = await asyncio.get_running_loop().run_in_executor(None, doh.resolve, host)   # same resolver as liveness (doh.py)
        if d["rcode"] == "NXDOMAIN": return None, (502, "DNS", "nxdomain")
        if d["rcode"] == "DOH_ERROR":
            try: infos = await asyncio.get_running_loop().getaddrinfo(host, port, type=socket.SOCK_STREAM)
            except socket.gaierror as e: return None, (502, "DNS", f"error_{e.errno}")
            ips = list(dict.fromkeys(i[4][0] for i in infos))
        elif d["rcode"] != "NOERROR": return None, (502, "DNS", d["rcode"].lower())
        else: ips = d["a"] + d["aaaa"]
    bad = [ip for ip in ips if not ip_ok(ip)]
    if bad: return None, (403, "Blocked", f"non_global_ip:{bad[0]}")
    return ips[0], None


async def open_conn(host, ip, port):
    if not UPSTREAM:
        return await asyncio.wait_for(asyncio.open_connection(ip, port), CONNECT_S)
    u = urllib.parse.urlsplit(UPSTREAM)
    r, w = await asyncio.wait_for(asyncio.open_connection(u.hostname, u.port or 8080), CONNECT_S)
    auth = ""
    if u.username: auth = "Proxy-Authorization: Basic " + base64.b64encode(f"{urllib.parse.unquote(u.username)}:{urllib.parse.unquote(u.password or '')}".encode()).decode() + "\r\n"
    w.write(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n{auth}\r\n".encode()); await w.drain()
    head = await asyncio.wait_for(r.readuntil(b"\r\n\r\n"), CONNECT_S)
    if b" 200 " not in head.split(b"\r\n", 1)[0] + b" ":
        w.close(); raise ConnectionError("upstream refused: " + head.split(b"\r\n", 1)[0].decode(errors="replace")[:80])
    return r, w


async def pipe(r, w, budget):
    n = 0
    try:
        while n < budget:
            chunk = await asyncio.wait_for(r.read(65536), IDLE_S)
            if not chunk: break
            n += len(chunk); w.write(chunk); await w.drain()
    except (asyncio.TimeoutError, ConnectionError, asyncio.IncompleteReadError): pass
    finally:
        try: w.close()
        except Exception: pass
    return n


async def handle(cr, cw, sem):
    t0 = time.time(); rec = {"client": (cw.get_extra_info("peername") or ["?"])[0]}
    async with sem:
        try:
            head = await asyncio.wait_for(cr.readuntil(b"\r\n\r\n"), 15)
        except (asyncio.TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError, ConnectionError):
            cw.close(); return
        lines = head.decode("latin-1").split("\r\n"); method, target, _ = (lines[0].split(" ") + ["", ""])[:3]
        rec |= {"method": method}
        if method == "CONNECT":
            host, _, port = target.rpartition(":"); port = int(port) if port.isdigit() else 0
        elif method in ("GET", "HEAD") and target.startswith("http://"):
            u = urllib.parse.urlsplit(target); host, port = u.hostname or "", u.port or 80
        else:
            rec |= {"decision": "blocked", "why": "method_or_form"}; await reply(cw, 403, "Blocked", "method"); log(**rec); cw.close(); return
        rec |= {"host": host, "port": port}
        ip, err = await vet(host.strip("[]"), port)
        if err:
            rec |= {"decision": "refused", "why": f"{err[1]}:{err[2]}"}; await reply(cw, *err); log(**rec, ms=int((time.time() - t0) * 1000)); cw.close(); return
        rec["ip"] = ip
        try:
            ur, uw = await open_conn(host, ip, port)
        except asyncio.TimeoutError:
            rec |= {"decision": "failed", "why": "connect_timeout"}; await reply(cw, 504, "Connect", "timeout"); log(**rec); cw.close(); return
        except (ConnectionRefusedError,) as e:
            rec |= {"decision": "failed", "why": "connect_refused"}; await reply(cw, 502, "Connect", "refused"); log(**rec); cw.close(); return
        except OSError as e:
            why = "unreachable" if "unreachable" in str(e).lower() else f"error_{type(e).__name__}"
            rec |= {"decision": "failed", "why": why}; await reply(cw, 502, "Connect", why); log(**rec); cw.close(); return
        if method == "CONNECT":
            cw.write(b"HTTP/1.1 200 Connection established\r\n\r\n"); await cw.drain()
        else:
            u = urllib.parse.urlsplit(target); path = (u.path or "/") + ("?" + u.query if u.query else "")
            hdrs = [l for l in lines[1:] if l and l.split(":", 1)[0].strip().lower() not in HOP_HEADERS]
            uw.write((f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(hdrs) + "\r\nConnection: close\r\n\r\n").encode("latin-1")); await uw.drain()
        up, down = await asyncio.gather(pipe(cr, uw, 256 * 1024), pipe(ur, cw, MAX_BYTES))
        log(**rec, decision="allowed", via="upstream" if UPSTREAM else "direct", bytes_up=up, bytes_down=down, ms=int((time.time() - t0) * 1000))


async def serve():
    host, port = LISTEN.rsplit(":", 1)
    if host not in ("127.0.0.1", "::1", "localhost"): raise SystemExit("egress proxy must listen on loopback")
    LOG.parent.mkdir(exist_ok=True)
    sem = asyncio.Semaphore(MAX_CONC)
    srv = await asyncio.start_server(lambda r, w: handle(r, w, sem), host, int(port), limit=16384)
    label = os.environ.get("SGINTEL_VANTAGE") or ("upstream:" + urllib.parse.urlsplit(UPSTREAM).hostname if UPSTREAM else f"direct:{socket.gethostname()}")
    STATE.write_text(json.dumps({"listen": LISTEN, "upstream": bool(UPSTREAM), "vantage": label, "pid": os.getpid(), "started_at": iso(now())}))
    print(f"egress proxy on {LISTEN} | vantage={label} | log={LOG}", flush=True)
    async with srv: await srv.serve_forever()


def main(): asyncio.run(serve())
