"""autoMate CLI — a smart NAS for AI.

    automate serve            # start the warehouse (browser auto-opens)
    automate mcp              # expose every tool/store over stdio MCP
    automate doctor           # show paths, configured providers, integrations
    automate relay <url>      # open a reverse tunnel for remote access
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
import time
import webbrowser

from .settings import PATHS, SERVER
from .version import __version__


def _serve(args: argparse.Namespace) -> int:
    try:
        import uvicorn
    except ImportError:
        sys.stderr.write("uvicorn not installed. Run: pip install 'autoMate[server]'\n")
        return 1
    from .server import create_app

    PATHS.ensure()
    app = create_app()
    host, port = args.host or SERVER.host, args.port or SERVER.port
    url = f"http://{host}:{port}"

    if args.open and not args.no_open:
        def _open():
            time.sleep(1.0)
            try:
                webbrowser.open(url)
            except Exception:  # noqa: BLE001
                pass
        threading.Thread(target=_open, daemon=True).start()

    bar = "═" * 56
    print(f"\n  ╔{bar}╗")
    print(f"  ║   autoMate v{__version__}".ljust(60) + "║")
    print(f"  ║   Open this in your browser: {url}".ljust(60) + "║")
    print(f"  ║   Data dir: {PATHS.home}".ljust(60) + "║")
    print(f"  ║   Press Ctrl+C to stop.".ljust(60) + "║")
    print(f"  ╚{bar}╝\n")
    uvicorn.run(app, host=host, port=port, log_level="info")
    return 0


def _mcp(_args: argparse.Namespace) -> int:
    from .server.mcp_bridge import serve_stdio
    serve_stdio()
    return 0


def _relay(args: argparse.Namespace) -> int:
    from .relay import run
    return run(args.relay_url, token=args.token, local_url=args.local)


def _doctor(_args: argparse.Namespace) -> int:
    from .server.state import build_state
    state = build_state()
    print(f"autoMate v{__version__}")
    print(f"data dir: {PATHS.home}")
    print(f"db:       {PATHS.db}")
    print()
    providers = state.db.list_providers()
    configured = [p for p in providers if p["api_key_set"]]
    print(f"providers: {len(providers)} known, {len(configured)} configured")
    for p in configured:
        print(f"  ✓ {p['display_name']} ({p['default_model'] or '?'})")
    active = state.providers.active_provider_id()
    print(f"  active: {active or '(none)'}")
    print()
    conns = [c for c in state.db.list_connections() if c["status"] == "connected"]
    print(f"integrations connected: {len(conns)}")
    for c in conns:
        print(f"  ✓ {c['display_name']}  [{c['auth_kind']}]")
    print()
    print(f"tools registered: {len(state.registry.all())}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="automate", description=f"autoMate v{__version__} — a smart NAS for AI")
    sub = parser.add_subparsers(dest="cmd")

    p_serve = sub.add_parser("serve", help="run the web UI + HTTP API + WebSocket")
    p_serve.add_argument("--host", default=None)
    p_serve.add_argument("--port", type=int, default=None)
    p_serve.add_argument("--open", dest="open", action="store_true", default=True)
    p_serve.add_argument("--no-open", dest="no_open", action="store_true")
    p_serve.add_argument("--trace", action="store_true", help="record local tool execution traces")
    p_serve.set_defaults(func=_serve)

    p_mcp = sub.add_parser("mcp", help="expose tools as a stdio MCP server")
    p_mcp.add_argument("--trace", action="store_true", help="record local tool execution traces")
    p_mcp.set_defaults(func=_mcp)

    p_doctor = sub.add_parser("doctor", help="print runtime status and config")
    p_doctor.set_defaults(func=_doctor)

    p_relay = sub.add_parser("relay", help="open a reverse tunnel to a remote relay (advanced)")
    p_relay.add_argument("relay_url", help="ws(s):// URL of the relay tunnel endpoint")
    p_relay.add_argument("--token", default=None, help="bearer token for the relay (or AUTOMATE_RELAY_TOKEN env var)")
    p_relay.add_argument("--local", default=None, help="local hub URL (default: http://127.0.0.1:8765)")
    p_relay.set_defaults(func=_relay)

    if argv is None:
        argv = sys.argv[1:]
    # Double-clicking automate.exe lands here with no subcommand. Most users
    # expect a UI to open, not a help screen — so default to `serve`.
    if not argv:
        argv = ["serve"]

    args = parser.parse_args(argv)
    if getattr(args, "trace", False):
        os.environ["AUTOMATE_DEVTOOLS"] = "true"
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
